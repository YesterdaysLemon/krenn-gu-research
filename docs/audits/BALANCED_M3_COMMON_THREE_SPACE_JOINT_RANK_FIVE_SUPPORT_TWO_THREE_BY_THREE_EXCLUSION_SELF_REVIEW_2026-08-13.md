# Hostile self-review: rank-five support-two (3,3) exclusion

## Verdict

**PASS at the stated local scope.**  The package excludes the complete
transverse joint-rank-five support-two (3,3) involved-row profile for a
normalized, target-consistent physical m=3 common-shore full sensor.  It does
not exclude support one, a Hilbert--Burch coordinate atlas, joint rank at most
four, another physical component, a higher order, the all-rank-drop branch, or
the global conjecture.  Global Krenn--Gu remains **UNRESOLVED**.

Reviewed artifacts:

- the owning written theorem;
- its SymPy primary verifier;
- its standard-library Fraction no-import audit;
- the S2AG graph and row-space localization;
- the S2AI two-plane common-zero atlas and singleton determinant; and
- the S2AJ support-contraction conventions.

## Adversarial claim inventory

1. Rank-three involved projections make the relation plane the graph of an
   invertible map L.
2. The two support-contracted diagonal targets force
   L e_0=alpha e_1 and
   L e_1=-(beta/chi)e_0+(nu/chi)e_1, with all displayed scalars nonzero.
3. Contracting the complete target equation by the third-row kernel gives
   S_0=-(eta_0/beta)T_0, S_2=0, and a two-term S_1 in
   span(T_0,T_1).
4. Coefficientwise permanent symmetry applies to L F_c, not to F_c itself.
   Its T_2 coefficient at c=2 forces the third graph column to be ell e_2.
5. The complete target table then gives a rank-one T_2 square and puts the
   three required mixed polarized maps in the binary diagonal plane D_01.
6. D_01 has zero intersection with every structural subspace used in the
   two- and three-source square charts because T_0,T_1 differ from T_2 in all
   three source factor lines.
7. The S2AI common-zero atlas remains exhaustive after replacing one
   transverse correction line by D_01.  Only the fully conjugate two-source
   chart uses the mutual correction condition, and there both displayed
   tensors lie in the fixed-factor space x tensor y tensor Z, which still
   intersects D_01 trivially.
8. The resulting zero alternating separated tensor contradicts the generic
   determinant of the three physical singleton columns.
9. No entry of either root--root block outside the inherited support
   contractions is assumed monomial, rank one, separable, tangent, generic,
   or invertible.

## Hostile questions

### Does the colour-zero target really force L e_0 onto e_1?

Yes.  A preimage a of e_0 tensor e_0 in

~~~text
beta a tensor e_0+chi e_1 tensor L a
~~~

has no e_2 component after projection in the first factor, and its e_0
coefficient can be normalized to one.  Thus a=e_0+t e_1.  The already forced
identity

~~~text
L e_1=-(beta/chi)e_0+(nu/chi)e_1
~~~

makes the e_0 terms cancel in the e_1 first-factor row, leaving
L e_0=-(t nu/chi)e_1.  Invertibility rules out t=0, so alpha is nonzero.
The primary verifier checks both diagonal preimages with six independent
nonzero scalar symbols; the independent audit checks a separate rational
specialization.

### Were the correction tensors inferred from only selected rows?

No.  Equation (17) in the theorem is the full eta contraction for all nine
first-two-root row pairs.  Rows (0,0), (2,0), and (1,1) solve S_0,S_2,S_1,
and the remaining six rows replay as exact identities.  Both computational
routes check all nine.  The conclusion is plane containment, not an
unsupported claim that every correction is one pure tensor.

### Is the permanent-symmetry matrix orientation correct?

Yes.  With

~~~text
p_b=sum_i L_(b,i)r_i
~~~

and the symmetric matrix S_c(a,i)=M_(r_a,r_i)(q_c), one has

~~~text
F_c=S_c L^T,
L F_c=L S_c L^T.
~~~

Therefore L F_c is symmetric.  The T_2 coefficient of F_2 is E_(2,2), so
L E_(2,2) is symmetric.  The provisional entries L_(0,2),L_(1,2) are exactly
its two upper skew entries and must vanish.  The verifier checks this symbolic
orientation directly; the no-import audit reconstructs the sparse product
with row tuples.

