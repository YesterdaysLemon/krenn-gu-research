"""Primary exact checks for the displayed star full-extension exclusion."""

from __future__ import annotations

import hashlib
from itertools import combinations
from pathlib import Path

import sympy as sp

Vector = tuple[sp.Expr, ...]
Polynomial = dict[int, sp.Expr]

ROOT = Path(__file__).resolve().parents[2]
EDGES = tuple(combinations(range(4), 2))
FULL_MASK = (1 << 6) - 1

M1 = (-1, 1, 0, 1, 0, 0)
M2 = (1, -1, 0, 0, -1, 1)
D0 = (-1, 2, -1, 1, 0, 1)
D1 = (1, 0, -1, 0, -1, 0)
D2 = (0, 0, 0, 2, 0, 0)
SOURCE_QUADRATICS = {"m1": M1, "m2": M2, "d0": D0, "d1": D1, "d2": D2}
CHANNELS = tuple(SOURCE_QUADRATICS)

DEPENDENCIES = {
    "claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md": "76AEBB661CA3E89DF3E4228954B0D7CB3D736414A4AB22C2EBC9A2C84A774D62",
    "claims/arbitrary-order/verify_arbitrary_permanent_star_pair_two_sided_projection_drop.py": "223B61126635FE59987B75684CFA6FCA1173737913CEAD0F46D98AA3A8C3DF1B",
    "claims/arbitrary-order/audit_arbitrary_permanent_star_pair_two_sided_projection_drop.py": "CD4D833DB7CB132FCFED02A0BD2353799E184DAC3DFAC9EC5F714F998F614311",
    "docs/audits/ARBITRARY_PERMANENT_STAR_PAIR_TWO_SIDED_PROJECTION_DROP_REVIEW_2026-08-15.md": "F0C61339191FDD02C6F72F721C175636DC4A302554C71FF51C8809747D30203F",
    "claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md": "2B44641806EEE9B14D2F9DCC692C2E8E1CB9917832A9C2FD9E658243ACFE51F5",
    "claims/arbitrary-order/verify_arbitrary_permanent_star_pair_kernel_support_boundary.py": "73406FF9C62A2113341BBC97E36E2E4F4151CF399E72EEBFD831A05944744124",
    "claims/arbitrary-order/audit_arbitrary_permanent_star_pair_kernel_support_boundary.py": "0D4F649C78577158E39577FB5CBDDA1A0057534E75A803F1EB73F25726DA5721",
    "docs/audits/ARBITRARY_PERMANENT_STAR_PAIR_KERNEL_SUPPORT_BOUNDARY_REVIEW_2026-08-15.md": "EC573CB950EFBCB9DFE300DBCEBDCE9992E6DF839EF77A45C038E605EA925A45",
    "claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_PAIR_SAME_MODE_NONCOMMON_AND_SUPPORT_TWO_BOUNDARY_THEOREM.md": "27AA460A9846A3568F3160DF3F6A03C798E87696D1A6E22900F13F8A76EF5AD9",
    "claims/arbitrary-order/verify_arbitrary_permanent_star_pair_same_mode_noncommon_and_support_two_boundary.py": "0D24DC727902A18824B5D5470542F5BDF7E87FDAB4C5D5FEBE5C439CCE4FFAEA",
    "claims/arbitrary-order/audit_arbitrary_permanent_star_pair_same_mode_noncommon_and_support_two_boundary.py": "E849C2F5A3D0A14414156F70DC7A58CF62B332585A4271268EB54B705719F543",
    "docs/audits/ARBITRARY_PERMANENT_STAR_PAIR_SAME_MODE_NONCOMMON_AND_SUPPORT_TWO_BOUNDARY_REVIEW_2026-08-15.md": "FB85A20E79B35020FECD790A6A9B5B2922F12B2D699C50052967AF434C164E82",
    "claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_PAIR_SINGLETON_NN_EXCLUSION_THEOREM.md": "EA29D52F17100A7D99F5A56254309B69BC21744E5C2BAFE78A981F19097B4693",
    "claims/arbitrary-order/verify_arbitrary_permanent_star_pair_singleton_nn_exclusion.py": "CED670F3D48B567CBC62B4759718E056E21A5E21CB1F42DDA85426F502A4B0FE",
    "claims/arbitrary-order/audit_arbitrary_permanent_star_pair_singleton_nn_exclusion.py": "8ADCB1EAF9B4E3C5B140463AEC89615DBE323A385DC3893030F57C10ECAFA031",
    "docs/audits/ARBITRARY_PERMANENT_STAR_PAIR_SINGLETON_NN_EXCLUSION_REVIEW_2026-08-15.md": "271D2C87D4F76FDF3541816183A40E83A3E7B5B8F9379FDEB6FC584188122535",
    "claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_TRIANGLE_EXCEPTIONAL_COMPANION_PROPAGATION_THEOREM.md": "9C70842573B3DD02BE5AC9CC65B08047AF0C6877892EA816A5D89B2024ED36A3",
    "claims/arbitrary-order/verify_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py": "97177FE5D7A44821428AAED34707FAD30490D50D80163609A28FB3AE7BE663F0",
    "claims/arbitrary-order/audit_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py": "9DB62582D752C85F2E7AE8343EC806B95786C5693466ECFB3666C5F838A35289",
    "docs/audits/ARBITRARY_PERMANENT_STAR_TRIANGLE_EXCEPTIONAL_COMPANION_PROPAGATION_REVIEW_2026-08-15.md": "7BDFE90C91664B8A8AF5C3B6BFC8997F274D8EB4BCBF863757CD63E81DC30300",
}

