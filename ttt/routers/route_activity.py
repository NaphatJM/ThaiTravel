from fastapi import APIRouter, HTTPException, status
from ttt.schemas import schema_activity
from ttt.models import model_activity
from sqlmodel import select
from ttt import models

router = APIRouter(prefix="/activities", tags=["Activity"])


@router.get("/")
async def get_activities():
    statement = select(model_activity.Activity)
    results = models.session.exec(statement)
    db_activities = results.all()
    if not db_activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No activities found"
        )
    return db_activities


@router.get("/{activity_id}", response_model=schema_activity.Activity_schema)
async def get_activity(activity_id: int) -> model_activity.Activity:
    statement = select(model_activity.Activity).where(
        model_activity.Activity.id == activity_id
    )
    results = models.session.exec(statement)
    db_activity = results.one_or_none()
    if not db_activity:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity with ID {activity_id} not found",
        )
    return db_activity


@router.post("/", response_model=schema_activity.Activity_schema)
async def create_activity(
    activity: schema_activity.Activity_schema,
) -> model_activity.Activity:
    db_activity = model_activity.Activity(**activity.model_dump())
    models.session.add(db_activity)
    models.session.commit()
    models.session.refresh(db_activity)
    return db_activity


@router.put("/{activity_id}", response_model=schema_activity.Activity_schema)
async def update_activity(
    activity_id: int, activity: schema_activity.Activity_schema
) -> model_activity.Activity:
    statement = select(model_activity.Activity).where(
        model_activity.Activity.id == activity_id
    )
    results = models.session.exec(statement)
    db_activity = results.one_or_none()
    if not db_activity:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity with ID {activity_id} not found",
        )
    for key, value in activity.items():
        setattr(db_activity, key, value)
    models.session.add(db_activity)
    models.session.commit()
    models.session.refresh(db_activity)
    return db_activity


@router.delete("/{activity_id}")
async def delete_activity(activity_id: int):
    statement = select(model_activity.Activity).where(
        model_activity.Activity.id == activity_id
    )
    results = models.session.exec(statement)
    db_activity = results.one_or_none()
    if not db_activity:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity with ID {activity_id} not found",
        )
    models.session.delete(db_activity)
    models.session.commit()
    return {"message": f"Activity {activity_id} deleted successfully."}
