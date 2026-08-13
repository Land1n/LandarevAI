from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

class GenericRepository(ABC, Generic[T]):
    """Абстрактный репозиторий для сущности типа T."""

    @abstractmethod
    def read_all(self) -> List[T]:
        """Вернуть все сущности типа T."""
        pass

    @abstractmethod
    def create(self, entity: T) -> bool:
        """Создать новую сущность. Вернуть True при успехе."""
        pass

    @abstractmethod
    def read_by_id(self, entity_id: int) -> Optional[T]:
        """Найти сущность по ID. Вернуть None, если не найдена."""
        pass

    @abstractmethod
    def update(self, entity_id: int, entity: T) -> bool:
        """Обновить сущность с заданным ID. Вернуть True при успехе."""
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Удалить сущность по ID. Вернуть True при успехе."""
        pass