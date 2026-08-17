# Four-root constant target-module selector quotient and maximum-root sharpness

## Status

**Exact characteristic-zero constant-selector criterion and sharp graph-side
incidence boundary.**  Fix four roots, a named residual pair `Q`, four open
ports `U`, and the complete fixed-`Q` surplus-two companion equation.  Keep
all `2079` nonempty even deck coordinates.  For every pair `S subset U` and
for `S=U`, the existence of a constant module selector for the physical
tensor

```text
H_(Q union S)(z_Q,-_S)                                (1)
```

is equivalent to one explicit quotient class being nonzero.  The desired
companion coefficient `g_S` must survive modulo the coefficient slices of
**every** nuisance label.  This is the exact noncircular version of

```text
P_S in im A_S.                                       (2)
```

The criterion is graph-specific in the legal sense: the selector may depend
on the fixed graph, root data, residual contractions, and companion map.  It
is nevertheless constant in the open port coordinates and is verified on
every deck column before the GHZ target value is inspected.  A rational
function-field inverse or a functional chosen merely because its realized
output is diagonal is not such a selector.

Both outcomes occur already on the maximum-root, triple-blocker graph-side
stratum.

1. An explicit one-parameter chart has all seven selectors (the six pairs
   and `U`) for every `t!=0`.  Each selector is one no-`c` root-word pivot,
   and the triple-blocker helper rows contain a `c` letter, so they cannot
   contaminate it.
2. At `t=0` all seven desired coefficients vanish.  More sharply, a second
   maximum-root triple-blocker chart has `g_U!=0` but one nuisance label has
   all `81` root basis words as coefficient slices.  Hence the four-port
   quotient class is zero and no `T` selector exists.

Thus maximum-root saturation and blocker incidence alone neither force nor
forbid constant target attachment.  The full mixed hypothetical-witness
equations must force the good quotient branch, exclude the bad branch, or
supply a different detector.  The positive chart is not proved to meet the
witness locus, and the negative chart is not a witness or a physical
same-state ambiguity.  No permanent restriction is obtained.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

This theorem refines the open attachment input in the
[`pair/four-port interference theorem`](TWO_RESIDUAL_PAIR_FOUR_PORT_DIAGONAL_INTERFERENCE_AND_CAMOUFLAGE_BOUNDARY_THEOREM.md)
and the affine incidence language of the
[`two-chart boundary`](TWO_CHART_TARGET_INCIDENCE_AND_CLONED_CAMOUFLAGE_ATLAS_BOUNDARY_THEOREM.md).
It uses the full companion expansion of the
[`surplus-two deck sensor`](MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md)
but does not assume that sensor is observable.

## 1. The full fixed-`Q` module

Work over a characteristic-zero field `K`.  Let

```text
R={1,2,3,4},              B=Q disjoint-union U,
Q={q0,q1},                U={u1,u2,u3,u4}.             (3)
```

Every local space has dimension three.  Fix nonzero residual vectors `z_q`
but leave the roots and the four ports open.  Put

```text
E=direct-sum_(empty!=I subset B, |I| even)
     tensor_(i in I) V_i^*,
F=(tensor_(i in R) V_i^*) tensor (tensor_(u in U) V_u^*).
                                                               (4)
```

The dimensions are

```text
dim E=sum_(k=2,4,6) binom(6,k)3^k=2079,
dim F=3^8=6561.                                      (5)
```

The fixed-`Q` companion equation is the constant linear map

```text
Gamma_Q:E -> F.                                      (6)
```

It is obtained from the full uncontracted matching identity by inserting
`z_q0,z_q1` only after every nonempty even deck label has been retained.
This is not the `301`-parameter fixed-graph slice obtained by solving for
edge blocks, and no deck label is suppressed.

Fix

```text
S in binom(U,2) union {U},
L_S^*=(tensor_(i in R)V_i^*) tensor
      (tensor_(u in U-S)V_u^*),
W_S=tensor_(u in S)V_u^*.                            (7)
```

