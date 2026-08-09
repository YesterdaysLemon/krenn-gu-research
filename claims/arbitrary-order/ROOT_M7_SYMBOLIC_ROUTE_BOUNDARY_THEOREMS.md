# Root `m=7` symbolic route boundary theorems

## Status

This note gives four exact characteristic-zero conclusions in the active
five-root/seven-blocker/two-residual cell.  They replace several tempting
but invalid proof transfers by sharp statements:

1. the common-cofactor Gram theorem is automatic at two residual vertices;
2. the displayed Hall-satisfying construction is excluded by one lower-jet
   coefficient, without a word search;
3. the entire majority-ideal hierarchy can hold while a mixed coefficient
   remains nonzero; and
4. the present lower-frame theorem does not force a partition-closed Wick
   or Hirota window.

These are proof-route theorems, not a global proof.  An arbitrary
`P_7 -> Delta_3` restriction with tangent companion blocks remains unknown.

## 1. Two residual vertices give exactly the old two-port factorisation

Let `Q={q_0,q_1}` and put

```text
A=[[0,h],[h,0]].
```

The principal-hafnian cofactor matrix is

```text
C(A)=J=[[0,1],[1,0]],                                (1)
```

because deleting both residual vertices leaves the empty hafnian.  If

```text
R_u=(a_u,b_u)^T,
```

then the common Gram identity specializes to

```text
H_uv-h B_uv=R_u^T J R_v
           =a_u tensor b_v+b_u tensor a_v.            (2)
```

Conversely every family on the right of (2) has a legal symmetric-hafnian
realization: choose covectors `ell_t` with `ell_t(z_t)=1` and set

```text
B_(u,q_0)=a_u tensor ell_0,
B_(u,q_1)=b_u tensor ell_1,
B_(q_0,q_1)=0.
```

Thus no additional principal-hafnian representability condition remains
in the `h=0`, two-residual Gram layer.  Its completed blocker matrix has
rank at most two.  A full three-dimensional leaf anchor is therefore never
invertible, so the published full-leaf Schur chart is empty.

For the exact Hall-satisfying data, the global `2 x 21` port matrix has rank
two and `R^T J R` has rank two.  The scalar anchors

```text
A={(1,e_0),(3,e_2)},   D={(5,e_1),(5,e_2)}
```

have cross-Gram `I_2`; their scalar Schur defect is identically zero.  The
construction saturates, rather than violates, the rank-two stratum.

## 2. One lower-jet coefficient excludes the displayed construction

All five displayed root blocks have the form

```text
B_(r_i,u)=e_2^* tensor H_u[i,-],                       (3)
```

and all root--root and root--residual blocks were set to zero.  Vary roots
`r_0,r_1` in directions `y_0=y_1=e_0`.  Every graph edge incident to either
varied root evaluates to zero: (3) vanishes on `e_0`, and the other incident
blocks are zero.  The graph mixed derivative is therefore zero.

On the all-colour-zero blocker coefficient, however, the GHZ derivative is

```text
e_0^*(e_0)e_0^*(e_0)=1.                               (4)
```

Hence this particular bounded construction fails the exact equation
`0=1`.  This argument checks one named coefficient; it does not enumerate
the `3^7` blocker words.  Tangent root--root or root--residual companions
can change the graph-side zero without changing the top `P_7` slice, so
the displayed `0=1` is not an arbitrary-family obstruction.

## 3. The whole majority hierarchy is non-discriminating here

Let

```text
P={p_0,...,p_6}=R union Q,   R={p_0,...,p_4},
Q={p_5,p_6},                 B={b_0,...,b_6}.
```

With indices modulo seven, define three edge-disjoint perfect matchings

```text
M_c={p_j b_(j+2c):j in Z/7},                 c=0,1,2,  (5)
```

and give `p_j b_(j+2c)` the rank-one block `e_c tensor e_c`.  Set every
other block to zero and contract the roots and residual vertices with
`(1,1,1)`.

This is an exact symbolic survivor of every structural condition currently
tested by the majority hierarchy:

- root--root and root--residual couplings vanish, and `h=0`;
- the blocker incidence is `012,01,01,02,02,12,12` up to order;
- every root-row family and both residual port families span `C^3`;
- each local `7 x 3` blocker map has rank three;
- the colourwise two-port Hall condition is sharp; and
- each pure `P_7` coefficient is one, with unique matching `M_c`.

Now let `S` be any `7+r` of the fourteen vertices, `1<=r<=6`, and let `k`
be the number of `M_c` pairs internal to `S`.  The other `7-k` pairs
contribute at most one selected vertex, so

```text
7+r=|S| <= 2k+(7-k)=7+k,
```

and `k>=r`.  The pure colour-`c` tensor on `S` is divisible by any `r` of
those internal pure edges.  Therefore

