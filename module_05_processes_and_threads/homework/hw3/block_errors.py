"""
Реализуйте контекстный менеджер, который будет игнорировать переданные типы исключений, возникающие внутри блока with.
Если выкидывается неожидаемый тип исключения, то он прокидывается выше.
"""

from typing import Collection, Type, Literal
from types import TracebackType


class BlockErrors:
    def __init__(self, errors: Collection[Type[BaseException]]) -> None:
        # Сохраняем допустимые типы исключений
        self.allowed_errors = tuple(errors)

    def __enter__(self) -> None:
        # Ничего не делаем при входе в контекст
        return None

    def __exit__(
        self,
        raised_exception_type: Type[BaseException] | None,
        raised_exception_value: BaseException | None,
        raised_traceback: TracebackType | None
    ) -> Literal[True] | None:

        # Если исключения не было — просто выходим
        if raised_exception_type is None:
            return None

        # Если тип исключения входит в разрешённые или является дочерним — подавляем
        if issubclass(raised_exception_type, self.allowed_errors):
            return True  # True = подавить исключение

        # Иначе — не подавляем (исключение пойдёт наружу)
        return None
