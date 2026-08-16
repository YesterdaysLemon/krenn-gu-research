"""Primary dependency and topology checks for the fixed-pair endpoint."""

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
        name="distinct_two_low_reduction",
        commit="aa21e104645094b10830c5236210cd2961003579",
        theorem=(
            "claims/arbitrary-order/"
            "ARBITRARY_PERMANENT_FIXED_PAIR_DISTINCT_TWO_LOW_REDUCTION_THEOREM.md",
            "87BD9CCC45C07088465C27FB4032BCC34DDB7004789A3FC28ECA36F3BFA67D1E",
        ),
        primary=(
            "claims/arbitrary-order/"
            "verify_arbitrary_permanent_fixed_pair_distinct_two_low_reduction.py",
            "20ECAA638C7AFDFB11187925C76AA6DD9F142E63AE41AD5220F27FA70518290A",
        ),
        audit=(
            "claims/arbitrary-order/"
            "audit_arbitrary_permanent_fixed_pair_distinct_two_low_reduction.py",
            "F8A1350BD36DA6CFCEBCA674791F44B6DBCF00BD782F53B6319E609005658D56",
        ),
        review=(
            "docs/audits/"
            "ARBITRARY_PERMANENT_FIXED_PAIR_DISTINCT_TWO_LOW_REDUCTION_REVIEW_2026-08-15.md",
            "FA72305DCA86760A934736168D6FB8E9647A8FA8B6E5C5E66B2A008CD830FEA3",
        ),
    ),
    FrozenPackage(
        name="zero_branch_exclusion",
        commit="6daade565a5424b17ba272ef609b17271e4f8c4d",
        theorem=(
            "claims/arbitrary-order/"
            "ARBITRARY_PERMANENT_FIXED_PAIR_TWO_LOW_ZERO_BRANCH_EXCLUSION_THEOREM.md",
            "236065BB239059865C91105D49590693E5D9121DD1A0BBB365863A7667FCF0CA",
        ),
        primary=(
            "claims/arbitrary-order/"
            "verify_arbitrary_permanent_fixed_pair_two_low_zero_branch_exclusion.py",
            "85504804E6BF5A056C53E6E8FDD93B999AB56A0C2E63187E24C590840C58600D",
        ),
        audit=(
            "claims/arbitrary-order/"
            "audit_arbitrary_permanent_fixed_pair_two_low_zero_branch_exclusion.py",
            "7CB12A912E30C6A44AAC784CE6786E822106BA7A59E3EB396BE9DB33244CEDF6",
        ),
        review=(
            "docs/audits/"
            "ARBITRARY_PERMANENT_FIXED_PAIR_TWO_LOW_ZERO_BRANCH_EXCLUSION_REVIEW_2026-08-15.md",
            "83462F64188C6D8D0B6D4801779828CCA43CCA88F1896B6A5052D7A3A93BBA0A",
        ),
    ),
    FrozenPackage(
        name="E22_branch_exclusion",
        commit="7bc6e6bb1ff97080671a1ff9f53ea37fe96e02be",
        theorem=(
            "claims/arbitrary-order/"
            "ARBITRARY_PERMANENT_FIXED_PAIR_DISTINCT_TWO_LOW_E22_EXCLUSION_THEOREM.md",
            "925284C772176125855BF99199B6789E430355A0D4F87553E727CA746B206925",
        ),
        primary=(
            "claims/arbitrary-order/"
            "verify_arbitrary_permanent_fixed_pair_distinct_two_low_e22_exclusion.py",
            "00BA077A4F4023ECA875C2B9DD826D8FFC2690723CBA16B1C6737720A611E2FC",
        ),
        audit=(
            "claims/arbitrary-order/"
            "audit_arbitrary_permanent_fixed_pair_distinct_two_low_e22_exclusion.py",
            "0B640BF86F7C495821705D3489307ECA668BFD6951AF342B18665E2B577473B8",
        ),
        review=(
            "docs/audits/"
            "ARBITRARY_PERMANENT_FIXED_PAIR_DISTINCT_TWO_LOW_E22_EXCLUSION_REVIEW_2026-08-15.md",
            "1BD0A74E440342382981BC894316D2BA4E61F3438AC4CF659C0E90FD21B9CF05",
        ),
    ),
)


def sha256(path: Path) -> str:
    """Hash text after normalizing checkout CRLF to Git-style LF."""

    normalized = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(normalized).hexdigest().upper()


