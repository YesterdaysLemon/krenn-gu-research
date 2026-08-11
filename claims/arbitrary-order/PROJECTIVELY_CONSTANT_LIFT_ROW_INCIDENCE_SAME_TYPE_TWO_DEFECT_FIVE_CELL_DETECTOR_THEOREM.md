# Projectively constant lift: row-incidence same-type two-defect five-cell detector

## Status

**Exact conditional characteristic-zero detector theorem.**  Work in the
aligned common-two-row, projectively constant tight cell

```text
q=0,                  r=5,                  |B|=5.    (1)
```

For each outside mode put

```text
S_w=span(a_w,b_w),
D={w in B:dim S_w<=1}.                                (2)
```

Suppose `|D|=2`, both defects are degenerate, and they have the same type:

```text
AA: a_u,a_v!=0 and b_u=b_v=0;
BB: a_u=a_v=0 and b_u,b_v!=0.                         (3)
```

Then at least one non-aligned root has a nonzero complete two-open detector.
Together with the preceding mixed/zero and regular-defect theorems, this gives
conditional detection for **every aligned projective `q=0,r=5` cell with at
most two local `a/b` defects**.

This is not witness exclusion.  It does not treat a cell with three or more
defects, prove fixed-root injectivity, treat `q=0,r>=6` or `q>=1`, address an
unfactorized outside graph, or supply universal extraction/gluing.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Imported five-cell system

Use the hypotheses and notation of the
[`three-activity two-defect theorem`](PROJECTIVELY_CONSTANT_LIFT_THREE_ACTIVITY_AND_MIXED_DEGENERATE_TWO_DEFECT_FIVE_CELL_DETECTOR_THEOREM.md).
The four non-aligned roots are

```text
P={1,2,3,4}.                                          (4)
```

Their fixed five-mode restriction is

```text
P_5(h_1,h_2,h_3,h_4,b)
 =sum_(c=0)^2 X_c e_c^(tensor B),
X_0 X_1 X_2!=0.                                      (5)
```

Every local flattening of (5) has rank three, and every persistent root row
has full cross-mode span.  For a defect `w`, put

```text
R_(p,w)=P_4(h_p,a,a,b;B-{w}),
I_w={p in P:R_(p,w)=0}.                               (6)
```

Collective invisibility means that all four projective two-open coefficients
`C_i` vanish.  The preceding theorem then gives

```text
|I_u|>=2,        |I_v|>=2,
I_u intersection I_v!=empty,
P-(I_u union I_v)!=empty.                             (7)
```

Its exact common kernels are

```text
AA:
  h_u=-2 lambda a_u,
  h_v=-2 lambda a_v,
  h_t= lambda a_t                 at the three transverse t;

BB:
  h_u=-gamma b_u,
  h_v=-gamma b_v,
  h_t=alpha_t a_t+gamma b_t,
  sum_t alpha_t=0.                                   (8)
```

## 2. Imported row-incidence quotas

The five source rows of (5) are

```text
H={b,h_1,h_2,h_3,h_4}.                               (9)
```

For a source-row subset `Q subset H` and a mode `w`, define

```text
Z_w(Q)={c:e_c^* belongs to span{r_w:r in Q}}.         (10)
```

Two exact arbitrary-permanent results apply to (5).

1. The
   [`five-mode row-pair incidence theorem`](ARBITRARY_PERMANENT_FIVE_MODE_ROW_PAIR_INCIDENCE_THEOREM.md)
   says that for every pair `Q`, every `Z_w(Q)` is nonempty and

   ```text
   #{w:c in Z_w(Q)}>=2             for each c.        (11)
   ```

2. The
   [`kernel Hall hierarchy`](../p5/frontier/P5_KERNEL_HALL_HIERARCHY.md)
   says that for every triple `Q`,

   ```text
   #{w:c in Z_w(Q)}>=3             for each c.        (12)
   ```

A line contains at most one target coordinate point and a plane contains at
most two.  We use (11)--(12) only in these intrinsic incidence forms.

## 3. The inactive sets are diamonds

### Lemma 1 (same-type inactive-set size)

Under collective invisibility,

```text
|I_u|=|I_v|=2.                                        (13)
```

### Proof

The lower bounds are (7).  Consider `I_u` at the other defect `v`.

- In type `AA`, every `p in I_u` has `h_(p,v)` on the `a_v` line and
  `b_v=0`.
- In type `BB`, every `p in I_u` has `h_(p,v)` on the `b_v` line, together
  with the fixed row `b_v`.

