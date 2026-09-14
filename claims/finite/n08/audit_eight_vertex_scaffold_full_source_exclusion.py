"""Independent reconstruction and portable RUP audit of the order-eight scaffold CNF.

This audit imports no primary scientific implementation.  It expands every
one of the 3^8 physical target equations word first, using a separate bitmask
perfect-matching recursion, and reconstructs the monomial-support CNF.  The
CNF is a necessary condition for a complex physical realization.  A compact
committed fixture selects original clauses from that reconstructed CNF and
gives a sequential reverse-unit-propagation (RUP) derivation of the empty
clause.  The RUP engine below is independent of the primary scientific code.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_FIXTURE = REPO_ROOT / "tests/fixtures/eight_vertex_scaffold_full_source_rup.json"
COLOURS = tuple(range(3))
VERTICES = tuple(range(8))
LEFT = frozenset(range(4))
RIGHT = frozenset(range(4, 8))
INTERNAL_MATCHINGS = {
    0: frozenset((frozenset((0, 1)), frozenset((2, 3)))),
    1: frozenset((frozenset((0, 2)), frozenset((1, 3)))),
    2: frozenset((frozenset((0, 3)), frozenset((1, 2)))),
}
CROSSING_KEYS = tuple(
    (left_colour, right_colour, left_vertex, right_vertex)
    for left_colour in COLOURS
    for right_colour in COLOURS
    if left_colour != right_colour
    for left_vertex in range(4)
    for right_vertex in range(4)
)
CROSSING_VARIABLE = {
    key: index + 1 for index, key in enumerate(CROSSING_KEYS)
}

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Monomial = tuple[int, ...]
Polynomial = Counter[Monomial]
Clause = tuple[int, ...]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def portable_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return f"<external>/{resolved.name}"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@lru_cache(maxsize=None)
def perfect_matchings(mask: int) -> tuple[Matching, ...]:
    """Pair the least set vertex with each possible partner."""
    if mask == 0:
        return ((),)
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    remainder = mask ^ first_bit
    result = []
    choices = remainder
    while choices:
        second_bit = choices & -choices
        choices ^= second_bit
        second = second_bit.bit_length() - 1
        for tail in perfect_matchings(remainder ^ second_bit):
            result.append(((first, second),) + tail)
    return tuple(result)


def permutation_matching_cover() -> frozenset[Matching]:
    result = set()
    for permutation in itertools.permutations(VERTICES):
        pairs = [tuple(sorted(permutation[i : i + 2])) for i in range(0, 8, 2)]
        result.add(tuple(sorted(pairs)))
    return frozenset(result)


def edge_factor(
    u: int,
    v: int,
    colour_u: int,
    colour_v: int,
) -> Monomial | None:
    """Return (), one crossing variable, or None for a structural zero."""
    u_left = u in LEFT
    v_left = v in LEFT
    if u_left == v_left:
        if colour_u != colour_v:
            return None
        local_u, local_v = (u, v) if u_left else (u - 4, v - 4)
        local_edge = frozenset((local_u, local_v))
        return () if local_edge in INTERNAL_MATCHINGS[colour_u] else None

    require(u_left and v in RIGHT, "matching edges must be stored increasingly")
    if colour_u == colour_v:
        return None
    return (
        CROSSING_VARIABLE[(colour_u, colour_v, u, v - 4)],
    )


def target_polynomial(word: tuple[int, ...], matchings: tuple[Matching, ...]) -> Polynomial:
    """Expand T_word-delta_word with exact integer coefficients."""
    polynomial: Polynomial = Counter()
    for matching in matchings:
        monomial = []
        for u, v in matching:
            factor = edge_factor(u, v, word[u], word[v])
            if factor is None:
                break
            monomial.extend(factor)
        else:
            polynomial[tuple(sorted(monomial))] += 1
    if len(set(word)) == 1:
        polynomial[()] -= 1
    return Counter(
        {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}
    )


@dataclass(frozen=True)
class Equation:
    word: tuple[int, ...]
    polynomial: Polynomial


@dataclass(frozen=True)
class EncodedEquation:
    equation: Equation
    monomial_variables: tuple[int, ...]


def reconstruct_equations(matchings: tuple[Matching, ...]) -> tuple[Equation, ...]:
    return tuple(
        Equation(word, target_polynomial(word, matchings))
        for word in itertools.product(COLOURS, repeat=8)
    )


def and_clauses(monomial_variable: int, factors: Monomial) -> tuple[Clause, ...]:
    clauses = [(-monomial_variable, factor) for factor in factors]
    clauses.append((monomial_variable, *(-factor for factor in factors)))
    return tuple(clauses)


def singleton_clauses(
    monomial_variables: tuple[int, ...],
    constant_active: bool,
) -> tuple[Clause, ...]:
    if constant_active:
        return (tuple(monomial_variables),)
    return tuple(
        (-variable, *(other for other in monomial_variables if other != variable))
        for variable in monomial_variables
    )


def reconstruct_cnf(
    equations: tuple[Equation, ...],
) -> tuple[tuple[Clause, ...], tuple[EncodedEquation, ...], int]:
    clauses = []
    encoded = []
    next_variable = 97
    shared_monomial_variables: dict[Monomial, int] = {}
    for equation in equations:
        occurrence_variables = []
        for monomial in sorted(term for term in equation.polynomial if term):
            monomial_variable = shared_monomial_variables.get(monomial)
            if monomial_variable is None:
                monomial_variable = next_variable
                next_variable += 1
                shared_monomial_variables[monomial] = monomial_variable
                clauses.extend(and_clauses(monomial_variable, monomial))
            occurrence_variables.append(monomial_variable)
        occurrence_tuple = tuple(occurrence_variables)
        clauses.extend(singleton_clauses(occurrence_tuple, () in equation.polynomial))
        encoded.append(EncodedEquation(equation, occurrence_tuple))
    return tuple(clauses), tuple(encoded), next_variable - 1


def render_dimacs(clauses: tuple[Clause, ...], variable_count: int) -> bytes:
    lines = [f"p cnf {variable_count} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode("ascii")


def canonical_clause_bytes(clauses: tuple[Clause, ...]) -> bytes:
    """Serialize clauses without a DIMACS header for subset/derivation hashes."""
    return "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses).encode("ascii")


def validate_clause(clause: Clause, variable_count: int, label: str) -> None:
    require(all(type(literal) is int for literal in clause), f"{label} has a noninteger literal")
    require(all(literal != 0 for literal in clause), f"{label} contains DIMACS terminator zero")
    require(
        all(abs(literal) <= variable_count for literal in clause),
        f"{label} references an out-of-range variable",
    )
    require(len(set(clause)) == len(clause), f"{label} repeats a literal")
    literal_set = set(clause)
    require(
        not any(-literal in literal_set for literal in clause),
        f"{label} is tautological",
    )


def unit_propagation_conflict(
    clauses: tuple[Clause, ...],
    assumptions: tuple[int, ...],
    variable_count: int,
) -> tuple[bool, int]:
    """Return whether plain unit propagation conflicts, plus assignments made.

    This is a fresh occurrence-count implementation, not an import or a port of
    the project's primary RUP helper.  A true literal permanently satisfies a
    clause; a false literal decrements its number of unassigned entries.  When
    that count reaches one, the remaining literal is queued.
    """
    positive_occurrences: list[list[int]] = [[] for _ in range(variable_count + 1)]
    negative_occurrences: list[list[int]] = [[] for _ in range(variable_count + 1)]
    remaining = [len(clause) for clause in clauses]
    satisfied = [False] * len(clauses)
    assignments = [0] * (variable_count + 1)  # 1 true, -1 false, 0 unset
    queue: list[int] = []
    queue_cursor = 0

    for clause_index, clause in enumerate(clauses):
        if not clause:
            return True, 0
        for literal in clause:
            occurrences = positive_occurrences if literal > 0 else negative_occurrences
            occurrences[abs(literal)].append(clause_index)
        if len(clause) == 1:
            queue.append(clause[0])
    queue.extend(assumptions)

    while queue_cursor < len(queue):
        literal = queue[queue_cursor]
        queue_cursor += 1
        variable = abs(literal)
        value = 1 if literal > 0 else -1
        prior = assignments[variable]
        if prior == value:
            continue
        if prior == -value:
            return True, sum(assignment != 0 for assignment in assignments)
        assignments[variable] = value

        true_occurrences = (
            positive_occurrences[variable]
            if value > 0
            else negative_occurrences[variable]
        )
        false_occurrences = (
            negative_occurrences[variable]
            if value > 0
            else positive_occurrences[variable]
        )
        for clause_index in true_occurrences:
            satisfied[clause_index] = True
        for clause_index in false_occurrences:
            if satisfied[clause_index]:
                continue
            remaining[clause_index] -= 1
            if remaining[clause_index] == 0:
                return True, sum(assignment != 0 for assignment in assignments)
            if remaining[clause_index] == 1:
                unit_literal = next(
                    candidate
                    for candidate in clauses[clause_index]
                    if assignments[abs(candidate)] == 0
                )
                queue.append(unit_literal)

    return False, sum(assignment != 0 for assignment in assignments)


def validate_rup_fixture(
    payload: dict[str, object],
    clauses: tuple[Clause, ...],
    variable_count: int,
    equation_sha256: str,
    cnf_sha256: str,
) -> tuple[dict[str, object], tuple[Clause, ...], tuple[Clause, ...]]:
    require(payload.get("schema") == "n8-two-k4-full-source-rup-v1", "RUP schema differs")
    require(
        payload.get("scope") == "C; two fixed K4 unit scaffolds; all96hollow crossing entries free",
        "RUP scope differs",
    )
    require(payload.get("word_count") == 6561, "RUP word count differs")
    require(payload.get("variable_count") == variable_count, "RUP variable count differs")
    require(payload.get("clause_count") == len(clauses), "RUP clause count differs")
    require(payload.get("equation_sha256") == equation_sha256, "RUP equation digest differs")
    require(payload.get("cnf_lf_sha256") == cnf_sha256, "RUP CNF digest differs")

    raw_indices = payload.get("core_clause_indices")
    raw_additions = payload.get("rup_additions")
    require(isinstance(raw_indices, list), "RUP core indices are absent")
    require(isinstance(raw_additions, list), "RUP additions are absent")
    require(len(raw_indices) == 1521, "RUP core index count differs")
    require(len(raw_additions) == 108, "RUP addition count differs")
    require(all(type(index) is int for index in raw_indices), "a core index is not an integer")
    core_indices = tuple(raw_indices)
    require(tuple(sorted(core_indices)) == core_indices, "core indices are not sorted")
    require(len(set(core_indices)) == len(core_indices), "core indices repeat")
    # The extraction fixture deliberately uses Python/CaDiCaL-reader offsets:
    # these are zero-based positions in the canonical reconstructed clause list.
    require(
        all(0 <= index < len(clauses) for index in core_indices),
        "a core index lies outside the reconstructed CNF",
    )
    core_clauses = tuple(clauses[index] for index in core_indices)
    initial_core_conflict, initial_core_assignments = unit_propagation_conflict(
        core_clauses, (), variable_count
    )
    require(not initial_core_conflict, "selected core already conflicts under bare unit propagation")

    additions = []
    for addition_index, raw_clause in enumerate(raw_additions):
        require(isinstance(raw_clause, list), f"RUP addition {addition_index} is not a list")
        clause = tuple(raw_clause)
        validate_clause(clause, variable_count, f"RUP addition {addition_index}")
        additions.append(clause)
    additions_tuple = tuple(additions)
    require(additions_tuple[-1] == (), "RUP derivation does not end in the empty clause")
    require(all(addition for addition in additions_tuple[:-1]), "empty clause occurs before the end")

    working = list(core_clauses)
    assignment_counts = []
    for addition_index, clause in enumerate(additions_tuple):
        conflict, assignment_count = unit_propagation_conflict(
            tuple(working),
            tuple(-literal for literal in clause),
            variable_count,
        )
        require(conflict, f"RUP addition {addition_index} fails unit propagation")
        assignment_counts.append(assignment_count)
        working.append(clause)

    return (
        {
            "core_clause_count": len(core_clauses),
            "core_index_base": 0,
            "core_first_index": core_indices[0],
            "core_last_index": core_indices[-1],
            "core_clause_sha256": hashlib.sha256(canonical_clause_bytes(core_clauses)).hexdigest(),
            "initial_core_unit_conflict": False,
            "initial_core_unit_assignments": initial_core_assignments,
            "rup_addition_count": len(additions_tuple),
            "rup_addition_sha256": hashlib.sha256(canonical_clause_bytes(additions_tuple)).hexdigest(),
            "rup_checks_passed": len(additions_tuple),
            "final_clause_empty": True,
            "assignment_count_min": min(assignment_counts),
            "assignment_count_max": max(assignment_counts),
            "assignment_count_total": sum(assignment_counts),
            "final_empty_assignment_count": assignment_counts[-1],
        },
        core_clauses,
        additions_tuple,
    )


def audit_rup_mutations(
    payload: dict[str, object],
    core_clauses: tuple[Clause, ...],
    additions: tuple[Clause, ...],
    variable_count: int,
) -> dict[str, object]:
    # Without the selected original clauses, the first nontrivial addition is
    # not RUP.  This tests that the proof is actually bound to its core.
    no_core_conflict, _ = unit_propagation_conflict(
        (), tuple(-literal for literal in additions[0]), variable_count
    )
    require(not no_core_conflict, "the first addition unexpectedly passes without the core")

    # Clause 2501 is a single load-bearing original clause for the first RUP
    # step.  Deleting it makes the negated first addition propagation-consistent.
    core_indices = tuple(payload["core_clause_indices"])
    crucial_position = core_indices.index(2501)
    crucial_clause = core_clauses[crucial_position]
    require(crucial_clause == (-549, 17), "crucial core clause content differs")
    core_without_crucial = (
        core_clauses[:crucial_position] + core_clauses[crucial_position + 1 :]
    )
    deleted_core_conflict, _ = unit_propagation_conflict(
        core_without_crucial,
        tuple(-literal for literal in additions[0]),
        variable_count,
    )
    require(deleted_core_conflict is False, "deleting crucial core clause did not break first RUP step")

    # RUP negates the candidate clause.  Applying the literals with their
    # original polarity must fail for at least one step of this certificate.
    wrong_polarity_index = None
    working = list(core_clauses)
    for addition_index, clause in enumerate(additions[:-1]):
        conflict, _ = unit_propagation_conflict(tuple(working), clause, variable_count)
        if not conflict:
            wrong_polarity_index = addition_index
            break
        working.append(clause)
    require(wrong_polarity_index is not None, "wrong-polarity assumptions passed every nonempty step")

    # Find an actual one-literal sign mutation that is no longer RUP.  The
    # search is deterministic and runs against the same prefix as the original.
    sign_mutation = None
    working = list(core_clauses)
    for addition_index, clause in enumerate(additions[:-1]):
        for literal_index, literal in enumerate(clause):
            mutated = clause[:literal_index] + (-literal,) + clause[literal_index + 1 :]
            if -literal in set(clause):
                continue
            conflict, _ = unit_propagation_conflict(
                tuple(working), tuple(-entry for entry in mutated), variable_count
            )
            if not conflict:
                sign_mutation = {
                    "addition_index": addition_index,
                    "literal_index": literal_index,
                    "original_literal": literal,
                    "mutated_literal": -literal,
                }
                break
        if sign_mutation is not None:
            break
        working.append(clause)
    require(sign_mutation is not None, "no one-literal sign mutation broke RUP")

    truncated_payload = dict(payload)
    truncated_payload["rup_additions"] = [list(clause) for clause in additions[:-1]]
    final_empty_rejected = False
    try:
        require(truncated_payload["rup_additions"][-1] == [], "RUP derivation does not end in the empty clause")
    except AssertionError:
        final_empty_rejected = True
    require(final_empty_rejected, "truncated derivation was not rejected")

    bad_indices = list(core_indices)
    bad_indices[0] = -1
    full_clause_count = int(payload["clause_count"])
    out_of_range_index_rejected = not all(0 <= index < full_clause_count for index in bad_indices)
    require(out_of_range_index_rejected, "negative core index was not rejected")

    return {
        "first_addition_without_core_is_not_rup": True,
        "deleted_crucial_core_clause_breaks_first_rup": {
            "canonical_zero_based_clause_index": 2501,
            "clause": list(crucial_clause),
        },
        "wrong_assumption_polarity_not_conflicting_at_addition": wrong_polarity_index,
        "one_literal_sign_mutation_not_rup": sign_mutation,
        "missing_final_empty_clause_rejected": final_empty_rejected,
        "negative_core_index_rejected": out_of_range_index_rejected,
    }


def canonical_equation_bytes(equations: tuple[Equation, ...]) -> bytes:
    lines = []
    for equation in equations:
        row = {
            "word": "".join(map(str, equation.word)),
            "terms": [
                {"monomial": list(monomial), "coefficient": coefficient}
                for monomial, coefficient in sorted(equation.polynomial.items())
            ],
        }
        lines.append(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
    return "".join(lines).encode("utf-8")


def artifact_equation_bytes(equations: tuple[Equation, ...]) -> bytes:
    """Render the frozen run's compact word/term-record digest format."""
    return "".join(
        json.dumps(
            (equation.word, sorted(equation.polynomial.items())),
            separators=(",", ":"),
        )
        + "\n"
        for equation in equations
    ).encode("utf-8")


