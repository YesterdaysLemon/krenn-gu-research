# Fixed-Q dense directed-spur generic cross-array exclusion

## Status

**Exact characteristic-zero exclusion of a Zariski-open, three-parameter
larger-support root-to-port chart.**  Continue in the dense `K_4/K_4`,
`h!=0` residue of `GLD21`, after the canonical shore normalization used by
`GLD23`.  Keep two root-to-port colour slices equal to `I_4`.  In the third
colour add one directed support edge to the `GLD25` switch:

```text
A^c=I_4+uE_(0,1)+vE_(1,0)+wE_(0,2),    u,v,w!=0.    (1)
```

Sixteen complete ten-vertex coefficient rows have an exact polynomial left
combination whose graph-variable side is zero and whose constant side is

```text
uvw(uv-1)(uv+1)^2(uv-u-v-1)(uv+vw+w+1)^2.           (2)
```

Consequently no hypothetical witness lies outside the four named divisors

```text
uv=1,
uv=-1,
uv-u-v-1=0,
uv+vw+w+1=0.                                         (3)
```

This is deliberately a **generic/open-subset theorem**, not a pointwise
exclusion of the entire directed-spur chart.  The four divisors in (3) are
residual proof obligations, not asserted solution loci.  The boundary
`w=0` is the full two-amplitude chart already excluded by `GLD25`.

The extra edge in (1) changes the support of partial root-to-port permanents,
although it does not by itself create a third full `4 x 4` perfect matching.
The theorem does **not** cover its exceptional divisors, a reverse
`E_(2,0)` edge, further nonzero cross-array entries, root-colour-changing
blocks, either proper-secondary-clique cell, or any weighted-permanent
branch.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

Dependencies:

- [`GLD21`](FIXED_Q_RESPONSE_MAP_ZERO_DEAD_COLOUR_H_GATE_AND_DENSE_COMPANION_ABSORPTION_THEOREM.md)
- [`GLD23`](FIXED_Q_DENSE_COLOUR_DEPENDENT_PRIVATE_PERMUTATION_EXCLUSION_THEOREM.md)
- [`GLD25`](FIXED_Q_DENSE_TWO_AMPLITUDE_SINGLE_SWITCH_CROSS_ARRAY_EXCLUSION_THEOREM.md)

## 1. Canonical dense graph data

Work over a characteristic-zero field `K` with roots
`R={r_0,r_1,r_2,r_3}`, residual pair `Q={q_0,q_1}`, and ports
`U={u_0,u_1,u_2,u_3}`.  Use colours `(c,d,a)=(0,1,2)`, with `a` dead.

Retain the canonical dense data

```text
h=1,
v_i^c=(1,1),    v_i^d=(1,-1),    v_i^a=(0,0),
B_ij=0.                                               (4)
```

Every root-to-port block is colour diagonal:

```text
W_(r_i,u_j)(-,e_s)=A^s_(ij)e_(i,s)^*,               (5)
A^a=A^d=I_4,
A^c=I_4+uE_(0,1)+vE_(1,0)+wE_(0,2).                 (6)
```

Changing the active colour or relabelling the switched indices gives the
corresponding equivalent chart.  The present result assumes this support; it
does not claim that every larger nonprivate array can be normalized to (6).

## 2. Complete coefficient system

Leave free all

```text
24 root--residual entries,
54 root--root entries,
3 pure target coefficients.                          (7)
```

Thus the affine coefficient system has `81` independent unknowns.  For a
port word `omega` and root word `rho`, the complete ten-vertex matching sum
has the same three exhaustive nonzero types as `GLD23`--`GLD25`:

1. `q_0--q_1` and four root--port edges;
2. one residual--root, one residual--port, and three root--port edges;
3. two residual--port, one root--root, and two root--port edges.

The new directed edge contributes to the partial permanents in the last two
types.  Direct port--port edges vanish by (4).  Subtract the corresponding
pure target scalar only on an all-one-colour root/port word.  Write each
complete coefficient equation as

```text
A_(omega,rho)(u,v,w)X=b_(omega,rho)(u,v,w).           (8)
```

All entries lie in `Z[u,v,w]`.

## 3. Exact sixteen-row relation

Set

```text
f = uv-u-v-1,
h_1 = uv+vw+w+1,
j = u^2v^2-2u^2v-2uv^2-uvw-2uv-uw-2u
    -v^2w-3vw-2v-2w-3.                               (9)
```

