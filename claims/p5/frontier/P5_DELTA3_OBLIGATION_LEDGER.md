# The remaining-obligation ledger for closing `P_5 -> Delta_3`

## Status and scope

Working note (agent12, 2026-08-04).  This ledger does three things and
claims nothing else:

1. it states **exactly** what remains to be proven so that the
   conclusion "the `P_5 -> Delta_3` restriction admits no
   GHZ-diagonal `H31`/`H22` incidence" — and hence, with the already
   verified theorems, "no restriction `P_5 -> Delta_3` exists over
   `C`" — becomes a theorem (Part I);
2. it tabulates the current status of every obligation against the
   verified repository documents (Part II); and
3. it identifies the minimal remaining set after subsumption, and
   assesses its size honestly (Part III).

Every mathematical assertion below either cites a verified repository
document, or is proven here from first principles, or is explicitly
marked as an *obligation* (open).  Nothing in this note changes the
global **UNRESOLVED** status of the prize conjecture.

Companion documents produced in the same session (same directory):

* `P5_POINTWISE_SPECIALIZATION_META_THEOREM.md` — the rigorous
  generic-to-pointwise transfer theorems used throughout Part I.5 and
  Part III, with the ninth-component demonstration;
* `extract_p5_h31_ninth_explicit_divisors.py` + `.json`,
  `retry_frame_q2_extraction.py` + `.json`,
  `check_ninth_extraction_points.py` + `.json`,
  `close_new_curve_descent.py` + `.json` — the exact fail-closed
  computations that upgrade the ninth component's generic `H31`
  theorem to a pointwise theorem off explicit plane curves.

Throughout, component numbering follows
`P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md` extended by the census
snapshot
`research_snapshots/2026-08-04-p4-exhaustiveness-sweep-census-thirteen/`:

```text
1 first rank-two (dim 5)     8  disjoint mixed-star (dim 5)
2 diagonal-quadric (3,3) (5) 9  all-rank-one triangle (dim 5)
3 L_1 split cubic (5)        10 coincident-support (dim 6)
4 L_2 split cubic (5)        11 equal-support sixfold (dim 6)
5 L_3 split cubic (5)        12 Zb1 fivefold, rank sum 19 (dim 5)
6 mixed-orientation (5)      13 Za2 fivefold, rank sum 19 (dim 5)
7 six-dimensional (dim 6)
```

---

# Part I — the exact logical statement of what remains

## I.1 The frontier reduction (verified input)

By the verified chain — the exact-three-coordinate tree-chart theorem,
the complete partial `q4_211` theorem, the exact `q5_221` theorem, the
`q5_311` exclusion, and the two-singleton theorem, combined with the
audited 6,495-signature census
(`P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`) — every hypothetical
restriction `P_5 -> Delta_3` over `C` has, at some mode `m_0`, a local
map in one of the two normalized families

```text
H31: e_0,e_0,e_0,e_1, a e_0+b e_1+c e_2,  bc != 0        (240 signatures)
H22: e_0,e_0,e_1,e_1, a e_0+b e_1+c e_2,  c != 0,
                                          (a,b) != (0,0)  (270 signatures)
```

after simultaneous diagonal source rescaling.  Hence:

> **(⋆)**  If no `H31` local family and no `H22` local family can be
> completed by four further local maps, then no restriction
> `P_5 -> Delta_3` exists over `C`, and the corresponding finite case
> of the Krenn–Gu programme at this reduction level is closed.

Everything below makes the two hypotheses of (⋆) precise.

## I.2 The common base: the marked pure-compression locus

Fix a hypothetical restriction with an `H31` map at mode `m_0`, and
let `A^(1),...,A^(4): C^5 -> C^3` be the other four local maps.
Contracting `Delta_3` at `m_0` by the target covectors `E_c^*` and
pulling back gives the three source covectors `u_0,u_1,u_2` of the
frontier document, and the two deletion identities

```text
Phi(e_4) = (lambda_2/c) E_2^{(x)4}                (pure deletion),
Phi(e_3) = lambda_1 E_1^{(x)4} - (b lambda_2/c) E_2^{(x)4}
                                                  (sharp Delta_2 deletion),
```

with all `lambda_i != 0` (the diagonal of `Delta_3` is full) and
`bc != 0`.  For each `i` define, restricting to the pure-deletion
source coordinates `{0,1,2,3}`:

```text
beta_i  := colour-2 row of A^(i) on columns {0,1,2,3},
alpha_i := colour-1 row of A^(i) on columns {0,1,2,3},
U_i     := span(alpha_i, beta_i)  ⊆ (C^4)^*.
```

**Fact 1 (pair purity; from the two identities).**  The restriction of
`P_4` through the four `2x4` pair maps `(alpha_i, beta_i)` is the
single word `beta beta beta beta` with nonzero coefficient
`lambda_2/c` — i.e. a nonzero decomposable tensor.  (Every pair word
containing an `alpha` slot is a `{colour 1, colour 2}`-mixed word of
the pure deletion, which vanishes; the all-`beta` word is `lambda_2/c`.)

