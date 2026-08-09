"""Independent no-import audit of the four-residual even Wick tower theorem."""

PORT_COUNT = 6
RESIDUAL_COUNT = 4
TOTAL_COUNT = PORT_COUNT + RESIDUAL_COUNT


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for mask, coefficient in polynomial.items():
            result[mask] = result.get(mask, 0) + coefficient
    return {mask: coefficient for mask, coefficient in result.items() if coefficient}


def scale(polynomial, scalar):
    return add({mask: scalar * coefficient for mask, coefficient in polynomial.items()})


def multiply(left, right):
    result = {}
    for left_mask, left_coefficient in left.items():
        for right_mask, right_coefficient in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = (
                result.get(mask, 0) + left_coefficient * right_coefficient
            )
    return add(result)


def inverse_unit(polynomial):
    assert polynomial.get(0) == 1
    nilpotent = add(polynomial, {0: -1})
    result = {0: 1}
    power = {0: 1}
    for degree in range(1, PORT_COUNT + 1):
        power = multiply(power, nilpotent)
        result = add(result, scale(power, -1 if degree % 2 else 1))
    assert multiply(polynomial, result) == {0: 1}
    return result


PORT_EDGES = {
    (left, right): 1 + left + 2 * right
    for left in range(PORT_COUNT)
    for right in range(left + 1, PORT_COUNT)
}
RESIDUAL_EDGES = {
    (left, right): 2 + 3 * left - right
    for left in range(RESIDUAL_COUNT)
    for right in range(left + 1, RESIDUAL_COUNT)
}
INCIDENCE = tuple(
    tuple(1 + residual + port + residual * port for port in range(PORT_COUNT))
    for residual in range(RESIDUAL_COUNT)
)


def edge_weight(left, right):
    if left > right:
        left, right = right, left
    if right < PORT_COUNT:
        return PORT_EDGES[(left, right)]
    if left >= PORT_COUNT:
        return RESIDUAL_EDGES[(left - PORT_COUNT, right - PORT_COUNT)]
    return INCIDENCE[right - PORT_COUNT][left]


HAFNIAN_CACHE = {0: 1}


def hafnian(mask):
    if mask in HAFNIAN_CACHE:
        return HAFNIAN_CACHE[mask]
    if mask.bit_count() % 2:
        return 0
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    remainder = mask ^ first_bit
    value = 0
    partners = remainder
    while partners:
        partner_bit = partners & -partners
        partner = partner_bit.bit_length() - 1
        value += edge_weight(first, partner) * hafnian(remainder ^ partner_bit)
        partners ^= partner_bit
    HAFNIAN_CACHE[mask] = value
    return value


def response(residual_mask):
    shifted_residuals = residual_mask << PORT_COUNT
    return {
        port_mask: hafnian(port_mask | shifted_residuals)
        for port_mask in range(1 << PORT_COUNT)
        if (port_mask.bit_count() + residual_mask.bit_count()) % 2 == 0
        and hafnian(port_mask | shifted_residuals)
    }


def linear(residual):
    return {1 << port: INCIDENCE[residual][port] for port in range(PORT_COUNT)}


def complement(pair):
    return tuple(vertex for vertex in range(4) if vertex not in pair)


def fixed_graph_audit():
    moment = response(0)
    inverse_moment = inverse_unit(moment)
    pairs = tuple(
        (left, right) for left in range(4) for right in range(left + 1, 4)
    )
    pair_decks = {
        pair: response((1 << pair[0]) | (1 << pair[1])) for pair in pairs
    }
    top_deck = response((1 << 4) - 1)
    loops = tuple(linear(residual) for residual in range(4))

    corrected = {}
    pair_products = {}
    for pair in pairs:
        normalized = multiply(inverse_moment, pair_decks[pair])
        edge = RESIDUAL_EDGES[pair]
        assert normalized.get(0, 0) == edge
        pair_products[pair] = multiply(loops[pair[0]], loops[pair[1]])
        assert add(normalized, {0: -edge}) == pair_products[pair]
        corrected[pair] = add(pair_decks[pair], scale(moment, -edge))

    products = (
        multiply(pair_products[(0, 1)], pair_products[(2, 3)]),
        multiply(pair_products[(0, 2)], pair_products[(1, 3)]),
        multiply(pair_products[(0, 3)], pair_products[(1, 2)]),
    )
    assert products[0] == products[1] == products[2]

    residual_hafnian = (
        RESIDUAL_EDGES[(0, 1)] * RESIDUAL_EDGES[(2, 3)]
        + RESIDUAL_EDGES[(0, 2)] * RESIDUAL_EDGES[(1, 3)]
        + RESIDUAL_EDGES[(0, 3)] * RESIDUAL_EDGES[(1, 2)]
    )
    predicted = add(
        scale(multiply(moment, moment), residual_hafnian),
        multiply(
            moment,
            add(
                *(
                    scale(corrected[complement(pair)], RESIDUAL_EDGES[pair])
                    for pair in pairs
                )
            ),
        ),
        multiply(corrected[(0, 1)], corrected[(2, 3)]),
    )
    assert multiply(moment, top_deck) == predicted

    perturbed_top = add(top_deck, {15: 1})
    assert multiply(moment, perturbed_top) != predicted
    print("independent fixed-graph even tower and perturbed-top obstruction: PASS")


def pentad(values):
    def k(left, right):
        return values[tuple(sorted((left, right)))]

    return (
        k(0, 1) * k(0, 2) * k(1, 3) * k(2, 4) * k(3, 4)
        - k(0, 1) * k(0, 2) * k(1, 4) * k(2, 3) * k(3, 4)
        - k(0, 1) * k(0, 3) * k(1, 2) * k(2, 4) * k(3, 4)
        + k(0, 1) * k(0, 3) * k(1, 4) * k(2, 3) * k(2, 4)
        + k(0, 1) * k(0, 4) * k(1, 2) * k(2, 3) * k(3, 4)
        - k(0, 1) * k(0, 4) * k(1, 3) * k(2, 3) * k(2, 4)
        + k(0, 2) * k(0, 3) * k(1, 2) * k(1, 4) * k(3, 4)
        - k(0, 2) * k(0, 3) * k(1, 3) * k(1, 4) * k(2, 4)
        - k(0, 2) * k(0, 4) * k(1, 2) * k(1, 3) * k(3, 4)
        + k(0, 2) * k(0, 4) * k(1, 3) * k(1, 4) * k(2, 3)
        - k(0, 3) * k(0, 4) * k(1, 2) * k(1, 4) * k(2, 3)
        + k(0, 3) * k(0, 4) * k(1, 2) * k(1, 3) * k(2, 4)
    )


def incomplete_equations_control():
    cycle = {(0, 1), (0, 2), (1, 3), (2, 4), (3, 4)}
    values = {}
    for left in range(5):
        for right in range(left + 1, 5):
            values[(left, right)] = int((left, right) in cycle)
    assert pentad(values) == 1
    print("independent five-port nonfactorization control: PASS")


def main():
    fixed_graph_audit()
    incomplete_equations_control()
    print("four-residual even Wick tower independent audit: PASS")


if __name__ == "__main__":
    main()
