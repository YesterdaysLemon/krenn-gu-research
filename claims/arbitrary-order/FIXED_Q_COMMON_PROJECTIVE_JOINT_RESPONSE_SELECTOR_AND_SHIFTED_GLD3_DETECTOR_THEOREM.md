# Fixed-Q common projective joint-response selector and shifted GLD3 detector

## Status

**Exact characteristic-zero common-line reduction and conditional mixed
detector at arbitrary residual scalar.**  The joint `M/Z` quotient of `GLD15`
need not have rank two at all seven four-root targets.  It is enough that the
seven exact operator-supply spaces share one nonzero projective coefficient
vector.

For the physical residual scalar `h`, a common vector `(delta,eta)` and the
effective scalar

```text
a=delta+h eta
```

supply the six pair tensors

```text
D_e=delta M_e+eta Z_e=a B_e+eta K_e
```

and the four-port tensor

```text
T'=delta M_U+eta Z_U.
```

They satisfy the denominator-free shifted interference identity

```text
a T'=C(D)-C(eta K).
```

The corrected compound on the right has one-port flattening rank at most two.
Consequently the `GLD3` nine-word determinant applies with effective scalar
`a`.  The divisor `a=0`, including the pure-`Z` line when `h=0`, is a rank
contradiction; when `a!=0`, the detector exposes one of nine mixed selected
four-port coefficients.  Three-colour pair-depth activity therefore
contradicts the pure GHZ target for every value of `h`.

This is strictly weaker than seven joint rank-two quotients.  Rank-two target
spaces impose no constraint on the common line; every rank-one target space
must merely have the same projective slope.  A single zero space or two
distinct rank-one slopes destroy the common package.  Exact two-active
camouflage on the common line `[1:1]` proves that the activity hypothesis is
load-bearing.

**Successor update (2026-08-24).**
[`GLD68`](FOUR_ROOT_COMPLEMENTARY_PAIR_BASE_NUISANCE_SATURATION_AND_SEVEN_SHADOW_SOURCE_EXCLUSION_THEOREM.md)
proves that the six `GLS16` pair base shadows cannot source this all-seven
package: at most one member of each complementary pair survives.  The present
common-line theorem remains valid for rows supplied non-leadingly or through
another interface; only the former `GLS17` all-six base-shadow incoming edge
is removed.

The theorem does not prove that a common line exists on every hypothetical
witness, force selected-response activity, exclude the zero-intersection
branch, integrate a formal response fibre into a graph fibre, or imply a
permanent restriction.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Dependencies:

- [`GLD15`](FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md)
- [`GLD3`](TWO_RESIDUAL_PAIR_FOUR_PORT_DIAGONAL_INTERFERENCE_AND_CAMOUFLAGE_BOUNDARY_THEOREM.md)

## 1. One fixed module and seven exact coefficient spaces

Work over a characteristic-zero field `K`.  Fix one four-root surplus-two
graph, one residual pair `Q={q0,q1}`, one fully specified residual contraction,
and one four-port set

```text
U={1,2,3,4}.                                           (1)
```

Let the contracted residual-edge scalar be

```text
h in K.                                                (2)
```

Retain the complete nonempty even deck module and every nuisance coefficient
slice exactly as in `GLD15`.  For each

```text
S in F_7:=binom(U,2) union {U},                        (3)
```

let

```text
C_S subset K^2                                        (4)
```

be the exact constant-open-port operator-coefficient space.  Thus
`(delta,eta) in C_S` exactly when some constant functional on the full
fixed-`Q` companion equation has operator output

```text
delta P_S^M+eta P_S^Z.                                (5)
```

The coefficient axes and normalization in (4)--(5) are the globally fixed
`M,Z` conventions of `GLD15`.  They may not be changed target by target.
Every `C_S` is one of `0`, a line, or `K^2`.

Define the common coefficient space

```text
C_*:=intersection_(S in F_7) C_S subset K^2.          (6)
```

### Theorem 1 (common projective selector criterion)

The following are equivalent:

1. `C_*!=0`;
2. every `C_S` is nonzero and all rank-one `C_S` are the same projective
   line;
3. there is one nonzero `(delta,eta) in K^2` and seven constant functionals
   `lambda_S`, on the same graph, `Q`, contraction, and `M/Z` normalization,
   such that

   ```text
   (lambda_S tensor id)Gamma_Q
      =delta P_S^M+eta P_S^Z                          (7)
   ```

   for every `S in F_7`.

