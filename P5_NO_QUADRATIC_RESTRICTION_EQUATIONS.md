# The `P_5` restriction image has no quadratic equations

## Status

This is an exact negative result about low-degree algebraic separators.
It is not a restriction `P_5 -> Delta_3` and does not resolve the global
Krenn--Gu conjecture.

Let

```text
P_5 in (C^5) tensor power 5
```

be the order-five permanent tensor, and let `X` be its full local
restriction image in `(C^3) tensor power 5`:

```text
X = {
  (A_1 tensor ... tensor A_5) P_5 :
  A_i : C^5 -> C^3
}.
```

The exact result is:

> No nonzero homogeneous quadratic polynomial vanishes on `X`.

Thus no linear or quadratic polynomial can separate `Delta_3` from
`X`.  Any covariant equation strategy must start in degree at least
three.

## Multiplicity-free quadratic decomposition

Put `W_i = C^3`.  The degree-two polynomial representation decomposes
under `GL(W_1) x ... x GL(W_5)` as

```text
Sym^2(W_1 tensor ... tensor W_5)
  =
  direct sum over |S| even of
    (tensor over i in S exterior^2 W_i)
    tensor
    (tensor over i not in S Sym^2 W_i).
```

There are

```text
binomial(5,0) + binomial(5,2) + binomial(5,4) = 16
```

summands.  Each is irreducible and occurs once.  Their dimensions sum
to

```text
6^5 + binomial(5,2) 3^2 6^3
    + binomial(5,4) 3^4 6
  = 29,646
  = dimension Sym^2(C^243).
```

The pullback of quadratic polynomials along the restriction
parametrization is equivariant.  Its kernel is therefore a direct sum
of some of these sixteen modules.  It is enough to prove that the
pullback is nonzero on every module.

## One isolated coefficient per module

Write

```text
P_5 = sum over sigma in S_5
        e_sigma(0) tensor ... tensor e_sigma(4).
```

For an even subset `S` of the five modes, project `P_5 tensor P_5`
antisymmetrically in the modes of `S` and symmetrically in the other
modes.

- If `S` is empty, the pair `(identity, identity)` gives a coefficient
  equal to one.
- If `|S|=2`, pair the identity with the transposition on `S`.
  The union of those two permutation matchings has only those two
  ordered decompositions, and the two exterior signs multiply to
  `+1`.  The isolated coefficient is two.
- If `|S|=4`, pair the identity with a four-cycle on `S`, fixing the
  fifth point.  The alternating union is one cycle, so again only the
  two ordered permutation pairs contribute.  Four exterior signs
  multiply to `+1`, and the coefficient is two.

Every one of the sixteen projections is nonzero.  Equivariance and
irreducibility make the pullback injective on each multiplicity-one
summand, hence on the entire quadratic space.

## Replay

Run:

```text
python verify_p5_no_quadratic_restriction_equations.py
```

The verifier enumerates all `120^2` ordered pairs of source
permutations for each of the sixteen modules.  It checks the isolated
coefficient, the complete dimension count, and the even-parity module
count exactly.

## Boundary

The degree-three and higher covariant spaces can have nontrivial
multiplicity spaces, so the multiplicity-one argument no longer
settles them.  The degree-six scalar-invariant module is treated
separately in `P5_DEGREE_SIX_INVARIANT_PULLBACK.md`; its pullback is
also injective.  Non-invariant modules of degree at least three and
higher-degree invariant relations remain possible.
