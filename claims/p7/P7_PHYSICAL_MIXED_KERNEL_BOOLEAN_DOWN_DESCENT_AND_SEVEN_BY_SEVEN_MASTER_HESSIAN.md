# The physical P7 mixed kernel descends to a seven-by-seven master Hessian

## Status

**Exact characteristic-zero compression of the remaining physical-star
incidence.**  Work in the seven-leaf zeon algebra

```text
Z=K[z_1,...,z_7]/(z_1^2,...,z_7^2),
ell=z_1+...+z_7,
A=sum_i a_i z_i,
F=sum_(i<j)f_ij z_i z_j.                            (1)
```

The preceding mixed-Lefschetz obstruction proves that every physical P7
extension satisfies

```text
ell^2 A F=0.                                         (2)
```

This note proves that (2) has a much smaller exact model.  Put

```text
alpha=sum_i a_i,       r_i=sum_(j!=i)f_ij,
R=sum_i r_i,           delta_ij=alpha-2(a_i+a_j).   (3)
```

In seven variables,

```text
ker(ell^2:Z_3->Z_5)=ker(D:Z_3->Z_2),                (4)
```

where `D=sum_i partial_i` is Boolean lowering.  The corrected zeon Leibniz
rule therefore turns (2) into the 21 local edge equations

```text
delta_ij f_ij+a_i r_j+a_j r_i=0.                    (5)
```

This is an exact equivalence, not a further necessary contraction.

Let `M_A` be the complemented `21 x 21` matrix of multiplication by
`ell^2 A`, and let `L_A` be the edge-indexed matrix in (5).  There is one
fixed invertible rational matrix `J`, independent of `A`, such that

```text
M_A=J L_A,
J=2I+(2/3)1 1^T-R_edge^T R_edge,
det J=2^16 3^6.                                      (6)
```

Here `R_edge` is the unsigned vertex--edge incidence matrix of `K_7`.
Thus the former weighted-Kneser determinant is exactly a fixed scalar times
the determinant of the local down-operator system:

```text
det M_A=2^16 3^6 det L_A.                            (7)
```

On the open chart

```text
a_i!=0,       delta_ij!=0 for every i<j,             (8)
```

the matrix determinant lemma compresses all 21 dimensions to seven.  Define

```text
T_ii=1+sum_(j!=i) a_j/delta_ij,
T_ij=a_i/delta_ij                         (i!=j),    (9)

H_A=T diag(a_1,...,a_7).                             (10)
```

Then `H_A` is symmetric and

```text
det M_A
 =2^16 3^6 (product_(i<j)delta_ij) det T
 =2^16 3^6 (product_(i<j)delta_ij)/(product_i a_i)
    det H_A.                                         (11)
```

More strongly, the kernels are explicitly isomorphic.  If
`x in ker H_A`, put `r_i=a_i x_i` and

```text
f_ij=-a_i a_j(x_i+x_j)/delta_ij.                    (12)
```

This gives every vector in `ker M_A`, and every mixed-kernel vector arises
uniquely this way.  It has full edge support exactly when

```text
x_i+x_j!=0                         for every i<j.    (13)
```

Thus, away from the explicit 21 denominator hyperplanes, the physical
mixed-kernel question is one symmetric seven-variable Hessian incidence,
not a 21-variable determinant or a search over leaf graphs.

The exceptional divisors `delta_ij=0` are not discarded.  There (5) forces
`a_i r_j+a_j r_i=0` and leaves `f_ij` to the remaining equations.  The
six-equal-coordinate determinant wall from the preceding theorem lies on
one such exceptional family, confirming that those divisors are essential.

Equations (2)--(13) characterize the necessary mixed kernel, not the entire
physical extension.  A reconstructed `F` must still satisfy primitivity,
the stronger annihilator equation `F(2ell A+tF)=0`, and full support.  The
generic master-Hessian incidence, exceptional divisors, physical P7
extension, and global Krenn--Gu remain **UNKNOWN/UNRESOLVED**.

