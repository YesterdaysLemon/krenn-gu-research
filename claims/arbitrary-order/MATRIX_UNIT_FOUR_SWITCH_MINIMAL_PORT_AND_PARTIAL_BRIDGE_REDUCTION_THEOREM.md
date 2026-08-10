# Matrix-unit four-switch, minimal-port, and partial-bridge reduction theorem

## Status

This note proves exact arbitrary-order reductions inside the `r=1`
matrix-unit branch of the maximal torus-root theorem, over `C` and at every
even order `n>=6`.

Every hypothetical witness in that branch has a matching-induced
nonconstant word with at most four deviations from an occurring colour.  A
word with the globally minimum number `k` of deviations therefore has
`1<=k<=4`.  Its complete coefficient is one finite `k`-port hafnian response,
and a suitable choice of pure baseline always exposes at least two nonzero
deviation-spanning alternating-cycle groups.  Thus zero cofactors alone
cannot dispose of the minimum word.

The four-switch involution gives two further exact consequences.  If `k=4`,
one colour is rigid at every vertex, so this entire case enters the existing
rigid-colour annihilating-deletion system.  If `k=3`, every edge and its
four-switch partner have endpoint-deviation types `(0,0)`, `(1,2)`, or
`(2,2)`.

For a fixed colour, the vertices carrying off-diagonal column killers obey a
separate partial-bridge dichotomy: either one induced edge exposes a genuine
deeper double-star blocker component, or all induced edges satisfy the exact
coordinate-bridge zero pattern and the two failure-plane classes differ in
size by at most the number of rigid vertices.  Full nonrigidity for all three
colours therefore enters the simultaneous balanced all-bridge branch unless
a deeper component occurs.  Proper nonempty nonrigidity sets remain an exact
open boundary.

The displayed six- and eight-vertex systems are exact countermechanisms to
two tempting propagation shortcuts.  Neither is a Krenn--Gu witness.  No
claim here excludes `k=1,2,3`, the globally rigid arbitrary-order branch, the
partial-bridge boundary, or the `r>=2` maximal-root branch.  The global
conjecture remains **UNRESOLVED**.

## 1. Matrix-unit conventions and minimum deviations

Let `Omega` have even cardinality `n>=6`.  In the `r=1` branch every physical
edge is one nonzero matrix unit, so for `e={u,v}` write

```text
B_e(x_u,x_v)
 = lambda_e x_u[ell_u(e)] x_v[ell_v(e)],
lambda_e!=0.                                         (1)
```

Assume throughout that `T_W=Delta_(n,3)`.  A perfect matching `F` induces
the word `chi_F(v)=ell_v(e_v)`, where `e_v` is the edge of `F` incident with
`v`.  The three pure target coefficients provide pure perfect matchings
`M_0,M_1,M_2` with nonzero edge products.  They are physically edge-disjoint.
The Bogdanov matching theorem, in the form already used by the universal
zero-layer theorem, gives a nonmonochromatic perfect matching in their union.
Hence at least one matching-induced nonconstant word exists.

Among every matching-induced nonconstant word and every colour occurring in
that word, choose `(chi,c)` minimizing

```text
k=|D|,             D={v:chi(v)!=c}.                  (2)
```

Thus `D` is nonempty and proper.

### Theorem 1 (four-deviation bound)

One has

```text
1<=k<=4.                                             (3)
```

### Proof

Choose distinct colours `c,d`, pure matchings `M_c,M_d`, and an edge
`e={u,v}` of `M_d`.  The edge cannot belong to `M_c`.  Let `u',v'` be the
`M_c`-mates of `u,v`.  The four vertices are distinct.  Replace the two
`M_c` edges `uu',vv'` by the physical edges `uv,u'v'`, retaining `M_c` on
all other vertices.  This is a perfect matching.  It gives colour `d` to
`u,v`, arbitrary endpoint colours to `u',v'`, and colour `c` to every other
vertex.  Since `n>=6`, colour `c` still occurs and the word is nonconstant.
It has between two and four deviations from `c`, proving (3).

## 2. The four-switch involution

Fix a pure `c` matching `M`.  Let `pi` be its fixed-point-free mate
involution.  For every edge `e={u,v}` outside `M`, define

```text
tau_M(e)={pi(u),pi(v)}.                               (4)
```

The edges `e,tau_M(e)` are disjoint and, together with `M` off their four
endpoints, form a perfect matching.  Put

```text
delta_c(e)=#{w in e:ell_w(e)!=c} in {0,1,2}.         (5)
```

