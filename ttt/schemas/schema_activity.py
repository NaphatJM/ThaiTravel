from pydantic import BaseModel, ConfigDict
import decimal


class Activity_base_schema(BaseModel):
    user_id: int
    description: str
    province_id: int
    amount: decimal.Decimal

    model_config = ConfigDict(from_attributes=True)


class Activity_create_schema(Activity_base_schema):
    pass


class Activity_update_schema(BaseModel):
    user_id: int | None = None
    description: str | None = None
    province_id: int | None = None
    amount: decimal.Decimal | None = None

    model_config = ConfigDict(from_attributes=True)


class Activity_schema(Activity_base_schema):
    id: int
    tax_return: decimal.Decimal | None = None
