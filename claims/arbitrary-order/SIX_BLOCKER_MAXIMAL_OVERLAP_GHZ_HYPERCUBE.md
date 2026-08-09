# Maximal-overlap `P_6` restrictions lie in one GHZ coefficient hypercube

## Status

**Exact arbitrary-order characteristic-zero compatibility theorem.**  In a
hypothetical global Krenn--Gu witness, suppose two five-root first-surplus
configurations share four roots and the same six blockers.  At every residual
vertex choose one torus simultaneous-kernel vector for each root marking.
The two extracted `P_6` restrictions are then opposite corners of one Boolean
family of six-blocker tensors.  Every corner has an exact four-root/two-port
cofactor expansion, and the three GHZ coefficient arrays are rank-one Segre
cubes.  Equivalently, every Boolean square minor of each colour's coefficient
array vanishes.

This is the global compatibility missing from the local port-freedom theorem
[`SIX_BLOCKER_NONZERO_CROSS_PORT_FREEDOM.md`](SIX_BLOCKER_NONZERO_CROSS_PORT_FREEDOM.md).
It holds with zero or nonzero exchanged-root coupling and at every even
ambient order.  It does **not** directly identify the opposite `P_6`
pullbacks: the intermediate corners are genuine companion cofactor tensors,
not further first-surplus permanent restrictions.  No contradiction is
derived here.  The arbitrary-order local-to-global reduction remains
**UNKNOWN**, and the global Krenn--Gu conjecture remains **UNRESOLVED**.

## Two overlapping first-surplus systems

Let `Omega` be an even vertex set and let the global perfect-matching form
satisfy

```text
H_W((z_v)_(v in Omega))
  =sum_(c=0)^2 product_(v in Omega) z_v[c].             (1)
```

Let

```text
I={0,1,2,3},       R=I union {a},       R'=I union {b}
```

be pairwise zero-coupled, fully supported root sets.  Assume that both have
the same total blocker union

```text
B={u_0,...,u_5}.
```

Put

```text
Q=Omega minus (I union {a,b} union B).                  (2)
```

Since `|Omega|` is even, `|Q|` is even.  Relative to `R`, the residual
nonblocker set is `{b} union Q`; relative to `R'`, it is `{a} union Q`.
Choose the torus kernel vectors used in the two one-port extractions:

```text
z_b^0 in K_b(R),          z_q^0 in K_q(R),
z_a^1 in K_a(R'),         z_q^1 in K_q(R')             (3)
```

for every `q in Q`.  They exist by the usual finite-union argument over
`C`, because these vertices are outside the common blocker union.

Let

```text
E={a,b} union Q
```

and attach two vectors to every `v in E`:

```text
p_a^0=x_a,       p_a^1=z_a^1,
p_b^0=z_b^0,     p_b^1=x_b,
p_q^0=z_q^0,     p_q^1=z_q^1.                          (4)
```

Every vector in (4) is fully supported.  More importantly, both choices at
every residual vertex annihilate all four common-root incident covectors:

```text
B_iv(x_i,p_v^epsilon)=0
for i in I, v in E, epsilon in {0,1}.                   (5)
```

For `a,b`, (5) uses zero coupling within one root marking and the opposite
port condition.  For `q`, both kernel spaces in (3) contain the four common
root constraints.

## The common cofactor master

For a Boolean word `epsilon in {0,1}^E`, fix the common roots to `x_i`, fix
each residual vertex `v` to `p_v^(epsilon_v)`, and leave the six blocker modes
free.  Call the resulting six-mode tensor `T_epsilon`.

No surviving matching contains a common-root--common-root edge or, by (5), a
common-root--residual edge.  The four common roots therefore pair with four
distinct blockers.  If `S` is the pair of unused blockers, the remaining
matching lives on `E union S`.  Thus, term by term,

```text
T_epsilon(z_B)
 =sum_(S subset B, |S|=2)
    per([B_iu(x_i,z_u)]_(i in I,u in B\S))
    H_(E union S)((p_v^(epsilon_v))_(v in E),(z_u)_(u in S)).      (6)
```

This is exactly the surplus-two cofactor formula with four roots, six
blockers, and the even residual set `E`.  It is valid for arbitrary even
`|Omega|`; no order-twelve truncation is used.

