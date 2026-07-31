# Rank-two pair kernels are secant or tangent block pencils

## Status

This is an exact characteristic-zero structural theorem for the
squarefree `P_4` compression algebra.  It uses only the geometry of a
line relative to the Segre quadric; no component search or elimination
is involved.

Put

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2)
```

and let `U,V` be two-dimensional subspaces of `R_1`.  Suppose the
multiplication map

```text
mu: U tensor V -> R_2
```

has rank exactly two.  Then its two-dimensional kernel has one of the
following two forms.

1. **Secant type.**  There are bases `(u_0,u_1)` of `U` and
   `(v_0,v_1)` of `V` such that

   ```text
   u_0 v_0=0,       u_1 v_1=0.                    (1)
   ```

   If both zero products have two-coordinate support, their support
   pairs are distinct.  Hence they are either disjoint, giving a
   `2+2` block center, or overlap in one coordinate, giving a `1+3`
   block center.  Support-one cases lie in the closure of these block
   patterns.

2. **Tangent type.**  After permuting source coordinates and changing
   bases in `U,V`,

   ```text
   U=V=span(X_0,w),                                (2)
   ```

   where `w in span(X_1,X_2,X_3)` has support at least two.  In
   particular, tangency at a genuine two-coordinate zero product is
   impossible when `rank(mu)=2`.

Thus there is no third kernel type: an exact rank-two pair image is
governed by a `2+2`/`1+3` secant center or by a coincident-plane
tangent through a coordinate line.

This reduces one of the open boundaries in the pure-`P_4` component
classification.  It does not classify how several exceptional pairs
fit together, prove that the eight known components are exhaustive,
close their special `H22` fibres, or settle the global Krenn--Gu
conjecture.

## The annihilator bound

For

```text
u=sum_i u_i X_i,       v=sum_i v_i X_i,
```

the equation `uv=0` is

```text
u_i v_j+u_j v_i=0       for i<j.                  (4)
```

If `u` has at least three nonzero coordinates, put
`rho_i=v_i/u_i` on its support.  Equation (4) says

```text
rho_i=-rho_j
```

for every pair.  Three indices force all `rho_i` to be zero, and an
index outside the support is then killed by any nonzero `u_i`.
Therefore `v=0`.

If `u` has two-coordinate support, (4) confines `v` to the same
coordinate pair and leaves one linear condition.  If `u` has
one-coordinate support, (4) confines `v` to that coordinate line.
Consequently

```text
dim Ann_R1(u) <= 1       for every nonzero u in R_1.  (5)
```

The same argument also classifies every nonzero zero product:

- on two-coordinate support, `u` and `v` are the two opposite binary
  directions;
- on one-coordinate support, `u` and `v` are proportional to the same
  coordinate vector.

## The kernel line and the Segre quadric

Because `rank(mu)=2`,

```text
K=ker(mu) subset U tensor V
```

has dimension two.  Its projectivization is a line

```text
P(K) subset P(U tensor V)=P^3.
```

The decomposable tensors in `P(U tensor V)` form the smooth Segre
quadric

```text
Sigma=P(U) x P(V).
```

A line contained in `Sigma` belongs to one of its two rulings.  It
would have the form

```text
P(u tensor V)       or       P(U tensor v).
```

If such a line lay in `P(K)`, a nonzero linear form would annihilate a
two-dimensional subspace of `R_1`, contradicting (5).  Hence
`P(K)` is not contained in `Sigma`.

Over `C`, a line not contained in a smooth quadric meets it in a
length-two scheme.  There are exactly two cases: two reduced points
or one double point.

This is the smallest Kronecker-pencil dichotomy: the kernel pencil is
secant or tangent to the rank-one locus.

## Reduced intersection: two zero products

Suppose

```text
P(K) intersection Sigma =
 { [u_0 tensor v_0], [u_1 tensor v_1] }.           (6)
