"""Exact unit-pivot binomial transport through larger recursive cancellations.

Discovery only eliminates exponent coefficients +1 or -1. Nonunit residual
relations are retained diagnostically, never saturated or replaced by parity.
Certificates replay original Laplace fibres and integer combinations without
running elimination. A surviving quotient assignment is not a weight model.
"""

from __future__ import annotations

from collections import Counter

from krenn_gu.recursive_tensor_binomials import (
    RecursiveTensorBinomials, TensorLaplaceOrigin,
)


def _subtract(row, multiple, other):
    for variable, power in other.items():
        row[variable] = row.get(variable, 0) - multiple * power
        if row[variable] == 0:
            del row[variable]


class UnitSignedQuotient:
    """Sound Laurent substitutions, not a complete general lattice algorithm."""

    def __init__(self, rows, *, max_rows=40000, max_terms=8192, max_bits=2048):
        if len(rows) > max_rows:
            raise ValueError("unit quotient row bound")
        self.rows = rows
        self.max_terms = max_terms
        self.max_bits = max_bits
        self.pivots = {}
        self.residual = []
        self.kernel = None
        todo = [(dict(row.exponents), {i: 1}) for i, row in enumerate(rows)]
        self.passes = 0
        while todo:
            self.passes += 1
            start_rank = len(self.pivots)
            residual = []
            for row, combination in sorted(todo, key=lambda item: len(item[0])):
                self.reduce(row, combination)
                if not row:
                    if self.sign_bit(combination):
                        self.kernel = combination
                        break
                    continue
                unit = [v for v, power in row.items() if abs(power) == 1]
                if unit:
                    pivot = max(unit)
                    if row[pivot] < 0:
                        row = {v: -p for v, p in row.items()}
                        combination = {i: -k for i, k in combination.items()}
                    self.pivots[pivot] = row, combination, len(self.pivots)
                else:
                    residual.append((row, combination))
            self.residual = residual
            if self.kernel is not None or len(self.pivots) == start_rank:
                break
            todo = residual

        self.normal = {}
        for pivot, (row, combination, _index) in reversed(tuple(self.pivots.items())):
            expression = Counter()
            bit = self.sign_bit(combination)
            for variable, power in row.items():
                if variable == pivot:
                    continue
                factors, sign = self.normal.get(variable, ({variable: 1}, 0))
                for factor, exponent in factors.items():
                    expression[factor] -= power * exponent
                bit -= power * sign
            expression = {v: p for v, p in expression.items() if p}
            self.check_size(expression, {})
            self.normal[pivot] = expression, bit % 2

    def sign_bit(self, combination):
        return sum(k * self.rows[i].sign_bit for i, k in combination.items()) % 2

    def check_size(self, row, combination):
        if max(len(row), len(combination)) > self.max_terms or max(
            (abs(value).bit_length() for value in (*row.values(), *combination.values())),
            default=0,
        ) > self.max_bits:
            raise ValueError("unit quotient size bound")

    def reduce(self, row, combination):
        """Subtract recorded unit pivots; carry the SAME integer operations."""
        while True:
            candidates = [v for v in row if v in self.pivots]
            if not candidates:
                return
            pivot = min(candidates, key=lambda v: self.pivots[v][2])
            previous, prior_combination, _index = self.pivots[pivot]
            multiple = row[pivot]
            _subtract(row, multiple, previous)
            _subtract(combination, multiple, prior_combination)
            self.check_size(row, combination)

    def signature(self, term):
        exponents = Counter()
        bit = 0
        for variable, power in term.items():
            factors, sign = self.normal.get(variable, ({variable: 1}, 0))
            for factor, exponent in factors.items():
                exponents[factor] += power * exponent
            bit += power * sign
        return tuple(sorted((v, p) for v, p in exponents.items() if p)), (-1 if bit % 2 else 1)

    def coordinates(self, target):
        row, combination = dict(target), {}
        self.reduce(row, combination)
        if row:
            return None
        return {i: -k for i, k in combination.items()}


def _origin_data(origin):
    return {"vertices": origin.vertices, "word": origin.word,
            "vertex": origin.vertex, "orientation": origin.orientation}


def _read_origin(item):
    vertices, word = tuple(item["vertices"]), tuple(item["word"])
    if any(type(v) is not int for v in (*vertices, *word, item["vertex"])):
        raise ValueError("origin indices must be integers")
    return TensorLaplaceOrigin(vertices, word, item["vertex"], item["orientation"])


