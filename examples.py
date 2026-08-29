"""
Example usage and testing of the skincare routine engine data module.

This script demonstrates how to use the data structures and utility functions.
"""

# Example 1: Creating a skin profile
from data import SkinProfile

profile = SkinProfile(
    skin_type="oily",
    concerns=["acne", "blackheads"],
    sensitivity_level=2
)

print("=" * 70)
print("EXAMPLE 1: Skin Profile")
print("=" * 70)
print(f"Profile: {profile.model_dump_json(indent=2)}\n")


# Example 2: Creating a product
from data import Product

cleanser = Product(
    id="prod_001",
    brand="CeraVe",
    name="Foaming Cleanser",
    product_type="cleanser",
    active_family="",
    max_weekly_frequency=7,
    time_allowed="ANY",
    is_safe_for_barrier_concerns=False,
    is_safe_for_sensitive=True
)

bha_treatment = Product(
    id="prod_002",
    brand="Paula's Choice",
    name="2% BHA Liquid Exfoliant",
    product_type="exfoliant",
    active_family="BHA",
    max_weekly_frequency=3,
    time_allowed="PM",
    is_safe_for_barrier_concerns=False,
    is_safe_for_sensitive=False
)

print("=" * 70)
print("EXAMPLE 2: Products")
print("=" * 70)
print(f"Cleanser: {cleanser.model_dump_json(indent=2)}\n")
print(f"BHA Treatment: {bha_treatment.model_dump_json(indent=2)}\n")


# Example 3: Checking concern ingredients
from data import get_concern_ingredients

print("=" * 70)
print("EXAMPLE 3: Recommended Ingredients by Concern")
print("=" * 70)
for concern in ["acne", "damaged_barrier", "hyperpigmentation"]:
    ingredients = get_concern_ingredients(concern)
    print(f"{concern}: {ingredients}\n")


# Example 4: Checking barrier and inflammatory status
from data import is_barrier_compromised, is_inflammatory

print("=" * 70)
print("EXAMPLE 4: Barrier and Inflammatory Status")
print("=" * 70)

normal_concerns = ["acne", "blackheads"]
barrier_concerns = ["damaged_barrier", "redness"]
eczema_concerns = ["eczema"]

print(f"Concerns: {normal_concerns}")
print(f"  Barrier compromised: {is_barrier_compromised(normal_concerns)}")
print(f"  Inflammatory: {is_inflammatory(normal_concerns)}\n")

print(f"Concerns: {barrier_concerns}")
print(f"  Barrier compromised: {is_barrier_compromised(barrier_concerns)}")
print(f"  Inflammatory: {is_inflammatory(barrier_concerns)}\n")

print(f"Concerns: {eczema_concerns}")
print(f"  Barrier compromised: {is_barrier_compromised(eczema_concerns)}")
print(f"  Inflammatory: {is_inflammatory(eczema_concerns)}\n")


# Example 5: Getting incompatible ingredients
from data import get_incompatible_ingredients

print("=" * 70)
print("EXAMPLE 5: Incompatible Ingredients")
print("=" * 70)

test_cases = [
    (["acne", "blackheads"], 3, "Acne profile, moderately sensitive"),
    (["damaged_barrier"], 4, "Barrier concern, resilient"),
    (["eczema", "redness"], 1, "Eczema, very sensitive"),
    (["seborrhea"], 3, "Seborrhea, moderately sensitive"),
]

for concerns, sensitivity, description in test_cases:
    incompatible = get_incompatible_ingredients(concerns, sensitivity)
    print(f"{description}")
    print(f"  Concerns: {concerns}, Sensitivity: {sensitivity}")
    print(f"  Avoid: {incompatible}\n")


# Example 6: Getting sensitivity overrides
from data import get_sensitivity_override_for_concerns

print("=" * 70)
print("EXAMPLE 6: Sensitivity Overrides")
print("=" * 70)

test_overrides = [
    ["acne"],
    ["damaged_barrier"],
    ["eczema"],
    ["damaged_barrier", "redness"],
]

for concerns in test_overrides:
    override = get_sensitivity_override_for_concerns(concerns)
    print(f"Concerns: {concerns}")
    print(f"  Sensitivity override: {override}\n")


# Example 7: Getting safety flags
from data import get_safety_flags_for_concerns

print("=" * 70)
print("EXAMPLE 7: Safety Flags")
print("=" * 70)

test_flags = [
    ["acne"],
    ["damaged_barrier"],
    ["eczema", "redness"],
    ["seborrhea"],
]

for concerns in test_flags:
    flags = get_safety_flags_for_concerns(concerns)
    print(f"Concerns: {concerns}")
    for key, value in flags.items():
        if value:  # Only show True flags
            print(f"  {key}: {value}")
    print()


# Example 8: Creating a routine output
from data import RoutineOutput

routine = RoutineOutput(
    am_routine=[cleanser],
    pm_routine=[cleanser, bha_treatment],
    warnings=[
        "Limit BHA to 2-3x per week",
        "Use SPF 30+ during the day when using BHA"
    ],
    explanations=[
        "BHA recommended for acne and blackheads",
        "Gentle cleanser safe for daily use",
        "Morning routine focuses on gentle cleansing"
    ],
    skipped_concerns=[],
    conflict_analysis=None
)

print("=" * 70)
print("EXAMPLE 8: Routine Output")
print("=" * 70)
print(f"Morning routine: {len(routine.am_routine)} products")
print(f"Evening routine: {len(routine.pm_routine)} products")
print(f"Warnings: {routine.warnings}")
print(f"Explanations: {routine.explanations}\n")


# Example 9: Accessing concern data
from data import SKIN_CONCERNS, CONCERN_INGREDIENTS_MAP, CONCERN_SAFETY_FLAGS

print("=" * 70)
print("EXAMPLE 9: Direct Data Access")
print("=" * 70)
print(f"Total skin concerns: {len(SKIN_CONCERNS)}")
print(f"Total ingredients in map: {len(CONCERN_INGREDIENTS_MAP)}\n")

print("Damaged Barrier Concern:")
safety_flags = CONCERN_SAFETY_FLAGS.get("damaged_barrier", {})
print(f"  Description: {safety_flags.get('description')}")
print(f"  Blocked ingredients: {safety_flags.get('blocked_ingredients')}")
print(f"  Priority repair: {safety_flags.get('priority_repair')}\n")

print("Seborrhea Concern:")
safety_flags = CONCERN_SAFETY_FLAGS.get("seborrhea", {})
print(f"  Description: {safety_flags.get('description')}")
print(f"  Prefer lightweight: {safety_flags.get('prefer_lightweight')}\n")

print("=" * 70)
print("All examples completed successfully!")
print("=" * 70)
