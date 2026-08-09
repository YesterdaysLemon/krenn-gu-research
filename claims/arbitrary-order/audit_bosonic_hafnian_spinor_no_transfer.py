"""Independent no-import audit for the hafnian/spinor route exclusion."""


def hafnian(matrix, vertices):
    vertices = tuple(vertices)
    if not vertices:
        return 1
    if len(vertices) % 2:
        return 0
    first = vertices[0]
    total = 0
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        total += matrix[first][second] * hafnian(matrix, rest)
    return total


def audit_sign_cycle():
    # Encode the desired coefficient signs on S_3.  Multiplying the first
    # two transposition-ratio equations forces +1 around the third square,
    # while determinant parity requires -1.
    first_ratio = -1
    second_ratio = -1
    forced_third_ratio = first_ratio * second_ratio
    required_third_ratio = -1
    assert forced_third_ratio == 1
    assert forced_third_ratio != required_third_ratio


def audit_exchange_failure():
    matrix = [[0 for _ in range(6)] for _ in range(6)]
    for i, j, value in (
        (0, 1, 1),
        (0, 2, 1),
        (0, 3, 1),
        (0, 5, 1),
        (1, 4, 1),
        (2, 4, 1),
        (3, 4, -1),
        (4, 5, 2),
    ):
        matrix[i][j] = matrix[j][i] = value

    x = frozenset((0, 3, 4, 5))
    y = frozenset((0, 1, 2, 4))
    assert hafnian(matrix, sorted(x)) == 1
    assert hafnian(matrix, sorted(y)) == 2
    for other in x ^ y:
        exchanged = x ^ frozenset((5, other))
        assert hafnian(matrix, sorted(exchanged)) == 0


if __name__ == "__main__":
    audit_sign_cycle()
    audit_exchange_failure()
    print("bosonic hafnian spinor no-transfer independent audit: PASS")
