"""Pruebas del núcleo: python3 -m unittest discover -s scripts"""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

import stress_test
from cptools.models import DEBUG, RELEASE, RunResult, Verdict, judge, outputs_match
from cptools.runner import CheckerError, make_comparator, run


def py(code: str) -> list[str]:
    return [sys.executable, "-c", code]


class RunnerTest(unittest.TestCase):
    def test_echo_and_local_env(self) -> None:
        result = run(py("import os,sys; print(os.environ['LOCAL'], sys.stdin.read().strip())"), b"hola", 5)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.split(), ["1", "hola"])

    def test_generators_are_importable(self) -> None:
        self.assertEqual(run(py("import cpgen"), b"", 5).returncode, 0)

    def test_timeout_kills(self) -> None:
        result = run(py("while True: pass"), b"", 0.3)
        self.assertTrue(result.timed_out)
        self.assertGreater(result.cpu_time, 0.1)

    def test_crash_is_nonzero(self) -> None:
        result = run(py("import os,signal; os.kill(os.getpid(), signal.SIGSEGV)"), b"", 5)
        self.assertEqual(result.returncode, -11)

    def test_memory_is_measured(self) -> None:
        result = run(py("x = bytearray(100 * 1024 * 1024); x[::4096] = b'1' * len(x[::4096])"), b"", 10)
        self.assertGreater(result.memory_mb, 100)


class JudgeTest(unittest.TestCase):
    def ok_result(self, stdout: str = "1 2\n", cpu: float = 0.1, mem: float = 10) -> RunResult:
        return RunResult(0, stdout, "", cpu, mem, False)

    def test_token_comparison_ignores_whitespace(self) -> None:
        self.assertIs(judge(self.ok_result("1   2"), "1\n2\n", RELEASE, 1, 256), Verdict.OK)
        self.assertIs(judge(self.ok_result("1 3"), "1 2", RELEASE, 1, 256), Verdict.WA)

    def test_limits_only_enforced_in_release(self) -> None:
        slow = self.ok_result(cpu=5, mem=999)
        self.assertIs(judge(slow, None, RELEASE, 1, 256), Verdict.TLE)
        self.assertIs(judge(self.ok_result(mem=999), None, RELEASE, 1, 256), Verdict.MLE)
        self.assertIs(judge(slow, None, DEBUG, 1, 256), Verdict.OK)


class CompareTest(unittest.TestCase):
    def test_eps(self) -> None:
        self.assertTrue(outputs_match("3.1415926 yes", "3.14159265 yes", 1e-6))
        self.assertTrue(outputs_match("1000000.5", "1000000.0", 1e-6))  # relativo
        self.assertFalse(outputs_match("3.2", "3.1", 1e-6))
        self.assertFalse(outputs_match("YES", "yes", 1e-6))
        self.assertFalse(outputs_match("1 2", "1", 1e-6))
        self.assertFalse(outputs_match("3.1415926", "3.14159265"))  # sin eps: exacto

    def test_checker_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            checker = Path(tmp, "check.py")
            checker.write_text("import sys; got = int(open(sys.argv[3]).read()); sys.exit(0 if got % 2 == 0 else 1 if got > 0 else 3)")
            compare = make_comparator([sys.executable, str(checker)], None)
            self.assertTrue(compare(b"", "4", "2"))
            self.assertFalse(compare(b"", "3", "2"))
            with self.assertRaises(CheckerError):
                compare(b"", "-1", "2")


class StressTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)

    def stress(self, files: dict[str, str], *extra: str) -> int:
        """Escribe los programas en la carpeta temporal y corre stress_test sin imprimir."""
        for name, code in files.items():
            (self.dir / name).write_text(code)
        args = [arg for role in ("sol", "brute", "gen") for arg in (f"--{role}", str(self.dir / f"{role}.py"))]
        with contextlib.redirect_stdout(io.StringIO()):
            return stress_test.main([*args, *extra])

    def test_finds_and_saves_counterexample(self) -> None:
        """sol falla solo cuando la entrada es 0: el stress debe encontrarlo y guardarlo."""
        code = self.stress({
            "gen.py": "import sys, random; print(random.Random(int(sys.argv[1])).randint(0, 3))",
            "brute.py": "print(int(input()) * 2)",
            "sol.py": "x = int(input()); print(x * 2 if x else 1)",
        }, "--iters", "200")

        self.assertEqual(code, 1)
        saved = list((self.dir / "tests").glob("stress_*.in"))
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0].read_text().strip(), "0")
        self.assertEqual(saved[0].with_suffix(".out").read_text().strip(), "0")

    def test_checker_accepts_other_valid_answers(self) -> None:
        """Imprimir cualquier múltiplo de n: sol y brute difieren, pero ambos son correctos."""
        self.assertEqual(self.stress({
            "gen.py": "import sys, random; print(random.Random(int(sys.argv[1])).randint(1, 9))",
            "brute.py": "print(input())",
            "sol.py": "print(2 * int(input()))",
            "check.py": "import sys; n, got = (int(open(f).read()) for f in (sys.argv[1], sys.argv[3])); sys.exit(got % n != 0)",
        }, "--iters", "20"), 1)  # sin checker: WA falso
        self.assertEqual(self.stress({}, "--iters", "20", "--checker", str(self.dir / "check.py")), 0)


if __name__ == "__main__":
    unittest.main()
