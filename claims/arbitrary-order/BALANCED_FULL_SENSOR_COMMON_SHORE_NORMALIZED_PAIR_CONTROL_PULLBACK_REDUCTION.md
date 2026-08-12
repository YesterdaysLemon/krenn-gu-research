# Balanced full-sensor common-shore normalized pair-control pullback reduction

## Status

**Exact characteristic-zero reduction for the eight normalized `m=3`
full-row controls.**  Every control from the normalized full-row S2M theorem
has the same binary residual gate after projecting the three root colour spaces
away from colour `0`: one singleton slice is a transverse pure tensor, every
other singleton slice vanishes, and the empty companion is one pure tensor in
the other nonzero colour.

Consequently, a common-shore realization of any of the eight controls would
produce a solution of one explicit `2 x 2 x 2` syzygy--permanent system.  The
eight realization questions therefore reduce to one exact residual problem.
This document does **not** prove that residual system empty, and hence does not
prove any of the eight controls nonrealizable.  It also makes no retained-jet
exclusion, physical-graph, witness, or global claim.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## 1. Input and notation

Use the common-shore image theorem at `m=3`.  Thus the root spaces are
three-dimensional spaces `A_i` with basis `e_(i,0),e_(i,1),e_(i,2)`, the
root--root blocks are

```text
B_12 in A_1 tensor A_2,
B_13 in A_1 tensor A_3,
B_23 in A_2 tensor A_3,                              (1)
```

and a singleton slice has the shared-factor form

```text
delta_B(h_1,h_2,h_3)
 = h_1 tensor B_23
   + insert_2(B_13,h_2)
   + B_12 tensor h_3.                               (2)
```

For three cross-block triples `k_x,k_y,k_r`, write their polarized
six-term permanent as

```text
Perm(k_x,k_y,k_r)
 = sum_(sigma in S_3)
     (k_(sigma(x)))_1 tensor
     (k_(sigma(y)))_2 tensor
     (k_(sigma(r)))_3.                              (3)
```

Formula (3) is the coefficient of `x_q y_q r_q` in the empty companion when
the three triples are the colour-`q` cross-block slices.

The eight S2M controls consist of two outside controls, three `x`-endpoint
controls, and three `y`-endpoint controls.  Each has a pivot colour
`a in {1,2}`.  Put

```text
q={1,2}\{a}.                                        (4)
```

Thus `q=2` for `a=1` and `q=1` for `a=2`.

## 2. The common binary pullback

Let

```text
pi_i:A_i -> V_i=span(e_(i,a),e_(i,q))               (5)
```

be the coordinate projection killing `e_(i,0)`.  Apply the corresponding
pair and triple projections to every shore block and every sensor slice.
Equations (2)--(3) commute with these projections because they are sums of
tensor products.  Denote

```text
p_i=pi_i(e_(i,a)),       z_i=pi_i(e_(i,q)).          (6)
```

### Theorem 1 (eight controls, one binary residual)

For each of the eight S2M matrices, the projected singleton and empty columns
have the following common form:

1. exactly one singleton slice is `p_1 tensor p_2 tensor p_3`;
2. all other singleton slices vanish, in particular the three colour-`q`
   slices vanish;
3. the only nonzero coefficient of the projected empty companion is
   `z_1 tensor z_2 tensor z_3`, at nonroot colour word `(q,q,q)`.

Therefore, if any S2M control lies in the common-shore matching-sum image,
then there exist binary blocks

```text
C_12 in V_1 tensor V_2,
C_13 in V_1 tensor V_3,
C_23 in V_2 tensor V_3                              (7)
```

such that, for

```text
D_C(u_1,u_2,u_3)
 =u_1 tensor C_23
  +insert_2(C_13,u_2)
  +C_12 tensor u_3,                                 (8)
```

one has

```text
p_1 tensor p_2 tensor p_3 in image(D_C),            (9)
```

and there are `k_x,k_y,k_r in kernel(D_C)` satisfying

```text
Perm(k_x,k_y,k_r)=z_1 tensor z_2 tensor z_3.         (10)
```

### Proof

The S2M controls start with the three GHZ entries in the empty column and
replace the pivot row `(a,a,a)`.  Hence after (5) the `a`-diagonal empty
coefficient is zero, the colour-`0` diagonal dies, and precisely the
`q`-diagonal coefficient remains.  This proves part 3.

