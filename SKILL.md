---
name: tossinvest-skill
description: Work with the Toss Securities Open API for Korean and US stock market data, stock info, exchange rates, market calendars, account and holdings lookups, order history, buying power, sellable quantity, commissions, and guarded order create/modify/cancel workflows. Use when Codex needs to call or build against developers.tossinvest.com, inspect the Toss OpenAPI schema, generate client code, or operate with TOSS_API_KEY/TOSS_SECRET_KEY credentials.
---

# Toss Securities Open API

## Overview

Use this skill to build against or operate the Toss Securities Open API. The bundled references preserve the official OpenAPI sources, and `scripts/tossinvest.py` provides a deterministic CLI for authentication, market data, account data, order history, order information, and guarded order mutations.

## Source Selection

- Read `references/workflows.md` for task routing, endpoint groups, safety rules, rate limits, and common workflows.
- Read `references/openapi.json` when exact request parameters, schemas, enum values, examples, or response envelopes matter.
- Read `references/official-overview.md` for the official quick start, rate limit model, and error model.
- Read `references/api-reference-index.md` to locate official per-API and per-model markdown pages.

## Credentials

Use `TOSS_API_KEY` as the OAuth client ID and `TOSS_SECRET_KEY` as the OAuth client secret. Also accept these aliases when present: `TOSSINVEST_CLIENT_ID`, `TOSS_CLIENT_ID`, `TOSSINVEST_CLIENT_SECRET`, and `TOSS_CLIENT_SECRET`. The bundled CLI first reads process environment variables, then falls back to simple assignments in `~/.zshrc`, `~/.zprofile`, or `~/.profile`.

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

## Trading Safety

Treat `create-order`, `modify-order`, and `cancel-order` as live financial side effects.

- First produce a dry run and show the exact request body.
- Execute only after the user explicitly confirms the exact action, symbol, side, quantity or amount, price, account, and order ID when applicable.
- Require both `--execute` and `--yes` for live order mutations.
- Prefer `--client-order-id` for order creation. The CLI blocks live create-order calls without it unless `--allow-no-client-order-id` is also supplied.

Dry-run example:

```bash
python3 scripts/tossinvest.py create-order --account 1 --symbol 005930 --side BUY --order-type LIMIT --quantity 1 --price 70000 --client-order-id test-001
```

Live execution example, only after explicit confirmation:

```bash
python3 scripts/tossinvest.py create-order --account 1 --symbol 005930 --side BUY --order-type LIMIT --quantity 1 --price 70000 --client-order-id test-001 --execute --yes
```

## Response Handling

Expect successful non-auth responses to use a common JSON envelope with `result`. OAuth token responses use the OAuth2 shape. On errors, capture the HTTP status, `X-Request-Id` or `cf-ray`, Toss error code/message/data, and rate limit headers.

For 429 responses, wait for `Retry-After` when present and then retry with jitter. Watch `X-RateLimit-Remaining` and slow down before reaching zero.
