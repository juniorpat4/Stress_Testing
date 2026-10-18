---
name: competitive-programming
description: >
  Resolver, depurar y verificar problemas de programación competitiva y entrevistas
  de código en C++ y Python. Detecta la plataforma y adapta el formato: jueces de
  entrada/salida estándar (Codeforces, AtCoder, OmegaUp, Beecrowd, CSES, SPOJ) con
  main() y lectura de stdin, o plataformas basadas en clases (LeetCode) con solo
  `class Solution` y un harness oculto tras `#ifdef LOCAL`. Incluye scripts de
  verificación con sanitizers y medición de tiempo/memoria (verify_limits.py),
  búsqueda de contraejemplos por fuerza bruta (stress_test.py) y generadores
  aleatorios de arreglos, árboles, listas y grafos. Por defecto NO da la solución
  (modo sin spoilers): prepara el problema y verifica el código del usuario. Usar cuando
  el usuario pegue un enunciado (texto, o foto/captura del problema), un enlace a un juez, pida una solución, un brute force,
  un stress test, un generador, o diga "WA", "TLE", "MLE", "RE", "contraejemplo", "complejidad".
---

# Programación competitiva y entrevistas de código

> **Regla primera: modo sin spoilers (§6).** El usuario quiere pensar el problema por
> su cuenta. Nunca des la idea, la técnica, la estructura ni el código de la solución
> salvo que lo pida explícitamente.

## 0. Contrato universal (léelo primero)

Todo lo que genera esta skill respeta **una sola regla de oro**:

> Compilado con `-DLOCAL` (C++) o ejecutado con `LOCAL=1` (Python), **todo programa
> es un filtro `stdin → stdout`**.

- En modo juez estándar eso ya es cierto por naturaleza.
- En modo LeetCode, la `class Solution` queda intacta y un `main()` de prueba vive
  dentro de `#ifdef LOCAL` (C++) o tras un guard de `LOCAL` (Python).

Gracias a ese contrato, `verify_limits.py`, `stress_test.py` y los generadores
funcionan **igual** para ambos mundos: solo ven ejecutables que leen y escriben texto.

## 1. Detección de plataforma

Decide el modo **antes** de escribir código, en este orden de prioridad:

1. **Lo que diga el usuario** ("es de LeetCode", "Codeforces 1980C") siempre gana.
2. **URL o nombre**: `leetcode.com` → LeetCode. `codeforces.com`, `atcoder.jp`,
   `omegaup.com`, `beecrowd.com.br`, `cses.fi`, `spoj.com` → Juez estándar.
3. **Forma del enunciado**:

| Señal en el enunciado | Modo |
|---|---|
| Firma dada (`class Solution`, `def twoSum(self, ...)`), "Return ...", ejemplos `Input: nums = [2,7], target = 9` | **LeetCode** |
| Secciones "Input"/"Output", "The first line contains t", "time limit per test", "memory limit", formato de salida exacto | **Juez estándar** |

4. **Ambiguo** → pregunta una sola vez. Si no hay respuesta, usa Juez estándar.

Anuncia el modo en una línea al empezar: `Modo: Juez estándar (Codeforces)` o
`Modo: LeetCode (class Solution)`.

### Particularidades por juez

- **Codeforces**: casi siempre multitest (`t`). Hay *hacks*: evita `unordered_map`
  con claves controladas por el rival sin un hash con semilla aleatoria.
  Python: recomendar enviar con **PyPy 3**.
- **AtCoder**: normalmente un único caso; salida exacta (ojo con `Yes`/`No` vs
  `YES`/`NO`). Restricciones pequeñas en A/B, grandes en E+.
- **OmegaUp**: entrada estándar; verifica si el problema pide salida con o sin
  salto final y si hay subtareas (resolver por subtareas puntúa parcialmente).
- **Beecrowd**: a menudo se lee **hasta EOF** (`while (cin >> n)`), y el formato de
  salida (espacios, salto de línea final) se compara estrictamente.

