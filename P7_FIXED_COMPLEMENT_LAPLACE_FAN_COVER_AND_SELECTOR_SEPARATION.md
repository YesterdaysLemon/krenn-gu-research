# Fixed-complement Laplace forces the P7 fan, but not its selectors

## Status

**Exact characteristic-zero graph-side forcing theorem and exact selector
separation countermodel.**  The marked permanental Laplace argument is
stronger than the previously used averaged identity.  In one nonzero pure
`5 x 5` chart, fix any two of the four unmarked columns.  Ordinary Laplace
expansion along those two columns proves that the corresponding four-blocker
window is clean.  Hence every pure colour supplies all six of its possible
graph-side windows, not merely one.

For the canonical blocker profile

```text
012, 01,01, 02,02, 12,12,                            (1)
```

the three six-window families contain the tetrahedral fan

```text
1234, 1256, 1356, 1456.                              (2)
```

Moreover, the double-blocker null directions can be chosen once and for all,
so (2) is compatible at the level of physical port directions.

This does **not** make the four marked-star sensors legal.  A fixed rational
common root--blocker system attains the full graph-side window cover while
every nonzero marked shore occurs at a root pair of exact lower-frame rank
one.  The only rank-two root pairs have zero shore product on every fixed
window.  Thus the present hypotheses force the fan geometry but do not force
the companion selectors needed to turn it into a response sensor.

No graph, support, alignment, matching family, or colour-word enumeration is
used.  The countermodel is a single displayed common bilinear system.  It is
not a full mixed-word `P_7 -> Delta_3` restriction, and the global Krenn--Gu
conjecture remains **UNRESOLVED**.

## 1. Fixed-complement marked Laplace

Let `K` be a field, let `R` be a five-element root set, and write the columns
of a pure chart as

```text
B_c={t} disjoint_union A,             |A|=4.          (3)
```

Here `t` is the unique triple blocker.  Let `H` be the associated `5 x 5`
scalar root--blocker matrix.  For a fixed pair `S subset A` and a root pair
`I subset R`, put

```text
L_S(I)=per H[I,S] per H[R\I,{t} union (A\S)].         (4)
```

### Theorem 1 (fixed-complement Laplace identity)

For every two-subset `S` of `A`,

```text
sum_(I subset R, |I|=2) L_S(I)=per H.                 (5)
```

Consequently, if `per H!=0`, then for every one of the six choices of `S`
there is a root pair `I` with `L_S(I)!=0`.

Proof.  Partition the permanent expansion by the set `I` of roots sent into
the fixed column pair `S`.  The restriction of a bijection to `I` contributes
to `per H[I,S]`; its complementary restriction contributes to the other
factor in (4).  Conversely, two such complementary bijections glue uniquely.
Every full bijection occurs once, proving (5).  The nonvanishing conclusion
uses only that `K` is a field.

This is not the earlier marked average

```text
sum_(|J|=|D|=3, t in D) per H[J,D] per H[R\J,B_c\D]
   =6 per H.                                         (6)
```

Identity (5) holds separately for each retained pair `S`; no division by six
and no characteristic-zero counting step is needed.

## 2. Complete graph-side window cover

Let the seven physical blockers be

```text
B={t} disjoint_union U_0 disjoint_union U_1
      disjoint_union U_2,             |U_c|=2,        (7)
```

where `U_c` is the double-blocker pair missing colour `c`.  The pure
colour-`c` base is

```text
B_c=B\U_c={t} union A_c.                              (8)
```

Fix `S subset A_c` of size two.  Choose `I` with `L_S(I)!=0`, and put

```text
J=R\I,
D={t} union (A_c\S),
W=B\D=U_c union S.                                   (9)
```

Both permanents

```text
per H[I,S],                    per H[J,D]              (10)
```

are nonzero.  The second is the nonzero three-root shore factor, and the
first is its nonzero pure complement.  Since `t in D`, every blocker of `W`
is double type.

### Theorem 2 (six-window cover)

If the pure colour-`c` permanent is nonzero, then every window

```text
W_(c,S)=U_c union S,       S in binom(A_c,2),          (11)
```

is graph-side clean.  Thus one pure colour supplies six clean windows, and
the three nonzero pure colours supply all eighteen colour-tagged windows.

