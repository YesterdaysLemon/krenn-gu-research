# Two residual companions alone fail at the third root jet

## Status

**Exact arbitrary-order characteristic-zero topology theorem.**  Let a
hypothetical three-colour GHZ graph witness contain `r>=4` fully supported
roots, their blocker union, and exactly two residual nonblockers `q_0,q_1`
fixed at simultaneous-kernel vectors.  Suppose:

1. the root--blocker rows vary projectively to first order at every root;
2. after restricting at root `i` to the scalar tangent kernel `S_i`, every
   differentiated root--blocker edge vanishes;
3. no root--root edge is effective on these restricted jets: its one-tangent
   contractions against the other base root and its two-tangent restriction
   are all zero;
4. consequently the only effective edge for a restricted root tangent goes
   to one of `q_0,q_1`.

Then the graph cannot equal GHZ.  Indeed, every restricted two-root mixed
derivative has cofactor quotient span at most one.  Pairwise resonance and
the exact clique theorem therefore force the uniform balanced tangent
pattern.  But a matching cannot send three varied roots injectively to only
two residual endpoints, so the restricted graph triple derivative is zero,
whereas the uniform GHZ triple derivative has quotient rank two.

Thus any witness in this two-residual cell with `r>=4` must escape through at
least one of the following:

```text
nonprojective root--blocker variation;
an effective root--root restricted tangent channel;
a third effective nonroot companion endpoint.
```

This excludes a companion topology, not every two-residual graph and not
the all-full-span cofactor incidence.  It does not prove that any listed
escape is impossible.  The arbitrary-order local-to-global reduction and
the global Krenn--Gu conjecture remain **UNRESOLVED**.  No finite field is
used.

## Restricted tangent setup

Normalize every root logarithmically so its base vector is `(1,1,1)`.  The
projectively constant root--blocker derivative at root `i` is governed by a
covector

```text
a_i,                 a_i(1,1,1) != 0,
S_i=ker(a_i).                                      (1)
```

For `y_i in S_i`, every differentiated edge from root `i` to a blocker is
zero.  Write the two residual tangent covectors as

```text
psi_(i,t)(y_i)=B_(i,q_t)(y_i,z_t),      t=0,1.     (2)
```

The root--root hypothesis means, for distinct roots `i,j`,

```text
B_ij(S_i,x_j)=0,
B_ij(x_i,S_j)=0,
B_ij(S_i,S_j)=0.                                  (3)
```

These assumptions allow arbitrary blocker--blocker, blocker--residual, and
residual--residual edges, and arbitrary complementary hafnians.  Only their
connectivity to a differentiated root is constrained.

## Every pair sees one cofactor line

Differentiate at roots `i,j` and restrict to `S_i tensor S_j`.  By (1) and
(3), a surviving matching must pair the two roots to the two distinct
residual endpoints.  There are exactly two assignments.  Both delete the
same four vertices, so they multiply one common complementary tensor
`C_ij`.  The complete restricted graph derivative is

```text
[psi_(i,0)(y_i) psi_(j,1)(y_j)
 +psi_(i,1)(y_i) psi_(j,0)(y_j)] C_ij.             (4)
```

Its image modulo the scalar GHZ tensor has dimension at most one, whether
or not `C_ij` itself is nonzero.

The GHZ side is the coordinatewise-product map

```text
mu_(a_i,a_j):S_i tensor S_j -> K^3/<(1,1,1)>.      (5)
```

Its rank is always one or two.  Equality with (4) therefore forces rank one
for every pair.  By the resonance-clique classification, for `r>=4` there is
one coordinate `c` such that, projectively,

```text
a_i=e_p^*+e_q^*                 for every i,       (6)
```

where `{p,q}` is the complementary coordinate pair.

## The third-jet contradiction

Differentiate at three distinct roots and restrict to their three spaces in
(6).  Every surviving graph matching would have to pair each of those roots
to `q_0` or `q_1`: blocker edges vanish by (1), and root--root edges vanish
by (3).  A perfect matching uses each residual endpoint at most once, so no
such matching exists.  The complete restricted graph triple derivative is
therefore zero.

On the GHZ side, after permuting coordinates, vectors in the common tangent
space have the form

```text
u=(x,-x,z).
```

The coordinatewise product of three such vectors is

```text
(X,-X,Z),                                          (7)
```

whose image modulo `(1,1,1)` has rank two.  This is nonzero and contradicts
the graph derivative.  The contradiction proves the theorem.

## Sharp boundary

For exactly three roots, the pairwise-resonant clique may instead be the
three coordinate covectors.  Its triple coordinatewise product is zero, so
the last step does not contradict that exceptional pattern.  For `r>=4`
the axis pattern is unavailable.

Allowing a root--root tangent edge changes both arguments: it can contribute
another cofactor class to (4), and at third order one root pair may use that
edge while the third root uses a residual endpoint.  Likewise a third
effective nonroot endpoint defeats the pigeonhole step.  Those are genuine
open escape routes and are not suppressed by the theorem.

## Replay

Replay the rank, clique, and parity dependencies first:

```powershell
uv run --with sympy python verify_root_mixed_second_jet_quotient_rank_classification.py
python audit_root_mixed_second_jet_quotient_rank_classification.py
uv run --with sympy python verify_root_mixed_second_jet_resonance_clique_classification.py
python audit_root_mixed_second_jet_resonance_clique_classification.py
uv run --with sympy python verify_root_resonant_mixed_jet_parity_classification.py
python audit_root_resonant_mixed_jet_parity_classification.py
```

Then run:

```powershell
uv run --with sympy python verify_root_two_residual_only_companion_third_jet_obstruction.py
python audit_root_two_residual_only_companion_third_jet_obstruction.py
uv run --with sympy --with ruff python -m ruff check verify_root_two_residual_only_companion_third_jet_obstruction.py audit_root_two_residual_only_companion_third_jet_obstruction.py
python -m py_compile verify_root_two_residual_only_companion_third_jet_obstruction.py audit_root_two_residual_only_companion_third_jet_obstruction.py
```

The primary checks the two residual assignments, the common deletion set,
the uniform triple rank, and the matching pigeonhole through ten roots.  The
no-import audit independently enumerates injective residual assignments and
all coordinate permutations through fourteen roots.  The arbitrary-order
proof is the exact matching argument above; the bounded enumerations audit
its indexing only.
