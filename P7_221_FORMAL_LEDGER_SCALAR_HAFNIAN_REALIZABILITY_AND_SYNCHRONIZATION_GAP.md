# The formal 2+2+1 cofactor ledger is scalar-hafnian realizable chart by chart

## Status

**Exact positive scalar result, with a strict synchronization boundary.**  Every
one of the three scalar colour charts of the formal cofactor ledger in
`P7_TWO_ENDPOINT_AXIS_MULTIPLICITY_REDUCTION_AND_221_COMMON_JET_MODEL.md` is
the complete prescribed part of the principal-hafnian vector of an explicit
seven-core, seven-terminal weighted graph.  The colour-0 and colour-1 graphs
are rational.  The colour-2 graph is defined over

```text
K=Q(rho),                  rho^2=21.                    (1)
```

Thus no scalar hafnian-condensation, inverse-minor, or principal-cofactor
obstruction can exclude the formal ledger.

This does **not** produce one physical graph.  The particular certificates
displayed here use incompatible terminal--terminal blocks, and they do not
cancel mixed blocker-colour words.  The later exact construction
[`P7_221_COMMON_TERMINAL_BLOCK_SCALAR_HAFNIAN_REALIZABILITY.md`](P7_221_COMMON_TERMINAL_BLOCK_SCALAR_HAFNIAN_REALIZABILITY.md)
removes the first defect: all three scalar charts admit realizations with one
common terminal block.  The still later diagonal-gluing theorem puts all
three pure charts into one tensor-valued physical block graph.  Mixed-word
cancellation remains unknown.

## 1. Scalar principal-hafnian translation

Let

```text
P={1,2,3,4,5,a,b},             Q={a,b},                (2)
```

where `a=q_0` and `b=q_1`, and let `Z` be seven core vertices.  In colour
chart `c`, the requested scalar cofactor is

```text
C_D^(c) = haf W_c[Z union (P\D)]                       (3)
```

for even deletion sets `D`.  The lower-root ledger prescribes all 35
coordinates with `|D|=4`, all seven with `|D|=6`, and 20 of the 21 with
`|D|=2`.  Only `C_Q` is free among the nonempty even deletions.  `C_empty` is
also outside the lower-root ledger.  Hence there are 62 prescribed scalar
values per chart and 186 in total.

Here is the entire prescribed ledger.  Entries are ordered `(c=0,c=1,c=2)`.

For `|D|=2`,

```text
D     C_D                       D     C_D
1a    ( 0, 1, 0)               1b    ( 0, 0, 1)
2a    ( 0, 0, 1)               2b    ( 0, 1, 0)
3a    ( 1, 0, 0)               3b    ( 0, 0, 1)
4a    ( 0, 0, 1)               4b    ( 1, 0, 0)
5a    ( 1, 0, 0)               5b    ( 0, 1, 0)
12    ( 0,-1, 1)               34    (-1, 0, 1)
13    ( 0, 0, 1)               14    ( 0, 0, 1)
23    ( 0, 0, 1)               24    ( 0, 0, 1)
15    ( 0, 1, 0)               25    ( 0, 1, 0)
35    ( 1, 0, 0)               45    ( 1, 0, 0).       (4)
```

For the ten root-pair-plus-`Q` deletions,

```text
D       C_D                     D       C_D
12ab    (0,1,0)                 34ab    (1,0,0)
13ab    (0,0,1)                 14ab    (0,0,0)
23ab    (0,0,0)                 24ab    (0,0,1)
15ab    (0,1,0)                 25ab    (0,0,0)
35ab    (0,0,0)                 45ab    (1,0,0).        (5)
```

Among the 20 triple-tag deletions, the only nonzero values are

```text
C_123a=(0,0,1),    C_124b=(0,0,1),
C_134a=(0,0,1),    C_234b=(0,0,1),
C_125a=(0,1,0),    C_345b=(1,0,0).                    (6)
```

Every other `C_ijka` and `C_ijkb`, for a three-subset `{i,j,k}` of
`{1,2,3,4,5}`, is `(0,0,0)`.  The five root-quartet values are

```text
C_1234=(0,0,1/7),
C_1235=C_1245=C_1345=C_2345=(0,0,0).                  (7)
```

