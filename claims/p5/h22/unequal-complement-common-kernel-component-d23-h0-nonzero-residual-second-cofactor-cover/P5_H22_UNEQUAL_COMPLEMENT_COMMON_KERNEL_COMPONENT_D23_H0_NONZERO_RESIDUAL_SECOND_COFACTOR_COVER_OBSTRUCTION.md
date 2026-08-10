# Component twenty-two residual second-cofactor cover obstruction

## Status

**Exact characteristic-zero generic-component theorem.**  Work over
`K=Q(A,R,D)` on the finite-`D23` component-twenty-two residual

```text
h1=0,       2*h3=2*A+R,       G=G2=P=0,            (1)
```

with all open factors listed in the preceding cofactor-open theorem,
including

```text
h0!=0,       R*h2!=1,       rho*(rho-1)*(rho+1)!=0. (2)
```

Then a second fixed eight-by-eight mixed minor is nonzero.  Hence the
fourteen-by-eight mixed matrix has rank eight, its common binary extension
kernel is zero, and no weighted-`H22` lift exists on (1)--(2).

Together with the first cofactor-open theorem, this closes the entire
displayed `h1=0`, finite-`D23` residual over `K`.  It does not close the
unexhausted `h1!=0` locus, special parameter fibres, arbitrary source order,
or the global Krenn--Gu conjecture, which remains **UNRESOLVED**.

No finite-field calculation is used.  One rational specialization is used
only to certify that two universal resultants are nonzero polynomials in
`Q[A,R,D]`; the conclusion is over the rational function field `K`.

## Cramer reduction of the first cofactor divisor

Both `G` and the first cofactor polynomial `P` are linear in `h0,h2`.  Write

```text
G =a0*h0+a2*h2+ac,
P =b0*h0+b2*h2+bc,                                 (3)
Delta=a0*b2-a2*b0,
n0=a2*bc-ac*b2,       n2=ac*b0-a0*bc.              (4)
```

At every common zero of `G,P`, Cramer's identities give

```text
Delta*h0=n0,       Delta*h2=n2.                    (5)
```

The exact specialization `(A,R,D)=(2,1,3)` gives

```text
Delta=-36*(7947*rho^3+24451*rho^2-2443*rho-16419),
n0=12*(971*rho^3-2989*rho^2+3829*rho+205),         (6)

Res_rho(Delta,n0)
 =-29467769797761114707066880000000 !=0.            (7)
```

Resultants are universal polynomials in the coefficients.  Thus (7) proves
that `Res_rho(Delta,n0)` is nonzero in `Q[A,R,D]`, so `Delta,n0` are coprime
in `K[rho]`.  Equations (5) therefore rule out `Delta=0`; every point of
(1) lies on the Cramer open and has

```text
h0=n0/Delta,       h2=n2/Delta.                    (8)
```

Since `G2` is bilinear in `h0,h2`, write it as

```text
G2=c02*h0*h2+c0*h0+c2*h2+cc.
```

After (8), its cleared numerator is

```text
N=c02*n0*n2+c0*n0*Delta+c2*n2*Delta+cc*Delta^2.    (9)
```

The primitive part of `N` in `rho` has degree seven and is divisible by
`rho+1`.  This is an exact polynomial division over `Q[A,R,D]`.  Since
`rho+1` is inverted in (2), the remaining equation is a degree-six
polynomial

```text
Qbar=N_primitive/(rho+1)=0.                        (10)
```

This sextic is a temporary exact survivor classification, not a claimed
binary lift.

## The second mixed minor

Let `M` be the same fourteen-by-eight finite-`D23` mixed matrix as in the
first cofactor theorem.  Take all columns and rows

```text
(0,2,3,4,5,7,8,10),                               (11)
```

and call the determinant `J`.  Every entry of `M` has total degree at most
two in `h0,h2`.  Consequently

```text
F=Delta^16*J(n0/Delta,n2/Delta) in K[rho].         (12)
```

If the common mixed kernel were nonzero on (1), then every maximal minor,
including `J`, would vanish; hence `F=0`.

It remains to prove that (10) and (12) cannot vanish simultaneously.  This
again needs only one exact nonzero-resultant specialization.  At
`(A,R,D)=(2,1,3)`, the primitive sextic is

```text
58411813*rho^6 + 86961310*rho^5 - 782473889*rho^4
-1226471868*rho^3 + 1607129299*rho^2
+839733022*rho - 813293399.                        (13)
```

The second minor itself factors as

```text
J=5760000*rho*(rho-1)*(rho+1)*(rho+2)*(3*rho+1)
  *(1679*h0*rho^2-1470*h0*rho-3341*h0
    +109*rho^2-138*rho-55).                        (14)
```

After (8), its reduced numerator has primitive factorization

```text
rho*(rho-1)*(rho+1)^2*(rho+2)*(rho+13)*(3*rho+1)
*(43*rho-61)*(563*rho^2-600*rho-107).              (15)
```

Exact Euclidean algorithms give

```text
gcd(Qbar,Delta)=gcd(Qbar,numerator(15))=1.          (16)
```

Since the specialization of (12) differs from a positive power of `Delta`
times (15) only by a nonzero rational scalar, (16) says that the universal
resultant `Res_rho(Qbar,F)` has a nonzero specialization.  It is therefore
nonzero over `K`.  Equations (10) and (12) have no common root over the
algebraic closure of `K`, so `J!=0` at every point of (1)--(2).  This proves
the claimed rank-eight obstruction.

## Boundary

The theorem is generic in `A,R,D`.  It does not assert the same result after
specializing onto the zero divisor of either universal resultant.  Those
special parameter fibres remain separate projective/special-fibre work.
The `h1!=0` finite-`D23` locus also remains **UNKNOWN**.  Nothing here is a
counterexample to the conjecture.

## Replay

Replay the dependency first:

```powershell
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-h0-nonzero-residual-cofactor-open/verify_p5_h22_unequal_complement_common_kernel_component_d23_h0_nonzero_residual_cofactor_open_obstruction.py
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-h0-nonzero-residual-cofactor-open/audit_p5_h22_unequal_complement_common_kernel_component_d23_h0_nonzero_residual_cofactor_open_obstruction.py
```

Then run:

```powershell
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-h0-nonzero-residual-second-cofactor-cover/verify_p5_h22_unequal_complement_common_kernel_component_d23_h0_nonzero_residual_second_cofactor_cover_obstruction.py
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-h0-nonzero-residual-second-cofactor-cover/audit_p5_h22_unequal_complement_common_kernel_component_d23_h0_nonzero_residual_second_cofactor_cover_obstruction.py
```

The primary reconstructs the residual and both mixed minors with repository
utilities.  The audit imports no repository code and independently rebuilds
the component rows, permanents, mixed matrix, Cramer reduction, sextic, and
second-minor specialization.
