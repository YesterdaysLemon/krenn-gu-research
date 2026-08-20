# Fixed-Q dense two-amplitude single-switch cross-array exclusion

## Status

**Exact characteristic-zero exclusion of the full two-independent-
off-diagonal-amplitude `2 x 2` switch chart.**  Continue in the dense
`K_4/K_4`, `h!=0` residue of `GLD21`, after the canonical shore normalization
used by `GLD23`.  Keep the dead and one active root-to-port colour slices
equal to `I_4`.  In the other active colour use

```text
A^c=I_4+u E_(0,1)+v E_(1,0),    u,v!=0.             (1)
```

No hypothetical witness lies on this chart.  A generic exact left relation
among eighteen complete ten-vertex coefficient rows cancels all `81`
root-side and pure-target variables and leaves

```text
2uv(u+1)(uv+1)(uv-u-v-1).                            (2)
```

Three divisor certificates and two residual zero-dimensional certificates
close the entire vanishing locus of (2).  In particular, the proof does not
divide by either off-diagonal amplitude or discard any exceptional fibre.

This theorem strictly extends `GLD24`, which is the slice `u=1`, `v=t`.
It does **not** cover a general nonprivate `4 x 4` colour slice with further
nonzero entries, a root-to-port edge that changes root colour, either
proper-secondary-clique cell, or any weighted-permanent branch.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

Dependencies:

- [`GLD21`](FIXED_Q_RESPONSE_MAP_ZERO_DEAD_COLOUR_H_GATE_AND_DENSE_COMPANION_ABSORPTION_THEOREM.md)
- [`GLD23`](FIXED_Q_DENSE_COLOUR_DEPENDENT_PRIVATE_PERMUTATION_EXCLUSION_THEOREM.md)
- [`GLD24`](FIXED_Q_DENSE_BALANCED_SINGLE_SWITCH_CROSS_ARRAY_EXCLUSION_THEOREM.md)

## 1. Canonical dense graph data

Work over a characteristic-zero field `K` with roots
`R={r_0,r_1,r_2,r_3}`, residual pair `Q={q_0,q_1}`, and ports
`U={u_0,u_1,u_2,u_3}`.  Use colours `(c,d,a)=(0,1,2)`, with `a` dead.

Retain the `GLD23` canonical dense data

```text
h=1,
v_i^c=(1,1),    v_i^d=(1,-1),    v_i^a=(0,0),
B_ij=0.                                               (3)
```

As in `GLD23`, reaching (3) from arbitrary dense shores uses only invertible
coordinate changes after a harmless algebraic scalar extension.  The present
theorem makes an additional chart assumption on the normalized root-to-port
array; it does not assert that every nonprivate array has this support.

### Definition 1 (two-amplitude single switch)

Every root-to-port block is colour diagonal:

```text
W_(r_i,u_j)(-,e_s)=A^s_(ij) e_(i,s)^*.               (4)
```

The normalized matrices are

```text
A^a=I_4,
A^d=I_4,
A^c=I_4+u E_(0,1)+v E_(1,0),    u,v in K^*.          (5)
```

Changing the switched active colour or the two switched indices gives an
equivalent chart after the corresponding colour/index relabelling.  Both
off-diagonal amplitudes are independent.  The four diagonal entries remain
fixed by the chart normalization, so (5) is not a claim about an arbitrary
`2 x 2` block with independently varying diagonal entries.

## 2. Complete coefficient rows

Leave every remaining root-side coefficient free:

```text
p_(epsilon,r,s)=W_(r,q_epsilon)(e_(r,s),z_(q_epsilon))
    for 2*4*3=24 entries,
w_(ij,st)=W_(r_i,r_j)(e_(i,s),e_(j,t))
    for 6*3*3=54 entries.                             (6)
```

Also allow three arbitrary pure target coefficients
`alpha_c,alpha_d,alpha_a`.  Thus the affine coefficient system has `81`
unknowns.  No equality among root--residual or root--root block entries is
used.

For a port word `omega` and root word `rho`, the complete ten-vertex matching
sum has the same three exhaustive nonzero types as `GLD23` and `GLD24`:

1. `q_0--q_1` and four root--port edges;
2. one residual--root, one residual--port, and three root--port edges;
3. two residual--port, one root--root, and two root--port edges.

The two cross entries in (5) add matchings inside these types.  Direct
port--port edges vanish by (3).  Subtract `alpha_s` only on the all-`s`
root/port word.  Write the resulting equation as

```text
A_(omega,rho)(u,v) X = b_(omega,rho)(u,v).            (7)
```

All entries lie in `Z[u,v]`.

For the certificate tables below set

```text
f = uv-u-v-1,
q = u^2+2u-1,
g = u^2v^2-3u^2v-3uv^2-4uv-u-v-1.                  (8)
```

Digit words use the colour order `(0,1,2)=(c,d,a)`.

## 3. Generic eighteen-row certificate

