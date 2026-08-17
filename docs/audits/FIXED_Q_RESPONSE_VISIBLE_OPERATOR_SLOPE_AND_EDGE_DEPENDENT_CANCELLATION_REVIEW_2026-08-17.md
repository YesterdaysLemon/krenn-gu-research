# Fixed-Q response-visible operator slope and edge-dependent cancellation hostile review -- 2026-08-17

## Verdict

**Accepted at the frozen theorem and script hashes below.**  No P0 or P1
defect remains.  The package proves an exact characteristic-zero
response-visible operator-slope interface, a six-independent-pair-slope
identity, an edge-dependent eighteen-word cancellation detector, and a
globally decomposable-channel common-slope exclusion.  It does not force a
nonzero legal operator space, response visibility, cancellation, local
support, physical witness integration, or any permanent restriction.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## Operator spaces and response visibility

For one fixed graph, residual pair, fully supported contraction, basis, and
complete `GLD15` nuisance quotient, let `C_S` be the exact constant
operator-coefficient space and let `R_S(a,b)` be the mixed part of
`aM_S+bZ_S`.  Applying any legal full-nuisance operator identity to the full
fixed-`Q` GHZ equation gives

```text
C_S subset ker R_S,
dim C_S + rank R_S <= 2.
```

Thus rank-two operator supply forces both responses pure, a rank-one line is
either uniquely response-visible or response-invisible, and a zero operator
space imposes no response constraint.  The inclusion is one-way: observed
target shape does not manufacture an operator identity.

On an `M`-active rank-one nuisance chart, the two cofactor minors
`(mu_S,zeta_S)` give the exact operator line and slope `zeta_S/mu_S`.
Their orientation and the same-line determinant
`mu_S zeta_T-zeta_S mu_T` were checked against the complete nuisance span.
On the response-visible seven-target stratum, the stacked mixed-response
matrix has `6*6+78=114` rows, `6441` total `2 x 2` minors, and `3348`
cross-target minors after the within-target rank-one relations are removed.

## Edge-dependent cancellation detector

For independently normalized pair slopes `p_e` and four-port slope `t`, the
selected response obeys the exact complementary-matching identity

```text
T=sum_(e|f) [
  D_e D_f
  +(t-p_f) D_e K_f
  +(t-p_e) K_e D_f
  +(p_e p_f-t(p_e+p_f)) K_e K_f
].
```

The homogeneous polynomials in projective row coordinates are explicitly
scoped as the closure of the all-`M`-active chart.  The theorem does not extend
the normalized detector onto pure-`Z` axes.

When all three quadratic corrections vanish and one complementary pair is
three-full with both slopes different from `t`, twelve oriented `2+1+1`
mixed rows force its two physical `K` blocks diagonal.  The six ordered
`2+2` rows then give the rank-five ratio system

```text
r_e^c+r_f^d=1  for c!=d,
```

whose solutions are `(r,r,r,1-r,1-r,1-r)`.  The physical block-rank bound
forces `r=0` on one edge and rank three on the other, a contradiction.
Therefore at least one of the eighteen displayed coefficients is nonzero.

Inside the cancellation locus, nonzero four-port `Z` slope makes the
complementary slope map the involution `p -> tp/(p-t)` and forces every
surviving witness onto the three support divisors.  At four-port slope zero,
each complementary matching instead contains a pure-`M` pair.  These are an
exact conditional split, not proof that cancellation holds.

## Globally decomposable channel boundary

For the stronger physical class

```text
K_uv=a_u tensor a_v  (u<v),
K_vu=K_uv^transpose,
```

one three-full complementary pair excludes a mixed-free four-port response
for every common finite pair/four-port slope.  The channel is globally
vertex-factorable, not an arbitrary collection of rank-one edge blocks.  The
common-line branch inherits the `GLD16` nine-word detector; the special
quadratic-cancellation branch inherits the `GLD17` eighteen-word detector;
and the remaining branch uses a fixed set of twenty-five mixed words.  In the
last branch, the selected `2+1+1` rows force full ternary support and fixed
ratios, after which one `3+1` coefficient equals a nonzero `-6rA`.

Exact controls show the hypotheses are load-bearing: unequal edge slopes can
remain pure after support drops; the noncancellation rank-two physical
fixtures survive full support; and globally decomposable camouflage retains
three-colour activity but no three-full edge.  These are physical response
windows, not legal module rows, witnesses, graph fibres, or counterexamples.

## Independent checks and frozen hashes

The primary replay uses exact SymPy determinants, symbolic slope identities,
matrix ranks, and complete four-port word enumeration.  The independent
audit imports neither SymPy nor the primary; it separately uses standard
library `Fraction` elimination, sparse polynomial dictionaries, raw endpoint
vectors, and direct complementary-matching enumeration.  It also checks the
Wick involution and its fixed points independently.

Both focused scripts pass, as do Ruff check and format-check.  The scripts
replay the bounded identities, minors, ratio system, sharp controls, activity
products, and word ledgers.  The arbitrary-field full-nuisance inclusion and
support proofs remain load-bearing.

Frozen at base HEAD `ba84a2d8173bfdb8c718d9e612ed54fffeba820d`:

```text
theorem  54bfa1fa9a89100869553131b4f6b66354583e0d17b79948ac8f4c66a8842ee3
primary  df7332c766ea2f9158a72f7abde86facf9aa2838aa417b42d4855cd41cd65e22
audit    f15a1a09e98486ec57851a3b505fa5657101633549ccf92f1dd0096e5a32a509
```

## Exact remainder

Still **UNKNOWN**: forcing nonzero operator spaces or response visibility on
every witness; resolving pure-`Z`, zero-space, and invisible rank-one strata;
forcing all three edge-dependent cancellation equations; forcing one
three-full complementary pair; excluding noncancellation and sparse-support
branches for general physical rank-two channels; physical integration beyond
the fixed companion equation; and every weighted-permanent consequence.
