#!/usr/bin/env python3
"""Construct the exact moving response data for the GLD80 survivor chart.

This module is a reusable construction layer, not a theorem or an elimination
certificate.  It keeps the GLD75 equal-leaf survivor variables symbolic, solves
the fixed GLD70 nuisance map with its certified rank-44 pivot, and transports
the complete response by adjugate tensor matrices.  The default public route
is an exact arithmetic circuit: substitutions are made before the tensor
transport and mixed quotient are evaluated, so Gaussian validation remains
small while the symbolic construction stays denominator-aware.

The moving literal-Delta quotient is represented by a fixed row chart.  Its
13-by-13 determinant is retained as a named localization factor.  The
45-by-45 quadratic matrix uses the same intrinsic minor descriptors as GLD82,
but this file does not assert that its determinant is nonzero away from a
specialization.  In particular, no survivor-open or global Krenn--Gu claim is
made here.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from itertools import chain, permutations
from pathlib import Path
from typing import Any, Mapping, Sequence

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]

GLD72_PATH = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_gaussian_ghz_survivor_and_determinant_safe_route_refutation.py"
)
GLD74_PATH = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension.py"
)
GLD75_PATH = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_survivor_locus_symmetry_and_local_germ_reduction.py"
)
GLD76_PATH = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_survivor_response_universal_module_reduction.py"
)
S3_PATH = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "verify_four_root_torus_star_survivor_response_s3_representation_reduction.py"
)
GAUSSIAN_QUADRATIC_CERTIFICATE_PATH = (
    ROOT
    / "claims"
    / "arbitrary-order"
    / "four_root_torus_star_survivor_invariant_quadratic_macaulay_certificate.json"
)
GAUSSIAN_QUADRATIC_CERTIFICATE_SHA256 = (
    "4cdaf08a5f5dc40abc845d4dc1e6046ce3b259b2c751dfd3ec2955e5b94e65e0"
)


# These are the 45 intrinsic minors used by the candidate GLD82 construction.
# They are copied here so construction does not depend on the verifier; only
# the optional GLD72 validation reads the byte-pinned package certificate.
MINOR_DESCRIPTORS = (
    (2, 3, 0, 1),
    (2, 3, 0, 2),
    (2, 3, 1, 2),
    (2, 6, 0, 1),
    (2, 6, 0, 2),
    (2, 6, 1, 2),
    (2, 14, 0, 1),
    (2, 14, 0, 2),
    (2, 14, 1, 2),
    (2, 15, 0, 1),
    (2, 15, 0, 2),
    (2, 16, 0, 1),
    (2, 16, 0, 2),
    (2, 16, 1, 2),
    (2, 18, 0, 1),
    (2, 18, 0, 2),
    (2, 18, 1, 2),
    (2, 19, 0, 1),
    (2, 19, 0, 2),
    (2, 19, 1, 2),
    (2, 22, 0, 1),
    (2, 27, 0, 1),
    (2, 27, 0, 2),
    (2, 27, 1, 2),
    (3, 6, 0, 1),
    (3, 6, 0, 2),
    (3, 6, 1, 2),
    (3, 14, 0, 1),
    (3, 14, 0, 2),
    (3, 14, 1, 2),
    (3, 15, 0, 1),
    (3, 15, 0, 2),
    (3, 16, 0, 1),
    (3, 16, 0, 2),
    (3, 16, 1, 2),
    (3, 18, 0, 1),
    (3, 18, 0, 2),
    (3, 18, 1, 2),
    (3, 19, 0, 1),
    (6, 14, 0, 1),
    (6, 14, 0, 2),
    (6, 14, 1, 2),
    (6, 16, 0, 1),
    (6, 16, 1, 2),
    (16, 18, 0, 1),
)
DEGREE_TWO_PAIRS = tuple((left, right) for left in range(9) for right in range(left, 9))
assert len(MINOR_DESCRIPTORS) == len(DEGREE_TWO_PAIRS) == 45


# GLD78's moving mixed quotient chart.  These are positions in the 78-row
# mixed list, not indices in the full 81-row tensor list.
MOVING_MIXED_PIVOT_POSITIONS = (
    0,
    1,
    2,
    3,
    4,
    5,
    7,
    8,
    9,
    11,
    17,
    27,
    53,
)


def _load(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    # ``dataclasses`` consults sys.modules while resolving postponed
    # annotations on Python 3.13.  Register dynamically loaded predecessor
    # modules before executing them, matching ordinary import semantics.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@dataclass(frozen=True)
class RepositoryModules:
    """Loaded committed GLD72--GLD76/S3 implementation modules."""

    gld72: Any
    gld73: Any
    gld74: Any
    gld75: Any
    gld76: Any
    s3: Any
    parent: Any


@lru_cache(maxsize=1)
def load_repository_modules() -> RepositoryModules:
    """Load only committed predecessor modules used by this builder."""

    gld75 = _load(GLD75_PATH, "gld75_moving_builder")
    gld74 = _load(GLD74_PATH, "gld74_moving_builder")
    gld76 = _load(GLD76_PATH, "gld76_moving_builder")
    s3 = _load(S3_PATH, "s3_moving_builder")
    gld72 = gld75.load_gld72()
    gate = gld72.load_gate()
    parent = gate.load_parent()
    gld73 = gld74.load_gld73()
    return RepositoryModules(gld72, gld73, gld74, gld75, gld76, s3, parent)


@dataclass(frozen=True)
class EqualLeafChart:
    """The GLD75 equal-leaf scale-fixed frame chart."""

    shifts: tuple[sp.Symbol, ...]
    centre: sp.Matrix
    leaf: sp.Matrix
    survivor_generators: tuple[sp.Expr, ...]
    scale_equation: sp.Expr
    certificate_sha256: str
    certificate_path: Path

    @property
    def frames(self) -> tuple[sp.Matrix, ...]:
        return (self.centre, self.leaf, self.leaf, self.leaf)

    @property
    def origin(self) -> dict[sp.Symbol, sp.Integer]:
        return {shift: sp.Integer(0) for shift in self.shifts}

    def target(self, parent: Any) -> sp.Matrix:
        return parent_tensor_from_frames(parent, self.centre, self.leaf)

    def specialize(
        self, substitutions: Mapping[sp.Symbol, sp.Expr]
    ) -> tuple[sp.Matrix, sp.Matrix]:
        return (
            self.centre.subs(substitutions),
            self.leaf.subs(substitutions),
        )


def parent_tensor_from_frames(
    parent: Any, centre: sp.Matrix, leaf: sp.Matrix
) -> sp.Matrix:
    """Return the 81-vector (T(F)) in the repository word order."""

    return sp.Matrix(
        [
            sp.expand(
                sum(
                    centre[root, colour]
                    * leaf[first, colour]
                    * leaf[second, colour]
                    * leaf[third, colour]
                    for colour in range(3)
                )
            )
            for root, first, second, third in parent.LOCAL_INDICES
        ]
    )


def build_equal_leaf_chart(
    modules: RepositoryModules | None = None,
) -> EqualLeafChart:
    """Build GLD75's symbolic equal-leaf frames and ten survivor generators."""

    modules = modules or load_repository_modules()
    certificate_path = Path(modules.gld75.CERTIFICATE)
    raw = certificate_path.read_bytes().replace(b"\r\n", b"\n")
    data = json.loads(raw)
    shifts = tuple(sp.symbols("x0:15"))
    generators = tuple(
        modules.gld75.sparse_polynomial(encoded, shifts).as_expr()
        for encoded in data["basis"]
    )
    assert len(generators) == 10

    centre0, leaf0 = modules.gld72.candidate_frames()
    centre = sp.Matrix(
        3,
        3,
        [centre0[index] + shifts[index] for index in range(9)],
    )
    leaf = sp.ones(3, 3)
    for local_index, (row, colour) in enumerate(
        (item for row in (1, 2) for item in ((row, 0), (row, 1), (row, 2)))
    ):
        leaf[row, colour] = leaf0[row, colour] + shifts[9 + local_index]

    return EqualLeafChart(
        shifts=shifts,
        centre=centre,
        leaf=leaf,
        survivor_generators=generators,
        scale_equation=shifts[8],
        certificate_sha256=hashlib.sha256(raw).hexdigest(),
        certificate_path=certificate_path,
    )


