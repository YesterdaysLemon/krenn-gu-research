# Fixed-Q response-visible operator slopes and edge-dependent cancellation divisor

## Status

**Exact characteristic-zero joint-module constraint, edge-dependent response
identity, and conditional eighteen-word detector.**  `GLD15` identifies the
constant operator-coefficient space for every pair and four-port target.
`GLD16` treats one common projective line, and `GLD17` treats two
unequal-slope cancellation branches when all six pair slopes agree.  This
theorem adds three exact interfaces:

1. on a hypothetical witness, every legal operator line lies in the kernel of
   the realized mixed-response map, so a rank-one line is either visible in
   the response coefficients or is genuinely response-invisible;
2. the `GLD17` quadratic-cancellation detector extends to six independent
   pair slopes;
3. on a globally decomposable physical channel, the remaining common-pair
   noncancellation locus is also excluded by one three-full complementary
   pair.

For pair slopes `p_e` and four-port slope `t`, put

```text
gamma_(ef)=p_e p_f-t(p_e+p_f)                         (1)
```

for each complementary matching `e|f`.  If all three `gamma_(ef)` vanish,
all six selected pair blocks are diagonal, and one complementary pair is
three-full with both pair slopes different from `t`, then one of eighteen
displayed mixed four-port coefficients is nonzero.  Hence, on the nonzero-`t`
cancellation chart, every surviving hypothetical witness lies on the product
of the three complementary support divisors.  At `t=0`, cancellation instead
forces a pure-`M` pair slope on every complementary matching.

The theorem does **not** force a nonzero operator space, response visibility,
the cancellation equations, or the local support condition; does not cover a
pure-`Z` pair axis by an `M`-active normalization; does not integrate a
response fixture into a witness; and gives no permanent restriction.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

Dependencies:

- [`GLD15`](FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md)
- [`GLD16`](FIXED_Q_COMMON_PROJECTIVE_JOINT_RESPONSE_SELECTOR_AND_SHIFTED_GLD3_DETECTOR_THEOREM.md)
- [`GLD17`](FIXED_Q_UNEQUAL_SLOPE_QUADRATIC_CANCELLATION_THREE_FULL_PAIR_EXCLUSION_THEOREM.md)

## 1. Exact operator spaces and mixed-response visibility

Work over a characteristic-zero field `K`.  Fix one graph, residual pair `Q`,
fully supported contraction, GHZ basis, and complete fixed-`Q` companion
module.  For

```text
F_7=binom(U,2) union {U},       |U|=4,                (2)
```

let `C_S subset K^2` be the exact `GLD15` operator-coefficient space.  Thus
`(a,b) in C_S` precisely when a constant functional on the complete companion
module, fixed before inspecting the response values, has operator output

```text
a P_S^M+b P_S^Z.                                      (3)
```

Write `M_S=P_S^M(H)` and `Z_S=P_S^Z(H)`.  Let

```text
Delta_S=span{w_(S,0),w_(S,1),w_(S,2)} subset W_S     (4)
```

be the pure GHZ output subspace and define the realized mixed-response map

```text
R_S:K^2 -> W_S/Delta_S,
R_S(a,b)=[a M_S+b Z_S].                               (5)
```

For a pair, `R_S` is represented by a `6 x 2` mixed-coordinate matrix.  For
`S=U`, it is represented by a `78 x 2` matrix.

### Theorem 1 (operator inclusion and response-visible slope)

If the full fixed-`Q` mixed GHZ equation holds, then

```text
C_S subset ker R_S.                                   (6)
```

Put `k_S=dim C_S`.  Consequently:

```text
k_S+rank R_S<=2.                                      (6a)
```

1. `k_S=2` forces `R_S=0`;
2. `k_S=1` forces `rank R_S<=1`; if `rank R_S=1`, then
   `C_S=ker R_S` and the mixed response determines the projective operator
   line exactly;
3. if `k_S=1` and `R_S=0`, the operator line is response-invisible and remains
   a full-module datum;
