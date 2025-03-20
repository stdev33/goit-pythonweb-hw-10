from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: Optional[date] = None
    additional_info: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

    class Config:
        from_attributes = True
