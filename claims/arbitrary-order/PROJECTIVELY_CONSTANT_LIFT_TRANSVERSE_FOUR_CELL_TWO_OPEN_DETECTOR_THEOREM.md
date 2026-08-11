# Projectively constant lift: transverse four-cell two-open detector

## Status

**Exact conditional characteristic-zero detector theorem.**  Work on the
aligned common-two-row, projectively constant branch of the single-open
consecutive permanent lift.  In the next tight cell after the minimum one,

```text
q=0,                  r=4,                  |B|=4,    (1)
```

assume in addition that the two physical outside row families are locally
transverse:

```text
a_u and b_u are linearly independent for every u in B.             (2)
```

Then at least one root `i` other than the aligned root `j` has a nonzero
projective two-open row-replacement tensor.  Consequently every nonzero
affine absorption direction at that selected root is detected by the
complete two-open graph tensor.  More precisely, the conclusion holds for
every `i` whose two complementary companion covectors at `j` are linearly
independent.  The rank-two companion frame guarantees that at least one such
`i` exists; if all three companion pairs are independent, all three choices
of `i` are detected.

The proof supplies a separate algebraic result: on four ternary modes, the
collision operator

```text
h |-> P_4(h,a,a,b)                                      (3)
```

is injective under (2).  This is an exact cross-depth transport for one
locally transverse `q=0,r=4` cell.  Condition (2) is not proved for every
hypothetical witness, and it is sufficient rather than necessary.  The
result does not exclude a witness in this cell, prove injectivity of the
fixed-root companion-to-cofactor map, treat the local-dependence boundary,
handle `q=0,r>=5` or `q>=1`, or address an unfactorized outside graph.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Imported lift and four-cell notation

Use the hypotheses and notation of
[`PROJECTIVELY_CONSTANT_SINGLE_OPEN_CONSECUTIVE_PERMANENT_LIFT_AND_COMPANION_FRAME_THEOREM.md`](PROJECTIVELY_CONSTANT_SINGLE_OPEN_CONSECUTIVE_PERMANENT_LIFT_AND_COMPANION_FRAME_THEOREM.md)
and
[`PROJECTIVELY_CONSTANT_LIFT_ROW_QUOTAS_AND_MINIMAL_CELL_TWO_OPEN_DETECTOR_THEOREM.md`](PROJECTIVELY_CONSTANT_LIFT_ROW_QUOTAS_AND_MINIMAL_CELL_TWO_OPEN_DETECTOR_THEOREM.md).
Thus

```text
Omega=R disjoint-union B,
R={i,j,s,t},           |B|=4,                          (4)

W_uv=a_u tensor b_v+b_u tensor a_v,
b_u=h_(j,u),
W_ju(y,-)=eta_j(y)b_u,
eta_j(x_j)=1.                                           (5)
```

On `B^+=B disjoint-union {j}`, the complete single-open equation is the
weighted diagonal restriction

```text
P_5(hat h_i,hat h_s,hat h_t,hat a,hat b)
 =sum_(c=0)^2 bar X_c e_c^(tensor B^+),
bar X_0 bar X_1 bar X_2!=0.                            (6)
```

The old-root companions satisfy

```text
ell_(j,v)(x_j)=0                         for v!=j,
span{ell_(j,i),ell_(j,s),ell_(j,t)}=Ann(x_j),
dim Ann(x_j)=2.                                         (7)
```

Contracting (6) at `x_j` gives the tight four-row restriction

```text
P_4(h_i,h_s,h_t,b)
 =sum_(c=0)^2 X_c e_c^(tensor B),
X_0 X_1 X_2!=0.                                        (8)
```

The arbitrary-surplus full-span theorem applied to (8) gives

```text
span{h_(v,u):u in B}=(K^3)^*             for every v in R.   (9)
```

In particular, no persistent row family `h_v` is zero.

On the projectively constant branch the defect term in the complete
two-open variation vanishes.  For distinct `i,j`, its remaining coefficient
tensor is

