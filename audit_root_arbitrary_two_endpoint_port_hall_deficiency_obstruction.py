"""Independent no-import audit of the odd-gadget two-port Hall defect."""

from __future__ import annotations

from itertools import permutations


def port_entry(blocker_count: int, family: int, column: int, colour: int) -> int:
    if column == 0 and colour == 0:
        return 1
    if column == 1 and colour == 2:
        return 1
    if column == blocker_count - 1 and colour == 1:
        return 1 if family == 0 else -1
    return 0


def assignment_sum(blocker_count: int, colour: int) -> tuple[int, int]:
    assignments = 0
    coefficient_sum = 0
    for u, v in permutations(range(blocker_count), 2):
        coefficient = (
            port_entry(blocker_count, 0, u, colour)
            * port_entry(blocker_count, 1, v, colour)
        )
        if coefficient:
            assignments += 1
            coefficient_sum += coefficient
    return assignments, coefficient_sum


def mixed_control(blocker_count: int) -> int:
    # Column 0 has colour 0 and column 1 colour 2.  The two port assignments
    # both survive and have coefficient one.
    return (
        port_entry(blocker_count, 0, 0, 0)
        * port_entry(blocker_count, 1, 1, 2)
        + port_entry(blocker_count, 1, 0, 0)
        * port_entry(blocker_count, 0, 1, 2)
    )


def main() -> None:
    cases = 0
    pure_checks = 0
    for blocker_count in range(5, 26, 2):
        for colour in range(3):
            assignments, coefficient = assignment_sum(blocker_count, colour)
            if assignments != 0 or coefficient != 0:
                raise AssertionError((blocker_count, colour, assignments, coefficient))
            pure_checks += 1
        if mixed_control(blocker_count) != 2:
            raise AssertionError(blocker_count)
        cases += 1
    print("PASS: independent two-port Hall-deficiency audit")
    print(f"odd blocker counts: {cases}")
    print(f"pure-colour assignment checks: {pure_checks}")
    print("mixed two-port assignment control: 2")
    print("finite-field proof used: no")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
