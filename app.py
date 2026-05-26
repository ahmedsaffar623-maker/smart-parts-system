import streamlit as st
from supabase import create_client

# 1. إعدادات الاتصال
SUPABASE_URL = "https://kvehcxtccbfqofrhbmht.supabase.co"
SUPABASE_KEY = "sb_publishable_nSn2mLEBLr08eFTUMjXxaA_LkN6xSA9"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. إدارة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 3. واجهة الدخول
if not st.session_state.logged_in:
    st.title("🔐 تسجيل الدخول")
    user = st.text_input("اسم المستخدم")
    pw = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        if user == "admin" and pw == "123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("بيانات الدخول خاطئة")
else:
    # 4. لوحة التحكم
    st.sidebar.button("تسجيل خروج", on_click=lambda: st.session_state.update(logged_in=False) or st.rerun())
    st.title("📦 لوحة تحكم قطع الغيار")
    
    # إضافة قطعة
    name = st.text_input("اسم القطعة")
    qty = st.number_input("الكمية", min_value=0)
    if st.button("إضافة"):
        # تعديل ليتوافق مع النسخة الجديدة من supabase
        supabase.table("parts").insert({"name": name, "quantity": qty}).execute()
        st.success("تمت الإضافة!")
        st.rerun()

    # عرض البيانات
    st.subheader("📋 القائمة:")
    response = supabase.table("parts").select("*").execute()
    st.table(response.data)
