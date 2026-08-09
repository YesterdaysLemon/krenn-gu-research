# Replay tokens, five-sector exchange closure, and nonalignment counterfamilies

## Status

**Exact arbitrary-order conditional closure theorem and exact structural
counterfamilies.**  The six-token ear theorem and the three-port phase
theorem meet in one sharp statement:

- source replay has only the partitions `2+1` and `1+1+1`;
- if all five isolated exchanges of one anchored three-port coefficient are
  forced, their gains are inconsistent over characteristic zero;
- every proper four-exchange subsystem is lattice-independent.

The current support, ear, conformal, local-rank, and pure-backbone hypotheses
do not force those five sectors, or a coefficient-induced conformal carrier
containing all three excess cells.  A base countermodel exists at `m=6`, and
an explicit colour-preserving splice gives a nonalignment family for every
`m>=9`.  These are structural boundary models, not `P_m -> Delta_3`
restrictions.

The inputs are
[`ARBITRARY_PERMANENT_THREE_EXCESS_SIX_TOKEN_EAR_THEOREM.md`](ARBITRARY_PERMANENT_THREE_EXCESS_SIX_TOKEN_EAR_THEOREM.md),
[`ARBITRARY_PERMANENT_THREE_EXCESS_B3_PHASE_HOLONOMY_NOGO.md`](ARBITRARY_PERMANENT_THREE_EXCESS_B3_PHASE_HOLONOMY_NOGO.md),
and
[`ARBITRARY_PERMANENT_THREE_EXCESS_CONFORMAL_CORE_ALIGNMENT_BOUNDARY.md`](ARBITRARY_PERMANENT_THREE_EXCESS_CONFORMAL_CORE_ALIGNMENT_BOUNDARY.md).

## The source replay partition is not `3`

For a source `p`, replay multiplicity is exactly excess-cell incidence:

```text
s(p)=deg_G(p)-3=h_E(p).                              (1)
```

The port-localization theorem proves that the exceptional-source set has
size two or three.  Therefore all three excess cells cannot meet one source,
and the source-shore replay partition is exactly one of

```text
2+1,                     1+1+1.                     (2)
```

If a coefficient-induced cycle exists, all source replay tokens lie on it.
For an aligned `C_4`, its two sources have

```text
s=(2,1),                  h=s+1=(3,2).               (3)
```

For an aligned `C_6`, its three sources have

```text
s=(1,1,1),                h=(2,2,2).                 (4)
```

An aligned minimal theta has the same source profile (4).  This is the exact
connection between the constant ear schedule and the conformal carrier.  No
analogous identification holds on the mode shore.

## The five anchored exchange vectors

Fix one ordered nonzero three-port matrix and use the six directed arc-ratio
variables

```text
x_12,x_21,x_13,x_31,x_23,x_32.                      (5)
```

The three transposition and two oriented three-cycle gains have exponent
vectors

```text
lambda_12=e_12+e_21,
lambda_13=e_13+e_31,
lambda_23=e_23+e_32,
lambda_+ =e_12+e_23+e_31,
lambda_- =e_13+e_32+e_21.                           (6)
```

They have rank four and one primitive integer relation:

```text
lambda_+ + lambda_-
  -lambda_12-lambda_13-lambda_23=0.                 (7)
```

Every coefficient in (7) is nonzero, and every proper four-vector subset is
independent.  Thus (7) is the entire relation lattice.

## Five-sector closure theorem

Suppose physical incidence isolates all five exchanges as two-term forbidden
coefficients on the same anchored ratios.  Each then gives

```text
x^(lambda_s)=-1.                                    (8)
```

Multiplying the two oriented-cycle equations and dividing by the three
transposition equations gives, by (7),

```text
1=(-1)^2/(-1)^3=-1,                                 (9)
```

a contradiction over characteristic zero.  In `B_3` coordinates, the same
calculation is

```text
u=v=-1       => uv=1,
a=b=c=-1     => abc=-1,                             (10)
```

contradicting the toric identity `uv=abc`.

Conversely, every proper subset of the five vectors is independent.  Its
gain assignment extends to a character of the ambient algebraic torus, so
the corresponding `-1` equations are soluble over `C*`.  Absent further
physical identifications, the all-five closure hypothesis is sharp.

## Gain-graph and biased-graph translation

