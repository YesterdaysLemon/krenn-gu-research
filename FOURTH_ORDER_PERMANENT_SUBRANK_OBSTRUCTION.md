# Fourth-order permanent subrank obstruction

## Status

This is a self-contained tensor theorem over `C`:

```text
the order-four permanent tensor has subrank exactly two.       (1)
```

Equivalently, no choice of four local linear maps can turn the
four-dimensional permanent tensor into a concise three-colour diagonal
tensor.  This excludes the fully tight four-root/four-blocker endpoint
of the multi-star reduction.  It is not a proof for permanent tensors of
arbitrary order and is not a global resolution of the Krenn--Gu
conjecture.

## Tensor formulation

Let

```text
P_4 = sum_(sigma in S_4)
        e_(sigma(0)) tensor e_(sigma(1))
        tensor e_(sigma(2)) tensor e_(sigma(3))
```

in `(C^4) tensor 4`, and let

```text
Delta_3 = sum_(c=0)^2 f_c tensor f_c tensor f_c tensor f_c.
```

We prove that there are no linear maps `L_i:C^4 -> C^3` satisfying

```text
(L_0 tensor L_1 tensor L_2 tensor L_3) P_4 = Delta_3.   (2)
```

Because every one-mode flattening of `Delta_3` has rank three, every
`L_i` would have rank three.  Dually, (2) would restrict the multilinear
permanent form to four hyperplanes

```text
U_i = a_i^perp subset C^4.                              (3)
```

## Pair images

Let `E` be the six-dimensional space with coordinates indexed by the
unordered pairs of `{0,1,2,3}`.  For hyperplanes `U_a,U_b`, define

```text
mu_(a,b)(u,v)_[ij] = u[i]v[j] + u[j]v[i],
A_(a,b) = span mu_(a,b)(U_a,U_b) subset E.              (4)
```

The `01|23` flattening of `P_4` factors through the nondegenerate
complement pairing on `E`:

```text
<e_[ij],e_[kl]> = 1 if {i,j,k,l}={0,1,2,3},
                  0 otherwise.                          (5)
```

Indeed, expanding (4) on a pair and its complement produces each of the
24 permutations exactly once.  Therefore the rank of the restricted
flattening between `A_(a_0,a_1)` and `A_(a_2,a_3)` is at least

```text
dim A_(a_0,a_1) + dim A_(a_2,a_3) - 6.                 (6)
```

We need only the following exact dimension classification.

### Pair-image lemma

If `a,b` are not proportional, then

```text
dim A_(a,b) >= 5.                                      (7)
```

If `a=b` projectively and `a` has `k` nonzero coordinates, then

```text
dim A_(a,a) = k+2.                                     (8)
```

To see this, identify `E*` with symmetric bilinear forms having zero
diagonal in the standard basis.  The annihilator of `A_(a,b)` consists
of such forms `q` that vanish on `a^perp x b^perp`.

When `a,b` are independent, symmetry gives

```text
q = lambda a tensor a + mu b tensor b.
```

The zero-diagonal equations are

```text
lambda a[i]^2 + mu b[i]^2 = 0,  i=0,1,2,3.
```

Their solution space has dimension at most one, proving (7).

When `a=b`, every symmetric form vanishing on `a^perp x a^perp` is

```text
q = a tensor s + s tensor a.
```

Its diagonal vanishes exactly when `s[i]=0` on the support of `a`.
The annihilator consequently has dimension `4-k`, which gives (8).

In particular,

```text
dim A_(a,b) <= 4
```

only when the two hyperplanes are equal and their common normal has at
most two nonzero coordinates.  Call such a pair of modes special.

## Three flattenings force three equal hyperplanes

Every `2|2` flattening of `Delta_3` has rank three.  By (6), in each of
the three pair partitions

```text
01|23, 02|13, 03|12
```

at least one of the two pairs must be special: if both pair images had
dimension at least five, the flattening rank would be at least four.

Special edges join modes having the same low-support projective normal,
so they form disjoint unions of cliques.  Such a graph on four vertices
meets all three perfect matchings only if one clique has at least three
vertices.  After relabelling,

```text
U_0 = U_1 = U_2 = U = a^perp,
|support(a)| <= 2.                                     (9)
```

## The final slice obstruction

If `a` has one nonzero coordinate, the first three modes omit that
coordinate.  In every nonzero permanent term the fourth mode must supply
it.  The fourth one-mode flattening consequently has rank at most one,
contrary to the rank-three flattening of `Delta_3`.

It remains to take `|support(a)|=2`.  Coordinate permutation and a
simultaneous diagonal rescaling normalize

```text
a = (1,1,0,0),
U = {x : x[0]+x[1]=0}.
```

On `U`, write

```text
l=x[1], m=x[2], n=x[3], so x[0]=-l.
```

Contract the fourth mode of `P_4` against its four coordinate
functionals and restrict the first three modes to `U`.  Under the
standard identification of symmetric three-tensors with cubic
polynomials, the four slices are proportional to

```text
 lmn, -lmn, -l^2 n, -l^2 m.                            (10)
```

Their slice space is the three-dimensional space

```text
S = l * span{mn, l n, l m}.                            (11)
```

It contains no nonzero decomposable tensor.  Every tensor in `S` is
symmetric, and a nonzero symmetric decomposable three-tensor must be a
cube `q^3` of a linear form.  If `q^3` belonged to (11), it would be
divisible by `l`, hence `q` would be divisible by `l`.  But no nonzero
multiple of `l^3` occurs in (11).

The fourth-mode slice space of a concise restriction has dimension
three, so it would equal `S`.  In contrast, the corresponding slice
space of `Delta_3` contains the three nonzero decomposable tensors

```text
f_0 tensor 3, f_1 tensor 3, f_2 tensor 3.
```

This contradiction proves that (2) is impossible.

## Exact subrank

The lower bound two is explicit.  Use the identity permutation and the
four-cycle

```text
(0,1,2,3), (1,2,3,0).
```

At mode `i`, retain only `span(e_i,e_(i+1 mod 4))`.  The union of these
two perfect matchings is one alternating eight-cycle, so it has exactly
those two perfect matchings.  The restriction of `P_4` is therefore
`Delta_2`.  Together with the obstruction above, this proves (1).

## Consequence for blockers

Let four fully supported root vectors be pairwise zero-coupled.  If the
union of their blockers over the three colours had exactly four
vertices, the multi-star lower bound would make every one of those
vertices a blocker for every colour.  The exact-factorisation identity
would turn their root--blocker permanent into a diagonal tensor.  Every
remaining outside vertex is a nonblocker for all three colours, so each
residual coordinate-product tensor is nonzero; full support at the roots
then makes all three diagonal coefficients nonzero.  After local
rescaling this is precisely the forbidden concise restriction (2).

Hence four such roots require at least five blocker vertices in total.
This result controls the fully tight endpoint.  It does not yet exclude
larger blocker unions or prove the analogous permanent-subrank statement
for order at least five.

## Verification

Run:

```text
python verify_fourth_order_permanent_subrank.py
python audit_fourth_order_permanent_subrank.py
```

The primary verifier reconstructs `P_4`, all three flattenings, the pair
image and annihilator dimensions in the canonical cases, the slice
space (10), and the explicit two-colour restriction.  The independent
audit exhausts projective hyperplane normals and all pair images over
`F_5`, checks the special-edge covering statement, and exhausts every
linear-form cube in the finite-field version of (11).  The theorem
itself is over `C`; the finite-field audit is an independent formula and
case-coverage check.
