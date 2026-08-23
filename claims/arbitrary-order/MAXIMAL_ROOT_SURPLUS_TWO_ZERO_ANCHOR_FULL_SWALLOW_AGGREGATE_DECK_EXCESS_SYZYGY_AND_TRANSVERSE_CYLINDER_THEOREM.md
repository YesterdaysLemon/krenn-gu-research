# Maximum-root surplus-two zero-anchor full-swallow aggregate deck, excess-syzygy, and transverse-cylinder theorem

## Status and scope

**Exact characteristic-zero arbitrary-root pointwise reduction and abstract
sharpness theorem.**  Fix one `GLS8`-eligible `(Q,A)` chart, one fully
supported residual contraction, and the zero-anchor full-swallow branch of
`GLS35`--`GLS39`.  If

```text
B=B_Q^anc=im sigma_Q,             k=dim B,
S=Delta+Kq,                       s=dim S,
```

then the complete fixed-residual target equation has aggregate incidence
image inside the at-most-four-dimensional space `S`.  It admits an exact
all-port-test lift through `ker sigma_Q`.  The pullbacks of rows in
`Ann(S)`, canonically dual to `B/S`, form a `k-s` excess-syzygy module: they
are nonzero on the labelled incidence family but vanish after the
complementary physical decks are aggregated.  They annihilate `q` and all
three pure probe tensors, so they are not legal anchor or target selectors.

On `D(p)`, the transverse image `P_Q(B)=N_empty^tr` has dimension `k-1`.
Every promoted pair desired tensor, its complete transverse nuisance, and
its three pure target columns lie in the corresponding `9(k-1)`-dimensional
cylinder.  This reduces legal survival exactly to that cylinder, but does
not force survival, response, synchronization, activity, or a receiver for
the row.

An exact rational six-label control has `k=6`, `s=4`, aggregate rank four,
two excess syzygies, full swallow, and the complete fixed-residual target
identity on every port word.  Its complementary-deck forms are specified as
an abstract labelled interface; they are not proved to be simultaneous
principal permanents of one physical graph.  Thus the control is a sharp
no-go for fixed-residual incidence/deck linear algebra, not a hypothetical
witness or counterexample.

This is `GLS40`.  It does not exclude any remaining rank `4,...,9` fibre,
force the silent source branch into full swallow, supply a legal downstream
package, or close the strategic node.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## Dependencies and provenance

The owning interfaces are:

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  for the promoted target family and legal selector criterion;
- [`GLS22`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md)
  and [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md)
  for `P_Q`, complete transverse nuisances, and target coupling;
- [`GLS35`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RAW_ROOT_DECK_QUOTIENT_AND_OUTPUT_COEFFICIENT_SEPARATION_NO_GO_THEOREM.md)
  for `B_Q^anc`, full swallow, and `P_Q(B)=N_empty^tr`;
- [`GLS36`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_THEOREM.md)
  for `B=im sigma_Q`, the labelled deck map `rho_Q`, and the fixed-residual
  target equation; and
- [`GLS39`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_COMPLETE_PAIRWISE_DIAGONAL_FAMILY_RANK_BOUND_AND_MINIMAL_RAW_SWALLOW_EXCLUSION_THEOREM.md)
  for the universal full-swallow floor `k>=4`.

No external literature claim is used.  The new content is the all-test
kernel lift, the canonical excess module and its exact dimension, the
rank-stratified transverse cylinder, and the exact abstract sharpness
control.

## 1. Aggregate deck image and all-test lift

Let

```text
E=E_A^*=V_(a_0)^* tensor V_(a_1)^*,
Delta=span{r_0,r_1,r_2},
Z=tensor_(u in Uhat) V_u,
ell_c=(e_c^*)^(tensor |Uhat|) in Z^*,
H=H_Uhat in Z^*.
```

Every residual-torus scalar `alpha_c` is nonzero.  Retain the incidence map
and complete labelled deck map

```text
sigma=sigma_Q:L_Q -> E,             rho=rho_Q:Z -> L_Q.
```