The unique pivot singleton contribution is the coordinate tensor at
`(a,a,a)`, so it survives as `p_1 tensor p_2 tensor p_3`.  Every correction
singleton contribution in the displayed S2M matrices is supported at one of

```text
(0,0,1), (0,1,0), (1,0,0),                          (11)
```

and is therefore killed by (5).  This includes the correction terms in the
mixed endpoint controls `(a,b)=(1,2)`.  No other singleton entry is present.
This proves parts 1--2 for all eight controls.

If an original control had common shore blocks (1), applying (5) to those
blocks and their cross slices would give binary blocks (7).  The surviving
singleton slice yields (9) through (2), while the three vanished colour-`q`
slices put `k_x,k_y,k_r` in `kernel(D_C)`.  Projecting the six-term formula
(3) gives (10).  Thus (9)--(10) are necessary for every one of the eight
realizations.

## 3. The exact residual obligation

The remaining binary question is:

```text
Can image(D_C) contain p_1 tensor p_2 tensor p_3
while three kernel vectors have polarized permanent
z_1 tensor z_2 tensor z_3?                           (12)
```

Closing (12) negatively would exclude all eight *particular* S2M controls
from the common-shore image at once.  It would not prove the universal S2
pair-pole gate, because S2M only supplies eight ambient sharpness controls.
Conversely, a solution of (12) would show only that the binary projection is
compatible; lifting it to all ternary singleton and empty coefficients would
remain necessary.

The tempting inference

```text
three zero singleton slices imply their empty coefficient is zero          (13)
```

is false in general.  Already in one-dimensional root spaces, take all three
root--root blocks equal to `1`.  Then `kernel(D_C)` is the plane
`u_1+u_2+u_3=0`, and three vectors in that plane can have nonzero ordinary
`3 x 3` permanent.  For example, take the three columns of

```text
[  0   3   3 ]
[  1   3   2 ].                                      (14)
[ -1  -6  -5 ]
```

Every column sum is zero, while the permanent is `-48`.  Thus (12) requires
the simultaneous transverse-image condition (9); zero singleton slices alone
do not settle it.

No characteristic-zero proof or counterexample to (12) is asserted here.
Finite-field enumeration or numerical residuals, if used during discovery,
are not evidence for this theorem and do not change that status.

## 4. Proof-topology consequence

The exact boundary is now

```text
eight normalized full-row controls                         PROVED (S2M);
exact m=3 common-shore image formulas                       PROVED (S2N);
common binary pullback and residual (9)--(10)               PROVED HERE;
emptiness or realizability of the binary residual           OPEN;
realizability of any complete ternary S2M control            OPEN;
universal failure on every realized balanced incidence       OPEN.       (15)
```

This reduction preserves the distinction between an ambient target-consistent
matrix and a physical common-shore matching-sum sensor.  It neither supplies
a physical-variable realization nor infers lattice coupling from shared
variables.  All higher-order recurrences, all-pair compatibility, the
all-rank-drop branch, and every unrelated proof-DAG leaf retain their previous
status.  Global Krenn--Gu remains **UNRESOLVED**.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_full_sensor_common_shore_normalized_pair_control_pullback.py
python -I claims/arbitrary-order/audit_balanced_full_sensor_common_shore_normalized_pair_control_pullback.py
python -m py_compile claims/arbitrary-order/verify_balanced_full_sensor_common_shore_normalized_pair_control_pullback.py claims/arbitrary-order/audit_balanced_full_sensor_common_shore_normalized_pair_control_pullback.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_full_sensor_common_shore_normalized_pair_control_pullback.py claims/arbitrary-order/audit_balanced_full_sensor_common_shore_normalized_pair_control_pullback.py
```

The primary replay reconstructs the polynomial coefficient tensors of all
eight displayed S2M matrices, applies the three root projections, and checks
the surviving singleton and empty coefficients exactly with SymPy.  It also
checks the one-dimensional sharpness boundary by an explicit permanent.

The independent audit imports neither SymPy nor repository code.  It rebuilds
the eight controls as integer sparse supports, applies independently written
coordinate projections, and computes the sharp permanent by enumerating the
six permutations directly.
