# P7 deletion-cube observability and the clean-window boundary

## Status

**Exact characteristic-zero observability theorem and P7 boundary.**  This note
introduces a small linear theory for deciding which complementary hafnian
cofactors are recoverable from legal root jets.  It then applies that theory to
the canonical five-root, seven-blocker, two-residual cell.

There are two new conclusions.

1. Every nonzero pure `P_5` restriction in the canonical minimal blocker
   profile contains a **clean graph-side four-port window**.  Three fixed roots
   can be forced onto a three-blocker shore, leaving four double-type blockers
   and the two residual vertices.  The proof is the symbolic identity

   ```text
   sum_(|J|=|D|=3, t in D)
      per H[J,D] per H[R\J,B_c\D] = 6 per H.          (1)
   ```

   Here `H` is the nonzero `5 x 5` pure root--blocker matrix, `t` is its
   triple-blocker column, and `B_c` is its five-column pure blocker base.

2. This window is not yet a partition-closed response chart.  A legal
   two-root companion selector may recover the two **top** coefficients
   `m_W` and `z_W`, but the two-residual dual-Wick equation also needs the
   empty and pair coefficients on `W`.  Those lower faces do not follow from
   the top face: an exact one-parameter family of legal two-residual graph
   responses has fixed `(m_1234,z_1234)=(0,1)` and varying lower response.

Thus the old statement "the lower jets do not expose a four-cube" can now be
sharpened.  A clean four-window is forced on the graph side of the minimal
cell; what is missing is a legal left inverse that exposes a
**partition-closed deletion cube** on that same window.  This is a precise
observability deficit, not evidence that the desired cube is impossible.

The note does not exclude the P7 cell, construct a GHZ realization, or prove
the Krenn--Gu conjecture.  The P7 branch and the global conjecture remain
**UNRESOLVED**.

## 1. Deletion-cube observability

Let `E` be a finite-dimensional space of legal root probes and `V` the tensor
space carried by the uncontracted blockers.  A mixed root jet has the exact
deletion-class form

```text
T = sum_(a in A) g_a tensor C_a in E tensor V,         (2)
```

where `C_a` is a complementary principal-hafnian cofactor and `g_a` is the
companion form that created its deletion class.  Let `P subset E^*` be the
space of legal linear probes.  Its observation map is

```text
O_P : P -> k^A,
ell |-> (ell(g_a))_(a in A).                           (3)
```

The cofactor family is hidden state; a legal jet is an observation of that
state.  This elementary viewpoint matters because a polynomial identity on
principal deletions can be applied only after the required deletion classes
have actually been recovered.

### Theorem 1 (selector/observability criterion)

For `d=(d_a) in k^A`, the combination `sum_a d_a C_a` can be recovered by a
linear combination of legal probe outputs for every cofactor family if and
only if

```text
d in rowspace O_P.                                    (4)
```

In particular, every `C_a` can be selected individually if and only if
`O_P` has full column rank.  If `lambda in ker(g_a -> sum lambda_a g_a)`,
then for every `S in V` the deformation

```text
C_a |-> C_a + lambda_a S                              (5)
```

leaves `T` unchanged.  Hence no argument using only that jet can distinguish
the deformed cofactor family.

Proof.  Applying `ell in P` to (2) gives

```text
(ell tensor id)(T)=sum_a ell(g_a) C_a.                (6)
```

The obtainable coefficient vectors are exactly the row space of (3), proving
(4).  Full individual recovery is equivalent to containing every coordinate
row, hence to full column rank.  Under (5), the change in (2) is

```text
(sum_a lambda_a g_a) tensor S=0,                      (7)
```

which proves the kernel statement.

For two companion classes the familiar failure is already exact.  If the
only observed form is `g_0+mu g_1`, then only `C_0+mu C_1` is visible and

```text
(C_0,C_1) |-> (C_0+mu S,C_1-S)                        (8)
```

