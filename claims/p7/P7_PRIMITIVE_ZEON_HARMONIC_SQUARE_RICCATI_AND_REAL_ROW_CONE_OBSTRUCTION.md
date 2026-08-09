# Primitive P7 squares obey a zeon harmonic-square Riccati law

## Status

**Exact characteristic-zero contractions and a real open-cone exclusion.**
Work in the eight-variable square-free commutative algebra

```text
Z=K[z_0,...,z_7]/(z_0^2,...,z_7^2),
ell=z_0+...+z_7,
Q=sum_(i<j)b_ij z_i z_j,
H=Q^2/2.                                             (1)
```

Write `partial_i` for Boolean deletion of `z_i`, `D=sum_i partial_i`, and

```text
r_i=sum_(j!=i)b_ij,       S=sum_i r_i,
B=(b_ij),                 b_ii=0.                    (2)
```

At middle degree, Boolean `sl_2` gives

```text
ell H=0  <=>  D H=0.                                 (3)
```

The lowering operator is not an ordinary derivation: repeated variables
are killed by the zeon product.  Its exact corrected Leibniz rule is

```text
partial_i(fg)
 =(partial_i f)g+f(partial_i g)
  -2z_i(partial_i f)(partial_i g).                   (4)
```

Consequently a primitive square is a **zeon harmonic square** satisfying

```text
Q(DQ)=sum_i z_i(partial_i Q)^2.                      (5)
```

Equation (5) is exactly the 56 dual-triangle equations, but it admits useful
low-degree contractions which were not visible in the star denominators.
Every primitive square satisfies, for `i!=j`,

```text
(B^2)_ij
 =(S/2-2r_i-2r_j)b_ij+r_i r_j+2b_ij^2,              (6)
```

and, for every vertex `i`,

```text
(Br)_i-sum_(j!=i)b_ij^2
 =r_i(S/2-r_i).                                      (7)
```

Summing once more gives the symmetric quadratic Casimir

```text
S^2=4(sum_i r_i^2-sum_(i<j)b_ij^2).                 (8)
```

These identities hold over every characteristic-zero field.  They are
necessary contractions, not claimed to replace the full triangle system.

Over the reals, a full-edge primitive square must therefore obey the strict
row-sum cone inequality

```text
|sum_i r_i| < 2 sqrt(sum_i r_i^2).                  (9)
```

Indeed, all 28 real edge squares in (8) have positive sum, strictly so on
the edge torus.  Thus the two closed circular cones cut out by the reverse
inequality are empty.  In particular, constant real row sums are impossible.
If `mu=S/8` and `sigma^2=(1/8)sum_i(r_i-mu)^2`, then every hypothetical
real full-edge solution with `mu!=0` must satisfy

```text
sigma>|mu|.                                          (10)
```

This does not exclude complex solutions: the sum of the `b_ij^2` in (8) is
not a Hermitian norm over `C`.  The complex primitive-square torus, the
mixed-sign physical extension incidence, P7, and global Krenn--Gu remain
**UNKNOWN/UNRESOLVED**.

## 1. Corrected zeon calculus

Every zeon form has a unique decomposition relative to vertex `i`,

```text
f=f_0+z_i f_1,       g=g_0+z_i g_1,                 (11)
```

where the four displayed forms do not contain `z_i`.  Since `z_i^2=0`,

```text
fg=f_0g_0+z_i(f_1g_0+f_0g_1).
```

The left side of (4) is therefore `f_1g_0+f_0g_1`.  Its first two terms on
the right are

```text
f_1(g_0+z_i g_1)+(f_0+z_i f_1)g_1,
```

and the correction removes the two copies of `z_i f_1g_1`.  This proves
(4) over any field in which two is nonzero.

Apply (4) to `f=g=Q` and sum over `i`:

```text
D(Q^2)=2Q(DQ)-2sum_i z_i(partial_iQ)^2.              (12)
```

