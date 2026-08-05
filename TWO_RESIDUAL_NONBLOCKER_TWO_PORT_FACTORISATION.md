# Two-residual-nonblocker factorisation of the surplus-two port tensor

## Status

**Exact arbitrary-order characteristic-zero bridge theorem.**  Let `r`
fully supported pairwise-zero roots in a hypothetical three-colour GHZ
realization have exactly `r+2` blockers.  Suppose exactly two other vertices
`q0,q1` remain after the roots and blockers, and choose simultaneous-kernel
vectors at them with all three coordinates nonzero.

For blocker modes `u,v`, the residual two-port form is exactly

```text
W_uv=h*B_uv+a_u tensor b_v+b_u tensor a_v.            (1)
```

Here `h` is the residual edge value between `q0,q1`, while `a_u,b_u` are
the two blocker-to-residual covectors.  Moreover, exactly one of the
following holds on the two simultaneous-kernel spaces:

1. the residual edge restricts to a nonzero coordinate monomial; or
2. torus kernel vectors may be chosen with `h=0`, and (1) becomes the
   simultaneous two-row permanent factorisation.

In the second case the complete surplus-two cofactor is the restriction of
`P_(r+2)`.  Thus every such diagonal cofactor system forces both residual
port-row families to span the full target dual.  This is a reduction, not a
nonrestriction theorem: the coordinate-monomial alternative and the
all-full-span `P_(r+2)` systems remain open.  In particular it does not prove
`P_6` or `P_7` nonrestriction, the arbitrary-order local-to-global step, or
the global Krenn--Gu conjecture, which remains **UNRESOLVED**.

## Setup

Let `R` be the roots, `B` the blocker union, and

```text
|R|=r,       |B|=r+2,       Q={q0,q1}.                (2)
```

For each residual vertex put

```text
K_q=intersection_(i in R) ker B_iq(x_i,-).             (3)
```

Because `q0,q1` are not blockers for any colour, neither `K_q` is contained
in a coordinate hyperplane.  Hence each contains a vector with all three
coordinates nonzero.  Choose such vectors `z0 in K_q0`, `z1 in K_q1` and
define

```text
h=B_q0q1(z0,z1),
a_u(z)=B_uq0(z,z0),
b_u(z)=B_uq1(z,z1).                                   (4)
```

The root-to-blocker covectors are denoted `H_u[i,-]=B_iu(x_i,-)`.

## Exact four-vertex recursion

There are exactly three perfect matchings on `{u,v,q0,q1}`.  Expanding by
them gives

```text
H_{u,v,q0,q1}(z_u,z_v,z0,z1)
 =B_uv(z_u,z_v) B_q0q1(z0,z1)
  +B_uq0(z_u,z0) B_vq1(z_v,z1)
  +B_uq1(z_u,z1) B_vq0(z_v,z0),                      (5)
```

which is (1).  No division, genericity assumption, or finite-field
specialization is used.

The arbitrary-surplus matching identity therefore reads

```text
sum_(u<v) (h*B_uv+a_u b_v+b_u a_v)
            tensor P_r(H_w:w in B\{u,v})
 =sum_(c=0)^2 d_c e_c^(tensor(r+2)),                  (6)
```

with every `d_c` nonzero.

## Torus-zero versus coordinate-monomial dichotomy

Restrict the residual bilinear form to

```text
beta=B_q0q1 | (K_q0 x K_q1).                          (7)
```

Let `K^times` denote the complement in `K` of its three coordinate
hyperplanes.  Both `K_q0^times` and `K_q1^times` are nonempty dense opens.

Assume that `beta` has no zero on their product.  If its matrix rank is at
least two, its bilinear polynomial is irreducible.  Its zero hypersurface
would then be an irreducible subset of the finite union of the six coordinate
boundary divisors.  It would have to lie in one of them, which would make a
coordinate variable divide `beta`, contradicting rank at least two.

Thus `beta` has rank one and factors as `ell0*ell1`.  For each factor of
dimension at least two, the projective hyperplane `ell_j=0` has no torus
point.  Being irreducible and contained in the union of the three coordinate
hyperplanes, it equals one coordinate hyperplane section.  Hence `ell_j` is
proportional to a restricted coordinate covector.  If the corresponding
kernel space is one-dimensional, all its coordinate restrictions are
nonzero and proportional, so the same conclusion holds.  Therefore

```text
beta(z0,z1)=kappa*z0[c]*z1[d],       kappa!=0          (8)
```

on `K_q0 x K_q1`, for some colours `c,d`.

Conversely (8) has no zero on the torus product.  We have proved the exact
dichotomy

```text
torus zero h=0 exists,
or the residual restriction is a nonzero coordinate monomial.             (9)
```

This includes one-dimensional kernel spaces; they are not silently removed.

## Permanent extraction when `h=0`

Choose the torus zero from (9).  Then (6) has

```text
W_uv=a_u b_v+b_u a_v.                                (10)
```

Append the two common port rows `a,b` to the `r` root rows.  The unsigned
Laplace expansion of the `(r+2) x (r+2)` permanent along those final two
rows is

```text
P_(r+2)(H;a;b)
 =sum_(u<v) (a_u b_v+b_u a_v)
             tensor P_r(H_w:w in B\{u,v}).           (11)
```

Every monomial occurs exactly once: the pair `{u,v}` is the set of columns
used by the two port rows, their two assignments give the parenthesis in
(11), and the roots biject with the remaining columns.  Combining (6),
(10), and (11) gives

```text
P_(r+2) -> Delta_3.                                  (12)
```

The exact common-row full-span theorem applies to (12).  Consequently

```text
span{a_u:u in B}=(C^3)^*,
span{b_u:u in B}=(C^3)^*.                            (13)
```

If either family spans at most two, the torus-zero branch is impossible.
For four roots this extracts `P_6`; for five roots it extracts `P_7`.
Neither extraction is presently a contradiction in full generality.

## Boundary

```text
two residual nonblockers: exact recursion PROVED;
residual edge not coordinate-monomial: torus-zero factorisation PROVED;
factorised port-row spans: full span PROVED NECESSARY;
coordinate-monomial residual edge: UNKNOWN;
all-full-span P_(r+2) restriction: UNKNOWN;
three or more residual nonblockers: higher hafnian recursion not classified;
arbitrary-order local-to-global reduction: UNKNOWN;
global Krenn--Gu conjecture: UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_two_residual_nonblocker_two_port_factorisation.py
uv run --with sympy python audit_two_residual_nonblocker_two_port_factorisation.py
```

The primary checks the exact four-vertex matching recursion, the Laplace
bijection through seven rows, representative exact kernel-space torus-zero
and coordinate-monomial cases, and the theorem dependencies.  The audit has
no repository imports and independently rebuilds perfect matchings by a
subset recurrence and the port-row assignment ledger.  The projective
irreducibility argument above proves the dichotomy over `C`; the finite
replays audit its algebra and indexing and use no finite-field inference.
