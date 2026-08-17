# `P_6` co-two spanning-tree radical and simultaneous factor compatibility boundary

## Status

**Exact characteristic-zero theorem and simultaneous all-fifteen sharpness
boundary.**  Once one common six-mode permanent pullback with six labelled
three-planes has already been supplied, mixed-radical constraints at the five
edges of any spanning tree are necessary and sufficient for all nonconstant
target coefficients to vanish.  This compresses fifteen pair tests to five,
but it does not construct or synchronize the common planes.

Triple and quartet zeon-product identities are necessary compatibility
conditions for independently presented pair sensors.  They are far from
sufficient: an exact common-plane model has equality-six pair spaces,
rank-six complementary sensors at all fifteen pairs, pair-level diagonal
quotients, every product-overlap identity, and three nonzero pure
coefficients, but its `001122` coefficient is `41456`.

The countermodel is one common `P_6` pullback but not a
`P_6 -> Delta_3` restriction and not a graph witness.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Common co-two data

Let `K` be a field of characteristic zero and put

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).                 (1)
```

For each mode `i in [6]`, let `U_i subset (Z_6)_1` be a three-plane with one
fixed ordered basis

```text
u_(i,0), u_(i,1), u_(i,2).                            (2)
```

The coefficient of the colour word `gamma:[6]->[3]` in the resulting
`P_6` pullback is

```text
T_gamma=[x_0...x_5] product_(i=0)^5 u_(i,gamma(i)).   (3)
```

For a pair `{a,b}`, define

```text
B_ab=span{u_(a,c)u_(b,d):c,d in [3]},
M_ab=span{u_(a,c)u_(b,d):c!=d},                       (4)

A_bar(ab)
 =span{product_(i notin {a,b}) u_(i,c_i):c_i in [3]}. (5)
```

Use the perfect complement pairing

```text
<f,g>=[x_0...x_5]fg.                                  (6)
```

Thus `M_ab subset A_bar(ab)^perp` says that every word bichromatic at
`{a,b}` has zero coefficient.

## 2. A spanning tree suffices after common factorization

### Theorem 1 (spanning-tree mixed-radical criterion)

Let `T` be any spanning tree on the six modes.  The common pullback (3) is a
weighted diagonal tensor

```text
sum_(c=0)^2 lambda_c e_c^(tensor 6),    lambda_c!=0,   (7)
```

if and only if

```text
T_(c,c,c,c,c,c)=lambda_c!=0,            c=0,1,2,      (8)

M_ab subset A_bar(ab)^perp
for every {a,b} in E(T).                                 (9)
```

In that event (9) also holds at the ten non-tree pairs.

### Proof

Let `gamma` be nonconstant.  A colouring of a connected graph which is
constant across every edge is constant on all vertices.  Therefore some tree
edge `{a,b}` is bichromatic under `gamma`.  The pair factor in (3) belongs to
`M_ab`, while the complementary four-mode factor belongs to `A_bar(ab)`.
Equation (9) gives `T_gamma=0`.  Equation (8) supplies precisely the three
nonzero constant coefficients, proving (7).

Conversely, if (7) holds, pair any generator `u_(a,c)u_(b,d)` of `M_ab`
with any generator of `A_bar(ab)`.  Since `c!=d`, the corresponding complete
word is nonconstant and its coefficient is zero.  Hence the radical
containment holds for every one of the fifteen pairs.

Connectivity is the exact word-cover hypothesis in this argument: on a
disconnected test graph, a colouring may be constant on each component and
different between components without exposing a tested bichromatic edge.

### Scope

The theorem has breadth five pair charts but every radical uses its four-mode
complement, so each test is still a full six-mode target equation.  Its depth
is degree two paired with degree four.  Its common hidden data are the six
ordered planes (2), already assumed.  Their transition maps are identities
because the frames and colour labels are fixed.  The result compresses target
verification; it neither identifies pair factorizations nor glues them.

## 3. Necessary simultaneous product invariants

For subspaces of `Z_6`, write `UV=span{uv:u in U,v in V}`.  Any common
six-mode factorization by six labelled three-planes satisfies, for distinct
modes,

```text
B_ab U_c=B_ac U_b=B_bc U_a=U_a U_b U_c,               (10)

B_ab B_cd=B_ac B_bd=B_ad B_bc
             =U_a U_b U_c U_d,                        (11)

