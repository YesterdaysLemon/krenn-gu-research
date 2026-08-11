# Hostile review of the zero-permanent pure-residue closure

## Verdict and provenance

**PASS.**  The strengthened common-quadric theorem completely excludes a
physical common-conformal balanced shore, with arbitrary internal nonroot
blocks and with no condition on the scalar cross permanent.

The two scalar-permanent cases use different target equations:

- nonzero permanent contradicts a nonconstant mixed-word zero; and
- zero permanent contradicts a constant-colour pure coefficient.

This closes the previously recorded zero-permanent boundary only because a
physical common-conformal shore uses the same scalar matrix for every target
colour word.  It does not close arbitrary one-word column separation or the
general nonseparable `Q`-divisible branch.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

Reviewed strengthening:

```text
claims/arbitrary-order/
  BALANCED_COMMON_QUADRIC_MIXED_PERMANENT_DIVISIBILITY_AND_CONFORMAL_SHORE_EXCLUSION_THEOREM.md
```

## 1. The pure target residue is nonzero

Fix a constant nonroot word of colour `c`.  Ternary GHZ contracts to

```text
tensor_(i in R) e_(i,c)^*.
```

After the fixed root identifications and repeated-root substitution, its
polynomial is

```text
product_(i in R) R_(i,c)(x),
R_(i,c)(x)=e_(i,c)^*(A_i^(-1)x).
```

Each factor is a nonzero linear form because `A_i` is an isomorphism and the
coordinate covector is nonzero.  Their product is therefore nonzero.  This
checks the main point missed by the earlier mixed-only checkpoint: a constant
word does not have target zero, but its exact nonzero residue is just as
rigid.

## 2. The same modulo-Q matching partition applies

The all-cross companion and every non-all-cross sector do not depend on
whether the nonroot coordinate word is constant.

- `D=N` still carries `C_empty=1` and contributes `perm H_c`.
- Every `D!=N` still contains a root--root matching edge and is divisible by
  the common diagonal quadric `Q`.

Thus equality with GHZ forces

```text
perm H_c = product_i R_(i,c) mod (Q).
```

No mixed-word vanishing is inserted into this step, and arbitrary internal
nonroot blocks remain confined to sectors already killed modulo `Q`.

## 3. Why zero permanent is contradictory

On a common-conformal shore the cross matrix for every word has the form

```text
H_alpha[i,u]=lambda[i,u] L_(u,alpha(u))(x).
```

The scalar matrix `lambda` is fixed by the physical edge scalars and is the
same for constant and nonconstant words.  If `perm(lambda)=0`, column
factorization gives `perm H_c=0` for every constant colour `c`.  The pure
residue would then say that the irreducible rank-three quadratic `Q` divides
the product of the nonzero root linear forms.

In the polynomial UFD an irreducible is prime.  A degree-two irreducible
cannot divide a nonzero linear factor, so it cannot divide their product.
This is the exact contradiction.

The proof does not infer that a zero permanent matrix is zero, singular in a
determinantal sense relevant to the permanent, or entrywise sparse.  Permanent
cancellation is allowed and is precisely what the pure equation excludes in
this physical stratum.

## 4. The permanent dichotomy is exhaustive

Let `p=perm(lambda)`.

```text
p != 0  -> choose a nonconstant word -> mixed residue contradiction;
p  = 0  -> choose a constant word    -> pure residue contradiction.
```

These cases exhaust a field.  The argument works for `m>=2`; in the original
Krenn--Gu range `m>=3`.  Characteristic zero keeps the polynomial and
irreducibility arguments valid, but the zero branch does not divide by `p`
or by any edge scalar.

## 5. Scope that must not be strengthened

The closure needs the physical common-conformal hypothesis:

1. one common nondegenerate symmetric form `q` after fixed endpoint maps;
2. one scalar `lambda[i,u]` attached to each cross edge; and
3. hence the same scalar matrix for every coordinate word.

If a single nonconstant word happens to factor columnwise with scalar matrix
of permanent zero, there need not be any compatible factorization for a
constant word.  The pure argument cannot be imported.  That one-word boundary
remains open.

Likewise, for arbitrary nonseparable cross matrices the permanent may be a
nonzero multiple of `Q` for every mixed word and may have the required pure
residue for constant words.  The theorem records those simultaneous residue
conditions but does not exclude them.

No theorem derives a common root quadric or common-conformal cross shore from
all-balanced rank drop, full-sensor incidence, local concision, or block
invertibility.  The global branches remain open.

## 6. Degenerate forms remain separately excluded

If the common form `q` is degenerate, every edge incident to a chosen root
has its root covector in an image of dimension below three.  The graph's
one-vertex flattening rank is then below the ternary GHZ rank three.  The
strengthening does not apply irreducibility language to a degenerate
quadratic.

## 7. Computational independence

The strengthened primary verifier adds zero-permanent matrices at `m=2,3`.
For each it:

- constructs the column-factored cross permanent and confirms it is zero;
- builds the full repeated-root graph contraction with arbitrary internal
  weights and confirms its residue modulo `Q` is zero; and
- checks that a separate product of nonzero root forms has nonzero residue.

The no-import audit uses different zero-permanent matrices at `m=2,4`, its
own sparse polynomial arithmetic, direct matching recursion, and normal-form
reduction by `z^2=-(x^2+y^2)`.  It reaches the same pure-residue mismatch
without importing SymPy or primary code.

These examples audit the branch logic and conventions.  The arbitrary-order
proof is the constant-word target contraction, common matching congruence,
shared scalar permanent, and UFD argument.

## 8. Accepted proof-topology update

```text
common-conformal balanced shore, nondegenerate q:      EXCLUDED completely;
arbitrary internal nonroot completion repairs it:      FALSE;
zero scalar cross permanent in that physical stratum:  CLOSED by pure word;
one-word zero-permanent column factorization:           OPEN;
general nonseparable simultaneous Q-residue branch:     OPEN;
universal common-quadric/conformal extraction:          NOT PROVED;
global Krenn--Gu conjecture:                             UNRESOLVED.
```

## Strongest fresh-referee objection

The pure closure would be invalid if the scalar matrix used for a mixed word
could change with the target colour word.  Physical common-conformal blocks
prevent that: `lambda[i,u]` is an edge scalar, while only the column linear
form changes with the nonroot coordinate.  The theorem is accepted because
it states this shared-matrix hypothesis and does not transfer the closure to
arbitrary wordwise factorizations.