| `omega` | `rho` | multiplier |
|---|---|---:|
| `1100` | `0000` | `-2uv(u+1)(uv+1)` |
| `1000` | `1000` | `2uv(u+1)^2(uv+1)` |
| `0100` | `1000` | `-2u(u+1)^2(uv+1)` |
| `0200` | `0200` | `2uv(u+1)(v+1)(uv+1)` |
| `0020` | `0020` | `-2uv(u+1)f` |
| `0002` | `0002` | `-2uv(u+1)f` |
| `0110` | `0000` | `(u+1)^2(uv+1)f` |
| `0101` | `0000` | `(u+1)^2(uv+1)f` |
| `0110` | `0110` | `-(u+1)(uv-1)(uv+1)f` |
| `0100` | `0100` | `2(u+1)(uv-1)(uv+1)f` |
| `0010` | `0010` | `(u+1)g` |
| `0000` | `0110` | `-(uv-1)(uv+1)f` |
| `0101` | `0101` | `-(u+1)(uv-1)(uv+1)f` |
| `0001` | `0001` | `(u+1)g` |
| `0000` | `0101` | `-(uv-1)(uv+1)f` |
| `0011` | `0000` | `2(u+1)(u^2v^2+u+v+1)` |
| `0011` | `0011` | `2(u+1)(uv+1)(u+v+1)` |
| `0000` | `0011` | `2(u+1)(uv+1)(u+v+1)` |

Exact expansion gives

```text
sum_j lambda_j A_j = 0,
sum_j lambda_j b_j = 2uv(u+1)(uv+1)f.                (9)
```

Since `u,v!=0`, this excludes the complement of the three divisors

```text
D_1: u=-1,    D_2: uv=-1,    D_3: f=0.              (10)
```

## 4. The three exceptional divisors

### 4.1 The divisor `u=-1`

After setting `u=-1`, use the following twelve rows.

| `omega` | `rho` | multiplier |
|---|---|---:|
| `1100` | `0000` | `v-1` |
| `0200` | `0200` | `-(v-1)(v+1)` |
| `0020` | `0020` | `v-1` |
| `0002` | `0002` | `v-1` |
| `0100` | `0100` | `2(v-1)(v+1)` |
| `0120` | `0120` | `-(v-1)(v+1)` |
| `0102` | `0102` | `-(v-1)(v+1)` |
| `0011` | `0000` | `-v-1` |
| `0011` | `0011` | `v-1` |
| `0010` | `0010` | `1-v` |
| `0001` | `0001` | `1-v` |
| `0000` | `0011` | `v-1` |

Their graph-variable side is zero and their constant side is

```text
2v(v-1).                                               (11)
```

Because `v!=0`, only the point `(-1,1)` remains on `D_1`.

### 4.2 The divisor `uv=-1`

Here `u!=0`, so substitute `v=-u^(-1)`.  The following polynomial-cleared
thirteen-row relation is exact in `K[u,u^(-1)]`.

| `omega` | `rho` | multiplier |
|---|---|---:|
| `1100` | `0000` | `2u` |
| `1000` | `1000` | `-2u(u+1)` |
| `0100` | `1000` | `-2u^2(u+1)` |
| `0200` | `0200` | `-2(u-1)` |
| `0100` | `0100` | `4q` |
| `0120` | `0120` | `-2q` |
| `0102` | `0102` | `-2q` |
| `0010` | `0010` | `-(u^2-1)` |
| `0001` | `0001` | `-(u^2-1)` |
| `0110` | `0000` | `-(u+1)q` |
| `0101` | `0000` | `-(u+1)q` |
| `0111` | `0100` | `2q` |
| `0011` | `0011` | `2(u^2+u-1)` |

It leaves

```text
2q = 2(u^2+2u-1).                                     (12)
```

Thus only the quadratic locus `q=0` remains on `D_2`.

### 4.3 The divisor `f=0`

The equation `f=0` gives

```text
v=(u+1)/(u-1).                                        (13)
```

The denominator is legal: `f(1,v)=-2`.  After this substitution, use the
following eighteen rows.

| `omega` | `rho` | multiplier |
|---|---|---:|
| `1100` | `1100` | `2u(u+1)^2q` |
| `0100` | `1000` | `-2u(u+1)q(u-1)` |
| `0200` | `0200` | `2u(u+1)^2q` |
| `0100` | `0100` | `-2(u+1)q(2u^2+u+1)` |
| `0020` | `0020` | `2u(u+1)^2(u-1)` |
| `0002` | `0002` | `2u(u+1)^2(u-1)` |
| `0000` | `1100` | `2u(u+1)^2q` |
| `0110` | `0000` | `-(u+1)^2q(u-1)` |
| `0101` | `0000` | `-(u+1)^2q(u-1)` |
| `0110` | `0110` | `(u+1)(u^2+1)q` |
| `0010` | `0010` | `-(u+1)(3u^2+4u-1)(u-1)` |
| `0000` | `0110` | `(u^2+1)q` |
| `0101` | `0101` | `(u+1)(u^2+1)q` |
| `0001` | `0001` | `-(u+1)(3u^2+4u-1)(u-1)` |
| `0000` | `0101` | `(u^2+1)q` |
| `0011` | `0000` | `2(u+1)(u-1)^2` |
| `0011` | `0011` | `2(u+1)q(u-1)` |
| `0000` | `0011` | `2(u+1)q(u-1)` |

