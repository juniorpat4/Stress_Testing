---
name: structure
description: >
  Analiza un problema de programación competitiva o entrevista y lista las estructuras
  de datos que sirven para resolverlo, con su complejidad y su equivalente en C++ (STL)
  y en Python. Se invoca solo con /structure.
argument-hint: "[enunciado o enlace; vacío = el problema actual]"
disable-model-invocation: true
---

# /structure: estructuras de datos para el problema

Problema: $ARGUMENTS

Si está vacío, usa el problema que se está resolviendo en la conversación. Si no hay
ninguno, pide el enunciado en una línea y detente.

El enunciado puede venir como **imagen** (captura o foto) adjunta o en un mensaje anterior:
léela. En las restricciones, los exponentes suelen perderse (`105` casi siempre es `10⁵`,
`2·105` es `2·10⁵`): si un límite no se lee con total claridad, **pregúntalo en una línea
antes de seguir**, porque cambia la complejidad objetivo.

## Pasos

1. Del enunciado saca: `n` y `q` máximos, el TL, y la **lista de operaciones** que la
   estructura debe soportar (insertar, borrar, mínimo, k-ésimo, suma en rango,
   actualizar punto o rango, unir conjuntos, pertenencia, vecino más cercano...).
   Anota si las consultas son **online** u **offline** (conocidas de antemano: permite
   ordenarlas o comprimir valores).
2. Presupuesto: ~10⁸ operaciones/s en C++ (Python ~10⁷) → complejidad máxima por operación.
3. Busca candidatas en la tabla de referencia y clasifícalas en privado: las que sirven
   y las tentadoras que no (no caben en el presupuesto o no resuelven lo pedido).
4. **No escribas la solución.** Si el usuario pide después el código, pasa a la skill `competitive-programming`.

## Dos niveles (el usuario quiere pensar por su cuenta)

- **Nivel 1, pistas (por defecto):** muestra las candidatas **sin decir cuál sirve**.
- **Nivel 2, veredicto:** si `$ARGUMENTS` contiene "veredicto" o "¿cuál?", o el usuario
  lo pide después de un nivel 1 ("¿cuál?", "dame el veredicto"), sobre el mismo problema.
  Si el usuario ya eligió una ("usaría X"), empieza diciendo si su elección sirve y por qué.

## Formato nivel 1: pistas

**Operaciones:** lista corta.
**Presupuesto:** n = …, q = … → O(…) por operación.

| Estructura | Qué cubre | Complejidad |
|---|---|---|

- 4–6 candidatas **mezcladas**: las que sirven y 1–2 tentadoras que no, sin marcar
  cuáles son cuáles. Nada de ✓/✗, "recomendada" ni "trampa".
- Cierra con una línea: *"¿Cuál usarías y por qué? Cuando decidas, pide el veredicto
  con `/structure veredicto` o escribe «¿cuál?»."*

## Formato nivel 2: veredicto

**Operaciones** y **presupuesto** como en el nivel 1.

| Estructura | Operación que resuelve | Complejidad | C++ | Python | ¿Sirve? |
|---|---|---|---|---|---|

- Las mismas candidatas del nivel 1; ahora las que no sirven llevan ✗ y el motivo
  (p. ej. "✗ heap: no permite borrar un elemento arbitrario").
- **Recomendada:** una, en 1–2 frases con el porqué.
- **Trampa:** el error típico con esa estructura en este problema, en 1 línea.

## Tabla de referencia

| Necesito… | Estructura | C++ | Python |
|---|---|---|---|
| Índice O(1), agregar al final | arreglo dinámico | `vector` | `list` |
| Pertenencia o conteo, sin orden | hash | `unordered_set/map` (Codeforces: hash con semilla, por los hacks) | `set`, `dict`, `Counter` |
| Orden + buscar, borrar, vecino (`lower_bound`) | BST balanceado | `set`, `map`, `multiset` | **no hay en stdlib**: `bisect` sobre lista ordenada (inserción O(n)) o `SortedList` (LeetCode sí la trae; Codeforces no) |
| k-ésimo o rank con inserciones | árbol de estadísticos de orden | `__gnu_pbds` `tree` (ordered_set) | Fenwick sobre valores comprimidos |
| Mínimo o máximo con inserciones | heap | `priority_queue` | `heapq` (min-heap; negar para máximo) |
| Mínimo o máximo de una ventana deslizante | deque monótono | `deque` | `collections.deque` |
| FIFO, BFS | cola | `queue` | `collections.deque` |
| LIFO, paréntesis, siguiente mayor | pila (monótona) | `vector` / `stack` | `list` |
| Suma en rango, arreglo fijo | sumas de prefijos | `vector<ll>` + `partial_sum` | `itertools.accumulate` |
| Suma en rango + actualizar punto | Fenwick (BIT) | a mano | a mano |
| min, max, gcd en rango + actualizaciones | segment tree | a mano | a mano |
| Actualizar rango + consultar rango | segment tree con lazy | a mano | a mano |
| min o max en rango, sin actualizaciones | sparse table (consulta O(1)) | a mano | a mano |
| Unir conjuntos, ¿misma componente? | DSU (union-find) | a mano | a mano |
| Prefijos de strings, XOR máximo | trie | a mano | `dict` anidado |
| Grafo | lista de adyacencia | `vector<vi>` | `list[list[int]]` |
| Subconjuntos pequeños, bits | bitset / máscaras | `bitset<N>`, `int` | `int` |
| Valores grandes con pocos distintos | compresión de coordenadas | `sort` + `unique` + `lower_bound` | `sorted(set(...))` + `dict` |
