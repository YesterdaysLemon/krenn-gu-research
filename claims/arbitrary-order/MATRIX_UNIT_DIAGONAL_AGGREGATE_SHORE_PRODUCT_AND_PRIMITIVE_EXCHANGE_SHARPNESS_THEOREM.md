# Matrix-unit diagonal aggregate shore-product and primitive-exchange sharpness theorem

## Status

This is an exact arbitrary-order characteristic-zero refinement of the live
`U7J -> U7` obligation in the complete nonzero `r=1` matrix-unit branch.  It
covers the aggregate active-cycle case left outside `U7K`: every matching
other than the selected incoming diagonal term and selected outgoing
offdiagonal term is itself diagonal.

There is a complete structural reduction.

1. The diagonal fibre at a word `chi` is the Cartesian product of the three
   pure-shore matching sets.  After division by the selected incoming
   diagonal monomial, its Laurent polynomial is the product of three
   normalized shore polynomials.
2. The corresponding diagonal difference lattice is the direct sum of the
   three shore matching-difference lattices.  This is an exact disjoint-edge
   support statement, not an inference from shared physical variables.
3. If the diagonal fibre is aggregate, then one shore contains a second
   perfect matching.  Flipping one component of its symmetric difference
   with the selected shore matching produces another diagonal fibre term
   whose difference is one primitive alternating even-cycle vector.
4. On a diagonal-only aggregate active cycle, the complete equations have
   the exact shore-product normal form

```text
lambda(F_i)/lambda(G_(i-1))
  + product_c S_(i,c)=0,

H=(-1)^m product_(i,c) S_(i,c)^(-1)                (1)
```

   at the hypothetical witness.  Every shore factor is nonzero there.

This necessary primitive exchange is a support-lattice direction, not a
zero binomial relation.  A diagonal extra has no offdiagonal core, produces
no bridge word, and does not by itself enter either the bridge/deeper
alternative or the cancelling pure-cofactor machinery.  Shortest-cycle
minimality adds no arc and hence no further conclusion.  Useful coupling
still requires an actual non-direct intersection with another target-fibre
lattice.

The boundary is exact.  A complete locally concise twelve-vertex family over
`Q(t)` has:

```text
only active words:                                  one three-cycle;
complete active-cycle fibre sizes:                  3,2,2;
all extra cycle matchings:                          diagonal;
diagonal extra difference:                         one primitive 6-cycle;
all three pure target coefficients:                 exactly 1;
sum of the three cycle-fibre lattices:               direct and saturated;
physical variables shared across those lattices:    YES;
integer dependency among their four generators:     NONE;
selected holonomy:                                  -1/(1+t);
selected cycle plus pure-anchor H-elimination:       zero ideal.
```

A different mixed word is a singleton of weight one, so the complete target
ideal of this fixed support is a unit.  The family is not a witness or an
apparent counterexample.  No support-minimality or moment-balanced-gauge
claim is made for this fixed family.  It proves that diagonal aggregate
structure, shortest-cycle minimality, pure-anchor normalization, and
physical-variable overlap do not alone force an odd dependency, useful
lattice coupling, parallel successor, or pure/deeper entry.  Whether the
complete target block always supplies a unit or other closure remains open.

The complete nonzero `r=1` branch and the global Krenn--Gu conjecture remain
**UNKNOWN/UNRESOLVED**.

## 1. Diagonal fibres as shore products

Work over `C` at a hypothetical complete nonzero `r=1` matrix-unit witness.
Fix an active mixed word `chi` and put

```text
V_c={v:chi(v)=c},                    c=0,1,2.        (2)
```

Every `|V_c|` is even.  Let `Z^c` be the scalar support/weight matrix formed
by the physical edges whose two endpoint labels are `c,c`.  Write

```text
M_c(chi)=set of support perfect matchings of Z^c[V_c],
h_c(V_c)=sum_(M in M_c(chi)) lambda(M).              (3)
```

An edge in a compatible matching is diagonal exactly when its two endpoint
labels agree.  Compatibility with `chi` then places both endpoints in the
same `V_c`.  Conversely, every pure-`c` edge inside `V_c` is compatible with
`chi`.  Therefore the set of all diagonal compatible matchings is exactly

```text
D(chi)=M_0(chi) x M_1(chi) x M_2(chi),              (4)
```

where a triple is identified with the union of its three disjoint matchings.
In particular,

