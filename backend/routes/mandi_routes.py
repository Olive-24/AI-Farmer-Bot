from services.agmarknet_service import get_mandi_prices, get_best_mandi, get_available_crops, get_best_mandi_smart, evaluate_trader_offer
from fastapi import APIRouter, HTTPException
from services.agmarknet_service import get_mandi_prices, get_best_mandi, get_available_crops, get_best_mandi_smart

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


@router.get("/best-mandi-smart/{crop}")
def best_mandi_smart(crop: str, quantity_quintal: float = 1):
    """
    Transport cost factor in karke best NET PROFIT wali mandi suggest karta hai.
    Example: /best-mandi-smart/wheat?quantity_quintal=5
    """
    result = get_best_mandi_smart(crop, quantity_quintal)
    if not result:
        raise HTTPException(status_code=404, detail=f"'{crop}' ke liye data nahi mila.")
    return {"crop": crop, "quantity_quintal": quantity_quintal, **result}

@router.get("/evaluate-offer/{crop}")
def evaluate_offer(crop: str, offer_price: float, quantity_quintal: float = 1):
    """
    Trader ke offer ko evaluate karta hai aur negotiation advice deta hai.
    Example: /evaluate-offer/onion?offer_price=1800&quantity_quintal=5
    """
    result = evaluate_trader_offer(crop, offer_price, quantity_quintal)
    if not result:
        raise HTTPException(status_code=404, detail=f"'{crop}' ke liye data nahi mila.")
    return result