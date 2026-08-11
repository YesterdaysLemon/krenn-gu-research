# Matrix-unit GHZ diagonal-torus polystability, endpoint balance, and active-transport sharpness

## Status

This is an exact arbitrary-order characteristic-zero theorem for the
matrix-unit branch.  A matrix-unit label support has one of two mutually
exclusive behaviours:

1. an integral diagonal one-parameter subgroup of the GHZ stabilizer gives
   every physical edge a nonnegative exponent and at least one edge a
   positive exponent; or
2. every physical edge occurs with positive integer multiplicity in an
   endpoint-label multicover whose colour loads are constant across all
   vertices.

The first behaviour gives an exact `t -> 0` realization of the same GHZ
tensor with strictly smaller physical support.  Consequently every
support-minimal matrix-unit witness has the second behaviour.  Explicitly,
there are integers

```text
m_e>0, q_c>0
```

such that, at every vertex `v` and for every colour `c`,

```text
sum_(e incident to v, ell_v(e)=c) m_e = q_c.        (1)
```

This is a strict support theorem.  The positive integers `m_e` are auxiliary
separating-dual weights, not the complex physical amplitudes `lambda_e`.

The condition is sharp at the active-word boundary.  An exact complete
eight-vertex table below satisfies (1) with every `m_e=1`, has maximum
torus-root number one, and has all three pure target coefficients equal to
one.  One active word and the forced ternary bridge-hexagon label pattern
produce a second active word, and both mixed coefficients cancel exactly in
two terms.  A different mixed coefficient is one, so the table is **not** a
Krenn--Gu witness.  Thus endpoint balance does not exclude the local algebra
of an active transport step or replace the remaining global mixed equations.

The `r=1` branch and the global Krenn--Gu conjecture remain
**UNKNOWN/UNRESOLVED**.

## 1. Matrix-unit incidence and the two alternatives

Let `Omega` be an even vertex set and let `E` be the nonzero physical
support.  On an edge `e={u,v}`, write

```text
B_e(x_u,x_v)
 = lambda_e x_u[ell_u(e)] x_v[ell_v(e)],
lambda_e !=0.                                       (2)
```

Let `H=Q^(Omega x {0,1,2})`.  For `beta in H`, put

```text
sigma_c(beta)=sum_(v in Omega) beta_(v,c),
L={beta:sigma_0(beta)=sigma_1(beta)=sigma_2(beta)=0},
r_e(beta)=beta_(u,ell_u(e))+beta_(v,ell_v(e)).       (3)
```

Call `beta in L intersect Z^(Omega x {0,1,2})` an **erasing GHZ direction**
when

```text
r_e(beta)>=0 for every e in E,
r_e(beta)>0 for at least one e.                     (4)
```

Call positive integers `(m_e)` an **endpoint-label balance** when there are
integers `(q_c)` satisfying (1).

### Theorem 1 (strict alternative)

Exactly one of the following holds:

```text
an erasing GHZ direction exists;
a positive integral endpoint-label balance exists. (5)
```

### Proof

Work first over `R`.  The rational linear map

```text
r:L_R -> R^E,       beta |-> (r_e(beta))_(e in E)   (6)
```

has image a linear subspace `S`.

If `S` contains a nonzero vector in the nonnegative orthant, normalize its
edge-coordinate sum to one.  The resulting nonempty polyhedron in the
`beta` variables is defined over `Q`, so it has a rational point.  Clearing
denominators gives an integral `beta` satisfying (4).

Suppose instead that

```text
S intersect R_(>=0)^E={0}.                          (7)
```

Then `S` is disjoint from the compact simplex

```text
K={y:y_e>=0, sum_e y_e=1}.                          (8)
```

Strictly separate `S` and `K`.  Because `S` is a subspace, the separating
functional must vanish on `S`; because every coordinate vertex of `K` lies
in `K`, its coefficient vector `p` satisfies

```text
p_e>0 for every e,       sum_e p_e r_e(beta)=0
for every beta in L_R.                               (9)
```

The subspace `S` is rational, and the inequalities `p_e>0` are open, so a
rational `p` can be chosen.  The second statement in (9) says that the
endpoint-load vector `r^T p` lies in `L_R^perp`, which is spanned by the
three colour-sum vectors.  Hence there are rational `q_c` such that

```text
sum_(e incident to v, ell_v(e)=c) p_e=q_c
for every v,c.                                      (10)
```

Clear all denominators to obtain (1) with `m_e>0` integral.

The alternatives cannot coexist.  Pairing an endpoint balance with an
erasing direction gives

