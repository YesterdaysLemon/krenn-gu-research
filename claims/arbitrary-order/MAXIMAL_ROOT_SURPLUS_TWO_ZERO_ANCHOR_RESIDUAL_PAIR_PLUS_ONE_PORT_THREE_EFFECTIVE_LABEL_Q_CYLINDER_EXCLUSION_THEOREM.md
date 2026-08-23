# Maximum-root surplus-two zero-anchor residual-pair-plus-one-port three-effective-label q-cylinder exclusion theorem

## Status and scope

**Exact characteristic-zero arbitrary-root pointwise exclusion.**  Fix one
`GLS8`-eligible `(Q,A)` chart, one fully supported residual contraction, and
the zero-anchor fibre `omega=0`.  Put

```text
q=a_0 tensor b_1+a_1 tensor b_0 in E_A^*,
p=epsilon_A(q).
```

No target-consistent point has effective support
`Q disjoint-union {u}` for one promoted port `u`, even when `q=0`.  Across
`(A union {u})|(Uhat-{u})`, the zero-`q` source has only two left generators,
while the target has three.  When `q!=0`, quotienting the complete physical
source by the `q tensor V_u^*` cylinder first forces `q` onto one pure
diagonal line.  The rank-one residual factorization of that pure `q` then
forces one at-most-two-dimensional residual shore to contain all three
coordinate axes, a contradiction.

Together with `GLS48`, every target-consistent zero-anchor point on `D(p)` has
at least four effective auxiliary labels.  The proof retains arbitrary
physical complementary decks, including zero and proportional decks, and is
pointwise on every residual-shore, incidence-rank, nuisance-rank, response,
and divisor fibre.  It divides by no response, deck, or chosen minor.

This is `GLS49`.  It does not treat `p=0` outside the displayed support,
exclude four-or-more effective labels, or exclude the other three-label
support types possible when `p=0`.
It does not force full swallow, attach raw escape, produce a selector,
physical response, or named receiver, or close the strategic node.  The
scalar `p` is a root-deck coefficient evaluation, not a named physical
response.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Dependencies and provenance

The owning interfaces are:

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  for `|Uhat|=2r-2>=4` and the exact promoted target equation;
- [`GLS21`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_BASE_SHADOW_ALL_PORT_NUISANCE_COLLAPSE_THEOREM.md)
  and [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md)
  for the complete raw labels and their coefficient slices;
- [`GLS35`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RAW_ROOT_DECK_QUOTIENT_AND_OUTPUT_COEFFICIENT_SEPARATION_NO_GO_THEOREM.md)
  for `q`, `p=epsilon_A(q)`, and the zero-anchor source notation;
- [`GLS36`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_THEOREM.md)
  for the fixed-residual physical target equation and residual--port tensors;
- [`GLS39`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_COMPLETE_PAIRWISE_DIAGONAL_FAMILY_RANK_BOUND_AND_MINIMAL_RAW_SWALLOW_EXCLUSION_THEOREM.md)
  for the auxiliary residual labels; and
- [`GLS48`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TWO_EFFECTIVE_LABEL_ADAPTIVE_CUT_PURE_TARGET_EXCLUSION_THEOREM.md)
  for the unconditional three-effective-label floor.

No external literature claim is used.  The new content is the exact
three-label `q`-cylinder quotient, the pure-`q` forcing lemma, and the
residual-shore contradiction.

## 1. Three-label support on `D(p)`

Retain the `GLS39` auxiliary labels

```text
T=Q disjoint-union Uhat,          Q={q_0,q_1},
Act={t in T:X_t!=0 or Y_t!=0}.                         (1)
```

The residual domains are one-dimensional and

```text
X_(q_s)(1)=a_s,                  Y_(q_s)(1)=b_s,
q=a_0 tensor b_1+a_1 tensor b_0.                       (2)
```

### Lemma 1 (both residual labels are effective on `D(p)`)

If `p!=0`, then `q!=0` and `q_0,q_1 in Act`.  Hence `|Act|=3` would imply

```text
Act=Q disjoint-union {u}                               (3)
```

for one promoted port `u`.

#### Proof

