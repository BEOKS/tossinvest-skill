---
name: tossinvest-skill
description: Work with the Toss Securities Open API for Korean and US stock market data, stock info, exchange rates, market calendars, account and holdings lookups, order history, buying power, sellable quantity, commissions, conditional orders, rankings, trading trends, market indicators, realtime WebSocket integration, and delegated trading workflows. Use when an agent needs to run user-delegated buy/sell/order-management loops, call or build against developers.tossinvest.com, inspect the Toss OpenAPI schema, generate client code, or operate with TOSS_API_KEY/TOSS_SECRET_KEY credentials.
---

# Toss Securities Open API

## Overview

Use this skill to build against or operate the Toss Securities Open API. The bundled references preserve the official OpenAPI sources, and `scripts/tossinvest.py` provides a deterministic CLI for authentication, market data, account data, order history, order information, and user-delegated autonomous order mutations.

## Source Selection

- Bundled official references were refreshed on 2026-09-08 (OpenAPI 1.2.14). They are a snapshot; check the official sources again for future API changes.
- Read `references/current-api.md` for newly added REST APIs, updated order rules, and WebSocket routing. The CLI supports new REST endpoints through `request`; it does not implement a WebSocket client.
- Read `references/asyncapi.json` for exact realtime subscription and message schemas.
- Read `references/workflows.md` for task routing, endpoint groups, safety rules, rate limits, and common workflows.
- Read `references/openapi.json` when exact request parameters, schemas, enum values, examples, or response envelopes matter.
- Read `references/official-overview.md` for the official quick start, rate limit model, and error model.
- Read `references/api-reference-index.md` to locate official per-API and per-model markdown pages.

## Credentials

Use `TOSS_API_KEY` as the OAuth client ID and `TOSS_SECRET_KEY` as the OAuth client secret. Also accept these aliases when present: `TOSSINVEST_CLIENT_ID`, `TOSS_CLIENT_ID`, `TOSSINVEST_CLIENT_SECRET`, and `TOSS_CLIENT_SECRET`. The bundled CLI first reads process environment variables, then falls back to simple assignments in `~/.zshrc`, `~/.zprofile`, or `~/.profile`.

After changing shell credentials, reload them in the calling process or start a new shell: inherited environment values take precedence over shell-file fallback. On `invalid_client`, check the configured client ID/secret; on 403, check the WTS Open API allowed IP list. Do not repeatedly reissue tokens to diagnose authorization errors.

Never print secrets. Avoid printing full access tokens unless the user explicitly needs one for an external tool; `scripts/tossinvest.py token` redacts tokens by default.

## CLI Quick Start

Run from the skill directory:

```bash
python3 scripts/tossinvest.py list-endpoints
python3 scripts/tossinvest.py token
python3 scripts/tossinvest.py stocks --symbols 005930,AAPL
python3 scripts/tossinvest.py prices --symbols 005930,AAPL
python3 scripts/tossinvest.py accounts
```

Account, asset, order history, and order information APIs require an account sequence:

```bash
python3 scripts/tossinvest.py holdings --account 1
python3 scripts/tossinvest.py buying-power --account 1 --currency KRW
python3 scripts/tossinvest.py orders --account 1 --status OPEN
```

For convenience, set `TOSSINVEST_ACCOUNT`, `TOSS_ACCOUNT`, or `TOSS_ACCOUNT_SEQ` and omit `--account`.

## Trading Operations

Treat `create-order`, `modify-order`, `cancel-order`, and conditional-order creation/modification/cancellation via `request` as live financial side effects. A conditional order can create a trade later without the agent running; authorization must cover that behavior and its expiry.

- When the user delegates autonomous trading in natural language, treat that delegation as permission to run repeated buy, sell, modify, and cancel operations while the instruction remains active. Do not require per-order reconfirmation inside the delegated run.
- Use current account state, market sessions, buying power, sellable quantity, warnings, fees, prices, orderbooks, trades, and candles to decide each live mutation.
- Prefer a dry run immediately before live mutations to validate the exact request body, then execute the same action autonomously when it still matches the delegated objective and current market data.
- After live mutations, inspect order status and continue the delegated loop when appropriate: wait, modify, cancel, place follow-up orders, or stop with a concise report.
- Require both `--execute` and `--yes` for live order mutations.
- Prefer `--client-order-id` for order creation. The CLI blocks live create-order calls without it unless `--allow-no-client-order-id` is also supplied.

Dry-run example:

```bash
python3 scripts/tossinvest.py create-order --account 1 --symbol 005930 --side BUY --order-type LIMIT --quantity 1 --price 70000 --client-order-id test-001
```

Live execution example:

```bash
python3 scripts/tossinvest.py create-order --account 1 --symbol 005930 --side BUY --order-type LIMIT --quantity 1 --price 70000 --client-order-id test-001 --execute --yes
```

## Response Handling

Expect successful non-auth responses to use a common JSON envelope with `result`. OAuth token responses use the OAuth2 shape. On errors, capture the HTTP status, `X-Request-Id`, with `referenceId`, `x-amz-cf-id`, or legacy `cf-ray` as fallbacks, Toss error code/message/data, and rate limit headers.

The CLI handles two failure modes automatically:

- 401 with a cached token: reissues the token once and retries. Only one access token is valid per client, so another process issuing a token silently invalidates the cache.
- 429: retries up to `--max-retries` times (default 2, or `TOSSINVEST_MAX_RETRIES`), waiting for `Retry-After` or `X-RateLimit-Reset` with jitter. Pass `--max-retries 0` to disable.

When calling the API without the CLI, implement the same behavior. `list-endpoints` reports each endpoint's `rateLimitGroup` — pace loops per group and watch `X-RateLimit-Remaining` before it reaches zero.

The CLI decodes gzip responses. For an uncertain order result, inspect order state before retrying and preserve the same body and `clientOrderId` within its 10-minute window; stop if the outcome cannot be reconciled.