```text
0 = sum_c q_c sigma_c(beta)
  = sum_e m_e r_e(beta) >0,                         (11)
```

where the strict inequality uses `m_e>0`, (4), and at least one positive
edge exponent.  This contradiction proves the exact alternative.

This is the finite-dimensional strict theorem of alternatives, proved here
directly so that no positivity is ever imposed on a physical amplitude.

## 2. The erasing direction really lowers support

### Theorem 2 (GHZ-preserving degeneration)

Suppose the matrix-unit graph satisfies

```text
T_W=Delta_(n,3)=sum_(c=0)^2 e_c^(tensor n)          (12)
```

and admits an erasing direction `beta`.  Then it has an exact realization
of the same tensor with strictly fewer nonzero physical blocks.

### Proof

For `t in C^*`, scale the colour-`c` covector at vertex `v` by
`t^(beta_(v,c))`.  Edge (2) becomes

```text
lambda_e t^(r_e(beta))
 x_u[ell_u(e)]x_v[ell_v(e)].                        (13)
```

The constant colour-`c` target term is scaled by

```text
t^(sigma_c(beta))=1,                                (14)
```

so the transformed graph still realizes (12) for every `t!=0`.

Every exponent in (13) is nonnegative.  Therefore every physical block has
a finite value at `t=0`: edges of exponent zero retain their nonzero blocks,
and edges of positive exponent vanish.  Perfect-matching coefficients are
polynomials in these finite edge entries.  Taking `t -> 0` in their exact
identities preserves (12).  At least one edge vanishes by (4), so physical
support strictly decreases.

Negative individual entries of `beta` cause no pole in a physical block:
only the edge exponents (13) enter the matrix-unit table, and all of those
are nonnegative.  The singularity of the auxiliary local scaling at `t=0`
is irrelevant to the finite limiting graph.

### Corollary 3 (support-minimal endpoint balance)

Every support-minimal matrix-unit realization of (12) has a positive
integral endpoint-label balance.

Moreover all three `q_c` in (1) are positive.  Indeed the nonzero constant
colour-`c` coefficient contains a pure-`c` perfect matching.  Every vertex
therefore has at least one incident edge whose local label is `c`; since
every `m_e` is positive, the common load `q_c` is positive.

Equivalently, replacing each physical edge by `m_e` formal parallel copies
produces an auxiliary multigraph in which every vertex has exactly `q_c`
incident half-edges labelled `c`, and every original physical edge occurs.
This multicover records incidence only.  It is not a positive-amplitude or
probabilistic representation of (12).

## 3. A balanced active transport table

Use vertices `0,...,7`.  Each entry below is
`(label at the smaller endpoint,label at the larger endpoint;weight)`:

```text
01=(0,0; 1)    02=(2,0; 1)    03=(0,0; 1)
04=(0,1;-1)    05=(1,1; 1)    06=(2,2; 1)
07=(1,0;-1/2)

12=(0,0; 1)    13=(2,2; 1)    14=(1,1; 1)
15=(1,2; 1)    16=(0,2; 1)    17=(2,1; 1)

23=(2,0; 1)    24=(0,0; 1)    25=(2,2; 1)
26=(1,1; 1)    27=(1,2; 1)

34=(1,0; 1)    35=(0,0; 1)    36=(2,1; 1)
37=(1,1; 1)

45=(0,0; 1)    46=(2,0; 1)    47=(2,2; 1)
56=(1,0; 1)    57=(0,0; 1)    67=(0,0; 1/2).       (15)
```

Every edge is present and is a nonzero matrix unit.  Thus evaluation on
two torus vectors is nonzero on every pair, and the maximum torus-root
number is exactly one.

### Theorem 4 (strict balance and pure targets)

Taking `m_e=1` for all 28 edges gives, at every vertex,

```text
(q_0,q_1,q_2)=(3,2,2).                              (16)
```

The three pure coefficients are all one.  Their nonzero matching terms are

```text
colour 0:
  01|24|35|67,       weight 1/2,
  03|12|45|67,       weight 1/2;

colour 1:
  05|14|26|37,       weight 1;

colour 2:
  06|13|25|47,       weight 1.                      (17)
```

### Proof

Directly count the endpoint labels in (15).  Each row has three local
zeroes, two local ones, and two local twos, proving (16).  For a constant
word, only edges labelled `(c,c)` at both endpoints are eligible.  Their
perfect matchings are exactly those in (17), and the displayed weights sum
to one in each colour.

### Theorem 5 (one exact bridge-pattern transport step)

Put

```text
chi_0=(0,1,2,0,1,2,0,0).                           (18)
```

Its complete compatible matching set is