## 2. Reglas de estilo

### C++ (foco: programación competitiva)

- **Obligatorio**: todo archivo C++ empieza con la **plantilla del usuario (§3.0)**,
  copiada sin cambios. Ya trae `#include <bits/stdc++.h>` y `using namespace std;`.
  En modo LeetCode la plantilla va **dentro** del bloque que se copia (la clase usa
  sus macros y alias), no bajo `#ifdef LOCAL`.
- Estándar `-std=c++20`. Orden fijo del archivo:
  1. plantilla §3.0
  2. constantes y estructuras propias del problema
  3. funciones auxiliares
  4. `solve()`
  5. `main()`
- Usa los alias y macros de la plantilla (`ll`, `vi`, `vll`, `ii`, `forn`, `fore`,
  `all`, `sz`, `pb`, `el`, `fi`/`se`) donde acorten sin oscurecer. No añadas macros nuevas.
  En LeetCode respeta la firma que da la plataforma (`vector<int>&`, no `vi&`).
- **Nombres reservados por la plantilla**: ninguna variable ni función puede
  llamarse `fi`, `se`, `pb`, `el`, `sz`, `all`, `ri`, `dbg`, `forn`, `for1`, `fore`,
  `ford`, `fored`, `inf`, `nax`, `mod`, `pi`, `eps`, `dr`, `dc` (p. ej. `vi all(n);`
  o `int el;` no compilan o cambian de significado).
- `ri(n)` usa `scanf`: **no lo mezcles con `cin`** si hay `sync_with_stdio(false)`,
  porque el orden de lectura deja de estar garantizado. Por defecto, `cin`.
- `dbg(x)` escribe en `cerr` y solo existe con `-DLOCAL` sin `-DNDEBUG`: puede
  quedarse en el envío sin afectar la salida.
- `ld` es `double` en esta plantilla (no `long double`): si hace falta más
  precisión, escribe `long double` explícitamente.
- Nombres descriptivos (`dist`, `adj`, `prefix`), no `a1`, `tmp2`.
- `el` (`'\n'`), nunca `endl` (fuerza flush). Fast I/O siempre en `main()`.
- Desbordamiento: si un producto o suma puede pasar de ~2·10⁹, usa `long long`
  (y `0LL` en `accumulate`).
- Multitest: prefiere estructuras locales a `solve()`. Si usas arreglos globales,
  reinicia solo la porción usada (no `memset` de todo el arreglo por caso).
- Encabezado de complejidad sobre `solve()` o el método:
  `// Tiempo: O(n log n) | Memoria: O(n)`.

### Python (foco: ingeniería de software)

- Python 3.10+ con *type hints* en todas las firmas.
- **Separar I/O de lógica**: `solve(...)` es una función pura (sin `input()` ni
  `print()`), `main()` parsea y formatea. Esto la vuelve testeable.
- Juez estándar: lectura masiva con `sys.stdin.buffer.read().split()` y salida
  acumulada con un único `sys.stdout.write`.
- Tipos nativos en modo juez (`list[int]`, `dict[str, int]`); en LeetCode respeta
  la firma de la plataforma (`List[int]`, `Optional[TreeNode]`).
- Recursión profunda: preferir iterativo; si no, `sys.setrecursionlimit` y avisar
  del riesgo de stack overflow.

## 3. Plantillas por modo

### 3.0 Plantilla C++ del usuario (obligatoria)

Va al inicio de **todo** archivo C++ (soluciones, `brute`, generadores en C++).
Es la plantilla del usuario con un único ajuste: su macro de depuración `d(x)`
pasó a ser `dbg(x)` en `cerr` y solo con `LOCAL` (la original escribía en `cout`
y rompía la comparación de salidas; además `d(x)` chocaba con `vi d(n);`).