### Could a hidden T_2 singleton correction contaminate the symmetry step?

No.  The kernel contraction gives S_0,S_1 in D_01 and S_2=0.  Hence every
singleton correction has zero T_2 coefficient.  The only T_2 coefficient in
the c=2 fibre is the physical target at root pair (2,2), so the coefficient
matrix is exactly E_(2,2).

### Does the target table discard arbitrary entries of B or C?

No.  Once the graph and correction tensors are fixed, the table is evaluated
with all eighteen entries of B and C independent.  At root pair (2,2), the
rows L_(2,0)=L_(2,1)=0 and S_2=0 remove every correction regardless of those
entries.  At pairs (0,2), (1,2), and (0,0), arbitrary block entries only
multiply S_0 or S_1 and therefore stay inside D_01.  The primary verifier
uses eighteen unrelated SymPy symbols; the audit uses an unrelated dense
rational pair of blocks.

### Why do D_01-valued mixed products vanish against the T_2 square?

For a two-source repeated row v=x+y, every mixed value lies in

~~~text
x tensor Y tensor Z + X tensor y tensor Z,
~~~

where x,y are the first two factor lines of T_2.  For a three-source v, the
decomposable rank-one square shares two base factor lines; quotienting the
square identity forces every q in Q to use those same two lines, giving the
same structural sum.  The binary diagonal plane generated by T_0,T_1 has
zero intersection with this sum because both generators use different X and
Y coordinate lines.  This is a subspace statement, so cancellation between
T_0 and T_1 cannot evade it.  The primary replay checks ranks 15 and 17; the
independent audit rebuilds the basis and repeats the same rank calculation.

### Was the old line-valued S2AI lemma silently overgeneralized?

No.  The proof reopens every place where S2AI used the correction line.
The first use was only to show a mixed product cannot meet the structural
sum; D_01 has the same zero-intersection property.  In the fully conjugate
chart, both mutual products lie in x tensor y tensor Z; D_01 again has zero
intersection.  The other two-source charts and every three-source chart use
only common-zero equations, V intersect Q=0, or the scaling determinant.
They do not use one-dimensionality of the correction space.

### Does characteristic zero enter honestly?

Yes.  The fully conjugate chart uses the nonzero scalar 2 in the polarized
and alternating identities.  All other divisions are by scalars already
proved nonzero.  The theorem is stated over characteristic zero and makes no
claim in characteristic two.

### Why must the alternating separated tensor be nonzero?

The graph basis u_i=D_(B,C)(e_i,L e_i) is a basis of U because the transverse
derivative is injective on P.  The three separately linear physical singleton
columns have coefficient row forms r_0,r_1,r_2 in that basis.  Their generic
determinant is exactly A_XYZ(r_0,r_1,r_2).  A full four-column sensor requires
the three singleton columns to be independent, so this determinant is
nonzero.  This argument does not use a monomial block.

### Did the tempting proportional-slice argument prove too much?

No.  Initial exploration showed that q_0 and q_1 proportionality alone is
exactly absorbed by the corrections in (18); it gives no contradiction in
the (3,3) profile.  The written proof does not use that failed inference.
It instead uses the T_2 coefficientwise symmetry and the complete two-plane
target table.  The old local sharpness control remains valid and is not
misreported as physical.

### Is the independent audit genuinely independent?

Yes.  The primary route uses SymPy matrices, Kronecker products, symbolic
blocks, and nullspaces.  The audit imports no repository file and no
third-party library.  It uses flat tuples of standard-library Fraction
values, hand-written Gaussian elimination, direct six-permutation loops, a
different dense block fixture, and basis exhaustion for the structural
subspaces.

## Stop boundary

The proved conjunction is

~~~text
normalized target-consistent physical m=3 common-three-space full sensor
+ dim U=3
+ rank H=5
+ transverse two-root derivative of rank six
+ third-row rank two with support-two kernel
+ involved row ranks (3,3).
~~~

It closes only the final support-two involved-row profile.  Support one, the
three Hilbert--Burch coordinate atlases, joint rank at most four, other
component and pole strata, every higher order, the all-rank-drop branch, and
global Krenn--Gu remain open.  No global status change is authorized by this
checkpoint.
