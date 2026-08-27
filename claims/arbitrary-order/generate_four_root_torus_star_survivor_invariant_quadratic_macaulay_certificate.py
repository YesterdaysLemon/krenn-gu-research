#!/usr/bin/env python3
"""Generate the durable GLD82 Gaussian Macaulay coefficient certificate."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERIFIER = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_survivor_invariant_quadratic_macaulay_principal_open_nonextension.py"
)


def load_verifier():
    spec = importlib.util.spec_from_file_location("gld82_generator", VERIFIER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    verifier = load_verifier()
    result = verifier.construct()
    payload = verifier.canonical_certificate_bytes(result)
    verifier.CERTIFICATE.write_bytes(payload)
    print(f"wrote {verifier.CERTIFICATE} ({len(payload)} bytes)")


if __name__ == "__main__":
    main()
