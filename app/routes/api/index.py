from fastapi import APIRouter
from app.routes.api.userRoutes import router as user_router
from app.routes.api.predictRoutes import router as predict_router

router = APIRouter()
router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(predict_router, tags=["ml"])
