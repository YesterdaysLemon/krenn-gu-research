# Full-only / one-extra cycle-factor lemma

## Statement

Fix an equality-architecture support whose full 2-factor is a disjoint
union of even cycles. All selected edge entries are assumed nonzero.

At a colouring `x`, suppose the active perfect matchings are exactly the
alternating choices on the full cycles. Write the two alternating
monomials of cycle `i` as `A_i(x)` and `B_i(x)`. Then

```text
T(x) = product_i (A_i(x) + B_i(x)).
```

If `x` is forbidden, at least one cycle binomial
`A_i(x) + B_i(x)` must vanish.

Now fix one such cycle relation `r`. Suppose another forbidden colouring
`y` has exactly the full-only matchings plus one additional perfect
matching `M`, and one full-cycle factor at `y` is the same Laurent
binomial relation `r`. Then `r` cannot vanish: otherwise the full-only
product vanishes and

```text
T(y) = monomial(M,y) != 0,
```

contradicting that `y` is forbidden.

Consequently, a full-only forbidden equation is impossible whenever
every distinct cycle relation in its factorization is ruled out by a
forbidden one-extra equation.

## Proof

The full-only perfect matchings independently choose one of the two
alternating matchings on each even cycle. Distributivity gives the stated
product factorization. The coefficient ring is a Laurent polynomial
domain in supported nonzero edge entries, so a zero product has a zero
cycle factor.

At a one-extra colouring, cancelling the named cycle factor annihilates
the entire full-only product. The only remaining term is the monomial of
the additional active perfect matching. Every factor of that monomial is
a selected nonzero support entry, so the monomial cannot vanish. This
contradicts the required zero amplitude.

Combining the positive full-only clause with the negative one-extra
units gives an explicit Boolean contradiction. For two full cycles it is
the three-clause core

```text
r1 or r2
not r1
not r2
```

## Machine replay

`find_fourteen_vertex_one_extra_cycle_core.py` searches one fixed support
for this motif. `verify_fourteen_vertex_one_extra_cycle_core.py` is an
independent implementation: it reconstructs every skeleton perfect
matching, checks that all three recorded colourings are non-monochromatic,
recomputes their exact active matching sets and Laurent relations, and
checks the final Boolean contradiction.

Verified instances currently exist on tested residual supports in both
the order-14 `C4+C10` and `C6+C8` families. Activation-mask transport is
independently reconstructed by
`verify_fourteen_vertex_two_even_cycle_one_extra_cycle_augmentation.py`.

## Boundary

The lemma is general, but existence of the required three colourings has
not been proved for every support. The complete `C4+C10`, `C6+C8`, and
`C4+C4+C6` families and the global Krenn--Gu conjecture remain open.
