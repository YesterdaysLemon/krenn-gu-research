# Symbolic translation and literature frontier (2 August 2026)

## Scope

This review starts from the current exact frontier, not from a new support
search:

- every `P_m -> Delta_3` restriction has at least `3m+3` nonzero row cells;
- the eliminated `3m+2` equality layer reduced to a bipartite negative-gain
  cancellation graph on two exceptional sources;
- the five-root cell gives coloured quotient-minor equations, but common
  tangent edges do not force a rank-two hidden pair;
- scalar overlay identities are surjective and therefore cannot obstruct the
  cell by themselves.

The goal is to identify mathematical translations that preserve the exact
complex cancellations.  Positive-weight, numerical, finite-field, border,
and asymptotic statements are not silently promoted to proofs of the original
characteristic-zero exact restriction problem.

The strict permanent bound has one immediate transfer that should be kept
separate from the speculative translations below.  Whenever the proved
root--blocker lemmas extract `P_m -> Delta_3`, their active cell support is at
least `3m+3`.  In the one-port case this gives
`I(R,B)+p>=3r+6`, and the graph-only sufficient contradiction
`e_G(R,B)+e_G(B,Q)<=3r+5`.  For exactly two residual nonblockers, the new
torus dichotomy removes the former factorization qualifier on the
non-coordinate branch: `I+p_0+p_1>=3r+9`, while a cut of size at most
`3r+8` forces a nonzero coordinate-monomial residual restriction.  The
exact second-surplus `P_5/P_6/P_7` support staircase is `18/21/24` with
coordinate-forcing cut thresholds `17/20/23`.  Forcing a sparse extraction
globally, or excluding the coordinate branch, is still open.  See
`GRAPH_EXTRACTION_STRICT_SUPPORT_TRANSFER_COROLLARY.md` and
`ARBITRARY_ORDER_TWO_RESIDUAL_STRICT_SUPPORT_STAIRCASE_AND_COORDINATE_FORCING.md`.

## 3 August addendum: selector descent and permanental tomography

### Principal-deletion response decks and a root-parity superselection rule

The formal response jets from Euler--Hessian unmixing are now physical graph
objects.  For the common response `Lambda_Q`, differentiation in any matching
whose covered vertex set is `D` gives exactly `Lambda_(Q minus D)`, independent
of the matching.  Thus `g_e` is the named two-vertex principal-deletion deck,
and every nonzero disjoint entry of `G` is the named four-vertex deck.  The
apparent edge-jet tensor collapses to a much smaller square-free deletion
deck.  A nonzero affine fibre with identical complete present-vertex tensors
but varying pair-deletion tensors proves that arbitrary local evaluations,
polarizations, and finite differences cannot universally simulate the
missing vacuum.

Legal mixed-root exposure has an exact parity law.  For `r` roots and an even
deletion set `D` of size `2k`, its coefficient is the augmented hafnian

```text
Omega_D=haf [ L    H_D ]
              [H_D^T  0 ],
```

or equivalently a sum of root partial matchings times permanents.  It is zero
unless `r` is even and `r>=2k`.  Hence no root-polarization word on the
three-root `P_5` or five-root `P_7` shore contains the even decks needed by
Euler--Hessian unmixing.  This is a structural no-go, not a rank shortage.
Four-root `P_6` is the first compatible branch.  Its existing zero
root--root chart kills the depth-two coefficient, but a clean `2 x 3`
permanental fan has determinant `-2` and can recover all six pair-deletion
faces when its shore and nuisance separation are legally supplied.

