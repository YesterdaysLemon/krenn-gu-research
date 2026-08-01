# Derived projective coverage boundary for embedded-`P3` weighted `H22`

```yaml
role: proof_a
date_utc: 2026-08-01T11:57:01Z
git_commit: 8a30d84c08e5e82f2927ea0f186193a424cde325
claim_label: DERIVED
scope: exact chart and pivot coverage supplied by the normalized embedded-P3 H22 theorems and the verified full r0=0 divisor, including its separately audited t0 nonzero endpoints
inputs:
  P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md: dfc2ca99ac668605b54a08b2a4dfb48f74abba97ae2ecc405121d21b8e7f3f4a
  P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md: baf5531740cfd77207f31cf8e1de2b5b838701cbcae5ec778667e6e7f712d15e
  P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md: 7ae8c19e5a43ac7af2cac35892af59130555ab509495d5280745aad114eed056
  P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_VERIFICATION.md: 55ccdd6cbce892a1171a71f0bbb5e8c04241cb269c98ac797dbdf85e96f4f38b
  P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_T_NONZERO_WEIGHT_ENDPOINTS_OBSTRUCTION_CANDIDATE.md: 71bf270bdf74fe756b89a130fcb64c3eacddd5f28cdc5c9c8ed9a4386c1a9ac7
  P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_T_NONZERO_WEIGHT_ENDPOINTS_VERIFICATION.md: 8e4cbe9b66bd1e53f374ef36e9fd257b410014297d9760cdf5472598f505d838
  P5_H22_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_VERIFICATION.md: b83ddbe1e1f928dd18b9914c2c3433e612e315096888023a343af62ddf52c5c7
method: exact normal-support census, Grassmann Pluecker chart reduction, matching-partner invariants under all source permutations, homogeneous-weight orientation tracking, and explicit nonzero pure counterexamples
command: uv run --with sympy python derive_p5_h22_embedded_p3_projective_coverage_boundary.py
outputs:
  derive_p5_h22_embedded_p3_projective_coverage_boundary.py: 78561496ffad9791c72a3ad44dab2f9184a4803cf4e303e16be78e74079c3248
  P5_H22_EMBEDDED_P3_COMPONENT_PROJECTIVE_COVERAGE_BOUNDARY.md: hash reported by replay
limitations: this is a coverage theorem, not an H22 obstruction on the uncovered strata; the full r0=0 divisor is verified, but the remaining normal-mask, Grassmann-pivot, and orientation-endpoint strata keep the full projective component UNKNOWN
```

## Verdict

**The existing results do not cover the entire projective closure.**  The old
full-support counterexample

```text
[C:A:B]=[1:1:1],             U0=span(e0,e1)
```

is now repaired by the independently supported `r0=t0=0` corner.  However,
`r0=0` is not the only free-plane divisor omitted by the normalized chart.
The independent Grassmann pivot divisor and a matching-sensitive normal
divisor remain uncovered.  A further orientation-specific homogeneous endpoint
is uncovered even where both primary pivots are nonzero.

Consequently the complete embedded-`P3` projective weighted-`H22` fibre remains
**UNKNOWN**.  No positive lift is asserted on any uncovered stratum.

## Frozen chart statement

Let `c` be the source coordinate whose hyperplane contains the embedded pure
`P3` triple.  Freeze the weighted-`H22` perfect matching `M`.  Its unique
partner of `c` is

```text
p=M(c).
```

After naming the remaining matched pair `(q,r)`, the homogeneous normal base
of the last three planes is

```text
n1=(C, A, B),
n2=(C,-A,-B),
n3=(C,-A, B),

(C,A,B)=(n_p,n_q,n_r).                            (1)
```

The pure restriction is nonzero exactly when at least two of `C,A,B` are
nonzero.  The standalone derivation rebuilds kernels for all seven support
masks and obtains

```text
mask 1: {}                 mask 2: {}
mask 3: {T100= 2}          mask 4: {}
mask 5: {T101=-2}          mask 6: {T110=-2}
mask 7: {T100=2,T101=-2}.                           (2)
```

Thus support-one normals are inadmissible, but mask 6 is a genuine pure
boundary and cannot be discarded.

The free plane is transverse to `H_c`, and its intrinsic kernel line is

```text
L=U0 intersect H_c.
```

The normalized and `r0=0` results use the Grassmann chart

```text
P_cp(U0)!=0,                                      (3)
```

equivalently, the `p` coordinate of `L` is nonzero.  In canonical labels
`(c,p,q,r)=(0,1,2,3)`, row reduction gives exactly

```text
alpha0=(0,1,S,U),
beta0 =(1,0,R,T).                                 (4)
```

Its Pluecker coordinates are

```text
P01=-1, P02=-S, P03=-U,
P12= R, P13= T, P23=ST-UR.                        (5)
```

The divisor called `r0=0` is therefore

```text
R=P12=0
```

*inside* the open Grassmann chart `P01!=0`.  It is not the missing pivot
divisor `P01=0`.

## What the current dependencies cover

First assume

```text
C B P01 !=0.                                      (6)
```

