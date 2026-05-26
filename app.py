import streamlit as st
from supabase import create_client

# تأكد من مفاتيحك الصحيحة
url = "https://kvehcxtccbfqofrhbmht.supabase.co"
key = "sb_publishable_nSn2mLEBLr08eFTUMjXxaA_LkN6xSA9"
supabase = create_client(url, key)

st.title("📦 نظام إدارة قطع الغيار المتكامل")
menu = st.sidebar.radio("القائمة", ["المخزون", "المشتريات", "الفواتير"])

if menu == "المخزون":
    st.header("📋 المخزون")
    res = supabase.table("parts").select("*").execute()
    st.table(res.data)

elif menu == "المشتريات":
    st.header("📥 المشتريات")
    # نموذج تسجيل المشتريات
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
