from lc_local import ListNode, list_to_str, parse_list  # solo local: LeetCode ya define ListNode

# ======== COPIAR A LEETCODE DESDE AQUÍ ========
from typing import Optional


class Solution:
    # Tiempo: O(n) | Memoria: O(1)
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev: Optional[ListNode] = None
        while head:
            # El lado derecho se evalúa completo antes de asignar: no hace falta temporal.
            head.next, prev, head = prev, head, head.next
        return prev
# ======== HASTA AQUÍ ========


def _local_main() -> None:
    import sys

    for line in filter(None, map(str.strip, sys.stdin.read().splitlines())):
        print(list_to_str(Solution().reverseList(parse_list(line))))


if __name__ == "__main__":
    import os

    if os.environ.get("LOCAL"):
        _local_main()
