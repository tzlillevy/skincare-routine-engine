"""
מאגר מוצרים נקי ותקין.
"""
from .schema import Product

SEED_PRODUCTS = [
    Product(
        id="p_cleanse_cetaphil",
        name="Gentle Skin Cleanser",
        brand="Cetaphil",
        product_type="cleanser",
        active_family="",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_cleanse_cerave_foaming",
        name="Foaming Facial Cleanser",
        brand="CeraVe",
        product_type="cleanser",
        active_family="Niacinamide",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_toner_paulas_bha",
        name="Skin Perfecting 2% BHA Liquid Exfoliant",
        brand="Paula's Choice",
        product_type="exfoliant",
        active_family="BHA",
        max_weekly_frequency=3,
        time_allowed="PM",
        is_safe_for_barrier_concerns=False,
        is_safe_for_sensitive=False
    ),
    Product(
        id="p_serum_to_niacinamide",
        name="Niacinamide 10% + Zinc 1%",
        brand="The Ordinary",
        product_type="serum",
        active_family="Niacinamide",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_moist_illiyoon_ceramide",
        name="Ceramide Ato Concentrate Cream",
        brand="Illiyoon",
        product_type="moisturizer",
        active_family="Ceramides",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_sun_beauty_of_joseon_rice",
        name="Relief Sun : Rice + Probiotics",
        brand="Beauty of Joseon",
        product_type="sunscreen",
        active_family="",
        max_weekly_frequency=7,
        time_allowed="AM",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    )
]