from typing import Union, List

Number = Union[int, float, complex]


def find_insert_position(nums: List[Number], x: Number) -> int:
    # Инициализируем границы поиска
    low = 0
    high = len(nums)

    # Бинарный поиск: делим массив пополам на каждой итерации
    while low < high:
        mid = (low + high) // 2
        # Если x больше или равен текущему элементу,
        # значит позиция вставки находится правее
        if nums[mid] < x:
            low = mid + 1
        else:
            # Иначе позиция вставки слева или здесь
            high = mid

    return low

if __name__ == "__main__":
    # Пример из задания
    A = [1, 2, 3, 3, 3, 5]
    x = 4
    pos = find_insert_position(A, x)
    print(f"Позиция для 4 в {A}: {pos}")

    # Крайние случаи
    print(f"Пустой массив: {find_insert_position([], 10)}")
    print(f"В начало: {find_insert_position([10, 20], 5)}")
    print(f"В конец: {find_insert_position([10, 20], 30)}")