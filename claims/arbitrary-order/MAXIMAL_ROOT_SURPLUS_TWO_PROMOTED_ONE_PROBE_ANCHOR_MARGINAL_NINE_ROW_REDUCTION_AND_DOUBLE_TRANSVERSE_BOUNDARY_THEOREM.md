# Maximum-root surplus-two promoted one-probe anchor marginal, nine-row reduction, and double-transverse boundary

## Status

**Exact characteristic-zero arbitrary-root physical-module reduction.**  On
the nonzero top-anchor branch of `GLS23`, contraction at either one of the two
actual probe-root vectors maps the eight-dimensional transverse root space
onto the two-dimensional annihilator of the other probe root.  If the
corresponding partial contraction of the top anchor is nonzero, wedging by
that anchor marginal gives a canonical denominator-free one-dimensional root
quotient.  Tensoring with a promoted pair complement produces an exact
`9`-row physical nuisance module.

Thus every promoted pair target has a common-anchor marginal route

```text
72 transverse rows -> 63 anchor-quotient rows -> 9 marginal rows. (1)
```

Survival in the last quotient is exactly the existence of a legal `GLS8`
selector whose coefficient functional factors through this route.  The
complete GHZ target identity, pure-rank trichotomy, and every nuisance-rank
drop descend exactly.  This is a sufficient selector route, not an
equivalence with arbitrary `63`-row or `72`-row survival.

The anchor alternatives are exhaustive and pointwise:

1. the anchor is zero;
2. it is nonzero and at least one probe-root marginal is nonzero, giving the
   common `9`-row family above; or
3. it is nonzero and both probe-root marginals vanish, so it lies in the
   four-dimensional double-transverse core.

At root order three, simultaneous usefulness of the six `9`-row pair
quotients, usefulness of the top target, and the existing three-colour
activity gate supply the exact legally attached `GLD3` window and are
therefore impossible on a hypothetical witness.  None of those hypotheses is
forced here.  The zero anchor, double-transverse anchor, marginal absorption,
response-zero, top absorption, and low-activity branches remain open.  No
named committed detector accepts the arbitrary-order high-depth rows by this
theorem alone.  The strategic node and the global Krenn--Gu conjecture remain
**UNRESOLVED**.

## Dependencies and provenance

The promoted target family, exact constant-selector criterion, and physical
responses come from

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md).

The transverse projector, complete-target quotient, source aggregate, and
all-rank failure criterion come from

- [`GLS22`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md).

The complete physical nuisance slices and common top anchor come from

- [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md).

The root-order-three conditional contradiction uses exactly the declared
attachment and activity interface of

- [`GLD3`](TWO_RESIDUAL_PAIR_FOUR_PORT_DIAGONAL_INTERFERENCE_AND_CAMOUFLAGE_BOUNDARY_THEOREM.md).

No external literature claim is used.  The new content is the canonical
one-probe exact sequence, the denominator-free anchor wedge, its physical
label-slice module, the anchor-relative synchronization fork, and the precise
conditional `r=3` detector edge.

## 1. Canonical one-probe exact sequences

Retain the `GLS22`--`GLS23` notation

```text
A={a_0,a_1},
E_A^*=V_(a_0)^* tensor V_(a_1)^*,
epsilon_A=x_(a_0) tensor x_(a_1),
E_A^tr=ker epsilon_A,
omega=W_(a_0,a_1) in E_A^tr.                           (2)
```

For `i in {0,1}`, put `j=1-i` and

```text
L_j={ell in V_(a_j)^*:ell(x_(a_j))=0},
rho_i:E_A^tr -> L_j,
rho_0(v)=v(x_(a_0),-),
rho_1(v)=v(-,x_(a_1)).                                 (3)
```

Factor order is restored canonically after the contraction.

### Theorem 1 (one-probe transverse exact sequence)

For each `i`, `rho_i` is surjective and

```text
dim E_A^tr=8,       dim L_j=2,       dim ker rho_i=6. (4)
```

Equivalently,

```text
0 -> ker rho_i -> E_A^tr -> L_j -> 0                 (5)
```

is exact.

#### Proof

If `v in E_A^tr`, then

```text
rho_i(v)(x_(a_j))=epsilon_A(v)=0,
```