A_bar(ab)=B_cd B_ef=B_ce B_df=B_cf B_de,              (12)
```

where `{c,d,e,f}` is the complement of `{a,b}` in (12).

These are exact zeon-product identities, following from associativity and
commutativity.  No exterior or Pluecker identity is imported.  Failure of
one displayed equality is a decisive incompatibility among proposed
independently factored pair records; (10) itself uses the proposed endpoint
factor `U_c`.  Passing all of them is not known to reconstruct degree-one
factors from unfactored pair spaces.  Even when a common factorization is
already present, the identities do not imply the mixed radicals (9).

Once the complement products in (12) have genuinely been synchronized, the
load-bearing tree conditions can be written

```text
M_ab perpendicular to B_cd B_ef                         (13)
```

on five tree edges.  Before factor identifiability is proved, pair overlaps
are correspondences between factorization fibres, not elements of a
transition group.

## 4. Exact common-factor all-fifteen countermodel

Put

```text
w_0=x_0+x_3,
w_1=x_1+x_4,
w_2=x_2+x_5,
U=span{w_0,w_1,w_2}.                                  (14)
```

Use this same plane at all six modes, with ordered basis

```text
v_0=w_0+w_1+w_2       =(1,1,1,1,1,1),
v_1=w_0+2w_1+3w_2     =(1,2,3,1,2,3),
v_2=w_0+4w_1+9w_2     =(1,4,9,1,4,9).                 (15)
```

The basis-change determinant is `2`, so these are independent.

### Pair spaces

The six products

```text
w_0^2,w_1^2,w_2^2,w_0w_1,w_0w_2,w_1w_2              (16)
```

have, on coefficient rows `03,14,25,01,02,12`, a diagonal minor with entries
`2,2,2,1,1,1` and determinant `8`.  Hence `dim U^2=6`.  Injectivity of
`Sym^2(U)->U^2` gives

```text
M=span{v_0v_1,v_0v_2,v_1v_2},          dim M=3,       (17)
```

and the classes of `v_0^2,v_1^2,v_2^2` form a basis of `U^2/M`.  Therefore
all fifteen pairs are equality-six pair-level diagonal-quotient frames.

### Complement sensors

Since `w_i^3=0`, every degree-four product belongs to the span of

```text
w_i^2 w_j^2                         (i<j),
w_i^2 w_j w_k                       ({i,j,k}={0,1,2}). (18)
```

The six displayed elements have distinct coordinate-pair occupancy patterns
of types `(2,2,0)` and `(2,1,1)`, so they are independent.  Thus

```text
dim U^4=6.                                             (19)
```

Every complementary sensor is `U^4`; all fifteen have rank six.  Equations
(10)--(12) hold automatically for the one common factorization.

### Target failure

For the pure words,

```text
[x_0...x_5]v_c^6=6! product_(p=0)^5 v_c[p],
```

so their coefficients are

```text
720, 25920, 933120.                                   (20)
```

Nevertheless,

```text
[x_0...x_5]v_0^2 v_1^2 v_2^2=41456!=0.               (21)
```

For a direct check, write `A=w_0,B=w_1,C=w_2`.  Extracting one copy of each
coordinate from the three disjoint coordinate pairs contributes a factor
eight, and

```text
[A^2B^2C^2]
 (A+B+C)^2(A+2B+3C)^2(A+4B+9C)^2
 =1332+198+52+2088+1104+408
 =5182.                                               (22)
```

Thus (21) is `8*5182`.  This proves that common factorization, pair-level
equality-six diagonal-quotient admissibility, all-fifteen sensor rank drop,
pure nonvanishing, and all product-overlap identities do not imply the mixed
radicals.  Indeed the
model is mode-symmetric: for every chosen pair, a mode permutation of
`001122` is bichromatic at that pair and still has coefficient `41456`.
Thus every one of the fifteen mixed-radical containments fails.

## 5. Exact frontier consequence

The all-fifteen problem can now be separated as

```text
independent pair records
  -> identify and synchronize six common labelled planes;       OPEN
  -> verify five spanning-tree mixed radicals;                   EXACT
  -> all fifteen radicals and every mixed coefficient zero;     PROVED
  -> verify the three pure coefficients are nonzero;
  -> weighted Delta_3.                                           PROVED. (23)
```

The countermodel rules out replacing the middle radical step by dimensions,
pure coefficients, or triple/quartet factor-space compatibility.  Product
dimensions seven through nine and the equality-six factorization fibres
remain open.  Graph-to-local extraction is prior to every step above: a
hypothetical graph must first legally supply one common `P_6` pullback.  Pair
sensors cannot manufacture that restriction, so this theorem does not close
GL or prove `P_6` nonrestriction.

## Replay

Run from repository root:

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_p6_cotwo_spanning_tree_radical_and_simultaneous_factor_compatibility.py
python -I claims/arbitrary-order/audit_arbitrary_permanent_p6_cotwo_spanning_tree_radical_and_simultaneous_factor_compatibility.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_p6_cotwo_spanning_tree_radical_and_simultaneous_factor_compatibility.py claims/arbitrary-order/audit_arbitrary_permanent_p6_cotwo_spanning_tree_radical_and_simultaneous_factor_compatibility.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_p6_cotwo_spanning_tree_radical_and_simultaneous_factor_compatibility.py claims/arbitrary-order/audit_arbitrary_permanent_p6_cotwo_spanning_tree_radical_and_simultaneous_factor_compatibility.py
```

The primary uses exact rational bitmask zeon arithmetic to reconstruct the
pair and complement spaces, their dimensions and product identities, all
three pure coefficients, (21), and the tree word cover.  The no-import audit
uses a direct permutation permanent, the named pair minor, the six occupancy
patterns in (18), the hand coefficient ledger (22), and an independently
chosen tree.  These are focused convention checks; the connected-colouring,
product-associativity, and displayed basis arguments prove the theorems.
