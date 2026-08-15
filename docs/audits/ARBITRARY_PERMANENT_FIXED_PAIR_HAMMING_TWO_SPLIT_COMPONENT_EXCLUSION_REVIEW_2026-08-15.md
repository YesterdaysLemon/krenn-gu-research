# Hostile review of the fixed-pair Hamming-two split-component exclusion

## Verdict and provenance

**PASS, with the two stated split-family scopes.**  No mathematical or
implementation blocker survived hostile review.  The package proves two
pointwise characteristic-zero exclusions in the low-projection residual of
the fixed pair-dimension-five theorem:

1. a common plane `H=span{x_4,x_5,h}` with arbitrary bases at modes `2,3,4`
   is incompatible with the three nonzero pure equations and the exact
   Hamming-two equations when mode `5` dualizes the fixed pair as stated; and
2. the affine planes
   `H_t=span{x_4,x_5,h(s_t)}` with arbitrary parameters and bases, together
   with an arbitrary basis of the displayed three-plane `Z` at mode `5`, are
   incompatible with the nonzero colour-two pure coefficient and the
   accumulated Hamming-one and Hamming-two equations.

The two conclusions do not classify the full low-projection residual, all
simultaneous zero tensors of the mixed-radical quartics, or cancellation-based
components outside the named families.  Unrestricted `P_6 -> Delta_3`,
arbitrary-order permanent nonrestriction, and the global Krenn--Gu conjecture
remain **UNKNOWN/UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_HAMMING_TWO_SPLIT_COMPONENT_EXCLUSION.md
  verify_arbitrary_permanent_fixed_pair_hamming_two_split_component_exclusion.py
  audit_arbitrary_permanent_fixed_pair_hamming_two_split_component_exclusion.py
```

The review independently reconstructed both tensor factorizations before the
files arrived, then compared the written proof and both implementations
against that derivation.  It attacked shell quantifiers, arbitrary-basis
cancellation, the dimension and scope of `Z`, zero pure factors, and the
`P_3` slice-space invariant.  Two overbroad sharpness sentences found during
review were corrected to retain the pure hypotheses and, in the affine
family, the Hamming-one equations.

## 1. Dependency and proof-topology boundary

The package uses the exact fixed two-mode product table and the five
complement quartics from
`ARBITRARY_PERMANENT_FIXED_PAIR_DIMENSION_FIVE_FULL_PROJECTION_BOUNDARY.md`.
It does not import that theorem's full-projection argument.  Instead, it
attacks two explicit pieces of the residual where the projected ranks are
already allowed to drop.

The only additional tensor fact is a self-contained slice-space property of
the order-three permanent `P_3`.  The theorem reproves it by three principal
minors, so no unreviewed external classification or tensor-rank assertion is
load-bearing.

The later proposed `W/V` compression is a separate possible successor.  It is
not used by this package and was not required for this verdict.

No generic-point, closure, orbit-normalization, or exhaustive residual-cover
claim occurs.  Both exclusions are exact implications inside explicitly
parameterized families.

## 2. Fixed quartics and coefficient convention

Direct edge complementation in the square-free algebra gives

```text
star(m_1)= x_4x_5 x_1(x_3-x_2-x_0),
star(m_2)= x_4x_5 x_0(x_3-x_2-x_1),

