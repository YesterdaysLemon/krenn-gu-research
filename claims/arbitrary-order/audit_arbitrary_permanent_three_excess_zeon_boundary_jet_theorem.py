"""Independent no-import audit of the zeon boundary jet identity."""


class Zeon:
    def __init__(self, terms=None):
        self.terms = {
            key: value
            for key, value in (terms or {}).items()
            if value
        }

    @staticmethod
    def constant(value):
        return Zeon({(0, 0): value})

    @staticmethod
    def u(index):
        return Zeon({(1 << index, 0): 1})

    @staticmethod
    def v(index):
        return Zeon({(0, 1 << index): 1})

    def __add__(self, other):
        answer = dict(self.terms)
        for key, value in other.terms.items():
            answer[key] = answer.get(key, 0) + value
            if answer[key] == 0:
                del answer[key]
        return Zeon(answer)

    def __mul__(self, other):
        answer = {}
        for (u_left, v_left), left_value in self.terms.items():
            for (u_right, v_right), right_value in other.terms.items():
                if u_left & u_right or v_left & v_right:
                    continue
                key = (u_left | u_right, v_left | v_right)
                answer[key] = answer.get(key, 0) + left_value * right_value
        return Zeon(answer)

    def coefficient(self, u_mask, v_mask):
        return self.terms.get((u_mask, v_mask), 0)


def permutations(values):
    if not values:
        return [()]
    answer = []
    for index, value in enumerate(values):
        remainder = values[:index] + values[index + 1 :]
        for tail in permutations(remainder):
            answer.append((value,) + tail)
    return answer


def permanent(matrix):
    if not matrix:
        return 1
    answer = None
    for permutation in permutations(tuple(range(len(matrix)))):
        term = matrix[0][permutation[0]]
        for row in range(1, len(matrix)):
            term = term * matrix[row][permutation[row]]
        answer = term if answer is None else answer + term
    return answer


def numeric_permanent(matrix):
    if not matrix:
        return 1
    return sum(
        product(matrix[row][permutation[row]] for row in range(len(matrix)))
        for permutation in permutations(tuple(range(len(matrix))))
    )


def product(values):
    answer = 1
    for value in values:
        answer *= value
    return answer


def minor(matrix, deleted_row, deleted_column):
    return [
        [value for column, value in enumerate(row) if column != deleted_column]
        for row_index, row in enumerate(matrix)
        if row_index != deleted_row
    ]


def as_zeon_matrix(matrix):
    return [[Zeon.constant(value) for value in row] for row in matrix]


def main():
    x = [[2, 3], [5, 7]]
    y = [[11, 13], [17, 19]]
    z = [[23, 29], [31, 37]]
    w = [[41, 43], [47, 53]]

    u = [Zeon.u(0), Zeon.u(1)]
    v = [Zeon.v(0), Zeon.v(1)]
    jet_matrix = as_zeon_matrix(w)
    for r in range(2):
        for q in range(2):
            z_v = Zeon.constant(0)
            u_y = Zeon.constant(0)
            for j in range(2):
                z_v = z_v + Zeon.constant(z[r][j]) * v[j]
            for i in range(2):
                u_y = u_y + u[i] * Zeon.constant(y[i][q])
            jet_matrix[r][q] = jet_matrix[r][q] + z_v * u_y

    jet = permanent(jet_matrix)
    assert jet.coefficient(0, 0) == numeric_permanent(w)

    responses = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            for q in range(2):
                for r in range(2):
                    responses[i][j] += (
                        y[i][q]
                        * numeric_permanent(minor(w, r, q))
                        * z[r][j]
                    )
            assert jet.coefficient(1 << i, 1 << j) == responses[i][j]

    assert jet.coefficient(3, 3) == 2 * numeric_permanent(y) * numeric_permanent(z)

    full = [x[0] + y[0], x[1] + y[1], z[0] + w[0], z[1] + w[1]]
    reconstructed = numeric_permanent(x) * jet.coefficient(0, 0)
    for i in range(2):
        for j in range(2):
            reconstructed += minor(x, i, j)[0][0] * jet.coefficient(1 << i, 1 << j)
    reconstructed += jet.coefficient(3, 3) // 2
    assert reconstructed == numeric_permanent(full)

    # Independent degree-three factorial in the rank-one zeon update.
    u3 = [Zeon.u(index) for index in range(3)]
    v3 = [Zeon.v(index) for index in range(3)]
    rank_one = [[v3[row] * u3[column] for column in range(3)] for row in range(3)]
    assert permanent(rank_one).coefficient(7, 7) == 6

    print("independent no-import zeon boundary jet audit: PASS")
    print("integer square-zero algebra, full block reconstruction, and 3! top layer")


if __name__ == "__main__":
    main()
