# Matrix-unit GHZ moment-balanced gauge and unit-phase active-transport sharpness

## Status

This is an exact arbitrary-order theorem over `C` for the matrix-unit branch.
It strengthens the preceding endpoint-label balance theorem from auxiliary
incidence weights to the actual physical amplitudes after a
GHZ-preserving positive diagonal gauge.

For every support-minimal matrix-unit realization of

```text
T_W=Delta_(n,3),
```

there are positive local scale factors `s_(v,c)` with

```text
product_v s_(v,c)=1                                  (1)
```

for each colour `c`, such that the transformed physical amplitudes

```text
lambda'_e=s_(u,ell_u(e))s_(v,ell_v(e))lambda_e       (2)
```

have vertex-independent squared-magnitude colour loads:

```text
sum_(e incident to v, ell_v(e)=c) |lambda'_e|^2=q_c
for every v,c, with q_c>0.                           (3)
```

The gauge is unique modulo positive diagonal GHZ transformations that leave
every physical edge amplitude unchanged.  It is the unique minimizer, on
that quotient, of an explicit strictly convex coercive exponential
functional.  No appeal to a numerical optimizer or to a black-box
geometric-invariant-theory theorem is needed.

The conclusion is deliberately over `C`, not over an arbitrary
characteristic-zero field: complex absolute values, positive real scaling,
and real convexity are load-bearing.

The condition is phase-blind and sharp at the active-word boundary.  An
exact complete eight-vertex table over `Q(omega)`, where
`omega^2+omega+1=0`, has every physical amplitude of modulus one, already
satisfies (3) with loads `(3,2,2)`, and has all three pure coefficients one.
It nevertheless retains two exactly cancelling active fibres and the forced
ternary bridge transport between them.  A different mixed coefficient is
one, so the table is **not** a Krenn--Gu witness.  Its three colour
nonrigidity sets are all nonempty and proper.  Thus moment balance plus the
pure target coordinates does not synchronize phases, exclude local active
transport, or force proper nonrigidity sets to become global.

The `r=1` branch and the global Krenn--Gu conjecture remain
**UNKNOWN/UNRESOLVED**.

## 1. The real GHZ torus and strict support balance

Let `Omega` be an even vertex set.  On every nonzero physical edge
`e={u,v}`, write

```text
B_e(x_u,x_v)
 =lambda_e x_u[ell_u(e)]x_v[ell_v(e)],
lambda_e in C^*.                                    (4)
```

Let

```text
H_R=R^(Omega x {0,1,2}),
sigma_c(x)=sum_(v in Omega) x_(v,c),
L_R={x:sigma_0(x)=sigma_1(x)=sigma_2(x)=0},
r_e(x)=x_(u,ell_u(e))+x_(v,ell_v(e)).                (5)
```

The preceding
[`GHZ diagonal-torus endpoint-balance theorem`](MATRIX_UNIT_GHZ_DIAGONAL_TORUS_POLYSTABILITY_ENDPOINT_BALANCE_AND_ACTIVE_TRANSPORT_SHARPNESS_THEOREM.md)
proves that a support-minimal matrix-unit realization has positive numbers
`p_e` and common colour loads `b_c` satisfying

```text
sum_(e incident to v, ell_v(e)=c) p_e=b_c
for every v,c.                                      (6)
```

Indeed that theorem supplies positive integers.  Pairing (6) with `x in
L_R` gives

```text
sum_e p_e r_e(x)=sum_c b_c sigma_c(x)=0.             (7)
```

Put

```text
R:L_R -> R^E,       x |-> (r_e(x))_e,
S=R(L_R),
K=ker R.                                             (8)
```

Because every `p_e` is strictly positive, (7) implies that every nonzero
`z in S` has at least one positive and at least one negative coordinate.
Weak nonnegative balance would not be enough for this conclusion.

## 2. The convex moment functional

Put

```text
a_e=|lambda_e|^2>0
```

and define on `L_R`

```text
Phi(x)=sum_e a_e exp(2r_e(x)).                       (9)
```

It is constant on cosets of `K`, so it descends to `L_R/K`, identified
with `S` by `R`.

### Theorem 1 (coercive strict convexity on the quotient)

The descended functional is coercive and strictly convex.  Consequently it
has a unique minimizer `x_*+K`.

### Proof

Consider the unit sphere of the finite-dimensional subspace `S`.  For every
point `z` on it, (7) and `p_e>0` show that

```text
max_e z_e>0.
```

The maximum-coordinate function is continuous, so compactness gives a
constant `delta>0` such that

```text
max_e z_e>=delta ||z||
```

for all `z in S`.  Therefore

```text
sum_e a_e exp(2z_e)
 >=(min_e a_e) exp(2 delta ||z||)                    (10)
```

after selecting a maximizing coordinate.  This tends to infinity with
`||z||`, proving coercivity.

For `y in L_R`, the first and second directional derivatives are

```text
d Phi_x(y)=2 sum_e a_e exp(2r_e(x)) r_e(y),
d^2 Phi_x(y,y)=4 sum_e a_e exp(2r_e(x)) r_e(y)^2.    (11)
```

