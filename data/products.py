"""
מאגר מוצרים מורחב ומקיף הכולל מוצרי K-Beauty, מוצרי iHerb וסקירות Reviews by Maya.
"""
from .schema import Product

SEED_PRODUCTS = [
    # ==========================================
    # --- 1. סבוני ניקוי פנים (Cleansers) ---
    # ==========================================
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
        id="p_cleanse_laroche_toleriane",
        name="Toleriane Hydrating Gentle Cleanser",
        brand="La Roche-Posay",
        product_type="cleanser",
        active_family="Ceramides",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_cleanse_cosrx_good_morning",
        name="Low pH Good Morning Gel Cleanser",
        brand="COSRX",
        product_type="cleanser",
        active_family="Tea_Tree",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=False,
        is_safe_for_sensitive=False
    ),
    Product(
        id="p_cleanse_roundlab_dokdo",
        name="1025 Dokdo Cleanser",
        brand="Round Lab",
        product_type="cleanser",
        active_family="Panthenol",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_cleanse_heimish_all_clean",
        name="All Clean Balm (ניקוי ראשוני והסרת איפור)",
        brand="Heimish",
        product_type="cleanser",
        active_family="",
        max_weekly_frequency=7,
        time_allowed="PM",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    # ==========================================
    # --- 2. טונרים ותמציות (Toners & Essences) ---
    # ==========================================
    Product(
        id="p_toner_cosrx_snail",
        name="Advanced Snail 96 Mucin Power Essence",
        brand="COSRX",
        product_type="essence",
        active_family="Centella_Asiatica",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_toner_cosrx_propolis",
        name="Full Fit Propolis Synergy Toner",
        brand="COSRX",
        product_type="toner",
        active_family="Panthenol",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_toner_im_from_rice",
        name="Rice Toner (הזנה, הבהרה וזוהר)",
        brand="I'm From",
        product_type="toner",
        active_family="Niacinamide",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_toner_haruharu_black_rice",
        name="Black Rice Hyaluronic Toner",
        brand="Haruharu WONDER",
        product_type="toner",
        active_family="Hyaluronic_Acid",
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
        id="p_toner_isntree_chestnut_bha",
        name="Chestnut BHA 2% Clear Liquid",
        brand="Isntree",
        product_type="exfoliant",
        active_family="Salicylic_Acid",
        max_weekly_frequency=3,
        time_allowed="PM",
        is_safe_for_barrier_concerns=False,
        is_safe_for_sensitive=False
    ),
    Product(
        id="p_toner_anua_heartleaf",
        name="Heartleaf 77% Soothing Toner",
        brand="Anua",
        product_type="toner",
        active_family="Panthenol",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_toner_to_glycolic",
        name="Glycolic Acid 7% Toning Solution",
        brand="The Ordinary",
        product_type="toner",
        active_family="Glycolic_Acid",
        max_weekly_frequency=2,
        time_allowed="PM",
        is_safe_for_barrier_concerns=False,
        is_safe_for_sensitive=False
    ),
    # ==========================================
    # --- 3. סרומים: טיפול באקנה, שחורים ומרקם ---
    # ==========================================
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
        id="p_serum_to_salicylic",
        name="Salicylic Acid 2% Solution",
        brand="The Ordinary",
        product_type="serum",
        active_family="Salicylic_Acid",
        max_weekly_frequency=3,
        time_allowed="PM",
        is_safe_for_barrier_concerns=False,
        is_safe_for_sensitive=False
    ),
    Product(
        id="p_serum_geek_porefectly",
        name="Porefectly Clear 2% BHA + Sarcosine",
        brand="Geek & Gorgeous",
        product_type="serum",
        active_family="Salicylic_Acid",
        max_weekly_frequency=3,
        time_allowed="PM",
        is_safe_for_barrier_concerns=False,
        is_safe_for_sensitive=True
    ),
    # ==========================================
    # --- 4. סרומים: פיגמנטציה, כתמים ו-PIE/PIH ---
    # ==========================================
    Product(
        id="p_serum_to_azelaic",
        name="Azelaic Acid Suspension 10%",
        brand="The Ordinary",
        product_type="serum",
        active_family="Azelaic_Acid",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_serum_melano_cc",
        name="Melano CC Vitamin C Essence",
        brand="Rohto Mentholatum",
        product_type="serum",
        active_family="Pure_Vitamin_C",
        max_weekly_frequency=7,
        time_allowed="AM",
        is_safe_for_barrier_concerns=False,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_serum_timeless_vit_c",
        name="20% Vitamin C + E Ferulic Acid Serum",
        brand="Timeless Skin Care",
        product_type="serum",
        active_family="Pure_Vitamin_C",
        max_weekly_frequency=7,
        time_allowed="AM",
        is_safe_for_barrier_concerns=False,
        is_safe_for_sensitive=False
    ),
    Product(
        id="p_serum_naturium_tranexamic",
        name="Tranexamic Topical Acid 5%",
        brand="Naturium",
        product_type="serum",
        active_family="Tranexamic_Acid",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_serum_to_alpha_arbutin",
        name="Alpha Arbutin 2% + HA",
        brand="The Ordinary",
        product_type="serum",
        active_family="Alpha_Arbutin",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_serum_axis_y_dark_spot",
        name="Dark Spot Correcting Glow Serum",
        brand="AXIS-Y",
        product_type="serum",
        active_family="Niacinamide",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    # ==========================================
    # --- 5. סרומים: אנטי-אייג'ינג, רטינואידים ומיצוק ---
    # ==========================================
    Product(
        id="p_serum_beauty_of_joseon_retinal",
        name="Revive Eye Serum : Ginseng + Retinal",
        brand="Beauty of Joseon",
        product_type="serum",
        active_family="Retinoids",
        max_weekly_frequency=4,
        time_allowed="PM",
        is_safe_for_barrier_concerns=False,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_serum_geek_agame_5",
        name="A-Game 5 (0.05% Retinal)",
        brand="Geek & Gorgeous",
        product_type="serum",
        active_family="Retinoids",
        max_weekly_frequency=3,
        time_allowed="PM",
        is_safe_for_barrier_concerns=False,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_serum_to_buffet",
        name="Multi-Peptide + HA Serum (Buffet)",
        brand="The Ordinary",
        product_type="serum",
        active_family="Peptides",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_serum_to_caffeine",
        name="Caffeine Solution 5% + EGCG",
        brand="The Ordinary",
        product_type="treatment",
        active_family="Caffeine",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    # ==========================================
    # --- 6. סרומים: שיקום, אדמומיות ולחות עמוקה ---
    # ==========================================
    Product(
        id="p_serum_skin1004_centella",
        name="Madagascar Centella Ampoule",
        brand="SKIN1004",
        product_type="ampoule",
        active_family="Centella_Asiatica",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_serum_torriden_dive_in",
        name="DIVE-IN Low Molecular Hyaluronic Acid Serum",
        brand="Torriden",
        product_type="serum",
        active_family="Hyaluronic_Acid",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_serum_purito_unscented_centella",
        name="Centella Unscented Recovery Serum",
        brand="PURITO",
        product_type="serum",
        active_family="Centella_Asiatica",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    # ==========================================
    # --- 7. קרמי לחות (Moisturizers) ---
    # ==========================================
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
        id="p_moist_etude_soonjung_2x",
        name="SoonJung 2x Barrier Intensive Cream",
        brand="ETUDE",
        product_type="moisturizer",
        active_family="Panthenol",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_moist_purito_oat_in",
        name="Oat-in Calming Gel Cream",
        brand="PURITO",
        product_type="moisturizer",
        active_family="Panthenol",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_moist_pyunkang_yul_nutrition",
        name="Nutrition Cream (הזנה עמוקה לעור יבש)",
        brand="Pyunkang Yul",
        product_type="moisturizer",
        active_family="",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_moist_laroche_cicaplast",
        name="Cicaplast Baume B5+",
        brand="La Roche-Posay",
        product_type="moisturizer",
        active_family="Panthenol",
        max_weekly_frequency=7,
        time_allowed="PM",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_moist_cerave_pm",
        name="PM Facial Moisturizing Lotion",
        brand="CeraVe",
        product_type="moisturizer",
        active_family="Niacinamide",
        max_weekly_frequency=7,
        time_allowed="ANY",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    # ==========================================
    # --- 8. מקדמי הגנה (Sunscreens) ---
    # ==========================================
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
    ),
    Product(
        id="p_sun_roundlab_birch",
        name="Birch Juice Moisturizing Sunscreen",
        brand="Round Lab",
        product_type="sunscreen",
        active_family="Hyaluronic_Acid",
        max_weekly_frequency=7,
        time_allowed="AM",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_sun_skin1004_hyalu_cica",
        name="Madagascar Centella Hyalu-Cica Water-Fit Sun Serum",
        brand="SKIN1004",
        product_type="sunscreen",
        active_family="Centella_Asiatica",
        max_weekly_frequency=7,
        time_allowed="AM",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    ),
    Product(
        id="p_sun_laroche_anthelios_uvmune",
        name="Anthelios UVMune 400 Invisible Fluid SPF50+",
        brand="La Roche-Posay",
        product_type="sunscreen",
        active_family="",
        max_weekly_frequency=7,
        time_allowed="AM",
        is_safe_for_barrier_concerns=True,
        is_safe_for_sensitive=True
    )
]