is invisible.  Conversely, two independent companion forms have dual
selectors and expose both cofactors.

### Definition 1 (partition-closed deletion chart)

For a port set `W`, a response chart is partition-closed through order `d`
if it individually exposes the two principal response families

```text
m_S=haf(B[S]),
z_S=haf(G[Q union S])                                  (9)
```

for every even `S subset W` with `|S|<=d`.

This is the natural data object for residual-relative response polynomials.
Indeed, the coefficient recursion for `Phi=M^(-1)Z` is an incidence-algebra
convolution over all proper subsets of `S`.  A top coefficient without its
proper even subsets is not a domain on which that recursion can be evaluated.

For two residual vertices and `W={1,2,3,4}`, the required degree-four
dual-Wick equation is

```text
z_W - h m_W
    - sum_(P subset W, |P|=2) (z_P-h m_P)m_(W\P)=0,    (10)
```

where `h=z_empty`.  Thus knowing only `(m_W,z_W)` does not test (10).

## 2. The canonical seven-blocker cell

Use the active notation

```text
R={r_0,...,r_4},        |R|=5,
B,                      |B|=7,
Q={q_0,q_1}.                                             (11)
```

In the minimal incidence cell the blocker types are

```text
012, 01,01, 02,02, 12,12.                              (12)
```

For each colour `c`, the two blockers missing colour `c` can be restricted to
their simultaneous-kernel direction.  The other five blockers form a pure
`P_5` system.  Denote that five-column set by `B_c`; it consists of the unique
triple blocker `t` and four double blockers.  After evaluating the pure
directions, write its scalar root--blocker matrix as

```text
H=(H_(r,b))_(r in R,b in B_c),       per H != 0.        (13)
```

The nonvanishing is forced by the nonzero GHZ pure coefficient.

### Lemma 2 (marked permanental Laplace identity)

For every `5 x 5` matrix `H` and every marked column `t`, identity (1) holds.

Proof.  Expand a product

```text
per H[J,D] per H[R\J,B_c\D]                           (14)
```

as pairs of bijections.  Their disjoint union is a unique full bijection
`sigma:R->B_c`.  Conversely, a fixed `sigma` contributes precisely when
`D=sigma(J)` and `t in D`, equivalently when the root `sigma^(-1)(t)` belongs
to `J`.  A three-subset `J` containing that root is obtained by choosing two
of the other four roots, so `sigma` is counted

```text
binom(4,2)=6                                           (15)
```

times.  Summing over full bijections proves (1).  This is a symbolic marked
Laplace count, not a search through blocker configurations.

### Corollary 3 (nonzero shore with double-only complement)

If `per H !=0`, there exist a root triple `J subset R` and a column triple
`D subset B_c`, with `t in D`, such that

```text
per H[J,D] !=0,
per H[R\J,B_c\D] !=0.                                 (16)
```

Put

```text
I=R\J,                  |I|=2,
W=B\D,                  |W|=4.                        (17)
```

Every blocker in `W` is double type: `D` contains the unique triple blocker,
and every other blocker of `B` has double type.

Proof.  The right side of (1) is nonzero.  In characteristic zero, at least
one summand on the left is nonzero, so both factors in that summand are
nonzero.  The type assertion follows from (12).

The characteristic-zero hypothesis is used exactly here.  The factor six
must not vanish.

## 3. A clean graph-side four-window

For a blocker `w` and root triple `J`, let

```text
K_w(J)=intersection_(j in J) ker r_(j,w),              (18)
```

where `r_(j,w)` is the root--blocker covector at `w`.  A double-type blocker
has total root-row span of dimension at most two.  Therefore every `w in W`
from Corollary 3 has

```text
K_w(J) != 0.                                           (19)
```

Choose nonzero `z_w in K_w(J)` for all `w in W`, and retain on `D` the pure
directions used in (13).  Every edge from a root in `J` to a blocker in `W`
now vanishes.  If the two roots in `I` are saturated by a legal companion
matching, the three roots in `J` must be matched bijectively to `D`.  Their
common scalar factor is the nonzero number `per H[J,D]`.

