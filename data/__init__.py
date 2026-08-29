"""Data module for skincare routine engine.

Contains all data structures, mappings, utilities, and seed products for managing
skin profiles, products, concerns, active ingredients, and safety flags.
"""

# Import constants
from .concerns import (
    SKIN_TYPES,
    SKIN_CONCERNS,
    ACTIVE_INGREDIENTS,
    CONCERN_INGREDIENTS_MAP,
    BARRIER_CONCERNS,
    INFLAMMATORY_CONCERNS,
    DIRECT_ACIDS,
    STRONG_RETINOIDS,
    HARSH_INGREDIENTS,
    MALASSEZIA_FEEDING_INGREDIENTS,
    PHYSICAL_EXFOLIANTS,
    CONCERN_SAFETY_FLAGS,
    SENSITIVITY_LEVELS,
)

# Import utility functions
from .concerns import (
    get_concern_ingredients,
    is_barrier_compromised,
    is_inflammatory,
    get_blocked_ingredients_for_concern,
    get_incompatible_ingredients,
    get_sensitivity_override_for_concerns,
    get_safety_flags_for_concerns,
)

# Import Pydantic models
from .schema import (
    SkinProfile,
    Product,
    RoutineStep,
    RoutineOutput,
    ConflictAnalysis,
    SkinTypeEnum,
    TimeOfDayEnum,
    ProductTypeEnum,
)

# Import seed products and utilities
from .products import (
    SEED_PRODUCTS,
    get_products_by_type,
    get_products_by_active,
    get_safe_for_barrier,
    get_safe_for_sensitive,
)

__all__ = [
    # Constants
    "SKIN_TYPES",
    "SKIN_CONCERNS",
    "ACTIVE_INGREDIENTS",
    "CONCERN_INGREDIENTS_MAP",
    "BARRIER_CONCERNS",
    "INFLAMMATORY_CONCERNS",
    "DIRECT_ACIDS",
    "STRONG_RETINOIDS",
    "HARSH_INGREDIENTS",
    "MALASSEZIA_FEEDING_INGREDIENTS",
    "PHYSICAL_EXFOLIANTS",
    "CONCERN_SAFETY_FLAGS",
    "SENSITIVITY_LEVELS",
    # Utility functions
    "get_concern_ingredients",
    "is_barrier_compromised",
    "is_inflammatory",
    "get_blocked_ingredients_for_concern",
    "get_incompatible_ingredients",
    "get_sensitivity_override_for_concerns",
    "get_safety_flags_for_concerns",
    # Pydantic models
    "SkinProfile",
    "Product",
    "RoutineStep",
    "RoutineOutput",
    "ConflictAnalysis",
    "SkinTypeEnum",
    "TimeOfDayEnum",
    "ProductTypeEnum",
    # Seed products
    "SEED_PRODUCTS",
    "get_products_by_type",
    "get_products_by_active",
    "get_safe_for_barrier",
    "get_safe_for_sensitive",
]

