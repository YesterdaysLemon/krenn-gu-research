# Hostile review of fixed-pair same-mode `N/N`, `q_+` exclusion

## Verdict and exact scope

**PASS, for the stated fixed-pair, pointwise, characteristic-zero,
same-mode common-kernel branch with a `q_+` companion.**  No residual-scalar,
support, placement, quotient-chart, rank-profile, tensor-order, same-slot,
field, dependency, implementation, or scope blocker survived final hostile
review.

The package assumes a remaining local plane contains the common exceptional
line

```text
N=K(x_2+x_3)
```

as the restricted kernel line of both mixed-factor projections.  The local
support of `N` is singleton or `{0,1}`, and the exact target propagates a
singleton colour-2 companion in

```text
span{x_0+x_1,x_2-x_3}.
```

The two projective companion branches are `q_-` and `q_+`.  This package
excludes

```text
q_+=x_0+x_1
```

for every support and placement case covered by the hypothesis.  The sibling
package excludes `q_-`, but the present package does not claim the later
same-mode synthesis, unrestricted `P_6 -> Delta_3` nonrestriction, or a
resolution of the global problem.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Reviewed frozen package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_SAME_MODE_NN_Q_PLUS_EXCLUSION_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_same_mode_nn_q_plus_exclusion.py
  audit_arbitrary_permanent_fixed_pair_same_mode_nn_q_plus_exclusion.py
```

Load-bearing frozen predecessors replayed in this review:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
  ARBITRARY_PERMANENT_FIXED_PAIR_SINGLETON_EXCEPTIONAL_COMPANION_PROPAGATION_THEOREM.md
  ARBITRARY_PERMANENT_FIXED_PAIR_SAME_MODE_COMMON_NONCOMMON_EXCLUSION_THEOREM.md
  ARBITRARY_PERMANENT_FIXED_PAIR_SAME_MODE_NN_Q_MINUS_EXCLUSION_THEOREM.md
```

## 1. Exact residual geometry

With

```text
R=span{x_0,x_1,x_2,x_3},       A=span{x_4,x_5},
J((a_4,a_5),(b_4,b_5))=a_4b_5+a_5b_4,
```

the five fixed complementary quartics are all `x_4x_5` times the displayed
quadratic in the theorem.  Direct contraction gives

```text
i_N(m_1,m_2,d_0,d_1,d_2)=(0,0,h_0,h_1,0),
i_q(m_1,m_2,d_0,d_1,d_2)=(L,L,L,L,-2M),

N=x_2+x_3,
q=q_+=M=x_0+x_1,
h_0=-x_0+x_1+x_2+x_3,
h_1= x_0-x_1+x_2+x_3,
L=-x_0-x_1-x_2+x_3.
```

Hence

```text
H=ker L intersect ker M=span{N,P},       P=x_0-x_1.
```

The exact double-`N` row is

```text
i_N i_N(m_1,m_2,d_0,d_1,d_2)=(0,0,2,2,0).
```

For `r=rho N+P`, direct contraction independently reproduces

```text
m_1: A=(1,-1, 1,-1),       m_2: B=(1,-1,-1, 1),
d_0: (rho-1)h_0,            d_1: (rho+1)h_1,
d_2: 2P.
```

The `P` residuals additionally satisfy

```text
A+B=C+D=2P,
C=(1,-1,-1,-1),             D=(1,-1,1,1).
```

These rows, all endpoint scalars `rho+-1`, and every common kernel used in
the proof were independently recomputed over the rationals.  The primary and
audit polarizers each compared `675` exact contraction entries with direct
four-slot polarization.

If the original `N` mode contained all of `H`, it would contain `P`.  The
legal `q,P` double contraction first forces the colour-2 coordinate of `P`
to vanish.  In separate evaluations of the original slot, the zero mixed
targets give `Theta(A)=Theta(B)=0`, while `A+B=C+D`.  The `d_0,d_1` targets
for `P` and `N` then identify independent pure `000` and `111` tensors,
forcing every local coefficient of `N` to vanish.  Thus the original mode
meets `H` in exactly `KN`; no same-slot double contraction is hidden here.

## 2. Characteristic-zero no-`H` quotient gate

Assume the two modes left after the original and companion modes are disjoint
from `H`.  Their images are three-dimensional hyperplanes `U,V` in

```text
W=(R/H) direct-sum A=D direct-sum A,       dim D=dim A=2.
```

For a nonzero quotient vector `(p,a)`, contraction of the zero `L` component
of the companion tensor and the off-colour zero `M` component gives two
scalar bilinear forms vanishing on `U times V`.

When `p!=0`, choose `D` coordinates `(x,y)` with `p=(1,0)` and put
`ell=J(a,-)`.  The two forms are

