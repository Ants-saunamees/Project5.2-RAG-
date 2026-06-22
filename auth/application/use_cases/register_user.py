from auth.domain.entities.user import User
from auth.domain.interfaces.user_repo import UserRepository
from auth.domain.rules.password_rules import validate_password
from auth.domain.services.token_services import create_access_token, create_refresh_token
from auth.domain.entities.token import RefreshToken
from datetime import datetime, timedelta


class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepository, token_repo):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def execute(self, username: str, email: str, password: str, department: str):
        email = email.lower()

        # 1. Validate password (raise if invalid)
        validate_password(password)

        # 2. Check if user already exists
        existing_email = await self.user_repo.find_by_email(email)
        if existing_email:
            raise Exception("Email already in use")

        existing_username = await self.user_repo.find_by_username(username)
        if existing_username:
            raise Exception("Username already in use")

        # 3. Create user entity
        user = User.create(username, email, password, department)
        user = await self.user_repo.save(user)

        # 4. Create access token
        access_token = create_access_token({"user_id": user.id})

        refresh_token_entity = RefreshToken.create(user.id)

        await self.token_repo.save(refresh_token_entity)

        # 6. Return success result (domain use case returns data, not JSON)
        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token_entity.token,
        }
