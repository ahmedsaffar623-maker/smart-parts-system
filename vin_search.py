from fastapi import APIRouter
from app.services.vin_service import search_vehicle_by_vin

router = APIRouter()


@router.get("/search-vin/{vin}")
def search_vin(vin: str):

    return search_vehicle_by_vin(vin)