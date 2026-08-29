"""
דוגמאות לשימוש בחוקי ההתנגשויות והמוצרים החדשים.

Examples for using the new conflict detection rules and product database.
"""

from data import SEED_PRODUCTS, SkinProfile, Product
from engine import (
    check_pair_conflict,
    check_product_conflict,
    validate_routine_safety,
    validate_barrier_safety,
    get_product_ordering,
    suggest_frequency_adjustments,
    INCOMPATIBLE_PAIRS,
    ROUTINE_STEP_ORDER,
    RoutineSolver,
)


print("\n" + "="*80)
print("דוגמה 1: בדיקת קונפליקט בין שני רכיבים פעילים")
print("Example 1: Checking conflict between two active ingredients")
print("="*80)

# בדיקה אם Retinoids ו-BHA בקונפליקט
conflict = check_pair_conflict("Retinoids", "BHA")
print(f"\nהאם Retinoids + BHA בקונפליקט? {conflict}")
print(f"Is Retinoids + BHA in conflict? {conflict}")

conflict2 = check_pair_conflict("Niacinamide", "Panthenol")
print(f"\nהאם Niacinamide + Panthenol בקונפליקט? {conflict2}")
print(f"Is Niacinamide + Panthenol in conflict? {conflict2}")


print("\n" + "="*80)
print("דוגמה 2: בדיקת קונפליקט בין שני מוצרים")
print("Example 2: Checking conflict between two products")
print("="*80)

# חילוץ מוצרים מקובץ הבסיס
retinol = [p for p in SEED_PRODUCTS if "Retinol" in p.name][0]
bha = [p for p in SEED_PRODUCTS if "BHA" in p.name][0]

print(f"\nמוצר 1: {retinol.brand} - {retinol.name}")
print(f"Product 1: {retinol.brand} - {retinol.name}")
print(f"רכיבים פעילים: {retinol.active_family}")
print(f"Active ingredients: {retinol.active_family}")

print(f"\nמוצר 2: {bha.brand} - {bha.name}")
print(f"Product 2: {bha.brand} - {bha.name}")
print(f"רכיבים פעילים: {bha.active_family}")
print(f"Active ingredients: {bha.active_family}")

conflict_msg = check_product_conflict(retinol, bha)
if conflict_msg:
    print(f"\n⚠️ קונפליקט זוהה: {conflict_msg}")
    print(f"⚠️ Conflict detected: {conflict_msg}")
else:
    print("\n✅ אין קונפליקט בין המוצרים")
    print("✅ No conflict between products")


print("\n" + "="*80)
print("דוגמה 3: בדיקת בטיחות שגרה שלמה")
print("Example 3: Validating complete routine safety")
print("="*80)

# יצירת שגרה PM (ערב)
routine_pm = [
    [p for p in SEED_PRODUCTS if p.id == "prod_003"][0],  # Cleanser
    [p for p in SEED_PRODUCTS if p.id == "prod_021"][0],  # Hydrating serum
    [p for p in SEED_PRODUCTS if p.id == "prod_014"][0],  # Retinol 1%
    [p for p in SEED_PRODUCTS if p.id == "prod_027"][0],  # Moisturizer PM
]

print(f"\n🌙 שגרת ערב (PM Routine):")
print(f"🌙 Evening routine:")
for i, product in enumerate(routine_pm, 1):
    print(f"\n{i}. {product.brand} - {product.name}")
    print(f"   Type: {product.product_type}")
    print(f"   Active: {product.active_family if product.active_family else 'No actives'}")

warnings = validate_routine_safety(routine_pm, "PM")

if warnings:
    print(f"\n⚠️ אזהרות שנמצאו ({len(warnings)}):")
    print(f"⚠️ Warnings found ({len(warnings)}):")
    for warning in warnings:
        print(f"   {warning}")
else:
    print("\n✅ השגרה בטוחה! אין קונפליקטים")
    print("✅ Routine is safe! No conflicts detected")


print("\n" + "="*80)
print("דוגמה 4: בדיקת בטיחות לעור עם חוסם פגום")
print("Example 4: Validating routine for compromised barrier skin")
print("="*80)

