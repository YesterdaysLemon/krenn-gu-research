# Four-root torus-star survivor fraction-free quadratic principal-open nonextension

## Status

**Exact explicit polynomial-circuit principal-open survivor and source-branch
exclusion (`GLD82`).** Work over `K=Q(i)` and then extend scalars to `C`.
Retain the fixed `GLD70` fully-supported, nonisotropic rank-two maximal-star
interface, the scale-fixed equal-leaf survivor chart of `GLD75`--`GLD80`, and
the complete legal `q_0` first response.

There is an explicitly constructed polynomial

```text
Delta_82(F)=Omega(F) gamma_num(F) det M_ff(F)             (1)
```

on the fifteen-variable equal-leaf frame chart. It is nonzero at the `GLD72`
Gaussian frame. On the survivor subopen `D(Delta_82)`, every concise GHZ
tensor and every raw coefficient preimage fails the necessary legal
first-response condition. By `GLD81`, the same open excludes every actual
root-order-four, surplus-two, fully-supported, rank-three, nonisotropic
maximal-star GHZ source whose induced normalized survivor frame lies there.

The determinant in (1) is a `45 x 45` coefficient-span determinant of forty-
five named intrinsic response quadrics in eight invariant raw coordinates and
one homogenizing coordinate. It is supplied as an exact evaluable arithmetic
circuit; its large expansion in the frame variables is not printed. There
are no unspecified denominator-clearing exponents.

The divisor `V(Delta_82)`, other survivor components and gauges, rank/support
boundaries, triangles, other root profiles, and the global Krenn--Gu
conjecture remain **UNRESOLVED**.

Owning dependencies are `GLD74`--`GLD81`, in particular:

- [`GLD75` equal-leaf survivor chart](FOUR_ROOT_TORUS_STAR_SURVIVOR_LOCUS_SYMMETRY_AND_LOCAL_GERM_REDUCTION_THEOREM.md);
- [`GLD76` complete response module](FOUR_ROOT_TORUS_STAR_SURVIVOR_RESPONSE_UNIVERSAL_MODULE_AND_PROJECTIVE_ESCAPE_REDUCTION_THEOREM.md);
- [`GLD78` moving literal-Delta and Reynolds construction](FOUR_ROOT_TORUS_STAR_SURVIVOR_RESPONSE_SIGN_BOUNDARY_INVARIANT_PRINCIPAL_OPEN_NONEXTENSION_THEOREM.md);
- [`GLD80` existential survivor-open theorem](FOUR_ROOT_TORUS_STAR_SURVIVOR_EXISTENTIAL_PRINCIPAL_OPEN_FIRST_RESPONSE_NONEXTENSION_THEOREM.md); and
- [`GLD81` physical source bridge](FOUR_ROOT_TORUS_STAR_SOURCE_TO_SURVIVOR_RESPONSE_INCIDENCE_BRIDGE_THEOREM.md).

## 1. Exact chart and fixed raw solve

Let `x_0,...,x_14` be the `GLD75` equal-leaf frame shifts and write

```text
F=(A,G,G,G).
```

The ten certified survivor generators, together with the scale equation
`x_8=0`, define the scale-fixed survivor scheme used below. Its declared base
is the intersection with the `GLD80` affine neighborhood containing the
Gaussian point `F_0`. No assertion about a point outside that intersection or
in another gauge is made.

Keep the original fixed nuisance map

```text
b: K^79 -> K^81,                 rank b=44.
```

The `GLD70` rows and columns select the constant unit pivot

```text
theta_0=510015580149921683079168 != 0.                 (2)
```

Its fixed right inverse gives a polynomial section `alpha_piv(F)` of
`b alpha=T(F)` modulo the survivor ideal. Let

```text
e_V=(1/6) sum_(sigma in S_3) rho_raw(sigma).
```

Add the fixed invariant-kernel calibration `k_*` recorded by the builder and
put

```text
bar(alpha)_0(F)=e_V alpha_piv(F)+k_*.
```

Choose the fixed Gaussian-calibrated invariant kernel basis

```text
V_0=(v_0,...,v_7),       (ker b)^(S_3)=span_K(V_0).     (3)
```

The displayed builder minor of `V_0` is `-6912+6912i`, so (3) introduces no
moving basis divisor. Every invariant raw preimage is uniquely
`bar(alpha)_0(F)+V_0u`.

## 2. Exact Reynolds compression

For every leaf permutation and each root index separately, the complete
interface satisfies

```text
b rho_raw(sigma)=rho_ten(sigma)b,
H_r rho_raw(sigma)=rho_ten(sigma)H_r,       r=0,1,2,3, (4)
```

and the thirteen-dimensional `Q`/eta-residual constant block is preserved.
The independent symbolic covariance audit proves (4) over the universal
polynomial port ring for all six permutations. The equal-leaf adjugate
specialization therefore preserves it on the frame open below; the root
index is not permuted.

