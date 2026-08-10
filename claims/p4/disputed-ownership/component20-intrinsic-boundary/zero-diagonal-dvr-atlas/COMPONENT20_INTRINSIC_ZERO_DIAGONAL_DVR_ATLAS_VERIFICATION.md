# Independent verification of the component-20 intrinsic-zero diagonal atlas

```yaml
role: verifier
date_utc: 2026-08-01T15:02:14Z
git_commit: f997c8366b461f3952faef0d35b512318341909d
claim_label: VERIFIED
scope: complete diagonal source-torus DVR/Puiseux atlas over component-20 intrinsic zero bases (p,q)=(0,1),(-1,0), including pointwise Hall H31/H22 obstructions on the sixteen nonzero leading charts
inputs:
  COMPONENT20_INTRINSIC_ZERO_DIAGONAL_DVR_ATLAS_CANDIDATE.md: 1648d1c5660d47964b5ea94f26a93c2571b0265cf32a425ae4e6038f009efd6d
  P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md: dcaae5365f5e2072e798c2ee52dea47c0d5c48f073ed7553ae5f758e9830f0b2
  P4_COMMON_SINGLETON_COMPONENT.md: 9506c62510deebfb19c2cba5fff22940c35946007d9deafb2d12588676c6980d
  P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md: eb5a8fb528a9c367ec059a06a5630cbcb533be5c49a4ecd1ee8148cac6644b32
  P4_TRIPLE_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md: 81b7346d5f4ce7205dc4c4563e6ecd95a98c59363db3498b1c355ea62489647c
method: fresh polynomial Pluecker reconstruction, exact real-linear min-plus exhaustion, symbolic leading planes and permanent/minor witnesses, exact centre symmetry, component-hypothesis checks, and direct Hall support
command: uv run --with sympy --with z3-solver python claims/p4/disputed-ownership/component20-intrinsic-boundary/zero-diagonal-dvr-atlas/audit_component20_intrinsic_zero_diagonal_dvr_atlas_candidate.py
outputs:
  audit_component20_intrinsic_zero_diagonal_dvr_atlas_candidate.py: f54bd0526c940d244a3bdc1e7a4953f76f855178053dae0726324afc47f17ede
  COMPONENT20_INTRINSIC_ZERO_DIAGONAL_DVR_ATLAS_VERIFICATION.md: hash reported by replay
limitations: diagonal source-torus DVR/Puiseux arcs only; placement is closure placement under frozen component theorems; no non-diagonal or arbitrary GL4 arcs, component exhaustiveness, arbitrary-order reduction, prize graph, or global Krenn-Gu conclusion
```

## Verdict

**VERIFIED in the stated diagonal scope.**  The verifier did not import or
execute the construction script, did not read or trust its JSON certificate,
and did not read or use the proof-B report or script.  It reconstructed the
atlas before comparing the candidate statement.

## Base geometry and exponent

The normalized mode-zero plane has the regular polynomial Pluecker vector

```text
(p(p+1), -q(q-1), -(p-q+1), (p+q)^2, -(p+q), p+q).
```

It satisfies the Pluecker relation identically and is nonzero at both
`(0,1)` and `(-1,0)`, while all restricted tensor coefficients vanish there.

Let `u,v,r,s,w,h,x0,x1,x2` have the meanings in the candidate.  Directly
from the four plane wedges, the source determinant, and the intrinsic kernel
rows, the verifier obtains

```text
E=3*x0+x1+x2+z+a0-m0-m1-m2-m3.
```

The four kernel-row valuations are `(a0,x0,x0,z)`; the source determinant
contributes `x0+x1+x2`.  This independently explains every term and why the
selected-row shortcut is invalid.

Exact real-linear queries are unsatisfiable for a counterexample on all four
finite ultrametric branches

```text
r<s, s<r, r=s=w, r=s<w,
```

and on the exact one-sided/diagonal axes `u=0`, `v=0`, and `u=v!=0`.
They prove

```text
E>=0,
E=0 iff x1=x2=0 and x0<=-h.
```

