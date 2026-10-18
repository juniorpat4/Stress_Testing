"""Generadores aleatorios reutilizables para stress tests y casos máximos.

Uso típico en el gen.py de un problema (contrato de stress_test: `gen.py <seed>`):

    from cpgen import make_rng, tree

    rng = make_rng()
    print(tree(rng, rng.randint(1, 8), shape=rng.choice(["random", "line", "star"])).to_codeforces())

Todas las funciones reciben un `random.Random` explícito: misma semilla → mismo caso.
Listas enlazadas de LeetCode: se serializan igual que un arreglo, `to_leetcode(int_array(...))`.
"""

from __future__ import annotations

import json
import random
import sys
from dataclasses import dataclass
from itertools import combinations
from typing import Literal

TreeShape = Literal["random", "line", "star"]


def make_rng(argv: list[str] | None = None) -> random.Random:
    """Crea el generador con la semilla de argv[1]."""
    args = sys.argv if argv is None else argv
    if len(args) < 2:
        raise SystemExit("uso: gen.py <seed>")
    return random.Random(int(args[1]))


def int_array(rng: random.Random, n: int, lo: int, hi: int, *, distinct: bool = False) -> list[int]:
    """n enteros en [lo, hi]. Permutación de 1..n: int_array(rng, n, 1, n, distinct=True)."""
    if not distinct:
        return [rng.randint(lo, hi) for _ in range(n)]
    if hi - lo + 1 < n:
        raise ValueError(f"no hay {n} valores distintos en [{lo}, {hi}]")
    return rng.sample(range(lo, hi + 1), n)


def to_leetcode(values: list[int | None]) -> str:
    """Literal LeetCode: [1,null,2]. Sirve para arreglos, listas enlazadas y árboles binarios."""
    return json.dumps(values, separators=(",", ":"))


@dataclass(frozen=True, slots=True)
class Tree:
    n: int
    edges: list[tuple[int, int]]  # nodos 1..n

    def to_codeforces(self) -> str:
        """n en la primera línea y luego n-1 líneas `u v`."""
        return "\n".join([str(self.n), *(f"{u} {v}" for u, v in self.edges)])


@dataclass(frozen=True, slots=True)
class Graph:
    n: int
    edges: list[tuple[int, ...]]  # (u, v) o (u, v, w); nodos 1..n

    def to_codeforces(self) -> str:
        """`n m` en la primera línea y luego m líneas `u v [w]`."""
        lines = [f"{self.n} {len(self.edges)}", *(" ".join(map(str, e)) for e in self.edges)]
        return "\n".join(lines)


def tree(rng: random.Random, n: int, shape: TreeShape = "random") -> Tree:
    """Árbol de n nodos. `random` tiene profundidad ~O(log n); `line` fuerza la recursión
    más profunda posible y `star` el grado máximo."""
    label = rng.sample(range(1, n + 1), n)  # etiquetas al azar: que el nodo 1 no sea siempre la raíz
    edges: list[tuple[int, int]] = []
    for child in range(1, n):
        if shape == "line":
            parent = child - 1
        elif shape == "star":
            parent = 0
        else:
            parent = rng.randrange(child)
        u, v = label[parent], label[child]
        edges.append((u, v) if rng.random() < 0.5 else (v, u))
    rng.shuffle(edges)
    return Tree(n, edges)


def graph(
    rng: random.Random,
    n: int,
    m: int,
    *,
    connected: bool = True,
    weights: tuple[int, int] | None = None,
) -> Graph:
    """Grafo simple no dirigido (sin bucles ni aristas repetidas) con m aristas."""
    max_edges = n * (n - 1) // 2
    if m > max_edges:
        raise ValueError(f"un grafo simple de {n} nodos admite como máximo {max_edges} aristas")
    if connected and n > 0 and m < n - 1:
        raise ValueError(f"un grafo conexo de {n} nodos necesita al menos {n - 1} aristas")

    chosen: set[tuple[int, int]] = set()
    if connected and n > 1:
        chosen = {(min(u, v), max(u, v)) for u, v in tree(rng, n).edges}

    if 2 * m > max_edges:
        # Denso: muestrear del resto de pares (el rechazo tardaría mucho cerca de max_edges).
        remaining = [p for p in combinations(range(1, n + 1), 2) if p not in chosen]
        chosen.update(rng.sample(remaining, m - len(chosen)))
    else:
        while len(chosen) < m:
            u, v = rng.sample(range(1, n + 1), 2)
            chosen.add((min(u, v), max(u, v)))

    edges: list[tuple[int, ...]] = []
    for u, v in sorted(chosen):  # sorted: el orden del set no depende de la semilla
        pair = (u, v) if rng.random() < 0.5 else (v, u)
        edges.append(pair if weights is None else (*pair, rng.randint(*weights)))
    rng.shuffle(edges)
    return Graph(n, edges)


def binary_tree(rng: random.Random, n: int, lo: int, hi: int) -> list[int | None]:
    """Árbol binario aleatorio en el orden por niveles de LeetCode (con null y sin null finales)."""
    if n == 0:
        return []
    values = [rng.randint(lo, hi) for _ in range(n)]
    children: list[list[int | None]] = [[None, None] for _ in range(n)]
    free_slots = [(0, 0), (0, 1)]  # (nodo, 0 = izquierdo / 1 = derecho)
    for node in range(1, n):
        i = rng.randrange(len(free_slots))
        free_slots[i], free_slots[-1] = free_slots[-1], free_slots[i]
        parent, side = free_slots.pop()  # swap-and-pop: quitar un elemento al azar en O(1)
        children[parent][side] = node
        free_slots += [(node, 0), (node, 1)]

    order: list[int | None] = []
    queue: list[int | None] = [0]
    for node in queue:  # BFS: recorrer la lista mientras crece
        if node is None:
            order.append(None)
            continue
        order.append(values[node])
        queue.extend(children[node])
    while order[-1] is None:
        order.pop()
    return order
