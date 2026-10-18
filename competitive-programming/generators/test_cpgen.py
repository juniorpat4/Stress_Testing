"""Invariantes de cpgen: python3 -m unittest discover -s generators"""

from __future__ import annotations

import random
import unittest

from cpgen import binary_tree, graph, int_array, make_rng, to_leetcode, tree


def is_connected(n: int, edges: list[tuple[int, ...]]) -> bool:
    adj: dict[int, list[int]] = {v: [] for v in range(1, n + 1)}
    for u, v, *_ in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen, stack = {1}, [1]
    while stack:
        for nxt in adj[stack.pop()]:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return len(seen) == n


class TreeTest(unittest.TestCase):
    def test_every_shape_is_a_valid_tree(self) -> None:
        rng = random.Random(1)
        for shape in ("random", "line", "star"):
            for n in (1, 2, 7, 50):
                t = tree(rng, n, shape)
                self.assertEqual(len(t.edges), n - 1)
                self.assertTrue(is_connected(n, t.edges), (shape, n))

    def test_shapes(self) -> None:
        rng = random.Random(2)
        degree = lambda t: [sum(v in e for e in t.edges) for v in range(1, t.n + 1)]  # noqa: E731
        self.assertLessEqual(max(degree(tree(rng, 30, "line"))), 2)
        self.assertEqual(max(degree(tree(rng, 30, "star"))), 29)

    def test_same_seed_same_case(self) -> None:
        self.assertEqual(tree(random.Random(7), 20), tree(random.Random(7), 20))
        self.assertEqual(make_rng(["gen.py", "7"]).random(), random.Random(7).random())


class GraphTest(unittest.TestCase):
    def test_simple_and_connected(self) -> None:
        rng = random.Random(3)
        for n, m in ((1, 0), (5, 4), (6, 9), (6, 15), (40, 60)):  # (6, 15) = completo: rama densa
            g = graph(rng, n, m, weights=(1, 9))
            pairs = {frozenset(e[:2]) for e in g.edges}
            self.assertEqual(len(g.edges), m)
            self.assertEqual(len(pairs), m, "aristas repetidas")
            self.assertTrue(all(len(p) == 2 for p in pairs), "bucle u == v")
            self.assertTrue(all(1 <= e[2] <= 9 for e in g.edges))
            self.assertTrue(is_connected(n, g.edges))

    def test_impossible_sizes_raise(self) -> None:
        with self.assertRaises(ValueError):
            graph(random.Random(0), 4, 7)
        with self.assertRaises(ValueError):
            graph(random.Random(0), 4, 2)


class ArrayAndBinaryTreeTest(unittest.TestCase):
    def test_distinct_array(self) -> None:
        self.assertEqual(sorted(int_array(random.Random(4), 6, 1, 6, distinct=True)), [1, 2, 3, 4, 5, 6])

    def test_binary_tree_level_order(self) -> None:
        rng = random.Random(5)
        self.assertEqual(binary_tree(rng, 0, 1, 9), [])
        for n in (1, 2, 10, 100):
            order = binary_tree(rng, n, 1, 9)
            self.assertEqual(sum(v is not None for v in order), n)
            self.assertIsNotNone(order[0])
            self.assertIsNotNone(order[-1])
        self.assertEqual(to_leetcode([1, None, 2]), "[1,null,2]")


if __name__ == "__main__":
    unittest.main()
