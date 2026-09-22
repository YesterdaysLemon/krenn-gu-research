# Protected-component elimination and the Ward--boundary gap

## Status and evidence boundary

**Proved exact parent reduction and mechanism obstructions over C.** The
[independent review](../../docs/audits/PROTECTED_FULL_SOURCE_PARENT_REVIEW_2026-09-22.md)
passed. The boundary-contraction formulas, elimination
equivalence, polarization obstruction, Ward identities, and unrestricted
Ward-module classification have written analytic proofs below.  The three
companion scripts replay finite controls and semantic examples; they are not
the proofs of the arbitrary-order statements.

The Ward--boundary matching statement remains open.  No elimination theorem,
SFULL exclusion, or global Krenn--Gu resolution is claimed.  No Lean
formalization is supplied.

The protected family and the absence of an arbitrary-witness normal form are
owned by the [pure-matching scaffold theorem](PURE_MATCHING_SCAFFOLD_STRUCTURAL_GATE_NO_GO_THEOREM.md).
The current full-source parent and earlier extension barriers are recorded in
[the full-source extension barrier package](PROTECTED_SCAFFOLD_FULL_SOURCE_EXTENSION_BARRIERS.md).
The literal exterior-resource calculus used here is owned by the
[minority-cycle and resource theorem](PROTECTED_SCAFFOLD_MINORITY_CYCLE_AND_RESOURCE_BOUNDARY.md).

## 1. Parent proposition, quantifiers, and intended consumer

For each integer `k>=2`, a **protected scaffold** has `k` disjoint physical
K4 components.  In every component the three monochromatic perfect matchings

```text
M_0=01|23,  M_1=02|13,  M_2=03|12
```

have unit matrix-entry blocks `E_00,E_11,E_22`; every oriented
intercomponent block is an arbitrary hollow `3 x 3` matrix over `C`, with the
reverse orientation its transpose.  SFULL asserts that no such array has the
full normalized ternary GHZ matching tensor for any `k>=2`.

The proposed induction is deliberately narrower:

> **Protected-component elimination.**  From every full protected source
> with `k>=3`, remove some whole protected K4 and construct, from the same
> physical entries, a legal protected full source on the remaining `k-1`
> components.

This implication, iterated only while `k>=3`, reaches the accepted
[protected `k=2` exclusion](../finite/n08/EIGHT_VERTEX_PROTECTED_SCAFFOLD_EXCLUSION.md)
and proves SFULL.  It does not assert an arbitrary-witness normal form, so
even success would not by itself prove global Krenn--Gu.

The bounds matter.  A single protected K4 (`k=1`) is a valid normalized GHZ
source.  The exact empty-exterior diagonal contraction is the scalar `3`, not
`1`.  The `k=2` controls below are proper-subsystem nonwitnesses; they refute
canonical update rules and weakened supply claims, but do not refute an
existential elimination theorem whose premise is a full source and whose
scope is `k>=3`.

## 2. Exact boundary contraction

Remove one protected component `A={0,1,2,3}` and let `U` be the `N=4(k-1)`
exterior physical vertices.  Work in the physical vertex-square-zero algebra

```text
Z_U = C[x_(i,a): i in U, a in {0,1,2}]
      /(x_(i,a)x_(i,b): fixed i, arbitrary a,b).
```

The literal exterior matching quadratic and local incidence pencils are

```text
Q = sum_(i<j in U) sum_(a,b) W_ij[a,b] x_(i,a)x_(j,b),
f_(v,c) = sum_(i in U,a) W_vi[c,a] x_(i,a).
```

Define the common top matching map

```text
Phi_Q(P) = [full exterior physical support] exp(Q) P.       (1)
```

For color `c`, write `M_c={pq,rs}` and put

```text
u_c=f_(p,c)f_(q,c),   v_c=f_(r,c)f_(s,c).
```

Partitioning physical matchings by the number of local-to-exterior edges
gives the literal fixed-color and diagonal-sum boundary polynomials