Then (1) and (4) are literally the normalized sign/free-plane chart.

- `R!=0` is scaled to the three verified normalized theorems.  Their generic,
  rank-two-line, and rank-one cases exhaust the finite homogeneous-weight
  chart.
- At weight `[1:0]`, both all-alpha weighted contractions have a structural
  zero first column, so neither can be the genuine binary member.
- `R=0,T=0` is the independently supported corner, including homogeneous
  infinity.
- `R=0,T!=0` with `rho*sigma!=0` is supported by the independently checked
  signed transport and invertible rebalance.
- The two `R=0,T!=0` endpoints are independently verified by the named
  endpoint theorem and its no-import audit.

Now take `C A P01!=0,B=0`.  Swapping `q,r` makes the new `B'` nonzero and
changes the free coordinates by

```text
(R',T')=(T,R).                                    (7)
```

It preserves the `D01` weight but reverses the `D23` weight:

```text
D01: [rho:sigma] -> [rho:sigma],
D23: [rho:sigma] -> [sigma:rho].                  (8)
```

For `rho*sigma!=0`, the verified diagonal rebalance is invertible, so the
nonendpoint locus enters the preceding chart.  At `[1:0]`, the direct
all-alpha zero-column obstruction applies.  At `[0:1]`, (8) gives opposite
endpoints and cannot be rebalanced.  If `T=0`, then `R'=0`; the `R=0,T'=0`
corner or the verified `R=0,T'!=0` endpoint theorem covers the point.  If
`T!=0`, the scoped endpoint theorem does not apply.

This is the exact coverage delivered by the named dependency union.  It is
strictly smaller than the full projective closure.

## Invariant omitted divisors

Under a source permutation transported together with `(c,M)`, the pair

```text
(c,p) -> (g(c),g(p))
```

remains the common coordinate and its matching partner.  Hence both zero
conditions

```text
n_p=C=0,                  P_cp(U0)=0               (9)
```

are invariant under all source permutations, coordinate signs/scalings, and
tensor-mode permutations.  The derivation checks all 24 source permutations.
Permuting a perfect matching abstractly does not change these relative
incidences.

There are therefore two unconditional coverage gaps:

1. the **normal partner divisor**

   ```text
   C=0,                  A B !=0;
   ```

2. the **free Grassmann pivot divisor**

   ```text
   P_cp(U0)=0,           U0 not subset H_c.
   ```

There is also the orientation endpoint gap already exposed by (7)--(8):

```text
B=0, C A P01 T!=0,       [rho:sigma]=[0:1].        (10)
```

None of the three normalized theorems, the verified `r0=t0=0` corner, the
`r0=0` nonendpoint transport, or the scoped endpoint theorem treats these
strata.

## The old counterexample is now covered

For

```text
[C:A:B]=[1:1:1],       U0=span(e0,e1),
```

the last three planes form the unique embedded triple in `H0`, and the pure
`P4` support is

```text
T1100=2,               T1101=-2.
```

Here

```text
C B P01 !=0,
(S,U,R,T)=(0,0,0,0).
```

Thus the point does not enter the old normalized `R=1` chart, exactly as the
refuted projective-closure audit observed.  It now enters the independently
supported `R=T=0` corner.  The previous counterexample invalidated the old
dependency union but is not itself a remaining gap.

## Two explicit uncovered pure points

### Free-pivot representative

Keep the full-support normal `[1:1:1]` but take

```text
U0=span(e0,e2).
```

Then

```text
P01=0,                 P02!=0,
T1100=2,               T1101=-2.
```

The last three planes are again the unique embedded triple in `H0`.  Changing
to the `P02` Grassmann pivot also changes the partner of the common coordinate;
transporting the matching back restores the invariant zero `P_cp=0`.

### Normal-mask-6 representative

Take

```text
[C:A:B]=[0:1:1],       U0=span(e0,e1),
```

and the last planes

```text
U1=U2=span(e1,e2-e3),
U3=span(e1,e2+e3).
```

Direct order-four expansion gives the sole nonzero coefficient

```text
T1110=-2.
```

The embedded triple is uniquely `(U1,U2,U3) subset H0`.  The free pivot is
valid, but the normal coefficient at the matching partner is zero.  This is
the exact mask-6/matching obstruction identified by the old independent audit;
the new `r0` results do not change it.

## Evidence boundary

- This note proves a chart-coverage statement, not emptiness on the uncovered
  divisors.
- The endpoint dependency is independently `VERIFIED`; it still does not
  cover the unrelated pivot and orientation strata listed above.
- No finite-field computation or parameter grid contributes evidence.
- No alternative embedded triple exists in either explicit counterexample.
- No component-exhaustiveness, arbitrary-order local-to-global, prize-graph,
  or global Krenn--Gu conclusion is made.

Replay:

```text
uv run --with sympy python derive_p5_h22_embedded_p3_projective_coverage_boundary.py
```

The script rebuilds all normal support masks, the canonical Pluecker chart,
the two pure counterexamples, unique embedded triples, the 24 permutation
invariants, the infinity zero-column identity, and the orientation-endpoint
swap.
