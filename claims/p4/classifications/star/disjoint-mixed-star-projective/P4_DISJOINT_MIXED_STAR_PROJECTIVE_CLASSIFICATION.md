# Projective exhaustion of the disjoint mixed star

## Status

**Exact characteristic-zero classification theorem.**  Every nonzero pure
`P_4` tuple with the disjoint mixed-star orientation and support pattern
`{01,01,23}` belongs to the closure of component eight.  This includes the
projective leaf chart omitted from the original component construction and
the later affine reverse theorem.

Consequently this entire rank-one exceptional-graph stratum is exhausted;
it creates no additional component.  No elimination or parameter search is
used.  The proof is an irreducible determinant hypersurface together with a
dimension argument for its projectivized kernel incidence.

## Homogeneous marked normal form

Keep the binary notation

```text
a=X_0+X_1,       a_bar=X_0-X_1,
b=X_2+X_3,       b_bar=X_2-X_3.                    (1)
```

As in the affine theorem, exact-pair normalization and the nonzero active
coefficient give

```text
y_0=b_bar,       x_1=x_2=a,
y_3=a_bar,       x_3=b,
x_0=Aa+B a_bar+b-b_bar.                             (2)
```

Homogenize the first moving kernel row with `[h:g:p] in P^2`:

```text
y_1=-Ag a+h a_bar+g b+p b_bar.                     (3)
```

The first omitted purity word has already forced the coefficient `-Ag`.
Write the second kernel row as

```text
y_2=-Aj a+eta a_bar+j b+kappa b_bar.                (4)
```

The affine chart in
[`P4_DISJOINT_MIXED_STAR_AFFINE_CLASSIFICATION.md`](../disjoint-mixed-star-affine/P4_DISJOINT_MIXED_STAR_AFFINE_CLASSIFICATION.md)
is `h!=0`.

## The homogeneous kernel incidence

The only nonzero or potentially nonzero coefficients are

```text
T_0000= 4(eta p+h kappa),

T_1000=-4(Bgj-Bkappa p+eta g+eta p+h j+h kappa),

T_1001=-4(A^2gj+B eta g+B h j+eta h),

T_1111=4.                                           (5)
```

Thus purity is exactly

```text
N(h,g,p) (j,kappa,eta)^T=0,                         (6)

N=
[ 0            h           p     ]
[ Bg+h         h-Bp        g+p   ]
[ A^2g+Bh      0           Bg+h  ].                 (7)
```

Its determinant is

```text
Phi_h=
 A^2 B g p^2+A^2g^2h-B^2g^2h+B^2hp^2
 -Bgh^2-h^3.                                        (8)
```

Setting `h=1` recovers the irreducible affine polynomial from component
eight.  Equation (8) is its homogenization in `[h:g:p]`; it is not divisible
by `h`, so it is irreducible as well.  Hence

```text
D={Phi_h=0} subset A^2_(A,B) x P^2_[h:g:p]          (9)
```

is an irreducible threefold.

On the open set `rank N=2`, the projective kernel is unique.  Its graph over
`D` is therefore an irreducible threefold, and its affine part is exactly
component eight by the reverse theorem.

## The complete rank-one base

The nine `2 x 2` minors of (7) factor into elementary pieces.  Separating
`h!=0` and `h=0` gives the following complete rank-one locus.

1. On `h!=0`, rescale `h=1`.  Then

   ```text
   Bg+1=0,       g+Bp^2=0,       A^2g+B=0.          (10)
   ```

   Equivalently, for `B!=0`,

   ```text
   g=-1/B,       Bp=plus-or-minus1,
   A=plus-or-minus B.                               (11)
   ```

2. On `h=0,B!=0`, rank one forces

   ```text
   p=0,       g!=0,       A=plus-or-minus B.        (12)
   ```

3. On `h=0,B=0,A!=0`, the unique base point is

   ```text
   [g:p]=[0:1].                                     (13)
   ```

4. On `h=0,A=B=0`, every `[g:p] in P^1` has rank one. (14)

Each piece in (11)--(14) has dimension one.  There is no rank-zero matrix:
the projective triple `[h:g:p]` cannot make every row of (7) vanish.

## Why there is no vertical component

Let

```text
I={(A,B,[h:g:p],[j:kappa:eta]):N(j,kappa,eta)^T=0}
  subset A^2 x P^2 x P^2.                           (15)
```

The ambient space has dimension six, and (15) is cut out by three
equations.  By the principal ideal theorem, every irreducible component of
`I` has dimension at least three.

Over the rank-one base (11)--(14), the projective kernel is `P^1`.
Since that base has dimension one, the full rank-one incidence has dimension
two.  It is too small to contain an irreducible component of `I`.

Any component of `I` must therefore meet the rank-two open set.  There the
kernel is unique, so every such component is the closure of the same graph
over the irreducible threefold `D`.  It follows that

```text
I=closure(Graph(ker N over rank N=2))               (16)
```

is irreducible.  In particular, every projective kernel direction over
(11)--(14) is a limit of component-eight points.  Some directions acquire
additional rank-three edges and some drop a pair image to rank two; neither
behavior creates a component.

This is the clean projective version of the explicit affine arcs.  It is a
small Springer-resolution argument: the kernel incidence resolves the
singular determinant hypersurface, while codimension prevents an extra
vertical component.

## Exact replay

```text
uv run --with sympy python claims/p4/classifications/star/disjoint-mixed-star-projective/verify_p4_disjoint_mixed_star_projective_classification.py
python claims/p4/classifications/star/disjoint-mixed-star-projective/audit_p4_disjoint_mixed_star_projective_classification.py
```

The primary verifier reconstructs the homogeneous permanent coefficients,
all nine factored minors, the rank-one normal forms, and representative pair
profiles.  The independent audit rebuilds the projective boundary with
rational arithmetic and a subset-DP permanent.  The irreducibility and
dimension argument is the written proof above.
