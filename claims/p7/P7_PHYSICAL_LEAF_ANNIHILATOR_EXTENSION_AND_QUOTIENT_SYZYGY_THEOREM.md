# Physical P7 extension is a leaf annihilator and quotient-syzygy incidence

## Status

**Exact characteristic-zero physical-intersection reduction.**  Work in the
seven-leaf Boolean algebra

```text
A(L)=K[z_1,...,z_7]/(z_1^2,...,z_7^2),
ell=z_1+...+z_7.
```

This continues
`P7_PRIMITIVE_BOOLEAN_SQUARE_COMPLEMENT_RADIAL_AND_EXCEPTIONAL_CLIQUE_THEOREM.md`
and
`P7_PRIMITIVE_QUOTIENT_SINGULAR_APOLAR_RADIAL_BILINEAR_INCIDENCE_THEOREM.md`.

Let `F in A_2(L)` have every edge coefficient nonzero, put

```text
N=F^2/2,
ell N=0,
J(z_S)=z_(L minus S).                               (1)
```

The preceding radial theorem asks for a full-support linear form `A` and a
nonzero scalar `t` satisfying

```text
AF=t JN.                                             (2)
```

This note proves that (2) is equivalent to one quadratic annihilator:

```text
K=2 ell A+tF,
FK=0.                                                (3)
```

Conversely, every nonzero `K in Ann_2(F)` whose class modulo `ell A_1`
is a nonzero multiple of the class of `F` reconstructs `[A:t]`; it gives a
full-edge P7 primitive square exactly when all seven coefficients of the
recovered `A` are nonzero.  Thus a physical P7 extension is equivalent to
a projective incidence inside the degree-two annihilator of its P6-order
leaf square.

In particular, multiplication

```text
mu_2(F):A_2(L)->A_4(L),              W -> FW        (4)
```

must have rank at most 20.  On the minimal rank-20 branch, `Ann_2(F)` is one
line and the extension condition is one exact quotient collinearity test.
The rank-at-most-19 leaf branch is retained separately.

The quotient-singular condition also factors through multiplication by the
same `F`.  For `G` in the 20-dimensional total-zero leaf-edge space, put

```text
d=partial G,
C_G=2AG-t dF in A_3(L).                              (5)
```

Then

```text
2t Phi_N(G)=F C_G.                                   (6)
```

Hence quotient singularity is exactly the existence of a nonzero structured
cubic syzygy

```text
C_G in Ann_3(F).                                     (7)
```

The degree-two and degree-three multiplication maps are adjoint, so they
have the same rank.  This yields an exact rank comparison and separates
the branches:

```text
rank(D|P)<=rank mu_2(F)<=20;                         (8)

rank mu_2(F)<=19  => quotient singular automatically;
rank mu_2(F)=20    => one leaf annihilator K, then test (7);
rank(D|P)<=18      <=> at least two independent G solve (7). (9)
```

This is a support-free descent and factorization, not an emptiness proof.
Whether either physical branch in (9) meets the full edge torus remains
**UNKNOWN**.  P7 and global Krenn--Gu remain **UNRESOLVED**.

## 1. The seven-leaf Lefschetz identities

The Boolean strong Lefschetz maps used below are

```text
ell:A_3(L)->A_4(L),
ell^3:A_2(L)->A_5(L).                               (10)
```

Both are isomorphisms in characteristic zero: their source and target
dimensions are 35 and 21 respectively, and each is the corresponding
middle unsigned inclusion matrix with nonzero Boolean `sl_2` eigenvalues.

Because `N` in (1) is a primitive leaf four-form,

```text
N+ell JN=0.                                          (11)
```

These two facts turn the radial complement equation into an annihilator
statement without losing a component or inverting a graph coordinate.

## 2. Exact leaf-annihilator extension theorem

### Theorem 1 (radial extension equals a quadratic zero divisor)

Assume (1).  For any `A in A_1(L)` and `t in K^*`, equations (2) and (3)
are equivalent.

### Proof

If `AF=t JN`, multiply by `ell` and use (11):

```text
F ell A=t ell JN=-tN=-tF^2/2.
```

After multiplying by two, this is `F(2ell A+tF)=0`.

Conversely, assume `FK=0`.  Then

```text
ell(AF-t JN)
 =F ell A-t ell JN
 =-tN+tN=0.                                         (12)
```

The first map in (10) is injective, so `AF-t JN=0`.  This proves the
equivalence.

There is a useful denominator-free master identity, valid before imposing
primitivity:

```text
FK=2ell(AF-t JN)+2t(N+ell JN).                      (13)
```

