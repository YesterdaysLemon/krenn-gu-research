# Maximum-root surplus-two zero-anchor tangent-root Fitting boundary and constant-anchor Segre silence

## Status

**Exact characteristic-zero arbitrary-root module theorem, pointwise anchor
dichotomy, and rational two-active diagonal/singleton channel boundary.**  The
four complete
coefficientwise profiles supplied by `GLS33` define a finite linear
observation map on the `81` probe coefficients of any fixed promoted-port
word.  Its kernel has an exact block decomposition into two shore
multiplier kernels and one coupled tangent-block kernel.  On a nonempty
explicit Fitting open in the ambient shore-matrix parameter space, the
observation rank is `75`, and the missing six
directions are exactly the two physical tangent-root incidence syzygies,
three from either shore.  Every rank-drop fibre is retained by the same block
rank formula; it is not discarded by localization.

The `GLS33` constant root-deck equation has a separate pointwise dichotomy.
Restrict its pure diagonal tensor to the product of the exact local kernels

```text
K_u^00=ker a_u intersect ker b_u.
```

If that restriction is nonzero, one tuple simultaneously forces a nonzero
root-deck value and a nonzero singleton anchor class at every port; in
particular this branch cannot occur on `p=0`.  If it is zero, the diagonal
lies in the exact sum of local two-row cylinders.  For one, two, or three
surviving diagonal colours, this silent branch has a complete killed-colour
or Segre-line classification: surviving coordinate restrictions are
projectively synchronized at every port except possibly one.

An exact same-graph two-active channel lies on the silent **diagonal target**
locus and makes every first-polarized singleton contraction silent while
retaining the `GLS30` normal identity and six nonzero physical responses.  Its
physical constant root-deck value is nonzero, so the complete `00` equation
detects it.  It also fails the uncontracted `10` and `01` equations and is not
a witness.  Thus the load-bearing continuation is to couple the tangent-root
syzygies, the physical root deck, and the Segre-silent diagonal locus using
the full residual-polynomial equations.

This is `GLS34`.  It is not a divisor exclusion, coefficient-side legal
selector, complete-`GLS23` nuisance survivor, response/activity theorem,
arbitrary-root source cover, strategic-node closure, or resolution of the
Krenn--Gu conjecture.  The global status remains **UNRESOLVED**.

## Dependencies and notation

Use

- [`GLS30`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_NORMAL_PRODUCT_DIVISOR_KERNEL_PROFILE_AND_SAME_GRAPH_SHARPNESS_THEOREM.md) for the one-/two-active normal-kernel profiles;
- [`GLS32`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FIRST_POLARIZED_SINGLETON_KERNEL_AND_SIMULTANEOUS_ABSORPTION_SHARPNESS_THEOREM.md) for the first-polarized singleton kernels; and
- [`GLS33`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RESIDUAL_LAURENT_POLARIZATION_AND_ROOT_DECK_KERNEL_ANCHOR_THEOREM.md) for the four residual-polynomial profiles and constant root-deck equation.

Let `K` have characteristic zero.  Write `Z_0,Z_1,A_0,A_1` for four
three-dimensional spaces and

```text
R=K[z_(0,0),z_(0,1),z_(0,2),z_(1,0),z_(1,1),z_(1,2)]
```

with residual bidegree.  The physical shore covectors are

```text
xi_i^0(z_0) in A_i^* tensor R_(1,0),
xi_i^1(z_1) in A_i^* tensor R_(0,1),
lambda_i^s=xi_i^s(s_i),
N_i=xi_i^0 cross xi_i^1 in A_i tensor R_(1,1).       (1)
```

Here `s_i` is the actual nonzero root vector and a declared volume form gives
the cross product.  Put

```text
rho_i=lambda_i^1 xi_i^0-lambda_i^0 xi_i^1
     =s_i cross N_i in A_i^* tensor R_(1,1).          (2)
```

The equality in (2) is the vector triple-product identity in the declared
bases.  Hence

```text
rho_i(s_i)=rho_i(N_i)=0.                              (3)
```

## 1. The complete residual observation map

For one fixed promoted-port coefficient word, let

