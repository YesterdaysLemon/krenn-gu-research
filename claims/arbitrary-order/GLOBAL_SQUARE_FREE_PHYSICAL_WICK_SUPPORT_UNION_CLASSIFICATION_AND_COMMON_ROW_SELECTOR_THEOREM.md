# Global square-free physical Wick support-union classification and common-row selector

## Status

**Exact characteristic-zero global common-row theorem.**  Fix one scalar
coefficient word on `n>=7` ports and a physical two-residual pair channel

```text
K_ij=a_i b_j+b_i a_j.                                (1)
```

The aggregate degree-two to degree-four Wick map over **all** four-port rows
is multiplication by the product of two linear forms in the square-free
algebra.  Write `S=supp a`, `T=supp b`, and `V=S union T`.  The map is
injective exactly when

```text
|S|>=5,       |T|>=5,       and
  [ |V|>=7  or  (|V|=6 and Delta_6(a,b)!=0) ].       (C)
```

where `Delta_6` is the exact physical determinant from the six-port theorem.
If `|V|=5`, necessarily `S=T=V` and the kernel has dimension exactly five.
If either support has size at most four, its one-step kernel persists.

This closes an exact part of the all-principal-minors-singular branch left by
the [`six-port Wick theorem`](SIX_PORT_PHYSICAL_WICK_SELECTOR_TWO_ACTIVE_ALL_SUBWINDOW_AND_DEEPER_RESPONSE_THEOREM.md).
At seven ports, take one factor nonzero everywhere and the other nonzero on
exactly five ports.  For the pair formed by the two zero ports, every
principal six-port determinant containing that pair vanishes, yet the full
thirty-five-row map has rank twenty-one and identifies the pair.  Thus a
nonzero principal six-port determinant is sufficient but not necessary even
for bounded exact recovery.

The classification is pointwise for every nonzero coefficient choice on the
named supports.  It also computes the complete one-sided small-support kernel
when the other factor uses at least seven ports, gives exact singular controls
on the six-port boundary, and implies intrinsic injectivity whenever the
physical scalar channel has no zero edge on `n>=7` ports.

As before, the result is downstream of target attachment.  It cannot create
legal constant selectors for the `z_2` or `z_4` rows.  It does not by itself
recover the full tensor from one scalar word, exclude a hypothetical witness,
or imply a weighted permanent restriction.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## 1. Square-free factorization

Let `K` be a characteristic-zero field and put

```text
A(n)=K[x_1,...,x_n]/(x_1^2,...,x_n^2),
A(n)_d=span{x_I:|I|=d}.                              (2)
```

For `c=(c_i)` write

```text
ell_c=sum_i c_i x_i,
U_c^(d):A(n)_d -> A(n)_(d+1),       f |-> ell_c f.   (3)
```

Because squares vanish,

```text
ell_a ell_b=sum_(i<j)(a_i b_j+b_i a_j)x_i x_j
           =sum_(i<j)K_ij x_i x_j.                  (4)
```

Encode the unknown pair array as

```text
m=sum_(i<j)m_ij x_i x_j.                             (5)
```

The coefficient of `x_S`, `|S|=4`, in `ell_a ell_b m` is

```text
(mu_(a,b)m)_S
 =sum_(P subset S, |P|=2)K_(S-P)m_P.                (6)
```

Therefore

```text
mu_(a,b)=U_a^(3) U_b^(2)=U_b^(3) U_a^(2).           (7)
```

Equation (7) is an identity of the literal physical Wick map, not a generic
matrix model.

## 2. Linear-form support lemma

For a coefficient vector `c`, let

```text
r(c)=|{i:c_i!=0}|.                                   (8)
```

### Lemma 1 (square-free one-step rank)

Multiplication by `ell_c` from degree `d` to degree `d+1` is injective if

```text
r(c)>=2d+1.                                          (9)
```

For `d=2`, its kernel dimension in the full `n`-variable algebra is

```text
dim ker U_c^(2)=
  binom(n,2)   if r=0,
  n-1          if r=1 or 2,
  2            if r=3 or 4,
  0            if r>=5.                              (10)
```

### Proof

Diagonal scaling of the supported variables turns `ell_c` into
`x_1+...+x_r`.  Split by the degree `j` in the other `n-r` variables:

```text
A(n)_d=direct-sum_(j=0)^d A(r)_(d-j) tensor A(n-r)_j. (11)
```

On the `j`-summand, `U_c^(d)` is the inclusion map

```text
U_r^(d-j):A(r)_(d-j) -> A(r)_(d-j+1)                (12)
```

tensored with the identity.

For completeness, `U_r^(k)` is injective when `r>=2k+1`.  Suppose numbers
`f_T`, indexed by the `k`-sets, have zero sum over the `k`-subsets of every
`(k+1)`-set.  For distinct `a,b`, subtract the equations on
`R union {a}` and `R union {b}`, where `R` is a `k`-set disjoint from them.
The common term `f_R` cancels and gives

```text
sum_(T subset R, |T|=k-1)(f_(T union {a})-f_(T union {b}))=0. (13)
```

The same assertion in degree `k-1` lives on `r-2>=2(k-1)+1` vertices, so
induction makes every displayed difference zero.  The Johnson graph on
`k`-sets is connected, hence all `f_T` are one scalar.  One `(k+1)`-set
equation gives `(k+1)f_T=0`, so characteristic zero makes that scalar zero.
The case `k=0` starts the induction.

Condition (9) now follows from (11), since the largest internal degree is
`d`.  For `d=2`, the only failing blocks are the elementary inclusion maps

```text
A(r)_2 -> A(r)_3,
A(r)_1 -> A(r)_2,
A(r)_0 -> A(r)_1.                                   (14)
```

Their ranks give, respectively:

- `r=4`: `6 -> 4`, kernel dimension two;
- `r=3`: `3 -> 1`, kernel dimension two;
- `r=2`: one internal degree-two kernel plus one degree-one kernel for each
  of the `n-2` outside variables, total `n-1`;
- `r=1`: one degree-one kernel for each of the `n-1` outside variables;
- `r=0`: the map is zero.

All blocks are injective for `r>=5`.  This proves (10). `square`

## 3. Support-union classification

Put

```text
S=supp a,       T=supp b,       V=S union T,
C=S intersect T,                Y=T-S.               (15)
```

Variables outside `V` will be called `Z` variables.

### Lemma 2 (outside-union reduction)

Assume `|S|,|T|>=5`.  Splitting by `Z`-degree gives

```text
A(n)_2=direct-sum_(j=0)^2 A(V)_(2-j) tensor A(Z)_j. (16)
```

On the `j`-summand, `mu_(a,b)` is multiplication by `ell_a ell_b` from
degree `2-j` to degree `4-j` on `A(V)`.  The `j=1,2` maps are injective.
Consequently the global kernel is exactly the kernel of

```text
ell_a ell_b:A(V)_2 -> A(V)_4.                        (17)
```

### Proof

For `j=1`, multiplication by the first factor is injective from degree one
to two because its support has size at least three, and multiplication by
the second is injective from degree two to three because its support has size
at least five.  For `j=2`, the map sends `1` to `ell_a ell_b`, which is
nonzero.  Indeed, a square-free product of two linear forms each supported on
at least five vertices cannot vanish.  If the supports differ, a vertex in
their symmetric difference paired with a vertex in the other support gives a
nonzero cross term.  If the supports are equal, three common nonzero
coordinates make the equations `a_i b_j+b_i a_j=0` force incompatible
pairwise ratios.
`square`

### Lemma 3 (coefficient-independent union-seven injectivity)

If

```text
|S|>=5,              |T|>=5,              |V|>=7,    (18)
```

then `mu_(a,b)` is injective for every choice of nonzero coefficients on
those supports.

### Proof

If either support has size at least seven, put the other factor first in
(7).  Lemma 1 makes the degree-two multiplication injective at support five
and the degree-three multiplication injective at support seven.

It remains to treat `|S|,|T| in {5,6}`.  Suppose `m in A(V)_2` and put

```text
p=ell_b m,                 ell_a p=0.                (19)
```

The kernel of `U_a^(3):A(V)_3 -> A(V)_4` is a
five-dimensional subspace contained entirely in `A(S)_3`.  To see this,
split by degree outside `S`.  All positive outside-degree blocks have
internal degree at most two and are injective by Lemma 1.  On the zero block,
the transpose of `U_r^(k)` becomes `U_r^(r-k-1)` after complementing subsets.
For `r=5,6` and `k=3`, that transpose is injective, so the zero block is
surjective and has dimension defect five.  Thus `p in A(S)_3`.

