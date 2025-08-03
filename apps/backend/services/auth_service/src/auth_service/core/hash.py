"""Hashing logic."""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def compute_password_hash(password: str) -> str:
    """
    Return provided password hash.

    :param password: password string
    :return: hash of the provided password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify provided string password and hashed password.

    :param plain_password: plain string password
    :param hashed_password: hashed password (ex. from database)
    :return: is passwords match
    """
    return pwd_context.verify(plain_password, hashed_password)