CYCLES = {
    "B0": {
        "p": (1, 0, 1, 0),
        "allowed": (1, 2),
        "q": (-1, 0, 1, 0),
        "e": 0,
        "r_p": (0, -1, 0, 1, -1),
        "r_q": (0, 0, 1, 0, 0),
        "ell": (0, -2, 0, -2),
        "relation": (-1, 1, 1, -1, 1),
    },
    "C0": {
        "p": (1, -1, 0, 0),
        "allowed": (0, 2),
        "q": (1, 1, 0, 0),
        "e": 1,
        "r_p": (0, 1, -1, 0, -1),
        "r_q": (0, 0, 0, 1, 0),
        "ell": (0, 0, -2, 0),
        "relation": (-3, -1, 1, 0, 1),
    },
    "B1": {
        "p": (1, 0, 0, 1),
        "allowed": (0, 2),
        "q": (-1, 0, 0, 1),
        "e": 1,
        "r_p": (-3, 0, 1, 0, 1),
        "r_q": (0, 0, 0, 1, 0),
        "ell": (0, 0, 2, 0),
        "relation": (-3, -1, 1, 0, 1),
    },
    "C1": {
        "p": (1, 1, 1, 1),
        "allowed": (1, 2),
        "q": (-1, 1, 1, 1),
        "e": 0,
        "r_p": (-1, 0, 0, 1, 1),
        "r_q": (-2, 0, 1, 0, 0),
        "ell": (0, -2, 0, 2),
        "relation": (-1, -1, 0, 1, 1),
    },
}


def sha256(path: Path) -> str:
    """Hash text after normalizing checkout CRLF to Git-style LF."""

    normalized = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(normalized).hexdigest().upper()


def assert_dependencies() -> dict[str, object]:
    """Pin every reviewed dependency byte-for-byte."""
    for relative, expected in DEPENDENCIES.items():
        path = ROOT / relative
        assert path.is_file()
        assert sha256(path) == expected
        if relative.startswith("docs/audits/"):
            assert "PASS" in path.read_text(encoding="utf-8")
    return {"files": len(DEPENDENCIES), "review_verdicts": 5, "hashes": "SHA-256"}


def first_four_product(left: Vector, right: Vector) -> tuple[sp.Expr, ...]:
    """Multiply two first-four forms in square-free edge order."""
    return tuple(
        sp.expand(left[first] * right[second] + left[second] * right[first])
        for first, second in EDGES
    )


