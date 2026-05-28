from fastapi import APIRouter

from app.schemas.contracts import RiskProfile
from app.services.sqlite_store import store

router = APIRouter(tags=["settings"])


@router.get("/settings/risk-profile", response_model=RiskProfile)
def get_risk_profile() -> RiskProfile:
    return store.get_risk_profile()


@router.post("/settings/risk-profile", response_model=RiskProfile)
def update_risk_profile(profile: RiskProfile) -> RiskProfile:
    return store.save_risk_profile(profile)
