"""Generate a canonical receipt from the primary C9 enumerator.

This is deliberately a primary-route producer: it imports the owning
enumerator, asks it for a supported unique low-q word, and records only the
gauge-fixed configuration, a canonical support digest, and one matching.
The independent checker in this directory does not import this module or the
primary enumerator and reconstructs every support from the two bit fields.
"""

from __future__ import annotations

import sys
import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRIMARY_PATH = HERE / "enumerate_k3.py"
OUTPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("tmp/minimum-density-k3-regenerated.jsonl")


def load_primary():
    spec = importlib.util.spec_from_file_location("primary_cycle_square", PRIMARY_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {PRIMARY_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_support(edges):
    return sorted((x, y, cx, cy) for x, y, cx, cy, _weight, _name in edges)


def support_digest(support):
    payload = json.dumps(support, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def main():
    primary = load_primary()
    source_sha = hashlib.sha256(PRIMARY_PATH.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    temporary = OUTPUT.with_suffix(".jsonl.tmp")
    rows = 0
    with temporary.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps({
            "kind": "meta",
            "schema": 1,
            "primary_sha256": source_sha,
            "expected_rows": 32768,
        }, sort_keys=True) + "\n")
        for pair_bits in range(1 << 9):
            choice = primary.pair_choices(pair_bits)
            if any(primary.is_transit(choice, t) and primary.is_transit(choice, u)
                   for t, u in primary.F_EDGES):
                continue
            for map_bits in range(1 << 9):
                maps = primary.edge_maps(choice, map_bits)
                if not primary.hidden_alignment_holds(choice, maps):
                    continue
                edges = primary.scalar_edges(choice, maps)
                _counts, unique_low, _macro = primary.classify_terms(edges)
                if not unique_low:
                    raise AssertionError((pair_bits, map_bits, "no primary witness"))
                word, q, names = min(unique_low, key=lambda item: (item[0], item[1], item[2]))
                by_name = {name: (x, y, cx, cy)
                           for x, y, cx, cy, _weight, name in edges}
                matching = sorted(by_name[name] for name in names)
                support = canonical_support(edges)
                record = {
                    "kind": "row",
                    "pair_bits": pair_bits,
                    "map_bits": map_bits,
                    "support_sha256": support_digest(support),
                    "word": list(word),
                    "q": list(q),
                    "matching": matching,
                }
                stream.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
                rows += 1
                if rows % 4096 == 0:
                    print("primary_rows", rows, flush=True)
    if rows != 32768:
        raise AssertionError(rows)
    temporary.replace(OUTPUT)
    print("PRIMARY_CANONICAL_RECEIPT_PASS", rows, support_digest([[rows]]))
    print("receipt", OUTPUT)


if __name__ == "__main__":
    main()
