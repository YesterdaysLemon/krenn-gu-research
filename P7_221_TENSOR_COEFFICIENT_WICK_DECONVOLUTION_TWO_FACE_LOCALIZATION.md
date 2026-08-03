# Tensor-coefficient Wick deconvolution localizes every mixed 2+2+1 word to two faces

## Status and corrected vertex roles

**Exact characteristic-zero tensor-coefficient localization theorem.**  Let

```text
Z={seven blocker/core vertices},
P={1,2,3,4,5,a,b},             Q={a,b}.               (1)
```

The vertices in `P` are roots and residual endpoints that survive or are
deleted in a cofactor.  Whenever they survive, their local modes are already
frozen at the chosen basepoint contractions.  Their terminal--terminal block

```text
M=(M_ij)_(i,j in P)                                  (2)
```

is therefore scalar.

The three colour charts, and all mixed-colour words, live on the seven
blocker/core vertices `Z`.  This distinction is essential: the common scalar
terminal theorem does **not** supply coloured local variables or
off-diagonal colour entries at vertices in `P`.

Put the scalar terminal-presence variables in the ordinary squarefree
algebra and retain the blocker tensor as its coefficient space.  Terminal
Wick multiplication is then an invertible scalar action on a tensor-valued
deletion cube.  For every mixed blocker word, the formal `2+2+1` ledger
vanishes on all 62 prescribed faces.  Only the unprescribed deletions `Q` and
`empty` remain.  Exact deconvolution shows that the no-terminal-edge core
response is supported on the same degree-five face and the degree-seven top
face; only the scalar edge `M_ab` shears the latter by the former.

Thus the mixed tensor synchronization problem is Wick-equivalent, word by
word, to a **two-face top residual**.  This is a localization theorem, not a
realization of that residual by one common seven-core graph.  P7 and the
Krenn--Gu conjecture remain unresolved.

## 1. Tensor-valued boundary response

For every blocker `z in Z`, let `E_z` be its local coefficient space and put

```text
T=bigotimes_(z in Z) E_z.                            (3)
```

Every surviving terminal in `P` is evaluated at its fixed scalar mode, while
the seven blocker legs remain open.  For an odd terminal set `S subset P`,
write

```text
H_(Z union S) in T                                   (4)
```

for the resulting blocker matching tensor.  Work in

```text
A=K[x_i:i in P]/(x_i^2:i in P)                       (5)
```

and define the tensor-valued odd boundary signature

```text
F=sum_(S subset P, |S| odd) H_(Z union S) x_S
  in T tensor A.                                     (6)
```

The scalar terminal Wick moment is

```text
E_M=sum_(S subset P, |S| even) haf(M[S])x_S
   =exp_A(sum_(i<j)M_ij x_i x_j).                    (7)
```

It is a unit with inverse `E_(-M)`.

Split every matching according to the edges having both endpoints in `P`.
The remaining matching uses no terminal--terminal edge.  Its tensor-valued
signature `Phi` satisfies

```text
F=E_M Phi,                 Phi=E_(-M)F.              (8)
```

This proof is coefficientwise in `T`; no multiplication of blocker tensors
is required.  Equivalently, (8) follows after applying every linear
functional in `T^*`.

## 2. The 62 prescribed faces

The cofactor indexed by an even deletion set `D subset P` is the coefficient
on the surviving terminal set:

```text
C_D=H_(Z union (P minus D)).                          (9)
```

The formal `2+2+1` ledger prescribes every deletion of sizes two, four, and
six, except `D=Q`.  Their number is

```text
(binom(7,2)-1)+binom(7,4)+binom(7,6)
=20+35+7=62.                                         (10)
```

Every prescribed `C_D` is a linear combination of the three monochromatic
blocker tensors.  Hence, for any mixed blocker word `sigma`,

```text
[sigma]C_D=0                                         (11)
```

on all 62 faces.

The two unprescribed even deletions are

```text
D=Q,                 surviving set P minus Q,
D=empty,             surviving set P.               (12)
```

Put

```text
alpha_sigma=[sigma]C_Q,
beta_sigma =[sigma]C_empty.                          (13)
```

Then the complete mixed-word scalar projection of (6) is

```text
F_sigma=[sigma]F
 =alpha_sigma x_(P minus Q)+beta_sigma x_P.          (14)
```

There are no hidden degree-one or degree-three terms: they are among the 62
prescribed zero faces.  Every other degree-five face is also prescribed and
zero.

## 3. Exact two-face deconvolution

### Theorem 1 (mixed-word two-face localization)

For every mixed blocker word `sigma`,

```text
Phi_sigma=[sigma]Phi
 =alpha_sigma x_(P minus Q)
  +(beta_sigma-M_ab alpha_sigma)x_P.                 (15)
```

Proof.  Apply `[sigma]` to (8); scalar Wick multiplication commutes with this
coefficient extraction.  Multiply (14) by `E_(-M)` in the squarefree
algebra.

The constant term of `E_(-M)` retains both displayed monomials.  A
nonconstant even monomial can multiply `x_(P minus Q)` only when all its
vertices lie in the complement `Q={a,b}`.  The only possibility is the edge
`ab`, whose coefficient in `E_(-M)` is `-M_ab`.  No nonconstant monomial can
multiply `x_P`.  Thus the only additional term is