so the displayed codomain is correct.  Given `ell in L_j`, choose
`alpha in V_(a_i)^*` with `alpha(x_(a_i))=1`.  The tensor
`alpha tensor ell`, in the appropriate factor order, lies in `E_A^tr` and
maps to `ell`.  Hence `rho_i` is onto.  Rank--nullity gives (4)--(5).
`square`

Put

```text
u_i=rho_i(omega) in L_j.                               (6)
```

### Theorem 2 (exhaustive anchor-marginal trichotomy)

Exactly one of the following disjoint alternatives holds.

```text
Z: omega=0;

M: omega!=0 and u_0!=0 or u_1!=0;

D: omega!=0 and u_0=u_1=0.                            (7)
```

In branch `D`, with

```text
L_0=x_(a_0)^perp subset V_(a_0)^*,
L_1=x_(a_1)^perp subset V_(a_1)^*,
```

one has

```text
0!=omega in L_0 tensor L_1,                           (8)
```

and its `2 x 2` core matrix has rank one or two.

#### Proof

The three conditions in (7) are visibly disjoint and exhaustive.  The kernel
of contraction at `x_(a_0)` is `L_0 tensor V_(a_1)^*`; the kernel of
contraction at `x_(a_1)` is `V_(a_0)^* tensor L_1`.  Their intersection is
`L_0 tensor L_1`, proving (8).  A nonzero tensor in a tensor product of two
two-dimensional spaces has matrix rank one or two.  `square`

Branch `Z` is the zero-top-target branch of `GLS23`.  The rest of this theorem
works on branch `M`, one nonzero `u_i` at a time.  It never divides by a
coordinate of `u_i`.

## 2. Denominator-free common-anchor quotient

Fix `i` with `u_i!=0`.  Since `dim L_j=2`, define

```text
mu_i:E_A^tr -> wedge^2 L_j,
mu_i(v)=u_i wedge rho_i(v).                            (9)
```

### Theorem 3 (one-dimensional root quotient)

The map `mu_i` is surjective, has rank one and kernel dimension seven, and

```text
mu_i(omega)=0.                                        (10)
```

It therefore induces a surjection

```text
E_A^tr/K omega -> wedge^2 L_j                         (11)
```

whose source and target dimensions are seven and one.

#### Proof

The map `v -> u_i wedge v` on the two-space `L_j` has kernel `K u_i` and
one-dimensional image.  Compose it with the surjection `rho_i` from Theorem
1.  This proves the rank and kernel dimensions.  Equation (10) is
`u_i wedge u_i=0`, so (11) is well defined and onto.  No normalization or
division is used.  `square`

For a promoted pair complement `C subset Uhat`, `|C|=2`, let

```text
K_C^tr=E_A^tr tensor V_C^*,
t_C in K_C^tr,
N_C^tr subset K_C^tr                                  (12)
```

be the `GLS22` desired tensor and `GLS23` complete nuisance.  Define

```text
A_(C,i)=(wedge^2 L_j) tensor V_C^*,
r_(C,i)=(mu_i tensor id)(t_C),
M_(C,i)=(mu_i tensor id)(N_C^tr).                      (13)
```

Then

```text
dim A_(C,i)=1*3^2=9.                                  (14)
```

### Theorem 4 (exact physical nine-row nuisance)

Retain the `GLS23` data

```text
D_0=D intersect Uhat,
X=C intersect D_0,
Y=D_0-C,
Z=C-D_0,
a_D in E_A^tr tensor V_(D_0)^*.
```

Put

```text
b_(D,i)=(mu_i tensor id)(a_D)
          in (wedge^2 L_j) tensor V_(D_0)^*.          (15)
```

The complete marginal nuisance is exactly

```text
M_(C,i)=sum_(D in binom(Bhat,2), D!=C)
          Slice_Y(b_(D,i)) tensor V_Z^*.              (16)
```

The `D=Q` term and the projected top-anchor term are both zero.  No other
active label is removed.

#### Proof

Apply `mu_i` to the root factor of the exact `GLS23` decomposition.  Root
contraction commutes with coefficient slicing on the disjoint `D_0` factors,
so the image of each labelled space is exactly its summand in (16).  The
`D=Q` projected companion is already zero.  The top summand is
`K omega tensor V_C^*` and maps to zero by (10).  Linear image commutes with
the finite sum, proving equality rather than only containment.  `square`

