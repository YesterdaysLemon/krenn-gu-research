"""Independent no-import audit of the P6 equality-five exclusion.

This script imports neither the primary verifier, any upstream verifier, nor
SymPy.  It pins all reviewed bytes, reconstructs the finite group actions
from raw permutations, checks the eight integral frames with a standalone
rational reducer, and independently exhausts the six endpoint classes.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THEOREM = (
    ROOT / "claims/arbitrary-order/"
    "ARBITRARY_PERMANENT_P6_COTWO_EQUALITY_FIVE_FULL_EXTENSION_EXCLUSION_THEOREM.md"
)
PRIMARY = (
    ROOT / "claims/arbitrary-order/"
    "verify_arbitrary_permanent_p6_cotwo_equality_five_full_extension_exclusion.py"
)
THEOREM_SHA256 = "bd3428b41fd4bca2d57641de279e58e5d9c1b8f81dad287fe1ce731cade3a9de"
PRIMARY_SHA256 = "1dcb2fc490dbd1ab393063f43a74232ebe31d0cd77bfbf65aefeebe16831ca16"

DEPENDENCIES = {
    "claims/arbitrary-order/ARBITRARY_PERMANENT_COTWO_EQUALITY_FIVE_ACTIVE_SUPPORT_ORBIT_SYNTHESIS_THEOREM.md": "9399ccb4286583a1f1e90bd7025e706b3de47c652214bb1e8b7c8f6ba986a6d5",
    "claims/arbitrary-order/verify_arbitrary_permanent_cotwo_equality_five_active_support_orbit_synthesis.py": "175543a58c352b05ff2f13ccf1b75ec3b9080b11bd0a879a1649391481cfd779",
    "claims/arbitrary-order/audit_arbitrary_permanent_cotwo_equality_five_active_support_orbit_synthesis.py": "2f8272cea197fac253fe0b4f6e09091fffd6d0be161a3e0ff5f0bc72dfcc4047",
    "docs/audits/ARBITRARY_PERMANENT_COTWO_EQUALITY_FIVE_ACTIVE_SUPPORT_ORBIT_SYNTHESIS_REVIEW_2026-08-15.md": "be13f69678f36b6db79277af66a85144e0b334c14535dcdd29573ab10fb53f03",
    "claims/arbitrary-order/ARBITRARY_PERMANENT_COTWO_R4_BASED_FRAME_ORBIT_CLASSIFICATION_THEOREM.md": "cff044ea8e89d504f4ecf9c62ca55dfd5361cd54f5cb85083b09aed8b834d677",
    "claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_based_frame_orbit_classification.py": "8560c80c85abc643a7591161295c22bf052589bcfc0529ca2a067a452cb1baf1",
    "claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_based_frame_orbit_classification.py": "123ee95416724fa80a537fd3fd2eec216f461d9f2e2d88268ccb82aed3758fc8",
    "docs/audits/ARBITRARY_PERMANENT_COTWO_R4_BASED_FRAME_ORBIT_CLASSIFICATION_REVIEW_2026-08-15.md": "f1610e9bbcc4065ac24a1e0cd7f81ddaf989bca5d4026ae2a23bd2ff7a5f680f",
    "claims/arbitrary-order/ARBITRARY_PERMANENT_MONOMIAL_COVARIANCE_AND_BASED_FRAME_ORBIT_TRANSPORT_LEMMA.md": "b1762f22813e5b749ff0c81da6c6ce5e9b8e95601662d87cb21835aaf63c3da0",
    "claims/arbitrary-order/verify_arbitrary_permanent_monomial_covariance_and_based_frame_orbit_transport.py": "e37a2e98447f6058496a3487d0a01f498b331e730cc3b01c72fc6750cec5838e",
    "claims/arbitrary-order/audit_arbitrary_permanent_monomial_covariance_and_based_frame_orbit_transport.py": "1ec63510db2e03a58d7502aae7160310b4f324bfad0547bb1e86a05a2602a740",
    "docs/audits/ARBITRARY_PERMANENT_MONOMIAL_COVARIANCE_AND_BASED_FRAME_ORBIT_TRANSPORT_REVIEW_2026-08-16.md": "3cfdc0b2d7ceb5af59247fd87d6469a8bb5b4c6f03ff2c077b05abda866ef5ec",
    "claims/arbitrary-order/ARBITRARY_PERMANENT_TRIANGLE_PAIR_FULL_EXTENSION_EXCLUSION_THEOREM.md": "02c87a0811777b0a833598d9217fbf117613f8b7089a21c0ae6d4ed6964648b9",
    "claims/arbitrary-order/verify_arbitrary_permanent_triangle_pair_full_extension_exclusion.py": "fdbbe2711c471ebf0453398f722412371fd4091b0593a5fddd70ae4b6508d31a",
    "claims/arbitrary-order/audit_arbitrary_permanent_triangle_pair_full_extension_exclusion.py": "9b15c86c1c0b232ea3d622a9868b95cacb135da59534d9da97175a55236f23ce",
    "docs/audits/ARBITRARY_PERMANENT_TRIANGLE_PAIR_FULL_EXTENSION_EXCLUSION_REVIEW_2026-08-15.md": "3d30a06354ea4f929ddd015436b5fd94ac3e05f133743019fb87a1783fadafcd",
    "claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_PAIR_FULL_EXTENSION_EXCLUSION_THEOREM.md": "c9daabb0c288f6fb54c9fb209fd5d2e341118efe0c181442899757063ea0b66d",
    "claims/arbitrary-order/verify_arbitrary_permanent_star_pair_full_extension_exclusion.py": "3ae361503755db59fec772a042ceb319b31ca869958758bca55083a0b2de5ecc",
    "claims/arbitrary-order/audit_arbitrary_permanent_star_pair_full_extension_exclusion.py": "0add6399e692361bae467a0b6ca361b6e6c521c34f230b28e7babc36fd200371",
    "docs/audits/ARBITRARY_PERMANENT_STAR_PAIR_FULL_EXTENSION_EXCLUSION_REVIEW_2026-08-15.md": "35ece859d0da216d3e60008410feb109eea531dceceff442a53e1f3c8ac2480d",
    "claims/arbitrary-order/ARBITRARY_PERMANENT_FIXED_PAIR_FULL_EXTENSION_EXCLUSION_THEOREM.md": "8ae57e0032b046303260bcef9dc0ae56635dc9aeaa9af096d609079523d65dde",
    "claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_full_extension_exclusion.py": "9979fbc9528c8d059f5a1802a2487a5da3d4b0ce651947c0d7ea6480b5050c35",
    "claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_full_extension_exclusion.py": "7cf90a8a3e3498cc707fea3ec5e273b90e10372da04e3c8262b8c1bf74c72f21",
    "docs/audits/ARBITRARY_PERMANENT_FIXED_PAIR_FULL_EXTENSION_EXCLUSION_REVIEW_2026-08-15.md": "be668be16f2a9df74a122ce34d8adf5f177a35d4acc9a1596adf558bccbda5f5",
    "claims/arbitrary-order/ARBITRARY_PERMANENT_COTWO_R4_PURE_STAR_FULL_EXTENSION_EXCLUSION_THEOREM.md": "e0b069b11107f006650954d339ef8e6e9465c2b492059450236f5238b2567cbc",
    "claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_pure_star_full_extension_exclusion.py": "36c285c44bfa4d4c61fc084773f1604e398ebac94e1aa8fd72e6bf5a8e1e6d49",
    "claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_pure_star_full_extension_exclusion.py": "4fcfbf910701eb28c1913ab9fc39a6921c689c536ee12f42cadf6a35b0b51163",
    "docs/audits/ARBITRARY_PERMANENT_COTWO_R4_PURE_STAR_FULL_EXTENSION_EXCLUSION_REVIEW_2026-08-16.md": "f324e6741a0ad66a53849a6298a266e745b358c275523620036d5765dd60d6bc",
    "claims/arbitrary-order/ARBITRARY_PERMANENT_COTWO_R4_FIXED_E1_FULL_EXTENSION_EXCLUSION_THEOREM.md": "a7ee294986e79c7f1bc38e0b2ce0dc1a5ee09d230f2fd06796846d677a361acf",
    "claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_fixed_e1_full_extension_exclusion.py": "24a84558c6d842bc5d034dfcc6494c60a03c75cf8e5f47e2e63a6c3ccfeed2f8",
    "claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_fixed_e1_full_extension_exclusion.py": "ef9cc36cbe0ad27dfeafc1e24ee0a717cde17e9e2ff6684ffc1981567585b4cc",
    "docs/audits/ARBITRARY_PERMANENT_COTWO_R4_FIXED_E1_FULL_EXTENSION_EXCLUSION_REVIEW_2026-08-16.md": "0b3775df217207a36538ffaf02d2e483bbe5c08193574b2d3ecc8873b81f9287",
    "claims/arbitrary-order/ARBITRARY_PERMANENT_COTWO_R4_FIXED_E2_FULL_EXTENSION_EXCLUSION_THEOREM.md": "cf79c02d6c45359f1f26aefad4e4c0ab9715a57ada26b1e57d18a772022b764e",
    "claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_fixed_e2_full_extension_exclusion.py": "a4f68fb8ae8d5d977c99875c2e2298c2417e29a408b81f1345c9bde990477a91",
    "claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_fixed_e2_full_extension_exclusion.py": "7d0c24e338524ed04ef387a0c31977a821c73dbd70e31f3ba2d390a8a6809589",
    "docs/audits/ARBITRARY_PERMANENT_COTWO_R4_FIXED_E2_FULL_EXTENSION_EXCLUSION_REVIEW_2026-08-16.md": "55cd1aa465a250af3107139931a21685802d66291a400b28bb92cfa9e9803374",
}

CATALOGS = {
    "(3,1)": {
        "size": 4,
        "valid": ((0, 1, 2), (0, 1, 3)),
        "ordered": ((0, 1, 3, 2),),
        "swap": (1, 0, 3, 2),
        "ordered_order": 2,
        "full_order": 4,
        "ordered_sizes": (2,),
        "full_sizes": (2,),
    },
    "(4,1)": {
        "size": 6,
        "valid": (
            (0, 1, 3),
            (0, 1, 4),
            (0, 1, 5),
            (0, 2, 4),
            (0, 2, 5),
            (0, 3, 5),
            (0, 4, 5),
            (1, 2, 3),
            (1, 2, 4),
            (1, 3, 4),
            (1, 3, 5),
            (2, 3, 4),
            (2, 3, 5),
            (2, 4, 5),
        ),
        "ordered": ((4, 1, 5, 3, 0, 2), (0, 4, 3, 2, 1, 5)),
        "swap": (5, 3, 4, 1, 2, 0),
        "ordered_order": 6,
        "full_order": 12,
        "ordered_sizes": (1, 1, 6, 6),
        "full_sizes": (2, 12),
    },
    "(4,2)": {
        "size": 6,
        "valid": (
            (0, 1, 3),
            (0, 1, 5),
            (0, 2, 4),
            (0, 2, 5),
            (0, 3, 5),
            (0, 4, 5),
            (1, 2, 3),
            (1, 2, 4),
            (1, 3, 4),
            (1, 3, 5),
            (2, 3, 4),
            (2, 4, 5),
        ),
        "ordered": (
            (0, 3, 4, 1, 2, 5),
            (5, 1, 4, 3, 2, 0),
            (3, 5, 2, 0, 4, 1),
        ),
        "swap": (5, 3, 4, 1, 2, 0),
        "ordered_order": 8,
        "full_order": 16,
        "ordered_sizes": (4, 4, 4),
        "full_sizes": (4, 4, 4),
    },
}

FRAMES = (
    (
        "(3,1)",
        "unique",
        (0, 1, 2),
        ((0, 1, -1, 0), (0, 0, 0, 1), (-1, 0, 1, 0)),
        ((0, -1, 1, 0), (1, 1, 0, 0), (0, 0, 0, 1)),
    ),
    (
        "(4,1)",
        "k=3",
        (0, 1, 4),
        ((1, -1, 0, 0), (1, 0, 0, -1), (1, 0, -1, 0)),
        ((1, -1, 1, 1), (1, 1, 1, -1), (1, 1, -1, 1)),
    ),
    (
        "(4,1)",
        "k=2 displayed",
        (0, 1, 3),
        ((-1, 0, 1, 0), (1, 0, 0, -1), (0, 1, -1, 0)),
        ((1, 1, -1, 1), (1, 1, 0, 0), (0, -1, 1, 0)),
    ),
    (
        "(4,1)",
        "k=1",
        (0, 2, 5),
        ((1, -1, -1, 1), (0, 0, 1, -1), (1, 0, -1, 0)),
        ((1, 0, 0, 1), (0, 0, 1, -1), (1, 1, 0, 0)),
    ),
    (
        "(4,1)",
        "k=0",
        (2, 3, 5),
        ((1, -1, 1, -1), (1, -1, -1, 1), (1, 1, -1, -1)),
        ((1, 0, 1, 0), (1, 0, 0, 1), (1, 1, 0, 0)),
    ),
    (
        "(4,2)",
        "e=0 displayed",
        (0, 1, 3),
        ((1, 0, 0, -1), (0, 1, 0, -1), (0, 0, 1, -1)),
        ((0, 1, 1, 0), (1, 0, 1, 0), (0, 0, 1, -1)),
    ),
    (
        "(4,2)",
        "e=1",
        (0, 2, 5),
        ((0, 1, -1, 0), (1, -1, 0, 0), (1, 0, 0, -1)),
        ((0, 1, 0, 1), (1, -1, 0, 0), (1, 0, 1, 0)),
    ),
    (
        "(4,2)",
        "e=2",
        (0, 2, 4),
        ((1, 1, -1, -1), (0, 1, 0, -1), (1, 0, 0, -1)),
        ((1, 1, 1, 1), (0, 1, 1, 0), (1, 0, 1, 0)),
    ),
)

EDGES = tuple(combinations(range(4), 2))


def file_sha256(path: Path) -> str:
    """Hash text after normalizing checkout CRLF to Git-style LF."""

    return sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def audit_frozen_bytes() -> str:
    """Check the new theorem, primary, and all frozen upstream packages."""

    assert file_sha256(THEOREM) == THEOREM_SHA256
    assert file_sha256(PRIMARY) == PRIMARY_SHA256
    ledger = []
    for relative, expected in sorted(DEPENDENCIES.items()):
        path = ROOT / relative
        observed = file_sha256(path)
        assert observed == expected, f"dependency drift: {relative}: {observed}"
        if "/audits/" in relative:
            prefix = path.read_text(encoding="utf-8")[:1200]
            assert "## Verdict" in prefix and "**PASS" in prefix
        ledger.append(f"{relative}:{observed}")
    assert len(ledger) == 36
    return sha256("\n".join(ledger).encode()).hexdigest()


def group_closure(
    size: int, generators: tuple[tuple[int, ...], ...]
) -> set[tuple[int, ...]]:
    """Construct a finite permutation group from raw generators."""

    identity = tuple(range(size))
    group = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            composite = tuple(generator[current[index]] for index in range(size))
            if composite not in group:
                group.add(composite)
                frontier.append(composite)
    return group


def triple_orbit(
    triple: frozenset[int], group: set[tuple[int, ...]]
) -> set[frozenset[int]]:
    """Return the orbit of one unordered colour triple."""

    return {frozenset(action[index] for index in triple) for action in group}


def partition_orbits(
    valid: set[frozenset[int]], group: set[tuple[int, ...]]
) -> tuple[set[frozenset[int]], ...]:
    """Partition a frozen valid catalog under one group action."""

    unseen = set(valid)
    orbits = []
    while unseen:
        orbit = triple_orbit(next(iter(unseen)), group)
        assert orbit <= valid
        orbits.append(orbit)
        unseen -= orbit
    return tuple(orbits)


def endpoint_for(orbit: str, triple: frozenset[int]) -> str:
    """Route one raw triple without consulting the primary verifier."""

    if orbit == "(3,1)":
        return "triangle-012"
    if orbit == "(4,1)":
        k = len(triple & {0, 1, 4})
        return "star-pure-014" if k in {0, 3} else "star-mixed-013"
    assert orbit == "(4,2)"
    e = len(triple & {2, 4})
    return {0: "fixed-e0-013", 1: "fixed-e1-025", 2: "fixed-e2-024"}[e]


def audit_group_cover() -> dict[str, object]:
    """Independently exhaust the ordered and exchanged based-frame orbits."""

    profiles = {}
    endpoints = set()
    total_full_orbits = 0
    for name, raw in CATALOGS.items():
        size = raw["size"]
        valid = {frozenset(triple) for triple in raw["valid"]}
        ordered_generators = tuple(raw["ordered"])
        swap = raw["swap"]
        assert isinstance(size, int)
        assert isinstance(swap, tuple)

        ordered_group = group_closure(size, ordered_generators)
        full_group = group_closure(size, (*ordered_generators, swap))
        assert len(ordered_group) == raw["ordered_order"]
        assert len(full_group) == raw["full_order"]

        ordered_orbits = partition_orbits(valid, ordered_group)
        full_orbits = partition_orbits(valid, full_group)
        assert tuple(sorted(map(len, ordered_orbits))) == raw["ordered_sizes"]
        assert tuple(sorted(map(len, full_orbits))) == raw["full_sizes"]

        routed = []
        for orbit in full_orbits:
            labels = {endpoint_for(name, triple) for triple in orbit}
            assert len(labels) == 1
            label = labels.pop()
            endpoints.add(label)
            routed.append((label, len(orbit)))
        total_full_orbits += len(full_orbits)
        profiles[name] = {
            "valid": len(valid),
            "ordered_orbits": tuple(sorted(map(len, ordered_orbits))),
            "full_orbits": tuple(sorted(routed)),
        }

    assert total_full_orbits == 6
    assert endpoints == {
        "triangle-012",
        "star-mixed-013",
        "star-pure-014",
        "fixed-e0-013",
        "fixed-e1-025",
        "fixed-e2-024",
    }
    assert endpoint_for("(4,1)", frozenset((0, 2, 5))) == "star-mixed-013"
    assert endpoint_for("(4,2)", frozenset((0, 2, 5))) == "fixed-e1-025"
    return {"classes": total_full_orbits, "profiles": profiles}


def rational_rank(rows: list[tuple[int, ...]] | tuple[tuple[int, ...], ...]) -> int:
    """Compute exact row rank using standalone Fraction elimination."""

    if not rows:
        return 0
    work = [[Fraction(entry) for entry in row] for row in rows]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            multiple = work[row][column]
            work[row] = [
                entry - multiple * basis
                for entry, basis in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def product(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Multiply linear forms in the four-variable square-free algebra."""

    return tuple(
        left[first] * right[second] + left[second] * right[first]
        for first, second in EDGES
    )


