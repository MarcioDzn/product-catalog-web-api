from datetime import datetime

import phonenumbers
from pydantic import BaseModel, EmailStr, field_validator


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        try:
            phone = phonenumbers.parse(value, "BR")
        except phonenumbers.NumberParseException:
            raise ValueError("Número de telefone inválido")

        if not phonenumbers.is_valid_number(phone):
            raise ValueError("Número de telefone inválido")

        return phonenumbers.format_number(
            phone,
            phonenumbers.PhoneNumberFormat.E164,
        )


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    phone: str | None = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str | None) -> str | None:
        if value is None:
            return None

        try:
            phone = phonenumbers.parse(value, "BR")
        except phonenumbers.NumberParseException:
            raise ValueError("Número de telefone inválido")

        if not phonenumbers.is_valid_number(phone):
            raise ValueError("Número de telefone inválido")

        return phonenumbers.format_number(
            phone,
            phonenumbers.PhoneNumberFormat.E164,
        )


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
