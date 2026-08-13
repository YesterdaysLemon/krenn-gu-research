# Balanced `m=3` common-three-space transverse-rank-six beta-zero localization

## Status

**Exact characteristic-zero localization of the sole surviving joint-rank-six
common-three-space mechanism.**  Let `U` be the total singleton span of a
normalized, target-consistent physical `m=3` common shore.  Assume

```text
dim U=3,                         rank H=6,             (1)
```

and retain the transverse case left open by S2AC.  After permuting roots,

```text
B_23=B!=0,        B_13=C!=0,        B_12=0,           (2)
rank D_(B,C)=6.                                         (3)
```

Then the following exact alternatives hold.

1. The three-plane of relations between the first two root-row blocks is
   contained in one fixed target-coordinate hyperplane; or
2. at least one of those root-row blocks has rank exactly two.  Its kernel is
   the missing coordinate `e_s^*`, the corresponding contraction of the
   opposite root--root block is a nonzero multiple of the diagonal coordinate
   `e_s`, and all relation-plane contractions of both root--root blocks use
   that same third-root coordinate line.

Independently, absence of a fully supported beta-zero annihilator forces the
two root--root blocks into one of two sharp forms: one block is a coordinate
monomial, or one block has a coordinate factor and a common-end pencil whose
base point lies on the target-coordinate boundary while the other block lies
in its associated tangent family.

This is a localization, not an exclusion.  Both displayed boundaries still
require the uncontracted permanent equations.  Joint rank at most five, the
other S2T/S2Q branches, higher orders, all-rank-drop, a witness, and a
counterexample remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. The transverse linear normal form

Put

```text
K=image H subset A_1 direct-sum A_2 direct-sum A_3.  (4)
```

The shared derivative is

```text
D_(B,C)(a,b,c)=a tensor B+C tensor b.                 (5)
```

It ignores `A_3`.  Rank six therefore gives

```text
ker D_(B,C)=A_3.                                     (6)
```

Since `D_(B,C)(K)=U` has dimension three, rank--nullity on the
six-dimensional space `K` gives

```text
A_3 subset K,
K=A_3 direct-sum K_12,        dim K_12=3,             (7)
U=D_(B,C)(K_12),

K_12=K intersect (A_1 direct-sum A_2).               (8)
```

Let

```text
L=K_12^perp subset A_1^* direct-sum A_2^*, dim L=3.  (9)
```

Write the transposed root-row maps as

```text
rho:A_1^*->W^*,       pi:A_2^*->W^*,
theta:A_3^*->W^*,     W=X direct-sum Y direct-sum Z. (10)
```

Then

```text
ker(rho+pi)=L,
V=image rho+image pi,                     dim V=3,
Q=image theta,                            dim Q=3,
V intersect Q=0.                                      (11)
```

Indeed, (7) makes `theta` injective.  A common vector of `V` and `Q` would
come from a covector vanishing on `K`; evaluation on the contained `A_3`
kills its third component, after which (9) kills the common vector.  Since
`rank H=6`, the two row spaces in (11) are complementary.

## 2. The beta-zero root-block atlas

For root covectors `alpha,beta,gamma`, put

```text
lambda=(beta tensor gamma)(B),
mu=(alpha tensor gamma)(C).                          (12)
```

The S2S contraction vector is

```text
beta_root=(lambda,mu,0).                              (13)
```

If `lambda=mu=0`, the product functional annihilates the whole image of
`D_(B,C)`, hence annihilates `U`.  S2R therefore implies

```text
there are no fully supported alpha,beta,gamma
with lambda=mu=0.                                    (14)
```

We classify exactly when two matrices can satisfy (14).

### Lemma 1 (two-block torus-zero classification)

Let `B in A_2 tensor A_3` and `C in A_1 tensor A_3` be nonzero over an
algebraically closed characteristic-zero field.  If (14) holds, then, after
possibly exchanging `B,C` and permuting coordinates at their noncommon
endpoints, one of the following occurs.

