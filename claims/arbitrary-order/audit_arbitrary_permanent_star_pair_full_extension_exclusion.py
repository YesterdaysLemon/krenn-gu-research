"""Independent no-SymPy audit of the displayed star endpoint."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from krenn_gu.bootstrap import bootstrap

REPO_ROOT, HERE = bootstrap(__file__)

Scalar = int | Fraction
Vector = tuple[Scalar, ...]
Linear = tuple[int, int, int]
Quadratic = tuple[int, int, int, int, int, int]
Polynomial = dict[int, Fraction]

EDGES = tuple(combinations(range(4), 2))
FULL_MASK = (1 << 6) - 1

M1 = (-1, 1, 0, 1, 0, 0)
M2 = (1, -1, 0, 0, -1, 1)
D0 = (-1, 2, -1, 1, 0, 1)
D1 = (1, 0, -1, 0, -1, 0)
D2 = (0, 0, 0, 2, 0, 0)
SOURCE_QUADRATICS = {"m1": M1, "m2": M2, "d0": D0, "d1": D1, "d2": D2}
CHANNELS = tuple(SOURCE_QUADRATICS)


@dataclass(frozen=True)
class Artifact:
    """One dependency file pinned by content and Git blob."""

    role: str
    path: str
    sha256: str
    blob: str


@dataclass(frozen=True)
class Package:
    """One hostile-reviewed dependency package."""

    name: str
    commit: str
    artifacts: tuple[Artifact, ...]


PACKAGES = (
    Package(
        "two_sided",
        "ca21e1d32c2e00a228d5be8050e57badd95f73d4",
        (
            Artifact(
                "theorem",
                "claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md",
                "76AEBB661CA3E89DF3E4228954B0D7CB3D736414A4AB22C2EBC9A2C84A774D62",
                "29d6874fad7057122ece6a4bad2a60ce3f89c836",
            ),
            Artifact(
                "primary",
                "claims/arbitrary-order/verify_arbitrary_permanent_star_pair_two_sided_projection_drop.py",
                "223B61126635FE59987B75684CFA6FCA1173737913CEAD0F46D98AA3A8C3DF1B",
                "037c730d7e95c2b95597b8400232ed723b63baac",
            ),
            Artifact(
                "audit",
                "claims/arbitrary-order/audit_arbitrary_permanent_star_pair_two_sided_projection_drop.py",
                "CD4D833DB7CB132FCFED02A0BD2353799E184DAC3DFAC9EC5F714F998F614311",
                "f9867fb2c03a3a5cda2b40a743bed9fef32f7edc",
            ),
            Artifact(
                "review",
                "docs/audits/ARBITRARY_PERMANENT_STAR_PAIR_TWO_SIDED_PROJECTION_DROP_REVIEW_2026-08-15.md",
                "F0C61339191FDD02C6F72F721C175636DC4A302554C71FF51C8809747D30203F",
                "c47ded42913e03a7dde7562ec9333b3b58e6cf02",
            ),
        ),
    ),
    Package(
        "kernel",
        "985f1a4cd49508da067ba1b4d788b2e576368448",
        (
            Artifact(
                "theorem",
                "claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md",
                "2B44641806EEE9B14D2F9DCC692C2E8E1CB9917832A9C2FD9E658243ACFE51F5",
                "c6da76f7c05de49a923120d83e931d0e94b1a4e8",
            ),
            Artifact(
                "primary",
                "claims/arbitrary-order/verify_arbitrary_permanent_star_pair_kernel_support_boundary.py",
                "73406FF9C62A2113341BBC97E36E2E4F4151CF399E72EEBFD831A05944744124",
                "98c0c18d9e4548040ca1f75e3b11e0e319a80d1c",
            ),
            Artifact(
                "audit",
                "claims/arbitrary-order/audit_arbitrary_permanent_star_pair_kernel_support_boundary.py",
                "0D4F649C78577158E39577FB5CBDDA1A0057534E75A803F1EB73F25726DA5721",
                "44e26a0f87ece8d37dbf51c2f7e89e155c86a633",
            ),
            Artifact(
                "review",
                "docs/audits/ARBITRARY_PERMANENT_STAR_PAIR_KERNEL_SUPPORT_BOUNDARY_REVIEW_2026-08-15.md",
                "EC573CB950EFBCB9DFE300DBCEBDCE9992E6DF839EF77A45C038E605EA925A45",
                "3282fda7525aa36c0ac30d0506518dee26bccb29",
            ),
        ),
    ),
    Package(
        "same_mode_boundary",
        "85e49d1100b6b77b610b07744ac377eb291691e7",
        (
            Artifact(
                "theorem",
                "claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_PAIR_SAME_MODE_NONCOMMON_AND_SUPPORT_TWO_BOUNDARY_THEOREM.md",
                "27AA460A9846A3568F3160DF3F6A03C798E87696D1A6E22900F13F8A76EF5AD9",
                "bcfb433dd3d4022be83ec09d43d0b4008560b298",
            ),
            Artifact(
                "primary",
                "claims/arbitrary-order/verify_arbitrary_permanent_star_pair_same_mode_noncommon_and_support_two_boundary.py",
                "0D24DC727902A18824B5D5470542F5BDF7E87FDAB4C5D5FEBE5C439CCE4FFAEA",
                "bb0ac965729742e316de620819b89397ef0197de",
            ),
            Artifact(
                "audit",
                "claims/arbitrary-order/audit_arbitrary_permanent_star_pair_same_mode_noncommon_and_support_two_boundary.py",
                "E849C2F5A3D0A14414156F70DC7A58CF62B332585A4271268EB54B705719F543",
                "d9070888749620e95533db24fbe8ec21160d5e0d",
            ),
            Artifact(
                "review",
                "docs/audits/ARBITRARY_PERMANENT_STAR_PAIR_SAME_MODE_NONCOMMON_AND_SUPPORT_TWO_BOUNDARY_REVIEW_2026-08-15.md",
                "FB85A20E79B35020FECD790A6A9B5B2922F12B2D699C50052967AF434C164E82",
                "910ce207f2004d52f4e851d501e6e4022f132688",
            ),
        ),
    ),
    Package(
        "same_mode",
        "4541cce432f621b9954251a0454f820cef500aac",
        (
            Artifact(
                "theorem",
                "claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_PAIR_SINGLETON_NN_EXCLUSION_THEOREM.md",
                "EA29D52F17100A7D99F5A56254309B69BC21744E5C2BAFE78A981F19097B4693",
                "3ca61522b4ede881e53fdd08d9d914bf72b56cea",
            ),
            Artifact(
                "primary",
                "claims/arbitrary-order/verify_arbitrary_permanent_star_pair_singleton_nn_exclusion.py",
                "CED670F3D48B567CBC62B4759718E056E21A5E21CB1F42DDA85426F502A4B0FE",
                "f26d073c5bbf60d0f850ed488854b3b6b0a55286",
            ),
            Artifact(
                "audit",
                "claims/arbitrary-order/audit_arbitrary_permanent_star_pair_singleton_nn_exclusion.py",
                "8ADCB1EAF9B4E3C5B140463AEC89615DBE323A385DC3893030F57C10ECAFA031",
                "5953ae1325e90fa35584f203990233bcefe2204d",
            ),
            Artifact(
                "review",
                "docs/audits/ARBITRARY_PERMANENT_STAR_PAIR_SINGLETON_NN_EXCLUSION_REVIEW_2026-08-15.md",
                "271D2C87D4F76FDF3541816183A40E83A3E7B5B8F9379FDEB6FC584188122535",
                "9cdfb41d6798a45d67f32a7c332589e77688ed51",
            ),
        ),
    ),
    Package(
        "companion",
        "76240ca4becc1b58b9803ac1ec6a4db159c07d3c",
        (
            Artifact(
                "theorem",
                "claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_TRIANGLE_EXCEPTIONAL_COMPANION_PROPAGATION_THEOREM.md",
                "9C70842573B3DD02BE5AC9CC65B08047AF0C6877892EA816A5D89B2024ED36A3",
                "b75c8b3baf1f181129aac68020c51e038b4900b0",
            ),
            Artifact(
                "primary",
                "claims/arbitrary-order/verify_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py",
                "97177FE5D7A44821428AAED34707FAD30490D50D80163609A28FB3AE7BE663F0",
                "cd8fcab56f71e3833972103dac9498acd74b43d9",
            ),
            Artifact(
                "audit",
                "claims/arbitrary-order/audit_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py",
                "9DB62582D752C85F2E7AE8343EC806B95786C5693466ECFB3666C5F838A35289",
                "d0f44eb3cb6be8ff94d9981115f19ba7d5e8c44e",
            ),
            Artifact(
                "review",
                "docs/audits/ARBITRARY_PERMANENT_STAR_TRIANGLE_EXCEPTIONAL_COMPANION_PROPAGATION_REVIEW_2026-08-15.md",
                "7BDFE90C91664B8A8AF5C3B6BFC8997F274D8EB4BCBF863757CD63E81DC30300",
                "c858dd723a0035262fedf9c61fa62c706b089bfb",
            ),
        ),
    ),
)

CYCLES = {
    "B0": {
        "p": (1, 0, 1, 0),
        "allowed": (1, 2),
        "q": (-1, 0, 1, 0),
        "e": 0,
        "r_p": (0, -1, 0, 1, -1),
        "r_q": (0, 0, 1, 0, 0),
        "ell": (0, -2, 0, -2),
        "relation": (-1, 1, 1, -1, 1),
        "kernel_basis": ((1, 0, 0, 0), (0, 0, 1, 0), (0, 1, 0, -1)),
    },
    "C0": {
        "p": (1, -1, 0, 0),
        "allowed": (0, 2),
        "q": (1, 1, 0, 0),
        "e": 1,
        "r_p": (0, 1, -1, 0, -1),
        "r_q": (0, 0, 0, 1, 0),
        "ell": (0, 0, -2, 0),
        "relation": (-3, -1, 1, 0, 1),
        "kernel_basis": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1)),
    },
    "B1": {
        "p": (1, 0, 0, 1),
        "allowed": (0, 2),
        "q": (-1, 0, 0, 1),
        "e": 1,
        "r_p": (-3, 0, 1, 0, 1),
        "r_q": (0, 0, 0, 1, 0),
        "ell": (0, 0, 2, 0),
        "relation": (-3, -1, 1, 0, 1),
        "kernel_basis": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1)),
    },
    "C1": {
        "p": (1, 1, 1, 1),
        "allowed": (1, 2),
        "q": (-1, 1, 1, 1),
        "e": 0,
        "r_p": (-1, 0, 0, 1, 1),
        "r_q": (-2, 0, 1, 0, 0),
        "ell": (0, -2, 0, 2),
        "relation": (-1, -1, 0, 1, 1),
        "kernel_basis": ((1, 0, 0, 0), (0, 0, 1, 0), (0, 1, 0, 1)),
    },
}


def digest(data: bytes) -> str:
    """Return an uppercase SHA-256 digest."""
    return hashlib.sha256(data).hexdigest().upper()


def git_bytes(*arguments: str) -> bytes:
    """Run Git and return stdout bytes."""
    result = subprocess.run(
        ("git", *arguments),
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def git_success(*arguments: str) -> bool:
    """Return whether one quiet Git query succeeds."""
    return subprocess.run(
        ("git", *arguments),
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def audit_git_objects() -> dict[str, object]:
    """Check current bytes, pinned commits, and Git blobs independently."""
    report: dict[str, object] = {}
    for package in PACKAGES:
        resolved = git_bytes("rev-parse", f"{package.commit}^{{commit}}").decode().strip()
        assert resolved == package.commit
        assert git_success("merge-base", "--is-ancestor", package.commit, "HEAD")
        artifacts = {}
        for artifact in package.artifacts:
            committed = git_bytes("show", f"{package.commit}:{artifact.path}")
            current = (REPO_ROOT / artifact.path).read_bytes().replace(b"\r\n", b"\n")
            blob = git_bytes("rev-parse", f"{package.commit}:{artifact.path}").decode().strip()
            assert committed == current
            assert digest(committed) == artifact.sha256
            assert blob == artifact.blob
            artifacts[artifact.role] = {"sha256": artifact.sha256, "blob": blob}
        report[package.name] = {"commit": resolved, "artifacts": artifacts}
    return report


def artifact_text(package_name: str, role: str) -> str:
    """Read a dependency only after its independent pins are known."""
    package = next(package for package in PACKAGES if package.name == package_name)
    artifact = next(artifact for artifact in package.artifacts if artifact.role == role)
    return (REPO_ROOT / artifact.path).read_text(encoding="utf-8")


def audit_dependency_boundaries() -> dict[str, object]:
    """Check the four accepted interfaces and review scope fences."""
    two_sided = artifact_text("two_sided", "theorem")
    kernel = artifact_text("kernel", "theorem")
    same_mode_boundary = artifact_text("same_mode_boundary", "theorem")
    same_mode = artifact_text("same_mode", "theorem")
    companion = artifact_text("companion", "theorem")
    assert "min_(2<=t<=5) rank(Phi_1|L_t) <= 2" in two_sided
    assert "min_(2<=t<=5) rank(Phi_2|L_t) <= 2" in two_sided
    assert "rank(Phi_k|L_t)>=2" in kernel
    assert "Phi_1: N=x_1+x_2" in kernel
    assert "Phi_2: N=x_1+x_2" in kernel
    assert "same-mode common/noncommon line pairs:                  EXCLUDED;" in same_mode_boundary
    assert "same-mode proportional N/N, support two:                EXCLUDED;" in same_mode_boundary
    assert "same-mode low for both displayed star projections:       EXCLUDED;" in same_mode
    for token in (
        "x_2-x_0 / {0}",
        "x_0+x_1 / {1}",
        "x_3-x_0 / {1}",
        "-x_0+x_1+x_2+x_3 / {0}",
    ):
        assert token in companion

    reviews = {}
    for package in PACKAGES:
        review = artifact_text(package.name, "review")
        assert "**PASS," in review
        assert "UNRESOLVED" in review
        reviews[package.name] = "PASS"
    return {
        "two_sided_drop": True,
        "rank_floor_and_six_lines": True,
        "same_mode_boundary_and_completion": True,
        "four_companion_arrows": True,
        "reviews": reviews,
    }


def first_four_product(left: Vector, right: Vector) -> Vector:
    """Multiply two forms in four-variable square-free edge order."""
    return tuple(
        left[first] * right[second] + left[second] * right[first]
        for first, second in EDGES
    )


def rational_rank(rows: list[list[Scalar]]) -> int:
    """Return exact row rank by standalone Fraction elimination."""
    matrix = [[Fraction(value) for value in row] for row in rows]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot_value for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scalar = matrix[row][column]
            matrix[row] = [
                matrix[row][index] - scalar * matrix[pivot_row][index]
                for index in range(len(matrix[0]))
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def complement_core_matrix(quadratic: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    """Build a complementary quadratic core independently."""
    matrix = [[0] * 4 for _ in range(4)]
    vertices = set(range(4))
    for coefficient, edge in zip(quadratic, EDGES, strict=True):
        first, second = sorted(vertices - set(edge))
        matrix[first][second] += coefficient
        matrix[second][first] += coefficient
    return tuple(tuple(row) for row in matrix)


CORES = {
    name: complement_core_matrix(quadratic)
    for name, quadratic in SOURCE_QUADRATICS.items()
}


def matrix_vector(matrix: tuple[tuple[int, ...], ...], vector: Vector) -> Vector:
    """Multiply a four-by-four matrix and vector."""
    return tuple(
        sum((row[index] * vector[index] for index in range(4)), 0)
        for row in matrix
    )


def double_contract(name: str, first: Vector, second: Vector) -> Scalar:
    """Contract a core in two distinct slots."""
    row = matrix_vector(CORES[name], first)
    return sum((row[index] * second[index] for index in range(4)), 0)


def vector_combination(values: tuple[Vector, ...], coefficients: Vector) -> Vector:
    """Form an exact vector combination."""
    return tuple(
        sum((coefficients[index] * values[index][coordinate] for index in range(len(values))), 0)
        for coordinate in range(len(values[0]))
    )


def audit_cycle_and_relation_tables() -> dict[str, object]:
    """Reconstruct all cycle scalars and hyperplane relations."""
    u = ((-1, 0, 1, 0), (1, 0, 0, -1), (0, 1, -1, 0))
    v = ((1, 1, -1, 1), (1, 1, 0, 0), (0, -1, 1, 0))
    products = tuple(tuple(first_four_product(left, right) for right in v) for left in u)
    assert products[0][1] == M1
    assert products[1][0] == M2
    assert products[0][0] == D0
    assert products[1][1] == D1
    assert products[2][2] == D2
    assert rational_rank([list(entry) for row in products for entry in row]) == 5

    expected_relation_matrices = {
        "B0": ((0, 2, 0, 2), (2, 0, 0, 0), (0, 0, 0, 0), (2, 0, 0, 0)),
        "C0": ((0, 0, 1, 0), (0, 0, -1, 0), (1, -1, 0, 1), (0, 0, 1, 0)),
        "B1": ((0, 0, 1, 0), (0, 0, -1, 0), (1, -1, 0, 1), (0, 0, 1, 0)),
        "C1": ((0, -1, 0, 1), (-1, 0, -1, 0), (0, -1, 0, 1), (1, 0, 1, 0)),
    }
    report = {}
    for name, data in CYCLES.items():
        p_rows = tuple(matrix_vector(CORES[channel], data["p"]) for channel in CHANNELS)
        q_rows = tuple(matrix_vector(CORES[channel], data["q"]) for channel in CHANNELS)
        assert vector_combination(p_rows, data["r_p"]) == data["ell"]
        assert vector_combination(q_rows, data["r_q"]) == data["ell"]
        allowed = data["allowed"]
        companion = data["e"]
        assert set(allowed) | {companion} == {0, 1, 2}
        assert all(data["r_p"][2 + colour] for colour in allowed)
        assert data["r_q"][2 + companion] == 1

        relation_matrix = tuple(
            tuple(
                sum(
                    data["relation"][index] * CORES[channel][row][column]
                    for index, channel in enumerate(CHANNELS)
                )
                for column in range(4)
            )
            for row in range(4)
        )
        assert relation_matrix == expected_relation_matrices[name]
        basis = data["kernel_basis"]
        assert all(sum(data["ell"][index] * vector[index] for index in range(4)) == 0 for vector in basis)
        assert rational_rank([list(vector) for vector in basis]) == 3
        assert all(
            sum(
                left[row] * relation_matrix[row][column] * right[column]
                for row in range(4)
                for column in range(4)
            )
            == 0
            for left in basis
            for right in basis
        )
        unused = tuple(data["relation"][2 + colour] for colour in allowed)
        assert all(unused)
        report[name] = {"ell": data["ell"], "unused_coefficients": unused}
    return {"source_rank": 5, "cycles": report}


def square_free_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply in the six-variable square-free algebra."""
    result: Polynomial = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = result.get(mask, Fraction(0)) + left_value * right_value
    return {mask: value for mask, value in result.items() if value}