**Fact 2 (rank-two pairs; verified).**  A pair of rank `<= 1` is
impossible: `P5_H31_SINGLE_GATE_P3_REDUCTION.md`,
`P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md`,
`P5_H31_SECONDARY_GATE_EXCLUSION.md`.  So each `U_i` is an honest
2-plane.

**Definition (the base).**  Let

```text
X    := { (U_1,...,U_4) ∈ Gr(2,(C^4)^*)^4 :
          the pair restriction of P_4 is decomposable
          (all three 4x4 flattenings of the 2^4-entry
           restricted tensor have rank <= 1) },
X_nz := X ∖ { pair restriction = 0 }.
```

`X` is Zariski-closed; `X_nz` is open in `X` (both statements
basis-independent).  By Facts 1–2, **every hypothetical `H31`
configuration hands us a point `x ∈ X_nz`** — with no freedom to move
it.  This is the single most important sentence in the ledger: the
obligation is pointwise over `X_nz` because the adversary picks the
point.

The same holds for `H22`.  There the pure deletion is again colour 2
on `{0,1,2,3}`, and the sharp neighbours are the *weighted* deletions
of `v_0=e_0+e_1` and `v_1=e_2+e_3` (frontier document (6)–(10)); for
the `01` pencil the relevant pair is `(colour-0 row, colour-2 row)`,
for the `23` pencil `(colour-1 row, colour-2 row)`.  Fact 1 holds
verbatim for each pencil's pair tuple.  So `H31` and `H22` fibre
problems live over the *same* base `X_nz`; they differ only in the
fibre conditions.

**The pure-factor structure.**  At `x ∈ X_nz` the restricted pair
tensor is `c · f_1 ⊗ f_2 ⊗ f_3 ⊗ f_4` with `f_i ∈ (U_i-coordinates)^*`
and `c != 0`; the line `span(alpha_i) = ker f_i ⊂ U_i` is *intrinsic*
to `x`.  The residual basis freedom is exactly the marking

```text
beta_i(t) = beta_i + t_i alpha_i,   t = (t_0,...,t_3) ∈ C^4,
```

modulo irrelevant row scalings (the `kappa_i = 0` forcing verified,
e.g., in `P5_H31_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md`
(4)–(5), and identically in the other component documents; the
argument is chart-independent: a nonzero pure marking forces the
kernel row to stay on the intrinsic line).

## I.3 The fibres

Fix `x ∈ X_nz`, bases as above, a distinguished coordinate
`q ∈ {0,1,2,3}` (`H31`) or a pencil `P ∈ {01, 23}` with slope
`r ∈ C^*` (`H22`).  Let `z = (x_0..x_3, y_0..y_3) ∈ C^8` be the
fifth-column extensions of the eight marked rows, `M(t)z = 0` the
fourteen mixed binary words of the corresponding deletion, and
`A(z)`, `B(t,z)` the two diagonal words (`A` is always `t`-free).  For
each mode `m` let `P_m(t,z)` be the `8x4` one-marked matrix of the
neighbouring deletion (rows: `alpha/beta` words of the other three
modes; columns: source coordinates).

**Lemma T (ternary factorization; necessary condition).**
If the configuration extends to an `H31` (or `H22`) local family,
then for every mode `m`:

```text
rank P_m(t,z) <= 3 .
```

*Proof.*  Each row of `P_m` is the covector
`c_w = P_4' ·_{j != m} (marked row_j(w))` on the mode-`m` source.  In a
lift, the marked rows are pullbacks of target covectors,
`alpha_j = (A^(j))^T E_1^*`, `beta_j = (A^(j))^T E_2^*` (colours as per
the frame), so by multilinearity
`c_w = (A^(m))^T ( T' ·_{j != m} E^*_{c_j(w)} )` with
`T'` the restricted order-4 tensor.  Every row therefore lies in the
row space of `A^(m)`, of dimension `<= 3`.  ∎

**Definition (the marked fibres).**

```text
F^H31_q(x)      := { (t,[z]) : M_q(t)z = 0,  A_q(z)·B_q(t,z) != 0,
                     rank P_m(t,z) <= 3 for all m } ,
F^H22,P_r(x)    := the same with the weighted deletion D_P^r .
```

These use *necessary* conditions only (fail-closed): emptiness of
`F` excludes the lift; non-emptiness of `F` proves nothing.

**Lemma B (binary geometry; explains every mechanism in the corpus).**
`A` and `B(t,·)` are linear forms in `z`.  Hence, at fixed `(x,t)`,
there is **no** genuine binary survivor iff

```text
ker M(t) ⊆ ker A     or     ker M(t) ⊆ ker B(t) ,
```

because a linear subspace contained in a union of two hyperplanes lies
in one of them.  All documented closure mechanisms are instances:
identically dead frames (`A ≡ 0`: comp 10 frames `q=0,1`, comp 10
`H22` `01`-pencil) realize the first inclusion globally;
rank-7-with-reconstruction-kernel mechanisms realize
`ker M = span(z_rec) ⊆ ker A`; survivor sheets are exactly the loci in
`(x,t)` where an extra kernel direction escapes both hyperplanes.

