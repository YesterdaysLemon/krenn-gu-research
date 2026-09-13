"""Replay linear combinations of source equations after integer transport.

Every source leaf is a complete Laplace identity. Explicit integer combinations
of complete binomial identities transport its monomials to signed Laurent
monomials. The DAG uses only rational linear combinations and division by
guarded nonzero monomials. A nonzero singleton is impossible over C.

This checker runs no binomial elimination, quotient discovery, or polynomial
reduction. Its output is conditional on the reconstructed support guard, not
an exclusion of every cofactor assignment on the same physical support.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction

from krenn_gu.recursive_tensor_quotient import RecursiveTensorQuotient, _read_origin


def replay_recursive_row_space(instance, model, certificate):
    if certificate["schema"] != "recursive-laurent-row-space-v1":
        raise ValueError("unknown row-space certificate")
    if type(certificate["n"]) is not int or certificate["n"] != instance.n:
        raise ValueError("wrong row-space order")
    model = tuple(model)
    if any(type(v) is not int for v in model):
        raise ValueError("model literals must be integers")
    algebra = RecursiveTensorQuotient(instance)
    assigned, positive = algebra.binomials.support(model)
    original_ids = set(instance.entries.values()) | set(instance.coefficients.values())
    relation_origins = [_read_origin(item) for item in certificate["relations"]]
    rows = [algebra.binomials.raw_relation(origin, positive) for origin in relation_origins]
    dag = certificate["dag"]
    if not dag or len(dag) > 10000 or len(rows) > 10000:
        raise ValueError("row-space certificate size bound")
    values, dependencies = {}, {}
    guard_origins = list(relation_origins)
    variables, used_rows = set(), set()

    def monomial(data):
        pairs = tuple(tuple(pair) for pair in data)
        if any(len(pair) != 2 or any(type(v) is not int for v in pair)
               or pair[0] not in original_ids or pair[0] not in positive or not pair[1]
               for pair in pairs):
            raise ValueError("Laurent powers require typed nonzero source variables")
        if pairs != tuple(sorted(pairs)) or len({v for v, power in pairs}) != len(pairs):
            raise ValueError("noncanonical Laurent monomial")
        variables.update(v for v, power in pairs)
        return pairs

    for node in dag:
        index = node["id"]
        if type(index) is not int or index < 0 or index in values:
            raise ValueError("invalid or repeated DAG node")
        poly = Counter()
        parents = []
        if node["kind"] == "source":
            origin = _read_origin(node["origin"])
            if type(origin.orientation) is not int or origin.orientation != 1:
                raise ValueError("source leaf orientation must be one")
            guard_origins.append(origin)
            terms = algebra.terms(origin, positive)
            if len(terms) != len(node["transports"]):
                raise ValueError("a complete source fibre must be transported")
            for (term, coefficient), transport in zip(terms, node["transports"], strict=True):
                target = monomial(transport["monomial"])
                sign = transport["sign"]
                coefficients = transport["coefficients"]
                if type(sign) is not int or sign not in (-1, 1):
                    raise ValueError("invalid transport sign")
                if len(coefficients) != len(rows) or any(type(k) is not int for k in coefficients):
                    raise ValueError("transport needs an integer coefficient per row")
                expected = Counter(term)
                expected.subtract(dict(target))
                actual, bit = Counter(), 0
                for i, (row, k) in enumerate(zip(rows, coefficients, strict=True)):
                    if k:
                        used_rows.add(i)
                    for v, power in row.exponents:
                        actual[v] += k*power
                    bit += k*row.sign_bit
                if {v: p for v, p in actual.items() if p} != {v: p for v, p in expected.items() if p}:
                    raise ValueError("integer exponent transport failed")
                if sign != (-1 if bit % 2 else 1):
                    raise ValueError("integer sign transport failed")
                poly[target] += coefficient*sign
        elif node["kind"] == "divide":
            parent = node["parent"]
            if type(parent) is not int or parent not in values:
                raise ValueError("division parent must precede its child")
            parents.append(parent)
            divisor = dict(monomial(node["monomial"]))
            scalar = node["scalar"]
            if type(scalar) is not int or not scalar:
                raise ValueError("division needs a nonzero integer scalar")
            for powers, coefficient in values[parent].items():
                remainder = Counter(dict(powers))
                remainder.subtract(divisor)
                key = tuple(sorted((v, p) for v, p in remainder.items() if p))
                poly[key] += Fraction(coefficient, scalar)
        elif node["kind"] == "combine":
            for side in ("left", "right"):
                parent, scalar = node[side], node[side+"_scalar"]
                if type(parent) is not int or parent not in values or type(scalar) is not int:
                    raise ValueError("combination needs preceding parents and integer scalars")
                parents.append(parent)
                for powers, coefficient in values[parent].items():
                    poly[powers] += scalar*coefficient
        else:
            raise ValueError("unknown DAG operation")
        values[index] = {m: c for m, c in poly.items() if c}
        if len(values[index]) > 10000:
            raise ValueError("polynomial replay term bound")
        dependencies[index] = parents
    final = certificate["contradiction_node"]
    if type(final) is not int or final not in values or len(values[final]) != 1:
        raise ValueError("final equation is not a nonzero Laurent singleton")
    reachable, todo = set(), [final]
    while todo:
        node = todo.pop()
        if node not in reachable:
            reachable.add(node)
            todo.extend(dependencies[node])
    if reachable != set(values) or used_rows != set(range(len(rows))):
        raise ValueError("unused DAG nodes or binomial relations")
    cut = set(algebra.binomials.guard_cut(assigned, positive, guard_origins))
    cut.update(-v for v in variables)
    cut = tuple(sorted(cut, key=lambda v: (abs(v), v)))
    if any(type(v) is not int for v in certificate["cut"]) or tuple(certificate["cut"]) != cut:
        raise ValueError("row-space cut differs from complete source guards")
    if any(v in assigned for v in cut):
        raise ValueError("source template does not violate its cut")
    return {"status": "EXACT_RECURSIVE_ROW_SPACE_REPLAY_PASS", "cut": cut,
            "relations": len(rows), "dag_nodes": len(dag), "guard_literals": len(cut)}
