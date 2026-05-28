from fastapi import APIRouter

from app.schemas.contracts import RiskProfile

router = APIRouter(tags=["settings"])
_risk_profile = RiskProfile()


@router.get("/settings/risk-profile", response_model=RiskProfile)
def get_risk_profile() -> RiskProfile:
    return _risk_profile


@router.post("/settings/risk-profile", response_model=RiskProfile)
def update_risk_profile(profile: RiskProfile) -> RiskProfile:
    global _risk_profile
    _risk_profile = profile
    return _risk_profile
