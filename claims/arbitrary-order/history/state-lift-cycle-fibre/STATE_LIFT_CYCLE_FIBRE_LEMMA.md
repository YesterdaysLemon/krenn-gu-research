# Withdrawn state-lift cycle-fibre proposal

## Status

**WITHDRAWN.**  This file is retained only as an audit trail and must not
be used as a theorem or certificate.

The construction confused the three `(vertex,target)` killer tasks with
the inherited physical colour states at that vertex.  Pairing target
tasks `(c,r)` produces physical half-colours `(r,c)`, and the normal map
`c -> f_v(c)` need not be a permutation.  Consequently the physical
port units do not define a fixed-point-free involution on
`V x {0,1,2}`, and the asserted 2-regular lifted cycle cover need not
exist.

The exact correction is in
`RECIPROCAL_PORT_ORIENTATION_CORRECTION.md`.  It leads instead to the
strictly positive physical-port table and the valid arbitrary-order
exclusion in
`ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md`.

Everything below this paragraph describes the withdrawn construction.

## Lifted state graph

Let `V` be the physical vertex set and let

```text
Omega = V x {0,1,2}
```

be the set of vertex-colour states.

The distinguished diagonal matching `M_c` defines a fixed-point-free
involution

```text
delta(v,c) = (M_c(v),c).
```

The reciprocal cubic port graph uses every vertex-colour stub exactly
once, so it defines another fixed-point-free involution

```text
kappa(v,c) = (w,d)
```

when the port edge between `v` and `w` has half-colours `(c,d)`.

Let `Lambda` be the graph on `Omega` whose edges are the `delta` and
`kappa` pairs.  Every state has one incident edge of each kind.  Therefore
`Lambda` is a vertex-disjoint union of even cycles alternating between
diagonal and port edges.

## Exact fibre theorem

A physical vertex colouring

```text
a : V -> {0,1,2}
```

selects the transversal

```text
S_a = {(v,a(v)) : v in V}.
```

The forced units compatible with `a` are exactly the edges of the induced
state graph `Lambda[S_a]`.  Consequently:

1. guaranteed perfect matchings inducing `a` are in bijection with
   perfect matchings of `Lambda[S_a]`;
2. every component of `Lambda[S_a]` is a path or a whole component cycle
   of `Lambda`;
3. if `a` is feasible, each path component has one perfect matching and
   each cycle component has two; and
4. the exact guaranteed-monomial multiplicity is

```text
2 ^ r(a),
```

where `r(a)` is the number of components of `Lambda` contained entirely
in `S_a`.

In particular, a feasible guaranteed colouring is a singleton exactly
when it does not contain an entire lifted cycle.

A lifted cycle that contains two states of the same physical vertex can
never be contained in a transversal.  Only lifted cycles whose projection
to `V` is injective can produce a cancellation fibre.  Call these
*transversal lifted cycles*.

## Proof

At a selected state `(v,c)`, the forced diagonal unit compatible with the
physical colour is the `M_c` edge, represented by `delta`.  The forced
port unit compatible with the same colour is the unique port using stub
`(v,c)`, represented by `kappa`.  No other forced unit is compatible.
Thus the compatible forced graph is precisely `Lambda[S_a]`.

An induced subgraph of a disjoint union of cycles is a disjoint union of
paths unless it contains every vertex of a component, in which case that
component remains a cycle.  A feasible path component must have even
order and then has a unique perfect matching.  An even cycle has exactly
two.  Multiplication over components proves the formula.

## Interaction with the full potential cone

Let `p(v,c)` be any local potential neutral on every forced diagonal
transition.  For every lifted component `C`,

```text
sum_(x in C) p(x) = 0,
```

because the diagonal edges of `C` partition its states into pairs with
opposite total potential.

For any Boolean extreme potential from
`FULL_ADMISSIBLE_POTENTIAL_CONE_LEMMA.md`, all local values are `+5` or
`-5`.  Hence every lifted cycle contains equally many positive and
negative states.

Let `g` be the minimum length of a transversal lifted cycle, with
`g=infinity` if none exists.  A feasible colouring containing fewer than
`g/2` positive states under a Boolean extreme potential cannot contain a
whole transversal lifted cycle.  It is therefore a guaranteed singleton.
This gives a simple sufficient condition for an extreme-minimum
contradiction.

The condition is not necessary.  In the 395 hard order-twelve
architectures, the minimum transversal lifted-cycle length is four.
Only seven architectures have an extreme minimum with fewer than two
positive states, while the complete cone excludes all 395.  The remaining
arbitrary-order task is therefore a cycle-avoidance statement at the
minimum positive-state count, not merely a lifted-girth bound.

## Finite regression verification

Run

```text
python verify_state_lift_cycle_fibres.py
```

On all 395 original-six-ray order-twelve residuals, the verifier rebuilds
the 36-state lifted graph, checks the alternating `D/K` degree-two
condition, and compares the formula `2^r` with the exact matching count
for every one of 130,581 feasible colouring fibres.  It also reconstructs
the transversal lifted girth and the seven cases covered by the simple
positive-state bound.  The output is

```text
tmp/state_lift_cycle_fibres_verified.json
```

## Boundary

The construction requires the pairwise-disjoint exact-cubic diagonal
normal form and the complete reciprocal port cover.  It does not apply
unchanged when selected monochromatic matchings overlap, when diagonal
support has higher degree, or before the simultaneous balanced
all-bridge reduction.