## I.4 The master obligation

> **Master Theorem Schema.**  Suppose:
>
> **(O-Cover)** there is an explicit finite list of irreducible closed
> loci `C_1, ..., C_N ⊂ Gr(2,(C^4)^*)^4` and a verified theorem
> `X_nz ⊆ (C_1 ∪ ... ∪ C_N)` up to the symmetry group `G`
> (source `GL`-diagonal torus and permutations, mode permutations,
> and the frame-colour swap);
>
> **(O-H31)** for every `k`, every point
> `x ∈ C_k ∩ X_nz` (every point: interior, parameter divisors,
> deeper strata, and the projective/chart boundary of every
> parametrization — as long as the pair restriction at `x` is
> nonzero), and every `q ∈ {0,1,2,3}`:  `F^H31_q(x) = ∅`;
>
> **(O-H22)** for the same range of `x`, both pencils
> `P ∈ {01,23}`, and every slope `r ∈ C^*`:  `F^H22,P_r(x) = ∅`.
>
> Then no `H31` and no `H22` local family exists over `C`, and with
> (⋆) the restriction `P_5 -> Delta_3` is impossible.

*Proof of the implication.*  A hypothetical `H31` family yields
`x ∈ X_nz` (Facts 1–2), a marking `t` (pure-factor structure), an
extension `z` with `M_q(t)z = 0` and `A·B != 0` (the sharp `Delta_2`
deletion identity; sharpness holds for the whole family because
`bc != 0` makes both diagonals nonzero), and Lemma T's rank bounds —
i.e. a point of `F^H31_q(x)` for the `q` given by the signature's
labelling.  By (O-Cover) and `G`-equivariance of all fibre conditions
(Lemma E below), we may take `x` in some `C_k`, contradicting
(O-H31).  For `H22`: `(a,b) != (0,0)`; if `a != 0` the `01` pencil is
sharp with an honest slope `r ∈ C^*` (the slope is a ratio of two
nonzero residual torus weights), giving a point of `F^H22,01_r(x)`,
contradicting (O-H22); symmetrically for `b != 0`.  ∎

**Lemma E (equivariance).**  All fibre conditions are equivariant
under `G`: permanent tensors are diagonal-source eigenvectors, source
permutations permute deletion frames and pencil labels, mode
permutations permute the four planes, and the colour swap `1 <-> 2`
exchanges `alpha_i <-> beta_i` and `A <-> B`.  Hence `F(gx)` is empty
iff `F(x)` is, and (O-H31)/(O-H22) need only be proven on orbit
representatives.  (This is used silently throughout the corpus as
"source/mode symmetry translates"; the verified instance is, e.g.,
the `k`-gauge of `P5_H31_COINCIDENT_SUPPORT_...md`.)

Three important clarifications of the quantifiers:

* **Pencil labels.**  For a fixed chart the documents check `D_01` and
  `D_23` only.  The other coordinate pair-splits (`02|13`, `03|12`)
  occur among the 270 signatures but are carried to these two by
  source permutations *moving the base point within the `G`-orbit*
  (Lemma E).  Per orbit, two pencils suffice.
* **Slope endpoints.**  `r ∈ {0, ∞}` is *not* an honest `H22` slope
  (a vanishing torus weight is not a gauge of anything); those limits
  are exactly the `H31` coordinate frames
  (`D_01^0 ~ q=0`, `D_01^∞ ~ q=1`, `D_23^0 ~ q=2`, `D_23^∞ ~ q=3`;
  identification verified in
  `verify_slope_boundary_frame_identifications.py`).  So (O-H22)
  quantifies over `C^*` only, and the endpoint statements are owned by
  (O-H31).
* **(O-Cover) is a genuine hypothesis** only because the current
  proofs are organized component-by-component.  Any explicit closed
  cover of `X_nz` works — e.g. the exhaustiveness sweep's case-tree
  strata.  What is *not* negotiable is that some verified cover
  exists; "we know thirteen components" is a lower bound, which is
  the wrong direction.

## I.5 What less suffices — and what does not

This is the crux the whole remaining programme turns on.

**(a) Function-field theorems give density, not points.**  A verified
statement "the generic marked fibre of component `C` is empty" is a
statement over the generic point `Spec K(C)`.  By Chevalley's theorem
the survivor image

```text
S(C) := { x ∈ C : F(x) != ∅ }
```

is a constructible set, and generic emptiness says exactly: `S(C)` is
not dense, i.e. `S(C) ⊆ Z` for some proper closed `Z ⊊ C`.  Two
things it does **not** give:

1. an *identification* of `Z` — the Gröbner eliminations behind the
   generic theorems invert denominators that the theorem statements
   only partially display ("implicit denominators", flagged
   explicitly in `P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md`, Honest
   gaps); and