Suppose a full raw preimage has the necessary three-column rank-one response.
Its three quotient classes are proportional, including every zero-column and
rank-drop case. Applying the same quotient Reynolds map to all three classes
preserves proportionality. By (4), the result is the response of the averaged
full preimage, which has the form `bar(alpha)_0+V_0u`. Conversely, an invariant
raw preimage is already a full raw preimage. Thus the affine base images of
the full and invariant necessary incidences agree exactly.

This averaging occurs intrinsically in the quotient by the stable constant
block. The fixed thirteen-row coordinate chart introduced in Section 3 need
not itself be an equivariant choice of representatives.

This does not assert that the bilinear lift equation itself is Reynolds-
equivalent. Only the proved necessary rank-one consequence is compressed.

## 3. Fraction-free moving literal-Delta quotient

Put

```text
d(F)=det(A) det(G)^3,
delta_gauge(F)=product_(u=1)^3 product_(c=0)^2 (F_u)_(0,c),
Omega(F)=delta_gauge(F)d(F).                            (5)
```

In the normalized chart `delta_gauge=1`. Define the polynomial tensor
transport

```text
U_num(F)=adj(A) tensor adj(G) tensor adj(G) tensor adj(G).
```

On `D(d)`, this is `d U_F`, where `U_F` sends `T(F)` to literal `Delta_4`.
For the three demanded response directions it gives

```text
U_num(F) R(F)=d(F) Diag,                                (6)
```

up to the allowed common invertible monomial change of the three response
columns. Thus the transported target is exactly the diagonal response space.
Let `C` be the fixed `81 x 13` `Q`/eta-residual response block and let
`pi_mix` retain the 78 non-diagonal tensor words. Set

```text
C_num(F)=pi_mix U_num(F) C.
```

Use the following positions in the ordered mixed-word list:

```text
I_gamma=(0,1,2,3,4,5,7,8,9,11,17,27,53),
gamma_num(F)=det C_num(F)[I_gamma,:].                   (7)
```

Let `J_gamma` be the ordered complement. For a 78-row matrix `v`, define

```text
Q_num,F(v)=
 gamma_num v[J_gamma,:]
 -C_num[J_gamma,:] adj(C_num[I_gamma,:]) v[I_gamma,:]. (8)
```

Formula (8) is polynomial and denominator-free. On `D(gamma_num)` it is
`gamma_num` times the ordinary quotient by the constant block.

For homogeneous coordinates

```text
y=(u_0,...,u_7,s) in P^8,
```

form the polynomial linear columns

```text
Zhat_r(F;y)=Q_num,F(
 pi_mix U_num(F) H_r(s bar(alpha)_0(F)+V_0u)), r=0,1,2. (9)
```

The matching partition retains the fourth root column through
`Z_0+Z_1+Z_2-Z_3=0`. The complete legal response incidence therefore implies

```text
rank[Zhat_0 Zhat_1 Zhat_2]<=1                         (10)
```

on `D(Omega gamma_num)`. No response minor or nonzero column is selected.

At `F_0`, the exact builder obtains

```text
d(F_0)=24-24i,
gamma_num(F_0)=-692533995824480256(1+i),               (11)
```

both nonzero.

## 4. The forty-five quadratic coefficient determinant

For quotient rows `p<q` and response columns `c<d`, let

```text
q_(p,q;c,d)(F;y)
 =Zhat_c(F;y)_p Zhat_d(F;y)_q
 -Zhat_d(F;y)_p Zhat_c(F;y)_q.                         (12)
```

Order the 45 degree-two monomials by pairs `(i,j)` with
`0<=i<=j<=8` in lexicographic order. Select these 45 quadrics:

```text
(2,3,0,1)   (2,3,0,2)   (2,3,1,2)
(2,6,0,1)   (2,6,0,2)   (2,6,1,2)
(2,14,0,1)  (2,14,0,2)  (2,14,1,2)
(2,15,0,1)  (2,15,0,2)
(2,16,0,1)  (2,16,0,2)  (2,16,1,2)
(2,18,0,1)  (2,18,0,2)  (2,18,1,2)
(2,19,0,1)  (2,19,0,2)  (2,19,1,2)
(2,22,0,1)
(2,27,0,1)  (2,27,0,2)  (2,27,1,2)
(3,6,0,1)   (3,6,0,2)   (3,6,1,2)
(3,14,0,1)  (3,14,0,2)  (3,14,1,2)
(3,15,0,1)  (3,15,0,2)
(3,16,0,1)  (3,16,0,2)  (3,16,1,2)
(3,18,0,1)  (3,18,0,2)  (3,18,1,2)
(3,19,0,1)
(6,14,0,1)  (6,14,0,2)  (6,14,1,2)
(6,16,0,1)  (6,16,1,2)
(16,18,0,1).                                           (13)
```

Let `M_ff(F)` be their `45 x 45` coefficient matrix, with monomials indexing
rows and (13) indexing columns. Equations (2)--(9), (12), and (13) are the
portable exact arithmetic circuit for every entry. This defines the
polynomial in (1) without a term order or hidden denominator.

