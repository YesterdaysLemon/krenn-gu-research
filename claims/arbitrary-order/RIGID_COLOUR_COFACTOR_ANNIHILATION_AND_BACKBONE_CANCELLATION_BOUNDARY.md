# Rigid-colour cofactor annihilation and backbone-cancellation boundary

## Status

This note proves an exact conditional reduction inside the `r=1`
matrix-unit branch of the maximal torus-root theorem.  If one target colour
is rigid at every vertex, every coefficient factors into a principal hafnian
in that colour and an induced two-colour matching tensor.  The witness
equations then become an exact annihilating-deletion-deck system.

Without any rigidity assumption, near-monochromatic words give an exact
active-deck identity at every vertex, two-point words give a pure-cofactor
versus cross-cycle dichotomy, and a minimal-deviation word reduces every
remaining cancellation to pure-cofactor vanishing or cancellation among
cycles spanning all deviations.

The note also gives an exact six-vertex matrix-unit graph in which all three
mixed perfect matchings in the selected Bogdanov backbone cancel
simultaneously.  Six different mixed coefficients remain nonzero, so the
graph is **not** a Krenn--Gu witness.  It refutes only the shortcut claiming
that backbone cancellation itself is impossible or already forces the
simultaneous balanced all-bridge normal form.

No theorem here forces a globally rigid colour in every `r=1` witness, and
the rigid-colour deletion system is not excluded.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## 1. Matrix-unit and rigidity conventions

Let `Omega` have even size `n>=6`, and suppose every physical edge block is
one nonzero matrix unit, as forced by the `r=1` branch of
[`MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md`](MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md).
For an edge `e={u,v}`, write

```text
B_e(x_u,x_v)
 = lambda_e x_u[ell_u(e)] x_v[ell_v(e)],
lambda_e != 0.                                      (1)
```

The labels `ell_u(e)` and `ell_v(e)` are attached to the displayed endpoints;
reversing the edge reverses the two labels but not `lambda_e`.

Fix a colour `c`.  A vertex `v` is **`c`-rigid** when, on every incident
edge `e={u,v}`,

```text
ell_u(e)=c  =>  ell_v(e)=c.                          (2)
```

Thus `v` has no incident unit whose remote half-label is `c` and whose local
half-label is different from `c`.  Failure of (2) is exactly the availability
of an off-diagonal column-`c` singleton at `v`; obtaining all further
all-bridge hypotheses still requires the separate double-star analysis.

Let `Z^c` be the scalar symmetric matrix

```text
Z^c_uv = lambda_{uv}  if ell_u(uv)=ell_v(uv)=c,
       = 0            otherwise.                    (3)
```

For `U subset Omega`, let `W^{!=c}[U]` be the induced matrix-unit graph on
`U` after restricting every local space to the two colours other than `c`.
Its tensor is denoted `T_{W^{!=c}[U]}`.  Odd matching tensors are zero, and
`haf(Z^c[S])=0` for odd `|S|`, while `haf(Z^c[empty])=1`.

## 2. Rigid-colour factorization

### Lemma 1 (two rigid endpoints)

If `u` and `v` are both `c`-rigid, then their edge is either labelled
`(c,c)` or both endpoint labels avoid `c`.

### Proof

If `ell_u(uv)=c`, rigidity at `v` forces `ell_v(uv)=c`.  If instead
`ell_v(uv)=c`, rigidity at `u` forces `ell_u(uv)=c`.  Therefore exactly one
endpoint cannot carry `c`.

### Lemma 2 (rigid avoiding-edge cofactor)

Assume `T_W=Delta_(n,3)`.  If `u,v` are `c`-rigid and their edge has labels
`(a,b)` with `a,b!=c`, then

```text
haf(Z^c[Omega-{u,v}])=0.                             (4)
```

### Proof

