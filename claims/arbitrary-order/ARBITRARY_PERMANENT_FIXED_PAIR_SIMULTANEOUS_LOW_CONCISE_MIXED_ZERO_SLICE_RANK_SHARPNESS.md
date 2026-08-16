# Arbitrary permanent fixed-pair simultaneous-low concise mixed-zero slice-rank sharpness

## Status

This note gives a second exact rational sharpness fixture in the simultaneous
projection-drop residual of the fixed equality-five pair.  It strengthens
`ARBITRARY_PERMANENT_FIXED_PAIR_SIMULTANEOUS_LOW_MIXED_ZERO_SENSOR_RANK_THREE_SHARPNESS.md`
by passing the full conciseness gate:

```text
output flattening rank:       3;
four input flattening ranks: (3,3,3,3).
```

Both mixed-radical quartic tensors vanish identically, every local plane has
rank three, both projection families have low modes, and suitable local
colour bases make all three intended monochromatic coefficients nonzero.

The fixture is still **not** a restriction to `Delta_3`.  Its three fixed
output slices have multilinear ranks

```text
(2,3,3,2), (2,2,3,2), (2,3,2,2),
```

rather than `(1,1,1,1)`.  More strongly, one two-versus-three flattening of
the full five-way tensor has rank nine, so its tensor rank is at least nine;
the nondegenerate three-colour diagonal target has tensor rank three.

This is a boundary witness, not a permanent restriction or a counterexample
to the global conjecture.  The global Krenn--Gu status remains
**UNRESOLVED**.

## 1. Fixed pair and sensor convention

Work over `Q` in the six-variable square-free algebra.  At modes `0,1`, use

```text
u_0=x_0-x_3,      u_1=x_1-x_3,      u_2=x_2-x_3,
v_0=x_1+x_2,      v_1=x_0+x_2,      v_2=x_2-x_3.
```

In edge order `(01,02,03,12,13,23)`, put

```text
m_1=(0,1,-1,0,0,-1),       m_2=(0,0,0,1,-1,-1),
d_0=(1,1,0,0,-1,-1),       d_1=(1,0,-1,1,0,-1),
d_2=(0,0,0,0,0,-2).
```

The complementary quartics are

```text
star(m_1)= x_4x_5 x_1 (x_3-x_2-x_0),
star(m_2)= x_4x_5 x_0 (x_3-x_2-x_1),
star(d_0)= x_4x_5 (x_1+x_2)(x_3-x_0),
star(d_1)= x_4x_5 (x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5 x_0x_1.
```

Write `D=span{d_0,d_1,d_2}`.  The complementary sensor is `D^*`-valued,
with output coordinates in the dual basis `(d_0^*,d_1^*,d_2^*)`.

The two mixed-factor projections are

```text
Phi_1=(x_1,x_4,x_5,x_3-x_2-x_0),
Phi_2=(x_0,x_4,x_5,x_3-x_2-x_1).
```

## 2. Exact rational local planes

In coordinates `(x_0,x_1,x_2,x_3,x_4,x_5)`, take the ordered bases

```text
L_2:
  a_20=(0,1,0,0,-1,0),
  a_21=(0,0,1,0,-1,0),
  a_22=(0,0,0,1, 1,0);

L_3:
  a_30=(1,0,0,0,0,1),
  a_31=(0,1,0,0,1,0),
  a_32=(0,0,1,0,0,1);

L_4:
  a_40=(1,0,0,0, 0,-1),
  a_41=(0,0,1,0, 1, 0),
  a_42=(0,0,0,1,-1, 0);

L_5:
  a_50=(1,1, 0,0, 0,0),
  a_51=(0,0, 1,1, 0,0),
  a_52=(1,0,-1,0,-1,1).
```

Every triple has rank three.  Exact row reduction gives

```text
(rank Phi_1|L_2,...,rank Phi_1|L_5)=(2,2,2,2),
(rank Phi_2|L_2,...,rank Phi_2|L_5)=(1,3,2,2).              (1)
```

Thus the first family is low at all four modes and the second is low at
three modes.

## 3. Exact mixed zeros and conciseness

Let `T_q` be the four-linear complementary tensor for `q`.  Direct exact
evaluation of all `81` words gives

```text
T_(m_1)=T_(m_2)=0.                                        (2)
```

The three fixed output slices are linearly independent.  For example, the
following three words isolate the three dual output coordinates:

```text
word    (T_d0,T_d1,T_d2)

0021    (-2, 0, 0),
0011    ( 0,-2, 0),
0010    ( 0, 0,-2).                                      (3)
```

Hence the output flattening rank is three.  Exact flattening of each input
mode against the other three inputs and `D^*` gives

```text
(rank_2,rank_3,rank_4,rank_5)=(3,3,3,3).                  (4)
```

The sensor is therefore concise at all five factors.

## 4. Slice ranks and the tensor-rank obstruction

For each fixed output coordinate, flatten the corresponding four-way slice
at each input mode.  The exact multilinear ranks are

```text
T_d0: (2,3,3,2),
T_d1: (2,2,3,2),
T_d2: (2,3,2,2).                                         (5)
```

No slice is a rank-one tensor.  Because local `GL_3` changes preserve these
ranks, no local colour bases plus diagonal output scaling can turn the
fixture into a fixed-output diagonal tensor.

There is also a basis-independent obstruction that permits an arbitrary
invertible output change.  Label the five tensor factors

```text
(L_2,L_3,L_4,L_5,D^*).
```

All one-factor flattening ranks are three.  The ten two-factor flattening
ranks are

```text
L_2 L_3: 8,      L_2 L_4: 7,      L_2 L_5: 8,
L_2 D^*: 6,      L_3 L_4: 8,      L_3 L_5: 9,
L_3 D^*: 8,      L_4 L_5: 8,      L_4 D^*: 8,
L_5 D^*: 6.                                             (6)
```

Every matrix flattening rank is a lower bound for five-way tensor rank, so
the `L_3 tensor L_5` flattening proves

```text
tensor rank >=9.                                         (7)
```

The nondegenerate three-colour diagonal tensor is a sum of three rank-one
terms and has output flattening rank three, hence tensor rank exactly three.
Equations (6)--(7) exclude equivalence even under
`GL_3^4 x GL(D^*)`.

## 5. All three monochromatic coefficients can be nonzero

The failure is not caused by a forced zero among the intended pure
coefficients.  Use the following new colour bases, displayed by their row
coordinates in the `a` bases:

```text
L_2: (-1, 1, 1),   ( 0,-1, 0),   (0,0, 1);
L_3: ( 0, 1, 0),   ( 1,-1,-1),   (0,0, 1);
L_4: (-1, 1, 0),   ( 1, 1,-1),   (1,0, 1);
L_5: ( 0, 1, 1),   (-1,-1, 0),   (1,1,-1).               (8)
```

All four coordinate matrices are invertible.  In these bases the intended
monochromatic values are

```text
T_d0(000)=2,             T_d1(111)=2,
T_d2(222)=-2.                                             (9)
```

The mixed-radical tensors remain zero because (2) is a basis-free tensor
identity.  Other fixed-output mixed-colour coefficients survive, as they
must by (5)--(7).

## 6. Exact boundary and next gate

```text
fixed equality-five pair:                              YES;
four rank-three local planes:                          YES;
both full mixed-radical tensors zero:                  YES;
rank drop in each projection family:                   YES;
output rank three:                                     YES;
all four input flattening ranks three:                 YES;
all intended monochromatic coefficients nonzero:      YES;
each fixed output slice rank one:                      NO;
five-way tensor rank three:                            NO, rank at least 9;
restriction to Delta_3:                                NO;
global Krenn--Gu conjecture:                           UNRESOLVED.
```

The next necessary survivor gate is now exact: all three nonzero fixed
slices must have multilinear rank `(1,1,1,1)`, and their three factor lines
must span each local dual three-space.  Those aligned factor bases are
precisely what would turn the mixed-zero sensor into a candidate
`Delta_3` restriction.

Replay the fixture with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_simultaneous_low_concise_mixed_zero_slice_rank_sharpness.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_simultaneous_low_concise_mixed_zero_slice_rank_sharpness.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_simultaneous_low_concise_mixed_zero_slice_rank_sharpness.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_simultaneous_low_concise_mixed_zero_slice_rank_sharpness.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_simultaneous_low_concise_mixed_zero_slice_rank_sharpness.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_simultaneous_low_concise_mixed_zero_slice_rank_sharpness.py
```

The primary verifier uses direct exact square-free multiplication and SymPy
rank computations.  The independent audit uses the factorized quartics, a
separate permanent evaluator, and custom exact rational elimination without
importing the primary or SymPy.
