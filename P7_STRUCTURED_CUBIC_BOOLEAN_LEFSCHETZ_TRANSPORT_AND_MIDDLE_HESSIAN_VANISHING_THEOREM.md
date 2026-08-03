# Physical P7 structured cubics have a canonical Lefschetz kernel

## Status

**Exact characteristic-zero closure of the structured-cubic test conditional
on physical extension.**  Work in

```text
A=K[z_1,...,z_7]/(z_1^2,...,z_7^2),
ell=z_1+...+z_7,
Omega=sum_(i<j)z_i z_j=ell^2/2.                    (1)
```

Let `F in A_2` have all 21 edge coefficients nonzero, and assume the physical
leaf-extension equations from
`P7_PHYSICAL_LEAF_ANNIHILATOR_EXTENSION_AND_QUOTIENT_SYZYGY_THEOREM.md`:

```text
ell F^2=0,
t!=0,
K=2ell A+tF!=0,
FK=0,                                               (2)
```

where `A in A_1` is full support.  For a quadratic `X`, write `sigma(X)` for
the sum of its 21 edge coefficients and put

```text
G_0=ker(sigma:A_2->K),
partial(z_i z_j)=z_i+z_j,
T=I+ell partial:G_0->G_0.                           (3)
```

This note proves that `T` is an automorphism with spectrum

```text
1^(14), 6^6,
T^(-1)=I-(ell partial)/6.                           (4)
```

The following explicit covariant is nonzero:

```text
s=sigma(K),
H=s Omega-21K in G_0,
G=T^(-1)H=H-(ell partial H)/6.                      (5)
```

For `d=partial G`, its physical structured cubic satisfies

```text
C_G=2AG-t dF
   =2AH-dK
   =-(ts/2)ell F+((s/2)ell-42A-d)K in Ann_3(F).    (6)
```

Consequently **every physical P7 leaf extension is quotient singular**.
There is no separate rank-20 structured determinant to test: it vanishes
identically after imposing the physical extension equations.  This includes
the rank-20 and rank-at-most-19 leaf-annihilator strata.  Thus nonemptiness of
the physical quotient-singular extension locus is now equivalent to
nonemptiness of the physical extension locus itself.

Equation (6) also strictly reduces the earlier zero/generated/essential
trichotomy.  In

```text
E_3(F)=Ann_3(F)/(A_1 Ann_2(F))
```

the canonical structured cubic has

```text
[C_G]=-(t sigma(K)/2)[ell F].                       (7)
```

Thus `sigma(K)=0` forces the constructed syzygy to be quadratically
generated.  When `sigma(K)!=0`, its generated-versus-essential placement is
controlled by the single canonical class `[ell F]`; it is essential exactly
when that class is nonzero.

On the rank-20 stratum, the apolar algebra

```text
R_F=A/Ann(F),                 H_R=(1,7,20,20,7,1)   (8)
```

has a nonzero class `[Omega] in (R_F)_2` killed by multiplication by `[A]`.
Hence the middle map

```text
times A:(R_F)_2->(R_F)_3                            (9)
```

is singular, and the second higher Hessian of the Macaulay dual quintic of
`R_F` vanishes at `A`.

This theorem does **not** construct or exclude a full-edge physical
extension.  It proves that quotient singularity is automatic if one exists.
The full-edge physical extension incidence, P7, and global Krenn--Gu remain
**UNKNOWN/UNRESOLVED**.

## 1. Boolean Lefschetz transport on the total-zero hyperplane

Let `U` denote multiplication by `ell` and `D=partial`.  The unsigned
vertex-edge incidence map

```text
D:A_2->A_1
```

has rank seven in characteristic zero.  Its kernel `P_2` therefore has
dimension 14.  Let

```text
P_1={p in A_1:sum_i p_i=0},               dim P_1=6. (10)
```

For `p in P_1`, direct coefficient comparison gives

```text
D(Up)=5p.                                             (11)
```

Both `P_2` and `UP_1` lie in `G_0`, their intersection is zero by (11), and
their dimensions add to 20.  Hence