Thus (11) is exactly the term needed to turn the zero product back into the
radial equation.

### Corollary 2 (the annihilator is genuinely nonzero)

If all coefficients of `A` are nonzero, then the `K` in (3) cannot vanish.

### Proof

If `K=0`, then `F=-2ell A/t`.  Primitivity gives

```text
0=ell F^2=(4/t^2)ell^3 A^2.
```

The second map in (10) is injective, so `A^2=0`.  In characteristic zero,

```text
A^2=2 sum_(i<j)a_i a_j z_i z_j,
```

which permits at most one nonzero coefficient of `A`, a contradiction.

The same argument proves another required nondegeneracy:

```text
F full-edge and ell F^2=0  =>  F notin ell A_1.      (14)
```

Indeed, writing `F=ell B` would force `B^2=0`, after which `F` has at most
one star of nonzero edges.

## 3. Projective extension incidence

Let

```text
C=ell A_1(L) subset A_2(L),             dim C=7,
pi:A_2(L)->A_2(L)/C,                    dim quotient=14. (15)
```

Multiplication by `ell:A_1->A_2` is injective.  Theorem 1 gives the exact
criterion below.

### Theorem 3 (P6-order leaf square to P7 extension)

A full-edge `F` satisfying (1) extends to a full-edge primitive P7 quadratic

```text
Q=z_0 A+tF                                             (16)
```

if and only if there are `K in Ann_2(F)` and `t in K^*` such that

```text
pi(K)=t pi(F),
K-tF=2ell A,                                         (17)
```

and all seven coefficients of the uniquely recovered `A` are nonzero.

### Proof

The forward direction is (3).  Conversely, (17) defines `A` uniquely;
Theorem 1 gives `AF=tJN`.  Then

```text
Q^2/2=t z_0 AF+t^2N=t^2(z_0 JN+N),                  (18)
```

which is primitive by (1) and (11).  Full support of `F,A,t` is exactly
full support of the reconstructed graph.  Equation (14) ensures
`pi(F)!=0`, so the multiplier `t` in (17) is a genuine nonzero projective
coordinate.

Let `rho=rank mu_2(F)`.  Theorem 3 immediately forces

```text
rho<=20,                    dim Ann_2(F)=21-rho.      (19)
```

On `rho=20`, choose the unique projective generator `[K_F]` of the
annihilator.  Extension is equivalent to

```text
pi(K_F) wedge pi(F)=0,
pi(K_F)!=0,                                           (20)
```

followed by the seven explicit nonvanishing checks on the incidence lift in
(17).  When permitted, `[A:t]` is unique.  On `rho<=19`, the exact retained
problem is the projective linear incidence

```text
P(Ann_2(F)) intersects P(C+span{F}) with t!=0
and full-support incidence remainder.                (21)
```

No dimension count is promoted to nonemptiness or emptiness.

## 4. Uniform switching family is excluded exactly

The annihilator obstruction is nonvacuous on the full edge torus.  For
nonzero scalars `s_1,...,s_7`, put

```text
F_s=sum_(i<j)s_i s_j z_i z_j.                        (22)
```

The matrix of `mu_2(F_s)` is diagonally equivalent to the unsigned inclusion
matrix `W_(2,4)(7)`:

```text
mu_2(F_s)=diag(s_U) W_(2,4)(7) diag(s_e^(-1)).       (23)
```

The inclusion matrix has full column rank 21 in characteristic zero.
Therefore

```text
Ann_2(F_s)=0,                                        (24)
```

and no member of this entire full-edge switching family can extend through
the primitive P7 radial incidence.  This is a fixed symbolic family control;
it is not a claim about every full-edge `F`.

At the opposite coordinate boundary, let `F=z_1B` and `A=z_1`, with `B` a
linear form in the other leaves.  Then `F^2=AF=0` and

```text
F(2ell A+tF)=0.                                      (25)
```

This exact square-zero family shows why support permission in Theorem 3
cannot be omitted.  It is not a physical torus point.

## 5. Quotient singularity is a cubic syzygy of the same leaf form

Continue with a physical extension `(F,A,t)` from Theorem 3.  Let

```text
G_0={G in A_2(L):sum_(i<j)g_ij=0},
d=partial G=sum_i(sum_(j!=i)g_ij)z_i.
```

The preceding quotient-singular theorem defined

```text
Phi_N(G)=G(JN)-dN.                                   (26)
```

Define `C_G` by (5).  Before imposing radial closure there is the universal
factor identity

```text
F C_G=2t Phi_N(G)+2G(AF-t JN).                       (27)
```

On (2), this becomes (6), proving

