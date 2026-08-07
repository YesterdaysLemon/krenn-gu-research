# No `H31` lift on the symmetry orbit of the rank-two family chart

## Status

This is an exact characteristic-zero obstruction.

Take any admissible member of the five-parameter family in
[`P4_DECOMPOSABLE_RANK_TWO_FAMILY.md`](claims/p4/classifications/pair-geometry/decomposable-rank-two-family/P4_DECOMPOSABLE_RANK_TWO_FAMILY.md),
and apply arbitrary permutations of its four source coordinates and
four tensor modes.  No resulting pure `P_4` compression can be the pure
member of an `H31` pure/`Delta_2` pencil with rank-three ternary local
maps.

By
[`P4_PURE_RANK_TWO_COMPONENT_THEOREM.md`](claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_THEOREM.md),
the displayed family is a dense chart in a generically smooth
five-dimensional component of the plane locus.  This theorem excludes
the displayed **marked row section** and its source/mode symmetry
translates.  It does not exclude every marking over the corresponding
plane component.

This scope distinction is material.  The exact construction in
[`P5_H31_MARKED_BASIS_OPEN_BRANCH.md`](P5_H31_MARKED_BASIS_OPEN_BRANCH.md)
keeps the same four generic planes, shifts the complementary
pure-colour rows by their kernel rows, and obtains a binary `Delta_2`
extension off `L=0`.  That branch is still excluded by a separate
ternary determinant, but it is not covered by the mixed matrices below.

It also does **not** exclude all boundary markings of the component
closures.  Some plane boundaries have already been excluded by the
rank-one gate theorems, but all-rank-two marked fibres outside the
displayed row section remain part of the honest `H31` frontier.  Nor
does this theorem classify or exclude any additional components.

## Four orientations

Write the family rows as `A_r=V_r`, `B_r=U_r`, with parameters

```text
E I != 0,   L,Q,C arbitrary,   D=C+E I L != 0.       (1)
```

They give a pure tensor on source coordinates `0,1,2,3`.  In an `H31`
pencil, one of those coordinates is distinguished: it is present in
the pure hyperplane and replaced by the fifth source coordinate in the
neighbouring `Delta_2` hyperplane.

After undoing a mode permutation and relabelling the source
permutation, every symmetry translate reduces to exactly one of the
four choices

```text
q=0,1,2,3                                      (2)
```

for that distinguished family coordinate.  The case `q=3` is the
theorem already proved in
[`P5_H31_KNOWN_RANK_TWO_FAMILY_OBSTRUCTION.md`](P5_H31_KNOWN_RANK_TWO_FAMILY_OBSTRUCTION.md).
We treat the other three choices here.

For fixed `q`, retain the three source columns other than `q` and append
new fifth-coordinate entries

```text
A_r[p]=x_r,   B_r[p]=y_r.
```

Let `N_q` be the `14 x 8` coefficient matrix of the mixed binary words
on the neighbouring hyperplane.  Its kernel is exactly the space of
binary extensions having no mixed target coefficients.

## The open stratum `L != 0`

For `q=0,1,2`, respectively, direct permanent expansion gives the
following kernel generators:

```text
k_0=(1,L,-1/I,0 ; 0,0,0,1),
k_1=(Q,1,0,0 ; 1,0,1,0),
k_2=(0,-L,1/I,-1/(EI) ; D/(EI),1/I,0,1).             (3)
```

The semicolon separates the `x` and `y` entries.  Each vector is killed
by the corresponding `N_q`.  Rank seven follows without any hidden
genericity condition from the following pairs of `7 x 7` minors:

```text
q=0:
  4 E^3 I^9 L^4 (2LQ+1)(QD+EI),
 -4 E^3 I^6 L^3 Q^3;

q=1:
  4 E^4 I^6 L^6 (LQ+1)^2,
 -4 E^3 I^7 L^9 (LQ+2);

q=2:
 -4 E^4 I^2 L^2 (2LQ+1),
  4 E^4 L^2 Q^2.                                     (4)
```