### Theorem 5 (factor-through selector criterion)

The following are equivalent for a fixed pair target `C`.

1. There is a functional `lambda_bar in A_(C,i)^*` which annihilates
   `M_(C,i)` and satisfies `lambda_bar(r_(C,i))=1`.
2. `[r_(C,i)]!=0` in `A_(C,i)/M_(C,i)`.
3. There is a legal normalized full `GLS8` selector whose coefficient
   functional factors through `mu_i tensor id_(V_C^*)`.

#### Proof

Finite-dimensional separation gives `1 <=> 2`.  Pulling `lambda_bar` back
along `mu_i tensor id` annihilates the complete `GLS23` nuisance and
normalizes `t_C`, hence is legal by `GLS22` and `GLS8`.  Conversely, a
coefficient functional which factors through this map descends to
`lambda_bar`; legality gives the two displayed conditions.  `square`

This theorem does not say that every legal selector factors through the
nine-row map.  Failure in (13) can coexist with survival in the `63`-row or
full `72`-row quotient.

## 3. Complete-target coupling and all-rank failure

Let `d_(C,c)^tr`, `w_(S_C,c)`, `alpha_c`, and the physical response
`P_(S_C)(H;z_Q)` be as in `GLS22`.  Put

```text
d_(C,c)^i=(mu_i tensor id)(d_(C,c)^tr).                (17)
```

### Theorem 6 (marginal target trichotomy)

In `A_(C,i)/M_(C,i)`,

```text
sum_(c=0)^2 alpha_c [d_(C,c)^i] tensor w_(S_C,c)
 =[r_(C,i)] tensor P_(S_C)(H;z_Q).                    (18)
```

The marginal pure quotient has rank at most one, and the following are
equivalent.

1. `[r_(C,i)]!=0` and `P_(S_C)(H;z_Q)!=0`.
2. At least one marginal pure class `[d_(C,c)^i]` is nonzero.
3. The three marginal pure columns have rank exactly one.
4. A legal nonzero-response `GLS8` selector exists through the nine-row
   route.

#### Proof

Apply `mu_i tensor id` to the exact `GLS22` target identity.  The complete
nuisance maps to (16).  The right side is decomposable.  The three right pure
words remain independent and the residual coefficients `alpha_c` are units,
so the same rank-one argument as in `GLS22` proves all equivalences.  Theorem
5 supplies the legal selector.  `square`

Let `B_(C,i)(z)` present `M_(C,i)(z)` in the nine-row space and let

```text
D_(C,i)(z)=[d_(C,0)^i|d_(C,1)^i|d_(C,2)^i],
h(z)=H_Q(z),                    p(z)=p_(A,Q)(z).       (19)
```

Define

```text
U_(C,i)={z:
 h(z)p(z)!=0 and rank[B_(C,i)(z)|D_(C,i)(z)]
                  >rank B_(C,i)(z)}.                 (20)
```

### Theorem 7 (nine-row radical--Fitting criterion)

For fixed `C` and a fixed nonzero anchor marginal `u_i`, `U_(C,i)` is empty
if and only if, for every `1<=k<=9`,

```text
(h p) I_k([B_(C,i)|D_(C,i)])
  subset sqrt_geom(I_k(B_(C,i))).                     (21)
```

This includes every marginal nuisance-rank drop and response-zero fibre.

#### Proof

Theorem 6 identifies useful marginal attachment with augmented rank rise.
On the nuisance-rank-`k-1` stratum, rank rises exactly when every `k`-minor of
`B_(C,i)` vanishes and some augmented `k`-minor does not.  Intersect with the
common source gate `D(hp)` and apply the geometric Laurent Nullstellensatz.
No anchor coordinate, response coordinate, or minor is inverted.  `square`

## 4. Anchor-relative source synchronization

For the source Laplace pairs `C subset U`, retain

```text
tau_C=Per_(K_0,U-C),
T_Q=sum_C t_C tensor tau_C
   =p F_Q-q tensor Pi_Q.                              (22)
```

Put

```text
A_(Q,i)=(mu_i tensor id_(V_U^*))(T_Q)
       =sum_C r_(C,i) tensor tau_C.                   (23)
```

### Theorem 8 (marginal aggregate fork)

Exactly one of the following holds.

1. `A_(Q,i)!=0`; then at least one source-pair raw nine-row tensor
   `r_(C,i)` is nonzero.
