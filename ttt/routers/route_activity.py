from fastapi import APIRouter
from ttt.schemas.schema_activity import Activity
from typing import List

router = APIRouter(prefix="/activities", tags=["Activity"])


@router.get("/", response_model=List[Activity])
async def get_activities():
    return [
        Activity(
            id=1,
            user_id=1,
            description="Description for Activity 1",
            location="Location 1",
            amount=100,
            tax_return=10,
        ),
        Activity(
            id=2,
            user_id=2,
            description="Description for Activity 2",
            location="Location 2",
            amount=200,
            tax_return=None,
        ),
    ]


@router.post("/", response_model=Activity)
async def create_activity(activity: Activity):
    return activity


@router.get("/{activity_id}", response_model=Activity)
async def get_activity(activity_id: int):
    return Activity(
        id=activity_id,
        user_id=1,
        description=f"Description for Activity {activity_id}",
        location=f"Location {activity_id}",
        amount=100,
        tax_return=10 if activity_id == 1 else None,
    )


@router.put("/{activity_id}", response_model=Activity)
async def update_activity(activity_id: int, activity: Activity):
    return activity


@router.delete("/{activity_id}")
async def delete_activity(activity_id: int):
    return {"message": f"Activity {activity_id} deleted successfully."}
