# Four-root torus-star equal-leaf survivor rank-at-most-six syndrome boundary containment

## Status

**Exact scoped boundary theorem (`GLD86`).** Work over
`K=Q(i)` and then extend scalars to `C`. On the complete scale-fixed,
equal-leaf survivor base used by `GLD83` and `GLD84`, every point whose
center coefficient matrix has rank at most six lies on one of four named
leaf-frame divisors. The statement is set-theoretic over geometric points;
it is not a claim that any of those divisors is empty.

The proof uses the exact `GLD75` bidirectional ideal certificate and the fixed
`GLD71` 37-row syndrome basis. The displayed 7-by-7 syndrome minor factors
as the square of the product of four explicit divisors. Since the scale-fixed
center coordinate is `C_8=1`, a zero syndrome forces the last selected column
to be a linear combination of the first eight. Off the four divisors, the
selected minor then forces rank at least seven for the first eight syndrome
columns. Differentiating the bidirectional certificate at an incidence-zero
point transfers that rank to the `10 x 8` center coefficient matrix `A` of
`GLD84`.

This theorem does **not** compute or exclude the pulled-back `GLD83` Fitting
ideal. After `Omega` saturation, all four named divisors remain retained
branches: none of the four divisors is excluded after `Omega` saturation.
The Gaussian rank-seven chart of `GLD83`/`GLD84` remains open context, and the
global Krenn--Gu conjecture remains **UNRESOLVED**.

Owning dependencies are the exact `GLD71` punctured-syndrome basis, the
`GLD75` equal-leaf bidirectional certificate, the `GLD83` definition of the
intrinsic Fitting residual and `Omega`, and the `GLD84` center-linear system.

## 1. The chart and the two exact incidence descriptions

Retain the complete scale-fixed equal-leaf chart

```text
B=Spec K[x_0,...,x_14]/(g_0,...,g_9,x_8),
```

where `g_0,...,g_9` are the ten pinned `GLD75` basis generators. The first
eight shifts are center entries and the last six are the two lower rows of a
common leaf frame. Put

```text
c=(x_0,...,x_7)^T,
z=(x_9,...,x_14)=(p,q,r,a,b,c),
s=1+i+r.
```

The actual common leaf frame and the actual center frame are

```text
G = [1  1       1      ]       C = C_0+(x_0,...,x_8),
    [p  q       s      ]
    [a  1+b     1+c    ],

C_0 = [-2-2i  -1+2i  3]
      [ 0     -3+3i  0]
      [ 0     -1+2i  1].
```

Here `C` is read row-major as a nine-vector, and `C_0+(x_0,...,x_8)` means
entrywise addition in that order. In particular, on `x_8=0`,

```text
C_8=1.                                                   (1)
```

The `GLD71` sparse relation list `R` is a fixed basis of the annihilator of
the rank-44 torus-star nuisance space. For a relation
`rho=(rho_(u i j k))` and root-major center coordinate `(u,v)`, define

```text
M(G)_(rho,(u,v))
  = sum_(i,j,k=0)^2 rho_(u i j k) G_(i,v)G_(j,v)G_(k,v).
```

This gives a `37 x 9` matrix over `K[p,q,r,a,b,c]`. If `f=M(G)C`, then `f`
is exactly the 37 equal-leaf syndrome/incidence equations for this relation
basis. `GLD75` uses a different nullspace row basis for the same annihilator,
but the two fixed bases are related by an invertible constant matrix over `K`.

The `GLD75` certificate supplies polynomial matrices in both directions

```text
g=U f,                 f=V g,                              (2)
```

with the row/column transposes suppressed in this display. Its canonical
serialized carrier has SHA-256
`05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57`.
Therefore, on geometric points of the displayed chart,

```text
B=0 iff M(G)C=0.                                         (3)
```

No numerical or sampled equivalence is being asserted in (3): it is the
combination of the exact bidirectional certificate with the fixed annihilator
basis change.

Finally, `GLD84` writes the ten basis equations after `x_8=0` as

```text
g(z,c)=A(z)c+q(z),        A(z) in Mat_(10 x 8)(K[z]).       (4)
```

The matrix `A` is the center-shift Jacobian of the ten generators.

## 2. The exact syndrome minor and its four divisors

Use the following rows and columns of `M(G)`:

```text
R_7=(0,1,17,19,31,32,33),
S_7=(2,3,4,5,6,7,8).                                    (5)
```

Writing `s=1+i+r`, exact characteristic-zero arithmetic gives

```text
det M(G)_(R_7,S_7)
 =432 (p-q)^2 (p-s)^2 (q-s)^2
      (p q+p s+q s-p-q-s)^2.                             (6)
```

Define the four named divisors

```text
H_1=p-q,
H_2=p-s,
H_3=q-s,
H_4=p q+p s+q s-p-q-s.                                  (7)
```

Equation (6) is an identity in `K[p,q,r,a,b,c]`. In particular, the
determinant has no `a`, `b`, or `c` terms even though those variables occur in
the selected matrix entries. The factor 432 is a nonzero unit in
characteristic zero.

The primary verifier reconstructs the full `37 x 9` matrix from the pinned
`GLD71` relations and evaluates (6) with exact symbolic arithmetic. The
independent audit does not import a repository module: it rederives only the
selected rows from their compact syndrome formulas and expands the determinant
with sparse `Fraction` arithmetic.

## 3. Rank transfer from the syndrome to the center matrix

