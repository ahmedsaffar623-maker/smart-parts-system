import streamlit as st

st.title("نظام إدارة قطع الغيار الذكي")
st.write("مرحباً بك في نظامك الخاص")

username = st.text_input("اسم المستخدم")
password = st.text_input("كلمة المرور", type="password")

if st.button("دخول"):
    if username == "admin" and password == "123":
        st.success("تم تسجيل الدخول بنجاح!")
    else:
        st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
