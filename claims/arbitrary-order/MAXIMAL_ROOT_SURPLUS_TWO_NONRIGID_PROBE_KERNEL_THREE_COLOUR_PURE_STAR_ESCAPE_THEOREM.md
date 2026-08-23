# Maximum-root surplus-two probe-kernel pure-star flag and GLD3 activity no-go

## Status and scope

The global Krenn--Gu conjecture is **UNRESOLVED**.

This document proves `GLS56`, a probe-kernel refinement of the older
three-colour hyperplane-annihilation theorem.  Work in the complete promoted two-probe chart
of `GLS8`.  The probe labels are `A={a_0,a_1}` and the auxiliary labels are

```text
Bhat=Q disjoint-union Uhat,          |Bhat|=2r,       r>=3.
```

The conditional algebra below is valid over any characteristic-zero field
`K` once the complete identity is supplied.  The live maximum-root physical
source in this repository is over `K=C`; no broader source-existence
quantifier is being inferred.

For `n in Bhat`, put

```text
J_n:V_n -> V_(a_0)^* direct-sum V_(a_1)^*,
J_n(k)=(W_(a_0,n)(-,k),W_(a_1,n)(-,k)),              (1)
K_n=ker J_n.
```

Suppose that `n` is nonrigid in the sense of `GLS55`, so

```text
K_n intersect (K^*)^3 != empty.                       (2)
```

Then every fully supported `k in K_n` has the following pointwise escape:
for each target colour `c`, some auxiliary neighbour `t!=n` satisfies

```text
W_(n,t)(k,-) in K^* e_(t,c)^*.                        (3)
```

The three neighbours in (3) are distinct.  Uniformly on the whole linear
kernel `K_n`, for every colour `c` there is a fixed neighbour `t_c` such that

```text
0 != W_(n,t_c)(K_n,-) subset K e_(t_c,c)^*.           (4)
```

The fixed neighbours can again be chosen distinct, and one fully supported
`k in K_n` makes all three fixed shores in (4) nonzero simultaneously.
Every exceptional torus point is retained by a descending linear-section
flag of length at most `dim K_n`: at each stage one fixed neighbour is pure
and nonzero off the next section.  Thus rank-two, rank-one, and rank-zero
nonrigid kernels require at most one, two, and three strata per colour.

There is also an exact receiver warning.  If `n` and either old probe are
re-anchored as the two residual vertices of a `GLD3` four-port window, then
`h=0`.  If the three pair responses among the three pure-star neighbours are
target-diagonal, they are forced to be zero.  Hence every four-port
complementary pair-depth product through those three neighbours is zero.
The pure star does not merely fail to prove `GLD3` activity on this natural
re-anchoring; it forces that activity gate to fail.

This is a support-free, denominator-free consequence of the complete target
identity.  It is pointwise before any residual contraction and retains every
rank and divisor fibre.  It does not assume the zero-anchor equation
`W_(a_0,a_1)=0`; the top deck is killed by the same star contraction used in
the proof.

On the zero-anchor `r=3` branch, `GLS55` makes the consequence exhaustive:
either all six auxiliary labels are rigid, or there is a unique nonrigid
label and it has a simultaneous three-colour pure star into three of the
other five, all of which are rigid.  This is not a legal target selector or
a downstream attachment theorem.

## Dependencies and provenance

- `GLS8` owns the complete uncontracted two-probe identity and the physical
  matching-deck interpretation.
- `GLS55` is used only for the final zero-anchor `r=3` bifurcation.  The
  pure-star theorem itself needs no zero-anchor or five-rigid-label premise.
- [`THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md`](THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md)
  is the historical antecedent: it proves the unrestricted pointwise
  coordinate-killer mechanism and a generic fixed edge on the whole local
  space.  It does not prove that a fixed killer remains nonzero after
  restriction to `ker J_n`, retain exceptional kernel sections, or type the
  resulting star against `GLD3`.

The pointwise step below is a self-contained specialization of that older
mechanism.  The new steps are the nonzero fixed-edge refinement on `K_n`, its
complete exceptional-section flag, the `r=3` rigid-supported bifurcation,
and the exact `GLD3` activity no-go.  The proof contracts one probe-silent auxiliary label and then uses a
single chosen target colour to contract every remaining auxiliary label in
the kernel of its evaluated star shore.  Every physical matching deck then
dies through the silent label, while that target colour remains nonzero.

