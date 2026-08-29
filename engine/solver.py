"""
RoutineSolver - אלגוריתם בחירה וניקוד מותאם אישית לשגרות טיפוח.
"""
from typing import List, Dict, Optional
from data.schema import SkinProfile, Product
from data.schema import RoutineOutput as RoutinePlan
from data.products import SEED_PRODUCTS
from data.concerns import get_concern_ingredients
from .rules import check_product_conflict

class RoutineSolver:
    def __init__(self, products: Optional[List[Product]] = None):
        self.products = products or SEED_PRODUCTS
        self.profile: Optional[SkinProfile] = None
        self.target_ingredients: List[str] = []
        self.warnings: List[str] = []
        self.explanations: List[str] = []

    def solve(self, profile: SkinProfile) -> RoutinePlan:
        self.profile = profile
        self.target_ingredients = []
        self.warnings = []
        self.explanations = []

        # 1. איסוף רכיבים מומלצים
        for concern in profile.concerns:
            try:
                ingr = get_concern_ingredients(concern)
                self.target_ingredients.extend(ingr)
            except ValueError:
                pass

        # 2. בדיקת מחסום עור פגוע
        has_barrier_damage = "damaged_barrier" in profile.concerns or "eczema" in profile.concerns
        if has_barrier_damage:
            self.warnings.append("זוהה מחסום עור פגוע או גירוי פעיל. חומרים מקלפים וחומצות חזקות הוסרו מהשגרה לטובת שיקום והרגעה.")

        # 3. בחירת מוצרים בעזרת מערכת ניקוד
        am_cleanser = self._pick_best(ptype="cleanser", is_am=True)
        pm_cleanser = self._pick_best(ptype="cleanser", is_am=False)

        am_moisturizer = self._pick_best(ptype="moisturizer", is_am=True)
        pm_moisturizer = self._pick_best(ptype="moisturizer", is_am=False)

        am_sunscreen = self._pick_best(ptype="sunscreen", is_am=True)

        # בחירת טיפולים פעילים (סרומים/טונרים) מותאמים אישית
        am_actives = self._pick_actives(is_am=True, max_count=1)
        pm_actives = self._pick_actives(is_am=False, max_count=3)

        # הרכבת שגרת בוקר
        am_routine = []
        if am_cleanser:
            am_routine.append(am_cleanser)
        am_routine.extend(am_actives)
        if am_moisturizer:
            am_routine.append(am_moisturizer)
        if am_sunscreen:
            am_routine.append(am_sunscreen)

        # הרכבת שגרת ערב
        pm_routine = []
        if pm_cleanser:
            pm_routine.append(pm_cleanser)
        pm_routine.extend(pm_actives)
        if pm_moisturizer:
            pm_routine.append(pm_moisturizer)

        # נימוקים
        self._generate_explanations(am_routine + pm_routine)

        return RoutinePlan(
            am_routine=am_routine,
            pm_routine=pm_routine,
            warnings=self.warnings,
            explanations=self.explanations
        )

    def _score_product(self, prod: Product, is_am: bool) -> float:
        score = 0.0
        
        # התאמת זמן יום
        if is_am and not prod.am_suitable:
            return -100.0
        if not is_am and not prod.pm_suitable:
            return -100.0

        # בדיקת רגישות ומחסום עור
        has_barrier_damage = "damaged_barrier" in self.profile.concerns or "eczema" in self.profile.concerns
        if has_barrier_damage and not prod.is_safe_for_barrier_concerns:
            return -100.0
        if self.profile.sensitivity_level <= 2 and not prod.is_safe_for_sensitive:
            return -50.0

        # ניקוד לפי רכיבים מומלצים למטרות
        if prod.active_family:
            for active in self.target_ingredients:
                if active.lower() in prod.active_family.lower() or prod.active_family.lower() in active.lower():
                    score += 15.0

        # התאמת סוג עור
        stype = self.profile.skin_type
        pname = prod.name.lower()
        bname = prod.brand.lower()
        if stype == "oily" and ("gel" in pname or "foam" in pname or "bha" in pname or "niacinamide" in pname):
            score += 5.0
        elif stype == "dry" and ("hydrating" in pname or "rich" in pname or "cream" in pname or "hyaluronic" in pname):
            score += 5.0

        return score

    def _pick_best(self, ptype: str, is_am: bool) -> Optional[Product]:
        candidates = [p for p in self.products if p.product_type == ptype]
        candidates.sort(key=lambda p: self._score_product(p, is_am), reverse=True)
        return candidates[0] if candidates and self._score_product(candidates[0], is_am) > -50 else None

    def _pick_actives(self, is_am: bool, max_count: int) -> List[Product]:
        candidates = [p for p in self.products if p.product_type in ["serum", "toner", "treatment"]]
        scored = []
        for p in candidates:
            sc = self._score_product(p, is_am)
            if sc > 0:
                scored.append((sc, p))

        scored.sort(key=lambda x: x[0], reverse=True)
        
        selected: List[Product] = []
        for _, prod in scored:
            if len(selected) >= max_count:
                break
            # מניעת קונפליקט מול מוצרים שכבר נבחרו
            has_conflict = False
            for s in selected:
                if check_product_conflict(prod, s) or check_product_conflict(s, prod):
                    has_conflict = True
                    break
            if not has_conflict:
                selected.append(prod)

        return selected

    def _generate_explanations(self, all_prods: List[Product]):
        added = set()
        for p in all_prods:
            if p.id in added:
                continue
            added.add(p.id)
            if p.active_family:
                self.explanations.append(f"{p.brand} - {p.name}: שולב בשגרה בזכות רכיב ה-{p.active_family} המותאם ישירות למטרות הטיפוח שלך.")