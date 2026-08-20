# Review: bidirected-spur `uv=-1` generic exclusion

## Verdict

**Accept as an exact characteristic-zero generic exclusion inside one
`GLD31` exceptional divisor.**  It leaves four residual surfaces and does
not claim pointwise divisor closure.  The global conjecture remains
**UNRESOLVED**.

## Load-bearing checks

1. `u!=0` makes the substitution `v=-1/u` legal and global on the divisor.
2. Fourteen complete coefficient rows retain all `81` independent variables.
3. The polynomial-cleared relation leaves exactly
   `-2uwz^2(u-1)(z-1)(z+1)(wz-2)`.
4. Characteristic zero and nonzero `u,w,z` remove only the displayed chart
   factors; `u=1`, `z=1`, `z=-1`, and `wz=2` are explicitly left open.
5. The primary uses direct `945`-matching rows.  The audit uses recursive
   permanents and compares all fourteen expanded rows; the witness table and
   SymPy arithmetic are shared.
6. At `z=0`, this divisor is exactly within the proved `GLD27` `uv=-1`
   directed-spur boundary.  That does not close any `z!=0` residual surface.

## Replay

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_generic_exclusion.py
python claims/arbitrary-order/audit_fixed_q_dense_bidirected_spur_uv_minus_one_generic_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_minus_one_divisor_exclusion.py
```
