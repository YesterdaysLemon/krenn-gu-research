# The `P_5` restriction image has no quintic equations

## Status

This is an exact characteristic-zero theorem about the full local
restriction image of the order-five permanent tensor.  It does not
produce a restriction `P_5 -> Delta_3` and does not resolve the global
Krenn--Gu conjecture.

For

```text
X = {
  (A_1 tensor ... tensor A_5) P_5 :
  A_i : C^5 -> C^3
},
```

the theorem is:

> No nonzero homogeneous quintic polynomial vanishes on `X`.

Together with the quadratic, cubic, and quartic calculations, the
defining ideal of `X` has no nonzero element of degree at most five.
A global covariant separator must have degree at least six.

## Quintic representation blocks

The five partitions of five that fit in three target dimensions are:

```text
name  partition  Specht dimension  Schur dimension on C^3
T     [5]                 1                 21
U     [4,1]               4                 24
V     [3,2]               5                 15
X     [2,2,1]             5                  3
W     [3,1,1]             6                  6.
```

Schur--Weyl duality decomposes
`Sym^5((C^3) tensor power 5)` into modules indexed by five such
partitions.  Exact `S_5` character arithmetic gives

```text
2,955 ordered module tuples with nonzero multiplicity,
  115 representatives up to permutation of the five tensor modes,
```

with multiplicities from one through 61.  The complete Schur-dimension
sum is

```text
7,355,513,529 = binomial(243 + 4, 5),
```

so the decomposition covers the entire quintic polynomial space.

## Exact multiplicity-rank calculation

The verifier uses concrete models of all five `S_5` representations:

- `U=[4,1]` is the four-dimensional standard representation;
- `W=[3,1,1]` is its exterior square;
- `V=[3,2]` is the five-dimensional kernel of the vertex-incidence map
  on the ten unordered pairs of five points;
- `X=[2,2,1]` is the sign twist of `V`; and
- `T=[5]` is trivial.

It checks every representation product, character, character inner
product, and rational matrix-unit relation.  It then projects arbitrary
local covectors with

```text
e_ij = (dim lambda / 120)
       sum_(g in S_5) rho_lambda(g inverse)[j,i] g
```

and contracts five copies of `P_5`.

The contraction is evaluated by a subset dynamic program over five
simultaneous source permutations.  Its exact state-layer sizes are

```text
1, 3,125, 100,000, 100,000, 3,125, 1,
```

and its transition counts are

```text
3,125, 3,200,000, 24,300,000, 3,200,000, 3,125.
```

The verifier tests both an isolated nonzero permutation tuple and an
invalid zero tuple.  For efficiency it fixes four valid projected local
covectors and varies the fifth.  Every resulting vector is checked to
be diagonally `S_5`-invariant before exact row reduction.

All 115 representative blocks reach their theoretical multiplicity.
The largest block, `W W W W W`, reaches rank 61 in its
`6^5 = 7,776`-dimensional ambient Specht tensor product.  Mode symmetry
transports the representative results to all 2,955 ordered tuples.

The arithmetic is exact modulo seven.  Since seven does not divide the
matrix-unit denominator 120, every full modular rank contains a
nonzero rational minor.  Therefore the complete quintic pullback is
injective over `Q` and over `C`.

## Replay

On Linux, macOS, or WSL with a C++20 compiler:

```text
g++ -O3 -std=c++20 \
  verify_p5_no_quintic_restriction_equations.cpp \
  -o verify_p5_no_quintic_restriction_equations

./verify_p5_no_quintic_restriction_equations
```

The default command verifies all 115 representatives.  The deterministic
work can also be split into the disjoint first-three-dimension-product
ranges

```text
0--36, 37--64, 65--96, 97--144, 145--216
```

with `--min-first-three-product` and
`--max-first-three-product`.  The run uses seed `20260727` and contains
no floating-point arithmetic.

## Boundary

This rules out every degree-five covariant equation, including the
first layer where five-copy matching and Latin-square-style
factorizations could have appeared.  It does not rule out non-invariant
equations of degree six or higher, higher-degree scalar invariants,
Grassmannian incidence obstructions, or support-local Laurent
identities.

The separate degree-six calculation rules out all eleven scalar
`SL(3)^5` invariants as separators.  It does not analyze the full
degree-six covariant space.
