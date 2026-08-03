# Four-window tetrahedral pair tomography

## Status

**Exact characteristic-zero reconstruction theorem.**  Marked-star data from
three clean four-windows can recover at most five of the six pair faces of a
chosen window.  Four windows already suffice.

More precisely, take the target window `1234` and the three fan windows

```text
1256, 1356, 1456.                                    (1)
```

Every one of the six target pair weights on `1234` is an explicit linear
combination of their marked-star observations, with every nuisance edge
cancelled.  Together with the three-window no-go theorem, this makes four the
minimal number of clean windows in the marked-star sensor model.

This is a positive observability theorem, not a proof that a hypothetical
`P_7` witness legally supplies the four windows in (1).  No graph, support,
alignment, or colour-word enumeration is used.

## 1. The marked-star sensor

Let `x_ij=x_ji` be a weight on every pair of the six double blockers.  For a
four-window `W` and `i in W`, write

```text
s_W(i)=sum_(j in W\{i}) x_ij.                         (2)
```

These are exactly the marked-star observations.  On the target window put

```text
s_i=s_1234(i),  i=1,2,3,4.                           (3)
```

For `ab in {12,13,14}`, the fan window `ab56` gives the alternating shore
functional

```text
d_ab=(s_ab56(a)+s_ab56(b)-s_ab56(5)-s_ab56(6))/2
    =x_ab-x_56.                                       (4)
```

All four spokes from `{a,b}` to `{5,6}` cancel termwise.  The common nuisance
edge `x_56` then cancels between fan windows, so

```text
p=d_12-d_13=x_12-x_13,
q=d_12-d_14=x_12-x_14.                               (5)
```

Thus the three fan windows supply precisely the two cycle-defect directions
missing from the four unsigned vertex degrees of `K_4`.

## 2. Closed reconstruction

Equations (3)--(5) give

```text
x_12=(s_1+p+q)/3,
x_13=x_12-p,
x_14=x_12-q.                                         (6)
```

Set

```text
A=s_2-x_12,   B=s_3-x_13,   C=s_4-x_14.              (7)
```

The remaining triangle is then

```text
x_23=(A+B-C)/2,
x_24=(A+C-B)/2,
x_34=(B+C-A)/2.                                      (8)
```

Every expression in (6)--(8) is a linear combination of marked-star data
from the four windows (1), and (4)--(5) prove that no nuisance pair survives.
The only denominators are `2` and `3`.

### Theorem 1 (tetrahedral pair tomography)

Over a field of characteristic different from `2` and `3`, the marked-star
observations on

```text
1234, 1256, 1356, 1456                              (9)
```

recover all six pair weights on `1234` while cancelling all nine pair weights
outside `1234`.

Proof.  Identity (4) follows by expanding four vertex degrees.  Equations
(5)--(8) then solve the target `K_4` explicitly.

## 3. Rank certificate and minimality

Let `M` be the `16 x 15` observation matrix for (9), and let `M_N` be its
nine nuisance columns.  Exact integer elimination gives

```text
rank M=14,                 rank M_N=8,
rank M-rank M_N=6.                                     (10)
```

A `14 x 14` minor of `M` has determinant `-12`, while an `8 x 8` minor of
`M_N` has determinant `2`.  The formulas above give the matching upper bounds
and identify the six-dimensional recovered target quotient directly.

The three-window theorem proves that any three four-windows recover at most
five target pair directions.  Hence four is minimal in this sensor model.
This minimality is symbolic: it uses the previously proved constant
selector-matroid classification, not a census of physical graphs or supports.

## 4. Consequence for the P7 legality problem

For the canonical blocker profile

```text
012, 01,01, 02,02, 12,12,                            (11)
```

all four windows in (9) lie on the six double blockers and avoid the unique
triple blocker.  Therefore the missing partition-closed pair layer would be
observable if one target shore and the three fan shores could be exposed
with compatible marked-star coefficients.

This replaces an open-ended search for lower faces by one concrete legal
forcing problem:

```text
force a common outside pair {5,6} and three clean fan windows
whose inside pairs are {1,2}, {1,3}, {1,4}.           (12)
```

The theorem does not assert that three pure colours provide those four
windows, that their selector normalizations are compatible, or that the empty
face is already exposed.  It reconstructs exactly the six pair faces once
the four marked-star sensors are legal.

## Scope wall

```text
three clean marked-star windows:       at most five pair directions;
four tetrahedral-fan windows:           all six pair directions, exact;
minimal marked-star window count:       FOUR;
nuisance pair cancellation:             COMPLETE;
legal forcing of the fourth P7 window: UNKNOWN;
empty-face observability:               UNKNOWN;
partition-closed P7 response window:    UNKNOWN;
P7 nonrestriction:                      UNKNOWN;
global Krenn--Gu conjecture:            UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_p7_four_clean_window_tetrahedral_pair_tomography.py
python audit_p7_four_clean_window_tetrahedral_pair_tomography.py
python -m py_compile verify_p7_four_clean_window_tetrahedral_pair_tomography.py audit_p7_four_clean_window_tetrahedral_pair_tomography.py
uv run --with ruff ruff check verify_p7_four_clean_window_tetrahedral_pair_tomography.py audit_p7_four_clean_window_tetrahedral_pair_tomography.py
```

The primary replay verifies the polynomial identities, recovered coordinates,
ranks, and displayed minors.  The independent no-import audit repeats the
calculation with rational row reduction and basis-vector reconstruction.

