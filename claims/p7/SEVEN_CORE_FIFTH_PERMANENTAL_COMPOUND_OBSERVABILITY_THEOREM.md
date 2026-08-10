# Seven-core fifth permanental compound observability

## Status

**Exact generic theorem and fixed-rank certificate.**  For a `7 x 7` scalar
core--terminal incidence matrix `R`, the degree-five no-terminal-edge response
is the fifth permanental compound of `R` applied to the 21 core-edge weights.
This compound is generically invertible: at `R=I_7` it is exactly the
complement-index permutation matrix.

Consequently, when twenty mixed degree-five faces vanish and only one face is
free, an invertible compound forces the entire core-edge vector onto one
explicit inverse-column line.  Any already prescribed same-colour core edges
must satisfy two-by-two proportionality circuits against that line.

For the fixed mixed incidence matrix of the word

```text
sigma=(2,2,2,0,0,0,0),
```

the compound has full rank 21 over `Q(sqrt(21))`.  Two independent good-prime
certificates give nonzero determinants.  This note does not recompute the
existing four-face circuit; it supplies its general observability framework.

No support, word, graph-family, parameter, or minor search is used.

## 1. The fifth permanental compound

Let the core and terminal index sets both be

```text
Z=P={0,1,2,3,4,5,6}.                                  (1)
```

Let `E=binom(Z,2)` be the 21 core pairs and let `F=binom(P,5)` be the 21
five-terminal faces.  For a scalar `7 x 7` matrix `R`, define

```text
C_5^per(R)_(S,e)=per R[Z minus e,S],
S in F,                       e in E.                 (2)
```

The row labels are terminal five-sets and the column labels are deleted core
pairs.

Let `a=(A_e)_(e in E)` be the core-edge vector.  A degree-five matching uses
five core--terminal edges and exactly one core--core edge.  Splitting on that
edge gives

```text
Phi_S=sum_(e in E) per R[Z minus e,S] A_e,            (3)

Phi^(5)=C_5^per(R) a.                                 (4)
```

This is a one-edge Laplace decomposition, not a matching-support search.

## 2. Generic invertibility

### Theorem 1 (complement-index identity)

At the identity incidence matrix,

```text
C_5^per(I_7)_(S,e)=1 if S=Z minus e,
                    0 otherwise.                     (5)
```

Hence `C_5^per(I_7)` is the permutation matrix of the complement bijection

```text
binom(Z,2) -> binom(Z,5),              e |-> Z minus e. (6)
```

In particular,

```text
det C_5^per(I_7)=+/-1.                                (7)
```

Proof.  The submatrix `I_7[Z minus e,S]` has nonzero permanent exactly when
its row-index set equals its column-index set.  In that case it is an identity
matrix after the common ordering, and its permanent is one.

### Corollary 2 (generic degree-five observability)

The polynomial

```text
Delta_5(R)=det C_5^per(R)                             (8)
```

is not identically zero.  It is homogeneous of degree `5*21=105`.  On the
nonempty Zariski-open set `Delta_5(R)!=0`, the 21 degree-five faces determine
all 21 core-edge weights uniquely:

```text
a=C_5^per(R)^(-1) Phi^(5).                            (9)
```

Thus a generic seven-core incidence matrix has no degree-five invisible
core-edge direction.

## 3. One exceptional face forces one edge line

Let `S_*` be one exceptional five-terminal face.  In the `2+2+1` deletion
ledger,

```text
S_*=P minus Q,                    Q={a,b},             (10)
```

after relabelling the seven terminals as `1,2,3,4,5,a,b`.

Assume the other twenty mixed degree-five responses vanish while `Phi_(S_*)`
is free.  Then

```text
Phi^(5)=tau e_(S_*)                                  (11)
```

for some scalar `tau`.  If `C=C_5^per(R)` is invertible, put

```text
v=C^(-1)e_(S_*).                                     (12)
```

### Theorem 3 (exceptional-face line law)

Every compatible core-edge vector is on the line

```text
a=tau v.                                             (13)
```

Conversely, every vector on this line has all twenty prescribed faces zero.

This is immediate from (4) and invertibility.  If the exceptional face also
vanishes, then `tau=0` and every core edge vanishes.

## 4. Same-colour proportionality circuits

Suppose a set `E_0 subset E` of same-colour edge weights is already fixed:

```text
A_e=alpha_e,                       e in E_0.           (14)
```