4. `k_S=0` gives no response-shape constraint.

### Proof

For `(a,b) in C_S`, apply its constant operator identity to the full witness
equation.  The GHZ target has output in `Delta_S`, so
`aM_S+bZ_S in Delta_S`.  This is (6).  The four branches are rank-nullity in
the two-dimensional coefficient plane.  `square`

The inclusion is one-way in general.  Mixed target shape cannot manufacture
an operator identity that the complete nuisance quotient does not supply.

### Exact full-nuisance chart minors

Let `B_S` be any matrix whose columns span the complete joint nuisance and put
`r=rank B_S`.  On a rank-one `M`-active chart choose `r` nuisance columns `J`
and `r+1` coordinate rows `I` such that

```text
mu_S=det [B_(S,I,J) | g_(S,M,I)] !=0.                 (7)
```

Define

```text
zeta_S=det [B_(S,I,J) | g_(S,Z,I)].                   (8)
```

The cofactor functional of (7) annihilates the full nuisance image, because
the selected `r` columns already span it, and has desired evaluation row
`(mu_S,zeta_S)`.  Therefore

```text
C_S=K(mu_S,zeta_S),       p_S=zeta_S/mu_S.            (9)
```

The ratio is independent of the chosen nonzero chart: it is the unique
projective rank-one operator line.  On a witness, every mixed coordinate
`omega` satisfies the denominator-cleared identity

```text
mu_S M_S(omega)+zeta_S Z_S(omega)=0.                 (10)
```

Two `M`-active rank-one targets have the same slope exactly when

```text
mu_S zeta_T-zeta_S mu_T=0.                           (11)
```

This is a polynomial full-nuisance test, not a selector chosen from the
observed output.

### Corollary 1.1 (finite common-line visibility test)

Assume `k_S>=1` for all seven targets and every rank-one `C_S` is
response-visible.  Stack the seven maps in (5):

```text
R_*:K^2 -> direct_sum_(S in F_7) W_S/Delta_S.         (12)
```

Then

```text
intersection_S C_S=ker R_*.                          (13)
```

Thus the `GLD16` common-line condition is equivalent on this stratum to
`rank R_*<=1`.  The matrix of `R_*` has `6*6+78=114` rows, so its rank is
decided by `binom(114,2)=6441` exact `2 x 2` minors.  Because every individual
target has rank at most one, a nonzero obstruction may be chosen among the
`3348` cross-target row pairs.

If a rank-one target is response-invisible, (13) need not hold; its slope is
then controlled only by a module minor such as (11).  A zero operator space or
pure-`Z` line is also a separate stratum.

## 2. Six independent pair slopes

Fix one physical `q=2`, `h=0` response on `U={1,2,3,4}`.  For every edge
`e={u,v}`, let

```text
K_e=x_u tensor y_v+y_u tensor x_v,                    (14)
```

so `rank K_e<=2`.  Let `B_e` be arbitrary direct pair blocks and use

```text
C(Y)=sum_(e|f) Y_e Y_f,
X(B,K)=sum_(e|f)(B_e K_f+K_e B_f),                   (15)
```

where the sums run over the three complementary matchings of `U`.

Choose `M`-active normalized pair rows `[1:p_e]` independently and one
`M`-active four-port row `[1:t]`.  Their physical values are

```text
D_e=B_e+p_e K_e,
T=C(B)+t X(B,K).                                      (16)
```

### Theorem 2 (edge-dependent slope identity)

Every package (16) satisfies

```text
T=sum_(e|f) {
    D_e D_f
   +(t-p_f) D_e K_f
   +(t-p_e) K_e D_f
   +gamma_(ef) K_e K_f
  },                                                  (17)
```

with `gamma_(ef)` from (1).

For unnormalized projective rows `[a_e:b_e]` and `[a_U:b_U]`, define

```text
Gamma_(ef)=a_U b_e b_f-b_U(b_e a_f+a_e b_f).         (18)
```

On the `M`-active chart,

