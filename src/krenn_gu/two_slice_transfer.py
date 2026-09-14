"""Exact eight-row two-slice transfer identities on eight physical vertices.

The family uses base colour 2, boundary vertices (x,p,q,y)=(0,5,6,7),
and bulk F={1,2,3,4}.  The two q-colour slices share the same expanded
bulk hafnian.  Alternating contractions in the x and y colours cancel that
shared cofactor without naming it as an independent variable or dividing by
it.  The surviving pure-target term is the declared physical monomial.

These patterns are guarded polynomial identities.  Their vertex/colour
orbits are not asserted here to cover an arbitrary support or witness.
"""

from __future__ import annotations

from krenn_gu.two_edge_surplus_shore import entry, replay


N = 8
BASE = 2
NONBASE = (0, 1)
X_VERTEX = 0
P_VERTEX = 5
Q_VERTEX = 6
Y_VERTEX = 7
BULK = (1, 2, 3, 4)


def _require_nonbase(name: str, colour: int) -> None:
    if type(colour) is not int or colour not in NONBASE:
        raise ValueError(f"{name} must be one of the two nonbase colours {NONBASE}")


def make_pattern(x: int, z: int, t: int) -> dict[str, object]:
    """Build one exact eight-row identity for nonbase colours x, z, and t.

    The physical entry families are

        A_a=W05[a,2], B_a=W06[a,t],
        C_d=W57[2,d], D_d=W67[2,d].

    The q=t slice uses the alternating A*D contraction.  The q=2 slice
    uses its negative B*C contraction.  The shared degree-six part cancels,
    while the pure word in the second slice leaves B_x*C_z.
    """

    _require_nonbase("x", x)
    _require_nonbase("z", z)
    _require_nonbase("t", t)

    A = {a: entry(X_VERTEX, P_VERTEX, a, BASE) for a in (x, BASE)}
    B = {a: entry(X_VERTEX, Q_VERTEX, a, t) for a in (x, BASE)}
    C = {d: entry(P_VERTEX, Y_VERTEX, BASE, d) for d in (z, BASE)}
    D = {d: entry(Q_VERTEX, Y_VERTEX, BASE, d) for d in (z, BASE)}

    zeros = set()
    for vertex in BULK:
        zeros.update(
            (
                entry(vertex, P_VERTEX, BASE, BASE),
                entry(vertex, Q_VERTEX, BASE, t),
                entry(vertex, Y_VERTEX, BASE, z),
                entry(vertex, Y_VERTEX, BASE, BASE),
            )
        )
    zeros.update(
        (
            entry(P_VERTEX, Q_VERTEX, BASE, t),
            entry(P_VERTEX, Q_VERTEX, BASE, BASE),
        )
    )
    if len(zeros) != 18:
        raise AssertionError(f"two-slice guard has {len(zeros)} entries, expected 18")

    sources = []
    # First q=t slice: (u_A tensor u_D)(T_t).
    for a, d in ((BASE, BASE), (BASE, z), (x, BASE), (x, z)):
        word = [BASE] * N
        word[X_VERTEX] = a
        word[Q_VERTEX] = t
        word[Y_VERTEX] = d
        sources.append(
            {
                "word": "".join(map(str, word)),
                "multiplier": sorted(
                    (
                        A[x] if a == BASE else A[BASE],
                        D[z] if d == BASE else D[BASE],
                    )
                ),
                "coefficient": 1 if (a == BASE) == (d == BASE) else -1,
            }
        )

    # Second q=2 slice: -(u_B tensor u_C)(T_2).
    for a, d in ((BASE, BASE), (BASE, z), (x, BASE), (x, z)):
        word = [BASE] * N
        word[X_VERTEX] = a
        word[Q_VERTEX] = BASE
        word[Y_VERTEX] = d
        sources.append(
            {
                "word": "".join(map(str, word)),
                "multiplier": sorted(
                    (
                        B[x] if a == BASE else B[BASE],
                        C[z] if d == BASE else C[BASE],
                    )
                ),
                "coefficient": -1 if (a == BASE) == (d == BASE) else 1,
            }
        )

    target = sorted((B[x], C[z]))
    return {
        "schema": "eight-vertex-physical-degree6-identity-v1",
        "n": N,
        "field": "any field",
        "family": "two-slice-shared-cofactor-transfer",
        "parameters": {
            "base_colour": BASE,
            "x_colour": x,
            "z_colour": z,
            "first_slice_colour": t,
            "boundary_vertices": [X_VERTEX, P_VERTEX, Q_VERTEX, Y_VERTEX],
            "bulk_vertices": list(BULK),
        },
        "entry_families": {
            "A_a": "W05[a,2]",
            "B_a": f"W06[a,{t}]",
            "C_d": "W57[2,d]",
            "D_d": "W67[2,d]",
            "A": {str(a): A[a] for a in (x, BASE)},
            "B": {str(a): B[a] for a in (x, BASE)},
            "C": {str(d): C[d] for d in (z, BASE)},
            "D": {str(d): D[d] for d in (z, BASE)},
        },
        "zero_entry_ids": sorted(zeros),
        "nonzero_entry_ids": target,
        "target_monomial": target,
        "sources": sources,
        "equation_convention": (
            "P_word=T_W(word)-1 for pure words, T_W(word) otherwise"
        ),
        "identity": "sum(source.coefficient * source.multiplier * P_word) = B_x*C_z",
        "uses_boundary_relation": False,
        "requires_nonzero_proper_cofactor": False,
        "cofactor_divisions": 0,
    }


def four_patterns() -> list[dict[str, object]]:
    """Return canonical types after fixing x=0 by the common nonbase swap."""

    return [make_pattern(0, z, t) for z in NONBASE for t in NONBASE]


def validate_four_patterns() -> list[dict[str, object]]:
    """Replay all four canonical polynomial identities with actual hafnians."""

    results = []
    expected_counts = [6, 6, 6, 6, 18, 18, 18, 18]
    for pattern in four_patterns():
        result = replay(pattern)
        if result["source_term_counts"] != expected_counts:
            raise AssertionError(
                "unexpected expanded source counts: "
                f"{result['source_term_counts']} != {expected_counts}"
            )
        if result["zero_entry_ids"] != pattern["zero_entry_ids"]:
            raise AssertionError("replay changed the declared zero guard")
        if result["nonzero_entry_ids"] != pattern["nonzero_entry_ids"]:
            raise AssertionError("replay changed the declared nonzero guard")
        results.append(result)
    return results