Thus `F=L_S^* tensor W_S`.  Let

```text
P_S:E -> W_S                                         (8)
```

be zero on every direct summand except `I=Q union S`, and on that summand
evaluate the `Q` slots at `z_Q`.  It is the formal projection (1).

The coefficient multiplying that target block in the companion expansion is

```text
g_S=G_(U-S) in L_S^*.                                (9)
```

For `lambda in L_S=(L_S^*)^*`, define

```text
A_S(lambda)=(lambda tensor id_(W_S)) Gamma_Q
             in Hom(E,W_S).                          (10)
```

The load-bearing restriction in (10) is the tensor-product form of the
functional.  An unrestricted recovery map `E -> W_S` is a different and
weaker problem.

## 2. Exact nuisance quotient

Remove the desired block formally:

```text
Theta_S=Gamma_Q-g_S tensor P_S.                      (11)
```

Define the full nuisance coefficient-slice space

```text
N_S=span{
  (id_(L_S^*) tensor eta)(Theta_S(x)):
  x in E, eta in W_S^*
} subset L_S^*.                                      (12)
```

Because `E` is the direct sum of the labelled deck spaces, (12) retains
every coordinate of every non-target label.  It also retains every unwanted
coefficient slice after the fixed residual evaluation.

### Theorem 1 (constant target-module selector criterion)

The following are equivalent.

1. There is a constant `lambda in L_S` such that

   ```text
   A_S(lambda)=P_S.                                  (13)
   ```

2. There is a `lambda in N_S^perp` with

   ```text
   lambda(g_S)=1.                                    (14)
   ```

3. The desired coefficient has nonzero quotient class

   ```text
   [g_S]!=0 in L_S^*/N_S.                            (15)
   ```

Equivalently,

```text
rank[N_S | g_S]=rank N_S+1.                          (16)
```

When these conditions hold, the complete selector family is the affine
slice

```text
{lambda in N_S^perp:lambda(g_S)=1}.                  (17)
```

When they fail, a dual functional on `Hom(E,W_S)` separates `P_S` from
`im A_S`.  This does **not** imply a nonzero projection of
`ker Gamma_Q`, an unrestricted deck ambiguity, or a second physical graph.

### Proof

Subtract (8) from (10) and use (11).  On the desired direct summand the
difference is `(lambda(g_S)-1)P_S`.  On every other labelled direct summand
it is `(lambda tensor id)Theta_S`.  The direct summands are independent, so
(13) holds exactly when `lambda(g_S)=1` and `lambda` kills every coefficient
slice in (12).  This proves the equivalence of 1 and 2.

Finite-dimensional separation gives a functional which kills `N_S` and is
nonzero on `g_S` exactly when `g_S` is not in `N_S`.  Normalize that value to
one; characteristic zero is more than sufficient for this field-linear
step.  This proves 2--3, (16), and (17).  `square`

### Exact finite sizes

Before quotienting the fixed residual evaluation, a pair selector has

```text
dim L_S=3^6=729,            2079*3^2=18711 rows,      (18)
```

while the four-port selector has

```text
dim L_U=3^4=81,             2079*3^4=168399 rows.     (19)
```

Evaluation at the two fixed residual vectors factors `E` through a quotient
of dimension

```text
1+2[binom(4,2)3^2+binom(4,4)3^4]
 +2[binom(4,1)3+binom(4,3)3^3]
=511.                                                   (20)
```

The effective row counts are therefore `4599` for a pair and `41391` for
`U`.  Solving all seven selectors independently uses `6*729+81=4455`
unknowns.  These counts make (16) a finite exact Gaussian-elimination
problem; they do not decide its witness-locus outcome.

## 3. A maximum-root triple-blocker seven-selector chart

Choose a basis `a_i,b_i,c_i` of every root dual space.  At every outside
mode choose a covector `epsilon_v` and a vector `z_v` with
`epsilon_v(z_v)=1`.  Use private ports `u_i` and prescribe the clean
root companions