The implication `p!=0 => q!=0` is immediate from `p=epsilon_A(q)`.  If
`q_s` were ineffective, then both `a_s` and `b_s` would vanish, and both
summands in (2) would vanish.  Thus `q=0`, a contradiction.  With both
residual labels active, the third label in a three-element support must be a
promoted port. `square`

## 2. Complete cut source and the `q`-cylinder

Assume (3).  Write

```text
V=V_u,                  R=Uhat-{u},
W_R^*=tensor_(v in R) V_v^*,
E=E_A^*=V_(a_0)^* tensor V_(a_1)^*.
```

Since `|Uhat|>=4`, the right shore `R` is nonempty.  Let

```text
X=X_u:V -> V_(a_0)^*,       Y=Y_u:V -> V_(a_1)^*,

G_s(z)=a_s tensor Y(z)+X(z) tensor b_s
      in E,                 s=0,1,                    (4)
```

and regard each `G_s` as one tensor in `E tensor V^*`.

Across the physical flattening

```text
(A union {u}) | R,                                  (5)
```

the only raw labels whose root coefficients can be nonzero are

```text
Q,             {q_0,u},             {q_1,u}.         (6)
```

The `Q` term is `q tensor H_Uhat`; its left column space in (5) lies in
`Kq tensor V^*`, even when `H_Uhat` is entangled across `u|R`.  Each
residual--port term has the fixed left tensor `G_s` and an arbitrary right
physical deck.  The zero anchor removes the separate top `omega` term.
Therefore the complete source left column space lies in

```text
L=K G_0+K G_1+(Kq tensor V^*)
  subset E tensor V^*.                               (7)
```

This is a containment, not an assertion that any displayed deck or `G_s` is
nonzero.

At a fully supported residual contraction the target is

```text
sum_(c=0)^2 alpha_c d_c tensor w_c,
d_c=r_c tensor e_c^* in E tensor V^*,
w_c=(e_c^*)^(tensor |R|) in W_R^*,                   (8)
```

with every `alpha_c!=0`.  The `w_c` are independent because `R` is nonempty.
Thus equality of source and target implies

```text
d_0,d_1,d_2 in L.                                   (9)
```

Zero, proportional, or cancelling right decks can only shrink the source
column space and do not affect (9).

## 3. Pure `q` forcing

### Lemma 2 (the zero-`q` support branch is impossible)

Under (3) and exact target consistency, `q!=0`.

#### Proof

If `q=0`, then (7) has dimension at most two.  But (8)--(9) put the three
independent tensors `d_0,d_1,d_2` in that space, a contradiction. `square`

### Lemma 3 (exact diagonal columns modulo the `q`-cylinder)

Let `q in E` be nonzero and put

```text
C_q=Kq tensor V^* subset E tensor V^*.
```

Then the classes of `d_0,d_1,d_2` in `(E tensor V^*)/C_q` span

```text
3 dimensions,  if q is not proportional to any r_j;
2 dimensions,  if q is proportional to one r_j.      (10)
```

#### Proof

A relation modulo `C_q` is

```text
sum_i gamma_i r_i tensor e_i^*=q tensor ell           (11)
```

for some `ell in V^*`.  Evaluate the `u` slot at the coordinate vector
`e_k`.  Equation (11) gives

```text
gamma_k r_k=ell(e_k)q.                                (12)
```

If `q` is not on a pure line, (12) forces both scalars to vanish for every
`k`, so the three classes are independent.  If `q` is proportional to
`r_j`, exactly `d_j` lies in `C_q`, while the other two classes remain
independent. `square`

### Corollary 3.1 (`q` is pure under three-label target consistency)

Under (7)--(9), there are scalars and covectors such that each

```text
d_i=lambda_i G_0+mu_i G_1+q tensor ell_i.             (13)
```

Lemma 2 gives `q!=0`.  Modulo `C_q`, the right side of (7) has dimension at
most two.  Lemma 3 therefore forces

```text
q=kappa r_j                                             (14)
```

for some unique colour `j` and nonzero `kappa`.

## 4. Residual-shore contradiction

Form the `3 by 2` factor matrices

```text
A=[a_0 | a_1],              C=[b_1 | b_0],
q=A C^T.                                              (15)
```

Since (14) has matrix rank one, (15) implies

