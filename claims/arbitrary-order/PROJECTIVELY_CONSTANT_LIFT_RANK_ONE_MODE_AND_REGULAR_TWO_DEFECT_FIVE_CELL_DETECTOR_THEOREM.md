# Projectively constant lift: rank-one mode and regular two-defect five-cell detector

## Status

**Exact conditional characteristic-zero detector theorem.**  Work in the
aligned common-two-row, projectively constant tight cell

```text
q=0,                  r=5,                  |B|=5.    (1)
```

For each outside mode put

```text
S_u=span(a_u,b_u),
D={u in B:dim S_u<=1}.                                (2)
```

Call a mode in `D` **regular** when both `a_u` and `b_u` are nonzero, hence
nonzero proportional covectors.  Then at least one non-aligned root has a
nonzero complete two-open detector in either of the following new strata:

1. `|D|=1`, with no nonvanishing assumption at the unique defective mode;
2. `|D|=2` and at least one of the two defective modes is regular.

Together with the complete locally transverse theorem (`D` empty), this
proves detection whenever there is at most one arbitrary local defect, or
there are exactly two defects and at least one is regular.  The proof covers
every rank-two companion configuration and every root quotient-support
pattern in those strata.

This remains conditional cell detection.  It does not derive the aligned
factorization or projective shore, exclude a witness, prove fixed-root
injectivity, close the case of two one-sided/zero defects or three or more
defects, treat `q=0,r>=6` or `q>=1`, or address an unfactorized outside
graph.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Imported five-cell system

Use the notation and hypotheses of the
[`complete transverse five-cell theorem`](PROJECTIVELY_CONSTANT_LIFT_COMPLETE_TRANSVERSE_FIVE_CELL_TWO_OPEN_DETECTOR_THEOREM.md).
The four non-aligned roots are

```text
P={1,2,3,4}.                                          (3)
```

Their companion covectors span a plane:

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
#{u:h_(p,u)!=0}>=3.                                  (6)
```

For an unordered pair `{p,q}` define

```text
B_pq=P_5(h_p,h_q,a,a,b),                              (7)
```

and for a mode `u` define the retained collision tensor

```text
R_(p,u)=P_4(h_p,a,a,b;B-{u}).                         (8)
```

The four projective two-open coefficients are

```text
C_i=sum_(v in P-{i}) ell_v tensor B_(P-{i,v}).        (9)
```

At mode `u`, quotienting (7) by `S_u` gives the imported exact identity

```text
(pi_u tensor id)B_pq
 =pi_u(h_(p,u)) tensor R_(q,u)
  +pi_u(h_(q,u)) tensor R_(p,u).                     (10)