```text
K_c=(1+u_c)(1+v_c),
K=sum_c K_c=3+K_2+K_4,                                (2)
K_2=sum_c(u_c+v_c),
K_4=sum_c u_cv_c.
```

For an arbitrary local color word `alpha`, the exact boundary is

```text
K_alpha
 = product_(v in A) f_(v,alpha_v)
   + sum_(uv protected and compatible with alpha)
       product_(w in A minus {u,v}) f_(w,alpha_w)
   + [alpha is constant].                              (3)
```

A full source supplies, with the same actual `Q` and incidence pencils in
every row,

```text
Phi_Q(K_alpha)=G_alpha,                                (4)
```

where `G_(c^4)=X_c=product_(i in U)x_(i,c)` and every mixed `G_alpha` is zero.
In particular,

```text
Phi_Q(K_c)=X_c,
Phi_Q(K)=G:=X_0+X_1+X_2.                              (5)
```

No independent cofactor or generic inverse is used in (1)--(5).

The 81 local rows have an exact `48+30+3` structure.  A nonconstant local
word has at most one compatible protected edge.  Forty-eight words have one,
thirty have none, and the three constant words have two.  For a protected
edge `e in M_c` with complement `bar(e)={p,q}`, the 48 selectors and three
pure rows are

```text
Phi_Q((1+z_e^c) f_(p,a)f_(q,b))=0       for (a,b)!=(c,c),
Phi_Q((1+z_e^c)(1+z_bar(e)^c))=X_c,                    (6)
z_{uv}^c=f_(u,c)f_(v,c).
```

The 30 remaining rows are the transversal quartic zeros.  These equations
compress to one tensor formula, but as a linear system they impose no further
identity among the exterior vacuum response, the six two-leg responses, and
the target tensors: each four-leg row has its own leading unknown.  Any
elimination step must therefore use the nonlinear sharing of the actual
`W,Q`, not a free linear-cofactor model.

## 3. The exact elimination gate

Let `H_U` be the vector space of **legal corrections** `Delta` on the retained
vertices:

1. `Delta` is zero on every edge within a retained protected K4, preserving
   all six fixed internal blocks there; and
2. every same-color coordinate `Delta_ij[a,a]` between retained components is
   zero, preserving hollow crossing blocks.

For this removed component, source-preserving elimination is equivalent to

```text
there exists Delta in H_U such that
Phi_Q(exp(Delta)-K)=0.                                 (ELIM)
```

Indeed, (ELIM) says that the smaller literal quadratic `Q+Delta` has top
tensor `G`; membership in `H_U` says it is still a protected scaffold.  This
is the weakest same-exterior relative-kernel formulation.  It does not demand
the false operator identity `exp(Delta)=K`.

The exact all-order parent gap is to derive (ELIM), for some component, from
all full source equations (4).  The work below rules out several proposed
ways of deriving it but does not rule out (ELIM) itself.

## 4. Why the canonical quadratic updates fail

The most direct candidate is `Delta=K_2`.  It requires both

```text
K_2 in H_U,
Phi_Q(exp(K_2)-K)=0.                                  (7)
```

The second equation is the selector-gluing identity.  Color by color, with
`R_c=u_c+v_c`, one could first seek

```text
Phi_Q(exp(R_c))=X_c,                                  (8)
```

but the aggregate still requires

```text
Phi_Q(exp(R_0+R_1+R_2))
  = sum_c Phi_Q(exp(R_c)).                             (9)
```

The left side permits simultaneous reuse of mutually exclusive removed-color
sectors.  Equation (9) does not follow from the three equations (8).

The exact formal connected expansion exposes the defect.  With
`A=K_2/3`, `B=K_4/3`,

```text
log(K/3)=L_2+L_4+L_6+...,
L_2=K_2/3,
L_4=K_4/3-K_2^2/18.                                  (10)
```

Equivalently, the first unnormalized exponential error contains

```text
K_2^2/2-K_4
 = (1/2) sum_e (z_e)^2
   + sum_(e<f, e intersects f) z_ez_f.                (11)
```

