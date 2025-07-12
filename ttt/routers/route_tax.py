from fastapi import APIRouter
from ttt.schemas.schema_location import taxReduction
from typing import List

router = APIRouter(prefix="/tax_reductions", tags=["Tax Reduction"])


@router.get("/")
async def get_tax_reductions():
    return [
        taxReduction(id=1, province_=1, tax_discount_percent=5.0),
        taxReduction(id=2, province_=2, tax_discount_percent=10.0),
        taxReduction(id=3, province_=3, tax_discount_percent=15.0),
    ]


@router.get("/{tax_reduction_id}")
async def get_tax_reduction(tax_reduction_id: int):
    return taxReduction(
        id=tax_reduction_id,
        province_=1,
        tax_discount_percent=5.0 if tax_reduction_id == 1 else 10.0,
    )


@router.post("/")
async def create_tax_reduction(tax_reduction: taxReduction):
    return tax_reduction


@router.put("/{tax_reduction_id}")
async def update_tax_reduction(tax_reduction_id: int, tax_reduction: taxReduction):
    return tax_reduction


@router.delete("/{tax_reduction_id}")
async def delete_tax_reduction(tax_reduction_id: int):
    return {"message": f"Tax reduction {tax_reduction_id} deleted successfully."}
