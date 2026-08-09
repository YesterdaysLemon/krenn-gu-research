# Root-tangent companions are necessary beyond the coordinate-monomial slice

## Status

**Exact arbitrary-order characteristic-zero tangent no-go.**  Consider the
two-residual coordinate-monomial slice realization from
[`TWO_RESIDUAL_COORDINATE_MONOMIAL_SLICE_UNIVERSALITY_NOGO.md`](TWO_RESIDUAL_COORDINATE_MONOMIAL_SLICE_UNIVERSALITY_NOGO.md).
It realizes every blocker-admissible surplus-two cofactor identity after the
roots and residual kernels have been fixed.  No such realization, with its
rank-one root endpoints and zero tangent companions, can satisfy the full
unspecialized three-colour GHZ identity.

More generally, at any fully supported root `i` of a hypothetical global
witness, at least one of the following must occur:

1. the root--blocker covectors vary nonprojectively to first order at `x_i`;
2. the root--root and root--residual first-order evaluation covectors that
   actually carry nonzero companion cofactors span the full tangent
   annihilator `x_i^perp`, hence have dimension exactly two.

In particular, one isolated tangent companion cannot repair a projectively
constant root--blocker derivative.

This proves a necessary off-slice escape, not the impossibility of the whole
coordinate-monomial branch.  The companion terms may exist and may repair
the tangent identity.  Their classification, the arbitrary-order
local-to-global reduction, and the global Krenn--Gu conjecture remain
**UNKNOWN** or **UNRESOLVED**.  No finite field is used.

## Tangent setup

Fix `r>=2` fully supported pairwise-zero roots, `m=r+2` blockers, and two
residual nonblockers.  After fixing all roots and residual kernel vectors,
suppose the blocker tensor is the concise diagonal

```text
Lambda=sum_(c=0)^2 d_c e_c^(tensor m),
d_0*d_1*d_2!=0.                                    (1)
```

Fix one root `i`, write its vector as

```text
x_i=(x_0,x_1,x_2),       x_0*x_1*x_2!=0,           (2)
```

and vary it to `x_i+epsilon*y`.  Assume first that all root--blocker edges
have a common left endpoint to first order: there is one covector `ell_i`
such that for every blocker `u`,

```text
B_(i,u)(x_i,-)=H_u[i,-],
B_(i,u)(y,-)=ell_i(y) H_u[i,-].                    (3)
```

Also assume the tangent companion evaluations vanish:

```text
B_(i,j)(y,x_j)=0                 for every other root j,
B_(i,q)(y,z_q)=0                 for both residual vertices q.          (4)
```

Equations (3)--(4) hold in the slice-universality construction: its
root--blocker blocks are `ell_i tensor H_u[i,-]`, its root--root blocks are
zero, and its root--residual blocks evaluate through covectors vanishing on
the chosen residual kernel vector.

## Derivative of the matching side

Every matching that survives at the fixed slice pairs root `i` to exactly one
blocker.  By (3), differentiating that edge multiplies its full matching
monomial by the same scalar `ell_i(y)`.  A matching containing a root--root
or root--residual edge cannot contribute a first derivative by (4).  Hence
the complete derivative of the blocker tensor is

```text
d/d epsilon|_0 Lambda(x_i+epsilon*y)
  =ell_i(y) Lambda.                                  (5)
```

This is termwise and allows arbitrary blocker--blocker cofactors.  No
factorization of those cofactors is used.

## Derivative of the GHZ side

The colour-`c` coefficient in (1) contains the root factor `x_c`.  Therefore
the same derivative on the target side is

```text
sum_(c=0)^2 d_c * (y_c/x_c) * e_c^(tensor m).       (6)
```

Comparing the three nonzero diagonal coefficients in (5) and (6) gives, for
every tangent vector `y`,

```text
ell_i(y)=y_0/x_0=y_1/x_1=y_2/x_2.                  (7)
```

No linear form satisfies (7).  Taking `y=e_0` makes its middle expression
zero and its first expression `1/x_0!=0`.  Equivalently, coefficient
comparison would require the same covector to equal all three independent
coordinate covectors

```text
ell_i=e_0^*/x_0=e_1^*/x_1=e_2^*/x_2.              (8)
```

This contradiction proves the tangent no-go.

## One companion is still insufficient

