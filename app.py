import streamlit as st
import pandas as pd

from supabase import create_client
from dotenv import load_dotenv

import os

# ==========================================
# تحميل بيانات البيئة
# ==========================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ==========================================
# إعداد الصفحة
# ==========================================

st.set_page_config(
    page_title="RUWAIEI SMART SYSTEM",
    page_icon="🚘",
    layout="wide"
)

# ==========================================
# CSS تصميم احترافي
# ==========================================

st.markdown("""
<style>

/* الخلفية العامة */

.stApp {
    background-color: #0f0f0f;
    color: white;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background-color: #111111;
    border-left: 3px solid #ff7a00;
}

/* العناوين */

h1, h2, h3, h4 {
    color: #ff7a00 !important;
    font-weight: bold;
}

/* النصوص */

p, label, div {
    color: white;
}

/* حقول الإدخال */

.stTextInput input {

    background-color: #1b1b1b !important;

    color: white !important;

    border: 2px solid #ff7a00 !important;

    border-radius: 12px;

    height: 45px;

    font-size: 15px;
}

/* الأزرار */

.stButton button {

    width: 100%;

    background-color: #ff7a00;

    color: white;

    border: none;

    border-radius: 12px;

    height: 48px;

    font-size: 16px;

    font-weight: bold;

    transition: 0.3s;
}

/* Hover */

.stButton button:hover {

    background-color: #ff9500;

    color: black;
}

/* الجداول */

[data-testid="stDataFrame"] {

    border: 1px solid #ff7a00;

    border-radius: 12px;

    overflow: hidden;
}

/* البطاقات */

[data-testid="metric-container"] {

    background-color: #1a1a1a;

    border: 1px solid #ff7a00;

    padding: 15px;

    border-radius: 12px;
}

/* الرسائل */

.stSuccess {

    background-color: #1b1b1b !important;

    border: 1px solid #00c853;

    border-radius: 10px;
}

.stError {

    background-color: #1b1b1b !important;

    border: 1px solid #ff3d00;

    border-radius: 10px;
}

/* الفواصل */

hr {
    border-color: #ff7a00;
}

/* المسافات */

.block-container {
    padding-top: 2rem;
}

/* القائمة الجانبية */

section[data-testid="stSidebar"] .stRadio label {

    color: white !important;

    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# Normalize VIN
# ==========================================

def normalize_vin(vin):

    if not vin:
        return ""

    vin = vin.upper().strip()

    vin = vin.replace(" ", "")
    vin = vin.replace("-", "")
    vin = vin.replace("_", "")

    return vin

# ==========================================
# البحث الذكي بالـ VIN
# ==========================================

def search_by_vin(vin):

    vin = normalize_vin(vin)

    response = supabase.table(
        "vin_inventory_view"
    ).select("*").eq(
        "vin_number",
        vin
    ).execute()

    return response.data

# ==========================================
# جلب المخزون
# ==========================================

def get_inventory():

    response = supabase.table(
        "parts"
    ).select("*").limit(1000).execute()

    return response.data

# ==========================================
# القائمة الجانبية
# ==========================================

st.sidebar.title("🚗 نظام الرويعي الذكي")

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "القائمة الرئيسية",
    [
        "لوحة التحكم",
        "البحث بالـ VIN",
        "إدارة المخزون"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "نظام ذكي لإدارة قطع غيار السيارات الصينية"
)

# ==========================================
# لوحة التحكم
# ==========================================

if menu == "لوحة التحكم":

    st.title("📊 لوحة التحكم الذكية")

    # ======================================
    # الإحصائيات
    # ======================================

    total_parts = supabase.table(
        "parts"
    ).select(
        "*",
        count="exact"
    ).execute()

    total_vins = supabase.table(
        "vin_parts"
    ).select(
        "*",
        count="exact"
    ).execute()

    total_suppliers = supabase.table(
        "suppliers"
    ).select(
        "*",
        count="exact"
    ).execute()

    low_stock = supabase.table(
        "parts"
    ).select(
        "*",
        count="exact"
    ).lte(
        "current_stock",
        5
    ).execute()

    # ======================================
    # بطاقات الإحصائيات
    # ======================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📦 إجمالي القطع",
            total_parts.count
        )

    with col2:

        st.metric(
            "🚗 عدد VIN",
            total_vins.count
        )

    with col3:

        st.metric(
            "🏢 الموردين",
            total_suppliers.count
        )

    with col4:

        st.metric(
            "⚠️ قطع منخفضة المخزون",
            low_stock.count
        )

    st.divider()

    # ======================================
    # القطع منخفضة المخزون
    # ======================================

    st.subheader("⚠️ القطع منخفضة المخزون")

    low_stock_parts = supabase.table(
        "parts"
    ).select(
        "part_number, part_name, current_stock"
    ).lte(
        "current_stock",
        5
    ).limit(20).execute()

    if low_stock_parts.data:

        df = pd.DataFrame(
            low_stock_parts.data
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.success(
            "لا توجد قطع منخفضة المخزون"
        )

# ==========================================
# صفحة البحث بالـ VIN
# ==========================================

elif menu == "البحث بالـ VIN":

    st.title("🔍 البحث الذكي برقم الشاصي")

    vin_input = st.text_input(
        "أدخل رقم الشاصي VIN"
    )

    if st.button("بحث"):

        vin = normalize_vin(vin_input)

        if len(vin) != 17:

            st.error(
                "رقم الشاصي يجب أن يكون 17 خانة"
            )

        else:

            results = search_by_vin(vin)

            if results:

                st.success(
                    f"تم العثور على {len(results)} قطعة متوافقة"
                )

                table_data = []

                for item in results:

                    stock_status = "✅ متوفر"

                    if item["current_stock"] <= 0:

                        stock_status = "❌ غير متوفر"

                    table_data.append({

                        "رقم القطعة":
                            item["part_number"],

                        "اسم القطعة":
                            item["part_name"],

                        "الوصف":
                            item["description"],

                        "المخزون":
                            item["current_stock"],

                        "السعر":
                            item["unit_price"],

                        "الموقع":
                            item["location_code"],

                        "الحالة":
                            stock_status,

                        "نوع التوافق":
                            item["compatibility_type"]
                    })

                df = pd.DataFrame(
                    table_data
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

            else:

                st.error(
                    "لا توجد بيانات مرتبطة بهذا VIN"
                )

# ==========================================
# إدارة المخزون
# ==========================================

elif menu == "إدارة المخزون":

    st.title("📦 إدارة المخزون")

    inventory = get_inventory()

    if inventory:

        df = pd.DataFrame(inventory)

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.warning(
            "المخزون فارغ"
        )
