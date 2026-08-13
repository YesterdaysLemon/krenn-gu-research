# Self-review: `(1,1,2)` double-repeated outer intersection exclusion

Date: 2026-08-13

Reviewed claim:

[`BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_DOUBLE_REPEATED_OUTER_INTERSECTION_EXCLUSION_THEOREM.md`](../../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_DOUBLE_REPEATED_OUTER_INTERSECTION_EXCLUSION_THEOREM.md)

## Review outcome

The claim is accepted as an exact characteristic-zero subcase exclusion.
It excludes the simultaneous double-repeated intersection in the
distinct-colour central coordinate-pair chart of the Hilbert--Burch
`(1,1,2)` profile.  Together with S2AS--S2AV, it closes that chart, but not
the same-colour central chart, an outer coordinate-pair chart, every
`(1,1,2)` boundary, or any broader frontier.  Global status remains
`UNRESOLVED`.

The proof was reviewed as a new boundary argument.  Neither exterior target
face used by the predecessor theorems survives on this intersection.  The
new load-bearing inputs are the rank-one square/radical dimension bound,
the fact that `q_u=h_u` belongs to both spaces in the third-colour coloop,
and the full coefficientwise correction map in the central-colour coloop.

## Scope audit

The theorem assumes:

```text
characteristic zero;
normalized target-consistent physical m=3 common-three-space full sensor;
dim U=3;
rank H=5;
Hilbert--Burch projection profile (1,1,2);
s,t,u pairwise distinct;
x=lambda e_s, y=mu e_t;
z=nu e_t, w=xi e_s;
lambda mu nu xi nonzero.
```

The last line is exactly the simultaneous intersection omitted by S2AV.
No step treats a same-colour chart or infers an outer coordinate-pair chart
from the central one.

## Derivative, quotient, and torus audit

Direct substitution of both kernel generators in

```text
D_B(a,b,c)
 =-mu nu a tensor e_t tensor e_t
  -lambda xi e_s tensor b tensor e_s
  +lambda mu e_s tensor e_t tensor c
```

gives zero.  The derivative has rank seven and annihilator equations

```text
lambda alpha_s+nu gamma_t=0,
mu beta_t+xi gamma_s=0.
```

Substitution in the transpose gives the scalar-general identity

```text
D_B^T(alpha tensor beta tensor gamma)
 =nu xi gamma_s gamma_t(alpha,beta,gamma).
```

Thus there are seven distinct torus factors, not nine: the two repeated
outer evaluations duplicate `gamma_t` and `gamma_s`.  The finite-union step
uses only that the characteristic-zero field is infinite and never divides
by either recovery factor.

The proof of `dim Q=3` was checked separately.  The classes of `r_s,p_t`
give quotient rank two because the full row image has dimension five while
`V` has dimension three.  The row `q_u=h_u` cannot vanish: otherwise
third-root `e_u^*` contraction kills both the all-cross permanent and
`D_B(K)`, but not the target `T_u` coefficient.  This argument uses the
complete physical target identity, not genericity.

## Combined-row alternatives

If a combined row is a coloop, deletion leaves a two-dimensional image
containing both two-planes `R,P`; hence `R=P`.  The untouched table then
aligns `p_s` with the radical `r_t` and converts the `T_u` map into a
rank-one square on the complementary row.

The new square-radical lemma was checked in all source-support cases:

- full support gives a square kernel of dimension two;
- two-source support either leaves a one-dimensional mixed kernel or
  removes the third source and kills the square;
- pure support puts the radical solutions in
  `X direct-sum span(d_Y-d_Z)`.  A rank-one square sees only a
  one-dimensional projection to `X`, while the projection kernel is also
  one-dimensional, so the alleged three-plane has dimension at most two.

This excludes all three combined-row choices without an exterior target.

## Third-colour coloop audit

For `alpha_u=0`, the untouched table has a common radical in `S`, one
complete zero row against the external coloop, and the rank-one `T_u` core.
The full- and two-source radical cases give the same dimension/rank
contradictions as the predecessor common-radical atlas.  In the only
remaining pure-source normal form,

```text
S=span(x,d_Y+d_Z),
Q subset X direct-sum span(d_Y-d_Z),
ell is the coefficient of d_Y-d_Z.
```

Characteristic zero is used when comparing the plus and minus components:
every vector of `S intersect Q` has `ell=0`.  But the double-repeated row
identity gives `q_u=h_u in S intersect Q` and `ell(q_u)=1`.  This is an
immediate contradiction.  First/second-root symmetry covers `beta_u`.

## Central-colour coloop and correction audit

For `alpha_t=0`, the complete zero rectangle has the only viable source
atlas

```text
p=x+y,
S,Q subset E=span(x-y) direct-sum Z.
```

Writing every vector as `c(x-y)+z`, the permanent is exactly

```text
-2 x tensor y tensor
 (c_1 c_2 z_3+c_1 c_3 z_2+c_2 c_3 z_1).
```

The zero map has a three-dimensional kernel only in two ways.  If the
kernel is the complete `Z` source, the alleged core has rank zero or three.
Otherwise the zero map is identically zero.  The latter alternative forces

```text
r_u proportional to p_s proportional to a pure Z vector,
ker ell=Q intersect Z,
T_u in span(x tensor y tensor z).
```

The coefficientwise correction step was audited from first principles.
Pulling `G_N-J in Target tensor U` back through
`D_B:K/ker D_B -> U` gives a linear map `Phi` on `V`.  Comparing all seven
support coefficients produces the exact scalings

```text
mu nu Phi(r_i)=delta_(i,t)T_t-per(r_i,p_t,q_t),
lambda xi Phi(p_j)=delta_(j,s)T_s-per(r_s,p_j,q_s),
lambda mu Phi(h_k)=per(r_s,p_t,q_k).
```

No sign or nonzero scalar was discarded.  Since `q_s,q_t` span
`ker ell`, the rows `r_s,p_t` also lie in `E`.  Linearity of `Phi` along
`p_s proportional r_u` then puts `T_s` in
`span(x) tensor span(y) tensor Z`.  It shares two factor lines with `T_u`,
contrary to target transversality.  Root symmetry covers `beta_s`.

## Computational evidence audit

The primary SymPy replay checks:

- the scalar-general derivative, rank, kernel, annihilator, recovery scalar,
  and seven distinct torus coordinates;
- all seven coefficientwise correction scalings;
- the full/two/pure square-radical rank bounds;
- the common-radical sum/difference normal form and intersection;
- the complete scalar-`Z` permanent formula, rank-one zero-rectangle model,
  and fixed two-factor target subspace.

The independent audit imports no repository code and no third-party
package.  It uses `Fraction`, reverse-flat tensor storage, its own permanent
and alternating implementations, and separate Gaussian elimination.  It
reconstructs the derivative/recovery identities and all canonical rank
models independently.

The scripts replay exact identities and rank calculations.  The finite
union argument, arbitrary-vector source atlases, physical interpretation of
`Alt`, and root symmetry remain mathematical arguments in the theorem.

## Status boundary

Accepted consequence:

```text
distinct-colour central (1,1,2), nonrepeated:       IMPOSSIBLE (S2AU)
distinct-colour central (1,1,2), one repeated:      IMPOSSIBLE (S2AV)
distinct-colour central (1,1,2), double repeated:   IMPOSSIBLE (this claim)

same-colour central and outer coordinate charts:    OPEN
other (1,1,2), (1,2,2), lower ranks, other branches,
and higher orders:                                  OPEN
global Krenn--Gu:                                   UNRESOLVED
```

No exact counterexample was found.  This subcase closure does not trigger a
dedicated global resolution audit.
