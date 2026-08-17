# Fixed-Q unequal-slope quadratic-cancellation three-full-pair exclusion

## Status

**Exact characteristic-zero response exclusion and conditional module
detector.**  `GLD16` treats the branch in which the six pair targets and the
four-port target share one projective `M/Z` coefficient vector.  This theorem
handles two special unequal-slope branches.

Normalize the six pair rows to slope `[1:p]` and the four-port row to slope
`[1:t]`.  On the physical `h=0` branch put

```text
D_e=B_e+pK_e,
T=C(B)+tX(B,K).
```

This is an `M`-active normalization: a pure-`Z` pair row with zero `M`
coefficient cannot be rescaled to `[1:p]` and lies outside the theorem.

If

```text
p(p-2t)=0,             p!=t,                          (1)
```

then the quadratic `C(K)` correction cancels.  If every `D_e` is diagonal, one
complementary edge pair on which all six diagonal entries of the two `D`
blocks are nonzero forces one of eighteen displayed mixed coefficients of `T`
to be nonzero.  No local-frame-rank, concision, or nonzero pure coefficient of
`T` is needed.

Consequently, on a hypothetical witness, legally attached pair rows of one
common slope and a legally attached four-port row of the other slope contradict
the GHZ target on this local nonvanishing branch.  The theorem does not force
those operator rows, the slope relation, or the six nonzero pair values; does
not integrate a response fixture into a witness; and gives no permanent
restriction.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

Dependencies:

- [`GLD16`](FIXED_Q_COMMON_PROJECTIVE_JOINT_RESPONSE_SELECTOR_AND_SHIFTED_GLD3_DETECTOR_THEOREM.md)
- [`GLD3`](TWO_RESIDUAL_PAIR_FOUR_PORT_DIAGONAL_INTERFERENCE_AND_CAMOUFLAGE_BOUNDARY_THEOREM.md)

## 1. Fixed response algebra and unequal slopes

Work over a characteristic-zero field `K`.  Fix one physical `q=2`, `h=0`
response on one four-port set

```text
U={1,2,3,4}.                                           (2)
```

For every edge `e={u,v}` let

```text
K_e=x_u tensor y_v+y_u tensor x_v,                    (3)
```

so every `3 x 3` block `K_e` has rank at most two.  Let `B_e` be arbitrary
direct pair blocks.  For six pair arrays `Y`, write

```text
C(Y)=Y_12Y_34+Y_13Y_24+Y_14Y_23,                     (4)
```

and let

```text
X(B,K)=
 (B_12K_34+K_12B_34)
 +(B_13K_24+K_13B_24)
 +(B_14K_23+K_14B_23).                               (5)
```

The residual-absent and residual-present layers are

```text
M_e=B_e,                 Z_e=K_e,
M_U=C(B),                Z_U=X(B,K).                  (6)
```

Fix scalars `p,t in K` and define the selected response package

```text
D_e=M_e+pZ_e=B_e+pK_e,
T=M_U+tZ_U=C(B)+tX(B,K).                              (7)
```

The coefficient axes in (7) are one globally fixed `M/Z` normalization.  A
target-by-target rescaling that changes `p` or `t` changes the assertion.

### Lemma 1 (general unequal-slope identity)

For arbitrary `p,t`,

```text
T=C(D)+(t-p)X(D,K)+p(p-2t)C(K).                      (8)
```

### Proof

Substitute `B=D-pK`.  Polarization gives

```text
C(D-pK)=C(D)-pX(D,K)+p^2C(K),
X(D-pK,K)=X(D,K)-2pC(K).                             (9)
```

Insert (9) into (7) and collect terms.  `square`

Under (1), put

```text
q=t-p.                                               (10)
```

Then `q!=0` and (8) becomes

```text
T=C(D)+qX(D,K).                                      (11)
```

The two branches in (1) are `p=0,t!=0` and `p=2t,t!=0`.

## 2. One three-full complementary pair forces a mixed word

Assume all six selected pair tensors `D_e` are diagonal in one fixed ternary
port basis.  Fix orientations of one complementary edge partition

```text
e=(i,j),                 f=(r,s)=U-e.                 (12)
```

Suppose

```text
D_e(c,c)!=0,             D_f(c,c)!=0
for c=0,1,2.                                          (13)
```

