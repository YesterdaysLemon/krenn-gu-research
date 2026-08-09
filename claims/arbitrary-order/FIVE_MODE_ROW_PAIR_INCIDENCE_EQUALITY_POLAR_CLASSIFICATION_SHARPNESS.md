# Five-mode row-pair equality: polar classification and sharpness

## Status

**Exact symbolic classification and fixed rational sharpness model.**  The
five-mode row-pair incidence theorem proves that every source-row pair in a
hypothetical

```text
P_m -> Delta_3
```

restriction has at least five coordinate-incidence modes.  This note
classifies the equality-at-five incidence multihypergraphs without assigning
labels to named modes.  There are exactly **nineteen** colour-orbit types.

In the rank-two residual-plane cell, the full two-port polar matrix identities
reduce those nineteen types to exactly three survivors.  One survivor has an
exact rational `P_7` realization satisfying simultaneously:

- the canonical root profile `012,01,01,02,02,12,12`;
- all seven residual planes of rank two;
- all twenty-one synchronized polar matrix identities;
- the three nonzero pure root permanents;
- the three nonzero missing-colour residual factors; and
- local concision at every blocker.

Thus the five-mode lower bound is sharp for the complete synchronized polar
subsystem, even after the canonical and pure conditions are imposed.  The
model is **not** a `P_7 -> Delta_3` restriction: the uncontracted mixed-word
identity is not asserted.

No assignment, support, word, graph, or parameter search is used.

## 1. Incidence notation

Fix a source-row pair `p,q`.  At mode `w`, put

```text
A_w=span{r_(w,p),r_(w,q)},
K_w=ker r_(w,p) intersection ker r_(w,q),
Z_w={c:e_c^* belongs to A_w},
N_c={w:c belongs to Z_w}.                              (1)
```

The kernel-deletion quota gives

```text
|N_c|>=2                                                (2)
```

for each target colour.  Also `|Z_w|<=2`.

Assume exactly five `Z_w` are nonempty.  Write

```text
x_c = number of singleton labels {c},
y_c = number of doubleton labels missing c,
X=sum x_c,                    Y=sum y_c.                (3)
```

Thus `y_0` counts `{1,2}`.  We have

```text
X+Y=5,
deg(c)=|N_c|=x_c+Y-y_c>=2.                              (4)
```

The total incidence is `5+Y`, so `1<=Y<=5`.

## 2. The nineteen equality multihypergraphs

The following derivation is by integer partitions and the inequalities (4),
not by placing labels on five distinguishable modes.

### `Y=1`

All three degrees equal two.  Up to colour permutation,

```text
A.   {12}+2{0}+{1}+{2}.                                (5)
```

### `Y=2`

Put `z_c=x_c-y_c`.  Equation (4) says `z_c>=0` and
`sum z_c=1`, so `x=y+e_s`.  The partitions `2` and `1+1`,
with the surplus placed either on or off a repeated part, give

```text
B1.  2{12}+3{0},
B2.  2{12}+2{0}+{1},
B3.  {12}+{02}+{0}+{1}+{2},
B4.  {12}+{02}+2{0}+{1}.                              (6)
```

### `Y=3`

The partitions of three give:

- `(3,0,0)`, forcing the two singletons onto the repeated coordinate;
- `(2,1,0)`, with the spare singleton on any of its three inequivalent
  multiplicity positions; or
- `(1,1,1)`, with singleton partition `2` or `1+1`.

Hence

```text
C1.  3{12}+2{0},
C2.  2{12}+{02}+2{0},
C3.  2{12}+{02}+{0}+{1},
C4.  2{12}+{02}+{0}+{2},
C5.  {12}+{02}+{01}+2{0},
C6.  {12}+{02}+{01}+{0}+{1}.                         (7)
```

### `Y=4`

There is one singleton.  A non-singleton coordinate has `y_c<=2`, while the
singleton coordinate has `y_c<=3`.  The admissible partitions and singleton
positions give

