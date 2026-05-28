from abc import ABC, abstractmethod

from app.schemas.contracts import MarketSummary, StockSnapshot


class MarketDataProvider(ABC):
    @abstractmethod
    def get_market_summary(self) -> MarketSummary:
        raise NotImplementedError

    @abstractmethod
    def list_stocks(self) -> list[StockSnapshot]:
        raise NotImplementedError

    @abstractmethod
    def get_stock(self, symbol: str) -> StockSnapshot:
        raise NotImplementedError
