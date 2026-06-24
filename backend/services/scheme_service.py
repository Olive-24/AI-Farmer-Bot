# Govt scheme checker - mock data
# Real PM-Kisan/Kisan Suvidha DB Aadhaar-linked private data hai,
# isliye demo ke liye representative mock schemes bana rahe hain.

from datetime import datetime, timedelta

GOVT_SCHEMES = [
    {
        "id": "pm_kisan",
        "name": "PM-Kisan Samman Nidhi",
        "description": "₹6,000 per year direct income support, 3 installments mein ₹2,000 har 4 mahine",
        "eligibility": "Sabhi landholding farmers (kuch exclusions ke saath - income tax payers, govt employees nahi le sakte)",
        "benefit_amount": "₹6,000/year",
        "category": "income_support",
        "registration_status": "open",
        "deadline": None,
        "how_to_apply": "pmkisan.gov.in pe online register karo, ya nearest CSC (Common Service Centre) jaake",
    },
    {
        "id": "fasal_bima",
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "description": "Crop insurance - natural disasters, pest attacks, disease se hone wale nuksaan ka coverage",
        "eligibility": "Sabhi farmers (loanee aur non-loanee dono)",
        "benefit_amount": "Crop loss ka coverage (premium bahut kam - 1.5-5% of sum insured)",
        "category": "insurance",
        "registration_status": "open",
        "deadline_days_from_now": 12,
        "how_to_apply": "pmfby.gov.in pe ya bank/CSC se register karo, crop sowing ke 10 din ke andar",
    },
    {
        "id": "kisan_credit_card",
        "name": "Kisan Credit Card (KCC)",
        "description": "Low-interest loan (4% tak) crop production, equipment, aur other farm needs ke liye",
        "eligibility": "Sabhi farmers (landowner, tenant farmers, sharecroppers)",
        "benefit_amount": "Loan limit ₹3 lakh tak (interest subsidy ke saath)",
        "category": "credit",
        "registration_status": "open",
        "deadline": None,
        "how_to_apply": "Nearest bank branch mein apply karo, land documents ke saath",
    },
    {
        "id": "soil_health_card",
        "name": "Soil Health Card Scheme",
        "description": "Free soil testing aur fertilizer recommendation report",
        "eligibility": "Sabhi farmers",
        "benefit_amount": "Free service",
        "category": "advisory",
        "registration_status": "open",
        "deadline": None,
        "how_to_apply": "Nearest Krishi Vigyan Kendra (KVK) ya agriculture department office mein contact karo",
    },
    {
        "id": "kusum_yojana",
        "name": "PM-KUSUM (Solar Pump Scheme)",
        "description": "Solar powered irrigation pump pe 60% subsidy",
        "eligibility": "Farmers jo diesel/electric pump use kar rahe hain",
        "benefit_amount": "60% subsidy + 30% bank loan (sirf 10% farmer ko dena hai)",
        "category": "subsidy",
        "registration_status": "open",
        "deadline_days_from_now": 25,
        "how_to_apply": "State renewable energy department ya pmkusum.mnre.gov.in pe register karo",
    },
]


def get_all_schemes():
    """
    Saari available schemes ki list deta hai, deadline calculate karke.
    """
    schemes_with_deadline = []
    for scheme in GOVT_SCHEMES:
        s = scheme.copy()
        if s.get("deadline_days_from_now"):
            deadline_date = datetime.now() + timedelta(days=s["deadline_days_from_now"])
            s["deadline"] = deadline_date.strftime("%d/%m/%Y")
            s["days_remaining"] = s["deadline_days_from_now"]
        schemes_with_deadline.append(s)
    return schemes_with_deadline


def get_scheme_by_category(category: str):
    """
    Category se filter karta hai (income_support, insurance, credit, advisory, subsidy)
    """
    all_schemes = get_all_schemes()
    return [s for s in all_schemes if s["category"] == category.lower()]


def get_urgent_schemes(days_threshold: int = 30):
    """
    Jin schemes ki deadline najdeek hai (default 30 din ke andar)
    """
    all_schemes = get_all_schemes()
    return [s for s in all_schemes if s.get("days_remaining") and s["days_remaining"] <= days_threshold]