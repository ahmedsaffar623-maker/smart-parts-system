import streamlit as st
from supabase import create_client

# تأكد من أن الرابط والمفتاح صحيحان تماماً من إعدادات Supabase
SUPABASE_URL = "https://kvehcxtccbfqofrhbmht.supabase.co"
SUPABASE_KEY = "sb_publishable_nSn2mLEBLr08eFTUMjXxaA_LkN6xSA9"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="نظام قطع الغيار", layout="wide")
st.title("📦 نظام إدارة قطع الغيار المتكامل")

# القائمة الجانبية
menu = st.sidebar.radio("القائمة", ["المخزون", "المشتريات", "الفواتير"])

try:
    if menu == "المخزون":
        st.header("📋 المخزون")
        res = supabase.table("parts").select("*").execute()
        st.table(res.data)

    elif menu == "المشتريات":
        st.header("📥 تسجيل مشتريات")
        with st.form("purchase"):
            name = st.text_input("اسم القطعة")
            qty = st.number_input("الكمية", min_value=1)
            cost = st.number_input("التكلفة")
            if st.form_submit_button("حفظ"):
                supabase.table("purchases").insert({"part_name": name, "quantity": qty, "cost": cost}).execute()
                st.success("تم الحفظ!")

    elif menu == "الفواتير":
        st.header("🧾 الفواتير")
        res = supabase.table("invoices").select("*").execute()
        st.table(res.data)

except Exception as e:
    st.error(f"خطأ في الاتصال: {e}")
    
