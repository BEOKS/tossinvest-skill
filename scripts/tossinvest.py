#!/usr/bin/env python3
"""CLI helper for the Toss Securities Open API."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OPENAPI_PATH = ROOT / "references" / "openapi.json"
DEFAULT_BASE_URL = "https://openapi.tossinvest.com"
TOKEN_SKEW_SECONDS = 60

CLIENT_ID_ENV = ("TOSS_API_KEY", "TOSSINVEST_CLIENT_ID", "TOSS_CLIENT_ID")
CLIENT_SECRET_ENV = ("TOSS_SECRET_KEY", "TOSSINVEST_CLIENT_SECRET", "TOSS_CLIENT_SECRET")
ACCOUNT_ENV = ("TOSSINVEST_ACCOUNT", "TOSS_ACCOUNT", "TOSS_ACCOUNT_SEQ")
TRUE_VALUES = {"1", "true", "yes", "y", "on"}
RATE_HEADER_NAMES = (
    "x-request-id",
    "cf-ray",
    "x-ratelimit-limit",
    "x-ratelimit-remaining",
    "x-ratelimit-reset",
    "retry-after",
)
SHELL_ENV_CACHE: dict[str, str] | None = None


class TossApiError(Exception):
    def __init__(self, status: int, headers: dict[str, str], body: Any):
        self.status = status
        self.headers = headers
        self.body = body
        super().__init__(f"Toss API request failed with HTTP {status}")


def env_first(names: tuple[str, ...]) -> str | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    shell_env = load_shell_env()
    for name in names:
        value = shell_env.get(name)
        if value:
            return value
    return None


def load_shell_env() -> dict[str, str]:
    global SHELL_ENV_CACHE
    if SHELL_ENV_CACHE is not None:
        return SHELL_ENV_CACHE

    wanted = set(CLIENT_ID_ENV + CLIENT_SECRET_ENV + ACCOUNT_ENV)
    values: dict[str, str] = {}
    for rc_path in (Path.home() / ".zshrc", Path.home() / ".zprofile", Path.home() / ".profile"):
        try:
            lines = rc_path.read_text().splitlines()
        except OSError:
            continue
        for raw_line in lines:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export ") :].strip()
            elif line.startswith("typeset -x "):
                line = line[len("typeset -x ") :].strip()
            try:
                tokens = shlex.split(line, comments=True, posix=True)
            except ValueError:
                continue
            for token in tokens:
                if "=" not in token:
                    continue
                key, value = token.split("=", 1)
                if key in wanted and value:
                    values[key] = value
    SHELL_ENV_CACHE = values
    return values


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def parse_key_value(items: list[str] | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in items or []:
        if "=" not in item:
            raise SystemExit(f"Expected KEY=VALUE, got: {item}")
        key, value = item.split("=", 1)
        if not key:
            raise SystemExit(f"Empty query key in: {item}")
        result[key] = value
    return result


def parse_json_object(raw: str | None) -> dict[str, Any] | None:
    if raw is None:
        return None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise SystemExit("--body-json must be a JSON object")
    return parsed


def normalize_symbols(raw: str) -> str:
    symbols = [part.strip() for part in raw.replace(" ", ",").split(",") if part.strip()]
    if not symbols:
        raise SystemExit("At least one symbol is required")
    if len(symbols) > 200:
        raise SystemExit("Toss Open API accepts at most 200 symbols per request")
    return ",".join(symbols)


def account_arg(args: argparse.Namespace) -> str:
    account = getattr(args, "account", None) or env_first(ACCOUNT_ENV)
    if not account:
        names = ", ".join(ACCOUNT_ENV)
        raise SystemExit(f"Account sequence is required. Pass --account or set one of: {names}")
    return str(account)


def token_cache_path() -> Path | None:
    override = os.environ.get("TOSSINVEST_TOKEN_CACHE")
    if override:
        if override.lower() in {"none", "off", "false", "0"}:
            return None
        return Path(override).expanduser()
    base = os.environ.get("XDG_CACHE_HOME")
    cache_root = Path(base).expanduser() if base else Path.home() / ".cache"
    return cache_root / "tossinvest-skill" / "token.json"


def client_hash(client_id: str) -> str:
    return hashlib.sha256(client_id.encode("utf-8")).hexdigest()


def load_token_cache(client_id: str) -> str | None:
    path = token_cache_path()
    if path is None or not path.exists():
        return None
    try:
        cached = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    if cached.get("client_id_sha256") != client_hash(client_id):
        return None
    expires_at = float(cached.get("expires_at", 0))
    if expires_at <= time.time() + TOKEN_SKEW_SECONDS:
        return None
    token = cached.get("access_token")
    return token if isinstance(token, str) and token else None


def save_token_cache(client_id: str, token: str, expires_in: int) -> None:
    path = token_cache_path()
    if path is None:
        return
    payload = {
        "client_id_sha256": client_hash(client_id),
        "access_token": token,
        "expires_at": int(time.time()) + int(expires_in),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    try:
        path.chmod(0o600)
    except OSError:
        pass


def request_json(
    method: str,
    path: str,
    *,
    query: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
    account: str | None = None,
    auth: bool = True,
    args: argparse.Namespace,
) -> tuple[int, dict[str, str], Any]:
    base_url = args.base_url.rstrip("/")
    if not path.startswith("/"):
        path = "/" + path
    filtered_query = {
        key: bool_text(value) if isinstance(value, bool) else value
        for key, value in (query or {}).items()
        if value is not None
    }
    url = base_url + path
    if filtered_query:
        url += "?" + urlencode(filtered_query)

    headers = {
        "Accept": "application/json",
        "User-Agent": "tossinvest-skill/1.0",
    }
    data = None
    if auth:
        headers["Authorization"] = f"Bearer {get_access_token(args)}"
    if account is not None:
        headers["X-Tossinvest-Account"] = str(account)
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")

    request = Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urlopen(request, timeout=args.timeout) as response:
            response_body = response.read()
            response_headers = normalized_headers(response.headers)
            return response.status, response_headers, decode_body(response_body)
    except HTTPError as exc:
        response_body = exc.read()
        raise TossApiError(exc.code, normalized_headers(exc.headers), decode_body(response_body)) from exc
    except URLError as exc:
        raise SystemExit(f"Network error: {exc.reason}") from exc


def normalized_headers(headers: Any) -> dict[str, str]:
    return {str(key).lower(): str(value) for key, value in headers.items()}


def decode_body(raw: bytes) -> Any:
    if not raw:
        return None
    text = raw.decode("utf-8", errors="replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def selected_headers(headers: dict[str, str]) -> dict[str, str]:
    return {name: headers[name] for name in RATE_HEADER_NAMES if name in headers}


def get_access_token(args: argparse.Namespace) -> str:
    client_id = env_first(CLIENT_ID_ENV)
    client_secret = env_first(CLIENT_SECRET_ENV)
    if not client_id or not client_secret:
        raise SystemExit("Missing Toss credentials. Set TOSS_API_KEY and TOSS_SECRET_KEY.")

    if not args.refresh_token and not args.no_token_cache:
        cached = load_token_cache(client_id)
        if cached:
            return cached

    form = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    data = urlencode(form).encode("utf-8")
    url = args.base_url.rstrip("/") + "/oauth2/token"
    request = Request(
        url,
        data=data,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "tossinvest-skill/1.0",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=args.timeout) as response:
            payload = decode_body(response.read())
    except HTTPError as exc:
        raise TossApiError(exc.code, normalized_headers(exc.headers), decode_body(exc.read())) from exc
    except URLError as exc:
        raise SystemExit(f"Network error while issuing token: {exc.reason}") from exc

    if not isinstance(payload, dict) or not payload.get("access_token"):
        raise SystemExit(f"Unexpected token response: {payload!r}")
    token = str(payload["access_token"])
    expires_in = int(payload.get("expires_in", 0) or 0)
    if not args.no_token_cache and expires_in > TOKEN_SKEW_SECONDS:
        save_token_cache(client_id, token, expires_in)
    return token


def redact_token(token: str) -> str:
    if len(token) <= 16:
        return "***"
    return token[:8] + "..." + token[-6:]


def emit(payload: Any, args: argparse.Namespace, *, status: int | None = None, headers: dict[str, str] | None = None) -> None:
    if args.include_headers:
        payload = {
            "status": status,
            "headers": selected_headers(headers or {}),
            "body": payload,
        }
    if args.compact:
        print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


def load_openapi() -> dict[str, Any]:
    try:
        return json.loads(OPENAPI_PATH.read_text())
    except FileNotFoundError as exc:
        raise SystemExit(f"OpenAPI file not found: {OPENAPI_PATH}") from exc


def cmd_list_endpoints(args: argparse.Namespace) -> None:
    spec = load_openapi()
    endpoints = []
    for path, methods in spec.get("paths", {}).items():
        for method, operation in methods.items():
            tags = operation.get("tags", [])
            if args.tag and args.tag not in tags:
                continue
            endpoints.append(
                {
                    "method": method.upper(),
                    "path": path,
                    "operationId": operation.get("operationId"),
                    "tags": tags,
                    "summary": operation.get("summary"),
                }
            )
    emit(
        {
            "title": spec.get("info", {}).get("title"),
            "version": spec.get("info", {}).get("version"),
            "baseUrl": spec.get("servers", [{}])[0].get("url"),
            "endpoints": endpoints,
        },
        args,
    )


def cmd_schema(args: argparse.Namespace) -> None:
    spec = load_openapi()
    schemas = spec.get("components", {}).get("schemas", {})
    schema = schemas.get(args.name)
    if schema is None:
        available = sorted(schemas)
        raise SystemExit(f"Unknown schema {args.name!r}. Available: {', '.join(available)}")
    emit(schema, args)


def cmd_token(args: argparse.Namespace) -> None:
    token = get_access_token(args)
    payload: dict[str, Any] = {"token_type": "Bearer", "access_token": token if args.show_token else redact_token(token)}
    emit(payload, args)


def call_get(args: argparse.Namespace, path: str, query: dict[str, Any] | None = None, account: str | None = None) -> None:
    status, headers, body = request_json("GET", path, query=query, account=account, args=args)
    emit(body, args, status=status, headers=headers)


def cmd_orderbook(args: argparse.Namespace) -> None:
    call_get(args, "/api/v1/orderbook", {"symbol": args.symbol})


def cmd_prices(args: argparse.Namespace) -> None:
    call_get(args, "/api/v1/prices", {"symbols": normalize_symbols(args.symbols)})


def cmd_trades(args: argparse.Namespace) -> None:
    call_get(args, "/api/v1/trades", {"symbol": args.symbol, "count": args.count})


def cmd_price_limits(args: argparse.Namespace) -> None:
    call_get(args, "/api/v1/price-limits", {"symbol": args.symbol})


def cmd_candles(args: argparse.Namespace) -> None:
    call_get(
        args,
        "/api/v1/candles",
        {
            "symbol": args.symbol,
            "interval": args.interval,
            "count": args.count,
            "before": args.before,
            "adjusted": args.adjusted,
        },
    )


def cmd_stocks(args: argparse.Namespace) -> None:
    call_get(args, "/api/v1/stocks", {"symbols": normalize_symbols(args.symbols)})


def cmd_warnings(args: argparse.Namespace) -> None:
    call_get(args, f"/api/v1/stocks/{args.symbol}/warnings")


def cmd_exchange_rate(args: argparse.Namespace) -> None:
    call_get(
        args,
        "/api/v1/exchange-rate",
        {
            "dateTime": args.date_time,
            "baseCurrency": args.base,
            "quoteCurrency": args.quote,
        },
    )


def cmd_market_calendar(args: argparse.Namespace) -> None:
    call_get(args, f"/api/v1/market-calendar/{args.country}", {"date": args.date})


def cmd_accounts(args: argparse.Namespace) -> None:
    call_get(args, "/api/v1/accounts")


def cmd_holdings(args: argparse.Namespace) -> None:
    call_get(args, "/api/v1/holdings", {"symbol": args.symbol}, account_arg(args))


def cmd_orders(args: argparse.Namespace) -> None:
    call_get(
        args,
        "/api/v1/orders",
        {
            "status": args.status,
            "symbol": args.symbol,
            "from": args.from_date,
            "to": args.to_date,
            "cursor": args.cursor,
            "limit": args.limit,
        },
        account_arg(args),
    )


def cmd_order(args: argparse.Namespace) -> None:
    call_get(args, f"/api/v1/orders/{args.order_id}", account=account_arg(args))


def cmd_buying_power(args: argparse.Namespace) -> None:
    call_get(args, "/api/v1/buying-power", {"currency": args.currency}, account_arg(args))


def cmd_sellable_quantity(args: argparse.Namespace) -> None:
    call_get(args, "/api/v1/sellable-quantity", {"symbol": args.symbol}, account_arg(args))


def cmd_commissions(args: argparse.Namespace) -> None:
    call_get(args, "/api/v1/commissions", account=account_arg(args))


def dry_run_payload(method: str, path: str, account: str | None, body: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "dryRun": True,
        "method": method,
        "path": path,
        "account": account,
        "body": body or {},
        "executeHint": (
            "Re-run with --execute --yes after explicit confirmation, or while operating "
            "under a user-delegated autonomous trading instruction."
        ),
    }


def execute_mutation(
    args: argparse.Namespace,
    *,
    method: str,
    path: str,
    body: dict[str, Any] | None = None,
    account: str | None = None,
) -> None:
    if not args.execute:
        emit(dry_run_payload(method, path, account, body), args)
        return
    if not args.yes:
        raise SystemExit("Live order mutations require both --execute and --yes")
    status, headers, response_body = request_json(method, path, body=body, account=account, args=args)
    emit(response_body, args, status=status, headers=headers)


def cmd_create_order(args: argparse.Namespace) -> None:
    if bool(args.quantity) == bool(args.order_amount):
        raise SystemExit("Pass exactly one of --quantity or --order-amount")
    if args.order_amount and args.order_type != "MARKET":
        raise SystemExit("--order-amount is only valid with --order-type MARKET")
    if args.order_type == "LIMIT" and not args.price:
        raise SystemExit("--price is required for LIMIT orders")
    if args.order_type == "MARKET" and args.price:
        raise SystemExit("--price is not valid for MARKET orders")
    if args.execute and not args.client_order_id and not args.allow_no_client_order_id:
        raise SystemExit("Live create-order requires --client-order-id or --allow-no-client-order-id")

    body: dict[str, Any] = {
        "symbol": args.symbol,
        "side": args.side,
        "orderType": args.order_type,
    }
    optional_fields = {
        "clientOrderId": args.client_order_id,
        "timeInForce": args.time_in_force,
        "quantity": args.quantity,
        "orderAmount": args.order_amount,
        "price": args.price,
    }
    for key, value in optional_fields.items():
        if value is not None:
            body[key] = value
    if args.confirm_high_value_order:
        body["confirmHighValueOrder"] = True

    execute_mutation(args, method="POST", path="/api/v1/orders", body=body, account=account_arg(args))


def cmd_modify_order(args: argparse.Namespace) -> None:
    if args.order_type == "LIMIT" and not args.price:
        raise SystemExit("--price is required for LIMIT modifications")
    if args.order_type == "MARKET" and args.price:
        raise SystemExit("--price is not valid for MARKET modifications")
    body: dict[str, Any] = {"orderType": args.order_type}
    for key, value in (("quantity", args.quantity), ("price", args.price)):
        if value is not None:
            body[key] = value
    if args.confirm_high_value_order:
        body["confirmHighValueOrder"] = True
    execute_mutation(
        args,
        method="POST",
        path=f"/api/v1/orders/{args.order_id}/modify",
        body=body,
        account=account_arg(args),
    )


def cmd_cancel_order(args: argparse.Namespace) -> None:
    execute_mutation(
        args,
        method="POST",
        path=f"/api/v1/orders/{args.order_id}/cancel",
        body={},
        account=account_arg(args),
    )


def cmd_request(args: argparse.Namespace) -> None:
    query = parse_key_value(args.query)
    body = parse_json_object(args.body_json)
    method = args.method.upper()
    account = args.account or None
    if method not in {"GET", "HEAD"} and not args.execute:
        emit(dry_run_payload(method, args.path, account, body), args)
        return
    if method not in {"GET", "HEAD"} and not args.yes:
        raise SystemExit("Mutating generic requests require both --execute and --yes")
    status, headers, response_body = request_json(
        method,
        args.path,
        query=query,
        body=body,
        account=account,
        auth=not args.no_auth,
        args=args,
    )
    emit(response_body, args, status=status, headers=headers)


def add_common_account(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--account", help="Toss accountSeq for X-Tossinvest-Account")


def add_mutation_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--execute", action="store_true", help="execute live order mutation")
    parser.add_argument(
        "--yes",
        action="store_true",
        help="confirm live mutation after explicit confirmation or under delegated autonomous trading",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Toss Securities Open API CLI")
    parser.add_argument("--base-url", default=os.environ.get("TOSSINVEST_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--timeout", type=float, default=float(os.environ.get("TOSSINVEST_TIMEOUT", "30")))
    parser.add_argument("--refresh-token", action="store_true", help="ignore cached token and issue a new one")
    parser.add_argument("--no-token-cache", action="store_true", help="do not read or write token cache")
    parser.add_argument("--include-headers", action="store_true", help="wrap output with status and selected response headers")
    parser.add_argument("--compact", action="store_true", help="print compact JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p = subparsers.add_parser("list-endpoints", help="list endpoints from bundled OpenAPI JSON")
    p.add_argument("--tag", help="filter by OpenAPI tag, for example 'Order Info'")
    p.set_defaults(func=cmd_list_endpoints)

    p = subparsers.add_parser("schema", help="print a schema from bundled OpenAPI JSON")
    p.add_argument("name")
    p.set_defaults(func=cmd_schema)

    p = subparsers.add_parser("token", help="issue or reuse OAuth2 token")
    p.add_argument("--show-token", action="store_true", help="print full access token")
    p.set_defaults(func=cmd_token)

    p = subparsers.add_parser("orderbook", help="GET /api/v1/orderbook")
    p.add_argument("--symbol", required=True)
    p.set_defaults(func=cmd_orderbook)

    p = subparsers.add_parser("prices", help="GET /api/v1/prices")
    p.add_argument("--symbols", required=True, help="comma-separated symbols, max 200")
    p.set_defaults(func=cmd_prices)

    p = subparsers.add_parser("trades", help="GET /api/v1/trades")
    p.add_argument("--symbol", required=True)
    p.add_argument("--count", type=int, default=50)
    p.set_defaults(func=cmd_trades)

    p = subparsers.add_parser("price-limits", help="GET /api/v1/price-limits")
    p.add_argument("--symbol", required=True)
    p.set_defaults(func=cmd_price_limits)

    p = subparsers.add_parser("candles", help="GET /api/v1/candles")
    p.add_argument("--symbol", required=True)
    p.add_argument("--interval", required=True, choices=("1m", "1d"))
    p.add_argument("--count", type=int, default=100)
    p.add_argument("--before")
    p.add_argument("--adjusted", type=parse_bool, default=True)
    p.set_defaults(func=cmd_candles)

    p = subparsers.add_parser("stocks", help="GET /api/v1/stocks")
    p.add_argument("--symbols", required=True, help="comma-separated symbols, max 200")
    p.set_defaults(func=cmd_stocks)

    p = subparsers.add_parser("warnings", help="GET /api/v1/stocks/{symbol}/warnings")
    p.add_argument("--symbol", required=True)
    p.set_defaults(func=cmd_warnings)

    p = subparsers.add_parser("exchange-rate", help="GET /api/v1/exchange-rate")
    p.add_argument("--base", required=True, choices=("KRW", "USD"))
    p.add_argument("--quote", required=True, choices=("KRW", "USD"))
    p.add_argument("--date-time")
    p.set_defaults(func=cmd_exchange_rate)

    p = subparsers.add_parser("market-calendar", help="GET /api/v1/market-calendar/{KR|US}")
    p.add_argument("--country", required=True, choices=("KR", "US"))
    p.add_argument("--date")
    p.set_defaults(func=cmd_market_calendar)

    p = subparsers.add_parser("accounts", help="GET /api/v1/accounts")
    p.set_defaults(func=cmd_accounts)

    p = subparsers.add_parser("holdings", help="GET /api/v1/holdings")
    add_common_account(p)
    p.add_argument("--symbol")
    p.set_defaults(func=cmd_holdings)

    p = subparsers.add_parser("orders", help="GET /api/v1/orders")
    add_common_account(p)
    p.add_argument("--status", required=True, choices=("OPEN", "CLOSED"))
    p.add_argument("--symbol")
    p.add_argument("--from-date")
    p.add_argument("--to-date")
    p.add_argument("--cursor")
    p.add_argument("--limit", type=int)
    p.set_defaults(func=cmd_orders)

    p = subparsers.add_parser("order", help="GET /api/v1/orders/{orderId}")
    add_common_account(p)
    p.add_argument("--order-id", required=True)
    p.set_defaults(func=cmd_order)

    p = subparsers.add_parser("buying-power", help="GET /api/v1/buying-power")
    add_common_account(p)
    p.add_argument("--currency", required=True, choices=("KRW", "USD"))
    p.set_defaults(func=cmd_buying_power)

    p = subparsers.add_parser("sellable-quantity", help="GET /api/v1/sellable-quantity")
    add_common_account(p)
    p.add_argument("--symbol", required=True)
    p.set_defaults(func=cmd_sellable_quantity)

    p = subparsers.add_parser("commissions", help="GET /api/v1/commissions")
    add_common_account(p)
    p.set_defaults(func=cmd_commissions)

    p = subparsers.add_parser("create-order", help="POST /api/v1/orders, dry-run by default")
    add_common_account(p)
    add_mutation_flags(p)
    p.add_argument("--symbol", required=True)
    p.add_argument("--side", required=True, choices=("BUY", "SELL"))
    p.add_argument("--order-type", required=True, choices=("LIMIT", "MARKET"))
    p.add_argument("--quantity")
    p.add_argument("--order-amount")
    p.add_argument("--price")
    p.add_argument("--time-in-force", choices=("DAY", "CLS"))
    p.add_argument("--client-order-id")
    p.add_argument("--confirm-high-value-order", action="store_true")
    p.add_argument("--allow-no-client-order-id", action="store_true")
    p.set_defaults(func=cmd_create_order)

    p = subparsers.add_parser("modify-order", help="POST /api/v1/orders/{orderId}/modify, dry-run by default")
    add_common_account(p)
    add_mutation_flags(p)
    p.add_argument("--order-id", required=True)
    p.add_argument("--order-type", required=True, choices=("LIMIT", "MARKET"))
    p.add_argument("--quantity")
    p.add_argument("--price")
    p.add_argument("--confirm-high-value-order", action="store_true")
    p.set_defaults(func=cmd_modify_order)

    p = subparsers.add_parser("cancel-order", help="POST /api/v1/orders/{orderId}/cancel, dry-run by default")
    add_common_account(p)
    add_mutation_flags(p)
    p.add_argument("--order-id", required=True)
    p.set_defaults(func=cmd_cancel_order)

    p = subparsers.add_parser("request", help="advanced generic request helper")
    p.add_argument("--method", required=True)
    p.add_argument("--path", required=True)
    p.add_argument("--query", action="append", help="repeat KEY=VALUE")
    p.add_argument("--body-json")
    p.add_argument("--account")
    p.add_argument("--no-auth", action="store_true")
    add_mutation_flags(p)
    p.set_defaults(func=cmd_request)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
        return 0
    except TossApiError as exc:
        payload = {
            "ok": False,
            "status": exc.status,
            "headers": selected_headers(exc.headers),
            "body": exc.body,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=None if getattr(args, "compact", False) else 2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