Define the aggregate incidence/deck map

```text
J_Q=sigma compose rho:Z -> E.                         (1)
```

The notation `J_Q` is deliberate: `GLS35` already uses `A_Q` for the formal
projection onto the residual-absent deck label.

### Theorem 1 (exact aggregate image and all-test kernel lift)

The complete fixed-residual target equation is exactly

```text
q tensor H+J_Q=sum_(c=0)^2 alpha_c r_c tensor ell_c. (2)
```

On full swallow, put

```text
B=im sigma,
S=Delta+Kq subset B.                                 (3)
```

Then

```text
im J_Q subset S,                 rank J_Q<=4.         (4)
```

Choose arbitrary lifts

```text
v,v_c in L_Q,
sigma(v)=q,                     sigma(v_c)=r_c.       (5)
```

For every `z in Z`, not only every mixed test,

```text
rho(z)+H(z)v-sum_c alpha_c ell_c(z)v_c in ker sigma. (6)
```

Changing any lift in (5) changes the left side of (6) by a
`ker sigma`-valued map.  On the mixed test space, every `ell_c` vanishes and
(6) is exactly the `GLS36` mixed lift.

#### Proof

Equation (2) is `GLS36` equation (17), with the two sides regarded as linear
maps from `Z` to `E`.  Rearranging proves (4).  Applying `sigma` to the left
side of (6) gives `J_Q+q tensor H-sum_c alpha_c r_c tensor ell_c`, which is
zero by (2).  Two choices of any lift differ by `ker sigma`. `square`

### Corollary 1.1 (exact aggregate rank)

If `q notin Delta`, then

```text
rank J_Q=dim span{H,ell_0,ell_1,ell_2}
        =3 if H in span{ell_0,ell_1,ell_2},
         4 otherwise.                                (7)
```

If `q in Delta`, write uniquely

```text
q=sum_c beta_c r_c.
```

Then

```text
rank J_Q=dim span{alpha_c ell_c-beta_c H:c=0,1,2}
        in {2,3}.                                     (8)
```

These formulas include `H=0`, `q=0`, diagonal silence, and every rank or
divisor fibre.  They divide by no response, coefficient, or minor.

#### Proof

If `q notin Delta`, the four output vectors `q,r_0,r_1,r_2` are independent,
so (2) identifies the rank with the span of their four coefficient
functionals.  The three pure words are independent, proving (7).  If
`q in Delta`, substitute its diagonal coordinates into (2).  The three
coefficient rows in (8) are a rank-three diagonal map minus a rank-at-most-one
map, so their rank is at least two and at most three. `square`

## 2. Canonical excess-syzygy module

For a subspace `R subset E`, write

```text
Ann(R)={lambda in E^*:lambda(R)=0}.
```

Let `sigma^*:E^* -> L_Q^*` be pullback and define

```text
E_Q^exc=sigma^*(Ann(S)) subset L_Q^*.                 (9)
```

### Theorem 2 (exact excess dimension and aggregate cancellation)

Let `k=dim B` and `s=dim S`.  Then

```text
dim E_Q^exc=k-s,
s=3 if q in Delta,
s=4 if q notin Delta.                                (10)
```

Every `theta in E_Q^exc` satisfies

```text
theta compose rho=0.                                 (11)
```

A nonzero `theta` is nonzero on at least one labelled summand of `L_Q`, but
every representing `lambda in Ann(S)` obeys

```text
lambda(q)=lambda(r_0)=lambda(r_1)=lambda(r_2)=0.      (12)
```

Thus these are exact labelwise incidence rows lost by aggregate deck
coupling.  They cannot normalize the raw `q` anchor or a pure target row.

#### Proof

Because `S subset B=im sigma`, the kernel of `sigma^*` restricted to
`Ann(S)` is `Ann(B)`.  Rank--nullity gives

```text
dim E_Q^exc=dim Ann(S)-dim Ann(B)=(9-s)-(9-k)=k-s.
```

