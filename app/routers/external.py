from fastapi import APIRouter

from app.utils import call_castlemock


router = APIRouter(tags=["CastleMock"])


@router.get("/external/weather", summary="Get mock weather from CastleMock")
def get_mock_weather():
    return call_castlemock("GET", "x0T4QS/forecast")


@router.post("/external/auth/login", summary="Mock user login via CastleMock")
def mock_login():
    return call_castlemock(
        "POST",
        "xpABue/auth",
        {"username": "demo_user", "password": "secret"},
    )


@router.put("/external/user/update", summary="Mock user update via CastleMock")
def update_user_profile():
    return call_castlemock("PUT", "kCpnzj/user/update")
