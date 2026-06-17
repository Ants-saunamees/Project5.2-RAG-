from passlib.context import CryptContext
import re
import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def prehash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def is_email(value: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", value) is not None

