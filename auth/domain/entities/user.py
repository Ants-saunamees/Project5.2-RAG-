from auth.domain.services.auth_services import hash

class User:
    def __init__(self, id: int | None, username: str, email: str, password_hash: str):
        if "@" not in email:
            raise ValueError("Invalid email")

        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def create(username, email: str, raw_password: str):
        hashed = hash(raw_password)

        return User(
            id=None,
            username=username,
            email=email,
            password_hash=hashed,
        )
