# C_{6,1}: kernel restriction, C_{4,1} = ∅, and where the method stops — 2026-10-09

This is a dated research record.  The global Krenn–Gu status is
**UNRESOLVED**, and nothing here changes it.  No theorem about witnesses is
added, withdrawn or re-scoped.  Section 9 says what the frontier needs.

Evidence labels:

- **[EXACT]**: a hand proof given here, or an exact (integer / rational /
  symbolic) computation.
  - [`verify_c61_kernel_restriction.py`](../../claims/finite/n08/verify_c61_kernel_restriction.py)
    replays the displayed identities and the one elementary rank fact.  It
    is a replay, not the proof.
  - [`verify_c41_exclusion.py`](../../claims/finite/n08/verify_c41_exclusion.py)
    is the computational half of the C_{4,1} proof (Section 5).
  - Both were written by the author of the hand arguments.  Neither is an
    independent audit.
- **[NUMERIC]**: a floating-point computation that converged to a residual
  below `1e-28` at bounded gauge-balanced norm, with a Jacobian-rank
  reading.  Evidence, never a proof.
- **[OBSERVATION]**: a numerical search that did not converge, or a reading
  of one model.  Never a proof.
- No **[MODULAR]** or **[SAT-RUN]** evidence was produced (Section 8).

## 0. Answer

1. **C_{6,1} is still OPEN.**  Neither Φ0 nor C_{6,1} = ∅ is proved, and no
   witness was found.  No escalation item arose: no computation produced an
   apparent C_{6,1} configuration.
2. **C_{4,1} = ∅  [EXACT, computer-assisted; no independent audit]**
   (Section 5).  C_{4,1} has four three-colour vertices and two
   non-adjacent one-colour vertices.  It never realizes GHZ(4,3) with three
   nonzero weights.
   - **Proof.**  (AK) and the torus reduce the problem to 292 strata of
     ancilla rows.  The tensor is linear in the `B`-blocks.  Each stratum
     is closed by explicit dual certificates (mostly rank-one, of
     kernel-restriction type), checked by exact multiplication.  Runtime is
     about 30 s.
   - **Calibration.**  This is the order-6 instance of the Lemma-5 route.
     The route is faithful one order down: with C_{4,1} = ∅, Lemma 5 sends
     every GHZ(6,3) configuration on six three-colour vertices into the
     order-6 matrix-unit class (every block a single nonzero entry).
3. **New exact family: kernel restriction (KR)** (Sections 2–4).
   Restricting a vertex `z` of `B` to the common kernel
   `K_z = ker r_z^T ∩ ker s_z^T` of its two ancilla rows turns it into a
   third ancilla adjacent to neither `a` nor `b`.  For every C_{6,1}
   configuration this gives:
   - **(KR1)** `|B - Z| <= 1`.  For all but at most one `z in B`, some unit
     vector `e_c` lies in `span(r_z, s_z)`.  Restricting two vertices
     outside `Z` produces a C_{4,1} configuration, which is impossible by 2.
     The unconditional `Per_3` argument (KR3) gives `|B - Z| <= 2`.
   - **(KR2)** For every pair `p = {k, k'}` whose complement does not kill
     all three colours, `C_p = r_k s_k'^T + s_k r_k'^T` is a nonzero
     diagonal matrix, with support fixed by the colour profile.
   - **(GCK)** A generalized conditional killer at any vertex outside `Z`.
     It contains the conditional killer (CK) of the ancilla note.
4. **The method stops at KR1 + KR2 + GCK** (Section 4).
   - Restricting one vertex lands in `D(5,3)`: five three-colour vertices
     and three pairwise non-adjacent ancillas realizing GHZ(5,3).  That
     class is **nonempty** [NUMERIC].  An isolated point modulo gauge
     converged to cost `1.4e-30`, and a separate engine confirms residual
     `2.4e-16`.
   - Restrictions at vertices of `Z` leave two-colour targets.  These are
     realized **exactly** by cycle constructions.
   - So the emptiness of restricted classes cannot exclude C_{6,1} beyond
     KR1.