def quartic_coefficient(quadratic: tuple[int, ...], vectors: tuple[Vector, ...]) -> Fraction:
    """Extract the full square-free coefficient of q times four forms."""
    polynomial: Polynomial = {
        (1 << first) | (1 << second): Fraction(value)
        for value, (first, second) in zip(quadratic, EDGES, strict=True)
        if value
    }
    for vector in vectors:
        linear = {
            1 << index: Fraction(value)
            for index, value in enumerate(vector)
            if value
        }
        polynomial = square_free_multiply(polynomial, linear)
    return polynomial.get(FULL_MASK, Fraction(0))


def unit(dimension: int, index: int) -> tuple[int, ...]:
    """Return a standard basis vector."""
    return tuple(int(position == index) for position in range(dimension))


def j_form(left: Vector, right: Vector) -> Scalar:
    """Evaluate the x4,x5 hyperbolic form."""
    return left[4] * right[5] + left[5] * right[4]


def audit_basis_factorizations() -> dict[str, int]:
    """Exhaust the two full-quartic factorizations by multilinearity."""
    basis6 = tuple(unit(6, index) for index in range(6))
    rank_three_checks = 0
    rank_two_checks = 0
    for data in CYCLES.values():
        hyperplane_basis = tuple((*vector, 0, 0) for vector in data["kernel_basis"])
        for name, quadratic in SOURCE_QUADRATICS.items():
            for first, second, third, fourth in product(
                hyperplane_basis,
                hyperplane_basis,
                basis6,
                basis6,
            ):
                actual = quartic_coefficient(quadratic, (first, second, third, fourth))
                expected = double_contract(name, first[:4], second[:4]) * j_form(third, fourth)
                assert actual == expected
                rank_three_checks += 1
            for first, second, third, fourth in product(
                basis6,
                basis6,
                hyperplane_basis,
                hyperplane_basis,
            ):
                actual = quartic_coefficient(quadratic, (first, second, third, fourth))
                expected = j_form(first, second) * double_contract(name, third[:4], fourth[:4])
                assert actual == expected
                rank_two_checks += 1
    expected_count = len(CYCLES) * len(CHANNELS) * 3 * 3 * 6 * 6
    assert rank_three_checks == rank_two_checks == expected_count
    return {"rank_three_entries": rank_three_checks, "rank_two_entries": rank_two_checks}


