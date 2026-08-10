# Adjacent-incidence `P_4` pencil reduction for normalized `q4_211`

## Status

This note proves an exact characteristic-zero reduction at any mode
containing both singleton normals in normalized `q4_211`.  In
particular it applies to the generic adjacent incidence type.

Assume

```text
b c != 0
```

and let mode `A` contain

```text
h_1=(b,0,0,-1,0),
h_2=(c,0,0,0,-1).                                   (1)
```

Then the two cross-residual scalars at `A` give exactly one of two
boundaries:

1. if exactly one scalar vanishes, one of the other three maps contains
   the new normal

   ```text
   n=(0,0,0,c,b);
   ```

2. if neither vanishes, an explicit order-four permanent restriction
   has image `Delta_2`.

Thus the adjacent type is reduced to a fourth-normal Schubert divisor
or a marked sharp-subrank-two boundary.  This does **not** exclude
either boundary, normalized `q4_211`, `P_5 -> Delta_3`, or the global
Krenn--Gu conjecture.

## The quotient at the common mode

Let the target covectors pulling back to (1) be

```text
x_A=(r,0,q),
y_A=(t,p,0).                                        (2)
```

The zero coordinates follow from

```text
(u_1,h_1) contract P_5=0,
(u_2,h_2) contract P_5=0.
```

Pullback on target covectors is injective, so `x_A,y_A` are independent
and

```text
(p,q)!=(0,0).                                        (3)
```

Both normals vanish on

```text
E=span(e_1,e_2).
```

Consequently `L_A(E)` lies in the common annihilator line
`ell_A` of `x_A,y_A`; it may be zero.  Quotient the target by this line:

```text
bar L_A:C^5 -> C^3/ell_A.                            (4)
```

The quotient dual is `span(x_A,y_A)`, whose pullback is
`span(h_1,h_2)`.  Restricted to

```text
X=span(e_0,e_3,e_4),
```

the map (4) therefore has rank two and kernel

```text
k=span(e_0+b e_3+c e_4).                             (5)
```

## A four-factor tensor made from the cross residuals

Put

```text
w_+=e_0+b e_3-c e_4,
w_-=e_0-b e_3+c e_4,
Z=span(w_+,w_-),
H=E direct-sum Z.                                    (6)
```

In `X` the determinant of the three columns `k,w_+,w_-` is

```text
-4bc.
```

Hence `k` is not in `Z`, and (4) restricts to an isomorphism

```text
Z -> C^3/ell_A.                                      (7)
```

Consider the decomposable order-four permanent tensor

```text
R=Sym(e_1,e_2,w_+,w_-) in H tensor 4.                (8)
```

When mode `A` receives `w_+`, the other three modes receive

```text
Q_21=Sym(e_1,e_2,w_-).
```

When `A` receives `w_-`, they receive

```text
Q_12=Sym(e_1,e_2,w_+).
```

Contracting the original pure identities at `A` by (2) gives, up to
nonzero diagonal coefficients,

```text
(tensor_(i!=A) L_i)Q_21=q e_2^3,
(tensor_(i!=A) L_i)Q_12=p e_1^3.                    (9)
```

Combining (7)--(9),

```text
(bar L_A tensor tensor_(i!=A)L_i)R
 =q bar L_A(w_+) tensor e_2^3
  +p bar L_A(w_-) tensor e_1^3.                     (10)
```

The two first-mode factors in (10) are independent.

## The two exact boundaries

If exactly one of `p,q` is nonzero, (10) is a nonzero decomposable
image of `P_4`.  Every map restricted to `H` has rank at least two:
`H` is a hyperplane in `C^5`, while every ambient map has rank three.
The common-mode quotient has rank exactly two.  The decomposable-`P_4`
rank-drop theorem therefore forces at least one of the other three maps
to have rank two on `H`.

The annihilator of (6) is

```text
H^perp=span(n),   n=(0,0,0,c,b).                     (11)
```

For a rank-three ambient map, restriction to `H` has rank two exactly
when its row space contains `n`.  This proves the first alternative.

If both `p,q` are nonzero, (10) is a concise two-colour diagonal tensor
after changing basis in the two-dimensional quotient at mode `A`.
Thus (8) gives a marked restriction

```text
P_4 -> Delta_2.                                      (12)
```

The order-four permanent has exact subrank two, so (12) is a sharp
boundary rather than a contradiction.  Its extra marking—the fixed
quotient kernel (5) and the prescribed singleton target lines in the
other three modes—is the remaining structure to exploit.

## Later marked-slice refinements

The marked boundary in (12) has since been classified.  If both
coordinate-deleted pure `P_3` slices have rank two at all three modes,
their six singleton rows lie in one explicit three-parameter normal
form.  Adding the `h_1` incidence at one mode and the `h_2` incidence
at another makes one pair-image six-dimensional and the complementary
pair-image four-dimensional.  The corresponding `2|2` flattening of
`P_4` then has rank at least four, contradicting the rank-two
flattening of `Delta_2`.

Every remaining rank-one slice has since been classified.  There is
exactly one gate of each kind, at distinct modes, and its rows lie in
one transverse or one tangent determinant stratum.  In the transverse
stratum all three third-colour rows become proportional to

