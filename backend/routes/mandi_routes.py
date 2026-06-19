from fastapi import APIRouter, HTTPException
from services.agmarknet_service import get_mandi_prices, get_best_mandi, get_available_crops

router = APIRouter()


@router.get("/crops")
def list_crops():
    """
    Saare available crops ki list deta hai.
    """
    return {"crops": get_available_crops()}


@router.get("/mandi-price/{crop}")
def mandi_price(crop: str):
    """
    Ek crop ka naam leke uske saare mandi prices deta hai.
    Example: /mandi-price/wheat
    """
    prices = get_mandi_prices(crop)
    if not prices:
        raise HTTPException(status_code=404, detail=f"'{crop}' ke liye data nahi mila. Available crops check kar /crops endpoint se.")
    return {"crop": crop, "mandis": prices}


@router.get("/best-mandi/{crop}")
def best_mandi(crop: str):
    """
    Ek crop ke liye sabse best price wali mandi suggest karta hai.
    Example: /best-mandi/onion
    """
    best = get_best_mandi(crop)
    if not best:
        raise HTTPException(status_code=404, detail=f"'{crop}' ke liye data nahi mila.")
    return {"crop": crop, "best_mandi": best}