"""Primary exact composition replay for the P6 equality-five exclusion.

The characteristic-zero proof is the accompanying theorem document.  This
script pins all reviewed inputs, invokes the exact based-frame and transport
replays, and checks that the complete orbit census is covered by six endpoint
packages.
"""

from __future__ import annotations

from hashlib import sha256
from math import comb
from pathlib import Path

import verify_arbitrary_permanent_cotwo_r4_based_frame_orbit_classification as based
import verify_arbitrary_permanent_monomial_covariance_and_based_frame_orbit_transport as transport

ROOT = Path(__file__).resolve().parents[2]

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

EXPECTED_ENDPOINTS = {
    "triangle-012",
    "star-mixed-013",
    "star-pure-014",
    "fixed-e0-013",
    "fixed-e1-025",
    "fixed-e2-024",
}


def file_sha256(path: Path) -> str:
    """Hash text after normalizing checkout CRLF to Git-style LF."""

    return sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def verify_frozen_dependencies() -> str:
    """Reject drift in any theorem, verifier, audit, or hostile review."""

    ledger = []
    for relative, expected in sorted(DEPENDENCIES.items()):
        path = ROOT / relative
        observed = file_sha256(path)
        assert observed == expected, f"dependency drift: {relative}: {observed}"
        if "/audits/" in relative:
            prefix = path.read_text(encoding="utf-8")[:1200]
            assert "## Verdict" in prefix
            assert "**PASS" in prefix
        ledger.append(f"{relative}:{observed}")
    assert len(ledger) == 36
    return sha256("\n".join(ledger).encode()).hexdigest()


def endpoint_for(orbit: str, triple: tuple[int, int, int]) -> str:
    """Route one admissible based frame to its reviewed endpoint class."""

    selected = set(triple)
    if orbit == "(3,1)":
        return "triangle-012"
    if orbit == "(4,1)":
        k = len(selected & {0, 1, 4})
        assert k in {0, 1, 2, 3}
        return "star-pure-014" if k in {0, 3} else "star-mixed-013"
    assert orbit == "(4,2)"
    e = len(selected & {2, 4})
    return {0: "fixed-e0-013", 1: "fixed-e1-025", 2: "fixed-e2-024"}[e]


def verify_exact_upstream_replays() -> dict[str, object]:
    """Re-run the exact characteristic-zero catalogs and covariance checks."""

    catalog_profiles = {
        data.name: based.verify_catalog_and_actions(data) for data in based.orbit_data()
    }
    data_by_name = {data.name: data for data in based.orbit_data()}
    frame_profiles = {
        (frame.orbit, frame.label): based.verify_frame(frame, data_by_name[frame.orbit])
        for frame in based.frames()
    }
    assert len(frame_profiles) == 8

    transport.verify_frozen_inputs_and_boundary()
    transport_profiles = {
        "permanent": transport.verify_symbolic_permanent_covariance(),
        "complement": transport.verify_symbolic_complement_covariance(),
        "colours_and_modes": transport.verify_colour_and_mode_transport(),
    }
    return {
        "catalogs": catalog_profiles,
        "frames": frame_profiles,
        "transport": transport_profiles,
    }


def verify_complete_orbit_cover() -> dict[str, object]:
    """Exhaust every valid triple and every omitted-mode exchange orbit."""

    profiles: dict[str, object] = {}
    observed_endpoints: set[str] = set()
    total_full_orbits = 0
    for data in based.orbit_data():
        valid = {frozenset(triple) for triple in data.valid_triples}
        full_group = based.group_closure(
            len(data.points), (*data.ordered_generators, data.swap_generator)
        )
        unseen = set(valid)
        endpoint_orbits = []
        while unseen:
            seed = tuple(sorted(next(iter(unseen))))
            orbit = based.triple_orbit(seed, full_group)
            assert orbit <= valid
            endpoints = {
                endpoint_for(data.name, tuple(sorted(triple))) for triple in orbit
            }
            assert len(endpoints) == 1
            endpoint = endpoints.pop()
            observed_endpoints.add(endpoint)
            endpoint_orbits.append((endpoint, len(orbit)))
            unseen -= orbit
        assert sum(size for _, size in endpoint_orbits) == len(valid)
        assert len(endpoint_orbits) == len(data.swap_representatives)
        total_full_orbits += len(endpoint_orbits)
        profiles[data.name] = tuple(sorted(endpoint_orbits))

    assert observed_endpoints == EXPECTED_ENDPOINTS
    assert total_full_orbits == 6

    representative_routes = {
        (frame.orbit, frame.label): endpoint_for(frame.orbit, frame.point_indices)
        for frame in based.frames()
    }
    assert representative_routes == {
        ("(3,1)", "unique"): "triangle-012",
        ("(4,1)", "k=3"): "star-pure-014",
        ("(4,1)", "k=2 displayed"): "star-mixed-013",
        ("(4,1)", "k=1"): "star-mixed-013",
        ("(4,1)", "k=0"): "star-pure-014",
        ("(4,2)", "e=0 displayed"): "fixed-e0-013",
        ("(4,2)", "e=1"): "fixed-e1-025",
        ("(4,2)", "e=2"): "fixed-e2-024",
    }
    return {
        "full_exchange_orbits": total_full_orbits,
        "profiles": profiles,
        "representative_routes": representative_routes,
    }


def verify_p6_consequence() -> dict[str, int]:
    """Check the integer jump and complementary sensor arithmetic."""

    source_modes = 6
    omitted_pairs = comb(source_modes, 2)
    equality_dimension = 5
    assert omitted_pairs == 15
    assert equality_dimension + 1 == 6
    pair_lower_bound = equality_dimension + 1
    sensor_sum_bound = comb(source_modes, 2) + 3
    sensor_upper_bound = sensor_sum_bound - pair_lower_bound
    assert sensor_sum_bound == 18
    assert sensor_upper_bound == 12
    return {
        "omitted_pairs": omitted_pairs,
        "pair_dimension_lower_bound": pair_lower_bound,
        "sensor_sum_bound": sensor_sum_bound,
        "sensor_dimension_upper_bound": sensor_upper_bound,
    }


def main() -> None:
    """Run the exact synthesis replay."""

    manifest = verify_frozen_dependencies()
    upstream = verify_exact_upstream_replays()
    cover = verify_complete_orbit_cover()
    consequence = verify_p6_consequence()
    print("P6 co-two equality-five full-extension exclusion primary: PASS")
    print(f"  frozen reviewed files: {len(DEPENDENCIES)}")
    print(f"  dependency manifest digest: {manifest}")
    print(f"  exact upstream replay: {upstream}")
    print(f"  exhaustive endpoint cover: {cover}")
    print(f"  P6 consequence: {consequence}")
    print("  dimension-at-least-six simultaneous residual: OPEN")
    print("  unrestricted P6 -> Delta_3: UNKNOWN")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
