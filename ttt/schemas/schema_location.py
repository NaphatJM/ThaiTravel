from pydantic import BaseModel, ConfigDict


# ---------- Province Schemas ----------


# ✅ Base schema (ใช้ภายในเท่านั้น ไม่ส่งออก)
class ProvinceBase(BaseModel):
    name: str
    code: str
    model_config = ConfigDict(from_attributes=True)


# ✅ สำหรับสร้าง (ไม่มี id)
class province_create_schema(ProvinceBase):
    pass


# ✅ สำหรับอัปเดต (optional fields)
class province_update_schema(ProvinceBase):
    name: str | None = None
    code: str | None = None
    model_config = ConfigDict(from_attributes=True)


# ✅ สำหรับตอบกลับ (response model มี id)
class province_schema(ProvinceBase):
    id: int


# ---------- TaxReduction Schemas ----------


class TaxReductionBase(BaseModel):
    tax_discount_percent: float
    model_config = ConfigDict(from_attributes=True)


# ✅ สำหรับสร้าง (ไม่ต้องส่ง id)
class taxReduction_create_schema(TaxReductionBase):
    province_id: int


# ✅ สำหรับอัปเดต (optional fields)
class taxReduction_update_schema(BaseModel):
    province_id: int | None = None
    tax_discount_percent: float | None = None
    model_config = ConfigDict(from_attributes=True)


# ✅ สำหรับตอบกลับ
class taxReduction_schema(TaxReductionBase):
    id: int
    province_id: int
