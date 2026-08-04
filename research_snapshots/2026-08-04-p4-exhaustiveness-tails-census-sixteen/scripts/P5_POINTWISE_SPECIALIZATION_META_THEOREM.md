# Pointwise specialization for the `H31`/`H22` component programme

## Status

Working note (agent12, 2026-08-04).  This document proves the
generic-to-pointwise transfer theorems invoked by
`P5_DELTA3_OBLIGATION_LEDGER.md` (same directory), states precisely
what semicontinuity does and does not give for the marked incidence
fibres, and demonstrates the machinery on the ninth (all-rank-one
triangle) component's `H31` theorem with exact, fail-closed
computations (`extract_p5_h31_ninth_explicit_divisors.py` /
`.json`, `check_ninth_extraction_points.py` / `.json`,
`retry_frame_q2_extraction.py` / `.json`).

Everything here is standard commutative algebra assembled for this
programme's specific fail-closed discipline; the point is not novelty
but the exact bookkeeping contract: *which finite certificate data,
per irreducible locus, convert the corpus's function-field theorems
into the pointwise statements that the master obligation of the
ledger actually requires.*  Nothing here resolves any component,
census, or global question by itself.

## 1. Setting

Fix `m >= 1` base parameters `p = (p_1,...,p_m)` and `n` fibre
variables `v = (v_1,...,v_n)`.  Let `R = Q[p]`, let `P ⊂ R` be a
prime ideal, `C := V(P) ⊆ A^m_C` the irreducible affine base (a
component chart, a divisor inside it, a slope-extended base
`C × A^1_r`, ...), `O := R/P` its coordinate ring over `Q`, and
`K := Frac(O)` its function field.

An *incidence system* is a finite set
`G = { g_1, ..., g_s } ⊂ R[v]`.  Open conditions
`h != 0` are always encoded by Rabinowitsch variables among the `v`
(`w·h - 1 ∈ G`), so feasibility is plain solvability of equations.
For `x ∈ C(C)` write

```text
F(x) := { v ∈ C^n : g_i(x, v) = 0 for all i },
S(C) := { x ∈ C(C) : F(x) != ∅ }          (the survivor locus).
```

In the ledger's application, `G` is (a chosen subset of) the
*necessary* conditions for an `H31`/`H22` lift at the base point:
the fourteen mixed words, the Rabinowitsch form of the diagonal
sharpness `A·B != 0`, and selected one-marked `4x4` minors (Lemma T
of the ledger).  Emptiness of `F(x)` excludes a lift at `x`;
non-emptiness proves nothing (fail-closed semantics).

Let `I := (G) + P·R[v] ⊆ R[v]` and `I_K := (image of G) ⊆ K[v]`.

## 2. What is true without any certificate

**Proposition 1 (Chevalley; ineffective).**
`S(C)` is a constructible subset of `C(C)`.  If `I_K = (1)` — the
generic fibre is empty — then `S(C)` is contained in a proper Zariski
closed subset of `C`; equivalently, there is a dense open `U ⊆ C`
with `F(x) = ∅` for every `x ∈ U(C)`.

*Proof.*  `S(C)` is the image of the affine variety
`V(I) ∩ (C × A^n)` under the projection to `C`, hence constructible.
If it were dense, its closure would be `C` and the generic point of
`C` would lie in the closure of the image, contradicting emptiness of
the generic fibre (the generic fibre is empty iff `S(C)` is not
dense: `I_K = (1)` iff `1 = Σ h_i g_i` over `K[v]` iff the system is
infeasible over every field extension of `K`, in particular over any
point mapping dominantly).  ∎

**Proposition 2 (why nothing stronger is available).**
The projection `V(I) ∩ (C × A^n) -> C` is in general not proper, and
`S(C)` is in general neither open nor closed.  In the ledger's
incidence systems all three obstructions occur:

1. the marking space is affine (`t ∈ C^4`): survivor markings can
   escape to infinity along divisors — a documented instance is the
   sheet marking `(af(r+1)-(r-1))t_1 = r+1` on component 8, which
   escapes to `t_1 = ∞` exactly on the coupled divisor
   (`P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md`, II.5);
2. the sharpness conditions `A·B != 0` are open conditions on the
   projectivizable variable `z`;
3. the fibre-nonemptiness genuinely *jumps up* on closed subsets of
   the base: on component 1, genuine binary `Delta_2` extensions
   exist exactly on the divisor `l=0`
   (`P5_H31_KNOWN_RANK_TWO_FAMILY_OBSTRUCTION.md`); on component 10,
   binary survivors appear exactly on `c=0` and `b+e=0`; on
   component 9, binary survivor *lines* exist already over the
   generic point and die only at the ternary stage.