## 1. Boolean down descent

Let `U` denote multiplication by `ell`.  The Boolean `sl_2` decomposition in
seven variables gives

```text
U^2:Z_3->Z_5,       D:Z_3->Z_2,
rank U^2=rank D=21,
ker U^2=ker D=P_3,               dim P_3=14.         (14)
```

The equality follows on each irreducible string: the degree-three primitive
summand is killed by both maps, and every lower primitive string maps
nontrivially under both.  It can also be checked from the fixed unsigned
subset-inclusion matrices.  This proves (4).

This Boolean `sl_2` framework is the zeon-algebra model developed in Philip
Feinsilver's [*Zeon algebra, Fock space, and Markov
chains*](https://arxiv.org/abs/1102.0368).  The equality of kernels in (4),
the fixed intertwiner below, and the master-Hessian descent are the new
problem-specific deductions here.

The corrected zeon product rule from
`P7_PRIMITIVE_ZEON_HARMONIC_SQUARE_RICCATI_AND_REAL_ROW_CONE_OBSTRUCTION.md`
gives

```text
D(AF)=(DA)F+A(DF)-2sum_i z_i(partial_iA)(partial_iF). (15)
```

Now

```text
DA=alpha,
DF=sum_i r_i z_i,
partial_iA=a_i,
partial_iF=sum_(j!=i)f_ij z_j.
```

The coefficient of `z_i z_j` in (15) is exactly the left side of (5).
Combining this with (4) proves the equivalence `(2) <=> (5)`.

Summing (5) over all edges incident to vertex `i` gives the useful contracted
system

```text
(F a)_i=alpha r_i+(R/2-2r_i)a_i.                    (16)
```

Summing (16) over `i` gives the scalar consequence

```text
sum_i a_i r_i=alpha R/2.                            (17)
```

These are necessary contractions of (5); unlike (5), they are not asserted
to recover the full mixed kernel.

## 2. Fixed equivalence with the weighted Kneser pencil

Index rows and columns by the 21 leaf edges.  Let `R_edge` be the `7 x 21`
unsigned incidence matrix and define `P_A` by

```text
(P_A)_{ij,i}=a_j,       (P_A)_{ij,j}=a_i,           (18)
```

with all other entries zero.  Then (5) is

```text
L_A=diag(delta_ij)+P_A R_edge.                       (19)
```

Let `D_3:Z_3->Z_2` be lowering and let `U_2:Z_3->Z_5` be multiplication by
`ell^2`, with the five-set rows complemented to edges.  Direct subset
incidence gives the fixed identity

```text
U_2=J D_3,                                          (20)
```

where `J` is (6).  Since `L_A=D_3 times A` and
`M_A=U_2 times A`, equation (20) proves `M_A=J L_A`.

The edge permutation module decomposes as

```text
1 direct-sum Std_6 direct-sum V_(5,2),
dimensions 1,6,14.                                  (21)
```

On these three summands, `R_edge^T R_edge` has eigenvalues `12,5,0` and
`1 1^T` has eigenvalues `21,0,0`.  Therefore `J` has eigenvalues

```text
4^1, (-3)^6, 2^14.                                  (22)
```

This proves its invertibility and determinant in (6), hence (7).

At `A=ell`, the two equivalent matrices are useful controls:

```text
L_ell=3I+R_edge^T R_edge,
spec(L_ell)=15^1,8^6,3^14;

M_ell=6 KG(7,2),
spec(M_ell)=60^1,(-24)^6,6^14.                      (23)
```

Their determinant ratio is again `2^16 3^6`.

## 3. Seven-by-seven determinant and kernel

On (8), put `Delta=diag(delta_ij)`.  Equations (18)--(19) and the matrix
determinant lemma give

```text
det L_A=det Delta det(I_7+R_edge Delta^(-1)P_A).     (24)
```

The final matrix in (24) is exactly `T` in (9).  Indeed, one edge `{i,j}`
contributes `a_j/delta_ij` to the `ii` entry and
`a_i/delta_ij` to the `ij` entry.  Since `H_A=T diag(a)`, its off-diagonal
entry is

```text
(H_A)_ij=a_i a_j/delta_ij,
```

and its diagonal entry is

```text
(H_A)_ii=a_i(1+sum_(j!=i)a_j/delta_ij).             (25)
```

This proves symmetry and (11).  Equivalently, `H_A` is the Hessian in `x`
of the rational quadratic master energy

```text
E_A(x)=1/2 sum_i a_i x_i^2
       +1/2 sum_(i<j) (a_i a_j/delta_ij)(x_i+x_j)^2. (26)
```

For the kernel statement, write `r=diag(a)x`.  If `Tr=0` in the `r`
coordinates, set

```text
f=-Delta^(-1)P_A r.                                 (27)
```

Then

```text
R_edge f=r-Tr=r,
L_A f=-P_A Tr=0.                                    (28)
```

Conversely, `L_Af=0` makes (27) mandatory; putting `r=R_edgef` gives
`Tr=0`.  This proves the kernel bijection.  Substituting
`r_i=a_i x_i` into (27) gives (12), and (8) makes its full-support criterion
exactly (13).

## 4. Exact wall

```text
ker(ell^2:Z_3->Z_5)=ker(D:Z_3->Z_2):       PROVED;
mixed kernel iff 21 local edge equations (5):        PROVED;
fixed equivalence M_A=J L_A:                         PROVED;
det J:                                               2^16 3^6;
generic mixed determinant reduced to 7 x 7:          PROVED;
generic symmetric master Hessian H_A:                EXACT;
generic kernel reconstruction (12):                  BIJECTION;
generic full-edge condition x_i+x_j!=0:              IFF;
21 denominator hyperplanes:                          RETAINED;
generic master Hessian has a good kernel vector:      UNKNOWN;
exceptional divisors contain a full-edge kernel:      UNKNOWN;
reconstructed kernel also satisfies primitivity/FK:   UNKNOWN;
full-edge physical P7 extension:                      UNKNOWN;
global Krenn--Gu:                                  UNRESOLVED. (29)
```

No graph, support, parameter, tuple, finite field, numerical point, minor,
or monomial enumeration enters the proof.  The replay checks only universal
Boolean incidence matrices, linear pencils, and fixed rational identities.

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_physical_mixed_kernel_boolean_down_descent.py
python claims/p7/audit_p7_physical_mixed_kernel_boolean_down_descent.py
python -m py_compile claims/p7/verify_p7_physical_mixed_kernel_boolean_down_descent.py claims/p7/audit_p7_physical_mixed_kernel_boolean_down_descent.py
uv run --with ruff ruff check claims/p7/verify_p7_physical_mixed_kernel_boolean_down_descent.py claims/p7/audit_p7_physical_mixed_kernel_boolean_down_descent.py
```

The primary verifier proves the universal `U_2=J D_3` identity, the
symbolic `M_A=J L_A` pencil equality, the determinant constant, and the
master-Hessian factorization/reconstruction.  The independent standard-
library audit rebuilds the incidence operators coefficientwise and checks
the determinant lemma and reconstruction over an exact generic rational
specialization.  Neither imports the other or project code.

## Dependencies

- [P7_PHYSICAL_EXTENSION_MIXED_HARD_LEFSCHETZ_SIGN_CHAMBER_AND_ONE_EXCEPTIONAL_ORBIT_OBSTRUCTION.md](P7_PHYSICAL_EXTENSION_MIXED_HARD_LEFSCHETZ_SIGN_CHAMBER_AND_ONE_EXCEPTIONAL_ORBIT_OBSTRUCTION.md)
- [P7_PRIMITIVE_ZEON_HARMONIC_SQUARE_RICCATI_AND_REAL_ROW_CONE_OBSTRUCTION.md](P7_PRIMITIVE_ZEON_HARMONIC_SQUARE_RICCATI_AND_REAL_ROW_CONE_OBSTRUCTION.md)
