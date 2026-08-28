# Four-root torus-star equal-leaf survivor rank-eight two-leaf slice Fitting exclusion

## Status

**Exact characteristic-zero finite-slice theorem (GLD91).** Work over
K=Q(i) and then extend scalars to C. On the named GLD84 rank-eight
Schur chart

~~~text
R_8=(0,1,2,3,4,5,6,7),
~~~

restrict the six leaf variables to the two-leaf slice

~~~text
x9=1, x10=x11=x12=0, x13=t, x14=u, x8=0.
~~~

The exact lifted Schur residual ideal on this slice has eleven geometric
points counted by the degree-eleven resultant. Five points lie on the
degree-five Q5 component and satisfy mu_R=0; two further points have
mu_R=0; three mu_R != 0 points lie on the centre-frame boundary; and the
remaining point is the pinned GLD85 point. At that remaining point the
full intrinsic GLD83 Fitting map has rank 45. Consequently

~~~text
V(I_Pl) intersect D(mu_R * Omega) intersect (this two-leaf slice) = empty.
~~~

Here Omega includes the centre and leaf frame factors and the fixed gauge
factor. This is an exact exclusion on one two-dimensional slice. It is not
a unit-ideal proof for the full six-leaf rank-eight chart, and it does not
resolve the Krenn--Gu conjecture.

The global conjecture remains **UNRESOLVED**. Other points of the six-leaf
chart, the other 44 rank-eight charts, rank-seven and lower-rank strata,
other survivor components and gauges, source branches, and all other graph
and root profiles remain open.

The owning upstream results are the [GLD83 bordered-Pluecker/Fitting
reduction](FOUR_ROOT_TORUS_STAR_SURVIVOR_BORDERED_PLUCKER_FITTING_OPEN_NONEXTENSION_THEOREM.md),
the [GLD84 centre-rank Schur cover](FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_CENTER_RANK_DETERMINANTAL_CHART_REDUCTION_THEOREM.md),
and the [GLD85 full-intrinsic nonzero point](FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_RANK_EIGHT_FULL_INTRINSIC_FITTING_NONZERO_THEOREM.md).
The exact moving response circuit is the committed
four_root_torus_star_survivor_moving_response_builder.py.

## 1. Exact obligation and slice

Retain the scale-fixed equal-leaf base

~~~text
B = Spec K[x_0,...,x_14]/(g_0,...,g_9,x_8).
~~~

On R_8, write c=(x_0,...,x_7) and z=(x_9,...,x_14). The ten survivor
generators have the exact centre-linear form

~~~text
g=A(z)c+q(z),
~~~

and the Schur localization is

~~~text
K[z,1/mu_R]/(rho_8,rho_9),
rho_k=mu_R q_k-A_(k,*) adj(A_R) q_R.
~~~

The slice used here fixes

~~~text
(x9,x10,x11,x12)=(1,0,0,0),
(x13,x14)=(t,u).
~~~

The fixed centre base is not the real matrix obtained by discarding its
Gaussian offsets. The committed builder gives

~~~text
[[-2-2i, -1+2i, 3],
 [ 0,   -3+3i, 0],
 [ 0,   -1+2i, 1]].
~~~

An earlier exploratory frame-boundary script accidentally used the real
matrix '[[-2,-1,3],[0,-3,0],[0,-1,1]]'. Its frame-boundary output is
withdrawn from this theorem. The primary verifier reconstructs the base
from the committed builder and asserts the displayed Gaussian matrix; the
certificate records it as data. The lifted residual polynomials themselves
were independently recomputed before this correction and are unchanged.

On the corrected slice, rho_8 and rho_9 have total degrees 3 and 4
and term counts 9 and 13. The Schur determinant mu_R has degree 3
and 9 terms. The numerator of the corrected centre-frame determinant has
degree 10 and 54 terms. Its exact Q(i) polynomial is pinned in the
certificate rather than replaced by a numerical determinant.

The exact Schur determinant is

~~~text
mu_R=(-6+30i)*(
 t^3
 +(19/13-35i/13)t^2u +(32/13-9i/13)t^2
 +(-2/13+29i/13)tu^2 +(46/13+22i/13)tu
 +(24/13-10i/13)t
 +(-10/13+15i/13)u^2 +(4/13+20i/13)u
 +6/13+4i/13).
~~~

## 2. Exact residual elimination

The primary computes a Q(i) lexicographic Groebner basis in (u,t) with

~~~text
basis length       = 3,
total degrees      = (9,9,10),
term counts        = (12,12,10),
elimination degree = 10.
~~~

The monic elimination polynomial factors as

~~~text
t (t+2/3) (t+1/5+3i/5) (t+6/13+4i/13) (t+1-i) Q5(t),
~~~

where

~~~text
Q5(t) = t^5
  +(98/65+1444i/585)t^4
  +(-1402/1755+3416i/1755)t^3
  +(-2/5+526i/1755)t^2
  +(-304/1755+272i/1755)t
  -88/1755-56i/1755.
~~~

Q5 is squarefree. The direct residual resultant in u has degree 11
and is the elimination polynomial times (t+2/3), reflecting the two
distinct u fibres above t=-2/3.

Away from t=-2/3, the residual basis contains an affine relation

~~~text
L(t,u)=u-U(t)=0,
~~~

of total degree 8 and 10 terms. The certificate pins its exact Gaussian
rational coefficients. Substitution into the four relevant polynomials and
reduction modulo Q5 gives the exact identities

