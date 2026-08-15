# Hostile review of the triangle-pair kernel-support boundary theorem

## Verdict and exact scope

**PASS, for the displayed `(3,1)` triangle frame, pointwise,
characteristic-zero, full-`Delta_3` scope.**  No mathematical,
quantifier, slot, characteristic, dependency, or implementation blocker
survived hostile review.

For every local mode of this explicit triangle pair, the new package proves

```text
rank(Phi_1|L_t) >= 2,             rank(Phi_2|L_t) >= 2.
```

More precisely, a nonzero local kernel vector must lie on one of the
following ambient lines:

```text
Phi_1: K(x_1+x_2), K(x_0+x_2), K(x_0-x_1),
Phi_2: Kx_3, K(x_1+x_2).
```

Together with the already reviewed two-sided projection-drop predecessor,
this makes the minimum local rank in each family exactly two.  This is a
necessary localization only.  The finite exceptional-line incidence
problem remains open; no existence of such incidences is asserted.  The
result does not transport automatically to another based frame or to the
inequivalent equality-five pair orbits.  Unrestricted `P_6 -> Delta_3`
nonrestriction is unknown, and the global Krenn--Gu conjecture remains
**UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_TRIANGLE_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
  verify_arbitrary_permanent_triangle_pair_kernel_support_boundary.py
  audit_arbitrary_permanent_triangle_pair_kernel_support_boundary.py
```

Load-bearing predecessors replayed during review:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_TRIANGLE_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md
  ARBITRARY_PERMANENT_FIXED_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
  ARBITRARY_PERMANENT_FIXED_PAIR_EXCEPTIONAL_KERNEL_NECESSITY_THEOREM.md
```

The first supplies the rank-at-most-two modes.  The latter two contain
independently reviewed versions of the two-dimensional active-colour and
one-surviving-diagonal lemmas reused in the new proof.

## 1. Kernels and single contractions

Solving the four defining equations of each projection directly gives

```text
ker(Phi_1)={(a,b,a+b,0,0,0)},
ker(Phi_2)={(0,a,a,b,0,0)}.
```

Independent differentiation of the five displayed quartics reproduces the
single-contraction table.  After suppressing the common factor `x_4x_5`,
the first kernel pencil gives

```text
F_1: 0,
F_2: a(x_0-x_1+x_2),
D_0: 2a x_3,
D_1: (a+b)(x_0+x_1+x_2),
D_2: b(x_0-x_1-x_2),
```

while the second gives

```text
F_1: b(-x_0-x_1+x_2),
F_2: 0,
D_0: 2b x_0,
D_1: a(x_0+x_1+x_2),
D_2: a(x_0-x_1-x_2).
```

For `Phi_1`, the four residual columns `(F_2,D_0,D_1,D_2)` have determinant

```text
-8 a^2 b(a+b).
```

Thus they form a basis of the first-four-coordinate covector space exactly
off `a=0`, `b=0`, and `a+b=0`.  For `Phi_2`, direct substitution verifies
the cleared relation

```text
-a i_p D_0+b i_p D_1+b i_p D_2=0.
```

When `ab!=0`, dividing by `b` gives precisely the relation used in the
written proof.  No quotient ring, algebraic closure, or projective
normalization is hidden in either calculation.

## 2. The generic `Phi_1` obstruction

Write the ambient six-space as

```text
R direct-sum A,
R=K^{0,1,2,3}, A=K^{4,5},
J((s_4,s_5),(t_4,t_5))=s_4t_5+s_5t_4.
```

After contracting a generic `Phi_1` kernel vector in one local slot, the
polarization of every residual quartic `x_4x_5 ell` is evaluation of

```text
C(y,z,w)=r(y)J(a(z),a(w))
        +r(z)J(a(y),a(w))
        +r(w)J(a(y),a(z)).
```

Because the four residual covectors are a basis, the full target equations
give, on the three remaining ordered colour bases,

```text
C(y_(s,i),y_(u,j),y_(v,l))=0 unless i=j=l,
C(y_(s,c),y_(u,c),y_(v,c))!=0 iff alpha_c!=0.
```

This is a vector identity in `R`, not merely a scalar or numerical test.

For distinct colours `i!=j`, the map

```text
w |-> C(y_(s,i),y_(u,j),w)
```

kills the three-plane `L_v`.  Its rank is therefore at most three.  On the
four-dimensional summand `R`, however, it is scalar multiplication by