If `|I_u|>=3`, four of the five fixed source rows at `v` therefore lie in one
line (counting the zero `b_v` in type `AA`), and only one row remains.  Their
local span has dimension at most two, contradicting the rank-three flattening
of (5).  Hence `|I_u|<=2`; the same argument applies to `I_v`.

By (7), two possibilities remain: `I_u=I_v`, or the sets form a diamond with
one common root and proper three-root union.

### Lemma 2 (`AA` cannot have equal inactive sets)

In type `AA`, `I_u!=I_v`.

### Proof

If `I_u=I_v={c,d}`, both rows lie in the one-dimensional common kernel (8).
Full root-row span makes their two kernel scalars nonzero, so `h_c,h_d` are
nonzero proportional row families.  Their local pair span is a line at every
one of the five modes.  Thus

```text
sum_(w in B) |Z_w({h_c,h_d})|<=5.                     (14)
```

But (11) requires two incidences for each of three colours, hence a total at
least six.  Contradiction.

### Lemma 3 (`BB` cannot have equal inactive sets)

In type `BB`, `I_u!=I_v`.

### Proof

If `I_u=I_v={c,d}`, use the source triple

```text
Q={b,h_c,h_d}.                                        (15)
```

At both defects its rows lie in the `b` line.  At every transverse mode they
lie in `S_t`, a plane.  Pair incidence makes each defect line contain exactly
one coordinate point.  Consequently

```text
sum_(w in B) |Z_w(Q)|<=1+1+2+2+2=8.                  (16)
```

The triple quota (12) requires three incidences for each of three colours, a
total at least nine.  Contradiction.

We may therefore label both same-type cases as

```text
I_u={c,x},       I_v={c,y},       z in P-(I_u union I_v).   (17)
```

The root `c` is inactive at both defects, `x` only after deleting `u`, `y`
only after deleting `v`, and `z` is active after either deletion.

## 4. The `AA` diamond is impossible

At every transverse mode, (8) and the one-sided kernel formulas give

```text
h_c,h_x,h_y in <a_t>.                                 (18)
```

All three displayed rows are nonzero there.  For example, if the scalar for
`h_x` vanished, the `A` collision kernel would make `h_x` zero at `v` and at
all three transverse modes, contradicting full root-row span.

At defect `u`, the pair `{b,h_p}` has local span `<h_(p,u)>` because `b_u=0`.
The nonempty pair incidence in (11) therefore makes every `h_(p,u)` a nonzero
coordinate covector.  Local rank three and (17) force the exact distribution

```text
u: h_c,h_y on <a_u>;  h_x,h_z on the other two coordinate axes.
v: h_c,h_x on <a_v>;  h_y,h_z on the other two coordinate axes.   (19)
```

Likewise, the pair `{h_c,h_x}` spans `<a_t>` at every transverse mode, so
each `a_t` is a coordinate covector.

Let `z_u,z_v` denote the target colours of the coordinate rows `h_(z,u)` and
`h_(z,v)`.

### Theorem 4 (`AA` detector)

The `AA` cell has some nonzero `C_i`.

### Proof

Assume collective invisibility and use (17)--(19).  The pure coefficient of
colour `z_u` in (5) is nonzero.

If `z_u=z_v`, its permanent would have to assign the single source row `h_z`
to both defect modes, which is impossible.

Suppose instead that `z_u!=z_v`.  In any pure-`z_u` source assignment, `h_z`
is forced at mode `u`.  At a transverse mode whose `a_t`-axis is not `z_u`,
the three rows `h_c,h_x,h_y` vanish on colour `z_u`; only `b` and `h_z` can
possibly supply that colour.  Since `h_z` is already used at `u`, at most one
such transverse mode can be filled by `b`.  Hence at least two of the three
transverse `a_t`-axes must have colour `z_u`.

The same argument for the nonzero pure-`z_v` coefficient forces at least two
transverse axes to have the distinct colour `z_v`.  Three modes cannot contain
two occurrences of each of two distinct colours.  This contradiction proves
the theorem.

## 5. The `BB` diamond is impossible

At defect `u`, the rows `b,h_c,h_y` lie in the `b_u` line; at defect `v`, the
rows `b,h_c,h_x` lie in the `b_v` line.  Local rank three makes `h_x,h_z`
independent modulo the first line and `h_y,h_z` independent modulo the second.

Pair incidence makes `b_u,b_v` coordinate covectors.  Write their colours as