```text
P=03|14|25|67,       diagonal,      weight  1/2,
F=04|15|23|67,       offdiagonal,   weight -1/2.    (19)
```

Hence

```text
D_(chi_0)=1/2,       Q_(chi_0)=-1/2.                (20)
```

The cross core of `F` is

```text
E=04|15|23.                                         (21)
```

It has one edge of each cross type.  Its only residual pure shore is the
nonzero edge `67`, so it is cofactor-active.  The ternary bridge hexagon is
present exactly:

```text
04=(0,1), 15=(1,2), 23=(2,0)
   force
24=(0,0), 05=(1,1), 13=(2,2).                      (22)
```

Together with `67`, those bridge edges induce the transported word

```text
chi_1=(1,2,0,2,0,1,0,0).                           (23)
```

That word is also exactly active.  Its complete compatible set is

```text
B=05|13|24|67,       diagonal,      weight  1/2,
F'=07|13|24|56,      offdiagonal,   weight -1/2,    (24)
```

so

```text
D_(chi_1)=1/2,       Q_(chi_1)=-1/2.                (25)
```

Thus (22) realizes the exact support, word change, and scalar equalities used
by the transport case of the active-word trichotomy, inside a strictly
endpoint-balanced support with exact pure targets.  Because table (15) is
not a full target realization, it is not asserted to occupy the geometric
no-deeper branch of the imported theorem.

At `chi_1`, the two cross edges `07` and `56` would require the binary
bridge edges `05=(0,0)` and `67=(1,1)` on the no-deeper branch.  Table (15)
instead has `05=(1,1)` and `67=(0,0)`.  It therefore fails that next forced
square support pattern.  It would be invalid to infer that this nonwitness
table enters the geometric deeper component; no active holonomy cycle is
claimed.

Finally, the mixed word

```text
(0,0,0,0,0,0,2,0)                                  (26)
```

has the unique compatible matching

```text
03|16|24|57
```

of weight one.  This proves directly that (15) is not a witness.  The table
is a sharpness model for the support theorem and one transport step only.

## 4. Exact scope and next obstruction

For a support-minimal hypothetical witness in the `r=1` matrix-unit branch:

```text
GHZ-preserving nonnegative edge degeneration:       IMPOSSIBLE;
strict positive endpoint-label multicover:          PROVED;
all three common endpoint loads are positive:       PROVED;
balance constrains complex physical amplitudes:     FALSE/NOT CLAIMED;
balance plus pure targets excludes local transport: FALSE;
balanced bridge-pattern transport algebra exists:   EXACT SHARPNESS;
balanced active holonomy cycle excluded:            UNKNOWN;
balanced deeper-blocker branch excluded:            UNKNOWN;
r=1 matrix-unit branch excluded:                    UNKNOWN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

The new condition should be intersected with the active-word response and
with the partial/deeper bridge topology.  It does not justify triangle
inequalities, positive matching measures, or cancellation-free hafnians:
the `m_e` solve a real incidence dual, while the `lambda_e` remain arbitrary
nonzero complex amplitudes.

In the title, diagonal-torus polystability means precisely the absence of an
erasing direction (4), equivalently the strict balance (1).  No statement
about stability under the full local general-linear group is intended.

## Replay

```powershell
python claims/arbitrary-order/verify_matrix_unit_ghz_diagonal_torus_polystability_endpoint_balance_and_active_transport_sharpness.py
python claims/arbitrary-order/audit_matrix_unit_ghz_diagonal_torus_polystability_endpoint_balance_and_active_transport_sharpness.py
python -m py_compile claims/arbitrary-order/verify_matrix_unit_ghz_diagonal_torus_polystability_endpoint_balance_and_active_transport_sharpness.py claims/arbitrary-order/audit_matrix_unit_ghz_diagonal_torus_polystability_endpoint_balance_and_active_transport_sharpness.py
python -m ruff check claims/arbitrary-order/verify_matrix_unit_ghz_diagonal_torus_polystability_endpoint_balance_and_active_transport_sharpness.py claims/arbitrary-order/audit_matrix_unit_ghz_diagonal_torus_polystability_endpoint_balance_and_active_transport_sharpness.py
```

The primary verifier checks the incidence dual identity, an explicit
erasing direction on the earlier six-vertex active table, all 105 matchings
of (15), the pure coefficients, both active fibres, the bridge hexagon, and
the exposed mixed word.  The independent no-import audit uses a separate
bitmask hafnian recursion, half-edge census, Laurent-exponent pairing, and
direct compatibility masks.  These bounded checks audit conventions and the
sharpness tables; the arbitrary-order result is the separation and exact
one-parameter proof above.
