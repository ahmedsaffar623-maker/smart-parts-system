import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="نظام قطع الغيار", layout="wide")

# تهيئة حالة الجلسة (Session State) للتأكد من تسجيل الدخول
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# واجهة تسجيل الدخول
if not st.session_state.logged_in:
    st.title("تسجيل الدخول")
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    
    if st.button("دخول"):
        if username == "admin" and password == "123":
            st.session_state.logged_in = True
            st.rerun()  # إعادة تحميل الصفحة لإظهار لوحة التحكم
        else:
            st.error("اسم المستخدم أو كلمة المرور خاطئة")
else:
    # هذا هو الجزء الذي يظهر بعد الدخول (لوحة التحكم)
    st.title("لوحة التحكم - نظام قطع الغيار")
    st.success("أهلاً بك في النظام!")
    
    # هنا يمكنك إضافة محتوى لوحة التحكم الخاص بك
    st.write("هنا يمكنك عرض الجداول والبيانات.")
    
    if st.button("تسجيل خروج"):
        st.session_state.logged_in = False
        st.rerun()
