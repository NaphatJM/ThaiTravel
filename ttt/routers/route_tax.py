from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from ttt.schemas import schema_location
from ttt.models import model_location
from ttt import models
from typing import List

router = APIRouter(prefix="/tax_reductions", tags=["Tax Reduction"])


@router.get("/")
async def get_tax_reductions():
    statement = select(model_location.TaxReduction)
    results = models.session.exec(statement)
    db_tax_reductions = results.all()
    if not db_tax_reductions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No tax reductions found"
        )
    return db_tax_reductions


@router.get("/{tax_reduction_id}")
async def get_tax_reduction(tax_reduction_id: int) -> model_location.TaxReduction:
    db_tax_reduction = models.session.get(model_location.TaxReduction, tax_reduction_id)
    if not db_tax_reduction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tax reduction with ID {tax_reduction_id} not found",
        )
    return db_tax_reduction


@router.post("/")
async def create_tax_reduction(
    tax_reduction: schema_location.taxReduction_create_schema,
) -> model_location.TaxReduction:
    db_tax_reduction = model_location.TaxReduction(**tax_reduction.model_dump())
    models.session.add(db_tax_reduction)
    models.session.commit()
    models.session.refresh(db_tax_reduction)
    return db_tax_reduction


@router.put("/{tax_reduction_id}")
async def update_tax_reduction(
    tax_reduction_id: int, tax_reduction: schema_location.taxReduction_update_schema
):
    db_tax_reduction = models.session.get(model_location.TaxReduction, tax_reduction_id)
    if not db_tax_reduction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tax reduction with ID {tax_reduction_id} not found",
        )
    for key, value in tax_reduction.model_dump(exclude_unset=True).items():
        setattr(db_tax_reduction, key, value)
    models.session.add(db_tax_reduction)
    models.session.commit()
    models.session.refresh(db_tax_reduction)
    return db_tax_reduction


@router.delete("/{tax_reduction_id}")
async def delete_tax_reduction(tax_reduction_id: int):
    db_tax_reduction = models.session.get(model_location.TaxReduction, tax_reduction_id)
    if not db_tax_reduction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tax reduction with ID {tax_reduction_id} not found",
        )
    models.session.delete(db_tax_reduction)
    models.session.commit()
    return {"message": f"Tax reduction {tax_reduction_id} deleted successfully."}
