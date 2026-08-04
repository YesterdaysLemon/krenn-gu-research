# Findings: component-exhaustiveness sweep of the remaining strata (Task A deep strata, coincident-support case branches, boundary leaves)

Exact computations over Q (sympy rationals + Singular: factorize,
minAssGTZ, `ds` standard bases).  Scripts in `scripts/` (s01..s13, each
self-contained, fail-closed asserts, Singular under subprocess timeouts;
a timeout is recorded as a null and the affected claim is downgraded to
open).  Conventions follow `verify_p4_inout_path_stratum_working_note.py`
(rmul, pairing, perm4 = permanent coefficient, purity = all three 4x4
flattenings of the 16-entry restriction have rank 1, universal
Segre-incidence at an anchor word, family tangents always include the
full projective source torus `diag(t0,t1,t2,1)`).

The ELEVENTH component cited throughout is the equal-support sixfold
`C10`, now documented standalone in
`P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md` (merged while this sweep
ran); that document lists "the deep strata of its chart" as open --
Task A below closes exactly those strata.

HEADLINE.  The swept strata contain **TWO previously unknown
pure-compression components**:

* a **TWELFTH component orbit** (five-dimensional, generic profile
  `(3,3,3,4,3,3)`, rank sum 19) -- the `Zb1` branch of the
  coincident-support chart, certificate in `s06`;
* a **THIRTEENTH component orbit** (five-dimensional, generic profile
  `(3,3,4,3,3,3)`, rank sum 19) -- the `Za2` branch of the same chart,
  certificate in `s08`, one orbit with its mirror `Za3`.

Both are certified at singular incidence points by the char-0
slice-standard-basis pattern of step28 (family tangent 5, incidence
tangent 6, transverse direction second-order obstructed, five-slice `ds`
local dimension 0 => local dimension exactly five => componenthood).
Every OTHER swept stratum either carries only the zero restriction or
embeds exactly into the tenth or eleventh component orbit.  The census
lower bound moves from eleven to **thirteen**; the open tails are listed
at the end.

A structural lemma used throughout the bookkeeping: the pure locus is
cut chartwise by 15 incidence equations in 20 chart variables, so
**every irreducible component has dimension >= 5**; strata of dimension
<= 4 are automatically walls, and their ambient components are found by
the local analysis at their points.

## TASK A: the equal-support chart's deep strata (s01, s02)

Configuration `E`: `u1 = (0,0,1,-1) = U1 cap Pi`, `y2 = (0,0,1,-e) =
U2 cap Pi`, `U3 = Pi`, relations `u1*y3 = 0`, `y2*u3 = 0`
(`y3 = conj(u1)`, `u3 = conj(y2)`), `U0` free.  For a pure nonzero
restriction the two associativity identities force exactly one of three
kernel patterns (s01):

| case | kernels | verdict |
|---|---|---|
| 1 (in-out) | `K3 = y3, K2 = y2` | open chart: W-branch only (known, = eleventh wall); deep strata below |
| 3 (out-in) | `K1 = u1, K3 = u3` | = case 1 of `E(1/e)` under the census symmetry (mode swap (12)) o diag(1,1,e,1): the whole case-3 sweep transfers |
| 4 (out-out) | `K1 = u1, K2 = y2` | open: `U0 = Pi` forced, `det = -(e-1)s^2`, every entry a multiple of `s`: pure => **zero**; deep `x-bar = t v-bar`: chart L **is the C10 = eleventh family** (gauge `c1=1, c2=e`), chart N `det = -4t^2v0^2v1^2(e-1)`: **empty** |

Case-1 deep strata (`rank M1 <= 1  <=>  s = 0 and (v2+v3)(v1x0-v0x1) = 0`),
the explicitly listed open items:

* **(i) `s = 0, v2+v3 = 0`** (`v = (v0,v1,v2,-v2)`, `x-bar = r*(v0,-v1)`):
  the ENTIRE `Gr(2, span(wbar,e2,e3))`-fibre is pure (`B` has rank <= 1
  identically on every chart; full 16-entry flattening purity verified
  symbolically).  Verdict: **embedded in the ELEVENTH** -- the stratum is
  EXACTLY the `(01)`-mode-swap of the C10 family (s02: exact span
  equalities chart by chart; chart L: `vv = wbar`, `c1' = c0`; chart N:
  `c1' = p/q`, `t' = r/p`; the single missing fibre point is the exact
  `c0 -> oo` limit inside the closed set `g(closure(C10))`).