```text
C_ij(z)=sum_(v in R-{i,j}) ell_(j,v)(z) A_(i,j;v),    (10)

A_(i,j;v)=P_4(
  (h_w)_(w in R-{i,j,v}),a,a,b).                      (11)
```

There is no factorial divisor in (11) because `q=0`.

All local spaces and covectors are over a characteristic-zero field `K`.

## 2. Four-mode collision injectivity

Let `B={0,1,2,3}` for this section.  At mode `u`, let `a_u,b_u` be linearly
independent covectors and complete them to a local dual basis

```text
(a_u,b_u,c_u).                                        (12)
```

For a variable row family `h=(h_u)_(u in B)`, write

```text
h_u=x_u a_u+y_u b_u+z_u c_u.                          (13)
```

### Lemma 1 (transverse collision operator)

Under (12),

```text
L_(a,b): direct-sum_(u in B) L_u^* -> tensor_(u in B) L_u^*,
L_(a,b)(h)=P_4(h,a,a,b)                               (14)
```

is injective.

### Proof

The labelled permanent expansion is

```text
P_4(h,a,a,b)
 =2 sum_(u!=v)
     h_u tensor b_v tensor
     (tensor_(w in B-{u,v}) a_w),                     (15)
```

where each displayed factor occupies its labelled mode.  The factor `2`
counts the two assignments of the identical `a` rows.

Assume (15) is zero.  Fix distinct modes `u,v` and read its coordinates in
the product basis induced by (12).

1. The word with `c_u` at mode `u`, `b_v` at mode `v`, and `a` at the other
   two modes has coefficient `2z_u`.  Hence every `z_u=0`.
2. The word with `b` at exactly the two modes `u,v` has coefficient
   `2(y_u+y_v)`.  Thus every pair sum is zero.  For three distinct indices,
   the three pair equations force twice each participating `y` to vanish;
   characteristic zero then gives every `y_u=0`.
3. The word with `b` only at mode `v` and `a` at the other three modes has
   coefficient

   ```text
   2 sum_(u!=v) x_u.                                  (16)
   ```

   Put `S=sum_u x_u`.  Equations (16) give `x_v=S` for all four `v`.
   Summing yields `S=4S`, hence `3S=0`; characteristic zero gives `S=0`
   and every `x_v=0`.

Therefore every `h_u=0`, proving injectivity.  The selected twelve
coordinates form a `12 x 12` minor of absolute determinant `24576`; the
primary verifier checks that certificate directly.

### Scope of the lemma

Local transversality is a clean sufficient condition, not a classification
of the collision kernel.  A single dependent local pair need not destroy
injectivity.  Conversely, dependent pairs can create a kernel: in normalized
coordinates take

```text
a_u=e_0^*                         for every u,
b_0=b_1=e_0^*,       b_2=b_3=e_1^*,
h_0=-e_0^*,          h_1=e_0^*,  h_2=h_3=0.           (17)
```

Then (15) is zero with `h!=0`.  This ambient example is not a diagonal
restriction or a graph witness; it only prevents deletion of hypothesis
(2) from Lemma 1 without a replacement argument.

## 3. Companion-basis deletion

### Lemma 2 (a basis survives one root deletion)

Among the three covectors in (7), choose an independent pair

```text
ell_(j,s), ell_(j,t).                                 (18)
```

Let `i` be the remaining root in `R-{j,s,t}`.  Then the two companions
appearing in (10) are exactly the basis (18), and

```text
A_(i,j;s)=P_4(h_t,a,a,b)=L_(a,b)(h_t),
A_(i,j;t)=P_4(h_s,a,a,b)=L_(a,b)(h_s).                (19)
```

### Proof

The frame in (7) has rank two, so at least one of its three `2 x 2` minors is
nonzero.  Choose the corresponding pair and delete the coordinate belonging
to the third root.  Formula (19) is (11) with the one remaining persistent
root written explicitly.

## 4. Transverse four-cell detection

### Theorem 3 (at least one two-open detector)