```text
G_0=P_2 direct_sum UP_1.                              (12)
```

On these two summands, `UD` has eigenvalues zero and five.  Therefore

```text
T=I+UD acts by 1 on P_2 and by 6 on UP_1.            (13)
```

This proves the spectrum in (4).  Equivalently, on `G_0`,

```text
(UD)^2=5UD,
(I+UD)(I-UD/6)=I.                                    (14)
```

This is the exact Boolean `sl_2` transport needed below.  It is not a
generic-rank assertion and involves no specialization of `F`.

## 2. A canonical quadratic transported from the physical annihilator

First, `K` and `Omega` are linearly independent.  Indeed,

```text
Omega=ell(ell/2) in ell A_1.
```

If `K` were proportional to `Omega`, then (2) would give

```text
tF=K-2ell A in ell A_1,
```

contradicting the previously proved fact that a full-edge primitive `F`
cannot lie in `ell A_1`.

The physical equations imply two cubic annihilators:

```text
AK in Ann_3(F),
AOmega in Ann_3(F).                                  (15)
```

The first follows from `FK=0`.  For the second, multiply the definition of
`K` by `ell F`:

```text
ell FK=4FAOmega+t ell F^2.                           (16)
```

Both terms on the left and the final term on the right vanish by (2), so
`FAOmega=0` in characteristic zero.

Now set `s=sigma(K)` and define `H` by (5).  Since

```text
sigma(Omega)=21,
```

one has `sigma(H)=0`.  The linear independence of `Omega,K` shows `H!=0`:
if `s=0`, then `H=-21K`; if `s!=0`, the equation `H=0` would make `K`
proportional to `Omega`.  Equation (15) gives

```text
AH in Ann_3(F).                                      (17)
```

Finally use (4) to define the nonzero `G=T^(-1)H in G_0` in (5).

## 3. Exact structured-cubic covariant

For an arbitrary `G in G_0`, put `d=partial G`.  Substitution of
`tF=K-2ell A` gives the universal identity

```text
C_G=2AG-t dF
   =2A(G+ell d)-dK
   =2AT(G)-dK.                                      (18)
```

For the `G` in (5), `T(G)=H`; hence

```text
C_G=2AH-dK in Ann_3(F)                              (19)
```

by (17) and `K in Ann_2(F)`.  The factor identity from the preceding package
then gives

```text
2t Phi_N(G)=FC_G=0.
```

Since `t` and `G` are nonzero, this is a genuine quotient-singular direction.

There is a sharper exact formula.  Multiplying `K=2ell A+tF` by `ell`
and using (1) yields

```text
4AOmega=ell K-t ell F.                              (20)
```

Using `H=sOmega-21K` in (19), equations (19)--(20) give

```text
C_G
 =2sAOmega-42AK-dK
 =-(ts/2)ell F+((s/2)ell-42A-d)K,                  (21)
```

which is (6).  The second term belongs to `A_1 Ann_2(F)`, proving (7).

For this forced canonical witness, the earlier trichotomy is therefore no
longer an unconstrained placement:

```text
s=0       => the canonical C_G is generated (possibly zero);
s!=0 and [ell F]=0  => it is generated (possibly zero);
s!=0 and [ell F]!=0 => it is essential and nonzero. (22)
```

Exact vanishing inside the first two lines is the remaining linear equation

```text
2AH=(partial G)K.                                   (23)
```

It is irrelevant to quotient singularity, which already follows from (19).

## 4. Apolar quintic and middle-Hessian vanishing on rank 20

Write

```text
F=sum_(i<j)f_ij z_i z_j
```

and introduce the square-free quintic

```text
Psi_F(x)=sum_(|S|=5) f_(L minus S) product_(i in S)x_i. (24)
```

Here `L minus S` is the complementary edge.  Differentiation by the `z_i`
identifies

```text
R_F=A/Ann(F)=K[partial_(x_1),...,partial_(x_7)]/Ann(Psi_F). (25)
```

