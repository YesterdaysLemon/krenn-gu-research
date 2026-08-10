# A degree-five mixed circuit obstructs every core-edge completion of the fixed 2+2+1 charts

## Status

**Exact obstruction for the current scalar certificates, not a universal
ledger obstruction.**  Fix the three common-terminal scalar graphs from
`P7_221_COMMON_TERMINAL_BLOCK_SCALAR_HAFNIAN_REALIZABILITY.md`, identify their
seven cores indexwise as in
`P7_221_DIAGONAL_BLOCK_GLUING_AND_MIXED_WORD_BOUNDARY.md`, and keep all
same-colour core edges and frozen core--terminal incidences unchanged.

For the mixed core word

```text
sigma=(2,2,2,0,0,0,0),                                (1)
```

allow every one of the twelve cross-colour core--core entries to be an
arbitrary scalar.  Four degree-five no-terminal-edge responses satisfy the
parameter-independent circuit

```text
Phi_125ab-Phi_145ab-Phi_235ab+Phi_345ab
  =2(805+52 rho)/49 !=0,          rho^2=21.            (2)
```

The four faces correspond to deletions `34,23,14,12`.  The formal ledger is
pure-colour, so its coefficient at the mixed word (1) vanishes on all four
faces and on every lower face entering their Wick quotients.  Hence all four
`Phi` values would have to vanish, contradicting (2).

Therefore **no choice of the twelve off-diagonal core-colour entries completes
these fixed pure scalar graphs to the tensor ledger**.  Another set of scalar
principal-hafnian realizations of the same ledger could have different
same-colour core and incidence data and is not excluded.

The later theorem
`P7_221_ARBITRARY_ALIGNMENT_DEGREE5_RECTANGLE_OBSTRUCTION.md` shows that the
same rectangle, with an alignment-adapted mixed word, excludes every core
alignment of these fixed colour-0/colour-2 charts.  Different scalar
realizations remain open.

## 1. The fixed mixed-word incidence matrix

Use the canonical core identifications

```text
colour 0:
(f_1,f_2,ell,h_3,h_4,h_5,h_a) -> (z_0,...,z_6),

colour 2:
(z_*,z_1,z_2,z_3,z_4,z_5,z_6) -> (z_0,...,z_6).       (3)
```

At core vertices `z_0,z_1,z_2` evaluate the frozen incidence in colour 2;
at `z_3,z_4,z_5,z_6` evaluate it in colour 0.  With terminal columns ordered

```text
(1,2,3,4,5,a,b),                                      (4)
```

the resulting `7 x 7` incidence matrix is

```text
R_sigma=
[ 0 0 0 0 1/7 0 0                    ]
[ 1 0 1 0 0   0 0                    ]
[ 0 1 0 1 0   0 0                    ]
[ 0 0 1 0 0   0 -rho                 ]
[ 0 0 0 1 0   0 -5-2rho/21           ]
[ 0 0 0 0 1   0 230+104rho/7         ]
[ 0 0 0 0 0   1 1+16rho/21           ].              (5)
```

The fixed same-colour core edges are

```text
A_12=1,
A_35=rho,
A_45=-6-1/rho,
A_46=1/rho,
A_56=1+22/rho,                                        (6)
```

and all other edges internal to `{0,1,2}` or `{3,4,5,6}` vanish.  Put

```text
A_ij=x_ij,       i in {0,1,2}, j in {3,4,5,6}.        (7)
```

These are all twelve possible cross-colour core entries.  No restriction is
placed on them.

## 2. The exact degree-five response formula

Let `S` be a five-subset of the terminals.  After Wick-deconvolving the fixed
terminal block, terminal--terminal matching edges are absent.  A perfect
matching on the seven cores and five surviving terminals must therefore
match five distinct cores to the five terminals and use exactly one
core--core edge on the two remaining cores.  Splitting on that edge gives

```text
Phi_S=sum_(0<=i<j<=6)
        A_ij per R_sigma[Z\{i,j},S].                   (8)
```

Thus every degree-five coefficient is linear in the core edges.  Equation
(8) is a one-edge Laplace decomposition, not an enumeration of graphs or
candidate supports.

For compactness put

```text
L=(-5-2rho/21)x_03-rho x_04,
U=230/7+104rho/49,
V=-5/7-2rho/147.                                      (9)
```

Direct evaluation of the four `5 x 5` permanents in (8) gives