The six squared-edge terms repeat two local legs; the twelve pairs from
different protected partitions repeat their unique common local vertex.
Only the three complementary-edge products are physical four-crossing terms,
and those are already the terms of `K_4`.  In the quartic connected layer
(10), the exact sector counts and coefficients are

| local-leg sector | count | coefficient |
|---|---:|---:|
| one protected edge squared | 6 | `-1/18` |
| two intersecting edges from different partitions | 12 | `-1/9` |
| one complementary pair | 3 | `2/9` |

Every physical boundary word (3) uses each removed physical vertex at most
once.  Direct coefficient extraction and constant-coefficient polarization
therefore cannot produce the eighteen repeated-leg terms.  This multidegree
fact is a barrier only to the direct linear/polarization proof; it is not a
no-go for polynomial consequences sharing the actual source entries.

The normalized truncation `3 exp(K_2/3)` does not repair the problem.  The
factor `3` is structural at empty boundary, while a legal normalized smaller
source has no free global prefactor.  Higher connected layers also persist:
for one color,

```text
log K_c=sum_(m>=1)(-1)^(m+1)(u_c^m+v_c^m)/m,          (12)
```

so every layer beyond the first repeats one of the two removed protected
pairs.

## 5. Exact v1/v2/v3 fibre controls

Use the three accepted n=8 Laurent families documented with the
[complete protected-scaffold exclusion](../finite/n08/EIGHT_VERTEX_PROTECTED_SCAFFOLD_EXCLUSION.md)
and stored in
[`eight_vertex_scaffold_subsystem_controls.json`](../../tests/fixtures/eight_vertex_scaffold_subsystem_controls.json).
On each of `v1`, `v2`, and `v3`, eliminating one K4 gives the exact identity

```text
K_2=-Q.                                               (13)
```

For all three controls, exact calculation verifies every one of the 81 local
words over each of the three pure exterior words (`243` rows per family), and
also

```text
Phi_Q(K_c)=X_c,
Phi_Q(exp(R_c))=X_c                  for c=0,1,2,
sum_c Phi_Q(exp(R_c))=G,
Phi_Q(exp(R_0+R_1+R_2))=0.                           (14)
```

Thus the selector-gluing residual is exactly `-G`.  The canonical update
`Q+K_2` is zero and deletes all six retained protected unit edges, so it fails
both legality and the target.  The connected quadratic truncation gives

```text
Phi_Q(exp(K_2/3))=(4/9)G,                             (15a)
3 Phi_Q(exp(K_2/3))=(4/3)G,                           (15)
```

Thus the literal smaller-source candidate for `Delta=K_2/3` has tensor
`(4/9)G`, not `G`, and is also illegal because it changes every retained
protected unit to `2/3`.  Only the inadmissible global prefactor `3` gives
the second value in (15).  Inserting the exact quartic correction `L_4`
restores `G` in exterior order four after that formal prefactor is retained.

These controls sharply show that complete pure-exterior local fibres,
colorwise Gaussian response, the v2 binary subsystem, and the v3
independent-minority plus component-constant subsystem do not imply
selector gluing.  They are not full sources: each has known split-word
errors.  They also do not refute the existential gate (ELIM).  At `k=2` the
retained exterior is itself the valid protected K4, and `Delta=0` already
satisfies (ELIM).  A proof using all split words at `k>=3` remains possible.

There is a second exact obstruction to a termwise two-replica repair.  In the
unlabelled union of two perfect matchings, let `b_u` count exterior edges
incident with removed vertex `u`.  Alternating-cycle ownership shuffles
preserve every `b_u`.  Repeated-edge and overlapping-pair sectors in (11)
have some `b_u=2`; a legal one-replica contraction times a frozen protected
matching has all `b_u<=1`.  No termwise shuffle identifies them.  A rescue
would need a signed aggregate identity using the split-color equations.

## 6. Why free kernel multiplication is unavailable

