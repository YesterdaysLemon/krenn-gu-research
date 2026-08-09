# The order-twelve quotient-zero cofactor condition is locally realizable

## Status

**Exact characteristic-zero local realization theorem.**  There are four
common-root row systems on six blockers, of ranks

```text
(2,2,2,3,3,3),
```

and fifteen nonzero rational blocker--blocker edge blocks for which the
entire four-root cofactor tensor is identically zero:

```text
C_I=0.                                                  (1)
```

Thus `C_I` lies in the GHZ diagonal plane, and the quotient-zero condition
from
[`SIX_BLOCKER_ORDER12_QUOTIENT_RANK_FRAME_CLASSIFICATION.md`](SIX_BLOCKER_ORDER12_QUOTIENT_RANK_FRAME_CLASSIFICATION.md)
cannot be excluded from the common-four-row constraints or from nonvanishing
of the blocker--blocker blocks alone.  The displayed syzygy is rigid for its
fixed common-row core: the 726 off-diagonal coefficient equations have exact
rational rank 134 in the 135 blocker-edge variables, and their one-dimensional
kernel is precisely the displayed solution.  Its three diagonal coefficients
also vanish.

The data extend to honest nonzero root--root, root--blocker, exchanged-root,
and exchanged-root--blocker blocks.  Both five-root markings have the same
six blockers, with every root deletion profile full, and both torus ports are
valid.  Nevertheless the endpoint permanent tensors are not diagonal; one
mixed endpoint has an off-diagonal coefficient `44`.  This is therefore a
local cofactor realization only, not a global Krenn--Gu witness.  The global
matching identity and arbitrary ambient order remain **UNKNOWN**, and the
global Krenn--Gu conjecture remains **UNRESOLVED**.

## The common four-row core

List the four common-root covectors at each blocker as the rows of `H_u`:

```text
H_0 = [ -1 -2 -1 ]
      [  0 -1  1 ]
      [ -1 -1 -2 ]
      [ -1 -1 -2 ],

H_1 = [  0  0  0 ]
      [  0  0  0 ]
      [  0 -1 -2 ]
      [  1  2  2 ],

H_2 = [  2 -2  0 ]
      [  0  0  1 ]
      [ -2  2  1 ]
      [  2 -2  1 ],

H_3 = [ -2  0  1 ]
      [  2 -2  0 ]
      [  0  0 -2 ]
      [ -2  0  2 ],

H_4 = [  2 -2  0 ]
      [  0 -1  0 ]
      [  1  0 -1 ]
      [  2  1 -2 ],

H_5 = [  1  0  1 ]
      [  0  2  0 ]
      [  0  2  1 ]
      [ -1  2  0 ].                                    (2)
```

Exact row reduction gives ranks `(2,2,2,3,3,3)`.  At each of the first three
modes, adjoining either `e_0^*` or `e_1^*` raises the rank to three.  Hence
take the exchanged root rows

```text
r_au=e_0^*,       r_bu=e_1^*       for every u.         (3)
```

Both five-root row spans are all of `(C^3)^*` at every blocker.  Their six
deletion profiles are therefore `(7,7,7,7,7,7)`.

## Fifteen nonzero blocker blocks

For `u<v`, orient the edge block from `u` to `v` and use the following
matrices:

```text
W_01=[[-1,-1, 0],[-1,-1, 0],[-2,-2, 0]],
W_02=[[ 0, 0, 2],[ 0, 0, 2],[ 0, 0, 4]],
W_03=[[-2, 0, 0],[-2, 0, 0],[-4, 0, 0]],
W_04=[[ 3, 1,-3],[ 3, 1,-3],[ 6, 2,-6]],
W_05=[[-1, 4, 1],[-1, 4, 1],[-2, 8, 2]],

W_12=[[-2, 2, 1],[-6, 6, 1],[-8, 8, 0]],
W_13=[[ 0, 0,-2],[ 2, 0,-6],[ 4, 0,-8]],
W_14=[[ 1, 0,-1],[ 0,-1, 0],[-2,-2, 2]],
W_15=[[ 0, 2, 1],[ 1, 2, 2],[ 2, 0, 2]],

W_23=[[-4, 0, 8],[ 4, 0,-8],[ 2, 0, 0]],
W_24=[[ 2, 2,-2],[-2,-2, 2],[-3,-1, 3]],
W_25=[[-2, 0,-2],[ 2, 0, 2],[ 1,-4,-1]],

W_34=[[ 2, 0,-2],[ 0, 0, 0],[ 2, 2,-2]],
W_35=[[ 0, 4, 2],[ 0, 0, 0],[-2, 0,-2]],
W_45=[[ 1,-6,-2],[ 0,-2,-1],[-1, 6, 2]].              (4)
```

