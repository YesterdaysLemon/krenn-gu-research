# Matrix-unit minimal pure-cofactor port aggregate and conformal-fan reduction

## Status

This is an exact arbitrary-order refinement of the branching side of the
least-supported pure-cofactor theorem.  It works over every field of
characteristic different from two and therefore over `C`.

At a branch vertex, the perfect matchings of the least residual split into
disjoint edge ports.  Every port sum is a nonzero first cofactor.  This gives
an exact alternative:

1. **sparse fan:** there is exactly one perfect matching in every port.  The
   matchings differ from a fixed matching by single alternating cycles, their
   union is a conformal exchange fan, and the residual equation is one exact
   `d`-nomial Laurent relation with monomial port cofactors; or
2. **aggregate port:** at least one nonzero first cofactor contains two or
   more matching monomials.

For two nonmatching ports at the same vertex, the corresponding alternating
cycles contain a conformal theta.  Its path parities are exactly
`odd/odd/odd` or `odd/even/even`.  The first theta has exactly three perfect
matchings and is matching-covered.  The second has exactly two perfect
matchings and leaves one selected port open to an exterior alternating
completion.

Both port alternatives and both cubic theta profiles occur in exact
characteristic-zero least residuals.  In particular, branching arity,
conformal-fan topology, and the local theta parity by themselves do not
contradict a pure hafnian cancellation and do not enter the matrix-unit
deeper-blocker component.  The pure-cofactor exit, the `r=1` branch, and the
global Krenn--Gu conjecture remain **UNKNOWN/UNRESOLVED**.

This theorem is intentionally stated for an abstract least pure residual.
The later all-bridge specialization proves that saturated bit flips make its
least core bipartite, so the one-open-port profile cannot occur there.  It
also adds matching-polytope bounds which force an aggregate port below the
extremal sparse degree.  Those are extra all-bridge hypotheses, not changes
to the generic theorem or to its sharp nonbipartite controls; see
[`ALL_BRIDGE_ACTIVE_DECK_ALL_DEGREE_LOCALIZED_PURE_CANCELLATION_AND_BIPARTITE_CORE_REDUCTION_THEOREM.md`](ALL_BRIDGE_ACTIVE_DECK_ALL_DEGREE_LOCALIZED_PURE_CANCELLATION_AND_BIPARTITE_CORE_REDUCTION_THEOREM.md).

## 1. Imported least-residual core

Let `Z=(z_ij)` be a hollow symmetric scalar matrix on a finite even set `S`.
For even `T subset S`, put

```text
h(T)=haf(Z[T]),                 h(empty)=1.          (1)
```

Let `R subset S` be a least-cardinality even set such that

```text
h(R)=0
and the support graph on R has a perfect matching.  (2)
```

For an edge `e=ij`, write

```text
C_e=z_ij h(R-{i,j}).                                (3)
```

The imported matching-covered-core theorem proves that the graph

```text
G={e:C_e!=0}                                        (4)
```

is exactly the union of all support perfect matchings on `R`.  It is
connected, matching-covered, and has minimum degree at least two.  Every
support perfect matching of `R` is therefore a perfect matching of `G`, and
conversely.

For a perfect matching `M`, let

```text
lambda(M)=product_(e in M) z_e.                     (5)
```

Every such monomial is nonzero.  Write `PM(G)` for the perfect matchings of
`G` and `N=|PM(G)|`.

## 2. Exact cofactor-port partition

Fix a vertex `v`.  For every edge `e` incident with `v`, define its matching
port

```text
PM(v,e)={M in PM(G):e in M}.                        (6)
```

### Theorem 1 (nonzero port partition)

The sets in (6) form a disjoint partition of `PM(G)`, and

```text
C_e=sum_(M in PM(v,e)) lambda(M) !=0,                (7)
h(R)=sum_(e incident with v) C_e=0.                  (8)
```

Consequently

```text
N>=deg_G(v).                                        (9)
```

### Proof

Every perfect matching contains exactly one edge at `v`, proving the
partition.  Expanding `h(R-{v,w})` into matching monomials and multiplying
by `z_vw` gives exactly the full matching monomials containing `vw`.  This
is (7).  There are no hidden complement terms: adjoining `vw` to any
supported complement matching gives a full support matching, so all of its
edges are allowed and lie in `G`.

The nonvanishing in (7) is the imported identity `G={e:C_e!=0}`.  Summing the
port partition gives the hafnian Laplace expansion (8).  Matching-coveredness
makes every port nonempty, so the number of matchings is at least the number
of ports.  QED.

Thus a port with several matching monomials may have internal partial
cancellation, but its total cannot vanish at the least residual.

## 3. Sparse fan or aggregate port