```text
F_0=J(A,A')+x ell(A')+x'ell(A),
F_1=y ell(A')+y'ell(A).
```

Cross-vanishing on two hyperplanes bounds each rank by two.  If
`J(a,a)!=0`, `F_0` has rank three.  If `a=0`, both hyperplanes are `D` plus
mutually `J`-orthogonal `A`-lines.  If `a` is nonzero isotropic, exact
hyperbolic coordinates show the two radicals meet in one line; distinct
hyperplanes are impossible and the unique common totally isotropic
hyperplane is `D+Ka`.

The initially omitted chart was `p=0`, where `a!=0` and

```text
F_0=x ell'+x'ell,             F_1=y ell'+y'ell.
```

Again the radicals have one-dimensional intersection.  Therefore `U=V`,
and the unique common totally isotropic hyperplane is

```text
D direct-sum Kb,              Kb=ker J(a,-).
```

This pure-`A` chart is now explicit in the theorem, primary verifier, and
independent audit.  It is required for a characteristic-zero proof; the
earlier finite-field orbit observation was not used as a proof.

For local bases

```text
u_i=(d_i,alpha_i b),          v_j=(e_j,beta_j b),
```

the live colour-2 contraction in the pure-`A` chart is

```text
c_0 beta_j d_i+d_0 alpha_i e_j+r h alpha_i beta_j,
h=J(b,b).
```

If `c_0d_0!=0`, the exact half-shifts

```text
d_i -> d_i+(h/(2c_0))alpha_i r,
e_j -> e_j+(h/(2d_0))beta_j r
```

absorb the pure term.  They do not change either map on `ker alpha` or
`ker beta`, so the two pure-`D` restrictions remain isomorphisms and retain
rank two.  A one-output-line `E_22` target is then impossible.  If exactly
one coefficient vanishes, the other pure-`D` restriction is still
surjective.  If both vanish, the live pure term forces

```text
alpha proportional e_2^*,       beta proportional e_2^*.
```

The `p!=0` chart yields the same exclusion/alignment conclusion without a
pure term.  Consequently the colour-0 and colour-1 columns of both shores
have zero `A`-part.  After contracting the actual pure-`R` vector `N`, a live
`d_0` or `d_1` cubic has at most the companion mode as an `A` supplier, but
`x_4x_5` needs two distinct supplier slots.  This closes the no-`H` branch.

## 3. Exhaustive `H`-line localization

The `q,r` double contraction for any `r in H` has zero left side, so the
colour-2 local coefficient of `r` is zero.  A two-dimensional local
intersection with `H` is impossible: over a characteristic-zero field it
contains a projective line outside any finite surviving list (and the
original-mode `P` argument above gives a direct exclusion there).

For support-two

```text
N=y_(t,0)+y_(t,1),             r=aN+bP,
```

the two legal `N,r` double contractions are

```text
2(a-b)G_sv=lambda_0 r_0 E_00,
2(a+b)G_sv=lambda_1 r_1 E_11.
```

They exclude support two for `r`, exclude the line `N`, and leave exactly

```text
r_-=N-P at colour 0,          r_+=N+P at colour 1.
```

The visible swap `x_0<->x_1`, colours `0<->1`, exchanges these endpoints.

For singleton `N=y_(t,0)`, the same equations become

```text
2(a-b)G_sv=lambda_0 r_0 E_00,
2(a+b)G_sv=0.
```

If `r_0!=0`, this localizes to the same-colour singleton `r_-`.  Otherwise
`r` is an opposite-colour singleton.  Projectively, its exhaustive list is

```text
r=rho N+P,                    rho in K,
```

together with the endpoint `r=N`.  The value `rho=-1` has zero `d_1`
residual against a live colour-1 target; `rho=1` is the special `r_+` chart;
all `rho!=+-1` share the generic four-tensor collapse.  No rational or
finite-field sampling is used to cover this projective continuum.

## 4. Rank profiles and diagonal tensor forks

For the support-two `r_-` cycle, the nonzero matrix

```text
G_sv=mu E_00
```

allows exactly the rank profiles

```text
(rank A_s,rank A_v)=(2,1),(1,1),(1,2).
```

The `(2,1)` profile makes `A_u` rank one supported only at colour `1`; the
pure `2222` word then has only the original mode as an `A` supplier.  In the
`(1,2)` profile, the live slices give `G_uv proportional E_11` and
`G_tv proportional E_22`; the zero residuals `h_2',k,P` and the off-target
`h_0` slice put `y_(s,1)` in `Kq_+`, contradicting independence from
`y_(s,2)=q_+`.

The initial `(1,1)` proof text incorrectly described the uncontracted pure
`1111` word as having only mode `u` available: for support-two `N`, the
individual vector `y_(t,1)` may have a nonzero `A`-part.  Before freeze this
was repaired by legally contracting the actual vector

