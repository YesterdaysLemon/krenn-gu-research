# Self-review of the `(1,1,2)` outer-coordinate-chart exclusion

## Review verdict

The claimed scope is supported: both genuinely outer coordinate-pair charts
of the rank-five Hilbert--Burch `(1,1,2)` atlas are impossible over
characteristic zero.  Together with the already proved central-chart chain,
this excludes the complete `(1,1,2)` profile because S2AG's three Boolean
clauses are equivalent to the presence of one of the three pairs
`(x,y)`, `(x,w)`, `(y,z)`.

This is a scoped characteristic-zero theorem, not a resolution of Krenn--Gu.
The `(1,2,2)` profile, lower joint ranks, other physical component types, and
higher orders remain open.  Global status stays **UNRESOLVED**.

## Scope and provenance questions

### Does the proof assume more than the theorem states?

No.  It uses the normalized target-consistent physical `m=3`
common-three-space full-sensor hypotheses, `dim U=3`, `rank H=5`, all three
root blocks nonzero, and the S2AG `(1,1,2)` Hilbert--Burch normal form.  The
selected outer chart has `x=lambda e_s`, `w=nu e_t`; independence of `z,w`
is exactly `z not parallel e_t`.

The proof temporarily assumes `y` is noncoordinate.  If `y` is coordinate,
then `(x,y)` is a central coordinate pair and S2AX already excludes it.  No
point is discarded.

### Why does closing the outer charts close the whole profile?

S2AG proves the exact clauses

```text
(x coordinate or y coordinate),
(x coordinate or z coordinate),
(y coordinate or w coordinate).
```

Their minimal satisfying sets are exactly `(x,y)`, `(x,w)`, `(y,z)`.
Additional coordinate factors only place a point in more than one of these
charts.  S2AS--S2AX close `(x,y)` and the new theorem closes `(x,w)` and,
by first/second-root symmetry, `(y,z)`.  There is no residual `(1,1,2)`
Boolean pattern.

### Is the symmetry between the two outer pairs exact?

Yes.  Starting from

```text
span{(x,0,z),(0,y,w)},
```

interchange roots one and two and then interchange the two kernel
generators.  The normal form becomes

```text
span{(y,0,w),(0,x,z)}.
```

Thus an original coordinate pair `(y,z)` is the new `(x',w')` pair.  The
projection profile remains `(1,1,2)`, and `z,w` independence is preserved.

## Derivative and torus audit

### Is the derivative correct?

Yes.  Substitution of `x=lambda e_s`, `w=nu e_t` in the Hilbert--Burch
blocks gives

```text
D_B(a,b,c)
 =-a tensor y tensor z
  -lambda nu e_s tensor b tensor e_t
  +lambda e_s tensor y tensor c.
```

Both displayed kernel generators vanish under this map, and the primary and
independent replays compute rank seven on exact samples.

### Is the recovery scalar correct?

Yes.  The annihilator equations are

```text
lambda alpha_s+gamma(z)=0,
beta(y)+nu gamma_t=0.
```

The three components of the transposed derivative become, respectively,

```text
nu gamma(z)gamma_t alpha,
nu gamma(z)gamma_t beta,
nu gamma(z)gamma_t gamma.
```

No division by a possibly vanishing coordinate of `y` occurs.

### Why are there exactly nine torus factors?

For a point of `L`, full target support means the nine ordinary evaluations
`alpha_i,beta_j,gamma_k` are all nonzero.  The first annihilator equation
makes `gamma(z)=-lambda alpha_s`, and `gamma_t` is already one of the third
root coordinate evaluations.  Thus the recovery scalar is nonzero at every
fully supported point.  S2R forbids such a point in `N=K^perp`.  The nine
ordinary coordinate hyperplanes cover `N`, and the infinite-field finite-
union lemma puts `N` in one fixed member.

Each restricted coordinate form is nonzero on `L`; the independent audit
checks this in both `y_s!=0` and `y_s=0` support patterns.

### Does a coordinate hyperplane really give a two-plane of rows?

Yes.  The selected hyperplane in the seven-dimensional `L` has dimension
six and contains the complete four-dimensional kernel `N` of `H^T|L`.
Therefore its image has dimension two.  This is a primal coloop statement,
not an inference from a filename or a generic computation.

## Exterior-face and rank audit

### Why is the binary exterior face exact?

For `alpha_s=0` and `beta(y)=0`, every component of `D_B^T` vanishes.
Contracting the complete target equation, not a quotient or sample, gives

```text
per(r(alpha),p(beta),q(gamma))
 =alpha_a beta_a gamma_aT_a+alpha_b beta_b gamma_bT_b.
```

The two targets are fully transverse.

### Are both row planes really two-dimensional when `y_s=0`?

The first-root plane is injective directly from the exterior face.  For the
second-root plane, the same face says a kernel vector is a multiple of
`e_s^*`.  If `t!=s`, a second exact exterior contraction gives
`per(r_s,p_s,q_s)=T_s`, so `p_s` is nonzero.  If `t=s`, setting `p_s=0`
makes both the all-cross term and every singleton correction miss the
`(s,s,s)` target coefficient.  Thus `p_s` is nonzero there as well.  This
closes the only possible kernel and proves `dim P=2`.