For `theta=sigma^*(lambda)` with `lambda in Ann(S)`, equations (1) and (4)
give `theta rho=lambda J_Q=0`.  A nonzero functional on the direct sum `L_Q`
has a nonzero labelled component, while (12) is the definition of `Ann(S)`.
`square`

Together with `GLS39`, the full-swallow rank fibres split exactly as

```text
q notin Delta, k=4:       E_Q^exc=0;
q notin Delta, k>=5:      dim E_Q^exc=k-4;
q in Delta,     k>=4:     dim E_Q^exc=k-3.            (13)
```

This is an exhaustive reduction, not an exclusion of any line of (13).

## 3. Exact transverse cylinders on `D(p)`

Assume now

```text
p=epsilon_A(q)!=0,
P_Q=p id_E-q tensor epsilon_A.                        (14)
```

Put

```text
C_Q=P_Q(B).
```

### Theorem 3 (rank-stratified complete target cylinder)

Pointwise on every full-swallow fibre in `D(p)`,

```text
C_Q=N_empty^tr,                  dim C_Q=k-1.         (15)
```

For every promoted pair target `C subset Uhat`, `|C|=2`,

```text
t_C in C_Q tensor V_C^*,
N_C^tr subset C_Q tensor V_C^*,
d_(C,c)^tr in C_Q tensor V_C^*    for c=0,1,2.       (16)
```

Consequently,

```text
t_C notin N_C^tr
```

in the full transverse target space if and only if the same survival holds
inside the cylinder `C_Q tensor V_C^*`.  Since `dim V_C^*=9`, its dimensions
for `k=4,...,9` are

```text
27,36,45,54,63,72.                                  (17)
```

Moreover,

```text
q notin Delta:
  dim P_Q(Delta)=3,
  dim C_Q/P_Q(Delta)=k-4;

q in Delta:
  dim P_Q(Delta)=2,
  dim C_Q/P_Q(Delta)=k-3.                            (18)
```

The rank-four cylinder is therefore either the pure projected three-plane
or a projected pure two-plane plus one extra line.  It is not the `GLS25`
27-row double-transverse module, whose owning hypothesis is `omega!=0`;
here `omega=0` and the promoted top desired tensor is zero.

#### Proof

`GLS35` gives `P_Q(B)=N_empty^tr`.  On `D(p)`, `ker P_Q=Kq`; full swallow
puts this line inside `B`, proving `dim C_Q=k-1`.

For a pair label `C`, every coefficient slice of its raw tensor `g_C` lies in
`B`, so `t_C=(P_Q tensor id)g_C` lies in the first space in (16).  The exact
`GLS23` nuisance formula is labelwise.  Its top-anchor term vanishes because
`omega=0`; the `D=Q` term is killed by `P_Q`; and every remaining coefficient
slice lies in `P_Q(B)`.  This proves the nuisance containment.  Full swallow
puts each `r_c` in `B`, proving the pure-column containment.  Since both the
desired tensor and nuisance lie in the cylinder, inclusion induces an
injective map on the one desired class, giving the survival equivalence.

Finally, if `q notin Delta`, `P_Q` is injective on `Delta`.  If
`q in Delta`, its restriction has kernel `Kq`.  Subtract these dimensions
from (15) to obtain (18). `square`

The theorem does not say that any desired class in (16) survives or has a
nonzero response.  At `p=0`, the aggregate and excess results remain valid,
but the `GLS22` projector equivalence and this cylinder statement are not
available.

## 4. Exact abstract rank-six sharpness control

Work over `K=Q`.  Use residual labels `q_0,q_1` with one-dimensional domains
and four ternary port labels `u_0,u_1,u_2,u_3`.  Assign colours

```text
c(q_0)=c(u_0)=0,
c(q_1)=c(u_1)=1,
c(u_2)=c(u_3)=2.                                    (19)
```

For a residual label of colour `c`, put

```text
X_t(lambda)=Y_t(lambda)=lambda e_c.
```

For a port label of colour `c`, put