Consequently there is no semicontinuity principle of the form
"generic emptiness + closedness of the exceptional locus ⟹ pointwise
emptiness"; the exceptional locus must be *produced*, and the fibres
over it must be *closed by new certificates*.  The next section makes
the production step effective.

**Lemma 3 (the only properness that survives; the binary dichotomy).**
Fix `x` and a marking `t`, and let `M`, `A`, `B` be the mixed matrix
and the two diagonal linear forms in `z`.  There is **no** genuine
binary survivor at `(x,t)` iff

```text
ker M(t) ⊆ ker A     or     ker M(t) ⊆ ker B(t).
```

*Proof.*  Genuine survivors are `z ∈ ker M` with `A(z)B(z) != 0`.
If none exists, the linear space `ker M` lies in the union of the two
hyperplanes `V(A) ∪ V(B)`; a vector space contained in a union of two
proper subspaces lies in one of them.  The converse is trivial.  ∎

This is the abstract content of every "reconstruction kernel" and
"dead frame" in the corpus: dead frames realize `A ≡ 0`
(`ker M ⊆ ker A` trivially); rank-7 frames with a reconstruction
kernel realize `ker M = span(z_rec) ⊆ ker A`; survivor sheets are the
`(x,t)` where an extra kernel direction escapes both hyperplanes.
Lemma 3 is fibrewise only; it induces no closed structure on the base
across rank jumps of `M`.

## 3. The effective transfer

**Theorem 1 (specialization of unit certificates).**
The following are equivalent:

1. `I_K = (1)`  (the verified generic emptiness);
2. `J := I ∩ R` contains an element `d ∉ P`.

Moreover, under (1)–(2):

* **(pointwise transfer)** for *every* `d ∈ J` and *every*
  `x ∈ C(C)` with `d(x) != 0`:  `F(x) = ∅`.  In particular
  `S(C) ⊆ C ∩ V(d)`;
* **(sharpness)** `V(J) ∩ C` equals the Zariski closure of `S(C)` in
  `C`; no smaller closed superset exists;
* **(effectivity)** generators of `J` are computable by eliminating
  `v` from `I` (Gröbner elimination over `Q`), and *any* nonzero
  element of `J mod P` already yields the pointwise transfer — a full
  Gröbner basis is not required for soundness, only for sharpness.

*Proof.*
(1) ⟹ (2): write `1 = Σ h_i ḡ_i` with `h_i ∈ K[v]`, `ḡ_i` the images
of `g_i`.  Clear denominators: there is `d_0 ∈ R ∖ P` and
`H_i ∈ R[v]` with `d_0 - Σ H_i g_i ∈ P·R[v]`.  Then
`d_0 ∈ (G)·R[v] + P·R[v] = I`, and `d_0 ∈ R`, so `d_0 ∈ J ∖ P`.

(2) ⟹ (pointwise): let `d ∈ J`, so `d = Σ H_i g_i + e` with
`e ∈ P·R[v]`.  Evaluate at `(x, v_0)` for `x ∈ C(C)` (so every
element of `P` vanishes at `x`) and any hypothetical `v_0 ∈ F(x)`:
the right side is `0`, the left side is `d(x) != 0` — contradiction.
Hence `F(x) = ∅`.

(2) ⟹ (1): `d` is invertible in `K`, so `1 = d^{-1}·d ∈ I_K`.

(sharpness): over the algebraically closed field `C`, the closure
theorem for elimination ideals gives that `V(I ∩ R)` is the Zariski
closure of the image of `V(I)` under projection; intersecting with
`C` and noting `V(I) ⊆ C × A^n` by construction gives
`V(J) ∩ C = closure(S(C))`.  A closed set containing `S(C)` contains
its closure.

(effectivity): elimination ideals are computable; the membership
certificate `d = Σ H_i g_i mod P·R[v]` produced by the Gröbner lift
is itself a proof object valid at every point with `d(x) != 0`.  ∎

**Remark 1 (semantics of the two uses).**
Theorem 1 is used in two distinct modes, and the ledger keeps them
apart:

* *binary mode* (no minors adjoined): `d(x) != 0` proves "no genuine
  binary survivor at `x`, for any marking" — the strongest pointwise
  statement (component 9, frame `q=1` below);