Although (4) supplies many elements of `ker Phi_Q`, the kernel is not an
ideal.  More strongly, the top map has no nonzero annihilator ideal.  For a
nonzero class `P in Z_U`, put `S=exp(Q)P`, which is nonzero because `exp(Q)`
is a unit.  Choose a nonzero colored monomial of `S` with inclusion-maximal
physical support and multiply by a monomial on its complementary physical
support with fixed colors.  Terms of smaller support cannot reach full
support, terms using a physical vertex outside the chosen support vanish, and
terms with the same support but different colors land in different top
coordinates.  The chosen coefficient is therefore detected.  Hence

```text
Phi_Q(P R)=0 for every R  ==>  P=0.                   (16)
```

Consequently one may not multiply a scalar source-zero equation by a desired
quadratic insertion and remain in the same kernel.  Likewise, multiplying
two scalar evaluations produces two independent matching replicas; it does
not identify their exterior resources or yield the same-source response
`Phi_Q(P_1P_2)`.  This is the same boundary behind the squarefree-resource
warning: the physical top evaluation is linear, not a ring homomorphism.

## 7. Exact Ward transport and its limitation

There is one valid nonlinear same-source operation.  For exterior matrices
`A_i in Mat_3(C)`, define

```text
D=sum_(i,a,b) A_i[a,b] x_(i,a) partial_(i,b),
nabla_D P=DP+(DQ)P=exp(-Q)D(exp(Q)P).                 (17)
```

These derivations preserve the physical vertex-square-zero ideal and full
physical support.  Hence

```text
Phi_Q(nabla_D P)=D Phi_Q(P),
[nabla_D,nabla_E]=nabla_[D,E].                        (18)
```

Ward iteration therefore preserves source residuals without assuming an
ideal kernel.  Its second-order expansion is

```text
nabla_E nabla_D P
 = ED P +(EDQ)P +(DQ)EP +(EQ)DP +(EQ)(DQ)P.           (19)
```

The last term is a genuine product of two quadratic responses in the same
source.  The other four correction terms are mandatory; dropping them is
exactly the free-multiplication error.

A requested tangent `D_AQ=Z` must solve the shared block system

```text
A_i Q_ij+Q_ij A_j^T=Z_ij          for every i<j.      (20)
```

One sufficient fixed-removed-vertex condition for keeping each differentiated
boundary pencil in its own color span is that matrices `B_v` satisfy

```text
F_vi A_i^T=B_v F_vi                 for every v,i.    (21)
```

If the boundary module may mix the four removed vertices, the general
condition is instead

```text
F_vi A_i^T=sum_w B_vw F_wi          for every v,i.    (21a)
```

Neither (20), (21), nor (21a) follows formally from the source equations.

There is also an exact target-covariance restriction in the parent range
`k>=3`, where `N>=8`.  If `DG` lies in the span of the three pure exterior
monomials, every off-diagonal `A_i[a,b]`, `a!=b`, is zero: acting on `X_b`
creates a distinct word with color `a` only at site `i`, so no other term can
cancel it.  If `DG=mu G`, then

```text
sum_i A_i[c,c]=mu                         for c=0,1,2,
Z_ij[a,b]=(A_i[a,a]+A_j[b,b])Q_ij[a,b].                (22)
```

A target-covariant tangent can therefore only scale coordinates already
present in `Q`; it cannot create a missing effective edge.  Realizing `K_2`
this way would impose an additional shared endpoint-potential condition on
the actual entries.

Even simultaneous tangent and boundary-module solvability is insufficient.
On `v1`, the Euler derivation

```text
D=-(1/2) sum_(i,a)x_(i,a)partial_(i,a)
```

satisfies `DQ=-Q=K_2`, preserves every boundary pencil, and makes every
boundary degree an eigenvector.  Yet (14) still gives the selector-gluing
error `-G`. Exact tangent alignment, boundary-module closure, and target
covariance therefore do not imply canonical selector gluing or legality of
the prescribed quadratic update. They do not refute existential elimination:
as above, `Delta=0` works for these k=2 nonwitness controls.

The global color operators `E_ab=sum_i x_(i,a)partial_(i,b)` yield one further
proved same-source identity.  Their quadratic `gl_3` Casimir is not scalar on
the whole full-support tensor space: there it is
`3N I+sum_(i!=j)tau_ij`.  It acts by `N(N+2)` on the symmetric target
subrepresentation `Sym^N(C^3)`, which contains every `X_c` and `G`.  Therefore
(5) gives

