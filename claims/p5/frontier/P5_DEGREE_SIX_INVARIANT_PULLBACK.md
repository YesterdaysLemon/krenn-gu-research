# Degree-six scalar invariants do not separate `P_5` from `Delta_3`

## Status

This is an exact negative result about one alternative proof strategy.
It is not a restriction `P_5 -> Delta_3`, an obstruction at higher
degree, or a solution of the global Krenn--Gu conjecture.

Let

```text
V = (C^3) tensor power 5
```

and let `I_6` be the space of homogeneous degree-six scalar polynomial
invariants on `V` under `SL(3)^5`.  Pull an invariant back along the
family of local restrictions of the order-five permanent tensor:

```text
Phi(f)(A_1,...,A_5)
  = f((A_1 tensor ... tensor A_5) P_5),

A_i : C^5 -> C^3.
```

The exact calculation proves:

> `dim_C(I_6) = 11`, and the pullback `Phi : I_6 -> C[A_1,...,A_5]`
> is injective.

Consequently no nonzero degree-six `SL(3)^5` scalar invariant vanishes on
every local restriction of `P_5`.  In particular, there is no separator
of this type that vanishes on the complete restriction image but is
nonzero at `Delta_3`.

## Why degree six is the first natural test

The determinant contraction at degree three uses one alternating
epsilon tensor in each of the five modes.  Swapping two of the three
tensor copies changes its sign by

```text
(-1)^5 = -1,
```

while a degree-three polynomial is symmetric in its three copies.
Therefore that contraction is identically zero.

At degree six, each local mode uses two epsilon tensors.  By
Schur--Weyl duality, the local multiplicity space is the `S_6` Specht
module of shape `(2,2,2)`, which has dimension five.  Scalar invariants
are the diagonal-`S_6` fixed vectors in its fifth tensor power.

`analyze_p5_degree_six_invariant_space.py` constructs the five standard
tableaux, the exact Young seminormal matrices for the adjacent
transpositions, and checks all Coxeter relations.  Its complete
character calculation satisfies

```text
sum_C |C| chi(C)^2 = 6!
```

and gives

```text
(1/6!) sum_C |C| chi(C)^5 = 11.
```

Thus the entire degree-six scalar-invariant space has dimension eleven.

## Exact basis witness modulo five

Partition the six tensor copies into two unordered triples.  There are
ten such local epsilon-pair contractions.  A five-tuple of local
partitions gives a degree-six scalar invariant.

The verifier fixes eleven explicit five-tuples.  It evaluates them on 32
deterministically generated generic tensors over `F_5`.  The first
eleven evaluation rows form a square minor with

```text
determinant = 1 mod 5.
```

Therefore the eleven integer-coefficient contractions are linearly
independent over `Q`.  Since the characteristic-zero invariant space has
dimension eleven, they form a basis of `I_6`.

## Exact pullback witness modulo five

The same eleven invariants are evaluated on 48 tensors of the form

```text
(A_1 tensor ... tensor A_5) P_5
```

for deterministic `3 x 5` matrices over `F_5`.  The verifier constructs
each restriction directly from all 120 source permutations.  Evaluation
rows

```text
0,1,2,3,4,5,6,8,9,10,11
```

form an `11 x 11` minor with

```text
determinant = 2 mod 5.
```

Hence the eleven pulled-back integer polynomials are linearly
independent over `Q`, and `Phi` is injective.

All contractions use pinned explicit paths.  Inputs are reduced to
`0,...,4`, and the conservative absolute intermediate bound

```text
3^30 * 4^6 < 2^63
```

makes the signed 64-bit calculation exact before reduction modulo five.
No floating-point value is used by the verifier.

## Replay

Run:

```text
python claims/p5/frontier/analyze_p5_degree_six_invariant_space.py
python claims/p5/frontier/verify_p5_degree_six_invariant_pullback.py
```

The first command certifies the 11-dimensional characteristic-zero
search space.  The second command certifies an explicit basis and the
full-rank pullback minor modulo five.

`probe_p5_degree_six_invariants.py` is the earlier numerical discovery
tool.  It is not part of the exact proof.

## Boundary

This result excludes only a polynomial that is simultaneously:

- homogeneous of degree six;
- a scalar invariant under `SL(3)^5`; and
- identically zero on all local restrictions of `P_5`.

It says nothing about non-invariant equations, higher-degree invariants,
relations among invariant values at degree twelve or above,
Grassmannian incidence obstructions, or sparse Laurent-resultant
identities.  Those remain possible routes.
