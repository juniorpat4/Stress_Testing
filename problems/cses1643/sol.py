import sys


def max_subarray_sum(a: list[int]) -> int:
    """Kadane: máxima suma de un subarreglo NO vacío. O(n) tiempo, O(1) extra."""
    best = current = a[0]  # arrancar en a[0] (no en 0) excluye el subarreglo vacío
    for x in a[1:]:
        current = max(x, current + x)  # extender el subarreglo anterior o empezar en x
        best = max(best, current)
    return best


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1 : 1 + n]))
    print(max_subarray_sum(a))


if __name__ == "__main__":
    main()
