# Hostile review: torus-star survivor-locus symmetry and local-germ reduction

Date: 2026-08-26

## Verdict

**Accept as an exact local survivor-germ theorem and a sharp correction to the
proposed symmetry route.**  At the `GLD72` Gaussian point, the fixed `GLD70`
survivor scheme is smooth of dimension five.  The identity component of the
local-basis stabilizer of the complete rank-`44` nuisance space consists only
of factor scalars and moves the tensor in one dimension.  Four genuine local
survivor parameters therefore remain after interface-preserving scaling.

The integration claim is supported by an explicit bidirectional ideal
certificate for a closed equal-leaf subincidence, not by tangent equality.
That subincidence is smooth of dimension five and must equal the full
survivor germ in the displayed frame gauge.

Do **not** accept this as first-response exclusion on a neighborhood or on all
of the survivor locus.  No parametric lift of the `GLD74` unit identities, no
exceptional polynomial `delta`, no component cover, and no source-interface
bridge has been proved.  The global conjecture remains **UNRESOLVED**.

Reviewed artifacts:

- [`FOUR_ROOT_TORUS_STAR_SURVIVOR_LOCUS_SYMMETRY_AND_LOCAL_GERM_REDUCTION_THEOREM.md`](../../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_SURVIVOR_LOCUS_SYMMETRY_AND_LOCAL_GERM_REDUCTION_THEOREM.md);
- [`verify_four_root_torus_star_survivor_locus_symmetry_and_local_germ_reduction.py`](../../claims/arbitrary-order/verify_four_root_torus_star_survivor_locus_symmetry_and_local_germ_reduction.py);
- [`audit_four_root_torus_star_survivor_locus_symmetry_and_local_germ_reduction.py`](../../claims/arbitrary-order/audit_four_root_torus_star_survivor_locus_symmetry_and_local_germ_reduction.py);
- [`generate_four_root_torus_star_survivor_locus_symmetry_and_local_germ_certificates.py`](../../claims/arbitrary-order/generate_four_root_torus_star_survivor_locus_symmetry_and_local_germ_certificates.py);
- [`four_root_torus_star_survivor_locus_symmetry_and_local_germ_certificates.json`](../../claims/arbitrary-order/four_root_torus_star_survivor_locus_symmetry_and_local_germ_certificates.json);
- the [`GLD74` full-fibre theorem](../../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_GAUSSIAN_SURVIVOR_FULL_COEFFICIENT_FIBRE_FIRST_RESPONSE_NONEXTENSION_THEOREM.md).

## 1. Claim and scope boundary

The accepted assertions are exactly:

```text
rank b=44,
dim Lie Stab_GL(3)^4(N_star)=4,
Lie Stab_GL(3)^4(N_star)=four factor scalars,
dim T_(T_0)(Stab(N_star) T_0)=1,
dim(N_star intersect T_(T_0)GHZ_3)=5,
the framed survivor germ at T_0 is smooth of dimension 5,
the full and equal-leaf framed germs agree locally.                 (1)
```

The conclusion is local over `C` at `T_0`.  It does not classify all finite
components of the stabilizer, all irreducible components of the survivor
locus, or any first-response incidence away from the basepoint.

## 2. Stabilizer calculation

Both implementations reconstruct all `79` raw columns and choose an exact
`44`-column basis.  For every one of the `36` infinitesimal matrix units in
`gl_3^4`, the action on all basis tensors is reduced by a `37`-row
annihilator.  The constraint system has rank `32`.  Its kernel is checked to
equal, rather than merely contain, the four factor-identity directions.

The factor-scalar torus is visibly contained in the stabilizer, so equality
of dimensions proves its equality with the identity component.  Its tensor
orbit is the overall scaling line.  Six root-coordinate permutations and six
leaf-mode permutations are separately checked against the complete nuisance
space.  The theorem correctly calls these a verified discrete subgroup and
does not infer a complete finite-component classification.

Pre-normalization root-diagonal and residual gauges do not create an
unrecorded tangent direction.  Any induced continuous local tensor action
that preserves the fixed canonical interface would lie in the already
computed stabilizer.  Frame rescalings stabilizing `Delta_4` are separately
accounted for as a nine-dimensional kernel of the frame-to-tensor map.

## 3. Tangent calculation and frame ambiguity

The exact infinitesimal `GL_3^4` action on `T_0` has rank `27` and kernel
dimension `9`, matching the dimension of the concise GHZ orbit and its
column-scaling stabilizer.  Applying the `37` nuisance annihilators gives a
constraint kernel whose tensor image has rank `5`.