The constant arc `u=v=0` has identically zero restriction.  At the regression
point `r=s=w=x0=1,x1=x2=0`, the correct value is `E=1`, whereas

```text
E_bad=x0+x1+x2+h-(m0+m1+m2+m3)
```

gives `-1`.  The old wedge/selected-row shortcut is therefore **REFUTED**.

## Sixteen leading charts

For arbitrary nonzero residue and torus units, exact leading-term extraction
gives the four stated `K0` rows and the four stated wall Pluecker vectors.
All eight wall vectors retain `c0`: a nonzero high-coordinate/`P23` ratio
has nonzero derivative with respect to `c0`, so it cannot be removed by a
common projective rescaling.

Every chart has intrinsic kernel rows `(K0,e,e,e)` and only coefficient
`T1111` nonzero.  Exact upper-minor identities and residue-stable lower-minor
witnesses give, at `(0,1)`,

| branch | interior | wall |
| --- | --- | --- |
| `r<s` | `(2,3,3,3,3,3)` | `(3,4,4,3,3,3)` |
| `s<r` | `(3,2,3,3,3,3)` | `(4,3,4,3,3,3)` |
| equal, no cancellation | `(3,3,3,3,3,3)` | `(4,4,4,3,3,3)` |
| equal, higher cancellation | `(3,3,2,3,3,3)` | `(4,4,3,3,3,3)` |

For the delicate equal/no-cancellation interior `03` pair, the independent
witness in physical plane-row order is

```text
rows (0,2,3), columns (1,2,3):
-c1^2*c2*(pi-theta)^2.
```

Thus `pi+theta=0` causes no rank drop; all four equal/no-cancellation charts
were also specialized directly at `theta=-pi` and retained their profiles
and nonzero pure scalar.

Source `diag(1,-1,-1,1)` followed by the exact mode swap `1<->2` produces
the other eight charts.  It sends raw mode-zero Plueckers by

```text
(a,b,c,d,e,f) -> (-a,-b,c,d,-e,-f)
```

and exchanges profile entries `01<->02` and `13<->23`.  Both plane rows and
all profiles satisfy this identity symbolically.

The exact axes route as follows: `v=0` to `r<s`, `u=0` to `s<r`, and
`u=v!=0` to equal/higher cancellation.  Hence the sixteen charts cover the
nonzero part of the complete diagonal fan.

## Closure placement

The placement labels were checked against the exact hypotheses of the
frozen component theorems and were not used to prove the obstruction.

- All eight interiors contain `e` in every plane, satisfy the three exact
  `B_K0` orthogonalities, and have nonzero active cubic; they lie in the
  component-18 common-singleton closure.
- The six `r<s`, `s<r`, and equal/higher interiors have one exact rank-two
  pair whose kernel contains `e tensor e` and the disjoint binary zero
  product.  They meet the support-one-secant theorem and lie in the
  component-15 closure.  No such placement is claimed for the two
  equal/no-cancellation interiors.
- All eight walls have every pair rank at least three.  Pairs `12,13,23`
  each have rank three with unique relation `e*e=0`, while `e` is not in
  `U0`.  These are precisely the non-common-singleton hypotheses of the
  triple-kernel theorem, so the walls lie in the component-16 closure.

All sixteen remain in the component-20 closure through their explicitly
realized diagonal DVR/Puiseux arcs.

## Pointwise H31 and weighted H22

For every chart the three kernel rows on modes `1,2,3` are `e`.  After an
arbitrary H31 extension and any source deletion, those three rows occupy at
most two columns.  Their all-alpha permanent is therefore identically zero
for all four deletions, arbitrary markings, residues, source units, and
extension entries.

The same direct calculation was made for `D01` and `D23`.  On the finite
homogeneous-weight chart, `lambda` remains symbolic and includes
`lambda=0`; `[1:0]` is checked directly.  In every case the three mapped
`e` rows again occupy at most two columns, so both all-alpha diagonals vanish.
Neither weighted direction can be binary.  Thus all sixteen charts have
empty marked-H31 and weighted-H22 incidence pointwise.

No finite-field inference, parameter grid, or broad search is used.  The
global Krenn--Gu conjecture remains unresolved.
