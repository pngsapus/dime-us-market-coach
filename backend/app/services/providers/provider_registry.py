from dataclasses import dataclass

from app.core.config import settings
from app.schemas.contracts import ProviderStatus
from app.services.providers.base import MarketDataProvider
from app.services.providers.mock_provider import MockMarketDataProvider
from app.services.providers.real_provider_stub import RealMarketDataProviderStub


@dataclass(frozen=True)
class ProviderResolution:
    requested_provider: str
    active_provider: str
    used_fallback: bool
    message: str


_MOCK_PROVIDER = MockMarketDataProvider()
_REAL_STUB_PROVIDER = RealMarketDataProviderStub()
_PROVIDERS: dict[str, MarketDataProvider] = {
    "mock": _MOCK_PROVIDER,
    "local": _MOCK_PROVIDER,
    "real_stub": _REAL_STUB_PROVIDER,
}
_FALLBACK_ONLY_PROVIDERS = {"real_stub"}


def resolve_provider(provider_name: str | None = None) -> tuple[MarketDataProvider, ProviderResolution]:
    requested = (provider_name or settings.market_data_provider or "mock").strip().lower()
    provider = _PROVIDERS.get(requested)
    if provider and requested not in _FALLBACK_ONLY_PROVIDERS:
        return provider, ProviderResolution(
            requested_provider=requested,
            active_provider=provider.provider_name,
            used_fallback=False,
            message="ใช้ mock/local provider",
        )
    if provider and requested in _FALLBACK_ONLY_PROVIDERS:
        return _MOCK_PROVIDER, ProviderResolution(
            requested_provider=requested,
            active_provider=_MOCK_PROVIDER.provider_name,
            used_fallback=True,
            message=f"provider '{requested}' เป็น placeholder ที่ยังไม่พร้อมใช้งาน จึง fallback เป็น mock/local provider",
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


def get_provider_status() -> ProviderStatus:
    provider, resolution = resolve_provider()
    status = provider.get_data_status()
    if not resolution.used_fallback:
        return status
    return status.model_copy(
        update={
            "is_degraded": True,
            "fallback_used": True,
            "fallback_reason": resolution.message,
            "degraded_reason": resolution.message,
            "freshness_label": "ใช้ mock/local fallback",
        }
    )


def get_provider_by_name(provider_name: str) -> MarketDataProvider | None:
    return _PROVIDERS.get(provider_name.strip().lower())
