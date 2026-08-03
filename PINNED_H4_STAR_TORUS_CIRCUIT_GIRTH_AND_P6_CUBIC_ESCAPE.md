# P7 pinned-star failure has torus circuit girth five, but P6 has a cubic escape

## Status

**Exact characteristic-zero singular-boundary theorem and nonzero P6
control.**  Let `B` be the graph on the vertices other than a fixed pin, and
form the `h_4` pinned-star coefficient matrix

```text
N_B[T,i]=h_(T minus {i})  if i in T,
         =0               otherwise,      |T|=5.      (1)
```

For the eight-vertex shore occurring in the `q=2,P_7` cell, a rank drop at a
full edge-torus point is necessarily diffuse:

```text
B_ij!=0 for every i<j,  N_B x=0,  x!=0
                  => |supp(x)|>=5.                    (2)
```

Equivalently, every collection of at most four columns of `N_B` is linearly
independent on the full edge torus.  This strengthens the earlier theorem
that the zero `h_4` deck cannot meet that torus.  It does not prove that
`N_B` has full rank there; circuits of sizes five through eight remain open.

The eight-vertex threshold is sharp in the immediately relevant smaller
case.  On seven vertices there is an exact graph over `Q(omega)`,
`omega^2+omega+1=0`, with **every edge nonzero** for which

```text
rank N_B=6<7,
ker N_B=span(0,0,0,0,0,1,1).                         (3)
```

Both its four- and six-hafnian decks have nonzero coordinates.  Thus the
`P_6` pinned determinant can fail away from every coordinate hyperplane;
edge-torus nonvanishing alone cannot force that inverse chart.  The escape
is built from the unique cubic-resonance normal form of a five-vertex
all-nonzero zero-`h_4` deck.

For a one-dimensional target-incidence cofactor **vector** line, every fixed
maximal pinned minor is homogeneous of degree equal to the number of columns.
It therefore either vanishes on the whole line or is nonzero at every nonzero
point of the line.  If a `P_7` cofactor line is contained in the pinned
rank-drop locus, every full-edge-torus realization on that line must carry a
kernel circuit of size at least five.  In `P_6`, the cubic escape proves that
line containment cannot be excluded from torus support alone.

Nothing here proves that a GHZ-compatible cofactor line contains the P6
control, or excludes the remaining P7 circuits.  The incidence-line
realizability problem, `P_6/P_7`, and global Krenn--Gu remain **UNKNOWN** or
**UNRESOLVED** as stated in the final wall.

## 1. Square-free Lefschetz form of the pinned matrix

Work over a characteristic-zero field `K` and put

```text
Z=K[z_1,...,z_N]/(z_1^2,...,z_N^2),
Q_B=sum_(i<j) B_ij z_i z_j,
M_4(B)=Q_B^2/2=sum_(|R|=4) h_R z_R.                   (4)
```

For `ell_x=sum_i x_i z_i`, equation `N_Bx=0` is exactly

```text
ell_x M_4(B)=0 in degree five.                        (5)
```

Thus a rank-drop vector is a degree-one annihilator of the square of the
matching quadratic.  This places the question in the strong-Lefschetz and
Artinian-complete-intersection setting, but the torus circuit theorem below
is elementary and does not import a general Lefschetz result.

Diagonal vertex scaling preserves support size.  If

```text
B_ij -> d_i d_j B_ij,       x_i -> d_i x_i,           (6)
```

then every row of (5) is multiplied by the product of its five vertex
scales.  Kernel supports are therefore intrinsic to the graph's vertex-gauge
orbit.

## 2. Two auxiliary torus lemmas

### Lemma 1 (zero four-deck torus exclusion)

On at least six vertices, an all-zero principal `h_4` deck forces some edge
weight to vanish.

### Proof

Assume all edges are nonzero and fix vertices `1,2`.  From
`h_{12ij}=0`,

```text
B_ij=-(B_1i B_2j+B_1j B_2i)/B_12.                   (7)
```

Put `r_i=B_2i/B_1i`.  Substitution in `h_{1ijk}=0` gives

```text
0=-(2/B_12)B_1i B_1j B_1k(r_i+r_j+r_k).              (8)
```

There are at least four ratios.  Comparing triple sums makes all of them
equal, and one triple gives `3r_i=0`, contradicting nonzero edges.

