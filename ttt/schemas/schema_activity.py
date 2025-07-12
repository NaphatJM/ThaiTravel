from pydantic import BaseModel
import decimal


class Activity(BaseModel):
    id: int
    user_id: int
    description: str
    location: str
    amount: decimal.Decimal
    tax_return: decimal.Decimal | None = None