Every matrix in (4) is nonzero.  As usual, the reverse orientation uses its
transpose.

For a target word `w=(w_0,...,w_5)`, let

```text
K_uv(w)
 =per([H_m[i,w_m]]_(i=0,...,3; m in B\{u,v})).        (5)
```

The coefficient of `w` in the common cofactor is

```text
[w]C_I=sum_(u<v) W_uv[w_u,w_v] K_uv(w).                (6)
```

Direct exact evaluation of (6) on all `3^6=729` words gives zero.  This
proves (1), including the three diagonal words.

The cancellation is not an artifact of excess freedom.  Put the 135 entries
of the fifteen blocks in lexicographic `(u,v,i,j)` order, and put the 726
nonconstant equations (6) into a matrix `A`.  Fraction-free rational row
reduction gives

```text
rank_Q(A)=134,       dim_Q ker(A)=1.                   (7)
```

The vector formed by (4) has 94 nonzero entries and spans that kernel.  Its
diagonal image is `(0,0,0)`.  Thus, for the fixed core (2), every diagonal
cofactor is a scalar multiple of the zero tensor.

## Honest local root and port realization

Take all six root vectors equal to

```text
x=(1,1,1),       z_a=(1,2,3),       z_b=(1,3,2).       (8)
```

Use the same exchanged-root data as in the earlier port-freedom theorem:

```text
h_a=(1,-2,1),             h_b=(-1,-1,2),
alpha_a=(2,-1,0),         zeta_a=(-1,1,0),
alpha_b=(3/2,-1/2,0),     zeta_b=(-1/2,1/2,0),
W_ab=alpha_a alpha_b^T.                                 (9)
```

Then the cross coupling is one, both mixed root/port couplings vanish, and
the two exchanged nonblocker spaces are

```text
<h_a,alpha_a>^perp=<z_a>,       <h_b,alpha_b>^perp=<z_b>.             (10)
```

Use `diag(1,-1,0)` on common-root pairs, `e_0 h_a^T` on common-root--`a`
edges, and `e_0 h_b^T` on common-root--`b` edges.  These blocks are nonzero
and give all required zero couplings.

Every row of (2) is also realized by a nonzero incident block.  For a
nonzero desired covector `r`, use `e_0 r^T`.  For a zero desired covector,
use

```text
(1,-1,0)^T e_0^T;                                      (11)
```

its contraction by `x^T` is zero although the block itself is nonzero.

Finally choose constant port rows

```text
s_au=(0,1,1),       s_bu=(1,0,1).                     (12)
```

The exchanged-root--blocker blocks

```text
W_au=alpha_a r_au^T+zeta_a s_au^T,
W_bu=alpha_b r_bu^T+zeta_b s_bu^T                     (13)
```

are nonzero and realize both the root and port rows.  Equations (2)--(13)
therefore give simultaneous roots, ports, all-full blocker profiles, and
nonzero edge blocks throughout the entire twelve-vertex local system.

## Why this is not a global witness

The local model satisfies the cofactor half `C_I=0`, but it does not satisfy
the other half of the quotient-zero branch, namely that every tensor
`Pi(y_a,y_b)` is diagonal.  At the mixed endpoint `(x_a,z_b)`, the exact
permanent coefficient at target word `000001` is

```text
[000001]Pi(x_a,z_b)=44 !=0.                            (14)
```

The GHZ coefficient at that word is zero.  Consequently the data cannot be
extended to the full matching identity as displayed.  It proves only that
no obstruction based on the common-row cofactor map, its diagonal quotient,
or nonzero local edge blocks can eliminate the quotient-zero branch.

## Exact residual

The quotient-zero branch now has a sharp boundary:

```text
C_I in mathcal D from local common-row/block data: SURVIVES;
C_I=0 with all fifteen blocker blocks nonzero: EXPLICITLY REALIZED;
simultaneous diagonal P1 x P1 permanent surface: UNKNOWN;
extension to a global matching identity: UNKNOWN;
global Krenn--Gu conjecture: UNRESOLVED.
```

The next obstruction must use the permanent surface `Pi`, not merely the
blocker cofactor `C_I`.

## Replay

```text
uv run --with sympy python claims/arbitrary-order/verify_six_blocker_order12_zero_quotient_cofactor_syzygy.py
uv run --with sympy python claims/arbitrary-order/audit_six_blocker_order12_zero_quotient_cofactor_syzygy.py
```

The primary verifier checks every cofactor coefficient, the exact rank-134
linear system, all local ranks and profiles, and every incident block.  The
no-import audit reconstructs the 729 coefficients and the local contractions
with separate rational routines.  No finite-field inference is used.
