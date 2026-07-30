#!/usr/bin/env python3
"""Verify generic H31 exclusion on the disjoint mixed-star component."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp

from p5_high_coordinate_tree_chart_cegar import singular_command_with_timeout
from verify_p4_disjoint_mixed_star_pure_component import family, relation
from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
)


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
)
COMPONENT = ROOT / "P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md"
COMPONENT_PRIMARY = ROOT / "verify_p4_disjoint_mixed_star_pure_component.py"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
MARKED_ROWS = (0, 1, 3, 7)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows) -> sp.Expr:
    return sp.factor(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def shifted_basis(alpha, beta, shifts):
    return tuple(
        tuple(
            sp.expand(
                beta[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def projection_linear(distinguished, a, b, f, phi, t0):
    common = (a**2 * b * f**2 + 2 * b**2 * f + b) * phi
    if distinguished == 2:
        constant = (
            3 * a**2 * f**2
            - 2 * b**2 * f**2
            - 2 * b * f
            - 3
        )
    elif distinguished == 3:
        constant = (
            -a**2 * f**2
            + 2 * b**2 * f**2
            + 2 * b * f
            + 1
        )
    else:
        raise ValueError(distinguished)
    return sp.expand(common + (1 - a**2 * f**2) * t0 + constant)


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def run_projection(distinguished: int, alpha, beta) -> dict[str, object]:
    a, b, f, phi = sp.symbols("a b f phi")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    shifts = sp.symbols("t0:4")
    inverse = sp.Symbol("w")
    marked_beta = shifted_basis(alpha, beta, shifts)
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished, alpha, marked_beta
    )
    extension = sp.Matrix(extensions)
    equations = (
        relation(a, b, f, phi),
        *tuple(mixed * extension),
        (diagonal_a * extension)[0] - 1,
        inverse * (diagonal_b * extension)[0] - 1,
    )
    eliminated = extensions + (inverse,)
    variables = eliminated + (phi,) + shifts
    lines = [
        "ring R=(0,a,b,f),("
        + ",".join(map(str, variables))
        + "),(dp(9),dp(5));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=eliminate(I," + "*".join(map(str, eliminated)) + ");",
        "J=std(J);",
    ]
    if distinguished in (0, 1):
        lines.extend(
            (
                "int unit=(reduce(1,J)==0);",
                '"CODEX_RESULT:"+string(unit);',
            )
        )
    else:
        expected = (
            relation(a, b, f, phi),
            shifts[1],
            shifts[2],
            shifts[3],
            projection_linear(
                distinguished, a, b, f, phi, shifts[0]
            ),
        )
        lines.extend(
            (
                "ideal E=" + ",".join(map(singular, expected)) + ";",
                "E=std(E);",
                "ideal JE=reduce(J,E);",
                "ideal EJ=reduce(E,J);",
                "JE=simplify(JE,2);",
                "EJ=simplify(EJ,2);",
                "int same=((size(JE)==0)&&(size(EJ)==0));",
                "int retained_dimension=dim(J)-9;",
                (
                    '"CODEX_RESULT:"+string(same)+":"'
                    '+string(retained_dimension)+":"+string(size(J));'
                ),
            )
        )
    lines.append("quit;")
    timeout = 300
    completed = subprocess.run(
        singular_command_with_timeout(timeout),
        input="\n".join(lines),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout + 5,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                "Singular projection failure",
                distinguished,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    results = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(results) == 1, completed.stdout
    if distinguished in (0, 1):
        assert results[0] == "CODEX_RESULT:1", completed.stdout
        return {
            "projected_ideal_unit": True,
            "genuine_markings": 0,
        }
    fields = results[0].split(":")
    assert fields[1] == "1", completed.stdout
    return {
        "projected_ideal": [
            "Phi",
            "t1",
            "t2",
            "t3",
            f"L{distinguished}",
        ],
        "bidirectional_ideal_equality": True,
        "retained_projection_dimension_over_C(a,b,f)": int(fields[2]),
        "computed_Groebner_basis_size": int(fields[3]),
        "genuine_markings_over_component_function_field": 1,
    }


def extension_identity(
    distinguished: int, alpha, beta
) -> dict[str, object]:
    a, b, f, phi, t0 = sp.symbols("a b f phi t0")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    extension = sp.Matrix(extensions)
    marking = (t0, 0, 0, 0)
    marked_beta = shifted_basis(alpha, beta, marking)
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished, alpha, marked_beta
    )
    first = (diagonal_a * extension)[0]
    second = (diagonal_b * extension)[0]
    marked = marked_extension(
        distinguished, extension, alpha, marked_beta, 0
    )
    determinant_matrix = marked[list(MARKED_ROWS), :]
    component_relation = relation(a, b, f, phi)
    marking_relation = projection_linear(
        distinguished, a, b, f, phi, t0
    )
    ratio = (
        f * (b * f + 1) * (1 - a**2 * f**2) / (a**2 * f + b)
    )
    if distinguished == 3:
        ratio = -ratio
    ideal_generators = (
        component_relation,
        marking_relation,
        *tuple(mixed * extension),
    )
    program = "\n".join(
        (
            "ring R=(0,a,b,f),(phi,t0,"
            + ",".join(map(str, extensions))
            + "),dp;",
            "option(redSB);",
            "ideal I="
            + ",".join(map(singular, ideal_generators))
            + ";",
            "I=slimgb(I);",
            "matrix N[4][4]="
            + ",".join(
                singular(determinant_matrix[row, column])
                for row in range(4)
                for column in range(4)
            )
            + ";",
            "poly determinant=det(N);",
            "poly rd=reduce(determinant,I);",
            f"poly rb=reduce({singular(first * second**2)},I);",
            "number observed=leadcoef(rd)/leadcoef(rb);",
            "poly check=reduce(rd-observed*rb,I);",
            f"number expected={singular(ratio)};",
            "int good=((check==0)&&(observed-expected==0));",
            "poly ra=reduce(" + singular(first) + ",I);",
            "poly rbdiag=reduce(" + singular(second) + ",I);",
            "int diagonals=((ra!=0)&&(rbdiag!=0));",
            (
                '"CODEX_RESULT:"+string(dim(I))+":"'
                '+string(good)+":"+string(diagonals)+":"'
                '+string(observed);'
            ),
            "quit;",
        )
    )
    timeout = 300
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
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                "Singular all-extension identity failure",
                distinguished,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    results = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(results) == 1, completed.stdout
    fields = results[0].split(":", 4)
    assert fields[1:4] == ["2", "1", "1"], completed.stdout
    return {
        "mixed_kernel_dimension": 2,
        "marked_mode": 0,
        "minor_rows": list(MARKED_ROWS),
        "factor_identity_ratio": fields[4],
        "diagonal_forms_nonzero_on_kernel": True,
    }


def main() -> None:
    a, b, f, phi = sp.symbols("a b f phi")
    planes = family(a, b, f, phi)
    alpha = tuple(tuple(plane.row(0)) for plane in planes)
    beta = tuple(tuple(plane.row(1)) for plane in planes)
    component_relation = relation(a, b, f, phi)
    tensor = {
        word: permanent(
            tuple(
                beta[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    assert all(
        sp.factor(
            value
            - {
                (1, 0, 0, 1): -4 * component_relation,
                (1, 1, 1, 1): 4,
            }.get(word, 0)
        )
        == 0
        for word, value in tensor.items()
    )
    assert sp.Poly(component_relation, a, b, f, phi).is_irreducible

    t = sp.symbols("t0:4")
    marked_beta = shifted_basis(alpha, beta, t)
    assert all(
        sp.factor(
            alpha[mode][left] * marked_beta[mode][right]
            - alpha[mode][right] * marked_beta[mode][left]
            - (
                alpha[mode][left] * beta[mode][right]
                - alpha[mode][right] * beta[mode][left]
            )
        )
        == 0
        for mode in range(4)
        for left, right in itertools.combinations(range(4), 2)
    )

    projections = {
        str(distinguished): run_projection(
            distinguished, alpha, beta
        )
        for distinguished in range(4)
    }
    certificates = {
        str(distinguished): extension_identity(
            distinguished, alpha, beta
        )
        for distinguished in (2, 3)
    }

    factor = sp.factor(
        f * (b * f + 1) * (1 - a**2 * f**2) / (a**2 * f + b)
    )
    output = {
        "verified": True,
        "field": "C(a,b,f)[phi]/(Phi)",
        "method": (
            "function-field saturated marked projection and "
            "all-extension determinantal Fitting identities"
        ),
        "component_relation": str(component_relation),
        "component_relation_irreducible": True,
        "projections": projections,
        "surviving_marking_sheets": 2,
        "surviving_distinguished_coordinates": [2, 3],
        "common_obstruction_factor": str(factor),
        "certificates": certificates,
        "generic_marked_fibre_excluded": True,
        "complete_boundary_marked_fibre_excluded": False,
        "known_pure_component_orbits_at_least": 8,
        "all_eight_known_components_generic_marked_fibres_excluded": True,
        "all_pure_components_classified": False,
        "H31_excluded": False,
        "weighted_H22_excluded_on_component": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            COMPONENT_PRIMARY.name: sha256(COMPONENT_PRIMARY),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_h31_disjoint_mixed_star_component_generic_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
