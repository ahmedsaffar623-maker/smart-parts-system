from app.database import supabase
from app.utils.normalize import normalize_vin


# ==========================================
# البحث بالشاصي
# ==========================================

def search_vehicle_by_vin(vin: str):

    vin = normalize_vin(vin)

    # التحقق من طول الشاصي

    if len(vin) != 17:

        return {
            "success": False,
            "message": "VIN MUST BE 17 CHARACTERS"
        }

    # البحث عن السيارة

    vehicle = supabase.table("vehicles") \
        .select("*") \
        .eq("vin_number", vin) \
        .execute()

    # إذا لم يتم العثور

    if not vehicle.data:

        return {
            "success": False,
            "message": "VIN NOT FOUND"
        }

    vehicle_data = vehicle.data[0]

    # جلب الكتالوج

    catalog = supabase.table("model_catalogs") \
        .select("*") \
        .eq("model_name", vehicle_data["model_name"]) \
        .execute()

    # جلب القطع المرتبطة بالموديل

    parts = supabase.table("parts") \
        .select("*") \
        .eq("model_name", vehicle_data["model_name"]) \
        .limit(200) \
        .execute()

    return {

        "success": True,

        "vehicle": {
            "vin_number": vehicle_data["vin_number"],
            "model_name": vehicle_data["model_name"],
            "mtoc": vehicle_data["mtoc"]
        },

        "catalog": catalog.data,

        "parts": parts.data
    }