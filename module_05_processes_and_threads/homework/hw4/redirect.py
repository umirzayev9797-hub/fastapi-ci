"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""
import sys
import traceback
import types
from typing import IO, Optional, Type

class Redirect:
    def __init__(self, *, stdout: Optional[IO] = None, stderr: Optional[IO] = None) -> None:
        self.target_stdout = stdout
        self.target_stderr = stderr
        self.previous_stdout = None
        self.previous_stderr = None

    def __enter__(self):
        self.previous_stdout = sys.stdout
        self.previous_stderr = sys.stderr

        if self.target_stdout is not None:
            sys.stdout = self.target_stdout

        if self.target_stderr is not None:
            sys.stderr = self.target_stderr

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[types.TracebackType]
    ) -> bool:
        if exc_type is not None and self.target_stderr is not None:
            # Записываем ошибку в файл, если он был передан
            self.target_stderr.write(traceback.format_exc())

        # Возвращаем стандартные потоки в исходное состояние
        sys.stdout = self.previous_stdout
        sys.stderr = self.previous_stderr

        # Возвращаем False, чтобы исключение пробрасывалось дальше
        return False

# --- Блок проверки ---
if __name__ == '__main__':
    print('Hello stdout')
    stdout_file = open('stdout.txt', 'w', encoding='utf-8')
    stderr_file = open('stderr.txt', 'w', encoding='utf-8')

    try:
        with Redirect(stdout=stdout_file, stderr=stderr_file):
            print('Hello stdout.txt')
            raise Exception('Hello stderr.txt')
    except Exception:
        # Ловим ошибку здесь, чтобы код пошел дальше к финальному принту
        pass

    stdout_file.close()
    stderr_file.close()

    print('Hello stdout again')
    raise Exception('Hello stderr')