```text
D1.  3{12}+{02}+{0},
D2.  2{12}+2{02}+{0},
D3.  2{12}+2{02}+{2},
D4.  2{12}+{02}+{01}+{0},
D5.  2{12}+{02}+{01}+{1}.                            (8)
```

The partition `(4,0,0)` violates a quota regardless of the singleton
position.

### `Y=5`

There are no singletons and `y_c<=3`.  The admissible partitions of five are

```text
E1.  3{12}+2{02},
E2.  3{12}+{02}+{01},
E3.  2{12}+2{02}+{01}.                                (9)
```

The counts are therefore `1+4+6+5+3=19`.

## 3. Rank-two polar filtering

Assume now that every residual `A_w` has rank two.  Leave modes `u,v` free
and contract every other mode through its null line `K_w=<kappa_w>`.  The
polar matrix identity is

```text
s_uv D_uv
 =diag(lambda_c product_(w notin {u,v}) kappa_w[c]),   (10)

D_uv=R_u^T [[0,1],[1,0]] R_v.                         (11)
```

Every `D_uv` has rank exactly two.  If `U={u,v}`, the nonzero diagonal
support on the right of (10) is

```text
C_U={c:N_c subset U}.                                  (12)
```

Since `|N_c|>=2`, a colour belongs to `C_U` exactly when `N_c=U`.  Therefore
every size-two neighbourhood must occur for exactly two colours: multiplicity
one would give rank one on the right, while multiplicity three would give
rank three and would also require a local plane to contain all three axes.

If `N_p=N_q`, every boundary label contains both `p,q` or neither.  Since a
nonempty label has size at most two, its label is either `{p,q}` or the
singleton `{r}`.  A common size-two neighbourhood therefore forces

```text
2{pq}+3{r},                                             (13)
```

which is Type B1.  If there is no size-two neighbourhood, every colour degree
is at least three; inspection of the five partition families above leaves
only Types D4 and E3.  Thus:

### Theorem 1 (rank-two equality filter)

The only equality-at-five incidence multihypergraphs compatible with the
rank support of all two-port polar identities are, up to colour permutation,

```text
B1.  2{12}+3{0},
D4.  2{12}+{02}+{01}+{0},
E3.  2{12}+2{02}+{01}.                                (14)
```

For B1, the two size-two neighbourhoods coincide and give the permitted
rank-two diagonal.  For D4 and E3, every neighbourhood has size at least
three, so every two-port target diagonal is zero and all complementary shore
permanents must vanish.

This theorem filters the polar subsystem.  It does not claim that all three
survivors lift to the original tensor identity.

## 4. Exact canonical P7 sharpness model

We realize Type D4.  Label the seven modes

```text
t,u01,v01,u02,v02,u12,v12.                            (15)
```

### Residual rows

Use coordinate columns `e_0,e_1,e_2` and set

```text
(a_t,b_t)       =(e_0-e_2, e_1-e_2),
(a_u01,b_u01)   =(e_0,     e_1-e_2),
(a_v01,b_v01)   =(e_0-e_2, e_1-e_2),
(a_u02,b_u02)   =(e_1,     e_2),
(a_v02,b_v02)   =(e_2,     e_1),
(a_u12,b_u12)   =(e_0,     e_1),
(a_v12,b_v12)   =(e_2,     e_0).                      (16)
```

Choose their null vectors

```text
k_t   =(1,1,1),           k_u01=(0,1,1),
k_v01 =(1,1,1),           k_u02=k_v02=(1,0,0),
k_u12 =(0,0,1),           k_v12=(0,1,0).              (17)
```

The incidence labels are

```text
Z_u01={0},
Z_u02=Z_v02={1,2},
Z_u12={0,1},
Z_v12={0,2},
Z_t=Z_v01=empty.                                      (18)
```

Thus the five boundary modes have Type D4 and

