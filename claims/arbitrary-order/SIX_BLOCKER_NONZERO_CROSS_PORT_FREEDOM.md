# Nonzero exchanged-root coupling leaves the two maximal-overlap ports locally free

## Status

**Exact characteristic-zero local structural theorem.**  Consider two
five-root, six-blocker first-surplus configurations in one twelve-vertex
local system.  Suppose their root sets share four roots and their six blocker
vertices agree, but the two exchanged roots have nonzero mutual coupling.
Then the four common-root incident covectors at each exchanged vertex span at
most one dimension.  This is a genuine concentration forced by the two port
conditions.  It does **not**, however, identify the two port rows at any
shared blocker: evaluation of an edge block on an exchanged root and on its
port is surjective onto an arbitrary pair of blocker covectors.

Consequently the local root, port, blocker-profile, and incident-edge-block
data do not force the two extracted `P_6` tensors to agree, to be
proportional, or to be related by a common output change of basis.  An exact
rational model below realizes the strongest catalogue pair

```text
three_missing_singletons  versus  all_full
```

with nonzero exchanged-root coupling and gives two nonproportional `P_6`
pullbacks.  This model is deliberately only local.  It does **not** specify
the blocker--blocker edges and does **not** satisfy the full
perfect-matching-polynomial-equals-GHZ identity.  Therefore it is not a
counterexample to Krenn--Gu.  Global matching compatibility, five-blocker
overlap, and arbitrary-order local-to-global gluing remain **UNKNOWN**.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## Setup and the forced rank-one concentration

Let

```text
I={0,1,2,3},       R=I union {a},       R'=I union {b},
B={u_0,...,u_5}.
```

The unique outside nonblocker for `R` is `b`, with torus port vector `z_b`;
the unique outside nonblocker for `R'` is `a`, with torus port vector `z_a`.
Write

```text
H_b=span{B_ib(x_i,-):i in I},       ell_b=B_ab(x_a,-),
H_a=span{B_ia(x_i,-):i in I},       ell_a=B_ba(x_b,-).
```

Put `beta=B_ab(x_a,x_b)` and suppose `beta != 0`.  Since `I union {b}` is a
zero-coupled root set, every covector in `H_b` vanishes on `x_b`.  The port
condition says that both `H_b` and `ell_b` vanish on `z_b`, whereas

```text
ell_b(x_b)=beta != 0.                                (1)
```

Thus `x_b,z_b` are independent and

```text
H_b subset Ann(span{x_b,z_b}),       dim H_b <= 1.   (2)
```

The same argument with `a,b` reversed gives `dim H_a <= 1`.  If `H_b` is
nonzero, then it equals `Ann(span{x_b,z_b})`; if in addition the full
nonblocker covector space is `H_b+<ell_b>`, that space has rank two and its
kernel is exactly `<z_b>`.  The symmetric statement holds at `a`.

This conclusion is basis-free.  In coordinates with `x_b=e_0,z_b=e_1`, its
normal form is simply

```text
H_b subset <(0,0,1)>,       ell_b=(beta,0,gamma).    (3)
```

## Why concentration supplies no second blocker constraint

Let `x,z` be independent vectors in a three-dimensional space `V`, and let
`U` be a blocker space.  For arbitrary prescribed covectors `r,s in U^*`,
choose `alpha,zeta in V^*` with

```text
alpha(x)=1, alpha(z)=0,       zeta(x)=0, zeta(z)=1.
```

Then the bilinear edge block

```text
W(v,w)=alpha(v) r(w)+zeta(v) s(w)                    (4)
```

satisfies `W(x,-)=r` and `W(z,-)=s`.  Hence

```text
Bil(V,U) -> U^* x U^*,       W |-> (W(x,-),W(z,-))   (5)
```

is surjective.  Applied independently on the edges `a--u` and `b--u` for
each shared blocker `u`, (5) says that the root row and port row are locally
arbitrary even after (1)--(3) have been imposed at the exchanged vertices.
The cross edge controls the two port kernels at `a,b`; it transmits no
automatic row identity through the blocker modes.

For a genuine GHZ witness the two concise diagonal coefficient triples would
be

```text
lambda_c^R
 =z_b[c] x_a[c] product_(i in I) x_i[c],

lambda_c^R'
 =z_a[c] x_b[c] product_(i in I) x_i[c].             (6)
```

Their coordinatewise ratio is

```text
x_a[c] z_b[c] / (z_a[c] x_b[c]),                    (7)
```

which is not forced to be independent of `c`.  Any further relation between
the two `P_6` restrictions must therefore use the global matching identity,
not only the maximal-overlap port and covector data.

