"""Attach exact source transports to a discovered row-space candidate.

The discovery report is not a certificate.  This packer reconstructs every
integer transport from the original complete Laplace fibres, emits the small
typed certificate, and requires exact replay before writing it.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys as _bootstrap_sys

for _bootstrap_parent in Path(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

from krenn_gu.recursive_tensor_quotient import (  # noqa: E402
    RecursiveTensorQuotient,
    UnitSignedQuotient,
    _origin_data,
    _read_origin,
)
from krenn_gu.recursive_tensor_row_space import replay_recursive_row_space  # noqa: E402
from krenn_gu.recursive_tensor_support import (  # noqa: E402
    build_recursive_tensor_support_cnf,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--discovery", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--fixture-output",
        type=Path,
        help="optional compact model-plus-certificate replay fixture",
    )
    args = parser.parse_args()
    for path in (args.output, args.fixture_output):
        if path is not None and path.exists():
            raise ValueError(f"output path must be new: {path}")

    report = json.loads(args.discovery.read_text(encoding="utf-8"))
    if (
        report.get("n") != args.n
        or report.get("status") != "MONOMIAL_CONTRADICTION_CANDIDATE"
    ):
        raise ValueError("discovery report has no matching contradiction candidate")
    instance = build_recursive_tensor_support_cnf(
        args.n,
        column_killers=False,
        fix_root_killers=False,
    )
    model = json.loads(args.model.read_text(encoding="utf-8"))
    algebra = RecursiveTensorQuotient(instance)
    assigned, positive = algebra.binomials.support(model)
    _expanded, raw, substitutions = algebra.binomials.extract(model)
    origins = set(raw)
    origins.update(origin for origin, _dependencies in substitutions.values())
    origins = sorted(
        origins,
        key=lambda origin: (
            origin.vertices,
            origin.word,
            origin.vertex,
            origin.orientation,
        ),
    )
    rows = [algebra.binomials.raw_relation(origin, positive) for origin in origins]
    quotient = UnitSignedQuotient(rows)
    if quotient.kernel is not None:
        raise ValueError("the model has an earlier binomial-kernel obstruction")

    used, variables = set(), set()
    dag = report["dag"]
    source_origins = []
    for node in dag:
        if node["kind"] == "source":
            origin = _read_origin(node["origin"])
            source_origins.append(origin)
            node["transports"] = []
            for term, _coefficient in algebra.terms(origin, positive):
                monomial, sign = quotient.signature(term)
                difference = Counter(term)
                difference.subtract(dict(monomial))
                coordinates = quotient.coordinates(
                    {
                        variable: power
                        for variable, power in difference.items()
                        if power
                    }
                )
                if coordinates is None:
                    raise AssertionError("row-space signature lacks integer transport")
                actual_sign = -1 if sum(
                    coefficient * rows[index].sign_bit
                    for index, coefficient in coordinates.items()
                ) % 2 else 1
                if sign != actual_sign:
                    raise AssertionError("row-space transport sign changed")
                used.update(coordinates)
                variables.update(variable for variable, _power in monomial)
                node["transports"].append(
                    {
                        "monomial": monomial,
                        "sign": sign,
                        "coordinates": coordinates,
                    }
                )
        elif node["kind"] == "divide":
            variables.update(variable for variable, _power in node["monomial"])

    selected = sorted(used)
    for node in dag:
        for transport in node.get("transports", []):
            coordinates = transport.pop("coordinates")
            transport["coefficients"] = [
                coordinates.get(index, 0) for index in selected
            ]
    relation_origins = [rows[index].origin for index in selected]
    guards = set(
        algebra.binomials.guard_cut(
            assigned,
            positive,
            source_origins + relation_origins,
        )
    )
    if not variables <= positive:
        raise ValueError("a Laurent monomial is not guarded nonzero")
    guards.update(-variable for variable in variables)
    certificate = {
        "schema": "recursive-laurent-row-space-v1",
        "n": args.n,
        "relations": [_origin_data(origin) for origin in relation_origins],
        "dag": dag,
        "contradiction_node": report["contradiction_node"],
        "cut": sorted(guards, key=lambda literal: (abs(literal), literal)),
    }
    result = replay_recursive_row_space(instance, model, certificate)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")

    if args.fixture_output is not None:
        required = set(instance.entries.values()) | set(instance.coefficients.values())
        for origin in source_origins + relation_origins:
            for other in origin.vertices:
                if other != origin.vertex:
                    state = origin.vertices, origin.word
                    edge = tuple(sorted((origin.vertex, other)))
                    required.add(instance.products[(state, edge)])
        fixture = {
            "model": [literal for literal in model if abs(literal) in required],
            "certificate": certificate,
        }
        args.fixture_output.parent.mkdir(parents=True, exist_ok=True)
        args.fixture_output.write_text(
            json.dumps(fixture, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
