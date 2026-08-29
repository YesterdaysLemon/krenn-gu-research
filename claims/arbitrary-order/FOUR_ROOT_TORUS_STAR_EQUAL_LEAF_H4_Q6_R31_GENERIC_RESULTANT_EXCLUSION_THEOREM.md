# Four-root torus-star equal-leaf H4 Q6 R31-free generic resultant localization (GLD96)

## Status and exact scope

**Exact scoped characteristic-zero theorem (`GLD96`, strengthened
2026-08-29).**  In the normalized equal-leaf H4 chart, use the six-row and
six-column selector

```text
R31 = (0,1,2,17,25,31),   S = (0,1,3,4,6,7).
```

Write `b=b88+B` and `c=c88+C`, where `(b88,c88)` is the written GLD88
three-parameter family.  On `V(Q6)` and the explicitly localized open

```text
D(E31 * H2 * g0 * Delta),
```

the four selected raw bordered seven-minors force `B=C=0`.  Consequently,
after the GLD88-to-GLD95 family identification, the corresponding
rank-at-most-six incidence is excluded on `D(Omega)` by GLD95.  This is a
generic resultant localization: it proves that `E31` and `g0` are nonzero
base polynomials by an exact specialization and then removes their zero
loci from the statement.  It does **not** close those exceptional loci.

The calculation is over `Q` and extends scalars to `C`.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

The result is deliberately narrower than a full H4 closure.  It includes
`R31=0` wherever the displayed remaining factors are nonzero, because no
inverse of `R31` occurs.  It does not cover arbitrary H4 points outside the
written F88 offset chart, the exceptional factors in the displayed
localization, the GLD83 pulled-back Fitting ideal, other
charts/components/source branches, or any unrelated root/order obligations.

## 1. Coordinates, divisors, and the exact statement

Use the scale-fixed leaf

```text
G = [1  1       1      ]
    [p  q       s      ],
    [a  1+b     1+c    ],

s = (p+q-pq)/(p+q-1).
```

The H4 relation is `pq+ps+qs-p-q-s=0`.  Put

```text
d0 = p+q-1,
P  = p^2-p+1,
L1 = p^2+2pq-2p-q,
L2 = 2pq-p+q^2-2q,
e  = 2pq^2-2pq-p-q^2-2q+2,
Delta = (p-q)d0 P L1 L2 e.
```

The exact rational functions `b88,c88` are the GLD88 functions, reproduced
in the GLD95 theorem document.  Thus the offsets are defined on `D(Delta)`:

```text
b = b88(p,q,a) + B,
c = c88(p,q,a) + C.
```

Let `M(G)` be the fixed 37-by-9 GLD71 syndrome.  Let `R31` denote the
following raw submatrix determinant (the symbol is overloaded in the usual
way with its row set):

```text
R31(G) = det M(G)[(0,1,2,17,25,31), (0,1,3,4,6,7)].
```

The four selected bordered minors are

```text
T0 = det M[(0,1,2,17,25,31,28), (0,1,3,4,6,7,8)],
T1 = det M[(0,1,2,17,25,31,32), (0,1,3,4,6,7,2)],
T2 = det M[(0,1,2,17,25,31,32), (0,1,3,4,6,7,5)],
T3 = det M[(0,1,2,17,25,31,33), (0,1,3,4,6,7,8)].
```

If `P` is the displayed 6-by-6 submatrix and the added row and column for
`T_i` are written as `r_i,c_i,x_i`, then the polynomial bordered-determinant
identity is

```text
T_i = det [ P    c_i ]
          [ r_i  x_i ]
    = R31*x_i - r_i*adj(P)*c_i.
```

This is an identity in the polynomial ring, not a Schur-complement division.
It remains valid when `R31=0`.  On the exact `(p,a)=(2,3)` witness replay, the
primary checks the adjugate expression against each direct bordered
determinant; the independent audit starts from the direct 7-by-7 determinants.
Thus `R31` selects the common rows and columns and supplies a diagnostic
factorization, but it is not a localization gate.

The Q6 equation is

```text
Q6 = 2p^4q^2-2p^4q+p^4
     +2p^3q^3-7p^3q^2+5p^3q-2p^3
     +2p^2q^4-7p^2q^3+12p^2q^2-7p^2q+2p^2
     -2pq^4+5pq^3-7pq^2+2pq+q^4-2q^3+2q^2.
```

Let `K=Q(p,a)` and, away from `H2=2p^2-2p+1`, reduce q-coefficients in
the finite algebra `K[q]/(Q6)`.  After substituting `b88+B,c88+C`, choose
parameter-only denominator clearings `D_i` (nonzero on `D(Delta)`) and write
`Ttilde_i=D_i*T_i`.  Clearing never uses B or C.  The four exact cleared
bordered minors have the form

```text
Ttilde_i = f_i(B) + C*g_i(B),  f_i(B) in B*K[q]/(Q6)[B].
```

