import threading
import queue
import time
import random
from typing import Any


class Task:
    def __init__(self, priority: int, func: Any, *args: Any) -> None:
        self.priority = priority
        self.func = func
        self.args = args

    # Добавляем метод сравнения "меньше чем"
    def __lt__(self, other):
        # Если приоритеты равны, нам все равно, кто меньше
        # Если не равны, сравниваем по значению приоритета
        return self.priority < other.priority

    def __repr__(self) -> str:
        # Ограничим вывод аргумента до 3 знаков после запятой
        return f"Task(priority={self.priority}).\tsleep({round(self.args[0], 3)})"

    def execute(self) -> None:
        self.func(*self.args)


class Producer(threading.Thread):
    def __init__(self, queue: queue.PriorityQueue) -> None:
        super().__init__()
        self.queue = queue

    def run(self) -> None:
        print("Producer: Running")
        # Генерируем 10 случайных задач
        for _ in range(10):
            priority = random.randint(0, 10)
            sleep_time = random.random()
            task = Task(priority, time.sleep, sleep_time)

            # В PriorityQueue кладем кортеж (приоритет, объект)
            self.queue.put((priority, task))

        print("Producer: Done")


class Consumer(threading.Thread):
    def __init__(self, queue: queue.PriorityQueue) -> None:
        super().__init__()
        self.queue = queue

    def run(self) -> None:
        print("Consumer: Running")
        while True:
            try:
                # Извлекаем кортеж (priority, task)
                # timeout нужен, чтобы поток не завис, если данных нет
                priority, task = self.queue.get(timeout=1)

                print(f">running {task}")
                task.execute()

                # Помечаем выполнение
                self.queue.task_done()
            except queue.Empty:
                # Если очередь пуста в течение секунды — заканчиваем
                break
        print("Consumer: Done")


def main() -> None:
    q = queue.PriorityQueue()

    producer = Producer(q)
    consumer = Consumer(q)

    # По условию: сначала Producer добавляет все задачи
    producer.start()
    producer.join()

    # Затем Consumer их выполняет
    consumer.start()
    consumer.join()


if __name__ == "__main__":
    main()