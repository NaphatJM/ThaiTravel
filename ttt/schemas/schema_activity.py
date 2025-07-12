from pydantic import BaseModel
import decimal


class Activity_schema(BaseModel):
    id: int
    user_id: int
    description: str
    location: str
    amount: decimal.Decimal
    tax_return: decimal.Decimal | None = None
