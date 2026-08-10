# Direction-conic reduction for one-cross normalized `q4_211`

## Status

This is an exact characteristic-zero refinement of
[`P5_Q4_211_ONE_CROSS_PENCIL_SATURATION_REDUCTION.md`](P5_Q4_211_ONE_CROSS_PENCIL_SATURATION_REDUCTION.md)
on

```text
a b c != 0.
```

In the `q` orientation, let `A` be the common `h_1,h_2` mode and let
`Y` be a remaining mode containing the mandatory opposite pencil

```text
span(h_1,n).
```

The normal `h_2` at `A` and the normal `n` at `Y` both pull back from
target colour zero.  Let `P,Q` be the other two modes.  Then exactly
one of the following occurs:

1. `R_P` or `R_Q` contains the whole direction plane

   ```text
   span(u_1,u_2);
   ```

2. `L_A(e_1+e_2)=0` or `L_Y(e_1+e_2)=0`; or
3. both restrictions to one nondegenerate ternary conic have rank two,
   their kernel lines are polar, and their direction incidences are

   ```text
   {R_P intersect span(u_1,u_2),
    R_Q intersect span(u_1,u_2)}
      ={C u_2, C m},                                 (1)

   m=c u_1-b u_2=(0,0,0,c,-b).
   ```

In the colour-swapped `p` orientation, (1) becomes

```text
{C u_1,C m}.                                        (2)
```

At least one of the two polar kernel lines lies in
`span(e_1+e_2,e_1-e_2)`.  If the mandatory opposite-pencil mode is the
otherwise unselected mode, both kernels lie there and one of them is
exactly `span(e_1+e_2)`.

Combining this conic with the binary-cubic theorem eliminates the
apparently free polar core.  In the `q` orientation, at least one of
the following four explicit gates must occur:

1. a second mode contains both `h_1,h_2`;
2. a mode contains `span(h_2,n)`;
3. a mode contains `span(u_1,u_2)`; or
4. `L_A(e_1+e_2)=0` or
   `L_Y(e_1+e_2)=0`.

The colour-swapped list replaces the second gate by `span(h_1,n)`.

This is a strict reduction, not an exclusion of the direction-plane,
common-kernel, or polar alternatives, all adjacent incidence,
normalized `q4_211`, `P_5 -> Delta_3`, or the global Krenn--Gu
conjecture.

## The common ternary conic

Put

```text
s=e_1+e_2,
d=e_1-e_2,
w=e_0-b e_3-c e_4,
H_0=span(s,d,w).                                    (3)
```

The support plane annihilator is

```text
H_0^perp=span(u_1,u_2).                             (4)
```

In the `q` orientation, `h_2=L_A^* e_0^*` up to scale.  The
opposite-pencil theorem supplies `Y` with `h_1,n`, and the universal
fourth-normal identity gives `n=L_Y^* e_0^*` up to scale.  Contracting
also by `u_0` at the distinguished mode leaves

```text
(u_0,h_2,n) contract P_5=-c Q_a,                    (5)
```

where, up to a harmless common normalization, the symmetric matrix of
`Q_a` in the basis `(s,d,w)` is

```text
M=[
 [ a/2,    0, 1 ],
 [   0, -a/2, 0 ],
 [   1,    0, 0 ]
].                                                   (6)
```

Its determinant is `a/2`.  The target contraction is a nonzero
multiple of

```text
e_0 tensor e_0
```

through modes `P,Q`.

Let

```text
r_P=rank(L_P|H_0),   r_Q=rank(L_Q|H_0).
```

If one rank is one, its row space intersects the two-plane (4) in
dimension two and therefore contains all of `span(u_1,u_2)`.  This is
alternative 1.

Otherwise both ranks are at least two.  Sylvester's inequality for the
invertible matrix (6) and its rank-one image gives

```text
1 >= r_P+r_Q-3.
```

Hence

```text
r_P=r_Q=2.                                          (7)
```

Each row space contains one direction line

```text
ell_i=R_i intersect span(u_1,u_2).
```

The target covector pulling back to `ell_i` annihilates `e_0`, since it
annihilates the rank-two image plane in (5), which contains the pure
factor `e_0`.

Let `k_P,k_Q` be the two kernel lines in `H_0`.  As in the disjoint
conic-polarity reduction, rank one in (5) is equivalent to

```text
k_P^T M^(-1) k_Q=0,                                 (8)
```

where

```text
M^(-1)=[
 [ 0,    0,    1 ],
 [ 0, -2/a,    0 ],
 [ 1,    0, -a/2]
].                                                   (9)
```

## Polarizing the direction pencil

Write

```text
ell_P=A u_1+B u_2,
ell_Q=C u_1+D u_2.                                  (10)
```

The target covectors pulling back to these lines annihilate colour
zero.  Contract at `A` by `h_2` and at `P,Q` by
`ell_P,ell_Q`.  The target contraction is zero.  On the source, all
three rows are supported on coordinates `0,3,4`, so it is

```text
Perm_3(h_2,ell_P,ell_Q) Sym(e_1,e_2).
```

