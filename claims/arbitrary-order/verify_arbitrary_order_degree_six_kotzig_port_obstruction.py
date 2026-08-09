"""Verify the local tables in the arbitrary-order degree-six theorem."""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

Normal = tuple[int, int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def bits(normal: Normal) -> tuple[int, int, int]:
    return (
        int(normal[0] == 2),
        int(normal[1] == 2),
        int(normal[2] == 1),
    )


def potential(normal: Normal) -> tuple[int, int, int]:
    b0, b1, b2 = bits(normal)
    return (
        1 - 2 * b2,
        2 * (b2 - b0),
        2 * (b0 + b1 - 1),
    )


def allowed(
    left: Normal,
    right: Normal,
    row: int,
    column: int,
) -> bool:
    return all(
        (row, column) == (target, target)
        or row == left[target]
        or column == right[target]
        for target in range(3)
    )


def saturated(
    left: Normal, right: Normal, colour: int
) -> bool:
    left_bits = bits(left)
    right_bits = bits(right)
    return all(
        left_bits[bit] != right_bits[bit]
        for bit in range(3)
        if bit != colour
    )


def main() -> None:
    normals = tuple(
        itertools.product((1, 2), (0, 2), (0, 1))
    )
    q = {normal: potential(normal) for normal in normals}

    forced = []
    optional = []
    for colour in range(3):
        for left in normals:
            for right in normals:
                if not saturated(left, right, colour):
                    continue
                if not allowed(left, right, colour, colour):
                    raise AssertionError(
                        "saturated own-colour unit became forbidden"
                    )
                value = q[left][colour] + q[right][colour]
                forced.append((colour, left, right, value))
                for row in range(3):
                    for column in range(3):
                        if (
                            row != column
                            and allowed(
                                left,
                                right,
                                row,
                                column,
                            )
                        ):
                            optional.append(
                                (
                                    left,
                                    right,
                                    row,
                                    column,
                                    q[left][row]
                                    + q[right][column],
                                )
                            )

    if len(forced) != 48 or any(
        row[-1] != 0 for row in forced
    ):
        raise AssertionError("forced diagonal table changed")
    if len(optional) != 42 or any(
        row[-1] <= 0 for row in optional
    ):
        raise AssertionError("optional diagonal table changed")

    reciprocal_tasks = 0
    physical_ports = []
    for left in normals:
        for right in normals:
            for target in range(3):
                partner_target = left[target]
                if right[partner_target] != target:
                    continue
                reciprocal_tasks += 1
                row, column = partner_target, target
                if not allowed(
                    left, right, row, column
                ):
                    continue
                physical_ports.append(
                    (
                        left,
                        right,
                        target,
                        partner_target,
                        q[left][row] + q[right][column],
                    )
                )

    port_histogram = Counter(
        row[-1] for row in physical_ports
    )
    if (
        reciprocal_tasks != 96
        or len(physical_ports) != 72
        or port_histogram != Counter(
            {1: 24, 2: 16, 3: 24, 4: 8}
        )
    ):
        raise AssertionError("corrected physical-port table changed")

    theorem = Path(
        "ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md"
    )
    payload = {
        "verified": True,
        "status": (
            "arbitrary_order_degree_six_kotzig_port_local_verification"
        ),
        "normal_types": len(normals),
        "saturated_oriented_diagonal_transitions": len(forced),
        "forced_diagonal_potential_values": [0],
        "permitted_optional_diagonal_transitions": len(optional),
        "optional_diagonal_potential_histogram": {
            str(key): value
            for key, value in sorted(
                Counter(row[-1] for row in optional).items()
            )
        },
        "reciprocal_target_task_transitions": reciprocal_tasks,
        "admissible_corrected_physical_ports": len(
            physical_ports
        ),
        "physical_port_potential_histogram": {
            str(key): value
            for key, value in sorted(port_histogram.items())
        },
        "physical_ports_strictly_positive": True,
        "matching_existence_input": (
            "Bogdanov theorem, reported as "
            "Chandran-Gajjala-Illickan Theorem 1.7"
        ),
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp",
        "arbitrary_order_degree_six_kotzig_port_obstruction_verified.json",
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "verified": True,
                "physical_ports": len(physical_ports),
                "port_potential_histogram": dict(
                    sorted(port_histogram.items())
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