### Lemma 2 (the triangle-star map is injective on the edge torus)

Let `C` be an all-edge-nonzero graph on `m>=5` vertices.  The map

```text
P_C:K^m -> K^{binom(m,3)},
(P_Cv)_{ijk}=v_i C_jk+v_j C_ik+v_k C_ij             (9)
```

is injective.

### Proof

Suppose `P_Cv=0`.  If two entries `v_i,v_j` vanish, a triangle containing
them and one nonzero entry forces `C_ij=0`.  Thus `v` has at most one zero.

If no entry vanishes, divide the equation on `{i,j,k}` by `v_i v_j v_k`
and put

```text
c_ij=C_ij/(v_i v_j).
```

Every triangle sum `c_ij+c_ik+c_jk` is zero.  The two-subset versus
three-subset inclusion matrix has full column rank for `m>=5`.  Indeed, fix
`1,2`.  The triangle `{1,2,k}` gives

```text
c_1k+c_2k=-c_12.                                     (10a)
```

For three vertices `k,l,r` outside `{1,2}`, comparison of the triangles
`{1,k,l}` and `{2,k,l}` shows that the differences
`c_1k-c_2k` have pairwise opposite sums; three such indices force every
difference to vanish.  Equation (10a) then makes all `c_1k,c_2k` equal,
the triangles `{1,k,l}` make every `c_kl=c_12`, and `{k,l,r}` gives
`3c_12=0`.  Hence all `c_ij=0`, a contradiction.

If exactly one entry, say `v_0`, is zero, triangles `{0,i,j}` give

```text
C_0i/v_i+C_0j/v_j=0                                  (10)
```

for every pair among at least four remaining vertices.  Three such vertices
force all these nonzero ratios to be zero, again a contradiction.

## 3. The sharp five-vertex cubic zero-deck

Lemma 1 is sharp at five vertices.  Its exceptional torus chart has a simple
classification.

Take four vertices and name their six edges

```text
C_12=a, C_13=b, C_14=c,
C_23=d, C_24=e, C_34=f.                               (11)
```

Adding a fifth vertex with star vector `v` makes all four-hafnians containing
that vertex zero exactly when

```text
P_C v=0,
P_C=[
  0 f e d
  f 0 c b
  e c 0 a
  d b a 0
].                                                    (12)
```

The remaining four-hafnian is

```text
h_1234=af+be+cd.                                      (13)
```

Put `U=af,V=be,W=cd`.  Direct expansion gives

```text
det P_C=U^2+V^2+W^2-2UV-2UW-2VW.                     (14)
```

On `U+V+W=0`, this becomes

```text
det P_C=4(V^2+VW+W^2).                                (15)
```

### Proposition 3 (five-vertex cubic-resonance classification)

If every edge of a five-vertex graph is nonzero and every principal
four-hafnian vanishes, then for either primitive cube root `omega`, after
choosing four of the vertices,

```text
(af,be,cd)=lambda(omega^2,omega,1),   lambda!=0.       (16)
```

Conversely, (16), together with a nonzero vector in `ker P_C` as the fifth
star, constructs such a graph.  The kernel of `P_C` is exactly
one-dimensional: a three-by-three principal minor is twice a product of
three nonzero edges, so `rank P_C>=3`.  Every nonzero kernel vector has every
coordinate nonzero, since deleting a hypothetical zero coordinate would
leave an invertible three-by-three principal system.

Over an algebraic closure, vertex scaling and permutation give the canonical
representative

```text
a=1, b=omega, c=1, d=1, e=1, f=omega^2,
ker P_C=span(omega,omega^2,omega^2,1).                (17)
```

### Proof

The fifth star is nonzero in every coordinate, so (12) is singular.  Equations
(13)--(15) force `rho=V/W` to satisfy `rho^2+rho+1=0`, yielding (16).
Conversely, (13)--(15) vanish.  The rank observation gives a kernel line;
using a nonzero vector on that line gives all five remaining zero-deck
equations.  Substitution verifies (17).  The vertex-scaling normalization is
the solution of four nonzero edge-normalization equations; over an
algebraic closure the required roots exist.

This cubic orbit is a genuine cancellation stratum, not a low-matching-number
support: every one of its ten edges is nonzero.

