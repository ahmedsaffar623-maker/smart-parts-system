import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv

# ==========================================
# إعداد الصفحة
# ==========================================

st.set_page_config(
    page_title="Smart Parts to search by VIN",
    page_icon="🚗",
    layout="wide"
)

# ==========================================
# تحميل متغيرات البيئة
# ==========================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ==========================================
# تنسيق الواجهة
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #0f172a;
    color: white;
}

h1, h2, h3 {
    color: white;
}

.stTextInput input {
    background-color: #1e293b;
    color: white;
}

.stButton button {
    width: 100%;
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 45px;
    border: none;
    font-size: 16px;
}

[data-testid="stSidebar"] {
    background-color: #111827;
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
# جلب بيانات السيارة
# ==========================================

def get_vehicle(vin):

    response = supabase.table("vehicles") \
        .select("*") \
        .eq("vin_number", vin) \
        .execute()

    if response.data:
        return response.data[0]

    return None

# ==========================================
# جلب الكتالوج
# ==========================================

def get_catalog(model_name):

    response = supabase.table("model_catalogs") \
        .select("*") \
        .eq("model_name", model_name) \
        .execute()

    if response.data:
        return response.data[0]

    return None

# ==========================================
# جلب القطع المتوافقة
# ==========================================

def get_compatible_parts(vin):

    response = supabase.table("vin_parts") \
        .select("""

            part_number,

            parts(
                part_number,
                part_name,
                current_stock,
                sale_price,
                location,
                part_type
            )

        """) \
        .eq("vin_number", vin) \
        .execute()

    return response.data

# ==========================================
# القائمة الجانبية
# ==========================================

# ==========================================
# صفحة البحث بالـ VIN
# ==========================================
st.sidebar.title("🚗 نظام الرويعي الذكي")

menu = st.sidebar.radio(
    "القائمة",
    [
        "لوحة التحكم",
        "البحث بالـ VIN",
        "إدارة المخزون"
    ]
)

# ==========================================
# البحث بالـ VIN
# ==========================================

if menu == "البحث بالـ VIN":

    st.title("🔍 البحث الذكي برقم الشاصي")

    vin_input = st.text_input(
        "أدخل رقم الشاصي VIN"
    )

    if st.button("بحث"):

        vin = normalize_vin(vin_input)

        if len(vin) != 17:

            st.error("رقم الشاصي يجب أن يكون 17 خانة")

        else:

            vehicle = get_vehicle(vin)

            if not vehicle:

                st.error("لم يتم العثور على السيارة")

            else:

                st.success("تم العثور على السيارة")

                # ==================================
                # بيانات السيارة
                # ==================================

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "MODEL",
                        vehicle["model_name"]
                    )

                with col2:
                    st.metric(
                        "MTOC",
                        vehicle["mtoc"]
                    )

                with col3:
                    st.metric(
                        "VIN",
                        vehicle["vin_number"]
                    )

                # ==================================
                # الكتالوج
                # ==================================

                catalog = get_catalog(
                    vehicle["model_name"]
                )

                if catalog:

                    st.markdown("## 📘 الكتالوج")

                    st.link_button(
                        "فتح الكتالوج الأصلي",
                        catalog["catalog_url"]
                    )

                # ==================================
                # القطع المتوافقة
                # ==================================

                st.markdown("## 📦 القطع المتوافقة")

                compatible_parts = get_compatible_parts(vin)

                if compatible_parts:

                    parts_table = []

                    for item in compatible_parts:

                        if item["parts"]:

                            p = item["parts"]

                            stock_status = "✅ متوفر"

                            if p["current_stock"] <= 0:
                                stock_status = "❌ غير متوفر"

                            parts_table.append({

                                "رقم القطعة":
                                    p["part_number"],

                                "اسم القطعة":
                                    p["part_name"],

                                "المخزون":
                                    p["current_stock"],

                                "السعر":
                                    p["sale_price"],

                                "الموقع":
                                    p["location"],

                                "النوع":
                                    p["part_type"],

                                "الحالة":
                                    stock_status
                            })

                    st.dataframe(
                        parts_table,
                        use_container_width=True
                    )

                else:

                    st.warning(
                        "لا توجد قطع مرتبطة بهذا VIN"
                    )

# ==========================================
# إدارة المخزون
# ==========================================

elif menu == "إدارة المخزون":

    st.title("📦 إدارة المخزون")

    inventory = supabase.table("parts") \
        .select("*") \
        .limit(1000) \
        .execute()

    if inventory.data:

        st.dataframe(
            inventory.data,
            use_container_width=True
        )

    else:

        st.warning("لا يوجد مخزون")
