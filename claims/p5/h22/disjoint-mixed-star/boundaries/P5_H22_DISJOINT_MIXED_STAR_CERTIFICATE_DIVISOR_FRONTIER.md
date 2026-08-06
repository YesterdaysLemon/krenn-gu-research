# Certificate-divisor frontier for component-eight `H22`

## Status

This is a proof ledger and stopped symbolic frontier, not a new global
theorem.  It records which codimension-one factors from the first
reduced final `D_01` certificate have exact boundary theorems and which
do not.

No factor is promoted merely because it occurs in one Bezout
certificate.  A listed factor is marked closed only when a normalized
characteristic-zero incidence ideal or a stronger exact obstruction is
available.

## Intrinsic determinant ledgers

The selected `D_23` maximal minors have exact common contents recorded
in
[`P5_H22_DISJOINT_MIXED_STAR_AF_APHI_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_AF_APHI_BOUNDARY_OBSTRUCTION.md).
Every common divisor is now covered by an exact theorem.

The selected `D_01` maximal minors and their independent rank pivot have
exact contents recorded in
[`P5_H22_DISJOINT_MIXED_STAR_ZERO_SLOPE_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_ZERO_SLOPE_BOUNDARY_OBSTRUCTION.md).
Their common base divisors are also covered.

After diagonal normalization, the seven maximal minors are redundant
in the final three `D_01` Fitting ideals: `A_01(z)=1` makes `z`
nonzero, and `M_01(t)z=0` already forces rank at most seven.  The
generic theorem verifier now uses this smaller presentation.

## First reduced final-certificate factor ledger

One exact cleared certificate for the reduced branch
`t_1=t_3=0` contains the following square-free factors.  The table
records their present evidence status.

| factor or family | interpretation | status |
|---|---|---|
| `a^2 f^2+2bf+1` | coefficient divisor; normalizes to a new quadratic branch | exact closed |
| `-a^2 f^2+b^2 f^2+bf+1` | component coefficient `K` | exact closed by parameter branches |
| `a^2 f+b` | component chart denominator | exact closed by parameter branches |
| `a,b,f,a-b,a+b,bf+1` | coordinate/pivot divisors | exact closed or rank-one |
| `af-1,af+1` | four rational `a phi=+/-1` sheets plus old pieces | exact closed |
| `r-1,r+1` | equal/opposite weights | exact closed at binary level |
| `rP+Q` | principal coupled slope graph | exact closed cross-mode |
| `(a+b)r+(a-b)` | source-ratio graph | exact closed |
| `(a+b)r-(a-b)` | sign-conjugate source-ratio graph | exact closed |
| `(af-1)r+(af+1)` | basis-ratio graph | exact closed cross-mode |
| `U r+V` below | larger linear slope graph | **open** |
| `R_2(r)` below | quadratic slope graph | **open** |

Here

```text
U=a^2 f^2+2ab f^2+2af-1,
V=-a^2 f^2+2ab f^2+2af+1,                        (1)
```

and the quadratic factor has the compact form

```text
R_2(r)=
 (a+b)^2(af+1)r^2
 +2(2a^2bf+3a^2-b^2)r
 +(a-b)^2(1-af).                                  (2)
```

This table classifies the factors of one certificate, not every
possible certificate and not the intrinsic projection ideal.

## The two open divisors

### Linear graph

On the source-torus quotient `f=1`, (1) becomes

```text
(a^2+2ab+2a-1)r+(-a^2+2ab+2a+1)=0.               (3)
```

Its missing rational chart is contained in the already-closed
`bf=-1,af=+/-1` strata.  At a generic `F_11` component point, both
weighted directions have exact rank-seven mixed matrices on their
genuine markings and fixed rank-four minors.

The following characteristic-zero presentations all reached a
ten-minute limit:

- algebraic `r,phi` with mode-zero `0137/0157`;
- algebraic `r,phi` with mode-one `0457`;
- rational substitution for `r`;
- the torus slice `f=1`;
- solving (3) for `b` over `C(a,r)`;
- the branch `t_1=t_3=0` after that normalization.

Each is a null result.  None proves existence or nonexistence.

### Quadratic graph

The discriminant of (2) is

```text
4a^2(
 a^4f^2+2a^2b^2f^2+12a^2bf+8a^2
 +b^4f^2-4b^3f-4b^2
).                                                 (4)
```

The missing leading-coefficient chart
`(a+b)^2(af+1)=0` reduces to already-closed `r=-1`, `bf=-1`, or
`af=-1` strata.

Exact split-fibre diagnostics over `F_11` and `F_13` find:

- mode-one `0457` nonzero on every genuine `D_01` direction;
- mode-zero `0137/0157` nonzero on every genuine `D_23` direction.

Algebraic-extension calculations using those minors and alternative
mode-three minors reached ten-minute limits in `D_01`.  These are null
results, not a theorem.

## Structural reduction

The exact source-torus quotient

```text
(a,b,f,phi) ~ (af,bf,1,phi/f)
```

is proved in
[`P5_H22_DISJOINT_MIXED_STAR_TORUS_QUOTIENT.md`](P5_H22_DISJOINT_MIXED_STAR_TORUS_QUOTIENT.md).
It reduces the component base from a threefold to a surface while
leaving both weighted slopes unchanged.  The two open divisors remain
computationally hard even on this quotient.

The next useful symbolic method should therefore eliminate the linear
extension variables before the algebraic base variables.  Promising
forms are:

1. a Cramer/kernel-line presentation on each marking component;
2. the norm of a fixed marked minor from the quadratic base extension;
3. a subresultant or Fitting-module computation over the quotient
   surface, rather than another full Gröbner basis in all variables.

## Global proof boundary

Closing (1)--(2) would finish only the visible codimension-one factors
of one reduced certificate on one known pure component.  Deeper
intersections, other certificates, component exhaustiveness, the full
`P_5 -> Delta_3` obstruction, and the arbitrary-order global lift all
remain unresolved.