2. *anything at all* about points of `Z` — and this is not a
   technicality: fibre non-emptiness genuinely jumps up on closed
   subsets.  Verified instances: on component 1 the divisor `l=0`
   acquires genuine binary `Delta_2` extensions
   (`P5_H31_KNOWN_RANK_TWO_FAMILY_OBSTRUCTION.md`); on component 10
   the divisors `c=0`, `b+e=0` acquire binary survivors killed only
   ternarily; on component 9 *even the generic point* has whole
   binary survivor marking lines, killed only ternarily.

**(b) There is no properness to invoke.**  The incidence

```text
E := { (x,t,[z]) : M(t)z = 0, A·B != 0, rank conditions }
```

fails properness over the base three ways: the marking space is affine
(`t ∈ C^4`; markings genuinely escape to infinity — the component-8
coupled-divisor sheet marking `t_1 -> ∞` in atlas II.5 is a live
example); the sharpness conditions `A·B != 0` are open; and the
ternary conditions are closed *conditions on an open set*.  So "the
non-empty locus is closed" is false as a general principle here.
What survives of properness is only Lemma B's fibrewise statement
(the `[z]`-direction alone is projective), which produces the sheet
stratification but no base-closedness.

**(c) The effective substitute (the meta-theorem).**  What replaces
semicontinuity is specialization of unit certificates.  If the
Rabinowitsch-saturated fibre system is the unit ideal over `K(C)` —
which is precisely what the verified generic theorems compute — then
its contraction to the coordinate ring `O(C)` contains a nonzero
element `d`, effectively computable by re-running the elimination with
the parameters as ring variables; and for every point `x ∈ C` with
`d(x) != 0` the fibre statement holds *pointwise*.  The obligation at
`C` then becomes the obligation at the explicit hypersurface
`C ∩ V(d)`, of strictly smaller dimension; Noetherian induction makes
the descent finite.  Full statements and proofs:
`P5_POINTWISE_SPECIALIZATION_META_THEOREM.md` (Theorems 1–2), with the
ninth-component `H31` demonstration (all four frames extracted; see
Part II.4).  Identity-level closures (statements proven as polynomial
identities over `Z[params, t, z]`, like component 10's dead frames
`q=0,1` and its `H22` `01`-pencil) are already pointwise over the
whole chart and need no extraction.

**(d) Discharge lemmas (the "needs less" content).**  The following
reduce the obligation set; each is proven in the meta-theorem
companion (Lemmas D1–D4 there) and applied in Part III:

* **L1 (zero-restriction discharge).**  If the pair restriction
  vanishes at `x`, then `x ∉ X_nz` and *no* fibre obligation exists at
  `x`.  Consequence: every chart locus where the concentrated
  single-word coefficient vanishes identically is **not** an
  obligation.  (It also cannot be reached by "continuity" arguments:
  the master theorem never quantifies over it.)
* **L2 (equivariance)** — Lemma E: obligations live on `G`-orbits.
* **L3 (slope-endpoint identification)** — `H22` endpoint slopes are
  `H31` frames; honest `H22` slopes are `r ∈ C^*`.
* **L4 (locus-intrinsic fibres).**  `F(x)` depends on `x` only — not
  on the component through which `x` was found.  A point closed once
  is closed for every component, wall, or boundary containing it.  In
  particular the *complete* `H31` closures of components 1 and 2
  discharge the `H31` obligations of every stratum of every other
  component that lies inside `closure(C_1) ∪ closure(C_2)`.
* **L5 (levels).**  "Binary-level" and "ternary-level" closures are
  both complete exclusions at their loci; the level only records which
  necessary condition bites.

**(e) Bottom line for Part I.**  The implication needs *pointwise*
emptiness over `X_nz` — no semicontinuity principle weakens this —
but the pointwise statement is reachable by finitely many verified
moves: per irreducible locus, either an identity-level proof, or a
function-field unit certificate *plus an explicit extracted
specialization divisor*, plus recursion into that divisor; plus the
discharge lemmas; plus a verified cover (O-Cover).

---

# Part II — current obligation status

## II.1 The signature layer (verified, complete)

1,680 high-coordinate signatures; 1,170 excluded by local type; the
remaining 510 are `H31` (240 = 120 `a=0` + 120 `a!=0`) and `H22`
(270 = 180 with one of `a,b` zero + 90 with `ab != 0`).  The
fail-closed census and its independent audit replay
(`verify_p5_high_coordinate_partial_frontier.py`,
`audit_p5_high_coordinate_partial_frontier.py`).  Closing (O-H31)
kills all 240 at once; (O-H22) all 270 — the signature multiplicity
is pure labelling (Lemma E).

## II.2 Non-plane strata (verified, complete)

Rank-one pairs and gate configurations: closed
(`P5_H31_SINGLE_GATE_*`, `P5_H31_SECONDARY_GATE_EXCLUSION.md`).
The zero-row/two-singleton and lower-coordinate branches: closed by
the frontier chain.  No open obligation in this layer.

## II.3 Generic fibre theorems per component

