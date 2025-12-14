"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys
from typing import List


def get_mean_size(ls_output_lines: List[str]) -> float:
    total_size = 0
    file_count = 0

    # Итерируемся по каждой строке, которая представляет файл/директорию
    for line in ls_output_lines:
        line = line.strip()  # Удаляем лишние пробелы и символы новой строки
        if not line:
            continue  # Пропускаем пустые строки

        columns = line.split()

        # Проверка минимального количества колонок для безопасного доступа к элементам
        # В выводе ls -l обычно 9 колонок.
        if len(columns) < 9:
            continue

        if not columns[0].startswith('-'):
            continue

        # Получение размера файла. Это 5-я колонка (индекс 4)
        try:
            size = int(columns[4])
        except ValueError:
            # Пропускаем строки, где 5-я колонка не является числом (что маловероятно для ls -l)
            continue

        total_size += size
        file_count += 1

    # Обработка случая, когда файлов нет
    if file_count == 0:
        return 0.0

    return total_size / file_count


if __name__ == '__main__':
    lines = sys.stdin.readlines()

    if lines and lines[0].startswith('total'):
        data_lines = lines[1:]
    else:
        data_lines = lines

    mean_size = get_mean_size(data_lines)
    print(mean_size)