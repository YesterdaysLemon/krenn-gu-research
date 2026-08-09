# Diagonal block gluing solves pure-chart coexistence for the 2+2+1 ledger

## Status

**Exact frozen-terminal gluing theorem and explicit mixed-word boundary.**
The three scalar principal-hafnian graphs for the formal 2+2+1 ledger already
define one honest seven-core bilinear block graph on their pure colour charts.
The only scalar datum that had to agree across those charts was the
terminal--terminal restriction, and
`P7_221_COMMON_TERMINAL_BLOCK_SCALAR_HAFNIAN_REALIZABILITY.md` supplies
exactly that agreement.

There is no additional requirement that the three scalar core--core matrices
be equal.  A physical core--core edge is a `3 x 3` bilinear block; its three
diagonal evaluations are independent entries of that one block.  Likewise,
one core--terminal block can interpolate the three scalar incidence values.

This correction does not solve the tensor problem.  The diagonal lift has an
explicit nonzero mixed blocker-colour coefficient equal to `1/7`.  This note
by itself only excludes the naive diagonal lift.  The later degree-five
four-face circuit proves that no choice of its off-diagonal core entries can
repair these fixed pure certificates; other scalar lifts remain open.

## 1. Fixed-terminal scalar charts

Let `Z={z_0,...,z_6}` be the seven core vertices and let

```text
P={1,2,3,4,5,a,b}                                      (1)
```

be the deletion-labelled terminal vertices.  Give every core space `V_z` a
colour basis

```text
e_z^0,e_z^1,e_z^2                                      (2)
```

with dual basis `alpha_z^0,alpha_z^1,alpha_z^2`.  At every terminal `p`, fix
the nonzero vector `v_p` used in the cofactor restriction and choose a
covector

```text
eta_p(v_p)=1.                                          (3)
```

Suppose scalar chart `c` is a weighted graph on `Z union P` with block
decomposition

```text
A_c(z,z')       on Z x Z,
R_c(z,p)        on Z x P,
M_c(p,q)        on P x P.                              (4)
```

For an even deletion set `D subset P`, its chartwise cofactor is

```text
C_D^(c)=haf W_c[Z union (P\D)].                        (5)
```

The terminal vectors in (3) are fixed while the core chart changes.
Therefore one physical terminal edge has only the single frozen evaluation

```text
B_pq(v_p,v_q).                                         (6)
```

This is why agreement of the scalar terminal matrices is a real gluing
condition, whereas agreement of the scalar core matrices is not.

## 2. The diagonal block gluing theorem

Assume

```text
M_0=M_1=M_2=M.                                         (7)
```

Define one family of physical bilinear edge blocks by

```text
B_zz' = sum_(c=0)^2 A_c(z,z') alpha_z^c tensor alpha_z'^c,

B_zp  = sum_(c=0)^2 R_c(z,p) alpha_z^c tensor eta_p,

B_pq  = M(p,q) eta_p tensor eta_q.                     (8)
```

Use transpose blocks in the reverse orientations.  These are ordinary
bilinear forms on the physical local spaces, not formal chart labels.

### Theorem 1 (fixed-terminal diagonal gluing)

For every colour `c`, every deletion set `D`, and every perfect matching of
`Z union (P\D)`, evaluating all core inputs at `e_z^c` and all surviving
terminal inputs at `v_p` gives exactly the corresponding scalar chart-`c`
matching weight.  Consequently

```text
T_(B,D)(e_z^c : z in Z; v_p : p in P\D)=C_D^(c).       (9)
```

Proof.  Each possible edge evaluates as

```text
B_zz'(e_z^c,e_z'^c)=A_c(z,z'),
B_zp(e_z^c,v_p)=R_c(z,p),
B_pq(v_p,v_q)=M(p,q).                                  (10)
```

Thus (10) identifies the weight of every physical matching term with the
weight of the same matching in scalar graph `c`.  Summing term by term gives
(9).

Conversely, any one physical block graph evaluated at the fixed terminal
vectors has the chart-independent value (6).  Hence, within this unrestricted
frozen-terminal cofactor layer, equality (7) is necessary and sufficient for
edgewise coexistence of arbitrary scalar core and incidence charts.

This is a pure-chart theorem.  It makes no assertion about a core assignment
that uses more than one colour.

## 3. Application to the exact 2+2+1 graphs

Put the three exact common-terminal graphs on one labelled core set by the
indexwise identifications

```text
colour 0 and 1:
(f_1,f_2,ell,h_3,h_4,h_5,h_a) -> (z_0,...,z_6),

colour 2:
(z_*,z_1,z_2,z_3,z_4,z_5,z_6) -> (z_0,...,z_6).       (11)
```

All three terminal restrictions are the exact matrix over
`Q(rho)`, `rho^2=21`, given by

```text
M_12=M_14=M_23=M_34=-(1+22/rho),
M_13=M_24=M_1a=M_3a=M_2b=M_4b=7,
M_1b=M_2a=M_3b=M_4a=-rho,
M_ab=1-rho,                                            (12)
```

