토스증권 OpenAPI 는 제공하는 기능에 따라 다음 **여섯 가지 카테고리**로 분류됩니다.

- **인증 (Auth)** — OAuth 2.0 토큰 발급
- **시세·종목 정보 (Market Data · Stock Info · Market Info · Market Indicators · Ranking)** — 시세, 종목 마스터, 환율, 장 운영 시간, 랭킹, 지수
- **계좌·자산 (Account · Asset)** — 계좌 목록 및 보유 주식 조회
- **주문 (Order · Order History · Order Info)** — 주문 생성·정정·취소, 주문 조회, 거래 가능 정보
- **조건주문 (Conditional Order · Conditional Order History)** — 감시 조건 등록 시 자동 매매 (단일 · OCO · OTO)
- **웹소켓 (Trade·Orderbook·Order Event)** — 실시간 체결·호가·주문 이벤트 구독

국내 및 미국 주식의 시세, 종목 정보, 환율, 장 운영 시간 등 시장 데이터를 조회할 수 있고, 본인 계좌의 보유 주식과 주문·조건주문을 관리할 수 있습니다.

---

## 개요

### 인증

토스증권 Open API 는 모든 호출에 OAuth 2.0 액세스 토큰을 요구합니다.

- OAuth 2.0 액세스 토큰 발급 (Client Credentials Grant)

### 시세·종목 정보

종목·시장에 대해 모든 사용자에게 동일하게 제공되는 객관적 데이터입니다.

- 시세 (현재가, 호가, 체결, 캔들 OHLCV, 상·하한가)
- 종목 마스터 (종목명, 시장, 통화, 상장 상태, 발행주식수)
- 매수 유의사항 (정리매매, 단기과열, 투자경고/위험, VI 발동, 신주인수권)
- 수급 동향 (투자자별 매매동향, 프로그램매매, 공매도, 신용거래, 대차거래 — 국내 종목)
- 환율 (KRW↔USD)
- 장 운영 시간 (KRX·NXT 국내 캘린더, 미국 캘린더)
- 랭킹 (거래대금·거래량·등락률 / 시장 전체·토스증권 체결 기준)
- 지수 (국내 지수·국채 현재가, 캔들, 투자자별 매매대금)

사용자 계좌와 무관한 정보이므로 **OAuth 2.0 토큰만으로 호출 가능**합니다.

### 계좌·자산

본인 계좌의 자산 현황을 조회하는 API 입니다.

- 계좌 목록 조회
- 보유 주식 조회 (종목별 상세 + 합산 평가)

### 주문

본인 계좌의 매매를 다루는 API 입니다.

- 주문 생성·정정·취소
- 주문 조회 (대기중 / 종료) 및 상세 조회
- 매수 가능 금액, 판매 가능 수량, 매매 수수료 조회

### 조건주문

지정한 가격에 도달하면 자동으로 매매(매수/매도) 주문을 생성하는 조건주문 API 입니다.

- 조건주문 등록·수정·취소
- 조건주문 조회 (진행 중 / 종료) 및 상세 조회
- 타입: 단일(SINGLE) · OCO(One-Cancels-the-Other) · OTO(One-Triggers-the-Other)
- 호가유형: 지정가(LIMIT) · 시장가(MARKET)

**계좌·자산**, **주문**, **조건주문** 카테고리는 OAuth 2.0 토큰에 더해 **계좌 식별 헤더 `X-Tossinvest-Account`** 를 함께 전달해야 합니다.

### 웹소켓

시세·주문 이벤트를 실시간으로 전달받는 웹소켓 API 입니다.

- 실시간 체결·호가 구독
- 실시간 주문 이벤트 구독

### 연동 방식

