from fastapi import APIRouter
from services.scheme_service import get_all_schemes, get_scheme_by_category, get_urgent_schemes

router = APIRouter()


@router.get("/schemes")
def list_schemes():
    """
    Saari available govt schemes ki list deta hai.
    """
    return {"schemes": get_all_schemes()}


@router.get("/schemes/category/{category}")
def schemes_by_category(category: str):
    """
    Category se filter karta hai.
    Example: /schemes/category/insurance
    """
    schemes = get_scheme_by_category(category)
    return {"category": category, "schemes": schemes}


@router.get("/schemes/urgent")
def urgent_schemes(days: int = 30):
    """
    Jin schemes ki deadline najdeek hai.
    Example: /schemes/urgent?days=15
    """
    schemes = get_urgent_schemes(days)
    return {"urgent_schemes": schemes}