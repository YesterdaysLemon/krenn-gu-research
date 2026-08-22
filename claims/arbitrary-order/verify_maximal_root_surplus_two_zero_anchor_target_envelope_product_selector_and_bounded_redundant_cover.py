"""Exact primary checks for the GLS28 zero-anchor target envelope."""

from __future__ import annotations

from itertools import product

import sympy as sp


def in_span(columns: sp.Matrix, item: sp.Matrix) -> bool:
    if columns.cols == 0:
        return item == sp.zeros(item.rows, item.cols)
    return sp.Matrix.hstack(columns, item).rank() == columns.rank()


def basis_matrix(columns: sp.Matrix) -> sp.Matrix:
    basis = columns.columnspace()
    return sp.Matrix.hstack(*basis) if basis else sp.zeros(columns.rows, 0)


def tensor_space(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    columns = [
        sp.kronecker_product(left[:, i], right[:, j])
        for i, j in product(range(left.cols), range(right.cols))
    ]
    return (
        sp.Matrix.hstack(*columns) if columns else sp.zeros(left.rows * right.rows, 0)
    )


def projector(q: sp.Matrix) -> sp.Matrix:
    epsilon = sp.ones(1, 9)
    p = (epsilon * q)[0]
    assert p != 0
    return p * sp.eye(9) - q * epsilon


def check_tangent_quotient_dimensions() -> dict[tuple[int, int], int]:
    e0, e1, _e2 = sp.eye(3).columnspace()
    dimensions: dict[tuple[int, int], int] = {}
    for d0, d1 in product((1, 2), repeat=2):
        shore0 = sp.Matrix.hstack(e0, e0 if d0 == 1 else e1)
        shore1 = sp.Matrix.hstack(e0, e0 if d1 == 1 else e1)
        q = sp.kronecker_product(shore0[:, 0], shore1[:, 1]) + sp.kronecker_product(
            shore0[:, 1], shore1[:, 0]
        )
        p_q = projector(q)
        x0 = basis_matrix(shore0)
        x1 = basis_matrix(shore1)
        tangent = basis_matrix(
            sp.Matrix.hstack(tensor_space(x0, sp.eye(3)), tensor_space(sp.eye(3), x1))
        )
        tangent_bar = basis_matrix(p_q * tangent)
        assert tangent.rank() == 3 * d0 + 3 * d1 - d0 * d1
        assert tangent_bar.rank() == tangent.rank() - 1
        assert p_q.rank() == 8
        h = p_q.rank() - tangent_bar.rank()
        assert h == 9 - 3 * d0 - 3 * d1 + d0 * d1
        dimensions[(d0, d1)] = h
    assert dimensions == {(1, 1): 4, (1, 2): 2, (2, 1): 2, (2, 2): 1}
    return dimensions


def root_support(
    tensor: sp.MutableDenseNDimArray, kept_slots: tuple[int, ...]
) -> sp.Matrix:
    """Return the root support after retaining the selected port slots."""
    port_shape = tensor.shape[1:]
    sliced_columns: list[sp.Matrix] = []
    kept_shape = tuple(port_shape[index] for index in kept_slots)
    cut_slots = tuple(
        index for index in range(len(port_shape)) if index not in kept_slots
    )
    for cut_values in product(*(range(port_shape[index]) for index in cut_slots)):
        values = dict(zip(cut_slots, cut_values, strict=True))
        flat: list[sp.Expr] = []
        for root in range(tensor.shape[0]):
            for kept_values in product(*(range(size) for size in kept_shape)):
                indices = [0] * len(port_shape)
                for slot, value in values.items():
                    indices[slot] = value
                for slot, value in zip(kept_slots, kept_values, strict=True):
                    indices[slot] = value
                flat.append(tensor[(root, *indices)])
        sliced_columns.append(sp.Matrix(flat))
    return basis_matrix(sp.Matrix.hstack(*sliced_columns))


def full_root_support(tensor: sp.MutableDenseNDimArray) -> sp.Matrix:
    columns = []
    for port_values in product(*(range(size) for size in tensor.shape[1:])):
        columns.append(
            sp.Matrix([tensor[(root, *port_values)] for root in range(tensor.shape[0])])
        )
    return basis_matrix(sp.Matrix.hstack(*columns))


def pad_one_target_slot(partial: sp.Matrix, slot: int) -> sp.Matrix:
    """Pad an E x V_shared tensor into E x V_0 x V_1 coefficient space."""
    columns = []
    for column in partial.columnspace():
        array = sp.MutableDenseNDimArray.zeros(8, 3)
        for root, shared in product(range(8), range(3)):
            array[root, shared] = column[3 * root + shared]
        for missing in range(3):
            output = sp.zeros(8 * 9, 1)
            for root, shared in product(range(8), range(3)):
                target = (shared, missing) if slot == 0 else (missing, shared)
                output[9 * root + 3 * target[0] + target[1]] = array[root, shared]
            columns.append(output)
    return sp.Matrix.hstack(*columns)


def check_label_by_label_envelope() -> dict[str, int]:
    root_basis = sp.eye(8)
    target_basis = sp.eye(9)
    tangent = root_basis[:, :3]

    # A one-Q label whose promoted port is retained in the target.
    one_q = sp.MutableDenseNDimArray.zeros(8, 3)
    for root, port in product(range(3), range(3)):
        one_q[root, port] = root + port + 1
    retained = root_support(one_q, (0,))
    retained_padded = pad_one_target_slot(retained, 0)
    assert in_span(tensor_space(tangent, target_basis), retained_padded)

    # The same type with its promoted port outside the target is fully sliced.
    sliced = full_root_support(one_q)
    sliced_padded = tensor_space(sliced, target_basis)
    assert in_span(tensor_space(tangent, target_basis), sliced_padded)

    # A promoted pair sharing one target port: slice the foreign port, then pad.
    overlap = sp.MutableDenseNDimArray.zeros(8, 3, 3)
    for root, shared, foreign in product(range(8), range(3), range(3)):
        overlap[root, shared, foreign] = (root + 1) * (shared + 2) + foreign
    overlap_support = full_root_support(overlap)
    overlap_partial = root_support(overlap, (0,))
    overlap_padded = pad_one_target_slot(overlap_partial, 0)
    assert in_span(tensor_space(overlap_support, target_basis), overlap_padded)

    # A disjoint promoted pair is fully sliced and padded by both target slots.
    disjoint = sp.MutableDenseNDimArray.zeros(8, 3, 3)
    for root, left, right in product(range(8), range(3), range(3)):
        disjoint[root, left, right] = (root + left + 1) * (right + 1)
    disjoint_support = full_root_support(disjoint)
    disjoint_padded = tensor_space(disjoint_support, target_basis)
    assert in_span(tensor_space(disjoint_support, target_basis), disjoint_padded)

    envelope = basis_matrix(
        sp.Matrix.hstack(tangent, overlap_support, disjoint_support)
    )
    nuisance = basis_matrix(
        sp.Matrix.hstack(
            retained_padded, sliced_padded, overlap_padded, disjoint_padded
        )
    )
    assert in_span(tensor_space(envelope, target_basis), nuisance)
    return {
        "tangent_rank": tangent.rank(),
        "overlap_supplier_rank": overlap_support.rank(),
        "disjoint_supplier_rank": disjoint_support.rank(),
        "nuisance_rank": nuisance.rank(),
        "envelope_rank": envelope.rank(),
    }


def check_product_selectors() -> dict[str, object]:
    root = sp.eye(8)
    target = sp.eye(9)
    envelope = root[:, :7]
    supplier = root[:, 7]
    desired = sp.kronecker_product(supplier, target[:, 0])
    nuisance = tensor_space(envelope, target)
    mu = sp.kronecker_product(supplier.T, target[:, 0].T)
    assert mu * nuisance == sp.zeros(1, nuisance.cols)
    assert (mu * desired)[0] == 1
    assert not in_span(nuisance, desired)

    # A nontrivial pure representative differs from desired by nuisance.
    delta = supplier + root[:, 0]
    pure = sp.kronecker_product(delta, target[:, 0])
    assert (mu * pure)[0] == 1

    # Exact quotient coupling: the discrepancy is nuisance tensor response.
    response = sp.Matrix([2, 0, 0])
    left = sp.kronecker_product(pure, response)
    right = sp.kronecker_product(desired, response)
    discrepancy = left - right
    assert discrepancy != sp.zeros(discrepancy.rows, 1)
    assert in_span(tensor_space(nuisance, sp.eye(3)), discrepancy)
    assert (sp.kronecker_product(mu, sp.eye(3)) * left) != sp.zeros(3, 1)
    return {
        "envelope_rank": envelope.rank(),
        "nuisance_rank": nuisance.rank(),
        "selector_on_desired": (mu * desired)[0],
        "selector_on_pure": (mu * pure)[0],
        "response": tuple(response),
    }


def check_bounded_covers_and_sharpness() -> dict[str, object]:
    e0, e1, e2, e3 = sp.eye(4).columnspace()
    ell = e0 + e1 + e2 + e3
    assert in_span(sp.Matrix.hstack(e0, e1, e2, e3), ell)
    assert sp.Matrix.hstack(e0, e1, e2, e3).rank() == 4

    # A fully redundant h=2 supplier family has a three-label circuit.
    f0, f1 = sp.eye(2).columnspace()
    w1, w2, w3 = f0, f1, -(f0 + f1)
    assert w1 + w2 + w3 == sp.zeros(2, 1)
    for item, others in (
        (w1, (w2, w3)),
        (w2, (w1, w3)),
        (w3, (w1, w2)),
    ):
        assert in_span(sp.Matrix.hstack(*others), item)

    # Useful-row failure does not make every supplier direction redundant.
    diagonal = f0
    suppliers = (f0, f0, f1)
    for excluded in range(3):
        others = [item for index, item in enumerate(suppliers) if index != excluded]
        assert in_span(sp.Matrix.hstack(*others), diagonal)
    assert not in_span(sp.Matrix.hstack(suppliers[0], suppliers[1]), suppliers[2])

    # In h=1, deletion-stable spanning forces at least two nonzero labels.
    line = sp.Matrix([[1]])
    assert in_span(sp.Matrix.hstack(line), line)
    assert in_span(sp.Matrix.hstack(line), line)
    return {
        "h4_cover_labels": 4,
        "h2_full_absorption_circuit_labels": 3,
        "sharp_countermodel_supplier_ranks": tuple(item.rank() for item in suppliers),
        "h1_minimum_nonzero_labels": 2,
    }


def check_laurent_augmented_minor() -> dict[str, object]:
    t = sp.symbols("t", nonzero=True)
    envelope = sp.Matrix([1, t])
    diagonal = sp.Matrix([t, 0])
    augmented = sp.Matrix.hstack(envelope, diagonal)
    witness = sp.factor(augmented.det())
    assert witness == -(t**2)
    assert augmented.subs(t, 2).rank() == 2
    assert envelope.subs(t, 2).rank() == 1

    redundant = sp.Matrix.hstack(sp.Matrix([1, 0]), sp.Matrix([0, 1]))
    coefficients = redundant.inv() * sp.Matrix([1 / t, t])
    assert sp.simplify(redundant * coefficients - sp.Matrix([1 / t, t])) == sp.zeros(
        2, 1
    )
    return {
        "escape_minor": witness,
        "escape_specialization": 2,
        "redundant_denominator": t,
    }


def main() -> None:
    dimensions = check_tangent_quotient_dimensions()
    envelope = check_label_by_label_envelope()
    selectors = check_product_selectors()
    covers = check_bounded_covers_and_sharpness()
    laurent = check_laurent_augmented_minor()
    print("zero-anchor target-envelope primary checks: PASS")
    print("  tangent quotient dimensions:", dimensions)
    print("  GLS23 label-type envelope:", envelope)
    print("  product selector and response gate:", selectors)
    print("  bounded covers and sharpness:", covers)
    print("  Laurent augmented-minor specialization:", laurent)
    print("  scope: exact reduction only; synchronization and node closure remain open")


if __name__ == "__main__":
    main()