```text
N=y_(t,0)+y_(t,1) in R.
```

The resulting live `C_(h_1)` cell on `(s,u,v)` has
`A_s e_1=A_v e_1=0`, so only mode `u` can supply an `A` factor and the cubic
vanishes.  The repaired argument is exact and does not assume the individual
support-two columns are pure `R`.

The singleton same-colour `r_-` cycle uses the same three exhaustive rank
profiles with the different zero/live `h_1` target.  They close respectively
by the exact kernel of `L,h_0,h_1`, the two-dimensional common kernel of
`h_2',k,P`, and the one-`A`-supplier pure `d_1` word.  Every matrix slice is
taken in a mode distinct from the contracted `N` or `r_-` slot.

For the generic opposite-colour continuum, `G_sv=0` and rank-zero shores are
incompatible with the live `h_0,h_1` tensors.  Thus

```text
A_s=p alpha^T,               A_v=q gamma^T,
J(p,q)=0,                    alpha_2=0.
```

The four legal contraction equations, in orders `(s,u,v)` and `(s,t,v)`,
are

```text
X tensor delta tensor gamma + alpha tensor beta tensor Z=lambda_0 e_0^3,
Y tensor delta tensor gamma + alpha tensor beta tensor W=0,
X tensor epsilon tensor gamma + alpha tensor pi tensor Z=0,
Y tensor epsilon tensor gamma + alpha tensor pi tensor W=lambda_1' e_1^3.
```

Quotienting the first factor by `K alpha` forces `alpha= e_0` or `e_1`.
Both coordinate forks were rederived entry by entry.  In one fork

```text
delta,gamma~e_0, epsilon=Z=Y=beta=0, pi,W~e_1;
```

in the other

```text
epsilon,gamma~e_1, delta=W=X=pi=0, beta,Z~e_0.
```

In either case the only possible colour-2 `A` pair is zero by the
two-dimensional `J`-orthogonal-line geometry.  This argument includes the
proportional-isotropic possibility and kills the live `d_2` word.

At `r_+=N+P`, the zero `d_0` tensor disappears, so the two three-equation
forks were checked separately.  For `alpha=e_1`, the `v_2` companion slice
gives `L(v_2)=0`, `M(v_2)!=0`, and `G_tu~E_22`; the mixed residuals and
`h_1` put `v_2` in `KM`, contradicting `L(M)=-2`.  For `alpha=e_0`, the row
`delta=0` confines every `A_u` column to one line, while
`beta~e_0` forces `A_u e_2=0`, contradicting the `(2,2)` entry of `G_tu`.

The distinct second-singleton-`N` endpoint has the full four equations
above and is excluded by the same two coordinate forks.

## 5. Coincident `q_+` and second-`N` mode

The distinct-mode collapsed cycle does **not** cover a mode containing both

```text
y_(s,1)=N,                   y_(s,2)=q_+.
```

This was a genuine case-cover gap in the earlier attack, and the frozen
package now contains a separate legal-slot proof.  With the original
`y_(t,0)=N`, the legal double contraction of the two `N` vectors in the
distinct modes `t,s` gives

```text
G_uv=0.
```

Neither `A_u` nor `A_v` can vanish, because the live `h_1` and `M` tensors
would then require one common Gram matrix to be supported at both `E_11`
and `E_22`.  Hence both ranks are one.  Write

```text
A_u=u alpha^T,               A_v=v gamma^T,
epsilon_i=J(A_t e_i,v),      pi_i=J(A_t e_i,u).
```

Since `y_(t,0)=N` is pure `R`, `epsilon_0=pi_0=0`.  The live contraction of
`N=y_(s,1)` has first-factor support `e_1`, while the separate live
contraction of `q_+=y_(s,2)` has first-factor support `e_2`.  Therefore
`epsilon,pi` are independent.  The zero `h_0` contraction in the single
mode `s` is

```text
epsilon tensor (h_0R_u) tensor gamma
 +pi tensor alpha tensor (h_0R_v)=0.
```

Independence forces `h_0R_u=h_0R_v=0`.  Contracting the original `N` in mode
`t`, its live `h_0` tensor is then

```text
(h_0R_s) tensor G_uv
 +(h_0R_u) tensor G_sv
 +(h_0R_v) tensor G_su=0,
```

a contradiction.  `N` and `q_+` in the same mode are used only in separate
single-slot evaluations; they are never inserted into two tensor slots.

For completeness, a non-`N` line `rho N+P` sharing the companion mode also
cannot create a missing branch: its two mixed residuals are `A,B`, and

```text
M=(B-A)/2-L.
```

