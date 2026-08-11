# Projectively constant lift: complete four-cell two-open detector

## Status

**Exact conditional characteristic-zero detector theorem.**  Work on the
aligned common-two-row, projectively constant branch of the single-open
consecutive permanent lift.  In the tight four-root cell

```text
q=0,                  r=4,                  |B|=4,    (1)
```

at least one root `i` other than the aligned root `j` has a nonzero
projective two-open row-replacement tensor.  Consequently every nonzero
affine absorption direction at that selected root is detected by the
complete two-open graph tensor.  More precisely, the conclusion holds for
every `i` whose two complementary companion covectors at `j` are linearly
independent.  The rank-two companion frame guarantees at least one such
root; if the three companions are pairwise independent, all three choices of
`i` are detected.

No local transversality assumption on the two physical outside rows is
needed.  The proof first converts collision vanishing into four three-mode
deletion cofactors.  The all-subset Hall hierarchy forces at least three of
those cofactors to vanish unless the detector is nonzero.  That extreme
zero pattern either violates the lifted `a/b` row quotas or forces a common
outside zero `a_u=b_u=0`.  In the common-zero case, a one-coordinate
recolouring makes the remaining three-mode cofactor nonzero, after which
local concision gives the final contradiction.

This completely closes **two-open affine-gauge invisibility** inside the
conditional aligned projective `q=0,r=4` cell.  It does not force the aligned
factorization or projective branch, exclude a hypothetical witness in the
cell, prove fixed-root injectivity, treat `q=0,r>=5` or `q>=1`, or address an
unfactorized outside graph.  Detection of a gauge direction is not a witness
exclusion.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Imported lift and notation

Use the hypotheses and notation of
[`PROJECTIVELY_CONSTANT_SINGLE_OPEN_CONSECUTIVE_PERMANENT_LIFT_AND_COMPANION_FRAME_THEOREM.md`](PROJECTIVELY_CONSTANT_SINGLE_OPEN_CONSECUTIVE_PERMANENT_LIFT_AND_COMPANION_FRAME_THEOREM.md)
and
[`PROJECTIVELY_CONSTANT_LIFT_ROW_QUOTAS_AND_MINIMAL_CELL_TWO_OPEN_DETECTOR_THEOREM.md`](PROJECTIVELY_CONSTANT_LIFT_ROW_QUOTAS_AND_MINIMAL_CELL_TWO_OPEN_DETECTOR_THEOREM.md).
Thus

```text
Omega=R disjoint-union B,
R={i,j,s,t},           |B|=4,                          (2)

W_uv=a_u tensor b_v+b_u tensor a_v,
b_u=h_(j,u),
W_ju(y,-)=eta_j(y)b_u,
eta_j(x_j)=1.                                           (3)
```

On `B^+=B disjoint-union {j}`, the complete single-open equation is

```text
P_5(hat h_i,hat h_s,hat h_t,hat a,hat b)
 =sum_(c=0)^2 bar X_c e_c^(tensor B^+),
bar X_0 bar X_1 bar X_2!=0.                            (4)
```

The new-column values are

```text
hat h_v|_j=ell_(j,v),       hat a|_j=eta_j,
hat b|_j=0,                 v in R-{j},                (5)
```

and the companion frame satisfies

```text
ell_(j,v)(x_j)=0,
span{ell_(j,i),ell_(j,s),ell_(j,t)}=Ann(x_j),
dim Ann(x_j)=2.                                         (6)
```

On the projectively constant branch the complete two-open coefficient at
distinct roots `i,j` is

```text
C_ij(z)=sum_(v in R-{i,j}) ell_(j,v)(z) A_(i,j;v),    (7)

A_(i,j;v)=P_4(
  (h_w)_(w in R-{i,j,v}),a,a,b).                      (8)
```

There is no factorial divisor because `q=0`.  The full affine variation is

```text
delta T_ij(y,z)=tau kappa_i(y) C_ij(z).               (9)
```

The lifted repeated-row quotas give

```text
p_a>=2,                 p_b>=3,                        (10)
```

where `p_a,p_b` count nonzero covectors on `B`.

