from fastapi import APIRouter
from app.api import patients

router = APIRouter()
router.include_router(patients.router, prefix="/patients", tags=["Patients"])
