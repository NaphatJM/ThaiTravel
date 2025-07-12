from pydantic import BaseModel


class User(BaseModel):
    id: int
    full_name: str
    citizen_id: str
    email: str
    phone: str
    address: str
    is_admin: bool = False
