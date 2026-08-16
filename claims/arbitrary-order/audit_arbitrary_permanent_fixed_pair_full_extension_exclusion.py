"""Independent Git-object audit of the fixed-pair proof composition.

The audit imports neither the primary verifier nor SymPy.  It checks the
reviewed dependency bytes directly against their pinned commits, reads the
accepted theorem boundaries independently, and exhausts the terminal truth
table.
"""

from __future__ import annotations

import hashlib
import ast
import json
import subprocess
import sys
from dataclasses import dataclass
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from krenn_gu.bootstrap import bootstrap

REPO_ROOT, HERE = bootstrap(__file__)


@dataclass(frozen=True)
class Artifact:
    """One file pinned to a reviewed commit."""

    role: str
    path: str
    sha256: str


@dataclass(frozen=True)
class Package:
    """A reviewed dependency package."""

    name: str
    commit: str
    artifacts: tuple[Artifact, ...]


PACKAGES = (
    Package(
        "reduction",
        "aa21e104645094b10830c5236210cd2961003579",
        (
            Artifact(
                "theorem",
                "claims/arbitrary-order/"
                "ARBITRARY_PERMANENT_FIXED_PAIR_DISTINCT_TWO_LOW_REDUCTION_THEOREM.md",
                "87BD9CCC45C07088465C27FB4032BCC34DDB7004789A3FC28ECA36F3BFA67D1E",
            ),
            Artifact(
                "primary",
                "claims/arbitrary-order/"
                "verify_arbitrary_permanent_fixed_pair_distinct_two_low_reduction.py",
                "20ECAA638C7AFDFB11187925C76AA6DD9F142E63AE41AD5220F27FA70518290A",
            ),
            Artifact(
                "audit",
                "claims/arbitrary-order/"
                "audit_arbitrary_permanent_fixed_pair_distinct_two_low_reduction.py",
                "F8A1350BD36DA6CFCEBCA674791F44B6DBCF00BD782F53B6319E609005658D56",
            ),
            Artifact(
                "review",
                "docs/audits/"
                "ARBITRARY_PERMANENT_FIXED_PAIR_DISTINCT_TWO_LOW_REDUCTION_REVIEW_2026-08-15.md",
                "FA72305DCA86760A934736168D6FB8E9647A8FA8B6E5C5E66B2A008CD830FEA3",
            ),
        ),
    ),
    Package(
        "zero",
        "6daade565a5424b17ba272ef609b17271e4f8c4d",
        (
            Artifact(
                "theorem",
                "claims/arbitrary-order/"
                "ARBITRARY_PERMANENT_FIXED_PAIR_TWO_LOW_ZERO_BRANCH_EXCLUSION_THEOREM.md",
                "236065BB239059865C91105D49590693E5D9121DD1A0BBB365863A7667FCF0CA",
            ),
            Artifact(
                "primary",
                "claims/arbitrary-order/"
                "verify_arbitrary_permanent_fixed_pair_two_low_zero_branch_exclusion.py",
                "85504804E6BF5A056C53E6E8FDD93B999AB56A0C2E63187E24C590840C58600D",
            ),
            Artifact(
                "audit",
                "claims/arbitrary-order/"
                "audit_arbitrary_permanent_fixed_pair_two_low_zero_branch_exclusion.py",
                "7CB12A912E30C6A44AAC784CE6786E822106BA7A59E3EB396BE9DB33244CEDF6",
            ),
            Artifact(
                "review",
                "docs/audits/"
                "ARBITRARY_PERMANENT_FIXED_PAIR_TWO_LOW_ZERO_BRANCH_EXCLUSION_REVIEW_2026-08-15.md",
                "83462F64188C6D8D0B6D4801779828CCA43CCA88F1896B6A5052D7A3A93BBA0A",
            ),
        ),
    ),
    Package(
        "E22",
        "7bc6e6bb1ff97080671a1ff9f53ea37fe96e02be",
        (
            Artifact(
                "theorem",
                "claims/arbitrary-order/"
                "ARBITRARY_PERMANENT_FIXED_PAIR_DISTINCT_TWO_LOW_E22_EXCLUSION_THEOREM.md",
                "925284C772176125855BF99199B6789E430355A0D4F87553E727CA746B206925",
            ),
            Artifact(
                "primary",
                "claims/arbitrary-order/"
                "verify_arbitrary_permanent_fixed_pair_distinct_two_low_e22_exclusion.py",
                "00BA077A4F4023ECA875C2B9DD826D8FFC2690723CBA16B1C6737720A611E2FC",
            ),
            Artifact(
                "audit",
                "claims/arbitrary-order/"
                "audit_arbitrary_permanent_fixed_pair_distinct_two_low_e22_exclusion.py",
                "0B640BF86F7C495821705D3489307ECA668BFD6951AF342B18665E2B577473B8",
            ),
            Artifact(
                "review",
                "docs/audits/"
                "ARBITRARY_PERMANENT_FIXED_PAIR_DISTINCT_TWO_LOW_E22_EXCLUSION_REVIEW_2026-08-15.md",
                "1BD0A74E440342382981BC894316D2BA4E61F3438AC4CF659C0E90FD21B9CF05",
            ),
        ),
    ),
)


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
    """Check current files and committed objects against every pinned digest."""
    report: dict[str, object] = {}
    for package in PACKAGES:
        resolved = git_bytes("rev-parse", f"{package.commit}^{{commit}}").decode().strip()
        assert resolved == package.commit
        assert git_success("merge-base", "--is-ancestor", package.commit, "HEAD")
        artifact_report: dict[str, str] = {}
        for artifact in package.artifacts:
            committed = git_bytes("show", f"{package.commit}:{artifact.path}")
            current = (REPO_ROOT / artifact.path).read_bytes().replace(b"\r\n", b"\n")
            assert committed == current
            assert digest(committed) == artifact.sha256
            artifact_report[artifact.role] = artifact.sha256
        report[package.name] = {
            "commit": resolved,
            "ancestor_of_HEAD": True,
            "artifacts": artifact_report,
        }

    reduction_commit = PACKAGES[0].commit
    assert git_success("merge-base", "--is-ancestor", reduction_commit, PACKAGES[1].commit)
    assert git_success("merge-base", "--is-ancestor", reduction_commit, PACKAGES[2].commit)
    return report


