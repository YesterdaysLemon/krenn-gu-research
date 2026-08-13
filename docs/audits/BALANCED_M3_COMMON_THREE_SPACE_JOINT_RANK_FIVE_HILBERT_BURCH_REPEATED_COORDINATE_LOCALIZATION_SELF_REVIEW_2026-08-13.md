# Hostile review: Hilbert--Burch repeated-coordinate localization

## Claim under review

The proposed theorem treats only the joint-rank-five, three-root
Hilbert--Burch `(1,1,1)` profile.  If two of its three rank-one triangle
factors equal one target-coordinate line `e_s`, it proves that the remaining
factor has zero `e_s` coordinate.  It therefore excludes the all-same-
coordinate triangle but does not exclude the residual complementary-plane
boundary or the complete `(1,1,1)` atlas.

Global status remains **UNRESOLVED**.

## Adversarial questions

### 1. Is the Hilbert--Burch normal form being assumed beyond S2AG?

No.  S2AG proves that every three-root joint-rank-five point has derivative
rank seven, that its two-dimensional derivative kernel lies in `K=image H`,
and that the `(1,1,1)` profile can be normalized as
`span((x,0,z),(0,y,z))`.  Its signed minors are exactly the three blocks in
equation (2).  The new theorem starts only after that proved reduction.

### 2. Does "two equal coordinate factors" survive root permutation?

Yes.  The three signed minors and the permanent equation are symmetric under
permutation of the three roots.  After such a permutation, the repeated pair
can be written `x=lambda e_s`, `y=mu e_s`, with `lambda mu!=0`; the remaining
factor is `z`.  The proof retains these scalars, and no target-colour
permutation changes the assertion `z_s=0`.

### 3. Why are all corrections zero on the displayed `2 x 2 x 3` grid?

For `x=lambda e_s`, `y=mu e_s`, every derivative tensor is a scalar-weighted
sum of `a tensor e_s tensor z`, `e_s tensor b tensor z`, and
`e_s tensor e_s tensor c`.  If the first two root colours both differ from
`s`, every summand has zero coefficient, for every third-root colour.  Since
the singleton correction plane is `D_B(K)`, the complete physical equation
on those rows is the bare all-cross permanent equal to the GHZ target.  This
is coefficientwise and uses all third-root rows.

### 4. Why does `z_s!=0` produce two independent contractions?

The restriction of a covector in `z^perp` to the complementary coordinate
plane `span(e_u,e_v)` is an isomorphism exactly when `z_s!=0`.  Explicitly,
the covectors with restrictions `(1,0)` and `(0,1)` have `e_s` coefficients
`-z_u/z_s` and `-z_v/z_s`.  The determinant of the corresponding coordinate
test is `z_s`.  Thus the two contracted rows exist uniquely and retain the
two diagonal target coefficients independently.

### 5. Could one of the six binary-frame rows be zero or dependent?

No.  If, for example, `r_u,r_v` were dependent, compare the diagonal entry
`per(r_u,p_u,q'_u)=T_u` with the crossed zero
`per(r_v,p_u,q'_u)=0`; the dependence coefficient must be zero, after which
the `v` diagonal cannot be nonzero.  The same argument applies to the `p`
and `q'` pairs.  Thus `R,P,Q` really are two-planes.

### 6. Why do the six rows lie in one three-plane?

They arise from root covectors annihilating `ker D_B`.  Because
`ker D_B subset K`, one has `K^perp subset (ker D_B)^perp`.  The kernel of
`H^T` is `K^perp`, so the image of the seven-dimensional annihilator is
`7-4=3` dimensional.  The two non-`s` coordinate rows annihilate the two
kernel generators directly, and each third-root contraction annihilates
their shared factor `z`.  No claim about the full nine-row span is needed.

### 7. Is the binary-frame lemma silently assuming the three two-planes
span the ambient three-plane?

No.  If their combined span has dimension two, all three two-planes agree,
which is the first case of the proof.  Otherwise their span is a
three-plane, and the normal-incidence split is exhaustive.  Enlarging an
ambient three-plane when all three agree changes none of the equal-plane
argument.

