# A nonzero diagonal cofactor core whose `P_6` image misses the torus

## Status

**Exact characteristic-zero local construction and fixed-core obstruction.**
There are six rank-two common-row matrices and fifteen nonzero
blocker--blocker edge blocks whose four-root cofactor is the nonzero diagonal
tensor

```text
-1536 e_0^6+1536 e_1^6.                               (1)
```

Thus the quotient-zero condition `C_I in mathcal D` survives with a nonzero
diagonal cofactor, not only with the zero cofactor constructed previously.
The data extend to a twelve-vertex local system in which all 66 pair blocks
are nonzero and both five-root deletion profiles are full.

Nevertheless this common-row core cannot support a concise diagonal `P_6`.
Its off-diagonal cofactor kernel has dimension 27, but the diagonal image of
that kernel is exactly the line spanned by `(-1,1,0)`, which misses the target
coordinate torus.  Every diagonal six-row permanent obtained by appending
arbitrary two rows therefore has zero third coefficient.

The displayed twelve-vertex data are not global: a mixed endpoint has an
off-diagonal coefficient equal to `4`.  This theorem neither constructs nor
excludes any other synchronized `P_6` family.  Arbitrary ambient/source and
projective realizability remain **UNKNOWN**, and the global Krenn--Gu
conjecture remains **UNRESOLVED**.

## The six common-row matrices

On the first four modes use the two-colour four-cycle:

```text
H_u[root,0]=1 iff root=u,
H_u[root,1]=1 iff root=u+1 mod 4,
H_u[root,2]=0,                       u=0,1,2,3.         (2)
```

On the last two modes use

```text
H_4 = [ 0 -4  4;  2 -3  2;  2  5 -6;  2  1 -2],
H_5 = [-1  0 -4; -2 -4  0;  0 -2  4;  0  1 -2].      (3)
```

All six matrices have rank two.  The first four are the standard alternating
four-cycle restriction of `P_4` to `Delta_2`: their all-zero and all-one
permanents are one, and all other target words vanish.

For this core define the cofactor map `Lambda_H` exactly as in
[`SIX_BLOCKER_ORDER12_ZERO_QUOTIENT_CORE_NO_CONCISE_P6.md`](SIX_BLOCKER_ORDER12_ZERO_QUOTIENT_CORE_NO_CONCISE_P6.md):

```text
[w]Lambda_H(W)
 =sum_(u<v) W_uv[w_u,w_v]
   per([H_m[root,w_m]]_(root=0,...,3; m notin {u,v})). (4)
```

## Fifteen nonzero blocks

The following integer blocks are all nonzero:

```text
W_01=[1478  128    0; 1007  980    0;    0    0    0]
W_02=[-128  384    0; -980 -120    0;    0    0    0]
W_03=[-384  356    0;  120 1478    0;    0    0    0]
W_04=[ 640  784 -784;  234 1225 -1374;   0    0    0]
W_05=[ 100 -384 1296; 1672 3772 -1240;   0    0    0]

W_12=[ 980  120    0;  298 -512    0;    0    0    0]
W_13=[-120 -1478   0;  512 -128    0;    0    0    0]
W_14=[-2248 1796 -640; -340 -2130 2428;  0    0    0]
W_15=[ 342  256 1240;  256  980 -680;    0    0    0]

W_23=[-512  128    0;  384 -384    0;    0    0    0]
W_24=[-256  640 -640; -512    0 1152;    0    0    0]
W_25=[-256 -384 -512;  384 -128  384;    0    0    0]
W_34=[-256 -384 -384; -640  640 -640;    0    0    0]
W_35=[-384 -256  384;  256  384  128;    0    0    0]
W_45=[ 576 1536 2304; -256  512 -512; -416 -512 -640]. (5)
```

Direct evaluation of all 729 target words gives

```text
Lambda_H(W)=-1536 e_0^6+1536 e_1^6.                  (6)
```

There are 80 nonzero displayed entries.  The zeros inside individual blocks
do not matter: every one of the fifteen edge blocks itself is nonzero.

## Exact kernel and diagonal image

