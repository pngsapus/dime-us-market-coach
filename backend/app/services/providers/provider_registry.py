from dataclasses import dataclass

from app.core.config import settings
from app.services.providers.base import MarketDataProvider
from app.services.providers.mock_provider import MockMarketDataProvider


@dataclass(frozen=True)
class ProviderResolution:
    requested_provider: str
    active_provider: str
    used_fallback: bool
    message: str


_MOCK_PROVIDER = MockMarketDataProvider()
_PROVIDERS: dict[str, MarketDataProvider] = {
    "mock": _MOCK_PROVIDER,
    "local": _MOCK_PROVIDER,
}


def resolve_provider(provider_name: str | None = None) -> tuple[MarketDataProvider, ProviderResolution]:
    requested = (provider_name or settings.market_data_provider or "mock").strip().lower()
    provider = _PROVIDERS.get(requested)
    if provider:
        return provider, ProviderResolution(
            requested_provider=requested,
            active_provider=provider.provider_name,
            used_fallback=False,
            message="ใช้ mock/local provider",
        )
    return _MOCK_PROVIDER, ProviderResolution(
        requested_provider=requested,
        active_provider=_MOCK_PROVIDER.provider_name,
        used_fallback=True,
        message=f"ไม่รู้จัก provider '{requested}' จึง fallback เป็น mock/local provider",
    )


def get_active_provider() -> MarketDataProvider:
    provider, _ = resolve_provider()
    return provider


def get_provider_resolution() -> ProviderResolution:
    _, resolution = resolve_provider()
    return resolution