@dataclass
class FixedNuisanceInterface:
    """The exact fixed GLD70 map and complete q0 response maps."""

    modules: RepositoryModules
    xi: tuple[Any, ...]
    eta: tuple[Any, ...]
    ports: Any
    columns: tuple[sp.Matrix, ...]
    nuisance: sp.Matrix
    pivot_columns: tuple[int, ...]
    pivot_rows: tuple[int, ...]
    pivot_matrix: sp.Matrix
    pivot_inverse: sp.Matrix
    kernel: sp.Matrix
    left_relations: sp.Matrix
    constant: sp.Matrix
    response_maps: tuple[sp.Matrix, ...]
    mixed_rows: tuple[int, ...]
    raw_descriptors: tuple[Any, ...]
    raw_actions: tuple[sp.Matrix, ...]

    @property
    def constant_indices(self) -> tuple[int, ...]:
        return (0, *range(13, 25))

    def solve_target(self, target: sp.Matrix) -> sp.Matrix:
        """Solve using the certified fixed rank-44 pivot columns."""

        target = sp.Matrix(target)
        assert target.rows == 81
        right = self.pivot_inverse * target[list(self.pivot_rows), :]
        alpha = sp.zeros(79, target.cols)
        for local_column, raw_column in enumerate(self.pivot_columns):
            for target_column in range(target.cols):
                alpha[raw_column, target_column] = sp.expand(
                    right[local_column, target_column]
                )
        return alpha

    def reynolds_average(self, value: sp.Matrix) -> sp.Matrix:
        """Average a raw-coordinate vector/matrix under leaf S3."""

        value = sp.Matrix(value)
        return (
            sum(
                (action * value for action in self.raw_actions),
                sp.zeros(value.rows, value.cols),
            )
            / 6
        )


def build_fixed_nuisance_interface(
    modules: RepositoryModules | None = None,
) -> FixedNuisanceInterface:
    """Reconstruct GLD70's fixed 81-by-79 map and GLD76 responses."""

    modules = modules or load_repository_modules()
    parent = modules.parent
    xi0, eta0, ports = parent.canonical_torus_star(1)
    xi = tuple(xi0)
    eta = tuple(eta0)
    columns = tuple(
        sp.Matrix(column)
        for column in chain.from_iterable(parent.full_q_layer_columns(xi, eta, ports))
    )
    assert len(columns) == 79
    nuisance = sp.Matrix.hstack(*columns)
    assert nuisance.shape == (81, 79)

    pivot_columns = tuple(parent.STAR_PIVOT_COLUMNS)
    pivot_rows = tuple(parent.STAR_PIVOT_ROWS)
    pivot_matrix = nuisance.extract(pivot_rows, pivot_columns)
    assert sp.factor(pivot_matrix.det()) == parent.STAR_MINOR_CONSTANT
    pivot_inverse = pivot_matrix.inv()

    kernel = sp.Matrix.hstack(*nuisance.nullspace())
    left_relations = sp.Matrix.hstack(*nuisance.T.nullspace()).T
    assert kernel.shape == (79, 35)
    assert left_relations.shape == (37, 81)

    constant_indices = (0, *range(13, 25))
    constant = nuisance[:, list(constant_indices)]
    response_maps = tuple(
        modules.gld76.q0_response_maps(
            modules.gld73,
            eta,
            ports,
            parent.LOCAL_INDICES,
        )
    )
    assert len(response_maps) == 4
    assert all(response.shape == (81, 79) for response in response_maps)

    mixed_rows = tuple(
        row for row, word in enumerate(parent.LOCAL_INDICES) if len(set(word)) != 1
    )
    descriptors = modules.s3.raw_descriptors()
    leaf_group = tuple(permutations((1, 2, 3)))
    raw_actions = tuple(
        modules.s3.permutation_matrix(descriptors, (0, *sigma)) for sigma in leaf_group
    )
    return FixedNuisanceInterface(
        modules=modules,
        xi=xi,
        eta=eta,
        ports=ports,
        columns=columns,
        nuisance=nuisance,
        pivot_columns=pivot_columns,
        pivot_rows=pivot_rows,
        pivot_matrix=pivot_matrix,
        pivot_inverse=pivot_inverse,
        kernel=kernel,
        left_relations=left_relations,
        constant=constant,
        response_maps=response_maps,
        mixed_rows=mixed_rows,
        raw_descriptors=descriptors,
        raw_actions=raw_actions,
    )


