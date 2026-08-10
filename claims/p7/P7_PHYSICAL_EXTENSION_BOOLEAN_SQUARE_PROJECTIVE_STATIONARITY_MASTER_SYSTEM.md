# The remaining physical P7 equations are Boolean-square projective stationarity

## Status

**Exact characteristic-zero master system.**  On the generic mixed-kernel
chart, the 21 edge variables are reconstructed from seven variables by

```text
delta_ij=alpha-2(a_i+a_j),
w_ij=a_i a_j/delta_ij,
y_ij=x_i+x_j,
f_ij=-w_ij y_ij,
H_A x=0.                                              (1)
```

This note translates every remaining physical P7 equation into two explicit
degree-four covariants in the fixed 14-dimensional Boolean primitive space.
Primitivity says the first covariant is primitive.  The full annihilator
equation says the derivative of the Boolean squaring map in direction
`ell A` is projectively radial at its value.  The unknown generic extension
incidence is therefore one Hessian-kernel/projective-stationarity system in
seven `x` variables, not an unstructured 21-edge search.

The translation is exact but is not an exclusion.  Its generic good locus,
higher-corank strata, exceptional walls, full physical P7 extension, and
global Krenn--Gu remain **UNKNOWN/UNRESOLVED**.

## 1. Quartet covariants

For a four-set `S`, let `M(S)` be its three partitions into two edges.  Put

```text
Psi_S(x)=sum_({e,g} in M(S)) w_e w_g y_e y_g,         (2)

Lambda_S(x)=sum_({e,g} in M(S))
 (w_e y_e b_g+w_g y_g b_e),
b_ij=a_i+a_j.                                         (3)
```

Because `f_e=-w_e y_e`, these are exactly

```text
Psi=coefficient vector of F^2/2,
-Lambda=coefficient vector of F ell A.                (4)
```

Let

```text
P_4=ker(ell:Z_4->Z_5),       dim P_4=14.              (5)
```

The primitive-square equation `ell F^2=0` is precisely

```text
sum_(S subset T, |S|=4) Psi_S=0
for every five-set T,                                 (6)
```

or `Psi in P_4`.  The already imposed mixed-kernel equation gives

```text
ell Lambda=-F ell^2 A=0,                              (7)
```

so `Lambda` automatically lies in the same 14-space.

## 2. Projective stationarity

The remaining annihilator equation is

```text
F(2ell A+tF)=0.                                       (8)
```

By (4), its 35 quartet coefficients are exactly

```text
t Psi=Lambda.                                         (9)
```

Let `q(F)=F^2/2`.  Its differential is `dq_F(G)=FG`, so (9) says

```text
dq_F(ell A)=t q(F).                                  (10)
```

Thus the prescribed tangent direction `ell A` is radial under the Boolean
squaring map at `F`.  Eliminating the nonzero amplitude `t` gives the
coordinate-free projective stationarity equation

```text
Psi wedge Lambda=0 in exterior^2 P_4,
Psi!=0, Lambda!=0.                                   (11)
```

The nonvanishing clauses are essential.  If `Psi=0`, then `F^2=0`; equation
(8) also gives `F ell A=0`.  Multiplication by `ell:Z_3->Z_4` is an
isomorphism, while multiplication by a full-support `A:Z_2->Z_3` is
injective after diagonal scaling to `ell`.  Hence `F=0`, impossible on the
edge torus.  If `Lambda=0`, (9) contradicts `t Psi!=0`.

