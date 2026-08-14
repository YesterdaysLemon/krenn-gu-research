# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight fully-injective off-diagonal-monomial residual coordinate-endpoint exclusion

## Status

**Exact characteristic-zero exclusion of every off-diagonal monomial endpoint
left by S2CC.**  Retain all hypotheses and notation of the fully-injective
monomial-residual endpoint localization.  Thus

```text
D(a,b,c)=(a tensor y-x tensor b) tensor w+C tensor c,
ker D=span((x,y,0)),
rank rho=rank pi=rank theta=3,
```

and suppose

```text
C=lambda e_d tensor e_e,       d!=e,       lambda!=0.       (1)
```

S2CC proves that `w_d=w_e=0`; hence `w` is proportional to the unique third
coordinate vector `e_t`.  This theorem proves that this coordinate endpoint
is impossible.  Consequently, inside the monomial part of the remaining
fully-injective `(3,3,3)` row profile, only the diagonal coordinate endpoints
left by S2CD survive.

The proof uses the complete target slice, not a selected-source experiment.
It first establishes a sparse-edge plane-separation lemma through an exhaustive
projective incidence atlas.  Exact rational Nullstellensatz identities exclude
all atlas charts.  The common-row shift then places the physical middle row in
the third plane, and nine terminal graph charts are excluded both by exact
certificates and by a characteristic-not-two tangent-tensor argument.

This is a local exclusion, not a resolution of the fully-injective profile or
of the conjecture.  The diagonal coordinate endpoints, every nonmonomial
residual, wider lower-rank cells, other components and pole strata, higher
orders, and all-rank drop remain open.  Global Krenn--Gu remains
**UNRESOLVED**.

## 1. The complete off-diagonal endpoint face

Relabel

```text
d=0,                  e=1,                  t=2,
C=lambda e_0 tensor e_1,                    w=e_2.   (2)
```

The covectors `e_0^*,e_1^*` form a basis of `w^perp`.  Write

```text
r_i=rho(e_i^*),       p_j=pi(e_j^*),
q_k=theta(e_k^*),     k in {0,1},
u=r_2,                v=p_2,
R=span(r_0,r_1),      P=span(p_0,p_1),
Q=span(q_0,q_1).                                      (3)
```

All three displayed planes lie in the four-dimensional joint row space `E`.
Full injectivity makes them genuine two-planes and makes each of
`(r_0,r_1,u)` and `(p_0,p_1,v)` independent.

S2CC supplies, for every `gamma in w^perp`, the complete tensor identity

```text
per(r_i,p_j,q_gamma)-delta_(i=j) gamma_i T_i
  =C_(i,j) S_gamma.                                  (4)
```

After harmless nonzero rescaling, its restriction to (2) is

```text
per(r_0,p_0,q_0)=T_0,
per(r_1,p_1,q_1)=T_1,                                (5)

per(r_i,p_j,q_k)=0
  at every other binary cell except (i,j)=(0,1),     (6)

per(R,v,Q)=0,
per(u,P,Q)=0,
per(u,v,Q)=0.                                        (7)
```

The two cells `per(r_0,p_1,q_k)=S_k` are unrestricted.  The tensors `T_0`
and `T_1` are nonzero, decomposable, and fully transverse.  The last equation
of (7) is load-bearing below.  It follows directly from (4): `gamma_2=0`,
the second coordinate is absent from both the row and column of `C`, and the
target term also vanishes.  It is not inferred from the two common-row faces.

## 2. Sparse-edge plane separation

We isolate the new incidence statement.

### Lemma 1 (physical sparse-edge separation)

Let `E` be four-dimensional over a characteristic-zero field.  Let ordered
two-planes `(R,P,Q)` carry the table (5)--(6), and let `v` be a nonzero row
outside `P` satisfying `per(R,v,Q)=0`.  Then

```text
R intersect Q=0.                                     (8)
```

#### Proof: the projective atlas

Assume `R intersect Q` is nonzero and normalize

```text
r_0=e_0,                 r_1=e_1.                    (9)
```

There are two Schubert strata.

If `dim(R intersect Q)=1`, diagonal rescaling gives three supports for the
intersection line:

```text
span(r_0),       span(r_1),       span(r_0+r_1).     (10)
```

Relative to that line, an ordered basis of `Q` has three forms: the line is
the first row, the second row, or the difference of two outside rows.  Put
`S=R+Q`, so `dim S=3`.  Dimension forces either

```text
dim(P intersect S)=1              or              P subset S.  (11)
```

In the first alternative, the intersection line has three projective affine
charts and its position in the ordered `P` basis has three Borel supports.  In
the second, the two ordered `P` rows have `3 x 3` projective charts.  Therefore
this stratum has

```text
3 x 3 x (3 x 3 + 3 x 3)=162                      (12)
```

denominator-free charts.

If `R=Q`, an ordered `Q` basis has seven diagonal-torus support forms: two
monomial, four with exactly one zero matrix entry, and one full-support
one-parameter form.  The plane `P` is disjoint from `R`, meets it in a line,
or equals it.  These contribute respectively `1`, `2 x 3`, and `1` charts,
so this stratum has

```text
7 x (1+6+1)=56                                      (13)
```

charts.  Equations (12)--(13) give 218 initial incidence charts.

Exact ordinary-ring identities exclude 210 of them from the 48 constrained
coefficients of (5)--(6) alone.  Eight lift-hard charts are not promoted from
their bounded solver outcome.  Instead, they are refined using the physical
row `v`.

For a hard chart with `dim(P intersect S)=1`, split `v outside S` and
`v in S`.  In the first case choose `v=e_3` and shift both middle rows along
`v` into `S`; their ordered plane is covered by flag pivots.  In the second,
`v` and `P intersect S` form a flag in `S`.  For a hard chart with `P subset
S`, the same outside split gives an ordered-plane flag, while the inside split
gives the full flag

```text
span(v) < span(v,p_0) < S.                          (14)
```

The allowed operations are nonzero row rescaling, shifts
`p_j -> p_j+lambda_j v`, and the exceptional-edge shear
`p_1 -> p_1+mu p_0`.  Each preserves all constrained cells.

Ordinary pivot elimination gives the six standard affine flag charts
`f_ij`, `i!=j`.  Three pressure charts are replaced by complete smaller
unions, not by localizations:

- in the generic-affine outside case, the retained pivots together with
  three explicit projective boundary charts cover the complement;
- in the generic-`q_1` outside and inner cases, the missing first-row support
  is split into one affine chart and its endpoint;
- the generic-affine `f_21` chart has rows
  `(a,b,1)` and `(c,1,0)`.  If `c!=0`, it is already `f_20`; if `c=0`, it is
  exactly the durable `f21_p10_zero` chart.

Equivalently, for independent rows `a,b in k^3`, the pivot `f_ij` is available
when

```text
a_i (a_i b_j-a_j b_i) !=0.                          (15)
```

Successively setting the minors in (15) to zero gives precisely the listed
boundary charts.  Thus their union covers the whole flag variety over the
ground field; no inverse appears in a certificate.

The eight hard parents produce 98 logical refinement charts.  Together with
the 210 table-only charts, they give 308 separation charts.  The certificate
identities prove every chart empty, contradicting the assumed nonzero
intersection.  This proves (8).  QED.

### Independent coverage checks

The primary verifier reconstructs every reduced flag union over `F_3` and
`F_5`; the no-import audit uses a separate `F_7` implementation.  They cover
all `52`, `186`, and `456` complete flags respectively.  These finite-field
checks are adversarial checks of the implementation, not substitutes for the
minor argument (15).

## 3. Both target planes separate

Apply Lemma 1 to the physical middle row `v=p_2`.  Injectivity of `pi` gives
`v notin P`, so

```text
R intersect Q=0.                                    (16)
```

Exchange the first two roots.  The free edge remains one ordered sparse edge,
and `u=r_2` is now the physical middle row.  Lemma 1 gives

```text
P intersect Q=0.                                    (17)
```

No assertion that arbitrary sparse tables exist is made; the lemma is used
only on the complete physical face (5)--(7).

## 4. The common middle row lies in `Q`

Since `(p_0,p_1,v)` is independent,

```text
B=P+span(v),                         dim B=3.        (18)
```