```text
J(a(y_(s,i)),a(y_(u,j))).
```

A nonzero scalar would give rank at least four, so all different-colour
columns in different modes are `J`-orthogonal.

The resulting two-dimensional geometry is exhaustive.  If every mode's
`A`-image has dimension at most one, an active same-colour pairing forces
both endpoint modes to support only that colour, so no second colour can
be active.  If one mode has two independent columns of colours `e,f`, then
the third-colour columns in both other modes are orthogonal to a basis and
vanish.  If both `e,f` are active, the two distinct orthogonal-complement
lines supplied outside the first mode also force its third-colour column
to vanish.  Hence at most two colours are active, and in the two-active
case every third-colour `A`-column in the three remaining modes is zero.

The proof uses only the safe implication

```text
alpha_c!=0  =>  colour c is active.
```

Indeed, a nonzero all-`c` value of `C` requires at least one nonzero
same-colour `J` pairing.  The converse can fail by cancellation and is not
used.

If two local coefficients of the removed kernel vector were nonzero, the
third colour would have zero `A`-part in all three remaining modes.  In the
original pure coefficient at that third colour, only the removed local mode
could then contribute an `A`-part.  Multilinearity assigns the distinct
factors `x_4,x_5` to distinct slots, so one mode cannot supply both.  The
pure coefficient would vanish, contradicting its nonzero target.  This is
the load-bearing slot argument; the removed kernel vector's own zero
`A`-part is consistent but not needed for this final inference.

Thus a generic `Phi_1` kernel vector would have exactly one nonzero local
coefficient.

## 3. One surviving diagonal is impossible

Relabel the sole surviving colour as zero.  For a pair of zero-labelled
columns with nonzero `J` pairing, the off-diagonal target identities force
the `R`-parts of the two other-colour vectors in the third mode to vanish.
Both vectors then lie in `A` and are orthogonal to the same nonzero
zero-labelled `A`-vector.  Since `J` is nondegenerate on the two-space
`A`, that orthogonal complement is a line.  The two local vectors are
dependent, contradicting independence of the ordered local triple.

This excludes every `Phi_1` direction with `ab(a+b)!=0`.  It is a
field-linear argument: no square roots, closure, or positivity are used.

## 4. Exceptional `Phi_1` supports

On each remaining parameter line one diagonal residual vanishes
identically, and the corresponding nonzero pure target forces one local
coefficient to vanish:

```text
a=0       => alpha_0=0,  p in K(x_1+x_2), support subset {1,2};
b=0       => alpha_2=0,  p in K(x_0+x_2), support subset {0,1};
a+b=0     => alpha_1=0,  p in K(x_0-x_1), support subset {0,2}.
```

The theorem does not strengthen these containments to singleton support or
claim that any exceptional line is realizable.

## 5. The `Phi_2` dependence and exceptional supports

For `ab!=0`, applying the exact residual relation to the contracted target
gives

```text
-(a/b) lambda_0 alpha_0 e_0^* tensor 3
+lambda_1 alpha_1 e_1^* tensor 3
+lambda_2 alpha_2 e_2^* tensor 3=0.
```

These three coordinate cubes occupy disjoint entries of the
three-mode tensor space and are linearly independent over every field.
All displayed scalars are nonzero, so every `alpha_c` vanishes, contrary
to the nonzero kernel vector.  Thus only `a=0` or `b=0` remains.

At `a=0`, the vector is a nonzero multiple of `x_3`; both `D_1` and `D_2`
contract to zero, forcing `alpha_1=alpha_2=0`, so its support is exactly
`{0}`.  At `b=0`, the vector is a multiple of `x_1+x_2`; `D_0` contracts
to zero and forces `alpha_0=0`, leaving support contained in `{1,2}`.

## 6. Finite-union rank floor

For fixed `k,t`, let

```text
S=L_t intersect ker(Phi_k).
```

The preceding exclusions put `S` in a union of three ambient lines for
`Phi_1` or two ambient lines for `Phi_2`.  A characteristic-zero field is
infinite, and a vector space over an infinite field cannot be a finite
union of proper linear subspaces.  Therefore `dim S<=1`.  Rank-nullity on
the three-dimensional `L_t` gives

```text
rank(Phi_k|L_t)>=2.
```

The two-sided predecessor is used only for its already reviewed upper
bound: each family has some mode of rank at most two.  Combining the bounds
gives

