"""Replay the finite controls for protected-component elimination.

The checker reconstructs the exterior vertex-square-zero algebra on the
accepted n=8 v1/v2/v3 Laurent families.  It verifies the literal K4 boundary,
all local-word rows over pure exterior words, and the exact failures of the
canonical quadratic updates.  The controls are not full GHZ sources and do
not refute the open full-source elimination implication.

No receipt file is written; a JSON result is printed to stdout.
"""
from __future__ import annotations

import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

ROOT, _ = bootstrap(__file__)
FIXTURE = ROOT / "tests/fixtures/eight_vertex_scaffold_subsystem_controls.json"
ZERO_EXP = (0,) * 6
MATCHINGS = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}
# Polynomial keys are (sorted ((exterior_vertex,color),...), Laurent exponent).
# Repeated exterior physical vertices vanish.


def add(*polys):
    out = defaultdict(Fraction)
    for p in polys:
        for key, value in p.items():
            out[key] += value
    return {key: value for key, value in out.items() if value}


def scale(p, scalar):
    scalar = Fraction(scalar)
    return {key: scalar * value for key, value in p.items() if scalar * value}


def mul(p, q):
    out = defaultdict(Fraction)
    for (word1, exp1), value1 in p.items():
        vertices1 = {v for v, _ in word1}
        for (word2, exp2), value2 in q.items():
            if vertices1.intersection(v for v, _ in word2):
                continue
            word = tuple(sorted(word1 + word2))
            exp = tuple(a + b for a, b in zip(exp1, exp2))
            out[(word, exp)] += value1 * value2
    return {key: value for key, value in out.items() if value}


def one():
    return {((), ZERO_EXP): Fraction(1)}


def variable(vertex, color, coeff=1, exp=ZERO_EXP):
    return {(((vertex, color),), exp): Fraction(coeff)}


def top(p):
    return {key: value for key, value in p.items() if len(key[0]) == 4}


def exp_quadratic(q):
    # Four exterior physical vertices: only degrees 0,2,4 survive.
    return add(one(), q, scale(mul(q, q), Fraction(1, 2)))


def fixture_f(family, parameter_order, local_vertex, local_color):
    terms = []
    for parameter_index, ((a, b), support) in enumerate(
        zip(parameter_order, family["supports"])
    ):
        if a != local_color:
            continue
        for entry_index, (i, j) in enumerate(support):
            if i != local_vertex:
                continue
            exponent = [0] * 6
            exponent[parameter_index] = 1 if entry_index == 0 else -1
            sign = 1 if entry_index == 0 else -1
            terms.append(variable(j, b, sign, tuple(exponent)))
    return add(*terms) if terms else {}


def protected_q():
    terms = []
    for color, edges in MATCHINGS.items():
        for u, v in edges:
            terms.append(mul(variable(u, color), variable(v, color)))
    return add(*terms)


def ghz():
    terms = []
    for color in range(3):
        p = one()
        for vertex in range(4):
            p = mul(p, variable(vertex, color))
        terms.append(p)
    return add(*terms)


def boundary(family, parameter_order):
    kcs = []
    uv = []
    for color in range(3):
        (p, q), (r, s) = MATCHINGS[color]
        u = mul(
            fixture_f(family, parameter_order, p, color),
            fixture_f(family, parameter_order, q, color),
        )
        v = mul(
            fixture_f(family, parameter_order, r, color),
            fixture_f(family, parameter_order, s, color),
        )
        kcs.append(mul(add(one(), u), add(one(), v)))
        uv.append((u, v))
    k = add(*kcs)
    k2 = add(*(add(u, v) for u, v in uv))
    k4 = add(*(mul(u, v) for u, v in uv))
    assert k == add(scale(one(), 3), k2, k4)
    return kcs, uv, k, k2, k4


def boundary_word(family, parameter_order, colors):
    fs = [
        fixture_f(family, parameter_order, vertex, colors[vertex])
        for vertex in range(4)
    ]
    all_cross = one()
    for f in fs:
        all_cross = mul(all_cross, f)
    terms = [all_cross]
    for color, edges in MATCHINGS.items():
        for u, v in edges:
            if colors[u] == color and colors[v] == color:
                complement = [w for w in range(4) if w not in (u, v)]
                terms.append(mul(fs[complement[0]], fs[complement[1]]))
    if len(set(colors)) == 1:
        terms.append(one())
    return add(*terms)


def coefficient_word(p, colors):
    wanted = tuple((vertex, color) for vertex, color in enumerate(colors))
    return {
        exp: value for (word, exp), value in p.items() if word == wanted
    }


def sub(p, q):
    return add(p, scale(q, -1))


def summarize(p):
    words = defaultdict(int)
    for (word, _), _value in p.items():
        colors = tuple(color for _vertex, color in word)
        words[colors] += 1
    first = None
    if p:
        (word, exp), value = sorted(p.items(), key=lambda item: repr(item[0]))[0]
        first = {
            "word": "".join(str(color) for _vertex, color in word),
            "coefficient": str(value),
            "laurent_exponent": list(exp),
        }
    return {"terms": len(p), "words": len(words), "first": first}


