from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_patients():
    return [
        {"id": 1, "name": "John Doe", "age": 35},
        {"id": 2, "name": "Jane Smith", "age": 28}
    ]
