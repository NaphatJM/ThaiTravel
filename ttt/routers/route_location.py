from fastapi import APIRouter
from ttt.schemas.schema_location import province
from typing import List

router = APIRouter(prefix="/locations", tags=["Location"])


@router.get("/provinces")
async def get_provinces():
    return [
        province(id=1, name="Bangkok", code="BKK"),
        province(id=2, name="Chiang Mai", code="CM"),
        province(id=3, name="Phuket", code="PKT"),
    ]


@router.get("/provinces/{province_id}", response_model=province)
async def get_province(province_id: int):
    return province(
        id=province_id, name=f"Province {province_id}", code=f"CODE{province_id}"
    )


@router.post("/provinces", response_model=province)
async def create_province(province: province):
    return province


@router.put("/provinces/{province_id}", response_model=province)
async def update_province(province_id: int, province: province):
    return province


@router.delete("/provinces/{province_id}")
async def delete_province(province_id: int):
    return {"message": f"Province {province_id} deleted successfully."}
