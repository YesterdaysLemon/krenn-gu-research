# Rank-five boundary and catalecticant gates for common-port `1+1+1`

## Status

This is an exact characteristic-zero checkpoint for the nonlinear incidence
isolated in
[`P6_COMMON_PORT_111_FROBENIUS_REDUCTION.md`](P6_COMMON_PORT_111_FROBENIUS_REDUCTION.md).
It proves two new facts and feeds one later exact obstruction.

1. The nine forbidden exceptional quadrics can have rank **five**, not merely
   the previously exhibited rank six, while the three marked classes remain
   independent modulo their span.  Thus any attempted proof that starts by
   asserting `dim K >= 6` is false.
2. For this sharp rank-five configuration, the first nonlinear requirement
   forces a `5 x 5` bilinear catalecticant to have rank at most two on a
   product of two projective planes.  Twenty-two of its determinantal
   equations split into sixteen explicit bilinear gates.  Irreducibility
   reduces these necessary equations to 53 minimal gate covers, with a unique
   cover of size four.

The unique size-four branch is excluded in the follow-up theorem
[`P6_COMMON_PORT_111_UNIQUE_FOUR_GATE_OBSTRUCTION.md`](P6_COMMON_PORT_111_UNIQUE_FOUR_GATE_OBSTRUCTION.md).
This note does **not** construct or exclude the three shared full-mode planes
on the other 52 branches.  Their remaining minors, common kernels, and marked
rank-one conditions are still open.  The checkpoint therefore does not decide
`P_6 -> Delta_3` or the global Krenn--Gu conjecture.

## An exact rank-five exceptional configuration

Work in

```text
R=C[X_0,...,X_4]/(X_0^2,...,X_4^2).
```

In the order `x_01,x_02,x_10,x_12,x_20,x_21`, take

```text
x_01=( 0,-1,-1, 0, 0),
x_02=( 1, 0, 0, 0,-2),
x_10=( 0, 0, 0,-1, 1),
x_12=(-1, 0, 1, 0, 0),
x_20=(-1, 1, 0, 0, 0),
x_21=( 1, 0, 0, 2, 0).                              (1)
```

Each exceptional pair in

```text
E_0=(0,x_01,x_02),
E_1=(x_10,0,x_12),
E_2=(x_20,x_21,0)
```

has rank two.  The six displayed vectors have the balanced relation

```text
x_01+x_02+2x_10+x_12+x_20+x_21=0.                   (2)
```

Let `K` be the span of the same nine forbidden products as in the earlier
reduction and let

```text
q_0=x_10 x_20,
q_1=x_01 x_21,
q_2=x_02 x_12,
Z=span(q_0,q_1,q_2).
```

Exact row reduction over `Q` gives

```text
dim K=5,
dim(K+Z)=8.                                           (3)
```

In particular, the three marked classes are independent modulo `K`.  With
the degree-two/degree-three Frobenius pairing, put

```text
H=K^perp,                 L=(K+Z)^perp.
```

Then

```text
dim H=5,                  dim L=2,                  (4)
dim(H/L)=3.
```

The two-dimensional mixed allowance is not abstract.  It has the following
two decomposable generators:

```text
ell_0=(X_2-2X_4)(X_0-2X_3)(X_1-2X_3),
ell_1=(X_0+X_2)(X_1-2X_4)(X_3+X_4),                 (5)
L=span(ell_0,ell_1).
```

Moreover the three marked quadrics pair surjectively with `H`; exact dual
cubics exist.  Consequently the complete *linear* Frobenius table is again
consistent: use the dual cubics on the three diagonal words and zero on all
mixed words.  Equation (5) shows that even the mixed allowance itself is
spanned by factorizable cubics.  What is missing is one shared
`3 x 3 x 3` grid of linear factors.

## A necessary bilinear catalecticant gate

Use the following five forbidden products as a basis of `K`:

```text
k_0=x_10 x_21,
k_1=x_12 x_20,
k_2=x_12 x_21,
k_3=x_02 x_20,
k_4=x_01 x_10.                                      (6)
```

In the quadratic monomial order

```text
01,02,03,04,12,13,14,23,24,34,
```

their coefficient rows are

```text
( 0, 0,-1, 1, 0, 0, 0, 0, 0, 2),
(-1,-1, 0, 0, 1, 0, 0, 0, 0, 0),
( 0, 1,-2, 0, 0, 0, 0, 2, 0, 0),
( 1, 0, 0, 2, 0, 0,-2, 0, 0, 0),
( 0, 0, 0, 0, 0, 1,-1, 1,-1, 0).                   (7)
```

