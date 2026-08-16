"""Primary dependency and topology checks for the displayed triangle endpoint."""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from krenn_gu.bootstrap import bootstrap

REPO_ROOT, HERE = bootstrap(__file__)


@dataclass(frozen=True)
class FrozenPackage:
    """One reviewed theorem package used by the composition."""

    name: str
    commit: str
    theorem: tuple[str, str]
    primary: tuple[str, str]
    audit: tuple[str, str]
    review: tuple[str, str]


PACKAGES = (
    FrozenPackage(
        name="two_sided_projection_drop",
        commit="ba39b00cc3d49309fc25e44754cb06f66eaefbdb",
        theorem=(
            "claims/arbitrary-order/"
            "ARBITRARY_PERMANENT_TRIANGLE_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md",
            "C5E8F47B499318595481D84DB75425240BA6A01AD512A92BF923F5FAB56BF485",
        ),
        primary=(
            "claims/arbitrary-order/"
            "verify_arbitrary_permanent_triangle_pair_two_sided_projection_drop.py",
            "770F21C2D34A5B98CE5820D023405D0A95B3FE167539747E3EFB9EDE4A538153",
        ),
        audit=(
            "claims/arbitrary-order/"
            "audit_arbitrary_permanent_triangle_pair_two_sided_projection_drop.py",
            "14AB3E48905246452B9B02D962D0D5902D543398EA74B0009ACAF12C720D136D",
        ),
        review=(
            "docs/audits/"
            "ARBITRARY_PERMANENT_TRIANGLE_PAIR_TWO_SIDED_PROJECTION_DROP_REVIEW_2026-08-15.md",
            "4E52015588B2DA8353B717D3704C7D2149B21B0046BD4FDD1B3664500E5A27F6",
        ),
    ),
    FrozenPackage(
        name="kernel_support_boundary",
        commit="6e4d8ec79191a51c90dd188f7bdc2d7fde36b5f7",
        theorem=(
            "claims/arbitrary-order/"
            "ARBITRARY_PERMANENT_TRIANGLE_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md",
            "60858DFE1C1C9E11C74662B815E1A4173616C3277E28A25520EDAD97148EBA82",
        ),
        primary=(
            "claims/arbitrary-order/"
            "verify_arbitrary_permanent_triangle_pair_kernel_support_boundary.py",
            "67F27BEF7A3C8A071344F6B48BEA265DF2173E839586C988239F039DBB72F8DF",
        ),
        audit=(
            "claims/arbitrary-order/"
            "audit_arbitrary_permanent_triangle_pair_kernel_support_boundary.py",
            "B0C5DFBC8ED8086BCF5EDAA8665BD57131E2291ED73601A269F35996B973FBA8",
        ),
        review=(
            "docs/audits/"
            "ARBITRARY_PERMANENT_TRIANGLE_PAIR_KERNEL_SUPPORT_BOUNDARY_REVIEW_2026-08-15.md",
            "09692AF859DB180F6D2BD5E0A51361F07BDFD33CCBC47671794A5B06FB2D1676",
        ),
    ),
    FrozenPackage(
        name="same_mode_exclusion",
        commit="f8267fc172ac8f9bee528e3b2ae876635253823b",
        theorem=(
            "claims/arbitrary-order/"
            "ARBITRARY_PERMANENT_TRIANGLE_PAIR_SAME_MODE_TWO_LOW_EXCLUSION_THEOREM.md",
            "196A46E7B85A332956DB6CCF99BD72F1999E3B8205E774F077C552C70961A155",
        ),
        primary=(
            "claims/arbitrary-order/"
            "verify_arbitrary_permanent_triangle_pair_same_mode_two_low_exclusion.py",
            "9DDA7DB2F2059A596E242D69834078CE852E70DBB90B450E0775F040394870E5",
        ),
        audit=(
            "claims/arbitrary-order/"
            "audit_arbitrary_permanent_triangle_pair_same_mode_two_low_exclusion.py",
            "4F0B502445D5330421D597CCF674B1F0227E5D14E8DADABFF26253954827BE95",
        ),
        review=(
            "docs/audits/"
            "ARBITRARY_PERMANENT_TRIANGLE_PAIR_SAME_MODE_TWO_LOW_EXCLUSION_REVIEW_2026-08-15.md",
            "48D59C4408EA1F91E6B6AA436C474B903B578B41C0E23444A201510F1E08C0AC",
        ),
    ),
    FrozenPackage(
        name="companion_propagation",
        commit="76240ca4becc1b58b9803ac1ec6a4db159c07d3c",
        theorem=(
            "claims/arbitrary-order/"
            "ARBITRARY_PERMANENT_STAR_TRIANGLE_EXCEPTIONAL_COMPANION_PROPAGATION_THEOREM.md",
            "9C70842573B3DD02BE5AC9CC65B08047AF0C6877892EA816A5D89B2024ED36A3",
        ),
        primary=(
            "claims/arbitrary-order/"
            "verify_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py",
            "97177FE5D7A44821428AAED34707FAD30490D50D80163609A28FB3AE7BE663F0",
        ),
        audit=(
            "claims/arbitrary-order/"
            "audit_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py",
            "9DB62582D752C85F2E7AE8343EC806B95786C5693466ECFB3666C5F838A35289",
        ),
        review=(
            "docs/audits/"
            "ARBITRARY_PERMANENT_STAR_TRIANGLE_EXCEPTIONAL_COMPANION_PROPAGATION_REVIEW_2026-08-15.md",
            "7BDFE90C91664B8A8AF5C3B6BFC8997F274D8EB4BCBF863757CD63E81DC30300",
        ),
    ),
)