```text
X_t(z)=Y_t(z)=z_c e_c.                               (20)
```

The residual pair is

```text
q=mu_(q_0,q_1)(1 tensor 1)=E_01+E_10.               (21)
```

Exclude that pair from `sigma` exactly as in `GLS36`, and include every
one-residual and port--port pair.  Then

```text
B=im sigma=Sym_3,
k=6,
Delta+Kq subset B,
s=4.                                                 (22)
```

Let `x_(j,c)` denote the `c`-coordinate functional on `u_j`.  Set

```text
H=x_(0,0)x_(1,1)x_(2,0)x_(3,0).                     (23)
```

Declare the following evaluated complementary-deck forms and set every other
one to zero:

```text
h_(u_0,u_1)=-x_(2,0)x_(3,0),
h_(q_0,u_0)=(1/2)x_(1,0)x_(2,0)x_(3,0),
h_(q_1,u_1)=(1/2)x_(0,1)x_(2,1)x_(3,1),
h_(u_2,u_3)=(1/2)x_(0,2)x_(1,2).                    (24)
```

Take `alpha_0=alpha_1=alpha_2=1`.  Direct substitution gives, on every one
of the `3^4` port words,

```text
sigma rho
 =-q tensor H+r_0 tensor ell_0+r_1 tensor ell_1+r_2 tensor ell_2. (25)
```

Hence the complete fixed-residual target equation (2) holds exactly, with

```text
rank J_Q=4,                      dim E_Q^exc=2.       (26)
```

If `epsilon_A` is evaluation at the all-ones probe vectors, then `p=2`, so
the control also lies in `D(p)` and `dim P_Q(B)=5`.

### Theorem 4 (fixed-residual incidence/deck data do not exclude full swallow)

The data (19)--(24) satisfy (21)--(26) exactly.  Therefore full swallow, the
complete fixed-residual aggregate target identity, maximal aggregate rank
four, and nonzero excess syzygies are mutually consistent at the typed
label/deck level.

The deck forms (23)--(24) are assigned independently.  No assertion is made
that they are principal permanents of one graph, remain compatible over the
whole residual family, satisfy a `GLS4` maximum-root source package, or have
the required physical responses.  The control is not a graph, not a witness,
and not a counterexample to the conjecture.

#### Proof

Pairs of equal colours in (19)--(20) generate the three diagonal matrices;
pairs of different colours generate the three symmetric off-diagonal
matrices.  The pair `Q` is omitted, but other `0`--`1` pairs retain its
off-diagonal line, proving (22).  The pair `(u_0,u_1)` with its first deck in
(24) contributes `-q tensor H`.  The next two pairs contribute
`r_0 tensor ell_0` and `r_1 tensor ell_1`; the factor `1/2` cancels the two
equal rank-one summands.  The last pair similarly contributes
`r_2 tensor ell_2`.  This proves (25).  The four coefficient tensors in
(25) are independent, while (10) gives the excess dimension. `square`

## 5. Exact rank-five polarization/mixed boundary

There is also a lower-rank control which retains exact whole-domain
polarization and the mixed lift but necessarily fails the pure target.
Over `Q`, take two active promoted labels `u,v` with ternary domains and

```text
X_u=[[ 0, 0, 0],       Y_u=[[-1, 0, 1],
     [ 1, 1, 0],             [ 0, 0, 0],
     [-1, 0, 1]],            [ 0, 0, 0]],

X_v=[[ 1, 1, 0],       Y_v=[[ 0, 0,-1],
     [ 0, 0, 0],             [ 0, 1, 0],
     [ 0,-1, 1]],            [ 0, 0, 1]].             (27)
```

Set both residual-label maps and every other port incidence map to zero, so
`q=0`, and retain `omega=0` from the document-wide zero-anchor scope.  The
sole nonzero incidence block is `mu_(u,v)`, and exact elimination
gives

```text
im mu_(u,v)
 =Delta+K(E_12-E_10)+K(E_20-E_21),
rank B=5.                                             (28)
```

Explicit diagonal witnesses are

