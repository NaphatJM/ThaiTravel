from fastapi import APIRouter

from .authentication_router import router as auth_router
from .route_user import router as user_router
from .route_location import router as location_router
from .route_activity import router as activity_router
from .route_tax import router as tax_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(location_router)
router.include_router(activity_router)
router.include_router(tax_router)
router.include_router(user_router)
