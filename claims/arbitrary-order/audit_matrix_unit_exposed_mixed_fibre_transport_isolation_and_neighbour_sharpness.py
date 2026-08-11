"""Independent no-import audit of exposed-fibre isolation and sharpness."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations

Edge = tuple[int, int]
Monomial = tuple[Fraction, int]

# Each row is (left, right, decimal label code, coefficient, t exponent, balance).
# This packed table is independently encoded and imports no repository module.
ROWS = (
    (0, 1, 0, 1, 0, 1),
    (0, 2, 0, 1, 0, 1),
    (0, 3, 0, 1, 0, 4),
    (0, 4, 0, 1, 0, 1),
    (0, 5, 12, 1, 0, 6),
    (0, 6, 11, 1, 2, 1),
    (0, 7, 22, 1, 0, 7),
    (1, 2, 1, -1, 0, 4),
    (1, 3, 0, 1, 0, 1),
    (1, 4, 10, -1, 0, 3),
    (1, 5, 11, 1, 0, 4),
    (1, 6, 22, 1, 0, 7),
    (1, 7, 0, 1, 0, 1),
    (2, 3, 11, 1, 0, 3),
    (2, 4, 1, -1, -1, 2),
    (2, 5, 22, 1, 0, 1),
    (2, 6, 0, 1, 0, 4),
    (2, 7, 20, 1, 0, 6),
    (3, 4, 22, 1, 0, 7),
    (3, 5, 1, 1, 1, 2),
    (3, 6, 10, 1, 0, 3),
    (3, 7, 11, 1, 0, 1),
    (4, 5, 0, 1, 0, 3),
    (4, 6, 11, 1, 0, 1),
    (4, 7, 11, 1, -2, 4),
    (5, 6, 1, 1, 0, 4),
    (5, 7, 11, 1, 0, 1),
    (6, 7, 11, 1, 0, 1),
)


def unpack(code: int) -> tuple[int, int]:
    """Decode one decimal endpoint-label pair."""
    return divmod(code, 10)


def pack_word(digits: tuple[int, ...]) -> int:
    """Pack a ternary word with vertex zero least significant."""
    return sum(digit * 3**vertex for vertex, digit in enumerate(digits))


def row_maps():
    """Build independent edge, label, Laurent-weight, and balance maps."""
    labels = {}
    weights = {}
    balances = {}
    for left, right, code, coefficient, exponent, balance in ROWS:
        edge = (left, right)
        labels[edge] = unpack(code)
        weights[edge] = (Fraction(coefficient), exponent)
        balances[edge] = Fraction(balance)
    return labels, weights, balances


def edge_bits() -> dict[Edge, int]:
    """Give every physical edge an independent bit."""
    return {edge: 1 << index for index, edge in enumerate(combinations(range(8), 2))}


def matching_bits(edges: tuple[Edge, ...]) -> int:
    """Pack a matching as a 28-bit set."""
    bits = edge_bits()
    return sum(bits[edge] for edge in edges)


def multiply(left: Monomial, right: Monomial) -> Monomial:
    """Multiply Laurent monomials."""
    return left[0] * right[0], left[1] + right[1]


def matching_weight(edges: tuple[Edge, ...], weights: dict[Edge, Monomial]) -> Monomial:
    """Multiply independently encoded edge weights."""
    result = (Fraction(1), 0)
    for edge in edges:
        result = multiply(result, weights[edge])
    return result


def enumerate_fibres():
    """Traverse matchings by least-set-bit deletion and pack word fibres."""
    labels, weights, _ = row_maps()
    bits = edge_bits()
    fibres: dict[int, list[tuple[int, Monomial, bool]]] = defaultdict(list)

    def visit(
        mask: int,
        word: list[int],
        scalar: Monomial,
        diagonal: bool,
        selected: int,
    ) -> None:
        if not mask:
            fibres[pack_word(tuple(word))].append((selected, scalar, diagonal))
            return
        low = mask & -mask
        left = low.bit_length() - 1
        remainder = mask ^ low
        partners = remainder
        while partners:
            partner_bit = partners & -partners
            right = partner_bit.bit_length() - 1
            partners ^= partner_bit
            edge = (left, right)
            left_label, right_label = labels[edge]
            next_word = word[:]
            next_word[left] = left_label
            next_word[right] = right_label
            visit(
                remainder ^ partner_bit,
                next_word,
                multiply(scalar, weights[edge]),
                diagonal and left_label == right_label,
                selected | bits[edge],
            )

    visit((1 << 8) - 1, [-1] * 8, (Fraction(1), 0), True, 0)
    return fibres


def polynomial(records: list[tuple[int, Monomial, bool]]) -> dict[int, Fraction]:
    """Collect a sparse Laurent coefficient from fibre records."""
    result: dict[int, Fraction] = {}
    for _, (coefficient, exponent), _ in records:
        result[exponent] = result.get(exponent, Fraction(0)) + coefficient
        if not result[exponent]:
            del result[exponent]
    return result


def audit_support_and_balance() -> dict[str, object]:
    """Check completeness, nonvanishing, and the fixed strict balance."""
    labels, weights, balances = row_maps()
    assert set(labels) == set(combinations(range(8), 2))
    assert len(labels) == 28
    assert all(coefficient for coefficient, _ in weights.values())
    assert all(value > 0 for value in balances.values())

    loads = [[[Fraction(0) for _ in range(3)] for _ in range(8)]][0]
    for edge, value in balances.items():
        left, right = edge
        left_label, right_label = labels[edge]
        loads[left][left_label] += value
        loads[right][right_label] += value
    assert tuple(tuple(row) for row in loads) == ((Fraction(7),) * 3,) * 8
    return {"physical_pairs": 28, "strict_common_load": 7, "parameter_nonzero": True}


def audit_fibres() -> dict[str, object]:
    """Audit the four selected zero fibres and the exposed monomial."""
    fibres = enumerate_fibres()
    assert sum(map(len, fibres.values())) == 105
    assert len(fibres) == 101

    cycle_words = (
        (0, 0, 0, 0, 1, 1, 1, 1),
        (0, 0, 1, 1, 0, 0, 1, 1),
        (0, 1, 0, 1, 0, 1, 0, 1),
    )
    eta = (0, 0, 0, 0, 0, 1, 0, 0)
    nu = (0, 2, 0, 0, 1, 1, 2, 1)
    zero_codes = {code for code, records in fibres.items() if not polynomial(records)}
    assert zero_codes == {pack_word(word) for word in cycle_words + (nu,)}

    eta_records = fibres[pack_word(eta)]
    assert eta_records == [
        (matching_bits(((0, 4), (1, 7), (2, 6), (3, 5))), (Fraction(1), 1), False)
    ]

    nu_records = fibres[pack_word(nu)]
    assert nu_records == [
        (
            matching_bits(((0, 2), (1, 6), (3, 5), (4, 7))),
            (Fraction(1), -1),
            False,
        ),
        (
            matching_bits(((0, 3), (1, 6), (2, 4), (5, 7))),
            (Fraction(-1), -1),
            False,
        ),
    ]
    assert all(not record[2] for record in nu_records)
    assert tuple(eta.count(colour) for colour in range(3)) == (7, 1, 0)
    assert tuple(nu.count(colour) for colour in range(3)) == (3, 3, 2)
    assert {
        tuple(word.count(colour) for colour in range(3)) for word in cycle_words
    } == {(4, 4, 0)}

    pure_values = []
    for colour in range(3):
        records = fibres[pack_word((colour,) * 8)]
        assert len(records) == 1 and records[0][2]
        pure_values.append(polynomial(records))
    assert pure_values == [{0: Fraction(1)}] * 3

    return {
        "perfect_matchings": 105,
        "induced_words": 101,
        "zero_mixed_fibres": 4,
        "exposed_equation": "t=0",
        "neighbour_equation": "t^-1-t^-1=0",
        "transport_multidegrees": ((4, 4, 0), (7, 1, 0), (3, 3, 2)),
    }


def audit_holonomy_and_sample() -> dict[str, object]:
    """Reassemble H independently and evaluate a nontrivial family point."""
    _, weights, _ = row_maps()
    bridges = (
        ((2, 3), (4, 5)),
        ((1, 5), (2, 6)),
        ((4, 6), (1, 3)),
    )
    crosses = (
        ((2, 4), (3, 5)),
        ((1, 2), (5, 6)),
        ((1, 4), (3, 6)),
    )
    numerator = (Fraction(1), 0)
    denominator = (Fraction(1), 0)
    circulation: Counter[Edge] = Counter()
    for bridge, cross in zip(bridges, crosses):
        numerator = multiply(numerator, matching_weight(bridge, weights))
        denominator = multiply(denominator, matching_weight(cross, weights))
        circulation.update(bridge)
        circulation.subtract(cross)
    holonomy = (
        numerator[0] / denominator[0],
        numerator[1] - denominator[1],
    )
    assert holonomy == (Fraction(-1), 0)
    assert set(circulation.values()) == {-1, 1}
    assert len(circulation) == 12

    parameter = Fraction(3)
    evaluated = {
        edge: coefficient * parameter**exponent
        for edge, (coefficient, exponent) in weights.items()
    }
    assert all(evaluated.values())
    assert evaluated[(3, 5)] == 3
    assert evaluated[(2, 4)] == Fraction(-1, 3)
    assert evaluated[(4, 7)] == Fraction(1, 9)
    assert evaluated[(0, 6)] == 9
    return {
        "holonomy": -1,
        "circulation_support": 12,
        "independent_parameter_sample": parameter,
        "exposed_coefficient": parameter,
    }


def main() -> None:
    """Run the independent audit and print a compact summary."""
    support = audit_support_and_balance()
    fibres = audit_fibres()
    holonomy = audit_holonomy_and_sample()
    print("independent exposed-fibre isolation audit: PASS")
    print(f"  packed support/balance: {support}")
    print(f"  least-bit Laurent fibre census: {fibres}")
    print(f"  independent holonomy/family sample: {holonomy}")


if __name__ == "__main__":
    main()
