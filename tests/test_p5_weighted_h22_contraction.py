"""Bounded parity and consumer-graph tests for the weighted-H22 core."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import sympy as sp


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from krenn_gu import p5_weighted_h22_contraction as shared  # noqa: E402
from krenn_gu.bootstrap import expose_claim_package  # noqa: E402

ADAPTER_PACKAGE = (
    "claims/p5/h22/"
    "common-active-binary-triangle-component-generic"
)
ADAPTER_MODULE = (
    "derive_p5_h22_common_active_binary_triangle_"
    "component_generic_obstruction_candidate"
)
expose_claim_package(REPO_ROOT, ADAPTER_PACKAGE)
adapter = __import__(ADAPTER_MODULE)


class WeightedH22ContractionParityTests(unittest.TestCase):
    """Check the infrastructure extraction without replaying any solver."""

    def setUp(self) -> None:
        self.alpha = (
            (sp.Rational(1, 2), 2, -1, 3),
            (4, sp.Rational(-2, 3), 5, 1),
            (0, 7, sp.Rational(3, 5), -4),
            (2, -3, 6, sp.Rational(5, 7)),
        )
        self.beta = (
            (-2, 1, 4, sp.Rational(1, 3)),
            (3, -5, 2, 7),
            (sp.Rational(4, 9), 6, -3, 2),
            (5, sp.Rational(-1, 4), 1, -6),
        )
        self.extensions = tuple(sp.Rational(i, i + 1) for i in range(1, 9))

    def test_public_words_and_permanent_match_claim_adapter(self) -> None:
        self.assertEqual(shared.WORDS, adapter.WORDS)
        matrix = (
            (1, 2, 3, 4),
            (sp.Rational(1, 2), -1, 5, 2),
            (3, 0, sp.Rational(2, 3), -2),
            (4, -3, 1, sp.Rational(5, 7)),
        )
        self.assertEqual(shared.permanent4(matrix), adapter.permanent4(matrix))

    def test_all_projection_charts_match_claim_adapter(self) -> None:
        row = (sp.Rational(2, 3), -4, 5, sp.Rational(7, 2))
        extension = sp.Rational(-3, 8)
        slope = sp.Rational(5, 11)
        for direction in ("D01", "D23"):
            with self.subTest(direction=direction, chart="finite"):
                self.assertEqual(
                    shared.project(row, extension, direction, "finite", slope),
                    adapter.project(row, extension, direction, "finite", slope),
                )
            with self.subTest(direction=direction, chart="infinity"):
                self.assertEqual(
                    shared.project(row, extension, direction, "infinity"),
                    adapter.project(row, extension, direction, "infinity"),
                )

    def test_all_sixteen_coefficients_match_in_every_chart(self) -> None:
        for direction in ("D01", "D23"):
            for chart, slope in (
                ("finite", sp.Rational(5, 11)),
                ("infinity", None),
            ):
                with self.subTest(direction=direction, chart=chart):
                    actual = shared.build_model(
                        self.alpha,
                        self.beta,
                        self.extensions,
                        direction,
                        chart,
                        slope,
                    )
                    expected = adapter.build_model(
                        self.alpha,
                        self.beta,
                        self.extensions,
                        direction,
                        chart,
                        slope,
                    )
                    self.assertEqual(actual["coefficients"], expected["coefficients"])
                    self.assertEqual(actual["mixed"], expected["mixed"])
                    self.assertEqual(actual["A"], expected["A"])
                    self.assertEqual(actual["B"], expected["B"])


class WeightedH22ConsumerGraphTests(unittest.TestCase):
    """Pin the inverse-taper boundary established by Stage 31."""

    def test_shared_core_has_39_consumers_and_adapter_has_one(self) -> None:
        shared_consumers: list[str] = []
        adapter_consumers: list[tuple[str, tuple[str, ...]]] = []
        for path in REPO_ROOT.rglob("*.py"):
            if any(part in {".git", "__pycache__"} for part in path.parts):
                continue
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            relative = path.relative_to(REPO_ROOT).as_posix()
            for node in ast.walk(tree):
                if not isinstance(node, ast.ImportFrom):
                    continue
                if node.module == "krenn_gu.p5_weighted_h22_contraction":
                    shared_consumers.append(relative)
                if node.module == ADAPTER_MODULE:
                    adapter_consumers.append(
                        (relative, tuple(alias.name for alias in node.names))
                    )

        self.assertEqual(len(shared_consumers), 39)
        self.assertEqual(len(set(shared_consumers)), 39)
        self.assertEqual(
            adapter_consumers,
            [
                (
                    "claims/p5/h22/"
                    "common-center-kernel-star-component-s-zero-k-infinity-"
                    "coordinate-survivor/"
                    "verify_p5_h22_common_center_kernel_star_component_s_zero_"
                    "k_infinity_coordinate_survivor.py",
                    ("singular_command",),
                )
            ],
        )


class WeightedH22DependencyPinTests(unittest.TestCase):
    """Keep the moved wall ledger's text hashes cross-platform and live."""

    def test_lf_normalized_dependency_pins_resolve(self) -> None:
        package = (
            REPO_ROOT
            / "claims/p5/h22/disputed-ownership/p-plus-q-wall"
        )
        checker_path = package / "audit_p5_h22_p_plus_q_diagonal_dvr_coverage.py"
        spec = importlib.util.spec_from_file_location("p5_h22_wall_coverage", checker_path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)

        ledger = json.loads(
            (package / "p5_h22_p_plus_q_diagonal_dvr_coverage.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(len(ledger["dependencies"]), 16)
        for key, dependency in ledger["dependencies"].items():
            with self.subTest(dependency=key):
                self.assertEqual(
                    checker.sha256(REPO_ROOT / dependency["path"]),
                    dependency["sha256"],
                )

        with tempfile.TemporaryDirectory() as raw_tmp:
            sample = Path(raw_tmp) / "sample.txt"
            sample.write_bytes(b"alpha\r\nbeta\r\n")
            self.assertEqual(
                checker.sha256(sample),
                hashlib.sha256(b"alpha\nbeta\n").hexdigest(),
            )


if __name__ == "__main__":
    unittest.main()