### Theorem 4 (conditional clean-window extraction)

Let the two-root jet on `I` have the two companion deletion classes

```text
T_I = g_empty tensor C_I + g_Q tensor C_(I union Q).   (20)
```

If its legal observation map has rank two, dual selectors for `g_empty` and
`g_Q` exist.  After the contractions above, those selectors recover, up to
the same nonzero shore factor,

```text
z_W=haf(G[Q union W]),
m_W=haf(B[W]),                                         (21)
```

respectively.  Thus every canonical pure `P_5` chart contains a conditional
clean four-port response window.

Proof.  A root in `I` cannot use a blocker in the differentiated lower-jet
component.  In the `g_empty` class the pair `I` is saturated without deleting
`Q`; after the forced `J--D` matching, the remaining vertex set is `Q union
W`, giving `z_W`.  In the `g_Q` class the roots in `I` delete both residual
vertices; the remaining set is `W`, giving `m_W`.  Theorem 1 supplies the two
selectors, and the forced shore contributes the common nonzero factor from
(16).

The rank-two assumption is substantive.  If `g_empty` and `g_Q` are
proportional, (8) proves that this jet sees only one linear combination of
the two responses.  Existing lower-frame rank theorems sometimes force two
or three independent target columns, but the marked Laplace identity does
not yet guarantee that its particular complementary root pair `I` lies in
such a rank-two chart.

Nor does Theorem 4 claim that the chosen kernel directions are fully
supported GHZ modes.  It is a graph-side extraction.  Target compatibility
is a separate equation.

## 4. The top face does not determine the deletion cube

The gap between Theorem 4 and Definition 1 is genuine even inside the exact
two-residual graph-response variety.

### Proposition 5 (one-parameter top-face fibre)

Work over any characteristic-zero field and take `a !=0`.  On four ports set

```text
B_34=a,
R_(q_0,1)=1,
R_(q_1,2)=a^(-1),
A_(q_0,q_1)=0,                                         (22)
```

with all other edges zero.  In the square-zero response algebra,

```text
M_a = 1+a x_3 x_4,
Phi_a = a^(-1) x_1 x_2,
Z_a = M_a Phi_a
    = a^(-1)x_1x_2+x_1x_2x_3x_4.                      (23)
```

Consequently

```text
(m_1234,z_1234)=(0,1)                                 (24)
```

for every `a`, while

```text
m_34=a,                 z_12=a^(-1)                   (25)
```

vary.  Hence the projection from a partition-closed four-port response to its
top pair `(m_W,z_W)` is not injective, even on legal two-residual matching
responses.

Proof.  The only port edge is `34`, so `M_a=exp(a x_3x_4)` gives the first
formula.  The only way to use both residual vertices is through ports `1,2`,
so the residual-relative factor is `a^(-1)x_1x_2`.  Multiplication in the
square-zero algebra gives (23), and coefficient extraction gives (24)--(25).

This proposition is not a P7 counterexample.  It proves the narrower—and
needed—logical statement that top-window exposure alone cannot license the
four-point dual-Wick equation.

## 5. Exact location of the missing data

For the active two-residual P7 cell, the currently proved legal lower-frame
classes have the schematic labels

```text
C_empty,
C_I and C_(I union Q) for root pairs I,
C_(R union {q_0}) and C_(R union {q_1}).               (26)
```

By contrast, a four-port response on `U subset B` has deletion label

```text
z_U = C_(R union (B\U)).                               (27)
```

When `|U|=4`, (27) deletes three blockers; when `|U|=6`, it deletes one.
None of the classes in (26) deletes a blocker.  The top coefficient in
Theorem 4 appears only after the additional shore contraction; its pair and
empty faces do not appear automatically.

