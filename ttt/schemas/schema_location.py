from pydantic import BaseModel


class province(BaseModel):
    id: int
    name: str
    code: str


class taxReduction(BaseModel):
    id: int
    province_id: int
    tax_discount_percent: float
