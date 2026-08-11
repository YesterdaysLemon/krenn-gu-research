# Projectively constant lift: complete transverse five-cell two-open detector

## Status

**Exact conditional characteristic-zero detector theorem.**  Work in the
aligned common-two-row, projectively constant tight cell

```text
q=0,                  r=5,                  |B|=5,    (1)
```

and assume only that

```text
dim span(a_u,b_u)=2                 for every u in B. (2)
```

Then at least one of the four non-aligned roots has a nonzero complete
two-open detector.  No additional condition on individual companion
covectors, deletion activity, or root-row quotient support is required.

This closes **all companion and root-transversality subcases inside the
locally transverse aligned projective `q=0,r=5` cell**.  The word
"complete" refers only to that conditional cell.  The theorem does not force
(2), exclude a witness, prove fixed-root injectivity, treat `q=0,r>=6` or
`q>=1`, or address an unfactorized outside graph.  The full aligned
`q=0,r=5` local-dependence boundary remains open.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## 1. Imported five-cell data

Use the hypotheses and notation of
[`PROJECTIVELY_CONSTANT_LIFT_FIVE_CELL_COLLECTIVE_COMPANION_AND_ACTIVITY_DETECTOR_THEOREM.md`](PROJECTIVELY_CONSTANT_LIFT_FIVE_CELL_COLLECTIVE_COMPANION_AND_ACTIVITY_DETECTOR_THEOREM.md)
and
[`PROJECTIVELY_CONSTANT_LIFT_FIVE_CELL_PAIR_COLLISION_AND_ALL_COMPANION_DETECTOR_THEOREM.md`](PROJECTIVELY_CONSTANT_LIFT_FIVE_CELL_PAIR_COLLISION_AND_ALL_COMPANION_DETECTOR_THEOREM.md).

Let

```text
P={1,2,3,4}                                            (3)
```

be the non-aligned roots.  Their companion covectors at the aligned root
span a plane:

```text
span{ell_p:p in P}=Ann(x_j),       dim Ann(x_j)=2.    (4)
```

The fixed five-mode layer is

```text
P_5(h_1,h_2,h_3,h_4,b)
 =sum_(c=0)^2 X_c e_c^(tensor B),
X_0 X_1 X_2!=0.                                      (5)
```

Every persistent root row has full cross-mode span, hence at least three
nonzero local covectors:

```text
span{h_(p,u):u in B}=(K^3)^*,
#{u:h_(p,u)!=0}>=3.                                   (6)
```

For an unordered pair `{p,q}` define

```text
B_pq=P_5(h_p,h_q,a,a,b).                              (7)
```

The four projective two-open coefficients are

```text
C_i=sum_(v in P-{i}) ell_v tensor B_(P-{i,v}).        (8)
```

All spaces and covectors are over a characteristic-zero field `K`.

## 2. Strong roots and weak-root trapping

Put

```text
S_u=span(a_u,b_u),
0!=k_u in ker a_u intersection ker b_u.               (9)
```

For a root row `h_p`, define its quotient escape set

```text
E_p={u:h_(p,u)(k_u)!=0}
   ={u:h_(p,u) notin S_u}.                            (10)
```

Call `p` **strong** if `|E_p|>=2` and **weak** if `|E_p|<=1`.

The imported five-mode pair-collision theorem gives:

### Lemma 1 (strong endpoint)

If `p` is strong, then

```text
B_pq!=0                     for every q!=p.           (11)
```

The two quotient escapes supply two common-kernel contractions; (6) supplies
a third nonzero mode.  Four-mode collision injectivity then makes
`g -> P_5(h_p,g,a,a,b)` injective.

The complementary consequence is new.

### Lemma 2 (weak endpoint traps a zero-pair partner)

Suppose `p` is weak and

```text
B_pq=0.                                               (12)
```

Then for every nonescape mode `u notin E_p`,

```text
h_(q,u) in S_u.                                       (13)
```

### Proof

Write

```text
alpha_u=h_(p,u)(k_u),       beta_u=h_(q,u)(k_u).      (14)
```

Contract (12) at `k_u`.  The two `a` assignments and the `b` assignment die,
leaving

```text
P_4(alpha_u h_q+beta_u h_p,a,a,b;B-{u})=0.           (15)
```

At `u notin E_p`, `alpha_u=0`.  Four-mode collision injectivity turns (15)
into

```text
beta_u h_(p,v)=0                  for every v!=u.     (16)
```

By (6), `h_p` is nonzero at at least three modes, so some `v!=u` has
`h_(p,v)!=0`.  Hence `beta_u=0`, which is (13).

### A necessary pairwise scope wall

Root-row support alone does not make every pair tensor nonzero.  In normalized
local bases let `a_u=e_0^*`, `b_u=e_1^*` and put

```text
h=(a,a,-2a,0,0),
g=(a,a,a,-a,0).                                      (17)
```

Both row families have at least three nonzero modes, but

```text
P_5(h,g,a,a,b)=0.                                    (18)
```

This is an exact ambient row-pair kernel, not a lifted graph witness.  It
shows why the proof below must use the full companion-imposed pattern of zero
pairs and local concision, rather than an invalid universal pair-nonvanishing
claim.

## 3. Companion frames force three exact zero patterns

Package the six tensors (7) into the symmetric zero-diagonal matrix

```text
X_iv=B_(P-{i,v})              for i!=v.              (19)
```

Let `L` be the `4 x 2` companion matrix.  All `C_i` vanish exactly when