The affine-in-C assertion follows directly from the exact raw c-degrees
listed below; `f_i(0)=0` follows from the 111 GLD88 common-kernel identities.
Define

```text
H_ij = (f_i*g_j - f_j*g_i)/B,
rho  = Res_B(H_01,H_02),
E31  = a cleared q-resultant/norm of rho against Q6,
g0   = a cleared q-resultant/norm of g_0(0) against Q6.
```

`Cleared` means that all powers of `H2` and the displayed family
denominators are removed before taking the primitive numerator; multiplying
`E31` or `g0` by a nonzero rational constant does not change the principal
open.  This gives the precise localization

```text
Ures = D(E31 * H2 * g0 * Delta).
```

The theorem is

```text
V(Q6,T0,T1,T2,T3) intersect Ures
    is contained in {B=0,C=0} = F88.
```

Using the GLD75/GLD86 incidence bridge and the GLD95 finite F88 exclusion,
the load-bearing consequence is the scoped empty intersection

```text
B_incidence intersect V(I_7(A)) intersect H4 intersect V(Q6)
  intersect Ures intersect D(Omega) = empty,
```

on this normalized offset domain.  Here `B_incidence` denotes
the incidence variety, not the offset variable `B`.

## 2. Exact raw determinant certificate

The primary verifier reconstructs the GLD71 sparse annihilator and computes
all five raw determinants over `Q`.  The numerator hashes are SHA256 hashes
of SymPy `srepr` strings.  The denominator is the reduced positive
denominator displayed by SymPy.

| determinant | denominator | terms | degrees `(p,q,a,b,c)` | numerator `srepr` SHA256 |
| --- | --- | ---: | --- | --- |
| `R31` | `1` | 289 | `(8,8,2,2,0)` | `48534ee25c536cbc4bfa36b126360a0479857cb3855d87ac9fd13b1e5e51cd32` |
| `T0` `(28,8)` | `d0^3` | 1268 | `(11,11,2,2,1)` | `ec46caa68329938274aca4330cdaddf562303eb6f220b6ff1f56cccf395a84b9` |
| `T1` `(32,2)` | `d0^2` | 1435 | `(10,10,3,3,1)` | `1a3a7ed2d5a75403be1f474c8d3d5355d5f3171f62ffe6c1d813caff75e83012` |
| `T2` `(32,5)` | `d0^3` | 2134 | `(12,12,3,3,1)` | `b21e118aaedaed1bb832f248f5cdae44498a28e5ef5ca40166d425f5e0f0512a` |
| `T3` `(33,8)` | `d0^2` | 850 | `(10,10,2,2,1)` | `726316fc7b1c76acb254793b271e9d77e655fda5333cef4643b4fe5c18fe14fb` |

The raw pivot numerator factors as

```text
R31 = 2*(p-q)*(p+q-1)*J31,
```

with a nonzero exact polynomial `J31`.  This factorization is retained as a
diagnostic rather than cancelled or inverted.  The theorem neither divides
by `R31` nor uses its factors to change the chart.  The independent audit's
direct bordered determinants do not compute an inverse of this submatrix.

The GLD88 vector used at `B=C=0` is

```text
k = (u,v,1),
u = (q^2-q+1)L2 / ((p-q)d0^3),
v = -P L1 / ((p-q)d0^3).
```

The primary checks all `3*37=111` block equations
`M(G)[:,3j:3j+3] k=0`.  Therefore every selected bordered minor vanishes at
`B=C=0`, proving the required B-divisibility after denominator clearing.

## 3. Four residuals and the exact nonzero witness

To prove that `E31` and `g0` are genuine (not identically zero), specialize
exactly to `(p,a)=(2,3)`.  Then

```text
Q6 = 5q^4 - 4q^3 + 12q^2 - 16q + 8.
```

The primary computes each bordered determinant as
`det(pivot)*entry - row*adj(pivot)*column`, reduces every q coefficient in
the Q6 algebra, and records the support:

| target | B-only exponents in `f_i` | B exponents in `g_i` | reduced monomial count |
| --- | --- | --- | ---: |
| `T0=(28,8)` | `1,2` | `0,1,2` | 5 |
| `T1=(32,2)` | `1,2,3` | `0,1,2` | 6 |
| `T2=(32,5)` | `1,2,3` | `0,1,2` | 6 |
| `T3=(33,8)` | `1,2` | `0,1,2` | 5 |

The two cross-polynomials `H_01,H_02` both have B-degree four.  Their
resultant, reduced modulo Q6 and made primitive in `Q[q]`, has coefficient
tuple (in descending powers of q)

```text
(
 -905501121543829653519134583029125628170363723798877745648523367180968018033574358187,
 -581967626061819630034063550351650331374757486676325140922444735277204122667234925864,
  1965327315048008656313355784299314970407615267446169045708659903094610123987480161652,
 -1135825891000896384111550023303077198001706298129393658672106278421500353284383698011
).
```

