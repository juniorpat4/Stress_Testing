# Skills de programación competitiva para Claude Code

Un conjunto de skills de [Claude Code](https://claude.com/claude-code) para practicar
programación competitiva y entrevistas de código en **C++** y **Python**, en jueces de
entrada estándar (Codeforces, AtCoder, OmegaUp, Beecrowd, CSES) y en LeetCode.

La idea central: **tú piensas el problema; las herramientas comprueban tu razonamiento.**
Por defecto nada te da la solución: preparan el problema, te dan pistas cuando las pides
y buscan contraejemplos a tu código.

## Contenido

| Carpeta | Qué es |
|---|---|
| `competitive-programming/` | Skill principal: detecta la plataforma, prepara la carpeta del problema y verifica tu código. Incluye los scripts y la librería de generadores. |
| `structure/` | Comando `/structure`: estructuras de datos candidatas para el problema (pistas → veredicto). |
| `techniques/` | Comando `/techniques`: técnicas candidatas (búsqueda binaria, dos punteros, DP…), en dos niveles. |
| `input/` | Comando `/input`: 3 casos borde con su output, verificado ejecutando un brute force. |
| `hint/` | Comando `/hint 1–3`: escalera de pistas (observación → familia de técnica → invariante clave). Anota en `problems/HINTS.md` el nivel que necesitaste. |
| `problems/` | Problemas resueltos y verificados que sirven de ejemplo de uso (ver abajo). |

## Requisitos

- **Linux** (los scripts usan `os.wait4` y `ru_maxrss` en KiB).
- **g++** con C++20 (las plantillas usan `<bits/stdc++.h>` y `_GLIBCXX_DEBUG`, propios de GCC).
- **Python ≥ 3.10**.
- Claude Code.

## Instalación

Cada skill se instala con un enlace simbólico en `~/.claude/skills`. Desde la raíz del repo:

```bash
for skill in competitive-programming structure techniques input hint; do ln -s "$PWD/$skill" ~/.claude/skills/$skill; done
```

Reinicia la sesión de Claude Code para que cargue las skills.

## Uso

- **Pega un enunciado** (texto o captura de pantalla). La skill detecta la plataforma, crea
  `sol.cpp` con la plantilla y `tests/` con los ejemplos, y espera. Solo escribe la solución
  si se lo pides ("resuélvelo").
- **`/structure`, `/techniques`, `/input`** sobre el problema actual. Los dos primeros
  muestran primero candidatas sin veredicto; al pedir «¿cuál?», antes te preguntan qué
  complejidad esperas y califican tu razonamiento.
- **`/hint 1`, `/hint 2`, `/hint 3`**: una pista cada vez más fuerte. `problems/HINTS.md`
  empieza vacío y guarda qué nivel necesitaste en cada problema, para repasarlos después.
- **Trae tu código con WA/TLE/RE**: la skill ejecuta los scripts y te dice qué falla (el
  contraejemplo), sin reescribir tu solución.

Los scripts también se usan solos:

```bash
python3 competitive-programming/scripts/verify_limits.py problems/cf600b/sol.cpp
```

```bash
python3 competitive-programming/scripts/stress_test.py --sol problems/cses1643/sol.cpp --brute problems/cses1643/brute.cpp --gen problems/cses1643/gen.py --iters 300
```

- `verify_limits.py`: compila en perfil **debug** (ASan, UBSan, `_GLIBCXX_DEBUG`) y
  **release** (`-O2`), ejecuta `tests/*.in` y compara con `.out`; mide tiempo de CPU y
  memoria. Acepta `--eps` (decimales) y `--checker` (varias respuestas válidas).
- `stress_test.py`: compara `sol` contra `brute` con entradas de `gen` hasta encontrar un
  contraejemplo, y lo guarda en `tests/` como test de regresión.

## Ejemplos en `problems/`

| Problema | Plataforma | Qué muestra |
|---|---|---|
| `cf600b` | Codeforces 600B | `sort` + `upper_bound`; caso máximo en release |
| `cses1643` | CSES 1643 | Kadane; el stress encontró el bug `best = 0` (`tests/stress_2.in`) |
| `cses1131` | CSES 1131 | Diámetro con doble BFS; generador de árboles `line`/`star` |
| `lc239` | LeetCode 239 | Deque monótono; harness `#ifdef LOCAL` |
| `lc226` | LeetCode 226 | Árboles: `TreeNode` y literales `[1,null,2]` en local |
| `lc206` | LeetCode 206 | Listas enlazadas: `ListNode` en local |

Cada uno tiene la solución en C++ y en Python. Los `tests/` contienen los ejemplos de
entrada y salida de cada enunciado; los enunciados no están incluidos.

## Pruebas

```bash
python3 -m unittest discover -s competitive-programming/scripts
```

```bash
python3 -m unittest discover -s competitive-programming/generators
```

```bash
python3 -m unittest discover -s competitive-programming/local
```

## Limitaciones conocidas

- No funciona en macOS (clang no trae `<bits/stdc++.h>`, y `ru_maxrss` viene en bytes) ni en Windows.
- La memoria medida nunca baja de ~12 MB: Linux hereda el pico del proceso Python padre.
- No soporta problemas interactivos.

## Licencia

[MIT](LICENSE).