def theorem_text(package_name: str) -> str:
    """Read one independently pinned theorem text."""
    package = next(package for package in PACKAGES if package.name == package_name)
    artifact = next(artifact for artifact in package.artifacts if artifact.role == "theorem")
    return (REPO_ROOT / artifact.path).read_text(encoding="utf-8")


def review_text(package_name: str) -> str:
    """Read one independently pinned hostile review."""
    package = next(package for package in PACKAGES if package.name == package_name)
    artifact = next(artifact for artifact in package.artifacts if artifact.role == "review")
    return (REPO_ROOT / artifact.path).read_text(encoding="utf-8")


def audit_accepted_boundaries() -> dict[str, object]:
    """Read the terminal interfaces independently from theorem/review prose."""
    reduction = theorem_text("reduction")
    zero = theorem_text("zero")
    e22 = theorem_text("E22")

    reduction_tokens = (
        "number of low modes:                                      exactly two;",
        "one Phi_1, one Phi_2",
        "M_(st)=0",
        "M_(st)=mu E_22",
        "mu!=0",
    )
    assert all(token in reduction for token in reduction_tokens)

    zero_tokens = (
        "exactly two distinct noncommon lows, one per family:",
        "other two modes high for both families:",
        "high-high pairing matrix zero:",
        "EXCLUDED;",
    )
    assert all(token in zero for token in zero_tokens)

    e22_tokens = (
        "number of low modes:                                  EXACTLY TWO;",
        "family distribution:                              ONE PER FAMILY;",
        "nonzero high-pairing branch M_(st)=mu E_22:",
        "EXCLUDED;",
    )
    assert all(token in e22 for token in e22_tokens)

    reviews = {name: review_text(name) for name in ("reduction", "zero", "E22")}
    for text in reviews.values():
        assert "**PASS," in text
        assert "blocker survived hostile review" in text
    return {
        "reduction": ["zero", "E22_nonzero"],
        "zero_theorem": "excludes zero",
        "E22_theorem": "excludes E22_nonzero",
        "hostile_reviews": {name: "PASS" for name in reviews},
    }


def audit_truth_table() -> dict[str, object]:
    """Independently exhaust branch membership and exclusion truth values."""
    rows: list[dict[str, object]] = []
    admissible_rows = 0
    surviving_rows = 0
    for zero_branch, e22_branch in product((False, True), repeat=2):
        reduction_admissible = zero_branch != e22_branch
        contradicted_by_zero_theorem = zero_branch
        contradicted_by_e22_theorem = e22_branch
        terminal_contradiction = (
            contradicted_by_zero_theorem or contradicted_by_e22_theorem
        )
        survives = reduction_admissible and not terminal_contradiction
        if reduction_admissible:
            admissible_rows += 1
            assert terminal_contradiction
        surviving_rows += survives
        rows.append(
            {
                "zero_branch": zero_branch,
                "E22_nonzero_branch": e22_branch,
                "reduction_admissible": reduction_admissible,
                "terminal_contradiction": terminal_contradiction,
                "survives": survives,
            }
        )
    assert admissible_rows == 2
    assert surviving_rows == 0
    return {"rows": rows, "admissible_rows": admissible_rows, "surviving_rows": 0}


def audit_endpoint_scope() -> dict[str, bool]:
    """Check the new endpoint preserves the exact non-global scope."""
    endpoint = (HERE / "ARBITRARY_PERMANENT_FIXED_PAIR_FULL_EXTENSION_EXCLUSION_THEOREM.md").read_text(
        encoding="utf-8"
    )
    assertions = {
        "fixed_pair_excluded": "exact extension of the fixed pair (1):                    EXCLUDED;",
        "no_4_1_transport": "transport to equality-five orbit (4,1):                   NOT PROVED;",
        "no_3_1_transport": "transport to equality-five orbit (3,1):                   NOT PROVED;",
        "unrestricted_unknown": "unrestricted P_6 -> Delta_3:                              UNKNOWN;",
        "global_unresolved": "global Krenn--Gu conjecture:                              UNRESOLVED.",
    }
    assert all(token in endpoint for token in assertions.values())
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    assert "sympy" not in imported_modules
    assert "verify_arbitrary_permanent_fixed_pair_full_extension_exclusion" not in imported_modules
    return {name: True for name in assertions}


def main() -> None:
    """Run the independent proof-composition audit."""
    report = {
        "git_objects": audit_git_objects(),
        "accepted_boundaries": audit_accepted_boundaries(),
        "truth_table": audit_truth_table(),
        "endpoint_scope": audit_endpoint_scope(),
        "primary_imported": False,
        "symbolic_library_used": False,
        "source_sha256": digest(Path(__file__).read_bytes()),
        "status": "FIXED_PAIR_EXCLUDED; GLOBAL_UNRESOLVED",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
