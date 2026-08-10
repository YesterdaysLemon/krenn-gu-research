# Two-all-normal-modes obstruction in normalized `q5_221`

## Status

This is an exact monotone tensor theorem over `C`.

No normalized `q5_221` restriction can have both modes containing
`h_2` also contain `h_0,h_1`.  Equivalently, monotone seven-incidence
cover `#5`

```text
D_0=0011,  D_1=0111,  D_2=0011
```

is impossible, including every higher-incidence stratum above it.
Together with the distinguished-normal theorem, this leaves seven
monotone cover orbits at this checkpoint.  Subsequent theorems close
them and complete normalized `q5_221`; `P_5 -> Delta_3` and the global
conjecture remain open.

## Orient the two distinguished modes

The distinguished-normal multiplicity theorem gives exactly two
`h_2` modes.  Call them `P,Q`.  Double contraction of both `T_0` and
`T_1` by their `h_2` pullbacks shows that the two pullbacks have
complementary singleton target support.  Relabel so that

```text
L_P^*epsilon_0 in C*h_2,
L_Q^*epsilon_1 in C*h_2.                             (1)
```

Suppose both modes are all-normal:

```text
U_P=U_Q=span(h_0,h_1,h_2).                           (2)
```

At `Q`, the `Q_02` residual has rank one and only `h_1` survives.
At `P`, the `Q_12` residual has rank one and only `h_0` survives.
The own-colour equations align those two surviving directions with
target colours zero and one.  On `H_2`, the target-two rows at `P,Q`
are respectively `h_1,h_0`.

Consequently the two remaining modes `A,B` must send the following
three nonzero bilinear tensors to three pure coordinate lines:

```text
(L_A tensor L_B)Sym(u_0,h_1) in C*(e_0 tensor e_0),
(L_A tensor L_B)Sym(h_0,u_1) in C*(e_1 tensor e_1),
(L_A tensor L_B)Sym(h_0,h_1) in C*(e_2 tensor e_2).  (3)
```

The first two identities are the doubly contracted `T_0,T_1`
identities; the third is the `T_2` identity contracted at `P,Q`.

## A three-edge dependency obstruction

Write the images at mode `A` as

```text
a=L_A(u_0), b=L_A(h_0), c=L_A(u_1), d=L_A(h_1),
```

and use primes for mode `B`.  Each equation in (3) is a nonzero
rank-one sum of two decomposable matrices:

```text
a tensor d' + d tensor a',
b tensor c' + c tensor b',
b tensor d' + d tensor b'.                           (4)
```

The elementary two-summand Segre lemma says that each line of (4) can
have rank one only if its two vectors are proportional at `A` or its
two vectors are proportional at `B`.  Thus colour the three source
edges

```text
{a,d}, {b,c}, {b,d}                                  (5)
```

by an endpoint `A` or `B` at which that dependency occurs.

There are three edges and only two colours, so one endpoint receives
at least two edges.  Any two edges in (5) leave at most two connected
components on the four source directions:

```text
{a,d}+{b,c}: two disjoint dependent pairs,
{a,d}+{b,d}: one dependent triple plus c,
{b,c}+{b,d}: one dependent triple plus a.
```

Hence the four images at that endpoint span a space of dimension at
most two.

But neither `A` nor `B` contains `h_2`, because `P,Q` are the exactly
two `h_2` modes.  Therefore restriction to

```text
H_2=span(e_0,e_1,e_2,e_3)
```

has rank three at both `A,B`.  Their four images
`a,b,c,d` and `a',b',c',d'` must each span a
three-dimensional space.  This contradicts the dependency conclusion
and proves the monotone obstruction.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q5_221_two_all_normal_modes.py
python claims/p5/frontier/audit_p5_q5_221_two_all_normal_modes.py
```

The primary verifier reconstructs the three bilinear source tensors
from the embedded `P_4` slices and checks all endpoint-colourings of the
three-edge dependency graph.  The independent audit obtains the source
contractions by apolar differentiation and checks the three possible
two-edge component partitions directly.  Neither enumerates local
maps or row spaces.
