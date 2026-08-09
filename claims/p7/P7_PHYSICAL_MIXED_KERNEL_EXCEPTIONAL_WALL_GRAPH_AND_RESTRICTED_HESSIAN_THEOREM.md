# Exceptional P7 mixed kernels are restricted wall-graph Hessians

## Status

**Exact characteristic-zero boundary theory.**  The generic seven-by-seven
master Hessian uses denominators

```text
delta_ij=alpha-2(a_i+a_j).                            (1)
```

This note retains every divisor `delta_ij=0` without a limit or saturation.
The wall edges form a rigid graph: disjoint complete bipartites between
complementary coefficient classes, plus at most one midpoint clique.  The
21 local mixed-kernel equations descend exactly to the radical of a smaller
Hessian restricted to the alternating wall constraints.

As applications, midpoint cliques `K_5,K_6,K_7` are excluded from every
full-edge mixed kernel.  A midpoint `K_4` with any additional outside wall
is also excluded.  The sole `K_4` branch left by the mixed equation has no
outside wall and lies on one explicit symmetric cubic.  Midpoint `K_3`, the
good-kernel locus on that `K_4` cubic, and general disjoint bipartite wall
systems remain **UNKNOWN**.  No physical P7 construction or global
Krenn--Gu proof is claimed.

## 1. Exact exceptional descent

Let

```text
W={ij:delta_ij=0},
r_i=sum_(j!=i)f_ij,
x_i=r_i/a_i,                                         (2)
```

with every `a_i!=0`, and let `R_W` be the unsigned vertex--edge incidence
matrix of the wall graph.  For each nonwall edge put

```text
w_ij=a_i a_j/delta_ij.                               (3)
```

Define the symmetric partial master matrix

```text
(B_W x)_i=a_i x_i
 +sum_(j:ij notin W) w_ij(x_i+x_j).                  (4)
```

Then the exceptional mixed kernels are exactly the pairs `(x,y)`, with `y`
indexed by wall edges, satisfying

```text
R_W^T x=0,
B_W x=R_W y,                                         (5)

f_ij=-w_ij(x_i+x_j)          if ij notin W,
f_ij=y_ij                     if ij in W.             (6)
```

Indeed, the wall instance of the local equation is
`a_i a_j(x_i+x_j)=0`, giving the first equation in (5).  The row-sum
definition `r=R f` gives the second.  Conversely, (5)--(6) reconstruct all
21 local equations and all seven row sums.

Since `B_W` is symmetric, (5) is solvable in `y` exactly when

```text
x lies in rad(B_W restricted to ker R_W^T).           (7)
```

Thus a wall with `d=dim ker R_W^T` is a `d x d` restricted-Hessian problem.
Full support adds only the exact open conditions

```text
x_i+x_j!=0 on every nonwall edge,
and y can be chosen with every wall coordinate nonzero. (8)
```

For one wall `W={12}`, let

```text
P(u_1,u_3,...,u_7)=(u_1,-u_1,u_3,...,u_7).           (9)
```

The complete mixed-kernel test on that divisor is the six-dimensional
condition

```text
det(P^T B_W P)=0.                                    (10)
```

A radical vector must pass (8), and the uniquely reconstructed wall value
is `y_12=(B_Wx)_1=(B_Wx)_2!=0`.  Equation (10) replaces any limiting use of
the singular generic Hessian.

## 2. The wall graph is forced by coefficient values

Put `c=alpha/2`.  A wall edge is exactly a pair with

```text
a_i+a_j=c.                                           (11)
```

The involution `p -> c-p` on coefficient values proves that `W` is a
disjoint union of:

- complete bipartites `K_(m,n)` between the `p` and `c-p` value classes
  when `p!=c/2`;
- at most one clique on the midpoint class `a_i=c/2=alpha/4`;
- isolated vertices.

On a connected bipartite component, `R_W^T x=0` leaves one alternating
parameter.  An isolate leaves one free parameter.  A midpoint clique of size
at least three contains an odd cycle and forces every `x_i=0` on that clique.
This is the signed-incidence mechanism behind the dimension drop in (7).