Equation (13) gives the necessary circuits

```text
alpha_e v_f-alpha_f v_e=0,          e,f in E_0.       (15)
```

To avoid denominators, define

```text
w=adj(C)e_(S_*).                                      (16)
```

Then `v=w/det C`, and (15) is the polynomial circuit

```text
alpha_e w_f-alpha_f w_e=0.                            (17)
```

One must also impose

```text
w_e=0  =>  alpha_e=0.                                 (18)
```

Conditions (17)--(18) are sufficient for the fixed coordinates to lie on a
common scalar multiple of `w`: if some fixed `w_e` is nonzero, it fixes the
multiple and (17) fixes every other prescribed coordinate; if all fixed
`w_e` vanish, (18) forces all fixed `alpha_e` to vanish.

Thus an invertible fifth compound turns any prescribed same-colour data into
explicit two-by-two proportionality tests.  The fixed-chart four-face circuit
in
[`P7_221_FIXED_DIAGONAL_LIFT_DEGREE5_MIXED_CIRCUIT_OBSTRUCTION.md`](P7_221_FIXED_DIAGONAL_LIFT_DEGREE5_MIXED_CIRCUIT_OBSTRUCTION.md)
is a sparse projected obstruction for the current charts; it is not repeated
here.

## 5. Full rank of the fixed 2220000 incidence

Use terminal columns `(1,2,3,4,5,a,b)` and put `rho^2=21`.  The fixed
incidence matrix is

```text
R_sigma=
[ 0 0 0 0 1/7 0 0                    ]
[ 1 0 1 0 0   0 0                    ]
[ 0 1 0 1 0   0 0                    ]
[ 0 0 1 0 0   0 -rho                 ]
[ 0 0 0 1 0   0 -5-2rho/21           ]
[ 0 0 0 0 1   0 230+104rho/7         ]
[ 0 0 0 0 0   1 1+16rho/21           ].              (19)
```

### Theorem 4 (fixed-incidence full observability)

Over `Q(rho)`,

```text
rank C_5^per(R_sigma)=21.                             (20)
```

Proof.  Reduce the coefficient ring

```text
Z[1/21,rho]/(rho^2-21)
```

modulo 43 and send `rho` to 8.  This is legal because

```text
8^2=21 mod 43,                    21!=0 mod 43.
```

Exact modular permanent evaluation and elimination give

```text
det C_5^per(R_sigma)=11 mod 43.                       (21)
```

If the determinant were zero over `Q(rho)`, every good reduction would be
zero.  Equation (21) proves (20).

The independent audit uses the different good reduction

```text
rho -> 18 mod 101,                18^2=21 mod 101,
det C_5^per(R_sigma)=91 mod 101.                       (22)
```

Thus the fixed mixed word has no degree-five invisible edge direction: its
full 21-face response determines all 21 core edges.  With twenty prescribed
zeros, all edge freedom is the single exceptional-face line (12).

## Scope wall

Proved:

- the general fifth permanental compound formula;
- nonvanishing of its determinant polynomial;
- generic observability of all 21 core edges;
- the exceptional-face inverse-column law and adjugate proportionality
  circuits;
- full rank of the exact fixed `2220000` incidence compound.

Not proved here:

- the existing four-face fixed-chart obstruction, which is only cited;
- a universal obstruction for every scalar lift of the ledger;
- incompatibility after changing the fixed pure incidence matrix;
- a `P_7 -> Delta_3` obstruction or the Krenn--Gu conjecture.

## Replay

```powershell
uv run --with sympy python claims/p7/verify_seven_core_fifth_permanental_compound_observability.py
python claims/p7/audit_seven_core_fifth_permanental_compound_observability.py
uv run --with sympy --with ruff python -m ruff check claims/p7/verify_seven_core_fifth_permanental_compound_observability.py claims/p7/audit_seven_core_fifth_permanental_compound_observability.py
python -m py_compile claims/p7/verify_seven_core_fifth_permanental_compound_observability.py claims/p7/audit_seven_core_fifth_permanental_compound_observability.py
```

The primary verifier checks the complement-index identity, the line law, and
the fixed determinant `11 mod 43`.  The independent no-import audit rebuilds
the compound separately and obtains `91 mod 101`.  Both use fixed matrices,
orders, primes, and square roots; neither searches supports, graph families,
parameters, faces, or minors.