5. **Φ0's order-4 analogue is false** [NUMERIC].  Two of the four
   edge-allowed C'_{4,1} solutions have `Φ(c^4) != 0` for all three
   colours.  At order 4 the edge channel `κ T_B` can itself carry
   GHZ(4,3), so this does not touch Φ0 at order 6.  It does rule out any
   order-blind proof of Φ0.
6. **Construction attempts** (Section 6) [OBSERVATION]: none converged.
   - four single-entry-ancilla support patterns for C_{6,1};
   - three lifts of the D(5,3) point, each un-contracting one of its
     ancillas into a three-colour vertex.

**Most load-bearing fact.**  `C_{4,1} = ∅` exactly, so the pair-contraction
route is faithful at order 6.  At order 8 the same restriction machinery
pins every C_{6,1} configuration to `|B - Z| <= 1` but cannot go further,
because the one-vertex restriction class `D(5,3)` is nonempty.  A proof of
C_{6,1} = ∅ (or of Φ0) must therefore use **several contractions of one
three-colour vertex at once**.  The natural finite test bed is the
single-entry-ancilla residual of Section 7.

## 1. Setting and notation

Conventions follow the ancilla note (branch `claude/ancilla-c61-20261009`,
file `docs/strategy/ancilla-c61-2026-10-09.md`) and Lemma 5 of
[`compressed-hessian-family-2026-10-09.md`](compressed-hessian-family-2026-10-09.md).

- `B = {0, ..., 5}` are three-colour vertices with `3 x 3` blocks `W_uv`.
- `a`, `b` are one-colour vertices with rows `r_z`, `s_z in C^3`
  (`z in B`), and no `ab` edge (`κ = 0`).
- For `y = (y_z)_{z in B}`, `y_z in C^3`, write `ℓ_z = r_z · y_z`,
  `m_z = s_z · y_z` and `A_uv = y_u^T W_uv y_v`.
- The generating polynomial of the tensor is
  `P(y) = Σ_{z != z'} ℓ_z m_z' Haf(A_{B - z - z'})`.  This is (1) of the
  ancilla note, with `Θ_γ[z, z'] = Haf(A_{B-z-z'})` at `y = e_γ`.
- C_{6,1} asks for `P = G` with `G(y) = Σ_c μ_c Π_z y_z[c]` and all
  `μ_c != 0`.

**Classes.**  `D(n, k)` is the set of configurations with `n` three-colour
vertices and `k` one-colour vertices, pairwise non-adjacent, whose tensor is
`GHZ(n,3)` with three nonzero weights.

- `C_{6,1} = D(6,2)` and `C_{4,1} = D(4,2)`.
- `D(n, k) = ∅` trivially when `k > n`, because no perfect matching exists.
- In every `D(n,k)` with `k >= 1` the tensor is **linear in the B-blocks**
  when `n - k = 2`.  Then each perfect matching uses exactly one `B`–`B`
  edge.

**Colour profile.**  `K_z = ker r_z^T ∩ ker s_z^T` (dimension 1, 2 or 3).
`E_z = {c : K_z ⊆ {y[c] = 0}} = {c : e_c ∈ span(r_z, s_z)}`.
`Z = {z : E_z != ∅}`.  For `S ⊆ B`, `E_S = ∪_{s in S} E_s`.

## 2. The kernel-restriction lemma  [EXACT]

**Lemma KR.**  Let `S ⊆ B`, `F = B - S`, and `v_s ∈ K_s` for `s in S`.
Contract the C_{6,1} tensor at every `s in S` with `v_s`.  The result,
as a tensor on `F`, is the matching tensor of the configuration on
`F ∪ {a, b} ∪ S` in which

- every `s in S` is a one-colour vertex,
- `s` has row `v_s^T W_{sf}` to `f in F`,
- `s` has weight `v_s^T W_{ss'} v_{s'}` to `s' in S`,
- `a` and `b` keep their rows on `F` and are adjacent to no one-colour
  vertex.

The target becomes `Σ_c g_c(v) Π_{f in F} y_f[c]`, with
`g_c(v) = μ_c Π_{s in S} v_s[c]`.