def fixed_pivot_section(
    interface: FixedNuisanceInterface, target: sp.Matrix
) -> sp.Matrix:
    """Public alias for the fixed rank-44 nuisance pivot solve."""

    return interface.solve_target(target)


@dataclass(frozen=True)
class LocalizationFactor:
    """One named open factor and its structural denominator role."""

    name: str
    role: str
    denominator_exponent: int
    numerator: sp.Expr | None = None
    base_value: sp.Expr | None = None
    circuit: str | None = None
    notes: str = ""


@dataclass
class LocalizationLedger:
    """Structural record of localization factors and denominator powers."""

    factors: list[LocalizationFactor] = field(default_factory=list)

    def add(self, factor: LocalizationFactor) -> None:
        assert factor.name not in {item.name for item in self.factors}
        self.factors.append(factor)

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(item.name for item in self.factors)

    def known_numerator_product(self) -> sp.Expr:
        result = sp.Integer(1)
        for factor in self.factors:
            if factor.numerator is not None:
                result *= factor.numerator
        return sp.factor(result)

    def circuit_defined(self) -> tuple[str, ...]:
        return tuple(
            factor.name
            for factor in self.factors
            if factor.numerator is None and factor.circuit is not None
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "factors": [
                {
                    "name": factor.name,
                    "role": factor.role,
                    "denominator_exponent": factor.denominator_exponent,
                    "numerator": (
                        None
                        if factor.numerator is None
                        else str(sp.factor(factor.numerator))
                    ),
                    "base_value": (
                        None
                        if factor.base_value is None
                        else str(sp.factor(factor.base_value))
                    ),
                    "circuit": factor.circuit,
                    "notes": factor.notes,
                }
                for factor in self.factors
            ],
            "known_numerator_product": str(self.known_numerator_product()),
            "circuit_defined_numerators": list(self.circuit_defined()),
        }


@dataclass(frozen=True)
class AdjugateTensorTransport:
    """Denominator-free tensor transport circuit for (U_F)."""

    frames: tuple[sp.Matrix, ...]
    words: tuple[tuple[int, ...], ...]
    adjugates: tuple[sp.Matrix, ...]
    determinants: tuple[sp.Expr, ...]

    @classmethod
    def from_frames(
        cls,
        frames: tuple[sp.Matrix, ...],
        words: Sequence[tuple[int, ...]],
    ) -> "AdjugateTensorTransport":
        assert len(frames) == 4
        return cls(
            frames=tuple(frames),
            words=tuple(words),
            adjugates=tuple(frame.adjugate() for frame in frames),
            determinants=tuple(sp.factor(frame.det()) for frame in frames),
        )

    @property
    def denominator_product(self) -> sp.Expr:
        return sp.factor(sp.prod(self.determinants))

    def _specialized_adjugates(
        self, substitutions: Mapping[sp.Symbol, sp.Expr] | None
    ) -> tuple[sp.Matrix, ...]:
        if substitutions is None:
            return self.adjugates
        return tuple(
            matrix.subs(substitutions).applyfunc(sp.expand) for matrix in self.adjugates
        )

    def entry(
        self,
        output_word: tuple[int, ...],
        source_word: tuple[int, ...],
        substitutions: Mapping[sp.Symbol, sp.Expr] | None = None,
    ) -> sp.Expr:
        adjugates = self._specialized_adjugates(substitutions)
        return sp.prod(
            adjugates[mode][output_word[mode], source_word[mode]] for mode in range(4)
        )

    def apply(
        self,
        value: sp.Matrix,
        substitutions: Mapping[sp.Symbol, sp.Expr] | None = None,
        expand: bool = False,
    ) -> sp.Matrix:
        r"""Apply (U_{F,\mathrm{num}}) without forming an 81-by-81 matrix."""

        value = sp.Matrix(value)
        assert value.rows == len(self.words)
        adjugates = self._specialized_adjugates(substitutions)
        # At a concrete specialization the tensor numerator is an ordinary
        # exact 81-by-81 matrix.  Materialize it once; the sparse circuit loop
        # below is retained for genuinely symbolic calls.
        if substitutions is not None and all(
            not entry.free_symbols for matrix in adjugates for entry in matrix
        ):
            tensor_matrix = sp.kronecker_product(*adjugates)
            result = tensor_matrix * value
            return result.applyfunc(sp.expand) if expand else result
        output = sp.zeros(len(self.words), value.cols)
        for output_index, output_word in enumerate(self.words):
            for source_index, source_word in enumerate(self.words):
                coefficient = sp.prod(
                    adjugates[mode][output_word[mode], source_word[mode]]
                    for mode in range(4)
                )
                if coefficient == 0:
                    continue
                for column in range(value.cols):
                    output[output_index, column] += (
                        coefficient * value[source_index, column]
                    )
        if expand:
            return output.applyfunc(sp.expand)
        return output

    def matrix(
        self,
        substitutions: Mapping[sp.Symbol, sp.Expr] | None = None,
        expand: bool = False,
    ) -> sp.Matrix:
        """Materialize the 81-by-81 numerator matrix on demand."""

        return self.apply(
            sp.eye(len(self.words)),
            substitutions=substitutions,
            expand=expand,
        )


def adjugate_tensor_transport(
    frames: tuple[sp.Matrix, ...],
    words: Sequence[tuple[int, ...]],
) -> AdjugateTensorTransport:
    """Public constructor for the denominator-free (U_{F,\rm num}) circuit."""

    return AdjugateTensorTransport.from_frames(frames, words)


