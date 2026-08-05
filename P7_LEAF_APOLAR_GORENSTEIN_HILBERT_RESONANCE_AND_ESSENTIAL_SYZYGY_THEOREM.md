# P7 leaf annihilators have a Gorenstein Hilbert and resonance branch split

## Status

**Exact characteristic-zero apolar Hilbert classification and non-forcing
theorem for the two physical leaf-annihilator branches.**  Let

```text
A=K[z_1,...,z_7]/(z_1^2,...,z_7^2)
```

and let `F in A_2` have all 21 edge coefficients nonzero.  For each degree
put

```text
mu_r(F):A_r->A_(r+2),                 X -> XF,
Ann_r(F)=ker mu_r(F).                                 (1)
```

Continue from
`P7_PHYSICAL_LEAF_ANNIHILATOR_EXTENSION_AND_QUOTIENT_SYZYGY_THEOREM.md`.
A physical P7 extension forces

```text
ell F^2=0,
rho=rank mu_2(F)<=20.                                (2)
```

This note proves the exact Hilbert classification

```text
H_(A/Ann(F))=(1,7,rho,rho,7,1).                     (3)
```

The quotient is an Artinian Gorenstein algebra of socle degree five.  Full
edge support is used sharply: it forces `Ann_1(F)=0`.

Let

```text
d_2=dim Ann_2(F)=21-rho,
E_3(F)=Ann_3(F)/(A_1 Ann_2(F)),
beta_3=dim E_3(F).                                   (4)
```

Then

```text
dim Ann_3(F)=35-rho,
beta_3>=max(0,6rho-112).                             (5)
```

Consequently the physical branches separate exactly as follows.

```text
rho=20: one quadratic annihilator and beta_3>=8;
rho=19: two quadratic annihilators and beta_3>=2;
rho<=18: Hilbert growth alone forces no essential cubic.    (6)
```

On `rho=20`, if the unique quadratic annihilator `K` is itself full-edge,
then multiplication `A_1->A_3` by `K` is injective and

```text
beta_3=8 exactly.                                    (7)
```

The structured quotient-singular cubic

```text
C_G=2AG-t(partial G)F                                (8)
```

must lie in `Ann_3(F)`.  Equation (6) gives the exact trichotomy: `C_G` can
vanish, can be a linear multiple of a quadratic annihilator, or can define
an essential class in `E_3(F)`.  Hilbert dimensions alone exclude none of
these three possibilities.  In particular, the rank-20 structured map is
square for a structural reason, while rank 19 is automatically singular and
rank at most 18 is a genuinely deeper resonance problem.

This is a rigorous non-forcing theorem, not a physical construction.  No
full-edge primitive `F` in either branch is produced.  Both branches, P7,
and global Krenn--Gu remain **UNKNOWN/UNRESOLVED**.

## 1. Full-edge quadratics have no linear annihilator

### Lemma 1 (support-free linear injectivity)

If every coefficient `f_ij` of `F` is nonzero, then

```text
LF=0 with L=sum_i l_i z_i   =>   L=0.               (9)
```

### Proof

The coefficient on a triple `{i,j,k}` is

```text
l_i f_jk+l_j f_ik+l_k f_ij=0.                       (10)
```

There are three cases.

1. If every `l_i` is nonzero, divide (10) by `l_i l_j l_k` and put
   `g_ij=f_ij/(l_i l_j)`.  Then

   ```text
   g_ij+g_ik+g_jk=0
   ```

   on every triple.  The unsigned inclusion map `W=W_(2,3)(7)` has full
   column rank 21 in characteristic zero.  Symbolically,

   ```text
   W^T W=5I+Adj(L(K_7)),
   ```

   and the three eigenvalues are `15,8,3`, on spaces of dimensions
   `1,6,14`.  Thus every `g_ij=0`, contradicting full support of `F`.
2. If exactly one coefficient, say `l_i`, vanishes, then for distinct
   `j,k!=i`, equation (10) becomes

   ```text
   l_j f_ik+l_k f_ij=0.
   ```

   With `r_j=f_ij/l_j`, this says `r_j+r_k=0` for every pair among six
   indices.  If `B` is the unsigned vertex-edge incidence matrix of `K_6`,
   then

   ```text
   B^T B=4I+J,
   ```

   whose eigenvalues are `10` and `4`.  Hence `B` has rank six, so every
   `r_j=0`, again contradicting full support.
3. If two coefficients `l_j,l_k` vanish while some `l_i` does not, (10)
   gives `l_i f_jk=0`, immediately contradicting full support.

