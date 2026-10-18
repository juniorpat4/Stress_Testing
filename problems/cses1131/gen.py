"""Caso pequeño de CSES 1131: `python3 gen.py <seed>` (cpgen llega vía PYTHONPATH)."""

from cpgen import make_rng, tree


def main() -> None:
    rng = make_rng()
    shape = rng.choice(["random", "line", "star"])
    print(tree(rng, rng.randint(1, 8), shape).to_codeforces())


if __name__ == "__main__":
    main()