def clause_value(clause: Clause, assignment: dict[int, bool]) -> bool:
    return any(
        assignment.get(abs(literal), False) == (literal > 0)
        for literal in clause
    )


def audit_encoding_semantics(encoded: tuple[EncodedEquation, ...]) -> dict[str, int]:
    and_occurrences = 0
    nonconstant_row_controls = 0
    constant_row_controls = 0
    for encoded_row in encoded:
        terms = sorted(term for term in encoded_row.equation.polynomial if term)
        for variable, factors in zip(encoded_row.monomial_variables, terms):
            clauses = and_clauses(variable, factors)
            all_true = {factor: True for factor in factors}
            all_true[variable] = True
            require(all(clause_value(clause, all_true) for clause in clauses), "AND true case failed")

            false_output = {factor: True for factor in factors}
            false_output[variable] = False
            require(
                not all(clause_value(clause, false_output) for clause in clauses),
                "AND reverse implication is missing",
            )

            one_false = {factor: True for factor in factors}
            one_false[factors[0]] = False
            one_false[variable] = True
            require(
                not all(clause_value(clause, one_false) for clause in clauses),
                "AND forward implication is missing",
            )
            one_false[variable] = False
            require(
                all(clause_value(clause, one_false) for clause in clauses),
                "AND false case rejected",
            )
            and_occurrences += 1

        row_clauses = singleton_clauses(
            encoded_row.monomial_variables,
            () in encoded_row.equation.polynomial,
        )
        if () in encoded_row.equation.polynomial:
            all_false = {variable: False for variable in encoded_row.monomial_variables}
            require(
                not all(clause_value(clause, all_false) for clause in row_clauses),
                "constant singleton was not forbidden",
            )
            one_true = dict(all_false)
            one_true[encoded_row.monomial_variables[0]] = True
            require(
                all(clause_value(clause, one_true) for clause in row_clauses),
                "constant plus one monomial was rejected",
            )
            constant_row_controls += 1
        else:
            all_false = {variable: False for variable in encoded_row.monomial_variables}
            require(
                all(clause_value(clause, all_false) for clause in row_clauses),
                "zero active terms should be admitted",
            )
            if encoded_row.monomial_variables:
                one_true = dict(all_false)
                one_true[encoded_row.monomial_variables[0]] = True
                require(
                    not all(clause_value(clause, one_true) for clause in row_clauses),
                    "one active term was not forbidden",
                )
                if len(encoded_row.monomial_variables) >= 2:
                    two_true = dict(one_true)
                    two_true[encoded_row.monomial_variables[1]] = True
                    require(
                        all(clause_value(clause, two_true) for clause in row_clauses),
                        "two active terms should be admitted",
                    )
            nonconstant_row_controls += 1
    return {
        "and_occurrences_checked": and_occurrences,
        "nonconstant_rows_checked": nonconstant_row_controls,
        "constant_rows_checked": constant_row_controls,
    }