The chosen local frame slice sets all nine entries in the first rows of the
three leaf frames to one.  This is valid only on the explicit open where
those entries are nonzero; that open contains `T_0`.  Its `27` variables have
`37` nuisance-incidence equations with Jacobian rank `22`.  Thus the slice
reproduces the five-dimensional tensor tangent without silently treating a
GHZ decomposition as globally unique.  Finite colour permutations remain
possible but do not affect the local calculation.

## 4. Tangent equality is not used as transitivity

The equal-leaf slice has `15` shifted variables and `37` displayed incidence
generators.  The certificate stores ten alternative generators and two
sparse transformation matrices.  The portable replays verify both

```text
g=fP,                              f=gQ,                         (2)
```

over `Q(i)`.  Hence this is equality of ideals, not equality of zero sets at
sampled points.  The ten-generator Jacobian has rank `10`, giving a smooth
five-dimensional closed germ.

The full incidence contains that germ and has tangent dimension five.  Its
local dimension is therefore exactly five and its local ring is regular,
hence a domain.  A closed subgerm of the same dimension has height-zero ideal,
which must vanish in this domain.  This proves equality of the germs.  The
argument supplies the geometric step that tangent equality alone would not.

The free implicit-function coordinates are

```text
x6, x8, x12, x13, x14.                                      (3)
```

They exhibit five integrated directions; quotienting the one-dimensional
scalar orbit leaves four.  This rules out an open `H.T_0` orbit and any finite
family of such orbits in a neighborhood.

## 5. Certificate provenance and independence

The canonical LF-serialized certificate is `15040` bytes with SHA-256

```text
05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57.
```

It contains `27` forward and `63` reverse multiplier terms.  The primary
route uses the live theorem implementations and SymPy.  The isolated audit
imports no repository or third-party module.  It separately implements
Gaussian-rational arithmetic, permanent construction, exact elimination,
local actions, Jacobians, and sparse-polynomial multiplication.  Both replay
every identity in (2) and independently recover the stabilizer and tangent
ranks.  Singular is optional and used only by the producer to regenerate the
proof object.

## 6. Hostile attacks and rejected strengthenings

### 6.1 The GLD72 survivor was accidentally excluded

Rejected.  Both routes reconstruct its exact frames, nonzero determinants,
and membership in `N_star`.  It is the origin of the certified local germ.

### 6.2 Nonzero epsilon was treated as GHZ membership

Rejected.  The calculation uses the full `37`-equation annihilator of the
fixed nuisance space and the exact invertible frames.  The `GLD70` `Q`
generator plays no inferential role.

### 6.3 Equal tangent spaces were called equal components

Rejected.  Bidirectional ideal identities prove that the equal-leaf
subincidence is a smooth five-dimensional germ.  Regular-local dimension then
proves equality with the full germ.  No global component exhaustiveness is
claimed.

### 6.4 The complete interface stabilizer was inferred from abstract GHZ
symmetry

Rejected.  Every local infinitesimal generator is tested on a complete basis
of the actual `44`-space, and every stated discrete physical symmetry is
tested on all `79` columns.  The finite component group is deliberately left
unclassified.

### 6.5 The frame gauge discarded a divisor from a global theorem

Rejected.  The result is explicitly local at a point where the gauge product
is one.  No response minor, determinant, support coordinate, or survivor
chart is inverted to claim global coverage.

### 6.6 GLD74 now holds on the survivor germ

Rejected as unsupported.  The `GLD74` quotient and sparse unit identities
have only been proved at `T_0` across its full `35`-dimensional raw fibre.
The new four transverse survivor parameters enter both `b alpha=T(F)` and
`D_q0(alpha)L=R(F)`.  A parametric syzygy/Fitting calculation or an exact
divisor cover is still required.

### 6.7 An unfinished exact lift is evidence against the theorem

Rejected.  The bounded attempts at unchanged-multiplier lifting and a
rank-seven Schur expansion did not finish.  A timeout is neither a failed
identity nor evidence of existence.  No claim depends on those attempts.

## 7. Accepted frontier delta

Relative to `GLD74`:

1. symmetry compression is exactly ruled out near `T_0`;
2. the survivor locus has a smooth five-dimensional local germ there;
3. after tensor scaling, exactly four transverse survivor parameters remain;
4. in the displayed frame gauge the three leaf frames may be taken equal
   throughout that germ;
5. the next local parent computation has four survivor parameters plus the
   complete `35`-dimensional raw fibre and must retain all response-rank
   drops;
6. whole-locus response nonextension, a principal-open `delta`, exceptional
   divisors, other components, and source-interface globalization remain
   open.

This is meaningful parent-level progress and a route correction, not closure
of the parent first-response proposition.
