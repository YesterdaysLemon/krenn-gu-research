"""Independently replay a pure-deleted-tensor support CNF extension."""

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


import argparse
import hashlib
import itertools
import json
from pathlib import Path


Edge = tuple[int, int]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        prefix, kind, variables, clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise AssertionError("invalid DIMACS header")
    return int(variables), int(clauses)


def allowed_edges() -> tuple[Edge, ...]:
    return tuple(
        (first, second)
        for first in range(8)
        for second in range(first + 1, 8)
        if first != 0 or second <= 3
    )


def entry(
    first: int,
    second: int,
    first_colour: int,
    second_colour: int,
) -> int:
    if first < second:
        edge = (first, second)
        row, column = first_colour, second_colour
    else:
        edge = (second, first)
        row, column = second_colour, first_colour
    return 1 + 9 * allowed_edges().index(edge) + 3 * row + column


def matchings(vertices: tuple[int, ...]) -> tuple[tuple[Edge, ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    allowed = set(allowed_edges())
    result: list[tuple[Edge, ...]] = []
    for partner_index, partner in enumerate(vertices[1:], start=1):
        edge = (min(first, partner), max(first, partner))
        if edge not in allowed:
            continue
        rest = vertices[1:partner_index] + vertices[partner_index + 1 :]
        for smaller in matchings(rest):
            result.append((edge, *smaller))
    return tuple(result)


def expected_conditions(
    stars: list[dict[str, object]],
) -> list[tuple[tuple[int, ...], int]]:
    result: list[tuple[tuple[int, ...], int]] = []
    seen: set[tuple[tuple[int, ...], int]] = set()
    for star in stars:
        center = int(star["center"])
        neighbours = tuple(map(int, star["colour_neighbours"]))
        if (
            not 0 <= center < 8
            or len(neighbours) != 3
            or center in neighbours
            or len(set(neighbours)) != 3
            or any(not 0 <= neighbour < 8 for neighbour in neighbours)
        ):
            raise AssertionError("malformed star manifest")
        for colour, neighbour in enumerate(neighbours):
            vertices = tuple(
                value
                for value in range(8)
                if value not in {center, neighbour}
            )
            key = (vertices, colour)
            if key not in seen:
                seen.add(key)
                result.append(key)
    return result


def replay(
    old_variables: int,
    conditions: list[tuple[tuple[int, ...], int]],
) -> tuple[list[tuple[int, ...]], list[dict[str, object]], int]:
    next_variable = old_variables + 1
    indicator_for: dict[tuple[int, ...], int] = {}
    clauses: list[tuple[int, ...]] = []
    rows: list[dict[str, object]] = []
    for vertices, target_colour in conditions:
        local_matchings = matchings(vertices)
        required_rows = 0
        forbidden_rows = 0
        for colouring in itertools.product((0, 1, 2), repeat=len(vertices)):
            colours = dict(zip(vertices, colouring, strict=True))
            indicators: list[int] = []
            for matching in local_matchings:
                factors = tuple(
                    sorted(
                        entry(
                            first,
                            second,
                            colours[first],
                            colours[second],
                        )
                        for first, second in matching
                    )
                )
                if factors not in indicator_for:
                    indicator_for[factors] = next_variable
                    for factor in factors:
                        clauses.append((-next_variable, factor))
                    clauses.append(
                        (next_variable, *(-factor for factor in factors))
                    )
                    next_variable += 1
                indicators.append(indicator_for[factors])
            if all(value == target_colour for value in colouring):
                clauses.append(tuple(indicators))
                required_rows += 1
            else:
                for index, indicator in enumerate(indicators):
                    clauses.append(
                        (
                            -indicator,
                            *(
                                other
                                for other_index, other in enumerate(indicators)
                                if other_index != index
                            ),
                        )
                    )
                forbidden_rows += 1
        rows.append(
            {
                "vertices": list(vertices),
                "target_colour": target_colour,
                "perfect_matchings": len(local_matchings),
                "colourings": 3 ** len(vertices),
                "required_rows": required_rows,
                "forbidden_rows": forbidden_rows,
            }
        )
    return clauses, rows, next_variable - 1


def parse_clause(line: str) -> tuple[int, ...]:
    values = tuple(map(int, line.split()))
    if not values or values[-1] != 0:
        raise AssertionError("unterminated DIMACS clause")
    return values[:-1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    base = Path(manifest["base_cnf"])
    output = Path(manifest["output_cnf"])
    if sha256(base) != manifest["base_cnf_sha256"]:
        raise AssertionError("base CNF hash mismatch")
    if sha256(output) != manifest["output_cnf_sha256"]:
        raise AssertionError("output CNF hash mismatch")

    old_variables, old_clauses = header(base)
    conditions = expected_conditions(manifest["stars"])
    expected_tail, expected_rows, expected_variables = replay(
        old_variables, conditions
    )
    new_variables, new_clauses = header(output)
    if new_variables != expected_variables:
        raise AssertionError("new variable count mismatch")
    if new_clauses != old_clauses + len(expected_tail):
        raise AssertionError("new clause count mismatch")
    if manifest["rows"] != expected_rows:
        raise AssertionError("pure-tensor row manifest mismatch")

    with base.open("r", encoding="ascii") as base_handle, output.open(
        "r", encoding="ascii"
    ) as output_handle:
        next(base_handle)
        next(output_handle)
        for line_number, base_line in enumerate(base_handle, start=2):
            if output_handle.readline() != base_line:
                raise AssertionError(
                    f"base prefix changed at line {line_number}"
                )
        for index, expected in enumerate(expected_tail):
            observed_line = output_handle.readline()
            if not observed_line:
                raise AssertionError(f"missing tail clause {index}")
            if parse_clause(observed_line) != expected:
                raise AssertionError(f"tail clause mismatch at index {index}")
        if output_handle.readline():
            raise AssertionError("unexpected extra output clauses")

    payload = {
        "verified": True,
        "manifest": str(args.manifest),
        "base_cnf_sha256": sha256(base),
        "output_cnf_sha256": sha256(output),
        "stars": len(manifest["stars"]),
        "pure_tensors": len(conditions),
        "monomial_indicators": expected_variables - old_variables,
        "appended_clauses": len(expected_tail),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
