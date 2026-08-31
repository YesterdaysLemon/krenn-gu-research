# Four-root torus-star equal-leaf H4 Q6 p=0,1 nonzero-offset exclusion (GLD102)

## Status and exact scope

**Proved exact scoped characteristic-zero theorem (GLD102).**

On the normalized GLD88/F88 equal-leaf H4 offset chart, let `M(G)` be the
complete `37 x 9` GLD71 syndrome and write

~~~text
b = b88(p,q,a) + B,
c = c88(p,q,a) + C.
~~~

For either `p=0` or `p=1`, with arbitrary `a`, the exact statement is

~~~text
V(Q6) intersect D(Delta) intersect {rank M(G) <= 6}
  is contained in V(B,C).
~~~

Equivalently, there is no rank-at-most-six point with nonzero offset
`(B,C)!=(0,0)` on either of these two parameter fibres.  The proof uses the
exhaustive cover

~~~text
(B,C)!=(0,0)  =>  B!=0  or  (B=0 and C!=0).
~~~

This is an offset implication, not an endpoint exclusion.  It does not show
that the `B=C=0` F88 point is absent, does not assert a physical incidence
empty set, and does not extend to arbitrary `p`, the full `E31=0` wall, or
another chart.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Chart, equations, and retained gates

The normalized equal-leaf chart is

~~~text
G = [1  1       1      ]
    [p  q       s      ]
    [a  1+b     1+c    ],

s = (p+q-pq)/(p+q-1).
~~~

The H4 relation is `pq+ps+qs-p-q-s=0`.  Put

~~~text
d0 = p+q-1,
P  = p^2-p+1,
L1 = p^2+2pq-2p-q,
L2 = 2pq-p+q^2-2q,
e  = 2pq^2-2pq-p-q^2-2q+2,
Delta = (p-q)d0 P L1 L2 e.
~~~

The quartic relation is

~~~text
Q6 = 2p^4q^2-2p^4q+p^4
     +2p^3q^3-7p^3q^2+5p^3q-2p^3
     +2p^2q^4-7p^2q^3+12p^2q^2-7p^2q+2p^2
     -2pq^4+5pq^3-7pq^2+2pq+q^4-2q^3+2q^2.
~~~

Its `q`-leading coefficient is `H2=2p^2-2p+1`, which equals one at both
`p=0` and `p=1`.  Every denominator cleared in GLD102 factors through
`Delta`; the two chart ideals explicitly localize at `Delta`.  No factor of
`Delta` is cancelled or silently restored.

At the two fibres,

~~~text
p=0: Q6=q^4-2q^3+2q^2,
     Delta=-q^3(q-2)(q-1)(q^2+2q-2),

p=1: Q6=q^4-2q^3+2q^2-2q+1,
     Delta=-q(q-1)^3(q+1)(q^2-4q+1).
~~~

## 2. Six actual necessary seven-minors

The six generators are actual ordered `7 x 7` minors of `M(G)`:

~~~text
T0 = det M[(0,1,2,17,25,31,28), (0,1,3,4,6,7,8)],
T1 = det M[(0,1,2,17,25,31,32), (0,1,3,4,6,7,2)],
T2 = det M[(0,1,2,17,25,31,32), (0,1,3,4,6,7,5)],
T3 = det M[(0,1,2,17,25,31,33), (0,1,3,4,6,7,8)],
Y1 = det M[(0,1,17,28,31,32,33), (0,1,3,4,5,6,7)],
X3 = det M[(0,1,17,28,31,32,33), (0,1,2,3,4,6,7)].
~~~

Thus `rank M(G)<=6` makes all six vanish.  GLD102 uses only this forward
implication.  It never claims that these selectors generate the full rank
ideal or that selector vanishing is sufficient for low rank.

Both tracked implementations independently reconstruct the minors from the
GLD71 sparse syndrome data and the written GLD88 family.  They agree on all
24 primitive equation hashes: six selectors, two parameter fibres, and two
offset charts.

## 3. The B-open chart

On `D(B)`, set `C=B t`, divide each selected minor by the common nonzero
factor `B`, clear only `Delta`-unit denominators, and adjoin the inverse
equation `z B Delta-1`.

For `p=0`, the first five selectors have the exact grevlex basis

~~~text
z^2 + z/8 + 1/128,
a - 1,
q - 16z - 2,
B + 8z,
t + 240z/17 + 7/17.
~~~

The sixth selector `T3` reduces to zero, so the six-selector locus consists
of exactly the two conjugate roots of `128z^2+16z+1`.  Written explicitly,
with `epsilon` equal to `-1` or `1`, they are

