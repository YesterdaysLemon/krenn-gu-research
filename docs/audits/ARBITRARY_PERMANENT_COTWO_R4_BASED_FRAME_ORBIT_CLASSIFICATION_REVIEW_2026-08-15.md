# Hostile review of the co-two `r=4` based-frame orbit classification

## Verdict and exact scope

**PASS, for the stated characteristic-zero, pair-level classification of
based frames in the three Delta-admissible active-support-four unbased
orbits.**  No rank-one-catalog, stabilizer-completeness, orbit-count,
representative-frame, field, implementation, or scope blocker survived
hostile review.

The reviewed theorem proves that the rank-one loci for the canonical
`(3,1)`, `(4,1)`, and `(4,2)` pairs contain exactly `4,6,6` projective
points.  Their bispanning triples number `2,14,12`.  Dividing by the full
ordered-pair monomial stabilizer gives `1,4,3` based-frame orbits; allowing
exchange of the two omitted modes gives `1,2,3` orbits.  All points are
rational, so no continuous based-frame modulus remains.

The classification is pair-level.  It neither constructs a full extension
nor itself transports a fixed-frame full-extension theorem through the other
modes.  The alternate `(4,1)` and `(4,2)` based frames remain separate
transport obligations.  Unrestricted `P_6 -> Delta_3` is unknown and the
global Krenn--Gu conjecture remains **UNRESOLVED**.

Reviewed frozen working-tree bytes:

```text
theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_COTWO_R4_BASED_FRAME_ORBIT_CLASSIFICATION_THEOREM.md
CFF044EA8E89D504F4ECF9C62CA55DFD5361CD54F5CB85083B09AED8B834D677

primary verifier:
claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_based_frame_orbit_classification.py
8560C80C85ABC643A7591161295C22BF052589BCFC0529CA2A067A452CB1BAF1

independent no-import audit:
claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_based_frame_orbit_classification.py
C1CF6B55A5B4880E8AC2FA251392D84BEA4DA8995A4F7F37FBA5B68D1BAD3B7C
```

No theorem or script edit was required by this review.

## 1. Rank-one criterion and quotient conventions

For a canonical pair of three-planes `U,V` with `B=UV` and `dim B=5`, let

```text
mu: U tensor V -> B,
L=mu^*(B^*) subset U^* tensor V^*.
```

Relative to ordered bases, `mu` is a `6 x 9` product-coefficient matrix of
rank five.  Its four-dimensional kernel supplies four bilinear membership
equations for the five-plane `L`: a rank-one tensor `a tensor b` belongs to
`L` exactly when it annihilates `ker(mu)`.

Three paired rank-one points give a pair-level `Delta_3` frame exactly when
their three left projective factors and three right projective factors both
span.  Indeed, their common kernel in `U tensor V` is the six-dimensional
off-diagonal coordinate space.  Since `ker(mu)` has dimension four and lies
there, its image is the two-dimensional mixed-product space; the three
diagonal products are independent modulo that space.  The converse is the
same argument in reverse.

Projectivizing each factor removes the independent nonzero colour scalings.
Passing from an ordered triple to an unordered three-subset removes common
colour permutation, but not an independent permutation on only one factor.
The package uses these quotient conventions consistently.

## 2. Exact characteristic-zero rank-one catalogs

Exact square-free multiplication of the three canonical product tables and
rational row reduction reproduced the four displayed membership equations
for each type.  Their solution sets were then attacked independently by the
nine disjoint charts in which the first nonzero coordinate of `a` and of `b`
is normalized to one.

### `(3,1)`

The equations include

```text
a_1 b_2=0,
b_1(a_0+a_2)=0.
```

If `a_1=0`, the remaining equations give either the coordinate points `P0`,
`P2`, or the single noncoordinate point

```text
((1,0,-1);(1,-1,0))=P3.
```

If `a_1!=0`, then `b_2=0`; the other equations force

```text
((0,1,0);(0,1,0))=P1.
```

Thus the catalog has exactly four points and no residual branch.

### `(4,1)`

The factored equations are

```text
a_0(b_1+b_2)=0,
a_1(b_0+b_2)=0,
b_1(a_0+a_2)=0,
```

