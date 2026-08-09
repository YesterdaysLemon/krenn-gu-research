# Order-14 `C3+C3+C8` equality-family certificate

## Theorem

There is no order-14, three-colour equality-architecture witness whose
full-block 2-factor has cycle type `C3+C3+C8`.

This is a complete finite theorem for that factor type.  It is not a
proof of the remaining order-14 factor types or of the global Krenn--Gu
conjecture.

## Exact singleton-factor exhaustion

Fix the labelled full factor

```text
C3 = (0,1,2)
C3 = (3,4,5)
C8 = (6,7,8,9,10,11,12,13).
```

A singleton colour class must be a perfect matching in the complement of
this factor.  There are exactly 44,250 such matchings.

For each matching `S`, the verifier independently enumerates every perfect
matching of `F union S` and records the exact subset of `S` that it uses.
An exact subset-zeta transform then gives the number of active perfect
matchings for each of the 128 possible activation subsets of `S`.

The result is:

```text
eligible singleton perfect matchings             44,250
with a forbidden one-term activation              44,064
individually one-term-free factors                    186
```

The minimum one-term activation sizes among the 44,064 eliminated factors
have the exact histogram

```text
size 2     40,032
size 3      3,312
size 5        720
```

## The common disconnected split

The 186 surviving factors are exactly the Cartesian product of:

- the 6 bijective perfect matchings between the two triangles; and
- the 31 perfect matchings inside `K8-C8`.

Thus every surviving factor has component-edge profile

```text
between the two C3 components       3
from the first C3 to C8             0
from the second C3 to C8            0
inside C8                           4
```

In particular, every individually admissible singleton factor preserves
the same nontrivial vertex split

```text
L = {0,1,2,3,4,5}
R = {6,7,8,9,10,11,12,13}.
```

The full factor also preserves this split.  Therefore any support assembled
from three admissible singleton colour classes is disconnected as
`G_L disjoint-union G_R`.  Pairwise disjointness of the singleton factors
can only remove candidates; it cannot reconnect the two sides.

## Disconnected-tensor contradiction

For a graph with no edge between `L` and `R`, every perfect matching is the
union of one perfect matching on each component.  Hence every coefficient
of the matching tensor factors:

```text
T(a_L,a_R) = T_L(a_L) T_R(a_R).
```

For each colour `c`, the required monochromatic coefficient is

```text
T_L(c^6) T_R(c^8) = 1.
```

Both factors are therefore nonzero.  Choose two distinct colours `c` and
`d`.  The nonmonochromatic coefficient obtained by colouring all of `L`
with `c` and all of `R` with `d` equals

```text
T_L(c^6) T_R(d^8),
```

which is a product of two nonzero complex numbers.  The Krenn--Gu target
requires this coefficient to be zero, a contradiction.

This obstruction is purely algebraic and does not depend on signs,
genericity, numerical tolerances, or a lattice calculation.

## Independent replay

Run:

```text
python claims/finite/n14/verify_fourteen_vertex_c3_c3_c8_family.py
```

The verifier uses a fresh smallest-vertex matching recursion, reconstructs
all 44,250 factors, independently computes all activation counts, checks
that the 186 survivors are exactly the `6 x 31` disconnected product
family, and records the factorization contradiction.

The final audit is

```text
tmp/fourteen_vertex_c3_c3_c8_family_verified.json
```

and contains:

```json
{
  "verified": true,
  "status": "all_c3_c3_c8_equality_supports_closed"
}
```
