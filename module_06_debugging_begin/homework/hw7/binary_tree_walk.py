"""
Помимо того чтобы логи писать, нужно их ещё и уметь читать,
иначе мы будем как в известном анекдоте, писателями, а не читателями.

Для вас мы написали простую функцию обхода binary tree по уровням.
Также в репозитории есть файл с логами, написанными этой программой.

Напишите функцию restore_tree, которая принимает на вход путь до файла с логами
    и восстанавливать исходное BinaryTree.

Функция должна возвращать корень восстановленного дерева

def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    pass

Примечание: гарантируется, что все значения, хранящиеся в бинарном дереве уникальны
"""
import itertools
import logging
import random
import re
from collections import deque
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("tree_walk")


@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"


def walk(root: BinaryTreeNode):
    queue = deque([root])

    while queue:
        node = queue.popleft()

        logger.info(f"Visiting {node!r}")

        if node.left:
            logger.debug(
                f"{node!r} left is not empty. Adding {node.left!r} to the queue"
            )
            queue.append(node.left)

        if node.right:
            logger.debug(
                f"{node!r} right is not empty. Adding {node.right!r} to the queue"
            )
            queue.append(node.right)


counter = itertools.count(random.randint(1, 10 ** 6))


def get_tree(max_depth: int, level: int = 1) -> Optional[BinaryTreeNode]:
    if max_depth == 0:
        return None

    node_left = get_tree(max_depth - 1, level=level + 1)
    node_right = get_tree(max_depth - 1, level=level + 1)
    node = BinaryTreeNode(val=next(counter), left=node_left, right=node_right)

    return node


def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    """
    Восстанавливает бинарное дерево по логам BFS.
    Логи имеют формат: "INFO:Visiting <BinaryTreeNode[val]>"
    Гарантируется уникальность значений.
    """
    node_map = {}
    parent_queue = deque()
    root = None

    with open(path_to_log_file, "r", encoding="utf-8") as f:
        for line in f:
            m = re.search(r"<BinaryTreeNode\[(\d+)\]>", line)
            if not m:
                continue
            val = int(m.group(1))
            node = BinaryTreeNode(val=val)
            node_map[val] = node

            if not root:
                root = node
                parent_queue.append(node)
                continue

            while parent_queue:
                parent = parent_queue[0]
                if not parent.left:
                    parent.left = node
                    break
                elif not parent.right:
                    parent.right = node
                    parent_queue.popleft()
                    break
                else:
                    parent_queue.popleft()

            parent_queue.append(node)

    return root


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(message)s",
        filename="walk_log_4.txt",
    )

    # создаём дерево и логируем обход
    root = get_tree(7)
    walk(root)

    # пример восстановления дерева из логов
    restored_root = restore_tree("walk_log_4.txt")
    print("Восстановленное дерево корень:", restored_root)

