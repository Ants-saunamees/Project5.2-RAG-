from auth.domain.entities.token import RefreshToken
from auth.domain.interfaces.token_repo import RefreshTokenRepository
from sqlalchemy.ext.asyncio import AsyncSession
from auth.infrastructure.db.token_model import RefreshTokenModel
from sqlalchemy import select
from auth.domain.services.token_services import create_refresh_token
from datetime import datetime, timedelta
from auth.domain.services.token_services import hash_token


class TokenRepoImpl(RefreshTokenRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, entity: RefreshToken):
        raw = entity.token
        hashed = hash_token(raw)

        model = RefreshTokenModel(
            user_id=entity.user_id,
            token=hashed,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
            revoked=False
        )

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        return RefreshToken(
            id=model.id,
            token=model.token,
            user_id=model.user_id,
            expires_at=model.expires_at,
            created_at=model.created_at,
            revoked=model.revoked
        )

    async def find_by_token(self, token_str: str):
        result = await self.session.execute(
            select(RefreshTokenModel).where(RefreshTokenModel.token == token_str)
        )
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return RefreshToken(
            id=model.id,
            user_id=model.user_id,
            token=model.token,
            expires_at=model.expires_at,
            created_at=model.created_at,
            revoked=model.revoked
        )

    async def revoke(self, token: RefreshToken):
        result = await self.session.execute(
            select(RefreshTokenModel).where(RefreshTokenModel.id == token.id)
        )
        model = result.scalar_one_or_none()

        if model is None:
            return None

        model.revoked = True
        await self.session.commit()
        await self.session.refresh(model)

        return RefreshToken(
            id=model.id,
            token=model.token,
            user_id=model.user_id,
            expires_at=model.expires_at,
            created_at=model.created_at,
            revoked=model.revoked
        )

    async def rotate_refresh_token(self, old_token: RefreshToken):
        # 1. Load DB model for the old token
        db_old = await self.session.get(RefreshTokenModel, old_token.id)
        db_old.revoked = True
        await self.session.commit()

        # 2. Generate new raw refresh token
        new_raw = create_refresh_token()
        new_hashed = hash_token(new_raw)

        # 3. Create new DB model
        db_new = RefreshTokenModel(
            user_id=old_token.user_id,
            token=new_hashed,
            expires_at=datetime.utcnow() + timedelta(days=30),
            created_at=datetime.utcnow(),
            revoked=False
        )

        self.session.add(db_new)
        await self.session.commit()
        await self.session.refresh(db_new)

        # 4. Convert DB model → domain entity
        new_entity = RefreshToken(
            id=db_new.id,
            user_id=db_new.user_id,
            token=db_new.token,
            expires_at=db_new.expires_at,
            created_at=db_new.created_at,
            revoked=db_new.revoked
        )

        return new_raw, new_entity

    async def validate_refresh(self, raw_token: str):
        """
        Validates a refresh token:
        - Must exist
        - Must match hashed token in DB
        - Must not be expired
        - Must not be used
        Returns the DB token record or None.
        """

        if not raw_token:
            print("token is none")
            return None

        hashed = hash_token(raw_token)

        result = await self.session.execute(
            select(RefreshTokenModel).where(
                RefreshTokenModel.token == hashed,
                RefreshTokenModel.expires_at > datetime.utcnow(),
                RefreshTokenModel.revoked == False
            )
        )

        record = result.scalar_one_or_none()

        if record is None:
            return None

        return RefreshToken(
            id=record.id,
            user_id=record.user_id,
            token=record.token,
            expires_at=record.expires_at,
            created_at=record.created_at,
            revoked=record.revoked
        )


