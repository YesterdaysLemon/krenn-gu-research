"""Primary exact checks for the triangle same-mode two-low exclusion."""

from __future__ import annotations

import json
from itertools import combinations, permutations, product

import sympy as sp

Vector = tuple[sp.Expr, ...]


def add(*vectors: Vector) -> Vector:
    """Add vectors coordinatewise."""
    return tuple(sp.expand(sum(vector[i] for vector in vectors)) for i in range(6))


def scale(value: sp.Expr, vector: Vector) -> Vector:
    """Scale a vector."""
    return tuple(sp.expand(value * entry) for entry in vector)


def evaluate(covector: Vector, vector: Vector) -> sp.Expr:
    """Evaluate a covector on a vector."""
    return sp.expand(sum(x * y for x, y in zip(covector, vector, strict=True)))


def polarized_product(factors: tuple[Vector, ...], vectors: tuple[Vector, ...]) -> sp.Expr:
    """Evaluate the complete polarization of a product of linear factors."""
    return sp.expand(sum(
        sp.prod(evaluate(factors[row], vectors[column]) for row, column in enumerate(order))
        for order in permutations(range(len(factors)))
    ))


def data() -> tuple[dict[str, tuple[sp.Expr, tuple[Vector, ...]]], tuple[Vector, ...]]:
    """Return the coordinate covectors and five triangle quartics."""
    coordinates = tuple(
        tuple(sp.Integer(i == j) for i in range(6))
        for j in range(6)
    )
    x0, x1, x2, x3, x4, x5 = coordinates
    ell1 = add(x2, scale(-1, x1), scale(-1, x0))
    ell2 = add(x2, scale(-1, x1))
    factors = {
        "f1": (sp.Integer(1), (x4, x5, x3, ell1)),
        "f2": (sp.Integer(1), (x4, x5, x0, ell2)),
        "d0": (sp.Integer(2), (x4, x5, x0, x3)),
        "d1": (sp.Integer(1), (x4, x5, x2, add(x0, x1))),
        "d2": (sp.Integer(1), (x4, x5, x1, add(x0, scale(-1, x2)))),
    }
    return factors, coordinates


def residual(
    coefficient: sp.Expr,
    factors: tuple[Vector, ...],
    vector: Vector,
) -> Vector:
    """Contract a pure-R vector and extract the residual R-covector."""
    answer = []
    for coordinate in range(4):
        basis = tuple(sp.Integer(i == coordinate) for i in range(6))
        x4 = tuple(sp.Integer(i == 4) for i in range(6))
        x5 = tuple(sp.Integer(i == 5) for i in range(6))
        value = coefficient * polarized_product(factors, (vector, basis, x4, x5))
        answer.append(sp.expand(value))
    return tuple(answer)


def check_single_contractions_and_theta() -> dict[str, object]:
    """Check all exceptional contractions and the noncommon Theta gate."""
    factors, _coordinates = data()
    n = (0, 1, 1, 0, 0, 0)
    b_line = (1, 0, 1, 0, 0, 0)
    c_line = (1, -1, 0, 0, 0, 0)
    s_line = (0, 0, 0, 1, 0, 0)
    lines = {"N": n, "B": b_line, "C": c_line, "S": s_line}
    table = {
        line: {
            name: residual(coefficient, rows, vector)
            for name, (coefficient, rows) in factors.items()
        }
        for line, vector in lines.items()
    }

    assert table["B"]["f2"] == table["C"]["f2"] == (1, -1, 1, 0)
    assert table["S"]["f1"] == (-1, -1, 1, 0)
    assert table["B"]["d0"] == table["C"]["d0"] == (0, 0, 0, 2)
    assert table["S"]["d0"] == (2, 0, 0, 0)

    mixed_plane = sp.Matrix.hstack(
        sp.Matrix(table["B"]["f2"]),
        sp.Matrix(table["S"]["f1"]),
    )
    assert mixed_plane.rank() == 2
    beta0 = sp.symbols("beta0", nonzero=True)
    alpha0 = sp.symbols("alpha0")
    candidate = beta0 * sp.Matrix(table["B"]["d0"]) - alpha0 * sp.Matrix(table["S"]["d0"])
    assert sp.Matrix.hstack(mixed_plane, candidate).rank() == 3

    assert table["N"]["f1"] == table["N"]["f2"] == table["N"]["d0"] == (0, 0, 0, 0)
    assert table["N"]["d1"] == (1, 1, 1, 0)
    assert table["N"]["d2"] == (1, -1, -1, 0)
    residual_pair = sp.Matrix.vstack(
        sp.Matrix([table["N"]["d1"]]),
        sp.Matrix([table["N"]["d2"]]),
    )
    assert residual_pair.rank() == 2
    assert residual_pair.nullspace() == [
        sp.Matrix((0, -1, 1, 0)),
        sp.Matrix((0, 0, 0, 1)),
    ]

    return {
        "exceptional_lines_checked": sorted(lines),
        "mixed_kernel_dimension": 2,
        "noncommon_d0_augmented_rank": 3,
        "common_residual_kernel_basis": ["x1-x2", "x3"],
    }


