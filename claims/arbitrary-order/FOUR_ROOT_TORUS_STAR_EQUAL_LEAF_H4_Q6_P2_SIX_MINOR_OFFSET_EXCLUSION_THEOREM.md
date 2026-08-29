# Four-root torus-star equal-leaf H4 Q6 p=2 six-minor offset exclusion (GLD97)

## Status and exact scope

**Proved exact scoped characteristic-zero theorem (GLD97).**  In the normalized
scale-fixed equal-leaf H4 chart, specialize the GLD88/GLD96 coordinates to
'p=2', retain 'a' as a free parameter, and write the two GLD88 center offsets
as

~~~text
b = b88(2,q,a) + B,
c = c88(2,q,a) + C.
~~~

Let 'M(G)' be the fixed 37-by-9 GLD71 syndrome evaluated at this full
offset point.  On the displayed characteristic-zero 'Q6' fibre and the
denominator-safe open 'D(Delta_2)', every geometric point for which
'rank M(G) <= 6' has

~~~text
B = C = 0.
~~~

Consequently, after the exact GLD75/GLD86 incidence bridge, the p=2 H4/Q6
rank-at-most-six incidence is empty on the determinant-safe chart

~~~text
D(Omega Delta_2).
~~~

Here 'Delta_2' is the p=2 specialization of the GLD88/GLD95 denominator
product and 'Omega' is the frame/gauge gate.  This is a statement about one
normalized equal-leaf chart and one p=2 fibre.  It is not a global
Krenn--Gu resolution; the global conjecture remains **UNRESOLVED**.

On `D(Delta_2)`, the offset change is an affine translation in the two free
leaf coordinates:

~~~text
B = b - b88(2,q,a),
C = c - c88(2,q,a).
~~~

It is therefore a bijection for arbitrary original `b,c` in this normalized
chart; no pivot, minor, or rank equation is imposed in defining `B,C`.
Thus the result covers the whole normalized p=2 H4/Q6 fibre on the declared
open, including the old `P6=0` portion where the written F88 formulas remain
defined.  It does not cover a different gauge or scale chart.

The implication is deliberately stated from the full syndrome rank
condition.  It does not claim that an arbitrary raw GLD83 response/Fitting
point has already been proved equivalent to this normalized offset chart,
nor that every H4 point has rank at most six without the upstream incidence
argument.

The primary exact verifier is
`claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_p2_six_minor_offset_exclusion.py`.
It reconstructs the canonical GLD71 syndrome and GLD88 family, checks the
six raw determinants and all `111` F88 kernel identities, and proves the
rank-only ideal statement without an `R31` generator.  A separate direct
sparse-support/Bareiss implementation provides the independent exact audit.

## 1. Coordinates and determinant-safe gates

Use the GLD96 scale-fixed leaf

~~~text
G = [1  1       1      ]
    [2  q       s      ],
    [a  1+b     1+c    ],

s = (2-q)/(q+1).
~~~

This is the p=2 specialization of the H4 relation
'pq+ps+qs-p-q-s=0'.  The GLD88 family is the written rational family in
the offset chart, with 'b88' and 'c88' having the denominators displayed in
GLD95.  At p=2, the factors used by GLD95 specialize to

~~~text
d0 = q+1,
P  = 3,
L1 = 3q,
L2 = q^2+2q-2,
e  = 3q(q-2),

Delta_2 = (2-q)(q+1)P L1 L2 e
        = -27 q^2 (q-2)^2 (q+1)(q^2+2q-2).
~~~

Thus 'D(Delta_2)' makes the displayed leaf and F88 offsets defined and
keeps the GLD95 denominator factors units.  The center/frame gate is not
replaced by this product:

~~~text
Omega = delta_gauge det(C_phys) det(G)^3,
~~~

with 'delta_gauge=1' in the normalized chart.  In particular, after the
offset forcing reaches the F88 origin `B=C=0`, the specialized GLD95 leaf
determinant still has the factor
'-3a+p+1 = 3(1-a)' in its numerator.  Any such determinant zero, or any
center determinant zero, lies outside 'D(Omega)' and is not silently
retained as a physical point.

The q-boundary polynomial is

~~~text
Q2(q) := Q6(2,q)
      = 5q^4 - 4q^3 + 12q^2 - 16q + 8.
~~~

The constant leading coefficient '5' is a unit in characteristic zero.
Moreover, the p=2 factors in 'Delta_2' are not being inverted merely
because 'Q2=0': 'Q2' is nonzero at 'q=0,2,-1', and its gcd with
'q^2+2q-2' is one.  The exact quotient routine therefore treats
denominator checks separately from the 'Q2' equation.  It aborts if a
q-, a-, B-, or C-dependent denominator survives the reduction, rather than
silently localizing the claimed ideal; see the focused primary verifier and
its independent audit.
Thus the Q2 fibre itself does not lie in a Delta_2 factor; the explicit
'D(Delta_2)' gate is retained to state the chart domain and the inherited
downstream theorem exactly.

