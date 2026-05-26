import streamlit as st
from supabase import create_client
import pandas as pd

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="نظام الرويعي الذكي",
    page_icon="🚗",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.stApp {
    background-color: #0f172a;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

.sidebar-title {
    color: white;
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}

.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0 0 10px rgba(0,0,0,0.4);
}

.card-title {
    font-size: 18px;
    color: #cbd5e1;
}

.card-value {
    font-size: 32px;
    font-weight: bold;
    color: #38bdf8;
}

h1,h2,h3,h4 {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SUPABASE CONNECTION
# ==========================================

SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_KEY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.markdown(
    "<div class='sidebar-title'>🚗 نظام الرويعي الذكي</div>",
    unsafe_allow_html=True
)

menu = st.sidebar.radio(
    "القائمة الرئيسية",
    [
        "لوحة التحكم",
        "البحث بالشاصي",
        "المخزون",
        "المبيعات",
        "المشتريات",
        "العملاء",
        "الفواتير",
        "المدفوعات",
        "التقارير"
    ]
)

# ==========================================
# DASHBOARD
# ==========================================

if menu == "لوحة التحكم":

    st.title("📊 لوحة التحكم الرئيسية")

    try:

        parts_count = supabase.table("parts").select("id", count="exact").execute()
        customers_count = supabase.table("customers").select("id", count="exact").execute()
        sales_count = supabase.table("sales").select("id", count="exact").execute()
        orders_count = supabase.table("orders").select("id", count="exact").execute()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class='card'>
                <div class='card-title'>الأصناف</div>
                <div class='card-value'>{parts_count.count}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='card'>
                <div class='card-title'>العملاء</div>
                <div class='card-value'>{customers_count.count}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class='card'>
                <div class='card-title'>المبيعات</div>
                <div class='card-value'>{sales_count.count}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class='card'>
                <div class='card-title'>الطلبات</div>
                <div class='card-value'>{orders_count.count}</div>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(e)

# ==========================================
# VIN SEARCH
# ==========================================

elif menu == "البحث بالشاصي":

    st.title("🔍 البحث بالشاصي")

    vin = st.text_input("أدخل رقم الشاصي")

    if st.button("بحث"):

        try:

            result = supabase.table("vehicles") \
                .select("*") \
                .eq("vin_number", vin) \
                .execute()

            if result.data:

                vehicle = result.data[0]

                st.success("تم العثور على السيارة")

                st.write("### بيانات السيارة")
                st.write(f"الموديل: {vehicle['model_name']}")
                st.write(f"MTOC: {vehicle['mtoc']}")

                catalog = supabase.table("model_catalogs") \
                    .select("*") \
                    .eq("model_name", vehicle['model_name']) \
                    .execute()

                if catalog.data:
                    st.write("### رابط الكتالوج")
                    st.link_button(
                        "فتح الكتالوج",
                        catalog.data[0]['catalog_url']
                    )

            else:
                st.warning("رقم الشاصي غير موجود")

        except Exception as e:
            st.error(e)

# ==========================================
# INVENTORY
# ==========================================

elif menu == "المخزون":

    st.title("📦 إدارة المخزون")

    search = st.text_input("بحث برقم القطعة")

    try:

        query = supabase.table("parts").select("*")

        if search:
            query = query.ilike("part_number", f"%{search}%")

        result = query.limit(200).execute()

        if result.data:

            df = pd.DataFrame(result.data)

            st.dataframe(
                df,
                use_container_width=True
            )

        else:
            st.warning("لا توجد بيانات")

    except Exception as e:
        st.error(e)

# ==========================================
# SALES
# ==========================================

elif menu == "المبيعات":

    st.title("💰 المبيعات")

    with st.form("sales_form"):

        customer_id = st.number_input("رقم العميل", min_value=1)
        invoice_number = st.text_input("رقم الفاتورة")
        total_amount = st.number_input("إجمالي الفاتورة")
        paid_amount = st.number_input("المبلغ المدفوع")

        submit = st.form_submit_button("حفظ الفاتورة")

        if submit:

            remaining = total_amount - paid_amount

            if remaining <= 0:
                status = "paid"
            elif paid_amount > 0:
                status = "partial"
            else:
                status = "unpaid"

            try:

                supabase.table("sales").insert({
                    "customer_id": customer_id,
                    "invoice_number": invoice_number,
                    "total_amount": total_amount,
                    "paid_amount": paid_amount,
                    "remaining_amount": remaining,
                    "payment_status": status
                }).execute()

                st.success("تم حفظ الفاتورة")

            except Exception as e:
                st.error(e)

# ==========================================
# PURCHASES
# ==========================================

elif menu == "المشتريات":

    st.title("📥 المشتريات")

    with st.form("purchase_form"):

        supplier_id = st.number_input("رقم المورد", min_value=1)
        invoice_number = st.text_input("رقم فاتورة الشراء")
        total_amount = st.number_input("إجمالي الشراء")

        submit = st.form_submit_button("حفظ")

        if submit:

            try:

                supabase.table("purchases").insert({
                    "supplier_id": supplier_id,
                    "invoice_number": invoice_number,
                    "total_amount": total_amount
                }).execute()

                st.success("تم حفظ فاتورة الشراء")

            except Exception as e:
                st.error(e)

# ==========================================
# CUSTOMERS
# ==========================================

elif menu == "العملاء":

    st.title("👥 العملاء")

    with st.form("customer_form"):

        customer_name = st.text_input("اسم العميل")
        phone = st.text_input("الجوال")
        customer_type = st.selectbox(
            "نوع العميل",
            ["individual", "workshop"]
        )

        submit = st.form_submit_button("إضافة العميل")

        if submit:

            try:

                supabase.table("customers").insert({
                    "customer_name": customer_name,
                    "phone": phone,
                    "customer_type": customer_type
                }).execute()

                st.success("تم إضافة العميل")

            except Exception as e:
                st.error(e)

    st.divider()

    try:

        customers = supabase.table("customers") \
            .select("*") \
            .limit(100) \
            .execute()

        if customers.data:
            st.dataframe(pd.DataFrame(customers.data))

    except Exception as e:
        st.error(e)

# ==========================================
# INVOICES
# ==========================================

elif menu == "الفواتير":

    st.title("🧾 الفواتير")

    try:

        invoices = supabase.table("sales") \
            .select("*") \
            .order("id", desc=True) \
            .limit(100) \
            .execute()

        if invoices.data:

            st.dataframe(
                pd.DataFrame(invoices.data),
                use_container_width=True
            )

    except Exception as e:
        st.error(e)

# ==========================================
# PAYMENTS
# ==========================================

elif menu == "المدفوعات":

    st.title("💳 المدفوعات")

    with st.form("payments_form"):

        customer_id = st.number_input("رقم العميل", min_value=1)

        payment_type = st.selectbox(
            "نوع العملية",
            ["receipt", "debt_collection"]
        )

        amount = st.number_input("المبلغ")

        notes = st.text_area("ملاحظات")

        submit = st.form_submit_button("حفظ")

        if submit:

            try:

                supabase.table("payments").insert({
                    "customer_id": customer_id,
                    "payment_type": payment_type,
                    "amount": amount,
                    "notes": notes
                }).execute()

                st.success("تم حفظ العملية")

            except Exception as e:
                st.error(e)

# ==========================================
# REPORTS
# ==========================================

elif menu == "التقارير":

    st.title("📈 التقارير")

    try:

        sales = supabase.table("sales") \
            .select("total_amount") \
            .execute()

        if sales.data:

            df = pd.DataFrame(sales.data)

            total_sales = df['total_amount'].sum()

            st.metric(
                label="إجمالي المبيعات",
                value=f"{total_sales:,.2f} ريال"
            )

            st.bar_chart(df['total_amount'])

    except Exception as e:
        st.error(e)