The three zero tensors `Theta(A)=Theta(B)=Theta(L)=0` contradict the live
`Theta(M)` tensor directly.  The main case tree already closes such a
configuration through the no-`H` or other-`H` branch; this identity is an
independent exhaustiveness check.

## 6. Hostile repairs and legality audit

The following defects in intermediate reasoning were found and repaired
before the reviewed hashes were frozen:

1. **Missing pure-`A` quotient chart.**  The initial no-`H` classification
   treated only `p!=0`.  The `p=0` forms, their unique common hyperplane,
   and the exact half-shift are now explicit.
2. **Support-two `(1,1)` supplier wording.**  The initial pure-word sentence
   forgot that an individual support-two `N` column may carry `A`.  The
   frozen proof contracts the actual pure-`R` vector `N` before invoking the
   one-supplier contradiction.
3. **Coincident `q_+/N` mode.**  The distinct-mode rank-`(1,1)` collapse was
   initially being asked to cover a collapsed same-mode shore.  Section 9.2
   now gives the separate `epsilon,pi` independence proof above.
4. **Audit scope-marker typo.**  A stray literal plus sign in one required
   status string made the independent audit fail.  It was removed before
   freeze; the audit then passed without weakening any assertion.

Every displayed double contraction uses vectors from distinct local modes.
When two useful vectors lie in one mode, the proof compares separate single
contractions through one linear tensor map.  Every final `x_4x_5` supplier
argument respects multilinearity: the two `A` factors must come from two
different input slots.  No same-slot contraction, same-slot `A` pairing, or
silent reuse of one local vector survived review.

Characteristic zero is sufficient.  The proof uses `2!=0`, the exact
half-shift denominators, finite-dimensional rank, and the infinitude of the
field for the two-dimensional `H`-intersection shortcut.  It uses no order,
positivity, algebraic closure, generic point, numerical approximation, or
finite-field-to-characteristic-zero inference.

## 7. Computational replay and independence

The final current-byte replay passed at base commit
`45b48edff19815a376254c6d00bbdc59f817fddc`:

```text
q_+ primary exact verifier:                            PASS;
q_+ independent no-import audit:                      PASS;
q_- sibling primary and audit:                        PASS;
kernel-support predecessor primary and audit:         PASS;
singleton-companion predecessor primary and audit:    PASS;
same-mode common/noncommon primary and audit:          PASS;
py_compile on the reviewed Python files:               PASS;
Ruff on the reviewed Python files:                     PASS.
```

The primary q+ verifier uses SymPy and reports `675` exact direct-polarization
entries.  It reconstructs the residual tables, both quotient charts, the
half-shift, rank-profile kernels, generic and special coordinate forks, and
the coincident-mode tensor rank.

The independent audit imports neither SymPy nor the primary verifier.  It
uses square-free monomial dictionaries, `Fraction` row reduction, and a
separately written permutation polarizer, again checking `675` exact entries.
Its enumeration of `156` hyperplanes over `F_5` is explicitly labelled
finite-field stress evidence only; the written characteristic-zero
classification is the proof.

## 8. Accepted boundary

```text
same-mode common kernel line N/N:                       ASSUMED;
singleton/support-two support of original N:            EXHAUSTIVE;
q_+ no-H quotient branch:                               EXCLUDED;
q_+ support-two H-line branches:                        EXCLUDED;
q_+ singleton same-colour cycle:                        EXCLUDED;
q_+ singleton opposite-colour continuum:                EXCLUDED;
q_+ distinct second-singleton-N endpoint:               EXCLUDED;
q_+ coincident companion/second-N mode:                  EXCLUDED;
all q_+ placements under the theorem hypothesis:        EXCLUDED;
q_- companion branch:                         SIBLING THEOREM;
combined same-mode synthesis:                      NOT CLAIMED HERE;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

## Final reviewed hashes

```text
q_+ theorem:
2DFD23DFDE70593BF8363B633C15901D106CDF7F9C7C40C41B6CCA00CF1FBB50

q_+ primary verifier:
D33281C8989BB59C175EB71D702AB3EB1196D96CADF03A199DDC5A220D72ACBD

q_+ independent audit:
2BF281EE66AD86819446A22C7813C9AFCE86ABC8B91CC90176785BC7A808735E

kernel-support predecessor theorem:
7AEC9CD00DEBAC1D5CFA91D44E5D3634BD6D05FF8CA755BA1C2E83D1F8C3C45B

singleton-companion predecessor theorem:
EF703D8B5EA711945D6384A93F2542F8A84F2D5140FBB2B7D2F1CB944D25EA57

same-mode common/noncommon predecessor theorem:
05F1655F238025804309A8A0071BA0B53FE4BB5A250DE76DD5ABF15438FAF990

q_- sibling theorem:
3F4141CDE71069FB249025A0122C657F8F803DA922FDC47268181B5BE99D76D4
```
