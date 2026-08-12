# Matrix-unit all-bridge beta-three sparse-port primitive lattice and binomial comparison-graph theorem

## Status

This document proves an exact characteristic-zero reduction in the
simultaneous balanced all-bridge branch.  It composes the `A5` sparse
quartic port labelling, the conditional `A6` fixed-completion block, the
`A7` binomial-sublattice sign filter, and the `U7E/U7F` exact binomial
quotient.

There are two new conclusions.

1.  The three differences of the four `A6` block matchings form a primitive
    direct summand of the ambient physical edge lattice.  Consequently, if
    the *complete* mixed fibre containing that block has difference rank
    exactly three, its whole difference lattice equals the `A6` lattice.
    Under the `A7` containment hypothesis, every surviving complete fibre
    then has even cardinality.  In particular, odd sizes `7,9,...` are
    excluded; size five was already excluded by `A6`.
2.  Every additional physical binomial comparison whose difference lies in
    the `A6` lattice is exactly a comparison between two of the four sparse
    ports.  Such comparisons form a graph on four vertices.  A balanced sign
    branch survives exactly when every comparison crosses its `2+2` sign
    cut.  This gives an exact closure criterion for aligned `Q/C^2` and the
    three possible balanced `Q/Q` restrictions arising from different
    binomial cores.

The theorem does **not** force a fixed completion, complete-fibre rank three,
integral containment in a binomial core, or any additional comparison
fibre.  It is a reduction and conditional exclusion interface, not a proof
of the global conjecture.  The global Krenn--Gu status remains
**UNRESOLVED**.

## 1. Setup

Work over a field of characteristic zero on the complete nonzero physical
Laurent torus.  Assume the `A5` beta-three least core has a sparse quartic
site `v`.  Its four incident core-port edges are

```text
f_0,f_1,f_2,f_3,                                      (1)
```

and the four core perfect matchings are indexed so that

```text
f_i in M_i,
f_j notin M_i for j!=i.                               (2)
```

Assume the `A6` fixed-completion hypothesis: a common complementary matching
`K` extends the four core matchings into four terms

```text
Mhat_i=K union M_i,       i=0,1,2,3,                  (3)
```

of one complete mixed zero-target fibre `F_chi`.  Let

```text
a_i=1_(Mhat_i) in Z^E,
u_i=a_i-a_0,             i=1,2,3,
L_A6=<u_1,u_2,u_3>_Z.                                 (4)
```

Here `E` is the full physical edge set, not merely the core support.  The
`A6` theorem proves that `u_1,u_2,u_3` are linearly independent and that the
four block terms have zero total amplitude.

Choose `a_0` as reference for the complete fibre and put

```text
L_F=<1_P-a_0 : P in F_chi>_Z subset Z^E.             (5)
```

Because the four block terms belong to `F_chi`,

```text
L_A6 subset L_F.                                      (6)
```

## 2. Sparse-port coordinate retraction

Let

```text
pi:Z^E -> Z^3,
pi(x)=(x_(f_1),x_(f_2),x_(f_3)).                     (7)
```

The coordinate at `f_0` is deliberately omitted.

### Theorem 1 (primitive direct summand)

The restriction of `pi` to `L_A6` is an isomorphism

```text
pi|_(L_A6):L_A6 -> Z^3,
pi(u_i)=e_i.                                          (8)
```

Consequently the map

```text
sigma:Z^3 -> L_A6,
sigma(e_i)=u_i                                        (9)
```

is an integral section, and

```text
r=sigma o pi: Z^E -> L_A6                            (10)
```

is a retraction.  Therefore

```text
Z^E = L_A6 direct_sum ker(r),                         (11)
```

and `L_A6` is primitive (equivalently, saturated) in `Z^E`.

### Proof

The common matching `K` is disjoint from `v`, so it contributes zero to all
four coordinates in (1).  By (2), `a_i` has coordinate one at `f_i` and zero
at every other `f_j`.  Thus `u_i=a_i-a_0` restricts on the four sparse-port
coordinates to

```text
e_(f_i)-e_(f_0).                                      (12)
```

