"""Fail-closed audit of the eight-vertex 4-regular support exclusion."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])

from eight_vertex_degree4_support import (
    complement_edges,
    connected_after_deletion,
    decode_graph6,
    is_four_connected,
    skeleton_matchings,
)

EXPECTED_HOUSE_SHA256 = (
    "6946d13a0aec85386d47d087ad2a9f2561b05d8580f0ec937414f8d31359d34f"
)
EXPECTED_NAUTY_SHA256 = (
    "545cfd83233b4bd966ef0c483ddc8bec4099dcf451cf9d2e2013e46c0e641262"
)
EXPECTED_ALL_CUBIC_SHA256 = (
    "a8bbfcf47bd61aaec24ca2f04122dc90fc0aafc4f6ae82e5c118c328226d192e"
)
EXPECTED_DIRECT_REGULAR_SHA256 = (
    "781b0a4dd2c4289669bc9ff37264cc85afccfa9aaddc9313ae8466fd1bb111e5"
)
EXPECTED_CNF_SHA256 = {
    0: "97a388ff469b45317093aa44c54f488a2523f2f3ed8a7b72a72c113b48497ccf",
    1: "47d91520313ed5a5324c6a1a76018c167cd87c32ba75310a2e2d969150bb185a",
    2: "522ccb3fef84df670ebf23bdc3ba277ad3d1c3551227fa11f337e093d53837dd",
    3: "f61556520776af1e8138a877ec83c4cc1398431ba09f6f55aacfed634e8415fd",
    4: "e65096f573d4e38cfb29bbcfb021205edd4a1bba95b09071c9c9cec3b7685e40",
    5: "418d09659b6b425c4dd9005761bb73fbd6e98e8b60d9dd365391ef90cae960d7",
}
EXPECTED_PROOF_SHA256 = {
    0: "389457c7a49ba088c750ae60e1a6997720c21c2a09f0264c0117c882a9b5e380",
    1: "ed807dfcfdc4eef33b33164af11aff97b51038bdf45e1671061bb6c81d0f8c52",
    2: "f8e88d600d74383633e0870b57c8d03f7f6ce70391fa59e8978fcbde332a3526",
    3: "a1866d6805885cc6e770f42951769ac239ac27b5075d12eaa20f0068c8724ae5",
    4: "bec393bfe221b3c3718d8c5e7058e2e2089e415d9ecb36611f7878970ff5e510",
    5: "a6456784f7ef18336d834b2fd52b8cdb3635f5abac23756aa2926b1421304c96",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def graph_rows(path: Path) -> list[tuple[tuple[int, int], ...]]:
    return [
        decode_graph6(line)
        for line in path.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]


def isomorphic(
    first: tuple[tuple[int, int], ...],
    second: tuple[tuple[int, int], ...],
    n: int = 8,
) -> bool:
    second_set = set(second)
    return any(
        {
            tuple(sorted((permutation[u], permutation[v])))
            for u, v in first
        }
        == second_set
        for permutation in itertools.permutations(range(n))
    )


def dimacs_header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        prefix, kind, variables, clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise AssertionError(f"bad DIMACS header: {path}")
    return int(variables), int(clauses)


def main() -> None:
    base = Path(".").resolve()
    tmp = base / "tmp"
    cnf_dir = tmp / "eight_vertex_degree4_cnf"
    house_path = tmp / "cub08.g6"
    nauty_path = tmp / "cub08_nauty.g6"
    all_cubic_path = tmp / "cub08_all_nauty.g6"
    direct_regular_path = tmp / "reg4_08_nauty.g6"
    if sha256(house_path) != EXPECTED_HOUSE_SHA256:
        raise AssertionError("House of Graphs cubic list hash mismatch")
    if sha256(nauty_path) != EXPECTED_NAUTY_SHA256:
        raise AssertionError("nauty-generated cubic list hash mismatch")
    if sha256(all_cubic_path) != EXPECTED_ALL_CUBIC_SHA256:
        raise AssertionError("all-cubic nauty list hash mismatch")
    if sha256(direct_regular_path) != EXPECTED_DIRECT_REGULAR_SHA256:
        raise AssertionError("direct 4-regular nauty list hash mismatch")

    house = graph_rows(house_path)
    nauty = graph_rows(nauty_path)
    all_cubic = graph_rows(all_cubic_path)
    direct_regular = graph_rows(direct_regular_path)
    if len(house) != 5 or len(nauty) != 5:
        raise AssertionError("expected five connected cubic graph classes")
    if len(all_cubic) != 6 or len(direct_regular) != 6:
        raise AssertionError("expected six unrestricted complement classes")
    if all_cubic[:5] != nauty:
        raise AssertionError("connected cubic ordering changed")
    mapping: list[int] = []
    for graph in house:
        hits = [
            index
            for index, candidate in enumerate(nauty)
            if isomorphic(graph, candidate)
        ]
        if len(hits) != 1:
            raise AssertionError(
                f"catalogue graph has {len(hits)} nauty images"
            )
        mapping.append(hits[0])
    if sorted(mapping) != list(range(5)):
        raise AssertionError("catalogue and nauty lists are not bijective")
    disconnected = [
        index
        for index, graph in enumerate(all_cubic)
        if not connected_after_deletion(
            8, graph, frozenset()
        )
    ]
    if disconnected != [5]:
        raise AssertionError("expected one disconnected cubic class")
    catalogue = [*house, all_cubic[5]]
    catalogue_to_all_cubic = [*mapping, 5]
    complement_to_direct_regular: list[int] = []
    for cubic in catalogue:
        complement = complement_edges(8, cubic)
        hits = [
            index
            for index, candidate in enumerate(direct_regular)
            if isomorphic(complement, candidate)
        ]
        if len(hits) != 1:
            raise AssertionError(
                "complement does not have one direct regular image"
            )
        complement_to_direct_regular.append(hits[0])
    if sorted(complement_to_direct_regular) != list(range(6)):
        raise AssertionError("direct regular catalogue is not bijective")

    batch = json.loads(
        (tmp / "eight_vertex_degree4_support.json").read_text(
            encoding="utf-8"
        )
    )
    batch_rows = {
        int(row["cubic_index"]): row for row in batch["graphs"]
    }
    extra_batch = json.loads(
        (tmp / "eight_vertex_degree4_all_nauty_support.json").read_text(
            encoding="utf-8"
        )
    )
    batch_rows.update(
        {
            int(row["cubic_index"]): row
            for row in extra_batch["graphs"]
        }
    )
    if set(batch_rows) != set(range(6)):
        raise AssertionError("support batches do not contain six classes")

    audited: list[dict[str, object]] = []
    for index, cubic in enumerate(catalogue):
        skeleton = complement_edges(8, cubic)
        four_connected = is_four_connected(8, skeleton)
        row = batch_rows[index]
        if bool(row["four_connected_complement"]) != four_connected:
            raise AssertionError(f"connectivity mismatch at class {index}")

        cnf = cnf_dir / f"complement_cubic_{index}.cnf"
        cnf_hash = sha256(cnf)
        if cnf_hash != EXPECTED_CNF_SHA256[index]:
            raise AssertionError(f"CNF hash mismatch at class {index}")
        variables, clauses = dimacs_header(cnf)
        expected_matchings = len(skeleton_matchings(8, skeleton))
        if (
            row["status"] != "UNSAT"
            or int(row["variables"]) != variables
            or int(row["clauses"]) != clauses
            or int(row["perfect_matchings"]) != expected_matchings
        ):
            raise AssertionError(f"batch metadata mismatch at class {index}")

        glucose_path = (
            cnf_dir / f"complement_cubic_{index}_glucose.json"
        )
        glucose = json.loads(glucose_path.read_text(encoding="utf-8"))
        if (
            glucose["status"] != "UNSAT"
            or int(glucose["variables"]) != variables
            or int(glucose["clauses"]) != clauses
        ):
            raise AssertionError(f"Glucose replay failed at class {index}")
        referenced_cnf = (base / str(glucose["cnf"])).resolve()
        if sha256(referenced_cnf) != cnf_hash:
            raise AssertionError(
                f"Glucose used a different CNF at class {index}"
            )

        cadical_log = (
            cnf_dir / f"complement_cubic_{index}_cadical195.log"
        )
        if "s UNSATISFIABLE" not in cadical_log.read_text(
            encoding="utf-8"
        ):
            raise AssertionError(f"CaDiCaL failed at class {index}")
        proof = (
            cnf_dir / f"complement_cubic_{index}_cadical195.drat"
        )
        proof_hash = sha256(proof)
        if proof_hash != EXPECTED_PROOF_SHA256[index]:
            raise AssertionError(f"proof hash mismatch at class {index}")
        drat_log = (
            cnf_dir / f"complement_cubic_{index}_drat_trim.log"
        )
        if "s VERIFIED" not in drat_log.read_text(encoding="utf-8"):
            raise AssertionError(f"DRAT proof failed at class {index}")

        audited.append(
            {
                "cubic_index": index,
                "all_cubic_nauty_index": catalogue_to_all_cubic[index],
                "direct_regular_nauty_index": (
                    complement_to_direct_regular[index]
                ),
                "perfect_matchings": expected_matchings,
                "variables": variables,
                "clauses": clauses,
                "cnf": str(cnf.relative_to(base)),
                "cnf_sha256": cnf_hash,
                "glucose_seconds": glucose["elapsed_seconds"],
                "proof": str(proof.relative_to(base)),
                "proof_bytes": proof.stat().st_size,
                "proof_sha256": proof_hash,
                "drat_log": str(drat_log.relative_to(base)),
            }
        )

    if len(audited) != 6:
        raise AssertionError("expected all six audited classes")
    result = {
        "verified": True,
        "claim": (
            "no complex witness on an eight-vertex "
            "4-regular skeleton"
        ),
        "catalogue_classes": len(catalogue),
        "connected_cubic_catalogue_classes": len(house),
        "all_cubic_nauty_classes": len(all_cubic),
        "direct_regular_nauty_classes": len(direct_regular),
        "catalogue_to_all_cubic_nauty": catalogue_to_all_cubic,
        "complement_to_direct_regular_nauty": (
            complement_to_direct_regular
        ),
        "four_connected_classes": sum(
            is_four_connected(8, complement_edges(8, cubic))
            for cubic in catalogue
        ),
        "three_cut_classes": 1,
        "classes": audited,
    }
    output = tmp / "eight_vertex_4regular_final_audit.json"
    output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {output}: verified=True")


if __name__ == "__main__":
    main()
