# Fixed-Q dense bidirected-spur generic cross-array exclusion

## Status

**Exact characteristic-zero generic/open-subset exclusion on a
four-parameter nonprivate cross-array chart.**  Extend the completed `GLD30`
family by the reverse support edge

```text
A^c=I_4+uE_(0,1)+vE_(1,0)+wE_(0,2)+zE_(2,0),
u,v,w,z!=0.                                          (1)
```

Outside five explicit hypersurfaces, no hypothetical witness lies on this
chart.  This is a generic theorem, not a pointwise completion: every listed
hypersurface remains open, as do further support entries,
root-colour-changing blocks, proper-secondary cells, and every
weighted-permanent bridge.  The `z=0` boundary is empty by `GLD30`.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

Dependency:

- [`GLD30`](FIXED_Q_DENSE_DIRECTED_SPUR_UV_PLUS_VW_PLUS_W_PLUS_ONE_DIVISOR_EXCLUSION_THEOREM.md)

## 1. Complete coefficient system

Use the canonical dense-shore data and colour-diagonal cross-array convention
of `GLD30`.  All `24` root--residual entries, `54` root--root entries, and
three pure target scalars remain independent.  For each port/root word pair
`(omega,rho)`, let

```text
A_(omega,rho)(u,v,w,z)X=b_(omega,rho)(u,v,w,z)       (2)
```

be the complete ten-vertex coefficient equation.  Both verifier routes use
all three exhaustive nonzero matching types; no root-side coefficient is
specialized.

Set

```text
s_- = uv+wz-1,
s_+ = uv+wz+1,
h   = uv+vw+w+1.                                    (3)
```

The fifth polynomial is

```text
p = -u^2v^2z-u^2v^2+u^2vz^2+2u^2vz+u^2v
    -uv^2w+uv^2+4uv wz-uwz^2+uw+uz^2+2uz+u
    +v^2w^2z+v^2w-vw^2z^2+2vw^2z+2vw+v
    -w^2z^2+w^2z+wz^2+w+z+1.                       (4)
```

Spaces in monomials such as `uv wz` in (4) are typographical grouping only;
the replay scripts store the expanded polynomial literally.

## 2. Exact detector

An exact sixteen-row polynomial relation gives

```text
sum lambda_(omega,rho) A_(omega,rho) = 0,

sum lambda_(omega,rho) b_(omega,rho)
  = 2uv wz(uv+1)s_-s_+hp.                           (5)
```

The displayed product `uv wz` means `u*v*w*z`.  The primary verifier stores
all sixteen row keys and polynomial multipliers and reconstructs each row by
direct enumeration of all `945` perfect matchings.  The audit imports the
literal witness table but reconstructs each row independently by recursive
permanents for the three matching types.

Because the field has characteristic zero and (1) assumes `u,v,w,z!=0`,
equation (5) contradicts the complete coefficient system whenever

```text
uv+1 != 0,
uv+wz-1 != 0,
uv+wz+1 != 0,
uv+vw+w+1 != 0,
p != 0.                                             (6)
```

### Theorem 1 (generic bidirected-spur exclusion)

The dense `K_4/K_4`, `h!=0` residue contains no hypothetical witness on the
open subset (1), (6).

### Proof

Apply the exact row relation (5).  Its left side cancels every one of the
`81` independent variables.  Under (1), (6), its right side is nonzero in
characteristic zero, contradicting (2).  `square`

## 3. Exact frontier and scope ledger

```text
GLD30 directed-spur family:                              EMPTY;
added reverse edge zE_(2,0):                             INPUT;
four-parameter detector:              2uv wz(uv+1)s_-s_+hp;
generic complement of five divisors:                     EMPTY;
uv=-1 divisor:                                             OPEN;
uv+wz=1 divisor:                                           OPEN;
uv+wz=-1 divisor:                                          OPEN;
uv+vw+w+1=0 divisor:                                       OPEN;
p=0 divisor:                                               OPEN;
z=0 boundary:                                  CLOSED BY GLD30;
entire bidirected-spur chart:                               OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

Scope:

- **field:** characteristic zero;
- **response hypothesis and normalization:** exactly those of `GLD30`;
- **cross-array subcell:** the open subset (1), (6);
- **unrestricted data:** all `78` root-side entries and three pure target
  scalars;
- **proved object:** a generic/open-subset exclusion, not a pointwise theorem;
- **unproved boundaries:** the complete five-factor exceptional locus,
  additional support entries, reverse orientations beyond (1), and the other
  `GLD21` cells;
- **permanent implication:** none.

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion.py
python claims/arbitrary-order/audit_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_plus_vw_plus_w_plus_one_divisor_exclusion.py
```

The primary derives all rows by direct `945`-matching expansion.  The audit
derives the same sixteen rows through recursive permanents and compares every
expanded coefficient and right-hand side.  Certificate data and SymPy
arithmetic are shared, while the row derivations are separate.  The `GLD30`
replay is the stated `z=0` boundary dependency; it is not reproduced by the
new detector.