Call (13) a **three-full complementary pair**.  This is a local sufficient
nonvanishing condition, not a claimed exhaustive or minimal support
classification.

For ordered distinct colours `a,b`, let `c` denote the third colour and define
the twelve `2+1+1` words

```text
w_e(a,b;c,c)=(a at i,b at j,c at r,c at s),
w_f(c,c;a,b)=(c at i,c at j,a at r,b at s),          (14)
```

and define the six `2+2` words

```text
w_(c,d)=(c at i,c at j,d at r,d at s),      c!=d.   (15)
```

All eighteen words in (14)--(15) are mixed.

### Theorem 2 (quadratic-cancellation eighteen-word detector)

Under (1)--(13), at least one of the eighteen coefficients of `T` in
(14)--(15) is nonzero.

### Proof

Suppose instead that all eighteen displayed coefficients vanish.  First
diagonalize the two channel blocks on the named partition.  Let `a,b,c` be
the three distinct colours and consider `w_f(c,c;a,b)`.  Pair diagonality kills
`C(D)`.  In `X(D,K)`, every term belonging to either other complementary
partition contains a mixed entry of a `D` block, while on `e|f` only

```text
D_e(c,c)K_f(a,b)                                     (16)
```

survives.  Equations (11), coefficient vanishing, `q!=0`, and (13) give
`K_f(a,b)=0`.  Varying the ordered pair `a!=b` proves that `K_f` is diagonal.
The six words `w_e(a,b;c,c)` similarly prove that `K_e` is diagonal.

Write `D_e^c=D_e(c,c)` and similarly for the other diagonal entries.  On the
mixed `cc|dd` word for `e|f`, where `c!=d`, the other two partitions again
vanish by pair diagonality.  Equation (11) is therefore

```text
D_e^c D_f^d
 +q(D_e^c K_f^d+K_e^c D_f^d)=0.                     (17)
```

All denominators below are nonzero by (10) and (13).  Set

```text
r_e^c=-q K_e^c/D_e^c,        r_f^c=-q K_f^c/D_f^c.  (18)
```

Dividing (17) gives the six equations

```text
r_e^c+r_f^d=1                  whenever c!=d.         (19)
```

For two colours `c,c'`, choose the third colour `d`.  The two equations with
the same `r_f^d` show `r_e^c=r_e^c'`.  The symmetric argument applies to
`r_f`.  Hence for one scalar `r`,

```text
r_e^0=r_e^1=r_e^2=r,
r_f^0=r_f^1=r_f^2=1-r.                              (20)
```

The diagonal physical block `K_e` has rank at most two, so one of its three
diagonal entries is zero.  By (13), (18), and (20), this forces `r=0`.
Then every diagonal entry of `K_f` equals `-D_f^c/q` and is nonzero, so the
diagonal matrix `K_f` has rank three.  This contradicts (3).  `square`

The proof uses the full diagonality of all six `D` blocks to kill the two
unselected complementary matchings.  It uses nonvanishing only on the six
entries in (13).  It does not use a rank-two hypothesis on each local frame;
the intrinsic block bound `rank K_e<=2` is sufficient.

## 3. Conditional witness consequence

Return to one fixed graph, residual pair `Q`, fully specified contraction,
four-port window, and the complete fixed-`Q` companion module.  Suppose:

1. for every pair `e subset U`, the exact joint operator space of `GLD15`
   contains `(1,p)`;
2. the four-port operator space contains `(1,t)`;
3. the same globally normalized scalars satisfy (1);
4. one complementary pair satisfies the six nonvanishing conditions (13).

The selector functionals may differ between targets; the graph, `Q`,
contraction, port basis, coefficient axes, and slopes may not.

### Corollary 3.1 (conditional unequal-slope witness exclusion)

No hypothetical Krenn--Gu witness satisfies conditions 1--4.

### Proof

Apply the seven constant operator identities to the full mixed GHZ equation.
The six selected pair tensors `D_e` and the selected four-port tensor `T` are
target-diagonal.  Theorem 2 forces one of the displayed mixed coefficients of
`T` to be nonzero, giving the contradiction.  `square`

This corollary needs neither seven joint rank-two spaces nor one common
projective line.  It treats the two exact unequal-slope cancellation branches
in (1).  It does not assert that any of conditions 1--4 is forced on the
witness locus.