For linear forms `b,c in R_1`, define the catalecticant

```text
C_K(b,c)_(s,p)=tau(k_s X_p b c),
0<=s,p<=4.                                           (8)
```

Every entry is bilinear in the ten coordinates of `(b,c)`.  If three
full-mode planes `A,B,C subset R_1` satisfy

```text
ABC subset H=K^perp,                                 (9)
```

then, for every `(b,c) in B x C`,

```text
A subset ker C_K(b,c).
```

Since `dim A=3`, this implies the necessary condition

```text
rank C_K(b,c) <= 2       identically on B x C.       (10)
```

Conversely, (9) is equivalent to the existence of one **fixed** three-plane
`A` contained in all these kernels.  The pointwise rank bound (10) alone does
not supply that common plane: its three-dimensional kernels may vary with
`(b,c)`.  Thus (8)--(10) give a necessary determinantal reduction of the
forbidden-quadratic shared-factor problem.  Recovering a common `A` remains a
separate step before the marked quadrics are imposed.

## Twenty-two split minors

All one hundred `3 x 3` minors of (8) must vanish on `B x C`.  A selected set
of twenty-two of them factors exactly as

```text
constant * g_i(b,c) g_j(b,c) g_k(b,c),              (11)
```

where only sixteen distinct bilinear forms `g_0,...,g_15` occur.  The replay
artifact records every row set, column set, scalar, and coefficient matrix,
so (11) is a coefficient identity rather than a numerical factor test.

The four simplest gates are

```text
g_0 =b_3 c_4+b_4 c_3,
g_3 =b_1 c_4+b_4 c_1,
g_5 =b_1 c_2+b_2 c_1,
g_9 =b_2 c_3+b_3 c_2.                               (12)
```

The coordinate ring of the affine space `B x C` is a domain.  Therefore,
whenever one product in (11) vanishes identically on `B x C`, at least one
of its three bilinear factors vanishes identically there.  Choosing gates
that hit all twenty-two triples is a finite hypergraph problem.  Its exact
minimal covers have size distribution

```text
size 4:  1,
size 5:  6,
size 6: 13,
size 7: 14,
size 8: 16,
size 9:  2,
size 10: 1.                                         (13)
```

The unique four-gate cover is exactly

```text
{g_0,g_3,g_5,g_9}.                                  (14)
```

At the time of this checkpoint, every solution of the rank-two catalecticant
condition lay in one of the following exact alternatives:

1. all four cycle gates in (12) vanish on `B x C`; or
2. at least five of the sixteen recorded gates vanish on `B x C`, in one of
   the other 52 minimal-cover patterns.

The first alternative is now impossible: its bilinear zero rectangles are
the two alternating coordinate three-planes, and an explicit remaining minor
has value `-4` or `4` on them.  See
[`P6_COMMON_PORT_111_UNIQUE_FOUR_GATE_OBSTRUCTION.md`](P6_COMMON_PORT_111_UNIQUE_FOUR_GATE_OBSTRUCTION.md).
Every surviving solution must therefore use one of the other 52 covers, each
of size at least five.  One must still classify those zero rectangles, impose
the other determinantal minors, recover a common three-dimensional kernel
`A`, and finally require the three marked forms

```text
(a,b,c) |-> tau(q_d a b c)
```

to be nonzero rank-one tensors whose factor covectors are independent in
all three modes.

## Replay

Run:

```text
uv run --with sympy python verify_p6_common_port_111_rank_five_catalecticant.py
python audit_p6_common_port_111_rank_five_catalecticant.py

uv run --with sympy python verify_p6_common_port_111_unique_four_gate_obstruction.py
python audit_p6_common_port_111_unique_four_gate_obstruction.py
```

The primary verifier performs exact rational row reduction, reconstructs
`H`, `L`, the factorizations (5), marked dual cubics, the catalecticant, all
twenty-two identities (11), and the minimal-cover census (13)--(14).  The
independent audit rebuilds the squarefree products and ranks over several
finite fields, then checks every exported determinant identity with a
separate sparse-polynomial implementation.  The modular checks audit the
integer identities; all theorem statements above are proved over `C` by the
displayed exact algebra and the domain argument.