Let `Lambda_H^off` delete the three constant target words.  Exact sparse
rational row reduction gives

```text
rank_Q(Lambda_H^off)=108,
dim_Q ker(Lambda_H^off)=27.                            (7)
```

Appending the three diagonal coefficient rows raises the rank only once:

```text
rank_Q(Lambda_H)=109.                                  (8)
```

Consequently the diagonal image of the off-diagonal kernel is
one-dimensional.  The nonzero vector (6) spans it, so

```text
Lambda_H(ker Lambda_H^off) intersect mathcal D
 =span{(-1,1,0)}.                                     (9)
```

In particular this line has empty intersection with `(C^*)^3`.

Append arbitrary exchanged rows `a_u,b_u in C^3` to each `H_u`.  The exact
two-row Laplace identity from the preceding fixed-core theorem is

```text
Pi_H(a,b)=Lambda_H(W(a,b)),
W_uv(a,b)=a_u^T b_v+b_u^T a_v.                        (10)
```

If `Pi_H(a,b)` is diagonal, then `W(a,b)` lies in the off-diagonal kernel.
Equation (9) forces its coefficient vector to be a multiple of `(-1,1,0)`.
It is therefore never concise.  This excludes every exchanged-row choice and
every pair of exchanged pencils for this fixed core.

## Full local twelve-vertex realization

Take all six root vectors equal to

```text
x=(1,1,1),
```

and take torus ports

```text
z_a=(1,2,3),       z_b=(1,3,2).                       (11)
```

Use the same nonzero zero-coupled root--root, common-to-exchanged, and cross
blocks as in the zero-cofactor local theorem.  In particular the exchanged
cross form has `beta=1`, both mixed values zero, and `delta=0`.

At blocker modes zero through three append the row `n_u=(0,0,1)`; at modes
four and five append `n_u=(1,0,0)`.  Use `n_u` for both exchanged root rows
and both port rows.  Each `n_u` lies outside the row span of `H_u`, so

```text
rank[H_u;n_u]=3,
profile[H_u;n_u]=7                  for every u.       (12)
```

The standard two-point interpolation blocks realize the same `n_u` at the
root and port vector.  Zero common-root covectors are realized by nonzero
blocks whose contraction by `x` vanishes.  Together with (5), this gives a
nonzero block on every one of the `binom(12,2)=66` pairs.

This remains only local.  At the mixed endpoint the appended rows are both
`n_u`, and direct expansion gives

```text
[000200]Pi_H(n,n)=4 !=0.                               (13)
```

The word is off diagonal, while its global diagonal target coefficient is
zero.  Thus the full matching identity is not realized.

## Exact residual

```text
nonzero C_I in the GHZ diagonal plane with all 15 blocker blocks: REALIZED;
full local twelve-vertex nonzero-edge system: REALIZED;
diagonal kernel image meeting the coefficient torus for this core: NO;
concise diagonal P_6 for this core: NO;
other quotient-zero common-row cores: UNKNOWN;
global matching identity for the displayed local system: FALSE;
global Krenn--Gu conjecture: UNRESOLVED.
```

The refined common-core invariant is now

```text
K_H=ker(Lambda_H^off),
J_H=Lambda_H(K_H) subset mathcal D.                    (14)
```

A viable quotient-zero surface needs `J_H` to meet the coefficient torus.
The zero-cofactor core has `J_H=0`; the present core has
`J_H=span(-1,1,0)`.  Neither is viable.

## Replay

```text
python claims/arbitrary-order/verify_six_blocker_order12_nonzero_diagonal_cofactor_no_torus_p6.py
python claims/arbitrary-order/audit_six_blocker_order12_nonzero_diagonal_cofactor_no_torus_p6.py
```

The primary verifier uses exact rational arithmetic for (6)--(9), checks all
729 coefficients, reconstructs all local ranks and nonzero pair-block
categories, and checks (13).  The independent audit uses finite fields only
to audit the two displayed rational ranks and independently rechecks the
integer tensor.  No finite-field output is used as the characteristic-zero
proof.
