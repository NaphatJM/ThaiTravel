from fastapi import APIRouter

from ttt.routers import route_location, route_activity, route_tax, route_user

router = APIRouter()
router.include_router(route_location.router)
router.include_router(route_activity.router)
router.include_router(route_tax.router)
router.include_router(route_user.router)
