import streamlit as st
from supabase import create_client
import os
import pandas as pd
from dotenv import load_dotenv

# إعداد الصفحة
st.set_page_config(page_title="نظام الرويعي الذكي", page_icon="🚗", layout="wide")

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# تنسيق الواجهة (برتقالي، أسود، أبيض)
st.markdown("""
<style>
    .main { background-color: #ffffff; color: #000000; }
    h1, h2, h3 { color: #f97316; }
    .stButton button { background-color: #f97316; color: white; border-radius: 8px; border: none; }
    [data-testid="stSidebar"] { background-color: #000000; color: white; }
    [data-testid="stSidebar"] * { color: white; }
</style>
""", unsafe_allow_html=True)

# دالة جلب آمنة
def get_data(table, vin):
    try:
        response = supabase.table(table).select("*").eq("vin_number", vin).execute()
        return response.data if response.data else []
    except:
        return []

# القائمة الجانبية
menu = st.sidebar.radio("القائمة", ["لوحة التحكم", "البحث بالـ VIN", "إدارة المخزون"])

if menu == "البحث بالـ VIN":
    st.title("🔍 البحث الذكي برقم الشاصي")
    vin_input = st.text_input("أدخل رقم الشاصي (VIN)")
    
    if st.button("بحث"):
        vin = vin_input.upper().strip().replace(" ", "").replace("-", "")
        if len(vin) == 17:
            vehicle_data = get_data("vehicles", vin)
            if vehicle_data:
                vehicle = vehicle_data[0]
                st.success("تم العثور على السيارة")
                col1, col2, col3 = st.columns(3)
                col1.metric("الموديل", vehicle.get("model_name", "N/A"))
                col2.metric("MTOC", vehicle.get("mtoc", "N/A"))
                col3.metric("VIN", vehicle.get("vin_number", "N/A"))
                
                # جلب القطع
                parts_res = supabase.table("vin_parts").select("part_number, parts(part_name, current_stock, sale_price, location)").eq("vin_number", vin).execute()
                if parts_res.data:
                    df = pd.DataFrame([ {**p.get("parts"), "رقم القطعة": p.get("part_number")} for p in parts_res.data if p.get("parts")])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("لا توجد قطع مرتبطة بهذا الشاصي")
            else:
                st.error("لم يتم العثور على السيارة")
        else:
            st.error("يجب أن يتكون رقم الشاصي من 17 خانة")

elif menu == "إدارة المخزون":
    st.title("📦 إدارة المخزون")
    res = supabase.table("parts").select("*").execute()
    if res.data:
        st.dataframe(pd.DataFrame(res.data), use_container_width=True)
