# Pinned hafnian star systems give rational edge tomography with three surplus roots

## Status

**Exact arbitrary-order characteristic-zero theorem, with conditional
`P_5/P_6/P_7` transfers and sharp singular controls.**  Let `A=(a_e)` be a
symmetric zero-diagonal weighted graph on a named `n`-set, and write

```text
h_T=haf A[T],                 h_empty=1.
```

Fix a vertex `p`.  Expanding a principal `2k`-hafnian by the partner of `p`
gives

```text
h_({p} union T)=sum_(s in T) a_ps h_(T minus s),
|T|=2k-1.                                              (1)
```

This is a linear system for the `n-1` individual edges incident to `p`,
whose coefficients are named principal `(2k-2)`-hafnians and whose
right-hand side consists of named principal `2k`-hafnians.  If

```text
2k-1 <= n-2,                                           (2)
```

then the pinned system has full column rank on a nonempty Zariski-open
chart.  Applying it at every pin recovers **every edge uniquely and
rationally** from the two named decks on a common nonempty open set.

In a residual cell with

```text
n=2q+r,             k=q+1,
```

condition (2) is exactly `r>=3`.  Hence the first two labeled residual-
hafnian layers rationally recover all edges on an open chart in:

- the `q=2` cells of `P_5`, `P_6`, and `P_7`; and
- the `q=4` cell of `P_7`.

This strictly strengthens the unpinned edge-sum system, which needs
`r>=4`, and the earlier four-hafnian Jacobian theorem, which gives only
finite algebraic recovery.  More generally, the first `2q`-hafnian deck
alone is generically finite algebraic when `r>=2`.  This covers the
`q=4,P_6` cell with `r=2`.  At `r=1` it is necessarily nonidentifying: the
fibre through the nonzero all-one deck is smooth of dimension
`binom(n,2)-n`.  For `q=6,P_7`, this gives an exact 65-dimensional local
fibre, while the next residual-hafnian layer is absent.  The same theorem
gives a 27-dimensional nonidentifying all-one fibre for `q=4,P_5`.

The qualifications are essential.  The theorem assumes that the two named
decks are legally and synchronously exposed from one witness and that the
result lies off an explicit determinant locus.  Sparse matching tori give
positive-dimensional fibres with constant two-deck data, so global recovery
is false.  Nothing here proves that GHZ forces the legal labels or the open
chart.  No `P_5/P_6/P_7` obstruction and no global Krenn--Gu conclusion is
claimed; the conjecture remains **UNRESOLVED**.

## 1. Arbitrary-order pinned partner expansion

Let `K` be a characteristic-zero field, let `V` be a named `n`-set, and fix
`p in V`.  Put `V_p=V minus {p}`.  For `T subset V_p` of size `2k-1` and
`s in V_p`, define

```text
N_p^(k)(A)[T,s] = h_(T minus s)  if s in T,
                   0              otherwise.           (3)
```

The matrix has `binom(n-1,2k-1)` rows and `n-1` columns.

### Theorem 1 (pinned star system)

For every `k>=1`,

```text
N_p^(k)(A) (a_ps)_(s in V_p)
    = (h_({p} union T))_(|T|=2k-1).                    (4)
```

### Proof

Every perfect matching of `{p} union T` contains a unique edge `{p,s}`.
After choosing that partner `s`, the remaining matching is an arbitrary
perfect matching of `T minus {s}`.  Partitioning the hafnian expansion by
the partner of `p` proves (1) and (4), with no generic hypothesis.

## 2. Square-free algebra and the Lefschetz mechanism

The partner system has a useful commutative-algebra translation.  Work in

```text
Z_n=K[z_1,...,z_n]/(z_1^2,...,z_n^2)
```

and encode the graph by

```text
Q_A=sum_(i<j) a_ij z_i z_j.
```

Because every surviving monomial in `Q_A^j` is an ordered list of the `j`
edges of a perfect matching,

```text
M(A)=exp(Q_A)=sum_(T even) h_T z_T.                    (5)
```

For a fixed pin, let

```text
L_p(A)=sum_(s != p) a_ps z_s.
```

Let `M^(p)` denote the restriction of `M` obtained by setting `z_p=0`.
Inside the square-free algebra on the `n-1` unpinned variables, (1) says

```text
L_p(A) M^(p)_(2k-2)(A)
  =sum_(|T|=2k-1) h_({p} union T) z_T.                 (6)
```

