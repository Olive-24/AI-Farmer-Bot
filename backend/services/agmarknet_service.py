import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AGMARKNET_API_KEY")
RESOURCE_ID = os.getenv("AGMARKNET_RESOURCE_ID")
BASE_URL = f"https://api.data.gov.in/resource/{RESOURCE_ID}"

TRANSPORT_COST_PER_KM_PER_QUINTAL = 4  # ₹ per km per quintal (estimate)
PAGE_SIZE = 10  # API ki hard limit per request


# ---------------------------------------------------------
# MOCK DATA — fallback jab real govt API slow/down ho
# ---------------------------------------------------------
MOCK_MANDI_DATA = {
    "wheat": [
        {"mandi": "Karnal", "state": "Haryana", "district": "Karnal", "min_price": 2280, "max_price": 2380, "modal_price": 2340, "arrival_date": "mock"},
        {"mandi": "Ambala", "state": "Haryana", "district": "Ambala", "min_price": 2450, "max_price": 2560, "modal_price": 2510, "arrival_date": "mock"},
        {"mandi": "Panipat", "state": "Haryana", "district": "Panipat", "min_price": 2300, "max_price": 2400, "modal_price": 2360, "arrival_date": "mock"},
        {"mandi": "Sonipat", "state": "Haryana", "district": "Sonipat", "min_price": 2310, "max_price": 2410, "modal_price": 2365, "arrival_date": "mock"},
        {"mandi": "Delhi Azadpur", "state": "Delhi", "district": "Delhi", "min_price": 2380, "max_price": 2470, "modal_price": 2420, "arrival_date": "mock"},
    ],
    "onion": [
        {"mandi": "Nashik", "state": "Maharashtra", "district": "Nashik", "min_price": 2000, "max_price": 2150, "modal_price": 2080, "arrival_date": "mock"},
        {"mandi": "Pune", "state": "Maharashtra", "district": "Pune", "min_price": 1950, "max_price": 2050, "modal_price": 2000, "arrival_date": "mock"},
        {"mandi": "Lasalgaon", "state": "Maharashtra", "district": "Nashik", "min_price": 2050, "max_price": 2200, "modal_price": 2120, "arrival_date": "mock"},
        {"mandi": "Indore", "state": "Madhya Pradesh", "district": "Indore", "min_price": 1850, "max_price": 1980, "modal_price": 1920, "arrival_date": "mock"},
    ],
    "tomato": [
        {"mandi": "Kolar", "state": "Karnataka", "district": "Kolar", "min_price": 1200, "max_price": 1400, "modal_price": 1300, "arrival_date": "mock"},
        {"mandi": "Bangalore", "state": "Karnataka", "district": "Bangalore", "min_price": 1350, "max_price": 1500, "modal_price": 1420, "arrival_date": "mock"},
        {"mandi": "Madanapalle", "state": "Andhra Pradesh", "district": "Annamayya", "min_price": 1280, "max_price": 1450, "modal_price": 1360, "arrival_date": "mock"},
        {"mandi": "Nashik", "state": "Maharashtra", "district": "Nashik", "min_price": 1150, "max_price": 1320, "modal_price": 1240, "arrival_date": "mock"},
    ],
    "potato": [
        {"mandi": "Agra", "state": "Uttar Pradesh", "district": "Agra", "min_price": 980, "max_price": 1100, "modal_price": 1040, "arrival_date": "mock"},
        {"mandi": "Farrukhabad", "state": "Uttar Pradesh", "district": "Farrukhabad", "min_price": 1020, "max_price": 1150, "modal_price": 1085, "arrival_date": "mock"},
        {"mandi": "Indore", "state": "Madhya Pradesh", "district": "Indore", "min_price": 990, "max_price": 1120, "modal_price": 1055, "arrival_date": "mock"},
    ],
    "rice": [
        {"mandi": "Karnal", "state": "Haryana", "district": "Karnal", "min_price": 3100, "max_price": 3300, "modal_price": 3200, "arrival_date": "mock"},
        {"mandi": "Amritsar", "state": "Punjab", "district": "Amritsar", "min_price": 3200, "max_price": 3420, "modal_price": 3310, "arrival_date": "mock"},
        {"mandi": "Raipur", "state": "Chhattisgarh", "district": "Raipur", "min_price": 2950, "max_price": 3150, "modal_price": 3050, "arrival_date": "mock"},
    ],
    "cabbage": [
        {"mandi": "Mukkom Market", "state": "Keralam", "district": "Kozhikode", "min_price": 2400, "max_price": 2600, "modal_price": 2500, "arrival_date": "mock"},
        {"mandi": "Bangalore", "state": "Karnataka", "district": "Bangalore", "min_price": 2200, "max_price": 2450, "modal_price": 2320, "arrival_date": "mock"},
    ],
}