def check_propagated_line_and_double_contractions() -> dict[str, object]:
    """Check the H-pencil contraction and the low-pair scalars."""
    factors, _coordinates = data()
    s, t = sp.symbols("s t")
    q = (0, s, -s, t, 0, 0)
    actual = {
        name: residual(coefficient, rows, q)
        for name, (coefficient, rows) in factors.items()
    }
    expected = {
        "f1": (-t, -t, t, -2 * s),
        "f2": (-2 * s, 0, 0, 0),
        "d0": (2 * t, 0, 0, 0),
        "d1": (-s, -s, s, 0),
        "d2": (s, s, -s, 0),
    }
    assert actual == expected

    n = (0, 1, 1, 0, 0, 0)
    x3 = (0, 0, 0, 1, 0, 0)

    def double_scalar(name: str, left: Vector, right: Vector) -> sp.Expr:
        coefficient, rows = factors[name]
        x4 = tuple(sp.Integer(i == 4) for i in range(6))
        x5 = tuple(sp.Integer(i == 5) for i in range(6))
        return sp.expand(coefficient * polarized_product(rows, (left, right, x4, x5)))

    nn = {name: double_scalar(name, n, n) for name in factors}
    ss = {name: double_scalar(name, x3, x3) for name in factors}
    assert nn == {"f1": 0, "f2": 0, "d0": 0, "d1": 2, "d2": -2}
    assert all(value == 0 for value in ss.values())
    return {
        "propagated_pencil_checked": True,
        "N_N_double_scalars": {name: str(value) for name, value in nn.items()},
        "S_S_all_zero": True,
    }


def check_hhpp_profile() -> dict[str, object]:
    """Exhaust the six coordinate-plane charts in the HHPP branch."""
    z = tuple(sp.eye(4).col(i) for i in range(4))
    parameter = sp.symbols("t", nonzero=True)

    def tensor_values(factors: tuple[sp.Matrix, ...], bases: tuple[list[sp.Matrix], ...]) -> list[sp.Expr]:
        return [
            sp.factor(sum(
                sp.prod((factors[order[slot]].T * vectors[slot])[0] for slot in range(3))
                for order in permutations(range(3))
            ))
            for vectors in product(*bases)
        ]

    report: dict[str, dict[str, object]] = {}
    zero_first = []
    for plane_indices in combinations(range(4), 2):
        complement = [index for index in range(4) if index not in plane_indices]
        i, j = complement
        plane = [z[index] for index in plane_indices]
        high_plus = [*plane, z[i] + parameter * z[j]]
        high_minus = [*plane, z[i] - parameter * z[j]]
        first = tensor_values((z[1], z[2], z[3] - z[0]), (plane, high_plus, high_minus))
        second = tensor_values((z[1], z[2], z[0]), (plane, high_plus, high_minus))
        first_nonzero = sorted({str(value) for value in first if value != 0})
        second_nonzero = any(value != 0 for value in second)
        key = "".join(str(index) for index in plane_indices)
        report[key] = {
            "first_nonzero_values": first_nonzero,
            "second_nonzero": second_nonzero,
        }
        if not first_nonzero:
            zero_first.append((plane_indices, second_nonzero))
    assert zero_first == [((0, 3), False)]
    return {"charts": report, "only_zero_first_chart": "03", "second_also_zero": True}


def check_coefficient_gate() -> dict[str, object]:
    """Exhaust the zero-factor split of the invertible 2x2 gate over F5."""
    prime = 5
    patterns: set[tuple[bool, bool, bool, bool]] = set()
    matrices = 0
    for r1, r2, s1, s2 in product(range(prime), repeat=4):
        determinant = (r1 * s2 - r2 * s1) % prime
        if not determinant:
            continue
        matrices += 1
        # Coefficients of A,B,C,D after solving (29), up to nonzero scalars.
        a_live = s2 % prime != 0
        b_live = s1 % prime != 0
        c_live = r2 % prime != 0
        d_live = r1 % prime != 0
        # A,C share rho_h; B,D share rho_b.  A shared factor cannot support
        # both E11 and E22.
        if a_live and c_live:
            continue
        if b_live and d_live:
            continue
        patterns.add((a_live, b_live, c_live, d_live))
    assert patterns == {
        (True, False, False, True),
        (False, True, True, False),
    }
    return {
        "field": "F_5",
        "invertible_coefficient_matrices": matrices,
        "surviving_zero_patterns_ABCD": sorted(patterns),
    }


