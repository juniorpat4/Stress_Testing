# ======== COPIAR A LEETCODE DESDE AQUÍ ========
from collections import deque
from typing import List


class Solution:
    # Tiempo: O(n) | Memoria: O(k)
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        window: deque[int] = deque()  # índices cuyos valores van en orden decreciente
        result: List[int] = []
        for i, x in enumerate(nums):
            if window and window[0] <= i - k:
                window.popleft()  # ya salió de la ventana
            while window and nums[window[-1]] <= x:
                window.pop()  # nunca será máximo
            window.append(i)
            if i >= k - 1:
                result.append(nums[window[0]])
        return result
# ======== HASTA AQUÍ ========


# ======== Harness local (equivalente a #ifdef LOCAL) ========
def _local_main() -> None:
    import json
    import sys

    lines = [ln for ln in sys.stdin.read().splitlines() if ln.strip()]
    for nums_line, k_line in zip(lines[::2], lines[1::2]):
        answer = Solution().maxSlidingWindow(json.loads(nums_line), int(k_line))
        print(json.dumps(answer, separators=(",", ":")))


if __name__ == "__main__":
    import os

    if os.environ.get("LOCAL"):
        _local_main()
