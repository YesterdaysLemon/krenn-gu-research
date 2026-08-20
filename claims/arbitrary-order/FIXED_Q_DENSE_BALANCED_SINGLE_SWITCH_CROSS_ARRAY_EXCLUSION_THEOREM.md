# Fixed-Q dense balanced single-switch cross-array exclusion

## Status

**Exact characteristic-zero exclusion of a genuinely nonprivate
root-to-port chart.**  Continue in the dense `K_4/K_4`, `h!=0` residue of
`GLD21`, after the canonical shore normalization used by `GLD23`.  Keep the
dead and one active root-to-port colour slices private identity arrays.  In
the other active colour replace one private `2 x 2` block by

```text
[1  1]
[t  1],                    t!=0,                     (1)
```

and retain private identity entries at the other two ports.

No hypothetical witness lies on this balanced single-switch chart.  Eighteen
complete ten-vertex coefficient equations have an exact polynomial left
combination whose graph-variable side is zero and whose constant side is

```text
-4t(t+1).                                             (2)
```

This excludes every `t!=0,-1`.  At the only exceptional value `t=-1`, a
different ten-equation rational combination gives `0=1`.

The chart is genuinely outside `GLD23`: for `t!=0` the switched colour has
two nonzero entries in each of two rows and columns and supports the identity
and transposition matchings.  The theorem does **not** cover an arbitrary
`2 x 2` block with two independent normalized off-diagonal amplitudes, a
larger nonprivate cross array, either proper-secondary-clique cell, or any
weighted-permanent branch.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Dependencies:

- [`GLD21`](FIXED_Q_RESPONSE_MAP_ZERO_DEAD_COLOUR_H_GATE_AND_DENSE_COMPANION_ABSORPTION_THEOREM.md)
- [`GLD23`](FIXED_Q_DENSE_COLOUR_DEPENDENT_PRIVATE_PERMUTATION_EXCLUSION_THEOREM.md)

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
array; it does not assert that every nonprivate array can be put in this form.

### Definition 1 (balanced single switch)

Every root-to-port block is colour diagonal:

```text
W_(r_i,u_j)(-,e_s)=A^s_(ij) e_(i,s)^*.               (4)
```

The three normalized matrices are

```text
A^a=I_4,
A^d=I_4,
A^c=I_4+E_(0,1)+t E_(1,0),    t in K^*.              (5)
```

Changing the switched active colour or the two switched indices gives an
equivalent chart after the corresponding colour/index relabelling.  The word
`balanced` records the load-bearing normalization of the diagonal entries
and the `E_(0,1)` amplitude to one.  A general two-amplitude switch is not
claimed.

## 2. Complete coefficient rows

Leave every remaining root-side coefficient free:

```text
p_(epsilon,r,s)=W_(r,q_epsilon)(e_(r,s),z_(q_epsilon))
    for 2*4*3=24 entries,
w_(ij,st)=W_(r_i,r_j)(e_(i,s),e_(j,t))
    for 6*3*3=54 entries.                             (6)
```

Also allow three arbitrary pure target coefficients `alpha_c,alpha_d,alpha_a`.
Thus the affine coefficient system has `81` unknowns.  This is conservative:
no hidden equality among root--residual or root--root block entries is used.

For a port word `omega` and root word `rho`, the complete ten-vertex matching
sum has the same three exhaustive types as `GLD23`:

1. `q_0--q_1` and four root--port edges;
2. one residual--root, one residual--port, and three root--port edges;
3. two residual--port, one root--root, and two root--port edges.

The cross entries in (5) merely add additional matchings inside these three
types.  A direct port--port edge is zero by (3).  Subtract `alpha_s` only on
the all-`s` root/port word.

Write the resulting equation as

```text
A_(omega,rho)(t) X = b_(omega,rho)(t).                (7)
```

All entries lie in `Z[t]` and have degree at most one before rows are
combined.

## 3. Generic eighteen-row certificate

The following table uses digit words in the order `(0,1,2)=(c,d,a)`.  Its
multiplier column gives a polynomial `lambda_j(t)`.