```text
rank A<=1 or rank C<=1.                               (16)
```

Indeed, if both ranks were two, `C^T:K^3->K^2` would be surjective and
`A:K^2->K^3` injective, so their composition would have rank two.

### Theorem 4 (the residual-pair-plus-one-port support is impossible)

There is no exact target-consistent point satisfying

```text
omega=0,                 Act=Q disjoint-union {u}.     (17)
```

#### Proof

By (16), first suppose `rank A<=1`.  Since `q!=0`, in fact

```text
span{a_0,a_1}=K e_j,
e_j in span{b_0,b_1}.                                 (18)
```

For either colour `i!=j`, take representation (13) and define

```text
B_i=lambda_i b_0+mu_i b_1 in span{b_0,b_1}.           (19)
```

Let `P_j` be the projection of the first root-probe factor onto the two
coordinate axes different from `e_j`.  Apply `P_j tensor id` to (13) and
evaluate the port slot at arbitrary `z in V`.  Equations (4), (14), and
(18) kill the `a_s tensor Y` and `q tensor ell_i` terms, leaving

```text
(P_j X(z)) tensor B_i=e_i^*(z) e_i tensor e_i.        (20)
```

Set `z=e_i`.  The right side is nonzero, so equality of simple tensors in
(20) forces `B_i` to be a nonzero multiple of `e_i`.  Doing this for both
colours different from `j`, (18)--(19) put all three independent coordinate
vectors in `span{b_0,b_1}`, whose dimension is at most two.  This is
impossible.

If `rank C<=1`, transpose the whole argument: now
`span{b_0,b_1}=Ke_j`, while `e_j in span{a_0,a_1}`.  Project the second
root-probe factor away from `e_j`; the two remaining representations force
both other coordinate vectors into `span{a_0,a_1}`, the same contradiction.
Thus neither alternative in (16) can occur. `square`

### Corollary 4.1 (four-effective-label floor on `D(p)`)

`GLS48` gives `|Act|>=3` at every target-consistent zero-anchor fully
supported fixed-residual point.  Lemma 1 and Theorem 4 exclude equality on
`D(p)`.
Therefore

```text
omega=0 and p!=0 and exact target consistency
imply |Act|>=4.                                       (21)
```

This conclusion is rank-independent and hence includes every target-
consistent rank-five full-swallow fibre on `D(p)`.  The premise `p!=0`
supplies no named physical response.

## 5. Exact boundary

```text
zero-anchor D(p) target point with <=3 labels:            EXCLUDED;
zero-anchor support Q disjoint-union {u}, any q:          EXCLUDED;
zero-anchor D(p) target point with >=4 labels:            OPEN;
other zero-anchor p=0 target points with exactly 3 labels: OPEN;
rank-five full swallow on D(p), >=4 labels:               OPEN;
ranks six through nine / raw escape / nonzero anchor:     OPEN;
selector, response, synchronization, nuisance, anchor:    NOT SUPPLIED;
arbitrary-root source cover and strategic-node closure:    UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

The smallest continuation is the four-or-more-effective-label `D(p)` target
cell, where more than two residual--port/port--port left tensors survive the
`q`-cylinder quotient, together with the separate `p=0` three-label cell.
Any successor must retain the physical deck coupling and must not infer a
selector, response, or full-swallow source edge from the activity floor.

## Verification boundary

Run the focused exact primary verifier:

```bash
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_residual_pair_plus_one_port_three_effective_label_q_cylinder_exclusion.py
```

It checks the exhaustive three-label support on `D(p)`, builds the exact
`27`-coordinate target columns and `q`-cylinders, replays the quotient ranks
for every pure line and hostile non-pure representatives, and verifies the
rank-two shore obstruction symbolically.

Run the genuinely independent no-import audit:

```bash
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_residual_pair_plus_one_port_three_effective_label_q_cylinder_exclusion.py
```

It uses a custom `F_3` eliminator to exhaust all `9,841` projective `q` lines
in the full nine-dimensional root-probe coefficient space, independently
confirming that exactly the three pure lines have quotient dimension two and
all others dimension three.  It separately audits every support and shore-
orientation case without importing the primary.  The finite-field census is
corroboration; the proof above is characteristic zero.
