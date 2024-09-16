from fastapi import APIRouter

from .endpoints.company import router as company_router
from .endpoints.authentication import router as authentication_router
from .endpoints.orders import router as orders_router
from .endpoints.items import router as items_router

router = APIRouter()
router.include_router(company_router, tags=["Company"])
router.include_router(authentication_router, tags=["Authentication"])
router.include_router(orders_router, tags=["Orders"])
router.include_router(items_router, tags=["Items"])

