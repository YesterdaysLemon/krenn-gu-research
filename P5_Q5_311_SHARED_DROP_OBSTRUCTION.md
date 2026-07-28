# The shared rank-drop branch of `q5_311` is impossible

## Status

This is an exact tensor theorem over `C`.

In the normalized `q5_311` branch of a hypothetical restriction

```text
P_5 -> Delta_3,
```

the two rare deleted-`P_4` slices cannot lose rank in the same remaining
mode.  Combined with
[`P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md`](P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md),
their two rank-drop sets must therefore be disjoint two-element sets
partitioning the four remaining modes.

This eliminates one arbitrary-chart branch of `q5_311`.  It does not
yet eliminate the disjoint `2+2` branch, the complete restriction
`P_5 -> Delta_3`, or the arbitrary-order Krenn--Gu prize conjecture.

## Setup

Let the three majority source rows be `M={m_0,m_1,m_2}` and the two rare
source rows be `s_1,s_2`.  The slice obtained by deleting `s_1` is a
nonzero pure tensor in target direction `w_1`; deleting `s_2` gives a
nonzero pure tensor in the independent target direction `w_2`:

```text
T_1=lambda_1 w_1 tensor w_1 tensor w_1 tensor w_1,
T_2=lambda_2 w_2 tensor w_2 tensor w_2 tensor w_2,
lambda_1 lambda_2 != 0.                               (1)
```

Suppose one remaining mode `h` loses rank under both deletions.  The
rank-drop incidence lemma says that its three rows on `M` span a line
`L`, while its rows `x,y` on `s_1,s_2` complete `L` to a basis:

```text
span(L,x,y)=C^3.                                      (2)
```

In the first slice, mode `h` sees `M` together with `s_2`, so its image
is `span(L,y)` and hence

```text
w_1 in span(L,y).
```

In the second slice it sees `M` together with `s_1`, giving

```text
w_2 in span(L,x).                                     (3)
```

## The common residual tensor

Let

```text
S=(tensor over the other three modes, restricted to M) P_3.   (4)
```

This is one fixed tensor: it depends only on the three common source
rows and the three modes other than `h`.

Choose a covector `phi_y` in mode `h` that vanishes on `L` and `x` and
satisfies `phi_y(y)=1`.  Contract the first identity in (1) against
`phi_y`.  On the source side, the covector kills the three rows in `M`
and selects `s_2`, leaving exactly `S`.  On the target side it gives

```text
S=lambda_1 beta_1 w_1 tensor w_1 tensor w_1,           (5)
```

where `beta_1` is the coefficient of `y` in `w_1` relative to
`span(L,y)`.

Similarly, the covector `phi_x` killing `L,y` and taking `x` to one
contracts the second slice to

```text
S=lambda_2 beta_2 w_2 tensor w_2 tensor w_2.           (6)
```

Here `beta_2` is the coefficient of `x` in `w_2` relative to
`span(L,x)`.

If `beta_1=0`, then `w_1=L` and (5) says `S=0`.  Equation (6) then
forces `beta_2=0`, because its other factors and `lambda_2` are nonzero.
But this would also give `w_2=L`, contradicting independence of
`w_1,w_2`.  The same argument applies with the indices reversed.

Thus both beta coefficients are nonzero.  Equations (5)--(6) then say
that the two pure tensors

```text
w_1 tensor w_1 tensor w_1,
w_2 tensor w_2 tensor w_2
```

are proportional.  Pure nonzero tensors are proportional only when
their corresponding factor lines are proportional.  This again
contradicts the independence of the two target colour directions.

The assumed shared rank-drop mode cannot exist.

## Consequence

Each rare deletion drops rank in at least two of the four remaining
modes.  Since the drop sets are now disjoint, both have size exactly two:

```text
|D_1|=|D_2|=2,
D_1 disjoint union D_2={1,2,3,4}.                     (7)
```

The only remaining `q5_311` rank-incidence branch is the disjoint `2+2`
partition.

## Verification

Run:

```text
python verify_p5_q5_311_shared_drop_obstruction.py
python audit_p5_q5_311_shared_drop_obstruction.py
```

The primary verifier reconstructs both deleted-`P_4` contractions,
checks that they produce the same residual `P_3`, and verifies the
linear independence of the two target pure cubes.  The independent
audit enumerates the projective configuration over `F_3` and `F_5` and
finds no compatible shared-drop instance.  The finite-field census
audits the case split; the written argument above is over `C`.
