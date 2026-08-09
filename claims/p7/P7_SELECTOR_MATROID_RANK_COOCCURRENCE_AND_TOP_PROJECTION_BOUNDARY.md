# P7 selector matroids, rank co-occurrence, and the top-projection boundary

## Status

**Exact characteristic-zero theorems and countermodels.**  The clean-window
theorem forces a graph-side four-port window in the canonical seven-blocker
cell.  This note tests the two shortest ways one might try to turn that window
into a P7 obstruction:

1. force the window to occur at a root pair with two independent companion
   selectors; or
2. combine the top coefficients from many overlapping windows and eliminate
   the hidden lower faces.

Neither implication follows from the current hypotheses.

- Three simultaneous canonical pure `P_7` matrices are constructed in which
  the only root pairs with lower-frame rank two have **zero** marked-shore
  products.  Every nonzero clean shore occurs at rank one.
- A positive weighted-Laplace theorem identifies when this cannot happen: a
  balanced edge weighting on the graph of rank-at-least-two root pairs forces
  a rank-two clean shore.  For five roots the uncovered tangent patterns are
  the all-axis multiplicities `4+1`, `3+1+1`, and `2+2+1`.
- Even granting all six clean four-windows in one pure chart and independent
  top selectors on each, their twelve top coefficients together with the
  visible pure two-port aggregate are Zariski dense.  Their elimination ideal
  is zero.  Hence no polynomial obstruction using only those data follows
  from marked Laplace plus two-residual dual-Wick.

The surviving route is narrower: expose actual pair/empty faces, or use
mixed-colour/shared-block equations that couple the scalar charts.  These
results do not construct a full coloured P7 restriction and do not prove the
Krenn--Gu conjecture.  P7 and the global conjecture remain **UNRESOLVED**.

## 1. The selector matroid of a four-window

Fix `W={1,2,3,4}`.  Its partition-closed two-residual response state is

```text
c_W=(m_empty,z_empty,(m_e)_(e in E(K4)),
                    (z_e)_(e in E(K4)),m_W,z_W).       (1)
```

There are sixteen coordinates, or fourteen unknown coordinates after the
normalizations `m_empty=1` and `z_empty=h` are known.  A legal shore/root
sensor `alpha` has a shore factor `s_(alpha,f)` and a companion form
`g_(alpha,f)` for each deletion face `f`.  After a legal root probe
`ell_alpha`, its observation row is

```text
O_(alpha,f)=s_(alpha,f) ell_alpha(g_(alpha,f)).         (2)
```

The selector theorem from the preceding note says that partition closure is
equivalent to the combined matrix `O` having full column rank on the desired
faces.  This defines the **deletion-face selector matroid**: the ground set is
the response-face family, and independence is column independence in `O`.

### Proposition 1 (private-selector criterion)

A family of legal sensors recovers every desired face if its sensor/face
support bipartite graph has a square subgraph with a unique perfect matching
and all entries on that matching are nonzero.  Equivalently, after permuting
rows and columns, a triangular family of private selectors with nonzero
diagonal is sufficient.

Proof.  In the determinant expansion of the square submatrix, the unique
perfect matching supplies the only nonzero monomial.  Its product is nonzero,
so the submatrix is invertible.  This is a support-level sufficient condition,
not a necessary one: several determinant monomials may also sum nontrivially.

### The marked-overlay pair block

In edge order

```text
12,13,14,23,24,34,                                    (3)
```

the four standard marked star observations have matrix

```text
A = [1 1 1 0 0 0]
    [1 0 0 1 1 0]
    [0 1 0 1 0 1]
    [0 0 1 0 1 1].                                    (4)
```

Over characteristic zero,

```text
rank A=4,
ker A={n(s,t):s,t in k},
n(s,t)=(-s-t,s,t,t,s,-s-t).                           (5)
```

For an additional legal jet row `b=(b_e)`, define its defect signature

```text
sigma(b)=(-b_12+b_13+b_24-b_34,
          -b_12+b_14+b_23-b_34).                      (6)
```

These are exactly the two pairings of `b` with the kernel basis
`n(1,0),n(0,1)`.

### Theorem 2 (exact pair-defect completion criterion)

Two extra rows `b,c` complete the six pair faces if and only if