```text
D_chi=sum_(X in D(chi)) lambda(X)
     =product_c h_c(V_c).                            (5)
```

For an active word the imported diagonal-factorization theorem gives
`D_chi=-Q_chi!=0`.  Thus every factor in (5) is nonzero and every
`M_c(chi)` is nonempty.

Let the selected incoming diagonal matching be

```text
G=P_0 union P_1 union P_2,       P_c in M_c(chi).    (6)
```

Define the normalized shore polynomial and shore difference lattice by

```text
S_c=sum_(M in M_c(chi)) lambda(M)/lambda(P_c),

L_c=span_Z{1_M-1_(P_c):M in M_c(chi)}.              (7)
```

### Theorem 1 (exact shore product and direct sum)

One has

```text
D_chi/lambda(G)=product_c S_c.                      (8)
```

If `L_diag` is generated by all differences between diagonal matchings in
`D(chi)`, then

```text
L_diag=L_0 direct-sum L_1 direct-sum L_2.           (9)
```

### Proof

Weights multiply over the disjoint shore union, so expanding the right side
of (8) gives every triple in (4) exactly once.  This proves (8).

Every vector in `L_c` is supported only on physical edge coordinates with
both endpoints in `V_c`.  Those three edge-coordinate sets are pairwise
disjoint.  Hence the sum in (9) is direct.  Every diagonal matching
difference is a sum of its three shore differences, and every shore
difference extends by the fixed `P_d` for `d!=c`.  Thus the direct sum is
exactly `L_diag`.  QED.

Equation (9) does not classify the intersection of `L_diag` with target
lattices at other words.  Literal reuse of an edge variable by two equations
does not make that intersection nonzero.

## 2. A primitive exchange is unavoidable

Suppose the diagonal fibre contains a matching `X!=G`.  In the Cartesian
decomposition (4), some shore component `M!=P_c`.

### Theorem 2 (single-shore primitive exchange)

There is a diagonal compatible matching `X_C` such that

```text
1_(X_C)-1_G=delta_C,                                 (10)
```

where `delta_C` is supported on one alternating even cycle, has coefficients
`+1` and `-1` alternating around that cycle, and is primitive in the ambient
integer edge lattice.

### Proof

The symmetric difference `M triangle P_c` is a nonempty disjoint union of
alternating even cycles.  Choose one component `C`.  Replace the `P_c` edges
of `C` by the `M` edges of `C` and leave `P_c` unchanged off `C`.  The result
`P_c^C` is another support perfect matching of `V_c`.

Extend it by the fixed `P_d` on the other shores.  The resulting `X_C` is a
diagonal term in the same complete fibre.  Common edges cancel from its
incidence difference with `G`, leaving exactly the alternating signed cycle
vector `delta_C`.  Its nonzero coordinates are all `+1` or `-1`, so their
greatest common divisor is one.  It is primitive.  QED.

The conclusion is deliberately not called a primitive **relation**.  The
complete target equation contains the sum of all diagonal terms together
with the offdiagonal response.  Neither `lambda(X_C)-lambda(G)` nor its
normalized binomial is known to vanish.

## 3. Exact normal form on a diagonal-only aggregate cycle

Let

```text
chi_0 -> chi_1 -> ... -> chi_(m-1) -> chi_0         (11)
```

be an imported active transport cycle.  At `chi_i` let `F_i` be the selected
outgoing offdiagonal matching and `G_(i-1)` the selected incoming diagonal
matching.  Assume the cycle has **diagonal-only aggregate excess**:

```text
every compatible matching at chi_i other than
F_i and G_(i-1) is diagonal.                         (12)
```

Thus the whole offdiagonal coefficient at `chi_i` is the singleton
`lambda(F_i)`, while the whole diagonal coefficient is the shore product
`D_i`.

Choose the shore pieces

```text
G_(i-1)=union_c P_(i,c)                              (13)
```

and define `S_(i,c)` as in (7).

### Theorem 3 (diagonal aggregate cycle normal form)

The complete target equation at `chi_i` is exactly

```text
lambda(F_i)/lambda(G_(i-1))
  + product_c S_(i,c)=0.                            (14)
```

At the hypothetical witness every `S_(i,c)` is nonzero, and the selected
holonomy satisfies

```text
H=(-1)^m product_(i,c) S_(i,c)^(-1).                (15)
```

### Proof

