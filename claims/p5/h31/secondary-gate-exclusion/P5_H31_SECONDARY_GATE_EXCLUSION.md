# Exclusion of the secondary-gate `H31` branch

## Status

This is an exact characteristic-zero obstruction for the remaining
single-gate boundary of `H31`.

Start with one binary row pair that has rank one on the pure
four-dimensional hyperplane.  If one of the other three pairs drops
rank after restriction to the common source three-space, then no
rank-three ternary lift exists.

Together with
[`P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md`](../single-gate-rank-two-m-exclusion/P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md),
this excludes **every** `H31` pure/`Delta_2` pencil having a rank-one
row pair on its pure hyperplane.

It does not classify or exclude every all-rank-two pure-`P_4`
compression, exclude all of `H31` or `H22`, prove
`P_5 -> Delta_3` impossible, or settle the global conjecture.

The proof reframes the boundary as:

1. a `2 x 2 x 2` subrank-two restriction of `P_3`;
2. a pair-image polarity problem;
3. two support normal forms for the zero locus of the `P_3` pair map;
   and
4. one-marked determinantal and mixed-colour obstructions.

No ambient-map or Grassmannian search is used.

## The unique secondary gate

Use

```text
M=span(e_0,e_1,e_2),
H_s=M+Ce_s,
H_p=M+Ce_p.
```

Normalize the primary gate at mode zero:

```text
alpha_0|H_s=0,      alpha_0|H_p=e_p^*.              (1)
```

Selecting `alpha_0` on `H_p` leaves a nonzero pure `P_3` tensor through
modes `1,2,3`, supported at `alpha_1 alpha_2 alpha_3`.

If the pair at one of those modes has rank one on `M`, its `beta` row
is proportional to its `alpha` row.  Replacing that `alpha` row in the
nonzero pure coefficient by the proportional `beta` row must give
zero, so the proportionality scalar is zero.  Hence

```text
beta_i|M=0.                                         (2)
```

The `beta^4` coefficient is nonzero on both `H_s,H_p`, so
`beta_i` has a nonzero entry on both exceptional coordinates.  Two
rows satisfying (2) would use the same exceptional coordinate twice
in either `beta^4` permanent.  Thus there is exactly one secondary
gate.  Put it at mode one.  The pairs at modes two and three have rank
two on `M`.

Write their marked rows as

```text
alpha_1=a,   beta_0=v,
alpha_2=c,   beta_2=d,
alpha_3=e,   beta_3=f.                              (3)
```

## A `P_3 -> Delta_2` polarity

For `x,y in M^*`, define the pair product

```text
mu(x,y)=(
 x_1y_2+x_2y_1,
 x_0y_2+x_2y_0,
 x_0y_1+x_1y_0
).                                                   (4)
```

Then `P_3(z,x,y)=z dot mu(x,y)`.

The two binary diagonals and all their mixed coefficients say

```text
a dot mu(c,e) != 0,      a dot mu(c,f)=0,
a dot mu(d,e)  = 0,      a dot mu(d,f)=0,

v dot mu(c,e)  = 0,      v dot mu(c,f)=0,
v dot mu(d,e)  = 0,      v dot mu(d,f)!=0.           (5)
```

Thus the restriction of `P_3` to

```text
span(a,v) tensor span(c,d) tensor span(e,f)
```

is `Delta_2` in the displayed bases.  In particular, `a,v` are
independent.

Let

```text
R=span(mu(c,e),mu(c,f),mu(d,e),mu(d,f)).             (6)
```

The two nonzero diagonal pair products in (5) are independent, so
`dim R` is two or three.

### Full pair image

If `dim R=3`, the one-marked map at the secondary gate on `H_p` is
injective.  Indeed, its four coefficients using `alpha_0=e_p^*`
annihilate a candidate row `gamma_1|M` on all of `R`, hence force
`gamma_1|M=0`.  The coefficient using
`beta_0,beta_2,beta_3` is then

