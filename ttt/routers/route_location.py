from fastapi import APIRouter
from ttt.schemas.schema_location import province_schema
from typing import List

router = APIRouter(prefix="/locations", tags=["Location"])


@router.get("/provinces")
async def get_provinces():
    return [
        province_schema(id=1, name="Bangkok", code="BKK"),
        province_schema(id=2, name="Chiang Mai", code="CM"),
        province_schema(id=3, name="Phuket", code="PKT"),
    ]


@router.get("/provinces/{province_id}", response_model=province_schema)
async def get_province(province_id: int):
    return province_schema(
        id=province_id, name=f"Province {province_id}", code=f"CODE{province_id}"
    )


@router.post("/provinces", response_model=province_schema)
async def create_province(province: province_schema):
    return province


@router.put("/provinces/{province_id}", response_model=province_schema)
async def update_province(province_id: int, province: province_schema):
    return province


@router.delete("/provinces/{province_id}")
async def delete_province(province_id: int):
    return {"message": f"Province {province_id} deleted successfully."}
