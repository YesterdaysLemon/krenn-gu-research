# Self-review of the `(1,2,2)` `alpha_s`-coloop exclusion

## Review verdict

The claimed orientation exclusion is supported.  In the S2AZ `(1,2,2)`
gauge, the assumption `N subset {alpha_s=0}` puts each member of a complete
projective determinant-face pencil into three two-planes in one
at-most-three-space.  The two coordinate-projection determinants either
produce the already-forbidden binary diagonal cube or vanish in one of two
exact ways.  The one-sided cases are the existing same-third-row
obstruction.  The common degeneration gives a same-pair table, and the new
lemma exhausts all incidences of its three row planes.

This closes only `N subset {alpha_s=0}`.  Seven `(1,2,2)` coordinate
coloops, joint rank at most four, other physical components and pole strata,
higher orders, and the global conjecture remain open.  Global Krenn--Gu
remains **UNRESOLVED**.

## Scope and inherited identities

### Is the selected coloop used with its exact scope?

Yes.  S2AZ proves that, for any selected coordinate hyperplane `F`,

```text
dim H^T(L intersect F)=2,
L=(ker D_B)^perp.
```

For `F={alpha_s=0}`, that image contains
`R=rho(e_s^perp)`, already proved two-dimensional.  Equality therefore gives

```text
H^T(L intersect {alpha_s=0})=R.
```

No assertion about the six-row image of either complementary first-root
coloop is used.

### Are `pi` and `theta` really injective outside the `beta_t` coloop?

Yes.  Their injectivity proof uses only the S2AZ gauge, not the later
`beta_t`-coloop assumption.  Each map has a rank-two image modulo
`V=H^T(L)`, because the evaluation pairs `(y,e_t)` and `(z,w)` are
independent.  The respective evaluation-kernel line is nonzero.  If its row
vanished, the corresponding root contraction would kill both `D_B(K)=U`
and the all-cross term, while the target contraction is a nonzero linear
combination of the independent `T_i`.  Hence each residual row is nonzero
and each three-dimensional root-row map has rank three.

## Determinant-face pencil audit

### Is equation (10) a complete face rather than a sampled identity?

Yes.  For every projective direction `[h:k]`, the evaluation pairs of
`P_delta` and `Q_delta` are proportional to `(h,k)`.  Their determinant

```text
beta(y) gamma(w)-mu beta_t gamma(z)
```

therefore vanishes identically on the product of the two planes.  Setting
`alpha_s=0` kills the other two components of the derivative transpose.
Thus every product functional on the whole `2 x 2 x 2` face annihilates
`U`, and the full target equation applies.

### Why do the three row planes share one at-most-three-space?

The evaluation-kernel line of each pencil plane maps into `R` via the exact
coloop image.  Representatives with opposite evaluation pairs combine to an
element of `L intersect {alpha_s=0}`, so their `p` and `q` rows sum to an
element of `R`.  Consequently their quotient classes modulo `R` span the
same line.  Hence

```text
R, p(P_delta), q(Q_delta) subset R+span(p(beta_delta)).
```

Injectivity makes all three images two-dimensional.  This argument uses
neither a pointwise choice of `H` nor an assumed equality of row planes.

### Are the projection gates correct?

Yes.  A covector plane `n^perp` projects isomorphically to the two
coordinates complementary to `s` exactly when `n_s` is nonzero.  The two
normals are

```text
k y-h mu e_t,                    k z-h w,
```

whose `s` coordinates are precisely

```text
L_P=k y_s-h mu delta_(s,t),      L_Q=k z_s-h w_s.
```

When both are nonzero, coordinate lifts turn the complete face into the
S2AN binary diagonal cube.  If the common space has dimension only two, the
three row planes agree and the equal-plane proof of that obstruction applies.

## Projective fork audit

### Does pointwise gate failure imply the stated global alternatives?

