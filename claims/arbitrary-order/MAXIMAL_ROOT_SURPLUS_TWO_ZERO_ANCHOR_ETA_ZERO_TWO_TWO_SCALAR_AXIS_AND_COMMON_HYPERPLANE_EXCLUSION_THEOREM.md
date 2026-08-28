# Maximum-root surplus-two zero-anchor eta-zero two-two scalar-axis and common-hyperplane exclusion

## Status

**Candidate exact characteristic-zero same-source exclusion (`GLS66`).**
Continue from the `GLS65` eta-zero local rank profile `2,2,3,3`.  The full
`GLS64` scalar hierarchy first forces the two rank-three ports to be active
on the same deficient side.  It kills the cross-product edge between the
two silent ports and synchronizes all four silent--rank-three edges.

The same active-side alignment puts the two rank-three `P_4` source
rowspaces in hyperplanes whose normals omit one common fixed-row source
coordinate.  Purity forces those hyperplanes to coincide.  Since at least
one rank-three port is `c`-oriented, their common normal has support on only
the inactive fixed-row coordinate and one probe coordinate.  The exact
squarefree annihilator of that common hyperplane excludes every same- or
opposite-orientation pair of silent ports.

Consequently the complete `GLS65` eta-zero `2+2` residual is empty.  With
`GLS64`, this would exclude the entire `GLS63` exactly-two-deficient family.
This candidate does not touch profiles with three or more deficient maps,
the unique-nonrigid branch, attachment, response, selector,
synchronization/activity, the nonzero-anchor branch, or arbitrary root
order.  It does not change the global status without hostile review.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## Dependencies and exact scope

- [`GLS63`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_MIXED_KERNEL_PARTIAL_UNCONTRACTION_AND_TWO_DEFICIENT_BINARY_LOCALIZATION_THEOREM.md)
  supplies exactly two deficient maps with common kernel `K e_c`, four
  injective nonaxis ports, `|E_c| in {3,4}`, and the nonzero binary deck.
- [`GLS64`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TWO_DEFICIENT_MATCHING_INTEGRABILITY_AND_KERNEL_EDGE_ZERO_LOCALIZATION_THEOREM.md)
  supplies `eta=0`, all six `delta` equations, all eight one-kernel cofactor
  equations, and the nonzero raw matching scalar `H`.
- [`GLS65`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_ETA_ZERO_PERMANENT_SOURCE_AND_TWO_TWO_LOCAL_RANK_LOCALIZATION_THEOREM.md)
  identifies the separated `P_4` source and confines it to exactly two
  silent rank-two ports and two rank-three ports.

Work over the common characteristic-zero fraction field.  Relabel the two
silent ports as `s,t` and the rank-three ports as `r,v`.  Retain the `GLS64`
notation

```text
A_i=a_i(k_i),              B_i=b_i(k_i),
w_(ij)=W_(ij)(k_i,k_j),
H=w_(st)w_(rv)+w_(sr)w_(tv)+w_(sv)w_(tr).            (1)
```

Here `k_i=p_i cross q_i`.  At a silent port, `a_i,b_i` lie on the `c`-line
and `(k_i)_c=0`, hence

```text
A_s=B_s=A_t=B_t=0.                                   (2)
```

At a rank-three port, `p_i,q_i` span a plane and at least one of `a_i,b_i`
leaves it.  Therefore

```text
(A_r,B_r)!=(0,0),             (A_v,B_v)!=(0,0).       (3)
```

## 1. Scalar-axis synchronization

### Lemma 1 (the silent edge vanishes)

```text
w_(st)=0.                                               (4)
```

### Proof

The `GLS64` cofactor equations with the open rank-three port omitted give

```text
A_r w_(st)=B_r w_(st)=0.                              (5)
```

Equation (3) forces (4). `square`

### Lemma 2 (one common active deficient side)

After exchanging the two deficient labels if necessary,

```text
A_r,A_v!=0,              B_r=B_v=0.                   (6)
```

Moreover, for `lambda=A_v/A_r`,

```text
w_(tv)=-lambda w_(tr),
w_(sv)=-lambda w_(sr),
H=-2lambda w_(sr)w_(tr)!=0.                           (7)
```

In particular all four silent--rank-three `w` values are nonzero.

### Proof

The cofactors with silent ports `s,t` omitted say that both columns

```text
(w_(tv),w_(tr))^T,             (w_(sv),w_(sr))^T     (8)
```

lie in the kernel of

```text
M=[A_r A_v; B_r B_v].                                 (9)
```

If `det M!=0`, all four entries in (8) vanish.  Together with (4), this
would give `H=0`, contrary to `GLS63`.  Hence

```text
A_rB_v-B_rA_v=0.                                     (10)
```

Because this is the `eta=0` divisor, the remaining pair equation is

