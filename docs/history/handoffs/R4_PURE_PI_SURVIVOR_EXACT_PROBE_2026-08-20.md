# R4 opposite-colour pure-`Pi_Q` survivor: exact bounded probe

Date: 2026-08-20
Branch: `codex/kg-r4-pure-pi-survivor-20260820`
Base: `origin/main` at `df394d387d246d4331359a9ce0f16d7700f724bb`
Global Krenn--Gu status: **UNRESOLVED**

## Status

**Candidate compact refutation of the GLS9 full-rank, literal-all-response-zero,
opposite-colour pure-`Pi_Q` contracted-target locus.**  The exact probe finds
no complete contracted-target point in either GLS9 shore normal form.  It
proves this first in a larger module model in which every active complementary
permanent other than `Pi_Q` is allowed to be an independent tensor.  Therefore
common-incidence permanental integrability, GLS4 quotient survival, and the raw
incidence gate cannot restore a point.

This is a proof-producing discovery, not yet an independently audited theorem.
No owning theorem, audit, ledger, or live-frontier file was changed in this
task.  Promotion requires a separate hostile review of the written invariant
and its correspondence with GLS9 equation (8).  The `det H_Q=0` divisor,
weaker GLS7 response-zero patterns, and nonzero-response absorption branches
remain **OPEN**.

No apparent exact point satisfying all original physical GHZ coefficients was
found.  In particular, there is no counterexample to escalate.

## 1. Exact locus and full coefficient model

Fix distinct residual colours `(i,j,k)`.  In the ordered colour basis
`(i,j,k)`, the GLS9 projection conclusion and full-rank open put

```text
H = [[h_ii, h_ij, h_ik],
     [0,    h_jj, 0   ],
     [0,    h_kj, h_kk]],

det H = h_ii h_jj h_kk != 0,
Pi_Q = nu e_k^(tensor 4),             nu != 0.          (1)
```

The three target weights `mu_0,mu_1,mu_2` are nonzero.  The probe substitutes
each GLS9 normal form into the complete labelled six-slot equality

```text
sum_(P in binom(B,2)) sh_(P,B-P)(H_P tensor Pi_P)
  = sum_(c=0)^2 mu_c product_(v in B)e_(v,c)^*.          (2)
```

It explicitly materializes all `3^6=729` coefficient equations in slot order
`(q0,q1,u0,u1,u2,u3)`.  It does not replace (2) by the GLS9 projection.
Because all `U--U` blocks vanish, only `Q`, the active `q0--U` pairs, and the
active `q1--U` pairs occur.

The non-`Q` tensors `Pi_(q0,u)` and `Pi_(q1,u)` are deliberately independent
four-slot tensors.  This drops, rather than adds, common-incidence equations.
The resulting systems have:

| Shore | Relaxed variables | Full coefficient equations | Structurally nonzero equations in canonical charts |
|---|---:|---:|---|
| singleton | 174 | 729 | `138` to `170`, depending on `(a,b)` |
| two-port | 339 | 729 | `406` for each coordinate-factor colour |

For the nine canonical singleton coordinate choices `(a,b)`, the exact
nonzero-equation counts are

```text
(0,0):142  (0,1):168  (0,2):166
(1,0):170  (1,1):142  (1,2):167
(2,0):167  (2,1):166  (2,2):138.                       (3)
```

Every actual incidence-integrable contracted target on the GLS9 survivor
would be a point of this relaxed system.  Emptiness of the relaxation is thus
a sound exclusion; it is not an inference from a sampled incidence atlas.

## 2. Singleton certificate

Let the singleton active port be `t`.  At the complete coefficients with
`q0=q1=i`, every `q1--t` term vanishes because its residual factor is `e_j`.
Move the `H tensor Pi_Q` term to the target side.  The exact four-port tensor
that the remaining `q0--t` companion must equal is

```text
D_i = mu_i e_i^(tensor U) - nu h_ii e_k^(tensor U).    (4)
```

The two coefficients in (4) are nonzero on the declared open.  Flattening at
`t | U-{t}` gives rank two.  The complete singleton companion contribution is
one simple tensor, so its flattening has rank at most one.

The script records a denominator-free four-coefficient certificate.  Write
`A_ii,A_kk,A_iK,A_kI` for the two diagonal and two crossed entries of that
flattening and

```text
E_ii = A_ii - mu_i,
E_kk = A_kk + nu h_ii,
E_iK = A_iK,
E_kI = A_kI.                                           (5)
```

The singleton minor is identically

```text
A_ii A_kk - A_iK A_kI = 0.                            (6)
```

Consequently the coefficient ideal contains

```text
mu_i nu h_ii
 = E_ii E_kk - (nu h_ii)E_ii + mu_i E_kk - E_iK E_kI. (7)
```

