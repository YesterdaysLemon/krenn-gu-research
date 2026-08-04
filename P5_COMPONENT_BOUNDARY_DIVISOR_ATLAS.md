# Boundary-divisor atlas for the `H31`/`H22` component program

## Status and scope

Working note (agent4).  This atlas systematizes, for every certified
pure-`P_4` component orbit and both local frames (`H31`, weighted
`H22`), the loci that the generic-point obstruction theorems exclude:
parameter divisors, slope divisors, marking-branch divisors, and
projective boundaries.  It then closes, with new exact certificates,
the four interior/boundary slope divisors of the eighth (disjoint
mixed-star) component's weighted-`H22` theorem:

```text
r = 1   (both pencils)   closed at binary level (new, exact identity);
r = -1  (both pencils)   closed at binary level (new, Groebner unit);
r = 0   (both pencils)   = the H31 q-frames; D_01 side closed at
                          binary level, D_23 side closed at ternary
                          level (new certificates + H31 shadow);
af(r+1)-(r-1)=0 (D_01)   OPEN: mode-3 certificate designed, modular
                          evidence complete, on-divisor denominator
                          units certified; main Groebner timeout-null
                          (II.5).
```

All new certificates are over the generic component point
`K=C(a,b,f)[phi]/(Phi)`; intersections of the slope divisors with the
component's parameter divisors and the projective boundary remain
open, as everywhere else in the program.  Nothing here claims
component exhaustiveness or touches the global prize problem.

Reproduction scripts: `scripts/` next to this note; output ledgers
`slope_divisor_modular_survey.json`,
`coupled_divisor_modular_survey.json`,
`r1_binary_obstruction_verified.json`,
`rm1_binary_obstruction_verified.json`,
`slope_boundary_frame_identifications_verified.json`,
`special_slope_reduced_fitting_results.json`.

## Conventions

* Component numbering follows the frontier
  (`P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`): 1 first rank-two, 2
  diagonal-quadric `(3,3)`, 3-5 split-cubic `L_1,L_2,L_3`, 6
  mixed-orientation, 7 six-dimensional, 8 disjoint mixed-star.  The
  ninth (all-rank-one triangle), tenth (coincident-support), and
  eleventh (equal-support sixfold) components certified by the
  parallel census work have no `H31`/`H22` generic theorems yet and
  are outside these tables; adding them is listed in Part III.
* `H31` frame: coordinate deletion `q` with marked bases
  `beta_i(t)=beta_i+t_i alpha_i`.
* Weighted `H22` frame: the two diagonal-hyperplane pencils
  `D_01^r(u)=(r u_0+u_1,u_2,u_3,u_4)`,
  `D_23^r(u)=(u_0,u_1,r u_2+u_3,u_4)`, slope `r` generically
  transcendental.  A *slope divisor* is a proper closed condition on
  `r` (possibly coupled to parameters) excluded by the generic proof.
* "Displayed" divisors are stated in the theorem docs; "implicit"
  divisors are denominators of the underlying Groebner/elimination
  runs that the docs do not enumerate.  Both are open unless a
  closure is cited.
* Status legend: `closed` (complete fibre statement), `generic-only`
  (function-field theorem; listed divisors open), `new-closed`
  (closed by the certificates in this atlas).

## Part I — the systematic table

### `H31` frame