Because `H=Q^2/2`, equations (3) and (12) prove (5).  The terminology
"zeon" and the Boolean `sl_2` raising/lowering representation are standard;
see Philip Feinsilver,
[*Representations of sl(2) in the Boolean lattice, and the Hamming and
Johnson schemes*](https://arxiv.org/abs/1102.0368).  The harmonic-square
identity and Riccati contractions below are the problem-specific transfer.

## 2. Coordinate harmonic-square equation

Since

```text
DQ=sum_i r_i z_i,
partial_i Q=sum_(j!=i)b_ij z_j,                     (13)
```

the coefficient of `z_i z_j z_k` in (5) is

```text
b_ij r_k+b_ik r_j+b_jk r_i
 =2(b_ij b_ik+b_ij b_jk+b_ik b_jk).                (14)
```

These are precisely the dual-triangle equations previously obtained from
middle Boolean duality.  Formula (5) adds an intrinsic product-rule origin:
the all-plus quadratic terms are the collision correction measuring the
failure of ordinary differentiation in the square-free algebra.

## 3. Pair contraction and the matrix Riccati law

Fix an edge `{i,j}` and sum (14) over all `k` outside it.  The left side is

```text
b_ij(S-2r_i-2r_j)+2r_i r_j.                         (15)
```

On the right,

```text
sum_(k outside {i,j}) b_ik b_jk=(B^2)_ij,
sum_k(b_ik+b_jk)=r_i+r_j-2b_ij,
```

so it is

```text
2b_ij(r_i+r_j-2b_ij)+2(B^2)_ij.                    (16)
```

Equating (15) and (16) proves (6).  It is a Hadamard-corrected algebraic
Riccati equation for the symmetric zero-diagonal matrix `B`: ordinary
matrix squaring, row-sum diagonal data, a rank-one term `rr^T`, and the
entrywise square of `B` are forced to agree off diagonal.

## 4. Vertex contraction and the Casimir

Sum (6) over `j!=i`.  Put

```text
d_i=sum_(j!=i)b_ij^2.
```

The left side is `(Br)_i-d_i`.  The sum of the right side is

```text
(3S/2)r_i-3r_i^2-2(Br)_i+2d_i.
```

Rearrangement proves (7).  Finally sum (7) over `i`.  Symmetry gives

```text
sum_i(Br)_i=sum_i r_i^2,
sum_i d_i=2sum_(i<j)b_ij^2,
sum_i r_i(S/2-r_i)=S^2/2-sum_i r_i^2.
```

These three identities reduce exactly to (8).

For real coefficients, full edge support makes
`sum_(i<j)b_ij^2>0`; (8) gives (9).  Writing

```text
sum_i r_i^2=8mu^2+8sigma^2,       S=8mu,
```

turns (9) into `sigma^2>mu^2` when `mu!=0`, proving (10).

## 5. Exact wall

```text
corrected zeon Leibniz rule:                    PROVED;
primitive middle square iff zeon harmonic:      PROVED;
harmonic-square equation (5):                   EXACT;
56 dual triangles from (5):                     EXACT;
off-diagonal matrix Riccati identity (6):       PROVED;
eight vertex contractions (7):                  PROVED;
global quadratic Casimir (8):                   PROVED;
real reverse row-sum cones:                     EMPTY ON EDGE TORUS;
constant real row sums:                         IMPOSSIBLE;
real row-sum coefficient of variation:          STRICTLY GREATER THAN ONE;
complex row-sum cone consequence:               NONE CLAIMED;
complex primitive-square edge torus:            UNKNOWN;
full-edge physical P7 extension:                UNKNOWN;
global Krenn--Gu:                               UNRESOLVED. (17)
```

No graph, support, parameter, tuple, finite field, numerical point, or
monomial search enters the proof.  The replay expands only universal fixed
Boolean identities and their symbolic contractions.

## Replay

```powershell
uv run --with sympy python verify_p7_primitive_zeon_harmonic_square_riccati.py
python audit_p7_primitive_zeon_harmonic_square_riccati.py
python -m py_compile verify_p7_primitive_zeon_harmonic_square_riccati.py audit_p7_primitive_zeon_harmonic_square_riccati.py
uv run --with ruff ruff check verify_p7_primitive_zeon_harmonic_square_riccati.py audit_p7_primitive_zeon_harmonic_square_riccati.py
```

The primary verifier checks the fixed middle raising/lowering kernel, the
corrected Leibniz rule, and all symbolic contractions with SymPy.  The
independent standard-library audit uses a separate sparse polynomial and
Boolean algebra implementation.  Neither imports the other or project code.

## Dependencies

- [P7_PRIMITIVE_BOOLEAN_SQUARE_DUAL_TRIANGLE_STAR_NORMAL_FORM.md](P7_PRIMITIVE_BOOLEAN_SQUARE_DUAL_TRIANGLE_STAR_NORMAL_FORM.md)
- [P7_PRIMITIVE_BOOLEAN_SQUARE_STAR_CLOSURE_DISCRIMINANT_AND_ZERO_ROW_BOUNDARY_THEOREM.md](P7_PRIMITIVE_BOOLEAN_SQUARE_STAR_CLOSURE_DISCRIMINANT_AND_ZERO_ROW_BOUNDARY_THEOREM.md)
