# Component 21: the `h0=infinity` boundary and its joint `(s,p)` normal

## Status and scope

This note proves three exact characteristic-zero statements on the displayed
normalized component-21 sheet.

1. The complete nonzero boundary obtained from `h0=infinity` with `p != 0`
   is empty for fixed-order marked `H31` and homogeneous weighted `H22`.
2. At its missing corner `s=1/h0=0`, `p=0`, the complete nonzero first
   projectivized joint `(s,p)`-normal residual is also empty.
3. If `q` tends to zero as well, the complete nonzero monomial `(p,sq)`
   normal residual is empty, for every relative DVR or Puiseux valuation.

Each assertion is proved directly by four global unit ideals: marked `H31`
for distinguished vertices two and three, and weighted `H22` in the finite
and infinite weight charts.  Both normal assertions are incidence
calculations on exact residual pairs; this note does not use pure support as
a transfer theorem.

Other marking infinities, simultaneous marking poles, extension poles, and
arbitrary source, ambient, or projective degenerations remain **UNKNOWN**.
In particular, an ambient `P5` leading term whose `P4` restriction is zero is
not classified merely by the pure-tensor normal calculation below.  The
arbitrary-order local-to-global reduction remains open.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

No finite-field computation is used as proof.

## The homogeneous `h0` chart

Put

\[
 A=(1,1,0,0),\quad C=(1,-1,0,0),\quad
 B=(0,0,1,1),\quad D=(0,0,1,-1),
\]

and use the finite component bases

\[
\begin{aligned}
 a&=(A+pB,\ell A+C,C,D),\\
 b&=(C+qB,A,B+\kappa A,A+\ell C).
\end{aligned}
\]

The other markings remain finite, so for `i=1,2,3` replace `b_i` by
`b_i+h_i a_i`.  At `h0=infinity`, put `s=1/h0` and use the regular scaled
row

\[
 b_0^{\infty}(s)=a_0+s b_0
 =A+pB+s(C+qB).                                  \tag{1}
\]

Direct permanent expansion gives the complete pure support

\[
 T_{0111}=4p,\qquad T_{1111}=4(p+qs).             \tag{2}
\]

At `s=0`, this becomes

\[
 T_{0111}=T_{1111}=4p.                            \tag{3}
\]

Thus (3) is a nonzero projective `P4` tensor exactly when `p != 0`.

## Four direct boundary unit ideals

On `s=0`, take `beta_0=alpha_0=A+pB`, retain

\[
 p,q,\kappa,\ell,h_1,h_2,h_3
\]

as polynomial variables, and introduce all eight extension coordinates.
For distinguished vertices zero and one, the all-`alpha` binary diagonal is
identically zero, so Hall fails.  For each of distinguished vertices two and
three, adjoin the fourteen mixed equations, normalize the all-`alpha`
diagonal, invert the all-`beta` diagonal, and adjoin all 32 entries of the
mode-three one-marked obstruction map.  The two reduced Groebner bases are
`[1]` over `Q`; no component or marking denominator is inverted.

For weighted `H22`, the reverse orientation is Hall-deficient because the
`D01` all-`alpha` diagonal vanishes identically.  In the surviving
`D01`-pure/`D23`-binary orientation, impose the fifteen unwanted `D01`
coefficients, normalize its all-`beta` coefficient, impose the fourteen
mixed `D23` coefficients, invert both `D23` diagonals, and adjoin the full
mode-three obstruction map.  The finite and infinite homogeneous weight
charts both have reduced Groebner basis `[1]`.

These four global unit ideals prove that every point of the boundary (3)
with `p != 0` is obstructed, including all finite values of the remaining
displayed parameters and markings.

## The sharp joint `(s,p)`-normal residual

The corner `s=p=0` cannot be classified by simply substituting in (3), since
its pure tensor is zero.  Write

\[
 p=tP,\qquad s=tS
\]

and keep `q,kappa,ell,h1,h2,h3` finite.  By multilinearity, the coefficient
of `t` in the complete pure tensor is represented by the mode-zero residual
pair

\[
 a_0^{\mathrm{res}}=PB,\qquad
 b_0^{\mathrm{res}}=PB+S(C+qB),                  \tag{4}
\]

while the other three mode pairs are unchanged.  Its complete pure support
is

\[
 T_{0111}^{\mathrm{res}}=4P,\qquad
 T_{1111}^{\mathrm{res}}=4(P+Sq).                \tag{5}
\]

Equations (4)--(5) are identities in `Q[P,S,q,kappa,ell,h1,h2,h3]`.
The normal direction is `[S:P]`; neither affine chart nor either endpoint is
discarded.