After forgetting `f_0`, equation (8) follows.  Equations (9)--(10) give
`r(u_i)=u_i`, so `r` is the identity on `L_A6` and is idempotent.  Every
`x in Z^E` decomposes as

```text
x=r(x)+(x-r(x)),
```

with the second summand in `ker(r)`.  The intersection is zero because `r`
is the identity on its image.  This proves (11).  A direct summand of a free
abelian group is primitive.  QED.

This is stronger than the rank-three statement in `A6`.  Linear
independence alone does not imply saturation; the physical sparse-port
identity minor is load-bearing.

### Corollary 1.1 (same-rank landing)

If


```text
rank_Z(L_F)=3,                                        (13)
```

then

```text
L_F=L_A6.                                             (14)
```

### Proof

By (6), `L_F/L_A6` is a finite abelian group when the two lattices have the
same rank.  For `x in L_F`, some positive integer `m` therefore satisfies
`mx in L_A6`.  Theorem 1 makes `L_A6` saturated in the common ambient lattice
`Z^E`, so `x in L_A6`.  Hence `L_F subset L_A6`, and (6) gives equality.
QED.

Without Theorem 1, equal rank would not suffice: a finite-index proper
superlattice is otherwise possible.

## 3. Exact-rank-three complete fibres have even size

Now also assume the `A7` integral containment hypothesis.  Thus a
parity-consistent same-multidegree binomial core has lattice `L_bin` and sign
character

```text
rho:L_bin -> {+1,-1},
L_A6 subset L_bin.                                    (15)
```

Assume the complete fibre has rank three as in (13).  Corollary 1.1 gives

```text
1_P-a_0 in L_A6 subset L_bin       for every P in F_chi. (16)
```

Write

```text
epsilon(P)=rho(1_P-a_0) in {+1,-1}.                  (17)
```

The normalized complete mixed target equation maps modulo the binomial core
to the scalar

```text
s_F=sum_(P in F_chi) epsilon(P).                     (18)
```

### Theorem 2 (even-fibre landing)

Under (13) and (15), exactly one of the following holds.

1. `s_F!=0`, in which case the binomial core together with the complete
   target equation generates the unit ideal.
2. `s_F=0`, in which case

   ```text
   |F_chi| is even.                                   (19)
   ```

Hence every odd exact-rank-three complete fibre is excluded.  Combining
this with `A6`, the possible surviving cardinalities are

```text
4,6,8,10,...;                                         (20)
```

in particular, sizes `5,7,9,...` do not survive.

### Proof

The exact `U7E/U7F` quotient sends every normalized term to (17), so the
complete target polynomial has image (18).  A nonzero scalar is a unit in
characteristic zero.  If it vanishes, it is a sum of `|F_chi|` numbers in
`{+1,-1}`.  Such a sum can be zero only when the plus and minus counts agree,
which proves (19).  `A6` separately proves that the fibre has four terms or
at least six, never five.  QED.

### Corollary 2.1 (the six-term complement)

Suppose `|F_chi|=6` and the `A7` branch survives.  The four fixed-completion
block signs already have two plus and two minus.  Therefore the two terms of

```text
R_chi=F_chi-{Mhat_0,Mhat_1,Mhat_2,Mhat_3}            (21)
```

have opposite signs.  Their difference belongs to `L_A6 subset L_bin`, and
their normalized two-term sum belongs to the binomial-core ideal.  This is
an exact opposite-sign complement binomial, not a proof that such a
six-term fibre exists or that it supplies a new independent target equation.

## 4. Landing of physical comparison binomials

Let `P,Q` be distinct physical perfect matchings in one complete binomial
fibre of the same multidegree, and orient its normalized difference as

```text
d=1_P-1_Q.                                            (22)
```

Assume

```text
d in L_A6.                                            (23)
```

Every perfect matching uses exactly one physical edge incident with `v`.
Besides the four edges (1), there may be other incident physical edges; they
must not be silently discarded.

### Theorem 3 (physical port-pair landing)

Under (23), there are distinct `p,q in {0,1,2,3}` such that

```text
d=a_p-a_q.                                            (24)
```

