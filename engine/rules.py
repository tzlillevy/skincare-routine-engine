"""
Rule engine for skincare routine validation and conflict detection.

This module defines incompatibility rules, product ordering constraints,
and validation functions for skincare routine recommendations.
"""

from typing import Dict, List, Set, Tuple, Optional
from data import Product


# =============================================================================
# INCOMPATIBLE INGREDIENT PAIRS
# =============================================================================

INCOMPATIBLE_PAIRS: Dict[str, Set[str]] = {
    """
    שילובים של רכיבים פעילים שאסור לשים באותו חלון זמן (AM או PM).
    
    קונפליקטים עיקריים:
    - Retinoids + Direct Acids (חומצות ישירות) = אירוג חמור ופוטנציאל נזק לחוסם
    - Retinoids + Pure Vitamin C = עלול להפחית אפקטיביות הדדית
    - Direct Acids + Pure Vitamin C = pH מתנגש ומונח יציבות
    - Benzoyl Peroxide + Retinoids = אירוג מגביר וניוון רטינואידים
    - Benzoyl Peroxide + Pure Vitamin C = ניוון Vitamin C וצמצום יעילות
    - BHA + AHA = חומצות מתחרות על אותו מקום
    """
    # Retinoids conflicts
    "Retinoids": {
        "AHA",           # חומצות ישירות
        "BHA",           # חומצות ישירות
        "PHA",           # חומצות מעודנות
        "Pure_Vitamin_C", # חומצה בעלת pH נמוך
        "Benzoyl_Peroxide", # חומצה עצמאית
    },
    
    # Direct Acids conflicts
    "AHA": {
        "Retinoids",
        "BHA",           # שתי חומצות תחרות
        "Pure_Vitamin_C",
        "Benzoyl_Peroxide",
    },
    
    "BHA": {
        "Retinoids",
        "AHA",
        "Pure_Vitamin_C",
        "Benzoyl_Peroxide",
    },
    
    "PHA": {
        "Retinoids",
        "AHA",
        "Pure_Vitamin_C",
        "Benzoyl_Peroxide",
    },
    
    # Pure Vitamin C conflicts
    "Pure_Vitamin_C": {
        "Retinoids",
        "AHA",
        "BHA",
        "PHA",
        "Benzoyl_Peroxide",
    },
    
    # Benzoyl Peroxide conflicts
    "Benzoyl_Peroxide": {
        "Retinoids",
        "AHA",
        "BHA",
        "Pure_Vitamin_C",
        "Peptides",
        "Copper_Peptides",
    },
    
    # Peptides conflicts
    "Peptides": {
        "AHA",           # חומצות מפרקות פפטידים
        "BHA",
        "PHA",
        "Pure_Vitamin_C", # חמצון הדדי
        "Benzoyl_Peroxide",
    },
    
    # Copper Peptides conflicts
    "Copper_Peptides": {
        "AHA",           # חומצות מפרקות פפטידים
        "BHA",
        "PHA",
        "Pure_Vitamin_C", # חמצון הדדי ופגיעה ביעילות
        "Benzoyl_Peroxide",
    },
}


# =============================================================================
# GENTLE LAYERING SEQUENCE - סדר שלבי מריחה קלאסי
# =============================================================================

ROUTINE_STEP_ORDER: List[str] = [
    "cleanser",      # 1. ניקוי - היסוד הראשון
    "toner",         # 2. טוני - הכנה ויסת pH
    "essence",       # 3. אסנס - הידרציה קלה
    "serum",         # 4. סרום - רכיבים פעילים וטיפול
    "ampoule",       # 5. אמפולה - טיפול מרוכז (אם יש)
    "treatment",     # 6. טיפול - צבעונים או טיפול נקודתי
    "sheet_mask",    # 7. מסכה דיסקית (אם יש) - טיפול עמוק
    "moisturizer",   # 8. לחות - חיתום וזקיקה
    "oil",           # 9. שמן - שכבה נוספת הגנה (PM בלבד)
    "sunscreen",     # 10. SPF - הגנה (AM בלבד)
]

# מיפוי סדר שלבים למספרים לשימוש באלגוריתם
STEP_ORDER_MAP: Dict[str, int] = {step: idx for idx, step in enumerate(ROUTINE_STEP_ORDER)}


# =============================================================================
# TIMING RESTRICTIONS - הגבלות זמן ליישום
# =============================================================================