| # | `H31` generic | `H22` generic (weighted, slope-transcendental) |
|---|---|---|
| 1 | **closed** (and complete: see II.5) | closed, generic only |
| 2 | **closed** (and complete: see II.5) | closed, generic only — exclusion locus *not explicit* (properness proof; atlas-level gap) |
| 3 | closed, generic only | closed, generic only |
| 4 | closed, generic only | closed, generic only |
| 5 | closed, generic only | closed, generic only |
| 6 | closed, generic only | closed, generic only |
| 7 | closed, generic only | closed, generic only |
| 8 | closed, generic only | closed, generic only |
| 9 | closed, generic only; **pointwise off seven explicit curves (this session — II.4)** | closed, generic only |
| 10 | closed **at binary level**; frames `q=0,1` closed at *every chart point* (identities) | closed at binary level (`01` pencil identically dead at every point and slope) |
| 11 | **OPEN — no theorem** | **OPEN — no theorem** |
| 12 | **OPEN — no theorem** (no standalone component doc yet) | **OPEN — no theorem** |
| 13 | **OPEN — no theorem** (no standalone component doc yet) | **OPEN — no theorem** |

Documents: components 1–8 as listed in the atlas Part I; component 9:
`P5_H31_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md`,
`P5_H22_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md`;
component 10: `P5_H31_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md`,
`P5_H22_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md`.

## II.4 Parameter divisors, per component and frame

Legend: `discharged(L1)` = the pair restriction vanishes identically
there (pure coefficient cited), so the locus is outside `X_nz`;
`closed` = verified complete-fibre statement on the locus;
`open` = obligation.  "implicit" = the un-extracted denominators of
the generic eliminations — an *unbounded* obligation until extraction
is run (meta-theorem step 2).

**Component 1** (`H31` complete).  `H22`: pure coefficient
`T_1111 = 2(C+L)` ⟹ `C+L=0` **discharged(L1)**.  Open: `QU=0`
(marking `t_0`), `P=0` (marking `t_2`), slope divisor `r=1`
(sheet-`B` coefficient), `H=Z-r+1=0` branch, eight projective-kernel
chart denominators (implicit), projective boundary.

**Component 2** (`H31` complete).  `H22` open: the rank-drop locus of
the extension bundle `D_d` (not computed), dense-chart factors
`C(C-l)(1-l^2)r=0`, projective boundary — the only component whose
`H22` exceptional locus is not even explicit in principle (properness
transports one exact fibre; no divisor list exists).

**Components 3–5** (`L_1,L_2,L_3`).  Pure coefficients
`4DG`, `4D(D+G-S)`, `-4DS` ⟹ `D=0`, `G=0` / `D=0`, `D+G-S=0` /
`D=0`, `S=0` respectively **discharged(L1)** in both frames.
`H31` open: `L_1`: `S=0`, `G+S=0`, marking denominators `S`, `S-D+G`;
`L_2`: `D+G=0`, marking-pencil jumps; `L_3`: implicit only;
all three: implicit + projective boundary.
`H22` open: marking denominators `S+G, S, S-D+G, D+G`; slope divisors
implicit (five saturated Fitting ideals over `C(S,D,G,r)`); boundary.

**Component 6.**  Pure coefficient `N = q(d+p+q)` ⟹ `q=0`,
`d+p+q=0` **discharged(L1)**.  `H31` open: `d=0, p=0, d+q=0, p+q=0` +
implicit + boundary.  `H22` open: `d+q=0` sheet + implicit slope
divisors + boundary.

**Component 7.**  Pure coefficient `T_BBBB = 2su` ⟹ `s=0`, `u=0`
**discharged(L1)** (`s=0` is also the chart-validity divisor — the
chart itself must be re-covered there, see II.7).  `H31` open:
`u-v=0` (markings `tau,sigma`) + implicit + boundary.  `H22`: the
*only* component with a fully displayed divisor list; `r=1` **closed**
(equal-weight theorem); open: `r=-1`, `u=1`, `u=v`, `pr-p+1=0`
(marking-coupled), `ru-r+u-v=0` (survivor degeneration), boundary.

**Component 8.**  No pure-coefficient discharge documented (the
component is a hypersurface `Phi=0`; no single-word coefficient is
stated).  `H31` open: `1-a^2f^2=0`, `f=0`, `bf+1=0`, `a^2f+b=0`
(obstruction-ratio factors) + implicit + boundary.  `H22`: slope
divisors `r ∈ {0, 1, -1, ∞}` **closed at binary/ternary level, both
pencils** (atlas Part II; the `r=0/∞` closures by `H31`-frame
identification, verified); **open**: the coupled divisor
`af(r+1)-(r-1)=0` (`D_01`) — certificate designed, modular evidence
complete, main Gröbner **timeout-null** at 550 s (the one place a
generic certificate provably *fails* on a divisor: the mode-0 Fitting
minor drops to rank three there, and the obstruction must move to
modes 1–3); parameter divisors `a=0, b=0, f=0, phi=0, af=±1, bf+1=0,
a^2f+b=0, a^2f^2+2bf+1=0, a^2bf^2+2a^2f+b=0, b^2f^2+bf+1-a^2f^2=0`;
slope × parameter intersections; boundary.

