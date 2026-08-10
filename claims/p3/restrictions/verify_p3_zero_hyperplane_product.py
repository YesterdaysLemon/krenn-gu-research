#!/usr/bin/env python3
"""Primary symbolic verifier for the zero-plane restriction of P3."""

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

REPO_ROOT, HERE = _bootstrap_repository(__file__)


import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = HERE / "P3_ZERO_HYPERPLANE_PRODUCT_THEOREM.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pair_vector(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            left[1] * right[2] + left[2] * right[1],
            left[0] * right[2] + left[2] * right[0],
            left[0] * right[1] + left[1] * right[0],
        ]
    )


def pair_image(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.hstack(
        *[
            pair_vector(left[:, first], right[:, second])
            for first in range(left.cols)
            for second in range(right.cols)
        ]
    )


def main() -> None:
    v0, v1, v2 = sp.symbols("v0 v1 v2")
    fixed_map = sp.Matrix(
        [
            [0, v2, v1],
            [v2, 0, v0],
            [v1, v0, 0],
        ]
    )
    assert sp.factor(fixed_map.det()) == 2 * v0 * v1 * v2

    coordinate_plane_data = {}
    standard = sp.eye(3)
    for missing in range(3):
        kept = [index for index in range(3) if index != missing]
        plane = standard[:, kept]
        image = pair_image(plane, plane)
        assert image.rank() == 1
        nonzero_rows = [
            row
            for row in range(3)
            if any(image[row, column] for column in range(image.cols))
        ]
        assert nonzero_rows == [missing]

        restricted_values = [
            pair_vector(plane[:, first], plane[:, second]).dot(
                plane[:, third]
            )
            for first, second, third in itertools.product(
                range(2),
                repeat=3,
            )
        ]
        assert restricted_values == [0] * 8
        coordinate_plane_data[str(missing)] = {
            "pair_image_rank": image.rank(),
            "pair_image_coordinate": missing,
            "restricted_coefficients_nonzero": 0,
        }

    output = {
        "verified": True,
        "field": "C",
        "fixed_vector_map_determinant": "2*v0*v1*v2",
        "minimum_input_subspace_dimensions": [2, 2, 2],
        "coordinate_planes_checked": 3,
        "coordinate_plane_data": coordinate_plane_data,
        "zero_plane_triples_classified": 3,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p3_zero_hyperplane_product_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
