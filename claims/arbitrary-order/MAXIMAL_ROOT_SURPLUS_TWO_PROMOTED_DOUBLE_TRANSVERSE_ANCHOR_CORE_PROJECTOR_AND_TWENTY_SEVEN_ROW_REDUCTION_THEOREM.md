# Maximum-root surplus-two promoted double-transverse anchor core projector and twenty-seven-row reduction

## Status

**Exact characteristic-zero arbitrary-root physical-module reduction.**  This
theorem treats the nonzero double-transverse top-anchor branch left by
`GLS24`.  The retained all-port companion `q` and its nonzero scalar
`p=epsilon_A(q)` canonically split the eight-dimensional transverse probe-root
space.  A denominator-free operator projects it onto the four-dimensional
double-transverse core and satisfies the same scaled-idempotent relation as
the earlier transverse projector.

On the branch where the nonzero top anchor `omega` lies in that core, wedging
the projected root tensor by `omega` gives a three-dimensional root quotient.
Every promoted pair target therefore has an exact physical `27`-row
factor-through nuisance module:

```text
72 transverse rows -> 63 anchor-quotient rows -> 27 core rows. (1)
```

The promoted top target has a separate exact four-row core test whose desired
coefficient is `p^2 omega`.  Complete-target pure rank, response gating, every
nuisance-rank fibre, and an anchor-relative source synchronization fork
descend exactly.  Pair or top survival in these reduced modules supplies a
legal full `GLS8` selector; failure is not equivalent to failure in the full
`63/72`- or eight-row quotients.

Together, `GLS24` and this theorem give bounded physical factor-through tests
on every **nonzero** anchor point: `9` rows when an actual-root anchor marginal
is nonzero, and `27/4` pair/top rows on the nonzero double-transverse branch.
They do not force any reduced class to survive.

At root order three, simultaneous usefulness of the six `27`-row pair
modules, usefulness of the four-row top module, and the existing three-colour
activity gate enter `GLD3` and are impossible on a hypothetical witness.
The zero-anchor branch, every reduced or full absorption/response-zero fibre,
low activity, and every arbitrary-order downstream-shape obligation remain
open.  The strategic node and the global Krenn--Gu conjecture remain
**UNRESOLVED**.

## Dependencies and provenance

The promoted physical target family and legal constant-selector criterion
come from

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md).

The retained all-port tensor `q`, nonzero scalar `p`, exact transverse
quotient, target identity, and source aggregate come from

- [`GLS22`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md).

The complete physical nuisance formula and common top anchor come from

- [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md).

The exhaustive anchor-marginal split and identification of the nonzero
double-transverse branch come from

- [`GLS24`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ONE_PROBE_ANCHOR_MARGINAL_NINE_ROW_REDUCTION_AND_DOUBLE_TRANSVERSE_BOUNDARY_THEOREM.md).

The root-order-three conditional contradiction again uses exactly the
declared attachment and activity interface of

- [`GLD3`](TWO_RESIDUAL_PAIR_FOUR_PORT_DIAGONAL_INTERFERENCE_AND_CAMOUFLAGE_BOUNDARY_THEOREM.md).

No external literature claim is used.  The new content is the canonical
denominator-free double-transverse projector, its exterior anchor quotient,
the exact `27/4` physical modules, and their source/target interfaces.

## 1. The canonical double-transverse projector

Retain

```text
A={a_0,a_1},
E_A^*=V_(a_0)^* tensor V_(a_1)^*,
epsilon_A=x_(a_0) tensor x_(a_1),
E_A^tr=ker epsilon_A,
q=G_Q^A(z_Q),                 p=epsilon_A(q)!=0.       (2)
```

Put

```text
L_0=x_(a_0)^perp subset V_(a_0)^*,
L_1=x_(a_1)^perp subset V_(a_1)^*,
E_A^dbl=L_0 tensor L_1,        dim E_A^dbl=4.          (3)
```

Use the `GLS24` marginal maps

```text
rho_0(v)=v(x_(a_0),-) in L_1,
rho_1(v)=v(-,x_(a_1)) in L_0.                          (4)
```

The two partial contractions of `q` are

```text
s_0=q(-,x_(a_1)) in V_(a_0)^*,
s_1=q(x_(a_0),-) in V_(a_1)^*,                        (5)
```

and satisfy

```text
s_0(x_(a_0))=s_1(x_(a_1))=p.                         (6)
```

