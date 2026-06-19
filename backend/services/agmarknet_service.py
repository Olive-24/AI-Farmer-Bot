# Mock mandi price data (jab tak real API key nahi milti)
# Real Agmarknet API jaisa hi structure hai - baad mein easily swap ho jayega

MOCK_MANDI_DATA = {
    "wheat": [
        {"mandi": "Karnal", "state": "Haryana", "min_price": 2280, "max_price": 2380, "modal_price": 2340, "distance_km": 0},
        {"mandi": "Ambala", "state": "Haryana", "min_price": 2450, "max_price": 2560, "modal_price": 2510, "distance_km": 38},
        {"mandi": "Panipat", "state": "Haryana", "min_price": 2300, "max_price": 2400, "modal_price": 2360, "distance_km": 22},
        {"mandi": "Sonipat", "state": "Haryana", "min_price": 2310, "max_price": 2410, "modal_price": 2365, "distance_km": 30},
        {"mandi": "Kurukshetra", "state": "Haryana", "min_price": 2400, "max_price": 2490, "modal_price": 2450, "distance_km": 55},
        {"mandi": "Hisar", "state": "Haryana", "min_price": 2260, "max_price": 2350, "modal_price": 2305, "distance_km": 90},
        {"mandi": "Delhi Azadpur", "state": "Delhi", "min_price": 2380, "max_price": 2470, "modal_price": 2420, "distance_km": 70},
    ],
    "onion": [
        {"mandi": "Nashik", "state": "Maharashtra", "min_price": 2000, "max_price": 2150, "modal_price": 2080, "distance_km": 45},
        {"mandi": "Pune", "state": "Maharashtra", "min_price": 1950, "max_price": 2050, "modal_price": 2000, "distance_km": 0},
        {"mandi": "Lasalgaon", "state": "Maharashtra", "min_price": 2050, "max_price": 2200, "modal_price": 2120, "distance_km": 60},
        {"mandi": "Solapur", "state": "Maharashtra", "min_price": 1900, "max_price": 2020, "modal_price": 1960, "distance_km": 85},
        {"mandi": "Indore", "state": "Madhya Pradesh", "min_price": 1850, "max_price": 1980, "modal_price": 1920, "distance_km": 250},
        {"mandi": "Bengaluru", "state": "Karnataka", "min_price": 2100, "max_price": 2250, "modal_price": 2180, "distance_km": 620},
    ],
    "tomato": [
        {"mandi": "Kolar", "state": "Karnataka", "min_price": 1200, "max_price": 1400, "modal_price": 1300, "distance_km": 0},
        {"mandi": "Bangalore", "state": "Karnataka", "min_price": 1350, "max_price": 1500, "modal_price": 1420, "distance_km": 65},
        {"mandi": "Madanapalle", "state": "Andhra Pradesh", "min_price": 1280, "max_price": 1450, "modal_price": 1360, "distance_km": 180},
        {"mandi": "Nashik", "state": "Maharashtra", "min_price": 1150, "max_price": 1320, "modal_price": 1240, "distance_km": 320},
    ],
    "potato": [
        {"mandi": "Agra", "state": "Uttar Pradesh", "min_price": 980, "max_price": 1100, "modal_price": 1040, "distance_km": 0},
        {"mandi": "Farrukhabad", "state": "Uttar Pradesh", "min_price": 1020, "max_price": 1150, "modal_price": 1085, "distance_km": 75},
        {"mandi": "Hooghly", "state": "West Bengal", "min_price": 950, "max_price": 1080, "modal_price": 1010, "distance_km": 1100},
        {"mandi": "Indore", "state": "Madhya Pradesh", "min_price": 990, "max_price": 1120, "modal_price": 1055, "distance_km": 520},
    ],
    "rice": [
        {"mandi": "Karnal", "state": "Haryana", "min_price": 3100, "max_price": 3300, "modal_price": 3200, "distance_km": 0},
        {"mandi": "Kaithal", "state": "Haryana", "min_price": 3150, "max_price": 3350, "modal_price": 3260, "distance_km": 45},
        {"mandi": "Amritsar", "state": "Punjab", "min_price": 3200, "max_price": 3420, "modal_price": 3310, "distance_km": 250},
        {"mandi": "Raipur", "state": "Chhattisgarh", "min_price": 2950, "max_price": 3150, "modal_price": 3050, "distance_km": 900},
    ],
    "sugarcane": [
        {"mandi": "Muzaffarnagar", "state": "Uttar Pradesh", "min_price": 340, "max_price": 360, "modal_price": 350, "distance_km": 0},
        {"mandi": "Meerut", "state": "Uttar Pradesh", "min_price": 345, "max_price": 365, "modal_price": 355, "distance_km": 35},
        {"mandi": "Kolhapur", "state": "Maharashtra", "min_price": 320, "max_price": 340, "modal_price": 330, "distance_km": 1400},
    ],
    "cotton": [
        {"mandi": "Adilabad", "state": "Telangana", "min_price": 6800, "max_price": 7200, "modal_price": 7000, "distance_km": 0},
        {"mandi": "Akola", "state": "Maharashtra", "min_price": 6900, "max_price": 7300, "modal_price": 7100, "distance_km": 220},
        {"mandi": "Rajkot", "state": "Gujarat", "min_price": 7000, "max_price": 7400, "modal_price": 7200, "distance_km": 950},
    ],
    "maize": [
        {"mandi": "Davangere", "state": "Karnataka", "min_price": 1900, "max_price": 2050, "modal_price": 1980, "distance_km": 0},
        {"mandi": "Nizamabad", "state": "Telangana", "min_price": 1850, "max_price": 2000, "modal_price": 1920, "distance_km": 280},
        {"mandi": "Davanagere Rural", "state": "Karnataka", "min_price": 1920, "max_price": 2070, "modal_price": 2000, "distance_km": 15},
    ],
}


def get_mandi_prices(crop: str):
    """
    Crop ka naam leke uske saare mandi prices return karta hai.
    Real API integration ke time, yeh function sirf andar se change hoga -
    baahar se call karne wala code same rahega.
    """
    crop = crop.lower().strip()
    return MOCK_MANDI_DATA.get(crop, [])


def get_best_mandi(crop: str):
    """
    Sabse zyada modal_price wali mandi return karta hai.
    """
    prices = get_mandi_prices(crop)
    if not prices:
        return None
    best = max(prices, key=lambda x: x["modal_price"])
    return best


def get_available_crops():
    """
    Saare crops ki list return karta hai jinka data available hai.
    """
    return list(MOCK_MANDI_DATA.keys())