```text
mu(e_0,e_0)=-r_0,
mu(e_1,e_1)= r_1,
mu(e_2,e_2)= r_2.                                    (29)
```

The annihilator of (28) is

```text
span{E_01,E_02,E_10+E_12,E_20+E_21}.                 (30)
```

If a prospective third-label vector is
`z=(x_0,x_1,x_2,y_0,y_1,y_2)`, requiring its pairings with every vector of
both active label spaces to remain in (28) gives `24` homogeneous linear
equations of rank six.  One independent `6 x 6` subsystem has determinant
`-1`.  Hence every compatible third label map is zero over every field.

Type `u,v` as two of the at least four promoted ports and set every internal
edge on `Bhat` to zero.  Then every complementary deck, `H`, and `rho` vanish.
The exact mixed equation and kernel lift hold for every residual choice, but
the pure target fails.  Even if one allows an arbitrary sole complementary
deck `h_(u,v)`, the raw tensor is

```text
mu_(u,v) tensor h_(u,v),
```

which has flattening rank one across `(A,u,v)|(remaining ports)`, while the
ternary GHZ target has rank three across the same cut.

### Theorem 5 (rank five is algebraically real but pure-deck false)

Equations (27)--(30) give an exact rank-five full-swallow incidence family
with `q=0`, exact whole-domain polarization, no compatible third active
label, and every mixed `GLS36` equation.  It cannot satisfy the complete
pure target equation because of the rank-one/rank-three flattening gap.

This proves that whole-domain polarization, full-swallow membership, and the
mixed lift alone cannot exclude rank five.  It does not classify every
rank-five family; in particular, the two-active-label rigidity of this
control is not asserted universally.

#### Proof

Direct multiplication of (27) gives (28)--(29).  Pairing with the four rows
in (30) gives zero, and their independence plus the five-dimensional image
proves equality.  Applying the same four rows to all six pairings of a third
vector with bases of `u` and `v` gives the stated full-rank system, hence the
maximality claim.  The deck-zero mixed identity is immediate.  A single
tensor product has flattening rank one, while the three pure GHZ summands
give three independent rows and columns. `square`

## 6. Frontier and unresolved remainder

```text
aggregate deck image lies in Delta+Kq:                   PROVED;
all-test ker(sigma) lift:                                PROVED;
canonical excess dimensions k-3 or k-4:                  PROVED;
rank-stratified p!=0 transverse cylinders:               PROVED;
typed fixed-residual rank-six sharpness control:          PROVED;
rank-five full-swallow polarization/mixed control:         PROVED;
rank-five control satisfies the pure target:               FALSE;
rank-six deck assignment comes from one matching graph:   NOT CLAIMED;
rank-four through rank-nine full-swallow fibres:           OPEN;
target survival / response / synchronization / activity:  OPEN;
silent p=0 source cover and raw escape attachment:         OPEN;
strategic-node closure:                                   OPEN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

The smallest remaining full-swallow obligation is now explicitly
labelwise: use simultaneous principal-permanent compatibility over the same
physical graph and the full residual family to contradict every excess
branch in (13), or force one target-specific escape with nonzero response and
a complete legal package inside (16).  The zero-excess rank-four,
`q notin Delta` branch requires its own physical analysis.  The abstract
control proves that one fixed aggregate equation cannot perform this step.

## Verification boundary

Run the focused exact primary verifier:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_full_swallow_aggregate_deck_excess_syzygy_and_transverse_cylinder.py
```

Run the genuinely independent no-import audit:

```text
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_full_swallow_aggregate_deck_excess_syzygy_and_transverse_cylinder.py
```

The primary uses SymPy to replay the aggregate-rank formulas, excess
dimensions, cylinder dimensions, all `81` port words of the rank-six
control, and the rank-five compatibility/flattening boundary.  The audit
imports no project module or third-party package; it uses independent
rational elimination, dense rational tuples, and sparse word-by-word
evaluation.  The
arbitrary-root statements are the written linear-algebra proofs above, not a
finite search.
