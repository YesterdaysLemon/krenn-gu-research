# Complete exclusion of two-level physical P7 stars

## Status

**Exact characteristic-zero orbit closure.**  Let the seven star coefficients
of a putative physical P7 extension take at most two nonzero values.  Up to a
leaf permutation and interchange of the values, their multiplicities are

```text
1+6, 2+5, or 3+4.                                    (1)
```

The preceding mixed-Hard-Lefschetz theorem excludes `1+6`.  This note closes
`2+5` and `3+4` symbolically.  The `2+5` weighted-Kneser kernel is supported
in modules which omit the unique same-side edge.  The `3+4` pencil has one
additional block-constant cubic wall carrying a full-edge mixed kernel, but
that kernel violates an exact primitive five-set equation.  Therefore no
physical full-edge P7 extension has a nonzero star with at most two distinct
coordinate values.

This is not a construction or a global P7 exclusion.  Stars with at least
three distinct values, the general exceptional-divisor system, the full P7
extension incidence, and global Krenn--Gu remain **UNKNOWN/UNRESOLVED**.

## 1. The two-block edge decomposition

Put value `p` on a set `A` of size `m`, value `q` on a set `B` of size
`n=7-m`, and assume `pq!=0`.  Write `u,v,w` for constant edge values on
`AA,AB,BB`.  The local Boolean-down pencil from
`P7_PHYSICAL_MIXED_KERNEL_BOOLEAN_DOWN_DESCENT_AND_SEVEN_BY_SEVEN_MASTER_HESSIAN.md`
is

```text
(L_A f)_ij=delta_ij f_ij+a_i r_j+a_j r_i,
delta_ij=alpha-2(a_i+a_j).                           (2)
```

The edge permutation module under `S_m x S_n` splits into block-constant,
standard, tensor-standard, and harmonic two-subset summands.  On the three
row-sum-free summands, `L_A` is scalar:

```text
AA harmonic:        delta_AA=(m-4)p+nq;
AB tensor-standard: delta_AB=(m-2)p+(n-2)q;
BB harmonic:        delta_BB=mp+(n-4)q.              (3)
```

For one sum-zero coordinate vector on `A`, the paired `AA/AB` standard block
is

```text
K_A = [ 2(m-3)p+nq,       pn                 ]
      [ (m-2)q,           (m-2)p+2(n-1)q    ].       (4)
```

For one sum-zero coordinate vector on `B`, the paired `AB/BB` standard block
is

```text
K_B = [ 2(m-1)p+(n-2)q,   p(n-2)             ]
      [ mq,                mp+2(n-3)q         ].      (5)
```

When one of the two-set modules is too small, the identically zero standard
column is omitted.  Finally, on type-constant edge values `(u,v,w)`, the
quotient block is

```text
C_mn = [ 3(m-2)p+nq,                    2pn, 0       ]
       [ (m-1)q, 2((m-1)p+(n-1)q), (n-1)p           ]
       [ 0,                              2mq,
                                      mp+3(n-2)q    ]. (6)
```

Equations (3)--(6) are obtained directly from (2).  The replay constructs an
explicit 21-vector equivariant basis, proves it is invertible, and verifies
`L_A C=C K` symbolically.  Thus the factorization below is a representation-
theoretic determinant, not a parameter or graph enumeration.

## 2. The `2+5` orbit has no full-edge mixed kernel

For `(m,n)=(2,5)`, the summands have dimensions

```text
AB tensor 4; A-standard 1; BB harmonic 5;
B-standard pair 2*4; block-constant 3.               (7)
```

Their nontrivial blocks satisfy

```text
AB tensor eigenvalue =3q,
A-standard eigenvalue=8q,
BB harmonic eigenvalue=2p+q,

det K_B=4(p^2+2pq+3q^2),
det C_25=360q^3.                                     (8)
```

Consequently

```text
det L_A =5*2^14*3^6 q^8 (2p+q)^5
          (p^2+2pq+3q^2)^4,                         (9)

det M_A =5*2^30*3^12 q^8 (2p+q)^5
          (p^2+2pq+3q^2)^4.                         (10)
```

The fixed factor between (9) and (10) is `det J=2^16*3^6`.
If `2p+q=0`, the kernel is the `BB` harmonic module, so every `AA` and `AB`
coordinate is zero.  If `p^2+2pq+3q^2=0`, the kernel is `B`-standard and
has every `AA` coordinate zero.  These two walls do not meet for `q!=0`.
All other blocks are invertible.  Thus no singular `2+5` pencil contains a
full-edge vector, over any characteristic-zero field.

## 3. The `3+4` mixed-kernel cubic

For `(m,n)=(3,4)`, the dimensions are

```text
AB tensor 6; BB harmonic 2; A-standard pair 2*2;
B-standard pair 2*3; block-constant 3.               (11)
```

Here

```text
det K_A=24q^2,
det K_B=4(3p^2+2pq+q^2),
det C_34=36(p^3+2p^2q+3pq^2+4q^3).                  (12)
```

It follows that