Define the denominator-free operator

```text
Xi_Q:E_A^tr -> E_A^*,
Xi_Q(v)=p v-s_0 tensor rho_0(v)-rho_1(v) tensor s_1.  (7)
```

### Theorem 1 (double-transverse scaled projector)

The operator `Xi_Q` has image exactly `E_A^dbl`, rank four, and kernel

```text
ker Xi_Q=(K s_0 tensor L_1)+(L_0 tensor K s_1),       (8)
```

an internal direct sum of dimension four.  Moreover,

```text
Xi_Q|_(E_A^dbl)=p id,
Xi_Q^2=p Xi_Q.                                        (9)
```

Thus on `D(p)`, `p^(-1)Xi_Q` is the canonical projection associated with the
splittings

```text
V_(a_0)^*=K s_0 direct-sum L_0,
V_(a_1)^*=K s_1 direct-sum L_1.                       (10)
```

Equations (7)--(9), rather than (10), are the load-bearing denominator-free
form.

#### Proof

Contract (7) at `x_(a_0)`.  The three terms give

```text
p rho_0(v)-p rho_0(v)-rho_1(v)(x_(a_0))s_1=0,
```

because `rho_1(v) in L_0`.  The other contraction is symmetric.  Hence the
image lies in `E_A^dbl`.  If `v` already lies in the double-transverse core,
both `rho_i(v)` vanish and `Xi_Q(v)=pv`; since `p!=0`, the image is the whole
core and has rank four.  Equation (9) follows by applying this restriction to
the image.

Every tensor in the right side of (8) is killed by direct substitution.  The
sum is direct: a nonzero equality `s_0 tensor ell_1=ell_0 tensor s_1` would
make `s_0` proportional to an element of `L_0`, contradicting (6), and
similarly for `s_1`.  Its dimension is four, which equals the kernel dimension
by rank--nullity.  This proves (8).  The splittings (10) follow from (6) on
`D(p)`.  `square`

## 2. The double-transverse anchor quotient

Work now on branch `D` of `GLS24`:

```text
0!=omega=W_(a_0,a_1) in E_A^dbl.                     (11)
```

Theorem 1 gives

```text
Xi_Q(omega)=p omega.                                  (12)
```

Define

```text
Omega_omega=omega wedge E_A^dbl
             subset wedge^2 E_A^dbl,
dim Omega_omega=3,

chi_Q:E_A^tr -> Omega_omega,
chi_Q(v)=omega wedge Xi_Q(v).                         (13)
```

### Theorem 2 (three-dimensional anchored core quotient)

The map `chi_Q` is onto, has rank three and kernel dimension five, and kills
`omega`.  It induces a surjection

```text
E_A^tr/K omega -> Omega_omega                         (14)
```

from a seven-dimensional space to a three-dimensional space.

#### Proof

The map `w -> omega wedge w` on the four-space `E_A^dbl` has kernel
`K omega` and rank three.  Compose it with the surjective `Xi_Q`.  Equation
(12) gives `chi_Q(omega)=p omega wedge omega=0`.  The dimensions and induced
map follow.  No coordinate of `omega` or `p` is divided out.  `square`

## 3. Exact physical pair and top modules

For a promoted pair complement `C`, retain

```text
t_C in E_A^tr tensor V_C^*,
N_C^tr subset E_A^tr tensor V_C^*.                    (15)
```

Define

```text
A_C^dbl=Omega_omega tensor V_C^*,
r_C^dbl=(chi_Q tensor id)(t_C),
M_C^dbl=(chi_Q tensor id)(N_C^tr).                    (16)
```

Then

```text
dim A_C^dbl=3*3^2=27.                                 (17)
```

For the top target put

```text
A_empty^dbl=E_A^dbl,
r_empty^dbl=Xi_Q(t_empty)=p^2 omega,
M_empty^dbl=Xi_Q(N_empty^tr).                         (18)
```

The equality for the desired coefficient uses `t_empty=p omega` from
`GLS23`.

### Theorem 3 (exact physical `27/4` nuisances)

For an active complement pair `D`, use the `GLS23` tensor

```text
a_D in E_A^tr tensor V_(D_0)^*,       D_0=D intersect Uhat,
```

and define

```text
c_D=(chi_Q tensor id)(a_D)
       in Omega_omega tensor V_(D_0)^*,
e_D=(Xi_Q tensor id)(a_D)
       in E_A^dbl tensor V_(D_0)^*.                   (19)
```

