# Matrix-unit minimal pure-cofactor matching-covered core and single-cycle theorem

## Status

This is an exact arbitrary-order refinement of the least-supported pure-
cofactor exit in the `r=1` matrix-unit branch.  It works over every field of
characteristic different from two and therefore over `C`.

The preceding phase-holonomy theorem proved that a least supported pure
hafnian cancellation has an active first-cofactor graph of minimum degree at
least two.  It left the degree-two case as a spanning disjoint union of even
cycles and the other case as unspecified phase branching.

Minimality gives substantially more:

1. the active first-cofactor graph is exactly the allowed-edge graph, namely
   the union of all perfect matchings of the pure support;
2. this allowed-edge graph is connected and matching-covered;
3. every active edge lies on an alternating even cycle relative to every
   fixed perfect matching;
4. the degree-two branch is one **single** even cycle, has exactly two perfect
   matchings, and gives one primitive signed Laurent binomial with monomial
   first cofactors; and
5. the branching branch is a connected multi-cycle exchange core with at
   least three perfect matchings and cyclomatic rank at least two.  Its total
   branching excess is a positive even integer, so it has either a vertex of
   degree at least four or at least two vertices of degree at least three.

This is a sharper structural reduction, not an exclusion.  A primitive pure
cycle relation can be consistent, and the theorem does not force the
branching core into the deeper-blocker component.  The `r=1` branch and the
global Krenn--Gu conjecture remain **UNKNOWN/UNRESOLVED**.

## 1. Least supported pure cancellation

Let `Z=(z_ij)` be a hollow symmetric scalar matrix on a finite even set `S`.
For every even `T subset S`, write

```text
h(T)=haf(Z[T]),              h(empty)=1.             (1)
```

Assume `h(S)=0` although the support graph of `Z[S]` has a perfect matching.
Choose an even subset `R subset S` of least cardinality such that

```text
h(R)=0
and the support graph G_R has a perfect matching.    (2)
```

Then `|R|>=4`.  Fix one perfect matching `P` of `G_R`.

For every pair `ij subset R`, put

```text
C_ij=z_ij h(R-{i,j}),                               (3)
```

and let `A_R` be the graph of pairs for which `C_ij!=0`.

Call an edge of `G_R` **allowed** if it belongs to at least one perfect
matching of `G_R`.  Let `Allow(G_R)` be the spanning graph of all allowed
edges.

The imported minimal-cofactor theorem gives

```text
P subset A_R,
sum_(j!=i) C_ij=0        for every i in R,           (4)
```

and hence `delta(A_R)>=2`.

## 2. Active cofactors are exactly allowed edges

### Theorem 1 (allowed-core identity)

One has the exact graph identity

```text
A_R=Allow(G_R).                                      (5)
```

Consequently the perfect matchings of `G_R` and `A_R` are the same.

### Proof

If `ij in A_R`, then `z_ij!=0` and

```text
h(R-{i,j})!=0.                                      (6)
```

A nonzero hafnian has at least one nonzero matching term, so the support on
`R-{i,j}` has a perfect matching.  Adjoining `ij` gives a perfect matching
of `G_R`; hence `ij` is allowed.

Conversely, suppose `ij` is allowed.  Then `z_ij!=0`, and deleting it from a
perfect matching containing it leaves a supported perfect matching on
`R-{i,j}`.  This is a proper even subset of `R`.  Minimality in (2) therefore
forces

```text
h(R-{i,j})!=0,                                      (7)
```

so `C_ij!=0` and `ij in A_R`.  This proves (5).

Every perfect matching uses only allowed edges.  Conversely every perfect
matching of the allowed subgraph is a support matching of `G_R`, proving the
last statement.  QED.

Thus first-cofactor activity has no hidden phase-dependent edge deletion at
the least residual: it is determined exactly by perfect-matching support.

## 3. Minimality forces connectedness

Let the connected components of `A_R` have vertex sets

```text
R_1,...,R_s.                                        (8)
```

The fixed matching `P` uses only `A_R`, so it restricts to a perfect matching
on every `R_q`.  In particular every component has positive even order.

### Theorem 2 (matching-covered connected core)