star(d_0)= x_4x_5(x_1+x_2)(x_3-x_0),
star(d_1)= x_4x_5(x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5x_0x_1.
```

The review recomputed all five identities from the fixed product vectors.
For a complementary colour word `w`, the coefficient

```text
T_q(w)=[x_0x_1x_2x_3x_4x_5] q y_2y_3y_4y_5
```

therefore has no normalization or polarization ambiguity.

When the first two colours are fixed to `(c,c)`, an exact Hamming-`j` word
around `c^6` is precisely a complementary word at distance `j` from `c^4`.
The first theorem uses only distance exactly two.  The second theorem uses the
union of distances one and two.  Neither proof silently replaces one
condition by the other.

## 3. Common-plane factorization under arbitrary bases

Let `H=span{x_4,x_5,h}`, where `h` is a nonzero first-four-coordinate form.
At modes `2,3,4`, write arbitrary ordered bases of `H` relative to
`(x_4,x_5,h)` as invertible matrices `A_2,A_3,A_4`, and define

```text
R(i,j,k)=P_3(A_2e_i,A_3e_j,A_4e_k).
```

The requirement that mode `5` dualize the fixed pair is an explicit component
hypothesis, not an inferred property of every first-four-coordinate plane.
For its basis `z_e`, it gives the diagonal pairing weights `mu_c!=0` and kills
the two mixed rows.

Every full-monomial contribution must take `x_4` and `x_5` from two of modes
`2,3,4`; the remaining mode supplies `h`.  Terms using two copies of `h`
cannot supply both `x_4,x_5`, and terms repeating `x_4` or `x_5` vanish in the
square-free algebra.  Consequently, with no uncatalogued cancellation,

```text
T_(d_c)(i,j,k,e)=mu_c delta_(c,e) R(i,j,k),
T_(m_1)=T_(m_2)=0.
```

This identity is multilinear in the columns of each `A_t`, so checking it in
the reference bases proves it for arbitrary bases.  As an additional hostile
regression, five independently chosen integral `GL_3` triples were expanded
directly in the six-variable square-free algebra.  All 1,215 tested diagonal
pairing identities agreed with the displayed factorization.

## 4. Why exact Hamming two kills the common plane

Every nonconstant ternary triple `(i,j,k)` has a colour `e` occurring exactly
once.  The full word

```text
(e,e,i,j,k,e)
```

then differs from `e^6` in exactly the other two middle positions.  It is an
exact Hamming-two word, not merely a word of accumulated radius at most two.
The Hamming-two equation and `mu_e!=0` force `R(i,j,k)=0`.

This singleton-colour construction covers all 24 nonconstant ternary triples:
the `2+1` and `1+1+1` multiplicity patterns both have a singleton.  The three
pure equations make the three diagonal entries nonzero.  Hence the assumed
target equations would make `R` a concise diagonal tensor.

But `R` is a `GL_3^3` translate of `P_3`.  Its incompatibility with a concise
diagonal tensor is checked by the invariant in Section 6 below.  No
Hamming-one equation is used in this argument.

## 5. Affine `h(s_t),Z` factorization and exact quantifiers

The affine family is

```text
h(s)=x_1+s x_2+(1+s)x_3,
H_t=span{x_4,x_5,h(s_t)},
Z=ker(-x_0+x_1-x_2+x_3)
  subset span{x_0,x_1,x_2,x_3}.
```

The normal defining `Z` is nonzero, so `Z` has dimension three in the
four-dimensional first-coordinate space.  Thus an arbitrary independent
mode-`5` triple in `Z` is exactly an arbitrary ordered basis of `Z`; no
additional ambient `x_4` or `x_5` directions are being admitted.

For `z=(z_0,z_1,z_2,z_3) in Z`, independent calculation gives

```text
<m_1,x_4x_5h(s)z> = -z_0+z_1-z_2+z_3 = 0,
<m_2,x_4x_5h(s)z> = 0,
<d_0,x_4x_5h(s)z> = 2(1+s)z_2,
<d_1,x_4x_5h(s)z> = 2s z_3,
<d_2,x_4x_5h(s)z> = -2z_0.
```

The first two identities show that both mixed-radical tensors vanish for
every choice of the three parameters and all four local bases.  The last
identity is independent of `s` and of which middle mode supplies its
`h(s_t)` factor.  Therefore, for arbitrary invertible middle basis matrices,

```text
T_(d_2)(i,j,k,e)=-2x_0(z_e)R(i,j,k),
```

with the same `GL_3^3` translate `R` of `P_3`.

The colour-two pure coefficient says

```text
-2x_0(z_2)R(2,2,2) != 0.
```

Thus neither factor may be zero.  Holding colours at modes `2` and `5` equal
to two, the eight remaining words `(2,2,2,j,k,2)` with
`(j,k)!=(2,2)` split as four exact Hamming-one and four exact Hamming-two
words.  The accumulated radius-two equations force all eight other entries
of the colour-two slice to vanish.  Its `(2,2)` entry remains nonzero, so the
slice has rank one.

This proof genuinely uses both shells.  Exact Hamming two alone does not kill
the four entries in which exactly one of `j,k` differs from two.  Conversely,
the conclusion also depends on the nonzero colour-two pure coefficient; the
reviewed wording no longer claims exclusion from family membership alone.

Five referee-side exact trials with independently chosen integral parameters,
three arbitrary `GL_3` middle bases, and an arbitrary `GL_3` basis change of
`Z` checked another 1,215 mixed/`d_2` identities.  All mixed coefficients
were zero and every `d_2` coefficient agreed with the factorization above.

## 6. Slice-space invariant and basis changes

In a standard first-mode slicing, the slice space of `P_3` consists of

```text
         [ 0   a_2 a_1]
A(a)=   [a_2   0  a_0].
         [a_1  a_0  0 ]
```

The three principal two-by-two minors are

```text
-a_2^2,       -a_1^2,       -a_0^2.
```

If a slice had rank at most one, all these minors would vanish, hence
`a_0=a_1=a_2=0` over a field.  The slice space therefore contains no nonzero
rank-one matrix.

This property survives arbitrary local basis changes.  A change in the first
mode only changes the basis used to span the same slice space.  Changes in the
other two modes left- and right-multiply every slice by invertible matrices,
which preserve individual matrix ranks.  Thus neither common-plane nor affine
basis freedom can create the rank-one slice forced by the shell equations.

The independent audit exhausts all 125 slices over `F_5` and obtains the rank
histogram

```text
rank 0: 1,       rank 1: 0,       rank 2: 60,       rank 3: 64.
```

This finite calculation is a falsification audit; the three-minor argument is
the universal proof.

## 7. Characteristic boundary and sharp fixture

The package correctly states characteristic zero and does not silently extend
the fixed-pair result to positive characteristic.  In characteristic two,
`d_2` and all coefficients carrying its factor `-2` vanish, so the affine
colour-two pure step is unavailable.  The review therefore retains the stated
scope even though the isolated `P_3` slice-minor argument works more broadly.

At `s_2=s_3=s_4=-2`, the previous sharp fixture lies in both named families.
Its mode-`5` vectors form a basis of `Z`, and the stripped pairing matrix is

```text
[[0,0,0],
 [0,0,0],
 [-4,0,0],
 [0,8,0],
 [0,0,-2]].
```

Direct replay again gives projection profiles `(3,3,3,1)` and `(2,2,2,2)`,
three nonzero pure coefficients, all Hamming-one coefficients zero, and nine
nonzero Hamming-two coefficients.  The canonical 729-word table retains
SHA-256

```text
1360041C9A60D4451F58F18B978DFB30C86B707BB4FC7C860D7573D4686A7DA8.
```

The new theorems say that these nine coefficients cannot all be removed in
the common-plane family while retaining the pure equations, or in the affine
family while retaining the colour-two pure coefficient and all Hamming-one
equations.  They do not claim that arbitrary parameter or basis changes must
preserve those auxiliary target equations automatically.

## 8. Computational independence and replay

The primary verifier uses SymPy and a sparse six-variable square-free algebra.
It reconstructs all five quartics, derives the affine identities symbolically,
checks the reference `P_3` support and singleton map, expands the affine
`d_2` tensor for arbitrary symbolic parameters, verifies the slice minors,
and replays the sharp fixture.

The independent audit imports neither the primary module nor SymPy.  It uses
custom sparse arithmetic, exact `Fraction` elimination, direct 720-term
permanents, and separate finite-field enumeration.  Over `F_5` it checks 625
affine pairing instances, 421,875 `d_2` reference-tensor instances across all
parameter triples and all `Z` vectors, and all 125 `P_3` slices.

Focused final replay passed:

```text
new primary verifier:                         PASS;
new independent no-import audit:             PASS;
new py_compile:                              PASS;
new Ruff check:                              PASS;
fixed-pair full-projection predecessor:      PASS/PASS.
```

The programs replay exact identities and independently stress conventions.
The arbitrary-basis and characteristic-zero conclusions are supplied by the
written multilinearity and slice-invariance arguments, not by finite sampling
alone.

## 9. Novelty and remaining obligations

The new content is the localization of exact Hamming-shell constraints to two
explicit low-projection split families.  The `P_3` rank-one-free slice-space
fact itself has antecedents elsewhere in the repository; this package does
not claim it as a new invariant.  The application to the fixed pair, the
common-plane singleton-colour cover, and the affine `d_2` factorization are the
scoped successor results.

Accepted boundary:

```text
common-H family under pure + exact H2:                  EXCLUDED;
affine h(s_t),Z family under colour-2 pure + H1 + H2:   EXCLUDED;
arbitrary bases within both named families:             INCLUDED;
arbitrary affine parameters s_2,s_3,s_4:                INCLUDED;
all mixed-radical zero-tensor components:               NOT CLASSIFIED;
general fixed-pair radius-two residual:                 OPEN;
separate W/V compression successor:                    NOT USED HERE;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
arbitrary-order permanent nonrestriction:               UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.
```

Any integration that treats these exclusions as new live frontier nodes must
update the canonical frontier/navigation artifacts under the repository
contract.  This review does not broaden the theorem or discharge unrelated
integration and publication obligations.

## Final reviewed hashes

```text
theorem:
B47171CF8AB8129889FCB211C6B7C53E99FF84D5B913E7CE37384F9EFB5A5D0C

primary verifier:
55541B1B0310EDC930F435AB3C3277BEA7B854989B1DC5D618524241B571737E

independent audit:
BFEA62BB75F2B7DB6D8AC8FE70EB6D2804EEE76279C45F1D85EE14168185658B
```