If every `C_S=K^2`, then `C_*=K^2`.  Otherwise the common space in the good
branch is the unique rank-one member shared by all rank-one targets.

### Proof

The subspaces of a two-dimensional vector space are exactly zero, lines, and
the whole space.  Intersecting with `K^2` changes nothing, intersecting with a
line restricts to that line, two distinct lines intersect in zero, and a zero
member kills the intersection.  This proves the equivalence of 1 and 2.

By `GLD15`, `C_S` is exactly the image of the constant-functional evaluation
map on the two desired labelled blocks.  Hence a fixed vector belongs to all
seven spaces exactly when seven target-specific functionals realize (7) with
the same coefficients.  This proves the equivalence with 3.  `square`

The functionals in (7) may vary with `S`; the graph, `Q`, contraction, open
GHZ bases, coefficient axes, and `(delta,eta)` may not.  Separate nonzero
rank-one rows with different slopes do not satisfy Theorem 1.

## 2. Arbitrary-`h` denominator-free shifted response identity

Let `B_e` be the direct pair block and let

```text
K_e=x_u tensor y_v+y_u tensor x_v                  (8)
```

be the residual-incidence pair block, with the fixed residual contractions
already inserted.  The globally labelled `GLD15` pair layers are

```text
M_e=B_e,                 Z_e=h B_e+K_e.               (9)
```

For six pair arrays `X`, put

```text
C(X)=X_12 X_34+X_13 X_24+X_14 X_23.                 (10)
```

Define the polarized cross term

```text
X(B,K)=
 (B_12 K_34+K_12 B_34)
 +(B_13 K_24+K_13 B_24)
 +(B_14 K_23+K_14 B_23).                             (11)
```

The residual-absent and residual-present four-port layers are

```text
M_U=C(B),                 Z_U=h C(B)+X(B,K).          (12)
```

Fix a nonzero common vector `(delta,eta) in C_*`, and put

```text
a=delta+h eta.                                       (13a)
```

Apply the functionals from Theorem 1 to one physical deck and define

```text
D_e=delta M_e+eta Z_e=a B_e+eta K_e,
T'=delta M_U+eta Z_U
  =a C(B)+eta X(B,K).                                (13b)
```

### Theorem 2 (arbitrary-`h` shifted GLD3 identity)

The common selected package satisfies

```text
a T'=C(D)-C(eta K).                                  (14)
```

Moreover every one-port flattening of `C(eta K)` has rank at most two.

### Proof

For each complementary pair partition `{e,f}`, expand

```text
(a B_e+eta K_e)(a B_f+eta K_f)
 =a^2 B_eB_f
  +a eta(B_eK_f+K_eB_f)
  +eta^2 K_eK_f.                                     (15)
```

Summing (15) over the three partitions and subtracting
`C(eta K)=eta^2 C(K)` gives exactly `a T'` by (11)--(13b).
This is a polynomial identity in `delta,eta,h`; no response, selector
coefficient, or effective scalar is divided out.

The pair array `eta K` has the same two-shore form as (8): scale every
`x_u` by `eta` and leave every `y_u` fixed.  The common-row expansion of
`GLD3` therefore places every one-port row of `C(eta K)` in
`span{x_u,y_u}`, proving rank at most two.  This includes `eta=0`.
`square`

Equation (14) is derived from one fixed physical graph and one fixed response
window.  It is not obtained by separately factorizing the six selected pair
tensors.  Conversely, (14) does not claim that the selected combination is a
new labelled deck summand or that varying `(delta,eta)` gives a same-graph
fibre.

## 3. Three-active-colour contradiction

Suppose now that the fixed graph/deck is a hypothetical Krenn--Gu witness, so
the seven operator identities (7) may be applied to the full mixed GHZ
equation.  Every selected `D_e` and `T'` is then target-diagonal in the same
fixed port bases.

Fix a port `u`.  For each colour `c`, choose an incident edge

```text
e_c={u,v_c},       f_c=U-e_c,       delta_c!=c,       (16)
```

and assume

```text
g_c=D_(e_c)(c,c)D_(f_c)(delta_c,delta_c)!=0
       for c=0,1,2.                                  (17)
```

This is exactly the `GLD3` three-colour pair-depth activity condition, now
for the common selected pair package `D`.

