"""Necessary support-level SAT test for a forced killer-edge pattern.

An edge entry is represented by a Boolean saying whether its complex weight
is nonzero.  A matching monomial is nonzero exactly when its three entries
are nonzero.  Hence:

* a monochromatic amplitude must contain a nonzero matching monomial;
* a forbidden amplitude cannot contain exactly one nonzero monomial.

The resulting CNF is only a necessary condition for the polynomial system,
but UNSAT is an exact impossibility certificate over every field.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from killer_pattern_certificates import pattern_arcs
from search_killer_patterns import Pattern, active_mask_for_pattern
from search_witness import EquationSystem

Edge = tuple[int, int]
Clause = tuple[int, ...]


@dataclass
class CNF:
    variable_count: int = 0
    clauses: list[Clause] = field(default_factory=list)

    def variable(self) -> int:
        self.variable_count += 1
        return self.variable_count

    def add(self, *literals: int) -> None:
        self.clauses.append(tuple(literals))

    def write_dimacs(self, path: Path) -> None:
        lines = [f"p cnf {self.variable_count} {len(self.clauses)}"]
        lines.extend(
            " ".join(str(literal) for literal in clause) + " 0"
            for clause in self.clauses
        )
        path.write_text("\n".join(lines) + "\n", encoding="ascii")


def matching_indicator(cnf: CNF, factors: tuple[int, ...]) -> int:
    indicator = cnf.variable()
    for factor in factors:
        cnf.add(-indicator, factor)
    cnf.add(indicator, *(-factor for factor in factors))
    return indicator


def support_cnf(
    system: EquationSystem,
    pattern: Pattern,
    forced_nonzero_edges: set[Edge],
    forced_zero_entries: set[int] | None = None,
    forced_nonzero_entries: set[int] | None = None,
    rectangular_support_edges: set[Edge] | None = None,
    colouring_selectors: dict[int, int] | None = None,
) -> CNF:
    """Build the amplitude-support relaxation, with optional rank-one support.

    ``rectangular_support_edges`` imposes the zero/nonzero support condition
    of a matrix of rank at most one.  Its nonzero entries must form a
    Cartesian product of a set of rows and a set of columns (or be empty).
    """
    active = active_mask_for_pattern(system, pattern)
    cnf = CNF()
    entry_variables = {
        int(index): cnf.variable() for index in np.flatnonzero(active)
    }
    forced_zero_entries = forced_zero_entries or set()
    forced_nonzero_entries = forced_nonzero_entries or set()
    rectangular_support_edges = rectangular_support_edges or set()

    overlap = forced_zero_entries & forced_nonzero_entries
    if overlap:
        raise ValueError(
            f"entries cannot be both forced zero and nonzero: {sorted(overlap)}"
        )
    for flat_index in sorted(forced_zero_entries):
        variable = entry_variables.get(flat_index)
        if variable is not None:
            cnf.add(-variable)
    for flat_index in sorted(forced_nonzero_entries):
        variable = entry_variables.get(flat_index)
        if variable is None:
            cnf.add()
        else:
            cnf.add(variable)

    for edge in sorted(rectangular_support_edges):
        edge_index = system.edge_index[edge]

        def entry(row: int, column: int) -> int | None:
            return entry_variables.get(
                edge_index * system.d * system.d
                + row * system.d
                + column
            )

        for first_row in range(system.d):
            for second_row in range(first_row + 1, system.d):
                for first_column in range(system.d):
                    for second_column in range(first_column + 1, system.d):
                        diagonal = (
                            entry(first_row, first_column),
                            entry(second_row, second_column),
                        )
                        cross = (
                            entry(first_row, second_column),
                            entry(second_row, first_column),
                        )
                        for antecedent, consequent in (
                            (diagonal, cross),
                            (cross, diagonal),
                        ):
                            if None in antecedent:
                                continue
                            for required in consequent:
                                if required is None:
                                    cnf.add(
                                        -antecedent[0],
                                        -antecedent[1],
                                    )
                                else:
                                    cnf.add(
                                        -antecedent[0],
                                        -antecedent[1],
                                        required,
                                    )

    # Every selected killer-edge block is nonzero.  A mutual killer edge has
    # one structurally active entry; an unpaired killer edge has one active
    # row or column, and at least one of those three entries must be nonzero.
    for edge in forced_nonzero_edges:
        edge_index = system.edge_index[edge]
        start = edge_index * system.d * system.d
        active_entries = [
            index
            for index in range(start, start + system.d * system.d)
            if active[index]
        ]
        if not active_entries:
            raise ValueError(
                f"forced edge {edge} has no active entries"
            )
        cnf.add(*(entry_variables[index] for index in active_entries))

    for colouring_index, raw_colouring in enumerate(system.colourings):
        colouring = tuple(int(value) for value in raw_colouring)
        selector = None
        if colouring_selectors is not None:
            selector = cnf.variable()
            colouring_selectors[colouring_index] = selector

        def add_amplitude_clause(*literals: int) -> None:
            if selector is None:
                cnf.add(*literals)
            else:
                cnf.add(-selector, *literals)

        indicators: list[int] = []
        for matching in system.matchings:
            factors: list[int] = []
            for edge in matching:
                flat_index = (
                    system.edge_index[edge] * system.d * system.d
                    + colouring[edge[0]] * system.d
                    + colouring[edge[1]]
                )
                variable = entry_variables.get(flat_index)
                if variable is None:
                    break
                factors.append(variable)
            else:
                indicators.append(
                    matching_indicator(cnf, tuple(factors))
                )

        if system.target[colouring_index]:
            add_amplitude_clause(*indicators)
        else:
            # Forbid exactly one true indicator.  Zero or at least two are
            # the only supports on which a sum can vanish.
            for indicator in indicators:
                add_amplitude_clause(
                    -indicator,
                    *(other for other in indicators if other != indicator),
                )
    return cnf


def windows_to_wsl(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    suffix = resolved.as_posix().split(":", 1)[1]
    return f"/mnt/{drive}{suffix}"


def solve_with_minisat(cnf: CNF, path: Path) -> str:
    cnf.write_dimacs(path)
    result_path = path.with_suffix(".result")
    completed = subprocess.run(
        [
            "wsl",
            "-d",
            "Ubuntu",
            "--",
            "minisat",
            "-verb=0",
            windows_to_wsl(path),
            windows_to_wsl(result_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode == 10:
        return "SAT"
    if completed.returncode == 20:
        return "UNSAT"
    raise RuntimeError(
        f"MiniSat failed with {completed.returncode}: "
        f"{completed.stdout}\n{completed.stderr}"
    )


def solve_with_cadical(cnf: CNF, path: Path) -> str:
    cnf.write_dimacs(path)
    completed = subprocess.run(
        [
            "wsl",
            "-d",
            "Ubuntu",
            "--",
            "cadical",
            "--quiet",
            "--no-witness",
            windows_to_wsl(path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode == 10:
        return "SAT"
    if completed.returncode == 20:
        return "UNSAT"
    raise RuntimeError(
        f"CaDiCaL failed with {completed.returncode}: "
        f"{completed.stdout}\n{completed.stderr}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern", type=Path)
    parser.add_argument("--cnf", type=Path, default=Path("tmp/support.cnf"))
    args = parser.parse_args()

    payload = json.loads(args.pattern.read_text(encoding="utf-8"))
    pattern = payload.get("pattern", payload)
    system = EquationSystem(6, 3)
    forced_edges = {
        edge
        for edge, arcs in pattern_arcs(pattern).items()
        if len(arcs) == 2
    }
    args.cnf.parent.mkdir(parents=True, exist_ok=True)
    cnf = support_cnf(system, pattern, forced_edges)
    status = solve_with_minisat(cnf, args.cnf)
    print(
        json.dumps(
            {
                "status": status,
                "variables": cnf.variable_count,
                "clauses": len(cnf.clauses),
                "forced_edges": len(forced_edges),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
