# Four-root simultaneous swallowed-pure nonzero-response physical control

## Status

**Exact characteristic-zero physical graph-side sharpness theorem.**  There
is a four-root, surplus-two ternary graph with all of the following
properties simultaneously:

- the four roots form a maximum-cardinality torus zero set;
- every outside mode is a rank-three blocker;
- the full ten-mode state is locally concise;
- all three pure GHZ coefficients are exactly one and the entire Hamming-one
  shell is zero;
- all six fixed-`Q` pair responses and the four-port response are nonzero;
- for all seven targets, every active pure GHZ class is swallowed by the
  complete nuisance slice space, so `q_S=0`.

Thus maximum-root saturation, the strongest blocker quotas, local concision,
pure normalization, the Hamming-one shell, and physical response
nonvanishing do **not** force the good `GLD7` quotient branch.

The graph is not a Krenn--Gu witness: one displayed mixed full-state
coefficient equals one.  Therefore this is not a witness-locus obstruction
or a counterexample.  It proves that the remaining full mixed target
equations are load-bearing.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

This theorem sharpens the graph-side bad quotient in
[`GLD5`](FOUR_ROOT_CONSTANT_TARGET_MODULE_SELECTOR_QUOTIENT_AND_MAXIMUM_ROOT_SHARPNESS_THEOREM.md)
and the swallowed-pure branch isolated by
[`GLD7`](FIXED_Q_FULL_MODULE_TARGET_QUOTIENT_RANK_ONE_PURE_SURVIVAL_AND_SIX_PORT_ATTACHMENT_TRICHOTOMY_THEOREM.md).

## 1. Exact graph

Work over a characteristic-zero field `K`.  Put

```text
R={r0,r1,r2,r3},       U={u0,u1,u2,u3},
Q={q0,q1},             B=U disjoint-union Q.           (1)
```

Use the dual coordinate basis `e_0^*,e_1^*,e_2^*` at every mode, and set

```text
x_ri=(1,1,1),          z_qj=(1,1,1).                   (2)
```

Every root--root block is zero.  In the following table, an entry `c`
denotes the rank-one same-coordinate block `e_c^* tensor e_c^*`, and `-`
denotes zero:

```text
       u0 u1 u2 u3 q0 q1
r0      1  0  2  -  0  2
r1      2  -  -  1  2  0
r2      -  1  0  2  -  1
r3      0  2  1  0  1  - .                            (3)
```

Every outside--outside edge is nonzero, with unit weight and coordinate
colour

```text
01:0  02:2  03:0  04:2  05:0
12:1  13:1  14:2  15:0
23:0  24:1  25:2
34:1  35:0
45:0.                                                   (4)
```

Outside indices `0,1,2,3,4,5` mean `u0,u1,u2,u3,q0,q1`.

## 2. Maximum roots, blockers, and local concision

### Theorem 1 (incidence and state properties)

The graph (3)--(4) has the following properties.

1. `R` is a maximum-cardinality torus zero set.
2. Every outside mode is a rank-three blocker for `R`.
3. The three pure full-state coefficients are exactly one.
4. Every Hamming-one coefficient adjacent to a pure word is zero.
5. The full ten-mode state is locally concise.

### Proof

Every nonzero edge in (3)--(4) is a coordinate monomial, so it evaluates
nonzero on every pair of torus vectors.  Each outside vertex has three
nonzero root incidences and one zero entry.  A torus zero set containing that
outside vertex can therefore contain at most the single old root at the
zero entry.  No zero set contains two outside vertices because their edge in
(4) is nonzero.  Hence every torus zero set meeting `B` has size at most two,
whereas `R` has size four.  This proves maximum cardinality over all vertex
sets and all torus-vector choices.

At each outside mode the four root rows in (3) are exactly
`e_0^*,e_1^*,e_2^*,0` in some order, so their span has rank three.  This
proves the blocker statement.

Direct matching inspection gives one pure matching in each colour and no
second matching with the same word.  Their coefficients are one.  A word
which differs from a pure word at exactly one mode has odd colour
multiplicities and therefore has no same-coordinate perfect matching.

For any chosen mode, take the three flattening columns in which all other
modes have colour `c=0,1,2`.  The rows indexed by the colour at the chosen
mode form the identity matrix: the diagonal entries are the pure
coefficients and the off-diagonal entries are Hamming-one coefficients.
Every one-mode flattening therefore has rank three, proving local concision.
`square`

## 3. Seven nonzero responses and seven swallowed quotients

Let `H` be the physical principal matching deck of (4), and use the fixed
fully supported contraction (2).  For

```text
S in binom(U,2) union {U},                              (5)
```

let `P_S(H)` and `N_S` be the physical response and complete nuisance space
of `GLD7`.

### Theorem 2 (simultaneous nonzero swallowed branch)

For every `S` in (5),

```text
P_S(H)!=0,
d_(S,0),d_(S,1),d_(S,2) in N_S,
q_S=0.                                                   (6)
```

Moreover every desired companion coefficient is zero:

```text
g_S=0.                                                   (7)
```

### Proof of response nonvanishing and (7)

Every induced outside graph on `Q union S` is complete with nonzero
coordinate-monomial edges.  Evaluating the open `S` slots at `(1,1,1)`
gives three matching contributions for a pair `S` and fifteen for `S=U`.
Thus every response tensor is nonzero.

For a pair, `g_S=G_(U-S)` would require one root--root edge; for `S=U`,
`g_U=G_empty` would require two.  All root--root blocks vanish, proving (7).

### Exact nuisance certificates