## 1. One-colour covector alternative

Let `V=K^3` have the declared target basis and let `ell in V^*`.  Fix a
colour `c`.

### Lemma 1 (coordinate covector or surviving kernel coordinate)

Exactly one of the following holds:

```text
ell in K^* e_c^*;
there is v in ker ell with v_c!=0.                    (5)
```

### Proof

If `ell=lambda e_c^*` with `lambda!=0`, every vector in its kernel has
`c`-coordinate zero.  Conversely, suppose that no vector in `ker ell` has a
nonzero `c`-coordinate.  Then

```text
ker ell subset ker e_c^*.
```

If `ell=0`, this containment is false.  Otherwise both kernels are
hyperplanes, so they are equal and `ell` is a nonzero multiple of `e_c^*`.
This proves (5).  `square`

No full-support vector is required in the second alternative.  Retaining
only the chosen `c`-coordinate is what makes the argument below colourwise.

## 2. Complete matching contraction

The complete `GLS8` identity is

```text
T_W(-_A,-_Bhat)
 =sum_(D in binom(Bhat,2)) G_D^A tensor H_(Bhat-D)
  +omega tensor H_Bhat,                               (6)
```

where `omega=W_(a_0,a_1)` may be zero or nonzero.  On a hypothetical
Krenn--Gu witness the right target tensor is

```text
sum_(c=0)^2 e_(a_0,c)^* tensor e_(a_1,c)^*
                    tensor tensor_(t in Bhat)e_(t,c)^*.   (7)
```

Fix

```text
k_n in K_n intersect (K^*)^3                         (8)
```

and a target colour `c`.

### Theorem 2 (pointwise three-colour pure-star escape)

There is a neighbour `t!=n` satisfying (3).  Doing this for the three target
colours gives three distinct neighbours.

### Proof

Suppose no neighbour satisfies (3) for the chosen colour.  For every
`t in Bhat-{n}`, apply Lemma 1 to

```text
ell_t=W_(n,t)(k_n,-).
```

Choose `k_t in V_t` with

```text
ell_t(k_t)=0,                  k_(t,c)!=0.             (9)
```

Evaluate (6) at all auxiliary vectors `k_t`, leaving the two probe slots
open.

If `n in D`, the companion `G_D^A` is zero because both probe incidences of
`n` vanish at `k_n`.  If `n notin D`, the deck `H_(Bhat-D)` contains `n`.
Every perfect matching in that deck pairs `n` with some
`t in Bhat-(D union {n})`, and its `n--t` edge evaluates to
`ell_t(k_t)=0`.  Hence the whole deck is zero.  The same argument kills
`H_Bhat` in the top term, independently of `omega`.

Thus the evaluated left side is zero.  The coefficient of
`e_(a_0,c)^* tensor e_(a_1,c)^*` on the target side is

```text
k_(n,c) product_(t in Bhat-{n}) k_(t,c),              (10)
```

which is nonzero by (8)--(9).  This is a contradiction and proves (3).

A nonzero covector cannot be a multiple of two different coordinate
covectors, so the neighbours supplied for distinct colours are distinct.
`square`

The proof used every perfect matching in every labelled deck.  It did not
discard a nuisance label, divide by an edge, or choose a rank minor.

## 3. Uniform kernel-shore consequence

For `t!=n` and a colour `c`, define the linear subspace

```text
P_(t,c)={k in K_n:
          W_(n,t)(k,-) belongs to K e_(t,c)^*}.       (11)
```

Let

```text
T_n=K_n intersect (K^*)^3.                            (12)
```

This is a nonempty Zariski-open subset of the linear space `K_n`.

### Theorem 3 (fixed pure restricted shores)

For every colour `c`, there is a neighbour `t_c` such that (4) holds.  The
three `t_c` can be chosen distinct.  Moreover, there is one

```text
k in T_n                                                   (13)
```

for which all three covectors `W_(n,t_c)(k,-)` are nonzero.

### Proof

Theorem 2 gives the finite constructible cover