*Proof.*  Contracting a matching tensor at a vertex with a vector gives the
matching tensor with that vertex replaced by a one-colour vertex carrying
the contracted rows.  The `a`–`s` and `b`–`s` weights are `r_s · v_s = 0`
and `s_s · v_s = 0`.  ∎

`g_c` vanishes identically on `Π_{s in S} K_s` iff `c ∈ E_S`, since a
product of linear forms on an irreducible product space vanishes iff one
factor does.  The verifier replays the lemma exactly for every `S` with
`|S| = 1, ..., 4` on three random integer configurations, against two
independent tensor engines.

## 3. Unconditional consequences  [EXACT]

### 3.1 KR3: at most two vertices outside Z

**Lemma KR3.**  For every 3-subset `S ⊆ B`, `E_S != ∅`.  Equivalently,
`|B - Z| <= 2`.

*Proof.*

1. Take `|S| = 3` and `F = {1, 2, 3}` (relabelled).
2. In every perfect matching of the restricted configuration, `a` and `b`
   are matched to two distinct vertices of `F`.  The third vertex of `F` is
   matched to one vertex of `S`, and the other two vertices of `S` are
   matched to each other.
3. So the restricted tensor is `Σ_{π} Π_{i in F} (N_i y_i)[π(i)]`.  Here
   `π` runs over bijections from `F` to the roles `(a, b, S)`, and `N_i`
   has rows `r_i`, `s_i` and `u_i = Σ_{s} W_{is} v_s · A_{s's''}(v)`.
   This is `(N_1^T ⊗ N_2^T ⊗ N_3^T) Per_3`, where
   `Per_3 = Σ_{π in S_3} e_{π(1)} ⊗ e_{π(2)} ⊗ e_{π(3)}`.
4. If `E_S = ∅`, choose `v` with every `g_c(v) != 0`.  The target is the
   concise unit tensor `diag(g)`.
5. Every flattening of `diag(g)` has rank 3, so every `N_i` is invertible.
   Then `Per_3` is `GL^3`-equivalent to the unit tensor `<3>`.
6. That is impossible.
   - The mode-1 slice span of `Per_3` is the space of symmetric hollow
     `3 x 3` matrices `[[0,c,b],[c,0,a],[b,a,0]]`.  All its 2 x 2 minors
     vanish only at `a = b = c = 0`, so it contains no rank-one matrix.
   - The slice span of `<3>` (the diagonal matrices) contains `E_00`.
   - Slice spans transform by `M ↦ B M C^T` under `GL^3`, which preserves
     rank.  ∎

The same argument at `|S| = 4` gives the D(2,2) statement used next.  It
also shows `D(2,2) = D(3,3) = ∅`: a rank `<= 2` bilinear form, or a `Per_3`
image, is never a concise unit tensor.

### 3.2 KR2: forced diagonal pair matrices

**Lemma KR2.**  Let `p = {k, k'}`, `S = B - p` (`|S| = 4`), and
`C_p = r_k s_k'^T + s_k r_k'^T`.  For all `v ∈ Π_{s in S} K_s`,

```text
diag(g_0(v), g_1(v), g_2(v)) = h_S(v) · C_p,      h_S(v) = Haf(A(v)_S).      (KR2)
```

Consequently:

- if `E_S != [3]`, then `C_p` is a nonzero diagonal matrix, and
  `C_p[c,c] != 0` iff `c ∉ E_S`;
- if `E_S = [3]`, then `C_p = 0` or `h_S ≡ 0` on `Π K_s`.

*Proof.*  In the restricted configuration `a` and `b` must both be matched
into `p`, and the four one-colour vertices of `S` are matched among
themselves.  So the tensor is `h_S(v) (y_k^T C_p y_k')`.  Compare the
coefficients with the target `y_k^T diag(g(v)) y_k'`.  If `g ≢ 0`, evaluate
at a `v` with `g_c(v) != 0` for every `c ∉ E_S`.  ∎

KR2 bites only when some colour is **rare**, meaning
`N_c = {z : c ∈ E_z}` has at most two elements.  The forced pairs are then
the `p ⊇ N_c`.

