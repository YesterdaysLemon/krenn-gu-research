# Fixed-Q unequal-slope quadratic-cancellation hostile review -- 2026-08-17

## Verdict

**Accepted at the frozen theorem and script hashes recorded below.**  No P0
or P1 defect remains.  The result is an exact characteristic-zero
eighteen-word response detector and a conditional fixed-module witness
exclusion on two special unequal-slope branches.  It does not force the
operator slopes or local nonvanishing on every witness, classify all unequal
slopes, or imply a permanent restriction.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## Unequal-slope identity

With one common pair slope `[1:p]` and four-port slope `[1:t]`, the selected
physical `h=0` package satisfies

```text
D_e=B_e+pK_e,
T=C(D)+(t-p)X(D,K)+p(p-2t)C(K).
```

On the two branches `p=0,t!=0` and `p=2t,t!=0`, the quadratic `C(K)` term
vanishes while `q=t-p` remains nonzero.  This gives the exact reduced identity

```text
T=C(D)+qX(D,K).
```

The normalization is load-bearing: one fixed graph, residual pair,
contraction, ternary basis, and `M/Z` coefficient plane are used.  All six
pair rows have the same `p`, and the four-port row has one fixed `t`.
This is an `M`-active normalization; pure-`Z` pair axes are outside the
theorem.

## Eighteen-word detector

Assume all six `D` blocks are diagonal and one complementary pair `e|f` is
three-full: both blocks have all three diagonal entries nonzero.  The twelve
oriented `2+1+1` mixed words isolate every off-diagonal entry of `K_e` and
`K_f`, forcing both physical channel blocks to be diagonal.  The six ordered
`2+2` words then give

```text
r_e^c+r_f^d=1    for c!=d.
```

Over three colours, the exact solution is
`(r,r,r,1-r,1-r,1-r)`.  Since each physical `K` block has rank at most two,
one diagonal entry of `K_e` vanishes, forcing `r=0`; all three entries of
`K_f` are then nonzero, contradicting its rank bound.  Therefore at least one
of the eighteen displayed mixed coefficients of `T` is nonzero.

The proof uses global pair diagonality to kill the two other complementary
matchings but uses nonvanishing only on the six entries of the named pair.  It
does not assume rank-two local frames, concision, or a nonzero pure coefficient
of `T`.  The six-value condition is a local sufficient hypothesis, not a
claimed exhaustive or globally minimal support classification.

## Sharpness controls

Three exact physical response windows delimit the statement:

- The `GLD16` `p=2,t=1` fixture lies on the cancellation branch, has pure
  four-port values `(-12,1,1)` and full three-colour activity, but has no
  three-full complementary pair.  The six-value condition cannot simply be
  omitted.
- With `K_e=diag(2,-2,0)`, `B_e=E_22`, and `(p,t)=(1,0)`, every selected pair
  block is `diag(2,-2,1)`, all eighteen pair values are nonzero, activity is
  full, and `T=3e_2^tensor4` is pure.  The quadratic-cancellation relation is
  essential.
- Supporting the three colours of `B` on the three perfect matchings gives
  `T=(1,1,1)` and makes `14|23` three-full with both selected blocks
  `diag(2,-2,1)`.  Thus the slope boundary persists with pure normalization
  and the exact local six-value hypothesis.

These controls are response-algebra fixtures, not legal module-selector rows,
hypothetical witnesses, graph fibres, or counterexamples.

## Independent checks and frozen hashes

The primary uses exact SymPy symbolic matrices, determinants, nullspaces, and
tensor enumeration.  The independent audit imports neither SymPy nor the
primary; it separately uses sparse polynomial dictionaries, direct
complementary-match enumeration, `Fraction` elimination, and raw endpoint
vectors for the physical channels.  Both construct exactly eighteen distinct
mixed words and verify their displayed formulas.

The two focused commands pass, as do Ruff check, Ruff format check,
conflict-marker scanning, and `git diff --check`.

Frozen at base HEAD `53756977b3e919d717a7a8cbc8444cd5916422f4`:

```text
theorem  923c58104dd64441eecf75d8784b14ceadeab00f3e6fbb969ce056f806000bb3
primary  885234064f0ca30f65991cf0b977f505fba547788a0bf349fab49597ac727fc2
audit    fc6e631bd90711ac2497fa76abcf9794a4928f67f5aa2bd4c475d77fed851ad0
```

The scripts replay the bounded identities, word supports, ratio system, and
controls.  The arbitrary-field support and physical-rank proof remains
load-bearing.

## Exact remainder

Still **UNKNOWN**: forcing the required pair/four-port operator slopes;
forcing a three-full complementary pair on the witness locus; excluding the
other unequal-slope values; physical integration beyond the fixed companion
equation; and every weighted-permanent consequence.
