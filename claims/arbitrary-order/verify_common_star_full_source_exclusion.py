"""Primary exact companion for the common-star full-source exclusion.

This is finite corroboration of the written all-order proof.  It checks the
literal physical AB-word source, the odd component-word contraction, and the
even four-probe rank obstruction with exact rational arithmetic.

Scope is deliberately split:

* odd component count uses component-constant targets only;
* even component count uses independently colored center/leaf AB words from
  the full physical GHZ source (CSFULL), not CSQ4 or FB.

No finite replay is presented as the all-order proof.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from typing import Iterable, Sequence


Scalar = Fraction
ColorVector = tuple[Scalar, Scalar, Scalar]
ColorWord = tuple[int, ...]

COLORS = range(3)
ONE: ColorVector = (Fraction(1), Fraction(1), Fraction(1))
BALANCE: ColorVector = (Fraction(1), Fraction(1), Fraction(-2))
U1: ColorVector = (Fraction(1), Fraction(-1), Fraction(0))
U2: ColorVector = (Fraction(1), Fraction(0), Fraction(-1))

PROTECTED_MATCHINGS = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}


@dataclass(frozen=True)
class Gadget:
    """One literal common-star gadget on a component pair."""

    u: int
    v: int
    color_u: int
    color_v: int
    center: Scalar
    leaf: Scalar


@dataclass(frozen=True)
class ExtraPhysicalEntry:
    """An off-family crossing entry used only by a scientific mutation."""

    u: int
    local_u: int
    v: int
    local_v: int
    color_u: int
    color_v: int
    weight: Scalar


def validate_common_star(k: int, gadgets: Sequence[Gadget]) -> None:
    """Check the declared simple, hollow, one-label, nonzero family."""

    if k < 1:
        raise ValueError("the component count must be positive")
    seen_pairs: set[tuple[int, int]] = set()
    for gadget in gadgets:
        if not (0 <= gadget.u < gadget.v < k):
            raise ValueError("gadget endpoints must satisfy 0 <= u < v < k")
        if gadget.color_u not in COLORS or gadget.color_v not in COLORS:
            raise ValueError("gadget endpoint colors must lie in {0,1,2}")
        if gadget.color_u == gadget.color_v:
            raise ValueError("common-star gadgets are hollow")
        if not gadget.center or not gadget.leaf:
            raise ValueError("both actual gadget factors must be nonzero")
        pair = (gadget.u, gadget.v)
        if pair in seen_pairs:
            raise ValueError("the component graph is simple and one-label")
        seen_pairs.add(pair)


def _add_symmetric(matrix: list[list[Scalar]], u: int, v: int, value: Scalar) -> None:
    matrix[u][v] += value
    matrix[v][u] += value


def hafnian(matrix: Sequence[Sequence[Scalar]], vertices: Iterable[int]) -> Scalar:
    """Exact recursive hafnian of a principal submatrix."""

    initial = tuple(vertices)

    @lru_cache(maxsize=None)
    def rec(active: tuple[int, ...]) -> Scalar:
        if not active:
            return Fraction(1)
        if len(active) % 2:
            return Fraction(0)
        u = active[0]
        answer = Fraction(0)
        for position in range(1, len(active)):
            v = active[position]
            weight = matrix[u][v]
            if weight:
                remaining = active[1:position] + active[position + 1 :]
                answer += weight * rec(remaining)
        return answer

    return rec(initial)


def literal_source(
    k: int,
    gadgets: Sequence[Gadget],
    word: Sequence[int],
    *,
    extra_entries: Sequence[ExtraPhysicalEntry] = (),
) -> Scalar:
    """Literal physical source for a word on all ``4*k`` vertices."""

    validate_common_star(k, gadgets)
    if len(word) != 4 * k or any(color not in COLORS for color in word):
        raise ValueError("a physical word must give one valid color per vertex")

    size = 4 * k
    matrix = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for component in range(k):
        offset = 4 * component
        for color, matching in PROTECTED_MATCHINGS.items():
            for local_u, local_v in matching:
                u, v = offset + local_u, offset + local_v
                if word[u] == color and word[v] == color:
                    _add_symmetric(matrix, u, v, Fraction(1))

    for gadget in gadgets:
        center_u, center_v = 4 * gadget.u, 4 * gadget.v
        if word[center_u] == gadget.color_u and word[center_v] == gadget.color_v:
            _add_symmetric(matrix, center_u, center_v, gadget.center)
        leaf_u = center_u + gadget.color_u + 1
        leaf_v = center_v + gadget.color_v + 1
        if word[leaf_u] == gadget.color_u and word[leaf_v] == gadget.color_v:
            _add_symmetric(matrix, leaf_u, leaf_v, gadget.leaf)

    for entry in extra_entries:
        if not (0 <= entry.u < entry.v < k):
            raise ValueError("extra-entry endpoints must satisfy 0 <= u < v < k")
        if not (0 <= entry.local_u < 4 and 0 <= entry.local_v < 4):
            raise ValueError("extra-entry local vertices must lie in {0,1,2,3}")
        u = 4 * entry.u + entry.local_u
        v = 4 * entry.v + entry.local_v
        if word[u] == entry.color_u and word[v] == entry.color_v:
            _add_symmetric(matrix, u, v, entry.weight)

    return hafnian(matrix, range(size))


def ab_physical_word(x: Sequence[int], y: Sequence[int]) -> ColorWord:
    if len(x) != len(y):
        raise ValueError("center and leaf words must have equal length")
    word: list[int] = []
    for center_color, leaf_color in zip(x, y):
        word.extend((center_color, leaf_color, leaf_color, leaf_color))
    return tuple(word)


def literal_ab_source(
    k: int,
    gadgets: Sequence[Gadget],
    x: Sequence[int],
    y: Sequence[int],
    *,
    extra_entries: Sequence[ExtraPhysicalEntry] = (),
) -> Scalar:
    return literal_source(
        k,
        gadgets,
        ab_physical_word(x, y),
        extra_entries=extra_entries,
    )


def compatible_factor_matrix(
    k: int,
    gadgets: Sequence[Gadget],
    colors: Sequence[int],
    factor: str,
) -> tuple[tuple[Scalar, ...], ...]:
    if len(colors) != k:
        raise ValueError("component coloring has the wrong length")
    if factor not in {"center", "leaf"}:
        raise ValueError("factor must be 'center' or 'leaf'")
    matrix = [[Fraction(0) for _ in range(k)] for _ in range(k)]
    for gadget in gadgets:
        if colors[gadget.u] == gadget.color_u and colors[gadget.v] == gadget.color_v:
            value = gadget.center if factor == "center" else gadget.leaf
            _add_symmetric(matrix, gadget.u, gadget.v, value)
    return tuple(tuple(row) for row in matrix)


def ab_hafnian_formula(
    k: int,
    gadgets: Sequence[Gadget],
    x: Sequence[int],
    y: Sequence[int],
) -> Scalar:
    """Common-set hafnian formula for a literal common-star AB word."""

    validate_common_star(k, gadgets)
    if len(x) != k or len(y) != k:
        raise ValueError("AB words must give one center/leaf color per component")
    center = compatible_factor_matrix(k, gadgets, x, "center")
    leaf = compatible_factor_matrix(k, gadgets, y, "leaf")
    answer = Fraction(0)
    for size in range(0, k + 1, 2):
        for active in combinations(range(k), size):
            if any(x[u] != y[u] for u in range(k) if u not in active):
                continue
            answer += hafnian(center, active) * hafnian(leaf, active)
    return answer


def color_words(k: int):
    return product(COLORS, repeat=k)


def exact_fixtures() -> dict[int, tuple[Gadget, ...]]:
    """Small asymmetric rational fixtures used by the primary replay."""

    return {
        2: (
            Gadget(0, 1, 0, 2, Fraction(2), Fraction(3)),
        ),
        3: (
            Gadget(0, 1, 0, 1, Fraction(2), Fraction(5)),
            Gadget(0, 2, 0, 1, Fraction(-3), Fraction(7)),
            Gadget(1, 2, 2, 0, Fraction(11), Fraction(-2)),
        ),
        4: (
            Gadget(0, 1, 0, 1, Fraction(2), Fraction(3)),
            Gadget(0, 2, 1, 2, Fraction(-3), Fraction(5)),
            Gadget(0, 3, 2, 0, Fraction(7), Fraction(-2)),
            Gadget(1, 2, 2, 0, Fraction(11), Fraction(13)),
            Gadget(1, 3, 0, 2, Fraction(-5), Fraction(17)),
            Gadget(2, 3, 1, 0, Fraction(19), Fraction(-7)),
        ),
    }


def compare_all_ab_words(k: int, gadgets: Sequence[Gadget]) -> int:
    words = list(color_words(k))
    checked = 0
    for x in words:
        for y in words:
            literal = literal_ab_source(k, gadgets, x, y)
            formula = ab_hafnian_formula(k, gadgets, x, y)
            if literal != formula:
                raise AssertionError(f"AB formula mismatch at x={x}, y={y}")
            checked += 1
    return checked


def k1_full_ghz_check() -> int:
    """The single protected K4 is a valid full-GHZ exception."""

    checked = 0
    for word in product(COLORS, repeat=4):
        target = Fraction(1) if len(set(word)) == 1 else Fraction(0)
        if literal_source(1, (), word) != target:
            raise AssertionError(f"k=1 target mismatch at {word}")
        checked += 1
    return checked


def diagonal_component_contraction(
    k: int, gadgets: Sequence[Gadget], covector: ColorVector = BALANCE
) -> Scalar:
    answer = Fraction(0)
    for word in color_words(k):
        coefficient = Fraction(1)
        for color in word:
            coefficient *= covector[color]
        answer += coefficient * ab_hafnian_formula(k, gadgets, word, word)
    return answer


def odd_target_closed_form(k: int, covector: ColorVector = BALANCE) -> Scalar:
    if k % 2 != 1:
        raise ValueError("the odd target formula is used only at odd k")
    return sum((entry**k for entry in covector), Fraction(0))


def dot(left: ColorVector, right: ColorVector) -> Scalar:
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def canonical_even_probes(
    k: int,
) -> tuple[tuple[tuple[ColorVector, ...], ...], tuple[tuple[ColorVector, ...], ...]]:
    if k < 2 or k % 2:
        raise ValueError("canonical even probes require even k >= 2")
    rows = []
    leaves = []
    for first in (U1, U2):
        rows.append((first, ONE, *((ONE,) * (k - 2))))
    for second in (U1, U2):
        leaves.append((ONE, second, *((BALANCE,) * (k - 2))))
    return tuple(rows), tuple(leaves)


def validate_cross_orthogonality(
    row_systems: Sequence[Sequence[ColorVector]],
    leaf_systems: Sequence[Sequence[ColorVector]],
) -> int:
    if len(row_systems) != 2 or len(leaf_systems) != 2:
        raise ValueError("the rank test requires two row and two leaf probes")
    k = len(row_systems[0])
    if k < 2 or any(len(system) != k for system in (*row_systems, *leaf_systems)):
        raise ValueError("all probe systems must have the same component count")
    checked = 0
    for p, q, component in product(range(2), range(2), range(k)):
        if dot(row_systems[p][component], leaf_systems[q][component]) != 0:
            raise ValueError(
                "all four crossed probe pairs must be locally orthogonal; "
                f"failure at p={p}, q={q}, component={component}"
            )
        checked += 1
    return checked


def contract_ab_formula(
    k: int,
    gadgets: Sequence[Gadget],
    row_system: Sequence[ColorVector],
    leaf_system: Sequence[ColorVector],
) -> Scalar:
    answer = Fraction(0)
    words = list(color_words(k))
    row_coefficients = {}
    leaf_coefficients = {}
    for x in words:
        coefficient = Fraction(1)
        for component, color in enumerate(x):
            coefficient *= row_system[component][color]
        row_coefficients[x] = coefficient
    for y in words:
        coefficient = Fraction(1)
        for component, color in enumerate(y):
            coefficient *= leaf_system[component][color]
        leaf_coefficients[y] = coefficient
    for x in words:
        for y in words:
            answer += (
                row_coefficients[x]
                * leaf_coefficients[y]
                * ab_hafnian_formula(k, gadgets, x, y)
            )
    return answer


def full_layer_contraction(
    k: int,
    gadgets: Sequence[Gadget],
    systems: Sequence[Sequence[ColorVector]],
    factor: str,
) -> tuple[Scalar, Scalar]:
    answer = []
    for system in systems:
        contraction = Fraction(0)
        for word in color_words(k):
            coefficient = Fraction(1)
            for component, color in enumerate(word):
                coefficient *= system[component][color]
            matrix = compatible_factor_matrix(k, gadgets, word, factor)
            contraction += coefficient * hafnian(matrix, range(k))
        answer.append(contraction)
    return answer[0], answer[1]


def determinant_2x2(matrix: Sequence[Sequence[Scalar]]) -> Scalar:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def target_probe_matrix(
    row_systems: Sequence[Sequence[ColorVector]],
    leaf_systems: Sequence[Sequence[ColorVector]],
) -> tuple[tuple[Scalar, Scalar], tuple[Scalar, Scalar]]:
    """Contract the constant-word target against the supplied four probes."""

    if len(row_systems) != 2 or len(leaf_systems) != 2:
        raise ValueError("the target matrix requires two row and two leaf probes")
    k = len(row_systems[0])
    if k < 1 or any(len(system) != k for system in (*row_systems, *leaf_systems)):
        raise ValueError("all target probe systems must have the same component count")
    matrix = []
    for p in range(2):
        row = []
        for q in range(2):
            value = Fraction(0)
            for color in COLORS:
                term = Fraction(1)
                for component in range(k):
                    term *= (
                        row_systems[p][component][color]
                        * leaf_systems[q][component][color]
                    )
                value += term
            row.append(value)
        matrix.append(tuple(row))
    return tuple(matrix)  # type: ignore[return-value]


def even_target_probe_matrix(k: int) -> tuple[tuple[Scalar, Scalar], tuple[Scalar, Scalar]]:
    """Canonical even-probe target matrix used in the closed-form proof."""

    rows, leaves = canonical_even_probes(k)
    return target_probe_matrix(rows, leaves)


def even_target_closed_form(k: int) -> dict[str, object]:
    if k < 2 or k % 2:
        raise ValueError("the even target formula requires even k >= 2")
    matrix = ((Fraction(2), Fraction(1)), (Fraction(1), Fraction(1 + 2 ** (k - 2))))
    return {"matrix": matrix, "determinant": Fraction(1 + 2 ** (k - 1))}


def even_probe_certificate(
    k: int,
    gadgets: Sequence[Gadget],
    *,
    row_systems: Sequence[Sequence[ColorVector]] | None = None,
    leaf_systems: Sequence[Sequence[ColorVector]] | None = None,
    require_orthogonality: bool = True,
) -> dict[str, object]:
    """Replay the four contractions and their active full-layer factorization."""

    validate_common_star(k, gadgets)
    if row_systems is None or leaf_systems is None:
        canonical_rows, canonical_leaves = canonical_even_probes(k)
        row_systems = canonical_rows if row_systems is None else row_systems
        leaf_systems = canonical_leaves if leaf_systems is None else leaf_systems
    if require_orthogonality:
        validate_cross_orthogonality(row_systems, leaf_systems)

    source = tuple(
        tuple(
            contract_ab_formula(k, gadgets, row_systems[p], leaf_systems[q])
            for q in range(2)
        )
        for p in range(2)
    )
    center = full_layer_contraction(k, gadgets, row_systems, "center")
    leaf = full_layer_contraction(k, gadgets, leaf_systems, "leaf")
    outer = tuple(tuple(center[p] * leaf[q] for q in range(2)) for p in range(2))
    target = target_probe_matrix(row_systems, leaf_systems)
    return {
        "source": source,
        "outer": outer,
        "source_determinant": determinant_2x2(source),
        "target": target,
        "target_determinant": determinant_2x2(target),
        "orthogonality_checked": require_orthogonality,
    }


def off_family_center_leaf_mutation() -> dict[str, object]:
    """One center-to-leaf entry invalidates the common-set formula."""

    gadgets = exact_fixtures()[3]
    extra = ExtraPhysicalEntry(
        u=0,
        local_u=0,
        v=1,
        local_v=1,  # the color-0 leaf at component 1
        color_u=2,
        color_v=0,
        weight=Fraction(13),
    )
    x = (2, 2, 0)
    y = (0, 0, 1)
    formula = ab_hafnian_formula(3, gadgets, x, y)
    literal = literal_ab_source(3, gadgets, x, y, extra_entries=(extra,))
    return {"x": x, "y": y, "formula": formula, "literal": literal}


def run_primary_replay() -> dict[str, object]:
    fixtures = exact_fixtures()
    words_checked = sum(compare_all_ab_words(k, fixtures[k]) for k in (2, 3))
    k1_checked = k1_full_ghz_check()

    odd_source = diagonal_component_contraction(3, fixtures[3])
    odd_target = odd_target_closed_form(3)
    if odd_source != 0 or odd_target == 0:
        raise AssertionError("odd component-word contraction did not separate source and target")

    even_receipts = {}
    for k in (2, 4):
        receipt = even_probe_certificate(k, fixtures[k])
        expected = even_target_closed_form(k)
        if receipt["source"] != receipt["outer"]:
            raise AssertionError(f"proper crossing layers survived at k={k}")
        if receipt["source_determinant"] != 0:
            raise AssertionError(f"source contractions did not have rank <= 1 at k={k}")
        if receipt["target"] != expected["matrix"]:
            raise AssertionError(f"target probe matrix mismatch at k={k}")
        if receipt["target_determinant"] != expected["determinant"]:
            raise AssertionError(f"target determinant mismatch at k={k}")
        even_receipts[k] = receipt

    for k in range(2, 22, 2):
        expected = even_target_closed_form(k)
        if determinant_2x2(expected["matrix"]) != expected["determinant"]:
            raise AssertionError(f"closed-form determinant mismatch at k={k}")

    mutation = off_family_center_leaf_mutation()
    if mutation["literal"] == mutation["formula"]:
        raise AssertionError("off-family center-to-leaf mutation escaped detection")

    return {
        "ab_words_checked": words_checked,
        "k1_full_words_checked": k1_checked,
        "odd_k3_source_contraction": odd_source,
        "odd_k3_target_contraction": odd_target,
        "even_component_counts_checked": tuple(even_receipts),
        "even_closed_forms_checked": 10,
        "off_family_mutation_detected": True,
        "status": "ODD_COMPONENT_TARGET_AND_EVEN_CSFULL_EXCLUSION_REPLAY",
    }


def main() -> None:
    receipt = run_primary_replay()
    print(f"literal AB words checked exactly: {receipt['ab_words_checked']}")
    print(f"k=1 full physical words checked exactly: {receipt['k1_full_words_checked']}")
    print("odd component-word zero-sum contraction: PASS")
    print("even k=2,4 crossed-orthogonal source outer product: PASS")
    print("even target determinant 1+2^(k-1), k=2,...,20: PASS")
    print("scientific off-family mutation detection: PASS")
    print("scope: odd component targets; even CSFULL AB words; not even CSQ4 or FB")


if __name__ == "__main__":
    main()