By (12), the complete coefficient is `lambda(F_i)+D_i`.  It vanishes because
`chi_i` is a mixed target word.  Divide by the nonzero selected incoming
monomial and apply (8), obtaining (14).

Both `lambda(F_i)` and `lambda(G_(i-1))` are nonzero.  Equation (14) therefore
shows that the product of the shore factors is nonzero.  Equivalently, (5)
and active synchronization already show that each shore hafnian is nonzero.
Thus every `S_(i,c)` is nonzero at the witness.

Rearrange (14):

```text
lambda(G_(i-1))/lambda(F_i)
  =-product_c S_(i,c)^(-1).                         (16)
```

Multiply over `i` and cyclically reindex the incoming `G` terms.  The left
side is the imported holonomy `H`, proving (15).  QED.

No shore polynomial is asserted to be a unit in its group algebra.  The
inverse in (15) is only the inverse of its nonzero scalar value at the
hypothetical witness.

### Why shortest-cycle minimality is inert here

The shortest-cycle argument in `U7K` constrains a new **bridge arc** produced
by a nonempty offdiagonal core.  A diagonal extra has empty offdiagonal core,
changes no word, and supplies no bridge square or hexagon.  It therefore
adds no directed transport arc to which shortestness can be applied.

The full shore hafnians in (5) are nonzero, so the diagonal extra also does
not trigger the least cancelling-shore hypotheses of the pure-cofactor
theorems.  A smaller cancelling residual or a conformal completion into a
pure target may exist in a particular support, but neither is forced by
(2)--(15).

The remaining exact obligation is lattice-theoretic: prove that some shore
difference lattice in (9) meets another selected target lattice
non-directly in a way that kills every residual sheet, or obtain a unit or a
separate pure/deeper exit.  Shared physical variables are not enough.

## 4. Complete twelve-vertex sharpness family

Use vertices `0,...,11` and a parameter `t` with

```text
t!=0,                 1+t!=0,
x=-(1+t).                                             (17)
```

For a physical pair `uv`, notation `uv:ab:w` records the endpoint labels
`a,b` in increasing vertex order and scalar weight `w`.

On vertices `0,...,7` take:

```text
01:00:1   02:00:1   03:00:1   04:00:1
05:12:1   06:11:1   07:22:1
12:01:-1  13:00:1   14:10:-1  15:11:1  16:22:1  17:00:1
23:11:1   24:01:x   25:22:1   26:00:1  27:20:1
34:22:1   35:01:1   36:10:1   37:11:1
45:00:1   46:11:1   47:11:1
56:01:1   57:11:1   67:11:1.                         (18)
```

The six new-new pairs are:

```text
89:00:1       8,10:00:1     8,11:11:1
9,10:11:1    9,11:00:1     10,11:11:1.              (19)
```

For old-new pairs use the default rules

```text
u in {0,...,7}, j in {8,9}:      uj:01:1;
u in {0,...,7}, j in {10,11}:    uj:10:1,            (20)
```

with the following overrides:

```text
08:22:1   19:22:1   28:00:t   39:00:1
6,10:22:1  7,11:22:1   1,11:10:2.                   (21)
```

Equations (18)--(21) assign one nonzero matrix unit to all `66` physical
pairs.  The weight two on `1,11` removes one irrelevant accidental active
fibre; it occurs in none of the displayed cycle, pure, or excluding
singleton terms.

Take the three words

```text
chi_0=000011110011,
chi_1=001100110011,
chi_2=010101010011.                                  (22)
```

### Theorem 4 (shortest `3/2/2` diagonal aggregate family)

The complete fibres of (22) are exactly:

```text
chi_0:
  01|24|35|67|89|10,11     weight x       outgoing F_0;
  01|28|39|46|57|10,11     weight t       diagonal extra X;
  02|13|46|57|89|10,11     weight 1       incoming G_2;

chi_1:
  01|23|45|67|89|10,11     weight 1       incoming G_0;
  04|12|37|56|89|10,11     weight -1      outgoing F_1;

chi_2:
  02|14|36|57|89|10,11     weight -1      outgoing F_2;
  04|15|26|37|89|10,11     weight 1       incoming G_1. (23)
```

All three sums vanish.  The sole extra cycle term is `X`, and it is
diagonal.  Over `Q(t)` these are the only mixed words whose total coefficient
vanishes while their offdiagonal coefficient is nonzero.

The selected bridge data are the old four-vertex squares with the common
new residual edges:

```text
E_0=24|35,  B_0=23|45,  P_0=01|67|89|10,11;
E_1=12|56,  B_1=15|26,  P_1=04|37|89|10,11;
E_2=14|36,  B_2=46|13,  P_2=02|57|89|10,11.         (24)
```

Thus the three active words form the unique active transport cycle and in
particular a shortest one.

The pure fibres are the singletons

```text
0^12: 03|17|26|45|8,10|9,11     weight 1;
1^12: 06|15|23|47|8,11|9,10     weight 1;
2^12: 08|19|25|34|6,10|7,11     weight 1.           (25)
```

Every vertex sees all three endpoint labels.  Hence the table is complete,
locally concise, and satisfies all three pure target equations exactly.

### Proof

There are `11!!=10395` perfect matchings on twelve labelled vertices.
Exact matching-first enumeration gives (23), (25), and the stated active-word
census.  The first cycle sum is `x+t+1=0` and the other two are `1-1=0`.
Every pure singleton has weight one.

The labels in (24) verify each bridge square directly.  Since each active
word has one offdiagonal term and there are no other active words, the
directed transport graph on active words is exactly the displayed
three-cycle.  Inspection of (18)--(21) gives every local label set
`{0,1,2}`.  QED.

## 5. Primitive shore exchange and exact lattice separation

At `chi_0`, the selected incoming and extra diagonal matchings agree on the
one-shore matching `46|57|10,11`.  On the zero shore they are

```text
P=02|13|89,
M=01|28|39.                                         (26)
```

Their union is the alternating six-cycle

```text
0-2-8-9-3-1-0.                                      (27)
```

Thus

```text
d=1_X-1_(G_2)                                       (28)
```

is precisely the primitive vector promised by Theorem 2.  The zero-shore
hafnian is `1+t=-x!=0`; it is not a cancelling pure residual.

Put

```text
u_0=1_(F_0)-1_(G_2),
u_1=1_(F_1)-1_(G_0),
u_2=1_(F_2)-1_(G_1).                                (29)
```

On the edge columns `01,02,12,24`, the four rows `u_0,u_1,u_2,d` have matrix

```text
[ 1 -1  0  1]
[-1  0  1  0]
[ 0  1  0  0]
[ 1 -1  0  0],                                      (30)
```

whose determinant is one.  Therefore the four vectors are integer
independent and generate a saturated rank-four sublattice.  In particular,

```text
<u_0,d> direct-sum <u_1> direct-sum <u_2>            (31)
```

is the exact sum of the three selected cycle-fibre difference lattices.
There is no integer dependency, odd or otherwise, among these generators.

Nevertheless `d` and the selected cycle directions literally share the
physical edge variables

```text
01, 02, 13.                                         (32)
```

Equations (30)--(32) are the promised sharp distinction: physical-variable
overlap occurs, while genuine support-difference lattice coupling does not.
The pure fibres (25) are singletons and add no within-fibre difference
directions.

## 6. Zero selected holonomy elimination and the outside unit

In the group algebra of (31), write

```text
a=Z^(u_0),  b=Z^(u_1),  c=Z^(u_2),  q=Z^d.          (33)
```

The normalized selected mixed equations are

```text
1+a+q=0,
1+b=0,
1+c=0.                                              (34)
```

The family maps this quotient to `Q(t)` by

```text
q |-> t,
a |-> -(1+t),
b |-> -1,
c |-> -1,
H=(abc)^(-1) |-> -1/(1+t).                          (35)
```

The three pure equations (25) hold identically along the same map.  Since the
image of `H` is a nonconstant rational function of the transcendental
parameter `t`, the induced map from `Q[H,H^(-1)]` is injective.  Hence the
selected cycle equations together with the pure anchors have zero
elimination ideal in `H`.  They form a proper ideal and do not contain a
unit.

The complete target block does exclude this fixed support.  The mixed word

```text
eta=000001000011                                     (36)
```

has the unique compatible matching

```text
04|17|26|35|89|10,11                                (37)
```

of weight one.  Its target-zero equation is one Laurent monomial and
therefore a unit.  The family is not a Krenn--Gu witness.

## 7. Consequence for the live `U7` edge

The purely diagonal aggregate branch now has the exact decision boundary

