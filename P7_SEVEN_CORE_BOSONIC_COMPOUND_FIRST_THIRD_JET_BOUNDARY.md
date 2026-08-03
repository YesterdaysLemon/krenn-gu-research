# Seven-core bosonic compounds: the first/third-jet boundary

## Status

**Exact compound formula, differential identity, and dominance theorem.**  For
one seven-core graph with scalar terminal-presence variables, the no-terminal-
edge response is governed by bosonic hafnian compounds.  Its degree-three
response is a directional derivative of its degree-one response with respect
to the core block.  This is a first-jet relation, not a pointwise equation.

More strongly, the scalar map from a symmetric seven-core block and seven
terminal columns to the combined degree-one and degree-three response is
dominant in characteristic zero.  Consequently there is no nonzero universal
polynomial relation among those `7+35=42` scalar response coordinates.

Applied to the correctly Wick-deconvolved formal `2+2+1` ledger, this rules
out a scalar rank, apolar, or compound identity using only degrees one and
three as a possible obstruction.  A formal common-core model exists over the
three-idempotent algebra by combining the already verified scalar colour
charts.  That model is not a physical tensor graph: orthogonal global colour
idempotents suppress precisely the mixed blocker words that remain nonzero in
the physical local tensor algebra.

This result deliberately stops before degree five.  A fixed-chart
degree-five compound selector uses additional pure-chart information and is
a separate, stronger test; it is neither implied nor contradicted by the
degree-one/degree-three dominance statement here.  That test is packaged in
[`P7_221_FIXED_DIAGONAL_LIFT_DEGREE5_MIXED_CIRCUIT_OBSTRUCTION.md`](P7_221_FIXED_DIAGONAL_LIFT_DEGREE5_MIXED_CIRCUIT_OBSTRUCTION.md).

No word, support, graph-family, or parameter enumeration is used.  The
dominance certificate is one fixed Jacobian minor at one displayed point.

## 1. General seven-core compound formula

Let `Z={0,...,6}` be the core vertices and `P={0,...,6}` the terminal labels.
Work in the squarefree terminal algebra

```text
S=K[x_p:p in P]/(x_p^2:p in P).                       (1)
```

At core vertex `i`, let

```text
L_i=sum_p ell_(i,p) x_p                               (2)
```

be its terminal-incidence form.  The coefficients may be scalars, or may
carry the local core covector at vertex `i`.  Let `A=(A_ij)` be the symmetric
zero-diagonal core--core block.  For `S subset Z`, put

```text
h_S(A)=haf A[Z minus S].                               (3)
```

It is zero when `|Z minus S|` is odd.

### Theorem 1 (bosonic compound expansion)

The no-terminal-edge response is

```text
Phi=sum_(k odd) Phi^(k),

Phi^(k)=sum_(S subset Z, |S|=k) h_S(A) product_(i in S) L_i. (4)
```

Proof.  In a matching contributing to terminal degree `k`, let `S` be the
core vertices matched to terminals.  The other core vertices are matched
internally and contribute `haf A[Z minus S]`; the selected terminal edges
contribute `product L_i`.  Summing over `S` proves (4).

For a terminal singleton `p` and a terminal triple `T={p,q,r}`, coefficient
extraction gives

```text
Phi_p=sum_i h_{i}(A) ell_(i,p),                        (5)

Phi_T=sum_(|S|=3) h_S(A) per L[S,T].                  (6)
```

The permanent, rather than a determinant, is the bosonic compound.

## 2. The exact first/third differential coupling

For distinct terminals `q,r`, define a symmetric rank-at-most-two direction
in core-block space by

```text
B^(qr)_ij=ell_(i,q)ell_(j,r)+ell_(i,r)ell_(j,q).       (7)
```

### Theorem 2 (bosonic insertion derivative)

For pairwise distinct `p,q,r`,

```text
Phi_(pqr)=D_(B^(qr)) Phi_p.                            (8)
```

Here the derivative varies `A` and holds `L` fixed.

Proof.  Principal hafnians obey

```text
partial h_i / partial A_jk = h_{ijk}                  (9)
```

when `i,j,k` are distinct, and the derivative is zero otherwise.  Therefore

```text
D_(B^(qr)) Phi_p
 =sum_i sum_(j<k; j,k!=i)
   h_{ijk} ell_(i,p)
   (ell_(j,q)ell_(k,r)+ell_(j,r)ell_(k,q)).            (10)
```

For each three-set `{i,j,k}`, its six terms are exactly
`h_{ijk} per L[{i,j,k},{p,q,r}]`, proving (8).

Equation (8) explains an important logical point.  A response can satisfy

```text
Phi_p(A)=0,                    Phi_(pqr)(A)!=0,         (11)
```

because the second value is a directional derivative at the zero, not a
multiple or contraction of the value.

## 3. Scalar first/third compounds have no polynomial equation

Take scalar `A` and a scalar `7 x 7` matrix `L`.  Define the polynomial map

```text
Psi:(A,L) |-> ((Phi_p)_p, (Phi_T)_(|T|=3))
             in K^7 direct-sum K^35.                  (12)
```

The domain has `21+49=70` coordinates.

### Theorem 3 (dominance)

Over every characteristic-zero field, `Psi` is dominant.  Equivalently, its
42 coordinate functions are algebraically independent.  Hence no nonzero
polynomial in the degree-one and degree-three scalar response coordinates
vanishes for every seven-core graph.

Proof.  Order the 21 core edges lexicographically and flatten the 49 entries
of `L` row-major.  For parameter index `k=0,...,69`, put

```text
q(k)=((k^2+3k+7) mod 11)-5.                            (13)
```

