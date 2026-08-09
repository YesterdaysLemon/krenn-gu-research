# Generic weighted `H22` obstruction on the six-dimensional `P_4` component

## Status

This is an exact characteristic-zero obstruction on the generic
diagonal-source orbit of the six-dimensional pure-compression
component proved in
[`P4_SIX_DIMENSIONAL_PURE_COMPONENT.md`](../../../p4/components/six-dimensional/P4_SIX_DIMENSIONAL_PURE_COMPONENT.md).

Restoring the source-torus slope changes the two `H22` neighbors into
weighted diagonal-hyperplane pencils.  Generically:

1. the `01` pencil has no binary `Delta_2` extension;
2. the `23` pencil has exactly one rational marking pencil and a
   two-dimensional extension kernel; but
3. two mode-zero marked minors exclude every genuine extension from a
   ternary local map.

Thus a relevant pure binary plane cannot be generic on this component
in a hypothetical `H22` restriction.

This does **not** close the slope or parameter divisors omitted by the
function field, the component's projective boundary, the other known
pure components, component exhaustiveness, all of `H22`, or the global
conjecture.

## Weighted diagonal pencils

Use the normalized `H22` contractions

```text
v_0=e_0+e_1,        v_1=e_2+e_3,        v_2=e_4.
```

After putting the pure `P_4` plane configuration into its apolar normal
form, the residual diagonal source torus changes the two neighboring
source bases to

```text
D_01^r(q)=(r q_0+q_1,q_2,q_3,q_4),
D_23^r(q)=(q_0,q_1,r q_2+q_3,q_4).                  (1)
```

The slope `r` belongs in the component function field.  Setting `r=1`
too early gives the valid but exceptional equal-weight boundary in
[`P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md`](P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md);
it does not represent the generic orbit.

## Apolar basis and markings

Over

```text
K=C(s,d,u,v,r)
```

use

```text
alpha_0=(1,0,0,-1)
beta_0 =(0,0,1,1)

alpha_1=(s v,v-u,-s u,d(v-u))
beta_1 =(s,1-u,0,d+u(s-d))

alpha_2=(1,0,-1,0)
beta_2 =(0,1,-s,-d)

alpha_3=(0,0,1,-1)
beta_3 =(1,0,0,1).                                  (2)
```

The only nonzero binary coefficient is

```text
T_1111=2 s u.
```

Every marked representative is

```text
beta_i(t_i)=beta_i+t_i alpha_i.                     (3)
```

Write the fifth-coordinate extensions as

```text
alpha_i -> (alpha_i,x_i),
beta_i(t_i) -> (beta_i(t_i),y_i).                   (4)
```

The sixteen neighboring binary coefficients are linear in

```text
z=(x_0,x_1,x_2,x_3,y_0,y_1,y_2,y_3).
```

## Exact weighted projection

For each pencil, impose the fourteen mixed coefficient equations,
normalize the `0000` diagonal to one, and invert the `1111` diagonal.
Eliminating `(z,w)` gives

```text
D_01^r:  (1),                                       (5)

D_23^r:  t_0,
          (u-v)t_1+u-1,
          (u-v)t_2-sv.                              (6)
```

Thus the `01` direction is already empty at binary level.  The `23`
direction has the single rational sheet

```text
t_0=0,
t_1=(1-u)/(u-v),
t_2=sv/(u-v),
t_3=p arbitrary.                                   (7)
```

This is why the weighted-slope restoration matters: the generic
`23` pencil has a real binary survivor even though its equal-weight
specialization does not.

## The two extension directions

On the open set

```text
s u (r-1)(r+1)(u-1)(u-v)(pr-p+1) != 0,
```

a selected `6 x 6` mixed minor is

```text
-2 s^2 u^2 (r-1)^2 (r+1)^3
   (u-1)(u-v)^2(pr-p+1).                            (8)
```

Hence the mixed kernel on (7) has dimension two.  An exact basis
consists of:

1. a genuine direction `z_g`, on which the two diagonals are

   ```text
   A z_g =
   -2r(r-1)(u-v)^2 /
     (su(r+1)(u-1)(pr-p+1)),

   B z_g = 2(ru-r+u-v)/(u-1);                       (9)
   ```

2. a reconstruction direction

   ```text
   z_0=(0,u-v,0,0,0,0,1,0),
   A z_0=B z_0=0.                                  (10)
   ```

Every genuine binary extension is therefore

```text
k z_g+l z_0,        k!=0.                           (11)
```

The second kernel line cannot itself carry `Delta_2`; it only changes
the representative of a genuine extension.

## Two-minor ternary obstruction

For a ternary `H22` lift, the mode-zero one-marked contraction through
the other three binary planes must have rank at most three.  Let `N(z)`
be its `8 x 4` matrix.  Adjoin to the fourteen mixed equations the two
minors

```text
det N_0127(z),       det N_0137(z),                  (12)
```

and saturate by `(A z)(B z)`.  Over `C(s,d,u,v,r,p)`,

```text
<mixed rows, det N_0127, det N_0137,
  w(Az)(Bz)-1> = (1).                               (13)
```

Consequently at least one minor in (12) is nonzero on every genuine
extension (11).  The marked contraction has rank four, whereas a
local map to three target coordinates has rank at most three.  No
generic `23` survivor lifts to `H22`.

Combining (5) and (13) closes both weighted diagonal directions at the
generic component point.

## Honest frontier

The theorem leaves the divisors visible in (8)--(9), exceptional
marking specializations such as `pr-p+1=0`, the equal-weight and
opposite-weight slope boundaries, and the component's parameter and
projective boundary.  It also says nothing about diagonal incidences
on the other pure components or any additional component.

The next non-brute-force task is to close these divisors by the same
kernel/Fitting method and then transport the weighted diagonal
reduction to the other certified pure components.

## Verification

Run

```text
python claims/p5/h22/six-dimensional/verify_p5_h22_six_dimensional_component_generic_obstruction.py
python claims/p5/h22/six-dimensional/audit_p5_h22_six_dimensional_component_generic_obstruction.py
```

The primary verifier reconstructs (2), computes both exact
function-field projections, replays the mixed minor and the two kernel
directions, and proves the characteristic-zero unit ideal (13).  The
independent audit uses a separate dynamic-programming permanent and
modular row reduction.  It exhausts all marked bases at generic
weighted samples, recovers (7), enumerates the projective extension
kernel, and replays the two-minor rank obstruction.  Its finite-field
results are corroboration only; the theorem is the
characteristic-zero calculation above.