Finally, the seven size-six values are

```text
C_1234ab=(0,0,1/7),
C_1235ab=C_1245ab=C_1345ab=C_2345ab=(0,0,0),
C_12345a=C_12345b=(0,0,0).                            (8)
```

Equations (4)--(8) list every prescribed coordinate; no unspecified zero is
being suppressed except through the exhaustive sentence following (6).

## 2. Rational coordinate-copy realizations for colours 0 and 1

Index the seven core vertices by the terminals:

```text
Z={z_1,z_2,z_3,z_4,z_5,z_a,z_b}.                      (9)
```

Join `p` only to `z_p`, with weight one, and put no edge between two
terminals.  Let `A_c` be the weighted graph on `Z`.  In colour 0 its nonzero
edges are

```text
A_0[3,a]=A_0[4,b]=A_0[5,a]=A_0[3,5]=A_0[4,5]=1,
A_0[3,4]=-1.                                          (10)
```

In colour 1 they are

```text
A_1[1,a]=A_1[2,b]=A_1[5,b]=A_1[1,5]=A_1[2,5]=1,
A_1[1,2]=-1.                                          (11)
```

All other core edges, including `[a,b]`, vanish.  In the graph remaining
after deletion of `D`, every surviving terminal `p` is forced to match
`z_p`.  The unmatched core vertices are precisely those indexed by `D`.
Consequently

```text
C_D^(c)=haf A_c[D],                  c=0,1.            (12)
```

This proves the values in (4) directly and reduces every higher prescribed
coordinate to a principal hafnian of the same displayed seven-vertex matrix.
Exact expansion gives all of (5)--(8).  The two free values selected by these
constructions are

```text
c=0: C_Q=0, C_empty=1;
c=1: C_Q=0, C_empty=1.                                (13)
```

The value `C_empty=1` is the unique all-coordinate-copy matching.

## 3. Exact colour-2 realization over Q(sqrt(21))

The colour-2 chart has a compact forced-factor construction.  Give terminal
`5` a private core vertex `z_*`, join them with weight `1/7`, and isolate
`z_*` and `5` from all other vertices.  The remaining terminals and core are

```text
U={1,2,3,4,a,b},       Z_6={z_1,z_2,z_3,z_4,z_5,z_6}. (14)
```

The only core--core edges are

```text
A[z_1,z_2]=1,       A[z_3,z_4]=1/rho,
A[z_5,z_6]=rho.                                         (15)
```

The core--terminal incidence rows, written as linear forms on `U`, are

```text
r_1=X_1+X_3,                 r_2=X_2+X_4,
r_3=X_a+X_1+X_3,             r_4=X_b+X_2+X_4,
r_5=X_1+X_3,                 r_6=X_2+X_4.              (16)
```

Put

```text
kappa=1+22/rho.                                         (17)
```

Every terminal--terminal edge on `U` is listed below:

```text
M_12=M_14=M_23=M_34=-kappa,
M_13=M_24=M_1a=M_3a=M_2b=M_4b=7,
M_1b=M_2a=M_3b=M_4a=-rho,
M_ab=1-rho.                                             (18)
```

There are no other edges.

Let

```text
G_T=haf W_2[Z_6 union T],                  T subset U.  (19)
```

The complete even six-port response needed here is

```text
G_empty=1.                                              (20)
```

For pairs,

```text
G_ab=1,
G_13=G_24=G_1a=G_3a=G_2b=G_4b=7,                      (21)
```

and the other eight pair responses vanish.  For four-subsets,

```text
G_1234=103/21,
G_123a=G_124b=G_134a=G_234b=0,                         (22)
```

while each of

```text
123b, 124a, 12ab, 134b, 13ab,
14ab, 234a, 23ab, 24ab, 34ab                           (23)
```

has response `7`.  Finally,

```text
G_1234ab=103/21+252 rho.                                (24)
```

The private pair gives the exact factorization

```text
C_D^(2) = 0                         if 5 is in D,
C_D^(2) = (1/7) G_(U\D)            if 5 is not in D.   (25)
```

