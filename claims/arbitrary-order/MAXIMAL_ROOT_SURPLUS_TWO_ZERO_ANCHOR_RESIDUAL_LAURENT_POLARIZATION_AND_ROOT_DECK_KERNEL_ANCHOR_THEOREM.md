# Maximum-root surplus-two zero-anchor residual-Laurent polarization and root-deck kernel anchor

## Status

**Exact characteristic-zero arbitrary-root polynomial identities and rational
fixed-contraction sharpness boundary.**  On the zero-anchor branch, retain the
two residual vectors as independent Laurent variables and choose the
denominator-free shore normals given by their `2 x 2` incidence minors.  The
two complete first-polarized equations and the product-normal equation then
hold as exact bihomogeneous polynomial identities of bidegrees `(2,2)`,
`(2,2)`, and `(3,3)`.  No response, residual coordinate, shore minor, or
projector scalar is divided out; rank-drop and `p=0` fibres remain in the
identities, although the minor normals can vanish there.

The one missing coefficient of the **unprojected** two-variable evaluation
pencil is the actual-root constant equation.  It contains the physical
residual-absent port deck `H_Uhat`.  Contracting every port, or every port but
one, by the exact local kernel `ker a_u intersect ker b_u` removes all promoted
pair and one-`Q` suppliers and isolates `p H_Uhat` against the pure diagonal.
This gives an exact target-anchor quotient, not forced anchor survival.

The merged `GLS32` graph passes both first-polarized equations and the normal
equation at the chosen all-ones residual contraction.  It does **not** pass
the residual-Laurent family: the two first-polarized equations each have `76`
coefficientwise residual-colour failures, with displayed opposite monomials
which cancel only at the chosen point.  The normal equation holds
coefficientwise, while the actual-root constant equation has `200`
residual-colour failures and `41` failures after the all-ones contraction.
Thus `GLS32` refutes a fixed-contraction projected argument but not a
residual-family argument.

This is `GLS33`.  It does not exclude the one-active or two-active divisor,
force a legal selector or anchor, cover other shore types or arbitrary-root
source branches, close the maximum-root surplus-two strategic node, or
resolve the conjecture.  The global Krenn--Gu status remains **UNRESOLVED**.

## Dependencies and notation

Use

- [`GLS21`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_BASE_SHADOW_ALL_PORT_NUISANCE_COLLAPSE_THEOREM.md) for the raw promoted matching decomposition;
- [`GLS22`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md) for `q`, `p`, and `P_Q`;
- [`GLS27`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RESIDUAL_FAMILY_GENERIC_ESCAPE_AND_COORDINATE_SHORE_NORMAL_FORM_THEOREM.md) for the residual Laurent family;
- [`GLS31`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIMULTANEOUS_ABSORPTION_EVALUATION_PENCIL_AND_MIXED_EQUATION_SHARPNESS_THEOREM.md) for the fixed-contraction polarized notation; and
- [`GLS32`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FIRST_POLARIZED_SINGLETON_KERNEL_AND_SIMULTANEOUS_ABSORPTION_SHARPNESS_THEOREM.md) for the sharp control.

Let `K` have characteristic zero and put

```text
Uhat=K_0 disjoint-union U,       |Uhat|=m=2r-2,
Bhat=Q disjoint-union Uhat,      Q={q_0,q_1},
Lambda=K[z_(s,c):s=0,1 and c=0,1,2].                 (1)
```

The Laurent localization used by `GLS27` may be substituted for `Lambda`;
the identities below already have polynomial coefficients.  Retain the
actual probe-root vectors `s_0,s_1` and define

```text
xi_i^s(z_s)=W_(a_i,q_s)(-,z_s),
X_i=span_Lambda{xi_i^0,xi_i^1},
q(z)=xi_0^0 tensor xi_1^1+xi_0^1 tensor xi_1^0,
p(z)=q(z)(s_0,s_1),
alpha_c(z)=z_(0,c)z_(1,c).                           (2)
```