```text
delta_(rv)=A_rB_v+B_rA_v=0.                          (11)
```

Characteristic zero turns (10)--(11) into
`A_rB_v=B_rA_v=0`.  Since neither pair in (3) is zero, the two pairs lie on
the same coordinate axis.  Exchange the deficient labels to obtain (6).
Equations (8)--(9) now give the first two identities in (7), and substituting
them into (1), using (4), gives the third.  Nonzero `H` gives the final
nonvanishing statement. `square`

This step uses the complete same-source scalar hierarchy.  The pure `P_4`
equation alone does not imply (6)--(7).

## 2. Rank-three source hyperplanes

Let

```text
U_i=im L_i^* subseteq F^{ {P,Q,A,B} }                (12)
```

be the dual source rowspace of the local permanent map.  For `i=r,v`, it
is a hyperplane.  Under (6), `a_i` is outside `span{p_i,q_i}` while `b_i`
lies inside it.  Thus the one-dimensional kernel normal of `U_i` has zero
`A` coordinate:

```text
U_i=nu_i^perp,              nu_i in span{P,Q,B}.      (13)
```

The nonzero pure tensor belongs to the tensor product of the four local
images, so each target `c`-factor belongs to its corresponding local image.
At the rank-three ports, `L_i^*` identifies the three-dimensional physical
dual with `U_i`; the transported target-coordinate functional on `U_i` is
therefore nonzero.

At a silent port choose output rows `(c,o)`.  Its source plane is

```text
U_j=span{u_j,e_(rho_j)},
rho_j=Q for an X-oriented port,
rho_j=P for a Y-oriented port.                        (14)
```

The active pure-shore coefficient gives

```text
rho_j=Q  => u_j[P]!=0,
rho_j=P  => u_j[Q]!=0.                                (15)
```

Work in the squarefree algebra

```text
R=F[P,Q,A,B]/(P^2,Q^2,A^2,B^2),                      (16)
```

whose multiplication pairing `R_2 x R_2 -> R_4=F` is perfect.

### Lemma 3 (the rank-three hyperplanes coincide)

```text
U_r=U_v.                                               (17)
```

### Proof

Suppose the normals in (13) are independent.  Put
`S'=span{P,Q,B}` and write

```text
U_i=F A direct-sum V_i,       V_i=nu_i^perp subset S'. (18)
```

The two distinct planes `V_r,V_v` span `S'`, so

```text
A S' subseteq U_r U_v.                                (19)
```

The complement pairing identifies `A S'` perfectly with
`R_2(S')`.  Purity says that every coefficient with an off row at a silent
port vanishes for every choice of rows at `r,v`.  Equivalently, the
corresponding silent-off product annihilates the whole pair image
`U_rU_v`.  Since `A S' subseteq U_rU_v`, its `R_2(S')` component must
therefore vanish under the perfect pairing.

If the silent orientations are opposite, their two-off product is
`PQ in R_2(S')`, contradicting (19).  If both off rows are `Q`, the one-off
product `Q u_t` has the nonzero `u_t[P]PQ` component in `R_2(S')` by (15).
If both are `P`, the corresponding product has the nonzero
`u_t[Q]PQ` component.  In every case (19) detects a nonzero coefficient,
a contradiction.  Thus the normals are proportional and (17) follows.
`square`

## 3. The common normal has support at most two

At least three of the four ports lie in `E_c`, while only `s,t` are silent.
Hence at least one rank-three port is `c`-oriented.  Exchange the probes if
necessary and call it an `X`-oriented port.  There

```text
p_r=x_r c_r,              pi_c(row Y_r)=F^2.          (20)
```

The fixed vector `b_r` lies in the generic plane `span{p_r,q_r}` by
`B_r=0`.  Modulo `c_r`, a fixed vector cannot be proportional over the
fraction field to the generic two-direction vector `pi_c(q_r)`.  Hence

```text
b_r in F c_r.                                         (21)
```

The kernel relation at `r` consequently uses only source rows `P,B`.
The `B` coefficient is nonzero, since the active `P` shore is nonzero.
Scale the common normal from (17) to

```text
nu=tau P+B,              U_r=U_v=U=nu^perp.           (22)
```

Here `tau` is an arbitrary fraction-field scalar, including zero.  A
`Y`-oriented chosen port gives the probe-exchanged normal `tau Q+B`; all
arguments below are symmetric.  Because the `B` coefficient was proved
nonzero before scaling, this affine chart loses no projective
`tau=infinity` case.

## 4. Exact common-hyperplane annihilator

### Lemma 4 (no silent pair survives)

There are no two silent oriented planes (14)--(15) for which the restriction
of `P_4` by `U,U,U_s,U_t` is nonzero and pure on their declared `c` rows.

### Proof

First suppose `tau!=0`.  Put