Fix a perfect matching `P` of `G`, a vertex `v`, and its unique incident
`P`-edge `p`.  Put `d=deg_G(v)`.

For every other incident edge `e`, choose a matching `Q_e` containing `e`.
The component through `v` of `P triangle Q_e` is a `P`-alternating even
cycle `Gamma_e` containing both `p` and `e`.  Toggling only that component
gives another full perfect matching

```text
P_e=P triangle Gamma_e.                             (10)
```

Let

```text
K_v=union_(e incident with v, e!=p) Gamma_e.         (11)
```

Every vertex of `K_v` occurs with its `P`-mate, all its cycles share `p`,
and `P` restricts to a perfect matching both on `K_v` and on its vertex
complement.  Hence `K_v` is a connected conformal subgraph.  It contains the
`d` distinct internal perfect matchings

```text
P|K_v,
(P|K_v) triangle Gamma_e       (e!=p),              (12)
```

which use the `d` different edges at `v`.

### Theorem 2 (port-aggregate/conformal-fan dichotomy)

Exactly one of the following holds at `v`.

#### A. Sparse conformal fan

`N=d`.  Every port contains exactly one perfect matching.  For every
`e!=p`, the unique matching `M_e` in that port satisfies

```text
P triangle M_e=Gamma_e                             (13)
```

for one alternating cycle; no additional disjoint exchange cycle occurs.
The perfect matchings of `G` are exactly

```text
P and M_e=P triangle Gamma_e       (e!=p).          (14)
```

Every port cofactor is a single monomial, and division by the nonzero
`lambda(P)` gives the exact Laurent relation

```text
1+sum_(e!=p) rho_e=0,
rho_e=lambda(M_e)/lambda(P)
     =product_(a in M_e-P) z_a / product_(a in P-M_e) z_a.       (15)
```

Each `rho_e` is the character of one alternating cycle.

#### B. Nonzero aggregate port

`N>d`.  At least one incident edge `e` has

```text
|PM(v,e)|>=2,
C_e=sum_(M in PM(v,e)) lambda(M) !=0.               (16)
```

Thus the branching residual contains a structurally unavoidable aggregate
pure-cofactor port.

### Proof

Theorem 1 partitions `N` matchings into `d` nonempty ports.  If `N=d`, every
port is a singleton.  For its unique `M_e`, the symmetric difference with
`P` contains a cycle `Gamma_e` through `v`.  Toggling only `Gamma_e` gives a
perfect matching in the same `e`-port.  Uniqueness forces that matching to be
`M_e`; hence no other symmetric-difference component can occur.  Equations
(14)--(15) follow from (7)--(8).

If `N>d`, the pigeonhole principle gives a port with at least two matchings.
Equation (7) says its aggregate is nevertheless nonzero.  The two cases are
exclusive and exhaustive.  QED.

The word **aggregate** here concerns a pure first-cofactor port.  It is not
being identified with an aggregate active mixed-word fibre without an
additional matrix-unit bridge.

## 4. The conformal theta carried by two exits

Choose two distinct non-`P` edges `e,f` at the same branch vertex `v`, and
choose alternating cycles `Gamma_e,Gamma_f` as above.  Regard
`Gamma_f` as the base cycle.  Starting at `v`, follow `Gamma_e` through `e`
until its first subsequent vertex `y` on `Gamma_f`.  Let that initial path be
`B`.  Its interior is disjoint from `Gamma_f`.  The two `v`--`y` arcs of
`Gamma_f`, together with `B`, form a theta subdivision `H` containing the
three root edges `p,e,f`.

The vertex set of `H` is closed under the `P`-matching.  Indeed, every
interior vertex of `B` uses its `P`-edge inside the alternating path, and the
two endpoints have their `P`-edges on `B union Gamma_f`.  Therefore

```text
P|(R-V(H)) is a perfect matching,                   (17)
```

so `H` is conformal.  This is a subgraph statement; `H` need not be induced,
and the pure support can contain additional chords on the same vertices.

### Theorem 3 (closed or one-open-port theta)

The path `B` has odd length.  The two base-cycle arcs have the same parity.
Consequently exactly one of the following occurs.

#### A. Closed all-odd theta

All three theta paths have odd length.  The theta edge set has exactly three
perfect matchings: each one selects the endpoint edges of one path and the
internal alternating edges of the other two paths.  Every theta edge occurs
in one of them.  Thus `H` is itself matching-covered and realizes all three
root ports `p,e,f` internally.

#### B. One-open-port theta

`B` has odd length and both base arcs have even length.  The theta edge set
has exactly two perfect matchings.  They assign the two endpoints to opposite
even base arcs.  Neither uses the endpoint edge `e` of `B`; the `e`-port is
completed only in the larger conformal fan through `Gamma_e`.  The two cycles
formed from `B` and a base arc are odd, so this profile certifies a
nonbipartite pure core.

