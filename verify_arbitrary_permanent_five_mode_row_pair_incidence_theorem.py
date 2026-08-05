"""Verify the symbolic core of the five-mode row-pair incidence theorem.

The six incidence patterns are the normal forms derived in the theorem note;
this script checks those normal forms and their polar-rank witnesses.  It does
not enumerate assignments of labels to modes.
"""

import sympy as sp

IncidenceType = tuple[frozenset[int], ...]


def neighbourhoods(pattern: IncidenceType) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(index for index, label in enumerate(pattern) if color in label)
        for color in range(3)
    )


def main() -> None:
    # The six normal forms obtained algebraically from Y=2,3,4.
    patterns: dict[str, IncidenceType] = {
        "I": (frozenset((1, 2)), frozenset((1, 2)), frozenset((0,)), frozenset((0,))),
        "II": (frozenset((1, 2)), frozenset((0, 2)), frozenset((0,)), frozenset((1,))),
        "III": (frozenset((1, 2)), frozenset((0, 2)), frozenset((0, 1)), frozenset((0,))),
        "IV": (frozenset((1, 2)), frozenset((1, 2)), frozenset((0, 2)), frozenset((0,))),
        "V": (frozenset((1, 2)), frozenset((1, 2)), frozenset((0, 2)), frozenset((0, 2))),
        "VI": (frozenset((1, 2)), frozenset((1, 2)), frozenset((0, 2)), frozenset((0, 1))),
    }
    expected_degrees = {
        "I": (2, 2, 2),
        "II": (2, 2, 2),
        "III": (3, 2, 2),
        "IV": (2, 2, 3),
        "V": (2, 2, 4),
        "VI": (2, 3, 3),
    }
    expected_doubles = {"I": 2, "II": 2, "III": 3, "IV": 3, "V": 4, "VI": 4}

    for name, pattern in patterns.items():
        degrees = tuple(len(neighbourhood) for neighbourhood in neighbourhoods(pattern))
        assert degrees == expected_degrees[name]
        assert sum(len(label) == 2 for label in pattern) == expected_doubles[name]
        assert all(degree >= 2 for degree in degrees)

    # Types II--VI each expose a unique size-two colour neighbourhood whose
    # endpoints are both double-incidence, hence rank-two, modes.
    witnesses = {"II": 2, "III": 1, "IV": 1, "V": 0, "VI": 0}
    for name, color in witnesses.items():
        pattern = patterns[name]
        ns = neighbourhoods(pattern)
        witness = ns[color]
        assert len(witness) == 2
        assert all(ns[other] != witness for other in range(3) if other != color)
        assert all(len(pattern[index]) == 2 for index in witness)

    # A corrected port block between any two rank-two endpoints is rank two.
    u00, u01, u10, u11 = sp.symbols("u00 u01 u10 u11")
    v00, v01, v10, v11 = sp.symbols("v00 v01 v10 v11")
    u_frame = sp.Matrix(((u00, u01), (u10, u11)))
    v_frame = sp.Matrix(((v00, v01), (v10, v11)))
    j_form = sp.Matrix(((0, 1), (1, 0)))
    port_minor = u_frame.T * j_form * v_frame
    assert sp.factor(port_minor.det() + u_frame.det() * v_frame.det()) == 0

    # Type I: S consists of singleton-{0} modes and T of plane-{1,2}
    # modes.  The free-S slice is supported only on colour zero.
    n_i = neighbourhoods(patterns["I"])
    singleton_pair = n_i[0]
    double_pair = n_i[1]
    assert n_i[1] == n_i[2]
    assert singleton_pair.isdisjoint(double_pair)
    assert len(singleton_pair) == len(double_pair) == 2

    lambda_0, lambda_1, lambda_2 = sp.symbols("lambda_0 lambda_1 lambda_2", nonzero=True)
    free_s_target = sp.diag(lambda_0, 0, 0)
    assert free_s_target.rank() == 1

    # If that rank-one slice forces one singleton endpoint down to
    # A=<e0*>, choose e1 in its two-dimensional kernel.  All other
    # contracted modes can be chosen with colour-one coordinate nonzero.
    alpha, shore_product = sp.symbols("alpha shore_product", nonzero=True)
    collapsed_kernel_vector = sp.Matrix((0, 1, 0))
    other_singleton_vector = sp.Matrix((0, alpha, sp.Symbol("beta")))
    assert collapsed_kernel_vector[0] == collapsed_kernel_vector[2] == 0
    assert collapsed_kernel_vector[1] * other_singleton_vector[1] != 0
    free_t_target = sp.diag(
        lambda_0 * collapsed_kernel_vector[0],
        lambda_1 * collapsed_kernel_vector[1] * other_singleton_vector[1] * shore_product,
        lambda_2 * collapsed_kernel_vector[2],
    )
    assert free_t_target.rank() == 1
    assert free_t_target[1, 1] != 0

    # The T endpoints are coordinate planes {1,2}; an exact representative
    # gives a rank-two diagonal port response.
    r_left = sp.Matrix(((0, 1, 0), (0, 0, 1)))
    r_right = sp.Matrix(((0, 0, 1), (0, 1, 0)))
    double_port = r_left.T * j_form * r_right
    assert double_port == sp.diag(0, 1, 1)
    assert double_port.rank() == 2

    print("PASS: six algebraically derived four-mode incidence normal forms")
    print("PASS: omitted Y=3 type IV has degrees (2,2,3) and a rank witness")
    print("PASS: Types II-VI fail the unique size-two neighbourhood test")
    print("PASS: Type I fails its second polar rank test")
    print("SCOPE: at least five incidence modes; equality at five remains open")


if __name__ == "__main__":
    main()
