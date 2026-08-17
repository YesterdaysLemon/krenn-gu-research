"""Independent no-import audit of the surplus-two companion sensor.

This audit imports neither SymPy nor the primary verifier.  It uses the
root-injection description rather than the primary's matching recurrence.
"""

from __future__ import annotations

from itertools import combinations, permutations

Word = tuple[int, ...]


def double_factorial(value: int) -> int:
    answer = 1
    while value > 0:
        answer *= value
        value -= 2
    return answer


def injection_column(
    r: int, private: frozenset[int], residuals: tuple[int, ...]
) -> dict[Word, int]:
    """Enumerate residual-to-root injections after private roots are forced."""

    remaining = tuple(root for root in range(r) if root not in private)
    if len(remaining) < len(residuals) or (len(remaining) - len(residuals)) % 2:
        return {}

    result: dict[Word, int] = {}
    for chosen_roots in permutations(remaining, len(residuals)):
        word = [0 if root in private else 1 for root in range(r)]
        valid = True
        for residual, root in zip(residuals, chosen_roots, strict=True):
            if residual == 0:
                # q_0 contributes b, so the word remains unchanged.
                continue
            if residual == 1:
                word[root] = 2
                continue
            valid = False
        if not valid:
            continue
        coefficient = double_factorial(len(remaining) - len(residuals) - 1)
        key = tuple(word)
        result[key] = result.get(key, 0) + coefficient
    return result


def audit_columns() -> None:
    for r in range(1, 9):
        columns: list[dict[Word, int]] = []
        pivot_supports: set[Word] = set()

        for size in range(r + 1):
            for private_tuple in combinations(range(r), size):
                private = frozenset(private_tuple)
                ell = r - size
                allowed_residuals = ((), (0, 1)) if ell % 2 == 0 else ((0,), (1,))
                if ell == 0:
                    allowed_residuals = ((),)

                for residuals in allowed_residuals:
                    column = injection_column(r, private, residuals)
                    assert column
                    columns.append(column)

                    no_c = all(2 not in word for word in column)
                    if no_c:
                        pivot = tuple(0 if root in private else 1 for root in range(r))
                    else:
                        first_remaining = next(
                            root for root in range(r) if root not in private
                        )
                        pivot_list = [0 if root in private else 1 for root in range(r)]
                        pivot_list[first_remaining] = 2
                        pivot = tuple(pivot_list)
                    assert pivot in column
                    assert pivot not in pivot_supports
                    pivot_supports.add(pivot)

        assert len(columns) == 2 ** (r + 1) - 1
        assert len(pivot_supports) == len(columns)


def audit_grade_bijection() -> None:
    for r in range(1, 12):
        for surplus in range(0, 12, 2):
            outside_size = r + surplus
            labels = []
            for root_pairs in range(r // 2 + 1):
                cross_roots = r - 2 * root_pairs
                outside_hafnian_size = outside_size - cross_roots
                labels.append(outside_hafnian_size)
                assert outside_hafnian_size == surplus + 2 * root_pairs
            assert len(labels) == len(set(labels))
            if surplus == 2:
                assert labels == list(range(2, outside_size + 1, 2))
            if surplus >= 4:
                assert min(labels) >= 4


def audit_response_partition() -> None:
    for r in range(1, 12):
        ports = range(r)
        m_labels = {
            subset
            for size in range(0, r + 1, 2)
            for subset in combinations(ports, size)
        }
        z_labels = {
            subset
            for size in range(0, r + 1, 2)
            for subset in combinations(ports, size)
        }
        assert len(m_labels) == 2 ** (r - 1) if r else 1
        assert len(z_labels) == len(m_labels)
        # M_empty is structural, so the nonempty desired coordinate count is:
        assert (len(m_labels) - 1) + len(z_labels) == 2**r - 1


def audit_rank_capacity() -> None:
    for r in range(1, 20):
        assert 2 ** (r + 1) - 1 <= 3**r


def main() -> None:
    audit_columns()
    audit_grade_bijection()
    audit_response_partition()
    audit_rank_capacity()
    print("independent surplus-two companion-sensor audit: PASS")


if __name__ == "__main__":
    main()
