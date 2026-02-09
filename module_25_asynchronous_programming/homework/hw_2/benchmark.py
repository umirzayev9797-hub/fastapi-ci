import time
from async_cats import run_async
from thread_cats import run_threads
from process_cats import run_processes


COUNTS = [10, 50, 100]


def measure(fn, n):
    start = time.perf_counter()
    fn(n)
    end = time.perf_counter()

    dur = end - start
    speed = n / dur

    return dur, speed


def main():
    results = []

    for n in COUNTS:
        a = measure(run_async, n)
        t = measure(run_threads, n)
        p = measure(run_processes, n)

        results.append((n, a, t, p))

    print("\n# Markdown Table\n")
    print("| Count | Async (s) | Async img/s | Threads (s) | Thr img/s | Proc (s) | Proc img/s |")
    print("|------|-----------|------------|-------------|-----------|----------|-----------|")

    for n, a, t, p in results:
        print(
            f"| {n} | {a[0]:.2f} | {a[1]:.2f} | "
            f"{t[0]:.2f} | {t[1]:.2f} | "
            f"{p[0]:.2f} | {p[1]:.2f} |"
        )


if __name__ == "__main__":
    main()
