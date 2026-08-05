# Findings: equal-support in-out stratum (Task A) and rank-two-dominated strata (Task B)

Exact computations over Q (sympy rationals + Singular factorization /
primary decomposition).  Scripts in `scripts/` (step1..step29, each
self-contained; steps 28-29 were added at integration and are covered
by the addendum at the end of this file); conventions follow
`verify_p4_inout_path_stratum_working_note.py` (rmul, pairing, perm4,
chart reductions, universal Segre incidence).

## TASK A: the equal-support in-out chart

Configuration: relations `u1*y3 = 0`, `y2*u3 = 0` with all four vectors in
the coordinate plane `Pi = span(X2,X3)`:

    u1 = (0,0,1,-1),  y3 = (0,0,1,1),  u3 = (0,0,1,e),  y2 = (0,0,1,-e),
    U1 = span(u1,v),  U2 = span(y2,x),  U3 = span(y3,u3) = Pi   (e != 1).

`Pi` carries the nondegenerate binary form `B(u,w) = u2*w3 + u3*w2`
(zero product of two Pi-vectors = B-conjugacy; isotropics X2, X3), so the
conjugate of any U2-kernel direction exists inside U3 = Pi automatically.

### Proved (steps 1-7)

1. Exactly two covectors survive on U0 (all u1-side and u3-side conditions
   die by associativity): `<z v, y2 y3> = 0`, `<z v, x y3> = 0`.
2. The covector matrix has equal columns 2,3: `u1 in U0` on the whole
   rank-2 stratum.  Pivot(0,1) `= -(e-1)(v2+v3)(v1 x0 - v0 x1)`.
3. Active determinant, (0,1)-chart (Singular):
   `det B = c (e-1)^4 (v2+v3)(v1 x0 - v0 x1)^2 (v0 x1 + v1 x0)^2`.
   The open-chart branch `s := v0 x1 + v1 x0 = 0` forces `U0 = Pi` and
   every tensor entry is an exact multiple of `s`: identically ZERO
   restriction.  No pure point in the open (0,1)-chart.
4. Active determinant, (0,2)-chart (pivot `-v1(e-1)s`):
   `det = c (e-1)^4 v1 (v1 x0 - v0 x1) s^3`.  The unique rank-2-stratum
   branch with nonzero restriction is the W-branch
   `W: v1 x0 - v0 x1 = 0, s != 0`.
5. On W: `U0 = span((v0,-v1,0,0), u1)`; in the shape family with
   `U0 = span((a,b,0,0), u1)` the entries have the closed forms
   `T0011 = (e-1)(a x1 + b x0)`, `T0100 = -(c-1)(a v1 + b v0)`,
   `T0101 = -(c-e)(a v1 + b v0)`,
   `T0110 = (a v1 + b v0)(x2+x3) + (v2+v3)(a x1 + b x0)`,
   `T0111 = (a v1 + b v0)(e x2+x3) + (e v2+v3)(a x1 + b x0)`,
   `T1111 = (e-1) s`; purity with nonzero value forces exactly
   `a v1 + b v0 = 0` and `a x1 + b x0 = 0` (the W-equation), after which
   the restriction is the SINGLE word `(u1-row, v, x, u3)` with value
   `(e-1) s`.
6. Kernels on W: `K0 = (v0,-v1,0,0)`, `K1 = u1`, `K2 = y2`, `K3 = y3`:
   three of the four kernels lie in the one plane `Pi`, and the
   {13}-relation is KERNEL-KERNEL (`u1` spans `K1`), identically on the
   branch.  Invariants at two exact samples: profile `(4,4,3,4,3,3)`
   (star at 3), all rank-one relations, supports all `{2,3}`.
7. Family tangent rank 5 (with full projective torus); universal
   Segre-incidence Jacobian rank 13 (tangent dim 7) at three samples:
   W-points are singular points of the pure locus.

### The new SIX-dimensional family (steps 22-25)

Freeing the Pi-directions of U0, U1, U2 independently exposes the honest
object.  Define

    C10:  U0 = span((v0,-v1,0,0), (0,0,1,-c0)),
          U1 = span((0,0,1,-c1), v),
          U2 = span((0,0,1,-c2), (t v0, t v1, x2, x3)),
          U3 = Pi = span(X2, X3),

with free moduli `(c0, c1, c2, t, v-class 2, x-class 1)` = SIX.  Then
(step22, symbolic over the function field):

- the restriction is pure for ALL parameter values; the only nonzero
  entries in the adapted bases are
  `T1110 = -2 t v0 v1 (c0 - 1)`, `T1111 = -2 t v0 v1 (c0 + 1)`;