# שגרה עם actives חזקים
routine_with_actives = [
    [p for p in SEED_PRODUCTS if p.id == "prod_001"][0],  # Gentle cleanser
    [p for p in SEED_PRODUCTS if p.id == "prod_009"][0],  # BHA
    [p for p in SEED_PRODUCTS if p.id == "prod_026"][0],  # Moisturizer
]

print(f"\n🚨 שגרה עם actives חזקים בחוסם פגום:")
print(f"🚨 Strong actives routine with compromised barrier:")

barrier_warnings = validate_barrier_safety(
    routine_with_actives,
    barrier_compromised=True,
    sensitivity=1
)

if barrier_warnings:
    print(f"\n❌ בעיות בטיחות ({len(barrier_warnings)}):")
    print(f"❌ Safety issues ({len(barrier_warnings)}):")
    for warning in barrier_warnings:
        print(f"   {warning}")
else:
    print("\n✅ בטוח לחוסם פגום")
    print("✅ Safe for compromised barrier")


print("\n" + "="*80)
print("דוגמה 5: סדר מוצרים קלאסי")
print("Example 5: Classic product ordering")
print("="*80)

# שגרה בחוסר סדר
unsorted_routine = [
    [p for p in SEED_PRODUCTS if p.id == "prod_030"][0],  # Sunscreen
    [p for p in SEED_PRODUCTS if p.id == "prod_001"][0],  # Cleanser
    [p for p in SEED_PRODUCTS if p.id == "prod_018"][0],  # Niacinamide
    [p for p in SEED_PRODUCTS if p.id == "prod_026"][0],  # Moisturizer
    [p for p in SEED_PRODUCTS if p.id == "prod_006"][0],  # Essence
]

print(f"\n❌ סדר שגוי (Wrong order):")
for i, product in enumerate(unsorted_routine, 1):
    print(f"{i}. {product.product_type} - {product.name}")

sorted_routine = get_product_ordering(unsorted_routine)

print(f"\n✅ סדר נכון (Correct order):")
for i, product in enumerate(sorted_routine, 1):
    print(f"{i}. {product.product_type} - {product.name}")


print("\n" + "="*80)
print("דוגמה 6: הצעות לתדירות שימוש")
print("Example 6: Suggested usage frequencies")
print("="*80)

routine_with_freq = [
    [p for p in SEED_PRODUCTS if p.id == "prod_008"][0],  # AHA
    [p for p in SEED_PRODUCTS if p.id == "prod_009"][0],  # BHA
    [p for p in SEED_PRODUCTS if p.id == "prod_016"][0],  # Pure Vitamin C
    [p for p in SEED_PRODUCTS if p.id == "prod_013"][0],  # Retinol 0.5%
]

print(f"\nמוצרים עם actives חזקים (Strong actives):")

suggestions = suggest_frequency_adjustments(routine_with_freq)

for product_name, frequency in suggestions.items():
    print(f"\n{product_name}")
    print(f"   Suggested: {frequency}x per week")
    print(f"   הצעה: {frequency} פעמים בשבוע")


print("\n" + "="*80)
print("דוגמה 7: סדר שלבי מריחה קלאסי")
print("Example 7: Classic layering sequence")
print("="*80)

print(f"\n📋 סדר הלחמה מומלץ (הכי דק לעבה):")
print(f"📋 Recommended layering sequence (thinnest to thickest):\n")

for i, step_type in enumerate(ROUTINE_STEP_ORDER, 1):
    print(f"{i:2d}. {step_type.upper()}")


print("\n" + "="*80)
print("דוגמה 8: טבלת קונפליקטים")
print("Example 8: Conflict compatibility matrix")
print("="*80)

print(f"\n🚫 רכיבים פעילים שאסור לשים ביחד:")
print(f"🚫 Incompatible active ingredients:\n")

for active, conflicts in list(INCOMPATIBLE_PAIRS.items())[:3]:
    print(f"{active} ❌ cannot mix with:")
    for conflict in sorted(conflicts):
        print(f"   • {conflict}")
    print()


print("\n" + "="*80)
print("דוגמה 9: בניית שגרה בטוחה - מ-scratch")
print("Example 9: Building a safe routine from scratch")
print("="*80)

# בואו נבנה שגרה בטוחה לעור acne-prone (נוטה לאקנה)

from data import get_products_by_type, get_products_by_active