- By (AK), `N_c ⊇ {z_c, w_c}`, the ancilla killers of `a` and `b`.
- The symmetric PyTheus completion of the ancilla note (its Section 3.4)
  meets KR2 with equality: `N_c = P_c` and `C_{P_c} ∝ e_c e_c^T`.  So KR2
  does not reprove that rank-two no-go; that argument is a different
  mechanism.

### 3.3 GCK: generalized conditional killers

**Lemma GCK.**  Let `s ∈ B - Z`.  Then for every colour `c` there is
`u ∈ B - s` with

```text
v^T W_su ∈ C · e_c^T   for every v ∈ K_s,
```

and it is nonzero for generic `v ∈ K_s`.

*Proof.*

1. Restrict `s` to a full-support `v ∈ K_s` (Lemma KR, `|S| = 1`).  The
   vertex `s` becomes a one-colour vertex adjacent to neither `a` nor `b`,
   with rows `u_f = W_sf^T v`.  Every perfect matching sends `s` into
   `F = B - s`.
2. Restrict each `f in F` to `ker u_f^T`.  Every channel vanishes, while the
   target is `Σ_c μ_c v[c] Π_f y_f[c]` with nonzero weights.
3. The hyperplane-annihilation theorem
   ([`THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md`](../../claims/arbitrary-order/THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md),
   `m = 5`) then gives, for each `c`, an `f` with `u_f ∝ e_c`, nonzero.
4. If `dim K_s = 2`, the full-support `v` are Zariski-dense in `K_s`.  The
   condition is linear in `v` and there are finitely many `f`, so one `f`
   works on all of `K_s`.  ∎

- The case `r_s = s_s = 0` (`K_s = C^3`) is the conditional killer (CK) of
  the ancilla note, i.e. a column killer.
- When `K_s` is a line `C k_s`, GCK says that each colour has a partner `u`
  with `k_s^T W_su` a nonzero multiple of `e_c^T`.  This is a value-level
  condition, invisible to the support model.

### 3.4 Remarks on encodability

KR1 (Section 4.3), KR3 and KR2 are **not** support-level clauses for
general rows.

- `e_c ∈ span(r_z, s_z)` is a rank condition: a 2 x 2 minor of `(r_z, s_z)`
  on the other two colours vanishes.
  - Its support shadow is "the two rows restricted to `[3] - c` have
    rectangle-shaped support".
  - Two full rows satisfy that shadow.
- So the 155-entry SAT model of the ancilla note survives the support
  shadows.  At its three full-row vertices `2, 4, 5`, KR1 makes at least
  two of these minors vanish, which is a value-level condition.
- For single-entry rows everything here becomes combinatorial (Section 7).
- The models were not re-run (Section 8).

## 4. Where kernel restriction stops

### 4.1 D(5,3) is nonempty  [NUMERIC]

Restricting one vertex `s ∉ Z` gives a `D(5,3)` configuration.  The search
`run_track.py 5 3 0` (seed 7, restart 3) uses Levenberg–Marquardt in chunks,
with the torus balancing of the ancilla note after every chunk.  It
converged as follows:

- cost `1.4e-30`;
- max residual `2e-16` after polishing;
- balanced `max|w| = 0.78`, norm 4.2;
- Jacobian rank 120 of 135 variables, so the kernel equals the gauge
  dimension 15 (`5 x 3` torus plus 3 ancilla scales, minus the 3 GHZ
  weights);
- 1 of 5 restarts;
- a re-evaluation with a separate engine, summing over all 105 perfect
  matchings of `K_8` with zero ancilla–ancilla weights, gives pure words
  `1, 1, 1` and max mixed `|T| = 2.4e-16` (`c61x/crosscheck53.py`).

The structure of the point (as read numerically):

- Each ancilla has unit rows of three distinct colours at three distinct
  vertices, as (AK) demands.
- Vertex 0 meets the three ancillas in a permutation pattern of single
  entries.
- Vertex 4 has three full ancilla rows of equal modulus.
- All `B` blocks have rank 3.
- At every vertex the three ancilla rows are independent, so all common
  kernels are 0: no vertex of this point can be restricted further.

Fix the torus so that the nine single-entry ancilla rows become `1` and the
GHZ weights stay `1` (`c61x/gauge53.py`).  Then several `B` entries vanish
and several equal `1/6` to six digits, which suggests an exact algebraic
point.  No exact form was sought.  `D(5,3)` is not a Krenn–Gu class: it
has three one-mode vertices.

