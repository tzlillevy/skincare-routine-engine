"""
Pydantic models for skincare routine engine data structures.

Defines the core data models for skin profiles, products, and routine outputs
with comprehensive validation and type hints.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class SkinTypeEnum(str, Enum):
    """Valid skin types."""
    OILY = "oily"
    DRY = "dry"
    COMBINATION = "combination"
    NORMAL = "normal"


class TimeOfDayEnum(str, Enum):
    """Valid times of day for product application."""
    AM = "AM"
    PM = "PM"
    ANY = "ANY"


class ProductTypeEnum(str, Enum):
    """Product categories in a skincare routine."""
    CLEANSER = "cleanser"
    EXFOLIANT = "exfoliant"
    TONER = "toner"
    ESSENCE = "essence"
    SERUM = "serum"
    AMPOULE = "ampoule"
    SHEET_MASK = "sheet_mask"
    MOISTURIZER = "moisturizer"
    SUNSCREEN = "sunscreen"
    OIL = "oil"
    TREATMENT = "treatment"


class SkinProfile(BaseModel):
    """
    Represents a user's skin profile with type, concerns, and sensitivity.
    
    Attributes:
        skin_type: Primary skin type classification (oily, dry, combination, normal)
        concerns: List of skin concerns to address (e.g., acne, blackheads, anti_aging)
        sensitivity_level: Scale from 1 (very sensitive) to 5 (very resilient)
    
    Example:
        >>> profile = SkinProfile(
        ...     skin_type="oily",
        ...     concerns=["acne", "blackheads"],
        ...     sensitivity_level=2
        ... )
    """
    skin_type: str = Field(..., description="Skin type: oily, dry, combination, or normal")
    concerns: List[str] = Field(..., min_items=1, description="At least one concern required")
    sensitivity_level: int = Field(..., ge=1, le=5, description="Sensitivity level 1-5")
    
    @field_validator("skin_type")
    @classmethod
    def validate_skin_type(cls, skin_type: str) -> str:
        """Validate that skin type is recognized."""
        valid_types = {"oily", "dry", "combination", "normal"}
        if skin_type not in valid_types:
            raise ValueError(f"Unknown skin type: {skin_type}. Must be one of: {valid_types}")
        return skin_type
    
    @field_validator("concerns")
    @classmethod
    def validate_concerns(cls, concerns: List[str]) -> List[str]:
        """Validate that all concerns are known."""
        valid_concerns = {
            "acne", "blackheads", "texture", "anti_aging", "hyperpigmentation",
            "pie_redness", "pih_redness", "keratosis_pilaris", "dehydrated_skin", "dark_circles",
            "eye_puffiness", "damaged_barrier", "redness", "eczema", "seborrhea",
            "insect_bites"
        }
        for concern in concerns:
            if concern not in valid_concerns:
                raise ValueError(f"Unknown concern: {concern}. Must be one of: {valid_concerns}")
        return concerns


class Product(BaseModel):
    """
    Represents a skincare product with its properties and compatibility info.
    
    Attributes:
        id: Unique product identifier
        brand: Product brand name
        name: Product name/description
        product_type: Category of product (cleanser, serum, moisturizer, etc.)
        active_family: Primary active ingredient(s) - space-separated string
        max_weekly_frequency: Maximum times per week the product can be used (1-7)
        time_allowed: When product can be used (AM, PM, or ANY)
        is_safe_for_barrier_concerns: Whether safe for damaged_barrier/eczema
        is_safe_for_sensitive: Whether suitable for sensitive skin (level 1-2)
    
    Example:
        >>> product = Product(
        ...     id="prod_001",
        ...     brand="Example Brand",
        ...     name="Gentle Cleanser",
        ...     product_type="cleanser",
        ...     active_family="",
        ...     max_weekly_frequency=7,
        ...     time_allowed="ANY",
        ...     is_safe_for_barrier_concerns=True,
        ...     is_safe_for_sensitive=True
        ... )
    """
    id: str = Field(..., description="Unique product identifier")
    brand: str = Field(..., description="Product brand name")
    name: str = Field(..., description="Product name/description")
    product_type: str = Field(..., description="Product category")
    active_family: str = Field(
        default="",
        description="Primary active ingredient(s) as space-separated string"
    )
    max_weekly_frequency: int = Field(
        default=7,
        ge=1,
        le=7,
        description="Maximum times per week the product can be used"
    )
    time_allowed: str = Field(
        default="ANY",
        description="When product can be used (AM, PM, or ANY)"
    )
    is_safe_for_barrier_concerns: bool = Field(
        default=False,
        description="Safe for damaged_barrier, eczema, or redness concerns"
    )
    is_safe_for_sensitive: bool = Field(
        default=False,
        description="Suitable for sensitive skin (sensitivity level 1-2)"
    )
    
    @field_validator("time_allowed")
    @classmethod
    def validate_time_allowed(cls, time_allowed: str) -> str:
        """Validate time_allowed is AM, PM, or ANY."""
        valid_times = {"AM", "PM", "ANY"}
        if time_allowed not in valid_times:
            raise ValueError(f"time_allowed must be one of: {valid_times}")
        return time_allowed


class RoutineStep(BaseModel):
    """
    Represents a single step in a skincare routine.
    
    Attributes:
        step_number: Order in routine (1, 2, 3, etc.)
        product: The Product object for this step
        notes: Usage notes or instructions
        frequency: Times per week this product is used in routine
    """
    step_number: int = Field(..., ge=1, description="Step order in routine")
    product: Product
    notes: Optional[str] = Field(default=None, description="Usage notes or instructions")
    frequency: int = Field(default=1, ge=1, le=7, description="Times per week used")


class RoutineOutput(BaseModel):
    """
    Represents a complete skincare routine recommendation.
    
    Attributes:
        am_routine: List of Product objects for morning routine
        pm_routine: List of Product objects for evening routine
        warnings: Any compatibility or usage warnings
        explanations: Explanation of recommendations
        skipped_concerns: Concerns that couldn't be addressed
        conflict_analysis: Detailed analysis of ingredient conflicts (if any)
    
    Example:
        >>> routine = RoutineOutput(
        ...     am_routine=[...],  # List[Product]
        ...     pm_routine=[...],  # List[Product]
        ...     warnings=["Limit exfoliants to 2x per week"],
        ...     explanations=["BHA recommended for acne"],
        ...     skipped_concerns=[]
        ... )
    """
    am_routine: List[Product] = Field(
        default_factory=list,
        description="List of products for morning routine (in order)"
    )
    pm_routine: List[Product] = Field(
        default_factory=list,
        description="List of products for evening routine (in order)"
    )
    warnings: List[str] = Field(
        default_factory=list,
        description="Compatibility warnings and safety notices"
    )
    explanations: List[str] = Field(
        default_factory=list,
        description="Explanations of why products were recommended"
    )
    skipped_concerns: List[str] = Field(
        default_factory=list,
        description="Concerns that couldn't be adequately addressed"
    )
    conflict_analysis: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Detailed analysis of ingredient interactions"
    )


class ConflictAnalysis(BaseModel):
    """
    Detailed analysis of ingredient conflicts in a routine.
    
    Attributes:
        has_conflicts: Whether conflicts were detected
        conflict_details: Description of each conflict
        severity_level: HIGH, MEDIUM, or LOW
        recommendations: Suggestions to resolve conflicts
    """
    has_conflicts: bool = Field(..., description="Whether conflicts were detected")
    conflict_details: List[str] = Field(
        default_factory=list,
        description="Detailed description of each conflict"
    )
    severity_level: Optional[str] = Field(
        default=None,
        description="Conflict severity: HIGH, MEDIUM, or LOW"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Suggestions to resolve conflicts"
    )
