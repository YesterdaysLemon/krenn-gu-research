# A twenty-first component from a coincident-support rank-one star

## Status

**Exact characteristic-zero component theorem.**  The pure `P_4`
compression locus has a six-dimensional irreducible component whose generic
pair profile, in edge order `01,02,03,12,13,23`, is

```text
(3,4,4,3,3,4).                                      (1)
```

The three exceptional edges form a star and carry coefficient-rank-one
relations supported on the same binary source pair.  The exceptional graph
distinguishes this component from the equal-support sixfold, whose exceptional
edges form a triangle and whose relation-rank word is `(2,1,1)`.  Pair profile
or dimension separates every other previously certified orbit.  The exact
lower bound is therefore twenty-one symmetry-inequivalent pure-`P_4`
component orbits.

The mixed-chain vertical fibre left open in equation (22) of
[`P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md`](../../P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md)
is a boundary of this component.  Together with the other residual-placement
theorems, this closes the exactly-one-kernel rank-one triangle cell at the
pure-`P_4` level.  It does not settle the marked `P_5` fibres of the new
components or the global Krenn--Gu conjecture.

## The homogeneous family

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2)
```

and put

```text
A=X_0+X_1,       C=X_0-X_1,
B=X_2+X_3,       D=X_2-X_3.                         (2)
```

Thus `AC=BD=0` and `A^2+C^2=0`.  For parameters `p,q,kappa` and
`[r:s]` in `P^1`, define

```text
U_0=span(A+pB, C+qB),
U_1=span(A,C),
U_2=span(C,B+kappa A),
U_3=span(rA+sC,D).                                  (3)
```

Direct squarefree multiplication gives only

```text
T_0010= 4pr,       T_0110=-4ps,
T_1010= 4qr,       T_1110=-4qs.                     (4)
```

The four displayed entries are the decomposable matrix

```text
4 (p,q)^T (r,-s),                                  (5)
```

with the third and fourth mode factors fixed.  Hence every point of (3) is
pure, and it is nonzero whenever `(p,q)!=(0,0)`.

In the displayed row coordinates the same factorization is

```text
4(p y_0+q x_0)(y_1-ell x_1)x_2y_3.                (5a)
```

## A star of three coincident-support exact pairs

On the chart `r=1`, write `ell=s/r`.  The three exceptional relations, in
the displayed row orders of (3), have coefficient vectors

```text
edge 01: (1,-q/p,-p/q,1),
edge 12: (1,0,0,0),
edge 13: (ell,0,1,0).                               (6)
```

Each reshapes to a rank-one `2 x 2` matrix.  Intrinsically these are the
zero products

```text
(A-(p/q)C)(A-(q/p)C)=0,
A C=0,
(ell A+C)(A+ell C)=0.                              (7)
```

All three exact pairs live on the same source support `{0,1}`.  Their mode
graph is the star with centre mode one.

The four pure-kernel rows of (5a) are

```text
q y_0-p x_0,       ell y_1+x_1,       y_2,       x_3.
```

Away from `p+ell q=0`, the relations in (6) use exactly the first, third,
and second of these kernel rows, respectively, and no second pure-kernel
endpoint.  Thus their generic sorted kernel-endpoint signature is
`(1,1,1,0)`.

At `(p,q,kappa,ell)=(2,3,1,2)`, exact row reduction gives (1).  Transparent
maximal pair-image minors on the three exterior edges are

```text
edge 02: -8pq,
edge 03: -8(ell+1)(ell p+q),
edge 23: -8 kappa ell(ell+1).                       (8)
```

Thus (1) holds on a nonempty dense open set; no sampling is used to infer
genericity.

## Six actual family directions

Restore the projective diagonal source torus

```text
diag(t_0,t_1,t_2,1).                                (9)
```

Use Grassmann charts with pivots

```text
(01),(01),(01),(02)                                (10)
```

and order the sixteen free entries rowwise as `g_0,...,g_15`.  The seven
written parameters `(p,q,kappa,ell,t_0,t_1,t_2)` contain the exact stabilizer

```text
(p,q,kappa,ell,t_0,t_1,t_2)
 -> (sigma p,sigma q,kappa/sigma,ell,
     sigma t_0,sigma t_1,t_2).