## 4. Sharpness controls

### 4.1 The six local nonzero values cannot simply be omitted

The unequal-slope physical response control in `GLD16` has

```text
p=2,                    t=1,                         (21)
```

so it lies on the branch `p=2t`.  Its six diagonal pair tensors have
three-colour pair-depth activity, and its four-port tensor is pure with
coefficients

```text
(-12,1,1).                                            (22)
```

Nevertheless no edge, and hence no complementary pair, is three-full.  Thus
the conclusion is false if (13) is simply deleted.  This does not prove that
(13) is a globally minimal support hypothesis.

### 4.2 The quadratic-cancellation relation is load-bearing

At every port take

```text
x_u=(1,1,0),             y_u=(1,-1,0).               (23)
```

Then every physical channel block is

```text
K_e=diag(2,-2,0),        rank K_e=2.                 (24)
```

Put `B_e=E_22` on every edge and choose

```text
p=1,                    t=0.                         (25)
```

All six selected pair tensors are

```text
D_e=diag(2,-2,1),                                     (26)
```

so every complementary pair is three-full and three-colour pair-depth
activity holds.  But

```text
T=C(B)=3 e_2^tensor4                                  (27)
```

is pure.  Here `p(p-2t)=1`, so (1) fails.  This exact physical response
control shows that arbitrary unequal slopes cannot replace the cancellation
condition, even with rank-two residual frames and all eighteen pair entries
nonzero.

### 4.3 The slope boundary survives pure normalization

Keep the channel (24), still with `(p,t)=(1,0)`, but support colour zero of
`B` on the matching `12|34`, colour one on `13|24`, and colour two on
`14|23`, every displayed coefficient equal to one.  The three coloured edge
families are pairwise cross-intersecting, and

```text
T=C(B)=e_0^tensor4+e_1^tensor4+e_2^tensor4.           (28)
```

The pair package is diagonal and has three-colour pair-depth activity.  On the
complementary pair `14|23`, both blocks equal `diag(2,-2,1)`, so (13) holds.
Thus this control satisfies the local six-value hypothesis and has three
nonzero pure four-port coefficients; it fails only the quadratic-cancellation
condition.  It strengthens the slope boundary without replacing the
all-eighteen-nonzero control in Section 4.2.

All controls in this section are exact physical response windows.  They are
not claimed legal fixed-module operator rows, hypothetical witnesses,
same-graph fibres, or counterexamples to the global conjecture.

## 5. Exact frontier and scope ledger

```text
general unequal-slope identity (8):                         PROVED;
quadratic-cancellation reduction (11):                      PROVED;
channel diagonalization from 2+1+1 target rows:             PROVED;
ternary ratio propagation (19)--(20):                       PROVED;
one three-full complementary-pair eighteen-word detector:   PROVED;
conditional fixed-module witness exclusion:                 PROVED;
three-activity without (13) suffices:                        FALSE;
all eighteen pair nonzeros without (1) suffice:             FALSE;
pure normalization removes the slope restriction:           FALSE;
required pair/four operator slopes forced on every witness:  UNKNOWN;
three-full complementary pair forced on every witness:      UNKNOWN;
remaining unequal slopes classified:                        UNKNOWN;
weighted permanent implication:                             UNKNOWN;
global Krenn--Gu conjecture:                                 UNRESOLVED.
```

The breadth is one named four-port set, its six pair rows, one graph, one
`Q`, and one contraction.  The response depth is pair and four-port.  The
reconstructed object is the unequal-slope package `(D_e,T)`, not separate
`M,Z`.  The ambiguity object is the remaining slope/support locus outside
(1) and (13), including pure-`Z` pair axes; no transition group is claimed.
The target implication is the rank-three contradiction for `K_f`.  The
permanent implication is none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_fixed_q_unequal_slope_quadratic_cancellation_three_full_pair_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_unequal_slope_quadratic_cancellation_three_full_pair_exclusion.py
```

The primary exact symbolic replay checks (8), the mixed-row support formulas,
the ternary ratio system, and all three physical controls.  The independent
standard-library audit uses a separate sparse polynomial representation,
direct complementary-matching enumeration, exact `Fraction` row reduction,
and independently constructed controls.  These scripts audit the bounded
identities and examples.  The arbitrary-field support and rank argument in
Theorem 2 is load-bearing.