Write

```text
ell_b=ell_C+sum_(y in Y)b_y x_y,
m=m_0+sum_y x_y m_y+sum_(y<z)x_y x_z m_yz,           (20)
```

with `m_0 in A(S)_2`, `m_y in A(S)_1`, and `m_yz in K`.  Since `p` has no
`Y` variable, coefficient comparison gives

```text
p=ell_C m_0,
b_y m_0+ell_C m_y=0,
b_y m_z+b_z m_y+ell_C m_yz=0,
b_y m_zw+b_z m_yw+b_w m_yz=0.                       (21)
```

For `|Y|=1`, these equations put `p` in `ell_C^2 A(S)_1`.  For `|Y|=2`,
multiplying the pair equation by `ell_C` and using the singleton equations
gives

```text
2b_yb_z m_0=ell_C^2 m_yz,
p in K ell_C^3.                                      (22)
```

For `|Y|>=3`, multiply a triple equation by `ell_C^2` and use (22) on its
three pairs.  Then

```text
6b_yb_zb_w m_0=0.                                   (23)
```

Characteristic zero and nonzero support coefficients give `m_0=0`, hence
`p=0`; Lemma 1 makes `U_b^(2)` injective, so `m=0`.

Suppose first `|S|=5`.  Since `|V|>=7`, either `|Y|>=3`, already handled, or
`|Y|=2`.  In the latter case `|C|=3` or `4`.  Choose `d in S-C` and a
three-set `R subset C`.  The coefficient of `x_d x_R` in
`ell_a ell_C^3` is

```text
6a_d product_(i in R)b_i!=0.                         (24)
```

Thus the candidate in (22) is not killed by `ell_a` unless it is zero.

Now let `|S|=6`.  The cases `|Y|>=2` are identical.  For `|Y|=1`, one has
`|C|=4` or `5`, and it remains to show that

```text
phi=ell_a ell_C^2:A(S)_1 -> A(S)_4                  (25)
```

is injective.  Scale the supported variables so
`ell_a=sum_(i in S)x_i` and `ell_C=sum_(i in C)t_i x_i`, with all `t_i!=0`.

If `|C|=4`, write `S=C union {d,e}` and `u=sum u_i x_i`.  The rows on
`{d,e,i,j}` give `u_d+u_e=0`.  Rows on `d union R` and `e union R`, for
three-sets `R subset C`, give

```text
sum_(i in R)(u_d+u_i)/t_i=0,
sum_(i in R)(u_e+u_i)/t_i=0.                         (26)
```

The four reciprocal triple sums cannot all vanish; their differences would
make all `1/t_i` equal and then make `3/t_i=0`.  Hence (26) and
`u_d+u_e=0` force `u_d=u_e=0`.  The remaining `4 x 4` matrix is `J-I`, with
eigenvalues `3,-1`, so `u_C=0`.

If `|C|=5`, write `S=C union {d}`.  The `d union R` rows and the injectivity
of `W_(1,3)(5)` force `u_i=-u_d` on `C`.  The four-`C` rows then give

```text
u_d e_2(t_(C-{i}))=0                 for every i.    (27)
```

If `u_d!=0`, put `T_1=sum t_i` and `E_2=sum_(i<j)t_it_j`.  Equations (27)
make every `t_i` a root of `z^2-T_1z+E_2`; hence the five nonzero `t_i` take
at most two values.  The all-equal case gives `6t_i^2!=0`.  In the two-value
case, the multiplicities `1+4` force a zero value, while `2+3` make the root
sum and root product inconsistent (after scaling, `p=-2q` but simultaneously
`pq=-2q^2` and `E_2=-5q^2`).  Thus `u_d=0`, and then `u=0`.  This proves
(25), and completes the proof. `square`

### Theorem 2 (exhaustive support-union criterion)

For `n>=7`, the global physical Wick map is injective if and only if
condition (C) holds.

### Proof

If either support has size at most four, put that factor first in (7).
Lemma 1 gives a nonzero degree-two kernel which persists under the second
multiplication.  If both supports have size at least five, Lemma 2 reduces to
their union.