```

The factors on each side are independent; otherwise the joining line
would be a Segre ruling.  They therefore give bases of `U` and `V`,
and membership in `K` gives (1).

Assume first that both zero products have genuine two-coordinate
supports `S_0,S_1`.  If `S_0=S_1`, both `U` and `V` equal the same
coordinate two-plane.  All their products then lie in the single line

```text
C X_p X_q subset R_2,
```

contradicting `rank(mu)=2`.  Thus `S_0` and `S_1` are distinct.
Two distinct two-subsets of four coordinates are either disjoint or
meet in exactly one coordinate.  These are precisely the `2+2` and
`1+3` block centers already present in the radical-plane
classification.

If exactly one zero product is supported on one coordinate, say
`X_p X_p=0`, replace it by

```text
(X_p+epsilon X_q)(X_p-epsilon X_q)=0.
```

Choose `q` so that the new two-coordinate label is distinct from the
two-coordinate label of the other zero product.  If both products
have support one, perform this deformation on both, choosing two
distinct coordinate-pair labels (the original coordinates are
distinct because the factors are bases).  The two displayed
decomposable kernel tensors keep the multiplication rank at most two,
while a nonzero two-by-two image minor at `epsilon=0` stays nonzero
for generic `epsilon`.  Thus the rank remains exactly two nearby, and
every support-one case lies in the closure of a `2+2` or `1+3` secant
stratum.

## Double intersection: the tangent normal forms

Suppose `P(K)` is tangent to `Sigma` at `[u tensor v]`.  A non-ruling
tangent direction has the form

```text
u tensor v' + u' tensor v,                         (7)
```

where `(u,u')` and `(v,v')` are bases.  Since the whole tangent line is
in `K`,

```text
uv=0,       uv'+u'v=0.                             (8)
```

If `u,v` have two-coordinate support, diagonal source scaling
normalizes them to

```text
u=X_0+X_1,       v=X_0-X_1.
```

Write `u'=(p,q,r,s)` and `v'=(P,Q,R,S)`.  The `X_0X_2` and `X_1X_2`
coefficients in the second equation of (8) are

```text
R+r,       R-r,
```

so `R=r=0`; the coordinate-three equations similarly give `S=s=0`.
Thus both complementary rows remain in
`span(X_0,X_1)`.  Consequently `U=V=span(X_0,X_1)`, whose product
space is only `C X_0X_1`.  This has rank one, contradicting the
hypothesis.  A rank-two kernel line therefore cannot be tangent at a
two-coordinate zero product.

If `u,v` have one-coordinate support, normalize both to `X_0`.
For each `j>0`, the `X_0X_j` coefficient of (8) is

```text
v'_j+u'_j.
```

After shifting `u',v'` by their respective first basis rows, one has

```text
u'=w,       v'=-w,
```

with `w in span(X_1,X_2,X_3)`.

Here the product image is spanned by

```text
X_0 w,       w^2.
```

These vectors have disjoint monomial supports.  The first is nonzero;
the second is nonzero exactly when `w` has at least two nonzero
coordinates.  Hence the assumed rank is two precisely in that case,
which proves (2).

## Why this is the useful foreign language

The unresolved pair-image-rank boundary had been phrased as a larger
system of permanent equations.  In the language of matrix pencils it
is only a line meeting the rank-one quadric.

The relevant outside literature is:

- De Teran, Dopico, and Landsberg,
  [An explicit description of the irreducible components of the set
  of matrix pencils with bounded normal
  rank](https://arxiv.org/abs/1606.02574), which organizes bounded-rank
  pencils by Kronecker type;
- de Seguins Pazzis,
  [Large spaces of bounded rank matrices
  revisited](https://arxiv.org/abs/1507.05375), for the broader
  compression-space viewpoint;
- Bernardi and Gesmundo,
  [Triangular tensor networks, pencils of matrices and
  beyond](https://arxiv.org/abs/2602.15114), which shows that
  low-physical-dimension triangle networks are controlled by
  Kronecker invariants, coincident-root loci, and determinantal
  geometry.

The last paper is especially close to the remaining exceptional
triangle in this repository: it suggests organizing three compatible
pair pencils by their Kronecker data before writing any new incidence
ideal.

## Verification

The proof above is symbolic and complete.  A tiny exact replay of the
annihilator ranks, both tangent coefficient systems, the tangent-rank
consequences, and representative secant normal forms is provided by

```text
uv run --with sympy \
  python verify_p4_rank_two_pair_kernel_geometry.py
```

The replay is not a search and is not needed as a substitute for the
proof.