```text
N_0={u01,u12,v12},
N_1={u02,v02,u12},
N_2={u02,v02,v12}.                                    (19)
```

Every `N_c` has size three.

### Root rows

For root `0`, take

```text
H_(0,t)   =(1,1,-2),
H_(0,u01) =(1,0,0),       H_(0,v01)=(1,-1,0),
H_(0,u02) =(0,0,1),       H_(0,v02)=(0,0,1),
H_(0,u12) =(0,1,0),       H_(0,v12)=(0,0,1).          (20)
```

For roots `i=1,2,3,4`, put `n=i+1` and take

```text
H_(i,t)   =(1,n,n^2),
H_(i,u01) =(1,n,0),       H_(i,v01)=(n,1,0),
H_(i,u02) =(1,0,n),       H_(i,v02)=(n,0,1),
H_(i,u12) =(0,1,n),       H_(i,v12)=(0,n,1).          (21)
```

Their blocker spans are exactly

```text
012,01,01,02,02,12,12,                                (22)
```

and each root's seven local rows span the full three-space.  Together with
the residual rows, every blocker is locally concise.

### All twenty-one polar identities

Equation (20) was chosen so that

```text
H_(0,w)(k_w)=0
```

for every mode `w`.  Hence the first row of the five-by-seven evaluated shore
matrix is zero, and every complementary five-by-five permanent `s_uv`
vanishes.

On the target side, (19) says no `N_c` is contained in a two-mode set.
Therefore every diagonal entry on the right of (10) also vanishes.  All
twenty-one polar matrix identities are exactly `0=0`.  Every corrected
residual block `D_uv` nevertheless has rank two.

### Pure coefficients

Let the missing-colour pairs be

```text
U_0={u12,v12},       U_1={u02,v02},       U_2={u01,v01}. (23)
```

The five-root pure permanents on their complements are

```text
P_0=652,                 P_1=284,                 P_2=7200. (24)
```

The residual factors are

```text
D_(U_0)^(00)=D_(U_1)^(11)=D_(U_2)^(22)=1.             (25)
```

Thus all three full pure coefficients are nonzero, with values
`652,284,7200`.

### Corollary 2 (sharp polar boundary)

Five coordinate-incidence modes are attainable simultaneously with all
rank-two two-port polar identities, the canonical profile, local concision,
and all three pure coefficients.  Consequently none of those data can raise
the row-pair lower bound from five to six.

## Scope wall

Proved:

- the nineteen equality-at-five incidence orbits under colour permutation;
- the exact three-survivor rank-two polar filter;
- an exact Type-D4 common root/residual model satisfying all twenty-one polar
  matrix identities and all canonical pure data.

Not proved or claimed:

- the original uncontracted mixed-word identity;
- a factorized `P_7 -> Delta_3` restriction;
- liftability of any polar survivor to a permanent restriction;
- sharpness of five for the full tensor identity;
- the Krenn--Gu conjecture.

The exact conclusion is

```text
full P_m identity => at least five row-pair incidence modes;

polar identities + canonical P7 profile + pure data
    !=> a sixth incidence mode.                        (26)
```

## Replay

```powershell
uv run --with sympy python verify_five_mode_row_pair_incidence_equality_polar_classification_sharpness.py
python audit_five_mode_row_pair_incidence_equality_polar_classification_sharpness.py
uv run --with sympy --with ruff python -m ruff check verify_five_mode_row_pair_incidence_equality_polar_classification_sharpness.py audit_five_mode_row_pair_incidence_equality_polar_classification_sharpness.py
python -m py_compile verify_five_mode_row_pair_incidence_equality_polar_classification_sharpness.py audit_five_mode_row_pair_incidence_equality_polar_classification_sharpness.py
```

The primary verifier checks the nineteen derived normal forms, the exact
three-survivor filter, and every stated property of the rational model.  The
independent no-import audit repeats the classification and model arithmetic
with separate exact routines.  These fixed replays do not replace the
symbolic completeness proof and perform no search.