```text
det [sigma(b);sigma(c)] !=0.                           (7)
```

If the direct pair family `M` and residual-present pair family `Z` are both
hidden behind separate copies of (4), added legal jets must span the
four-dimensional defect

```text
ker A direct_sum ker A.                               (8)
```

Empty- and top-face selectors do not change this pair defect.

Proof.  Since `A` has row rank four, adjoining two rows gives rank six exactly
when their restrictions to `ker A` are independent.  In the displayed kernel
basis those restrictions are (6), proving (7).  The two response families are
independent column blocks until a further legal equation couples them, giving
(8).

### Proposition 3 (legal residual response in the pair kernel)

Set the direct port matrix `B=0`, the residual edge `h=0`, and use residual
incidence rows

```text
a=lambda(1,-1,0,0),
b=(0,0,1,-1).                                         (9)
```

Then the two-residual Gram response has pair vector

```text
z_pair=lambda(0,1,-1,-1,1,0)=lambda n(1,-1).          (10)
```

Moreover

```text
M=1,
z_empty=m_W=z_W=0,                                    (11)
```

and all four marked star observations vanish for every `lambda`.

Proof.  The pair response is

```text
K_ij=a_i b_j+b_i a_j.                                 (12)
```

Direct substitution gives (10).  Equation (5) then kills every star sum.
With no direct port edge and no residual edge, the other coefficients in
(11) vanish.  Thus this is an actual one-parameter matching response, not a
formal observation-space deformation.

Consequently one clean window, both of its top selectors, and all four
standard star observations still do not close the pair faces.  A new lower
jet helps only if its signature leaves `rowspace(A)`.

## 2. Overlapping windows as a global observation matrix

For a family `mathcal W` of four-windows on a common port set, define a matrix
with rows `(W,i)`, columns global pair faces `e`, and

```text
(A_mathcalW)_((W,i),e)=1 iff i in e subset W.          (13)
```

Let `W_0` be a target window.  Pair faces outside `W_0` are nuisance columns.

### Theorem 4 (target recovery with nuisance faces)

All six pair faces of `W_0` are linearly recoverable from the marked-window
observations if and only if

```text
rank A_mathcalW
 - rank (A_mathcalW)_(E outside E(W_0)) = 6.           (14)
```

Every global pair face is recoverable if and only if `A_mathcalW` has full
column rank.

Proof.  Mod out the observation column space generated by nuisance faces.
The remaining six columns are recoverable exactly when their images are
independent in the quotient.  The dimension of their joint image is the rank
difference in (14).

A useful sufficient condition is link-span completeness: for every port `i`,
the incidence vectors of

```text
{W minus {i}: W in mathcal W, i in W}                  (15)
```

span all coordinates incident to `i`.  Then every vector in `ker A_mathcalW`
vanishes on every star, hence on every pair.  In particular, the family of all
four-windows inside a port set of order at least five has full pair-face rank
in characteristic zero.

Current P7 theory forces one clean window, not this link cover.  Theorem 4 is
therefore a sufficient target for a future multi-shore theorem, not an
available P7 deduction.

## 3. Marked shore and lower-frame rank need not co-occur

Let `rho(I)` be the exact lower-frame rank of a root pair `I`.  Take tangent
covectors

```text
a_0=a_1=e_0^*,
a_2=a_3=e_1^*,
a_4=e_2^*.                                             (16)
```

The lower-frame classification gives

```text
rho(01)=rho(23)=2,
rho(I)=1 for every other pair I.                       (17)
```

Indeed, a pair containing axis colours `A` has rank `3-|A|`.

### A five-by-five cancellation block

Consider

```text
H = [u_0  1 0 0 0]
    [u_1  0 1 0 0]
    [u_2  0 0 1 0]
    [u_3  0 0 0 1]
    [  1  x y z w],                                    (18)
```

subject to

```text
1+u_0 x+u_1 y=0,
1+u_2 z+u_3 w=0.                                      (19)
```

The first column is marked.  Direct permanental Laplace expansion gives

```text
per H=1+u_0x+u_1y+u_2z+u_3w=-1.                       (20)
```