@dataclass(frozen=True)
class AdjugateRawIntertwiner:
    """Block circuit for the moving raw coordinate change (S_F).

    The numerator blocks are adjugates.  Residual blocks carry one inverse
    frame determinant and pair blocks carry one determinant for each endpoint;
    those exponents are exposed rather than hidden in symbolic inverses.
    """

    frames: tuple[sp.Matrix, ...]
    descriptors: tuple[Any, ...]
    adjugates: tuple[sp.Matrix, ...]
    determinants: tuple[sp.Expr, ...]

    @classmethod
    def from_frames(
        cls,
        frames: tuple[sp.Matrix, ...],
        descriptors: Sequence[Any],
        adjugates: Sequence[sp.Matrix] | None = None,
        determinants: Sequence[sp.Expr] | None = None,
    ) -> "AdjugateRawIntertwiner":
        # Reuse the tensor transport's exact adjugates/determinants when the
        # caller has already built them.  This keeps the public circuit lazy
        # and avoids a second symbolic 3-by-3 adjugate pass.
        if adjugates is None:
            adjugates = tuple(frame.adjugate() for frame in frames)
        if determinants is None:
            determinants = tuple(sp.factor(frame.det()) for frame in frames)
        return cls(
            frames=tuple(frames),
            descriptors=tuple(descriptors),
            adjugates=tuple(adjugates),
            determinants=tuple(determinants),
        )

    def numerator_entry(
        self,
        output_index: int,
        source_index: int,
        substitutions: Mapping[sp.Symbol, sp.Expr] | None = None,
    ) -> sp.Expr:
        output = self.descriptors[output_index]
        source = self.descriptors[source_index]
        if output[0] != source[0]:
            return sp.Integer(0)
        adjugates = self.adjugates
        if substitutions is not None:
            adjugates = tuple(
                matrix.subs(substitutions).applyfunc(sp.expand) for matrix in adjugates
            )
        if output[0] == "q":
            return sp.Integer(1)
        if output[0] == "residual":
            if output[1:3] != source[1:3]:
                return sp.Integer(0)
            return adjugates[output[2]][output[3], source[3]]
        if output[0] == "pair":
            if output[1] != source[1]:
                return sp.Integer(0)
            modes = output[1]
            colours = output[2]
            source_colours = source[2]
            return sp.prod(
                adjugates[mode][colour, source_colour]
                for mode, colour, source_colour in zip(
                    modes, colours, source_colours, strict=True
                )
            )
        raise AssertionError(f"unknown raw descriptor {output!r}")

    def denominator_exponents(self, index: int) -> tuple[int, int, int, int]:
        descriptor = self.descriptors[index]
        exponents = [0, 0, 0, 0]
        if descriptor[0] == "residual":
            exponents[descriptor[2]] = 1
        elif descriptor[0] == "pair":
            for mode in descriptor[1]:
                exponents[mode] = 1
        return tuple(exponents)

    def apply(
        self,
        value: sp.Matrix,
        substitutions: Mapping[sp.Symbol, sp.Expr] | None = None,
        denominator_free: bool = True,
        expand: bool = False,
    ) -> sp.Matrix:
        value = sp.Matrix(value)
        size = len(self.descriptors)
        assert value.rows == size
        output = sp.zeros(size, value.cols)
        for target in range(size):
            for source in range(size):
                numerator = self.numerator_entry(target, source, substitutions)
                if numerator == 0:
                    continue
                if not denominator_free:
                    exponents = self.denominator_exponents(source)
                    denominator = sp.prod(
                        self.determinants[mode].subs(substitutions) ** exponents[mode]
                        for mode in range(4)
                        if exponents[mode]
                    )
                    numerator /= denominator
                for column in range(value.cols):
                    output[target, column] += numerator * value[source, column]
        if expand:
            return output.applyfunc(sp.expand)
        return output


def adjugate_raw_intertwiner(
    frames: tuple[sp.Matrix, ...],
    descriptors: Sequence[Any],
    adjugates: Sequence[sp.Matrix] | None = None,
    determinants: Sequence[sp.Expr] | None = None,
) -> AdjugateRawIntertwiner:
    """Public constructor for the structurally denominator-tracked (S_F)."""

    return AdjugateRawIntertwiner.from_frames(
        frames,
        descriptors,
        adjugates=adjugates,
        determinants=determinants,
    )


@dataclass(frozen=True)
class MixedQuotientPivot:
    """A fixed 13-row chart for the moving mixed quotient."""

    mixed_rows: tuple[int, ...]
    pivot_positions: tuple[int, ...]
    quotient_positions: tuple[int, ...]
    canonical_constant: sp.Matrix

    @classmethod
    def moving(cls, interface: FixedNuisanceInterface) -> "MixedQuotientPivot":
        assert len(MOVING_MIXED_PIVOT_POSITIONS) == 13
        quotient_positions = tuple(
            row
            for row in range(len(interface.mixed_rows))
            if row not in set(MOVING_MIXED_PIVOT_POSITIONS)
        )
        return cls(
            mixed_rows=interface.mixed_rows,
            pivot_positions=MOVING_MIXED_PIVOT_POSITIONS,
            quotient_positions=quotient_positions,
            canonical_constant=interface.constant.extract(
                interface.mixed_rows,
                range(interface.constant.cols),
            ),
        )

    @classmethod
    def canonical(cls, interface: FixedNuisanceInterface) -> "MixedQuotientPivot":
        constant = interface.constant.extract(
            interface.mixed_rows,
            range(interface.constant.cols),
        )
        pivots = tuple(constant.T.rref()[1])
        quotient_positions = tuple(
            row for row in range(constant.rows) if row not in set(pivots)
        )
        return cls(
            mixed_rows=interface.mixed_rows,
            pivot_positions=pivots,
            quotient_positions=quotient_positions,
            canonical_constant=constant,
        )

    @property
    def base_canonical_determinant(self) -> sp.Expr:
        return sp.factor(self.canonical_constant[list(self.pivot_positions), :].det())

    def project(
        self,
        constant_mixed: sp.Matrix,
        value_mixed: sp.Matrix,
        denominator_free: bool = False,
    ) -> tuple[sp.Matrix, sp.Expr]:
        """Project 78-row data, optionally clearing the quotient denominator."""

        constant_mixed = sp.Matrix(constant_mixed)
        value_mixed = sp.Matrix(value_mixed)
        pivot = constant_mixed[list(self.pivot_positions), :]
        quotient = constant_mixed[list(self.quotient_positions), :]
        value_pivot = value_mixed[list(self.pivot_positions), :]
        value_quotient = value_mixed[list(self.quotient_positions), :]
        gamma = sp.factor(pivot.det())
        if denominator_free:
            projected = (
                gamma * value_quotient - quotient * pivot.adjugate() * value_pivot
            )
        else:
            projected = value_quotient - quotient * pivot.inv() * value_pivot
        return projected.applyfunc(sp.expand), gamma


