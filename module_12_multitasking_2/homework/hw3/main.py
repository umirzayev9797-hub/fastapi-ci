from threading import Semaphore, Thread
import time
import sys

sem: Semaphore = Semaphore()


def fun1():
    while True:
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)


def fun2():
    while True:
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)


# Устанавливаем daemon=True при создании потоков
t1: Thread = Thread(target=fun1, daemon=True)
t2: Thread = Thread(target=fun2, daemon=True)

try:
    t1.start()
    t2.start()

    # Главный поток должен оставаться активным, чтобы ловить Ctrl+C.
    # Метод join() без таймаута блокирует сигнал в некоторых версиях Python,
    # поэтому используем цикл с коротким сном.
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Этот блок сработает только в главном потоке при нажатии Ctrl+C
    print('\nReceived keyboard interrupt, quitting threads.')
    # Поскольку t1 и t2 — демоны, они умрут здесь автоматически
    sys.exit(0)