### Proof

The path `B` begins with the non-`P` edge `e`.  Its final edge is also
non-`P`: if it were the `P`-edge at `y`, its preceding vertex would already
lie on the `P`-alternating base cycle, contradicting the choice of `y` as the
first return.  Hence the alternating path `B` has odd length.

The base cycle is even, so its two complementary arcs have the same parity.
This proves the two listed parity profiles.

On an odd path between the theta endpoints, a matching of the path either
uses both endpoints or neither.  On an even path it uses exactly one
endpoint.  With three odd paths, exactly one path uses both endpoints, giving
three perfect matchings.  With one odd and two even paths, the odd path uses
neither endpoint and the two even paths use opposite endpoints, giving two
perfect matchings.  The statements about root edges and odd side cycles are
immediate.  QED.

At a degree-`d` vertex there are `binomial(d-1,2)` choices of two exits and
hence that many ordered-independent theta carriers, although their vertices
and edges may overlap.  No disjointness is claimed.

## 5. Finite branch normal form

Apply the branching-excess theorem from the imported core result.

### Corollary 4

Every branching least residual has one of the following exact forms.

1. Some vertex has degree `d>=4`.  At that vertex there is either a sparse
   conformal `d`-fan with one exact `d`-nomial relation (15), or a nonzero
   aggregate port (16).  Every pair of its `d-1` nonmatching exits carries
   one of the two theta profiles in Theorem 3.
2. The maximum degree is three.  Then at least two distinct cubic vertices
   exist.  At each one there is either an exact sparse trinomial conformal
   fan or a nonzero aggregate port, together with a closed or one-open-port
   conformal theta.

This reduces the old unspecified branching case to explicit finite local
carriers and aggregate remainders.  It does not bound the size of the core or
assert that the carriers at two branch sites are disjoint.

## 6. Exact sharpness families

The preceding structures do not themselves contradict minimality.

### 6.1 Sparse `d`-fan for every `d>=3`

Work over `Q`.  Let `Theta_d` have endpoints `u,w` and `d` internally
vertex-disjoint paths of length three

```text
u--a_i--b_i--w,              1<=i<=d.               (18)
```

Give the three edge types weights

```text
z_(u,a_i)=1,
z_(a_i,b_i)=1,
z_(b_i,w)=t_i,
t_1=...=t_(d-1)=1,
t_d=-(d-1).                                         (19)
```

There are exactly `d` perfect matchings:

```text
M_i={u a_i,b_i w} union {a_j b_j:j!=i},
lambda(M_i)=t_i.                                   (20)
```

Hence

```text
haf(Z[V(Theta_d)])=sum_i t_i=0.                    (21)
```

This is a least supported cancellation.  To see it, consider any principal
vertex subset with a support perfect matching.

- If it contains neither endpoint, or exactly one endpoint, its support
  matching is unique and has nonzero weight.
- If it contains both endpoints and has an unpaired internal vertex on two
  different paths, the matching is again unique when it exists.
- The only nonunique case contains both endpoints and the complete internal
  pair `{a_i,b_i}` for every `i` in a nonempty set `I`.  Its hafnian is
  `sum_(i in I)t_i`.  A proper subsum of (19) is never zero.  The only zero
  is `I={1,...,d}`, the full vertex set.

Every edge of `Theta_d` belongs to a matching in (20), so its allowed core is
the whole connected graph.  At `u`, each port is one monomial.  Relative to
`M_1`, the other matchings are the single alternating flips on the two-path
cycles.  Thus (18)--(21) realize the sparse conformal `d`-fan and its exact
`d`-nomial relation at every arity.

For `d=3`, the carrier is the closed all-odd theta of Theorem 3.

### 6.2 The one-open-port cubic profile

On `R={0,1,2,3}`, take the complete graph with

```text
z_01=z_23=z_02=z_13=z_03=1,
z_12=-2.                                            (22)
```

Its three perfect-matching weights are `1,1,-2`; their sum is zero, and all
proper supported even subsets have order two and nonzero hafnian.  Thus this
is again a least residual.

Fix `P={01,23}` at `v=0`, with exits `e=02` and `f=03`.  The two alternating
four-cycles produce a first-return theta with path lengths `1,2,2`.  Its edge
set has the two matchings `{01,23}` and `{03,12}`.  The `02` port requires
the exterior edge `13` from its full alternating cycle.  This realizes the
one-open-port profile while the full cubic fan still has exactly three
perfect matchings and one sparse trinomial cancellation.

### 6.3 A genuine aggregate port

On the bipartite graph `K_(3,3)` with shores `{0,1,2}` and `{3,4,5}`, set all
edge weights to one except

```text
z_03=-2.                                            (23)
```