```text
gamma_(ef)=Gamma_(ef)/(a_U a_e a_f).                 (19)
```

Hence, on the `M`-active chart, all `K_eK_f` corrections vanish exactly when
the three homogeneous polynomials `Gamma_(ef)` vanish.  The equations (18)
define the multihomogeneous closure of that chart; they do not extend the
normalized detector to a pure-`Z` boundary.  If all pair rows share `[a:b]`,
(18) reduces to

```text
b(a_U b-2a b_U)=0,                                   (20)
```

which is exactly the `GLD17` cancellation condition.

### Proof

For one matching substitute `B_e=D_e-p_eK_e` and
`B_f=D_f-p_fK_f` into its contribution to `C(B)+tX(B,K)`.  Collect the four
products.  This gives (17).  Clearing the three `M` coefficients gives
(18)--(19); (20) is immediate.  `square`

## 3. Edge-dependent eighteen-word detector

Assume from now on:

1. every `D_e` is diagonal in the fixed GHZ basis;
2. all three `gamma_(ef)` vanish;
3. one named complementary partition `e={i,j}`, `f={r,s}` satisfies

```text
p_e!=t,       p_f!=t,                                 (21)
D_e(c,c)D_f(c,c)!=0       for c=0,1,2.                (22)
```

Call (22) **three-fullness** of `e|f`.

The following eighteen words depend only on the named partition:

- for each ordered `a!=b`, let `c` be the third colour and put `(a,b)` on
  `e` and `(c,c)` on `f`;
- the six swapped words put `(c,c)` on `e` and `(a,b)` on `f`;
- for each ordered `c!=d`, put `(c,c)` on `e` and `(d,d)` on `f`.

### Theorem 3 (edge-dependent cancellation detector)

At least one of those eighteen mixed coefficients of `T` is nonzero.

### Proof

Suppose all eighteen vanish.  On a word `(a,b)` on `e` and `(c,c)` on `f`,
where `a,b,c` are distinct, every term containing a `D` block from either
other matching has a mixed `D` entry and vanishes.  All three `K_eK_f` terms
vanish by condition 2.  The remaining coefficient is

```text
(t-p_e) K_e(a,b) D_f(c,c).                            (23)
```

Conditions (21)--(22) force every off-diagonal entry of `K_e` to vanish.  The
six swapped words similarly diagonalize `K_f`.

For ordered `c!=d`, the `(c,c;d,d)` coefficient is now

```text
D_e^c D_f^d
 +(t-p_f) D_e^c K_f^d
 +(t-p_e) K_e^c D_f^d=0.                             (24)
```

Set

```text
r_e^c=-(t-p_e)K_e^c/D_e^c,
r_f^c=-(t-p_f)K_f^c/D_f^c.                           (25)
```

The six equations (24) become

```text
r_e^c+r_f^d=1       for c!=d.                        (26)
```

Over three colours their exact solution is

```text
r_e^0=r_e^1=r_e^2=r,
r_f^0=r_f^1=r_f^2=1-r.                               (27)
```

The diagonal physical block `K_e` has rank at most two, so one diagonal entry
vanishes.  By (21)--(22) and (25), `r=0`.  Equation (27) then makes all three
diagonal entries of `K_f` nonzero, contradicting `rank K_f<=2`.  `square`

The proof uses no equality among the six pair slopes and no rank-two local
frame, concision, or pure-output nonvanishing hypothesis.

## 4. Exact cancellation-locus residue on a witness

Return to one fixed graph, `Q`, contraction, GHZ basis, and complete companion
module.  Suppose the seven chosen `M`-active rows are legal constant operator
rows, all selected pair tensors are target-diagonal, and all three homogeneous
equations (18) vanish.

For a complementary partition define

```text
A_(ef)=product_(c=0)^2 D_e(c,c)D_f(c,c).              (28)
```

### Corollary 4.1 (nonzero four-port `Z` coefficient)

If `b_U!=0`, every surviving hypothetical witness satisfies