The surrounding language is square-free apolar contraction and algebraic
observability.  The parameter-fibre viewpoint is consonant with
[Meshkat--Rosen--Sullivant](https://arxiv.org/abs/1609.07985), but their
state-space framework does not imply this deletion identity or the parity
law.  **Principal-deletion response jet** and the augmented-hafnian legality
criterion are invented objects in this package, proved directly from perfect
matchings.  See
`RESPONSE_JETS_AS_PRINCIPAL_DELETION_DECKS_AND_ROOT_PARITY_LEGALITY_THEOREM.md`.

### Clean P6 selector as a Segre pullback

Assume the parity-compatible four-root selector has one nonzero root--root
shore, an invertible clean `2 x 3` fan `O`, and that all competing depth-zero,
depth-four, root--root, and blocker terms have been killed or subtracted with
the same normalization.  If the isolated depth-two observation is target
diagonal, quotienting the target by its diagonal three-plane and inverting
`O` forces every one of the six labeled deck tensors into that plane.
For each target colour the corresponding six-vector `z` therefore satisfies

```text
O z = mu vec(r s^T),
```

so its exact ideal is the pullback of the three `2 x 2` minors defining
`Seg(P^1 x P^2)`.  This gives a codimension-two, degree-three projective
condition for each colour.  It is a genuine selector equation, not a support
enumeration.

The resulting equation also proves a sharp no-go theorem for a tempting
closure strategy.  For every `O in GL_6(K)` over an infinite
characteristic-zero field, every coordinate of
`O^(-1) vec(r s^T)` is a nonzero bilinear polynomial.  Their product is
nonzero, so the inverse Segre cone always contains a point of `(K^*)^6`.
Three points can simultaneously be chosen with left-factor rank two and
right-factor rank three because the additional minors define nonempty open
conditions.  Consequently invertibility plus GHZ rank one can never by
itself force a face coordinate to vanish.

There is also a fixed exact permanental control.  With
`a(t)=(1,t)`, `b(t)=(1,t^2,t^3)`, and columns
`a(t_i) tensor b(t_j)+a(t_j) tensor b(t_i)`, the fan determinant is

```text
-2 product_(i<j)(t_i-t_j)^2 (t_0+t_1+t_2+t_3).
```

At `(1,2,3,4)` it equals `-2880`, and an explicit 18-entry full-torus deck
maps to three rank-one target slices with active factor ranks `(2,3)`.  A
nonzero root--root bilinear shore can simultaneously vanish at the original
root evaluation and equal one after the selected polarization.  This is an
abstract target-clean response ledger, deliberately not claimed to be a
physical synchronized hafnian deck.

The square-free permanent language is consonant with
[Feinsilver--McSorley](https://arxiv.org/abs/1710.00788), and the generation
of the Segre ideal by `2 x 2` minors is standard; see
[Bernardi](https://arxiv.org/abs/0705.1942).  The clean-selector descent,
universal torus-permission theorem, and explicit permanental fan are the new
problem-specific statements.  The remaining intersection is the physical
hafnian-deck locus, the three fixed target lines, synchronized depth-four
compatibility, and legal nuisance separation.  See
`P6_CLEAN_TWO_BY_THREE_SELECTOR_SEGRE_PULLBACK_AND_TORUS_PERMISSION_THEOREM.md`.

### The P6 scalar face morphism has a section

The pulled-back Segre equations also cannot be cut by an intrinsic scalar
hafnian relation among the six physical faces.  Let an eight-vertex graph
have four core vertices `C` and a four-window `W`.  Given arbitrary values
`y_pq` for the six hafnians on `C union {p,q}`, put every core edge equal to
one, every core--window edge equal to `tau`, and set

```text
a_pq=(y_pq-12 tau^2)/3.
```

The core hafnian is three and its cofactor form is the hollow all-one
matrix, so the bordered-hafnian formula gives each desired value exactly.
This is an affine section of the six-face morphism onto `K^6`, not merely a
dense-image calculation.  Avoiding finitely many values of `tau` puts every
one of the 28 graph edges on the torus.

The same section synchronizes rather than discards the next depth.  All
seventy four-vertex hafnian companions have closed formulas according to
how many window vertices remain, and all thirty-six partner-expansion
stresses for the six faces hold identically.  Therefore allowing the
four-deck to take its induced common-graph value still places no restriction
on the six faces.  For every invertible fan `O`, the physical full-edge-
torus face locus meets `O^(-1)Seg(P^1 x P^2)`.

The boundary is tensorial.  The three explicit pure-colour Segre face
columns can be realized simultaneously as diagonal entries of one block
graph with every edge block invertible.  But the mixed word with colour
pairs `00|11|22` has the unique matching coefficient `-10/3`, not zero.
Thus pure-colour scalar synchronization, scalar four-deck integrability,
fan invertibility, and full support do not imply a target-clean GHZ tensor.
Mixed-colour cancellation and independently prescribed target four-deck
incidence remain open.  See
`P6_PHYSICAL_SIX_FACE_HAFNIAN_SECTION_FOUR_DECK_SYNCHRONIZATION_AND_SEGRE_SHARPNESS.md`.

### Four residuals need only the even Wick tower

The complete residual-cumulant theorem originally used every residual
subset.  On the parity-compatible four-residual window, all odd depths can
instead be eliminated.  Normalize the empty, six pair, and full responses
by the empty moment `M`, and write

```text
F_ij=a_ij+P_ij.
```

Physical representability is equivalent to the existence of four common
port-linear forms `L_i` such that `P_ij=L_iL_j`, together with

```text
F_1234=haf(a)+sum_(ij) a_ij P_(Q minus {i,j})+P_12P_34.
```

This is a necessary-and-sufficient even-tower theorem: `log M` reconstructs
the port graph, the constants `a_ij` reconstruct the residual graph, and the
four `L_i` reconstruct the incidence rows.  It yields the observable
division-free equations

```text
N_12N_34=N_13N_24=N_14N_23,
MZ_1234=haf(a)M^2+M sum_(ij)a_ij N_(Q minus {i,j})+N_12N_34,
```

where `N_ij=Z_ij-a_ijM`.  These quartics are not sufficient without the
common-row factorization: a fixed five-port pentad defect makes every
displayed product zero while remaining nonrepresentable.

This is the exact physical layer to intersect with the clean `P_6` Segre
pullback.  The legality gap has also become exact.  The products above are
square-free subset convolutions, while an all-blockers-present target tensor
coefficient supplies only one total blocker set.  Local polarization does
not create the missing blocker-deletion companions.  A new heralded or
target-derived synchronization identity is still required.  The Gaussian
moment-variety and loop-hafnian analogies are supported by
[Amendola--Faugere--Sturmfels](https://arxiv.org/abs/1510.04654) and
[Cardin--Quesada](https://arxiv.org/abs/2212.06067); the even-only
elimination and P6 interface are proved directly here.  See
`FOUR_RESIDUAL_EVEN_WICK_TOWER_AND_P6_SYNCHRONIZATION_THEOREM.md`.

### The exact corrected two-port ideal and its first pentad

The arbitrary-order cofactor decomposition has an exact observable ideal at
one response depth.  For scalar port directions, subtract the common direct
layer and write

```text
k_ij=r_i^T C(A) r_j,                  i!=j.
```

The diagonal values are latent.  Introduce them formally, impose the
`(q+1) x (q+1)` minors of the completed symmetric matrix, and eliminate the
diagonal variables.  The resulting symmetric factor-analysis ideal is
exactly the universal polynomial ideal of the corrected two-port family at
residual order `q`.  This is an equality, not only a necessary rank bound:
one fixed nonsingular hafnian cofactor form realizes every symmetric matrix
of rank at most `q` over the algebraic closure.  For `q>=4`, the existing
complete-support `h=0` residual core already suffices.  Consequently no
further hafnian-specific polynomial involving only one corrected two-port
depth can exist.

At two residuals, write `k_ij=a_i b_j+b_i a_j`.  The map on at most four
scalar ports is dominant.  Five ports are minimal, and their ideal is the
principal degree-five pentad: a fixed 12-term polynomial, alternating under
port permutations and of degree two at every port.  For block ports, evaluate
the five bilinear blocks on arbitrary vectors.  The pentad's complete
coefficient tensor lies in

```text
Sym^2(V_1^*) tensor ... tensor Sym^2(V_5^*),
```

and any nonzero coefficient is a basis-independent, denominator-free
obstruction to a common two-residual channel.  No diagonal completion or
invertible anchor is needed.  A hypothetical Krenn--Gu witness must still
provide five legally compatible corrected port blocks; that exposure is not
yet proved.

This is precisely the algebraic-statistical geometry studied in
[Drton--Sturmfels--Sullivant, *Algebraic Factor Analysis: Tetrads, Pentads
and Beyond*](https://arxiv.org/abs/math/0509390): their model invariants come
from eliminating diagonal entries of symmetric low-rank matrices.  The
identification of the hafnian residual response with that variety, the fixed
torus-zero realization, and the block-port pentad tensor are the new
problem-specific transfer.  See
`RESIDUAL_TWO_PORT_FACTOR_ANALYSIS_IDEAL_AND_FIVE_PORT_PENTAD_THEOREM.md`.

### Root-budget legality and the null-polar pentad no-go

The five-port pentad is algebraically minimal, but its legal exposure has a
new three-colour obstruction.  In a two-residual cell with `m` blockers and
`m-2` roots, the residual-present pair `z_uv` requires deletion depth `m-2`
and therefore sits exactly at the maximal root grade.  The direct pair
`m_uv` requires depth `m`, two beyond the entire root staircase.  Hence
`D_uv=z_uv-hm_uv` is directly eligible on `h=0`, whereas `h!=0` needs a new
synchronized correction mechanism.

Parity is not the decisive obstruction on `h=0`.  Fix two source rows and
contract every mode outside a desired pair in their common null space.  For
each target colour `c`, let `N_c` be the modes where that colour covector
lies in the two-row span.  The permanent identity forces `|N_c|>=2`.  If a
null-polar pair block on `e` is nonzero, some colour survives every
complementary null contraction, forcing `N_c subset e`, hence `N_c=e`.
One colour cannot certify two distinct pairs, so all null-polar contractions
together activate at most three pair blocks—even if a different null vector
is chosen for every pair.

Each of the twelve pentad monomials uses five distinct edges.  Consequently
the determinant-cleared weighted pentad obtained from null-polar shore
values vanishes term by term on every diagonal target identity.  This closes
the marked-star, common-null, and pair-dependent-null fan routes to the
pentad.  It does not close a target-compatible named mixed-label sensor or a
new parameter-jet desingularization of a shore-zero family.  The theorem
combines the factor-analysis circuit with the row-pair incidence quota; see
`LEGAL_FIVE_PORT_PENTAD_WINDOW_ROOT_BUDGET_AND_NULL_POLAR_SPARSITY_THEOREM.md`.

### Primitive-square quotient Hessian and radial complement closure

The singular primitive `P_7` branch admits a second translation through
middle Boolean representation theory.  If `ell Q_B^2=0`, complement symmetry
and the primitive down equations force the full edge-indexed hafnian Hessian
`D` to annihilate every additive edge vector `(u_i+u_j)_(ij)`.  The forced
kernel is the eight-dimensional vertex-incidence space, the six-hafnian
cofactor has all eight vertex row sums zero, and `D` descends to the
20-dimensional quotient `ker R^T`.  On the quotient-determinant open, the
four-/six-hafnian deck reconstructs the primitive edge component uniquely;
the remaining fibre is exactly the additive gauge `b=p+Ru`, with an exact
quotient scalar stress for the top hafnian.  The universal corank-eight bound
is sharp in the ambient 14-dimensional primitive four-set space: a fixed sum
of `(4,4)` polytabloids has a named `20 x 20` catalecticant minor
`2^18*3^6*8117`.  That control is deliberately not promoted to a physical
square or torus graph.

The additive quotient fibre is rigid once primitivity and the edge torus are
restored.  An additive edge change `b -> b+R u` is the Boolean quadratic
change

```text
Q -> Q+ell U,                 U=sum_i u_i z_i.
```

If both endpoints obey `ell Q^2=0`, Boolean Lefschetz injectivity cancels
`ell^2` and gives the exact transition equation

```text
U(Q+Q')=0.
```

Multiplication by a linear form supported on at least five variables is
injective from degree two to degree three.  Therefore every nonzero primitive
gauge has support at most four.  The coefficient on a triple with one vertex
inside the support and two outside then forces every edge within the
complement to vanish.  This proves, for every order at least eight, that the
primitive full-edge torus has no nontrivial additive chord.

At order eight, `ell^2:A_3 -> A_5` is an isomorphism.  After complementing
five-sets its matrix is `2 KG(8,3)`, with spectrum

```text
20^(1), (-12)^(7), 6^(20), (-2)^(28).
```

For any quotient representative `p`, define
`Theta(Q_p)=(ell^2)^(-1)(ell Q_p^2)`.  The complete primitive gauge fibre is
the explicit 56-coordinate quadratic system

```text
Theta(Q_p)+2Q_p U+ell U^2=0.
```

It has at most one solution producing a full-edge graph.  Hence on the
quotient-Hessian open, identical labeled `H_4/H_6` decks determine at most
one primitive torus realization.  This is an identifiability theorem, not an
existence theorem; coordinate-boundary star families show that the torus
hypothesis is essential.  The Boolean `sl_2` language is supported by
[Feinsilver](https://arxiv.org/abs/1102.0368), while the additive-chord law,
support-four boundary, and quadratic gauge system are problem-specific.  See
`P7_PRIMITIVE_ADDITIVE_GAUGE_RIGIDITY_AND_COORDINATE_BOUNDARY_THEOREM.md`.

The 35 unresolved leaf quadrics also have a more geometric form.  Modulo the
21 anchor equations they are equivalent to complementary four-hafnian
symmetry.  For a full-support Schur-pencil direction `x`, define a linear
triple vector `u` and a quadratic complementary-four-set vector `v`.  Full
closure is exactly `u wedge v=0`; both vectors are nonzero on the edge torus,
so the affine radial scale is then unique.  On the corank-one pencil stratum,
an adjugate column produces 595 dependent degree-67 equations and an exact
reconstruction.  Rank at most 19 is retained as a separate branch.  The
exceptional value class `a_j=R/4` has size at most four; when its size is four,
the remaining weights `p,q,r`, with `p+q+r=0`, obey

```text
3pqr+2s(pq+pr+qr)+12s^3=0.
```

This combines Boolean `sl_2`, catalecticants, and a determinantal pencil.
Feinsilver supplies the Boolean-lattice representation language
([arXiv:1102.0368](https://arxiv.org/abs/1102.0368)); higher-Hessian and
Lefschetz criteria are standard in
[Maeno--Watanabe](https://arxiv.org/abs/0903.3581), and catalecticant minors
as secant equations are developed by
[Landsberg--Ottaviani](https://arxiv.org/abs/1111.4567).  None of those
sources contains the incidence-kernel theorem, radial complement criterion,
or degree-67 pencil equations proved here.  See
`P7_PRIMITIVE_BOOLEAN_SQUARE_QUOTIENT_HESSIAN_CORANK_AND_TOMOGRAPHY.md` and
`P7_PRIMITIVE_BOOLEAN_SQUARE_COMPLEMENT_RADIAL_AND_EXCEPTIONAL_CLIQUE_THEOREM.md`.

### The quotient-singular P7 branch as an apolar incidence

The deeper quotient-Hessian branch is no longer only the zero set of a
large determinant.  For the primitive middle four-form `H=Q^2/2`, complement
symmetry and the perfect Boolean pairing give

```text
D w=0  iff  wH=0.
```

Thus the forced eight-dimensional incidence kernel is the ideal piece
`ell A_1`, while every additional quotient-kernel direction is a genuine
quadratic annihilator.  This is the square-free Macaulay-apolar meaning of
quotient singularity.

On a seven-leaf radial chart, write the primitive leaf four-form as `N` and
identify the 20-dimensional quotient with the total-zero leaf-edge
hyperplane

```text
G_0={G:sum_(j<k)g_jk=0}.
```

The quotient operator is conjugate to the square linear map obtained by
complementing

```text
Phi_N(G)=G(JN)-(partial G)N.
```

Every entry is linear in `N`.  Its determinant is a nonzero homogeneous
degree-20 polynomial on the 14-dimensional primitive leaf space; a fixed
ambient control has exact determinant

```text
2^24 3^13 7 8117.
```

At rank nineteen the annihilator direction `[G]` is projectively unique;
rank at most eighteen remains as the deeper incidence.  For a physical
radial graph, the entire singular branch lifts to

```text
N=F^2/2,       ell_L N=0,       AF=t JN,
sum g_jk=0,    G(JN)=(partial G)N.
```

In particular it descends to a seven-leaf full-edge primitive-square
problem.  These are quadratic and bilinear equations with auxiliary data,
not the earlier degree-67 elimination.  Their physical edge-torus
intersection is still unknown.  The apolar/catalecticant language is
standard in [Landsberg--Ottaviani](https://arxiv.org/abs/1111.4567), and the
Boolean `sl_2` structure in [Feinsilver](https://arxiv.org/abs/1102.0368);
the conjugacy and radial formula are problem-specific.  See
`P7_PRIMITIVE_QUOTIENT_SINGULAR_APOLAR_RADIAL_BILINEAR_INCIDENCE_THEOREM.md`.

### Switching gauge and uniform-curve secant saturation

Arbitrary-order vertex switching `a_ij -> z_i z_j a_ij` acts on the hafnian
Hessian by diagonal congruence and on the legal companion map by invertible
column scaling.  When graph and sensor are switched together, the full root
tensor changes only by `product z_i`.  Switching is therefore projectively
vertical: it preserves the sensor image, target incidence, flattening ranks,
and Hessian openness and cannot supply a missing GHZ tangent direction.

For the fixed legal sensor and the physical uniform graph `a_uv=t`, two named
`9 x 9` flattening minors have the form

```text
984150 t^18 P_0(t),       98415 t^18 P_1(t),
gcd(P_0,P_1)=1 over Q[t].
```

Consequently every characteristic-zero `t!=0` has flattening rank exactly
nine and border rank at least nine, while every eight-shore Hessian is
invertible.  The entire switching saturation is disjoint from `sigma_8`, not
only from the GHZ variety `sigma_3`.  Ordinary and structured flattenings are
standard secant-variety tools; see the
[Hitchhiker guide](https://arxiv.org/abs/1812.10267) and
[Landsberg--Ottaviani](https://arxiv.org/abs/1111.4567).  The two-minor
saturation certificate and the conclusion that switching is a legal
projective gauge are exact results of this package.  Nonuniform quotient
directions remain unknown.  See
`P7_LEGAL_NONROOT_SWITCHING_COVARIANCE_AND_UNIFORM_CURVE_SECANT_SATURATION.md`.

### Shallow Hessian tomography and affine descent

The arbitrary-order residual inverse no longer needs the complete nested
cofactor tower on its nonsingular Hessian chart.  For `q=2m` residual
vertices, place the two-deletion cofactors in `c` and the four-deletion
cofactors in the edge-indexed hafnian Hessian `D`.  Homogeneous Euler gives

```text
D a=(m-1)c.
```

At the all-one full-edge-torus point, `D=(q-5)!! KG(q,2)`.  The three
Kneser eigenspaces give the exact nonzero determinant

```text
((q-5)!!)^binom(q,2) binom(q-2,2) (-(q-3))^(q-1),
```

so `a=(m-1)D^(-1)c` is a rational inverse on a nonempty open at every even
order.  This also places an etale point of the cofactor polar map inside the
full torus, proving that cofactor-only universal equations cannot obstruct
the residual graph.  The joint jet does have a complete obstruction:
after `delta=det D` and `B=(m-1)adj(D)c`, the nonlinear four-deletion deck
equations

```text
delta^(m-2) d_(e,f)=haf(B[Q minus (e union f)])
```

together with `m delta h=(m-1)c^T adj(D)c` are necessary and sufficient on
`delta!=0`.  The linear Kneser support and four-set pairing shell is not
sufficient for `q>=8`.  This is adjacent to polar Cremona maps,
Artinian-Gorenstein matching algebras, and Hessian/Lefschetz criteria.  It
is not an application of Lorentzian-polynomial theory: the all-one hafnian
Hessian has positive multiplicity `1+binom(q,2)-q`, whereas a Lorentzian
polynomial would have only one positive Hessian eigenvalue.  See
`RESIDUAL_HAFNIAN_HESSIAN_KNESER_ETALE_AND_JET_INTEGRABILITY_THEOREM.md`.

For `P_7`, this invented shallow-Hessian chart is already legal.  On an
eight-shore, the existing full sensor labels exactly the `70` entries of
the `H_4` deck forming `D` and the `28` entries of the `H_6` deck forming
`c`; one Hessian inverse and one cyclic eight-row star system recover all
36 nonroot edges.  The nine eight-shore inverses admit an affine descent
form: local `(H_4,H_8)` physicality plus equality on every overlap is
equivalent to global `H_4/H_6/H_8` physicality, and all 84 separate `H_6`
partner checks become automatic.  `P_5` lacks the needed adjacent depths;
one `P_6` jet has only 81 channels for 70 raw `H_4` plus 28 raw `H_6`
labels.  Nonlinear or multi-jet `P_6`, GHZ incidence on the P7 Hessian open,
and singular-Hessian descent remain unknown.  See
`SHALLOW_HAFNIAN_HESSIAN_TWO_DECK_INVERSION_AND_P7_LEGAL_SENSOR_INTERFACE.md`.

### Euler--Hessian response observability and radial amplitude

The same polar calculus separates common-cofactor response channels without
requiring a larger residual graph.  For a vector-valued response

```text
L=hU+sum_e c_e T_e,
g=cU+DT,
G=DU+J dot T,
```

Euler gives `Da=(m-1)c` and `J dot a=(m-2)D`.  Therefore the newly defined
Euler--Hessian connection

```text
S=G-J dot D^(-1)g
```

cancels all cofactor channels and leaves `S=DU/(m-1)`.  On `det D!=0`, the
first and second response jets recover `U` and every `T_e` uniquely.  When
`h!=0`, value plus first jet already suffice; when `h=0`, they instead obey
one exact vector-space gauge, removed by the second jet.  On the singular
divisor, actual data satisfy the inverse-free equation `adj(D)g=0`; an exact
six-vertex full-torus example shows this has a genuine corank-one branch.
For the arbitrary blocker aggregate, the recovered `T_pq` are honest
`P_(r+2)` extensions.  A three-colour diagonal channel would therefore give
the strict support bound `3r+9` at arbitrary residual order.

This is a sharp observability theorem and a sharp legality wall.  The present
`P_7` sensor exposes the scalar jet `(h,c,D)`, not the tensor response jets
`(g,G)`: formal differentiation of an edge coefficient is not a permitted
local-vector probe.  In neighboring literature, algebraic observability and
identifiability also ask which hidden parameters are determined by output
jets and use algebraic matroids to organize the answer
([Meshkat--Rosen--Sullivant](https://arxiv.org/abs/1609.07985)).  The theorem
here is static, exact, and specialized to the hafnian Euler identities; no
state-space result is being imported.  The higher-Hessian/Lefschetz
connection is similarly supported by the characteristic-zero criterion of
[Maeno--Watanabe](https://arxiv.org/abs/0903.3581), while the rational polar
map viewpoint is classical
([Dolgachev](https://arxiv.org/abs/math/0005048)).  Neither source supplies
the response unmixing formula or its legal physical realization.  See
`ARBITRARY_ORDER_HAFNIAN_EULER_HESSIAN_CHANNEL_UNMIXING_AND_SINGULAR_DISCRIMINANT.md`.

There is a second separation on a target-incidence line.  If
`(h,c,D)=t(h_0,c_0,D_0)`, then `det D` and the adjugate numerator scale so
that the reconstructed graph is projectively constant.  The scalar Euler
stress is also projective, but after the common homogeneous factor is
removed each nonlinear deck equation is affine-linear in `t`.  Thus a
Hessian-open radial line contains at most one nonzero physical jet.  On the
nine `P_7` shores, all determinants, stresses, and overlaps are projective;
all four-deck equations must select one common amplitude.

Two exact controls prevent an overclaim.  The all-one physical deck is in the
common Hessian open and an injective ambient **nonlegal** sensor can send its
line to GHZ, so incidence, dimensions, and rank alone cannot obstruct it.
For the fixed **legal** rank-219 sensor, the same physical deck has a nonzero
named `9 x 9` flattening minor and hence border rank at least nine.  Legal
observability plus physical Hessian openness therefore does not imply GHZ.
The unresolved question is precisely whether a legal torus-concise
rank-three incidence line survives both the projective tests and the common
affine amplitude.  See
`ARBITRARY_HAFNIAN_JET_LINE_PROJECTIVE_AFFINE_SEPARATION_AND_P7_GHZ_BOUNDARY.md`.

The singular complement is no longer an opaque primitive intersection.
Boolean `sl_2` duality identifies the kernels of the up and down operators at
middle degree four, translating `ell Q_B^2=0` into 56 triangle equations

```text
b_ij r_k+b_ik r_j+b_jk r_i
 =2(b_ij b_ik+b_ij b_jk+b_ik b_jk),
r_i=sum_(j!=i)b_ij.
```

All row sums cannot vanish on the edge torus, because their vanishing would
put the reciprocal edge vector in the injective `W_(2,3)(8)` kernel.  At a
vertex with `r_0!=0`, every off-star edge satisfies

```text
[r_0-2(b_0j+b_0k)]b_jk
 =2b_0j b_0k-b_0j r_k-b_0k r_j.
```

Away from the 21 denominator divisors this is a rational star/row-sum normal
form in a projective 14-parameter ambient closure system; on each divisor
the corresponding numerator must vanish, so the exceptional branches stay
visible.  Middle complementation also forces opposite four-set hafnians to
agree, and a separate symbolic argument excludes reciprocal-rank-one edge
data.  Feinsilver's Boolean-lattice `sl_2` representation
([arXiv:1102.0368](https://arxiv.org/abs/1102.0368)) supplies the surrounding
representation-theoretic language; the identities and kernel argument here
are self-contained.  See
`P7_PRIMITIVE_BOOLEAN_SQUARE_DUAL_TRIANGLE_STAR_NORMAL_FORM.md`.

The dual-triangle system also admits a new differential-algebra
interpretation.  Boolean deletion is not a derivation of the zeon product;
its exact collision-corrected rule is

```text
partial_i(fg)=(partial_i f)g+f(partial_i g)
               -2z_i(partial_i f)(partial_i g).      (23a)
```

Since the up and down kernels agree in middle degree, a primitive square is
equivalently the zeon harmonic-square equation

```text
Q(DQ)=sum_i z_i(partial_i Q)^2.                      (23b)
```

Its triple coefficients are the 56 equations above.  Summing them over the
third vertex gives a Hadamard-corrected matrix Riccati law.  If `B=(b_ij)`,
`r=B1`, and `S=sum_i r_i`, then

```text
(B^2)_ij=(S/2-2r_i-2r_j)b_ij+r_i r_j+2b_ij^2.       (23c)
```

Summing (23c) by row and then globally gives

```text
(Br)_i-sum_(j!=i)b_ij^2=r_i(S/2-r_i),
S^2=4(sum_i r_i^2-sum_(i<j)b_ij^2).                 (23d)
```

Thus every real full-edge primitive square must lie strictly outside the
two closed cones `|S|>=2||r||`.  Constant real row sums are impossible, and
the standard deviation of the eight row sums must exceed the absolute
value of their mean.  No complex exclusion is inferred: (23d) uses ordinary
squares, not absolute squares.  Feinsilver's zeon/Boolean-`sl_2` calculus
provides the surrounding language; (23b)--(23d) are the new transfer.  See
`P7_PRIMITIVE_ZEON_HARMONIC_SQUARE_RICCATI_AND_REAL_ROW_CONE_OBSTRUCTION.md`.

The generic part is now resolved by an invented determinantal star-closure
theory.  With seven star weights `a_j`, normalized row variables `y_j`, and
21 normalized off-star edges `x_jk`, the 21 anchor triangles plus seven row
definitions are one homogeneous `28 x 28` pencil

```text
T(a)=[I,-V; U^T,D],
P(a)=det T(a)=det(D+U^T V).
```

The symmetric homogeneous polynomial `P` has degree 21 and
`P(1,...,1)=5*8^6*3^15!=0`.  Every edge-torus primitive-square point lies on
`P=0`; hence the generic star fibre is empty, with no parameter enumeration.
The remaining problem is exactly the incidence of a full-support kernel of
this pencil with 35 displayed leaf-triangle quadrics.  The pencil retains the
exceptional divisors and classifies them by
`Delta_jk=0 iff y_j+y_k=0`.  A separate reciprocal-Cayley argument improves
the zero-row boundary to `|{i:r_i=0}|<=3`.  In elimination language, `P` is
a determinantal projection obstruction, but the elementary Schur-complement
proof is complete and no general determinantal-representation theorem is
being substituted for the 35 unresolved quadrics.  See
`P7_PRIMITIVE_BOOLEAN_SQUARE_STAR_CLOSURE_DISCRIMINANT_AND_ZERO_ROW_BOUNDARY_THEOREM.md`.

### Mixed-root filtration, deletion-label geometry, and a nonlinear escape

The arbitrary mixed-root problem now has an exact matching-filtration
answer.  Restricting a perfect matching to `r` roots gives a partial matching
on the roots and an injection of the remaining roots into the nonroot set.
A term with `j` root--root pairs therefore deletes exactly `r-2j` nonroots.
For the five-root/two-residual `P_7` cell, the direct blocker pair and the
one-residual singleton require depth seven and are absent from every linear
mixed-root word, while the available depths are only five, three, and one.
This is a symbolic support theorem, not an enumeration.  A one-edge
nine-nonroot graph and a nonzero common-shore graph make the linear boundary
physical and sharp.  See
`MIXED_ROOT_DELETION_FILTRATION_AND_HERALD_FREE_PAIR_NO_GO.md`.

The missing deletion labels are governed by a precise algebraic-statistical
observability map.  For a fixed root set `I`, the jet factors as

```text
J_I=sum_A G_A tensor C_(I union A),
Gamma_I:e_A |-> G_A.
```

One named cofactor is determined exactly when its coordinate functional lies
in `im Gamma_I^*`; the full invisible translation space is
`ker(Gamma_I) tensor W`.  There are legal arbitrary-order selector charts
with diagonal entries `(q-|A|-1)!!`, but their common-core root requirement is
not met by the balanced `P_5`--`P_7` cells.  This translation is naturally a
linear inverse problem or algebraic matroid.  If cross-depth observations
also exposed multiplication in the square-free deletion algebra
`K[x_1,...,x_q]/(x_i^2)`, its graded automorphisms would collapse from a
general linear cofactor gauge to permutation and diagonal rescaling.  The
current jets expose vector spaces, not that multiplication.  See
`LOWER_MIXED_ROOT_JET_DELETION_LABEL_TOMOGRAPHY_AND_SQUAREFREE_GAUGE_THEOREM.md`.

### Pinned Lefschetz inversion, a complete P7 sensor, and its incidence wall

The square-free algebra does more than organize the deletion labels.  For a
named graph, pin a vertex `p` and expand every upper hafnian by the partner
of `p`:

```text
h_(p union T)=sum_(s in T) a_ps h_(T minus {s}).
```

At the all-one graph this is a subset-inclusion matrix, or equivalently
multiplication by a power of the Lefschetz element in
`K[z_1,...,z_n]/(z_i^2)`.  The strong Lefschetz property of monomial complete
intersections is the surrounding commutative-algebra theory; Herzog and
Popescu survey the classical result and extensions in
[*The strong Lefschetz property and simple extensions*](https://arxiv.org/abs/math/0506537).
Here a self-contained inclusion-rank proof gives the exact reconstruction
hierarchy.  With surplus `r`, the first `h_(2q)` deck is generically finite
for `r>=2`, while the consecutive `h_(2q),h_(2q+2)` decks rationally recover
every edge for `r>=3`.  At `r=1`, the nonzero all-one fibre is smooth of
dimension `binom(n,2)-n`; this is 27 for the `P_5,q=4` cell and 65 for the
`P_7,q=6` cell.  See
`PINNED_HAFNIAN_STAR_SYSTEM_AND_RATIONAL_EDGE_TOMOGRAPHY_THEOREM.md`.

The five-root `P_7,q=2` selector problem is now solved on a legal graph-side
open chart.  One fixed integer companion operator has all 219 columns
independent, so the 126 four-, 84 six-, and nine eight-hafnian labels are
simultaneously selectable.  Combined with the pinned theorem, this gives a
relative rational inverse for all 36 nonroot edges on a nonempty product
open, with the companion blocks retained as known base parameters.  This is
not a GHZ chart: appending the three pure diagonal target columns gives rank
222, so the sensor image intersects the diagonal target space only at zero.
The nonzero determinant makes the target-incidence condition a proper,
nonvacuous determinantal locus.  Any witness must lie there or on the sensor
rank-drop locus.  See
`P7_FULL_MIXED_ROOT_219_LABEL_SENSOR_AND_PINNED_STAR_GATING_BOUNDARY.md`.

The singular side has an equally exact translation to Gram completion and
rigidity.  On the double star with center pair `p,q` and leaves `i`, the only
nonzero shallow coordinates are

```text
h_(pqij)=x_i y_j+x_j y_i.
```

They form an off-diagonal hyperbolic Gram map.  The completion-matrix idea is
parallel to Singer and Cucuringu's rigidity approach to
[*Uniqueness of Low-Rank Matrix Completion by Rigidity Theory*](https://arxiv.org/abs/0902.3846).
The exact Jacobian here has rank 34 among 36 edge variables: the center edge
and reciprocal shore scaling survive.  Yet a separate ratio argument proves
that the zero four-deck cannot meet the full edge torus for `n>=6` in
characteristic zero.  Thus the generic Lefschetz inverse and the double-star
fibre are two strata of one observation map, not contradictory claims.  See
`P7_COMBINED_SHALLOW_DECK_DOUBLE_STAR_GAUGE_AND_ZERO_TORUS_BOUNDARY.md`.

The proposed **incidence--Lefschetz stratification** now has its first exact
layer.  On a full `P_7` sensor, quotient by the 219-dimensional companion
image.  The resulting 24-dimensional cokernel restricts to a `24 x 3` map on
the diagonal target space.  A nonzero diagonal target occurs exactly when
this map has rank at most two.  Dually, it is the restriction of the
24-dimensional left kernel to the three pure target words.  One exterior
covariant packages all augmented minors.  The corresponding special
Schubert locus in `Gr(219,243)` has codimension 22; intersection dimensions
two and three begin in codimensions 46 and 72.  See
`FIVE_ROOT_DIAGONAL_TARGET_INCIDENCE_SCHUBERT_DUALITY_AND_COFACTOR_LINE_THEOREM.md`.

At a generic incidence point the allowable 219-vector is one
sensor-dependent projective line.  This gives 218 linear relations, but no
nonzero sensor-independent homogeneous relation follows from incidence and
rank alone: every nonzero abstract cofactor vector occurs for some ambient
injective sensor.  The matching form of the companion map and physical
hafnian realizability must therefore do the remaining work.

On the pinned open, that remaining work is explicit.  Eight Cramer star
systems reconstruct all 36 candidate edges projectively.  The first natural
determinant-cleared partner residuals have degree nine in the cofactor-line
coordinates.  Their nonvanishing excludes the whole line.  If they vanish,
126 four-hafnian equations fix at most one nonzero radial amplitude, and one
partner row for each of the 84 six- and nine eight-hafnian labels is a
necessary and sufficient graph-side integrability test.  See
`P7_TARGET_INCIDENCE_DETERMINANT_CLEARED_HAFNIAN_INTEGRABILITY_THEOREM.md`.

Secant geometry supplies an unconditional pressure theorem on the legal
sensor image.  The third secant of `Segre((P^2)^5)` has projective dimension
32, witnessed by the three pure and 30 single-flip tangent words.  Therefore
every projective 218-plane full-sensor image meets that secant in dimension
at least eight.  Root-local `GL(3)^5` changes are legal: with contragredient
root vectors they preserve sensor rank, pairwise-zero roots, contractions,
and symmetric blocks.  Hence any torus-concise honest rank-three point in the
mandatory border family produces a legal diagonal target-incidence chart.
The exact remaining alternative is that the whole family is trapped in the
nonconcise, colliding-summand, lower-rank, or root-coordinate boundary.

At actual incidence the same geometry gives a small tangent criterion.  An
`r`-term diagonal target has `10r` single-flip local-basis directions.  One-
and two-term targets cannot cover the 22-dimensional incidence normal; a
three-term target is locally transverse exactly when the 30-word space maps
with rank 22 modulo `W+Delta`.  See
`P7_LEGAL_LOCAL_BASIS_BORDER_GHZ_INTERSECTION_AND_SINGLE_FLIP_TRANSVERSALITY_THEOREM.md`.

The degree-nine integrability theory also has a legal endpoint-torus action.
Endpoint scaling acts diagonally on companion columns, fixes the full sensor
image and target-incidence subspace, and transforms the pinned candidate graph
by vertex scaling.  Every projective partner, overlap, Euler, and four-deck
stress is a semi-invariant; only the required affine line amplitude moves,
by the total endpoint-product character.  Consequently endpoint magnitudes
cannot force a projective line obstruction.  If a projectively integrable
incidence line exists, affine compatibility cuts exactly one codimension-one
product character on its normalization orbit.  This remains conditional on
existence of the line.  See
`P7_LEGAL_ENDPOINT_TORUS_COVARIANCE_AND_AFFINE_LINE_NORMALIZATION_WALL.md`.

There is now a parallel `P_6` chart.  Set all four-root pair blocks to zero
and use a fixed legal six-blocker/two-residual companion system.  Its 70
depth-four columns are independent in `3^4=81` channels, so every principal
four-hafnian of the eight nonroots is labeled.  The inclusion-matrix
Jacobian gives relative generic finite recovery of all 28 edges.  Appending
the diagonal target raises the fixed rank to 73; ambient target incidence is
the codimension-nine Schubert locus in `Gr(70,81)`.  This proves that `P_6`
passes the legal top-deck sensor threshold, without proving that a GHZ point
meets the sensor or Jacobian open.  See
`P6_FOUR_ROOT_FULL_H4_SENSOR_AND_TARGET_INCIDENCE_BOUNDARY.md`.

The dimension-deficient `P_5` cell now has a different, compressed answer.
Its three-root sensor has 27 channels for 35 four-hafnian labels, and one
fixed legal chart is surjective with kernel dimension eight.  Nevertheless,
the composite map from the 21 nonroot edges to the 27 root-tensor channels
has full Jacobian rank 21 at the all-one graph.  Thus the physical graph is
generically finite over the compressed observation even though the named
four-deck is not linearly recoverable.  This is exactly the structured-
variety viewpoint of Breiding--Gesmundo--Michalek--Vannieuwenhoven,
[*Algebraic compressed sensing*](https://arxiv.org/abs/2108.13208), now with
a legal fixed rather than generic measurement operator.

It also suggests the **compressed target-incidence correspondence**.  The
projective four-hafnian image `X subset P^34` has dimension 20.  For a
surjective sensor `Gamma`, the inverse image of the three-dimensional
diagonal target is an 11-plane.  The incidence calculation

```text
20+dim Gr(10,34)=260 < dim Gr(11,35)=264
```

puts arbitrary surjective sensors that can meet a nonzero physical target
inside an ambient locus of codimension at least four.  Formal target fibers
are automatic, but physical target incidence is exceptional.  The legal
pullback of this locus remains unknown.  For branch control, the exact next
object is the collision scheme
`{(A,A'):F_4(A)-F_4(A') in ker Gamma}`, with its unavoidable diagonal and
sign components.  See
`P5_COMPRESSED_H4_PHYSICAL_TOMOGRAPHY_AND_TARGET_TANGENT_BOUNDARY.md`.

The determinant boundary itself has a square-free circuit theory.  For the
eight-vertex shore of `P_7`, a kernel vector of the pinned four-hafnian matrix
is a degree-one annihilator of `Q_B^2` in the square-free algebra.  On the
full edge torus every such dependency has support exactly eight.  Supports one
through four are excluded by zero-deck torus rigidity, injectivity of a
triangle-star map, and a hyperbolic-product independence argument.  Support
five is excluded by a new conic reduction: after gauge normalization the five
cross stars lie in one plane, a pair-product isomorphism identifies the
three-support equations modulo a nondegenerate binary quadratic, and its two
linear factors reduce to full-rank triple-incidence systems.  Support six is
excluded by a second exact incidence reduction.  Three-support rows polarize
all 15 internal edges through two cross-stars; four-support rows become the
`W_(2,4)(6)` image of a reciprocal polarization edge form.  That square
inclusion matrix has determinant `1458`, forcing the form to vanish and then
contradicting the edge torus.  Support seven is the clean Boolean-Lefschetz
case: its single-complement row operator factors as edge-to-triangle
inclusion followed by multiplication from square-free degree three to degree
four on seven variables.  The first map is injective and the second is the
middle Lefschetz isomorphism, so every internal edge would vanish.  The only
remaining torus branch has the exact intrinsic equation `ell Q_B^2=0` in the
eight-variable square-free algebra.  Thus `Q_B^2` lies in the 14-dimensional
primitive kernel of `A_4 -> A_5`; the open question is whether this primitive
Boolean-square locus meets the 28-edge torus.  This is
compatible with the strong-Lefschetz viewpoint; Cook's
[*The Lefschetz properties of monomial complete intersections in positive characteristic*](https://arxiv.org/abs/1111.4979)
records the characteristic-zero monomial-complete-intersection background,
while the circuit proofs here are self-contained.  See
`P7_PINNED_H4_TORUS_SUPPORT_FIVE_BINARY_QUADRATIC_EXCLUSION.md`,
`P7_PINNED_H4_TORUS_SUPPORT_SIX_RECIPROCAL_POLARIZATION_EXCLUSION.md`, and
`P7_PINNED_H4_TORUS_SUPPORT_SEVEN_BOOLEAN_LEFSCHETZ_EXCLUSION.md`.

The smaller `P_6` boundary has an exact cubic escape.  Over `Q(omega)` with
`omega^2+omega+1=0`, one all-edge-nonzero seven-vertex graph has pinned rank
six, kernel `e_5+e_6`, and nonzero four- and six-hafnian coordinates.  Its
five-vertex core is the complete classification of an all-nonzero zero
four-deck: the three opposite-edge products occur in ratio
`(omega^2,omega,1)`.  Therefore coordinate nonvanishing cannot force the
`P_6` pinned open.  On any incidence cofactor line, each fixed pinned minor
is homogeneous, so the whole nonzero line is either inside or outside that
minor's open chart.  See
`PINNED_H4_STAR_TORUS_CIRCUIT_GIRTH_AND_P6_CUBIC_ESCAPE.md`.

The next decisive theorem must now act on the **legal pullback** of these
incidence loci: either show it is empty on the full-sensor/pinned open, force
one of the explicit degree-nine or four-deck stresses to be nonzero, or
classify its descent to coordinate/Gram singular strata.  The surviving
torus cases are now precise: the single full-support-eight `P_7` pinned
branch and the `P_6` cubic-resonance alternative.  Neither is currently forced
or excluded by the GHZ equations.

There is, however, a genuinely nonlinear way around the depth ceiling on a
generic chart.  For a named `n`-vertex graph, send its edges to all principal
four-vertex hafnians

```text
h_ijkl=a_ij a_kl+a_ik a_jl+a_il a_jk.
```

At the all-one graph the Jacobian is the classical subset-inclusion matrix
`W_(2,4)(n)`.  A direct kernel argument proves full column rank for `n>=6`,
so the edge field is finite algebraic over the four-hafnian field.  The
inclusion-matrix connection sits inside the integral diagonal-form theory of
Ghorbani, Khosrovshahi, Maysoori, and Mohammad-Noori,
[*Inclusion Matrices and Chains*](https://arxiv.org/abs/0709.3144), while the
generic-finite conclusion is the algebraic-identifiability translation.
For the nine nonroots of `P_7`, the full sensor theorem above supplies those
labels on a legal open and hence recovers all 36 edges up to finitely many
algebraic branches even before the stronger consecutive-deck inverse is
used.  The one-edge line lies in the zero deck fibre, and `A` and `-A` share
a deck, so singular stratification and branch selection are indispensable.
The 126 deck labels cannot fit in one `2^5=32` two-plane root jet, but the
complete 219-label shallow system does fit, and is attained, in the full
`3^5=243` root tensor.  See
`PRINCIPAL_FOUR_HAFNIAN_GENERIC_EDGE_TOMOGRAPHY_AND_P7_SINGULAR_FIBRE_BOUNDARY.md`.

The two-fan co-occurrence problem also has a projective-geometric reduction
on the actual five-root cell.  Two root pairs are equal, share one root, or
are disjoint.  Under complementary-row nondegeneracy, the common kernel of
two shared-root fans is the kernel of four evaluations of a binary quadratic
on the common root's two-plane.  It vanishes off a second-Veronese boundary.
If all ten shores are available and neither a transverse fan wedge nor a
Veronese-boundary root occurs, the five row-lines in `P^3` are pairwise
incident and hence all concurrent or all coplanar.  Explicit common
graph-side `P_7` sectors attain both the transverse rank-six case and the
sharp rank-five boundary.  The classical projective-line alternative is
therefore useful, but target GHZ equations are still needed to force one of
its obstructive branches.  See
`P7_FIVE_ROOT_TWO_FAN_SHARING_AND_SHARED_ROOT_VERONESE_TRANSVERSALITY.md`.

Together these translations reorganize the frontier:

```text
linear mixed-root access to the pair:       IMPOSSIBLE BY DEPTH;
named P7 shallow cofactor exposure:         PROVED ON A LEGAL OPEN;
relative rational P7 edge recovery there:  PROVED;
diagonal target incidence on sensor open:  PROPER DETERMINANTAL LOCUS;
singular shallow-deck fibres:               NONEMPTY AND PHYSICAL;
actual five-root two-fan geometry:           CLASSIFIED;
GHZ forcing of incidence/pinned branch:      UNKNOWN.
```

The current obstruction is best viewed as an inverse problem with a graded
legality constraint.  For a residual subset `T` and port subset `S`, a
root-saturated principal-cofactor observation can occur only when

```text
|S|+|T|>=2q.
```

This is an upper filter.  Moment division, residual cumulants, the
two-residual discriminant, and zeon-apolar catalecticants use subset
recursions and therefore require a down-set.  Exact scalar graph families at
`q=2` and at every even `q>=4` keep every eligible coefficient fixed while a
missing lower coefficient varies.  This proves that adding all currently
legal principal depths cannot close the gap by postprocessing.  See
`RESIDUAL_DEPTH_OBSERVABILITY_STAIRCASE_AND_ALL_DEPTH_KERNEL_THEOREM.md`.

The positive inverse theorem is permanental tomography.  On a square
residual--port chart, the degree-`k` response is the `k`th permanental
compound of the incidence matrix applied to the `k`-deletion principal
hafnian cofactors.  At identity incidence every even compound is the
identity, so all are simultaneously invertible on one nonempty Zariski-open
set.  The recovered arrays come from one residual graph if and only if all
nested partner-expansion recurrences hold.  Their determinant-cleared forms
are exact polynomial obstructions, with Hadamard stress as the depth-zero
member.  See
`HIGHER_RESIDUAL_PERMANENTAL_TOMOGRAPHY_NESTED_COFACTOR_STRESS_AND_CUMULANT_INTERFACE.md`.

On one four-port window, a fully polarized nonprojective root pair is a
four-channel sensor on the six pair faces.  Its observation matrix satisfies

```text
K(A,B)c=vec(A X(c) B^T),              rank K(A,B)<=4.
```

Thus one sensor has a sharp generic defect two.  Two sensors recover all six
faces exactly when their invisible planes are transverse, and an explicit
integer pair realizes stacked rank six.  This is the exact linear
observation-matroid criterion replacing the earlier unit marked-star
normalization.  Current
GHZ theory does not force two compatible sensors or separate their nuisance
columns.  See
`NONPROJECTIVE_ROOT_PAIR_FAN_SELECTOR_TOMOGRAPHY_THEOREM.md`.

The neighboring literatures clarify the translation without supplying the
missing graph theorem.  Algebraic-matroid identifiability studies which
coordinate observations generically distinguish parameterized models; see
Drton, Hollering, and Wu,
[*Identifiability of Homoscedastic Linear Structural Equation Models using
Algebraic Matroids*](https://arxiv.org/abs/2308.01821).  Cellular sheaves and
their Laplacians organize local data, restriction maps, global sections, and
cohomological inconsistency; see Hansen and Ghrist,
[*Toward a Spectral Theory of Cellular Sheaves*](https://arxiv.org/abs/1808.01513).
Here the exact chart calculation shows why ordinary scalar holonomy is too
weak: one fixed residual edge has all nine coordinate labels on overlapping
torus planes with every transition gain equal to one.  On torus lines the
label is pure gauge, and the complete compatibility equations are the linear
circuits among rank-one evaluation tensors.  See
`CROSS_ROOT_COORDINATE_MONOMIAL_CHART_HOLONOMY_AND_NINE_CHART_NO_GO.md`.

The hafnian/cumulant side remains closest to Gaussian-state combinatorics:
Hamilton et al. connect Gaussian boson sampling probabilities to hafnians
([*Gaussian Boson Sampling*](https://arxiv.org/abs/1612.01199)), while Cardin
and Quesada express photon-number moments through loop hafnians and study
cumulants ([*Photon-number moments and cumulants of Gaussian
states*](https://arxiv.org/abs/2212.06067)).  The repository's
root-budget staircase, nested-cofactor criterion, and transverse-fan theorem
are problem-specific consequences, not claims imported from those papers.

## Residual-depth cumulants, zeon apolarity, and the sharp Gram boundary

The arbitrary-order residual-hafnian two-port decomposition has now been
audited independently.  Its corrected pair family has one common symmetric
middle form `C(A)`, and the residual edge/cofactor compatibility retains the
Hadamard-stress equation

```text
(A Hadamard C(A))1=haf(A)1.
```

There is no rank improvement on the torus-zero branch: for every even
`q>=4`, the complete-support residual matrix with `A_12=-(q-2)` and every
other edge one has `haf(A)=0` but `rank C(A)=q`.  This exact countermodel
closes the tempting route "residual cancellation implies one fewer Gram
channel."  See
`RESIDUAL_HAFNIAN_COMMON_GRAM_AUDIT_AND_TORUS_ZERO_FULL_RANK_SHARPNESS.md`.

The useful translation appears only after retaining compatible residual
deletion depths.  In the commuting square-zero port/residual algebra, divide
every depth by the common port-only moment `M`.  The complete normalized
tower is exactly

```text
Phi=exp(Q_A+Q_R),             log Phi=Q_A+Q_R.
```

Thus singleton residual cumulants are the port-incidence rows, pair
cumulants are scalar residual edges, and all cumulants of residual order at
least three vanish.  Equivalently, every depth is one loop hafnian with
square-zero linear loop weights.  For two residual vertices this gives the
division-free cross-depth discriminant

```text
MZ-Y_0Y_1=hM^2.
```

Every nonzero synchronized port moment recovers `h`; the `B=0` family proves
the all-nonempty-moments-zero escape sharp.  These statements form a
necessary-and-sufficient test for a complete isolated scalar response tower,
but a top `P_7` coefficient does not itself expose the three companion
deletion families.  See
`RESIDUAL_DEPTH_LOOP_HAFNIAN_CUMULANT_AND_TWO_PORT_DISCRIMINANT_THEOREM.md`.

The same response has an apolar refinement in the zeon, or commuting
zero-square, algebra.  For one fixed residual-present response, mark `k`
disjoint port legs and concatenate every compatible remaining port degree.
The resulting catalecticant factors through
the `k`th permanental compound of the common incidence matrix, so

```text
rank Cat_k <= min{binom(q,k),binom(r+k-1,k)},
```

where `r` is the incidence rank.  Its top block is the complement polar
pairing of the `k`th and `(q-k)`th permanental compounds.  Doubled identity
incidence realizes a complement permutation matrix of size `binom(q,k)`, so
the residual-order bound is best possible.  This imports the language of
Feinsilver--McSorley zeon powers and multigraded apolar catalecticants, while
the common nested hafnian tower is problem-specific.  See
`RESIDUAL_ZEON_APOLAR_MULTI_LEG_CATALECTICANT_THEOREM.md`.

The literature interfaces are now precise.  Gaussian boson sampling explains
the hafnian/Wick exponential; loop-hafnian moment and cumulant formulas
motivate the residual logarithm; zeon powers identify permanental compounds;
and apolarity packages the common derivative space as catalecticant minors.
None of those theories supplies the missing legal deletion-depth selector.
The next proof obligation is therefore observability, not another top-only
rank inequality: expose one compatible coefficient of the two-residual
discriminant, the third residual cumulant, or a nontrivial zeon
catalecticant from the same hypothetical witness.

There is also an exact ear-theoretic translation of the first surviving
support layer.  Hetyei's theorem, in the modern form stated by Dalwadi,
Pause, Diwan, and Kothari, extends every conformal cycle of a bipartite
matching-covered graph by single odd ears.  For the `3m+3` support graph this
requires `m+3` ears.  Their endpoint schedule has exactly six uses beyond
the mandatory first use of every vertex, split as three per bipartition
shore.  These replay counts equal `deg(v)-3`, so the abstract ear resource is
identical to excess-cell incidence on the source shore.  On the mode shore
it measures degree surplus instead; the mandatory cover need not be
mode-cubic.  This gives a new constant-width causal target for
conformal/backbone alignment, but no exclusion yet.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_SIX_TOKEN_EAR_THEOREM.md`.

The phase-decorated `B_3` proposal has also been reduced to a precise local
system.  The six physical terms form one projective phase point, and choosing
a different backbone term is the `S_3` chart action
`(R_tau w)_rho=w_(tau rho)/w_tau`; it creates no new equation.  A
same-word incidence-aligned cube face is flat only when its two port
transports commute.  Exact `Q(sqrt(3))` countermodels realize both allowed
nontrivial abelian images, `C_2` and `C_3`, at the abstract chart-local-system
level; they do not construct distinct physical backbones.  Therefore a
useful global holonomy obstruction must first force noncommuting transport or
isolate a mixed coefficient.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_B3_PHASE_HOLONOMY_NOGO.md`.

The missing conformal/backbone incidence has an exact Hall formulation.  A
precoloured conformal matching lies in a selected pure-backbone union exactly
when each colour's fixed partial matching extends in its coordinate support
graph.  Under that additional alignment, an induced conformal cycle carrying
the excess cells collapses to `C_4` or `C_6`; an aligned three-term theta
collapses to the minimal simple theta.  The theta's three matching monomials
have zero toric ideal, and its two completing chords are exactly the channels
that recreate the full `B_3` bypass.  One explicit aligned `C_6` model and
one exact theta-chord matrix show that neither isolated core suffices.

The corresponding multi-core obstruction is now lattice-theoretic.  A
family of aligned binomials `x^lambda_s=-1` is inconsistent over `C*` exactly
when the `lambda_s` have an integer relation whose coefficient sum is odd.
This imports the character-extension viewpoint for algebraic tori while
preserving the permanent signs.  Forcing such an odd relation from physical
incidence remains open.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_CONFORMAL_CORE_ALIGNMENT_BOUNDARY.md`.

The resulting gain system has a sharp biased-graph closure theorem.  The
three transposition exchanges and two oriented three-cycle exchanges on one
anchored port matrix have one primitive integer relation, with odd
coefficient sum.  Thus making all five coefficients isolated negative
binomials is impossible, while every proper subset is torically soluble.
This is the permanent analogue of the theta property in Zaslavsky's biased
graphs.  The six-token schedule does not force that closure: exact structural
countermodels at `m=6` and every `m>=9` retain the ear, Hall, conformal,
local-rank, and pure-backbone data but have no aligned all-excess carrier.
See
`ARBITRARY_PERMANENT_THREE_EXCESS_REPLAY_EXCHANGE_CLOSURE_THEOREM.md`.

The spinor translation exposes a different sharp boundary.  The `3 x 3`
permanent obeys a Plucker-type identity with the characteristic-zero defect
`2 x_13 x_23 x_31 x_32`.  A bare theta kills the defect; its two completing
chords support it.  An exact six-token conformal-`K_3,3` model realizes a
nonzero defect and an exact mixed cancellation over `Q(sqrt(2))`.  Thus
matchgate identities or Kuo condensation apply only after proving a
Pfaffian/planar eligibility structure.  Little's conformal-`K_3,3`
characterization gives the clean conditional theorem, while the fact that
the second secant of the six-terminal pure-spinor variety fills `P^31`
explains why summing two spinorial channels supplies no universal identity.
See
`ARBITRARY_PERMANENT_THREE_EXCESS_BOSONIC_PLUCKER_DEFECT_THEOREM.md`.

The needed cross-coefficient mechanism is a local apolar contraction.  An
alternate colour that sees only one diagonal cell replaces a port row by a
singleton; selected replacements contract the coefficient to a principal
complementary permanent.  The completed `K_3,3` bypass survives radius one
because its three principal `2 x 2` permanents vanish, but any radius-two
contraction is a unique nonzero matching.  This Hamming-face pinch excludes
coefficient-induced diagonal-excess `K_3,3` completions at arbitrary order.
See `ARBITRARY_PERMANENT_THREE_EXCESS_HAMMING_FACE_PINCH_THEOREM.md`.

Keeping the unspecialized port tensor yields a broader invented invariant:
bosonic boundary-entanglement rank, the maximum one-versus-two flattening
rank.  The completed theta has rank at least two for both allowed excess-mode
profiles, `1+1+1` and `2+1+0`; characteristic zero prevents collapse in the
second profile through the same factor `2` as the Plucker defect.  A zero or
rank-one exterior-decoupled `Delta_3` slice is therefore impossible.  Any
remaining completion must export and cancel nonempty boundary sectors.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_BOUNDARY_ENTANGLEMENT_RANK_THEOREM.md`.

An apolar boundary quotient removes the remaining convolution assumption.
Quotienting by outgoing core-mode covectors kills every nonempty boundary
sector termwise.  Exact degree tightness makes the conformal exterior
matching uniquely selectable by a colour word, so the empty sector is
nonzero.  The surviving port tensor has flattening rank at least two, while
the projected `Delta_3` slice has rank at most one.  Hence simultaneous
eligibility of both theta-completing chords is impossible for `m>=4` in the
tight aligned conformal completed-theta setup.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_APOLAR_BOUNDARY_QUOTIENT_THEOREM.md`.

The one-chord diagonal-`1+1+1` profile is now closed as well.  With four
outgoing core cells, a colour-by-colour cut transport law confines every
rank-one quotient chart; the only target-like chart deletes an aligned theta
edge.  With three outgoing cells, all boundary quotients are lines, the port
tensor retains flattening rank two, and the unique exterior surplus mode
still permits a nonzero empty-sector selector.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_ONE_CHORD_CUT_COLOR_EXCLUSION_THEOREM.md`.

The `2+1+0` profile marks a sharp method boundary.  An exact 21-cell model
has one complete zero mixed coefficient, local rank, pure backbones,
matching-coveredness, and conformality, but its apolar survival profile is
`(3,2,0)`: one outgoing boundary span fills the whole port space.  The
ordinary product quotient annihilates the core and the diagonal target
simultaneously.  Its backbone-alignment defect is one, so it does not meet
the global alignment hypothesis.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_ONE_CHORD_APOLAR_SATURATION_BOUNDARY.md`.

## 0. Derived flattenings and boundary-measurement theories

### Koszul and Young flattenings

Ordinary tensor flattening forgets a saturated factor.  Koszul/Young
flattenings replace one contraction by maps involving exterior powers and
then take determinantal rank conditions.  Landsberg and Ottaviani introduced
the vector-bundle/Young-flattening method for equations of secant varieties:

- J. M. Landsberg and Giorgio Ottaviani,
  *Equations for secant varieties via vector bundles*,
  [arXiv:1010.1825](https://arxiv.org/abs/1010.1825).

The method has now been applied recursively to determinant and permanent
tensors themselves:

- Jong In Han, Jeong-Hoon Ju, and Yeongrak Kim,
  *Recursive Koszul flattenings of determinant and permanent tensors*,
  [arXiv:2503.12032](https://arxiv.org/abs/2503.12032).

A still broader recent construction uses Kronecker--Koszul and tangency
flattenings to obtain new determinantal equations for tensor secant
varieties:

- Matej Dolezalek and Mateusz Michalek,
  *Nonlinear methods for tensors: determinantal equations for secant
  varieties beyond cactus*,
  [arXiv:2602.12762](https://arxiv.org/abs/2602.12762).

These papers validate one piece of the proposed derived apolar boundary
signature: exterior-power data can support nontrivial rank tests after a
plain matrix flattening or quotient has lost information.  In the saturated
one-chord model, `B_2=V_2`, so `V_2/B_2=0` while
`Lambda^3(B_2)` is one-dimensional and nonzero.

The transfer stops there.  Published Koszul flattenings act on a fixed tensor
and detect secant/tensor-rank geometry.  The present problem needs an
operator on a matching boundary convolution which simultaneously:

1. kills or grades every nonempty boundary sector;
2. leaves a computable nonzero class of the empty core;
3. commutes with the exact `P_m -> Delta_3` restriction; and
4. gives a rank/direction mismatch on the diagonal target.

No cited construction supplies that matching-compatible differential.  The
graded carrier in the apolar-saturation note is therefore a rigorous vector
space proposal, not an imported theorem or a proved obstruction.

### Grassmannian boundary measurements and dimer boundary states

Postnikov's boundary-measurement map packages weighted directed paths in a
planar network into Grassmannian coordinates and organizes their gauge and
cell structure:

- Alexander Postnikov,
  *Total positivity, Grassmannians, and networks*,
  [arXiv:math/0609764](https://arxiv.org/abs/math/0609764).

Planar dimer theory similarly packages boundary monomer sectors into one
Pfaffian partition function.  A representative exact theorem is:

- Alessandro Giuliani, Ian Jauslin, and Elliott H. Lieb,
  *A Pfaffian formula for monomer-dimer partition functions*,
  [arXiv:1510.05027](https://arxiv.org/abs/1510.05027).

These theories suggest a second construction target: replace the
termwise-killing quotient by a boundary response tensor whose coordinates
are the balanced `A--Q/R--P` matching sectors, and seek relations among its
minors or Pluecker coordinates.  Such an object would retain the saturated
top boundary sector rather than map it to zero.

Again the hypotheses do not transfer automatically.  Postnikov's map is a
planar directed-network/Grassmannian construction.  The boundary-monomer
formula is planar and Pfaffian.  The present support may contain a conformal
`K_3,3`, and the bosonic permanent has the explicit factor-two Pluecker
defect recorded in the bosonic-defect theorem.  Therefore planarity,
Pfaffian eligibility, or a valid Kasteleyn signing must first be proved on
the relevant boundary response graph.  Without that bridge, Grassmannian
or fermionic identities are conditional tools, not equations of the
original permanent tensor.

### Resulting exact research fork

The saturated `2+1+0` branch is now split into two non-equivalent proof
obligations:

```text
alignment route:
    force a colour-labelled theta matching into one selected pure-backbone
    union, strengthening setwise defect delta_H=0 to common-word alignment;

derived-boundary route:
    construct a matching-compatible exterior/Koszul differential or a
    boundary response tensor, then prove a target-rank identity without
    assuming planarity or Pfaffianity.
```

The 21-cell saturation model blocks any proof using only the ungraded apolar
quotient and the structural ledgers.  It does not block either route above.

## 1. Gain graphs and a new multi-backbone gluing diagram

### Existing theory

In a gain graph, oriented edges carry elements of a group, reversal inverts
the gain, and a cycle is balanced when its gain product is the identity.
Zaslavsky's foundational biased-graph theory organizes these balanced cycles
and the associated matroids:

- Thomas Zaslavsky, *Biased graphs. I. Bias, balance, and gains*, JCTB 47
  (1989),
  [doi:10.1016/0095-8956(89)90063-4](https://doi.org/10.1016/0095-8956(89)90063-4).

### Exact translation obtained here

At `3m+2` equality, let `p_1,p_2` be the exceptional sources and define

```text
g_(i,c)=r_(i,p_2)[c]/r_(i,p_1)[c].
```

Every cancellable mixed backbone matching gives an edge between two
mode--colour states and forces `g_u/g_v=-1`.  Thus the cancellation graph is
an all-negative gain graph and must be bipartite.  This is proved in
`ARBITRARY_PERMANENT_EQUALITY_NEGATIVE_GAIN_GRAPH_THEOREM.md`.

### Exact no-go for one backbone

For a fixed triple `H=M_0 union M_1 union M_2`, every incident state `(i,c)`
has a canonical side: the pure edge of `M_c` at mode `i` ends at either
`p_1` or `p_2`.  Every cancellation edge joins the two sides.  Thus the
fixed-backbone gain graph is combinatorially bipartite before the ratio
equations are used.  An exchange complex whose attaching loops are already
walks in that graph adds no new odd-holonomy obstruction.

### New theory to build: the multi-backbone gain diagram

Let the objects be all triples `(M_0,M_1,M_2)` of pure matchings, with an
elementary transition when one matching changes along one alternating cycle.
Attach to each object its fixed-backbone cancellation graph.  Identify a
vertex `(i,c)` across all objects because its physical ratio `g_(i,c)` is
independent of the chosen matching.  The resulting colimit graph is
`Gamma^*` from
`ARBITRARY_PERMANENT_EQUALITY_NEGATIVE_GAIN_GRAPH_THEOREM.md`.

Each fibre is bipartite, but the colimit need not be: a state may lie on the
`p_1` side in one pure matching and the `p_2` side in another.  Every edge in
the colimit still has gain `-1`, so a hypothetical restriction requires the
whole colimit to be bipartite.

The pure-matching cube theorem makes the diagram finite in structure at
every order: every switch is an exceptional-source four-cycle, and at most
two colours can switch.  Thus the object set is a face of `{0,1}^k`, `k<=2`,
with at most four objects.  The two-switch case is confined to co-located
noncoordinate excess cells.  This is a theorem about the choice space, not
permission to enumerate the mixed matchings inside those objects.

The zero-dimensional face is now impossible.  If every colour has a unique
pure matching, full colour eligibility has a unique-matching triangular
form with at most two nonmatching edges.  Rectangle cancellation makes the
sets of colours used by mixed matchings at the two exceptional sources
disjoint.  It also forces each pair of pure colour matchings to form one
Hamilton cycle: every multi-component two-factor produces either a mixed
matching with the same terminal colour or two complementary mixed matchings
whose cross partners create a pure switch.  Bogdanov supplies a mixed
matching, so one exceptional-source colour set is a singleton.  A nonforced
edge of that colour is a chord of the Hamilton cycle formed by the other two
colours; extending the chord to a perfect matching contradicts the singleton
port rule.  Hence every equality survivor has one or two switches.

This packages the remaining equality problem into one exact combinatorial
claim:

```text
Do alternating-cycle transitions among all pure matchings force an odd
cycle after their ratio-state vertices are identified?
```

This is the highest-priority arbitrary-order route.  It uses matching
exchange between backbones; it does not repeat the already exhausted
single-backbone odd-cycle argument.

The backbone-colouring glue theorem gives a complete descent formulation.
Its vertices are connected components of the fixed-backbone graphs; shared
ratio states label overlap edges by the xor of the two canonical side
assignments.  The colimit is bipartite exactly when this `F_2` overlap graph
is balanced.  A one-switch straddling pair gives an immediate unbalanced
two-cycle.

The one-switch cut normal-form theorem first sharpened that target.  The nonzero
pure switch binomial forbids every nonmonochromatic matching in either
selected backbone that uses both switch edges.  After deleting the switch
core, the common residual backbone has a unique perfect matching; its
alternating dependency digraph is therefore acyclic and its biadjacency
support triangular.  In the two-fibre
component-incidence graph, the only nonzero overlap labels are the two
switch states.  Equality holds at the gluing level exactly when those two
marked edges belong to the cut space: both are bridges, or they are a
two-edge series cut.  A straddling pair is only the smallest violating cycle.
Abstract bridge and series-pair models survive this cut-space test.

The full permanent backbone now excludes them by a different transfer.  In
the one-switch branch, component selection forces every pair of selected
pure matchings to be one alternating Hamilton cycle.  The exceptional edges
of a nonswitch colour are therefore two chords of the Hamilton cycle formed
by the other colours.  Extending each chord to a mixed perfect matching and
applying two-source localization forces both cross cells, producing a second
pure matching of the nonswitch colour.  Hence the one-switch branch is empty
at every order.  This is a perfect-one-factorization obstruction rather than
a gain-holonomy obstruction.

This is a direct transfer from unique-perfect-matching theory and the
Dulmage--Mendelsohn viewpoint, but the marked cut condition is specific to
the permanent cancellation local system.  See Kotzig's 1959
[unique-matching record](https://eudml.org/doc/29879) and Dulmage--Mendelsohn,
[*Coverings of Bipartite Graphs*](https://doi.org/10.4153/CJM-1958-052-0).

The two-switch branch has a complementary local invariant.  Its two
noncoordinate excess rows are co-located at one mode and the equality ledger
leaves exactly one coordinate row there.  Localization forces that row to
have the third colour, so local concision makes the switch-colour `2 x 2`
minor nonzero.  In gain coordinates, `g_(a,c)!=g_(a,d)`.  Path parity then
separates the two same-mode switch states whenever they have the same source
side, and also separates each switch state from its mandatory partner in
every fibre.  Therefore the most local candidate pair cannot straddle; a
ratio state away from the common excess mode is essential.  Cross-colour
pairs at `b_c,b_d` remain open.

This also marks the exact limit of two nearby imported theories.  The excess
plane lies in `Gr(2,3)`, which has no quadratic Pluecker equation.  The two
known switch rectangles admit one coherent edge signing, so there is no
two-rectangle Pfaffian obstruction.  Adding the third row pair would obstruct
one common determinant signing, but that orientation failure is not a
contradiction in the bosonic permanent system.  Matchgate identities would
additionally require a full deletion-closed boundary signature.
Cai--Gorenstein and Bravyi explain that signature-level hypothesis; the
present alternate backbones do not satisfy it automatically.

The direct mixed-backbone route to the third switch-mode rectangle is now
reduced exactly to Hall completion.  Delete the common excess mode, both
degree-four switch modes, and the three sources they occupy.  The remaining
graph is switch-independent.  A perfect matching completes the desired mixed
word and forces its rectangle equation.  If no matching exists, a minimal
deficient set has deficit one; its two
switch-colour matchings form one alternating path plus cycles, and its shore
has cut signature `(1,1,1)` or `(1,1,3)`.  An explicit six-mode support with
the five-edge signature satisfies the complete degree ledger, local ranks,
pure-switch classification, and every source-subset Hall quota.  It is not a
mixed-coefficient solution, but proves that these structural conditions do
not force completion.  It does not rule out deriving the same rectangle
indirectly from other mixed equations.

This is the appropriate tight-cut translation: contract a connected shore
while retaining its three or five boundary port values, and seek a boundary
coefficient identity incompatible with the diagonal target.  The three-edge
signature is now excluded exactly.  Its two switch-colour ports occupy the
same outside source, so full-support Laplace expansion has only two distinct
complement minors and flattening rank at most two.  The corresponding
nontrivial flattening of `Delta_3` has rank three.  The five-edge signature
is now excluded by a separate boundary-state argument.  Defect-one balance
forces an internal Kempe pairing bit; a pure switch toggles the exterior bit
while preserving the interior.  Choosing the aligned backbone gives a
one-cycle flip whose mixed monomial lacks its localized two-source cross
partner.  Thus no no-completion shore survives, and the residual perfect
matching and cross-colour port rectangle are forced at every order.  The
shore interior remains symbolic throughout; no census of supports is used.

The remaining two-switch branch is now excluded without further scalar gain
algebra.  Select the two switch matchings so that their common excess mode
`a` goes to opposite exceptional sources.  Their two-factor contains the
path `p_1--a--p_2`.  Any other component would allow a mixed component
selection using both selected switch edges, so switch-core rigidity makes
the factor Hamilton.  The two exceptional edges of the nonswitch colour are
then Hamilton chords.  Their two mixed extensions force both cross cells and
create a forbidden pure switch in that colour.  This closes all equality
strata and sharpens the support bound from `3m+2` to `3m+3`.

## 2. Toric ideals and matching-exchange binomials

### Existing theory

Perfect matchings become monomials, and their symmetric differences decompose
into even cycles.  Toric ideals record when two products of matching monomials
have the same incidence vector.  Recent work relates generator degrees for
matching-polytope toric ideals to edge colourings of bipartite multigraphs:

- Mori, Motomura, Ohsugi, and Tsuchiya, *Toric ideal of matching polytopes and
  edge colorings*, [arXiv:2501.19209](https://arxiv.org/abs/2501.19209).

The nearby matroid version asks whether toric relations are generated by
quadratic symmetric exchanges; see Lasoń,
[*On the toric ideals of matroids of a fixed rank*](https://arxiv.org/abs/1601.08199).

### Safe transfer

The equality equation `AD+BC=0` is a signed exchange binomial.  After choosing
one sign gauge, its exponent difference is exactly the four-cycle lattice
move `AD-BC`.  Thus the **exponents** live in a matching toric ideal while the
**coefficient signs** live in the gain local system of Section 1.

Neither structure alone is enough:

- the toric ideal forgets the required plus sign;
- the gain graph forgets which exchange cycles are generated by actual
  perfect matchings.

Together they suggest a rigorous target: compute a symbolic presentation of
the exchange lattice of the three chosen pure matchings, then prove that the
`-1` character on its rectangle generators is not trivial on the relation
lattice.  One odd relation in that lattice is exactly the desired
contradiction.  This is a lattice-rank/Smith-normal-form theorem in symbols,
not a census of matchings.

### Exact three-excess port reduction

The strict support theorem makes `3m+3` the first remaining layer.  Choose
the mandatory `3m`-cell coordinate cover.  The three excess cells have two
or three exceptional source endpoints: one endpoint is impossible because
Bogdanov supplies a mixed backbone matching and an alternating cancellation
cycle needs two new source endpoints.

Exceptional-source localization then collapses every coefficient of a word
induced by the selected backbone exactly.  Relative to its backbone matching
`F`, every other term for the same word agrees outside the exceptional
sources and permutes their `F`-preimage modes.  There can be only one exchange
cycle, so the change is a transposition or a three-cycle.  After the common
arbitrary-order interior monomial is factored, the full coefficient is

```text
W_F per(X),          X of size 2 x 2 or 3 x 3.
```

Thus the matching-toric boundary of a mixed backbone word has at most the six
elements of `S_3`.  Pure words are sharper.  A colour-eligibility graph has
only three cells beyond its chosen matching.  After contraction these are at
most three loopless dependency arcs, which contain at most one directed
cycle.  Hence every colour has at most two pure matchings, related by one
alternating four- or six-cycle, and the pure backbones form a Boolean cube of
dimension at most three and size at most eight.  This is stronger than a
bounded search claim: it is an exact quotient of every backbone-induced
coefficient by its common interior plus a dependency-digraph classification
of all pure choices.

The new obstruction is also sharp.  A `3 x 3` permanent may vanish while a
distinguished row has no cross entry, because the complementary two ports
transpose and cancel with that row fixed.  For a chord row `s`, the fixed-row
channel is

```text
X_(s,s) per(X_(hat s,hat s)).
```

Nonvanishing of that complementary `2 x 2` permanent forces a cross arc out
of `s`.  If this holds for all three chord rows, a directed two- or
three-cycle of forced arcs gives a second pure matching.  The precise next
problem is therefore to exclude the fixed-port bypass rectangles, not to
enumerate the six permutations.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_PORT_PERMUTATION_THEOREM.md`.

### Matching-covered and `B_3` phase translations

At exact support `3m+3`, the physical support graph is matching-covered.  An
edge in no perfect matching could be deleted without changing the
polynomial, contradicting the strict support theorem.  A disconnected
support would factor across components and have flattening rank one, whereas
the corresponding nontrivial flattening of `Delta_3` has rank three.

De Carvalho and Little's quoted general theorem implies that any three
prescribed edges of a matching-covered graph lie in a conformal subgraph
formed from at most two alternating circuits.  Their sharper three-edge
corollary says the carrier is an induced circuit, an even subdivision of
`Theta`, or an even subdivision of one of nine `K_4`-generated graphs.
Bipartiteness excludes the last family because every member retains an odd
circuit.
Hence the excess cells lie in a conformal even circuit or theta subdivision,
with exactly two or three internal perfect matchings; see [*Matching Covered
Graphs with Three Removable
Classes*](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v21i2p13).
This is the correct even bipartite analogue of the tempting factor-critical
ear translation.

For a three-source backbone word, normalize the three transposition
monomials to `a,b,c` and the oriented three-cycle monomials to `u,v`.  The
complete coefficient and its toric circuit are

```text
1+a+b+c+u+v=0,       uv=abc.
```

The multiplicative equation is exactly the unique cubic circuit of the
`3 x 3` Birkhoff polytope described by Haase and Paffenholz in
[*Groebner Bases for Transportation
Polytopes*](https://arxiv.org/abs/math/0607194).  The three complementary
fixed-row channels are `1+c,1+b,1+a`.  Setting `a=b=c=-1` leaves the
consistent equations `u+v=2`, `uv=-1`, realized over `C` by a full-support
port matrix with `u,v=1+sqrt(2),1-sqrt(2)`.  Hence even simultaneous
vanishing of all three channels cannot be excluded inside one port
coefficient.

The invented next object is a proposed phase-decorated `B_3` exchange
complex: glue one additive/toric phase variety for every backbone-induced
mixed word and identify shared physical row-cell factors across the Boolean
pure-backbone cube.  To incorporate the conformal cycle/theta theorem, its
definition still needs carrier-selection data recording how that theorem's
matching meets each pure backbone.  The intended object retains both complex
phases and global matching reuse; either ingredient alone is insufficient.

## 3. Determinantal ideals, Grassmannians, and a cofactor quiver

### Existing theory

The visible condition that two quotient cofactors are proportional is the
rank-one determinantal variety, cut out by `2 x 2` minors.  Across many linked
linear maps, quiver semi-invariants provide systematic determinantal
equations.  Schofield and Van den Bergh prove that, in characteristic zero,
determinantal semi-invariants span the semi-invariant functions for acyclic
quivers:

- Schofield and Van den Bergh, *Semi-invariants of quivers for arbitrary
  dimension vectors*, [arXiv:math/9907174](https://arxiv.org/abs/math/9907174).

Symmetric quivers add Pfaffian semi-invariants on skew-symmetric arrows; see
Aragona, [*Semi-invariants of Symmetric Quivers*](https://arxiv.org/abs/1006.4378).

### Exact translation obtained here

For every active root deletion `k`, the pair

```text
(bar C_k,bar E_k)
```

is a two-row matrix of rank at most one.  Its minors are the quotient-wedge
invariants.  At least two sectors are active, yielding five degree-eight
products without naming them.

### Proposed theory: a bound deletion-depth cofactor quiver

Make one vertex for each quotient cofactor space at each deletion depth.
Edge-contraction maps and root/end-point expansions become arrows; the
five hidden-pair equations become rank constraints on five two-arrow
Kronecker fragments.  Common root-edge parameters impose relations between
arrows, so this is a **bound/constrained** representation variety, not
automatically the ordinary acyclic quiver space covered by the cited
semi-invariant theorem.

The proof program must first define the group action and relations and check
whether the resulting quiver is acyclic, or instead work with the more
general map-of-projectives formulation.  Only then is it legitimate to seek
a determinantal semi-invariant that vanishes on the legal shared-edge image
and is nonzero on the prescribed lower-jet frame.  Schofield theory suggests
candidate forms; it does not guarantee such a separator here.

This remains preferable to eliminating all edge weights if a separator can
be found.  One semi-invariant could certify incompatibility uniformly over an
entire component, as the repository's row-module certificates already do in
lower-order cells.

The tangent counterfamily sharply specifies the missing data: a determinant
built only from `h_k,q_k,g_t` cannot work.  At least one actual complementary
blocker cofactor value must enter.

## 4. Matchgates, spinors, and delta-matroids: a conditional local tool

### Existing theory

Cai and Gorenstein prove that the matchgate identities are necessary and
sufficient for planar matchgate signatures:

- Cai and Gorenstein, *Matchgates Revisited*,
  [arXiv:1303.6729](https://arxiv.org/abs/1303.6729).

Tropical Wick relations and even delta-matroids describe the support-side
spinor analogue; see Rincón,
[*Isotropical Linear Spaces and Valuated Delta-Matroids*](https://arxiv.org/abs/1004.4950).

### Proven non-transfer and remaining use

Generic bosonic principal hafnians cannot be changed into principal
Pfaffians by a fixed edge signing from six vertices onward, and complex
cancellation can destroy delta-matroid support.  Those exclusions are proved
in `BOSONIC_HAFNIAN_SPINOR_NO_TRANSFER.md`.

Therefore no global Grassmann--Plücker identity may be imported.  A narrower
conditional route remains legitimate: if the equality/gain analysis forces a
coherent sub-Pfaffian representation across the entire relevant
boundary-deletion family, with compatible signs, then matchgate identities
apply on that chart.  A Pfaffian orientation computing one full matching sum
is not enough.  The proof obligation is to derive the coherent family from
the permanent hypotheses; planarity is one sufficient route, but cannot be
assumed.

Priority: medium.  It may close a rigid equality subcase, but it is not a
universal bosonic theory.

## 5. Tensor subrank, invariant theory, and orbit closure

### Existing theory

Ordinary tensor subrank is exactly the largest diagonal tensor obtainable by
independent local linear maps.  Christandl, Fawzi, Ta, and Zuiddam study the
distinct symmetric version, where the same map is used on every leg, and its
relation to ordinary/asymptotic subrank:

- *Symmetric Subrank of Tensors and Applications*,
  [arXiv:2104.01130](https://arxiv.org/abs/2104.01130).

Entanglement polytopes turn covariants into local spectral witnesses for
orbit closures:

- Walter, Doran, Gross, and Christandl, *Entanglement Polytopes*,
  [arXiv:1208.0365](https://arxiv.org/abs/1208.0365).

Tensor-network state spaces can be nonclosed, so exact image membership and
border membership must be separated:

- Landsberg, Qi, and Ye, *On the geometry of tensor network states*,
  [arXiv:1105.4449](https://arxiv.org/abs/1105.4449).

Geometric-complexity work also warns that coarse moment-polytope or
`SL`-representation data can be too weak for orbit-closure lower bounds:

- Bürgisser and Ikenmeyer, *Geometric Complexity Theory and Tensor Rank*,
  [arXiv:1011.1350](https://arxiv.org/abs/1011.1350).

### Safe transfer

`P_m -> Delta_3` is an exact ordinary-subrank restriction, not a symmetric,
border, or asymptotic statement.  Local concision and Hall
quotas resemble moment-polytope inequalities, but the sharp `3m+2` survivor
shows that such inequalities are not enough.  The useful next objects are
explicit covariants or nonlinear flattenings that:

```text
vanish on every legal hafnian/permanent restriction image,
but do not vanish on Delta_3.
```

The coloured quotient minors are not yet such covariants or separators.
They are coordinate-dependent determinantal equations on one uniform-axis
lower-jet chart, derived using the `Delta_3` target; no `GL`-equivariance or
nonvanishing target evaluation has been proved.  The bound-cofactor-quiver
program asks whether they can be combined into a genuine separator without
passing to border or asymptotic rank.  Symmetric/asymptotic subrank
functionals remain orientation, not proof certificates for this exact
finite problem.

## 6. Bosonic Gaussian moments, apolarity, and cumulant sheaves

### Existing theory

Hafnians are transversal moments of a formal centered Gaussian family, and
Gaussian moment parametrizations form algebraic moment varieties.  Useful
entry points are:

- Hamilton et al., *Gaussian Boson Sampling*,
  [arXiv:1612.01199](https://arxiv.org/abs/1612.01199);
- Améndola, Faugère, and Sturmfels, *Moment Varieties of Gaussian Mixtures*,
  [arXiv:1510.04654](https://arxiv.org/abs/1510.04654).

### Exact repository transfer

In the vertex-exclusive square-zero algebra, the full family of partial
matching tensors is

```text
M=exp(Q),                 log M=Q.
```

Thus all connected cumulants above degree two vanish **for the full
partition-closed partial-moment family in which proper blocker subsets are
retained and core vertices may split or delete**.  A shell of complementary
cofactors retaining one common blocker core need not be log-quadratic after
coefficient extraction.  The current lower-frame theorem does not force the
required family, and the scalar hidden overlay is surjective.  This is proved in
`BLOCK_SQUARE_ZERO_WICK_COMPLETION_THEOREM.md` and
`ROOT_M7_HIROTA_HIDDEN_OVERLAY_SURJECTIVITY_NOGO.md`.

### Proposed analogy: a deletion-cumulant gluing obstruction

Regard known cofactor values on the subset lattice as prospective local
sections.  A legal graph should give compatible log-quadratic completions on
partition-closed windows.  This resembles a Čech obstruction, but is not yet
a sheaf or a defined cohomology class: restriction maps, the gauge/torsor
structure on nonunique completions, and gauge-independent overlap differences
must all be constructed.

A rigorous program is:

1. choose partition-closed windows that allow proper core subsets;
2. define their completion spaces and restriction maps;
3. quotient the nonuniqueness by an explicit gauge action;
4. only then define and test an overlap obstruction against the `Delta_3`
   frame.

The scalar-surjectivity theorem says one window has zero obstruction.  The
first possible class must be coloured and use at least two overlapping root
deletions, matching the quotient-wedge result.

Priority: high after the cofactor quiver is written, because the quiver
arrows provide the overlap maps this sheaf needs.

## 7. Tropical, stable, and Lorentzian methods: degeneration only

### Existing theory

Lorentzian polynomials have M-convex support and strong Hodge-type
inequalities; see Brändén and Huh,
[*Lorentzian polynomials*](https://arxiv.org/abs/1902.03719).  Valuated
delta-matroids give the tropical spinor-side exchange theory in Rincón's
paper cited above.

### Boundary

The Krenn--Gu weights are arbitrary complex numbers.  Positivity,
real-stability, negative dependence, and Lorentzian inequalities do not
survive arbitrary destructive interference.  The support of nonzero complex
principal hafnians is not even always a delta-matroid.

These tools become legitimate only after a proved one-parameter degeneration
in which a unique leading term is selected and the `Delta_3` restriction is
preserved after compensating local scalings.  This suggests combining
Hilbert--Mumford one-parameter subgroups with matching valuations.  The hard
lemma is existence of a useful nontrivial degeneration of an arbitrary exact
hypothetical solution.  Without that lemma, tropical or Lorentzian output is
not evidence about the original complex cancellation problem.

Priority: exploratory, but fully symbolic.

## 8. Matching delta-matroids: support compression, not amplitudes

### Existing theory

Bouchet's matching delta-matroid records the vertex sets saturated by
matchings; its symmetric exchange law is generated by alternating paths:
[*Matchings and delta-matroids*](https://doi.org/10.1016/0166-218X(92)90272-C).
On the spinor side, Rincón relates even/valuated delta-matroids to tropical
Wick vectors and principal Pfaffians:
[*Isotropical Linear Spaces and Valuated Delta-Matroids*](https://arxiv.org/abs/1004.4950).

### Exact repository transfer

The realizable terminal sectors of the conformal exterior form an even
matching delta-matroid.  Bipartite balance and exchange against the empty
sector prove that every nonempty sector contains a feasible elementary
mode-source pair.  Hence absence of *all* boundary sectors reduces exactly to
emptiness of a pairwise link graph.  After contracting one conformal exterior
matching, that link graph is the Boolean reachability relation
`L=B D^* C`; a directed cut is therefore a complete support certificate.
The weighted response of pair `(a_i,p_j)` is

```text
E_ij=sum_(q,r) Y_iq Z_rj per(W_(delete r,delete q))
    =(Y C_per(W) Z)_ij.
```

This is proved in
`ARBITRARY_PERMANENT_THREE_EXCESS_BOUNDARY_DELTA_MATROID_THEOREM.md`.

### Boundary

The support delta-matroid can have auxiliary generic skew/Pfaffian
coordinates, but their Wick identities do not become identities of the
physical unsigned permanent weights.  Even when a pair is linkable, its
aggregate `E_ij` can vanish by complex cancellation.  Conversely,
elementary responses do not determine higher sector amplitudes.  Thus the
theorem compresses the support problem exactly but leaves separate bosonic
cofactor problems at the elementary and higher amplitude layers.

Priority: immediate for every remaining boundary branch.

## 9. Zeon algebras and a new all-sector boundary jet

### Existing theory

Zeons are commuting square-zero generators.  Feinsilver and McSorley develop
their connection with permanents and permanent trace formulas:
[*Zeons, Permanents, the Johnson Scheme, and Generalized Derangements*](https://arxiv.org/abs/1710.00788).
This is also the algebraic language used by the repository's block selector
and full partial-matching Wick completion.

### Exact repository transfer

For exterior block `W` and crossing blocks `Y,Z`, introduce terminal zeons
`u_i,v_j` and the rank-one perturbation

```text
J_W(u,v)=per(W+(Zv)(u^T Y)).
```

If `R_(I,J)` is the complete boundary response covering core mode set `I`
and core source set `J`, with common size `k`, then

```text
[u_I v_J]J_W = k! R_(I,J).
```

Contracting these coefficients with complementary permanents of the core
matrix reconstructs the full block permanent exactly.  For the three-port
problem the degrees `0,1,2,3` simultaneously retain the empty, elementary,
second, and saturated top boundary layers.  Each layer also factors as a
permanental compound product

```text
R^(k)=P_k(Y) D_k(W) P_k(Z),
```

providing determinantal flattenings at every degree.  This is proved in
`ARBITRARY_PERMANENT_THREE_EXCESS_ZEON_BOUNDARY_JET_THEOREM.md`.

### Boundary

The jet is an all-sector carrier, not yet an obstruction.  Its generic
squarefree support is the matching delta-matroid, but physical complex
weights can cancel within any coefficient.  No cross-degree ideal,
differential, or target-rank mismatch has yet been proved.

Priority: highest for the saturated `2+1+0` and bare-core branches.

## 10. Algebraic geometry of the boundary-signature map

### Exact repository theorem

For a three-port core and `3 x 3` exterior, the balanced zeon jet has 20
coordinates.  The response morphism from the 27 entries of `Y,Z,W` has an
exact rank-20 Jacobian certificate at a small integer point.  Hence its image
is Zariski dense in the entire balanced signature space, and the 20 response
coordinates are algebraically independent.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_BOUNDARY_JET_DOMINANCE_NOGO.md`.

### Consequence

There is no ambient cross-degree polynomial identity to discover.  The
unconstrained ideal of the boundary-jet image is zero.  Any useful equation
must instead come from the image of the smaller locus cut out by colour
incidence, local rank, pure-backbone extension, or coefficient alignment.

In Holant terminology this is dominance of the charge-balanced six-terminal
signature map.  It rules out ambient matchgate-style equations for arbitrary
permanent gadgets, while leaving the planar/Pfaffian matchgate locus and
holographic basis orbits untouched; compare Cai and Gorenstein,
[*Matchgates Revisited*](https://arxiv.org/abs/1303.6729).

This changes the algebraic target from

```text
find equations of all boundary jets
```

to

```text
define the coloured/aligned incidence variety;
eliminate Y,Z,W only after imposing its equations.
```

Priority: this constrained image, not the ambient jet space, is now the
highest-priority invented object.

## 11. First equation of the aligned response locus

The coloured-extension incidence now yields a genuine constrained theorem
in the physical eight-cell one-chord `2+1+0` subbranch.  Alignment reserves
the zero-excess port's word colour for a core theta edge.  Mandatory outgoing
cells at nonexceptional exterior sources are forced into their colour
backbones, so the port has exactly the other two outgoing colours:

```text
s_2=2,              B_2=span(e_c:c!=alpha_2),
q_2=1.
```

This excludes the saturation mechanism of the 21-cell method countermodel.
The degree ledger leaves three surplus placements; an exact apolar
rank-two/rank-one mismatch excludes the exterior-surplus placement.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_ONE_CHORD_210_ALIGNMENT_DESATURATION_THEOREM.md`.

The intermediate aligned image has only two concentrated charts:

```text
(s_0,s_1,s_2;tau)=(1,1,2;0) or (0,2,2;0).
```

Their projected cores are always nonzero.  Hence any survivor has an
`alpha_2`-monochromatic exterior complement and must retain `e_(alpha_2)` at
the other two ports.  In the `a_1`-concentrated chart this forces
`alpha_1=alpha_2`; for a mixed aligned word, `alpha_0` is then different.
Perfectness further forces the aligned `a_0` edge to coincide physically
with the `alpha_2` pure-backbone edge.  It must be a bichromatic excess cell,
so the diagonal theta matching through mandatory `z_0` is excluded there.

Both charts are in fact excluded by the mandatory cover and cut transport.
At source `p_2`, its two nonexcess core cells force
`alpha_1!=alpha_2`, immediately killing the `a_1`-concentrated chart.  In the
`a_0`-concentrated chart, cubic exterior transport reduces after cancellation
to `C\{alpha_2}=C\{alpha_1}`, the opposite equality.  Thus the complete
aligned physical eight-cell one-chord `2+1+0` subbranch is excluded.

The separate physical-nine-cell branch also closes symbolically.  If the
second chord has colour `gamma!=alpha_2`, source-cover uniqueness forces
`{alpha_1,alpha_2,gamma}=C`.  It must be retained in the full port tensor,
but an `alpha_2` coordinate slice kills exactly its `gamma` terms.  The
physical degree ledger has only four placements.  Two retain the nonzero
Segre minor `a d^2`; in the other two, cut-colour transport forces the
`alpha_2` target factor into a boundary span while the port slice stays
nonzero.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_INELIGIBLE_NINTH_CELL_EXCLUSION_THEOREM.md`.

This realizes the coloured/aligned response-image idea in its smallest
useful form: incidence and cut transport are imposed before a coordinate
slice is tested against the rank-one Segre ideal.  The tool is an ordinary
flattening minor, not a Pfaffian identity; compare Landsberg--Manivel,
[*On the ideals of secant varieties of Segre varieties*](https://arxiv.org/abs/math/0311388),
and the boundary-tensor viewpoint in Landsberg--Qi--Ye,
[*On the geometry of tensor network states*](https://arxiv.org/abs/1105.4449).

Priority: classify and attack the bare aligned theta, which is now the
remaining aligned `2+1+0`-adjacent physical port rather than a one-chord
case.

## 12. Bare-theta absorption and marked pair-deletion response

The bare theta exposes the limit of the colour-sliced Segre method.  Exact
`1+1+1` and `2+1+0` charts satisfy the local physical surplus ledger, local rank,
cut-colour transport, and the aligned `1+1-2=0` theta equation, yet their
strongest legal quotient is a nonzero monochromatic `Delta_3` slice.  Two
quotient ports share the target colour; the open port absorbs the theta
relation and returns its transverse target direction.  This one-open-port
absorption persists at the local port/cut-ledger level if differently
coloured chord directions are added to the killed span and a corresponding
colour-preserving exterior reroute is available.  No such exterior graph is
constructed.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_BARE_THETA_ABSORPTION_AND_COFACTOR_RESPONSE_BOUNDARY.md`.

The separate `3+0+0` excess-mode profile has only two physical seven-cell
placements.  Its maximal-exterior-surplus chart is excluded by a nonzero
row-zero response against two distinct target lines.  Its cubic-exterior
chart has an exact zero-absorption divisor: the three independent excess
forms combine into the one outgoing boundary colour and vanish in the
quotient, while the target also vanishes.  Thus all three mode profiles meet
a sharp ordinary-quotient boundary.

The useful new object is instead the marked pair-deletion response matrix

```text
R_ij=Omega_ij Q_ij,
```

where `Q_ij` is a bare-theta permanental cofactor and `Omega_ij` is its
exterior completion response.  On a cofacial theta block, Kuo's signless
condensation gives a symmetric compound equation.  A rank-one target gives
the same minor with the alternating sign.  If the exterior responses obey
one toric cross-ratio, the two equations force `2R_11R_22=0`, contradicting
nonvanishing in characteristic zero.  Kuo's planar identity is local and
valid here; what remains unknown is the nonplanar exterior holonomy needed
to transport it.  The current product quotient cannot help because it kills
the marked pair-deletion sectors themselves.

This translation separates the literature correctly: Kuo condensation is
safe on the two local theta faces; matchgate, Postnikov, and electrical-grove
response identities remain conditional on outer-face/disk terminalization.
The invented target is a marked response functor retaining bidegree
`(1,1)`, not another universal identity on the ambient response jet.

The first audit of that target gives a sharp no-go and a small-order
exception.  The marked exterior matrix is exactly the degree-one zeon
response

```text
Omega=Y C_per(W) Z.
```

With two exterior channels, `W=Y=I_2` and
`Z=[[1,s],[t,1]]` give `det(Omega)=1-st`, while every elementary response
and the degree-two response `1+st` are nonzero.  The feasible sectors still
form the complete balanced even delta-matroid.  Hence matching exchange and
the compound tower do not force the desired toric holonomy.

This no-go persists under the full support-side package.  An exact `m=5`,
18-cell graph has a mandatory tricolour cover, local rank three, three pure
backbones, a conformal bare theta, matching-covered support, generalized cut
transport, and an aligned `1+1-2=0` coefficient, but its relevant transverse
marked block is `[[1,2],[1,3]]`.  Its determinant is one.  The graph is not
a restriction: the `(0,2,2;1)` quotient leaves the exact residue
`3e_0+4e_1` against a zero target.

Relative to the unique empty exterior matching, the marked response is a
weighted alternating-path matrix.  Lindstrom--Gessel--Viennot identifies
its `2 x 2` minors with signed sums of vertex-disjoint alternating-path
pairs.  A common alternating separator therefore forces the needed rank-one
transmission.  With one exterior channel, `Omega=YZ` is already an outer
product, so the cross-ratio is automatic at `m=4`.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_MARKED_RESPONSE_TORIC_HOLONOMY_BOUNDARY.md`.

Priority: force alternating vertex-connectivity at most one from the **full
restriction equations**, prove cancellation of the two-channel Cauchy--Binet
sum, or construct the still-missing legal target marking.  Planarity alone
is not the right condition: planar boundary measurements naturally have
higher-rank Grassmannian minors.

The general residual-hafnian Gram route has a parallel sharp boundary.  For
every even residual order `q>=4`, the matrix with all edge weights one except
`A_01=-(q-2)` obeys

```text
haf(A)=0,
det C(A)=2^(q-2)(q-1)(q-3)^3((q-5)!!)^q !=0.
```

Thus the torus-zero choice does not lower the common cofactor rank.  Over
`C`, a rank-`rho` symmetric middle form is a sum of exactly
`ceiling(rho/2)` symmetrized rank-one channel pairs, so the example's
canonical middle form needs `q/2` synchronized permanent channels.  This is
not an observable lower bound: at `q=4` its physical off-diagonal data have
a one-channel completion.  Only `q=2` guarantees the single two-row
permanent before incidence or completion collapse.  A real graph separator
can do better on cross-localized data: a residual separator of size `s`
factors the cofactor cross-block through at most `2^(s-1)` parity subsets.
It affects the `P_7` aggregate only if all relevant port pairs cross.  See
`RESIDUAL_HAFNIAN_TORUS_ZERO_FULL_RANK_COFACTOR_BOUNDARY.md`.

This introduces the exact physical invariant
`chi_off(M)=min_d ceiling(rank(M+diag(d))/2)`, a complex symmetric
minimum-rank completion problem.  At `q=4`, `chi_off=1` although the
canonical channel number is two.  The appropriate neighboring literature is
therefore symmetric matrix completion, not just hafnian rank: Bernstein,
Blekherman, and Lee's
[*Typical ranks in symmetric matrix completion*](https://arxiv.org/abs/1909.06593)
supplies the generic-completion viewpoint, while this conjecture requires
exact nongeneric cofactor strata and then a further quotient by the Laplace
map.

The full response tower admits a sharper translation.  In the
vertex-exclusive Wick algebra,

```text
Z_Q=M_B Phi_(A,R),
[x_S]Phi=sum_(T subset Q, |T|=|S|)
  haf(A[Q minus T]) per(R_(T,S)),
degree Phi<=|Q|.
```

Thus all even degrees form a simultaneous permanental-compound lift through
one common residual incidence matrix.  On disjoint port charts their
one-leg flattenings obey `rank[F_2|F_4|F_6|...]<=|Q|`; if `F_2` has full
residual rank, every higher column must lie in its column space.  This is a
cross-deletion-depth invariant, not a Pluecker relation.  At two residuals it
reduces to the already implicit dual-Wick tangent recursion; at four
residuals the synchronized `F_4` layer is genuinely new data beyond the Gram
response.  The missing `P_7` step is now precise: expose one actual
partition-closed lower-jet window before applying these equations.  See
`RESIDUAL_RELATIVE_RESPONSE_POLYNOMIAL_DUAL_WICK_THEOREM.md`.

Priority on the residual route: force a small separator from blocker
incidence, expose an invertible anchor for the exact Schur defect, or impose
the first lower mixed-Hessian/four-point cumulant.  Do not infer a rank drop
from `haf(A)=0`.

## 14. Deletion-cube observability: a new exact translation

The residual route now has a more precise intermediate object.  Write a legal
mixed root jet as

```text
T=sum_a g_a tensor C_a.
```

The companion forms `g_a` are columns of an observation map and the
complementary hafnian cofactors `C_a` are hidden state.  A cofactor combination
is recoverable exactly when its coefficient row lies in the observation
rowspace; a kernel vector gives an invisible cofactor deformation.  This is a
static algebraic theorem, not merely an analogy with sensing.  The P7 note
proves it and then shows that every canonical pure `P_5` chart forces a clean
four-port graph window, while an exact response fibre proves that its top face
does not determine its proper subset faces.  See
`P7_DELETION_CUBE_OBSERVABILITY_AND_CLEAN_WINDOW_BOUNDARY.md`.

Four neighboring literatures now suggest genuinely different next moves.

1. **Structural observability.**  Lin's structural-control viewpoint asks when
   a sparsity pattern generically permits full-state recovery.  The direct
   transfer here is smaller and exact: build the combined legal-jet
   observation matrix, then seek a matching/matroid certificate for full
   column rank on the deletion classes.  Dynamics and genericity are not
   imported; the graph problem needs exact weighted rank on the GHZ locus.
   [Lin, *Structural Controllability*](https://doi.org/10.1109/TAC.1974.1100557).

2. **Algebraic matroids and local completion.**  Kiraly--Theran--Tomioka study
   whether particular hidden matrix entries are algebraically determined by a
   visible coordinate set, using circuits and local completion rather than
   reconstructing the whole matrix.  The corresponding object here is the
   algebraic matroid of the map from legal edge/cofactor parameters to visible
   jet coefficients.  A circuit polynomial containing one missing pair face
   would give the desired projected identity; dominance of that projection
   would prove that no such identity exists at the chosen data level.
   [Király--Theran--Tomioka, *The Algebraic Combinatorial Approach for
   Low-Rank Matrix Completion*](https://arxiv.org/abs/1211.4116) and
   [Király--Rosen--Theran, *Algebraic matroids with graph
   symmetry*](https://arxiv.org/abs/1312.3777).

3. **Incidence algebras and Mobius inversion.**  `Z=M Phi` is convolution on
   the Boolean lattice of port subsets, and the recursive recovery of `Phi`
   is precisely incidence-algebra inversion.  This explains rigorously why a
   top face without its interval of proper faces is insufficient.  The new
   possibility is to eliminate the hidden interval variables from several
   overlapping copies of the convolution ideal, rather than trying to invent
   an illegal vacuum evaluation.  [Rota, *On the Foundations of Combinatorial
   Theory I: Theory of Mobius Functions*](https://link.springer.com/article/10.1007/BF00531932).

4. **Sheaf-style local-to-global gluing.**  Assign to each clean four-window
   its response-coordinate space and to each overlap the legally observable
   restriction map.  A global response is a compatible section.  This makes
   the proposed multi-shore attack concrete: compute whether the kernel
   directions survive gluing, or whether overlap consistency kills them.
   Cohomological language is optional; first one must prove the actual legal
   restriction maps.  Robinson's sensor-integration framework supplies the
   neighboring formalism, not a ready-made graph theorem.  [Robinson,
   *Sheaves are the canonical datastructure for sensor
   integration*](https://arxiv.org/abs/1603.01446).

The ranked symbolic program from this translation is:

1. compute the companion-selector matroid on the marked shore and decide
   whether its complementary root pair can always be made rank two;
2. glue two or three overlapping marked shores and compute the common
   observation kernel on the Boolean pair faces;
3. eliminate those hidden pair faces from the synchronized dual-Wick ideals;
4. if the visible projection is dominant, stop pursuing that invariant and
   enlarge the legal observation system rather than enumerating supports.

This program is finite-dimensional symbolic algebra on forced windows.  It
does not ask for an enumeration of the 4.6-million quadruple shell.

The first selector-matroid calculation now closes two weaker versions of this
program.  The unsigned `K_4` star-incidence block has rank four on six pair
faces, with exact two-dimensional kernel
`(-s-t,s,t,t,s,-s-t)`.  Two new legal rows complete a pair family exactly
when their defect signatures on that kernel are independent.  An actual
two-residual response lies in the kernel, so top and star data do not imply
partition closure.  On several windows the correct recovery condition is a
rank difference after quotienting nuisance pair columns; all four-windows on
five ports are sufficient, but current P7 theory forces only one.

Rank-two root data need not occur on the forced shore either.  Three exact
canonical pure `P_7` matrices with axis pattern `2+2+1` have all rank-two
marked-shore products zero and nonzero pure permanents.  A positive weighted
Laplace theorem recovers co-occurrence whenever the graph of rank-at-least-two
pairs has a common nonzero weighted degree.  This covers every non-axis case
and the all-axis patterns `5` and `3+2`, leaving the singleton partitions
`4+1`, `3+1+1`, and `2+2+1` as the exact rank boundary.

Finally, algebraic-matroid elimination on only the top faces is now settled
negatively.  One scalar/pure graph family exposes all six marked four-windows
with independent top selectors and maps rationally onto a dense open subset
of the twelve top `M/Z` coordinates plus the two-port aggregate.  Its visible
elimination ideal is zero.  A circuit polynomial must therefore include a
lower pair face, a mixed-colour coefficient, or a shared-block constraint.
See
`P7_SELECTOR_MATROID_RANK_COOCCURRENCE_AND_TOP_PROJECTION_BOUNDARY.md`.

The first lower-face circuit is now explicit.  On three directions at each
endpoint of one physical pair, the corrected two-residual response is the
rank-at-most-two matrix

```text
D_uv=a_u b_v^T+b_u a_v^T,
det D_uv=0.
```

Its nine entries form a minimal algebraic-matroid circuit: omitting any one
entry makes coordinate projection dominant.  A two-chart minor may have full
rank, and the three diagonal entries admit arbitrary common-block
interpolation.  More strongly, three same-colour pair/top response varieties
form a fibre product over the common residual scalar.  Thus the algebraic
matroid says exactly what the next sensor must see: the six off-diagonal mixed
entries of one pair block.

Neither the all-axis jet frames nor companion matching topology supplies that
sensor.  Every all-axis tuple has a globally consistent formal diagonal
deletion-state model for all mixed root subsets.  The singleton partitions
also have three- or four-edge strong companion graphs saturating every
axis-deficient shore, often with one or both residual endpoints unused.
Lower-frame class count can use frozen-root partner sets instead of `Q`.
Hence only common principal-hafnian values or an actual mixed-word selector
can activate the determinant.  See
`P7_MIXED_COLOR_PAIR_CIRCUIT_AND_AXIS_JET_BOUNDARY.md`.

The common-companion equations now separate two of the exceptional axis
patterns from the third.  In the strict tangent-only model with exactly two
effective residual endpoints, three same-axis roots are impossible: pair
rank two makes each root--root form diagonal, while the two triple endpoint
forms force the endpoint frame at a third root to vanish or collapse to rank
one.  Hence `4+1` and `3+1+1` are conditionally excluded.  A single explicit
common block system satisfies all lower-root equations for `2+2+1`, including
the nontrivial identity `G_0+G_Q=7y_1y_2y_3y_4`, against a nonconflicting
formal cofactor ledger.  Realizing that ledger as simultaneous principal
hafnians remains the exact gap.  See
`P7_TWO_ENDPOINT_AXIS_MULTIPLICITY_REDUCTION_AND_221_COMMON_JET_MODEL.md`.

That gap is absent in each scalar colour chart separately.  Two rational
coordinate-copy graphs realize the complete colour-0 and colour-1 ledger,
and an exact forced-private construction over `Q(sqrt(21))` realizes the
colour-2 ledger, including its signed pair values and `1/7` quartet.  Hence no
monochromatic principal-hafnian identity can exclude `2+2+1`.  The terminal
block mismatch in those first certificates is also removable: squarefree
Wick deconvolution produces a determinant-one four-core factorization for
colour 0, an involution transfers it to colour 1, and both use the existing
colour-2 terminal block.  All 186 scalar coordinates therefore share one
terminal matrix.  That common matrix is already sufficient to glue the three
charts into one honest bilinear block graph on their pure colour evaluations:
core--core chart values occupy the three diagonal entries of each physical
block, while core--terminal chart values occupy one common frozen-terminal
column.  The resulting graph realizes all 186 prescribed and six free pure
cofactors.  Its canonical diagonal lift nevertheless has the exact forbidden
mixed coefficient `1/7` at deletion `1234ab` and core word `2220000`.
Off-diagonal core-colour entries are invisible to every pure chart and could
still cancel it, so this is a boundary for the diagonal lift rather than a
universal obstruction.
See
`P7_221_FORMAL_LEDGER_SCALAR_HAFNIAN_REALIZABILITY_AND_SYNCHRONIZATION_GAP.md`.
See
`P7_221_COMMON_TERMINAL_BLOCK_SCALAR_HAFNIAN_REALIZABILITY.md`.
See
`P7_221_DIAGONAL_BLOCK_GLUING_AND_MIXED_WORD_BOUNDARY.md`.

The mixed tensor residual has now been localized symbolically.  Regard the
terminal deletion labels as squarefree presence variables and take one mixed
blocker-word coefficient.  Its 62 prescribed faces all vanish, so before
terminal deconvolution it has the two-face form

```text
F_sigma=alpha_sigma*x_(P\Q)+beta_sigma*x_P.
```

Removing the common scalar terminal Gaussian gives

```text
Phi_sigma=alpha_sigma*x_(P\Q)
          +(beta_sigma-M_ab*alpha_sigma)*x_P.
```

Hence the common core has zero mixed degree-one and degree-three faces and
zero mixed degree-five faces except `P\Q`.  This replaces a large list of
mixed deletion equations by two unprescribed coefficients per word; it does
not construct a common off-diagonal extension.  See
`P7_221_TENSOR_COEFFICIENT_WICK_DECONVOLUTION_TWO_FACE_LOCALIZATION.md`.

The low bosonic compounds now give a positive information boundary and a
negative fixed-chart result.  For seven cores,

```text
Phi^(k)=sum_(|S|=k) haf(A[Z\S]) product_(i in S)L_i.
```

The exact insertion identity
`Phi_pqr=D_(B^(qr))Phi_p` makes the cubic response a directional derivative
of the singleton response, not a multiple of its value.  More decisively,
the scalar map to all seven singleton and 35 cubic responses is dominant in
characteristic zero: a fixed integer `42 x 42` Jacobian minor is nonzero.
No universal scalar polynomial in degrees one and three can therefore
exclude the ledger.

At degree five, each response is the one-core-edge compound

```text
Phi_S=sum_(i<j) A_ij per R[Z\{i,j},S].
```

Writing these 21 equations as `Phi^(5)=C_5^per(R)a` exposes an exact
observability theorem.  At `R=I_7`, the fifth permanental compound is the
complement-index permutation matrix, so its determinant is a nonzero degree-
105 polynomial.  A generic incidence therefore recovers every core edge.
When twenty mixed faces vanish and only `P\Q` is free, an invertible compound
confines `a` to one inverse-column line and converts fixed monochromatic edges
into adjugate `2 x 2` proportionality circuits.  The exact `2220000`
incidence has full compound rank 21 over `Q(rho)`.

For the fixed common-terminal charts, the mixed word `2220000` has the exact
dual face selector

```text
Phi_125ab-Phi_145ab-Phi_235ab+Phi_345ab
  =2(805+52 rho)/49 !=0.
```

The alternating row of the fifth permanental compound annihilates all twelve
cross-colour core variables and isolates the fixed monochromatic edge
`A_12=1`.  Since the four corresponding deletion faces are prescribed mixed
zeros, no off-diagonal core completion repairs the indexwise charts.

This is now alignment-independent for the fixed colour-0/colour-2
certificates.  After the column transform `(1-3,2-4,5,a,b)`, the colour-2
rows contain two zero-row pairs carrying nonzero core edges, while three
anchor rows become the coordinate rows `5,a,b`.  For every core bijection, a
row-matroid case split selects one zero-edge pair and a subset of anchors so
that the same four-face rectangle reduces to a nonzero complementary
colour-0 minor.  No cross-colour edge survives.  Hence every alignment of
these fixed charts is excluded without enumerating alignments or words.

The adapted word is essential.  A deliberately relabelled word
`(2,0,2,2,0,0,0)` has a six-parameter solution to all twenty degree-five
equations, with one point also satisfying every singleton equation.  On that
entire family, the three cubic faces `124,125,12a` normalize to

```text
q-delta,        p,        q(p-delta alpha/C).
```

They generate one via
`q*p-q(p-delta alpha/C)-(delta alpha/C)(q-delta)
=delta^2 alpha/C !=0`.  Thus that single word is closed at degree three even
though its degree-five compound system is consistent.  Different pure scalar
realizations remain outside all these fixed-chart theorems.  See
`P7_SEVEN_CORE_BOSONIC_COMPOUND_FIRST_THIRD_JET_BOUNDARY.md` and
`SEVEN_CORE_FIFTH_PERMANENTAL_COMPOUND_OBSERVABILITY_THEOREM.md`,
`P7_221_FIXED_DIAGONAL_LIFT_DEGREE5_MIXED_CIRCUIT_OBSTRUCTION.md`,
`P7_221_ARBITRARY_ALIGNMENT_DEGREE5_RECTANGLE_OBSTRUCTION.md`,
`P7_221_ALIGNED_CORE_DEGREE5_AFFINE_COMPLETION.md`, and
`P7_221_ALIGNED_CORE_DEGREE3_THREE_FACE_NULLSTELLENSATZ_OBSTRUCTION.md`.

The hoped-for single-word extension over the whole pure-chart fibre has an
exact singular boundary.  For every mixed incidence `R`, the system
`C_5^per(R)a=tau e_*` has a finite linear-algebra dichotomy.  If the compound
is invertible, fixed monochromatic coordinates obey adjugate proportionality
circuits.  If it is singular, either a left-kernel vector kills `tau`, or the
solutions form an inverse-image line plus `ker C_5`.  A legal relabelling of
the verified colour-2 chart puts two identical incidence rows into
`2220000`; its compound then has exact rank six.  Explicit cross-colour edges
over `Q(rho)` give `C_5a=0` on all 21 degree-five faces.  This does not evade
the alignment-adaptive fixed-chart theorem, which may choose another word,
and it does not solve degrees one and three.  It proves that neither generic
observability nor one preselected compound determinant is fibre-uniform.  See
`P7_PURE_CHART_FIFTH_COMPOUND_FIBRE_DICHOTOMY_AND_SINGULAR_ESCAPE.md`.

There is nevertheless a coordinate-free full-tensor consequence.  Let
`U_i` be the span of the terminal-incidence covectors at core mode `i` and
project `V_i^*` to `V_i^*/U_i`.  Projecting two modes `i,j` in any degree-five
response kills every matching summand except the one with core edge `A_ij`.
Every physical four-face rectangle therefore has flattening rank at most one
across `{i,j}|rest`.  The formal rectangle `(rho-2)(D_0+D_1)` has rank two
exactly when the projected colour-0 and colour-1 diagonal directions at that
pair are independent.  Consequently every physical realization must make
those two images dependent at all 21 pairs.  A sparse legal projected model
attains rank one when one diagonal direction dies, showing that the
pairwise condition is sharp locally and still needs a global compatibility
argument.  See
`P7_221_DEGREE5_INCIDENCE_QUOTIENT_RECTANGLE_FLATTENING_THEOREM.md`.

The projection cannot be omitted.  An exact physical graph with two core
edges and sparse terminal support realizes the entire non-`D_2` four-face
tuple

```text
((rho-2)D_0,0,0,(rho-2)D_1),
```

and therefore the unprojected contraction `(rho-2)(D_0+D_1)`.  The common
`D_2` baseline remains absent, but the contracted binary GHZ tensor itself is
not a physical/global-idempotent separator.  See
`P7_221_FOUR_FACE_BINARY_GHZ_PHYSICAL_COUNTERMODEL.md`.

The 21 pairwise quotient laws do have a complete global classification.  For
the images `(x_i,y_i)` of the two binary colours, each mode is intrinsically
of type zero, one of the two pure axes, a common line, or a genuine plane.
Two decomposable tensors are proportional only when their corresponding
nonzero factors are proportional.  Hence a genuine-plane mode is compatible
only with zero or pure-axis modes.  Globally, either all seven quotient maps
have rank at most one, so every incidence span meets the binary plane, or one
mode has rank two and each of the other six incidence spans contains an
actual pure axis.  Both alternatives have sharp quotient models.  See
`P7_221_ALL_PAIR_INCIDENCE_QUOTIENT_BINARY_COHERENCE_CLASSIFICATION.md`.

Three other prescribed faces upgrade this from binary to tricolour.  Exact
Wick inversion gives two-colour diagonal tensors on `1234a`, `1235b`, and
`1345b`, coupling the pairs `01`, `02`, and `12`, respectively, with all
coefficients nonzero in `Q(rho)`.  Hence for every core pair the three
projected diagonal tensors
`x_i^c tensor x_j^c`, `c=0,1,2`, span at most one dimension.

This admits a coordinate-free projective-support classification.  Let `S_i`
be the colours surviving at mode `i`, and let `I_i` be the colour pairs whose
images are independent there.  The quotient equations hold exactly when no
pair in `I_i` is wholly contained in `S_j` for `i!=j`.  Every quotient map of
rank at least two contributes a nonempty `I_i`, and distinct such modes must
contribute distinct colour pairs.  There are only three pairs, so at most
three of seven quotient maps have rank at least two.  At least four incidence
spans therefore meet the three-colour diagonal space in dimension at least
two.  Three rank-two modes, supported on `01`, `12`, and `02`, attain the
bound.  See
`P7_221_TRICOLOUR_INCIDENCE_QUOTIENT_PROJECTIVE_SUPPORT_THEOREM.md`.

The mixed-word selector itself is no longer missing in the factorized `h=0`
branch.  For a selected pair `{u,v}`, choose a common residual-null vector at
each of the other five blockers and contract those five legs in the full
`P_7` word tensor.  Every other surplus-two pair term meets a contracted null
leg and vanishes termwise.  The result is the exact matrix identity

```text
s_uv D_uv=diag(d_c product_(w notin {u,v}) kappa_w[c]).
```

Since `rank D_uv<=2`, five torus-capable null spaces would make the right side
rank three.  Thus at most four of seven common null spaces meet the coordinate
torus, or equivalently at least three residual row spans contain a coordinate
covector.  This is an arbitrary-order three-boundary law.  It does not extend
directly to `h!=0`, where the selected response is `hB_uv+D_uv` and may have
rank three.  See `P7_RESIDUAL_NULL_POLAR_SELECTOR_H0_THEOREM.md`.

The canonical incidence profile does not strengthen the resulting count by
itself.  Residual polar planes can be prescribed independently of the
canonical root-row planes.  An exact rational model has the required
`012,01,01,02,02,12,12` spans, nonzero pure permanents, and nonzero pure
residual factors, yet exactly three non-torus null lines, all clustered at
`t,01,01` and all carrying the same coordinate incidence.  More generally
the incidence positions and labels are arbitrary at this layer.  Hence any
next obstruction must restore the per-colour kernel Hall quotas or retain the
full contracted matrix identities; the coarse incidence corollary plus pure
data is sharp.  See
`P7_RESIDUAL_NULL_INCIDENCE_CANONICAL_PROFILE_SHARPNESS.md`.

Doing both gives a new arbitrary-order theorem.  For any selected source-row
pair in `P_m -> Delta_3`, each target colour occurs in its local row span at
least twice.  If only three modes had any coordinate incidence, their planes
would be exactly `01,02,12`.  Contracting through the third null axis and all
torus nulls isolates a nonzero rank-one diagonal on the other two modes.  But
their two rank-two row maps compose through the nondegenerate two-channel
pairing to rank exactly two.  Thus every source-row pair has at least four
coordinate-incidence modes.  A complete symbolic classification of equality
at four has six types, indexed by the number of doubleton incidence modes.
Five die on a unique size-two colour neighbourhood with rank-two endpoints.
The repeated-pair type first forces one singleton mode to be exactly
`<e_0^*>`; a second polar contraction then gives the same rank-one/rank-two
contradiction.  Therefore every pair has at least five incidence modes.
Applied to factorized `P_7` port rows, the torus/non-torus split improves to
at most `2/5`.  See
`ARBITRARY_PERMANENT_FOUR_MODE_ROW_PAIR_INCIDENCE_THEOREM.md` and
`ARBITRARY_PERMANENT_FIVE_MODE_ROW_PAIR_INCIDENCE_THEOREM.md`.

That five-mode theorem is sharp at exactly the level used in its proof.
There are nineteen equality-at-five colour-orbit types, distributed by one
through five doubleton incidence modes as `1,4,6,5,3`.  Polar rank reduces
them to three types.  An exact Type-D4 `P_7` model satisfies all 21 polar
identities with canonical root spans, local concision, nonzero pure `P_5`
permanents, and nonzero residual pure factors.  Its residual pair response
still has rank two.  It is not asserted to satisfy the full mixed coefficient
identity.  Thus a stronger incidence bound cannot follow from the polar,
canonical, and pure data alone; the next step must use the common-core mixed
equations.  See
`FIVE_MODE_ROW_PAIR_INCIDENCE_EQUALITY_POLAR_CLASSIFICATION_SHARPNESS.md`.

For `h!=0`, synchronized deletion depth is exactly the missing observable.
If both the residual-absent tensor `T_0` and residual-present tensor `T_Q`
are legally exposed with the same direct blocks and root cofactors, then

```text
T_Q-hT_0=sum D_uv tensor F_uv
```

globally cancels the arbitrary direct layer.  Residual-null polarization and
the four-mode theorem then apply whenever
`product_c(z_0[c]z_1[c]-h)` is nonzero.  A persistent coordinate-monomial
escape reduces to the aligned resonance `h=z_0[c]z_1[c]`; every scalar
two-depth cancellation loses that same target colour, so rank three is gone.
When pure and full pair blocks are jointly visible, the corrected matrix
pencil has a common rank-two root and vanishing minor resultants.  Full blocks
alone remain affine-unconstrained.  One top `P_7` equation does not supply the
required `T_0`, so this is a conditional boundary rather than an exclusion.
Under the strict all-axis two-endpoint assumptions, singleton jets do force
both endpoint forms to be bases and hence make the empty/`Q` pair companions
independent.  The marked shore then legally exposes synchronized top
responses.  But it restricts each blocker to a root-null line: the induced
observation of a `3 x 3` pair block has rank one and kernel dimension eight.
The exact family `M_a=1+a x_3x_4`, `Phi_a=h+a^(-1)x_1x_2` fixes all exposed
top data while its lower direct and corrected pairs vary.  Thus synchronized
top exposure is strictly weaker than the partition-closed pair
synchronization needed by the determinant.
See
`P7_SYNCHRONIZED_TWO_DEPTH_POLAR_SELECTOR_AND_ALIGNED_RESONANCE_BOUNDARY.md`.
See
`P7_STRICT_TWO_ENDPOINT_SYNCHRONIZED_TOP_FACE_AND_SHORE_LINE_BOUNDARY.md`.

## Legal lower-jet observability after the residual translation

The residual-relative response theorem now has a sharp legality boundary at
the actual `P_7` root budget.  If `q` residual vertices are retained, only

```text
z_S with |S|>=q,          m_S with |S|>=2q
```

can be isolated by the current probe-root principal-cofactor mechanism.  At
`q=2`, every direct pair `m_e` is missing; at `q=4`, every direct layer and
even the residual-present pair layer are missing.  Granting the maximal
`q=2` visible window, the residual scalar, and all four marked-star values
does not create a hidden relation: the honest response map is dominant, with
an exact Jacobian minor `360`.  The four-point insertion is nevertheless
recoverable on the precise additive locus

```text
z_12+z_34=z_13+z_24=z_14+z_23.
```

At `q=4`, the same four-point expression equals a quartic permanental
compound rather than zero.  See
`P7_ROOT_BUDGET_DUAL_WICK_OBSERVABILITY_AND_QUARTIC_ESCAPE.md`.

The marked-star sensor itself has now been solved exactly.  Any three clean
four-windows on the six double blockers recover at most five of one target
window's six pair faces, and five is attained.  Four windows are both
necessary and sufficient: the tetrahedral fan

```text
1234, 1256, 1356, 1456
```

cancels every nuisance pair and reconstructs the target `K_4` by explicit
linear formulas.  This is a new bosonic boundary-tomography lemma rather than
an imported theorem.  Fixed-complement Laplace expansion now forces all six
graph-side windows in every pure colour, so the fourth fan window itself is
no longer the obstruction.  What remains is compatible marked-star exposure
and residual-present pair normalization on those windows.  See
`P7_THREE_CLEAN_WINDOW_PAIR_FACE_RECOVERY_NO_GO.md` and
`P7_FOUR_CLEAN_WINDOW_TETRAHEDRAL_PAIR_TOMOGRAPHY_THEOREM.md`, and
`P7_FIXED_COMPLEMENT_LAPLACE_FAN_COVER_AND_LOWER_FRAME_SEPARATION.md`.

Two other apparent bridges are closed.  First, for `h!=0` the direct term
makes the top two-port cofactor map affine-surjective, so synchronization is
not observable without a companion depth.  The exact `P_5` and one-port
`P_6` support transfers remain unconditional under their extraction
hypotheses, but the support-`24` `P_7` transfer remains conditional.  See
`GRAPH_EXTRACTION_TOP_TWO_PORT_SYNCHRONIZATION_OBSERVABILITY_BOUNDARY.md`.
Second, face-specific incidence quotients obey a canonical Mayer--Vietoris
exact sequence and common-edge descent, but a rational seven-mode lift
satisfies all overlap comparisons at the sharp tricolour ranks.  Projective
edge lines alone therefore cannot finish the gluing.  Residual five-row
permanents, unprojected equations, or joint degrees are essential.  See
`P7_221_FACE_SPECIFIC_QUOTIENT_MAYER_VIETORIS_AND_SHARP_LIFT.md`.

## Cross-area translation after the two-face reduction

The current equations sit close to several established subjects, but the
transfers have different legal strength.

1. **Algebraic statistics and trek separation.**  Trek separation turns
   graphical path factorizations into low-rank covariance submatrices and
   determinantal constraints.  The bosonic transfer is not a covariance
   determinant: it is the permanental compound in the degree-five formula
   above.  Its dual rows are still exact observable selectors.  The new
   four-face circuit is the first successful transfer of that strategy: a
   `2 x 2` alternating face functional isolates one hidden core edge without
   reconstructing the remaining edge vector.  See Sullivant, Talaska, and
   Draisma, [*Trek separation for Gaussian graphical
   models*](https://arxiv.org/abs/0812.1938).  Permanental compound matrices
   also have an independent matrix-theory literature; unlike determinantal
   ideals, even ideals of generic `2 x 2` subpermanents can have embedded
   components and several minimal-prime heights.  See Al'pina and Al'pin,
   [*Permanental compound matrices and Schneider's
   theorem*](https://doi.org/10.1007/s10958-005-0483-6), and Laubenbacher and
   Swanson, [*Permanental Ideals*](https://arxiv.org/abs/math/9812112).

2. **Moment and cumulant varieties.**  Gaussian moment varieties suggest
   studying the Zariski image of the compound parametrization, while binary
   cumulant coordinates suggest Boolean-lattice Mobius changes that simplify
   hidden-subset models.  Both transfers are now concrete: Jacobian dominance
   proves that the scalar first/third moment image has no equations, and
   squarefree Wick deconvolution reduces every mixed word to two faces.  See
   Amendola, Faugere, and Sturmfels, [*Moment Varieties of Gaussian
   Mixtures*](https://arxiv.org/abs/1510.04654), and Sturmfels and Zwiernik,
   [*Binary Cumulant Varieties*](https://arxiv.org/abs/1103.0153).

3. **Gaussian photon cumulants and connected matching objects.**  In photon
   statistics, loop hafnians encode moments and the Montrealer encodes
   connected cumulants/Hamiltonian cycles.  This suggests testing a connected
   degree-five selector once several blocker words are coupled.  It does not
   create a new equation for the current marker-linear deletion cube: its
   legal cumulant is exactly the Wick deconvolution already used.  See Cardin
   and Quesada, [*Photon-number moments and cumulants of Gaussian
   states*](https://arxiv.org/abs/2212.06067).

4. **Hafnian shuffle identities.**  Shuffle-algebra proofs organize Wick and
   hafnian identities without signs and may compress higher compound
   calculations.  They apply to complete compatible families, so a proposed
   use must still prove that the required deletion faces are legally present.
   See Luque and Thibon, [*Pfaffian and hafnian identities in shuffle
   algebras*](https://arxiv.org/abs/math/0204026).

5. **Tensor-network image geometry.**  The formal global-idempotent common
   core realizes every diagonal chart because it suppresses mixed products;
   the physical vertexwise tensor algebra does not.  This is an exact image
   membership problem, not merely orbit-closure or border membership.  The
   new incidence quotient is a small image equation of this kind: after two
   mode quotients, a physical degree-five rectangle lies on a Segre rank-one
   cone.  The formal GHZ rectangle misses that cone unless the quotient makes
   its two diagonal summands dependent.  The known nonclosedness of
   tensor-network state spaces is nevertheless a warning against accepting a
   degeneration as a physical realization.  See
   Landsberg, Qi, and Ye, [*On the geometry of tensor network
   states*](https://arxiv.org/abs/1105.4449).

The alignment-independent dual row now exists for the current fixed scalar
certificates, but a fixed word can enter a rank-six singular compound stratum
inside the same pure fibre.  The strongest new route is consequently a joint
compatibility invariant across words, degrees, or the 21 pairwise incidence
quotients.  Ordinary matchgate/spinor identities remain conditional because
generic hafnian signs do not transfer.

## Cofactor-depth grading and the new symbolic frontier

The latest results suggest a useful invented object: the **cofactor-depth
grading**.  Give a complementary principal-hafnian symbol three indices,

```text
C_(I,A,D),                                             (23)
```

where `I` is the differentiated root set, `A` is the set of nonblocker
companion endpoints deleted with it, and `D` is the deleted blocker set.
The projective nonempty root jets live entirely in blocker depth `D=empty`.
The pair observations needed by tetrahedral tomography instead have
`|D|=5`.  Before principal-hafnian realizability is imposed, different
deletion labels are independent coordinates.  The jet-orthogonal splice
supplies a point of the complete 31-equation depth-zero ledger; adjoining the
pair-face variables is therefore a polynomial-ring extension.  Its
elimination ideal in the depth-five pair coordinates is zero.

This gives an exact observability theorem, not only a metaphor:

```text
all nonempty projective root jets
  !=> any polynomial constraint on the marked pair-face defect.    (24)
```

The missing information must be a **cross-depth principal-hafnian relation**
or a legal observation that physically identifies coordinates at the two
depths.  This is the rigorous core of a possible cofactor-depth spectral
sequence: the formal first page splits by deletion depth, while physical
hafnian condensation, common-edge matching, and marked-star exposure are
the only currently known candidates for differentials between pages.  No
spectral-sequence convergence theorem is claimed; (23)--(24) are the proved
graded statement that any such theory must extend.

The graph-side fan and its target equation now meet on a particularly sharp
boundary.  Fixed-complement Laplace forces every one of the eighteen
colour-tagged clean windows and hence the tetrahedral fan.  A jet-orthogonal
common-block model retains them while satisfying all 31 nonempty mixed root
jets, and its distinguished empty/residual companion forms are independent
at every shore even though every nonzero shore has cofactor-image rank one.
Thus cofactor-image rank and selector rank are separate invariants.  But each
canonical clean-window word is GHZ-null.  Independent selectors force

```text
m_W=z_W=0,
sum_(|e|=2) z_e m_(W minus e)=0,                      (25)
```

rather than a nonzero moment chart.  The family
`M=1+t`, `Phi=lambda-lambda*t`, `Z=lambda` satisfies every such response
equation with fixed nonempty data and varying empty scalar.  Root singleton
companions and the blocker singleton depths needed to recover `lambda` are
different physical edge families.  See
`P7_221_JET_ORTHOGONAL_SPLICE_AND_FORMAL_FIXED_WINDOW_NO_GO.md` and
`P7_GHZ_NULL_FAN_DUAL_WICK_DEFECT_AND_SINGLETON_DEPTH_SEPARATION.md`.

The vacuum-free part of dual Wick survives this collapse.  For
`|S|=2d>=4`,

```text
D_S=sum_(|e|=2) z_e m_(S minus e)-z_S=(d-1)h m_S.     (26)
```

Cross-window minors eliminate `h`, and a compatible nonzero `m_4` or `m_6`
recovers it.  Equation (25) shows that the forced canonical fan instead lies
on the simultaneous moment-null stratum.  A successful empty-face theory
must therefore prove that some legally exposed noncanonical moment is
nonzero, or synchronize paired blocker-singleton depths; it cannot merely
add more canonical fan windows.  See
`P7_VACUUM_FREE_DUAL_WICK_PROJECTIVIZATION_AND_EMPTY_SCALAR_ESCAPE.md`.

The residual-permanent translation has also moved from facewise ranks to one
common quotient.  Quotienting any three core modes by the full terminal-
incidence spans kills every degree-five physical term.  Three independent
prescribed diagonal faces then force

```text
sum_i rank(q_i restricted to E_i)<=6.                 (27)
```

At equality, the three colour supports are distinct two-mode sets.  If they
were disjoint, degree-five Laplace descent would make every projected
four-point core hafnian vanish on the six active modes.  A new bosonic
matching lemma proves that a characteristic-zero six-vertex edge system with
all four-point hafnians zero has matching number at most two, contradicting
the three forced support edges.  Hence the disjoint equality stratum is
excluded.  The triangle `01,12,02` realizes the overlapping quotient shadow,
so the next circuit must distinguish overlapping supports or force the rank
strictly below six.  See
`P7_221_THREE_MODE_RESIDUAL_ANNIHILATION_AND_FULL_QUOTIENT_RANK_SUM_BOUND.md`
and
`P7_221_EXTREMAL_RANK_SIX_DISJOINT_SUPPORT_DEGREE3_HAFNIAN_OBSTRUCTION.md`.

A separate invented low-jet calculus closes the minimal tangent-cycle
topology.  Coordinatewise squaring on the two-dimensional diagonal quotient
forces the edge classes to the three projective Hadamard idempotents; a
three-root matching pinch leaves only an even alternating binary cycle.
Uniform full-root derivatives along the two idempotent axes then select two
different perfect matchings with the same complete deletion set.  Both graph
derivatives use one common principal cofactor, while the GHZ derivatives are
independent pure tensors.  This **common-cofactor collision** excludes the
minimal cycle at full root order.  Nonminimal companion systems remain open;
see
`ROOT_TANGENT_MINIMAL_CYCLE_IDEMPOTENT_SECOND_THIRD_JET_CLASSIFICATION.md`.

## 3 August polar, overlap, and null-stratum refinements

The cofactor-depth proposal now has its first exact generic route
elimination.  Let `h` be the generic six-vertex hafnian and
`C_ij=partial h/partial x_ij` its fifteen four-point principal cofactors.
There is no cubic polynomial `P` with

```text
h^2=P((C_ij)_(i<j)).                                  (28)
```

The proof averages a putative identity to `S_6`, classifies the eight
three-edge multigraph orbit sums, and uses eight private coefficients plus
the coefficient of two disjoint triangles.  The private coefficients force
the matching-orbit coefficient to one, while the last coefficient gives
`6=0`.  Cofactor dominance also rules out weights below eight when
`weight(C)=2` and `weight(h)=3`.  Thus the deletion-depth differential cannot
be a bosonic copy of the determinant adjugate or the lowest polynomial
multiplicative-Legendre formula.

This is exactly where the neighboring literatures separate.  The
multiplicative-Legendre theory of cubic homaloidal polynomials explains why
(28) is the natural first polar formula; see Chaput and Sabatino,
[*On homaloidal polynomial functions of degree 3 and prehomogeneous vector
spaces*](https://arxiv.org/abs/1011.5975).  Luque--Thibon shuffle identities
still organize complete Wick families, but (28) proves that they cannot
collapse the generic six-blocker chart to a sign-free cubic adjugate.  The
quadratic Wick relations of the spinor variety remain available only after
a compatible Pfaffian chart has been proved; see Rincón,
[*Isotropical Linear Spaces and Valuated
Delta-Matroids*](https://arxiv.org/abs/1004.4950).  The appropriate generic
replacement is therefore the algebraic correspondence of the generically
finite polar map, while the `P_7` problem still needs a special-fibre or
tensor-valued incidence theorem.  See
`SIX_BLOCKER_HAFNIAN_POLAR_CUBIC_CONDENSATION_NO_GO.md`.

There is still a universal differential across the grading.  If a clean
three-root/three-blocker shore has nonzero permanent `f`, a complementary
blocker-edge derivative of the two depth-zero root-pair cofactors gives

```text
partial_(a_p) L C_I=f z_e,
partial_(a_p) L C_(I union Q)=f m_e,       p=W minus e. (29)
```

Thus formal hafnian differentiation supplies all six pair faces with common
normalization.  The legal physical sector is stricter: a tangent root pair
contributes `f per(K[:,p]) z_e`, where `K` is its `2 x 4` root-to-window
incidence matrix.  Four ordinary unit marked stars from that root pair exist
exactly when all six second permanental minors of `K` are one common nonzero
scalar.  Pure-shore nonvanishing does not force this.  In the projectively
constant branch `K=0`, so the differential is identically zero on every
physical marked sector.  Edge differentiation changes a bilinear edge block
and cannot be smuggled in as local scalar rescaling.  The new cofactor-depth
object is therefore a quiver with a proved formal arrow and a proved zero
physical realization on the projective page; a nonprojective incidence
sector or new edge-specific circuit is required.  See
`P7_CROSS_DEPTH_HAFNIAN_DERIVATIVE_AND_PROJECTIVE_MARKED_STAR_BOUNDARY.md`.

The equality-six quotient has also been classified structurally.  Three
distinct two-mode supports form one of

```text
3K2,        P3 disjoint-union K2,        P4,        K1,3,        K3. (30)
```

Full residual Laplace descent forces every projected four-hafnian on a
four-set containing a support edge to vanish, and forces the analogous
six-point quotient shadow.  The earlier matching theorem excludes `3K2`.
For `P3 disjoint-union K2`, six legally descended tensor components satisfy
an explicit characteristic-zero unit certificate

```text
E-tB-rD+((st+rw)/2)(pE+F-xC-yA)=1.                   (31)
```

Hence that type is excluded too.  Exact vertexwise quotient controls for
`P4`, `K1,3`, and `K3` satisfy every forced degree-three and degree-one
shadow, so those three are the sharp physical-lift frontier rather than
targets for another quotient-only rank argument.  See
`P7_221_OVERLAPPING_RANK_SIX_SUPPORT_CLASSIFICATION_AND_P3K2_CUBIC_OBSTRUCTION.md`.

Finally, the canonical null fan is complete at four-point depth.  The
eighteen colour-tagged windows cover all fifteen four-subsets of the six
double blockers.  Conditional independent top selectors therefore give
all `m4=z4=0`; the characteristic-zero matching lemma then gives support
matching number at most two and hence `m6=z6=0`.  The residual correction
`K=Z_2-hB` is tangent to this simultaneous four-hafnian-zero locus.  A
rational common-block sharpness control has all three pure coefficients
equal to one and only the canonical clean axes.  Even after both full
blocker-singleton rows are installed, all nonempty responses remain fixed
while `h` varies when `B=0`.  Consequently, a successful vacuum recovery
must legally co-expose a nonzero direct pair with the paired residual data,
or use the complete mixed system to force departure from `B=0`; simply
adding singleton rows is insufficient.  See
`P7_COMPLETE_FOUR_FACE_NULL_STRATUM_AND_PAIRED_DEPTH_SHARPNESS.md`.

## 3 August tensor-axis transfer on the canonical P6 section

The split-surjective scalar six-face construction has now been tested
against the complete first mixed-colour layer.  For majority colour `c` and
singleton colour `d`, all `5+1` coefficients on the six faces are one
symbolic axis family

```text
sum_(u in S minus {v}) B_vu[d,c]
    haf A^(c)[S minus {u,v}]=0.                      (32)
```

The six pure face values enter through the two-coordinate complement-sum
covariant

```text
kappa_c=(y45+y67-y46-y57, y45+y67-y47-y56).         (33)
```

When the two relevant covariants are nonzero, the combined `72 x 56` axis
operator has rank 51.  Its kernel is exactly the five-dimensional space of
hollow directed core matrices with zero row and column sums.  In particular,
every off-diagonal colour entry touching the four-window is forced to zero.
The next `4+2` coefficient is then `3b_pq^(d)`.  All three exact Segre
columns have nonzero `kappa`, all eighteen `b_pq` are nonzero, and one fixed
coefficient is `3b_45^(2)=-10`.  Hence no off-diagonal completion of the
canonical common-graph section is GHZ diagonal.

The residual five-space is a directed-flow shadow of the mixed coefficient
ideal; the complement-sum covariant is its two-dimensional matching-sum
quotient.  This is a new problem-specific axis/circulation translation, not
a colour-word search.  An exact GHZ stabilizer theorem also shows that every
invertible local GHZ-to-GHZ gauge is monomial, so the nonzero mixed
coefficient survives the whole target-stabilizer orbit.  Other scalar points
in the split-surjective face fibre remain open.  See
`P6_AXIS_COMPLEMENT_SUM_COVARIANT_OFFDIAGONAL_AND_GAUGE_NO_GO.md`.

## 3 August arbitrary-fibre P6 axis/Gram transfer

The canonical rank-51 obstruction is not a property of the six pure face
values alone.  For any scalar realization of those values, split the 56
directed axis variables into twelve core columns and forty-four columns
incident to the four-window.  If `M` is the complete `5+1` axis operator and
`M_C` its core restriction, then projection of `ker M` to the port columns
has the exact dimension

```text
delta = 44-rank(M)+rank(M_C).
```

This is a quotient-matroid identity: the projected kernel is the kernel of
the port map after quotienting the equation space by the core image.  Hence
port-supported cancellation exists exactly when `delta>0`, with no choice
of section built into the criterion.

At the exact `tau=0` scalar section, all pure core--window edges vanish,
core edges equal one, and window edge `pq` equals `y_pq/3`.  It realizes the
same six prescribed faces in every colour, but now

```text
(rank M, rank M_C, nullity M, delta)=(19,7,37,32).
```

The kernel is the direct sum of all 32 directed core--window axes and the
five-dimensional core circulation space.  Thus the formerly forced
`3b_pq` coefficient can be cancelled.  Writing the core--window entries for
an ordered colour pair as a `4 x 4` matrix `X` and `D=J_4-I_4`, all six
window-pair-minority coefficients become

```text
y_pq+x_p^T D x_q.
```

The three required hollow symmetric Gram matrices are nonsingular.  Over an
algebraically closed characteristic-zero field, congruence of nondegenerate
symmetric forms supplies invertible `X` with `X^T D X=-y` off diagonal.
This simultaneously kills every `5+1` coefficient and every `4+2` word whose
minority vertices are the two window ports.

The translation exposes a new, location-sensitive residual.  If one
minority vertex is core vertex `i` and the other is window vertex `p`, the
coefficient is exactly

```text
Y_(i,q)(DX)_(i,p).
```

If both directed Gram factors are invertible and every such residual
vanishes, their row supports force one factor to be monomial.  Its Gram
matrix would then obey
`y_45 y_67=y_46 y_57=y_47 y_56`; the three exact columns give respectively
`(126,696,300)`, `(180,1914,1080)`, and `(-46,2774,1350)`.  Therefore the
nonsingular Gram route cannot finish the two-colour equations.  Singular
factors and the other `4+2` placements on this section are closed by the
tetrad-support theorem below; a different scalar fibre and the genuinely
three-colour system remain open.  This is an exact symbolic
fibre/Gram reduction, not a word or parameter search.  Representable-matroid
contraction and symmetric matrix completion are the neighboring theories;
see [Rosen--Sidman--Theran](https://arxiv.org/abs/1809.00865) and
[Bernstein--Blekherman--Lee](https://arxiv.org/abs/1909.06593).  The rank and
product claims here are proved directly.  See
`P6_ARBITRARY_FIBRE_AXIS_PORT_DEFECT_AND_TWO_COLOUR_GRAM_ESCAPE_THEOREM.md`.

## 3 August tau-zero tetrad-support closure

The full `tau=0` axis kernel has arbitrary core--window matrices `X,Y` and a
five-dimensional directed core circulation `Z`.  No rank assumption is now
needed.  On a face with window pair `p,q`, define

```text
P_ij(Y;pq)=Y_ipY_jq+Y_iqY_jp,
R_ij(Z)=Z_ikZ_jl+Z_ilZ_jk,
```

where `{k,l}` complements `{i,j}` in the four-core.  Three complete `4+2`
matching placements give

```text
3b_pq+sum_(i<j)P_ij=0,
b_pq(1+R_ij)+P_ij=0,
Y_iq(DX)_ip=0                         (p!=q).          (33a)
```

Thus every symmetrized row-pair vector of `Y` lies on the fixed line `Kb`.
For a full-support line which fails the complementary-product tetrads, the
map `s -> offdiag(r symmetric s)` is injective whenever `r` has support at
least three.  A graph on the four row indices then has exactly one nonzero
edge: a vertex of degree two would make two neighboring rows proportional
and force the tetrads, while two disjoint edges contradict injectivity.
Therefore `Y` has exactly two nonzero rows.  Swapping colours gives the same
conclusion for `X`.

The mixed equation in (33a) forces the two row supports to be complementary
and the two nonzero rows of `X` to sum to zero.  Their unique row-pair vector
is consequently

```text
(-2r_pr_q)_(p<q),                                      (33b)
```

which satisfies all complementary-product tetrads.  Each exact face column
violates those identities, a contradiction.  This excludes every singular
and nonsingular factor and every core circulation surviving `5+1` at
`tau=0`.

The zero-circulation subcase has an arbitrary-order Euler explanation.  For
a `2m`-core, the both-core equations and

```text
sum_(i<j)a_ij haf(A[C minus {i,j}])=m haf(A)          (33c)
```

turn the window equation into `(1-m)b haf(A)=0`.  The full circulation
escapes this sum-only test through one exact quadratic energy `E(Z)=-3`, but
the individual row-pair and mixed equations above still close it.

Finally, the previous nonzero-`tau` theorem handles any pair of nonzero
section parameters.  If `tau_c!=0` and `tau_d=0`, the majority-`c` axis
equations kill the core-`d`/window-`c` entries, leaving a nonzero `3b_pq^c`
on some face.  Hence every point of the explicit
`(tau_0,tau_1,tau_2)` split-surjective section family is excluded.  This
does not exclude other points of the much larger six-face scalar fibre.
The tetrad language is adjacent to
[Drton--Sturmfels--Sullivant](https://arxiv.org/abs/math/0509390); the
row-support and mixed-location closure are proved directly here.  See
`P6_TAU_ZERO_SINGULAR_GRAM_TETRAD_SUPPORT_AND_FOUR_PLUS_TWO_NO_GO.md`.

## 3 August two-shore fibre and obstruction transfer

The excluded tau-section is not representative of the entire scalar fibre.
There is an exact rational point with matching core

```text
a_01=3,       a_23=1,
```

all other core and all window edges zero, and only core--window rows 0 and 1
active.  Rows 2 and 3 vanish.  Writing the two active rows as `r,s`, the six
face values are the hyperbolic Gram coordinates

```text
y_pq=r_p s_q+s_p r_q.                                (33d)
```

Every full-support six-vector has a rational factor of this form after a
rank-two diagonal completion; explicit rational factors realize all three
fixed target columns.  For each colour pair the resulting axis operator has

```text
(rank M,rank M_C,nullity M,delta)=(30,2,26,16).       (33e)
```

Its kernel is exactly the coordinate span of the sixteen bidirected edges
between the inactive core pair and the window, together with ten core--core
directions.  An exact deformation in those coordinates kills the
both-window-minority family, the inactive-core-pair family, and one active
core/window family.  The other active-row placement is not killed: its
coefficient is

```text
s_p^(d)r_q^(c),                                      (33f)
```

and a face-45 orientation makes (33f) equal the prescribed nonzero face
value in colour `d`.

This is a strict obstruction transfer, not a P6 construction.  It proves
that neither the tau tetrad nor the location of its first fatal `4+2`
coefficient is fibre-invariant.  A genuine invariant must couple both
hyperbolic shore rows, use the additional H4 target incidence, or survive a
further axis deformation.  The rank-two diagonal completion is the same
algebraic-factor-analysis geometry developed by
[Drton--Sturmfels--Sullivant](https://arxiv.org/abs/math/0509390); all
identities and ranks used here are proved directly.  See
`P6_TWO_SHORE_HYPERBOLIC_SCALAR_FIBRE_AXIS_DEFECT_AND_FOUR_PLUS_TWO_TRANSFER_THEOREM.md`.

## 3 August equivariant primitivity-resultant transfer

The seven-leaf descent of the P7 quotient-singular branch now admits a
second translation, this time to finite-group harmonic analysis and
homogeneous elimination.  Give the cyclic-distance classes of `K_7` weights
`a,b,c` and then allow arbitrary nonzero vertex switches `s_i`.  A four-face
of the Boolean square factors by the product of its four switches.  Dividing
each five-set primitive equation by the common five-switch product makes the
equations linear in `r_i=s_i^(-1)`.  They form a `C_7`-equivariant map

```text
K_(a,b,c):K^7 -> K^21.                               (34)
```

The three cyclic orbits in the codomain are the three distances of the
missing edge.  On the character `r_i=t^i`, `t^7=1`, (34) is therefore just
three explicit homogeneous quadrics `E_1(t),E_2(t),E_3(t)` in `a,b,c`.
Their degree-four Macaulay multiplication matrix has a fixed `15 x 15`
minor satisfying

```text
det M_*(1)=-2^5 3^9 5,
det M_*(t)=-2^13 3^2 t^3(t+1) mod Phi_7(t).          (35)
```

Thus the three quadratic multiples span every quartic for all seven
characters.  They have no common nonzero projective parameter, every
character block of (34) is injective, and no nonzero switched-circulant
seven-leaf square is primitive.  This includes all coordinate boundaries
among `a,b,c` and uses no tuple enumeration.

The reusable object suggested by this proof is an **equivariant primitivity
resultant**: after switching makes primitivity linear in reciprocal vertex
weights, decompose the resulting finite-group operator into irreducible
blocks and certify each block's projective parameter ideal by a Macaulay
minor or another exact elimination certificate.  Bamieh's circulant/DFT
viewpoint supplies the simultaneous-diagonalization language, while the
D'Andrea--Dickenstein determinant formulas supply the surrounding
Macaulay/resultant vocabulary.  The switching reduction and the block
certificates (35) are new to this problem.  See
`SEVEN_LEAF_SWITCHED_CIRCULANT_PRIMITIVE_SQUARE_NO_GO_THEOREM.md`.

This closes only a structured infinite family inside `ell_L F^2=0`.
Arbitrary asymmetric seven-leaf primitive squares and the additional radial
and apolar-annihilator equations remain open.

## 3 August target-line pentad and pinned-star transfer

The five-port factor-analysis circuit is now coefficient-level legal on the
full-sensor simple-incidence stratum.  If the legal 219-label companion map
is injective and its diagonal-target intersection is one projective line
`[w]`, a linear left inverse selects each of the 21 named coordinates

```text
y_ij=w_{ {0,1,i,j} }.                                (36)
```

Every five-blocker restriction is therefore an actual linear coefficient
window, rather than a hoped-for null-polar selector.  On the residual-edge
branch `h=a_01=0`, the pair array has hyperbolic Gram form
`a_0i a_1j+a_0j a_1i`; its 21 five-port pentads assemble into one
`S_7`-equivariant exterior covariant in `wedge^5 K^7`.  A single nonzero
component excludes the entire nonzero target line from `h=0`.  A fixed
ambient simple-incidence map with pentad `-6` proves that Schubert incidence
alone does not force this physical circuit.

On the pinned open, the residual edge is exactly

```text
h=(u_0)_1/d_0,                                      (37)
```

so `h=0` is a homogeneous degree-eight numerator.  After that gate, all 21
absolute residual-pair four-deck equations are equivalent to

```text
tau y_ij=(u_0)_i(u_1)_j+(u_0)_j(u_1)_i.             (38)
```

The cleared `2 x 2` minors have degree 17 and are necessary and sufficient
for this complete pair sector, with both-zero and one-zero cases retained.
This translates the same target line successively through Schubert
incidence, algebraic factor-analysis circuits, and rank-one Segre geometry.
Drton--Sturmfels--Sullivant supply the factor-analysis/pentad vocabulary;
the named P7 projection and its pinned-star alignment are new.  See
`P7_TARGET_LINE_H0_PAIR_PROJECTION_PENTAD_AND_STAR_ALIGNMENT_THEOREM.md`.

The existence of a legal full-rank GHZ point on the simple-incidence pinned
open is still unknown, as are the other 105 four-deck coordinates and the
higher decks.

## 3 August physical leaf-annihilator and quotient-syzygy transfer

The physical intersection inside the P7 quotient-singular radial system now
has a support-free zero-divisor formulation.  For a seven-leaf quadratic
`F`, put `N=F^2/2` and assume `ell N=0`.  Boolean Lefschetz injectivity and
`N+ell JN=0` give the exact equivalence

```text
AF=tJN  <=>  F(2ell A+tF)=0.                         (39)
```

Consequently a full-edge P6-order leaf square extends to a full-edge P7
primitive square exactly when `Ann_2(F)` contains a class projectively equal
to `[F]` modulo `ell A_1`, with a full-support incidence remainder.  Every
physical extension therefore satisfies

```text
rank(mu_2(F):A_2->A_4)<=20.                          (40)
```

At rank 20 the annihilator is one projective line and extension is one
quotient-collinearity test.  Rank at most 19 is a distinct retained
incidence, not a dimension-count conclusion.  The full-edge uniform
switching family has rank 21 and is excluded exactly, while a square-zero
coordinate-boundary family shows why torus permission is essential.

The same leaf form also controls quotient singularity.  For total-zero
`G`, with `d=partial G`, define `C_G=2AG-t dF`.  Then

```text
2t Phi_N(G)=F C_G.                                   (41)
```

Thus quotient singularity is a structured cubic syzygy in `Ann_3(F)`.
Degree-two and degree-three multiplication by `F` are complemented
transposes, so

```text
rank(D|P)<=rank mu_2(F).                             (42)
```

Leaf rank at most 19 is automatically quotient-singular.  Quotient rank at
most 18 is exactly the separate condition that at least two independent
structured cubic syzygies occur.  This translates the physical radial
problem into projective annihilator incidence and syzygy geometry; Cook's
strong-Lefschetz context and Feinsilver's Boolean `sl_2` model supply the
ambient theory, while (39), (41), and (42) are the new P7 identities.  See
`P7_PHYSICAL_LEAF_ANNIHILATOR_EXTENSION_AND_QUOTIENT_SYZYGY_THEOREM.md`.

Both the rank-20 and rank-at-most-19 physical extension tori remain unknown.
The structured-syzygy condition is no longer an additional rank-20 test, as
the Boolean transport below proves it automatic on every physical extension.

## 3 August projected-Veronese ramification transfer

The leaf multiplication rank is also the ramification rank of a classical
projective construction.  With `V=A_2(L)` and `W=A_4(L)`, Boolean
multiplication is a surjection

```text
m:Sym^2(V)->W,          dimensions 231 -> 35,         (43)
```

with 196-dimensional kernel.  Hence `F -> F^2/2` is the projection of the
quadratic Veronese `nu_2(P^20)` from the center `P(ker m)=P^195`.  Its
differential and projection-center tangent intersection are

```text
d(H_4)_F(K)=FK,
P(ker m) intersect T_(nu_2([F]))nu_2(P(V))
  =P(F symmetric Ann_2(F)).                          (44)
```

The physical annihilator `K=2ell A+tF` is therefore exactly a structured
tangent direction killed by the projection.  Every radial P7 extension is
forced into the ramification locus:

```text
rank d(H_4)_F<=20.                                   (45)
```

This yields a rigorous strategy no-go.  The generic full-Jacobian
four-hafnian tomography chart cannot locally invert the physical primitive
radial branch, because that branch is disjoint from the chart.  At rank 20
the center meets the Veronese tangent in one point; at rank at most 19 the
intersection is positive-dimensional.  Oeding--Raicu supply the surrounding
tangential Segre--Veronese geometry, while the Boolean projection and the
structured P7 tangent incidence are the new transfer.  See
`SEVEN_LEAF_HAFNIAN_PROJECTED_VERONESE_RAMIFICATION_AND_STRUCTURED_TANGENT_THEOREM.md`.

The structured ramification incidence may still meet the edge torus; the
translation rules out generic inversion, not the physical branch.

## 3 August weighted legal-companion pullback ideal

The target-line pair tests now pull all the way back to the legal companion
parameter ring without a free cofactor vector.  If

```text
B(z)=pi_Delta Gamma(z):K^219->K^240,                 (46)
```

then variable diagonal incidence is the maximal-minor ideal `I_219(B)`.
On a full-sensor rank-218 quotient chart, the signed `218 x 218` maximal
minors of a selected `218 x 219` row submatrix form the unique kernel vector
`q(z)`.  Substitution gives legal-parameter covariants of relative line
weights 5, 8, and 17 for the pentad, `h=0` gate, and star alignment.

The eliminated minors are shadows of one stronger weighted ideal.  Give an
invertible amplitude `tau` relative weight 15 and localize at the sensor,
line, and two pinned determinants.  Then

```text
J_pair=<eta(q),
        tau q_{01ij}-khat_ij(q):2<=i<j<=8>.          (47)
```

This Laurent ideal is necessary and sufficient for the complete 21-entry
`h=0` residual-pair four-deck sector.  Under a chart change `q'=s q`, it
glues by

```text
tau'=s^15 tau.                                       (48)
```

All five-port pentads and degree-17 alignment minors belong to `J_pair`.
The Laurent amplitude is essential: ordinary rank-one minors would retain
the forbidden case `q_pair!=0`, `khat=0`, `tau=0`.

There is also a sharp non-forcing boundary.  Exact ambient simple-incidence
decks give

```text
d_0=d_1=32805,   eta=0,   pentad=-6,
one alignment minor=-2152336050.                     (49)
```

Thus even pinned-open gated Schubert incidence does not force the physical
pair ideal.  The remaining question is genuinely in the legal symmetric
companion image: whether the localized ideal (47) is the unit ideal there.
See
`LEGAL_COMPANION_SIMPLE_INCIDENCE_WEIGHTED_PULLBACK_IDEAL_AND_NONFORCING_THEOREM.md`.

This is an exact determinant/exterior-power and weighted-line-bundle
translation, not an expansion or enumeration of the enormous maximal-minor
ideal.

## 3 August legal secant--factor codimension barrier

The legal localized ideal cannot be decided by the factor-analysis layer
alone.  Let `Gamma:U->(K^3)^(tensor 5)` be any injective legal 219-label
companion map.  The third secant of the five-qutrit Segre has projective
dimension 32, so the projective dimension theorem gives

```text
dim(P(im Gamma) intersect sigma_3(Segre))
 >=218+32-242=8.                                      (49a)
```

This is a mandatory border-rank-three preimage inside every actual legal
full sensor; no arbitrary ambient incidence map replaces `Gamma`.

The seven-port two-factor-analysis arrays

```text
y_ij=a_i b_j+b_i a_j
```

form an irreducible affine cone of dimension 13.  A fixed rank-13 Jacobian
certificate proves the dimension exactly.  Since the named 21-coordinate
pair projection from `U` is surjective, the projective inverse image of this
factor locus has dimension 210 and codimension eight in `P(U)=P^218`.
Therefore

```text
mandatory border preimage intersect complete factor locus != empty. (49b)
```

The whole factor-analysis ideal—not just a selected pentad—is consequently
proper on the mandatory legal border family.  More generally, any at-most-
eight homogeneous scalar components from the gate/pentad/alignment hierarchy
still have a common border-rank-three zero.

This does not construct a legal GHZ point.  The forced intersection can lie
in the nonconcise secant boundary, the zero pair-coordinate base locus, or a
pinned/root-torus boundary.  On a proper zero-dimensional good chart, let
`A_Gamma` be the finite coordinate algebra.  Then the gate is a unit exactly
when its multiplication determinant is nonzero, and the complete surviving
pair sector is the finite Laurent quotient

```text
A_Gamma[tau,tau^(-1)]/
 <eta, tau y_ij-khat_ij>.                              (49c)
```

Thus the next legal calculation is finite Artinian linear algebra after a
mandatory intersection is formed, not unrestricted elimination over 219
cofactor coordinates.  Torus-concise simple incidence and nonvanishing of
(49c) remain unknown.  See
`LEGAL_P7_SECANT_FACTOR_CODIMENSION_BARRIER_AND_ARTINIAN_PAIR_IDEAL_REDUCTION.md`.

## 3 August committed-sensor ordered Chow/norm criterion

The preceding finite reduction can be made exact for the committed sensor
without adding 219 preimage variables.  Let `B` be its already certified
first-219-row square block, `beta=det B`, and

```text
v(z)=adj(B)z_R,
rho_s(z)=beta z_s-Gamma_s v(z)                    (s outside R). (49d)
```

There are exactly 24 residuals, and all vanish if and only if `z` belongs to
the legal sensor image.  On an actual image point, `v=beta q`, so the named
pair coordinates are recovered up to one harmless common scalar.

Parameterize honest ordered rank-three tensors by the 32-dimensional
projective bundle over three copies of `Segre((P^2)^5)`.  On the open where
the three factors form a basis at each root and all mixture coefficients are
nonzero, Kruskal's inequality `3+3+3>=8` gives exactly six ordered lifts of
each tensor.  Pulling (49d) and the exact `I_(7,2)` factor ideal to this
space yields

```text
32 - 24 - 8 = 0                                      (49e)
```

as the proper expected dimension.  The factor ideal has 35 cubics and 21
pentads, codimension eight, and degree 259.

The good union can be selected without enumerating 221-minors or 21 pair
charts.  Contract the bivector of two 24-residual columns and the 21-vector
of named pairs against algebraically independent selectors.  Their product
with the torus-concise and pinned factors is one universal separator
`G_gen`.  After adjoining `w G_gen-1` and one generic projective
dehomogenizer, the finite algebra `A_good` satisfies

```text
A_good=0  iff the committed intersection misses the good union,
A_good!=0 iff it has a torus-concise, root-torus, simple,
             pair-nonzero, pinned survivor.           (49f)
```

Inside any finite quotient, multiplication by a boundary product is
nilpotent exactly when all support is boundary-trapped, nonnilpotent exactly
when some support survives, and invertible exactly when every support point
survives.  The characteristic polynomial of that one multiplication matrix
records all three cases.  The final legal `h=0` sector is the finite Laurent
quotient obtained by adjoining `eta=0` and the 21 star-alignment equations.

This is a decision package, not the decision itself.  The committed 24
coefficient polynomials and localized quotient have not yet been
materialized.  If the good localization is empty, the surviving border
fibres fall under the four border-rank-three normal-form mechanisms of
Buczyński--Landsberg; if it is nonempty, that classification is bypassed.
Rhodes supplies the Kruskal uniqueness theorem, Drton--Sturmfels--Sullivant
the factor ideal, and Qi the independent downstairs third-secant equations.
See
`COMMITTED_LEGAL_SENSOR_ORDERED_SECANT_FACTOR_CHOW_NORM_AND_BOUNDARY_TRAP_CRITERION.md`.

## 3 August apolar-Gorenstein Hilbert and resonance transfer

Full edge support rigidifies the leaf-annihilator branch before any physical
incidence is imposed.  If `F` has all 21 coefficients nonzero, the triple
equations for a linear annihilator reduce, according to its zero support, to
either the full-rank `W_(2,3)(7)` inclusion map or the full-rank unsigned
vertex-edge incidence of `K_6`.  Hence

```text
Ann_1(F)=0.                                           (50)
```

The quotient by the complete multiplication annihilator has the perfect
top pairing induced by `XF`, so it is Artinian Gorenstein of socle degree
five.  With `rho=rank mu_2(F)`, its exact Hilbert vector is

```text
H_(A/Ann(F))=(1,7,rho,rho,7,1).                      (51)
```

Let `E_3=Ann_3(F)/(A_1 Ann_2(F))`.  Pure dimension comparison gives

```text
dim E_3>=max(0,6rho-112).                            (52)
```

Thus rank 20 has one quadratic annihilator and at least eight essential
cubics; if that annihilator is full-edge, the number is exactly eight.
Rank 19 has two quadratic annihilators and at least two essential cubics.
For rank at most 18, the Hilbert lower bound is zero and the multiplication

```text
A_1 tensor Ann_2(F)->Ann_3(F)                        (53)
```

is a separate resonance problem.

The structured physical cubic `C_G=2AG-t(partial G)F` has the exhaustive
trichotomy

```text
C_G=0;  C_G in A_1 Ann_2(F) minus {0};
[C_G]!=0 in E_3.                                     (54)
```

The Hilbert vector and the essential-cubic counts force none of these three
placements.  They explain why the rank-20 structured map is square and why
rank 19 is automatically singular, but they do not settle the physical
incidence.  Macaulay inverse systems, Boolean `sl_2`, and mixed-Hessian
determinantal geometry supply the surrounding theories; the full-edge
injectivity and branch counts are the new transfer.  See
`P7_LEAF_APOLAR_GORENSTEIN_HILBERT_RESONANCE_AND_ESSENTIAL_SYZYGY_THEOREM.md`.

## 3 August Boolean-Lefschetz structured-cubic closure

The physical extension equations force more than the Hilbert vector alone.
On the total-zero hyperplane `G_0` of seven-leaf quadratics, put

```text
T=I+ell partial.
```

The Boolean `sl_2` decomposition is

```text
G_0=ker(partial:A_2->A_1) direct-sum ell P_1,
spec(T)=1^14,6^6,                 T^(-1)=I-ell partial/6.       (55)
```

Let `K=2ell A+tF` be the nonzero physical quadratic annihilator,
`Omega=ell^2/2`, and `s=sigma(K)`.  The two quadratics `K,Omega` are
independent, and

```text
H=s Omega-21K,                  G=T^(-1)H                       (56)
```

are nonzero with `G` total-zero.  The identities `FK=0` and `ell F^2=0`
give both `AK` and `AOmega` in `Ann_3(F)`.  Therefore

```text
C_G=2AG-t(partial G)F
   =2AH-(partial G)K in Ann_3(F).                                (57)
```

This is an explicit nonzero structured kernel direction, so every physical
P7 leaf extension is quotient singular, including rank 20.  The sharper
class formula is

```text
[C_G]=-(t sigma(K)/2)[ell F]
       in Ann_3(F)/(A_1 Ann_2(F)).                               (58)
```

Thus `sigma(K)=0` makes the canonical cubic quadratically generated, while
otherwise its essential placement is governed by the single class
`[ell F]`.  On rank 20, `[Omega]` is nonzero in the apolar degree-two
quotient and `[A][Omega]=0`; equivalently the middle multiplication map and
the second higher Hessian of the Macaulay dual quintic vanish at `A`.

This closes the former structured determinant but not the extension
incidence.  No full-edge `F,A,t` satisfying the physical extension equations
is constructed or excluded.  Boolean `sl_2` and mixed-Hessian theory supply
the neighboring language; the covariants (56)--(58) are the new direct
transfer.  See
`P7_STRUCTURED_CUBIC_BOOLEAN_LEFSCHETZ_TRANSPORT_AND_MIDDLE_HESSIAN_VANISHING_THEOREM.md`.

## 3 August mixed-Hodge physical-star obstruction

The same physical equations have a second contraction which depends only on
the radial star.  Multiplying `FK=0`, with `K=2ell A+tF`, by `ell` and using
`ell F^2=0` gives

```text
(ell^2 A)F=0.                                         (59)
```

Thus multiplication by `ell^2 A:A_2->A_5` must be singular and must kill a
full-edge quadratic.  After complementing the five-set rows to edges, its
matrix is the weighted Kneser pencil

```text
M_A(e,g)=2 sum_(v outside e union g)a_v  if e cap g=empty,
           0                              otherwise.  (60)
```

Equivalently, if `C` is the adjacency of `KG(7,2)`, `S=sum a_i`, and
`W_(e,e)=sum_(i in e)a_i`, then `M_A=2(SC-WC-CW)`.

Over the reals, identify the Boolean algebra with the cohomology ring of
`(P^1)^7`.  If all coefficients of `A` have one sign, then `ell,ell,+/-A`
are Kähler classes.  The mixed Hard Lefschetz theorem makes (59)'s map an
isomorphism, a contradiction.  Its signature throughout the positive
chamber is `(15,6)`, computed at `A=ell` from the Kneser spectrum.  This is
the first chamber-wide exclusion of the physical extension incidence.

There is also a field-independent orbit exclusion.  Up to a leaf
permutation, put `A=(p,q,q,q,q,q,q)` with `pq!=0`.  Splitting the edge space
into six exceptional-star and fifteen internal edges gives

```text
M_A=[ 0       6q C_6            ],
    [ 6q C_6^T 2(p+2q)D_6      ],                 (61)

det M_A=(2(p+2q))^9(-144q^2)^5(-1440q^2).
```

Here `C_6 C_6^T=4I+6J` and `D_6=KG(6,2)` has spectrum
`6^1,(-3)^5,1^9`.  If `p+2q!=0`, the map is invertible.  On the sole wall
`p=-2q`, its kernel is the nine-dimensional internal harmonic module
`{(0,y):C_6y=0}` and therefore has all six exceptional-star coordinates
zero.  Neither case permits the full-edge `F` required by (59).

Dinh and Nguyen prove the mixed Hodge--Riemann and mixed Hard Lefschetz
theorems used for the real chamber in
[*The mixed Hodge--Riemann bilinear relations for compact Kähler
manifolds*](https://arxiv.org/abs/math/0501449).  Equations (59)--(61), the
weighted-Kneser transfer, and the characteristic-zero exceptional-orbit
closure are proved directly here.  General mixed-sign stars remain unknown.
See
`P7_PHYSICAL_EXTENSION_MIXED_HARD_LEFSCHETZ_SIGN_CHAMBER_AND_ONE_EXCEPTIONAL_ORBIT_OBSTRUCTION.md`.

## 3 August Boolean-down descent of the physical mixed kernel

The weighted-Kneser system (59)--(60) has a second, exact model.  Put
`alpha=sum_i a_i`, `r_i=sum_(j!=i)f_ij`, and
`delta_ij=alpha-2(a_i+a_j)`.  Boolean `sl_2` gives

```text
ker(ell^2:Z_3->Z_5)=ker(D:Z_3->Z_2),                 (62)
```

both equal to the 14-dimensional primitive space.  Applying the corrected
zeon Leibniz rule to `AF` turns the physical mixed equation into the exact
local system

```text
delta_ij f_ij+a_i r_j+a_j r_i=0.                    (63)
```

If `L_A` is the edge matrix in (63), `R` is unsigned vertex--edge incidence,
and `M_A` is (60), then the universal intertwiner

```text
M_A=J L_A,
J=2I+(2/3)11^T-R^T R,
spec(J)=4^1,(-3)^6,2^14.                            (64)
```

In particular `det M_A=2^16 3^6 det L_A`; the former 21-dimensional
determinant loses no information under this descent.  On the chart
`a_i delta_ij!=0`, the determinant lemma reduces it to the symmetric
seven-by-seven Hessian of

```text
E_A(x)=1/2 sum_i a_i x_i^2
       +1/2 sum_(i<j) a_i a_j (x_i+x_j)^2/delta_ij. (65)
```

Every mixed-kernel vector is reconstructed uniquely by

```text
r_i=a_i x_i,
f_ij=-a_i a_j(x_i+x_j)/delta_ij.                    (66)
```

Thus full edge support is exactly `x_i+x_j!=0` for all pairs.  The 21
exceptional hyperplanes `delta_ij=0` remain separate exact branches; they
include the six-equal-coordinate wall above.  This is a genuine dimensional
compression, not a search: the generic master-Hessian incidence, exceptional
branches, primitivity, and the stronger nonlinear annihilator equation all
remain unknown.  Feinsilver's zeon/Boolean `sl_2` model supplies the ambient
language in [*Zeon algebra, Fock space, and Markov
chains*](https://arxiv.org/abs/1102.0368); (62)--(66) are the direct new
transfer.  See
`P7_PHYSICAL_MIXED_KERNEL_BOOLEAN_DOWN_DESCENT_AND_SEVEN_BY_SEVEN_MASTER_HESSIAN.md`.

## 3 August complete two-level physical-star exclusion

The master system permits a representation-theoretic closure of every star
with at most two nonzero coordinate values.  Put `p` on `m` leaves and `q`
on `7-m` leaves.  The edge module under `S_m x S_(7-m)` splits into trivial,
standard, tensor-standard, and harmonic two-subset summands, and the local
matrix (63) preserves every summand.

For multiplicities `2+5`, the exact determinant is

```text
det M_A=5*2^30*3^12 q^8 (2p+q)^5
        (p^2+2pq+3q^2)^4.                            (67)
```

The linear wall is the `BB` harmonic module; the quadratic wall is the
`B`-standard module.  Both omit the unique `AA` edge, so neither can contain
a full-edge mixed kernel.

For multiplicities `3+4`,

```text
det M_A=2^30*3^12 p^2 q^4 (p+2q)^6
        (3p^2+2pq+q^2)^3
        (p^3+2p^2q+3pq^2+4q^3).                     (68)
```

The tensor and standard walls again miss an edge orbit.  The last cubic is
different: after `q=1` and

```text
c(t)=t^3+2t^2+3t+4,                                 (69)
```

its one-dimensional block-constant kernel has full-edge values

```text
f_AA=8t^2,
f_AB=-t(3t+4),
f_BB=-2(t^2+2t+8)/t.                                (70)
```

This proves that the generic master-Hessian good-kernel incidence is not
empty: the cubic has a unique real root in `(-2,-3/2)`, away from every
denominator divisor.  Signature or mixed-kernel singularity alone therefore
cannot finish P7.

Primitivity does finish this orbit.  One coefficient of `ell F^2` becomes

```text
24(t^2+2t+8)(6t^3+9t^2+2t+8)/t^2,                  (71)
```

and the two exact resultants with `c` are

```text
256 and 1280.                                        (72)
```

Thus (71) is nonzero at every complex cubic root in characteristic zero.
Together with the earlier `1+6` exclusion, all nonzero one- and two-level
stars are excluded.  Stars with at least three values remain open.  The
mixed-Hessian viewpoint is adjacent to Gondim and Zappalà's Lefschetz
criterion in [*On mixed Hessians and the Lefschetz
properties*](https://arxiv.org/abs/1803.09664); the orbit factors and
primitive resultant are the direct new transfer.  See
`P7_PHYSICAL_EXTENSION_TWO_LEVEL_STAR_ORBIT_COMPLETE_EXCLUSION_THEOREM.md`.

## 3 August exceptional wall-graph Hessian

The denominator divisors in (65)--(66) now have an exact, denominator-free
descent.  Let `W={ij:delta_ij=0}`, `x_i=r_i/a_i`, and let `R_W` be unsigned
incidence of the wall graph.  Deleting wall edges from the master energy gives
a partial symmetric Hessian `B_W`.  Exceptional mixed kernels are exactly

```text
R_W^T x=0,
B_W x=R_W y,                                         (73)

f_ij=-a_i a_j(x_i+x_j)/delta_ij  off W,
f_ij=y_ij                         on W.              (74)
```

Equivalently, `x` lies in the radical of `B_W` restricted to
`ker R_W^T`.  This gives a six-by-six exact test for one wall and contracts
every multiple-wall stratum to the number of alternating wall components.

Writing `c=alpha/2`, wall adjacency is `a_i+a_j=c`.  The involution
`p -> c-p` therefore forces `W` to be a disjoint union of complete bipartites
between complementary value classes, plus at most one clique on the midpoint
class `a_i=alpha/4`.  A bipartite component contributes one alternating
parameter; a midpoint clique of size at least three forces all its `x`
coordinates to zero.

Let the midpoint value be `h=alpha/4!=0`.  The restricted equations exclude
`K_7` by coefficient sum, `K_6` by the scalar `-4h`, and `K_5` by

```text
det B_restricted
 =15 b h^2(b+h)/((b-h)(b+2h)) !=0.                  (75)
```

For a midpoint `K_4`, the outside values satisfy `b+c+d=0`.  With no outside
wall, singularity is possible only on

```text
3bcd+2h(bc+bd+cd)+12h^3=0.                           (76)
```

That cubic is retained.  With one outside wall, the two-dimensional
restricted determinant is

```text
-96h^4/((b-4h)(b+2h)),                               (77)
```

and its boundary `K_(1,2)` has coefficient `-4h`; both are excluded.  Thus a
midpoint `K_4` plus any outside wall is impossible.  The good-kernel locus on
(76), midpoint `K_3`, and general bipartite wall systems remain unknown.
Monfared and Mallik's [signless-Laplacian matrix-tree
analogue](https://arxiv.org/abs/1805.04759) supplies the neighboring
incidence language; (73)--(77) are the new physical transfer.  See
`P7_PHYSICAL_MIXED_KERNEL_EXCEPTIONAL_WALL_GRAPH_AND_RESTRICTED_HESSIAN_THEOREM.md`.

## Ranked proof program

0. **Resolve the legal pullback of target incidence.**  The ambient equation
   is now the rank-at-most-two `24 x 3` cokernel covariant, and its generic
   cofactor line has complete determinant-cleared graph-side tests.  Prove
   that the mandatory at-least-eight-dimensional border-GHZ intersection
   escapes the nonconcise/collision boundary, or that every legal line makes
   one scale-free degree-nine/four-deck stress nonzero, or prove that every
   component descends to a classified coordinate or hyperbolic-Gram
   boundary.  The 30-word single-flip rank test, rank-222 chart, endpoint
   torus, and double star are the mandatory tangent, open, gauge, and singular
   controls.
1. **Force two transverse nonprojective fans on one window.**  One fully
   polarized root pair has observation rank at most four on the six pair
   faces, and this defect is generically exactly two.  Two compatible pairs
   are algebraically sufficient exactly when their fan kernels are
   transverse.  Prove their legal co-occurrence with common nonzero shores
   and separate the root--root/residual companion columns, or prove that the
   target forces a different labeled sensor.  The projective page remains
   identically zero and cannot supply either fan.
2. **Physical circuits for `P4`, `K1,3`, and `K3`.**  The common full-terminal
   quotient has rank sum at most six.  Both `3K2` and `P3 disjoint-union K2`
   are excluded, while exact quotient-core controls preserve the other three
   overlap types.  Use the unprojected residual permanents jointly across
   faces; another quotient-only four- or six-hafnian shadow cannot suffice.
3. **Cross the root-budget staircase.**  Every currently legal principal
   depth lies in `|S|+|T|>=2q`, while response inversion and cumulants require
   lower subset faces.  Exact all-depth fibers show that postprocessing the
   entire eligible tower cannot recover them.  Force a genuinely mixed GHZ
   coefficient, herald/vacuum simulator, or synchronized direct-pair sector
   below the staircase.
4. **Classify the surviving pinned circuits.**  On the `P_7` edge torus,
   every singular dependency has full support eight.  Classify this primitive
   middle-degree Boolean-square branch and intersect it with the degree-nine
   line tests.  For `P_6`, any
   claimed torus exclusion must separately eliminate the exact
   primitive-cube-root two-column escape.
5. **Physical-idempotent separator.**  Find a polynomial/covariant that
   vanishes for vertexwise local-colour block graphs but distinguishes the
   formal global-idempotent realization.  It must use the uncontracted
   degree-five tuple, joint degrees, or degree seven: the binary contraction
   itself is a physical image point, while scalar degrees one and three are
   dominant.
6. **Phase-decorated `B_3` exchange complex.**  Define the missing incidence
   alignment between the conformal cycle/theta matching and the
   at-most-eight pure backbones, then glue the exact additive and cubic toric
   equations.  A single coefficient cannot exclude simultaneous bypasses.
7. **Force a line-integrability stress.**  The target-incidence line now has
   explicit degree-nine partner residuals and absolute four-deck equations.
   Mod out the endpoint torus first: magnitudes preserve every projective
   stress and move only the total affine character.  Use the directional
   matching data to force one residual nonzero, rather than searching over
   219 free cofactor variables.
8. **Coloured deletion-cumulant compatibility.**  Use two overlapping root
   windows to turn quotient minors into a global log-quadratic obstruction.
9. **Conditional Pfaffian chart.**  Apply matchgate identities only if a
   support-specific orientation is forced.
10. **GIT/tropical degeneration.**  Seek a one-parameter initial form that
   preserves the exact diagonal restriction; do not substitute asymptotic or
   border statements.

## Current status wall

```text
new arbitrary-surplus deck hierarchy: r>=2 finite, r>=3 rational;
new r=1 smooth nonidentifiability: dimensions 27 and 65 in P5/P7 cells;
new full P7 shallow sensor:       rank 219 on a legal integer chart;
new diagonal target separation:  augmented rank 222, incidence locus proper;
new P7 target-incidence quotient: 24x3 rank <=2, ambient codimension 22;
generic P7 incidence cofactor set: one sensor-dependent projective line;
line hafnian integrability test:   degree-nine stresses plus affine scale;
mandatory P7 border-GHZ family:   projective dimension at least eight;
torus-concise point in that family: UNKNOWN;
three-term local-basis tangent test: rank 22 on 30 single flips;
endpoint torus projective stresses: SEMI-INVARIANT;
endpoint torus affine amplitude:   total-product character;
physical points on Hessian-open jet line: AT MOST ONE NONZERO POINT;
ambient GHZ/physical Hessian-open line: CONSTRUCTED, NONLEGAL;
fixed legal sensor at all-one deck: BORDER RANK AT LEAST NINE;
new full P6 top-deck sensor:      rank 70 in 81 channels;
new P6 target separation:        augmented rank 73, ambient codimension nine;
new compressed P5 tomography:    Jacobian rank 21 in 27 channels;
new P5 inverse-target incidence: ambient codimension at least four;
P7 torus pinned circuit support: exactly eight if singular;
P7 full-support-eight branch:    UNKNOWN;
primitive Boolean middle space:  dimension 14;
primitive square meets edge torus: UNKNOWN;
primitive five-set equations:     EXACT DUAL TRIANGLE SYSTEM;
torus row sums all zero:          IMPOSSIBLE;
primitive star-closure pencil:     28x28, DEGREE-21 DISCRIMINANT;
primitive generic star fibre:      EMPTY ON EDGE TORUS;
primitive remaining leaf interface: 35 EXACT QUADRICS;
primitive leaf interface translation: u wedge v=0, UNIQUE NONZERO SCALE;
primitive corank-one cleared equations: DEGREE 67;
primitive deeper Schur-pencil branch: RANK AT MOST 19, UNKNOWN;
primitive exceptional divisors:   EXACT COMPLEMENTARY-SUM GRAPH;
primitive vanishing row sums:      AT MOST THREE;
primitive zeon harmonic-square law: EXACT CORRECTED LEIBNIZ IDENTITY;
primitive off-diagonal Riccati law: EXACT;
primitive row-sum quadratic Casimir: EXACT;
real reverse row-sum cones:         EMPTY ON EDGE TORUS;
constant real row-sum branch:       IMPOSSIBLE;
complex consequence of real cone:   NONE CLAIMED;
primitive a=R/4 value class:       SIZE AT MOST FOUR;
primitive size-four exceptional class: EXPLICIT CUBIC;
primitive full-Hessian kernel:     CONTAINS 8D VERTEX-INCIDENCE SPACE;
primitive quotient Hessian:        DIMENSION 20;
primitive quotient-open linear fibre: ADDITIVE 8-GAUGE;
primitive additive chord support:   AT MOST FOUR;
primitive nonzero gauge complement: FORCED INDEPENDENT SET;
primitive edge-torus additive gauge: RIGID, NO NONTRIVIAL CHORD;
primitive P7 gauge feasibility:     EXACT 56-COORDINATE QUADRATIC SYSTEM;
primitive quotient-open torus deck: AT MOST ONE REALIZATION;
ambient primitive Hessian rank 20: EXACT SHARPNESS CONTROL, NONPHYSICAL;
primitive full kernel:             DEGREE-TWO APOLAR ANNIHILATOR;
primitive quotient-singular chart: 20x20 BILINEAR RADIAL MAP;
primitive singular determinant:    NONZERO DEGREE 20 ON 14-SPACE;
primitive rank-19 annihilator:      UNIQUE PROJECTIVELY;
primitive rank<=18 annihilator:     RETAINED;
physical singular radial lift:      QUADRATIC/BILINEAR SYSTEM;
physical singular lift meets edge torus: UNKNOWN;
physical radial extension equation: QUADRATIC ANNIHILATOR INCIDENCE;
physical leaf multiplication rank:  AT MOST 20;
physical leaf rank-20 branch:        ONE ANNIHILATOR LINE;
physical leaf rank<=19 branch:       RETAINED, UNKNOWN;
quotient singularity on physical lift: STRUCTURED CUBIC SYZYGY;
quotient rank versus leaf rank:      rank(D|P)<=rank(mu_2(F));
every physical leaf extension is quotient singular: PROVED;
canonical structured kernel direction: NONZERO, EXPLICIT;
rank-20 structured determinant on physical incidence: ZERO;
canonical essential class: -(t sigma(K)/2)[ell F];
rank-20 middle second Hessian at A: ZERO;
physical star mixed-Lefschetz kernel: (ell^2 A)F=0;
weighted Kneser star pencil:          EXACT 21x21 FORMULA;
real same-sign physical stars:        EXCLUDED BY MIXED HARD LEFSCHETZ;
same-sign pencil signature:           (15,6);
six-equal-coordinate star orbit:      EXCLUDED IN CHARACTERISTIC ZERO;
six-equal determinant wall p=-2q:     9D KERNEL, ALL STAR EDGES ZERO;
physical mixed Boolean-down system:   21 EXACT LOCAL EDGE EQUATIONS;
weighted Kneser/local intertwiner J:  FIXED, INVERTIBLE;
determinant ratio det(M_A)/det(L_A):   2^16 3^6;
generic physical mixed master system: SYMMETRIC 7x7 HESSIAN;
generic mixed-kernel reconstruction:  EXACT BIJECTION;
generic full-edge mixed condition:    x_i+x_j NONZERO FOR ALL PAIRS;
generic master-Hessian good kernel:    EXISTS ON EXACT 3+4 CUBIC;
nonzero 2+5 physical stars:            EXCLUDED;
3+4 nontrivial mixed-kernel walls:     MISS AN EDGE ORBIT;
3+4 block-constant cubic mixed kernel: FULL EDGE, EXACT;
3+4 cubic primitive obstruction:       NONZERO BY RESULTANTS 256,1280;
nonzero stars with <=2 values:          EXCLUDED;
stars with >=3 values:                  UNKNOWN;
mixed exceptional delta reconstruction: EXACT RESTRICTED HESSIAN;
mixed wall graph:                       COMPLEMENTARY BIPARTITES + MIDPOINT;
midpoint wall K5,K6,K7:                 EXCLUDED;
midpoint wall K4 plus outside wall:      EXCLUDED;
bare midpoint K4 wall:                  ONE CUBIC, UNKNOWN GOOD KERNEL;
midpoint K3 and bipartite wall systems: UNKNOWN;
general mixed-sign physical star:     UNKNOWN;
quotient rank<=18 structured syzygies: AT LEAST TWO;
leaf four-hafnian map:                PROJECTED VERONESE;
Boolean multiplication projection center: P^195;
leaf four-hafnian ramification kernel: Ann_2(F);
physical radial branch on full-Jacobian open: IMPOSSIBLE;
physical rank-20 tangent-center point: UNIQUE PROJECTIVELY;
physical rank<=19 tangent-center intersection: POSITIVE-DIMENSIONAL;
full-edge leaf linear annihilator:    IMPOSSIBLE;
leaf annihilator quotient Hilbert vector: (1,7,rho,rho,7,1);
rank-20 essential cubic annihilators: AT LEAST EIGHT;
rank-19 essential cubic annihilators: AT LEAST TWO;
rank<=18 Hilbert essential-cubic forcing: NONE;
structured physical cubic placement: ZERO / GENERATED / ESSENTIAL;
Hilbert data decides structured placement: NO;
seven-leaf switched-circulant primitive square: IMPOSSIBLE;
arbitrary nonzero vertex switching in that family: INCLUDED;
general seven-leaf primitive square: UNKNOWN;
reciprocal-rank-one torus branch: IMPOSSIBLE;
P6 torus pinned rank drop:       exact cubic-resonance control;
new singular shallow-deck fibre: exact double-star dimension two;
new arbitrary-order exclusion:    all 3m+2 equality faces impossible;
new arbitrary-order theorem:      support >=3m+3 and S_3 port normal form;
new exact local invariant:        additive/toric B_3 phase variety;
new boundary support theorem:     all sectors descend to L=B D^* C links;
new weighted boundary object:     all-sector zeon jet J_W;
new aligned-port theorem:         aligned one-chord 2+1+0 fully excluded;
new residual rank boundary:       h=0 still permits rank C(A)=q;
new residual locality tool:       separator cross-rank <=2^(s-1);
new residual gluing invariant:    rank[F_2|F_4|F_6|...]<=q on disjoint charts;
new forced P7 chart:              marked shore with double-only four-window;
new exact information boundary:  top window face does not determine lower cube;
new P7 root-budget law:           z needs |S|>=q, direct m needs |S|>=2q;
all-depth root-budget domain:     upper staircase |S|+|T|>=2q;
eligible all-depth response map: exact affine fibers hide lower faces;
compound-open response tower:    complete nested-cofactor tomography;
compound integrability test:     determinant-cleared nested stresses;
shallow Hessian inverse:          A=(m-1)D^-1 c on a full-torus open;
all-one Hessian determinant:      exact Kneser spectrum, arbitrary order;
joint (h,c,D) integrability:      determinant-cleared iff on det D!=0;
cofactor-only torus obstruction:  IMPOSSIBLE BY DOMINANCE;
P7 one-shore Hessian recovery:    all 36 nonroot edges, RATIONAL;
P7 nine-shore affine descent:     EXACT ON COMMON HESSIAN OPEN;
GHZ meets P7 sensor/Hessian open: UNKNOWN;
Euler-Hessian response connection: EXACT ARBITRARY ORDER;
h!=0 value/first-jet unmixing:     UNIQUE;
h=0 value/first-jet fibre:         EXACT VECTOR-SPACE GAUGE;
first/second response-jet unmixing: UNIQUE ON det D!=0;
singular response-jet equation:    adj(D)g=0;
first response jet = principal two-deletion deck: PROVED;
second response jet = principal four-deletion deck: PROVED;
top present-vertex tensor determines pair deck: NO, EXACT AFFINE FIBRE;
odd-root P5/P7 deck exposure by root words: IMPOSSIBLE BY PARITY;
clean four-root P6 pair-deck tomography: EXACT 2x3 FAN, CONDITIONAL LEGALITY;
clean P6 target equation:              THREE PULLED-BACK SEGRE QUADRICS PER COLOUR;
clean P6 Segre pullback:               CODIMENSION TWO, DEGREE THREE;
every invertible P6 fan:               SEGRE PULLBACK MEETS COORDINATE TORUS;
all-nonzero permanental P6 fan:        det=-2 VANDERMONDE^2 sum(t);
GHZ alone forces shore/fan/face zero:  FALSE;
physical synchronized P6 deck lift:   UNKNOWN;
P6 physical scalar six-face morphism: SPLIT SURJECTIVE ONTO K^6;
P6 induced complete H4 deck:          70 CLOSED-FORM LABELS;
P6 face/H4 partner stresses:          36 IDENTITIES SATISFIED;
P6 scalar torus faces meet every Segre fan: PROVED;
three pure-colour sections in one block graph: CONSTRUCTED;
that block graph target-clean:         FALSE, MIXED WORD=-10/3;
canonical P6 axis operator:             RANK 51, NULLITY 5;
canonical P6 port off-diagonals:        FORCED ZERO;
canonical P6 forced 4+2 coefficient:    NONZERO;
canonical P6 off-diagonal completion:   IMPOSSIBLE;
canonical P6 GHZ-stabilizer orbit:       EXCLUDED;
arbitrary-fibre P6 axis port defect:     delta=44-rank(M)+rank(M_C);
tau=0 P6 boundary axis data:             ranks (19,7), nullity 37, delta 32;
tau=0 directed core-window axes:         32 FREE DIRECTIONS;
canonical forced 3b_pq fibre-invariant:  FALSE;
tau=0 all 5+1 coefficients:              ZERO;
tau=0 window-pair-minority 4+2 layer:    ZERO BY GRAM CONGRUENCE;
tau=0 mixed core/window 4+2 residual:    Y_(i,q)(DX)_(i,p);
nonsingular Gram route completes 4+2:    IMPOSSIBLE;
singular Gram route completes 4+2:       IMPOSSIBLE;
tau=0 full axis-kernel completion:       IMPOSSIBLE, CORE CIRCULATIONS INCLUDED;
explicit three-parameter tau-section family: EXCLUDED;
non-tau two-shore P6 scalar fibre:       EXACT RATIONAL REALIZATION;
two-shore P6 axis data:                  ranks (30,2), nullity 26, delta 16;
two-shore window/inactive/one-active 4+2 families: CANCELLED;
two-shore opposite active-row residual: NONZERO FACE VALUE;
tau tetrad/obstruction location fibre-invariant: FALSE;
other P6 scalar six-face fibres:         UNKNOWN;
P6 full two-/three-colour cancellation:  UNKNOWN;
four-residual even response tower:     COMPLETE IFF CRITERION;
four common pair rows P_ij=L_iL_j:     NECESSARY AND SUFFICIENT WITH TOP LAW;
even complementary products:          THREE EQUAL DIVISION-FREE PRODUCTS;
even full-response Wick law:           EXACT DIVISION-FREE IDENTITY;
odd residual depths needed at q=4:     NO;
quartic shell implies common rows:     FALSE BY FIVE-PORT PENTAD;
clean P6 optional-blocker convolution: UNKNOWN;
legal exposure of required synchronized decks: UNKNOWN;
maximal q2 visible response map:  DOMINANT, exact Jacobian minor 360;
conditional four-point selector: complementary z weights must be additive;
q4 four-point law:                quartic permanent defect can equal one;
new cofactor-rank no-go:          rho>=2 pair need not meet a nonzero shore;
new projection no-go:             all six top windows have dense visible image;
three marked-star windows:        target pair recovery <=5, SHARP;
four-window tetrahedral fan:      all six target pairs recovered, EXACT;
all graph-side fan windows:       FORCED BY FIXED-COMPLEMENT LAPLACE;
rho>=2 shore in rational model:   ZERO FOR EVERY WINDOW;
distinguished companion rank:     TWO AT EVERY ROOT PAIR IN SPLICE;
legal marked-star fan exposure:   UNKNOWN;
formal shore/edge depth0->5 arrow: EXACT COMMON NORMALIZATION;
physical two-root marked weights: SIX PERMANENTAL 2x2 MINORS;
fully polarized root-pair fan:    RANK AT MOST FOUR, GENERIC DEFECT TWO;
two transverse root-pair fans:    ALGEBRAICALLY RECOVER ALL SIX FACES;
legal transverse-fan cooccurrence: UNKNOWN;
projective-page marked differential: IDENTICALLY ZERO;
canonical fan target words:       GHZ-NULL;
all-tag top selectors, conditional: ALL 15 m4=z4=0, THEN m6=z6=0;
root-jet ideal on pair faces:      ZERO FORMAL ELIMINATION IDEAL;
vacuum-free dual-Wick defect:     EXACT;
canonical moment denominator:     NOT FORCED, FREE-h RESPONSE EXISTS;
both blocker singleton rows alone: STILL FREE h WHEN DIRECT B=0;
generic cubic hafnian condensation: IMPOSSIBLE, FIRST WEIGHT AT LEAST EIGHT;
new mixed-colour circuit:          det(corrected 3x3 pair block)=0;
coordinate-chart transition law:   EXACT, SCALAR HOLONOMY CAN BE TRIVIAL;
nine coordinate plane charts:      ONE COMMON EDGE REALIZES ALL LABELS;
torus-line coordinate label:        PURE GAUGE;
new axis topology boundary:        jet frames and matching shores still viable;
new strict axis reduction:         only 2+2+1 survives two-endpoint model;
new scalar ledger result:          all three 2+2+1 charts are hafnian-realizable;
new scalar synchronization:         one common terminal block is realized;
new pure-chart gluing:               one block graph realizes all pure charts;
new diagonal-lift boundary:          one forbidden mixed coefficient is 1/7;
new mixed residual localization:     only two unprescribed faces per word;
new low-compound boundary:           scalar degrees 1+3 are dominant;
new fifth-compound theorem:          generic incidence observes all 21 edges;
new degree-five circuit:             four faces cancel all 12 cross variables;
fixed charts, every core alignment:  EXCLUDED;
adapted single-word degree5/1 layer: CONSISTENT;
that word's three cubic faces:       UNIT IDEAL;
single-word compound over pure fibre: SINGULAR ESCAPE EXISTS;
full-tensor quotient law:            all 21 GHZ pair images must be dependent;
quotient law alone:                  sharp rank-one local escape exists;
unprojected binary GHZ contraction:  PHYSICALLY REALIZED;
all-pair binary quotient coherence:  TWO STRATA, BOTH ABSTRACTLY SHARP;
tricolour quotient rank law:         at least four codimension-two modes;
tricolour quotient bound:            SHARP ON ABSTRACT QUOTIENT DATA;
face-quotient Mayer--Vietoris law:    EXACT;
common-edge quotient gluing alone:   SHARP RATIONAL LIFT EXISTS;
full-terminal quotient rank sum:     AT MOST SIX;
rank-six disjoint colour supports:   EXCLUDED;
rank-six P3 disjoint-union K2:       EXCLUDED BY UNIT CERTIFICATE;
rank-six P4, K1,3, and K3:           QUOTIENT CONTROLS EXIST, LIFTS UNKNOWN;
new synchronization gap:            other scalar lifts remain;
new h=0 polar selector:            five null legs isolate one mixed pair block;
new arbitrary-order boundary:      at least three coordinate-incidence modes;
new incidence sharpness:           canonical profile does not balance the three;
new row-pair incidence theorem:    every pair needs at least five modes;
new five-mode sharpness:           polar/canonical/pure data attain equality;
new h!=0 conditional selector:     synchronized depth cancels direct blocks;
new aligned-resonance boundary:    scalar depth subtraction then loses a colour;
top two-port data at h!=0:         FULL AFFINE IMAGE;
corrected two-port universal ideal: SYMMETRIC FACTOR-ANALYSIS ELIMINATION IDEAL;
extra one-depth hafnian polynomial: NONE;
two-residual scalar ports <=4:     DOMINANT;
two-residual five-port ideal:      PRINCIPAL DEGREE-FIVE PENTAD;
block-port pentad obstruction:     EXACT BASIS-INDEPENDENT TENSOR;
legal five-port corrected window:  UNKNOWN;
q2 residual-present pair root depth: MAXIMAL AND PARITY ELIGIBLE;
q2 direct pair root depth:          TWO BEYOND BUDGET;
residual-null polar active pairs:   AT MOST THREE;
null-polar five-port pentad:        TERMWISE ZERO;
pair-dependent null fans evade bound: FALSE;
full-sensor named pair projection:  EXACT ON SIMPLE INCIDENCE LINE;
target-line h=0 pentad covariant:    DEGREE 5, S7-EQUIVARIANT;
nonzero target-line pentad:          EXCLUDES ENTIRE h=0 LINE;
pinned target-line h=0 gate:         EXACT DEGREE 8;
pinned 21-pair star alignment:       IFF, DEGREE 17;
target incidence alone forces pentad: FALSE, CONTROL=-6;
legal GHZ point on that pinned stratum: UNKNOWN;
legal companion incidence ideal:     I_219(pi_Delta Gamma);
simple-incidence line covariant:      SIGNED 218-MINORS;
weighted legal pair amplitude:        RELATIVE WEIGHT 15;
localized legal h=0 pair ideal:       EXACT IFF CRITERION;
ambient gated incidence forces pair ideal: FALSE;
legal border-GHZ preimage dimension: AT LEAST EIGHT;
seven-port factor inverse-image codimension: EXACTLY EIGHT;
mandatory legal secant--factor intersection: NONEMPTY;
complete factor ideal excludes legal border family: FALSE;
eight scalar covariants exhaust border family: FALSE;
proper secant--factor chart reduction: FINITE ARTINIAN LAURENT ALGEBRA;
committed sensor image membership:      24 ADJUGATE RESIDUALS;
ordered honest rank-three parameter space: DIMENSION 32;
torus-concise ordered secant cover:     DEGREE SIX;
exact I_(7,2) generators/degree:        35 CUBICS, 21 PENTADS, DEGREE 259;
universal good-open selector:           EXTERIOR/PAIR CONTRACTION, NO CHART ENUMERATION;
committed localized good quotient:      EXACT FINITE CRITERION, NOT BUILT;
good quotient nonzero:                  UNKNOWN;
committed h=0 star-alignment quotient:  UNKNOWN;
boundary trap on empty good quotient:   FOUR SECANT NORMAL-FORM MECHANISMS;
legal localized pair ideal is unit:   UNKNOWN;
P5/P6 support 18/21:              UNCONDITIONAL AFTER KNOWN EXTRACTION;
P7 support 24 transfer:           CONDITIONAL ON LEGAL SYNCHRONIZATION;
minimal tangent-companion cycle:  EXCLUDED BY FULL-ROOT COFACTOR COLLISION;
legal nonroot switching direction: PROJECTIVE GAUGE;
uniform physical legal-sensor curve: FLATTENING RANK NINE FOR ALL t!=0;
uniform switching saturation border rank: AT LEAST NINE;
nonuniform switching-quotient GHZ incidence: UNKNOWN;
highest-priority invented objects: legal five-port pentad window, synchronized deletion-deck selector, and nonuniform secant quotient invariant;
new legality boundary:             top synchronization has shore rank one;
highest-priority literature tools: square-free apolarity, quotient Lefschetz, secant saturation, determinantal elimination;
full proof or counterexample:      NOT YET;
global Krenn--Gu conjecture:       UNRESOLVED.
```
