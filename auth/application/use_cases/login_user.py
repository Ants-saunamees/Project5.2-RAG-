from datetime import timedelta, datetime
from auth.domain.services.auth_services import verify_password
from auth.domain.entities.token import RefreshToken
from auth.domain.services.token_services import create_refresh_token, create_access_token
from auth.domain.interfaces.user_repo import UserRepository
from auth.domain.interfaces.token_repo import RefreshTokenRepository
from auth.domain.services.auth_services import is_email, prehash


class LoginUserUseCase:
    def __init__(self, user_repo: UserRepository, token_repo: RefreshTokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def execute(self, identifier: str, password: str):
        identifier = identifier.lower()

        # 1. Decide email or username
        if is_email(identifier):
            user = await self.user_repo.find_by_email(identifier)
        else:
            user = await self.user_repo.find_by_username(identifier)

        # 2. User not found
        if not user:
            raise Exception("Invalid credentials")

        # 3. Password check
        if not verify_password(prehash(password), user.password_hash):
            raise Exception("Invalid credentials")

        access_token = create_access_token({
            "user_id": user.id
        })

        # 5. Create refresh token
        refresh_token_entity = RefreshToken.create(user.id)

        await self.token_repo.save(refresh_token_entity)
        # 7. Return result
        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token_entity.token
        }