All entries of `M_ff` and its determinant are ambient polynomials in the frame
variables. In Theorem 4.1 they are restricted to the declared survivor scheme.

The moving builder specializes at `F_0`, divides only by the verified nonzero
values in (11), and matches all 2,025 entries of the byte-pinned Gaussian
matrix. Its exact determinant is

```text
-378089878893442723106646837537745718758189247729870198909680050358976512
 /205891132094649
+25931419533924809154531852205198475327334321064667678574124775287933632512
 /1853020188851841 i !=0.                               (14)
```

The certificate SHA-256 is

```text
4cdaf08a5f5dc40abc845d4dc1e6046ce3b259b2c751dfd3ec2955e5b94e65e0. (15)
```

Indeed, if `M_0` denotes the normalized Gaussian matrix, then

```text
M_ff(F_0)=(d(F_0) gamma_num(F_0))^2 M_0,
det M_ff(F_0)=(d(F_0) gamma_num(F_0))^90 det M_0 !=0.   (16)
```

### Theorem 4.1 (explicit fraction-free principal open)

The projective invariant rank-one incidence (9)--(12) is empty over every
geometric point of `D(Delta_82)` in the declared survivor chart. Consequently
every raw coefficient preimage there fails the complete legal first-response
condition.

#### Proof

On `D(det M_ff)`, the 45 selected quadrics form a basis of the 45-dimensional
space of quadrics in `y_0,...,y_8`. Their ideal therefore contains every
`y_j^2`. A common projective zero would have every `y_j=0`, impossible.

If any full raw preimage admitted a legal first response, (10) would hold.
Section 2 would give an invariant affine solution, hence the projective point
`[u:1]` in (9), contradicting the empty projective incidence. The factors
`Omega` and `gamma_num` make every covariance and quotient step legal.
`square`

### Corollary 4.2 (physical maximal-star source branch)

No complex Krenn--Gu witness on the `GLD81` root-order-four, surplus-two,
fully-supported, rank-three, nonisotropic maximal-star source branch can have
an induced normalized survivor frame in `D(Delta_82)`.

#### Proof

`GLD81` sends every such physical source and its physical raw coefficients to
the complete legal response incidence. Theorem 4.1 excludes it. `square`

## 5. Residual obligations and hostile controls

The named residual alternatives are:

1. `det M_ff=0` in the frame and quotient open;
2. `gamma_num=0`;
3. a frame/gauge divisor in `Omega=0`;
4. another survivor component or frame gauge; or
5. a lower-rank port, smaller survivor family, maximal triangle, residual
   coordinate boundary, isotropic slope, other root/surplus profile, or
   non-leading source branch.

The fixed `GLD70` support and nonisotropic conditions are branch hypotheses,
not moving-frame denominators. They are not discarded or promoted beyond
their declared scope.

Hostile controls:

- `GLD72` remains an exact concise GHZ tensor in `N_star`; it is excluded only
  from legal first response.
- The `GLD70` `Q` generator and epsilon are not used as GHZ-membership tests.
- Every raw preimage is retained before Reynolds projection. The exact
  symbolic audit proves individual-root covariance and the averaged
  necessary-condition implication.
- The intrinsic minors retain zero columns and every response-rank drop.
- The homogenizing coordinate `s` retains escape to infinity in the invariant
  compactification. No classification of the full non-invariant projective
  boundary is claimed or needed for affine base-image exclusion.
- Literal-Delta transport uses the complete interface and the adjugate
  numerator. The invalid untransported moving `65 x 3` shortcut is not used.
- Frame nonuniqueness is controlled only in the certified `GLD75`--`GLD80`
  gauge.
- The result is a fixed-star principal-open theorem and named physical-source
  corollary, not divisor coverage or global resolution.

## 6. Verification

Run:

```powershell
python claims/arbitrary-order/four_root_torus_star_survivor_moving_response_builder.py
python claims/arbitrary-order/verify_four_root_torus_star_survivor_invariant_quadratic_macaulay_principal_open_nonextension.py
python -I claims/arbitrary-order/audit_four_root_torus_star_survivor_moving_response_covariance.py
python -I claims/arbitrary-order/audit_four_root_torus_star_survivor_invariant_quadratic_macaulay_principal_open_nonextension.py
```

The builder constructs the exact polynomial circuit and proves that its
normalized Gaussian specialization matches the stored matrix entry for entry.
The primary verifier independently reconstructs the physical `GLD74` quotient,
the invariant raw block, the 45 named quadrics, their determinant, certificate
bytes, and quotient fingerprint. The moving covariance audit proves the
universal leaf-permutation and recentered Reynolds identities. The final
no-import audit parses `Q(i)` independently and recomputes the stored `45 x 45`
determinant by fraction Gaussian elimination; it does not independently
rederive the physical quotient.
