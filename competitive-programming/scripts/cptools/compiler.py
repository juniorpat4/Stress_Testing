"""Convierte un archivo fuente en el comando (argv) que lo ejecuta."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from .models import LOCAL_DIR, BuildProfile

CPP_SUFFIXES = {".cpp", ".cc", ".cxx"}


class CompileError(Exception):
    """El compilador rechazó el código; el mensaje trae su salida."""


def build(source: Path, profile: BuildProfile, out_dir: Path) -> list[str]:
    """Compila si hace falta y devuelve el argv listo para ejecutar."""
    if source.suffix == ".py":
        return [sys.executable, str(source)]  # Python no tiene perfiles: LOCAL=1 lo pone el runner
    if source.suffix in CPP_SUFFIXES:
        return [str(_compile_cpp(source, profile, out_dir))]
    raise ValueError(f"Extensión no soportada: {source.suffix} (usa .cpp o .py)")


def _compile_cpp(source: Path, profile: BuildProfile, out_dir: Path) -> Path:
    compiler = shutil.which("g++")
    if compiler is None:
        raise CompileError("No se encontró g++ en el PATH")

    exe = out_dir / f"{source.stem}_{profile.name}"
    proc = subprocess.run(
        [compiler, *profile.flags, f"-I{LOCAL_DIR}", str(source), "-o", str(exe)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise CompileError(proc.stderr)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr, end="")  # warnings: compila, pero conviene verlos
    return exe