```text
W_ij=t b_i tensor b_j,
W_(i,u_j)(-,z_(u_j))=delta_ij a_i,
W_(i,q0)(-,z_q0)=b_i,
W_(i,q1)(-,z_q1)=c_i.                                (21)
```

The omitted outside covector `epsilon_v` is understood in every displayed
root--outside contraction.  Let `C=U-S`.

### Theorem 2 (simultaneous clean selectors)

For `t!=0`, all seven desired quotient classes are nonzero.  More precisely,

```text
g_S=t a_C b_S tensor epsilon_C             if |S|=2,
g_U=3t^2 b_1b_2b_3b_4.                              (22)
```

No other companion column contains the indicated no-`c` root word.  The
dual root-word functional, tensored with complement-port vectors on which
`epsilon_u` is one, is a constant selector after normalization by `t^(-1)`
for a pair and `(3t^2)^(-1)` for `U`.

At `t=0`, every coefficient in (22) is zero, so all seven module selectors
fail.

### Proof

For the label `Q union S`, the roots assigned outside are exactly `C`.
Every `i in C` must use its private port and contributes `a_i`.  The
remaining roots `S` are internally paired.  For `|S|=2` there is one internal
edge and coefficient `t`; for `S=U` there are three root perfect matchings,
each with coefficient `t^2`.  This proves (22).

In the clean companion ledger, a column containing neither `q1` nor a helper
row has no `c` letter.  Its `a`-support is exactly its set of private ports,
so the word `a_Cb_S` identifies `C` uniquely.  Every column using `q1`
contains a `c`.  Hence the pivot is absent from every nuisance label, which
proves the selector assertion by Theorem 1.  If `t=0`, a pair output still
needs one internal root edge and the four-port output needs two, proving the
last assertion.  `square`

### Maximum-root and triple-blocker upgrade

Over `C`, the chart may be installed on the graph-side incidence stratum
without changing a selector.  Choose torus roots as in the surplus-two sensor chart,
with every root--root evaluation zero and `c_i(x_i)!=0`.  At each outside
mode retain its assigned `epsilon_v` row and add two blocks

```text
c_j tensor eta_v,             c_k tensor theta_v,     (23)
```

from suitable roots, where `epsilon_v,eta_v,theta_v` are independent.
Their evaluations at the torus roots make the outside row span three, so
every outside mode is a triple blocker.  Every new companion monomial using
(23) has a `c` root letter and is killed by all the no-`c` selectors in
Theorem 2.

Make every outside--outside block a nonzero coordinate monomial.  Two torus
outside vectors can then never be mutually zero-coupled.  An outside vertex
also has an assigned nonzero coordinate edge to an old root, so including it
removes at least one old root.  The displayed four-root set is therefore
maximum-cardinality.  This proves that the seven-selector locus meets the
maximum-root triple-blocker graph-side stratum.  No target equation has been
imposed.

## 4. A nonzero desired coefficient swallowed by nuisance

The zero-root wall does not show the full sharpness of the quotient.
Retain the same four roots and ports, but put

```text
W_(i,u_j)=delta_ij sum_(c=0)^2
  e_(i,c)^* tensor e_(u_j,c)^*.                       (24)
```

Consider the four-port selector `S=U`.  The nuisance deck label `I=Q` has
companion `G_U`.  Because (24) permits only the identity root-to-port
assignment,

```text
G_U=product_(i=1)^4
  (sum_(c=0)^2 e_(i,c)^* tensor e_(u_i,c)^*).         (25)
```

### Theorem 3 (maximum-root triple-blocker nonselector chart over `C`)

The `81` port-coordinate slices of (25) are the `81` root basis words.
Consequently

```text
N_U=L_U^*,                                            (26)
```

and no constant four-port module selector exists.  The construction may be
chosen with `g_U=G_empty!=0` and may be upgraded to the maximum-root,
triple-blocker stratum.

### Proof

