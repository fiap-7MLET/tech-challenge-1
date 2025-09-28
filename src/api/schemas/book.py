from pydantic import BaseModel
from typing import Optional

class BookSchema(BaseModel):
    id: Optional[int]
    title: str
    price: float
    rating: int
    availability: bool
    category: str
    image: Optional[str]

    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    id: Optional[int]
    email: str
    password: str

    class Config:
        orm_mode = True
