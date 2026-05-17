from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["Ephemeris"])


@router.get("/health")
def health_check():
    return {"status": "OK"}
