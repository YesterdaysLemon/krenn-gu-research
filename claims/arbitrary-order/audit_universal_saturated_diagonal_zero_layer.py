"""Independent audit of the universal balanced-bridge zero layer."""

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


from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    # Reverse bit order and enumeration order from the primary program.
    records = []
    for b2, b1, b0 in itertools.product((1, 0), repeat=3):
        normal = (
            2 if b0 else 1,
            2 if b1 else 0,
            1 if b2 else 0,
        )
        q = (
            10 * (1 - b1 - b2),
            10 * (b2 - b0),
            10 * (b0 + b1 - 1),
        )
        records.append((normal, (b0, b1, b2), q))
    if len({normal for normal, _bits, _q in records}) != 8:
        raise AssertionError("independent normal census changed")

    def plane_survives(
        left,
        right,
        row: int,
        column: int,
    ) -> bool:
        for target in range(3):
            if (
                row != left[target]
                and column != right[target]
                and (row, column) != (target, target)
            ):
                return False
        return True

    histogram: Counter[int] = Counter()
    zeros = []
    permitted = 0
    for left, left_bits, left_q in records:
        for right, right_bits, right_q in records:
            for column in (2, 1, 0):
                for row in (2, 1, 0):
                    if not plane_survives(
                        left, right, row, column
                    ):
                        continue
                    permitted += 1
                    value = left_q[row] + right_q[column]
                    histogram[value] += 1
                    if value == 0:
                        zeros.append(
                            (
                                left_bits,
                                right_bits,
                                row,
                                column,
                            )
                        )

    if (
        permitted != 180
        or histogram != Counter({0: 48, 10: 96, 20: 36})
        or len(zeros) != 48
    ):
        raise AssertionError(
            "independent universal-potential census failed"
        )
    for left_bits, right_bits, row, column in zeros:
        if row != column:
            raise AssertionError("zero bichromatic unit found")
        for bit in range(3):
            if bit != row and left_bits[bit] == right_bits[bit]:
                raise AssertionError(
                    "zero diagonal transition is not saturated"
                )

    primary = Path(
        "tmp",
        "universal_saturated_diagonal_zero_layer_verified.json",
    )
    source = json.loads(primary.read_text(encoding="utf-8"))
    expected_histogram = {
        str(key): value
        for key, value in sorted(histogram.items())
    }
    if (
        source.get("verified") is not True
        or source.get("permitted_oriented_units") != permitted
        or source.get("universal_edge_potential_histogram")
        != expected_histogram
        or source.get("zero_potential_units") != len(zeros)
    ):
        raise AssertionError(
            "primary and independent universal tables disagree"
        )

    theorem = HERE / "UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md"
    payload = {
        "verified": True,
        "status": (
            "universal_saturated_diagonal_zero_layer_independently_audited"
        ),
        "method": (
            "reversed bit construction, direct coordinate-plane tests, "
            "and closed universal potential"
        ),
        "normal_types": len(records),
        "permitted_oriented_units": permitted,
        "universal_edge_potential_histogram": expected_histogram,
        "zero_potential_units": len(zeros),
        "zero_layer_exactly_saturated_monochromatic_diagonal": True,
        "primary": str(primary),
        "primary_sha256": sha256(primary),
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp",
        "universal_saturated_diagonal_zero_layer_audited.json",
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "verified": True,
                "permitted_units": permitted,
                "histogram": dict(sorted(histogram.items())),
                "zero_units": len(zeros),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
