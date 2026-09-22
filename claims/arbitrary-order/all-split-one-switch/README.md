# One-switch obstruction for the color-regular all-split parent

Date: 2026-09-22

## Status

This package records a **proved finite mechanism obstruction** and one open
all-order lemma.  It does not exclude the all-split family and does not
resolve the Krenn--Gu conjecture.

The exact finite control and its exhaustive replay show that one oriented
one-switch system, by itself, is compatible with every binary-Hamilton and
resource-cycle condition supplied by the current all-split reduction.  A
proof of the parent must use the opposite orientation, a multi-switch word,
or another full-source equation.

## Parent, supply, and consumer

The parent is the residual obligation in
[`COLOR_REGULAR_ALL_SPLIT_SOURCE_REDUCTION.md`](../COLOR_REGULAR_ALL_SPLIT_SOURCE_REDUCTION.md).
Its hypotheses are the protected K4 scaffold on `k>=2` components, hollow
all-split color-regular crossing support, and the full source equations.
The reduction supplies:

1. the three protected matching involutions `m_a,m_b,m_c`, with
   `m_a m_b=m_c` on every K4;
2. Hamilton binary transitions `D_ab` for all ordered color pairs;
3. one hollow colored resource cycle `F=C_(6k)`; and
4. the boundary-hitting condition for every nonconstant switched label
   word.

The intended consumer is an all-order exclusion of the all-split residual.
This package narrows that consumer to a genuinely bidirectional or
multi-switch argument.

## The two oriented one-switch systems

Fix a base color `a`, write the other colors as `b,c`, and set

```text
P=D_ab,                 Q=D_ac.
```

For an `M_a` resource `R`, define `H_R(P->Q)` to equal `P` away from the two
vertices of `R` and to use the two `Q` arcs on `R`.  Define `H_R(Q->P)` by
interchanging `P,Q`.

The **forward root condition** says that `H_R(P->Q)` has a directed cycle
containing both endpoints of `R`, for every `R`.  The **reverse root
condition** is the same statement for `H_R(Q->P)`.

These are weaker than the actual one-switch boundary equations.  If `R^-`
is the predecessor `M_a` resource determined by the intermediate `b--c`
edge of the oriented resource cycle, forward boundary saturation requires
every directed cycle of `H_R(P->Q)` to contain all four endpoints of
`R^-` and `R`.  Reversing the constant and exceptional labels supplies the
opposite oriented system.  Therefore a hypothetical full source supplies
both root conditions, and in fact supplies both stronger predecessor
conditions.

The remaining clean proposition is:

> **Bidirectional K4 straddling lemma (open).** Let `|V|=4k`.  Let
> `m_a,m_b,m_c` be the protected K4 involutions, so `m_a m_b=m_c`.  Let
> `P,Q` be hollow Hamilton permutations satisfying
> `P m_a P^-1=m_b` and `Q m_a Q^-1=m_c`.  Then some `M_a` resource `R`
> fails the forward or reverse root condition.

This proposition would exclude the all-split residual.  It is not proved
here.

The unrestricted cyclic-order/root-condition argument, with the physical
K4 hypotheses omitted, is false.  For example, take

```text
m=(01)(23)(45),
P=(0 1 2 3 4 5),
Q=(0 1 4 5 2 3).
```

Every `m` pair satisfies both oriented root conditions.  This six-vertex
control lies outside `|V|=4k` and physical hollowness, and
`P m P^-1,Q m Q^-1` do not form the required K4 Klein triple with `m`.
It therefore refutes only a proof from unrestricted cyclic orders; it does
not isolate the necessity of the Klein relation while retaining the other
physical hypotheses.

## Exact forward-only control

The replay uses `k=5`, so `V={0,...,19}`.  Within each component the
protected matchings are

```text
A={(0,1),(2,3)},   B={(0,2),(1,3)},   C={(0,3),(1,2)}.
```

Resource indices are component-major.  The base-`A` binary transitions are

