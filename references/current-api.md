# Current API additions and constraints

Official sources, retrieved 2026-09-08:
- Overview: https://openapi.tossinvest.com/openapi-docs/overview.md
- REST contract (1.2.14): https://openapi.tossinvest.com/openapi-docs/latest/openapi.json
- Realtime contract: https://openapi.tossinvest.com/openapi-docs/latest/asyncapi.json

## REST coverage

The installed CLI has dedicated commands for the original REST endpoints and a generic `request` command for all additional REST endpoints. `list-endpoints` reads the refreshed spec. Before using a new endpoint, inspect its parameters and request schema in `openapi.json`; `request` does not perform full schema validation.

| Feature | Method and path | Main parameters |
| --- | --- | --- |
| All listed stocks | GET `/api/v1/stocks/all` | required `market`; optional `status`, `securityType`, `commonShare` |
| Investor trading | GET `/api/v1/stocks/{symbol}/investor-trading` | KR symbol; `count` 1–100, `until` |
| Program trades | GET `/api/v1/stocks/{symbol}/program-trades` | KR symbol; `count` 1–100, `until` |
| Short selling | GET `/api/v1/stocks/{symbol}/short-selling` | KR symbol; `count` 1–100, `until` |
| Credit trades | GET `/api/v1/stocks/{symbol}/credit-trades` | KR symbol; `count` 1–100, `until` |
| Securities lending | GET `/api/v1/stocks/{symbol}/securities-lending` | KR symbol; `count` 1–100, `until` |
| Rankings | GET `/api/v1/rankings` | required `type`, `marketCountry`, `duration`; optional `count`, `excludeInvestmentCaution` |
| Indicator prices | GET `/api/v1/market-indicators/prices` | required comma-separated `symbols` |
| Indicator candles | GET `/api/v1/market-indicators/{symbol}/candles` | required `interval`; optional `count`, `before` |
| Indicator investor trading | GET `/api/v1/market-indicators/{symbol}/investor-trading` | KOSPI/KOSDAQ; required `interval`; optional `count`, `until` |
| Conditional order list | GET `/api/v1/conditional-orders` | account header; required `status`; optional `symbol`, `cursor`, `limit` |
| Conditional order detail | GET `/api/v1/conditional-orders/{conditionalOrderId}` | account header |
| Conditional order creation | POST `/api/v1/conditional-orders` | account header; `ConditionalOrderCreateRequest` |
| Conditional order modification | POST `/api/v1/conditional-orders/{conditionalOrderId}/modify` | account header; `ConditionalOrderModifyRequest` |
| Conditional order cancellation | DELETE `/api/v1/conditional-orders/{conditionalOrderId}` | account header |

Read-only examples (run from the skill directory):

```bash
python3 scripts/tossinvest.py request --method GET --path /api/v1/stocks/all --query market=KOSPI
python3 scripts/tossinvest.py request --method GET --path /api/v1/rankings --query type=MARKET_TRADING_AMOUNT --query marketCountry=KR --query duration=1d --query count=5
python3 scripts/tossinvest.py request --method GET --path /api/v1/stocks/005930/investor-trading --query count=5
python3 scripts/tossinvest.py request --method GET --path /api/v1/market-indicators/prices --query symbols=KOSPI,KOSDAQ
python3 scripts/tossinvest.py request --method GET --path /api/v1/conditional-orders --account 1 --query status=OPEN
```

Use the account sequence returned by `accounts`, not an assumed value. The generic helper needs an explicit `--account` for account-scoped endpoints. Query values, including ISO timestamps containing `+`, are URL-encoded by the helper. Follow returned `nextBefore`, `nextUntil`, and `nextCursor` unchanged for pagination.

`TOP_GAINERS` and `TOP_LOSERS` do not support `duration=realtime`. Bond indicators support daily candles only; minute candles are for KOSPI/KOSDAQ. Refer to the Market Indicators tag in `openapi.json` for the supported symbol catalog.

## Order changes

- `--time-in-force OPG`: KR opening auction orders, LIMIT or MARKET, subject to session acceptance. `CLS` is US LIMIT only. `DAY` remains the default.
- US fractional quantity is allowed only for MARKET SELL, up to six decimal places. Fractional buys use `orderAmount`.
- US fractional quantity sells and amount orders are accepted from regular-session opening until one hour before regular-session close.
- Modify KR orders with a positive integer `quantity`; omit `quantity` when modifying US orders. Resolve the market from current order/stock data because the modify CLI receives an opaque order ID.
- Conditional orders support SINGLE, OCO and OTO. OCO/OTO require LIMIT and both conditions; SINGLE omits the second condition. `expireDate` is required. OCO/OTO are limited to one group per symbol; inspect existing conditional orders before creating a group.
- Conditional orders can trigger future trades. Only register them when the user's authorization covers the conditions, size and expiry. `request` uses dry-run by default for POST/DELETE; live calls require `--execute --yes`.
- For generic order creation, supply `clientOrderId` in the JSON body. The dedicated create-order command enforces it for live orders by default; the generic helper does not. Reuse the same key and identical payload only when retrying the same intended order, within the documented 10-minute idempotency window. An uncertain outcome or `idempotency-key-conflict` needs reconciliation, not a new key.

## Authentication and diagnostics

Register the caller's allowed IP in WTS Settings > Open API. A 403 can indicate an unregistered IP. OAuth `invalid_client` indicates client authentication failure; `invalid-token` / `expired-token` concern an access token. Only one token is valid per client, so prefer the shared token cache over repeated issuance.

Process environment variables take precedence over shell-file fallback. After editing `.zshrc`, reload credentials in the calling shell or start a new process with the updated environment. Never display credential values. The CLI handles gzip JSON for success, OAuth, and error responses; diagnostic header fallbacks include `referenceId` and `x-amz-cf-id`.

## WebSocket integration

The REST CLI has no WebSocket subcommand. For realtime integration, read the bundled `asyncapi.json` plus the WebSocket section of `official-overview.md` and use a WebSocket-capable client.

- Endpoint: `wss://openapi-ws.tossinvest.com/ws/v1`, Bearer token in the handshake header, same allowed IP list as REST.
- Subscription JSON is one array describing the entire desired subscription set; every declaration replaces the previous set. `[]` unsubscribes all.
- Types: `trade:kr`, `trade:us`, `orderbook:kr`, `orderbook:us`, `personal:order`. Personal-order `codes` are string account sequences. KR quotes combine KRX and NXT.
- Maximum two connections per account; opening another displaces the oldest. Maximum 100 channel/code subscriptions per connection; five declarations per second.
- Send `PING` every 60 seconds; receiving market data does not reset the 180-second client-idle timeout.
- Inspect both `subscriptions.subscribed` and `subscriptions.rejected`. Correct or remove rejected items before redeclaring. On reconnect, redeclare the full desired set.
- Quotes are lossy. Personal-order delivery is lossless only inside the current connection; disconnected events are not replayed. After reconnect, reconcile orders through REST. A blocked order consumer can be disconnected after two seconds.