```text
E_(S,c) in (I_S^r)_(1^S)                              (6)
```

for every majority set, every level, and every colour.  All `r=1`
entangled-dual conditions and the memberships for overlapping sets hold
simultaneously for the same global edge system.  No stronger Cech or Koszul
compatibility statement is being asserted.

Nevertheless the assignment

```text
p_0->b_0, p_1->b_1, p_2->b_4, p_3->b_5,
p_4->b_6, p_5->b_2, p_6->b_3
```

gives the forbidden mixed blocker word `0022111` with coefficient one.
It is unique because a blocker and its chosen colour determine its anchor.
Thus pure-tensor ideal membership, even at every order and simultaneously
on all overlapping sets, cannot enforce mixed-colour cancellation.

## 4. The current frame theorem forces no Wick window

Write `C_D=H_(V-D)` after the prescribed fixed contractions, leaving all
blocker legs free.  The all-axis lower-frame theorem says only that certain
spans of the `C_(I union A)` contain `<D_0,D_1>`.  It does not select `A`,
fix an individual `C_D`, or supply moments on proper blocker subsets.

This logical gap is sharp.  There is a formal model of the stated
cofactor-span conclusions with nonzero deletion classes only at

```text
C_empty,
C_I and C_(I union Q) for root pairs I,
C_(R union {q_0}), C_(R union {q_1}).                  (7)
```

Assign the two values `D_0,D_1` to each pair of displayed classes.  For
root derivatives of size two use `A=empty,Q`; for sizes three, four, and
five use

```text
A=(R-I) union {q_j}.
```

Every size and parity condition holds, but (7) contains no affine
even-subset four-cube, hence no six-cube.  This is a formal model of the
proved frame equations, not a claim of simultaneous principal-hafnian
realizability.  It proves that a partition-closed cumulant window is not a
logical consequence of the current theorem.

The smallest admissible four-terminal overlay uses

```text
D={4,5}, U={1,2,3,q_0}, common core B union {q_1}.
```

Its four visible products are

```text
f_0=C_45 C_(12345q_0),
f_1=C_(345q_0) C_1245,
f_2=C_(245q_0) C_1345,
f_3=C_2345 C_(145q_0).                                (8)
```

All deletion classes in (8) have legal parity, but none of the intermediate
classes is individually forced.  If the six hidden overlay classes are
`x_01,...,x_23`, their incidence equations are

```text
f_0=x_01+x_02+x_03,     f_1=x_01+x_12+x_13,
f_2=x_02+x_12+x_23,     f_3=x_03+x_13+x_23.            (9)
```

The `4 x 6` incidence matrix has rank four in characteristic not two.  For
arbitrary formal `f_i`, a right inverse is

```text
x_01=f_1, x_12=x_13=0,
x_02=(f_0-f_1+f_2-f_3)/2,
x_03=f_0-f_1-x_02, x_23=f_2-x_02.                     (10)
```

Thus the incidence identities alone expose only the hidden defect

```text
f_0-f_1+f_2-f_3=2(x_02-x_13),                         (11)
```

not a visible linear vanishing equation.  Common-weight or realizability
conditions can still impose additional nonlinear equations on the hidden
classes; surjectivity of (9) makes no assertion about those equations.

Nor may one retain the blocker core and import an ordinary Wick cumulant.
For the all-ones graph on a two-vertex core plus four terminals,

```text
H_core=1, H_(core+pair)=3, H_(core+four)=15,
```

so the normalized bosonic four-point cumulant is

```text
15-9-9-9=-12,
```

not zero.  The alternating Hirota expression is the different quantity
`15-9+9-9=6`; both are nonzero here, but they must not be conflated.
Coefficient extraction on a common core is not multiplicative and does not
preserve log-quadraticity.  Genuine `kappa_4` or `kappa_6` needs the missing
proper-blocker-subset moments.

## Verification

Run:

```text
uv run --with sympy python verify_root_m7_symbolic_route_boundary_theorems.py
python audit_root_m7_symbolic_route_boundary_theorems.py
```

Both implementations check all 26 lower-frame root-subset cases and both
displayed cofactor choices in each case, the seven-bit no-cube statement,
exact fixed matrices, the closed-form majority
count, a six-vertex hafnian recurrence, and the explicit right inverse (10).
They audit the abstract incidence identities, not common-weight
realizability of arbitrary hidden classes.  They perform no large support,
word, or matching enumeration.

## Boundary

```text
two-residual Gram completion:              AUTOMATIC;
displayed Hall construction:               EXCLUDED by one lower jet;
majority hierarchy alone:                  INSUFFICIENT;
Wick/Hirota window from current frames:     NOT FORCED;
named intermediate cofactor constraints:   NEEDED;
arbitrary tangent-completed P_7 system:     UNKNOWN;
global Krenn-Gu conjecture:                 UNRESOLVED.
```