def fixture() -> tuple[list[list[Vector]], dict[str, tuple[sp.Expr, tuple[Vector, ...]]]]:
    """Return the exact rational near-survivor and quartics."""
    half = sp.Rational(1, 2)
    quarter = sp.Rational(1, 4)
    planes = [
        [
            (1, 0, 0, 0, 0, 0),
            (0, 1, 1, 0, 0, 0),
            (0, 0, 0, 1, half, half),
        ],
        [
            (0, 0, 0, 1, 0, 0),
            (half, quarter, quarter, 0, 0, 0),
            (0, 0, 0, 0, 1, 1),
        ],
        [
            (1, 0, 0, 0, 0, 0),
            (0, 0, 0, 1, -half, half),
            (0, 1, 1, 0, 0, 0),
        ],
        [
            (0, 1, -1, 0, 0, 0),
            (0, 0, 0, 0, 1, -1),
            (half, 0, -half, 0, 0, 0),
        ],
    ]
    factors, _coordinates = data()
    return planes, factors


def check_near_survivor() -> dict[str, object]:
    """Replay the rational fixture and identify its off-target cells."""
    planes, factors = fixture()
    _factors, coordinates = data()
    x0, x1, x2, x3, x4, x5 = coordinates
    ell1 = add(x2, scale(-1, x1), scale(-1, x0))
    ell2 = add(x2, scale(-1, x1))
    phi1 = sp.Matrix([x3, x4, x5, ell1])
    phi2 = sp.Matrix([x0, x4, x5, ell2])
    rank_pairs = []
    for plane in planes:
        matrix = sp.Matrix.hstack(*(sp.Matrix(vector) for vector in plane))
        assert matrix.rank() == 3
        rank_pairs.append(((phi1 * matrix).rank(), (phi2 * matrix).rank()))
    assert rank_pairs == [(2, 2), (3, 2), (2, 2), (2, 3)]

    j_matrix = sp.Matrix(((0, 1), (1, 0)))
    a_b = sp.Matrix([[vector[4] for vector in planes[1]], [vector[5] for vector in planes[1]]])
    a_h = sp.Matrix([[vector[4] for vector in planes[3]], [vector[5] for vector in planes[3]]])
    assert a_b.T * j_matrix * a_h == sp.zeros(3, 3)

    def contracted_cells(fixed_mode: int, fixed_colour: int) -> dict[str, list[tuple[tuple[int, ...], str]]]:
        remaining_modes = [mode for mode in range(4) if mode != fixed_mode]
        answer: dict[str, list[tuple[tuple[int, ...], str]]] = {}
        for name, (coefficient, rows) in factors.items():
            cells = []
            for colours in product(range(3), repeat=3):
                vectors = [planes[fixed_mode][fixed_colour]]
                vectors.extend(planes[mode][colour] for mode, colour in zip(remaining_modes, colours, strict=True))
                value = sp.expand(coefficient * polarized_product(rows, tuple(vectors)))
                if value != 0:
                    cells.append((colours, str(value)))
            answer[name] = cells
        return answer

    first_n = contracted_cells(0, 1)
    second_n = contracted_cells(2, 2)
    x3_slice = contracted_cells(1, 0)
    assert first_n == {"f1": [], "f2": [], "d0": [], "d1": [((1, 1, 1), "1")], "d2": []}
    assert second_n == {"f1": [], "f2": [], "d0": [], "d1": [], "d2": [((2, 2, 2), "1")]}
    assert x3_slice["f1"] == [((0, 1, 1), "-1")]
    assert x3_slice["d0"] == [((0, 1, 1), "2")]
    assert all(plane[0][4:] == (0, 0) for plane in planes)

    return {
        "projection_rank_pairs": rank_pairs,
        "N_colour1_live_cell": first_n["d1"],
        "N_colour2_live_cell": second_n["d2"],
        "x3_off_target_f1": x3_slice["f1"],
        "x3_off_target_d0": x3_slice["d0"],
    }


def main() -> None:
    """Run all primary exact checks and print a deterministic report."""
    report = {
        "single_contractions_and_theta": check_single_contractions_and_theta(),
        "propagation_and_double_contractions": check_propagated_line_and_double_contractions(),
        "hhpp_profile": check_hhpp_profile(),
        "coefficient_gate": check_coefficient_gate(),
        "near_survivor": check_near_survivor(),
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
