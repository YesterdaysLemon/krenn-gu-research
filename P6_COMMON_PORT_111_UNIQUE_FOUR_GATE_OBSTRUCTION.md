# The unique four-gate rank-five branch is impossible

## Status

**Exact characteristic-zero obstruction.**  In the rank-five common-port
`1+1+1` configuration from
[`P6_COMMON_PORT_111_RANK_FIVE_CATALYTICANT_CHECKPOINT.md`](P6_COMMON_PORT_111_RANK_FIVE_CATALYTICANT_CHECKPOINT.md),
the unique size-four cover of the twenty-two split catalecticant minors is

```text
{g_0,g_3,g_5,g_9}.                                  (1)
```

No pair of three-planes `B,C subset C^5` on which all four gates in (1)
vanish can satisfy the full pointwise rank-two catalecticant condition.  In
fact the four gates force

```text
B=C=span(e_0,e_2,e_4)
```

or

```text
B=C=span(e_0,e_1,e_3),                              (2)
```

and one explicit catalecticant value has rank three in either case.
At this theorem's checkpoint, every surviving solution had to lie on one of
the other 52 minimal gate-cover branches, all of size at least five.  Those
branches are now excluded by perfect-pairing certificates in
[`P6_COMMON_PORT_111_ALL_GATE_COVERS_OBSTRUCTION.md`](P6_COMMON_PORT_111_ALL_GATE_COVERS_OBSTRUCTION.md).

Together the two follow-up theorems exclude all 53 covers for the displayed
rank-five model.  They do not classify every configuration with `dim K=5`,
decide `P_6 -> Delta_3`, or settle the global Krenn--Gu conjecture.

## Four gates on a coordinate cycle

Use coordinates `e_0,...,e_4` of `V=C^5`.  The four gates are

```text
g_0(b,c)=b_3 c_4+b_4 c_3,
g_3(b,c)=b_1 c_4+b_4 c_1,
g_5(b,c)=b_1 c_2+b_2 c_1,
g_9(b,c)=b_2 c_3+b_3 c_2.                           (3)
```

They are the hyperbolic edge pairings on the four-cycle

```text
1--2--3--4--1.                                      (4)
```

For a cycle edge `ij`, write `E_ij=span(e_i,e_j)`, let `pi_ij` be coordinate
projection to `E_ij`, and put

```text
R_ij=ker(pi_ij)=span(e_k:k notin {i,j}).             (5)
```

The gate on `E_ij` is nondegenerate.  If it vanishes on `B x C`, then

```text
dim pi_ij(B)+dim pi_ij(C) <= 2.                     (6)
```

## A zero projection is impossible

Suppose `pi_ij(B)=0`.  Since both `B` and `R_ij` have dimension three,

```text
B=R_ij.                                             (7)
```

Let `kl` be the opposite edge of (4).  Then `pi_kl(B)=E_kl`, so (6) forces

```text
C=R_kl.                                             (8)
```

On either edge joining an endpoint of `ij` to an endpoint of `kl`, the two
planes project to the two opposite coordinate lines.  Their hyperbolic
pairing is nonzero, contradicting the adjacent gate.  The same argument with
`B,C` interchanged excludes `pi_ij(C)=0`.

Thus every cycle-edge projection of both planes is nonzero.  Equation (6)
now gives

```text
dim pi_ij(B)=dim pi_ij(C)=1                         (9)
```

for all four edges.

## Rank-one cycle projections force alternating coordinate planes

Let

```text
ell_i=e_i^* restricted to B in B^*.                 (10)
```

Condition (9) says that adjacent `ell_i,ell_j` are proportional and not both
zero.  The zero set among `ell_1,...,ell_4` is therefore an independent set
of the four-cycle.

If it has size zero or one, all nonzero `ell_1,...,ell_4` are proportional.
Together with `ell_0` they span at most a two-space.  This is impossible,
because the five coordinate restrictions span the three-dimensional dual
`B^*`.

The zero set must consequently be one of the two maximum independent sets

```text
{1,3},       {2,4}.                                 (11)
```

If it is `{1,3}`, then `B` is contained in the three-space
`span(e_0,e_2,e_4)` and hence equals it.  The other case gives
`B=span(e_0,e_1,e_3)`.  The same argument applies to `C`.

The hyperbolic edge pairings in (3) exclude opposite parity choices for
`B,C`: on every cycle edge those choices select opposite coordinate lines,
which pair nontrivially.  Equal parity choices vanish identically.  This
proves (2).

## The full catalecticant fails on both planes

Use the five-row basis of the forbidden quadratic span `K` fixed in the
rank-five checkpoint and its catalecticant

```text
C_K(b,c)_(s,p)=tau(k_s X_p b c).                    (12)
```

For the even plane in (2), take `(b,c)=(e_0,e_2)`.  Exact squarefree
multiplication gives

```text
C_K(e_0,e_2)=
((0,2,0, 0,0),
 (0,0,0, 0,0),
 (0,0,0, 0,0),
 (0,0,0,-2,0),
 (0,0,0,-1,1)).                                    (13)
```

Rows `(0,3,4)` and columns `(1,3,4)` have determinant `-4`.

For the odd plane, take `(b,c)=(e_0,e_1)`.  Then

```text
C_K(e_0,e_1)=
((0,0,2,0,0),
 (0,0,0,0,0),
 (0,0,0,0,2),
 (0,0,0,0,0),
 (0,0,0,-1,1)).                                    (14)
```

Rows `(0,2,4)` and columns `(2,3,4)` have determinant `4`.
Both values therefore have rank at least three, contradicting the necessary
rank-at-most-two condition on `B x C`.  This proves the obstruction.

## Exact replay

```text
uv run --with sympy python verify_p6_common_port_111_unique_four_gate_obstruction.py
python audit_p6_common_port_111_unique_four_gate_obstruction.py
```

The primary verifier reconstructs the gate matrices, their radicals and
opposite-edge contradictions, the two alternating planes, the unique
four-cover, and both rational catalecticant minors.  The independent audit
rebuilds the cycle combinatorics and all matrices modulo `5,7,11`.  Neither
script searches a Grassmannian or infers a characteristic-zero statement
from finite-field points.
