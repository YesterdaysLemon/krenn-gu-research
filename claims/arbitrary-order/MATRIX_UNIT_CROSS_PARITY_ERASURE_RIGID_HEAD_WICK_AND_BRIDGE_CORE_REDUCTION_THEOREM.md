# Matrix-unit cross-parity erasure, rigid-head Wick tower, and bridge-core reduction

## Status

This note proves exact arbitrary-order reductions for the ternary `r=1`
matrix-unit branch over `C`.  For every colour, a parity projection separates
matchings by the number of edges carrying that colour at exactly one
endpoint.  If the positive even sector vanishes, all such cross units erase
and the same target is realized by a graph with a two-root torus
configuration.  Otherwise two matching-aligned cross flags force either the
existing deeper blocker component or a genuine monochromatic bridge.

A simultaneous three-colour parity projection strengthens this to explicit
binary bridge squares and ternary bridge hexagons.  A rigid-head matching
partition supplies an all-order Wick tower coupling proper nonrigidity sets
to pure principal hafnians in the other colours.  In the no-deeper branch,
the non-bridge graph on a nonrigidity set is a functional pseudoforest; when
the global minimum has at least three deviations this sharply bounds its
intersection with the existing `K_(2s)`/`K_(s,s)` pure-support components.

These results do not synchronize the word changed by bridge normalization,
exclude the deeper or erased multi-root branches, or prove that every proper
nonrigidity set becomes global.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. Setup

Let `Omega` have even cardinality `n>=6`, and assume

```text
T_W = Delta_(n,3).                                      (1)
```

Assume the maximum cardinality of a zero-coupled torus-root configuration is
one.  The maximal-root theorem then writes every physical pair as one
nonzero matrix unit

```text
B_uv(x_u,x_v)
 = lambda_uv x_u[ell_u(uv)] x_v[ell_v(uv)],
lambda_uv != 0.                                         (2)
```

For a colour `c`, let `X_c` be the physical edges carrying label `c` at
exactly one endpoint.  Orient such an edge

```text
s -> h
```

from its non-`c` endpoint to its `c` endpoint.  Its tail set is exactly

```text
S_c={s: some edge has a non-c label at s and label c remotely},
R_c=Omega-S_c.                                          (3)
```

Thus the vertices in `R_c` are `c`-rigid.  Let `Z^c` be the scalar matrix of
pure `(c,c)` units.  Odd hafnians are zero by convention.

## 2. Cross parity and exact erasure

For a perfect matching `M`, put

```text
nu_c(M)=|M intersect X_c|,
T_j^c=sum_(M:nu_c(M)=j)
        (product_(e in M) lambda_e) e_(chi_M),          (4)
```

where `chi_M` is the endpoint word induced by `M` and `e_(chi_M)` is its
coordinate tensor.

### Theorem 1 (cross-parity projection)

One has

```text
nu_c(M)<=|S_c|,
|chi_M^(-1)(c)| congruent nu_c(M) mod 2.               (5)
```

Consequently, as complete tensors,

```text
O_c:=sum_(j odd) T_j^c=0,
T_0^c+E_c=Delta_(n,3),
E_c:=sum_(j>=2 even) T_j^c.                            (6)
```

### Proof

Distinct `X_c` edges in one matching have distinct tails.  A pure `(c,c)`
edge contributes two `c` vertices, an edge avoiding `c` contributes none,
and an `X_c` edge contributes one.  This proves (5).

Equivalently, apply the same local involution

```text
D_c=diag(1,1,-1)                                       (7)
```

at every vertex, with the minus sign placed in coordinate `c`.  It negates
exactly the units in `X_c`.  Since `n` is even, it fixes all three pure
target tensors.  The two isotypic projections of (1) give (6).

### Corollary 1 (erasure)

If `E_c=0`, set every block in `X_c` to zero.  The resulting graph
`W^(c,0)` satisfies

```text
T_(W^(c,0))=T_0^c=Delta_(n,3)                          (8)
```

and is globally `c`-rigid.  If `S_c` was nonempty, at least one physical
pair is now the zero block; arbitrary fully supported vectors on its two
endpoints form a two-root torus configuration.  Hence the maximal-root
number of `W^(c,0)` is at least two and the witness enters the existing
maximal-root blocker/deck branch.

