# GLD101 `a=0`, d2 B-open compact portable leaf package

Status: **scoped exact repository package; not a theorem or frontier change**.

The global Krenn--Gu conjecture remains **UNRESOLVED**. Integration requires a
clean committed-tree replay and an independent reviewer receipt.

## Exact statement packaged

On the normalized equal-leaf H4 branch

\[
  a=0,\qquad p^2+1=0,\qquad Q_6(p,q)=0,
  \qquad B\,H_2\,\Delta\ne0,
\]

rank at most six makes the six actual selected minors

\[
  T_0,T_1,T_2,T_3,Y_1,X_3
\]

vanish. On `B!=0`, writing `C=B*t` and cancelling the reversible common B
factor gives six Gaussian equations. At `p=i`, the ideal

```text
Q6, H_T3, H_Y1, H_X3, z*B*Delta-1
```

has an exact unit lift. The `p=-i` branch follows coefficientwise by
conjugation because the parent equations have rational coefficients. The
separately required H2 gate is explicit:

```text
H2(i) = 2*i^2 - 2*i + 1 = -1 - 2*i,
Norm(-1 - 2*i) = 5.
```

This uses the minimum-cardinality core `{T3,Y1,X3}`, but the package retains
and reconstructs all six actual minors so the rank-to-selected-minor bridge is
visible. No converse from selected-minor vanishing to rank is used or claimed.

## Tracked portable seam

The certificate
`claims/arbitrary-order/certificates/GLD101_A0_D2_BOPEN_T3_Y1_X3_PORTABLE_CERTIFICATE.json`
contains:

- repository-relative LF-normalized pins for GLD71, GLD88, GLD101, and the
  prior no-import GLD102 audit;
- the exact row/column definitions and primitive Gaussian equations for all
  six selected minors;
- every cleared denominator factor and the assertion that it lies in Delta;
- the squarefree quartic Q6, its coprime Delta remainder, and the H2 norm-5
  gate;
- the exact 66-line Singular source hash and expected unit-lift markers; and
- accepted lineage plus explicit quarantine of invalid or non-independent
  precursors.

The certificate LF SHA-256 is
`e4d0c5a07a930d8c4305a897e613b73185d48df885f9907f0e67a41fc593338c`.
The generated Singular source is 7,155 bytes with SHA-256
`58530b32e87ff5a4198478c375755ed0452a4c6351ee234872796155c2dd4199`.
Neither that generated `.sing` file nor the historical 47 MB transcript is
tracked.

## Two verification routes

The lightweight primary
`claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_d2_bopen_portable.py`
consumes only the tracked JSON. It checks canonical serialization, scope and
nonclaims, reconstructs Q6 and Delta from rational formulas, checks
squarefreeness/coprimality and the H2 norm, validates every Gaussian equation
digest, and regenerates the solver source byte-for-byte.

The independent audit
`claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_d2_bopen_portable.py`
imports no repository module and no primary checker. It AST-parses the literal
37-row GLD71 relation tuple, locally transcribes the pinned GLD88 H4 chart,
rebuilds the six seven-by-seven determinants directly, performs the B-open
substitution and cancellation, checks all denominators against Delta, reduces
modulo Q6, and regenerates the same source. A fresh run on the package worktree
took about 364 seconds.

## Reproducible replay

From a clean export of the commit containing this package:

```text
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_d2_bopen_portable.py
python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_d2_bopen_portable.py
python -m unittest -v tests.test_gld101_d2_bopen_portable_certificate
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_d2_bopen_portable.py --emit-singular build/gld101-d2-bopen.sing
python tools/research/run_bounded.py --run-id gld101-d2-bopen-portable --timeout-seconds 600 --memory-mb 8192 -- Singular build/gld101-d2-bopen.sing
```

On Windows, use the repository's WSL Singular route if native `Singular` is
absent. The generated source must retain its exact hash. A bounded replay must
exit zero with a singleton nonzero constant basis, unit column 1, a zero
`matrix(I)*T-matrix(L)` check, five nonzero multipliers, and
`IDENTITY_SUM_MINUS_ONE` equal to zero, followed by:

```text
CERTIFICATE_EXACT 1
RUN_COMPLETE 1
```

A timeout, nonzero exit, error marker, missing marker, source-hash mismatch,
or disagreement between reconstruction routes fails closed.

## Evidence quarantine

- Cross-audit comparators v1 through v4 are invalid non-evidence: they omitted
  the required denominator inverse when comparing a cleared numerator with a
  rational coefficient modulo Q6.
- The historical transcript checker is corroborative only. It checks hashes
  and multiplication-back markers but does not independently derive the six
  equations.
- Machine-local source and large transcript artifacts are superseded as
  portability evidence. Their hashes remain provenance, not runtime inputs.

## Nonclaims and frontier decision

This package makes no claim on `B=0`, does not supply the separate generic
C-open or R4 B-open leaves, and proves no endpoint or physical statement. It
does not establish a P6 or P8 parent theorem, arbitrary `a`, full E31, or the
global conjecture.

No `docs/current-frontier.md` edit accompanies this package. Parent-level or
frontier promotion requires the separately portable leaf seams, their tracked
composition checker, clean-export replay, and adversarial independent review.