All spaces and covectors are over a characteristic-zero field `K`.

## 2. Quotienting a four-mode collision

For each outside mode `u`, define

```text
S_u=span{a_u,b_u},       rho_u=dim S_u<=2,             (11)
```

and let `pi_u:L_u^* -> L_u^*/S_u` be the quotient map.  Define the
three-mode deletion cofactor

```text
Q_u=P_3(
  (a_v)_(v in B-{u}),
  (a_v)_(v in B-{u}),
  (b_v)_(v in B-{u})).                                (12)
```

### Lemma 1 (collision quotient identity)

For every row family `h=(h_u)_(u in B)`,

```text
(pi_u tensor id_(B-{u})) P_4(h,a,a,b)
 =pi_u(h_u) tensor Q_u.                               (13)
```

Consequently, if `P_4(h,a,a,b)=0` and `Q_u!=0`, then

```text
h_u in S_u.                                           (14)
```

### Proof

The labelled permanent expansion is

```text
P_4(h,a,a,b)
 =2 sum_(v!=w)
     h_v tensor b_w tensor
     (tensor_(z in B-{v,w}) a_z).                     (15)
```

In every term with `v!=u`, the factor at mode `u` is either `a_u` or
`b_u`, so `pi_u` kills it.  The terms with `v=u` are exactly `h_u` tensored
with the three-mode permanent (12).  This proves (13).  Over a field, a
tensor product of two nonzero vectors is nonzero, so (14) follows.

## 3. Hall incidence forces three zero deletion cofactors

Choose independent companions

```text
ell_(j,s), ell_(j,t),                                  (16)
```

and let `i` be the complementary root.  Suppose for contradiction that
`C_ij=0`.  Independence in (16), including after restriction to
`ker eta_j`, gives

```text
P_4(h_t,a,a,b)=0,
P_4(h_s,a,a,b)=0.                                     (17)
```

Put

```text
Z={u in B:Q_u=0}.                                     (18)
```

For `u notin Z`, Lemma 1 puts both `h_(s,u)` and `h_(t,u)` in `S_u`.

Apply the all-subset kernel Hall theorem to the four lifted source rows

```text
I={hat h_s,hat h_t,hat a,hat b}.                      (19)
```

For each target colour, its coordinate axis belongs to the span of the rows
in (19) at at least four of the five modes.  Thus there are at least

```text
3*4=12                                                (20)
```

axis-mode incidences.

At mode `j`, (16), (5), and `eta_j(x_j)=1` show that the rows in (19) span
the full three-dimensional local dual.  At `u notin Z`, their span is
exactly `S_u`, of dimension `rho_u`; at `u in Z`, its dimension is at most
three.  A `d`-dimensional subspace contains at most `d` of the three
independent coordinate axes.  Hence Hall gives the capacity inequality

```text
12 <= 3 + sum_(u notin Z) rho_u + 3|Z|.               (21)
```

### Lemma 2 (zero-set size)

Under (17),

```text
|Z|>=3.                                               (22)
```

### Proof

If `Z` were empty, the right side of (21) would be at most
`3+4*2=11`.

If `Z={w}`, equation (21) forces `rho_u=2` at all three modes `u!=w`.
At those modes, complete `(a_u,b_u)` to local bases.  In the induced product
basis, `Q_w/2` is the sum of the three distinct basis words having `b` at
one mode and `a` at the other two.  It is nonzero, contradicting `w in Z`.

Suppose `Z={u,v}` and write the remaining modes as `s,t`.  Equation (21)
forces `rho_s+rho_t>=3`; relabel so that `rho_s=2` and `rho_t>=1`.
Flatten `Q_u=0` at the independent pair `a_s,b_s`.  The coefficients of
`b_s` and `a_s`, respectively, give

```text
a_v tensor a_t=0,
b_v tensor a_t+a_v tensor b_t=0.                      (23)
```

Likewise `Q_v=0` gives

```text
a_u tensor a_t=0,
b_u tensor a_t+a_u tensor b_t=0.                      (24)
```