Yes.  The binary diagonal obstruction gives `L_P L_Q=0` at every rational
projective direction.  A characteristic-zero field is infinite, so this
homogeneous quadratic is the zero polynomial.  The polynomial ring is an
integral domain, hence one linear factor is identically zero.  The first
factor vanishes identically exactly when `s!=t` and `y_s=0`; the second does
so exactly when `z_s=w_s=0`.

This is an exact polynomial identity, not promotion from a generic sample.

### Are the finite-avoidance choices legitimate over the stated field?

Yes.  Each later choice excludes only roots of finitely many nonzero linear
forms on `P^1`: the two coordinate directions, one surviving gate, and at
most two directions where an active annihilator becomes coordinate.  An
infinite field has a direction outside that finite union.  No algebraic
closure or numerical specialization is used.

### Do the one-sided alternatives exactly match S2AO?

Yes.  Under `A` alone, `P_delta` consists of an invisible `e_s^*` row and
one row active in both complementary target coordinates, while `Q_delta`
has coordinate lifts.  The two nonzero cells share the active second row;
exchanging the last two permanent arguments makes it the S2AO
same-third-row table.  Under `B` alone, the roles are reversed and the two
cells directly share the active third row.  Injectivity ensures that every
displayed ordered pair is a genuine basis.

## Same-pair lemma audit

### Is the source-coordinate zero pattern complete?

Yes.  The row table has eight cells and only `(0,1,1)` and `(1,1,1)` are
nonzero.  Their values are scalar multiples of fully transverse targets
`T_0,T_1`.  In source coordinates extending those target factors, every
coefficient product except `xi_0 eta_0 zeta_0` and
`xi_1 eta_1 zeta_1` restricts to zero on `R x P x Q`.  The positions of the
two target coefficients inside the row table do not change this
source-coordinate kernel statement.

### Are all pairwise-distinct plane incidences covered?

Yes.  Three distinct plane normals in a three-space either are independent
or span a two-dimensional pencil.  Exact row reduction gives respectively

```text
span(A^3,B^3,C^3),
span(A^3,B^3,AB(A+B)).
```

In the first kernel, the S2AN shared-quadratic divisor argument makes the
two coordinate forms in every target pair proportional and contradicts a
zero mixed coefficient.  In the pencil kernel, unique factorization puts
all source-coordinate forms in the two-dimensional normal pencil, although
they must span the dual of the embedded three-space.

### Are all equal-plane incidences covered?

Yes.

- If `R=P`, symmetry of `L F` applied separately to the independent target
  coefficients `E_01` and `E_11` kills the entire first row of the change
  matrix `L`.  The `R=Q` case is identical by permanent symmetry.
- If `P=Q`, symmetry at `E_11` makes `q_0` proportional to `p_0`.  The zero
  mixed column then identifies both surviving values with the single square
  map `per(-,p_1,p_1)|R`.  Its image contains two fully transverse
  decomposable tensors, contrary to the S2AL tangent-line separation lemma.

If all three planes agree, the first bullet already gives a contradiction.
If the ambient common space has dimension two, all three two-planes agree.
Thus no incidence is omitted.

## Evidence and independence audit

The primary SymPy replay checks the determinant face, both coordinate gates,
the coefficients of the projective factor fork, representative exact tables
for all four gate patterns, the independent and pencil cubic restriction
kernels, and all equal-plane matrix orientations.

The independent audit imports neither SymPy nor the primary verifier.  It
uses `fractions.Fraction`, its own determinant and row-reduction routines, a
reversed symmetric-cubic coefficient order, separately chosen rational
fixtures, and direct reconstruction of the equal-plane matrices.

The scripts replay displayed identities and exact finite-dimensional linear
algebra.  They do not replace the arbitrary-field polynomial, divisor,
unique-factorization, or incidence-exhaustion arguments in the proof.

## Remaining obligations

This result proves only

```text
N subset {alpha_s=0}                              IMPOSSIBLE.
```

Together with S2BB, two of the nine S2AZ coordinate coloops are closed.
The other seven coloop orientations, joint rank at most four, other physical
component types and low-span pole strata, higher orders, and global
resolution remain open.  Global status stays **UNRESOLVED**.
