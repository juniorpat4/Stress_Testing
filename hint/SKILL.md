---
name: hint
description: >
  Escalera de pistas para un problema de programación competitiva: /hint 1 da una
  observación, /hint 2 la familia de la técnica y /hint 3 el invariante clave. Registra
  el nivel que necesitaste para repasar esos problemas después. Se invoca solo con /hint.
argument-hint: "[1|2|3] [enunciado o enlace; vacío = el problema actual]"
disable-model-invocation: true
---

# /hint: escalera de pistas

Argumentos: $ARGUMENTS

- **Nivel:** el primer número (1, 2 o 3). Sin número: el siguiente al último que se dio
  para este problema en la conversación, o 1 si no hubo ninguno.
- **Problema:** el resto de los argumentos; si no hay, el problema de la conversación.
  Si no hay ninguno, pide el enunciado en una línea y detente.

El enunciado puede venir como **imagen** (captura o foto): léela. Si un límite de las
restricciones no se lee con total claridad (`105` casi siempre es `10⁵`), pregúntalo antes.

## Los tres niveles

| Nivel | Da | Ejemplo (subarreglo más corto con suma ≥ S, valores positivos) |
|---|---|---|
| 1 | **Observación**: una propiedad del enunciado que desbloquea, sin nombrar técnica ni estructura | "Como todos los valores son positivos, ¿qué le pasa a la suma si alargas el subarreglo?" |
| 2 | **Familia** de la técnica, sin explicar cómo aplicarla | "Dos punteros." |
| 3 | **Invariante clave**: la idea que hace correcto al algoritmo, sin pasos completos | "Para cada `r`, el mejor `l` nunca retrocede cuando `r` avanza." |

Reglas:
- **Una sola pista** del nivel pedido, en 1–2 frases. Nunca reveles un nivel superior.
- **Nunca código** ni la solución paso a paso.
- Si pide el nivel 3 directamente, dáselo: es su decisión.

## Registro

Después de dar la pista, actualiza el registro de estudio:

- **Ruta:** resuelve el enlace simbólico del directorio base de esta skill
  (`realpath <directorio base>`) y usa `../problems/HINTS.md` relativo a él.
- Si el archivo está **vacío o no existe**, escribe primero este encabezado:

  ```
  # Registro de pistas

  | Fecha | Problema | Nivel máximo |
  |---|---|---|
  ```

- Si el problema **ya tiene fila**, actualiza el nivel solo si el nuevo es mayor, y la
  fecha. Si no, agrega una fila al final.
- **Problema** = nombre corto + plataforma e ID, o el enlace (ej. `CSES 1643 Maximum
  Subarray Sum`). **Nunca** escribas la pista ni la idea en el registro.

## Cierre

Termina con una línea: *"Registrado: <problema> → nivel N. Si sigues atascado: `/hint N+1`."*
En el nivel 3: *"Registrado: <problema> → nivel 3. Es la última pista: con esto deberías
poder escribirlo."*
