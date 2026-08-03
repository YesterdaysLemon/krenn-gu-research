# The strict two-endpoint axis branch reduces sharply to 2+2+1

## Status

**Exact characteristic-zero conditional exclusion and sharp common-block
model.**  In the strict tangent-only companion branch with exactly two
effective nonroot endpoints, no three roots can have the same coordinate-axis
tangent type.  Thus the five-root all-axis patterns `4+1` and `3+1+1` are
impossible in this branch, and `2+2+1` is the sole surviving multiplicity.

The conclusion is sharp at the present level.  One explicit `2+2+1` system
uses the same honest endpoint forms and root--root tangent blocks for every
root subset and satisfies all 31 nonempty lower-root tensor equations.  Its
complementary blocker tensors are one globally nonconflicting **formal
principal-cofactor ledger**.  They are not yet proved to be the simultaneous
principal hafnians of one blocker/residual graph.

The later
[`P7_221_FORMAL_LEDGER_SCALAR_HAFNIAN_REALIZABILITY_AND_SYNCHRONIZATION_GAP.md`](P7_221_FORMAL_LEDGER_SCALAR_HAFNIAN_REALIZABILITY_AND_SYNCHRONIZATION_GAP.md)
realizes every prescribed cofactor exactly in each monochromatic scalar chart.
Those three chart graphs use different terminal--terminal blocks, so one
common physical graph and mixed-colour cancellation remain open.

Accordingly this is a genuine common-block strengthening of the earlier
subset-dependent formal state model, but it is not a global `P_7` exclusion
or construction.  Frozen-root one-tangent channels, nonprojective
root--blocker derivatives, extra effective endpoints, and common
principal-cofactor realizability remain outside the theorem.  The Krenn--Gu
conjecture remains **UNRESOLVED**.

## 1. Exact branch assumptions

Work over a characteristic-zero field.  The five roots are restricted to
coordinate-axis tangent planes.  Make the following strict assumptions.

1. Differentiated root--blocker edges vanish on those tangent planes.
2. Exactly `Q={q_0,q_1}` are effective fixed companion endpoints.
3. Root--root companion blocks are tangent-only and annihilate the frozen
   root vector at either endpoint.  Thus a frozen root does not create an
   additional one-tangent companion channel.
4. One common family of root--root forms `B_ij` and endpoint forms `p_i,q_i`
   is used for every differentiated root subset.
5. For every singleton, same-axis pair, and same-axis triple, the two legal
   parity classes attain the rank-two GHZ target flattening.  Hence the two
   companion forms span the corresponding two-dimensional diagonal plane.

The complementary blocker tensors may initially be treated as formal
principal-cofactor symbols, but the same deletion label must always carry the
same value.  This last consistency condition is enforced explicitly below.

If roots `i,j` are varied, their two companion forms are

```text
B_ij,
H_ij=p_i q_j+q_i p_j.                                  (1)
```

An internal residual-edge contribution is a scalar multiple of `B_ij` and
does not change their span.  For three varied roots, the two endpoint-tag
forms are

```text
K_p=B_12 p_3+B_13 p_2+B_23 p_1,
K_q=B_12 q_3+B_13 q_2+B_23 q_1.                        (2)
```

## 2. Three roots of one axis type are impossible

Suppose roots `1,2,3` have the same axis type.  Choose local tangent
coordinates `(x_i,y_i)`.  The pair target at `i,j` is the diagonal plane

```text
<x_i x_j, y_i y_j>.                                    (3)
```

Rank-two equality and the two-class assumption force both `B_ij` and `H_ij`
into (3).  In particular write

```text
B_12=A x_1 x_2+C y_1 y_2.                              (4)
```

The triple target plane is

```text
<x_1 x_2 x_3, y_1 y_2 y_3>.                            (5)
```

Write

```text
p_3=p_x x_3+p_y y_3,
q_3=q_x x_3+q_y y_3.                                   (6)
```

In `K_p,K_q`, the mixed monomials displayed below have unique sources:

```text
[x_1 x_2 y_3](K_p,K_q)=A(p_y,q_y),
[y_1 y_2 x_3](K_p,K_q)=C(p_x,q_x).                    (7)
```

