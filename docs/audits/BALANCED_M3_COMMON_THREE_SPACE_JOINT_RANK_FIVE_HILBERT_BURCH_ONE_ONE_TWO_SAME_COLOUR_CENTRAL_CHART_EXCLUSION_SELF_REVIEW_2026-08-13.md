# Self-review: `(1,1,2)` same-colour central-chart exclusion

Date: 2026-08-13

Reviewed claim:

[`BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_SAME_COLOUR_CENTRAL_CHART_EXCLUSION_THEOREM.md`](../../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_SAME_COLOUR_CENTRAL_CHART_EXCLUSION_THEOREM.md)

## Review outcome

The claim is accepted as an exact characteristic-zero subcase exclusion.
It excludes the complete same-colour central coordinate-pair chart of the
Hilbert--Burch `(1,1,2)` profile.  Together with S2AW it closes both central
charts, but not the genuinely outer coordinate-pair charts or the full
`(1,1,2)` profile.  Global status remains `UNRESOLVED`.

## Scope audit

The theorem assumes:

```text
characteristic zero;
normalized target-consistent physical m=3 common-three-space full sensor;
dim U=3;
rank H=5;
Hilbert--Burch projection profile (1,1,2);
ker D_B=span((lambda e_s,0,z),(0,mu e_s,w));
lambda mu nonzero;
z,w independent.
```

No genericity, coordinate support, or divisor condition is placed on
`z,w`.  Their independence is exactly the profile-two condition in the
third root.  The theorem does not infer either outer coordinate chart from
this central one.

## Imported localization audit

S2AS is used only for facts it proves on the same-colour chart:

- `R=span(r_a,r_b)` and `P=span(p_a,p_b)` are two-planes;
- the complete untouched table is
  `per(r_i,p_j,q(gamma))=delta_(i,j)gamma_iT_i`;
- recovery and finite-union torus avoidance reduce the chart to the four
  ordinary coloops `alpha_a,alpha_b,beta_a,beta_b`.

S2AS's same-colour equal-plane argument does not require the
distinct-colour repeated-line exclusions.  No result from S2AT--S2AW is
silently specialized to this chart.

## Third-row rank and full-sensor audit

The proof needs `dim Q=3`, not merely two.  Modulo `V`, the third rows have
the two independent quotient coordinates `gamma(z),gamma(w)` because
`z,w` are independent and the full row image has rank five.  Their common
normal `n` gives `q(n)=h(n) in V`.  If this row vanished, third-root
contraction by `n` would kill the all-cross permanent and all of `D_B(K)`,
while leaving the nonzero target contraction `sum_i n_iT_i`.  Thus the
third direction is nonzero.

The alternating tensor of `V` is nonzero for the same reason as in S2AV:
`D_B|K` identifies `K/ker D_B` with the three-dimensional singleton span,
and the alternating separated tensor is the generic determinant of the
three singleton columns.  This is a physical full-sensor consequence, not
an added genericity assumption.

## Ordinary-coloop reduction audit

For `alpha_a=0`, deleting `r_a` leaves the second-row plane
`S=P=span(p_a,p_b)` and the row `r_b` inside it.  Writing

```text
r_b=c p_a+d p_b
```

is exhaustive.  The untouched table gives exactly four maps:

```text
M(r_a,p_a)=gamma_aT_a,     M(r_a,p_b)=0,
M(r_b,p_a)=0,              M(r_b,p_b)=gamma_bT_b.
```

When `cd!=0`, bilinearity gives a rank-one square of `r_b` onto `T_b`
and a rank-one mixed map containing `r_b` onto `T_a`.  The cited S2AL
square/mixed tangent lemma applies to an arbitrary subspace `Q` and says
their decomposable images share a source factor.  This contradicts target
transversality.

Target-colour permutation exchanges `a,b`; first/second-root symmetry
exchanges the `alpha` and `beta` pairs.  Therefore checking
`alpha_a` covers all four ordinary coloops.

## Endpoint lemma audit

### Square-zero endpoint

When `d=0`, `r_b` is proportional to `p_a`.  One row has zero square on
the three-plane `Q` and two nonzero rank-one mixed maps onto `T_a,T_b`.
The source-support split is exhaustive:

- a pure row puts its fixed source factor into both targets;
- a full-support row has only a two-dimensional square kernel;
- a two-source row `x+y` puts `Q` in `X direct-sum Y`, where the mixed map
  factors through `L(q)=x tensor q_Y+q_X tensor y`.  This map has only a
  one-dimensional kernel, so its restriction to a three-plane cannot have
  rank one.

Thus this endpoint is impossible.

### Rank-one-square endpoint

When `c=0`, `r_b` is proportional to `p_b`.  Its square has rank one on
`Q`, while the independent rows `r_a,p_a` are both mixed radicals.

- a pure repeated row has zero square;
- for a full-support row, the two-dimensional square kernel lies inside
  `Q`.  Coefficient comparison on that complete scaling kernel makes every
  mixed radical proportional to the repeated row;
- for a two-source repeated row, the rank-one square leaves a
  two-dimensional `Q_0` in the missing-source hyperplane.  The mixed zero
  has only a one-dimensional kernel there unless the radical also misses
  that source.  Both radicals therefore miss it, forcing their alternating
  tensor with the repeated row to vanish.

Both alternatives contradict the nonzero full-sensor alternating tensor.

## Computational evidence audit

The primary SymPy replay checks the scalar-general derivative, kernel,
annihilator, recovery scalar, an exact quotient-rank representative, the
full/two/pure endpoint rank models, and all three coefficient cases.

The independent audit imports no repository module or third-party package.
It uses `Fraction`, reverse-flat tensor storage, an independently written
permanent and alternating map, and separate Gaussian elimination.  It
reconstructs the derivative/recovery and both endpoint atlases.

The scripts replay exact identities and canonical rank calculations.  The
finite-union localization, arbitrary-vector implications, physical
interpretation of `Alt`, and symmetry argument remain mathematical steps in
the owning theorem.

## Status boundary

Accepted consequence:

```text
distinct-colour central (1,1,2):                    IMPOSSIBLE (S2AW)
same-colour central (1,1,2):                        IMPOSSIBLE (this claim)
genuinely outer coordinate charts / other (1,1,2): OPEN
(1,2,2), lower ranks, other branches, higher order: OPEN
global Krenn--Gu:                                   UNRESOLVED
```

No exact counterexample was found.  This chart closure does not trigger a
dedicated global resolution audit.
