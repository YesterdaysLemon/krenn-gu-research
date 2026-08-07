#!/usr/bin/env python3
"""Verify the mixed-orientation sixth pure-P4 component."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
from pathlib import Path

import sympy as sp


import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
THEOREM = HERE / "P4_MIXED_ORIENTATION_PURE_COMPONENT.md"
KNOWN_FIRST = REPO_ROOT / "claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_THEOREM.md"
KNOWN_SECOND = (
    REPO_ROOT / "claims" / "p4" / "components" / "diagonal-quadric"
    / "P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md")
KNOWN_THREE = REPO_ROOT / "P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md"
RADICAL_STAR = (
    REPO_ROOT / "claims" / "p4" / "classifications" / "star"
    / "radical-star" / "P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md")
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
PAIRS = tuple(itertools.combinations(range(4), 2))
PIVOTS = ((0, 2), (0, 2), (0, 1), (0, 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def coefficients(
    planes: tuple[sp.Matrix, ...],
) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: sp.factor(
            permanent(
                tuple(planes[mode].row(word[mode]) for mode in range(4))
            )
        )
        for word in WORDS
    }


def contraction_covectors(
    a: sp.Expr,
    c: sp.Expr,
    d: sp.Expr,
    p: sp.Expr,
    q: sp.Expr,
) -> sp.Matrix:
    mode_rows = (
        (
            sp.Matrix([0, 0, 1, 1]),
            sp.Matrix([a, 1, c, d]),
        ),
        (
            sp.Matrix([p, 1, 0, q]),
            sp.Matrix([-1, 0, 1, 0]),
        ),
        (
            sp.Matrix([1, 0, 1, 0]),
            sp.Matrix([0, 0, -1, 1]),
        ),
    )
    identity = sp.eye(4)
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        if bits == (0, 0, 0):
            continue
        rows.append(
            tuple(
                permanent(
                    (
                        identity.row(coordinate),
                        mode_rows[0][bits[0]].T,
                        mode_rows[1][bits[1]].T,
                        mode_rows[2][bits[2]].T,
                    )
                )
                for coordinate in range(4)
            )
        )
    return sp.Matrix(rows)


def family_planes(
    d: sp.Expr,
    p: sp.Expr,
    q: sp.Expr,
    scales: tuple[sp.Expr, sp.Expr, sp.Expr] = (1, 1, 1),
) -> tuple[sp.Matrix, ...]:
    N = q * (d + p + q)
    planes = (
        sp.Matrix(((-d * p, d + q, N, 0), (d * p, -d - q, 0, N))),
        sp.Matrix(((0, 0, 1, 1), (-d, 1, -p - q, d))),
        sp.Matrix(((p, 1, 0, q), (-1, 0, 1, 0))),
        sp.Matrix(((1, 0, 1, 0), (0, 0, -1, 1))),
    )
    source_scale = sp.diag(*scales, 1)
    return tuple(plane * source_scale for plane in planes)


def p3_family_planes(
    d: sp.Expr,
    p: sp.Expr,
    q: sp.Expr,
) -> tuple[sp.Matrix, ...]:
    N = q * (d + p + q)
    return (
        sp.Matrix(((-N, -d - q, d * p, 0), (N, d + q, 0, d * p))),
        sp.Matrix(((0, 0, 1, 1), (-d - p - q, 1, 0, d))),
        sp.Matrix(((p, 1, 0, q), (-1, 0, 1, 0))),
        sp.Matrix(((1, 0, 1, 0), (0, 0, -1, 1))),
    )


def reduce_in_charts(
    planes: tuple[sp.Matrix, ...],
) -> tuple[tuple[sp.Matrix, ...], tuple[sp.Expr, ...]]:
    reduced = []
    coordinates = []
    for plane, pivots in zip(planes, PIVOTS, strict=True):
        chart = sp.simplify(plane[:, pivots].inv() * plane)
        nonpivots = tuple(index for index in range(4) if index not in pivots)
        reduced.append(chart)
        coordinates.extend(
            chart[row, column]
            for row in range(2)
            for column in nonpivots
        )
    return tuple(reduced), tuple(coordinates)


def chart_planes(variables: tuple[sp.Symbol, ...]) -> tuple[sp.Matrix, ...]:
    result = []
    for mode, pivots in enumerate(PIVOTS):
        nonpivots = tuple(index for index in range(4) if index not in pivots)
        plane = sp.zeros(2, 4)
        plane[0, pivots[0]] = 1
        plane[1, pivots[1]] = 1
        entries = variables[4 * mode : 4 * mode + 4]
        for row in range(2):
            for offset, column in enumerate(nonpivots):
                plane[row, column] = entries[2 * row + offset]
        result.append(plane)
    return tuple(result)


def product_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    columns = []
    for left_row in range(2):
        for right_row in range(2):
            columns.append(
                sp.Matrix(
                    tuple(
                        left[left_row, first] * right[right_row, second]
                        + left[left_row, second] * right[right_row, first]
                        for first, second in PAIRS
                    )
                )
            )
    return sp.Matrix.hstack(*columns)


def pair_data(
    planes: tuple[sp.Matrix, ...],
) -> dict[tuple[int, int], tuple[int, tuple[int, ...]]]:
    result = {}
    for left, right in PAIRS:
        matrix = product_matrix(planes[left], planes[right])
        result[left, right] = (
            matrix.rank(),
            tuple(
                sp.Matrix(2, 2, tuple(vector)).rank()
                for vector in matrix.nullspace()
            ),
        )
    return result


def pure_kernel_lines(
    planes: tuple[sp.Matrix, ...],
) -> tuple[sp.Matrix, ...]:
    tensor = coefficients(planes)
    result = []
    for mode in range(4):
        factor = None
        for word in WORDS:
            zero = list(word)
            one = list(word)
            zero[mode] = 0
            one[mode] = 1
            values = tensor[tuple(zero)], tensor[tuple(one)]
            if values != (0, 0):
                factor = values
                break
        assert factor is not None
        first, second = factor
        result.append(
            sp.simplify(
                second * planes[mode].row(0)
                - first * planes[mode].row(1)
            )
        )
    return tuple(result)


def proportional(left: sp.Matrix, right: sp.Matrix) -> bool:
    return sp.Matrix.vstack(left, right).rank() == 1


def directed_relation_signature(
    planes: tuple[sp.Matrix, ...],
) -> tuple[int, int, tuple[int, ...]]:
    kernels = pure_kernel_lines(planes)
    indegrees = [0] * 4
    rank_one = 0
    rank_two = 0
    for (left, right), (image_rank, relation_ranks) in pair_data(
        planes
    ).items():
        if image_rank != 3:
            continue
        if relation_ranks == (2,):
            rank_two += 1
            continue
        if relation_ranks != (1,):
            continue
        rank_one += 1
        relation = product_matrix(
            planes[left], planes[right]
        ).nullspace()[0]
        matrix = sp.Matrix(2, 2, tuple(relation))
        pivot = next(
            (row, column)
            for row in range(2)
            for column in range(2)
            if matrix[row, column] != 0
        )
        row, column = pivot
        left_factor = matrix[:, column]
        right_factor = matrix[row, :] / matrix[row, column]
        left_vector = left_factor.T * planes[left]
        right_vector = right_factor * planes[right]
        if proportional(left_vector, kernels[left]):
            indegrees[left] += 1
        if proportional(right_vector, kernels[right]):
            indegrees[right] += 1
    return rank_one, rank_two, tuple(sorted(indegrees, reverse=True))


def diagonal_quadric_space(plane: sp.Matrix) -> tuple[sp.Matrix, ...]:
    first, second = plane.nullspace()
    restriction = sp.Matrix(
        (
            tuple(first[index] ** 2 for index in range(4)),
            tuple(
                2 * first[index] * second[index] for index in range(4)
            ),
            tuple(second[index] ** 2 for index in range(4)),
        )
    )
    return tuple(restriction.nullspace())


def jump_signature(planes: tuple[sp.Matrix, ...]) -> tuple[int, int]:
    two_two = 0
    one_three = 0
    for plane in planes:
        quadrics = diagonal_quadric_space(plane)
        if len(quadrics) == 1:
            continue
        assert len(quadrics) == 2
        if any(
            all(vector[index] == 0 for vector in quadrics)
            for index in range(4)
        ):
            one_three += 1
        else:
            two_two += 1
    return two_two, one_three


def singular_command() -> list[str]:
    native = shutil.which("Singular")
    if native:
        return [native, "-q"]
    wsl = shutil.which("wsl.exe")
    if wsl:
        return [wsl, "--exec", "/usr/bin/Singular", "-q"]
    raise RuntimeError("Singular is required for the exact decomposition")


def verify_minimal_primes(minors: tuple[sp.Expr, ...]) -> None:
    expression = lambda value: str(sp.expand(value)).replace("**", "^")
    expected = (
        ("c+p+q", "a+d"),
        ("d+q", "a+c+p"),
        ("c", "a+d+p+q"),
        ("c-d+p-q", "a"),
        ("c-d", "a+p-q"),
    )
    lines = [
        'LIB "primdec.lib";',
        "ring r=0,(a,c,d,p,q),dp;",
        f"ideal I={','.join(expression(value) for value in minors)};",
        "ideal R=radical(I);",
    ]
    for index, generators in enumerate(expected):
        lines.append(f"ideal P{index}={','.join(generators)};")
    lines.append("ideal J=P0;")
    for index in range(1, len(expected)):
        lines.append(f"J=intersect(J,P{index});")
    lines.extend(
        (
            "R=std(R); J=std(J);",
            "ideal A=simplify(reduce(R,J),2);",
            "ideal B=simplify(reduce(J,R),2);",
            "list L=minAssGTZ(R);",
            "int equal=(size(A)==0 && size(B)==0);",
            (
                '"CODEX_RESULT:"+string(dim(R))+":"'
                '+string(size(L))+":"+string(equal);'
            ),
        )
    )
    completed = subprocess.run(
        singular_command(),
        input="\n".join(lines) + "\n",
        text=True,
        capture_output=True,
        timeout=300,
        check=False,
    )
    assert completed.returncode == 0
    assert not completed.stderr.strip()
    assert "?" not in completed.stdout
    result = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.strip().startswith("CODEX_RESULT:")
    ]
    assert result == ["CODEX_RESULT:3:5:1"], completed.stdout


def known_samples() -> dict[str, tuple[sp.Matrix, ...]]:
    a, d, e, h, n = map(sp.Integer, (2, 3, 5, 7, 11))
    cap_d = d + h * n * e
    first = (
        sp.Matrix(((1, 0, a, h * (a - n)), (0, 1, cap_d / h, d))),
        sp.Matrix(((e, 1, 0, 0), (0, 0, 1, h))),
        sp.Matrix(((0, 1, 0, h * n * e), (-1 / n, 0, 1, 0))),
        sp.Matrix(((1, 0, n, 0), (0, 0, -1 / h, 1))),
    )
    second = (
        sp.Matrix(((2, -1, -1, -2), (1, -1, 1, 1))),
        sp.Matrix(((1, 0, 0, -1), (1, 1, -1, 1))),
        sp.Matrix(((3, 1, 1, -1), (0, 1, -1, 0))),
        sp.Matrix(((1, 0, 0, 1), (0, 1, 1, 0))),
    )
    one_three = {
        "L1": (1, 3, 4, 2),
        "L2": (1, 3, 4, 6),
        "L3": (1, 2, 3, -6),
    }
    result = {"first": first, "second": second}
    for branch, (S, D, G, T) in one_three.items():
        P = G - T
        Q = D - S
        result[branch] = (
            sp.Matrix(((2, P + Q, Q - P, 0), (0, 0, 1, 1))),
            sp.Matrix(((0, 1, -1, 0), (1, 0, S, D))),
            sp.Matrix(((1, 0, G, T), (0, 1, 0, -1))),
            sp.Matrix(((0, 1, 1, 0), (0, 1, 0, 1))),
        )
    return result


def main() -> None:
    a, c, d, p, q = sp.symbols("a c d p q")
    contractions = contraction_covectors(a, c, d, p, q)
    nonzero_rows = tuple(
        index for index in range(7) if any(contractions.row(index))
    )
    assert nonzero_rows == (3, 4, 6)
    core = contractions[list(nonzero_rows), :]
    minors = tuple(
        sp.factor(core[:, columns].det())
        for columns in itertools.combinations(range(4), 3)
    )
    verify_minimal_primes(minors)

    D, P, Q = sp.symbols("D P Q")
    planes = family_planes(D, P, Q)
    tensor = coefficients(planes)
    expected = 2 * Q * (D + P + Q)
    assert tensor[(0, 0, 0, 0)] == expected
    assert all(
        value == 0
        for word, value in tensor.items()
        if word != (0, 0, 0, 0)
    )

    t0, t1, t2 = sp.symbols("t0 t1 t2")
    family = family_planes(D, P, Q, (t0, t1, t2))
    _, family_coordinates = reduce_in_charts(family)
    family_variables = (D, P, Q, t0, t1, t2)
    base = {D: 1, P: 2, Q: 3, t0: 1, t1: 1, t2: 1}
    family_jacobian = sp.Matrix(family_coordinates).jacobian(
        family_variables
    ).subs(base)
    family_rows = (0, 1, 3, 4, 5)
    family_columns = (0, 1, 2, 3, 5)
    family_minor = family_jacobian.extract(
        family_rows, family_columns
    )
    assert family_jacobian.rank() == 5
    assert family_minor.det() == -sp.Rational(9, 2)

    sample = tuple(plane.subs(base) for plane in family)
    reduced_sample, sample_coordinates = reduce_in_charts(sample)
    sample_tensor = coefficients(reduced_sample)
    anchor = (1, 0, 1, 0)
    assert sample_tensor[anchor] != 0
    ratios = []
    for mode in range(4):
        opposite = list(anchor)
        opposite[mode] = 1 - opposite[mode]
        ratios.append(
            sp.simplify(
                sample_tensor[tuple(opposite)] / sample_tensor[anchor]
            )
        )
    assert ratios == [0, -sp.Rational(1, 5), 0, 0]

    chart_variables = sp.symbols("x0:16")
    target_variables = sp.symbols("z0:4")
    chart_tensor = coefficients(chart_planes(chart_variables))
    equations = []
    for word in WORDS:
        if word == anchor:
            continue
        product = 1
        for mode in range(4):
            if word[mode] != anchor[mode]:
                product *= target_variables[mode]
        equations.append(
            chart_tensor[word] - chart_tensor[anchor] * product
        )
    all_variables = chart_variables + target_variables
    substitution = {
        **dict(zip(chart_variables, sample_coordinates, strict=True)),
        **dict(zip(target_variables, ratios, strict=True)),
    }
    incidence_jacobian = sp.Matrix(equations).jacobian(
        all_variables
    ).subs(substitution)
    incidence_columns = (
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        12,
        14,
        16,
        18,
        19,
    )
    incidence_minor = incidence_jacobian[:, incidence_columns]
    assert incidence_jacobian.rank() == 15
    assert incidence_minor.det() == -737280

    sample_pair_data = pair_data(sample)
    assert tuple(
        sample_pair_data[pair][0] for pair in PAIRS
    ) == (4, 4, 3, 4, 3, 3)
    assert all(
        sample_pair_data[pair][1] == (1,)
        for pair in ((0, 3), (1, 3), (2, 3))
    )
    assert jump_signature(sample) == (0, 1)
    new_directed = directed_relation_signature(sample)
    assert new_directed == (3, 0, (2, 1, 0, 0))

    known = known_samples()
    known_directed = {
        name: directed_relation_signature(planes)
        for name, planes in known.items()
    }
    assert known_directed["first"] == (2, 1, (1, 1, 0, 0))
    assert known_directed["second"] == (2, 1, (1, 1, 0, 0))
    assert all(
        known_directed[branch] == (3, 0, (1, 1, 1, 0))
        for branch in ("L1", "L2", "L3")
    )

    # The P3 prime is a mode-(0,1) symmetry translate of P1.
    dprime = -Q * (D + P + Q) / (D + Q)
    p1 = family_planes(D, P, Q)
    p3 = p3_family_planes(dprime, P, Q)

    def same_plane(left: sp.Matrix, right: sp.Matrix) -> bool:
        left_pluecker = tuple(
            sp.factor(left[:, pair].det()) for pair in PAIRS
        )
        right_pluecker = tuple(
            sp.factor(right[:, pair].det()) for pair in PAIRS
        )
        pivot = next(
            index
            for index in range(6)
            if left_pluecker[index] != 0 and right_pluecker[index] != 0
        )
        return all(
            sp.factor(
                left_pluecker[index] * right_pluecker[pivot]
                - right_pluecker[index] * left_pluecker[pivot]
            )
            == 0
            for index in range(6)
        )

    swapped = (p1[1], p1[0], p1[2], p1[3])
    assert all(
        same_plane(left, right)
        for left, right in zip(swapped, p3, strict=True)
    )

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "mixed coordinate-pair zero products, exact determinantal "
            "decomposition, and smooth Segre-incidence certificate"
        ),
        "mixed_contraction_nonzero_rows": list(nonzero_rows),
        "rank_two_locus_dimension": 3,
        "rank_two_locus_minimal_primes": 5,
        "family_nonzero_coefficient": str(expected),
        "family_tangent_rank": family_jacobian.rank(),
        "family_minor_rows": list(family_rows),
        "family_minor_columns": [
            str(family_variables[index]) for index in family_columns
        ],
        "family_minor_determinant": str(family_minor.det()),
        "incidence_anchor": "1010",
        "incidence_target_ratios": [str(value) for value in ratios],
        "incidence_jacobian_rank": incidence_jacobian.rank(),
        "incidence_minor_columns": list(incidence_columns),
        "incidence_minor_determinant": int(incidence_minor.det()),
        "component_dimension": 5,
        "pair_profile": [4, 4, 3, 4, 3, 3],
        "jump_signature_two_two_one_three": [0, 1],
        "directed_relation_signature": {
            "rank_one_edges": new_directed[0],
            "rank_two_edges": new_directed[1],
            "sorted_kernel_endpoint_indegrees": list(new_directed[2]),
        },
        "known_component_directed_signatures": {
            name: {
                "rank_one_edges": signature[0],
                "rank_two_edges": signature[1],
                "sorted_kernel_endpoint_indegrees": list(signature[2]),
            }
            for name, signature in known_directed.items()
        },
        "P1_P3_mode_swap_birational_equivalence_verified": True,
        "known_pure_component_orbits_at_least": 6,
        "all_pure_components_classified": False,
        "H31_new_component_marked_fibre_excluded": False,
        "H22_excluded": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            path.name: sha256(path)
            for path in (KNOWN_FIRST, KNOWN_SECOND, KNOWN_THREE, RADICAL_STAR)
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / "tmp" / "p4_mixed_orientation_pure_component_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