For `I=01`, a nonzero two-column complementary permanent can use only the
first identity block; its marked three-by-three shore factor is the second
expression in (19), hence zero.  For `I=23`, the roles reverse and the shore
factor is the first expression in (19), again zero.  Thus every marked-shore
product with `rho(I)>=2` vanishes although `per H` is nonzero.

### Theorem 5 (simultaneous canonical pure-P7 countermodel)

Let the seven physical blockers be

```text
t=012; u_01,v_01,u_02,v_02,u_12,v_12.                 (21)
```

Use the following three pure root matrices, with rows `r_0,...,r_4`:

```text
H_0, columns (t,u_01,v_01,u_02,v_02):
[-1 1 0 0 0]
[ 0 0 1 0 0]
[-1 0 0 1 0]
[ 0 0 0 0 1]
[ 1 1 0 1 0]

H_1, columns (t,u_12,v_12,u_01,v_01):
[ 0 1 0 0 0]
[-1 0 1 0 0]
[ 0 0 0 1 0]
[-1 0 0 0 1]
[ 1 0 1 0 1]

H_2, columns (t,u_02,v_02,u_12,v_12):
[-1 1 0 0 0]
[-1 0 1 0 0]
[-1 0 0 1 0]
[ 1 0 0 0 1]
[ 1 1 0 1 0].                                        (22)
```

Then:

1. `per H_c=-1` for all three colours;
2. every marked shore complementary to `01` or `23` has zero product;
3. some marked shores at rank-one pairs are nonzero;
4. the columns in (22) are the three coordinate slices of one canonical
   blocker-covector system of exact type
   `012,01,01,02,02,12,12`;
5. after adjoining residual rows `q_0,q_1` as an identity matching to the two
   blockers missing colour `c`, each pure seven-by-seven source--blocker
   permanent remains `-1`.

Proof.  Each matrix is a specialization of (18)--(19), so (20) proves the
first claim and the block argument proves the second.  A direct minor in
`H_0`, for example `I=02` with complementary unmarked columns
`u_01,u_02`, has product one, proving the third.

To assemble the physical blocker covectors, use the `c`-column of `H_c` as
the colour-`c` coordinate at that blocker and put zero in a missing colour.
The row covectors at `t` span all three coordinates; the two blockers of each
double type span exactly their named coordinate plane.  Hence the incidence
profile is exactly (21).  On a pure colour, the two residual rows and the two
missing-colour blockers form an identity block disjoint from `H_c`.  The
seven-by-seven permanent is therefore `per(H_c)=-1`.

Finally take the fixed root vectors to be `(1,1,1)` and define the
root--blocker bilinear blocks by

```text
B_(i,b)=a_i tensor r_(i,b),                            (23)
```

where `r_(i,b)` is the assembled blocker covector.  Since `a_i(1,1,1)=1`,
the fixed root rows are exactly (22), while tangent directions lie in
`ker(a_i)`.  Thus the pure matrices and lower-frame axis pattern belong to
one legal canonical bilinear system.

This is a pure P7/common-block countermodel, not a full mixed-colour GHZ
restriction.

## 4. A positive balanced-shore theorem

For one nonzero pure matrix `H`, let `G_rho` be the graph on its five roots
whose edges are the pairs `I` with `rho(I)>=2`.  Give its edges scalar weights
`omega_I` and suppose every vertex has the same nonzero weighted degree `d`:

```text
sum_(I contains k) omega_I=d for every root k.         (24)
```

### Theorem 6 (balanced weighted Laplace forces co-occurrence)

If (24) holds and `per H !=0`, then some marked shore complementary to an
edge of `G_rho` has nonzero product.  In other words, a clean four-window and
rank-at-least-two lower frame co-occur.

Proof.  For a root pair `I`, let `S_I` be the sum of its marked shore products.
A full matching `sigma` contributes to `S_I` exactly when the root matched to
the marked column is not in `I`.  Therefore its coefficient in
`sum_I omega_I S_I` is

```text
sum_(I not containing k) omega_I
 =sum_I omega_I-d.
```

The handshake identity gives `sum_I omega_I=5d/2`, so every full matching has
coefficient `3d/2`.  Hence

```text
sum_(I in E(G_rho)) omega_I S_I=(3d/2) per H !=0.      (25)
```

Some summand, and then some individual shore product inside it, is nonzero.