```text
Phi_125ab = L-1/7+rho/7,                               (10)

Phi_145ab = L+U x_23-(rho/7)x_25-1/7+rho/7,           (11)

Phi_235ab = L+U x_14+V x_15-1/7+rho/7,                (12)

Phi_345ab = L+U(x_14+x_23)+V x_15-(rho/7)x_25
             +229/7+111rho/49.                        (13)
```

The six cross variables not displayed in (10)--(13) have coefficient zero
on each of these faces.  The other six cancel in the alternating sum.
Consequently

```text
Phi_125ab-Phi_145ab-Phi_235ab+Phi_345ab
 =230/7+104rho/49
 =2(805+52rho)/49.                                    (14)
```

This constant is nonzero in `Q(rho)` because

```text
805^2-21*52^2=591241 !=0.                              (15)
```

## 3. Why the four Wick faces must be zero

Let `F_T^sigma` be the full frozen-terminal cofactor coefficient at the mixed
core word (1), before removing terminal--terminal edges.  The prescribed
cofactor tensors are pure colour 0, 1, or 2.  Hence

```text
F_T^sigma=0                                            (16)
```

for every prescribed surviving terminal set `T` of size one, three, or five.

The common terminal block acts only on terminal variables.  Its exact
squarefree Wick relation is

```text
F=E_M Phi,             Phi=E_(-M) F.                  (17)
```

For a five-set `S`, the coefficient `Phi_S^sigma` is a linear combination of
`F_T^sigma` with `T subset S` and `|T|=5,3,1`.  All those deletion faces have
sizes two, four, and six and are prescribed in the formal ledger.  Equation
(16) therefore implies

```text
Phi_S^sigma=0                                          (18)
```

for each of the four sets in (10)--(13).  Their complements are

```text
P\125ab=34,       P\145ab=23,
P\235ab=14,       P\345ab=12.                        (19)
```

Equations (14), (18), and (19) prove the obstruction.

### Theorem 1 (fixed-chart off-diagonal core completion obstruction)

Keep the exact colour-0, colour-1, and colour-2 scalar certificates, their
indexwise core identification (3), their common terminal block, every pure
core--core diagonal entry, and every frozen core--terminal incidence.  Then
no assignment of the twelve cross-colour core entries (7) makes the resulting
block graph realize the formal tensor cofactor ledger.

Proof.  Any such assignment would make all four mixed Wick coefficients in
(10)--(13) zero by (16)--(19), but their alternating sum is the nonzero
constant (14).

## 4. Sharp boundary

The theorem closes all core--core off-diagonal freedom for **these particular
pure scalar lifts** and the single mixed word (1).  It is stronger than the
earlier observation that the zero off-diagonal lift has one bad mixed
coefficient: arbitrary values of all twelve relevant cross entries cannot
repair the four faces simultaneously.

It does not prove any of the following:

- that every scalar realization of the formal ledger has the circuit (14);
- that changing the pure core--core or core--terminal realization cannot
  remove the circuit;
- that additional tangent-jet compatibility is impossible;
- a universal tensor-valued `P_7` obstruction; or
- the Krenn--Gu conjecture.

The exact status is

```text
current pure scalar certificates:                    REALIZED;
their common frozen terminal block:                  REALIZED;
arbitrary cross-core completion of these charts:     EXCLUDED;
other pure scalar lifts with cancellable mixed words: UNKNOWN;
full P7 restriction and global Krenn--Gu:             UNRESOLVED. (20)
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_221_fixed_diagonal_lift_degree5_mixed_circuit_obstruction.py
python claims/p7/audit_p7_221_fixed_diagonal_lift_degree5_mixed_circuit_obstruction.py
python -m py_compile claims/p7/verify_p7_221_fixed_diagonal_lift_degree5_mixed_circuit_obstruction.py claims/p7/audit_p7_221_fixed_diagonal_lift_degree5_mixed_circuit_obstruction.py
uv run --with ruff ruff check claims/p7/verify_p7_221_fixed_diagonal_lift_degree5_mixed_circuit_obstruction.py claims/p7/audit_p7_221_fixed_diagonal_lift_degree5_mixed_circuit_obstruction.py
```

The primary verifier reconstructs (5)--(7), computes only the four permanent
responses in (10)--(13), differentiates their circuit with respect to all
twelve variables, and checks (14)--(15) exactly in SymPy.  The independent
audit imports neither SymPy nor any project verifier; it repeats the four
calculations using rational-pair arithmetic in
`Q[rho]/(rho^2-21)` and an affine twelve-variable coefficient vector.
Neither replay searches parameters, supports, graph families, or deletion
subsets.