The zero-anchor hypothesis is

```text
omega=W_(a_0,a_1)=0.                                 (3)
```

Choose the declared colour bases on the two three-dimensional probe spaces.
For each shore let `N_i(z)` be the vector of signed `2 x 2` minors of the
`3 x 2` matrix with columns `xi_i^0,xi_i^1`.  Equivalently it is the
coordinate cross product

```text
N_i=xi_i^0 cross xi_i^1.                             (4)
```

Then

```text
xi_i^0(N_i)=xi_i^1(N_i)=0,                           (5)
```

and `N_i` is bihomogeneous of residual bidegree `(1,1)`.  It is nonzero
exactly on the rank-two shore open and vanishes, rather than introducing a
denominator, on the rank-drop locus.

For every promoted port `u`, put

```text
a_u=W_(a_0,u)(s_0,-),       x_u=W_(a_0,u)(N_0,-),
b_u=W_(a_1,u)(s_1,-),       y_u=W_(a_1,u)(N_1,-),    (6)
lambda_i^s=xi_i^s(s_i).
```

For `D={u,v}` in canonical order define

```text
K_D^00=a_u tensor b_v+b_u tensor a_v,
K_D^10=x_u tensor b_v+b_u tensor x_v,
K_D^01=a_u tensor y_v+y_u tensor a_v,
K_D^11=x_u tensor y_v+y_u tensor x_v.                (7)
```

Let `R_(Uhat-D)(z)` and `S_(s,u)(z_(1-s))` be the complete physical response
and labelled one-`Q` deck tensors of `GLS31`, now with the residual variables
left formal.  They have residual bidegrees `(1,1)` and respectively `(0,1)`
or `(1,0)`.

## 1. Denominator-free residual-Laurent polarization

### Theorem 1 (complete polynomial coefficient identities)

On a complete ternary GHZ hypothetical witness, the following identities hold
in `Lambda tensor tensor_(u in Uhat)V_u^*`:

```text
sum_D K_D^10 tensor R_(Uhat-D)
 +sum_(s,u)lambda_1^s x_u tensor S_(s,u)
 =sum_c alpha_c N_0(c)s_1(c)e_c^(tensor m),           (8)

sum_D K_D^01 tensor R_(Uhat-D)
 +sum_(s,u)lambda_0^s y_u tensor S_(s,u)
 =sum_c alpha_c s_0(c)N_1(c)e_c^(tensor m),           (9)

sum_D K_D^11 tensor R_(Uhat-D)
 =sum_c alpha_c N_0(c)N_1(c)e_c^(tensor m).          (10)
```

Every one-`Q` label is retained separately.  Equations (8)--(9) are
bihomogeneous of bidegree `(2,2)` and (10) is bihomogeneous of bidegree
`(3,3)`.  Hence they are finite coefficientwise residual-colour systems,
not identities only at one chosen residual contraction.

#### Proof

Use the raw `GLS21` promoted decomposition before applying `P_Q`.  Evaluate
the two `A` slots at

```text
s_0+tau N_0,       s_1+upsilon N_1.                  (11)
```

A promoted-pair coefficient expands into the four tensors in (7).  For a
one-`Q` label `{q_s,u}`, the zero-anchor coefficient is

```text
xi_0^s tensor W_(a_1,u)+W_(a_0,u) tensor xi_1^s.     (12)
```

Equations (5) leave exactly

```text
tau lambda_1^s x_u,       upsilon lambda_0^s y_u,    (13)
```

with no `tau upsilon` term.  The `D=Q` coefficient is `q(z)`; (5) makes it
constant in (11).  The top-grade coefficient vanishes by (3).  Expanding the
GHZ target gives the right sides of (8)--(10).  Comparing the `tau`,
`upsilon`, and `tau upsilon` coefficients proves the identities directly,
without a projector or division by `p`.

