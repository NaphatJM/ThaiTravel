from fastapi import APIRouter, HTTPException, status
from ttt.schemas import schema_location
from ttt.models import model_location
from ttt import models
from sqlmodel import select

router = APIRouter(prefix="/locations", tags=["Location"])


@router.get("/provinces")
async def get_provinces():
    statement = select(model_location.Province)
    results = models.session.exec(statement)
    db_provinces = results.all()
    if not db_provinces:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No provinces found"
        )
    return db_provinces


@router.get("/provinces/{province_id}")
async def get_province(province_id: int) -> model_location.Province:
    db_province = models.session.get(model_location.Province, province_id)
    if not db_province:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Province with ID {province_id} not found",
        )
    return db_province


@router.post("/provinces")
async def create_province(
    province: schema_location.province_create_schema,
) -> model_location.Province:
    db_province = model_location.Province(**province.model_dump())
    models.session.add(db_province)
    models.session.commit()
    models.session.refresh(db_province)
    return db_province


@router.put("/provinces/{province_id}")
async def update_province(
    province_id: int, province: schema_location.province_update_schema
) -> model_location.Province:
    db_province = models.session.get(model_location.Province, province_id)
    if not db_province:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Province with ID {province_id} not found",
        )
    update_data = province.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_province, key, value)
    models.session.add(db_province)
    models.session.commit()
    models.session.refresh(db_province)
    return db_province


@router.delete("/provinces/{province_id}")
async def delete_province(province_id: int):
    db_province = models.session.get(model_location.Province, province_id)
    if not db_province:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Province with ID {province_id} not found",
        )
    models.session.delete(db_province)
    models.session.commit()
    return {"message": f"Province {province_id} deleted successfully."}