| `omega` | `rho` | `lambda_j(t)` |
|---|---|---:|
| `1100` | `0000` | `-2t(t+1)` |
| `1000` | `1000` | `4t(t+1)` |
| `0100` | `1000` | `-4(t+1)` |
| `0200` | `0200` | `2t(t+1)^2` |
| `0020` | `0020` | `4t` |
| `0002` | `0002` | `4t` |
| `0110` | `0000` | `-4(t+1)` |
| `0101` | `0000` | `-4(t+1)` |
| `0110` | `0110` | `2(t^2-1)` |
| `0100` | `0100` | `-4(t^2-1)` |
| `0010` | `0010` | `-2(t^2+4t+1)` |
| `0000` | `0110` | `t^2-1` |
| `0101` | `0101` | `2(t^2-1)` |
| `0001` | `0001` | `-2(t^2+4t+1)` |
| `0000` | `0101` | `t^2-1` |
| `0011` | `0000` | `2(t^2+t+2)` |
| `0011` | `0011` | `2(t+1)(t+2)` |
| `0000` | `0011` | `2(t+1)(t+2)` |

Exact expansion gives the polynomial identities

```text
sum_j lambda_j(t) A_j(t)=0,
sum_j lambda_j(t) b_j(t)=-4t(t+1).                   (8)
```

No division occurs in (8), so the identity specializes legally at every
`t`, including `t=-2`.  For `t!=0,-1`, equations (7)--(8) are inconsistent.

## 4. The `t=-1` fibre

At `t=-1`, use the ten rows

```text
(1100,0000), (1000,1000), (0100,1000), (0100,0100),
(0120,0120), (0102,0102), (0110,0000), (0101,0000),
(0111,0100), (0011,0011)                            (9)
```

with respective multipliers

```text
(1/2,-1,-1,2,-1,-1,-1,-1,1,1/2).                  (10)
```

Direct exact expansion gives

```text
sum_j lambda_j A_j(-1)=0,
sum_j lambda_j b_j(-1)=1.                           (11)
```

Thus the exceptional fibre also asserts `0=1`.  Notice that
`per([[1,1],[-1,1]])=0`; the special certificate does not assume a nonzero
pure switched-colour root-to-port permanent.

### Theorem 2 (balanced single-switch exclusion)

The dense `K_4/K_4`, `h!=0` residue contains no hypothetical witness on the
balanced single-switch chart of Definition 1.

### Proof

Let `t!=0`.  If `t!=-1`, apply (8); its right side is nonzero in
characteristic zero.  If `t=-1`, apply (11).  In both cases the complete GHZ
coefficient identities give a contradiction.  `square`

## 5. Exact frontier and scope ledger

```text
GLD21 dense h!=0 companion normal form:                 INPUT;
GLD23 canonical dense shore gauge:                      INPUT;
dead and one active cross slices:                       PRIVATE IDENTITY;
other active cross slice:                               I+E_01+tE_10;
nonprivate switch parameter:                            t!=0;
generic polynomial detector:                            -4t(t+1);
exceptional t=-1 fibre:                                 0=1;
balanced single-switch chart:                           EMPTY;
two-independent-amplitude switch:                       UNKNOWN;
general nonprivate root-to-port arrays:                  UNKNOWN;
proper-secondary-clique h!=0 cells:                     UNKNOWN;
weighted permanent implication:                         UNKNOWN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

Scope:

- **field:** characteristic zero;
- **response hypothesis:** the dense `K_4/K_4` literal all-seven
  response-map-zero cell of `GLD21`;
- **normalization:** the exact dense shore gauge of `GLD23`;
- **cross-array subcell:** two identity colour slices and one balanced
  single `2 x 2` switch with both off-diagonal entries nonzero;
- **unrestricted data:** all `78` root-side entries and all three pure target
  scalars;
- **excluded object:** one positive-dimensional genuinely nonprivate chart,
  not the whole nonprivate dense cell;
- **permanent implication:** none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_balanced_single_switch_cross_array_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_dense_balanced_single_switch_cross_array_exclusion.py
```

The primary verifier uses SymPy and a separately enumerated list of all `945`
perfect matchings.  It reconstructs the `28` selected rows directly from the
ten-vertex graph and checks both polynomial left identities.

The independent audit imports neither SymPy nor the primary.  It implements
`Q[t]` as tuples of exact `Fraction` coefficients, derives the rows from the
three matching types and recursive permanents, and separately checks (8) and
(11).  The finite coefficient arithmetic is proof-producing.  The chart
normalization and its precise boundary remain the load-bearing written
hypothesis.