Equation (7) is the multiplicative theta law for gain graphs.  Zaslavsky's
biased-graph theory requires the balanced cycles of a gain graph to satisfy
the theta property; its original formulation is
[*Biased graphs. I. Bias, balance, and gains*](https://doi.org/10.1016/0095-8956(89)90063-4).

Here every isolated cancellation asks for a **negative** rather than balanced
cycle.  A theta cannot have all three pairwise cycle gains equal to `-1`,
because the oriented cycle vectors sum as in (7).  The five-sector theorem is
the complete `B_3` version: three two-cycles and two oriented three-cycles
form one signed biased-graph closure relation.

## Why the replay budget does not force closure

The aligned `C_6` model in the conformal-core boundary note already has
degree excess

```text
s(x_0)=s(x_1)=s(x_2)=1,
s(p_0)=s(p_1)=s(p_2)=1,                              (11)
```

and zero elsewhere.  Hence every conformal-cycle ear decomposition has the
exact `3+3` replay budget at those vertices.  Its named mixed coefficient
isolates only one oriented `C_6` equation `x^lambda=-1`.  The generated
exchange lattice has rank one and no nonzero relation, so it cannot yield
(9).  The model is not a full restriction because the remaining forbidden
coefficients are not imposed.

The same support may be decorated with all three excess cells supported only
in coordinate colour two.  Its two conformal-cycle matchings then induce
different words, while matching-coveredness, local rank, pure backbones, and
the replay vector remain.  Thus the uncoloured ear schedule does not force
coloured alignment.

## A stronger `2+1` nonalignment base

There is a second `m=6` base for which no conformal cycle or theta carrier
containing all three excess cells can align.  Use modes `x_j,y_j`, sources
`p_j,q_j`, with indices modulo three.  Its 18 mandatory cells are

```text
B_0=x_0 p_2,      A_1=x_1 p_1,      A_2=x_2 p_2,
N_j=y_j q_j,      C_j=x_j q_j,       D_j=y_j p_j,
C'_j=x_j q_(j+1), D'_0=y_0 p_1,      D'_2=y_2 p_0,
J=y_1 p_0.                                           (12)
```

They partition into pure coordinate matchings

```text
M_0={B_0,A_1,C_2,N_0,N_1,D'_2},
M_1={C_0,A_2,N_2,C_1,D_0,D_1},
M_2={C'_2,D_2,C'_1,C'_0,J,D'_0}.                    (13)
```

Add three colour-two excess cells

```text
A_0=x_0 p_0,          B_1=x_1 p_0,          B_2=x_2 p_1. (14)
```

The induced conformal cycle is

```text
x_0-A_0-p_0-B_1-x_1-A_1-p_1-B_2-x_2-A_2-p_2-B_0-x_0.
                                                               (15)
```

Its two internal matchings are

```text
{A_0,A_1,A_2},               {B_0,B_1,B_2}.         (16)
```

Both contain excess cells.  In the colour-two graph, fixing `A_0` deletes
`x_0,p_0` and isolates `y_1`; fixing `B_1,B_2` deletes
`x_1,p_0,x_2,p_1` and isolates `y_0,y_1`.  Hence neither partial matching
extends to a pure colour-two matching.  More strongly, relative to `M_2` the
excess dependency arcs are

```text
q_1 -> p_0,             q_2 -> p_0,             q_0 -> p_1,
```

which are acyclic, so `M_2` is the unique pure colour-two matching.

The replay vector is

```text
s(x_0)=s(x_1)=s(x_2)=1,
s(p_0)=2,              s(p_1)=1,                    (17)
```

with every other entry zero.  Here `P_*={p_0,p_1}`, but the excess cells use
three distinct modes.  An aligned induced cycle would have to be `C_4` and
therefore use only two modes; an aligned theta would require three
exceptional sources.  Consequently no conformal carrier containing all
three excess cells can align.

## Unbounded colour-preserving splice

For every `n>=3`, take the cubic three-coloured circulant `R_n` with modes
`u_j`, sources `v_j`, and colour-`c` matching

```text
L_c={u_j v_(j+c):j in Z/n}.                         (18)
```

In the disjoint union of the base and `R_n`, delete the two colour-zero edges

```text
N_0=y_0 q_0,                 u_0 v_0,
```

and replace them by

```text
y_0 v_0,                     u_0 q_0.               (19)
```

This colour-preserving two-switch keeps all three coordinate colour classes
perfect matchings and preserves every degree.  The base remains connected
after deleting `N_0`.  Also `L_0 union L_1` is a spanning `2n`-cycle in
`R_n`, so deleting `u_0v_0` leaves a spanning path; the two cross edges join
the pieces.  The switch also preserves a complement perfect matching for
(15), leaves the induced carrier and colour-two Hall failures untouched, and
makes every mandatory edge allowed.  The two carrier matchings plus that
complement cover the excess edges, so the connected full support remains
matching-covered.

The resulting order is

```text
m=6+n,                    |E|=21+3n=3m+3.           (20)
```

All new vertices have degree three, so (17) is unchanged.  This yields a
nonalignment counterfamily for every `m>=9`.  It disproves alignment from the
ear-token and coloured-Hall data alone, not from the full mixed-coefficient
equations of a genuine restriction.

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_three_excess_replay_exchange_closure_theorem.py
python audit_arbitrary_permanent_three_excess_replay_exchange_closure_theorem.py
```

The primary verifier proves the rank-four five-vector ledger symbolically,
checks every property of the `m=6` nonalignment base, and instantiates the
two-switch construction at independent sizes.  The independent no-import
audit reconstructs the relation, Hall-isolation witnesses, replay vector,
and affine splice counts.  The arbitrary-`n` splice proof is equations
(18)--(20), not a finite census.

## Boundary

```text
source replay partition 3:                    EXCLUDED;
source replay partitions 2+1 and 1+1+1:       POSSIBLE;
all five anchored exchange sectors:           INCONSISTENT;
every proper four-sector subset:               LATTICE-INDEPENDENT;
five-sector closure forced by six tokens:      FALSE;
coloured carrier alignment forced by tokens:   FALSE;
structural nonalignment family:                m=6 AND EVERY m>=9;
full mixed-equation counterexample:             NOT CLAIMED;
exclusion of support 3m+3:                     NOT PROVED;
global Krenn--Gu conjecture:                    UNRESOLVED.
```