Restricting the right side of (1) gives

```text
T_epsilon(z_B)
 =sum_(c=0)^2 Lambda_(c,epsilon) product_(u in B) z_u[c],          (7)

Lambda_(c,epsilon)
 =product_(i in I)x_i[c] product_(v in E)p_v^(epsilon_v)[c].      (8)
```

Every coefficient in (8) is nonzero.

## Segre compatibility of every corner

For fixed colour `c`, equation (8) is a pure tensor across the Boolean
factors.  If `v,w in E` are distinct and `epsilon` has zeroes in those two
positions, then

```text
Lambda_(c,epsilon)
Lambda_(c,epsilon+e_v+e_w)
 =Lambda_(c,epsilon+e_v)
  Lambda_(c,epsilon+e_w).                             (9)
```

Equivalently, every two-dimensional face of the coefficient hypercube has
rank one.  Along a single residual coordinate,

```text
Lambda_(c,epsilon+e_v)/Lambda_(c,epsilon)
 =p_v^1[c]/p_v^0[c],                                  (10)
```

independent of every other bit.  Equations (9)--(10) are basis-free after
interpreting (8) as the Segre tensor of the two evaluation vectors at each
residual vertex.

## The two endpoint corners are exactly the `P_6` extractions

At `epsilon=0`, vertex `a` is fixed to `x_a` while every vertex of
`{b} union Q` is fixed to its `R`-kernel vector.  Hence `a` has zero coupling
to every other residual vertex.  For `S={u,v}`, the residual factor in (6)
expands as

```text
H_(E union {u,v})
 =B_au(x_a,z_u) g_v^R(z_v)
  +B_av(x_a,z_v) g_u^R(z_u),                          (11)
```

where

```text
g_u^R(z_u)=H_({u,b} union Q)(z_u,z_b^0,(z_q^0)_q).    (12)
```

Substituting (11) into (6) is the two-row Laplace expansion of the permanent
with rows

```text
(B_iu(x_i,-))_(i in I),       B_au(x_a,-),       g_u^R.            (13)
```

Therefore `T_0` is precisely the first `P_6` pullback supplied by the
odd-residual one-port theorem.  At `epsilon=1`, the symmetric expansion with
`b=x_b` and the `R'` kernel vectors proves that `T_1` is precisely the second
`P_6` pullback.

The endpoint coefficient triples are

```text
Lambda_(c,0)
 =product_(i in I)x_i[c] x_a[c] z_b^0[c]
  product_(q in Q)z_q^0[c],

Lambda_(c,1)
 =product_(i in I)x_i[c] z_a^1[c] x_b[c]
  product_(q in Q)z_q^1[c].                           (14)
```

This recovers the earlier order-twelve ratio formula when `Q` is empty.

## Why the compatibility is not yet a contradiction

Equation (9) relates opposite endpoints only through the other
`2^|E|-2` corners.  At a mixed corner, neither `a` nor `b` is generally an
additional root whose edges to all other residual vertices vanish.  Its
factor in (6) is therefore a genuine joint residual matching form.  Such a
corner need not be a pullback of `P_6`, and the completed `P_5` component
classification does not apply to it automatically.

The exact frontier is consequently

```text
common arbitrary-order GHZ hypercube: PROVED;
endpoint P_6 restrictions: PROVED;
elimination of the companion cofactor corners: UNKNOWN;
deduction of a forbidden P_5/P_6 restriction: UNKNOWN;
global Krenn--Gu conjecture: UNRESOLVED.
```

A successful local-to-global theorem must now obstruct the whole cofactor
hypercube, rather than seek a pairwise row identity between its two endpoint
permanents.

## Replay

```text
python verify_six_blocker_maximal_overlap_ghz_hypercube.py
python audit_six_blocker_maximal_overlap_ghz_hypercube.py
```

The primary verifier compares the surviving matching monomials with (6) and
with both endpoint `P_6` Laplace expansions for residual sets of sizes zero,
two, and four.  It also checks every Boolean square minor in exact rational
sample cubes.  The no-import audit uses a separate hafnian dynamic program,
deterministic rational edge weights, and independent coefficient data.  The
finite computations replay the combinatorial identities; the written
argument proves the arbitrary-order characteristic-zero statement.  No
finite-field inference is used.