print(f"\n👤 פרופיל עור:")
print(f"👤 Skin Profile:")
profile = SkinProfile(
    skin_type="oily",
    concerns=["acne", "blackheads"],
    sensitivity_level=3
)
print(f"Skin type: {profile.skin_type}")
print(f"Concerns: {', '.join(profile.concerns)}")
print(f"Sensitivity: {profile.sensitivity_level}/5")

# בחירת מוצרים מתאימים
cleanser = [p for p in SEED_PRODUCTS if p.id == "prod_002"][0]
bha = [p for p in SEED_PRODUCTS if p.id == "prod_012"][0]
niacinamide = [p for p in SEED_PRODUCTS if p.id == "prod_018"][0]
moisturizer = [p for p in SEED_PRODUCTS if p.id == "prod_026"][0]
sunscreen = [p for p in SEED_PRODUCTS if p.id == "prod_030"][0]

suggested_routine = [cleanser, bha, niacinamide, moisturizer, sunscreen]

print(f"\n🌞 שגרה בוקר מוצעת (AM Routine):")
print(f"🌞 Suggested AM Routine:\n")

for i, product in enumerate(suggested_routine, 1):
    print(f"{i}. {product.brand} - {product.name}")
    print(f"   Type: {product.product_type}")
    print(f"   Active: {product.active_family if product.active_family else 'None'}")
    print(f"   Frequency: {product.max_weekly_frequency}x/week")
    print(f"   Barrier safe: {'Yes ✅' if product.is_safe_for_barrier_concerns else 'No ❌'}")
    print()

# בדיקת בטיחות
warnings = validate_routine_safety(suggested_routine, "AM")
print(f"\n✅ בדיקת בטיחות:")
print(f"✅ Safety check:")
if warnings:
    for warning in warnings:
        print(f"   ⚠️ {warning}")
else:
    print(f"   ✅ שגרה בטוחה ללא קונפליקטים!")
    print(f"   ✅ Safe routine with no conflicts!")


print("\n" + "="*80)
print("דוגמה 10: RoutineSolver - דוגמה 1 - עור שמן עם אקנה (sensitivity 3)")
print("Example 10: RoutineSolver - Example 1 - Oily skin with acne (sensitivity 3)")
print("="*80)

# יצירת פרופיל עור שמן עם אקנה וראשים שחורים
profile_acne = SkinProfile(
    skin_type="oily",
    concerns=["acne", "blackheads"],
    sensitivity_level=3,
)

print(f"\n👤 פרופיל העור:")
print(f"👤 Skin Profile:")
print(f"  Skin Type: {profile_acne.skin_type} (שמן)")
print(f"  Concerns: {', '.join(profile_acne.concerns)}")
print(f"  Sensitivity: {profile_acne.sensitivity_level}/5 (מתונה)")
print(f"  Sensitivity: {profile_acne.sensitivity_level}/5 (moderate)")

# הרצת RoutineSolver
solver = RoutineSolver()
routine_acne = solver.solve(profile_acne)

print(f"\n🌞 שגרת בוקר (AM Routine):")
print(f"🌞 Morning Routine ({len(routine_acne.am_routine)} products):")
for i, product in enumerate(routine_acne.am_routine, 1):
    print(f"\n  {i}. {product.brand} - {product.name}")
    print(f"     Type: {product.product_type}")
    print(f"     Active: {product.active_family if product.active_family else 'None'}")
    print(f"     Safe for barrier: {'✅' if product.is_safe_for_barrier_concerns else '❌'}")
    print(f"     Safe for sensitive: {'✅' if product.is_safe_for_sensitive else '❌'}")

print(f"\n🌙 שגרת ערב (PM Routine):")
print(f"🌙 Evening Routine ({len(routine_acne.pm_routine)} products):")
for i, product in enumerate(routine_acne.pm_routine, 1):
    print(f"\n  {i}. {product.brand} - {product.name}")
    print(f"     Type: {product.product_type}")
    print(f"     Active: {product.active_family if product.active_family else 'None'}")
    print(f"     Frequency: {product.max_weekly_frequency}x/week")

print(f"\n📋 הסברים:")
print(f"📋 Explanations:")
for explanation in routine_acne.explanations[:3]:  # Show first 3
    print(f"  {explanation}")