* **(ii) `v1x0 = v0x1 = 0` (support-degenerate v or x; `s=0` forced)**:
  on `v0 = x0 = 0` all four planes lie in the coordinate hyperplane
  `{z0 = 0}`: `T == 0` identically (zero-column permanent lemma); the
  mirror `v1 = x1 = 0` follows by the source swap `(01)`.  Verdict:
  **empty** (zero restriction).
* **(iii) `v0 = v1 = 0` (`U1 = Pi`)** and the mirror `x0 = x1 = 0`
  (`U2 = Pi`): the residual 2x2 block vanishes identically on every
  fibre chart in every kernel case: **empty**.  Deepest stratum
  `U1 = U2 = U3 = Pi`: permanent has three rows supported on `{2,3}`:
  **empty**.

Also identified exactly (s02): the W-branch `= C10(c0=c1=1, c2=e)` (the
known kernel-kernel wall of the eleventh) and case-4-deep chart L
`= C10(c1=1, c2=e, c0 free)`.

CONCLUSION (Task A).  Every nonzero pure point of the equal-support
configuration and all its deep strata lies in the ELEVENTH component
orbit; no twelfth component arises here.

## TASK B1: the coincident-support chart's remaining case branches (s03..s09)

The radical-star classification's coincident-support case with
proportional free factors is the tenth's chart: `ybar = (1,-1,0,0)`,
`u3 = (1,1,0,0)`, `U1 = span(ybar,p)`, `U2 = span(ybar,q)`,
`U3 = span(u3,w)`, `U0` free, relations `ybar*u3 = 0` at `{1,3},{2,3}`.
(The other coincident-support case -- independent free factors -- is the
equal-support configuration `E` above, so Task A already covers it.)
Kernel dichotomy (s03): **case Z** (`K1 = K2 = ybar`) with three
covectors on `U0`, or **case Y** (`K3 = u3`) with one covector.

### Case Z (s03): stratification

* `u3 in ker M_Z` identically: `U0` contains `u3` on every rank-2
  stratum.
* `rank M_Z <= 2  <=>  w2*w3*(w0-w1)*(p2q3-p3q2) = 0`: four rank-2
  branch families (Z-a: `p_Pi || q_Pi`; Z-b: `w in Pi`; Z-c: `w_Pi`
  isotropic, two mirrors).
* `rank M_Z <= 1`: exactly SIX primes (minAssGTZ):
  `#1` degenerate (`w = 0`); `#2` `U3 = P01, p||q`; `#3`/`#6`
  all-planes-in-a-coordinate-hyperplane: `T == 0`; `#4`
  `p_Pi || q_Pi || conj(w_Pi), w in Pi`: **the TENTH's home stratum**
  (whole `Gr(2,3)`-fibre pure, reproducing the tenth's two-word tensor
  exactly); `#5` `U1 = U2 = P01`: zero.
* `#2`: the `p not|| q` part forces `U0 = P01` and pure => zero; the
  `p || q` part's pure fibre points are
  `U0 = span((al,1,0,0),(0,0,1,k))` and embed EXACTLY into the
  **eleventh** (the C10 family's `c1 = c2` wall under the source swap
  `(02)(13)`).

### Case Z rank-2 branches (s04): seven pure families

All seven branch families are identically pure with forced `U0`
(kernels `K1 = K2 = ybar` everywhere):

| branch | equation | generic profile | sum | verdict |
|---|---|---|---|---|
| Za1 | `w3 = -k w2` | `(3,3,4,3,3,3)` | 19 | = **tenth's `m = 1` wall** (s05: exact span identification, mode bijection `(0,1,2,3)->(K,I,J,L)`, `r = W/w2`) |
| Za2 | `(b+e)(k w2-w3) + 2Wbek = 0` | `(3,3,4,3,3,3)` | 19 | **THIRTEENTH component** (s08) |
| Za3 | mirror sign | `(3,3,4,3,3,3)` | 19 | = source-swap-`(01)` image of Za2: same orbit |
| Zb1 | `k(p2+q2)+(p3+q3) = 0` | `(3,3,3,4,3,3)` | 19 | **TWELFTH component** (s06) |
| Zb2 | `k(p2+q2)-(p3+q3) = 0` | `(3,3,3,4,3,3)` | 19 | = `(03)`-mode-swap of Zb1: same orbit |
| Zc1 | `(p2q3+p3q2)W + (p3+q3)w2 = 0` | `(3,3,2,4,3,3)` | 18 | rank-2 pair edge at `{0,3}`; **open** (below) |
| Zc2 | mirror | `(3,3,2,4,3,3)` | 18 | = source-swap-(01) image of Zc1 |

