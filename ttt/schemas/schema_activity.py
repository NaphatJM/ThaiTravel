from pydantic import BaseModel, ConfigDict
import decimal


class Activity_schema(BaseModel):
    user_id: int
    description: str
    province_id: int
    amount: decimal.Decimal
    tax_return: decimal.Decimal | None = None

    model_config = ConfigDict(from_attributes=True)


class Activity_create_schema(Activity_schema):
    pass


class Activity_update_schema(Activity_schema):
    user_id: int | None = None
    description: str | None = None
    province_id: int | None = None
    amount: decimal.Decimal | None = None
    tax_return: decimal.Decimal | None = None

    model_config = ConfigDict(from_attributes=True)
