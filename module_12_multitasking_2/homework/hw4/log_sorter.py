import threading
import requests
import time
import queue
import logging
from datetime import datetime

# Настройка базового логгера для вывода в консоль
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Приоритетная очередь для логов
# Хранит кортежи: (timestamp, "строка лога")
log_queue = queue.PriorityQueue()


def fetch_date_from_server(ts: int) -> str:
    """Делает запрос к локальному серверу для получения даты"""
    url = f"http://127.0.0.1:8080/timestamp/{ts}"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return response.text.strip()
    except Exception as e:
        return f"Error: {e}"
    return "N/A"


class LogWorker(threading.Thread):
    def __init__(self, thread_id: int):
        super().__init__(name=f"Worker-{thread_id}")
        self.daemon = True

    def run(self):
        logger.info(f"Thread {self.name} started.")
        # Каждый поток работает 20 секунд
        for _ in range(20):
            # 1. Получаем timestamp непосредственно перед запросом
            current_ts = int(time.time())

            # 2. Получаем дату с сервера
            formatted_date = fetch_date_from_server(current_ts)

            # 3. Кладем в приоритетную очередь (автоматическая сортировка по ts)
            log_entry = f"{current_ts} {formatted_date}"
            log_queue.put((current_ts, log_entry))

            # 4. Пишем раз в секунду
            time.sleep(1)
        logger.info(f"Thread {self.name} finished.")


def file_writer():
    """Поток, который забирает логи из очереди и пишет в файл"""
    with open('sorted_logs.txt', 'a', encoding='utf-8') as f:
        while True:
            # Получаем элемент с наименьшим timestamp
            # Если очередь пуста, ждем
            try:
                ts, entry = log_queue.get(timeout=5)
                f.write(entry + '\n')
                f.flush()  # Принудительно сбрасываем в файл
                log_queue.task_done()
            except queue.Empty:
                # Если 5 секунд ничего нет, считаем, что все закончили
                break


def main():
    # 1. Запускаем поток для записи в файл
    writer_thread = threading.Thread(target=file_writer, daemon=True)
    writer_thread.start()

    # 2. Запускаем 10 потоков с интервалом в 1 секунду
    workers = []
    for i in range(1, 11):
        worker = LogWorker(thread_id=i)
        worker.start()
        workers.append(worker)
        time.sleep(1)  # Интервал запуска согласно условию

    # 3. Ждем завершения всех рабочих потоков
    for worker in workers:
        worker.join()

    # 4. Ждем, пока очередь допишется в файл
    log_queue.join()
    logger.info("All logs are processed and saved to sorted_logs.txt")


if __name__ == "__main__":
    main()