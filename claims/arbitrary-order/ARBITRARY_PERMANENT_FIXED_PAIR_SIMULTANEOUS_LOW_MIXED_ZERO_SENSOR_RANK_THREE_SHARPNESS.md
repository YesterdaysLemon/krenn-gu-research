# Arbitrary permanent fixed-pair simultaneous-low mixed-zero sensor-rank-three sharpness

## Status

This note gives an exact rational sharpness fixture for the simultaneous
projection-drop residual left open by
`ARBITRARY_PERMANENT_FIXED_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md`.
For the same fixed equality-five pair, four explicit rank-three local planes
have all of the following properties:

1. both mixed-radical quartic tensors vanish identically;
2. each projection family has a rank-drop mode;
3. the resulting three-output pure sensor has output rank three;
4. after independent changes of local colour bases, all three monochromatic
   pure coefficients are nonzero.

Nevertheless the fixture is **not** a restriction to `Delta_3`.  Its four
input flattening ranks are `(3,1,1,2)`, whereas the nondegenerate diagonal
target has input flattening rank three at every mode.  This obstruction is
invariant under arbitrary local `GL_3` changes, and even under an arbitrary
invertible change of the three-dimensional output space.

Thus simultaneous projection drop, both full mixed tensors zero, sensor
rank three, local rank three, and nonzero monochromatic coefficients do not
by themselves imply a restriction.  The fixture does not satisfy the other
mixed-colour `Delta_3` equations, does not refute permanent nonrestriction,
and does not resolve the global Krenn--Gu conjecture.  The global status
remains **UNRESOLVED**.

## 1. Fixed pair and complementary sensors

Work over `Q` in

```text
Z_6=Q[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

At modes `0,1`, use the fixed pair

```text
u_0=x_0-x_3,      u_1=x_1-x_3,      u_2=x_2-x_3,
v_0=x_1+x_2,      v_1=x_0+x_2,      v_2=x_2-x_3.
```

In edge order `(01,02,03,12,13,23)`, its five product-space basis vectors
are

```text
m_1=(0,1,-1,0,0,-1),       m_2=(0,0,0,1,-1,-1),
d_0=(1,1,0,0,-1,-1),       d_1=(1,0,-1,1,0,-1),
d_2=(0,0,0,0,0,-2).
```

For `q` among these five quadratics, let `T_q` be the complementary
four-linear tensor on modes `2,3,4,5`.  Direct edge complementation gives

```text
star(m_1)= x_4x_5 x_1 (x_3-x_2-x_0),
star(m_2)= x_4x_5 x_0 (x_3-x_2-x_1),

