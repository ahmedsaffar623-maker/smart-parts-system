from fastapi import APIRouter
from app.database import supabase

router = APIRouter()


# ==========================================
# جميع العملاء
# ==========================================

@router.get("/customers")
def customers():

    result = supabase.table("customers") \
        .select("*") \
        .limit(1000) \
        .execute()

    return result.data


# ==========================================
# عملاء الورش
# ==========================================

@router.get("/workshops")
def workshops():

    result = supabase.table("customers") \
        .select("*") \
        .eq("customer_type", "workshop") \
        .execute()

    return result.data


# ==========================================
# عملاء الأفراد
# ==========================================

@router.get("/individual-customers")
def individual_customers():

    result = supabase.table("customers") \
        .select("*") \
        .eq("customer_type", "individual") \
        .execute()

    return result.data