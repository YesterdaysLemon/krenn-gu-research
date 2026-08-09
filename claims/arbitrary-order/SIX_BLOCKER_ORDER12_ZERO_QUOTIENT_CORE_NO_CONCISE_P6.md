# The quotient-zero cofactor core has no nonzero diagonal `P_6` pullback

## Status

**Exact characteristic-zero fixed-core obstruction.**  Consider the six
four-row matrices displayed in
[`SIX_BLOCKER_ORDER12_ZERO_QUOTIENT_COFACTOR_SYZYGY.md`](SIX_BLOCKER_ORDER12_ZERO_QUOTIENT_COFACTOR_SYZYGY.md).
They admit a unique blocker--blocker cofactor syzygy, up to scale, and that
syzygy was used there to realize `C_I=0` with all fifteen blocks nonzero.

For this same fixed common-row core, append *arbitrary* exchanged rows
`a_u,b_u in C^3` at each of the six modes and contract `P_6`.  If the resulting
six-mode tensor is GHZ diagonal, then it is the zero tensor.  In particular,
the core supports no concise restriction

```text
P_6 -> Delta_3,
```

and hence cannot support the quotient-zero `P^1 x P^1` surface from the
order-twelve classification.

This rules out the explicit common-row core only.  It does **not** rule out
other quotient-zero cores, the quotient-rank-one conic/rulings branch, an
unrestricted `P_6 -> Delta_3` restriction, or an arbitrary-order global
configuration.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## The fixed common-row core

For blocker modes `u=0,...,5`, take the four common-root row matrices

```text
H_0 = [-1 -2 -1;  0 -1  1; -1 -1 -2; -1 -1 -2],
H_1 = [ 0  0  0;  0  0  0;  0 -1 -2;  1  2  2],
H_2 = [ 2 -2  0;  0  0  1; -2  2  1;  2 -2  1],
H_3 = [-2  0  1;  2 -2  0;  0  0 -2; -2  0  2],
H_4 = [ 2 -2  0;  0 -1  0;  1  0 -1;  2  1 -2],
H_5 = [ 1  0  1;  0  2  0;  0  2  1; -1  2  0].       (1)
```

Their ranks are `(2,2,2,3,3,3)`.

For a target word `w in {0,1,2}^6` and a pair `u<v`, let

```text
K_uv(w)
 =per([H_m[root,w_m]]_(root=0,...,3; m notin {u,v})). (2)
```

Define the linear cofactor map on fifteen `3 x 3` blocks by

```text
[w] Lambda_H(W)
 =sum_(u<v) W_uv[w_u,w_v] K_uv(w).                    (3)
```

Deleting the three constant words gives the off-diagonal map

```text
Lambda_H^off:(Mat_3)^15 -> C^726.                     (4)
```

Exact rational row reduction gives

```text
rank_Q(Lambda_H^off)=134,      dim ker=1.              (5)
```

The nonzero generator `W_*` of that kernel is the fifteen-block collection
displayed in the preceding cofactor-syzygy theorem.  Direct evaluation of all
`3^6=729` coefficients gives the stronger identity

```text
Lambda_H(W_*)=0.                                      (6)
```

Thus the unique off-diagonal kernel line has zero diagonal image as well:

```text
ker(Lambda_H^off)=ker(Lambda_H)=<W_*>.                 (7)
```

## Laplace reduction of every appended-row permanent

Now choose arbitrary row covectors

```text
a_u=(a_u[0],a_u[1],a_u[2]),
b_u=(b_u[0],b_u[1],b_u[2])       (u=0,...,5),          (8)
```

with no rank, support, or proportionality assumption.  Let `Pi_H(a,b)` be
the pullback of `P_6` through the six source-by-target matrices whose rows at
mode `u` are

```text
[H_u; a_u; b_u].                                      (9)
```

Expanding the permanent along its last two source rows groups the two
possible assignments to every unordered pair `u<v`.  Put

```text
W_uv(a,b)=a_u^T b_v+b_u^T a_v,                        (10)
```

so entry `(c,d)` is

```text
a_u[c] b_v[d]+b_u[c] a_v[d].                          (11)
```

The expansion is the exact tensor identity

```text
Pi_H(a,b)=Lambda_H(W(a,b)).                            (12)
```

No use is made here of the graph edge blocks from the local cofactor model;
`W(a,b)` is simply the effective block collection produced by the two
appended permanent rows.

## Obstruction

Suppose `Pi_H(a,b)` is GHZ diagonal.  Its 726 off-diagonal coefficients
vanish, so by (5)--(7)

```text
W(a,b)=kappa W_*                                      (13)
```

for some scalar `kappa`.  Equations (6) and (12) then give

```text
Pi_H(a,b)=kappa Lambda_H(W_*)=0.                       (14)
```

Therefore this common-row core has no nonzero diagonal pullback at all.  In
particular, no choice of two exchanged pencils can produce the nonempty open
concise surface required by the quotient-zero branch.

The obstruction explains the earlier mixed-endpoint coefficient `44`
structurally: changing the exchanged root or port rows cannot repair that
failure while retaining the same six common matrices.  Any successful
quotient-zero model must change the common-row core so that its off-diagonal
cofactor kernel has nonzero diagonal image.

## Exact residual

```text
displayed quotient-zero cofactor core supports C_I=0: YES;
same core supports a nonzero diagonal P_6 pullback: NO;
all quotient-zero common-row cores: UNKNOWN;
quotient-rank-one synchronized P_6 curves: UNKNOWN;
arbitrary ambient/source/projective realization: UNKNOWN;
global Krenn--Gu conjecture: UNRESOLVED.
```

The next structural target is therefore a common-row classification by the
two integers

```text
dim ker(Lambda_H^off),
rank(Lambda_H restricted to ker(Lambda_H^off)).        (15)
```

A quotient-zero surface needs the second number to be positive; the explicit
local cofactor core has values `(1,0)`.

## Replay

```text
uv run --with sympy python claims/arbitrary-order/verify_six_blocker_order12_zero_quotient_core_no_concise_p6.py
python claims/arbitrary-order/audit_six_blocker_order12_zero_quotient_core_no_concise_p6.py
```

The primary verifier performs exact sparse rational row reduction of the
`726 x 135` off-diagonal matrix, checks all 729 coefficients of `W_*`, and
runs an indexing-sensitive 729-coefficient rational instance of the two-row
Laplace identity.  The general identity is the term-by-term expansion proved
above.  The independent audit reconstructs the matrix separately and uses
modular ranks only as a finite-field audit of the characteristic-zero
certificate.  No finite-field observation is used as the characteristic-zero
proof.
