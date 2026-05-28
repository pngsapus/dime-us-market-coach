from fastapi import APIRouter

from app.schemas.contracts import DiscoveryRun
from app.services.discovery_engine import discovery_engine

router = APIRouter(tags=["discovery"])


@router.get("/discovery/latest", response_model=DiscoveryRun)
def get_latest_discovery() -> DiscoveryRun:
    return discovery_engine.latest()


@router.post("/discovery/run", response_model=DiscoveryRun)
def run_discovery() -> DiscoveryRun:
    return discovery_engine.run(write_files=True)