```cpp
#ifndef TEMPLATE_H
#define TEMPLATE_H

#include <bits/stdc++.h>

#define fi first
#define se second
#define forn(i,n) for(int i=0; i< (int)n; ++i)
#define for1(i,n) for(int i=1; i<= (int)n; ++i)
#define fore(i,l,r) for(int i=(int)l; i<= (int)r; ++i)
#define ford(i,n) for(int i=(int)(n) - 1; i>= 0; --i)
#define fored(i,l,r) for(int i=(int)r; i>= (int)l; --i)
#define pb push_back
#define el '\n'
#if defined(LOCAL) && !defined(NDEBUG)
#define dbg(x) cerr<< #x<< " " << x<<el
#else
#define dbg(x) ((void)0)
#endif
#define ri(n) scanf("%d",&n)
#define sz(v) int(v.size())
#define all(v) v.begin(),v.end()
using namespace std;
typedef long long ll;
typedef double ld;
typedef pair<int,int> ii;
typedef pair<ll,ll> pll;
typedef tuple<int, int, int> iii;
typedef vector<int> vi;
typedef vector<ii> vii;
typedef vector<ll> vll;
typedef vector<ld> vd;

const int inf = 1e9, nax = 1e5+200, mod = 1e9 + 7;
const ld pi = acos(-1);
const ld eps= 1e-9;
int dr[] = {1,-1,0, 0,1,-1,-1, 1};
int dc[] = {0, 0,1,-1,1, 1,-1,-1};

ostream& operator<<(ostream& os, const ii& pa) {
  return os << "("<< pa.fi << ", " << pa.se << ")";
}

#endif // TEMPLATE_H
```

### 3.1 Juez estándar — C++

```cpp
// <plantilla §3.0 completa aquí>

// Tiempo: O(n) | Memoria: O(n)
void solve() {
    int n;
    cin >> n;
    vll a(n);
    forn(i, n) cin >> a[i];

    cout << accumulate(all(a), 0LL) << el;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t = 1;
    cin >> t;  // eliminar esta línea si el problema tiene un único caso
    while (t--) solve();
    return 0;
}
```

### 3.2 Juez estándar — Python

```python
import sys
from collections.abc import Iterator


def solve(a: list[int]) -> int:
    """Lógica pura: sin I/O, testeable de forma aislada."""
    return sum(a)


def main() -> None:
    data: Iterator[bytes] = iter(sys.stdin.buffer.read().split())
    t = int(next(data))
    out: list[str] = []
    for _ in range(t):
        n = int(next(data))
        a = [int(next(data)) for _ in range(n)]
        out.append(str(solve(a)))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
```

### 3.3 LeetCode — C++

La plantilla va dentro del bloque copiado, porque la clase usa sus macros y alias.
El archivo completo sigue siendo **enviable tal cual** (sin `LOCAL` el harness
desaparece). *Sin verificar en LeetCode*: que acepte `<bits/stdc++.h>` y que las
macros cortas (`fi`, `se`, `el`) no choquen con el código que LeetCode añade; si
falla, quita el `#include` o la macro conflictiva del bloque copiado.

```cpp
// ======== COPIAR A LEETCODE DESDE AQUÍ ========
// <plantilla §3.0 completa aquí>
#ifdef LOCAL
#include "lc_local.hpp"  // TreeNode, ListNode y parsers de literales; en LeetCode ya existen
#endif

class Solution {
public:
    // Tiempo: O(n) promedio | Memoria: O(n)
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> seen;  // valor -> índice
        seen.reserve(sz(nums) * 2);
        forn(i, sz(nums)) {
            auto it = seen.find(target - nums[i]);
            if (it != seen.end()) return {it->se, i};
            seen[nums[i]] = i;
        }
        return {};
    }
};
// ======== HASTA AQUÍ ========

#ifdef LOCAL
// Entrada: por cada caso, una línea por argumento, en el formato de LeetCode.
int main() {
    string numsLine, targetLine;
    while (getline(cin, numsLine) && getline(cin, targetLine)) {
        vi nums = parseIntVector(numsLine);
        int target = stoi(targetLine);
        cout << toString(Solution().twoSum(nums, target)) << el;
    }
    return 0;
}
#endif
```