The four-switch word has exactly

```text
delta_c(e)+delta_c(tau_M(e))                         (6)
```

deviations from `c`.  If (6) is nonzero, it is a matching-induced
nonconstant word in which `c` occurs, and therefore is at least the global
minimum `k`.

### Theorem 2 (the `k=4` rigid absorption and `k=3` pair types)

If `k=4`, then every physical edge is either labelled `(c,c)` or both of its
endpoint labels avoid `c`.  In particular every vertex is globally
`c`-rigid in the sense of the rigid-colour theorem.

If `k=3`, then for every edge outside `M` the unordered pair

```text
{delta_c(e),delta_c(tau_M(e))}
```

is one of

```text
{0,0}, {1,2}, {2,2}.                                 (7)
```

### Proof

For `k=4`, (6) is either zero or at least four, while its maximum is four.
Thus its two summands are both zero or both two.  Every `M` edge is already
`(c,c)`, proving global `c`-rigidity.

For `k=3`, the only allowed sums in `{0,1,2,3,4}` are `0,3,4`, which gives
exactly (7).  In particular a one-`c` endpoint edge is paired with an edge
avoiding `c`, while types `(0,1)`, `(0,2)`, and `(1,1)` cannot occur.

This is a support theorem.  It does not assert that the globally rigid
deletion system is inconsistent at arbitrary order, and (7) is not by itself
a contradiction.

### Theorem 2A (pure-support classification when `k>=3`)

Assume `k>=3`, and let `G_c` be the unweighted graph of all physical
`(c,c)` edges.  For every distinct `u,v`,

```text
uv in E(G_c)
  iff G_c-{u,v} has a perfect matching.               (8)
```

Every connected component of `G_c` is therefore either a complete graph of
even order or a balanced complete bipartite graph.

### Proof

If `G_c-{u,v}` has a perfect matching but `uv` is not `(c,c)`, their union
with the physical edge `uv` induces a nonconstant word with one or two
deviations from `c`, contradicting `k>=3`.

Conversely, suppose `uv` is `(c,c)`.  If one pure `c` matching already
contains it, deletion leaves a perfect matching.  Otherwise apply the
four-switch construction to `uv` and any pure `c` matching `M`.  Since
`delta_c(uv)=0`, minimum three forbids its partner from having deviation one
or two.  Hence `tau_M(uv)` is also `(c,c)`, and the four-switch is a pure
`c` matching containing `uv`.  This proves (8).  In particular every edge
of every connected component is allowed, so each component is
factor-connected.

The classical Kotzig--Lovasz canonical-partition theorem says that in a
factor-connected graph the relation

```text
u~v  iff  u=v or deletion of {u,v} leaves no perfect matching
```

