# Self-review: `(1,1,2)` repeated-outer-factor divisor exclusion

Date: 2026-08-13

Reviewed claim:

[`BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_REPEATED_OUTER_FACTOR_DIVISOR_EXCLUSION_THEOREM.md`](../../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_REPEATED_OUTER_FACTOR_DIVISOR_EXCLUSION_THEOREM.md)

## Review outcome

The claim is accepted as an exact characteristic-zero subcase exclusion.
It excludes a distinct-colour central `(1,1,2)` chart when exactly one of
the two outer factors repeats its opposite central coordinate.  First/second
root symmetry covers the mate divisor.  It does not exclude the simultaneous
double-repeated intersection, and it does not change the global
`UNRESOLVED` status.

The load-bearing advance is not a specialization of S2AS away from its
stated divisor.  The old `T_s` face vanishes identically here.  The new proof
uses the surviving `T_t` face, the untouched `T_u` core, and the nonzero
alternating separated tensor forced by physical full-sensor rank.

## Scope audit

The theorem assumes all of the following:

```text
characteristic zero;
normalized target-consistent physical m=3 common-three-space full sensor;
dim U=3;
rank H=5;
all three root-root blocks nonzero;
Hilbert--Burch projection profile (1,1,2);
s,t,u pairwise distinct;
x=lambda e_s, y=mu e_t;
w=nu e_s;
z,w independent;
z not proportional to e_t.
```

Independence of `z,w` is written as `z not proportional to e_s`.  The
additional condition `z not proportional to e_t` removes the simultaneous
double-repeated intersection.  The symmetric statement exchanges roots one
and two, `z,w`, and colours `s,t`.

No step assumes that `z` is generic, fully supported, or noncoordinate.  In
particular, `z proportional e_u` is included.  In that subcase
`gamma(z)=0` duplicates one coordinate hyperplane in the torus cover; the
finite-union argument remains valid with fewer distinct hyperplanes.

## Derivative and torus-recovery audit

For

```text
ker D_B=span((lambda e_s,0,z),(0,mu e_t,nu e_s)),
```

the reviewed derivative is

```text
D_B(a,b,c)
 =-mu a tensor e_t tensor z
  -lambda nu e_s tensor b tensor e_s
  +lambda mu e_s tensor e_t tensor c.
```

Both displayed kernel vectors were substituted directly.  Its annihilator
has equations

```text
lambda alpha_s+gamma(z)=0,
mu beta_t+nu gamma_s=0.
```

Substitution in the exact transpose gives

```text
D_B^T(alpha tensor beta tensor gamma)
 =nu gamma(z)gamma_s(alpha,beta,gamma).
```

The scalar `nu` is nonzero and harmless.  No division by `gamma(z)` or
`gamma_s` is made on their zero divisors.

The root torus on this annihilator is controlled by four ordinary root-row
coordinates, three third-root coordinates, and `gamma(z)`.  The old
`gamma(w)` factor is exactly the already listed `gamma_s`; it was not
double-counted as a new geometric condition.

## Equal-plane fork audit

Every combined-third-row or recovery-factor hyperplane leaves a
six-dimensional source with the four-dimensional relation kernel, so its
image is two-dimensional and contains both row planes `R,P`.  This proves
`R=P`; it does not assume equality from a filename or from generic rank.

When `R=P`, symmetry aligns the radical lines `r_t,p_s`.  The complete
untouched table supplies

```text
per(v,S,Q)=0,
per(d,d,q_u)=T_u.
```

The surviving exterior face supplies `per(B,v,q_*)=T_t`.  The new lemma was
checked in all source-support cases:

- full support puts `Q` in the two-dimensional square kernel and the mixed
  zero then makes the complementary row proportional to `v`;
- two-source support either confines `Q` to one line or kills the core;
- pure support gives conjugate `Y,Z` projections, so the core fixes both
  factor lines and every decomposable exterior value lies on one of those
  two tangent rulings.

Thus the equal-plane fork is excluded with `T_t,T_u` alone.  No missing
`T_s` equation is used.

## Coloop-rank and full-sensor audit

Deleting any torus-forced coloop row leaves six rows with the same
four-dimensional relation kernel, hence a two-plane `S`.  The third-row
image has dimension three, not merely at least two:

- the quotient classes of `A,B` give two directions because `z,e_s` are
  independent;
- the common normal `n in z^perp intersect e_s^perp` gives a nonzero row in
  `S`; otherwise the complete physical target contraction by `n` would
  vanish on the left and remain nonzero on the GHZ target.

