# Projectively constant single-open consecutive permanent lift and companion frame

## Status

**Exact conditional characteristic-zero reduction.**  Start with the
maximum-root fixed-surplus identity on

```text
Omega=R disjoint-union B,
|R|=r>=2,              |B|=m=r+2q,          q>=0.     (1)
```

Assume that the outside graph has one physical common-two-row
factorization, that one row is the fixed incidence row of a root `j`, and
that the complete open shore of `j` is projectively constant.  Then the
entire single-open-root identity is one honest restriction

```text
P_(m+1) -> weighted Delta_3.                           (2)
```

The original factorized fixed layer is its contraction at `x_j`, so this is
an exact consecutive-order extension `P_m` to `P_(m+1)`, not two unrelated
local restrictions.

The same identity gives an exact companion-frame theorem.  The old-root
companion covectors at `j` span the full tangent annihilator of `x_j`, and
their effective combinations map isomorphically onto the two-dimensional
diagonal quotient modulo the fixed layer.  Thus the companion space called
`E_j` in the two-open gauge theorem has dimension exactly two, not merely
positive dimension.

This is a positive synchronization reduction, not an exclusion.  The
common-two-row factorization, its alignment with a root row, and projective
constancy are hypotheses; none is forced for every hypothetical witness.
Arbitrary `P_(m+1)` restrictions remain open, as does transport of the
companion frame to the next two-open row-replacement depth.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.  No graph, support, word,
matching-family, or parameter enumeration is used.

## 1. Fixed-surplus and projective hypotheses

Work over a characteristic-zero field with ternary local spaces.  Let the
fully supported root vectors `x_s`, `s in R`, satisfy

```text
W_st(x_s,x_t)=0                    for s!=t.           (3)
```

For `u in B` and distinct roots `s,t`, write

```text
h_(s,u)=W_su(x_s,-),
ell_(s,t)=W_st(-,x_t) in L_s^*.                       (4)
```

Fix `j in R`.  Suppose the physical outside blocks admit the aligned
factorization

```text
W_uv=a_u tensor b_v+b_u tensor a_v,
b_u=h_(j,u)                         for u,v in B.       (5)
```

Suppose also that the whole open `j` shore is projectively constant: there
is `eta_j in L_j^*` such that

```text
eta_j(x_j)=1,
W_ju(y,-)=eta_j(y)b_u               for every u in B. (6)
```

No nonvanishing assumption is placed on an individual `a_u`, `b_u`, or
`ell_(j,s)`.  The normalization in (6) is compatible with the fixed row
because evaluation at `y=x_j` gives `h_(j,u)=b_u`.

Put

```text
M=m+1=r+2q+1,
bar X_c=product_(s in R-{j}) x_s[c] !=0.              (7)
```

The new target-mode set is

```text
B^+=B disjoint-union {j}.                             (8)
```

Define `M`-mode row families on `B^+` by

```text
hat h_s|_B=(h_(s,u))_(u in B),     hat h_s|_j=ell_(j,s),
hat a|_B=(a_u)_(u in B),           hat a|_j=eta_j,
hat b|_B=(b_u)_(u in B),           hat b|_j=0,         (9)
```

for every `s in R-{j}`.  The values in the new column are covectors on
`L_j`; the other values are covectors on their corresponding outside modes.

## 2. The consecutive permanent lift

### Theorem 1 (single-open permanent lift)

Under (1)--(9), the complete single-open-root contraction is

```text
1/(q+1)! P_M(
  (hat h_s)_(s in R-{j}),
  hat a repeated q+1,
  hat b repeated q+1)

 =sum_(c=0)^2 bar X_c e_c^(star tensor B^+).          (10)
```

All three weights in (10) are nonzero.  After multiplication by `(q+1)!`,
equation (10) is therefore an ordinary weighted multilinear restriction
`P_M -> Delta_3`.

Its contraction at `x_j` is exactly the fixed factorized layer

```text
F
 =1/q! P_m(
    (h_s)_(s in R-{j}),
    a repeated q,
    b repeated q+1)

 =sum_(c=0)^2 x_j[c] bar X_c e_c^(star tensor B).     (11)
```

Here a zero repetition is absent and `0! = 1`, so (10)--(11) include `q=0`.

### Proof

On every even outside set `S` of size `2t`, the physical factorization (5)
gives the exact Wick expansion

```text
H_S=1/t! P_(2t)(a repeated t,b repeated t;S).         (12)
```

For a fixed endpoint split, its `t!` bipartite perfect matchings are exactly
the multiplicity left after the identical-row permanent is divided by
`t!`.  This is an unsigned matching bijection over characteristic zero.

First use (12) with `t=q`.  The root row `h_j=b` is one additional `b` row,
so unsigned Laplace expansion of the fixed-surplus layer gives (11).