### The TWELFTH component (s06)

Family `F12`: `U0 = span(u3,(0,0,1,-k))`, `U1 = span(ybar,(0,1,p2,p3))`,
`U2 = span(ybar,(0,1,q2,q3))`, `U3 = span(u3,(0,0,1,k))` with the single
tie `k(p2+q2)+(p3+q3) = 0`.  Certificate:
identically pure (support `{0110, 1110}`); generic profile
`(3,3,3,4,3,3)` with ALL 4x4 pair minors vanishing identically at the
five rank-3 edges (so rank sum <= 19 on the whole closure); family
tangent rank 5 (incl. full torus) at `(p2,p3,q2,k) = (3,-1,5,2)`;
incidence Jacobian rank 14 (tangent 6) with the transverse direction
SECOND-ORDER OBSTRUCTED (`rank [J|c2] = 15`); char-0 five-slice `ds`
local dimension 0 => local dimension EXACTLY five => `closure(F12)` is
an irreducible component.  Distinctness: the three sixfolds cannot pass
through the sample (an irreducible sixfold has local dimension 6 > 5 at
each of its points); the eight certified fivefolds all have rank-sum-21
samples, impossible in a closure whose points have rank sum <= 19.
Five rank-one relations at the sample: `u3 (x) ybar` at `{0,1},{0,2}`,
`ybar (x) u3` at `{1,3},{2,3}`, `conj(w) (x) w` at `{0,3}`.

### The THIRTEENTH component (s08)

Family `F13`: `U0 = span(u3, zeta)`,
`zeta = ((b+e)(k w2+w3), 0, -2bek w2, 2bek w3)`, `U1,U2` as in the
chart with `p = (0,1,b,-bk)`, `q = (0,1,e,-ek)`,
`U3 = span(u3, (0,W,w2,w3))`, `W = -(b+e)(k w2-w3)/(2bek)`.
Same certificate chain: identically pure (single word `e_0110`, value
`-4bek`); profile `(3,3,4,3,3,3)`, all 4x4 pair minors vanish at the
five rank-3 edges (sum <= 19 on the closure); tangent 5; incidence 14,
obstructed transverse; five-slice local dimension 0 => dimension exactly
5 => component.  Distinctness: sixfolds by local dimension; certified
fivefolds by rank sum; the TWELFTH by the two-complementary-coordinate-
plane incidence invariant (on all of `closure(F12)` the mode-0 plane
meets both `span(e0,e1)` and `span(e2,e3)`; at the F13 sample NO plane
meets two complementary coordinate planes).  The mirror branch Za3 is
carried onto F13 at the SAME parameters by the census symmetry
`(01)`-source swap, which flips the branch invariant
`Q = 2Wbek/[(b+e)(k w2-w3)]` from -1 to +1 (s08 (7); the first-draft
claim that `diag(1,1,1,-1)` does this was wrong -- that symmetry
preserves each branch, and the corrected identification is verified by
exact span equalities plus the forced-kernel argument).

### Independent cross-checks (s07)

