from fastapi import FastAPI
from app.api import patients

app = FastAPI(title="AyurSutra – Panchakarma Patient Management")
app.include_router(patients.router, prefix="/patients", tags=["Patients"])

@app.get("/")
def root():
    return {"message": "Welcome to AyurSutra API"}
