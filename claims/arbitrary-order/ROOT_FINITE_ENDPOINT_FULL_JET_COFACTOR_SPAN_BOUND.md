# Finite endpoints bound the full-root cofactor span

## Status

**Exact arbitrary-order characteristic-zero cofactor-span theorem.**  Let
`r>=2` fully supported pairwise-zero roots of a hypothetical three-colour
GHZ graph witness have projectively constant root--blocker first derivatives.
Restrict the logarithmic tangent at root `i` to

```text
S_i=ker(a_i),                 a_i(1,1,1) != 0,          (1)
```

so differentiated root--blocker edges vanish.  Let `Q` be the union of the
fixed nonblocker vertices having a nonzero one-tangent contraction with at
least one `S_i`, and write `t=|Q|`.  Root--root tangent--tangent blocks are
arbitrary.

For the derivative taken once at every root, the graph-side tensor image is
contained in the span of at most

```text
N(r,t)=sum_(0<=ell<=min(r,t), ell congruent r mod 2) binomial(t,ell)       (2)
```

complementary hafnian tensors.  Therefore the full GHZ root jet has rank at
most `N(r,t)`.

The first sharp consequences are:

1. `t=0`, `r` odd: all three coordinate-axis tangent types occur;
2. `t<=1`: at least two distinct coordinate-axis tangent types occur;
3. `t=2`: either some coordinate-axis tangent type occurs, or every `a_i`
   is supported on one common coordinate pair `{p,q}`.

The first two recover
[`ROOT_AT_MOST_ONE_ENDPOINT_FULL_JET_AXIS_NECESSITY.md`](ROOT_AT_MOST_ONE_ENDPOINT_FULL_JET_AXIS_NECESSITY.md).
The third is new: it constrains the five-root/seven-blocker/two-residual cell
even when arbitrary root--root tangent channels are restored.

This is a necessary full-jet condition, not a realization theorem.  The axis
and common-coordinate-pair branches remain open, as do nonprojective
root--blocker variation, three or more effective endpoints, and the actual
mixed-colour cofactor identities.  The arbitrary-order local-to-global
reduction and the global Krenn--Gu conjecture remain **UNRESOLVED**.  No
finite field is used.

## Endpoint-subset decomposition

Differentiate once at every root and restrict at root `i` to `S_i`.  Every
surviving matching pairs a root either to another root or to one vertex of
`Q`.  Let `A subset Q` be the endpoints used by root--endpoint edges and put
`ell=|A|`.  The remaining `r-ell` roots pair internally, so

```text
ell congruent r mod 2,        0<=ell<=min(r,t).         (3)
```

For fixed `A`, every term deletes exactly the same vertex set

```text
R union A.                                             (4)
```

All choices of which roots use `A`, all root-to-endpoint bijections, and all
internal root pairings therefore multiply the single complementary matching
tensor `C_(R union A)`.  Their sum is one scalar multilinear form times that
tensor.  Summing over admissible endpoint subsets gives at most the number
in (2) of cofactor classes.  No cancellation hypothesis and no restriction
on root--root tangent blocks is used.

For `r>=2`, the first values are

```text
t=0:  N=1 for even r, N=0 for odd r;
t=1:  N=1;
t=2:  N=2.                                           (5)
```

Thus `t=2` forces the full GHZ jet to have tensor-image rank at most two.

## Exact rank-two classification

For each coordinate set

```text
l_(i,c)=e_c^* restricted to S_i,
F_c=tensor_(i in R) l_(i,c).                           (6)
```

The three independent diagonal target tensors make the full GHZ jet rank

```text
dim span{F_0,F_1,F_2}.                                (7)
```

As before, `F_c=0` exactly when an axis-`c` tangent covector occurs.  Hence
the existence of any axis type immediately makes (7) at most two.

Assume now that every `F_c` is nonzero.  If two of them, say `F_p,F_q`, are
proportional, equality of nonzero decomposable tensors makes
`l_(i,p),l_(i,q)` proportional at every root.  The covector

```text
e_p^*-rho_i e_q^*                                    (8)
```