It remains to prove the stronger pure membership in (6).  Write
`C=U-S`.  For `D subset B`, `|D|=4`, put `I=B-D`.  Let

```text
nu_S(D;sigma;beta)=(id_(L_S^*) tensor eta)Theta_S(x).   (8)
```

Here `sigma:D intersect S->{0,1,2}` fixes the coefficient colours on the
open target ports used by the companion, and
`beta:C-D->{0,1,2}` fixes the remaining complement-port deck colours.  On
`S-D` and `Q-D`, take deck colour zero.  The functional `eta` selects
`sigma` on `D intersect S` and colour zero on `S-D`.  Since `z_q=(1,1,1)`,
every residual evaluation is one.  Equivalently, (8) is obtained by
enumerating the bijections between the four roots and `D`, multiplying the
four root--outside monomials, filtering the named `S` colours, and appending
`beta` on `C-D`.  Every such `D` is a nuisance companion set.

The following twenty-one identities hold coefficientwise.  A string such as
`0125` denotes `D`; entries before the semicolon after it are `sigma`, and
the final entries are `beta`.

```text
S=01:
 d0=nu(0125;0:0,1:0;3:0)
 d1=nu(0123;0:1,1:1;-)
 d2=nu(0123;0:2,1:2;-)

S=02:
 d0=nu(0125;0:0,2:0;3:0)
 d1=nu(0123;0:1,2:1;-)
 d2=nu(0123;0:2,2:2;-)-nu(0124;0:0,2:2;3:0)

S=03:
 d0=-nu(0235;0:2,3:0;1:0)+nu(0245;0:0;1:0)
 d1=nu(0134;0:1,3:1;2:1)
 d2=nu(0135;0:2,3:2;2:2)

S=12:
 d0=nu(0125;1:0,2:0;3:0)
 d1=nu(0123;1:1,2:1;-)
 d2=nu(0123;1:2,2:2;-)

S=13:
 d0=nu(1235;1:0,3:0;0:0)
 d1=nu(0134;1:1,3:1;2:1)-nu(0135;1:0,3:1;2:1)
 d2=nu(0123;1:2,3:2;-)

S=23:
 d0=nu(1235;2:0,3:0;0:0)
 d1=nu(0123;2:1,3:1;-)
 d2=nu(0123;2:2,3:2;-)

S=U:
 d0=nu(0125;0:0,1:0,2:0;-)
 d1=nu(0123;0:1,1:1,2:1,3:1;-)
 d2=nu(0123;0:2,1:2,2:2,3:2;-).                       (9)
```

Each right side belongs to `N_S` by definition.  Direct expansion of the
four-root bijections gives the singleton pure word on the left.  Thus all
three active pure classes vanish in `L_S^*/N_S` for all seven `S`, proving
(6). `square`

For completeness, exact rational row reduction of every nuisance generator
gives

```text
S       generators    rank      d0 d1 d2 in N_S
01          203        175       T  T  T
02          203        174       T  T  T
03          200        165       T  T  T
12          175        157       T  T  T
13          194        166       T  T  T
23          194        169       T  T  T
U           115         61       T  T  T.              (10)
```

The pair ambient spaces have dimension `3^6=729`; the four-port ambient
space has dimension `3^4=81`.  The displayed identities (9), not the rank
table alone, are the proof of pure membership.

## 4. Exact mixed failure

### Theorem 3 (not a witness)

In vertex order

```text
(r0,r1,r2,r3,u0,u1,u2,u3,q0,q1),                       (11)
```

the mixed word

```text
1200100020                                                (12)
```

has coefficient one.

### Proof

The matching

```text
(r0,u0)(r1,q0)(r2,u2)(r3,u3)(u1,q1)                    (13)
```

has exactly the word (12), and direct inspection shows no second matching
has that word.  Hence the coefficient is one.  A GHZ target has zero mixed
coefficients, so the graph does not satisfy the full target equation.
`square`

## 5. Frontier and UNKNOWN remainder

```text
maximum-root/triple-blocker physical control:             PROVED;
pure normalization + Hamming-one zero + local concision:  PROVED;
all seven physical responses nonzero:                     PROVED;
all seven active pure quotient ranks zero:                PROVED;
these incidence/nonvanishing conditions force q=1:        FALSE;
control satisfies the full mixed target equation:         FALSE;
simultaneous q=0,P_S(H)!=0 on a hypothetical witness:     UNKNOWN;
bounded mixed detector for every swallowed-pure branch:   UNKNOWN;
coefficient-pure syzygy or permanent implication:         UNKNOWN;
global Krenn--Gu conjecture:                               UNRESOLVED.
```

The breadth is one four-root/four-port chart and all seven targets for one
fixed `Q`.  The depth is the complete fixed-`Q` nuisance module plus one full
ten-mode mixed coefficient.  The reconstructed data are the seven nonzero
physical responses, but none is target-attached because every desired module
class vanishes.  There is no transition object.  The obstruction is the
simultaneous swallowed-pure quotient, and the mixed coefficient excludes
this control from the witness locus.  The permanent implication is none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_four_root_simultaneous_swallowed_pure_nonzero_response_physical_control.py
python -I claims/arbitrary-order/audit_four_root_simultaneous_swallowed_pure_nonzero_response_physical_control.py
```

The primary verifier enumerates full-state matchings and root-to-`D`
companion bijections, checks all twenty-one identities (9), and computes the
exact nuisance ranks (10).  The independent no-import audit uses a
vertex-deletion matching recurrence, separately constructed tagged
root/outside matchings, and standard-library rational elimination.  The
scripts audit a finite proof leaf; the incidence and target-scope arguments
above remain load-bearing.