```text
T_n subset union_(t!=n)
 {k in P_(t,c):W_(n,t)(k,-)!=0}.                     (14)
```

The closure of each nonempty member on the right is contained in the linear
space `P_(t,c)`.  Since `T_n` is dense in the irreducible vector space
`K_n`, a finite union of proper closed linear subspaces cannot contain it.
Therefore some `P_(t,c)` is all of `K_n`, and its restricted edge map is
not zero.  This is (4).

Choose one such neighbour for each colour.  One neighbour cannot serve two
colours because its nonzero image would lie in two distinct coordinate
lines.  Thus the three neighbours are distinct.

Write the three nonzero restricted edge maps as

```text
W_(n,t_c)(k,-)=mu_c(k)e_(t_c,c)^*,
0!=mu_c in K_n^*.                                    (15)
```

The coordinate hyperplanes and the three kernels `ker mu_c` are finitely
many proper linear subspaces of `K_n`.  They cannot cover `K_n` over the
infinite field `K`.  A vector outside their union satisfies (13) and makes
all three shores nonzero.  `square`

The fixed shores in (4) need not remain nonzero on every exceptional point
of `T_n` when `dim K_n>=2`.  The exact pointwise cover is (14); another
neighbour may carry the pure shore where one fixed scalar `mu_c` vanishes.
When `rank J_n=2`, `K_n` is a fully supported line, so each nonzero `mu_c`
is nonzero at every torus point of that line.

### Theorem 3.1 (complete exceptional-section flag)

Fix a colour `c`.  There are linear subspaces and neighbours

```text
K_n=L_0 strictly contains L_1 strictly contains ... strictly contains L_s,
t_0,...,t_(s-1),                                      (16a)
```

with `s<=dim K_n`, such that:

1. `L_s intersect T_n` is empty;
2. for every `i<s`,

   ```text
   W_(n,t_i)(L_i,-) subset K e_(t_i,c)^*
   ```

   is nonzero on `L_i`;
3. writing

   ```text
   W_(n,t_i)(k,-)=mu_i(k)e_(t_i,c)^*  on L_i,
   L_(i+1)=L_i intersect ker mu_i,                    (16b)
   ```

   the shore is nonzero at every point of
   `(L_i intersect T_n)-L_(i+1)`.

Hence these at-most-`dim K_n` locally closed strata cover every exceptional
torus point of the probe kernel without choosing a denominator.

### Proof

Begin with `L_0=K_n`.  If `L_i intersect T_n` is empty, stop.  Otherwise
repeat the finite-cover proof of Theorem 3 on the irreducible linear space
`L_i`, using Theorem 2 at every point of its nonempty torus intersection.
It supplies a neighbour whose restricted shore is a nonzero pure
`c`-coordinate map on all of `L_i`.  Define `L_(i+1)` by (16b).  Its
dimension is strictly smaller.  The process therefore stops after at most
`dim K_n` steps, and the displayed strata have the asserted coverage.
`square`

The nonrigid rank profiles are therefore retained exactly:

```text
rank J_n=0: dim K_n=3, at most three pure-star strata per colour;
rank J_n=1: dim K_n=2, at most two pure-star strata per colour;
rank J_n=2: dim K_n=1, one fixed shore is pointwise nonzero;
rank J_n=3: n is rigid and the theorem does not apply.               (16)
```

## 4. Rigid readouts and the pair-companion synchronization boundary

Write the two probe-incidence blocks of any auxiliary label `t` as

```text
X_t=sum_(c=0)^2 x_(t,c) tensor e_(t,c)^*,
Y_t=sum_(c=0)^2 y_(t,c) tensor e_(t,c)^*,             (17)
```

with `x_(t,c) in V_(a_0)^*` and `y_(t,c) in V_(a_1)^*`.  If the rigid
coordinate readout of `t` uses colour `c`, then

```text
(x_(t,c),y_(t,c))!=(0,0).                            (18)
```

This condition is necessary, not sufficient, for the coordinate readout.

For two labels `s,t`, the `(c,c)` auxiliary-coordinate coefficient of their
pair companion is

```text
Gamma_(s,t,c)=x_(s,c) tensor y_(t,c)
              +x_(t,c) tensor y_(s,c).               (19)
```

### Theorem 4 (same-coordinate pair-companion trichotomy)

