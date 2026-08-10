# Physical P7 extensions avoid the Kähler chamber and every one-exceptional orbit

## Status

**Exact characteristic-zero obstruction on two meaningful full-support
strata, with a mixed-Hodge translation.**  Work in

```text
A=K[z_1,...,z_7]/(z_1^2,...,z_7^2),
ell=z_1+...+z_7.
```

Assume a physical leaf extension as in
`P7_STRUCTURED_CUBIC_BOOLEAN_LEFSCHETZ_TRANSPORT_AND_MIDDLE_HESSIAN_VANISHING_THEOREM.md`:

```text
F in A_2 is full edge,
A=sum_i a_i z_i is full support,
t!=0,
ell F^2=0,
K=2ell A+tF,
FK=0.                                                (1)
```

Multiplying `FK=0` by `ell` and using primitivity gives the new necessary
condition

```text
(ell^2 A)F=0.                                       (2)
```

Thus the `21 x 21` mixed-Lefschetz map

```text
M_A=times(ell^2 A):A_2->A_5                         (3)
```

must be singular and must have a full-edge vector in its kernel.  After
complementing five-sets to edges, its symmetric edge-indexed matrix is

```text
(M_A)_(e,g)=2 sum_(v notin e union g)a_v,   e cap g=empty;
             0,                            otherwise. (4)
```

Equation (4) turns the physical extension problem into a weighted Kneser
mixed-Hessian obstruction depending only on the radial star `A`, before `F`
or `K` is reconstructed.

Two exact exclusions follow.

1. Over the reals, the coefficients `a_i` cannot all have one sign.  Indeed,
   the Boolean algebra is the cohomology ring of `(P^1)^7`; if `A` or `-A`
   has all positive coefficients, mixed Hard Lefschetz says multiplication by
   the three Kähler classes `ell,ell,+/-A` is an isomorphism `A_2->A_5`,
   contradicting (2).
2. Over every characteristic-zero field, no full-support vector with six
   equal coordinates can occur.  Up to permutation it has the form

   ```text
   A=pz_1+q(z_2+...+z_7),                 pq!=0.     (5)
   ```

   The determinant and exceptional kernel of (3) are

   ```text
   det M_A
    =(2(p+2q))^9(-144q^2)^5(-1440q^2);              (6)

   p+2q!=0  => ker M_A=0;
   p=-2q    => dim ker M_A=9,
                every kernel vector has all six z_1z_j coefficients zero.
                                                               (7)
   ```

   The first line contradicts (2); the second contradicts full edge support
   of `F`.  Hence the entire one-exceptional orbit (5), including its sole
   determinant wall, is physically empty.

This is not a global emptiness proof.  A hypothetical real physical
extension must have both positive and negative star coefficients and cannot
have a six-fold repeated coordinate.  The remaining mixed-sign, less
symmetric full-support incidence, P7, and global Krenn--Gu remain
**UNKNOWN/UNRESOLVED**.

## 1. The forced mixed-Lefschetz kernel

From the definition of `K`,

```text
ell FK=2ell^2 AF+t ell F^2.                          (8)
```

Both the left side and the second term on the right vanish by (1).  Since
the characteristic is zero, (2) follows.

Let `e,g` be leaf edges.  Use the degree-two edge monomials as the source
basis and complement each degree-five target monomial to an edge `g`.  The
entry is zero unless `e` and `g` are disjoint.  In the disjoint case the
three missing vertices support the cubic factor from `ell^2 A`, whose
coefficient is twice the sum of their `a`-coefficients.  This proves (4).

Equivalently, let `C_7` be the adjacency matrix of the Kneser graph
`KG(7,2)` and let

```text
w_e=sum_(i in e)a_i,
S=sum_i a_i,
W=diag(w_e).
```

Then

```text
M_A=2(S C_7-WC_7-C_7W).                             (9)
```

This is a fixed linear matrix pencil in the seven star coefficients, not a
sampled determinant or an eliminated shadow.

## 2. Mixed Hard Lefschetz excludes the same-sign real chambers

There is a graded-ring identification

```text
A_R = H^(2*)(X,R),                  X=(P^1)^7,       (10)
```

where `z_i` is the pullback of the positive generator from the `i`th factor.
A linear form `L=sum_i l_i z_i` with every `l_i>0` is a Kähler class.

Assume first that all `a_i>0`.  The mixed Hard Lefschetz theorem applied to
the three Kähler classes

```text
ell, ell, A
```

on the seven-dimensional compact Kähler manifold `X` gives an isomorphism

```text
times(ell^2 A):H^4(X,R)->H^10(X,R).                 (11)
```

Both sides have dimension `binom(7,2)=21`; under (10), this is exactly
`M_A`.  If all `a_i<0`, replace `A` by `-A`; the multiplication map changes
only by a nonzero scalar.  Thus (3) is invertible throughout both same-sign
chambers, contradicting the physical kernel (2).

The same argument applies after multiplying all `a_i` by a common nonzero
real scalar.  It is an exact chamber theorem, not a positivity heuristic.
At the symmetric anchor `A=ell`, the complemented matrix is six times the
`KG(7,2)` adjacency matrix, whose eigenvalues are