| # | component | certificate doc | excluded loci of the generic proof | status |
|---|-----------|-----------------|------------------------------------|--------|
| 1 | first rank-two | `P5_H31_KNOWN_RANK_TWO_FAMILY_OBSTRUCTION.md`, `P5_H31_RANK_TWO_COMPONENT_ORBIT_OBSTRUCTION.md`, `P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md`, `P5_H31_COMPONENT_CHART_BOUNDARY_(MARKED_FIBRE_)OBSTRUCTION.md`, `P5_H31_COMPONENT_FIBER/FIBRE_INFINITY_*.md`, `P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md`, `P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md`, `P5_H31_SINGLE_GATE_*`, `P5_H31_SECONDARY_GATE_EXCLUSION.md` | `l=0` family divisor (closed); marked-basis bundle (closed); preferred-chart nonzero divisor, Schubert line at infinity, internal `E=0` divisor (closed); 21 toric boundary orbits (closed); rank-one gate strata (closed) | **closed** |
| 2 | diagonal-quadric `(3,3)` | `P5_H31_DIAGONAL_QUADRIC_ELLIPTIC_GENERIC_OBSTRUCTION.md` + eight companion divisor docs + `P5_H31_DIAGONAL_QUADRIC_OUTER_BOUNDARY_OBSTRUCTION.md` | conic-ratio divisors `U=0`, singular fibres `r=+-1` (elliptic `r`, not the `H22` slope), `H=+-1` rulings, factored slice `C(C+1)(1-E^2)=0`, marking divisors `t2=x`, `t3=1`, pivot divisors `t0=0,t3=1,t2=r^2x`, normalization boundary `rxD=0`, genus-two trisection, outer `ABF=0` gauge boundary | **closed** |
| 3 | `L_1` split cubic | `P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md` (9),(15) | parameter divisors `D=0, G=0, S=0, G+S=0` (identity denominator `8DG(G+S)`), marking denominators `S`, `S-D+G`; projective boundary; implicit elimination denominators | generic-only |
| 4 | `L_2` split cubic | same doc, (11),(16),(17) | `D=0, D+G=0, D+G-S=0` (identity denominator `8D(D+G)(D+G-S)`), marking pencil jumps `t_2=G(D+G-S)/(D+G)`, `t_1=S` (closed inside the generic proof); projective boundary; implicit | generic-only |
| 5 | `L_3` split cubic | same doc, (13) | no surviving marking generically (all four `q` projections unit); parameter divisors of those unit certificates implicit; pure-coefficient boundary `DS=0`; projective boundary | generic-only |
| 6 | mixed-orientation | `P5_H31_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md` (5)-(10) | `q=0, d=0, p=0, d+q=0, p+q=0, d+p+q=0` (sheets (6),(8), identities (9): `-p^2q/(d+p+q)`, `d(d+q)/q`, `-(d+q)`; transverse entries (10)); projective boundary; implicit | generic-only |
| 7 | six-dimensional | `P5_H31_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md` (6)-(9) | chart `s=a+c=0`; `u=0` (pure coeff `2su`), `u-v=0` (markings `tau,sigma`); "exceptional parameter specializations deliberately left to the boundary problem"; projective boundary; implicit Fitting denominators | generic-only |
| 8 | disjoint mixed-star | `P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` (6)-(10) | `1-a^2f^2=0` (i.e. `af=+-1`, marking-exactness divisor), `f=0`, `bf+1=0`, `a^2f+b=0` (obstruction ratio `R=f(bf+1)(1-a^2f^2)/(a^2f+b)`); projective boundary; implicit projection denominators | generic-only |

### Weighted `H22` frame