* *lift mode* (certificate minors adjoined): `d(x) != 0` proves "no
  `H31`/`H22` lift through this frame at `x`" — binary survivors may
  exist at `x`, but each violates a necessary rank condition.  This
  is the mode that matches the corpus's ternary closures.

**Remark 2 (hypersurface bases).**  For a component chart cut by one
irreducible `Phi` (components 2, 8), `P = (Phi)` and the elimination
is run with `Phi` adjoined to the system; `d` must be taken outside
`(Phi)`, which the implementation checks by reduction.  For free
charts (components 9: `K = C(p,q)`) `P = 0` and every nonzero
element of `J` qualifies.

**Theorem 2 (finite Noetherian descent; what "closing a component"
means).**  Let `C_0` be an irreducible base.  Suppose inductively
that for every irreducible locally closed `C ⊆ C_0` reached by the
recursion one of the following verified moves is supplied:

* **(identity move)** a polynomial identity over `Z[p, t, z]` proving
  `F(x) = ∅` for every `x ∈ C(C)` (e.g. an identically vanishing
  diagonal plus Lemma 3; component 10 frames `q=0,1`);
* **(certificate move)** a unit certificate `I_K(C) = (1)` for a
  sound incidence system at `C`'s generic point, together with an
  extracted `d_C ∈ J ∖ P` (Theorem 1), and recursion into the
  finitely many irreducible components of `C ∩ V(d_C)`;
* **(discharge move)** a proof that `C ∩ X_nz = ∅` (Lemma D1), or
  that `C` is `G`-equivalent to an already closed locus (Lemma D2),
  or contained in one (Lemma D4).

Then the recursion terminates after finitely many moves, and its
completion proves `F(x) = ∅` for every `x ∈ C_0(C)`.

*Proof.*  Each certificate move strictly decreases dimension
(`d_C ∉ P` means `V(d_C)` meets `C` properly), and each split
produces finitely many irreducible components (Noetherianity of
`R`); identity and discharge moves are leaves.  A strictly
decreasing dimension bounded below by `0` admits no infinite chain;
at dimension `0` the loci are finitely many points and the
certificate move at a point is an exact Gröbner feasibility check
over a number field.  Coverage: at every point `x ∈ C_0(C)`, follow
the recursion: either some leaf contains `x` (its move applies at
`x`), or `x` survives into a deeper locus; termination forces the
former.  ∎

**Remark 3 (per-component data contract).**  Theorem 2 turns "close
component `C` pointwise" into a finite explicit checklist:

```text
(i)   the generic unit certificates      [exists for comps 1-10]
(ii)  one extraction run per certificate [this note: comp 9 H31]
(iii) recursion data for each component of C ∩ V(d)
(iv)  the boundary: apply the same contract to the closure
      strata of the chart parametrization  [only comps 1-2 H31 done]
```

Item (ii) is cheap when it works and *bounds item (iii) for the
first time* — before extraction, the divisor list of a generic
theorem is open-ended ("implicit denominators"); after it, the
obligation is exactly `V(d)`.

## 4. Discharge lemmas

**Lemma D1 (zero-restriction discharge).**  If the pair restriction
of `P_4` at `x` is the zero tensor then no `H31` or `H22`
configuration produces `x`, and no fibre obligation exists at `x`.
*Proof.*  Fact 1 of the ledger: a configuration's pair restriction
has all-`beta` coefficient `lambda_2/c != 0`.  ∎
Consequently chart loci on which the concentrated single-word
coefficient vanishes identically (comp 3: `4DG`; comp 4:
`4D(D+G-S)`; comp 5: `4DS`; comp 6: `2q(d+p+q)`; comp 7: `2su`;
comp 10: `-2kP` at `k=0`; comp 1 `H22`: `2(C+L)`) are outside
`X_nz` and are *not* part of any obligation.  (Component 10's `P=0`
is *not* discharged: the raw two-word support degenerates there to
the single word `1100` with coefficient `-2kQ != 0`.)

**Lemma D2 (equivariance).**  The symmetry group `G` (diagonal
source torus, source permutations, mode permutations, frame-colour
swap) acts on base and fibre data compatibly; `F(gx) = ∅` iff
`F(x) = ∅`.  *Proof.*  Permanents are diagonal-source eigenvectors
(all sixteen words rescale by one unit and columns of one-marked
maps rescale by units — ranks and (non)vanishing are preserved);
permutations permute rows/frames/pencils; the colour swap exchanges
`alpha_i <-> beta_i`, `A <-> B`, and relabels frames.  ∎