```text
P=D_AB = {0:13,1:15,2:19,3:17,4:18,5:16,6:11,7:9,8:3,9:1,
          10:5,11:7,12:10,13:8,14:2,15:0,16:14,17:12,18:6,19:4},

Q=D_AC = {0:12,1:15,2:6,3:5,4:1,5:2,6:11,7:8,8:3,9:0,
          10:14,11:13,12:18,13:17,14:19,15:16,16:9,17:10,
          18:7,19:4}.
```

They induce the hollow resource maps

```text
FAB=(7,9,8,5,1,3,4,0,6,2),
FAC=(6,3,1,4,0,7,9,8,5,2).
```

For roots `R=0,...,9`, the unique cycles of `H_R(P->Q)` have lengths

```text
16,14,13,15,18,13,11,11,11,18.
```

The predecessor compatibility graph contains the Hamilton cycle

```text
0 -> 1 -> 2 -> 3 -> 6 -> 5 -> 4 -> 8 -> 9 -> 7 -> 0.
```

Using these arcs for the `B--C` resource matching produces one hollow
resource cycle `C_30`.  Exactly 160 of the `2^10` endpoint orientations of
those `B--C` edges make `D_BC` Hamilton.  For every one of those 160
orientations:

* `D_AB,D_AC,D_BC` are Hamiltonian;
* every forward base-`A` one-switch row is saturated by its actual
  predecessor resource;
* the corresponding systems for bases `B,C` fail; and
* the reverse base-`A` root condition fails except at roots `0,9`.

This is an exact support/mechanism control, not a full source.  Switching
root `A_1={2,3}` in the reverse direction gives the cycle

```text
(0,12,18,7,8,3,17,10,14,19,4,1,15,16,9).
```

With colors `A=0,B=1,C=2`, the resulting literal physical word is

```text
(2,2,0,2,2,0,0,2,2,2,2,0,2,0,2,2,2,1,2,2).
```

The cycle omits one endpoint of the switched root, so it cannot saturate the
reverse boundary.  The switched-cycle coefficient formula from the parent
reduction consequently gives a nonzero mixed coefficient.

There is also a two-switch base-`A` failure.  In the canonical signed ladder,
the nonconstant label word

```text
(0,0,0,0,0,0,0,1,0,1)
```

has the directed cycle

```text
(16,14,19,4,18,7,9,1,15)
```

Its literal physical word is

```text
(0,1,0,0,2,0,0,2,0,1,0,0,0,0,1,1,2,0,1,2),
```

and the displayed cycle does not hit its `0->1` boundary at root `9`.
Labels above are written in
component-major resource-index order, while adjacency uses the resource-
cycle order

```text
(0,1,2,3,6,5,4,8,9,7).
```

Thus the two entries labelled `1` are consecutive around the actual
resource cycle and create exactly one `0->1` boundary.  The associated mixed
physical word also has nonzero coefficient under the exact switched-cycle
formula.  These witnesses explicitly show why the control is not a source.

## Consequences for proof design

The control disproves each of the following forward-only shortcuts:

* binary Hamiltonicity forces some one-switch row to lack a predecessor;
* a contained full root always gives a smaller switched cycle;
* a globally shortest switched cycle contains no other full root; and
* a Hamilton predecessor assignment cannot exist.

Thus the next all-order proof must couple the two oriented systems or use a
multi-switch/full-word equation.  Global sign parity, unoriented chord
interlacing, and forward-only cycle minimality are insufficient.

## Replay

Run from repository root:

```text
python claims/arbitrary-order/all-split-one-switch/replay.py
```

The script uses only the Python standard library and exact finite
enumeration.  It checks the resource maps, hollowness, the single `C_30`,
all binary Hamilton conditions, all forward one-switch rows, reverse-row
failure, the explicit mixed witness, and the count of 160 Hamilton
`B--C` endpoint orientations.

The replay is a finite proof of this mechanism obstruction.  It is not an
all-order case cover and is not evidence that the global conjecture is
resolved.
