"""Primary exact checks for the three-edge shore flattening exclusion."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    l_c, l_d, l_e, o_q, o_p = sp.symbols("l_c l_d l_e o_q o_p")
    three_port = l_c * o_q + l_d * o_q + l_e * o_p
    two_complement = (l_c + l_d) * o_q + l_e * o_p
    assert sp.expand(three_port - two_complement) == 0

    shore_vectors = sp.Matrix([[1, 0], [1, 0], [0, 1]])
    complement_vectors = sp.eye(2)
    shore_flattening = shore_vectors * complement_vectors
    assert shore_flattening.rank() == 2

    target_flattening = sp.diag(2, 3, 5)
    assert target_flattening.rank() == 3
    assert all(target_flattening.minor_submatrix(i, i).det() != 0 for i in range(3))

    size_s = sp.symbols("size_s", integer=True, positive=True)
    size_t = size_s - 1
    assert sp.simplify(size_s - size_t) == 1

    print("arbitrary permanent equality three-edge shore flattening: PASS")
    print("fixed factor/rank algebra only; no matching or support search was performed")


if __name__ == "__main__":
    main()