## 4. P7 torus circuit girth

### Theorem 4 (no pinned circuit of size at most four)

Let `B` be an all-edge-nonzero graph on eight named vertices.  If `N_Bx=0`
for the matrix (1), then either `x=0` or

```text
|supp(x)|>=5.                                         (18)
```

### Proof

Write `S=supp(x)` and `C=V minus S`.

#### Supports one and two

If `|S|=1`, take a five-set consisting of its one supported vertex and any
four vertices of the seven-set `C`.  Equation (1) says every principal
four-hafnian on `C` is zero.  Lemma 1 contradicts the edge torus.

If `|S|=2`, do the same using either one supported vertex and four vertices
of the six-set `C`.  Again the complete four-deck on `C` is zero, contrary to
Lemma 1.

#### Support three

Now `|C|=5`.  Five-sets meeting `S` once show that every four-hafnian on `C`
is zero; this is allowed only on the cubic cancellation stratum of
Proposition 3.

For `a in S`, let `v_a=(B_ai)_{i in C}` be its nonzero cross-star.  A five-set
containing `a,b in S` and a triple `R subset C` gives

```text
x_a (P_C v_b)_R+x_b(P_C v_a)_R=0.                    (19)
```

Put `w_a=P_Cv_a/x_a`.  Equations (19) say `w_a+w_b=0` for every pair in a
three-set, hence every `w_a=0`.  Lemma 2 makes every `v_a=0`, contradicting
the edge torus.

#### Support four

Here `|C|=4`.  The one-support equations give `h_C=0`.  The pair equations
again imply

```text
P_Cv_a=0             for every a in S.                (20)
```

The four-by-four matrix `P_C` in (12) has rank at least three because its
three-by-three principal minors are nonzero.  Since every `v_a` is nonzero,
it must have rank exactly three.  Write

```text
ker P_C=span(k),       v_a=lambda_a k,
lambda_a!=0,           k_i!=0.                        (21)
```

Let `D_ab=B_ab` be the edges inside `S`.  On a five-set
`{a,b,c,i,j}` with three vertices in `S` and two in `C`, equation (1) is

```text
C_ij A_abc+2k_i k_j B_abc=0,                          (22)

A_abc=x_a D_bc+x_b D_ac+x_c D_ab,
B_abc=x_a lambda_b lambda_c
     +x_b lambda_a lambda_c
     +x_c lambda_a lambda_b.
```

The two six-vectors `(C_ij)` and `(k_i k_j)` are linearly independent.  If
`C_ij=mu k_i k_j`, then `P_Ck=0` would read

```text
3mu k_i k_j k_l=0
```

on every triple, impossible on the edge torus.  Thus (22) forces
`B_abc=0` for every triple in `S`.  Dividing by the nonzero product of the
three lambdas gives

```text
x_a/lambda_a+x_b/lambda_b+x_c/lambda_c=0              (23)
```

for all four triples of a four-set.  Their incidence matrix has determinant
`-3`, so every ratio is zero, contradicting `a in supp(x)`.

All four possible support sizes are excluded, proving (18).

The theorem does not classify supports five through eight.  In particular,
it is a circuit-girth statement, not a proof that the pinned determinant is
a unit after localizing all edge coordinates.

## 5. Exact P6 full-torus escape

Let `omega^2+omega+1=0`.  On vertices `0,...,4`, use the canonical cubic
zero-deck graph

```text
C_01=1,       C_02=omega,   C_03=1,
C_12=1,       C_13=1,       C_23=omega^2,
C_04=omega,   C_14=omega^2, C_24=omega^2, C_34=1.    (24)
```

Add vertices `5,6` and set

```text
C_i5=1,       C_i6=-1        (0<=i<=4),
C_56=1.                                                (25)
```

Every one of the 21 edge weights is nonzero.

### Theorem 5 (P6 cubic pinned escape)

For the seven-vertex graph (24)--(25),

```text
rank N_C=6,
ker N_C=span(e_5+e_6).                                (26)
```

The deck is not the zero deck; for example,

```text
h_0125=omega+2,
h_012356=-6.                                          (27)
```

### Proof

