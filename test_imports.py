#!/usr/bin/env python
"""Quick test to verify all imports work correctly."""

import sys
print(f"Python Version: {sys.version}")
print(f"Python Path: {sys.executable}\n")

# Test imports
try:
    from data import SkinProfile, Product, RoutineOutput, SEED_PRODUCTS
    print("✅ data module imported successfully")
    print(f"   - {len(SEED_PRODUCTS)} products loaded")
except Exception as e:
    print(f"❌ Error importing data: {e}")
    sys.exit(1)

try:
    from engine import (
        check_pair_conflict,
        validate_routine_safety,
        RoutineSolver,
    )
    print("✅ engine module imported successfully")
    print("   - RoutineSolver class ready")
except Exception as e:
    print(f"❌ Error importing engine: {e}")
    sys.exit(1)

# Test RoutineSolver instantiation
try:
    solver = RoutineSolver()
    print("✅ RoutineSolver instantiated successfully\n")
except Exception as e:
    print(f"❌ Error creating RoutineSolver: {e}")
    sys.exit(1)

# Test with a simple profile
try:
    profile = SkinProfile(
        skin_type="oily",
        concerns=["acne"],
        sensitivity_level=3
    )
    print(f"✅ Test profile created: {profile.skin_type}, {profile.concerns}\n")
    
    # Try to solve
    print("🔄 Running solver.solve() on test profile...")
    routine = solver.solve(profile)
    
    print(f"✅ Solver executed successfully!")
    print(f"   - AM routine: {len(routine.am_routine)} products")
    print(f"   - PM routine: {len(routine.pm_routine)} products")
    print(f"   - Warnings: {len(routine.warnings)}")
    print(f"   - Explanations: {len(routine.explanations)}")
    
except Exception as e:
    print(f"❌ Error during solve: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("🎉 All tests passed! System is ready to use.")
print("="*60)
