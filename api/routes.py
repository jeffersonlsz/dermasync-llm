from fastapi import APIRouter
from .endpoints import router as endpoints_router
from .segmentos import router as segmentos_router

router = APIRouter()
router.include_router(endpoints_router)
router.include_router(segmentos_router)