## 2. Raw syndrome minors and supports

All row and column lists below are zero-based indices in the full GLD71
37-by-9 syndrome.  The four bordered minors are the raw rational
determinants already used by GLD96; their primitive denominator-cleared
representatives are polynomial:

~~~text
T0 = det M[(0,1,2,17,25,31,28), (0,1,3,4,6,7,8)],
T1 = det M[(0,1,2,17,25,31,32), (0,1,3,4,6,7,2)],
T2 = det M[(0,1,2,17,25,31,32), (0,1,3,4,6,7,5)],
T3 = det M[(0,1,2,17,25,31,33), (0,1,3,4,6,7,8)].
~~~

These supports are pinned in
'claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_R31_GENERIC_RESULTANT_EXCLUSION_THEOREM.md:66-86'.
Although their row sets contain the old GLD96 R31 pivot rows, these are
seven-by-seven determinants.  Their vanishing is a raw rank condition; it
does not require the six-by-six R31 determinant to be nonzero.

The two additional direct seven-minors are

~~~text
D0 = det M[(1,17,28,0,25,31,32), (0,1,2,3,4,5,6)],
D2 = det M[(1,17,28,0,31,32,3), (0,1,2,3,4,5,6)].
~~~

They use only the first seven syndrome columns, so they are direct
rank-seven controls independent of the ninth column used by T0 and T3.
The p=2 primary records exactly these supports in its canonical `MINORS`
table and computes both as direct determinants; the independent audit uses
the same row/column selections with a different determinant implementation.

For the ideal calculation below, the same symbols 'T_i,D_j' denote the
primitive, denominator-cleared polynomial representatives after substituting
'p=2' and reducing q-coefficients modulo 'Q2'.  The clearing is only by
declared parameter-independent constants and by the already declared chart
denominators.  No B or C factor is divided out.  More precisely, the exact
Q2-coprime denominator checks and quotient reduction prove

~~~text
V(Q2, raw T0, raw T1, raw T2, raw T3, raw D0, raw D2)
  intersect D(Delta_2)
= V(J) intersect D(Delta_2),
~~~

where `J` is defined in Section 3.  Reduction modulo `Q2` is used only on
`V(Q2)`; no equality of vanishing loci away from that fibre is asserted.

The self-contained audit records the unreduced raw denominator factors as

~~~text
T0: q(q+1)^3,   T1: q^2(q+1)^2,
T2: q^2(q+1)^3, T3: q(q+1)^2,
D0: (q+1)^6,   D2: (q+1)^6.
~~~

These are all among the p=2 chart gates in 'Delta_2'.  Their exact
denominator and numerator-hash assertions are pinned in
'claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_p2_six_minor_offset_exclusion.py:152-174'.

## 3. The p=2 six-minor ideal

Work in

~~~text
R = Q[a,q,B,C]
~~~

with grevlex variable order '(B,C,q,a)', and define

~~~text
J = (Q2, T0, T1, T2, T3, D0, D2) in R.
~~~

The exact p=2 symbolic-'a' calculation gives the grevlex basis

~~~text
GrevlexBasis(J) = [Q2/5, B, C],

Q2/5 = q^4 - (4/5)q^3 + (12/5)q^2 - (16/5)q + 8/5.
~~~

The order in the displayed list is immaterial; the content is the ideal
equality

~~~text
J = (Q2/5, B, C).
~~~

There is no equation on 'a'.  In particular, this is not the result of
specializing the old double-pivot residuals to 'a=0' or 'a=2'; it is a
single exact calculation over the whole p=2 fibre.

### Theorem 3.1 (p=2 offset forcing)

Let 'P' be a geometric point over an algebraic closure of 'Q' in the
displayed p=2 offset chart and 'D(Delta_2)'.  If

~~~text
Q2(P)=0
and
rank M(G)(P) <= 6,
~~~

then

~~~text
B(P)=C(P)=0.
~~~

#### Proof

Rank at most six makes every seven-by-seven minor of the full syndrome zero.
In particular, the four raw T-minors and the two raw direct D-minors vanish.
Together with `Q2(P)=0`, the raw/reduced vanishing equality in Section 2
places 'P' in 'V(J)'.  The displayed exact basis of 'J' then gives
'B(P)=C(P)=0'.  No R31 equation is used.  'square'

