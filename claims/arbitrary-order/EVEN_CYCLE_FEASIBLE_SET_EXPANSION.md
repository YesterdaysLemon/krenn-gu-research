# Even-cycle feasible-set expansion

## Statement

Let `F` be a vertex-disjoint union of even cycles and let `U` be a
matching of edges outside `F`. For `T subset U`, write `D_C(T)` for the
endpoints of `T` lying on a component cycle `C` of `F`.

The perfect matchings of `F union U` split disjointly according to their
singleton-edge set `T`. The number with singleton set exactly `T` is

```text
q_F(T) = product over cycles C of q_C(D_C(T)),
```

where:

```text
q_C(empty) = 2,

q_C(D) = 1
  if D is nonempty and consecutive vertices of D in cyclic order
  are separated by odd distances on C,

q_C(D) = 0 otherwise.
```

Equivalently, for nonempty `D`, its vertices must alternate between the
two bipartition classes of the even cycle in cyclic order.

Thus a feasible `T` has exactly

```text
2^(number of cycles untouched by T)
```

full-edge completions. In particular, a feasible `T` touching every cycle
has a unique completion.

## Proof

Fix `T`. Since `U` is a matching, using exactly the edges of `T` deletes
their endpoints from `F`. The remaining graph is a disjoint union over
the cycle components, so its perfect-matching count is the product of the
component counts.

If no vertex is deleted from an even cycle, its two alternating perfect
matchings are the only choices.

Otherwise, list the deleted vertices in cyclic order. Deleting them cuts
the cycle into paths. If two consecutive deleted vertices are at cyclic
distance `d`, the intervening path contains `d-1` vertices. That path has
a perfect matching exactly when `d-1` is even, or equivalently when `d`
is odd; in that case its perfect matching is unique. All remaining paths
are independent, proving the formula.

Every perfect matching of `F union U` has one well-defined intersection
with `U`, so summing these disjoint classes over `T subset U` gives all
perfect matchings exactly once.

## Weighted amplitude expansion

At any colouring that activates exactly the singleton-edge matching `U`,
the active graph is `F union U`. Its amplitude therefore has the exact
expansion

```text
sum over feasible T subset U
  product_(e in T) w_e
  product_(cycles touched by T) path_completion_C(T)
  product_(cycles untouched by T) (A_C + B_C).
```

Here `A_C` and `B_C` are the two alternating cycle monomials at that
colouring. Every touched-cycle path completion is a single nonzero
monomial.

This one formula explains three existing obstruction layers:

- a minimal feasible `T` touching every cycle gives a one-term forbidden
  amplitude;
- a new feasible `T` leaving one cycle untouched gives a nonzero monomial
  times one cycle binomial, the one-extra-cycle mechanism;
- comparing two exactly activated sets that differ by one singleton edge
  transports the common completion sums, giving the matching/factor-fork
  mechanisms.

An independent bitmask recursion exhaustively checks every deleted-vertex
set on `C4,C6,...,C14`:

```text
python claims/arbitrary-order/verify_even_cycle_feasible_set_expansion.py
```

It must write
`tmp/even_cycle_feasible_set_expansion_verified.json` with
`"verified": true`. The arbitrary disjoint-union statement then follows
by multiplication over components, exactly as in the proof.

## Boundary

The lemma is an exact arbitrary-order expansion, but it does not by itself
prove that three edge-disjoint singleton perfect matchings contain a
sequence of feasible subsets whose amplitude equations are inconsistent.
That remaining statement is now a purely combinatorial/algebraic target:
force an incompatible family of cycle-binomial choices from the
feasible-set poset.