```text
T in A_0^* tensor A_1^* tensor Z_0^* tensor Z_1^*   (4)
```

be an arbitrary probe coefficient tensor.  Equivalently,
`T(v_0,v_1;z_0,z_1)` is bilinear in the two `A` arguments and belongs to
`R_(1,1)`.  Define

```text
Obs(T)=(
 T(s_0,s_1),
 T(N_0,s_1),
 T(s_0,N_1),
 T(N_0,N_1))                                         (5)
```

in

```text
R_(1,1) direct-sum R_(2,2) direct-sum
R_(2,2) direct-sum R_(3,3).                          (6)
```

These are exactly the `00`, `10`, `01`, and `11` coefficientwise profiles of
`GLS33`; the first is the unprojected constant profile.

Choose bases with `s_0=s_1=e_0`.  Write

```text
N_i=(n_(i,0),n_(i,1),n_(i,2)),
T=(t_(a,b))_(0<=a,b<=2),        t_(a,b) in R_(1,1).  (7)
```

Define the multiplication maps

```text
kappa_i:R_(1,1)^2 -> R_(2,2),
kappa_i(f,g)=n_(i,1)f+n_(i,2)g,                      (8)

mu:R_(1,1)^4 -> R_(3,3),
mu((U_(a,b))_(a,b=1,2))
 =sum_(a,b=1,2)n_(0,a)n_(1,b)U_(a,b).                (9)
```

### Theorem 1 (exact block-kernel decomposition)

There is a coordinate-block identification under which

```text
ker Obs = ker kappa_0 direct-sum ker kappa_1
          direct-sum ker mu.                         (10)
```

Consequently, on every coefficient fibre,

```text
dim ker Obs
 =(18-rank kappa_0)+(18-rank kappa_1)+(36-rank mu),  (11)

rank Obs=81-dim ker Obs.                             (12)
```

No shore minor, residual coordinate, or projector scalar is divided out.

#### Proof

The `00` component of (5) is `t_(0,0)`.  After it vanishes, the `10`
component is

```text
n_(0,1)t_(1,0)+n_(0,2)t_(2,0),                      (13)
```

and the `01` component is the analogous first-row expression.  These are the
two maps in (8).  In the `11` component, the first-column terms are a multiple
of (13), the first-row terms are a multiple of its shore-one analogue, and
the corner has already vanished.  The only remaining expression is (9) on
the tangent `2 x 2` block.  The three groups of input entries are disjoint,
which proves (10) and the dimension formulas.  `square`

The universal syzygies (2) give

```text
rho_0 tensor A_1^* + A_0^* tensor rho_1
 subseteq ker Obs.                                   (14)
```

In particular `rank kappa_i<=17` and `rank mu<=32`.

### Theorem 2 (rank-75 Fitting open and six tangent-root directions)

On the exact Fitting open

```text
rank kappa_0=17,       rank kappa_1=17,
rank mu=32,                                            (15)
```

one has

```text
ker Obs=rho_0 tensor A_1^*+A_0^* tensor rho_1,
dim ker Obs=6,       rank Obs=75.                     (16)
```

This ambient shore-data open is nonempty in characteristic zero.  No claim is
made here that it intersects the maximum-root or GHZ witness locus.

#### Proof

Under the first two rank conditions, each `ker kappa_i` is the one-dimensional
constant-multiple line generated by

```text
(-n_(i,2),n_(i,1)).                                  (17)
```

The rank-`32` condition makes `ker mu` four-dimensional.  Its four evident
constant syzygies are the two column copies of (17) from shore zero and the
two row copies from shore one.  They are independent: a dependence would make
one tangent pair `(n_(i,1),n_(i,2))` a polynomial multiple of a fixed
direction and would enlarge `ker kappa_i`.  They therefore exhaust
`ker mu`.  Adding the first-column and first-row generators gives precisely
the six tensors in (14), proving (16).

For exact nonemptiness, take `s_0=s_1=e_0` and use the four shore matrices

