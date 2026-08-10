# P7 primitive-square star closure has a fixed discriminant, and at most three row sums vanish

## Status

**Exact characteristic-zero obstruction for the last full-support pinned
branch.**  Continue with the notation of
`P7_PRIMITIVE_BOOLEAN_SQUARE_DUAL_TRIANGLE_STAR_NORMAL_FORM.md`.  Thus

```text
B=(b_ij)_(0<=i,j<=7),   b_ii=0,   b_ij=b_ji!=0,
r_i=sum_(j!=i) b_ij,
```

and the primitive Boolean-square condition is equivalent to

```text
b_ij r_k+b_ik r_j+b_jk r_i
 =2(b_ij b_ik+b_ij b_jk+b_ik b_jk)       (i,j,k distinct).   (1)
```

There is an anchor with nonzero row sum.  Name it `0`, put

```text
a_j=b_0j,        R=r_0=sum_(j=1)^7 a_j,
Delta_jk=R-2(a_j+a_k).                                (2)
```

This note proves two new facts.

First, all 21 triangles through `0` together with the seven row-sum
definitions are one homogeneous `28 x 28` linear pencil.  Its determinant
is a nonzero symmetric homogeneous polynomial `P(a_1,...,a_7)` of degree
21.  Every edge-torus solution of (1) satisfies

```text
P(a_1,...,a_7)=0.                                    (3)
```

At the equal-star point,

```text
P(1,...,1)=15*8^6*3^14=5*8^6*3^15 !=0.              (4)
```

Consequently the generic star fibre is empty on the edge torus.  This is a
global polynomial obstruction in the seven anchor edges, not a denominator-
open parameter count.  It retains every exceptional divisor
`Delta_jk=0`.

Second, if

```text
Z={i:r_i=0},                                          (5)
```

then

```text
|Z|<=3.                                               (6)
```

The preceding dual-triangle note only proved that some row sum is nonzero,
and the immediate inclusion-map argument gives `|Z|<=4`.  The new four-row
boundary classification below rules out equality.

These results do **not** prove that the primitive-square locus misses the
edge torus.  On `P=0`, a full-support kernel of the star pencil must still
satisfy 35 displayed leaf-triangle quadrics.  Existence on that incidence
locus remains **UNKNOWN**.  P7 full-support rank drop remains **UNKNOWN**,
and global Krenn--Gu remains **UNRESOLVED**.

## 1. The star-closure linear pencil

Because every `a_j` is nonzero, write

```text
r_j=a_j(1+y_j),
x_jk=b_jk/(a_j a_k)                         (1<=j<k<=7).     (7)
```

The row-sum definition for row `j` becomes

```text
y_j=sum_(k!=j) a_k x_jk.                             (8)
```

Substitute (7) into the triangle equation for `{0,j,k}`.  Its two pure
star products cancel, leaving

```text
y_j+y_k+Delta_jk x_jk=0.                             (9)
```

Let `E` be the 21 two-subsets of `{1,...,7}`.  Define the unsigned incidence
matrix and its complementary-weighted partner by

```text
U_(j,{p,q}) = 1 if j in {p,q}, and 0 otherwise,
V_(j,{j,k}) = a_k,   V_(j,e)=0 if j notin e,
D=diag_(e={j,k})(Delta_jk).                           (10)
```

For column vectors `y in K^7` and `x in K^21`, equations (8)--(9) are

```text
T(a) [y;x]=0,

T(a) = [ I_7   -V(a) ] .                             (11)
       [ U^T     D(a) ]
```

Taking the Schur complement of `I_7` gives the polynomial

```text
P(a)=det T(a)=det(D(a)+U^T V(a)).                    (12)
```

Every entry of the last `21 x 21` matrix is linear in `a`, so `P` is either
zero or homogeneous of degree 21.  Simultaneously permuting the seven leaf
labels conjugates this matrix by the induced edge permutation.  Hence `P`
is symmetric.

At `a_1=...=a_7=1`, one has `R=7`, `D=3I_21`, and `V=U`.  The unsigned
incidence matrix of `K_7` satisfies