with every edge involving terminal `5` equal to zero.  Take `A_c,R_c` from
the three explicit scalar certificates and insert them in (8).

### Corollary 2 (one block graph for all pure ledger charts)

The blocks (8), (11), and (12) form one seven-core/seven-terminal physical
bilinear graph whose three pure core-colour evaluations reproduce all 186
prescribed scalar cofactors of the formal 2+2+1 ledger.  They also reproduce
the six selected free values

```text
c=0: C_Q=0,       C_empty=155+110 rho/7,
c=1: C_Q=0,       C_empty=155+110 rho/7,
c=2: C_Q=103/147, C_empty=103/147+36 rho.             (13)
```

Thus the phrase “common tensor-valued core data” does not describe a further
pure-chart synchronization condition: (8) supplies those data immediately.
The remaining coupling begins only when mixed core colours are evaluated.

## 4. An exact forbidden mixed word in the diagonal lift

The construction (8) deliberately sets every off-diagonal core colour entry
to zero.  It does not cancel all mixed words.

Delete

```text
D={1,2,3,4,a,b},                                       (14)
```

so only terminal `5` survives, and assign core colours

```text
(colour(z_0),...,colour(z_6))=(2,2,2,0,0,0,0).         (15)
```

In the indexwise gluing (11), the relevant scalar factors are

```text
R_2(z_0,5)=1/7,
A_2(z_1,z_2)=1,
haf A_0[{z_3,z_4,z_5,z_6}]
  =A_0(z_3,z_5) A_0(z_4,z_6)
  =rho*(1/rho)=1.                                      (16)
```

Core--core edges between different colours vanish in the diagonal lift.
The factorization in (16) is therefore the unique nonzero matching class for
(14)--(15), and its coefficient is

```text
1/7.                                                    (17)
```

But the prescribed cofactor at (14) is

```text
C_D=(0,0,1/7),                                         (18)
```

meaning the pure colour-2 blocker word has coefficient `1/7` and every mixed
blocker word must vanish.  The assignment (15) is mixed, so (17) proves:

### Proposition 3 (the diagonal lift is not a GHZ cofactor realization)

The particular diagonal block graph (8) realizes every pure scalar chart but
does not realize the full tensor-valued formal ledger.

This is not a universal obstruction.  Entries

```text
B_zz'(e_z^c,e_z'^d),             c!=d,                 (19)
```

are completely invisible in all three pure charts and remain available to
create cancelling mixed matchings.  Proposition 3 does not show that no
choice of (19), or no more general block extension, can cancel (17) together
with every other mixed coefficient.

The later theorem
`P7_221_FIXED_DIAGONAL_LIFT_DEGREE5_MIXED_CIRCUIT_OBSTRUCTION.md` closes the
first possibility for these fixed charts: a four-face degree-five circuit
cancels all twelve relevant off-diagonal variables and remains nonzero.  It
The subsequent arbitrary-alignment rectangle theorem excludes every core
bijection of these fixed colour-0/colour-2 charts.  Neither theorem excludes
a different scalar realization of the same pure ledgers.

## 5. Exact scope

The theorem concerns the frozen-terminal principal-cofactor layer.  It
specifies the values of terminal blocks at `(v_p,v_q)` and of core--terminal
blocks at `(e_z^c,v_p)`.  If the same physical terminal blocks must also obey
additional tangent-jet restrictions away from the fixed vectors, their
simultaneous linear extension is a separate compatibility problem.  No such
extension theorem is claimed here.

The corrected status wall is

```text
three scalar principal-hafnian charts:          REALIZED;
one common frozen terminal matrix:              REALIZED;
one physical block graph on all pure charts:    REALIZED;
the canonical diagonal lift:                    FAILS A MIXED WORD;
off-diagonal core completion of these fixed charts: EXCLUDED LATER;
different pure scalar lift with mixed cancellation:  UNKNOWN;
full tangent-jet/block compatibility:           NOT PROVED HERE;
full P7 restriction and global Krenn--Gu:        UNRESOLVED. (20)
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_221_diagonal_block_gluing_and_mixed_word_boundary.py
python claims/p7/audit_p7_221_diagonal_block_gluing_and_mixed_word_boundary.py
python -m py_compile verify_p7_221_diagonal_block_gluing_and_mixed_word_boundary.py audit_p7_221_diagonal_block_gluing_and_mixed_word_boundary.py
uv run --with ruff ruff check verify_p7_221_diagonal_block_gluing_and_mixed_word_boundary.py audit_p7_221_diagonal_block_gluing_and_mixed_word_boundary.py
```

The primary verifier constructs all 91 physical edge blocks explicitly as
`3 x 3` matrices, checks transpose symmetry, recovers each scalar edge graph,
checks all 186 prescribed and six free pure cofactors, and evaluates the mixed
coefficient (17).  The independent audit imports neither SymPy nor either
primary verifier; it reconstructs the three charts and diagonal block
evaluation using exact rational pairs in `Q[rho]/(rho^2-21)`.  Neither replay
searches supports, parameter values, or graph candidates.
