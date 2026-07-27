"""SAT + exact signed-lattice probe after tricolour row coverage.

The SAT layer deliberately over-approximates complex local maps: it uses
only exact zero/nonzero entries, source-row tricolour coverage, structural
rank three of every local map, nonempty pure-colour permanents, and the
absence of a uniquely supported mixed permanent.

Each model is then tested for an inconsistent integer lattice of two-term
mixed cancellation equations.  Exploratory only until a complete,
independently replayed UNSAT/CEGAR certificate is produced.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import pathlib
import subprocess
import sys
from fractions import Fraction

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from integer_signed_lattice import IntegerSignedLattice  # noqa: E402
from integer_constant_lattice import IntegerConstantLattice  # noqa: E402


MODES = tuple(range(5))
SOURCES = tuple(range(5))
COLOURS = tuple(range(3))
PERMUTATIONS = tuple(itertools.permutations(SOURCES))
MIXED = tuple(
    colours
    for colours in itertools.product(COLOURS, repeat=5)
    if len(set(colours)) > 1
)
ALL_COLOURINGS = tuple(itertools.product(COLOURS, repeat=5))


def entry_key(mode: int, source: int, colour: int) -> tuple:
    return ("x", mode, source, colour)


def add_and_equivalence(
    cnf: CNF, output: int, factors: list[int]
) -> None:
    for factor in factors:
        cnf.append([-output, factor])
    cnf.append([output] + [-factor for factor in factors])


def add_lex_leq(
    cnf: CNF,
    pool: IDPool,
    left: list[int],
    right: list[int],
    label: tuple,
) -> None:
    """Exact Boolean lexicographic constraint left <= right."""
    assert len(left) == len(right)
    prefix = pool.id(("lex_prefix", *label, 0))
    cnf.append([prefix])
    for index, (left_bit, right_bit) in enumerate(zip(left, right)):
        # If all earlier bits agree, 1 > 0 is forbidden here.
        cnf.append([-prefix, -left_bit, right_bit])
        equal = pool.id(("lex_equal", *label, index))
        cnf.extend(
            [
                [-equal, -left_bit, right_bit],
                [-equal, left_bit, -right_bit],
                [equal, left_bit, right_bit],
                [equal, -left_bit, -right_bit],
            ]
        )
        next_prefix = pool.id(("lex_prefix", *label, index + 1))
        cnf.extend(
            [
                [-next_prefix, prefix],
                [-next_prefix, equal],
                [next_prefix, -prefix, -equal],
            ]
        )
        prefix = next_prefix


def finite_field_local_signatures() -> tuple[tuple, ...]:
    source = ROOT / "tmp" / "probe_p5_hall_hierarchy_csp.py"
    dependency = ROOT / "audit_five_row_projective_normal_forms.py"
    cache = ROOT / "tmp" / "p5_local_signatures_cache.json"
    fingerprint = hashlib.sha256(
        source.read_bytes() + b"\0" + dependency.read_bytes()
    ).hexdigest()
    if cache.exists():
        payload = json.loads(cache.read_text(encoding="utf-8"))
        if (
            payload.get("schema") == 1
            and payload.get("source_fingerprint") == fingerprint
            and payload.get("count") == 6495
        ):
            signatures = tuple(
                (tuple(item[0]), tuple(item[1]))
                for item in payload["signatures"]
            )
            if len(signatures) == 6495:
                return signatures

    spec = importlib.util.spec_from_file_location("hall_probe", source)
    hall = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(hall)
    signatures = tuple(sorted(hall.local_signatures()))
    assert len(signatures) == 6495
    cache.write_text(
        json.dumps(
            {
                "schema": 1,
                "source_fingerprint": fingerprint,
                "count": len(signatures),
                "signatures": signatures,
            },
            separators=(",", ":"),
        )
        + "\n",
        encoding="utf-8",
    )
    return signatures


def build_cnf(
    allowed_local_signatures: tuple[tuple, ...] | None = None,
    double_lex: bool = False,
    hall_hierarchy: bool = False,
    pair_hierarchy: bool = False,
    abstract_pairs: bool = False,
) -> tuple[CNF, IDPool]:
    pool = IDPool()
    cnf = CNF()

    # For every source row and colour, some mode has exactly that
    # singleton support.
    for source in SOURCES:
        for colour in COLOURS:
            singletons = []
            for mode in MODES:
                singleton = pool.id(("singleton", mode, source, colour))
                factors = [pool.id(entry_key(mode, source, colour))]
                other = [
                    pool.id(entry_key(mode, source, other_colour))
                    for other_colour in COLOURS
                    if other_colour != colour
                ]
                for factor in factors:
                    cnf.append([-singleton, factor])
                for factor in other:
                    cnf.append([-singleton, -factor])
                cnf.append([singleton, -factors[0], *other])
                singletons.append(singleton)
            cnf.append(singletons)

    # Structural column rank three is necessary for injectivity.
    injections = tuple(itertools.permutations(SOURCES, 3))
    for mode in MODES:
        witnesses = []
        for injection in injections:
            witness = pool.id(("local_rank", mode, injection))
            factors = [
                pool.id(entry_key(mode, injection[colour], colour))
                for colour in COLOURS
            ]
            add_and_equivalence(cnf, witness, factors)
            witnesses.append(witness)
        cnf.append(witnesses)

    if allowed_local_signatures is not None:
        local_pattern_variables: list[list[int]] = []
        for mode in MODES:
            witnesses = []
            for pattern_index, signature in enumerate(
                allowed_local_signatures
            ):
                pattern = signature[0]
                witness = pool.id(("local_pattern", mode, pattern_index))
                witnesses.append(witness)
                for source in SOURCES:
                    for colour in COLOURS:
                        entry = pool.id(entry_key(mode, source, colour))
                        cnf.append(
                            [-witness, entry]
                            if pattern[source] & (1 << colour)
                            else [-witness, -entry]
                        )
            cnf.append(witnesses)
            local_pattern_variables.append(witnesses)

            # A signature includes incidence information in addition to its
            # zero/nonzero support.  Select one actual signature rather than
            # allowing several incompatible incidence refinements of the
            # same support simultaneously.
            if hall_hierarchy or pair_hierarchy:
                cnf.extend(
                    CardEnc.atmost(
                        witnesses,
                        bound=1,
                        vpool=pool,
                        encoding=EncType.seqcounter,
                    ).clauses
                )

        if hall_hierarchy or pair_hierarchy:
            source_subsets = (
                tuple(itertools.combinations(SOURCES, 2))
                if pair_hierarchy
                else tuple(
                    subset
                    for size in (2, 3, 4)
                    for subset in itertools.combinations(SOURCES, size)
                )
            )
            for subset_index, subset in enumerate(source_subsets):
                required = len(subset)
                for colour in COLOURS:
                    containing_modes = []
                    for mode in MODES:
                        incidence = pool.id(
                            (
                                "hierarchy_incidence",
                                mode,
                                subset_index,
                                colour,
                            )
                        )
                        supporting_patterns = [
                            local_pattern_variables[mode][pattern_index]
                            for pattern_index, signature in enumerate(
                                allowed_local_signatures
                            )
                            if signature[1][subset_index]
                            & (1 << colour)
                        ]
                        for witness in supporting_patterns:
                            cnf.append([-witness, incidence])
                        cnf.append([-incidence, *supporting_patterns])
                        containing_modes.append(incidence)
                    cnf.extend(
                        CardEnc.atleast(
                            containing_modes,
                            bound=required,
                            vpool=pool,
                            encoding=EncType.seqcounter,
                        ).clauses
                    )

    if abstract_pairs:
        source_pairs = tuple(itertools.combinations(SOURCES, 2))
        source_pair_index = {
            pair: index for index, pair in enumerate(source_pairs)
        }
        # Keep the incidence-variable numbering stable as more auxiliary
        # local-geometry constraints are added below.
        for mode in MODES:
            for pair_index, _pair in enumerate(source_pairs):
                for colour in COLOURS:
                    pool.id(
                        (
                            "pair_incidence",
                            mode,
                            pair_index,
                            colour,
                        )
                    )

        def incidence_possible(
            first_mask: int, second_mask: int, colour: int
        ) -> bool:
            coordinate = 1 << colour
            if first_mask == coordinate or second_mask == coordinate:
                return True
            other_mask = 7 ^ coordinate
            first_projection = first_mask & other_mask
            second_projection = second_mask & other_mask
            return (
                first_projection != 0
                and first_projection == second_projection
                and bool((first_mask | second_mask) & coordinate)
            )

        for mode in MODES:
            same_coordinate_variables: dict[tuple[int, int, int], int] = {}
            for pair_index, (first, second) in enumerate(source_pairs):
                incidence_variables = [
                    pool.id(("pair_incidence", mode, pair_index, colour))
                    for colour in COLOURS
                ]
                cnf.append(incidence_variables)
                cnf.append([-variable for variable in incidence_variables])

                for colour, incidence in enumerate(incidence_variables):
                    first_singleton = pool.id(
                        ("singleton", mode, first, colour)
                    )
                    second_singleton = pool.id(
                        ("singleton", mode, second, colour)
                    )
                    cnf.append([-first_singleton, incidence])
                    cnf.append([-second_singleton, incidence])

                    same_coordinate = pool.id(
                        (
                            "same_coordinate_pair",
                            mode,
                            pair_index,
                            colour,
                        )
                    )
                    same_coordinate_variables[
                        (first, second, colour)
                    ] = same_coordinate
                    cnf.extend(
                        [
                            [-same_coordinate, first_singleton],
                            [-same_coordinate, second_singleton],
                            [
                                same_coordinate,
                                -first_singleton,
                                -second_singleton,
                            ],
                        ]
                    )
                    for first_mask in range(8):
                        for second_mask in range(8):
                            if incidence_possible(
                                first_mask, second_mask, colour
                            ):
                                continue
                            exclusion = [-incidence]
                            for source, mask in (
                                (first, first_mask),
                                (second, second_mask),
                            ):
                                for entry_colour in COLOURS:
                                    entry = pool.id(
                                        entry_key(
                                            mode, source, entry_colour
                                        )
                                    )
                                    exclusion.append(
                                        -entry
                                        if mask & (1 << entry_colour)
                                        else entry
                                    )
                            cnf.append(exclusion)

                # Exact coordinate-plane inference from zero patterns.  Two
                # nonzero rows supported inside {c,d}, jointly using both
                # coordinates, must span that coordinate plane whenever
                # their span contains any coordinate at all.  (If they were
                # dependent, their common non-coordinate line would violate
                # the local pair condition already imposed above.)
                for left, right in itertools.combinations(COLOURS, 2):
                    plane_mask = (1 << left) | (1 << right)
                    plane_supports = (
                        1 << left,
                        1 << right,
                        plane_mask,
                    )
                    for first_mask in plane_supports:
                        for second_mask in plane_supports:
                            if first_mask | second_mask != plane_mask:
                                continue
                            antecedent_escape = []
                            for source, mask in (
                                (first, first_mask),
                                (second, second_mask),
                            ):
                                for entry_colour in COLOURS:
                                    entry = pool.id(
                                        entry_key(
                                            mode, source, entry_colour
                                        )
                                    )
                                    antecedent_escape.append(
                                        -entry
                                        if mask & (1 << entry_colour)
                                        else entry
                                    )
                            cnf.append(
                                [
                                    *antecedent_escape,
                                    incidence_variables[left],
                                ]
                            )
                            cnf.append(
                                [
                                    *antecedent_escape,
                                    incidence_variables[right],
                                ]
                            )

                # If the pair spans two coordinate points, its two rows lie
                # in that coordinate plane and jointly use both axes.
                for left, right in itertools.combinations(COLOURS, 2):
                    left_incidence = incidence_variables[left]
                    right_incidence = incidence_variables[right]
                    excluded_colour = next(
                        colour
                        for colour in COLOURS
                        if colour not in (left, right)
                    )
                    for source in (first, second):
                        cnf.append(
                            [
                                -left_incidence,
                                -right_incidence,
                                -pool.id(
                                    entry_key(
                                        mode, source, excluded_colour
                                    )
                                ),
                            ]
                        )
                    for colour in (left, right):
                        cnf.append(
                            [
                                -left_incidence,
                                -right_incidence,
                                pool.id(entry_key(mode, first, colour)),
                                pool.id(entry_key(mode, second, colour)),
                            ]
                        )

            # Projective plane closure.  If spans (a,b) and (a,d) both
            # contain e_c and row a is not itself e_c, then b and d lie in
            # the same projective line <a,e_c>.  Their span therefore also
            # contains e_c unless b and d are the same coordinate point.
            for centre in SOURCES:
                others = tuple(
                    source for source in SOURCES if source != centre
                )
                for first, second in itertools.combinations(others, 2):
                    centre_first = source_pair_index[
                        tuple(sorted((centre, first)))
                    ]
                    centre_second = source_pair_index[
                        tuple(sorted((centre, second)))
                    ]
                    outer_pair = tuple(sorted((first, second)))
                    outer_index = source_pair_index[outer_pair]
                    for colour in COLOURS:
                        same_coordinate_escapes = [
                            same_coordinate_variables[
                                (
                                    outer_pair[0],
                                    outer_pair[1],
                                    coordinate,
                                )
                            ]
                            for coordinate in COLOURS
                        ]
                        cnf.append(
                            [
                                -pool.id(
                                    (
                                        "pair_incidence",
                                        mode,
                                        centre_first,
                                        colour,
                                    )
                                ),
                                -pool.id(
                                    (
                                        "pair_incidence",
                                        mode,
                                        centre_second,
                                        colour,
                                    )
                                ),
                                pool.id(
                                    (
                                        "singleton",
                                        mode,
                                        centre,
                                        colour,
                                    )
                                ),
                                pool.id(
                                    (
                                        "pair_incidence",
                                        mode,
                                        outer_index,
                                        colour,
                                    )
                                ),
                                *same_coordinate_escapes,
                            ]
                        )

        # Exact pair-cover consequence of the kernel Hall hierarchy.
        for pair_index, _pair in enumerate(source_pairs):
            for colour in COLOURS:
                cnf.extend(
                    CardEnc.atleast(
                        [
                            pool.id(
                                (
                                    "pair_incidence",
                                    mode,
                                    pair_index,
                                    colour,
                                )
                            )
                            for mode in MODES
                        ],
                        bound=2,
                        vpool=pool,
                        encoding=EncType.seqcounter,
                    ).clauses
                )

    if double_lex:
        for mode in range(4):
            add_lex_leq(
                cnf,
                pool,
                [
                    pool.id(entry_key(mode, source, colour))
                    for source in SOURCES
                    for colour in COLOURS
                ],
                [
                    pool.id(entry_key(mode + 1, source, colour))
                    for source in SOURCES
                    for colour in COLOURS
                ],
                ("mode", mode),
            )
        for source in range(4):
            add_lex_leq(
                cnf,
                pool,
                [
                    pool.id(entry_key(mode, source, colour))
                    for mode in MODES
                    for colour in COLOURS
                ],
                [
                    pool.id(entry_key(mode, source + 1, colour))
                    for mode in MODES
                    for colour in COLOURS
                ],
                ("source", source),
            )
        for colour in range(2):
            add_lex_leq(
                cnf,
                pool,
                [
                    pool.id(entry_key(mode, source, colour))
                    for mode in MODES
                    for source in SOURCES
                ],
                [
                    pool.id(entry_key(mode, source, colour + 1))
                    for mode in MODES
                    for source in SOURCES
                ],
                ("colour", colour),
            )

    # Pure target coefficients need a supported perfect matching.
    for colour in COLOURS:
        witnesses = []
        for permutation in PERMUTATIONS:
            witness = pool.id(("pure", colour, permutation))
            factors = [
                pool.id(entry_key(mode, permutation[mode], colour))
                for mode in MODES
            ]
            add_and_equivalence(cnf, witness, factors)
            witnesses.append(witness)
        cnf.append(witnesses)

    # A forbidden mixed coefficient cannot have exactly one supported
    # permanent monomial.
    for colours in MIXED:
        witnesses = []
        for permutation in PERMUTATIONS:
            witness = pool.id(("mixed", colours, permutation))
            factors = [
                pool.id(
                    entry_key(mode, permutation[mode], colours[mode])
                )
                for mode in MODES
            ]
            add_and_equivalence(cnf, witness, factors)
            witnesses.append(witness)
        for index, witness in enumerate(witnesses):
            cnf.append(
                [-witness]
                + witnesses[:index]
                + witnesses[index + 1 :]
            )
    return cnf, pool


def supports_from_model(pool: IDPool, model: list[int]) -> tuple[tuple[int, ...], ...]:
    positive = set(value for value in model if value > 0)
    return tuple(
        tuple(
            sum(
                (pool.id(entry_key(mode, source, colour)) in positive)
                << colour
                for colour in COLOURS
            )
            for source in SOURCES
        )
        for mode in MODES
    )


def monomial(
    supports: tuple[tuple[int, ...], ...],
    colours: tuple[int, ...],
    permutation: tuple[int, ...],
    variables: tuple[tuple[int, int, int], ...],
    positions: dict[tuple[int, int, int], int],
) -> list[int]:
    vector = [0] * len(variables)
    for mode in MODES:
        variable = (mode, permutation[mode], colours[mode])
        assert supports[mode][permutation[mode]] & (1 << colours[mode])
        vector[positions[variable]] += 1
    return vector


def signed_lattice_result(
    supports: tuple[tuple[int, ...], ...]
) -> dict:
    variables = tuple(
        (mode, source, colour)
        for mode in MODES
        for source in SOURCES
        for colour in COLOURS
        if supports[mode][source] & (1 << colour)
    )
    positions = {variable: index for index, variable in enumerate(variables)}
    equations = []
    rows = []
    for colours in MIXED:
        active = tuple(
            permutation
            for permutation in PERMUTATIONS
            if all(
                supports[mode][permutation[mode]] & (1 << colours[mode])
                for mode in MODES
            )
        )
        if len(active) != 2:
            continue
        first = monomial(
            supports, colours, active[0], variables, positions
        )
        second = monomial(
            supports, colours, active[1], variables, positions
        )
        rows.append(
            [left - right for left, right in zip(first, second)]
        )
        equations.append((colours, active))
    if not rows:
        return {"binomials": 0, "inconsistent": False}
    lattice = IntegerSignedLattice(rows)
    certificate = None
    contradiction_mode = None
    if lattice.has_inconsistent_kernel:
        witness = next(
            vector
            for vector in lattice.kernel_basis
            if sum(vector) % 2
        )
        certificate = {
            "relation": [
                {
                    "equation_index": index,
                    "coefficient": coefficient,
                    "colours": equations[index][0],
                    "permutations": equations[index][1],
                }
                for index, coefficient in enumerate(witness)
                if coefficient
            ],
            "coefficient_sum": sum(witness),
            "used_binomial_indices": [
                index
                for index, coefficient in enumerate(witness)
                if coefficient
            ],
        }
        contradiction_mode = "inconsistent_binomial_sign"
    else:
        for colours in ALL_COLOURINGS:
            active = tuple(
                permutation
                for permutation in PERMUTATIONS
                if all(
                    supports[mode][permutation[mode]]
                    & (1 << colours[mode])
                    for mode in MODES
                )
            )
            if not active:
                continue
            monomials = [
                monomial(
                    supports,
                    colours,
                    permutation,
                    variables,
                    positions,
                )
                for permutation in active
            ]
            groups: list[dict] = []
            used_binomial_indices: set[int] = set()
            for permutation, vector in zip(active, monomials):
                placed = False
                for group in groups:
                    difference = [
                        left - right
                        for left, right in zip(
                            vector, group["representative_vector"]
                        )
                    ]
                    coordinates = lattice.coordinates(difference)
                    if coordinates is None:
                        continue
                    sign = -1 if sum(coordinates) % 2 else 1
                    used_binomial_indices.update(
                        index
                        for index, coefficient in enumerate(coordinates)
                        if coefficient
                    )
                    group["terms"].append((permutation, sign))
                    group["signed_coefficient"] += sign
                    placed = True
                    break
                if not placed:
                    groups.append(
                        {
                            "representative_vector": vector,
                            "terms": [(permutation, 1)],
                            "signed_coefficient": 1,
                        }
                    )
            nonzero_groups = [
                group for group in groups if group["signed_coefficient"]
            ]
            is_pure = len(set(colours)) == 1
            if (is_pure and not nonzero_groups) or (
                not is_pure and len(nonzero_groups) == 1
            ):
                contradiction_mode = (
                    "annihilated_pure_target"
                    if is_pure
                    else "isolated_signed_monomial_class"
                )
                certificate = {
                    "colours": colours,
                    "active_permutations": active,
                    "groups": [
                        {
                            "representative": group["terms"][0][0],
                            "signed_coefficient": group[
                                "signed_coefficient"
                            ],
                            "terms": group["terms"],
                        }
                        for group in groups
                    ],
                    "used_binomial_indices": sorted(
                        used_binomial_indices
                    ),
                }
                break
    return {
        "binomials": len(rows),
        "lattice_rank": lattice.rank,
        "kernel_dimension": len(lattice.kernel_basis),
        "inconsistent": contradiction_mode is not None,
        "contradiction_mode": contradiction_mode,
        "certificate": certificate,
    }


def singleton_column(
    supports: tuple[tuple[int, ...], ...],
    mode: int,
    colour: int,
) -> int | None:
    active = [
        source
        for source in SOURCES
        if supports[mode][source] & (1 << colour)
    ]
    return active[0] if len(active) == 1 else None


def residual_collision_result(
    supports: tuple[tuple[int, ...], ...]
) -> dict | None:
    """A pure and mixed contraction leave the same residual permanent."""
    for size in (2, 3, 4):
        for modes in itertools.combinations(MODES, size):
            for pure_colour in COLOURS:
                pure_sources = tuple(
                    singleton_column(supports, mode, pure_colour)
                    for mode in modes
                )
                if (
                    any(source is None for source in pure_sources)
                    or len(set(pure_sources)) != size
                ):
                    continue
                source_set = set(pure_sources)
                for mixed_colours in itertools.product(COLOURS, repeat=size):
                    if len(set(mixed_colours)) == 1:
                        continue
                    mixed_sources = tuple(
                        singleton_column(supports, mode, colour)
                        for mode, colour in zip(modes, mixed_colours)
                    )
                    if (
                        any(source is None for source in mixed_sources)
                        or set(mixed_sources) != source_set
                    ):
                        continue
                    return {
                        "contradiction_mode": "residual_permanent_collision",
                        "modes": modes,
                        "pure_colour": pure_colour,
                        "pure_sources": pure_sources,
                        "mixed_colours": mixed_colours,
                        "mixed_sources": mixed_sources,
                    }
    return None


def column_support(
    supports: tuple[tuple[int, ...], ...],
    mode: int,
    colour: int,
) -> frozenset[int]:
    return frozenset(
        source
        for source in SOURCES
        if supports[mode][source] & (1 << colour)
    )


def partial_matchings(
    supports: tuple[tuple[int, ...], ...],
    modes: tuple[int, ...],
    colours: tuple[int, ...],
    source_set: frozenset[int],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        assignment
        for assignment in itertools.permutations(sorted(source_set))
        if all(
            supports[mode][source] & (1 << colour)
            for mode, colour, source in zip(modes, colours, assignment)
        )
    )


def factored_residual_collision_result(
    supports: tuple[tuple[int, ...], ...]
) -> dict | None:
    """A closed pure block and a unique mixed block share a source set."""
    for size in (2, 3, 4):
        for modes in itertools.combinations(MODES, size):
            for pure_colour in COLOURS:
                pure_colours = (pure_colour,) * size
                pure_union = frozenset().union(
                    *(
                        column_support(supports, mode, pure_colour)
                        for mode in modes
                    )
                )
                if len(pure_union) != size:
                    continue
                pure_matchings = partial_matchings(
                    supports, modes, pure_colours, pure_union
                )
                if not pure_matchings:
                    continue
                for mixed_colours in itertools.product(COLOURS, repeat=size):
                    if len(set(mixed_colours)) == 1:
                        continue
                    if any(
                        not column_support(supports, mode, colour)
                        <= pure_union
                        for mode, colour in zip(modes, mixed_colours)
                    ):
                        continue
                    mixed_matchings = partial_matchings(
                        supports, modes, mixed_colours, pure_union
                    )
                    if len(mixed_matchings) != 1:
                        continue
                    return {
                        "contradiction_mode": (
                            "factored_residual_permanent_collision"
                        ),
                        "modes": modes,
                        "source_set": tuple(sorted(pure_union)),
                        "pure_colour": pure_colour,
                        "pure_matchings": pure_matchings,
                        "mixed_colours": mixed_colours,
                        "mixed_matching": mixed_matchings[0],
                    }
    return None


def factored_residual_collision_clause(
    pool: IDPool,
    supports: tuple[tuple[int, ...], ...],
    collision: dict,
) -> tuple[list[int], int, int]:
    modes = tuple(collision["modes"])
    source_set = frozenset(collision["source_set"])
    pure_colour = int(collision["pure_colour"])
    mixed_colours = tuple(collision["mixed_colours"])
    mixed_matching = tuple(collision["mixed_matching"])
    positive: set[int] = set()
    negative: set[int] = set()

    # Preserve confinement of both selected column families to S.
    for mode, mixed_colour in zip(modes, mixed_colours):
        for colour in {pure_colour, mixed_colour}:
            for source in SOURCES:
                if source not in source_set:
                    negative.add(pool.id(entry_key(mode, source, colour)))

    # Preserve the sole nonzero mixed partial-matching monomial.
    for mode, colour, source in zip(
        modes, mixed_colours, mixed_matching
    ):
        positive.add(pool.id(entry_key(mode, source, colour)))

    # Preserve inactivity of all other mixed partial permutations.
    for assignment in itertools.permutations(sorted(source_set)):
        if assignment == mixed_matching:
            continue
        zero_factors = [
            pool.id(entry_key(mode, source, colour))
            for mode, colour, source in zip(
                modes, mixed_colours, assignment
            )
            if not (
                supports[mode][source] & (1 << colour)
            )
        ]
        assert zero_factors
        negative.add(min(zero_factors))
    assert not (positive & negative)
    return (
        [-variable for variable in sorted(positive)] + sorted(negative),
        len(positive),
        len(negative),
    )


def residual_collision_clause(
    pool: IDPool,
    collision: dict,
) -> tuple[list[int], int, int]:
    positive: set[int] = set()
    negative: set[int] = set()
    assignments = (
        (
            collision["modes"],
            (collision["pure_colour"],) * len(collision["modes"]),
            collision["pure_sources"],
        ),
        (
            collision["modes"],
            collision["mixed_colours"],
            collision["mixed_sources"],
        ),
    )
    for modes, colours, sources in assignments:
        for mode, colour, active_source in zip(modes, colours, sources):
            for source in SOURCES:
                variable = pool.id(entry_key(mode, source, colour))
                if source == active_source:
                    positive.add(variable)
                else:
                    negative.add(variable)
    assert not (positive & negative)
    return (
        [-variable for variable in sorted(positive)] + sorted(negative),
        len(positive),
        len(negative),
    )


def active_permutations(
    supports: tuple[tuple[int, ...], ...],
    colours: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        permutation
        for permutation in PERMUTATIONS
        if all(
            supports[mode][permutation[mode]] & (1 << colours[mode])
            for mode in MODES
        )
    )


def conflict_cube_clause(
    pool: IDPool,
    supports: tuple[tuple[int, ...], ...],
    lattice: dict,
) -> tuple[list[int], int, int]:
    certificate = lattice["certificate"]
    assert certificate is not None
    if lattice["contradiction_mode"] == "inconsistent_binomial_sign":
        binomial_colours = [
            tuple(item["colours"])
            for item in certificate["relation"]
        ]
        target_colours: list[tuple[int, ...]] = []
    else:
        used = set(certificate["used_binomial_indices"])
        # Reconstruct the same ordered binomial list.
        all_binomial_colours = [
            colours
            for colours in MIXED
            if len(active_permutations(supports, colours)) == 2
        ]
        binomial_colours = [
            all_binomial_colours[index] for index in sorted(used)
        ]
        target_colours = [tuple(certificate["colours"])]
    used_colours = tuple(dict.fromkeys(binomial_colours + target_colours))

    positive: set[int] = set()
    negative: set[int] = set()
    for colours in used_colours:
        active = set(active_permutations(supports, colours))
        for permutation in PERMUTATIONS:
            factors = [
                pool.id(
                    entry_key(mode, permutation[mode], colours[mode])
                )
                for mode in MODES
            ]
            if permutation in active:
                positive.update(factors)
                continue
            zero_factors = [
                factor
                for mode, factor in enumerate(factors)
                if not (
                    supports[mode][permutation[mode]]
                    & (1 << colours[mode])
                )
            ]
            assert zero_factors
            negative.add(min(zero_factors))
    assert not (positive & negative)
    clause = [-variable for variable in sorted(positive)] + sorted(negative)
    return clause, len(positive), len(negative)


def block_exact_support(
    solver: Solver,
    pool: IDPool,
    supports: tuple[tuple[int, ...], ...],
) -> None:
    clause = []
    for mode in MODES:
        for source in SOURCES:
            for colour in COLOURS:
                variable = pool.id(entry_key(mode, source, colour))
                clause.append(
                    -variable
                    if supports[mode][source] & (1 << colour)
                    else variable
                )
    solver.add_clause(clause)


def exact_support_clause(
    pool: IDPool,
    supports: tuple[tuple[int, ...], ...],
) -> list[int]:
    clause = []
    for mode in MODES:
        for source in SOURCES:
            for colour in COLOURS:
                variable = pool.id(entry_key(mode, source, colour))
                clause.append(
                    -variable
                    if supports[mode][source] & (1 << colour)
                    else variable
                )
    return clause


def binomial_closure_result(
    supports: tuple[tuple[int, ...], ...],
    local_signatures: tuple[tuple, ...] | None = None,
    return_frontier: bool = False,
) -> dict | None:
    """Iteratively promote two signed monomial classes to new relations."""
    variables = tuple(
        (mode, source, colour)
        for mode in MODES
        for source in SOURCES
        for colour in COLOURS
        if supports[mode][source] & (1 << colour)
    )
    positions = {variable: index for index, variable in enumerate(variables)}
    equation_data = []
    for colours in ALL_COLOURINGS:
        active = active_permutations(supports, colours)
        equation_data.append(
            (
                colours,
                active,
                [
                    monomial(
                        supports,
                        colours,
                        permutation,
                        variables,
                        positions,
                    )
                    for permutation in active
                ],
            )
        )

    rows: list[list[int]] = []
    constants: list[Fraction] = []
    records: list[dict] = []
    if local_signatures is not None:
        source_pairs = tuple(itertools.combinations(SOURCES, 2))
        for mode, signature in enumerate(local_signatures):
            _local_supports, incidences = signature
            for pair_index, (first, second) in enumerate(source_pairs):
                incidence_mask = incidences[pair_index]
                for coordinate in COLOURS:
                    if not (incidence_mask & (1 << coordinate)):
                        continue
                    other = [
                        colour
                        for colour in COLOURS
                        if colour != coordinate
                    ]
                    first_variables = (
                        (mode, first, other[0]),
                        (mode, second, other[1]),
                    )
                    second_variables = (
                        (mode, first, other[1]),
                        (mode, second, other[0]),
                    )
                    first_active = all(
                        variable in positions for variable in first_variables
                    )
                    second_active = all(
                        variable in positions for variable in second_variables
                    )
                    if not first_active and not second_active:
                        continue
                    if first_active != second_active:
                        return {
                            "contradiction_mode": (
                                "local_incidence_singleton_minor"
                            ),
                            "mode": mode,
                            "source_pair": (first, second),
                            "coordinate": coordinate,
                            "uses_local_incidence": True,
                        }
                    first_vector = [0] * len(variables)
                    second_vector = [0] * len(variables)
                    for variable in first_variables:
                        first_vector[positions[variable]] += 1
                    for variable in second_variables:
                        second_vector[positions[variable]] += 1
                    rows.append(
                        [
                            left - right
                            for left, right in zip(
                                first_vector, second_vector
                            )
                        ]
                    )
                    constants.append(Fraction(1))
                    records.append(
                        {
                            "kind": "local_incidence_minor",
                            "mode": mode,
                            "source_pair": (first, second),
                            "coordinate": coordinate,
                        }
                    )
    for colours, active, monomials in equation_data:
        if len(set(colours)) > 1 and len(active) == 2:
            rows.append(
                [
                    left - right
                    for left, right in zip(monomials[0], monomials[1])
                ]
            )
            constants.append(Fraction(-1))
            records.append(
                {
                    "kind": "original_binomial",
                    "colours": colours,
                    "permutations": active,
                }
            )
    if not rows:
        return (
            {
                "frontier": True,
                "variables": variables,
                "rows": [],
                "constants": [],
                "records": records,
            }
            if return_frontier
            else None
        )

    for iteration in range(len(variables) + 1):
        lattice = IntegerConstantLattice(rows, constants)
        if lattice.has_inconsistent_kernel:
            return {
                "contradiction_mode": "binomial_closure_inconsistent_sign",
                "iterations": iteration,
                "relations": len(rows),
                "rank": lattice.rank,
                "records": records,
                "uses_local_incidence": local_signatures is not None,
            }
        if local_signatures is not None:
            source_pairs = tuple(itertools.combinations(SOURCES, 2))
            for mode, signature in enumerate(local_signatures):
                local_supports, incidences = signature
                for pair_index, (first, second) in enumerate(source_pairs):
                    incidence_mask = incidences[pair_index]
                    for coordinate in COLOURS:
                        if not (
                            incidence_mask & (1 << coordinate)
                        ):
                            continue
                        coordinate_mask = 1 << coordinate
                        if (
                            local_supports[first] == coordinate_mask
                            or local_supports[second] == coordinate_mask
                        ):
                            continue
                        has_possibly_nonzero_cross_minor = False
                        cross_minor_audit = []
                        for other in COLOURS:
                            if other == coordinate:
                                continue
                            first_term = (
                                (mode, first, coordinate),
                                (mode, second, other),
                            )
                            second_term = (
                                (mode, first, other),
                                (mode, second, coordinate),
                            )
                            first_active = all(
                                variable in positions
                                for variable in first_term
                            )
                            second_active = all(
                                variable in positions
                                for variable in second_term
                            )
                            if first_active != second_active:
                                has_possibly_nonzero_cross_minor = True
                                cross_minor_audit.append(
                                    (other, "one_term_nonzero")
                                )
                                continue
                            if not first_active:
                                cross_minor_audit.append(
                                    (other, "identically_zero")
                                )
                                continue
                            first_vector = [0] * len(variables)
                            second_vector = [0] * len(variables)
                            for variable in first_term:
                                first_vector[positions[variable]] += 1
                            for variable in second_term:
                                second_vector[positions[variable]] += 1
                            difference = [
                                left - right
                                for left, right in zip(
                                    first_vector, second_vector
                                )
                            ]
                            transported = lattice.transported_constant(
                                difference
                            )
                            if transported != 1:
                                has_possibly_nonzero_cross_minor = True
                            cross_minor_audit.append(
                                (
                                    other,
                                    (
                                        "unconstrained"
                                        if transported is None
                                        else f"ratio_{transported}"
                                    ),
                                )
                            )
                        if not has_possibly_nonzero_cross_minor:
                            return {
                                "contradiction_mode": (
                                    "local_incidence_forced_rank_one"
                                ),
                                "iterations": iteration,
                                "mode": mode,
                                "source_pair": (first, second),
                                "coordinate": coordinate,
                                "cross_minor_audit": cross_minor_audit,
                                "relations": len(rows),
                                "rank": lattice.rank,
                                "records": records,
                                "uses_local_incidence": True,
                            }
                forced_zero_minors = []
                for source_triple in itertools.combinations(SOURCES, 3):
                    determinant_terms = []
                    for colour_permutation in itertools.permutations(
                        COLOURS
                    ):
                        selected = tuple(
                            (
                                mode,
                                source,
                                colour_permutation[row_index],
                            )
                            for row_index, source in enumerate(
                                source_triple
                            )
                        )
                        if not all(
                            variable in positions
                            for variable in selected
                        ):
                            continue
                        vector = [0] * len(variables)
                        for variable in selected:
                            vector[positions[variable]] += 1
                        inversions = sum(
                            colour_permutation[left]
                            > colour_permutation[right]
                            for left in range(3)
                            for right in range(left + 1, 3)
                        )
                        determinant_terms.append(
                            (
                                colour_permutation,
                                Fraction(
                                    -1 if inversions % 2 else 1
                                ),
                                vector,
                            )
                        )
                    groups: list[dict] = []
                    for permutation, sign, vector in determinant_terms:
                        placed = False
                        for group in groups:
                            difference = [
                                left - right
                                for left, right in zip(
                                    vector,
                                    group["representative_vector"],
                                )
                            ]
                            transported = (
                                lattice.transported_constant(difference)
                            )
                            if transported is None:
                                continue
                            group["coefficient"] += sign * transported
                            group["terms"].append(
                                (
                                    permutation,
                                    str(sign),
                                    str(transported),
                                )
                            )
                            placed = True
                            break
                        if not placed:
                            groups.append(
                                {
                                    "representative_vector": vector,
                                    "coefficient": sign,
                                    "terms": [
                                        (permutation, str(sign), "1")
                                    ],
                                }
                            )
                    nonzero_groups = [
                        group
                        for group in groups
                        if group["coefficient"]
                    ]
                    if nonzero_groups:
                        break
                    forced_zero_minors.append(
                        {
                            "source_triple": source_triple,
                            "terms": [
                                {
                                    "coefficient": str(
                                        group["coefficient"]
                                    ),
                                    "terms": group["terms"],
                                }
                                for group in groups
                            ],
                        }
                    )
                else:
                    return {
                        "contradiction_mode": (
                            "local_incidence_forced_rank_two"
                        ),
                        "iterations": iteration,
                        "mode": mode,
                        "forced_zero_minors": forced_zero_minors,
                        "relations": len(rows),
                        "rank": lattice.rank,
                        "records": records,
                        "uses_local_incidence": True,
                    }
        promoted = False
        for colours, active, monomials in equation_data:
            if not active:
                continue
            groups: list[dict] = []
            for permutation, vector in zip(active, monomials):
                placed = False
                for group in groups:
                    difference = [
                        left - right
                        for left, right in zip(
                            vector, group["representative_vector"]
                        )
                    ]
                    constant = lattice.transported_constant(difference)
                    if constant is None:
                        continue
                    group["coefficient"] += constant
                    group["terms"].append((permutation, str(constant)))
                    placed = True
                    break
                if not placed:
                    groups.append(
                        {
                            "representative_vector": vector,
                            "coefficient": Fraction(1),
                            "terms": [(permutation, "1")],
                        }
                    )
            nonzero = [
                group for group in groups if group["coefficient"]
            ]
            pure = len(set(colours)) == 1
            if (pure and not nonzero) or (
                not pure and len(nonzero) == 1
            ):
                return {
                    "contradiction_mode": (
                        "binomial_closure_annihilated_pure"
                        if pure
                        else "binomial_closure_isolated_class"
                    ),
                    "iterations": iteration,
                    "relations": len(rows),
                    "rank": lattice.rank,
                    "target_colours": colours,
                    "records": records,
                    "uses_local_incidence": local_signatures is not None,
                }
            if pure or len(nonzero) != 2:
                continue
            first_coefficient = Fraction(nonzero[0]["coefficient"])
            second_coefficient = Fraction(nonzero[1]["coefficient"])
            difference = [
                left - right
                for left, right in zip(
                    nonzero[0]["representative_vector"],
                    nonzero[1]["representative_vector"],
                )
            ]
            if lattice.coordinates(difference) is not None:
                continue
            rows.append(difference)
            # a M + b N = 0 gives M/N=-b/a.
            constants.append(-second_coefficient / first_coefficient)
            records.append(
                {
                    "kind": "promoted_binomial",
                    "colours": colours,
                    "coefficients": (
                        str(first_coefficient),
                        str(second_coefficient),
                    ),
                    "group_terms": (
                        nonzero[0]["terms"],
                        nonzero[1]["terms"],
                    ),
                }
            )
            promoted = True
            break
        if not promoted:
            return (
                {
                    "frontier": True,
                    "variables": variables,
                    "rows": rows,
                    "constants": [str(value) for value in constants],
                    "records": records,
                    "rank": lattice.rank,
                }
                if return_frontier
                else None
            )
    raise AssertionError("binomial closure exceeded variable rank")


def symmetry_clause_orbit(pool: IDPool, clause: list[int]) -> list[list[int]]:
    """A modest C5(mode) x C5(source) x S3(colour) clause orbit."""
    output = set()
    source_pairs = tuple(itertools.combinations(SOURCES, 2))
    source_pair_index = {
        pair: index for index, pair in enumerate(source_pairs)
    }
    for mode_shift in MODES:
        for source_shift in SOURCES:
            for colour_permutation in itertools.permutations(COLOURS):
                transformed = []
                for literal in clause:
                    key = pool.obj(abs(literal))
                    if key[0] == "x":
                        _, mode, source, colour = key
                        new_key = entry_key(
                            (mode + mode_shift) % 5,
                            (source + source_shift) % 5,
                            colour_permutation[colour],
                        )
                    else:
                        assert key[0] == "pair_incidence"
                        _, mode, pair_index, colour = key
                        shifted_pair = tuple(
                            sorted(
                                (
                                    (source_pairs[pair_index][0]
                                     + source_shift)
                                    % 5,
                                    (source_pairs[pair_index][1]
                                     + source_shift)
                                    % 5,
                                )
                            )
                        )
                        new_key = (
                            "pair_incidence",
                            (mode + mode_shift) % 5,
                            source_pair_index[shifted_pair],
                            colour_permutation[colour],
                        )
                    new_variable = pool.id(new_key)
                    transformed.append(
                        new_variable if literal > 0 else -new_variable
                    )
                output.add(tuple(sorted(transformed)))
    return [list(item) for item in sorted(output)]


def local_pattern_clause_orbit(
    pool: IDPool,
    clause: list[int],
    allowed_local_signatures: tuple[tuple, ...],
) -> list[list[int]]:
    """C5(mode) x C5(source) x S3(colour) orbit for signature clauses."""
    signature_index = {
        signature: index
        for index, signature in enumerate(allowed_local_signatures)
    }
    source_subsets = tuple(
        subset
        for size in (2, 3, 4)
        for subset in itertools.combinations(SOURCES, size)
    )
    subset_index = {
        subset: index for index, subset in enumerate(source_subsets)
    }

    def colour_mask(mask: int, permutation: tuple[int, ...]) -> int:
        return sum(
            ((mask >> colour) & 1) << permutation[colour]
            for colour in COLOURS
        )

    def transformed_signature(
        signature: tuple,
        source_shift: int,
        colour_permutation: tuple[int, ...],
    ) -> tuple:
        supports, incidences = signature
        new_supports = [0] * len(SOURCES)
        for old_source in SOURCES:
            new_source = (old_source + source_shift) % 5
            new_supports[new_source] = colour_mask(
                supports[old_source], colour_permutation
            )
        new_incidences = []
        for new_subset in source_subsets:
            old_subset = tuple(
                sorted(
                    (source - source_shift) % 5
                    for source in new_subset
                )
            )
            new_incidences.append(
                colour_mask(
                    incidences[subset_index[old_subset]],
                    colour_permutation,
                )
            )
        return tuple(new_supports), tuple(new_incidences)

    output = set()
    for mode_shift in MODES:
        for source_shift in SOURCES:
            for colour_permutation in itertools.permutations(COLOURS):
                transformed = []
                for literal in clause:
                    key = pool.obj(abs(literal))
                    assert key[0] == "local_pattern"
                    _, mode, pattern_index = key
                    new_signature = transformed_signature(
                        allowed_local_signatures[pattern_index],
                        source_shift,
                        colour_permutation,
                    )
                    new_key = (
                        "local_pattern",
                        (mode + mode_shift) % 5,
                        signature_index[new_signature],
                    )
                    new_variable = pool.id(new_key)
                    transformed.append(
                        new_variable if literal > 0 else -new_variable
                    )
                output.add(tuple(sorted(transformed)))
    return [list(item) for item in sorted(output)]


def run_singular_signature(
    signature_indices: list[int],
    output_directory: pathlib.Path,
    *,
    support_only: bool = False,
    timeout_seconds: int = 300,
    algorithm: str = "slimgb",
) -> dict:
    if timeout_seconds <= 0:
        raise ValueError("Singular timeout must be positive")
    if algorithm not in {"std", "slimgb"}:
        raise ValueError("Singular algorithm must be std or slimgb")
    slug = "_".join(map(str, signature_indices))
    prefix = "p5_support" if support_only else "p5_signature"
    source = output_directory / f"{prefix}_{algorithm}_{slug}.sing"
    log = output_directory / f"{prefix}_{algorithm}_{slug}.log"
    generator = (
        ROOT / "tmp" / "generate_p5_signature_laurent_singular.py"
    )
    output_directory.mkdir(exist_ok=True)
    try:
        command = [
            sys.executable,
            str(generator),
            "--indices",
            ",".join(map(str, signature_indices)),
            "--output",
            str(source),
            "--order",
            "dp",
            "--algorithm",
            algorithm,
        ]
        if support_only:
            command.append("--support-only")
        generated = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        return {
            "phase": "generator_timeout",
            "timeout_seconds": error.timeout,
            "source": str(source),
            "log": str(log),
            "signature_indices": signature_indices,
            "order": "dp",
            "algorithm": algorithm,
            "support_only": support_only,
            "unit_ideal": False,
        }
    if generated.returncode:
        return {
            "phase": "generator_failed",
            "returncode": generated.returncode,
            "stdout": generated.stdout.strip(),
            "stderr": generated.stderr.strip(),
            "source": str(source),
            "log": str(log),
            "signature_indices": signature_indices,
            "order": "dp",
            "algorithm": algorithm,
            "support_only": support_only,
            "unit_ideal": False,
        }
    resolved = source.resolve()
    drive = resolved.drive.rstrip(":").lower()
    wsl_path = (
        f"/mnt/{drive}/"
        + str(resolved)[len(resolved.drive) :].lstrip("\\/").replace("\\", "/")
    )
    try:
        solved = subprocess.run(
            [
                "wsl.exe",
                "--exec",
                "/usr/bin/Singular",
                "-q",
                wsl_path,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        return {
            "phase": "singular_timeout",
            "timeout_seconds": error.timeout,
            "source": str(source),
            "log": str(log),
            "signature_indices": signature_indices,
            "order": "dp",
            "algorithm": algorithm,
            "support_only": support_only,
            "unit_ideal": False,
        }
    log.write_text(solved.stdout, encoding="utf-8")
    return {
        "returncode": solved.returncode,
        "stdout": solved.stdout.strip(),
        "stderr": solved.stderr.strip(),
        "source": str(source),
        "log": str(log),
        "signature_indices": signature_indices,
        "order": "dp",
        "algorithm": algorithm,
        "support_only": support_only,
        "unit_ideal": (
            solved.returncode == 0
            and solved.stderr == ""
            and "UNIT_IDEAL" in solved.stdout
        ),
    }


def run_singular_abstract_signature(
    supports: tuple[tuple[int, ...], ...],
    pair_incidences: list[tuple[int, ...]],
    output_directory: pathlib.Path,
) -> dict:
    descriptor_payload = {
        "supports": supports,
        "pair_incidences": pair_incidences,
    }
    canonical = json.dumps(
        descriptor_payload, sort_keys=True, separators=(",", ":")
    )
    slug = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
    descriptor = output_directory / f"p5_abstract_{slug}.json"
    source = output_directory / f"p5_abstract_{slug}.sing"
    log = output_directory / f"p5_abstract_{slug}.log"
    generator = (
        ROOT / "tmp" / "generate_p5_signature_laurent_singular.py"
    )
    output_directory.mkdir(exist_ok=True)
    descriptor.write_text(
        json.dumps(descriptor_payload, indent=2) + "\n",
        encoding="utf-8",
    )
    try:
        generated = subprocess.run(
            [
                sys.executable,
                str(generator),
                "--descriptor",
                str(descriptor),
                "--output",
                str(source),
                "--order",
                "dp",
                "--algorithm",
                "slimgb",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        return {
            "phase": "generator_timeout",
            "timeout_seconds": error.timeout,
            "source": str(source),
            "log": str(log),
            "descriptor": str(descriptor),
            "descriptor_sha256": hashlib.sha256(
                descriptor.read_bytes()
            ).hexdigest(),
            "order": "dp",
            "algorithm": "slimgb",
            "unit_ideal": False,
        }
    if generated.returncode:
        raise RuntimeError(
            f"abstract Singular generator failed: {generated.stderr}"
        )
    resolved = source.resolve()
    drive = resolved.drive.rstrip(":").lower()
    wsl_path = (
        f"/mnt/{drive}/"
        + str(resolved)[len(resolved.drive) :].lstrip("\\/").replace("\\", "/")
    )
    try:
        solved = subprocess.run(
            [
                "wsl.exe",
                "--exec",
                "/usr/bin/Singular",
                "-q",
                wsl_path,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        return {
            "phase": "singular_timeout",
            "timeout_seconds": error.timeout,
            "source": str(source),
            "log": str(log),
            "descriptor": str(descriptor),
            "descriptor_sha256": hashlib.sha256(
                descriptor.read_bytes()
            ).hexdigest(),
            "order": "dp",
            "algorithm": "slimgb",
            "unit_ideal": False,
        }
    log.write_text(solved.stdout, encoding="utf-8")
    return {
        "returncode": solved.returncode,
        "stdout": solved.stdout.strip(),
        "stderr": solved.stderr.strip(),
        "source": str(source),
        "log": str(log),
        "descriptor": str(descriptor),
        "descriptor_sha256": hashlib.sha256(
            descriptor.read_bytes()
        ).hexdigest(),
        "order": "dp",
        "algorithm": "slimgb",
        "unit_ideal": (
            solved.returncode == 0
            and solved.stderr == ""
            and "UNIT_IDEAL" in solved.stdout
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=int, default=20)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--local-f5", action="store_true")
    parser.add_argument("--state", type=pathlib.Path)
    parser.add_argument("--symmetry-orbits", action="store_true")
    parser.add_argument("--double-lex", action="store_true")
    parser.add_argument("--hall-hierarchy", action="store_true")
    parser.add_argument("--pair-hierarchy", action="store_true")
    parser.add_argument("--abstract-pairs", action="store_true")
    parser.add_argument("--singular", action="store_true")
    args = parser.parse_args()
    if args.abstract_pairs and args.local_f5:
        raise ValueError("--abstract-pairs and --local-f5 are alternatives")
    if args.hall_hierarchy and args.pair_hierarchy:
        raise ValueError(
            "--hall-hierarchy and --pair-hierarchy are alternatives"
        )
    allowed = finite_field_local_signatures() if args.local_f5 else None
    if (args.hall_hierarchy or args.pair_hierarchy) and allowed is None:
        raise ValueError(
            "--hall-hierarchy/--pair-hierarchy requires --local-f5"
        )
    cnf, pool = build_cnf(
        allowed,
        double_lex=args.double_lex,
        hall_hierarchy=args.hall_hierarchy,
        pair_hierarchy=args.pair_hierarchy,
        abstract_pairs=args.abstract_pairs,
    )
    learned_records = []
    if args.state is not None and args.state.exists():
        raw_state = json.loads(args.state.read_text(encoding="utf-8"))
        learned_records = list(raw_state.get("learned_records", []))
        for record in learned_records:
            clause = list(map(int, record["clause"]))
            entry_or_pair_clause = all(
                pool.obj(abs(literal))[0] in ("x", "pair_incidence")
                for literal in clause
            )
            local_pattern_clause = (
                allowed is not None
                and all(
                    pool.obj(abs(literal))[0] == "local_pattern"
                    for literal in clause
                )
            )
            if args.symmetry_orbits and entry_or_pair_clause:
                cnf.extend(symmetry_clause_orbit(pool, clause))
            elif args.symmetry_orbits and local_pattern_clause:
                cnf.extend(
                    local_pattern_clause_orbit(pool, clause, allowed)
                )
            else:
                cnf.append(clause)
    print(
        json.dumps(
            {
                "variables": pool.top,
                "clauses": len(cnf.clauses),
                "mixed_tuples": len(MIXED),
                "allowed_local_signatures": (
                    None if allowed is None else len(allowed)
                ),
                "preloaded_learned_clauses": len(learned_records),
                "symmetry_orbits": args.symmetry_orbits,
                "double_lex": args.double_lex,
                "hall_hierarchy": args.hall_hierarchy,
                "pair_hierarchy": args.pair_hierarchy,
                "abstract_pairs": args.abstract_pairs,
            }
        ),
        flush=True,
    )
    with Solver(name="cadical195", bootstrap_with=cnf.clauses) as solver:
        for model_index in range(args.models):
            if not solver.solve():
                print(json.dumps({"status": "UNSAT", "after_models": model_index}))
                if args.state is not None:
                    args.state.write_text(
                        json.dumps(
                            {
                                "status": "UNSAT",
                                "learned_records": learned_records,
                            },
                            indent=2,
                        )
                        + "\n",
                        encoding="utf-8",
                    )
                return
            model = solver.get_model()
            supports = supports_from_model(pool, model)
            selected_signature_indices: list[int] = []
            selected_signatures: list[tuple] = []
            if allowed is not None:
                positive_model = {value for value in model if value > 0}
                for mode in MODES:
                    candidates = [
                        pattern_index
                        for pattern_index in range(len(allowed))
                        if pool.id(
                            ("local_pattern", mode, pattern_index)
                        )
                        in positive_model
                    ]
                    assert candidates
                    selected_signature_indices.append(candidates[0])
                    selected_signatures.append(allowed[candidates[0]])
            selected_pair_incidences: list[tuple[int, ...]] = []
            if args.abstract_pairs:
                positive_model = {value for value in model if value > 0}
                source_pairs = tuple(
                    itertools.combinations(SOURCES, 2)
                )
                for mode in MODES:
                    incidences = tuple(
                        sum(
                            (
                                pool.id(
                                    (
                                        "pair_incidence",
                                        mode,
                                        pair_index,
                                        colour,
                                    )
                                )
                                in positive_model
                            )
                            << colour
                            for colour in COLOURS
                        )
                        for pair_index, _pair in enumerate(source_pairs)
                    )
                    selected_pair_incidences.append(incidences)
                    selected_signatures.append(
                        (supports[mode], incidences)
                    )
            lattice = signed_lattice_result(supports)
            collision = (
                None
                if lattice["inconsistent"]
                else residual_collision_result(supports)
            )
            factored_collision = (
                None
                if lattice["inconsistent"] or collision is not None
                else factored_residual_collision_result(supports)
            )
            if factored_collision is not None:
                collision = factored_collision
            closure = (
                None
                if lattice["inconsistent"] or collision is not None
                else binomial_closure_result(
                    supports,
                    (
                        tuple(selected_signatures)
                        if selected_signatures
                        else None
                    ),
                )
            )
            if closure is not None:
                lattice = {
                    **lattice,
                    "inconsistent": True,
                    "contradiction_mode": closure["contradiction_mode"],
                    "certificate": closure,
                }
            if collision is not None:
                lattice = {
                    **lattice,
                    "inconsistent": True,
                    "contradiction_mode": collision[
                        "contradiction_mode"
                    ],
                    "certificate": collision,
                }
            if not lattice["inconsistent"] and args.singular:
                if args.abstract_pairs:
                    singular = run_singular_abstract_signature(
                        supports,
                        selected_pair_incidences,
                        ROOT / "tmp",
                    )
                elif selected_signature_indices:
                    singular = run_singular_signature(
                        selected_signature_indices, ROOT / "tmp"
                    )
                else:
                    raise RuntimeError(
                        "--singular requires --local-f5 or --abstract-pairs"
                    )
                if singular["unit_ideal"]:
                    lattice = {
                        **lattice,
                        "inconsistent": True,
                        "contradiction_mode": "singular_unit_ideal",
                        "certificate": singular,
                    }
                else:
                    print(
                        json.dumps(
                            {
                                "singular_survivor": singular,
                                "supports": supports,
                                "selected_signature_indices": (
                                    selected_signature_indices
                                ),
                            }
                        ),
                        flush=True,
                    )
            if args.verbose or not lattice["inconsistent"]:
                print(
                    json.dumps(
                        {
                            "model": model_index,
                            "supports": supports,
                            "nonzero_entries": sum(
                                mask.bit_count()
                                for local in supports
                                for mask in local
                            ),
                            "coordinate_rows": sum(
                                mask in (1, 2, 4)
                                for local in supports
                                for mask in local
                            ),
                            "selected_signature_indices": (
                                selected_signature_indices
                            ),
                            "selected_local_incidences": [
                                signature[1]
                                for signature in selected_signatures
                            ],
                            "selected_pair_incidences": (
                                selected_pair_incidences
                            ),
                            "lattice": lattice,
                        }
                    ),
                    flush=True,
                )
            if not lattice["inconsistent"]:
                print("signed-lattice survivor", flush=True)
                return
            if lattice["contradiction_mode"] == "residual_permanent_collision":
                clause, positive_count, negative_count = (
                    residual_collision_clause(pool, lattice["certificate"])
                )
            elif lattice["contradiction_mode"] == (
                "factored_residual_permanent_collision"
            ):
                clause, positive_count, negative_count = (
                    factored_residual_collision_clause(
                        pool, supports, lattice["certificate"]
                    )
                )
            elif lattice["contradiction_mode"].startswith(
                ("binomial_closure_", "local_incidence_")
            ):
                if lattice["certificate"].get(
                    "uses_local_incidence", False
                ):
                    if args.abstract_pairs:
                        clause = exact_support_clause(pool, supports)
                        clause.extend(
                            -pool.id(
                                (
                                    "pair_incidence",
                                    mode,
                                    pair_index,
                                    colour,
                                )
                            )
                            for mode, incidences in enumerate(
                                selected_pair_incidences
                            )
                            for pair_index, mask in enumerate(incidences)
                            for colour in COLOURS
                            if mask & (1 << colour)
                        )
                    else:
                        clause = [
                            -pool.id(
                                (
                                    "local_pattern",
                                    mode,
                                    pattern_index,
                                )
                            )
                            for mode, pattern_index in zip(
                                MODES, selected_signature_indices
                            )
                        ]
                else:
                    clause = exact_support_clause(pool, supports)
                positive_count = sum(literal < 0 for literal in clause)
                negative_count = sum(literal > 0 for literal in clause)
            elif lattice["contradiction_mode"] == "singular_unit_ideal":
                if args.abstract_pairs:
                    clause = exact_support_clause(pool, supports)
                    clause.extend(
                        -pool.id(
                            (
                                "pair_incidence",
                                mode,
                                pair_index,
                                colour,
                            )
                        )
                        for mode, incidences in enumerate(
                            selected_pair_incidences
                        )
                        for pair_index, mask in enumerate(incidences)
                        for colour in COLOURS
                        if mask & (1 << colour)
                    )
                else:
                    clause = [
                        -pool.id(
                            (
                                "local_pattern",
                                mode,
                                pattern_index,
                            )
                        )
                        for mode, pattern_index in zip(
                            MODES, selected_signature_indices
                        )
                    ]
                positive_count = len(clause)
                negative_count = 0
            else:
                clause, positive_count, negative_count = (
                    conflict_cube_clause(pool, supports, lattice)
                )
            entry_or_pair_clause = all(
                pool.obj(abs(literal))[0] in ("x", "pair_incidence")
                for literal in clause
            )
            local_pattern_clause = (
                allowed is not None
                and all(
                    pool.obj(abs(literal))[0] == "local_pattern"
                    for literal in clause
                )
            )
            if args.symmetry_orbits and entry_or_pair_clause:
                clauses_to_add = symmetry_clause_orbit(pool, clause)
            elif args.symmetry_orbits and local_pattern_clause:
                clauses_to_add = local_pattern_clause_orbit(
                    pool, clause, allowed
                )
            else:
                clauses_to_add = [clause]
            for learned_clause in clauses_to_add:
                solver.add_clause(learned_clause)
            learned_records.append(
                {
                    "clause": clause,
                    "supports": supports,
                    "contradiction_mode": lattice[
                        "contradiction_mode"
                    ],
                    "certificate": lattice["certificate"],
                }
            )
            if args.state is not None and (
                len(learned_records) % 10 == 0
            ):
                args.state.parent.mkdir(exist_ok=True)
                args.state.write_text(
                    json.dumps(
                        {
                            "status": "IN_PROGRESS",
                            "learned_records": learned_records,
                        },
                        indent=2,
                    )
                    + "\n",
                    encoding="utf-8",
                )
            if model_index % 100 == 99:
                print(
                    json.dumps(
                        {
                            "learned": model_index + 1,
                            "last_cube_positive": positive_count,
                            "last_cube_negative": negative_count,
                            "last_clause_length": len(clause),
                        }
                    ),
                    flush=True,
                )
    if args.state is not None:
        args.state.parent.mkdir(exist_ok=True)
        args.state.write_text(
            json.dumps(
                {
                    "status": "IN_PROGRESS",
                    "learned_records": learned_records,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    print(
        f"model limit reached total_learned={len(learned_records)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
