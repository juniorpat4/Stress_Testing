"""Tipos de datos y reglas de veredicto compartidos por los scripts."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
LOCAL_DIR = SKILL_DIR / "local"  # TreeNode/ListNode solo-local: -I para g++, PYTHONPATH para Python
GENERATORS_DIR = SKILL_DIR / "generators"


@dataclass(frozen=True, slots=True)
class BuildProfile:
    name: str
    flags: tuple[str, ...]
    enforce_limits: bool  # con sanitizers el tiempo y la memoria no son fiables
    time_factor: float  # se mata el proceso tras time_factor × TL de reloj


_COMMON = ("-std=c++20", "-DLOCAL")

DEBUG = BuildProfile(
    name="debug",
    flags=_COMMON + (
        "-O1", "-g", "-Wall", "-Wextra", "-Wshadow",
        "-D_GLIBCXX_DEBUG",
        "-fsanitize=address,undefined",
        "-fno-sanitize-recover=all",  # sin esto UBSan avisa pero el programa sigue y termina con 0
        "-fno-omit-frame-pointer",
    ),
    enforce_limits=False,
    time_factor=10.0,
)

RELEASE = BuildProfile(
    name="release",
    flags=_COMMON + ("-O2", "-DNDEBUG"),
    enforce_limits=True,
    time_factor=2.0,
)

PROFILES: dict[str, BuildProfile] = {p.name: p for p in (DEBUG, RELEASE)}


class Verdict(str, Enum):
    OK = "OK"
    WA = "WA"
    TLE = "TLE"
    MLE = "MLE"
    RE = "RE"


@dataclass(frozen=True, slots=True)
class RunResult:
    returncode: int  # negativo = muerto por señal (p. ej. -11 = SIGSEGV)
    stdout: str
    stderr: str
    cpu_time: float  # segundos de CPU (user + sys), lo que miden los jueces
    memory_mb: float  # RSS máximo
    timed_out: bool  # lo matamos por exceder el límite de reloj


def outputs_match(got: str, expected: str, eps: float | None = None) -> bool:
    """Comparación por tokens (ignora espacios y saltos). Con eps, los números se aceptan
    si el error absoluto o relativo es <= eps, como en Codeforces."""
    got_tokens, exp_tokens = got.split(), expected.split()
    if eps is None or len(got_tokens) != len(exp_tokens):
        return got_tokens == exp_tokens
    return all(g == e or _close(g, e, eps) for g, e in zip(got_tokens, exp_tokens))


def _close(got: str, expected: str, eps: float) -> bool:
    try:
        g, e = float(got), float(expected)
    except ValueError:
        return False
    return abs(g - e) <= eps * max(1.0, abs(e))


def judge(
    result: RunResult,
    expected: str | None,
    profile: BuildProfile,
    time_limit: float,
    memory_limit_mb: float,
    same: Callable[[str, str], bool] = outputs_match,  # (obtenido, esperado); un checker la sustituye
) -> Verdict:
    if result.timed_out:
        return Verdict.TLE
    if result.returncode != 0:
        return Verdict.RE
    if profile.enforce_limits:
        if result.cpu_time > time_limit:
            return Verdict.TLE
        if result.memory_mb > memory_limit_mb:
            return Verdict.MLE
    if expected is not None and not same(result.stdout, expected):
        return Verdict.WA
    return Verdict.OK
