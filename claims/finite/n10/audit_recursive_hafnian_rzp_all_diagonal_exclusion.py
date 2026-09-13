"""Independent no-import audit of the n=10 RZP cover and frozen CNFs.

This file deliberately imports neither ``krenn_gu`` nor ``python-sat``.  It
reconstructs variable allocation, clauses, DIMACS bytes, matching orbits, and
explicit stabilizer transporters with the Python standard library, then checks
the frozen CNF/proof identities in the evidence manifest.  DRAT proof checking
remains the separate primary replay step.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


CYCLE_TYPES = (
    (5,),
    (4, 1),
    (3, 2),
    (3, 1, 1),
    (2, 2, 1),
    (2, 1, 1, 1),
    (1, 1, 1, 1, 1),
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def identity(path):
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            size += len(chunk)
            digest.update(chunk)
    return {"bytes": size, "sha256": digest.hexdigest()}


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(remainder):
            yield ((first, second), *matching)


def canonical_pair(n, cycle_type):
    require(sum(cycle_type) == n // 2, "cycle type does not partition n/2")
    first = tuple((vertex, vertex + 1) for vertex in range(0, n, 2))
    second = []
    offset = 0
    for part in cycle_type:
        atoms = tuple(range(offset, offset + part))
        if part == 1:
            second.append((2 * atoms[0], 2 * atoms[0] + 1))
        else:
            for position, atom in enumerate(atoms):
                successor = atoms[(position + 1) % part]
                second.append(tuple(sorted((2 * atom + 1, 2 * successor))))
        offset += part
    return first, tuple(sorted(second))


def partner_map(matching):
    result = {}
    for first, second in matching:
        result[first] = second
        result[second] = first
    return result


def alternating_cycle_type(first, second):
    partners = partner_map(first), partner_map(second)
    unvisited = set(partners[0])
    parts = []
    while unvisited:
        start = min(unvisited)
        current = start
        colour = 0
        component = set()
        while True:
            component.add(current)
            current = partners[colour][current]
            colour = 1 - colour
            if current == start and colour == 0:
                break
        unvisited -= component
        parts.append(len(component) // 2)
    return tuple(sorted(parts, reverse=True))


def stabilizer_transporter(first, second):
    partners = partner_map(first), partner_map(second)
    unseen = set(partners[0])
    walks = []
    while unseen:
        start = min(unseen)
        current = start
        walk = []
        while True:
            other = partners[0][current]
            walk.extend((current, other))
            unseen.difference_update((current, other))
            current = partners[1][other]
            if current == start:
                break
        walks.append(tuple(walk))
    walks.sort(key=lambda walk: (-len(walk), walk))
    return {
        vertex: image
        for image, vertex in enumerate(itertools.chain.from_iterable(walks))
    }


def image_matching(matching, transporter):
    return tuple(
        sorted(
            tuple(sorted((transporter[first], transporter[second])))
            for first, second in matching
        )
    )


def expected_cases():
    expected = {}
    for cycle_type in CYCLE_TYPES[:-1]:
        label = "p".join(map(str, cycle_type))
        expected[f"top-{label}"] = {
            "n": 10,
            "matching_cycle_type": list(cycle_type),
            "third_matching_cycle_type": None,
            "two_part_only": False,
            "no_singleton_cancellation": False,
        }
    shared = list(CYCLE_TYPES[-1])
    for cycle_type in CYCLE_TYPES:
        label = "shared" if cycle_type == CYCLE_TYPES[-1] else "p".join(map(str, cycle_type))
        expected[f"shared-third-{label}"] = {
            "n": 10,
            "matching_cycle_type": shared,
            "third_matching_cycle_type": list(cycle_type),
            "two_part_only": False,
            "no_singleton_cancellation": False,
        }
    return expected


class IndependentEncoder:
    def __init__(self, n, matching_cycle_type, third_matching_cycle_type):
        self.n = n
        self.next_variable = 1
        self.clauses = []
        vertices = tuple(range(n))
        pairs = tuple(itertools.combinations(vertices, 2))
        self.even_sets = tuple(
            tuple(subset)
            for size in range(4, n + 1, 2)
            for subset in itertools.combinations(vertices, size)
        )
        self.edges = {
            (colour, edge): self.variable()
            for colour in range(3)
            for edge in pairs
        }
        self.hafnians = {
            (colour, subset): self.variable()
            for colour in range(3)
            for subset in self.even_sets
        }
        self.products = {
            (colour, subset, edge): self.variable()
            for colour in range(3)
            for subset in self.even_sets
            for edge in itertools.combinations(subset, 2)
        }
        self.add_recursive_clauses()
        whole = vertices
        for colour in range(3):
            self.clauses.append((self.hafnians[(colour, whole)],))
        if matching_cycle_type is not None:
            first, second = canonical_pair(n, matching_cycle_type)
            self.clauses.extend((self.edges[(0, edge)],) for edge in first)
            self.clauses.extend((self.edges[(1, edge)],) for edge in second)
        if third_matching_cycle_type is not None:
            require(
                tuple(matching_cycle_type) == (1,) * (n // 2),
                "third matching normalization used outside shared case",
            )
            _first, third = canonical_pair(n, third_matching_cycle_type)
            self.clauses.extend((self.edges[(2, edge)],) for edge in third)
        self.add_rainbow_clauses()

    def variable(self):
        result = self.next_variable
        self.next_variable += 1
        return result

    def hafnian_literal(self, colour, subset):
        subset = tuple(sorted(subset))
        if not subset:
            return None
        if len(subset) == 2:
            return self.edges[(colour, subset)]
        return self.hafnians[(colour, subset)]

    def add_recursive_clauses(self):
        for colour in range(3):
            for subset in self.even_sets:
                result = self.hafnians[(colour, subset)]
                incident = {vertex: [] for vertex in subset}
                for edge in itertools.combinations(subset, 2):
                    product = self.products[(colour, subset, edge)]
                    edge_literal = self.edges[(colour, edge)]
                    remainder = tuple(vertex for vertex in subset if vertex not in edge)
                    cofactor = self.hafnian_literal(colour, remainder)
                    require(cofactor is not None, "product has an empty cofactor")
                    self.clauses.extend(
                        (
                            (-product, edge_literal),
                            (-product, cofactor),
                            (product, -edge_literal, -cofactor),
                        )
                    )
                    incident[edge[0]].append(product)
                    incident[edge[1]].append(product)
                for vertex in subset:
                    terms = incident[vertex]
                    self.clauses.append((-result, *terms))
                    for position, product in enumerate(terms):
                        others = terms[:position] + terms[position + 1 :]
                        self.clauses.append((-product, result, *others))

    def add_rainbow_clauses(self):
        vertices = tuple(range(self.n))
        for word in itertools.product(range(3), repeat=self.n):
            classes = tuple(
                tuple(
                    vertex
                    for vertex, assigned in zip(vertices, word, strict=True)
                    if assigned == colour
                )
                for colour in range(3)
            )
            if not all(len(part) % 2 == 0 for part in classes):
                continue
            if sum(bool(part) for part in classes) < 2:
                continue
            clause = tuple(
                -literal
                for colour, part in enumerate(classes)
                if (literal := self.hafnian_literal(colour, part)) is not None
            )
            self.clauses.append(clause)

    def dimacs_bytes(self):
        lines = [f"p cnf {self.next_variable - 1} {len(self.clauses)}"]
        lines.extend(" ".join(map(str, (*clause, 0))) for clause in self.clauses)
        return ("\r\n".join(lines) + "\r\n").encode("ascii")


def audit_local_semantics():
    def product_rows(product, edge, cofactor):
        return (
            (not product or edge)
            and (not product or cofactor)
            and (product or not edge or not cofactor)
        )

    for values in itertools.product((False, True), repeat=3):
        require(product_rows(*values) == (values[0] == (values[1] and values[2])), "bad product equivalence")
    checked = 0
    for term_count in range(2, 10):
        for result in (False, True):
            for terms in itertools.product((False, True), repeat=term_count):
                clauses = (not result or any(terms)) and all(
                    not term or result or any(terms[:position] + terms[position + 1 :])
                    for position, term in enumerate(terms)
                )
                semantic = (not result or any(terms)) and (result or sum(terms) != 1)
                require(clauses == semantic, "Laplace support clauses changed meaning")
                checked += 1
    return checked


def audit_cover(case_specs):
    expected = expected_cases()
    actual = {case["id"]: case["parameters"] for case in case_specs}
    require(actual == expected, "manifest is not the exact 13-case cover")
    fixed, _other = canonical_pair(10, (5,))
    observed = set()
    count = 0
    for matching in perfect_matchings(tuple(range(10))):
        cycle_type = alternating_cycle_type(fixed, matching)
        observed.add(cycle_type)
        transporter = stabilizer_transporter(fixed, matching)
        canonical_first, canonical_second = canonical_pair(10, cycle_type)
        require(image_matching(fixed, transporter) == canonical_first, "first matching transport failed")
        require(image_matching(matching, transporter) == canonical_second, "second matching transport failed")
        count += 1
    require(count == 945 and observed == set(CYCLE_TYPES), "matching cover is incomplete")
    return {"perfect_matchings": count, "cycle_types": [list(row) for row in sorted(observed, reverse=True)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    require(manifest.get("schema") == "recursive-hafnian-rzp-drat-v2", "wrong manifest schema")
    require(args.artifact_dir.is_dir(), "artifact directory is missing")
    report = {
        "schema": "recursive-hafnian-rzp-independent-audit-v1",
        "status": "HOLD",
        "scope": "independent cover, encoder, CNF identity, and proof-byte audit; DRAT semantics replay separately",
        "local_truth_table_rows": audit_local_semantics(),
        "cover": audit_cover(manifest["cases"]),
        "cases": [],
    }
    for case in manifest["cases"]:
        parameters = case["parameters"]
        encoder = IndependentEncoder(
            parameters["n"],
            tuple(parameters["matching_cycle_type"]),
            tuple(parameters["third_matching_cycle_type"])
            if parameters["third_matching_cycle_type"] is not None
            else None,
        )
        generated = encoder.dimacs_bytes()
        cnf_path = args.artifact_dir / case["cnf"]["file"]
        proof_path = args.artifact_dir / case["proof"]["file"]
        expected_cnf = {key: case["cnf"][key] for key in ("bytes", "sha256")}
        expected_proof = {key: case["proof"][key] for key in ("bytes", "sha256")}
        require(identity(cnf_path) == expected_cnf, f"{case['id']}: frozen CNF identity differs")
        require(identity(proof_path) == expected_proof, f"{case['id']}: frozen proof identity differs")
        generated_identity = {
            "bytes": len(generated),
            "sha256": hashlib.sha256(generated).hexdigest(),
        }
        require(generated_identity == expected_cnf, f"{case['id']}: independent CNF reconstruction differs")
        report["cases"].append(
            {
                "id": case["id"],
                "variables": encoder.next_variable - 1,
                "clauses": len(encoder.clauses),
                "cnf": expected_cnf,
                "proof": expected_proof,
                "status": "PASS",
            }
        )
        print(json.dumps({"id": case["id"], "status": "PASS"}), flush=True)
    report.update(status="PASS", checked_cases=len(report["cases"]))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "checked_cases": report["checked_cases"]}))


if __name__ == "__main__":
    main()
