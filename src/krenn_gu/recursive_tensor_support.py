"""Source-coupled recursive coefficient supports for unrestricted pair blocks.

Unlike the all-diagonal RZP model, one subset variable is indexed by its entire
colour word. No factorization across colour classes is assumed. This is only a
necessary condition for a complex GHZ witness, not a realization algorithm.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

from pysat.formula import CNF

Vertices = tuple[int, ...]
Word = tuple[int, ...]
State = tuple[Vertices, Word]
Edge = tuple[int, int]


@dataclass
class RecursiveTensorSupportInstance:
    n: int
    cnf: CNF
    entries: dict[tuple[int, int, int, int], int]
    coefficients: dict[State, int]
    products: dict[tuple[State, Edge], int]
    killers: dict[tuple[int, int, int], int]
    clause_counts: dict[str, int]

    def entry(self, u: int, v: int, a: int, b: int) -> int:
        """Physical entry with colour a at u and b at v, including transpose."""
        if u == v:
            raise ValueError("no self-pair entries")
        return self.entries[(u, v, a, b) if u < v else (v, u, b, a)]

    def coefficient(self, vertices: Vertices, word: Word) -> int | None:
        """Empty coefficient is constant one; two-vertex coefficients alias g."""
        if len(vertices) != len(word) or len(vertices) % 2:
            raise ValueError("an even subset needs one colour per vertex")
        if vertices != tuple(sorted(set(vertices))):
            raise ValueError("vertices must be distinct and increasing")
        if not vertices:
            return None
        if len(vertices) == 2:
            return self.entry(*vertices, *word)
        return self.coefficients[(vertices, word)]

    def product_factors(self, state: State, edge: Edge) -> tuple[int, int]:
        vertices, word = state
        positions = {vertex: position for position, vertex in enumerate(vertices)}
        u, v = edge
        remaining = tuple(vertex for vertex in vertices if vertex not in edge)
        remainder_word = tuple(word[positions[vertex]] for vertex in remaining)
        remainder = self.coefficient(remaining, remainder_word)
        if remainder is None:
            raise ValueError("product variables start at subset size four")
        return self.entry(u, v, word[positions[u]], word[positions[v]]), remainder


def build_recursive_tensor_support_cnf(
    n: int,
    *,
    impose_target: bool = True,
    column_killers: bool = True,
    fix_root_killers: bool = True,
) -> RecursiveTensorSupportInstance:
    """Encode every coloured-subset Laplace support identity, sharing sources.

    The optional killer constraints use the three-colour hyperplane-annihilation
    theorem. For each (v,c), some incident oriented block has only column c
    nonzero. Here c belongs to the OTHER endpoint, not v. Fixing the three
    selected neighbours of vertex zero to 1,2,3 is a vertex relabelling only.
    """
    if n < 4 or n % 2:
        raise ValueError("n must be even and at least four")
    if fix_root_killers and not column_killers:
        raise ValueError("root killer symmetry requires column killers")
    if column_killers and not impose_target:
        raise ValueError("column killers are necessary only under the GHZ target")

    cnf = CNF()
    entries = {}
    coefficients = {}
    products = {}
    killers = {}
    next_id = 0

    def allocate() -> int:
        nonlocal next_id
        next_id += 1
        return next_id

    vertices = tuple(range(n))
    for u, v in itertools.combinations(vertices, 2):
        for a, b in itertools.product(range(3), repeat=2):
            entries[(u, v, a, b)] = allocate()
    for size in range(4, n + 1, 2):
        for subset in itertools.combinations(vertices, size):
            for word in itertools.product(range(3), repeat=size):
                coefficients[(subset, word)] = allocate()

    counts = {key: 0 for key in (
        "product_definitions", "nonzero_accessibility", "singleton_cancellation",
        "target", "killer_definitions", "killer_existence", "symmetry",
    )}
    instance = RecursiveTensorSupportInstance(
        n, cnf, entries, coefficients, products, killers, counts,
    )
    for state, result in coefficients.items():
        subset, _word = state
        incident = {vertex: [] for vertex in subset}
        for edge in itertools.combinations(subset, 2):
            product = allocate()
            products[(state, edge)] = product
            first, second = instance.product_factors(state, edge)
            cnf.extend(([-product, first], [-product, second],
                        [product, -first, -second]))
            counts["product_definitions"] += 3
            for vertex in edge:
                incident[vertex].append(product)
        for terms in incident.values():
            cnf.append([-result, *terms])
            counts["nonzero_accessibility"] += 1
            for index, product in enumerate(terms):
                cnf.append([-product, result, *terms[:index], *terms[index + 1:]])
                counts["singleton_cancellation"] += 1

    if impose_target:
        for word in itertools.product(range(3), repeat=n):
            result = coefficients[(vertices, word)]
            cnf.append([result if len(set(word)) == 1 else -result])
            counts["target"] += 1

    if column_killers:
        for vertex in vertices:
            for colour in range(3):
                choices = []
                for neighbour in vertices:
                    if neighbour == vertex:
                        continue
                    killer = allocate()
                    killers[(vertex, colour, neighbour)] = killer
                    choices.append(killer)
                    inside = [instance.entry(vertex, neighbour, row, colour)
                              for row in range(3)]
                    outside = [instance.entry(vertex, neighbour, row, column)
                               for row in range(3) for column in range(3)
                               if column != colour]
                    # k iff the block has a nonempty column c and zero elsewhere.
                    cnf.append([-killer, *inside])
                    cnf.extend([-killer, -entry] for entry in outside)
                    cnf.extend([killer, -entry, *outside] for entry in inside)
                    counts["killer_definitions"] += 10
                cnf.append(choices)
                counts["killer_existence"] += 1
        if fix_root_killers:
            for colour in range(3):
                cnf.append([killers[(0, colour, colour + 1)]])
                counts["symmetry"] += 1

    if cnf.nv != next_id:
        raise AssertionError("unreferenced allocated variable")
    return instance
