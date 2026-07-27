# The `P_5` restriction image has no quartic equations

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

> No nonzero homogeneous quartic polynomial vanishes on `X`.

Combined with the preceding quadratic and cubic theorems, the defining
ideal of `X` has no nonzero element of degree at most four.  A global
covariant separator must have degree at least five.

## Quartic representation blocks

Only four partitions of four fit in three target dimensions:

```text
name  partition  Specht dimension  Schur dimension on C^3
T     [4]                 1                 15
S     [3,1]               3                 15
D     [2,2]               2                  6
R     [2,1,1]             3                  3.
```

Schur--Weyl duality decomposes
`Sym^4((C^3) tensor power 5)` into modules indexed by five such
partitions.  The diagonal-`S_4` invariant multiplicity is computed by
the exact character formula.

There are:

```text
839 ordered module tuples with nonzero multiplicity,
 44 representatives up to permutation of the five tensor modes,
```

with multiplicities in

```text
1, 2, 3, 4, 5, 7, 10.
```

The complete Schur-dimension sum is

```text
148,897,035 = binomial(243 + 3, 4),
```

so the decomposition covers the entire quartic polynomial space.

## Exact multiplicity-rank calculation

As in the cubic proof, the pullback kernel on one isotypic component
has the form `K tensor U`, where `K` lies in the small diagonal
Specht-invariant multiplicity space.  It is enough to show that
contractions of four copies of `P_5` span that multiplicity space.

The verifier uses integer models of all four `S_4` representations:

- `S=[3,1]` is the standard sum-zero representation;
- `R=[2,1,1]` is its sign twist;
- `D=[2,2]` is the standard representation of the induced action on
  the three pair partitions of four points; and
- `T=[4]` is trivial.

It constructs the rational matrix units

```text
e_ij = (dim lambda / 24)
       sum_(g in S_4) rho_lambda(g inverse)[j,i] g
```

and contracts deterministic local covectors against four copies of
`P_5`.  A compiled subset dynamic program sums over four simultaneous
source permutations without enumerating the full quartic coordinate
space.

The replay checks exactly:

- all `S_4` representation products, characters, and matrix-unit
  relations;
- every dynamic-program state-layer cardinality;
- diagonal-`S_4` invariance of every multiplicity vector;
- the 839-module, 44-representative, and 148,897,035-dimension counts;
  and
- full modular row rank in every representative block.

Every block reaches its theoretical multiplicity, including all six
multiplicity-ten types.

The arithmetic is exact modulo five.  Since five does not divide the
matrix-unit denominator 24, every nonzero modular rank witnesses a
nonzero rational minor.  Mode symmetry of `P_5` carries the 44
representatives to all 839 ordered tuples.  Therefore the complete
quartic pullback is injective over `Q` and over `C`.

## Replay

On Linux, macOS, or WSL with a C++20 compiler:

```text
g++ -O3 -std=c++20 \
  verify_p5_no_quartic_restriction_equations.cpp \
  -o verify_p5_no_quartic_restriction_equations

./verify_p5_no_quartic_restriction_equations
```

The deterministic replay uses seed `20260727`, contains no
floating-point arithmetic, and normally completes in seconds.

## Boundary

This moves the first possible global covariant equation to degree five.
It does not prove that a degree-five equation exists or separates
`Delta_3`.  The degree-six scalar-invariant pullback is also known to be
injective, but non-invariant degree-five and higher modules and
higher-degree invariant relations remain possible.
