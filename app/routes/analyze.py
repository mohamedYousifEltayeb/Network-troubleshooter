from fastapi import APIRouter
from app.core.templates import templates

router = APIRouter()

@router.get("/test")
def tester():
    return {
        "Message":"Analyzer router works!"
    }
