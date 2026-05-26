import streamlit as st
from supabase import create_client

# إعدادات الاتصال (تأكد من وضع بيانات مشروعك الحقيقية)
SUPABASE_URL = "https://kvehcxtccbfqofrhbmht.supabase.co"
SUPABASE_KEY = "sb_publishable_nSn2mLEBLr08eFTUMjXxaA_LkN6xSA9"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="نظام قطع الغيار", layout="wide")
st.title("📦 نظام إدارة قطع الغيار المتكامل")

# القائمة الجانبية للتنقل
menu = st.sidebar.radio("القائمة الرئيسية", ["المخزون", "المشتريات", "الفواتير"])

# 1. قسم المخزون (عرض وإضافة)
if menu == "المخزون":
    st.header("📋 المخزون الحالي")
    
    # نموذج إضافة قطعة جديدة
    with st.expander("➕ إضافة قطعة جديدة للمخزون"):
        with st.form("add_part"):
            name = st.text_input("اسم القطعة")
            qty = st.number_input("الكمية", min_value=0)
            if st.form_submit_button("إضافة"):
                supabase.table("parts").insert({"name": name, "quantity": qty}).execute()
                st.success("تمت الإضافة!")
                st.rerun()
    
    # عرض المخزون
    res = supabase.table("parts").select("*").execute()
    st.table(res.data)

# 2. قسم المشتريات
elif menu == "المشتريات":
    st.header("📥 تسجيل المشتريات")
    with st.form("purchase_form"):
        part_name = st.text_input("اسم القطعة")
        qty = st.number_input("الكمية المشتراة", min_value=1)
        cost = st.number_input("التكلفة الإجمالية")
        if st.form_submit_button("حفظ المشتريات"):
            supabase.table("purchases").insert({"part_name": part_name, "quantity": qty, "cost": cost}).execute()
            st.success("تم تسجيل المشتريات!")

# 3. قسم الفواتير
elif menu == "الفواتير":
    st.header("🧾 الفواتير")
    res = supabase.table("invoices").select("*").execute()
    st.table(res.data)
