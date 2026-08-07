# Complete classification of the all-pair `(2,1,1)` triangle cell

## Status

**Exact characteristic-zero component-exhaustion theorem for one coarse
cell.**  Every nonzero pure `P_4` restriction with all six pair-product ranks
at least three and a selected exceptional triangle of relation-rank word
`(2,1,1)` lies in a certified component closure.  The classification exposes
one new five-dimensional orbit, the unequal-complement common-kernel
component twenty-two.  No other orbit occurs in this cell.

Together with the previous five resolved coarse cells and the completed
`triangle-(1,1,1)` cell, this leaves exactly the two star cells `(2,1,1)` and
`(1,1,1)` open in the eight-cell all-pair reduction.  Special/projective
`P_5` fibres and the arbitrary-order local-to-global step remain separate;
the Krenn--Gu conjecture is **UNRESOLVED**.

## Six Borel flag orbits

Put the rank-two relation on edge `12` and the rank-one edges on `13,23`.
In pure kernel/active bases, a rank-one relation cannot use the active row at
both endpoints, because it would kill the nonzero all-active coefficient.
At a leaf--centre edge there are therefore three flags:

```text
A=(leaf kernel, centre kernel),
B=(leaf kernel, centre active),
C=(leaf active, centre kernel).                    (1)
```

Swapping leaves one and two makes the pair of flags unordered.  Hence the
complete list is

```text
AA, AB, AC, BB, BC, CC.                            (2)
```

Support-one exact products are handled first by the support-one reduction:
they are lower-pair or embedded-`P_3`.  On genuine support two, the six rows
of (2) route as follows.

| flag | intrinsic orientation | exact placement |
|---|---|---|
| `AA` | common-kernel `YY` | dense polarity obstruction; projective survivor in component 13 |
| `AB` | radical crossed | empty on the all-pair locus |
| `AC` | common-kernel `YX` | factorization obstruction, hence empty |
| `BB` | common-active | components 11 or 12, or lower-pair |
| `BC` | crossed | component 1, embedded-`P_3`, or lower-pair |
| `CC` | common-kernel active/active | component 13 on equal complements; component 22 on unequal complements; remaining faces lower-pair, embedded-`P_3`, or zero |

The exact source theorems are:

- [`P4_SUPPORT_ONE_211_TRIANGLE_REDUCTION.md`](../../../../../P4_SUPPORT_ONE_211_TRIANGLE_REDUCTION.md);
- [`P4_COMMON_KERNEL_YY_211_TRIANGLE_OBSTRUCTION.md`](../../../../../P4_COMMON_KERNEL_YY_211_TRIANGLE_OBSTRUCTION.md) and [`P4_COMMON_KERNEL_YY_211_TRIANGLE_PROJECTIVE_CLASSIFICATION.md`](../common-kernel-yy-211-triangle-projective/P4_COMMON_KERNEL_YY_211_TRIANGLE_PROJECTIVE_CLASSIFICATION.md);
- [`P4_RADICAL_CROSSED_211_TRIANGLE_OBSTRUCTION.md`](../../../../../P4_RADICAL_CROSSED_211_TRIANGLE_OBSTRUCTION.md);
- [`P4_COMMON_KERNEL_YX_211_FACTORISATION_OBSTRUCTION.md`](../../../../../P4_COMMON_KERNEL_YX_211_FACTORISATION_OBSTRUCTION.md);
- [`P4_TRANSVERSE_COMMON_FACTOR_COMPONENT.md`](../../../../../P4_TRANSVERSE_COMMON_FACTOR_COMPONENT.md) and [`P4_COMMON_ACTIVE_211_TRIANGLE_PROJECTIVE_BOUNDARY_CLASSIFICATION.md`](../common-active-211-triangle-projective-boundary/P4_COMMON_ACTIVE_211_TRIANGLE_PROJECTIVE_BOUNDARY_CLASSIFICATION.md);
- [`P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md`](../crossed-211-triangle-support/P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md);
- [`P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT.md`](../../../../../P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT.md) and [`P4_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT.md`](../../../../../P4_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT.md).

Each source theorem keeps its own lower-pair and projective hypotheses
explicit.  Their union covers (1)--(2), so no unproved density argument is
being used in this aggregate conclusion.

## Replay

```text
python claims/p4/classifications/triangle-211/211-triangle-complete/verify_p4_211_triangle_complete_classification.py
python claims/p4/classifications/triangle-211/211-triangle-complete/audit_p4_211_triangle_complete_classification.py
```

The primary replay checks the complete flag-orbit enumeration and validates
the exact status markers in every source theorem.  The audit independently
reconstructs the three allowed endpoint flags and their six leaf-swap
orbits.  These constant combinatorial checks organize, but do not replace,
the cited characteristic-zero symbolic proofs.
