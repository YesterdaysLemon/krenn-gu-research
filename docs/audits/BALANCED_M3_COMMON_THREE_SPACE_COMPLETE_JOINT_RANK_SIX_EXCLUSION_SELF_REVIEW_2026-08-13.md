# Self-review: complete common-three-space joint-rank-six exclusion

Date: 2026-08-13

## Claim boundary

The reviewed theorem closes the coordinate-relation-plane alternative left by
S2AE and therefore completes the exclusion of joint cross rank six on the
normalized, target-consistent physical `m=3` common-three-space stratum.  It
does not exclude joint rank at most five, another S2T/S2Q component type,
higher order, or the all-rank-drop branch.  Global Krenn--Gu remains
`UNRESOLVED`.

## Reconstruction from the owning equations

I reconstructed the proof from `K=image H`, the transverse derivative, and
the coefficientwise empty-permanent target equation.

1. A coordinate relation `L subset {u_s=0}` is exactly the dual statement
   `(e_s,0) in K_12`.
2. Hence the opposite involved row has rank at most two.  Reusing the
   target-kernel argument with its original hypotheses—not the later common
   contraction line—forces rank exactly two, a coordinate kernel `e_d^*`,
   and the diagonal block row `B_(d,-)=kappa e_d`.
3. The other involved row has rank three or two.  No rank-one profile is
   silently discarded: a two-dimensional kernel would contain a support-two
   vector and contradict the same target-kernel argument.
4. In profile `(3,2)`, `K_12` is the graph of a rank-two map `T` with
   `ker T=e_s` and `image T=e_d^perp`.  The zero physical row `p_d` determines
   every coefficient preimage and gives the full identity

   ```text
   G_N=J-kappa^(-1)T_d D(e_d,T e_d).
   ```

5. Permanent symmetry makes every coefficient matrix `F=S T^T`.  If `s=d`,
   the two remaining rows form the already audited symmetric-square
   contradiction.  If `s!=d`, deleting nonroot colour `d` kills the entire
   correction and leaves a binary five-product table.  Its projected third
   row plane still has dimension at least two because the target root-3
   flattening has rank two.
6. In profile `(2,2)`, target absorption forces `d=s`, and the complete
   three-plane is

   ```text
   span{(e_s,0),(0,e_c),(e_j,tau e_j)}.
   ```

   The beta-zero atlas forces one diagonal block to be a coordinate monomial.
   After its target term cancels, one square derivative has one GHZ image
   line.  The other two independent rows would have to be mixed zero
   divisors, unless one maps to a disjoint GHZ line.  The square-pencil lemma
   forbids both possibilities.

## Mistakes and discarded shortcuts

- A finite-field reconnaissance over `F_3` found no binary five-product
  table.  This was used only to choose the proof direction.  It is not in the
  theorem, verifier semantics, or status claim.
- An attempted exhaustive finite-field square-pencils scan timed out.  No
  inference was drawn from the timeout.  The final argument instead computes
  the square kernel exactly by the number of nonzero source components.
- It would be invalid to reuse S2AE's graph isomorphism in profile `(2,2)`.
  The final proof treats that profile separately and obtains its three-plane
  from both projection kernels.
- It would also be invalid to assume projection of `Q` stays
  three-dimensional after deleting a nonroot colour.  The proof needs only
  dimension two and derives that lower bound from the surviving binary target
  flattening.

## Hostile checks of the new lemmas

### Binary five-product lemma

The proof splits `u` into three, two, or one nonzero source components.

- Three components: the square kernel is exactly the two scaling syzygies;
  vanishing of the mixed derivative there makes `v` proportional to `u`, so
  its square also vanishes.
- Two components: the square kernel is the sum of those two sources.  A third
  component of `v` leaves only one mixed-kernel direction, too small for the
  projected plane; without it the square of `v` vanishes.
- One component: the mixed kernel is one whole source plus one conjugate
  line.  A rank-one square restriction fixes a two-plane.  The second mixed
  zero then forces the other diagonal image to share two factor lines with
  the first, contradicting the two coordinate GHZ products.

No support chart or zero component is omitted.

### Square-pencil lemma

- A pure `u` has zero square and is excluded by the nonzero hypothesis.
- For two-source `u`, the square kernel inside `Q` is a two-plane.  The exact
  mixed zero-divisor equation is `v=lambda(x,-y,0)`, so its space is one
  dimensional.  A nonzero rank-one mixed image either shares the square's
  missing-source factor or is a decomposable point of a two-factor Segre
  tangent and shares one of its other factors.
- For full-support `u`, the square kernel consists of two scaling syzygies.
  A decomposable square image lies on one ruling of the Segre tangent.  Two
  mixed evaluations have fixed factor lines from that ruling; asking for a
  line disjoint in all modes forces both evaluations to vanish and hence
  `v` proportional to `u`.  The zero-divisor space is actually zero.

These arguments use `2!=0`; the theorem is characteristic zero.

## Root-block atlas audit

In profile `(2,2)`, S2AD's atlas gives either a coordinate monomial directly
or a block with coordinate image.  The latter cannot retain a noncoordinate
third-root form: its only nonzero endpoint row is the row already proved to
equal `kappa e_s` (or `kappa' e_c`).  Therefore that block is precisely the
matching diagonal coordinate monomial.  No boundary-pencil case is dropped.

## Verification independence

The primary replay uses SymPy and column-oriented tensor matrices.  It checks
both graph charts, the exact 27-entry graph correction, symbolic kernels for
the five-product and square-pencil cases, the two-rank-two relation plane,
and coordinate-image monomial forcing.

The independent audit imports neither SymPy nor repository code.  It uses
`Fraction`, separate row-oriented elimination, and linear maps whose columns
are rebuilt from coordinate probes.  It checks the same ranks, kernels,
factor-support controls, graph correction, and two-rank-two orthogonality by
a different representation.  The arbitrary-subspace and Segre-tangent
statements remain the written proof.

## Remaining obligation

The live common-three-space frontier is now joint rank at most five, along
with the other component types already listed in S2T.  A successor must not
infer that low joint rank is impossible merely from the high-rank sequence;
the codimension-four intersection `K intersect ker D` can be larger and must
be analyzed explicitly.