def get_mock_prices(crop: str):
    crop = crop.strip().lower()
    return MOCK_MANDI_DATA.get(crop, [])


# ---------------------------------------------------------
# REAL API — Agmarknet se live data
# ---------------------------------------------------------
def fetch_raw_records(max_pages: int = 5, timeout_seconds: int = 8):
    """
    Bina filter ke, multiple pages fetch karta hai (govt API ka filter unreliable hai).
    timeout_seconds kam rakha hai (8 sec) taaki overall request zyada na latke -
    agar govt server slow hai, hum jaldi give up karke mock data pe switch karenge.
    """
    all_records = []

    for page in range(max_pages):
        offset = page * PAGE_SIZE
        params = {
            "api-key": API_KEY,
            "format": "json",
            "limit": PAGE_SIZE,
            "offset": offset,
        }

        try:
            response = requests.get(BASE_URL, params=params, timeout=timeout_seconds)
            if response.status_code != 200:
                print(f"Page {page}: status {response.status_code}")
                continue
            data = response.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Page {page} error: {e}")
            continue

        records = data.get("records", [])
        if not records:
            break

        all_records.extend(records)

    return all_records


def get_real_prices(crop: str, max_pages: int = 5):
    crop = crop.strip().lower()
    raw_records = fetch_raw_records(max_pages=max_pages)

    mandis = []
    for r in raw_records:
        commodity_name = str(r.get("commodity", "")).strip().lower()
        if crop in commodity_name or commodity_name in crop:
            mandis.append({
                "mandi": r.get("market", "Unknown"),
                "state": r.get("state", "Unknown"),
                "district": r.get("district", "Unknown"),
                "min_price": float(r.get("min_price", 0)),
                "max_price": float(r.get("max_price", 0)),
                "modal_price": float(r.get("modal_price", 0)),
                "arrival_date": r.get("arrival_date", ""),
            })
    return mandis


# ---------------------------------------------------------
# HYBRID — real API try karo, fail ho toh mock data do
# ---------------------------------------------------------
def get_mandi_prices(crop: str, max_pages: int = 5):
    """
    Pehle real Agmarknet API try karta hai. Agar woh empty/fail ho jaye
    (govt server slow/down), automatically mock data pe fallback karta hai.
    Response mein 'source' field bata deta hai data kahan se aaya.
    """
    real_prices = get_real_prices(crop, max_pages=max_pages)

    if real_prices:
        for p in real_prices:
            p["source"] = "live_api"
        return real_prices

    # Fallback to mock data
    mock_prices = get_mock_prices(crop)
    for p in mock_prices:
        p["source"] = "mock_fallback"
    return mock_prices


def get_best_mandi(crop: str):
    prices = get_mandi_prices(crop)
    if not prices:
        return None
    best = max(prices, key=lambda x: x["modal_price"])
    return best


