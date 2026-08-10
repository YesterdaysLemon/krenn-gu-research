#!/usr/bin/env python3
"""Independent exact and audit-only modular checks of the normalized sheet."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess
import time

import sympy as sp
import sys
from pathlib import Path

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


WORDS4 = tuple(itertools.product((0, 1), repeat=4))
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))

p, q = sp.symbols("p q")
H = sp.symbols("h0:4")
Z = sp.symbols("x0:4") + sp.symbols("y0:4")
w, u = sp.symbols("w u")


def permanent3(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(3))
            for permutation in PERMUTATIONS3
        )
    )


def permanent4(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS4
        )
    )


def bases() -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    one, zero = sp.Integer(1), sp.Integer(0)
    s = p - q + 1
    e = (one, zero, zero, zero)
    alpha = (
        (zero, -p * (p + 1), q * (q - 1), s),
        e,
        e,
        (one, one, one, zero),
    )
    canonical = (
        (-s, -p - q, p + q, zero),
        (zero, p + 1, q - 1, one),
        (zero, p, q, one),
        e,
    )
    beta = tuple(
        tuple(
            sp.expand(canonical[mode][coordinate] + H[mode] * alpha[mode][coordinate])
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    return alpha, beta


def extension_rows_from_cofactors(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> dict[tuple[int, ...], tuple[sp.Expr, ...]]:
    """Build all sixteen extension rows without differentiating a permanent."""
    retained = tuple(index for index in range(4) if index != distinguished)
    rows = {}
    for word in WORDS4:
        row = [sp.Integer(0)] * 8
        for mode in range(4):
            selected = tuple(
                tuple(
                    (beta[other] if word[other] else alpha[other])[coordinate]
                    for coordinate in retained
                )
                for other in range(4)
                if other != mode
            )
            target = mode + 4 * word[mode]
            row[target] = permanent3(selected)
        rows[word] = tuple(row)
    return rows


def mode_three_map_from_cofactors(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    """Build the mode-three map from complementary 3x3 permanents."""
    result = []
    for bits in WORDS3:
        selected = tuple(beta[mode] if bits[mode] else alpha[mode] for mode in range(3))
        result.append(
            [
                permanent3(
                    tuple(
                        tuple(row[index] for index in range(4) if index != coordinate)
                        for row in selected
                    )
                )
                for coordinate in range(4)
            ]
        )
    return sp.Matrix(result)


def neighbouring_mode_three_map(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    retained = tuple(index for index in range(4) if index != distinguished)
    alpha_extended = tuple(
        tuple(alpha[mode][index] for index in retained) + (Z[mode],)
        for mode in range(4)
    )
    beta_extended = tuple(
        tuple(beta[mode][index] for index in retained) + (Z[4 + mode],)
        for mode in range(4)
    )
    return mode_three_map_from_cofactors(alpha_extended, beta_extended)


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for the independent exact audit")


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def ideal_line(name: str, generators: tuple[sp.Expr, ...]) -> str:
    return "ideal " + name + "=" + ",".join(map(singular, generators)) + ";"


def primary_components(
    distinguished: int,
) -> tuple[tuple[sp.Expr, ...], ...]:
    h0, h1, h2, h3 = H
    if distinguished == 1:
        return (
            (h0, h3, h2, h1 + q - 1),
            (h0, h3, h2, q),
            (h0, h3, h2, 2 * q - 1),
            (h0, h3, h1, 2 * q - 1),
            (h0, h3, h1, h2 + q),
            (h0, h3, h1, q - 1),
        )
    if distinguished == 2:
        return (
            (h0, h3, h2, h1 + p + 1),
            (h0, h3, h2, p),
            (h0, h3, h2, 2 * p + 1),
            (h0, h3, h1, 2 * p + 1),
            (h0, h3, h1, h2 + p),
            (h0, h3, h1, p + 1),
        )
    if distinguished == 3:
        return (
            (q, h2, h1 - p - 1, h0, h3),
            (q - 1, h2 - p, h1, h0, h3),
            (p - q, h2 - q, h1, h0, h3),
            (p - q + 2, h2, h1 - q + 1, h0, h3),
            (2 * p * q - p + q, h2**2, h1 - h2, h0, h3),
            (p, h2, h1 - q + 1, h0, h3),
            (p + 1, h2 - q, h1, h0, h3),
        )
    raise ValueError(distinguished)


def displayed_projection(distinguished: int) -> tuple[sp.Expr, ...]:
    h0, h1, h2, h3 = H
    if distinguished == 0:
        return (sp.Integer(1),)
    if distinguished == 1:
        return (
            h0,
            h3,
            h1 * h2,
            (2 * q - 1) * (q * h1 + (q - 1) * h2 + q * (q - 1)),
            h2 * (h2 + q) * (q - 1) * (2 * q - 1),
        )
    if distinguished == 2:
        return (
            h0,
            h3,
            h1 * h2,
            (2 * p + 1) * (p * h1 + (p + 1) * h2 + p * (p + 1)),
            h2 * (h2 + p) * (p + 1) * (2 * p + 1),
        )
    raise ValueError(distinguished)


def exact_audit(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    pure: sp.Matrix,
) -> dict[str, object]:
    rows = extension_rows_from_cofactors(distinguished, alpha, beta)
    mixed = sp.Matrix(
        [rows[word] for word in WORDS4 if word not in ((0, 0, 0, 0), (1, 1, 1, 1))]
    )
    diagonal_alpha = sp.Matrix([rows[(0, 0, 0, 0)]])
    diagonal_beta = sp.Matrix([rows[(1, 1, 1, 1)]])
    extension = sp.Matrix(Z)
    normalized_open = (p + q) * (p - q + 1)
    equations = (
        *tuple(mixed * extension),
        (diagonal_alpha * extension)[0] - 1,
        w * (diagonal_beta * extension)[0] - 1,
        u * normalized_open - 1,
    )
    neighbouring = neighbouring_mode_three_map(distinguished, alpha, beta)
    matrix_entries = [
        neighbouring[row, column] for row in range(8) for column in range(4)
    ]
    variables = Z + (w, u) + H + (p, q)
    program = [
        "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(10),dp(4),dp(2));",
        "option(redSB);",
        "proc sameIdeal(ideal A,ideal B)",
        "{",
        " ideal SA=std(A); ideal SB=std(B);",
        " ideal AB=reduce(SA,SB); ideal BA=reduce(SB,SA);",
        " AB=simplify(AB,2); BA=simplify(BA,2);",
        " return((size(AB)==0)&&(size(BA)==0));",
        "}",
        ideal_line("I", equations),
        "I=slimgb(I);",
        "ideal J=std(eliminate(I,x0*x1*x2*x3*y0*y1*y2*y3*w*u));",
    ]
    if distinguished < 3:
        program.extend(
            (
                ideal_line("Expected", displayed_projection(distinguished)),
                "int projection_equal=sameIdeal(J,Expected);",
            )
        )
    else:
        components = primary_components(3)
        for index, component in enumerate(components, start=1):
            program.append(ideal_line(f"Q{index}", component))
        program.append("ideal Expected=Q1;")
        for index in range(2, len(components) + 1):
            program.append(f"Expected=intersect(Expected,Q{index});")
        program.extend(
            (
                "Expected=std(Expected);",
                "int projection_equal=sameIdeal(J,Expected);",
            )
        )
    program.extend(
        (
            "matrix N[8][4]=" + ",".join(map(singular, matrix_entries)) + ";",
            "ideal MaximalMinors=minor(N,4);",
            "ideal RankDrop=slimgb(I+MaximalMinors);",
            "poly rankRemainder=reduce(1,RankDrop);",
            ideal_line("TransverseColumn", tuple(pure[:, distinguished])),
            "ideal Transverse=slimgb(I+TransverseColumn);",
            "poly transverseRemainder=reduce(1,Transverse);",
            '"CODEX_RESULT:d='
            + str(distinguished)
            + ':projection_equal="+string(projection_equal)'
            + '+":rank_unit="+string(rankRemainder==0)'
            + '+":transverse_unit="+string(transverseRemainder==0)'
            + '+":minors="+string(size(MaximalMinors));',
            "quit;",
        )
    )
    started = time.perf_counter()
    completed = subprocess.run(
        singular_command(),
        input="\n".join(program),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=600,
        check=False,
    )
    elapsed = time.perf_counter() - started
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                "independent Singular audit failure",
                distinguished,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    markers = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1, completed.stdout
    fields = dict(field.split("=", 1) for field in markers[0].split(":")[1:])
    assert fields["projection_equal"] == "1", (distinguished, fields)
    assert fields["rank_unit"] == "1", (distinguished, fields)
    assert fields["transverse_unit"] == "1", (distinguished, fields)
    assert int(fields["minors"]) == (6, 68, 68, 68)[distinguished]
    return {
        "distinguished_coordinate": distinguished,
        "independent_projected_ideal_replay_equal": True,
        "independent_all_minors_rank_drop_empty": True,
        "independent_transverse_vanishing_empty": True,
        "nonzero_generated_maximal_minors": int(fields["minors"]),
        "singular_seconds": round(elapsed, 3),
    }


def permanent3_mod(rows: list[list[int]], prime: int) -> int:
    return (
        sum(
            rows[0][permutation[0]] * rows[1][permutation[1]] * rows[2][permutation[2]]
            for permutation in PERMUTATIONS3
        )
        % prime
    )


def bases_mod(
    p_value: int, q_value: int, prime: int
) -> tuple[list[list[int]], list[list[int]]]:
    s = (p_value - q_value + 1) % prime
    alpha = [
        [0, -p_value * (p_value + 1), q_value * (q_value - 1), s],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
    ]
    beta = [
        [-s, -p_value - q_value, p_value + q_value, 0],
        [0, p_value + 1, q_value - 1, 1],
        [0, p_value, q_value, 1],
        [1, 0, 0, 0],
    ]
    return (
        [[entry % prime for entry in row] for row in alpha],
        [[entry % prime for entry in row] for row in beta],
    )


def shifted_mod(
    alpha: list[list[int]],
    canonical: list[list[int]],
    marking: tuple[int, ...],
    prime: int,
) -> list[list[int]]:
    return [
        [
            (canonical[mode][coordinate] + marking[mode] * alpha[mode][coordinate])
            % prime
            for coordinate in range(4)
        ]
        for mode in range(4)
    ]


def extension_rows_mod(
    distinguished: int,
    alpha: list[list[int]],
    beta: list[list[int]],
    prime: int,
) -> list[list[int]]:
    retained = [index for index in range(4) if index != distinguished]
    rows = []
    for word in WORDS4:
        row = [0] * 8
        for mode in range(4):
            selected = [
                [
                    (beta[other] if word[other] else alpha[other])[coordinate]
                    for coordinate in retained
                ]
                for other in range(4)
                if other != mode
            ]
            row[mode + 4 * word[mode]] = permanent3_mod(selected, prime)
        rows.append(row)
    return rows


def mode_three_map_mod(
    alpha: list[list[int]], beta: list[list[int]], prime: int
) -> list[list[int]]:
    result = []
    for bits in WORDS3:
        selected = [beta[mode] if bits[mode] else alpha[mode] for mode in range(3)]
        result.append(
            [
                permanent3_mod(
                    [
                        [row[index] for index in range(4) if index != coordinate]
                        for row in selected
                    ],
                    prime,
                )
                for coordinate in range(4)
            ]
        )
    return result


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    if not matrix:
        return 0
    work = [[entry % prime for entry in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        work[rank] = [(entry * inverse) % prime for entry in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][column]:
                multiplier = work[row][column]
                work[row] = [
                    (work[row][index] - multiplier * work[rank][index]) % prime
                    for index in range(len(work[row]))
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def nullspace_mod(matrix: list[list[int]], prime: int) -> list[list[int]]:
    work = [[entry % prime for entry in row] for row in matrix]
    row = 0
    pivots = []
    for column in range(len(work[0])):
        pivot = next(
            (index for index in range(row, len(work)) if work[index][column]), None
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = pow(work[row][column], -1, prime)
        work[row] = [(entry * inverse) % prime for entry in work[row]]
        for other in range(len(work)):
            if other != row and work[other][column]:
                multiplier = work[other][column]
                work[other] = [
                    (work[other][index] - multiplier * work[row][index]) % prime
                    for index in range(len(work[other]))
                ]
        pivots.append(column)
        row += 1
        if row == len(work):
            break
    free = [column for column in range(len(work[0])) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [0] * len(work[0])
        vector[free_column] = 1
        for pivot_row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -work[pivot_row][free_column] % prime
        basis.append(vector)
    return basis


def dot_mod(row: list[int], vector: list[int], prime: int) -> int:
    return sum(left * right for left, right in zip(row, vector)) % prime


def first_genuine_kernel_vector(
    basis: list[list[int]],
    diagonal_alpha: list[int],
    diagonal_beta: list[int],
    prime: int,
) -> list[int] | None:
    for coefficients in itertools.product(range(prime), repeat=len(basis)):
        if not any(coefficients):
            continue
        vector = [
            sum(
                coefficients[index] * basis[index][coordinate]
                for index in range(len(basis))
            )
            % prime
            for coordinate in range(len(basis[0]))
        ]
        if dot_mod(diagonal_alpha, vector, prime) and dot_mod(
            diagonal_beta, vector, prime
        ):
            return vector
    return None


def expected_marking(
    distinguished: int,
    p_value: int,
    q_value: int,
    marking: tuple[int, int, int, int],
    prime: int,
) -> bool:
    h0, h1, h2, h3 = marking
    if distinguished == 0:
        return False
    if h0 or h3:
        return False
    if distinguished == 1:
        return any(
            (
                h2 == 0 and (h1 + q_value - 1) % prime == 0,
                h2 == 0 and q_value == 0,
                h2 == 0 and (2 * q_value - 1) % prime == 0,
                h1 == 0 and (2 * q_value - 1) % prime == 0,
                h1 == 0 and (h2 + q_value) % prime == 0,
                h1 == 0 and (q_value - 1) % prime == 0,
            )
        )
    if distinguished == 2:
        return any(
            (
                h2 == 0 and (h1 + p_value + 1) % prime == 0,
                h2 == 0 and p_value == 0,
                h2 == 0 and (2 * p_value + 1) % prime == 0,
                h1 == 0 and (2 * p_value + 1) % prime == 0,
                h1 == 0 and (h2 + p_value) % prime == 0,
                h1 == 0 and (p_value + 1) % prime == 0,
            )
        )
    return any(
        (
            q_value == 0 and h2 == 0 and (h1 - p_value - 1) % prime == 0,
            (q_value - 1) % prime == 0 and (h2 - p_value) % prime == 0 and h1 == 0,
            (p_value - q_value) % prime == 0
            and (h2 - q_value) % prime == 0
            and h1 == 0,
            (p_value - q_value + 2) % prime == 0
            and h2 == 0
            and (h1 - q_value + 1) % prime == 0,
            (2 * p_value * q_value - p_value + q_value) % prime == 0
            and h2 == 0
            and h1 == 0,
            p_value == 0 and h2 == 0 and (h1 - q_value + 1) % prime == 0,
            (p_value + 1) % prime == 0 and (h2 - q_value) % prime == 0 and h1 == 0,
        )
    )


def finite_field_audit(prime: int = 11) -> dict[str, object]:
    """Run a tiny representative regression; make no characteristic-zero claim."""
    inverse_two = pow(2, -1, prime)
    samples = (
        ("generic", 1, 5),
        ("q=p and q=1/2", inverse_two, inverse_two),
        ("q=p and p=-1/2", -inverse_two % prime, -inverse_two % prime),
        ("q=p+2 and p=-1/2", -inverse_two % prime, (-inverse_two + 2) % prime),
    )
    marking_checks = 0
    incidence_markings = [0, 0, 0, 0]
    extension_directions = [0, 0, 0, 0]
    sample_results = []
    for label, p_value, q_value in samples:
        normalized_open = (p_value + q_value) * (p_value - q_value + 1) % prime
        assert normalized_open != 0, (label, p_value, q_value)
        alpha, canonical = bases_mod(p_value, q_value, prime)
        sample_incidence = [0, 0, 0, 0]
        sample_directions = [0, 0, 0, 0]
        # At most twelve explicit controls: the four generic projected
        # points, representatives of every deletion-three stratum and the
        # marking axes, one in-plane negative control, and two off-plane
        # negative controls.  There is no h1,h2 sweep.
        markings = tuple(
            sorted(
                {
                    (0, (1 - q_value) % prime, 0, 0),
                    (0, 0, -q_value % prime, 0),
                    (0, (-p_value - 1) % prime, 0, 0),
                    (0, 0, -p_value % prime, 0),
                    (0, 0, 0, 0),
                    (0, (q_value - 1) % prime, 0, 0),
                    (0, 0, q_value, 0),
                    (0, (p_value + 1) % prime, 0, 0),
                    (0, 0, p_value, 0),
                    (0, 1, 1, 0),
                    (1, 0, 0, 0),
                    (0, 0, 0, 1),
                }
            )
        )
        assert len(markings) <= 12
        for marking in markings:
            marking_checks += 1
            beta = shifted_mod(alpha, canonical, marking, prime)
            pure = mode_three_map_mod(alpha, beta, prime)
            for distinguished in range(4):
                assert any(row[distinguished] for row in pure)
                rows = extension_rows_mod(distinguished, alpha, beta, prime)
                mixed = rows[1:15]
                diagonal_alpha = rows[0]
                diagonal_beta = rows[15]
                mixed_rank = rank_mod(mixed, prime)
                alpha_open = rank_mod(mixed + [diagonal_alpha], prime) > mixed_rank
                beta_open = rank_mod(mixed + [diagonal_beta], prime) > mixed_rank
                # Over F_11, two proper hyperplanes cannot cover a nonzero
                # kernel.  Hence both functionals being nonzero on the kernel
                # is equivalent to a simultaneous genuine-open vector.
                genuine_exists = alpha_open and beta_open
                expected = expected_marking(
                    distinguished, p_value, q_value, marking, prime
                )
                assert genuine_exists == expected, (
                    p_value,
                    q_value,
                    distinguished,
                    marking,
                    genuine_exists,
                    expected,
                )
                if not genuine_exists:
                    continue
                incidence_markings[distinguished] += 1
                sample_incidence[distinguished] += 1
                retained = [index for index in range(4) if index != distinguished]
                kernel = nullspace_mod(mixed, prime)
                extension = first_genuine_kernel_vector(
                    kernel, diagonal_alpha, diagonal_beta, prime
                )
                assert extension is not None
                alpha_extended = [
                    [alpha[mode][index] for index in retained] + [extension[mode]]
                    for mode in range(4)
                ]
                beta_extended = [
                    [beta[mode][index] for index in retained] + [extension[4 + mode]]
                    for mode in range(4)
                ]
                neighbouring = mode_three_map_mod(alpha_extended, beta_extended, prime)
                assert rank_mod(neighbouring, prime) == 4
                extension_directions[distinguished] += 1
                sample_directions[distinguished] += 1
        sample_results.append(
            {
                "label": label,
                "parameter_sample": [p_value, q_value],
                "representative_markings_checked": len(markings),
                "incidence_markings_by_deletion": sample_incidence,
                "genuine_extension_witnesses_by_deletion": (sample_directions),
            }
        )
    return {
        "prime": prime,
        "normalized_base_samples": len(samples),
        "base_marking_pairs_checked": marking_checks,
        "samples": sample_results,
        "incidence_markings_by_deletion": incidence_markings,
        "genuine_extension_witnesses_checked_by_deletion": (extension_directions),
        "projection_zero_sets_matched": True,
        "neighbouring_mode_three_rank_four_on_checked_witnesses": True,
        "pure_transverse_column_nonzero_on_all_checked_markings": True,
        "characteristic_zero_inference_from_finite_field": False,
        "exhaustive_over_finite_normalized_sheet": False,
        "purpose": "tiny representative audit-only regression",
    }


def main() -> None:
    alpha, beta = bases()
    tensor = {
        word: sp.factor(
            permanent4(
                tuple(beta[mode] if word[mode] else alpha[mode] for mode in range(4))
            )
        )
        for word in WORDS4
    }
    normalized_open = (p + q) * (p - q + 1)
    assert sp.factor(tensor[(1, 1, 1, 1)] - 2 * normalized_open) == 0
    assert all(
        sp.factor(value) == 0 for word, value in tensor.items() if word != (1, 1, 1, 1)
    )
    pure = mode_three_map_from_cofactors(alpha, beta)
    exact = [
        exact_audit(distinguished, alpha, beta, pure) for distinguished in range(4)
    ]
    modular = finite_field_audit()
    print(
        json.dumps(
            {
                "status": "pass",
                "claim_label": "VERIFIED",
                "role": "independent cofactor reconstruction and modular regression audit",
                "primary_verifier_imported": False,
                "field_for_exact_checks": "characteristic zero",
                "exact_characteristic_zero_audits": exact,
                "finite_field_audit": modular,
                "finite_field_inference_used": False,
                "all_special_divisor_intersections_inside_open_audited": True,
                "intrinsic_boundary_p_minus_q_plus_one_closed": False,
                "normalization_boundary_p_plus_q_closed": False,
                "parameter_infinity_closed": False,
                "source_torus_or_projective_boundaries_closed": False,
                "singleton_sheet_closed": False,
                "weighted_H22_closed": False,
                "global_Krenn_Gu_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
