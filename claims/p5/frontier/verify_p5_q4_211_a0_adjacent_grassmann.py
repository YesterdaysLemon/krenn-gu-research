#!/usr/bin/env python3
"""Verify the Grassmannian obstruction on the a=0 adjacent boundary."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_A0_ADJACENT_GRASSMANN_OBSTRUCTION.md"
PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pair_contraction(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    """Coordinates of P4(left,right,-,-) on the six squarefree pairs."""
    coordinates = []
    for first, second in PAIRS:
        complement = [
            index
            for index in range(4)
            if index not in (first, second)
        ]
        coordinates.append(
            sp.expand(
                left[complement[0]] * right[complement[1]]
                + left[complement[1]] * right[complement[0]]
            )
        )
    return sp.Matrix(coordinates)


def permanent4(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    matrix = sp.Matrix.vstack(*(row.T for row in rows))
    return sp.expand(
        sum(
            sp.prod(matrix[index, permutation[index]] for index in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def all_minors(
    matrix: sp.Matrix,
    size: int,
) -> list[sp.Expr]:
    minors = []
    for rows in itertools.combinations(range(matrix.rows), size):
        for columns in itertools.combinations(range(matrix.cols), size):
            minor = sp.expand(matrix.extract(rows, columns).det())
            if minor != 0:
                minors.append(minor)
    return minors


def same_plane(
    first: tuple[sp.Matrix, sp.Matrix],
    second: tuple[sp.Matrix, sp.Matrix],
) -> bool:
    first_matrix = sp.Matrix.hstack(*first)
    second_matrix = sp.Matrix.hstack(*second)
    return (
        first_matrix.rank() == 2
        and second_matrix.rank() == 2
        and sp.Matrix.hstack(first_matrix, second_matrix).rank() == 2
    )


def main() -> None:
    rho, sigma = sp.symbols("rho sigma")

    # Normalized dual coordinates are (E,S,P,Q).  The six coordinates
    # below are ordered as 01,02,03,12,13,23.
    h = sp.Matrix([1, 0, 0, -1])
    u = sp.Matrix([1, 0, 1, 0])
    n = sp.Matrix([0, 0, 1, 1])
    m = sp.Matrix([0, 0, 1, -1])
    u_plus = sp.Matrix([1, 0, 0, 1])
    h_one = sp.Matrix([1, 0, -1, 0])

    planes = {
        "Ph": (h, m),
        "P": (h, u),
        "Pu": (u, m),
        "P0": (n, u_plus),
    }
    assert same_plane(planes["P"], (u, n))
    assert same_plane(planes["Pu"], (u_plus, m))
    assert same_plane(planes["Ph"], (h_one, m))
    assert same_plane(planes["P0"], (h_one, n))

    # The complement-pairing matrix is nondegenerate and realizes the
    # four-linear permanent from the two pair contractions.
    complement_pairing = sp.zeros(6, 6)
    for index, pair in enumerate(PAIRS):
        complement = tuple(entry for entry in range(4) if entry not in pair)
        complement_pairing[index, PAIRS.index(complement)] = 1
    assert complement_pairing.det() == -1

    generic_rows = sp.symbols("r0:16")
    row_vectors = tuple(
        sp.Matrix(generic_rows[4 * index : 4 * index + 4])
        for index in range(4)
    )
    pairing_value = (
        pair_contraction(row_vectors[0], row_vectors[1]).T
        * complement_pairing
        * pair_contraction(row_vectors[2], row_vectors[3])
    )[0]
    assert sp.expand(pairing_value - permanent4(row_vectors)) == 0

    # The two rank-three restrictions have projective kernel lines
    # (1,rho,1,1) and (1,sigma,1,-1).  These bases cover rho,sigma=0.
    kernel_a = sp.Matrix([1, rho, 1, 1])
    kernel_y = sp.Matrix([1, sigma, 1, -1])
    rows_a = (
        sp.Matrix([-rho, 1, 0, 0]),
        sp.Matrix([-1, 0, 1, 0]),
        sp.Matrix([-1, 0, 0, 1]),
    )
    rows_y = (
        sp.Matrix([-sigma, 1, 0, 0]),
        sp.Matrix([-1, 0, 1, 0]),
        sp.Matrix([1, 0, 0, 1]),
    )
    assert all((row.T * kernel_a)[0] == 0 for row in rows_a)
    assert all((row.T * kernel_y)[0] == 0 for row in rows_y)
    assert sp.Matrix.hstack(*rows_a).rank() == 3
    assert sp.Matrix.hstack(*rows_y).rank() == 3

    ay_pair_image = sp.Matrix.hstack(
        *(
            pair_contraction(row_a, row_y)
            for row_a in rows_a
            for row_y in rows_y
        )
    )
    ay_witness = sp.factor(
        ay_pair_image.extract(
            (0, 1, 2, 4, 5),
            (1, 2, 4, 5, 6),
        ).det()
    )
    assert ay_witness == 4

    # First Schubert chart: U contains h and V contains u.
    x_s, x_p, x_q, y_s, y_p, y_q = sp.symbols(
        "x_s x_p x_q y_s y_p y_q"
    )
    x = sp.Matrix([0, x_s, x_p, x_q])
    y = sp.Matrix([0, y_s, y_p, y_q])
    moving_pair_image = sp.Matrix.hstack(
        pair_contraction(h, u),
        pair_contraction(h, y),
        pair_contraction(x, u),
        pair_contraction(x, y),
    )
    moving_minors = all_minors(moving_pair_image, 3)
    moving_groebner = sp.groebner(
        moving_minors,
        x_s,
        y_s,
        x_p,
        x_q,
        y_p,
        y_q,
        order="grevlex",
    )
    expected_groebner = {
        x_q * y_s**2,
        x_q * y_s * y_p,
        x_q * (y_p - y_q) * (y_p + y_q),
        x_s**2 * y_q,
        x_s * x_p * y_q,
        y_q * (x_p - x_q) * (x_p + x_q),
        x_s * x_q * y_q,
        x_q * y_s * y_q,
        x_s * y_s,
        y_s * (x_p + x_q),
        x_s * (y_p + y_q),
        (x_p + x_q) * (y_p + y_q),
    }
    assert {
        sp.factor(polynomial.as_expr())
        for polynomial in moving_groebner.polys
    } == expected_groebner

    reduced_pair_image = moving_pair_image.subs({x_s: 0, y_s: 0})
    reduced_minors = {
        sp.factor(minor)
        for minor in all_minors(reduced_pair_image, 3)
    }
    reduced_minors |= {-minor for minor in tuple(reduced_minors)}
    reduced_generators = {
        (x_p + x_q) * (y_p + y_q),
        (y_p + y_q) * (x_p * y_q + x_q * y_p),
        (x_p + x_q) * (x_p * y_q + x_q * y_p),
        (x_p * y_q - x_q * y_p)
        * (x_p * y_q + x_q * y_p),
    }
    assert reduced_generators <= reduced_minors

    # Second Schubert chart: U=P is fixed and V is arbitrary.  The two
    # linear maps have kernels u_plus and h_one.
    h_operator = sp.Matrix.hstack(
        *(pair_contraction(h, sp.eye(4)[:, index]) for index in range(4))
    )
    u_operator = sp.Matrix.hstack(
        *(pair_contraction(u, sp.eye(4)[:, index]) for index in range(4))
    )
    assert h_operator.rank() == 3
    assert u_operator.rank() == 3
    assert h_operator * u_plus == sp.zeros(6, 1)
    assert u_operator * h_one == sp.zeros(6, 1)

    v0, v1, v2, v3, w0, w1, w2, w3 = sp.symbols(
        "v0 v1 v2 v3 w0 w1 w2 w3"
    )
    vector_v = sp.Matrix([v0, v1, v2, v3])
    vector_w = sp.Matrix([w0, w1, w2, w3])
    common_image_solutions = sp.linsolve(
        tuple(h_operator * vector_v - u_operator * vector_w),
        (v0, v1, v2, v3, w0, w1, w2, w3),
    )
    solution_tuple = next(iter(common_image_solutions))
    assert sp.simplify(solution_tuple[1]) == 0
    assert sp.simplify(
        solution_tuple[0] - solution_tuple[2] - solution_tuple[3]
    ) == 0

    branch_s, branch_p, branch_q = sp.symbols(
        "branch_s branch_p branch_q"
    )
    branch_vector = sp.Matrix([0, branch_s, branch_p, branch_q])
    h_kernel_branch = sp.Matrix.hstack(
        h_operator * branch_vector,
        u_operator * u_plus,
        u_operator * branch_vector,
    )
    u_kernel_branch = sp.Matrix.hstack(
        h_operator * h_one,
        h_operator * branch_vector,
        u_operator * branch_vector,
    )
    branch_bases = []
    for branch_matrix in (h_kernel_branch, u_kernel_branch):
        branch_groebner = sp.groebner(
            all_minors(branch_matrix, 3),
            branch_s,
            branch_p,
            branch_q,
            order="grevlex",
        )
        branch_basis = {
            sp.factor(polynomial.as_expr())
            for polynomial in branch_groebner.polys
        }
        assert branch_basis == {
            branch_s**2,
            branch_s * branch_p,
            (branch_p - branch_q) * (branch_p + branch_q),
            branch_s * branch_q,
        }
        branch_bases.append(
            tuple(str(polynomial) for polynomial in branch_basis)
        )

    surviving_pairs = (
        ("Ph", "P"),
        ("Ph", "Pu"),
        ("P", "Ph"),
        ("P", "Pu"),
        ("P", "P0"),
    )
    for first, second in surviving_pairs:
        pair_image = sp.Matrix.hstack(
            *(
                pair_contraction(row_first, row_second)
                for row_first in planes[first]
                for row_second in planes[second]
            )
        )
        assert pair_image.rank() == 2

    # Every candidate has a parameter-independent nonzero 2x2 minor in
    # the complementary AY|CD flattening.
    flattening_witnesses = {
        ("Ph", "P"): ((1, 6), (0, 1), -4),
        ("Ph", "Pu"): ((2, 6), (0, 3), 4),
        ("P", "Ph"): ((1, 6), (0, 1), -4),
        ("P", "Pu"): ((2, 6), (2, 3), 4),
        ("P", "P0"): ((1, 2), (0, 2), 4),
    }
    verified_witnesses = {}
    for plane_pair, (row_indices, column_indices, expected) in (
        flattening_witnesses.items()
    ):
        first, second = plane_pair
        flattening = sp.Matrix(
            [
                [
                    permanent4((row_a, row_y, row_c, row_d))
                    for row_c in planes[first]
                    for row_d in planes[second]
                ]
                for row_a in rows_a
                for row_y in rows_y
            ]
        )
        witness = sp.factor(
            flattening.extract(row_indices, column_indices).det()
        )
        assert witness == expected
        verified_witnesses[f"{first},{second}"] = str(witness)

    output = {
        "verified": True,
        "field": "C",
        "parameter_stratum": "a=0, b*c != 0",
        "orientation": "q; p follows by singleton-colour symmetry",
        "pair_space_dimension": 6,
        "complement_pairing_determinant": int(complement_pairing.det()),
        "AY_pair_image_lower_bound": 5,
        "AY_minor_witness": str(ay_witness),
        "moving_schubert_survivors": [
            ["Ph", "P"],
            ["Ph", "Pu"],
            ["P", "Pu"],
        ],
        "fixed_P_survivors": [["P", "Ph"], ["P", "Pu"], ["P", "P0"]],
        "complete_quadrangle_pairs": [list(pair) for pair in surviving_pairs],
        "flattening_minor_witnesses": verified_witnesses,
        "adjacent_a0_excluded": True,
        "disjoint_a0_excluded": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_a0_adjacent_grassmann_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
