# M1 — the specialization-divisor extraction pass (symbolic route)

Branch: `symbolic/m1-extraction-pass`, forked from the merged canonical
continuation (`main` @ f24782f, PR #27).

## Why this branch exists

`P5_DELTA3_OBLIGATION_LEDGER.md` III.2 names M1 as *the one force
multiplier that changes the arithmetic*: each successful extraction run
converts the implicit Gröbner denominators of a generic `H31`/`H22`
fibre theorem into an explicit bounded list of curves/hypersurfaces,
and every closure it produces is pointwise — the currency the master
theorem actually accepts.  The ledger orders it **before** any further
hand-crafted divisor work, so hand effort is spent only on loci that
provably carry survivors.

Sixteen runs are listed (`H31`: components 3–8 and 10; `H22`:
components 1, 3–10), plus component 2 `H22` which needs a replacement
proof first.  This branch exists to run them component-by-component.

## Toolchain — verified on this machine

- Singular 4.3.2 runs under WSL (`wsl -e bash`), on `PATH`.
- Python 3.12 with `sympy`/`numpy` installed at user level
  (`python3 -m pip install --user --break-system-packages sympy numpy`).
- The ledger scripts resolve the repo root from `__file__`
  (commit `07e34de`), so they run from any checkout location.

Reproduction of the known-good reference (ninth component, `H31`):

```
cd research_snapshots/2026-08-04-p5-delta3-obligation-ledger/scripts
wsl -e bash -c "cd $(pwd) && python3 extract_p5_h31_ninth_explicit_divisors.py"
```

Measured here: all four frames `q0,q1,q2,q3` extract, wall time
~460 s, and the contraction generators reproduce the committed
ledger byte-for-byte except the per-run timing fields.  That is the
go/no-go gate for any further extraction on this machine.

## Known-hard instance: tenth component, `H31`

`extract_p5_h31_tenth_explicit_divisors.py` is the recorded timeout-null
(840 s budget exceeded in the corpus, re-confirmed here; a staged
eliminate-t-first variant also exceeds 240 s before producing output).
Structural facts established on this branch (all over
`K = Q(b,e,m,c)`, the `k=1` gauge):

- the system is 16 equations in 13 variables
  `x0..x3, y0..y3, w, t0..t3`;
- every equation is **multilinear** (each variable appears to degree ≤1);
- the 14 mixed equations are **linear in the 15 `t`-monomials**
  `1, t_i, t_i t_j, t_i t_j t_k`, and their coefficient matrix has
  full row rank 14 over `Q(x,y,b,e,m,c)`;
- the 14 mixed forms are pairwise **not** monomial multiples of one
  another, and do not collapse to a small core by simple `t`-monomial
  combinations (reductions modulo the `t`-free form `A` leave 2–26
  terms), so the elimination is genuinely 14-way, not redundant.

That last point is the honest diagnosis: the bottleneck is not a
mis-posed or redundant system but a genuinely large multilinear
elimination.  Candidate symbolic routes to try **before** any longer
raw Gröbner run, in order of expected payoff:

1. **Determinantal/Fitting formulation.**  Because the mixed block is
   linear in the `t`-monomials, existence of a nonzero `t`-kernel is a
   rank condition on a `14 x 15` coefficient matrix over
   `Q(x,y,b,e,m,c)`.  The contraction we want is a Fitting ideal /
   rank-drop locus, which Singular's `minor` + `eliminate` may handle
   with a better monomial order than the current direct elimination.
2. **Block ordering.**  Eliminate in the order the geometry suggests:
   the four `t`-coordinates first (they are the marking), then `w`,
   then the two `y`-pairs, rather than the single `eliminate` over all
   13 variables.  The current script already uses a `dp(13),dp(4)`
   product order but a single `eliminate`; splitting into successive
   `eliminate`/`interred` passes with `slimgb` between them is the
   recorded mitigation that unblocked the ninth's frame `q2`.
3. **Two-stage with the `A-1` Rabinowitsch last.**  Adjoin the
   `t`-free normalization `A=1` before eliminating the `t`-block so
   the elimination runs over the affine chart, then handle `w*B=1`
   afterward.

Every run stays **fail-closed**: a timeout or parse failure is recorded
as `timeout_null`/`parse_failure` in the JSON ledger, never as success.

## Deliverables for this branch

- one extraction ledger JSON per component/frame run, named
  `extract_p5_<frame>_<component>_explicit_divisors.json`;
- a short `EXTRACTION_RUN_LEDGER.md` tabulating, per run, the extracted
  generators and their factorization (the list M2 then consumes);
- no global-status claim.  Each run is a local finite computation;
  the conjecture stays **UNRESOLVED**.
