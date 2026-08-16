# Hostile review of the pair-dimension-five `r=4` orbit classification

## Verdict and provenance

**PASS, within the stated active-support-four and pair-level scope.**  No
mathematical, orbit-exhaustiveness, characteristic, or implementation blocker
survived hostile review.  The package classifies exactly five unbased pairs of
three-planes `U,V subset (Z_4)_1` with `dim(UV)=5` under coordinate
permutations and nonzero coordinate scalings.  Exactly three of those five
orbits admit colour bases satisfying the necessary pair-level `Delta_3`
condition.

The result does not classify equality-five pairs with five or six active
coordinates, based-frame stabilizer orbits, or extensions through the four
remaining modes.  It therefore does not prove unrestricted
`P_6 -> Delta_3`, permanent nonrestriction, or the global Krenn--Gu
conjecture.  Those remain **UNKNOWN/UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_PAIR_DIMENSION_FIVE_R4_ORBIT_CLASSIFICATION_THEOREM.md
  verify_arbitrary_permanent_pair_dimension_five_r4_orbit_classification.py
  audit_arbitrary_permanent_pair_dimension_five_r4_orbit_classification.py
```

The review independently rederived the annihilator classification, checked
both directions of the rank-one admissibility criterion, attacked the two
nonadmissible rank-one loci, replayed every displayed admissible product
table, and checked the exact separator between the fixed `(4,2)` pair and the
new `(4,1)` frame.  No theorem or script edit was required.

The package was new relative to `origin/main` commit
`4efbbd2c4dc364930809cfceb5486268fa3fd00f`.  This is a repository-level
novelty statement, not an external priority claim.

## 1. Why the unbased classification has exactly five orbits

Every three-plane in the four-dimensional linear space is a hyperplane, so
write

```text
U=ker(alpha),
V=ker(beta).
```

When `alpha,beta` are independent, a symmetric bilinear form vanishing on
`U x V` kills `U intersect V` and descends to the two-dimensional quotient.
The two quotient lines are orthogonal, so in the dual coordinates supplied
by `alpha,beta` every such form is uniquely

```text
Q=c alpha alpha^T + e beta beta^T.
```

Requiring the matrix to have zero diagonal gives exactly

```text
c alpha_i^2 + e beta_i^2=0,  i=0,1,2,3.
```

The ordinary annihilator of `UV` is one-dimensional precisely when these
four equations have a one-dimensional nonzero solution.  Neither `c` nor
`e` can vanish.  Therefore `alpha` and `beta` have the same support, and all
nonzero ratios `beta_i/alpha_i` have the same square.  Over characteristic
zero, dividing by one ratio leaves signs `+1` and `-1`; both signs must occur
because the hyperplanes are distinct.

Coordinate scalings normalize `alpha` to ones on its support, coordinate
permutations group the signs, and projective rescaling of `beta` exchanges
the two sign blocks.  Thus the distinct-hyperplane cases are exactly

```text
(support size, smaller sign block) =
(2,1), (3,1), (4,1), (4,2).
```

Their unique annihilator support graphs are respectively

```text
K_(1,1) + 2 isolated vertices,
K_(1,2) + 1 isolated vertex,
K_(1,3),
K_(2,2),
```

with four distinct degree multisets.  Hence no two of these four normal forms
can be monomially equivalent.

When `U=V=ker(alpha)`, every bilinear annihilator is

```text
alpha z^T+z alpha^T.
```

The zero-diagonal conditions are `2 alpha_i z_i=0`, so an alpha support of
size `s` gives annihilator dimension `4-s` and

```text
dim(U^2)=6-(4-s)=2+s.
```

Equality five occurs only at `s=3`, producing one coincident orbit.  Although
its annihilator graph is also `K_(1,3)`, it is separated from the distinct
`(4,1)` orbit by `dim(U intersect V)`: three versus two.  These arguments are
both exhaustive and invariant under every allowed equivalence, giving the
claimed five and only five unbased orbits.

## 2. The pair-level `Delta_3` criterion

Let multiplication be

```text
mu:U tensor V -> B=UV
```

and let `L=mu^*(B^*)` be its five-dimensional multiplication-dual space in
`U^* tensor V^*`.

If colour bases make the mixed products span a two-space `M` complementary
to three diagonal products, the quotient dual `(B/M)^*` pulls back to three
rank-one matrices supported on the three diagonal colour positions.  Their
left factors form a basis of `U^*`, and their right factors form a basis of
`V^*`.

Conversely, suppose `L` contains three rank-one forms
`lambda_e tensor rho_e` whose two factor triples are bases.  In the dual
primal bases, all three forms vanish on every mixed colour product and form
the identity matrix on the three diagonal products.  Their common kernel in
`B` has dimension two.  The mixed products lie in that kernel, while the
diagonals are independent modulo it.  Since all nine basis products generate
`B`, the mixed span must equal the whole two-dimensional kernel.  Thus the
direct-sum and `dim M=2` requirements follow; neither is silently assumed.

This proves the criterion for an arbitrary pair-level radical.  It is more
than a check of one preferred colour basis, but it remains only a necessary
pair-level condition for a full six-mode restriction.

## 3. The coincident and `(2,1)` obstructions

For the coincident support-three orbit, the multiplication-dual space is

```text
[a b c]
[b d e]
[c e 0].
```

A nonzero symmetric rank-one matrix is a scalar multiple of `ww^T`.  Its
bottom-right zero forces the third coordinate of `w` to vanish.  Consequently
all left and right factors of all rank-one members lie in the same fixed
two-space, so no three can be bases.

For `(2,1)`, the dual space is

```text
[0 a b]
[c 0 e]
[d e 0].
```

The lower-right two-by-two minor is `-e^2`, hence rank one forces `e=0`.
The remaining decisive minors are

```text
ac=ad=bc=bd=0.
```

Over a field, either `(a,b)=0` or `(c,d)=0`.  Thus every nonzero rank-one
matrix has either fixed left factor `e_0` and a right factor in a two-plane,
or fixed right factor `e_0` and a left factor in a two-plane.  Three such
points cannot span both factor spaces simultaneously: obtaining three left
directions forces at most two right directions, and conversely.  This closes
the second nonadmissible orbit without a genericity assumption.

## 4. Exact admissible frames

For each of `(3,1)`, `(4,1)`, and `(4,2)`, the theorem gives explicit rational
ordered bases.  Independent multiplication in edge order

```text
(01,02,03,12,13,23)
```

reproduced every displayed entry.  In each case:

```text
rank of six mixed products = 2,
rank of all nine products  = 5,
rank of mixed plus three diagonal products = 5.
```

Therefore the three diagonal products are independent modulo the mixed
two-space, proving existence of a `Delta`-admissible frame in each remaining
unbased orbit.  Zero mixed products in the `(3,1)` table cause no problem;
the complete mixed family still spans exactly two dimensions.

Together with the two rank-one-locus obstructions, this proves the exact
pair-level admissibility list:

```text
coincident support-three: NOT admissible;
(2,1):                    NOT admissible;
(3,1):                    admissible;
(4,1):                    admissible;
(4,2):                    admissible.
```

The result asserts existence of at least one admissible colour frame in each
of the last three unbased orbits.  It does not classify all such frames under
the smaller stabilizer of the diagonal target.

## 5. Fixed-pair nonuniversality and the `r=6` boundary

The previously studied fixed pair has normal sign split `(4,2)` and unique
annihilator supported on `K_(2,2)`.  The new explicit `(4,1)` admissible frame
has unique annihilator supported on the star `K_(1,3)`.  Coordinate scalings
preserve the zero pattern of the unique annihilator, and coordinate
permutations preserve its graph isomorphism type.  The two admissible pairs
are therefore exactly inequivalent before any choice of colour bases.

This proves that the fixed `(4,2)` pair is not universal among either all
active-support-four equality-five pairs or the pair-level admissible ones.
Consequently neither fixed-pair exclusion theorem can be transported to the
`(4,1)` orbit without a new argument.

Zero extension into `Z_6` preserves product rank, admissibility, active
support size four, and the annihilator support graph on that active support.
It therefore supplies inequivalent pair-level examples in six coordinates.
It does not supply the other four local modes, a `P_6 -> Delta_3` restriction,
or a counterexample.

## 6. Characteristic and evidence boundaries

The theorem is correctly stated over characteristic zero.  The proof uses
that `2` is nonzero in the coincident-hyperplane dimension formula and that
equal squares have signs `+/-`.  Characteristic two collapses both pieces of
the classification and is outside scope.  The displayed ranks also replay
over `F_3` and `F_5`, but the package does not need or claim a positive-
characteristic theorem.

No algebraic closure, generic point, orbit closure, sampling claim, or
computer-assisted exhaustive characteristic-zero case split is load-bearing.
The finite-field census audits the written normal-form derivation; the
written linear algebra proves the characteristic-zero statement.

## 7. Computational independence and replay

The primary verifier uses SymPy exact linear algebra.  It checks all five
normal-form hyperplanes and product ranks, reconstructs the annihilator graph
invariants, verifies the two displayed dual spaces and decisive minors, and
replays every product and direct-sum assertion in the three admissible
frames.

The independent audit imports neither the primary verifier nor SymPy.  It
uses a custom modular reducer, fraction-free integer determinants, an
exhaustion of all 24,336 ordered projective normal pairs over `F_5`, and a
separate enumeration of every projective rank-one point in each canonical
five-dimensional dual space.  It also replays all rational product tables
with integer arithmetic.

The finite-field equality-five census found exactly 728 ordered pairs:

```text
P3:      64;
(2,1):   24;
(3,1):  192;
(4,1):  256;
(4,2):  192.
```

The five rank-one loci had respectively `6,12,4,6,6` projective points over
`F_5`; a bispanning triple existed exactly for `(3,1)`, `(4,1)`, and `(4,2)`.

Focused final replay passed:

```text
primary exact verifier:                 PASS;
independent no-import audit:            PASS;
py_compile:                             PASS;
Ruff:                                   PASS;
fixed `(4,2)` predecessor replays:      PASS/PASS.
```

## 8. Accepted scope and remaining obligations

```text
active-support-four equality-five unbased orbits:       FIVE, CLASSIFIED;
pair-level Delta-admissible unbased orbit types:         THREE, CLASSIFIED;
fixed `(4,2)` frame universal in active support four:    FALSE;
fixed-pair exclusions transported to `(3,1)`/`(4,1)`:   NOT JUSTIFIED;
all admissible based-frame stabilizer orbits:            OPEN;
active-support-five/six equality-five classification:    OPEN;
existence of full six-mode extensions from these pairs:  OPEN;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.
```

Any integration that makes this classification a live frontier node must
update the canonical frontier/navigation and theorem-ledger artifacts under
the repository contract.  This review does not perform that integration or
broaden the pair-level result.

## Final reviewed hashes

```text
theorem:
4B7FCCCCF68B55E1DDEACB7328B7469A8A82F36AA2AB0303E9094519A95FC5BC

primary verifier:
C99410B5D01F6BFB71B7C8F07859A83376BBF38A935B6F5313E4983A6BECFF07

independent audit:
62F1D4EDEBDAEE01D9F61DD43E705568DC18188A39EBFEE4A2FE971572961E03
```
