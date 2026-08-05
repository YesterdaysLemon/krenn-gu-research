# Component 21: the other three single marking poles

## Status and scope

This note closes the nonzero restriction arising from each of the three
single-pole charts `h1=infinity`, `h2=infinity`, and `h3=infinity` on the
displayed normalized component-21 sheet.  For each pole it proves two exact
characteristic-zero statements.

1. The boundary tensor itself is zero, but every nonzero first normal in the
   marking parameter is obstructed for fixed-order marked `H31` and
   homogeneous weighted `H22`.
2. Above the zero locus of that first normal, every nonzero monomial
   `(s_i p,s_i q)` normal is obstructed for the same two target types, for
   every relative DVR or Puiseux valuation.

All incidence calculations are made directly on exact residual pairs.  Pure
support is used to identify the zero loci, not as a transfer theorem.

The finite `h0` marking chart is retained throughout.  Consequently,
simultaneous marking poles remain **UNKNOWN**.  Extension-coordinate poles,
arbitrary source, ambient, and projective degenerations, and any ambient
`P5` leading term with zero `P4` restriction also remain **UNKNOWN**.  The
arbitrary-order local-to-global reduction is open, and the global Krenn--Gu
conjecture remains **UNRESOLVED**.

No finite-field computation is used as proof.

## Homogeneous marking rows

Write

\[
 A=(1,1,0,0),\quad C=(1,-1,0,0),\quad
 B=(0,0,1,1),\quad D=(0,0,1,-1),
\]

and retain the finite component bases

\[
\begin{aligned}
 a&=(A+pB,\ell A+C,C,D),\\
 b&=(C+qB,A,B+\kappa A,A+\ell C).
\end{aligned}
\]

For a fixed `i` in `{1,2,3}`, all markings except `h_i` remain finite.  Thus
replace `b_j` by `b_j+h_j a_j` for `j != i`.  In homogeneous coordinates at
`h_i=infinity`, put `s_i=1/h_i` and use the regular scaled row

\[
 b_i^\infty(s_i)=a_i+s_i b_i.                    \tag{1}
\]

An exact permanent expansion, separately for all three values of `i`, gives

\[
 T_{0111}=4p s_i,\qquad
 T_{1111}=4s_i(h_0p+q),                          \tag{2}
\]

with all other coefficients zero.  Hence the boundary `s_i=0` has zero
`P4` restriction.  It is not claimed to be obstructed merely by that fact.

## The complete first normal

The coefficient of `s_i` in (2) is represented directly by retaining the
other three mode pairs and replacing the `i`-th pair by

\[
 a_i^{\rm res}=0,\qquad b_i^{\rm res}=b_i.       \tag{3}
\]

Its pure support is

\[
 T_{0111}^{\rm res}=4p,\qquad
 T_{1111}^{\rm res}=4(h_0p+q).                  \tag{4}
\]

For each `i=1,2,3`, apply the full incidence construction directly to (3),
retaining

\[
 p,q,\kappa,\ell,h_0,\{h_j:j\ne 0,i\}
\]

as polynomial variables and introducing all eight extension coordinates.
The distinguished-zero and distinguished-one marked `H31` orientations are
Hall-deficient.  For each of distinguished vertices two and three, impose
the fourteen mixed equations, normalize the all-alpha diagonal, invert the
all-beta diagonal, and impose the full 32-entry mode-three obstruction map.
Both reduced Groebner bases are `[1]` over `Q`.

For homogeneous weighted `H22`, the reverse orientation is Hall-deficient
because the `D01` all-alpha diagonal vanishes identically.  In the surviving
`D01`-pure/`D23`-binary orientation, impose all unwanted coefficients,
normalize the required `D01` coefficient, invert both `D23` diagonals, and
impose the full mode-three obstruction map.  The finite and infinite weight
charts again both have reduced Groebner basis `[1]`.

Thus twelve exact global unit ideals, four for each marking pole, obstruct
every nonzero first normal (4).  Its zero locus is exactly

\[
 p=q=0.                                          \tag{5}
\]

No component or finite-marking denominator is inverted.

## The monomial `(s_i p,s_i q)` normal

Equation (2) shows that on any one of these homogeneous marking charts, the
pure restriction is controlled exactly by the monomial pair

\[
 (s_i p,s_i q).                                  \tag{6}
\]

Let a characteristic-zero DVR arc, or an arc in a finite Puiseux extension,
approach `s_i=p=q=0`.  Suppose `s_i p` and `s_i q` are not both identically
zero.  Put

\[
 m=\min\{v(s_i)+v(p),v(s_i)+v(q)\},
\]

and let `P,Q` be their coefficients of order `m`, using zero when the
corresponding valuation is larger.  Then `(P,Q)!=(0,0)`.  After division by
the common order, an exact residual-pair representative is obtained by
specializing `p=q=0`, using (3) at mode `i`, and replacing the mode-zero pair
by

\[
 a_0^{\rm wt}=PB,\qquad
 b_0^{\rm wt}=(h_0P+Q)B.                         \tag{7}
\]

The finite value of `h0` in (7) is the centre of the arc.  Variations of
`h0` enter only at higher order.  Direct permanent expansion gives

\[
 T_{0111}^{\rm wt}=4P,\qquad
 T_{1111}^{\rm wt}=4(h_0P+Q).                   \tag{8}
\]

For every `i=1,2,3`, the same two marked `H31` and two homogeneous weighted
`H22` constructions applied directly to (7) have reduced Groebner basis
`[1]`.  These are twelve further exact global unit ideals.  Since `(P,Q)` is
nonzero, (8) is nonzero, including the cancellation direction
`Q=-h0 P` where only `T_0111` survives.

This proves the assertion for all three valuation comparisons and does not
select an affine chart on `[P:Q]`.

## Exact conclusion

**For each of the three single marking poles `h1=infinity`, `h2=infinity`,
and `h3=infinity`, the complete nonzero first marking normal and every
nonzero monomial `(s_i p,s_i q)` normal contain no fixed-order marked `H31`
point and no homogeneous weighted `H22` point.**

The boundary itself and the residual with `P=Q=0` have zero `P4`
restriction.  Their possible realization by an earlier ambient `P5` leading
term is outside this statement.  Intersections with another marking pole
are also outside this statement.

## Replay

Replay the pinned normalized component-21 package first:

```powershell
uv run --with sympy python .\verify_p5_component21_normalized_parameter_compactification_complete_obstruction.py
uv run --with sympy python .\audit_p5_component21_normalized_parameter_compactification_complete_obstruction.py
```

Then run:

```powershell
uv run --with sympy python .\verify_p5_component21_other_single_marking_infinity_weighted_normal_obstruction.py
uv run --with sympy python .\audit_p5_component21_other_single_marking_infinity_weighted_normal_obstruction.py
uv run --with sympy --with ruff python -m ruff check .\verify_p5_component21_other_single_marking_infinity_weighted_normal_obstruction.py .\audit_p5_component21_other_single_marking_infinity_weighted_normal_obstruction.py
uv run --with sympy python -m py_compile .\verify_p5_component21_other_single_marking_infinity_weighted_normal_obstruction.py .\audit_p5_component21_other_single_marking_infinity_weighted_normal_obstruction.py
```

The primary reconstructs all 24 unit ideals and the exact homogeneous,
first-normal, and weighted-normal identities.  The independent audit imports
no repository code, uses a subset-DP permanent, reconstructs all 24 ideals,
pins the normalized component-21 dependency hashes, and replays the primary
as a subprocess.