def check_frozen_dependencies() -> dict[str, object]:
    """Verify every pinned theorem, implementation, audit, and review byte."""
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
            assert actual == expected
            artifacts[role] = actual
        review_text = (REPO_ROOT / package.review[0]).read_text(encoding="utf-8")
        assert "**PASS," in review_text
        assert "No mathematical" in review_text or "blocker survived hostile review" in review_text
        report[package.name] = {"commit": package.commit, "sha256": artifacts, "review": "PASS"}
    assert len({package.commit for package in PACKAGES}) == 3
    return report


def check_common_interface() -> dict[str, object]:
    """Check that the three theorem texts expose one common fixed target."""
    required_common = (
        "characteristic zero",
        "star(m_1)",
        "star(m_2)",
        "star(d_0)",
        "star(d_1)",
        "star(d_2)",
        "lambda_c!=0",
        "UNRESOLVED",
    )
    theorem_texts = {
        package.name: (REPO_ROOT / package.theorem[0]).read_text(encoding="utf-8")
        for package in PACKAGES
    }
    for name, text in theorem_texts.items():
        missing = [token for token in required_common if token not in text]
        assert not missing, (name, missing)

    reduction = theorem_texts["distinct_two_low_reduction"]
    assert "number of low modes:" in reduction and "EXACTLY TWO" in reduction
    assert "family distribution:" in reduction and "ONE PER FAMILY" in reduction
    assert "zero high-pairing branch:" in reduction
    assert "E_22 high-pairing branch:" in reduction

    zero = theorem_texts["zero_branch_exclusion"]
    assert "high-high pairing matrix zero:" in zero
    assert "EXCLUDED" in zero
    assert "nonzero E_22 high-high branch:" in zero

    e22 = theorem_texts["E22_branch_exclusion"]
    assert "nonzero high-pairing branch M_(st)=mu E_22:" in e22
    assert "zero high-pairing branch M_(st)=0:" in e22
    assert "EXCLUDED" in e22
    return {
        "common_tokens": len(required_common),
        "reduction_terminal_branches": ["M=0", "M=mu*E22, mu!=0"],
        "zero_dependency_accepts": "M=0",
        "E22_dependency_accepts": "M=mu*E22, mu!=0",
    }


def check_proof_topology() -> dict[str, object]:
    """Exhaust the two terminal leaves of the composed proof."""
    reduction_leaves = frozenset({"zero", "E22_nonzero"})
    excluded_leaves = {
        "zero": "zero_branch_exclusion",
        "E22_nonzero": "E22_branch_exclusion",
    }
    assert reduction_leaves == frozenset(excluded_leaves)

    truth_table: list[dict[str, object]] = []
    for matrix_is_zero in (True, False):
        leaf = "zero" if matrix_is_zero else "E22_nonzero"
        contradiction = leaf in excluded_leaves
        truth_table.append(
            {
                "M_is_zero": matrix_is_zero,
                "terminal_leaf": leaf,
                "excluded_by": excluded_leaves[leaf],
                "contradiction": contradiction,
            }
        )
        assert contradiction
    assert all(row["contradiction"] for row in truth_table)
    return {
        "reduction_leaves": sorted(reduction_leaves),
        "excluded_leaves": excluded_leaves,
        "truth_table": truth_table,
        "surviving_leaves": [],
    }


def check_scope_fence() -> dict[str, bool]:
    """Ensure the endpoint document retains the required negative scope claims."""
    theorem = HERE / "ARBITRARY_PERMANENT_FIXED_PAIR_FULL_EXTENSION_EXCLUSION_THEOREM.md"
    text = theorem.read_text(encoding="utf-8")
    required = (
        "transport to equality-five orbit (4,1):                   NOT PROVED;",
        "transport to equality-five orbit (3,1):                   NOT PROVED;",
        "unrestricted P_6 -> Delta_3:                              UNKNOWN;",
        "global Krenn--Gu conjecture:                              UNRESOLVED.",
    )
    assert all(token in text for token in required)
    return {
        "no_4_1_transport": True,
        "no_3_1_transport": True,
        "no_unrestricted_claim": True,
        "global_status_unresolved": True,
    }


def main() -> None:
    """Run the dependency and proof-topology verifier."""
    report = {
        "frozen_dependencies": check_frozen_dependencies(),
        "common_interface": check_common_interface(),
        "proof_topology": check_proof_topology(),
        "scope_fence": check_scope_fence(),
        "source_sha256": sha256(Path(__file__)),
        "status": "FIXED_PAIR_EXCLUDED; GLOBAL_UNRESOLVED",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