```text
R_0=P-tau B,               S_0=P+tau B.               (23)
```

Then

```text
U=span{Q,A,R_0},
UU=span{QA, PQ-tau QB, PA-tau AB, PB}.                (24)
```

Direct use of the complementary-pairing basis gives

```text
(UU)^perp=span{Q S_0,A S_0}.                          (25)
```

Every silent-off product must lie in (25).  On the other hand, the
all-`c` silent product restricts the source to a bilinear form on
`U_r x U_v`.  Because the rank-three maps `L_r^*,L_v^*` are isomorphisms
from their three-dimensional physical dual spaces onto these hyperplanes,
the nonzero pure target says that this form is exactly a nonzero scalar
multiple of the outer product of the two transported target-coordinate
functionals at `r,v`; in particular it has rank one.

If both silent off rows are `Q`, comparison of the `PQ,QA,QB` coordinates
in `Q u_j in (UU)^perp`, together with (15), gives

```text
u_j in span{Q,S_0},             j=s,t.                (26)
```

Modulo the annihilator (25), their product is a nonzero multiple of

```text
S_0^2=2tau PB.                                        (27)
```

The bilinear form on `U x U` obtained by pairing with `PB` reads the `QA`
coefficient.  In the basis `(Q,A,R_0)` it has matrix

```text
[0 1 0; 1 0 0; 0 0 0],                              (28)
```

of rank two.  The two rank-three target factors require rank one, a
contradiction.

If both silent off rows are `P`, then `P u_j` has only `PQ,PA,PB`
coordinates.  Membership in (25) with `tau!=0` forces it to be zero, but
its `PQ` coefficient is the nonzero active value `u_j[Q]`.  If the
orientations are opposite, the two-off product `PQ` does not lie in (25).
Thus all three orientation types are impossible when `tau!=0`.

Now let `tau=0`.  Then

```text
U=span{P,Q,A},
UU=(UU)^perp=span{PQ,PA,QA}.                          (29)
```

For either off row `P` or `Q`, the one-off condition forces the `B`
coordinate of the other silent `c` row to vanish.  Hence
`u_s,u_t in U` and `u_su_t in UU`.  But `UU` is totally isotropic for the
complement pairing: every complementary degree-two monomial uses `B`.
The purported all-`c` target coefficient is therefore zero, again a
contradiction. `square`

The proof retains zero coefficients in the silent `c` rows.  It uses only
the nonzero active entries in (15) and does not localize at an individual
raw port edge.

## 5. Eta-zero and exactly-two-deficient exclusion

### Theorem 5 (`GLS66`)

The complete `GLS65` eta-zero `2,2,3,3` residual is empty.

### Proof

Lemmas 1--2 give the common active-side scalar normal form.  Lemmas 3--4
then contradict the separated nonzero pure `P_4` identity. `square`

### Corollary 5.1

There is no complete zero-anchor root-order-three all-six-rigid witness with
exactly two deficient joint probe maps.

Indeed `GLS64` excludes the locus `eta!=0`, while Theorem 5 excludes
`eta=0` after the exhaustive `GLS65` local-rank localization.

## 6. Sharp scope and next parent obligation

The argument uses all of the following:

```text
exactly two deficient maps with common kernel K e_c;
four remaining ports injective and nonaxis;
|E_c| in {3,4};
the full GLS64 pair/cofactor hierarchy and H!=0;
the GLS65 separated P_4 identity and exact 2233 rank profile. (30)
```

It does not extend silently to three or more deficient maps.  There the
kernel-support incidence, number of surviving ports, target colour support,
and effective permanent order all change.  The next top-down parent is the
complete three-plus-deficient branch of the mixed-kernel hierarchy, followed
separately by attachment and nonzero-anchor obligations.

## 7. Exact frontier

```text
GLS65 eta-zero local profile 2233:                    EXCLUDED;
GLS63 exactly-two-deficient branch:                   EXCLUDED;
zero-anchor r=3 all-six-rigid deficient floor:        at least 3;
three-or-more-deficient profiles:                     OPEN;
unique-nonrigid / alternate receiver:                 OPEN;
response/selector/synchronization/activity package:   OPEN;
nonzero-anchor and arbitrary-root strategic node:     OPEN;
global Krenn-Gu conjecture:                           UNRESOLVED. (31)
```

## 8. Verification boundary

The primary verifier replays the scalar-axis identities, common-hyperplane
product/annihilator formulas, and rank-two target slice.  The independent
standard-library audit performs finite-field censuses of the scalar
hierarchy and every physically aligned silent-orientation pair for the
common hyperplane.  These scripts audit finite and displayed algebraic
leaves; the same-source hierarchy, fraction-field rowspace, and purity
bridges above remain the written proof.

From repository root run:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_scalar_axis_and_common_hyperplane_exclusion.py
```