If `a_t!=0`, equations (23)--(24) force
`a_u=b_u=a_v=b_v=0`, so `Q_s=0`.  If `a_t=0`, then `b_t!=0` because
`rho_t>=1`; the second equations force `a_u=a_v=0`, and again `Q_s=0`
because all three `a` factors on `B-{s}` vanish.  Both cases contradict
`s notin Z`.  Therefore `|Z|` cannot be two, proving (22).

## 4. Extreme deletion vanishing forces a common zero

### Lemma 3 (common-zero reduction)

Under (17), some outside mode `w` satisfies

```text
a_w=b_w=0.                                            (25)
```

### Proof

Assume no common zero exists.  First suppose `rho_t=2` at some mode `t`.
By (22), choose distinct `u,v in Z-{t}`.  Flatten `Q_u=0` at the independent
pair `a_t,b_t`.  If `p,q` are the other two modes in `B-{t,u}`, the
coefficient equations are

```text
a_p tensor a_q=0,
b_p tensor a_q+a_p tensor b_q=0.                      (26)
```

One of `a_p,a_q` is zero.  Because there is no common zero, its corresponding
`b` is nonzero, and the second equation forces the other `a` to be zero as
well.  Repeating with `Q_v=0` shows

```text
a_z=0                  for every z in B-{t}.           (27)
```

Thus `p_a<=1`, contradicting the lifted quota `p_a>=2` in (10).

It follows that `rho_u<=1` at every outside mode.  Apply the all-subset Hall
theorem again, now to the two lifted rows `{hat a,hat b}`.  Every target
coordinate axis must lie in their span at two modes, requiring six
axis-mode incidences.  Their span has dimension at most one at each outside
mode and is the line generated by `eta_j` at mode `j`, so at most five
incidences are possible.  This contradiction proves (25).

## 5. The common-zero boundary also detects

Fix a common-zero mode `w` from (25), and put `U=B-{w}`.

### Lemma 4 (the surviving deletion cofactor is nonzero)

```text
Q_w=P_3(a|_U,a|_U,b|_U)!=0.                           (28)
```

### Proof

The lifted row `hat b` vanishes at both `w` and `j`, so its only possible
nonzero modes are the three modes of `U`.  The singleton tricolour-cover
theorem applied to (4) forces a relabelling

```text
U={u_0,u_1,u_2},
b_(u_c)=beta_c e_c^*,             beta_c!=0.          (29)
```

Assume `Q_w=0`.  Its labelled expansion is

```text
Q_w/2
 =b_(u_0) tensor a_(u_1) tensor a_(u_2)
  +a_(u_0) tensor b_(u_1) tensor a_(u_2)
  +a_(u_0) tensor a_(u_1) tensor b_(u_2).             (30)
```

If one `a_(u_c)` vanished, (30) and the nonzero corresponding `b_(u_c)`
would force another `a` to vanish.  Since also `a_w=0`, this would give
`p_a<=1`, contradicting (10).  Hence all three `a` covectors on `U` are
nonzero.

Flattening (30) at each mode now shows that `a_(u_c)` is proportional to
`b_(u_c)`: a selector killing `a_(u_c)` but not `b_(u_c)` would otherwise
leave the nonzero product of the other two `a` covectors.  Thus both `a` and
`b` evaluate on the constant outside input `e_c` only at `u_c`.

Evaluate (4) with every mode of `B` set to `e_c` and mode `j` first set to
`e_c`.  The `b` row is forced to `u_c`, the `a` row is forced to `j`, and
the three persistent rows occupy `B-{u_c}`.  The coefficient is

```text
eta_j(e_c) beta_c K_c=bar X_c!=0,                    (31)

K_c=P_3(h_i,h_s,h_t;B-{u_c})
    evaluated on the constant colour c.              (32)
```

Change only mode `j` to `e_d`, `d!=c`.  The same unique row-type assignment
has coefficient

```text
eta_j(e_d) beta_c K_c.                                (33)
```

The target word is mixed, so (33) is zero.  Equation (31) makes
`beta_c K_c` nonzero, hence `eta_j(e_d)=0`.  Choosing `c!=d` contradicts
the nonvanishing of `eta_j(e_d)` forced by (31) with colour `d`.  Therefore
`Q_w!=0`.

