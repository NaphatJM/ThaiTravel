from pydantic import BaseModel
import datetime


class User(BaseModel):
    id: int
    full_name: str
    citizen_id: str
    email: str
    phone: str
    address: str
