"""Deterministic GHZ-to-subcoefficient facts and solver-free circuit replay.

All zero/nonzero facts are derived from physical support and full GHZ supports.
No freely chosen Boolean proper-coefficient value is admitted as a premise.
"""

from __future__ import annotations

import itertools
from collections import Counter

from krenn_gu.full_tensor_cancellation import perfect_matchings
from krenn_gu.recursive_hafnian_binomials import RecursiveBinomial
from krenn_gu.recursive_tensor_binomials import sparse_integer_circuit


class SourceCoefficientPeeling:
    def __init__(self, instance):
        if instance.clause_counts["target"] != 3 ** instance.n:
            raise ValueError("peeling requires the full GHZ target")
        self.instance = instance
        self.matchings = {}

    def initial_facts(self, support):
        support = tuple(support)
        if (any(type(v) is not int for v in support)
                or len(support) != len(self.instance.entries)
                or set(map(abs, support)) != set(self.instance.entries.values())):
            raise ValueError("one truth value is required for each physical entry")
        facts = {abs(v): int(v > 0) for v in support}
        for (vertices, word), variable in self.instance.coefficients.items():
            if len(vertices) == self.instance.n:
                facts[variable] = int(len(set(word)) == 1)
        return facts

    def expansion(self, state, vertex):
        if vertex not in state[0]:
            raise ValueError("expansion vertex is outside the subset")
        return tuple(self.instance.product_factors(state, tuple(sorted((vertex, other))))
                     for other in state[0] if other != vertex)

    def derive(self, support):
        facts = self.initial_facts(support)
        initial = set(facts)
        constraints = []
        for state, result in self.instance.coefficients.items():
            for vertex in state[0]:
                expansion = self.expansion(state, vertex)
                terms = tuple(cofactor for entry, cofactor in expansion if facts[entry])
                constraints.append((result, terms, state, vertex))
        derivations = {}

        def add(variable, value, state, vertex, result, terms):
            if variable in facts:
                if facts[variable] != value:
                    raise ValueError("support propagation already contradicts GHZ")
                return
            parents = tuple((v, facts[v]) for v in sorted({result, *terms} - {variable}) if v in facts)
            derivations[variable] = {"variable": variable, "value": value,
                                     "vertices": state[0], "word": state[1],
                                     "vertex": vertex, "parents": parents}
            facts[variable] = value

        passes = 0
        while True:
            passes += 1
            before = len(facts)
            for result, terms, state, vertex in constraints:
                live = [v for v in terms if facts.get(v) == 1]
                unknown = [v for v in terms if v not in facts]
                value = facts.get(result)
                if value == 0:
                    if len(live) == 1 and not unknown:
                        raise ValueError("support propagation already contradicts GHZ")
                    if len(unknown) == 1 and len(live) <= 1:
                        add(unknown[0], int(bool(live)), state, vertex, result, terms)
                elif value == 1:
                    if not live and not unknown:
                        raise ValueError("support propagation already contradicts GHZ")
                    if not live and len(unknown) == 1:
                        add(unknown[0], 1, state, vertex, result, terms)
                elif not unknown and len(live) <= 1:
                    add(result, int(bool(live)), state, vertex, result, terms)
            if len(facts) == before:
                break
        return facts, initial, derivations, passes

    def monomials(self, state):
        vertices, word = state
        if vertices not in self.matchings:
            self.matchings[vertices] = tuple(perfect_matchings(vertices))
        colours = dict(zip(vertices, word, strict=True))
        return tuple(tuple(sorted(self.instance.entry(u, v, colours[u], colours[v]) for u, v in matching))
                     for matching in self.matchings[vertices])

    def binomial(self, state, positive):
        live = [term for term in self.monomials(state) if all(v in positive for v in term)]
        if len(live) != 2:
            raise ValueError("derived zero is not a complete two-term matching fibre")
        row = Counter(live[0])
        row.subtract(Counter(live[1]))
        entries = tuple(sorted((v, p) for v, p in row.items() if p))
        if entries and entries[0][1] < 0:
            entries = tuple((v, -p) for v, p in entries)
        return entries

    def replay(self, support, certificate):
        """Finite local truth tables plus integer addition; no propagation/Smith solver."""
        try:
            facts = self.initial_facts(support)
            positive = {v for v in support if v > 0}
            entry_ids = set(self.instance.entries.values())
            guards = set()
            for step in certificate["derivations"]:
                state = tuple(step["vertices"]), tuple(step["word"])
                result = self.instance.coefficients[state]
                variable, value = step["variable"], step["value"]
                if (type(variable) is not int or type(value) is not int
                        or value not in (0, 1) or variable in facts):
                    return False
                expansion = self.expansion(state, step["vertex"])
                terms = []
                for entry, cofactor in expansion:
                    guards.add(entry if entry in positive else -entry)
                    if entry in positive:
                        terms.append(cofactor)
                local = {result, *terms}
                if variable not in local:
                    return False
                parents = dict(step["parents"])
                if len(parents) != len(step["parents"]) or variable in parents or not set(parents) <= local:
                    return False
                for parent, parent_value in parents.items():
                    if (type(parent) is not int or type(parent_value) is not int
                            or parent_value not in (0, 1) or parent not in facts
                            or facts[parent] != parent_value):
                        return False
                    if parent in entry_ids:
                        guards.add(parent if parent_value else -parent)
                free = sorted(local - set(parents))
                allowed_values = set()
                for bits in itertools.product((0, 1), repeat=len(free)):
                    assignment = {**parents, **dict(zip(free, bits, strict=True))}
                    count = sum(assignment[cofactor] for cofactor in terms)
                    allowed = (count >= 1) if assignment[result] else (count != 1)
                    if allowed:
                        allowed_values.add(assignment[variable])
                if allowed_values != {value}:
                    return False
                facts[variable] = value
            total = Counter()
            parity = 0
            for item in certificate["binomials"]:
                state = tuple(item["vertices"]), tuple(item["word"])
                if facts.get(self.instance.coefficients[state]) != 0:
                    return False
                coefficient = item["coefficient"]
                if type(coefficient) is not int or not coefficient:
                    return False
                for variable, power in self.binomial(state, positive):
                    total[variable] += coefficient * power
                parity += coefficient
                for term in self.monomials(state):
                    absent = [v for v in term if v not in positive]
                    if absent:
                        guards.add(-min(absent))
                    else:
                        guards.update(term)
            if any(total.values()) or parity % 2 != 1:
                return False
            cut = tuple(sorted((-v for v in guards), key=lambda v: (abs(v), v)))
            return cut == tuple(certificate["cut"])
        except (KeyError, ValueError, TypeError, IndexError):
            return False

    def find_obstruction(self, support):
        support = tuple(support)
        facts, initial, derivations, passes = self.derive(support)
        positive = {v for v in support if v > 0}
        found = {}
        for state, variable in self.instance.coefficients.items():
            if facts.get(variable) != 0:
                continue
            try:
                row = self.binomial(state, positive)
            except ValueError:
                continue
            found.setdefault(row, state)
        rows = [RecursiveBinomial(row, 1, ()) for row in found]
        vector, diagnostic = sparse_integer_circuit(rows)
        diagnostic.update(facts=len(facts), derived_facts=len(derivations), passes=passes,
                          forced_binomials=len(rows))
        if vector is None:
            return None, diagnostic
        needed = set()

        def visit(variable):
            if variable in initial or variable in needed:
                return
            needed.add(variable)
            for parent, _value in derivations[variable]["parents"]:
                visit(parent)

        binomials = []
        for coefficient, state in zip(vector, found.values(), strict=True):
            if coefficient:
                visit(self.instance.coefficients[state])
                binomials.append({"vertices": state[0], "word": state[1], "coefficient": coefficient})
        selected = [item for v, item in derivations.items() if v in needed]
        guards = set()
        entry_ids = set(self.instance.entries.values())
        for item in selected:
            state = tuple(item["vertices"]), tuple(item["word"])
            for entry, _cofactor in self.expansion(state, item["vertex"]):
                guards.add(entry if entry in positive else -entry)
            for parent, value in item["parents"]:
                if parent in entry_ids:
                    guards.add(parent if value else -parent)
        for item in binomials:
            state = tuple(item["vertices"]), tuple(item["word"])
            for term in self.monomials(state):
                absent = [v for v in term if v not in positive]
                if absent:
                    guards.add(-min(absent))
                else:
                    guards.update(term)
        certificate = {"derivations": selected, "binomials": binomials,
                       "cut": tuple(sorted((-v for v in guards), key=lambda v: (abs(v), v)))}
        if not self.replay(support, certificate):
            raise AssertionError("solver-free peeling certificate failed local truth-table replay")
        return certificate, diagnostic