Thus every nonzero physical perfect-matching difference in `L_A6` is exactly
one unordered sparse-port pair direction, up to orientation.

### Proof

Every element of `L_A6` has zero coordinate on each incident edge outside
`{f_0,f_1,f_2,f_3}`.  If exactly one of `P,Q` uses such an outside edge, or
if they use two different outside edges, (22) has a nonzero outside
coordinate, contradicting (23).

If both use the same outside edge, then `pi(d)=0`.  Theorem 1 says that `pi`
is injective on `L_A6`, so `d=0`, contradicting `P!=Q`.  The same argument
applies if both use the same `f_p`.

The only remaining possibility is that `P` and `Q` use distinct sparse-port
edges `f_p,f_q`.  The vectors `d` and `a_p-a_q` lie in `L_A6` and have the
same image under `pi`; injectivity gives (24).  QED.

This theorem classifies a comparison *after* (23) is known.  It does not
force any additional complete fibre to be binomial or to land in `L_A6`.

## 5. The comparison graph

Index the four `A6` terms by the vertices

```text
V_4={0,1,2,3}.                                        (25)
```

For a family of additional complete binomial comparisons satisfying (23),
put an undirected edge `{p,q}` in a simple graph `H` whenever the family
contains the direction `+/- (a_p-a_q)`.

Fix one balanced `A7` restriction and write

```text
epsilon_p=rho(a_p-a_0),
epsilon_0=1.                                          (26)
```

Its two plus vertices and two minus vertices define a balanced cut
`C_epsilon` of `V_4`.

### Theorem 4 (exact opposition-graph criterion)

For an edge `{p,q}` of `H`, its normalized binomial maps modulo the chosen
core to

```text
1+epsilon_p epsilon_q.                               (27)
```

Consequently:

- if `p,q` have the same sign, (27) is `2` and the combined branch ideal is
  the unit ideal globally across all torsion sheets;
- if `p,q` have opposite signs, (27) is `0` and that comparison is already
  absorbed by the binomial-core ideal.

The balanced restriction survives all comparisons in `H` if and only if

```text
every edge of H crosses C_epsilon.                    (28)
```

### Proof

Theorem 3 writes the physical difference as `+/- (a_p-a_q)`.  The sign
character sends its Laurent monomial to `epsilon_p epsilon_q`; inversion
does not change a sign in `{+1,-1}`.  This proves (27).  The scalar `2` is a
unit in characteristic zero.  For opposite signs, the exact binomial-core
quotient has zero image, so the comparison belongs to its kernel.  Applying
this edge by edge proves (28).  QED.

### Corollary 4.1 (`Q/C^2`)

For the unique aligned `Q/C^2` survivor, the complementary doubletons are

```text
D_x={0,1},       D_y={2,3},
epsilon|_(D_x)=+1,
epsilon|_(D_y)=-1.                                   (29)
```

One comparison excludes this survivor if and only if its edge lies within
`D_x` or within `D_y`.  Every cross-doubleton comparison is redundant.

### Corollary 4.2 (`Q/Q` uniform closure)

Across the possible parity-consistent binomial cores, the three possible
balanced `Q/Q` restrictions are exactly the three unordered `2+2` cuts of
`V_4`.  They are alternatives for the one fixed character of a chosen core,
not three torsion sheets simultaneously present for that core.  A
predetermined comparison graph closes all three possible restrictions if
and only if it admits no bipartition with two vertices on each side.

No graph with at most two edges closes all three.  The inclusion-minimal
closure graphs have three edges and are exactly

```text
a triangle plus an isolated vertex,  or  K_(1,3).    (30)
```

The path `P_4` is the sharp three-edge nonclosure: its unique bipartition has
two vertices on each side and survives.

### Proof

Any graph with at most two edges can be placed across some balanced cut, so
one restriction survives.  More intrinsically, a surviving restriction is
precisely a balanced proper two-colouring of `H`.