**Consequence.**  The exclusion `D(5,3) = ∅`, which would give `Z = B` in
C_{6,1}, is false (numerically).  The emptiness of the class reached by
restricting a single coloured vertex to its ancilla kernel cannot exclude
C_{6,1}.

### 4.2 Two-colour residues are realizable  [EXACT]

If `S ⊆ Z` kills a colour, the restricted target has at most two colours.
Two-colour GHZ targets with pairwise non-adjacent ancillas are realized
exactly by an even cycle that alternates the two colours.  For example, take
the 6-cycle `a-1-2-b-3-4-a` with perfect matchings `{a1, 2b, 34}` (colour 0)
and `{12, b3, 4a}` (colour 1).  It has exactly those two perfect matchings,
so its tensor is `|0000> + |1111>`.  The same works for any number of
non-adjacent ancillas spaced along a cycle.

So restrictions at vertices of `Z` yield no contradiction by themselves.

### 4.3 KR1, and the end of the method

**Lemma KR1  [EXACT, using Section 5].**  In every C_{6,1} configuration,
`|B - Z| <= 1`.

*Proof.*

1. Suppose `s, s' ∉ Z`.  Restrict them to full-support `v ∈ K_s` and
   `v' ∈ K_s'`.
2. Write `p_f`, `q_f` for their contracted rows and `c_S = v^T W_ss' v'`.
   In the restricted configuration `a` and `b` are always matched into
   `F = B - {s, s'}`.  The other two vertices `k, k'` of `F` are matched
   in one of two ways:
   - to each other, while `ss'` is an edge: this gives `c_S W_kk'`;
   - to `s` and `s'`: this gives `p_k q_k'^T + q_k p_k'^T`.
3. So the restricted tensor is `Σ ℓ_i m_j y_k^T M_kk' y_k'` with
   `M_kk' = c_S W_kk' + p_k q_k'^T + q_k p_k'^T`.  This is the tensor of a
   C_{4,1} configuration with blocks `M`, rows `r_f, s_f` and no `ab`
   edge.  Its target is `GHZ(4,3)` with weights `μ_c v[c] v'[c] != 0`.
4. That contradicts `C_{4,1} = ∅` (Section 5).  ∎

| restricted set | restricted class | status | consequence for C_{6,1} |
|---|---|---|---|
| one `s ∉ Z` | `D(5,3)` | nonempty [NUMERIC] | GCK only |
| two `s, s' ∉ Z` | C_{4,1} with blocks `M` | empty [EXACT, Section 5] | KR1: `|B - Z| <= 1` |
| three | `Per_3` image | empty [EXACT] | KR3: `|B - Z| <= 2` (superseded by KR1) |
| four | rank-2 form | empty unless the profile kills | KR2 |
| any `S ⊆ Z` killing a colour | two-colour target | nonempty [EXACT] | none |

So kernel restriction ends at KR1 + KR2 + GCK.  That is a structural
constraint, not a contradiction.

- After KR1 at most one vertex can be restricted with all colours alive.
- That restriction lands in a nonempty class.
- Every other restriction kills a colour and lands in a realizable
  two-colour class.

## 5. C_{4,1} = ∅  [EXACT, computer-assisted]

**Theorem C41.**  Take four three-colour vertices with arbitrary complex
`3 x 3` blocks and two one-colour vertices `a`, `b` with arbitrary rows and
no `ab` edge.  No such configuration has matching tensor `GHZ(4,3)` with
three nonzero weights.

**Why it matters (calibration).**  Lemma 5 one order down sends every
GHZ(6,3) configuration on six three-colour vertices to C_{4,1}, outside the
pairs whose block is a single nonzero entry.  So Theorem C41 gives:

> every GHZ(6,3) configuration on six three-colour vertices has every block
> equal to a single nonzero entry.

That is the order-6 matrix-unit class.  The six-vertex exclusion already
covers it, so this is not needed for the six-vertex theorem.  It shows that
the pair-contraction route reproduces that theorem modulo its matrix-unit
residual: **the route is faithful one order down.**  Had C_{4,1} been
nonempty, the route would have been suspect at order 8 as well.