The 24x24 semicontinuity sieve against all ELEVEN certified components
(calibrated on the tenth's self-alignment and on Za1-vs-tenth):
`Za1/Za2/Za3` pass only `tenth`; `Zb1/Zb2` pass only `dq`;
`Zc1/Zc2` pass only `first`/`seventh`.  The closed triple-span
invariant (`dim(U_I+U_J+U_L) <= 3` on all of `closure(tenth)`,
verified identically on the family) excludes the tenth at the
`Za2/Za3/Zb1/Zb2` samples (all of whose mode-triples span `C^4`), and
the step29 coordinate-plane invariant excludes the eleventh at all six
branch samples.  So the sieve exclusions and the certificate-level
exclusions agree.

### Open in the (b2)-chart (s09)

* **Zc branches**: identically pure, `Zc2 = (01)`-source image of Zc1,
  profile bound sum <= 18 on the closure, family tangent 5, incidence
  Jacobian rank 13 (tangent SEVEN -- doubly singular, like the tenth's
  A/B walls).  The five-slice `ds` standard basis did not terminate in
  the local budget (recorded null): the ambient component of the Zc
  wall is **open-with-diagnosis** -- the sieve leaves exactly two
  possibilities: a wall of the SEVENTH (whose rank-2 pair edge matches)
  or a further new component.  (`first` cannot contain it: if the local
  dimension were 5 the closure would be a component with rank sum <= 18
  < 21.)
* **case Y** (`K3 = u3`): single covector `Y1 = (P, P, p3+q3, p2+q2)`,
  `P = p2q3+p3q2`; `U0` ranges over `Gr(2, span(ybar,kA,kB))`; the
  residual 2x2x2 purity system's minAssGTZ stratification is computed
  (chart without `ybar`: 35 primes, 29 carrying a nonzero restriction,
  dims 5-6 of the 9 chart variables; chart with `ybar` in `U0`: 18
  primes, 11 nonzero).  Identified: the `p||q||conj(w_Pi), w in Pi`
  survivor lies in the TENTH's stratum (`#4` above).  The remaining
  survivors are kernel-coincidence WALLS whose census identification is
  **open**; the `P = 0` chart degeneration needs the alternate kernel
  chart and is open.
* **p-in-Pi walls** (`U1 = span(ybar, (0,0,1,pk))` etc.):
  `rank M_Z <= 2 <=> w1w2w3(pk*q2 - q3) = 0`; explicit branch dets
  computed; identification **open** (codim >= 2 walls).

## TASK B2: the disjoint chart's third deep sub-branch `x2 = 0` (s10)

On the double-deep stratum of the disjoint chart the active determinant
is `4(be-al)(v0+v1)x2^2`; the squared factor's branch `x2 = 0` (i.e.
`U2 = P01`) is IDENTICALLY PURE with
`T = -2(x0+x1) [(al,be) (x) (1,v2)]` on the `(x-slot, u3-slot)` words,
and the source swap `(02)(13)` carries the whole family EXACTLY onto
the C10 family (`(c0, c1, c2, t) = (-1, -v1/v0, al/be, al)`, mode
bijection `(0,1,2,3) -> (2,1,3,0)`).  Verdict: **embedded in the
ELEVENTH**; no new component.

## TASK C: boundary leaves (partial; s12, s01, s03)