### 3.4 LeetCode — Python

```python
# Con TreeNode/ListNode, esta línea va ARRIBA y fuera del bloque copiado:
# from lc_local import TreeNode, ListNode, parse_tree, tree_to_str, parse_list, list_to_str
from typing import List, Optional  # LeetCode ya los importa; aquí para uso local.


class Solution:
    # Tiempo: O(n) promedio | Memoria: O(n)
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen: dict[int, int] = {}  # valor -> índice
        for i, x in enumerate(nums):
            if (j := seen.get(target - x)) is not None:
                return [j, i]
            seen[x] = i
        return []


# ======== Harness local (equivalente a #ifdef LOCAL) ========
def _local_main() -> None:
    import json
    import sys

    lines = [ln for ln in sys.stdin.read().splitlines() if ln.strip()]
    for nums_line, target_line in zip(lines[::2], lines[1::2]):
        nums: List[int] = json.loads(nums_line)  # los literales de LeetCode son JSON
        answer = Solution().twoSum(nums, int(target_line))
        print(json.dumps(answer, separators=(",", ":")))


if __name__ == "__main__":
    import os

    if os.environ.get("LOCAL"):
        _local_main()
```

Reglas del harness LeetCode (ambos lenguajes):
- Formato de entrada = **un argumento por línea, tal como aparece en el ejemplo de
  LeetCode** (`[2,7,11,15]` y luego `9`). Así se pegan los ejemplos sin editarlos.
- Varios casos seguidos en el mismo archivo; se procesa hasta EOF.
- Salida en formato LeetCode (`[0,1]`, `true`, `"abc"`), una línea por caso.
- `TreeNode` / `ListNode` y los literales LeetCode viven en `local/` (nunca se
  redefinen en la solución, LeetCode ya los trae):

  | C++ (`lc_local.hpp`) | Python (`lc_local.py`) |
  |---|---|
  | `parseIntVector`, `parseList`, `parseTree` | `json.loads`, `parse_list`, `parse_tree` |
  | `toString(vector<int> \| ListNode* \| TreeNode*)`; bool: `cout << boolalpha` | `dumps`, `list_to_str`, `tree_to_str` |

  Los scripts añaden `-I local` a g++ y `local/` al `PYTHONPATH`. A mano:
  `g++ -DLOCAL -I <skill>/local sol.cpp` y `env PYTHONPATH=<skill>/local LOCAL=1 python3 sol.py`.
  En Python, la línea `from lc_local import ...` va **fuera** del bloque copiado.
  Ejemplos completos: `problems/lc226` (árbol) y `problems/lc206` (lista).

## 4. Estructura de trabajo por problema

Al empezar un problema, crea (o usa) esta carpeta:

```
<problema>/
├── sol.cpp | sol.py        # solución principal (formato de la plataforma)
├── brute.cpp | brute.py    # fuerza bruta obviamente correcta (mismo contrato I/O)
├── gen.py                  # `gen.py <seed>` imprime UN caso; usa la librería cpgen
├── checker.py              # opcional, varias respuestas válidas: `checker <in> <esperado> <obtenido>`, exit 0 acepta / 1 rechaza
└── tests/
    ├── 1.in   1.out        # ejemplos del enunciado
    └── ...
```

El `brute` en modo LeetCode es otra `class Solution` con el **mismo harness**, así
ambos leen la misma entrada.

## 5. Protocolo de verificación

Nunca declares una solución "correcta" sin pasar por estos pasos (en orden):