For `s in R-{j}`, define the surplus-two-higher companion tensor

```text
C_s
 =1/(q+1)! P_m(
    (h_t)_(t in R-{j,s}),
    a repeated q+1,
    b repeated q+1).                                  (13)
```

Using (12) with `t=q+1` shows term by term that (13) is exactly the physical
tensor `Lambda^+_(js)` from the single-open-root equation.  Likewise, (6)
and the `t=q` expansion show that the sector where open root `j` meets
outside is

```text
L_j(W_jB(y,-))=eta_j(y)F.                             (14)
```

The exact single-open-root matching partition is therefore

```text
eta_j(y)F+sum_(s in R-{j}) ell_(j,s)(y) C_s
 =sum_(c=0)^2 bar X_c y[c] e_c^(star tensor B).       (15)
```

Now expand the permanent in (10) along its new column `j`.

- Assigning that column to `hat h_s` gives
  `ell_(j,s)(y) C_s` after division by `(q+1)!`.
- There are `q+1` identical choices assigning it to an `hat a` row.  Their
  total is

  ```text
  (q+1)/(q+1)! eta_j(y)
    P_m((h_s)_(s!=j),a^q,b^(q+1))
   =eta_j(y)F.                                        (16)
  ```

- Assigning it to an `hat b` row gives zero.

Thus the column expansion is exactly the left side of (15), proving (10).
At `y=x_j`, equation (3) gives `ell_(j,s)(x_j)=0`, while (6) gives
`eta_j(x_j)=1`; hence (10) contracts to (11).  This proves the consecutive
extension claim with all factorials and multiplicities preserved.

## 3. Exact companion quotient frame

Let

```text
Diag_B=span{e_0^(star tensor B),
            e_1^(star tensor B),
            e_2^(star tensor B)}
```

and define the diagonal isomorphism

```text
D_j:L_j -> Diag_B,
D_j(y)=sum_(c=0)^2 bar X_c y[c] e_c^(star tensor B).  (17)
```

It is an isomorphism because every `bar X_c` is nonzero, and (11) says

```text
F=D_j(x_j).                                           (18)
```

Define the effective companion coefficient plane and its cofactor map by

```text
E_j={(ell_(j,s)(y))_(s!=j):y in ker eta_j},

A_j((lambda_s)_(s!=j))=sum_(s!=j) lambda_s C_s.       (19)
```

### Theorem 2 (companion quotient frame)

The map

```text
ker eta_j -> E_j,
y |-> (ell_(j,s)(y))_(s!=j)                           (20)
```

is an isomorphism.  In particular,

```text
dim E_j=2,
span{ell_(j,s):s!=j}=Ann(x_j).                        (21)
```

Moreover, `A_j` restricts to an isomorphism

```text
A_j:E_j -> D_j(ker eta_j),                            (22)
```

and the latter is the exact two-dimensional complement of `F` in
`Diag_B`.  Equivalently, the induced map

```text
L_j/<x_j> -> Diag_B/<F>,
[y] |-> [sum_(s!=j) ell_(j,s)(y) C_s]                 (23)
```

is an isomorphism.  The bracket on the right is taken in the full outside
tensor space modulo `<F>`; its image is precisely the diagonal quotient.
No assertion is made that every individual `C_s` is diagonal.

### Proof

For `y in ker eta_j`, equation (15) becomes

```text
A_j((ell_(j,s)(y))_s)=D_j(y).                         (24)
```

Since `D_j` is injective, (20) has zero kernel.  Its domain has dimension
two, proving `dim E_j=2` and (22).  Every `ell_(j,s)` annihilates `x_j` by
(3), so their span lies in the two-dimensional space `Ann(x_j)`.  Injectivity
of (20) forces that span to have dimension two, proving (21).

The normalization `eta_j(x_j)=1` gives the direct sum

```text
L_j=ker eta_j direct-sum <x_j>.                       (25)
```

Applying `D_j` and using (18) gives

```text
Diag_B=D_j(ker eta_j) direct-sum <F>.                 (26)
```

Equations (22) and (26) prove (23).  The formula is independent of the
representative of `[y]` because every `ell_(j,s)` vanishes on `x_j`.

### Consequences

There must be at least two linearly independent old-root companions at
`j`; in particular the aligned projectively constant branch requires

```text
r>=3.                                                 (27)
```

More importantly, the effective coefficient-to-cofactor map is already
injective at the single-open depth.  The still-open two-open detector uses
the different row-replacement tensors `A_(i,j;s)`.  Its missing step is
therefore an exact cross-depth transport or selector relating those tensors
to the frame (22), not proof that `E_j` is nonzero.

## 4. Imported Hall and strict-support consequences

The lift (10) permits every arbitrary-permanent necessary theorem to be
applied without a new extraction assumption.  Two consequences are useful
for bookkeeping.