In particular, `|S_c|=1` always erases, because no matching can use a
positive even number of `X_c` edges.  More generally, if the ordinary
matching number of the support graph `X_c` is at most one, then `E_c=0`
structurally.  Such an intersecting simple edge family is a star or a
triangle.

Erasure changes the realization but not its tensor.  It proves a reduction,
not impossibility of the original realization.

### Support-minimal consequence

If any witness exists, choose one minimizing the finite number of nonzero
physical pair blocks.  If this witness lies in the `r=1` branch and
`X_c` is nonempty, (8) is forbidden by support minimality.  Therefore

```text
E_c != 0,
matching-number(X_c)>=2.                               (9)
```

If every `X_c` is empty, every unit is diagonal and the witness is globally
rigid in all three colours.  Thus support minimality gives an exhaustive
entry into either the fully diagonal branch or the bridge/deeper analysis
below.

## 3. Matching-aligned bridges and minimum sectors

Choose a mixed word `chi` with `[E_c]_chi!=0`, a contributing matching `F`,
and let

```text
j=nu_c(F)>=2,
P={the j non-c tails of the X_c edges in F},
D=chi^(-1)({0,1,2}-{c}).                              (10)
```

For every `p in P`, its matching edge `p h_p` is a noncoordinate
column-`c` primary killer and `h_p` lies outside `P`.  The heads are distinct.
Equation (6) also gives

```text
[T_0^c]_chi=-[E_c]_chi != 0,                          (11)
```

so there is a zero-cross matching `F_0` inducing the same word.

### Theorem 2 (tail clique or deeper component)

For any distinct `p,q in P`, disable the two matching-aligned killers on

```text
H_p={x:x[chi(p)]=0},
H_q={y:y[chi(q)]=0}.                                  (12)
```

The disabled-killer double-star dichotomy gives exactly one of:

1. the root block is the nonzero pure unit `(c,c)`; or
2. the restricted zero locus has a `c`-open irreducible component carrying
   two fixed blockers on a dense constructible stratum.

This includes the case where the root unit is killed identically on
`H_p x H_q`: because the two primary neighbours are independently external,
the entire product is the `c`-open deeper component, not the nonzero bridge
alternative.

Consequently, if no such deeper component occurs, `P` is a pure-`c` clique.
The zero-cross matching `F_0` pairs `D` internally by edges avoiding `c` and
cannot pair two vertices of `P`.  Its mate map therefore injects `P` into
`D-P`, and the `j` distinct `c`-heads of `F` lie outside `D`.  Hence

```text
|D|>=2|P|=2j,
|chi^(-1)(c)|>=j,
n>=3j.                                                (13)
```

On the deeper component, the multi-star theorem applies pointwise.  After
shrinking to a dense constructible blocker stratum, it gives either at least
three blockers or the exact tight two-blocker permanent with its pure-`c`
residual factor.  No uniform blocker pair is asserted on the whole component.

### Theorem 3 (minimum-sector separation)

Let `(chi,c)` be globally minimum among matching-induced nonconstant words,
with `c` occurring in `chi`, and put `k=|D|`.  The four-switch theorem gives
`1<=k<=4`.

Absent the deeper component:

1. `[E_c]_chi=0`.  Indeed, otherwise Theorem 2 supplies the even set `P`.
   Put `Q=F_0(P)`.  Pair `P` arbitrarily inside its forced `c`-clique, pair
   `Q` by any physical matching, and retain `F_0` elsewhere.  The new word
   has deviation set contained in `D-P`; global minimality forces it to be
   pure `c`.  Every unordered pair carries a nonzero matrix unit in the
   `r=1` branch, so every prescribed pairing of the even set `Q` is a
   physical nonzero matching.  Varying that matching forces

   ```text
   D=P disjoint-union Q,
   |D|=2|P|,                                           (14)
   ```

   and forces `Q` to be a `c`-clique.  Since `|P|` is even and at least two,
   `k<=4` leaves `k=4,|P|=2`, but the upstream `k=4` theorem makes `c`
   globally rigid, contradicting the cross edges.

2. For `k=2`, zero-cross and two-cross support cannot coexist.  If both did,
   the zero-cross matching would use the prescribed avoiding-`c` root edge,
   while the two-cross matching would supply two external killers with the
   same local rows; the killed root restriction is the deeper alternative.
   Thus the remaining cell is either a zero pure deletion cofactor in the
   zero-cross sector, or an internally cancelling two-injection sector with
   the two deviations joined by a `(c,c)` bridge.

