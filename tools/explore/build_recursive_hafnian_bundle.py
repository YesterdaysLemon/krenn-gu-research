"""Build a deterministic portable ZIP for the frozen n=10 RZP proof family.

The bundle stays outside ordinary Git history.  It contains the exact CNFs and
binary DRAT proofs, the evidence manifest, generator/replay/audit sources, the
pinned dependency list, and the pinned drat-trim source needed to rebuild the
checker.  Every input is hashed before it is admitted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys as _bootstrap_sys
import zipfile

for _bootstrap_parent in Path(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)


FIXED_TIME = (2026, 9, 13, 0, 0, 0)
CHECKER_FILES = ("drat-trim", "drat-trim.c", "Makefile", "LICENSE", "README.md")
REPOSITORY_FILES = {
    "src/krenn_gu/__init__.py": "src/krenn_gu/__init__.py",
    "src/krenn_gu/bootstrap.py": "src/krenn_gu/bootstrap.py",
    "src/krenn_gu/recursive_hafnian_support.py": "src/krenn_gu/recursive_hafnian_support.py",
    "tools/explore/replay_recursive_hafnian_drat.py": "tools/explore/replay_recursive_hafnian_drat.py",
    "claims/finite/n10/audit_recursive_hafnian_rzp_all_diagonal_exclusion.py": "claims/finite/n10/audit_recursive_hafnian_rzp_all_diagonal_exclusion.py",
    "requirements.lock.txt": "requirements.lock.txt",
}


def identity_bytes(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def identity(path):
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            size += len(chunk)
            digest.update(chunk)
    return {"bytes": size, "sha256": digest.hexdigest()}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def write_bytes(archive, name, data):
    info = zipfile.ZipInfo(name, FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def readme_text():
    return """# Portable n=10 all-diagonal RZP proof bundle

This bundle checks one scoped result: the recursive zero-pattern necessary
model is UNSAT in the exhaustive thirteen matching-normalized n=10 branches.
Together with the written bridge, this excludes complex all-diagonal ternary
Krenn-Gu witnesses at n=10. It does not exclude AP', bichromatic blocks, other
orders, or the global conjecture.

Create a Python environment with the pinned `python-sat` version. The exact
checker binary used for the recorded proof replay is bundled because a fresh
rebuild can differ byte-for-byte even when the source and reported compiler
version agree. Make the pinned binary executable on a POSIX host:

    python -m pip install -r requirements.lock.txt
    chmod +x checker/drat-trim

The audited checker source is also included. A fresh rebuild is a useful
control, but its hash must be reported rather than substituted for the pinned
binary unless the evidence manifest is deliberately re-audited.

Run the independent no-import encoder/cover audit:

    python claims/finite/n10/audit_recursive_hafnian_rzp_all_diagonal_exclusion.py \
      --manifest evidence/recursive-cancellation-consistency-evidence-2026-09-12.json \
      --artifact-dir artifacts --output independent-audit.json

Replay all binary proofs and the three checker controls:

    python tools/explore/replay_recursive_hafnian_drat.py \
      --manifest evidence/recursive-cancellation-consistency-evidence-2026-09-12.json \
      --artifact-dir artifacts --checker checker/drat-trim \
      --output-dir replay --case-timeout-seconds 300

`BUNDLE-CONTENTS.json` pins every member admitted by the builder. The ZIP hash
is external to the ZIP and should be recorded alongside any distribution.
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--checker-source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), "output archive must be new")
    manifest_raw = args.manifest.read_bytes()
    manifest = json.loads(manifest_raw)
    require(manifest.get("schema") == "recursive-hafnian-rzp-drat-v2", "wrong manifest schema")

    members = []
    staged = []

    def add_file(archive_name, path, expected=None, mode=0o100644):
        actual = identity(path)
        if expected is not None:
            require(actual == expected, f"{archive_name}: identity differs")
        staged.append((archive_name, path, mode))
        members.append({"path": archive_name, "identity": actual})

    add_file(
        "evidence/recursive-cancellation-consistency-evidence-2026-09-12.json",
        args.manifest,
    )
    seen_artifacts = set()
    for case in manifest["cases"]:
        for field in ("cnf", "proof"):
            item = case[field]
            require(item["file"] not in seen_artifacts, "duplicate proof-bundle member")
            seen_artifacts.add(item["file"])
            add_file(
                f"artifacts/{item['file']}",
                args.artifact_dir / item["file"],
                {key: item[key] for key in ("bytes", "sha256")},
            )
    for archive_name, relative in REPOSITORY_FILES.items():
        add_file(archive_name, REPO_ROOT / relative)
    checker = manifest["checker"]
    for name in CHECKER_FILES:
        path = args.checker_source_dir / name
        expected = None
        mode = 0o100755 if name == "drat-trim" else 0o100644
        if name == "drat-trim":
            expected = {
                "bytes": path.stat().st_size,
                "sha256": checker["sha256"],
            }
        elif name == "drat-trim.c":
            expected = {
                "bytes": path.stat().st_size,
                "sha256": checker["source_sha256"],
            }
        elif name == "Makefile":
            expected = {
                "bytes": path.stat().st_size,
                "sha256": checker["makefile_sha256"],
            }
        add_file(f"checker/{name}", path, expected, mode)

    readme = readme_text().encode("utf-8")
    members.append({"path": "README.md", "identity": identity_bytes(readme)})
    contents = {
        "schema": "recursive-hafnian-rzp-portable-bundle-v1",
        "scope": manifest["scope"],
        "manifest_identity": identity_bytes(manifest_raw),
        "members": sorted(members, key=lambda row: row["path"]),
    }
    contents_raw = (json.dumps(contents, indent=2, sort_keys=True) + "\n").encode("utf-8")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        args.output,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        allowZip64=True,
    ) as archive:
        write_bytes(archive, "README.md", readme)
        write_bytes(archive, "BUNDLE-CONTENTS.json", contents_raw)
        for archive_name, path, mode in sorted(staged):
            info = zipfile.ZipInfo(archive_name, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = mode << 16
            with path.open("rb") as source, archive.open(info, "w", force_zip64=True) as target:
                for chunk in iter(lambda: source.read(1 << 20), b""):
                    target.write(chunk)
    report = {
        "status": "PASS",
        "archive": str(args.output.resolve()),
        "archive_identity": identity(args.output),
        "payload_members": len(staged),
        "content_manifest_identity": identity_bytes(contents_raw),
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
