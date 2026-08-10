# Direction-plane obstruction for adjacent one-cross normalized `q4_211`

## Status

This note exactly excludes the full-direction-plane gate in the
adjacent one-cross branch of normalized `q4_211` over `C`.

Assume

```text
b c != 0
```

and let `A` be an `h_1,h_2` common mode in one of the two one-cross
orientations.  Let `Y` be the opposite-pencil mode forced by the
normal-pencil theorem.  Then no other mode can contain

```text
span(u_1,u_2).                                      (1)
```

On `abc != 0`, the two-gate theorem consequently leaves only

```text
L_A(e_1+e_2)=0
or
L_Y(e_1+e_2)=0.                                     (2)
```

This is an exact gate exclusion whenever the gate is present, not an
exclusion of (2), all normalized `q4_211`, or the parameter boundaries
`b=0`, `c=0`,
`P_5 -> Delta_3`, or the global Krenn--Gu conjecture.

## The direction rows have fixed target colours

Put

```text
E=span(e_1,e_2),
H_0=span(e_1+e_2,e_1-e_2,e_0-b e_3-c e_4).
```

The annihilator of `H_0` is

```text
H_0^perp=span(u_1,u_2).                             (3)
```

Suppose a remaining mode `Z` contains the plane (1), and write

```text
L_Z^* alpha=u_1,
L_Z^* beta =u_2.                                    (4)
```

The conic contraction used in the direction-conic theorem has nonzero
image `e_0 tensor e_0` through its two remaining modes.  Since (3)--(4)
make `L_Z|H_0` rank one, its image line is therefore exactly

```text
L_Z(H_0)=C e_0.                                     (5)
```

Both covectors in (4) annihilate this line:

```text
alpha[0]=beta[0]=0.                                 (6)
```

They are independent because pullback is injective and `u_1,u_2` are
independent.

Now contract the original tensor identity in two symmetric ways.  At
the distinguished mode use `u_1`, at `Z` use `u_2`, and then interchange
the two rows.  The source contraction is the same tensor

```text
(u_1,u_2) contract P_5
 =P_3(e_1,e_2,e_0+b e_3+c e_4).                    (7)
```

The two target contractions are

```text
lambda_1 beta[1] e_1^3,
lambda_2 alpha[2] e_2^3.                            (8)
```

They are equal.  Since the two displayed pure tensors are independent
and both diagonal coefficients are nonzero,

```text
beta[1]=alpha[2]=0.                                 (9)
```

Equations (6), (9), and independence give, up to nonzero scale,

```text
alpha=e_1^*,
beta =e_2^*.                                        (10)
```

Thus the two directions at `Z` have their original target colours;
there is no residual target shear.

## The `q` orientation

In the `q` orientation,

```text
h_2=L_A^* e_0^*
```

up to scale, while `h_1` pulls back from a covector

```text
x_A=(r,0,q),   q != 0.
```

Both `h_1,h_2` annihilate `E`, so their target covectors imply

```text
L_A(E) subset C e_1.                               (11)
```

The opposite-pencil theorem supplies a distinct mode `Y` containing

```text
span(h_1,n),
n=(0,0,0,c,b).
```

Every occurrence of `n` pulls back from target `e_0^*`.  If
`L_Y^*x_Y=h_1`, the zero contraction

```text
(u_1,h_1) contract P_5=0
```

forces `x_Y[1]=0`.  Independence from the `n` row forces
`x_Y[2] != 0`.  Hence the same common-annihilator argument gives

```text
L_Y(E) subset C e_1.                               (12)
```

Repeat the colour-two direction at the distinguished mode and at `Z`.
By (10), the target contraction through the three remaining modes is
nonzero:

```text
(tensor over A,Y,W)
 ((u_2,u_2) contract P_5)
   =nonzero scalar * e_2 tensor e_2 tensor e_2.     (13)
```

On the source,

```text
(u_2,u_2) contract P_5
 =2c P_3(e_1,e_2,e_3).                              (14)
```

Every monomial in (14) assigns the unique factor `e_3` to only one of
the three modes `A,Y,W`.  At least one of `A,Y` therefore receives a
factor in `E`.  By (11)--(12), that factor has zero target-colour-two
coordinate.  Thus the coefficient of `e_2 tensor e_2 tensor e_2` in
the left side of (13) is zero, contradicting (13).

## The `p` orientation

Interchanging singleton colours gives the identical argument.  Now the
common mode and the forced `span(h_2,n)` mode both satisfy

```text
L_A(E),L_Y(E) subset C e_2.
```

Equations (6)--(10) still fix the two direction colours.  Repeating
`u_1` gives

```text
(u_1,u_1) contract P_5
 =2b P_3(e_1,e_2,e_4)
 -> nonzero scalar * e_1^3.
```

At least one of `A,Y` receives an `E` factor, whose target-colour-one
coordinate is zero.  The required pure coefficient again vanishes.
This excludes (1) in both orientations.

## Consequence

On `abc != 0`, the generic normalized incidence analysis is now:

- parallel minimal incidence reselects as adjacent;
- exact disjoint incidence is impossible;
- adjacent two-cross incidence is impossible;
- the full-direction-plane gate in adjacent one-cross incidence is
  impossible; and
- every surviving adjacent one-cross configuration lies on the sole
  common-kernel divisor (2).

The remaining generic task is therefore kernel propagation, rather
than a Grassmannian or ambient-map search.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q4_211_one_cross_direction_plane.py
python claims/p5/frontier/audit_p5_q4_211_one_cross_direction_plane.py
```

The primary verifier differentiates (7), (14), and its colour-swapped
counterpart, checks (3), and expands the forbidden pure coefficients.
The independent audit reconstructs the contractions and the
two-dimensional target-covector argument over `F_5,F_7`.  It enumerates
no ambient maps or Grassmannians.  The finite-field calculations audit
the formulas; the proof above is over `C`.
