from pydantic import BaseModel, ConfigDict
import decimal


class Activity_schema(BaseModel):
    id: int
    user_id: int
    description: str
    location: str
    amount: decimal.Decimal
    tax_return: decimal.Decimal | None = None

    model_config = ConfigDict(from_attributes=True)


class Activity_create_schema(Activity_schema):
    pass


class Activity_update_schema(Activity_schema):
    user_id: int | None = None
    description: str | None = None
    location: str | None = None
    amount: decimal.Decimal | None = None
    tax_return: decimal.Decimal | None = None

    model_config = ConfigDict(from_attributes=True)
