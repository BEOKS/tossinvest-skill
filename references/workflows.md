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

Use `references/openapi.json` as the source of truth in this repository. It was captured from the official OpenAPI JSON and includes paths, schemas, examples, authentication, and response definitions.

## Endpoint Map

All URIs are relative to `https://openapi.tossinvest.com`.

| Group | Method | Path | Operation | Purpose |
|---|---:|---|---|---|
| Auth | POST | `/oauth2/token` | `issueOAuth2Token` | OAuth2 client credentials token |
| Market Data | GET | `/api/v1/orderbook` | `getOrderbook` | bid/ask orderbook for one symbol |
| Market Data | GET | `/api/v1/prices` | `getPrices` | current prices for up to 200 symbols |
| Market Data | GET | `/api/v1/trades` | `getTrades` | recent trades for one symbol |
| Market Data | GET | `/api/v1/price-limits` | `getPriceLimit` | upper/lower price limits |
| Market Data | GET | `/api/v1/candles` | `getCandles` | 1 minute or 1 day OHLCV candles |
| Stock Info | GET | `/api/v1/stocks` | `getStocks` | stock master data |
| Stock Info | GET | `/api/v1/stocks/{symbol}/warnings` | `getStockWarnings` | buy warnings |
| Market Info | GET | `/api/v1/exchange-rate` | `getExchangeRate` | KRW/USD exchange rate |
| Market Info | GET | `/api/v1/market-calendar/KR` | `getKrMarketCalendar` | KR market sessions |
| Market Info | GET | `/api/v1/market-calendar/US` | `getUsMarketCalendar` | US market sessions |
| Account | GET | `/api/v1/accounts` | `getAccounts` | account list |
| Asset | GET | `/api/v1/holdings` | `getHoldings` | holdings and portfolio summary |
| Order History | GET | `/api/v1/orders` | `getOrders` | open or closed order list |
| Order | POST | `/api/v1/orders` | `createOrder` | create live order |
| Order History | GET | `/api/v1/orders/{orderId}` | `getOrder` | order detail |
| Order | POST | `/api/v1/orders/{orderId}/modify` | `modifyOrder` | modify live order |
| Order | POST | `/api/v1/orders/{orderId}/cancel` | `cancelOrder` | cancel live order |
| Order Info | GET | `/api/v1/buying-power` | `getBuyingPower` | cash buying power |
| Order Info | GET | `/api/v1/sellable-quantity` | `getSellableQuantity` | sellable quantity |
| Order Info | GET | `/api/v1/commissions` | `getCommissions` | commission rates |

## Authentication

Exchange `TOSS_API_KEY` and `TOSS_SECRET_KEY` for an OAuth2 access token with `POST /oauth2/token`.

Important behavior from the official spec:

- Use `grant_type=client_credentials`.
- Token responses do not use the common `result` envelope.
- Refresh tokens are not provided.
- Only one access token is valid per client; reissuing a token invalidates the previous one.

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
- `timeInForce` defaults to `DAY`; `CLS` is used for supported close orders such as US LOC.
- `clientOrderId` is an idempotency key valid for 10 minutes. Prefer it for live order creation.
- `confirmHighValueOrder` is required by the API for high-value orders.

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

Rate limits are per client and API group. The official overview lists these baseline groups:

| Group | Limit |
|---|---:|
| `AUTH` | 5 TPS |
| `ACCOUNT` | 1 TPS |
| `ASSET` | 5 TPS |
| `STOCK` | 5 TPS |
| `MARKET_INFO` | 3 TPS |
| `MARKET_DATA` | 10 TPS |
| `MARKET_DATA_CHART` | 5 TPS |
| `ORDER` | 6 TPS, 3 TPS during 09:00-09:10 KST |
| `ORDER_HISTORY` | 5 TPS |
| `ORDER_INFO` | 6 TPS, 3 TPS during 09:00-09:10 KST |

Check response headers because limits may change: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, and `Retry-After`.

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

For support or debugging, retain `X-Request-Id`; if missing, retain `cf-ray`. Treat unknown enum values and unknown error codes as possible future additions.

## Client Generation

Use `references/openapi.json` for code generation or typed client work. For quick inspection:

```bash
python3 scripts/tossinvest.py list-endpoints --tag "Order Info"
python3 scripts/tossinvest.py schema OrderCreateRequest
python3 scripts/tossinvest.py schema ErrorResponse
```