The graph `A_R` is connected.  Hence it is a connected matching-covered graph
of minimum degree at least two.

### Proof

Every perfect matching of `G_R` uses only allowed edges by Theorem 1 and
therefore stays inside the components in (8).  Conversely, any choice of one
support perfect matching on each `R_q` has a disjoint union which is a perfect
matching of `G_R`.  Matching weights multiply, so the full hafnian factors
exactly:

```text
h(R)=product_(q=1)^s h(R_q).                         (9)
```

The left side is zero.  Over a field, at least one factor `h(R_q)` is zero.
Its component supports the restricted matching `P|R_q`.  If `s>1`, this
would be a smaller even supported cancellation than `R`, contradicting (2).
Therefore `s=1`.  QED.

Support edges between putative components cannot evade the argument: if one
occurred in a full perfect matching, it would be allowed and would join the
components; if it occurs in none, it contributes to no term of (9).

## 4. Alternating-cycle generation

Fix any perfect matching `P` of `A_R`.

### Theorem 3 (every active edge is alternating)

Every edge of `A_R` lies on a `P`-alternating even cycle.

### Proof

If an active edge `e` is not in `P`, Theorem 1 supplies a perfect matching
`Q` containing `e`.  The symmetric difference `P triangle Q` is a disjoint
union of `P`-alternating even cycles, one of which contains `e`.

Now let `e=uv in P`.  Since `delta(A_R)>=2`, choose an active edge `f!=e`
incident with `u`.  It is not in `P`.  Choose a perfect matching `Q`
containing `f`.  At `u`, the component of `P triangle Q` containing `f`
also contains the unique `P`-edge `e`.  Thus `e` lies on a `P`-alternating
even cycle as well.  QED.

This is an exact exchange property of the least residual.  It does not say
that the alternating cycle itself has zero hafnian.

## 5. Sharpened cycle/branching dichotomy

### Theorem 4 (single cycle or connected exchange core)

Exactly one of the following holds.

#### A. Primitive single-cycle branch

`A_R` is one connected even cycle.  It has exactly two perfect matchings,
say `P_0,P_1`, and

```text
h(R)=lambda(P_0)+lambda(P_1)=0,                     (10)
```

so

```text
lambda^(1_(P_0)-1_(P_1))=-1.                       (11)
```

The exponent in (11) is primitive.  For every cycle edge `e`, the support on
`R-endpoints(e)` has exactly one perfect matching, and its hafnian is that
single nonzero matching monomial.  Every support edge outside the cycle has
no perfect-matching complement and has zero first cofactor for structural,
not cancelling, reasons.

#### B. Branching exchange-core branch

`A_R` is connected and matching-covered, has at least three perfect
matchings, and has cyclomatic rank

```text
beta=|E(A_R)|-|R|+1 >=2.                            (12)
```

Every edge lies on an alternating even cycle relative to `P`, and at least
two distinct such cycles occur.  Moreover

```text
sum_(v in R) (deg(v)-2)=2(beta-1),                  (13)
```

a positive even integer.  Therefore either some vertex has degree at least
four or at least two vertices have degree at least three.

### Proof

If every vertex has degree two, Theorem 2 makes `A_R` one cycle.  The
restriction of `P` makes its length even.  An even cycle has exactly its two
alternating perfect matchings, and Theorem 1 says there are no other perfect
matchings of `G_R`.  This gives (10), and division by the nonzero monomial
`lambda(P_1)` gives (11).  Its exponent has entries in `{0,+1,-1}` and at
least one entry of magnitude one, so it is primitive.

Deleting the endpoints of a cycle edge leaves one even path, which has a
unique perfect matching.  Any different supported matching of that
complement, when joined to the deleted edge, would be a full perfect matching
using an edge outside the cycle, contradicting Theorem 1.  The assertion
about an outside support edge is the contrapositive of allowedness.

Otherwise some degree is at least three.  Since every degree is at least two,

```text
2|E(A_R)|=sum_v deg(v) >= 2|R|+2,                  (14)
```

where the excess is at least two because the degree sum is even.  Equations
(12)--(13) follow.

