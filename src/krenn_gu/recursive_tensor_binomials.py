"""Sparse exact circuit discovery from shared coloured-subset Laplace identities.

One-term identities eliminate nonzero subset coefficients without extracting
roots. Discovery may miss integer dependencies; every returned contradiction is
lifted back to unexpanded source identities and checked by integer arithmetic.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import reduce
from math import gcd


@dataclass(frozen=True)
class TensorLaplaceOrigin:
    vertices: tuple[int, ...]
    word: tuple[int, ...]
    vertex: int
    orientation: int = 1


@dataclass(frozen=True)
class TensorBinomial:
    exponents: tuple[tuple[int, int], ...]
    sign_bit: int
    origin: TensorLaplaceOrigin


def sparse_integer_circuit(rows, *, max_row_terms=2048, max_certificate_terms=4096,
                           max_bits=2048, max_rows=20000):
    """One-sided bounded elimination; None is not an integer consistency proof."""
    if len(rows) > max_rows:
        return None, {"status": "ROW_BOUND", "rows": len(rows)}
    pivots = {}
    order = sorted(range(len(rows)), key=lambda i: (len(rows[i].exponents), i))
    for step, index in enumerate(order):
        row = dict(rows[index].exponents)
        combination = {index: 1}
        while row:
            pivot = min(row)
            if pivot not in pivots:
                if row[pivot] < 0:
                    row = {v: -p for v, p in row.items()}
                    combination = {i: -k for i, k in combination.items()}
                pivots[pivot] = row, combination
                break
            previous, previous_combination = pivots[pivot]
            a, b = row[pivot], previous[pivot]
            divisor = gcd(abs(a), abs(b))
            a //= divisor
            b //= divisor
            new_row = {v: b * p for v, p in row.items()}
            for v, p in previous.items():
                new_row[v] = new_row.get(v, 0) - a * p
            row = {v: p for v, p in new_row.items() if p}
            new_combination = {i: b * k for i, k in combination.items()}
            for i, k in previous_combination.items():
                new_combination[i] = new_combination.get(i, 0) - a * k
            combination = {i: k for i, k in new_combination.items() if k}
            divisor = reduce(gcd, (abs(v) for v in (*row.values(), *combination.values())), 0)
            if divisor > 1:
                row = {v: p // divisor for v, p in row.items()}
                combination = {i: k // divisor for i, k in combination.items()}
            if len(row) > max_row_terms or len(combination) > max_certificate_terms or max(
                (abs(v).bit_length() for v in (*row.values(), *combination.values())), default=0
            ) > max_bits:
                return None, {"status": "SIZE_BOUND", "step": step, "rank": len(pivots)}
        if not row and sum(k * rows[i].sign_bit for i, k in combination.items()) % 2:
            vector = tuple(combination.get(i, 0) for i in range(len(rows)))
            total = Counter()
            for i, coefficient in combination.items():
                for variable, power in rows[i].exponents:
                    total[variable] += coefficient * power
            if any(total.values()):
                raise AssertionError("sparse integer certificate failed replay")
            return vector, {"status": "ODD_INTEGER_CIRCUIT", "step": step, "rank": len(pivots)}
    return None, {"status": "NO_CIRCUIT_FOUND_NOT_SATURATED", "rank": len(pivots)}


class RecursiveTensorBinomials:
    def __init__(self, instance):
        self.instance = instance

    def support(self, model):
        assigned = set(model)
        if 0 in assigned or any(-literal in assigned for literal in assigned):
            raise ValueError("invalid Boolean support assignment")
        required = set(self.instance.entries.values()) | set(self.instance.coefficients.values())
        if not required <= {abs(v) for v in assigned}:
            raise ValueError("incomplete coefficient/entry support assignment")
        return assigned, {v for v in assigned if v > 0}

    def expansion(self, state, vertex, positive):
        live = []
        for other in state[0]:
            if other == vertex:
                continue
            edge = tuple(sorted((vertex, other)))
            first, second = self.instance.product_factors(state, edge)
            if first in positive and second in positive:
                live.append((edge, Counter((first, second))))
        return live

    def raw_relation(self, origin, positive):
        if type(origin.orientation) is not int or origin.orientation not in (-1, 1):
            raise ValueError("invalid relation orientation")
        state = origin.vertices, origin.word
        if origin.vertex not in origin.vertices:
            raise ValueError("expansion vertex is outside its subset")
        result = self.instance.coefficients[state]
        live = self.expansion(state, origin.vertex, positive)
        if result in positive and len(live) == 1:
            row = Counter({result: 1})
            row.subtract(live[0][1])
            sign = 0
        elif result not in positive and len(live) == 2:
            row = live[0][1].copy()
            row.subtract(live[1][1])
            sign = 1
        else:
            raise ValueError("origin is not a complete binomial Laplace fibre")
        return TensorBinomial(tuple(sorted((v, origin.orientation * p) for v, p in row.items() if p)),
                              sign, origin)

    def extract(self, model):
        _assigned, positive = self.support(model)
        expressions = {v: Counter({v: 1}) for v in self.instance.entries.values() if v in positive}
        substitutions = {}
        found = {}
        raw_rows = {}
        for state, result in self.instance.coefficients.items():
            vertices, word = state
            expansions = [(vertex, self.expansion(state, vertex, positive)) for vertex in vertices]
            if any((result in positive and not live) or (result not in positive and len(live) == 1)
                   for _vertex, live in expansions):
                raise ValueError("support violates a Laplace support rule")
            if result in positive:
                unique = next(((v, live[0]) for v, live in expansions if len(live) == 1), None)
                if unique is None:
                    expressions[result] = Counter({result: 1})
                else:
                    vertex, (_edge, factors) = unique
                    expression = Counter()
                    for factor, power in factors.items():
                        for variable, exponent in expressions[factor].items():
                            expression[variable] += power * exponent
                    expressions[result] = expression
                    substitutions[result] = (
                        TensorLaplaceOrigin(vertices, word, vertex),
                        tuple(factor for factor in factors if factor in substitutions),
                    )
            for vertex, live in expansions:
                if not ((result in positive and len(live) == 1)
                        or (result not in positive and len(live) == 2)):
                    continue
                origin = TensorLaplaceOrigin(vertices, word, vertex)
                raw = self.raw_relation(origin, positive)
                expanded = Counter()
                for variable, power in raw.exponents:
                    for entry, exponent in expressions[variable].items():
                        expanded[entry] += power * exponent
                entries = tuple(sorted((v, p) for v, p in expanded.items() if p))
                if entries and entries[0][1] < 0:
                    entries = tuple((v, -p) for v, p in entries)
                    origin = TensorLaplaceOrigin(vertices, word, vertex, -1)
                    raw = self.raw_relation(origin, positive)
                if entries or raw.sign_bit:
                    key = entries, raw.sign_bit
                    if key not in found:
                        found[key] = TensorBinomial(entries, raw.sign_bit, origin)
                        raw_rows[origin] = raw
        return tuple(found.values()), raw_rows, substitutions

    def guard_cut(self, assigned, positive, origins):
        guards = set()
        for origin in origins:
            state = origin.vertices, origin.word
            result = self.instance.coefficients[state]
            guards.add(result if result in positive else -result)
            for other in origin.vertices:
                if other == origin.vertex:
                    continue
                edge = tuple(sorted((origin.vertex, other)))
                product = self.instance.products[(state, edge)]
                factors = self.instance.product_factors(state, edge)
                live = all(v in positive for v in factors)
                literal = product if live else -product
                if literal not in assigned:
                    raise ValueError("missing or untruthful product support guard")
                guards.add(literal)
        return tuple(sorted((-literal for literal in guards), key=lambda v: (abs(v), v)))

    def verify_certificate(self, model, certificate):
        """Check original complete Laplace fibres, integer identity, and all guards."""
        try:
            assigned, positive = self.support(model)
            total = Counter()
            sign = 0
            origins = []
            for item in certificate["equations"]:
                coefficient = item["coefficient"]
                if type(coefficient) is not int or not coefficient:
                    return False
                origin = TensorLaplaceOrigin(tuple(item["vertices"]), tuple(item["word"]),
                                             item["vertex"], item["orientation"])
                row = self.raw_relation(origin, positive)
                for variable, power in row.exponents:
                    total[variable] += coefficient * power
                sign += coefficient * row.sign_bit
                origins.append(origin)
            if any(total.values()) or sign % 2 != 1:
                return False
            return tuple(certificate["cut"]) == self.guard_cut(assigned, positive, origins)
        except (ValueError, KeyError, TypeError, IndexError):
            return False

    def find_obstruction(self, model):
        model = tuple(model)
        rows, raw_rows, substitutions = self.extract(model)
        vector, diagnostic = sparse_integer_circuit(rows)
        diagnostic.update(relations=len(rows), substitutions=len(substitutions))
        if vector is None:
            return None, diagnostic
        combination = Counter()

        def subtract_substitution(variable, coefficient):
            if variable not in substitutions:
                return
            origin, dependencies = substitutions[variable]
            combination[origin] -= coefficient
            for dependency in dependencies:
                subtract_substitution(dependency, coefficient)

        for row, coefficient in zip(rows, vector, strict=True):
            if not coefficient:
                continue
            combination[row.origin] += coefficient
            for variable, power in raw_rows[row.origin].exponents:
                subtract_substitution(variable, coefficient * power)
        combination = {origin: coefficient for origin, coefficient in combination.items() if coefficient}
        assigned, positive = self.support(model)
        certificate = {
            "equations": [{"vertices": origin.vertices, "word": origin.word,
                           "vertex": origin.vertex, "orientation": origin.orientation,
                           "coefficient": coefficient} for origin, coefficient in combination.items()],
            "cut": self.guard_cut(assigned, positive, combination),
        }
        if not self.verify_certificate(model, certificate):
            raise AssertionError("lifted original-source integer circuit failed replay")
        return certificate, diagnostic
