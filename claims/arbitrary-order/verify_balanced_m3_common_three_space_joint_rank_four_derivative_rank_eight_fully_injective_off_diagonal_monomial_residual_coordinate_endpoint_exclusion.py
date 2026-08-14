#!/usr/bin/env python3
"""Exact replay of the off-diagonal monomial coordinate endpoint exclusion.

The owning theorem proves the projective atlas cover.  This verifier checks
the complete sparse target face (including the cross common zero), performs
independent finite-field sanity checks of every reduced flag cover, checks the
atlas lineage, and replays each canonical rational Nullstellensatz identity.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from itertools import permutations, product
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / (
    "balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_"
    "fully_injective_off_diagonal_monomial_residual_coordinate_endpoint_"
    "certificates.json"
)
CERTIFICATE_SHA256 = (
    "e940282a15261df2e5cc6d46c698b9bdb5e37299d5b5bb791dfeef4d711e3af1"
)
VARIABLES = (
    "x10",
    "x11",
    "x12",
    "x13",
    "y10",
    "y11",
    "y12",
    "y13",
    "z10",
    "z11",
    "z12",
    "z13",
    "x00",
    "x01",
    "x02",
    "x03",
    "y00",
    "y01",
    "y02",
    "y03",
    "z00",
    "z01",
    "z02",
    "z03",
    "p00",
    "p01",
    "p02",
    "p03",
    "p10",
    "p11",
    "p12",
    "p13",
    "q00",
    "q01",
    "q10",
    "q11",
)
SYMBOLS = sp.symbols(" ".join(VARIABLES))
SYMBOL_BY_NAME = dict(zip(VARIABLES, SYMBOLS, strict=True))

Row = tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]
FiniteVector = tuple[int, int, int]
FiniteFlag = tuple[FiniteVector, FiniteVector]


def complete_endpoint_face() -> None:
    """Reconstruct every constrained cell of the S2CC endpoint slice."""

    d, e, t = 0, 1, 2
    residual = sp.zeros(3, 3)
    residual[d, e] = 1
    gamma_rows = (sp.eye(3)[:, d], sp.eye(3)[:, e])
    expected: dict[tuple[int, int, int], str] = {}
    for i, j, k in product(range(3), range(3), range(2)):
        gamma = gamma_rows[k]
        target_coefficient = int(i == j) * gamma[i]
        residual_coefficient = residual[i, j]
        if target_coefficient:
            expected[i, j, k] = f"T{i}"
        elif residual_coefficient:
            expected[i, j, k] = f"S{k}"
        else:
            expected[i, j, k] = "0"

    assert expected[0, 0, 0] == "T0"
    assert expected[1, 1, 1] == "T1"
    assert {expected[0, 1, k] for k in range(2)} == {"S0", "S1"}
    assert all(
        expected[i, j, k] == "0"
        for i, j, k in product(range(2), range(2), range(2))
        if (i, j) != (0, 1) and (i, j, k) not in {(0, 0, 0), (1, 1, 1)}
    )
    # u=r_t and v=p_t are complete common rows, and their cross is zero.
    assert all(expected[t, j, k] == "0" for j, k in product(range(3), range(2)))
    assert all(expected[i, t, k] == "0" for i, k in product(range(3), range(2)))
    assert all(expected[t, t, k] == "0" for k in range(2))
    print("off-diagonal complete target face and cross-zero: PASS")


def normalize_vector(vector: FiniteVector, prime: int) -> FiniteVector:
    values = tuple(value % prime for value in vector)
    pivot = next(index for index, value in enumerate(values) if value)
    inverse = pow(values[pivot], -1, prime)
    return tuple(value * inverse % prime for value in values)  # type: ignore[return-value]


def flag(a: FiniteVector, b: FiniteVector, prime: int) -> FiniteFlag | None:
    wedge = (
        (a[0] * b[1] - a[1] * b[0]) % prime,
        (a[0] * b[2] - a[2] * b[0]) % prime,
        (a[1] * b[2] - a[2] * b[1]) % prime,
    )
    if not any(wedge):
        return None
    return normalize_vector(a, prime), normalize_vector(wedge, prime)


def all_flags(prime: int) -> set[FiniteFlag]:
    vectors = [
        vector
        for vector in product(range(prime), repeat=3)
        if any(vector)
    ]
    output = set()
    for a, b in product(vectors, repeat=2):
        value = flag(a, b, prime)
        if value is not None:
            output.add(value)
    return output


def pivot_rows(
    first_pivot: int,
    second_pivot: int,
    values: tuple[int, int, int],
) -> tuple[FiniteVector, FiniteVector]:
    remaining = next(
        index
        for index in range(3)
        if index not in {first_pivot, second_pivot}
    )
    first = [0, 0, 0]
    first[first_pivot] = 1
    free = [index for index in range(3) if index != first_pivot]
    first[free[0]], first[free[1]] = values[0], values[1]
    second = [0, 0, 0]
    second[second_pivot] = 1
    second[remaining] = values[2]
    return tuple(first), tuple(second)  # type: ignore[return-value]


def add_pivot_chart(
    output: set[FiniteFlag], first: int, second: int, prime: int
) -> None:
    for values in product(range(prime), repeat=3):
        value = flag(*pivot_rows(first, second, values), prime)
        assert value is not None
        output.add(value)


def add_parametric_chart(
    output: set[FiniteFlag],
    prime: int,
    parameter_count: int,
    rows: object,
) -> None:
    row_function = rows
    assert callable(row_function)
    for values in product(range(prime), repeat=parameter_count):
        a, b = row_function(*values)
        value = flag(a, b, prime)
        assert value is not None
        output.add(value)


def reduced_flag_cover(kind: str, prime: int) -> set[FiniteFlag]:
    output: set[FiniteFlag] = set()
    pivots: dict[str, tuple[int, int]]
    if kind == "outside_generic_affine":
        pivots = {"f02": (0, 2), "f20": (2, 0)}
        add_parametric_chart(
            output, prime, 2, lambda a, b: ((a, b, 1), (0, 1, 0))
        )
        add_parametric_chart(
            output, prime, 1, lambda a: ((0, 1, 0), (1, 0, a))
        )
        add_parametric_chart(
            output, prime, 0, lambda: ((0, 1, 0), (0, 0, 1))
        )
        add_parametric_chart(
            output, prime, 1, lambda a: ((1, a, 0), (0, 1, 0))
        )
    elif kind == "outside_generic_q1":
        pivots = {"f01": (0, 1), "f02": (0, 2), "f20": (2, 0), "f21": (2, 1)}
        add_parametric_chart(
            output, prime, 1, lambda a: ((0, 1, 0), (1, 0, a))
        )
        add_parametric_chart(
            output, prime, 0, lambda: ((0, 1, 0), (0, 0, 1))
        )
    elif kind == "inner_generic_affine":
        pivots = {"f12": (1, 2), "f20": (2, 0), "f21": (2, 1)}
        add_parametric_chart(
            output, prime, 1, lambda a: ((1, a, 0), (0, 1, 0))
        )
        add_parametric_chart(
            output, prime, 0, lambda: ((0, 1, 0), (1, 0, 0))
        )
        add_parametric_chart(
            output, prime, 0, lambda: ((1, 0, 0), (0, 0, 1))
        )
        add_parametric_chart(
            output, prime, 1, lambda a: ((1, 0, 0), (0, 1, a))
        )
    elif kind == "inner_generic_q1":
        pivots = {"f20": (2, 0), "f21": (2, 1)}
        add_parametric_chart(
            output,
            prime,
            2,
            lambda a, b: ((a, 1, 0), (b, 0, 1)),
        )
        add_parametric_chart(
            output, prime, 1, lambda a: ((1, a, 0), (0, 1, 0))
        )
        add_parametric_chart(
            output, prime, 0, lambda: ((0, 1, 0), (1, 0, 0))
        )
        add_parametric_chart(
            output, prime, 1, lambda a: ((1, 0, 0), (0, a, 1))
        )
    elif kind == "inner_default":
        pivots = {"f12": (1, 2), "f20": (2, 0), "f21": (2, 1)}
        add_parametric_chart(
            output, prime, 1, lambda a: ((1, a, 0), (0, 1, 0))
        )
        add_parametric_chart(
            output, prime, 0, lambda: ((0, 1, 0), (1, 0, 0))
        )
        add_parametric_chart(
            output, prime, 1, lambda a: ((1, 0, 0), (0, a, 1))
        )
    else:
        raise AssertionError(kind)
    for first, second in pivots.values():
        add_pivot_chart(output, first, second, prime)
    return output


def atlas_sanity() -> None:
    """Check the reduced charts and terminal orbit count independently."""

    for prime, expected_count in ((3, 52), (5, 186)):
        universe = all_flags(prime)
        assert len(universe) == expected_count
        for kind in (
            "outside_generic_affine",
            "outside_generic_q1",
            "inner_generic_affine",
            "inner_generic_q1",
            "inner_default",
        ):
            assert reduced_flag_cover(kind, prime) == universe, (kind, prime)

        # T\GL_2/B has three orbits; the nonzero Q-line has three torus
        # support orbits.  These are the 3 x 3 terminal graph charts.
        matrices = [
            (a, b, c, d)
            for a, b, c, d in product(range(prime), repeat=4)
            if (a * d - b * c) % prime
        ]
        quotient_representatives = (
            (1, 0, 0, 1),
            (0, 1, 1, 0),
            (1, 1, 1, 0),
        )
        quotient_orbits = set()
        for representative in quotient_representatives:
            a, b, c, d = representative
            for l0, l1, r0, r1, shear in product(
                range(1, prime),
                range(1, prime),
                range(1, prime),
                range(1, prime),
                range(prime),
            ):
                # left diagonal, then right upper triangular
                quotient_orbits.add(
                    (
                        l0 * a * r0 % prime,
                        l0 * (a * shear + b * r1) % prime,
                        l1 * c * r0 % prime,
                        l1 * (c * shear + d * r1) % prime,
                    )
                )
        assert quotient_orbits == set(matrices)
        assert {
            tuple(bool(value) for value in vector)
            for vector in product(range(prime), repeat=2)
            if any(vector)
        } == {(True, False), (False, True), (True, True)}
    print("projective flag and terminal orbit atlas: PASS")


def parse_row(raw_row: list[str]) -> Row:
    assert len(raw_row) == 4
    return tuple(
        sp.sympify(value, locals=SYMBOL_BY_NAME) for value in raw_row
    )  # type: ignore[return-value]


def form(root: str, bit: int) -> tuple[sp.Symbol, ...]:
    return tuple(
        SYMBOL_BY_NAME[f"{root}{bit}{coordinate}"] for coordinate in range(4)
    )


def evaluate(linear_form: tuple[sp.Symbol, ...], row: Row) -> sp.Expr:
    return sum(
        (
            coefficient * coordinate
            for coefficient, coordinate in zip(linear_form, row, strict=True)
        ),
        sp.Integer(0),
    )


def polarized_product(
    source_bits: tuple[int, int, int], rows: tuple[Row, Row, Row]
) -> sp.Expr:
    forms = (
        form("x", source_bits[0]),
        form("y", source_bits[1]),
        form("z", source_bits[2]),
    )
    return sp.expand(
        sum(
            (
                evaluate(forms[0], ordered[0])
                * evaluate(forms[1], ordered[1])
                * evaluate(forms[2], ordered[2])
                for ordered in permutations(rows)
            ),
            sp.Integer(0),
        )
    )


def case_generators(specification: dict[str, object]) -> list[sp.Poly]:
    raw_rows = specification["rows"]
    assert isinstance(raw_rows, list) and len(raw_rows) == 6
    rows = tuple(parse_row(row) for row in raw_rows)
    generators = []
    for source_bits in product(range(2), repeat=3):
        for row_bits in product(range(2), repeat=3):
            if row_bits[:2] == (0, 1):
                continue
            value = polarized_product(
                source_bits,
                (rows[row_bits[0]], rows[2 + row_bits[1]], rows[4 + row_bits[2]]),
            )
            if source_bits == (0, 0, 0) and row_bits == (0, 0, 0):
                value -= 1
            if source_bits == (1, 1, 1) and row_bits == (1, 1, 1):
                value -= 1
            generators.append(sp.Poly(value, *SYMBOLS, domain=sp.QQ))
    raw_physical = specification["physical_v"]
    if raw_physical is not None:
        assert isinstance(raw_physical, list)
        physical = parse_row(raw_physical)
        for source_bits in product(range(2), repeat=3):
            for i, k in product(range(2), repeat=2):
                value = polarized_product(
                    source_bits, (rows[i], physical, rows[4 + k])
                )
                generators.append(sp.Poly(value, *SYMBOLS, domain=sp.QQ))
    assert len(generators) == (80 if raw_physical is not None else 48)
    return generators


def multiplier_poly(encoded: list[list[object]]) -> sp.Poly:
    terms: dict[tuple[int, ...], sp.Rational] = {}
    for raw_coefficient, raw_sparse_exponent in encoded:
        coefficient = sp.Rational(str(raw_coefficient))
        assert coefficient
        exponent = [0] * len(VARIABLES)
        previous = -1
        for raw_index, raw_power in raw_sparse_exponent:  # type: ignore[misc]
            index = int(raw_index)
            power = int(raw_power)
            assert previous < index < len(VARIABLES)
            assert power > 0
            exponent[index] = power
            previous = index
        key = tuple(exponent)
        assert key not in terms
        terms[key] = coefficient
    return sp.Poly.from_dict(terms, *SYMBOLS, domain=sp.QQ)


def certificate_replay() -> None:
    raw = CERTIFICATE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA256
    data = json.loads(raw)
    assert data["format"] == "sparse-nullstellensatz-atlas-v2"
    assert tuple(data["variable_order"]) == VARIABLES
    assert data["generator_order"] == (
        "first_48_source_bits_then_nonexceptional_row_bits_lexicographic;"
        " physical_tail_source_bits_then_RQ_row_bits_lexicographic"
    )
    mapping = data["coverage_case_to_specification"]
    specifications = data["specifications"]
    certificates = data["cases"]
    assert data["coverage_case_count"] == len(mapping) == 317
    assert data["certificate_specification_count"] == len(specifications) == 287
    assert set(certificates) == set(specifications) == set(mapping.values())
    assert all(
        digest == specification["program_sha256"]
        for digest, specification in specifications.items()
    )
    assert Counter(data["coverage_case_stages"].values()) == {
        "separation_table": 210,
        "separation_refinement": 98,
        "endpoint_graph": 9,
    }
    assert Counter(data["coverage_case_kinds"].values()) == {
        "table_48": 210,
        "physical_80": 107,
    }
    multiplicities = Counter(mapping.values())
    assert sum(value - 1 for value in multiplicities.values()) == 30
    assert Counter(value for value in multiplicities.values() if value > 1) == {
        2: 12,
        4: 6,
    }

    zero = sp.Poly(0, *SYMBOLS, domain=sp.QQ)
    one = sp.Poly(1, *SYMBOLS, domain=sp.QQ)
    term_count = 0
    for index, digest in enumerate(sorted(specifications), start=1):
        generators = case_generators(specifications[digest])
        multipliers = certificates[digest]
        assert len(multipliers) == len(generators)
        total = zero
        for generator, encoded in zip(generators, multipliers, strict=True):
            term_count += len(encoded)
            total += multiplier_poly(encoded) * generator
        assert total == one, specifications[digest]["representative"]
        if index % 50 == 0:
            print(f"  exact certificate specifications replayed: {index}/287")
    assert term_count == 151484
    print(
        "off-diagonal Nullstellensatz certificates: PASS "
        f"(317 coverage charts / 287 systems / {term_count} multiplier terms)"
    )


def main() -> None:
    complete_endpoint_face()
    atlas_sanity()
    certificate_replay()
    print("off-diagonal monomial coordinate endpoint exclusion: PASS")


if __name__ == "__main__":
    main()