```text
gamma_1[e_p] P_3(v,d,f),
```

which forces the exceptional entry to vanish as well.

On `H_s`, the transverse vector `e_s^*` has that same nonzero
coefficient `P_3(v,d,f)`.  The transverse-kernel principle therefore
forces `gamma_1=0`, contradicting rank three.  Hence a surviving lift
would require

```text
dim R=2.                                             (7)
```

Because the restrictions of `a,v` are a dual basis on the span of the
two diagonal pair products, (5) and (7) force the off-diagonal pair
products to vanish identically:

```text
mu(c,f)=mu(d,e)=0.                                   (8)
```

## Classifying the zero pair products

For nonzero `x,y`, equation `mu(x,y)=0` has a short exact
classification.

- If `x` has three nonzero coordinates, the matrix of
  `y -> mu(x,y)` has determinant `2x_0x_1x_2`, so `y=0`, impossible.
- If `x` has support one, then `y` is on the same coordinate line.
- If `x` has support two, say
  `x=(x_0,x_1,0)` with `x_0x_1!=0`, then

  ```text
  y is proportional to (x_0,-x_1,0).                (9)
  ```

Thus each zero pair in (8) is a sign-mated pair on one coordinate
line or plane.  Independence of `mu(c,e)` and `mu(d,f)` leaves, up to
permuting source coordinates and modes two and three, exactly two
support patterns:

```text
L: one coordinate line and its complementary coordinate plane;
P: two distinct coordinate planes.                  (10)
```

The same-plane and two-line patterns make the two diagonal pair
products proportional and are impossible.

## Stratum L: line against complementary plane

After row rescaling, the common-plane rows are

```text
c=f=(1,0,0),
d=(0,r,t),          e=(0,r,-t),
a=(a_0,r,-t),       v=(v_0,r,t),       r t!=0.       (11)
```

For either exceptional coordinate, write the six non-gate extension
entries as

```text
T=beta_0[q], X=alpha_1[q],
C=alpha_2[q], D=beta_2[q],
E=alpha_3[q], F=beta_3[q],
```

and put `g=beta_1[q]!=0`.  The four remaining binary mixed equations
reduce exactly to

```text
T=-Cv_0,   X=-Fa_0,   Dv_0=Ea_0.                    (12)
```

On `H_p`, the following one-marked minors are

```text
det F_2[0,1,4,7] =  8g r^3t^3 v_0,
det F_3[0,5,6,7] = -8a_0 g^2 r^3t^3,
det F_1[0,3,6,7] = -8E r^3t^3.                      (13)
```

After these force `v_0=a_0=E_p=0`, equation (12) gives
`T_p=X_p=0`, and

```text
det F_0[0,2,4,7] = 8D_p g_p^2 r^3t^3.               (14)
```

Thus `D_p=0`.  Every nonzero minor in (13)-(14) has a nonzero
transverse coefficient on the other hyperplane, so injectivity invokes
the same transverse-kernel contradiction as above.

Keep the now-forced deepest `H_p` form, and allow `D_s,E_s` on the
pure hyperplane.  The stacked five-dimensional one-marked maps have
minors

```text
det F_0[0,2,4,8,15] = 16D_s g_p g_s r^4t^4,
det F_1[6,7,8,11,15]= -16E_s r^4t^4.                (15)
```

Hence `D_s=E_s=0` as well.

At this deepest point, the stacked kernels at modes zero and two are

```text
ker F_0=C(-1,0,0,C_s,C_p),
ker F_2=span(e_s^*,e_p^*).                           (16)
```

Their ranks are certified by the nonzero minors

```text
8g_pg_s r^3t^3,   4g_s r^2t^2.                      (17)
```

Rank three makes `gamma_0` a nonzero multiple of the first vector in
(16), while `gamma_2=(0,0,0,H_s,H_p)`.  On each hyperplane,

```text
per(gamma_0,alpha_1,gamma_2,alpha_3)
 =2r t H_q
```