def complement_core_matrix(quadratic: tuple[int, ...]) -> sp.Matrix:
    """Return the symmetric matrix of the complementary star core."""
    matrix = sp.zeros(4)
    vertices = set(range(4))
    for coefficient, edge in zip(quadratic, EDGES, strict=True):
        first, second = sorted(vertices - set(edge))
        matrix[first, second] += coefficient
        matrix[second, first] += coefficient
    return matrix


CORES = {
    name: complement_core_matrix(quadratic)
    for name, quadratic in SOURCE_QUADRATICS.items()
}


def contract(name: str, vector: Vector) -> sp.Matrix:
    """Contract one R slot of a complementary core."""
    return CORES[name] * sp.Matrix(vector)


def double_contract(name: str, first: Vector, second: Vector) -> sp.Expr:
    """Contract two distinct R slots of a complementary core."""
    return sp.expand((sp.Matrix(first).T * CORES[name] * sp.Matrix(second))[0])


def linear_combination(values: tuple[sp.Matrix, ...], coefficients: tuple[int, ...]) -> sp.Matrix:
    """Form an exact linear combination of column vectors."""
    return sum(
        (coefficient * value for coefficient, value in zip(coefficients, values, strict=True)),
        sp.zeros(values[0].rows, 1),
    )


def assert_star_and_cycle_table() -> dict[str, object]:
    """Reconstruct the star cores and all four common-cubic rows."""
    u = (
        (-1, 0, 1, 0),
        (1, 0, 0, -1),
        (0, 1, -1, 0),
    )
    v = (
        (1, 1, -1, 1),
        (1, 1, 0, 0),
        (0, -1, 1, 0),
    )
    products = tuple(tuple(first_four_product(left, right) for right in v) for left in u)
    assert products[0][1] == M1
    assert products[1][0] == M2
    assert products[0][0] == D0
    assert products[1][1] == D1
    assert products[2][2] == D2
    assert sp.Matrix([entry for row in products for entry in row]).rank() == 5

    replay = {}
    for name, data in CYCLES.items():
        p_rows = tuple(contract(channel, data["p"]) for channel in CHANNELS)
        q_rows = tuple(contract(channel, data["q"]) for channel in CHANNELS)
        ell = sp.Matrix(data["ell"])
        assert linear_combination(p_rows, data["r_p"]) == ell
        assert linear_combination(q_rows, data["r_q"]) == ell
        allowed = data["allowed"]
        companion = data["e"]
        assert set(allowed) | {companion} == {0, 1, 2}
        assert all(data["r_p"][2 + colour] != 0 for colour in allowed)
        assert data["r_p"][2 + companion] == 0
        assert data["r_q"][2 + companion] == 1
        assert all(data["r_q"][2 + colour] == 0 for colour in allowed)
        replay[name] = {
            "allowed": allowed,
            "companion_colour": companion,
            "ell": data["ell"],
            "low_diagonal_coefficients": tuple(data["r_p"][2 + colour] for colour in allowed),
        }
    return {"source_rank": 5, "cycles": replay, "support_branches": 12}


def core_polynomial(name: str, variables: Vector) -> sp.Expr:
    """Return the complementary quadratic polynomial."""
    return sp.expand(
        sum(
            CORES[name][first, second] * variables[first] * variables[second]
            for first, second in EDGES
        )
    )


