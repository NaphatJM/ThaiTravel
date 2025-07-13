from sqlmodel import SQLModel, Field, Relationship

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .model_activity import Activity


class Province(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    code: str
    activities: list["Activity"] = Relationship(back_populates="province")
    tax_reductions: Optional["TaxReduction"] = Relationship(
        back_populates="province", sa_relationship_kwargs={"uselist": False}
    )


class TaxReduction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    province_id: int | None = Field(default=None, foreign_key="province.id")
    tax_discount_percent: float

    province: "Province" = Relationship(back_populates="tax_reductions")