```text
60^1, (-24)^6, 6^14.                                (12)
```

The signature is therefore `(15,6)` and, by mixed Hard Lefschetz and
connectedness, remains so throughout the positive chamber.

The mixed theorem used in (11) is due to Dinh--Nguyen,
[*The mixed Hodge--Riemann bilinear relations for compact Kähler
manifolds*](https://arxiv.org/abs/math/0501449).  The paper supplies the
general mixed Hard Lefschetz theorem.  Equations (2), (4), and its use as a
physical P7 star obstruction are the problem-specific transfer.

## 3. Exact `S_6` block diagonalization of the one-exceptional orbit

Now work over an arbitrary characteristic-zero field and impose (5).  Split
the 21 edges into

```text
E_star={1i:2<=i<=7},                    dim 6,
E_int ={ij:2<=i<j<=7},                  dim 15.      (13)
```

Let `C` be the `6 x 15` matrix

```text
C_(i,jk)=1 if i notin {j,k}, and 0 otherwise,        (14)
```

and let `D` be the disjoint-edge adjacency matrix of `KG(6,2)` on
`E_int`.  Formula (4) becomes the exact block matrix

```text
M_A = [ 0       6q C             ]
      [ 6q C^T  2(p+2q) D        ].                 (15)
```

The required representation data are elementary:

```text
CC^T=4I_6+6J_6,                                     (16)

spec(D)=6^1,(-3)^5,1^9.                             (17)
```

Indeed, a row of `C` has ten ones and two distinct rows overlap in six
positions, proving (16).  The internal edge permutation module decomposes
under `S_6` as

```text
1 direct_sum Std_5 direct_sum V_(4,2),              (18)
```

with dimensions `1,5,9`; the Kneser adjacency eigenvalues on these summands
are precisely (17).  The star module is `1 direct_sum Std_5`, and `C` has
squared singular values 40 and 4 on those two summands.  It vanishes on the
nine-dimensional final summand.

Consequently (15) splits into:

```text
one 2 x 2 block of determinant -1440q^2;
five 2 x 2 blocks of determinant -144q^2;
nine scalars 2(p+2q).                               (19)
```

Multiplying (19) proves (6).

Because `q!=0`, singularity is possible only at `p=-2q`.  At that value the
six paired `2 x 2` blocks remain invertible, while the nine-dimensional
`V_(4,2)` block vanishes.  Equivalently, solving (15) gives

```text
ker M_(-2q,q,...,q)
 ={(0,y):Cy=0},                         dim ker C=9. (20)
```

Every vector in (20) has zero star coordinates.  It cannot be the full-edge
`F` required by (1).  This completes the orbit exclusion.

## 4. Exact wall

```text
physical extension forces (ell^2 A)F=0:                 PROVED;
weighted Kneser pencil (4)/(9):                          EXACT;
same-sign real A chamber:                                EXCLUDED;
mixed-Hodge signature there:                             (15,6);
A proportional to ell:                                   EXCLUDED;
six-equal-coordinate orbit, generic ratio:               EXCLUDED;
six-equal-coordinate determinant wall p=-2q:             KERNEL STAR-ZERO;
six-equal-coordinate full-edge physical extension:       IMPOSSIBLE;
hypothetical real A has both coefficient signs:           NECESSARY;
mixed-sign general star A:                                UNKNOWN;
full-edge physical leaf extension exists:                 UNKNOWN;
P7 pinned matrix full rank on primitive torus:            UNKNOWN;
global Krenn--Gu:                                         UNRESOLVED. (21)
```

The exact determinant timeout attempted during discovery is not used as
evidence and is not part of the replay.  No graph/support enumeration,
parameter sweep, numerical approximation, finite-field inference, Groebner
elimination, or timeout enters the proof.

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_physical_extension_mixed_hard_lefschetz_sign_chamber_and_one_exceptional_orbit.py
python claims/p7/audit_p7_physical_extension_mixed_hard_lefschetz_sign_chamber_and_one_exceptional_orbit.py
python -m py_compile claims/p7/verify_p7_physical_extension_mixed_hard_lefschetz_sign_chamber_and_one_exceptional_orbit.py claims/p7/audit_p7_physical_extension_mixed_hard_lefschetz_sign_chamber_and_one_exceptional_orbit.py
uv run --with ruff ruff check claims/p7/verify_p7_physical_extension_mixed_hard_lefschetz_sign_chamber_and_one_exceptional_orbit.py claims/p7/audit_p7_physical_extension_mixed_hard_lefschetz_sign_chamber_and_one_exceptional_orbit.py
```

The primary verifier checks the universal mixed-kernel identity, matrix
formula (4), exact `S_6` block decomposition, determinant (6), exceptional
kernel support, and the symmetric Hard-Lefschetz anchor.  The independent
standard-library audit rebuilds those identities using a separate formal
Boolean algebra and exact rational representation matrices, importing
neither the primary verifier nor project code.
