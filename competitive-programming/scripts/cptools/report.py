"""Explica por qué falló una ejecución (lo comparten los dos CLIs)."""

from __future__ import annotations

from .models import RunResult, Verdict, outputs_match

STDERR_TAIL_LINES = 25


def report_failure(
    result: RunResult, expected: str | None, verdict: Verdict, eps: float | None = None
) -> None:
    if verdict is Verdict.RE:
        tail = result.stderr.strip().splitlines()[-STDERR_TAIL_LINES:]
        print(f"    código de salida {result.returncode}; stderr (últimas líneas):")
        for line in tail:
            print(f"    | {line}")
    elif verdict is Verdict.WA and expected is not None:
        got_lines, exp_lines = result.stdout.splitlines(), expected.splitlines()
        for i in range(max(len(got_lines), len(exp_lines))):
            got = got_lines[i] if i < len(got_lines) else "<nada>"
            exp = exp_lines[i] if i < len(exp_lines) else "<nada>"
            if not outputs_match(got, exp, eps):
                print(f"    línea {i + 1}: esperado {exp!r}, obtenido {got!r}")
                break
