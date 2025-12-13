"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""


def get_summary_rss(ps_output_file_path: str) -> str:
    total_bytes = 0

    with open(ps_output_file_path, 'r') as output_file:
        lines = output_file.readlines()[1:]  # пропускаем заголовок

        for line in lines:
            columns = line.split()
            rss_kb = int(columns[5])          # RSS в килобайтах
            total_bytes += rss_kb * 1024      # перевод в байты

    units = ['B', 'KiB', 'MiB', 'GiB', 'TiB']
    unit_index = 0

    while total_bytes >= 1024 and unit_index < len(units) - 1:
        total_bytes //= 1024
        unit_index += 1

    return f'{total_bytes} {units[unit_index]}'


if __name__ == '__main__':
    path: str = 'output_file.txt'
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
