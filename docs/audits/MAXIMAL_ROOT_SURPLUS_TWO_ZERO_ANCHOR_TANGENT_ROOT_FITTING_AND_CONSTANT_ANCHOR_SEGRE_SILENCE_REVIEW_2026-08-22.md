# Hostile review: zero-anchor tangent-root Fitting boundary and constant-anchor Segre silence

## Verdict

**Accepted at the exact corrected scope.**  The four `GLS33` polynomial
profiles have the stated block-kernel decomposition.  The explicit ambient
shore-matrix certificate proves that the rank-`75` Fitting open is nonempty,
but does not prove that this open meets the maximum-root GHZ witness locus.
On that open the six blind directions are exactly the two tangent-root
syzygy families.

The constant root-deck equation gives the stated pointwise non-silent/silent
dichotomy on every local-row and `p` fibre.  The zero-support case is included,
and the one-/two-/three-colour silent locus has the declared killed-coordinate
or Segre-line form.  The surviving singleton classes are output-side
covectors, not legal coefficient-side selectors.

The two-active control is accepted only as a **diagonal-silent channel
boundary**.  Its diagonal target restriction and first-polarized singleton
target contractions are zero, but its physical constant deck has defect `4`.
Thus the complete constant equation detects it.  The Krenn--Gu conjecture
remains **UNRESOLVED**.

## Audited base and artifacts

The review was performed from

```text
origin/main = 41e4d19c66c4eae59a9976da515ddb8bf3b191e7
```

against `GLS30`, `GLS32`, `GLS33`, and the coefficient-side legal-selector
interfaces of `GLS22/GLS23` and the later attachment packages.  The tranche
contains

- the `GLS34` theorem document;
- a focused exact SymPy verifier;
- an independent no-import standard-library audit; and
- package-index, current-frontier, and strategic-node-DAG updates.

## Mathematical hostile review

### 1. Exact coefficientwise block decomposition

After choosing bases with `s_0=s_1=e_0`, an arbitrary probe tensor is a
`3 x 3` matrix `(t_ab)` of residual-bidegree `(1,1)` polynomials.  The `00`
profile sets `t_00=0`.  The `10` and `01` profiles then apply the two
multiplication maps `kappa_0,kappa_1` to the tangent first column and row.
Modulo those equations, the `11` profile applies only `mu` to the tangent
`2 x 2` block.  The input blocks are disjoint, giving the exact kernel and
rank formulas without localization.

The shore incidence covector

```text
rho_i=lambda_i^1 xi_i^0-lambda_i^0 xi_i^1=s_i cross N_i
```

annihilates both `s_i` and `N_i`.  Hence its three extensions from either
shore are always blind.  On ranks `(17,17,32)` the two `kappa` kernels and
the four `mu` syzygies have exactly those generators, so the observation
kernel has dimension six and rank `75`.

### 2. Ambient Fitting scope

The four displayed integer shore matrices give exact ranks

```text
(rank kappa_0,rank kappa_1,rank mu,
 rank blind,rank Obs)=(17,17,32,6,75).
```

Nonzero maximal minors prove that the corresponding open is nonempty over
characteristic zero.  This is an ambient shore-data statement.  Neither the
certificate nor genericity proves maximum-root incidence, GHZ equations, or
intersection with the hypothetical-witness locus.

Every exceptional shore is retained by the exact block-rank formula.  A
specialized residual point is a different operation: four scalar evaluations
cannot inherit the global polynomial rank, and `N_i(z)=0` or
`N_i(z) parallel s_i` can silence that point.  The `p=0` divisor is separate.

### 3. Constant anchor dichotomy

For `A_u=span{a_u,b_u}` and `K_u=A_u^perp`, restriction of the diagonal
`Delta` to `tensor_u K_u` is either nonzero or zero.  In the nonzero case one
pure tuple evaluates it nontrivially.  `GLS33` equation (16) then forces
`pH_Uhat` nonzero, and the same tuple evaluated in every one-free-port
equation proves every singleton diagonal class nonzero modulo `A_u`.
Therefore `p=0` is impossible in this branch.

