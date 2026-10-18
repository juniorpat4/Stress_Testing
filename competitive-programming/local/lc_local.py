"""Solo local: LeetCode ya define TreeNode y ListNode.

Literales LeetCode ("[1,null,2]") <-> estructuras. Los literales son JSON, así que
el parseo es json.loads y la salida json.dumps compacto.
"""

from __future__ import annotations

import json
from collections import deque
from typing import Any, Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val: int = 0, left: Optional[TreeNode] = None, right: Optional[TreeNode] = None) -> None:
        self.val = val
        self.left = left
        self.right = right


def dumps(value: Any) -> str:
    """Salida en formato LeetCode: [1,null,2], true, "abc"."""
    return json.dumps(value, separators=(",", ":"))


def parse_list(literal: str) -> Optional[ListNode]:
    head: Optional[ListNode] = None
    for val in reversed(json.loads(literal)):
        head = ListNode(val, head)
    return head


def list_to_str(head: Optional[ListNode]) -> str:
    values: list[int] = []
    while head:
        values.append(head.val)
        head = head.next
    return dumps(values)


def parse_tree(literal: str) -> Optional[TreeNode]:
    """Orden por niveles: cada nodo no nulo consume dos valores (izquierdo, derecho)."""
    values: list[Optional[int]] = json.loads(literal)
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    pending = deque([root])
    rest = iter(values[1:])
    while pending:
        node = pending.popleft()
        for side in ("left", "right"):
            val = next(rest, None)  # agotado: el resto de hijos son null
            if val is not None:
                child = TreeNode(val)
                setattr(node, side, child)
                pending.append(child)
    return root


def tree_to_str(root: Optional[TreeNode]) -> str:
    values: list[Optional[int]] = []
    queue: deque[Optional[TreeNode]] = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            values.append(None)
            continue
        values.append(node.val)
        queue.extend((node.left, node.right))
    while values and values[-1] is None:
        values.pop()  # LeetCode omite los null finales
    return dumps(values)
