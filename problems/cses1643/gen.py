"""Caso pequeño de CSES 1643: `python3 gen.py <seed>` (cpgen llega vía PYTHONPATH)."""

from cpgen import int_array, make_rng


def main() -> None:
    rng = make_rng()
    n = rng.randint(1, 8)  # casos chicos: el primer contraejemplo ya es legible
    print(n)
    print(*int_array(rng, n, -10, 10))


if __name__ == "__main__":
    main()