~~~text
q = 1 + epsilon*i,
B = (1-epsilon*i)/2,
a = 1,
t = (8-15epsilon*i)/17,
C = B t.
~~~

At both points all six displayed selectors vanish.  However, the direct
minor with rows `(0,1,2,17,25,28,32)` and columns `(0,1,2,3,4,5,6)` is

~~~text
(-29952 + 28416 epsilon*i)/289,
~~~

which is nonzero.  Hence the complete syndrome has rank at least seven at
both selected-minor survivors.  Neither point can satisfy the assumed rank
bound.

For `p=1`, the first five selectors have basis

~~~text
z^2 + 1/64,
a + 8z - 1,
q + 8z,
B + 1/2,
t - 40z/13 + 12/13.
~~~

The exact remainder of `T3` is

~~~text
-2048z/13 - 384/13.
~~~

It is coprime to `64z^2+1`, so the sixth selector removes both residual
points.  The `p=1` B-open six-selector locus is empty.

The basis digests reported by the primary are

~~~text
p=0: 9537b7269b6d1ca5d1782213313dc45c70b7b5357ec363b2b849ee754c86556f
p=1: 949dbbd7cb669602c03400612c7636dfdc0666127a99e8fa84591d3897ff60f3
~~~

## 4. The B=0, C-open chart

When `B=0`, every displayed selected minor is exactly `C` times a polynomial
coefficient in `a,q`.  On `D(C)` the rank equations therefore imply the six
coefficient equations.  For each of `p=0` and `p=1`, the exact ideal

~~~text
<Q6, six C-coefficients, z Delta-1> in Q[a,q,z]
~~~

has grevlex basis `[1]`.  Thus no selected-minor point, and hence no
rank-at-most-six point, lies on `V(B) intersect D(C*Delta)`.

This division uses the declared `C!=0` chart.  It is not a cancellation at
`C=0` and says nothing about the endpoint.

## 5. Exhaustive composition

For a nonzero offset there are exactly two cases:

1. `B!=0`, excluded at both parameter values by Section 3; or
2. `B=0` and `C!=0`, excluded at both parameter values by Section 4.

Therefore, on `V(Q6) intersect D(Delta)` with `p=0` or `p=1`, the complete
syndrome rank bound `rank M(G)<=6` forces `B=C=0`.

For the `a=0` GLD101 norm cover, GLD102 closes the two retained norm supports
`p=0` and `p=1` at the level of nonzero offsets.  It does not by itself close
the other GLD101 supports or the `B=C=0` endpoint.

## 6. Tracked evidence and independence

The primary verifier is

~~~text
claims/arbitrary-order/
  verify_four_root_torus_star_equal_leaf_h4_q6_p01_nonzero_offset_exclusion.py
~~~

It imports the pinned committed GLD71 and GLD88 constructors, reconstructs
the six raw sparse offset minors once over `Q(p,q,a)`, specializes both
fibres, recomputes all ideals, and checks the full-syndrome rank witnesses.
Its reference-host exact run completed in about 25 seconds.

The independent audit is

~~~text
claims/arbitrary-order/
  audit_four_root_torus_star_equal_leaf_h4_q6_p01_nonzero_offset_exclusion.py
~~~

It imports no project verifier.  It carries copied immutable syndrome
supports and a local GLD88 chart transcription, specializes each chart before
forming direct exact matrix determinants, and independently recomputes the
same equation hashes, bases, remainders, units, and rank witnesses.  Its
reference-host exact run completed in about 59 seconds.

The two implementations share the mathematical selector definitions and
chart formulas, as they must, but differ in source boundary, determinant
construction, and specialization order.  No Singular binary or ignored
research-run artifact is required for either tracked replay.

## 7. Nonclaims

GLD102 does not claim:

* that `B=C=0` is empty or that the F88 endpoint is physically impossible;
* a physical incidence theorem, a composition with `C_8=1`, `D(Omega)`, or
  GLD95;
* an arbitrary-`p`, arbitrary-E31-wall, generic-parameter, or full H4/Q6
  theorem;
* a conclusion on `Delta=0`, another gauge, chart, component, source branch,
  profile, root, or order;
* a converse from six selected minors to syndrome rank;
* Fitting-ideal emptiness, source integrability, graph lifting, target
  attachment, or global gluing; or
* a proof, refutation, or resolution of the global Krenn--Gu conjecture.

The exact result is the stated `p=0,1` nonzero-offset exclusion, and no more.
The global Krenn--Gu conjecture remains **UNRESOLVED**.