print(f"\n⚠️ אזהרות ({len(routine_acne.warnings)}):")
print(f"⚠️ Warnings ({len(routine_acne.warnings)}):")
for warning in routine_acne.warnings[:3]:  # Show first 3
    print(f"  {warning}")

print(f"\n✅ בעיות מכוסות: {len(profile_acne.concerns)}/2")
print(f"❌ בעיות שלא הצליחו: {len(routine_acne.skipped_concerns)}")


print("\n" + "="*80)
print("דוגמה 11: RoutineSolver - דוגמה 2 - עור רגיש עם מחסום פגום (sensitivity 1)")
print("Example 11: RoutineSolver - Example 2 - Sensitive skin with damaged barrier (sensitivity 1)")
print("="*80)

# יצירת פרופיל עור רגיש עם מחסום פגום
profile_barrier = SkinProfile(
    skin_type="combination",
    concerns=["damaged_barrier", "redness"],
    sensitivity_level=1,
)

print(f"\n👤 פרופיל העור:")
print(f"👤 Skin Profile:")
print(f"  Skin Type: {profile_barrier.skin_type} (combined)")
print(f"  Concerns: {', '.join(profile_barrier.concerns)}")
print(f"  Sensitivity: {profile_barrier.sensitivity_level}/5 (רגיש מאד)")
print(f"  Sensitivity: {profile_barrier.sensitivity_level}/5 (very sensitive)")

# הרצת RoutineSolver
solver_barrier = RoutineSolver()
routine_barrier = solver_barrier.solve(profile_barrier)

print(f"\n🌞 שגרת בוקר (AM Routine):")
print(f"🌞 Morning Routine ({len(routine_barrier.am_routine)} products):")
for i, product in enumerate(routine_barrier.am_routine, 1):
    print(f"\n  {i}. {product.brand} - {product.name}")
    print(f"     Type: {product.product_type}")
    print(f"     Active: {product.active_family if product.active_family else 'No actives (safe!)'}")
    print(f"     Safe for barrier: {'✅ YES' if product.is_safe_for_barrier_concerns else '❌ NO'}")
    print(f"     Safe for sensitive: {'✅ YES' if product.is_safe_for_sensitive else '❌ NO'}")

print(f"\n🌙 שגרת ערב (PM Routine):")
print(f"🌙 Evening Routine ({len(routine_barrier.pm_routine)} products):")
for i, product in enumerate(routine_barrier.pm_routine, 1):
    print(f"\n  {i}. {product.brand} - {product.name}")
    print(f"     Type: {product.product_type}")
    print(f"     Active: {product.active_family if product.active_family else 'No actives (safe!)'}")
    print(f"     Barrier-safe: {'✅ YES' if product.is_safe_for_barrier_concerns else '❌ NO'}")

print(f"\n📋 הסברים:")
print(f"📋 Explanations:")
for explanation in routine_barrier.explanations:
    print(f"  {explanation}")

print(f"\n⚠️ אזהרות ({len(routine_barrier.warnings)}):")
print(f"⚠️ Warnings ({len(routine_barrier.warnings)}):")
for warning in routine_barrier.warnings:
    print(f"  {warning}")

# Verify that harsh actives are blocked
harsh_actives = ["AHA", "BHA", "Retinoids", "Pure_Vitamin_C"]
actives_in_routine = []
for product in routine_barrier.am_routine + routine_barrier.pm_routine:
    if product.active_family:
        for active in product.active_family.split():
            if any(harsh in active for harsh in harsh_actives):
                actives_in_routine.append(active)

if actives_in_routine:
    print(f"\n❌ שגיאה! נמצאו actives חזקים: {actives_in_routine}")
    print(f"❌ ERROR! Found harsh actives: {actives_in_routine}")
else:
    print(f"\n✅ מעולה! אין חומצות או רטינול - מחסום מוגן!")
    print(f"✅ Perfect! No acids or retinol - barrier protected!")

print(f"\n✅ בעיות מכוסות: {len(profile_barrier.concerns)}/2")
print(f"❌ בעיות שלא הצליחו: {len(routine_barrier.skipped_concerns)}")


print("\n" + "="*80)
print("🎉 כל הדוגמאות הושלמו בהצלחה!")
print("🎉 All examples completed successfully!")
print("="*80 + "\n")
