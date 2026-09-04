"""Independent reconstruction and DPLL tree checker; standard library only."""

if not __debug__:
    raise RuntimeError(
        "This checker requires assertions; Python -O/-OO is unsupported."
    )

from collections import Counter
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import argparse

PIN = "4415ea3d243603910729098d104240ca2d6fd2fa1d2843098e3131b4088ac1ac"
INPUT_PIN = PIN
CERT_PIN = "d73b746cbf5bafdcb1ac6e2af9bcac65475e5d7d1595f82cabca25bc8556c1fd"


def read_cnf(path):
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PIN
    rows = raw.decode("ascii").splitlines()
    header = rows.pop(0).split()
    assert header[:2] == ["p", "cnf"]
    n, m = map(int, header[2:])
    clauses = []
    for row in rows:
        values = list(map(int, row.split()))
        assert values[-1] == 0 and all(0 < abs(x) <= n for x in values[:-1])
        clauses.append(tuple(values[:-1]))
    assert len(clauses) == m
    return n, clauses


def reconstruct():
    edges = list(combinations(range(6), 2))

    def entry(u, v, a, b):
        if u > v:
            u, v, a, b = v, u, b, a
        return 1 + 9 * edges.index((u, v)) + 3 * a + b

    def match(vertices):
        if not vertices:
            yield []
        else:
            a = vertices[0]
            for b in vertices[1:]:
                rest = [x for x in vertices if x not in (a, b)]
                for smaller in match(rest):
                    yield [(a, b)] + smaller

    groups = {}
    groups["matrix_units"] = []
    for u, v in edges:
        if u // 3 == v // 3:
            variables = [entry(u, v, a, b) for a, b in product(range(3), repeat=2)]
            groups["matrix_units"].append(variables)
            groups["matrix_units"] += [[-a, -b] for a, b in combinations(variables, 2)]
    groups["term_definitions"] = []
    groups["coefficient_necessities"] = []
    for deletion in range(9):
        i, j = divmod(deletion, 3)
        remain = [v for v in range(6) if v not in (i, j + 3)]
        matchings = list(match(remain))
        assert len(matchings) == 3
        for word_number in range(81):
            colors = {
                v: (word_number // 3 ** (3 - k)) % 3 for k, v in enumerate(remain)
            }
            terms = [136 + deletion * 243 + word_number * 3 + k for k in range(3)]
            for t, matching in zip(terms, matchings):
                a, b = [entry(u, v, colors[u], colors[v]) for u, v in matching]
                groups["term_definitions"] += [[-t, a], [-t, b], [t, -a, -b]]
            if i == j and all(c == i for c in colors.values()):
                groups["coefficient_necessities"].append(terms)
            else:
                groups["coefficient_necessities"] += [
                    [-t] + [s for s in terms if s != t] for t in terms
                ]
    groups["rectangles"] = []
    for u in range(3):
        for v in range(3, 6):
            for a, b, c, d in product(range(3), repeat=4):
                antecedent = [-entry(u, v, a, b), -entry(u, v, c, d)]
                groups["rectangles"] += [
                    antecedent + [entry(u, v, a, d)],
                    antecedent + [entry(u, v, c, b)],
                ]
    groups["anchors"] = []
    rectangles = [(i, j) for i in range(3) for j in range(3) if i != j]
    for r, (i, j) in enumerate(rectangles):
        aa = [a for a in range(3) if a != i]
        bb = [b for b in range(3, 6) if b != j + 3]
        # Arithmetic label map: each rectangle has six row then six column selectors.
        row = {
            (u, c): 2323 + 12 * r + 3 * k + c
            for k, u in enumerate(aa)
            for c in range(3)
        }
        col = {
            (v, c): 2329 + 12 * r + 3 * k + c
            for k, v in enumerate(bb)
            for c in range(3)
        }
        for (u, c), selector in row.items():
            for v, a, b in product(bb, range(3), range(3)):
                if a != c:
                    groups["anchors"].append([-selector, -entry(u, v, a, b)])
        for (v, c), selector in col.items():
            for u, a, b in product(aa, range(3), range(3)):
                if b != c:
                    groups["anchors"].append([-selector, -entry(u, v, a, b)])
        for a, b in product(range(3), repeat=2):
            groups["anchors"].append([-entry(*aa, a, b), row[aa[0], a], row[aa[1], b]])
            groups["anchors"].append([-entry(*bb, a, b), col[bb[0], a], col[bb[1], b]])
    return groups


def conflicts_by_up(clauses, decisions):
    # Deliberately no solver state reuse: reduce each original clause afresh.
    truth = set(decisions)
    if any(-lit in truth for lit in truth):
        return True
    while True:
        units = set()
        for clause in clauses:
            if any(lit in truth for lit in clause):
                continue
            residual = {lit for lit in clause if -lit not in truth}
            if not residual:
                return True
            if len(residual) == 1:
                units.update(residual)
        if any(-lit in truth or -lit in units for lit in units):
            return True
        if units <= truth:
            return False
        truth.update(units)


def verify_tree(document, n, clauses):
    assert document["format"] == "dpll-binary-up-v1"
    assert document["cnf_sha256"] == PIN
    assert document["variables"] == n and document["clauses"] == len(clauses)

    def reduce_formula(formula, assumptions):
        # Functional, batch-unit elimination. None is the falsified formula.
        # No watches, trail, learned clauses, or solver imports.
        while True:
            true, false = assumptions
            if true & false:
                return None
            smaller = []
            unit_true = unit_false = 0
            for positive, negative in formula:
                if positive & true or negative & false:
                    continue
                positive &= ~false
                negative &= ~true
                union = positive | negative
                if not union:
                    return None
                smaller.append((positive, negative))
                if union & (union - 1) == 0:
                    unit_true |= positive
                    unit_false |= negative
            formula = smaller
            if not (unit_true or unit_false):
                return formula
            assumptions = (unit_true, unit_false)

    normalized = []
    for clause in clauses:
        positive = negative = 0
        for lit in clause:
            if lit > 0:
                positive |= 1 << (lit - 1)
            else:
                negative |= 1 << (-lit - 1)
        if not positive & negative:
            normalized.append((positive, negative))
    pending = [(document["tree"], (), reduce_formula(normalized, (0, 0)))]
    branches = leaves = 0
    while pending:
        node, decisions, residual = pending.pop()
        if node is None:
            assert residual is None, ("invalid leaf", decisions)
            leaves += 1
        else:
            assert isinstance(node, list) and len(node) == 3
            lit, left, right = node
            assert type(lit) is int and 0 < abs(lit) <= n
            assert abs(lit) not in {abs(x) for x in decisions}
            branches += 1
            for child, decision in ((left, lit), (right, -lit)):
                mask = 1 << (abs(decision) - 1)
                assumption = (mask, 0) if decision > 0 else (0, mask)
                child_formula = (
                    None if residual is None else reduce_formula(residual, assumption)
                )
                pending.append((child, decisions + (decision,), child_formula))
    assert leaves == branches + 1
    return {"branches": branches, "leaves": leaves}


def selftest():
    def document(n, clauses, tree):
        return {
            "format": "dpll-binary-up-v1",
            "cnf_sha256": PIN,
            "variables": n,
            "clauses": len(clauses),
            "tree": tree,
        }

    cases = [
        (1, [(1,), (-1,)], None, True),
        (2, [(1, 2), (1, -2), (-1, 2), (-1, -2)], [1, None, None], True),
        (2, [(1, 2), (1, -2), (-1, 2), (-1, -2)], None, False),
        (2, [(1, 2), (-1, 2)], [2, None, None], False),
        (1, [(1,)], None, False),
        (1, [(1, -1)], None, False),
        (1, [(1, 1), (-1, -1)], None, True),
        (1, [(1,), (-1,)], [2, None, None], False),
        (1, [(1,), (-1,)], [1, None], False),
    ]
    for n, clauses, tree, expected in cases:
        try:
            verify_tree(document(n, clauses, tree), n, clauses)
            accepted = True
        except AssertionError:
            accepted = False
        assert accepted == expected, (clauses, tree, expected)
    return len(cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cnf",
        type=Path,
        help="Frozen DIMACS CNF (required except for --self-test-only).",
    )
    parser.add_argument(
        "--certificate",
        type=Path,
        help="Frozen certificate (default: certificate.json adjacent to CNF).",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--self-test-only",
        action="store_true",
        help="Run checker controls without reading external artifacts.",
    )
    mode.add_argument(
        "--encoding-only",
        action="store_true",
        help="Reconstruct the pinned CNF without checking the certificate.",
    )
    args = parser.parse_args()
    controls = selftest()
    if args.self_test_only:
        print(
            json.dumps(
                {
                    "checker_controls": "PASS",
                    "checker_positive_and_negative_controls": controls,
                },
                indent=2,
            )
        )
        return
    if args.cnf is None:
        parser.error("--cnf PATH is required unless --self-test-only is supplied")
    n, clauses = read_cnf(args.cnf)
    groups = reconstruct()
    expected = [tuple(c) for rows in groups.values() for c in rows]
    normalize = lambda rows: Counter(tuple(sorted(c)) for c in rows)
    assert normalize(expected) == normalize(clauses)
    assert n == 2394 and len(clauses) == 11394
    # Independent finite semantic sanity checks.
    for a, b, t in product([False, True], repeat=3):
        encoded = (not t or a) and (not t or b) and (t or not a or not b)
        assert encoded == (t == (a and b))
    for ts in product([False, True], repeat=3):
        zero = all(
            not ts[k] or any(ts[j] for j in range(3) if j != k) for k in range(3)
        )
        assert zero == (sum(ts) != 1)
    result = {
        "encoding": "PASS",
        "cnf_sha256": PIN,
        "variables": n,
        "checker_positive_and_negative_controls": controls,
        "clause_categories": {k: len(v) for k, v in groups.items()},
    }
    if not args.encoding_only:
        path = args.certificate or args.cnf.with_name("certificate.json")
        raw_certificate = path.read_bytes()
        certificate_hash = hashlib.sha256(raw_certificate).hexdigest()
        assert certificate_hash == CERT_PIN, (
            "Certificate bytes do not match the frozen certificate hash"
        )
        result["certificate_sha256"] = certificate_hash
        result["certificate"] = verify_tree(json.loads(raw_certificate), n, clauses)
        result["certificate_status"] = "PASS"
    else:
        result["certificate_status"] = "NOT RUN: --encoding-only"
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