def get_best_mandi_smart(crop: str, quantity_quintal: float = 1):
    """
    Net profit (price - transport cost) ke hisaab se best mandi suggest karta hai.
    """
    prices = get_mandi_prices(crop)
    if not prices:
        return None

    results = []
    for mandi in prices:
        distance_km = 0  # Future: Maps API se actual distance
        transport_cost_per_quintal = distance_km * TRANSPORT_COST_PER_KM_PER_QUINTAL
        net_price_per_quintal = mandi["modal_price"] - transport_cost_per_quintal

        results.append({
            "mandi": mandi["mandi"],
            "state": mandi["state"],
            "district": mandi["district"],
            "modal_price": mandi["modal_price"],
            "distance_km": distance_km,
            "net_price_per_quintal": round(net_price_per_quintal, 2),
            "arrival_date": mandi["arrival_date"],
            "source": mandi.get("source", "unknown"),
        })

    results.sort(key=lambda x: x["net_price_per_quintal"], reverse=True)

    return {
        "best_option": results[0] if results else None,
        "all_options": results
    }


def get_available_crops(max_pages: int = 5):
    """
    Real API se commodities list karta hai. Fail hone par mock data ke crops deta hai.
    """
    raw_records = fetch_raw_records(max_pages=max_pages)
    crops = set()
    for r in raw_records:
        commodity_name = r.get("commodity", "").strip()
        if commodity_name:
            crops.add(commodity_name)

    if crops:
        return sorted(list(crops))

    # Fallback
    return sorted([c.capitalize() for c in MOCK_MANDI_DATA.keys()])

def evaluate_trader_offer(crop: str, offer_price: float, quantity_quintal: float = 1):
    """
    Trader ke offer ko mandi prices se compare karke advice deta hai.
    Negotiation coach - Scenario 4 wala feature.
    """
    prices = get_mandi_prices(crop)
    if not prices:
        return None

    # Average modal price nikal saari mandis ka
    avg_price = sum(m["modal_price"] for m in prices) / len(prices)

    # Best mandi bhi nikal lo comparison ke liye
    best = max(prices, key=lambda x: x["modal_price"])

    diff_from_avg = avg_price - offer_price
    percent_diff = (diff_from_avg / avg_price) * 100 if avg_price > 0 else 0

    # Decision logic
    if percent_diff <= 0:
        verdict = "accept"
        advice = f"Yeh offer (₹{offer_price}) mandi average (₹{round(avg_price, 2)}) se behtar ya barabar hai. Accept kar sakte ho!"
    elif percent_diff < 5:
        verdict = "accept"
        advice = f"Offer thoda kam hai mandi average se, but difference sirf {round(percent_diff, 1)}% hai - reasonable hai. Accept kar sakte ho ya thoda negotiate kar lo."
    elif percent_diff < 15:
        counter_price = round(avg_price * 0.97, 2)  # 3% margin negotiate ke liye
        verdict = "counter"
        advice = f"Yeh offer mandi average se {round(percent_diff, 1)}% kam hai. Counter karo ₹{counter_price}/quintal pe."
    else:
        counter_price = round(avg_price * 0.97, 2)
        verdict = "reject_or_counter"
        advice = f"Yeh offer mandi average se {round(percent_diff, 1)}% kam hai - bahut kam hai! Counter karo ₹{counter_price}/quintal pe, ya '{best['mandi']}, {best['state']}' mandi try karo jaha ₹{best['modal_price']}/quintal mil raha hai."

    total_loss_if_accepted = round((avg_price - offer_price) * quantity_quintal, 2)

    return {
        "crop": crop,
        "offer_price": offer_price,
        "mandi_average_price": round(avg_price, 2),
        "best_mandi": {"name": best["mandi"], "state": best["state"], "price": best["modal_price"]},
        "percent_difference": round(percent_diff, 2),
        "verdict": verdict,
        "advice": advice,
        "potential_loss_total": total_loss_if_accepted if total_loss_if_accepted > 0 else 0,
        "quantity_quintal": quantity_quintal,
    }