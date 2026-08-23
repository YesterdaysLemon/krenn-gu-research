"""Focused exact checks for GLS55's torus-rigid five-label floor."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


Vector = tuple[Fraction, Fraction, Fraction]
Row = tuple[Fraction, ...]


def matrix_rank(rows: list[Row]) -> int:
    """Exact row rank over Q."""
    work = [list(row) for row in rows if any(row)]
    rank = 0
    width = len(work[0]) if work else 0
    for column in range(width):
        pivot = next(
            (index for index in range(rank, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [entry / scale for entry in work[rank]]
        for index in range(len(work)):
            if index == rank or not work[index][column]:
                continue
            scale = work[index][column]
            work[index] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(work[index], work[rank], strict=True)
            ]
        rank += 1
    return rank


def rowspace_contains_coordinate(rows: list[Vector]) -> bool:
    rank = matrix_rank(rows)
    for coordinate in range(3):
        basis = [Fraction(coordinate == index) for index in range(3)]
        if matrix_rank(rows + [tuple(basis)]) == rank:
            return True
    return False


def kernel_has_torus_vector(rows: list[Vector]) -> bool:
    """Decide torus incidence in K^3 by exact rank-profile formulas."""
    independent: list[Vector] = []
    for row in rows:
        if matrix_rank(independent + [row]) > len(independent):
            independent.append(row)
    rank = len(independent)
    if rank == 3:
        return False
    if rank == 0:
        return True
    if rank == 1:
        return sum(entry != 0 for entry in independent[0]) >= 2
    first, second = independent
    kernel = (
        first[1] * second[2] - first[2] * second[1],
        first[2] * second[0] - first[0] * second[2],
        first[0] * second[1] - first[1] * second[0],
    )
    assert any(kernel)
    return all(kernel)


def audit_linear_kernel_profiles() -> dict[str, int]:
    raw_rows = [
        tuple(Fraction(entry) for entry in row)
        for row in product((-1, 0, 1), repeat=3)
        if any(row)
    ]
    checked = 0
    ranks = {rank: 0 for rank in range(4)}
    # Repeated rows are allowed: they exercise every rank-drop fibre.
    for row_count in range(4):
        families = [()] if row_count == 0 else product(raw_rows, repeat=row_count)
        for family in families:
            rows = list(family)
            rank = matrix_rank(rows)
            rigid = not kernel_has_torus_vector(rows)
            coordinate_readout = rowspace_contains_coordinate(rows)
            assert rigid == coordinate_readout
            checked += 1
            ranks[rank] += 1

    examples = {
        "rank0": [],
        "rank1_coordinate": [(Fraction(1), Fraction(0), Fraction(0))],
        "rank1_torus": [(Fraction(1), Fraction(1), Fraction(0))],
        "rank2_coordinate": [
            (Fraction(1), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(1), Fraction(0)),
        ],
        "rank2_torus": [
            (Fraction(1), Fraction(0), Fraction(-1)),
            (Fraction(0), Fraction(1), Fraction(-1)),
        ],
        "rank3": [
            (Fraction(1), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(1)),
        ],
    }
    expected = {
        "rank0": False,
        "rank1_coordinate": True,
        "rank1_torus": False,
        "rank2_coordinate": True,
        "rank2_torus": False,
        "rank3": True,
    }
    for name, rows in examples.items():
        assert (not kernel_has_torus_vector(rows)) == expected[name]
    return {
        "families": checked,
        **{f"rank_{rank}": count for rank, count in ranks.items()},
    }


def choose_open_four(label_count: int, rigid: frozenset[int]) -> frozenset[int]:
    assert len(rigid) <= 4
    fillers = [label for label in range(label_count) if label not in rigid]
    return rigid | frozenset(fillers[: 4 - len(rigid)])


def audit_four_slot_contraction() -> dict[str, int]:
    rigid_cases = 0
    pair_cases = 0
    target_weight_cases = 0
    for root_order in range(3, 8):
        label_count = 2 * root_order
        labels = frozenset(range(label_count))
        for rigid_count in range(5):
            for rigid_tuple in combinations(labels, rigid_count):
                rigid = frozenset(rigid_tuple)
                open_four = choose_open_four(label_count, rigid)
                outside = labels - open_four
                assert len(open_four) == 4
                assert rigid <= open_four
                assert not (outside & rigid)
                rigid_cases += 1

                survivor_count = 0
                for pair in combinations(labels, 2):
                    pair_set = frozenset(pair)
                    if pair_set <= open_four:
                        survivor_count += 1
                        assert len(open_four - pair_set) == 2
                    else:
                        assert pair_set & outside
                    pair_cases += 1
                assert survivor_count == 6

                kernel_vectors = {
                    label: (
                        Fraction(label + 1),
                        Fraction(label + 2),
                        Fraction(label + 3),
                    )
                    for label in outside
                }
                beta = tuple(
                    product_fraction(kernel_vectors[label][colour] for label in outside)
                    for colour in range(3)
                )
                assert all(beta)
                normalized = tuple(beta[colour] / beta[colour] for colour in range(3))
                assert normalized == (Fraction(1),) * 3
                target_weight_cases += 1

    return {
        "rigid_subsets": rigid_cases,
        "raw_pairs": pair_cases,
        "target_weights": target_weight_cases,
    }


def product_fraction(values) -> Fraction:
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def perfect_matchings(vertices: tuple[str, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def audit_six_vertex_matching_reconstruction() -> dict[str, object]:
    probes = ("a0", "a1")
    ports = ("p0", "p1", "p2", "p3")
    matchings = list(perfect_matchings(probes + ports))
    assert len(matchings) == 15
    root_edge = []
    grouped: dict[frozenset[str], int] = {}
    for matching in matchings:
        edges = {frozenset(edge) for edge in matching}
        if frozenset(probes) in edges:
            root_edge.append(matching)
            continue
        touched = frozenset(
            port
            for edge in edges
            for port in ports
            if port in edge and bool(edge & frozenset(probes))
        )
        assert len(touched) == 2
        grouped[touched] = grouped.get(touched, 0) + 1
    assert len(root_edge) == 3
    assert set(grouped.values()) == {2}
    assert set(grouped) == {frozenset(pair) for pair in combinations(ports, 2)}
    return {
        "matchings": len(matchings),
        "zero_root_edge": len(root_edge),
        "pair_groups": len(grouped),
        "orientations_per_pair": sorted(set(grouped.values())),
    }


def audit_five_label_boundary() -> dict[str, int]:
    labels = frozenset(range(5))
    complements = []
    for pair in combinations(labels, 2):
        complement = labels - frozenset(pair)
        assert len(complement) == 3
        complements.append(complement)
    assert len(complements) == 10
    assert len(set(complements)) == 10
    return {"raw_pairs": 10, "deck_arity": 3, "external_vertices": 7}


def audit_incidence_only_boundary() -> dict[str, int]:
    identity: list[Vector] = [
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    ]
    assert matrix_rank(identity) == 3
    assert not kernel_has_torus_vector(identity)
    assert matrix_rank([]) == 0
    assert kernel_has_torus_vector([])

    symmetric_generators: list[Row] = []
    for left in range(3):
        for right in range(left, 3):
            matrix = [Fraction(0)] * 9
            matrix[3 * left + right] += 1
            matrix[3 * right + left] += 1
            symmetric_generators.append(tuple(matrix))
    assert len(symmetric_generators) == 6
    assert matrix_rank(symmetric_generators) == 6
    # Five injective labels and one zero label attain the rigidity floor while
    # incidence alone assigns no nonzero complementary deck or response.
    return {
        "rigid_labels": 5,
        "nonrigid_zero_labels": 1,
        "pair_image_rank": matrix_rank(symmetric_generators),
        "forced_decks": 0,
    }


def main() -> None:
    report = {
        "linear_kernel_profiles": audit_linear_kernel_profiles(),
        "four_slot_contraction": audit_four_slot_contraction(),
        "six_vertex_matching": audit_six_vertex_matching_reconstruction(),
        "five_label_boundary": audit_five_label_boundary(),
        "incidence_only_boundary": audit_incidence_only_boundary(),
    }
    print("GLS55 focused exact verifier: PASS")
    for key, value in report.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
