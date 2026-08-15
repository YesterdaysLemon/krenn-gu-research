"""Exact checks for the fixed-pair two-low zero-branch exclusion."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp

Vector = tuple[sp.Expr, ...]


def add(*vectors: Vector) -> Vector:
    """Add vectors coordinatewise."""
    return tuple(sp.expand(sum(vector[i] for vector in vectors)) for i in range(6))


def scale(value: sp.Expr, vector: Vector) -> Vector:
    """Scale one vector."""
    return tuple(sp.expand(value * entry) for entry in vector)


def evaluate(covector: Vector, vector: Vector) -> sp.Expr:
    """Evaluate a coordinate covector."""
    return sp.expand(sum(x * y for x, y in zip(covector, vector, strict=True)))


def polarized_product(factors: tuple[Vector, ...], vectors: tuple[Vector, ...]) -> sp.Expr:
    """Evaluate the complete polarization of four linear factors."""
    return sp.expand(
        sum(
            sp.prod(
                evaluate(factors[row], vectors[column])
                for row, column in enumerate(order)
            )
            for order in permutations(range(4))
        )
    )


def coordinate_vectors() -> tuple[Vector, ...]:
    """Return the six coordinate vectors."""
    return tuple(tuple(sp.Integer(i == j) for i in range(6)) for j in range(6))


def quartics() -> dict[str, tuple[sp.Expr, tuple[Vector, ...]]]:
    """Return the five factorized fixed-pair quartics."""
    x0, x1, x2, x3, x4, x5 = coordinate_vectors()
    l1 = add(x3, scale(-1, x2), scale(-1, x0))
    l2 = add(x3, scale(-1, x2), scale(-1, x1))
    return {
        "m1": (sp.Integer(1), (x4, x5, x1, l1)),
        "m2": (sp.Integer(1), (x4, x5, x0, l2)),
        "d0": (sp.Integer(1), (x4, x5, add(x1, x2), add(x3, scale(-1, x0)))),
        "d1": (sp.Integer(1), (x4, x5, add(x0, x2), add(x3, scale(-1, x1)))),
        "d2": (sp.Integer(-2), (x4, x5, x0, x1)),
    }


def exceptional_lines() -> dict[str, Vector]:
    """Return normalized noncommon exceptional generators."""
    return {
        "A0": tuple(map(sp.Integer, (1, 0, 0, 1, 0, 0))),
        "C0": tuple(map(sp.Integer, (1, 0, -1, 0, 0, 0))),
        "A1": tuple(map(sp.Integer, (0, 1, 0, 1, 0, 0))),
        "C1": tuple(map(sp.Integer, (0, 1, -1, 0, 0, 0))),
    }


def check_opposite_mixed_contractions() -> dict[str, tuple[int, ...]]:
    """Check the four exact single-contraction covectors."""
    x0, x1, x2, x3, x4, x5 = coordinate_vectors()
    l1 = add(x3, scale(-1, x2), scale(-1, x0))
    l2 = add(x3, scale(-1, x2), scale(-1, x1))
    h1 = add(x1, l1)
    h2 = add(x0, l2)
    summary: dict[str, tuple[int, ...]] = {}
    for name, line in exceptional_lines().items():
        if name.endswith("0"):
            assert evaluate(x0, line) == evaluate(l2, line) == 1
            factors = quartics()["m2"][1]
            expected = h2
        else:
            assert evaluate(x1, line) == evaluate(l1, line) == 1
            factors = quartics()["m1"][1]
            expected = h1
        contraction = tuple(
            polarized_product(factors, (line, x4, x5, basis))
            for basis in coordinate_vectors()
        )
        assert contraction == expected
        summary[name] = tuple(map(int, contraction))
    return summary


def j_pair(left: Vector, right: Vector) -> sp.Expr:
    """Evaluate the hyperbolic pairing on A-coordinates."""
    return sp.expand(left[4] * right[5] + left[5] * right[4])


def symbolic_vector(prefix: str) -> Vector:
    """Return one generic ambient vector."""
    return tuple(sp.symbols(f"{prefix}0:6"))


def rank_one_high(prefix: str, image: tuple[sp.Expr, sp.Expr], rho: sp.Expr) -> Vector:
    """Return a generic R-vector with prescribed rank-one A-coordinate."""
    entries = sp.symbols(f"{prefix}0:4")
    return (*entries, image[0] * rho, image[1] * rho)


def check_symbolic_mixed_factorization() -> dict[str, int]:
    """Directly polarize both legal low-slot contractions."""
    u4, u5, v4, v5, rs, rt = sp.symbols("u4 u5 v4 v5 rs rt")
    u = (u4, u5)
    v = (v4, v5)
    b = symbolic_vector("b")
    a = symbolic_vector("a")
    s = rank_one_high("s", u, rs)
    t = rank_one_high("t", v, rt)
    x0, x1, x2, x3, _, _ = coordinate_vectors()
    l1 = add(x3, scale(-1, x2), scale(-1, x0))
    l2 = add(x3, scale(-1, x2), scale(-1, x1))
    h1 = add(x1, l1)
    h2 = add(x0, l2)
    j_uv = sp.expand(u4 * v5 + u5 * v4)

    checked = 0
    for name in ("A0", "C0"):
        low = exceptional_lines()[name]
        direct = polarized_product(quartics()["m2"][1], (low, b, s, t))
        expected = sp.expand(
            j_pair(b, s) * evaluate(h2, t)
            + j_pair(b, t) * evaluate(h2, s)
            + j_uv * rs * rt * evaluate(h2, b)
        )
        assert sp.expand(direct - expected) == 0
        checked += 1

    for name in ("A1", "C1"):
        low = exceptional_lines()[name]
        direct = polarized_product(quartics()["m1"][1], (low, a, s, t))
        expected = sp.expand(
            j_pair(a, s) * evaluate(h1, t)
            + j_pair(a, t) * evaluate(h1, s)
            + j_uv * rs * rt * evaluate(h1, a)
        )
        assert sp.expand(direct - expected) == 0
        checked += 1

    return {"symbolic_factorizations": checked}


def check_high_covector_independence_identity() -> dict[str, sp.Expr]:
    """Check the determinant identity behind highness."""
    x = sp.symbols("x0:3")
    ell = sp.symbols("ell0:3")
    rho = sp.symbols("rho0:3")
    h = tuple(xi + li for xi, li in zip(x, ell, strict=True))
    original = sp.Matrix((x, ell, rho)).det()
    contracted = sp.Matrix((x, h, rho)).det()
    assert sp.expand(original - contracted) == 0
    assert original != 0
    return {"det_x_l_rho": sp.expand(original), "det_x_h_rho": sp.expand(contracted)}


def rank_mod(columns: tuple[tuple[int, ...], ...], prime: int) -> int:
    """Return column rank over one prime field."""
    work = [list(row) for row in zip(*columns, strict=True)]
    row = 0
    for column in range(len(columns)):
        pivot = next((i for i in range(row, len(work)) if work[i][column] % prime), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = pow(work[row][column] % prime, prime - 2, prime)
        work[row] = [(inverse * entry) % prime for entry in work[row]]
        for i in range(len(work)):
            if i == row:
                continue
            factor = work[i][column] % prime
            if factor:
                work[i] = [
                    (entry - factor * pivot_entry) % prime
                    for entry, pivot_entry in zip(work[i], work[row], strict=True)
                ]
        row += 1
        if row == len(work):
            break
    return row


def tensor_product(left: tuple[int, ...], right: tuple[int, ...], prime: int) -> tuple[int, ...]:
    """Flatten one outer product."""
    return tuple((x * y) % prime for x in left for y in right)


def check_no_two_term_cancellation() -> dict[str, int]:
    """Exhaust the pure-tensor cancellation lemma over F3."""
    prime = 3
    vectors = tuple(v for v in product(range(prime), repeat=3) if any(v))
    checked = 0
    for rho_s in vectors:
        for h_s in vectors:
            if rank_mod((rho_s, h_s), prime) != 2:
                continue
            for rho_t in vectors:
                for h_t in vectors:
                    first = tensor_product(rho_s, h_t, prime)
                    second = tensor_product(h_s, rho_t, prime)
                    assert rank_mod((first, second), prime) == 2
                    checked += 1
    assert checked == 421_824
    return {"F3_cancellation_cases": checked}


def j_pair_mod(left: tuple[int, int], right: tuple[int, int], prime: int) -> int:
    """Evaluate J over a prime field."""
    return (left[0] * right[1] + left[1] * right[0]) % prime


def check_orthogonal_line_dichotomy() -> dict[str, int]:
    """Exhaust the final two-dimensional dichotomy over F5."""
    prime = 5
    vectors = tuple(v for v in product(range(prime), repeat=2) if any(v))
    zero = (0, 0)
    independent = 0
    dependent = 0
    for u in vectors:
        for v in vectors:
            if j_pair_mod(u, v, prime):
                continue
            allowed = tuple(
                w
                for w in (zero, *vectors)
                if j_pair_mod(w, u, prime) == j_pair_mod(w, v, prime) == 0
            )
            if rank_mod((u, v), prime) == 2:
                assert allowed == (zero,)
                independent += 1
            else:
                assert j_pair_mod(u, u, prime) == 0
                assert all(rank_mod((u, w), prime) <= 1 for w in allowed)
                assert all(j_pair_mod(left, right, prime) == 0 for left in allowed for right in allowed)
                dependent += 1
    assert independent > 0 and dependent > 0
    return {"F5_independent_pairs": independent, "F5_dependent_pairs": dependent}


def main() -> None:
    """Run all exact replay checks."""
    print("opposite mixed contractions:", check_opposite_mixed_contractions())
    print("direct symbolic polarization:", check_symbolic_mixed_factorization())
    print("high-covector determinant identity:", check_high_covector_independence_identity())
    print("two-term cancellation:", check_no_two_term_cancellation())
    print("orthogonal-line dichotomy:", check_orthogonal_line_dichotomy())
    print("fixed-pair two-low zero-branch primary checks: PASS")


if __name__ == "__main__":
    main()