This is a necessary-condition certificate, not a claim that the six
displayed minors generate the full rank-six determinantal ideal.  Their
purpose is sufficient: the displayed subset already has the stated
vanishing consequence.

## 4. Upstream incidence bridge and downstream F88 exclusion

The upstream bridge is the exact GLD75/GLD86 statement on the normalized
equal-leaf chart:

~~~text
B_inc = 0  iff  M(G) C_center = 0,
rank(A_lin) = rank(M(G)[:,0:8]),
C_center,8 = 1.
~~~

Here 'B_inc' denotes the equal-leaf incidence ideal, not the offset
coordinate 'B'; `C_center` is the vectorization of the physical 3-by-3
center matrix `C_phys`, not the offset 'C'.  GLD86 proves this center-column rank equality from the
bidirectional polynomial certificate; see
'claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_RANK_AT_MOST_SIX_SYNDROME_BOUNDARY_CONTAINMENT_THEOREM.md:63-85'
and ':148-173'.  Because the last center coordinate equals one,
`M(G) C_center=0` also gives

~~~text
M(G)[:,8] = -sum_{j<8} C_center,j M(G)[:,j].
~~~

Hence the ninth syndrome column lies in the span of the first eight, so a
true point of 'B_inc intersect V(I_7(A_lin))' supplies the full-syndrome
rank-at-most-six hypothesis of Theorem 3.1.  The raw-minor ideal is therefore
a legitimate necessary-condition consumer of that bridge.  Here `A_lin`
denotes the GLD86 linear coefficient matrix, to distinguish it from the
physical center matrix used in `Omega`.

The output 'B=C=0' identifies the written GLD88/GLD95 F88 family.  GLD92
closes the dense two-six-minor portion and retains an explicit finite
common-minor residual.  GLD95 then closes that finite residual on the full
declared `D(Delta)` open, including the old-`P6=0` content fibres.  The exact
GLD88 block kernel makes every otherwise surviving rank-six center singular.
Thus

~~~text
B_inc intersect V(I_7(A_lin)) intersect F88 intersect V(Q2)
  intersect D(Omega Delta_2) = empty
~~~

for this p=2 specialization.  The relevant all-factor F88 exclusion and
its bridge are recorded in
'claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_FINITE_COMMON_MINOR_EXCLUSION_THEOREM.md:49-84'
and ':91-124'; GLD92 supplies only the dense portion and its explicit
retained residual ledger at
'claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_BOUNDARY_DENSE_MINOR_EXCLUSION_THEOREM.md:103-136'
and ':259-271'.

This downstream step is conditional on the already stated GLD75/GLD86
bridge and the GLD92/GLD95 F88 theorem.  GLD97 does not turn a Fitting-open
calculation into an incidence equivalence.

## 5. Why this does not hide an R31, E31, or g0 localization

The strengthened GLD96 generic resultant proof uses the open
'D(E31 H2 g0 Delta)'.  Its polynomial bordered-determinant identity does not
invert 'R31', so that theorem already includes 'R31=0' wherever the remaining
gates are nonzero.  It still leaves the exceptional resultant factors outside
its scope; see
'claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_R31_GENERIC_RESULTANT_EXCLUSION_THEOREM.md'.
GLD97 is a p=2 calculation with a different logical shape:

1. 'R31' is not a generator of 'J', and no inverse of 'R31' is used.
   The producer's four residual expressions are formed by the polynomial
   adjugate identity

   ~~~text
   R31 * M[row,column] - (pivot-row/column cross term),
   ~~~

   which is the bordered seven-minor itself.  This is cross-multiplication,
   not division.  The primary's exact basis input is visibly
   `[Q2/5,T0,T1,T2,T3,D0,D2]`, with no `R31` generator.

2. 'E31' and 'g0' are not defined or inverted in the p=2 ideal.  They are
   generic coefficient/resultant devices used to select a unit coefficient
   in GLD96; the direct D-minors replace that need on this fibre.

3. 'H2=2p^2-2p+1' specializes to the constant '5', so the generic H2
   exceptional fibre is absent in characteristic zero at p=2.  The
   determinant-safe domain is still 'D(Omega Delta_2)', not all of affine
   parameter space.

Thus R31 may vanish at a point covered by Theorem 3.1.  The theorem does
not assert that 'E31' or 'g0' are globally nonzero, nor does it replace the
generic GLD96 localization for p different from 2.

The former selected-minor/double-pivot residuals at 'a=0' and 'a=2' are
hostile controls, not assumptions of GLD97.  A selected system containing
'R28,R31' can leave those residual fibres; the exact full-syndrome D0/D2
checks are chosen direct rank-seven counterchecks for them.  If a
selected residual survives while either D-minor is nonzero, it is a
spurious selected-minor solution, not a rank-at-most-six point.  If the
actual leaf or center determinant gate is zero, it is instead outside
'D(Omega)'.  The global ideal calculation makes neither branch part of
the theorem's hypothesis.

