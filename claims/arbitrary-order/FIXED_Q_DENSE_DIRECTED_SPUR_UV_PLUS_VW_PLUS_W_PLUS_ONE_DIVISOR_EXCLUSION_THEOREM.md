# Fixed-Q dense directed-spur `uv+vw+w+1=0` divisor exclusion

## Status

**Exact characteristic-zero pointwise exclusion of the final exceptional
divisor left by `GLD26`, completing its directed-spur chart.**  On

```text
A^c=I_4+uE_(0,1)+vE_(1,0)+wE_(0,2),    u,v,w!=0,    (1)
```

impose `uv+vw+w+1=0`.  No hypothetical witness lies on this divisor.
Together with `GLD26`--`GLD29`, this proves the whole nonzero chart (1)
empty.  The `w=0` boundary is already empty by `GLD25`.

This is not a coordinate-free nonprivate theorem.  The reverse spur, further
support entries, root-colour-changing blocks, proper-secondary cells, and
every weighted-permanent bridge remain open.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Dependencies:

- [`GLD25`](FIXED_Q_DENSE_TWO_AMPLITUDE_SINGLE_SWITCH_CROSS_ARRAY_EXCLUSION_THEOREM.md)
- [`GLD26`](FIXED_Q_DENSE_DIRECTED_SPUR_GENERIC_CROSS_ARRAY_EXCLUSION_THEOREM.md)
- [`GLD27`](FIXED_Q_DENSE_DIRECTED_SPUR_UV_MINUS_ONE_DIVISOR_EXCLUSION_THEOREM.md)
- [`GLD28`](FIXED_Q_DENSE_DIRECTED_SPUR_UV_ONE_DIVISOR_EXCLUSION_THEOREM.md)
- [`GLD29`](FIXED_Q_DENSE_DIRECTED_SPUR_UV_MINUS_U_MINUS_V_MINUS_ONE_DIVISOR_EXCLUSION_THEOREM.md)

## 1. Complete coefficient rows and legal chart

Use the canonical dense-shore data and colour-diagonal cross-array convention
of `GLD26`.  All `24` root--residual entries, `54` root--root entries, and
three pure target scalars remain independent.  For every port/root word pair
`(omega,rho)`, let

```text
A_(omega,rho)(u,v,w)X=b_(omega,rho)(u,v,w)           (2)
```

be the complete ten-vertex coefficient equation, including all three
exhaustive nonzero matching types.

Set

```text
H=uv+vw+w+1,       F=uv-u-v-1,
q_a=u^2+1,         q_b=u^2-2u-1.                    (3)
```

If `v=-1`, then `H=1-u`, so `H=0` forces `u=1` and hence `uv=-1`.
That complete line is empty by `GLD27`.  On the remaining open chart
`v!=-1`, solve legally

```text
w=-(uv+1)/(v+1).                                   (4)
```

## 2. Divisor detector and exhaustive curve cover

After (4), an exact sixteen-row relation cancels all `81` variable
coefficients and leaves

```text
-uv(u-1)(u+v)(uv+1)(uv-2v-1).                      (5)
```

The chart assumptions remove `u=0` and `v=0`.  The complete residual locus
of (5) is therefore

```text
C_0: uv=-1,
C_1: u=1,
C_2: u+v=0,
C_3: uv-2v-1=0.                                    (6)
```

The first component is empty by `GLD27`.  The other three have exact curve
certificates below.

## 3. The `u=1` curve

Equations (4) and `u=1` give `w=-1`.  A fourteen-row relation leaves

```text
-2v(v-1)(v+1).                                     (7)
```

Here `v=0` is excluded by the chart, `v=-1` lies on `GLD27`, and `v=1`
lies on the proved `GLD28` divisor `uv=1`.  Thus `C_1` is empty.

## 4. The `u+v=0` curve

On the open chart `v!=-1`, write

```text
v=-u,       w=-u-1.                                (8)
```

A fifteen-row relation leaves