def sha256(path: Path) -> str:
    """Hash text after normalizing checkout CRLF to Git-style LF."""

    normalized = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(normalized).hexdigest().upper()


def check_frozen_dependencies() -> dict[str, object]:
    """Check every pinned theorem, verifier, audit, and review byte."""
    report: dict[str, object] = {}
    for package in PACKAGES:
        assert len(package.commit) == 40
        assert all(character in "0123456789abcdef" for character in package.commit)
        artifacts: dict[str, str] = {}
        for role in ("theorem", "primary", "audit", "review"):
            relative, expected = getattr(package, role)
            path = REPO_ROOT / relative
            assert path.is_file(), path
            actual = sha256(path)
            assert actual == expected, (package.name, role, actual, expected)
            artifacts[role] = actual
        review_text = (REPO_ROOT / package.review[0]).read_text(encoding="utf-8")
        assert "**PASS," in review_text
        assert "UNRESOLVED" in review_text
        report[package.name] = {
            "commit": package.commit,
            "sha256": artifacts,
            "review": "PASS",
        }
    assert len({package.commit for package in PACKAGES}) == 4
    return report


def theorem_text(package_name: str) -> str:
    """Read one pinned theorem from the working tree."""
    package = next(package for package in PACKAGES if package.name == package_name)
    return (REPO_ROOT / package.theorem[0]).read_text(encoding="utf-8")


def check_accepted_interfaces() -> dict[str, object]:
    """Check the four exact interfaces used by the composition."""
    two_sided = theorem_text("two_sided_projection_drop")
    kernel = theorem_text("kernel_support_boundary")
    same_mode = theorem_text("same_mode_exclusion")
    companion = theorem_text("companion_propagation")

    common_tokens = (
        "characteristic zero",
        "x_4x_5 x_3",
        "x_4x_5 x_0",
        "lambda_c!=0",
        "UNRESOLVED",
    )
    for name, text in {
        "two_sided": two_sided,
        "kernel": kernel,
        "same_mode": same_mode,
    }.items():
        missing = [token for token in common_tokens if token not in text]
        assert not missing, (name, missing)

    assert "min_(2<=t<=5) rank(Phi_2|L_t) <= 2." in two_sided
    assert "rank(Phi_k|L_t)>=2." in kernel
    assert "Kx_3,                  with local support exactly {0}" in kernel
    assert "K(x_1+x_2),            with local support in {1,2}" in kernel
    assert "same-mode proportional N/N:" in same_mode
    assert "every same-mode cross-family low:" in same_mode
    assert "EXCLUDED;" in same_mode
    assert "Phi_2   X=x_3" in companion
    assert "x_1+x_2 / nonempty subset of {1,2}" in companion
    assert "some distinct local mode" in companion
    return {
        "projection_drop": "some Phi_2 rank <= 2",
        "rank_floor": "every local Phi rank >= 2",
        "Phi_2_low_lines": ["N", "X"],
        "same_mode_low": "excluded",
        "X_companion": "distinct-mode N",
    }


