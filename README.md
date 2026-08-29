# Skincare Routine Conflict Resolver & Recommendation Engine

A comprehensive Python engine for analyzing skincare routines, detecting ingredient conflicts, and generating personalized skincare recommendations based on skin type, concerns, and sensitivity level.

## Project Structure

```
skincare-routine-engine/
├── data/                          # Data layer - concerns, ingredients, and schemas
│   ├── __init__.py               # Package exports
│   ├── concerns.py               # Skin concerns and ingredient mappings
│   └── schema.py                 # Pydantic data models
├── engine/                        # Core business logic
│   └── __init__.py
├── api/                           # FastAPI endpoints
│   └── __init__.py
├── app/                           # Streamlit dashboard
│   └── __init__.py
└── README.md
```

## Data Layer (`data/`)

### `concerns.py`
Contains comprehensive mappings of:
- **Skin Types**: oily, dry, combination, normal
- **15 Skin Concerns**: acne, blackheads, texture, anti_aging, hyperpigmentation, pih_redness, keratosis_pilaris, dehydrated_skin, dark_circles, eye_puffiness, damaged_barrier, redness, eczema, seborrhea, insect_bites
- **Active Ingredients**: 30+ skincare actives with detailed descriptions
- **Concern-Ingredient Mapping**: Recommended ingredients for each concern
- **Safety Flags & Restrictions**: Barrier override flags, inflammatory concerns, ingredient restrictions

#### Key Safety Features:
- **Barrier Concerns**: `damaged_barrier`, `eczema`, `redness` - blocked from harsh acids and strong retinoids
- **Malassezia Concerns**: `seborrhea` - restrictions on heavy oils and lipids
- **Inflammatory Concerns**: Additional restrictions for sensitive conditions
- **Sensitivity Overrides**: Automatic sensitivity level adjustment for barrier-compromised skin

#### Utility Functions:
```python
from data import (
    get_concern_ingredients,
    is_barrier_compromised,
    is_inflammatory,
    get_incompatible_ingredients,
    get_sensitivity_override_for_concerns,
    get_safety_flags_for_concerns,
)
```

### `schema.py`
Pydantic models for data validation:

#### `SkinProfile`
```python
from data import SkinProfile

profile = SkinProfile(
    skin_type="oily",
    concerns=["acne", "blackheads"],
    sensitivity_level=2
)
```

#### `Product`
```python
from data import Product

product = Product(
    id="prod_001",
    brand="Example Brand",
    name="Gentle Cleanser",
    product_type="cleanser",
    active_family="",
    max_weekly_frequency=7,
    time_allowed="ANY",
    is_safe_for_barrier_concerns=True,
    is_safe_for_sensitive=True
)
```

#### `RoutineOutput`
```python
from data import RoutineOutput, Product

routine = RoutineOutput(
    am_routine=[product1, product2],
    pm_routine=[product3, product4],
    warnings=["Limit exfoliants to 2x per week"],
    explanations=["BHA recommended for acne treatment"],
    skipped_concerns=[]
)
```

## Skin Concerns & Recommended Ingredients

### Acne
- Recommended: BHA, Benzoyl Peroxide, Azelaic Acid, Retinoids, Niacinamide
- Blocked (sensitive): All harsh actives

### Damaged Barrier
- Recommended: Ceramides, Panthenol, Centella, Snail Mucin, Fatty Acids
- Blocked: AHA, BHA, PHA, Retinoids, Pure Vitamin C, Physical Scrubs
- **Priority**: Barrier repair

### Eczema
- Recommended: Colloidal Oatmeal, Ceramides, Low-Dose Urea, Panthenol, Centella
- Blocked: Direct Acids, Strong Retinoids, Artificial Fragrances, Drying Alcohols
- **Priority**: Soothing and barrier repair
- **Requirement**: Hypoallergenic formulations

### Hyperpigmentation
- Recommended: Pure Vitamin C, Arbutin, Tranexamic Acid, Niacinamide, Azelaic Acid, AHA

### Seborrhea
- Recommended: Zinc PCA, Azelaic Acid, Mild Antifungals, Niacinamide, BHA
- Blocked: Heavy oils, esters (Malassezia-feeding ingredients)
- **Preference**: Lightweight formulations

## Usage Examples

### Check Barrier Status
```python
from data import is_barrier_compromised, BARRIER_CONCERNS

concerns = ["eczema", "dehydrated_skin"]
if is_barrier_compromised(concerns):
    print("Barrier is compromised - prioritize repair")
```

### Get Safety Restrictions
```python
from data import get_incompatible_ingredients, get_safety_flags_for_concerns

concerns = ["damaged_barrier", "redness"]
sensitivity = 2

incompatible = get_incompatible_ingredients(concerns, sensitivity)
safety_flags = get_safety_flags_for_concerns(concerns)

print(f"Avoid: {incompatible}")
print(f"Safety flags: {safety_flags}")
```

### Get Recommended Ingredients
```python
from data import get_concern_ingredients

acne_ingredients = get_concern_ingredients("acne")
print(f"For acne, consider: {acne_ingredients}")
```

## Sensitivity Levels

1. **Very Sensitive** - Avoid all harsh actives, barrier-focused approach
2. **Sensitive** - Limit strong actives, introduce gradually
3. **Moderately Sensitive** - Moderate active use, monitor closely
4. **Resilient** - Can tolerate most actives at normal concentrations
5. **Very Resilient** - Can use aggressive treatments and high concentrations

## Ingredient Categories

### Direct Acids (Exfoliants)
- AHA (Alpha Hydroxy Acid)
- BHA (Beta Hydroxy Acid)
- PHA (Polyhydroxy Acid)

### Retinoids (Anti-Aging)
- Retinoids
- Gentle Eye Retinol

### Hydrating Actives
- Hyaluronic Acid
- Glycerin
- Panthenol
- Snail Mucin

### Barrier Repair
- Ceramides
- Fatty Acids
- Centella Asiatica

### Anti-Inflammatory
- Niacinamide
- Azelaic Acid
- Allantoin
- Centella Asiatica

### Brightening
- Pure Vitamin C
- Arbutin
- Tranexamic Acid

## Next Steps

- **Engine Module**: Implement constraint solver for routine generation
- **API Module**: Build FastAPI endpoints for routine recommendations
- **App Module**: Create Streamlit dashboard for user interaction
- **Database**: Add product database and user profile storage
- **Testing**: Comprehensive unit and integration tests

## License

(To be determined)