def check_family(family, parameter_order):
    q = protected_q()
    expq = exp_quadratic(q)
    target = ghz()
    kcs, uv, k, k2, k4 = boundary(family, parameter_order)
    k2_equals_minus_q = not add(k2, q)
    assert k2_equals_minus_q

    pure_fiber_rows = 0
    for encoded in range(3 ** 4):
        value = encoded
        local_colors = []
        for _ in range(4):
            local_colors.append(value % 3)
            value //= 3
        response = top(
            mul(expq, boundary_word(family, parameter_order, tuple(local_colors)))
        )
        for exterior_color in range(3):
            got = coefficient_word(response, (exterior_color,) * 4)
            expected = (
                {ZERO_EXP: Fraction(1)}
                if tuple(local_colors) == (exterior_color,) * 4
                else {}
            )
            assert got == expected
            pure_fiber_rows += 1
    assert pure_fiber_rows == 243

    exact = top(mul(expq, k))
    assert exact == target

    color_exact = []
    color_quadratic_residuals = []
    for color, (kc, (u, v)) in enumerate(zip(kcs, uv)):
        pure = {
            key: value
            for key, value in target.items()
            if all(c == color for _vertex, c in key[0])
        }
        got = top(mul(expq, kc))
        assert got == pure
        color_exact.append(summarize(sub(got, pure)))
        quadratic = top(exp_quadratic(add(q, u, v)))
        color_quadratic_residuals.append(summarize(sub(quadratic, pure)))

    unit_quadratic = top(exp_quadratic(add(q, k2)))
    logarithmic_prefactor = scale(
        top(exp_quadratic(add(q, scale(k2, Fraction(1, 3))))), 3
    )
    l2 = scale(k2, Fraction(1, 3))
    l4 = add(
        scale(k4, Fraction(1, 3)),
        scale(mul(k2, k2), Fraction(-1, 18)),
    )
    connected_through_four = scale(
        top(add(exp_quadratic(add(q, l2)), l4)), 3
    )
    assert connected_through_four == exact

    sum_color_quadratics = {}
    for u, v in uv:
        sum_color_quadratics = add(
            sum_color_quadratics,
            top(exp_quadratic(add(q, u, v))),
        )
    assert sum_color_quadratics == target

    # In exterior degree four, these are the exact algebraic defects.
    unit_defect_formula = top(
        add(
            mul(q, q),
            k4,
            scale(mul(k2, k2), Fraction(-1, 2)),
        )
    )
    log_defect_formula = top(
        add(k4, scale(mul(k2, k2), Fraction(-1, 6)))
    )
    assert sub(exact, unit_quadratic) == unit_defect_formula
    assert sub(exact, logarithmic_prefactor) == log_defect_formula

    return {
        "family": family["name"],
        "all_local_words_over_pure_exterior_rows": pure_fiber_rows,
        "quadratic_update_k2": summarize(k2),
        "quadratic_update_k2_equals_minus_exterior_q": k2_equals_minus_q,
        "exact_contraction_residual": summarize(sub(exact, target)),
        "color_exact_residuals": color_exact,
        "color_quadratic_residuals": color_quadratic_residuals,
        "unit_quadratic_residual": summarize(sub(unit_quadratic, target)),
        "unit_exact_minus_candidate": summarize(sub(exact, unit_quadratic)),
        "log_prefactor_residual": summarize(sub(logarithmic_prefactor, target)),
        "log_exact_minus_candidate": summarize(sub(exact, logarithmic_prefactor)),
        "connected_through_degree_four_residual": summarize(
            sub(connected_through_four, target)
        ),
        "sum_color_quadratics_residual": summarize(
            sub(sum_color_quadratics, target)
        ),
        "selector_gluing_residual": summarize(
            sub(unit_quadratic, sum_color_quadratics)
        ),
    }


def main():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if data.get("schema") != "n8-protected-scaffold-laurent-controls-v1":
        raise ValueError("wrong control fixture schema")
    parameter_order = tuple(tuple(pair) for pair in data["parameter_order"])
    expected_order = tuple(
        (c, d) for c in range(3) for d in range(3) if c != d
    )
    if parameter_order != expected_order:
        raise ValueError("wrong Laurent parameter order")
    families = {family["name"]: family for family in data["families"]}
    names = [
        "monochromatic_shores_v1",
        "binary_and_monochromatic_shores_v2",
        "independent_minorities_and_component_constants_v3",
    ]
    receipt = {
        "schema": "k4-boundary-quadratic-control-v1",
        "status": "verified_exact_finite_controls",
        "scope": "local-slice closure controls; v1/v2/v3 are not full sources",
        "families": [
            check_family(families[name], parameter_order) for name in names
        ],
    }
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
