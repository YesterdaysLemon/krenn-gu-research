# Bare-theta absorption and the marked cofactor-response target

## Status

**Exact characteristic-zero local identities, exact quotient method
countercharts, and a new conditional response obstruction.**  The aligned
bare theta is not automatically excluded by apolar boundary-sector killing
or ordinary tensor flattenings.  There are exact `1+1+1` and `2+1+0` port
charts satisfying the tight local physical degree ledger, local rank, aligned
three-term cancellation, and cut-colour transport whose strongest legal
quotient is a nonzero diagonal `Delta_3` slice.

The failure is structured: two port quotients become the same target-colour
line, while the third remains open.  The theta equation kills the aligned
component at that open port and leaves exactly the transverse target colour.
Call this **one-open-port theta absorption**.

The defect-free bare theta nevertheless has stronger local algebra.  Its
pair-deletion cofactor matrix satisfies signless condensation, while a
rank-one Segre response satisfies the corresponding alternating minor.
If a marked boundary construction transports both equations to the same
nonzero response matrix, their sign clash gives an immediate factor-`2`
contradiction.  The present product quotient kills those marked sectors, so
the required **marked pair-deletion response jet** remains a precise new
proof obligation.

These charts are representatives of two incidence orbits, not a
classification of all bare-theta incidences.  They are method countermodels,
not full restrictions and not graph constructions.  The global Krenn--Gu
conjecture remains unresolved.

## The bare theta and its cofactor matrix

Write the scalar aligned theta as

```text
X = [ A B C ]
    [ D E 0 ]
    [ F 0 G ],                 A B C D E F G !=0,  (1)
```

and put

```text
Z=per(X)=A E G+B D G+C E F.                        (2)
```

For a forbidden aligned mixed coefficient, after removing its nonzero
common exterior monomial,

```text
Z=0.                                               (3)
```

Let `Q_ij` be the permanent obtained by deleting row `i` and column `j`.
Direct expansion gives

```text
Q = [ E G       D G       E F     ]
    [ B G       A G+C F   B F     ]
    [ C E       C D       A E+B D ].               (4)
```

Every entry of (4) is nonzero under (1)--(3).  The product entries are
manifestly nonzero, while

```text
Q_22=-B D G/E,                 Q_33=-C E F/G.      (5)
```

The two bounded theta faces obey the signless condensation equations

```text
Z G=Q_11 Q_22+Q_12 Q_21,
Z E=Q_11 Q_33+Q_13 Q_31.                           (6)
```