**Component 9.**  Pure coefficient `T_1111 = -2` — *never zero*: L1
discharges **nothing**; every displayed divisor is an honest
obligation.  `H31` displayed open list: `p=0, q=0, q+1=0, p-1=0,
pq+1=0, pq-p+1=0, pq+p+1=0` + implicit + boundary.
**This session's upgrade (meta-theorem demonstration):** the four
frame systems (marking free, certificate minors adjoined,
Rabinowitsch-saturated) were re-eliminated over `Q[p,q]` with the
parameters as ring variables; all four contractions are nonzero and
explicit:

```text
frame q=1 :  (pq-p+2)                          [3.0 s]
frame q=0 :  (p(pq+1))                         [0.6 s]
frame q=3 :  (p(q+2)(q+1)^2 , g_2)             [13.8 s]
             — as a set: {p=0} ∪ {q=-1} ∪ {q=-2}
frame q=2 :  (pq(q+1)(pq-p+1))                 [slimgb retry 0.6 s;
             plain std+eliminate had timed out at 520 s]
```

Consequence (pointwise theorem, fail-closed): **at every chart point
off the explicit curve union**

```text
D9 = {p=0} ∪ {q=0} ∪ {q=-1} ∪ {q=-2}
     ∪ {pq+1=0} ∪ {pq-p+1=0} ∪ {pq-p+2=0}
```

**the complete marked `H31` fibre is empty pointwise** — not just
generically.  The remaining component-9 `H31` obligation collapses
from "the seven displayed divisors *plus unknown implicit
denominators*" to exactly the seven explicit curves of `D9`, plus
chart closure and projective boundary.  Three sharpenings against
the theorem document's displayed list (14):

* `pq-p+2` (frame `q=1`) and `q+2` (frame `q=3`) are **new** —
  invisible in (14); the witness check
  (`check_ninth_extraction_points.json`) proves `pq-p+2=0` is a
  *genuine* survivor curve, not an artifact: at `(p,q)=(-1,3)` and
  `(5,3/5)` (on the curve, off all displayed divisors) the
  frame-`q=1` binary system is feasible with exactly one survivor
  marking each — a real new obligation no generic theorem could see;
* `p-1` and `pq+p+1` from (14) lie in **no** frame contraction:
  those two displayed divisors carry no `H31` lift and are struck
  from the obligation table (over-conservative listing removed);
* pointwise emptiness independently replayed at `(2,1)` by direct
  rational Gröbner (all four frames infeasible).
* descent one level down, **completed**: the new curve `pq-p+2=0`
  is closed at *every* point (`close_new_curve_descent.py/.json`):
  on the curve (row-uniformly `p`-cleared system, sound on its chart
  `p != 0` which is all of the curve), the mode-0 nine-minor battery
  is unit over `Q(p)` and the contraction in `Q[p]` is the unit
  ideal `(1)` — no exceptional points.  The obligation discovered by
  the extraction is discharged in the same session.  The remaining
  component-9 `H31` divisor obligations are the six older curves
  `p=0, q=0, q=-1, q=-2, pq+1=0, pq-p+1=0` (all displayed in the
  theorem document except `q=-2`) plus chart closure and boundary.
`H22` open: slope divisors `r=0,1,-1` (endpoints transportable by
L3 once made explicit), coupled divisors
`pr+1=0, pr-1=0, pq+pr+1=0, pqr+r+1=0`, the same parameter list,
boundary.

**Component 10.**  Raw support `T_1100=-2kQ`, `T_1101=-2kP` ⟹ `k=0`
**discharged(L1)** (all sixteen words vanish).  `P=bec+b+e=0` is
*not* discharged (the restriction degenerates to the single word
`1100` with coefficient `-2kQ != 0`: still in `X_nz`; a different
concentration applies) — open.  Frames `q=0,1` and the `H22` `01`
pencil: closed at **every chart point** (polynomial identities — the
strongest closure level in the corpus).  Divisors `c=0`, `b+e=0`:
**closed** at ternary level, both frames.  Open: codim-2 survivor
strata (`{ec+1=0, m=0}`, `{bc+1=0, m=0}`, deeper census fine
structure), `P=0`, parameter-coupled slope divisors (unextracted),
chart closure, boundary.  The direct survivor-locus eliminations with
ring-variable parameters **timed out** at 550 s (recorded null) — the
same computation that succeeded for component 9 this session; the
difference is 4 parameters vs 2.  A slimgb-preconditioned retry of
exactly that extraction (frames `q=2,3`, binary mode) was run this
session (`extract_p5_h31_tenth_explicit_divisors.json`): frame
`q=2` **timeout-null again at 840 s even with slimgb** — the
4-parameter extraction is genuinely harder than the 2-parameter one
and needs the atlas's further mitigations (sheet splitting first,
block orderings, modular-guided factor hints) or a larger budget.
Frames `q=0,1` remain identity-dead pointwise regardless.

**Components 11–13.**  No generic theorems, hence no divisor rows:
the entire fibre programme is open.  Component 11's chart and walls
are documented (`P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md`);
components 12–13 have certificates only inside the sweep snapshot
(`s06`, `s08`) and no standalone documents.

