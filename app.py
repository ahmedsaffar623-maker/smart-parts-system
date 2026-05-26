import streamlit as st
from supabase import create_client

# 1. إعدادات الصفحة
st.set_page_config(page_title="نظام قطع الغيار", layout="wide")

# 2. إعداد الاتصال بـ Supabase (ضع مفاتيحك هنا)
SUPABASE_URL = "https://kvehcxtccbfqofrhbmht.supabase.co"
SUPABASE_KEY = "ضع_المفتاح_الخاص_بك_هنا" 
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 3. إدارة الجلسة (Session State)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 4. واجهة تسجيل الدخول
if not st.session_state.logged_in:
    st.title("🔐 تسجيل الدخول إلى النظام")
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    
    if st.button("دخول"):
        if username == "admin" and password == "123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
else:
    # 5. لوحة التحكم (تظهر بعد الدخول)
    st.sidebar.title("خيارات النظام")
    if st.sidebar.button("تسجيل خروج"):
        st.session_state.logged_in = False
        st.rerun()
        
    st.title("📦 لوحة تحكم قطع الغيار")
    
    # نموذج إضافة قطعة
    with st.form("add_part"):
        st.subheader("إضافة قطعة جديدة")
        name = st.text_input("اسم القطعة")
        qty = st.number_input("الكمية", min_value=0, step=1)
        submit = st.form_submit_button("حفظ في قاعدة البيانات")
        
        if submit:
            if name:
                # إرسال البيانات لـ Supabase
                supabase.table("parts").insert({"name": name, "quantity": qty}).execute()
                st.success(f"تم حفظ {name} بنجاح!")
            else:
                st.warning("يرجى كتابة اسم القطعة")

    # عرض البيانات من Supabase
    st.subheader("📋 قائمة قطع الغيار الحالية:")
    response = supabase.table("parts").select("*").execute()
    data = response.data
    
    if data:
        st.table(data)
    else:
        st.info("لا توجد بيانات حالياً.")
