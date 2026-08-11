# Hostile review of the common-quadric mixed-permanent obstruction

## Verdict and provenance

**PASS, with the zero-permanent and nonseparable branches retained.**  The
owning theorem proves an exact necessary divisibility for every nonconstant
nonroot coordinate word when one balanced root shore has a common
nondegenerate diagonal quadric.  It then excludes a column-separable cross
shore when its scalar permanent is nonzero.  Internal nonroot blocks are
arbitrary.

The theorem does not extract a common root quadric from every witness, prove
column separation, or prove that the cross-scalar permanent is nonzero.  It
therefore narrows but does not close the balanced-sensor branches.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

Reviewed candidate:

```text
claims/arbitrary-order/
  BALANCED_COMMON_QUADRIC_MIXED_PERMANENT_DIVISIBILITY_AND_CONFORMAL_SHORE_EXCLUSION_THEOREM.md
```

The review reconstructed the matching partition independently of both
scripts, then compared their polynomial conventions and exact outputs.

## 1. The root hypothesis is diagonal, not falsely bilinear

For fixed root identifications `A_i:L_i -> V`, the theorem assumes only

```text
W_ij(A_i^(-1)x,A_j^(-1)x)=rho_ij Q(x)
```

on simultaneous diagonal evaluation.  A bilinear block between two distinct
spaces need not become a symmetric copy of `Q`; any part invisible on the
diagonal is allowed.  This weaker hypothesis is sufficient because the proof
puts the same transformed root vector `x` in every root slot.

The isomorphisms `A_i` are fixed across all edges incident to root `i`.
Edge-dependent root identifications would not define one common variable `x`
and are not covered.

## 2. The balanced labels and empty coefficient are correct

With the owning balanced convention, companion `G_D` uses exactly the
nonroots `D` matched across the cut, while the internal deck member is
`C_(N-D)`.  The all-cross term is therefore

```text
D=N,       C_empty=1.
```

It carries the root-to-nonroot permanent with coefficient one.  For every
other legal `D`, the difference `m-|D|` is a positive even integer, so at
least one pair of roots is matched internally.  Every matching monomial in
that sector contains a factor `rho_ij Q(x)`.

This verifies the congruence

```text
full repeated-root contraction = all-cross permanent mod (Q).
```

There is no missing sector in which a proper `D` leaves one root unmatched,
and no higher internal deck value can cancel the residue: those deck values
multiply terms already in `(Q)`.

## 3. The target word is exactly zero

The proof chooses a coordinate basis vector at every nonroot.  If the
resulting word `alpha` is nonconstant, then for each GHZ colour `c` at least
one nonroot contraction contributes zero.  The entire root tensor is zero,
not merely one selected root coefficient.

Consequently the all-cross permanent must lie in `(Q)` as a polynomial.  The
argument applies to every nonconstant coordinate word and requires no
genericity, continuity, or sampled isotropic point.

## 4. It is a permanent, not a determinant

When every root crosses to `N`, a perfect matching is a bijection
`R -> N`.  Matching weights have no permutation sign.  Their sum is therefore
`perm H_alpha`, not `det H_alpha`.

Under column separation `H_(i,u)=lambda_(i,u)L_u`, factoring from columns
gives

```text
perm H = perm(lambda) product_u L_u.
```

Both scripts use unsigned permutation sums.  Introducing determinant signs
would change the theorem and is not justified by hafnian matching semantics.

## 5. Irreducibility and characteristic zero are used honestly

A rank-three ternary quadratic cannot factor into two linear forms: the
symmetric matrix of such a product has rank at most two.  Thus the
nondegenerate `Q` is absolutely irreducible.  In the polynomial UFD it is
prime, so divisibility of a product of nonzero linear forms would force
divisibility of one factor, which degree forbids.

Characteristic zero also keeps the special common-quadratic scalar
permanent `m!` nonzero.  The main exclusion itself assumes the displayed
scalar permanent is nonzero and does not divide by any root-edge scalar.

