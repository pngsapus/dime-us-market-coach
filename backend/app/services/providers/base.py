from abc import ABC, abstractmethod

from app.schemas.contracts import LocalStockUniverseItem, MarketSummary, ProviderStatus, StockSnapshot


class MarketDataProvider(ABC):
    provider_name: str
    provider_type: str

    @abstractmethod
    def get_market_summary(self) -> MarketSummary:
        raise NotImplementedError

    @abstractmethod
    def get_stock_universe(self) -> list[LocalStockUniverseItem]:
        raise NotImplementedError

    @abstractmethod
    def get_stock_snapshot(self, symbol: str) -> StockSnapshot:
        raise NotImplementedError

    @abstractmethod
    def get_data_status(self) -> ProviderStatus:
        raise NotImplementedError

    def list_stocks(self) -> list[StockSnapshot]:
        return [self.get_stock_snapshot(item.symbol) for item in self.get_stock_universe()]

    def get_stock(self, symbol: str) -> StockSnapshot:
        return self.get_stock_snapshot(symbol)
