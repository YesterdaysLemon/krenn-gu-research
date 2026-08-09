# Common-port `1+1+1` Frobenius reduction for `P_6`

## Status

This is an exact characteristic-zero reduction for the common-port
five-root/six-blocker profile in which the three exceptional modes miss the
three different target colours.  It converts the three overlapping pure
`P_5` deletions into one degree-two/degree-three Frobenius incidence.

The reduction does **not** exclude the profile or prove
`P_6` does not restrict to `Delta_3`.  An explicit integer example satisfies
the complete exceptional-plane and linear Frobenius rank conditions, so a
dimension count or pair-product argument alone cannot finish the case.  The
remaining issue is a marked triple-product factorisation for the three full
modes.

A subsequent exact checkpoint shows that the forbidden quadratic span can
drop further from six to five while the marked quotient remains
three-dimensional.  It extracts from the first nonlinear shared-factor
condition a necessary rank-two `5 x 5` bilinear catalecticant and sixteen
explicit gate forms.  Thus the rank-six example below is not a lower bound on
`dim K`; see
[`P6_COMMON_PORT_111_RANK_FIVE_CATALYTICANT_CHECKPOINT.md`](P6_COMMON_PORT_111_RANK_FIVE_CATALYTICANT_CHECKPOINT.md).

## The three overlapping pure deletions

Work in the squarefree Frobenius algebra

```text
R=C[X_0,...,X_4]/(X_0^2,...,X_4^2),
tau:R_5 -> C,
tau(X_0 X_1 X_2 X_3 X_4)=1.                           (1)
```

Then

```text
tau(v_0 v_1 v_2 v_3 v_4)
```

is the order-five permanent form.  In the common-port `1+1+1` profile,
contracting exceptional mode `E_c` in its missing target colour uses the
common source port and leaves a coordinate `P_5`.  The other two exceptional
root maps have rank two, while the three full root maps have rank three.

Normalize the exceptional root maps as

```text
E_0=(0,x_01,x_02),
E_1=(x_10,0,x_12),
E_2=(x_20,x_21,0),                                    (2)
```

where each displayed nonzero pair is independent in `R_1`.  Let the three
full root maps have marked bases

```text
A=(a_0,a_1,a_2),
B=(b_0,b_1,b_2),
C=(c_0,c_1,c_2).                                      (3)
```

The three port contractions say exactly

```text
(E_1,E_2,A,B,C) P_5 = lambda_0 e_0^5,
(E_0,E_2,A,B,C) P_5 = lambda_1 e_1^5,
(E_0,E_1,A,B,C) P_5 = lambda_2 e_2^5,
lambda_0 lambda_1 lambda_2 != 0.                       (4)
```

These are three pure tensors on overlapping five-mode systems.  They do not
form a `P_5 -> Delta_3` restriction: each deletion uses a different pair of
exceptional modes.

## Nine forbidden quadrics and three marked quadrics

The degree-two/degree-three Frobenius pairing

```text
R_2 x R_3 -> R_5 -> C                                 (5)
```

is perfect.  Define the nine quadrics

```text
K=span{
  x_10 x_21, x_12 x_20, x_12 x_21,
  x_01 x_20, x_02 x_20, x_02 x_21,
  x_01 x_10, x_01 x_12, x_02 x_10
} subset R_2,                                         (6)
```

and the three marked quadrics

```text
q_0=x_10 x_20,
q_1=x_01 x_21,
q_2=x_02 x_12,
Z=span(q_0,q_1,q_2).                                  (7)
```

For a full-mode target word `(i,j,k)`, put

```text
w_ijk=a_i b_j c_k in R_3.                             (8)
```

Every generator of `K` selects a nondiagonal pair of exceptional target
colours in one of the three identities (4).  Therefore

```text
tau(K w_ijk)=0                  for every i,j,k.       (9)
```

The three marked products select the only potentially nonzero exceptional
pair in their respective identities.  Thus

```text
tau(q_d w_ijk)=0                unless i=j=k=d,
tau(q_d w_ddd)=lambda_d != 0.                         (10)
```

In particular, the classes of `q_0,q_1,q_2` are independent modulo `K`.
Since `dim R_2=10`, writing `r=dim K` gives

