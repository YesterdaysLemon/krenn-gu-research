# Projectively constant lift: three-activity and mixed degenerate two-defect five-cell detector

## Status

**Exact conditional characteristic-zero detector theorem and boundary
reduction.**  Work in the aligned common-two-row, projectively constant tight
cell

```text
q=0,                  r=5,                  |B|=5.    (1)
```

For each outside mode put

```text
S_u=span(a_u,b_u),
D={u in B:dim S_u<=1}.                                (2)
```

The complete transverse, one-defect, and regular-two-defect strata are
already detected.  Suppose now that `|D|=2` and both defects are degenerate,
meaning at least one of `a_u,b_u` vanishes at each defective mode.  Call the
three possible types

```text
A: a_u!=0, b_u=0          (a-only),
B: a_u=0,  b_u!=0         (b-only),
Z: a_u=b_u=0              (zero).                    (3)
```

Then at least one non-aligned root has a nonzero complete two-open detector
for four of the six unordered type pairs:

```text
AB, AZ, BZ, ZZ.                                       (4)
```

Thus the only two-defect patterns not detected by the current argument are
`AA` and `BB`.  In either surviving pattern, collective invisibility forces
at least two root rows into each of the two retained collision kernels, with
the two inactive sets overlapping but not covering all four roots.  The
common kernel is written explicitly below.

This remains conditional cell detection and a residual classification.  It
does not exclude an `AA` or `BB` witness, close any cell with three or more
defects, prove fixed-root injectivity, treat `q=0,r>=6` or `q>=1`, or address
an unfactorized outside graph.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. Imported five-cell system

Use the hypotheses and notation of the
[`rank-one-mode theorem`](PROJECTIVELY_CONSTANT_LIFT_RANK_ONE_MODE_AND_REGULAR_TWO_DEFECT_FIVE_CELL_DETECTOR_THEOREM.md).
The four non-aligned roots are

```text
P={1,2,3,4}.                                          (5)
```

Their companions span a plane:

```text
span{ell_p:p in P}=Ann(x_j),       dim Ann(x_j)=2.    (6)
```

The fixed five-mode layer is

```text
P_5(h_1,h_2,h_3,h_4,b)
 =sum_(c=0)^2 X_c e_c^(tensor B),
X_0 X_1 X_2!=0.                                      (7)
```

Every persistent root row has full cross-mode span and hence at least three
nonzero local covectors.  For unordered `{p,q}` and a mode `u`, put

```text
B_pq=P_5(h_p,h_q,a,a,b),
R_(p,u)=P_4(h_p,a,a,b;B-{u}).                         (8)
```

The four projective two-open coefficients are

```text
C_i=sum_(v in P-{i}) ell_v tensor B_(P-{i,v}).        (9)
```

At mode `u`, quotienting a pair tensor by `S_u` gives

```text
(pi_u tensor id)B_pq
 =pi_u(h_(p,u)) tensor R_(q,u)
  +pi_u(h_(q,u)) tensor R_(p,u).                     (10)
```

All spaces and covectors are over a characteristic-zero field `K`.

## 2. Three active deletions force a one-line quotient

Fix a dependent mode `u in D` and abbreviate

```text
v_p=pi_u(h_(p,u)),       r_p=R_(p,u),
A_u={p:r_p!=0}.                                         (11)
```

### Lemma 1 (three-root tensor-line obstruction)

Let `a,b,c` be three indices and suppose `r_a,r_b,r_c` are nonzero.  Put

```text
F_pq=v_p tensor r_q+v_q tensor r_p.                  (12)
```

If there are scalars `delta_ab,delta_ac,delta_bc`, at least two nonzero, and
a tensor `T` such that

```text
F_ab=delta_ab T,
F_ac=delta_ac T,
F_bc=delta_bc T,                                     (13)
```

then `v_a,v_b,v_c` span at most one line.

### Proof