```text
det L_A =2^14*3^6 p^2 q^4 (p+2q)^6
          (3p^2+2pq+q^2)^3
          (p^3+2p^2q+3pq^2+4q^3),                  (13)

det M_A =2^30*3^12 p^2 q^4 (p+2q)^6
          (3p^2+2pq+q^2)^3
          (p^3+2p^2q+3pq^2+4q^3).                  (14)
```

The wall `p+2q=0` is tensor-standard and has only `AB` coordinates.  The
quadratic wall in (12) is `B`-standard and has no `AA` coordinate.  The
quadratic and cubic are coprime: after `t=p/q`, their resultant is `256`.
Therefore only the block-constant cubic can carry a full-edge mixed kernel.

Normalize `q=1` and put

```text
c(t)=t^3+2t^2+3t+4.                                 (15)
```

At every root of `c`, the generic master-Hessian chart is legal:
`t(4-t)(t+2)!=0`.  The block-constant mixed kernel is one-dimensional and,
up to a common nonzero scale, has edge-orbit values

```text
f_AA=8t^2,
f_AB=-t(3t+4),
f_BB=-2(t^2+2t+8)/t.                                (16)
```

Every value in (16) is nonzero at a root of `c`.  Equivalently, this is the
one genuine full-edge survivor of the mixed-kernel test in all two-level
orbits.  The real cubic is strictly increasing and has its unique real root
in `(-2,-3/2)`, so signature alone cannot remove it.

## 4. Primitivity kills the cubic survivor

For a block-constant quadratic `F` with orbit values `(u,v,w)`, the
coefficient of `ell F^2` on a five-set whose complementary pair has type
`AA` is

```text
6w(4v+w).                                             (17)
```

Substituting (16) into (17) gives

```text
24 (t^2+2t+8)(6t^3+9t^2+2t+8)/t^2.                  (18)
```

Neither numerator factor can vanish at a root of `c`, because

```text
Res_t(c,t^2+2t+8)=256,
Res_t(c,6t^3+9t^2+2t+8)=1280.                       (19)
```

Both resultants are nonzero in characteristic zero.  Hence (18) is nonzero,
contradicting the mandatory primitive equation `ell F^2=0`.  The unique
two-level full-edge mixed-kernel curve is therefore nonphysical.

Combining this with the earlier `1+6` exclusion proves the promised
two-level theorem.

## 5. Exact wall

```text
nonzero 1+6 star orbit:                    EXCLUDED;
nonzero 2+5 star orbit:                    EXCLUDED;
2+5 singular modules:                     MISS AA OR MORE;
nonzero 3+4 nontrivial-module walls:       MISS AN EDGE ORBIT;
3+4 block-constant cubic mixed kernel:     FULL EDGE, EXACT;
3+4 cubic primitive five-set coefficient: NONZERO;
nonzero stars with <=2 coordinate values:  EXCLUDED;
stars with >=3 coordinate values:          UNKNOWN;
exceptional mixed-kernel divisors:         PARTLY OPEN;
full-edge physical P7 extension:           UNKNOWN;
global Krenn--Gu:                          UNRESOLVED. (20)
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_physical_extension_two_level_star_orbit_complete_exclusion.py
python claims/p7/audit_p7_physical_extension_two_level_star_orbit_complete_exclusion.py
python -m py_compile verify_p7_physical_extension_two_level_star_orbit_complete_exclusion.py audit_p7_physical_extension_two_level_star_orbit_complete_exclusion.py
uv run --with ruff ruff check verify_p7_physical_extension_two_level_star_orbit_complete_exclusion.py audit_p7_physical_extension_two_level_star_orbit_complete_exclusion.py
```

The primary verifier constructs the full equivariant edge bases and proves
the universal block decompositions.  The independent standard-library audit
rebuilds the small blocks in exact polynomial arithmetic, certifies both
homogeneous determinants, and recomputes the primitive resultant obstruction.
Neither imports the other or project code.

## Dependencies and literature

- [P7_PHYSICAL_MIXED_KERNEL_BOOLEAN_DOWN_DESCENT_AND_SEVEN_BY_SEVEN_MASTER_HESSIAN.md](P7_PHYSICAL_MIXED_KERNEL_BOOLEAN_DOWN_DESCENT_AND_SEVEN_BY_SEVEN_MASTER_HESSIAN.md)
- [P7_PHYSICAL_EXTENSION_MIXED_HARD_LEFSCHETZ_SIGN_CHAMBER_AND_ONE_EXCEPTIONAL_ORBIT_OBSTRUCTION.md](P7_PHYSICAL_EXTENSION_MIXED_HARD_LEFSCHETZ_SIGN_CHAMBER_AND_ONE_EXCEPTIONAL_ORBIT_OBSTRUCTION.md)
- Gondim and Zappalà's [mixed-Hessian criterion for Lefschetz
  maps](https://arxiv.org/abs/1803.09664) supplies the neighboring algebraic
  framework.  The `S_m x S_n` block closure and primitive resultant
  obstruction above are problem-specific.