For a pair target, with

```text
Y=D_0-C,                 Z=C-D_0,
```

the complete anchored-core nuisance is exactly

```text
M_C^dbl=sum_(D in binom(Bhat,2), D!=C)
          Slice_Y(c_D) tensor V_Z^*.                  (20)
```

For the top target,

```text
M_empty^dbl=span{
 Slice_(D_0)(e_D):D in binom(Bhat,2)}.                (21)
```

In (20), both the `D=Q` term and top-anchor nuisance are zero after `chi_Q`.
In (21), `D=Q` is zero after the prior transverse projection, and the top
label is desired rather than nuisance.  Every other active unwanted label is
retained.

#### Proof

Apply `chi_Q` or `Xi_Q`, respectively, to the root factor of the exact
`GLS23` labelled nuisance formula.  These root maps commute with every port
coefficient slice.  The pair-target top label is `K omega tensor V_C^*` and
is killed by `chi_Q`; (12) shows why the top desired label must instead use
the unwedged core map in (18).  Linear image commutes with the finite labelled
sum, proving the exact equalities.  `square`

### Theorem 4 (factor-through selector criteria)

For a pair target, the following are equivalent.

1. `[r_C^dbl]!=0` in `A_C^dbl/M_C^dbl`.
2. A separating functional on the `27`-row module normalizes `r_C^dbl` and
   annihilates `M_C^dbl`.
3. A legal normalized full `GLS8` selector exists whose coefficient
   functional factors through `chi_Q tensor id_(V_C^*)`.

For the top target, the same equivalence holds with the four-row data in
(18) and factorization through `Xi_Q`.

#### Proof

Finite-dimensional separation gives the first two formulations.  Pull back a
separating functional along the stated root map.  The exact nuisance
equalities (20)--(21) make the pullback annihilate every unwanted labelled
operator, and normalization gives the desired formal projection by the
`GLS8` criterion.  Conversely, a legal functional factoring through the root
map descends and separates the reduced desired class.  `square`

These are sufficient routes inside the full selector problem.  A class may
die after `chi_Q` or `Xi_Q` and still survive before that map.

## 4. Complete-target coupling and all-rank failure

For a pair target and colour `c`, put

```text
d_(C,c)^dbl=(chi_Q tensor id)(d_(C,c)^tr).             (22)
```

For the top target put

```text
d_(empty,c)^dbl=Xi_Q(d_(empty,c)^tr).                 (23)
```

Use `star=pair` or `star=empty` for the corresponding reduced data.

### Theorem 5 (double-transverse target trichotomy)

In `A_C^dbl/M_C^dbl`, the image of the complete `GLS22` target identity is

```text
sum_(c=0)^2 alpha_c[d_(C,c)^dbl] tensor w_(S_C,c)
 =[r_C^dbl] tensor P_(S_C)(H;z_Q).                    (24)
```

This holds for both pair and top targets, using (22) or (23).  In either case
the reduced pure quotient has rank at most one, and the following are
equivalent.

1. The reduced desired class and named physical response are both nonzero.
2. At least one reduced pure class is nonzero.
3. The three reduced pure columns have rank exactly one.
4. A legal nonzero-response full selector exists through the corresponding
   `27`- or four-row route.

#### Proof

Apply the relevant root map to the `GLS22` target identity and use Theorem 3
for its complete nuisance image.  The right side is decomposable; the pure
right words are independent and the residual `alpha_c` are units.  The
standard exact rank-one argument proves the equivalences, and Theorem 4 gives
the legal selector.  `square`

Let `B_C^dbl(z)` present the reduced nuisance, let `D_C^dbl(z)` be the three
reduced pure columns, and put

```text
k_C=27 for a pair target,        k_empty=4,
h(z)=H_Q(z),                     p(z)=p_(A,Q)(z).
```

Define the useful locus by

```text
U_C^dbl={z:
 h(z)p(z)!=0 and rank[B_C^dbl(z)|D_C^dbl(z)]
                  >rank B_C^dbl(z)}.                 (25)
```

### Theorem 6 (double-transverse radical--Fitting criterion)

For a fixed target on branch (11), `U_C^dbl` is empty if and only if, for
every `1<=k<=k_C`,

