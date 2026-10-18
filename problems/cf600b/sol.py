import sys
from bisect import bisect_right


def solve(a: list[int], queries: list[int]) -> list[int]:
    """Para cada consulta x, cuántos elementos de `a` son <= x. O((n + m) log n)."""
    sorted_a = sorted(a)
    return [bisect_right(sorted_a, x) for x in queries]


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    a = list(map(int, data[2 : 2 + n]))
    queries = list(map(int, data[2 + n : 2 + n + m]))
    sys.stdout.write(" ".join(map(str, solve(a, queries))) + "\n")


if __name__ == "__main__":
    main()