```text
L_00=[[ 1, 1,-1], [ 2,-1, 1], [-2,-1, 0]],
L_01=[[-1,-1, 1], [ 2, 1, 2], [-1, 0,-1]],
L_10=[[-2, 2,-2], [ 0,-2,-1], [-1,-2, 1]],
L_11=[[ 2, 1, 0], [-1, 1, 1], [ 2, 1,-1]],           (18)
```

where `xi_i^s=L_is z_s`.  Exact integer elimination gives

```text
(rank kappa_0,rank kappa_1,rank mu,
 rank tangent generators,rank Obs)=(17,17,32,6,75). (19)
```

Nonzero maximal minors include `576`, `-2^25`, `2^55 3^7`, and `-896` for
the first four ranks, together with a nonzero integer `75 x 75` observation
minor.  Thus (15) defines a genuinely nonempty Zariski open over every
characteristic-zero field.  `square`

### Exact exceptional boundary

Equation (11), rather than the generic number `6`, owns every exceptional
fibre.  The loci

```text
rank kappa_i<=16                                      (20)
```

carry extra first-column or first-row syzygies.  They include identically
vanishing tangent normals, `N_i` parallel to `s_i`, and nonconstant
common-factor or fixed-direction tangent pairs.  On the `kappa` open, the
locus

```text
rank mu<=31                                           (21)
```

carries extra coupled tangent-block syzygies.

This is a coefficientwise polynomial statement.  At one specialized
residual point, (5) consists of only four scalar evaluations and has kernel
dimension at least `77`; a point with `N_i(z)=0` or `N_i(z)` parallel to
`s_i` can be silent even when the global polynomial map has rank `75`.
The divisor `p=0` is separate from (20)--(21).

## 2. Constant root-deck survival versus diagonal silence

Return to the arbitrary-root physical `GLS33` package with
`m=|Uhat|=2r-2`, and fix one residual contraction.  The following statement
is pointwise at that contraction, including when its `p` or shore ranks drop.
Put

```text
A_u=span{a_u,b_u} subseteq V_u^*,
K_u^00=A_u^perp=ker a_u intersect ker b_u,            (22)

delta_c=alpha_c s_0(c)s_1(c),
Delta=sum_c delta_c e_(1,c)^* tensor ... tensor
                         e_(m,c)^*.                   (23)
```

Let `res(Delta)` denote the restriction of `Delta` to
`tensor_u K_u^00`.

### Theorem 3 (pointwise simultaneous anchor-survival dichotomy)

Exactly one of the following holds.

1. **Non-silent branch.**  `res(Delta)!=0`.  Then there are
   `z_u in K_u^00` with

   ```text
   F(z)=sum_c delta_c product_u z_u(c)!=0.            (24)
   ```

   For the same tuple, the all-port `GLS33` equation gives

   ```text
   p H_Uhat((z_u)_u)=F(z)!=0,                         (25)
   ```

   and at every free port `u` the singleton equation gives a nonzero class

   ```text
   p[H_Uhat((z_v)_(v!=u),-)]
    =[sum_c delta_c(product_(v!=u)z_v(c))e_(u,c)^*]
       in V_u^*/A_u.                                 (26)
   ```

   In particular `p!=0` and all `m` output-side singleton anchor classes
   survive simultaneously.

2. **Silent branch.**  `res(Delta)=0`.  Equivalently,

   ```text
   Delta in sum_u V_1^* tensor ... tensor A_u tensor
                         ... tensor V_m^*.           (27)
   ```

   Every all-port constant-kernel contraction is then zero.

The dichotomy includes `rank A_u=0,1,2`, all shore-rank fibres, and `p=0`.
It uses no minors or division.  On a hypothetical witness, `p=0` forces the
silent branch.

#### Proof

If the restriction is nonzero, multilinearity supplies a pure tuple with
(24).  Equation (25) is `GLS33` equation (16).  For each `u`, evaluate the
right covector of `GLS33` equation (17) at the already chosen `z_u`; the
result is the same nonzero scalar `F(z)`.  A covector in `A_u` would vanish on
`K_u^00`, so its quotient class is nonzero.  Equation (25) also excludes
`p=0`.

For finite-dimensional spaces, the kernel of the product restriction is

