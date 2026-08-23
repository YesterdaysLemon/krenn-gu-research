# Hostile review: zero-anchor simultaneous absorption, evaluation pencils, and mixed-equation sharpness

## Verdict

**Accepted at the exact stated scope, subject to the corrections already
incorporated in `GLS31`.**  The physical polarization identities type-check,
the sparse rational graph independently replays, and the graph simultaneously
meets the declared maximum-root, pure, normal, complete-nuisance, and
top-diagonal gates.  It fails `313` original mixed GHZ coefficients and is
therefore an insufficiency certificate, not a witness or counterexample.

The theorem changes the live frontier only by eliminating the proposed
static incidence/absorption coupling as a sufficient route and by recording
the exact first-polarized equations that must be retained next.  It does not
close any divisor, supply a selector, close the strategic node, or change the
global status.  The Krenn--Gu conjecture remains **UNRESOLVED**.

## Audited base and artifacts

The audit was performed from

```text
origin/main = 8771e5433c23a5c55f690f15743e75c4b3fe4719
```

against the owning `GLS22`, `GLS23`, `GLS26`, `GLS29`, and `GLS30`
interfaces.  The reviewed tranche consists of

- the `GLS31` theorem document;
- its focused exact SymPy verifier;
- its independent standard-library `Fraction` audit; and
- the frontier, package index, and node-DAG updates in the same candidate
  tree.

## Mathematical hostile review

### 1. Evaluation pencils are not root-locus pencils

The vectors `n_i` are normals to the two residual shores.  Nothing in the
owning packages says that `s_i+tau n_i` remains a torus root or is tangent to
the maximum-root variety.  Early draft language calling these expressions
"root pencils" was rejected.  `GLS31` now calls them evaluation pencils in
the two `A` slots and draws no maximum-root conclusion along them.

### 2. Projector cancellation and the common factor `p`

For a promoted pair, the raw coefficient has four bidegrees

```text
K^00 + tau K^10 + upsilon K^01 + tau upsilon K^11.
```

Because `q` is constant on the evaluation pencil, `P_Q` cancels the constant
`K^00` term and multiplies the other three by `p`.  The complete coefficient
equations initially have this factor on both sides.  The final proof cancels
it only by citing the declared gate `p!=0`; it does not silently divide by a
response, normal coordinate, or rank minor.

### 3. One-`Q` terms are mandatory

For `{q_s,u}`, polarization gives the exact degree-one terms

```text
p tau lambda_1^s x_u,
p upsilon lambda_0^s y_u,
```

and no bidegree `(1,1)` term.  These multiply the intact labelled deck
`S_(s,u)`.  Omitting them would turn the first-polarized equations into a
false six-supplier identity.  The audit also rejected interpreting `S_(s,u)`
as a pair response or `K^10,K^01` as selectors.

The label `D=Q` projects to zero.  The top label disappears only under the
explicit zero-anchor hypothesis `omega=0`; on the nonzero-anchor branch it
would contribute at positive bidegrees.

### 4. Root order and tensor type

The target tensor in the arbitrary-root identities is
`e_c^(tensor m)`, `m=2r-2`.  An earlier fourfold display was valid only at
`r=3` and was corrected.  Canonical port reordering is declared in every
`K_D`.

### 5. The retained-root quotient is not new

The contraction `C_0` is surjective on `E_A^tr` and maps the residual tangent
envelope onto `X_1`.  The quotient isomorphism uses
`d_0=d_1=2`; without that gate its source dimension is
`(3-d_0)(3-d_1)` and the assertion need not hold.  The diagonal class maps to
`p n_0(c)[e_c]`, whose remaining quotient evaluation is
`p n_0(c)n_1(c)`.  Thus the construction recovers exactly `gamma`, not a
second support-free invariant.

This does not prove that no target-specific legal selector exists.  It proves
only that the displayed quotient contraction supplies no new one.

### 6. Exact graph interface

The graph was rebuilt from the displayed matrices rather than from discovery
state.  The following were checked exactly:

- the displayed root equations;
- monomial-edge independence number three, hence maximality of the root;
- outside incidence ranks `(2,2,1,2,2)` and defect six;
- `q=E_11+E_22`, `p=2`, rank-two shores, and `gamma=(1,0,0)`;
- all six suppliers `2E_00` and response scalars
  `(1,1,1,1,1,-9/2)`;
- the scalar normal tensor `e_0^(tensor4)`;
- pure coefficients `(1,1,1)`;
- all six nonzero promoted desired tensors;
- complete pair-nuisance ranks `(36,36,36,50,50,50)` and absorption of each
  desired tensor;
- top nuisance rank six, diagonal rank two, and exact diagonal containment;
  and
- exactly `313` nonzero mixed words, including the displayed coefficient
  `-1`.

The pair nuisances use the literal `GLS23` intersection cases.  In particular,
a kept one-`Q` coefficient tensor is not illegally split into separate kept-
port columns.

### 7. Off-target status

The graph passes pure normalization but fails original mixed coefficients.
Therefore it is not on the complete hypothetical-witness locus.  Statements
such as "the `GLS26` inclusion holds" mean that the exact target-side linear
inclusion forced by `GLS26` happens to hold for this graph; they do not invoke
the converse of `GLS26` or certify the full GHZ hypothesis.

No `GLS4` source permanent, arbitrary-root source cover, legal downstream
attachment package, or exceptional divisor fibre is certified by the graph.

## Independence review

The primary verifier uses SymPy matrices, direct exact rank, and a dense
labelled-slice representation.  The no-import audit does not import the
primary or SymPy.  It independently reconstructs every matrix with
standard-library `Fraction`, uses a separate recursive perfect-matching
engine, and computes ranks through sparse incremental column reduction.  It
also rebuilds the complete labelled nuisances rather than replaying printed
rank summaries.

Both routes reproduce the same maximum-root, incidence, module, response,
normal, pure, and mixed records.  The audit's polarization replay uses a
separate sparse bivariate-polynomial representation.  The arbitrary-root
quantification itself rests on the written multilinear proof, not a finite
sample.

## Rejected stronger claims

The following are not licensed:

- the one-active divisor is excluded;
- simultaneous pair absorption is impossible on an actual witness;
- a first-polarized supplier is a physical response or legal selector;
- the evaluation pencil lies in the root locus;
- the retained-root quotient is independent of the product-normal channel;
- the sparse graph is a witness or exact counterexample;
- `r=3` sharpness closes arbitrary-root coverage; or
- the maximum-root surplus-two strategic node or global conjecture is
  closed.

## Remaining load-bearing obligation

Retain the complete one-`Q` labelled sums in the first-polarized equations and
couple them to the one-/two-active divisor profiles.  Pointwise on every rank,
response, and divisor fibre, one must either produce a complete-`GLS23`
target separator with nonzero physical response and every declared downstream
gate, or derive a contradiction from the original mixed/root-deck equations.
Arbitrary-root source coverage remains separate and open.