## Exact local countermodel to automatic proportionality

Take all six root vectors equal to

```text
x=(1,1,1),       z_a=(1,2,3),       z_b=(1,3,2).
```

Set

```text
h_a=(1,-2,1),             h_b=(-1,-1,2),
alpha_a=(2,-1,0),         zeta_a=(-1,1,0),
alpha_b=(3/2,-1/2,0),     zeta_b=(-1/2,1/2,0).
```

Here `h_a` annihilates `x,z_a`, `h_b` annihilates `x,z_b`, and the
`alpha,zeta` pairs are the dual sections used in (4).  On the cross edge use

```text
W_ab=alpha_a alpha_b^T.
```

Then

```text
x^T W_ab x=1,       x^T W_ab z_b=0,
z_a^T W_ab x=0.                                      (8)
```

Thus `beta=1`, while `z_b` and `z_a` satisfy the opposite port-kernel
conditions.  On each common-root edge to `a` use `e_0 h_a^T`, and on each
common-root edge to `b` use `e_0 h_b^T`.  Common-root pairs may use
`diag(1,-1,0)`.  All these blocks are nonzero, all required root pairs are
zero-coupled, and the two exchanged nonblocker spaces have row spans

```text
<h_b,alpha_b> with kernel <z_b>,
<h_a,alpha_a> with kernel <z_a>.                     (9)
```

Now list the root covectors at a blocker in the order `I,a,b`.  Use

```text
u_0:
 e_1, e_2, e_1+e_2, e_1+2e_2, e_1-e_2, e_0,

u_1:
 e_0, e_2, e_0+e_2, e_0+2e_2, e_0-e_2, e_1,

u_2:
 e_0, e_1, e_0+e_1, e_0+2e_1, e_0-e_1, e_2,

u_3,u_4,u_5:
 e_0, e_1, e_2, e_0+e_1+e_2,
 e_0+2e_1+3e_2, 3e_0+2e_1+e_2.                    (10)
```

Deleting row `b` gives profiles `(6,5,3,7,7,7)` and root-map ranks
`(2,2,2,3,3,3)`.  Deleting row `a` gives six full profiles and rank three
at every blocker.  Choose the left port-`b` rows

```text
(1,1,0), (0,1,1), (1,0,1), (2,1,1), (1,3,1), (1,1,4),
```

and the right port-`a` rows

```text
(0,1,2), (2,0,1), (1,2,0), (1,1,2), (2,1,1), (1,2,1).             (11)
```

Formula (4) realizes every root/port pair in (10)--(11) by one honest
nonzero exchanged-root--blocker edge block.  Every resulting six-row local
map has rank three.

Contract `P_6` through those six local maps.  In lexicographic target-word
order, exact subset-permanent evaluation gives

```text
                         word 000001    word 000010
left restriction              12             12
right restriction             18             14.
```

The proportionality minor is

```text
12*14-12*18=-48 != 0.                                  (12)
```

Both tensors have 476 nonzero coefficients, and all `3^6=729` coefficients
are checked by the replay scripts.  There is not even one common linear map
`S` on the six source labels with

```text
S M_u^R=M_u^R'       for every u in B:                (13)
```

the combined rational linear system for the 36 entries of `S` has coefficient
rank 36 and augmented rank 37.  The local GHZ triples from (6) are `(1,3,2)`
and `(1,2,3)`, also nonproportional.  These calculations refute an automatic
second `P_6` relation at the local-data level; they do not assert that either
tensor equals its indicated GHZ diagonal.

## Exact residual

The nonzero-cross maximal-overlap branch now has a precise boundary:

```text
local port/covector/incident-block implication: disproved;
global perfect-matching compatibility of the two restrictions: UNKNOWN;
five-blocker overlap or additional residual ports: UNKNOWN;
arbitrary-order local-to-global reduction: UNKNOWN.
```

Any successful gluing theorem must use perfect matchings involving vertices
outside each six-blocker restriction, or another genuinely global invariant.
The rank-one concentration (2) alone cannot provide that missing relation.

## Replay

```text
uv run --with sympy python claims/arbitrary-order/verify_six_blocker_nonzero_cross_port_freedom.py
uv run --with sympy python claims/arbitrary-order/audit_six_blocker_nonzero_cross_port_freedom.py
```

The primary verifier checks the basis-free normal form, the universal edge
evaluation section, the explicit cross and incident blocks, both blocker
profile systems, the inconsistency of (13), all local ranks, and every `P_6`
coefficient over `Q`.  The no-import audit uses alternate dual sections and
an independent subset permanent implementation.  No finite-field inference
is used.