For `q=0` or `q=2`, the second minor is nonzero when `Q!=0`,
and the first is nonzero when `Q=0`.  For `q=1`, the two minors
cannot vanish simultaneously.  Thus (3) spans the kernel in every
case under (1) and `L!=0`.

The two diagonal coefficient functionals `(AAAA,BBBB)` on these
generators are

```text
q=0: (0,2D),
q=1: (0,2D),
q=2: (0,2D/I).                                      (5)
```

The first diagonal always vanishes.  Hence no neighbouring binary
`Delta_2` tensor exists on the open stratum.

## The divisor `L=0`

Now `C!=0`.  Exact kernel bases are:

```text
q=0:
  r_0=(-Q,-1,0,0 ; 1,0,1,0),
  r_1=( 1, 0,-1/I,0 ; 0,0,0,1);

q=1:
  e_x0,e_x1,e_y0,e_y1,e_y2;

q=2:
  s_0=( I,0,0,-1/E ; C/E,1,0,0),
  s_1=(-Q,-1,0,0 ; 1,0,1,0),
  s_2=(-1,0,1/I,0 ; 0,0,0,1).                       (6)
```

Their dimensions are certified by nonzero minors

```text
rank N_0=6:  2 E^3 I^5,
rank N_1=3:  8 C E^2,
rank N_2=5:  E^3.                                   (7)
```

For `q=1`, the `AAAA` functional vanishes on all five kernel
generators, so this orientation has no binary `Delta_2` extension.

For `q=0`, write the extension as `t r_0+u r_1`.  Its diagonal
coefficients are

```text
AAAA=-2Qt,   BBBB=2(EI t+C u).                       (8)
```

Thus a `Delta_2` extension requires

```text
Q t (EI t+C u) != 0.                                (9)
```

At mode one, the one-marked map on the neighbouring hyperplane has the
`4 x 4` minor

```text
-8 I Q t^2(EI t+C u)/E,                             (10)
```

so it is injective under (9).

For `q=2`, write the extension as `t s_0+u s_1+v s_2`.  Its diagonal
coefficients are

```text
AAAA=(2/I)(-I t+Q u+v),
BBBB=2(C t+E u).                                    (11)
```

The mode-one marked map has two `4 x 4` minors

```text
 8 t(Ct+Eu)(It-Qu-v)/(EI),
 8 u(Ct+Eu)(It-Qu-v)/(EI).                          (12)
```

Under the `Delta_2` conditions from (11), `t,u` cannot both vanish.
Consequently at least one minor in (12) is nonzero, and this marked map
is injective as well.

## The third-colour contradiction

Let `G_1` be the third target-coordinate row at mode one.  All
one-`G_1` coefficients must vanish on both binary hyperplanes.
Injectivity in (10) or (12) forces

```text
G_1 restricted to the neighbouring hyperplane = 0.
```

Hence the full five-coordinate row `G_1` is supported only on the
distinguished coordinate `q`.

On the pure hyperplane, however, the mode-one one-marked map does not
kill that coordinate.  For `q=0`, its coefficient word `000` is `Q`,
which is nonzero by (9).  For `q=2`, its coefficient word `010` is
`1`.  Therefore `G_1=0`, contradicting rank three of the full local
map.

This excludes `q=0` and `q=2`; `q=1` was already excluded at the binary
stage, and `q=3` is the prior theorem.  All four orientations in (2)
are impossible, proving the symmetry-orbit obstruction.

## Verification

Run:

```text
python verify_p5_h31_rank_two_component_orbit.py
python audit_p5_h31_rank_two_component_orbit.py
```

The primary verifier reconstructs every mixed coefficient matrix,
checks the kernel bases and all displayed minors symbolically, and
rebuilds the marked-map determinants.  The independent audit uses a
dynamic-programming permanent and modular row reduction over `F_5` and
`F_7`.  It checks every admissible family parameter tuple in the three
new orientations and every projective exceptional extension capable of
having two nonzero diagonals.  The finite-field computation audits the
stratification; the proof above is over characteristic zero.
