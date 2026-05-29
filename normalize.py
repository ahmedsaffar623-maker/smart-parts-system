# ==========================================
# تنظيف رقم القطعة
# ==========================================

def normalize_part_number(part_number: str):

    if not part_number:
        return ""

    normalized = (
        part_number
        .replace("-", "")
        .replace("_", "")
        .replace(" ", "")
        .replace(".", "")
        .replace("/", "")
        .upper()
        .strip()
    )

    return normalized


# ==========================================
# تنظيف رقم الشاصي VIN
# ==========================================

def normalize_vin(vin: str):

    if not vin:
        return ""

    vin = vin.upper().strip()

    # إزالة الفراغات
    vin = vin.replace(" ", "")

    # إزالة الرموز غير المطلوبة
    vin = vin.replace("-", "")
    vin = vin.replace("_", "")

    return vin


# ==========================================
# التحقق من VIN
# ==========================================

def validate_vin(vin: str):

    vin = normalize_vin(vin)

    # VIN يجب أن يكون 17 خانة

    if len(vin) != 17:

        return False

    # الأحرف الممنوعة عالمياً
    invalid_chars = ["I", "O", "Q"]

    for char in invalid_chars:

        if char in vin:

            return False

    return True


# ==========================================
# تنظيف النصوص
# ==========================================

def normalize_text(text: str):

    if not text:
        return ""

    return text.strip().upper()


# ==========================================
# تنظيف أرقام الجوال
# ==========================================

def normalize_phone(phone: str):

    if not phone:
        return ""

    phone = (
        phone
        .replace(" ", "")
        .replace("-", "")
        .replace("+", "")
    )

    return phone