```text
U U^T=5I_7+J_7.                                      (13)
```

Thus `U^T U` has eigenvalues `12` once, `5` six times, and `0` fourteen
times.  The eigenvalues of `3I_21+U^T U` are therefore

```text
15 (once),   8 (six times),   3 (fourteen times).    (14)
```

This proves (4), so `P` is nonzero and has degree 21.  For an edge-torus
solution, every `x_jk` is nonzero.  Therefore `(y,x)` is a nonzero vector
in `ker T(a)`, proving (3).  If `P(a)!=0`, the only star-closure solution is
`y=x=0`, which has every off-star edge zero and is outside the edge torus.
This is the claimed generic-fibre exclusion.

## 2. Exact leaf-triangle interface

Nothing about the 35 triangles among the leaves is hidden in the
determinant.  In the coordinates (7), the equation for a leaf triple
`{j,k,l}` is exactly

```text
x_jk(1+y_l)+x_jl(1+y_k)+x_kl(1+y_j)
 =2(a_j x_jk x_jl+a_k x_jk x_kl+a_l x_jl x_kl).     (15)
```

Hence the full star-chart problem is precisely:

```text
a_j!=0 and x_jk!=0;
T(a)[y;x]=0;
the 35 quadrics (15).                                (16)
```

Equation `P(a)=0` is a necessary projection of (16), not a sufficient
condition and not a construction.

The pencil also resolves the coordinate boundary without division.  From
(9) and `x_jk!=0`,

```text
Delta_jk=0  <=>  y_j+y_k=0.                          (17)
```

Thus the exceptional graph is simultaneously

```text
{jk:a_j+a_k=R/2} = {jk:y_j+y_k=0}.                   (18)
```

The left graph is a union of complete bipartite graphs between the value
classes `a=alpha` and `a=R/2-alpha`, together with the clique on the class
`a=R/4`.  The right graph is a union of complete bipartite graphs between
the classes `y=t` and `y=-t`, together with the clique on `y=0`.  In
particular, an odd cycle in the exceptional graph lies in the simultaneous
classes

```text
a=R/4,       y=0.                                    (19)
```

This is an exact classification of all denominator collisions compatible
with torus support.  It does not delete or saturate them away.

## 3. Five zero row sums are impossible

Put `c_ij=1/b_ij`.  If `i,j,k` all lie in `Z`, division of (1) by the three
nonzero edge weights gives

```text
c_ij+c_ik+c_jk=0.                                    (20)
```

For `s=|Z|`, these are `W_(2,3)(s)c=0`.  If `R_s` is the unsigned
vertex-edge incidence matrix of `K_s`, then

```text
W_(2,3)(s)^T W_(2,3)(s)=(s-4)I+R_s^T R_s,
R_s R_s^T=(s-2)I+J.                                  (21)
```

For `s>=5`, the Gram eigenvalues are

```text
3(s-2)                         (once),
2(s-3)                         (multiplicity s-1),
s-4                            (multiplicity C(s,2)-s).  (22)
```

They are all nonzero in characteristic zero.  Hence (20) would force every
internal `c_ij` to vanish, contrary to the edge-torus assumption.  Therefore
`|Z|<=4`.

## 4. Exact classification of the four-zero-row boundary

Assume for contradiction that `Z={1,2,3,4}`.  For any `k` outside `Z`, put

```text
x_i=c_ik,
y_i=(r_k/4)x_i                   (i in Z).            (23)
```

Here `r_k!=0` by the definition of `Z`, and all four `y_i` are nonzero.
The reciprocal form of (1), with `r_i=r_j=0`, gives

```text
c_ij=(r_k/2)x_i x_j-x_i-x_j
    =(4/r_k)(2y_i y_j-y_i-y_j).                      (24)
```

Sum (24) around any triple in `Z` and use (20).  Every three of the four
numbers `y_i` obey

```text
y_i y_j+y_i y_l+y_j y_l=y_i+y_j+y_l.                (25)
```

There is a short complete classification of (25).  Subtracting the
equations on `{i,j,k}` and `{i,j,l}` gives

