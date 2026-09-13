"""Build a small unit-propagation core for one replayed algebraic clause.

The input model supplies only a conditional coefficient template.  The
physical support is fixed independently (or derived from that model), the
recursive target instance is regenerated without killers or ratio clauses,
and the emitted packet is accepted only after the solver-free source-core
replayer checks it.
"""

from __future__ import annotations

import argparse
import json
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

from krenn_gu.recursive_tensor_support import (  # noqa: E402
    build_recursive_tensor_support_cnf,
)
from krenn_gu.source_quotient_core import (  # noqa: E402
    replay_guarded_algebraic_clause,
    replay_source_quotient_core,
    source_algebra_origins,
    unit_propagation_core,
)


def _read_json(path: _BootstrapPath):
    return json.loads(path.read_text(encoding="utf-8"))


def _unwrap_model(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("model"), list):
        return payload["model"]
    raise ValueError("model JSON must be a literal list or contain a model list")


def _unwrap_certificate(payload):
    if not isinstance(payload, dict):
        raise ValueError("certificate JSON must be an object")
    while set(payload) >= {"certificate"} and isinstance(payload["certificate"], dict):
        payload = payload["certificate"]
    return payload


def _positive_entries(payload, instance, model):
    if payload is None:
        positive = {literal for literal in model if literal > 0}
        return positive & set(instance.entries.values())
    if isinstance(payload, dict) and isinstance(payload.get("nonzero_entry_ids"), list):
        values = payload["nonzero_entry_ids"]
    elif isinstance(payload, list):
        values = payload
    else:
        raise ValueError("support JSON must be a list or contain nonzero_entry_ids")
    if any(type(value) is not int or value <= 0 for value in values):
        raise ValueError("nonzero entry ids must be positive integers")
    positive = set(values)
    if not positive <= set(instance.entries.values()):
        raise ValueError("support contains a non-entry variable")
    return positive


def build_packet(n, model, certificate, support_payload=None):
    instance = build_recursive_tensor_support_cnf(
        n,
        column_killers=False,
        fix_root_killers=False,
    )
    if any(type(literal) is not int for literal in model):
        raise ValueError("model literals must be integers")
    positive = {literal for literal in model if literal > 0}
    replay = replay_guarded_algebraic_clause(instance, model, certificate)
    positive_entries = _positive_entries(support_payload, instance, model)
    entry_support = [
        variable if variable in positive_entries else -variable
        for variable in instance.entries.values()
    ]

    coefficient_ids = set(instance.coefficients.values())
    needed = set()
    for origin in source_algebra_origins(certificate):
        state = origin.vertices, origin.word
        needed.add(instance.coefficients[state])
        for other in origin.vertices:
            if other == origin.vertex:
                continue
            edge = tuple(sorted((origin.vertex, other)))
            first, second = instance.product_factors(state, edge)
            if first in coefficient_ids:
                needed.add(first)
            if second in coefficient_ids:
                needed.add(second)

    full_formula = [*instance.cnf.clauses]
    full_formula.extend((literal,) for literal in entry_support)
    full_formula.append(replay["clause"])
    core = unit_propagation_core(full_formula)
    if core is None:
        raise RuntimeError(
            "the checked algebraic clause does not unit-refute this physical support"
        )
    if replay["clause"] not in {_canonical(clause) for clause in core}:
        raise RuntimeError("the extracted conflict does not use the algebraic clause")
    entry_ids = set(instance.entries.values())
    physical_cut = sorted(
        {
            -clause[0]
            for clause in core
            if len(clause) == 1 and abs(clause[0]) in entry_ids
        },
        key=lambda literal: (abs(literal), literal),
    )
    packet = {
        "schema": "recursive-source-algebra-core-v2",
        "n": n,
        "scope": "conditional physical-support exclusion; not a parent cover",
        "entry_support": entry_support,
        "coefficient_support": [
            [variable, int(variable in positive)] for variable in sorted(needed)
        ],
        "algebra_certificate": certificate,
        "core_clauses": [list(clause) for clause in core],
        "rup_additions": [[]],
        "physical_cut": physical_cut,
    }
    result = replay_source_quotient_core(instance, packet)
    return packet, result


def _canonical(clause):
    return tuple(sorted(set(clause)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--model", type=_BootstrapPath, required=True)
    parser.add_argument("--certificate", type=_BootstrapPath)
    parser.add_argument("--support", type=_BootstrapPath)
    parser.add_argument("--output", type=_BootstrapPath, required=True)
    args = parser.parse_args()
    model_payload = _read_json(args.model)
    model = _unwrap_model(model_payload)
    if args.certificate is None:
        certificate = _unwrap_certificate(model_payload)
    else:
        certificate = _unwrap_certificate(_read_json(args.certificate))
    support = _read_json(args.support) if args.support else None
    packet, result = build_packet(args.n, model, certificate, support)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