Thus localization at `D(mu_i nu h_ii)` is the unit ideal.  This is the
smallest singleton gap: four original coefficients require a nonzero `2x2`
minor while the shore supplies rank at most one.

The complete legitimate singleton open is

```text
D(alpha beta nu mu_0 mu_1 mu_2 h_ii h_jj h_kk),       (7a)
```

where `alpha,beta` are exactly the two known-nonzero local coordinate
coefficients.  The shorter open used by the certificate is already sufficient;
no unproved generic entry is inverted.

The probe verifies (7) on all

```text
6 ordered colour triples
* 4 singleton-port choices
* 3 q0-local coordinate choices
* 3 q1-local coordinate choices
= 216 exact singleton charts.                          (8)
```

## 3. Two-port line forcing and the one-coefficient gap

Write the ordered active ports as `(s,t)`, choosing `s` to carry the coordinate
factor.  The exact GLS9 form is

```text
alpha_s = sigma e_a,                    sigma != 0,
alpha_t = b_i e_i + b_j e_j + b_k e_k, alpha_t != 0,

A_s=e_i tensor alpha_s,     C_s= tau e_j tensor alpha_s,
A_t=e_i tensor alpha_t,     C_t=-tau e_j tensor alpha_t,
tau != 0.                                                   (9)
```

Choose a legitimate coordinate open `D(b_p)` for the nonzero second factor.
At `q0=q1=i`, freeze the two inactive ports first to colour `i` and then to
colour `k`.  The two active-port matrices have the module form

```text
M_c = alpha_s x_c^T + y_c alpha_t^T,                  (10)
```

and the complete target equations require

```text
M_i = mu_i E_ii,
M_k = -nu h_ii E_kk.                                  (11)
```

For a nonzero scalar `delta`, membership

```text
delta E_cc in alpha_s tensor K^3 + K^3 tensor alpha_t (12)
```

forces the line `K e_c` to be one of `K alpha_s,K alpha_t`.  Coefficientwise,
if `a!=c`, row `c` of (10) is `y_c b^T`.  If `E_cc` and `E_cd` denote the
corresponding equations, the exact certificate is

```text
b_c E_cd - b_d E_cc = delta b_d       for every d!=c. (13)
```

Since `delta` is nonzero, (13) forces `b_d=0` for `d!=c`, and the diagonal
equation forces `b_c!=0`.  Applying this to both equations in (11) gives

```text
{K alpha_s, K alpha_t} = {K e_i, K e_k}.              (14)
```

There are only two residual coordinate ideals:

```text
a=i:  J_i=(b_i,b_j) on D(b_k),
a=k:  J_k=(b_j,b_k) on D(b_i).                        (15)
```

If `a=j`, the two required lines are incompatible.  If the selected nonzero
pivot is not the remaining line in (15), the chart is already empty.

On either ideal in (15), inspect the single **original**, unprojected all-`j`
coefficient.  The `H tensor Pi_Q` term vanishes because `Pi_Q` is pure in
colour `k`; every `q0--U` term vanishes because `q0=j!=i`; and every `q1--U`
term vanishes because both local factor lines have zero `j` coordinate.  The
coefficient equation is therefore exactly

```text
-mu_j = 0,                                             (16)
```

contradicting `D(mu_j)`.  The nonzero `tau` is retained in every chart; it is
not set to one or discarded.

The complete covering atlas has

```text
6 ordered colour triples
* 12 ordered active-port choices (which port is coordinate)
* 3 coordinate-factor colours a
* 3 selected nonzero coordinates p of alpha_t
= 648 chart instances.                                (17)
```

These covering charts overlap when both factors are coordinate.  Their exact
disposition is:

| Class | Count |
|---|---:|
| `a=j`: two incompatible required lines | 216 |
| required other line contradicts the selected nonzero pivot | 288 |
| residual ideal (15), then the all-`j` gap (16) | 144 |

The full saturation ledger is

```text
D(sigma tau b_p nu mu_0 mu_1 mu_2 h_ii h_jj h_kk).    (18)
```

No component is removed by an unproved generic-entry assumption.  The only
entry of `alpha_t` inverted on a chart is its selected known-nonzero
coordinate `b_p`.

## 4. GLS4 gates and exact control point

The physical incidence model consists of six labelled `4x3` matrices `L_u`.
The exact representable GLS4 gates are recorded as follows.

- `rank L_u>=1` and `sum_u(3-rank L_u)<=6` have 435 exact rank profiles.
  Each exact-rank stratum is given by all larger-minor zero equations and one
  selected rank-minor open.  The overlapping selected-minor atlas has
  `428295232` chart instances; it is counted, not enumerated.