```

All spaces and covectors are over a characteristic-zero field `K`.

## 2. A four-active rank-one mode detects for every companion frame

Fix a mode `u in D` and abbreviate

```text
Q_u=(K^3)^*/S_u,
v_p=pi_u(h_(p,u)),
r_p=R_(p,u).                                         (11)
```

### Lemma 1 (rank-one companion trapping)

Suppose

```text
r_p!=0                         for every p in P.      (12)
```

If all four tensors `C_i` vanish, then

```text
dim span{v_1,v_2,v_3,v_4}<=1.                        (13)
```

### Proof

The exact companion classification has three cases.

#### Good frame

Every pair tensor `B_pq` is zero.  Choose an index `p`.  If `v_p=0`, then
(10) and `r_p!=0` force every `v_q=0`.  If `v_p!=0`, the zero equation

```text
v_p tensor r_q+v_q tensor r_p=0                     (14)
```

and nonvanishing of both retained tensors make every `v_q` proportional to
`v_p`.  Thus (13) holds.

#### Zero companion

If `ell_k=0`, collective invisibility forces

```text
B_kq=0                         for every q!=k.        (15)
```

The same argument applied to the three equations centered at `k` gives
(13).  This also covers two zero companions.

#### Balanced frame

There is a partition

```text
P={p,q} disjoint-union {s,t}                         (16)
```

into two nonzero companion lines.  The tensor kernel of the companion map
has the exact form

```text
B_pq=B_st=0,
the four cross-pair tensors are fixed nonzero
scalar multiples of one tensor T.                   (17)
```

Indeed, write the two companion lines as
`ell_p=A_p e,ell_q=A_q e` and `ell_s=B_s f,ell_t=B_t f`, with all four
scalars nonzero.  The `e` and `f` components of `XL=0` first kill the two
within-pair entries.  The remaining four scalar equations leave one free
cross entry and express the other three as nonzero scalar multiples of it.
The complement permutation relating `X` to the `B_pq` preserves cross pairs,
so the same one-tensor-line statement is exactly (17).

From the two zero-pair equations and (12), each of the pairs `{v_p,v_q}`
and `{v_s,v_t}` spans at most one line.  If either pair is zero, (13)
follows.  Otherwise there are nonzero scalars `lambda,mu` such that

```text
v_q=lambda v_p,       r_q=-lambda r_p,
v_t=mu v_s,           r_t=-mu r_s.                  (18)
```

Suppose `v_p,v_s` were independent.  Then

```text
A=v_p tensor r_s,       E=v_s tensor r_p             (19)
```

would be independent tensors: selectors on `Q_u` isolate the nonzero
factors `r_s,r_p`.  But (10) gives

```text
(pi_u tensor id)B_ps=A+E,
(pi_u tensor id)B_pt=mu(-A+E).                       (20)
```

Equation (17) requires the two displayed tensors to be proportional with a
fixed nonzero proportionality scalar.  Comparing the independent
coefficients of `A,E` would make that scalar simultaneously `mu` and
`-mu`, impossible in characteristic zero.  Hence `v_p,v_s` are dependent,
and (13) follows in the balanced case as well.

### Theorem 2 (four-active dependent-mode detector)

If a mode `u in D` satisfies (12), then some coefficient `C_i` is nonzero.

### Proof

If every `C_i` vanished, Lemma 1 would put all four root covectors at mode
`u` in the inverse image of one quotient line.  Since `b_u in S_u`, the
five source rows of (5) would lie locally in a space of dimension at most

```text
dim S_u+1<=2.                                         (21)
```

Every permanent tensor has local flattening image inside the span of its
source covectors.  The right side of (5) has local flattening rank three
because all three weights are nonzero.  This contradiction proves the
theorem.

## 3. A sharp four-mode collision extension

The transverse four-mode theorem proves injectivity of

```text
L_(a,b):h |-> P_4(h,a,a,b)                           (22)
```

when all four local pairs are independent.  The following exact extension
handles one regular dependent mode.

### Lemma 3 (one-dependent-mode collision classification)

Assume `a_i,b_i` are independent at three of four modes and dependent at
the remaining mode `0`.  Then (22) is injective **if and only if** both
`a_0` and `b_0` are nonzero.

### Proof of injectivity

When both are nonzero, choose local bases so that

```text
a_0=e_0^*,       b_0=lambda e_0^*,       lambda!=0,  (23)
a_i=e_0^*,       b_i=e_1^*                 (i=1,2,3).
```

Write

```text
h_0=x_0 a_0+y_0 c_0+z_0 d_0,
h_i=x_i a_i+y_i b_i+z_i c_i.                         (24)
```

In the labelled expansion

```text
P_4(h,a,a,b)
 =2 sum_(i!=j) h_i tensor b_j tensor
    (tensor_(k notin {i,j}) a_k),                    (25)
```

coordinates with one `c` or `d` factor first give

```text
y_0=z_0=z_1=z_2=z_3=0.                               (26)
```

Coordinates with `b` at two of the three transverse modes give

```text
y_i+y_j=0                    (1<=i<j<=3),             (27)
```

so characteristic zero gives every `y_i=0`.  Put

```text
S=x_1+x_2+x_3.                                       (28)
```

The coordinate with `b` only at transverse mode `i` gives

```text
x_0+S-x_i=0,                                         (29)
```

while the pure-`a` coordinate gives `lambda S=0`.  Hence `S=0`, every
`x_i=x_0`, and `0=S=3x_0`.  Thus all `x_i=0`, proving injectivity.

### Sharpness

If one or both special covectors vanish, (22) has an exact nonzero kernel.
With the three transverse modes labelled `1,2,3`:

```text
a_0!=0, b_0=0:
    h_0=-2a_0,       h_1=a_1, h_2=a_2, h_3=a_3;