The degree statements follow from (2), (4), and the declared response/deck
degrees.  Since this is an equality in the polynomial ring, every divisor and
rank-drop fibre is retained.  When a minor normal vanishes, the corresponding
identity can become silent; polynomial retention is not fibre exclusion.
`square`

At any rank-two residual point, substituting a scalar multiple of the usual
shore normal recovers `GLS31` equations (9)--(11).  Conversely, one fixed
point cannot replace the coefficientwise polynomial identities.

More generally, any polynomial vector `n_i(z)` annihilating both
`xi_i^0(z_0)` and `xi_i^1(z_1)` may replace `N_i` in the corresponding
identity.  Its own residual degree replaces the canonical degree count.  The
constant `e_0` normals in the control below are therefore literal instances
of the same raw coefficient equations.

## 2. The actual-root constant deck and its kernel anchor

For a port define the subspace of `V_u`

```text
K_u^00=ker a_u intersect ker b_u.                    (14)
```

Each space has dimension at least one; it may be larger on a rank-drop
fibre.  Write `H_Uhat` for the physical residual-absent port deck.

### Theorem 2 (constant root-deck equation)

The constant coefficient of (11) is

```text
sum_D K_D^00 tensor R_(Uhat-D)
 +sum_(s,u)(lambda_0^s b_u+lambda_1^s a_u)
       tensor S_(s,u)
 +p H_Uhat
 =sum_c alpha_c s_0(c)s_1(c)e_c^(tensor m).          (15)
```

This is the only coefficient of the unprojected evaluation pencil not present
in (8)--(10).  The transverse projector cancels it identically, because it is
the value at the base point `(s_0,s_1)`.

For arbitrary `z_u in K_u^00` at every port, (15) contracts to

```text
p H_Uhat((z_u)_u)
 =sum_c alpha_c s_0(c)s_1(c) product_u z_u(c).        (16)
```

For a fixed free port `u` and arbitrary `z_v in K_v^00`, `v!=u`, it contracts
to the covector identity

```text
p H_Uhat((z_v)_(v!=u),-)
 +sum_s S_(s,u)((z_v)_(v!=u))
      (lambda_0^s b_u+lambda_1^s a_u)
 =sum_c alpha_c s_0(c)s_1(c)
      (product_(v!=u)z_v(c))e_(u,c)^*.               (17)
```

Consequently, modulo `span{a_u,b_u}`, the pure diagonal covector in (17)
equals the class of the residual-absent anchor `p H_Uhat`.  No nonvanishing
of either class is asserted.

#### Proof

The promoted-pair constant is `K_D^00`.  Evaluating (12) at `(s_0,s_1)` gives
`lambda_0^s b_u+lambda_1^s a_u`.  The `D=Q` term is exactly `p H_Uhat`, and
the top term vanishes by (3).  The GHZ constant coefficient is the right side
of (15).

In (16), every promoted-pair supplier has an endpoint factor among `a_v,b_v`
and every one-`Q` supplier lies in `span{a_u,b_u}` at its labelled port, so
the declared kernels kill both sums.  For (17), every term whose labelled
port is not `u` is killed at that port; every promoted pair containing `u`
has its other endpoint killed.  Only the displayed one-`Q` terms at `u` and
the port deck remain.  No coordinate, kernel vector, or `p` is divided out.
`square`

## 3. Exact failure of fixed-contraction camouflage over the residual family

Use the exact `GLS32` graph.  For formal residual vectors `z_0,z_1`, all four
shore covectors lie polynomially in the coordinate plane

```text
span{e_1,e_2}.                                       (18)
```

On the fully supported Laurent torus both shore spans equal this plane; over
the polynomial ring the coordinate factors need not be units.  In either
setting `e_0` is a global constant denominator-free annihilator of both
shores.  Let
`E^10(z)`, `E^01(z)`, and `E^11(z)` denote the raw left side minus target side
of (8)--(10) with this constant normal.

### Theorem 3 (residual-colour separation of the GLS32 control)