- kernels: `K0 = (v0,-v1,0,0)` (the {01}-form conjugate of the direction
  `(v0,v1)` shared by v and x), `K1 = (0,0,1,-c1) = U1 cap Pi`,
  `K2 = (0,0,1,-c2) = U2 cap Pi`, `K3 = (0,0,1,c0)` = the B-conjugate of
  `U0 cap Pi`;
- generic invariants: profile `(4,4,3,4,3,3)` (star at mode 3), all three
  relations rank one with supports ALL EQUAL `{2,3}`, arrows `0 -> 3`,
  `3 -> 1`, `3 -> 2` (indegrees `(1,1,1,0)`), no kernel-kernel relation;
- family tangent rank = 6 exactly (13 parameters incl. full torus);
- the W-branch is the wall `c0 = c1` (there `K3` collides with the
  {13}-relation vector and that relation becomes kernel-kernel);
  C10 is INVARIANT under the mode-(12) swap (v' = x, t' = 1/t reproduce
  the shape and the ties), and the swap exchanges the `c0 = c1` and
  `c0 = c2` walls; the pure-locus tangent is 7-dimensional along ALL of
  C10 (W included), the one extra direction being the obstructed
  U3-deformation below;
- the extra tangent direction deforms U3 off Pi inside the hyperplane
  `H = span((v0,v1,0,0), X2, X3)` with ratio `a3 : b3 = -c0 : 1`
  (steps 24/25), and the purity minors
  `(a3 + b3 c0)(c0+c2)`, `a3^2 (c0+c1)(c0+c2)`, `b3^2 (c0+c1)(c0+c2)`,
  `(a3 + b3 c0)(c0+c1)` show it is SECOND-ORDER OBSTRUCTED for generic
  c's: within the natural 8-parameter shape family the pure locus through
  a generic C10 point is C10 alone.  (Local standard-basis certificate:
  attempted, heavy; open item.  The U3-deformations do integrate on the
  special walls `c1 = c2 = -c0` and `c1 = -c0` / `c2 = -c0`, giving
  further 6-dim crossing sheets - boundary geometry of the same orbit.)

### Census separation of C10

- The only certified six-dimensional component is the seventh, generic
  profile `(4,3,2,4,4,3)` (rank sum 20).  C10 has profile
  `(4,4,3,4,3,3)` (rank sum 21 > 20): rank monotonicity on closures
  excludes containment in the seventh under every mode permutation.
- All other certified components are five-dimensional, so none contains
  the six-dimensional C10.
- The W-branch (5-dim) is separated from every certified component: from
  1st/9th by star-vs-triangle profile shape at equal rank sum; from 7th by
  rank sum; from 2nd by relation-rank pattern; from L1/L2/L3, 6th, 8th
  (same profile `(4,4,3,4,3,3)`) by the kernel-kernel invariant, verified
  at exact generic samples of every family (steps 8, 20; the 8th at the
  Gaussian-rational generic point `(a,b,f,phi) = (2,1,2,i)`).