One perfect matching alone would make `A_R=P`, contradicting minimum degree
two.  If there were only two perfect matchings, their union would be a disjoint
union of common matching edges and alternating even cycles.  Minimum degree
two removes common isolated matching edges, and connectedness leaves one
even cycle, contrary to branching.  Thus at least three perfect matchings
occur.

Theorem 3 shows that the graph is generated by `P`-alternating cycles.  If
only one distinct cycle occurred, every edge would lie on it and `A_R` would
again be a cycle.  Hence there are at least two.  Finally (13) shows that the
branching excess cannot consist of one degree-three vertex alone: it is
realized by one excess of at least two or by at least two positive excesses.
QED.

## 6. Relation to the matrix-unit proof forest

In the pure-cancellation exit of active-word transport, `Z` is one pure-
colour shore matrix and `R` is selected inside the vanishing shore hafnian.
Theorem 4 replaces the previous normal form by

```text
pure cycle:
    one primitive even-cycle binomial,
    exactly two matching terms,
    monomial nonzero first cofactors;

pure branching:
    one connected matching-covered core,
    at least three matching terms,
    cyclomatic rank at least two,
    at least two branch sites or one degree-at-least-four site.   (15)
```

The cycle branch can now enter the signed-relation machinery as one exact
primitive pure relation.  The branching branch supplies multiple conformal
matching exchanges rather than an arbitrary three-term row sum.  Neither
fact is yet a contradiction.

The exact surviving obligations are:

1. combine the primitive pure-cycle relation with active mixed response data
   and prove a signed inconsistency or target-lattice unit;
2. use the connected multi-cycle exchange core to force a deeper blocker or
   another target equation;
3. exclude or further classify aggregate active-cycle fibres; or
4. close the remaining global `r=1` matrix-unit branch by another route.

## 7. Assumptions and boundary

```text
field:                                      characteristic not two;
matrix:                                     hollow symmetric scalar pure shore;
residual:                                   least-cardinality even supported hafnian zero;
active graph equals allowed-edge graph:     PROVED;
active graph connected/matching-covered:    PROVED;
every active edge P-alternating:             PROVED;
degree-two branch is one even cycle:         PROVED;
cycle has exactly two terms/monomial cofactors: PROVED;
branching core beta at least two:            PROVED;
branching core has at least three matchings: PROVED;
primitive pure-cycle relation inconsistent: UNKNOWN;
branching core forces deeper blocker:        UNKNOWN;
pure-cofactor exit excluded:                 UNKNOWN;
aggregate active-cycle fibre excluded:       UNKNOWN;
general r=1 exclusion:                       UNKNOWN;
global Krenn--Gu conjecture:                  UNRESOLVED.
```

The theorem concerns the exact least residual, not the full pure support
graph before minimalization.  Edges outside `A_R` may remain present in the
pure support, but they lie in no perfect matching of `R` and contribute to no
full residual matching term.

## 8. Evidence and replay

Run:

```powershell
python claims/arbitrary-order/verify_matrix_unit_minimal_pure_cofactor_matching_covered_core_and_single_cycle.py
python claims/arbitrary-order/audit_matrix_unit_minimal_pure_cofactor_matching_covered_core_and_single_cycle.py
python -m py_compile claims/arbitrary-order/verify_matrix_unit_minimal_pure_cofactor_matching_covered_core_and_single_cycle.py claims/arbitrary-order/audit_matrix_unit_minimal_pure_cofactor_matching_covered_core_and_single_cycle.py
python -m ruff check claims/arbitrary-order/verify_matrix_unit_minimal_pure_cofactor_matching_covered_core_and_single_cycle.py claims/arbitrary-order/audit_matrix_unit_minimal_pure_cofactor_matching_covered_core_and_single_cycle.py
```

The primary verifier uses exact rational hafnian recursion and an independent
perfect-matching census.  It checks least-residual selection, allowed-edge
and active-cofactor equality, component factorization, a six-cycle with an
inactive support chord, unique first cofactors, primitive binomial data, and
the connected branching `K_4` core.

The independent no-import audit uses bitmask matchings, separate rational row
reduction, different cycle and branching weights, and a disconnected
nonminimal cancellation whose least residual is recovered before the core is
tested.  The finite checks audit the mechanisms and sharpness models; the
arbitrary-order result is the proof above.