The exact rational identity cancels the graph-variable side and leaves

```text
-2u(u+1)^2q.                                          (14)
```

On the permitted chart `u!=0`.  If `u=-1`, then `f=-2v`, contradicting
`v!=0`.  Therefore (14) closes `D_3` away from `q=0`.  Moreover, on `f=q=0`,

```text
uv+1 = q/(u-1) = 0,                                   (15)
```

so the residual quadratic points already lie on `D_2`.

## 5. Residual zero-dimensional certificates

### 5.1 The point `(u,v)=(-1,1)`

Use the rows

```text
(1100,0000), (0200,0200), (0100,0100), (0120,0120),
(0102,0102), (0111,0100), (0011,0011)                (16)
```

with respective multipliers

```text
(1/2,-1,2,-1,-1,1,1/2).                              (17)
```

Direct exact expansion gives `0=1`.

### 5.2 The quadratic locus `q=0`, `uv=-1`

When `q=0`, division by nonzero `u` gives `v=-u^(-1)=-u-2`.  Work in the
quadratic quotient `K[u]/(q)` and use the rows

```text
(1100,1100), (0100,1000), (0200,0200), (0100,0100),
(0120,0120), (0102,0102), (0000,1100), (0010,0010),
(0001,0001), (0110,0000), (0101,0000), (0111,0100),
(0011,0011)                                           (18)
```

with respective multipliers

```text
(-1,-u,-1,3,-1,-1,-1,-1/2,-1/2,
 -(u+1)/2,-(u+1)/2,1,1).                             (19)
```

Reduction modulo `q` cancels all `81` variable coefficients and leaves
`1`.  Hence both quadratic conjugate points are impossible whenever they
exist over `K`; no algebraic-closure or rational-root assumption is used.

### Theorem 2 (two-amplitude single-switch exclusion)

The dense `K_4/K_4`, `h!=0` residue contains no hypothetical witness on the
two-amplitude single-switch chart of Definition 1.

### Proof

Let `u,v!=0`.  If all three factors in (10) are nonzero, use (9).  If
`u=-1`, use (11) unless `v=1`, when (16)--(17) applies.  Otherwise, if
`uv=-1`, use (12) unless `q=0`, when (18)--(19) applies.  In the remaining
case `f=0`, equations (14)--(15) give a contradiction.  These cases exhaust
the vanishing locus of (2), so every point of the chart is inconsistent with
the complete GHZ coefficient identities.  `square`

## 6. Exact frontier and scope ledger

```text
GLD21 dense h!=0 companion normal form:                 INPUT;
GLD23 canonical dense shore gauge:                      INPUT;
dead and one active cross slices:                       PRIVATE IDENTITY;
other active cross slice:                               I+uE_01+vE_10;
two independent off-diagonal parameters:                u,v!=0;
generic detector:                                       2uv(u+1)(uv+1)f;
exceptional divisors:                                   u=-1, uv=-1, f=0;
residual point and quadratic locus:                     BOTH EXACTLY CLOSED;
full two-amplitude single-switch chart:                 EMPTY;
larger-support nonprivate root-to-port arrays:           UNKNOWN;
root-colour-changing cross blocks:                      UNKNOWN;
proper-secondary-clique h!=0 cells:                     UNKNOWN;
weighted permanent implication:                         UNKNOWN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

Scope:

- **field:** characteristic zero;
- **response hypothesis:** the dense `K_4/K_4` literal all-seven
  response-map-zero cell of `GLD21`;
- **normalization:** the exact dense shore gauge of `GLD23`;
- **cross-array subcell:** two identity colour slices and one colour-diagonal
  `2 x 2` switch with independent nonzero off-diagonal amplitudes;
- **unrestricted data:** all `78` root-side entries and all three pure target
  scalars;
- **excluded object:** one two-dimensional genuinely nonprivate chart, not
  the whole nonprivate dense cell;
- **permanent implication:** none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_amplitude_single_switch_cross_array_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_dense_two_amplitude_single_switch_cross_array_exclusion.py
```

The primary verifier uses SymPy and independently enumerates all `945`
perfect matchings of the ten vertices.  It reconstructs every selected row
directly from the graph and checks the generic, three divisor, point, and
quadratic-quotient certificates.

The independent audit imports neither SymPy nor the primary.  It implements
`Q[u,v]` as sparse dictionaries with exact `Fraction` coefficients, derives
the rows from the three matching types and recursive permanents, and checks
the divisor substitutions in separate univariate and quotient arithmetic.
The finite coefficient arithmetic is proof-producing.  The chart
normalization and its precise boundary remain the load-bearing written
hypothesis.