For `|V|>=7`, Lemma 3 proves injectivity.  For `|V|=6`, the only undecided
block is the square `15 x 15` six-port map (4) of the six-port theorem, so it
is injective exactly when its published physical determinant `Delta_6(a,b)`
is nonzero.  For `|V|=5`, necessarily `S=T=V`;

```text
U_b^(2):A(V)_2 -> A(V)_3
```

is an isomorphism, while `U_a^(3):A(V)_3 -> A(V)_4` is surjective with a
five-dimensional kernel.  The global kernel therefore has dimension exactly
five.

On every injective branch, the matrix has `binom(n,2)` columns.  Select that
many independent four-set rows and invert the square submatrix.  Every named
pair coordinate is therefore a constant combination of at most
`binom(n,2)` rows after the graph chart is fixed. `square`

This is a pointwise classification.  It is not a generic/function-field
inverse and has no coefficient divisor on the union-seven branch.

### Six-port sharp subcharts

When `|V|=6` and `S,T` are distinct five-sets, write

```text
S=C union {d},       T=C union {y},       |C|=4,
ell_a=sum_(i in S)x_i,       ell_b=sum_(i in C)t_i x_i+x_y. (28)
```

Direct coefficient expansion of the published determinant gives

```text
Delta_6=-9216(product_(i in C)t_i)^2 e_2(t_C).       (29)
```

If `e_2(t_C)=0`, the kernel is exactly one-dimensional, generated by

```text
(x_y-ell_C)(x_d-sum_(i in C)x_i).                    (30)
```

Here is the pointwise corank argument.  On the nonzero coefficient torus,
the gradient of `e_2` cannot vanish on `e_2=0`: its `i`-th derivative is
`T-t_i`, where `T=sum_i t_i`; if all four vanished, all `t_i=T` and then
`T=4T`, forcing every `t_i=0` in characteristic zero.  Hence (29) has
nonzero gradient at every point of its torus zero set.  If the `15 x 15`
matrix had corank at least two, its adjugate would vanish, and Jacobi's
formula would make every derivative of its determinant zero, a
contradiction.  Its corank is therefore exactly one.

For the displayed vector, put `u=x_d-sum_(i in C)x_i`.  Direct square-free
multiplication gives

```text
ell_a ell_C^2 u=-4e_2(t_C)x_C,
ell_b(x_y-ell_C)u=-ell_C^2u.                         (30a)
```

Thus `mu_(a,b)((x_y-ell_C)u)=4e_2(t_C)x_C`.  The vector is nonzero because
its `x_d x_y` coefficient is one, so it spans the one-dimensional kernel on
the whole wall.  In particular, `t_C=(1,1,1,-1)` is an exact rank-fourteen
control.

The nested six/five chart is also genuinely value-sensitive.  With

```text
a=(1,1,1,1,1,1),       b=(3,3,3,-5,6,0),            (31)
```

every scalar edge `K_ij` on the six-set is nonzero, but `Delta_6=0` and the
map has rank fourteen.  In lexicographic edge order, one kernel vector has
coefficients

```text
6 on 01,02,12;       2 on 03,13,23;
-9 on 04,14,24;     -3 on 05,15,25;
-13 on 34;           1 on 35;          12 on 45.    (32)
```

These are exact boundary controls, not hypothetical witnesses.

## 4. Exact kernels and bounded common-row selectors

### Corollary 2.1 (one-sided kernel bases)

If `r(a)>=7`, put `B=supp b`, `Z=[n]-B`, `r=|B|`, and `y_i=b_ix_i` on `B`.
Then `ker mu_(a,b)=ker U_b^(2)`.  Besides the dimensions (10), exact bases
are:

```text
r=4: (y1y2+y3y4)-(y1y4+y2y3),
     (y1y3+y2y4)-(y1y4+y2y3);
r=3: y1y2-y2y3,       y1y3-y2y3;
r=2: y1y2, and x_z(y1-y2) for z in Z;
r=1: x_z y1 for z in Z;
r=0: every pair monomial.                             (33)
```

For `r>=5` the kernel is zero.  These bases follow blockwise from (11).

### Corollary 2.2 (intrinsic full-edge-support branch)