As in `GLD3`, let `beta_c` be the word on `U-{u}` with colour `c` at `v_c`
and colour `delta_c` at the other two ports, and form the nine actual selected
four-port coefficients

```text
G_(r,c)=T'(r at u,beta_c on U-{u}).                   (18)
```

All nine words in (18) are mixed.

### Theorem 3 (common-line nine-word detector)

Under (16)--(17), the selected submatrix of (14) is

```text
A=diag(g_0,g_1,g_2)-a G,
rank A<=2.                                            (19)
```

Hence:

1. if `a=0`, the three-active stratum is impossible;
2. if `a!=0`, at least one of the nine mixed coefficients in (18) is
   nonzero.

In either case a legally selected pure GHZ package satisfying (17) is
impossible.

### Proof

Target diagonality of every `D_e` makes the selected `3 x 3` submatrix of
`C(D)` equal to `diag(g_0,g_1,g_2)`, exactly as in the proof of `GLD3`
Theorem 3.  Restrict (14) to the same rows and columns.  Theorem 2 bounds the
rank of the selected submatrix of `C(eta K)` by two, giving (19).

If `a=0`, then (19) says that the invertible diagonal matrix
`diag(g_0,g_1,g_2)` has rank at most two.  If `a!=0` and every entry of
`G` vanished, the same contradiction would follow.  Finally, applying (7)
to the GHZ target makes `T'` diagonal, so every mixed entry in (18) must be
zero.  Thus both alternatives contradict a hypothetical witness.  `square`

### Corollary 3.1 (all-pure pair nonvanishing)

If one common vector in `C_*` produces diagonal pair tensors `D_e` whose
three pure diagonal entries are nonzero on all six edges, then (17) holds at
every port.  The common-line branch is therefore excluded.

## 4. Sharpness controls

### 4.1 Distinct slopes do not synchronize

Let six formal target spaces equal `span(1,1)` and let the seventh equal
`span(1,2)`.  Every target separately has a nonzero rank-one joint selector,
but

```text
span(1,1) intersection span(1,2)=0.                   (20)
```

There is no common package and no identity (14) with one coefficient vector.
This is an exact module-level control, not a graph or witness.

More generally, target-dependent slopes produce unmatched coefficients in
the three complementary products.  The homogeneous quadratic completion in
(15) is unavailable unless one vector lies in all seven `C_S`.

### 4.2 Unequal slopes survive even with three-colour activity

There is an exact physical `h=0` response-algebra control over `Q`.  At every
port take

```text
x_u=y_u=e0,              K_e=2E_00 for every edge e.  (21)
```

Define six diagonal pair tensors `A_e` by

```text
A_e(0,0)=2                         for every e,
A_e(1,1)=1                         for e in {12,23,34},
A_e(2,2)=1                         for e in {13,24},
all other entries zero,                                  (22)
```

and put `B_e=A_e-2K_e`.  Thus the six common pair rows have slope `[1:2]`:

```text
M_e+2Z_e=B_e+2K_e=A_e.                                (23)
```

Choose instead the four-port slope `[1:1]`.  Direct matching expansion gives

```text
M_U+Z_U=C(B)+X(B,K)
 =-12 e0^tensor4+e1^tensor4+e2^tensor4.               (24)
```

Every selected pair and four-port mixed coefficient vanishes.  Nevertheless,
at port `1` the three activity products may be chosen as

```text
A_14(0,0)A_23(1,1)=2,
A_12(1,1)A_34(0,0)=2,
A_13(2,2)A_24(0,0)=2.                                 (25)
```

For completeness, put `A=B+2K`.  Since `X(K,K)=2C(K)`, the four-port row is

```text
C(A-2K)+X(A-2K,K)=C(A)-X(A,K).
```

Here `K` has only colour zero and `A_e(0,0)=K_e(0,0)`.  Every mixed
zero/`c` word with even multiplicities is `2+2` and has exactly one diagonal
matching, whose `C(A)` term is cancelled by the corresponding `X(A,K)` term;
words with odd multiplicities have no diagonal matching.  The colour-one
edge family `{12,23,34}` and colour-two family `{13,24}` are
cross-intersecting, so no mixed one/two word occurs.  The pure coefficients
are respectively `3*4-3*8=-12`, `A_12(1,1)A_34(1,1)=1`, and
`A_13(2,2)A_24(2,2)=1`, proving (24) directly.

