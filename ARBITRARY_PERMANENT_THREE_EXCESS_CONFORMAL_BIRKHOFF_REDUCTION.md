# Arbitrary permanent three-excess conformal--Birkhoff reduction

## Status

This note gives two exact arbitrary-order translations of a hypothetical
characteristic-zero restriction

```text
P_m -> Delta_3,       support size exactly 3m+3,      m>=3. (1)
```

First, its physical row-support graph is matching-covered.  A published
three-edge theorem then places all three excess cells in a conformal subgraph
which, after bipartiteness is used, is either an even circuit or an even
subdivision of the three-edge theta graph.

Second, every forbidden mixed three-source coefficient induced by a selected
pure backbone lies on one additive permanent equation and the unique cubic
toric circuit of the Birkhoff polytope `B_3`.  The resulting phase variety
identifies the three complementary-minor channels exactly and proves that
even their simultaneous vanishing is locally consistent.

Neither result excludes support `3m+3`.  Together they compress the support
carrier to a cycle/theta conformal core and each localized forbidden mixed
coefficient to a five-variable boundary variety.  They do not confine all
cancellation matchings to that core.  No support or matching enumeration is
used.

## The physical support is matching-covered

Let `G` be the bipartite graph whose mode and source vertices are joined by
the `3m+3` nonzero physical row cells.  It has a perfect matching because
each nonzero pure target coefficient has at least one matching term.

Every edge of `G` lies in a perfect matching.  If an edge did not, its row
cell would occur in no term of the permanent at any input word.  Deleting
that cell would leave the same restriction with only `3m+2` cells,
contradicting the strict support theorem.

The graph is connected.  Otherwise a perfect matching makes every connected
component balanced between modes and sources, and the permanent factors
across any nontrivial union `A` of components:

```text
P_m(phi(x))=F(x_A) G(x_(A^c)).                       (2)
```

The flattening rank of (2) across `A | A^c` is one.  The corresponding
flattening of

```text
Delta_3=sum_(c=0)^2 lambda_c
        (product_(i in A)x_i[c])
        (product_(i notin A)x_i[c])                 (3)
```

has rank three: both sides contain three linearly independent nonzero
monomials and every `lambda_c` is nonzero.  This contradiction proves
connectedness.

Thus `G` is matching-covered: it is connected and every edge belongs to a
perfect matching.

## A conformal cycle/theta core

Let `E` be the three cells outside a mandatory `3m`-cell tricolour cover.
A theorem quoted as Theorem 2 by de Carvalho and Little implies that any
three edges of a matching-covered graph lie in a conformal subgraph formed
by the union of at most two alternating circuits, for some perfect matching
of the graph.  See
[de Carvalho--Little, *Matching Covered Graphs with Three Removable
Classes*](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v21i2p13),
especially its conformal-subgraph application for three prescribed edges.

Applying that theorem with `k=3` gives a perfect matching `M` and a subgraph
`K` such that

```text
E subset E(K),
K is the union of at most two M-alternating circuits,
G-V(K) has a perfect matching.                              (4)
```

The lengths and overlap pattern of the two circuits are not bounded.  The
result is nevertheless a genuine support-carrier compression: every excess
cell lies in one conformal cycle/theta core, while the arbitrary-order
complement is perfectly matchable and can be frozen in one matching term.
The theorem's matching `M` need not be a selected pure matching.

The same paper proves the sharper three-edge classification in Corollary 22:
the prescribed edges lie in a conformal subgraph which is an induced
circuit, an even subdivision of the three-edge multigraph `Theta`, or an
even subdivision of one of nine displayed cubic graphs `F`.

Only the first two cases can occur here.  Every graph in `F` is obtained
from `K_4` by repeated splicing with `K_4`, as described immediately before
that corollary.  The three vertices left from each newly spliced `K_4`
retain their triangle.  Hence every member of `F`, and every even
subdivision of it, contains an odd circuit.  Such a graph cannot be a
subgraph of the bipartite support `G`.

Therefore the three excess cells lie in a conformal subgraph of one of two
topological types:

```text
C:      one induced even circuit;
Theta:  three internally disjoint odd paths between two branch vertices. (4a)
```

The core has exactly two perfect matchings in case `C` and exactly three in
case `Theta`.  For `Theta`, a perfect matching chooses one of the three odd
branch paths to match both branch vertices; the even-sized interiors of the
other two paths then have their unique path matchings.  Thus the
arbitrary-length core has a bounded internal matching choice space of size
two or three.

This is the appropriate matching-covered analogue of an ear reduction.
Factor-critical odd-ear theory is not the right object because `G` is
balanced and bipartite.  Equations (4)--(4a) do not say that all
cancellation terms stay inside `K`; cross edges and coefficient colours
still have to be controlled.

## The normalized three-port phase variety

Now assume the exceptional-source set has size three and fix a perfect
matching `F` in a selected pure backbone.  The port-permutation theorem gives
a `3 x 3` matrix `X` with nonzero diagonal and coefficient `W_F per(X)`.
Divide its six permutation monomials by the diagonal monomial and put