```text
(-M_ab x_a x_b)(alpha_sigma x_(P minus Q))
=-M_ab alpha_sigma x_P,                              (16)
```

which proves (15).  The minus sign comes from `E_(-M)`, not from a Pfaffian
orientation.

### Corollary 2 (all lower mixed core faces vanish)

The no-terminal-edge core response `Phi_sigma` vanishes

```text
in degrees 1 and 3;
on all degree-5 faces except P minus Q.               (17)
```

Its entire possible support consists of the exceptional degree-five face
`P minus Q` and the degree-seven top face `P`.

### Corollary 3 (Wick-equivalent residual coordinates)

Define

```text
gamma_sigma=beta_sigma-M_ab alpha_sigma.             (18)
```

For every mixed word, terminal Wick deconvolution is the invertible shear

```text
(alpha_sigma,beta_sigma)
 <->(alpha_sigma,gamma_sigma),
beta_sigma=gamma_sigma+M_ab alpha_sigma.              (19)
```

Consequently the scalar terminal block creates no additional mixed-word
degrees of freedom and no further lower face.  It only changes the
degree-seven residual coordinate by the one edge `M_ab`.

For the common terminal certificate over `Q(rho)`,

```text
M_ab=1-rho,
gamma_sigma=beta_sigma+(rho-1)alpha_sigma.            (20)
```

## 4. What the theorem removes, and what it leaves

The common-terminal construction already proves that the three
monochromatic scalar charts admit the same `M`.  Theorem 1 says exactly what
that scalar synchronization does to the unknown mixed blocker words:

```text
mixed deletion cube
 --multiply by E_(-M)-->
no-terminal-edge mixed core response
 --support--> {P minus Q, P}.                         (21)
```

Thus terminal--terminal matching edges cannot be responsible for a hidden
mixed obstruction on a lower prescribed face.  Those faces vanish before
and after deconvolution.  Conversely, terminal Wick algebra alone cannot
exclude the remaining two-face residual, because `alpha_sigma,beta_sigma`
were not prescribed by the formal ledger.

A full tensor-valued graph must still realize all mixed residual pairs
`(alpha_sigma,gamma_sigma)` simultaneously using one common core--core and
core--terminal block system.  That is a structured seven-core realization
problem.  The present theorem neither solves it nor asserts that the free
coordinates may be chosen independently across words.

For the later fixed common-terminal scalar certificates, the degree-five
compound circuit in
`P7_221_FIXED_DIAGONAL_LIFT_DEGREE5_MIXED_CIRCUIT_OBSTRUCTION.md` proves that
no off-diagonal core completion solves that structured problem.  This does
not universalize the obstruction to other scalar lifts.

## 5. Why an ordinary cumulant adds nothing here

The signature `F` is tensor-valued and odd, with zero scalar constant term,
so `log F` is not defined.  Form instead the square-zero extension of `A` by
the `T tensor A` module, written `A plus epsilon(T tensor A)` with
`epsilon^2=0`.  There one may write

```text
G=E_M+epsilon F=E_M(1+epsilon Phi),
log G=Q_M+epsilon Phi.                                (22)
```

This is valid, but its marker-linear connected coefficient is exactly the
deconvolution (8).  Equations (15)--(19) therefore contain the full legal
cumulant information available from the current deletion cube.  No new
vanishing equation follows without a common-core realizability condition.

## Scope wall

Proved:

- scalar terminal Wick factorization with coefficients in the full blocker
  tensor space;
- exact identification of all 62 mixed prescribed faces as zero;
- two-face support of every mixed no-terminal-edge core response;
- the sign and value of the unique `M_ab` shear;
- equivalence of the mixed synchronization problem to a two-coordinate
  residual for each mixed blocker word.

Not proved:

- simultaneous realization of those residuals by one seven-core graph;
- independence or arbitrary assignability of different mixed-word residuals;
- cancellation of all mixed blocker words in one physical tensor graph;
- a P7 restriction or obstruction;
- the Krenn--Gu conjecture.

The theorem is a localization, and all realization/global claims remain
**UNKNOWN/UNRESOLVED**.

## Replay

```powershell
uv run --with sympy python verify_p7_221_tensor_coefficient_wick_deconvolution_two_face_localization.py
python audit_p7_221_tensor_coefficient_wick_deconvolution_two_face_localization.py
uv run --with sympy --with ruff python -m ruff check verify_p7_221_tensor_coefficient_wick_deconvolution_two_face_localization.py audit_p7_221_tensor_coefficient_wick_deconvolution_two_face_localization.py
python -m py_compile verify_p7_221_tensor_coefficient_wick_deconvolution_two_face_localization.py audit_p7_221_tensor_coefficient_wick_deconvolution_two_face_localization.py
```

The primary verifier checks the 62-face count, a generic symbolic scalar
terminal matrix, the exact squarefree inverse, and formula (15).  The
independent audit uses rational arithmetic and a separately implemented
hafnian recurrence.  Both are fixed seven-terminal algebra checks, not
support or graph-family searches.
