# Adversarial review of the same-type two-defect detector

## Review status and provenance

This record reviews
[`PROJECTIVELY_CONSTANT_LIFT_ROW_INCIDENCE_SAME_TYPE_TWO_DEFECT_FIVE_CELL_DETECTOR_THEOREM.md`](../../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_ROW_INCIDENCE_SAME_TYPE_TWO_DEFECT_FIVE_CELL_DETECTOR_THEOREM.md)
as a conditional characteristic-zero detector theorem.

Codex reconstructed the inactive-set reduction, the imported permanent
incidence interface, and both pure-coefficient contradictions independently
of the primary verifier.  The standard-library audit separately exhausts an
over-approximated support family from raw pair/triple quota data.  This is
durable adversarial reasoning, not independent human review.

Review verdict: **accept complete two-open detection for the `AA` and `BB`
two-degenerate-defect cells**, after the focused and repository-wide replay
gates pass.  Combined with the preceding theorem, every aligned projective
`q=0,r=5` cell with at most two local defects is detected.  Three-or-more
defect cells remain open.  No witness is excluded, and global Krenn--Gu
remains **UNRESOLVED**.

## 1. Reconstructed obligation

The preceding theorem leaves two same-type cells.  Under collective
invisibility, their inactive root sets satisfy

```text
|I_u|,|I_v|>=2,
I_u intersection I_v!=empty,
I_u union I_v proper in the four-root set.             (1)
```

The reviewed proof must not infer a contradiction merely from the existence
of a common collision kernel.  It must instead connect those kernels to exact
constraints of the fixed restriction

```text
P_5(h_1,h_2,h_3,h_4,b)=sum_c X_c e_c^(tensor 5),
X_0 X_1 X_2!=0.                                       (2)
```

The required bridge is supplied by already proved permanent row-incidence
quotas, not by a genericity assumption.

## 2. Imported incidence interface

For a selected source-row set `Q`, let `Z_w(Q)` be the target coordinate
covectors contained in its local row span.  Two prior exact results give:

```text
|Q|=2: every Z_w(Q) is nonempty,
       and each colour occurs in at least two modes;

|Q|=3: each colour occurs in at least three modes.     (3)
```

The first line uses the five-mode row-pair incidence theorem as well as its
kernel-deletion colour quotas.  The second is the all-subset kernel Hall
hierarchy.  Both apply because (2) is itself a concise `P_5 -> Delta_3`
restriction on source rows `{b,h_1,h_2,h_3,h_4}`.

The review checked that no argument reverses (3): the proof uses only the
necessary incidence counts.  A local line contributes at most one coordinate
point, and a local plane at most two.

## 3. Exact inactive-set census

For a root in `I_u`, the retained collision kernel controls its value at the
other defect `v`.

- In `AA`, those values lie on the `a_v` line and `b_v=0`.
- In `BB`, those values and the fixed `b_v` row lie on the `b_v` line.

Three inactive roots would leave at most one additional fixed source row, so
the local span at `v` would have dimension at most two.  Local rank three
therefore gives

```text
|I_u|=|I_v|=2.                                        (4)
```

Together with (1), the sets are either equal or form a three-root diamond.

The equal alternatives really are excluded by different arguments:

- the `AA` common kernel is one-dimensional, so the two common root families
  are proportional at all five modes; five line labels cannot supply the six
  pair incidences required by (3);
- in equal-set `BB`, the triple consisting of `b` and the two common roots has
  line/line/plane/plane/plane capacity `8`, below the required `9`.

Thus both cells have the exact diamond form

```text
I_u={c,x},       I_v={c,y},       z outside the union. (5)
```

The primary obtains six equal and twenty-four ordered diamond patterns.  The
audit reconstructs the same counts from four-bit masks.

## 4. `AA` support contradiction

At the three transverse modes, the common root and the two singly inactive
roots are nonzero multiples of `a_t`:

```text
h_c,h_x,h_y in <a_t>.                                 (6)
```

At an `A` defect, `b=0`.  Pair incidence for `{b,h_p}` therefore makes every
root value a nonzero coordinate row.  Local rank three forces the patterns

```text
u: c,y share a_u; x,z occupy the other two axes;
v: c,x share a_v; y,z occupy the other two axes.       (7)
```

