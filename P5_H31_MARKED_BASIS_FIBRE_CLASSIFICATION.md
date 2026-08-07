# Complete marked-basis obstruction on the known finite component chart

## Status

This is an exact characteristic-zero classification and obstruction.

For every finite-parameter member of the five-parameter all-rank-two
family in
[`P4_DECOMPOSABLE_RANK_TWO_FAMILY.md`](claims/p4/classifications/pair-geometry/decomposable-rank-two-family/P4_DECOMPOSABLE_RANK_TWO_FAMILY.md),
classify every marked row basis over its four planes that admits a
neighbouring binary `Delta_2` slice.  Every such binary extension has an
injective one-marked map in at least one mode and a transverse pure
coordinate.  Consequently none can lift to an `H31` restriction.

Thus the **entire marked-basis fibre** over the known finite family is
excluded, not only the canonical marked section or the dense shifted
section from
[`P5_H31_MARKED_BASIS_OPEN_BRANCH.md`](P5_H31_MARKED_BASIS_OPEN_BRANCH.md).

This does not classify the toric and Schubert boundary planes in the
projective closure of the component.  Moreover, the known component is
now proved **not** to be the only all-rank-two pure-compression
component; see
[`P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md`](claims/p4/components/diagonal-quadric/P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md).

## The marked-basis bundle

Normalize the family to `E=I=1` and put

```text
D=C+L,        A=1+LQ,        B=1+DQ,        D!=0.    (1)
```

Use kernel rows

```text
alpha_0=( 1,Q, 0,-A)
alpha_1=( L,1,-L,-L)
alpha_2=(-1,0, 1, 0)
alpha_3=( 0,0,-1, 1)                                (2)
```

and complementary pure-colour rows

```text
U_0=(0,1,D,C)
U_1=(0,0,1,1)
U_2=(0,1,0,L)
U_3=(1,0,1,0).                                      (3)
```

The restricted pure tensor has only

```text
coefficient(UUUU)=2D.                               (4)
```

The pure tensor determines the kernel line
`C alpha_r` inside each plane.  Up to nonzero row rescaling, every
marked basis over the same plane is therefore uniquely

```text
beta_r=U_r+t_r alpha_r,       t=(t_0,t_1,t_2,t_3).  (5)
```

Hence (5), not merely one displayed row section, is the complete affine
Borel fibre that must be checked.

The normalization loses no markings.  In the original parameters,
precompose all four maps by

```text
diag(EI,EI,E,1).
```

After nonzero row rescaling this sends

```text
(E,I,L,Q,C) -> (1,1,L,Q,C/(EI))
```

and bijectively sends the shift coordinates to

```text
(t_0, I t_1, t_2/I, t_3/(EI)).                      (6)
```

All binary diagonality conditions, marked-map ranks, and transverse
coordinate conditions are invariant under these invertible changes.

## The determinantal incidence

Fix a distinguished pure source coordinate `q`.  Delete `q`, append the
fifth source coordinate, and write its eight binary row entries as

```text
z=(x_0,x_1,x_2,x_3;y_0,y_1,y_2,y_3).
```

Let

```text
M_q(t) z=0                                           (7)
```

be the fourteen mixed binary coefficient equations, and let
`d_0(z),d_1(z)` be the two diagonal coefficients.  A binary `Delta_2`
extension exists exactly when

```text
z in ker M_q(t),       d_0(z)d_1(z)!=0.              (8)
```

This is a projection of a linear determinantal incidence, not an
enumeration of ambient local maps.

For `L!=0`, the common diagonal source action

```text
diag(1,L,1,1)
```

sets `L=1` and changes variables to

```text
c=C/L, qbar=LQ,
s=(t_0/L, L t_1, t_2/L, t_3).                       (9)
```

Exact characteristic-zero elimination of `z` after normalizing one
diagonal and inverting the other gives the table below.  For `L=0`,
`C!=0`; the analogous action `diag(1,C,1,1)` sets `C=1`.

## Complete binary-survivor table

Here `T,S` are arbitrary complex numbers.  Rows not listed are empty.

