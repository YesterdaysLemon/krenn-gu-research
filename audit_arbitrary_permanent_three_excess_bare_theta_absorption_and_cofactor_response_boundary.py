"""Independent no-import audit of the bare-theta response boundary."""


def counts(values):
    answer = {0: 0, 1: 0, 2: 0}
    for value in values:
        answer[value] += 1
    return answer


def main():
    # Exact nonzero bare theta with Z=0: A=1,B=1,C=-2,D=E=F=G=1.
    a, b, c, d, e, f, g = 1, 1, -2, 1, 1, 1, 1
    z = a * e * g + b * d * g + c * e * f
    assert z == 0
    q = (
        (e * g, d * g, e * f),
        (b * g, a * g + c * f, b * f),
        (c * e, c * d, a * e + b * d),
    )
    assert all(entry != 0 for row in q for entry in row)
    assert z * g == q[0][0] * q[1][1] + q[0][1] * q[1][0]
    assert z * e == q[0][0] * q[2][2] + q[0][2] * q[2][0]
    assert z * b == q[1][0] * q[2][2] + q[1][2] * q[2][0]
    assert z * c == q[1][0] * q[2][1] + q[1][1] * q[2][0]
    assert z * d == q[0][1] * q[2][2] + q[0][2] * q[2][1]
    assert z * f == q[0][1] * q[1][2] + q[0][2] * q[1][1]

    h = q[0][1] * q[1][0] * q[2][2] - q[0][2] * q[2][0] * q[1][1]
    assert h == (b * d * g - c * e * f) * z == 0

    mu = 3
    residue_111 = (mu + 0 - 2 * mu, 1 + 1 - 2 * 1)
    assert residue_111 == (-mu, 0)
    assert counts((1, 2, 2, 1, 2)) == counts((2, 1, 2, 1, 2))

    residue_210 = (1 + 1 - 2 * 1, 0 + 1 - 2 * 2)
    assert residue_210 == (0, -3)
    assert counts((1, 0, 1, 0, 1)) == counts((0, 1, 0, 1, 1))

    r11, r12, r21, r22 = 2, 3, 5, 7
    symmetric = r11 * r22 + r12 * r21
    alternating = r11 * r22 - r12 * r21
    assert symmetric + alternating == 2 * r11 * r22
    assert symmetric - alternating == 2 * r12 * r21

    print("independent no-import bare-theta response audit: PASS")
    print("method countercharts are exact; global response bridge remains open")


if __name__ == "__main__":
    main()