If `K_ij!=0` for every pair on `n>=7` ports, then `mu_K` is injective.  Two
zero coordinates of `a` would make their mutual `K` edge zero, so
`|supp a|>=n-1`; similarly `|supp b|>=n-1`.  No vertex is zero in both
factors, so `S union T=[n]`.  Condition (C) follows.

### Corollary 2.3 (twenty-one-row seven-port selector)

If one factor is nonzero on all `n` ports and the other has support at least
five, every named pair `P` lies in a seven-set containing five vertices from
the smaller support, extended arbitrarily if those vertices and `P` use fewer
than seven distinct ports.  The restricted `35 x 21` map is injective by Theorem 2.
Selecting a nonsingular `21 x 21` row minor gives `m_P` as a constant
combination of at most twenty-one four-port rows.

At `n=7`, take

```text
a_i=1                    for i=1,...,7,
b_i!=0                   for i=1,...,5,
b_6=b_7=0.                                           (34)
```

Every six-set containing `{6,7}` contains only four vertices of `supp b`, so
all five relevant principal six-port determinants vanish.  Nevertheless the
global `35 x 21` map is injective and supplies `{6,7}` by at most twenty-one
common rows.  This is an exact bounded closure of an all-relevant-six-minors
singular branch.

## 5. Response and target interface

For a literal `q=2` physical response on the `h=0` branch,

```text
z_2=K,                 z_4=mu_K(B).                  (35)
```

Fix one scalar coefficient word across an `n`-port union.  If its physical
residual rows satisfy condition (C), and all `binom(n,4)` tensors used in
`z_4` have already been attached by legal constant same-`Q` graph-equation selectors,
Theorem 2 recovers every scalar pair coefficient of `B` for that word.  The
left inverse is noncircular because `K`, the graph, `Q`, and the attached
rows are fixed before the inverse is applied.

To recover the full tensor blocks, a stated family of coefficient words must
cover every desired coefficient and satisfy (C) word by word.  One scalar
word, one nonzero minor, or one rational inverse does not provide full tensor
supply.  The theorem also assumes rather than constructs the upstream
constant attachment of `z_2` and `z_4`.

## 6. Frontier and UNKNOWN remainder

```text
physical factorization mu=U_a U_b:                      PROVED;
exhaustive scalar support-union criterion (C):           PROVED;
union at least seven is coefficient-independent:        PROVED;
union six is decided by published Delta_6:               PROVED;
union five has exact kernel dimension five:              PROVED;
selectors supported on at most binom(n,2) global rows:   PROVED;
full-factor selectors supported on at most 21 rows:      PROVED;
seven-port all-principal-minors-singular pair control:   PROVED;
exact kernel with one support at least seven:             PROVED;
support at most four permits injectivity:                 FALSE;
full edge support at n>=7 permits a scalar kernel:        FALSE;
wordwise support cover on every hypothetical witness:   UNKNOWN;
legal constant attachment of all required z_2,z_4:       UNKNOWN;
tensor-valued/witness singular-locus closure:            UNKNOWN;
depth-six attachment and mixed detector outside GLD6:    UNKNOWN;
weighted permanent attachment:                          UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

The breadth is every four-subwindow of one named `n`-port union, with the
first new common-row control at `n=7`.  The depth is the residual-present
pair layer and the residual-present four-port layer.  The reconstructed data
are scalar coefficients of the residual-absent direct pair array; a complete
word cover would reconstruct the tensor blocks.  There is no transition
gauge because all rows come from one graph and one `Q`.  The ambiguity object
is the kernel of square-free multiplication.  The target implication is
conditional exact supply after legal attachment; the permanent implication
is none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_global_square_free_physical_wick_support_union_classification_and_common_row_selector.py
python -I claims/arbitrary-order/audit_global_square_free_physical_wick_support_union_classification_and_common_row_selector.py
```

The primary verifier constructs the multiplication matrices directly in
exact arithmetic, checks the support-kernel table and bases, certifies the
full-rank `35 x 21` seven-port control and its five singular principal
six-windows, replays the distinct-five determinant and kernel, and checks the
nested rank-fourteen control.  The independent no-import audit works with
subset-incidence equations and a separately implemented fraction-free
eliminator.  These finite checks audit the displayed controls; the
arbitrary-support proof is Lemmas 1--3 and the union reduction above.