Choose one of the three port coordinates independently in every factor of
(25).  The resulting root slice is the same independently chosen root basis
word.  All `3^4=81` words occur once, proving (26).  Theorem 1 then forbids a
functional which annihilates the nuisance and normalizes `g_U`.

Choose nonzero root--root blocks which vanish at the selected torus roots but
have nonzero four-root hafnian; the `t b_i tensor b_j` blocks above with
`t!=0` suffice.  Thus `g_U!=0`.  Add two independent interpolation rows per
outside mode.  At zero helper parameters the nuisance-slice determinant is
one, so it has nonzero constant term.  Because a characteristic-zero field
is infinite, choose all helper parameters nonzero away from this determinant
and the finitely many assigned-edge zero sets.  The triple-blocker and
maximum-root argument following (23) applies unchanged.  `square`

The obstruction in Theorem 3 is formal module nonmembership, not merely a
low-rank realized output.  It is also not target-locus evidence: the full
mixed GHZ equations may avoid the chart.

## 5. Target, detector, and permanent interfaces

If the fixed graph data come from a hypothetical witness and (15) holds,
apply the corresponding `lambda` to the full fixed-`Q` GHZ equation.  Its
target side has the form

```text
sum_(c=0)^2 alpha_c tensor_(u in S)e_(u,c)^*,         (27)
```

because every contracted root and complement-port factor carries the same
colour on each pure GHZ summand.  Thus the output is target-diagonal without
choosing `lambda` from its value.  For the seven good classes, (27) supplies
exactly the same physical six `D_uv` tensors and `T` required by `GLD3`, with
one named `Q` and one set of contractions.

This still does not force three-colour complementary activity.  It also does
not make the corrected permanent aggregate weighted diagonal.  Therefore
the implications are

```text
seven quotient classes nonzero on a witness
  -> exact constant same-Q D/T attachment;

attachment + GLD3 three-colour activity
  -> displayed mixed-coefficient contradiction;

attachment alone
  -/> weighted permanent restriction.                (28)
```

## 6. Exact frontier and UNKNOWN remainder

```text
full fixed-Q deck-module dimension:                       2079;
constant selector iff [g_S]!=0 in L_S^*/N_S:             PROVED;
seven-selector maximum-root/triple-blocker chart:         PROVED;
zero-root seven-selector wall:                            PROVED;
g_U!=0 but N_U=L_U^* nonselector chart:                   PROVED;
maximum-root + triple blockers force attachment:          FALSE;
seven-selector good locus meets hypothetical witnesses:  UNKNOWN;
full mixed equations exclude every bad quotient locus:    UNKNOWN;
GLD3 three-colour activity after attachment:               UNKNOWN;
weighted permanent attachment:                            UNKNOWN;
global Krenn--Gu conjecture:                               UNRESOLVED.
```

The breadth is one complete fixed-`Q`, four-port chart.  The depth is every
surplus-two outside label of orders two, four, and six.  The reconstructed
objects are the six physical residual-present pair tensors and the physical
four-port tensor.  There is no overlap transition.  The ambiguity object is
the quotient class (15), not a physical graph fibre.  The target implication
is exact `D/T` attachment on the good branch; the permanent implication is
none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_four_root_constant_target_module_selector_quotient_and_maximum_root_sharpness.py
python -I claims/arbitrary-order/audit_four_root_constant_target_module_selector_quotient_and_maximum_root_sharpness.py
```

The primary verifier enumerates root partial matchings and root-to-outside
assignments for all `31` companion columns.  It checks the seven unique
pivots coefficientwise against all `2079` deck basis coordinates, their
`t`-degrees and multiplicities, the dimension counts, the zero-root wall,
and the `81` spanning nuisance slices.

The independent no-import audit derives the clean columns from residual-to-
root injections and disjoint support rather than importing the primary
recurrence.  It separately constructs the tensor-product identity nuisance,
checks its complete root-word image, and recomputes the fixed-`Q` quotient
dimension.  These bounded replays audit the displayed ledgers.  The
finite-dimensional separation proof, matching partition, pivot argument,
and maximum-root support proof above establish the theorem.