then vanishes on `S_i` for some nonzero `rho_i`, so `a_i` is supported on
the common coordinate pair `{p,q}`.  Conversely, common-pair support makes
`F_p,F_q` proportional, so (7) is at most two.

It remains to exclude a dependence among three pairwise nonproportional
`F_c`.  Suppose

```text
alpha_0 F_0+alpha_1 F_1+alpha_2 F_2=0                (9)
```

with every `alpha_c` nonzero.  At one root `j`, choose two independent
members among `l_(j,0),l_(j,1),l_(j,2)`, which span the two-dimensional
space `S_j^*`.  Express the third in that basis.  Both coefficients must be
nonzero, or (9) would force one nonzero complementary pure tensor to vanish.
Grouping (9) by the two basis covectors then makes the three complementary
pure tensors

```text
tensor_(i!=j) l_(i,c)                                 (10)
```

proportional.  Equality of decomposable tensors makes all three coordinate
restrictions proportional at every other root.  Since `r>=2`, choose such a
root; its coordinate restrictions would span only one dimension, contrary
to `dim S_i^*=2`.  Thus no dependence (9) exists.

Consequently, with no axis root, rank (7) is at most two exactly on the
common-coordinate-pair locus.  Combining this with (5) proves the `t=2`
alternative.

## Two-class frame rigidity

There are exactly two parity-allowed endpoint subsets when `t=2`:

```text
r odd:   {q_0}, {q_1};
r even:  emptyset, {q_0,q_1}.                         (11)
```

Write the corresponding full-root derivative as

```text
G_0 tensor C_0 + G_1 tensor C_1.                     (12)
```

Here the `G_j` are aggregate scalar root-matching forms and the `C_j` are
the two complementary hafnian tensors.  On either rank-exactly-two GHZ
branch, elementary flattening rank forces both pairs to be independent and

```text
span{G_0,G_1}=span of the nonzero GHZ coefficient forms,
span{C_0,C_1}=the corresponding two-dimensional diagonal tensor plane.    (13)
```

Indeed, in bases of those two row and column spaces, (12) is a product of
two `2 x 2` coefficient matrices.  A rank-two product has both factors
invertible.  Thus the two deletion cofactors are not merely nonzero: each is
itself diagonal and together they frame the exact target plane.

If exactly one axis type `c` occurs, that column plane is generated by the
other two pure diagonals.  On the no-axis common-pair branch `{p,q}`, write
`F_p=lambda F_q`; the plane is generated by the remaining pure diagonal and
the fixed combination of the `p,q` diagonals.  The actual simultaneous
realizability of these two principal cofactors is still open.

## Frontier consequence

At order fourteen, five roots with seven blockers leave exactly two residual
vertices.  Any projectively constant tangent lift of that first genuine
two-port cell must therefore satisfy

```text
an axis tangent occurs,
or all five tangent covectors lie in one coordinate-pair plane.            (14)
```

This condition is independent of the two-port factorization and survives
dense root--root tangent graphs.  The next exact task is to combine (14) with
the first-jet quotient frames and the complementary-hafnian identities on
the two deletion classes.  Equation (13) makes that target explicit; neither
branch is claimed empty here.

## Replay

```powershell
uv run --with sympy python verify_root_finite_endpoint_full_jet_cofactor_span_bound.py
python audit_root_finite_endpoint_full_jet_cofactor_span_bound.py
uv run --with sympy --with ruff python -m ruff check verify_root_finite_endpoint_full_jet_cofactor_span_bound.py audit_root_finite_endpoint_full_jet_cofactor_span_bound.py
python -m py_compile verify_root_finite_endpoint_full_jet_cofactor_span_bound.py audit_root_finite_endpoint_full_jet_cofactor_span_bound.py
```

The primary reconstructs the exact coefficient-form ranks on all small
projective covector tuples through four roots and checks (2) through twelve
roots and six endpoints.  The no-import audit uses a different integer
kernel, rational row reduction, a wider covector box, and an independent
endpoint-subset enumeration through eighteen roots.  These bounded checks
audit the algebra and indexing; the deletion-set and pure-tensor arguments
above prove the arbitrary-order theorem.