3. For `k=3`, one-cross and three-cross support cannot coexist for the same
   reason.  In a three-cross cell the deviation triangle is pure `(c,c)` and
   the three-injection sum cancels internally.  In a one-cross cell, let `A`
   be the deviations that occur as the unique cross tail in some compatible
   matching.  Every pair in `A` is a `(c,c)` bridge, so `|A|<=2`: if all
   three occurred, a matching crossing at the third deviation would have to
   pair the other two by the same physical edge while prescribing labels
   avoiding `c`.

The `k=1` cell remains one cross-cofactor row.  The theorem classifies the
surviving sector, but does not prove that its internal cancellation is
impossible.

## 4. Three-colour parity and bridge normalization

Call a matrix unit diagonal when its endpoint labels agree.  Grade a
matching word by its colour-count parity

```text
pi in F_2^3.                                           (15)
```

A diagonal edge contributes zero, and an offdiagonal type `{a,b}` contributes
`e_a+e_b`.  Since `n` is even, only `000,110,101,011` occur.  Split the
`000`-parity tensor as

```text
D_diag + Q_off = Delta_(n,3),                          (16)
```

where `D_diag` sums completely diagonal matchings and `Q_off` sums
`000`-parity matchings using at least one offdiagonal edge.  Every other
parity tensor is zero.

If `Q_off=0`, deleting every offdiagonal block leaves the diagonal witness
`D_diag=Delta`.  If a deleted edge existed, the new witness has maximal-root
number at least two.  Thus a support-minimal `r=1` witness with any
offdiagonal unit has `Q_off!=0`.

### Theorem 4 (bridge square and hexagon)

For a matching in `Q_off`, let `x_01,x_02,x_12` count its three offdiagonal
edge types.  Parity `000` says

```text
x_01 congruent x_02 congruent x_12 mod 2.              (17)
```

If the common parity is even, some type `{a,b}` occurs twice.  Write two
such disjoint edges as

```text
u_1(a)--v_1(b),       u_2(a)--v_2(b).                 (18)
```

Applying the imported disabled-primary-killer dichotomy to the two colours
gives either a deeper component or

```text
v_1v_2=(a,a),         u_1u_2=(b,b).                   (19)
```

This is the binary bridge square.

If the common parity is odd, choose one edge of each type and write

```text
u_0(0)--u_1(1),
v_0(0)--v_2(2),
w_1(1)--w_2(2).                                      (20)
```

Absent deeper, the three colours force

```text
u_1v_2=(0,0),
u_0w_2=(1,1),
v_0w_1=(2,2).                                        (21)
```

These promoted edges are disjoint and form the ternary bridge hexagon.

Repeatedly use (21) once when all three counts are odd, then use (19) on
pairs of every remaining type.  Every `000`-parity offdiagonal matching is
thereby normalized to a diagonal matching on the same vertex set with the
same colour multiplicities.  The exact induced word generally changes.
Coefficient cancellation is wordwise, so this normalization does not yet
compare the original coefficient with the normalized one.  That word-change
is the remaining synchronization gap; (19)--(21) alone do not imply the
simultaneous balanced all-bridge hypotheses.

## 5. The rigid-head dual Wick tower

Fix `c`, assume `S=S_c` is proper and nonempty, put `R=R_c`, and choose
`d!=c`.  For `s in S,r in R`, define

```text
F_sr^(d,c)=W_sr[d,c],                                  (22)
```

with value zero when that unit is absent.

### Theorem 5 (all-order rigid-head partition)

For every nonempty `T subset R`, the forbidden word equal to `c` on `T` and
`d` elsewhere gives

```text
0 = sum_(U subset T, |T-U| even)
      haf(Z^c[T-U])
      sum_(injections phi:U->S)
        (product_(r in U) F_(phi(r),r)^(d,c))
        haf(Z^d[Omega-(T union phi(U))]).              (23)
```

For one head `r` this is

```text
0=sum_(s in S) F_sr^(d,c) haf(Z^d[Omega-{s,r}]).       (24)
```

For two heads `r,t` it is

