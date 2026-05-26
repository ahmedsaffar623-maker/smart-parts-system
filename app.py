import streamlit as st
from supabase import create_client

# إعداد الاتصال
SUPABASE_URL = "https://kvehcxtccbfqofrhbmht.supabase.co"
SUPABASE_KEY = "sb_publishable_nSn2mLEBLr08eFTUMjXxaA_LkN6xSA9"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Ruwaiei ERP", layout="wide")
st.title("📦 نظام Ruwaiei المتكامل لقطع الغيار")

menu = st.sidebar.radio("القائمة الرئيسية", ["المخزون", "المبيعات", "البحث بالـ VIN"])

if menu == "المخزون":
    st.header("📋 إدارة المخزون")
    res = supabase.table("parts").select("*").execute()
    st.dataframe(res.data)

elif menu == "المبيعات":
    st.header("🧾 إصدار فاتورة بيع")
    with st.form("sale_form"):
        cust_id = st.number_input("ID العميل", min_value=1)
        part_num = st.text_input("رقم القطعة")
        qty = st.number_input("الكمية", min_value=1)
        if st.form_submit_button("إتمام البيع"):
            supabase.table("sales_items").insert({
                "part_number": part_num, 
                "quantity": qty
            }).execute()
            st.success("تم تسجيل العملية وتحديث المخزون تلقائياً!")

elif menu == "البحث بالـ VIN":
    st.header("🔍 البحث برقم الشاصي")
    vin = st.text_input("أدخل رقم الشاصي (VIN)")
    if vin:
        res = supabase.table("vin_search_view").select("*").eq("vin_number", vin).execute()
        st.table(res.data)
