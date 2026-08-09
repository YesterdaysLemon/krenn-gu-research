"""Audit the exact-20, 84-entry structural boundary for ``n=8,d=3``.

The proof has two finite support-level parts.

First, choose the three generic killer blocks at each vertex.  If ``r`` of
the selected skeleton edges are chosen from both ends, ``s`` from one end,
and ``t`` from neither end, then

    2 r + s = 3 n,       r + s + t = m.

A reciprocal killer block has at most one supported entry, a one-way killer
block at most three, and an unused block at most nine.  For ``n=8,m=20``
this gives ``entries <= 36 + 4 r <= 84``.  Equality forces twelve
reciprocal singleton blocks and eight full blocks.

Second, the failure-hyperplane backup theorem forces each singleton to be
diagonal.  At one vertex write its three singleton supports as
``(a_c,c)``, one for each opposite-end colour ``c``.  If ``a_c != c``,
the non-coordinate killer ``e_(a_c) outer e_c`` needs another incident
backup block ``B`` with:

* a nonzero ``c``-column independent of ``e_(a_c)``; and
* every nonzero non-``c`` column supported exactly on ``e_(a_c)``.

The two full equality blocks fail the second condition.  The other two
singleton blocks have columns different from ``c`` and fail the first.
This script exhausts all 27 local singleton-row assignments, for every
possible number zero through four of additional full blocks at the vertex,
and checks that the diagonal assignment is the unique one satisfying every
required backup.  On a 5-regular skeleton there are exactly two full blocks
at each vertex, so the full blocks form a spanning 2-factor.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

N = 8
D = 3
M = 20

Support = frozenset[tuple[int, int]]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry_bound_rows(
    n: int = N,
    m: int = M,
) -> list[dict[str, int]]:
    """Enumerate every integer killer-edge incidence decomposition."""

    rows: list[dict[str, int]] = []
    for reciprocal in range(m + 1):
        for one_way in range(m + 1):
            unused = m - reciprocal - one_way
            if unused < 0:
                continue
            if 2 * reciprocal + one_way != D * n:
                continue
            rows.append(
                {
                    "reciprocal_selected_edges": reciprocal,
                    "one_way_selected_edges": one_way,
                    "unused_edges": unused,
                    "entry_upper_bound": (
                        reciprocal + D * one_way + D * D * unused
                    ),
                }
            )
    return rows


def audit_general_entry_identity() -> int:
    """Exhaustively check ``E <= 9m-12n`` on a broad finite grid."""

    cases = 0
    for n in range(4, 22, 2):
        for m in range(D * n // 2, n * (n - 1) // 2 + 1):
            rows = entry_bound_rows(n, m)
            if not rows:
                raise AssertionError(
                    f"no incidence row for n={n}, m={m}"
                )
            maximum = max(row["entry_upper_bound"] for row in rows)
            if maximum != D * D * m - 12 * n:
                raise AssertionError(
                    f"general bound changed at n={n}, m={m}"
                )
            equality = [
                row
                for row in rows
                if row["entry_upper_bound"] == maximum
            ]
            if len(equality) != 1:
                raise AssertionError(
                    f"equality row is not unique at n={n}, m={m}"
                )
            if (
                equality[0]["reciprocal_selected_edges"]
                != D * n // 2
                or equality[0]["one_way_selected_edges"] != 0
                or equality[0]["unused_edges"] != m - D * n // 2
            ):
                raise AssertionError(
                    f"general equality structure changed at n={n}, m={m}"
                )
            cases += 1
    return cases


def is_backup(
    killer_row: int,
    killer_colour: int,
    block: Support,
) -> bool:
    """Replay the necessary support conditions for a backup block."""

    target_rows = {
        row for row, colour in block if colour == killer_colour
    }
    if not target_rows:
        return False
    if not any(row != killer_row for row in target_rows):
        return False
    for colour in range(D):
        if colour == killer_colour:
            continue
        column_rows = {row for row, other in block if other == colour}
        if column_rows and column_rows != {killer_row}:
            return False
    return True


def local_equality_blocks(
    singleton_rows: tuple[int, ...],
    full_degree: int,
) -> tuple[Support, ...]:
    """Return the three singleton and all full incident equality blocks."""

    singletons = tuple(
        frozenset({(row, colour)})
        for colour, row in enumerate(singleton_rows)
    )
    full = frozenset(itertools.product(range(D), repeat=2))
    return (*singletons, *((full,) * full_degree))


def local_assignment_has_backups(
    singleton_rows: tuple[int, ...],
    full_degree: int,
) -> bool:
    """Check every non-coordinate singleton killer has another backup."""

    blocks = local_equality_blocks(singleton_rows, full_degree)
    for colour, killer_row in enumerate(singleton_rows):
        if killer_row == colour:
            continue
        if not any(
            is_backup(killer_row, colour, block)
            for index, block in enumerate(blocks)
            if index != colour
        ):
            return False
    return True


def audit() -> dict[str, object]:
    bound_rows = entry_bound_rows()
    general_identity_checks = audit_general_entry_identity()
    maximum = max(row["entry_upper_bound"] for row in bound_rows)
    equality_rows = [
        row for row in bound_rows if row["entry_upper_bound"] == maximum
    ]
    if maximum != 84:
        raise AssertionError(f"unexpected entry maximum {maximum}")
    if equality_rows != [
        {
            "reciprocal_selected_edges": 12,
            "one_way_selected_edges": 0,
            "unused_edges": 8,
            "entry_upper_bound": 84,
        }
    ]:
        raise AssertionError("the equality incidence decomposition changed")

    assignments = list(itertools.product(range(D), repeat=D))
    survivors_by_full_degree: dict[int, list[tuple[int, ...]]] = {}
    for full_degree in range(5):
        surviving = [
            assignment
            for assignment in assignments
            if local_assignment_has_backups(
                assignment,
                full_degree,
            )
        ]
        if surviving != [tuple(range(D))]:
            raise AssertionError(
                "non-diagonal local equality assignment survived with "
                f"full degree {full_degree}: {surviving}"
            )
        survivors_by_full_degree[full_degree] = surviving

    full = frozenset(itertools.product(range(D), repeat=2))
    full_backup_checks = 0
    other_singleton_checks = 0
    for killer_colour in range(D):
        for killer_row in range(D):
            if killer_row == killer_colour:
                continue
            full_backup_checks += 1
            if is_backup(killer_row, killer_colour, full):
                raise AssertionError("a full equality block became a backup")
            for other_colour in range(D):
                if other_colour == killer_colour:
                    continue
                for other_row in range(D):
                    other_singleton_checks += 1
                    singleton = frozenset({(other_row, other_colour)})
                    if is_backup(
                        killer_row,
                        killer_colour,
                        singleton,
                    ):
                        raise AssertionError(
                            "a wrong-column singleton became a backup"
                        )

    script = Path(__file__)
    return {
        "claim": (
            "Every exact-20-edge n=8,d=3 support has at most 84 "
            "entries; equality forces eight full blocks and twelve "
            "diagonal singleton blocks. On a 5-regular skeleton these "
            "are a spanning full 2-factor and three singleton perfect "
            "matchings."
        ),
        "parameters": {"n": N, "d": D, "skeleton_edges": M},
        "general_three_colour_bound": "entries <= 9m - 12n",
        "general_identity_cases_checked": general_identity_checks,
        "killer_incidence_rows": bound_rows,
        "maximum_entries": maximum,
        "equality_rows": equality_rows,
        "local_assignments_checked_per_full_degree": len(assignments),
        "full_degrees_checked": list(survivors_by_full_degree),
        "local_assignments_with_all_required_backups": {
            str(full_degree): [list(row) for row in surviving]
            for full_degree, surviving in (
                survivors_by_full_degree.items()
            )
        },
        "full_block_nonbackup_checks": full_backup_checks,
        "wrong_column_singleton_nonbackup_checks": (
            other_singleton_checks
        ),
        "consequence": {
            "singleton_subgraph_degree": D,
            "singleton_colour_classes": (
                "three perfect matchings"
            ),
            "if_skeleton_is_5_regular": {
                "full_block_subgraph_degree": 2,
                "full_block_subgraph": "a spanning 2-factor",
            },
        },
        "script": str(script),
        "script_sha256": sha256(script),
        "verified": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/eight_vertex_entry84_boundary_verified.json"
        ),
    )
    args = parser.parse_args()
    payload = audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
