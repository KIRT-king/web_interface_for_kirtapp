from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    name: str
    lastname: str
    post: str
    email: str
    phone_number: str
    status: str
    last_check: str