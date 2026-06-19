토스증권 OpenAPI 는 제공하는 기능에 따라 다음 **네 가지 카테고리**로 분류됩니다.

- **인증 (Auth)** — OAuth 2.0 토큰 발급
- **시세·종목 정보 (Market Data · Stock Info · Market Info)** — 시세, 종목 마스터, 환율, 장 운영 시간
- **계좌·자산 (Account · Asset)** — 계좌 목록 및 보유 주식 조회
- **주문 (Order · Order History · Order Info)** — 주문 생성·정정·취소, 주문 조회, 거래 가능 정보

국내 및 미국 주식의 시세, 종목 정보, 환율, 장 운영 시간 등 시장 데이터를 조회할 수 있고, 본인 계좌의 보유 주식과 주문을 관리할 수 있습니다.

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
- 환율 (KRW↔USD)
- 장 운영 시간 (KRX·NXT 국내 캘린더, 미국 캘린더)

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

**계좌·자산** 및 **주문** 카테고리는 OAuth 2.0 토큰에 더해 **계좌 식별 헤더 `X-Tossinvest-Account`** 를 함께 전달해야 합니다.

### 연동 방식

토스증권 Open API 는 현재 **REST API** 만 제공합니다.

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

#### Market Info — 환율·장 운영 시간

| 엔드포인트 | 설명 |
|------|------|
| `GET /api/v1/exchange-rate` | KRW↔USD 환율 조회 |
| `GET /api/v1/market-calendar/KR` | 국내 장 운영 정보 (KRX·NXT 세션별 시간) |
| `GET /api/v1/market-calendar/US` | 해외 장 운영 정보 (데이마켓·프리·정규·애프터마켓) |

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

---

## 시작하기

1. **클라이언트 등록** — 토스증권 WTS에 로그인 후 설정 > Open API 메뉴에 진입하여 `client_id` 와 `client_secret` 을 발급받습니다.
2. **액세스 토큰 발급** — `POST /oauth2/token` 으로 Client Credentials Grant 방식의 access token 을 발급받습니다.
3. **API 호출** — 발급받은 토큰을 `Authorization: Bearer {access_token}` 헤더에 담아 호출합니다. **계좌·자산** 및 **주문** 카테고리는 `X-Tossinvest-Account: {accountSeq}` 헤더도 함께 전달합니다.

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
| `MARKET_INFO` | 초당 최대 3회 | -- |
| `MARKET_DATA` | 초당 최대 10회 | -- |
| `MARKET_DATA_CHART` | 초당 최대 5회 | -- |
| `ORDER` | 초당 최대 6회 | 09:00 ~ 09:10 KST: **초당 최대 3회** |
| `ORDER_HISTORY` | 초당 최대 5회 | -- |
| `ORDER_INFO` | 초당 최대 6회 | 09:00 ~ 09:10 KST: **초당 최대 3회** |

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

- `requestId` 는 응답 헤더 `X-Request-Id` 와 동일한 값입니다. CS 문의 시 첨부를 권장합니다. 일부 응답에서 requestId 가 누락된 경우, 응답 헤더의 `cf-ray` 값을 첨부해주세요.
- `code` 는 에러 코드 (예: `invalid-tick-size`, `order-not-found`, `invalid-token`) 입니다.
- `message` 는 에러와 관련된 메시지 입니다.
- `data` 는 에러 해결 힌트로, 코드별로 포함 여부와 키 구조가 다릅니다.

| HTTP Status               | 에러 코드                                | 발생 이유 |
|---------------------------|--------------------------------------|---|
| 400 BAD_REQUEST           | `invalid-request`                    | 요청이 유효하지 않습니다. 호가 유형·주문 방향·수량·금액·필수 파라미터 누락 등 다양한 사유가 있습니다. |
| 400 BAD_REQUEST           | `confirm-high-value-required`        | 주문 생성/정정 시 주문 금액이 1억원 이상인데 `confirmHighValueOrder` 가 `true` 가 아닙니다. |
| 400 BAD_REQUEST           | `account-header-required`            | `X-Tossinvest-Account` 헤더가 전달되지 않았습니다. |
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
| 409 CONFLICT              | `request-in-progress`                | 동일 `clientOrderId` 에 대한 주문 생성 요청이 이미 처리 중입니다. |
| 409 CONFLICT              | `already-filled`                     | 정정/취소 대상 주문이 이미 체결된 상태입니다. |
| 409 CONFLICT              | `already-canceled`                   | 정정/취소 대상 주문이 이미 취소된 상태입니다. |
| 409 CONFLICT              | `already-modified`                   | 정정/취소 대상 주문이 이미 정정된 상태입니다. |
| 409 CONFLICT              | `already-rejected`                   | 정정/취소 대상 주문이 이미 거부된 상태입니다. |
| 409 CONFLICT              | `already-processing`                 | 동일 주문에 대한 정정/취소가 이미 처리 중입니다. |
| 422 UNPROCESSABLE_ENTITY  | `insufficient-buying-power`          | 주문 가능 금액이 부족합니다. |
| 422 UNPROCESSABLE_ENTITY  | `order-hours-closed`                 | 현재 주문(생성/정정/취소)을 접수할 수 없는 시간입니다. |
| 422 UNPROCESSABLE_ENTITY  | `stock-restricted`                   | 해당 종목이 거래 제한 상태입니다. |
| 422 UNPROCESSABLE_ENTITY  | `price-out-of-range`                 | 주문 가격이 허용 범위(상/하한가)를 벗어났습니다. |
| 422 UNPROCESSABLE_ENTITY  | `opposite-pending-order-exists`      | 동일 종목에 반대 방향의 체결 대기 주문이 존재합니다. |
| 422 UNPROCESSABLE_ENTITY  | `order-type-not-allowed`             | 현재 사용할 수 없는 호가 유형입니다. |
| 422 UNPROCESSABLE_ENTITY  | `prerequisite-required`              | 약관 동의·위험 고지 등 사전 자격 요건을 충족하지 않았습니다. |
| 422 UNPROCESSABLE_ENTITY  | `market-not-supported-for-stock`     | 해당 종목은 요청 시장에서 거래할 수 없습니다. (KR) |
| 422 UNPROCESSABLE_ENTITY  | `investor-exchange-not-integrated`   | 투자자지시 거래소 설정이 통합(SOR)이 아닙니다. (KR) |
| 422 UNPROCESSABLE_ENTITY  | `amount-order-outside-regular-hours` | 금액 주문은 정규장에만 가능합니다. (US) |
| 422 UNPROCESSABLE_ENTITY  | `modify-restricted`                  | 해당 주문은 정정이 제한되어 있습니다. |
| 422 UNPROCESSABLE_ENTITY  | `cancel-restricted`                  | 해당 주문은 취소가 제한되어 있습니다. |
| 429 TOO_MANY_REQUESTS     | `edge-rate-limit-exceeded`           | Rate limit 초당 요청 수를 초과했습니다. |
| 429 TOO_MANY_REQUESTS     | `rate-limit-exceeded`                | Rate limit 초당 요청 수를 초과했습니다. |
| 500 INTERNAL_SERVER_ERROR | `internal-error`                     | 서버 일시 장애. |
| 500 INTERNAL_SERVER_ERROR | `maintenance`                        | 시스템 점검 중입니다. |