The neighboring signless-Laplacian/TU-subgraph language is developed by
Monfared and Mallik in [*An Analog of Matrix Tree Theorem for Signless
Laplacians*](https://arxiv.org/abs/1805.04759).  The coefficient-involution
classification and restricted physical Hessian here are the direct new
transfer.

## 3. Midpoint cliques of size at least five

Write the midpoint coefficient as

```text
h=alpha/4!=0.                                        (12)
```

For `K_7`, summing coefficients gives `7h=alpha=4h`, impossible in
characteristic zero.

For `K_6`, the outside coefficient is `-2h`.  The clique coordinates of `x`
vanish.  Its single outside restricted stationarity coefficient is

```text
-4h,                                                  (13)
```

so the outside coordinate also vanishes and every cross-edge reconstruction
in (6) is zero.

For `K_5`, let the two outside coefficients be `b,d`, so `b+d=-h`.  After
normalizing by the nonzero scale `h`, the restricted Hessian is `2 x 2`; in
homogeneous form its determinant is

```text
15 b h^2(b+h)/((b-h)(b+2h))
=-15 b d h^2/((b-h)(h-d)).                           (14)
```

The numerator is nonzero because `b,d,h` are nonzero.  The denominators are
nonzero on the exact `K_5` stratum; their vanishing enlarges the midpoint
clique to `K_6`.  Therefore (7) has no nonzero vector.  This excludes
midpoint `K_s` for every `s>=5`.

## 4. The midpoint `K_4` cubic

Let the three outside coefficients be `b,c,d`.  Their sum is zero.  On the
exact stratum with no outside walls, all six factors

```text
(b-h)(c-h)(d-h)(b+2h)(c+2h)(d+2h)                   (15)
```

are nonzero.  The restricted Hessian is `3 x 3`, and its determinant vanishes
exactly on

```text
3bcd+2h(bc+bd+cd)+12h^3=0.                           (16)
```

This cubic is retained.  The mixed equation alone does not show that its
radical contains a vector satisfying all good-support conditions (8), much
less primitivity and the full annihilator equation.

If the outside triple has one wall, say

```text
b+c=2h,       d=-2h,                                 (17)
```

then `x_c=-x_b`, and the restricted problem has dimension two.  Its exact
determinant is

```text
-96h^4/((b-4h)(b+2h)),                               (18)
```

which is nonzero on the exact one-outside-wall stratum.  At either boundary
of (18), the outside wall graph becomes `K_(1,2)`.  Its one-dimensional
restricted stationarity coefficient is again `-4h`, so that boundary is also
excluded.  Hence a midpoint `K_4` plus any additional outside wall has no
full-edge mixed kernel.

## 5. Exact wall

```text
exceptional mixed-kernel reconstruction (5)--(6): EXACT BIJECTION;
wall graph:             COMPLEMENTARY COMPLETE BIPARTITES + MIDPOINT CLIQUE;
restricted dimension:  dim ker R_W^T;
one-wall master test:   EXACT 6x6 RESTRICTED HESSIAN;
midpoint K7:            COEFFICIENT-IMPOSSIBLE;
midpoint K6:            EXCLUDED;
midpoint K5:            EXCLUDED;
midpoint K4 plus outside wall: EXCLUDED;
midpoint K4 no-outside-wall branch: CUBIC (16), UNKNOWN GOOD KERNEL;
midpoint K3:            UNKNOWN;
general bipartite wall systems: UNKNOWN;
remaining primitivity/annihilator equations: UNKNOWN;
full-edge physical P7 extension: UNKNOWN;
global Krenn--Gu:       UNRESOLVED.                  (19)
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_physical_mixed_kernel_exceptional_wall_graph.py
python claims/p7/audit_p7_physical_mixed_kernel_exceptional_wall_graph.py
python -m py_compile verify_p7_physical_mixed_kernel_exceptional_wall_graph.py audit_p7_physical_mixed_kernel_exceptional_wall_graph.py
uv run --with ruff ruff check verify_p7_physical_mixed_kernel_exceptional_wall_graph.py audit_p7_physical_mixed_kernel_exceptional_wall_graph.py
```

The primary verifier proves the exceptional reconstruction as a universal
matrix identity and computes the midpoint restricted Hessians in an exact
rational-function field.  The independent standard-library audit rebuilds
the same small determinants using its own bivariate rational-polynomial
arithmetic.  Neither imports the other or project code.

## Dependency

- [P7_PHYSICAL_MIXED_KERNEL_BOOLEAN_DOWN_DESCENT_AND_SEVEN_BY_SEVEN_MASTER_HESSIAN.md](P7_PHYSICAL_MIXED_KERNEL_BOOLEAN_DOWN_DESCENT_AND_SEVEN_BY_SEVEN_MASTER_HESSIAN.md)