1. **Análisis de complejidad** contra las restricciones. Referencia: ~10⁸
   operaciones simples por segundo en C++ (Python: ~10⁷, PyPy: ~10⁸ con suerte).

   | n máximo | Complejidad objetivo |
   |---|---|
   | ≤ 10–12 | O(n!), O(2ⁿ·n) |
   | ≤ 20–25 | O(2ⁿ), meet-in-the-middle |
   | ≤ 500 | O(n³) |
   | ≤ 5·10³ | O(n²) |
   | ≤ 2·10⁵ – 10⁶ | O(n log n), O(n) |
   | ≤ 10¹⁸ | O(log n), O(√n), fórmula |

2. **Ejemplos del enunciado** con `verify_limits.py` en perfil `debug`
   (sanitizers): detecta accesos fuera de rango, overflow con signo, uso de
   iteradores inválidos.
3. **Caso máximo** con `verify_limits.py` en perfil `release`: mide tiempo y
   memoria reales contra el TL/ML del problema.
4. **Si hay WA o dudas** → `stress_test.py` con `brute` + `gen.py` en casos
   pequeños hasta encontrar un contraejemplo mínimo; corrige y repite.

### 5.1 Perfiles de compilación (C++)

| Perfil | Flags | Para qué |
|---|---|---|
| `debug` | `-std=c++20 -O1 -g -Wall -Wextra -Wshadow -DLOCAL -D_GLIBCXX_DEBUG -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer` | Correctitud: UB, fuera de rango, overflow |
| `release` | `-std=c++20 -O2 -DLOCAL -DNDEBUG` | Tiempo y memoria realistas (como el juez) |

- **Corre siempre los dos perfiles**: un `front()` sobre un `deque` vacío o un
  `a[n]` pasan como OK en `release` (UB silencioso) y solo `debug` los detecta.
- `-fno-sanitize-recover=all` es imprescindible: sin él UBSan imprime el aviso
  pero el programa termina con código 0 y el caso parece correcto.
- **No midas tiempo ni memoria con el perfil `debug`**: ASan reserva memoria
  sombra y `_GLIBCXX_DEBUG` vuelve las operaciones de la STL varias veces más lentas.
- `-DNDEBUG` desactiva `assert` y la macro `dbg`, así no contaminan la medición.
- Python: se ejecuta con `LOCAL=1`; la memoria se mide igual (RSS máximo).
- El tiempo reportado es **CPU** (user + sys), como en los jueces. El proceso se
  mata a 2×TL de reloj en `release` (10×TL en `debug`) para ver cuánto se pasa.
- La memoria medida nunca baja de ~12 MB (Linux hereda el pico del Python padre
  antes del `exec`): sobrestima, nunca subestima.
- La pila del programa se sube a 512 MB, como en Codeforces, para que un DFS
  recursivo profundo no dé un RE local falso.

### 5.2 Scripts de la skill

Rutas relativas al directorio de esta skill. Arquitectura: los CLIs solo parsean
argumentos; la lógica vive en el paquete `scripts/cptools/`:

| Módulo | Responsabilidad |
|---|---|
| `models.py` | `BuildProfile` (DEBUG/RELEASE), `RunResult`, `Verdict`, `judge()`, `outputs_match()` |
| `compiler.py` | `build(source, profile, out_dir) -> argv` (g++ para `.cpp`, intérprete para `.py`) |
| `runner.py` | `run(argv, input, wall_limit) -> RunResult` con `wait4` (CPU + RSS del hijo); `make_comparator(checker, eps)` |
| `report.py` | `report_failure()`: cola de stderr en RE, primera línea distinta en WA |

Pruebas: `python3 -m unittest discover -s scripts` (y `-s generators`, `-s local`).