```text
n=(0,0,0,c,b).
```

The triple-`n` contraction is zero on `P_5` but nonzero on the target.
In the tangent stratum, two third-colour rows are proportional to `n`;
their double contraction exposes a `P_3` sign chart with incompatible
rank or coordinate support.  Thus the full two-cross marked boundary
is empty.  See:

- [`P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md`](../../p4/classifications/P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md)
- [`P5_Q4_211_MARKED_DELTA2_PAIR_IMAGE_OBSTRUCTION.md`](P5_Q4_211_MARKED_DELTA2_PAIR_IMAGE_OBSTRUCTION.md)
- [`P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md`](../../p4/classifications/P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md)
- [`P5_Q4_211_ALTERNATING_GATE_OBSTRUCTION.md`](P5_Q4_211_ALTERNATING_GATE_OBSTRUCTION.md)

## Consequence and remaining boundary

The parallel-incidence theorem shows that, on `bc != 0`, a selected
parallel pair always acquires another common-normal mode and can be
reselected as adjacent.  The present result therefore covers that
extra-incidence branch as well as the originally adjacent type.

The only remaining adjacent outcome on `bc != 0` is therefore the
one-cross branch: another row space contains the fourth normal in
(11).  A later projective-pencil reduction shows that this normal
always pulls back from doubled target colour zero.  It also forces a
remaining mode to contain the whole opposite normal pencil
`span(h_1,n)` or `span(h_2,n)`.  The pure residual pencil is further
  confined to a double-normal gate, the common kernel `e_1+e_2`, or the
  three rigid lines `h_2,n,u_1` / `h_1,n,u_2`.  A direction-conic
refinement removes the free rigid/polar core.  A later two-gate theorem
absorbs the second-common and double-normal alternatives.  The
remaining direction-plane and common-kernel gates are both impossible,
so adjacent one-cross incidence is empty on `abc != 0`.  See:

- [`P5_Q4_211_ONE_CROSS_PENCIL_SATURATION_REDUCTION.md`](P5_Q4_211_ONE_CROSS_PENCIL_SATURATION_REDUCTION.md)
- [`P5_Q4_211_ONE_CROSS_DIRECTION_CONIC_REDUCTION.md`](P5_Q4_211_ONE_CROSS_DIRECTION_CONIC_REDUCTION.md)
- [`P5_Q4_211_ONE_CROSS_TWO_GATE_REDUCTION.md`](P5_Q4_211_ONE_CROSS_TWO_GATE_REDUCTION.md)
- [`P5_Q4_211_ONE_CROSS_DIRECTION_PLANE_OBSTRUCTION.md`](P5_Q4_211_ONE_CROSS_DIRECTION_PLANE_OBSTRUCTION.md)
- [`P5_Q4_211_ONE_CROSS_COMMON_KERNEL_OBSTRUCTION.md`](P5_Q4_211_ONE_CROSS_COMMON_KERNEL_OBSTRUCTION.md)
The parameter boundaries `b=0` and `c=0` are not addressed here.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q4_211_adjacent_p4_pencil.py
python claims/p5/frontier/audit_p5_q4_211_adjacent_p4_pencil.py
python claims/p4/classifications/verify_p4_marked_delta2_slice_classification.py
python claims/p4/classifications/audit_p4_marked_delta2_slice_classification.py
python claims/p5/frontier/verify_p5_q4_211_marked_delta2_pair_image.py
python claims/p5/frontier/audit_p5_q4_211_marked_delta2_pair_image.py
python claims/p4/boundaries/verify_p4_marked_delta2_alternating_gate.py
python claims/p4/boundaries/audit_p4_marked_delta2_alternating_gate.py
python claims/p5/frontier/verify_p5_q4_211_alternating_gate_obstruction.py
python claims/p5/frontier/audit_p5_q4_211_alternating_gate_obstruction.py
python claims/p5/frontier/verify_p5_q4_211_one_cross_pencil_saturation.py
python claims/p5/frontier/audit_p5_q4_211_one_cross_pencil_saturation.py
python claims/p5/frontier/verify_p5_q4_211_one_cross_direction_conic.py
python claims/p5/frontier/audit_p5_q4_211_one_cross_direction_conic.py
python claims/p5/frontier/verify_p5_q4_211_one_cross_two_gate.py
python claims/p5/frontier/audit_p5_q4_211_one_cross_two_gate.py
python claims/p5/frontier/verify_p5_q4_211_one_cross_direction_plane.py
python claims/p5/frontier/audit_p5_q4_211_one_cross_direction_plane.py
python claims/p5/frontier/verify_p5_q4_211_one_cross_common_kernel.py
python claims/p5/frontier/audit_p5_q4_211_one_cross_common_kernel.py
```

The primary verifier checks the two cross contractions, the determinant
`-4bc`, the common quotient kernel, the annihilator (11), and the
abstract factorization (10).  The independent audit rederives the
contractions apolarly and checks the quotient and one-term/two-term
rank split over `F_3,F_5`.  It does not enumerate ambient maps.  The
finite-field calculations audit the formulas; the reduction above is
over `C`.
