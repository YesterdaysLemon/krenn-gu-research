from __future__ import annotations

import argparse
import io
import json
import unittest
from unittest import mock

import verify_p5_h31_component_chart_boundary_marked_fibre as verifier


class H31ChartBoundaryMarkedFibreReconciliationTests(unittest.TestCase):
    def test_exact_projection_component_cover(self) -> None:
        self.assertEqual(
            verifier.check_projection_reconciliation(),
            {
                "irreducible_projection_components": 13,
                "generic_rational_basis_records": 13,
                "exceptional_basis_records": 3,
                "locally_closed_certificate_records": 16,
                "projection_closure_artifact_loci": 2,
            },
        )

    def test_all_exact_factor_records(self) -> None:
        self.assertEqual(verifier.check_factor_records(), 16)

    def test_exceptional_records_and_overlap_assignments(self) -> None:
        records = {
            (record.distinguished, record.name): record
            for record in verifier.certificate_records()
        }
        self.assertEqual(len(records), 16)
        self.assertEqual(len(verifier.EXCEPTIONAL_BASIS_RECORDS), 3)
        self.assertIn(
            verifier.sp.Symbol("t0"),
            records[(2, "A1_axis_generic")].nonzero,
        )
        self.assertIn(
            verifier.sp.Symbol("R"),
            records[(3, "t0_zero")].nonzero,
        )

    def test_selected_unit_ideal_caller_checks_all_orientations(self) -> None:
        def fake_program(distinguished: int) -> tuple[str, int]:
            return f"program-{distinguished}", distinguished + 10

        def fake_run(program: str, timeout: float = 90) -> str:
            distinguished = int(program.rsplit("-", 1)[1])
            self.assertEqual(timeout, 123)
            return (
                f"Q={distinguished}_SELECTED\n"
                "BASIS_SIZE\n"
                "1\n"
                "basis[1]=1\n"
            )

        with (
            mock.patch.object(verifier, "selected_program", fake_program),
            mock.patch.object(verifier, "run_singular", fake_run),
        ):
            results = verifier.check_selected_unit_ideals(123)
        self.assertEqual(
            tuple(item["distinguished"] for item in results),
            tuple(range(4)),
        )
        self.assertTrue(all(item["unit_ideal"] for item in results))

    def test_cli_runs_selected_unit_ideals_by_default(self) -> None:
        with mock.patch("sys.argv", ["verifier"]):
            self.assertTrue(verifier.parse_args().selected_unit_ideals)
        with mock.patch(
            "sys.argv",
            ["verifier", "--no-selected-unit-ideals"],
        ):
            self.assertFalse(verifier.parse_args().selected_unit_ideals)

    def _run_patched_main(self, selected: bool) -> tuple[dict, mock.Mock]:
        permanent_values = iter(
            [2 * verifier.sp.Symbol("A")] + [verifier.sp.Integer(0)] * 15
        )
        selected_results = tuple(
            {
                "distinguished": q,
                "unit_ideal": True,
                "product_count": q,
            }
            for q in range(4)
        )
        selected_check = mock.Mock(return_value=selected_results)
        dummy_rows = ((0, 0, 0, 0),) * 4
        cover = {
            "irreducible_projection_components": 13,
            "generic_rational_basis_records": 13,
            "exceptional_basis_records": 3,
            "locally_closed_certificate_records": 16,
            "projection_closure_artifact_loci": 2,
        }
        stdout = io.StringIO()
        with (
            mock.patch.object(
                verifier,
                "parse_args",
                return_value=argparse.Namespace(
                    selected_unit_ideals=selected,
                    selected_timeout=123.0,
                ),
            ),
            mock.patch.object(verifier, "check_normalization"),
            mock.patch.object(
                verifier,
                "rows",
                return_value=(dummy_rows, dummy_rows),
            ),
            mock.patch.object(
                verifier,
                "permanent",
                side_effect=lambda _rows: next(permanent_values),
            ),
            mock.patch.object(
                verifier,
                "singular_program",
                side_effect=lambda q: str(q),
            ),
            mock.patch.object(
                verifier,
                "run_singular",
                side_effect=lambda program, timeout=90: program,
            ),
            mock.patch.object(
                verifier,
                "projection_basis",
                side_effect=lambda output: verifier.EXPECTED_PROJECTION[
                    int(output)
                ],
            ),
            mock.patch.object(
                verifier,
                "check_projection_reconciliation",
                return_value=cover,
            ),
            mock.patch.object(
                verifier,
                "check_factor_records",
                return_value=16,
            ),
            mock.patch.object(
                verifier,
                "check_selected_unit_ideals",
                selected_check,
            ),
            mock.patch.object(verifier, "sha256", return_value="frozen"),
            mock.patch("sys.stdout", stdout),
        ):
            verifier.main()
        return json.loads(stdout.getvalue()), selected_check

    def test_main_runs_and_reports_selected_unit_ideals_by_default(self) -> None:
        report, selected_check = self._run_patched_main(True)
        selected_check.assert_called_once_with(123.0)
        self.assertEqual(
            report["selected_saturation_unit_ideal_runs"]["completed"],
            4,
        )
        self.assertTrue(report["selected_saturation_exhaustiveness_confirmed"])

    def test_main_opt_out_reports_no_selected_exhaustiveness(self) -> None:
        report, selected_check = self._run_patched_main(False)
        selected_check.assert_not_called()
        self.assertEqual(
            report["selected_saturation_unit_ideal_runs"]["completed"],
            0,
        )
        self.assertFalse(report["selected_saturation_exhaustiveness_confirmed"])


if __name__ == "__main__":
    unittest.main()
