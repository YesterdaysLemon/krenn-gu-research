# An exact rank-two family compressing `P_4` to a pure tensor

## Status

This is an exact construction over `C`.  It proves that the rank-drop
theorem in
[`P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md`](P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md)
is sharp.

There are four rank-two maps

```text
L_r : C^4 -> C^2,   r=0,1,2,3,
```

for which

```text
(L_0 tensor L_1 tensor L_2 tensor L_3) P_4
  = lambda x_0 tensor x_1 tensor x_2 tensor x_3,
lambda != 0.                                           (1)
```

In fact the maps form a five-parameter family.  This does not produce a
restriction `P_5 -> Delta_3` or resolve the Krenn--Gu prize conjecture.
It shows that one rare deleted-`P_4` slice in `q5_311` cannot be excluded
in isolation: the simultaneous compatibility of the two deletions is
essential.

## Coefficient convention

Write the two coordinate rows of `L_r` as

```text
U_r,V_r in (C^4)^*,
L_r(e_s)=U_r[s] x_r + V_r[s] y_r.
```

For a target word `b in {0,1}^4`, select row `U_r` when `b_r=0` and row
`V_r` when `b_r=1`.  The coefficient of the corresponding target basis
tensor is the permanent of the resulting `4 x 4` matrix.

## The family

Choose parameters

```text
e != 0,  i != 0,  l,j,c arbitrary,  c+e*i*l != 0,
```

and abbreviate

```text
g=e*i*l.
```

Set

```text
U_0=(0,1,(c+g)/e,c)
U_1=(0,0,1,e)
U_2=(0,1,0,g)
U_3=(1,0,i,0)

V_0=(1,j,0,-e*i*(1+l*j))
V_1=(l,1,-i*l,-g)
V_2=(-1/i,0,1,0)
V_3=(0,0,-1/e,1).                                    (2)
```

Then direct permanent expansion gives

```text
coefficient(0000)=2(c+e*i*l),
coefficient(b)=0 for every nonzero b in {0,1}^4.       (3)
```

The four local maps all have rank two.  For `L_0,L_1,L_2,L_3`,
respectively, the row-pair minors on source-column pairs

```text
(0,1), (1,2), (1,2), (0,3)
```

are `-1,-1,1,1`.

## An integer point

The choice

```text
e=i=l=1,   j=c=0
```

gives

```text
U_0=(0,1,1,0)       V_0=(1,0,0,-1)
U_1=(0,0,1,1)       V_1=(1,1,-1,-1)
U_2=(0,1,0,1)       V_2=(-1,0,1,0)
U_3=(1,0,1,0)       V_3=(0,0,-1,1),
```

and hence

```text
(L_0 tensor L_1 tensor L_2 tensor L_3)P_4
  = 2 x_0 tensor x_1 tensor x_2 tensor x_3.            (4)
```

All 15 other coefficients vanish as integer identities.

## Verification

Run:

```text
python verify_p4_decomposable_rank_two_family.py
python audit_p4_decomposable_rank_two_family.py
```

The primary verifier expands all 16 permanents symbolically for the
five-parameter family and checks four explicit nonzero rank minors.  The
independent audit uses a different dynamic-programming permanent
implementation on the integer point, checks the 16 exact integer
coefficients, and verifies local rank two without importing the primary
code.