Assign the first 21 values to `A` and the next 49 to `L`.  Order response
rows by the seven singletons and then the 35 triples lexicographically.
In the `42 x 70` Jacobian, take all core-edge columns and the `L` columns
whose row-major indices are

```text
0,...,12, 14,...,19, 21,22.                            (14)
```

This is a `42 x 42` integer minor.  Exact elimination gives

```text
det minor = 81 mod 101.                                (15)
```

Thus its integer determinant is nonzero.  The differential of `Psi` is
surjective at (13), which proves dominance in characteristic zero.

The replay derives every Jacobian entry from (5)--(6), using

```text
partial h_S / partial A_uv = h_(S union {u,v})         (16)
```

when `u,v` are outside `S`.  It does not search for a graph or a minor.

### Corollary 4 (no scalar low-jet obstruction)

No universal scalar determinantal, apolar, catalecticant, or compound
polynomial involving only `Phi^(1)` and `Phi^(3)` can exclude a proposed
ledger point.  Such a polynomial would vanish on the image of `Psi`, hence
on its Zariski closure, which is the whole 42-dimensional response space.

This does not say that every response point has a scalar preimage; dominance
removes universal polynomial equations, not exceptional constructible
conditions.

## 4. Correct Wick deconvolution of the 2+2+1 ledger

Return to terminal labels

```text
P={1,2,3,4,5,a,b}.                                    (17)
```

Let `F_T` be the tensor coefficient on surviving terminal set `T`, and let
`M` be the common scalar terminal block.  Squarefree Wick deconvolution gives

```text
Phi_T=F_T-sum_({i,j} subset T) M_ij F_(T minus {i,j}) (18)
```

in degree three, because the only lower odd degree is one.  The ledger gives

```text
Phi_5=(1/7)D_2,             Phi_p=0 for p!=5.         (19)
```

Put

```text
rho^2=21,                   kappa=1+22/rho.           (20)
```

The nonzero degree-three coefficients after (18) are exactly

```text
Phi_123 =D_0,                  Phi_12a=D_0,
Phi_234 =D_1,                  Phi_34b=D_1,

Phi_125 =D_0+(kappa/7)D_2,
Phi_145 =(kappa/7)D_2,         Phi_235=(kappa/7)D_2,
Phi_345 =D_1+(kappa/7)D_2,

Phi_15b=Phi_25a=Phi_35b=Phi_45a=Phi_5ab=(rho/7)D_2.   (21)
```

All other degree-three coefficients vanish.  In particular, every displayed
coefficient remains in the diagonal span `<D_0,D_1,D_2>`.

The pattern does not violate Theorem 2.  For example,

```text
Phi_1=0,                       Phi_123=D_0,            (22)
```

is a zero value with a nonzero derivative in the direction `B^(23)`.

## 5. Formal common-core sharpness and the physical boundary

Let

```text
E=K epsilon_0 direct-sum K epsilon_1 direct-sum K epsilon_2,
epsilon_c epsilon_d=delta_(cd) epsilon_c.             (23)
```

The previously verified common-terminal theorem supplies, for each colour
`c`, one scalar seven-core pair `(A^(c),L^(c))` behind the same terminal
matrix `M`.  Form one `E`-valued common block

```text
A=sum_c epsilon_c A^(c),             L=sum_c epsilon_c L^(c). (24)
```

Hafnians and the compound formula are polynomial, so multiplication in (23)
gives componentwise

```text
Phi_E=sum_c epsilon_c Phi^(c).                         (25)
```

Identifying the vector basis `epsilon_c` with the diagonal tensors `D_c`
realizes the complete deconvolved scalar ledger, including (19)--(21), by one
formal common core.  This is a genuine sharpness model for every bosonic
compound identity valid over arbitrary commutative coefficient algebras.

It is not a physical graph.  In the physical blocker algebra, choosing colour
`c` on one edge and colour `d` on another produces a nonzero mixed local word;
there are no global orthogonal idempotents making that product zero.  Passing
from (23) to the physical vertexwise tensor algebra is exactly the unresolved
synchronization problem.

## Scope wall

Proved:

- the general seven-core bosonic compound formula;
- the exact first/third insertion-derivative identity;
- dominance of the scalar degree-one/degree-three response map;
- the corrected deconvolved ledger through degree three;
- a formal common-core realization over the global idempotent algebra.

Not proved:

- a common core over the physical local-colour tensor algebra;
- cancellation of mixed blocker words;
- any degree-five or degree-seven physical compatibility claim in this note;
- a `P_7 -> Delta_3` restriction or obstruction;
- the Krenn--Gu conjecture.

The exact boundary is

```text
scalar degrees 1+3:             no universal polynomial obstruction;
formal idempotent common core:  realized;
physical tensor common core:    unresolved.            (26)
```

## Replay

```powershell
uv run --with sympy python verify_p7_seven_core_bosonic_compound_first_third_jet_boundary.py
python audit_p7_seven_core_bosonic_compound_first_third_jet_boundary.py
uv run --with sympy --with ruff python -m ruff check verify_p7_seven_core_bosonic_compound_first_third_jet_boundary.py audit_p7_seven_core_bosonic_compound_first_third_jet_boundary.py
python -m py_compile verify_p7_seven_core_bosonic_compound_first_third_jet_boundary.py audit_p7_seven_core_bosonic_compound_first_third_jet_boundary.py
```

The primary verifier checks the deconvolution ledger, the local symbolic
derivative identity, and the fixed Jacobian minor `81 mod 101`.  The
independent no-import audit repeats the ledger over exact scaled quadratic
coefficients and certifies the same fixed minor as `833 mod 1009`.  Neither
replay searches graph supports, words, or parameter families.
