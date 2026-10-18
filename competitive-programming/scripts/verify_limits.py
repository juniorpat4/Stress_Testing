#!/usr/bin/env python3
"""Compila una solución, la ejecuta contra casos de prueba y mide tiempo y memoria.

Ejemplos:
  verify_limits.py sol.cpp                    # usa tests/ junto a sol.cpp, perfiles debug + release
  verify_limits.py sol.cpp --input max.in --profile release --tl 1 --ml 256
  verify_limits.py sol.py --tests tests/      # Python: se ejecuta con LOCAL=1
  verify_limits.py sol.cpp --eps 1e-6         # decimales con tolerancia
  verify_limits.py sol.cpp --checker check.py # varias respuestas válidas

Códigos de salida: 0 todo OK, 1 algún caso falló, 2 error de compilación o de uso.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from cptools.compiler import CompileError, build
from cptools.models import PROFILES, RELEASE, BuildProfile, Verdict, judge
from cptools.report import report_failure
from cptools.runner import CheckerError, make_comparator, run


@dataclass(frozen=True, slots=True)
class TestCase:
    name: str
    input_path: Path
    expected_path: Path | None  # sin .out solo se comprueba que no falle ni exceda límites


def collect_cases(tests_dir: Path | None, inputs: list[Path]) -> list[TestCase]:
    cases = [TestCase(p.name, p, None) for p in inputs]
    if tests_dir is not None:
        for inp in sorted(tests_dir.glob("*.in"), key=_natural_key):
            out = inp.with_suffix(".out")
            cases.append(TestCase(inp.name, inp, out if out.exists() else None))
    return cases


def _natural_key(path: Path) -> tuple[int, str]:
    """Ordena 2.in antes que 10.in."""
    return (int(path.stem), "") if path.stem.isdigit() else (sys.maxsize, path.stem)


def select_profiles(source: Path, choice: str) -> list[BuildProfile]:
    if source.suffix == ".py":
        return [RELEASE]  # los perfiles solo cambian flags de g++
    if choice == "both":
        return list(PROFILES.values())
    return [PROFILES[choice]]


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("source", type=Path, help="sol.cpp o sol.py")
    parser.add_argument("--tests", type=Path, help="carpeta con N.in / N.out (por defecto: tests/ junto al fuente)")
    parser.add_argument("--input", type=Path, action="append", default=[], help="archivo de entrada suelto (repetible)")
    parser.add_argument("--profile", choices=[*PROFILES, "both"], default="both")
    parser.add_argument("--tl", type=float, default=2.0, help="límite de tiempo en segundos (default 2)")
    parser.add_argument("--ml", type=float, default=256.0, help="límite de memoria en MB (default 256)")
    parser.add_argument("--eps", type=float, help="tolerancia para números (abs. o relativa)")
    parser.add_argument("--checker", type=Path, help="`checker <in> <esperado> <obtenido>`: 0 acepta, 1 rechaza")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    source: Path = args.source.resolve()
    if not source.is_file():
        print(f"error: no existe {source}", file=sys.stderr)
        return 2

    tests_dir = args.tests
    if tests_dir is None and not args.input and (source.parent / "tests").is_dir():
        tests_dir = source.parent / "tests"
    cases = collect_cases(tests_dir, args.input)
    if not cases:
        print("error: no hay casos (usa --tests DIR o --input FILE)", file=sys.stderr)
        return 2

    all_ok = True
    with tempfile.TemporaryDirectory(prefix="cp_build_") as build_dir:
        try:
            checker = build(args.checker.resolve(), RELEASE, Path(build_dir)) if args.checker else None
        except (CompileError, ValueError) as err:
            print(f"[checker] error de compilación:\n{err}", file=sys.stderr)
            return 2
        compare = make_comparator(checker, args.eps)

        for profile in select_profiles(source, args.profile):
            try:
                program = build(source, profile, Path(build_dir))
            except (CompileError, ValueError) as err:
                print(f"[{profile.name}] error de compilación:\n{err}", file=sys.stderr)
                return 2

            note = "" if profile.enforce_limits else "  (tiempo/memoria NO fiables con sanitizers)"
            print(f"== {source.name} · perfil {profile.name} · TL {args.tl:g}s · ML {args.ml:g}MB{note}")
            for case in cases:
                data = case.input_path.read_bytes()
                result = run(program, data, args.tl * profile.time_factor)
                expected = case.expected_path.read_text() if case.expected_path else None
                if expected is None and checker:
                    expected = ""  # un checker puede validar sin .out
                try:
                    verdict = judge(result, expected, profile, args.tl, args.ml,
                                    same=lambda got, exp: compare(data, got, exp))
                except CheckerError as err:
                    print(f"error del checker en {case.name}: {err}", file=sys.stderr)
                    return 2
                compared = "" if expected is not None else "  (sin .out)"
                print(
                    f"  {case.name:<14} {verdict.value:<4} "
                    f"{result.cpu_time * 1000:>8.0f} ms {result.memory_mb:>8.1f} MB{compared}"
                )
                if verdict is not Verdict.OK:
                    all_ok = False
                    report_failure(result, expected, verdict, args.eps)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
