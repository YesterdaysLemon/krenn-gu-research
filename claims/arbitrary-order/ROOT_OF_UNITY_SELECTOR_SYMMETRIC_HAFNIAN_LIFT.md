# Symmetric hafnian lift of the four-row selector

## Status

**Exact characteristic-zero heralded realization.**  The four-row
root-of-unity selector seed is the full matching polynomial of a legal
loopless symmetric graph after six ordinary local contractions.  Thus graph
symmetry and the hafnian expansion are not intrinsic obstructions to this
seed.

This does **not** remove the heralds, couple the selector to the fixed
Question-2 module, produce a Question-1 counterexample, or resolve the global
Krenn--Gu conjecture.  In the displayed lift, directly uncontracting the two
constant-column modes gives rank-one local maps, so that naive promotion is
provably non-concise.  More generally, the certified exact subrank-two theorem
for `P_4` excludes every three-colour promotion that first fixes the entire
left side and then changes only the four right local maps.

## The symmetric lift

Write

```text
B = [ u  v   1   1 ]
    [ w  z   1   1 ]
    [ p  q   2  -2 ]
    [ r  s   2  -2 ].
```

Let `A` be the symmetric `8 x 8` adjacency matrix

```text
A = [ 0   B  ] .
    [ B^T 0  ]
```

Every nonzero perfect matching of `A` pairs the four left vertices
bijectively with the four right vertices.  Conversely every such bijection is
a perfect matching.  Hence, including all 105 perfect matchings on eight
labelled vertices,

```text
haf(A)=per(B)
      =-8(uz+vw)+2(ps+qr).                         (1)
```

Exactly `4!=24` matching terms survive; the other 81 contain a zero
same-side edge.  Therefore (1) is an identity for the full symmetric graph
matching polynomial, not only a separately declared permanent.

## Legal coloured-edge realization

Use local dimension four.  Denote the bipartition by
`L_1,...,L_4` and `R_1,...,R_4`, and fix every left vector to `e_0`.  Leave

```text
z_(R_1)=(u,w,p,r),   z_(R_2)=(v,z,q,s)
```

variable.  On the edge `L_i R_j`, choose a `4 x 4` block whose zeroth row is
`e_i^T` for `j=1,2`.  For `j=3,4`, fix `z_(R_j)=e_0` and put respectively

```text
W_(L_i,R_3)[0,0]=(1,1,2,2)_i,
W_(L_i,R_4)[0,0]=(1,1,-2,-2)_i.
```

All other entries and all same-side edge blocks are zero, and the reverse
orientation is the transpose block.  Then

```text
e_0^T W_(L_i,R_j) z_(R_j)=B_ij,
```

so this is a loopless graph with the required symmetric edge convention.
The two constant columns are therefore honest fixed-mode, or herald,
contractions.

The same construction works after specializing the variable columns to any
lower-dimensional incidence images.  The four independent coordinates above
are useful because the motivating Question-2 module has local dimension four.

## The precise remaining barrier

Before contraction, the two constant right modes have local maps

```text
L_3=(1,1,2,2)^T e_0^T,
L_4=(1,1,-2,-2)^T e_0^T.                         (2)
```

Both have rank one.  A tensor obtained through either map has one-mode
flattening rank at most one, whereas every nontrivial diagonal tensor has
flattening rank at least two.  Consequently simply declaring these two
heralds to be outputs cannot promote this realization to Question 1.

There is also a completion-independent obstruction to the whole fixed-left
architecture.  After the four left vertices are contracted, the tensor in the
four right modes is

```text
(L_1 tensor L_2 tensor L_3 tensor L_4) P_4
```

for whatever four local maps a proposed completion supplies.  The exact
[`P_4` subrank theorem](FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md) says
that this can never be `Delta_3`.  Thus filling the unused columns of (2),
even so that all four maps have rank at least three, cannot repair a
three-colour promotion while the left half remains fixed.  A successful
construction would have to keep additional left modes live or use a larger
coupled matching architecture; this argument does not exclude either.

The bounded Route-F problem is now sharper:

1. the seed's permanent cancellation survives the full symmetric hafnian;
2. its constants have a legal herald implementation;
3. no completion confined to the four right modes can overcome the exact
   `P_4` subrank-two obstruction;
4. a useful promotion must therefore retain additional live modes and
   preserve the cancellation and all module coefficients; and
5. compatibility with the existing 17-mode Question-2 support remains to be
   checked from the combined graph, not inferred from (1).

## Exact replay

```text
uv run --with sympy python claims/arbitrary-order/verify_root_of_unity_selector_symmetric_hafnian_lift.py
python claims/arbitrary-order/audit_root_of_unity_selector_symmetric_hafnian_lift.py
python claims/arbitrary-order/verify_fourth_order_permanent_subrank.py
python claims/arbitrary-order/audit_fourth_order_permanent_subrank.py
```

The primary verifier constructs the symmetric adjacency and coloured edge
blocks, enumerates the full hafnian, and checks the four local-map ranks.  The
audit imports no proof code and recomputes the permanent and hafnian as sparse
integer polynomial dictionaries.  The last two commands replay the inherited
characteristic-zero subrank theorem and its separate finite-field audit; the
finite-field calculation is audit evidence, not the characteristic-zero
proof.
