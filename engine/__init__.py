"""Engine module for skincare routine conflict resolution and recommendations.

Contains rule-based logic for detecting ingredient conflicts, validating routines,
and a constraint satisfaction solver for generating optimized skincare routines.
"""

from .rules import (
    INCOMPATIBLE_PAIRS,
    ROUTINE_STEP_ORDER,
    STEP_ORDER_MAP,
    AM_ONLY_PRODUCTS,
    PM_ONLY_ACTIVES,
    check_pair_conflict,
    check_product_conflict,
    validate_routine_safety,
    get_product_ordering,
    check_timing_compatibility,
    get_weekly_frequency_warning,
    validate_barrier_safety,
    suggest_frequency_adjustments,
    print_incompatibility_chart,
    print_routine_order,
)

from .solver import RoutineSolver

__all__ = [
    # Constants
    "INCOMPATIBLE_PAIRS",
    "ROUTINE_STEP_ORDER",
    "STEP_ORDER_MAP",
    "AM_ONLY_PRODUCTS",
    "PM_ONLY_ACTIVES",
    # Functions
    "check_pair_conflict",
    "check_product_conflict",
    "validate_routine_safety",
    "get_product_ordering",
    "check_timing_compatibility",
    "get_weekly_frequency_warning",
    "validate_barrier_safety",
    "suggest_frequency_adjustments",
    "print_incompatibility_chart",
    "print_routine_order",
    # Solver class
    "RoutineSolver",
]