Equations (20)--(25) reproduce every colour-2 entry of (4)--(8).  They also
fix the two unprescribed even coordinates as

```text
C_Q^(2)=103/147,
C_empty^(2)=103/147+36 rho.                             (26)
```

For a symbolic derivation of the response, use the squarefree Gaussian
coefficient identity

```text
haf W[S] = [prod_(v in S) X_v]
           exp(sum_(u<v) W_uv X_u X_v).                (27)
```

Contracting the six core variables in (15)--(16) first gives constant term
one and the following nonzero quadratic terminal response:

```text
K_12=K_14=K_23=K_34=1+22/rho,
K_1b=K_2a=K_3b=K_4a=K_ab=rho.                          (28)
```

All other `K_ij` vanish.  The direct block (18) is exactly the desired pair
response (21) minus (28).  Squarefree multiplication through degrees four
and six then gives (22)--(24).  This is coefficient extraction in one fixed
sparse expression, not a search for a graph.

### Theorem 1 (chartwise scalar realizability)

The 186 prescribed scalar coordinates in (4)--(8) are simultaneous
principal hafnians within their respective colour charts.  The constructions
(9)--(11) realize colours 0 and 1 over `Q`; (14)--(18) realizes colour 2 over
`Q(sqrt(21))`.

## 4. The synchronization gap is the remaining obstruction

The theorem is deliberately chartwise.  Write `M_c` for the restriction of
the displayed graph to the seven terminal vertices `P`.  Then

```text
M_0=M_1=0,              M_2 is the nonzero matrix (18). (29)
```

In a physical realization those terminal modes are fixed.  Their mutual
edge block cannot be chosen afresh after selecting a blocker colour chart.
Therefore the three graphs above do not glue to one physical graph.

Equation (29) is a boundary of these **particular certificates**, not a
universal no-go theorem.  The later common-terminal theorem cited above
constructs more general colour-0 and colour-1 core--terminal incidences using
exactly the colour-2 terminal block.  Thus terminal-block incompatibility is
now known to be removable.

There is a second, logically independent issue.  Monochromatic scalar charts
test only the pure coefficients `D_0`, `D_1`, and `D_2`.  In one tensor-valued
graph a perfect matching may take different blocker colours on different
edges, producing mixed words such as `D_0D_1...`.  Edgewise interpolation of
the three pure charts does not make those coefficients disappear.  Their
global cancellation must be proved separately.

Thus the exact status wall is

```text
formal 2+2+1 ledger, colour by colour:       REALIZED;
scalar principal-hafnian obstruction:        ABSENT;
one common terminal block, chartwise:          REALIZED LATER;
one tensor-valued graph on all pure charts:     REALIZED LATER;
mixed blocker-colour cancellation:           UNKNOWN;
full P7 restriction and global Krenn--Gu:     UNRESOLVED. (30)
```

See `P7_221_DIAGONAL_BLOCK_GLUING_AND_MIXED_WORD_BOUNDARY.md` for that later
pure-chart gluing theorem and the exact mixed word that survives in its
canonical diagonal lift.

## Replay

```powershell
uv run --with sympy python verify_p7_221_formal_ledger_scalar_hafnian_realizability_and_synchronization_gap.py
python audit_p7_221_formal_ledger_scalar_hafnian_realizability_and_synchronization_gap.py
python -m py_compile verify_p7_221_formal_ledger_scalar_hafnian_realizability_and_synchronization_gap.py audit_p7_221_formal_ledger_scalar_hafnian_realizability_and_synchronization_gap.py
uv run --with sympy --with ruff python -m ruff check verify_p7_221_formal_ledger_scalar_hafnian_realizability_and_synchronization_gap.py audit_p7_221_formal_ledger_scalar_hafnian_realizability_and_synchronization_gap.py
```

The verifier constructs only the three matrices displayed above and checks
all 186 prescribed values plus the six free values in (13) and (26) by exact
SymPy arithmetic.  It performs no support search, parameter sweep, or
graph-family enumeration.
The independent no-import audit implements exact arithmetic in
`Q(rho)/(rho^2-21)` and a separate hafnian recurrence, then reconstructs the
same 186 prescribed coordinates and all six displayed free values.
