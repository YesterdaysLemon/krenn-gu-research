"""Independent no-import audit for the same-type two-defect detector."""

from __future__ import annotations

from itertools import product

COLOURS = (0, 1, 2)
ROWS = (0, 1, 2, 3, 4)  # b,c,x,y,z
FULL = 0b111


def singleton(colour: int) -> int:
    return 1 << colour


def plane_missing(colour: int) -> int:
    return FULL ^ singleton(colour)


def supports_colour(mask: int, colour: int) -> bool:
    return bool(mask & singleton(colour))


def has_source_assignment(mode_rows: tuple[tuple[int, ...], ...], colour: int) -> bool:
    """Use a recursive matching, independent of the primary permutation sum."""

    def extend(mode: int, used_rows: int) -> bool:
        if mode == len(mode_rows):
            return True
        for row, support in enumerate(mode_rows[mode]):
            if used_rows & (1 << row):
                continue
            if not supports_colour(support, colour):
                continue
            if extend(mode + 1, used_rows | (1 << row)):
                return True
        return False

    return extend(0, 0)


def colour_degrees(labels: tuple[int, ...]) -> tuple[int, int, int]:
    return tuple(sum(supports_colour(label, colour) for label in labels) for colour in COLOURS)


def audit_inactive_masks() -> tuple[int, int]:
    roots_mask = 0b1111
    equal = 0
    diamonds = 0
    for inactive_u in range(1, roots_mask + 1):
        if inactive_u.bit_count() != 2:
            continue
        for inactive_v in range(1, roots_mask + 1):
            if inactive_v.bit_count() != 2:
                continue
            if not (inactive_u & inactive_v):
                continue
            if (inactive_u | inactive_v) == roots_mask:
                continue
            if inactive_u == inactive_v:
                equal += 1
            else:
                diamonds += 1
                assert (inactive_u & inactive_v).bit_count() == 1
                assert (inactive_u | inactive_v).bit_count() == 3
    assert (equal, diamonds) == (6, 24)
    aa_pair_capacity = sum(1 for _ in range(5))
    aa_pair_quota = 3 * 2
    bb_triple_capacity = sum((1, 1, 2, 2, 2))
    bb_triple_quota = 3 * 3
    assert aa_pair_capacity < aa_pair_quota
    assert bb_triple_capacity < bb_triple_quota
    return equal, diamonds


def defect_axis_triples() -> tuple[tuple[int, int, int], ...]:
    return tuple(
        axes
        for axes in product(COLOURS, repeat=3)
        if len(set(axes)) == 3
    )


def audit_aa_overapproximation() -> tuple[int, int]:
    total = 0
    survivors = 0
    for a_u, x_u, z_u in defect_axis_triples():
        for a_v, y_v, z_v in defect_axis_triples():
            for transverse in product(COLOURS, repeat=3):
                total += 1
                modes: list[tuple[int, ...]] = [
                    (
                        0,
                        singleton(a_u),
                        singleton(x_u),
                        singleton(a_u),
                        singleton(z_u),
                    ),
                    (
                        0,
                        singleton(a_v),
                        singleton(a_v),
                        singleton(y_v),
                        singleton(z_v),
                    ),
                ]
                for axis in transverse:
                    modes.append(
                        (
                            FULL,
                            singleton(axis),
                            singleton(axis),
                            singleton(axis),
                            FULL,
                        )
                    )
                mode_rows = tuple(modes)
                if all(has_source_assignment(mode_rows, colour) for colour in COLOURS):
                    survivors += 1
    assert total == 972
    assert survivors == 0
    return total, survivors


def bb_mode_rows(
    beta_u: int,
    beta_v: int,
    missing_u: int,
    missing_v: int,
    transverse_missing: tuple[int, int, int],
) -> tuple[tuple[int, ...], ...]:
    modes: list[tuple[int, ...]] = [
        (
            singleton(beta_u),
            singleton(beta_u),
            plane_missing(missing_u),
            singleton(beta_u),
            FULL,
        ),
        (
            singleton(beta_v),
            singleton(beta_v),
            singleton(beta_v),
            plane_missing(missing_v),
            FULL,
        ),
    ]
    for missing in transverse_missing:
        plane = plane_missing(missing)
        modes.append((plane, plane, plane, plane, FULL))
    return tuple(modes)


def bb_triple_quota(
    beta_u: int,
    beta_v: int,
    missing_u: int,
    missing_v: int,
    transverse_missing: tuple[int, int, int],
) -> bool:
    transverse_planes = tuple(plane_missing(missing) for missing in transverse_missing)
    labels_bcx = (
        plane_missing(missing_u),
        singleton(beta_v),
        *transverse_planes,
    )
    labels_bcy = (
        singleton(beta_u),
        plane_missing(missing_v),
        *transverse_planes,
    )
    return min(colour_degrees(labels_bcx)) >= 3 and min(colour_degrees(labels_bcy)) >= 3


def audit_bb_overapproximation() -> tuple[int, int, int]:
    total = 0
    quota_ledgers = 0
    survivors = 0
    for beta_u, beta_v in product(COLOURS, repeat=2):
        for missing_u, missing_v in product(COLOURS, repeat=2):
            if missing_u == beta_u or missing_v == beta_v:
                continue
            for transverse_missing in product(COLOURS, repeat=3):
                total += 1
                if not bb_triple_quota(
                    beta_u,
                    beta_v,
                    missing_u,
                    missing_v,
                    transverse_missing,
                ):
                    continue
                quota_ledgers += 1
                mode_rows = bb_mode_rows(
                    beta_u,
                    beta_v,
                    missing_u,
                    missing_v,
                    transverse_missing,
                )
                if all(has_source_assignment(mode_rows, colour) for colour in COLOURS):
                    survivors += 1
    assert total == 972
    assert quota_ledgers == 54
    assert survivors == 0
    return total, quota_ledgers, survivors


def main() -> None:
    equal, diamonds = audit_inactive_masks()
    aa_total, aa_survivors = audit_aa_overapproximation()
    bb_total, bb_quota, bb_survivors = audit_bb_overapproximation()
    print(
        "AUDIT PASS: inactive masks independently give "
        f"{equal} equal and {diamonds} diamond patterns"
    )
    print(
        f"AUDIT PASS: {aa_total} raw AA support graphs have "
        f"{aa_survivors} three-pure-colour survivors"
    )
    print(
        f"AUDIT PASS: {bb_total} raw BB support graphs give {bb_quota} "
        f"triple-quota ledgers and {bb_survivors} survivors"
    )
    print("AUDIT SCOPE: AA/BB two-defect cells detected")
    print("AUDIT SCOPE: three-or-more defects and global Krenn-Gu remain open")
    print("searches=0 project_imports=0 computer_algebra=0")


if __name__ == "__main__":
    main()