def fixed_mixed_quotient_pivot(
    interface: FixedNuisanceInterface, moving: bool = True
) -> MixedQuotientPivot:
    """Return the certified fixed row chart used by the moving quotient."""

    return (
        MixedQuotientPivot.moving(interface)
        if moving
        else MixedQuotientPivot.canonical(interface)
    )


@dataclass
class StaticInvariantData:
    """Leaf-S3 Reynolds data and a Gaussian-calibrated canonical basis."""

    raw_reynolds_kernel: sp.Matrix
    raw_invariant_pivots: tuple[int, ...]
    raw_invariant_basis: sp.Matrix
    invariant_basis: sp.Matrix
    invariant_basis_rows: tuple[int, ...]
    invariant_basis_pivot: sp.Expr
    section_shift: sp.Matrix
    gaussian_section: sp.Matrix
    gaussian_transformed_basis: sp.Matrix
    gaussian_raw_pivots: tuple[int, ...]


def build_static_invariant_data(
    interface: FixedNuisanceInterface,
    chart: EqualLeafChart,
    calibrate_gaussian: bool = True,
) -> StaticInvariantData:
    """Build Reynolds data and calibrate to the GLD74 Gaussian coordinates.

    The calibration is a constant change of basis inside the invariant kernel.
    It makes the optional GLD72 replay compare the same 8 raw coordinates and
    averaged affine section as the existing Gaussian quotient.
    """

    # GLD78/GLD82 select their invariant basis from the unnormalised Reynolds
    # sum.  Keep that exact coordinate convention so the moving specialization
    # matches the byte-pinned Gaussian coefficient matrix entry for entry.
    reynolds_kernel = 6 * interface.reynolds_average(interface.kernel)
    invariant_pivots = tuple(reynolds_kernel.rref()[1])
    assert len(invariant_pivots) == 8
    raw_invariant_basis = reynolds_kernel[:, list(invariant_pivots)]

    target0 = chart.target(interface.modules.parent).subs(chart.origin)
    alpha0 = interface.solve_target(target0)
    direct_section0 = interface.reynolds_average(alpha0)

    gaussian_raw_pivots: tuple[int, ...] = ()
    gaussian_transformed_basis = raw_invariant_basis
    gaussian_section = direct_section0
    invariant_basis = raw_invariant_basis
    section_shift = sp.zeros(79, 1)

    if calibrate_gaussian:
        gld74 = interface.modules.gld74
        gld73, _xi, _eta, _ports, transformed_columns, target = gld74.transformed_map()
        transformed_particular, transformed_kernel, _pivots, _free = gld74.affine_fibre(
            gld73, transformed_columns, target
        )
        transformed_reynolds = 6 * interface.reynolds_average(transformed_kernel)
        gaussian_raw_pivots = tuple(transformed_reynolds.rref()[1])
        assert len(gaussian_raw_pivots) == 8
        gaussian_transformed_basis = transformed_reynolds[:, list(gaussian_raw_pivots)]
        transformed_section = interface.reynolds_average(transformed_particular)

        centre0, leaf0 = interface.modules.gld72.candidate_frames()
        frames0 = (centre0, leaf0, leaf0, leaf0)
        raw_change0 = interface.modules.gld76.raw_intertwiner(frames0)
        raw_change0_inverse = raw_change0.inv()
        invariant_basis = raw_change0_inverse * gaussian_transformed_basis
        gaussian_section = raw_change0_inverse * transformed_section
        section_shift = gaussian_section - direct_section0

        assert all(
            sp.simplify(value) == 0 for value in interface.nuisance * invariant_basis
        )
        assert all(
            sp.simplify(value) == 0
            for value in interface.nuisance * gaussian_section - target0
        )
        assert all(
            sp.simplify(value) == 0 for value in interface.nuisance * section_shift
        )
        assert invariant_basis.rank() == 8
        assert all(
            all(
                sp.simplify(value) == 0
                for value in action * invariant_basis - invariant_basis
            )
            for action in interface.raw_actions
        )

    invariant_basis_rows = tuple(invariant_basis.T.rref()[1])
    assert len(invariant_basis_rows) == 8
    invariant_basis_pivot = sp.factor(
        invariant_basis[list(invariant_basis_rows), :].det()
    )
    assert invariant_basis_pivot != 0
    return StaticInvariantData(
        raw_reynolds_kernel=reynolds_kernel,
        raw_invariant_pivots=invariant_pivots,
        raw_invariant_basis=raw_invariant_basis,
        invariant_basis=invariant_basis,
        invariant_basis_rows=invariant_basis_rows,
        invariant_basis_pivot=invariant_basis_pivot,
        section_shift=section_shift,
        gaussian_section=gaussian_section,
        gaussian_transformed_basis=gaussian_transformed_basis,
        gaussian_raw_pivots=gaussian_raw_pivots,
    )


def product_coefficient(
    left: int,
    right: int,
    first: Sequence[sp.Expr],
    second: Sequence[sp.Expr],
) -> sp.Expr:
    if left == right:
        return first[left] * second[right]
    return first[left] * second[right] + first[right] * second[left]