Indeed, a diagonal block on `13` or `23` cannot produce either monomial.
Because both triple forms lie in (5), all four quantities in (7) vanish.

- If `A,C` are both nonzero, then `p_3=q_3=0`.
- If exactly one is nonzero, then `p_3,q_3` are proportional.
- If both vanish, then `B_12=0`, so `{B_12,H_12}` spans at most one
  dimension.

The first two alternatives contradict the rank-two singleton equation at
root 3, which requires `p_3,q_3` to be independent.  The third contradicts
the rank-two pair equation.  This proves:

### Theorem 1 (same-axis multiplicity bound)

Under the assumptions of Section 1, every coordinate-axis type occurs at
most twice.

### Corollary 2 (five-root reduction)

Among the previously surviving all-axis multiplicities

```text
4+1,       3+1+1,       2+2+1,                        (8)
```

only `2+2+1` survives the strict two-endpoint common-companion equations.

No genericity assumption is used.  The proof needs precisely the two legal
companion classes and their rank-two equality with the target planes.

## 3. One common 2+2+1 tangent-block system

Take axis types `A,A,B,B,C`.  The surviving local coordinate forms are

```text
A roots 1,2:  (e_0,e_1,e_2)|S_i=(0,x_i,y_i),
B roots 3,4:  (e_0,e_1,e_2)|S_i=(u_i,0,y_i),
C root 5:     (e_0,e_1,e_2)|S_5=(u_5,x_5,0).          (9)
```

Use the common endpoint forms

```text
(p_1,q_1)=(x_1,y_1),    (p_2,q_2)=(y_2,x_2),
(p_3,q_3)=(u_3,y_3),    (p_4,q_4)=(y_4,u_4),
(p_5,q_5)=(u_5,x_5),                                   (10)
```

and define `H_ij` by (1).  The ten common root--root tangent blocks are

```text
B_12= y_1 y_2,                  B_34= y_3 y_4,
B_13=-x_1 y_3-y_1 u_3+y_1 y_3, B_14= y_1 y_4,
B_23= y_2 y_3,                 B_24=-y_2 u_4-x_2 y_4+y_2 y_4,
B_15=-y_1 u_5,                 B_25= x_2 x_5,
B_35= u_3 u_5,                 B_45=-y_4 x_5.          (11)
```

For unlike-axis pairs these have the compact form

```text
B_ij=lambda_ij H_ij+F_ij,                              (12)
```

where `F_ij` is the monomial in their unique shared target colour and

```text
lambda_13=lambda_24=lambda_15=lambda_45=-1,
lambda_14=lambda_23=lambda_25=lambda_35=0.             (13)
```

Thus every displayed object is one honest multilinear form on the tangent
spaces, shared across all lower-root equations.

## 4. Exact singleton, pair, and triple equations

Write `D_c` for the pure colour-`c` blocker tensor.  At singleton roots,
assign the two endpoint-tag cofactors `(C_(i q_0),C_(i q_1))` by

```text
i=1: (D_1,D_2),    i=2: (D_2,D_1),
i=3: (D_0,D_2),    i=4: (D_2,D_0),
i=5: (D_0,D_1).                                      (14)
```

Then `p_i C_(i q_0)+q_i C_(i q_1)` is exactly the singleton GHZ derivative.

For the same-axis pairs use

```text
(C_12,C_(12Q))=(D_2-D_1,D_1),
(C_34,C_(34Q))=(D_2-D_0,D_0).                         (15)
```

For example,

```text
B_12(D_2-D_1)+H_12 D_1=x_1 x_2 D_1+y_1 y_2 D_2.     (16)
```

For every unlike pair use

```text
(C_ij,C_(ijQ))=(D_shared,-lambda_ij D_shared).        (17)
```

Equations (12) and (17) leave exactly `F_ij D_shared`, the pair GHZ target.

The six nonzero two-axis triple companion identities are

```text
K_p(123)=y_1 y_2 y_3,    K_q(124)=y_1 y_2 y_4,
K_p(134)=y_1 y_3 y_4,    K_q(234)=y_2 y_3 y_4,
K_p(125)=x_1 x_2 x_5,    K_q(345)=u_3 u_4 u_5.       (18)
```

