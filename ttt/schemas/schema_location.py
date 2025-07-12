from pydantic import BaseModel


class province_schema(BaseModel):
    id: int
    name: str
    code: str


class taxReduction_schema(BaseModel):
    id: int
    province_id: int
    tax_discount_percent: float
