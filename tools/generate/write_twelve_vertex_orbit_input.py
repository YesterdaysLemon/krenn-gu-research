"""Write a compact deterministic input for the compiled order-12 pass."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


SOURCE = Path(
    "tmp/twelve_vertex_port_cell_orbits_counted.json"
)
OUTPUT = Path(
    "tmp/twelve_vertex_port_cell_orbits_input.txt"
)
MANIFEST = Path(
    "tmp/twelve_vertex_port_cell_orbits_input_manifest.json"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    cells = list(source["cell_representatives"])
    if len(cells) != 154:
        raise AssertionError("cell representative count changed")
    lines = [str(len(cells))]
    for cell_id, record in enumerate(cells):
        lines.append(
            " ".join(
                map(
                    str,
                    (
                        cell_id,
                        record["graph_index"],
                        record["cell_index"],
                        record["orbit_size"],
                        record["stabilizer_size"],
                        record["reciprocal_port_realizations"],
                    ),
                )
            )
        )
        diagonal_rows = []
        for colour, matching in enumerate(
            record["diagonal_matchings"]
        ):
            for left, right in matching:
                diagonal_rows.append(
                    (left, right, colour)
                )
        if len(diagonal_rows) != 18:
            raise AssertionError(
                "order-twelve diagonal edge count changed"
            )
        lines.extend(
            f"{left} {right} {colour}"
            for left, right, colour in diagonal_rows
        )
        normals = list(record["normal_types"])
        if len(normals) != 12:
            raise AssertionError("normal row count changed")
        lines.extend(
            " ".join(map(str, normal))
            for normal in normals
        )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        "\n".join(lines) + "\n", encoding="ascii"
    )
    manifest = {
        "verified": True,
        "status": "compiled_orbit_input_written",
        "source": str(SOURCE),
        "source_sha256": sha256(SOURCE),
        "output": str(OUTPUT),
        "output_sha256": sha256(OUTPUT),
        "cells": len(cells),
        "diagonal_edges_per_cell": 18,
        "normal_rows_per_cell": 12,
        "global_conjecture_resolved": False,
        "source_code": str(Path(__file__)),
        "source_code_sha256": sha256(Path(__file__)),
    }
    MANIFEST.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
