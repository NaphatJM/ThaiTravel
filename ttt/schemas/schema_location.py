from pydantic import BaseModel, ConfigDict


class province_schema(BaseModel):
    name: str
    code: str
    model_config = ConfigDict(from_attributes=True)


class taxReduction_schema(BaseModel):
    province_id: int
    tax_discount_percent: float
    model_config = ConfigDict(from_attributes=True)


class province_create_schema(province_schema):
    pass


class province_update_schema(province_schema):
    name: str | None = None
    code: str | None = None

    model_config = ConfigDict(from_attributes=True)


class taxReduction_create_schema(taxReduction_schema):
    pass


class taxReduction_update_schema(taxReduction_schema):
    province_id: int | None = None
    tax_discount_percent: float | None = None

    model_config = ConfigDict(from_attributes=True)
