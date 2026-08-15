"""Independent no-import audit of the two-low zero-branch exclusion."""

from __future__ import annotations

from itertools import permutations, product

Vector = tuple[int, ...]
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, int]


def linear_form(*entries: int) -> dict[int, int]:
    """Return the sparse dictionary of one linear form."""
    return {index: value for index, value in enumerate(entries) if value}


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply square-free polynomials, discarding repeated variables."""
    answer: Polynomial = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            if set(monomial_left) & set(monomial_right):
                continue
            monomial = tuple(sorted((*monomial_left, *monomial_right)))
            answer[monomial] = answer.get(monomial, 0) + coefficient_left * coefficient_right
    return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient}


def product_of_forms(forms: tuple[dict[int, int], ...], coefficient: int = 1) -> Polynomial:
    """Build a square-free polynomial from linear factors."""
    answer: Polynomial = {(): coefficient}
    for form in forms:
        answer = multiply(answer, {(index,): value for index, value in form.items()})
    return answer


def evaluate_monomial(monomial: Monomial, vectors: tuple[Vector, ...]) -> int:
    """Evaluate the complete polarization of one square-free monomial."""
    return sum(
        _product(vectors[column][coordinate] for coordinate, column in zip(monomial, order, strict=True))
        for order in permutations(range(len(monomial)))
    )


def _product(values: object) -> int:
    """Multiply an iterable of integers without importing math."""
    answer = 1
    for value in values:
        answer *= int(value)
    return answer


def polarize(polynomial: Polynomial, vectors: tuple[Vector, ...]) -> int:
    """Evaluate a homogeneous polynomial's complete polarization."""
    return sum(coefficient * evaluate_monomial(monomial, vectors) for monomial, coefficient in polynomial.items())


def fixed_quartics() -> dict[str, Polynomial]:
    """Independently reconstruct the five fixed-pair quartics."""
    x0 = linear_form(1, 0, 0, 0, 0, 0)
    x1 = linear_form(0, 1, 0, 0, 0, 0)
    x4 = linear_form(0, 0, 0, 0, 1, 0)
    x5 = linear_form(0, 0, 0, 0, 0, 1)
    l1 = linear_form(-1, 0, -1, 1, 0, 0)
    l2 = linear_form(0, -1, -1, 1, 0, 0)
    return {
        "m1": product_of_forms((x4, x5, x1, l1)),
        "m2": product_of_forms((x4, x5, x0, l2)),
        "d0": product_of_forms((x4, x5, linear_form(0, 1, 1, 0, 0, 0), linear_form(-1, 0, 0, 1, 0, 0))),
        "d1": product_of_forms((x4, x5, linear_form(1, 0, 1, 0, 0, 0), linear_form(0, -1, 0, 1, 0, 0))),
        "d2": product_of_forms((x4, x5, x0, x1), coefficient=-2),
    }


def basis(index: int) -> Vector:
    """Return one ambient coordinate vector."""
    return tuple(int(i == index) for i in range(6))


def covector_by_contraction(polynomial: Polynomial, low: Vector) -> Vector:
    """Read a remaining R-covector after supplying x4 and x5."""
    return tuple(polarize(polynomial, (low, basis(4), basis(5), basis(i))) for i in range(6))


def check_contractions() -> dict[str, Vector]:
    """Check all four opposite mixed contractions independently."""
    lines = {
        "A0": (1, 0, 0, 1, 0, 0),
        "C0": (1, 0, -1, 0, 0, 0),
        "A1": (0, 1, 0, 1, 0, 0),
        "C1": (0, 1, -1, 0, 0, 0),
    }
    expected = {
        "A0": (1, -1, -1, 1, 0, 0),
        "C0": (1, -1, -1, 1, 0, 0),
        "A1": (-1, 1, -1, 1, 0, 0),
        "C1": (-1, 1, -1, 1, 0, 0),
    }
    quartic = fixed_quartics()
    found = {
        name: covector_by_contraction(quartic["m2" if name.endswith("0") else "m1"], line)
        for name, line in lines.items()
    }
    assert found == expected
    return found


def j_pair(left: Vector, right: Vector) -> int:
    """Pair the last two coordinates."""
    return left[4] * right[5] + left[5] * right[4]


def dot(covector: Vector, vector: Vector) -> int:
    """Evaluate a covector."""
    return sum(x * y for x, y in zip(covector, vector, strict=True))


def with_a_part(r_part: tuple[int, int, int, int], a_part: tuple[int, int]) -> Vector:
    """Join R and A coordinates."""
    return (*r_part, *a_part)