```bash
# Fase 2 — sin opciones: usa tests/ junto al fuente y corre debug + release.
# Compara por tokens contra N.out; sin .out solo verifica que no falle ni exceda límites.
python3 scripts/verify_limits.py sol.cpp
python3 scripts/verify_limits.py sol.cpp --input max.in --profile release --tl 2 --ml 256
python3 scripts/verify_limits.py sol.cpp --eps 1e-6          # decimales: error abs. o relativo <= eps
python3 scripts/verify_limits.py sol.cpp --checker check.py  # varias respuestas válidas (sirve sin .out)
# Salida: 0 todo OK · 1 algún WA/TLE/MLE/RE · 2 error de compilación o de uso

# Fase 3 — busca contraejemplos sol vs brute con entradas de gen
python3 scripts/stress_test.py --sol sol.cpp --brute brute.cpp --gen gen.py --iters 1000
# Acepta también --eps y --checker. En el stress el checker recibe la salida de brute como "esperado".
# Salida: 0 sin contraejemplos · 1 contraejemplo · 2 error (compilación, gen/brute fallan, o el checker sale con código ≠ 0/1)

```

Reglas de `stress_test.py`:
- **Contrato del generador**: `gen <seed>` imprime UN caso por stdout; misma
  semilla → mismo caso (usa `random.Random(seed)`, nunca el `random` global).
- **Casos pequeños** (`n` ≤ 8–10, valores chicos): el primer contraejemplo ya es
  legible y `brute` puede ser O(n³) o exponencial.
- `sol` se compila en `debug` por defecto (un UB aparece como RE); `brute` y `gen`
  en `release`. Si `gen` o `brute` fallan, es error de la herramienta (código 2).
- Al primer fallo guarda `tests/stress_<seed>.in/.out` junto a `sol`:
  `verify_limits.py` lo incluye desde entonces como **test de regresión**.
- `sol` y `brute` pueden estar en lenguajes distintos (p. ej. `sol.py` vs `brute.cpp`).
- Coste real: ~40 ms por iteración, dominado por arrancar Python en `gen.py`
  (~26 ms). 1000 iteraciones ≈ 45 s.
- El stress solo encuentra lo que `gen` explora: con valores chicos **no**
  detecta overflow. Para eso, un caso aparte con valores extremos.

### 5.3 Generadores: `generators/cpgen.py`

Librería importable, no un CLI: cada problema tiene su `gen.py` de pocas líneas
que respeta el contrato `gen <seed>` y combina las piezas que necesita.

```python
from cpgen import make_rng, tree

def main() -> None:
    rng = make_rng()  # semilla desde argv[1]
    shape = rng.choice(["random", "line", "star"])
    print(tree(rng, rng.randint(1, 8), shape).to_codeforces())
```

| Pieza | Devuelve | Notas |
|---|---|---|
| `make_rng(argv=None)` | `random.Random` | semilla de `argv[1]` |
| `int_array(rng, n, lo, hi, distinct=False)` | `list[int]` | permutación: `int_array(rng, n, 1, n, distinct=True)` |
| `tree(rng, n, shape)` | `Tree` | `random` (profundidad ~log n), `line` (recursión máxima), `star` (grado máximo); etiquetas barajadas |
| `graph(rng, n, m, connected=True, weights=None)` | `Graph` | simple y no dirigido; `weights=(lo, hi)` añade pesos; valida que `m` sea posible |
| `binary_tree(rng, n, lo, hi)` | `list[int \| None]` | orden por niveles de LeetCode |
| `to_leetcode(values)` | `str` | `[1,null,2]`: arreglos, **listas enlazadas** y árboles binarios |
| `Tree.to_codeforces()` / `Graph.to_codeforces()` | `str` | `n` + aristas / `n m` + aristas `u v [w]` |

- `stress_test.py` y `verify_limits.py` añaden `generators/` al `PYTHONPATH` del
  hijo: `import cpgen` funciona sin tocar `sys.path`. A mano:
  `env PYTHONPATH=<skill>/generators python3 gen.py 7`.
- Mezcla formas en el stress (`rng.choice` de `shape`): un bug que solo aparece
  en caminos largos o en estrellas no sale con árboles aleatorios.
- Casos máximos para `verify_limits.py`: el mismo `tree(rng, 2 * 10**5, "line")`.
- Sin grafos dirigidos ni DAG por ahora: se añaden cuando un problema los pida.
- Pruebas: `python3 -m unittest discover -s generators`.

