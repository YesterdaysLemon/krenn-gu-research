# Maximal six-blocker overlap collapses to one port-swapped `P_6`

## Status

**Exact characteristic-zero structural theorem.**  Consider two five-root,
six-blocker first-surplus configurations in one twelve-vertex local system.
Suppose their root sets share four roots, their six blocker vertices agree,
and the two exchanged roots are also zero-coupled.  Then each exchanged root
is a valid torus nonblocker for the other five-root set.  The two extracted
`P_6` restrictions use exactly the same six root/port covector rows and
differ only by a simultaneous swap of the two exchanged output coordinates.
The permanent tensor and all three GHZ coefficients are invariant under that
swap.  Thus the purported concentration pair supplies one `P_6` restriction,
not two independent tensor constraints.

This closes one maximal-overlap branch of the six-blocker admissible-quotient
programme structurally.  It does **not** exclude `P_6 -> Delta_3`.  If the
exchanged roots have nonzero mutual coupling, their torus port vectors need
not be their root vectors and the row-swap collapse can fail.  Five-blocker
overlap, additional outside vertices, and the global perfect-matching
identity also remain **UNKNOWN**.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## The port-swap theorem

Let

```text
I={0,1,2,3},       R=I union {a},       R'=I union {b},
B={u_0,...,u_5}.
```

Assume all six root vectors `x_i`, `i in I union {a,b}`, have nonzero target
coordinates and are pairwise zero-coupled.  Assume further that, relative to
each of `R,R'`, the total blocker union is the same set `B`.  There are twelve
vertices, so the unique outside nonblocker for `R` is `b`, and that for `R'`
is `a`.

For `b` relative to `R`, put

```text
A_b(R)=span{B_ib(x_i,-):i in R},       K_b(R)=A_b(R)^perp.
```

Pairwise zero coupling gives `x_b in K_b(R)`.  Since every coordinate of
`x_b` is nonzero, no coordinate covector can belong to `A_b(R)`: otherwise
it would evaluate nontrivially on `x_b`.  Hence `b` blocks no colour and one
may choose its port vector to be

```text
z_b=x_b.
```

The same argument gives `z_a=x_a` for `R'`.

For a shared blocker `u`, define the six covectors

```text
r_iu=B_iu(x_i,-),       i in I union {a,b}.
```

In the natural root-then-port order, the one-port extraction maps have rows

```text
M_u^R  =(r_0u,r_1u,r_2u,r_3u,r_au,r_bu),
M_u^R' =(r_0u,r_1u,r_2u,r_3u,r_bu,r_au).           (1)
```

Thus `M_u^R'=S M_u^R`, where `S` swaps the last two output coordinates and
is independent of `u`.  The order-six permanent tensor is

```text
P_6=sum_(sigma in S_6)
       e_sigma(0) tensor ... tensor e_sigma(5).
```

Applying `S` in every mode permutes the summation index, so

```text
(S^*)^(tensor 6) P_6=P_6.                          (2)
```

The two GHZ coefficients agree as well:

```text
lambda_c^R
 =x_b[c] product_(i in I union {a}) x_i[c]
 =product_(i in I union {a,b}) x_i[c]
 =lambda_c^R'.                                     (3)
```

Equations (1)--(3) prove that the two extracted restrictions are identical
after their canonical row relabelling.  In particular, maximal root/blocker
overlap does not turn the one-port `P_6` problem into the two-port tensor of
[`TWO_PORT_SEVEN_BLOCKER_REDUCTION.md`](TWO_PORT_SEVEN_BLOCKER_REDUCTION.md),
nor does it produce a hidden `P_5` deletion.

## The strongest catalogue pair is locally realizable

The collapse is not vacuous.  The high-overlap local-type pair

```text
three_missing_singletons  versus  all_full
```

from the six-blocker admissible-quotient catalogue has exact covector and
incident-edge-block data with all six blockers shared.

Let `e_0,e_1,e_2` be the coordinate covectors.  List rows in the order
`I,a,b`.  At the three exceptional blockers take

```text
u_0:
 e_1, e_2, e_1+e_2, e_1+2e_2, e_1-e_2, e_0,

u_1:
 e_0, e_2, e_0+e_2, e_0+2e_2, e_0-e_2, e_1,

u_2:
 e_0, e_1, e_0+e_1, e_0+2e_1, e_0-e_1, e_2.      (4)
```

At each of `u_3,u_4,u_5`, take

```text
e_0, e_1, e_2, e_0+e_1+e_2,
e_0+2e_1+3e_2, 3e_0+2e_1+e_2.                     (5)
```

Deleting the port row `b` from (4)--(5) gives blocker profiles

```text
12,02,01,012,012,012,
```

the `three_missing_singletons` type.  Deleting port row `a` gives six full
profiles.  Adding the port row makes every full six-row map rank three, as
required by the `P_6` extraction.  Thus the left marking is precisely the
common-port `1+1+1` row-deletion pattern studied in
[`P6_COMMON_PORT_111_FROBENIUS_REDUCTION.md`](../p6/P6_COMMON_PORT_111_FROBENIUS_REDUCTION.md),
while the right marking is an all-full deletion of the same maps.

This covector table comes from honest nonzero incident edge blocks.  Take all
six root vectors equal to `x=(1,1,1)`.  Given a desired covector row `r`, put

```text
p=(1,1,1)/3,       W_iu=p r^T.
```

Then `x^T W_iu=r^T`, and `W_iu` is nonzero.  On every root--root edge take

```text
D=diag(1,-1,0).
```

It is nonzero and `x^T D x=0`.  The root--root incident covector is
`(1,-1,0)`, whose span contains no coordinate covector, while its kernel
contains the torus point `x`.  Consequently `a` and `b` are indeed the two
nonblocker ports claimed above.

This proves local covector-space and incident-edge-block realizability.  It
does **not** extend the displayed blocks to a graph whose full
perfect-matching polynomial equals GHZ.  In particular, it does not realize
the common-port Frobenius factorisation or evade the known gate obstructions.

## Exact residual

The maximal-overlap concentration route can add information only after at
least one hypothesis used in the collapse is removed:

```text
B_ab(x_a,x_b) != 0,          so z_a,z_b are not forced to be root vectors;
only five blockers shared;
additional outside vertices or different residual ports;
or a global matching identity coupling the otherwise free incident blocks.
```

The six-blocker profile catalogue alone, and even its local incident-block
realization, cannot decide those alternatives.  Covector/graph realizability
of the full GHZ matching identity remains `UNKNOWN`.

## Replay

```text
uv run --with sympy python claims/arbitrary-order/verify_six_blocker_maximal_overlap_port_swap_collapse.py
uv run --with sympy python claims/arbitrary-order/audit_six_blocker_maximal_overlap_port_swap_collapse.py
```

The primary verifier checks the simultaneous `S_6` row-swap invariance, the
GHZ coefficient identity, every profile and row rank in (4)--(5), all local
edge-block contractions, and both torus nonblocker spaces over `Q`.  The
no-import audit uses a separate subset-permanent contraction on all `3^6`
target words, a different incident-block section, and a different nonzero
root--root block.  No finite-field inference is used.