```text
A_(ef)=0      for all three complementary partitions. (29)
```

### Proof

Normalize the `M`-active four-port row, so `t!=0`.  From

```text
gamma_(ef)=(p_e-t)(p_f-t)-t^2=0,                     (30)
```

both differences in (21) are automatically nonzero.  If some `A_(ef)` were
nonzero, Theorem 3 would produce a mixed target coefficient.  `square`

On this nonzero-`t` chart, (30) is the graph of the **Wick involution**

```text
phi_t(p)=t p/(p-t).
```

It satisfies `phi_t(phi_t(p))=p`; its fixed points are exactly `p=0` and
`p=2t`, the two common-pair branches of `GLD17`.  Thus the generalized
cancellation locus consists of three independent complementary-pair fixed
points or nontrivial two-cycles of one involution.  The pole `p=t` is outside
this affine chart and is not a pure-axis extension of the detector.

### Corollary 4.2 (pure-`M` four-port axis)

If `b_U=0`, normalize to `t=0`.  Then every complementary partition satisfies

```text
p_e p_f=0,                                            (31)
```

or, homogeneously, `b_e b_f=0`.  Thus each complementary matching contains at
least one pure-`M` pair row.  Theorem 3 cannot fire on that matching because
both inequalities in (21) cannot hold.

Together, (29) and (31) give an exhaustive split **inside the generalized
cancellation locus**.  They do not say that a witness is forced onto that
locus.  If some `Gamma_(ef)` is nonzero, the noncancellation branch remains.

## 5. Exact controls and sharp boundaries

### 5.1 Response-visible and invisible module controls

The following are abstract quotient controls, not physical graphs or
witnesses:

- `C=K^2, R=0` realizes joint rank two;
- `C=K(1,p)` and one mixed response row `(-p,1)` realize a visible rank-one
  line with `C=ker R`;
- the same `C` with `R=0` realizes a response-invisible line;
- two visible lines `K(1,2)` and `K(1,3)` give a stacked rank-two response map
  and no common line;
- `C=0` permits an arbitrary response map.

These controls make every exception in Theorem 1 necessary.

### 5.2 Unequal pair slopes on the detector branch

Take `t=1`, the three complementary slope pairs

```text
(p_12,p_34)=(3/2,3),
(p_13,p_24)=(0,0),
(p_14,p_23)=(2,2),                                   (32)
```

and the physical rank-two channel `K_e=diag(2,-2,0)` on every edge.  All three
`gamma_(ef)` vanish.  Put `D_e=diag(2,-2,1)` on every edge and define
`B_e=D_e-p_eK_e`.  The partition `12|34` is three-full, its two slopes differ
from `t`, and the displayed mixed coefficient with colour `2` on `12` and
colour `0` on `34` is `-2`.  This is an exact physical response fixture on a
genuinely edge-dependent slope package.

### 5.3 Support-drop control with edge-dependent cancellation

Take `t=1`, `K_e=diag(2,0,0)`, and pair slopes

```text
(p_12,p_34)=(2,2),
(p_13,p_24)=(3,3/2),
(p_14,p_23)=(4,4/3).                                 (33)
```

Put colour `1` of `B` on edges `{12,23,34}`, colour `2` on `{13,24}`, and
put `B_e(0,0)=-2` on every edge.  Then all three `gamma_(ef)` vanish and

```text
T=(-12)e_0^tensor4+e_1^tensor4+e_2^tensor4           (34)
```

has no mixed coefficient.  The selected blocks have colour-zero values
`2(p_e-1)` but no complementary partition is three-full.  Thus the local
support divisor in (29) cannot simply be removed, even when the six pair
slopes are not synchronized.

### 5.4 Noncancellation control

The `GLD17` rank-two fixtures with `K_e=diag(2,-2,0)`, `p_e=1`, and `t=0`
have a three-full complementary pair, three-colour activity, and pure
four-port output, but `gamma_(ef)=1`.  One version has output
`3e_2^tensor4`; the matching-supported version has all three pure coefficients
equal to one.  Therefore target purity and full local support do not force
the cancellation equations.