```text
a=(X_12 X_21)/(X_11 X_22),
b=(X_13 X_31)/(X_11 X_33),
c=(X_23 X_32)/(X_22 X_33),                           (5)

u=(X_12 X_23 X_31)/(X_11 X_22 X_33),
v=(X_13 X_21 X_32)/(X_11 X_22 X_33).                (6)
```

Here `a,b,c` are the three transposition gains and `u,v` are the two oriented
three-cycle gains.  Missing port cells set the affected gains to zero.  A
forbidden mixed coefficient is exactly

```text
1+a+b+c+u+v=0.                                      (7)
```

The five gains also satisfy the multiplicative identity

```text
u v=a b c.                                          (8)
```

Indeed, both sides of (8) are the product of all six off-diagonal entries
divided by the square of the diagonal product.

Equation (8) is the normalized form of the unique cubic circuit of the
`3 x 3` Birkhoff polytope.  Its six lattice points are the permutation
matrices, and its toric ideal is the principal ideal

```text
z_123 z_231 z_312-z_132 z_213 z_321.                (9)
```

See Haase and Paffenholz,
[*Groebner Bases for Transportation
Polytopes*](https://arxiv.org/abs/math/0607194), Section 1.3.  The imported
toric equation is multiplicative; (7) is the problem-specific additive
permanent phase equation.

## Complementary minors in phase coordinates

After division by the relevant diagonal products, the three fixed-row
channels are

```text
row 1 fixed:  1+c,
row 2 fixed:  1+b,
row 3 fixed:  1+a.                                  (10)
```

Thus the complementary-minor forcing lemma succeeds exactly when the
corresponding expression in (10) is nonzero.

The fixed-row bypass from the port theorem is the coordinate face

```text
a=b=u=v=0,       c=-1.                              (11)
```

More strongly, all three complementary minors can vanish simultaneously
without contradicting one boundary coefficient.  Setting

```text
a=b=c=-1                                           (12)
```

reduces (7)--(8) to

```text
u+v=2,       u v=-1.                                (13)
```

Over a characteristic-zero field containing `sqrt(2)`, in particular `C` or
an algebraic closure, this has the two solutions

```text
{u,v}={1+sqrt(2),1-sqrt(2)}.                        (14)
```

This point is realized by the full-support port matrix

```text
    [     1       1  1-sqrt(2) ]
X = [    -1       1       1    ].                   (15)
    [ 1+sqrt(2)  -1       1    ]
```

Its permanent and all three complementary `2 x 2` permanents vanish, while
every entry and all five gains are nonzero.  Therefore no argument using
only one normalized three-port coefficient, diagonal nonvanishing, and the
three complementary minors can prove that one minor is nonzero.

For arbitrary fixed `a,b,c`, equations (7)--(8) say that `u,v` are the roots
of

```text
T^2+(1+a+b+c)T+a b c=0.                             (16)
```

Over the algebraic closure, a single coefficient is generically soluble.
The needed contradiction must use physical-cell identifications between
several backbone matrices, the conformal cycle/theta core (4a), or another
global constraint.

## Invented next object: the phase-decorated `B_3` exchange complex

For each pure backbone and each induced mixed matching, attach one copy of
the phase variety (7)--(8).  Identify gain factors whenever their matrix
entries are coefficients of the same physical row cell.  Retain the Boolean
pure-switch transitions from the dependency-digraph theorem, and saturate by
the nonzero pure diagonal monomials.

This proposed glued object is the **phase-decorated `B_3` exchange
complex**.  A complete definition must also attach a choice of conformal
carrier and record how its matching `M` meets each selected pure backbone.
It is intended to remember:

- additive permanent cancellation;
- the multiplicative Birkhoff circuit;
- physical-cell reuse across different backbones;
- the at-most-eight pure-backbone cube;
- the conformal cycle/theta carrier for the three excess cells.

Once that incidence data is formalized, an algebraic contradiction in the
complex would be a valid arbitrary-order obstruction.  A contradiction in
one isolated phase copy cannot exist because of (12)--(15).

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_three_excess_conformal_birkhoff_reduction.py
python audit_arbitrary_permanent_three_excess_conformal_birkhoff_reduction.py
```

The primary verifier checks the six normalized port monomials, equations
(7)--(10), the fixed-row face, the simultaneous-minor-zero solutions, matrix
(15), and the flattening-rank comparison.  The independent no-import audit
checks the same phase relations through exact quadratic arithmetic.  The
published matching-covered theorem and the arbitrary-order support proof are
proved in prose, not replaced by the finite scripts.

## Boundary

```text
support graph at 3m+3:                   MATCHING-COVERED;
three excess cells:                      IN A CONFORMAL CYCLE/THETA CORE;
core internal perfect matchings:         TWO OR THREE;
forbidden mixed three-port coefficient:   1+a+b+c+u+v=0;
B_3 toric circuit:                       uv=abc;
fixed-row channels:                      1+c, 1+b, 1+a;
all three channels zero:                 ALGEBRAICALLY CONSISTENT;
phase-decorated exchange complex:        PROPOSED, INCIDENCE DATA MISSING;
3m+3 restriction existence:              UNRESOLVED;
global Krenn--Gu conjecture:              UNRESOLVED.
```
