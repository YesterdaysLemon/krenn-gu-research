#!/usr/bin/env python3
"""Finite-field audit of the secondary-gate H31 exclusion."""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
import sys
from pathlib import Path


for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT
expose_claim_package(REPO_ROOT, "claims/p5/h31/single-gate-p3")

from audit_p5_h31_single_gate_p3_reduction import (  # noqa: E402
    permanent,
    projective_points_2,
    rank_mod,
)


THEOREM = HERE / "P5_H31_SECONDARY_GATE_EXCLUSION.md"
BITS3 = tuple(itertools.product((0, 1), repeat=3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pair_product(
    first: tuple[int, int, int],
    second: tuple[int, int, int],
    prime: int,
) -> tuple[int, int, int]:
    return (
        (
            first[1] * second[2]
            + first[2] * second[1]
        )
        % prime,
        (
            first[0] * second[2]
            + first[2] * second[0]
        )
        % prime,
        (
            first[0] * second[1]
            + first[1] * second[0]
        )
        % prime,
    )


def vector_rank(
    vectors: tuple[tuple[int, ...], ...],
    prime: int,
) -> int:
    return rank_mod([list(vector) for vector in vectors], prime)


def support(vector: tuple[int, ...]) -> frozenset[int]:
    return frozenset(
        index for index, entry in enumerate(vector)
        if entry
    )


def one_marked_map(
    mode: int,
    alpha: tuple[tuple[int, ...], ...],
    beta: tuple[tuple[int, ...], ...],
    prime: int,
) -> list[list[int]]:
    output = []
    for bits in BITS3:
        selected: list[tuple[int, ...] | None] = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other]
                    if bits[bit_index]
                    else alpha[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(
                int(index == coordinate)
                for index in range(4)
            )
            coefficient_row.append(
                permanent(
                    tuple(
                        basis
                        if other == mode
                        else selected[other]  # type: ignore[arg-type]
                        for other in range(4)
                    ),
                    prime,
                )
            )
        output.append(coefficient_row)
    return output


def combined_marked(
    mode: int,
    alpha_s: tuple[tuple[int, ...], ...],
    beta_s: tuple[tuple[int, ...], ...],
    alpha_p: tuple[tuple[int, ...], ...],
    beta_p: tuple[tuple[int, ...], ...],
    prime: int,
) -> list[list[int]]:
    source = one_marked_map(mode, alpha_s, beta_s, prime)
    partial = one_marked_map(mode, alpha_p, beta_p, prime)
    return (
        [row[:3] + [row[3], 0] for row in source]
        + [row[:3] + [0, row[3]] for row in partial]
    )


def selected_rank(
    matrix: list[list[int]],
    rows: tuple[int, ...],
    prime: int,
) -> int:
    return rank_mod([matrix[row] for row in rows], prime)


def line_plane_rows(
    a0: int,
    v0: int,
    extension: tuple[int, int, int, int],
    gate: int,
    prime: int,
    alpha_zero: bool = False,
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]:
    C, D, E, F = extension
    T = -C * v0 % prime
    X = -F * a0 % prime
    alpha = (
        (0, 0, 0, 0 if alpha_zero else 1),
        (a0, 1, -1 % prime, X),
        (1, 0, 0, C),
        (0, 1, -1 % prime, E),
    )
    beta = (
        (v0, 1, 1, T),
        (0, 0, 0, gate),
        (0, 1, 1, D),
        (1, 0, 0, F),
    )
    return alpha, beta


def two_plane_common(
    kind: str,
    prime: int,
) -> tuple[
    tuple[int, int, int],
    tuple[int, int, int],
    tuple[int, int, int],
    tuple[int, int, int],
    tuple[int, int, int],
    tuple[int, int, int],
]:
    if kind == "P0":
        a = (1, 1, 0)
        v = (1, -1 % prime, 0)
    else:
        a = (1, 0, -1 % prime)
        v = (1, 0, 1)
    c = (1, 1, 0)
    d = (1, 0, 1)
    e = (1, 0, -1 % prime)
    f = (1, -1 % prime, 0)
    return a, v, c, d, e, f


def two_plane_rows(
    kind: str,
    extension: tuple[int, int, int, int],
    gate: int,
    prime: int,
    alpha_zero: bool = False,
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]:
    C, D, E, F = extension
    a, v, c, d, e, f = two_plane_common(kind, prime)
    alpha = (
        (0, 0, 0, 0 if alpha_zero else 1),
        a + (0,),
        c + (C,),
        e + (E,),
    )
    beta = (
        v + (0,),
        (0, 0, 0, gate),
        d + (D,),
        f + (F,),
    )
    return alpha, beta


def audit_zero_pairs(prime: int) -> dict[str, object]:
    points = projective_points_2(prime)
    zero_pairs = []
    for first in points:
        for second in points:
            if pair_product(first, second, prime) != (0, 0, 0):
                continue
            first_support = support(first)
            second_support = support(second)
            assert first_support == second_support
            assert len(first_support) <= 2
            zero_pairs.append((first, second))

    pattern_counts: Counter[str] = Counter()
    exceptional_quadruples = 0
    for c, f in zero_pairs:
        for d, e in zero_pairs:
            if vector_rank((c, d), prime) != 2:
                continue
            if vector_rank((e, f), prime) != 2:
                continue
            first_diagonal = pair_product(c, e, prime)
            second_diagonal = pair_product(d, f, prime)
            if vector_rank(
                (first_diagonal, second_diagonal),
                prime,
            ) != 2:
                continue
            exceptional_quadruples += 1
            first_support = support(c)
            second_support = support(d)
            if len(first_support) == 1:
                assert len(second_support) == 2
                assert first_support.isdisjoint(second_support)
                pattern_counts["line_complementary_plane"] += 1
            elif len(second_support) == 1:
                assert len(first_support) == 2
                assert first_support.isdisjoint(second_support)
                pattern_counts["line_complementary_plane"] += 1
            else:
                assert len(first_support) == len(second_support) == 2
                assert first_support != second_support
                pattern_counts["two_distinct_coordinate_planes"] += 1

    return {
        "projective_points": len(points),
        "zero_pair_count": len(zero_pairs),
        "exceptional_basis_quadruples": exceptional_quadruples,
        "support_pattern_counts": dict(sorted(pattern_counts.items())),
    }


def audit_line_plane(prime: int) -> dict[str, object]:
    partial_cases: Counter[str] = Counter()
    deepest_partial = 0
    for a0 in range(prime):
        for v0 in range(prime):
            for C, D, E, F in itertools.product(
                range(prime),
                repeat=4,
            ):
                if (D * v0 - E * a0) % prime:
                    continue
                alpha, beta = line_plane_rows(
                    a0,
                    v0,
                    (C, D, E, F),
                    1,
                    prime,
                )
                if v0:
                    matrix = one_marked_map(2, alpha, beta, prime)
                    assert selected_rank(
                        matrix,
                        (0, 1, 4, 7),
                        prime,
                    ) == 4
                    partial_cases["v0"] += 1
                elif a0:
                    matrix = one_marked_map(3, alpha, beta, prime)
                    assert selected_rank(
                        matrix,
                        (0, 5, 6, 7),
                        prime,
                    ) == 4
                    partial_cases["a0"] += 1
                elif E:
                    matrix = one_marked_map(1, alpha, beta, prime)
                    assert selected_rank(
                        matrix,
                        (0, 3, 6, 7),
                        prime,
                    ) == 4
                    partial_cases["E"] += 1
                elif D:
                    matrix = one_marked_map(0, alpha, beta, prime)
                    assert selected_rank(
                        matrix,
                        (0, 2, 4, 7),
                        prime,
                    ) == 4
                    partial_cases["D"] += 1
                else:
                    deepest_partial += 1

    stacked_cases: Counter[str] = Counter()
    alpha_p, beta_p = line_plane_rows(
        0,
        0,
        (0, 0, 0, 0),
        1,
        prime,
    )
    for Ds in range(prime):
        for Es in range(prime):
            alpha_s, beta_s = line_plane_rows(
                0,
                0,
                (0, Ds, Es, 0),
                1,
                prime,
                alpha_zero=True,
            )
            if Ds:
                combined = combined_marked(
                    0,
                    alpha_s,
                    beta_s,
                    alpha_p,
                    beta_p,
                    prime,
                )
                assert selected_rank(
                    combined,
                    (0, 2, 4, 8, 15),
                    prime,
                ) == 5
                stacked_cases["Ds"] += 1
            elif Es:
                combined = combined_marked(
                    1,
                    alpha_s,
                    beta_s,
                    alpha_p,
                    beta_p,
                    prime,
                )
                assert selected_rank(
                    combined,
                    (6, 7, 8, 11, 15),
                    prime,
                ) == 5
                stacked_cases["Es"] += 1
            else:
                stacked_cases["deepest"] += 1

    deep_pairs = 0
    for Cs, Cp, Fs, Fp in itertools.product(
        range(prime),
        repeat=4,
    ):
        alpha_s, beta_s = line_plane_rows(
            0,
            0,
            (Cs, 0, 0, Fs),
            1,
            prime,
            alpha_zero=True,
        )
        alpha_p, beta_p = line_plane_rows(
            0,
            0,
            (Cp, 0, 0, Fp),
            1,
            prime,
        )
        combined0 = combined_marked(
            0,
            alpha_s,
            beta_s,
            alpha_p,
            beta_p,
            prime,
        )
        kernel0 = (-1 % prime, 0, 0, Cs, Cp)
        assert all(
            sum(left * right for left, right in zip(row, kernel0))
            % prime
            == 0
            for row in combined0
        )
        assert rank_mod(combined0, prime) == 4
        combined2 = combined_marked(
            2,
            alpha_s,
            beta_s,
            alpha_p,
            beta_p,
            prime,
        )
        assert rank_mod(combined2, prime) == 3
        assert all(
            row[3] == row[4] == 0
            for row in combined2
        )
        mixed = permanent(
            (
                (-1 % prime, 0, 0, Cs),
                alpha_s[1],
                (0, 0, 0, 1),
                alpha_s[3],
            ),
            prime,
        )
        assert mixed == 2 % prime
        deep_pairs += 1

    return {
        "partial_case_counts": dict(sorted(partial_cases.items())),
        "deepest_partial_extensions": deepest_partial,
        "stacked_case_counts": dict(sorted(stacked_cases.items())),
        "deepest_extension_pairs": deep_pairs,
    }


def audit_two_planes(prime: int) -> dict[str, object]:
    generic_cases: Counter[str] = Counter()
    tangent_parameters = []
    for alpha_parameter in range(prime):
        for beta_parameter in range(prime):
            K = alpha_parameter * (beta_parameter - 1) % prime
            L = beta_parameter * (alpha_parameter + 1) % prime
            if K == L == 0:
                tangent_parameters.append(
                    (alpha_parameter, beta_parameter)
                )
                continue
            for c0 in range(prime):
                for d0 in range(prime):
                    C = L * c0 % prime
                    F = -K * c0 % prime
                    D = L * d0 % prime
                    E = -K * d0 % prime
                    T = K * L * (c0 - d0) % prime
                    X = -T % prime
                    normal = (0, 1, 1)
                    a = tuple(
                        (left + alpha_parameter * right) % prime
                        for left, right in zip((1, 1, 0), normal)
                    )
                    v = tuple(
                        (left + beta_parameter * right) % prime
                        for left, right in zip((1, -1, 0), normal)
                    )
                    common = two_plane_common("P0", prime)
                    _, _, c, d, e, f = common
                    alpha_rows = (
                        (0, 0, 0, 1),
                        a + (X,),
                        c + (C,),
                        e + (E,),
                    )
                    beta_rows = (
                        v + (T,),
                        (0, 0, 0, 1),
                        d + (D,),
                        f + (F,),
                    )
                    if K:
                        marked = one_marked_map(
                            2,
                            alpha_rows,
                            beta_rows,
                            prime,
                        )
                        assert selected_rank(
                            marked,
                            (0, 5, 6, 7),
                            prime,
                        ) == 4
                        generic_cases["K"] += 1
                    else:
                        assert L
                        marked = one_marked_map(
                            3,
                            alpha_rows,
                            beta_rows,
                            prime,
                        )
                        assert selected_rank(
                            marked,
                            (0, 1, 4, 7),
                            prime,
                        ) == 4
                        generic_cases["L"] += 1

    assert set(tangent_parameters) == {
        (0, 0),
        (-1 % prime, 1),
    }

    tangent_cases: Counter[str] = Counter()
    deepest_tangents = []
    for kind in ("P0", "P1"):
        for extension in itertools.product(range(prime), repeat=4):
            C, D, E, F = extension
            alpha, beta = two_plane_rows(
                kind,
                extension,
                1,
                prime,
            )
            if kind == "P0":
                if F:
                    mode, rows, label = 0, (0, 1, 4, 7), "P0_F"
                elif E:
                    mode, rows, label = 0, (0, 2, 4, 7), "P0_E"
                elif C:
                    mode, rows, label = 1, (0, 3, 4, 7), "P0_C"
                elif D:
                    mode, rows, label = 1, (0, 3, 6, 7), "P0_D"
                else:
                    deepest_tangents.append(kind)
                    tangent_cases["P0_deepest"] += 1
                    continue
            else:
                if C:
                    mode, rows, label = 0, (0, 1, 4, 7), "P1_C"
                elif D:
                    mode, rows, label = 0, (0, 2, 4, 7), "P1_D"
                elif E:
                    mode, rows, label = 1, (0, 3, 4, 7), "P1_E"
                elif F:
                    mode, rows, label = 1, (0, 3, 5, 7), "P1_F"
                else:
                    deepest_tangents.append(kind)
                    tangent_cases["P1_deepest"] += 1
                    continue
            marked = one_marked_map(mode, alpha, beta, prime)
            assert selected_rank(marked, rows, prime) == 4
            tangent_cases[label] += 1

    stacked_cases: Counter[str] = Counter()
    for kind in ("P0", "P1"):
        alpha_p, beta_p = two_plane_rows(
            kind,
            (0, 0, 0, 0),
            1,
            prime,
        )
        for extension in itertools.product(range(prime), repeat=4):
            C, D, E, F = extension
            alpha_s, beta_s = two_plane_rows(
                kind,
                extension,
                1,
                prime,
                alpha_zero=True,
            )
            if not any(extension):
                stacked_cases[f"{kind}_deepest"] += 1
                continue
            if kind == "P0":
                if F:
                    mode, rows, label = 0, (0, 1, 4, 7, 8), "P0_F"
                elif E:
                    mode, rows, label = 0, (0, 2, 4, 7, 8), "P0_E"
                elif C:
                    mode, rows, label = 1, (4, 7, 8, 11, 15), "P0_C"
                else:
                    assert D
                    mode, rows, label = 1, (6, 7, 8, 11, 15), "P0_D"
            else:
                if C:
                    mode, rows, label = 0, (0, 1, 4, 8, 15), "P1_C"
                elif D:
                    mode, rows, label = 0, (0, 2, 4, 8, 15), "P1_D"
                elif E:
                    mode, rows, label = 1, (4, 7, 8, 11, 15), "P1_E"
                else:
                    assert F
                    mode, rows, label = 1, (5, 7, 8, 11, 15), "P1_F"
            combined = combined_marked(
                mode,
                alpha_s,
                beta_s,
                alpha_p,
                beta_p,
                prime,
            )
            assert selected_rank(combined, rows, prime) == 5
            stacked_cases[label] += 1

        alpha_s, beta_s = two_plane_rows(
            kind,
            (0, 0, 0, 0),
            1,
            prime,
            alpha_zero=True,
        )
        combined0 = combined_marked(
            0,
            alpha_s,
            beta_s,
            alpha_p,
            beta_p,
            prime,
        )
        normal = (0, 1, 1, 0, 0)
        assert all(
            sum(left * right for left, right in zip(row, normal))
            % prime
            == 0
            for row in combined0
        )
        assert rank_mod(combined0, prime) == 4
        combined2 = combined_marked(
            2,
            alpha_s,
            beta_s,
            alpha_p,
            beta_p,
            prime,
        )
        assert rank_mod(combined2, prime) == 3
        assert all(
            row[3] == row[4] == 0
            for row in combined2
        )
        a, v, _, _, _, f = two_plane_common(kind, prime)
        if kind == "P0":
            mixed_rows = (
                v + (0,),
                (0, 1, 1, 0),
                (0, 0, 0, 1),
                f + (0,),
            )
        else:
            mixed_rows = (
                (0, 1, 1, 0),
                a + (0,),
                (0, 0, 0, 1),
                f + (0,),
            )
        assert permanent(mixed_rows, prime) == -2 % prime

    return {
        "generic_case_counts": dict(sorted(generic_cases.items())),
        "tangent_parameters": tangent_parameters,
        "tangent_case_counts": dict(sorted(tangent_cases.items())),
        "stacked_case_counts": dict(sorted(stacked_cases.items())),
        "deepest_tangent_checks": deepest_tangents,
    }


def audit_prime(prime: int) -> dict[str, object]:
    return {
        "prime": prime,
        "zero_pair_geometry": audit_zero_pairs(prime),
        "line_plane": audit_line_plane(prime),
        "two_planes": audit_two_planes(prime),
    }


def main() -> None:
    audits = [audit_prime(prime) for prime in (5, 7)]
    output = {
        "verified": True,
        "method": (
            "independent modular pair products, permanents, and "
            "row reduction on the two support-polarity strata"
        ),
        "fields": audits,
        "ambient_local_maps_enumerated": False,
        "Grassmannians_enumerated": False,
        "finite_field_audit_is_characteristic_zero_proof": False,
        "secondary_gate_H31_lift_possible": False,
        "all_single_gate_H31_excluded": True,
        "all_rank_two_pure_P4_H31_excluded": False,
        "H31_excluded": False,
        "P5_to_Delta3_resolved": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = ROOT / "tmp" / "p5_h31_secondary_gate_audit.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
