from pydantic import BaseModel, EmailStr
#
class User(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr
    phone: str
    address: str