First, the `q+1` repeated `hat b` rows vanish at mode `j` and span at most
one covector line at each mode of `B`.  The all-subset Hall quota for
`q>=1`, and the singleton tricolour cover for `q=0`, require at least `q+1`
distinct `b`-modes for each target colour.  One line cannot contain two
different coordinate axes, so

```text
|B|=r+2q>=3(q+1),
r>=q+3.                                               (28)
```

This recovers the existing aligned-row Hall bound by a different, lifted
permanent view; it is not a stronger numerical inequality.

Second, let

```text
I_-j=#{(s,u):s in R-{j}, u in B, h_(s,u)!=0},
c_j=#{s in R-{j}:ell_(j,s)!=0},
p_a=#{u in B:a_u!=0},
p_b=#{u in B:b_u!=0}.                                 (29)
```

Counting distinct source-row cells in (10), including repeated rows as
distinct source coordinates, gives exactly

```text
S_j=I_-j+c_j+(q+1)(p_a+1)+(q+1)p_b.                  (30)
```

The strict arbitrary-permanent support theorem therefore yields

```text
S_j>=3M+3=3r+6q+6.                                   (31)
```

Equation (31) is an active-covector inequality for the lifted local maps.
It is not a bound on the total number of graph edges, and repetitions in
(30) must not be collapsed to physical-edge support.

## 5. Provenance and exact frontier

The fixed-surplus identity and exact single-open matching partition are
imported from
[`BALANCED_FIXED_SURPLUS_TRUNCATION_FIBRE_NONOBSERVABILITY_AND_TRANSVERSE_ABSORPTION_THEOREM.md`](BALANCED_FIXED_SURPLUS_TRUNCATION_FIBRE_NONOBSERVABILITY_AND_TRANSVERSE_ABSORPTION_THEOREM.md).
The complete two-open formula and its prior observation `E_j!=0` are in
[`BALANCED_TWO_OPEN_ROOT_GAUGE_DETECTOR_AND_STAR_INVISIBILITY_BOUNDARY.md`](BALANCED_TWO_OPEN_ROOT_GAUGE_DETECTOR_AND_STAR_INVISIBILITY_BOUNDARY.md).
The Hall and strict-support inputs are respectively
[`ARBITRARY_PERMANENT_KERNEL_DELETION_HIERARCHY.md`](ARBITRARY_PERMANENT_KERNEL_DELETION_HIERARCHY.md)
and
[`ARBITRARY_PERMANENT_EQUALITY_TWO_SWITCH_EXCLUSION_THEOREM.md`](ARBITRARY_PERMANENT_EQUALITY_TWO_SWITCH_EXCLUSION_THEOREM.md).

The new content is the exact new-column permanent construction (9)--(10),
the proof that the fixed restriction is its contraction, the quotient-frame
isomorphism (23), and the transferred support ledger (30)--(31).  No external
classification theorem is needed beyond the already imported permanent
results.  The theorem has not been formalized in Lean.  The preserved
line-by-line scope and adversarial reasoning are in the
[`2026-08-11 review record`](../../docs/audits/PROJECTIVELY_CONSTANT_SINGLE_OPEN_PERMANENT_LIFT_REVIEW_2026-08-11.md).

```text
aligned projectively constant single-open equation: P_(m+1) RESTRICTION;
fixed P_m layer as its x_j contraction:              PROVED;
effective old-root companion space E_j:              DIMENSION TWO;
companion cofactor map on E_j:                        EXACT QUOTIENT FRAME;
aligned-row Hall bound r>=q+3:                        RECOVERED;
lifted active row-cell support >=3M+3:                PROVED;
common-row alignment in every witness:               UNKNOWN;
projective constancy in every synchronized cell:      UNKNOWN;
transport to two-open row-replacement tensors:        UNKNOWN;
unfactorized higher-surplus detector:                 UNKNOWN;
arbitrary P_M nonrestriction:                         UNKNOWN;
global Krenn--Gu conjecture:                          UNRESOLVED.
```

## Replay

Run from repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_single_open_permanent_lift.py
python claims/arbitrary-order/audit_projectively_constant_single_open_permanent_lift.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_single_open_permanent_lift.py claims/arbitrary-order/audit_projectively_constant_single_open_permanent_lift.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_single_open_permanent_lift.py claims/arbitrary-order/audit_projectively_constant_single_open_permanent_lift.py
```

The primary verifier compares the physical perfect-matching contraction to
the proposed permanent symbolically on several small `(r,q)` cells, checks
the three Laplace sectors and factorials separately, and audits the quotient
frame and support arithmetic.  The independent no-import audit uses a
separate labelled-assignment ledger, exact integer arithmetic, and rational
row reduction.  These are bounded convention and falsification checks.  The
arbitrary-order theorem is the written matching and Laplace bijection plus
the imported permanent results.
