from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlmodel import select
from ttt.schemas import schema_location
from ttt.models import model_location
from ttt import models
from typing import List

router = APIRouter(prefix="/tax_reductions", tags=["Tax Reduction"])


@router.get("/", response_model=List[schema_location.taxReduction_schema])
async def get_tax_reductions(session: AsyncSession = Depends(models.get_session)):
    statement = select(model_location.TaxReduction)
    results = await session.exec(statement)
    db_tax_reductions = results.all()
    if not db_tax_reductions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No tax reductions found"
        )
    return [
        schema_location.taxReduction_schema.model_validate(t) for t in db_tax_reductions
    ]


@router.get("/{tax_reduction_id}", response_model=schema_location.taxReduction_schema)
async def get_tax_reduction(
    tax_reduction_id: int, session: AsyncSession = Depends(models.get_session)
) -> model_location.TaxReduction:
    db_tax_reduction = await session.get(model_location.TaxReduction, tax_reduction_id)
    if not db_tax_reduction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tax reduction with ID {tax_reduction_id} not found",
        )
    return schema_location.taxReduction_schema.model_validate(db_tax_reduction)


@router.post("/", response_model=schema_location.taxReduction_schema)
async def create_tax_reduction(
    tax_reduction: schema_location.taxReduction_create_schema,
    session: AsyncSession = Depends(models.get_session),
) -> model_location.TaxReduction:
    db_tax_reduction = model_location.TaxReduction(**tax_reduction.model_dump())
    session.add(db_tax_reduction)
    await session.commit()
    await session.refresh(db_tax_reduction)
    return schema_location.taxReduction_schema.model_validate(db_tax_reduction)


@router.put("/{tax_reduction_id}", response_model=schema_location.taxReduction_schema)
async def update_tax_reduction(
    tax_reduction_id: int,
    tax_reduction: schema_location.taxReduction_update_schema,
    session: AsyncSession = Depends(models.get_session),
):
    db_tax_reduction = await session.get(model_location.TaxReduction, tax_reduction_id)
    if not db_tax_reduction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tax reduction with ID {tax_reduction_id} not found",
        )
    for key, value in tax_reduction.model_dump(exclude_unset=True).items():
        setattr(db_tax_reduction, key, value)
    session.add(db_tax_reduction)
    await session.commit()
    await session.refresh(db_tax_reduction)
    return schema_location.taxReduction_schema.model_validate(db_tax_reduction)


@router.delete("/{tax_reduction_id}")
async def delete_tax_reduction(
    tax_reduction_id: int, session: AsyncSession = Depends(models.get_session)
):
    db_tax_reduction = await session.get(model_location.TaxReduction, tax_reduction_id)
    if not db_tax_reduction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tax reduction with ID {tax_reduction_id} not found",
        )
    await session.delete(db_tax_reduction)
    await session.commit()
    return {"message": f"Tax reduction {tax_reduction_id} deleted successfully."}