* **Coincident Pi-positions of the equal-support chart (`e = 1`,
  `U1 cap Pi = U2 cap Pi`)** -- the in-out analogue of the shared-factor
  coincidence (s12).  The `(e-1)`-factors of the `e != 1` chart
  formulas are DEGENERATE-BASIS artifacts (the F3-sheet lesson): with
  the honest Pi-basis, case beta (`K1 = K2 = u1`-direction) has: open
  part `U0 = Pi` forced and pure => zero; deep part chart L = the C10
  family at `c1 = c2 = 1` (inside the eleventh's parametrized family),
  chart N `det = -4t^2v0^2v1^2` => empty.  Case alpha (`K3 = conj(u1)`)
  reduces to a single covector and a 2x2x2 system; its minAss
  stratification has 10 primes with exactly FOUR nonzero survivors,
  all support/coincidence degenerations: `{x || e0}`, `{v || e0}`,
  `{s = 0, x in P01}`, `{s = 0, v in P01}` (gauge `v3 = x3 = 0`);
  identification of these four walls is **open**.
* **Coincident planes**: `U1 = U2 = P01` (`#5`) and `U3 = P01` (`#2`)
  inside the (b2)-chart: zero resp. eleventh (s03); `U1 = Pi`,
  `U2 = Pi`, `U1 = U2 = U3 = Pi` in the equal chart: zero (s01).
* **Support-degenerate star centres, lower-rank Delta, mixed
  rank-one/rank-two strata, triangle chord-wall identification**: NOT
  swept in this pass (unchanged from the snapshot's open list).

## The updated census (s11)

Thirteen certified component orbits.  Distinguishing sample data:

| # | orbit | dim | profile | sum | special invariants |
|---|---|---|---|---|---|
| 1 | first | 5 | (4,4,4,3,3,3) | 21 | triangle, one rank-2 relation |
| 2 | dq | 5 | (4,4,3,4,3,3) | 21 | |
| 3-5 | L1,L2,L3 | 5 | (4,4,3,4,3,3) | 21 | |
| 6 | sixth | 5 | (4,4,3,4,3,3) | 21 | |
| 7 | seventh | 6 | (4,3,2,4,4,3) | 20 | rank-2 pair edge |
| 8 | eighth | 5 | (4,4,3,4,3,3) | 21 | |
| 9 | ninth | 5 | (4,4,4,3,3,3) | 21 | all-rank-one triangle |
| 10 | tenth | 6 | (3,3,4,3,4,4) | 21 | triple-span <= 3 |
| 11 | eleventh | 6 | (4,4,3,4,3,3) | 21 | a coordinate plane |
| 12 | **twelfth** | 5 | (3,3,3,4,3,3) | **19** | K1 = K2 shared; U0 and U3 meet both P01 and P23 |
| 13 | **thirteenth** | 5 | (3,3,4,3,3,3) | **19** | K1 = K2 shared; single-word tensor; no plane meets two complementary coordinate planes |

The twelfth and thirteenth are the first components with generic
pair-rank sum BELOW 20 -- they live strictly inside the degenerate range
that the earlier profile-based censuses could not see.

## What remains toward exhaustiveness

1. the Zc-wall's ambient component (seventh-wall vs new; the slice
   certificate needs a bigger Singular budget or a smarter local
   system);
2. the case-Y survivor walls and their `P = 0` chart, and the p-in-Pi
   walls of the (b2)-chart;
3. the `e = 1` case-alpha survivor walls of the equal chart;
4. Task C leaves not swept: support-degenerate star centres (rank-two
   star), lower-rank Delta, mixed rank-one/rank-two strata, triangle
   chord-wall identification;
5. the twelfth's and thirteenth's independent audits, `H31`/`H22`
   obstructions, and standalone theorem documents;
6. the global exhaustiveness theorem: thirteen is a certified lower
   bound, not a census.

## Script index

- `s01_equal_support_cases_and_deep_strata.py` -- Task A: kernel-case
  trichotomy, case-4 open/deep, case-3 transfer, deep strata (i)-(iii)
  and coincident-plane leaves (pure-family / zero verdicts).
- `s02_equal_deep_i_in_eleventh.py` -- exact embeddings: stratum (i) =
  (01)-swap of C10; W-branch and case-4-deep = C10.
- `s03_b2_caseZ_stratification.py` -- M_Z, rank conditions, six rank<=1
  primes, tenth's home fibre, `#2`/`#5` verdicts (+ `#2` -> eleventh).
- `s04_b2_rank2_branches.py` -- the seven branch families: dets,
  samples, purity, invariants (profiles, kernels, triple spans,
  coordinate incidences).
- `s05_Za1_in_tenth.py` -- Za1 = tenth's m = 1 wall (exact).
- `s06_twelfth_certificate.py` -- the twelfth: purity, profile bound,
  tangent 5, incidence 14 + obstruction, five-slice dim 0,
  separations, Zb2 = (03)-swap.
- `s07_sieve_thirteen.py` -- the calibrated 24x24 sieve of all branches
  vs the eleven components + triple-span and coordinate-plane
  invariants.
- `s08_thirteenth_certificate.py` -- the thirteenth: same chain +
  separation from the twelfth; Za3 = mirror image.
- `s09_Zc_caseY_residual.py` -- Zc facts + open flag; case-Y
  stratification + survivor filter; p-in-Pi wall equations.
- `s10_disjoint_x2_in_eleventh.py` -- disjoint-chart `x2 = 0` sub-branch
  -> eleventh (exact).
- `s11_census_thirteen.py` -- the thirteen-orbit census invariant table.
- `s12_e1_coincident_leaf.py` -- the `e = 1` leaf: basis-artifact
  correction, case-beta verdicts, case-alpha stratification + open
  flag.
- `s13_Zc_ambient_resolution.py` -- conditional resolution of the Zc
  wall's ambient component: replays tangent 5 / incidence 13, attempts
  the char-0 five-slice under a hard timeout, and certifies a
  fourteenth component ONLY if the sliced local dimension is zero;
  otherwise reports the open verdict.