a_0=0, b_0!=0:
    h_1=-a_1,        h_2=a_2, h_0=h_3=0;

a_0=b_0=0:
    h_1!=0 arbitrary, h_0=h_2=h_3=0.                (30)
```

Direct substitution in (25) gives zero in every case.  These are ambient
collision kernels, not lifted graph witnesses.

In the normalized chart (23), a `12 x 12` coefficient minor of (22) has
determinant

```text
-24576 lambda^4,                                     (31)
```

which the primary verifier checks as a compact exact certificate.

## 4. At-most-two-defect five-cell detection

### Theorem 4 (one good deletion is sufficient)

Suppose `u in D` and the retained four-mode operator

```text
h |-> P_4(h,a,a,b;B-{u})                             (32)
```

is injective.  Then some `C_i` is nonzero.

### Proof

By (6), no persistent root row can be supported only at `u`; in fact every
root has at least three nonzero modes.  Therefore `h_p|_(B-{u})!=0` for
every `p`.  Injectivity of (32) gives all four inequalities (12), and
Theorem 2 applies.

### Corollary 5 (one arbitrary defect)

If `|D|=1`, some `C_i` is nonzero.  Delete the unique defective mode; all
four retained pairs are transverse, so the imported four-mode collision
theorem makes (32) injective.

### Corollary 6 (two defects with a regular member)

If `|D|=2` and one defect is regular, some `C_i` is nonzero.  Delete the
other defective mode.  The retained configuration has three transverse
pairs and one nonzero proportional pair, so Lemma 3 makes (32) injective.

Combining Corollaries 5--6 with the complete transverse theorem proves
two-open detection throughout

```text
|D|=0;
|D|=1;
|D|=2 with at least one regular defect.               (33)
```

For the selected root, the complete projective variation remains

```text
delta T_ij=tau kappa_i tensor C_i,                    (34)
```

so it is nonzero for every nonzero absorption covector `kappa_i`.

## 5. Exact residual boundary

The new content is

```text
four active deletions at a dependent mode:             DETECTS ALL COMPANIONS;
P4 collision with three transverse plus one regular
dependent pair:                                        INJECTIVE;
one-sided/zero special pair in that P4 collision:       NONINJECTIVE;
aligned projective q=0,r=5 with one arbitrary defect:   DETECTED;
aligned projective q=0,r=5 with two defects and at
least one regular defect:                              DETECTED;
two defects, both one-sided or zero:                    OPEN;
three or more local a/b defects:                        OPEN;
existence or exclusion of a witness in the cell:        OPEN;
fixed-root detector injectivity:                        UNKNOWN;
q=0,r>=6, q>=1, and unfactorized cells:                UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.         (35)
```

The lift, fixed layer, root-row full span, companion classification,
pair-collision quotient, and complete transverse cell are imported at their
existing scopes.  The rank-one companion trapping, sharp one-defect
four-mode collision classification, and at-most-two-defect transport are
proved here.  The theorem has not been formalized in Lean.  Its preserved
scope and adversarial reconstruction are in the
[`2026-08-11 review record`](../../docs/audits/PROJECTIVELY_CONSTANT_LIFT_RANK_ONE_MODE_AND_REGULAR_TWO_DEFECT_FIVE_CELL_REVIEW_2026-08-11.md).

## Replay

Run from repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_rank_one_mode_five_cell_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_rank_one_mode_five_cell_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_rank_one_mode_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_rank_one_mode_five_cell_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_rank_one_mode_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_rank_one_mode_five_cell_detector.py
```

The primary verifier checks the symbolic collision minor, all three sharp
one-sided kernels, 1,220 exact companion frames, representative quotient
trapping systems, and all 3,125 five-mode defect-type words.  The independent
no-import audit uses fraction-free determinants, rational row reduction, a
larger 2,310-frame census, polarized rank-one-subspace checks, and a separate
defect ledger.  These are bounded convention and falsification checks.  The
arbitrary-field implication is the written companion case split, local
flattening proof, and collision-coordinate argument above.