*Proof.*

1. **(AK)**  By the hyperplane-annihilation theorem (`m = 4`), restricting
   every vertex to the kernel of `a`'s row kills every channel.  So, for
   each colour `c`, `a` has a vertex `z_c` with `r_{z_c}` a nonzero multiple
   of `e_c`, and these vertices are distinct.  The same holds for `b`, with
   vertices `w_c`.
2. **Normalization.**  Relabel so that `z_c = c`, and scale by the torus so
   that `r_c = e_c` and `r_3 = ρ` is arbitrary.  The rows of `b` are
   `s_{w_c} = β_c e_c` for an injective `w`, and an arbitrary `σ` at the
   remaining vertex `u`.
   - Torus scalings that are still free, together with one global scaling
     of `b` (which rescales the weights), set further nonzero entries
     to 1.
   - Every other nonzero entry becomes an independent nonzero symbol
     (`stratum()` in the script).
   - The strata are given by `w` (24 choices) and the supports of `ρ` and
     `σ` (8 each), 1536 in all.  Simultaneous permutation of the colours
     and of vertices 0–2 reduces them to 292 orbits.
3. **Linearity.**  Each perfect matching uses exactly one `B`–`B` edge, so
   the tensor is `L(r, s) vec(W)`.  The pair `p` with complement `{i, j}`
   contributes `C_ij ⊗ W_p`.  Weights `μ_c != 0` for all `c` require, for
   every `c`,
   `e_{cccc} ∈ Im L + span(e_{c'c'c'c'} : c' != c)`.
4. **Certificates.**  For each stratum the script exhibits a colour `c` and
   a dual vector `Λ` such that
   - its entries are rational in the symbols, with monomial denominators;
   - `Λ^T [L | e_{c'c'c'c'}, c' != c] = 0` identically, checked by exact
     multiplication;
   - `Λ[cccc] = monomial · Π f_j`.
5. **Coverage.**  Points with every `f_j != 0` are excluded.  Each
   hypersurface `f_j = 0` is handled recursively: substitute `x = -b/a`
   for a variable in which `f_j = a x + b` is linear with a monomial `a`.
6. **Certificate types.**  Most certificates are rank-one of KR2 type:
   `Λ = λ_0 ⊗ λ_1 ⊗ λ_2 ⊗ λ_3`, with `λ_s ∈ K_s` for the two vertices
   outside a pair `{i, j}` and `λ_i^T C_ij λ_j = 0`.  The others come from a
   fraction-field left-nullspace search.

Result of `python claims/finite/n08/verify_c41_exclusion.py` (about 30 s):

- a self-test of `L` against a generic perfect-matching engine passes;
- 292 orbit representatives, 295 certificate leaves, 79 hypersurface
  branches, 119 fallback nullspace searches;
- `ALL STRATA EXCLUDED: C_{4,1} is empty`.  ∎

**Caveats.**

- The reduction in steps 1–2 is a hand argument.
- The certificate checker was written by the same author as the reduction.
- No independent audit exists.  An independent re-derivation of the
  strata, or an independent checker of the emitted certificates, is the
  natural audit.

**Corroboration [OBSERVATION].**  Before the proof, the numerics were
already consistent with it:

| system | restarts | result |
|---|---|---|
| C_{4,1}, unbalanced LM, 3000 evaluations | 8 | costs `8e-11`–`4e-8` at unbalanced `max|w|` 8–50; no quadratic convergence (border signature) |
| C_{4,1}, balanced after every 600-evaluation chunk | 25 | stuck at cost 0.31–0.71 |
| C'_{4,1} (ancilla edge allowed), balanced | 5 | 4 converged to `< 1e-28` |
| `D(4,4)`, balanced | 5 | stuck at 0.42–2.9 |
| `D(5,1)`, balanced | 5 | stuck at 0.42–0.63 |
| `D(3,1)` control | 5 | 5 converged |

## 6. Construction attempts  [OBSERVATION]

All runs used the balanced LM loop (5 chunks of 600 evaluations), target
GHZ(6,3) with unit weights, `κ = 0`.

