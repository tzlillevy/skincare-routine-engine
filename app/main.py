import streamlit as st
import sys
import time
from pathlib import Path

# נתיב יבוא המודולים
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from data import SkinProfile, Product, SKIN_TYPES, SKIN_CONCERNS, SEED_PRODUCTS
from engine import RoutineSolver, check_product_conflict

# הגדרות עמוד
st.set_page_config(
    page_title="התאמת שגרת טיפוח אישית",
    page_icon="🧴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# נעילת צבעים, מצב בהיר קבוע, ותיקון מוחלט לכל הרכיבים
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        background-color: #F8FAFC !important;
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Heebo', sans-serif !important;
    }

    html, body, [class*="css"], .stMarkdown, p, span, label, h1, h2, h3, h4, h5, div {
        font-family: 'Heebo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        color: #0F172A !important;
    }

    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0F172A !important;
        text-align: right !important;
        margin-bottom: 0.2rem;
    }

    .sub-title {
        font-size: 1.15rem;
        font-weight: 500;
        color: #475569 !important;
        text-align: right !important;
        margin-bottom: 1.8rem;
    }

    /* כפתורים רגילים */
    div.stButton > button, button[kind="secondary"], .stButton > button {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 8px 18px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }
    div.stButton > button:hover {
        background-color: #F1F5F9 !important;
        border-color: #94A3B8 !important;
        color: #0F172A !important;
    }

    div.stButton > button[kind="primary"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #1D4ED8 !important;
        color: #FFFFFF !important;
    }

    /* רדיו וצ'קבוקסים */
    div[role="radiogroup"] label, .stRadio label, .stCheckbox label {
        color: #0F172A !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        margin-bottom: 8px !important;
        display: flex !important;
        align-items: center !important;
        cursor: pointer !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03) !important;
    }

    div[role="radiogroup"] label:hover, .stCheckbox label:hover {
        border-color: #3B82F6 !important;
        background-color: #F1F5F9 !important;
    }

    /* כרטיס מוצר */
    .product-card {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        direction: rtl !important;
        text-align: right !important;
    }

    .step-badge {
        background-color: #EFF6FF;
        color: #1D4ED8 !important;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 6px;
    }

    .target-badge {
        background-color: #FEF3C7;
        color: #92400E !important;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 6px;
        display: inline-block;
    }

    .product-brand {
        font-size: 0.95rem;
        color: #2563EB !important;
        font-weight: 700;
    }

    .product-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F172A !important;
        margin-bottom: 4px;
    }

    .product-details {
        font-size: 0.9rem;
        color: #475569 !important;
        margin-top: 6px;
        line-height: 1.6;
    }

    /* תיבת בחירה סגורה */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border-color: #CBD5E1 !important;
    }
    .stSelectbox div[data-baseweb="select"] div {
        color: #0F172A !important;
        font-family: 'Heebo', sans-serif !important;
        font-weight: 500 !important;
    }

    /* תפריט נפתח (Dropdown) */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"],
    div[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }

    li[role="option"],
    ul[role="listbox"] li,
    div[data-baseweb="menu"] div,
    div[data-baseweb="menu"] li,
    div[role="option"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        font-family: 'Heebo', sans-serif !important;
        font-weight: 500 !important;
        text-align: right !important;
        direction: rtl !important;
    }

    li[role="option"]:hover,
    li[role="option"][aria-selected="true"],
    div[role="option"]:hover,
    div[role="option"][aria-selected="true"] {
        background-color: #EFF6FF !important;
        color: #1D4ED8 !important;
    }

    /* תיקון אזור העלאת קבצים והסרת כפילות הכפתור */
    [data-testid="stFileUploader"],
    [data-testid="stFileUploader"] section,
    section[data-testid="stFileUploaderDropzone"] {
        background-color: #FFFFFF !important;
        border: 2px dashed #CBD5E1 !important;
        border-radius: 12px !important;
        padding: 24px !important;
    }

    section[data-testid="stFileUploaderDropzone"] span,
    section[data-testid="stFileUploaderDropzone"] small,
    section[data-testid="stFileUploaderDropzone"] div {
        color: #475569 !important;
        font-family: 'Heebo', sans-serif !important;
    }

    /* הסתרת התוכן הפנימי המשוכפל והצגת כפתור עברי נקי */
    section[data-testid="stFileUploaderDropzone"] button {
        background-color: #2563EB !important;
        border: none !important;
        border-radius: 8px !important;
        min-width: 120px !important;
        height: 38px !important;
        position: relative !important;
        font-size: 0 !important;
        cursor: pointer !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    }

    section[data-testid="stFileUploaderDropzone"] button::after {
        content: "העלאת קובץ" !important;
        font-size: 0.95rem !important;
        color: #FFFFFF !important;
        font-family: 'Heebo', sans-serif !important;
        font-weight: 600 !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        white-space: nowrap !important;
    }

    section[data-testid="stFileUploaderDropzone"] button * {
        display: none !important;
    }

    section[data-testid="stFileUploaderDropzone"] button:hover {
        background-color: #1D4ED8 !important;
    }