Dimension gives a nonzero vector in `Q intersect B`.  Write it

```text
ell=a p_0+b p_1+c v.                                (19)
```

Equation (17) gives `c!=0`.  If `(a,b)!=(0,0)`, choose `lambda_0,lambda_1`
with

```text
a lambda_0+b lambda_1=c                             (20)
```

and shift

```text
P_lambda=span(p_0+lambda_0 v,p_1+lambda_1 v).       (21)
```

Then `ell in P_lambda intersect Q`.  The table survives by
`per(R,v,Q)=0`.  More subtly, the common first-row face needed after root
exchange also survives:

```text
per(u,p_j+lambda_j v,Q)
 =per(u,p_j,Q)+lambda_j per(u,v,Q)=0,               (22)
```

using the cross-zero in (7).  Lemma 1 after root exchange contradicts the
nonzero intersection.  Hence `a=b=0`, and (19) proves

```text
v in Q.                                             (23)
```

The symmetric argument also gives `u in Q`, though that placement is not
needed for the terminal contradiction.

## 5. The nine terminal graph charts

By (16), `E=R direct-sum Q`.  By (17), projection makes `P` the graph of an
invertible ordered `2 x 2` quotient matrix over `R`.  The target-preserving
diagonal rescalings and the allowed right-Borel shear
`p_1 -> p_1+mu p_0` leave three quotient orbits:

```text
diagonal: p_0=r_0+l_0,       p_1=r_1+l_1;
cross:    p_0=r_1+l_0,       p_1=r_0+l_1;
mixed:    p_0=r_0+r_1+l_0,   p_1=r_0+l_1.          (24)
```

The nonzero line `span(v)` in `Q` has three diagonal-torus supports:

```text
span(q_0),          span(q_1),          span(q_0+q_1).  (25)
```

Choose `h` complementary to `v` in `Q`.  Shifting the two middle rows along
`v` removes their `v`-components, so `l_0,l_1 in span(h)`.  Equations
(24)--(25) give exactly nine terminal charts.  The primary verifier checks
independently over `F_3` and `F_5` that the three quotient matrices exhaust
`T\GL_2/B` and that (25) exhausts nonzero `Q`-lines under the torus.

### A coordinate-free terminal audit

The nine terminal certificates have a separate analytic explanation.  Let
`Phi` denote the symmetric six-term polarization and put

```text
A=X(v), B=Y(v), C=Z(v),       x=X(a), y=Y(a), z=Z(a).
```

Then, in characteristic not two,

```text
Phi(a,v,v)/2=xBC+AyC+ABz.                            (26)
```

If (26) vanishes while `Phi(a,a,v)!=0`, contraction by annihilators gives
exactly two possibilities:

1. `A,B,C` are all nonzero, `x||A`, `y||B`, `z||C`, and
   `Phi(a,a,v)` lies on `A tensor B tensor C`;
2. exactly one of `A,B,C` is nonzero, and that fixed factor occurs in
   `Phi(a,a,v)`.

Exactly two nonzero values force the remaining row value to vanish and hence
`Phi(a,a,v)=0`; all three zero do the same.

For the cross quotient in (24), symmetry and `Phi(R,v,Q)=0` immediately give

```text
u_0 T_0=Phi(r_0,r_1,v)=u_1 T_1,
v=u_0q_0+u_1q_1,                                    (27)
```

which is impossible in all three supports (25).  For the diagonal quotient,
the generic support asks the same factor data in (26) to produce the
transverse tensors `T_0,T_1`; the two coordinate supports reduce to the
one-fixed-factor alternative and a zero-cell projection.  For the mixed
quotient, set

```text
D_i=Phi(r_i,r_i,v),            M=Phi(r_0,r_1,v).
```

The table gives

```text
D_0+M=u_0T_0,       M=u_1T_1,       M+D_1=0.        (28)
```

In the generic support, (28) and (26) force `D_0` onto the `T_1` line,
contrary to `D_0=T_0-T_1`.  In either coordinate support, the one-fixed-factor
alternative and the constrained cells `Phi(r_1,p_0,h)=0` and
`Phi(r_1,p_1,h)=0` force a nonzero target factor to vanish.  No unrestricted
`(r_0,p_1)` cell is used.  The exact nine-chart certificates below replay
these contradictions without relying on this analytic compression.