CONCLUSION (Task A).  The equal-support in-out stratum contains, beyond
identically-zero loci, exactly one new object: the six-parameter family
C10, pure for all parameter values, whose generic point lies in no
certified component closure.  A TENTH pure-compression component orbit
exists; its dimension is six modulo the final local-dimension certificate
(tangent 7 with a second-order obstructed normal direction), and the
W-branch is the five-dimensional kernel-kernel wall `c0 = c1` inside C10
(swapped to `c0 = c2` by the family's mode-(12) symmetry).  Deep strata
of the chart (`s = 0` with
`(v2+v3)(v1x0-v0x1) = 0`, or `v0 = v1 = 0`, or support-degenerate x)
remain to sweep.

> Integration note: this section was written in parallel with the
> certification of the coincident-support component (the census
> "tenth"), so "TENTH" above refers to what the final census numbers
> as the ELEVENTH orbit; the missing local-dimension certificate and
> the C10-versus-coincident-support comparison are both settled in the
> addendum at the end of this file (steps 28 and 29).

## TASK B: rank-two-dominated strata

### Rank-two edge structure (step9)

At a pure point every rank-3 edge relation has kernel-adapted matrix
`((A,B),(C,0))`; rank two means `B, C != 0`.  Gauges: the x-shift kills A;
x-scales normalize `mu = -C/B`: on a STAR all three mu's become 1; on a
TRIANGLE the holonomy `lambda = mu_12 mu_23 / mu_13` is invariant.  After
the gauge a rank-two edge is exactly

    y_i x_j = x_i y_j in R_2
      <=> G = y_i x_j^T - x_i y_j^T has G + G^T diagonal
      <=> q_ij = y_i o x_j - x_i o y_j is a diagonal quadric in Sym^2.

`G` has rank exactly 2 with column space U_i, row space U_j; `q_ij`
vanishes on both perps.  NO coordinate-pair support forcing (the 2nd
component's rank-two edge has full-support mode-0 vectors); the
zero-product support lemma is genuinely rank-one-only.  Diagonal quadrics
vanishing on a generic plane-perp form a line, so two planes joined by a
rank-two edge share ONE diagonal quadric Delta up to scale; all perps of a
rank-two-dominated configuration are isotropic planes of a single Delta
(for rank-4 Delta: points of the two rulings of the smooth quadric).

### The all-rank-two STAR is empty (steps 10-14)

For a star at mode 3 (`y_i x_3 = x_i y_3`, i = 0,1,2) the Sym^2
differences factor uniquely:
`(y_i - y_j, x_i - x_j) = sigma_ij (y_3, x_3)` - all four planes lie in
ONE PENCIL `U(sigma) = span(a + sigma y_3, b + sigma x_3)` (U_3 = the
infinite member), where `(a,b)` spans, with `(y_3,x_3)`, the 2-dim
solution space of the 6 linear equations `y x_3 = x y_3`.  On the pencil
family the restricted tensor depends only on the WEIGHT of the basis word,
`T[bits] = t_{|bits|}`, and each `t_w` is affine-linear in the elementary
symmetric functions of `(sigma_0, sigma_1, sigma_2)`.  Purity of a weight
tensor is the geometric-progression condition on `(t_0..t_4)`; its primary
decomposition over `Q(n2,n3)` is a single linear prime (Singular), and on
that prime `t_0 = ... = t_4 = 0` IDENTICALLY (rank-2 linear system with
augmented rank 2).

THEOREM.  The all-rank-two star stratum with generic centre contains no
nonzero pure restriction.  (Boundary leaves: support-degenerate centres
`n2, n3 in {0,1}, n2 = n3`, jumps of `dim(x_3 R_1 cap y_3 R_1)`, and
coincident planes `U_i = U_3`, where the commutativity relation
`y_3 x_3 - x_3 y_3 = 0` is automatically a rank-two relation.)

### The all-rank-two TRIANGLE reduces to a chord condition (steps 15-18)

For a triangle on modes {1,2,3}: unique factorization of the pairwise
Sym^2 identities forces holonomy `lambda = 1` and
`(y_2, x_2) = (y_1 + y_3, x_1 + x_3)` after gauges: U_1, U_2, U_3 are the
pencil members `sigma = 0, kappa, oo`, U_0 free.  The restricted tensor
depends only on `(bit_0, weight of bits 1..3)`: an effective 2x4 matrix
`N = [[Lambda(p)], [Lambda(q)]]` for a FIXED linear map
`Lambda: C^4 -> C^4`, `U_0 = span(p,q)`, with

    det Lambda = -16 n2^3 n3 (n2-1)(n2-n3)^3 (n3-1)^3
                 (kappa^2 + n2 (n3-1)(n2-n3))^2 .

Away from chart degeneracies purity needs
`kappa^2 = -n2(n3-1)(n2-n3)` (the stratum surface, irreducible), where
ALL 3x3 minors of Lambda vanish identically: rank Lambda = 2.  Purity with
nonzero restriction then needs `U_0 = span(k, w)`, `k in ker Lambda`,
`Lambda(w)` on the twisted-cubic cone `{(c, cr, cr^2, cr^3)}`;
`P(Im Lambda)` is a LINE, and at the rational stratum point
`(n2,n3,kappa) = (2,3,2)` the two section polynomials `r^2 - 3r + 2`,
`r^3 - 9r + 9` share no root (including r = oo): the "chord condition" is
a proper closed condition on the irreducible stratum surface.

CONSEQUENCE.  The generic all-rank-two triangle chart carries nonzero pure
points at most over a proper chord curve, each with finitely many U_0:
with the torus this gives families of dimension <= 4 - walls, not
components.  When the chord condition holds the configuration is genuinely
all-rank-two (relation in true-kernel bases has shape `((0,1),(-1,0))`).

SUMMARY (Task B).  Rank-two-dominated configurations generically support
NO nonzero pure restriction; pure points require either the
codimension-one chord degeneration (triangle; dim <= 4 walls) or
support/coincidence boundary degenerations (star).  This is consistent
with, and explains, the census: every certified component has at most one
rank-two relation among its chosen rank-3 edges.

## Open items

1. Airtight local-dimension certificate at a generic C10 point (Singular
   ds standard basis; char 31991 run launched; char-0 and an independent
   audit remain).  Then a standalone C10 component theorem document in the
   repo style (H31/H22 obstructions, separating invariants, audit).
2. Deep strata of the equal-support chart: (i) `s = 0, v2+v3 = 0`;
   (ii) `s = 0, v1 x0 = v0 x1 = 0` (support-degenerate v or x);
   (iii) `v0 = v1 = 0` (U1 inside Pi) - Grassmannian-moduli treatments.
3. Task B boundary leaves: support-degenerate star centres, coincident
   planes, lower-rank Delta; identification of the triangle chord walls
   inside the census; mixed strata (some rank-one, some rank-two).

## Script index

- step1_chart.py: covectors, identical vanishing, minors.
- step2_activedet.py: (0,1)-chart active determinant + Singular factors.
- step3_branch_zero.py: s = 0 zero-restriction proof; (0,2)-chart det.
- step4_Wbranch.py / step5_W_dimension.py / step21_W_sample2_rank.py:
  W-branch invariants, tangent 5, incidence rank 13 at three samples.
- step6/19/26: local-dimension attempts (incidence and minors forms).
- step7_shape_family.py: shape-family purity closed forms.
- step8_census_invariants.py / step20_more_census.py: census invariant
  table (2nd, L1, L2, L3, 6th, 8th incl. generic Gaussian sample, W).
- step9_ranktwo_structure.py: rank-two edge lemma, gauges, holonomy.
- step10-14: star pencil structure, weight tensor, purity prime, zero
  identity, Delta entries.
- step15-18: triangle pencil, Lambda, det Lambda, rank-2 identity, chord.
- step18b_triangle_chord_fast.py: check-only replay of the chord
  conclusion.  step18's function-field kernel solve exceeded local
  replay budgets (2400 s); step18b replays its symbolic first
  checkpoint (all 3x3 minors of Lambda vanish on the stratum) and
  replaces the solve by exact rational arithmetic at the stratum
  witness `(n2,n3,kappa) = (2,3,2)`: rank exactly two, the recorded
  section pair `{r^2-3r+2, r^3-9r+9}` spans the computed kernel, and
  the span has no common root (resultant 27; no root at `r = oo`).
  Properness of the chord condition needs exactly this witness, so the
  Task B triangle conclusion is fully re-verified (about three
  minutes).  step17's exploratory tail (the per-root `U_0` census over
  the irrational cubic roots) can hit a sympy `RecursionError` in some
  environments; its two decisive checkpoints — rank two at the witness
  and the recorded covector pair `[[2,-3,1,0],[9,-9,0,1]]` — replay
  green first and are independently covered by step18b.
- step22-25: C10 six-fold (purity for all parameters, invariants, tangent
  6, incidence 13, extra direction, obstruction minors).
- step27_swap_invariance.py: C10 is invariant under the mode-(12) swap
  with `(v,x,t,c1,c2) -> (x,v,1/t,c2,c1)`.
- step28_localdim_slice_char0.py, step29_c10_tenth_distinctness.py:
  integration addendum below.

## Addendum (integration pass, same day): C10 is an ELEVENTH component

Two certificates added while merging this snapshot settle both open
ends of Task A's conclusion.

**Local dimension (step28, exact, characteristic zero).**  Slicing the
eleven ratio-eliminated purity equations at the generic C10 sample by
six fixed rational linear forms through the point and computing a `ds`
standard basis in char 0 gives sliced local dimension ZERO.  By Krull's
height bound this is valid for ANY six forms, so the purity variety has
local dimension at most six at the sample; the family tangent has exact
rank six there (step23, including the full projective source torus),
so the local dimension is EXACTLY six and `closure(C10)` is an
irreducible component of the pure locus.  Its generic points are
singular points of that locus (incidence tangent seven everywhere along
C10) — the first certified component whose certificate is a local
standard-basis dimension count rather than a smooth incidence point.

**Distinctness from the coincident-support tenth (step29, exact).**
Let S be the closed set of plane 4-tuples having at least one
coordinate 2-plane among their four planes.  S is stable under every
census symmetry (mode permutations, source-coordinate permutations,
diagonal source torus, in-plane basis changes).  Every C10 point has
`U_3 = span(e_2,e_3)`, so `closure(C10)` lies inside S; the tenth
component's certificate point `(b,e,k,m,r) = (2,3,5,7,11)` has NO
coordinate plane (verified entry-wise, after re-grounding that point as
the certified pure tuple).  Hence `closure(C10) != g(tenth)` for every
census symmetry g.  Dimension six excludes the eight fivefolds and the
ninth; rank monotonicity (C10 rank-profile sum 21 > 20, replayed)
excludes the seventh.

**Conclusion.**  `closure(C10)` is a six-dimensional irreducible
pure-compression component lying in no previously certified component
orbit: the ELEVENTH component orbit.  The certified census lower bound
is now eleven.  (step26's FULL local standard basis is heavy: the
char-31991 run hits its 480 s Singular cap — recorded null; the char-0
slice above is the certificate precisely because slicing to dimension
zero is cheap.)  Open: C10's independent audit, boundary
classification, `H31`/`H22` obstructions, and the deep strata listed in
Task A.