All controls in Sections 5.2--5.4 are physical response windows only.  They
do not supply legal module rows, solve the full witness equation, identify
same-graph fibres, or refute the conjecture.

## 6. Globally decomposable channel: all common slopes excluded

There is one exact closure beyond the cancellation locus.  Assume all six
pair slopes have one common value `p`.  Put

```text
q=t-p,             r=p(p-2t),                         (35)
```

so Theorem 2 becomes

```text
T=C(D)+qX(D,K)+rC(K).                                (36)
```

Call the physical channel **globally decomposable** when there are port
covectors `a_u` such that

```text
K_uv=a_u tensor a_v.                                 (37)
```

Here (37) is written for `u<v`, and the reversed block is its transpose.  This
is a genuine physical subfamily: take `x_u=a_u` and `y_u=a_u/2`.  Global
vertex factorization is load-bearing; arbitrary edgewise rank-one blocks that
do not factor through one covector at each port are outside the statement.

### Theorem 4 (decomposable-channel all-slope exclusion)

Suppose all `D_e` are diagonal and one complementary pair `e|f` is
three-full.  If (37) holds, `T` cannot be mixed-free for any common pair slope
`p` and four-port slope `t`.  More precisely, the `q=0` and `r=0` branches
inherit the `GLD16` nine-word and `GLD17` eighteen-word detectors.  On the
remaining `qr!=0` branch, at least one coefficient in the following fixed set
of twenty-five mixed words is nonzero:

- the six ordered `(c,c;d,d)` words on the named pair `e|f` with `c!=d`;
- for each of the six edges `g` and each colour `c`, one `2+1+1` word with
  repeated colour `c` on `g` and the other two colours in a fixed order on its
  complement;
- one fixed `3+1` word, for example `(0,0,0,1)` after naming the ports.

### Proof

If `q=0`, three-fullness supplies the `GLD16` three-colour activity condition,
so its common-line detector applies.  If `r=0` and `q!=0`, `GLD17` applies.
It remains to assume

```text
q r !=0.                                             (38)
```

Write `e={i,j}`, `f={k,l}` and

```text
k_e^c=a_i^c a_j^c,
Z_e={c:k_e^c=0},                                     (39)
```

with analogous notation for `f`.  Suppose for contradiction that the
displayed twenty-five coefficients vanish.

For `c!=d`, the word `(c,c)` on `e` and `(d,d)` on `f` gives

```text
D_e^c D_f^d
 +q(D_e^c k_f^d+k_e^c D_f^d)
 +3r k_e^c k_f^d=0.                                 (40)
```

Indeed every one of the three complementary products in `C(K)` is the same
decomposable four-port monomial.  Equation (40) and three-fullness show that
there cannot be `c in Z_e`, `d in Z_f` with `c!=d`.

If `Z_e` is nonempty and `Z_f` is empty, choose `c in Z_e` and let `a,b` be
the other two colours.  Both endpoints of `f` have nonzero `a` and `b`
coordinates.  The `2+1+1` word with repeated colour `c` on `e` and colours
`a,b` on `f` has coefficient

```text
a_k^a a_l^b (q D_e^c+3r k_e^c)=q a_k^a a_l^b D_e^c,
```

which is nonzero.  If both zero sets are nonempty, the preceding no-distinct
zeros condition forces `Z_e=Z_f={c}`, and the same argument uses the other two
nonzero diagonal entries of `k_f`.  The symmetric cases exchange `e` and
`f`.  Hence

```text
Z_e=Z_f=empty.                                       (41)
```

The named partition covers all four ports, so every `a_u` has full ternary
support.  For any edge `g` and colour `c`, its complementary edge supports the
other two colours.  The corresponding `2+1+1` word therefore gives

```text
q D_g^c+3r k_g^c=0.                                  (42)
```

