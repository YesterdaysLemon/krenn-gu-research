# Switched-circulant seven-leaf squares are never primitive

## Status

**Exact characteristic-zero exclusion of an infinite symmetry family in the
P7 quotient-singular descent.**  Work in the Boolean algebra

```text
A(L)=K[z_0,...,z_6]/(z_0^2,...,z_6^2),
ell=z_0+...+z_6,
```

over a field `K` of characteristic zero.  Let `a,b,c in K`, let every
`s_i in K^*`, and give the edge `{i,j}` the weight

```text
x_ij=s_i s_j a    if the cyclic distance is 1,
x_ij=s_i s_j b    if the cyclic distance is 2,
x_ij=s_i s_j c    if the cyclic distance is 3.       (1)
```

Put

```text
F=sum_(i<j)x_ij z_i z_j,             N=F^2/2.        (2)
```

Then

```text
ell N=0    =>    a=b=c=0    =>    F=0.               (3)
```

Thus no nonzero seven-leaf circulant quadratic, even after arbitrary
nonzero vertex switching, has a primitive Boolean square.  The theorem
includes every coordinate boundary among `a,b,c`; it does not assume that
the 21 edge coefficients are nonzero.

The proof does not inspect parameter tuples.  It converts primitivity into
a `C_7`-equivariant linear kernel in the reciprocal switches, diagonalizes
that kernel into seven characters, and excludes every character by one
fixed degree-four Macaulay certificate.  The independent audit rebuilds the
certificate using only integer polynomial arithmetic.

This removes the switched-circulant family from the necessary seven-leaf
equation `ell_L F^2=0` in the P7 quotient-singular radial lift.  It does
**not** exclude an arbitrary seven-leaf quadratic, the full physical
singular incidence, P7, or global Krenn--Gu; those remain
**UNKNOWN/UNRESOLVED**.

## 1. Switching linearizes the primitive equations

First remove the switches and write `F_0` for the cyclic-distance form with
edge weights `a,b,c`.  For a four-set `T`, let

```text
n_T=[z_T]F_0^2/2.                                    (4)
```

It is the three-term hafnian of the induced weighted `K_4`.  Equation (1)
therefore gives

```text
[z_T]N=(product_(i in T)s_i)n_T.                     (5)
```

Primitivity has one equation for each five-set `S`:

```text
0=[z_S]ell N=sum_(v in S)[z_(S minus {v})]N.         (6)
```

Divide (6) by the nonzero product of the five switches in `S` and put
`r_v=s_v^(-1)`.  The result is

```text
sum_(v in S)n_(S minus {v}) r_v=0.                   (7)
```

Hence the 21 primitive equations are one linear map

```text
K_(a,b,c):K^7 -> K^21,                               (8)
```

whose coefficients are homogeneous quadrics in `a,b,c`.  Both the cyclic
shift of the seven vertices and the decomposition of five-sets by the
distance of their missing edge preserve (7).  Thus (8) is `C_7`-equivariant;
its codomain is three cyclic orbits, indexed by missing-edge distances
`d=1,2,3`.

Any switched primitive square would supply the nonzero vector

```text
r=(s_0^(-1),...,s_6^(-1)) in ker K_(a,b,c).          (9)
```

It is therefore enough to prove that (8) is injective whenever
`(a,b,c)!=(0,0,0)`.

## 2. The three Fourier-symbol quadrics

Extend scalars to an algebraic closure.  This cannot destroy injectivity
over `K`.  Since the characteristic is zero, the regular `C_7` module
splits into the seven characters

```text
r_v=t^v,                         t^7=1.              (10)
```

For such a character, the three missing-edge orbits in (7) reduce to three
scalar quadrics.  Define

```text
A=a^2+ac+b^2,
B=ab+ac+bc,
C=a^2+bc+c^2,
D=ab+b^2+c^2.                                        (11)
```

Direct expansion of the four-hafnians gives

```text
E_1=A(t^2+t^6)+B(t^3+t^5)+C t^4,
E_2=A t+B(t^3+t^6)+D(t^4+t^5),
E_3=B(t+t^2)+C(t^4+t^6)+D t^5.                      (12)
```

The character (10) lies in the kernel exactly when

```text
E_1(t)=E_2(t)=E_3(t)=0.                              (13)
```

Because 7 is prime, `t=1` is the trivial character and every other `t` is a
primitive seventh root.  This reduces injectivity of the full
21-equation, seven-unknown equivariant problem to two exact homogeneous
elimination checks in the three parameters `a,b,c`.

## 3. One degree-four Macaulay certificate

Multiply each quadratic in (12) by the six degree-two monomials

```text
a^2, ab, ac, b^2, bc, c^2.                           (14)
```

In the 15-dimensional space `K[a,b,c]_4`, this gives an `18 x 15`
coefficient matrix `M(t)`.  Select the following 15 rows:

```text
E_1 times all six monomials;
E_2 times a^2,ab,ac,b^2,bc;
E_3 times a^2,ab,ac,b^2.                             (15)
```

Call the resulting square matrix `M_*(t)`.  Exact integer determinant
calculation gives

```text
det M_*(1)=-3149280=-2^5 3^9 5,                     (16)
```

and, modulo the seventh cyclotomic polynomial
`Phi_7(t)=1+t+...+t^6`,