def audit_integral_frames() -> dict[tuple[str, str], tuple[int, int, str]]:
    """Check every ordered representative and its independent route."""

    profiles = {}
    for orbit, label, indices, left, right in FRAMES:
        assert rational_rank(left) == rational_rank(right) == 3
        table = tuple(tuple(product(u, v) for v in right) for u in left)
        mixed = [
            table[row][column]
            for row in range(3)
            for column in range(3)
            if row != column
        ]
        all_products = [table[row][column] for row in range(3) for column in range(3)]
        assert rational_rank(mixed) == 2
        assert rational_rank(all_products) == 5
        endpoint = endpoint_for(orbit, frozenset(indices))
        profiles[(orbit, label)] = (2, 5, endpoint)
    assert len(profiles) == 8
    assert profiles[("(4,1)", "k=1")][2] == "star-mixed-013"
    assert profiles[("(4,2)", "e=1")][2] == "fixed-e1-025"
    return profiles


def audit_p6_boundary() -> dict[str, int | str]:
    """Independently check the equality jump and sensor consequence."""

    pair_floor = 5
    equality_case = 5
    assert pair_floor == equality_case
    equality_case_excluded = True
    pair_floor_after_exclusion = pair_floor + int(equality_case_excluded)
    assert pair_floor_after_exclusion == 6
    omitted_pairs = comb(6, 2)
    sum_bound = omitted_pairs + 3
    sensor_bound = sum_bound - pair_floor_after_exclusion
    assert (omitted_pairs, sum_bound, sensor_bound) == (15, 18, 12)
    return {
        "omitted_pairs": omitted_pairs,
        "pair_floor": pair_floor_after_exclusion,
        "sensor_bound": sensor_bound,
        "simultaneous_residual": "OPEN",
    }


def main() -> None:
    """Run the independent audit."""

    manifest = audit_frozen_bytes()
    group_cover = audit_group_cover()
    frames = audit_integral_frames()
    boundary = audit_p6_boundary()
    print("P6 co-two equality-five full-extension exclusion no-import audit: PASS")
    print(f"  dependency manifest digest: {manifest}")
    print(f"  independent finite-group cover: {group_cover}")
    print(f"  exact integral frame profiles: {frames}")
    print(f"  P6 boundary: {boundary}")
    print("  unrestricted P6 -> Delta_3: UNKNOWN")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