Finally evaluate a `3+1` word.  Its `C(D)` coefficient is zero.  Each of the
three matching contributions to `X(D,K)` equals `-3r/q` times the same
nonzero decomposable monomial `A`, while `C(K)=3A`.  Thus

```text
T_(3+1)=-9rA+3rA=-6rA !=0,                           (43)
```

contradicting mixed purity in characteristic zero.  `square`

The rank-two controls in Section 5.4 show that global decomposability is
load-bearing.  Three-fullness is also load-bearing inside the decomposable
class.  For any common unequal slopes `p!=t`, take `K_e=E_00` on every edge,
put colour `1` of `A=B+tK` on `{12,23,34}`, colour `2` on `{13,24}`, and no
colour-zero entry in `A`.  Then `D=A+(p-t)K` and

```text
T=-3t^2 e_0^tensor4+e_1^tensor4+e_2^tensor4          (44)
```

are target-diagonal.  At port `1`, the three activity products

```text
D_14^0 D_23^1,
D_12^1 D_34^0,
D_13^2 D_24^0
```

all equal `p-t` and are nonzero.  No edge belongs to both coloured support
families, so no edge is three-full.  Thus three-colour activity does not
replace the local support hypothesis.
Theorem 4 is a common-pair-slope result; it does not classify six arbitrary
edge-dependent slopes off the cancellation locus.

## 7. Exact frontier and scope ledger

```text
full-witness operator inclusion C_S subset ker R_S:        PROVED;
response-visible/invisible rank-one split:                 PROVED;
114-row common-line visibility test:                       PROVED;
full-nuisance denominator-cleared slope minors:            PROVED;
edge-dependent slope identity and homogeneous Gamma:       PROVED;
all-Gamma-zero eighteen-word detector:                     PROVED;
nonzero-t cancellation support divisor (29):               PROVED;
zero-t pure-M matching boundary (31):                       PROVED;
globally decomposable channel, all common slopes:            PROVED;
target shape alone forces operator supply:                 FALSE;
three-colour activity alone forces three-fullness:          FALSE;
pure output/full support forces cancellation:               FALSE;
all operator spaces nonzero on every witness:              UNKNOWN;
rank-one lines response-visible on every witness:           UNKNOWN;
some cancellation package forced on every witness:         UNKNOWN;
support divisor excluded by the full mixed equations:       UNKNOWN;
pure-Z, zero-space, invisible, and noncancellation residue:  UNKNOWN;
rank-two edge-dependent noncancellation classified:          UNKNOWN;
weighted permanent implication:                            UNKNOWN;
global Krenn--Gu conjecture:                               UNRESOLVED.
```

The breadth is one fixed graph, residual pair, contraction, four-port set,
its six pair targets, and the four-port target.  The module depth is the
complete nonempty-even fixed-`Q` deck through `GLD15`; the response depth is
pair and four-port.  The reconstructed object on a visible line is its
projective operator slope, not separate `M,Z`.  The ambiguity object is the
zero/pure-`Z`/rank-two/invisible/noncancellation/support-drop stratification.
There is no transition group.  The target implication is the fixed
eighteen-word contradiction after legal row attachment.  The permanent
implication is none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_fixed_q_response_visible_operator_slope_and_edge_dependent_cancellation.py
python -I claims/arbitrary-order/audit_fixed_q_response_visible_operator_slope_and_edge_dependent_cancellation.py
```

The primary exact replay uses symbolic matrices and polynomials to check the
minor charts, visibility branches, identity (17), all eighteen word formulas,
the ratio system, divisor split, and physical controls.  The independent
standard-library audit separately uses sparse polynomial dictionaries,
`Fraction` elimination, direct complementary-matching enumeration, and raw
endpoint vectors.  These scripts audit the bounded identities and examples.
The inherited `q=0` and `r=0` branches of Theorem 4 retain the already-audited
`GLD16` and `GLD17` detectors.  The full-nuisance operator argument,
arbitrary-field support proof, and legal attachment implication remain
load-bearing.