The zero branch is exactly

```text
Delta in sum_u V_1^* tensor ... tensor A_u tensor ... tensor V_m^*,
```

by the kernel of a tensor-product restriction.  This argument is pointwise,
minor-free, and includes local ranks zero, one, and two.

### 4. Exhaustive three-colour silence

After restriction, each colour term is decomposable.  Empty support is
automatically silent.  One surviving term cannot cancel.  Two surviving
terms cancel exactly when their local factors are projectively proportional
at every port and their accumulated scalar has the declared value.

For three surviving terms, one simple tensor is a linear combination of two
others.  Such a combination is simple only when the first two differ in at
most one factor.  Hence all local colour restrictions align away from at most
one exceptional port, where the remaining vector relation is exact.  This is
the standard Segre-line argument and gives an exhaustive case cover for the
three available colours.

### 5. Corrected physical control scope

The modified two-active response-deck graph has

```text
p=-2,
K^00=(K e_0,K e_0,K e_1,K e_1),
K^10=(K e_1,K e_2,K e_0,K e_2),
K^01=(K e_2,K e_1,K e_2,K e_0).
```

Its constant diagonal restriction is zero, every declared `10/01`
three-port singleton product is zero, and all `24` actual `10/01` singleton
defect slices vanish.  The normal identity is `diag(1,2,0)`, and all six
physical responses are nonzero.  However exact four-port matching gives

```text
H_Uhat(e_0,e_0,e_1,e_1)=-2,
pH_Uhat=4,
Delta(e_0,e_0,e_1,e_1)=0.
```

Thus it fails the complete constant equation.  Its fixed profile failure
counts are `(15,10,11,0)`, its pure coefficients are `(0,0,0)`, and it has
`147` normalized-GHZ failures.  It is not a witness, maximum-root control, or
counterexample to `GLS33`.

## Independence review

The primary uses SymPy and imports the committed `GLS30` graph helper.  It
constructs the coefficient matrices, checks exact integer ranks and selected
maximal determinants, verifies `Obs*blind=0`, and reconstructs the modified
physical graph by direct perfect matchings.

The independent audit imports neither the primary, SymPy, nor repository
mathematics code.  It rebuilds the polynomial coefficient matrices and graph
with standard-library integers and `Fraction`, uses a different modular
elimination prime and a separate matching recursion, and obtains

```text
ranks 17/17/32/6/75,
profile failures 15/10/11/0,
zero singleton defect slices 24,
constant defect 4,
original failures 147.
```

Representative support-zero/one/two/three cases are checked independently.
The universal arbitrary-root statements rest on the written proofs, not on
the finite certificate.

## Rejected stronger claims

The following are not licensed:

- the rank-`75` ambient open meets the witness locus;
- a global coefficientwise rank specializes to the same pointwise rank;
- the six tangent-root directions vanish on physical decks;
- diagonal silence makes the physical constant equation silent;
- the two-active graph satisfies the complete `GLS33` equations;
- a nonzero output-side singleton class is a legal coefficient-side selector;
- the classes survive the complete `GLS23` nuisance;
- response, activity, synchronization, or a named downstream entry is forced;
- an `r=3` control supplies arbitrary-root source coverage; or
- the strategic node or global conjecture is closed.

## Remaining load-bearing obligation

Couple the uncontracted tangent-root coefficient directions, physical
root-deck equation, and killed-colour/Segre-line diagonal locus on the same
hypothetical witness, uniformly over every Fitting, residual, `p`, shore-rank,
response, and selector fibre.  Either contradict that combined locus or prove
the coefficient-side rank jump separating `q` from every raw non-`Q` label,
then establish complete nuisance survival, response, synchronization,
activity, and every gate of one named downstream detector.  Other shore types
and higher-root source coverage remain separate.
