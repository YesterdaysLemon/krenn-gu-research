# Support-four `P_5` contraction restriction

## Status

This is an exact positive restriction over `C`.  It marks the sharp
boundary of the support-at-most-three contraction obstruction:

```text
a support-four contraction of P_5 can restrict to Delta_3. (1)
```

It is not a restriction of `P_5` itself to `Delta_3`, and it is not a
counterexample to the Krenn--Gu conjecture.

## Canonical contraction

Let

```text
P_5 = sum_(sigma in S_5)
        e_(sigma(0)) tensor ... tensor e_(sigma(4)).
```

Contract its first mode by

```text
z = (1,1,1,1,0).
```

The resulting four-tensor `Q` has coefficient one on a tuple of four
distinct source coordinates exactly when its missing coordinate is in
`{0,1,2,3}`.  All other coefficients vanish.  Its quartic polynomial
is, up to the common polarization scalar,

```text
x_4 (x_1 x_2 x_3 + x_0 x_2 x_3
     + x_0 x_1 x_3 + x_0 x_1 x_2).                    (2)
```

## Integer local maps

For the four remaining modes, take the following source-by-target
matrices:

```text
A_0 =
[ 0  0  1]
[ 1  0  0]
[ 0  1  0]
[-1 -1  0]
[ 0  0 -1]

A_1 =
[ 1  1 -2]
[-2  1  1]
[ 1 -2  1]
[ 1  1  1]
[ 1  1  1]

A_2 =
[ 0  0  1]
[ 1  0  0]
[ 0  1  0]
[ 0 -1 -1]
[-1  0  0]

A_3 =
[-1 -1  1]
[ 1 -1 -1]
[-1  1 -1]
[-1  1 -1]
[ 0 -2  0].
```

Each matrix has column rank three.  Direct expansion of the 81 target
coefficients gives

```text
(A_0 tensor A_1 tensor A_2 tensor A_3) Q
  = 12 Delta_3.                                        (3)
```

Thus rescaling any one matrix by `1/12` gives a restriction to
`Delta_3`, and the ordinary subrank of `Q` is at least three.

Every contraction by a vector with exactly four nonzero coordinates is
equivalent to this one.  After permuting source coordinates, write the
vector as `(z_0,z_1,z_2,z_3,0)`.  In (2), scaling `x_i` by `z_i` for
`i=0,1,2,3` makes all four cubic coefficients equal to the same nonzero
product; a final scalar removes that product.  Therefore (1) holds for
every support-four contraction.

## A two-parameter family behind the integer point

The integer matrices are the specialization

```text
u=0, v=0, w=-1
```

of a family satisfying

```text
u v w - u v - u w - u - v w - v - w - 1 = 0.          (4)
```

For generic points of (4), the same construction pulls `Q` back to

```text
-12 (u+v+w) Delta_3.
```

The integer point is sufficient for the theorem; the family explains
why unconstrained numerical optimization found bounded, well-conditioned
solutions rather than the divergent border behaviour seen in the
support-three case.

## Verification

Run:

```text
python claims/arbitrary-order/verify_support_four_p5_contraction_restriction.py
python claims/arbitrary-order/audit_support_four_p5_contraction_restriction.py
```

The primary verifier reconstructs all `5!` source terms and all
`3^4=81` target coefficients over the integers, checks that precisely
the three diagonal coefficients equal 12, and symbolically verifies the
family identity (4).  The independent audit rebuilds the contraction
from the missing-coordinate rule and checks the integer maps over
`F_5` and `F_7`.

## Boundary

The support-at-most-three theorem remains valid and sharp.  What fails
is the proposed extension to support four.  In particular, contraction
arguments alone cannot force every row of a hypothetical
`P_5 -> Delta_3` local map to be a coordinate row.  The remaining exact
condition is still that the span of every pair of its five row
covectors contains a target coordinate covector; (3) shows why a
stronger conclusion cannot be obtained merely by allowing one more
source coordinate in the contraction.

The later simultaneous-pencil reduction sharpens this boundary.  A
normalized `q4_211` solution would require the same four maps to
diagonalize a three-dimensional space of contractions, whereas the
off-diagonal contraction matrix of every point in the family above has
rank four and only a one-dimensional kernel.  Thus no point of this
positive family lifts to `q4_211`; see
[`P5_Q4_211_SIMULTANEOUS_PENCIL_REDUCTION.md`](../p5/frontier/P5_Q4_211_SIMULTANEOUS_PENCIL_REDUCTION.md).