| distinguished `q` | parameter stratum | every surviving marking `t` |
| ---: | --- | --- |
| `0` | `L=0, Q!=0` | `(T,0,0,0)` |
| `0` | `L!=0, A=0, C!=0` | `(L,1/L,LD/C,0)` |
| `0` | `L!=0, B=0, C!=0` | `(-LD/C,0,0,0)` |
| `1` | `L!=0, B=0, L+2C!=0` | `(D,D/[L(L+2C)],0,0)` |
| `1` | `C=-L/2, Q=-2/L` | `(L/2,0,L,1)` |
| `1` | `C=-L/2, Q=-1/L` | `(0,1/L,-L,0)` |
| `1` | `C=-L/2, Q=0` | `(-L/2,0,L,1)` |
| `2` | `L=0` | `(T,0,0,0)` |
| `2` | `L!=0, QAB!=0` | `(-1/Q,0,L/A,0)` |
| `2` | `L!=0, A!=0, B=0` | `(T,0,L/A,0)` |
| `3` | `L!=0, Q!=0` | `(-1/Q,0,0,0)` |
| `3` | `L!=0, Q=0, C!=0` | `(-L,0,LD/C,1)` |
| `3` | `L=0, Q!=0` | `(T,0,0,0)` or `(0,0,0,S)` |
| `3` | `L=0, Q=0` | `(0,0,0,1)` |

The three isolated `q=1` rows are essential.  They lie on

```text
C=-L/2
```

and were invisible in a generic coefficient-field calculation.  At
`L=1,C=-1/2`, the specialized elimination basis is triangular:

```text
2s_0+qbar+1,
s_1+qbar^2+2qbar,
s_2-2qbar^2-4qbar-1,
s_3-qbar^2-2qbar-1,
qbar(qbar+1)(qbar+2).                                (10)
```

This gives exactly the three isolated markings in the table.

For comparison, the other normalized `L!=0` projections have terminal
factors

```text
q=0: (qbar+1)((c+1)qbar+1),
q=2: (s_0 qbar+1)((c+1)qbar+1),
q=3: s_3(s_3-1),                                    (11)
```

together with the linear equations recorded by the verifier.  Solving
their case splits gives precisely the displayed rows.

On `L=0`, the projection closures are

```text
q=0: <t_1,t_2,t_3>,
q=1: <1>,
q=2: <t_1,t_2,t_3>,
q=3: <t_1,t_2,t_0t_3>.                              (12)
```

Direct specialization of (7) resolves the nonclosed projection
boundaries: for `q=0,Q=0`, `d_0` vanishes on the whole kernel; for
`q=3,Q=0`, only `(0,0,0,1)` is an actual point.  This yields the
constructible, rather than merely Zariski-closed, table above.

## Every binary extension is ternarily obstructed

For a survivor, let `K=ker M_q(t)`.  The primary verifier supplies:

1. an explicit basis of `K`;
2. one or two maximal nonzero minors of `M_q(t)`, proving that the
   basis spans on the stated stratum;
3. the two diagonal linear forms on that basis; and
4. a cover by `4 x 4` one-marked minors.

Each useful marked minor factors as

```text
constant * d_0(z) * d_1(z) * ell(z),                (13)
```

where the listed residual linear forms `ell` have no common nonzero
zero on the relevant extension kernel.  Thus every `z` satisfying
(8), not only one chosen extension, makes at least one one-marked map
injective.

Three representative covers show the structure.

### Generic `q=2`

For

```text
t=(-1/Q,0,L/A,0)
```

a kernel basis is

```text
e_1=(1,0,0,-1; B/Q,1,0,0),
e_2=(1,L,-1,0; 1/Q,0,-L/A,-1).
```

Writing `z=u e_1+v e_2`, the diagonals are

```text
d_0=-2A(u+v),       d_1=2(Bu+v)/Q.                  (14)
```

The mode-two minor on rows `0137` and the mode-one minor on rows `0237`
reduce to two complementary residual factors.  More explicitly, useful
determinants include