Let `H` be inclusion-minimal with no such colouring.  If `H` is
nonbipartite, a four-vertex simple graph contains a triangle, and minimality
reduces `H` to that triangle.  If `H` is bipartite, its component colourings
can be flipped independently.  Minimal failure of a balanced colouring must
therefore be connected with bipartition sizes `1+3`; the minimal connected
graph with those shores is `K_(1,3)`.  Conversely, a triangle is not
bipartite and `K_(1,3)` has only a `1+3` bipartition, so both close every
balanced cut.  The only remaining connected three-edge tree on four vertices
is `P_4`, whose shores have size `2+2`.  QED.

Thus three suitably placed comparison carriers are necessary and sufficient
for a predetermined uniform `Q/Q` closure within this interface.  The
theorem does not force those carriers or allow their placement to depend on
an unknown sign branch unless a separate theorem supplies that dependence.

## 6. Sharp Laurent controls

Let

```text
A=C[X^(+/-1),Y^(+/-1),Z^(+/-1)],
p=1+X+Y+Z.                                            (31)
```

Take

```text
J_align=(1+Y,1+Z,1+XY).                              (32)
```

Its torus point has `(X,Y,Z)=(1,-1,-1)`, so `p=0`.  The aligned
`Q/C^2` doubleton sums are

```text
q_x=1+X=2,
q_y=Y+Z=-2.                                          (33)
```

Adding the within-doubleton comparison `1+X` makes the ideal a unit.  The
cross-doubleton comparison `1+X^(-1)Y` instead vanishes modulo `J_align` and
leaves a proper ideal.  This realizes both sides of Corollary 4.1.

For `Q/Q`, one fixed pair edge is same-sign in exactly one of the three
possible balanced cuts and opposite-sign in the other two.  Hence, across
the alternative cores, one predetermined edge kills exactly one possible
restriction and two edges kill at most two.  This is not a simultaneous
three-sheet statement for one core.  A triangle and a star realize the two
minimal closure types in (30), while `P_4` realizes the sharp surviving
boundary.

Noncontainment alone has no universal consequence.  For example,

```text
J_boundary=(1+XY)                                    (34)
```

does not contain `L_A6`; nevertheless `(X,Y,Z)=(1,-1,-1)` is a common torus
zero of `J_boundary` and `p`, with the nonzero doubleton values (33).  Thus
neither a second direction nor a unit follows merely from failure of the
`A7` containment hypothesis.

## 7. Dependencies and owner pins

The owning locations below are pinned to exact repository commit
`9a679a7af6726bbba32df0258ea2fb4e4655d675`.

1. **A5 route-port pairing.**
   [`ALL_BRIDGE_BIPARTITE_LEAST_CORE_BETA_THREE_ROUTE_PORT_PAIRING_THEOREM.md`](ALL_BRIDGE_BIPARTITE_LEAST_CORE_BETA_THREE_ROUTE_PORT_PAIRING_THEOREM.md),
   Git blob `b6b156515626ee2089b16e11c0030337645b2b96`, lines 185--316.
   It owns the four sparse singleton ports and the `Q/C^2` complementary
   nonzero doubletons.
2. **A6 fixed-completion block.**
   [`MATRIX_UNIT_ALL_BRIDGE_BETA_THREE_ROUTE_PORT_FIXED_COMPLETION_MIXED_FIBRE_RANK_THREE_BLOCK_THEOREM.md`](MATRIX_UNIT_ALL_BRIDGE_BETA_THREE_ROUTE_PORT_FIXED_COMPLETION_MIXED_FIBRE_RANK_THREE_BLOCK_THEOREM.md),
   Git blob `a0be6458bf26c36b9436bd83ecbaeec5ee84ccdb`, lines 100--249 and 251--360.
   It owns the conditional common completion, four-term zero block, rank
   three, complete-fibre complement, and formal polynomial `1+X+Y+Z`.
3. **A7 sign filter.**
   [`MATRIX_UNIT_ALL_BRIDGE_BETA_THREE_FIXED_COMPLETION_BINOMIAL_SUBLATTICE_PORT_SIGN_DICHOTOMY_THEOREM.md`](MATRIX_UNIT_ALL_BRIDGE_BETA_THREE_FIXED_COMPLETION_BINOMIAL_SUBLATTICE_PORT_SIGN_DICHOTOMY_THEOREM.md),
   Git blob `acb33938f9f64a5d764cbcfb0c3a396b70d9277e`, lines 103--333.
   It owns integral containment, the fixed sign character, imbalanced units,
   the aligned `Q/C^2` restriction, and the three balanced `Q/Q` restrictions.
