# Hostile review: `P_6` co-two dimension-six pair moduli

## Verdict and exact scope

**PASS, for the stated characteristic-zero pair-level sharpness theorem.**

The reviewed conclusion is deliberately negative about the proof route:

```text
the minimal surviving value dim B_ab=6 already contains
a nine-dimensional open family of pair-level admissible frames;
coordinate monomial orbits have dimension at most five;
the maximal linear complementary envelope has dimension twelve
and restricted pairing rank three.                              (1)
```

Therefore the finite equality-five orbit/endpoint method does not continue
by replacing five with six.  This verdict does **not** factor the linear
envelope through four further local planes, satisfy all fifteen pair
conditions, construct `P_6 -> Delta_3`, or prove nonrestriction.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Reviewed surface

The package consists of:

```text
ARBITRARY_PERMANENT_P6_COTWO_DIMENSION_SIX_PAIR_MODULI_AND_LINEAR_ENVELOPE_BOUNDARY.md;
verify_arbitrary_permanent_p6_cotwo_dimension_six_pair_moduli_and_linear_envelope.py;
audit_arbitrary_permanent_p6_cotwo_dimension_six_pair_moduli_and_linear_envelope.py.
```

Their normalized-LF SHA-256 values are recorded after the final hostile
replay:

```text
theorem:             c1f0db88f62d0abf4f16fb94c5f73c66cd03156662be97b4de7fe368400dbbbf
primary:             ce025ac7d2b647ad1df7444d671a805707708a6a35b6b044962e5c906d147530
independent audit:   40479837fd0bdd84a373dfaade5d87517d817c86b5a5b7f3d2df87fc26af834f
```

## 2. Algebra and characteristic attack

The explicit plane is

```text
U=span{x_0+x_3,x_1+x_4,x_2+x_5}.                       (2)
```

The six symmetric products have a named minor on edge rows

```text
03,14,25,01,02,12
```

equal to `diag(2,2,2,1,1,1)`, with determinant eight.  This proves
injectivity of `Sym^2(U)` in characteristic zero.  The factor two in each
square is essential; the theorem does not claim characteristic two.

The union of the supports in (2) is all six coordinates.  Full active
support does not mean that each individual basis vector uses all six
coordinates, and the proof never makes that stronger claim.

## 3. Pair-level admissibility attack

Using the same basis at the two omitted modes makes the ordered mixed
products repeat exactly three unordered cross products.  Injectivity of the
symmetric square gives

```text
dim B=6,        dim M=3,        dim B/M=3.              (3)
```

The three squares give a basis modulo `M`.  This is precisely the one-pair
mixed-radical/diagonal-quotient condition.  Coincident local planes are
allowed: local concision requires each plane to have dimension three, not
that different modes supply different subspaces.

No converse to the full restriction condition is used.  Pair-level
admissibility supplies neither the remaining four modes nor their 81
quartic products.

## 4. Open-family attack

The rank-six condition is the nonvanishing of a maximal minor in each
Grassmann chart and is therefore open.  Equation (2) proves that open is
nonempty.  Avoidance of the six coordinate hyperplanes is also open and is
satisfied by (2).  Since `Gr(3,6)` is irreducible of dimension nine, their
intersection is a nonempty nine-dimensional open.

This argument does not say that every three-plane has injective symmetric
square.  It only supplies the nonempty open family needed to refute a finite
orbit cover.

## 5. Linear-envelope attack

The degree-two/degree-four complement pairing has ambient dimension fifteen
on each side.  For `A_lin=M^perp`, exact duality gives

```text
dim A_lin=12,
left-radical(B x A_lin)=B intersect M=M,
rank(B x A_lin)=3.                                      (4)
```

Thus `6+12=18` saturates the co-two dimension-sum bound at the level of an
arbitrary linear complement.

The word *linear* cannot be dropped.  The actual sensor from four other
modes is a span of factored quartics.  Neither replay searches for those
four planes, and no statement identifies `A_lin` with such a product span.
Promoting (4) to an actual six-mode tensor would be a fatal quantifier error.

## 6. Orbit-dimension attack

The connected coordinate-scaling torus has dimension six.  Its scalar
diagonal acts trivially on the Grassmannian, so every effective monomial
orbit has dimension at most five; the finite coordinate-permutation group
does not change that dimension.  The diagonal embedding `U -> (U,U)` of the
nine-dimensional open remains nine-dimensional.  A finite union of orbit
closures of dimension at most five cannot cover it.

The conclusion is only that a finite list of monomial representatives is
impossible.  It does not rule out a uniform theorem over the moduli, a
different larger covariance group, or a global obstruction that avoids
classification entirely.

## 7. Relation to the live residual

The predecessor equality-five exclusion forces `dim B_ab>=6` at all fifteen
pairs of any hypothetical exact restriction.  This package assesses the
minimal equality-six stratum and proves that its one-pair algebra is broad.
The still-open obligations are:

1. factor the relevant subspace of `M_ab^perp` by four local three-planes;
2. impose the constant-colour/nonconstant-colour quartic incidence; and
3. make those data compatible across all fifteen omitted pairs.

The five-map simultaneous-kernel criterion is a valid global encoding of
the same mixed target equations, but this theorem neither solves nor weakens
its nonlinear factorization condition.  Dimensions seven, eight, and nine
also remain open.

## 8. Primary/audit independence

The primary uses SymPy over the rationals.  It builds the square-free
products, checks the named determinant exactly, computes a rational basis of
`M^perp`, and evaluates the restricted pairing.

The independent audit runs under `python -I`, imports neither the primary
nor SymPy, and uses separately implemented modular row reduction and kernel
construction over `F_101` and `F_103`.  It independently enters the three
linear forms and reconstructs all coefficients.  Agreement at two primes is
an audit of the displayed integral fixture; the written determinant and
dimension arguments prove the characteristic-zero statements.

Both computations are fixed matrices of size at most `15 x 12`.  No symbolic
Groebner basis, nonlinear solve, unbounded enumeration, or high-memory job is
launched.

## 9. Hostile failure-mode checklist

```text
determinant eight used in characteristic two:               REJECTED;
active support six confused with dense individual forms:    REJECTED;
coincident local planes forbidden without reason:           REJECTED;
ordered mixed products counted as six dimensions:           REJECTED;
pair-level admissibility promoted to full extension:         REJECTED;
M^perp promoted to a factored four-mode sensor:              REJECTED;
one omitted pair promoted to all fifteen:                    REJECTED;
finite-orbit failure promoted to nonrestriction:             REJECTED;
equality-six assessment promoted to dimensions seven--nine:  REJECTED;
P_6 statement promoted to arbitrary order:                   REJECTED;
numerical or modular evidence used as the theorem proof:      REJECTED;
global status strengthened:                                  REJECTED.       (5)
```

## 10. Accepted boundary

```text
full-support pair-level equality-six frames:              NONEMPTY OPEN;
dimension of the open family:                             NINE;
maximum monomial-orbit dimension:                         FIVE;
minimum parameter gap:                                    FOUR;
linear complementary dimension twelve / rank three:       PROVED;
finite monomial-orbit equality-five-style continuation:     BLOCKED BY MODULI;

factored four-mode complementary sensor:                   OPEN;
simultaneous fifteen-pair mixed incidence:                 OPEN;
unrestricted P_6 -> Delta_3:                              UNKNOWN;
global Krenn--Gu conjecture:                               UNRESOLVED.
```