def quadratic_matrix_from_linear_forms(
    root_maps: Sequence[sp.Matrix],
    affine_columns: Sequence[sp.Matrix],
    descriptors: Sequence[tuple[int, int, int, int]] = MINOR_DESCRIPTORS,
) -> sp.Matrix:
    """Build the 45 selected quadratic columns from three 65-row maps."""

    assert len(root_maps) == len(affine_columns) == 3
    assert all(matrix.shape[1] == 8 for matrix in root_maps)
    assert all(matrix.rows == 65 for matrix in root_maps)
    assert all(matrix.shape == (65, 1) for matrix in affine_columns)
    linear_forms = [
        [
            tuple(sp.expand(root_maps[root][row, column]) for column in range(8))
            + (sp.expand(affine_columns[root][row, 0]),)
            for row in range(65)
        ]
        for root in range(3)
    ]
    selected_columns = []
    for left_row, right_row, left_column, right_column in descriptors:
        first = linear_forms[left_column][left_row]
        second = linear_forms[right_column][right_row]
        third = linear_forms[right_column][left_row]
        fourth = linear_forms[left_column][right_row]
        selected_columns.append(
            sp.Matrix(
                [
                    sp.expand(
                        product_coefficient(left, right, first, second)
                        - product_coefficient(left, right, third, fourth)
                    )
                    for left, right in DEGREE_TWO_PAIRS
                ]
            )
        )
    matrix = sp.Matrix.hstack(*selected_columns)
    assert matrix.shape == (45, 45)
    return matrix


@dataclass
class MovingResponseEvaluation:
    """Exact response data at one frame substitution."""

    substitutions: dict[sp.Symbol, sp.Expr]
    frames: tuple[sp.Matrix, ...]
    frame_determinants: tuple[sp.Expr, ...]
    frame_denominator: sp.Expr
    quotient_gamma: sp.Expr
    alpha_section: sp.Matrix
    invariant_basis: sp.Matrix
    root_maps: tuple[sp.Matrix, ...]
    affine_columns: tuple[sp.Matrix, ...]
    quadratic_matrix: sp.Matrix
    denominator_free: bool

    @property
    def quadratic_rank(self) -> int:
        return int(self.quadratic_matrix.rank())


@dataclass
class MovingQuadraticCircuit:
    """Exact evaluable arithmetic circuit for the moving 45-by-45 matrix."""

    builder: "MovingResponseBuilder"
    descriptors: tuple[tuple[int, int, int, int], ...] = MINOR_DESCRIPTORS

    def evaluate(
        self,
        substitutions: Mapping[sp.Symbol, sp.Expr] | None = None,
        denominator_free: bool = True,
    ) -> sp.Matrix:
        return self.builder.evaluate(
            substitutions=substitutions,
            denominator_free=denominator_free,
        ).quadratic_matrix

    def symbolic(self, denominator_free: bool = True) -> sp.Matrix:
        """Materialize the symbolic matrix; this may be substantially larger."""

        return self.builder.evaluate_symbolic(
            denominator_free=denominator_free,
        ).quadratic_matrix


@dataclass
class MovingResponseBuilder:
    """Reusable GLD75--80 moving response construction."""

    modules: RepositoryModules
    chart: EqualLeafChart
    interface: FixedNuisanceInterface
    transport: AdjugateTensorTransport
    raw_transport: AdjugateRawIntertwiner
    quotient: MixedQuotientPivot
    invariant: StaticInvariantData
    ledger: LocalizationLedger
    _target: sp.Matrix | None = field(default=None, init=False, repr=False)
    _alpha_section: sp.Matrix | None = field(default=None, init=False, repr=False)

    @property
    def quadratic_circuit(self) -> MovingQuadraticCircuit:
        return MovingQuadraticCircuit(self)

    def target(self) -> sp.Matrix:
        if self._target is None:
            self._target = self.chart.target(self.modules.parent)
        return self._target

    def alpha_section(self) -> sp.Matrix:
        """Return the Reynolds-averaged fixed-pivot section over the chart."""

        if self._alpha_section is None:
            fixed_section = self.interface.solve_target(self.target())
            self._alpha_section = (
                self.interface.reynolds_average(fixed_section)
                + self.invariant.section_shift
            ).applyfunc(sp.expand)
        return self._alpha_section

    def _normalise_substitutions(
        self,
        substitutions: Mapping[sp.Symbol, sp.Expr] | None,
    ) -> dict[sp.Symbol, sp.Expr]:
        if substitutions is None:
            return self.chart.origin
        result = self.chart.origin
        for symbol, value in substitutions.items():
            assert symbol in self.chart.shifts
            result[symbol] = sp.sympify(value)
        assert sp.simplify(result[self.chart.shifts[8]]) == 0, (
            "the GLD82 builder is defined on the scale-fixed chart x8=0"
        )
        return result

    def _ledger_with_values(
        self,
        frame_determinants: tuple[sp.Expr, ...],
        frame_denominator: sp.Expr,
        gamma: sp.Expr,
    ) -> LocalizationLedger:
        # The base ledger remains structural; this copy makes numeric values
        # available to callers without mutating the builder's declaration.
        result = LocalizationLedger()
        for factor in self.ledger.factors:
            if factor.name == "frame_denominator":
                result.add(
                    LocalizationFactor(
                        **{
                            **factor.__dict__,
                            "numerator": frame_denominator,
                        }
                    )
                )
            elif factor.name == "mixed_quotient_pivot":
                result.add(
                    LocalizationFactor(
                        **{
                            **factor.__dict__,
                            "numerator": gamma,
                        }
                    )
                )
            else:
                result.add(factor)
        return result

    def evaluate(
        self,
        substitutions: Mapping[sp.Symbol, sp.Expr] | None = None,
        denominator_free: bool = True,
    ) -> MovingResponseEvaluation:
        """Evaluate the exact circuit after specializing the survivor shifts."""

        substitutions = self._normalise_substitutions(substitutions)
        frames = tuple(
            frame.subs(substitutions).applyfunc(sp.expand)
            for frame in self.chart.frames
        )
        frame_determinants = tuple(sp.factor(frame.det()) for frame in frames)
        frame_denominator = sp.factor(sp.prod(frame_determinants))
        target = self.target().subs(substitutions).applyfunc(sp.expand)
        alpha_section = self.alpha_section().subs(substitutions).applyfunc(sp.expand)
        invariant_basis = self.invariant.invariant_basis

        constant_num = self.transport.apply(
            self.interface.constant,
            substitutions=substitutions,
            expand=False,
        )
        constant_mixed = constant_num.extract(
            self.interface.mixed_rows,
            range(self.interface.constant.cols),
        )
        pivot = constant_mixed[list(self.quotient.pivot_positions), :]
        quotient = constant_mixed[list(self.quotient.quotient_positions), :]
        gamma = sp.factor(pivot.det())
        if denominator_free:
            pivot_operator = pivot.adjugate()

            def project(value_mixed: sp.Matrix) -> sp.Matrix:
                value_pivot = value_mixed[list(self.quotient.pivot_positions), :]
                value_quotient = value_mixed[list(self.quotient.quotient_positions), :]
                return (
                    gamma * value_quotient - quotient * pivot_operator * value_pivot
                ).applyfunc(sp.expand)

        else:
            assert gamma != 0
            pivot_operator = pivot.inv()

            def project(value_mixed: sp.Matrix) -> sp.Matrix:
                value_pivot = value_mixed[list(self.quotient.pivot_positions), :]
                value_quotient = value_mixed[list(self.quotient.quotient_positions), :]
                return (
                    value_quotient - quotient * pivot_operator * value_pivot
                ).applyfunc(sp.expand)

        root_maps: list[sp.Matrix] = []
        affine_columns: list[sp.Matrix] = []
        for response in self.interface.response_maps[:3]:
            response_num = self.transport.apply(
                response,
                substitutions=substitutions,
                expand=False,
            )
            invariant_output = response_num * invariant_basis
            affine_output = response_num * alpha_section
            invariant_mixed = invariant_output.extract(
                self.interface.mixed_rows,
                range(invariant_output.cols),
            )
            affine_mixed = affine_output.extract(
                self.interface.mixed_rows,
                range(affine_output.cols),
            )
            invariant_quotient = project(invariant_mixed)
            affine_quotient = project(affine_mixed)
            if not denominator_free:
                # U_num is d_F times U_F.  Quotienting does not remove that
                # common output scalar, so restore the literal-Delta map.
                invariant_quotient = invariant_quotient.applyfunc(
                    lambda value: sp.cancel(value / frame_denominator)
                )
                affine_quotient = affine_quotient.applyfunc(
                    lambda value: sp.cancel(value / frame_denominator)
                )
            root_maps.append(invariant_quotient)
            affine_columns.append(affine_quotient)

        matrix = quadratic_matrix_from_linear_forms(
            root_maps,
            affine_columns,
        )
        assert target.rows == 81
        return MovingResponseEvaluation(
            substitutions=substitutions,
            frames=frames,
            frame_determinants=frame_determinants,
            frame_denominator=frame_denominator,
            quotient_gamma=gamma,
            alpha_section=alpha_section,
            invariant_basis=invariant_basis,
            root_maps=tuple(root_maps),
            affine_columns=tuple(affine_columns),
            quadratic_matrix=matrix,
            denominator_free=denominator_free,
        )

    def evaluate_symbolic(
        self, denominator_free: bool = True
    ) -> MovingResponseEvaluation:
        """Materialize the symbolic circuit over the 15-variable chart."""

        # An empty mapping would mean the origin in evaluate(); symbolic
        # construction therefore uses the explicit symbolic path below.
        substitutions: Mapping[sp.Symbol, sp.Expr] | None = {
            symbol: (sp.Integer(0) if index == 8 else symbol)
            for index, symbol in enumerate(self.chart.shifts)
        }
        return self.evaluate(
            substitutions=substitutions,
            denominator_free=denominator_free,
        )

    def structural_ledger(self) -> dict[str, object]:
        return self.ledger.as_dict()