| attempt | restarts | best cost |
|---|---|---|
| single-entry ancilla rows, `a = 012012`, `b = 012012` | 4 | 0.50 |
| single-entry ancilla rows, `a = 012012`, `b = 120120` | 4 | 0.50 |
| single-entry ancilla rows, `a = 012---`, `b = ---012` (three neighbours each) | 4 | 0.50 |
| single-entry ancilla rows, `a = 012012`, `b = 201120` | 4 | 0.29 |
| lift of the D(5,3) point, its ancilla 5 → three-colour vertex | 4 | 0.40 |
| same, ancilla 6 | 4 | 0.40 |
| same, ancilla 7 | 4 | 0.70 |

- In the single-entry patterns, the string gives for each `z = 0..5` the
  colour of the single nonzero entry of the ancilla row (`-` means no
  edge).  The `B` blocks are full.
- The lift sets `W_{z,new}` so that contraction with `v = (1,1,1)`
  reproduces the D(5,3) ancilla rows exactly.  It makes the new vertex's
  ancilla rows orthogonal to `v`, adds a random completion of size 0.3, and
  runs LM.  It tests whether the isolated D(5,3) point extends to a C_{6,1}
  point whose `v`-contraction it is.

## 7. Status and the sharper next statement

- **C_{6,1}: OPEN.**  **Φ0: OPEN.**  Its order-4 analogue is false
  [NUMERIC].
- **C_{4,1} = ∅** [EXACT, computer-assisted, unaudited].  The route is
  faithful at order 6.
- **New exact constraints on any C_{6,1} configuration:** KR1
  (`|B - Z| <= 1`), KR2 and GCK.
- **No-go for the emptiness form of the method** [NUMERIC + EXACT]:
  kernel restriction, used through the emptiness of restricted classes,
  cannot exclude C_{6,1} beyond KR1.  Its exact identities (KR2) remain
  usable.
  - The single-vertex step lands in `D(5,3)`, which is nonempty [NUMERIC,
    isolated modulo gauge].
  - Steps at vertices of `Z` land in two-colour targets, which are
    realizable [EXACT].
- **Refuted heuristic.**  A natural uniform extension of the route reads:
  "pairwise non-adjacent ancillas obstruct GHZ(n,3) whenever `n + k >= 6`".
  It fails at `(n, k) = (5, 3)` [NUMERIC].  It holds for every other class
  tested here:
  - `(6,0)`: theorem;
  - `(4,2)` and `(3,3)`: exact;
  - `(4,4)` and `(5,1)`: observation.

**Sharper next statement (one).**

> **(M61)** No C_{6,1} configuration has single-entry ancilla rows (every
> `r_z`, `s_z` zero or a nonzero multiple of a unit vector).

Why this one:

1. **It is the known mechanism.**  It is exactly the class of the PyTheus
   construction with its ancilla edge deleted, and of every design in which
   each ancilla edge carries one colour.
2. **It is finite.**  For single-entry rows, `E_z`, `Z`, (AK), KR1 and the
   support shadow of KR2 are combinatorial.  An exact enumeration
   (`c61x/mono61_filter.py`, scratch) leaves **356 orbit patterns** under
   `S_6 × S_3 ×` (swap `a`, `b`).
3. **It is a test of the missing ingredient.**  On each pattern, the KR2
   identities `diag(g(v)) = h_S(v) C_p` become polynomial equations in the
   `B`-blocks alone (`h_S` is a 4-vertex hafnian).  Excluding a pattern
   therefore needs exactly the simultaneous use of several contractions that
   the no-go calls for.
4. **Either outcome is informative.**  A proof excludes the only known
   mechanism exactly.  An exact witness in M61 is a C_{6,1} witness, an
   escalation item that would refute the route.

## 8. Not done

- **Modular Gröbner / saturation.**  Not run.
  - No Gröbner engine is installed on this host (no Singular, msolve,
    Macaulay2 or Sage), and WSL was avoided per the brief.
  - sympy's `groebner` is not viable at 60–170 variables.
  - No MODULAR evidence is claimed.  The C41 proof used exact linear
    algebra instead, which its linear structure allows.