The word "colour-tagged" matters: a physical four-subset can occur in more
than one colour family.  The claim is about the exact nonzero shores, not
about eighteen distinct four-subsets.

### Simultaneous port directions

Let `T_b subset V_b^*` be the total root-row span at a double blocker `b`.
The canonical profile gives `dim T_b<=2`, so choose once and for all

```text
0!=z_b in ann(T_b).                                  (12)
```

Every root row at `b` annihilates `z_b`.  Therefore the same `z_b` works for
every root triple and every window containing `b`.  The six-window cover is
simultaneously clean on one common family of physical port directions; it
does not require a window-dependent choice of `z_b`.

## 3. The tetrahedral fan is forced graph-side

Relabel the three missing-colour pairs as

```text
U_1={1,2},             U_2={3,4},
U_0={5,6}.                                             (13)
```

In colour zero, `A_0={1,2,3,4}`.  Theorem 2 with

```text
S=12,13,14                                             (14)
```

gives the three fan windows

```text
1256, 1356, 1456.                                    (15)
```

In colour one, `A_1={3,4,5,6}`.  The choice `S=34` gives the target window

```text
U_1 union {3,4}=1234.                                (16)
```

The directions (12) make (15)--(16) compatible on every overlapping
blocker.  Hence the combinatorial and graph-side legality problem posed by
tetrahedral pair tomography is solved positively.

What is not supplied is a common legal observation row.  Each window may use
a different complementary root pair `I`; its two required companion classes
must still be separated, and the four marked-star lower values must still be
exposed with the normalized shore factor.

## 4. Sharp selector separation

The missing implication cannot be recovered from the pure permanent,
canonical profile, and current lower-frame rank data alone.

Take root tangent covectors of axis types

```text
alpha_0=alpha_1=e_0^*,
alpha_2=alpha_3=e_1^*,
alpha_4=e_2^*.                                       (17)
```

The exact lower-frame classification gives

```text
rho(01)=rho(23)=2,
rho(I)=1 for every other root pair I.                 (18)
```

Use the following pure matrices, with the displayed physical column orders:

```text
H_0, columns (t,u_01,v_01,u_02,v_02):
[-1 1 0 0 0]
[ 0 0 1 0 0]
[-1 0 0 1 0]
[ 0 0 0 0 1]
[ 1 1 0 1 0]

H_1, columns (t,u_12,v_12,u_01,v_01):
[ 0 1 0 0 0]
[-1 0 1 0 0]
[ 0 0 0 1 0]
[-1 0 0 0 1]
[ 1 0 1 0 1]

H_2, columns (t,u_02,v_02,u_12,v_12):
[-1 1 0 0 0]
[-1 0 1 0 0]
[-1 0 0 1 0]
[ 1 0 0 0 1]
[ 1 1 0 1 0].                                       (19)
```

All three permanents equal `-1`.  For each matrix and every local retained
column pair `S subset {1,2,3,4}`, direct `2 x 2` and `3 x 3` permanent
multiplication gives

```text
L_S(01)=L_S(23)=0.                                   (20)
```

One nonzero rank-one witness for every fixed `S` is:

| chart | `S=12` | `S=13` | `S=14` | `S=23` | `S=24` | `S=34` |
|:--|:--|:--|:--|:--|:--|:--|
| `H_0` | `I=14:-1` | `I=02:1` | `I=34:-1` | `I=14:-1` | `I=13:-1` | `I=34:-1` |
| `H_1` | `I=04:-1` | `I=02:-1` | `I=04:-1` | `I=24:-1` | `I=13:1` | `I=24:-1` |
| `H_2` | `I=14:-1` | `I=02:1` | `I=34:-1` | `I=14:-1` | `I=13:-1` | `I=34:-1` |

The entry after the colon is `L_S(I)`.  This table is a fixed exact
certificate, not a classification or search.  Equation (5) also shows
conceptually why every column pair must have some nonzero witness.

To assemble (19) into one physical canonical system, take the colour slices
at the shared blockers:

```text
r_(i,t)   =(H_0[i,0],H_1[i,0],H_2[i,0]),
r_(i,u01)=(H_0[i,1],H_1[i,3],0),
r_(i,v01)=(H_0[i,2],H_1[i,4],0),
r_(i,u02)=(H_0[i,3],0,H_2[i,1]),
r_(i,v02)=(H_0[i,4],0,H_2[i,2]),
r_(i,u12)=(0,H_1[i,1],H_2[i,3]),
r_(i,v12)=(0,H_1[i,2],H_2[i,4]).                     (21)
```

