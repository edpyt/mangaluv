from typing import TypedDict


class CreateUserData(TypedDict):
    email: str
    full_name: str
    password: str
    password_confirm: str