This is the explicit Macaulay inverse system underlying the perfect pairing
in the preceding apolar-Hilbert theorem.

For degree-two operators `q,r`, the second higher-Hessian bilinear form at
the point `A=sum_i a_i z_i` is

```text
(q,r) -> (qr Psi_F)(a)
       =lambda(qrA),                                (26)
```

where `lambda([X])` is the top coefficient of `XF`.  Thus, after choosing a
basis of `(R_F)_2`, its matrix is the perfect-pairing matrix of
multiplication (9).  Its determinant vanishes exactly when (9) is singular.

Suppose now `rank mu_2(F)=20`.  Then `Ann_2(F)=span{K}`.  The independence
of `Omega,K` proved above implies

```text
[Omega]!=0 in (R_F)_2.                              (27)
```

Equation (15) says

```text
[A][Omega]=0 in (R_F)_3.                            (28)
```

Therefore the rank-20 middle multiplication determinant, equivalently the
second higher Hessian in (26), is exactly zero on the physical incidence.
This is the apolar/Hessian explanation for the explicit structured kernel
in (5), not an additional assumed degeneracy.

The relationship between higher Hessians and multiplication maps in
Artinian Gorenstein algebras is standard; see Gondim--Zappala,
[*On mixed Hessians and the Lefschetz
properties*](https://arxiv.org/abs/1803.09664).  The Boolean `sl_2`
decomposition used in (12)--(14) is developed by
[Feinsilver](https://arxiv.org/abs/1102.0368).  Equations (5), (6), and the
forced physical Hessian zero are the new problem-specific transfer.

## 5. Exact wall

```text
T=I+ell partial on G_0:                              AUTOMORPHISM;
T spectrum and determinant:                         1^14, 6^6 / 6^6;
canonical H=sigma(K)Omega-21K:                       NONZERO, TOTAL ZERO;
canonical G=T^(-1)H:                                NONZERO, TOTAL ZERO;
canonical C_G in Ann_3(F):                          PROVED;
every physical leaf extension is quotient singular: PROVED;
rank-20 structured determinant on physical incidence: ZERO;
rank-20 middle second Hessian at A:                  ZERO;
canonical essential class: -(t sigma(K)/2)[ell F];  PROVED;
sigma(K)=0 canonical placement:                      GENERATED;
sigma(K)!=0 placement:                              CONTROLLED BY [ell F];
canonical cubic itself vanishes:                     NOT FORCED;
full-edge physical leaf extension exists:            UNKNOWN;
full-edge rank-20 physical extension exists:         UNKNOWN;
full-edge rank-at-most-19 physical extension exists: UNKNOWN;
P7 pinned matrix full rank on primitive torus:        UNKNOWN;
global Krenn--Gu:                                     UNRESOLVED. (29)
```

The theorem is conditional on the exact physical extension equations (2).
No graph/support enumeration, parameter sweep, numerical approximation,
finite-field inference, Groebner elimination, or timeout enters the proof.

## Replay

```powershell
uv run --with sympy python verify_p7_structured_cubic_boolean_lefschetz_transport_and_middle_hessian_vanishing.py
python audit_p7_structured_cubic_boolean_lefschetz_transport_and_middle_hessian_vanishing.py
python -m py_compile verify_p7_structured_cubic_boolean_lefschetz_transport_and_middle_hessian_vanishing.py audit_p7_structured_cubic_boolean_lefschetz_transport_and_middle_hessian_vanishing.py
uv run --with ruff ruff check verify_p7_structured_cubic_boolean_lefschetz_transport_and_middle_hessian_vanishing.py audit_p7_structured_cubic_boolean_lefschetz_transport_and_middle_hessian_vanishing.py
```

The primary verifier checks the full `G_0` transport spectrum, the formal
Boolean identities (16), (18), and (21), the canonical covariant, and the
explicit apolar-quintic/Hessian pairing.  The independent standard-library
audit rebuilds the transport operator and every formal identity with its own
sparse polynomial algebra, importing neither the primary verifier nor project
code.