## II.5 Projective/chart boundaries

* Components 1–2, `H31`: **closed** — the only complete boundary
  programmes in the corpus (marked-basis bundle, preferred-chart
  divisor, Schubert line, internal `E=0`, 21 toric orientations;
  elliptic regular chart, both marking divisors, pivot complement,
  normalization boundary, outer `ABF=0`).
* Everything else — components 3–13 `H31`, components 1–13 `H22`:
  **open**.  No `H22` boundary statement exists for any component.
* By L1, only the boundary part where the pair restriction stays
  nonzero is an obligation (e.g. entire toric vertices with zero
  restriction discharge automatically; this is how the comp-1/2
  boundary programmes were finite).

## II.6 Slope obligations (`H22` only) — summary

| # | endpoints `r∈{0,∞}` (=`H31` frames, L3) | `r=1` | `r=-1` | coupled |
|---|---|---|---|---|
| 1 | transportable, not executed | open (`(r-1)` sheet coefficient) | open | — |
| 2 | transportable, not executed | open | open | unknown (no explicit list) |
| 3–5 | transportable, not executed | implicit | implicit | implicit |
| 6 | transportable, not executed | implicit | implicit | implicit |
| 7 | transportable, not executed | **closed** (equal-weight) | open (recipe drafted in atlas III) | `pr-p+1=0`, `ru-r+u-v=0` open |
| 8 | **closed** (verified identification) | **closed** | **closed** | `af(r+1)-(r-1)=0` **open, timeout-stuck**; slope×param open |
| 9 | transportable, not executed | open | open | `pr±1=0, pq+pr+1=0, pqr+r+1=0` open |
| 10 | **closed** (in-doc: `r=0,1,-1` unit + `∞` = `q=3`) | **closed** | **closed** | parameter-coupled unextracted |
| 11–13 | — no generic theorem yet — | | | |

## II.7 Exhaustiveness (O-Cover)

Current state: **thirteen certified component orbits — a lower
bound, not a census** (snapshot README, verbatim).  The open tails:

1. the `Zc`-wall ambient component (seventh-wall vs a *fourteenth*
   component; the deciding slice standard basis timed out; `s13`
   re-runs it conditionally);
2. the case-`Y` survivor walls and their `P=0` chart, and the
   `p`-in-`Pi` walls of the `(b2)`-chart;
3. the `e=1` case-alpha survivor walls of the equal chart;
4. Task C leaves never swept: support-degenerate star centres
   (rank-two star), lower-rank `Delta`, mixed rank-one/rank-two
   strata, triangle chord-wall identification;
5. components 12–13: independent audits, standalone documents;
6. the global assembly: a theorem `X_nz ⊆ ∪ closures` (the current
   case tree covers the *classified* orientations: directed
   radical-star, mixed orientations in the dense `3x4` chart,
   in-out path, coincident/equal support; remaining per the frontier
   document: other mixed kernel-edge orientations, rank-two
   exceptional relations, lower pair-image rank).

Risk note: the certified census went 8 → 11 → 13 within 2026-08-04.
Each new component adds two generic-theorem obligations plus a full
descent tree.  The census has **not stabilized**, and (O-Cover) is
the only obligation whose size is currently *unbounded* by any
verified statement.

---

# Part III — the minimal remaining set

## III.1 Deduplication rules (proved in Part I.5(d))

Applying L1–L5 to Part II turns the per-component tables into a
locus-based ledger.  Rules: (i) drop every `discharged(L1)` row;
(ii) fold `H22` endpoint slopes into `H31` frames (L3); (iii) merge
walls shared between components — a wall is one obligation, owned by
whichever ambient locus closes it first (L4); (iv) obligations on
loci inside `closure(C_1) ∪ closure(C_2)` are already closed for
`H31` (L4 + the complete comp-1/2 `H31` theorems).

## III.2 The minimal ledger

**M0 (blocking everything downstream): generic theorems for
components 11, 12, 13, both frames.**  Six function-field theorems.
Until these exist, the census cannot shrink and *no* pointwise
statement about those components is even formulable.  (The eleventh's
chart is documented; the twelfth/thirteenth need standalone component
documents first.)

**M1 (the extraction pass): one specialization-divisor extraction per
generic theorem.**  Sixteen runs (`H31`: components 3–8 and 10 = 7,
component 9 done this session; `H22`: components 1 and 3–10 = 9),
plus component 2 `H22`, which needs a *replacement* proof first —
its properness argument has no elimination to extract.  Each successful run
converts "implicit denominators" (unbounded) into an explicit curve/
hypersurface list (bounded).  Evidence of feasibility: component 9
`H31` — all four frames, 0.6–14 s each (this session).  Evidence of
difficulty: component 10's recorded 550 s timeouts (4 parameters),
component 8's coupled-divisor timeout.  Mitigations recorded in the
atlas (block orderings, `slimgb`, sheet-splitting) and in the
meta-theorem document (two-stage elimination, per-sheet fallbacks).