Suppose two quotient vectors, say `v_a,v_b`, were independent.  Then
`delta_ab!=0`: otherwise `F_ab=0` and the equality of two nonzero rank-one
tensors would make `v_a,v_b` proportional.  A selector killing `v_a,v_b`
shows that `v_c` lies in their span; otherwise applying it to `F_ab` and
`F_ac` contradicts `r_a!=0`.  Write

```text
v_c=A v_a+B v_b,
gamma=delta_ac/delta_ab,
eta=delta_bc/delta_ab.                               (14)
```

Selectors dual to `v_a,v_b` applied to (13) give

```text
A=eta,        B=gamma,
r_c=gamma r_b-eta r_a,
r_c=eta r_a-gamma r_b.                               (15)
```

Characteristic zero makes `r_c=0`, a contradiction.  Thus no independent
pair exists.

### Lemma 2 (three-activity companion trapping)

If

```text
|A_u|>=3,                                             (16)
```

and all four collective tensors `C_i` vanish, then

```text
dim span{v_1,v_2,v_3,v_4}<=1.                        (17)
```

### Proof

Use the exact companion classification.

#### Good frame

All six `B_pq` vanish.  Center the zero equations (10) at any active root.
Every inactive partner has zero quotient vector, and every active partner
is proportional to the center.  This gives (17).

#### One zero companion

Let `ell_k=0`.  Then

```text
B_kq=0                         for every q!=k,        (18)
```

while the three pair tensors among `P-{k}` lie in one fixed tensor line.
The coefficient pattern on that triangle has at least two nonzero entries,
because the three nonzero companions have a nontrivial relation with at
least two terms.

If `r_k!=0`, center (18) at `k` as in the good case.  Otherwise (16) says
that all three retained tensors away from `k` are nonzero.  Equation (18)
first gives `v_k=0`, and Lemma 1 applied to the remaining triangle gives
(17).

#### Two zero companions

The two remaining companions are independent.  The companion kernel permits
only the pair tensor joining those two nonzero-companion roots to survive;
all other pair tensors vanish.  Among at least three active roots, one has a
zero companion.  Centering its zero incident star gives (17).

#### Balanced frame

For a balanced partition

```text
P={p,q} disjoint-union {s,t},                        (19)
```

the two within-pair tensors vanish and all four cross tensors lie in one
fixed tensor line.  At least one endpoint in each pair is active.  Each
zero-pair equation therefore makes its two quotient vectors span at most one
line.

If exactly three roots are active, the inactive endpoint has zero quotient
vector.  One cross tensor is consequently zero, so all four quotient cross
tensors are zero.  Independent quotient lines for the two pairs would make
the cross tensor between two active endpoints nonzero, a contradiction.  If
all four roots are active, the two-cross-tensor argument from the rank-one
mode theorem gives the same conclusion.  Hence the two pair lines coincide,
proving (17).

### Theorem 3 (three-active dependent-mode detector)

If a dependent mode satisfies (16), then some `C_i` is nonzero.

### Proof

Otherwise Lemma 2 puts all four root covectors at `u` above one quotient
line.  Together with `b_u in S_u`, the five source rows of (7) have local
span at most

```text
dim S_u+1<=2.                                         (20)
```

The permanent restriction therefore has local flattening rank at most two,
whereas the weighted ternary diagonal in (7) has rank three.  This is the
required contradiction.

## 3. Exact one-sided collision kernels

Let one four-mode configuration have three transverse modes `1,2,3` and one
special mode `0`.  Put

```text
Q=P_3(a,a,b;{1,2,3}).                                (21)
```

Local transversality makes `Q!=0`: in local `a/b` bases, any word with `b`
at one chosen mode and `a` at the other two has coefficient two.

### Lemma 4 (the three degenerate kernels)

For

```text
L(h)=P_4(h,a,a,b),                                   (22)
```

the kernels at the three types in (3) are as follows.