together with the remaining bilinear equation.  On the branch `b_1=0`,
that equation gives exactly `P0,P2,P3`.  On `b_1!=0`, one has
`a_2=-a_0`.  If `a_0=0`, the unique point is `P1`.  If `a_0!=0`, then
`b_2=-b_1`; the alternatives `a_1=0` and `b_0=b_1` give exactly

```text
P4=((1,0,-1);(2,1,-1)),
P5=((1,-1,-1);(1,1,-1)).
```

Hence the catalog has exactly six points.

### `(4,2)`

All four equations factor:

```text
a_0(b_1-b_2)=0,        a_1(b_0-b_2)=0,
b_0(a_1-a_2)=0,        b_1(a_0-a_2)=0.
```

Splitting the last two equations into `b_0=0` or `a_1=a_2`, and `b_1=0`
or `a_0=a_2`, yields the three coordinate points `P0,P1,P3`, the two
two-support points `P2,P4`, and the all-one point `P5`.  These six branches
are exhaustive.

Every listed point is rational.  The chart calculations require only
division by normalized nonzero coordinates and, in the `(4,1)` catalog, by
`2`.  They are therefore valid over every characteristic-zero field.  No
algebraic-closure assumption, sampling argument, or finite-field lifting is
used for completeness.

## 3. Bispanning triples and absence of moduli

Exact left and right `3 x 3` determinants over the finite catalogs give:

```text
type      rank-one points      bispanning triples

(3,1)           4                      2
(4,1)           6                     14
(4,2)           6                     12
```

The triple lists in the theorem exhaust respectively all `4 choose 3` or
`6 choose 3` subsets.  A subset is accepted only when both factor matrices
have rank three.  Because every admissible frame is represented by one such
finite projective subset, with factor rescaling and common colour permutation
already quotiented out, there is no continuous based-frame modulus.

## 4. Full ordered-pair stabilizers

The finite actions were derived independently from the ambient monomial
stabilizers, rather than inferred from the stated point permutations.

Let `alpha,beta` be the two normal vectors, and let a monomial map have
coordinate permutation `sigma` and nonzero diagonal factors.  Preserving the
ordered pair is equivalent to sending each normal to a projective multiple
of itself.  On the common active support, the ratio

```text
r_i=beta_i/alpha_i
```

must therefore be carried by `sigma` to a common projective multiple of the
same ratio list.  The common zero support must also be preserved.  This gives
the complete finite residual groups:

```text
(3,1): ratio multiplicities 1+2 and one common zero -> S_2, order 2;
(4,1): ratio multiplicities 1+3                     -> S_3, order 6;
(4,2): ratio multiplicities 2+2
         -> (S_2 x S_2) semidirect S_2, order 8.
```

For `(3,1)`, the active coordinates have one common diagonal scale while the
inactive coordinate may have another.  Direct contragredient action on both
dual factors fixes all four projective rank-one points, so this connected
torus adds no orbit or modulus.  For the full-support types, a diagonal map
preserving a normal is projectively scalar and likewise contributes no
additional point action.

The induced point-label actions are exactly the theorem's generators:

```text
(3,1):  (P2 P3).

(4,1):  (P0 P4)(P2 P5),
         (P1 P4)(P2 P3).

(4,2):  (P1 P3)(P2 P4),
         (P0 P5)(P2 P4),
         (P0 P3)(P1 P5).
```

Enumerating every compatible ambient coordinate permutation gives exactly
`2,6,8` distinct actions, so the displayed generators are complete, not
merely a subgroup that happens to produce the advertised counts.

Their orbits on the bispanning triples are

```text
(3,1):  012                       size 2;

(4,1):  014, 013, 025, 235        sizes 1,6,6,1;

(4,2):  013, 025, 024             sizes 4,4,4.
```

Thus the ordered-pair orbit counts are exactly

```text
(1,4,3).                                                    (1)
```

For `(4,1)`, the invariant is the number `k` of selected points in
`T_+={P0,P1,P4}`.  For `(4,2)`, it is the number `e` selected from
`E={P2,P4}`.  These invariants separate the listed orbits.

## 5. Exchange of the omitted modes

Solving the corresponding monomial normal equations with `alpha` and `beta`
exchanged gives the exact factor-swapping actions

```text
(3,1): (P0 P1)(P2 P3),

(4,1): (P0 P5)(P1 P3)(P2 P4),

(4,2): (P0 P5)(P1 P3)(P2 P4).
```

