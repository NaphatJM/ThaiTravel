from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from decimal import Decimal

from ttt.schemas import schema_activity
from ttt.models import model_activity
from sqlmodel import select
from ttt import models

router = APIRouter(prefix="/activities", tags=["Activity"])


@router.get("/", response_model=list[schema_activity.Activity_schema])
async def get_activities(session: AsyncSession = Depends(models.get_session)):
    statement = select(model_activity.Activity)
    results = await session.exec(statement)
    db_activities = results.all()
    if not db_activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No activities found"
        )
    return [schema_activity.Activity_schema.model_validate(a) for a in db_activities]


@router.get("/{activity_id}", response_model=schema_activity.Activity_schema)
async def get_activity(
    activity_id: int, session: AsyncSession = Depends(models.get_session)
) -> model_activity.Activity:
    statement = select(model_activity.Activity).where(
        model_activity.Activity.id == activity_id
    )
    results = await session.exec(statement)
    db_activity = results.one_or_none()
    if not db_activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity with ID {activity_id} not found",
        )
    return schema_activity.Activity_schema.model_validate(db_activity)


@router.post("/", response_model=dict)
async def create_activity(
    activity: schema_activity.Activity_create_schema,
    session: AsyncSession = Depends(models.get_session),
):
    tax_stmt = select(models.TaxReduction).where(
        models.TaxReduction.province_id == activity.province_id
    )
    tax_result = await session.exec(tax_stmt)
    tax = tax_result.one_or_none()

    if not tax:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No tax reduction found for province ID {activity.province_id}",
        )

    tax_return_value = (
        activity.amount * Decimal(tax.tax_discount_percent) / Decimal(100)
    )

    activity_data = activity.model_dump(exclude={"tax_return"})

    db_activity = model_activity.Activity(**activity_data, tax_return=tax_return_value)

    session.add(db_activity)
    await session.commit()
    await session.refresh(db_activity)

    return {"ภาษีที่สามารถลดหย่อนได้": tax_return_value}


@router.put("/{activity_id}", response_model=schema_activity.Activity_schema)
async def update_activity(
    activity_id: int,
    activity: schema_activity.Activity_update_schema,
    session: AsyncSession = Depends(models.get_session),
) -> model_activity.Activity:
    statement = select(model_activity.Activity).where(
        model_activity.Activity.id == activity_id
    )
    results = await session.exec(statement)
    db_activity = results.one_or_none()
    if not db_activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity with ID {activity_id} not found",
        )
    update_activity = activity.model_dump(exclude_unset=True)
    for key, value in update_activity.items():
        setattr(db_activity, key, value)
    session.add(db_activity)
    await session.commit()
    await session.refresh(db_activity)
    return schema_activity.Activity_schema.model_validate(db_activity)


@router.delete("/{activity_id}")
async def delete_activity(
    activity_id: int, session: AsyncSession = Depends(models.get_session)
):
    statement = select(model_activity.Activity).where(
        model_activity.Activity.id == activity_id
    )
    results = await session.exec(statement)
    db_activity = results.one_or_none()
    if not db_activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity with ID {activity_id} not found",
        )
    await session.delete(db_activity)
    await session.commit()
    return {"message": f"Activity {activity_id} deleted successfully."}
