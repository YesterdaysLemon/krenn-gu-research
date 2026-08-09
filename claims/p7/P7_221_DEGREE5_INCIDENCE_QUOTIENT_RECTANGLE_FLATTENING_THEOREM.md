# Incidence quotients isolate one core edge in the full degree-five tensor map

## Status

**Exact conditional tensor obstruction, with a sharp quotient-level failure
model.**  This note treats the core--core tensors and core--terminal incidence
covectors as arbitrary.  It does not fix any of the existing scalar core
certificates, enumerate mixed colour words, or search supports.

The retained input is the exact common terminal block `M` from
`P7_221_COMMON_TERMINAL_BLOCK_SCALAR_HAFNIAN_REALIZABILITY.md`.  Wick
deconvolution of one four-face rectangle in the formal `2+2+1` ledger gives

```text
(rho-2)(D_0+D_1),                 rho^2=21,              (1)
```

where `D_c` is the pure colour-`c` tensor on all seven core modes.  For every
physical seven-core graph, a coordinate-free quotient by the terminal
incidence spans turns the same rectangle into a tensor of flattening rank at
most one.  Consequently (1) excludes a physical realization whenever one
pair of quotient modes keeps its two pure diagonal directions independent.

This is a genuine arbitrary-graph consequence, but it is conditional: the
independence need not hold.  A sparse exact model below shows that when it
fails, the projected formal rectangle can have rank one and can be reproduced
by a legal physical graph.  Thus the hypothesis is the exact boundary of this
particular quotient/flattening argument, not a disguised global proof.

## 1. The full degree-five map

Let the seven core modes be `V_i`, `i in Z`, and let the seven terminal labels
be

```text
P=(1,2,3,4,5,a,b).
```

Write

```text
A_ij in V_i^* tensor V_j^*,       R_i,p in V_i^*       (2)
```

for arbitrary core--core tensors and incidence covectors.  For a five-face
`S subset P`, `|S|=5`, the terminal-Wick-deconvolved response is

```text
T_S = sum_(i<j) A_ij tensor Per(R_(Z\{i,j}),S).          (3)
```

Here `Per(R_(Z\{i,j}),S)` is the tensor-valued permanent: sum over bijections
from the five remaining core modes to the five terminal columns, taking the
ordered tensor product of the corresponding `R_k,p`.  Formula (3) is simply
the matching partition according to the unique core--core edge in a matching
of seven core vertices against five surviving terminals.

For a terminal functional `lambda=sum_S lambda_S[S]`, put

```text
T_lambda = sum_S lambda_S T_S.                          (4)
```

No basis or colour chart is involved in (2)--(4).

There are `binom(7,5)=21` such five-faces.  The formal ledger prescribes the
twenty except `S=12345` (equivalently, except the deletion face `ab`).  The
argument below uses only four of the prescribed twenty, so the free face
never enters.

## 2. The exact formal rectangle

Let

```text
lambda = [125ab]-[145ab]-[235ab]+[345ab].               (5)
```

Using the common terminal block `M`, write `F_c(T)` for the formal cofactor
whose surviving terminal set is the odd set `T`.  Wick inversion on a
five-set is

```text
Phi_c(S) = sum_(E subset S, |E| even)
             haf((-M)[E]) F_c(S\E).                    (6)
```

All terms in (6) use surviving sets of sizes `5,3,1`, hence prescribed
cofactor faces.  Direct exact reduction in `Q(rho)`, `rho^2=21`, gives

```text
Phi_125ab = (rho-2, 0, (1+rho)/7),
Phi_145ab = (0,     0, (1+rho)/7),
Phi_235ab = (0,     0, (1+rho)/7),
Phi_345ab = (0, rho-2, (1+rho)/7).                      (7)
```

Thus the colour-2 coordinate cancels in (5), while colours 0 and 1 remain:

```text
Phi_lambda = (rho-2, rho-2, 0).                         (8)
```

If `epsilon_i^c in V_i^*` denotes the prescribed pure colour covector, (8)
is the tensor (1), with

```text
D_c = tensor_(i in Z) epsilon_i^c.                      (9)
```

## 3. Incidence-quotient isolation

For each core mode define its terminal incidence span and quotient

```text
U_i = span{R_i,p : p in P} subset V_i^*,
Q_i = V_i^*/U_i,                 pi_i:V_i^* -> Q_i.     (10)
```

### Lemma 1 (one-edge isolation)

For every pair `i<j` and every terminal functional `lambda`,

```text
(pi_i tensor pi_j tensor id) T_lambda
  = bar(A)_ij tensor B_ij(lambda),                      (11)

bar(A)_ij=(pi_i tensor pi_j)A_ij,                       (12)
```

for a tensor `B_ij(lambda)` on the other five core modes.  In particular,
the flattening of (11) across

```text
{i,j} | Z\{i,j}                                        (13)
```

has rank at most one.

### Proof