4. **U7E complete fibre lattice reduction.**
   [`MATRIX_UNIT_COMPLETE_SAME_MULTIDEGREE_FIBRE_LATTICE_REDUCTION_AND_BINOMIAL_PARITY_DICHOTOMY_THEOREM.md`](MATRIX_UNIT_COMPLETE_SAME_MULTIDEGREE_FIBRE_LATTICE_REDUCTION_AND_BINOMIAL_PARITY_DICHOTOMY_THEOREM.md),
   Git blob `bf3f8a1048d78459f24188bb46fb7953fdc5522c`, lines 102--284.
   It owns normalization, faithful Laurent descent, and the exact binomial
   parity dichotomy.
5. **U7F binomial quotient.**
   [`MATRIX_UNIT_BINOMIAL_CORE_TORSION_SHEET_AND_RANK_ONE_AGGREGATE_QUOTIENT_THEOREM.md`](MATRIX_UNIT_BINOMIAL_CORE_TORSION_SHEET_AND_RANK_ONE_AGGREGATE_QUOTIENT_THEOREM.md),
   Git blob `ed5f3e2b5e71bf7e7e34f6f6b9663641d5eb9560`, lines 85--227 and 330--385.
   It owns the exact group-algebra quotient, torsion sheets, and the rule that
   a nonzero scalar kills every sheet.

No conclusion is imported from or asserted about the `S2O` or `S2P`
common-shore sensor lanes.

## 8. Evidence contract

The focused primary verifier is

```text
claims/arbitrary-order/verify_matrix_unit_all_bridge_beta_three_sparse_port_primitive_lattice_and_binomial_comparison_graph.py
```

It should use exact physical matching incidences and integer arithmetic to
check the sparse-port retraction, same-rank collapse mechanism, even-fibre
sign ledger, physical outside-port cases, all simple comparison graphs on
four vertices, the `Q/C^2` criterion, and the sharp Laurent controls.

The independent audit is

```text
claims/arbitrary-order/audit_matrix_unit_all_bridge_beta_three_sparse_port_primitive_lattice_and_binomial_comparison_graph.py
```

It should import neither repository code nor the primary verifier, use a
different perfect-matching and lattice representation, independently derive
the comparison-cut census, and retain exact arithmetic throughout.

These finite checks are QA for the displayed four-term mechanisms.  The
arbitrary-order claims are carried by the written proofs: coordinate
retraction, saturation, finite-index collapse, exact group-algebra descent,
and the graph-colouring argument.

## 9. Exact boundary

```text
simultaneous balanced all-bridge branch:             ASSUMED;
beta=3 least core with one sparse quartic site:       ASSUMED;
A6 common fixed completion into one mixed fibre:      ASSUMED;
four sparse-port singleton matchings:                 IMPORTED;
L_A6 primitive/direct summand in physical edge lattice: PROVED;
complete-fibre difference rank exactly three:        NOT FORCED / CONDITIONAL;
rank three implies L_F=L_A6:                         PROVED;
A7 integral containment in a binomial core:           NOT FORCED / CONDITIONAL;
odd exact-rank-three contained fibres:                EXCLUDED;
six-term complement signs opposite:                  PROVED CONDITIONALLY;
extra physical binomial difference in L_A6:           NOT FORCED / CONDITIONAL;
such a difference is one sparse-port pair:            PROVED;
aligned Q/C^2 within-doubleton comparison:             UNIT;
aligned Q/C^2 cross-doubleton comparison:              REDUNDANT;
Q/Q comparison-graph closure threshold:               PROVED;
triangle or K1,3 comparison carriers exist:           NOT FORCED;
uncontained rank-at-least-three ideal:                 OPEN;
fixed completion, rank equality, and containment:      OPEN;
S2O/S2P common-shore residuals:                        OUT OF SCOPE;
global Krenn--Gu conjecture:                           UNRESOLVED.
```
