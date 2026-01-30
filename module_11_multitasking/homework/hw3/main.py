import logging
import random
import threading
import time
from typing import List

# Константы для контроля завершения
TOTAL_TICKETS: int = 10
MAX_TICKETS_TO_PRINT: int = 30  # Общий лимит билетов на весь день
TICKETS_PRINTED_TOTAL: int = 10  # Сколько уже "выпущено" (начальные 10)
NUM_SELLERS: int = 4

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger: logging.Logger = logging.getLogger(__name__)


class Seller(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_sold: int = 0

    def run(self) -> None:
        global TOTAL_TICKETS
        while True:
            # Спим ВНЕ семафора, чтобы дать шанс другим (включая директора)
            time.sleep(random.random())

            with self.sem:
                if TOTAL_TICKETS <= 0:
                    # Если билетов нет И директор больше не печатает (это проверит директор)
                    break

                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.name} sold one; {TOTAL_TICKETS} left')

        logger.info(f'Seller {self.name} finished. Total sold: {self.tickets_sold}')


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore

    def run(self) -> None:
        global TOTAL_TICKETS, TICKETS_PRINTED_TOTAL

        # Директор работает, пока не напечатает лимит билетов
        while TICKETS_PRINTED_TOTAL < MAX_TICKETS_TO_PRINT:
            time.sleep(0.1)  # Частая проверка остатка

            # Условие: если билетов мало
            if TOTAL_TICKETS <= NUM_SELLERS:
                with self.sem:
                    # Проверяем, не напечатали ли мы уже максимум
                    if TICKETS_PRINTED_TOTAL < MAX_TICKETS_TO_PRINT:
                        to_add = 10
                        TOTAL_TICKETS += to_add
                        TICKETS_PRINTED_TOTAL += to_add
                        logger.info(f'--- Director added {to_add} tickets. Total in stock: {TOTAL_TICKETS} ---')
                        time.sleep(0.5)  # Имитация работы станка


def main() -> None:
    # Семафор с 1 разрешением работает как мьютекс
    semaphore: threading.Semaphore = threading.Semaphore(1)

    # Создаем Директора
    director = Director(semaphore)
    director.start()

    # Создаем Продавцов
    sellers: List[Seller] = [Seller(semaphore) for _ in range(NUM_SELLERS)]
    for s in sellers:
        s.start()

    # Ожидаем только продавцов. Когда они закончат — программа завершится
    for s in sellers:
        s.join()

    logger.info('!!! All tickets in the city are sold out. Cinema closed !!!')


if __name__ == '__main__':
    main()