The smallest previously studied four-terminal hidden overlay tells the same
story in linear-algebraic form.  Its six hidden pair classes map onto four
visible values with a two-dimensional kernel.  In the ordering

```text
(x_01,x_02,x_03,x_12,x_13,x_23),                      (28)
```

the invisible directions are

```text
(-s-t,s,t,t,s,-s-t).                                  (29)
```

Theorem 1 identifies (29) as an observation-kernel deformation.  It cannot
be removed by simply naming the hidden classes.

A formal vacuum/Mobius extension would recover subset faces by inclusion and
exclusion, but a local graph tensor has no legal vacuum value: setting a
physical vector to zero annihilates the tensor instead of deleting that
vertex.  Such an extension is therefore conditional until a legal
dummy/herald/selector gadget is proved.

## 6. What would close the P7 response route

The dual-Wick route would become applicable on the clean window if one proves
either of the following.

1. **A partition-closed selector theorem:** legal jets and shore contractions
   whose combined observation matrix has full column rank on

   ```text
   {m_S,z_S: S subset W, |S| even}.                    (30)
   ```

2. **A projected identity:** an elimination of the lower faces from the
   dual-Wick ideal that yields a nonzero polynomial depending only on the
   presently visible top and overlapping-window data.

The clean-window theorem reduces the geometric search: there is no longer a
need to invent four surviving double-type ports.  They are forced by (1).
The remaining problem is an observability/gluing problem across companion
selectors and overlapping marked shores.

This creates a useful translation dictionary.

```text
principal hafnian deletions     hidden state
legal mixed root jets           observation channels
companion forms                 observation matrix columns
kernel cofactor deformations    unobservable state directions
dual-Wick subset recursion      Boolean-lattice state equation
overlapping clean shores        multi-chart sensor fusion
```

The relevant tools are therefore not limited to hafnian identities.  Linear
systems observability, matroid rank of selector columns, incidence-algebra
elimination, apolar/catalecticant recovery, and sheaf-like gluing of
overlapping local charts all become legitimate symbolic approaches.  No one
of those analogies is used as a theorem here; Theorems 1 and 4 state the exact
algebra that any such transfer must respect.

## Scope wall

Proved here:

- the exact selector/observation criterion and its invisible-deformation
  kernel;
- the marked permanental Laplace identity (1);
- existence of a nonzero three-root shore whose four-port complement consists
  only of double blockers;
- conditional exposure of the full four-port coefficients `(m_W,z_W)`;
- an exact legal response fibre proving that those top coefficients do not
  determine the partition-closed four-port cube.

Not proved here:

- rank two for the companion forms belonging to the shore produced by (1);
- target-compatible nonzero GHZ values on the chosen kernel directions;
- legal exposure of all pair/empty responses on one common window;
- a projected dual-Wick obstruction using only visible data;
- exclusion or realization of the P7 cell;
- the Krenn--Gu conjecture.

All six items remain **UNKNOWN/UNRESOLVED**.

## Replay

```powershell
uv run --with sympy python verify_p7_deletion_cube_observability_and_clean_window_boundary.py
python audit_p7_deletion_cube_observability_and_clean_window_boundary.py
uv run --with sympy --with ruff python -m ruff check verify_p7_deletion_cube_observability_and_clean_window_boundary.py audit_p7_deletion_cube_observability_and_clean_window_boundary.py
python -m py_compile verify_p7_deletion_cube_observability_and_clean_window_boundary.py audit_p7_deletion_cube_observability_and_clean_window_boundary.py
```

The primary verifier checks (1) over a generic symbolic `5 x 5` matrix by
subset dynamic programming, verifies the exact selector kernels, audits the
blocker-deletion labels, and multiplies the square-zero response fibre.  The
independent no-import audit uses a separate integer permanent recurrence,
rational coefficient dictionaries, and direct row-space checks.  These
bounded calculations audit the displayed identities.  The marked-bijection
proof, the observation-space proof, and the matching construction prove the
statements over characteristic zero.
