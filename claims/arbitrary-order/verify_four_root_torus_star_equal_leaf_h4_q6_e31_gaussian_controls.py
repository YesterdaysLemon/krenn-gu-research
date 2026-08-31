"""Direct exact E31 Gaussian-control reconstruction from tracked sources.

Exploratory only: this reconstructs selected actual seven-minors from the
committed GLD71 sparse syndrome and GLD88 H4 chart.  It intentionally does
not parse or import the generated all-pairs Singular source.  It does import
the hash-pinned GLD101 Python verifier for selector, Q6, and Delta provenance,
so this checker is not a no-import audit.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import platform
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "claims" / "arbitrary-order"
GLD71 = BASE / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
GLD88 = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
)
GLD101 = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_a0_six_selector_norm_cover.py"
)

EXPECTED_SOURCE_PINS = {
    "GLD71": {
        "path": GLD71,
        "raw_sha256": (
            "3342809b22cc1e5ffe960e14068f81303a3bc0b597e21e2d29c05c10c605dc7d",
            "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e",
        ),
        "lf_sha256": "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e",
    },
    "GLD88": {
        "path": GLD88,
        "raw_sha256": (
            "70c46728c397d7a18fd999c27ca3d10232f9e3169ad508be7071c109be322752",
            "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199",
        ),
        "lf_sha256": "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199",
    },
    "GLD101": {
        "path": GLD101,
        "raw_sha256": (
            "81fdddb281de33babe4d3aced6842a725e58f3db056d07072c3261f2bcedb788",
            "1cd7768ae3660dc97babddecd018c0a2cf4653fec8c7bb7f70b473cdb16c4a44",
            "c36d618651b92621627961d3004128f39cb43e522a76256c74b1141baf9d1a3c",
        ),
        "lf_sha256": "c36d618651b92621627961d3004128f39cb43e522a76256c74b1141baf9d1a3c",
    },
}
EXPECTED_SUPPORT_DIGEST = (
    "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
)

SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)
RSTAR = (0, 1, 17, 28, 31, 32, 33)
NAMED = {
    "T0": ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8)),
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "Y1": (RSTAR, (0, 1, 3, 4, 5, 6, 7)),
    "X3": (RSTAR, (0, 1, 2, 3, 4, 6, 7)),
}

p, q, a, B, C = sp.symbols("p q a B C")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_pinned_import_top_level_shape(path: Path) -> None:
    """Allow only the expected broad top-level statement shapes in a pinned source.

    This is a secondary drift check, not a proof that assignment right-hand
    sides are inert.  Exact raw and LF hash pins are the import safety boundary.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    inert = (
        ast.Import,
        ast.ImportFrom,
        ast.Assign,
        ast.AnnAssign,
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.ClassDef,
    )
    for node in tree.body:
        if isinstance(node, inert):
            continue
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            continue
        if (
            isinstance(node, ast.If)
            and isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name)
            and node.test.left.id == "__name__"
            and len(node.test.ops) == 1
            and isinstance(node.test.ops[0], ast.Eq)
            and len(node.test.comparators) == 1
            and isinstance(node.test.comparators[0], ast.Constant)
            and node.test.comparators[0].value == "__main__"
        ):
            continue
        raise AssertionError(("unsafe top-level import statement", path, ast.dump(node)))


def source_hashes(path: Path) -> dict[str, str]:
    raw = path.read_bytes()
    return {
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "lf_sha256": hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest(),
    }


def serial(value: sp.Expr) -> list[str]:
    expanded = sp.expand_complex(sp.cancel(value))
    real, imag = expanded.as_real_imag()
    return [str(sp.cancel(real)), str(sp.cancel(imag))]


def q6_polynomial() -> sp.Expr:
    return (
        2 * p**4 * q**2 - 2 * p**4 * q + p**4
        + 2 * p**3 * q**3 - 7 * p**3 * q**2 + 5 * p**3 * q - 2 * p**3
        + 2 * p**2 * q**4 - 7 * p**2 * q**3 + 12 * p**2 * q**2
        - 7 * p**2 * q + 2 * p**2 - 2 * p * q**4 + 5 * p * q**3
        - 7 * p * q**2 + 2 * p * q + q**4 - 2 * q**3 + 2 * q**2
    )


def delta_polynomial() -> sp.Expr:
    d0 = p + q - 1
    return (
        (p - q)
        * d0
        * (p**2 - p + 1)
        * (p**2 + 2 * p * q - 2 * p - q)
        * (2 * p * q - p + q**2 - 2 * q)
        * (2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2)
    )


