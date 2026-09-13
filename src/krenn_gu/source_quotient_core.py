"""Small RUP cores lifting guarded recursive algebra to physical support cuts.

No solver, Smith form, or unit-pivot elimination is used in replay. The only
premises are regenerated recursive/target clauses, one separately replayed
algebraic clause, and the displayed physical support units. Killers and ratio
clauses are deliberately not admitted as implicit premises.
"""

from __future__ import annotations

from krenn_gu.recursive_tensor_quotient import RecursiveTensorQuotient, _read_origin


def rup_conflict(clauses, assumptions=()):
    """Plain exact unit propagation, used only on small explicit clause cores."""
    assigned = set()
    for literal in assumptions:
        if -literal in assigned:
            return True
        assigned.add(literal)
    while True:
        before = len(assigned)
        for clause in clauses:
            if any(v in assigned for v in clause):
                continue
            remaining = [v for v in set(clause) if -v not in assigned]
            if not remaining:
                return True
            if len(remaining) == 1:
                assigned.add(remaining[0])
        if len(assigned) == before:
            return False


def _canonical(clause):
    return tuple(sorted(set(clause)))


def replay_source_quotient_core(instance, packet):
    """Replay against a freshly regenerated base instance supplied by the caller."""
    if packet["schema"] != "recursive-source-quotient-core-v1" or type(packet["n"]) is not int:
        raise ValueError("wrong source-core schema or order")
    if instance.n != packet["n"] or instance.clause_counts["target"] != 3 ** instance.n:
        raise ValueError("core requires the stated full target")
    if any(instance.clause_counts[key] for key in ("killer_definitions", "killer_existence", "symmetry")):
        raise ValueError("core replay requires the unaugmented recursive target instance")
    if sum(instance.clause_counts.values()) != len(instance.cnf.clauses):
        raise ValueError("augmented clauses are not admitted as base premises")
    entry_ids = set(instance.entries.values())
    coefficient_ids = set(instance.coefficients.values())
    support = packet["entry_support"]
    if (len(support) != len(entry_ids) or any(type(v) is not int for v in support)
            or set(map(abs, support)) != entry_ids):
        raise ValueError("one typed truth value is required per physical entry")
    entry_values = {abs(v): v > 0 for v in support}
    # This is a template for a conditional algebraic clause, not a witness or a
    # model of the whole recursive CNF. Unused coefficient values are arbitrary.
    values = {v: False for v in coefficient_ids}
    values.update(entry_values)
    seen = set()
    for variable, bit in packet["coefficient_support"]:
        if (type(variable) is not int or variable not in coefficient_ids or variable in seen
                or type(bit) is not int or bit not in (0, 1)):
            raise ValueError("invalid coefficient template")
        seen.add(variable)
        values[variable] = bool(bit)
    algebra = packet["quotient_certificate"]
    if algebra["kind"] != "recursive_quotient_singleton":
        raise ValueError("core format requires a recursive quotient certificate")
    origins = [_read_origin(algebra["target"]), *(_read_origin(item) for item in algebra["relations"])]
    for origin in origins:
        state = origin.vertices, origin.word
        for other in origin.vertices:
            if other == origin.vertex:
                continue
            edge = tuple(sorted((origin.vertex, other)))
            first, second = instance.product_factors(state, edge)
            values[instance.products[(state, edge)]] = values[first] and values[second]
    template = [v if bit else -v for v, bit in values.items()]
    if not RecursiveTensorQuotient(instance).verify_certificate(template, algebra):
        raise ValueError("original-source algebraic clause failed replay")

    core = [tuple(clause) for clause in packet["core_clauses"]]
    proof = [tuple(clause) for clause in packet["rup_additions"]]
    if len(core) > 10000 or len(proof) > 10000:
        raise ValueError("small-core format bound exceeded")
    for clause in (*core, *proof):
        if any(type(v) is not int or v == 0 or abs(v) > instance.cnf.nv for v in clause):
            raise ValueError("invalid core literal")
    source_cut = _canonical(algebra["cut"])
    guards, remaining = set(), set()
    algebra_uses = 0
    for clause in core:
        if len(clause) == 1 and abs(clause[0]) in entry_ids:
            literal = clause[0]
            if (literal > 0) != entry_values[abs(literal)]:
                raise ValueError("physical premise differs from source template")
            guards.add(literal)
        elif _canonical(clause) == source_cut:
            algebra_uses += 1
        else:
            remaining.add(_canonical(clause))
    base_clauses = len(remaining)
    for clause in instance.cnf.clauses:
        remaining.discard(_canonical(clause))
    if remaining or algebra_uses != 1:
        raise ValueError("core contains an unproved premise or omits its algebraic cut")
    if not proof or proof[-1] != ():
        raise ValueError("RUP sequence must finish at the empty clause")
    working = list(core)
    for clause in proof:
        if not rup_conflict(working, [-v for v in clause]):
            raise ValueError("RUP addition failed plain unit propagation")
        working.append(clause)
    cut = tuple(sorted((-v for v in guards), key=lambda v: (abs(v), v)))
    if any(type(v) is not int for v in packet["physical_cut"]) or cut != tuple(packet["physical_cut"]):
        raise ValueError("physical cut differs from the checked premises")
    return {"status": "EXACT_SOURCE_CORE_REPLAY_PASS", "physical_cut": cut,
            "physical_guard_count": len(cut), "core_clauses": len(core),
            "base_recursive_clauses": base_clauses, "rup_additions": len(proof),
            "killers_or_ratio_clauses": False}