Assume (18) for both `s` and `t`.  In characteristic different from two,
`Gamma_(s,t,c)=0` exactly in one of the following three cases:

1. `y_(s,c)=y_(t,c)=0` (the common pure-`X` probe axis);
2. `x_(s,c)=x_(t,c)=0` (the common pure-`Y` probe axis);
3. all four factors are nonzero and, for some `lambda!=0`,

   ```text
   x_(t,c)=lambda x_(s,c),
   y_(t,c)=-lambda y_(s,c).                          (20)
   ```

Consequently, if three labels have rigid readouts using one common colour,
then either some pair has `Gamma_(s,t,c)!=0` or all three labels use one
common pure probe axis at that colour.  Two labels retain the oblique
anti-synchronized alternative (20).

### Proof

If one of the two decomposable summands in (19) is zero, then both must be
zero.  Under (18), the only possibilities are the two common pure-axis
cases.  If both summands are nonzero, equality of nonzero decomposable
tensors gives proportional first factors and proportional second factors;
the minus sign gives exactly (20).  The converse checks directly.

For three labels, suppose every pair coefficient vanishes and the labels are
not all on one pure axis.  A pure-axis label paired with an oblique label or
the opposite pure axis gives a nonzero coefficient, so all three must be
oblique.  Choose common nonzero directions `p,q` and write

```text
x_(t,c)=alpha_t p,       y_(t,c)=beta_t q.
```

Pairwise vanishing says
`alpha_s beta_t+alpha_t beta_s=0`.  Dividing by the nonzero `alpha_t` and
putting `rho_t=beta_t/alpha_t` gives `rho_s+rho_t=0` for all three pairs.
Characteristic different from two forces all `rho_t=0`, contradicting the
oblique case.  `square`

A nonzero `Gamma_(s,t,c)` is only one diagonal coefficient of the physical
companion.  It is not a pure diagonal row, a nonzero complementary deck, or
a complete-nuisance selector.

### Lemma 4.1 (homogeneous common-probe synchronization identity)

Fix common probe contractions and write the resulting covectors at label
`t` as `x_t,y_t`.  For arbitrary scalars `delta_t,eta_t`, put

```text
d_t=delta_t x_t+eta_t y_t,
G_st=x_s tensor y_t+y_s tensor x_t,
A_st=x_s tensor y_t-y_s tensor x_t.
```

Then

```text
2(d_s tensor d_t
  -delta_s delta_t x_s tensor x_t
  -eta_s eta_t y_s tensor y_t)
 =(delta_s eta_t+eta_s delta_t)G_st
  +(delta_s eta_t-eta_s delta_t)A_st.                (21)
```

This follows by direct expansion.  The projective determinant
`delta_s eta_t-eta_s delta_t` is exactly the unequal-line defect.  Equal
non-axis lines kill that defect, while pure axes can kill the symmetric
coefficient of `G_st`.  `GLS55` supplies neither the common probe
contractions in this lemma nor nuisance absorption of the two square terms.

The boundary is pointwise, including the exact anti-synchronization divisor.
For example, with nonzero `p,q`, take at one colour

```text
x_s=p, y_s=q, x_t=p, y_t=zq.
```

Then `Gamma_(s,t,c)=(z+1)p tensor q`; both labels remain rigid with both
probe axes nonzero on the exceptional divisor `z=-1`.

## 5. Natural `GLD3` re-anchoring is activity-silent

Fix the simultaneous pure-star point from Theorem 3 and write its three
neighbours as `t_0,t_1,t_2`, indexed so that

```text
a_i:=W_(n,t_i)(k,-)=lambda_i e_(t_i,i)^*,
lambda_i!=0.                                           (22)
```

Choose either old probe `a_sigma` and any contraction vector `z` there.  Use
`{n,a_sigma}` as the residual pair of a four-port response window containing
`t_0,t_1,t_2` and one further port.  Put

```text
b_i:=W_(a_sigma,t_i)(z,-).                            (23)
```

Because `k in ker J_n`, the residual edge scalar is

```text
h=W_(n,a_sigma)(k,z)=0.                               (24)
```

Thus the `GLD3` pair response between two star neighbours is