Every coefficient in the second sum is positive.  It vanishes exactly when
`r_e(y)=0` for all `e`, namely when `y in K`.  Thus the Hessian is positive
definite on `L_R/K`.  Coercivity gives existence of a minimizer and strict
convexity gives uniqueness there.

## 3. The actual-amplitude moment-balanced gauge

### Theorem 2 (GHZ-preserving moment normal form)

Let `x_*` represent the minimizer in Theorem 1 and set

```text
s_(v,c)=exp(x_*_(v,c)),
lambda'_e=exp(r_e(x_*))lambda_e,
mu_e=|lambda'_e|^2=a_e exp(2r_e(x_*)).               (12)
```

Then (1)--(3) hold.  The transformed graph realizes exactly the same tensor
`Delta_(n,3)`.  The resulting edge amplitudes are unique under positive
GHZ-torus scaling, and `x_*` is unique modulo `K`.

### Proof

The critical-point equation from (11) is

```text
sum_e mu_e r_e(y)=0        for every y in L_R.       (13)
```

The transpose incidence vector in (13) has coordinate

```text
h_(v,c)=sum_(e incident to v, ell_v(e)=c) mu_e.      (14)
```

The orthogonal complement of `L_R` consists exactly of arrays that are
constant in `v` separately for each colour.  Hence (13) is equivalent to

```text
h_(v,c)=q_c
```

for every `v,c`, proving (3).

Since `x_* in L_R`, one has

```text
product_v s_(v,c)=exp(sigma_c(x_*))=1.              (15)
```

Every coefficient of a word `chi` is multiplied by the nonzero scalar

```text
product_v s_(v,chi(v)).                              (16)
```

For a constant colour word this is one by (15), while every mixed target
coefficient was zero and remains zero after multiplication.  Thus the full
tensor `Delta_(n,3)`, not only its three pure entries, is fixed.

For each colour `c`, its target coefficient is one.  At least one pure-`c`
perfect matching therefore occurs, so every vertex is incident to a
physical edge labelled `c` at that endpoint.  Since every `mu_e` is
positive, (14) gives `q_c>0`.

Finally, strict convexity makes the edge-exponent vector `R(x_*)` unique.
Two representatives differ precisely by `K`, whose elements have zero
exponent on every physical edge.  This proves the uniqueness statement.

### Corollary 3 (support-minimal matrix-unit candidates)

Every globally support-minimal hypothetical matrix-unit witness over `C`
has a representative satisfying (3).  Conversely, the existence of
positive `mu_e` satisfying (3) rules out a nonzero nonnegative support-
erasing direction by pairing, but it does not imply any phase relation among
the `lambda'_e`.

The phrase **moment-balanced gauge** in this document refers only to the
connected positive real part of the diagonal GHZ stabilizer.  No stability
or normal form under the full local general-linear group is claimed.

## 4. Exact unit-phase active-transport table

Let `omega` be a primitive cube root of unity:

```text
omega^2+omega+1=0.
```

Use vertices `0,...,7`.  Each entry is
`(label at the smaller endpoint,label at the larger endpoint;weight)`:

```text
01=(0,0;-omega)   02=(2,0;1)   03=(0,0;1)
04=(0,1;-1)       05=(1,1;1)   06=(2,2;1)
07=(1,0;-1)

12=(0,0;-omega^2) 13=(2,2;1)   14=(1,1;1)
15=(1,2;1)        16=(0,2;1)   17=(2,1;1)

23=(2,0;1)        24=(0,0;1)   25=(2,2;1)
26=(1,1;1)        27=(1,2;1)

34=(1,0;1)        35=(0,0;1)   36=(2,1;1)
37=(1,1;1)

45=(0,0;1)        46=(2,0;1)   47=(2,2;1)
56=(1,0;1)        57=(0,0;1)   67=(0,0;1).          (17)
```

Every edge is present and every weight belongs to `Q(omega)^*`.  Each of
the four exceptional phases has modulus one, as do all remaining weights.

### Theorem 4 (actual moment balance and pure targets)

The actual squared-magnitude load at every vertex is

```text
(q_0,q_1,q_2)=(3,2,2).                              (18)
```

Thus (17) is already at its moment-balanced point.  Its three pure
coefficients are all one.  The complete pure matching terms are

```text
colour 0:
  01|24|35|67,       weight -omega,
  03|12|45|67,       weight -omega^2;

colour 1:
  05|14|26|37,       weight 1;

colour 2:
  06|13|25|47,       weight 1.                      (19)
```

Indeed `-omega-omega^2=1`.  Notice that the pure zero coefficient already
uses phase addition; moment balance does not make its individual terms
positive real.

For this table the real zero-colour-sum Lie algebra has dimension `21`, the
edge-exponent map has rank `20`, and its kernel has dimension one.  The
Hessian of (9) has the same rank.  This audits the quotient in Theorem 1 on
a nontrivial stabilizer example rather than assuming the action is free.

## 5. Exact active transport survives the gauge

Put

```text
chi_0=(0,1,2,0,1,2,0,0).                           (20)
```

