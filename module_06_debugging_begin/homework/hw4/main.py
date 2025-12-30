"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
import json
from collections import Counter, defaultdict
from typing import Dict

LOG_FILE = "skillbox_json_messages.log"

# --- считываем файл только один раз ---
logs = []
with open(LOG_FILE, "r", encoding="utf-8") as f:
    for line in f:
        try:
            logs.append(json.loads(line))
        except json.JSONDecodeError:
            continue  # пропускаем некорректные строки, если есть

# --- создаём структуры для быстрого анализа ---
levels_count = Counter()        # для task1
hours_count = Counter()         # для task2
critical_05 = 0                 # для task3
dog_count = 0                   # для task4
warning_words = Counter()       # для task5

for log in logs:
    msg = log.get("message", "")
    level = log.get("level", "")
    time = log.get("time", "00:00:00")

    # 1. Счётчик уровней
    levels_count[level] += 1

    # 2. Счётчик по часам
    hour = int(time.split(":")[0])
    hours_count[hour] += 1

    # 3. CRITICAL в интервале 05:00:00 - 05:20:00
    if level == "CRITICAL":
        h, m, s = map(int, time.split(":"))
        if h == 5 and 0 <= m <= 20:
            critical_05 += 1

    # 4. Сообщения с dog
    if "dog" in msg.lower():
        dog_count += 1

    # 5. Слова в сообщениях уровня WARNING
    if level == "WARNING":
        words = [w.lower() for w in msg.split() if w.isalpha()]
        warning_words.update(words)

# --- функции для каждой задачи ---
def task1() -> Dict[str, int]:
    return dict(levels_count)

def task2() -> int:
    return hours_count.most_common(1)[0][0]

def task3() -> int:
    return critical_05

def task4() -> int:
    return dog_count

def task5() -> str:
    if warning_words:
        return warning_words.most_common(1)[0][0]
    return ""

# --- запуск ---
if __name__ == '__main__':
    tasks = (task1, task2, task3, task4, task5)
    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')

