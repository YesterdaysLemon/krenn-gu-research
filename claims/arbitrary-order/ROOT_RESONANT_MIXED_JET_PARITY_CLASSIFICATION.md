# Mixed-jet parity on the pairwise-resonant root splittings

## Status

**Exact characteristic-zero higher-jet theorem.**  The pairwise rank-one
classification leaves two exceptional scalar tangent patterns.  Their full
coordinatewise GHZ mixed derivatives are as follows.

1. For the uniform balanced pattern

   ```text
   S=ker(e_p^*+e_q^*)
   ```

   and every `k>=1`, the coordinatewise-product map

   ```text
   mu_k:S^(tensor k) -> K^3/<(1,1,1)>             (1)
   ```

   has rank two when `k` is odd and rank one when `k` is even.
2. For the three-axis pattern

   ```text
   S_0=ker(e_0^*), S_1=ker(e_1^*), S_2=ker(e_2^*),
   ```

   each pairwise product has quotient rank one, while the triple product
   `S_0 tensor S_1 tensor S_2 -> K^3` is identically zero.

Consequently, the sole pairwise-resonant pattern available for four or more
roots does not stay one-dimensional at higher order: every restricted
three-root GHZ mixed derivative already spans the full two-dimensional
diagonal quotient.  Any graph realization must supply a full quotient span
among the aggregate third-derivative matching/cofactor classes for every
root triple.

This is a necessary higher-jet condition, not a graph/hafnian
nonrealizability theorem.  It neither excludes the uniform balanced pattern
nor excludes the three-axis exception.  The arbitrary-order local-to-global
reduction and the global Krenn--Gu conjecture remain **UNRESOLVED**.  No
finite field is used.

## Uniform balanced pattern

Permute coordinates so the common zero coordinate is two.  Every vector in

```text
S=ker(e_0^*+e_1^*)
```

has the form

```text
u_i=(x_i,-x_i,z_i).                               (2)
```

The coordinatewise product of `k` such vectors is

```text
(X,(-1)^k X,Z),
X=product_i x_i,       Z=product_i z_i.           (3)
```

Both `X` and `Z` occur independently in the multilinear image: choose the
`(1,-1,0)` basis vector in every factor or choose `(0,0,1)` in every factor.

If `k` is even, (3) lies in

```text
span{(1,1,0),(0,0,1)}.
```

Modulo `(1,1,1)`, the two displayed vectors are negatives of one another,
so the quotient image has rank one.

If `k` is odd, the image contains `(1,-1,0)` and `(0,0,1)`.  If

```text
alpha(1,-1,0)+beta(0,0,1)=gamma(1,1,1),           (4)
```

the first two coordinates give `alpha=gamma=-alpha`.  Characteristic zero
forces `alpha=gamma=0`, and then `beta=0`.  The two quotient classes are
independent, proving rank two.  Coordinate permutation proves the assertion
for every common zero coordinate.

For `k=1`, this recovers the first-jet quotient isomorphism.  For `k=2`, it
recovers the rank-one resonance theorem.  The first new consequence is the
rank-two `k=3` mixed derivative.

## Three-axis pattern

Take

```text
u in S_0: u_0=0,
v in S_1: v_1=0,
w in S_2: w_2=0.
```

Then

```text
u coordinatewise-product v coordinatewise-product w=(0,0,0),            (5)
```

because each coordinate is killed by the tangent space bearing its index.
For a pair, say `S_0,S_1`, the product image contains only the coordinate-two
axis modulo the constant line and is nonzero; hence its quotient rank is
one.  The other two pairs follow by permutation.

Thus the triple-axis clique is more degenerate, not secretly rank two at the
third mixed derivative.  It exists only for exactly three pairwise-resonant
roots and needs a different obstruction involving other vertices or global
gluing.

## Graph-side boundary

After restricting tangent directions to the displayed kernels, the GHZ
side of any mixed root derivative is exactly the coordinatewise map above.
On the graph side, differentiating the hafnian partitions surviving
matchings according to how the varied roots pair with one another or with
effective companions.  Each partition contributes a scalar multilinear
form times a fixed complementary matching tensor.  Therefore the quotient
span of all such accessible aggregate classes must contain `im(mu_k)`.

For the uniform pattern, a one-line aggregate cofactor construction may
survive every even restricted jet, but cannot survive an odd restricted jet
without acquiring a second independent quotient class.  The theorem does
not determine whether the complete graph recursion can supply that class or
cancel all mixed-colour coefficients.

## Replay

Replay the pairwise dependencies first:

```powershell
uv run --with sympy python verify_root_mixed_second_jet_quotient_rank_classification.py
python audit_root_mixed_second_jet_quotient_rank_classification.py
uv run --with sympy python verify_root_mixed_second_jet_resonance_clique_classification.py
python audit_root_mixed_second_jet_resonance_clique_classification.py
```

Then run:

```powershell
uv run --with sympy python verify_root_resonant_mixed_jet_parity_classification.py
python audit_root_resonant_mixed_jet_parity_classification.py
uv run --with sympy --with ruff python -m ruff check verify_root_resonant_mixed_jet_parity_classification.py audit_root_resonant_mixed_jet_parity_classification.py
python -m py_compile verify_root_resonant_mixed_jet_parity_classification.py audit_root_resonant_mixed_jet_parity_classification.py
```

The primary constructs all tensor-basis image columns symbolically through
order ten and checks every common-zero coordinate.  The no-import audit uses
an independent integer implementation through order fifteen and checks all
six coordinate permutations.  These bounded checks audit the displayed
all-order formula (3); they are not the proof by themselves.