def _build_ledger(
    chart: EqualLeafChart,
    interface: FixedNuisanceInterface,
    transport: AdjugateTensorTransport,
    invariant: StaticInvariantData,
) -> LocalizationLedger:
    ledger = LocalizationLedger()
    gauge = sp.prod(chart.leaf[0, colour] for _mode in (1, 2, 3) for colour in range(3))
    frame_determinants = transport.determinants
    frame_denominator = transport.denominator_product
    ledger.add(
        LocalizationFactor(
            name="gauge_open",
            role="GLD75 normalized leaf-frame gauge",
            denominator_exponent=0,
            numerator=gauge,
            base_value=gauge.subs(chart.origin),
            notes="The normalized equal-leaf chart makes this factor 1.",
        )
    )
    for mode, determinant in enumerate(frame_determinants):
        ledger.add(
            LocalizationFactor(
                name=f"det_F_{mode}",
                role="frame inverse in U_F and S_F",
                denominator_exponent=1,
                numerator=determinant,
                base_value=determinant.subs(chart.origin),
                circuit=f"det(F_{mode})",
            )
        )
    ledger.add(
        LocalizationFactor(
            name="frame_denominator",
            role="common denominator of U_F",
            denominator_exponent=1,
            numerator=frame_denominator,
            base_value=frame_denominator.subs(chart.origin),
            circuit="prod_mode det(F_mode)",
        )
    )
    ledger.add(
        LocalizationFactor(
            name="nuisance_pivot",
            role="fixed GLD70 rank-44 nuisance pivot",
            denominator_exponent=0,
            numerator=sp.Integer(interface.modules.parent.STAR_MINOR_CONSTANT),
            base_value=sp.Integer(interface.modules.parent.STAR_MINOR_CONSTANT),
            notes="Transport uses this fixed pivot; no moving inverse is hidden.",
        )
    )
    ledger.add(
        LocalizationFactor(
            name="mixed_quotient_pivot",
            role="moving rank-13 mixed quotient pivot",
            denominator_exponent=1,
            circuit=(
                "det((U_num(F) C)_mixed[pivot_positions,:]); "
                "pivot_positions=" + repr(list(MOVING_MIXED_PIVOT_POSITIONS))
            ),
            notes="The numerator is evaluated by the quotient circuit.",
        )
    )
    ledger.add(
        LocalizationFactor(
            name="invariant_kernel_pivot",
            role="fixed rank-8 invariant-kernel basis",
            denominator_exponent=0,
            numerator=invariant.invariant_basis_pivot,
            base_value=invariant.invariant_basis_pivot,
            notes="The fixed-coordinate route introduces no moving basis divisor.",
        )
    )
    ledger.add(
        LocalizationFactor(
            name="support_open",
            role="GLD70 full-support interface hypothesis",
            denominator_exponent=0,
            numerator=sp.Integer(1),
            base_value=sp.Integer(1),
            circuit="fixed GLD70 support coordinates",
            notes="A fixed nonzero branch hypothesis, not a moving frame denominator.",
        )
    )
    ledger.add(
        LocalizationFactor(
            name="nonisotropic_open",
            role="GLD70 nonisotropic slope hypothesis",
            denominator_exponent=0,
            numerator=sp.Integer(1),
            base_value=sp.Integer(1),
            circuit="fixed GLD70 nonisotropic slope factor",
            notes="A fixed nonzero branch hypothesis, not a moving frame denominator.",
        )
    )
    return ledger


