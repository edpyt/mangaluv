from typing import TypedDict


class CreateUserData(TypedDict):
    email: str
    username: str
    password: str
    password_confirm: str