**Lemma D3 (slope endpoints).**  An honest `H22` slope is a ratio of
two nonzero residual torus weights, so `r ∈ C^*`; the projective
endpoints `r ∈ {0,∞}` of either pencil coincide with `H31`
coordinate frames (`D_01^0 ~ q=0`, `D_01^∞ ~ q=1`, `D_23^0 ~ q=2`,
`D_23^∞ ~ q=3`; identification verified exactly in
`verify_slope_boundary_frame_identifications.py` for component 8 and
stated with proof in the component-10 `H22` document).  Hence
endpoint obligations belong to (and are discharged by) the `H31`
side, per component, once the identification is written down — a
mechanical, finite check per component.

**Lemma D4 (locus-intrinsic fibres).**  `F(x)` is defined by `x`
alone (the intrinsic pure-factor lines, markings, extensions); a
point closed once is closed in every ambient component, wall, or
boundary containing it.  *Proof.*  The construction of Section I.3
of the ledger references only the plane tuple `x`.  ∎

## 5. Demonstration: the ninth component, `H31`

Base: `C = A^2_{(p,q)}` (the ninth component's chart is free:
`K = C(p,q)`, `P = 0`).  Verified input: the four function-field
statements of
`P5_H31_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md` —
frame `q=1` has unit binary projection; frames `q=0,2,3` have their
survivor sheets killed by the displayed one-marked minors, with unit
saturated Fitting ideals over `K`.

Incidence systems used (sound by Lemma T of the ledger):

```text
frame q=1:  { 14 mixed words,  w·A·B - 1 }                       (binary mode)
frame q=0:  + minors mode 1: rows (0,2,3,7), (0,3,6,7)           (lift mode)
frame q=2:  + minors mode 3: rows (0,2,3,7), (0,2,6,7), (0,2,4,7)(lift mode)
frame q=3:  + minor  mode 1: rows (0,1,4,7)                      (lift mode)
```

each with the marking `t` FREE (chart-free: no sheet substitution),
over the ring `Q[p,q]` with `p,q` as ring variables.  Every system
was first re-certified unit over `K` (fail-closed), then eliminated.
Results (`extract_p5_h31_ninth_explicit_divisors.json`):

```text
frame   seconds   contraction J = I ∩ Q[p,q]
q=1     3.0       ( p·q - p + 2 )
q=0     0.6       ( p·(p·q + 1) )
q=3     13.8      ( p·(q+1)^2·(q+2) ,  g_2 )        [two generators]
q=2     520       TIMEOUT-NULL with plain std+eliminate; retry with a
                  slimgb pre-pass: 0.6 s,
                  J = ( p·q·(q+1)·(p·q - p + 1) )
                  (retry_frame_q2_extraction.json).  Both per-sheet
                  fallbacks also extracted in < 0.2 s:
                  t_0-line sheet:  ( p·(p·q - p + 1) )
                  t_2-line sheet:  ( q·(p·q - p + 1) )
```

with `g_2 = p(q+1)(q+2)(2p^3+4p^2q-p^2-pq+3p-1)`, so
`gcd(g_1,g_2) = p(q+1)(q+2)` and, as sets,

```text
V(J_3) = {p=0} ∪ {q=-1} ∪ {q=-2}.
```

**Corollary (pointwise ninth-component `H31` theorem).**
For every chart point `(p_0,q_0) ∈ C^2` off the explicit curve union

```text
D9 := { p = 0 } ∪ { q = 0 } ∪ { q = -1 } ∪ { q = -2 }
      ∪ { pq+1 = 0 } ∪ { pq-p+1 = 0 } ∪ { pq-p+2 = 0 }
```

the complete marked `H31` fibre of the ninth component is empty
**pointwise**, not merely generically: frame `q=1` has no genuine
binary survivor at any marking (binary mode, off `pq-p+2=0`), and
frames `q=0,2,3` admit no `H31` lift (lift mode, off their listed
curves).  All four frame statements are now chart-free (no sheet
substitution) and all four contractions are principal-or-explicit.

**What the extraction bought, concretely.**

* *Confirmation*: frames `q=0,2`'s contractions
  `p(pq+1)` and `pq(q+1)(pq-p+1)` consist exactly of divisors already
  displayed in the theorem document's honest-frontier list (14) — for
  those frames the displayed list was complete, which was previously
  unknowable.