Its complete compatible matching set is

```text
P=03|14|25|67,       diagonal,      weight  1,
F=04|15|23|67,       offdiagonal,   weight -1.       (21)
```

Hence its total coefficient is zero and

```text
D_(chi_0)=1,       Q_(chi_0)=-1.                    (22)
```

The cross core of `F` has exactly the forced ternary bridge pattern

```text
04=(0,1), 15=(1,2), 23=(2,0)
   force
24=(0,0), 05=(1,1), 13=(2,2).                      (23)
```

Together with residual edge `67`, the bridge matching induces

```text
chi_1=(1,2,0,2,0,1,0,0).                           (24)
```

That word also has exactly two compatible terms:

```text
B =05|13|24|67,      diagonal,      weight  1,
F'=07|13|24|56,      offdiagonal,   weight -1,       (25)
```

so `D_(chi_1)=1`, `Q_(chi_1)=-1`, and its total coefficient is zero.
Thus actual moment balance, unit magnitudes, exact pure targets, and the
support and scalar algebra of one active transport step coexist.

As in the preceding rational sharpness theorem, this table is not a full
target realization and is not asserted to occupy the geometric no-deeper
branch of the imported bridge theorem.  In particular, failure of its next
selected square pattern is not evidence of geometric deeper-component
entry.

The mixed word

```text
(0,0,0,0,0,0,2,0)                                  (26)
```

has the unique compatible matching

```text
03|16|24|57
```

of weight one.  This is an exact exposed violation of the target and proves
that (17) is not a witness.

## 6. Proper nonrigidity sets also survive

For a colour `c`, use the existing definition

```text
S_c={v: some edge vw has ell_v(vw)!=c and ell_w(vw)=c},
R_c=Omega-S_c.                                      (27)
```

Directly from (17),

```text
S_0={0,2,3,4,5,6},       R_0={1,7},
S_1={0,1,3,4,5,6,7},     R_1={2},
S_2={1,2,3,6,7},         R_2={0,4,5}.               (28)
```

All three `S_c` are nonempty and proper.  Therefore strict support balance,
actual moment balance, unit magnitudes, and the three pure target equations
do not by themselves prove the still-open proper-set propagation step.
Because (17) violates another mixed equation, (28) does not refute a
propagation theorem that uses the complete target system.

## 7. Exact scope and next obstruction

For a support-minimal hypothetical witness in the `r=1` matrix-unit branch:

```text
positive integral endpoint-label balance:          PROVED;
positive GHZ gauge balancing actual |lambda_e|^2:  PROVED over C;
existence and uniqueness modulo edge stabilizer:   PROVED;
all three common actual loads q_c positive:         PROVED;
moment balance aligns or restricts edge phases:     FALSE/NOT CLAIMED;
moment balance plus pure targets excludes transport:FALSE;
moment balance plus pure targets forces S_c=Omega:  FALSE;
full target equations force proper-set propagation:UNKNOWN;
pure-shore cancellation and active holonomy:        UNKNOWN;
deeper-blocker branch:                              UNKNOWN;
r=1 matrix-unit branch:                             UNKNOWN;
global Krenn--Gu conjecture:                        UNRESOLVED.
```

The new normal form removes edge-magnitude imbalance as an independent
degree of freedom.  What remains in the active branch is genuinely joint:
the phases, all mixed coefficient sums, the active-word holonomy or
pure-shore cancellation exit, and the geometric deeper alternative must be
coupled.  Convexity of squared magnitudes cannot be reused as convexity of
complex matching coefficients.

## Replay

```powershell
python claims/arbitrary-order/verify_matrix_unit_ghz_moment_balanced_gauge_and_unit_phase_active_transport_sharpness.py
python claims/arbitrary-order/audit_matrix_unit_ghz_moment_balanced_gauge_and_unit_phase_active_transport_sharpness.py
python -m py_compile claims/arbitrary-order/verify_matrix_unit_ghz_moment_balanced_gauge_and_unit_phase_active_transport_sharpness.py claims/arbitrary-order/audit_matrix_unit_ghz_moment_balanced_gauge_and_unit_phase_active_transport_sharpness.py
python -m ruff check claims/arbitrary-order/verify_matrix_unit_ghz_moment_balanced_gauge_and_unit_phase_active_transport_sharpness.py claims/arbitrary-order/audit_matrix_unit_ghz_moment_balanced_gauge_and_unit_phase_active_transport_sharpness.py
```

The primary verifier uses exact rational arithmetic and the basis
`1,omega` of `Q(omega)`.  It enumerates all 105 perfect matchings, checks the
actual moment loads, computes the rational incidence and Hessian ranks,
replays a nontrivial exact rational GHZ gauge, and verifies the pure,
active, bridge, exposed-word, and nonrigidity data.  The independent audit
imports no primary code.  It uses decimal endpoint codes, a least-set-bit
compatible-hafnian recursion, an alternate colour-sum anchor, modular rank
with an explicit exact stabilizer, and a separate direct half-edge census.
These bounded checks audit the conventions and sharpness table.  The
arbitrary-order theorem is the convex proof in Sections 1--3.