```text
ker(tensor_u V_u^* -> tensor_u (K_u^00)^*)
 =sum_u V_1^* tensor ... tensor (K_u^00)^perp tensor
                         ... tensor V_m^*.           (28)
```

Since `(K_u^00)^perp=A_u`, (28) proves (27) and exhausts the other branch.
`square`

The classes in (26) are output-side port covectors.  They are not yet a
coefficient-side constant selector annihilating the complete labelled
`GLS23` nuisance.

## 3. Complete three-colour Segre classification of silence

For each colour put

```text
r_(u,c)=e_(u,c)^* restricted to K_u^00,
T_c=tensor_u r_(u,c),
S_Delta={c:delta_c!=0}.                               (29)
```

The colour tensor `T_c` is **killed** exactly when `r_(u,c)=0` at some port,
equivalently when `e_(u,c)^* in A_u`.  The silent equation is

```text
sum_(c in S_Delta)delta_c T_c=0.                     (30)
```

### Theorem 4 (killed-colour/Segre-line case cover)

Equation (30) has the following exhaustive classification.

0. If `|S_Delta|=0`, silence is automatic.

1. If `|S_Delta|=1`, its unique colour tensor is killed.

2. If `|S_Delta|=2`, either both colour tensors are killed, or both survive
   and their local factors are proportional at every port.  Writing

   ```text
   r_(u,d)=lambda_u r_(u,c)                           (31)
   ```

   gives the exact remaining condition

   ```text
   delta_c+delta_d product_u lambda_u=0.              (32)
   ```

3. If `|S_Delta|=3`, delete the killed colour tensors.  Zero survivors are
   silent, one survivor is impossible, and two survivors reduce to case 2.
   If all three survive, there is at most one exceptional port `u_0`; at
   every other port all three restrictions are projectively aligned.  Thus
   one may write

   ```text
   r_(u,c)=lambda_(u,c)rho_u       for u!=u_0,        (33)
   ```

   and silence is exactly the exceptional-port relation

   ```text
   sum_c delta_c(product_(u!=u_0)lambda_(u,c))
                 r_(u_0,c)=0.                        (34)
   ```

When all three terms survive, every nonexceptional `K_u^00` is a
one-dimensional fully supported line, so `rank A_u=2`.  The exceptional
space has dimension at most two, so `rank A_(u_0)>=1`.

#### Proof

A decomposable tensor is zero exactly when one factor is zero, giving the
killed cases.  Two nonzero decomposable tensors are proportional exactly
when their corresponding factors are proportional in every tensor slot;
this proves case 2.

For three surviving terms, solve (30) for one decomposable tensor as a
nontrivial linear combination of the other two.  A nontrivial combination of
two independent simple tensors is simple only when the two tensors differ in
at most one factor: if they differed in two factors, flattening across either
one would have rank two.  Hence all three local projective factors agree away
from at most one port, and factoring those common lines gives (34).  The
converse is immediate.  At a nonexceptional port, the three nonzero coordinate
restrictions span `(K_u^00)^*` but are all proportional, forcing dimension
one; at the exceptional port relation (34) bounds the span by two.  `square`

Thus the silent branch is not an unspecified zero: it is an exact union of
coordinate-killing cylinders and projective Segre-line synchronization
loci, with one allowed exceptional port.

## 4. Exact two-active silent channel boundary

Use the physical two-active response-deck graph of `GLS30`, with all-ones
actual root contractions and

```text
n_0=(1,1,0),          n_1=(1,2,1),          p=-2,
x=y=(e_0,e_0,e_1,e_1),
beta=(1,2,0).                                         (35)
```

Retain its six nonzero physical responses and replace only the two families
of `A`-port blocks so that

```text
a=(e_1,e_2,e_0,e_2),
b=(e_2,e_1,e_2,e_0).                                 (36)
```

One exact realization is

```text
W_(a_0,u)=r_0 a_u^T+t_0 x_u^T,
r_0=e_2,                    t_0=(1/2,1/2,-1),

W_(a_1,u)=r_1 b_u^T+t_1 y_u^T,
r_1=(1,-1,1),               t_1=(0,1,-1).            (37)
```

