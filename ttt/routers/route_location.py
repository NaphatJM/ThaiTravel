from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from ttt.schemas import schema_location
from ttt.models import model_location
from ttt import models
from sqlmodel import select

router = APIRouter(prefix="/locations", tags=["Location"])


@router.get("/provinces", response_model=list[schema_location.province_schema])
async def get_provinces(session: AsyncSession = Depends(models.get_session)):
    statement = select(model_location.Province)
    results = await session.exec(statement)
    db_provinces = results.all()
    if not db_provinces:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No provinces found"
        )
    return [schema_location.province_schema.model_validate(p) for p in db_provinces]


@router.get("/provinces/{province_id}", response_model=schema_location.province_schema)
async def get_province(
    province_id: int, session: AsyncSession = Depends(models.get_session)
) -> model_location.Province:
    db_province = await session.get(model_location.Province, province_id)
    if not db_province:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Province with ID {province_id} not found",
        )
    return schema_location.province_schema.model_validate(db_province)


@router.post("/provinces", response_model=schema_location.province_schema)
async def create_province(
    province: schema_location.province_create_schema,
    session: AsyncSession = Depends(models.get_session),
) -> model_location.Province:
    db_province = model_location.Province(**province.model_dump())
    session.add(db_province)
    await session.commit()
    await session.refresh(db_province)
    return schema_location.province_schema.model_validate(db_province)


@router.put("/provinces/{province_id}", response_model=schema_location.province_schema)
async def update_province(
    province_id: int,
    province: schema_location.province_update_schema,
    session: AsyncSession = Depends(models.get_session),
) -> model_location.Province:
    db_province = await session.get(model_location.Province, province_id)
    if not db_province:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Province with ID {province_id} not found",
        )
    update_data = province.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_province, key, value)
    session.add(db_province)
    await session.commit()
    await session.refresh(db_province)
    return schema_location.province_schema.model_validate(db_province)


@router.delete("/provinces/{province_id}")
async def delete_province(
    province_id: int, session: AsyncSession = Depends(models.get_session)
):
    db_province = await session.get(model_location.Province, province_id)
    if not db_province:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Province with ID {province_id} not found",
        )
    await session.delete(db_province)
    await session.commit()
    return {"message": f"Province {province_id} deleted successfully."}