Pair incidence for `{c,x}` makes each transverse `a_t` a coordinate axis.

Let `z_u,z_v` be the coordinate colours of row `z` at the two defects.  If
they agree, the corresponding pure coefficient would assign `z` twice.  If
they differ, a pure `z_u` assignment uses `z` at `u`; at every transverse mode
whose `a_t` colour is not `z_u`, only `b,z` can carry that colour, and only
`b` remains unused.  Hence at least two transverse `a_t` axes must have colour
`z_u`.  The same reasoning forces at least two to have the distinct colour
`z_v`, impossible on three modes.

This is a support-level zero: no permanent assignment exists.  It does not
assume positivity or rule out cancellation by numerical coefficients.

## 5. `BB` incidence and support contradiction

In the diamond (5), `b,c,y` share the `b_u` line and `b,c,x` share the `b_v`
line.  Call their coordinate colours `beta_u,beta_v`.

For the triple `{b,c,x}`, the local spans have capacities

```text
u plane, v line, three transverse S_t planes: 2+1+2+2+2=9.   (8)
```

Triple Hall also requires nine incidences, so equality holds everywhere:
the `u` plane and all three `S_t` are coordinate planes, and every colour has
degree exactly three.  The analogous triple `{b,c,y}` gives a coordinate
plane at `v` with the same exact ledger.

Let `mu_t` be the colour missing from `S_t`.  The four rows `b,c,x,y` lie in
that plane, while local rank puts `z` outside.  Thus `z` is the unique source
for `mu_t`.  Two equal transverse misses would kill the corresponding pure
coefficient, so the three misses are distinct.

Counting absent colours in the exact degree-three ledgers now gives

```text
span(b_u,x_u) misses beta_v,
span(b_v,y_v) misses beta_u.                           (9)
```

The first plane contains `beta_u`, so `beta_u!=beta_v`.  At mode `v`, every
row except `z` lies in the plane that misses `beta_u`; the same is true at the
unique transverse plane missing `beta_u`.  The pure-`beta_u` coefficient
would therefore assign `z` twice and is zero, contradicting (2).

Again, this is a no-assignment proof, not a sign or generic-magnitude
argument.

## 6. Computational independence

The primary verifier uses explicit source-support permanents and a structured
derivation of the AA axis cases and BB missing-colour ledgers.  It checks:

- the six equal and twenty-four diamond inactive-set patterns;
- 972 AA coordinate charts, split into 324 equal-`z` and 648 distinct-`z`
  cases;
- 972 BB coordinate-plane charts;
- 54 raw BB triple-quota ledgers and 36 exact distinct-missing ledgers; and
- zero surviving charts with all three pure coefficients supported.

The audit imports no repository code and no computer algebra.  It uses bitmask
supports, recursive bipartite matching rather than a permutation permanent,
and raw enumeration from the pair/triple quota inequalities.  Its support
sets deliberately over-approximate the unknown `b,z` entries; failure even in
that larger family is a valid falsification check.

Neither finite chart family proves the arbitrary-field incidence theorems.
Those are imported written results.  The new arbitrary-field implication is
the written inactive-set, capacity, and no-perfect-assignment argument.

## 7. Exact acceptance boundary

Accepted:

- size-two inactive sets for either same defect type;
- exclusion of the equal-set `AA` and `BB` patterns;
- complete detection of the remaining `AA` diamond;
- complete detection of the remaining `BB` diamond; and
- conditional detection of every aligned projective `q=0,r=5` cell with at
  most two local defects, after importing the preceding detector theorems.

Still open:

- every aligned projective `q=0,r=5` cell with at least three local defects;
- fixed-root injectivity and existence or exclusion of a witness;
- `q=0,r>=6`, every `q>=1` cell, and the unfactorized branch;
- universal extraction/gluing; and
- the global Krenn--Gu conjecture.

## Replay record

Before publication, run:

```powershell
python claims/arbitrary-order/verify_projectively_constant_lift_same_type_two_defect_five_cell_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_same_type_two_defect_five_cell_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_same_type_two_defect_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_same_type_two_defect_five_cell_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_same_type_two_defect_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_same_type_two_defect_five_cell_detector.py
```