```text
0 = Z^c_rt haf(Z^d[Omega-{r,t}])
  + sum_({s,u} subset S)
      (F_sr F_ut + F_st F_ur)
      haf(Z^d[Omega-{s,u,r,t}]).                       (25)
```

In addition, for every proper `T subsetneq R`,

```text
haf(Z^c[S union T]) haf(Z^d[R-T])=0.                  (26)
```

### Proof

A `c`-head `r in T` cannot meet a `d`-word vertex in `R-T`: compatibility
would give that rigid vertex a local non-`c` label and a remote `c` label.
It therefore pairs either internally in `T` by a pure-`c` edge or to a
distinct tail in `S` by a flag.  The residue is pure `d`.  Choosing the
internally paired set, the injection of exposed heads into tails, and the
two residual perfect matchings is reversible and preserves every weight.
This proves (23) with multiplicity one; (24)--(25) are its first two levels.

For (26), use the word `c` on `S union T` and `d` on `R-T`.  The same rigid
head argument forbids every edge across this cut, so the coefficient factors
as displayed.

If `|S|=1`, (24) kills every flag/d-cofactor product individually and (25)
kills every pure-`c` head-edge/d-cofactor product.  If `|S|=2`, (24)--(25)
are the exact paired two-root cell.  Any cofactor-active pair of flag terms
supplies the external killers, with a common head permitted; the nonzero
bridge branch forces the two tails to be joined by `(c,c)`, and every other
root unit gives the deeper component.

Vanishing cofactors can make every displayed equation vacuous.  The tower is
a synchronized cofactor-cover normal form, not an exclusion.

## 6. No-deeper flag incidence

For every `p in S_c`, choose one flag `p -> h_p`.  In the absence of the
external-killer deeper component, if `p!=q`, `h_p!=q`, and `h_q!=p`, the two
chosen neighbours are external to the root pair and Theorem 2 forces
`pq=(c,c)`.  Therefore the non-`(c,c)` graph induced by `S_c` is contained
in the undirected graph of the internal arcs `p -> h_p`.  It is a functional
pseudoforest and has at most `|S_c|` edges.  Equivalently, the pure-`c` graph
on `S_c` has at least

```text
binom(|S_c|,2)-|S_c|                                   (27)
```

edges.  If all selected heads lie in `R_c`, then `S_c` is a pure-`c` clique.

Now suppose the globally minimizing pair has `k>=3`.  The upstream
pure-support theorem makes every connected component of the pure-`c` graph
`G_c` either `K_(2s)` or `K_(s,s)`.  If `S_c` meets the components in sizes
`s_i`, and meets the two parts of a bipartite component in `a_i,b_i`, then

```text
sum_(i<j) s_i s_j
 + sum_(bipartite i) [binom(a_i,2)+binom(b_i,2)]
 <= |S_c|.                                             (28)
```

Indeed, every displayed pair is a nonedge of `G_c[S_c]`, hence an edge of
the functional pseudoforest.

### Corollary 2 (full flags force deeper at `k>=3`)

If `S_c=Omega`, the selected cross flags are `n` distinct internal nonedges,
because one cross unit cannot be oriented from both of its endpoints.  They
are contained in the complement, while the preceding pseudoforest argument
contains every complement edge in the selected flags.  Thus the complement
of `G_c` has exactly `n` edges.  More than one component
already contributes at least `2(n-2)>n` cross-component nonedges.  A complete
component contributes none.  A single `K_(m,m)` contributes `m(m-1)`, equal
to `2m=n` only at `m=3`.

The sole numerical exception is therefore `n=6,G_c=K_(3,3)`.  Its complement
is two triangles, and the six chosen flags orient each triangle as a directed
three-cycle.  One flag edge from each triangle, together with the pure-`c`
edge joining the two unused opposite-part vertices, is a perfect matching
with exactly two deviations from `c`, contradicting `k>=3`.  Thus full
`S_c` necessarily enters the deeper component at every even `n>=6`.

For proper `S_c`, the pseudoforest condition gives the following necessary
classification:

- in one clique component the complement is empty and all selected heads
  point outside `S_c`;
- in one bipartite component, its two intersection sizes are at most three,
  so `|S_c|<=6`;
- in two components with intersection sizes `a,b`, either `min(a,b)=1` or
  `(a,b)=(2,2)`, with any internal complement edges still subject to total
  cycle rank at most one;
