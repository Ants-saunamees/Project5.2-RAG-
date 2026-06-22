
from abc import ABC, abstractmethod
from auth.domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def save(self, user: User) -> User:
        """Persist a user and return the saved entity."""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        """Return a user by email or None if not found."""
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> User | None:
        """Return a user by ID or None if not found."""
        pass

    @abstractmethod
    def find_by_username(self, username: int) -> User | None:
        """Return a user by username or None if not found."""
        pass
