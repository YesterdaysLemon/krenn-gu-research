"""Fail-closed semantic audit for the P5 coordinate-support CEGAR ledger.

This auditor is deliberately separate from the discovery loop.  It rebuilds
the SAT variable map, checks every recorded blocking clause against its
recorded support/signature, and recomputes the exact non-Singular
contradiction that is claimed to justify the clause.

Singular unit-ideal rows are checked against their immutable source/log
artifacts by default.  Pass ``--rerun-singular`` to regenerate and rerun every
distinct signature tuple with the current independent Singular invocation.
"""

from __future__ import annotations

import argparse
import collections
import importlib.util
import itertools
import json
import pathlib
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXED_PROBE = ROOT / "tmp" / "probe_p5_max3_coordinate_support.py"
SPEC = importlib.util.spec_from_file_location("p5_fixed_probe_audit", FIXED_PROBE)
FIXED = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(FIXED)
P5 = FIXED.P5


def canonical_clause(clause: list[int]) -> tuple[int, ...]:
    """Canonical literal tuple, rejecting tautologies and repetitions."""
    if len(set(clause)) != len(clause):
        raise AssertionError("clause contains a repeated literal")
    if any(-literal in clause for literal in clause):
        raise AssertionError("clause is tautological")
    return tuple(sorted(clause))


def support_from_signature_indices(
    allowed: tuple[tuple, ...], signature_indices: tuple[int, ...]
) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(allowed[index][0]) for index in signature_indices)


def signature_indices_from_clause(
    pool: Any, clause: list[int]
) -> tuple[int, ...]:
    """Decode one five-local-signature blocking cube."""
    decoded: dict[int, int] = {}
    for literal in clause:
        if literal >= 0:
            raise AssertionError("local-signature cube has a positive literal")
        key = pool.obj(-literal)
        if key is None or key[0] != "local_pattern":
            raise AssertionError("signature cube contains a non-pattern literal")
        _, mode, pattern_index = key
        if mode in decoded:
            raise AssertionError("signature cube repeats a mode")
        decoded[int(mode)] = int(pattern_index)
    if set(decoded) != set(P5.MODES):
        raise AssertionError("signature cube does not specify all five modes")
    return tuple(decoded[mode] for mode in P5.MODES)


def clause_is_false_on_support(
    pool: Any,
    clause: list[int],
    supports: tuple[tuple[int, ...], ...],
    signature_indices: tuple[int, ...] | None,
) -> bool:
    for literal in clause:
        key = pool.obj(abs(literal))
        if key is None:
            raise AssertionError(f"unknown SAT variable {abs(literal)}")
        if key[0] == "x":
            _, mode, source, colour = key
            value = bool(supports[mode][source] & (1 << colour))
        elif key[0] == "local_pattern":
            if signature_indices is None:
                raise AssertionError("pattern literal without a signature tuple")
            _, mode, pattern_index = key
            value = signature_indices[mode] == pattern_index
        else:
            raise AssertionError(f"unsupported learned-clause key {key[0]!r}")
        literal_value = value if literal > 0 else not value
        if literal_value:
            return False
    return True


def viable_signature_tuples(
    allowed: tuple[tuple, ...],
    supports: tuple[tuple[int, ...], ...],
) -> list[tuple[tuple[int, ...], tuple[tuple, ...]]]:
    candidate_lists = [
        [
            pattern_index
            for pattern_index, signature in enumerate(allowed)
            if signature[0] == tuple(supports[mode])
        ]
        for mode in P5.MODES
    ]
    output = []
    for indices in itertools.product(*candidate_lists):
        signatures = tuple(allowed[index] for index in indices)
        if all(
            sum(
                bool(
                    signatures[mode][1][pair_index] & (1 << colour)
                )
                for mode in P5.MODES
            )
            >= 2
            for pair_index in range(10)
            for colour in P5.COLOURS
        ):
            output.append((tuple(indices), signatures))
    return output


