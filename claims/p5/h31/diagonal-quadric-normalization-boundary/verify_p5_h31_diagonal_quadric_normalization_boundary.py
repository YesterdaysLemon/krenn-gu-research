#!/usr/bin/env python3
"""Verify the complete elliptic-normalization boundary obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path
from typing import Callable

import sympy as sp

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/diagonal-quadric-curve-marked-fibre")

from krenn_gu.singular_runtime import (
    singular_command_with_timeout,
)
from verify_p5_h31_diagonal_quadric_curve_marked_fibre import singular
from krenn_gu.p5_marked_basis import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
    permanent,
)


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H31_DIAGONAL_QUADRIC_NORMALIZATION_BOUNDARY_OBSTRUCTION.md"
)
REGULAR = (
    REPO_ROOT / 'claims/p5/h31/elliptic-middle-coordinate-pivot-complement/P5_H31_ELLIPTIC_MIDDLE_COORDINATE_PIVOT_COMPLEMENT.md'
)
FACTORED = (
    REPO_ROOT / 'claims/p5/h31/diagonal-quadric-pure-direction-curve-marked-fibre/P5_H31_DIAGONAL_QUADRIC_PURE_DIRECTION_CURVE_MARKED_FIBRE_OBSTRUCTION.md'
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
EXPECTED_FINITE = {
    -1: {
        0: ("1",),
        1: ("1",),
        2: ("1",),
        3: (
            "t3",
            "t1+h",
            "t0+2*t2-h",
            "2*t2*h-h^2-1",
        ),
    },
    1: {
        0: (
            "t3",
            "t1-h",
            "t0+2*t2-h",
            "2*t2*h-h^2-1",
        ),
        1: ("1",),
        2: ("1",),
        3: ("1",),
    },
}
EXPECTED_INFINITY = {
    -1: {
        0: ("1",),
        1: ("1",),
        2: ("1",),
        3: ("t3", "t1+1", "t0+1", "z^2-2*t2+1"),
    },
    1: {
        0: ("t3", "t1-1", "t0+1", "z^2-2*t2+1"),
        1: ("1",),
        2: ("1",),
        3: ("1",),
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def direct_system_builder(distinguished, alpha, beta):
    return mixed_matrix(distinguished, alpha, beta)


def run_relative_projection(
    distinguished: int,
    alpha,
    beta,
    parameter: sp.Symbol,
    pure_factor: sp.Expr,
    system_builder: Callable,
    timeout: float = 180,
) -> tuple[str, ...]:
    extensions = sp.symbols("a0:4") + sp.symbols("b0:4")
    shifts = sp.symbols("t0:4")
    diagonal_inverse, pure_inverse = sp.symbols("ub uc")
    mixed, diagonal_a, diagonal_b = system_builder(
        distinguished,
        alpha,
        beta,
    )
    extension = sp.Matrix(extensions)
    equations = list(mixed * extension)
    equations.extend((
        (diagonal_a * extension)[0] - 1,
        diagonal_inverse * (diagonal_b * extension)[0] - 1,
        pure_inverse * pure_factor - 1,
    ))
    eliminated = extensions + (diagonal_inverse, pure_inverse)
    retained = shifts + (parameter,)
    variables = eliminated + retained
    program = "\n".join((
        "ring r=0,("
        + ",".join(map(str, variables))
        + f"),(dp({len(eliminated)}),dp({len(retained)}));",
        "option(redSB);",
        "ideal incidence=" + ",".join(map(singular, equations)) + ";",
        "ideal basis=std(incidence);",
        "ideal marking=eliminate(basis,"
        + "*".join(map(str, eliminated))
        + ");",
        "marking=std(marking);",
        '"MARKING";',
        "marking;",
        "quit;",
    ))
    completed = subprocess.run(
        singular_command_with_timeout(timeout),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout + 10,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError((
            "relative boundary projection failed",
            distinguished,
            parameter,
            completed.returncode,
            completed.stdout,
            completed.stderr,
        ))
    return tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in completed.stdout.replace("\r\n", "\n").splitlines()
        if line.startswith("marking[")
    )


def pluecker(left, right):
    return tuple(
        sp.factor(left[i] * right[j] - left[j] * right[i])
        for i in range(4)
        for j in range(i + 1, 4)
    )


def proportional(left, right) -> bool:
    return all(
        sp.factor(left[i] * right[j] - left[j] * right[i]) == 0
        for i in range(len(left))
        for j in range(len(left))
    )


def verify_boundary(
    system_builder: Callable = direct_system_builder,
) -> dict:
    C, E, H = sp.symbols("C E H")
    U = C + H
    S = 1 + C * H
    T = H + C * E**2
    psi = 1 + C * H - H**2 - C**2 * E**2 + C**2 * H**2 - C * E**2 * H
    assert sp.factor(psi - (S**2 - U * T)) == 0
    r = S / U
    x = sp.factor(1 - r * H)
    D = sp.factor(x + r**2 - 1)
    assert sp.factor(x - C * (1 - H**2) / U) == 0
    assert sp.factor(D - S * (1 - H**2) / U**2) == 0
    for delta in (-1, 1):
        boundary = {C: -1 / H, E: delta * H}
        assert sp.factor(S.subs(boundary)) == 0
        assert sp.factor(T.subs(boundary)) == 0
        assert sp.factor(U.subs(boundary) - (H**2 - 1) / H) == 0

    h, z = sp.symbols("h z")
    t = sp.symbols("t0:4")
    u, v = sp.symbols("u v")
    y1 = (1, 0, 0, -1)
    y2 = (0, 1, -1, 0)
    k0 = (1, 0, 0, 1)
    k1 = (0, 1, 1, 0)
    u1 = (1, -1, 1, 1)
    outputs = {}

    for delta in (-1, 1):
        finite_alpha = (
            (delta * h, -1, -1, -delta * h),
            y1,
            y2,
            k1,
        )
        finite_canonical = (
            u1,
            (h, h - 1, -h - 1, h),
            ((1 + delta) * h, 1, 1, (1 - delta) * h),
            k0,
        )
        finite_pure = {
            word: sp.factor(permanent(tuple(
                finite_canonical[mode]
                if word[mode]
                else finite_alpha[mode]
                for mode in range(4)
            )))
            for word in WORDS
        }
        assert sp.factor(
            finite_pure[(1, 1, 1, 1)]
            - 4 * (h - 1) * (h + 1)
        ) == 0
        assert all(
            value == 0
            for word, value in finite_pure.items()
            if word != (1, 1, 1, 1)
        )
        finite_beta = tuple(
            tuple(
                finite_canonical[mode][coordinate]
                + t[mode] * finite_alpha[mode][coordinate]
                for coordinate in range(4)
            )
            for mode in range(4)
        )

        infinity_alpha = (
            (delta, -z, -z, -delta),
            y1,
            y2,
            k1,
        )
        infinity_canonical = (
            u1,
            (1, 1 - z, -1 - z, 1),
            (1 + delta, z, z, 1 - delta),
            k0,
        )
        infinity_pure = {
            word: sp.factor(permanent(tuple(
                infinity_canonical[mode]
                if word[mode]
                else infinity_alpha[mode]
                for mode in range(4)
            )))
            for word in WORDS
        }
        assert sp.factor(
            infinity_pure[(1, 1, 1, 1)]
            + 4 * (z - 1) * (z + 1)
        ) == 0
        assert all(
            value == 0
            for word, value in infinity_pure.items()
            if word != (1, 1, 1, 1)
        )
        infinity_beta = tuple(
            tuple(
                infinity_canonical[mode][coordinate]
                + t[mode] * infinity_alpha[mode][coordinate]
                for coordinate in range(4)
            )
            for mode in range(4)
        )

        for mode in range(4):
            assert proportional(
                pluecker(
                    finite_alpha[mode],
                    finite_canonical[mode],
                ),
                tuple(
                    entry.subs(z, 1 / h)
                    for entry in pluecker(
                        infinity_alpha[mode],
                        infinity_canonical[mode],
                    )
                ),
            )

        finite_projections = {
            distinguished: run_relative_projection(
                distinguished,
                finite_alpha,
                finite_beta,
                h,
                h**2 - 1,
                system_builder,
            )
            for distinguished in range(4)
        }
        infinity_projections = {
            distinguished: run_relative_projection(
                distinguished,
                infinity_alpha,
                infinity_beta,
                z,
                1 - z**2,
                system_builder,
            )
            for distinguished in range(4)
        }
        assert finite_projections == EXPECTED_FINITE[delta]
        assert infinity_projections == EXPECTED_INFINITY[delta]

        distinguished = 3 if delta == -1 else 0
        candidate = (-1, delta, (z**2 + 1) / 2, 0)
        marked_beta = tuple(
            tuple(
                sp.factor(
                    infinity_canonical[mode][coordinate]
                    + candidate[mode] * infinity_alpha[mode][coordinate]
                )
                for coordinate in range(4)
            )
            for mode in range(4)
        )
        mixed, diagonal_a, diagonal_b = system_builder(
            distinguished,
            infinity_alpha,
            marked_beta,
        )
        kernel = (
            sp.Matrix((
                sp.Rational(1, 2),
                0,
                1 / (2 * z**2),
                -1 / (2 * z),
                -(z**2 - 1) / (4 * z**2),
                (z**2 - 1) / (4 * z**2),
                1,
                0,
            )),
            sp.Matrix((
                0,
                delta,
                -1 / z**2,
                1 / z,
                (z**2 - 1) / (2 * z**2),
                (3 * z**2 + 1) / (2 * z**2),
                0,
                1,
            )),
        )
        assert all(
            all(sp.factor(entry) == 0 for entry in mixed * vector)
            for vector in kernel
        )
        rank_minor = sp.factor(
            mixed.extract(
                (1, 2, 3, 4, 5, 9),
                (0, 1, 2, 3, 4, 5),
            ).det(method="domain-ge")
        )
        assert rank_minor == 128 * z**7
        extension = u * kernel[0] + v * kernel[1]
        J = u * z**2 - u + 6 * v * z**2 + 2 * v
        assert sp.factor(
            (diagonal_a * extension)[0]
            - delta * (u - 2 * v) / z
        ) == 0
        assert sp.factor(
            (diagonal_b * extension)[0]
            + (z**2 - 1) * J / (2 * z**2)
        ) == 0
        marked = marked_extension(
            distinguished,
            extension,
            infinity_alpha,
            marked_beta,
            1,
        )
        marked_minor = sp.factor(
            marked.extract((0, 1, 2, 7), range(4)).det(
                method="domain-ge"
            )
        )
        expected_minor = (
            (u - 2 * v) ** 2 * (z**2 - 1) * J / (2 * z**3)
        )
        assert sp.factor(marked_minor - expected_minor) == 0
        pure_column = one_marked_map(
            1,
            infinity_alpha,
            marked_beta,
        )[:, distinguished]
        assert any(entry != 0 for entry in pure_column)

        zero_substitution = {z: 0}
        zero_alpha = tuple(
            tuple(
                sp.factor(sp.sympify(entry).subs(zero_substitution))
                for entry in row
            )
            for row in infinity_alpha
        )
        zero_beta = tuple(
            tuple(
                sp.factor(sp.sympify(entry).subs(zero_substitution))
                for entry in row
            )
            for row in marked_beta
        )
        zero_mixed, zero_a, _zero_b = system_builder(
            distinguished,
            zero_alpha,
            zero_beta,
        )
        assert zero_mixed.rank() == 4
        zero_kernel = zero_mixed.nullspace()
        assert len(zero_kernel) == 4
        assert all((zero_a * vector)[0] == 0 for vector in zero_kernel)

        outputs[str(delta)] = {
            "finite_projections": {
                str(key): list(value)
                for key, value in finite_projections.items()
            },
            "infinity_projections": {
                str(key): list(value)
                for key, value in infinity_projections.items()
            },
            "survivor_orientation": distinguished,
            "uniform_marked_minor": str(expected_minor),
            "infinity_point_binary_survivor": False,
        }

    return {
        "boundary_identity_verified": True,
        "residual_components": ["E=H", "E=-H"],
        "projective_charts_complete": True,
        "cases": outputs,
        "binary_survivors_ternarily_obstructed": True,
        "whole_normalized_affine_slice_marked_fibre_closed": True,
    }


def main() -> None:
    result = verify_boundary()
    output = {
        "verified": True,
        "field": "C",
        **result,
        "dependencies": {
            REGULAR.name: sha256(REGULAR),
            FACTORED.name: sha256(FACTORED),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / 'tmp/p5_h31_diagonal_quadric_normalization_boundary_verified.json'
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
