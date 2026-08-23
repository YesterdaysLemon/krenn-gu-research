# Hostile review: zero-anchor first-polarized singleton kernels and simultaneous-absorption sharpness

## Verdict

**Accepted at the exact stated scope.**  The arbitrary-root singleton identities
type-check against the complete `GLS31` first-polarized equations, and the
exact rational graph independently replays.  It satisfies both complete
first-polarized equations, including every labelled one-`Q` deck term, while
also satisfying the earlier maximum-root, pure, response, normal-image,
complete-nuisance, and top-diagonal gates.

The graph fails `316` original mixed GHZ coefficients, including the displayed
Hamming-one coefficient.  It is therefore a sharp insufficiency certificate,
not a hypothetical witness or counterexample.  This is `GLS32`.  It neither
closes a normal-product divisor nor supplies a legal selector.  The Krenn--Gu
conjecture remains **UNRESOLVED**.

## Audited base and artifacts

The review was performed from

```text
origin/main = 627804846a5cc8a4b6d779a34ac8df6e8da33a46
```

against the owning `GLS22`, `GLS23`, `GLS26`, `GLS29`, `GLS30`, and `GLS31`
interfaces.  The reviewed tranche consists of

- the `GLS32` theorem document;
- its focused exact SymPy verifier;
- its independent standard-library `Fraction` audit; and
- the frontier, package-index, and node-DAG updates in the same candidate
  tree.

## Mathematical hostile review

### 1. Singleton isolation keeps the complete labelled equation

For fixed free port `u`, contracting every other port in

```text
K_v^10=ker x_v intersect ker b_v
```

kills every promoted-pair term in `GLS31` equation (9).  It also kills the
one-`Q` term indexed by `v!=u` through its `x_v` factor.  The two labels
`(s,u)` remain together as

```text
F_u^10=sum_s lambda_1^s S_(s,u).
```

This gives the stated covector identity without deleting a label or dividing
by a response, deck value, coordinate, or minor.  The transposed argument for
`K_v^01=ker a_v intersect ker y_v` is identical.  The conclusion is only an
image-dimension bound; a zero left side licenses no activity inference.

### 2. The identity is arbitrary-root, but the control is four-port

The contraction proof uses `m=2r-2` promoted ports and therefore has the
declared arbitrary-root scope.  The rational control has `r=3` and four
promoted ports.  Its finite replay cannot prove higher-root source coverage,
exclude the `r>=4` disjoint-supplier branch, or close another residual-shore
normal form.

### 3. Maximum-root certificate

The displayed root `{a_0,a_1,k}` satisfies all three root equations.  A torus
root containing an `a_i` cannot contain a residual vertex or any `u_j`
because a matrix-unit edge evaluates nontrivially on torus vectors.  Without
`A`, `q_0q_1=E_00` forbids both residual vertices.  One residual vertex with
two promoted ports forces both promoted `w`-values to vanish and leaves a
nonzero `lambda_uv z_u(0)z_v(0)` edge.  Four promoted ports would force the
three complementary response products to agree, whereas they are exactly
`(-2,1,-3/2)`.  Hence no torus root has order four.

The only divisions in this last contradiction are by coordinates of declared
torus vectors, all of which are nonzero.  No theorem statement localizes at
such a coordinate.

### 4. Complete first-polarized and normal equations

The physical responses are

```text
R_D=lambda_D E_00,
lambda=(1,1,-3/2,1,1,-2).
```

All six are nonzero.  Every normal supplier is `2E_00`, and
`2 sum_D lambda_D=1`.  The first-polarized suppliers are `E_00` on pairs
meeting `k` and `2E_00` on the other pairs, giving scalar total one in each
first-polarized equation.

The intact one-`Q` decks are not zero or omitted.  For every fixed removed
port the two residual labels obey `S_(0,u)+S_(1,u)=0`, while all four shore
weights equal one.  The independent audit counts `112` nonzero retained deck
entries before these pairwise cancellations across the two retained labels.
Thus equations (9)--(11) of `GLS31` all hold exactly.

Because `GLS31` proves that the projected evaluation identity has bidegree at
most `(1,1)` and that its constant term cancels under `P_Q`, these three
coefficient equations imply the whole **projected evaluation-pencil**
identity.  They do not produce a root-locus pencil.

### 5. Complete nuisance and target interface

The pair-nuisance construction uses the literal `GLS23` labelled intersection
cases.  Exact row reduction gives nuisance and augmented ranks

```text
(36,36,36,50,50,50)
```

for the six promoted targets; every desired tensor is nonzero of root-slice
rank one and absorbed.  The top nuisance has rank six, the `GLS26` projected
diagonal has rank two, and adjoining that diagonal does not increase rank.

These facts show only that the target-side linear gates happen to hold on the
off-target graph.  They do not invoke a converse of `GLS23` or `GLS26`, and
they do not certify a legal downstream selector.

### 6. Pure normalization and off-target failure

Colour zero follows from the normal sum.  In colours one and two the relevant
`A-Q` matching is forced and the promoted hafnian is

```text
12 product_u t_u=1.
```

Thus the pure coefficients are exactly `(1,1,1)`.  Direct perfect-matching
evaluation nevertheless finds exactly `316` mixed failures, including

```text
coeff(1,1,1,1,1,1,1,2)=1.
```

This is decisive evidence that the graph is not a witness.  The certificate
refutes only the sufficiency of the complete projected shore-normal pencil
together with the listed static gates.

## Independence review

The primary verifier imports only the already reviewed `GLS31` helper
implementation and uses SymPy dense matrices, exact rank, and direct matching
evaluation.  The audit imports neither the primary verifier, `GLS31`, nor
SymPy.  It rebuilds the graph with standard-library `Fraction`, uses a
separate recursive matching engine, sparse incremental reduction, and a
literal independent assembly of the `GLS23` labelled nuisances.

Both routes reproduce the maximum-root cross-product certificate, incidence
ranks `(3,3,2,2,2)`, all three polarized equations, all six responses,
complete pair/top ranks, pure coefficients, `316` mixed failures, and the
Hamming-one value.  The arbitrary-root quantifier of the singleton identities
rests on the written multilinear contraction proof, not the finite graph.

## Rejected stronger claims

The following are not licensed:

- the one-active or two-active normal-product divisor is excluded;
- singleton-kernel silence forces a nonzero deck or response;
- the first-polarized suppliers are legal selectors;
- simultaneous complete absorption is impossible on a hypothetical witness;
- the evaluation plane lies in the maximum-root locus;
- an `r=3` graph supplies arbitrary-root case coverage;
- the graph is a witness or exact counterexample; or
- the maximum-root surplus-two node or global conjecture is closed.

## Remaining load-bearing obligation

The one-active projected shore-normal plane is exhausted as a sufficient
equation family.  The next equation must retain residual-`Q` colours or actual
root-coordinate directions outside `span{s_i,n_i}`, and must be coupled
pointwise to every divisor, response, and rank-drop fibre.  It must either
produce a complete-`GLS23` separator with nonzero physical response and every
declared downstream gate, or contradict the original mixed GHZ coefficient
deck.  Two-active, other-shore, and arbitrary-root source coverage remain
separate open obligations.
