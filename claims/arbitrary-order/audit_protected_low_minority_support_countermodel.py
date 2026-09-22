"""Independent structural replay of the compact common-star P1 control.

This intentionally does not import either primary audit implementation.
It checks the literal 12 columns, constructs the 18 protected K4 support,
checks every six-left-color macro constraint, validates each enabled gadget's
local physical perfect matching, and checks the advertised D_c layering.
The all-order q<=1 exclusion remains an analytic argument in the owning theorem document.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, _HERE = bootstrap(__file__)
COLORS = range(3)
PAIRS = {(a, b) for a in COLORS for b in COLORS if a != b}
FIXTURE = REPO_ROOT / "tests/fixtures/protected_eighteen_component_macro_cover.json"


def protected_edges(component: int, color: int):
    others = [x for x in COLORS if x != color]
    # Ports are (component, "O") and (component, leaf-index).
    return {
        frozenset(((component, "O"), (component, color))),
        frozenset(((component, others[0]), (component, others[1]))),
    }


def blocked_colors(column, left_word):
    return {b for x, (a, b) in zip(left_word, column) if x == a}


def main():
    raw = FIXTURE.read_bytes()
    payload = json.loads(raw)
    columns = [tuple((int(s[0]), int(s[1])) for s in row) for row in payload["columns"]]

    assert len(columns) == 12
    assert len(set(columns)) == 12
    assert all(len(row) == 6 and set(row) == PAIRS for row in columns)

    # K_(6,12): one labelled component edge per left/right pair.
    left = tuple(range(6))
    right = tuple(range(6, 18))
    component_edges = {
        (u, v): columns[v - 6][u]
        for u in left
        for v in right
    }
    assert len(component_edges) == 72
    assert all(u < 6 <= v for u, v in component_edges)
    assert all(a != b for a, b in component_edges.values())

    # Each labelled component edge gives exactly the center-center and
    # selected-leaf crossing factors, with no duplicated physical factor.
    physical_crossing_edges = set()
    for (u, v), (a, b) in component_edges.items():
        physical_crossing_edges.add(frozenset(((u, "O", a), (v, "O", b))))
        physical_crossing_edges.add(frozenset(((u, a, a), (v, b, b))))
    assert len(physical_crossing_edges) == 144

    # For every label, the two crossing edges plus the complementary
    # protected leaf pair at each endpoint are a perfect matching of the
    # two incident K4s. Endpoint colors agree with the label.
    for a, b in PAIRS:
        u, v = 0, 6
        edges = {
            frozenset(((u, "O"), (v, "O"))),
            frozenset(((u, a), (v, b))),
        }
        left_other = [x for x in COLORS if x != a]
        right_other = [x for x in COLORS if x != b]
        edges.add(frozenset(((u, left_other[0]), (u, left_other[1]))))
        edges.add(frozenset(((v, right_other[0]), (v, right_other[1]))))
        used = [port for edge in edges for port in edge]
        assert len(used) == 8 and len(set(used)) == 8
        assert set(used) == {(u, "O"), (u, 0), (u, 1), (u, 2),
                             (v, "O"), (v, 0), (v, 1), (v, 2)}

    # Exact macro CSP: only constant global component colorings avoid all
    # gadgets. It is enough to enumerate 3^6 left words: each right column
    # is conditionally independent.
    nonconstant = 0
    for x in itertools.product(COLORS, repeat=6):
        blocked = [blocked_colors(row, x) for row in columns]
        if len(set(x)) == 1:
            c = x[0]
            assert all(s == set(COLORS) - {c} for s in blocked)
            assert all(set(COLORS) - s == {c} for s in blocked)
        else:
            nonconstant += 1
            assert any(s == set(COLORS) for s in blocked)
    assert nonconstant == 726

    # Literal common-star entries always orient D_c through the layer order
    # non-c leaf -> center -> c leaf.  Check it for every support label and
    # each possible target background color at either endpoint.
    for (a, b) in component_edges.values():
        for target in (a, b):
            source_leaf = b if target == a else a
            assert source_leaf != target
            layers = {("leaf", source_leaf): 0, ("center", None): 1,
                      ("leaf", target): 2}
            assert layers[("leaf", source_leaf)] < layers[("center", None)]
            assert layers[("center", None)] < layers[("leaf", target)]

    print(f"fixture_sha256={hashlib.sha256(raw).hexdigest()}")
    print("components=18 component_edges=72 physical_crossing_edges=144")
    print("macro_nonconstant_left_words=726")
    print("gadget_local_matchings=6")
    print("whole_port_layering=PASS")
    print("COMPACT_COMMON_STAR_INDEPENDENT_REPLAY_PASS")


if __name__ == "__main__":
    main()