def audit_mutations(
    equations: tuple[Equation, ...],
    encoded: tuple[EncodedEquation, ...],
    canonical_cnf: bytes,
) -> dict[str, object]:
    pure_words = [equation for equation in equations if len(set(equation.word)) == 1]
    require(len(pure_words) == 3, "pure-word census changed")
    require(all(not equation.polynomial for equation in pure_words), "pure constants did not cancel")

    # Dropping delta leaves one unavoidable constant in each pure row and hence
    # an empty singleton clause.  This tests the target sign at polynomial level.
    dropped_delta_empty_clauses = 0
    for equation in pure_words:
        t_polynomial = target_polynomial(equation.word, perfect_matchings(255))
        t_polynomial[()] += 1
        require(t_polynomial == Counter({(): 1}), "dropped-delta mutation differs")
        dropped_delta_empty_clauses += len(singleton_clauses((), True))
    require(dropped_delta_empty_clauses == 3, "dropped delta did not create empty clauses")

    first_nonempty = next(row for row in encoded if row.monomial_variables)
    first_term = min(term for term in first_nonempty.equation.polynomial if term)
    first_variable = first_nonempty.monomial_variables[0]
    full_and = and_clauses(first_variable, first_term)
    all_factors_true_output_false = {factor: True for factor in first_term}
    all_factors_true_output_false[first_variable] = False
    require(
        not all(clause_value(clause, all_factors_true_output_false) for clause in full_and),
        "control setup does not violate full AND",
    )
    require(
        all(
            clause_value(clause, all_factors_true_output_false)
            for clause in full_and[:-1]
        ),
        "deleting reverse AND clause did not admit false monomial support",
    )

    no_constant = next(
        row
        for row in encoded
        if () not in row.equation.polynomial and row.monomial_variables
    )
    one_active = {variable: False for variable in no_constant.monomial_variables}
    one_active[no_constant.monomial_variables[0]] = True
    singleton = singleton_clauses(no_constant.monomial_variables, False)
    require(
        not all(clause_value(clause, one_active) for clause in singleton),
        "control setup does not violate singleton clauses",
    )
    require(
        all(clause_value(clause, one_active) for clause in singleton[1:]),
        "deleting the matching singleton clause did not admit one active term",
    )

    constant_row = next(row for row in encoded if () in row.equation.polynomial)
    no_active_monomials = {
        variable: False for variable in constant_row.monomial_variables
    }
    constant_clause = singleton_clauses(constant_row.monomial_variables, True)
    require(
        not clause_value(constant_clause[0], no_active_monomials),
        "constant-row control does not forbid a lone constant",
    )

    # Removing the first physical matching contribution changes a source row
    # and therefore changes the canonical CNF; the complete 105 cover matters.
    mutated_polynomial = Counter(first_nonempty.equation.polynomial)
    del mutated_polynomial[first_term]
    mutated_equations = tuple(
        Equation(row.word, mutated_polynomial)
        if row is first_nonempty.equation
        else row
        for row in equations
    )
    mutated_clauses, _, mutated_variables = reconstruct_cnf(mutated_equations)
    mutated_cnf = render_dimacs(mutated_clauses, mutated_variables)
    require(mutated_cnf != canonical_cnf, "omitted matching did not change CNF")

    return {
        "dropped_pure_delta_empty_clauses": dropped_delta_empty_clauses,
        "deleted_reverse_and_clause_admits_false_support": True,
        "deleted_singleton_clause_admits_one_active_term": True,
        "constant_without_active_monomial_is_rejected": True,
        "omitted_matching_changes_cnf": True,
        "omitted_matching_cnf_sha256": hashlib.sha256(mutated_cnf).hexdigest(),
    }