### Lemma 5 (local concision contradiction)

The detector coefficient `C_ij` cannot vanish.

### Proof

If it vanished, (17), Lemma 1, `S_w={0}`, and Lemma 4 would give

```text
h_(s,w)=h_(t,w)=0.                                    (34)
```

At mode `w`, the five source rows of (4) would then have values

```text
h_(i,w), 0, 0, 0, 0.                                 (35)
```

Any permanent restriction lies at a target mode in the span of the source
covectors in that column.  Equation (35) therefore gives local flattening
rank at most one.  The weighted diagonal target in (4) has local flattening
rank three because all three weights are nonzero.  This is a contradiction.

## 6. Complete four-cell detection

### Theorem 6 (aligned projective `q=0,r=4` detector)

In the cell (1), choose any independent companion pair in (6) and open the
complementary root `i`.  Then

```text
C_ij!=0.                                              (36)
```

Consequently every nonzero affine absorption direction at that root is
detected by the complete two-open tensor.  At least one such root exists.
If the three companions are pairwise independent, the conclusion holds for
all three non-aligned roots.

### Proof

Assuming `C_ij=0` gives (17).  Lemmas 2 and 3 force a common-zero mode.
Lemmas 4 and 5 then contradict the complete lifted diagonal restriction.
Thus (36) holds.  Equation (9) is a tensor product of the nonzero detector
with any nonzero absorption covector, proving detection.  The companion frame
has rank two, so it contains an independent pair; pairwise independence lets
the same argument be repeated after each complementary deletion.

### Detection is not fixed-root injectivity

The proof shows that the map

```text
z |-> sum_(v in R-{i,j}) ell_(j,v)(z) A_(i,j;v)       (37)
```

is nonzero.  It does not prove that the two replacement tensors are linearly
independent, so (37) may have rank one on the effective companion plane.

## 7. Exact frontier

The new content is:

```text
collision quotient by span(a_u,b_u):                 EXACT Q_u FACTOR;
invisible companion-basis deletion cofactors:         AT LEAST THREE ZERO;
extreme zero pattern without a common a/b zero:        EXCLUDED;
common a/b zero with remaining Q_w zero:               EXCLUDED;
common a/b zero with two collision rows vanished:      LOCALLY NONCONCISE;
aligned projective q=0,r=4, at least one root:         TWO-OPEN DETECTED;
pairwise-independent companions in that cell:          EVERY ROOT DETECTED;
fixed-root detector map injective:                     UNKNOWN;
aligned q=0,r>=5 or q>=1 transport:                    UNKNOWN;
unfactorized higher-surplus detector:                  UNKNOWN;
existence or exclusion of a witness in this cell:      UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.          (38)
```

The all-subset Hall hierarchy is imported from
[`ARBITRARY_PERMANENT_KERNEL_DELETION_HIERARCHY.md`](ARBITRARY_PERMANENT_KERNEL_DELETION_HIERARCHY.md).
The complete lift, companion frame, row quotas, and two-open formula are
imported from the owners linked above.  The collision quotient, zero-set
classification, common-zero reduction, recolouring, and local-concision
closure are proved here.  The theorem has not been formalized in Lean.
The preserved line-by-line scope and hostile boundary checks are recorded in
the
[`2026-08-11 adversarial review`](../../docs/audits/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_FOUR_CELL_REVIEW_2026-08-11.md).

## Replay

Run from repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_complete_four_cell_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_complete_four_cell_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_complete_four_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_complete_four_cell_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_complete_four_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_complete_four_cell_detector.py
```

The primary verifier checks all four symbolic quotient slices, the
three-transverse nonvanishing certificate, the Hall-capacity arithmetic, the
two-zero flattening identities, all nine common-zero pure/mixed `P_5`
coefficients, and the local rank mismatch.  The independent no-import audit
instead uses a recursive permanent, exact integer quotient ledgers, a bounded
normalized zero-pattern census, direct common-zero coefficients, and separate
axis-capacity bookkeeping.  These are bounded convention and falsification
checks.  The characteristic-zero proof for every field instance in the
stated cell is the written quotient, Hall, flattening, recolouring, and
concision argument above.
