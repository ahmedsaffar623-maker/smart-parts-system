from app.database import supabase


# ==========================================
# تحديث المخزون
# ==========================================

def update_stock(
    part_number,
    quantity,
    movement_type,
    reference_type=None,
    reference_id=None,
    created_by=None
):

    # جلب القطعة

    part = supabase.table("parts") \
        .select("*") \
        .eq("part_number", part_number) \
        .execute()

    if not part.data:

        return {
            "success": False,
            "message": "PART NOT FOUND"
        }

    part_data = part.data[0]

    current_stock = part_data["current_stock"]

    # عمليات المخزون

    if movement_type == "purchase":

        new_stock = current_stock + quantity

    elif movement_type == "sale":

        new_stock = current_stock - quantity

    else:

        new_stock = current_stock

    # تحديث الكمية

    supabase.table("parts") \
        .update({
            "current_stock": new_stock
        }) \
        .eq("part_number", part_number) \
        .execute()

    # تسجيل الحركة

    supabase.table("inventory_movements") \
        .insert({

            "movement_type": movement_type,

            "reference_type": reference_type,

            "reference_id": reference_id,

            "part_number": part_number,

            "quantity": quantity,

            "quantity_before": current_stock,

            "quantity_after": new_stock,

            "created_by": created_by

        }) \
        .execute()

    return {

        "success": True,

        "part_number": part_number,

        "stock_before": current_stock,

        "stock_after": new_stock
    }