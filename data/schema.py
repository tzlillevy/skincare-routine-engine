"""
Pydantic models for skincare routine engine data structures.
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class SkinTypeEnum(str, Enum):
    OILY = "oily"
    DRY = "dry"
    COMBINATION = "combination"
    NORMAL = "normal"


class TimeOfDayEnum(str, Enum):
    AM = "AM"
    PM = "PM"
    ANY = "ANY"


class ProductTypeEnum(str, Enum):
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
    skin_type: str = Field(..., description="Skin type: oily, dry, combination, or normal")
    concerns: List[str] = Field(..., description="At least one concern required")
    sensitivity_level: int = Field(..., ge=1, le=5, description="Sensitivity level 1-5")
    
    @field_validator("skin_type")
    @classmethod
    def validate_skin_type(cls, skin_type: str) -> str:
        return skin_type
    
    @field_validator("concerns")
    @classmethod
    def validate_concerns(cls, concerns: List[str]) -> List[str]:
        return concerns


class Product(BaseModel):
    model_config = {"extra": "ignore"}  # מתעלם משדות נוספים ומאפשר לטעון את כל המוצרים המלאים בלי שגיאות
    
    id: str
    brand: str
    name: str
    product_type: str
    active_family: Optional[str] = Field(default=None)
    max_weekly_frequency: int = Field(default=7, ge=1, le=7)
    time_allowed: str = Field(default="ANY")
    is_safe_for_barrier_concerns: bool = Field(default=False)
    is_safe_for_sensitive: bool = Field(default=False)


class RoutineStep(BaseModel):
    step_number: int = Field(..., ge=1)
    product: Product
    notes: Optional[str] = Field(default=None)
    frequency: int = Field(default=1, ge=1, le=7)


class RoutineOutput(BaseModel):
    am_routine: List[Product] = Field(default_factory=list)
    pm_routine: List[Product] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    explanations: List[str] = Field(default_factory=list)
    skipped_concerns: List[str] = Field(default_factory=list)
    conflict_analysis: Optional[Dict[str, Any]] = Field(default=None)


# שורה קריטית כדי ש-RoutinePlan יעבוד במנוע החישוב
RoutinePlan = RoutineOutput


class ConflictAnalysis(BaseModel):
    has_conflicts: bool = Field(...)
    conflict_details: List[str] = Field(default_factory=list)
    severity_level: Optional[str] = Field(default=None)
    recommendations: List[str] = Field(default_factory=list)