Thus no nonzero `L` exists.  The same proof applies to every other
full-edge quadratic, including a full-edge extension annihilator `K`.

## 2. The multiplication annihilator is Gorenstein

The graded multiplication annihilator

```text
Ann(F)={X in A:XF=0}                                 (11)
```

is an ideal.  Define a top functional on the quotient by

```text
lambda([X])=[z_1...z_7]XF.                          (12)
```

For every `r`, the induced pairing

```text
(A/Ann(F))_r x (A/Ann(F))_(5-r) -> K,
([X],[Y]) -> lambda([XY])                            (13)
```

is perfect.  Indeed, if `XF!=0` in `A_(r+2)`, the ordinary complementary
Boolean pairing supplies a `Y in A_(5-r)` for which the top coefficient of
`XYF` is nonzero.  Its radical is therefore exactly `Ann_r(F)`, on both
sides.  This proves that `A/Ann(F)` is Artinian Gorenstein with socle degree
five.

The degree-`r` quotient dimension is `rank mu_r(F)`.  Lemma 1 gives

```text
rank mu_0=1,
rank mu_1=7.                                         (14)
```

The same top pairing identifies `mu_3(F)` with the complemented transpose
of `mu_2(F)`, and `mu_4(F)` with the complemented transpose of `mu_1(F)`.
Finally `mu_5(F)` has rank one because `F!=0`.  Hence

```text
(rank mu_0,...,rank mu_5)=(1,7,rho,rho,7,1),        (15)
```

which proves (3).

For comparison, the uniform switching family

```text
F_s=sum_(i<j)s_i s_j z_i z_j,              s_i!=0, (16)
```

has `rho=21`, so its Hilbert vector is `(1,7,21,21,7,1)`.  The coordinate
boundary `F=z_1(z_2+...+z_7)` has vector `(1,6,15,15,6,1)`.  These fixed
controls show both where full support enters Lemma 1 and that Gorenstein
symmetry itself does not impose the physical rank drop.

For (16), the diagonal Boolean-algebra automorphism `z_i -> s_i z_i`
reduces every nonzero switching vector to the all-ones control, so this is a
family statement rather than a sampled specialization.

## 3. Essential cubic annihilators

The degree-three part of the annihilator has dimension

```text
dim Ann_3(F)=dim A_3-rank mu_3(F)=35-rho.            (17)
```

Quadratic annihilators generate a subspace

```text
A_1 Ann_2(F) subset Ann_3(F).                        (18)
```

Since `dim A_1=7` and `dim Ann_2(F)=21-rho`,

```text
dim(A_1 Ann_2(F))<=7(21-rho).                       (19)
```

Quotienting (17) by (18) gives

```text
beta_3
 =35-rho-dim(A_1 Ann_2(F))
 >=35-rho-7(21-rho)
 =6rho-112.                                          (20)
```

Together with `beta_3>=0`, this proves (5)--(6).

### Rank 20

Here `Ann_2(F)=span{K}` is one line and `dim Ann_3(F)=15`.  More explicitly,

```text
beta_3=15-rank(mu_1(K):A_1->A_3).                   (21)
```

Thus `beta_3>=8`.  If `K` is full-edge, Lemma 1 gives rank seven and
`beta_3=8`, proving (7).  If `K` fails to have full edge support, the loss of
rank in multiplication by `K`, if any, can only increase `beta_3`; it never
removes the eight-dimensional lower bound.

The structured map `G -> C_G` has a 20-dimensional source, while

```text
dim A_3/Ann_3(F)=rho=20.                             (22)
```

This is why the rank-20 quotient-syzygy condition is a genuinely square
determinant after the unique extension annihilator is fixed.  The Hilbert
function neither forces nor forbids its determinant to vanish.

### Rank 19

Here `dim Ann_2(F)=2`, `dim Ann_3(F)=16`, and (20) gives

```text
beta_3>=2.                                           (23)
```

At the same time the structured map has source dimension 20 and target
quotient dimension 19.  Therefore it has a nonzero kernel before any
additional determinant is imposed.  This recovers the automatic quotient
singularity of the leaf-rank-19 physical branch and shows that at least two
cubic annihilator classes cannot be generated by its two quadratics.

### Rank at most 18

For `rho<=18`, the universal estimate in (20) is nonpositive.  The number
of essential cubics is governed by the actual resonance rank of

```text
A_1 tensor Ann_2(F) -> Ann_3(F).                     (24)
```

Thus neither the rank-20 count nor the rank-19 lower bound controls this
deeper branch.  Quotient rank at most 18 still requires at least two
independent structured `G`, as proved in the preceding package, but the
Hilbert vector alone cannot identify them.