def check_direct_polarization_fixtures() -> dict[str, int]:
    """Compare independent polarization with the displayed factorization."""
    quartic = fixed_quartics()
    lines = {
        "A0": (1, 0, 0, 1, 0, 0),
        "C0": (1, 0, -1, 0, 0, 0),
        "A1": (0, 1, 0, 1, 0, 0),
        "C1": (0, 1, -1, 0, 0, 0),
    }
    h1 = (-1, 1, -1, 1, 0, 0)
    h2 = (1, -1, -1, 1, 0, 0)
    r_b = ((1, 2, -1, 3), (-2, 1, 4, 0), (3, -1, 2, 1))
    a_b = ((1, 2), (-1, 3), (2, -2))
    r_s = ((2, 0, 1, -1), (1, -2, 3, 2), (0, 1, -1, 4))
    r_t = ((-1, 3, 0, 2), (2, 1, -2, 0), (4, -1, 1, 3))
    rho_s = (1, -2, 3)
    rho_t = (2, 1, -1)
    image_pairs = (((1, 1), (1, -1)), ((1, 0), (1, 0)))
    checked = 0
    for u, v in image_pairs:
        assert u[0] * v[1] + u[1] * v[0] == 0
        b_columns = tuple(with_a_part(r_b[i], a_b[i]) for i in range(3))
        s_columns = tuple(with_a_part(r_s[i], (u[0] * rho_s[i], u[1] * rho_s[i])) for i in range(3))
        t_columns = tuple(with_a_part(r_t[i], (v[0] * rho_t[i], v[1] * rho_t[i])) for i in range(3))
        for name, low in lines.items():
            polynomial = quartic["m2" if name.endswith("0") else "m1"]
            h = h2 if name.endswith("0") else h1
            for i, j, k in product(range(3), repeat=3):
                direct = polarize(polynomial, (low, b_columns[i], s_columns[j], t_columns[k]))
                formula = (
                    j_pair(b_columns[i], s_columns[j]) * dot(h, t_columns[k])
                    + j_pair(b_columns[i], t_columns[k]) * dot(h, s_columns[j])
                )
                assert direct == formula
                checked += 1
    assert checked == 216
    return {"direct_fixture_entries": checked}


def rank_mod(columns: tuple[tuple[int, ...], ...], prime: int) -> int:
    """Independent small-matrix column rank."""
    matrix = [list(row) for row in zip(*columns, strict=True)]
    rank = 0
    column = 0
    while rank < len(matrix) and column < len(columns):
        pivot = next((row for row in range(rank, len(matrix)) if matrix[row][column] % prime), None)
        if pivot is None:
            column += 1
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column] % prime, prime - 2, prime)
        matrix[rank] = [(inverse * value) % prime for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank:
                continue
            factor = matrix[row][column] % prime
            matrix[row] = [
                (value - factor * pivot_value) % prime
                for value, pivot_value in zip(matrix[row], matrix[rank], strict=True)
            ]
        rank += 1
        column += 1
    return rank


def outer(left: tuple[int, ...], right: tuple[int, ...], prime: int) -> tuple[int, ...]:
    """Flatten an outer product modulo a prime."""
    return tuple((x * y) % prime for x in left for y in right)


def audit_cancellation() -> dict[str, int]:
    """Seek a finite-field counterexample to the cancellation step."""
    prime = 3
    vectors = tuple(vector for vector in product(range(prime), repeat=3) if any(vector))
    checked = 0
    for rho_s in vectors:
        for h_s in vectors:
            if rank_mod((rho_s, h_s), prime) != 2:
                continue
            for rho_t in vectors:
                for h_t in vectors:
                    assert rank_mod((outer(rho_s, h_t, prime), outer(h_s, rho_t, prime)), prime) == 2
                    checked += 1
    assert checked == 421_824
    return {"F3_no_cancellation_cases": checked}


def det3(rows: tuple[tuple[int, int, int], ...]) -> int:
    """Compute a three-by-three determinant directly."""
    a, b, c = rows
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def audit_high_independence() -> dict[str, int]:
    """Check det(x,l,rho)=det(x,x+l,rho) on a rational grid."""
    rows = tuple(product((-1, 0, 1), repeat=3))
    checked = 0
    full_rank = 0
    for x in rows:
        for ell in rows:
            h = tuple(a + b for a, b in zip(x, ell, strict=True))
            for rho in rows:
                left = det3((x, ell, rho))
                right = det3((x, h, rho))
                assert left == right
                if left:
                    assert rank_mod((rho, h), 5) == 2
                    full_rank += 1
                checked += 1
    return {"determinant_grid_cases": checked, "full_rank_cases": full_rank}


def pair2(left: tuple[int, int], right: tuple[int, int], prime: int) -> int:
    """Pair two vectors in the hyperbolic plane modulo a prime."""
    return (left[0] * right[1] + left[1] * right[0]) % prime


def audit_orthogonal_dichotomy() -> dict[str, int]:
    """Independently exhaust the final plane argument over F7."""
    prime = 7
    nonzero = tuple(vector for vector in product(range(prime), repeat=2) if any(vector))
    all_vectors = ((0, 0), *nonzero)
    independent = 0
    dependent = 0
    for u in nonzero:
        for v in nonzero:
            if pair2(u, v, prime):
                continue
            common_orthogonal = tuple(
                w for w in all_vectors if pair2(w, u, prime) == pair2(w, v, prime) == 0
            )
            if rank_mod((u, v), prime) == 2:
                assert common_orthogonal == ((0, 0),)
                independent += 1
            else:
                assert pair2(u, u, prime) == 0
                assert all(rank_mod((u, w), prime) <= 1 for w in common_orthogonal)
                assert all(pair2(x, y, prime) == 0 for x in common_orthogonal for y in common_orthogonal)
                dependent += 1
    assert independent and dependent
    return {"F7_independent_pairs": independent, "F7_dependent_pairs": dependent}


def main() -> None:
    """Run the independent audit."""
    print("independent contractions:", check_contractions())
    print("independent direct polarization:", check_direct_polarization_fixtures())
    print("independent determinant audit:", audit_high_independence())
    print("independent cancellation audit:", audit_cancellation())
    print("independent orthogonal dichotomy:", audit_orthogonal_dichotomy())
    print("fixed-pair two-low zero-branch independent audit: PASS")


if __name__ == "__main__":
    main()