At the promoted port word `(0,0,0,1)`, exact evaluation gives

```text
[E^10(z)]_(0001)
 =1/4 (z_(0,0)z_(1,1)-z_(0,2)z_(1,0)),              (19)

[E^01(z)]_(0001)
 =1/4 (z_(0,0)z_(1,2)-z_(0,1)z_(1,0)).              (20)
```

Across all residual colour pairs and all `3^4` promoted words,

```text
E^10: 76 nonzero coefficients,
       38 on each of residual pairs (0,1) and (2,0);
E^01: 76 nonzero coefficients,
       38 on each of residual pairs (0,2) and (1,0);
E^11: 0 nonzero coefficients.                         (21)
```

At `z_0=z_1=(1,1,1)`, the opposite terms in (19)--(20), and all other
first-polarized failures, cancel pairwise.  This is why the chosen contraction
passes the complete projected `GLS31` pencil.

The unprojected constant equation has `200` nonzero residual-colour/promoted-
word coefficients.  After setting both residual vectors to all ones, it still
has `41` nonzero promoted words.  More directly, at that contraction choose
`z_u=e_1` at all four promoted ports.  These vectors lie in the declared
`K_u^00` spaces, while

```text
p=2,       H_Uhat(e_1,e_1,e_1,e_1)=1,
right side of (16)=1.                                 (22)
```

Thus (16) has defect one.  Hence the graph is excluded by both the
residual-Laurent first-polarized family and the actual-root constant deck.  It
remains a valid sharpness certificate for the single projected contraction
proved in `GLS32`.

#### Proof

Insert the displayed `GLS32` matrices into the raw perfect-matching tensor.
The only nonzero residual-pair coefficients of the first displayed port word
in the `10` profile are `+1/4` at `(0,1)` and `-1/4` at `(2,0)`, giving (19).
The `01` profile similarly has `+1/4` at `(0,2)` and `-1/4` at `(1,0)`, giving
(20).  Exhaustive exact coefficient collection gives (21), the constant
counts, and the all-ones cancellations.  Direct four-port matching gives
(22).  The focused verifier and independent no-import audit use separate
matching and reduction representations.
`square`

## 4. Exact boundary and next obligation

`GLS33` converts the residual-family continuation into explicit polynomial
equations and supplies a denominator-free root-deck anchor quotient.  It does
not prove that a diagonal class in (17) survives, that `H_Uhat` is target-pure
in a complete downstream nuisance quotient, or that any physical response is
nonzero and synchronized with it.  The canonical normals vanish on shore
rank-drop fibres, so those fibres are retained but not excluded.

The smallest surviving rank-two-shore obligation is to combine the
coefficientwise equations (8)--(10) and the constant anchor identity (17)
with the one-/two-active `GLS30` profiles.  On every residual divisor and rank
fibre, one must either force a complete-`GLS23` separator with nonzero physical
response, synchronization, activity, nuisance survival, and every named
downstream anchor gate, or contradict the same graph's full mixed coefficient
deck.  Other shore types and arbitrary-root source coverage remain open.

## Verification

Run the focused exact primary verifier:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_residual_laurent_polarization_and_root_deck_kernel_anchor.py
```

It reconstructs the `GLS32` graph, its formal residual shore normals, all four
raw residual-colour coefficient profiles, the fixed-contraction cancellations,
the displayed defects, and the exact `76/76/0/200/41` counts with SymPy.

Run the independent no-import audit:

```text
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_residual_laurent_polarization_and_root_deck_kernel_anchor.py
```

It uses only standard-library `Fraction`, a separate recursive matching
engine, direct residual-colour coefficient tables, and independent sparse
contraction.  It imports neither the primary verifier, `GLS32`, nor SymPy.

The arbitrary-root polynomial and kernel-anchor statements are proved by the
written matching partition and multilinear contraction.  Neither script
certifies divisor exclusion, selector/anchor survival, node closure, or global
resolution.