## 4. Exact structured-syzygy trichotomy

On a physical extension, the factorization

```text
2t Phi_N(G)=F C_G                                   (25)
```

shows that quotient singularity is `C_G in Ann_3(F)`.  Relative to (18),
there are exactly three algebraic possibilities:

```text
C_G=0;
C_G in A_1 Ann_2(F) minus {0};
[C_G]!=0 in E_3(F).                                  (26)
```

They correspond respectively to a resonance of the structured source map,
a cubic syzygy generated by the extension annihilators, and an essential
new cubic annihilator.  The cases are exhaustive and disjoint.  Equations
(6), (21), and (23) describe the available essential space but do not force
the physical `C_G` into or out of it.

This is the precise non-forcing boundary: Hilbert theory explains the
dimensions and minimal generators, while the remaining Krenn--Gu question
is the incidence of the special tensor `C_G=2AG-t(partial G)F` with those
spaces.

## 5. Literature translation

The perfect-pairing argument is the square-free inverse-system form of the
standard Artinian Gorenstein construction; the broader inverse-system
correspondence is developed by
[Elias--Rossi](https://arxiv.org/abs/1705.05686).  Hilbert functions and
Lefschetz behavior of Artinian Gorenstein algebras are discussed, for
example, by [Altafi](https://arxiv.org/abs/2007.10684).  The ambient
square-free monomial complete intersection has the characteristic-zero
strong Lefschetz property described by
[Cook](https://arxiv.org/abs/1111.4979), while the Boolean `sl_2`
decomposition behind the `1+6+14` spectral split is developed by
[Feinsilver](https://arxiv.org/abs/1102.0368).

The next natural translation is higher- or mixed-Hessian geometry: such
criteria turn ranks of multiplication maps in Artinian Gorenstein algebras
into determinantal loci, as in
[Gondim--Zappala](https://arxiv.org/abs/1601.04454).  That suggests a
coordinate-free way to study the remaining special incidence of `C_G`, but
no Hessian criterion currently proves or excludes a physical point here.

Those sources supply the established framework.  The full-edge injectivity
Lemma 1, the physical Hilbert vector (3), and the essential-syzygy split
(6) are the exact new translations used here.

## 6. Exact wall

```text
full-edge F has Ann_1(F)=0:                              PROVED;
A/Ann(F) is Gorenstein of socle degree five:              PROVED;
physical leaf Hilbert vector:                             (1,7,rho,rho,7,1);
rank-20 quadratic annihilator dimension:                  ONE;
rank-20 essential cubic annihilators:                     AT LEAST EIGHT;
rank-20 with full annihilator K:                          EXACTLY EIGHT;
rank-19 quadratic annihilator dimension:                  TWO;
rank-19 essential cubic annihilators:                     AT LEAST TWO;
rank-at-most-18 essential-cubic lower bound from Hilbert: NONE;
structured cubic trichotomy (26):                         EXHAUSTIVE;
Hilbert data forces rank-20 structured determinant zero:  NO;
Hilbert data excludes rank-20 determinant zero:           NO;
Hilbert data resolves rank-at-most-18 resonance:           NO;
full-edge primitive F with rho=20 and physical extension:  UNKNOWN;
full-edge primitive F with rho<=19 and physical extension: UNKNOWN;
physical quotient-singular P7 point:                       UNKNOWN;
global Krenn--Gu:                                          UNRESOLVED. (27)
```

No graph/support enumeration, parameter sweep, numerical approximation,
finite-field inference, Groebner elimination, or timeout enters the proof.

## Replay

```powershell
uv run --with sympy python verify_p7_leaf_apolar_gorenstein_hilbert_resonance_and_essential_syzygy.py
python audit_p7_leaf_apolar_gorenstein_hilbert_resonance_and_essential_syzygy.py
python -m py_compile verify_p7_leaf_apolar_gorenstein_hilbert_resonance_and_essential_syzygy.py audit_p7_leaf_apolar_gorenstein_hilbert_resonance_and_essential_syzygy.py
uv run --with ruff ruff check verify_p7_leaf_apolar_gorenstein_hilbert_resonance_and_essential_syzygy.py audit_p7_leaf_apolar_gorenstein_hilbert_resonance_and_essential_syzygy.py
```

The primary verifier checks both injectivity case matrices, all adjoint
multiplication maps, the two exact Hilbert controls, and every branch formula
for `rho=0,...,20`.  The independent standard-library audit rebuilds the
Boolean multiplication ranks, complementary pairings, and essential-syzygy
bounds without importing the primary or project code.
