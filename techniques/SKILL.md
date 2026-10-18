---
name: techniques
description: >
  Analiza un problema de programación competitiva o entrevista y lista las técnicas
  algorítmicas que sirven para resolverlo (búsqueda binaria, dos punteros, greedy, DP,
  BFS, Dijkstra...), con su complejidad y su idiom en C++ y Python. Se invoca solo con /techniques.
argument-hint: "[enunciado o enlace; vacío = el problema actual]"
disable-model-invocation: true
---

# /techniques: técnicas para el problema

Problema: $ARGUMENTS

Si está vacío, usa el problema que se está resolviendo en la conversación. Si no hay
ninguno, pide el enunciado en una línea y detente.

El enunciado puede venir como **imagen** (captura o foto) adjunta o en un mensaje anterior:
léela. En las restricciones, los exponentes suelen perderse (`105` casi siempre es `10⁵`,
`2·105` es `2·10⁵`): si un límite no se lee con total claridad, **pregúntalo en una línea
antes de seguir**, porque cambia la complejidad objetivo.

## Pasos

1. Del enunciado saca: `n` máximo, TL, qué se pide (mínimo/máximo, contar, decidir,
   construir) y las **señales**: arreglo ordenado o positivos, "mínimo X tal que...",
   subarreglo contiguo, grafo con o sin pesos, intervalos, `n ≤ 20`, módulo 10⁹+7...
2. Presupuesto: ~10⁸ operaciones/s en C++ (Python ~10⁷) → complejidad total máxima
   (`n ≤ 2·10⁵` → O(n log n); `n ≤ 5000` → O(n²); `n ≤ 20` → O(2ⁿ·n)).
3. Busca candidatas en la tabla de referencia y clasifícalas en privado: las que sirven
   y las tentadoras que no (no caben en el presupuesto o no resuelven lo pedido).
4. **No escribas la solución.** Si hace falta una
   estructura concreta, menciónala en una palabra y remite a `/structure`; si el
   usuario pide el código, pasa a la skill `competitive-programming`.

## Dos niveles (el usuario quiere pensar por su cuenta)

- **Nivel 1, pistas (por defecto):** muestra las candidatas **sin decir cuál sirve**.
- **Nivel 2, veredicto:** si `$ARGUMENTS` contiene "veredicto" o "¿cuál?", o el usuario
  lo pide después de un nivel 1 ("¿cuál?", "dame el veredicto"), sobre el mismo problema.
  Si el usuario ya eligió una ("usaría X"), empieza diciendo si su elección sirve y por qué.

## Formato nivel 1: pistas

**Se pide:** qué se calcula, en una línea.
**Señales:** las que aparecen en el enunciado.
**Presupuesto:** n = … → O(…) total.

| Técnica | Qué cubre | Complejidad |
|---|---|---|

- 4–6 candidatas **mezcladas**: las que sirven y 1–2 tentadoras que no, sin marcar
  cuáles son cuáles. Nada de ✓/✗, "recomendada" ni "trampa".
- Cierra con una línea: *"¿Cuál usarías y por qué? Cuando decidas, pide el veredicto
  con `/techniques veredicto` o escribe «¿cuál?»."*

## Formato nivel 2: veredicto

**Se pide**, **señales** y **presupuesto** como en el nivel 1.

| Técnica | Por qué encaja aquí | Complejidad | C++ | Python | ¿Sirve? |
|---|---|---|---|---|---|

- Las mismas candidatas del nivel 1; ahora las que no sirven llevan ✗ y el motivo
  (p. ej. "✗ heap: no permite borrar un elemento arbitrario").
- **Recomendada:** una, en 1–2 frases con el porqué.
- **Trampa:** el error típico con esa técnica en este problema, en 1 línea.

## Tabla de referencia

| Señal en el enunciado | Técnica | C++ | Python |
|---|---|---|---|
| Buscar en datos ordenados | búsqueda binaria | `lower_bound`, `upper_bound` | `bisect_left`, `bisect_right` |
| "Mínimo/máximo X tal que se cumple…" (predicado monótono) | búsqueda binaria sobre la respuesta | `while (lo < hi)` con `check(mid)` | igual, o `bisect_left(range(hi), True, key=check)` |
| Pares o subarreglos en arreglo ordenado o con valores positivos | dos punteros | dos índices `l`, `r` | igual |
| Subarreglo contiguo que crece y se encoge con una condición | ventana deslizante | `l`, `r` + estado de la ventana | igual, `Counter` para el estado |
| Suma de subarreglo, contar subarreglos con suma k | prefijos (+ hash de prefijos) | `partial_sum`, `unordered_map` | `accumulate`, `defaultdict(int)` |
| Muchas sumas en rango aplicadas antes de leer | arreglo de diferencias | `d[l] += v; d[r+1] -= v` | igual |
| Elección local óptima demostrable por intercambio | greedy (casi siempre tras ordenar) | `sort` con comparador | `sort(key=...)` |
| Subproblemas que se repiten: contar formas, óptimo sobre decisiones | DP (mochila, LIS, intervalos, dígitos) | tabla `vector` | lista o `@cache` (ojo con la recursión) |
| `n ≤ 20` | fuerza bruta por máscaras / backtracking | `forn(mask, 1 << n)` | `range(1 << n)` |
| `n ≤ 40` | meet in the middle | dos mitades + `sort` + búsqueda binaria | igual |
| Distancia mínima en grafo sin pesos o rejilla | BFS (pesos 0/1: 0-1 BFS) | `queue` / `deque` | `deque` |
| Distancia mínima con pesos no negativos | Dijkstra | `priority_queue` con `greater<>` | `heapq` |
| Pesos negativos / todos los pares con `n ≤ 400` | Bellman-Ford / Floyd-Warshall | bucles | bucles (Floyd en Python: solo `n` pequeño) |
| Conectividad, componentes, ciclos | DFS o DSU | recursivo o pila | pila explícita (límite de recursión) |
| Dependencias, "antes de" | orden topológico (Kahn) | `queue` de grado 0 | `deque` |
| Conectar todo con costo mínimo | MST (Kruskal + DSU) | `sort` de aristas | igual |
| Árbol: diámetro, subárboles, ancestros | DFS en árbol, rerooting, binary lifting (LCA) | DFS + `up[k][v]` | iterativo |
| Intervalos, eventos en el tiempo | ordenar + barrido (sweep line) | `sort` de eventos | igual |
| Buscar un patrón en un texto | KMP / función Z / hashing | a mano | a mano |
| Primos, divisores, `mod 10⁹+7` | criba, exponenciación rápida, inverso modular | a mano | `pow(a, b, mod)`, `pow(a, -1, mod)` |
| Muchas consultas conocidas de antemano | procesar offline (ordenar consultas, Mo) | `sort` de consultas | igual |