def p_xuv(first: Vector, second: Vector, third: Vector) -> Scalar:
    """Evaluate the full polarization of XUV."""
    return (
        first[0] * (second[1] * third[2] + second[2] * third[1])
        + first[1] * (second[0] * third[2] + second[2] * third[0])
        + first[2] * (second[0] * third[1] + second[1] * third[0])
    )


def multiply_linear(left: Linear, right: Linear) -> Quadratic:
    """Multiply forms in order X^2,XU,XV,U^2,UV,V^2."""
    x1, u1, v1 = left
    x2, u2, v2 = right
    return (
        x1 * x2,
        x1 * u2 + u1 * x2,
        x1 * v2 + v1 * x2,
        u1 * u2,
        u1 * v2 + v1 * u2,
        v1 * v2,
    )


def subtract_quadratic(left: Quadratic, right: Quadratic) -> Quadratic:
    """Subtract formal quadratic coefficient tuples."""
    return tuple(left[index] - right[index] for index in range(6))  # type: ignore[return-value]


def audit_formal_xuv() -> dict[str, object]:
    """Derive the annihilator/rank-one minors without symbolic software."""
    basis = tuple(unit(3, index) for index in range(3))
    formal_matrix: tuple[tuple[Linear, ...], ...] = tuple(
        tuple(
            tuple(int(p_xuv(basis[row], basis[column], basis[coefficient])) for coefficient in range(3))
            for column in range(3)
        )
        for row in range(3)
    )
    zero, x, u, v = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)
    assert formal_matrix == ((zero, v, u), (v, zero, x), (u, x, zero))
    minors = []
    for first, second in ((0, 1), (0, 2), (1, 2)):
        diagonal = multiply_linear(formal_matrix[first][first], formal_matrix[second][second])
        off = multiply_linear(formal_matrix[first][second], formal_matrix[second][first])
        minors.append(subtract_quadratic(diagonal, off))
    expected = (
        (0, 0, 0, 0, 0, -1),
        (0, 0, 0, -1, 0, 0),
        (-1, 0, 0, 0, 0, 0),
    )
    assert tuple(minors) == expected
    diagonal_lines = [
        [int(row == column == colour) for row in range(3) for column in range(3)]
        for colour in range(3)
    ]
    assert rational_rank(diagonal_lines) == 3
    return {"formal_matrix": formal_matrix, "principal_minors": expected, "diagonal_rank": 3}