Over a non-algebraically-closed characteristic-zero base field, an asserted
tensor equality and all matrix ranks survive scalar extension.  The proof may
therefore use absolute irreducibility over the algebraic closure without
strengthening the original equality.

## 6. The common-conformal specialization is physical and one-cut

For one balanced cut, the specialization assumes

```text
root-root block  = rho_ij q after the fixed endpoint maps,
root-cross block = lambda_iu q after the fixed endpoint maps.
```

It places no condition on nonroot--nonroot blocks.  Nondegeneracy of `q`
makes each column form

```text
L_u(x)=q(x,A_u e_(u,alpha(u)))
```

nonzero.  Hence one nonconstant word and one nonzero cross permanent trigger
the exclusion.  No assumption that all balanced cuts share the form, and no
all-balanced rank-drop hypothesis, is inserted.

If `q` is degenerate, every covector at any root lies in the first-factor
image of `q`, so that root's one-flattening rank is below three.  This is a
separate local-rank exclusion; the proof does not call a reducible degenerate
quadric irreducible.

## 7. The permanent-nonzero boundary is real

Entrywise nonzero complex matrices can have zero permanent.  Neither local
concision nor the common-quadric hypothesis as currently proved forces
`perm(lambda)!=0`.  The theorem states that condition as an assumption.

When it fails, the column-separable all-cross diagonal vanishes identically,
so the present mixed-word detector gives no contradiction.  That does not
construct a witness: other words, other root evaluations, other cuts, and
the full tensor equations remain.  The exact surviving conformal boundary is
therefore `perm(lambda)=0`, not “conformal shores are completely closed.”

Without column separation, the permanent may be a nonzero multiple of `Q`.
The surviving condition that **every** mixed-word permanent be divisible by
`Q` is likewise an open algebraic branch, not a claimed impossibility.

## 8. Computational independence and replay meaning

The primary verifier uses SymPy to:

- construct the full matching polynomial with arbitrary fixed internal
  nonroot weights through eight vertices;
- divide the difference from the all-cross permanent by `x^2+y^2+z^2`;
- check column factorization and nonzero scalar permanents through `m=6`;
- exhibit a nonzero exact isotropic evaluation; and
- audit target-word and degenerate-span conventions.

The independent audit imports no primary code or computer-algebra package.
It uses:

- a separate recursive matching generator;
- a custom sparse integer polynomial ring;
- normal-form reduction by `z^2=-(x^2+y^2)`;
- different cross forms, root/internal scalars, and column-separable
  instances; and
- independent unsigned permanent and exact rational-rank routines.

Both routes confirm the residue identity for `m=2,3,4`.  Their bounded checks
support indexing and constants only.  The arbitrary-order proof is the
written matching-sector argument and UFD divisibility.

## 9. Acceptance and proof-topology boundary

The accepted update is:

```text
common root quadric forces every mixed permanent into (Q): PROVED;
column-separable mixed word with nonzero permanent:        EXCLUDED;
common-conformal shore with arbitrary internal completion: EXCLUDED
  only when its cross permanent is nonzero;
zero-permanent conformal shore:                             OPEN;
nonseparable Q-divisible cross shore:                       OPEN;
universal common-quadric extraction:                        NOT PROVED;
global Krenn--Gu conjecture:                                UNRESOLVED.
```

This supports a new scoped balanced-shore node and makes the earlier
common-quadratic orbit a strict special case.  It does not close `S2`, `S3`,
or the global node.

## Strongest fresh-referee objection

The easiest overstatement is to replace “`perm(lambda)!=0`” by “all cross
entries are nonzero.”  Complex permanent cancellation makes that inference
false.  The theorem is accepted because it retains the exact permanent gate
and records `perm(lambda)=0` as a live boundary rather than silently
discarding it.