```text
I.  B=e_i tensor e_s up to a nonzero scalar;          (15)

II. B=e_i tensor z,
    C=e_j tensor w+x tensor z,                        (16)

    z,w are independent and their common annihilator
      span(gamma_0)=ker z intersect ker w
      lies on the target-coordinate boundary,
    ker z meets the root torus.                       (17)
```

In II, `x` is arbitrary (its `e_j` component may be absorbed into `w`) and
`w` is merely required to be independent of `z`.  Both I and II genuinely
avoid a fully supported simultaneous zero, so the alternatives are sharp.

### Proof

For a fixed fully supported `gamma`, a nonzero vector has no fully supported
annihilating covector exactly when it lies on one coordinate line.  Thus
(14) says that, for every `gamma` in the third-root torus, at least one of

```text
B(gamma) in A_2,             C(gamma) in A_1         (18)
```

is a nonzero coordinate vector.

The torus is irreducible.  It is covered by the six closed conditions saying
that one vector in (18) belongs to one fixed coordinate line.  Hence one
condition holds identically.  After exchanging blocks, suppose

```text
image(B:A_3^*->A_2) subset span(e_i),
B=e_i tensor z.                                      (19)
```

If `ker z` misses the torus, `z` is a coordinate vector and I holds.
Otherwise `P(ker z)` meets the torus in a dense open subset of an irreducible
line.  On that line `B(gamma)=0`, so `C(gamma)` must be nonzero coordinate.
Irreducibility again fixes one line `span(e_j)` and gives

```text
C(ker z) subset span(e_j).                           (20)
```

Modulo `e_j`, the map `C` vanishes on `ker z`; elementary linear algebra
therefore gives

```text
C=e_j tensor w+x tensor z.                           (21)
```

On `ker z`, nonvanishing of `C(gamma)=e_j w(gamma)` says that
`ker z intersect ker w` contains no torus point.  The two forms are
independent and their one-dimensional common kernel is consequently a point
of the coordinate boundary.  This is exactly II.  Notice that the boundary
point may have one zero coordinate and two nonzero coordinates; it need not
be a coordinate point.

Conversely, I makes `lambda` a product of two nonzero coordinate values.  In
II, either `z(gamma)!=0`, when `B(gamma)` is nonzero coordinate, or
`z(gamma)=0`.  In the latter case a fully supported `gamma` cannot span the
boundary line `ker z intersect ker w`, so `w(gamma)!=0` and
`C(gamma)=e_j w(gamma)` is nonzero coordinate.  Thus both forms satisfy
(14).  QED.

## 3. A relation-plane annihilator

Let

```text
L^circ={(u,v) in L:
        every coordinate of u and v is nonzero}.     (22)
```

Either `L^circ` is empty, in which case irreducibility of the linear space
`L` puts it in one of the six coordinate hyperplanes, giving alternative 1
of the theorem, or `L^circ` is dense in `L`.

Assume the latter.  For `ell=(u,v) in L^circ`, define the third-root form

```text
f_ell=B^T v-C^T u.                                   (23)
```

For every `gamma in ker f_ell`, the two contractions agree:

```text
lambda=(v tensor gamma)(B)
      =(u tensor gamma)(C)=mu.                        (24)
```

Consequently

```text
D_(B,C)^T(u tensor v tensor gamma)
 =lambda (u,v,0) in L direct-sum 0=K^perp.           (25)
```

Thus `u tensor v tensor gamma` annihilates `U`.

S2R first shows that `f_ell` is a nonzero coordinate form: any other
hyperplane contains a fully supported `gamma`.  Let its missing target colour
be `s`.  If `B^T v` did not vanish identically on `ker f_ell`, one could
choose `gamma` on that coordinate hyperplane with exactly its `s` coordinate
zero and with `lambda!=0`.  The target contraction would retain exactly two
colours, while (13) would have support two.  S2S says a nonzero contraction
retaining two target colours requires `beta_root` to have support three.
Contradiction.  Therefore

```text
B^T v, C^T u, f_ell all lie in span(e_s).             (26)
```

The dense irreducible set `L^circ` is covered by only three choices of `s`.
One choice is fixed on a dense subset and polynomial closure gives