star(d_0)= x_4x_5 (x_1+x_2)(x_3-x_0),
star(d_1)= x_4x_5 (x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5 x_0x_1.
```

Write

```text
Phi_1=(x_1,x_4,x_5,x_3-x_2-x_0),
Phi_2=(x_0,x_4,x_5,x_3-x_2-x_1).
```

## 2. The four rational planes

Let `a_(t,i)` be the following ordered bases, with coordinates in
`(x_0,x_1,x_2,x_3,x_4,x_5)`:

```text
L_2:
  a_20=(1, 0, 0, 1, 0, 0),
  a_21=(0, 1, 0,-1, 0, 0),
  a_22=(0, 0, 1, 1, 0, 0);

L_3:
  a_30=(1, 0, 0, 0, 0, 0),
  a_31=(0, 1, 0, 1, 0, 0),
  a_32=(0, 0, 1,-1,-1, 1);

L_4:
  a_40=(1, 0, 0, 1, 0, 0),
  a_41=(0, 1, 1, 0, 0, 0),
  a_42=(0, 0, 0, 0, 1,-1);

L_5:
  a_50=(0,-1, 1, 0, 0, 0),
  a_51=(0, 1, 0, 1, 0, 0),
  a_52=(0, 0, 0, 0, 1, 1).
```

Each displayed triple has rank three.  Exact row reduction gives the two
projection profiles

```text
(rank Phi_1|L_2,...,rank Phi_1|L_5)=(1,3,2,2),
(rank Phi_2|L_2,...,rank Phi_2|L_5)=(2,2,3,1).              (1)
```

The tuple therefore lies strictly inside the simultaneous-low residual.

## 3. Exact mixed zeros and the five-word sensor

Evaluate the five tensors on all `3^4=81` words in the displayed `a` bases.
Both mixed tensors vanish entrywise:

```text
T_(m_1)=T_(m_2)=0.                                        (2)
```

Put `D=span{d_0,d_1,d_2}`.  The `D^*`-valued sensor, written in the dual
output basis `(d_0^*,d_1^*,d_2^*)`, has only the following five nonzero word
values:

```text
word    (T_d0,T_d1,T_d2)

0220    (0, 4, 4)
0221    (0, 0,-4)
1220    (0,-4, 0)
2220    (0, 4, 0)
2221    (4, 0, 0).                                       (3)
```

Equivalently, if `epsilon_(t,i)` denotes the dual of `a_(t,i)`, the three
fixed output slices factor exactly as

```text
T_d0=4 epsilon_(2,2) tensor epsilon_(3,2)
       tensor epsilon_(4,2) tensor epsilon_(5,1),

T_d1=4 (epsilon_(2,0)-epsilon_(2,1)+epsilon_(2,2))
       tensor epsilon_(3,2) tensor epsilon_(4,2)
       tensor epsilon_(5,0),

T_d2=4 epsilon_(2,0) tensor epsilon_(3,2)
       tensor epsilon_(4,2)
       tensor (epsilon_(5,0)-epsilon_(5,1)).              (4)
```

Thus the full sensor is `sum_c T_dc tensor d_c^*`.

The output flattening has rank three.  Indeed, the mode-`2` factors of the
three slices in (4),

```text
epsilon_(2,2),
epsilon_(2,0)-epsilon_(2,1)+epsilon_(2,2),
epsilon_(2,0),
```

are linearly independent, so the three slice tensors are linearly
independent.  Equivalently, the rows `2221`, `1220`, and `0221` in (3)
isolate `d_0,d_1,d_2`.  Formula (4) is a three-term tensor decomposition,
while output flattening rank three is also a lower bound, so the full
`D^*`-valued tensor has tensor rank exactly three.
Each individual output slice has tensor rank one and multilinear rank
`(1,1,1,1)`.

## 4. Exact nonconciseness and non-Delta conclusion

Across the three summands in (4), the factor directions span dimensions

```text
mode 2: 3,
mode 3: 1,
mode 4: 1,
mode 5: 2.                                                (5)
```

These are exactly the four input flattening ranks of the full `D^*`-valued
tensor.  By contrast, a diagonal tensor with three nonzero coefficients,

```text
sum_(c=0)^2 lambda_c e_c^* tensor e_c^* tensor e_c^*
                       tensor e_c^* tensor d_c^*,
lambda_c!=0,                                             (6)
```

has input flattening rank three in every mode.  Input flattening ranks are
unchanged by local `GL_3` transformations and by invertible transformations
of the output.  Hence no local change of colour bases, with or without an
invertible output change, can transform (3) into (6).

The obstruction is not that the three intended pure coefficients must
vanish.  Define new ordered colour bases by their coordinates in the `a`
bases:

```text
L_2: (a_22,             a_21,             a_20),
L_3: (a_32,             a_32+a_30,        a_32+a_31),
L_4: (a_42,             a_42+a_40,        a_42+a_41),
L_5: (a_51,             a_50,             a_50+a_52).     (7)
```

Every triple in (7) is a basis.  On its three monochromatic words, the
fixed output components are

```text
T_d0(000)=4,             T_d1(111)=-4,
T_d2(222)=4.                                             (8)
```

Thus the fixture has local rank three and all three nonzero monochromatic
coefficients simultaneously.  Other mixed-colour `d_c` entries remain;
(5), not a preferred-basis computation, proves that they cannot all be
removed.

## 5. Exact boundary

```text
fixed equality-five pair:                              YES;
four rank-three complementary local planes:            YES;
both full mixed-radical tensors zero:                   YES;
rank drop in each projection family:                   YES;
three-dimensional output sensor:                       YES;
all three monochromatic coefficients nonzero in bases: YES;
input-concise in all four modes:                        NO, ranks (3,1,1,2);
restriction to Delta_3:                                NO;
counterexample to permanent nonrestriction:            NO;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

The next meaningful survivor gate is therefore not output rank alone.  A
simultaneous-low mixed-zero tuple must at least have output rank three and
input flattening ranks `(3,3,3,3)` before it can be a restriction.

Replay the exact fixture with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_simultaneous_low_mixed_zero_sensor_rank_three_sharpness.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_simultaneous_low_mixed_zero_sensor_rank_three_sharpness.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_simultaneous_low_mixed_zero_sensor_rank_three_sharpness.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_simultaneous_low_mixed_zero_sensor_rank_three_sharpness.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_simultaneous_low_mixed_zero_sensor_rank_three_sharpness.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_simultaneous_low_mixed_zero_sensor_rank_three_sharpness.py
```

The primary verifier uses direct exact square-free multiplication.  The
independent audit uses the factorized complementary quartics, a separate
permanent evaluator, and custom rational row reduction without importing the
primary verifier or SymPy.
