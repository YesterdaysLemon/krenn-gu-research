# Hostile review of the fixed-pair Hamming-radius-two compression exclusion

## Verdict and provenance

**PASS, within the stated `W/V` compression scope.**  No mathematical,
quantifier, characteristic, or implementation blocker survived hostile review.
The package proves a pointwise characteristic-zero exclusion for arbitrary
independent triples at modes `2,3,4` inside the displayed four-space `W` and
matching mode-`5` vectors inside the displayed three-space `V`, assuming the
three nonzero pure coefficients and the 54 labelled middle-mode Hamming-one
and Hamming-two equations.

The result does not classify all simultaneous zeros of the two mixed
quartics, all low-projection components of the fixed-pair residual, or the
general radius-two problem.  Unrestricted `P_6 -> Delta_3`, arbitrary-order
permanent nonrestriction, and the global Krenn--Gu conjecture remain
**UNKNOWN/UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_HAMMING_RADIUS_TWO_COMPRESSION_EXCLUSION.md
  verify_arbitrary_permanent_fixed_pair_hamming_radius_two_compression_exclusion.py
  audit_arbitrary_permanent_fixed_pair_hamming_radius_two_compression_exclusion.py
```

The review independently reconstructed the compression coordinates, all five
pulled-back tensors, the shell-to-colour-diagonal implication, and the full
projection-rank split.  It specifically attacked sensor cancellation, the
meaning and count of the 54 equations, zero `A`-columns, isotropic rank-one
images, the rank-two common-zero-label lemma, mode-`5` independence, and the
positive-characteristic boundary.  No theorem or script edit was required.

The reviewed files were new relative to `origin/main` commit
`4efbbd2c4dc364930809cfceb5486268fa3fd00f`.  This establishes repository
novelty of the scoped `W/V` localization, not an external priority claim.

## 1. Dependency and exact scope

The package uses the fixed pair

```text
u=(x_0-x_3, x_1-x_3, x_2-x_3),
v=(x_1+x_2, x_0+x_2, x_2-x_3)
```

and its three diagonal quadratics and two mixed quadratics from
`ARBITRARY_PERMANENT_FIXED_PAIR_DIMENSION_FIVE_FULL_PROJECTION_BOUNDARY.md`.
It does not reuse that theorem's full-projection contradiction.  Instead, it
works in the explicit low-projection family

```text
W=ker(x_0) intersect ker(x_3-x_2-x_1),
V={z:x_4(z)=x_5(z)=0 and x_3(z)-x_2(z)-x_0(z)=-x_1(z)}.
```

Direct rank calculation gives `dim W=4` and `dim V=3`, with the bases printed
in the theorem.  Each of modes `2,3,4` may be any three-plane in `W` with any
ordered basis.  The application takes an arbitrary ordered basis at mode `5`.
The theorem statement is slightly stronger: it only asks for matching
vectors `z_e in V`, because pure nonvanishing alone supplies every property
of those vectors used in the proof.  No independence or normalization of the
`z_e` is silently invoked.

The earlier split-component theorem is a predecessor, not a dependency.  The
common-plane sharp fixture lies inside the new `W/V` family, which confirms
that this is a relevant enlargement of the localized residual; the fixture
has nonzero Hamming-two entries and is not a counterexample to the new
theorem.

## 2. Sensor factorization and automatic mixed radicals

Write `W=R direct-sum A`, where

```text
y=alpha(x_1+x_3)+beta(x_2+x_3)+a x_4+b x_5,
r(y)=(alpha,beta),
a(y)=(a,b),
J((a,b),(a',b'))=ab'+ba'.
```

For

```text
z=(gamma,delta,epsilon,gamma-delta+epsilon,0,0) in V,
```

the three covector pairs are

```text
p_0=alpha+beta,   q_0=epsilon,
p_1=beta,         q_1=gamma-delta+epsilon,
p_2=alpha,        q_2=gamma.
```

Every two distinct `p_e` span `R^*`, and the three `q_e` form a basis of
`V^*`.  Defining

```text
C(y_2,y_3,y_4)
 =r(y_2)J(a(y_3),a(y_4))
 +r(y_3)J(a(y_2),a(y_4))
 +r(y_4)J(a(y_2),a(y_3)),
```

direct square-free multiplication gives, with no omitted factorial or
polarization normalization,

```text
[x_0...x_5] d_e y_2y_3y_4z
 =sigma_e q_e(z)p_e(C(y_2,y_3,y_4)),