토스증권 Open API 는 **REST API** 와 **웹소켓**(실시간 시세·주문 이벤트 구독)을 제공합니다. 웹소켓 연동 방법은 아래 [웹소켓 연동](#웹소켓-연동) 섹션을 참고하세요.

---

## 기능 목록

### 인증

#### Auth — OAuth 2.0

| 엔드포인트 | 설명 |
|------|------|
| `POST /oauth2/token` | OAuth 2.0 액세스 토큰 발급 (Client Credentials Grant) |

### 시세·종목 정보

#### Market Data — 시세

| 엔드포인트 | 설명 |
|------|------|
| `GET /api/v1/orderbook` | 호가 조회 |
| `GET /api/v1/prices` | 현재가 조회 |
| `GET /api/v1/trades` | 최근 체결 내역 조회 |
| `GET /api/v1/price-limits` | 상/하한가 조회 |
| `GET /api/v1/candles` | 캔들 차트 조회 (1분봉 · 일봉) |

#### Stock Info — 종목 정보

| 엔드포인트 | 설명 |
|------|------|
| `GET /api/v1/stocks` | 종목 기본 정보 조회 (symbol, 종목명, 시장, 통화, 상장 상태 등) |
| `GET /api/v1/stocks/{symbol}/warnings` | 매수 유의사항 조회 (정리매매, 과열, 투자경고/위험, VI, 신주인수권) |
| `GET /api/v1/stocks/{symbol}/investor-trading` | 투자자별 매매동향 조회 (개인·외국인·기관·기타법인 일별 거래량, 기관 세부 분류 포함) |
| `GET /api/v1/stocks/{symbol}/program-trades` | 프로그램매매 동향 조회 (차익·비차익 일별 거래량) |
| `GET /api/v1/stocks/{symbol}/short-selling` | 공매도 동향 조회 (일별 거래량·거래대금·비중) |
| `GET /api/v1/stocks/{symbol}/credit-trades` | 신용거래 동향 조회 (융자·대주 일별 수량·잔고·공여율) |
| `GET /api/v1/stocks/{symbol}/securities-lending` | 대차거래 동향 조회 (일별 체결·상환·잔고) |

#### Market Info — 환율·장 운영 시간

| 엔드포인트 | 설명 |
|------|------|
| `GET /api/v1/exchange-rate` | KRW↔USD 환율 조회 |
| `GET /api/v1/market-calendar/KR` | 국내 장 운영 정보 (KRX·NXT 세션별 시간) |
| `GET /api/v1/market-calendar/US` | 해외 장 운영 정보 (데이마켓·프리·정규·애프터마켓) |

#### Ranking — 주식 랭킹

| 엔드포인트 | 설명 |
|------|------|
| `GET /api/v1/rankings` | 랭킹 조회 (거래대금·거래량·등락률 / 시장 전체·토스증권 체결 기준) |
#### Market Indicators — 시장 지표

| 엔드포인트 | 설명 |
|------|------|
| `GET /api/v1/market-indicators/prices` | 시장 지표 현재가 조회 (국내 지수·국채) |
| `GET /api/v1/market-indicators/{symbol}/candles` | 시장 지표 캔들 차트 조회 (1분봉 · 일봉) |
| `GET /api/v1/market-indicators/{symbol}/investor-trading` | 투자자별 매매대금 조회 (코스피·코스닥) |

### 계좌·자산

#### Account — 계좌

| 엔드포인트 | 설명 |
|------|------|
| `GET /api/v1/accounts` | 계좌 목록 조회 |

#### Asset — 보유 자산

| 엔드포인트 | 설명 |
|------|------|
| `GET /api/v1/holdings` | 보유 주식 조회 (종목별 상세 + 평가금액·손익 합산) |

### 주문

#### Order — 주문 (생성·정정·취소)

| 엔드포인트 | 설명 |
|------|------|
| `POST /api/v1/orders` | 주문 생성 (지정가·시장가 / KR·US) |
| `POST /api/v1/orders/{orderId}/modify` | 주문 정정 (가격·수량) |
| `POST /api/v1/orders/{orderId}/cancel` | 주문 취소 |

#### Order History — 주문 조회

| 엔드포인트 | 설명 |
|------|------|
| `GET /api/v1/orders` | 주문 목록 조회 (대기중/종료) |
| `GET /api/v1/orders/{orderId}` | 주문 상세 조회 (모든 상태) |

#### Order Info — 거래 가능 정보

| 엔드포인트 | 설명 |
|------|------|
| `GET /api/v1/buying-power` | 매수 가능 금액 조회 (현금 기반, KRW·USD) |
| `GET /api/v1/sellable-quantity` | 판매 가능 수량 조회 |
| `GET /api/v1/commissions` | 매매 수수료 조회 (KR·US 시장별) |

### 조건주문

#### Conditional Order — 조건주문 (등록·수정·취소)

| 엔드포인트 | 설명 |
|------|------|
| `POST /api/v1/conditional-orders` | 조건주문 등록 (SINGLE · OCO · OTO) |
| `POST /api/v1/conditional-orders/{conditionalOrderId}/modify` | 조건주문 수정 |
| `DELETE /api/v1/conditional-orders/{conditionalOrderId}` | 조건주문 취소 |

#### Conditional Order History — 조건주문 조회

| 엔드포인트 | 설명 |
|------|------|
| `GET /api/v1/conditional-orders` | 조건주문 목록 조회 (진행 중 `OPEN` / 종료 `CLOSED`) |
| `GET /api/v1/conditional-orders/{conditionalOrderId}` | 조건주문 상세 조회 |

### 웹소켓

| 엔드포인트 | 설명 |
|------|------|
| `GET /ws/v1` (웹소켓) | 실시간 체결·호가·본인 주문 이벤트 구독 — [웹소켓 연동](#웹소켓-연동) 참고 |

---

## 시작하기

1. **클라이언트 등록** — 토스증권 WTS에 로그인 후 설정 > Open API 메뉴에 진입하여 `client_id` 와 `client_secret` 을 발급받습니다.
2. **허용 IP 등록** — 설정 > Open API 메뉴 하단의 **허용 IP 관리** 에서 API 호출을 허용할 IP 를 등록합니다. 등록된 허용 IP 목록에 없는 IP 에서의 호출은 403 으로 차단됩니다.
3. **액세스 토큰 발급** — `POST /oauth2/token` 으로 Client Credentials Grant 방식의 access token 을 발급받습니다.
4. **API 호출** — 발급받은 토큰을 `Authorization: Bearer {access_token}` 헤더에 담아 호출합니다. **계좌·자산**, **주문**, **조건주문** 카테고리는 `X-Tossinvest-Account: {accountSeq}` 헤더도 함께 전달합니다.

```bash
# 1) 토큰 발급
curl -s -X POST 'https://openapi.tossinvest.com/oauth2/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=client_credentials' \
  -d 'client_id=xxx' \
  -d 'client_secret=yyy'

# 2) 시세·종목 정보 (토큰만 필요)
curl -s 'https://openapi.tossinvest.com/api/v1/stocks?symbols=005930' \
  -H 'Authorization: Bearer eyJhbGciOi...'

# 3) 계좌·자산 / 주문 (토큰 + 계좌 헤더)
curl -s 'https://openapi.tossinvest.com/api/v1/holdings' \
  -H 'Authorization: Bearer eyJhbGciOi...' \
  -H 'X-Tossinvest-Account: 1'
```

---

## Rate Limits

모든 API 는 **클라이언트 × API 그룹** 단위로 초당 요청 수(TPS)가 제한됩니다.
각 API 의 description 끝에 해당 API 가 속한 Rate Limits Group 이 표기됩니다.
구체적인 한도 수치는 운영 상황에 따라 사전 공지 없이 조정될 수 있으며, 현재 허용 한도는 응답 헤더로 확인할 수 있습니다.

| Rate Limits Group | 요청 한도 | 피크시간 한도 |
|-------------------|-----------|----------------|
| `AUTH` | 초당 최대 5회 | -- |
| `ACCOUNT` | 초당 최대 1회 | -- |
| `ASSET` | 초당 최대 5회 | -- |
| `STOCK` | 초당 최대 5회 | -- |
| `STOCK_ALL` | 초당 최대 1회 | -- |
| `STOCK_TRADING_TREND` | 초당 최대 10회 | -- |
| `MARKET_INFO` | 초당 최대 3회 | -- |
| `MARKET_DATA` | 초당 최대 15회 | -- |
| `MARKET_DATA_CHART` | 초당 최대 20회 | -- |
| `RANKING` | 초당 최대 5회 | -- |
| `MARKET_INDICATOR_PRICE` | 초당 최대 10회 | -- |
| `MARKET_INDICATOR` | 초당 최대 10회 | -- |
| `MARKET_INDICATOR_CHART` | 초당 최대 5회 | -- |
| `ORDER` | 초당 최대 10회 | 09:00 ~ 09:10 KST: **초당 최대 10회** |
| `ORDER_HISTORY` | 초당 최대 5회 | -- |
| `ORDER_INFO` | 초당 최대 6회 | 09:00 ~ 09:10 KST: **초당 최대 3회** |
| `CONDITIONAL_ORDER` | 초당 최대 5회 | -- |
| `CONDITIONAL_ORDER_HISTORY` | 초당 최대 10회 | -- |

- 위 한도는 운영 상황에 따라 사전 공지 없이 조정될 수 있으며, 현재 허용 한도는 응답 헤더 `X-RateLimit-Limit` 으로 확인할 수 있습니다.

### 응답 헤더

정상 응답과 429 응답 모두에 다음 헤더가 포함됩니다:

| 헤더 | 의미 |
|------|------|
| `X-RateLimit-Limit` | 현재 허용된 초당 요청 수 (burst capacity) |
| `X-RateLimit-Remaining` | 버킷에 남은 토큰 수 (429 시 0) |
| `X-RateLimit-Reset` | 토큰 1 개 재충전까지 예상 초 |
| `Retry-After` | 재시도 권장 초 (429 응답에만 포함) |

### 429 대응 권장 사항

- 429 수신 시 `Retry-After` 헤더 값만큼 대기 후 재시도합니다.
- 지수 백오프(1s → 2s → 4s ...) 와 jitter 를 함께 적용합니다.
- `X-RateLimit-Remaining` 이 낮아질 때 클라이언트 측에서 요청 속도를 선제적으로 완화할 수 있습니다.

---

## 에러 응답

모든 에러 응답은 다음 envelope 으로 내려갑니다.

```json
{
  "error": {
    "requestId": "01HXYZABCDEFG123456789",
    "code": "invalid-request",
    "message": "주문 방향이 올바르지 않습니다.",
    "data": {
      "field": "side",
      "allowedValues": ["BUY", "SELL"]
    }
  }
}
```

- `requestId` 는 응답 헤더 `X-Request-Id` 와 동일한 값입니다. CS 문의 시 첨부를 권장합니다. 일부 응답에서 requestId 가 누락된 경우, 응답 헤더의 `referenceId` 또는 `x-amz-cf-id` 값을 첨부해주세요.
- `code` 는 에러 코드 (예: `invalid-tick-size`, `order-not-found`, `invalid-token`) 입니다.
- `message` 는 에러와 관련된 메시지 입니다.
- `data` 는 에러 해결 힌트로, 코드별로 포함 여부와 키 구조가 다릅니다.

| HTTP Status               | 에러 코드                                | 발생 이유 |
|---------------------------|--------------------------------------|---|
| 400 BAD_REQUEST           | `invalid-request`                    | 요청이 유효하지 않습니다. 호가 유형·주문 방향·수량·금액·필수 파라미터 누락 등 다양한 사유가 있습니다. |
| 400 BAD_REQUEST           | `confirm-high-value-required`        | 주문 생성/정정 시 주문 금액이 1억원 이상인데 `confirmHighValueOrder` 가 `true` 가 아닙니다. |
| 400 BAD_REQUEST           | `account-header-required`            | `X-Tossinvest-Account` 헤더가 전달되지 않았습니다. |
| 400 BAD_REQUEST           | `unsupported-ranking-duration`       | `TOP_GAINERS`·`TOP_LOSERS` 랭킹은 `duration=realtime` 을 지원하지 않습니다. |
| 400 BAD_REQUEST           | `unsupported-symbol`                 | 시장 지표 심볼 카탈로그에서 지원하지 않는 심볼입니다. 투자자별 매매대금은 `KOSPI`·`KOSDAQ` 만 지원합니다. |
| 400 BAD_REQUEST           | `unsupported-symbol`                 | 시장 지표에서 지원하지 않는 심볼입니다. |
| 400 BAD_REQUEST           | `unsupported-market`                 | 국내(KR) 종목만 지원하는 API 에 다른 시장의 종목을 요청했습니다. |
| 401 UNAUTHORIZED          | `invalid-token`                      | 토큰이 유효하지 않거나 형식이 잘못되었습니다. |
| 401 UNAUTHORIZED          | `edge-blocked`                       | `Authorization` 헤더가 전달되지 않았습니다. |
| 401 UNAUTHORIZED          | `expired-token`                      | 액세스 토큰이 만료되었습니다. |
| 401 UNAUTHORIZED          | `login-user-not-found`               | 토큰에 대응하는 로그인 정보를 찾을 수 없습니다. |
| 403 FORBIDDEN             | `edge-blocked`                       | 허용되지 않은 요청입니다. |
| 403 FORBIDDEN             | `forbidden`                          | 요청에 필요한 권한이 부족합니다. |
| 404 NOT_FOUND             | `edge-blocked`                       | 요청한 API 경로를 지원하지 않습니다. |
| 404 NOT_FOUND             | `stock-not-found`                    | 요청한 종목을 찾을 수 없습니다. |
| 404 NOT_FOUND             | `exchange-rate-not-found`            | 환율 정보를 찾을 수 없습니다. |
| 404 NOT_FOUND             | `account-not-found`                  | `X-Tossinvest-Account` 헤더가 가리키는 계좌를 찾을 수 없습니다. |
| 404 NOT_FOUND             | `order-not-found`                    | `orderId` 에 해당하는 주문을 찾을 수 없습니다. |
| 404 NOT_FOUND             | `conditional-order-not-found`        | `conditionalOrderId`·`type` 에 해당하는 조건주문을 찾을 수 없습니다. |
| 409 CONFLICT              | `request-in-progress`                | 동일 `clientOrderId` 에 대한 주문 생성 요청이 이미 처리 중입니다. |
| 409 CONFLICT              | `already-filled`                     | 정정/취소 대상 주문이 이미 체결된 상태입니다. |
| 409 CONFLICT              | `already-canceled`                   | 정정/취소 대상 주문이 이미 취소된 상태입니다. |
| 409 CONFLICT              | `already-modified`                   | 정정/취소 대상 주문이 이미 정정된 상태입니다. |
| 409 CONFLICT              | `already-rejected`                   | 정정/취소 대상 주문이 이미 거부된 상태입니다. |
| 409 CONFLICT              | `already-processing`                 | 동일 주문에 대한 정정/취소가 이미 처리 중입니다. |
| 414 URI_TOO_LONG          | `edge-blocked`                       | 요청 URI 길이를 초과했습니다. |
| 415 UNSUPPORTED_MEDIA_TYPE | `unsupported-content-type`          | 지원하지 않는 `Content-Type` 입니다. 요청 본문은 `application/json` 을 사용해 주세요. |
| 422 UNPROCESSABLE_ENTITY  | `insufficient-buying-power`          | 주문 가능 금액이 부족합니다. |
| 422 UNPROCESSABLE_ENTITY  | `order-hours-closed`                 | 현재 주문(생성/정정/취소)을 접수할 수 없는 시간입니다. |
| 422 UNPROCESSABLE_ENTITY  | `stock-restricted`                   | 해당 종목이 거래 제한 상태입니다. |
| 422 UNPROCESSABLE_ENTITY  | `price-out-of-range`                 | 주문 가격이 허용 범위(상/하한가)를 벗어났습니다. |
| 422 UNPROCESSABLE_ENTITY  | `opposite-pending-order-exists`      | 동일 종목에 반대 방향의 체결 대기 주문이 존재합니다. |
| 422 UNPROCESSABLE_ENTITY  | `order-type-not-allowed`             | 현재 사용할 수 없는 호가 유형입니다. |
| 422 UNPROCESSABLE_ENTITY  | `prerequisite-required`              | 약관 동의·교육 이수·위험 고지 등 사전 자격 요건을 충족하지 않았습니다. |
| 422 UNPROCESSABLE_ENTITY  | `market-not-supported-for-stock`     | 해당 종목은 요청 시장에서 거래할 수 없습니다. (KR) |
| 422 UNPROCESSABLE_ENTITY  | `investor-exchange-not-integrated`   | 투자자지시 거래소 설정이 통합(SOR)이 아닙니다. (KR) |
| 422 UNPROCESSABLE_ENTITY  | `amount-order-outside-regular-hours` | 금액 주문은 정규장에만 가능합니다. (US) |
| 422 UNPROCESSABLE_ENTITY  | `modify-restricted`                  | 해당 주문은 정정이 제한되어 있습니다. |
| 422 UNPROCESSABLE_ENTITY  | `cancel-restricted`                  | 해당 주문은 취소가 제한되어 있습니다. |
| 422 UNPROCESSABLE_ENTITY  | `insufficient-sellable-quantity`     | 매도 가능 수량이 부족합니다. |
| 422 UNPROCESSABLE_ENTITY  | `order-limit-exceeded`               | 주문 설정 한도를 초과했습니다. |
| 422 UNPROCESSABLE_ENTITY  | `duplicate-conditional-order`        | 동일 종목에 이미 그룹 조건주문(OCO/OTO)이 있습니다. (OCO·OTO 는 종목당 1개 / SINGLE 은 제한 없음) |
| 422 UNPROCESSABLE_ENTITY  | `condition-already-met`              | 설정한 가격이 이미 조건을 충족했습니다. 가격을 다시 설정해 주세요. |
| 422 UNPROCESSABLE_ENTITY  | `idempotency-key-conflict`           | 동일 `clientOrderId` 로 내용이 다른 주문(주문 생성·조건주문)을 재요청했습니다. |
| 422 UNPROCESSABLE_ENTITY  | `account-restricted`                 | 계좌 상태가 해당 주문을 허용하지 않습니다. (RIA·연금·종합매매 등) |
| 429 TOO_MANY_REQUESTS     | `edge-rate-limit-exceeded`           | Rate limit 초당 요청 수를 초과했습니다. |
| 429 TOO_MANY_REQUESTS     | `rate-limit-exceeded`                | Rate limit 초당 요청 수를 초과했습니다. |
| 500 INTERNAL_SERVER_ERROR | `internal-error`                     | 서버 일시 장애. |
| 500 INTERNAL_SERVER_ERROR | `maintenance`                        | 시스템 점검 중입니다. |

---

## 웹소켓 연동

REST 조회(요청-응답)와 달리, 웹소켓은 한 번 연결해두면 시세·주문의 변동분을 **실시간으로 전달**받는 통로입니다. 엔드포인트는 `wss://openapi-ws.tossinvest.com/ws/v1` 하나이며, 받고 싶은 데이터(체결·호가·주문 등)는 구독 메시지의 `type` 으로 선택합니다. 구독은 **선언형(declarative)** 으로, 클라이언트가 보내는 JSON 배열 1개가 곧 현재 구독 전체입니다.

수신 프레임의 `topic` 은 구독 선언의 `type` 뒤에 `codes` 원소를 `:` 로 이어 붙인 값입니다 — `trade:us` 로 `AAPL` 을 구독하면 `trade:us:AAPL`, `personal:order` 로 계좌 `3` 을 구독하면 `personal:order:3`.

채널별 구독 방법과 수신 payload 스키마·예제는 API 문서 **웹소켓** 그룹의 채널 항목(**Trade**·**Orderbook**·**Order Event**)을, 수신 프레임 구분 규칙과 한도는 **Connection** 항목을 참고하세요.

### 기능 목록

| 기능 | type | 설명 |
|---|---|---|
| 실시간 체결 | `trade:{시장}` | 체결 틱(체결가·체결량)을 실시간 푸시 |
| 실시간 호가 | `orderbook:{시장}` | 매도/매수 호가를 실시간 푸시 |
| 실시간 주문 | `personal:order` | 본인 계좌의 주문 이벤트를 실시간 푸시 |

`{시장}` 은 미국 `us`, 국내(통합) `kr` 입니다. 국내는 통합 시세(KRX+NXT)만 노출합니다.

### 연결

1. **연결** — `wss://openapi-ws.tossinvest.com/ws/v1` 로 연결하며 `Authorization: Bearer {access_token}` 헤더를 보냅니다(없거나 무효·만료면 `401`, 허용 IP 미등록 IP 에서의 시도는 `403` 으로 연결 거부 — REST 와 동일한 허용 IP 목록 적용). **TLS 필수**. **계정당 동시 연결 최대 2개** — 초과해 연결하면 새 연결이 수락되고, 가장 오래된 연결이 서버에 의해 종료됩니다.
2. **구독 선언** — 연결 후 JSON **배열 1개**를 보냅니다. 이 배열이 곧 현재 구독 전체이며(**full-replace**), 새 배열이 기존 구독을 전부 대체합니다(빠진 항목 자동 해제, 빈 배열 `[]` = 전체 해제).

   ```json
   [
     {"id": "req-1"},
     {"type": "trade:us", "codes": ["AAPL"]},
     {"type": "orderbook:kr", "codes": ["005930"]},
     {"type": "personal:order", "codes": ["3"]}
   ]
   ```

3. **수신** — 선언마다 서버가 `subscriptions` ack(구독 확정·거부 결과)로 응답하고, 구독 대상이 갱신될 때마다 `message` 프레임으로 데이터를 푸시합니다.

   ```json
   {"type": "subscriptions", "id": "req-1", "subscribed": ["trade:us:AAPL", "orderbook:kr:005930", "personal:order:3"], "rejected": []}
   {"type": "message", "topic": "trade:us:AAPL", "data": {...}}
   ```

4. **연결 유지** — 서버는 **클라이언트로부터의 수신이 180초간 없으면** 연결을 종료합니다. 서버가 보내주는 데이터는 이 타이머를 리셋하지 않으므로, 데이터를 받고 있는 중에도 180초 이내 주기로 `PING` 을 보내세요(**60초 간격 권장**) — 요청 형식과 `pong` 응답은 **Connection** 채널의 **[송신] PING** 스펙을 참고하세요. 웹소켓 표준 ping/pong 프레임도 지원됩니다.

터미널에서 위 흐름을 그대로 따라해볼 수 있습니다 (`wscat` 은 Node.js 가 있으면 `npx` 로 바로 실행됩니다):

```bash
# 1) 토큰 발급 — 응답 JSON 의 access_token 을 다음 단계에 사용
curl -s -X POST 'https://openapi.tossinvest.com/oauth2/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=client_credentials' \
  -d 'client_id=xxx' \
  -d 'client_secret=yyy'

# 2) 웹소켓 연결
npx -y wscat -c 'wss://openapi-ws.tossinvest.com/ws/v1' \
  -H 'Authorization: Bearer eyJhbGciOi...'

# 3) 연결된 프롬프트에 구독 선언(배열 1개)을 입력하면 ack 와 실시간 데이터가 도착합니다
> [{"type":"trade:us","codes":["AAPL"]}]
< {"type":"subscriptions","subscribed":["trade:us:AAPL"],"rejected":[]}
< {"type":"message","topic":"trade:us:AAPL","data":{...}}

# 4) 연결 유지 — 60초 간격으로 PING 입력
> PING
< {"type":"pong"}
```

### 데이터 전달 보장

| 채널 | 보장 | 의미 |
|---|---|---|
| 시세 (`trade`·`orderbook`) | LOSSY | 수신이 밀리면 중간 프레임이 유실될 수 있습니다 (항상 최신 상태 우선, 유실 감지용 sequence 미제공) |
| 주문 (`personal:order`) | LOSSLESS | 미소비분(backlog)을 건너뛰지 않고 유지합니다. 수신이 2초 이상 계속 막히면 연결이 종료됩니다 |

LOSSLESS 보장은 연결 세션 내에 한정됩니다. 연결이 끊긴 구간의 이벤트는 다시 전달되지 않으므로, 재연결 후 `GET /api/v1/orders` 로 주문 상태를 재동기화하세요.

### 웹소켓 Rate Limits

| 항목 | 한도 | 초과 시 |
|---|---|---|
| 동시 연결 | **계정당 2개** | 새 연결은 수락되고 가장 오래된 연결이 종료 |
| 연결당 구독 수 | **100건** (`codes` 합산 — 주문 `accountSeq` 포함) | `too-many-topics` |
| 선언(요청) 빈도 | **5회/초** | `rate-limit-exceeded` |

한도를 넘은 선언은 거부되고 기존 구독은 그대로 유지됩니다. 구독 수는 채널×종목 조합 기준입니다 — 같은 종목이라도 채널이 다르면 각각 1건입니다. `rate-limit-exceeded` 를 받으면 약 1초 대기 후 재선언하세요 (REST 와 달리 `Retry-After` 헤더는 제공되지 않습니다).

### 응답 프레임

서버 → 클라이언트 프레임은 top-level `type` 으로 구분합니다.

| 프레임 | 형태 | 의미 |
|---|---|---|
| `subscriptions` | `{"type":"subscriptions","id":"req-1","subscribed":[...],"rejected":[...]}` | 선언 결과 ack — 구독 확정(`subscribed`)·거부(`rejected`) 목록. `id` 는 보냈을 때만 echo |
| `message` | `{"type":"message","topic":"{full key}","data":{...}}` | 실시간 데이터(체결·호가·주문) |
| `error` | `{"type":"error","error":{"code":"...","message":"..."},"id":"req-1"}` | 선언 단위 실패(기존 구독 유지) 또는 서버 배포 시(`server-shutdown`). `id` 는 보냈을 때만 echo |
| `pong` | `{"type":"pong"}` | keepalive 응답 |

### 웹소켓 에러 / 거부

연결(handshake) 단계의 실패만 HTTP 상태로 응답합니다:

| HTTP Status | 원인 | 대응 |
|---|---|---|
| `401` | 토큰 없음·무효·만료 | 토큰 재발급 후 재연결 |
| `403` | 허용 IP 미등록 | WTS 설정 > Open API > 허용 IP 관리에서 IP 등록 |
| `503` | 서버 내부 오류 | 백오프 후 재시도 |

연결 이후의 실패는 모두 in-band 웹소켓 프레임이며 HTTP 상태가 아닙니다. 선언 **전체**가 실패하면 `error` 프레임, 일부 항목만 실패하면 `subscriptions.rejected[]` 로 알립니다.

| 위치 | code | 의미 |
|---|---|---|
| `error.code` | `wrong-format` | JSON 파싱 실패·배열 아님·원소가 객체 아님 |
| `error.code` | `no-type` | `type` 누락 |
| `error.code` | `invalid-type` | 지원하지 않는 `type` |
| `error.code` | `no-codes` | `codes` 누락·빈 배열·비문자열 원소 |
| `error.code` | `too-many-topics` | 요청 `codes` 합이 100건 초과 |
| `error.code` | `too-many` | 해석 후 구독 수 100건 초과(안전망) |
| `error.code` | `rate-limit-exceeded` | 선언 빈도 5회/초 초과 |
| `error.code` | `internal-error` | 서버 내부 오류 |
| `error.code` | `server-shutdown` | 서버 배포 시에는 프레임 직후 연결 종료, 재연결 후 재선언 필요 |
| `rejected[].code` | `stock-not-found` | 종목 마스터에 없는 symbol (나머지는 정상 구독) |
| `rejected[].code` | `symbol-market-mismatch` | 선언 마켓과 종목의 마켓 불일치 |
| `rejected[].code` | `account-not-found` | `personal:order` 의 `accountSeq` 가 본인 계좌가 아니거나 구독 부적격 (해당 계좌만 거부) |

`rejected[]` 항목은 원인을 수정하기 전에는 재선언에 포함해도 같은 이유로 다시 거부됩니다 — full-replace 특성상 재연결·재선언 때마다 반복되므로, 거부된 항목은 선언 목록에서 빼거나 수정한 뒤 다시 선언하세요. 일부 거부여도 `subscribed` 항목은 정상 구독되고 연결은 유지됩니다.
