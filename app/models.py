from typing import Any, Dict, Optional


class BaseItem:
    """Базовый класс для всех моделей."""

    def __init__(self, id_num: int) -> None:
        self.__id_num: int = id_num

    @property
    def id_num(self) -> int:
        """Геттер для ID."""
        return self.__id_num


class Task(BaseItem):
    """Класс задачи с инкапсуляцией и типизацией."""

    def __init__(
        self,
        id_num: int,
        title: str,
        description: Optional[str] = None
    ) -> None:
        super().__init__(id_num)
        self.__title: str = title
        self.__description: Optional[str] = description

    @property
    def title(self) -> str:
        """Геттер для заголовка."""
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        """Сеттер для заголовка."""
        if not value:
            raise ValueError("Title cannot be empty")
        self.__title = value

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь."""
        return {
            "id": self.id_num,
            "title": self.__title,
            "description": self.__description
        }