The following table uses digit words in colour order `(0,1,2)=(c,d,a)`.

| `omega` | `rho` | multiplier |
|---|---|---:|
| `0011` | `0011` | `-uvw(uv-1)(uv+1)h_1j` |
| `0010` | `0010` | `-uvw(uv-1)(uv+1)(u+v+2)h_1^2` |
| `0001` | `0001` | `uvw(uv-1)(uv+1)h_1j` |
| `0011` | `0000` | `uvw(uv-1)(u+v+2)h_1^3` |
| `0000` | `0011` | `-uvw(uv-1)(uv+1)^2j` |
| `0002` | `0002` | `-uvw(uv-1)(uv+1)fh_1^2` |
| `1000` | `1000` | `uvw(u+1)(uv-1)(uv+1)^2h_1^2` |
| `0100` | `1000` | `-uw(u+1)(uv-1)(uv+1)^2h_1^2` |
| `0100` | `0100` | `uvw(v+1)(uv-1)(uv+1)^2h_1^2` |
| `1000` | `0100` | `-vw(v+1)(uv-1)(uv+1)^2h_1^2` |
| `0100` | `0010` | `u(uv-1)(uv+1)^3fh_1` |
| `1100` | `0000` | `-uvw(uv-1)(uv+1)^2h_1^2` |
| `0110` | `0000` | `uvw(uv+1)^2(uv-w-1)fh_1` |
| `0101` | `0000` | `uvw(uv-1)(uv+1)fh_1^2` |
| `1010` | `0000` | `uvw(uv+1)^2(uv+vw-1)fh_1` |
| `1001` | `0000` | `uvw(uv-1)(uv+1)fh_1^2` |

Direct polynomial expansion gives

```text
sum_k lambda_k A_k = 0,
sum_k lambda_k b_k = uvw(uv-1)(uv+1)^2 f h_1^2.      (10)
```

There is no division in (10).  It therefore specializes legally on every
point of the parameter space; it simply ceases to contradict (8) on the
zero locus of its right side.

### Theorem 1 (generic directed-spur exclusion)

Assume `u,v,w!=0` and

```text
(uv-1)(uv+1)(uv-u-v-1)(uv+vw+w+1) != 0.             (11)
```

Then the dense `K_4/K_4`, `h!=0` residue contains no hypothetical witness on
the directed-spur chart (6).

### Proof

Under (11), the right side of (10) is nonzero.  Its left side cancels every
one of the `81` unrestricted graph-side and pure-target coefficients, so the
complete GHZ coefficient equations assert a nonzero scalar is zero.  This is
a contradiction.  `square`

## 4. Exact frontier and scope ledger

```text
GLD21 dense h!=0 companion normal form:                 INPUT;
GLD23 canonical dense shore gauge:                      INPUT;
GLD25 w=0 two-amplitude boundary:                       EMPTY;
active cross slice:                                     I+uE_01+vE_10+wE_02;
support parameters:                                     u,v,w!=0;
generic detector:                                       uvw(uv-1)(uv+1)^2fh_1^2;
complement of four residual divisors:                   EMPTY;
four residual divisors:                                OPEN;
entire directed-spur chart:                            OPEN;
reverse spur and larger-support arrays:                 UNKNOWN;
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
  slice with a two-way `0--1` switch plus the directed edge `0->2`;
- **scope mode:** pointwise on the open set (11), equivalently generic on the
  three-parameter chart;
- **unrestricted data:** all `78` root-side entries and all three pure target
  scalars;
- **excluded object:** one Zariski-open part of a larger-support chart, not
  its four exceptional divisors or the whole nonprivate dense cell;
- **permanent implication:** none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_generic_cross_array_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_dense_directed_spur_generic_cross_array_exclusion.py
```

The primary verifier uses SymPy and independently enumerates all `945`
perfect matchings of the ten vertices.  It reconstructs the sixteen complete
rows directly and checks (10).

The independent audit imports neither SymPy nor the primary.  It implements
`Q[u,v,w]` as sparse dictionaries with exact `Fraction` coefficients and
derives every row from recursive permanents for the three matching types.
Agreement checks both the matching ledger and the factored polynomial
certificate.  The chart hypothesis and the four-divisor boundary remain the
load-bearing written scope.
