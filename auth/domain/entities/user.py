from auth.domain.services.auth_services import hash_password, prehash

class User:
    def __init__(self, id: int | None, username: str, email: str, password_hash: str):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def create(username: str, email: str, raw_password: str):
        hashed = hash_password(prehash(raw_password))

        return User(
            id=None,
            username=username,
            email=email,
            password_hash=hashed,
        )
