#!/usr/bin/env python3
"""Busca un contraejemplo comparando sol contra brute con entradas aleatorias de gen.

Ejemplo:
  stress_test.py --sol sol.cpp --brute brute.cpp --gen gen.py --iters 1000

Contrato del generador: recibe la semilla como único argumento e imprime UN caso.
Al encontrar un fallo guarda el caso en tests/stress_<seed>.in/.out junto a sol,
así verify_limits.py lo vuelve a probar como test de regresión.

Códigos de salida: 0 sin contraejemplos, 1 contraejemplo encontrado,
2 error (compilación, o gen/brute fallan: en ellos se confía, no se juzgan).
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from cptools.compiler import CompileError, build
from cptools.models import PROFILES, RELEASE, RunResult, Verdict, judge
from cptools.report import report_failure
from cptools.runner import CheckerError, make_comparator, run

PREVIEW_CHARS = 1500
BRUTE_TIME_FACTOR = 10.0  # brute es lento a propósito: solo se le pide que termine


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--sol", type=Path, required=True, help="solución a probar")
    parser.add_argument("--brute", type=Path, required=True, help="fuerza bruta de confianza")
    parser.add_argument("--gen", type=Path, required=True, help="generador: `gen <seed>` imprime un caso")
    parser.add_argument("--iters", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=1, help="primera semilla (default 1)")
    parser.add_argument(
        "--profile", choices=list(PROFILES), default="debug",
        help="perfil de sol (default debug: un UB aparece como RE)",
    )
    parser.add_argument("--tl", type=float, default=2.0, help="límite de tiempo en segundos")
    parser.add_argument("--ml", type=float, default=256.0, help="límite de memoria en MB")
    parser.add_argument("--eps", type=float, help="tolerancia para números (abs. o relativa)")
    parser.add_argument("--checker", type=Path, help="`checker <in> <esperado> <obtenido>`: 0 acepta, 1 rechaza")
    return parser.parse_args(argv)


def preview(text: str) -> str:
    return text if len(text) <= PREVIEW_CHARS else text[:PREVIEW_CHARS] + "\n... (recortado)"


def trusted_failed(name: str, result: RunResult, seed: int) -> bool:
    """gen y brute no se juzgan: si fallan, el problema está en ellos, no en sol."""
    if result.returncode == 0 and not result.timed_out:
        return False
    reason = "excedió el tiempo" if result.timed_out else f"terminó con código {result.returncode}"
    print(f"\nerror: {name} {reason} con seed {seed}", file=sys.stderr)
    print(preview(result.stderr), file=sys.stderr)
    return True


def save_case(tests_dir: Path, seed: int, data: str, expected: str) -> Path:
    tests_dir.mkdir(exist_ok=True)
    inp = tests_dir / f"stress_{seed}.in"
    inp.write_text(data)
    inp.with_suffix(".out").write_text(expected)
    return inp


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    sol_src, brute_src, gen_src = (p.resolve() for p in (args.sol, args.brute, args.gen))
    for src in (sol_src, brute_src, gen_src):
        if not src.is_file():
            print(f"error: no existe {src}", file=sys.stderr)
            return 2
    # Igual que verify_limits: los perfiles solo cambian flags de g++.
    sol_profile = RELEASE if sol_src.suffix == ".py" else PROFILES[args.profile]

    with tempfile.TemporaryDirectory(prefix="cp_stress_") as build_dir:
        out_dir = Path(build_dir)
        try:
            sol = build(sol_src, sol_profile, out_dir)
            brute = build(brute_src, RELEASE, out_dir)
            gen = build(gen_src, RELEASE, out_dir)
            checker = build(args.checker.resolve(), RELEASE, out_dir) if args.checker else None
        except (CompileError, ValueError) as err:
            print(f"error de compilación:\n{err}", file=sys.stderr)
            return 2
        compare = make_comparator(checker, args.eps)

        print(f"Stress: {sol_src.name} ({sol_profile.name}) vs {brute_src.name} · gen {gen_src.name}")
        for i in range(args.iters):
            seed = args.seed + i
            case = run([*gen, str(seed)], b"", args.tl * RELEASE.time_factor)
            if trusted_failed("gen", case, seed):
                return 2
            data = case.stdout.encode()

            expected = run(brute, data, args.tl * BRUTE_TIME_FACTOR)
            if trusted_failed("brute", expected, seed):
                return 2

            got = run(sol, data, args.tl * sol_profile.time_factor)
            try:
                verdict = judge(got, expected.stdout, sol_profile, args.tl, args.ml,
                                same=lambda g, e: compare(data, g, e))
            except CheckerError as err:
                print(f"\nerror del checker con seed {seed}: {err}", file=sys.stderr)
                return 2
            if verdict is not Verdict.OK:
                print(f"\n✗ {verdict.value} con seed {seed} (iteración {i + 1})")
                print(f"--- entrada ---\n{preview(case.stdout)}")
                print(f"--- esperado (brute) ---\n{preview(expected.stdout)}")
                print(f"--- obtenido (sol) ---\n{preview(got.stdout)}")
                report_failure(got, expected.stdout, verdict, args.eps)
                saved = save_case(sol_src.parent / "tests", seed, case.stdout, expected.stdout)
                print(f"Guardado como test de regresión: {saved}")
                return 1
            if sys.stdout.isatty():  # el \r solo tiene sentido en una terminal, no en logs
                print(f"\r  {i + 1}/{args.iters} casos OK", end="", flush=True)

    print(f"\n✓ Sin contraejemplos en {args.iters} casos (seeds {args.seed}..{args.seed + args.iters - 1})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