```text
(y_k-y_l)(y_i+y_j-1)=0.                              (26)
```

Repeating (26) over the six pairs and substituting into any one equation
(25) gives the two elementary consequences

```text
y_i(y_i-1)(y_i^2-y_i+1)=0,
(y_i-y_j)(y_i+y_j-1)=0.                              (27)
```

These can equally be obtained by the following direct case split.  If all
four values are equal, (25) makes their common nonzero value `1`.  If a
pair differs, (26) makes the complementary pair sum to `1`; applying this
to the remaining differences rules out multiplicities `3+1`, `2+1+1`,
and four distinct values.  The only possibility is a `2+2` split with
values `p,q` satisfying

```text
p+q=1,       p^2-p+1=0,       pq=1.                 (28)
```

The all-one case makes (24) equal to zero and contradicts `c_ij!=0`.
In the `2+2` case, (24) has the rigid form

```text
c_ij=-8/r_k  on the two within-class edges,
c_ij= 4/r_k  on the four cross edges.                (29)
```

Set `t=4/r_k`.  The internal reciprocal graph on `Z` is independent of
`k`.  Comparing (29) for two outside vertices shows that its two-pair
partition and `t` are independent of `k`: two different negative perfect
matchings would force `t=-2t`, and all edge weights are nonzero.  Thus all
four outside row sums equal `4/t`.

Name the fixed two classes `A` and `B`.  For each outside vertex, the
reciprocals toward one class are `tp` and toward the other are `tq`, with
the orientation possibly swapped.  Since `pq=1`, the corresponding edge
weights are `q/t` and `p/t`.  Let `n` of the four outside vertices assign
`tp` to class `A`.  At a vertex of `A`, its three internal edge weights sum
to

```text
-1/(2t)+1/t+1/t=3/(2t).                              (30)
```

The zero row sums on `A` and `B`, multiplied by `t`, are therefore

```text
3/2+nq+(4-n)p=0,
3/2+np+(4-n)q=0.                                    (31)
```

Subtracting them and using `p!=q` gives `n=2`.  Either equation then reads

```text
3/2+2(p+q)=7/2=0.                                   (32)
```

impossible in characteristic zero.  This excludes `|Z|=4`; together with
Section 3 it proves (6).

## 5. Exact wall

```text
star triangles plus row closure form one 28 x 28 pencil: PROVED;
P(a) is symmetric, homogeneous of degree 21, nonzero:    PROVED;
equal-star determinant 5*8^6*3^15:                       PROVED;
every primitive-square edge-torus point lies on P=0:     PROVED;
generic star fibre on the edge torus:                    EMPTY;
exceptional graph Delta=0 iff y_j+y_k=0:                 PROVED;
leaf closure equals the 35 quadrics (15):                 PROVED;
number of vanishing row sums:                            AT MOST 3;
P=0 has a full-support kernel satisfying all 35 quadrics: UNKNOWN;
primitive Boolean-square locus meets the edge torus:      UNKNOWN;
P7 pinned matrix full rank on the edge torus:              UNKNOWN;
global Krenn--Gu:                                          UNRESOLVED. (33)
```

No graph enumeration, parameter search, numerical approximation, or
finite-field calculation enters this proof.

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_primitive_boolean_square_star_closure_discriminant.py
python claims/p7/audit_p7_primitive_boolean_square_star_closure_discriminant.py
python -m py_compile claims/p7/verify_p7_primitive_boolean_square_star_closure_discriminant.py claims/p7/audit_p7_primitive_boolean_square_star_closure_discriminant.py
uv run --with ruff ruff check claims/p7/verify_p7_primitive_boolean_square_star_closure_discriminant.py claims/p7/audit_p7_primitive_boolean_square_star_closure_discriminant.py
```

The primary verifier checks the universal coordinate identities, the exact
all-one determinant, the inclusion-map ranks, and the four-zero-row
classification.  The independent standard-library audit rebuilds the fixed
incidence matrices, uses exact integer row reduction, and separately checks
the polynomial reductions.  Neither performs a search.
