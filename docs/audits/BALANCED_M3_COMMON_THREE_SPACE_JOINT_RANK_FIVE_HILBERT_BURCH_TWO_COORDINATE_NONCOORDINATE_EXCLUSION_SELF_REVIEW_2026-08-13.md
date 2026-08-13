# Self-review: Hilbert--Burch two-coordinate/noncoordinate exclusion

Date: 2026-08-13

Claim under review:

[`BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_TWO_COORDINATE_NONCOORDINATE_EXCLUSION_THEOREM.md`](../../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_TWO_COORDINATE_NONCOORDINATE_EXCLUSION_THEOREM.md)

Global status after this claim: **UNRESOLVED**.

## Scope and adversarial questions

### 1. Does this theorem assume that two Hilbert--Burch factors are coordinate vectors without proving a cover?

No.  S2AG proves the exact beta-zero coordinate-boundary condition for the
`(1,1,1)` profile: at least two of `x,y,z` are target-coordinate vectors.
Root and colour permutations put a distinct pair in the displayed
`x=lambda e_0`, `y=mu e_1` chart.  S2AN--S2AP already exclude a repeated
coordinate line, and S2AQ already excludes a third distinct coordinate
line.  Thus a genuinely noncoordinate `z` is the complete remaining
`(1,1,1)` chart, not a sampled subcase.

### 2. Is "noncoordinate" silently strengthened to full support?

No.  The proof only uses that `z` has support at least two.  The primary and
independent replays separately cover support patterns `110`, `101`, `011`,
and `111`.  In particular, no `z_i` is assumed nonzero unless the proof
explicitly chooses one nonzero coordinate of the nonzero vector `z`.

### 3. Why are all three coordinate restrictions on `z^perp` nonzero?

For a coordinate functional `ell_i`, the inclusion
`z^perp subset ker ell_i` between two planes is equality.  Taking
annihilators then makes `z` proportional to `e_i`, contrary to the chart.
Thus each exterior target face is genuinely nonzero even when one
coordinate of `z` itself vanishes.

### 4. Is `Q=q(z^perp)` really a two-plane?

Yes.  The `T_2` core face detects every direction with `gamma_2!=0`.  Any
remaining kernel direction has `gamma_2=0`.  If `q(gamma)=0`, then
`gamma` annihilates every third component of `K`; together with
`gamma(z)=0`, contraction kills all of `D_B(K)`.  It also kills the
all-cross term, while the target contraction
`gamma_0 T_0+gamma_1 T_1` is nonzero.  This contradiction proves
injectivity on the second direction.  Both replays reconstruct this gate
independently.

### 5. Does torus recovery miss an exceptional divisor?

No.  A free-coordinate point of the seven-dimensional annihilator yields
fully supported factors only when its seven free coordinates and
`gamma(z)` are all nonzero.  The proof therefore uses eight hyperplanes,
not the seven from the coordinate-triangle chart.  On their complement,
the exact identity is

```text
D_B^T(alpha tensor beta tensor gamma)=gamma(z)^2 ell.
```

S2R excludes such a point in `N=K^perp`.  The finite-union lemma over the
infinite characteristic-zero field then places all of `N` in one of the
eight hyperplanes.

### 6. What replaces a coloop for the extra hyperplane `gamma(z)=0`?

The six-plane `L intersect {gamma(z)=0}` contains `N`, so its image under
`H^T` has dimension `6-4=2`.  It contains the preimages of `R` and `P`, and
for `gamma in z^perp` its gamma direction maps exactly to `q(gamma)`.
Therefore it contains `Q` as well.  Since all three are already
two-planes, `R=P=Q`.  No choice of a basis-dependent "eighth coloop" is
needed.

### 7. Is the `R=P` radical alignment valid in different row bases?

Yes.  Fix `gamma in z^perp` with `gamma_2!=0`.  The core face is a nonzero
rank-one bilinear form on the common plane.  Its left radical is
`span(r_1)` and its right radical is `span(p_0)`.  Permanent symmetry makes
the form symmetric on that plane, so left and right radicals agree.  The
primary replay checks the equivalent change-of-basis matrix identity; the
independent audit checks it by separate rational elimination.

### 8. Is the square-zero mixed-factor lemma exhaustive?

Yes.  It splits the nonzero common vector `v` by the number of active source
components.

- A pure `v` fixes that source factor in every mixed value.
- For two active sources, square-zero forces the third projection of `Q` to
  vanish; both mixed maps use the same `X tensor Y` factor map.
- For three active sources, `Q` is the exact two-dimensional square kernel.
  Every mixed value lies in one Segre tangent space, and a decomposable
  tensor in that tangent shares at least two base factors.

These cases exhaust `v`, and both replays use direct permanent expansion
with different tensor-index conventions.

### 9. Does `P=Q` really give the square tables used in the ordinary-coloop split?

Yes.  The `A` face and the `r_2` core face become symmetric rank-one
bilinear forms on the common plane, with images `T_0` and `T_2`.  The
`r_1` core table is zero.  The `B` face gives a nonzero `T_1`-valued map
with `r_1` and a zero map with `r_2`.  These are full plane tables because
`(p_0,p_2)` and `q(z^perp)` are both bases of the same plane.

### 10. Are the raw `q_k=h_k+z_k(A+B)` substitutions valid when some `z_k=0`?

Yes.  The identity is coefficientwise for every `k`.  Each ordinary-coloop
argument chooses any one index with `z_k!=0`; such an index exists because
`z` is nonzero.  No division by all three coordinates is made.

### 11. Is the final use of the S2AL tangent-line lemma circular or outside its scope?

No.  S2AL is an upstream theorem about the permanent map on arbitrary
subspaces of `X direct-sum Y direct-sum Z`.  In the `r_1`-coloop case, choose
`s` outside the kernel line of the `T_0` square and the kernel line of the
`T_1` mixed map.  On the one-dimensional subspace `span(A)`, the maps

```text
per(s,s,-),          per(s,r_1,-)
```

are nonzero rank-one maps onto `T_0,T_1`.  This is exactly Part 2 of the
S2AL lemma.  Its conclusion that the images share a source factor
contradicts their full transversality.  The use is pointwise and requires no
transfer from a larger row plane.

### 12. Are the first/third equality cases actually covered?

Yes.  Exchange the first two roots and the corresponding nonroot source
factors, then exchange target colours `0,1`.  This preserves the normalized
chart, swaps `z_0,z_1`, and interchanges `P=Q` with `R=Q`.  Noncoordinate
support and full transversality are invariant.

### 13. Does the verifier prove the theorem by itself?

No.  The Markdown argument is the proof.  The primary verifier replays the
symbolic identities and all support charts.  The no-import audit uses
standard-library rational arithmetic, a different tensor convention,
separate row reduction, and direct permanent expansion.  They guard the
load-bearing algebra but are not presented as an exhaustive solver over
all possible `H`.

### 14. What frontier changes, and what remains open?

Only the joint-rank-five Hilbert--Burch `(1,1,1)` profile closes.  The
`(1,1,2)` and `(1,2,2)` Hilbert--Burch profiles remain open, as do joint rank
at most four, other physical component and pole strata, higher orders, and
the global conjecture.  This is not a resolution audit and does not change
the repository's global **UNRESOLVED** status.

## Review conclusion

The exact support cover, eight-hyperplane torus fork, plane-equality
reductions, and both factor-sharing uses survive the adversarial checks
above.  The claim is appropriately scoped as a verified exclusion of the
last `(1,1,1)` Hilbert--Burch chart, with independent exact replay and no
global-status promotion.