They are the zero-bosonic-defect specializations of the permanent identity
in
`ARBITRARY_PERMANENT_THREE_EXCESS_BOSONIC_PLUCKER_DEFECT_THEOREM.md`.
They are also the two face-local weighted graphical-condensation relations
for this planar theta; compare Kuo,
[*Applications of Graphical Condensation for Enumerating Matchings and
Tilings*](https://arxiv.org/abs/math/0304090).  Four other anchor equations
follow by direct `3 x 3` expansion:

```text
B Z=Q_21 Q_33+Q_23 Q_31,
C Z=Q_21 Q_32+Q_22 Q_31,
D Z=Q_12 Q_33+Q_13 Q_32,
F Z=Q_12 Q_23+Q_13 Q_22.                           (7)
```

No general permanent Desnanot--Jacobi theorem is being claimed for (7).

At `Z=0`, (6) fixes two nonzero phase cross-ratios to `-1`.  Eliminating the
common channel gives the gauge-semi-invariant cubic

```text
H(Q)=Q_12 Q_21 Q_33-Q_13 Q_31 Q_22
    =(B D G-C E F) Z=0.                            (8)
```

Under row/column gauges `Q_ij -> r_i c_j Q_ij`, `H` changes by one overall
nonzero scalar.

## The augmented chord-killing product quotient

Return now to the hypothetical tight restriction at support `3m+3`, with all
three excess cells in the minimal theta.  Assume that a labelled theta
matching together with its common exterior complement lies in the selected
pure-backbone union and induces the aligned word, as in the preceding
one-chord theorems.  Neither completing chord is eligible at that word,
although either chord may exist physically in another mandatory coordinate
colour.

Let `B_i` be the span of covectors on cells leaving port mode `a_i`.  If a
completing chord is physically present but ineligible at the aligned word,
let `Y_i` be its coordinate direction; otherwise put `Y_i=0`.  Define

```text
D_i=B_i+span(Y_i),              rho_i:V_i -> V_i/D_i. (9)
```

Every nonempty balanced boundary sector contains an `A-Q` factor and dies
because `B_i subset D_i`.  Every empty-sector term using an ineligible
physical chord dies because its row factor lies in `Y_i`.  Alignment forces
all directions in `D_i` to differ from `alpha_i`, so each aligned theta
factor remains nonzero.  The localization lemma uniquely selects the frozen
empty-sector exterior complement exactly as in the one-chord theorems.

Thus (9) is stronger than the ordinary product quotient for the purpose of
isolating the bare theta: it kills both boundary sectors and differently
coloured physical chord terms.  The next two charts show that even this
stronger slice can land exactly on the projected diagonal target.

## Exact `1+1+1` absorption chart

Use the aligned colours

```text
(alpha_0,alpha_1,alpha_2)=(0,1,0)                 (10)
```

and forms

```text
z_0=z_2=e_0,             z_1=e_1,
L_0=e_0+e_1,             L_1=e_1+mu e_0,
L_2=e_0+e_1,             mu!=0.                   (11)
```

Take the covector port

```text
X_Theta = [ L_0  z_0  -2 z_0 ]
          [ z_1  L_1   0     ]
          [ z_2  0     L_2   ].                   (12)
```

At (10), its three theta terms are exactly `1,1,-2`; they are nonzero and
sum to zero.  Put

```text
D_0=D_2=span(e_1,e_2),        D_1=span(e_2).       (13)
```

The exact quotient is

```text
(rho_0 tensor rho_1 tensor rho_2)T_Theta
  =-mu e_0 tensor e_0 tensor e_0.                  (14)
```

For physically absent chords, (13) is realized by the outgoing-colour
ledger

```text
(s_0,s_1,s_2;tau)=(2,1,2;0).                      (15)
```

The source-side and mode-side cut multisets are both `1^2 2^3`.  Local rank
is three at every port: the boundary directions supply the coordinates
missing from the two-dimensional theta spans.

At the local port/cut-ledger level, a word-ineligible chord direction of
colour `2` can be moved into `D_i` while removing one outgoing colour-`2`
direction in its row.  Preserving the mandatory source cover would also
require a colour-preserving exterior `R-P/A-Q` to `R-Q` reroute.  Conditional
on that reroute, either or both chord directions leave the local counts,
`D_i`, local rank, cut transport, and (14) unchanged.  No simple,
matching-covered, conformal exterior graph realizing the reroute is
constructed here.

## Exact `2+1+0` absorption chart

Use

```text
(alpha_0,alpha_1,alpha_2)=(0,2,2),
z_0=e_0,                    z_1=z_2=e_2,
L_1=e_0+e_2,                L_2=e_0+2e_2,
M=e_2+e_0.                                         (16)
```

Take

```text
X_Theta = [ z_0  L_1  -2 L_2 ]
          [ M    z_1   0      ]
          [ z_2  0     z_2    ].                  (17)
```

Again the aligned terms are `1,1,-2`.  With

```text
D_0=span(e_1),          D_1=D_2=span(e_0,e_1),     (18)
```

one obtains

```text
(rho_0 tensor rho_1 tensor rho_2)T_Theta
  =-3 e_2 tensor e_2 tensor e_2.                  (19)
```

The absent-chord local ledger is

```text
(s_0,s_1,s_2;tau)=(1,2,2;0),                      (20)
```

and both cut shores have colours `0^2 1^3`.  At the local ledger level,
chord directions of colour `1` can be absorbed into `D_i` while the
corresponding outgoing directions are removed, provided the same
colour-preserving exterior reroute is available.  This preserves
(18)--(19), but does not prove a physical exterior realization.

Both absent-chord cut multisets use three cells of one repeated colour while
`tau=0`; a simple exterior realization would therefore require at least
three exterior modes, hence `m>=6`.  The displayed objects are exact local
tensor/cut-ledger charts at every formal port order, not existence claims at
`m=4` or `m=5`.

## Invented theory: the marked pair-deletion response jet

The ordinary product quotient cannot use (6).  Its pair-deletion sectors
are nonempty balanced sectors, so it kills them precisely when it kills the
unwanted convolution.  The next object must retain those sectors with
marks instead of annihilating them.

For each port row `i` and source `j`, let `Omega_ij` be the exterior matching
response that covers `a_i,p_j` externally and leaves the other four port
vertices for the theta, after fixing the exterior marking or word under
study.  The bidegree-`(1,1)` part of that boundary matching generating
function is the **marked pair-deletion response matrix**

```text
R_ij=Omega_ij Q_ij.                                (21)
```

Equation (21) is the exact boundary-convolution factorization of that one
sector.  What is not known is a usable relation among the nine exterior
factors `Omega_ij`.

Here is a sufficient local-to-global bridge.  Suppose, for one cofacial
`2 x 2` block, all four marked responses are nonzero and the exterior
responses have the toric holonomy

```text
Omega_11 Omega_22=Omega_12 Omega_21.               (22)
```

Then (3), (6), and (21) give the **symmetric-compound equation**

```text
R_11 R_22+R_12 R_21=0.                             (23)
```

If a target selector puts the same marked block on the rank-one Segre cone,
it also obeys the **alternating-compound equation**

```text
R_11 R_22-R_12 R_21=0.                             (24)
```

Adding and subtracting (23)--(24) gives

```text
2 R_11 R_22=2 R_12 R_21=0,                        (25)
```

contradicting nonvanishing in characteristic zero.  This is the promised
factor-`2` obstruction.

The proof obligation is now exact and smaller than "find another theta
identity":

1. construct a legal marked selector exposing the responses (21);
2. prove the single exterior cross-ratio equation (22), or a substitute
   that transports (6); and
3. prove that the corresponding target marked block satisfies (24).

Planar matchgate, Postnikov boundary-measurement, and electrical-grove
theories all produce related Pluecker or response identities, but require
planar terminal order or disk/outer-face hypotheses not known for the
ambient graph.  They are templates for (22), not unconditional inputs.
See Cai--Gorenstein,
[*Matchgates Revisited*](https://arxiv.org/abs/1303.6729), Postnikov,
[*Total positivity, Grassmannians, and networks*](https://arxiv.org/abs/math/0609764),
and Kenyon--Wilson,
[*Boundary partitions in trees and dimers*](https://arxiv.org/abs/math/0608422).

## Scope wall

```text
bare-theta cofactor matrix and six anchor quadrics:       PROVED;
all bare-theta cofactors at Z=0:                          NONZERO;
ordinary/augmented apolar quotient exclusion:             FALSE;
1+1+1 one-open-port absorption chart:                     EXACT;
2+1+0 one-open-port absorption chart:                     EXACT;
physical word-ineligible chord directions:                ABSORBABLE LOCALLY;
  required exterior colour reroute / graph realization:   NOT CONSTRUCTED;
full bare-theta incidence classification (2+4 orbits):     NOT ATTEMPTED HERE;
marked pair-deletion sector factorization (21):           EXACT;
exterior toric holonomy (22):                             NOT PROVED;
target marked Segre equation (24):                        NOT PROVED;
conditional symmetric/alternating factor-2 clash:         PROVED;
full global bare-theta exclusion:                         UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_arbitrary_permanent_three_excess_bare_theta_absorption_and_cofactor_response_boundary.py
python audit_arbitrary_permanent_three_excess_bare_theta_absorption_and_cofactor_response_boundary.py
```

The primary verifier reconstructs the cofactor matrix, all six anchor
identities, the gauge cubic, both exact quotient residues, the ledgers, and
the factor-`2` clash.  The independent no-import audit checks the same fixed
algebra with exact integer data.  Neither script searches a support family,
word family, or matching family.
