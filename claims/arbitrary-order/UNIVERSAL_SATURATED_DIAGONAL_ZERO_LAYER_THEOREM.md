# Universal saturated-diagonal zero-layer theorem

## Status

This is an arbitrary-order reduction for the complete simultaneous
three-colour balanced all-bridge branch.  It does not assume pairwise
disjoint selected matchings or a support-degree bound.

It proves that every hypothetical witness in this branch has a
nonmonochromatic minimum-potential coefficient supported entirely on
saturated monochromatic diagonal units.  That coefficient contains a
nonzero perfect-matching monomial and must cancel with at least one other
such monomial.  This is a strict reduction, not yet a contradiction and
not a proof of the global Krenn--Gu conjecture.

## Universal potential

Encode a normal type by

```text
b0 = 0 for f(0)=1,  b0 = 1 for f(0)=2,
b1 = 0 for f(1)=0,  b1 = 1 for f(1)=2,
b2 = 0 for f(2)=0,  b2 = 1 for f(2)=1.
```

Let `q^pi` be the six colour-permuted potentials from
`SIX_PERMUTED_POTENTIALS_LEMMA.md`, and define

```text
Q = sum_pi q^pi.
```

At a vertex of type `(b0,b1,b2)`, division by ten gives the simple
formula

```text
Q(0)/10 = 1 - b1 - b2,
Q(1)/10 = b2 - b0,
Q(2)/10 = b0 + b1 - 1.                              (1)
```

For an oriented physical matrix unit `(r,s)` between endpoint types
`f,g`, its edge potential is

```text
Q_f(r) + Q_g(s).                                     (2)
```

The complete balanced-bridge condition permits `(r,s)` exactly when, for
each target `c`,

```text
(r,s)=(c,c), or r=f(c), or s=g(c).                   (3)
```

Direct enumeration of all eight endpoint types, all 64 ordered type
pairs, and all nine matrix positions gives 180 permitted oriented units.
Stronger than merely being nonnegative after summation, every one of the
six summands `q^pi` is separately nonnegative on every permitted unit.
Each ray has histogram

```text
ray potential 0: 56
ray potential 1: 24
ray potential 2: 60
ray potential 3: 24
ray potential 4: 16.
```

The exact histogram for their sum is

```text
edge potential  0: 48
edge potential 10: 96
edge potential 20: 36.                               (4)
```

In particular every permitted unit is nonnegative.  Equality in (2)
holds exactly when

```text
r=s=c
```

and the endpoint types flip the two bits other than `bc`.  These are
precisely the 16 saturated oriented colour-`c` diagonal transitions for
each of the three colours.  No bichromatic unit has zero potential.

## Zero-layer matching

For each colour `c`, choose one nonzero monochromatic perfect-matching
monomial `M_c` from the required all-`c` coefficient.  The diagonal
matching-balance theorem says every edge of `M_c` is saturated for colour
`c`; hence all its units have potential zero.

Regard the selected units as a monochromatically edge-coloured
multigraph, retaining distinct coloured copies when selected matchings
share a physical vertex pair.  It has three differently coloured
monochromatic perfect matchings.  Since `n>4`, Bogdanov's theorem,
reported as Theorem 1.7 in Chandran--Gajjala--Illickan, supplies a
nonmonochromatic perfect matching `F`.

Let `chi` be the vertex colouring induced by `F`.  It is
nonmonochromatic and

```text
sum_v Q_v(chi(v)) = 0.                               (5)
```

Every supported perfect-matching monomial inducing `chi` partitions the
same vertex states, so its total edge potential is also zero.  By (4),
every unit in such a monomial must itself have zero potential.  Therefore
the entire coefficient of `chi` lies in the saturated monochromatic
diagonal layer.

The matching `F` contributes a nonzero monomial, while the Krenn--Gu
target requires the coefficient of `chi` to vanish.  Consequently:

1. there is at least one additional saturated-diagonal perfect-matching
   monomial inducing `chi`;
2. the zero-layer monomials cancel algebraically; and
3. the symmetric difference of `F` with another contributing matching
   contains a monochromatic alternating even cycle.

Equivalently, if `V_c=chi^{-1}(c)` and `Z^c` is the colour-`c`
saturated-diagonal matrix, the coefficient factors as

```text
product_c haf(Z^c[V_c]) = 0,                         (6)
```

although `F` supplies a nonzero monomial to every nonempty factor.

## Consequences

The pairwise-disjoint exact-degree-six theorem is the special case in
which the properly three-edge-coloured diagonal graph makes `F` the
unique zero-layer matching.  Equation (6) then cannot vanish.

In the remaining overlapping or higher-support cases, cancellation can
no longer hide in bichromatic ports or nonsaturated diagonal units.  It
must occur inside the three saturated monochromatic diagonal graphs.
An overlapping selected edge gives an especially concrete instance: if
`p` is shared by `M_a,M_b`, then the mixed colouring using colour `a` on
the endpoints of `p` and colour `b` elsewhere forces

```text
haf(Z^b[V minus endpoints(p)]) = 0,
```

even though `M_b minus {p}` is a nonzero monomial in that hafnian.  Thus
there must be a second colour-`b` matching on the complement and a
colour-`b` alternating cycle avoiding the endpoints of `p`.

The next unresolved step is to show that the saturated type-flip
geometry cannot sustain all these required cancellations, or to promote
one of them into an exact contradiction.

## Verification

Run:

```text
python verify_universal_saturated_diagonal_zero_layer.py
python audit_universal_saturated_diagonal_zero_layer.py
```

The primary verifier reconstructs the six permuted potentials, proves
componentwise nonnegativity, checks their sum against (1), enumerates all
180 permitted units, and proves the histogram and equality
characterization in (4).  The independent audit
builds the eight normal types directly from reversed bit triples, tests
the coordinate-plane restrictions rather than importing condition (3),
and uses formula (1) without the six-potential construction.

The matching-existence input is the published Bogdanov theorem.  The
programs certify the finite local table on which the new arbitrary-order
reduction depends.

## Boundary

This theorem applies only after reaching the simultaneous balanced
all-bridge normal form.  The separate deeper-blocker branch is outside
its hypotheses.  Within the all-bridge branch it reduces, but does not
yet exclude, overlapping selected matchings and higher support.
