"""Independent audit of pair-companion exchange and projective transport."""

from fractions import Fraction


def choose_pairs(items):
    for first in range(len(items)):
        for second in range(first + 1, len(items)):
            yield items[first], items[second]


def permutations(items):
    if not items:
        yield ()
        return
    for index, item in enumerate(items):
        remainder = items[:index] + items[index + 1 :]
        for tail in permutations(remainder):
            yield (item,) + tail


def factorial(value):
    answer = 1
    for factor in range(2, value + 1):
        answer *= factor
    return answer


def gcd(first, second):
    while second:
        first, second = second, first % second
    return abs(first)


def root_partial_matching_descriptions(order, target):
    roots = tuple(range(order))
    complement = tuple(port for port in roots if port not in target)
    descriptions = set()
    for edge in choose_pairs(roots):
        free = tuple(root for root in roots if root not in edge)
        for assigned in permutations(complement):
            mapping = tuple(zip(free, assigned))
            descriptions.add((edge, mapping))
    return descriptions


def residual_bijection_descriptions(order, target):
    roots = tuple(range(order))
    complement = tuple(port for port in roots if port not in target)
    outside = ("q0", "q1") + tuple(("u", port) for port in complement)
    descriptions = set()
    for assigned in permutations(outside):
        q0_root = assigned.index("q0")
        q1_root = assigned.index("q1")
        pair = tuple(sorted((q0_root, q1_root)))
        orientation = 0 if (q0_root, q1_root) == pair else 1
        port_map = tuple(
            (root, vertex[1])
            for root, vertex in enumerate(assigned)
            if isinstance(vertex, tuple)
        )
        description = (pair, orientation, port_map)
        assert description not in descriptions
        descriptions.add(description)

        reconstructed = [None] * order
        left, right = pair
        if orientation == 0:
            reconstructed[left], reconstructed[right] = "q0", "q1"
        else:
            reconstructed[left], reconstructed[right] = "q1", "q0"
        for root, port in port_map:
            reconstructed[root] = ("u", port)
        assert tuple(reconstructed) == assigned
    return descriptions


def audit_matching_bijections():
    counts = {}
    for order in range(2, 9):
        target_count = 0
        for target in choose_pairs(tuple(range(order))):
            partial = root_partial_matching_descriptions(order, target)
            residual = residual_bijection_descriptions(order, target)
            expected_partial = order * (order - 1) * factorial(order - 2) // 2
            assert len(partial) == expected_partial
            assert len(residual) == factorial(order)
            target_count += 1
        counts[order] = target_count
    return counts


def primitive(delta, eta):
    common = gcd(abs(delta), abs(eta))
    delta //= common
    eta //= common
    if delta < 0 or (delta == 0 and eta < 0):
        delta, eta = -delta, -eta
    return delta, eta


def directions(bound=4):
    answer = set()
    for delta in range(-bound, bound + 1):
        for eta in range(-bound, bound + 1):
            if delta or eta:
                answer.add(primitive(delta, eta))
    return tuple(sorted(answer))


def determinant(first, second):
    delta_t, eta_t = first
    delta_s, eta_s = second
    return delta_t * eta_s - eta_t * delta_s


def audit_projective_transport():
    lines = directions()
    generators = (Fraction(-5, 3), Fraction(1), Fraction(7, 2))
    checks = 0
    for second in lines:
        delta_s, eta_s = second
        for generator in generators:
            g_m = delta_s * generator
            g_z = eta_s * generator
            assert delta_s * g_z - eta_s * g_m == 0
            for first in lines:
                delta_t, eta_t = first
                cross = delta_t * g_z - eta_t * g_m
                expected = determinant(first, second) * generator
                assert cross == expected
                assert (cross == 0) == (first == second)
                checks += 1

    for first in lines:
        for second in lines:
            for third in lines:
                adjacent_zero = (
                    determinant(first, second) == 0 and determinant(second, third) == 0
                )
                assert adjacent_zero == (first == second == third)
    assert (1, 0) in lines
    assert (0, 1) in lines
    return checks, len(lines)


def audit_target_identity():
    values = (
        (Fraction(2), Fraction(3), Fraction(5), Fraction(7)),
        (Fraction(-1), Fraction(4), Fraction(-3), Fraction(2)),
        (Fraction(1), Fraction(0), Fraction(0), Fraction(1)),
        (Fraction(0), Fraction(1), Fraction(1), Fraction(0)),
    )
    checks = 0
    for delta_s, eta_s, delta_t, eta_t in values:
        generator = Fraction(11, 5)
        alpha = Fraction(13, 7)
        diagonal = Fraction(-17, 3)
        pure = diagonal * generator / alpha
        cross = determinant((delta_t, eta_t), (delta_s, eta_s)) * generator
        left = diagonal * cross
        right = determinant((delta_t, eta_t), (delta_s, eta_s)) * alpha * pure
        assert left == right
        checks += 1
    return checks


def main():
    matching_counts = audit_matching_bijections()
    projective_checks, line_count = audit_projective_transport()
    target_checks = audit_target_identity()
    print("independent physical pair-companion audit: PASS")
    print("orders and pair targets:", matching_counts)
    print("projective lines/checks:", line_count, projective_checks)
    print("target-coupling cases:", target_checks)
    print("scope: transport membership and node closure remain unproved")


if __name__ == "__main__":
    main()