```text
X L=0.                                                (20)
```

The exact companion classification from the first five-cell theorem gives
three cases.

### Lemma 3 (forced zero-pair patterns)

If every `C_i` vanishes, then one of the following holds.

1. **Good frame.**  Every companion is nonzero and the frame is not a
   balanced `2+2` split.  Then

   ```text
   B_pq=0                         for all six pairs.   (21)
   ```

2. **Zero companion.**  For every `k` with `ell_k=0`,

   ```text
   B_kq=0                         for every q!=k.     (22)
   ```

3. **Balanced frame.**  There is a partition

   ```text
   P={p,q} disjoint-union {s,t}                       (23)
   ```

   into two proportional nonzero companion pairs, and

   ```text
   B_pq=B_st=0.                                       (24)
   ```

### Proof

In the good case, the companion map is injective, so (20) gives `X=0` and
therefore (21).

Suppose `ell_k=0`.  Among the other three companions choose independent
`ell_a,ell_b`; write the remaining index as `c`.  The equation `C_c=0`
has independent companion components

```text
ell_a tensor B_kb+ell_b tensor B_ka=0,               (25)
```

so `B_ka=B_kb=0`.  Then `C_a=0` reduces to the nonzero companion `ell_b`
times `B_kc`, proving (22).  This includes the case of two zero companions.

For a balanced partition, decompose the companion plane into its two
projective lines.  In `C_p=0`, the component on the line of `ell_q` is
exactly `ell_q tensor B_st`, so `B_st=0`.  The symmetric argument in `C_s`
gives `B_pq=0`.

## 4. Complete locally transverse five-cell detection

### Theorem 4 (complete transverse `q=0,r=5` detector)

Under (1)--(10), at least one coefficient `C_i` in (8) is nonzero.
Consequently every nonzero affine absorption direction at at least one
non-aligned root is detected by the complete two-open graph tensor.

### Proof

Assume all four `C_i` vanish and use Lemma 3.

#### Good frame

All six pairs vanish.  If any root were strong, Lemma 1 would contradict one
of its zero pairs.  Hence all four roots are weak.  Each escape set has size
at most one, so

```text
|E_1 union E_2 union E_3 union E_4|<=4<|B|.          (26)
```

Choose a mode `u` outside that union.  Every root row and `b_u` lies in the
two-plane `S_u`.  The local flattening rank of the left side of (5) is at
most two, contradicting the rank-three weighted diagonal.

#### Zero companion

Let `ell_k=0`.  Equation (22) gives all three pairs incident with `k` zero.
If `k` were strong, Lemma 1 would contradict any one of them.  Thus `k` is
weak.  Choose any `u notin E_k`; such a mode exists.  Lemma 2 applied to all
three zero pairs puts every other root row in `S_u`.  The row `h_(k,u)` and
`b_u` already lie there.  Again the local source span is at most two,
contradicting (5).

#### Balanced frame

Use the partition (23).  The zero pair `B_pq` and Lemma 1 force both `p,q`
to be weak; otherwise the strong endpoint would make the pair nonzero.
Likewise `B_st=0` forces both `s,t` weak.  The same pigeonhole (26) supplies
a mode where all four root rows and `b` lie in `S_u`, contradicting local
rank three.

Every companion frame has been exhausted, so some `C_i!=0`.  The complete
projective variation at that root is

```text
delta T_ij=tau kappa_i tensor C_i,                    (27)
```

which is nonzero for every nonzero absorption covector `kappa_i`.

## 5. Exact residual boundary

The new content is

```text
weak zero-pair endpoint traps its partner off one mode: PROVED;
good companion frame in locally transverse q=0,r=5:    DETECTED;
zero-companion frame in locally transverse q=0,r=5:    DETECTED;
balanced 2+2 frame in locally transverse q=0,r=5:      DETECTED;
complete locally transverse aligned q=0,r=5 cell:      DETECTED;
pairwise full-support nonvanishing shortcut:            FALSE;
local a/b dependence in aligned q=0,r=5:               OPEN;
existence or exclusion of a witness in the cell:        OPEN;
fixed-root detector injectivity:                        UNKNOWN;
q=0,r>=6, q>=1, and unfactorized cells:                UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.          (28)
```

The lift, fixed layer, companion classification, root-row full span,
four-mode collision inverse, and strong-root pair injection are imported at
their existing scopes.  The weak trapping lemma, forced zero-pattern
transport, and complete transverse five-cell case split are proved here.
The theorem has not been formalized in Lean.  Its preserved line-by-line
scope and adversarial reconstruction are in the
[`2026-08-11 review record`](../../docs/audits/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_TRANSVERSE_FIVE_CELL_REVIEW_2026-08-11.md).

## Replay

Run from repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_complete_transverse_five_cell_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_complete_transverse_five_cell_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_complete_transverse_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_complete_transverse_five_cell_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_complete_transverse_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_complete_transverse_five_cell_detector.py
```

The primary verifier checks the companion classification and every forced
zero mask on an exact frame census, all common-kernel contraction slices,
weak-kernel quotient trapping, the exact pairwise scope-wall model, and the
escape-set pigeonhole.  The independent no-import audit uses rational
elimination, a larger frame census, a recursive permanent, separately
assembled weak charts, and an independent concision ledger.  These are
bounded convention and falsification checks.  The arbitrary-field result is
the written contraction, companion-line decomposition, pigeonhole, and local
flattening proof above.