The tuple SHA256 (of Python `repr(tuple)`) is
`f0b2368dda1ea6a89d31ccf98242f48ed5d3540a14d412393b7870719780a05b`.
Its resultant with Q6 has the nonzero exact factorization

```text
3^6 * 5^282 * 31^2 * 173^2 * 269 * 1709
  * 20357^2 * 270217^2 * 52321 * 475485394682070314208533.
```

The first C-coefficient at B=0 is

```text
g_0(0) = (-152501184q^3 + 255629952q^2
          -158823936q + 30786048)/3125,
```

and its numerator resultant with Q6 factors as

```text
2^33 * 3^16 * 5^14 * 110281.
```

Both factors are therefore nonzero in characteristic zero.  This is a
nonzero-witness argument for the generic base polynomials; it is not a claim
that the displayed integer factors remain units in every characteristic.

## 4. Proof of the localized implication

Assume a point on `V(Q6)` lies in `Ures` and all four selected bordered
minors vanish.  Since `H2` is inverted, the definitions above are valid in
the finite q-algebra.  If `B` is nonzero, each equation
`f_i(B)+C*g_i(B)=0` gives, after cross-multiplication,

```text
f_i*g_j - f_j*g_i = 0,
```

and hence `H_01=H_02=0` because every `f_i` is divisible by B.  The
definition of `E31` and the condition `E31 != 0` exclude a common Q6 root of
these two polynomials.  Thus `B=0`.  The first residual then reads
`C*g_0(0)=0`; the condition `g0 != 0` makes `g_0(0)` a unit in the Q6
algebra, so `C=0`.

At `B=C=0`, GLD88 supplies the three block-supported copies of `k`, and the
GLD75/GLD86 bridge identifies the incidence equations with this syndrome
system under `C_8=1`.  GLD95's exact all-factor F88 theorem then excludes
the remaining Q6 common-minor point on `D(Delta)`, including its old `P6=0`
content fibres.  With `D(Omega)`, this gives the scoped empty intersection
in Section 1.

## 5. Exceptional strata and retained frontier

The localization and the implication have these explicit fences:

| stratum | treatment in GLD96 |
| --- | --- |
| `R31=0` | covered wherever `E31 H2 g0 Delta` is nonzero; the intersections with retained exceptional factors remain open |
| `E31=0` | not covered; cross-resultant degeneracy is the next generic-boundary obligation |
| `g0=0` | not covered; the B=0 C-equation loses the selected unit coefficient |
| `H2=0` | not covered by this q-algebra reduction; no invalid generic division is used there |
| `Delta=0` | excluded from this theorem.  Portions are treated by the separately scoped GLD87/GLD89/GLD93/GLD94 results, but no blanket replacement is asserted here |
| outside F88 offset domain | not covered; GLD96 does not force an arbitrary H4 point into this written family without the displayed denominators |
| GLD83 Fitting pullback, other charts/components/source branches | remain open |
| global Krenn--Gu conjecture | remains **UNRESOLVED** |

The exploratory double-pivot census and any resultant on that boundary are
retained only as historical scoped evidence.  They are not used in the
theorem.  The strengthened implication covers `R31=0` directly on the same
remaining principal open; it does not close intersections of `R31=0` with
`E31=0`, `g0=0`, `H2=0`, or `Delta=0`.

## 6. Reproduction and independent audit

From the repository root run:

```text
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_r31_generic_resultant_exclusion.py
python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_r31_generic_resultant_exclusion.py
```

The primary reconstructs the 37 sparse relations through the GLD71
`coefficient_matrix`, uses the global bordered-determinant/adjugate identity,
checks it against direct determinants, and checks the
raw determinant hashes, all 111 GLD88 block identities, the four exact
specialized residuals, and the two nonzero norms.  The audit does not import
the primary or GLD88: it transcribes the F88 functions locally, accumulates
each syndrome entry directly from the pinned sparse supports, and computes
the bordered determinants by a Bareiss elimination in `Q(q)[B,C]`.  It then
replays the Q6 reduction and resultant.  The shared sparse support data and
the written F88/Q6 formulas are upstream mathematical inputs; neither script
reproves the GLD75/GLD86 bridge or GLD95's all-factor F88 theorem.

## 7. Lineage

GLD86 supplies the four-divisor rank-at-most-six syndrome containment.
GLD87 closes H1/H2/H3, and GLD88 supplies the H4 rational family and its
common block kernel.  GLD89, GLD90, GLD93, and GLD94 close separate named
divisor pieces.  GLD95 closes the finite Q6 common-minor residual on the
written F88 family.  GLD96 supplies the R31-free generic resultant
localization that reaches that GLD95 family from the four selected
seven-minors.  It removes `R31=0` as an independent wall on this offset
route, while retaining the exceptional-factor and global obligations.