**M2 (named divisor closures now open, post-discharge).**  From
II.4/II.6, the current named list (deduplicated):

* comp 1 `H22`: `QU=0`, `P=0`, `r=1`, `H=Z-r+1=0`;
* comp 2 `H22`: rank-drop locus of `D_d` (must first be made
  explicit), `C(C-l)(1-l^2)r=0`;
* comp 3: `S=0`, `G+S=0`, `S-D+G=0` (+`H22` mirrors);
  comp 4: `D+G=0` (+ jumps); comp 5: — (implicit only);
* comp 6: `d=0`, `p=0`, `d+q=0`, `p+q=0` (+`H22` `d+q=0`);
* comp 7: `u-v=0` (`H31`); `H22` `r=-1`, `u=1`, `u=v`, `pr-p+1=0`,
  `ru-r+u-v=0`;
* comp 8: `1-a^2f^2=0`, `f=0`, `bf+1=0`, `a^2f+b=0` (`H31`); `H22`
  parameter list (ten polynomials), **coupled divisor
  `af(r+1)-(r-1)=0` (stuck)**, slope×parameter intersections;
* comp 9 `H31`: exactly six explicit curves
  (`p`, `q`, `q+1`, `q+2`, `pq+1`, `pq-p+1`) plus chart
  closure/boundary — with `p-1`, `pq+p+1` struck and the newly
  discovered seventh curve `pq-p+2` **closed at every point**, both
  this session; comp 9 `H22`: `r=±1`, four coupled divisors, the
  parameter list;
* comp 10: `P=0`, codim-2 survivor strata, parameter-coupled slopes.

Each of these is a *recursive* instance of the same problem one
dimension down (meta-theorem Theorem 2): generic theorem over the
divisor + extraction + its own sub-divisors.  Historical cost per
divisor: between one two-row identity (component 8, `r=1`) and ten
documents (component 2's elliptic descent).

**M3 (boundary programmes).**  `H31`: components 3–13 (11
programmes).  `H22`: components 1–13 (13 programmes).  The only two
completed instances (components 1–2 `H31`) each required a full
plane-degeneration stratification (toric atlas / outer-boundary
reduction).  L1 trims each programme to the nonzero-restriction part
of the boundary.

**M4 (exhaustiveness).**  The six tails of II.7 plus the global
assembly theorem, i.e. (O-Cover).  Any new component found feeds
back into M0.

**M5 (the two stuck computations).**  Component 8's coupled divisor
(mode-3 Fitting, Gröbner timeout; two designed continuation routes)
and component 10's ring-variable survivor eliminations.  Both are
now instances of M1/M2 with concrete failure diagnostics.

## III.3 What is *not* an obligation (fully discharged, no residue)

* the 1,170 signature exclusions and the whole lower-coordinate
  frontier (II.1–II.2);
* rank-one pairs / gates; two-singleton branches;
* pure-coefficient loci: comp 1 `C+L=0` (`H22`), comps 3–5
  `D=0, G=0, S=0, D+G-S=0` (as per II.4), comp 6 `q=0, d+p+q=0`,
  comp 7 `s=0, u=0`, comp 10 `k=0` — all outside `X_nz` (L1);
* `H22` endpoint slopes for components 8 and 10 (verified
  identifications) — and for every other component *once* the
  mechanical L3 transport is written down (a finite check per
  component, no new mathematics);
* every `H31` obligation on loci inside `closure(C_1) ∪
  closure(C_2)` (L4) — this includes any exhaustiveness-tail
  stratum that turns out to embed there.

## III.4 Honest size assessment

Counting Part III.2: **6** missing generic theorems (M0), **16+1**
extraction runs of which two corpus-recorded attempts timed out
(M1), **~35** named open divisor loci each of which is a
one-dimension-down recursive instance (M2), **24** untouched
boundary programmes (M3), **6+1** exhaustiveness items with
unbounded downstream risk (M4).

Calibration against completed work: the two completed descent trees
(components 1–2, `H31` only) consumed roughly twenty theorem
documents.  The session narrative "ten of thirteen components closed
for both frames" counts only the *top node* of each tree (the generic
theorem) — the cheapest layer.  On the current evidence the remaining
programme is **several times larger than everything done so far**,
dominated by (in order): exhaustiveness risk (M4, unbounded),
boundary programmes (M3, 24 instances of the only step ever completed
twice), and divisor recursion (M2).  The one force multiplier that
changes the arithmetic is the meta-theorem pass (M1): it is cheap
where it works (component 9: seconds), it converts unknown-unknowns
into explicit curves, and every closure it produces is pointwise —
the currency the master theorem actually accepts.  It should be run
component-by-component *before* any further hand-crafted divisor
work, so that hand work is spent only on loci that provably carry
survivors.

The blunt sentence: **the component programme is structurally on
track but quantitatively early; roughly the top third of each
component's obligation tree exists, the bottom two thirds
(divisor recursion, boundaries) exist for exactly two of twenty-six
component-frame pairs, and the cover hypothesis (O-Cover) — without
which the per-component work cannot conclude — is not yet a theorem
and is still growing.**