```text
Phi_Q((sum_(a,b) nabla_ab nabla_ba - N(N+2))K)=0.     (23)
```

Its expansion contains the bilinear exterior response

```text
sum_(a,b)(E_ab Q)(E_ba Q)K                           (24)
```

together with all `E_abE_baK`, `(E_abE_baQ)K`, and first-response-times-
`DK` corrections.  Equation (23) genuinely couples exterior color words and
reaches a repeated-response sector.  It does not identify (24), which is
built from exterior blocks of `Q`, with the selector defect (11), which is
built from the four removed-to-exterior incidence families.  The v1 control
satisfies (23) while selector gluing still fails.

## 8. Unrestricted Ward-module membership already contains ELIM

The full unrestricted local-color Ward module has an exact pointwise support
classification, which prevents membership alone from serving as a proof.
Decompose the exterior zeon algebra by occupied physical support,

```text
Z_U=direct_sum_(S subset U) A_S,
A_S=(C^3)^(tensor S).
```

Let `g=direct_sum_i gl_3` act by all local color derivations.  The vertex
Euler operators `E_i=sum_a x_(i,a)partial_(i,a)` give exact support projectors

```text
pi_S=product_(i in S) E_i product_(j notin S)(1-E_j). (M1a)
```

On each `A_S`, products of local matrix units span `End(A_S)`.  Therefore,
for any finite family `F_alpha`, its pointwise unrestricted `g`-module is

```text
direct_sum_(S: some (F_alpha)_S != 0) A_S.            (M1)
```

Scalar division by a selected nonzero coefficient is legitimate at one fixed
complex source point; it is not a uniform polynomial identity in `W`.

Conjugating by `exp(Q)` gives the corresponding Ward-module classification
for `R_alpha=K_alpha-G_alpha`:

```text
M_Q(R_alpha)
 = exp(-Q) direct_sum_(S: some (exp(Q)R_alpha)_S != 0) A_S.  (M2)
```

For a full source, every transformed residual has zero component on the full
support `U`.  Raw top-degree terms can still appear after multiplication by
`exp(-Q)`; they cancel after the response is reconjugated.  The invariant is
the transformed top response, not the raw top component of a Ward iterate.

Now put `P=exp(Delta)-K`.  By (M2), bare pointwise membership
`P in M_Q(R_alpha)` requires `exp(Q)P` to vanish on every support absent from
all transformed residuals.  Its top-support instance is

```text
[A_U](exp(Q+Delta)-exp(Q)K)=0,
```

which is exactly (ELIM).  Thus unrestricted Ward-module membership does not
derive the missing response identity; it already tests that identity as one
of its necessary support conditions.  The Casimir operator is a legitimate
Ward element but does not evade this boundary.

A Ward argument becomes proof-producing only by exhibiting its combination
from independently established same-source coefficient identities.  A
denominator-free polynomial formula is the cleanest form.  A finite rational
open-cover argument is also possible if every nonzero denominator is proved
on its patch and every denominator-zero closed stratum is handled.  The exact
support classification (M1)--(M2) uses unrestricted local `gl_3`; restricted
target-covariant operator families may generate smaller modules.

## 9. The genuinely missing full-source lemma

The minimal missing implication is (ELIM).  A proof-producing form suggested
by the valid Ward operation above is the following open statement; no
uniqueness claim about possible nonlinear source operations is intended, and
bare pointwise module membership is expressly insufficient.

> **Ward--boundary matching (open).**  For every full protected source with
> `k>=3`, some removed component admits a legal `Delta in H_U` such that
> `exp(Delta)-K` is given by a denominator-free uniform Ward combination, or
> by a finite stratified family with every denominator-zero stratum closed,
> of the complete physical residuals `K_alpha-G_alpha`.  Its
> quadratic layer must account for `Delta-K_2`, and its first quartic layer
> must match the arbitrary-correction defect `Delta^2/2-K_4` to
> Casimir/color-changing responses of the same actual `Q,W`, retaining every
> `DK_alpha`, `D^jQ`, and transformed-target term.  The previously displayed
> `K_2^2/2-K_4` is only the canonical specialization `Delta=K_2`, whose
> legality is exactly one of the failed control conditions.

