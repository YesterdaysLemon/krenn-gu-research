# Partial minimal singleton-circuit dichotomy

## Theorem

Let the full factor `F` be a vertex-disjoint union of even cycles, and let
`S0,S1,S2` be pairwise edge-disjoint diagonal singleton perfect matchings.
Fix a singleton colour `c` and a nonempty proper subset `T` of `Sc`.
Assume that `T` is positive-minimal feasible.

Let `J` be the full cycles touched by endpoints of `T`, and let `K` be the
untouched full cycles.  Properly 2-colour the other two singleton factors,
then recolour all endpoints of `T` to `c`, exactly as in the minimal
singleton-circuit rectangle theorem.  At that target colouring, one of the
following must hold:

1. a full-cycle binomial on a cycle in `K` vanishes; or
2. on every cycle in `J`, the endpoints of `T` are exactly two adjacent
   vertices, and after contracting the cycles in `J`, the edges of `T`
   form one connected 2-regular multigraph.

In particular:

- if `K` consists of one cycle and alternative 2 fails, that untouched
  cycle relation is forced to have value `-1`;
- if `J` consists of one cycle, alternative 2 is impossible because it
  would require a singleton edge joining the adjacent ports, which is the
  full edge between them;
- for a full factor with exactly two cycles, every positive-minimal
  feasible `T` confined to one cycle forces the binomial on the other
  cycle to vanish.

## Exact target factorization

The exact-activation cube has no nonempty feasible singleton subset at
any proper corner.  At the target corner, positive minimality says that
the only feasible singleton subsets are the empty set and `T`.

On each touched cycle the endpoints of `T` leave one unique path
completion.  On each untouched cycle both alternating completions remain.
Writing `P_C=A_C+B_C` for a full-cycle binomial and `m_T` for the supported
nonzero monomial made from `T` and all touched-cycle path completions, the
target amplitude factors exactly as

```text
product_(C in K) P_C
  * (product_(C in J) P_C + m_T).                       (1)
```

The target is nonmonochromatic because `T` is proper, so (1) must vanish.

## Reduction to the port exception

Suppose no `P_C` with `C in K` vanishes.  Equation (1) then gives

```text
product_(C in J) P_C = -m_T != 0.
```

Every target binomial on a touched cycle is therefore nonzero.  Fix one
touched cycle and leave all other cycles at their target colours.  Every
proper local corner is a proper corner of the exact-activation cube, hence
has only the full-factor perfect matchings and zero amplitude.  All the
other target cycle binomials are nonzero, so the chosen local binomial
vanishes at every proper local corner.

The edge-local Mobius rectangle argument from the minimal
singleton-circuit rectangle theorem now applies without change.  The
deleted vertices on each touched cycle must be exactly one adjacent pair.
Contracting the touched cycles gives a 2-regular multigraph.  If it were
disconnected, the edges in one component would be a smaller nonempty
feasible subset of `T`, contradicting positive minimality.  It is
therefore connected.

When only one cycle is touched, connected 2-regularity would be a loop.
Its singleton edge would join the two adjacent ports, but that pair is
already a full edge and singleton factors are edge-disjoint from the full
factor.  Hence this case cannot occur.

## Consequence for computation

When exactly one full cycle is untouched and the port exception fails,
the theorem produces a mandatory ordinary Laurent binomial relation in
the original supported full-edge entries.  Relations obtained from
different singleton colours, minimal sets, and proper base colourings can
therefore be combined with the existing exact signed-lattice machinery.
An integer dependency with odd coefficient sum is a contradiction.

This theorem still leaves genuine port cycles and, with two or more
untouched cycles, a disjunction among their vanishing binomials.

## Independent audit

The combinatorial portions are replayed by:

```text
python verify_partial_minimal_singleton_circuit_dichotomy.py
```

The verifier exhausts every subset of a matching on unions of two to six
even cycles with total order at most 14, checks positive minimality,
completion counts, touched/untouched sets, and the connected port-cycle
exception.  It also checks the exact factorization counts

```text
full-only: 2^(|J|+|K|)
T-completions: 2^|K|.
```

It must write
`tmp/partial_minimal_singleton_circuit_dichotomy_verified.json` with
`"verified": true`.