- in three components, every intersection has size one and the complement is
  `K_3`;
- four or more met components are impossible.

The only unbounded non-clique cell is the two-component star case.  This is a
necessary support normal form, not a realization theorem.

## 7. Sparse sharpness family

Let `m>=3` be odd, with shores

```text
A={a_i:i mod m},       B={b_i:i mod m},
M_j={a_i b_(i+j):i mod m},       j=0,1,2.             (29)
```

Give `M_j` pure diagonal colour `j` and every edge weight `+1`.  Each pairwise
union is one Hamilton cycle because differences one and two are units modulo
odd `m`; its two alternating matchings give exactly `Delta_(2m,2)` on that
colour pair.

Add one offdiagonal chord `a_0a_1` labelled `(1,0)` with any nonzero weight.
Any perfect matching using it would leave `m-2` vertices of `A` and `m`
vertices of `B` in bipartite shift support, so the chord is sterile.  It gives

```text
S_0={a_0},       S_1={a_1},       S_2=empty,          (30)
```

and illustrates singleton erasure.

Nevertheless,

```text
{a_0b_0}
 union {a_i b_(i+1):1<=i<=m-2}
 union {a_(m-1)b_1}                                  (31)
```

is a perfect matching using all three pure matchings.  Its coefficient is
positive and its word is forbidden.  The family therefore passes every
pairwise two-colour restriction while failing the ternary tensor.

It omits every unused physical pair.  It is not an `r=1` realization and not
a Krenn--Gu counterexample.  It proves that complete nonzero support and the
ternary `000` sector are load-bearing.

## Scope and provenance

The matrix-unit classification and the transfer after erasure are imported
from
[`MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md`](MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md).
The label, pure-deck, and rigid-colour conventions are imported from
[`RIGID_COLOUR_COFACTOR_ANNIHILATION_AND_BACKBONE_CANCELLATION_BOUNDARY.md`](RIGID_COLOUR_COFACTOR_ANNIHILATION_AND_BACKBONE_CANCELLATION_BOUNDARY.md).
The `k<=4`, `k=4`, pure-support, port, and owning `S_c/R_c` results are
imported from
[`MATRIX_UNIT_FOUR_SWITCH_MINIMAL_PORT_AND_PARTIAL_BRIDGE_REDUCTION_THEOREM.md`](MATRIX_UNIT_FOUR_SWITCH_MINIMAL_PORT_AND_PARTIAL_BRIDGE_REDUCTION_THEOREM.md).
The external-killer alternatives and their pointwise blocker refinement are
imported with their original scopes from
[`DOUBLE_STAR_ANNIHILATION_LEMMA.md`](DOUBLE_STAR_ANNIHILATION_LEMMA.md) and
[`MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md`](MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md).

The parity projections, erasure, tail-clique/Hall inequalities,
minimum-sector separation, square/hexagon normalization, rigid-head tower,
functional-pseudoforest closure, and sparse sharpness family are new here.

```text
cross-parity and global-parity projections:       PROVED;
singleton/intersecting cross-support erasure:     PROVED;
support-minimal bridge/deeper entry:              PROVED;
tail clique and minimum-sector normal forms:      PROVED;
bridge square/hexagon normalization:              PROVED;
rigid-head Wick tower:                            PROVED;
full flags at minimizing k>=3 enter deeper:       PROVED;
proper flag propagation:                          UNKNOWN;
word synchronization after bridge normalization: UNKNOWN;
erased r>=2 and deeper-blocker branches:          UNKNOWN;
sparse family is a Krenn-Gu witness:              FALSE;
global Krenn-Gu conjecture:                       UNRESOLVED.
```

## Focused checks

Run from repository root:

```text
python claims/arbitrary-order/verify_matrix_unit_cross_parity_rigid_head_wick.py
python claims/arbitrary-order/audit_matrix_unit_cross_parity_rigid_head_wick.py
```

The primary script uses direct perfect-matching recursion to check the parity
and rigid-head partitions, coordinate-killer restrictions, bridge endpoint
ledgers, and representative sparse shifts.  The independent no-import audit
uses bitmask dynamic programming and a separate injection ledger.  These are
bounded convention and falsification checks; the arbitrary-order proofs are
the written involution, matching bijections, switching, and pseudoforest
arguments.