- **Jacobian rank of the full C_{6,1} map.**  Not computed.  GHZ is a
  limit of matching tensors (the border-point phenomenon), so a
  generic-rank statement could not exclude anything.
- **Support model.**  KR1, KR2 and KR3 were not encoded.  For general rows
  their support shadows are satisfied by full rows (Section 3.4).  For
  single-entry rows they are combinatorial (Section 7).
- **Exact D(5,3) witness.**  Not sought; it is off the parent.

## 9. Frontier

This commit does not edit `docs/current-frontier.md`.

- **Theorem C41** is a new exact result.  It sits on no live proof path:
  the six-vertex exclusion is already a theorem, and C41 calibrates the
  route rather than closing a branch.  Its consumer is KR1, an exact
  constraint inside the still-open C_{6,1} question.
- **KR1, KR2, KR3 and GCK** are constraints inside C_{6,1}.  They close
  no branch.
- **The candidate edge** `C_{6,1} = ∅ -> N8 exclusion` (from the ancilla
  note, not yet integrated) is unchanged.
- **For the integrator.**  When the ancilla note's frontier text update is
  integrated, two clauses may be added to the same row:
  - "the order-6 instance C_{4,1} is empty (exact, computer-assisted,
    unaudited), so the route is faithful at order 6";
  - "kernel restriction pins C_{6,1} to `|B - Z| <= 1` and stops there,
    since D(5,3) is nonempty numerically".
  - Any frontier edit also needs `node scripts/sync-frontier.mjs`.

## 10. Commands and scripts

Committed (both are exact):

- `python claims/finite/n08/verify_c61_kernel_restriction.py`, about 25 s;
  prints `ALL CHECKS PASSED`.
  - It checks the C_{6,1} tensor formula against a generic 8-vertex
    perfect-matching engine (729 words).
  - It replays Lemma KR for all `S` with `|S| <= 4`, the `Per_3` form at
    `|S| = 3` and the rank-2 form (KR2) at `|S| = 4`, on three random
    integer configurations.
  - It checks the slice-span fact.
- `python claims/finite/n08/verify_c41_exclusion.py` (`--verbose` for one
  line per stratum), about 30 s; prints
  `ALL STRATA EXCLUDED: C_{4,1} is empty`.  This is the computational half
  of Theorem C41.

Scratch (session scratchpad, not committed):

- `gconf.py`, `balance.py`, `run_track.py`: the generic LM engine with
  analytic Jacobian, the torus balancing, and the `D(n,k)` searches.
- `c61x/phi4.py`: `Φ(c^4)` in the C'_{4,1} solutions.
- `c61x/inspect53.py`, `c61x/crosscheck53.py`, `c61x/gauge53.py`: the
  D(5,3) point, its Jacobian rank, its independent re-evaluation and its
  gauge-fixed form.
- `c61x/mono_c61.py`, `c61x/lift53.py`: the construction attempts.
- `c61x/c41_monomial.py`, `c61x/c41_param_cert.py`, `c61x/c41_full.py`,
  `c61x/c41_rec.py`: development versions of the C41 check, superseded by
  the committed script.
- `c61x/mono61_filter.py`: the M61 pattern count.

Bounded run ids (`tools/research/run_bounded.py`, run root in the
scratchpad):

- numerics: `c61x-d42`, `c61x-d42e`, `c61x-d44`, `c61x-d53`, `c61x-d51`,
  `c61x-d31`, `c61x-d42-more`;
- construction attempts: `c61x-mono-m1` … `m4`, `c61x-lift-5`, `-6`, `-7`;
- C41: `c61x-c41mono`, `c61x-c41cert`, `c61x-c41rec-test`;
- `c61x-c41full`, `c61x-c41verify-full`, `-v2`, `-v3`: slow development
  versions, stopped by their owner (this session) after being superseded;
- `c61x-c41verify-v4` … `-v6`: the final script;
- `c61x-mono61-z1`: the M61 count.

Short checks (under 60 s) and inspections ran in the foreground.  One longer
run did too: the first unbalanced C_{4,1} search (8 restarts, about 2 min).
It ran outside the runner and exited normally.

All processes launched by this session have exited.