Give `u` colour `a`, give `v` colour `b`, and give every other vertex colour
`c`.  If `u` were paired to an outside vertex, the remote half-label seen
from `u` would be `c`; rigidity would force the local label at `u` to be
`c`, contradicting its assigned colour `a`.  The same holds for `v`.
Consequently every compatible perfect matching uses the edge `uv`, and the
coefficient of this forbidden word is exactly

```text
lambda_uv haf(Z^c[Omega-{u,v}]).                     (5)
```

The target coefficient is zero and `lambda_uv!=0`, proving (4).  There is no
division by a hafnian and no uniqueness assumption inside the complement.

### Theorem 3 (global rigid-colour factorization)

Assume every vertex is `c`-rigid.  For a word
`chi:Omega->{0,1,2}`, put `S=chi^(-1)(c)`.  Then

```text
[T_W]_chi
 = haf(Z^c[S])
   [T_{W^{!=c}[Omega-S]}]_(chi restricted to Omega-S).   (6)
```

### Proof

By Lemma 1, an edge compatible with `chi` cannot cross from `S` to
`Omega-S`: such an edge would have exactly one endpoint labelled `c`.
Every compatible perfect matching is therefore the disjoint union of a
`(c,c)` matching on `S` and a no-`c` matching on `Omega-S`.  Conversely any
such pair reconstructs one compatible perfect matching.  Products and
multiplicities are preserved, so summing the bijection gives (6), including
the empty and odd cases under the stated conventions.

### Corollary 4 (exact annihilating-deletion-deck system)

Under global `c`-rigidity, `T_W=Delta_(n,3)` is equivalent to all three of:

```text
haf(Z^c[Omega])=1;                                   (7)

T_{W^{!=c}[Omega]}=Delta_(n,2);                      (8)

for every nonempty proper even S subset Omega,
  haf(Z^c[S])!=0
  => T_{W^{!=c}[Omega-S]} is identically zero.       (9)
```

Indeed, (7) is the all-`c` word, (8) is the collection of words avoiding
`c`, and (9) is exactly (6) for all remaining words.  The reverse implication
uses the same exhaustive partition of the word set.  Equation (9) is a
pointwise annihilating principal-deletion deck, not a contradiction.  In
particular, taking `S=Omega-{u,v}` and the nonzero two-vertex avoiding-edge
coefficient recovers (4) for every physical edge avoiding `c`.

## 3. Exact six-vertex cancellation boundary

Use the ordered vertex list

```text
A0,A1,A2,B0,B1,B2.                                   (10)
```

For every cross edge `Ai Bj`, set its weight to `+1` and give both endpoints
the diagonal colour

```text
d=j-i mod 3.                                         (11)
```

On the two triangles, the ordered endpoint labels and weights are

```text
A0 A1 : (1,2),  +1       B0 B1 : (2,1),  -1
A1 A2 : (1,2),  +1       B1 B2 : (2,1),  -1
A0 A2 : (2,1),  +1       B0 B2 : (1,2),  -1.         (12)
```

These nine cross edges and six triangle edges specify all 15 physical pairs,
and every weight is nonzero.  Hence every edge bilinear is nonzero on the
full coordinate torus and the maximum torus-root cardinality is exactly one.
Colour `0` is globally rigid: its only incident remote-`0` labels occur on
the diagonal `(0,0)` cross edges.

The three cyclic-shift cross matchings are the unique pure-colour matchings,
so the pure coefficients are

```text
000000 : +1,
111111 : +1,
222222 : +1.                                         (13)
```

The three nonmonochromatic cross matchings have words

```text
012021,
120210,
201102.                                               (14)
```

For each word, the cross matching has weight `+1`.  A second matching keeps
its colour-`0` cross edge and uses the corresponding `A`- and `B`-triangle
edges, with total weight `-1`.  Thus every coefficient in (14) is exactly
zero.

The six remaining matching-induced words are

```text
112112, 121121, 122122,
211211, 212212, 221221.                               (15)
```

