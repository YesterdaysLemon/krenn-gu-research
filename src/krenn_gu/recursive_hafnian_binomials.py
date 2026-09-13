"""Extract exact binomials from complete live Laplace fibres.

A Boolean support is not a weight realization. These relations hold for
every realization of that support; an odd integer kernel certificate
excludes it. Passing the test leaves all larger cancellation sums open.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from krenn_gu.recursive_hafnian_support import RecursiveHafnianSupportInstance


@dataclass(frozen=True)
class LaplaceBinomialOrigin:
    colour: int
    subset: tuple[int, ...]
    vertex: int
    nonzero_edges: tuple[tuple[int, int], ...]
    result_nonzero: bool


@dataclass(frozen=True)
class RecursiveBinomial:
    # Numeric variables use the existing edge/hafnian indicator IDs as names;
    # no product-indicator b is treated as an independent numerical variable.
    exponents: tuple[tuple[int, int], ...]
    sign_bit: int
    origins: tuple[LaplaceBinomialOrigin, ...]


def extract_recursive_binomials(instance: RecursiveHafnianSupportInstance, model):
    """Extract zero/two-term and nonzero/one-term equations from a support.

    Product supports are recomputed from g and s, not trusted b indicators.
    Only local recurrence consistency is checked here. H1/H2 and other
    conditions must be checked separately before calling a support global.
    """

    model = tuple(model)
    model_set = set(model)
    assigned = {abs(literal) for literal in model}
    positive = {literal for literal in model if literal > 0}
    if any(-literal in model_set for literal in positive):
        raise ValueError("contradictory Boolean assignment")
    required = set(instance.edge_variables.values()) | set(instance.hafnian_variables.values())
    if not required <= assigned:
        raise ValueError("incomplete edge/hafnian support assignment")
    found: dict[tuple, list[LaplaceBinomialOrigin]] = {}
    for (colour, subset), result in instance.hafnian_variables.items():
        result_nonzero = result in positive
        for vertex in sorted(subset):
            live = []
            monomials = []
            for other in sorted(subset - {vertex}):
                edge = tuple(sorted((vertex, other)))
                edge_id = instance.edge_variables[(colour, edge)]
                remainder = instance.hafnian_literal(colour, subset - set(edge))
                if edge_id in positive and (remainder is None or remainder in positive):
                    live.append(edge)
                    term = Counter({edge_id: 1})
                    if remainder is not None:
                        term[remainder] += 1
                    monomials.append(term)
            if (result_nonzero and not live) or (not result_nonzero and len(live) == 1):
                raise ValueError("support violates a local Laplace rule")
            if result_nonzero and len(live) == 1:
                row = Counter({result: 1})
                row.subtract(monomials[0])
                sign = 0
            elif not result_nonzero and len(live) == 2:
                row = monomials[0].copy()
                row.subtract(monomials[1])
                sign = 1
            else:
                continue
            entries = tuple(sorted((variable, power) for variable, power in row.items() if power))
            if entries and entries[0][1] < 0:
                entries = tuple((variable, -power) for variable, power in entries)
            if not entries and sign == 0:
                continue
            origin = LaplaceBinomialOrigin(colour, tuple(sorted(subset)), vertex,
                                           tuple(live), result_nonzero)
            found.setdefault((entries, sign), []).append(origin)
    return tuple(RecursiveBinomial(entries, sign, tuple(origins))
                 for (entries, sign), origins in sorted(found.items()))


def verify_integer_circuit(relations, coefficients) -> bool:
    """Replay an integer dependency without trusting a Smith decomposition."""

    if len(coefficients) != len(relations) or any(type(k) is not int for k in coefficients):
        return False
    total = Counter()
    sign = 0
    for relation, coefficient in zip(relations, coefficients, strict=True):
        sign += coefficient * relation.sign_bit
        for variable, power in relation.exponents:
            total[variable] += coefficient * power
    return not any(total.values()) and sign % 2 == 1


def find_integer_circuit(relations, *, max_relations=256, max_variables=256):
    """Return a replayed odd integer kernel vector, or None.

    Explicit small bounds prevent a dense Smith calculation on a large
    solver model. Larger supports need bounded component/circuit extraction.
    None means only that these binomials are consistent over the complex
    torus, not that their originating hafnian equations are all satisfiable.
    """

    if not relations:
        return None
    variables = sorted({variable for relation in relations for variable, _ in relation.exponents})
    if len(relations) > max_relations or len(variables) > max_variables:
        raise ValueError("binomial component exceeds the explicit Smith-form bounds")
    for index, relation in enumerate(relations):
        if not relation.exponents and relation.sign_bit:
            vector = tuple(int(i == index) for i in range(len(relations)))
            assert verify_integer_circuit(relations, vector)
            return vector
    if not variables:
        return None
    from krenn_gu.integer_signed_lattice import IntegerSignedLattice

    rows = []
    for relation in relations:
        row = dict(relation.exponents)
        rows.append([row.get(variable, 0) for variable in variables])
    lattice = IntegerSignedLattice(rows, sign_bits=[r.sign_bit for r in relations])
    for vector in lattice.kernel_basis:
        if verify_integer_circuit(relations, vector):
            return vector
    return None


def circuit_support_cut(instance, model, relations, coefficients):
    """Return a guarded no-good clause for a replayed integer circuit.

    One complete Laplace fibre per used relation is sufficient. The guard
    fixes its result support and every incident product support, including
    zero terms. Activating a new cancellation term therefore escapes the
    cut. This is not an unconditional ban on the two displayed monomials.
    """

    model = tuple(model)
    if not verify_integer_circuit(relations, coefficients):
        raise ValueError("invalid integer circuit")
    model_set = set(model)
    positive = {literal for literal in model_set if literal > 0}
    rederived = {(relation.exponents, relation.sign_bit): set(relation.origins)
                 for relation in extract_recursive_binomials(instance, model)}
    guards = set()
    for relation, coefficient in zip(relations, coefficients, strict=True):
        if not coefficient:
            continue
        if not relation.origins:
            raise ValueError("circuit relation lacks a complete-fibre origin")
        origin = relation.origins[0]
        if origin not in rederived.get((relation.exponents, relation.sign_bit), set()):
            raise ValueError("circuit origin does not reproduce its relation")
        subset = frozenset(origin.subset)
        result = instance.hafnian_variables[(origin.colour, subset)]
        guards.add(result if origin.result_nonzero else -result)
        for other in sorted(subset - {origin.vertex}):
            edge = tuple(sorted((origin.vertex, other)))
            product_id = instance.product_variables[(origin.colour, subset, edge)]
            live = edge in origin.nonzero_edges
            literal = product_id if live else -product_id
            if literal not in model_set or (product_id in positive) != live:
                raise ValueError("candidate lacks the truthful complete-fibre guard")
            guards.add(literal)
    if any(-literal in guards for literal in guards):
        raise ValueError("inconsistent circuit support guards")
    return sorted((-literal for literal in guards), key=lambda literal: (abs(literal), literal))