| # | component | certificate doc | excluded loci of the generic proof | status |
|---|-----------|-----------------|------------------------------------|--------|
| 1 | first rank-two | `P5_H22_FIRST_RANK_TWO_COMPONENT_GENERIC_OBSTRUCTION.md` (6)-(8) | slope divisor `r=1` (sheet `B` coefficient `(r-1)`), `H=Z-r+1=0` branch behaviour; parameter/slope divisors `QU=0` (marking `t_0`), `P=0` (marking `t_2`), `C+L=0` (pure coeff), and the implicit denominators of the eight projective-kernel charts; projective boundary | generic-only |
| 2 | diagonal-quadric | `P5_H22_DIAGONAL_QUADRIC_COMPONENT_GENERIC_OBSTRUCTION.md` (9),(18) | the (uncomputed) rank-drop locus of the extension bundle `D_d` (where the displayed `8x8` minors vanish); dense-chart factors `C(C-l)(1-l^2)r=0`; projective boundary.  NOTE: properness transports one exact fibre, so the open divisor list here is *not explicit* — an atlas-level gap distinct from all other components | generic-only |
| 3 | `L_1` | `P5_H22_ONE_THREE_COMPONENTS_GENERIC_OBSTRUCTION.md` (6) | marking denominators `S+G=0, S=0, S-D+G=0`; pure coeff `4DG=0`; slope divisors implicit (five saturated Fitting ideals over `C(S,D,G,r)`); projective boundary | generic-only |
| 4 | `L_2` | same doc, (8) | `D+G=0`; pure coeff `4D(D+G-S)=0`; slope divisors implicit; projective boundary | generic-only |
| 5 | `L_3` | same doc, (4) | binary projections unit generically; divisors implicit; pure coeff `4DS=0`; projective boundary | generic-only |
| 6 | mixed-orientation | `P5_H22_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md` (8)-(10) | sheet coefficients `d+q=0` (sheet `B`), `N=q(d+p+q)=0` (pure coeff); slope divisors implicit in (6) charts and (10) Fitting saturations; projective boundary | generic-only |
| 7 | six-dimensional | `P5_H22_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md` (8)-(9); equal-weight boundary `P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md` | THE explicit list: `s=0, u=0, r=1, r=-1, u=1, u=v, pr-p+1=0` (marking-coupled slope divisor), survivor-degeneration divisor `ru-r+u-v=0` (`B z_g=0`); projective boundary.  `r=1` **closed** at binary level by the equal-weight theorem; `r=-1` and `pr-p+1=0` open | generic-only + one closed slope |
| 8 | disjoint mixed-star | `P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` (2),(3),(5),(5') | slope divisors `r=0, r=1, r=-1`, coupled divisor `af(r+1)-(r-1)=0` (sheet-`t_2` branch); parameter divisors `a=0, b=0, f=0, phi=0, af=+-1, bf=-1, a^2f+b=0, a^2f^2+2bf+1=0, a^2bf^2+2a^2f+b=0, b^2f^2+bf+1-a^2f^2=0`; projective boundary | generic-only → **slope divisors `r=1,-1,0` new-closed (this atlas)**, coupled divisor recorded below |

### Reading the table

Three structural observations, used in Part II:

1. **Slope endpoints are `H31` frames.**  For either pencil the
   projective slope boundary `r in {0, infinity}` degenerates the
   weighted deletion to a coordinate deletion:
   `D_01^0 ~ q=0`, `D_01^infinity ~ q=1`, `D_23^0 ~ q=2`,
   `D_23^infinity ~ q=3`.  Hence the `H31` generic theorems are
   simultaneously the torus-boundary certificates of the `H22`
   pencils, component by component.
2. **`r=+-1` are the equal/opposite-weight slopes.**  On the
   six-dimensional component `r=1` was already closed separately
   (equal-weight theorem).  The disjoint mixed-star component now has
   all four of `r=1,-1,0,infinity` closed on both pencils (Part II).
3. **Only component 7 has an explicitly displayed full divisor list**
   in the `H22` frame; components 1-6 carry implicit
   Groebner-denominator divisors.  Component 2's `H22` exclusion locus
   is not even explicit (properness argument).  Making those lists
   explicit is unfinished atlas work.

## Part II — case study: the slope divisors of component 8 (weighted `H22`)

Setting: `K=C(a,b,f)[phi]/(Phi)`,
`Phi=a^2bf phi^2+a^2f^2-b^2f^2+b^2phi^2-bf-1`, marked bases
`beta_i(t)=beta_i+t_i alpha_i`, fifth-coordinate extensions
`z=(x_0..x_3,y_0..y_3)`, fourteen mixed binary coefficients
`M(t)z=0`, diagonals `A(z)` (word `0000`), `B(z)` (word `1111`); a
genuine binary survivor needs `A(z)B(z) != 0`.

The generic theorem's `t`-free elimination solves the four single-`1`
words for `y_m`; the own-extension coefficients in the `D_23` pencil
carry the factors

```text
mode 0: (r+1)(af-1)(af+1)(bf+1)/(a^2f+b),
mode 1: (r-1)(bf+1),
mode 2: (r-1),
mode 3: (r-1)(bf+1)(a^2bf^2+2a^2f+b)/(a^2f+b),
```

so at `r=1` three of the four denominators vanish and the elimination
fails; at `r=-1` the mode-0 denominator vanishes; the `D_01` pencil
degenerates mirror-symmetrically (three `(r-1)` factors and one
`(r+1)`).

### II.1 Modular reconnaissance (`F_11`, `F_13`, all `p^4` markings)

Script: `explore_p5_h22_disjoint_mixed_star_slope_divisors_modular.py`.

| pencil | slope | mixed rank over all markings | markings with kernel | genuine survivors |
|--------|-------|------------------------------|----------------------|-------------------|
| `D_23` | 2 (control) | 8 off the locus, 7 on it | `p` (the line `t_1=t_2=t_3=0`) | `p-1`/`p` markings, 1 direction each; mode-0 marked rank 4; minors `(0,1,3,7),(0,1,5,7)` never both zero |
| `D_23` | 1 | **7 everywhere** | all `p^4` | **0** |
| `D_23` | -1 | 6 generically, 5 on a sublocus (32 markings at `p=11`, 38 at `p=13`) | all `p^4` | **0** |
| `D_23` | 0 | 7 except one marking (rank 6) | all `p^4` | 1 marking, 10 directions, all with mode-0 marked rank 4 |
| `D_01` | 1 | **6 everywhere** | all `p^4` | **0** |
| `D_01` | -1 | 6 generically, 5 on a `p^2` sublocus | all `p^4` | **0** |
| `D_01` | 0 | 7 everywhere | all `p^4` | **0** |

The `D_23` `r=0` survivor marking is `t_1=t_2=t_3=0` with
`t_0` the root of the `H31` linear form `L_2` — verified numerically:
at `p=11`, `(a,b,f,phi)=(1,2,7,3)` gives `t_0=4`, exactly the observed
survivor.  This confirms the frame identification
`D_23^0 = H31 q=2` (and `D_01^0 = H31 q=0`, which has unit
projection: no survivors, matching the table).

### II.2 The `r=1` closure (both pencils) — exact identities

Script: `verify_p5_h22_disjoint_mixed_star_slope_r1_binary_obstruction.py`
(sympy, exact mod `Phi`; ~31 s; ledger
`r1_binary_obstruction_verified.json`).  All statements are
polynomial congruences mod `Phi`, valid for **every** marking `t`.

**`D_23` at `r=1`.**

1. *Universal kernel.*  The `y_3` column of all fourteen mixed rows
   vanishes identically.  Hence every marking has the
   marking-independent kernel line `z=e_{y3}`, on which `A=0` and
   `B=4`: a pure-reconstruction direction, the exact analogue of the
   ubiquitous `q=1` kernel on the six-dimensional component.  The
   mixed rank is exactly seven: rank `<=7` for every marking by the
   universal kernel, and the `7x7` minor on rows
   `(0001,1000,1001,1010,1011,1100,1110)`, columns `x_0..x_3,y_0..y_2`,
   at `t=0` equals
   `2^15 a b^3 f (a-b)(a+b)(a^2f+b)(bf+1)^4(a^2bf^2+2a^2f+b)W_NUM`
   mod `Phi`, nonzero (`rank7_witness_r1_d23.py`); modularly rank is
   seven at every one of the `p^4` markings for `p=11,13`.
   Equivalently: at `r=1` the weighted three-row subconfiguration of
   planes `U_0,U_1,U_2` is itself a pure `P_3`-type compression — all
   its mixed `3x3` weighted permanents vanish on `Phi=0` and only the
   all-`beta` permanent (`=4`) survives.
2. *Diagonal concentration.*  `A = A0*x_0` with
   `A0 = 4b(af-1)(af+1)(bf+1)` (up to the unit `W=b(a^2f+b)` used for
   `phi`-reduction), a nowhere-vanishing unit of `K`.  So genuine
   requires `x_0 != 0`.
3. *Seven rows collapse.*  Every mixed word with `bits_0=0`
   (`0001,0010,0011,0100,0101,0110,0111`) is a multiple of `x_0`.
4. *Two-row combination identity* (all eight slots, mod `Phi`):

   ```text
   A0*M_0011 - (E3 + A0*t_3)*M_0010 = A0*V*x_0,
   ```

   where `E3` is the `t`-free part of the `0001`-row `x_0`
   coefficient and `V` (reduced value `-4af`) is the `t`-free part of
   the `0011`-row `x_0` coefficient; `A0` and `V` are units.  On any
   kernel vector the left side is `0`, so `x_0=0` and `A(z)=0`.

   **Conclusion: the `D_23` pencil has no genuine binary survivor at
   `r=1`, for any marking — the divisor closes at binary level,
   before any third target row is considered.**

**`D_01` at `r=1`.**

1. *Universal two-dimensional kernel* `e_{y1}, e_{y2}` (`A=0`, `B=4`
   on each): a double pure-reconstruction.
2. `A = A0'*x_3`, `A0' = 4ab*phi*(bf+1)(a^2f^2+2bf+1)`, a unit.
3. Every mixed word with `bits_3=0` is a multiple of `x_3`.
4. Two-row combination identity:

   ```text
   (C1 + A0'*t_1)*M_0010 - A0'*M_0110 = C1*C2*x_3,
   ```

   with `C1` (reduced `-4phi(bf+1)`) and `C2` (reduced `-4phi`)
   units.  Hence `x_3=0`, `A(z)=0` on every kernel vector.

   **Conclusion: the `D_01` pencil has no genuine binary survivor at
   `r=1` either.**

Since every `(a,b)`-support subfamily of `H22` requires at least one
sharp pencil with a genuine binary survivor, and both pencils are
empty at slope 1, **the slope divisor `r=1` of the generic
weighted-`H22` theorem on the disjoint mixed-star component is closed
over the generic component point**.  This is the exact analogue of the
six-dimensional equal-weight theorem, with the same two-row texture
(`M_1000=(t_0-1)A`, `(u-v)M_1110=-GA` there; the combination
identities above here).

Independent corroboration: Rabinowitsch Groebner certificates
`ideal(14 rows, Phi, w*A*B-1) = (1)` in Singular (instantaneous), and
the full `F_11`/`F_13` marking censuses.

*Left open at `r=1`:* intersections with the parameter divisors
dividing the displayed units (`a, b, f, phi, af+-1, bf+1, a^2f+b,
a^2f^2+2bf+1, a^2bf^2+2a^2f+b` and the `W`-powers), and the
projective boundary.

### II.3 The `r=-1` closure (both pencils) — Groebner units

Script: `probe_rabinowitsch.py`; both certificates

```text
ideal(14 mixed rows at r=-1, Phi, w*A(z)*B(z)-1) = (1)
```

return the unit ideal (Singular `std`, < 1 s each), for `D_23` and
`D_01`.  Hence **neither pencil has a genuine binary survivor at
`r=-1` for any marking: the `r=-1` slope divisor closes at binary
level over the generic component point.**

Structure behind it (exact congruences in
`verify_p5_h22_disjoint_mixed_star_slope_rm1_binary_obstruction.py`):
at `r=-1` the entire slot-0 column pair (`x_0` and `y_0`) of all
sixteen words vanishes mod `Phi` for `D_23` (slot-3 pair for `D_01`),
giving a marking-independent TWO-dimensional kernel with `A=B=0` on
it — a reconstruction plane rather than a line, which is why the
generic mixed rank drops to six.  Ledger:
`rm1_binary_obstruction_verified.json`.

### II.4 The `r=0` boundary slopes — `H31` frames

`r=0` lies on the boundary of the residual source torus (one weight
vanishes), and `D_01^0, D_23^0` are literally the `H31` frames
`q=0, q=2`; `r=infinity` gives `q=1, q=3`.  Consequently:

* `D_01` at `r=0`: no genuine binary survivor for any marking.  The
  direct 14-variable Rabinowitsch attempt TIMED OUT at 550 s (null
  result, recorded); the closure instead follows from the exact frame
  identification (`verify_slope_boundary_frame_identifications.py`)
  plus the already-verified `H31` `q=0` UNIT projection of
  `verify_p5_h31_disjoint_mixed_star_component_generic_obstruction.py`.
  Modular: 0 survivors among all `p^4` markings at `p=11,13`.
* `D_23` at `r=0`: genuine survivors exist (the `H31` `q=2` marking
  `t_1=t_2=t_3=0`, `L_2(t_0,phi)=0`; the lone `p=11` survivor `t_0=4`
  equals the `L_2` root), so the closure is ternary.  It follows BY
  IDENTIFICATION: the frame equality transports the verified `H31`
  `q=2` statement — exact projection ideal EQUALITY
  `(Phi,t_1,t_2,t_3,L_2)` plus the all-extension identity
  `det P_2[0,1,3,7]=R A B^2`, `R` nonzero — to the `H22` pencil
  verbatim; a rank-four one-marked contraction excludes any ternary
  local map, `H31` or `H22` alike.  Independently, since all four
  single-`1` elimination denominators are NONZERO at `r=0` (their
  `(r-1),(r+1)` factors evaluate to `-1,+1`), the generic theorem's
  `y`-eliminated `10 x 4` system `G` is valid there, and a chart-free
  in-frame certificate over ALL markings was attempted:
  `ideal(G(t)x rows at r=0, Phi, det D0[0,1,3,7], det D0[0,1,5,7],
  w*A(x)B(x)-1)` in `(phi,t0..t3,x0..x3,w)`
  (`verify_p5_h22_disjoint_mixed_star_slope_divisor_symbolic_fitting.py`,
  case `r0`; status in `special_slope_reduced_fitting_results.json`).
  (A first attempt with chart certificates on the full `14 x 8`
  system exceeded the 550 s budget — recorded as a null result; the
  reduced-system design replaced it.)

### II.5 The coupled divisor `af(r+1)-(r-1)=0` (`D_01` sheet branch)

On this divisor the generic `D_01` proof loses two things at once:
the global one-minor marking certificate (its unit factor list
contains `af(r+1)-(r-1)` itself), and the sheet-`t_2` branch marking
`(af(r+1)-(r-1))t_1=r+1`, which escapes to `t_1=infinity` (the branch
becomes empty since `r+1=2/(1-af) != 0` there).  Parametrizing the
divisor by the rational slope `r_c=(af+1)/(1-af)` keeps everything
inside `C(a,b,f)`; all four elimination denominators remain nonzero
(`r_c-1=2af/(1-af)`, `r_c+1=2/(1-af)`), so the reduced system `G`
survives.

Modular structure on the divisor (`p=11` slope `6`, `p=13` slope `5`;
`explore_coupled_divisor_modular.py`,
`analyze_coupled_divisor_survivors_modular.py`): exactly FOUR genuine
survivor markings —

```text
one on the sheet t_2=t_3=0;
two on the sheet t_1=0, phi(t_0-1)=f  (one of them with t_3=0);
one NEW point t_1=t_2=t_3=0 with a special t_0
    (t_0=8 at p=11, t_0=10 at p=13; NOT on phi(t_0-1)=f).
```

On the new point the mode-ZERO one-marked contraction has rank
THREE — all seventy of its `4x4` minors vanish — so the generic
theorem's mode-zero Fitting certificate provably fails on this
divisor; this is the only place in the slope atlas where a generic
certificate breaks rather than degenerates.  The obstruction moves to
another mode: every genuine survivor has mode-1,2,3 one-marked rank
four, with common nonzero minors across both primes

```text
mode 1: (0,4,5,7);   mode 2: (0,4,5,7);
mode 3: (0,2,4,7),(0,2,6,7),(0,3,5,7),(0,4,5,7),(0,4,6,7).
```

Char-0 certificate attempt
(`verify_p5_h22_disjoint_mixed_star_slope_divisor_symbolic_fitting.py`,
case `coupled`): one chart-free Fitting run with the slope kept as a
ring VARIABLE and the divisor polynomial `af(r+1)-(r-1)` adjoined to
the ideal — `ideal(divisor, Phi, G(t)x rows, det D3[0,2,4,7],
det D3[0,4,5,7], w*A(x)B(x)-1)` in `(phi,r,t0..t3,x0..x3,w)`, all
permanents computed inside Singular (program
`scripts/coupled_program.sing`, log
`scripts/coupled_singular_run.log`).  The four on-divisor denominator
unit certificates PASSED, certifying the reduced system is valid on
the whole divisor; the main Groebner hit the 550 s budget —
**timeout-null**, recorded in
`special_slope_reduced_fitting_results.json`.  The divisor therefore
remains OPEN at characteristic zero, with the complete modular
picture above and two natural next moves: (i) rerun with the `H31`
verifier's block ordering `(dp(extension),dp(marking))` + `slimgb`
(the pattern that succeeded where plain `dp` stalled), (ii) split
into the four sheet strata first (each fixes at least two `t`'s).

### II.6 Component-8 slope-divisor scoreboard

| divisor | pencil | survivors? | closure level | certificate |
|---|---|---|---|---|
| `r=1` | `D_23` | none | binary | two-row identity (II.2) + Rabinowitsch + modular |
| `r=1` | `D_01` | none | binary | two-row identity (II.2) + Rabinowitsch + modular |
| `r=-1` | `D_23` | none | binary | dead-column congruences + Rabinowitsch (II.3) |
| `r=-1` | `D_01` | none | binary | dead-column congruences + Rabinowitsch (II.3) |
| `r=0` | `D_01` | none | binary | `= H31 q=0` unit projection (identification; direct Rabinowitsch timed out, null) |
| `r=0` | `D_23` | one marking sheet | ternary | `= H31 q=2` theorem (identification; frame equality verified).  In-frame chart-free re-derivation: denominator units certified, main Groebner timeout-null at 550 s |
| `r=infinity` | `D_01` | none | binary | `= H31 q=1` unit projection (identification) |
| `r=infinity` | `D_23` | one marking sheet | ternary | `= H31 q=3` theorem (identification) |
| `af(r+1)-(r-1)=0` | `D_01` | four markings | OPEN (ternary attempted) | mode-3 chart-free Fitting: on-divisor denominator units certified, main Groebner timeout-null at the 550 s budget; modular evidence complete (II.5) |
| slope x parameter intersections | both | unknown | open | not attempted |

## Part III — cross-component transfer targets

The `r=1` mechanism (universal reconstruction kernel + concentrated
diagonal + two-row combination identity) is not specific to component
8.  The same recipe should be attempted, in order of expected ease,
on:

1. component 7 `r=-1` (the opposite-weight slope left open by the
   equal-weight theorem) and the coupled divisor `pr-p+1=0`;
2. component 1 `r=1` (sheet-`B` coefficient `(r-1)t_3+H`) and the
   `H=0` locus;
3. components 3-6: extract the implicit slope divisors first (rerun
   the generic eliminations tracking denominators), then specialize;
4. components 9-11 (all-rank-one triangle, coincident-support,
   equal-support sixfold): these have NO `H31`/`H22` generic theorems
   yet — the generic obstruction must come first, and only then do
   their divisor rows enter Part I.  The ninth has an exploratory
   modular `H31` census (line-shaped marking loci) as a starting
   point.

The `r in {0,infinity}` endpoints of every component's `H22` pencils
are its `H31` `q`-frames, so the corresponding `H31` generic theorems
transport there exactly as in II.4; making that transport explicit
per component is mechanical but unfinished.

Concrete recipe for the next target (component 7 at `r=-1`): rebuild
the sixteen-word system over `C(s,d,u,v)` at slope `-1` with the
apolar basis of the six-dimensional theorem, tabulate the `4 x 8`
pattern-permanent table (32 weighted `3x3` permanents), read off dead
columns/universal kernels, then either a two-row identity or the
14-variable Rabinowitsch (`probe_rabinowitsch.py` pattern).  The
selected `6x6` minor (8) of that theorem has the factor `(r+1)^3`, so
the mixed rank drops by at least one at `r=-1` — the same signature
that preceded the component-8 collapse.

## Appendix — equation-level "where stated" index

For every generic-only row of Part I, the precise places the open
divisors are visible:

| component/frame | divisor | where stated |
|---|---|---|
| 3-5 / H31 | `8DG(G+S)`, `8D(D+G)(D+G-S)` identity denominators | `P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md` (15),(16) |
| 3-5 / H31 | marking denominators `S+G`, `S`, `S-D+G`, `D+G` | same doc (9)-(12) |
| 6 / H31 | sheets and identities `(d+q)(p+q)`, `pq/(d+q)`, `p(p+q)/(d+p+q)`, `(d+p+q)/d`, `-p^2q/(d+p+q)`, `d(d+q)/q`, `-(d+q)` | `P5_H31_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md` (6),(8),(9) |
| 7 / H31 | `tau=(1-u)/(u-v)`, `sigma=sv/(u-v)`, `T_BBBB=2su`, chart `s!=0` | `P5_H31_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md` (2),(3),(6),(7) |
| 8 / H31 | `L_q` sheets need `1-a^2f^2!=0`; ratio `R=f(bf+1)(1-a^2f^2)/(a^2f+b)` | `P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` (6)-(10) |
| 1 / H22 | `Z,H,U,P,R,E` slope-coupled coefficients; sheets `t_3=0`, `(r-1)t_3+H=0` | `P5_H22_FIRST_RANK_TWO_COMPONENT_GENERIC_OBSTRUCTION.md` (6)-(8) |
| 2 / H22 | rank-8 open set of `D_d`; specialization `(C,E,l,r)=(-2/3,-1/4,2,2)`; minors (9) | `P5_H22_DIAGONAL_QUADRIC_COMPONENT_GENERIC_OBSTRUCTION.md` (7)-(9),(18) |
| 3-5 / H22 | markings (6),(8): `S+G`, `S`, `S-D+G`, `D+G`; pure coeffs (1) | `P5_H22_ONE_THREE_COMPONENTS_GENERIC_OBSTRUCTION.md` |
| 6 / H22 | relations (8), sheets (9): `d+q`, `pq`, `p-d` | `P5_H22_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md` |
| 7 / H22 | minor (8) `-2s^2u^2(r-1)^2(r+1)^3(u-1)(u-v)^2(pr-p+1)`; diagonals (9) incl. `B z_g=2(ru-r+u-v)/(u-1)` | `P5_H22_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md` |
| 8 / H22 | elimination denominators (2),(3); unit factor list of (5) incl. `r`, `r-1`, `r+1`, `af(r+1)-(r-1)`; sheet branches (5'),(6') | `P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` |

The `H22` correspondence between support subfamilies and pencils
(used throughout Part II): if the `H22` coefficient `a` is nonzero
the `{0,2}` plane needs a sharp `D_01` extension; if `b` is nonzero
the `{1,2}` plane needs a sharp `D_23` extension
(`P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md` (13)-(14)).

## Honest gaps

* Parameter divisors and projective boundaries remain open for
  components 3-8 in both frames (components 1-2 are closed for
  `H31`; no component is closed beyond the generic point for `H22`
  except the slope divisors of component 8 recorded here and the
  equal-weight slope of component 7).
* The implicit (non-displayed) Groebner denominators of the generic
  `H22` proofs for components 1-6 have not been extracted; the
  component-2 `H22` exclusion locus is not explicit at all.
* The coupled divisor `af(r+1)-(r-1)=0` — see `findings.md`.
* All new certificates are function-field statements; the
  slope-divisor × parameter-divisor intersections are untouched.
