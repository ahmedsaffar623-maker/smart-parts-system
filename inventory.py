from fastapi import APIRouter
from app.database import supabase

router = APIRouter()


# ==========================================
# عرض المخزون
# ==========================================

@router.get("/inventory")
def inventory_list():

    result = supabase.table("parts") \
        .select("*") \
        .limit(1000) \
        .execute()

    return result.data


# ==========================================
# حركة المخزون
# ==========================================

@router.get("/inventory-movements")
def inventory_movements():

    result = supabase.table("inventory_movements") \
        .select("*") \
        .order("created_at", desc=True) \
        .limit(500) \
        .execute()

    return result.data