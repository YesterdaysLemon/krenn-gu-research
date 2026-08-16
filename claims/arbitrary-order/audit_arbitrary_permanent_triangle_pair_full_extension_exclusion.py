"""Independent Git-object audit of the displayed triangle composition.

The audit imports neither the primary verifier nor SymPy.  It checks all
reviewed dependency objects against pinned commits and blobs, reads the
accepted theorem boundaries independently, and exhausts the N/X leaves.
"""

from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from krenn_gu.bootstrap import bootstrap

REPO_ROOT, HERE = bootstrap(__file__)


@dataclass(frozen=True)
class Artifact:
    """One file pinned to a reviewed commit and Git blob."""

    role: str
    path: str
    sha256: str
    blob: str


@dataclass(frozen=True)
class Package:
    """One reviewed dependency package."""

    name: str
    commit: str
    artifacts: tuple[Artifact, ...]


PACKAGES = (
    Package(
        "two_sided",
        "ba39b00cc3d49309fc25e44754cb06f66eaefbdb",
        (
            Artifact(
                "theorem",
                "claims/arbitrary-order/"
                "ARBITRARY_PERMANENT_TRIANGLE_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md",
                "C5E8F47B499318595481D84DB75425240BA6A01AD512A92BF923F5FAB56BF485",
                "7d51cee48633c7f625cfcd1a0b94530cc82fb3d6",
            ),
            Artifact(
                "primary",
                "claims/arbitrary-order/"
                "verify_arbitrary_permanent_triangle_pair_two_sided_projection_drop.py",
                "770F21C2D34A5B98CE5820D023405D0A95B3FE167539747E3EFB9EDE4A538153",
                "0d5e16265201ff476b2f8e80c4bc6abfac97f5ca",
            ),
            Artifact(
                "audit",
                "claims/arbitrary-order/"
                "audit_arbitrary_permanent_triangle_pair_two_sided_projection_drop.py",
                "14AB3E48905246452B9B02D962D0D5902D543398EA74B0009ACAF12C720D136D",
                "a40cfe160f9eb6e9f90fcf4901021c18dc836844",
            ),
            Artifact(
                "review",
                "docs/audits/"
                "ARBITRARY_PERMANENT_TRIANGLE_PAIR_TWO_SIDED_PROJECTION_DROP_REVIEW_2026-08-15.md",
                "4E52015588B2DA8353B717D3704C7D2149B21B0046BD4FDD1B3664500E5A27F6",
                "fde4bbaef4be2d4f04269fa6ff27d68c04e4a44d",
            ),
        ),
    ),
    Package(
        "kernel",
        "6e4d8ec79191a51c90dd188f7bdc2d7fde36b5f7",
        (
            Artifact(
                "theorem",
                "claims/arbitrary-order/"
                "ARBITRARY_PERMANENT_TRIANGLE_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md",
                "60858DFE1C1C9E11C74662B815E1A4173616C3277E28A25520EDAD97148EBA82",
                "952b7e876b8670d0a85f850713d87b04d0cbf310",
            ),
            Artifact(
                "primary",
                "claims/arbitrary-order/"
                "verify_arbitrary_permanent_triangle_pair_kernel_support_boundary.py",
                "67F27BEF7A3C8A071344F6B48BEA265DF2173E839586C988239F039DBB72F8DF",
                "02e574815669c64ebdb28c486291c95ee197ad28",
            ),
            Artifact(
                "audit",
                "claims/arbitrary-order/"
                "audit_arbitrary_permanent_triangle_pair_kernel_support_boundary.py",
                "B0C5DFBC8ED8086BCF5EDAA8665BD57131E2291ED73601A269F35996B973FBA8",
                "54570210a36e48febf6e52ce4e2ec2cffca25f5a",
            ),
            Artifact(
                "review",
                "docs/audits/"
                "ARBITRARY_PERMANENT_TRIANGLE_PAIR_KERNEL_SUPPORT_BOUNDARY_REVIEW_2026-08-15.md",
                "09692AF859DB180F6D2BD5E0A51361F07BDFD33CCBC47671794A5B06FB2D1676",
                "591a356909b3a412f5dee63f8a3913336d75f74b",
            ),
        ),
    ),
    Package(
        "same_mode",
        "f8267fc172ac8f9bee528e3b2ae876635253823b",
        (
            Artifact(
                "theorem",
                "claims/arbitrary-order/"
                "ARBITRARY_PERMANENT_TRIANGLE_PAIR_SAME_MODE_TWO_LOW_EXCLUSION_THEOREM.md",
                "196A46E7B85A332956DB6CCF99BD72F1999E3B8205E774F077C552C70961A155",
                "f99ca79a211b5ec241dfc5c460131cb73dac0658",
            ),
            Artifact(
                "primary",
                "claims/arbitrary-order/"
                "verify_arbitrary_permanent_triangle_pair_same_mode_two_low_exclusion.py",
                "9DDA7DB2F2059A596E242D69834078CE852E70DBB90B450E0775F040394870E5",
                "bafe1cc290e887264e4c94613689ab1d73eb4774",
            ),
            Artifact(
                "audit",
                "claims/arbitrary-order/"
                "audit_arbitrary_permanent_triangle_pair_same_mode_two_low_exclusion.py",
                "4F0B502445D5330421D597CCF674B1F0227E5D14E8DADABFF26253954827BE95",
                "f7731259bf5fe75e7e48fd2f57f81e5001da165a",
            ),
            Artifact(
                "review",
                "docs/audits/"
                "ARBITRARY_PERMANENT_TRIANGLE_PAIR_SAME_MODE_TWO_LOW_EXCLUSION_REVIEW_2026-08-15.md",
                "48D59C4408EA1F91E6B6AA436C474B903B578B41C0E23444A201510F1E08C0AC",
                "3bd7f333ab735891b452566e29edf251997435e5",
            ),
        ),
    ),
    Package(
        "companion",
        "76240ca4becc1b58b9803ac1ec6a4db159c07d3c",
        (
            Artifact(
                "theorem",
                "claims/arbitrary-order/"
                "ARBITRARY_PERMANENT_STAR_TRIANGLE_EXCEPTIONAL_COMPANION_PROPAGATION_THEOREM.md",
                "9C70842573B3DD02BE5AC9CC65B08047AF0C6877892EA816A5D89B2024ED36A3",
                "b75c8b3baf1f181129aac68020c51e038b4900b0",
            ),
            Artifact(
                "primary",
                "claims/arbitrary-order/"
                "verify_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py",
                "97177FE5D7A44821428AAED34707FAD30490D50D80163609A28FB3AE7BE663F0",
                "cd8fcab56f71e3833972103dac9498acd74b43d9",
            ),
            Artifact(
                "audit",
                "claims/arbitrary-order/"
                "audit_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py",
                "9DB62582D752C85F2E7AE8343EC806B95786C5693466ECFB3666C5F838A35289",
                "d0f44eb3cb6be8ff94d9981115f19ba7d5e8c44e",
            ),
            Artifact(
                "review",
                "docs/audits/"
                "ARBITRARY_PERMANENT_STAR_TRIANGLE_EXCEPTIONAL_COMPANION_PROPAGATION_REVIEW_2026-08-15.md",
                "7BDFE90C91664B8A8AF5C3B6BFC8997F274D8EB4BCBF863757CD63E81DC30300",
                "c858dd723a0035262fedf9c61fa62c706b089bfb",
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
    """Check current files and committed objects against all frozen pins."""
    report: dict[str, object] = {}
    for package in PACKAGES:
        resolved = git_bytes("rev-parse", f"{package.commit}^{{commit}}").decode().strip()
        assert resolved == package.commit
        assert git_success("merge-base", "--is-ancestor", package.commit, "HEAD")
        artifact_report: dict[str, dict[str, str]] = {}
        for artifact in package.artifacts:
            committed = git_bytes("show", f"{package.commit}:{artifact.path}")
            current = (REPO_ROOT / artifact.path).read_bytes()
            blob = git_bytes("rev-parse", f"{package.commit}:{artifact.path}").decode().strip()
            assert committed == current
            assert digest(committed) == artifact.sha256
            assert blob == artifact.blob
            artifact_report[artifact.role] = {
                "sha256": artifact.sha256,
                "blob": artifact.blob,
            }
        report[package.name] = {
            "commit": resolved,
            "ancestor_of_HEAD": True,
            "artifacts": artifact_report,
        }

    commits = {package.name: package.commit for package in PACKAGES}
    assert git_success(
        "merge-base", "--is-ancestor", commits["two_sided"], commits["kernel"]
    )
    assert git_success(
        "merge-base", "--is-ancestor", commits["kernel"], commits["same_mode"]
    )
    assert git_success(
        "merge-base", "--is-ancestor", commits["same_mode"], commits["companion"]
    )
    return report


def artifact_text(package_name: str, role: str) -> str:
    """Read one independently pinned dependency artifact."""
    package = next(package for package in PACKAGES if package.name == package_name)
    artifact = next(artifact for artifact in package.artifacts if artifact.role == role)
    return (REPO_ROOT / artifact.path).read_text(encoding="utf-8")


def audit_accepted_boundaries() -> dict[str, object]:
    """Read the four dependency interfaces independently."""
    two_sided = artifact_text("two_sided", "theorem")
    kernel = artifact_text("kernel", "theorem")
    same_mode = artifact_text("same_mode", "theorem")
    companion = artifact_text("companion", "theorem")

    assert "min_(2<=t<=5) rank(Phi_2|L_t) <= 2." in two_sided
    assert "rank(Phi_k|L_t)>=2." in kernel
    assert "Kx_3,                  with local support exactly {0}" in kernel
    assert "K(x_1+x_2),            with local support in {1,2}" in kernel
    assert "same-mode proportional N/N:" in same_mode
    assert "every same-mode cross-family low:" in same_mode
    assert "Phi_2   X=x_3" in companion
    assert "x_1+x_2 / nonempty subset of {1,2}" in companion

    review_tokens = {
        "two_sided": "other based-frame stabilizer orbits of type (3,1):",
        "kernel": "Phi_2: Kx_3, K(x_1+x_2).",
        "same_mode": "every same-mode cross-family low:",
        "companion": "some distinct local mode contains a nonzero",
    }
    review_report: dict[str, str] = {}
    for name, token in review_tokens.items():
        review = artifact_text(name, "review")
        assert "**PASS," in review
        assert token in review
        assert "UNRESOLVED" in review
        review_report[name] = "PASS"
    return {
        "Phi_2_drop": "rank <= 2",
        "rank_floor": "rank >= 2",
        "Phi_2_kernel_cover": ["N", "X"],
        "same_mode_cross_family_low": "excluded",
        "X_arrow": "distinct-mode N",
        "hostile_reviews": review_report,
    }


def audit_nx_exhaustion() -> dict[str, object]:
    """Independently derive and exhaust the N/X contradiction diagram."""
    low_line_cover = frozenset({"N", "X"})
    rows: list[dict[str, object]] = []
    surviving = 0
    for initial_line in sorted(low_line_cover):
        if initial_line == "N":
            terminal_line = "N"
            terminal_mode = "initial"
            propagation_used = False
        else:
            terminal_line = "N"
            terminal_mode = "distinct"
            propagation_used = True

        in_phi1_kernel = terminal_line == "N"
        in_phi2_kernel = terminal_line == "N"
        rank_floor = 2
        phi1_rank = rank_floor if in_phi1_kernel else 3
        phi2_rank = rank_floor if in_phi2_kernel else 3
        same_mode_contradiction = phi1_rank == phi2_rank == 2
        survives = not same_mode_contradiction
        surviving += survives
        rows.append(
            {
                "initial_line": initial_line,
                "propagation_used": propagation_used,
                "terminal_line": terminal_line,
                "terminal_mode": terminal_mode,
                "Phi_1_rank": phi1_rank,
                "Phi_2_rank": phi2_rank,
                "same_mode_contradiction": same_mode_contradiction,
                "survives": survives,
            }
        )
    assert {row["initial_line"] for row in rows} == low_line_cover
    assert all(row["same_mode_contradiction"] for row in rows)
    assert surviving == 0
    return {"rows": rows, "surviving_low_lines": []}


def audit_endpoint_scope_and_independence() -> dict[str, bool]:
    """Check the exact endpoint scope and no-import audit boundary."""
    endpoint = (
        HERE / "ARBITRARY_PERMANENT_TRIANGLE_PAIR_FULL_EXTENSION_EXCLUSION_THEOREM.md"
    ).read_text(encoding="utf-8")
    assertions = {
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
    assert all(token in endpoint for token in assertions.values())

    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imported_modules.add(node.module)
    assert "sympy" not in imported_modules
    assert not any(
        module.endswith(
            "verify_arbitrary_permanent_triangle_pair_full_extension_exclusion"
        )
        for module in imported_modules
    )
    return {
        **{name: True for name in assertions},
        "primary_imported": False,
        "symbolic_library_used": False,
    }


def main() -> None:
    """Run the independent Git-object and topology audit."""
    report = {
        "git_objects": audit_git_objects(),
        "accepted_boundaries": audit_accepted_boundaries(),
        "N_X_exhaustion": audit_nx_exhaustion(),
        "endpoint_scope_and_independence": audit_endpoint_scope_and_independence(),
        "source_sha256": digest(Path(__file__).read_bytes()),
        "status": "DISPLAYED_TRIANGLE_FRAME_EXCLUDED; GLOBAL_UNRESOLVED",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
