---
name: input
description: >
  Da 3 inputs clave y raros (casos borde) para entender o romper un problema de
  programación competitiva, cada uno con su output verificado ejecutando un brute force.
  Se invoca solo con /input.
argument-hint: "[enunciado o enlace; vacío = el problema actual]"
disable-model-invocation: true
---

# /input: 3 casos clave con su output

Problema: $ARGUMENTS

Si está vacío, usa el problema que se está resolviendo en la conversación. Si no hay
ninguno, pide el enunciado en una línea y detente.

El enunciado puede venir como **imagen** (captura o foto) adjunta o en un mensaje anterior:
léela. En las restricciones, los exponentes suelen perderse (`105` casi siempre es `10⁵`,
`2·105` es `2·10⁵`): si un límite no se lee con total claridad, **pregúntalo en una línea
antes de seguir**, porque cambia la complejidad objetivo.

## Pasos

1. Lee las restricciones exactas. **Todo input debe cumplirlas**: un caso inválido no
   enseña nada.
2. Elige los **3 casos más peligrosos para este problema** de esta lista (uno por categoría):
   - **mínimo**: `n = 1`, `k = n`, arreglo o árbol vacío (LeetCode), un solo nodo;
   - **valores extremos**: todos negativos, ceros, `10⁹` (overflow de `int` con pocos elementos);
   - **todo igual** o duplicados;
   - **estructura degenerada**: árbol en línea o estrella, grafo desconectado, ciclo;
   - **"no existe"**: el caso que exige imprimir `-1`, `NO` o el vacío;
   - **la trampa del greedy obvio**: el contraejemplo de la idea ingenua;
   - **orden**: ya ordenado, orden inverso.
3. Mantén cada input **pequeño** (que se lea de un vistazo, ~20 números como mucho).
   El tamaño máximo no se muestra: para TLE se usa `cpgen` + `verify_limits.py`.
4. **Nunca calcules un output de cabeza.** Obtén cada uno ejecutando:
   - el `brute.*` de la carpeta del problema si existe; si no,
   - un brute force directo en Python escrito en el scratchpad (`itertools`, todos los
     subconjuntos o subarreglos: lento pero obviamente correcto).
5. Si existe un `sol.*` del usuario, ejecútalo también con los 3 inputs. Si discrepa del
   brute, **dilo primero**: es un bug encontrado.
6. Formato de entrada de la plataforma: stdin del juez, o en LeetCode un argumento
   por línea con literales (`[1,null,2]`). No guardes archivos salvo que el usuario lo pida
   (si lo pide: `tests/edge_N.in` / `.out`, y `verify_limits.py` los usa solos).

## Formato de salida

Por cada caso:

### Caso N: <categoría> (qué error atrapa, en una frase)

```
<input exacto>
```

**Output:** `<output>`. Una línea con el porqué de ese resultado.

Termina con una línea: **"Verificado con: brute.cpp"** (o el brute de Python, o la
discrepancia con `sol.*` si la hubo).