Apply exactly the same `H31` and `H22` incidence constructions directly to
the residual pair (4), now retaining `P,S,q,kappa,ell,h1,h2,h3`
polynomially.  All four reduced Groebner bases are again `[1]`.  Therefore
every nonzero first residual (5) is obstructed for both target types.  This
direct calculation also avoids any claim that subtracting the coincident
central row is a legal basis operation.

The residual (5) is zero exactly when

\[
 P=0,\qquad Sq=0.                                 \tag{6}
\]

On the exceptional projective line `(P,S) != (0,0)`, condition (6) reduces
to `[S:P]=[1:0]` and `q=0`.  Hence, over a fixed nonzero component point with
`p=0,q!=0`, the entire joint exceptional line has nonzero residual and is
closed here.  The remaining varying-`q` case is treated next.

## The monomial `(p,sq)` normal

Equation (2) shows that the zero ideal of the pure tensor on this chart is
exactly

\[
 (p,sq).                                           \tag{7}
\]

Let `p(t),s(t),q(t)` be a characteristic-zero DVR arc, or an arc in a finite
Puiseux extension, for which `p` and `sq` are not both identically zero.  Put

\[
 m=\min\{v(p),v(s)+v(q)\},
\]

and let `P` and `R` be the coefficients of order `m` in `p` and `sq`, with a
zero coefficient when the corresponding valuation is larger.  Then
`(P,R)!=(0,0)`.  After division by `t^m`, the exact first nonzero pure tensor
is represented by

\[
 a_0^{\mathrm{mon}}=PB,\qquad
 b_0^{\mathrm{mon}}=(P+R)B,                       \tag{8}
\]

with all other rows specialized at the centre.  Its complete support is

\[
 T_{0111}^{\mathrm{mon}}=4P,\qquad
 T_{1111}^{\mathrm{mon}}=4(P+R).                 \tag{9}
\]

This includes all three valuation cases: `v(p)<v(s)+v(q)`, equality, and
`v(p)>v(s)+v(q)`.  In the last case `P=0` and `R!=0`, which is precisely the
later leading term missed by the ordinary joint first normal at (6).

Apply the full incidence construction directly to (8), retaining
`P,R,kappa,ell,h1,h2,h3` as polynomial variables.  The two marked `H31`
ideals and the two homogeneous weighted `H22` ideals again have reduced
Groebner basis `[1]`.  Since `(P,R)!=(0,0)`, (9) is nonzero.  Thus all
nonzero monomial `(p,sq)` normal directions are obstructed, without choosing
a valuation chart or inverting `P` or `R`.

## Exact conclusion

**The complete `h0=infinity`, `p!=0` boundary of the displayed finite
component-21 chart, the complete nonzero first projectivized joint
`(s,p)`-normal residual above `s=p=0`, and every nonzero monomial `(p,sq)`
normal residual contain no fixed-order marked `H31` point and no homogeneous
weighted `H22` point.**

In particular, if `q!=0` is fixed at the corner, all directions `[S:P]` are
covered by the ordinary joint normal.  If `q` varies to zero, the monomial
normal closes every arc having a nonzero projective `P4` leading term.  This
statement does not compactify the other markings or extension coordinates
and does not classify an earlier ambient `P5` leading term with zero `P4`
restriction.

## Replay

Replay the pinned normalized component-21 package first:

```powershell
uv run --with sympy python claims/p5/frontier/verify_p5_component21_normalized_parameter_compactification_complete_obstruction.py
uv run --with sympy python claims/p5/frontier/audit_p5_component21_normalized_parameter_compactification_complete_obstruction.py
```

Then run:

```powershell
uv run --with sympy python claims/p5/frontier/verify_p5_component21_single_marking_infinity_first_normal_obstruction.py
uv run --with sympy python claims/p5/frontier/audit_p5_component21_single_marking_infinity_first_normal_obstruction.py
uv run --with sympy --with ruff python -m ruff check claims/p5/frontier/verify_p5_component21_single_marking_infinity_first_normal_obstruction.py claims/p5/frontier/audit_p5_component21_single_marking_infinity_first_normal_obstruction.py
uv run --with sympy python -m py_compile claims/p5/frontier/verify_p5_component21_single_marking_infinity_first_normal_obstruction.py claims/p5/frontier/audit_p5_component21_single_marking_infinity_first_normal_obstruction.py
```

The primary reconstructs all twelve unit ideals and both exact normal
residuals.
The independent audit imports no repository code, uses a subset-DP permanent,
reconstructs the same ideals, pins the normalized component-21 dependency
hashes, and replays the primary as a subprocess.
