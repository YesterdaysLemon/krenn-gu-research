# Strict all-center-kernel star `(1,1,1)` obstruction

## Status

**Exact characteristic-zero orientation obstruction.**  A nonzero pure
`P_4` compression cannot have a rank-one exceptional star whose three
relations all point strictly to the pure-kernel endpoint at the center.

This excludes one orientation of the last open all-pair `P_4` cell.  It does
not classify relations pointing to both endpoints, the remaining mixed/
radical support collisions, or the whole star `(1,1,1)` cell.  The
Krenn--Gu conjecture remains **UNRESOLVED**.

## Proof

Choose pure-factor bases `(y_i,x_i)`, with `y_i` the pure-kernel row.  Center
the selected star at mode zero.  A strict arrow to the center has relation

```text
y_0 ell_i=0,                                       (1)
```

where `ell_i` is not the pure-kernel row at leaf `i`.  The degree-one
zero-divisor theorem says `y_0` has support one or two and its annihilator is
a unique line.  Hence all three `ell_i` are proportional to the same polar
form `ell`.  A Borel shift of the active leaf row by its kernel row therefore
normalizes

```text
x_1=x_2=x_3=ell.                                  (2)
```

The active coefficient of the allegedly nonzero pure tensor is now

```text
P_4(x_0,ell,ell,ell).                              (3)
```

But `ell` uses at most two source coordinates.  Its squarefree cube is zero,
so (3) is zero for every center active row `x_0`, a contradiction.

For binary support the exact pair is

```text
y_0=aX_i+bX_j,   ell=aX_i-bX_j;
```

for singleton support both are the same coordinate line.  These are all
possibilities in characteristic zero.

## Replay

```text
uv run --with sympy python claims/p4/classifications/star/all-center-kernel-star-111-obstruction/verify_p4_all_center_kernel_star_111_obstruction.py
uv run --with sympy python claims/p4/classifications/star/all-center-kernel-star-111-obstruction/audit_p4_all_center_kernel_star_111_obstruction.py
```

The primary verifier checks both zero-divisor supports symbolically.  The
independent subset-DP audit applies a source permutation and unequal scales
before checking both cubes.  No finite-field inference is used.