~~~text
rho_8(t,U(t))       = 0 mod Q5,
rho_9(t,U(t))       = 0 mod Q5,
mu_R(t,U(t))        = 0 mod Q5,
centre_num(t,U(t))  = 0 mod Q5.
~~~

Thus all five geometric Q5 points are outside the Schur localization. No
division by mu_R is used to discard them; the vanishing is recorded as an
explicit closed chart-boundary case.

The corrected residual-plus-centre-boundary Groebner basis has length 2
and its degree-ten elimination polynomial is the same degree-ten polynomial
displayed above. This projection fact is supplemented by the exact fibre
table below; it is not used as an assumption that every projected root has a
single fibre.

## 3. Complete finite fibre table

The six linear fibres are obtained by exact univariate gcds of the two
specialized residuals. The table records mu_R, the exact numerator of the
centre-frame determinant, and the leaf determinant. A zero centre numerator
is interpreted as a centre-frame boundary only when mu_R != 0.

| (t,u) | mu_R | centre numerator | leaf determinant | classification |
|---|---|---|---|---|
| (0,-3/5+i/5) | 0 | 0 | -2/5-6i/5 | Schur boundary |
| (-2/3,-2/3) | -92/3+44i/3 | 0 | -1/3-i/3 | centre-frame boundary |
| (-2/3,0) | -140/9-20i/9 | nonzero | -1-i/3 | the pinned GLD85 point |
| (-1/5-3i/5,0) | -576/125-3168i/125 | 0 | -8/5-4i/5 | centre-frame boundary |
| (-6/13-4i/13,-5/13+i/13) | -3264/169-1344i/169 | 0 | -12/13-8i/13 | centre-frame boundary |
| (-1+i,0) | 0 | 0 | 0 | Schur boundary |

At the pinned point, the corrected centre determinant is
1584/25+3312i/25, so all four frame determinants are nonzero. The exact
fibre table has six linear points plus the five Q5 points, matching the
degree-eleven resultant. Hence exactly one residual fibre lies in the
Schur/frame open.

## 4. Fitting exclusion at the sole open fibre

The sole point in the named Schur/frame open is

~~~text
(t,u)=(-2/3,0),
~~~

with the eight centre shifts pinned by GLD85. GLD85's exact upstream
certificate gives rank(C_F)=13 and a full intrinsic quotient map of shape
45 x 6240. Its selected 45 x 45 full-intrinsic minor has nonzero exact
reductions

~~~text
9639769 + 249939722 i  (mod 1000000007),
1610829 +   5232695 i  (mod 10000019),
~~~

with all 6240 exact denominator slots units at both primes. Therefore the
full intrinsic Fitting ideal I_Pl is nonzero at this sole open fibre. Since
there are no other residual points on the slice in D(mu_R*Omega),

~~~text
V(I_Pl) ∩ D(mu_R*Omega) ∩ (two-leaf slice) = empty.
~~~

This is a characteristic-zero conclusion: the finite residual classification
is exact over Q(i), and the only Fitting-rank input is the already audited
GLD85 denominator-checked modular certificate. It is not a floating-point,
finite-field sampling, or generic-rank inference.

## 5. Verification and independent audit

Run the primary derivation-side verifier:

~~~powershell
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_survivor_rank_eight_two_leaf_slice_fitting_exclusion.py
~~~

It loads the committed builder, asserts the corrected Gaussian-offset centre
base, derives the two lifted residuals and mu_R, computes both exact
Groebner eliminations, checks the Q5 reductions, reconstructs every linear
fibre, and verifies the pinned GLD85 certificate metadata.

Run the independent audit:

~~~powershell
python -I claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_survivor_rank_eight_two_leaf_slice_fitting_exclusion.py
~~~

The audit imports no repository Python module, SymPy, primary verifier, or
moving builder. It parses the committed sparse Q(i) artifact and uses its
own standard-library Fraction/Gaussian arithmetic to:

- reconstruct and factor the residual and resultant eliminants;
- check squarefreeness of Q5;
- check the affine relation u=U(t);
- recompose all four Q5 substitutions and independently reduce them modulo
  Q5 to zero;
- re-evaluate both residual equations, mu_R, the centre numerator, and the
  leaf determinant at every linear fibre; and
- pin the upstream GLD85 certificate hash, columns, denominator counts, and
  nonzero residues.

The audit does not claim to independently derive the primary's Groebner
basis. Its role is an independent polynomial/certificate replay, while the
primary owns the builder-to-Groebner derivation.

The committed artifact is
four_root_torus_star_equal_leaf_survivor_rank_eight_two_leaf_slice_fitting_certificate.json.
Its canonical LF SHA-256 is
6b3fb7fbd0b62e88b9027f8d94fcf31d86331e67a3d439dc4ef9bb0d03bbf82f.

## 6. Scope fences and next obligation

GLD91 does **not** prove that the full six-leaf pullback of I_Pl is the unit
ideal, nor that its full-chart residual is empty. The exact conclusion is
only the displayed two-leaf-slice intersection.

In particular, this theorem does not cover:

- the other points of the six-leaf rank-eight chart;
- the other 44 rank-eight Schur row charts;
- the 960 rank-seven charts or the rank-at-most-six determinantal branch;
- other equal-leaf components, gauges, frame/support/isotropic boundaries, or
  off-chart source branches; or
- other root orders, graph profiles, source integration/gluing, or the global
  Krenn--Gu conjecture.

The next load-bearing obligation remains the full six-variable rank-eight
Fitting ideal calculation, followed by the other rank-eight charts and the
rank-seven/lower-rank branches. A finite slice exclusion is not a chart
cover and cannot be promoted to a global theorem without those edges.