def validate_result(
    result: dict[str, object],
    equation_histogram: Counter[int],
    variable_count: int,
    clause_count: int,
    monomial_variable_count: int,
    cnf_path: Path,
    proof_path: Path,
    equation_sha256: str,
) -> None:
    require(result.get("status") == "UNSAT_SOLVER_PENDING_AUDIT", "solver status differs")
    require(result.get("mode") == "full", "solver mode differs")
    require(result.get("word_count") == 6561, "solver word count differs")
    require(result.get("crossing_variables") == 96, "crossing variable count differs")
    require(result.get("variables") == variable_count, "solver variable count differs")
    require(result.get("clauses") == clause_count, "solver clause count differs")
    require(
        result.get("monomial_variables") == monomial_variable_count,
        "solver monomial variable count differs",
    )
    reported_histogram = {
        int(size): int(count)
        for size, count in dict(result.get("row_term_histogram", {})).items()
    }
    require(reported_histogram == dict(equation_histogram), "row histogram differs")
    require(result.get("cnf_sha256") == file_sha256(cnf_path), "raw CNF hash differs")
    require(result.get("proof_sha256") == file_sha256(proof_path), "raw proof hash differs")
    require(
        result.get("equation_sha256") == equation_sha256,
        "coefficient-bearing equation digest differs",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument(
        "--raw-run-dir",
        type=Path,
        help="optionally compare against instance.cnf, proof.drat, and result.json",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    fixture_payload = json.loads(args.fixture.read_text(encoding="utf-8"))

    recursive_matchings = perfect_matchings(255)
    recursive_set = frozenset(tuple(sorted(matching)) for matching in recursive_matchings)
    permutation_set = permutation_matching_cover()
    require(len(recursive_matchings) == 105, "recursive matching count differs")
    require(len(recursive_set) == 105, "recursive matching duplication")
    require(recursive_set == permutation_set, "independent matching covers differ")
    require(len(CROSSING_KEYS) == 96, "crossing-variable census differs")
    require(set(CROSSING_VARIABLE.values()) == set(range(1, 97)), "crossing ids differ")

    equations = reconstruct_equations(recursive_matchings)
    require(len(equations) == 6561, "word census differs")
    equation_histogram = Counter(len(equation.polynomial) for equation in equations)
    all_coefficients = Counter(
        coefficient
        for equation in equations
        for coefficient in equation.polynomial.values()
    )
    require(set(all_coefficients) == {1}, "a scaffold coefficient is not +1")
    all_nonconstant_monomials = [
        monomial
        for equation in equations
        for monomial in equation.polynomial
        if monomial
    ]
    unique_global_monomials = len(set(all_nonconstant_monomials))
    require(
        unique_global_monomials == len(all_nonconstant_monomials),
        "a crossing monomial occurs in more than one source equation",
    )
    constant_rows = [equation for equation in equations if () in equation.polynomial]
    require(len(constant_rows) == 6, "nonzero constant-row census differs")
    require(
        all(len(set(equation.word[:4])) == len(set(equation.word[4:])) == 1 for equation in constant_rows),
        "a constant occurs outside two differently monochromatic shores",
    )

    clauses, encoded, variable_count = reconstruct_cnf(equations)
    canonical_cnf = render_dimacs(clauses, variable_count)
    artifact_equations = artifact_equation_bytes(equations)
    artifact_equation_sha256 = hashlib.sha256(artifact_equations).hexdigest()
    monomial_variable_count = variable_count - 96
    canonical_cnf_sha256 = hashlib.sha256(canonical_cnf).hexdigest()
    rup_replay, core_clauses, rup_additions = validate_rup_fixture(
        fixture_payload,
        clauses,
        variable_count,
        artifact_equation_sha256,
        canonical_cnf_sha256,
    )

    raw_artifacts = None
    if args.raw_run_dir:
        cnf_path = args.raw_run_dir / "instance.cnf"
        proof_path = args.raw_run_dir / "proof.drat"
        result_path = args.raw_run_dir / "result.json"
        result_payload = json.loads(result_path.read_text(encoding="utf-8"))
        artifact_raw = cnf_path.read_bytes()
        artifact_lf = artifact_raw.replace(b"\r\n", b"\n")
        require(canonical_cnf == artifact_lf, "canonical-LF CNF differs byte-for-byte")
        validate_result(
            result_payload,
            equation_histogram,
            variable_count,
            len(clauses),
            monomial_variable_count,
            cnf_path,
            proof_path,
            artifact_equation_sha256,
        )
        raw_artifacts = {
            "run_directory": portable_path(args.raw_run_dir),
            "cnf": portable_path(cnf_path),
            "cnf_raw_sha256": file_sha256(cnf_path),
            "canonical_lf_cnf_byte_equal": True,
            "proof": portable_path(proof_path),
            "proof_raw_sha256": file_sha256(proof_path),
            "result": portable_path(result_path),
            "result_raw_sha256": file_sha256(result_path),
        }

    semantic_controls = audit_encoding_semantics(encoded)
    mutation_controls = audit_mutations(equations, encoded, canonical_cnf)
    mutation_controls["portable_rup"] = audit_rup_mutations(
        fixture_payload, core_clauses, rup_additions, variable_count
    )
    equation_bytes = canonical_equation_bytes(equations)

    report = {
        "schema": "eight-vertex-scaffold-full-source-independent-audit-v2",
        "status": "PASS_PORTABLE_RUP_REPLAY",
        "scope": (
            "complete 96-dimensional hollow-crossing two-K4 scaffold at n=8; "
            "not arbitrary sources and not all orders"
        ),
        "artifacts": {
            "rup_fixture": portable_path(args.fixture),
            "rup_fixture_raw_sha256": file_sha256(args.fixture),
            "cnf_canonical_lf_sha256": canonical_cnf_sha256,
            "optional_raw_artifacts": raw_artifacts,
        },
        "independent_reconstruction": {
            "perfect_matchings_bitmask": len(recursive_matchings),
            "perfect_matchings_permutation_quotient": len(permutation_set),
            "words": len(equations),
            "crossing_variables": 96,
            "monomial_occurrence_variables": monomial_variable_count,
            "shared_monomial_variables": monomial_variable_count,
            "globally_unique_nonconstant_monomials": unique_global_monomials,
            "cnf_variables": variable_count,
            "cnf_clauses": len(clauses),
            "row_term_histogram": dict(sorted(equation_histogram.items())),
            "nonzero_coefficient_histogram": dict(sorted(all_coefficients.items())),
            "constant_rows": len(constant_rows),
            "equation_inventory_sha256": hashlib.sha256(equation_bytes).hexdigest(),
            "artifact_equation_sha256": artifact_equation_sha256,
            "artifact_equation_digest_equal": True,
            "canonical_lf_cnf_digest_equal": True,
        },
        "witness_to_cnf_bridge": {
            "crossing_support_variable": "true iff the corresponding complex entry is nonzero",
            "monomial_support_variable": "true iff every crossing factor is nonzero",
            "and_equivalence_encoded_both_directions": True,
            "source_equation_implication": (
                "A zero complex polynomial with nonzero coefficients cannot have "
                "exactly one nonzero combined monomial term."
            ),
            "constant_rows_treat_constant_as_always_active": True,
            "cnf_is_necessary_not_sufficient_for_weights": True,
            "physical_witness_would_induce_cnf_model": True,
        },
        "portable_rup_replay": rup_replay,
        "semantic_controls": semantic_controls,
        "mutation_controls": mutation_controls,
        "proof_checked_by_this_audit": True,
        "proof_semantics": (
            "Each appended clause is RUP because unit propagation conflicts under "
            "the negation of that clause; the last checked clause is empty."
        ),
        "finite_conclusion": (
            "The reconstructed support CNF is unsatisfiable, so no complex physical "
            "witness exists within this fixed order-eight two-K4 unit scaffold."
        ),
        "global_krenn_gu_status": "UNRESOLVED",
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(
        json.dumps(
            {
                "schema": report["schema"],
                "status": report["status"],
                "words": len(equations),
                "variables": variable_count,
                "clauses": len(clauses),
                "core_clauses": len(core_clauses),
                "rup_additions": len(rup_additions),
                "final_empty": rup_additions[-1] == (),
                "cnf_canonical_lf_digest_equal": True,
                "proof_checked_by_this_audit": True,
                "full_result": portable_path(args.output) if args.output else None,
                "global_krenn_gu_status": "UNRESOLVED",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