```text
D_ij=a_i tensor b_j+b_i tensor a_j.                  (25)
```

### Theorem 5 (diagonal pure-star triangle vanishing)

If all three tensors `D_01,D_02,D_12` in (25) are target-diagonal, then

```text
b_0=b_1=b_2=0,
D_01=D_02=D_12=0.                                    (26)
```

Consequently a four-port window containing the three star neighbours cannot
satisfy the three-colour complementary pair-depth activity hypothesis of
`GLD3`.

### Proof

For a fixed pair `i!=j`, equation (25) has the form

```text
lambda_i e_i^* tensor b_j+b_i tensor lambda_j e_j^*. (27)
```

Every coefficient away from row `i` or column `j` is already zero.  Requiring
(27) to be diagonal shows that `b_j` is supported in `span{e_i^*,e_j^*}`
and that `b_i` is supported in the same two coordinate lines.  Apply this to
the two pairs containing a fixed `i`.  The two support intersections leave

```text
b_i=mu_i e_i^*.                                      (28)
```

The sole possible coefficient in (27) is now the off-diagonal `(i,j)` cell,
so diagonality gives

```text
lambda_i mu_j+mu_i lambda_j=0.                       (29)
```

Put `nu_i=mu_i/lambda_i`.  The three equations are

```text
nu_0+nu_1=nu_0+nu_2=nu_1+nu_2=0.
```

Characteristic zero gives `nu_0=nu_1=nu_2=0`, proving (26).

Every perfect matching of four ports consisting of the three `t_i` and a
fourth port uses one edge of the triangle on the `t_i`.  That edge response
is zero by (26), so every complementary pair-depth product is zero.  `square`

The divisions in the proof are only by the three declared nonzero star
scalars `lambda_i`; no response, rank minor, residual edge, or nuisance
factor is inverted.

## 6. Root-order-three zero-anchor bifurcation

Assume now `r=3` and `omega=0`.  There are six auxiliary labels.  By
`GLS55`, at least five are rigid.

### Corollary 6 (six-rigid or rigid-supported pure star)

Exactly one of the following holds:

1. all six auxiliary labels are torus-rigid;
2. there is a unique nonrigid label `n`, and it has one fully supported
   simultaneous probe-kernel vector with three nonzero coordinate-pure edges
   in the three target colours to three distinct rigid labels.

### Proof

If a nonrigid label exists, `GLS55` says the other five labels are rigid.
Apply Theorem 3.  Otherwise every label is rigid.  `square`

This is an exhaustive source-structure split.  It is not an exhaustive
attachment split: neither branch supplies a complete-nuisance selector or a
named detector input.

## 7. Sharp interface boundary

The pure star consists of direct auxiliary--auxiliary physical shores.  It
is not a promoted physical response and it is not the coefficient row
`G_D^A` of a legal target selector.

An exact rational source-adjacent control makes the response boundary
explicit.  Use original roots `{a_0,a_1,n}`, ports
`{q_0,q_1,t_0,t_1,t_2}`, promoted residual pair `Q={q_0,q_1}`, and
`Uhat={n,t_0,t_1,t_2}`.  Write `E_ij=e_i^* tensor e_j^*` in the displayed
edge orientation and take

```text
W_(a_0,q_0)=E_00,       W_(a_1,q_1)=E_00,
W_(a_0,t_0)=E_00,       W_(a_1,t_1)=E_00,
W_(a_0,t_2)=E_00,
W_(q_0,q_1)=E_00,       W_(q_0,n)=E_00,
W_(q_1,t_c)=E_(0,c),    W_(n,t_c)=-E_(0,c),  c=0,1,2,
```

with every undeclared block zero.  Contract all roots and `Q` at
`(1,1,1)`.  The label `n` is nonrigid, the other five auxiliary labels are
rank-one coordinate-rigid, and

```text
W_(n,t_c)((1,1,1),-)=-e_(t_c,c)^*.
```

It has nonzero `H_Q`, raw `p_(A,Q)`, and complementary permanent `Pi_Q`, and
all root-pair evaluations vanish.  Nevertheless all six promoted pair
responses and the promoted top response vanish identically.  The full
eight-party matching tensor has one nonzero mixed coefficient `-2` and zero
pure coefficients, so it is not a witness.  This is an exact off-target
same-graph control, not a counterexample and not proof of full `GLS4`
eligibility.