```text
8u(u+v)A^2(Bu+v),
8(u+v)(Au+v)(Bu+v)/Q.                               (15)
```

If the first vanishes under (14), then `u=0`, and the second is
nonzero.

### Generic `q=3`

For `t=(-1/Q,0,0,0)`, write

```text
e_1=(1,0,0,-1; -B/Q,-1,0,0),
e_2=(1,1/Q,0,0; 0,0,-1/Q,0).
```

Then

```text
d_0=2(v-LQu),       d_1=-2Du.                       (16)
```

Two mode-two marked minors are

```text
-8QuD(u+v)(LQu-v),
-8uvD(LQu-v)/Q.                                     (17)
```

The first covers `u+v!=0`; if `u+v=0`, the second is nonzero by
(16).

### The `L=0,q=2` three-dimensional kernel

When `Q!=0`, choose kernel coordinates `(u,v,w)`.  After dividing by
the two diagonal forms, three marked minors have residual factors

```text
u-w,       u-Qv,       Qv+w.                        (18)
```

Their only common zero is `(0,0,0)`.  When `Q=0`, three mode-one
minors instead have residual factors `u,v,w`.

The remaining boundary rows have equally short covers.  They include
separate bases at `2C+L=0`, at the free-line point `T=D`, at
`S=0,1`, and at `Q=0`; no generic basis is silently specialized
through a pole or a rank drop.

For every mode used in these covers, the pure one-marked map has a
nonzero entry in the distinguished source-coordinate column.  In most
strata that entry is literally `1`; the exceptional entries are
nonzero multiples of `L`, which is already inverted.

## The `H31` contradiction

Let `G_r` be the third target-coordinate row in a mode whose
neighbouring one-marked map is injective.  All coefficients containing
one `G_r` must vanish on the binary `Delta_2` slice.  Injectivity forces

```text
G_r restricted to the neighbouring hyperplane = 0.
```

Hence `G_r` is supported only on the distinguished pure coordinate
`q`.  The transverse pure entry proved above forces that remaining
coordinate to vanish as well.  Thus `G_r=0`, contradicting rank three
of the full `H31` local map.

This proves:

```text
No marked basis over any finite member of the known five-parameter
all-rank-two pure-compression family lifts to H31.                  (19)
```

## Scope after this theorem

The marked-basis gap on the known finite family chart is closed.  The
genuine toric base boundary was subsequently closed in
[`P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md).
The nonzero preferred-chart divisor was subsequently closed in
[`P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md).
The first-plane infinity and internal `E=0` fibres were subsequently
closed in
[`P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md)
and
[`P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md).
Thus the complete marked fibre of the known component is closed.
The honest `H31` remainder is now:

1. the second diagonal-quadric component, whose complete fibre is open
   although one rational fibre is excluded in
   [`P5_H31_DIAGONAL_QUADRIC_COMPONENT_POINT_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_COMPONENT_POINT_OBSTRUCTION.md);
2. any further irreducible components of the all-rank-two pure `P_4`
   plane locus; and
3. the separate `H22` frontier.

No global Krenn--Gu conclusion follows yet.

## Verification

Run:

```text
python verify_p5_h31_marked_basis_fibre_classification.py
python audit_p5_h31_marked_basis_fibre_classification.py
```

Regenerate the two normalized Singular inputs, for any distinguished
`q=0,1,2,3`, with:

```text
python derive_p5_h31_marked_basis_fibre_elimination.py q \
  --absolute --normalize-l --direct-normalization --fast-groebner
python derive_p5_h31_marked_basis_fibre_elimination.py q \
  --absolute --normalize-c-l0 --direct-normalization --fast-groebner
```

The primary verifier reconstructs all mixed matrices from permanents,
checks the normalization actions, the projection-basis case splits,
every kernel basis and maximal-rank minor, every all-extension marked
minor cover, and every transverse pure entry.

The independent audit uses its own dynamic-programming permanents and
modular row reduction.  It checks the complete predicted marking
fibres over small finite fields and audits every projective binary
extension on those fibres.  The finite-field work is independent QA;
the elimination and identities above are the characteristic-zero
proof.