For the five-root lower-frame rank graph, a non-axis tangent covector is
adjacent in `G_rho` to every other root.  A signed rational solution of (24)
then exists.  Here is an explicit degree-one construction.  Group the axis
vertices by colour.  If there are `k>=2` non-axis vertices, give every edge
from a singleton axis group to a non-axis vertex weight `1/k`; in an axis
group of order `s>=2`, give internal edges weight `1/(s-1)` and its edges to
non-axis vertices weight zero.  If there are `r` singleton axis groups, give
every edge inside the non-axis clique weight

```text
(1-r/k)/(k-1).                                       (26a)
```

Every vertex then has weighted degree one.  With exactly one non-axis vertex,
put weight one on its edge to each singleton axis vertex.  Four axis vertices
use at most three colours, so choose a group of order `s>=2`.  If there are
`r` singleton groups, give the edges from the non-axis vertex to this chosen
group weight `(1-r)/s`, and choose its internal edge weight so each group
vertex has degree one.  Give every other nonsingleton axis clique internal
weight `1/(s'-1)` and cross weight zero.  The central degree is also one.
All weights are rational; negative weights are allowed.

If all covectors are axes, `G_rho` is the disjoint union of the same-axis
cliques.  A nonzero common-degree weighting exists exactly when no axis class
is a singleton: on a clique of order `s>=2`, assign every edge weight
`d/(s-1)`.  The five-root all-axis multiplicities covered by Theorem 6 are
therefore `5` and `3+2`; the uncovered partitions are

```text
4+1, 3+1+1, 2+2+1.                                  (26b)
```

The countermodel in Theorem 5 occupies the last pattern.  Thus rank
co-occurrence is automatic off a precise exceptional axis boundary, but not
on that boundary.

## 5. All six top windows have dominant visible image

We now grant much more than current P7 theory proves and show that top data
still carry no polynomial obstruction.

Let

```text
B={1,...,7},             B_c={3,4,5,6,7},
t=7.                                                   (27)
```

Index the roots by `3,...,7` and take the pure root--blocker matrix `H=I_5`.
Make the root rows zero on blockers `1,2`.  The five-root cofactors are then

```text
F_12=1,
F_uv=0 for {u,v}!={1,2}.                              (28)
```

For every `3<=i<j<=6`, put

```text
W_ij={1,2,i,j},
D_ij=B\W_ij.                                           (29)
```

The shore `D_ij` contains the marked column `7`; its identity minor and the
complementary two-by-two identity minor both equal one.  Hence all six
windows are simultaneously clean with unit shore factor.

Take two residual vertices with

```text
h=1,
K_12=gamma !=0,
K_uv=0 otherwise.                                     (30)
```

This is realized by `R_(q0,1)=1`, `R_(q1,2)=gamma` and all other residual
incidences zero.  Set `B_12=0`.  Given arbitrary desired top values

```text
m_ij, nu_ij,             3<=i<j<=6,                  (31)
```

put

```text
B_ij=(nu_ij-m_ij)/gamma.                              (32)
```

Choose cross edges `B_(1i)=u_i`, `B_(2i)=v_i` satisfying

```text
u_i v_j+u_j v_i=m_ij.                                 (33)
```

On the dense open set `m_34 m_35 m_36 !=0`, solve (33) by taking

```text
u_3=1, v_3=0,
v_j=m_(3j), j=4,5,6,                                  (34)
```

and solving

```text
[v_5 v_4   0] [u_4]   [m_45]
[v_6   0 v_4] [u_5] = [m_46].                         (35)
[  0 v_6 v_5] [u_6]   [m_56]
```

Its determinant is `-2m_34m_35m_36`, nonzero in characteristic zero.

### Theorem 7 (six-window top-projection dominance)

For every window in (29),

```text
m_(W_ij)=m_ij,
z_(W_ij)=nu_ij,                                       (36)
```

while the visible pure two-port aggregate is

```text
sum_(u<v) F_uv z_uv=z_12=gamma.                       (37)
```

Consequently the observed map contains the dense open set

```text
gamma m_34 m_35 m_36 !=0                              (38)
```