This is adjacent to the projective eigenconfiguration viewpoint for
polynomial maps developed by Abo, Seigal, and Sturmfels in
[*Eigenconfigurations of Tensors*](https://arxiv.org/abs/1505.05729).
Here the map is not a generic projective self-map: it is Boolean squaring,
the tangent direction is the physical `ell A`, and both sides are forced
into `P_4`.

## 3. Real Gram discriminator and scalar laws

Over the reals, (11) is equivalent to one sum-of-squares identity

```text
G=||Psi||^2 ||Lambda||^2-<Psi,Lambda>^2
 =sum_(S<R)(Psi_S Lambda_R-Psi_R Lambda_S)^2=0,       (12)
```

together with the nonvanishing clauses.  Then

```text
t=<Psi,Lambda>/||Psi||^2.                            (13)
```

Over a complex or arbitrary characteristic-zero field, (12) alone is not
sufficient on the isotropic locus; the full wedge equations (11) are
mandatory.

Two scalar consequences are useful filters.  The master-Hessian equation
gives the signed-network energy law

```text
sum_i a_i x_i^2
 +sum_(i<j)w_ij(x_i+x_j)^2=0.                        (14)
```

The primitive Riccati Casimir becomes

```text
(sum_i a_i x_i)^2
 =4(sum_i a_i^2 x_i^2
    -sum_(i<j)w_ij^2(x_i+x_j)^2).                    (15)
```

For a real full-edge solution, the last edge-square sum is strictly positive,
so

```text
|sum_i a_i x_i|<2 sqrt(sum_i a_i^2 x_i^2).           (16)
```

## 4. Denominator-free master system

Every exceptional divisor is retained by keeping the edge variables.  Put

```text
r_i=sum_(j!=i)f_ij,
delta_ij f_ij+a_i r_j+a_j r_i=0.                     (17)
```

For each four-set define

```text
Psi_S(f)=sum_({e,g} in M(S)) f_e f_g,                (18)

Phi_S(f,a)=sum_({e,g} in M(S))
 (f_e b_g+f_g b_e).                                  (19)
```

Then the complete polynomial system is

```text
sum_(S subset T)Psi_S(f)=0          for every |T|=5,
Phi_S(f,a)+t Psi_S(f)=0             for every |S|=4, (20)
```

together with (17) and the physical torus condition
`a_i f_ij t!=0`.  On the generic chart, (18)--(20) reduce exactly to
(2)--(11).  On a wall, they combine directly with the restricted-Hessian
reconstruction of
`P7_PHYSICAL_MIXED_KERNEL_EXCEPTIONAL_WALL_GRAPH_AND_RESTRICTED_HESSIAN_THEOREM.md`.

## 5. Exact wall

```text
generic mixed kernel:                 H_A x=0;
generic full edge:                    y_ij!=0;
primitive quartet covariant Psi:      EXACT;
directional quartet covariant Lambda: EXACT;
Psi,Lambda in fixed P_4:              PROVED, DIMENSION 14;
full annihilator equation:            t Psi=Lambda;
amplitude-free equation:              Psi wedge Lambda=0;
real proportionality discriminator:  ONE SUM OF SQUARES;
complex isotropic shortcut:           FORBIDDEN;
square-zero physical branch:          EXCLUDED;
denominator-free wall system:         EXACT POLYNOMIAL SYSTEM;
generic good stationary point:        UNKNOWN;
higher-corank and wall stationary points: UNKNOWN;
full-edge physical P7 extension:      UNKNOWN;
global Krenn--Gu:                     UNRESOLVED.     (21)
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_physical_extension_boolean_square_projective_stationarity.py
python claims/p7/audit_p7_physical_extension_boolean_square_projective_stationarity.py
python -m py_compile claims/p7/verify_p7_physical_extension_boolean_square_projective_stationarity.py claims/p7/audit_p7_physical_extension_boolean_square_projective_stationarity.py
uv run --with ruff ruff check claims/p7/verify_p7_physical_extension_boolean_square_projective_stationarity.py claims/p7/audit_p7_physical_extension_boolean_square_projective_stationarity.py
```

The primary verifier builds the universal Boolean products, proves all
quartet/quintet constants and signs, checks the fixed primitive dimension,
and verifies the radial derivative identity.  The independent standard-
library audit rebuilds the same claims with its own square-free polynomial
arithmetic.  Neither imports the other or project code.

## Dependencies

- [P7_PHYSICAL_MIXED_KERNEL_BOOLEAN_DOWN_DESCENT_AND_SEVEN_BY_SEVEN_MASTER_HESSIAN.md](P7_PHYSICAL_MIXED_KERNEL_BOOLEAN_DOWN_DESCENT_AND_SEVEN_BY_SEVEN_MASTER_HESSIAN.md)
- [P7_PRIMITIVE_ZEON_HARMONIC_SQUARE_RICCATI_AND_REAL_ROW_CONE_OBSTRUCTION.md](P7_PRIMITIVE_ZEON_HARMONIC_SQUARE_RICCATI_AND_REAL_ROW_CONE_OBSTRUCTION.md)