1. At an `A` mode,

   ```text
   ker L={lambda(-2a_0,a_1,a_2,a_3):lambda in K}.    (23)
   ```

2. At a `B` mode,

   ```text
   h_0=-gamma b_0,
   h_i=alpha_i a_i+gamma b_i,       i=1,2,3,
   alpha_1+alpha_2+alpha_3=0.                       (24)
   ```

3. At a `Z` mode,

   ```text
   ker L={h:h_0=0}.                                  (25)
   ```

### Proof

For type `A`, direct coefficient comparison in the labelled expansion of
`P_4(h,a,a,b)` kills every component outside the local `a` lines and leaves
the one relation (23).  Equivalently, the collision matrix has rank eleven
and (23) is its displayed nonzero kernel vector.

For type `B`, every nonzero term assigns either `h` or `b` to mode `0`, so

```text
L(h)=h_0 tensor Q+b_0 tensor P_3(h,a,a;{1,2,3}).     (26)
```

Quotienting at mode `0` gives `h_0 in span(b_0)`.  Write
`h_0=-gamma b_0`.  Comparing the one-`b` and pure-`a` words on the three
transverse modes gives exactly (24).

For type `Z`, both `a_0,b_0` vanish, so the only surviving assignment puts
`h` at mode `0`:

```text
L(h)=h_0 tensor Q.                                   (27)
```

Since `Q!=0`, this is (25).

The dimensions of (23)--(25) are respectively `1,3,9`.  They are collision
kernels, not graph witnesses.

## 4. Every two-defect pattern containing a zero mode detects

### Theorem 5 (zero-defect transport)

Suppose the two defective modes are `u,v`, with `u` of type `Z`, and the
remaining three modes transverse.  Then some `C_i` is nonzero, regardless of
whether `v` has type `A`, `B`, or `Z`.

### Proof

At mode `u`, both `a_u,b_u` vanish.  The local flattening rank of (7) is
three, so

```text
dim span{h_(p,u):p in P}=3.                           (28)
```

In particular at least three of those four covectors are nonzero.  Delete
the other defect `v`.  Because the retained set contains the zero mode `u`,
the same assignment argument as (27) gives

```text
R_(p,v)=h_(p,u) tensor P_3(a,a,b;B-{u,v}).           (29)
```

The three-mode factor is nonzero by transversality.  Thus at least three
`R_(p,v)` are nonzero, and Theorem 3 detects.  This closes `AZ`, `BZ`, and
`ZZ`.

## 5. The mixed `AB` pair detects

Let defect `u` have type `A` and defect `v` have type `B`.  Define the
inactive root sets

```text
I_u={p:R_(p,u)=0},       I_v={p:R_(p,v)=0}.           (30)
```

### Lemma 6 (the mixed common kernel is zero)

No nonzero root row family belongs to both retained collision kernels:

```text
ker R_(-,u) intersection ker R_(-,v)={0}.            (31)
```

### Proof

The condition `R_(p,v)=0` sees the `A` mode `u` as its special retained
mode.  By (23), for some `lambda`,

```text
h_(p,u)=-2lambda a_u,
h_(p,t)=lambda a_t                 at all three transverse t.   (32)
```

The condition `R_(p,u)=0` sees the `B` mode `v` as special.  By (24),

```text
h_(p,v)=-gamma b_v,
h_(p,t)=alpha_t a_t+gamma b_t,
sum_t alpha_t=0.                                      (33)
```

At every transverse mode, independence of `a_t,b_t` makes `gamma=0` and
`alpha_t=lambda`.  Then `0=sum_t alpha_t=3lambda`, so characteristic zero
gives `lambda=0`.  Equations (32)--(33) make the whole row family zero.

### Theorem 7 (mixed one-sided two-defect detector)

The `AB` cell has some nonzero `C_i`.

### Proof

Assume collective invisibility.  Theorem 3 forces

