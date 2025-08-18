"""Authentication API schemas."""

from typing import ClassVar, Self

from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    EmailStr,
    model_validator,
)


class UserBase(BaseModel):
    """User base pydantic model."""

    email: EmailStr
    full_name: str


class User(UserBase):
    """User from orm model."""

    id: UUID4
    is_active: bool

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class UserRegister(UserBase):
    """User registration model."""

    password: str
    password_confirm: str

    @model_validator(mode="after")
    def _verify_password_match(self) -> Self:
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self


class UserLogin(BaseModel):
    """User login model."""

    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    """Login user response."""

    access_token: str