```text
diagonal-only aggregate cycle
    -> Cartesian shore product;
    -> direct sum of shore difference lattices;
    -> at least one primitive one-shore alternating-cycle direction;
    -> no bridge arc from the extra;
    -> no full-shore cancellation;
    -> closure requires an additional target-lattice intersection,
       a unit/odd dependency, or a separately proved pure/deeper exit.      (38)
```

The twelve-vertex family proves that none of the last-line outcomes follows
from the preceding local data, even when the cycle is the unique shortest
active cycle and all pure coefficients are one.  The family itself is
excluded by an outside singleton, but no arbitrary-order theorem forces such
a singleton.

Together, `U7K` and the present theorem account structurally for every extra
matching in an aggregate active-cycle fibre:

```text
nonempty offdiagonal core:  U7K attachment/bridge decision;
empty offdiagonal core:     shore-product/primitive-exchange decision.      (39)
```

This is a proof-DAG refinement, not an exclusion of `U7`.

## 8. Assumptions and exact boundary

```text
field for the arbitrary-order theorem:                C;
physical branch:                                      complete nonzero r=1 matrix units;
cycle input:                                          imported active transport cycle;
diagonal-only hypothesis:                             every extra cycle matching has empty offdiagonal core;
diagonal Cartesian factorization:                     PROVED;
shore difference-lattice direct sum:                  PROVED;
primitive one-shore alternating exchange:             PROVED;
diagonal aggregate cycle normal form:                 PROVED;
shortest-cycle bridge consequence for diagonal extras: NONE (no arc);
full-shore pure-cofactor cancellation:                ABSENT (shore factors nonzero);
twelve-vertex family:                                 EXACT over Q(t), t(1+t)!=0;
family complete and locally concise:                  YES;
family's active transport graph:                      unique directed 3-cycle;
family's only extra cycle matching:                   DIAGONAL;
family's three pure coefficients:                     EXACTLY 1;
selected fibre-lattice sum:                           DIRECT, SATURATED RANK 4;
physical-variable overlap across directions:          YES;
integer/odd dependency among selected directions:     NONE;
selected-plus-pure holonomy elimination:              ZERO IDEAL;
complete target ideal of family:                      UNIT by singleton eta;
family a Krenn--Gu witness:                           NO;
family support-minimal / moment-balanced:             NOT CLAIMED;
universal outside unit forcing:                       UNKNOWN;
useful non-direct overlap forced:                     UNKNOWN;
proper-subshore pure cancellation forced:             UNKNOWN;
deeper-blocker branch excluded:                       UNKNOWN;
general r=1 branch excluded:                          UNKNOWN;
global Krenn--Gu conjecture:                          UNRESOLVED.
```

The primitive exchange is a support statement.  It is not promoted to a
vanishing binomial.  The direct-sum theorem is internal to one diagonal fibre
and does not assert that all other target lattices are disjoint.  The finite
family checks a sharp local boundary and is independently rejected by its
complete target system.

## 9. Evidence and replay

Run:

```powershell
python claims/arbitrary-order/verify_matrix_unit_diagonal_aggregate_shore_product_and_primitive_exchange_sharpness.py
python claims/arbitrary-order/audit_matrix_unit_diagonal_aggregate_shore_product_and_primitive_exchange_sharpness.py
python -m py_compile claims/arbitrary-order/verify_matrix_unit_diagonal_aggregate_shore_product_and_primitive_exchange_sharpness.py claims/arbitrary-order/audit_matrix_unit_diagonal_aggregate_shore_product_and_primitive_exchange_sharpness.py
python -m ruff check claims/arbitrary-order/verify_matrix_unit_diagonal_aggregate_shore_product_and_primitive_exchange_sharpness.py claims/arbitrary-order/audit_matrix_unit_diagonal_aggregate_shore_product_and_primitive_exchange_sharpness.py
```

The primary verifier uses exact SymPy polynomial arithmetic, a complete
matching-first census of all `10395` twelve-vertex perfect matchings, exact
shore hafnians, bridge and active-word checks, an integer lattice minor, and
a small Groebner elimination.

The independent audit imports no repository module and no symbolic algebra
package.  It rebuilds the table separately, uses 66-bit physical edge masks,
custom exact polynomial tuples, a last-vertex compatible-matching recursion,
Fraction Gaussian elimination, and triangular substitution ranks for the
holonomy map.  The arbitrary-order result is the written Cartesian-product,
alternating-cycle, and cycle-normal-form proof.  The finite scripts audit the
mechanisms and exact sharpness family; they do not claim an arbitrary-order
case census.
