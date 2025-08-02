"""Authentication API schemas."""

from typing import Self

from pydantic import BaseModel, EmailStr, model_validator


class UserBase(BaseModel):
    """User base pydantic model."""

    email: EmailStr
    full_name: str


class UserRegister(UserBase):
    """User registration model."""

    password: str
    password_confirm: str

    @model_validator(mode="after")
    def _verify_password_match(self) -> Self:
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self