```text
|I_u|>=2,              |I_v|>=2.                     (34)
```

Every persistent root row is nonzero by full span, so Lemma 6 makes the two
inactive sets disjoint.  With only four roots, they are complementary pairs.

At every transverse mode, (23) puts the roots in `I_v` on the local `a`
line, while (24) puts the roots in `I_u` inside `span(a_t,b_t)`.  The fixed
row `b_t` is in the same two-plane.  Hence all five source rows of (7) have
local span at most two, contradicting local rank three.  Thus collective
invisibility is impossible.

## 6. Exact same-type residual

Only `AA` and `BB` remain among two degenerate defects.  For either type let
`I_u,I_v` be as in (30).

### Proposition 8 (overlapping double-kernel boundary)

Any collectively invisible `AA` or `BB` system must satisfy

```text
|I_u|>=2,        |I_v|>=2,
I_u intersection I_v!=empty,
P-(I_u union I_v)!=empty.                             (35)
```

### Proof

The size bounds again follow from Theorem 3.  Every root in either inactive
set lies in `span(a_t,b_t)` at all three transverse modes, by (23) or (24).
If `I_u union I_v=P`, then every root row and `b_t` lies in that local
two-plane, contradicting the rank-three fixed layer.  Thus the union is
proper.  Two subsets of a four-element set, each of size at least two, with
proper union must intersect.  This is (35).

The common collision kernels are exact.  In the `AA` case they form the line

```text
h_u=-2lambda a_u,
h_v=-2lambda a_v,
h_t=lambda a_t                  at all transverse t.  (36)
```

In the `BB` case they form the three-dimensional family

```text
h_u=-gamma b_u,
h_v=-gamma b_v,
h_t=alpha_t a_t+gamma b_t,
sum_t alpha_t=0.                                      (37)
```

Equations (35)--(37) are a boundary reduction, not an exclusion.

## 7. Exact residual boundary

The new content is

```text
three active deletions at any dependent mode:          DETECTS ALL COMPANIONS;
exact retained collision kernels at A/B/Z modes:       DIMENSIONS 1/3/9;
two degenerate defects with a zero member:              DETECTED;
mixed a-only / b-only defects:                          DETECTED;
same-type AA or BB defects:                             DOUBLE-KERNEL BOUNDARY;
three or more local a/b defects:                        OPEN;
existence or exclusion of a witness in the cell:        OPEN;
fixed-root detector injectivity:                        UNKNOWN;
q=0,r>=6, q>=1, and unfactorized cells:                UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.         (38)
```

The lift, fixed layer, companion classification, pair quotient, root-row
full span, and previous defect detectors are imported at their existing
scopes.  The three-activity lemma, exact one-sided collision kernels,
zero-defect transport, mixed-kernel exclusion, and same-type crowding
reduction are proved here.  The theorem has not been formalized in Lean.  Its
preserved scope and adversarial reconstruction are in the
[`2026-08-11 review record`](../../docs/audits/PROJECTIVELY_CONSTANT_LIFT_THREE_ACTIVITY_AND_MIXED_DEGENERATE_TWO_DEFECT_FIVE_CELL_REVIEW_2026-08-11.md).

## Replay

Run from repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_three_activity_two_defect_five_cell_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_three_activity_two_defect_five_cell_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_three_activity_two_defect_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_three_activity_two_defect_five_cell_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_three_activity_two_defect_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_three_activity_two_defect_five_cell_detector.py
```

The primary verifier checks all companion degeneracies on exact activity
charts, the three collision kernels, all six two-defect common kernels, the
zero-mode factorization, and the inactive-set ledger.  The independent
no-import audit uses rational elimination, polarized rank-one-subspace
checks, direct labelled permanents, and a separate set census.  These are
bounded convention and falsification checks.  The arbitrary-field result is
the written tensor-line, kernel-intersection, and local-flattening proof
above.