Together with the ordered stabilizers, the induced action groups have orders
`4,12,16`.  In `(4,1)` the swap sends `k` to `3-k`, merging the two pure
orbits and the two mixed orbits.  In `(4,2)` it preserves `e`, and the unique
`(3,1)` ordered orbit was already complete.  The orbit counts after optional
mode exchange are therefore exactly

```text
(1,2,3).                                                    (2)
```

The labeled-mode and exchange-allowed conventions are stated separately and
are not mixed.

## 6. Eight integral representative frames

The primary verifier and the independent Fraction implementation both replay
all eight representatives:

```text
type      invariant/display label      catalog triple

(3,1)    unique                       012

(4,1)    k=3                          014
(4,1)    k=2, displayed               013
(4,1)    k=1                          025
(4,1)    k=0                          235

(4,2)    e=0, displayed               013
(4,2)    e=1                          025
(4,2)    e=2                          024
```

For each frame, exact checks establish:

```text
left and right basis ranks:                              3,3;
membership in the claimed normal hyperplanes:           YES;
mixed-product rank:                                      2;
total product rank:                                      5;
paired dual rank-one triple:                             AS DISPLAYED.
```

The alternate frames retain the two normal vectors of their claimed unbased
pair, so none changes unbased orbit while changing based-frame type.

## 7. Implementation and independence audit

Fresh replay of the frozen bytes gave

```text
primary exact verifier:                                  PASS;
independent no-import audit:                             PASS;
py_compile on both scripts:                              PASS;
Ruff on both scripts:                                    PASS.
```

The primary derives each four-dimensional equation space from the canonical
square-free product table with exact SymPy linear algebra, solves every pivot
chart, enumerates all bispanning triples and group orbits, and identifies all
eight integral frames.

Source inspection confirms that the audit imports neither the primary
verifier nor SymPy.  It uses a standalone `Fraction` row reducer for ranks,
basis coordinates, inverses, and frame recovery; it independently enumerates
the stated finite permutation actions and exhausts the bilinear loci over
`F_5` and `F_7`.

Those finite-field enumerations are **audit only**.  They check conventions
and catch extra reductions at two good primes; they do not prove the
characteristic-zero catalog.  That completeness is owned by the written
nine-chart factor argument and the exact primary replay.

One nonblocking independence limitation is recorded explicitly: the audit
hardcodes the membership equations and point actions rather than deriving
them anew from the canonical product tables and ambient normals.  Thus its
finite-field and group-closure passes are independent checks of the frozen
data, not a second derivation of those inputs.  The primary does derive the
equation spaces, and Sections 2, 4, and 5 of the written theorem give the
exact characteristic-zero and stabilizer derivations.  This limitation does
not change the theorem's status or the accurately stated audit boundary.

## 8. Accepted boundary

```text
field:                                                   CHARACTERISTIC ZERO;
canonical unbased types (3,1),(4,1),(4,2):              INPUT FROM PRIOR UNBASED CLASSIFICATION;
classification within each displayed canonical pair:    PROVED;
finite rank-one loci of sizes 4,6,6:                    PROVED;
all bispanning colour triples:                          CLASSIFIED;
ordered-pair based-frame orbit counts:                  1,4,3;
counts after optional omitted-mode exchange:            1,2,3;
continuous based-frame moduli:                          NONE;
eight displayed integral representatives:              CHECKED;

every (3,1) based frame equivalent to the displayed
  pair-level frame:                                     YES;
every (4,1) based frame equivalent to the displayed
  pair-level frame:                                     NO;
every (4,2) based frame equivalent to the displayed
  pair-level frame:                                     NO;

transport of fixed-frame full-extension exclusions to
  alternate (4,1) or (4,2) frames:                     NOT PROVED HERE;
existence of a full P_6 -> Delta_3 restriction:          NOT IMPLIED;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

## Final reviewed hashes

```text
theorem:
CFF044EA8E89D504F4ECF9C62CA55DFD5361CD54F5CB85083B09AED8B834D677

primary verifier:
8560C80C85ABC643A7591161295C22BF052589BCFC0529CA2A067A452CB1BAF1

independent audit:
C1CF6B55A5B4880E8AC2FA251392D84BEA4DA8995A4F7F37FBA5B68D1BAD3B7C
```