is an equivalence relation.  A short modern proof is included in
[Kita, *A Partially Ordered Structure and a Generalization of the Canonical
Partition for General Graphs with Perfect Matchings*](https://arxiv.org/abs/1205.3816).
By (8), its distinct equivalent vertices are exactly the nonadjacent pairs.
Thus every component of `G_c` is complete multipartite.

Let its part sizes sum to `2s`.  It has a perfect matching, so no part is
larger than `s`.  If every part is a singleton, the component is `K_(2s)`.
Otherwise choose two vertices in a part of size at least two.  Their deletion
must destroy all perfect matchings by (8).  In a complete multipartite graph
on `2s-2` vertices this means that one remaining part has size greater than
`s-1`.  The depleted part has size at most `s-2`, so a different part has
size exactly `s`.  Delete two vertices from that size-`s` part and repeat the
argument: another part must also have size `s`.  These two parts exhaust the
component, which is `K_(s,s)`.

### Theorem 2B (a cofactor-active four-vertex normal form for `k=3`)

Assume `k=3`.  Every minimizing matching contains an edge `e={u,v}` with
`delta_c(e)=1`.  There are distinct `a,b` outside `{u,v}` such that, putting
`Q={u,v,a,b}`,

```text
Z^c_ua Z^c_vb
haf(Z^c[Omega-{u,v,a,b}]) !=0,                       (9)
```

the four-switch partner `ab` has `delta_c(ab)=2`, and

```text
e | ab | (a pure c matching off {u,v,a,b})           (10)
```

induces a minimum three-deviation word `chi_e`; put
`D_e={x:chi_e(x)!=c}`.  This word has a nonzero local four-cycle group, and
its exact cycle grouping is

```text
0 = H_Q (lambda_uv lambda_ab
         + epsilon lambda_ub lambda_va)
    + sum_(active C with Q proper subset V(C))
        w(C) haf(Z^c[Omega-V(C)]),                    (10a)
```

where `H_Q=haf(Z^c[Omega-Q])`, and `epsilon` is one exactly when the third
pairing `ub|va` preserves `chi_e` on `Q`.  Consequently either a strictly
larger deviation-spanning cycle has a nonzero group, or the third pairing
exists and obeys the exact local cancellation

```text
lambda_uv lambda_ab + lambda_ub lambda_va=0.          (10b)
```

### Proof

Three is odd, so some edge of a minimizing matching contributes exactly one
deviation.  It is not a pure edge.  By (8), `G_c-{u,v}` has no perfect
matching.  Expand `haf(Z^c[Omega])=1` by the distinct partners of `u,v`:

```text
1=sum_(ordered distinct a,b in Omega-{u,v})
    Z^c_ua Z^c_vb
    haf(Z^c[Omega-{u,v,a,b}]).                        (11)
```

Some summand gives (9).  Choose a pure matching represented by a nonzero
monomial in that summand.  Its mate image of `e` is `ab`, and Theorem 2 gives
`delta_c(ab)=2`.  Equation (9) says that the resulting four-cycle group is
genuinely nonzero.  Relative to this baseline, the only other active cycle
on exactly `Q` is the third pairing.  Moreover `D_e` consists of the one
deviation endpoint of `uv` and both endpoints of `ab`; closure under the
baseline mate edges `ua,vb` adds the remaining endpoint of `uv`.  Hence
every baseline-alternating cycle containing all of `D_e` contains `Q`, and all
other groups use a strictly larger cycle.  The minimal-cycle grouping
therefore gives (10a).  If its final sum has no nonzero term, `epsilon=1` and
(10b) follows.

## 3. Adaptive baseline exposure

The earlier minimal-cycle theorem fixed an arbitrary pure baseline and left
two formal possibilities: every eligible cycle group could have a zero pure
cofactor, or at least two nonzero groups could cancel.  At a minimum word the
first possibility can always be removed by adapting the baseline.

### Theorem 3 (nonzero baseline exposure)

For the minimizing pair `(chi,c)`, there is a pure `c` matching `P` such that
the forbidden coefficient of `chi`, grouped relative to `P`, contains at
least two nonzero `D`-spanning alternating-cycle groups.

### Proof

Fix one matching `F` inducing `chi`.  Let `P` range over all pure `c`
perfect matchings.  By minimality, `F triangle P` has exactly one component
meeting `D`, and that component contains all of `D`: switching a component
meeting a proper nonempty subset of `D` would produce a matching-induced
nonconstant word with fewer deviations.

Group the pure coefficient

```text
haf(Z^c[Omega])=1                                    (12)
```

by this unique `D`-meeting component.  For a fixed component `C`, the group
is the nonzero product of the `P`-parity weights on `C`, summed against the
complete pure `c` hafnian on `Omega-V(C)`.  Since all groups sum to one, one
group is nonzero.  Choose a pure matching `P` occurring in that group.  The
same `C`, now viewed as a `P`-alternating active cycle for `chi`, has nonzero
cycle weight and nonzero complementary hafnian.  Its cycle group in the
forbidden coefficient is therefore nonzero.  That coefficient is zero, so
at least one additional nonzero group must cancel it.

No positivity, genericity, or division by a hafnian is used.

## 4. The complete minimum-port response

Put `R=Omega-D`.  For `i,j in D` and `r in R`, define

```text
Y_ij = W_ij[chi(i),chi(j)],
X_ir = W_ir[chi(i),c],
H_J  = haf(Z^c[R-J]),              J subset R,       (13)
```

with odd hafnians zero and `H_empty=haf(Z^c[R])`.

### Theorem 4 (exact `k`-port formula)

The forbidden coefficient is exactly

```text
0 = sum_(S subset D, |S| congruent |D| mod 2)
      haf(Y[D-S])
      sum_(injections f:S->R)
        (product_(i in S) X_(i,f(i))) H_(f(S)).       (14)
```

### Proof

Given a compatible perfect matching, let `S` be the deviation vertices sent
to the pure-`c` core `R`.  These vertices have distinct partners, giving the
injection `f`.  The remaining vertices `D-S` match internally through `Y`,
and the unused core vertices match through `Z^c`.  Conversely these three
pieces reconstruct one compatible perfect matching.  The correspondence is
bijective, preserves weights, and has no orientation multiplicity.  This
proves (14).

For `k=1`, (14) is the near-monochromatic cofactor row.  For `k=2`, writing
`D={p,q}` and

```text
h=haf(Z^c[R]),
H_rs=haf(Z^c[R-{r,s}]),
A_p[a,r]=W_pr[a,c],
A_q[b,r]=W_qr[b,c],                                  (15)
```

all nine boundary coefficients assemble into the exact matrix identity

```text
h W_pq + A_p H A_q^T = E_cc.                         (16)
```

For `k=3`, the live layers have one or three core crossings.  For `k=4`,
they have zero, two, or four core crossings.  Thus Theorem 1 reduces the
minimum cancellation to a response of at most four ports, but it does not
make the middle cofactor forms in (14) nondegenerate.

## 5. Fixed-colour partial bridges

For a colour `c`, let

```text
S_c={v: there is an edge vk with
          ell_v(vk)!=c and ell_k(vk)=c}.              (17)
```

For each `v in S_c`, choose one such neighbour `k_v`, write its local label
as `f_v(c)!=c`, and put

```text
H_v={x in C^3:x[f_v(c)]=0}.                          (18)
```

Let `R_c=Omega-S_c`.  These are the `c`-rigid vertices.  When `R_c` is
nonempty, contracting every vertex of `R_c` with `e_c` leaves the exact
boundary tensor

```text
e_c^(tensor S_c).                                    (19)
```

Its matching expansion is the full cut Wick response.  Equation (16) is its
two-boundary instance.  If `S_c=Omega`, no vertex is contracted and the
target remains the full `Delta_(n,3)`; that case is handled by the upstream
global bridge classification, not by (19).

### Theorem 5 (partial bridge or deeper blocker)

Exactly one of the following structural alternatives is available.

1. Some edge `pq` induced by `S_c` has endpoint labels satisfying none of

   ```text
   (ell_p,ell_q)=(c,c),
   ell_p=f_p(c),
   ell_q=f_q(c).                                      (20)
   ```

   Then the selected killers of `p,q` lie outside `{p,q}`.  On
   `H_p x H_q` the edge unit is neither zero nor a pure `c` coordinate
   product.  The disabled-killer double-star theorem supplies a `c`-open
   irreducible zero component with two fixed blockers on a dense
   constructible set.  Pointwise, the multi-star theorem then gives either
   at least three `c`-blockers or the exact tight two-blocker permanent with
   its residual pure-`c` factor.

2. Every edge induced by `S_c` obeys (20).  Equivalently, every restriction
   to `H_p x H_q` is a scalar multiple of `x_p[c]x_q[c]`, with zero scalar
   allowed.  If `{alpha,beta}` is the complement of `{c}` and

   ```text
   A={v in S_c:f_v(c)=alpha},
   B={v in S_c:f_v(c)=beta},                          (21)
   ```

   then

   ```text
   ||A|-|B|| <= |R_c|.                               (22)
   ```

### Proof of the balance bound

Inside `S_c`, a pure-`alpha` edge cannot join two vertices of `B`, by (20).
In a pure-`alpha` perfect matching of the full graph, every `B` vertex must
therefore be paired either to `A` or to `R_c`.  Hence

```text
|B|<=|A|+|R_c|.
```

The pure-`beta` matching gives the symmetric inequality, proving (22).

If `S_c=Omega`, (22) gives exact half-half balance.  The full global-bridge
argument in the double-star theorem eliminates its other exceptional normal
and yields the balanced bridge system.  Consequently, if `S_c=Omega` for
all three colours, either a deeper component occurs or all three balanced
bridge systems hold simultaneously, exactly the input of the
[`three-colour balanced-bridge intersection theorem`](THREE_COLOUR_BALANCED_BRIDGE_INTERSECTION_THEOREM.md).

When `S_c` is proper and nonempty, the selected killers (17)--(18), the full
cut response (19), and the balance condition (22) are necessary but do not
propagate `c`-nonrigidity into `R_c`.

## 6. Exact countermechanisms to lower-slice propagation

### A one-deviation cancellation with all lower controls

On vertices `0,...,7`, give the following edges their displayed labels; all
weights are `+1` except `03`, whose weight is `-1`:

```text
00: 01,23,45,67,12,13
10: 02,03
11: 04,15,26,37
22: 05,16,27,34
20: 14,25
01: 24
02: 35
12: every remaining edge.                             (23)
```

This specifies all 28 physical pairs by one nonzero matrix unit.  The three
pure coefficients are uniquely `+1`.  Every near-monochromatic coefficient
and every word with two vertices in one colour and all others in a second
colour is target-correct.  Nevertheless

```text
10000000                                               (24)
```

has two compatible matchings

```text
02|13|45|67,       03|12|45|67,                       (25)
```

with weights `+1,-1`.  Relative to `01|23|45|67`, they are two distinct
one-deviation alternating four-cycles with the same nonzero complement
hafnian.  Their cycle groups cancel exactly.  Seventy-nine other mixed words
remain nonzero, so the displayed system is not a witness.  It proves that the
near deck,
same-colour two-point slices, pure equations, and cycle grouping do not
exclude `k=1`.

### Three simultaneous proper nonrigidity sets

On vertices `0,...,5`, set

```text
00: 05,12,34                         weights +1;
10: 01,03                            weights +1;
02: 25                               weight +1;
02: 45                               weight -1;
11: 13,04,15,23                      weights +1;
22: 24,02,14,35                      weights +1.       (26)
```

The orientation in (26) is the displayed numerical endpoint order.  The
nonrigidity sets are

```text
S_0={0,5},       S_1={1,3},       S_2={2,4}.          (27)
```

For each colour `c`, contracting `Omega-S_c` at `e_c` gives exactly the full
nine-entry boundary tensor `e_c tensor e_c`; the only off-target boundary
channel cancels in two terms.  All pure coefficients equal one.  The full
tensor still has ten nonzero mixed coefficients.  Thus (26) is not a witness,
but it proves that even simultaneous exact two-port cut Grams do not force a
proper `S_c` to become all of `Omega`.  Complementary rigid-core cofactor
equations, not switching alone, carry the missing propagation information.

## 7. Scope and provenance

The matrix-unit classification is imported from
[`MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md`](MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md).
The cycle grouping and rigid-colour definition come from
[`RIGID_COLOUR_COFACTOR_ANNIHILATION_AND_BACKBONE_CANCELLATION_BOUNDARY.md`](RIGID_COLOUR_COFACTOR_ANNIHILATION_AND_BACKBONE_CANCELLATION_BOUNDARY.md).
The componentwise blocker conclusion and full global bridge classification
are imported, with their original hypotheses, from
[`DOUBLE_STAR_ANNIHILATION_LEMMA.md`](DOUBLE_STAR_ANNIHILATION_LEMMA.md) and
[`MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md`](MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md).
The full-flag conclusion also uses
[`THREE_COLOUR_BALANCED_BRIDGE_INTERSECTION_THEOREM.md`](THREE_COLOUR_BALANCED_BRIDGE_INTERSECTION_THEOREM.md)
with its original simultaneous-balance hypotheses.

The four-deviation bound, four-switch type restrictions, pure-support
classification, cofactor-active `k=3` cell, adaptive-baseline exposure,
complete minimum-port packaging, partial-set balance bound, and the two exact
countermechanisms are new here.

```text
r=1 matrix-unit classification:             PROVED UPSTREAM;
minimum deviation k<=4:                     PROVED;
k=4 implies global rigidity:                PROVED;
k=3 paired edge types:                      PROVED;
pure support at k>=3:                       DISJOINT K_(2s)/K_(s,s) COMPONENTS;
k=3 cofactor-active four-cell:              PROVED;
adaptive baseline has >=2 nonzero groups:   PROVED;
complete k<=4 port response:                PROVED;
full flags -> deeper or all-bridge:          PROVED CONDITIONALLY;
proper partial flags propagate globally:    UNKNOWN;
displayed finite systems are KG witnesses:  FALSE;
r=1 branch excluded:                        NO;
global Krenn--Gu conjecture:                 UNRESOLVED.
```

## Focused checks

Run from repository root:

```text
python claims/arbitrary-order/verify_matrix_unit_four_switch_minimal_port_and_partial_bridge.py
python claims/arbitrary-order/audit_matrix_unit_four_switch_minimal_port_and_partial_bridge.py
```

The primary check reconstructs the exact six- and eight-vertex coefficient
tables, all near and two-point slices claimed above, and the mate-involution
deviation ledger.  The independent no-import audit uses a separate matching
representation and coefficient implementation.  These bounded checks audit
endpoint orientation, multiplicity, and the countermechanisms.  The
arbitrary-order proofs are the written matching bijections and the imported
double-star/multi-star implications.