Thus separate rank-one pair and four-port rows, complete target shape, and
full three-colour activity do not suffice when their projective slopes differ.
This is a physical `q=2` response window, but it is not a legal module-selector
or hypothetical-witness realization; its residual frames have rank one.

### 4.3 Three-colour activity is load-bearing

Take the exact rational two-active camouflage response of `GLD3` Section 4,
but view its direct blocks `B` and residual channel `K` on the base `h=0`
graph.  Then

```text
M_e=B_e,          Z_e=K_e,
M_U=C(B),         Z_U=X(B,K).                         (26)
```

The common response-level vector `[delta:eta]=[1:1]` gives exactly the
camouflage tensors

```text
D_e=B_e+K_e,
T'=C(B)+X(B,K)
  =3 e0^tensor4+(4/3)e1^tensor4+e2^tensor4.           (27)
```

Every selected pair and four-port mixed coefficient vanishes and all three
pure four-port coefficients are nonzero, but only colours zero and one have
complementary pair-depth activity.  Thus the conclusion of Theorem 3 is false
without (17).

This is a physical response-algebra sharpness control.  It does not prove
that the `[1:1]` row is a legal module selector on that graph, does not satisfy
the full witness equations, and is not a counterexample.

### 4.4 Zero spaces and pure-axis lines

A single `C_S=0` kills `C_*`.  The pure-`M` and pure-`Z` axes are nevertheless
valid common lines when they occur at every target.  Theorem 3 includes both.
The pure residual-absent axis `eta=0` has `a=delta`.  The pure
residual-present axis `delta=0` has `a=h eta`, so it lies on the
rank-contradiction divisor exactly when `h=0`; for `h!=0` it enters the
nine-word alternative.  More generally `a=0` is the physical projective line
`[delta:eta]=[-h:1]`.  No division by `a`, `delta`, or `eta` occurs.

## 5. Exact frontier and scope ledger

```text
common coefficient space C_* and projective criterion:       PROVED;
same-slope seven-target constant operator package:            PROVED;
arbitrary-h denominator-free identity (14):                   PROVED;
effective-scalar a=0 active branch excluded:                  PROVED;
effective-scalar a!=0 nine-word mixed detector:               PROVED;
all-pure pair nonvanishing common-line branch excluded:       PROVED;
different rank-one slopes imply common supply:                FALSE;
unequal slopes plus target shape and three-activity contradict: FALSE;
two-active common-line target shape implies contradiction:    FALSE;
common nonzero line forced on every hypothetical witness:      UNKNOWN;
three-colour activity forced for a common selected package:    UNKNOWN;
zero-intersection witness branch excluded:                     UNKNOWN;
physical graph-fibre interpretation of selected combinations: UNKNOWN;
weighted permanent implication:                               UNKNOWN;
global Krenn--Gu conjecture:                                   UNRESOLVED.
```

The breadth is one four-port set, all six pair targets, one graph, one `Q`,
and one contraction.  The module depth is the complete nonempty even
surplus-two deck; the response depth is pair and four-port only.  The
reconstructed object is the common shifted package `(D_e,T')`, not separate
`M,Z` tensors.  The ambiguity object is the common coefficient subspace
`C_*`; it is zero, a projective line, or `K^2`.  There is no overlap
transition group.  The target implication is the nine-word contradiction
under (17).  The permanent implication is none.

## Verification boundary

The strengthened arbitrary-`h` statement and its exact residual scope are
audited in the
[2026-08-20 hostile review](../../docs/audits/FIXED_Q_COMMON_PROJECTIVE_JOINT_RESPONSE_SELECTOR_ARBITRARY_H_REVIEW_2026-08-20.md).

Run from repository root:

```powershell
python claims/arbitrary-order/verify_fixed_q_common_projective_joint_response_selector.py
python -I claims/arbitrary-order/audit_fixed_q_common_projective_joint_response_selector.py
```

The primary exact symbolic replay checks the arbitrary-`h` polynomial
identity, the effective-scalar divisor and pure-axis cases, common-subspace
trichotomy, unequal-slope three-active control, and rational `[1:1]`
camouflage response.  The independent standard-library audit uses a separate
polynomial dictionary, direct complementary-matching enumeration, and exact
`Fraction` tensor coefficients.
These scripts audit the bounded identities and controls.  The full-module
operator criterion and the determinant proof are load-bearing.
