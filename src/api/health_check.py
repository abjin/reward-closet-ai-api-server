from fastapi import APIRouter
import src.service.health_check as service

router = APIRouter(
    prefix="/health-check",
    tags=["Health Check"],
)


@router.get("/")
def health_check():
    return service.health_check()
