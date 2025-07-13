from sqlmodel import SQLModel, Field


class Province(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    code: str


class TaxReduction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    province_id: int | None = Field(default=None, foreign_key="province.id")
    tax_discount_percent: float
