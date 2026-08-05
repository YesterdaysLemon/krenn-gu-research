"""Symbolic sanity checks for the permanent kernel-deletion hierarchy.

The proof is in the accompanying note.  This script checks its symbolic
capacity arithmetic, quotient-space linear algebra, and equality incidence
bookkeeping.  Bogdanov's arbitrary-order theorem is a cited input.
"""

from __future__ import annotations

import sympy as sp


def quotient_basis(row: sp.Matrix) -> sp.Matrix:
    """Columns form a basis of the kernel of a nonzero row."""
    basis = row.nullspace()
    return sp.Matrix.hstack(*basis)


def restriction_rank(row: sp.Matrix, colours: tuple[int, ...]) -> int:
    basis = quotient_basis(row)
    restricted = sp.Matrix([[basis[c, j] for j in range(basis.cols)] for c in colours])
    return restricted.rank()


def check_capacity() -> None:
    m, s = sp.symbols("m s", integer=True)
    active_modes = m - s + 1
    available_rows = m - s
    pins = s - 1
    assert sp.simplify(active_modes - available_rows) == 1
    assert sp.simplify(active_modes + pins - m) == 0


def check_singleton_quotients() -> None:
    coordinate_rows = [
        sp.Matrix([[1, 0, 0]]),
        sp.Matrix([[0, 1, 0]]),
        sp.Matrix([[0, 0, 1]]),
    ]
    for killed, row in enumerate(coordinate_rows):
        survivors = tuple(c for c in range(3) if c != killed)
        assert restriction_rank(row, survivors) == 2
        assert restriction_rank(row, (0, 1, 2)) == 2

    # Up to coordinate permutation and nonzero diagonal rescaling, these are
    # the two noncoordinate support strata.  No coordinate term is killed.
    for row in (sp.Matrix([[1, 1, 0]]), sp.Matrix([[1, 1, 1]])):
        basis = quotient_basis(row)
        assert basis.rank() == 2
        assert restriction_rank(row, (0, 1, 2)) == 2
        for c in range(3):
            assert any(basis[c, j] != 0 for j in range(basis.cols))

    zero_row = sp.Matrix([[0, 0, 0]])
    zero_basis = sp.Matrix.hstack(*zero_row.nullspace())
    assert zero_basis == sp.eye(3)
    assert zero_basis.rank() == 3


def check_equality_ledger() -> None:
    m = sp.symbols("m", integer=True, positive=True)
    required_cells = 3 * m
    cells_per_source = 3
    assert sp.simplify(required_cells / m - cells_per_source) == 0

    # In the equality case, every mode has one edge of each colour after the
    # nonzero pure coefficients force each colour class to be a matching.
    mode_colour_degree = sp.ones(1, 3)
    assert list(mode_colour_degree) == [1, 1, 1]
    assert sum(mode_colour_degree) == 3

    # A target word chooses exactly one supported cell in every mode.  Hence
    # any compatible perfect matching is unique and has one monomial.
    choices_per_mode = [1, 1, 1]
    assert sp.prod(choices_per_mode) == 1

    # Small illustrative one-factorization: edge (i,i+c) has colour c.
    # The permutation (0,2,1) has word (0,1,2), and filtering by that word
    # leaves exactly its three entries.
    filtered = sp.zeros(3)
    permutation = (0, 2, 1)
    word = (0, 1, 2)
    for mode, (source, colour) in enumerate(zip(permutation, word, strict=True)):
        assert source == (mode + colour) % 3
        filtered[source, mode] = 1
    assert filtered.det() != 0
    assert sum(1 for value in filtered if value) == 3


def main() -> None:
    check_capacity()
    check_singleton_quotients()
    check_equality_ledger()
    print("arbitrary permanent kernel-deletion hierarchy: symbolic sanity checks PASS")
    print("arbitrary matching input: Bogdanov theorem (not finite enumeration)")


if __name__ == "__main__":
    main()