```text
B^T(pr_2 L) subset span(e_s),
C^T(pr_1 L) subset span(e_s).                         (27)
```

## 4. Target consistency forces an aligned rank-two row

The projection dimensions of the relation plane are exactly the involved
row ranks:

```text
dim pr_2 L=rank rho,             dim pr_1 L=rank pi. (28)
```

If both ranks were three, (27) would give

```text
B=b tensor e_s,                 C=c tensor e_s,      (29)
```

so the two derivative summands would meet on
`span(b tensor c tensor e_s)` and `rank D_(B,C)=5`, contradicting (3).
At least one of `rho,pi` therefore has nonzero kernel.

We record the target-consistency argument for `pi`; the other case is
symmetric.  Let `0!=v in ker pi`.  Then `(0,v) in L`, so every `(a,b) in
K_12` satisfies `v(b)=0`.  Contracting (5) in the second root gives

```text
v(U) subset (pr_1 K_12) tensor (v tensor id)(B).      (30)
```

The empty permanent is linear in the second root row, hence

```text
v(G_N)=0.                                             (31)
```

Target consistency `G_N in J+U` makes every nonzero colour in

```text
v(J)=sum_c v(e_c) e_(1,c) tensor e_(3,c) T_c         (32)
```

belong to (30).  The pure nonroot monomials `T_c` are independent.  The
fixed third-root factor in (30) cannot be proportional to two distinct
coordinate vectors.  It is also nonzero, since otherwise (32) could not be
absorbed.  Thus every nonzero vector of `ker pi` has coordinate support one.
A vector space of dimension at least two contains a sum with support at
least two, so

```text
rank pi=2,                      ker pi=span(e_d^*),
(e_d^* tensor id)(B) in span(e_d)\{0}.               (33)
```

But `e_d^* in pr_2 L`; comparison with (27) forces `d=s`.  Hence

```text
ker pi=span(e_s^*),
(e_s^* tensor id)(B)=kappa e_s,       kappa!=0.       (34)
```

The symmetric conclusion is

```text
ker rho=span(e_s^*),
(e_s^* tensor id)(C)=kappa' e_s,      kappa'!=0       (35)
```

whenever `rho` is the rank-two block.  This proves alternative 2.

## 5. Proof-topology consequence

The sole rank-six common-three-space survivor is now confined to

```text
two transverse root blocks, beta-zero atlas I or II;
and either
  relation plane L lies in one coordinate hyperplane;          OPEN;
or
  one involved root row has rank two with coordinate kernel,
  an aligned diagonal root-block contraction, and (27).        OPEN.

joint rank at most five / other physical branches:             OPEN;
global Krenn--Gu conjecture:                                   UNRESOLVED. (36)
```

The next exact obligation is to impose the full uncontracted permanent
identities on these coordinate-boundary normal forms.  No finite scan,
genericity argument, or numerical optimization is promoted here.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_transverse_rank_six_beta_zero_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_transverse_rank_six_beta_zero_localization.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_transverse_rank_six_beta_zero_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_transverse_rank_six_beta_zero_localization.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_transverse_rank_six_beta_zero_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_transverse_rank_six_beta_zero_localization.py
```

The primary replay checks the transverse derivative/kernel split, both sharp
beta-zero atlas families, the relation-plane annihilator identity, the
support-two S2S contradiction, projection/rank identities, and the target
kernel contraction.  The independent no-import audit reconstructs the same
maps using `Fraction` elimination and separate tensor indexing.  The torus
irreducibility and arbitrary-vector arguments above are the proof.

## Dependencies

- [`BALANCED_M3_COMMON_THREE_SPACE_JOINT_CROSS_RANK_SIX_SHARED_FACTOR_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_CROSS_RANK_SIX_SHARED_FACTOR_EXCLUSION_THEOREM.md)
- [`BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md`](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)
- [`BALANCED_M3_BOUNDARY_ANNIHILATOR_COMMON_QUOTIENT_P3_ORBIT_THEOREM.md`](BALANCED_M3_BOUNDARY_ANNIHILATOR_COMMON_QUOTIENT_P3_ORBIT_THEOREM.md)