Each has one compatible matching, of weight `-1`.  No other word is induced
by a perfect matching.  Therefore the graph satisfies every target
coefficient involving colour `0`, all nonempty proper deletion conditions
in (9), and the pure `1`/`2` coefficients, but it fails exactly the six
no-`0` mixed coefficients (15).  It is not a counterexample to Krenn--Gu.

The construction proves the following precise no-go statement:

```text
simultaneous cancellation of all mixed matchings
in the selected three-matching Bogdanov backbone
does not imply a contradiction, all-bridge entry,
or the full tensor identity.                          (16)
```

Off-backbone mixed coefficients are a logically necessary part of any
continuation from the `r=1` cancellation obligation.

## 4. Universal deck and minimal-cycle consequences

Return to an arbitrary `r=1` matrix-unit branch satisfying
`T_W=Delta_(n,3)`; no rigidity assumption is made in this section.

### Theorem 5 (near-monochromatic active deck)

For vertices `u!=v`, put

```text
C^c_uv=haf(Z^c[Omega-{u,v}]).                         (17)
```

Then, for every vertex `v` and colours `c,d`,

```text
sum_(u!=v : ell_v(vu)=d and ell_u(vu)=c)
  lambda_vu C^c_vu
 = 1  if d=c,
 = 0  if d!=c.                                       (18)
```

### Proof

Give `v` colour `d` and every other vertex colour `c`.  In every compatible
perfect matching, `v` has one partner `u` with the displayed endpoint labels,
and the remaining vertices contribute `C^c_vu`.  Partitioning by `u` gives
the left side of (18).  The target word is pure exactly when `d=c`.

For `d=c`, equation (18) gives at least one incident `(c,c)` edge with
nonzero cofactor at every vertex.  Thus the active cofactor support for each
pure colour has no isolated vertex.  For `d!=c`, if at least one summand is
nonzero then at least two are: one nonzero term cannot sum to zero over `C`.

### Theorem 6 (two-point cofactor versus cross cycle)

Fix an edge `e={p,q}` labelled `(c,c)`, and fix `d!=c`.  For an outside
vertex `u`, define

```text
X_pu^(c,d) = lambda_pu
  if ell_p(pu)=c and ell_u(pu)=d,
  and 0 otherwise,                                   (19)
```

and similarly for `q`.  With `U=Omega-{p,q}`, the two-point word that is `c`
at `p,q` and `d` on `U` gives

```text
0 = lambda_e haf(Z^d[U])
  + sum_({u,v} subset U)
      (X_pu X_qv + X_pv X_qu)
      haf(Z^d[U-{u,v}]).                             (20)
```

### Proof

A compatible matching either uses `e`, leaving a pure-`d` matching on `U`,
or sends `p,q` to two distinct outside vertices and leaves a pure-`d`
matching after deleting those partners.  The two bijections to `{u,v}` give
the displayed `2 x 2` permanent.  These alternatives are disjoint and
exhaustive, proving (20); the target word is nonconstant, so its coefficient
is zero.

If `haf(Z^d[U])!=0`, the first term is nonzero.  Hence some correction term
contains two disjoint nonzero `c`-to-`d` cross edges and a nonzero pure-`d`
four-deletion cofactor.  Choose one nonzero pure matching monomial in the
first term and one in that correction.  Their symmetric difference contains
an alternating cycle through `e`; relative to the first matching, `e` is the
unique baseline `c`-coloured edge on that cycle.  Therefore every pure edge
and other colour obey the exact, nonexclusive dichotomy

```text
pure deletion cofactor vanishes,
or a compatible two-cross-edge alternating cycle exists.   (21)
```

### Theorem 7 (minimal-deviation cycle normal form)

Among all nonconstant words induced by at least one physical perfect matching,
choose a pair `(chi,c)`, with `c` occurring in `chi`, minimizing

```text
|D|, where D={v:chi(v)!=c}.                           (22)
```

Thus `D` is nonempty and proper.

Such a word exists: the three pure target coefficients supply three
physically edge-disjoint pure perfect matchings, and the Bogdanov theorem
supplies a nonmonochromatic matching in their union.  Fix any nonzero pure-`c`
perfect matching `M_c`.

