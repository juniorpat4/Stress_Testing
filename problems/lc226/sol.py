from lc_local import TreeNode, parse_tree, tree_to_str  # solo local: LeetCode ya define TreeNode

# ======== COPIAR A LEETCODE DESDE AQUÍ ========
from typing import Optional


class Solution:
    # Tiempo: O(n) | Memoria: O(h) de pila de recursión
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root:
            root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root
# ======== HASTA AQUÍ ========


def _local_main() -> None:
    import sys

    for line in filter(None, map(str.strip, sys.stdin.read().splitlines())):
        print(tree_to_str(Solution().invertTree(parse_tree(line))))


if __name__ == "__main__":
    import os

    if os.environ.get("LOCAL"):
        _local_main()
