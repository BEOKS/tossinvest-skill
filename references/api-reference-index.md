# Documentation for 토스증권 Open API

<a name="documentation-for-api-endpoints"></a>
## Documentation for API Endpoints

All URIs are relative to *https://openapi.tossinvest.com*

| Class | Method | HTTP request | Description |
|------------ | ------------- | ------------- | -------------|
| *AccountApi* | [**getAccounts**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/AccountApi.md#getAccounts) | **GET** /api/v1/accounts | 계좌 목록 조회 |
| *AssetApi* | [**getHoldings**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/AssetApi.md#getHoldings) | **GET** /api/v1/holdings | 보유 주식 조회 |
| *AuthApi* | [**issueOAuth2Token**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/AuthApi.md#issueOAuth2Token) | **POST** /oauth2/token | OAuth2 액세스 토큰 발급 |
| *MarketDataApi* | [**getCandles**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/MarketDataApi.md#getCandles) | **GET** /api/v1/candles | 캔들 차트 조회 |
| *MarketDataApi* | [**getOrderbook**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/MarketDataApi.md#getOrderbook) | **GET** /api/v1/orderbook | 호가 조회 |
| *MarketDataApi* | [**getPriceLimit**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/MarketDataApi.md#getPriceLimit) | **GET** /api/v1/price-limits | 상/하한가 조회 |
| *MarketDataApi* | [**getPrices**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/MarketDataApi.md#getPrices) | **GET** /api/v1/prices | 현재가 조회 |
| *MarketDataApi* | [**getTrades**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/MarketDataApi.md#getTrades) | **GET** /api/v1/trades | 최근 체결 내역 조회 |
| *MarketInfoApi* | [**getExchangeRate**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/MarketInfoApi.md#getExchangeRate) | **GET** /api/v1/exchange-rate | 환율 조회 |
| *MarketInfoApi* | [**getKrMarketCalendar**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/MarketInfoApi.md#getKrMarketCalendar) | **GET** /api/v1/market-calendar/KR | 국내 장 운영 정보 조회 |
| *MarketInfoApi* | [**getUsMarketCalendar**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/MarketInfoApi.md#getUsMarketCalendar) | **GET** /api/v1/market-calendar/US | 해외 장 운영 정보 조회 |
| *OrderApi* | [**cancelOrder**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/OrderApi.md#cancelOrder) | **POST** /api/v1/orders/{orderId}/cancel | 주문 취소 |
| *OrderApi* | [**createOrder**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/OrderApi.md#createOrder) | **POST** /api/v1/orders | 주문 생성 |
| *OrderApi* | [**modifyOrder**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/OrderApi.md#modifyOrder) | **POST** /api/v1/orders/{orderId}/modify | 주문 정정 |
| *OrderHistoryApi* | [**getOrder**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/OrderHistoryApi.md#getOrder) | **GET** /api/v1/orders/{orderId} | 주문 상세 조회 |
| *OrderHistoryApi* | [**getOrders**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/OrderHistoryApi.md#getOrders) | **GET** /api/v1/orders | 주문 목록 조회 |
| *OrderInfoApi* | [**getBuyingPower**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/OrderInfoApi.md#getBuyingPower) | **GET** /api/v1/buying-power | 매수 가능 금액 조회 |
| *OrderInfoApi* | [**getCommissions**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/OrderInfoApi.md#getCommissions) | **GET** /api/v1/commissions | 매매 수수료 조회 |
| *OrderInfoApi* | [**getSellableQuantity**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/OrderInfoApi.md#getSellableQuantity) | **GET** /api/v1/sellable-quantity | 판매 가능 수량 조회 |
| *StockInfoApi* | [**getStockWarnings**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/StockInfoApi.md#getStockWarnings) | **GET** /api/v1/stocks/{symbol}/warnings | 매수 유의사항 조회 |
| *StockInfoApi* | [**getStocks**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/StockInfoApi.md#getStocks) | **GET** /api/v1/stocks | 종목 기본 정보 조회 |


<a name="documentation-for-models"></a>
## Documentation for Models

 - [Account](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/Account.md)
 - [AfterMarketSession](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/AfterMarketSession.md)
 - [ApiError](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ApiError.md)
 - [ApiResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ApiResponse.md)
 - [BuyingPowerResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/BuyingPowerResponse.md)
 - [Candle](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/Candle.md)
 - [CandlePageResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/CandlePageResponse.md)
 - [Commission](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/Commission.md)
 - [Cost](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/Cost.md)
 - [Currency](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/Currency.md)
 - [DailyProfitLoss](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/DailyProfitLoss.md)
 - [ErrorResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ErrorResponse.md)
 - [ExchangeRateResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ExchangeRateResponse.md)
 - [HoldingsItem](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/HoldingsItem.md)
 - [HoldingsOverview](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/HoldingsOverview.md)
 - [IntegratedHour](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/IntegratedHour.md)
 - [KrMarketCalendarResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/KrMarketCalendarResponse.md)
 - [KrMarketDay](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/KrMarketDay.md)
 - [KrMarketDetail](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/KrMarketDetail.md)
 - [MarketCountry](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/MarketCountry.md)
 - [MarketValue](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/MarketValue.md)
 - [OAuth2ErrorResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/OAuth2ErrorResponse.md)
 - [OAuth2TokenResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/OAuth2TokenResponse.md)
 - [Order](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/Order.md)
 - [OrderCreateAmountBased](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/OrderCreateAmountBased.md)
 - [OrderCreateQuantityBased](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/OrderCreateQuantityBased.md)
 - [OrderCreateRequest](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/OrderCreateRequest.md)
 - [OrderExecution](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/OrderExecution.md)
 - [OrderModifyRequest](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/OrderModifyRequest.md)
 - [OrderOperationResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/OrderOperationResponse.md)
 - [OrderResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/OrderResponse.md)
 - [OrderStatus](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/OrderStatus.md)
 - [OrderbookEntry](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/OrderbookEntry.md)
 - [OrderbookResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/OrderbookResponse.md)
 - [OverviewDailyProfitLoss](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/OverviewDailyProfitLoss.md)
 - [OverviewMarketValue](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/OverviewMarketValue.md)
 - [OverviewProfitLoss](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/OverviewProfitLoss.md)
 - [PaginatedOrderResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/PaginatedOrderResponse.md)
 - [PreMarketSession](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/PreMarketSession.md)
 - [Price](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/Price.md)
 - [PriceLimitResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/PriceLimitResponse.md)
 - [PriceResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/PriceResponse.md)
 - [ProfitLoss](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ProfitLoss.md)
 - [RegularMarketSession](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/RegularMarketSession.md)
 - [SellableQuantityResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/SellableQuantityResponse.md)
 - [StockInfo](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/StockInfo.md)
 - [StockWarning](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/StockWarning.md)
 - [Trade](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/Trade.md)
 - [UsAfterMarketSession](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/UsAfterMarketSession.md)
 - [UsDayMarketSession](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/UsDayMarketSession.md)
 - [UsMarketCalendarResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/UsMarketCalendarResponse.md)
 - [UsMarketDay](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/UsMarketDay.md)
 - [UsPreMarketSession](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/UsPreMarketSession.md)
 - [UsRegularMarketSession](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/UsRegularMarketSession.md)
 - [createOrder_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/createOrder_200_response.md)
 - [getAccounts_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getAccounts_200_response.md)
 - [getBuyingPower_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getBuyingPower_200_response.md)
 - [getCandles_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getCandles_200_response.md)
 - [getCommissions_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getCommissions_200_response.md)
 - [getExchangeRate_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getExchangeRate_200_response.md)
 - [getHoldings_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getHoldings_200_response.md)
 - [getKrMarketCalendar_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getKrMarketCalendar_200_response.md)
 - [getOrder_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getOrder_200_response.md)
 - [getOrderbook_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getOrderbook_200_response.md)
 - [getOrders_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getOrders_200_response.md)
 - [getPriceLimit_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getPriceLimit_200_response.md)
 - [getPrices_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getPrices_200_response.md)
 - [getSellableQuantity_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getSellableQuantity_200_response.md)
 - [getStockWarnings_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getStockWarnings_200_response.md)
 - [getStocks_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getStocks_200_response.md)
 - [getTrades_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getTrades_200_response.md)
 - [getUsMarketCalendar_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getUsMarketCalendar_200_response.md)
 - [modifyOrder_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/modifyOrder_200_response.md)


<a name="documentation-for-authorization"></a>
## Documentation for Authorization

<a name="oauth2ClientCredentials"></a>
### oauth2ClientCredentials

- **Type**: OAuth
- **Flow**: application
- **Authorization URL**:
- **Scopes**: N/A