There are six perfect matchings.  Two use `03` and have weight `-2`; the
other four have weight one, so the full hafnian is zero.  Every proper
supported principal subset has either a unique matching or a `2 by 2`
permanent equal to `2` or `-1`; hence the full six vertices are again the
least cancellation.

At vertex `0`, the three port sums are

```text
C_03=-4,
C_04=2,
C_05=2.                                             (24)
```

Every port contains two monomials, and (24) is a nonzero aggregate-port
cancellation.

These examples are pure scalar residuals, not complete matrix-unit tensor
tables and not Krenn--Gu witnesses.

## 7. Relation to the live proof forest

The branching side of the least pure cancellation is now reduced to

```text
sparse port:
    one conformal d-route alternating fan,
    exactly d full residual matchings,
    monomial first cofactors at the branch vertex,
    one exact d-nomial Laurent relation;

aggregate port:
    at least one nonzero first cofactor with multiple matching monomials;

cubic local carrier:
    a closed three-matching all-odd theta,
    or a two-matching odd/even/even theta whose open port needs an
    exterior alternating completion.                              (25)
```

The arbitrary-`d` family proves that no contradiction follows from the
number of ports, the existence of a conformal fan, or the sparse Laurent sum
alone.  The `K_4` and `K_(3,3)` models show that neither cubic theta profile
nor the aggregate alternative is empty.

A continuation must therefore add data absent here: a mixed target equation
that couples to the distinguished fan monomials, a theorem controlling the
aggregate port remainders, or root/killer incidence that genuinely enters
the deeper-blocker component.  Existing deeper-blocker theorems do not take
a pure conformal fan as a sufficient input.

In the simultaneous balanced all-bridge branch, the later bipartite-core
specialization removes the one-open profile, proves `N>=beta+1`, and confines
a sparse port site to `d=N=beta+1`.  Closed all-odd sparse fans and nonzero
aggregate ports both remain open as exclusions.

## 8. Assumptions and boundary

```text
field for the structural theorem:                 characteristic not two;
sharpness families:                               exact over Q;
residual:                                          least even supported hafnian zero;
active graph:                                      allowed matching-covered core;
cofactor ports partition all residual matchings:   PROVED;
every port sum nonzero:                            PROVED by minimality/core identity;
sparse fan or aggregate port:                      PROVED EXHAUSTIVE;
sparse matching differs by one alternating cycle:  PROVED;
fan is conformal:                                  PROVED;
closed/open theta parity dichotomy:                PROVED EXHAUSTIVE;
all arities sparse-sharp:                          PROVED over Q;
both cubic theta profiles sharp:                   PROVED over Q;
aggregate-port branch nonempty:                    PROVED over Q;
fan or aggregate port forces deeper blocker:       UNKNOWN;
mixed target equation couples to fan characters:   UNKNOWN;
pure-cofactor exit excluded:                       UNKNOWN;
general r=1 branch excluded:                       UNKNOWN;
global Krenn--Gu conjecture:                       UNRESOLVED.
```

No division is used except by the explicitly nonzero matching monomial
`lambda(P)` in (15).  No claim is made that a theta carrier is induced, that
different carriers are disjoint, or that a multi-term port is an aggregate
mixed-word fibre.

## 9. Evidence and replay

Run:

```powershell
python claims/arbitrary-order/verify_matrix_unit_minimal_pure_cofactor_port_aggregate_and_conformal_fan.py
python claims/arbitrary-order/audit_matrix_unit_minimal_pure_cofactor_port_aggregate_and_conformal_fan.py
python -m py_compile claims/arbitrary-order/verify_matrix_unit_minimal_pure_cofactor_port_aggregate_and_conformal_fan.py claims/arbitrary-order/audit_matrix_unit_minimal_pure_cofactor_port_aggregate_and_conformal_fan.py
python -m ruff check claims/arbitrary-order/verify_matrix_unit_minimal_pure_cofactor_port_aggregate_and_conformal_fan.py claims/arbitrary-order/audit_matrix_unit_minimal_pure_cofactor_port_aggregate_and_conformal_fan.py
```

The primary verifier uses exact rational hafnians and recursive matching
enumeration.  It checks sparse `Theta_d` residuals at several arities, the
two theta parity profiles, the single-cycle fan construction, the `K_4`
open-port completion, and the aggregate `K_(3,3)` port sums.

The independent no-import audit uses edge masks, route-state formulas, and
bipartite permutation sums rather than importing the primary implementation.
It checks the principal-subset minimality mechanism, endpoint-state theta
matching counts, sparse port characters, and aggregate port partition.
These bounded checks audit the formulas and sharpness models.  The arbitrary-
order conclusions are the matching partition, alternating-cycle toggle,
first-return theta, and parity proofs above.