def assert_restricted_core_relations() -> dict[str, object]:
    """Check every exact factor and both unused-colour coefficients."""
    x = sp.symbols("x0:4")
    polynomials = tuple(core_polynomial(channel, x) for channel in CHANNELS)
    expected_factors = {
        "B0": 2 * x[0] * (x[1] + x[3]),
        "C0": x[2] * (x[0] - x[1] + x[3]),
        "B1": x[2] * (x[0] - x[1] + x[3]),
        "C1": -(x[0] + x[2]) * (x[1] - x[3]),
    }
    result = {}
    for name, data in CYCLES.items():
        relation = data["relation"]
        actual = sp.factor(sum(coefficient * value for coefficient, value in zip(relation, polynomials, strict=True)))
        assert sp.expand(actual - expected_factors[name]) == 0
        kernel_basis = sp.Matrix([data["ell"]]).nullspace()
        assert len(kernel_basis) == 3
        inclusion = sp.Matrix.hstack(*kernel_basis)
        relation_matrix = sum(
            (coefficient * CORES[channel] for coefficient, channel in zip(relation, CHANNELS, strict=True)),
            sp.zeros(4),
        )
        assert inclusion.T * relation_matrix * inclusion == sp.zeros(3)
        unused_coefficients = tuple(relation[2 + colour] for colour in data["allowed"])
        assert all(unused_coefficients)
        result[name] = {
            "factor": expected_factors[name],
            "kernel_dimension": len(kernel_basis),
            "possible_unused_diagonal_coefficients": unused_coefficients,
        }
    return result