Assume (1)--(9) and local transversality (2).  For every `i` whose two
complementary companions are independent, the tensor `C_ij` in (10) is
nonzero.  At least one such `i` exists.  Hence every nonzero affine absorption
direction at one or more non-aligned roots is detected by the complete
two-open tensor.

If every pair among the three companions in (7) is independent, the
conclusion holds for every `i in R-{j}`.

### Proof

Choose `i,s,t` as in Lemma 2.  By (9), both `h_s` and `h_t` are nonzero row
families.  Lemma 1 and (19) therefore give

```text
A_(i,j;s)!=0,              A_(i,j;t)!=0.              (20)
```

The covectors in (18) are independent.  Applying a dual selector that kills
one and not the other shows that

```text
C_ij
 =ell_(j,s) tensor A_(i,j;s)
  +ell_(j,t) tensor A_(i,j;t)                         (21)
```

is a nonzero tensor.  Each companion annihilates `x_j`.  Since
`eta_j(x_j)=1`, restriction from `Ann(x_j)` to `(ker eta_j)^*` is an
isomorphism, so (21) also remains nonzero on the effective tangent plane
`ker eta_j`.

The imported complete two-open variation is

```text
delta T_ij(y,z)=tau kappa_i(y) C_ij(z)                (22)
```

on the projectively constant branch.  A tensor product of nonzero factors
over a field is nonzero.  Thus every nonzero affine absorption covector
`kappa_i` changes the complete two-open tensor.  Rank two of (7) guarantees
at least one independent pair and hence at least one such root `i`.  If all
three pairs are independent, repeat the argument for each complementary
root.

### Detection is not fixed-root injectivity

Equation (21) is nonzero, but Lemma 1 does not prove that its two cofactor
tensors are linearly independent.  The map

```text
z |-> ell_(j,s)(z)A_(i,j;s)+ell_(j,t)(z)A_(i,j;t)     (23)
```

may therefore have rank one.  The exact conclusion is nonzero detection,
not injectivity on the two-dimensional effective companion plane.

## 5. Exact frontier

The new content is:

```text
four-mode collision map under local a/b transversality: INJECTIVE;
rank-two companion frame after one suitable deletion: BASIS SURVIVES;
q=0,r=4 transverse cell, at least one absorption root: TWO-OPEN DETECTED;
q=0,r=4 with pairwise-independent companions:         EVERY ROOT DETECTED;
local a/b transversality forced by lifted GHZ:         UNKNOWN;
fixed-root detector map injective:                     UNKNOWN;
local-dependence boundary in q=0,r=4:                  UNKNOWN;
aligned q=0,r>=5 or q>=1 transport:                    UNKNOWN;
unfactorized higher-surplus detector:                  UNKNOWN;
existence or exclusion of a witness in this cell:      UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.          (24)
```

The single-open lift, rank-two companion frame, and projectively constant
two-open variation are imported from the owners linked above.  The nonzero
persistent-row fact is imported from
[`ARBITRARY_SURPLUS_COMMON_ROW_FULL_SPAN_OBSTRUCTION.md`](ARBITRARY_SURPLUS_COMMON_ROW_FULL_SPAN_OBSTRUCTION.md).
The four-mode collision injectivity, companion-basis deletion, and transverse
`q=0,r=4` detector are proved here.  The theorem has not been formalized in
Lean.

## Replay

Run from repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_transverse_four_cell_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_transverse_four_cell_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_transverse_four_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_transverse_four_cell_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_transverse_four_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_transverse_four_cell_detector.py
```

The primary verifier builds the normalized `81 x 12` collision matrix by a
labelled `4!` permanent, checks the explicit nonzero minor, replays several
exact local basis changes, and audits every rank-two three-companion deletion
pattern in a bounded integer family.  The independent no-import audit instead
uses a standard-library permutation ledger, an explicit rational left inverse
for all twelve collision coordinates, and a separate companion-minor
enumeration.  These are bounded convention and falsification checks.  The
characteristic-zero proof for every field instance satisfying the stated
hypotheses is the written basis-selector argument above.
