# Six permuted positive potentials lemma

## Status

This is an arbitrary-order symmetry corollary of the positive
optional-transition potential in
`THREE_COLOUR_DIAGONAL_MATCHING_BALANCE_THEOREM.md`.  It applies in the
same simultaneous balanced all-bridge, pairwise-disjoint exact-cubic
diagonal branch.  It strengthens the minimum-layer obstruction but does
not by itself exclude every order or prove the Krenn--Gu conjecture.

The symmetry lemma and its optional-diagonal sign table remain valid.
The older order-ten and order-twelve finite residual applications used an
incorrect physical-port orientation and are withdrawn.  Under the
corrected convention the base potential alone is already strictly
positive on every admissible physical port, yielding the arbitrary-order
exclusion in
`ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md`.

## Statement

Let a normal type be the fixed-point-free map

```text
f_i : {0,1,2} -> {0,1,2},
f_i(c) != c.
```

The base theorem associates to `f_i` the potential

```text
q_i(0) = 1 - 2 b2,
q_i(1) = 2 (b2 - b0),
q_i(2) = 2 (b0 + b1 - 1),
```

where the three bits encode the two choices of `f_i(c)`.

For any permutation `pi` of the three colours, define the relabelled
normal map by

```text
f_i^pi(pi(c)) = pi(f_i(c))
```

and pull the base potential back to the original colour names:

```text
q_i^pi(c) = q_(f_i^pi)(pi(c)).                         (1)
```

There are at most six such integer potentials.  For every `pi`:

1. each forced own-colour diagonal unit on an edge of `M_c` has endpoint
   potential sum zero;
2. every permitted optional off-diagonal unit on a diagonal edge has
   strictly positive endpoint potential sum;
3. the three monochromatic guaranteed matchings have total potential
   zero;
4. a minimum-potential nonmonochromatic guaranteed colouring has
   potential at most zero; and
5. no optional diagonal unit contributes to its coefficient.

Consequently, a witness must avoid a unique guaranteed perfect matching
simultaneously on the minimum layer of all six potentials.  For each
permutation separately, every non-singleton minimum coefficient factors
into even paths and zero-potential alternating diagonal/port cycle
binomials.

## Proof

Relabel every half-edge colour `c` as `pi(c)`.  A reciprocal normal
condition

```text
f_i(s)=r,  f_j(r)=s
```

becomes

```text
f_i^pi(pi(s))=pi(r),
f_j^pi(pi(r))=pi(s).
```

Likewise, an own-colour diagonal unit `(c,c)` becomes
`(pi(c),pi(c))`, and every balanced bridge-plane condition is simply
permuted.  The relabelled architecture therefore satisfies exactly the
hypotheses of the base potential theorem.

Apply that theorem after relabelling, then translate the local colours
back.  Equation (1) is precisely the translated potential.  Zero on
forced diagonal transitions, strict positivity on optional transitions,
and the minimum-layer replacement argument are all invariant under this
bijection.  This proves items 1--5.

The maximum-degree-two filtered-graph argument is also invariant under
colour relabelling, so the path/cycle factorization applies to every
permuted minimum layer.

## Positive potential cone

The six potentials can be combined.  If

```text
lambda_pi >= 0
```

for all permutations and at least one coefficient is positive, then

```text
Q_i(c) = sum_pi lambda_pi q_i^pi(c)                   (2)
```

is again zero on every forced own-colour diagonal transition and strictly
positive on every optional diagonal transition.  The minimum-layer
replacement proof therefore applies to every potential in this
six-generator cone, not just to its six displayed rays.

In particular, lexicographic refinements are valid.  Given an ordering
`pi_1,...,pi_6`, minimize `q^pi_1`, then `q^pi_2` among ties, and so on.
Because an architecture has finitely many guaranteed colourings, this
lexicographic order is realized by

```text
q^pi_1 + epsilon q^pi_2 + ... + epsilon^5 q^pi_6
```

for a sufficiently small positive rational `epsilon`.  Hence a witness
must have a non-singleton guaranteed fibre at every colouring exposed by
the entire positive cone, including every lexicographically exposed
minimum.

On the universal table of 24 `(normal type, local colour)` states, the
six integer potential columns are linearly independent.  In permutation
order their exact Gram matrix has diagonal 40 and off-diagonal 32:

```text
G = 8 I_6 + 32 J_6.                                   (3)
```

Thus the cone is genuinely six-dimensional.  The six-coordinate local
signature has 12 values, each shared by the two normal types that differ
only in the bit belonging to the chosen local colour.  This is the
expected unresolved bit on an own-colour diagonal transition.

## Order-ten consequence

The identity potential leaves 392 non-unique minimum-layer architectures
in the complete order-ten Kotzig/port census.  Each has one minimum
colouring with two guaranteed matchings on an alternating four-cycle.

Testing the five nonidentity potentials from (1) gives:

```text
identity residuals tested:                       392
residuals with a unique permuted minimum layer:  392
residuals surviving all six potentials:            0.
```

Every residual is exposed by at least four of the five nonidentity
permutations; 122 are exposed by all five.  In fact the two
transpositions

```text
(0,1,2) -> (0,2,1),
(0,1,2) -> (1,0,2)
```

already cover all 392 identity residuals.

Thus the full order-ten finite branch is excluded entirely within
minimum-potential guaranteed layers.  The independent maximal-support
singleton test remains a second, stronger-support confirmation but is
not needed for the order-ten conclusion.

## Verification boundary

The finite order-ten application is checked by:

```text
python analyze_ten_vertex_permuted_potential_survivors.py
python audit_ten_vertex_permuted_potential_survivors.py
```

The arbitrary-order lemma says that a witness must survive all six
minimum-layer rays and the full positive cone that they generate.  It
does not prove that some cone-exposed colouring always has a unique
matching, nor that the cycle binomials selected by different gradings are
globally inconsistent.
