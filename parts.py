from fastapi import APIRouter
from app.database import supabase
from app.utils.normalize import normalize_part_number

router = APIRouter()


# ==========================================
# البحث برقم القطعة
# ==========================================

@router.get("/search-part/{part_number}")
def search_part(part_number: str):

    normalized = normalize_part_number(part_number)

    result = supabase.table("parts") \
        .select("*") \
        .eq("normalized_part_number", normalized) \
        .execute()

    return result.data


# ==========================================
# جلب جميع القطع
# ==========================================

@router.get("/parts")
def get_parts():

    result = supabase.table("parts") \
        .select("*") \
        .limit(1000) \
        .execute()

    return result.data


# ==========================================
# القطع الناقصة
# ==========================================

@router.get("/low-stock-parts")
def low_stock_parts():

    result = supabase.table("low_stock_view") \
        .select("*") \
        .execute()

    return result.data