# Documentation for 토스증권 Open API

<a name="documentation-for-api-endpoints"></a>
## Documentation for API Endpoints

All URIs are relative to *https://openapi.tossinvest.com*

| Class | Method | HTTP request | Description |
|------------ | ------------- | ------------- | -------------|
| *AccountApi* | [**getAccounts**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/AccountApi.md#getAccounts) | **GET** /api/v1/accounts | 계좌 목록 조회 |
| *AssetApi* | [**getHoldings**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/AssetApi.md#getHoldings) | **GET** /api/v1/holdings | 보유 주식 조회 |
| *AuthApi* | [**issueOAuth2Token**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/AuthApi.md#issueOAuth2Token) | **POST** /oauth2/token | OAuth2 액세스 토큰 발급 |
| *ConditionalOrderApi* | [**cancelConditionalOrder**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/ConditionalOrderApi.md#cancelConditionalOrder) | **DELETE** /api/v1/conditional-orders/{conditionalOrderId} | 조건주문 취소 |
| *ConditionalOrderApi* | [**createConditionalOrder**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/ConditionalOrderApi.md#createConditionalOrder) | **POST** /api/v1/conditional-orders | 조건주문 생성 |
| *ConditionalOrderApi* | [**modifyConditionalOrder**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/ConditionalOrderApi.md#modifyConditionalOrder) | **POST** /api/v1/conditional-orders/{conditionalOrderId}/modify | 조건주문 수정 |
| *ConditionalOrderHistoryApi* | [**getConditionalOrder**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/ConditionalOrderHistoryApi.md#getConditionalOrder) | **GET** /api/v1/conditional-orders/{conditionalOrderId} | 조건주문 상세 조회 |
| *ConditionalOrderHistoryApi* | [**getConditionalOrders**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/ConditionalOrderHistoryApi.md#getConditionalOrders) | **GET** /api/v1/conditional-orders | 조건주문 목록 조회 |
| *MarketDataApi* | [**getCandles**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/MarketDataApi.md#getCandles) | **GET** /api/v1/candles | 캔들 차트 조회 |
| *MarketDataApi* | [**getOrderbook**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/MarketDataApi.md#getOrderbook) | **GET** /api/v1/orderbook | 호가 조회 |
| *MarketDataApi* | [**getPriceLimit**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/MarketDataApi.md#getPriceLimit) | **GET** /api/v1/price-limits | 상/하한가 조회 |
| *MarketDataApi* | [**getPrices**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/MarketDataApi.md#getPrices) | **GET** /api/v1/prices | 현재가 조회 |
| *MarketDataApi* | [**getTrades**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/MarketDataApi.md#getTrades) | **GET** /api/v1/trades | 최근 체결 내역 조회 |
| *MarketIndicatorsApi* | [**getMarketIndicatorCandles**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/MarketIndicatorsApi.md#getMarketIndicatorCandles) | **GET** /api/v1/market-indicators/{symbol}/candles | 시장 지표 캔들 차트 조회 |
| *MarketIndicatorsApi* | [**getMarketIndicatorInvestorTrading**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/MarketIndicatorsApi.md#getMarketIndicatorInvestorTrading) | **GET** /api/v1/market-indicators/{symbol}/investor-trading | 투자자별 매매대금 조회 |
| *MarketIndicatorsApi* | [**getMarketIndicatorPrices**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/MarketIndicatorsApi.md#getMarketIndicatorPrices) | **GET** /api/v1/market-indicators/prices | 시장 지표 현재가 조회 |
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
| *RankingApi* | [**getRankings**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/RankingApi.md#getRankings) | **GET** /api/v1/rankings | 주식 랭킹 조회 |
| *StockInfoApi* | [**getStockCreditTrades**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/StockInfoApi.md#getStockCreditTrades) | **GET** /api/v1/stocks/{symbol}/credit-trades | 신용거래 동향 조회 |
| *StockInfoApi* | [**getStockInvestorTrading**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/StockInfoApi.md#getStockInvestorTrading) | **GET** /api/v1/stocks/{symbol}/investor-trading | 투자자별 매매동향 조회 |
| *StockInfoApi* | [**getStockProgramTrades**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/StockInfoApi.md#getStockProgramTrades) | **GET** /api/v1/stocks/{symbol}/program-trades | 프로그램매매 동향 조회 |
| *StockInfoApi* | [**getStockSecuritiesLending**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/StockInfoApi.md#getStockSecuritiesLending) | **GET** /api/v1/stocks/{symbol}/securities-lending | 대차거래 동향 조회 |
| *StockInfoApi* | [**getStockShortSelling**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/StockInfoApi.md#getStockShortSelling) | **GET** /api/v1/stocks/{symbol}/short-selling | 공매도 동향 조회 |
| *StockInfoApi* | [**getStockWarnings**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/StockInfoApi.md#getStockWarnings) | **GET** /api/v1/stocks/{symbol}/warnings | 매수 유의사항 조회 |
| *StockInfoApi* | [**getStocks**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/StockInfoApi.md#getStocks) | **GET** /api/v1/stocks | 종목 기본 정보 조회 |
| *StockInfoApi* | [**listStocks**](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Apis/StockInfoApi.md#listStocks) | **GET** /api/v1/stocks/all | 마켓별 전체 종목 조회 |


<a name="documentation-for-models"></a>
## Documentation for Models

 - [Account](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/Account.md)
 - [AfterMarketSession](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/AfterMarketSession.md)
 - [ApiError](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ApiError.md)
 - [ApiResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ApiResponse.md)
 - [BuyingPowerResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/BuyingPowerResponse.md)
 - [Candle](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/Candle.md)
 - [CandlePageResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/CandlePageResponse.md)
 - [CfdBalance](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/CfdBalance.md)
 - [Commission](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/Commission.md)
 - [ConditionRequest](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ConditionRequest.md)
 - [ConditionalOrderCondition](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ConditionalOrderCondition.md)
 - [ConditionalOrderCreateRequest](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ConditionalOrderCreateRequest.md)
 - [ConditionalOrderCreateResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ConditionalOrderCreateResponse.md)
 - [ConditionalOrderDetailResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ConditionalOrderDetailResponse.md)
 - [ConditionalOrderModifyRequest](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ConditionalOrderModifyRequest.md)
 - [ConditionalOrderResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ConditionalOrderResponse.md)
 - [Cost](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/Cost.md)
 - [CreditTradeDetail](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/CreditTradeDetail.md)
 - [CreditTradeRecord](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/CreditTradeRecord.md)
 - [CreditTradesResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/CreditTradesResponse.md)
 - [Currency](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/Currency.md)
 - [DailyProfitLoss](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/DailyProfitLoss.md)
 - [ErrorResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ErrorResponse.md)
 - [ExchangeRateResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ExchangeRateResponse.md)
 - [ForeignerHolding](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ForeignerHolding.md)
 - [HoldingsItem](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/HoldingsItem.md)
 - [HoldingsOverview](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/HoldingsOverview.md)
 - [InstitutionTradingAmount](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/InstitutionTradingAmount.md)
 - [InstitutionTradingBreakdown](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/InstitutionTradingBreakdown.md)
 - [IntegratedHour](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/IntegratedHour.md)
 - [InvestorTradingAmount](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/InvestorTradingAmount.md)
 - [InvestorTradingRecord](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/InvestorTradingRecord.md)
 - [InvestorTradingResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/InvestorTradingResponse.md)
 - [InvestorTradingVolume](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/InvestorTradingVolume.md)
 - [KrMarketCalendarResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/KrMarketCalendarResponse.md)
 - [KrMarketDay](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/KrMarketDay.md)
 - [KrMarketDetail](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/KrMarketDetail.md)
 - [ListedStock](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ListedStock.md)
 - [MarketCountry](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/MarketCountry.md)
 - [MarketIndicatorCandle](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/MarketIndicatorCandle.md)
 - [MarketIndicatorCandlePageResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/MarketIndicatorCandlePageResponse.md)
 - [MarketIndicatorPriceResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/MarketIndicatorPriceResponse.md)
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
 - [PaginatedConditionalOrderResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/PaginatedConditionalOrderResponse.md)
 - [PaginatedOrderResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/PaginatedOrderResponse.md)
 - [PreMarketSession](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/PreMarketSession.md)
 - [Price](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/Price.md)
 - [PriceLimitResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/PriceLimitResponse.md)
 - [PriceResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/PriceResponse.md)
 - [ProfitLoss](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ProfitLoss.md)
 - [ProgramTradeRecord](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ProgramTradeRecord.md)
 - [ProgramTradesResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ProgramTradesResponse.md)
 - [ProgramTradingVolume](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ProgramTradingVolume.md)
 - [RankingItem](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/RankingItem.md)
 - [RankingPrice](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/RankingPrice.md)
 - [RankingResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/RankingResponse.md)
 - [RegularMarketSession](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/RegularMarketSession.md)
 - [SecuritiesLendingRecord](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/SecuritiesLendingRecord.md)
 - [SecuritiesLendingResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/SecuritiesLendingResponse.md)
 - [SellableQuantityResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/SellableQuantityResponse.md)
 - [ShortSellingRecord](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ShortSellingRecord.md)
 - [ShortSellingResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/ShortSellingResponse.md)
 - [StockInfo](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/StockInfo.md)
 - [StockInstitutionTradingBreakdown](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/StockInstitutionTradingBreakdown.md)
 - [StockInstitutionTradingVolume](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/StockInstitutionTradingVolume.md)
 - [StockInvestorTradingRecord](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/StockInvestorTradingRecord.md)
 - [StockInvestorTradingResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/StockInvestorTradingResponse.md)
 - [StockWarning](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/StockWarning.md)
 - [Trade](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/Trade.md)
 - [UsAfterMarketSession](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/UsAfterMarketSession.md)
 - [UsDayMarketSession](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/UsDayMarketSession.md)
 - [UsMarketCalendarResponse](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/UsMarketCalendarResponse.md)
 - [UsMarketDay](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/UsMarketDay.md)
 - [UsPreMarketSession](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/UsPreMarketSession.md)
 - [UsRegularMarketSession](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/UsRegularMarketSession.md)
 - [createConditionalOrder_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/createConditionalOrder_200_response.md)
 - [createOrder_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/createOrder_200_response.md)
 - [getAccounts_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getAccounts_200_response.md)
 - [getBuyingPower_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getBuyingPower_200_response.md)
 - [getCandles_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getCandles_200_response.md)
 - [getCommissions_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getCommissions_200_response.md)
 - [getConditionalOrder_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getConditionalOrder_200_response.md)
 - [getConditionalOrders_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getConditionalOrders_200_response.md)
 - [getExchangeRate_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getExchangeRate_200_response.md)
 - [getHoldings_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getHoldings_200_response.md)
 - [getKrMarketCalendar_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getKrMarketCalendar_200_response.md)
 - [getMarketIndicatorCandles_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getMarketIndicatorCandles_200_response.md)
 - [getMarketIndicatorInvestorTrading_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getMarketIndicatorInvestorTrading_200_response.md)
 - [getMarketIndicatorPrices_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getMarketIndicatorPrices_200_response.md)
 - [getOrder_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getOrder_200_response.md)
 - [getOrderbook_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getOrderbook_200_response.md)
 - [getOrders_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getOrders_200_response.md)
 - [getPriceLimit_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getPriceLimit_200_response.md)
 - [getPrices_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getPrices_200_response.md)
 - [getRankings_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getRankings_200_response.md)
 - [getSellableQuantity_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getSellableQuantity_200_response.md)
 - [getStockCreditTrades_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getStockCreditTrades_200_response.md)
 - [getStockInvestorTrading_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getStockInvestorTrading_200_response.md)
 - [getStockProgramTrades_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getStockProgramTrades_200_response.md)
 - [getStockSecuritiesLending_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getStockSecuritiesLending_200_response.md)
 - [getStockShortSelling_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getStockShortSelling_200_response.md)
 - [getStockWarnings_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getStockWarnings_200_response.md)
 - [getStocks_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getStocks_200_response.md)
 - [getTrades_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getTrades_200_response.md)
 - [getUsMarketCalendar_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/getUsMarketCalendar_200_response.md)
 - [listStocks_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/listStocks_200_response.md)
 - [modifyConditionalOrder_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/modifyConditionalOrder_200_response.md)
 - [modifyOrder_200_response](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/Models/modifyOrder_200_response.md)


<a name="documentation-for-authorization"></a>
## Documentation for Authorization

<a name="oauth2ClientCredentials"></a>
### oauth2ClientCredentials

- **Type**: OAuth
- **Flow**: application
- **Authorization URL**:
- **Scopes**: N/A
