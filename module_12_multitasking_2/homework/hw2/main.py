import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_count(username: str) -> int:
    """
    Подсчет количества процессов пользователя.
    -u: фильтр по пользователю
    --no-headers: убираем заголовок, чтобы wc -l не посчитал лишнюю строку
    """
    try:
        command = f"ps -u {username} --no-headers | wc -l"
        output = subprocess.check_output(command, shell=True).decode().strip()
        return int(output)
    except subprocess.CalledProcessError:
        return 0


def total_memory_usage(root_pid: int) -> float:
    """
    Суммарное потребление памяти (%MEM) процесса и всех его потомков.
    Используем pgrep для поиска всех дочерних PID и ps для получения %mem.
    """
    try:
        # 1. Находим все дочерние процессы (включая рекурсию)
        # pgrep -d ',' -P <root_pid> найдет прямых потомков. 
        # Чтобы получить все дерево, нам нужно собрать все PID.

        command = "ps -ax -o pid=,ppid=,pmem="
        output = subprocess.check_output(command, shell=True).decode().splitlines()

        # Строим дерево в памяти Python для эффективности
        children_map = {}
        memory_map = {}

        for line in output:
            parts = line.split()
            if len(parts) == 3:
                pid, ppid, pmem = int(parts[0]), int(parts[1]), float(parts[2])
                memory_map[pid] = pmem
                children_map.setdefault(ppid, []).append(pid)

        # Рекурсивно собираем память начиная с root_pid
        def get_tree_memory(current_pid):
            total = memory_map.get(current_pid, 0.0)
            for child in children_map.get(current_pid, []):
                total += get_tree_memory(child)
            return total

        return round(get_tree_memory(root_pid), 2)

    except Exception as e:
        logger.error(f"Error calculating memory: {e}")
        return 0.0


def main():
    current_user = subprocess.check_output("whoami", shell=True).decode().strip()
    print(f"Количество процессов пользователя {current_user}: {process_count(current_user)}")

    print(f"Потребление памяти деревом PID 1: {total_memory_usage(1)}%")


if __name__ == "__main__":
    main()