def modular_rank(rows: list[list[int]], prime: int) -> int:
    """Return row rank over F_p."""
    matrix = [[value % prime for value in row] for row in rows]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], prime - 2, prime)
        matrix[pivot_row] = [value * inverse % prime for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scalar = matrix[row][column]
            matrix[row] = [
                (matrix[row][index] - scalar * matrix[pivot_row][index]) % prime
                for index in range(len(matrix[0]))
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def kappa_mod(first: Vector, second: Vector, prime: int) -> tuple[int, int, int]:
    """Evaluate kappa(first,second) over F_p."""
    basis = tuple(unit(3, index) for index in range(3))
    return tuple(int(p_xuv(test, first, second)) % prime for test in basis)


def audit_finite_annihilators(prime: int) -> dict[str, int]:
    """Search the singleton-slice annihilator step for a countermodel."""
    vectors = tuple(product(range(prime), repeat=3))
    nonzero = tuple(vector for vector in vectors if vector != (0, 0, 0))
    map_checks = 0
    for vector in nonzero:
        matrix = [list(kappa_mod(unit(3, column), vector, prime)) for column in range(3)]
        assert modular_rank(matrix, prime) >= 2
        map_checks += 1
    pair_checks = 0
    candidates = 0
    for first in nonzero:
        for second in nonzero:
            if modular_rank([list(first), list(second)], prime) != 2:
                continue
            pair_checks += 1
            common = [
                vector
                for vector in vectors
                if kappa_mod(vector, first, prime) == (0, 0, 0)
                and kappa_mod(vector, second, prime) == (0, 0, 0)
            ]
            assert common == [(0, 0, 0)]
            candidates += len(vectors)
    return {"nonzero_maps": map_checks, "independent_pairs": pair_checks, "candidates": candidates}


def audit_topology_and_scope() -> dict[str, object]:
    """Exhaust all low/support leaves and enforce endpoint scope."""
    leaves = []
    for name, data in CYCLES.items():
        first, second = data["allowed"]
        leaves.extend(((name, (first,)), (name, (second,)), (name, (first, second))))
    assert len(leaves) == 12
    assert {name for name, _support in leaves} == set(CYCLES)
    assert all(set(support) <= set(CYCLES[name]["allowed"]) for name, support in leaves)

    endpoint = (HERE / "ARBITRARY_PERMANENT_STAR_PAIR_FULL_EXTENSION_EXCLUSION_THEOREM.md").read_text(
        encoding="utf-8"
    )
    required = (
        "exact extension of the displayed based frame (1):        EXCLUDED;",
        "all based-frame stabilizer orbits of unbased (4,1):      NOT CLASSIFIED;",
        "transport from (1) to every based (4,1) frame:           NOT PROVED;",
        "unbased (4,1) orbit universally excluded:                NOT PROVED;",
        "unrestricted P_6 -> Delta_3:                             UNKNOWN;",
        "global Krenn--Gu conjecture:                             UNRESOLVED.",
    )
    assert all(token in endpoint for token in required)
    assert "no exact extension from `P_6`" in endpoint
    return {"low_support_leaves": len(leaves), "survivors": 0, "scope_tokens": len(required)}


def main() -> None:
    """Run the independent audit."""
    git_objects = audit_git_objects()
    boundaries = audit_dependency_boundaries()
    cycles = audit_cycle_and_relation_tables()
    factorizations = audit_basis_factorizations()
    xuv = audit_formal_xuv()
    finite = {prime: audit_finite_annihilators(prime) for prime in (3, 5)}
    topology = audit_topology_and_scope()
    print("star-pair displayed-frame full-extension exclusion independent audit: PASS")
    print(f"  Git-object dependency audit: {git_objects}")
    print(f"  accepted dependency boundaries: {boundaries}")
    print(f"  standalone cycle/core tables: {cycles}")
    print(f"  basis-exhaustive full factorizations: {factorizations}")
    print(f"  formal XUV gates: {xuv}")
    print(f"  finite-field countermodel searches: {finite}")
    print(f"  proof topology and scope: {topology}")


if __name__ == "__main__":
    main()