Thus the unknown star is a degree-one form multiplied by the known lower
deck into the known upper pinned deck.

At the all-one graph `J`, with `L=sum_(s != p) z_s`,

```text
M_(2k-2)(J)
  =L^(2k-2)/(2^(k-1)(k-1)!)
  =(2k-3)!! sum_(|R|=2k-2) z_R.                        (7)
```

The all-one star matrix is therefore a power-of-`L` multiplication map
from degree one to degree `2k-1` in a square-free monomial complete
intersection.  Stanley's strong Lefschetz theorem for monomial complete
intersections places its maximal-rank behavior in a wider theory; Herzog
and Popescu summarize that theorem and extensions in
[*The strong Lefschetz property and simple extensions*](https://arxiv.org/abs/math/0506537).
The next section gives a self-contained rank proof, so no Lefschetz theorem
is imported into the argument.

## 3. Full pinned rank at the all-one graph

Let `W_(1,t)(N)` be the zero-one inclusion matrix whose rows are the
`t`-subsets of an `N`-set and whose columns are its vertices.  At `J`,

```text
N_p^(k)(J)=(2k-3)!! W_(1,2k-1)(n-1).                  (8)
```

### Lemma 2 (self-contained pinned inclusion rank)

If `1<=t<=N-1`, then over a characteristic-zero field

```text
rank W_(1,t)(N)=N.                                     (9)
```

### Proof

Suppose vertex scalars `x_s` satisfy

```text
sum_(s in T) x_s=0                                     (10)
```

for every `t`-set `T`.  Given distinct vertices `u,v`, choose a
`(t-1)`-set `R` disjoint from them; this is possible because `t<=N-1`.
Subtract (10) for `R union {u}` and `R union {v}` to obtain `x_u=x_v`.
All entries are one scalar `c`, and (10) gives `t c=0`.  Characteristic
zero implies `c=0`, so the kernel is zero.

Taking `N=n-1` and `t=2k-1` shows that (2) is precisely the range in which
the all-one pinned system has full column rank.  This proof is arbitrary
order and does not enumerate subset rows.

## 4. Rational reconstruction theorem

### Theorem 3 (pinned two-deck rational edge tomography)

Fix `k>=1` and suppose `2k-1<=n-2`.  There is a nonempty Zariski-open
subset `U` of edge space such that every named edge weight is uniquely a
rational function of

```text
(h_R)_(|R|=2k-2)  and  (h_S)_(|S|=2k).                 (11)
```

The joint two-deck map has a rational left inverse on `U` and is
generically birational onto its image.

### Proof

For each pin `p`, Lemma 2 gives `n-1` rows of `N_p^(k)(J)` with nonzero
determinant.  Fix one such row set and call the corresponding determinant
`Delta_p(A)`.  Its entries are named lower-deck coordinates or zero, so it
is a polynomial in the data (11).  Since `Delta_p(J)` is nonzero,

```text
U={A: product_(p in V) Delta_p(A) != 0}                (12)
```

is a nonempty Zariski-open set containing `J`.

On `U`, restrict (4) to the selected rows and use Cramer's rule:

```text
(a_ps)_(s != p)
  =N_(p,selected)(h_(2k-2))^(-1)
     (h_({p} union T))_(T selected).                   (13)
```

This reconstructs the entire star at `p` rationally and uniquely.  Applying
(13) at every pin recovers every edge.  The overlapping star formulas agree
on the image because they all recover the original edge vector.  Moreover,
any other graph with the same deck data has the same nonzero determinants
and must solve the same invertible star systems, so it is identical.

## 5. First-deck algebraic tomography and the secondary Euler system

The pinned inverse uses two consecutive decks.  The first deck alone has a
complete generic-identifiability threshold.  Define

```text
F_(2q): A |-> (h_S)_(|S|=2q).
```

Differentiating a hafnian with respect to an edge gives

```text
partial h_S / partial a_e
  =h_(S minus e) if e subset S, and 0 otherwise.
```

At the all-one graph,

```text
dF_(2q)|_J=(2q-3)!! W_(2,2q)(n).
```

The matrix `W_(2,s)(n)` has full column rank in characteristic zero when
`s<=n-2`.  Here is a self-contained proof.  If every `s`-set edge sum is
zero, subtract the sums on `{a} union T` and `{b} union T`.  All
`(s-1)`-subset sums of `d_t=x_at-x_bt` vanish on the other `n-2` vertices.
When `s<=n-2`, comparing two such subsets makes all `d_t` equal, their sum
makes them zero, and connectivity of the line graph makes all `x_e` equal;
one `s`-set sum then makes that common value zero.

### Theorem 4 (complete first-deck surplus hierarchy)

Write `n=2q+r`.

1. If `r>=2`, then `F_(2q)` is generically finite onto its image.  The edge
   field is a finite algebraic extension of the field generated by the
   named first deck.
2. If `r=1`, then `dF_(n-1)|_J` has rank `n`, and the fibre through `J` is
   smooth of dimension

   ```text
   binom(n,2)-n.
   ```

   The map has generic fibre dimension `binom(n,2)-n`, so generic finite
   recovery from that deck is impossible.

### Proof

For `r>=2`, the displayed Jacobian and the inclusion-rank proof give full
column rank at `J`.  A maximal Jacobian minor is nonzero on a nonempty open
set.  The image has dimension `binom(n,2)`, so the induced extension of
function fields is finite algebraic.

For `r=1`, rows of `W_(2,n-1)(n)` are indexed by the omitted vertex `i`.
For an edge variation `x`, put

```text
E=sum_e x_e,          d_i=sum_(e incident to i) x_e.
```

The row omitting `i` is `E-d_i`.  Hence the kernel equations are equivalent
to `E=d_i` for every `i`.  Summing gives `nE=sum_i d_i=2E`, so
characteristic zero and `n>2` imply

```text
E=0,                 d_i=0 for every i.
```

These `n` row equations are independent: if row coefficients `c_i` vanish
on every edge column, then with `C=sum_i c_i` one has
`C-c_u-c_v=0` for every pair `u,v`; all `c_i` are equal and `(n-2)c_i=0`.
Thus the rank is `n`.  The Jacobian criterion makes `J` a smooth point of
its fibre of codimension `n`.  Surjectivity of the differential also makes
the image dimension `n`, proving the generic fibre claim.

When `q>=2` (as in every boundary cell used here), no individual edge is
even locally identifiable on this nonzero fibre.
Given a prescribed edge `uv`, choose two other vertices `a,b` and take the
alternating four-cycle tangent vector

```text
x_uv=1,       x_va=-1,       x_ab=1,       x_bu=-1,
all other x_e=0.
```

Every unsigned vertex degree sum is zero, so this vector lies in the kernel
described above, and
its `uv` coordinate is nonzero.  Hence the differential of every edge
coordinate is nonzero along the smooth fibre.  Over `C`, the analytic
implicit-function theorem integrates such tangent directions to local
arcs; algebraically, smoothness gives the corresponding formal local
deformations.

The all-one first-deck value is nonzero: every coordinate equals
`(n-2)!!` because `n-1=2q`.  Thus this positive-dimensional fibre is not a
zero-deck or sparse-support artifact.  In `q=6,P_7`, `n=13` and

```text
binom(13,2)-13=78-13=65.
```

There is also a compatible but weaker two-deck global system.  For every
`2k`-set `S`,

```text
sum_(e subset S) a_e h_(S minus e)=k h_S.              (14)
```

Indeed, each perfect-matching monomial is counted once for each of its `k`
edges.  Equivalently, (14) is Euler's identity for the degree-`k` hafnian,
or the square-free exponential identity

```text
Q_A M_(2k-2)=k M_(2k).                                 (15)
```

At `J`, its coefficient matrix is

```text
(2k-3)!! W_(2,2k)(n).                                  (16)
```

For `n=2q+r` and `k=q+1`, this unpinned condition is `r>=4`.  Pinning lowers
the threshold to `r>=3`, exactly gaining the `q=2,P_5` and `q=4,P_7` cells.

## 6. Exact fixed certificates

For the `q=2` cells, `k=3` and the all-one coefficient is
`(2k-3)!!=3`.  In lexicographic subset and vertex order, fixed maximal
minors of `W_(1,5)(N)` have

```text
N=6  (P_5): row indices 0,1,2,3,4,5;          det=5;
N=7  (P_6): row indices 0,1,2,3,6,10,15;      det=5;
N=8  (P_7): row indices 0,1,2,3,4,10,20,35;   det=5.   (17)
```

The corresponding all-one star determinants are `5*3^N`, respectively.
For `q=4,P_7`, `n=11`, `k=5`, `N=10`, and `t=9`.  All ten rows form the
complement-of-a-vertex matrix, with the fixed lexicographic certificate

```text
det W_(1,9)(10)=9,
det N_p^(5)(J)=9*(7!!)^10=9*105^10.                    (18)
```

These small exact matrices merely replay Lemma 2; the proof does not depend
on finding the certificates.

## 7. Sharp global failure controls

The open-chart hypothesis cannot be removed.

### Proposition 5 (sparse matching torus)

Fix `q>=2` disjoint edges and set every other edge to zero.  Let their
nonzero weights be `t_1,...,t_q`, constrained only by

```text
product_(i=1)^q t_i=c != 0.                            (19)
```

Then the complete principal `2q`-hafnian deck has exactly one nonzero
coordinate, equal to `c`, while every principal `(2q+2)`-hafnian is zero.
The full two-deck data are constant on a `(q-1)`-dimensional algebraic
torus.

### Proof

The supported graph has exactly one matching of size `q`, namely the chosen
edge set, and has no matching of size `q+1`.  Its only nonzero lower-deck
coordinate is the hafnian on the `2q` endpoints, equal to the product (19).

Thus the joint deck map is not globally finite, injective, or rationally
invertible.  For `q=2`, the concrete family

```text
a_01=t,       a_23=t^(-1),       all other edges zero
```

has `h_{0,1,2,3}=1`, all other four-hafnians zero, and every six-hafnian
zero.  A one-edge affine line supplies the still simpler all-zero-deck
control.

## 8. Residual-cell translation and label capacity

In a cell with `m` blocker ports and `q` residual ports, the nonroot graph
has `n=m+q=2q+r` vertices and `r=m-q` roots.  The root-root deletion
filtration leaves nonroot orders

```text
2q, 2q+2, 2q+4, ... .                                  (20)
```

Theorem 3 uses exactly the first two layers and succeeds whenever `r>=3`.

| cell | `q` | `r` | `n` | two decks | exact consequence if named |
|---|---:|---:|---:|---|---|
| `P_5` | 2 | 3 | 7 | `h_4,h_6` | all 21 edges rationally recovered on `U` |
| `P_5` | 4 | 1 | 9 | `h_8` | generic fibre dimension 27; no edge locally identified |
| `P_6` | 2 | 4 | 8 | `h_4,h_6` | all 28 edges rationally recovered on `U` |
| `P_6` | 4 | 2 | 10 | `h_8` | all 45 edges generically finite algebraic |
| `P_6` | 6 | 0 | 12 | no root deck | root-selector mechanism unavailable |
| `P_7` | 2 | 5 | 9 | `h_4,h_6` | all 36 edges rationally recovered on `U` |
| `P_7` | 4 | 3 | 11 | `h_8,h_10` | all 55 edges rationally recovered on `U` |
| `P_7` | 6 | 1 | 13 | `h_12` | generic fibre dimension 65; no edge locally identified |

For the `q=2,P_6` row, the full consecutive `h_4,h_6` label set exceeds the
81 root channels, but the `h_4` deck alone fits.  The legal rank-70 chart in
`P6_FOUR_ROOT_FULL_H4_SENSOR_AND_TARGET_INCIDENCE_BOUNDARY.md` exposes all of
it and therefore realizes the generically finite first-deck conclusion
relative to known companion blocks.

For the `q=2` cells, the complete two-deck label counts versus the full
root-tensor dimensions are

```text
P_5: binom(7,4)+binom(7,6) = 42  > 3^3 = 27;
P_6: binom(8,4)+binom(8,6) = 98  > 3^4 = 81;
P_7: binom(9,4)+binom(9,6) = 210 <= 3^5 = 243.         (21)
```

The legal mixed-root ledger also contains every shallower same-parity
layer, even when rational reconstruction needs only the first two.  Thus

```text
q=2,P_5: 35+7       = 42;
q=2,P_6: 70+28+1    = 99  > 81;
q=2,P_7: 126+84+9   = 219 <= 243.                      (21a)
```

In particular, the nine depth-one `h_8` nuisance columns in `q=2,P_7`
raise the actual shallow selector load from 210 to 219, but it still fits
the 243-dimensional five-root tensor.  The companion construction in
`P7_FULL_MIXED_ROOT_219_LABEL_SENSOR_AND_PINNED_STAR_GATING_BOUNDARY.md`
attains rank 219 on a legal graph-side chart.  That result supplies the
missing relative label selector on a nonempty open set, but it does not
place a GHZ witness in that open set; at its displayed integer point the
sensor image is actually disjoint from the nonzero diagonal target space.

For `q=4,P_7`, the count is

```text
binom(11,8)+binom(11,10)=176 > 3^3=27.                 (22)
```

The higher-residual mixed counts are

```text
q=4,P_5: binom(9,8)=9 > 3^1=3;
q=4,P_6: binom(10,8)+binom(10,10)=46 > 3^2=9;
q=6,P_7: binom(13,12)=13 > 3^1=3.
```

The named deck polynomials are linearly independent as formal functions:
the two orders have different homogeneous degrees, and within one order
each matching monomial has the unique vertex support indexing its principal
hafnian.  Therefore a universal graph-independent **linear** selector from
one `3^r`-dimensional root tensor cannot expose every named coordinate when
the deck count exceeds `3^r`.  Only `q=2,P_7` passes this raw full-deck
capacity test.  The count alone does not construct the selector; the fixed
rank-219 construction cited above supplies it in the `q=2,P_7` case.

This count concerns direct formal label exposure.  It does not exclude a
smaller tailored set of minors, compressed nonlinear recovery, or a
synchronized stack of legal jets.  In particular, Theorem 3 is conditional
on named data and is not itself a root-tensor selector construction.

## 9. Exact frontier and UNKNOWN wall

```text
pinned arbitrary-order partner system:            PROVED;
first-deck generic finite recovery for r>=2:       PROVED;
first-deck smooth positive fibres for r=1:         PROVED;
full pinned rank for r>=3:                         PROVED;
rational unique two-deck inverse on open U:        PROVED;
q=2 P_5/P_6/P_7 inverse from named h4,h6:          PROVED;
q=4 P_6 finite algebraic recovery from named h8:   PROVED;
q=4 P_5 first-deck recovery:                       NONIDENTIFYING (DIM 27);
q=4 P_7 inverse from named h8,h10:                 PROVED;
unpinned Euler inverse for r>=4:                   PROVED;
global two-deck recovery:                          FALSE;
q=6 P_7 first-deck recovery:                       NONIDENTIFYING (DIM 65);
q=6 P_7 next-layer route:                          UNAVAILABLE (r=1);
q=6 P_6 root-deck route:                           UNAVAILABLE (r=0);
single-tensor full direct labels outside q=2 P_7: DIMENSIONALLY EXCLUDED;
q=2 P_7 full direct-label sensor:                  ATTAINED ON LEGAL OPEN;
q=2 P_7 sensor compatible with nonzero GHZ target: UNKNOWN;
legal sufficient deck/minor exposure for GHZ:      UNKNOWN;
GHZ forced off every pinned determinant locus:     UNKNOWN;
singular-locus stratification:                     NONEMPTY, CLASSIFICATION OPEN;
P_5/P_6/P_7 obstruction:                          UNKNOWN;
global Krenn--Gu:                                  UNRESOLVED.         (23)
```

The pinned determinant boundary is refined in
`PINNED_H4_STAR_TORUS_CIRCUIT_GIRTH_AND_P6_CUBIC_ESCAPE.md`: on the
eight-vertex `P_7` shore every full-edge-torus circuit uses at least five
columns, while an exact `P_6` cubic-resonance graph has an all-edge-nonzero
two-column circuit.  Thus torus nonvanishing is a genuine theorem in the
first four `P_7` circuit sizes but is not a general determinant criterion.

No graph supports, words, parameter grids, or finite fields were searched.
The finite computations below evaluate only fixed exact matrices and fixed
symbolic identities certifying the general proof.

## Replay

```powershell
uv run --with sympy python verify_pinned_hafnian_star_system_and_rational_edge_tomography.py
python audit_pinned_hafnian_star_system_and_rational_edge_tomography.py
python -m py_compile verify_pinned_hafnian_star_system_and_rational_edge_tomography.py audit_pinned_hafnian_star_system_and_rational_edge_tomography.py
uv run --with ruff ruff check verify_pinned_hafnian_star_system_and_rational_edge_tomography.py audit_pinned_hafnian_star_system_and_rational_edge_tomography.py
```

The primary verifier expands the symbolic pinned and Euler identities,
checks the exact inclusion ranks and determinants (17)--(18), and
reconstructs every star of fixed nonconstant `P_5/P_6/P_7` examples,
including the `q=4` case.  The independent standard-library audit uses
separate cached hafnian and rational-elimination code and verifies the same
reconstructions and sparse matching controls without project imports or a
computer-algebra package.