Put the corresponding shared-colour tensor on the indicated endpoint tag
and zero on the other tag.  Explicitly, the `q_0` tags are

```text
123 -> D_2,       134 -> D_2,       125 -> D_1,       (19)
```

and the `q_1` tags are

```text
124 -> D_2,       234 -> D_2,       345 -> D_0.       (20)
```

Every other triple contains all three axis types, so its GHZ target and both
cofactor tags are zero.

## 5. The nontrivial quartet cancellation

For `I={1,2,3,4}`, let

```text
G_0=B_12 B_34+B_13 B_24+B_14 B_23,
G_Q=sum_(three pair partitions {e,f})(B_e H_f+H_e B_f).              (21)
```

Put `Y=y_1 y_2 y_3 y_4` and

```text
Omega=
 x_1 x_2 y_3 y_4+x_1 y_2 y_3 u_4-x_1 y_2 y_3 y_4
+y_1 x_2 u_3 y_4+y_1 y_2 u_3 u_4-y_1 y_2 u_3 y_4
-y_1 x_2 y_3 y_4-y_1 y_2 y_3 u_4.                  (22)
```

Direct expansion gives

```text
G_0=3Y+Omega,       G_Q=4Y-Omega,       G_0+G_Q=7Y.  (23)
```

Therefore the formal assignments

```text
C_1234=C_(1234Q)=D_2/7                              (24)
```

give exactly `Y D_2`.  Characteristic zero is used here.  Each of the other
four quartets, and the quintet, contains all three axis types; assign their
legal cofactor tags zero, matching their zero GHZ target.

### Theorem 3 (sharp common-block lower-jet model)

Equations (9)--(24) satisfy the GHZ lower-root tensor equation for every
nonempty subset of the five roots using one common family `B_ij,p_i,q_i`.

Proof.  Singletons and pairs follow from (14)--(17).  The ten triples split
into the six identities (18) and four three-axis zeros.  The five quartets
split into (23)--(24) and four three-axis zeros; the quintet is also zero.
These cases exhaust the symbolic subset types.

The deletion labels are globally nonconflicting: their root part uniquely
recovers the differentiated subset, and their residual tag distinguishes the
two parity-legal classes.  Hence no cofactor symbol receives two values.

## 6. What remains missing

The theorem moves the boundary from an independently chosen companion frame
for each root subset to **one common tangent-block frame**.  That common frame
already excludes axis multiplicity three.

It does not prove that the assigned tensors

```text
D_2-D_1, D_2-D_0, D_c, 0, D_2/7                    (25)
```

are simultaneous principal hafnians of one legal blocker/residual graph.
Principal-cofactor realizability is now the precise obstruction separating
the surviving `2+2+1` jet model from a genuine `P_7` restriction.

The same-axis exclusion also does not apply when any strict assumption in
Section 1 fails.  In particular, extra deletion classes supplied by frozen
roots, one-tangent root--root blocks, or nonprojective blocker variations may
restore more than the two companion channels.

```text
4+1 and 3+1+1 in strict two-endpoint branch: EXCLUDED;
2+2+1 common tangent blocks plus formal ledger:       REALIZED;
common principal-hafnian ledger realization:          UNKNOWN;
full P7 restriction and global Krenn--Gu:              UNRESOLVED.   (26)
```

## Replay

```powershell
uv run --with sympy python verify_p7_two_endpoint_axis_multiplicity_reduction_and_221_common_jet_model.py
python audit_p7_two_endpoint_axis_multiplicity_reduction_and_221_common_jet_model.py
uv run --with sympy --with ruff python -m ruff check verify_p7_two_endpoint_axis_multiplicity_reduction_and_221_common_jet_model.py audit_p7_two_endpoint_axis_multiplicity_reduction_and_221_common_jet_model.py
python -m py_compile verify_p7_two_endpoint_axis_multiplicity_reduction_and_221_common_jet_model.py audit_p7_two_endpoint_axis_multiplicity_reduction_and_221_common_jet_model.py
```

The primary verifier uses SymPy to check the unique mixed coefficients, all
common pair/triple/quartet identities, and the complete fixed lower-root
system.  The independent no-import audit uses a separate sparse-polynomial
engine and clears the denominator seven exactly.  Neither performs a support
search or a graph-family enumeration.
