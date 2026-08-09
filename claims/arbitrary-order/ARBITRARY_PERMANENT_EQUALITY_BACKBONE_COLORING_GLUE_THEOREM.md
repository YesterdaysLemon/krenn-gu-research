# Arbitrary permanent equality backbone-colouring glue theorem

## Status

This is an exact characteristic-zero gluing criterion for the at-most-four
pure backbones in the `3m+2` equality stratum.  Every fixed-backbone
cancellation graph is canonically bipartite, so the only possible gain
obstruction lies in how those bipartitions disagree on shared ratio states.

The disagreement is completely measured by a second signed graph whose
vertices are connected components of the fixed-backbone graphs.  The full
all-backbone graph is bipartite if and only if this component-overlap graph
is balanced over `F_2`.

In particular, two adjacent cube backbones already contradict equality if
one common cancellation component connects two shared states whose relative
source-side parity changes across the pure switch.  This is a conditional
obstruction, not yet a proof that such a straddling component must occur.

## Fibre graphs

Let `T` be the face of `{0,1}^k`, with `k<=2`, parametrizing all pure
backbones from the pure-matching cube theorem.  The case `k=2` can occur
only in its co-located noncoordinate-excess branch.  For each `t in T`, let

```text
Gamma_t=(V_t,E_t)                                    (1)
```

be its fixed-backbone cancellation graph.  Every edge joins a state whose
pure edge ends at `p_1` to one whose pure edge ends at `p_2`.  On every
connected component `C` choose the canonical side map

```text
s_(t,C):C -> F_2,                                    (2)
s_(t,C)(u)+s_(t,C)(v)=1 for every edge uv in C.
```

A global exchange of the names `p_1,p_2` flips (2) on every component.
Independently, any connected-component side map is defined only up to adding
one on that component.  Such a change toggles all incident overlap labels
below, which is standard `F_2` switching and preserves every cycle sum.

Let

```text
Gamma^*=union_(t in T) Gamma_t                       (3)
```

after identifying equal physical ratio states `(i,c)` across fibres.

## Component-overlap gain graph

Define `Omega` as follows.

- A vertex of `Omega` is a pair `(t,C)` with `C` a connected component of
  `Gamma_t`.
- Whenever one physical ratio state `v` belongs to components `C` of
  `Gamma_t` and `D` of `Gamma_u`, add an overlap edge between `(t,C)` and
  `(u,D)` labelled

  ```text
  ell_v=s_(t,C)(v)+s_(u,D)(v) in F_2.                (4)
  ```

Parallel overlap edges are retained.  If a state belongs to more than two
fibres, add all pairwise overlap edges; equivalently, one may use an
incidence node carrying the shared global value `x_v`, with star equations
`kappa_(t,C)+x_v=s_(t,C)(v)`.

## Glue theorem

The following are equivalent.

1. `Gamma^*` is bipartite.
2. There is a global side map `x:V(Gamma^*) -> F_2` with
   `x_v+x_w=1` on every cancellation edge.
3. There are component offsets `kappa_(t,C) in F_2` satisfying

   ```text
   kappa_(t,C)+kappa_(u,D)=ell_v                     (5)
   ```

   on every overlap edge (4).
4. The xor sum of the labels (4) around every cycle of `Omega` is zero.

Proof.  Conditions 1 and 2 are the definition of bipartiteness.  Given `x`,
the quantity

```text
kappa_(t,C)=x_v+s_(t,C)(v)                           (6)
```

is independent of `v in C`, because both `x` and `s_(t,C)` change by one
across every edge.  Equality of the two expressions for a shared state gives
(5).  Conversely, offsets satisfying (5) define

```text
x_v=s_(t,C)(v)+kappa_(t,C),                          (7)
```

independently of which fibre component containing `v` is used.  Finally,
(5) is the standard vertex-potential equation on an `F_2`-gain graph; it is
solvable exactly when every cycle label sum is zero.

## Two-state parity obstruction

Suppose components `(t,C)` and `(u,D)` share two ratio states `v,w`.  The
two parallel overlap edges form a length-two cycle in `Omega`.  Balance
requires

```text
s_(t,C)(v)+s_(t,C)(w)
 =s_(u,D)(v)+s_(u,D)(w).                             (8)
```

Thus a relative-parity disagreement in (8) proves that `Gamma^*` is
nonbipartite and excludes equality.

Now let `t,u` be adjacent vertices of the pure-backbone cube, differing by
one colour switch.  That switch exchanges `p_1,p_2` on exactly two
mode--colour states.  If `v,w` lie together in a cancellation component in
both fibres and exactly one of them is switched, then the two sides of (8)
differ by one.  This **one-switch straddling condition** is therefore an
exact contradiction.

The remaining combinatorial task is sharply stated:

> prove that some nontrivial pure switch has a pair of shared states that
> straddles the switch and lies in one cancellation component on both sides
> of the cube edge, or classify the systems in which every switch avoids
> this condition.

No assertion of existence is made here.

## Literature relation

This is elementary descent for bipartite colourings, equivalently balance in
an `F_2` gain graph.  The terminology is compatible with Zaslavsky's biased
graphs, but the component-overlap graph and its connection to permanent
backbone switches are problem-specific.

The overlap construction is also the precise gluing structure that the
earlier proposed “rectangle holonomy complex” lacked: its cycles compare
different backbone fibres rather than reattaching walks already contained
in one canonically bipartite graph.

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_equality_backbone_coloring_glue_theorem.py
python audit_arbitrary_permanent_equality_backbone_coloring_glue_theorem.py
```

The primary verifier checks the component-offset equations over `F_2`, the
balanced and unbalanced overlap cycles, and the one-switch two-state
obstruction.  The audit repeats the descent by independent parity
propagation.  These are fixed symbolic checks; the proof is (4)--(8).

## Boundary

```text
fixed-backbone bipartitions:              CANONICAL;
all-backbone bipartition:                 OVERLAP-BALANCE CRITERION;
two-state relative-parity mismatch:       EXCLUDES EQUALITY;
one-switch straddling condition:          EXCLUDES EQUALITY;
forced straddling switch:                 UNKNOWN;
global Krenn--Gu conjecture:              UNRESOLVED.
```