### Why is the third-row image three-dimensional?

Modulo `V`, its two quotient coordinates are `gamma(z)` and `gamma_t`.
They are independent because `z` and `e_t` are independent.  Their common
kernel is one-dimensional.  Its nonzero vector `n` has `q(n) in V`; if that
row vanished, third-root contraction by `n` would kill the all-cross term
and, using `n(c)=0` on `K`, all of `D_B(K)`, but not the diagonal target.
Hence the third row has two quotient directions plus one nonzero direction
in `V`, so its rank is exactly three.

### Is the alternating tensor assumption imported honestly?

Yes.  The restriction `D_B|K` has kernel exactly `ker D_B` and identifies
`K/ker D_B` with the three-dimensional singleton span.  The separated
singleton columns are the three source projections of this quotient map;
their determinant is `Alt(V)`.  Physical full-sensor rank makes it nonzero.
This is the same proved bridge used by S2AV, S2AW, and S2AX.

## Coloop exhaustion audit

### Are all nine orientations treated?

Yes.

- `alpha_s=0` and all three `gamma_k=0` contain both two-planes `R,P` in
  the coloop complement.  The equal-plane binary-face lemma excludes them.
- `alpha_a=0` and `alpha_b=0` are the two first-root coloops.  They are
  handled separately for `y_s!=0` and `y_s=0`.
- All three `beta_j=0` orientations are classified by the support of the
  unique line `y^perp intersect beta_j^perp`: two visible binary coordinates,
  exactly one, or neither.  The three cases are exhaustive.

The counts are `4+2+3=9`.

### Does the generic coefficient fork reuse S2AX within its scope?

Yes.  Whenever restriction of `y^perp` to the two complementary target
coordinates is invertible, the exterior face is literally the S2AX binary
diagonal table after changing the second-root basis.  The proof uses only
permanent symmetry, the rank-three third row, the nonzero alternating tensor,
and full transversality of the two targets.  None depends on the central
derivative beyond producing that table.

### What happens when `y_s=0`?

Then `y_a y_b!=0`.  The visible line in `y^perp` carries both target
coordinates, while `e_s^*` is invisible on the binary face but has a nonzero
row.  Generic coefficients still give the S2AL square/mixed contradiction.
The sole endpoint has a square-zero radical row, a second radical row, and
two transverse mixed targets; Lemma 1 excludes it.

For a second-root coloop, the hyperplane-intersection line can have:

- two visible coordinates, giving the equal-plane fork;
- one visible coordinate, giving the transposed S2AX fork; or
- no visible coordinate, necessarily the nonzero row `p_s` when `y_s=0`.

The last line is a common radical of the whole in-plane row plane, and
Lemma 2 forces the two exterior targets to share a source factor.

## Endpoint-lemma audit

### Is Lemma 1's source split exhaustive?

Yes.  The square-zero row has pure, two-source, or full support.

- Full support has a two-dimensional square kernel and cannot contain the
  three-plane `Q`.
- Two-source support puts `Q` in those two sources; the mixed map containing
  the row has a one-dimensional kernel, hence rank at least two on `Q`.
- For a pure row, the second radical gives an exact sum/difference equation
  on the other two source projections.  Except at the proportional
  sum/difference endpoint, a two-plane of pure-source inputs makes the other
  mixed map have rank at least two.  At that endpoint both rank-one images
  share the two remaining factor lines.

Thus the two images cannot be fully transverse.

### Is Lemma 2's factor-sharing conclusion complete?

Yes.  A full-support radical is impossible.  A two-source radical places
the entire row plane and `Q` in two sources, so every exterior value has the
fixed third factor supplied by the coloop.  A pure radical gives an exact
relation between the other two projections.  In the two-nonzero case,
rank one on the two-plane kernel forces the plus tensor to vanish; the
alternating minus tensor is nonzero and pins both output factor lines.
All source-support cases are covered.

Characteristic zero is used in the finite-union steps and in the nonzero
factor `2` in the sum/difference endpoints.

## Computational and independence audit

The primary SymPy replay checks:

- rank-seven derivative and the two kernel generators;
- the recovery scalar and exterior-face annihilation;
- nine proper torus factors and quotient rank two;
- both support patterns of `y^perp`;
- every coefficient fork; and
- the full/two/pure source atlases of the two endpoint lemmas.

The independent audit imports neither the primary verifier nor SymPy.  It
uses `fractions.Fraction`, a separate Gaussian eliminator, a separately
constructed derivative, independent support-line enumeration, and separate
coefficient/source calculations.  The two scripts therefore do not merely
repeat one implementation under different filenames.

Neither script is the mathematical proof by itself.  They replay the exact
identities and finite source-support atlas used by the written proof.

## Formalization and global status

No Lean formalization is claimed.  The target statement, derivative bridge,
finite-union argument, and permanent source-support lemmas remain informal
mathematics with exact executable audits.

The result closes the complete joint-rank-five Hilbert--Burch `(1,1,2)`
profile.  It does not close `(1,2,2)`, joint rank at most four, the other
common-three-space or pole component types, higher orders, or the global
conjecture.  Krenn--Gu therefore remains **UNRESOLVED**.
