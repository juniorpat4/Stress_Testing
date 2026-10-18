"""Ejecuta un programa con límite de tiempo y mide su CPU y memoria máxima."""

from __future__ import annotations

import os
import resource
import signal
import subprocess
import tempfile
import time
from collections.abc import Callable
from pathlib import Path

from .models import GENERATORS_DIR, LOCAL_DIR, RunResult, outputs_match

Comparator = Callable[[bytes, str, str], bool]  # (entrada, obtenido, esperado) -> ¿aceptado?
CHECKER_WALL_SECONDS = 10.0


class CheckerError(Exception):
    """El checker no aceptó ni rechazó: terminó con un código distinto de 0 y 1."""

# Codeforces da ~256 MB de pila; con los 8 MB por defecto de Linux un DFS
# recursivo de 10^5 niveles daría un RE local que en el juez no existe.
STACK_LIMIT_BYTES = 512 * 1024 * 1024
POLL_SECONDS = 0.001


def _child_env() -> dict[str, str]:
    env = os.environ.copy()
    env["LOCAL"] = "1"  # activa el harness de Python (equivalente a -DLOCAL)
    # Todo gen.py puede `import cpgen` y toda sol.py `from lc_local import TreeNode`.
    env["PYTHONPATH"] = os.pathsep.join(
        filter(None, [str(GENERATORS_DIR), str(LOCAL_DIR), env.get("PYTHONPATH")])
    )
    env.setdefault("ASAN_OPTIONS", "detect_leaks=0")  # un `new TreeNode` sin delete es normal en CP
    env.setdefault("UBSAN_OPTIONS", "print_stacktrace=1")
    return env


def _raise_stack_limit() -> None:
    """Se ejecuta en el hijo entre fork y exec; el nuevo límite rige para el programa."""
    _, hard = resource.getrlimit(resource.RLIMIT_STACK)
    target = STACK_LIMIT_BYTES if hard == resource.RLIM_INFINITY else min(STACK_LIMIT_BYTES, hard)
    resource.setrlimit(resource.RLIMIT_STACK, (target, hard))


def run(argv: list[str], input_data: bytes, wall_limit: float) -> RunResult:
    """Ejecuta argv con input_data por stdin; lo mata si supera wall_limit segundos de reloj."""
    # Archivos temporales en vez de pipes: sin riesgo de deadlock con salidas grandes.
    with (
        tempfile.TemporaryFile() as fin,
        tempfile.TemporaryFile() as fout,
        tempfile.TemporaryFile() as ferr,
    ):
        fin.write(input_data)
        fin.seek(0)

        proc = subprocess.Popen(
            argv, stdin=fin, stdout=fout, stderr=ferr,
            env=_child_env(), preexec_fn=_raise_stack_limit,
        )
        deadline = time.monotonic() + wall_limit
        timed_out = False

        # wait4 (y no proc.wait) porque además devuelve el rusage de ESTE hijo.
        while True:
            pid, status, usage = os.wait4(proc.pid, os.WNOHANG)
            if pid != 0:
                break
            if time.monotonic() > deadline:
                os.kill(proc.pid, signal.SIGKILL)
                _, status, usage = os.wait4(proc.pid, 0)
                timed_out = True
                break
            time.sleep(POLL_SECONDS)

        proc.returncode = os.waitstatus_to_exitcode(status)  # ya está recogido: que Popen no lo espere otra vez

        fout.seek(0)
        ferr.seek(0)
        return RunResult(
            returncode=proc.returncode,
            stdout=fout.read().decode(errors="replace"),
            stderr=ferr.read().decode(errors="replace"),
            cpu_time=usage.ru_utime + usage.ru_stime,
            # shortcut: Linux conserva en ru_maxrss el pico previo al exec (la copia del Python
            # padre, ~12 MB), así que nunca baja de eso; sobrestima, nunca subestima. Medir con
            # un lanzador en C si hace falta precisión cerca del ML.
            memory_mb=usage.ru_maxrss / 1024,  # en Linux ru_maxrss viene en KiB
            timed_out=timed_out,
        )


def make_comparator(checker: list[str] | None, eps: float | None) -> Comparator:
    """Sin checker: comparación por tokens (con eps opcional). Con checker:
    `checker <entrada> <esperado> <obtenido>` y su código decide: 0 acepta, 1 rechaza."""
    if checker is None:
        return lambda _input, got, expected: outputs_match(got, expected, eps)

    def run_checker(input_data: bytes, got: str, expected: str) -> bool:
        with tempfile.TemporaryDirectory(prefix="cp_check_") as tmp:
            paths = [Path(tmp, name) for name in ("input.txt", "expected.txt", "got.txt")]
            paths[0].write_bytes(input_data)
            paths[1].write_text(expected)
            paths[2].write_text(got)
            result = run([*checker, *map(str, paths)], b"", CHECKER_WALL_SECONDS)
        if result.timed_out or result.returncode not in (0, 1):
            raise CheckerError(f"código {result.returncode}\n{result.stderr}")
        return result.returncode == 0

    return run_checker