## 6. Parent-attempt significance

This is intended as the serious parent-theorem attempt required before a
third sibling refinement:

* GLD86 supplies the upstream rank-at-most-six boundary, but leaves H4.
* GLD96 supplies four bordered-minor forcing after the generic E31, H2, and
  g0 localizations, without an R31 gate.
* GLD92 and GLD95 close the Q6 common-minor residual after the F88 family
  has been reached.
* GLD97 combines the bordered T-minors with two additional direct raw
  seven-minors D0 and D2.  The resulting p=2 ideal forces the F88 offsets
  without imposing E31 or g0, so it directly tests their exceptional fibres
  and selected-minor false positives.

The proof-topology delta is therefore a p=2 closure of the H4/Q6
rank-at-most-six route inside the full written F88-offset coordinate
ambient space.  It is not a new arbitrary-H4-to-F88 equivalence and it
does not close the GLD83 response/Fitting branch.

## 7. Explicit nonclaims and retained obligations

GLD97 does not claim:

* any p different from 2, or a theorem over the full Q6 curve in '(p,q)';
* coverage of a different gauge, scale chart, root profile, unequal-leaf
  component, source branch, survivor component, or order;
* that every arbitrary H4 point on 'Q6=0' lies in F88;
* that the GLD83 raw response/Fitting incidence is equivalent to the
  normalized syndrome rank condition used here;
* a pullback, saturation, or computation of the intrinsic GLD83 Fitting
  ideal 'I_Pl';
* validity on 'Delta_2=0' or 'Omega=0';
* a global replacement for the GLD96 'E31,H2,g0' generic argument; or
* a counterexample, a numerical result, or a resolution of the
  Krenn--Gu conjecture.

The upstream gap is precise.  GLD83 retains the raw moving response
columns, rank drops of its constant block, and the full Fitting residual;
its Fitting-open exclusion is sufficient but is not an incidence
equivalence.  See
'claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_SURVIVOR_BORDERED_PLUCKER_FITTING_OPEN_NONEXTENSION_THEOREM.md:82-124'
and ':262-368'.  A future parent closure still needs either an exact
raw-to-normalized-chart specialization/cover or a direct pulled-back
Fitting/incidence certificate.  GLD97 supplies neither.

The global status remains **UNRESOLVED**.

## 8. Reproduction and independent audit

Run both exact replays from the repository root, preferably through
`tools/research/run_bounded.py` with a `300`-second wall bound and a
`12288`-MB aggregate memory bound:

~~~text
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_p2_six_minor_offset_exclusion.py
python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_p2_six_minor_offset_exclusion.py
~~~

The primary imports the committed GLD71 and GLD88 constructors, rebuilds the
full `37 x 9` syndrome, checks all `111` F88 block-kernel identities, forms
`T0,...,T3` by the exact adjugate/Schur determinant identity, forms `D0,D2`
as direct determinants, and checks the raw and reduced hashes plus the exact
grevlex basis.  It passed in `92.080` seconds on the reference run.

The independent audit imports no project builder or verifier.  It copies the
ten required sparse supports as immutable input, accumulates syndrome entries
directly, and evaluates all six determinants with a local fraction-free
Bareiss routine.  It separately checks the raw denominator and numerator
hashes, the Q2/Delta gates, and the same exact polynomial-ring basis.  It
passed in `67.197` seconds.  A separate read-only source comparison matched
all ten copied supports to committed GLD71 and matched the written F88 and Q6
formulae to their canonical sources.  Both runs used CPython `3.13.14` and
SymPy `1.14.0` on the reference host.

Both routes pin the six reduced-polynomial hashes and the basis hash

~~~text
da8b07d04dfb0dbc9935345320722fb21f9e711bb9166f82db9fb23b0f7f585f.
~~~

The hostile scope and provenance review is
`docs/audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_P2_SIX_MINOR_OFFSET_EXCLUSION_REVIEW_2026-08-29.md`.

Exact recomputation of the grevlex basis and zero remainders for `B,C`
certifies ideal membership.  Giant standalone multiplier expressions are
not used as evidence.  A separate generic-p reconnaissance exhausted its
`1800`-second bound without output and is classified as inconclusive; it is
not part of GLD97.

The GLD83 raw/Fitting bridge is not a prerequisite for this scoped theorem.
It remains a nonblocking parent-extension obligation for reaching the
broader raw response/Fitting survivor route.  This theorem does not alter
the global status, which is **UNRESOLVED**.