```text
r <= 7.                                               (11)
```

## Necessary-and-sufficient triple-product normal form

Take Frobenius orthogonals

```text
H=K^perp subset R_3,
L=(K+Z)^perp subset H.                                (12)
```

The independence just proved gives

```text
dim H=10-r,
dim L=7-r,
dim(H/L)=3.                                           (13)
```

Equations (9)--(10) are equivalent to the following marked
triple-product conditions:

1. every one of the 27 products `w_ijk` lies in `H`;
2. every mixed product, with `(i,j,k)` not constant, lies in `L`; and
3. the three diagonal classes

   ```text
   [w_000], [w_111], [w_222] in H/L                  (14)
   ```

   form the basis Frobenius-dual to `[q_0],[q_1],[q_2]`.

Necessity is (9)--(10).  Conversely, (12)--(14) recover every coefficient in
the three tensors (4), so this is also sufficient for that pure-deletion
subsystem.  It is not sufficient for the remaining mixed coefficients of the
original six-mode restriction.

This isolates the next exact lemma.  One must classify three marked
three-planes in `R_1` whose 27 squarefree cubic products lie in `H`, whose 24
mixed products collapse into `L`, and whose three diagonal products remain
independent modulo `L`.

For example:

- if `r=7`, then `L=0`; all 24 mixed cubic products must vanish;
- if `r=6`, then `L` is one line; all 24 mixed cubic products must be
  proportional to one cubic while the diagonal products span the quotient.

## The linear Frobenius obstruction is sharp

The following six integer vectors, listed in the order
`x_01,x_02,x_10,x_12,x_20,x_21`, give an exact example:

```text
x_01=( 0, 0,-1,-1, 0),
x_02=( 0, 1, 0, 0,-1),
x_10=(-1, 0, 0, 1, 0),
x_12=( 0, 1, 0, 0,-1),
x_20=( 0, 1, 0,-1, 0),
x_21=(-1, 0,-1, 0, 0).                               (15)
```

Each pair in (2) has rank two.  Exact rational row reduction gives

```text
dim K=6,
dim(K+Z)=9.                                           (16)
```

Hence the three marked classes are independent, `H` has dimension four, and
`L` is a line.  Perfect Frobenius duality then supplies three cubic vectors
in `H` with the diagonal pairing table (10), while every vector in `L`
satisfies all twelve exceptional quadratic annihilations.  Thus all linear
pairing and dimension requirements of (9)--(13) are simultaneously
consistent over `C`: use those three dual vectors for
`w_000,w_111,w_222` and set all 24 mixed `w_ijk` to zero.

The example deliberately does **not** provide factorizations

```text
w_ijk=a_i b_j c_k.                                    (17)
```

That nonlinear, shared-factor condition is exactly what remains.  Therefore
an argument using only the dimensions of `K`, `H`, `L`, or the perfect
Frobenius pairing cannot exclude `1+1+1`.

## Why the existing certified theorems do not close it

Each pure `P_5` tensor in (4) has local root ranks

```text
(2,2,3,3,3).                                          (18)
```

The decomposable-`P_4` rank-drop theorem applies only after a source
contraction produces an embedded decomposable `P_4`; even then, its required
two rank-two modes are already the two exceptional maps in (18), so the
bound is sharp rather than contradictory.

The two-singleton `P_5` obstruction also does not apply.  Before port
contraction, each exceptional map has only one singleton port pullback.
After contracting the port, the missing columns of the other exceptional
maps become zero columns, not two distinct singleton source rows in one
mode.

Thus the certified `P_4`/`P_5` results stop precisely before the marked
triple-product incidence (12)--(17).

## Replay

Run:

```text
python claims/p6/verify_p6_common_port_111_frobenius_reduction.py
python claims/p6/audit_p6_common_port_111_frobenius_reduction.py
```

The primary verifier builds squarefree products over `Q`, reconstructs the
nine/three coefficient table, checks (16), computes `H` and `L`, and produces
an exact dual cubic basis.  The independent audit uses subset dictionaries
and modular row reduction over `F_3`, `F_5`, and `F_7`.  These programs audit
the reduction and its sharp linear relaxation; they do not claim a
factorization (17) or an unrestricted `P_6` result.
