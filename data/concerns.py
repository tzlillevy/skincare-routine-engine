"""
בסיס נתונים ומיפוי דרמטולוגי עבור סוגי עור, בעיות עור ורכיבים פעילים.
"""

SKIN_TYPES = {
    "oily": "עור שמן (ברק מוגבר, נטייה לפצעונים ונקבוביות)",
    "dry": "עור יבש (תחושת מתיחה, חספוס וקילופים)",
    "combination": "עור מעורב (שמנוניות באזור ה-T ויובש בלחיים)",
    "normal": "עור רגיל (מאוזן, ללא יובש או שמנוניות יתר)"
}

SKIN_CONCERNS = {
    "acne": "פצעונים ואקנה",
    "blackheads": "ראשים שחורים ונקבוביות חסומות",
    "texture": "מרקם עור לא אחיד ונקבוביות מורחבות",
    "hyperpigmentation": "כתמי שמש ופיגמנטציה",
    "pie_redness": "סימנים אדומים לאחר פצעונים (PIE)",
    "pih_redness": "כתמים כהים לאחר פצעונים (PIH)",
    "damaged_barrier": "מחסום עור פגוע (עקצוץ, אדמומיות ושריפה)",
    "eczema": "אקזמה וגירויים",
    "seborrhea": "סבוריאה וקילופים",
    "dehydrated_skin": "עור מיובש (חסר בלחות פנימית)",
    "anti_aging": "קמטוטים וסימני גיל",
    "redness": "אדמומיות כללית ורגישות",
    "dark_circles": "כהויות מתחת לעיניים",
    "eye_puffiness": "נפיחות מסביב לעיניים",
    "keratosis_pilaris": "חרסוסית (עור ברווז)",
    "insect_bites": "עקיצות וגירוי מקומי"
}

CONCERN_SAFETY_FLAGS = {
    "damaged_barrier": {
        "block_acids": True,
        "block_retinoids": True,
        "block_pure_vitamin_c": True,
        "focus": "barrier_repair"
    },
    "eczema": {
        "block_acids": True,
        "block_retinoids": True,
        "block_pure_vitamin_c": True,
        "focus": "soothing"
    }
}

CONCERN_TO_INGREDIENTS = {
    "acne": ["Salicylic_Acid", "Benzoyl_Peroxide", "Niacinamide", "Retinoids", "Tea_Tree"],
    "blackheads": ["Salicylic_Acid", "BHA", "Niacinamide", "Clay"],
    "texture": ["AHA", "Glycolic_Acid", "Lactic_Acid", "Retinoids"],
    "hyperpigmentation": ["Pure_Vitamin_C", "Niacinamide", "Azelaic_Acid", "Tranexamic_Acid", "Alpha_Arbutin"],
    "pie_redness": ["Azelaic_Acid", "Niacinamide", "Centella_Asiatica", "Tranexamic_Acid"],
    "pih_redness": ["Pure_Vitamin_C", "Azelaic_Acid", "Alpha_Arbutin", "Retinoids"],
    "damaged_barrier": ["Ceramides", "Hyaluronic_Acid", "Centella_Asiatica", "Panthenol", "Peptides"],
    "eczema": ["Ceramides", "Colloidal_Oatmeal", "Panthenol", "Hyaluronic_Acid"],
    "seborrhea": ["Zinc_Pyrithione", "Niacinamide", "Salicylic_Acid"],
    "dehydrated_skin": ["Hyaluronic_Acid", "Glycerin", "Ceramides", "Squalane"],
    "anti_aging": ["Retinoids", "Peptides", "Copper_Peptides", "Pure_Vitamin_C"],
    "redness": ["Centella_Asiatica", "Azelaic_Acid", "Panthenol", "Allantoin"],
    "dark_circles": ["Caffeine", "Peptides", "Pure_Vitamin_C"],
    "eye_puffiness": ["Caffeine", "Green_Tea", "Peptides"],
    "keratosis_pilaris": ["Salicylic_Acid", "Urea", "Lactic_Acid", "AHA"],
    "insect_bites": ["Centella_Asiatica", "Panthenol", "Aloe_Vera", "Allantoin"]
}

def get_concern_ingredients(concern: str) -> list[str]:
    """מחזיר את רשימת הרכיבים המומלצים עבור בעיית עור נתונה."""
    aliases = {
        "pie": "pie_redness",
        "pih": "pih_redness",
        "barrier": "damaged_barrier",
        "aging": "anti_aging",
        "pores": "texture",
        "large_pores": "texture",
        "dryness": "dehydrated_skin",
        "excess_oil": "acne",
        "uneven_texture": "texture"
    }

    clean_key = aliases.get(concern, concern)
    if clean_key in CONCERN_TO_INGREDIENTS:
        return CONCERN_TO_INGREDIENTS[clean_key]
    raise ValueError(f"Unknown concern: {concern}")