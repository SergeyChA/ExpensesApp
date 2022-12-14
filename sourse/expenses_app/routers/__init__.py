from fastapi import APIRouter
from . import (
    operations,
    auth,
    reports
)


router = APIRouter()
router.include_router(operations.router)
router.include_router(auth.router)
router.include_router(reports.router)