## 6. Exact Nullstellensatz exclusion

Choose source-coordinate bases whose first two factor lines are those of
`T_0,T_1`.  Their six selected coordinate forms on `E` have 24 independent
coefficients.  The atlas parameters add twelve reserved coordinates, for the
pinned 36-variable order.

For each table chart, expand the six-term permanent at all eight selected
source triples and all six constrained binary row cells.  This gives 48
ordered generators.  A physical refinement or endpoint appends the 32
selected coefficients of `per(R,v,Q)=0`, giving 80 generators.

For every literal polynomial system, the durable artifact contains an exact
ordinary-ring identity

```text
1=sum_nu h_nu f_nu.                                  (29)
```

The atlas has 317 logical coverage keys:

```text
210 table-only separation charts,
 98 physical separation refinements,
  9 terminal graph charts.                           (30)
```

Thirty keys are explicit lineage aliases for 18 repeated physical systems.
The generator hashes the complete key-free Singular program, so (30) is
stored as 287 canonical literal systems rather than recomputing or duplicating
identical certificates.  Every logical key retains its stage, parent, kind,
and canonical-system mapping.

The 287 identities contain 151,484 sparse multiplier terms: 142,580 in the
separation atlas and 8,904 in the terminal audit.  Their file SHA-256 is

```text
e940282a15261df2e5cc6d46c698b9bdb5e37299d5b5bb791dfeef4d711e3af1. (31)
```

There are no denominator variables, saturation variables, localizations,
modular lifts, or sampled parameter values.  Thus (29) excludes every chart
over every characteristic-zero field.  Lemma 1, (23), and the terminal cover
give the desired contradiction.

## 7. Proof-topology consequence

Combining S2CC, S2CD, and this theorem gives

```text
fully injective (3,3,3), C=lambda e_d tensor e_e:
  d!=e, w on the unique third coordinate:           IMPOSSIBLE;
  d=e, w on either complementary coordinate line:   OPEN;
  C nonmonomial:                                     OPEN.

joint-rank-three / derivative-rank-seven cells:      OPEN;
other components and pole strata:                    OPEN;
higher balanced orders / all-rank drop:               OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.     (32)
```

The surviving diagonal coordinate alternatives are necessary endpoints, not
constructed physical incidences.

## 8. Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_off_diagonal_monomial_residual_coordinate_endpoint_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_off_diagonal_monomial_residual_coordinate_endpoint_exclusion.py
python -m py_compile claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_off_diagonal_monomial_residual_coordinate_endpoint_certificates.py claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_off_diagonal_monomial_residual_coordinate_endpoint_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_off_diagonal_monomial_residual_coordinate_endpoint_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_off_diagonal_monomial_residual_coordinate_endpoint_certificates.py claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_off_diagonal_monomial_residual_coordinate_endpoint_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_off_diagonal_monomial_residual_coordinate_endpoint_exclusion.py
```

The generator needs Singular 4.x only for regeneration.  Every leaf runs in a
separate process, defaults to a 120-second wall cap and an 8-GiB address-space
cap, validates before entering the durable per-specification cache, and writes
no JSON after a filtered or incomplete run.  The primary replay uses SymPy.
The independent audit imports neither it nor the generator, reverses all 36
variables, parses row expressions through a restricted AST, and uses only
standard-library `Fraction` sparse arithmetic.

## Dependencies

- [Fully-injective monomial-residual endpoint localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_MONOMIAL_RESIDUAL_ENDPOINT_LOCALIZATION_THEOREM.md)
- [Diagonal-monomial two-supported endpoint exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_TWO_SUPPORTED_ENDPOINT_EXCLUSION_THEOREM.md)

## Scope boundary

```text
off-diagonal monomial coordinate endpoints:          IMPOSSIBLE;
diagonal monomial coordinate endpoints:              OPEN;
nonmonomial fully injective (3,3,3):                  OPEN;
other lower-rank cells / components / poles:          OPEN;
higher balanced orders / all-balanced rank-drop:      OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.     (33)
```