## 6. Modo sin spoilers (por defecto)

El usuario está aprendiendo (**C++ para competir**, **Python con mentalidad de
ingeniería**) y quiere pensar cada problema por su cuenta. La skill **verifica** su
razonamiento; no lo reemplaza.

**Al pegar un enunciado** (texto o **foto/captura**), solo:

> Con foto: en las restricciones los exponentes suelen perderse (`105` casi siempre es
> `10⁵`); si un límite no se lee con total claridad, pregúntalo en una línea. Transcribe
> los ejemplos a `tests/` **carácter por carácter** y muéstralos para que el usuario los
> compare con la imagen: un ejemplo mal copiado da un WA falso.

1. Anuncia la plataforma (§1).
2. Prepara la carpeta (§4): `sol.cpp` con la plantilla §3.0 y `solve()` vacío
   (en LeetCode: la firma exacta de la clase con cuerpo vacío y el harness `LOCAL`
   listo), y `tests/N.in` / `N.out` con los ejemplos del enunciado.
3. Recuerda en una línea las ayudas disponibles: `/hint 1–3`, `/structure`,
   `/techniques`, `/input` (pistas por niveles y casos borde) y `verify_limits.py`.
4. **Espera.** Sin idea, sin complejidad objetivo, sin pistas no pedidas.

**Cuando el usuario trae su código** (WA, TLE, RE o "¿está bien?"):
- Ejecuta `verify_limits.py`, y `stress_test.py` si hay `brute` y `gen`.
- Reporta **qué** falla: el veredicto, el contraejemplo mínimo, la salida esperada y
  la obtenida. **No** digas cómo arreglarlo ni reescribas su código, salvo que lo pida.
- Si te pide una pista, da la **más pequeña que lo desbloquee** (una pregunta o una
  observación), no la solución, y recuérdale `/hint`, que además registra el nivel usado.
- `brute` y `gen` se escriben solo si los pide (el brute ya revela una idea).

**Solo cuando lo pida explícitamente** ("resuélvelo", "muéstrame la solución", "dame
el código"):
1. **Primero C++, después Python**, ambos en el formato de la plataforma detectada.
2. En C++ explica: por qué esa estructura de la STL (costes de `vector`, `set`,
   `map`, `unordered_map`, `priority_queue`, `deque`), complejidad temporal y
   espacial, invalidación de iteradores, y trucos de implementación competitiva.
3. En Python explica las decisiones de diseño: separación I/O / lógica, tipado,
   estructuras de `collections`, y en qué se diferencia del rendimiento de C++.
4. Cierra con los **2–3 bloques más interesantes** del código y **un reto corto**
   (variante del problema, optimización o caso borde).

Si pide "solo la solución" o un solo lenguaje, respétalo.

## 7. Checklist de errores clásicos

Revísalo ante cualquier WA / RE / TLE:

- [ ] `int` desbordado (sumas, productos, `a[i] * a[j]`, índices `n*m`).
- [ ] Multitest: variables globales sin reiniciar, salida de un caso mezclada.
- [ ] Casos borde: `n = 1`, todos iguales, todos negativos, arreglo vacío (LeetCode).
- [ ] Leer hasta EOF cuando el juez no da `t` (Beecrowd).
- [ ] `endl` o `cin` sin `sync_with_stdio(false)` en entradas grandes → TLE.
- [ ] `unordered_map` atacado por hacks (Codeforces) → usar `map` o hash con semilla.
- [ ] Recursión profunda (DFS en árbol de 10⁵ nodos en línea) → stack overflow.
- [ ] `assert` no compila: GCC ≥ 16 ya no incluye `<cassert>` en `<bits/stdc++.h>`; añade `#include <cassert>`.
- [ ] Variable con nombre de macro de la plantilla (`all`, `el`, `se`...) o `ri()` mezclado con `cin`.
- [ ] Formato de salida exacto: mayúsculas, espacios finales, decimales (`fixed << setprecision`).
