import streamlit as st
from supabase import create_client

# 1. إعدادات الاتصال (ضع بياناتك الخاصة هنا)
SUPABASE_URL = "https://kvehcxtccbfqofrhbmht.supabase.co"
SUPABASE_KEY = "sb_publishable_nSn2mLEBLr08eFTUMjXxaA_LkN6xSA9"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# إعدادات الصفحة
st.set_page_config(page_title="نظام قطع الغيار المتكامل", layout="wide")
st.title("📦 نظام إدارة قطع الغيار المتكامل")

# القائمة الجانبية للتنقل
menu = st.sidebar.radio("القائمة الرئيسية", ["المخزون", "المشتريات", "الفواتير"])

# --- قسم المخزون ---
if menu == "المخزون":
    st.header("📋 المخزون الحالي")
    
    # نموذج إضافة قطعة
    with st.expander("➕ إضافة قطعة جديدة"):
        with st.form("add_part"):
            name = st.text_input("اسم القطعة")
            chassis = st.text_input("رقم الشاصي (اختياري)")
            qty = st.number_input("الكمية", min_value=0)
            if st.form_submit_button("حفظ"):
                supabase.table("parts").insert({
                    "name": name, 
                    "chassis_number": chassis, 
                    "quantity": qty
                }).execute()
                st.success("تمت الإضافة!")
                st.rerun()
    
    # عرض المخزون
    res = supabase.table("parts").select("*").execute()
    st.table(res.data)

# --- قسم المشتريات ---
elif menu == "المشتريات":
    st.header("📥 تسجيل المشتريات")
    with st.form("purchase_form"):
        p_name = st.text_input("اسم القطعة المشتراة")
        p_qty = st.number_input("الكمية", min_value=1)
        p_cost = st.number_input("التكلفة الإجمالية")
        if st.form_submit_button("حفظ العملية"):
            supabase.table("purchases").insert({
                "part_name": p_name, 
                "quantity": p_qty, 
                "cost": p_cost
            }).execute()
            st.success("تم تسجيل المشتريات!")
            st.rerun()

# --- قسم الفواتير ---
elif menu == "الفواتير":
    st.header("🧾 الفواتير")
    with st.form("invoice_form"):
        c_name = st.text_input("اسم العميل")
        total = st.number_input("إجمالي الفاتورة")
        if st.form_submit_button("إصدار الفاتورة"):
            supabase.table("invoices").insert({
                "customer_name": c_name, 
                "total_amount": total
            }).execute()
            st.success("تم حفظ الفاتورة!")
            st.rerun()
            
    res = supabase.table("invoices").select("*").execute()
    st.table(res.data)