class RecursiveTensorQuotient:
    def __init__(self, instance):
        self.instance = instance
        self.binomials = RecursiveTensorBinomials(instance)

    def terms(self, origin, positive):
        state = origin.vertices, origin.word
        if origin.vertex not in origin.vertices:
            raise ValueError("target expansion vertex outside its subset")
        result = self.instance.coefficients[state]
        terms = [(dict(factors), 1) for _edge, factors in
                 self.binomials.expansion(state, origin.vertex, positive)]
        if result in positive:
            terms.append(({result: 1}, -1))
        return terms

    def verify_certificate(self, model, certificate):
        """No unit elimination: reconstruct fibres and add integer exponents."""
        try:
            model = tuple(model)
            if any(type(v) is not int for v in model):
                return False
            assigned, positive = self.binomials.support(model)
            if certificate["kind"] == "binomial_kernel":
                return self.binomials.verify_certificate(model, certificate)
            if certificate["kind"] != "recursive_quotient_singleton":
                return False
            target = _read_origin(certificate["target"])
            if target.orientation != 1:
                return False
            terms = self.terms(target, positive)
            origins = [_read_origin(item) for item in certificate["relations"]]
            rows = [self.binomials.raw_relation(origin, positive) for origin in origins]
            from_terms = set()
            transports = []
            used = set()
            for transport in certificate["transports"]:
                first, second, sign = transport["from"], transport["to"], transport["sign"]
                if any(type(i) is not int for i in (first, second, sign)) or sign not in (-1, 1):
                    return False
                if not (0 <= first < len(terms) and 0 <= second < len(terms)):
                    return False
                if first == second or first in from_terms:
                    return False
                coefficients = transport["coefficients"]
                if len(coefficients) != len(rows) or any(type(k) is not int for k in coefficients):
                    return False
                expected = Counter(terms[first][0])
                expected.subtract(terms[second][0])
                actual = Counter()
                bit = 0
                for i, (row, coefficient) in enumerate(zip(rows, coefficients, strict=True)):
                    if coefficient:
                        used.add(i)
                    for v, power in row.exponents:
                        actual[v] += coefficient * power
                    bit += coefficient * row.sign_bit
                if {v: p for v, p in actual.items() if p} != {v: p for v, p in expected.items() if p}:
                    return False
                if (-1 if bit % 2 else 1) != sign:
                    return False
                from_terms.add(first)
                transports.append((first, second, sign))
            if used != set(range(len(rows))):
                return False
            representatives = set(range(len(terms))) - from_terms
            sums = {i: terms[i][1] for i in representatives}
            for first, second, sign in transports:
                if second not in representatives:
                    return False
                sums[second] += terms[first][1] * sign
            if sum(value != 0 for value in sums.values()) != 1:
                return False
            return tuple(certificate["cut"]) == self.binomials.guard_cut(
                assigned, positive, [target, *origins],
            )
        except (ValueError, KeyError, TypeError, IndexError):
            return False

    def find_obstruction(self, model):
        model = tuple(model)
        assigned, positive = self.binomials.support(model)
        _expanded, raw, substitutions = self.binomials.extract(model)
        origins = set(raw)
        origins.update(origin for origin, _dependencies in substitutions.values())
        origins = sorted(origins, key=lambda o: (o.vertices, o.word, o.vertex, o.orientation))
        rows = [self.binomials.raw_relation(origin, positive) for origin in origins]
        quotient = UnitSignedQuotient(rows)
        diagnostic = {"raw_relations": len(rows), "unit_rank": len(quotient.pivots),
                      "nonunit_residual_rows": len(quotient.residual), "passes": quotient.passes}
        if quotient.kernel is not None:
            selected = [i for i, k in quotient.kernel.items() if k]
            selected_origins = [rows[i].origin for i in selected]
            certificate = {"kind": "binomial_kernel", "equations": [
                {**_origin_data(rows[i].origin), "coefficient": quotient.kernel[i]} for i in selected
            ], "cut": self.binomials.guard_cut(assigned, positive, selected_origins)}
            if not self.verify_certificate(model, certificate):
                raise AssertionError("unit quotient kernel failed original-source replay")
            return certificate, diagnostic

        for state in self.instance.coefficients:
            for vertex in state[0]:
                target = TensorLaplaceOrigin(*state, vertex)
                terms = self.terms(target, positive)
                signatures = [quotient.signature(term) for term, _coefficient in terms]
                groups = Counter()
                for (_term, coefficient), (key, sign) in zip(terms, signatures, strict=True):
                    groups[key] += coefficient * sign
                if sum(value != 0 for value in groups.values()) != 1:
                    continue
                representatives = {}
                transports = []
                used = set()
                for index, (key, sign) in enumerate(signatures):
                    if key not in representatives:
                        representatives[key] = index, sign
                        continue
                    representative, base_sign = representatives[key]
                    difference = Counter(terms[index][0])
                    difference.subtract(terms[representative][0])
                    coordinates = quotient.coordinates({v: p for v, p in difference.items() if p})
                    if coordinates is None:
                        raise AssertionError("unit signature has no integer transport")
                    used.update(coordinates)
                    transports.append({"from": index, "to": representative,
                                       "coordinates": coordinates, "sign": sign * base_sign})
                selected = sorted(used)
                certificate = {"kind": "recursive_quotient_singleton", "target": _origin_data(target),
                               "relations": [_origin_data(rows[i].origin) for i in selected],
                               "transports": [{"from": t["from"], "to": t["to"], "sign": t["sign"],
                                               "coefficients": [t["coordinates"].get(i, 0) for i in selected]}
                                              for t in transports],
                               "cut": self.binomials.guard_cut(
                                   assigned, positive, [target, *(rows[i].origin for i in selected)]),
                               }
                if not self.verify_certificate(model, certificate):
                    raise AssertionError("recursive quotient failed original-source replay")
                return certificate, diagnostic
        diagnostic["status"] = "NO_UNIT_QUOTIENT_OBSTRUCTION_NOT_REALIZATION"
        return None, diagnostic
