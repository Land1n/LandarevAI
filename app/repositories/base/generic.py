from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional,Tuple

from app.core.logger.schemas.answer import Answer

T = TypeVar('T')

class GenericRepository(ABC, Generic[T]):
    """Абстрактный репозиторий для сущности типа T."""

    @abstractmethod
    def _model_class(self) -> type:
        """Возвращает класс модели. По умолчанию берётся из параметра типа, но для runtime нужно переопределить."""
        raise NotImplementedError("Subclasses must define _model_class() or override methods")

    @abstractmethod
    def read_all(self) -> Answer[T]:
        """Вернуть все сущности типа T."""
        pass

    @abstractmethod
    def create(self, entity: T) -> Answer[T]:
        """Создать новую сущность. Вернуть True при успехе."""
        pass

    @abstractmethod
    def read_by_id(self, id: int) -> Answer[T]:
        """Найти сущность по ID. Вернуть None, если не найдена."""
        pass

    @abstractmethod
    def update(self, id: int, entity: T) -> Answer[T]:
        """Обновить сущность с заданным ID. Вернуть True при успехе."""
        pass

    @abstractmethod
    def delete(self, id: int) -> Answer[T]:
        """Удалить сущность по ID. Вернуть True при успехе."""
        pass