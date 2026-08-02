# Coordinate-monomial two-residual slice universality no-go theorem

## Status

**Exact arbitrary-`r` characteristic-zero local-slice theorem.**  Let
`r>=2`, put `m=r+2`, and suppose a blocker-admissible surplus-two cofactor
datum `(H,W)` satisfies

```text
Lambda_H(W)=sum_(c=0)^2 d_c e_c^(tensor m),
d_0 d_1 d_2!=0.                                    (1)
```

Then `(H,W)` has an exact local edge realization with `r` fully supported
pairwise-zero roots, exactly `m` blockers, exactly two residual vertices,
one-dimensional torus simultaneous kernels at both residual vertices, and a
nonzero coordinate-monomial residual edge.  On the root/kernel slice, the
matching identity is exactly (1).

Consequently the coordinate-monomial residual-edge branch cannot be
excluded by the surplus-two cofactor equation, blocker incidence, root-row
span, or matching recursion alone.  It is slice-universal for the unresolved
blocker-admissible cofactor incidence.  Any proof excluding it must use
compatibility away from the fixed root/kernel slice or another genuinely
global condition.

This is a **no-go theorem for a proof route**, not a Krenn--Gu counterexample.
The constructed edge data are not asserted to satisfy the full unspecialized
global GHZ identity.  The all-full-span cofactor incidence, all-full-span
`P_(r+2)` restrictions, arbitrary-order local-to-global reduction, and the
global Krenn--Gu conjecture remain **UNKNOWN** or **UNRESOLVED**.

## Input cofactor datum

Let `B={u_0,...,u_(m-1)}`.  For each blocker mode `u`, let

```text
H_u in Mat_(r x 3),                                 (2)
```

and for each unordered pair `u<v`, let `W_uv` be a bilinear form on the two
blocker modes.  Define

```text
Lambda_H(W)
 =sum_(u<v) W_uv tensor P_r(H_w:w in B\{u,v}).      (3)
```

Blocker-admissible means that for every `u`, the row span of `H_u` contains
at least one coordinate covector.  This is exactly the local condition that
every vertex of `B` belongs to the root blocker union.  Equation (1) is the
smallest currently unresolved surplus-two algebraic object after the known
full-root-row-span theorem.

## Universal torus-line construction

Work in `V=Qbar^3` and put

```text
v=(1,1,1),
g_0=e_0^*-e_2^*,       g_1=e_1^*-e_2^*.            (4)
```

Choose fully supported root vectors

```text
x_0=(d_0,d_1,d_2),       x_i=v for i>0,             (5)
```

and covectors `ell_i` with `ell_i(x_i)=1`; for example
`ell_i=e_0^*/x_i[0]`.  Define the root edges by

```text
B_(i,u)(z_i,z_u)=ell_i(z_i) H_u[i,-](z_u),
B_(i,j)=0 for distinct roots i,j.                   (6)
```

For each residual vertex `q_j`, define

```text
B_(i,q_j)(z_i,z)=ell_i(z_i) g_i(z) for i=0,1,
B_(i,q_j)=0 for i>1.                                (7)
```

Then

```text
K_(q_j)=intersection_i ker B_(i,q_j)(x_i,-)
       =ker g_0 intersect ker g_1
       =span(v).                                    (8)
```

No coordinate covector lies in `span(g_0,g_1)=v^perp`, because every
coordinate covector is nonzero on `v`.  Hence both `q_0,q_1` are genuine
nonblockers for all three colours.  By blocker-admissibility and (6), the
root blocker union is exactly `B`.

Put

```text
B_(q_0,q_1)(z_0,z_1)=z_0[0] z_1[0].                (9)
```

On `K_(q_0) x K_(q_1)`, (9) is the nonzero coordinate monomial required by
the unresolved branch.  At the torus vectors `z_0=z_1=v`, its value is
`h=1`.

## Arbitrary-cofactor sector

Set every blocker--residual edge to zero and set

```text
B_(u,v)=W_uv.                                      (10)
```

After fixing the roots at (5) and both residual vertices at `v`, every
surviving perfect matching has exactly this form:

1. `q_0` pairs with `q_1`;
2. the `r` roots pair bijectively with `r` blockers;
3. the two unused blockers `u,v` pair through `W_uv`.

The matching sum is therefore exactly (3), term by term.  The restricted
GHZ coefficients are

```text
product_i x_i[c] v[c] v[c]=d_c,                    (11)
```

so the sliced identity is precisely (1).  In the notation of the certified
two-residual recursion,

```text
h=1,       a_u=b_u=0,       h B_uv=W_uv.            (12)
```

Thus the coordinate-monomial branch retains arbitrary blocker-pair
cofactors; it does not force a new rank or factorization condition.

## Embedded all-full-span permanent branch

Suppose the unresolved datum is factorized by two common port-row families,

```text
W_uv=a_u tensor b_v+b_u tensor a_v.                (13)
```

Set the blocker--blocker edges to zero and instead define

```text
B_(u,q_0)(z_u,z_0)=a_u(z_u) z_0[0],
B_(u,q_1)(z_u,z_1)=b_u(z_u) z_1[0].                (14)
```

At `z_0=z_1=v`, the two assignments of the residual vertices to an unused
blocker pair give exactly (13).  Matchings in which `q_0,q_1` pair together
vanish because the remaining blocker pair has zero edge.  The full sum is
the unsigned Laplace expansion

```text
P_m(H;a;b)=Lambda_H(W).                            (15)
```

Therefore every blocker-admissible all-full-span `P_(r+2)` diagonal system
embeds into the coordinate-monomial residual-edge branch, while preserving
the full spans of all root and port row families.  Excluding the coordinate
branch locally would in particular exclude this already open permanent
subproblem.

## Exact barrier

The smallest remaining cofactor object is the saturated incidence

```text
I_(r,2)^block = {
  (H,W): offdiag Lambda_H(W)=0,
         diag Lambda_H(W) in (C^*)^3,
         every H_u is blocker-admissible
}.                                                   (16)
```

The known first-polar theorem forces every persistent root-row family
`{H_u[i,-]:u in B}` to span the full target dual on (16), but does not prove
that (16) is empty.  Its factorized subvariety is the all-full-span
`P_(r+2)` restriction incidence (15).  The construction above proves that
neither object becomes smaller merely by naming the residual edge
coordinate-monomial.

What remains unavailable is an equation coupling this slice to other root
choices or to unfixed residual directions.  That is the precise missing
local-to-global input; broad elimination of (9) alone cannot supply it.

## Replay

Replay the dependency first:

```powershell
uv run --with sympy python verify_two_residual_nonblocker_two_port_factorisation.py
uv run --with sympy python audit_two_residual_nonblocker_two_port_factorisation.py
```

Then run:

```powershell
uv run --with sympy python verify_two_residual_coordinate_monomial_slice_universality_nogo.py
uv run --with sympy python audit_two_residual_coordinate_monomial_slice_universality_nogo.py
```

The primary reconstructs (4)--(12) exactly, checks the surviving matching
classes and the factorized Laplace sector through eight roots, and verifies
the coefficient scaling.  The audit imports no project code and uses a
separate anchored perfect-matching recurrence and assignment ledger.
Neither replay uses a finite field.
