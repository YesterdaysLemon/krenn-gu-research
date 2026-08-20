# Fixed-Q dense bidirected-spur `uv=-1` generic exclusion

## Status

**Exact characteristic-zero generic/open-subset exclusion on one `GLD31`
exceptional divisor.**  On

```text
A^c=I_4+uE_(0,1)+vE_(1,0)+wE_(0,2)+zE_(2,0),
u,v,w,z!=0,    uv=-1,                                (1)
```

no hypothetical witness exists outside four explicit residual surfaces.
This does not close the entire divisor.  The residual surfaces `u=1`,
`z=1`, `z=-1`, and `wz=2` remain open, as do the other four `GLD31`
hypersurfaces and all broader cells.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Dependency:

- [`GLD31`](FIXED_Q_DENSE_BIDIRECTED_SPUR_GENERIC_CROSS_ARRAY_EXCLUSION_THEOREM.md)

## 1. Legal parametrization and complete rows

Because `u!=0`, the divisor has the global parametrization

```text
v=-1/u.                                               (2)
```

Retain all `24` root--residual entries, `54` root--root entries, and three
pure target scalars.  For each port/root word pair `(omega,rho)`, use the
complete ten-vertex coefficient equation

```text
A_(omega,rho)(u,-1/u,w,z)X=b_(omega,rho)(u,-1/u,w,z). (3)
```

## 2. Exact detector

Fourteen exact polynomial-cleared row multipliers cancel all `81` variable
coefficients and leave

```text
-2uwz^2(u-1)(z-1)(z+1)(wz-2).                       (4)
```

The primary reconstructs the selected equations through direct enumeration
of all `945` perfect matchings.  The audit reconstructs them by recursive
permanents and compares every expanded row.

Since the field has characteristic zero and (1) makes `u,w,z` nonzero,
equation (4) is a contradiction whenever

```text
u!=1,    z!=1,    z!=-1,    wz!=2.                  (5)
```

### Theorem 1 (`uv=-1` generic divisor exclusion)

The `GLD31` bidirected-spur chart contains no hypothetical witness on the
open subset (1), (5).

### Proof

Substitute (2) into the complete system (3) and apply the exact fourteen-row
relation.  Its left side is zero.  Under (1), (5), its right side (4) is
nonzero, a contradiction.  `square`

## 3. Frontier and scope

```text
GLD31 exceptional divisor uv=-1:                     INPUT;
fourteen-row detector:       -2uwz^2(u-1)(z-1)(z+1)(wz-2);
generic complement of four surfaces:                 EMPTY;
u=1, z=1, z=-1, wz=2 surfaces:                        OPEN;
entire uv=-1 bidirected-spur divisor:                  OPEN;
other GLD31 divisors:                                  OPEN;
z=0 boundary:                              CLOSED BY GLD27;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

Scope:

- **field:** characteristic zero;
- **response hypothesis and normalization:** exactly those of `GLD31`;
- **cross-array subcell:** the open subset (1), (5);
- **unrestricted data:** all `81` root-side and pure-target variables;
- **proved object:** generic exclusion inside one divisor, not its pointwise
  closure;
- **permanent implication:** none.

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_generic_exclusion.py
python claims/arbitrary-order/audit_fixed_q_dense_bidirected_spur_uv_minus_one_generic_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_minus_one_divisor_exclusion.py
```

The primary reuses the direct `945`-matching row engine of `GLD31`; the audit
reuses its independently derived recursive-permanent engine.  The literal
fourteen-row witness table is new and shared.  The `GLD27` replay checks the
stated `z=0` boundary dependency.