AM_ONLY_PRODUCTS: Set[str] = {
    "Pure_Vitamin_C",  # קורא חמצון בשמש
    "Caffeine",        # עירור בוקר
    "sunscreen",       # הגנה דוקרנית
}

PM_ONLY_ACTIVES: Set[str] = {
    "Retinoids",       # יכול לגרום לרגישות בשמש
    "AHA",             # יכול לגרום לרגישות בשמש
    "BHA",             # יכול לגרום לרגישות בשמש
    "PHA",             # יכול לגרום לרגישות בשמש
    "Benzoyl_Peroxide", # יכול לגרום לרגישות בשמש
}


# =============================================================================
# VALIDATION FUNCTIONS - פונקציות בדיקה והתחזוקה
# =============================================================================

def check_pair_conflict(active1: str, active2: str) -> bool:
    """
    בדיקת קונפליקט בין שני רכיבים פעילים.
    
    Args:
        active1: הרכיב הפעיל הראשון
        active2: הרכיב הפעיל השני
        
    Returns:
        True אם קיים קונפליקט בינם
    """
    # בדיקה דו-כיוונית - אם active1 מתנגש עם active2 או להיפך
    return (active1 in INCOMPATIBLE_PAIRS and active2 in INCOMPATIBLE_PAIRS[active1]) or \
           (active2 in INCOMPATIBLE_PAIRS and active1 in INCOMPATIBLE_PAIRS[active2])


def check_product_conflict(product1: Product, product2: Product) -> Optional[str]:
    """
    בדיקת קונפליקט בין שני מוצרים בהתבסס על הרכיבים הפעילים שלהם.
    
    Args:
        product1: המוצר הראשון
        product2: המוצר השני
        
    Returns:
        תיאור הקונפליקט אם קיים, None אחרת
    """
    # חילוץ רכיבים פעילים מ-active_family
    actives1 = set(product1.active_family.split()) if product1.active_family else set()
    actives2 = set(product2.active_family.split()) if product2.active_family else set()
    
    # בדיקת כל הצירופים
    for active1 in actives1:
        for active2 in actives2:
            if check_pair_conflict(active1, active2):
                return f"קונפליקט: {active1} ב-{product1.name} תנגש עם {active2} ב-{product2.name}"
    
    return None


def validate_routine_safety(products: List[Product], time_of_day: str = "ANY") -> List[str]:
    """
    בדיקת בטיחות של שגרה שלמה - זיהוי כל הקונפליקטים.
    
    Args:
        products: רשימת מוצרים בשגרה
        time_of_day: "AM", "PM", או "ANY"
        
    Returns:
        רשימת אזהרות בנוגע לקונפליקטים שנמצאו
    """
    warnings: List[str] = []
    
    # בדיקת קונפליקטים בין כל זוגות המוצרים
    for i in range(len(products)):
        for j in range(i + 1, len(products)):
            conflict = check_product_conflict(products[i], products[j])
            if conflict:
                warnings.append(conflict)
    
    # בדיקת הגבלות זמן
    if time_of_day in ("AM", "ANY"):
        for product in products:
            actives = set(product.active_family.split()) if product.active_family else set()
            pm_only = PM_ONLY_ACTIVES & actives
            if pm_only and product.time_allowed in ("PM", "ANY"):
                warnings.append(
                    f"⚠️ {', '.join(pm_only)} ב-{product.name} עדיף להשתמש בערב בלבד (יכול לגרום לרגישות בשמש)"
                )
    
    # בדיקה כי SPF קיים בשגרת בוקר אם יש אקטיבים
    if time_of_day in ("AM", "ANY"):
        has_actives = any(p.active_family for p in products)
        has_spf = any(p.product_type == "sunscreen" for p in products)
        if has_actives and not has_spf:
            warnings.append("⚠️ אין SPF בשגרה בוקר - חייב SPF כשמשתמשים ב-Actives")
    
    return warnings


def get_product_ordering(products: List[Product]) -> List[Product]:
    """
    סידור מוצרים לפי סדר הלחמת קלאסי וטוב-ביוטי.
    
    Args:
        products: רשימה לא מסודרת של מוצרים
        
    Returns:
        רשימה של מוצרים ממוינת לפי סדר הלחמת נכון
    """
    return sorted(
        products,
        key=lambda p: STEP_ORDER_MAP.get(p.product_type, 999)
    )