(sigma_0,sigma_1,sigma_2)=(2,2,-2).
```

The reason is exhaustive: `z` has no `x_4,x_5`, so exactly two of the three
`W` columns supply those variables, while the remaining `W` column and `z`
enter the corresponding four-coordinate pairing.  The three choices of the
remaining column are exactly the three summands of `C`; the two orders of
`x_4,x_5` are exactly `J`.

Both mixed tensors vanish on all of `W^3 x V`.  For

```text
F_2=x_0x_4x_5(x_3-x_2-x_1),
```

the three `W` columns cannot occupy four nonzero factor rows.  For

```text
F_1=x_1x_4x_5(x_3-x_2-x_0),
```

the two possible assignments of `x_1` and the last factor to the remaining
`W` column and the `V` column cancel because those restrictions are equal on
`W` and opposite on `V`.  Thus the mixed equations are consequences of the
compression geometry, not additional hypotheses or sampled behavior.

The primary verifier expands this identity with fully symbolic arbitrary
vectors.  The independent audit instead checks every entry of the
`4 x 4 x 4 x 3` multilinear-domain basis for all five tensors over each of
`F_3`, `F_5`, and `F_7`: 960 entries per field.  The modular checks are
falsification evidence; the symbolic identity and written multilinearity
argument supply the characteristic-zero statement.

## 3. The 54-equation quantifier bridge

For each anchor colour `e`, changing one of the three middle modes gives

```text
(3 choose 1)*2=6
```

labelled Hamming-one equations, and changing two gives

```text
(3 choose 2)*2^2=12
```

labelled Hamming-two equations.  Across the three anchors there are exactly
`3*(6+12)=54` coefficient equations.  “54” counts labelled coefficient
instances; it does not claim linear independence of the resulting
polynomials.

Pure nonvanishing and the sensor factorization imply separately

```text
q_e(z_e)!=0,
p_e(C_(eee))!=0.
```

Consequently every shell equation at anchor `e` forces
`p_e(C_(ijk))=0`.  If `(i,j,k)` uses two colours, its distances from the two
constant words are one and two, so two distinct `p` sensors vanish.  If it
uses all three colours, its distance from every constant word is two.  Since
any two `p_e` span `R^*`, all 24 nonconstant entries of `C` vanish, while the
three diagonal entries remain nonzero.

This bridge uses precisely the displayed middle-mode subset of the
accumulated radius-two target equations.  It does not use shell equations
that change modes `0`, `1`, or `5`.  The optional mode-`5` dual-basis
normalization in the note follows only from the fuller Hamming-one shell and
is correctly separated from the proof.

## 4. Off-diagonal orthogonality

Fix two distinct modes and two distinct labels.  Contracting `C` against the
two selected vectors gives a linear map `K:W->R`.  It kills the independent
three-vector family in the remaining mode because all three resulting colour
words are nonconstant.  Since `dim W=4`, this gives `rank K<=1`.

On the `R`-summand, however,

```text
K(r'',0)=J(a,a')r''.
```

If `J(a,a')` were nonzero, this restriction alone would have rank two.
Therefore all cross-mode, cross-label pairs satisfy

```text
J(a_(s,i),a_(t,j))=0 for s!=t and i!=j.
```

This step uses the full independence of each middle-mode triple but does not
assume that the triple spans all of `W`.  The primary verifier exposes the
scalar `2 x 2` block and its determinant `J(a,a')^2`.

## 5. Complete projection-rank split

Let `rho_t` be the span rank in the two-space `A` of the three projected
columns at mode `t`.  Rank zero is impossible: three independent vectors
would then lie in the two-dimensional `R`-summand.

For rank one, let `Ka` be the nonzero image line and let `S` be the nonzero
label set.  The hostile review checked both possible zero-column patterns:

- If `|S|>=2`, cross-label orthogonality puts every projected column of the
  other two modes in `a^perp`.
- If `|S|=1`, the same conclusion holds at the two labels outside `S`, which
  is all the proof needs.

If `J` vanishes on the square of `a^perp`, the required diagonal `C` value is
already zero.  Otherwise every pair of nonzero vectors on that line pairs
nontrivially, contradicting cross-label orthogonality between the other two
modes.  This covers isotropic lines and zero projected columns; no division
by a coordinate is hidden.

Thus all three arrays have rank two.  For two rank-two arrays satisfying the
cross-label equations, choose two independent columns `b_j,b_k` and let `h`
be the remaining label.  Then `a_h` lies in both one-dimensional orthogonal
lines `b_j^perp` and `b_k^perp`.  If it were nonzero those lines would agree,
forcing all three `a` columns into one line, contrary to rank two.  Hence
`a_h=0`.  The other two `a` columns are independent, so orthogonality forces
`b_h=0`.  Rank two also makes this zero label unique.

Applying the lemma to mode pairs `(2,3)` and `(2,4)` gives a common label at
which all three projected columns vanish.  Every term of `C_(hhh)` then
vanishes, contradicting the nonzero diagonal condition.  The proof therefore
exhausts projection ranks zero, one, and two.

The independent audit separately enumerates all 728 nonzero three-column
arrays over `F_3`: 104 have rank one and 624 have rank two.  It finds 5,728
directed compatible pairs and exhausts 9,504 unordered pairwise-compatible
mode triples, allowing repeated arrays.  None even satisfies the necessary
condition that each diagonal label have a nonzero matched `J` pairing.  This
is a genuinely independent finite-field counterexample search, not the
universal proof; the written rank split proves the theorem.

## 6. Characteristic and closure boundaries

The theorem is stated over characteristic zero.  Its proof in fact works
over every field of characteristic different from two: `J` remains
nondegenerate, any two `p_e` remain independent, the `q_e` remain a basis,
and each `sigma_e` is nonzero.  Characteristic two is excluded because the
diagonal factors `2,-2` vanish; the claimed pure coefficients cannot be
obtained through this factorization.

The argument is pointwise and purely linear/multilinear.  It does not use an
algebraic closure, Zariski closure, genericity, a dense open set, or division
by a variable parameter.  It proves no component-cover or classification
claim beyond the explicitly named `W/V` family.

## 7. Computational independence and final replay

The primary verifier uses SymPy and a sparse six-variable square-free
algebra.  It checks the displayed compression coordinates, the symbolic
sensor factorization, both automatic mixed radicals, all shell combinatorics,
the contraction-map block, normalized rank-case algebra, and inclusion of the
prior sharp fixture.

The independent audit imports neither the primary module nor SymPy.  It uses
custom modular sparse multiplication, multilinear basis exhaustion, a
separate shell cover, and exhaustive `F_3` enumeration of the abstract
projection obstruction.  It is independent in representation, arithmetic,
and finite search route, while the written proof remains the source of the
universal characteristic-zero conclusion.

Focused final replay passed:

```text
new primary verifier:                         PASS;
new independent no-import audit:             PASS;
new py_compile:                              PASS;
new Ruff check:                              PASS;
Hamming-two split-component predecessor:     PASS/PASS;
fixed-pair full-projection predecessor:       PASS/PASS.
```

The new audit reported:

```text
W^3 x V basis-tensor entries:       960 in each of F_3,F_5,F_7;
shell counts:                       6 H1 + 12 H2 per anchor;
nonconstant anchor cover:           18 words by two, 6 words by three;
nonzero F_3 A-arrays:               728;
pairwise-compatible triples:        9,504;
triples passing diagonal necessity: 0.
```

## 8. Novelty and remaining obligations

The repository-level new content is the localization of the radius-two
constraints to the four-dimensional `W` compression, the factorization
through the `R`-valued tensor `C`, and the projection-rank obstruction ending
in a common zero label.  The fixed pair and its mixed quartics are inherited
from the predecessor package; the new theorem does not reclassify the full
mixed-zero locus.

Accepted boundary:

```text
W/V compression under three pure + 54 middle H1/H2:  EXCLUDED;
arbitrary three-planes and bases inside W:            INCLUDED;
matching mode-5 vectors in V, subject to pure nonzero: INCLUDED;
mixed-radical equations on W^3 x V:                   AUTOMATIC;
other mixed-quartic zero loci:                        NOT CLASSIFIED;
general fixed-pair radius-two residual:               OPEN;
unrestricted P_6 -> Delta_3:                          UNKNOWN;
arbitrary-order permanent nonrestriction:             UNKNOWN;
global Krenn--Gu conjecture:                          UNRESOLVED.
```

Any integration that makes this exclusion a live frontier node must update
the canonical frontier/navigation and theorem-ledger artifacts under the
repository contract.  This review does not perform that integration, broaden
the theorem, or discharge unrelated proof obligations.

## Final reviewed hashes

```text
theorem:
A88039A5D090311C4D6C8EFDEA194E945710756CB699B825E24E7547DA57FCB6

primary verifier:
A47FEEC379085D6ED1EA989B805D0D2F325E1AB96410956004211AA8F100A259

independent audit:
30369FF970CB2447C7AF40432E36E2206213408A3457C264F3AA72188CD27921
```