```text
min_t rank(Phi_1|L_t)=min_t rank(Phi_2|L_t)=2.
```

It does not imply that the minimizing modes coincide.

## 7. Characteristic, quantifier, and target boundaries

The statement is correctly restricted to characteristic zero.  The proof
uses the nonzero determinant factor `8`, nondegeneracy of the hyperbolic
form, division by a nonzero `b`, and infinitude of the base field.  The
finite-field runs below audit formulas only.

Every conclusion is pointwise for ordered independent local triples
satisfying the complete exact target equations.  Tensor-wide mixed zeros,
all three nonzero diagonal tensors, and values on every local colour tuple
are load-bearing.  The proof is not a Hamming-shell result and does not
establish a converse, realizability statement, or unrestricted extension
exclusion.

Accepted boundary:

```text
displayed triangle pair, every local Phi_k rank at least two: PROVED;
Phi_1 low kernels localized to three lines:                  PROVED;
Phi_2 low kernels localized to two lines:                    PROVED;
one rank-two mode in each family:                            PROVED NECESSARY;
finite exceptional-line incidence exclusion:                OPEN;
unrestricted P_6 -> Delta_3:                                UNKNOWN;
global Krenn--Gu conjecture:                                 UNRESOLVED.
```

## 8. Computational replay and independence

The new primary verifier uses exact SymPy arithmetic to reconstruct both
kernels, all ten polarized contractions, the determinant, the cleared
residual dependence, and the rank gates used by the structural lemmas.

The new no-import audit imports neither the primary verifier nor SymPy.  It
rebuilds the five expanded quartics as square-free monomial dictionaries,
contracts them directly, and exhausts both projective kernel pencils over
`F_5` and `F_7`.  It finds exactly three exceptional `Phi_1` directions
and two exceptional `Phi_2` directions in each field.  This is meaningfully
independent evidence for the displayed algebra and case boundaries, not an
independent computational proof of the characteristic-zero theorem.  The
written field-linear argument is the proof.  The independently reviewed
fixed-pair packages provide separate implementations and finite-field
stress tests for the abstract active-colour and one-diagonal lemmas.

Focused final replay passed:

```text
new primary exact verifier:                         PASS;
new independent no-import audit:                   PASS;
triangle two-sided predecessor primary/audit:      PASS/PASS;
fixed kernel-boundary predecessor primary/audit:   PASS/PASS;
fixed one-diagonal predecessor primary/audit:      PASS/PASS;
py_compile on all replayed scripts:                PASS;
Ruff on all replayed scripts:                      PASS;
git diff --check on tracked changes:               PASS.
```

## Final reviewed hashes

```text
new theorem:
60858DFE1C1C9E11C74662B815E1A4173616C3277E28A25520EDAD97148EBA82

new primary verifier:
67F27BEF7A3C8A071344F6B48BEA265DF2173E839586C988239F039DBB72F8DF

new independent audit:
B0C5DFBC8ED8086BCF5EDAA8665BD57131E2291ED73601A269F35996B973FBA8

triangle two-sided theorem:
C5E8F47B499318595481D84DB75425240BA6A01AD512A92BF923F5FAB56BF485

triangle two-sided primary verifier:
770F21C2D34A5B98CE5820D023405D0A95B3FE167539747E3EFB9EDE4A538153

triangle two-sided independent audit:
14AB3E48905246452B9B02D962D0D5902D543398EA74B0009ACAF12C720D136D

fixed kernel-boundary theorem:
7AEC9CD00DEBAC1D5CFA91D44E5D3634BD6D05FF8CA755BA1C2E83D1F8C3C45B

fixed kernel-boundary primary verifier:
2B5FC62CA56FA06E5CF06AAC12679CB1051CD7336E1F4B473ECB86AED48AF53C

fixed kernel-boundary independent audit:
038EDA376B773687523FA0885157907725FD38EB5D63AA83BCFD0095090C6F68

fixed one-diagonal theorem:
2FAB590264EDE5999F55540F2234BE2055637386B978D77469F592F58B004B60

fixed one-diagonal primary verifier:
256D1F4DEB3639E912E41C426E2D28E5FCB384C72DCDB00F9592064D33C904E5

fixed one-diagonal independent audit:
90014EC8E37B0F48F26BD4A9528E235F2FC26D5E757948E34B1744B1B743D6F1
```
