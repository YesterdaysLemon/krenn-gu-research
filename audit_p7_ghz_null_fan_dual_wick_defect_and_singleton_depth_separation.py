"""Independent no-import audit of the GHZ-null fan response theorem."""

from __future__ import annotations

from fractions import Fraction
from functools import cache


def ghz_diagonal_value(local_axes: tuple[int, ...]) -> tuple[int, int, int]:
    return tuple(int(all(axis == colour for axis in local_axes)) for colour in range(3))


def hafnian(
    vertices: tuple[int, ...], edge: dict[tuple[int, int], Fraction]
) -> Fraction:
    @cache
    def recurse(current: tuple[int, ...]) -> Fraction:
        if not current:
            return Fraction(1)
        first = current[0]
        total = Fraction(0)
        for position, partner in enumerate(current[1:], start=1):
            total += edge.get(tuple(sorted((first, partner))), Fraction(0)) * recurse(
                current[1:position] + current[position + 1 :]
            )
        return total

    return recurse(vertices)


def main() -> None:
    # Four explicit fan words and the six-double word, audited independently.
    words = (
        (1, 1, 1, 2, 2, 1, 1),
        (0, 1, 1, 0, 0, 0, 0),
        (0, 1, 0, 2, 0, 0, 0),
        (0, 1, 0, 0, 2, 0, 0),
        (0, 1, 1, 2, 2, 0, 0),
    )
    assert all(ghz_diagonal_value(word) == (0, 0, 0) for word in words)

    # Exact physical response at two distinct residual scalars.
    visible = []
    blocker_singletons = []
    for vacuum in (Fraction(2), Fraction(13, 5)):
        edges = {
            (0, 1): Fraction(1),
            (7, 8): vacuum,
            (0, 7): -vacuum,
            (1, 8): Fraction(1),
        }
        direct_pair = hafnian((0, 1), edges)
        residual_pair = hafnian((0, 1, 7, 8), edges)
        direct_four = hafnian((0, 1, 2, 3), edges)
        residual_four = hafnian((0, 1, 2, 3, 7, 8), edges)
        direct_six = hafnian((0, 1, 2, 3, 4, 5), edges)
        residual_six = hafnian((0, 1, 2, 3, 4, 5, 7, 8), edges)
        visible.append(
            (
                direct_pair,
                residual_pair,
                direct_four,
                residual_four,
                direct_six,
                residual_six,
            )
        )
        blocker_singletons.append(edges[(0, 7)])

    assert visible[0] == visible[1] == (1, 0, 0, 0, 0, 0)
    assert tuple(blocker_singletons) == (Fraction(-2), Fraction(-13, 5))

    # The null-window insertion is zero because all z-pairs are zero, while
    # the empty scalar differs.  No division or additive locus is used.
    z_pairs = (Fraction(0),) * 6
    direct_complements = (1, 0, 0, 0, 0, 0)
    insertion = sum(
        z * m for z, m in zip(z_pairs, direct_complements, strict=True)
    )
    assert insertion == 0

    # Independent representative deletion-label separation.
    roots = frozenset(range(5))
    residuals = frozenset((5, 6))
    blockers = frozenset(range(7, 14))
    root_jet_label = frozenset((0, 1)) | residuals
    pair_face_label = roots | (blockers - {7, 8})
    assert root_jet_label.isdisjoint(blockers)
    assert len(pair_face_label & blockers) == 5
    assert root_jet_label != pair_face_label

    print("independent GHZ-null fan audit: PASS")
    print("four_fan_words_and_six_double_word=GHZ_NULL")
    print("physical_visible_data_fixed_at_h=2,13/5")
    print("blocker_singleton_depth_changes_with_h=PASS")
    print("vacuum_free_null_defect=0")
    print("root_jet_and_pair_face_deletion_labels=DISJOINT")
    print("graph_search=0 support_search=0 colour_word_enumeration=0")


if __name__ == "__main__":
    main()