up to the nonzero scale of `gamma_0`.  This forbidden mixed target
coefficient forces `H_s=H_p=0`, hence `gamma_2=0`, a contradiction.
Stratum L is excluded.

## Stratum P: two distinct coordinate planes

Choose nonzero `p,q,r,t` and write

```text
c=(p,q,0),          f=(p,-q,0),
d=(r,0,t),          e=(r,0,-t),
n=(0,qr,pt).
```

Every compatible diagonal pair is

```text
a=(1,q/p,0)+alpha n,
v=(1,-q/p,0)+beta n.                                (18)
```

Put

```text
K=alpha(beta p r-1),
L=beta(alpha p r+1).                                (19)
```

The binary extension equations are

```text
CK+FL=0,        DK+EL=0,
T=CrK+EpL,      X=DpK+FrL.                          (20)
```

If `(K,L)!=(0,0)`, use parameters `c_0,d_0`:

```text
C=Lc_0, F=-Kc_0, D=Ld_0, E=-Kd_0.
```

The marked minors

```text
det F_2[0,5,6,7]
 = 8 alpha g^2 q^3t^3(beta p r-1)^2,

det F_3[0,1,4,7]
 =-8 beta g q^3t^3(alpha p r+1)^2                  (21)
```

exclude `K!=0` and `L!=0`, respectively.  Therefore `K=L=0`.
Equation (19) has exactly two solutions:

```text
P0: alpha=beta=0;
P1: alpha=-1/(pr), beta=1/(pr).                     (22)
```

For P0, one-marked minors on `H_p` force

```text
E_p=F_p=0 through F_0,
C_p=D_p=0 through F_1.                              (23)
```

For P1, the same conclusion holds with the two pairs interchanged:
`F_0` forces `C_p=D_p=0`, and `F_1` forces
`E_p=F_p=0`.  Explicit minors are listed and checked by the verifier.

With the partial-hyperplane extensions zero, stacked `5 x 5` minors
force all four pure-hyperplane extensions to vanish as well.  At the
resulting deepest point, for both P0 and P1,

```text
ker F_0=ker F_1=C(0,qr/(pt),1,0,0),
ker F_2=span(e_s^*,e_p^*).                           (24)
```

For P0, the forbidden coefficient

```text
per(beta_0,gamma_1,gamma_2,beta_3)=-2q H_q
```

forces both exceptional entries of `gamma_2` to vanish.  For P1, the
same conclusion follows from

```text
per(gamma_0,alpha_1,gamma_2,beta_3)=-2q H_q.         (25)
```

Thus `gamma_2=0`, again contradicting rank three.  This excludes P0
and P1, hence stratum P and the entire secondary-gate branch.

## Consequence for `H31`

There are now only two possibilities for a pure-hyperplane binary
compression in `H31`:

1. it has a rank-one pair, in which case the two single-gate theorems
   exclude it completely; or
2. all four binary row pairs have rank two on the pure hyperplane.

The known five-parameter component of case 2 is excluded separately,
but exhaustiveness of that component remains open.  The honest `H31`
frontier is therefore the still-unclassified all-rank-two
pure-`P_4` locus.

## Verification

Run:

```text
python claims/p5/h31/secondary-gate-exclusion/verify_p5_h31_secondary_gate_exclusion.py
python claims/p5/h31/secondary-gate-exclusion/audit_p5_h31_secondary_gate_exclusion.py
```

The primary verifier reconstructs both pair-image normal forms, every
binary extension equation, all displayed one-marked and stacked
minors, the deepest kernels, and the final mixed coefficients
symbolically.

The independent audit uses separate modular pair-product, permanent,
and row-reduction code over `F_5` and `F_7`.  It audits the zero-pair
support classification, the two normal forms, their determinantal
strata, and the deepest mixed coefficients.  It enumerates no ambient
maps or Grassmannians.  The finite-field calculation audits the case
boundaries; the proof above is over characteristic zero.