def evaluate_case(gld71, gld88, case_name: str) -> dict[str, object]:
    i = sp.I
    cases = {
        "p0": {p: sp.Integer(0), a: sp.Integer(0), q: 1 + i, B: (-3 - i) / 4},
        "p1": {p: sp.Integer(1), a: sp.Integer(1), q: i, B: (-1 - i) / 4},
    }
    point = cases[case_name]
    family = gld88.h4_family(p, q, a)
    family_values = {
        key: sp.cancel(value.subs(point)) for key, value in family.items()
    }
    expected_family = {
        "p0": {
            "s": 1 - i,
            "b": (-1 + i) / 4,
            "c": (-1 - i) / 4,
            "u": -1 + i,
            "v": -i,
            "h4_denominator": i,
            "rank_denominator": -4 * i,
            "b_denominator_factor": 1,
            "kernel_denominator": -1 + i,
        },
        "p1": {
            "s": -i,
            "b": (-3 + i) / 4,
            "c": (-3 - i) / 4,
            "u": -1 - i,
            "v": i,
            "h4_denominator": i,
            "rank_denominator": -4 * i,
            "b_denominator_factor": 1,
            "kernel_denominator": -1 - i,
        },
    }[case_name]
    for key, wanted in expected_family.items():
        if sp.cancel(family_values[key] - wanted) != 0:
            raise AssertionError(("unexpected H4 value", case_name, key, family_values[key], wanted))
    for key in (
        "h4_denominator",
        "rank_denominator",
        "b_denominator_factor",
        "kernel_denominator",
    ):
        if family_values[key] == 0:
            raise AssertionError(("vanishing H4 denominator", case_name, key))

    leaf = [
        [sp.Integer(1), sp.Integer(1), sp.Integer(1)],
        [point[p], point[q], family_values["s"]],
        [
            point[a],
            1 + family_values["b"] + point[B],
            1 + family_values["c"] + C,
        ],
    ]
    rows: dict[int, list[sp.Expr]] = {}
    for relation_row in SUPPORT_ROWS:
        entries = []
        for root in range(3):
            for component in range(3):
                total = sp.Integer(0)
                for indices, coefficient in gld71.SPARSE_RELATIONS[relation_row]:
                    if indices[0] != root:
                        continue
                    total += (
                        coefficient
                        * leaf[indices[1]][component]
                        * leaf[indices[2]][component]
                        * leaf[indices[3]][component]
                    )
                entries.append(sp.cancel(total))
        rows[relation_row] = entries

    minors = {}
    for name, (rowset, columns) in NAMED.items():
        matrix = sp.Matrix([[rows[row][column] for column in columns] for row in rowset])
        determinant = sp.cancel(matrix.det(method="domain-ge"))
        minors[name] = {
            "determinant": determinant,
            "at_C0": sp.cancel(determinant.subs(C, 0)),
            "dC_at_C0": sp.cancel(sp.diff(determinant, C).subs(C, 0)),
            "degree_C": str(sp.Poly(determinant, C, extension=sp.I).degree()),
        }

    substitution = {p: point[p], q: point[q], a: point[a]}
    q6 = sp.cancel(q6_polynomial().subs(substitution))
    h2 = sp.cancel((2 * p**2 - 2 * p + 1).subs(substitution))
    delta = sp.cancel(delta_polynomial().subs(substitution))
    localizer = sp.cancel(point[B] * h2 * delta)
    expected = {
        "p0": {
            "localizer": -4 + 12 * i,
            "Y1_at_C0": 2304 - 6912 * i,
            "Y1_dC_at_C0": 9216,
            "X3_at_C0": 6912 - 3456 * i,
            "X3_dC_at_C0": -6912 - 6912 * i,
            "generated_G_Y1": 36864,
            "generated_G_X3": -27648 - 27648 * i,
        },
        "p1": {
            "localizer": -4 + 4 * i,
            "Y1_at_C0": -216 - 792 * i,
            "Y1_dC_at_C0": 2304 + 288 * i,
            "X3_at_C0": -216 - 72 * i,
            "X3_dC_at_C0": 2016 + 576 * i,
            "generated_G_Y1": 9216 + 1152 * i,
            "generated_G_X3": 8064 + 2304 * i,
        },
    }[case_name]
    if q6 != 0 or h2 != 1 or sp.cancel(delta + 16 * i) != 0:
        raise AssertionError(("base/control value drift", case_name, q6, h2, delta))
    if sp.cancel(localizer - expected["localizer"]) != 0:
        raise AssertionError(("unexpected localizer", case_name, localizer))
    for name in ("T0", "T1", "T2"):
        if minors[name]["determinant"] != 0 or minors[name]["degree_C"] != "-oo":
            raise AssertionError(("minor not identically zero in C", case_name, name))
    for name in ("Y1", "X3"):
        for field in ("at_C0", "dC_at_C0"):
            wanted = expected[f"{name}_{field}"]
            if sp.cancel(minors[name][field] - wanted) != 0:
                raise AssertionError((case_name, name, field, minors[name][field], wanted))
        if minors[name]["degree_C"] != "1":
            raise AssertionError(("minor not affine in C", case_name, name))
        if sp.cancel(4 * minors[name]["dC_at_C0"] - expected[f"generated_G_{name}"]) != 0:
            raise AssertionError(("generated normalization mismatch", case_name, name))

    return {
        "point": {str(key): serial(value) for key, value in point.items()},
        "family": {key: serial(value) for key, value in family_values.items()},
        "q6": serial(q6),
        "h2": serial(h2),
        "delta": serial(delta),
        "localizer": serial(localizer),
        "generated_normalization_factor": "4",
        "minors": {
            name: {
                "at_C0": serial(record["at_C0"]),
                "dC_at_C0": serial(record["dC_at_C0"]),
                "degree_C": record["degree_C"],
            }
            for name, record in minors.items()
        },
    }