The all-ones and normal contractions of (37) are exactly `(a,x)` and `(b,y)`.

### Theorem 5 (diagonal-silent normal/singleton same-graph control)

For this graph,

```text
K^00=(K e_0,K e_0,K e_1,K e_1),
K^10=(K e_1,K e_2,K e_0,K e_2),
K^01=(K e_2,K e_1,K e_2,K e_0).                     (38)
```

Every three-port Hadamard product in the `10` and `01` families is zero, and
every three-colour constant diagonal term is killed on `tensor_u K_u^00`.
More strongly, contracting the **actual equation defects** in the `10` and
`01` profiles at the other three ports gives zero for all `2*4*3=24`
profile/free-port/free-colour slices.  Nevertheless the `11` normal identity
is exact and all six physical responses are nonzero.

The physical root deck does not vanish on the displayed all-port kernel
tuple.  Exact contraction gives

```text
H_Uhat(e_0,e_0,e_1,e_1)=-2,
p H_Uhat(e_0,e_0,e_1,e_1)=4,
Delta(e_0,e_0,e_1,e_1)=0.                            (39)
```

Thus the complete constant kernel equation detects this graph with defect
`4`; diagonal silence does not imply physical-equation silence.

This does not solve the uncontracted equations.  Against the fixed all-ones
residual contraction, exact `00/10/01/11` promoted-word failure counts are

```text
(15,10,11,0),                                        (40)
```

with first defect `-1` at word `0000` in each of the first three profiles.
The original eight-vertex graph has `147` GHZ coefficient failures and pure
coefficients `(0,0,0)`.

#### Proof

The four scalar contractions in (37) follow from

```text
s^T r_i=1,   n_i^T r_i=0,   s^T t_i=0,   n_i^T t_i=1.
```

Taking the two-row kernels gives (38).  Their displayed coordinate axes make
every declared three-port product and constant diagonal restriction zero.
Contracting each exact `10/01` defect tensor by those axes on the other three
ports gives the `24` zero singleton slices stated above.  The normal identity
and response tensors are unchanged from the exact `GLS30` graph.  Direct
four-port matching gives (39), and direct eight-vertex perfect-matching
expansion gives (40), the original failure count, and the pure coefficients.
`square`

This is a channel-side boundary only for the diagonal annihilator and
first-polarized singleton data.  It is detected by the complete constant
equation, is not maximum-root or pure-normalized, and fails the full `GLS33`
profiles.

## 5. Exact remaining obligation

The four polynomial profiles now have a complete generic blind-space
description, and the constant profile has a pointwise all-rank survival/silent
case cover.  The smallest next obligation is their **uncontracted coupling**.
On every Fitting, residual-coordinate, `p`, shore-rank, and response fibre,
one must either

1. prove that a physical deck tensor cannot occupy the six tangent-root
   syzygies while its diagonal anchor lies on one of the killed-colour or
   Segre-line silent loci; or
2. upgrade the non-silent classes (26) to a coefficient-side constant
   selector separating the complete labelled `GLS22/GLS23` nuisance, then
   prove nonzero response, synchronization, activity, nuisance survival, and
   every gate of one named downstream detector.

At `omega=0`, the `GLS23` top desired coefficient itself is zero.  Thus the
output-side root-deck class does not automatically attach the four-port target
needed by `GLD3`.  Other shore types, higher-root source coverage, permanent
restriction, and global resolution remain outside this theorem.

## Verification

Run the focused exact primary verifier:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_tangent_root_fitting_and_constant_anchor_segre_silence.py
```

It constructs the five certificate matrices in (19), checks the universal
tangent generators on the exact specialization, verifies representative
silent/surviving Segre cases, and reconstructs the physical control and all
values and counts in (35)--(40).

Run the independent no-import audit:

```text
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_tangent_root_fitting_and_constant_anchor_segre_silence.py
```

It uses only standard-library exact integers and `Fraction`, a different
elimination route and separate matching recursion, and imports neither the
primary verifier, SymPy, nor repository mathematics code.  The arbitrary-root
block decomposition, tensor-annihilator identity, and Segre classification
are the written proofs; the scripts audit the exact finite certificate and
sharp control.