in the thirteen-dimensional affine space with coordinates
`gamma,(m_ij),(nu_ij)`.  Its elimination ideal in those visible coordinates
is zero.  After imposing the target normalization `gamma=1`, the twelve top
window coordinates remain Zariski dense.

Proof.  The four-port direct hafnian is

```text
m_(W_ij)=B_(1i)B_(2j)+B_(1j)B_(2i)=m_ij              (39)
```

by (33).  In the two-residual relative response, the only corrected pair is
`12`, so

```text
z_(W_ij)=h m_(W_ij)+K_12 B_ij
         =m_ij+gamma(nu_ij-m_ij)/gamma=nu_ij.          (40)
```

Equations (28) and the pair equation `z_12=hB_12+K_12=gamma` prove (37).
Equations (32)--(35) give a rational inverse over (38), proving dominance and
the zero elimination ideal.

All six rank-two top selectors can coexist without changing this fixed pure
matrix.  At roots `3,...,6`, choose independent tangent forms `X_i,Y_i`.
Give every root pair `ij` a tangent-only root edge `X_iX_j`, and take its two
root--residual forms proportional to `Y_i` so that their two assignments sum
to `Y_iY_j`.  The two companion forms are independent, while all added forms
vanish at the fixed root vectors.  Thus even granting simultaneous top-face
selection does not change the dominance conclusion.

Theorem 7 rules out any projected identity that uses only the pure aggregate
and the top `M/Z` faces of these overlapping windows.  It does not rule out an
identity involving their pair faces, mixed-colour coefficients, or the fact
that all three colour charts must arise from the same complete edge-block
system.

## 6. Revised symbolic frontier

The response route now has three exact gates.

1. **Rank co-occurrence.**  Theorem 6 supplies it away from the exceptional
   all-axis partitions (26b); Theorem 5 disproves it on current data at
   `2+2+1`.
2. **Pair-face recovery.**  The exact missing rank is two per `M` or `Z` pair
   block, measured by (6)--(8).  A future lower jet must have a nonzero defect
   signature.
3. **Mixed-colour gluing.**  Top scalar windows have dominant image by
   Theorem 7.  Any obstruction must use information shared across colours or
   across deletion depth.

This shifts priority to:

- exclude the all-axis singleton patterns by their actual mixed coefficients;
- construct two legal lower-jet rows with independent defect signatures;
- build the algebraic matroid of pair faces across the three colour charts;
- or derive a mixed-colour circuit polynomial involving one hidden pair face.

None requires support-shell enumeration.

## Scope wall

Proved:

- the exact selector-matroid rank test and pair-defect signature;
- a legal two-residual family inside the marked-overlay kernel;
- a simultaneous canonical pure-P7 system with no rank-two marked shore;
- the balanced weighted-Laplace sufficient theorem;
- dominance of the aggregate plus every top face from all six clean windows.

Not proved:

- partition closure of any actual P7 window;
- impossibility of the exceptional all-axis patterns under mixed-colour
  equations;
- a common three-colour lower-face circuit;
- a full coloured `P_7 -> Delta_3` realization or exclusion;
- the Krenn--Gu conjecture.

All five items remain **UNKNOWN/UNRESOLVED**.

## Replay

```powershell
uv run --with sympy python verify_p7_selector_matroid_rank_cooccurrence_and_top_projection_boundary.py
python audit_p7_selector_matroid_rank_cooccurrence_and_top_projection_boundary.py
uv run --with sympy --with ruff python -m ruff check verify_p7_selector_matroid_rank_cooccurrence_and_top_projection_boundary.py audit_p7_selector_matroid_rank_cooccurrence_and_top_projection_boundary.py
python -m py_compile verify_p7_selector_matroid_rank_cooccurrence_and_top_projection_boundary.py audit_p7_selector_matroid_rank_cooccurrence_and_top_projection_boundary.py
```

The primary verifier checks the observation ranks and kernels, all three
canonical pure matrices and their physical blocker spans, the weighted marked
Laplace identity, the pure cofactor isolation, and the rational inverse for
the six-window dominance family.  The independent no-import audit uses
Fraction row reduction, a separate subset permanent recurrence, direct minor
products, and exact rational target samples.  These bounded replays audit the
formulas; the observation-space, marked-matching, balanced-weight, and
rational-dominance proofs establish the characteristic-zero results.
