# The `P_5` restriction image has no cubic equations

## Status

This is an exact characteristic-zero theorem about the full local
restriction image of the order-five permanent tensor.  It proves that a
global covariant separator cannot have degree three.  It does not
produce a restriction `P_5 -> Delta_3` and does not resolve the global
Krenn--Gu conjecture.

Let

```text
X = {
  (A_1 tensor ... tensor A_5) P_5 :
  A_i : C^5 -> C^3
}
```

inside `(C^3) tensor power 5`.  The theorem is:

> No nonzero homogeneous cubic polynomial vanishes on `X`.

Together with the quadratic theorem, the defining ideal of the
restriction image has no nonzero element of degree at most three.

## Cubic Schur--Weyl decomposition

The three irreducible representations of `S_3` are:

```text
T = [3]       trivial,   dimension 1
A = [1,1,1]   sign,      dimension 1
V = [2,1]     standard,  dimension 2.
```

For `W_i = C^3`, Schur--Weyl duality gives

```text
Sym^3(W_1 tensor ... tensor W_5)

  = direct sum over lambda_1,...,lambda_5 of

    ([lambda_1] tensor ... tensor [lambda_5])^(S_3)
      tensor
    (S_lambda_1 W_1 tensor ... tensor S_lambda_5 W_5).
```

The multiplicity is the dimension of the displayed diagonal-`S_3`
fixed space.  Exact character arithmetic finds 147 ordered module
tuples with nonzero multiplicity.  Mode permutation symmetry groups
them into thirteen type-count representatives.  The possible
multiplicities are one, three, and five.

Using

```text
dim S_[3](C^3)     = 10,
dim S_[1,1,1](C^3) = 1,
dim S_[2,1](C^3)   = 8,
```

the complete decomposition has dimension

```text
2,421,090 = binomial(243 + 2, 3),
```

the dimension of the full cubic polynomial space.

## What the pullback must span

Fix one ordered partition tuple and write its multiplicity space as
`M`.  The corresponding target module is

```text
M tensor U,

U = S_lambda_1(C^3) tensor ... tensor S_lambda_5(C^3).
```

The local restriction pullback is `GL(3)^5`-equivariant.  Since `U` is
irreducible, the kernel on this isotypic component has the form

```text
K tensor U
```

for a subspace `K` of `M`.  The component of
`P_5 tensor P_5 tensor P_5` determines a coefficient span
`R subset M`; the pullback is injective on the component exactly when
`R = M`.

Thus multiplicities, rather than the multi-million-dimensional cubic
space, are the only ranks that need to be checked.

## Exact rank witnesses modulo five

The verifier realizes `T`, `A`, and `V` over the integers and constructs
the rational group-algebra matrix units

```text
e_ij = (dim lambda / 6)
       sum_(g in S_3) rho_lambda(g inverse)[j,i] g.
```

For deterministic local covectors `q`, the family `q e_0a` fixes one
Schur functional while exposing the Specht index `a`.  Contracting five
such families with three copies of `P_5` gives an exact vector in `M`.
The contraction is evaluated by a subset dynamic program over three
simultaneous source permutations.

All arithmetic is reduced modulo five.  The verifier checks:

- the complete `S_3` representation and matrix-unit relations;
- compatibility of the copy-permutation action;
- a directly isolated three-permutation dynamic-program witness;
- diagonal-`S_3` invariance of every sampled multiplicity vector;
- the 147-module and `2,421,090`-dimension counts; and
- a nonzero full-rank minor for each of the thirteen type
  representatives.

Every representative reaches its full characteristic-zero multiplicity:

```text
multiplicity 1 -> rank 1
multiplicity 3 -> rank 3
multiplicity 5 -> rank 5.
```

The matrix units have only powers of six in their denominators, and
five does not divide six.  A nonzero minor modulo five therefore proves
that the corresponding rational minor is nonzero.  Mode symmetry of
`P_5` carries the thirteen representatives to all 147 ordered tuples.
Hence `R=M` in every cubic isotypic component, proving injectivity over
`Q` and therefore over `C`.

## Replay

Run:

```text
python verify_p5_no_cubic_restriction_equations.py
```

The replay uses deterministic seed `20260727` and normally completes in
well under one minute.

## Boundary

The full quartic calculation is completed in
`P5_NO_QUARTIC_RESTRICTION_EQUATIONS.md`, which also proves an injective
pullback.  Thus a global covariant search begins in degree five.  The
separately certified degree-six scalar-invariant pullback is also
injective, but non-invariant modules at degree five and above and
higher-degree invariant relations remain possible.
