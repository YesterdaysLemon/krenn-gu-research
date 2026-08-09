#!/usr/bin/env python3
"""Verify the complete toric marked-fibre obstruction for H31."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import sympy as sp


for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from derive_p5_h31_toric_marked_fibre_elimination import (  # noqa: E402
    marked_rows,
    singular,
    singular_program,
    toric_cases,
)
from p5_high_coordinate_tree_chart_cegar import (  # noqa: E402
    singular_command_with_timeout,
)
from verify_p5_h31_marked_basis_open_branch import (  # noqa: E402
    marked_extension,
    mixed_matrix,
    one_marked_map,
)


THEOREM = HERE / "P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md"
TORIC = (
    REPO_ROOT / "claims" / "p4" / "classifications" / "pair-geometry"
    / "pure-rank-two" / "boundaries"
    / "P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md"
)
SEGRE = (
    REPO_ROOT / "claims" / "p4" / "classifications" / "pair-geometry"
    / "pure-rank-two" / "P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md"
)
GENERATOR = REPO_ROOT / "derive_p5_h31_toric_marked_fibre_elimination.py"


EXPECTED_PROJECTION: dict[tuple[int, str], tuple[str, ...]] = {
    (0, "finite"): ("t3", "t2", "t1"),
    (0, "infinity"): ("t2", "t1", "t3*s", "t0*t3"),
    (1, "finite"): (
        "t3",
        "t2*s",
        "t1*t2+t2*r",
        "t0*t2",
        "t0*t1+t0",
    ),
    (1, "infinity"): ("t3", "t2", "t1+1"),
    (2, "finite"): ("1",),
    (2, "infinity"): ("1",),
    (3, "finite"): (
        "t3",
        "t1*s",
        "t0*t1",
        "t1*t2*r-t1",
        "t0*t2*r-t0*r+t2*s-s",
    ),
    (3, "infinity"): ("t3", "t2", "t0", "t1*s"),
    (4, "finite"): ("t2+1", "t1", "t3*s", "t3*r", "t0*t3"),
    (4, "infinity"): ("1",),
    (5, "finite"): ("t2", "t1+r", "t0", "t3*s"),
    (5, "infinity"): ("1",),
    (6, "finite"): ("t3", "t1+r", "t0", "t2*s"),
    (6, "infinity"): ("1",),
    (7, "finite"): (
        "t3",
        "t2*s+t0+t2",
        "t1*s+t1",
        "t2*r-1",
        "t0*r+s+1",
        "t0*t1",
    ),
    (7, "infinity"): ("t3", "t2", "t0+1", "t1*s"),
    (8, "finite"): (
        "t1",
        "t3*s-t3",
        "t2*s+t0-t2",
        "t2*r-1",
        "t0*r+s-1",
        "t0*t3",
    ),
    (8, "infinity"): ("t2", "t1", "t0-1", "t3*s"),
    (9, "finite"): ("t3", "t2", "t1"),
    (9, "infinity"): ("t2", "t1", "t3*s", "t0*t3"),
    (10, "finite"): ("t3", "t1", "t2*s", "t2*r", "t0*t2"),
    (10, "infinity"): ("t3", "t2", "t1"),
    (11, "finite"): ("t3", "t2", "t1"),
    (11, "infinity"): ("t3", "t2", "t1*s", "t0*t1"),
    (12, "finite"): ("t2", "t1", "t3*s", "t3*r", "t0*t3"),
    (12, "infinity"): ("t3", "t2", "t1"),
    (13, "finite"): ("t2", "t1+r", "t0", "t3*s"),
    (13, "infinity"): ("1",),
    (14, "finite"): ("t3", "t1+r", "t0", "t2*s"),
    (14, "infinity"): ("1",),
    (15, "finite"): (
        "t3",
        "t2*s+t0",
        "t1*s",
        "t2*r-1",
        "t0*r+s",
        "t0*t1",
    ),
    (15, "infinity"): ("t3", "t2", "t0", "t1*s"),
    (16, "finite"): (
        "t1",
        "t3*s",
        "t2*s+t0",
        "t2*r-1",
        "t0*r+s",
        "t0*t3",
    ),
    (16, "infinity"): ("t2", "t1", "t0", "t3*s"),
}

EXPECTED_PROJECTION_OVERRIDES: dict[
    tuple[int, int, str],
    tuple[str, ...],
] = {
    (5, 1, "finite"): ("t2", "t1-r", "t0", "t3*s"),
    (6, 1, "finite"): ("t3", "t1-r", "t0", "t2*s"),
    (7, 2, "finite"): (
        "t3",
        "t2*s-t0+t2",
        "t1*s+t1",
        "t2*r+1",
        "t0*r+s+1",
        "t0*t1",
    ),
    (7, 3, "finite"): (
        "t3",
        "t2*s-t0+t2",
        "t1*s+t1",
        "t2*r+1",
        "t0*r+s+1",
        "t0*t1",
    ),
    (8, 2, "finite"): (
        "t1",
        "t3*s-t3",
        "t2*s-t0-t2",
        "t2*r+1",
        "t0*r+s-1",
        "t0*t3",
    ),
    (8, 3, "finite"): (
        "t1",
        "t3*s-t3",
        "t2*s-t0-t2",
        "t2*r+1",
        "t0*r+s-1",
        "t0*t3",
    ),
}


CERTIFICATES: dict[
    tuple[int, str],
    tuple[tuple[int, tuple[int, int, int, int]], ...],
] = {
    (0, "finite"): ((2, (0, 1, 4, 7)),),
    (0, "infinity"): ((1, (0, 2, 3, 7)),),
    (1, "finite"): (
        (1, (0, 1, 3, 7)),
        (3, (0, 1, 4, 7)),
        (3, (0, 1, 3, 7)),
    ),
    (1, "infinity"): ((3, (0, 1, 3, 7)),),
    (2, "finite"): (),
    (2, "infinity"): (),
    (3, "finite"): (
        (2, (0, 1, 3, 7)),
        (2, (0, 1, 5, 7)),
        (3, (0, 2, 3, 7)),
        (3, (0, 4, 5, 7)),
    ),
    (3, "infinity"): ((3, (0, 4, 5, 7)),),
    (4, "finite"): (
        (1, (0, 1, 3, 7)),
        (2, (0, 2, 3, 7)),
    ),
    (4, "infinity"): (),
    (5, "finite"): ((2, (0, 1, 4, 7)),),
    (5, "infinity"): (),
    (6, "finite"): ((3, (0, 1, 4, 7)),),
    (6, "infinity"): (),
    (7, "finite"): ((3, (0, 2, 4, 7)),),
    (7, "infinity"): ((3, (0, 2, 4, 7)),),
    (8, "finite"): ((1, (0, 1, 4, 7)),),
    (8, "infinity"): ((1, (0, 1, 4, 7)),),
    (9, "finite"): ((2, (0, 1, 3, 7)),),
    (9, "infinity"): ((1, (0, 2, 3, 7)),),
    (10, "finite"): (
        (3, (0, 1, 3, 7)),
        (1, (0, 1, 3, 7)),
    ),
    (10, "infinity"): ((3, (0, 1, 3, 7)),),
    (11, "finite"): ((3, (0, 2, 3, 7)),),
    (11, "infinity"): ((2, (0, 1, 3, 7)),),
    (12, "finite"): (
        (1, (0, 1, 3, 7)),
        (2, (0, 2, 3, 7)),
    ),
    (12, "infinity"): ((1, (0, 1, 3, 7)),),
    (13, "finite"): ((2, (0, 1, 4, 7)),),
    (13, "infinity"): (),
    (14, "finite"): ((3, (0, 1, 4, 7)),),
    (14, "infinity"): (),
    (15, "finite"): ((3, (0, 2, 4, 7)),),
    (15, "infinity"): ((3, (0, 2, 4, 7)),),
    (16, "finite"): ((1, (0, 1, 4, 7)),),
    (16, "infinity"): ((1, (0, 1, 4, 7)),),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_singular(program: str, timeout: float = 180) -> str:
    completed = subprocess.run(
        singular_command_with_timeout(timeout),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout + 5,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(
            (
                "Singular failed",
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    if completed.stderr.strip():
        raise AssertionError(("unexpected Singular stderr", completed.stderr))
    return completed.stdout


def projection_basis(output: str) -> tuple[str, ...]:
    return tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in output.splitlines()
        if line.startswith("marking[")
    )


def selected_obstruction_program(
    case,
    distinguished: int,
    chart: str,
) -> tuple[str, int]:
    case_id = case.case_id
    alpha, beta, plane_parameters = marked_rows(case, chart)
    t = sp.symbols("t0:4")
    x = sp.symbols("x0:4")
    y = sp.symbols("y0:4")
    extension = sp.Matrix(x + y)
    inverse_b = sp.Symbol("ub")
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished,
        alpha,
        beta,
    )
    equations: list[sp.Expr] = list(mixed * extension)
    equations.extend((
        (diagonal_a * extension)[0] - 1,
        inverse_b * (diagonal_b * extension)[0] - 1,
    ))
    selected_products = 0
    for mode, rows in CERTIFICATES[(case_id, chart)]:
        determinant = sp.factor(
            marked_extension(
                distinguished,
                extension,
                alpha,
                beta,
                mode,
            )[list(rows), :].det()
        )
        assert determinant != 0
        pure_column = one_marked_map(mode, alpha, beta)[:, distinguished]
        products = tuple(
            entry * determinant
            for entry in pure_column
            if entry != 0
        )
        assert products
        equations.extend(products)
        selected_products += len(products)
    equations = [equation for equation in equations if equation != 0]
    variables = x + y + (inverse_b,) + t + plane_parameters
    program = "\n".join((
        "ring R=0,(" + ",".join(map(str, variables)) + "),dp;",
        "option(redSB);",
        "ideal obstruction=" + ",".join(map(singular, equations)) + ";",
        "ideal basis=slimgb(obstruction);",
        f'"CASE={case_id}_Q={distinguished}_CHART={chart}_SELECTED";',
        '"BASIS_SIZE"; size(basis);',
        "basis;",
        "quit;",
        "",
    ))
    return program, selected_products


def check_orientation_chart(
    case_id: int,
    distinguished: int,
    chart: str,
) -> dict[str, int | bool | str]:
    cases = toric_cases()
    case = cases[case_id]
    assert distinguished in case.all_rank
    assert chart in ("finite", "infinity")
    projection_output = run_singular(
        singular_program(
            case,
            distinguished,
            chart,
            absolute=True,
        ),
        timeout=90,
    )
    actual_projection = projection_basis(projection_output)
    expected_projection = EXPECTED_PROJECTION_OVERRIDES.get(
        (case_id, distinguished, chart),
        EXPECTED_PROJECTION[(case_id, chart)],
    )
    assert actual_projection == expected_projection, (
        case_id,
        distinguished,
        chart,
        actual_projection,
        expected_projection,
    )
    obstruction_program, product_count = selected_obstruction_program(
        case,
        distinguished,
        chart,
    )
    obstruction_output = run_singular(
        obstruction_program,
        timeout=45,
    )
    assert "BASIS_SIZE\n1\nbasis[1]=1" in (
        obstruction_output.replace("\r\n", "\n")
    ), (
        case_id,
        distinguished,
        chart,
        obstruction_output,
    )
    return {
        "case_id": case_id,
        "distinguished": distinguished,
        "chart": chart,
        "selected_products": product_count,
        "binary_empty": not CERTIFICATES[(case_id, chart)],
        "verified": True,
    }


def worker_subprocess(
    job: tuple[int, int, str],
) -> dict[str, int | bool | str]:
    case_id, distinguished, chart = job
    completed = subprocess.run(
        (
            sys.executable,
            str(Path(__file__).resolve()),
            "--worker",
            str(case_id),
            str(distinguished),
            chart,
        ),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=240,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                "toric worker failure",
                job,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    result = json.loads(completed.stdout)
    assert result["verified"] is True
    return result


def main() -> None:
    if len(sys.argv) == 5 and sys.argv[1] == "--worker":
        print(json.dumps(check_orientation_chart(
            int(sys.argv[2]),
            int(sys.argv[3]),
            sys.argv[4],
        )))
        return

    started = time.monotonic()
    cases = toric_cases()
    assert len(cases) == 17
    assert sum(len(case.all_rank) for case in cases) == 39
    assert set(EXPECTED_PROJECTION) == {
        (case_id, chart)
        for case_id in range(17)
        for chart in ("finite", "infinity")
    }
    assert set(CERTIFICATES) == set(EXPECTED_PROJECTION)

    jobs = tuple(
        (case.case_id, distinguished, chart)
        for case in cases
        for distinguished in case.all_rank
        for chart in ("finite", "infinity")
    )
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = tuple(executor.map(worker_subprocess, jobs))
    projection_runs = len(results)
    selected_runs = len(results)
    selected_products = sum(
        int(result["selected_products"]) for result in results
    )
    binary_empty_runs = sum(
        bool(result["binary_empty"]) for result in results
    )

    report = {
        "verified": True,
        "field": "characteristic zero",
        "method": (
            "absolute saturated projection ideals plus selected "
            "pure-entry times marked-minor unit ideals"
        ),
        "toric_direction_types": len(cases),
        "pure_direction_orientation_types": sum(
            len(case.all_rank) for case in cases
        ),
        "base_orbit_orientation_cases": 21,
        "charts": 2,
        "projection_unit_or_ledger_runs": projection_runs,
        "selected_obstruction_unit_ideal_runs": selected_runs,
        "binary_empty_orientation_chart_runs": binary_empty_runs,
        "selected_transverse_products": selected_products,
        "all_binary_extensions_ternarily_excluded": True,
        "genuine_toric_marked_fibre_closed": True,
        "projective_interior_boundary_closed": False,
        "additional_components_closed": False,
        "global": False,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "sha256": {
            THEOREM.name: sha256(THEOREM),
            TORIC.name: sha256(TORIC),
            SEGRE.name: sha256(SEGRE),
            GENERATOR.name: sha256(GENERATOR),
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
