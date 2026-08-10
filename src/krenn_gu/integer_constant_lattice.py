"""Exact integer-lattice transport with arbitrary rational constants."""

from __future__ import annotations
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)


from fractions import Fraction
from typing import Sequence

from krenn_gu.integer_signed_lattice import IntegerSignedLattice


class IntegerConstantLattice:
    """Relations ``x**row_i = constant_i`` over nonzero variables."""

    def __init__(
        self,
        rows: Sequence[Sequence[int]],
        constants: Sequence[Fraction | int],
    ) -> None:
        self.constants = tuple(Fraction(value) for value in constants)
        if any(not value for value in self.constants):
            raise ValueError("relation constant must be nonzero")
        self.integer_lattice = IntegerSignedLattice(
            rows, sign_bits=[0] * len(rows)
        )
        if len(self.constants) != self.integer_lattice.generators:
            raise ValueError("relation constant count changed")
        self.rows = self.integer_lattice.rows
        self.generators = self.integer_lattice.generators
        self.width = self.integer_lattice.width
        self.rank = self.integer_lattice.rank
        self.invariant_factors = (
            self.integer_lattice.invariant_factors
        )
        self.kernel_basis = self.integer_lattice.kernel_basis
        self.inconsistent_kernel_vector = next(
            (
                vector
                for vector in self.kernel_basis
                if self._constant_for_coordinates(vector) != 1
            ),
            None,
        )
        self.has_inconsistent_kernel = (
            self.inconsistent_kernel_vector is not None
        )

    def _constant_for_coordinates(
        self, coordinates: Sequence[int]
    ) -> Fraction:
        value = Fraction(1)
        for constant, coefficient in zip(
            self.constants, coordinates, strict=True
        ):
            value *= constant ** int(coefficient)
        return value

    def coordinates(self, vector: Sequence[int]) -> list[int] | None:
        return self.integer_lattice.coordinates(vector)

    def transported_constant(
        self, vector: Sequence[int]
    ) -> Fraction | None:
        coordinates = self.coordinates(vector)
        if coordinates is None:
            return None
        if self.has_inconsistent_kernel:
            raise ValueError(
                "transported constant is ambiguous because the relation "
                "system already has an inconsistent kernel dependency"
            )
        return self._constant_for_coordinates(coordinates)