```text
beta_u, beta_v.                                       (20)
```

Apply the triple quota to

```text
Q_x={b,h_c,h_x}.                                      (21)
```

At `v` its span is the `beta_v` line.  At `u` it is the plane
`span(b_u,h_(x,u))`.  At every transverse mode it lies in `S_t`.  Therefore
the total coordinate-incidence capacity is at most

```text
1+2+2+2+2=9.                                          (22)
```

The lower bound (12) is also nine.  Equality holds everywhere: the `u` plane
and every `S_t` are coordinate planes, and each target colour occurs in
exactly three of the five labels.  Applying the same argument to

```text
Q_y={b,h_c,h_y}                                       (23)
```

makes `span(b_v,h_(y,v))` a coordinate plane with the same exact degree
ledger.

Let

```text
mu_t     = colour missing from S_t,
mu_u^x   = colour missing from span(b_u,h_(x,u)),
mu_v^y   = colour missing from span(b_v,h_(y,v)).      (24)
```

At a transverse mode, the four rows `b,h_c,h_x,h_y` lie in `S_t`.  Local rank
three puts `h_z` outside that coordinate plane, so it is the only fixed source
row with a nonzero `mu_t` component.  If two transverse planes missed the same
colour, the corresponding nonzero pure coefficient in (5) would have to
assign `h_z` to both modes.  Thus

```text
{mu_t:t transverse}={0,1,2}.                          (25)
```

For `Q_x`, the singleton label at `v` is `{beta_v}` and the other four labels
are coordinate planes.  Exact degree three says that the four missing colours
consist of `beta_v` twice and each other colour once.  The three transverse
misses already use every colour once, so

```text
mu_u^x=beta_v.                                        (26)
```

Similarly,

```text
mu_v^y=beta_u.                                        (27)
```

The plane in (26) contains `b_u`, of colour `beta_u`, so
`beta_u!=beta_v`.

### Theorem 5 (`BB` detector)

The `BB` cell has some nonzero `C_i`.

### Proof

Assume collective invisibility.  At mode `v`, the rows `b,h_c,h_x` lie on the
`beta_v` axis, while `h_y` lies in the coordinate plane (27), which misses
`beta_u`.  Local rank three puts `h_z` outside that plane.  Hence `h_z` is the
only fixed source row with a nonzero `beta_u` component at `v`.

By (25), one transverse plane also misses `beta_u`; there too `h_z` is the
only source row with a nonzero `beta_u` component.  The pure-`beta_u`
coefficient of (5) would have to assign `h_z` to both modes, so it is zero.
This contradicts `X_(beta_u)!=0` and proves the theorem.

## 6. Exact residual boundary

Combining Theorems 4--5 with the preceding five-cell results gives

```text
q=0,r=5 with no local defects:                         DETECTED;
q=0,r=5 with one arbitrary local defect:               DETECTED;
q=0,r=5 with two defects of every possible type:       DETECTED;
q=0,r=5 with three or more local defects:              OPEN;
existence or exclusion of a witness in the cell:       OPEN;
fixed-root detector injectivity:                       UNKNOWN;
q=0,r>=6, q>=1, and unfactorized cells:                UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.         (28)
```

The lift, companion classification, collision kernels, root-row full span,
row-pair incidence, and kernel Hall quotas are imported at their existing
scopes.  The inactive-set size argument, same-type diamond reductions, and
the two pure-coefficient matching contradictions are proved here.  The
theorem has not been formalized in Lean.  Its preserved scope and adversarial
reconstruction are in the
[`2026-08-11 review record`](../../docs/audits/PROJECTIVELY_CONSTANT_LIFT_ROW_INCIDENCE_SAME_TYPE_TWO_DEFECT_FIVE_CELL_REVIEW_2026-08-11.md).

## Replay

Run from repository root:

```powershell
python claims/arbitrary-order/verify_projectively_constant_lift_same_type_two_defect_five_cell_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_same_type_two_defect_five_cell_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_same_type_two_defect_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_same_type_two_defect_five_cell_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_same_type_two_defect_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_same_type_two_defect_five_cell_detector.py
```

The primary verifier checks the inactive-set census, all coordinate-axis and
coordinate-plane incidence ledgers, and the pure-colour support permanents.
The independent no-import audit exhausts a larger over-approximated support
family from the raw pair/triple quotas.  Both are bounded convention and
falsification checks.  The arbitrary-field implication is the written Hall,
incidence, and no-perfect-assignment proof above.