```

At

```text
(p,q,kappa,ell,t_0,t_1,t_2)=(2,3,1,2,1,1,1),       (11)
```

the family Jacobian has rank six.  Its rows

```text
(g_0,g_1,g_2,g_8,g_10,g_12)
```

against parameter columns `(p,q,kappa,ell,t_0,t_2)` have determinant

```text
-5/72.                                              (12)
```

The image closure of (3) and (9) is therefore an irreducible sixfold.

## The seventh tangent direction is quadratically obstructed

Introduce Segre ratios `z_0,...,z_3` and use `alpha=0000` in the universal
incidence equations

```text
F_beta=T_beta-T_alpha product_(i: beta_i!=alpha_i) z_i=0,
beta!=alpha.                                       (13)
```

At (11), the normalized tensor has eight nonzero entries and ratios

```text
(z_0,z_1,z_2,z_3)=(-1/5,-3,1,0).                  (14)
```

The incidence Jacobian has rank thirteen.  Number the fifteen rows in
lexicographic word order after omitting `0000`.  Rows

```text
0,1,2,3,4,5,6,7,8,10,11,12,14                     (15)
```

against columns

```text
g_0,g_1,g_2,g_4,g_5,g_6,g_7,g_8,g_10,
g_12,g_13,g_14,z_3                                  (16)
```

have determinant

```text
100.                                                (17)
```

These thirteen equations therefore cut out a regular seven-dimensional
local scheme.  Its free coordinates are

```text
g_3,g_9,g_11,g_15,z_0,z_1,z_2.                    (18)
```

The six family directions project to the first six coordinates in (18)
with determinant `1/50`.  Fix those six coordinates at (11),(14), put
`z_2=1+h`, and solve the thirteen regular equations through order two.  The
two omitted equations, for words `1010` and `1110`, become

```text
(7/60)h^2+O(h^3),       -(7/20)h^2+O(h^3).         (19)
```

In particular the first omitted equation is nonzero in the regular local
domain cut out by (15).  Adding it lowers local dimension to at most six.
The six family directions in (12) give the reverse inequality.  Hence the
full incidence has local dimension exactly six, and the irreducible family
closure is an irreducible component.  A nonzero pure tensor has a unique
projective Segre point, so forgetting the ratios preserves the component
statement.

## Why this is a new orbit

The previously known sixfolds are separated as follows:

- components seven and fifteen have a generic rank-two pair;
- component nine has three generic rank-two pairs;
- component eleven has the same sorted profile `(3,3,3,4,4,4)`, but its
  three exceptional edges form a triangle and have relation-rank word
  `(2,1,1)`;
- the present exceptional graph is a star and all three relations have rank
  one.

Dimension separates the family from all previously certified fivefolds,
including components nineteen and twenty.  Pair-image ranks, relation ranks,
and exceptional graph type are invariant under source-coordinate
permutations, diagonal source scaling, mode permutations, and row-basis
changes.  Thus (3) is a genuinely new component orbit.

## The mixed-chain vertical fibre is its boundary

The residual fibre in the earlier reduction is

```text
U_0 in Gr(2,span(A,C,B)),
U_1=span(A,C),
U_2=span(C,B),
U_3=span(D,C).                                      (20)
```

The chart for `U_0` in (3) is dense in the irreducible projective plane
`Gr(2,span(A,C,B))`.  Set `kappa=0` and take the homogeneous arc

```text
[r:s]=[epsilon:1].                                 (21)
```

The four Pluecker points then converge exactly to (20) at `epsilon=0`.
At the limit the only nonzero tensor entries are

```text
T_0110=-4p,       T_1110=-4q.                      (22)
```

Therefore every nonzero point of the complete projective mixed-chain
vertical fibre, including its other `U_0` charts, lies in the component
closure.

## Exact replay

```text
uv run --with sympy python claims/p4/classifications/star/coincident-support-rank-one-star/verify_p4_coincident_support_rank_one_star_component.py
python claims/p4/classifications/star/coincident-support-rank-one-star/audit_p4_coincident_support_rank_one_star_component.py
```

The primary verifier checks (4)--(22) over `Q`, including the exact
stabilizer, family minor, rank-thirteen incidence minor, six-dimensional free
projection, two exact quadratic obstructions, and homogeneous boundary arc.
The independent audit rebuilds the permanent, pair products, chart
derivatives, second-order implicit solve, and boundary specialization over
`F_101` and `F_103`.  Both are fixed-size symbolic certificates; neither
searches a parameter grid or runs an elimination.