For every perfect matching `F` inducing `chi`, the symmetric difference
`F triangle M_c` has exactly one alternating component that meets `D`, and
that component contains all of `D`.  Every other nontrivial component is
pure `c`.

Indeed, every vertex of `D` lies in a nontrivial component.  If two distinct
components met `D`, replace the `F` edges by the `M_c` edges on one of them.
The resulting perfect matching would induce a nonconstant word with a
deviation set of strictly smaller cardinality, contradicting (22).  A
component disjoint from `D` uses only `(c,c)` edges on both alternating
parities.

Call an unoriented `M_c`-alternating cycle **active for `chi`** when it
contains `D` and its non-`M_c` parity has the endpoint labels prescribed by
`chi`.  Each cycle edge set is counted once.  Put

```text
w(C)=product_(e in C-M_c) lambda_e.                   (23)
```

Grouping the forbidden coefficient by its unique `D`-spanning component
gives the exact arbitrary-order identity

```text
0=[T_W]_chi
 = sum_(active C containing D)
     w(C) haf(Z^c[Omega-V(C)]).                      (24)
```

For a fixed cycle `C`, all remaining vertices have word colour `c`; their
complete contribution is precisely the displayed principal hafnian.  This
proves (24) without assuming uniqueness or absence of pure cycles in the
complement.

Equation (24) says that the number of nonzero cycle groups is either zero or
at least two.  Equivalently, the only two mechanisms left at minimal
deviation are

```text
every eligible cycle group is killed by a zero pure principal cofactor,
or at least two nonzero cycle groups cancel.          (25)
```

More generally, if there is a unique eligible active cycle, its complement
hafnian must vanish.  In particular such a unique cycle cannot leave zero or
two vertices: the empty hafnian is one, while a two-vertex complement is one
edge of `M_c` and has nonzero hafnian.  This is a structural cancellation
normal form, not an exclusion of the `r=1` branch.

## 5. Frontier and provenance

The maximum-one matrix-unit classification is imported from the maximal
torus-root theorem.  The existence of a mixed perfect matching in the union
of three differently coloured perfect matchings is the Bogdanov input already
recorded in
[`UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md`](UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md).
The rigid-colour definition, factorization (6), annihilation system (7)--(9),
exact cancellation boundary (10)--(16), active-deck identity (18), two-point
dichotomy (20)--(21), and minimal-cycle normal form (22)--(25) are the new
statements here.

```text
r=1 all-matrix-unit branch:                    PROVED upstream;
rigid avoiding-edge cofactor vanishing:        PROVED;
global rigid-colour coefficient factorization: PROVED CONDITIONALLY;
rigid-colour annihilating deletion system:      EXACT, NOT EXCLUDED;
existence of a globally rigid colour:           NOT FORCED;
near-monochromatic active-deck identity:         PROVED;
two-point cofactor/cross-cycle dichotomy:         PROVED;
minimal-deviation cycle normal form:             PROVED;
Bogdanov-backbone cancellation impossible:      REFUTED;
displayed six-vertex graph is a KG witness:      FALSE;
nonrigid branch to all-bridge/deeper blocker:    UNKNOWN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Focused checks

Run from repository root:

```text
python claims/arbitrary-order/verify_rigid_colour_cofactor_annihilation_and_backbone_cancellation_boundary.py
python claims/arbitrary-order/audit_rigid_colour_cofactor_annihilation_and_backbone_cancellation_boundary.py
```

The primary check reconstructs the 15 labelled perfect matchings, their exact
integer coefficients, global colour-`0` rigidity, and the factorization on
all `3^6` words of the displayed graph.  It also checks the near-monochromatic
and two-point ledgers on the colour-`0` exact slice.  The independent no-import
audit uses an explicit 15-matching ledger and a separate coefficient
implementation.  These bounded checks audit endpoint conventions and the
countermechanism.  The arbitrary-order statements are the written
matching-bijection and cycle-grouping proofs.
