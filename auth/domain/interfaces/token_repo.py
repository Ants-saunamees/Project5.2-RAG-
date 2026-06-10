from abc import ABC, abstractmethod
from auth.domain.entities.token import RefreshToken


class RefreshTokenRepository(ABC):

    @abstractmethod
    def save(self, token: RefreshToken) -> RefreshToken:
        """Persist a refresh token and return the saved entity."""
        pass

    @abstractmethod
    def find_by_token(self, token_str: str) -> RefreshToken | None:
        """Return a refresh token by its string value."""
        pass

    @abstractmethod
    def revoke(self, token: RefreshToken) -> None:
        """Mark a refresh token as revoked."""
        pass