We first record the linear-algebra bridge used by the containment.

### Lemma 3.1 (center-column rank equality on `B`)

At every geometric point of `B`,

```text
rank A(z) = rank M(G)[:,0:8].                            (8)
```

#### Proof

Let `f=M(G)C`. The certificate identities (2) hold in the polynomial ring.
At a point of `B`, both `f` and `g` vanish by (3). Differentiate (2) with
respect to the eight center shifts. The terms containing derivatives of `U`
or `V` are multiplied by the vanishing vector `f` or `g`, so they disappear:

```text
D_c g = U D_c f,       D_c f = V D_c g.                  (9)
```

Because `C` is affine-linear in `c`, `D_c f=M(G)[:,0:8]`. Equation (4) gives
`D_c g=A(z)`. The two inequalities from (9) imply equality of the two
ranks. `square`

### Theorem 3.2 (rank-at-most-six boundary containment)

Let `P` be a geometric point of `B` over `C` (equivalently, after extending
the exact calculation from `K` to an algebraic closure). If

```text
H_1(P)H_2(P)H_3(P)H_4(P) != 0,                            (10)
```

then

```text
rank A(P) >= 7.                                          (11)
```

Consequently, with `I_7(A)` denoting the ideal of 7-by-7 minors of `A`,

```text
B intersect V(I_7(A))
  subseteq B intersect V(H_1 H_2 H_3 H_4).                (12)
```

This is a pointwise/set-theoretic containment; no radical ideal equality is
claimed.

#### Proof

At a point of `B`, equation (3) and (1) give

```text
M(G)_8 = -sum_(j=0)^7 C_j M(G)_j.                         (13)
```

Here the subscript denotes a column. Expand the determinant in (5) after
replacing its final column by the right side of (13). Terms with `j=2,...,7`
have a repeated column and vanish. Thus

```text
det M(G)_(R_7,S_7)
 = -C_0 det M(G)_(R_7,(2,3,4,5,6,7,0))
   -C_1 det M(G)_(R_7,(2,3,4,5,6,7,1)).                  (14)
```

If the left side is nonzero, at least one of the two displayed 7-by-7
minors of `M(G)[:,0:8]` is nonzero. Hence

```text
rank M(G)[:,0:8] >= 7.                                   (15)
```

Under (10), the factorization (6) makes the left side nonzero. Lemma 3.1
then gives (11). Taking the contrapositive gives (12). `square`

## 4. `Omega` saturation and the retained residual branches

Let `Omega` be the frame/gauge open retained by `GLD83`, and let

```text
Z_low=(B intersect V(I_7(A))) intersect D(Omega).          (16)
```

be the rank-at-most-six part of the `GLD83` residual after the same open
condition. The exact consequence of Theorem 3.2 is only

```text
Z_low subseteq
  (B intersect V(H_1 H_2 H_3 H_4)) intersect D(Omega),      (17)
```

or, equivalently, the union of the four named divisor intersections with
`D(Omega)`. Saturating by `Omega` does not invert any `H_j` in this theorem.
No unit certificate, emptiness proof, or pointwise exclusion is supplied for
any of the four components. In particular, **none of the four divisors is
excluded after `Omega` saturation**; all four remain explicit low-rank
boundary obligations.

The theorem also does not assert that each divisor intersection is nonempty.
It records exactly what is proved: any surviving low-rank point must be on
the named union, while the divisor-by-divisor analysis remains to be done.

## 5. Relation to the adjacent frontier and hostile controls

- `GLD83` remains the owner of the intrinsic bordered-Pluecker/Fitting
  residual `V(I_Pl) intersect D(Omega)`. `GLD86` supplies no pullback of
  `I_Pl` and no new Fitting-open exclusion.
- `GLD84` remains the owner of the finite rank-eight/rank-seven/at-most-six
  center-rank cover. The Gaussian point is rank seven; this theorem does not
  promote that point to a component statement.
- The four factors in (6) are named leaves of the low-rank branch, not a
  claim that they are the complete irreducible decomposition of the survivor
  base or of the Fitting residual.
- The relation (3) is used only on the displayed equal-leaf chart and only
  with the exact certificate and scale-fixed condition. It is not transferred
  to other gauges, unequal-leaf components, source presentations, triangles,
  other roots, or other support profiles.
- The global Krenn--Gu conjecture remains **UNRESOLVED**.

The highest-value successor is now divisor-by-divisor analysis of the
`GLD83` Fitting pullback on `V(H_j) intersect D(Omega)`, retaining the full
raw response incidence on any `C_F` rank drop. A proof that one divisor is
empty would be a separate scoped theorem; a result on one principal open
would not close the other three.

## 6. Verification

Run from repository root:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_survivor_rank_at_most_six_syndrome_boundary_containment.py
python -I claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_survivor_rank_at_most_six_syndrome_boundary_containment.py
```

The primary replay checks the immutable `GLD75` certificate carrier and its
center-linear generators, reconstructs the `GLD71` syndrome map, verifies the
exact factorization (6), checks the Gaussian `C_8=1` point and rank, and
records the scope fences. The no-import audit uses only the Python standard
library, exact Gaussian fractions, a sparse polynomial determinant, and a
separate constant-matrix column-replacement fixture. The written
bidirectional-certificate differentiation is the bridge from the syndrome
minor to `rank A`; neither script turns a sampled or numerical observation
into a proof.