```text
(h p) I_k([B_C^dbl|D_C^dbl])
  subset sqrt_geom(I_k(B_C^dbl)).                     (26)
```

All reduced nuisance-rank drops and response-zero fibres are included.

#### Proof

Theorem 5 turns usefulness into augmented rank rise.  Stratify by nuisance
rank, intersect with `D(hp)`, and apply the geometric Laurent
Nullstellensatz exactly as in `GLS22` and `GLS24`.  No coordinate of `omega`,
`p`, a response, or a rank minor is inverted.  `square`

## 5. Double-transverse source synchronization

For the source Laplace aggregate

```text
T_Q=sum_(C subset U, |C|=2) t_C tensor tau_C
   =pF_Q-q tensor Pi_Q,                               (27)
```

put

```text
A_Q^dbl=(chi_Q tensor id_(V_U^*))(T_Q)
       =sum_C r_C^dbl tensor tau_C.                   (28)
```

### Theorem 7 (anchored-core aggregate fork)

Exactly one of the following holds.

1. `A_Q^dbl!=0`, so at least one source-pair raw `27`-row tensor is nonzero.
2. `A_Q^dbl=0`, in which case

   ```text
   (Xi_Q tensor id)(T_Q) in K omega tensor V_U^*.     (29)
   ```

For an individual source pair,

```text
r_C^dbl=0
 iff (Xi_Q tensor id)(t_C) in K omega tensor V_C^*.  (30)
```

#### Proof

Equation (28) is linear.  A nonzero sum has a nonzero summand.  The kernel of
`w -> omega wedge w` on `E_A^dbl` is exactly `K omega`, proving
(29)--(30).  `square`

Neither alternative gives quotient survival.  Alternative 2 is aggregate
core synchronization and is not termwise without the stronger equations
(30) for every source pair.

## 6. Root-order-three detector interface

At `r=3`, complementing the six pairs of the four-port set `Uhat` identifies
the six promoted pair targets with the six physical residual-present pair
responses, and the promoted top target with the physical residual-present
four-port response.

### Corollary 7.1 (conditional double-core entry to GLD3)

At one common fully supported residual point with `hp!=0`, assume branch
(11) and:

1. all six pair targets have reduced pure rank one in their `27`-row modules;
2. the top target has reduced pure rank one in its four-row core module; and
3. the six attached physical pair responses satisfy `GLD3` three-colour
   pair-depth activity.

Then the pulled-back selectors legally attach the exact six pair responses
and four-port response in one physical window.  `GLD3` exposes a nonzero mixed
target coefficient, contradicting the complete GHZ equations.  No
hypothetical witness lies in this conditional branch.

#### Proof

Theorem 5 supplies all seven exact normalized response selectors on the same
graph, residual pair, residual point, and port bases.  Their target outputs are
diagonal.  Hypothesis 3 supplies the remaining `GLD3` gate, whose nine-word
determinant is the stated contradiction.  `square`

## 7. Proof-DAG consequence and open boundary

The nonzero-anchor topology is now

```text
omega!=0
 -> some actual-root marginal nonzero:
      GLS24 common 9-row pair route;
 -> both actual-root marginals zero:
      GLS25 common 27-row pair route + 4-row top route. (31)
```

This is an exhaustive bounded **factor-through** reduction, not an exhaustive
selector or response theorem.  The following remain **OPEN**:

```text
zero-anchor exclusion:                                      OPEN;
forcing survival in any reduced or full pair module:         OPEN;
forcing top survival in the eight-row or four-row module:     OPEN;
forcing response nonvanishing and r=3 activity:               OPEN;
all reduced/full nuisance-rank exceptional fibres:            OPEN;
r>=4 named complete downstream detector:                     OPEN;
strategic-node closure:                                     OPEN.
```

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 8. Verification

Run the focused exact primary verifier:

```bash
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_double_transverse_anchor_core_projector_and_twenty_seven_row_reduction.py
```

Run the independent no-import audit:

```bash
python claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_double_transverse_anchor_core_projector_and_twenty_seven_row_reduction.py
```

The scripts replay the denominator-free projector, its exact image/kernel and
scaled idempotence, rank-one/rank-two double-core anchors, the exterior
quotient, `72 -> 63 -> 27` and `8 -> 4` dimensions, slice commutation,
rank-rise selector tests, aggregate synchronization, and the `r=3` response
window.  The arbitrary-root theorem is the written tensor proof above.