* *Discovery*: frame `q=1`'s curve `pq-p+2 = 0` and frame `q=3`'s
  line `q = -2` appear **nowhere** in the displayed list (14) — they
  are precisely the "implicit Gröbner denominators" the atlas warned
  about, now explicit and finite.  The witness check
  (`check_ninth_extraction_points.json`) *confirms the new curve is a
  genuine survivor locus, not a certificate artifact*: at the
  rational points `(p,q) = (-1,3)` and `(5, 3/5)` — on the curve and
  off every displayed divisor — the frame-`q=1` binary system is
  feasible, with exactly one survivor marking each
  (`t = (3/2,0,0,-1/2)` resp. `(-3/20,0,0,1/4)`).  The generic
  theorem's unit projection could never have seen this locus.  The
  same check replays pointwise emptiness at `(2,1)` off all curves
  (all four frame systems infeasible over `Q` at the point).
* *Two displayed divisors cleared*: `p-1 = 0` and `pq+p+1 = 0`
  belong to the document's honest-frontier list (14) but to **no**
  frame contraction — so at their points (off `D9`) the lift-mode
  systems are infeasible after all: those two divisors carry no
  `H31` lift and can be struck from the obligation table.  (They
  were sheet-validity/denominator artifacts, exactly the
  over-conservatism the extraction is designed to remove.)
* *Descent into the new curve — CLOSED at every point*:
  `close_new_curve_descent.py` executes the next certificate move ON
  `W = {pq-p+2=0}` (parametrized `q=(p-2)/p`, `p != 0` on all of
  `W`; equations and one-marked rows cleared by *row-uniform*
  `p`-powers, which rescales each `4x4` minor by a unit on `p != 0`
  — entry-wise clearing would be unsound and an earlier run with it
  was discarded).  Result (`close_new_curve_descent.json`): the
  mode-0 nine-minor battery is unit over `Q(p)`, and the contraction
  in `Q[p]` is the **unit ideal** — `d = 1`.  By Theorem 1 this
  closes the fibre at *every* point of `W`, with no exceptional
  points at all: every binary survivor on the curve (they exist —
  the witness markings above) has a rank-4 mode-0 one-marked map, so
  no `H31` lift exists anywhere on `W`.  Point preview consistent:
  at `(-1,3)` each single mode's battery is already unit over `Q`.
  The newly discovered obligation is thus discharged in the same
  session that discovered it; the informational survivor-sheet
  elimination over `Q(p)` timed out (null, recorded) but is not part
  of the theorem chain.  Ninth-component `H31` remainder after this:
  the six older curves `p=0`, `q=0`, `q=-1`, `q=-2`, `pq+1=0`,
  `pq-p+1=0`, plus chart closure and projective boundary.
* *Strategy lesson*: plain `std`+`eliminate` timed out on frame
  `q=2` where a `slimgb` pre-pass finished in 0.6 s — the same
  pattern the atlas recorded for the component-8 coupled divisor.
  The two corpus-recorded extraction timeouts (component 10's
  survivor-locus eliminations, component 8's coupled divisor) should
  be retried with the `slimgb` pre-pass before being treated as
  hard.
* *Scale calibration*: 2-parameter free chart: seconds.  The
  corpus-recorded 550 s timeouts are 4-parameter runs.  The
  extraction pass is not free — but it is the *only* step that
  converts the unbounded "implicit denominator" obligation into a
  bounded explicit one, so it should be attempted (with `slimgb`,
  block orderings, sheet-splitting, and bigger budgets where needed)
  for every generic theorem in the corpus: 7 more `H31` runs
  (components 3–8, 10), 9 `H22` runs (components 1, 3–10), with
  component 2 `H22` requiring a replacement elimination proof first.

## 6. Interface back to the ledger

Per Theorem 2, the exact per-component data contract is:

```text
component C, frame f:
  (a) generic unit certificate over K(C)         [status: ledger II.3]
  (b) extracted d_{C,f}  in  O(C) \ {0}          [status: comp 9 H31 done
                                                  (all four frames); comp 10
                                                  H31 attempted this session;
                                                  all others pending]
  (c) for each irreducible component D of C ∩ V(d_{C,f}):
        recurse (a)-(c) at D                     [comp 10: c=0, b+e=0 done;
                                                  comp 8: slope divisors done,
                                                  coupled divisor stuck]
  (d) boundary strata of the chart closure:
        same contract                            [only comps 1-2 H31 complete]
  (e) discharges D1-D4 applied first at every level
```

The ledger's Part III minimal set is exactly the todo list of this
contract across the thirteen (or more) components, plus the cover
obligation (O-Cover) that the contract cannot supply.