If this statement holds, (18) puts `exp(Delta)-K` in `ker Phi_Q`; legality and
(5) give a protected full source on `k-1` components.  Minimal `k` and the
accepted `k=2` exclusion then prove SFULL.

No Ward--boundary matching identity has been proved.  The Ward-module
formulation is a sufficient mechanism, not an established consequence of a
full source.  The exact controls rule out replacing its complete residual set
by pure local fibres, component constants, binary rows, independent-minority
rows, or tangent alignment.  The
[fixed-minority-depth no-go](PROTECTED_SCAFFOLD_FIXED_MINORITY_DEPTH_NO_GO.md)
separately proves that no uniform fixed minority-depth row set can replace
the full-source premise at arbitrary order; without evaluating a specified
gluing residual on those controls, it does not by itself disprove a
particular bounded-row Ward/gluing identity.
None of these boundaries rules out a cross-word identity using all full
equations and their shared physical entries.

Another sufficient proof-producing coordinate-ring route would exhibit a
uniformly constructed legal `Delta(W)` and uniform polynomial syzygies

```text
[x_beta](exp(Q+Delta)-exp(Q)K)
  = sum_omega h_(beta,omega)(W)
      (haf_omega(W)-delta_omega),                     (25)
```

plus corresponding syzygies for every forbidden coordinate of `Delta`.
This is also open.  Unlike free kernel multiplication, (25) would be a
genuine polynomial consequence in the shared source coordinates.  Such a
uniform construction is stronger than the pointwise existential statement
(ELIM); no choice or ideal-membership equivalence is asserted here.

## 10. Exact consequences and remaining obligation

The proved implications and controls establish:

1. The exact contraction edge from a protected source to the quartic boundary
   `K` is established with the literal common exterior matching core.
2. Source-preserving elimination is reduced exactly to the legal
   relative-kernel gate (ELIM).
3. The canonical updates `K_2` and `K_2/3`, fibrewise selector gluing, direct
   repeated-leg polarization, and termwise two-replica shuffling are blocked
   by exact controls.
4. Covariant Ward transport is validated as a legitimate nonlinear
   same-source operation, including the Casimir identity (23).
5. Bare unrestricted Ward-module membership is identified as a reformulation
   of the desired top-response condition, not an independent supply lemma.
6. The unresolved edge is a uniform or fully stratified
   Ward--boundary matching identity, or another explicit shared-coordinate
   syzygy, using the complete split-word equations.

The v1/v2/v3 arrays remain exact nonwitness controls for named proper
subsystems.  They do not refute a full-source or `k>=3` existential
elimination theorem.  The valid `k=1` source supplies the factor-three
normalization check.  No legal `Delta` is supplied under the full premise,
and Ward--boundary matching remains open.

## Reproduction and verifier scope

From repository root run:

```text
python -X utf8 claims/arbitrary-order/verify_protected_component_elimination.py
python -X utf8 claims/arbitrary-order/audit_protected_component_polarization.py
python -X utf8 claims/arbitrary-order/audit_protected_ward_module.py
```

The primary verifier reconstructs the literal exterior square-zero algebra
on the accepted v1/v2/v3 fixtures and checks `K_2=-Q`, all 243 local-word /
pure-exterior projections per family, the exact colorwise responses, both
quadratic-update defects, and the quartic restoration.  The polarization
audit independently reconstructs the `48+30+3` local-word classification and
the `6+12+3` connected-quartic sectors without importing the primary or a
generated receipt.  The Ward audit uses a two-vertex rational model to check
(M1)--(M2) and the raw-top versus transformed-response distinction.

These are exact finite replays.  The arbitrary-order contraction, kernel,
Ward, and module claims rest on the written proofs above.  None of the scripts
checks the open Ward--boundary statement or proves SFULL.