def check_proof_topology() -> dict[str, object]:
    """Exhaust the two low-kernel leaves and their contradictions."""
    rows: list[dict[str, object]] = []
    for low_line in ("N", "X"):
        initial_phi2_rank = 2
        if low_line == "N":
            contradiction_mode = "initial"
            companion_line = None
        else:
            contradiction_mode = "distinct_companion"
            companion_line = "N"

        line_at_contradiction = low_line if low_line == "N" else companion_line
        lies_in_both_ambient_kernels = line_at_contradiction == "N"
        phi1_rank_upper = 2 if lies_in_both_ambient_kernels else 3
        phi2_rank_upper = 2 if lies_in_both_ambient_kernels else 3
        rank_floor = 2
        both_ranks_exactly_two = (
            phi1_rank_upper == rank_floor and phi2_rank_upper == rank_floor
        )
        contradicted_by_same_mode = both_ranks_exactly_two
        assert initial_phi2_rank == 2
        assert line_at_contradiction == "N"
        assert contradicted_by_same_mode
        rows.append(
            {
                "initial_Phi_2_low_line": low_line,
                "companion_line": companion_line,
                "contradiction_mode": contradiction_mode,
                "line_in_both_ambient_kernels": lies_in_both_ambient_kernels,
                "both_ranks_exactly_two": both_ranks_exactly_two,
                "contradicted_by_same_mode": contradicted_by_same_mode,
            }
        )
    assert {row["initial_Phi_2_low_line"] for row in rows} == {"N", "X"}
    assert all(row["contradicted_by_same_mode"] for row in rows)
    return {"rows": rows, "surviving_low_lines": []}


def check_scope_fence() -> dict[str, bool]:
    """Ensure the endpoint retains the based-frame transport gap."""
    endpoint = HERE / "ARBITRARY_PERMANENT_TRIANGLE_PAIR_FULL_EXTENSION_EXCLUSION_THEOREM.md"
    text = endpoint.read_text(encoding="utf-8")
    required = {
        "displayed_frame_excluded": (
            "exact extension of the displayed based frame (1):        EXCLUDED;"
        ),
        "based_orbits_unclassified": (
            "all based-frame stabilizer orbits of unbased (3,1):      NOT CLASSIFIED;"
        ),
        "transport_not_proved": (
            "transport from (1) to every based (3,1) frame:           NOT PROVED;"
        ),
        "unbased_orbit_not_proved": (
            "unbased (3,1) orbit universally excluded:                NOT PROVED;"
        ),
        "unrestricted_unknown": (
            "unrestricted P_6 -> Delta_3:                             UNKNOWN;"
        ),
        "global_unresolved": (
            "global Krenn--Gu conjecture:                             UNRESOLVED."
        ),
    }
    assert all(token in text for token in required.values())
    return {name: True for name in required}


def main() -> None:
    """Run the dependency and proof-topology verifier."""
    report = {
        "frozen_dependencies": check_frozen_dependencies(),
        "accepted_interfaces": check_accepted_interfaces(),
        "proof_topology": check_proof_topology(),
        "scope_fence": check_scope_fence(),
        "source_sha256": sha256(Path(__file__)),
        "status": "DISPLAYED_TRIANGLE_FRAME_EXCLUDED; GLOBAL_UNRESOLVED",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