Every four-subset of `{0,...,4}` has hafnian zero by Proposition 3.  For a
five-set containing exactly one of `5,6`, equation `N_C(e_5+e_6)=0` is
therefore a zero four-hafnian on the cubic core.  For a five-set containing
both, its two terms are hafnians on one added vertex and three core vertices.
Such a hafnian is linear in the added vertex's core star, and the two stars
in (25) are negatives.  The terms cancel.  These are all five-set types, so
`e_5+e_6` lies in the kernel.

One fixed six-by-six minor is nonzero in the replay, proving rank at least
six; the displayed kernel proves rank at most six.  Direct matching expansion
gives (27).

This is a failure of one pinned coefficient matrix.  It does not assert that
the complete named `h_4,h_6` deck has a positive-dimensional graph fibre:
other pins and lower-deck coordinates involving the physical pin can still
carry information.

## 6. Incidence-line consequences

Suppose a root-sensor/target-incidence calculation leaves a one-dimensional
vector line of named cofactors,

```text
K_Gamma=K c.                                          (28)
```

The entries of a pinned matrix are linear coordinates on its lower deck.  A
fixed `r x r` pinned minor is homogeneous of degree `r`, so

```text
Delta(t c)=t^r Delta(c).                              (29)
```

Thus the nonzero incidence line is either entirely inside that minor's open
chart or entirely inside its determinant hypersurface.  More general affine
one-parameter slices still have the weaker degree-at-most-`r` finite-root
bound.

- If one nonzero incidence vector makes a selected minor nonzero, the same
  minor is nonzero everywhere else on that vector line.  Its degree is eight
  for the P7 eight-column system and seven for P6.
- If the whole realizable line lies in the pinned determinantal locus, then
  at every P7 full-edge-torus point Theorem 4 forces every kernel dependency
  to use at least five star columns.  Any proposed singular alternative with
  a one-, two-, three-, or four-label dependency is therefore a coordinate
  boundary, not a torus point.
- In P6, Theorem 5 shows that a two-column circuit can occur with every edge,
  and with both relevant deck orders nonzero.  The cubic-resonance factor in
  (16) is an exact algebraic alternative that a target-incidence argument
  must exclude; mere nonvanishing of edge coordinates is insufficient.

For P7, the surviving circuit sizes `5,6,7,8` are not yet classified.  They
are the precise torus singular alternatives to intersect with the
determinant-cleared hafnian-realizability equations on the target cofactor
line.

## 7. Exact wall

```text
five-vertex all-nonzero zero-h4 classification:      CUBIC RESONANCE;
triangle-star injectivity on >=5 edge-torus vertices: PROVED;
P6 seven-shore full-edge-torus pinned rank drop:      CONSTRUCTED;
P6 control has nonzero h4 and h6 coordinates:         PROVED;
P7 eight-shore torus circuits of size <=4:            IMPOSSIBLE;
P7 eight-shore torus circuits of size 5..8:           UNKNOWN;
P7 pinned matrix full rank on entire edge torus:      UNKNOWN;
target cofactor line not contained in pinned locus:   UNKNOWN;
GHZ excludes the P6 cubic resonance:                  UNKNOWN;
P6/P7 obstruction:                                   UNKNOWN;
global Krenn--Gu:                                     UNRESOLVED.       (30)
```

No supports, graphs, finite fields, words, or parameter grids were searched.
The replay evaluates only the displayed symbolic identities and fixed exact
matrices.

## Replay

```powershell
uv run --with sympy python verify_pinned_h4_star_torus_circuit_girth_and_p6_cubic_escape.py
python audit_pinned_h4_star_torus_circuit_girth_and_p6_cubic_escape.py
python -m py_compile verify_pinned_h4_star_torus_circuit_girth_and_p6_cubic_escape.py audit_pinned_h4_star_torus_circuit_girth_and_p6_cubic_escape.py
uv run --with ruff ruff check verify_pinned_h4_star_torus_circuit_girth_and_p6_cubic_escape.py audit_pinned_h4_star_torus_circuit_girth_and_p6_cubic_escape.py
```

The primary verifier checks (14)--(17), the auxiliary inclusion ranks, the
canonical five-vertex zero deck, the P7 circuit proof matrices, and the exact
rank-six P6 control over `Q(omega)`.  The independent standard-library audit
uses its own rational-pair arithmetic for `Q(omega)`, recursive hafnians, and
field Gaussian elimination.  Neither imports the other or any project code.
