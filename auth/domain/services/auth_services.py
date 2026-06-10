from passlib.context import CryptContext
import re

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)
def hash(text: str) -> str:
    return pwd_context.hash(text)

def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)

def is_email(value: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", value) is not None