The span at `t` has rank three; every double-blocker span has rank two and
is exactly its named coordinate plane.  If the fixed root vector is
`(1,1,1)`, the bilinear blocks

```text
B_(i,b)=alpha_i tensor r_(i,b)                        (22)
```

evaluate to (19), while their tangent hyperplanes have the axis pattern
(17).  Thus the pure matrices, all eighteen clean colour-tagged windows,
their common null directions, and the selector failure belong to one common
root--blocker system.

### Theorem 3 (maximal window cover with zero rank-two co-occurrence)

There is a rational canonical common root--blocker system such that:

1. all three pure permanents are nonzero;
2. all eighteen colour-tagged graph-side windows in Theorem 2 are clean;
3. the port null directions can be chosen globally;
4. every nonzero marked-shore factorization has `rho(I)=1`; and
5. no graph-side window has a nonzero marked shore at a rank-two root pair.

Proof.  Assertions 1 and 3 follow from (19)--(22).  Theorem 2 gives assertion
2.  Equations (18), (20), and the fixed witnesses prove assertions 4--5.

Rank one cannot separate the two companion classes required by the current
clean top-window extraction.  Hence complete graph-side window coverage does
not imply even one rank-two response window under the present hypotheses,
and in particular does not imply four compatible marked-star response
sensors.

This is sharp at the level under discussion: eighteen is the entire
colour-tagged graph-side window family, while zero is the minimum possible
number of rank-two-coincident windows.

## 5. Revised legality boundary

The fan problem has two logically different layers:

```text
fixed-complement pure Laplace
    => all six windows per colour
    => graph-side tetrahedral fan on common port directions;

current pure/canonical/lower-frame hypotheses
    !=> a nonzero shore at a rank-two companion pair
    !=> legal marked-star fan.                        (23)
```

The next theorem must therefore couple a fixed retained pair `S` to more
than the pure Laplace expansion.  Sufficient possibilities include:

1. a weighted identity forcing `L_S(I)!=0` for some `rho(I)>=2` **for that
   fixed `S`**, not merely after summing over windows;
2. a non-star companion row that separates the required deletion classes at
   a rank-one shore;
3. a mixed-colour equation that couples the different root pairs selected by
   the four graph-side fan windows; or
4. a direct marked-star extraction whose observation matrix bypasses the
   two-class top selector.

The fixed-complement identity removes window existence from the list of
unknowns.  Selector co-occurrence and marked-star exposure are the exact
remaining bottleneck.

## Scope wall

```text
six graph-side windows in each pure colour:        PROVED;
all eighteen colour-tagged graph-side windows:     PROVED;
tetrahedral fan occurrence:                        PROVED GRAPH-SIDE;
one common null direction per double blocker:      PROVED;
rank-two shore co-occurrence from current data:    IMPOSSIBLE TO FORCE;
legal top selectors on the fan:                    UNKNOWN;
legal marked-star rows on the fan:                 UNKNOWN;
empty-face observability:                          UNKNOWN;
partition-closed P7 response window:               UNKNOWN;
P7 nonrestriction:                                 UNKNOWN;
global Krenn--Gu conjecture:                        UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_p7_fixed_complement_laplace_fan_cover_and_selector_separation.py
python audit_p7_fixed_complement_laplace_fan_cover_and_selector_separation.py
python -m py_compile verify_p7_fixed_complement_laplace_fan_cover_and_selector_separation.py audit_p7_fixed_complement_laplace_fan_cover_and_selector_separation.py
uv run --with ruff ruff check verify_p7_fixed_complement_laplace_fan_cover_and_selector_separation.py audit_p7_fixed_complement_laplace_fan_cover_and_selector_separation.py
```

The primary verifier proves the six generic polynomial identities, checks the
fan inclusion, reconstructs the common canonical system, and verifies every
displayed exact countermodel statement.  The independent no-import audit
uses a separate integer permanent routine, the matching-bijection form of
fixed-complement Laplace, and rational row reduction.  These bounded replays
audit the formulas; the matching partition in Theorem 1 is the symbolic
proof for arbitrary matrices.