```text
-u(u-1)(u+1)(u^2+1)^2.                             (9)
```

The factor `u=0` is excluded.  At `u=1`, one has `uv=-1`, hence `GLD27`.
At `u=-1`, equation (8) gives the excluded boundary `w=0`.  Finally,
`u^2+1=0` gives `uv=-u^2=1`, hence `GLD28`.  Thus `C_2` is empty.

## 5. The `uv-2v-1=0` curve

The equation is impossible at `u=2`; otherwise it gives

```text
v=1/(u-2),       w=-2.                             (10)
```

A fifteen-row relation leaves

```text
2u(u-1)q_b.                                        (11)
```

Again `u=0` is excluded.  At `u=1`, equation (10) gives `v=-1`, hence
`GLD27`.  For the last factor,

```text
F |_(10) = -q_b/(u-2),                             (12)
```

so `q_b=0` lies exactly on the proved `GLD29` divisor `F=0`.  Thus `C_3`
is empty.

### Theorem 1 (final divisor exclusion)

The dense `K_4/K_4`, `h!=0` residue contains no hypothetical witness on
the chart (1) with `uv+vw+w+1=0`.

### Proof

The `v=-1` fibre is contained in `GLD27`.  On `v!=-1`, relation (5) reduces
the divisor exhaustively to (6).  `GLD27` closes `C_0`; relations (7), (9),
and (11), with the exact overlaps identified above, reduce `C_1,C_2,C_3`
to the proved scopes of `GLD27`, `GLD28`, and `GLD29` or to excluded chart
boundaries.  Hence the complete divisor is empty.  `square`

### Corollary 2 (directed-spur chart completion)

For `u,v!=0`, the full family

```text
I_4+uE_(0,1)+vE_(1,0)+wE_(0,2)
```

is empty for every `w`: `GLD25` handles `w=0`; `GLD26` handles the
complement of its four exceptional divisors for `w!=0`; and
`GLD27`--`GLD30` handle those four divisors pointwise.

## 6. Exact frontier and scope ledger

```text
GLD26 directed-spur chart:                              INPUT;
final exceptional divisor:                    uv+vw+w+1=0;
divisor detector: -uv(u-1)(u+v)(uv+1)(uv-2v-1);
three new residual curves:                         EXHAUSTED;
dependency residuals:                CLOSED BY GLD27--GLD29;
entire final divisor:                                  EMPTY;
entire nonzero directed-spur chart:                    EMPTY;
w=0 boundary:                             CLOSED BY GLD25;
reverse / broader support charts:                       OPEN;
global Krenn--Gu conjecture:                      UNRESOLVED.
```

Scope:

- **field:** characteristic zero;
- **response hypothesis and normalization:** exactly those of `GLD26`;
- **cross-array subcell:** the full `uv+vw+w+1=0`, `u,v,w!=0` divisor;
- **unrestricted data:** all `78` root-side entries and three pure target
  scalars;
- **excluded object:** the last divisor and, by the cited dependencies, this
  complete directed-spur coordinate family;
- **not excluded:** reverse or larger spurs, other nonprivate cross arrays,
  proper-secondary cells, or the remaining `GLD21` branches;
- **permanent implication:** none.

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_plus_vw_plus_w_plus_one_divisor_exclusion.py
python claims/arbitrary-order/audit_fixed_q_dense_directed_spur_uv_plus_vw_plus_w_plus_one_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_generic_cross_array_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_minus_one_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_one_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_minus_u_minus_v_minus_one_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_amplitude_single_switch_cross_array_exclusion.py
```

The primary reconstructs every selected row by directly enumerating all
`945` ten-vertex perfect matchings.  The audit reconstructs the same `19`
distinct rows through recursive permanents for the three exhaustive matching
types and compares their expanded coefficients.  The audit imports the
literal certificate tables from the primary module, so witness data and
SymPy arithmetic are shared; row derivation and implementation route are
separate.  `GLD25`--`GLD29` are theorem dependencies, not silently reproduced
by the two new scripts.