- Pure `Pi_Q` is 80 permanent-coefficient zero equations together with
  `Pi_Q[kkkk]=nu` on `D(nu)`.
- Raw `p_(A,Q)` nonvanishing is the union of 54 coordinate opens

  ```text
  D(L_q0[r,a]L_q1[s,b]+L_q0[s,a]L_q1[r,b]),
  r<s, a,b in {0,1,2}.                                 (19)
  ```

- On an actual GLS4 source, nonzero `Pi_Q` supplies individual order-two
  quotient survival by the owning theorem.  It is not encoded as an invented
  scalar condition in the contracted model.
- Maximum-root maximality is not equivalent to these incidence ranks and is
  not encoded by the probe.

The script replays the exact rational GLS9 source control with

```text
(i,j,k)=(0,1,2),   T={u0,u1},   H=I_3,   tau=1,
alpha_s=e_0,       alpha_t=e_1.                            (20)
```

It obtains

```text
rank(L_q0,L_q1,L_u0,L_u1,L_u2,L_u3)=(2,2,3,3,2,1),
total corank=5,
Pi_Q[2222]=1 and every other Pi_Q coefficient is zero,
raw p_(r1 r2,Q)[q0=1,q1=0]=1,
det H=1,                  H(1,1)=3.                    (21)
```

The existing GLS9 theorem verifies this graph's maximum-root property.  This
probe does not re-promote that fact and does **not** verify GLS4 quotient
survival for the off-target control.

The complete 729-coefficient residual has exactly six nonzero entries:

```text
000000 : -1
002222 :  1
010222 :  2
111111 : -1
112122 : -1
112222 :  1                                              (22)
```

Thus the control is a maximum-root/raw-incidence boundary point, not a
complete contracted-target point, not a quotient-survival point established
by this probe, and not an actual witness.  The previously displayed
`002222=1` gap is recovered as one of the six exact failures.

## 5. Points, ideals, and conclusion

```text
complete contracted-target points found:                0
actual maximum-root witnesses found:                     0
quotient-survival points independently established here: 0
singleton localized ideal:                              (1)
two-port localized ideal:                               (1)
global Krenn--Gu conjecture:                             UNRESOLVED
```

The smallest invariant gaps are:

1. singleton: the forbidden minor `-mu_i nu h_ii`, a rank-two-versus-rank-one
   discrepancy from four complete coefficients;
2. two-port: after the coefficientwise line forcing (13), one original
   all-`j` coefficient is `-mu_j`.

No Groebner basis, sampling inference, numerical solve, or positive-dimensional
stopping claim is used.  The compact module invariant resolves the relaxed
contracted system before incidence elimination is necessary.

## 6. Exact commands and observed results

Run from repository root:

```powershell
python tools/explore/r4_pure_pi_survivor_exact_probe.py
python -m py_compile tools/explore/r4_pure_pi_survivor_exact_probe.py
uvx --from ruff==0.16.2 ruff check --no-cache tools/explore/r4_pure_pi_survivor_exact_probe.py
uvx --from ruff==0.16.2 ruff format --check --no-cache tools/explore/r4_pure_pi_survivor_exact_probe.py
python check_hygiene.py
```

The probe printed status

```text
candidate_compact_refutation_of_the_GLS9_pure_Pi_contracted_locus
```

with 216 singleton charts and 648 covering two-port charts excluded, zero
complete contracted-target points, zero actual witnesses, and the six exact
control residuals in (22).  Compilation passed.  Ruff reported `All checks
passed!` and `1 file already formatted`.

The hygiene run completed every compile, artifact, link, ledger, portability,
layout, stale-path, provenance, manifest, fast-verifier, and version check.  It
exited with code one only at the candidate-index completeness gate because the two
authorized probe files and a separately owned concurrent theorem file were
untracked and unstaged.  This task did not stage, edit, or otherwise touch that
theorem file.

## 7. Promotion boundary

A promotion review should independently check only the following compact
points before touching GLS9 or the live frontier:

1. equation (2) has the same labelled shuffle convention as GLS9 equation
   (8), with no missing pair multiplicity;
2. (1) is exactly the GLS9 projected-`H` conclusion on `D(det H)`;
3. the singleton four-entry certificate (7) uses original coefficients;
4. the two-port row certificate (13) covers rank-one, rank-two, and both-
   coordinate local factors without an illicit open;
5. the all-`j` equation (16) has no surviving `H`, `A`, `C`, or direct-port
   term;
6. closing this one GLS9 leaf does not close `det H_Q=0`, the broader GLS7 `R`
   branch, nonzero-response absorption, the supply/attachment strategic node,
   or the global conjecture.

Until that audit is complete, this handoff should be cited as an exact bounded
probe and candidate proof, not as a merged theorem.