def infer_signature_indices(pool: Any, record: dict[str, Any]) -> tuple[int, ...] | None:
    key_kinds = {
        pool.obj(abs(literal))[0] for literal in record["clause"]
    }
    if key_kinds == {"local_pattern"}:
        return signature_indices_from_clause(pool, record["clause"])
    if key_kinds != {"x"}:
        raise AssertionError(f"mixed or unsupported clause key kinds: {key_kinds}")
    return None


def assert_fixed_shape(
    supports: tuple[tuple[int, ...], ...], shape: str
) -> None:
    observed = tuple(
        tuple(
            source
            for source, mask in enumerate(supports[mode])
            if mask not in (1, 2, 4)
        )
        for mode in P5.MODES
    )
    expected = tuple(tuple(row) for row in FIXED.SHAPES[shape])
    if observed != expected:
        raise AssertionError(
            f"fixed-shape mismatch: observed {observed}, expected {expected}"
        )


def audit_record(
    pool: Any,
    allowed: tuple[tuple, ...],
    record: dict[str, Any],
    rerun_singular: bool,
    rerun_algorithm: str = "std",
    rerun_artifact_dir: pathlib.Path | None = None,
) -> dict[str, Any]:
    clause = [int(literal) for literal in record["clause"]]
    canonical_clause(clause)
    supports = tuple(
        tuple(int(mask) for mask in row) for row in record["supports"]
    )
    if len(supports) != 5 or any(len(row) != 5 for row in supports):
        raise AssertionError("support is not a 5 by 5 mask array")
    if any(mask < 0 or mask > 7 for row in supports for mask in row):
        raise AssertionError("support contains an invalid colour mask")

    mode = str(record["contradiction_mode"])
    replayed_mode = mode
    replay_scope = "exact_recorded_mechanism"
    signature_indices = infer_signature_indices(pool, record)
    if signature_indices is not None:
        signature_support = support_from_signature_indices(
            allowed, signature_indices
        )
        if signature_support != supports:
            raise AssertionError("signature cube support differs from record")
    if not clause_is_false_on_support(
        pool, clause, supports, signature_indices
    ):
        raise AssertionError("learned clause is not false on its recorded model")

    lattice_modes = {
        "annihilated_pure_target",
        "inconsistent_binomial_sign",
        "isolated_signed_monomial_class",
    }
    closure_modes = {
        "binomial_closure_annihilated_pure",
        "binomial_closure_isolated_class",
        "local_incidence_forced_rank_one",
    }
    if mode in lattice_modes:
        result = P5.signed_lattice_result(supports)
        if not result["inconsistent"]:
            raise AssertionError("recomputed signed lattice is consistent")
        if result["contradiction_mode"] != mode:
            raise AssertionError(
                f"lattice mode mismatch: {result['contradiction_mode']} != {mode}"
            )
        expected, _, _ = P5.conflict_cube_clause(pool, supports, result)
        if canonical_clause(expected) != canonical_clause(clause):
            raise AssertionError("lattice conflict clause does not replay exactly")

    elif mode == "residual_permanent_collision":
        result = P5.residual_collision_result(supports)
        if result is None:
            raise AssertionError("residual collision no longer replays")
        expected, _, _ = P5.residual_collision_clause(pool, result)
        if canonical_clause(expected) != canonical_clause(clause):
            raise AssertionError("residual-collision clause does not replay")

    elif mode == "factored_residual_permanent_collision":
        result = P5.factored_residual_collision_result(supports)
        if result is None:
            raise AssertionError("factored residual collision no longer replays")
        expected, _, _ = P5.factored_residual_collision_clause(
            pool, supports, result
        )
        if canonical_clause(expected) != canonical_clause(clause):
            raise AssertionError(
                "factored-residual collision clause does not replay"
            )

    elif mode in closure_modes:
        signatures = (
            None
            if signature_indices is None
            else tuple(allowed[index] for index in signature_indices)
        )
        result = P5.binomial_closure_result(supports, signatures)
        if result is None:
            raise AssertionError("binomial closure no longer finds a contradiction")
        replayed_mode = str(result["contradiction_mode"])
        if replayed_mode not in closure_modes:
            raise AssertionError(
                f"closure replay returned unsupported mode {replayed_mode!r}"
            )
        uses_local_incidence = result.get(
            "uses_local_incidence", False
        )
        if signature_indices is None:
            if uses_local_incidence or mode.startswith("local_incidence_"):
                raise AssertionError(
                    "support-only clause unexpectedly needs local incidence"
                )
            expected = P5.exact_support_clause(pool, supports)
        else:
            expected = [
                -pool.id(("local_pattern", local_mode, pattern_index))
                for local_mode, pattern_index in zip(
                    P5.MODES, signature_indices
                )
            ]
            if not uses_local_incidence:
                replay_scope = "stronger_support_level_contradiction"
            elif replayed_mode != mode:
                replay_scope = "alternative_signature_level_contradiction"
        if canonical_clause(expected) != canonical_clause(clause):
            raise AssertionError("binomial-closure clause does not replay exactly")

    elif mode == "local_signature_exhaustion":
        if signature_indices is not None:
            raise AssertionError("signature exhaustion should block exact support")
        viable = viable_signature_tuples(allowed, supports)
        if not viable:
            raise AssertionError("support has no viable local-signature refinement")
        recomputed = []
        for indices, signatures in viable:
            result = P5.binomial_closure_result(supports, signatures)
            if result is None:
                raise AssertionError(
                    f"signature refinement {indices} survives recomputation"
                )
            recomputed.append(
                {
                    "signature_indices": indices,
                    "contradiction_mode": result["contradiction_mode"],
                }
            )
        claimed = record["certificate"]
        if int(claimed["viable_signatures"]) != len(viable):
            raise AssertionError("viable-signature count differs from certificate")
        normalized_claimed = [
            {
                "signature_indices": tuple(item["signature_indices"]),
                "contradiction_mode": item["contradiction_mode"],
            }
            for item in claimed["records"]
        ]
        if normalized_claimed != recomputed:
            raise AssertionError("signature-exhaustion records do not replay")
        expected = P5.exact_support_clause(pool, supports)
        if canonical_clause(expected) != canonical_clause(clause):
            raise AssertionError("exact-support clause does not replay")

    elif mode == "singular_unit_ideal":
        if signature_indices is None:
            raise AssertionError("Singular row lacks a signature cube")
        certificate = record["certificate"]
        if tuple(certificate["signature_indices"]) != signature_indices:
            raise AssertionError("Singular certificate signature tuple differs")
        source = pathlib.Path(certificate["source"])
        log = pathlib.Path(certificate["log"])
        if not source.is_file() or not log.is_file():
            raise AssertionError("Singular source or log artifact is missing")
        source_text = source.read_text(encoding="utf-8")
        log_text = log.read_text(encoding="utf-8")
        order = certificate.get("order")
        if order is None:
            order = (
                "dp"
                if any(
                    line.startswith("ring ") and line.rstrip().endswith(",dp;")
                    for line in source_text.splitlines()
                )
                else None
            )
        algorithm = certificate.get("algorithm")
        if algorithm is None:
            if "ideal G=std(I);" in source_text:
                algorithm = "std"
            elif "ideal G=slimgb(I);" in source_text:
                algorithm = "slimgb"
        if (
            int(certificate["returncode"]) != 0
            or certificate["stdout"].strip() != "UNIT_IDEAL"
            or certificate["stderr"].strip()
            or not certificate["unit_ideal"]
            or order != "dp"
            or algorithm not in {"std", "slimgb"}
        ):
            raise AssertionError("Singular metadata is not a clean unit-ideal run")
        signature_markers = {
            "// signature source: " + str(tuple(signature_indices)),
            "// signature indices: " + str(tuple(signature_indices)),
        }
        if not any(marker in source_text for marker in signature_markers):
            raise AssertionError("Singular source has the wrong signature marker")
        support_marker = "// supports: " + str(supports)
        if support_marker not in source_text:
            raise AssertionError("Singular source has the wrong support marker")
        if "UNIT_IDEAL" not in log_text or "SURVIVOR" in log_text:
            raise AssertionError("Singular log does not certify a unit ideal")
        if rerun_singular:
            replay = P5.run_singular_signature(
                list(signature_indices),
                (
                    rerun_artifact_dir
                    if rerun_artifact_dir is not None
                    else ROOT / "tmp" / "p5_ledger_audit_reruns"
                ),
                algorithm=rerun_algorithm,
            )
            if (
                replay["returncode"] != 0
                or replay["stdout"].strip() != "UNIT_IDEAL"
                or replay["stderr"].strip()
                or not replay["unit_ideal"]
            ):
                raise AssertionError("independent Singular rerun failed")
        expected = [
            -pool.id(("local_pattern", local_mode, pattern_index))
            for local_mode, pattern_index in zip(P5.MODES, signature_indices)
        ]
        if canonical_clause(expected) != canonical_clause(clause):
            raise AssertionError("Singular signature clause does not replay")

    elif mode == "singular_support_unit_ideal":
        if signature_indices is not None:
            raise AssertionError(
                "support-level Singular row must use an entry-support clause"
            )
        certificate = record["certificate"]
        certificate_indices = tuple(certificate["signature_indices"])
        if support_from_signature_indices(
            allowed, certificate_indices
        ) != supports:
            raise AssertionError(
                "support-level Singular certificate has the wrong support"
            )
        source = pathlib.Path(certificate["source"])
        log = pathlib.Path(certificate["log"])
        if not source.is_file() or not log.is_file():
            raise AssertionError("Singular source or log artifact is missing")
        source_text = source.read_text(encoding="utf-8")
        log_text = log.read_text(encoding="utf-8")
        order = certificate.get("order")
        if order is None:
            order = (
                "dp"
                if any(
                    line.startswith("ring ") and line.rstrip().endswith(",dp;")
                    for line in source_text.splitlines()
                )
                else None
            )
        algorithm = certificate.get("algorithm")
        if algorithm is None:
            if "ideal G=std(I);" in source_text:
                algorithm = "std"
            elif "ideal G=slimgb(I);" in source_text:
                algorithm = "slimgb"
        if (
            int(certificate["returncode"]) != 0
            or certificate["stdout"].strip() != "UNIT_IDEAL"
            or certificate["stderr"].strip()
            or not certificate["unit_ideal"]
            or not certificate.get("support_only")
            or order != "dp"
            or algorithm not in {"std", "slimgb"}
        ):
            raise AssertionError(
                "Singular metadata is not a clean support-level unit-ideal run"
            )
        signature_marker = (
            "// signature source: " + str(certificate_indices)
        )
        support_marker = "// supports: " + str(supports)
        if signature_marker not in source_text:
            raise AssertionError("Singular source has the wrong signature marker")
        if support_marker not in source_text:
            raise AssertionError("Singular source has the wrong support marker")
        if "// coefficient stratum: exact support only" not in source_text:
            raise AssertionError(
                "Singular source is not an exact-support stratum"
            )
        if "UNIT_IDEAL" not in log_text or "SURVIVOR" in log_text:
            raise AssertionError("Singular log does not certify a unit ideal")
        if rerun_singular:
            replay = P5.run_singular_signature(
                list(certificate_indices),
                (
                    rerun_artifact_dir
                    if rerun_artifact_dir is not None
                    else ROOT / "tmp" / "p5_ledger_audit_reruns"
                ),
                support_only=True,
                algorithm=rerun_algorithm,
            )
            if (
                replay["returncode"] != 0
                or replay["stdout"].strip() != "UNIT_IDEAL"
                or replay["stderr"].strip()
                or not replay["unit_ideal"]
            ):
                raise AssertionError(
                    "independent support-level Singular rerun failed"
                )
        expected = P5.exact_support_clause(pool, supports)
        if canonical_clause(expected) != canonical_clause(clause):
            raise AssertionError(
                "Singular support clause does not replay exactly"
            )

    else:
        raise AssertionError(f"unsupported contradiction mode {mode!r}")

    return {
        "mode": mode,
        "replayed_mode": replayed_mode,
        "replay_scope": replay_scope,
        "clause_length": len(clause),
        "signature_indices": signature_indices,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("state", type=pathlib.Path)
    parser.add_argument("--shape", choices=tuple(FIXED.SHAPES))
    parser.add_argument("--rerun-singular", action="store_true")
    parser.add_argument(
        "--rerun-algorithm",
        choices=("std", "slimgb"),
        default="std",
    )
    parser.add_argument(
        "--rerun-artifact-dir",
        type=pathlib.Path,
        default=ROOT / "tmp" / "p5_ledger_audit_reruns",
    )
    args = parser.parse_args()

    state = json.loads(args.state.read_text(encoding="utf-8"))
    if state.get("shape") != args.shape:
        raise AssertionError(
            f"state shape {state.get('shape')!r} != requested {args.shape!r}"
        )
    allowed = P5.finite_field_local_signatures()
    _cnf, pool = P5.build_cnf(
        allowed,
        double_lex=args.shape is None,
        pair_hierarchy=True,
    )
    records = list(state.get("learned_records", []))
    if not records:
        raise AssertionError("state contains no learned records")

    modes: collections.Counter[str] = collections.Counter()
    replayed_modes: collections.Counter[str] = collections.Counter()
    replay_scopes: collections.Counter[str] = collections.Counter()
    mode_drifts: collections.Counter[tuple[str, str]] = collections.Counter()
    clause_lengths: collections.Counter[int] = collections.Counter()
    base_clauses: set[tuple[int, ...]] = set()
    duplicate_base_clauses = 0
    singular_signatures: set[tuple[int, ...]] = set()
    for index, record in enumerate(records):
        try:
            result = audit_record(
                pool,
                allowed,
                record,
                rerun_singular=args.rerun_singular,
                rerun_algorithm=args.rerun_algorithm,
                rerun_artifact_dir=args.rerun_artifact_dir,
            )
        except Exception as error:
            raise AssertionError(
                f"record {index} failed semantic replay: {error}"
            ) from error
        supports = tuple(tuple(row) for row in record["supports"])
        if args.shape is not None:
            assert_fixed_shape(supports, args.shape)
        clause_key = canonical_clause(record["clause"])
        if clause_key in base_clauses:
            duplicate_base_clauses += 1
        else:
            base_clauses.add(clause_key)
        modes[result["mode"]] += 1
        replayed_modes[result["replayed_mode"]] += 1
        replay_scopes[result["replay_scope"]] += 1
        if result["replayed_mode"] != result["mode"]:
            mode_drifts[
                (result["mode"], result["replayed_mode"])
            ] += 1
        clause_lengths[result["clause_length"]] += 1
        if result["signature_indices"] is not None and result["mode"] == (
            "singular_unit_ideal"
        ):
            singular_signatures.add(result["signature_indices"])
        if (index + 1) % 100 == 0:
            print(
                json.dumps(
                    {
                        "audited": index + 1,
                        "total": len(records),
                        "last_mode": result["mode"],
                    }
                ),
                flush=True,
            )

    payload = {
        "status": "AUDIT_PASS",
        "state": str(args.state),
        "state_status": state.get("status"),
        "shape": args.shape,
        "records": len(records),
        "unique_base_clauses": len(base_clauses),
        "duplicate_base_clauses": duplicate_base_clauses,
        "modes": dict(sorted(modes.items())),
        "replayed_modes": dict(sorted(replayed_modes.items())),
        "replay_scopes": dict(sorted(replay_scopes.items())),
        "mode_drifts": {
            f"{recorded} -> {replayed}": count
            for (recorded, replayed), count in sorted(mode_drifts.items())
        },
        "clause_lengths": {
            str(length): count for length, count in sorted(clause_lengths.items())
        },
        "singular_signature_tuples": len(singular_signatures),
        "singular_rerun": args.rerun_singular,
        "singular_rerun_algorithm": (
            args.rerun_algorithm if args.rerun_singular else None
        ),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