### 8. Is the equal-plane matrix orientation correct?

Yes.  With `p_b=sum_i L_(b,i)r_i`, the permanent matrix is `F=S L^T`, where
`S` is symmetric.  Hence `L F=L S L^T` is symmetric.  The two target
coefficient matrices are `E_00` and `E_11`; symmetry of `L E_00` kills
`L_10`, and symmetry of `L E_11` kills `L_01`.  Thus `L` is diagonal, not
transposed diagonal.  Both checkers replay this column orientation.

### 9. Does the inherited square lemma apply to a two-plane rather than a
three-plane?

Yes.  The cited S2AL lemma was proved specifically for a two-plane `Q` and
exhausts both the two-source and three-source support of a row whose square
has rank one.  Here `Q=span(q'_u,q'_v)` is exactly a two-plane.  The diagonal
relation matrix produces two rank-one squares, the crossed entry produces
their zero mixed polarization, and the two GHZ tensors are fully transverse.

### 10. Are the three normal-incidence kernels complete?

Yes.  After the equal-plane case is removed, the plane normals are either
independent or three distinct points of one projective line.  In coordinates
their restriction kernels are respectively
`span(A^3,B^3,C^3)` and
`span(A^3,B^3,AB(A+B))`.  These follow by comparing the eight ordered basis
entries of `R^* tensor P^* tensor Q^*`.  The primary and independent scripts
compute the kernels from separate exact matrices.  The repeated-normal
kernel is also replayed as a check on the equal-plane boundary.

### 11. Why does a shared quadratic make two diagonal cubics proportional?

A diagonal ternary cubic with all three coefficients nonzero is smooth, so
it cannot split into three lines.  A nonpure split diagonal cubic is
therefore binary.  Any noncoordinate line factor of
`a A^3+b B^3` fixes the ratio `a:b` by its cube, so another diagonal cubic
sharing that factor is proportional.  In the pure case a repeated common
factor forces both cubics to be the same pure cube.  The proof uses a shared
quadratic, which is stronger than needed in the nonpure case.

### 12. Does the distinct-pencil argument assume every source coordinate
form is nonzero?

No.  It applies only to a nonzero form under consideration.  The two target
products guarantee nonzero `0` and `1` forms in each source, so they can be
used as the other two factors.  A nonzero product in
`S^3 span(A,B)` cannot have a linear factor outside `span(A,B)` by unique
factorization.  Zero coordinate forms already lie in that plane.  Hence all
nine coordinate forms lie there, contradicting that they separate the
points of the embedded three-space `V`.

### 13. Is the conclusion at `z_s=0` an exclusion or a witness claim?

Neither.  At `z_s=0`, the restriction `z^perp -> span(e_u,e_v)^*` drops to
rank one, so the two independent contractions used by the proof do not
exist.  The theorem records this as the remaining exact boundary.  It does
not assert that the boundary satisfies the other target equations or that a
physical graph realizes it.

### 14. What do the scripts prove and not prove?

The primary verifier replays the symbolic Hilbert--Burch derivative, its
kernel and untouched grid, the contraction determinant, the three
polarization kernels, the diagonal-divisor ratio, the equal-plane matrix,
and representative square-atlas charts.  The independent audit imports no
repository or third-party module and reconstructs those calculations using
`Fraction`, a row-oriented tensor representation, and separate elimination.
Neither script replaces the arbitrary-field unique-factorization argument,
the smoothness argument for a ternary diagonal cubic, or S2AG's upstream
Hilbert--Burch exhaustion.

## Verdict

The proof supports the exact repeated-coordinate localization
`x=lambda e_s, y=mu e_s => z_s=0` for nonzero `lambda,mu` and excludes the
all-same-coordinate `(1,1,1)` triangle.
The complementary-plane and coordinate-distinct `(1,1,1)` boundaries, the
other Hilbert--Burch profiles, lower joint ranks, other physical branches,
higher orders, and the global Krenn--Gu conjecture remain open.
