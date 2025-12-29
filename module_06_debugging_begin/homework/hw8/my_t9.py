"""
У нас есть кнопочный телефон (например, знаменитая Nokia 3310), и мы хотим,
чтобы пользователь мог проще отправлять СМС. Реализуем своего собственного клавиатурного помощника.

Каждой цифре телефона соответствует набор букв:
* 2 — a, b, c;
* 3 — d, e, f;
* 4 — g, h, i;
* 5 — j, k, l;
* 6 — m, n, o;
* 7 — p, q, r, s;
* 8 — t, u, v;
* 9 — w, x, y, z.

Пользователь нажимает на клавиши, например 22736368, после чего на экране печатается basement.

Напишите функцию my_t9, которая принимает на вход строку, состоящую из цифр 2–9,
и возвращает список слов английского языка, которые можно получить из этой последовательности цифр.
"""
import re
from typing import List

# соответствие цифр буквам
digit_to_letters = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


def my_t9(input_numbers: str) -> List[str]:
    # составляем регулярное выражение для поиска слов
    pattern = ""
    for digit in input_numbers:
        letters = digit_to_letters.get(digit, "")
        pattern += f"[{letters}]"

    regex = re.compile(f"^{pattern}$", re.IGNORECASE)

    words_found = []

    # читаем словарь
    with open("/usr/share/dict/words", "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if len(word) != len(input_numbers):
                continue
            if regex.match(word):
                words_found.append(word.lower())

    return words_found


if __name__ == "__main__":
    numbers: str = input("Введите последовательность цифр (2-9): ")
    words: List[str] = my_t9(numbers)
    print(*words, sep="\n")