2. `A_(Q,i)=0`; then

   ```text
   (rho_i tensor id)(T_Q) in K u_i tensor V_U^*.      (24)
   ```

For an individual source pair,

```text
r_(C,i)=0
 iff (rho_i tensor id)(t_C) in K u_i tensor V_C^*.   (25)
```

#### Proof

Equation (23) follows by linearity.  A nonzero sum has a nonzero summand.
The kernel of `v -> u_i wedge v` on `L_j` is exactly `K u_i`; applying this
to the root flattening proves (24)--(25).  `square`

The source facts `Pi_Q!=0` and `p!=0` do not decide this fork.  Raw
nonvanishing in alternative 1 is not quotient survival, while alternative 2
is an aggregate anchor-relative synchronization condition, not a termwise
one.

## 5. Root-order-three detector interface

Assume `r=3`.  Then `|Uhat|=4`.  For a pair complement `C`, the promoted
physical response is

```text
D_(Uhat-C)=H_(Q union (Uhat-C))(z_Q,-_(Uhat-C)),      (26)
```

and the top response is

```text
T=H_(Q union Uhat)(z_Q,-_Uhat).                       (27)
```

These are exactly the six residual-present pair responses and one
residual-present four-port response in the same physical `Q,z_Q,Uhat` window
of `GLD3`.

### Corollary 8.1 (conditional common marginal entry to GLD3)

Fix one `i` with `u_i!=0`.  Suppose, at one common fully supported residual
point with `h p!=0`, that

1. every one of the six pair targets has marginal pure quotient rank one in
   (18);
2. the promoted top target has transverse pure quotient rank one in `GLS22`;
   and
3. the resulting six physical pair responses satisfy the declared
   three-colour pair-depth activity of `GLD3`.

Then the six pulled-back marginal selectors and the top selector are legally
normalized, target-diagonal, and attached to the same physical window.
`GLD3` therefore exposes a nonzero actual mixed target coefficient, contrary
to the complete GHZ equations.  No hypothetical witness lies in this
conditional branch.

#### Proof

Theorem 6 supplies exact normalized selectors for all six named responses in
(26); the `GLS22` top rank-one condition supplies the exact selector for
(27).  All use the same graph, residual pair, residual point, and fixed port
bases.  Applying them to the GHZ tensor makes their outputs diagonal.  These
are precisely the attachment hypotheses of `GLD3`; hypothesis 3 is its
remaining activity gate.  Its nine-word determinant gives the stated mixed
coefficient contradiction.  `square`

This corollary does not promote individual nonzero responses to activity and
does not cover a different marginal choice for each target.  The one index
`i` is common to all six pair rows.

## 6. Proof-DAG consequence and open boundary

The promoted path is refined to

```text
GLS23 anchor split
 -> omega=0: top desired coefficient zero;
 -> omega!=0, u_0=u_1=0: nonzero double-transverse core;
 -> some u_i!=0:
      six/all pair targets admit common 9-row marginal tests
      + exact all-rank failure and aggregate synchronization forks. (28)
```

At `r=3`, the all-six-useful plus top-useful plus three-active leaf is now a
named existing detector contradiction.  The following remain **OPEN**:

```text
zero-anchor exclusion:                                      OPEN;
double-transverse-anchor exclusion:                         OPEN;
forcing one common nonzero anchor marginal:                  OPEN;
forcing all required nine-row pair survivals/responses:      OPEN;
forcing top survival and three-colour activity at r=3:       OPEN;
proper marginal nuisance-rank fibres:                        OPEN;
r>=4 named downstream detector package:                     OPEN;
strategic-node closure:                                     OPEN.
```

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 7. Verification

Run the focused exact primary verifier:

```bash
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_one_probe_anchor_marginal_nine_row_reduction_and_double_transverse_boundary.py
```

Run the independent no-import audit:

```bash
python claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_one_probe_anchor_marginal_nine_row_reduction_and_double_transverse_boundary.py
```

The scripts replay the one-probe exact sequence, wedge quotient, anchor
trichotomy, exact image/slice commutation, `72 -> 63 -> 9` dimensions,
rank-rise selector criterion, aggregate synchronization kernel, and the
root-order-three response-window identification.  The arbitrary-root result
is the written tensor argument above.