The full-sensor determinant was also audited.  Since `D_B|K` has kernel
exactly the two-dimensional derivative kernel, it identifies `K/ker D_B`
with `U`.  The three singleton columns are generically independent because
the complete sensor has rank four.  In a basis of the dual three-plane
`V=H^T(L)`, their determinant is the alternating separated tensor `Alt`.
Therefore `Alt!=0`; this is a physical rank consequence, not an extra
genericity hypothesis.

## First-root coloop audit

For `alpha_t=0`, the one-sided S2AU source-support lemma applies after the
surviving `T_t` face is upgraded to a square.  Review confirmed that its
proof after the square setup uses only the complete zero row, `dim Q=3`,
the nonzero `T_u` core, and transversality.  The old condition
`w not proportional e_s` was needed only to obtain the root-symmetric
`T_s` orientation; it is not used in this one-sided application.

For `alpha_u=0`, the S2AT square argument again makes `r_t` pure.  The two
end cases were rechecked without `T_s`:

- when the conjugating functional is nonzero, the untouched `T_u` core
  lies in the two-ruling tangent space and shares a factor with `T_t`;
- when it is zero, `p_s,p_u` are nonzero pure vectors in one source, while
  the two untouched entries say `p_s tensor M=0` and
  `p_u tensor M=T_u!=0`, an immediate contradiction.

## Second-root coloop audit

The two new abstract lemmas were reviewed independently.

### Common-radical orientation

For `beta_u=0`, the untouched table gives a common radical `p_s`, a zero
`r_t x p_u x Q` row, and the rank-one `T_u` core.  Splitting the radical by
source support gives:

- full support: square-kernel dimension two, impossible for `dim Q=3`;
- two sources: either a one-dimensional tangent kernel or a complete pure
  source on which the alleged rank-one core has rank three;
- one source: full-sensor alternation forces both complementary source
  components.  Exact coefficient comparison yields the canonical signs
  `p_Y=c d_Y`, `p_Z=-c d_Z`, the core line
  `x tensor d_Y tensor d_Z`, and an exterior Segre tangent in the last two
  factors.

Every decomposable exterior value therefore shares `d_Y` or `d_Z` with
`T_u`, contradicting `T_t`.

### Complete-zero-rectangle orientation

For `beta_s=0`, the coloop row `p_s` annihilates the complete rectangle
`S x Q`.  The exact rank atlases were checked by direct block expansion:

```text
p pure:       the full-sensor minor forces Q to the same pure source;

p=x+y:        dim ker(q |-> per(p,s,q))>=3 exactly on
              (X direct-sum Y) union (span(x-y) direct-sum Z);

p=x+y+z:      dim ker(q |-> per(p,s,q))>=3 exactly on
              L_X union L_Y union L_Z,
              L_X=X direct-sum span(y-z), cyclically.
```

The finite-union step is valid over the infinite characteristic-zero field
and puts the whole two-plane `S` in one atlas component.

- The pure case makes the core rank zero or three.
- In the two-source case, nonzero `Alt` selects
  `S,Q subset span(x-y) direct-sum Z`.  The core fixes factor lines `x,y`,
  and any decomposable exterior value in the resulting tangent space shares
  one of them.
- In the full-source case, nonzero `Alt` makes the common kernel exactly one
  complete pure source.  The core again has rank zero or three.

This is exhaustive by source support.  The only surviving atlas is the
two-source tangent, and it contradicts the transverse exterior target.

## Computational evidence audit

The primary verifier uses SymPy and checks:

- scalar-general derivative, kernel, annihilator, and transpose recovery;
- the repeated torus factors and surviving exterior contraction;
- the full/two/pure equal-plane atlas;
- the canonical common-radical normal form and its two tangent rulings;
- the pure/two/full zero-rectangle rank atlases;
- the exact untouched coloop row tables.

The independent audit imports no repository module and no third-party
package.  It uses `Fraction`, a z-major tensor index rather than the
primary Kronecker ordering, separately implemented permanent and alternating
maps, and its own Gaussian elimination.  It reconstructs the derivative,
recovery, rank-eight full-source equal-plane system, common-radical model,
and all zero-rectangle rank representatives.

The scripts replay displayed identities and rank calculations.  The finite
union arguments, arbitrary-vector factor-sharing implications, physical
full-sensor interpretation, and symmetry statement remain mathematical
arguments in the owning theorem.

## Status boundary

Accepted consequence:

```text
distinct-colour central (1,1,2), neither repeated:       IMPOSSIBLE (S2AU)
distinct-colour central (1,1,2), exactly one repeated:   IMPOSSIBLE (this claim)
distinct-colour central (1,1,2), both repeated:          OPEN
global Krenn--Gu:                                        UNRESOLVED
```

No exact counterexample was found.  No dedicated global resolution audit is
triggered by this subcase theorem.