Rigidity alone is equally insufficient on the all-six-rigid branch.  Two
exact full-map controls are useful.

1. For labels `t_(c,sigma)`, with `c in {0,1,2}` and `sigma in {1,-1}`,
   choose nonzero probe covectors `p,q` and put

   ```text
   X_t=p tensor e_(t,c)^*,
   Y_t=sigma q tensor e_(t,c)^*.
   ```

   Every label is rank-one coordinate-rigid and both probe maps are nonzero,
   but

   ```text
   G_(t_(c,sigma),t_(d,tau))
      =(sigma+tau)p tensor q tensor e_c^* tensor e_d^*.
   ```

   The only same-colour pairs have opposite signs and vanish; every surviving
   coefficient is off-diagonal.

2. Choose independent `p_0,p_1 in V_(a_0)^*` and nonzero
   `q_2 in V_(a_1)^*`, and for all six labels put

   ```text
   X_t=p_0 tensor e_(t,0)^*+p_1 tensor e_(t,1)^*,
   Y_t=q_2 tensor e_(t,2)^*.
   ```

   Every `J_t` is injective of rank three and both probes are active.  Every
   pair companion is supported only on the auxiliary colour cells
   `02,20,12,21`, so all diagonal coefficients vanish even off every
   joint-rank-drop fibre.

These controls are incidence/companion systems, not complete GHZ witnesses.
Together with the exact `z=-1` divisor above, they show that neither generic
full rank nor retention of both probe maps turns rigidity into diagonal
attachment.

If instead `n` is made one of the two residual vertices of a `GLD3` window,
the pure star supplies only one residual-shore family.  The second family,
the six diagonal pair responses, constant complete-nuisance selectors, and
the complementary pair-depth products remain unforced.

## 8. Exact frontier

```text
pointwise three-colour pure star from any nonrigid label: PROVED;
fixed pure restricted edge per colour on ker J_n:         PROVED;
one simultaneous torus point activating the fixed star:  PROVED;
complete exceptional kernel-section flag:                PROVED;
rigid same-coordinate companion trichotomy:               PROVED;
pure-axis / anti-synchronized / full-rank boundaries:      PROVED;
all rank/divisor/anchor fibres retained:                  PROVED;
r=3 zero-anchor six-rigid / unique-star bifurcation:      PROVED;
natural h=0 GLD3 re-anchoring has zero star triangle:      PROVED;
existence of a nonrigid label:                            NOT CLAIMED;
all-six-rigid branch:                                     OPEN;
rigidity forces a nonzero diagonal pair coefficient:      FALSE IN GENERAL;
pure star implies a promoted physical response:           FALSE IN GENERAL;
constant normalized complete-nuisance selector:           OPEN;
pair/four-port synchronization and pair-depth activity:   OPEN;
target-pure anchor and named downstream receiver:          OPEN;
maximum-root strategic-node closure:                       OPEN;
global Krenn--Gu conjecture:                               UNRESOLVED.
```

At root order three, the smallest remaining zero-anchor structural
obligation is now split cleanly.  The all-six-rigid branch needs complete
mixed/deck coupling beyond its exact pure-axis and anti-synchronization
boundaries.  On the unique-nonrigid branch, the natural `h=0` re-anchoring
lands on the zero-triangle activity boundary, so the next theorem must use
complete mixed equations to exclude that low-activity cell or construct a
different legally transported receiver.  At higher
root order, the theorem supplies the same pure-star escape for each
nonrigid label, but `GLS55` does not force its three neighbours to be rigid.

## Verification

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_nonrigid_probe_kernel_three_colour_pure_star_escape.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_nonrigid_probe_kernel_three_colour_pure_star_escape.py
```

The focused verifier checks the coordinate-covector alternative over exact
rationals, enumerates every companion/deck matching-kill type through root
order seven, checks the three-neighbour and rank-profile consequences, and
replays the exact sharp local control.  The independent standard-library
audit imports no project code or algebra package.  It uses modular covector
census, involution-coded perfect matchings, and a separately encoded local
control.  The bounded computations replay the interfaces; the written proof
carries arbitrary root order and characteristic zero.