Consider a summand of (3) indexed by a core edge `{k,l}`.  If
`{k,l}!={i,j}`, at least one of `i,j` is among the five terminal-matched core
modes.  That mode contributes some incidence covector `R_i,p in U_i` or
`R_j,p in U_j`, which is killed by its quotient map.  Only the `{i,j}`
summand survives, and it is exactly the separated tensor in (11).  Linearity
gives the claim for (4).  This proof neither expands a mixed word nor assumes
anything about the values or ranks of the `A` and `R` tensors.

## 4. The conditional rectangle obstruction

Projecting (1) at modes `i,j` gives

```text
(rho-2)(a_0 tensor b_0 + a_1 tensor b_1),               (14)

a_c = pi_i(epsilon_i^c) tensor pi_j(epsilon_j^c),
b_c = tensor_(k notin {i,j}) epsilon_k^c.               (15)
```

The two right factors `b_0,b_1` are linearly independent, and `rho-2` is
nonzero.  Therefore the flattening rank of (14) is exactly

```text
dim span{a_0,a_1}.                                      (16)
```

### Theorem 2 (incidence-quotient rectangle obstruction)

If, for at least one core pair `i<j`,

```text
pi_i(epsilon_i^0) tensor pi_j(epsilon_j^0),
pi_i(epsilon_i^1) tensor pi_j(epsilon_j^1)              (17)
```

are linearly independent, then no physical seven-core graph with the common
terminal block `M` realizes the formal tensor cofactor ledger.

Indeed, (16) makes the formal flattening rank two, whereas Lemma 1 makes every
physical flattening rank at most one.

Equivalently, any physical realization must satisfy the coordinate-free
necessary condition

```text
dim span{
  pi_i(epsilon_i^0) tensor pi_j(epsilon_j^0),
  pi_i(epsilon_i^1) tensor pi_j(epsilon_j^1)
} <= 1                                                     (18)
```

for every pair `i<j`.  Condition (18), rather than quotient dimension alone,
is the useful next local-to-global constraint.

## 5. Sharp failure model

The nondegeneracy in (17) cannot be deleted from this argument.  Fix a pair
`i,j` and choose

```text
U_i=span{epsilon_i^0},             U_j=0.               (19)
```

Then `dim Q_i=2`, `dim Q_j=3`, but `a_0=0` and `a_1!=0`; the projected formal
rectangle (14) has rank one.

This rank-one target is attained by a legal sparse physical graph.  Use only
the core edge `A_ij`, with `bar(A)_ij=a_1`.  On the other five core modes
`k_1,...,k_5`, take the only nonzero incidence entries to be

```text
R_k1,1=(rho-2) epsilon_k1^1,
R_k2,2=          epsilon_k2^1,
R_k3,5=          epsilon_k3^1,
R_k4,a=          epsilon_k4^1,
R_k5,b=          epsilon_k5^1.                          (20)
```

Then

```text
Per(125ab)=rho-2,
Per(145ab)=Per(235ab)=Per(345ab)=0.                     (21)
```

Add, if desired, one unused incidence covector `R_i,p=epsilon_i^0` to realize
the span in (19), and take all incidences at `j` to be zero.  Equations
(20)--(21) make the physical projected rectangle exactly

```text
(rho-2) a_1 tensor b_1,                                (22)
```

which is also the projection of (14).  This is a countermodel to the
quotient-rank inference when (17) fails.  It is **not** a realization of the
other ledger faces.

## Scope wall

Proved:

- the full tensor degree-five formula (3) has a universal one-edge quotient;
- every physical rectangle has quotient flattening rank at most one;
- the formal rectangle has rank two under the exact hypothesis (17);
- failure of (17) admits an exact projected rank-one physical countermodel.

Not proved:

- that some pair must satisfy (17) for every possible incidence family;
- a realization or obstruction for all faces when every pair is degenerate;
- independence from the common terminal block `M` used for Wick inversion;
- the `P_7 -> Delta_3` restriction or the global Krenn--Gu conjecture.

The resulting frontier is

```text
arbitrary A_ij and R_i,p + one nondegenerate quotient pair: EXCLUDED;
all quotient pairs degenerate as in (18):                  UNKNOWN;
global Krenn--Gu:                                           UNRESOLVED. (23)
```

## Replay

```powershell
uv run --with sympy python verify_p7_221_degree5_incidence_quotient_rectangle_flattening.py
python audit_p7_221_degree5_incidence_quotient_rectangle_flattening.py
python -m py_compile verify_p7_221_degree5_incidence_quotient_rectangle_flattening.py audit_p7_221_degree5_incidence_quotient_rectangle_flattening.py
uv run --with ruff ruff check verify_p7_221_degree5_incidence_quotient_rectangle_flattening.py audit_p7_221_degree5_incidence_quotient_rectangle_flattening.py
```

The primary replay reconstructs (7) from the formal ledger and common `M`,
checks the rank-two and rank-one flattenings, and verifies the sparse
permanents (21).  The independent audit uses hand-written `Q(sqrt(21))`
arithmetic and imports neither SymPy nor the primary verifier.  Neither replay
enumerates graph families, colour words, alignments, or face systems.