```text
det M_*(t)=-73728 t^3(t+1)
            =-2^13 3^2 t^3(t+1)       mod Phi_7.    (17)
```

Both values are nonzero in characteristic zero.  In (17), a primitive
seventh root is neither zero nor minus one.

Consequently, for every seventh root `t`, the degree-four part of the ideal

```text
(E_1(t),E_2(t),E_3(t))                               (18)
```

is all of `K[a,b,c]_4`.  If the three quadrics had a common nonzero
projective point, every quartic in (18) would vanish there.  One of
`a^4,b^4,c^4` is nonzero at such a point, a contradiction.  Therefore

```text
E_1(t)=E_2(t)=E_3(t)=0    =>    a=b=c=0              (19)
```

for all seven characters.

Every invariant kernel of (8) is a direct sum of character spaces.  Equation
(19) proves that the kernel is zero for every nonzero parameter triple.
This contradicts (9) and proves (3).

## 4. A reusable invented tool: equivariant primitivity resultants

The proof suggests a general symbolic device for symmetry-restricted
Boolean-square problems.

Let a finite group `Gamma` act on the vertices, let a parameterized
quadratic `F_theta` be `Gamma`-invariant, and allow arbitrary nonzero vertex
switches.  Switching a coefficient of `F_theta^m/m!` factors by the product
of the switches on its support.  Dividing the primitive equations by the
switch product produces a linear `Gamma`-equivariant map

```text
K_theta:(reciprocal switch module) ->
        (primitive-equation module).                 (20)
```

Over characteristic zero, decompose (20) into irreducible representation
blocks.  For each block, its maximal-minor ideal in `theta`, or any finite
degree multiplication matrix whose full-rank minor forces that ideal to
contain the whole graded piece, is an **equivariant primitivity resultant
certificate**.  If these certificates exclude every nonzero projective
`theta` on every irreducible block, then `K_theta` is injective and no
nonzero switched member of the family can be primitive.

For the present `C_7` family, all irreducibles are characters, the three
codomain orbits give (12), and (16)--(17) are the complete block
certificates.  This formulation is not a conjectural analogy: (20),
semisimple decomposition, and the full-graded-piece implication are the
proof above.  For nonabelian symmetry families it replaces seven scalar
characters by small matrix-valued representation blocks.

## 5. Literature translation

The Fourier step is the finite-group form of simultaneous diagonalization
of circulant operators.  Bamieh derives the discrete Fourier transform
precisely as the common change of basis that diagonalizes the circulant
matrix algebra and points to the representation-theoretic extension:
[Bamieh, *Discovering Transforms*](https://arxiv.org/abs/1805.05533).
The new problem-specific step here is that reciprocal vertex switching
turns Boolean primitivity into the equivariant operator (8).

The degree-four matrix belongs to the Macaulay/resultant side of elimination
theory.  D'Andrea and Dickenstein develop determinant formulas extending
classical Macaulay formulas for homogeneous multivariate resultants:
[D'Andrea--Dickenstein, *Explicit formulas for the multivariate
resultant*](https://arxiv.org/abs/math/0007036).  No general resultant
formula supplies (16)--(17); those are the exact specialized certificates
proved here.  Also, `det M_*` need not be identified with the normalized
resultant.  Its only required role is stronger and more elementary at this
specialization: it proves that the three quadratic multiples span every
quartic.

## 6. Interface with the P7 singular branch

The quotient-singular apolar reduction previously proved that every
physical P7 radial point supplies a seven-leaf quadratic `F` satisfying

```text
ell_L F^2=0.                                         (21)
```

The present theorem proves that (21) has no nonzero solution in the entire
switched-circulant family (1).  In particular:

```text
ordinary circulant ansatz:                    EXCLUDED;
arbitrary nonzero vertex switching:           INCLUDED IN EXCLUSION;
coordinate boundaries among a,b,c:            INCLUDED IN EXCLUSION;
all-nonzero switched-circulant edge torus:     EMPTY;
general seven-leaf primitive square:           UNKNOWN;
compatibility with AF=tJN and Phi_N(G)=0:       NOT REACHED;
physical quotient-singular radial edge torus:  UNKNOWN;
P7 and global Krenn--Gu:                        UNRESOLVED. (22)
```

The exclusion concerns a structured infinite family, not a dimension count
and not evidence that a generic or asymmetric family is empty.

No graph/support enumeration, parameter sweep, numerical approximation,
finite-field inference, Groebner elimination, or timeout is used.

## Replay

```powershell
uv run --with sympy python claims/p7/verify_seven_leaf_switched_circulant_primitive_square_no_go.py
python claims/p7/audit_seven_leaf_switched_circulant_primitive_square_no_go.py
python -m py_compile verify_seven_leaf_switched_circulant_primitive_square_no_go.py audit_seven_leaf_switched_circulant_primitive_square_no_go.py
uv run --with ruff ruff check verify_seven_leaf_switched_circulant_primitive_square_no_go.py audit_seven_leaf_switched_circulant_primitive_square_no_go.py
```

The primary verifier derives (12) directly from cyclic-distance hafnians,
checks the selected Macaulay determinant at the trivial and primitive
characters, and verifies all 21 switching reductions.  The independent
standard-library audit reconstructs the symbols from cyclic combinatorics
and evaluates the determinant by fraction-free polynomial Bareiss
elimination without importing the primary script or project code.
