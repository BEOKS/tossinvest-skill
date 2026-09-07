# Toss Securities Open API Workflows

## Table of Contents

- [Official Sources](#official-sources)
- [Endpoint Map](#endpoint-map)
- [Authentication](#authentication)
- [Market Data and Stock Info](#market-data-and-stock-info)
- [Accounts and Assets](#accounts-and-assets)
- [Autonomous Trading Loop](#autonomous-trading-loop)
- [Order Workflows](#order-workflows)
- [Rate Limits](#rate-limits)
- [Errors](#errors)
- [Client Generation](#client-generation)

## Official Sources

- Human docs: `https://developers.tossinvest.com/docs`
- Agent entrypoint: `https://developers.tossinvest.com/llms.txt`
- Overview: `https://openapi.tossinvest.com/openapi-docs/overview.md`
- OpenAPI index: `https://openapi.tossinvest.com/openapi-docs/latest/api-reference/README.md`
- Canonical OpenAPI JSON: `https://openapi.tossinvest.com/openapi-docs/latest/openapi.json`

Use `references/openapi.json` as the bundled REST contract (OpenAPI 1.2.14, retrieved 2026-09-08). Use `references/asyncapi.json` for WebSocket contracts. Both are snapshots of server-owned sources. See `current-api.md` for additions and operational changes; see the refreshed `official-overview.md` for the complete endpoint and rate-limit tables.

## Endpoint Map

All REST URIs are relative to `https://openapi.tossinvest.com`. Run `python3 scripts/tossinvest.py list-endpoints` to list every bundled operation, or filter with `--tag`. Dedicated CLI commands cover the original REST endpoints; use `request` for the additional endpoints documented in `current-api.md`.

## Authentication

Exchange `TOSS_API_KEY` and `TOSS_SECRET_KEY` for an OAuth2 access token with `POST /oauth2/token`.

Important behavior from the official spec:

- Use `grant_type=client_credentials`.
- Token responses do not use the common `result` envelope.
- Refresh tokens are not provided.
- Only one access token is valid per client; reissuing a token invalidates the previous one.

Because reissuance invalidates the previous token, the CLI recovers from a stale cached token automatically: on 401 with a cached token it reissues once and retries. Avoid issuing tokens from multiple processes in parallel.

Prefer `scripts/tossinvest.py` so token caching avoids unnecessary reissuance:

```bash
python3 scripts/tossinvest.py token
```

## Market Data and Stock Info

Use only the OAuth bearer token for market data, stock info, exchange rate, and market calendar calls.

```bash
python3 scripts/tossinvest.py orderbook --symbol 005930
python3 scripts/tossinvest.py prices --symbols 005930,AAPL
python3 scripts/tossinvest.py trades --symbol AAPL --count 20
python3 scripts/tossinvest.py candles --symbol 005930 --interval 1d --count 30
python3 scripts/tossinvest.py stocks --symbols 005930,AAPL
python3 scripts/tossinvest.py warnings --symbol 005930
python3 scripts/tossinvest.py exchange-rate --base KRW --quote USD
python3 scripts/tossinvest.py market-calendar --country KR --date 2026-06-19
```

Use 6 digit numeric symbols for KRX stocks and ticker symbols for US stocks. Multi-symbol endpoints accept comma-separated symbols.

For candle pagination, pass the previous response's `nextBefore` value as `--before` to fetch older candles. `count` is capped at 200 per request.

## Accounts and Assets

Account-scoped APIs need `X-Tossinvest-Account` with the `accountSeq` returned by `GET /api/v1/accounts`.

```bash
python3 scripts/tossinvest.py accounts
python3 scripts/tossinvest.py holdings --account 1
python3 scripts/tossinvest.py holdings --account 1 --symbol AAPL
```

For repeated use, set `TOSSINVEST_ACCOUNT`, `TOSS_ACCOUNT`, or `TOSS_ACCOUNT_SEQ`.

## Autonomous Trading Loop

Autonomous trading is a first-class workflow for this skill. When a user delegates trading in natural language, the agent may continue without per-order reconfirmation while that instruction remains active.

Use this loop:

1. Read the current account, holdings, buying power, sellable quantity, open orders, market session, warnings, fees, prices, orderbooks, trades, and candles.
2. Choose the next buy, sell, modify, cancel, wait, or stop action from the delegated objective and current data.
3. Produce a dry run for the exact order mutation.
4. If the dry run still matches the delegated objective and current data, execute the same mutation with `--execute --yes`.
5. Inspect order status and fills, then repeat the loop or report the final state.

The user is responsible for all investment outcomes from delegated live trading. The skill does not guarantee profit.

## Order Workflows

Always check buying power, sellable quantity, market sessions, warnings, and fees before placing or changing an order.

```bash
python3 scripts/tossinvest.py buying-power --account 1 --currency KRW
python3 scripts/tossinvest.py sellable-quantity --account 1 --symbol 005930
python3 scripts/tossinvest.py commissions --account 1
python3 scripts/tossinvest.py orders --account 1 --status OPEN
```

Order creation supports quantity-based orders and US market amount-based orders:

- Quantity-based: `symbol`, `side`, `orderType`, and `quantity`; `price` is required for `LIMIT`.
- Amount-based: US `MARKET` orders with `orderAmount`; use this for fractional amount buys.
- `timeInForce` defaults to `DAY`; `CLS` supports US LIMIT close orders, and `OPG` supports KR LIMIT/MARKET opening orders. See `current-api.md` for fractional-order and modification restrictions.
- `clientOrderId` is an idempotency key valid for 10 minutes. Prefer it for live order creation.
- `confirmHighValueOrder` is required by the API for high-value orders.

Order modification rules differ by market:

- KR stocks: `quantity` is required and must be a positive integer; missing/zero/negative/decimal returns `400 invalid-request`.
- US stocks: `quantity` must be omitted; sending it returns `400 us-modify-quantity-not-supported`. Modify price only.

Use dry runs first:

```bash
python3 scripts/tossinvest.py create-order --account 1 --symbol AAPL --side BUY --order-type MARKET --order-amount 100.5 --client-order-id aapl-amount-001
python3 scripts/tossinvest.py modify-order --account 1 --order-id ORDER_ID --order-type LIMIT --price 185.5
python3 scripts/tossinvest.py cancel-order --account 1 --order-id ORDER_ID
```

For live mutations, require `--execute --yes`. When a user has delegated autonomous trading for an active goal, the agent may execute after current market/account checks and a matching dry run still support the action:

```bash
python3 scripts/tossinvest.py cancel-order --account 1 --order-id ORDER_ID --execute --yes
```

## Rate Limits

Rate limits are per client and API group. Use the current table in `official-overview.md` and the returned `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, and `Retry-After` headers. The CLI retries 429 responses up to `--max-retries` times (default 2), using `Retry-After` or `X-RateLimit-Reset` with jitter. Reconcile uncertain order outcomes before resubmission.

`list-endpoints` includes each endpoint's `rateLimitGroup` for pacing polling loops.

## Errors

Common non-auth errors use this envelope:

```json
{
  "error": {
    "requestId": "01HXYZABCDEFG123456789",
    "code": "invalid-request",
    "message": "주문 방향이 올바르지 않습니다.",
    "data": {
      "field": "side"
    }
  }
}
```

For support or debugging, retain `X-Request-Id`; if missing, retain `referenceId` or `x-amz-cf-id` (and legacy `cf-ray` when present). Treat unknown enum values and unknown error codes as possible future additions.

## Client Generation

Use `references/openapi.json` for code generation or typed client work. For quick inspection:

```bash
python3 scripts/tossinvest.py list-endpoints --tag "Order Info"
python3 scripts/tossinvest.py schema OrderCreateRequest
python3 scripts/tossinvest.py schema ErrorResponse
```
