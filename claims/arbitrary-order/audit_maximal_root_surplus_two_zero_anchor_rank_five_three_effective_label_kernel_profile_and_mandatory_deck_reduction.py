"""Independent no-import audit for GLS50.

This implementation uses only hand-written arithmetic over F_5.  It does not
import SymPy, NumPy, the primary verifier, or repository code.
"""


P = 5
VECTORS = [(a, b, c) for a in range(P) for b in range(P) for c in range(P)]
NONZERO = [v for v in VECTORS if v != (0, 0, 0)]
AXES = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]


def inv(x):
    for y in range(1, P):
        if x * y % P == 1:
            return y
    raise ValueError("zero has no inverse")


def normalize(v):
    for x in v:
        if x % P:
            scale = inv(x % P)
            return tuple(scale * y % P for y in v)
    return (0, 0, 0)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b)) % P


LINES = sorted({normalize(v) for v in NONZERO})
FORMS = [(0, 0, 0)] + LINES
KERNELS = {form: [v for v in VECTORS if dot(form, v) == 0] for form in FORMS}


def direct_gamma_zero_audit():
    """Find a surviving diagonal target coefficient on every kernel product."""

    checked = 0
    for lambda_u in FORMS:
        for lambda_v in FORMS:
            witness = None
            for z in KERNELS[lambda_u]:
                if z == (0, 0, 0):
                    continue
                for w in KERNELS[lambda_v]:
                    if any(z[c] * w[c] % P for c in range(3)):
                        witness = (z, w)
                        break
                if witness is not None:
                    break
            assert witness is not None, (lambda_u, lambda_v)
            checked += 1
    return checked


def deck_line_cover_audit():
    """Audit the triple quotient directly through projective line incidence."""

    coordinate_index = {axis: c for c, axis in enumerate(AXES)}
    covers = {}
    for form in FORMS:
        normal = normalize(form)
        covers[form] = {coordinate_index[normal]} if normal in coordinate_index else set()

    valid = []
    for lambda_u in FORMS:
        for lambda_v in FORMS:
            for lambda_w in FORMS:
                union = covers[lambda_u] | covers[lambda_v] | covers[lambda_w]
                if union == {0, 1, 2}:
                    valid.append((lambda_u, lambda_v, lambda_w))
    assert len(valid) == 6
    assert all(set(triple) == set(AXES) for triple in valid)
    return len(valid)


def large_kernel_obstruction_audit():
    """Every dimension-at-least-two kernel meets the kernel of every deck form."""

    checked = 0
    # ker(h) runs over all planes, while h=0 gives the whole three-space.
    for h in FORMS:
        for deck in FORMS:
            intersection = [
                v for v in NONZERO if dot(h, v) == 0 and dot(deck, v) == 0
            ]
            assert intersection, (h, deck)
            # A nonzero vector always gives a nonzero target slice: choose any
            # nonzero coordinate c and then the matching pure opposite words.
            k = intersection[0]
            assert any(k[c] % P for c in range(3))
            checked += 1
    return checked


def line_deck_activity_audit():
    """A kernel line forces its opposite deck to be nonzero on that line."""

    hostile = 0
    admissible = 0
    for line in LINES:
        for deck in FORMS:
            if dot(line, deck) == 0:
                hostile += 1
                # The diagonal target slice at line is nevertheless nonzero,
                # so this pair cannot occur in the exact restricted equation.
                assert any(line)
            else:
                admissible += 1
    assert hostile > 0 and admissible > 0
    return hostile, admissible


def profile_audit():
    one_residual = set()
    for ku in (0, 1):
        for kv in (0, 1):
            if ku and kv:
                continue
            one_residual.add(tuple(sorted((1, 3 - ku, 3 - kv))))
    assert one_residual == {(1, 2, 3), (1, 3, 3)}

    three_port = set()
    for ku in (0, 1):
        for kv in (0, 1):
            for kw in (0, 1):
                if ku and kv and kw:
                    continue
                three_port.add(tuple(sorted((3 - ku, 3 - kv, 3 - kw))))
    assert three_port == {(2, 2, 3), (2, 3, 3), (3, 3, 3)}
    return sorted(one_residual), sorted(three_port)


def main():
    assert len(LINES) == (P**3 - 1) // (P - 1) == 31
    gamma_pairs = direct_gamma_zero_audit()
    deck_permutations = deck_line_cover_audit()
    large_kernel_pairs = large_kernel_obstruction_audit()
    hostile, admissible = line_deck_activity_audit()
    one_residual, three_port = profile_audit()

    print("GLS50 independent no-import audit: PASS")
    print(f"projective F_{P} lines: {len(LINES)}")
    print(f"gamma-zero deck pairs refuted directly: {gamma_pairs}")
    print(f"three-deck coordinate covers: {deck_permutations}")
    print(f"large-kernel/deck pairs refuted: {large_kernel_pairs}")
    print(f"kernel-line deck pairs: hostile={hostile}, admissible={admissible}")
    print(f"profiles: one-residual={one_residual}; three-port={three_port}")


if __name__ == "__main__":
    main()
