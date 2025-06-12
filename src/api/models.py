from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import src.service.models as service
from src.dto.models import PredictRequest

router = APIRouter(
    prefix="/models",
    tags=["AI Models"],
)

@router.post("/clothes/predict")
def clothes(body: PredictRequest):
    result = service.clothes_equipment(body.url)
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