def main() -> None:
    pins = {
        name: source_hashes(record["path"])
        for name, record in EXPECTED_SOURCE_PINS.items()
    }
    for name, actual in pins.items():
        expected = EXPECTED_SOURCE_PINS[name]
        if (
            actual["raw_sha256"] not in expected["raw_sha256"]
            or actual["lf_sha256"] != expected["lf_sha256"]
        ):
            raise AssertionError(("tracked source drift", name, actual, expected))
    for record in EXPECTED_SOURCE_PINS.values():
        assert_pinned_import_top_level_shape(record["path"])

    gld71 = load_module(GLD71, "gld71_for_e31_gaussian_control")
    gld88 = load_module(GLD88, "gld88_for_e31_gaussian_control")
    gld101 = load_module(GLD101, "gld101_for_e31_gaussian_control")
    tracked_selectors = {
        name: (
            gld101.NAMED[name]
            if name in gld101.NAMED
            else (gld101.RSTAR, gld101.EXTRA[name])
        )
        for name in NAMED
    }
    if tracked_selectors != NAMED:
        raise AssertionError(("GLD101 selector drift", tracked_selectors, NAMED))
    tracked_q6 = gld101.q6_expression().subs({gld101.p: p, gld101.q: q})
    tracked_chart = gld88.h4_family(gld101.p, gld101.q, a)
    tracked_delta = gld101.delta_expression(tracked_chart).subs(
        {gld101.p: p, gld101.q: q}
    )
    if sp.expand(q6_polynomial() - tracked_q6) != 0:
        raise AssertionError("local Q6 copy differs from pinned GLD101")
    if sp.expand(delta_polynomial() - tracked_delta) != 0:
        raise AssertionError("local Delta copy differs from pinned GLD101/GLD88")
    support_payload = [
        [
            row,
            [[list(indices), coefficient] for indices, coefficient in gld71.SPARSE_RELATIONS[row]],
        ]
        for row in SUPPORT_ROWS
    ]
    support_digest = hashlib.sha256(
        json.dumps(support_payload, separators=(",", ":")).encode()
    ).hexdigest()
    if support_digest != EXPECTED_SUPPORT_DIGEST:
        raise AssertionError(("support drift", support_digest))

    case_names = ("p0", "p1")
    case_results = {
        case_name: evaluate_case(gld71, gld88, case_name)
        for case_name in case_names
    }
    checker_hashes = source_hashes(Path(__file__))
    payload = {
        "schema_version": 1,
        "status": "succeeded",
        "claim_status": "exploratory",
        "evidence_mode": "exact characteristic-zero direct reconstruction",
        "scope": "two Gaussian controls for the E31 four-row candidate cover",
        "global_status": "UNRESOLVED",
        "case_set_complete": True,
        "pinned_import_top_level_shape_checked": True,
        "checker_sha256": checker_hashes,
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
        },
        "tracked_source_sha256": pins,
        "support_digest": support_digest,
        "selector_contract": {
            name: [list(rowset), list(columns)]
            for name, (rowset, columns) in tracked_selectors.items()
        },
        "cases": case_results,
    }
    canonical_payload = {
        "schema_version": payload["schema_version"],
        "claim_status": payload["claim_status"],
        "evidence_mode": payload["evidence_mode"],
        "scope": payload["scope"],
        "global_status": payload["global_status"],
        "case_set_complete": payload["case_set_complete"],
        "pinned_import_top_level_shape_checked": payload[
            "pinned_import_top_level_shape_checked"
        ],
        "checker_lf_sha256": checker_hashes["lf_sha256"],
        "tracked_source_lf_sha256": {
            name: record["lf_sha256"] for name, record in pins.items()
        },
        "support_digest": support_digest,
        "selector_contract": payload["selector_contract"],
        "cases": case_results,
    }
    result = {
        **payload,
        "run_payload_sha256": hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "canonical_payload_sha256": hashlib.sha256(
            json.dumps(
                canonical_payload,
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        ).hexdigest(),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