def square_free_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply in the six-variable square-free algebra."""
    result: Polynomial = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(result.get(mask, 0) + left_value * right_value)
    return {mask: value for mask, value in result.items() if value != 0}


def quartic_coefficient(quadratic: tuple[int, ...], vectors: tuple[Vector, ...]) -> sp.Expr:
    """Extract the full coefficient of q times four forms."""
    polynomial: Polynomial = {
        (1 << first) | (1 << second): sp.Integer(value)
        for value, (first, second) in zip(quadratic, EDGES, strict=True)
        if value
    }
    for vector in vectors:
        linear = {
            1 << index: sp.sympify(value)
            for index, value in enumerate(vector)
            if value != 0
        }
        polynomial = square_free_multiply(polynomial, linear)
    return sp.expand(polynomial.get(FULL_MASK, 0))


def j_form(left: Vector, right: Vector) -> sp.Expr:
    """Evaluate the x4,x5 hyperbolic form."""
    return sp.expand(left[4] * right[5] + left[5] * right[4])


def assert_full_quartic_factorizations() -> dict[str, int]:
    """Verify both all-colour factorizations for every cycle and channel."""
    a = sp.symbols("a0:6")
    b = sp.symbols("b0:6")
    c = sp.symbols("c0:6")
    d = sp.symbols("d0:6")
    generic_a: Vector = tuple(a)
    generic_b: Vector = tuple(b)
    generic_c: Vector = tuple(c)
    generic_d: Vector = tuple(d)
    checked = 0

    for data in CYCLES.values():
        kernel = sp.Matrix([data["ell"]]).nullspace()
        inclusion = sp.Matrix.hstack(*kernel)
        rank_three_a_r = inclusion * sp.Matrix(a[:3])
        rank_three_b_r = inclusion * sp.Matrix(b[:3])
        rank_two_c_r = inclusion * sp.Matrix(c[:3])
        rank_two_d_r = inclusion * sp.Matrix(d[:3])
        rank_three_a: Vector = (*tuple(rank_three_a_r), 0, 0)
        rank_three_b: Vector = (*tuple(rank_three_b_r), 0, 0)
        rank_two_c: Vector = (*tuple(rank_two_c_r), 0, 0)
        rank_two_d: Vector = (*tuple(rank_two_d_r), 0, 0)

        for name, quadratic in SOURCE_QUADRATICS.items():
            actual_three = quartic_coefficient(
                quadratic,
                (rank_three_a, rank_three_b, generic_c, generic_d),
            )
            expected_three = sp.expand(
                double_contract(name, rank_three_a[:4], rank_three_b[:4])
                * j_form(generic_c, generic_d)
            )
            assert sp.expand(actual_three - expected_three) == 0

            actual_two = quartic_coefficient(
                quadratic,
                (generic_a, generic_b, rank_two_c, rank_two_d),
            )
            expected_two = sp.expand(
                j_form(generic_a, generic_b)
                * double_contract(name, rank_two_c[:4], rank_two_d[:4])
            )
            assert sp.expand(actual_two - expected_two) == 0
            checked += 2
    return {"cycles": len(CYCLES), "channels": len(CHANNELS), "symbolic_factorizations": checked}


def p_xuv(first: Vector, second: Vector, third: Vector) -> sp.Expr:
    """Evaluate the full polarization of XUV."""
    return sp.expand(
        first[0] * (second[1] * third[2] + second[2] * third[1])
        + first[1] * (second[0] * third[2] + second[2] * third[0])
        + first[2] * (second[0] * third[1] + second[1] * third[0])
    )


def assert_xuv_gates() -> dict[str, object]:
    """Check the annihilator minors and rank-one-free slice obstruction."""
    basis = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    x, u, v = sp.symbols("x u v")
    vector = (x, u, v)
    annihilator = sp.Matrix(
        3,
        3,
        lambda row, column: p_xuv(basis[row], basis[column], vector),
    )
    assert annihilator == sp.Matrix(((0, v, u), (v, 0, x), (u, x, 0)))
    minors = tuple(
        sp.factor(annihilator.extract(indices, indices).det())
        for indices in ((0, 1), (0, 2), (1, 2))
    )
    assert minors == (-v**2, -u**2, -x**2)

    slice_x = sp.Matrix(((0, 0, 0), (0, 0, 1), (0, 1, 0)))
    slice_u = sp.Matrix(((0, 0, 1), (0, 0, 0), (1, 0, 0)))
    slice_v = sp.Matrix(((0, 1, 0), (1, 0, 0), (0, 0, 0)))
    assert sp.Matrix.hstack(
        slice_x.reshape(9, 1),
        slice_u.reshape(9, 1),
        slice_v.reshape(9, 1),
    ).rank() == 3
    r, s, t = sp.symbols("r s t")
    general = r * slice_x + s * slice_u + t * slice_v
    rank_one_minors = tuple(
        sp.factor(general.extract(indices, indices).det())
        for indices in ((0, 1), (0, 2), (1, 2))
    )
    assert rank_one_minors == (-t**2, -s**2, -r**2)

    diagonal_lines = []
    for colour in range(3):
        matrix = sp.zeros(3)
        matrix[colour, colour] = 1
        diagonal_lines.append(matrix.reshape(9, 1))
    assert sp.Matrix.hstack(*diagonal_lines).rank() == 3
    return {
        "annihilator_minors": minors,
        "slice_space_rank": 3,
        "rank_one_slice_minors": rank_one_minors,
        "weighted_delta_slice_rank": 3,
    }


def assert_proof_topology() -> dict[str, object]:
    """Exhaust the reviewed kernel and support leaves."""
    phi1 = ("N", "B0", "C0")
    phi2 = ("N", "B1", "C1")
    noncommon = tuple(line for line in (*phi1, *phi2) if line != "N")
    assert noncommon == tuple(CYCLES)
    branches = []
    for name, data in CYCLES.items():
        allowed = data["allowed"]
        supports = ((allowed[0],), (allowed[1],), allowed)
        branches.extend((name, support) for support in supports)
    assert len(branches) == 12
    assert all(set(support) <= set(CYCLES[name]["allowed"]) for name, support in branches)
    return {
        "rank_drop_families": 2,
        "common_line_leaf": "removed by same-mode exclusion",
        "noncommon_lines": noncommon,
        "support_leaves": len(branches),
        "endpoint": "displayed based frame only",
    }


def main() -> None:
    """Run all primary exact checks."""
    dependencies = assert_dependencies()
    cycles = assert_star_and_cycle_table()
    relations = assert_restricted_core_relations()
    factorizations = assert_full_quartic_factorizations()
    xuv = assert_xuv_gates()
    topology = assert_proof_topology()
    print("star-pair displayed-frame full-extension exclusion primary checks: PASS")
    print(f"  frozen dependencies: {dependencies}")
    print(f"  common-cubic cycles: {cycles}")
    print(f"  restricted core relations: {relations}")
    print(f"  full quartic factorizations: {factorizations}")
    print(f"  XUV gates: {xuv}")
    print(f"  proof topology: {topology}")


if __name__ == "__main__":
    main()