def build_moving_response_builder(
    calibrate_gaussian: bool = True,
    modules: RepositoryModules | None = None,
) -> MovingResponseBuilder:
    """Build the reusable GLD75--80 moving response circuit."""

    modules = modules or load_repository_modules()
    chart = build_equal_leaf_chart(modules)
    interface = build_fixed_nuisance_interface(modules)
    transport = adjugate_tensor_transport(
        chart.frames,
        modules.parent.LOCAL_INDICES,
    )
    raw_transport = adjugate_raw_intertwiner(
        chart.frames,
        interface.raw_descriptors,
        adjugates=transport.adjugates,
        determinants=transport.determinants,
    )
    quotient = fixed_mixed_quotient_pivot(interface, moving=True)
    invariant = build_static_invariant_data(
        interface,
        chart,
        calibrate_gaussian=calibrate_gaussian,
    )
    ledger = _build_ledger(chart, interface, transport, invariant)
    return MovingResponseBuilder(
        modules=modules,
        chart=chart,
        interface=interface,
        transport=transport,
        raw_transport=raw_transport,
        quotient=quotient,
        invariant=invariant,
        ledger=ledger,
    )


def build_quadratic_matrix(
    builder: MovingResponseBuilder | None = None,
    substitutions: Mapping[sp.Symbol, sp.Expr] | None = None,
    denominator_free: bool = True,
) -> MovingQuadraticCircuit | sp.Matrix:
    """Return a circuit, or evaluate its 45-by-45 matrix at substitutions.

    With no substitutions this returns an exact evaluable circuit rather than
    eagerly expanding the large symbolic determinant.  Pass a mapping of the
    15 GLD75 shifts to obtain an exact specialized SymPy matrix.
    """

    builder = builder or build_moving_response_builder()
    if substitutions is None:
        return builder.quadratic_circuit
    return builder.quadratic_circuit.evaluate(
        substitutions=substitutions,
        denominator_free=denominator_free,
    )


def _decode_gaussian(value: Sequence[int]) -> sp.Expr:
    assert len(value) == 4
    real_p, real_q, imaginary_p, imaginary_q = value
    return sp.Rational(real_p, real_q) + sp.I * sp.Rational(imaginary_p, imaginary_q)


def _stored_gaussian_reference_matrix() -> tuple[sp.Matrix, sp.Expr]:
    """Load the byte-pinned Gaussian matrix independently audited by GLD82."""

    stored = GAUSSIAN_QUADRATIC_CERTIFICATE_PATH.read_bytes().replace(b"\r\n", b"\n")
    assert hashlib.sha256(stored).hexdigest() == GAUSSIAN_QUADRATIC_CERTIFICATE_SHA256
    payload = json.loads(stored)
    assert payload["format"] == "gaussian-quadratic-macaulay-Qi-v1"
    assert tuple(tuple(item) for item in payload["minor_descriptors"]) == (
        MINOR_DESCRIPTORS
    )
    columns = [
        sp.Matrix([_decode_gaussian(value) for value in column])
        for column in payload["columns"]
    ]
    matrix = sp.Matrix.hstack(*columns)
    determinant = _decode_gaussian(payload["determinant"])
    assert matrix.shape == (45, 45) and determinant != 0
    return matrix, determinant


def validate_gld72(
    builder: MovingResponseBuilder | None = None,
) -> dict[str, object]:
    """Validate the rational moving circuit against the committed GLD74 matrix."""

    builder = builder or build_moving_response_builder(calibrate_gaussian=True)
    origin = builder.chart.origin
    moving = builder.evaluate(origin, denominator_free=False)
    reference, reference_det = _stored_gaussian_reference_matrix()
    equal = moving.quadratic_matrix == reference
    assert moving.quadratic_matrix.shape == reference.shape == (45, 45)
    assert moving.frame_denominator != 0
    assert moving.quotient_gamma != 0
    # Equality is expected after the constant Gaussian calibration.  Keep the
    # assertion exact: a basis mismatch must not be silently reported as a
    # successful validation.
    assert equal
    return {
        "status": "moving_response_builder_gld72_validation_pass",
        "global_conjecture": "UNRESOLVED",
        "field": "Q(i)",
        "survivor_shift_count": len(builder.chart.shifts),
        "survivor_generator_count": len(builder.chart.survivor_generators),
        "nuisance_shape_rank": [
            builder.interface.nuisance.rows,
            builder.interface.nuisance.cols,
            builder.interface.nuisance.rank(),
        ],
        "raw_kernel_shape": list(builder.interface.kernel.shape),
        "moving_quotient_shape": [65, 78],
        "moving_mixed_pivot_positions": list(builder.quotient.pivot_positions),
        "frame_determinants_at_gld72": [
            str(value) for value in moving.frame_determinants
        ],
        "frame_denominator_at_gld72": str(moving.frame_denominator),
        "mixed_quotient_gamma_numerator_at_gld72": str(moving.quotient_gamma),
        "invariant_basis_shape": list(builder.invariant.invariant_basis.shape),
        "invariant_basis_pivot": str(builder.invariant.invariant_basis_pivot),
        "quadratic_shape_rank": [
            *moving.quadratic_matrix.shape,
            45,
        ],
        "gaussian_reference_determinant": str(reference_det),
        "gaussian_matrix_exactly_matches": equal,
        "denominator_free_circuit_available": True,
        "localization": builder.structural_ledger(),
        "theorem_claimed": False,
    }


def main() -> None:
    result = validate_gld72()
    print("four-root survivor moving response builder: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