The same derivative comparison gives a sharper rank statement.  Keep the
projectively constant hypothesis (3), but now allow root--root and
root--residual tangent companions.  Each companion edge contributes a fixed
blocker tensor multiplied by one covector in `y`.  If the span of all such
effective companion covectors has dimension `t`, the derivative map from the
three-dimensional root tangent space has image dimension at most

```text
1+t.                                                 (9)
```

The `1` is the scalar row-replacement term `ell_i(y)Lambda`.  On the GHZ
side, (6) has coefficient matrix

```text
diag(d_0/x_0,d_1/x_1,d_2/x_2),                     (10)
```

which has rank three.  Therefore `1+t>=3`, so

```text
t>=2.                                                (11)
```

Thus a globally extendable coordinate slice with projectively constant
root--blocker tangent rows requires at least two linearly independent
effective root--root/root--residual companion covectors at every root.

## The companion span is exactly the tangent annihilator

The upper bound is forced by the original slice incidence.  For another root
`j`, its companion covector at root `i` is

```text
phi_ij(y)=B_ij(y,x_j).
```

Pairwise-zero roots give `B_ij(x_i,x_j)=0`, so `phi_ij(x_i)=0`.  Likewise a
residual kernel vector `z_q` gives

```text
psi_iq(y)=B_iq(y,z_q),       psi_iq(x_i)=0.
```

Thus every effective root--root/root--residual companion covector belongs to
the two-dimensional annihilator

```text
x_i^perp={phi:phi(x_i)=0}.                           (12)
```

The lower bound (11) therefore forces equality: the effective companion
covectors span all of `x_i^perp`.  Moreover (3) evaluated at `y=x_i` gives
`ell_i(x_i)=1`, so `ell_i` does not lie in `x_i^perp`.  Consequently

```text
span(ell_i, effective companions)=(C^3)^*.           (13)
```

This is an exact first-jet rigidity condition.  It is still only necessary:
two companion directions with the correct span need not satisfy the actual
cofactor-valued derivative equations or any second-order compatibility.

There is also a coefficient-side rigidity.  Let `Diag` be the
three-dimensional span of the diagonal blocker tensors in (1), and let
`D_i` denote the GHZ derivative map in (6).  Since every `d_c/x_c` is
nonzero, `D_i` is an isomorphism from the root tangent space to `Diag`, and

```text
D_i(x_i)=Lambda.
```

It therefore induces an isomorphism

```text
V/<x_i>  ->  Diag/<Lambda>.                         (14)
```

The scalar row-replacement term vanishes in the target quotient.  Hence the
effective companion cofactor map must itself induce (14).  In particular,
after grouping terms by a basis of `x_i^perp`, the corresponding two
aggregate companion-cofactor classes are independent modulo `Lambda` and
span `Diag/<Lambda>`.  Thus neither a one-dimensional covector span nor a
one-dimensional cofactor-class span can repair the slice.

This quotient-frame condition is stronger than the companion count, but it
still does not assert that such a frame extends to compatible graph edges.

## Consequence for the local-to-global frontier

The locally universal coordinate-monomial model is therefore definitively
not a full graph witness.  Any genuine global point over the same fixed
cofactor slice needs an escape from (3)--(4): a nonprojective root endpoint
or effective root--root/root--residual companions spanning the complete
plane `x_i^perp` whose aggregate cofactor classes simultaneously span
`Diag/<Lambda>`.  These companion terms arise before second-order or
multi-slice gluing and give the smallest new algebraic layer not visible in
the frozen cofactor incidence.

The theorem does **not** say that the companion layer is inconsistent.  It
only proves that further slice-only elimination cannot complete the global
argument.

## Replay

Replay the local construction first:

```powershell
uv run --with sympy python verify_two_residual_coordinate_monomial_slice_universality_nogo.py
uv run --with sympy python audit_two_residual_coordinate_monomial_slice_universality_nogo.py
```

Then run:

```powershell
uv run --with sympy python verify_root_tangent_companion_necessity_for_coordinate_slice.py
uv run --with sympy python audit_root_tangent_companion_necessity_for_coordinate_slice.py
```

The primary enumerates the surviving and differentiated matching classes
through eight roots, checks the scalar derivative identity, and verifies the
three incompatible coefficient systems exactly.  The audit imports no
repository code and uses an independent anchored perfect-matching recurrence.
