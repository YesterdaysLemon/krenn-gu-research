"""Greedily minimize an exact Singular torus-saturation contradiction.

The input is one generated ``fallback_*_q.sing`` program.  Duplicate
polynomials are removed first.  Several deterministic deletion orders then
seek an irreducible subset that still has reduced Groebner basis ``{1}``.
The saturation equation is always retained.

This produces a smaller exact core, not a proof that the core has minimum
cardinality.
"""

from __future__ import annotations
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])


import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from verify_prism_certificates import is_exact_unit_log


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wsl_path(path: Path) -> str:
    absolute = path.resolve()
    drive = absolute.drive.rstrip(":").lower()
    suffix = absolute.as_posix().split(":", 1)[1]
    return f"/mnt/{drive}{suffix}"


def parse_program(source: str) -> tuple[str, list[str], str]:
    marker = "ideal I=\n"
    start = source.index(marker) + len(marker)
    end_marker = ";\nprint("
    end = source.index(end_marker, start)
    prefix = source[:start]
    suffix = source[end:]
    polynomials = [
        item.strip()
        for item in source[start:end].split(",\n")
        if item.strip()
    ]
    if not polynomials or "sat*" not in polynomials[-1]:
        raise ValueError("last polynomial is not the saturation equation")
    return prefix, polynomials, suffix


def render(prefix: str, polynomials: list[str], suffix: str) -> str:
    return prefix + ",\n".join(f"  {item}" for item in polynomials) + suffix


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--output-source", type=Path, required=True)
    parser.add_argument("--output-log", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    original = args.source.read_text(encoding="utf-8")
    prefix, polynomials, suffix = parse_program(original)
    saturation = polynomials[-1]
    equations = list(dict.fromkeys(polynomials[:-1]))
    work = args.output_source.with_suffix(".work.sing")
    cache: dict[tuple[int, ...], tuple[bool, str]] = {}

    def test(indices: list[int]) -> tuple[bool, str]:
        key = tuple(sorted(indices))
        if key in cache:
            return cache[key]
        candidate = [equations[index] for index in key] + [saturation]
        work.write_text(
            render(prefix, candidate, suffix),
            encoding="utf-8",
        )
        try:
            completed = subprocess.run(
                [
                    "wsl.exe",
                    "-e",
                    "/usr/bin/Singular",
                    wsl_path(work),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=args.timeout,
            )
            log = completed.stdout
            passed = (
                completed.returncode == 0
                and not completed.stderr
                and is_exact_unit_log(log)
            )
        except subprocess.TimeoutExpired:
            passed = False
            log = "TIMEOUT\n"
        cache[key] = (passed, log)
        return cache[key]

    full = list(range(len(equations)))
    passed, _log = test(full)
    if not passed:
        raise RuntimeError("deduplicated source no longer proves the unit ideal")

    orders = (
        list(range(len(equations))),
        list(reversed(range(len(equations)))),
        sorted(range(len(equations)), key=lambda index: len(equations[index])),
        sorted(
            range(len(equations)),
            key=lambda index: len(equations[index]),
            reverse=True,
        ),
    )
    best = full
    for order in orders:
        retained = set(full)
        changed = True
        while changed:
            changed = False
            for index in order:
                if index not in retained:
                    continue
                trial = sorted(retained - {index})
                trial_passed, _trial_log = test(trial)
                if trial_passed:
                    retained.remove(index)
                    changed = True
        candidate = sorted(retained)
        if len(candidate) < len(best):
            best = candidate

    final_polynomials = [equations[index] for index in best] + [saturation]
    args.output_source.write_text(
        render(prefix, final_polynomials, suffix),
        encoding="utf-8",
    )
    final = subprocess.run(
        [
            "wsl.exe",
            "-e",
            "/usr/bin/Singular",
            wsl_path(args.output_source),
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=args.timeout,
    )
    if (
        final.returncode != 0
        or final.stderr
        or not is_exact_unit_log(final.stdout)
    ):
        raise RuntimeError("final minimized core did not verify")
    args.output_log.write_text(final.stdout, encoding="utf-8")
    payload = {
        "verified": True,
        "scope": "greedy irreducible exact rational torus core",
        "not_minimum_cardinality_claim": True,
        "source": str(args.source),
        "source_sha256": sha256(args.source),
        "original_equations_including_saturation": len(polynomials),
        "deduplicated_equations_excluding_saturation": len(equations),
        "core_equations_excluding_saturation": len(best),
        "retained_deduplicated_indices": best,
        "tests_run": len(cache),
        "output_source": str(args.output_source),
        "output_source_sha256": sha256(args.output_source),
        "output_log": str(args.output_log),
        "output_log_sha256": sha256(args.output_log),
    }
    args.output_manifest.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    if work.exists():
        work.unlink()
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