def check_timing_compatibility(product: Product, time_of_day: str) -> bool:
    """
    בדיקה אם מוצר מתאים לזמן היום הנתון.
    
    Args:
        product: המוצר לבדיקה
        time_of_day: "AM" או "PM"
        
    Returns:
        True אם המוצר מתאים לזמן זה
    """
    if product.time_allowed == "ANY":
        return True
    
    return product.time_allowed == time_of_day


def get_weekly_frequency_warning(products: List[Product]) -> List[str]:
    """
    בדיקה של משאבה שבועית אם מוצרים עם תדירות מוגבלת משמשים יותר מדי פעמים.
    
    Args:
        products: רשימת מוצרים
        
    Returns:
        רשימת אזהרות אם מוצר משמש יותר מפי הנתון
    """
    warnings: List[str] = []
    
    for product in products:
        if product.max_weekly_frequency < 7:
            warnings.append(
                f"⚠️ {product.name} יש להשתמש רק עד {product.max_weekly_frequency} פעמים בשבוע"
            )
    
    return warnings


def validate_barrier_safety(
    products: List[Product],
    barrier_compromised: bool,
    sensitivity: int
) -> List[str]:
    """
    בדיקת בטיחות חוסם לעור עם חוסם פגום או רגיש.
    
    Args:
        products: רשימת מוצרים בשגרה
        barrier_compromised: האם החוסם פגום
        sensitivity: רמת רגישות (1-5)
        
    Returns:
        רשימת אזהרות בטיחות
    """
    warnings: List[str] = []
    
    # בדיקה עם חוסם פגום
    if barrier_compromised:
        for product in products:
            if not product.is_safe_for_barrier_concerns:
                actives = product.active_family if product.active_family else "בלי רכיבים פעילים"
                warnings.append(
                    f"⚠️ חזור! {product.name} ({actives}) עלול לחמור על חוסם פגום"
                )
    
    # בדיקה עם רגישות גבוהה
    if sensitivity <= 2:
        for product in products:
            if not product.is_safe_for_sensitive:
                warnings.append(
                    f"⚠️ חזור! {product.name} עלול להיות קשה על עור רגיש"
                )
    
    return warnings


def suggest_frequency_adjustments(routine_products: List[Product]) -> Dict[str, int]:
    """
    הצעת תדירויות שימוש אופטימליות לרכיבים פעילים.
    
    Args:
        routine_products: מוצרים בשגרה המוצעת
        
    Returns:
        מילון של מוצר -> תדירות שבועית מוצעת
    """
    suggestions: Dict[str, int] = {}
    
    for product in routine_products:
        if product.active_family:
            # קבלת סקירה של סוג הרכיב
            if any(acid in product.active_family for acid in ["AHA", "BHA", "PHA"]):
                # חומצות ישירות - בדרך כלל 2-3 פעמים בשבוע
                suggestions[product.name] = min(product.max_weekly_frequency, 3)
            elif "Retinoids" in product.active_family:
                # רטינואידים - בדרך כלל 2-3 פעמים בשבוע
                suggestions[product.name] = min(product.max_weekly_frequency, 3)
            elif "Pure_Vitamin_C" in product.active_family:
                # ויטמין C טהור - בדרך כלל 4-5 פעמים בשבוע (בוקר)
                suggestions[product.name] = min(product.max_weekly_frequency, 5)
            elif "Benzoyl_Peroxide" in product.active_family:
                # Benzoyl Peroxide - בדרך כלל 1-2 פעמים בשבוע
                suggestions[product.name] = min(product.max_weekly_frequency, 2)
            else:
                # רכיבים אחרים - בדרך כלל יומיים
                suggestions[product.name] = product.max_weekly_frequency
    
    return suggestions


# =============================================================================
# DEBUG & INFORMATION FUNCTIONS
# =============================================================================

def print_incompatibility_chart() -> None:
    """הדפסת טבלת קונפליקטים לייעוץ."""
    print("\n" + "=" * 70)
    print("טבלת קונפליקטים - שילובים אסורים באותו חלון זמן")
    print("=" * 70)
    
    for active, conflicts in INCOMPATIBLE_PAIRS.items():
        print(f"\n🚫 {active} עלול להתנגש עם:")
        for conflict in sorted(conflicts):
            print(f"   ❌ {conflict}")


def print_routine_order() -> None:
    """הדפסת סדר הלחמת קלאסי."""
    print("\n" + "=" * 70)
    print("סדר הלחמת קלאסי - שכבות (מדקה לעבה)")
    print("=" * 70)
    
    for idx, step in enumerate(ROUTINE_STEP_ORDER, 1):
        print(f"{idx:2d}. {step.upper()}")
