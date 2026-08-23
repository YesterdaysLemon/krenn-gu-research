"""Independent no-import audit for GLS55.

This file deliberately uses only the standard library, bit masks, modular
subspace sets, and a reverse perfect-matching traversal.
"""

from itertools import combinations


PRIME = 5
WEIGHT_PRIME = 101


def inverse(value: int, prime: int = PRIME) -> int:
    return pow(value % prime, prime - 2, prime)


def dot(left: tuple[int, ...], right: tuple[int, ...], prime: int = PRIME) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True)) % prime


def normalized_projective(vector: tuple[int, int, int]) -> tuple[int, int, int]:
    for value in vector:
        if value % PRIME:
            scale = inverse(value)
            return tuple((scale * entry) % PRIME for entry in vector)
    raise ValueError("zero vector has no projective normalization")


def all_vectors(prime: int = PRIME):
    for packed in range(prime**3):
        value = packed
        entries = []
        for _ in range(3):
            entries.append(value % prime)
            value //= prime
        yield tuple(entries)


def complete_subspace_census() -> dict[str, int]:
    vectors = tuple(all_vectors())
    zero = frozenset({(0, 0, 0)})
    full = frozenset(vectors)

    projective = {
        normalized_projective(vector) for vector in vectors if vector != (0, 0, 0)
    }
    assert len(projective) == 31

    lines = {
        frozenset(
            tuple((scale * entry) % PRIME for entry in generator)
            for scale in range(PRIME)
        )
        for generator in projective
    }
    planes = {
        frozenset(vector for vector in vectors if dot(normal, vector) == 0)
        for normal in projective
    }
    subspaces = {zero, full, *lines, *planes}
    assert len(subspaces) == 64

    units = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    torus = tuple(vector for vector in vectors if all(vector))
    dimension_counts = {0: 0, 1: 0, 2: 0, 3: 0}
    rigid_count = 0

    for rowspace in subspaces:
        size_to_dimension = {1: 0, 5: 1, 25: 2, 125: 3}
        dimension_counts[size_to_dimension[len(rowspace)]] += 1

        kernel_has_torus = any(
            all(dot(row, vector) == 0 for row in rowspace) for vector in torus
        )
        contains_coordinate = any(unit in rowspace for unit in units)
        assert (not kernel_has_torus) == contains_coordinate
        rigid_count += contains_coordinate

    return {
        "subspaces": len(subspaces),
        "projective_lines": len(lines),
        "projective_planes": len(planes),
        "rigid_rowspaces": rigid_count,
        **{
            f"dimension_{dimension}": count
            for dimension, count in dimension_counts.items()
        },
    }


def bit_count(mask: int) -> int:
    return mask.bit_count()


def lowest_bits(mask: int, count: int) -> int:
    chosen = 0
    while count:
        bit = mask & -mask
        assert bit
        chosen |= bit
        mask ^= bit
        count -= 1
    return chosen


def audit_contraction_masks() -> dict[str, int]:
    rigid_cases = 0
    killed_pairs = 0
    live_pairs = 0
    weight_checks = 0
    for root_order in range(3, 7):
        label_count = 2 * root_order
        universe = (1 << label_count) - 1
        for rigid_count in range(5):
            for rigid_labels in combinations(range(label_count), rigid_count):
                rigid_mask = sum(1 << label for label in rigid_labels)
                nonrigid_mask = universe ^ rigid_mask
                open_mask = rigid_mask | lowest_bits(nonrigid_mask, 4 - rigid_count)
                outside_mask = universe ^ open_mask
                assert bit_count(open_mask) == 4
                assert rigid_mask & outside_mask == 0
                rigid_cases += 1

                survivors = 0
                for left, right in combinations(range(label_count), 2):
                    pair_mask = (1 << left) | (1 << right)
                    if pair_mask & outside_mask:
                        assert pair_mask & nonrigid_mask
                        killed_pairs += 1
                    else:
                        assert pair_mask & open_mask == pair_mask
                        assert bit_count(open_mask ^ pair_mask) == 2
                        live_pairs += 1
                        survivors += 1
                assert survivors == 6

                weights = [1, 1, 1]
                for label in range(label_count):
                    if not (outside_mask & (1 << label)):
                        continue
                    kernel_vector = (label + 1, label + 2, label + 3)
                    assert all(value % WEIGHT_PRIME for value in kernel_vector)
                    for colour in range(3):
                        weights[colour] *= kernel_vector[colour]
                        weights[colour] %= WEIGHT_PRIME
                assert all(weights)
                assert [
                    value * pow(value, -1, WEIGHT_PRIME) % WEIGHT_PRIME
                    for value in weights
                ] == [1, 1, 1]
                weight_checks += 1
    return {
        "rigid_masks": rigid_cases,
        "killed_pairs": killed_pairs,
        "live_pairs": live_pairs,
        "weight_checks": weight_checks,
    }


def reverse_matchings(mask: int):
    if mask == 0:
        yield ()
        return
    first = mask.bit_length() - 1
    without_first = mask ^ (1 << first)
    partners = without_first
    while partners:
        partner_bit = partners & -partners
        partner = partner_bit.bit_length() - 1
        remainder = without_first ^ partner_bit
        for tail in reverse_matchings(remainder):
            yield ((first, partner),) + tail
        partners ^= partner_bit


def audit_reverse_matching_partition() -> dict[str, int]:
    # vertices 0,1 are probes; vertices 2..5 are the four open labels.
    matchings = list(reverse_matchings((1 << 6) - 1))
    assert len(matchings) == 15
    zero_anchor = 0
    orientation_counts: dict[int, int] = {}
    for matching in matchings:
        edge_masks = {(1 << left) | (1 << right) for left, right in matching}
        if 0b11 in edge_masks:
            zero_anchor += 1
            continue
        touched = 0
        for edge_mask in edge_masks:
            if edge_mask & 0b11:
                touched |= edge_mask & 0b111100
        assert bit_count(touched) == 2
        orientation_counts[touched] = orientation_counts.get(touched, 0) + 1
    assert zero_anchor == 3
    assert len(orientation_counts) == 6
    assert set(orientation_counts.values()) == {2}
    return {
        "matchings": len(matchings),
        "zero_anchor": zero_anchor,
        "companion_pairs": len(orientation_counts),
        "oriented_terms": sum(orientation_counts.values()),
    }


def audit_arity_boundary() -> dict[str, int]:
    five_mask = 0b11111
    complements = set()
    for left, right in combinations(range(5), 2):
        complement = five_mask ^ (1 << left) ^ (1 << right)
        assert bit_count(complement) == 3
        complements.add(complement)
    assert len(complements) == 10
    assert not list(reverse_matchings((1 << 7) - 1))
    return {"trilinear_decks": len(complements), "odd_external_matchings": 0}


def main() -> None:
    reports = {
        "complete_f5_subspace_census": complete_subspace_census(),
        "contraction_masks": audit_contraction_masks(),
        "reverse_matching_partition": audit_reverse_matching_partition(),
        "five_label_arity_boundary": audit_arity_boundary(),
    }
    print("GLS55 independent no-import audit: PASS")
    for name, report in reports.items():
        print(f"  {name}: {report}")


if __name__ == "__main__":
    main()
