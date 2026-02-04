import requests
import time
from concurrent.futures import ThreadPoolExecutor

class APITester:
    def __init__(self, base_url="http://127.0.0.1:5000/api/books", num_requests=10):
        self.base_url = base_url
        self.num_requests = num_requests

    def _single_request(self, session=None):
        try:
            if session:
                session.get(self.base_url, timeout=5)
            else:
                requests.get(self.base_url, timeout=5)
        except:
            pass # Игнорируем единичные сбои для чистоты замера времени

    def run_test(self, use_session=False, use_threads=False):
        start_time = time.time()
        if use_threads:
            with ThreadPoolExecutor(max_workers=20) as executor:
                if use_session:
                    with requests.Session() as s:
                        list(executor.map(lambda _: self._single_request(s), range(self.num_requests)))
                else:
                    list(executor.map(lambda _: self._single_request(), range(self.num_requests)))
        else:
            if use_session:
                with requests.Session() as s:
                    for _ in range(self.num_requests): self._single_request(s)
            else:
                for _ in range(self.num_requests): self._single_request()
        return round(time.time() - start_time, 4)

def execute_benchmarks(num_list):
    print(f"{'Кол-во':<10} | {'Сессия':<8} | {'Потоки':<8} | {'Время (сек)':<12}")
    print("-" * 45)
    for n in num_list:
        tester = APITester(num_requests=n)
        for s, t in [(False, False), (False, True), (True, False), (True, True)]:
            res = tester.run_test(use_session=s, use_threads=t)
            label_s = "+S" if s else "-S"
            label_t = "+T" if t else "-T"
            print(f"{n:<10} | {label_s:<8} | {label_t:<8} | {res:<12}")
            time.sleep(0.1) # Даем серверу "выдохнуть"
        print("-" * 45)

if __name__ == "__main__":
    execute_benchmarks([10, 100, 1000])