"""Truthful zero-pattern encoding of the recursive hafnian identities.

For a colour ``c`` and even vertex set ``A``, let ``s[c, A]`` mean that
``haf(Z^c[A])`` is nonzero.  For an edge ``e={u,v}`` in ``A``, the product
support variable ``b[c, A, e]`` is defined truthfully by

    b[c, A, e] <-> (Z^c_e != 0 and haf(Z^c[A-e]) != 0).

The Laplace expansion at a vertex has only two support-level obstructions:
a nonzero result cannot have zero nonzero summands, and a zero result cannot
have exactly one nonzero summand.  The clauses below encode both statements
for every expansion while sharing the same subset-hafnian variables.

This is a necessary relaxation of actual complex weights.  It is stronger
than AP' but is not sufficient for a weighted realization.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

from pysat.formula import CNF, IDPool

Edge = tuple[int, int]
VertexSet = frozenset[int]


@dataclass(frozen=True)
class RecursiveHafnianSupportInstance:
    """One generated CNF and the variable maps needed to inspect it."""

    n: int
    cnf: CNF
    pool: IDPool
    edge_variables: dict[tuple[int, Edge], int]
    hafnian_variables: dict[tuple[int, VertexSet], int]
    product_variables: dict[tuple[int, VertexSet, Edge], int]
    rainbow_clauses: int
    product_definition_clauses: int
    nonzero_accessibility_clauses: int
    singleton_cancellation_clauses: int
    symmetry_clauses: int

    def hafnian_literal(self, colour: int, vertices: VertexSet) -> int | None:
        """Return the nonzero-hafnian literal; ``None`` means constant true."""

        if len(vertices) % 2:
            raise ValueError("hafnian support is defined only on even sets")
        if not vertices:
            return None
        if len(vertices) == 2:
            edge = tuple(sorted(vertices))
            return self.edge_variables[(colour, edge)]
        return self.hafnian_variables[(colour, vertices)]


def even_ordered_partitions(vertices: tuple[int, ...]):
    """Yield all ordered three-part partitions with even class sizes."""

    for word in itertools.product(range(3), repeat=len(vertices)):
        classes = tuple(
            frozenset(
                vertex
                for vertex, assigned_colour in zip(vertices, word, strict=True)
                if assigned_colour == colour
            )
            for colour in range(3)
        )
        if all(len(part) % 2 == 0 for part in classes):
            yield classes


def canonical_matching_pair(
    n: int,
    cycle_type: tuple[int, ...],
) -> tuple[tuple[Edge, ...], tuple[Edge, ...]]:
    """Return canonical matchings whose alternating cycles have ``cycle_type``.

    Parts are half-lengths: ``1`` is a shared edge, while ``k >= 2`` is one
    alternating cycle of length ``2*k`` in the union of the two matchings.
    """

    if n < 4 or n % 2:
        raise ValueError("n must be even and at least four")
    if not cycle_type or any(part < 1 for part in cycle_type):
        raise ValueError("cycle type must have positive parts")
    if sum(cycle_type) != n // 2:
        raise ValueError("cycle type must partition n/2")

    first = tuple((vertex, vertex + 1) for vertex in range(0, n, 2))
    second: list[Edge] = []
    atom_offset = 0
    for part in cycle_type:
        atoms = tuple(range(atom_offset, atom_offset + part))
        if part == 1:
            atom = atoms[0]
            second.append((2 * atom, 2 * atom + 1))
        else:
            for position, atom in enumerate(atoms):
                next_atom = atoms[(position + 1) % part]
                second.append(
                    tuple(sorted((2 * atom + 1, 2 * next_atom)))
                )
        atom_offset += part
    return first, tuple(sorted(second))


def build_recursive_hafnian_support_cnf(
    n: int,
    *,
    two_part_only: bool = False,
    no_singleton_cancellation: bool = False,
    matching_cycle_type: tuple[int, ...] | None = None,
    third_matching_cycle_type: tuple[int, ...] | None = None,
) -> RecursiveHafnianSupportInstance:
    """Build the recursive zero-pattern relaxation at even order ``n``.

    ``two_part_only`` and ``no_singleton_cancellation`` are sharpness controls,
    not alternate theorem statements.
    """

    if n < 4 or n % 2:
        raise ValueError("n must be even and at least four")

    pool = IDPool()
    cnf = CNF()
    vertices = tuple(range(n))
    pairs = tuple(itertools.combinations(vertices, 2))
    even_sets = tuple(
        frozenset(subset)
        for size in range(4, n + 1, 2)
        for subset in itertools.combinations(vertices, size)
    )

    edge_variables = {
        (colour, edge): pool.id(("g", colour, edge))
        for colour in range(3)
        for edge in pairs
    }
    hafnian_variables = {
        (colour, subset): pool.id(("s", colour, subset))
        for colour in range(3)
        for subset in even_sets
    }
    product_variables = {
        (colour, subset, edge): pool.id(("b", colour, subset, edge))
        for colour in range(3)
        for subset in even_sets
        for edge in itertools.combinations(sorted(subset), 2)
    }

    def h_lit(colour: int, subset: VertexSet) -> int | None:
        if not subset:
            return None
        if len(subset) == 2:
            return edge_variables[(colour, tuple(sorted(subset)))]
        return hafnian_variables[(colour, subset)]

    product_definition_clauses = 0
    nonzero_accessibility_clauses = 0
    singleton_cancellation_clauses = 0
    for colour in range(3):
        for subset in even_sets:
            result = hafnian_variables[(colour, subset)]
            incident: dict[int, list[int]] = {
                vertex: [] for vertex in subset
            }
            for edge in itertools.combinations(sorted(subset), 2):
                product = product_variables[(colour, subset, edge)]
                edge_lit = edge_variables[(colour, edge)]
                remainder_lit = h_lit(colour, subset - set(edge))
                if remainder_lit is None:
                    raise AssertionError("sets of size two have no b variable")

                # b <-> (g_e and s_(A-e)).
                cnf.append([-product, edge_lit])
                cnf.append([-product, remainder_lit])
                cnf.append([product, -edge_lit, -remainder_lit])
                product_definition_clauses += 3
                incident[edge[0]].append(product)
                incident[edge[1]].append(product)

            for vertex in sorted(subset):
                terms = incident[vertex]
                # A nonzero sum has at least one nonzero term.
                cnf.append([-result, *terms])
                nonzero_accessibility_clauses += 1
                if no_singleton_cancellation:
                    continue
                # If the result is zero, its nonzero-term count is not one.
                for position, product in enumerate(terms):
                    others = terms[:position] + terms[position + 1 :]
                    cnf.append([-product, result, *others])
                    singleton_cancellation_clauses += 1

    whole = frozenset(vertices)
    for colour in range(3):
        cnf.append([hafnian_variables[(colour, whole)]])

    symmetry_clauses = 0
    if third_matching_cycle_type is not None:
        if matching_cycle_type != (1,) * (n // 2):
            raise ValueError(
                "third matching cycle type is exhaustive only when the "
                "first two fixed matchings coincide"
            )
    if matching_cycle_type is not None:
        first, second = canonical_matching_pair(n, matching_cycle_type)
        for edge in first:
            cnf.append([edge_variables[(0, edge)]])
            symmetry_clauses += 1
        for edge in second:
            cnf.append([edge_variables[(1, edge)]])
            symmetry_clauses += 1
    if third_matching_cycle_type is not None:
        _first, third = canonical_matching_pair(
            n,
            third_matching_cycle_type,
        )
        for edge in third:
            cnf.append([edge_variables[(2, edge)]])
            symmetry_clauses += 1

    rainbow_clauses = 0
    for classes in even_ordered_partitions(vertices):
        nonempty = sum(bool(part) for part in classes)
        if nonempty < 2 or (two_part_only and nonempty == 3):
            continue
        clause = []
        for colour, part in enumerate(classes):
            literal = h_lit(colour, part)
            if literal is not None:
                clause.append(-literal)
        cnf.append(clause)
        rainbow_clauses += 1

    return RecursiveHafnianSupportInstance(
        n=n,
        cnf=cnf,
        pool=pool,
        edge_variables=edge_variables,
        hafnian_variables=hafnian_variables,
        product_variables=product_variables,
        rainbow_clauses=rainbow_clauses,
        product_definition_clauses=product_definition_clauses,
        nonzero_accessibility_clauses=nonzero_accessibility_clauses,
        singleton_cancellation_clauses=singleton_cancellation_clauses,
        symmetry_clauses=symmetry_clauses,
    )