The distinguished map sends both `e_1,e_2` to target `e_0`, while the
opposite-pencil mode `Y` maps their span into target `e_1`.  Therefore,
unless

```text
L_Y(s)=0,
```

the scalar permanent must vanish.  Direct expansion gives

```text
Perm_3(h_2,ell_P,ell_Q)=-2b A C.                    (11)
```

Similarly contract at `Y` by `n` and at `P,Q` by the two direction
lines.  Unless `L_A(s)=0`, the same off-diagonal argument gives

```text
Perm_3(n,ell_P,ell_Q)
 =2(Ab+Bc)(Cb+Dc)=0.                                (12)
```

If either common kernel occurs, this is alternative 2.  Otherwise
(11) says one of the two direction lines is `C u_2`, while (12) says
one is

```text
C(cu_1-bu_2)=C m.
```

These lines are distinct because `bc != 0`, proving (1).

In the `p` orientation, contract by `h_1` instead.  The corresponding
formula is

```text
Perm_3(h_1,ell_P,ell_Q)=-2c B D,                    (13)
```

so one direction line is `C u_1`; equation (12) again forces the other
to be `C m`.  This proves (2).

## Where the polar kernels lie

Among `P,Q` there is always at least one selected singleton-normal
mode not equal to `Y`: it contains `h_1` or `h_2`.  On `H_0`, either
normal restricts to a nonzero multiple of `w^*`:

```text
h_1(w)=2b,   h_2(w)=2c.
```

Its row plane therefore contains `w^*`, so its kernel lies in

```text
E=span(s,d).                                        (14)
```

If `Y` is the otherwise unselected mode, then `P,Q` are precisely the
selected `h_1`- and `h_2`-modes, so both kernels lie in `E`.
Restricting (9) to `E` gives

```text
k_P^T M^(-1)k_Q=-(2/a) delta_P delta_Q.
```

Equation (8) then forces `delta_P=0` or `delta_Q=0`; one kernel is the
radical line

```text
C s=C(e_1+e_2).                                     (15)
```

## Collision with the normal-pencil cubic

First note that no `h_1,h_2` common mode can also contain `n`.  The
fourth normal pulls back from `e_0^*`.  Independence then forces the
`h_1` covector to have a nonzero target-colour-two component and the
`h_2` covector to have a nonzero target-colour-one component.  Both
cross residuals would be nonzero, contrary to the alternating-gate
obstruction.

Now stay in the `q` orientation and suppose none of the four gates
listed in the status occurs.  The mandatory mode `Y` contains
`h_1,n`.

It cannot be the selected `h_2`-mode, by the preceding paragraph.  If
it were the otherwise unselected mode, then `P,Q` would be the selected
`h_1`- and `h_2`-modes.  Equation (1) assigns `m` to one of them.  But

```text
m=b h_2-c h_1,                                      (16)
```

so that mode would also contain the other singleton normal, producing
the excluded second common mode.

Hence `Y` is the selected `h_1`-mode.  The other two modes are the
selected `h_2`-mode `C` and the unselected mode `D`.  Avoiding a second
common mode forces the direction assignment in (1) to be

```text
C u_2 subset R_C,   C m subset R_D.                 (17)
```

On the other hand, avoiding the `span(h_2,n)` gate and the common
kernel at `A` puts the nonzero `J_-` residual in the three-root
alternative of the normal-pencil theorem.  Its three normal lines at
the remaining modes are

```text
C h_2 at C,   C n at Y,   C u_1 at D.               (18)
```

Equations (17)--(18) put both `u_1` and `m` in `R_D`.  Since

```text
m=c u_1-b u_2
```

and `b != 0`, this makes

```text
span(u_1,u_2) subset R_D,
```

contrary to the assumed absence of the direction-plane gate.

The `p` orientation is identical after colour interchange.  Its only
non-common placement has the selected `h_2`-mode as `Y`, puts `u_1`
at the selected `h_1`-mode and `m` at the unselected mode, while the
normal-pencil cubic puts `u_2` at that same unselected mode.  Again
the full direction plane is forced.  This proves the four-gate
corollary.

## Consequence

The one-cross boundary on `abc != 0` couples two small projective
objects:

- the binary cubic on the normal pencil, whose third root is `u_1` or
  `u_2`; and
- the nondegenerate conic (6), whose two remaining maps carry the
  fixed direction lines in (1) or (2) and polar kernel lines.

Their compatibility removes the free polar configuration.  The
remaining work is confined to the second-common-mode,
double-normal-plane, full-direction-plane, and common-kernel gates
listed above.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q4_211_one_cross_direction_conic.py
python claims/p5/frontier/audit_p5_q4_211_one_cross_direction_conic.py
```

The primary verifier differentiates (5), checks (4), (6), (9), and
expands the three polarized permanents (11)--(13).  The independent
audit row-reduces the conic over `F_5,F_7` and checks every projective
pair of direction lines against the two polarization equations.  It
enumerates no ambient maps or Grassmannians.  The finite-field checks
audit the formulas and case split; the reduction above is over `C`.