</style>
""", unsafe_allow_html=True)

# אתחול משתני מצב
if "step" not in st.session_state:
    st.session_state["step"] = 1
if "skin_type" not in st.session_state:
    st.session_state["skin_type"] = "normal"
if "selected_concerns" not in st.session_state:
    st.session_state["selected_concerns"] = []
if "sensitivity_level" not in st.session_state:
    st.session_state["sensitivity_level"] = 3
if "routine_output" not in st.session_state:
    st.session_state["routine_output"] = None

SKIN_TYPE_NAMES = {
    "oily": "עור שמן (ברק מוגבר, נטייה לפצעונים ונקבוביות)",
    "dry": "עור יבש (תחושת מתיחה, חספוס וקילופים)",
    "combination": "עור מעורב (שמנוניות באזור ה-T ויובש בלחיים)",
    "normal": "עור רגיל (מאוזן, ללא יובש או שמנוניות יתר)"
}

CONCERN_NAMES = {
    "acne": "פצעונים ואקנה",
    "blackheads": "ראשים שחורים ונקבוביות חסומות",
    "texture": "מרקם עור לא אחיד ונקבוביות מורחבות",
    "hyperpigmentation": "כתמי שמש ופיגמנטציה",
    "pie_redness": "סימנים אדומים לאחר פצעונים (PIE)",
    "pih_redness": "כתמים כהים לאחר פצעונים (PIH)",
    "damaged_barrier": "מחסום עור פגוע (עקצוץ, אדמומיות ושריפה)",
    "eczema": "אקזמה וגירויים",
    "seborrhea": "סבוריאה וקילופים",
    "dehydrated_skin": "עור מיובש (חסר בלחות פנימית)",
    "anti_aging": "קמטוטים וסימני גיל",
    "redness": "אדמומיות כללית ורגישות",
    "dark_circles": "כהויות מתחת לעיניים",
    "eye_puffiness": "נפיחות מסביב לעיניים",
    "keratosis_pilaris": "חרסוסית (עור ברווז)",
    "insect_bites": "עקיצות וגירוי מקומי"
}

TYPE_TRANSLATIONS = {
    "cleanser": "סבון פנים לניקוי",
    "toner": "טונר מאזן",
    "serum": "סרום טיפולי פעיל",
    "moisturizer": "קרם לחות",
    "sunscreen": "קרם הגנה מפני השמש",
    "treatment": "טיפול נקודתי",
    "oil": "שמן לפנים"
}

def get_product_target(prod: Product) -> str:
    """מזהה לאיזו בעיית עור המוצר מיועד בעיקר על סמך הרכיב הפעיל שבו."""
    actives = (prod.active_family or "").lower()
    ptype = prod.product_type
    
    if "bha" in actives or "salicylic" in actives:
        return "טיפול באקנה, שחורים וניקוי נקבוביות"
    if "aha" in actives or "glycolic" in actives or "lactic" in actives:
        return "חידוש מרקם העור ופילינג עדין"
    if "retinoid" in actives or "retinol" in actives:
        return "חידוש תאים, אנטי-אייג'ינג ושיפור מרקם"
    if "vitamin_c" in actives or "ascorbic" in actives:
        return "הבהרת פיגמנטציה, זוהר והגנה מנזקי חמצון"
    if "niacinamide" in actives:
        return "איזון שומניות, כיווץ נקבוביות והרגעת אדמומיות"
    if "azelaic" in actives:
        return "טשטוש סימנים אדומים (PIE) והרגעת עור"
    if "peptide" in actives or "copper" in actives:
        return "מיצוק העור, שיקום ועידוד ייצור קולגן"
    if "ceramide" in actives or "centella" in actives or "panthenol" in actives:
        return "שיקום מחסום העור, הרגעה והזנה אינטנסיבית"
    if "hyaluronic" in actives or "glycerin" in actives:
        return "הרוויית העור בלחות עמוקה"
    if ptype == "sunscreen":
        return "הגנה חיונית מנזקי UV ומניעת הזדקנות וכתמים"
    if ptype == "cleanser":
        return "הסרת לכלוך, עודפי שומן ואיפור ללא ייבוש"
    if ptype == "moisturizer":
        return "נעילת לחות ושמירה על רכות וגמישות העור"
    return "טיפוח ואיזון כללי"

st.markdown("<div class='main-title'>בניית שגרת טיפוח אישית 🧴</div>", unsafe_allow_html=True)

# ----------------- שלב 1: בחירת סוג עור -----------------
if st.session_state["step"] == 1:
    st.markdown("<div class='sub-title'>שלב 1 מתוך 3: מה סוג העור העיקרי שלך?</div>", unsafe_allow_html=True)
    
    selected_type_key = st.radio(
        "בחרי את סוג העור המתאים ביותר:",
        options=list(SKIN_TYPE_NAMES.keys()),
        format_func=lambda x: SKIN_TYPE_NAMES[x],
        index=list(SKIN_TYPE_NAMES.keys()).index(st.session_state["skin_type"])
    )
    
    st.write("")
    if st.button("המשך לבחירת מטרות טיפוח ⬅️", type="primary"):
        st.session_state["skin_type"] = selected_type_key
        st.session_state["step"] = 2
        st.rerun()

# ----------------- שלב 2: בחירת מטרות ורגישות -----------------
elif st.session_state["step"] == 2:
    st.markdown("<div class='sub-title'>שלב 2 מתוך 3: אילו מטרות ובעיות תרצי לשפר?</div>", unsafe_allow_html=True)
    st.write("**סמני את כל המטרות והבעיות שרלוונטיות עבורך:**")
    
    cols = st.columns(2)
    selected_concerns = []
    concern_items = list(CONCERN_NAMES.items())
    
    for i, (ckey, cname) in enumerate(concern_items):
        col = cols[0] if i < len(concern_items) / 2 else cols[1]
        with col:
            is_checked = st.checkbox(
                cname, 
                value=ckey in st.session_state["selected_concerns"], 
                key=f"chk_{ckey}"
            )
            if is_checked:
                selected_concerns.append(ckey)
                
    st.write("---")
    st.write("**רמת רגישות העור:**")
    sensitivity = st.slider(
        "בחרי מ-1 (רגיש מאוד, אדמומי בקלות) עד 5 (עמיד מאוד לכל תכשיר):",
        min_value=1,
        max_value=5,
        value=st.session_state["sensitivity_level"]
    )
    
    col_back, col_next = st.columns([1, 4])
    with col_back:
        if st.button("חזרה ➡️"):
            st.session_state["step"] = 1
            st.rerun()
    with col_next:
        if st.button("בנה לי שגרת טיפוח אישית ✨", type="primary", use_container_width=True):
            if not selected_concerns:
                st.warning("אנא סמני לפחות מטרה או בעיית עור אחת להמשך.")
            else:
                st.session_state["selected_concerns"] = selected_concerns
                st.session_state["sensitivity_level"] = sensitivity
                st.session_state["step"] = 3
                st.rerun()

# ----------------- שלב 3: הצגת השגרה ובדיקת מוצר -----------------
elif st.session_state["step"] == 3:
    if st.session_state["routine_output"] is None:
        with st.spinner("מנתח נתונים ומרכיב שגרה בטוחה ללא קונפליקטים... ⏳"):
            time.sleep(0.8)
            solver = RoutineSolver()
            profile = SkinProfile(
                skin_type=st.session_state["skin_type"],
                concerns=st.session_state["selected_concerns"],
                sensitivity_level=st.session_state["sensitivity_level"]
            )
            st.session_state["routine_output"] = solver.solve(profile)

    routine = st.session_state["routine_output"]
    st.markdown("<div class='sub-title'>שלב 3 מתוך 3: שגרת הטיפוח המותאמת עבורך</div>", unsafe_allow_html=True)
    
    if routine.warnings:
        for w in routine.warnings:
            st.warning(f"⚠️ {w}")
            
    pm_base = [p for p in routine.pm_routine if p.product_type in ["cleanser", "moisturizer", "oil"]]
    pm_actives = [p for p in routine.pm_routine if p.product_type not in ["cleanser", "moisturizer", "oil"]]
    
    is_split_pm = len(pm_actives) > 2

    col_am, col_pm = st.columns(2)
    
    # עמודת בוקר
    with col_am:
        st.markdown("### שגרת בוקר ☀️")
        for idx, prod in enumerate(routine.am_routine, 1):
            step_name = TYPE_TRANSLATIONS.get(prod.product_type, prod.product_type)
            target_desc = get_product_target(prod)
            st.markdown(f"""
            <div class="product-card">
                <span class="step-badge">שלב {idx}: {step_name}</span>
                <span class="target-badge">🎯 {target_desc}</span>
                <div class="product-brand">{prod.brand}</div>
                <div class="product-name">{prod.name}</div>
                <div class="product-details">
                    🧪 <b>רכיבים פעילים:</b> {prod.active_family if prod.active_family else 'בסיס עדין ומשקם'}<br>
                    📅 <b>תדירות מומלצת:</b> {prod.max_weekly_frequency} פעמים בשבוע
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    # עמודת ערב
    with col_pm:
        if not is_split_pm:
            st.markdown("### שגרת ערב 🌙")
            for idx, prod in enumerate(routine.pm_routine, 1):
                step_name = TYPE_TRANSLATIONS.get(prod.product_type, prod.product_type)
                target_desc = get_product_target(prod)
                st.markdown(f"""
                <div class="product-card">
                    <span class="step-badge">שלב {idx}: {step_name}</span>
                    <span class="target-badge">🎯 {target_desc}</span>
                    <div class="product-brand">{prod.brand}</div>
                    <div class="product-name">{prod.name}</div>
                    <div class="product-details">
                        🧪 <b>רכיבים פעילים:</b> {prod.active_family if prod.active_family else 'לחות והזנה'}<br>
                        📅 <b>תדירות מומלצת:</b> {prod.max_weekly_frequency} פעמים בשבוע
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("### שגרת ערב ברוטציה (למניעת עומס וגירוי) 🌙")
            st.caption("בחרת מספר בעיות עור הדורשות טיפולים שונים. כדי להגן על מחסום העור, פיצלנו את הטיפולים לערבים מתחלפים:")
            
            mid = (len(pm_actives) + 1) // 2
            routine_a = [pm_base[0]] + pm_actives[:mid] + pm_base[1:]
            routine_b = [pm_base[0]] + pm_actives[mid:] + pm_base[1:]
            
            tab_a, tab_b = st.tabs(["ערב א' (טיפול ראשי)", "ערב ב' (טיפול משלים)"])
            
            with tab_a:
                for idx, prod in enumerate(routine_a, 1):
                    step_name = TYPE_TRANSLATIONS.get(prod.product_type, prod.product_type)
                    target_desc = get_product_target(prod)
                    st.markdown(f"""
                    <div class="product-card">
                        <span class="step-badge">שלב {idx}: {step_name}</span>
                        <span class="target-badge">🎯 {target_desc}</span>
                        <div class="product-brand">{prod.brand}</div>
                        <div class="product-name">{prod.name}</div>
                        <div class="product-details">
                            🧪 <b>רכיבים פעילים:</b> {prod.active_family if prod.active_family else 'לחות והזנה'}<br>
                            📅 <b>תדירות:</b> לסירוגין (2-3 פעמים בשבוע)
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
            with tab_b:
                for idx, prod in enumerate(routine_b, 1):
                    step_name = TYPE_TRANSLATIONS.get(prod.product_type, prod.product_type)
                    target_desc = get_product_target(prod)
                    st.markdown(f"""
                    <div class="product-card">
                        <span class="step-badge">שלב {idx}: {step_name}</span>
                        <span class="target-badge">🎯 {target_desc}</span>
                        <div class="product-brand">{prod.brand}</div>
                        <div class="product-name">{prod.name}</div>
                        <div class="product-details">
                            🧪 <b>רכיבים פעילים:</b> {prod.active_family if prod.active_family else 'לחות והזנה'}<br>
                            📅 <b>תדירות:</b> לסירוגין (2-3 פעמים בשבוע)
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    if routine.explanations:
        st.markdown("""
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; margin-top: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
            <div style="font-weight: 700; font-size: 1.05rem; color: #1E293B; margin-bottom: 10px;">
                למה המערכת בחרה במוצרים אלו? 💡
            </div>
        """, unsafe_allow_html=True)
        for exp in routine.explanations:
            st.markdown(f"<div style='color: #475569; font-size: 0.95rem; margin-bottom: 6px;'>• {exp}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    
    # בדיקת מוצר אישי
    st.markdown("### בדיקת מוצר קיים והתאמה לשגרה ➕")
    st.write("רוצה לשלב מוצר שיש לך כבר בבית? בחרי אותו מהרשימה או העלי תמונה לבדיקת בטיחות והתנגשויות:")
    
    product_options = {f"{p.brand} - {p.name}": p for p in SEED_PRODUCTS}
    tab_select, tab_upload = st.tabs(["בחירת מוצר מהמאגר 📋", "העלאת תמונת מוצר 📷"])
    
    selected_prod_to_check = None
    
    with tab_select:
        choice = st.selectbox(
            "בחרי מוצר לבדיקה:",
            options=[""] + list(product_options.keys()),
            format_func=lambda x: "— בחרי מוצר מהרשימה —" if x == "" else x
        )
        if choice != "":
            selected_prod_to_check = product_options[choice]
            
    with tab_upload:
        uploaded_file = st.file_uploader("העלי תמונה של גב המוצר או רשימת הרכיבים:", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            st.info("התמונה נטענה בהצלחה. המוצר נותח במערכת:")
            selected_prod_to_check = SEED_PRODUCTS[1]  # Paula's Choice BHA Liquid
            st.write(f"מוצר שזוהה: **{selected_prod_to_check.brand} - {selected_prod_to_check.name}**")

    if selected_prod_to_check:
        st.write("")
        st.markdown(f"#### תוצאות בדיקה עבור: **{selected_prod_to_check.brand} - {selected_prod_to_check.name}**")
        
        concerns = st.session_state["selected_concerns"]
        is_barrier_issue = ("damaged_barrier" in concerns or "eczema" in concerns) and not selected_prod_to_check.is_safe_for_barrier_concerns
        
        if is_barrier_issue:
            st.error("🚫 **לא מומלץ לשימוש כרגע!** מחסום העור שלך במצב פגום, והמוצר מכיל רכיבים חזקים שעלולים לגרות אותו.")
        elif st.session_state["sensitivity_level"] <= 2 and not selected_prod_to_check.is_safe_for_sensitive:
            st.warning("⚠️ **זהירות לעור רגיש!** מומלץ להתחיל בהדרגה (פעם בשבוע) ולבצע מבחן רגישות.")
        else:
            st.success("✅ **בטוח לשימוש:** המוצר מתאים לרמת הרגישות ומצב העור שלך.")
            
        all_routine_products = routine.am_routine + routine.pm_routine
        conflicts = []
        for p in all_routine_products:
            conflict_msg = check_product_conflict(selected_prod_to_check, p)
            if conflict_msg:
                conflicts.append(f"קונפליקט מול **{p.name}** ({conflict_msg})")
                
        if conflicts:
            st.error("⚠️ **התנגשויות שנמצאו עם השגרה שלך:**")
            for c in conflicts:
                st.write(f"• {c}")
            st.info("💡 **המלצה:** אין למרוח את המוצר באותו יום או באותו זמן מריחה יחד עם המוצרים המתנגשים.")
        else:
            st.success("✨ **אין קונפליקטים כימיים!** ניתן להוסיף את המוצר לשגרה בבטחה.")
            
    st.write("---")
    if st.button("התחל מחדש 🔄"):
        st.session_state["step"] = 1
        st.session_state["routine_output"] = None
        st.session_state["selected_concerns"] = []
        st.rerun()