```text
Phi_N(G)=0  <=>  C_G in Ann_3(F).                    (28)
```

This is stronger than merely observing that two determinants vanish: the
same full-edge quadratic `F` controls both the extension annihilator `K`
and the structured quotient syzygy `C_G`.

## 6. Adjoint ranks and the exact deep-corank split

Let

```text
mu_3(F):A_3(L)->A_5(L),              C -> FC.        (29)
```

The top-degree Boolean pairing identifies `mu_3(F)` with the transpose of
`mu_2(F)` after complementing the three-/five-set bases.  Hence

```text
rank mu_3(F)=rho,
dim Ann_3(F)=35-rho.                                 (30)
```

Define the structured-syzygy map

```text
Xi_(F,A,t):G_0 -> A_3(L)/Ann_3(F),
G -> [C_G].                                          (31)
```

Equations (6) and the exact conjugacy from the preceding quotient theorem
give

```text
rank(D|P)=rank Xi_(F,A,t)<=rho.                      (32)
```

This proves the branch split advertised in (9).

- If `rho<=19`, every physical extension is quotient singular before any
  additional determinant is tested.
- If `rho=20`, then `Ann_2(F)` is the unique line from (20),
  `dim Ann_3(F)=15`, and quotient singularity is precisely the existence of
  a nonzero `G` whose structured cubic lands in that 15-space.
- Quotient rank at most 18 is the separate incidence

```text
dim ker Xi_(F,A,t)>=2.                               (33)
```

  This is automatic when `rho<=18`; for `rho=19` or `20` it is an additional
  structured rank drop.  It is retained rather than inferred from the
  corank-one analysis.

## 7. Literature translation

The isomorphisms (10) are instances of the strong Lefschetz property for
the square-free monomial complete intersection.  The general characteristic
zero result and its positive-characteristic boundary are discussed by
[Cook](https://arxiv.org/abs/1111.4979); the Boolean-lattice `sl_2`
realization is developed by
[Feinsilver](https://arxiv.org/abs/1102.0368).

The new content is not the abstract Lefschetz property.  It is the physical
extension equivalence (3)/(17), the common-annihilator factorization (27),
and the rank comparison (32) for the Krenn--Gu P7 radial system.

## 8. Exact wall

```text
radial equation AF=tJN <=> quadratic annihilator FK=0:       PROVED;
physical extension annihilator K:                            NONZERO;
full-edge primitive F lies outside ell A_1:                  PROVED;
P6-order leaf-to-P7 extension criterion (17):                NECESSARY/SUFFICIENT;
leaf multiplication rank at a physical extension:           AT MOST 20;
leaf rank-20 extension test:                                 ONE QUOTIENT COLLINEARITY;
leaf rank-at-most-19 extension incidence:                    RETAINED;
uniform switching full-edge family:                          EXACTLY EXCLUDED;
coordinate-boundary square-zero family:                      EXISTS;
quotient singularity <=> structured C_G in Ann_3(F):         PROVED;
quotient rank bounded by leaf multiplication rank:           PROVED;
leaf rank at most 19 implies quotient singular:              PROVED;
quotient rank at most 18:                                    SEPARATE INCIDENCE (33);
rank-20 physical extension satisfying cubic syzygy exists:   UNKNOWN;
rank-at-most-19 physical leaf extension exists:              UNKNOWN;
either physical quotient-singular torus branch is nonempty:  UNKNOWN;
P7 pinned matrix full rank on the primitive torus:           UNKNOWN;
global Krenn--Gu:                                             UNRESOLVED. (34)
```

No graph/support enumeration, numerical approximation, finite-field
inference, parameter sweep, Groebner elimination, or timeout is used.

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_physical_leaf_annihilator_extension_and_quotient_syzygy.py
python claims/p7/audit_p7_physical_leaf_annihilator_extension_and_quotient_syzygy.py
python -m py_compile claims/p7/verify_p7_physical_leaf_annihilator_extension_and_quotient_syzygy.py claims/p7/audit_p7_physical_leaf_annihilator_extension_and_quotient_syzygy.py
uv run --with ruff ruff check claims/p7/verify_p7_physical_leaf_annihilator_extension_and_quotient_syzygy.py claims/p7/audit_p7_physical_leaf_annihilator_extension_and_quotient_syzygy.py
```

The primary verifier checks the two Lefschetz isomorphisms, master identities
(13)/(27), multiplication-map adjointness, the exact rank comparison,
the uniform switching control, and the square-zero boundary family.  The
independent standard-library audit rebuilds all inclusion, multiplication,
complement, quotient, and formal Boolean identities without importing the
primary or project code.
