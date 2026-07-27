# Five-row projective incidence lemma

## Status

This is an exact local consequence over `C` of the support-at-most-three
`P_5` contraction obstruction.  It proves that every local map in a
hypothetical restriction

```text
P_5 -> Delta_3
```

must contain a nonzero row supported on a single target coordinate.  It
does not by itself exclude all five-map configurations.

## Projective lemma

Let

```text
r_0,...,r_4 in C^3
```

span `C^3`.  Suppose that for every distinct `p,q`,

```text
span(r_p,r_q) contains one of e_0,e_1,e_2.              (1)
```

**Theorem.**  At least one `r_p` is proportional to a coordinate vector.

If some `r_p=0`, then (1) says that every nonzero row paired with it is
itself a coordinate vector, and the conclusion is immediate.  Assume
therefore that all rows are nonzero and, for a contradiction, none is a
coordinate vector.

Write `P_p=[r_p]` and `E_c=[e_c]` in the projective plane.  The `P_p`
are distinct: two equal non-coordinate projective points would span no
`E_c`.

No three `P_p` are collinear.  Otherwise their common line `L` contains
an `E_c` by (1).  Because the five points span the plane, choose another
point `Q` off `L`.  The three lines from `Q` to the three points on `L`
must each pass through one of `E_0,E_1,E_2`.  The same `E_c` cannot be
used twice, since the corresponding two lines through `Q,E_c` would be
equal.  But every `E_c` already on `L` is unusable: the line from `Q` to
that `E_c` meets `L` at `E_c`, not at one of the non-coordinate `P_p`.
There are therefore fewer than three available coordinate points, a
contradiction.

Now take any triangle on three of the `P_p`.  Each side contains at
least one `E_c`.  The same `E_c` cannot lie on two sides, because their
intersection is one of the non-coordinate triangle vertices.  Hence
the three sides contain the three different coordinate points.

Colour every edge `P_p P_q` by the coordinate point on it.  Every
triangle is rainbow.  At a fixed vertex, the four incident edges must
then have pairwise different colours: any two occur together in a
triangle.  This is impossible with only three colours.  The
contradiction proves the theorem.

## Consequence for `P_5`

Suppose maps

```text
phi_i : C^3 -> C^5,   i=0,...,4,
```

pulled `P_5` back to `Delta_3`.  They are injective by conciseness.
For one mode `i`, let

```text
r_(i,s) = x_s composed with phi_i in (C^3)^*,
          s=0,...,4,                                  (2)
```

be its five source-coordinate rows.  They span `(C^3)^*`.

Fix source coordinates `p,q` and put

```text
K_pq = ker(r_(i,p)) intersect ker(r_(i,q)).
```

This space is nonzero.  Every `t in K_pq` maps to a source vector with
at most three nonzero coordinates.  If `t` had all three target
coordinates nonzero, contracting the claimed restriction in mode `i`
would give a restriction from a support-at-most-three contraction of
`P_5` to a concise `Delta_3`.  The support-at-most-three contraction
theorem excludes this.

Thus every vector in `K_pq` has a zero target coordinate.  Over the
infinite field `C`, the linear space `K_pq` must lie in one target
coordinate hyperplane.  By annihilator duality,

```text
span(r_(i,p),r_(i,q)) contains some e_c^*.             (3)
```

The projective theorem applies to the five rows in (2).  Therefore every
one of the five local maps contains a nonzero singleton row:

```text
for some source coordinate s and target colour c,
r_(i,s) is proportional to e_c^*.                      (4)
```

## Verification

Run:

```text
python verify_five_row_projective_incidence.py
python audit_five_row_projective_incidence.py
```

The primary verifier exhausts all `3^10=59,049` edge-colour assignments
on `K_5` and confirms that none makes every triangle rainbow.  It also
checks the local annihilator dimensions behind (3).  The independent
audit enumerates all five-point multisets in `PG(2,F_5)` (with an
optional zero row), retains every spanning configuration satisfying
(1), and confirms that each retained configuration contains a
coordinate point.

## Boundary

The singleton row in (4) is not necessarily isolated in its source
coordinate or target colour, and singleton rows chosen in different
modes need not use different source coordinates.  There are 68 orbits
of five singleton placements under source, mode, and target-colour
symmetry.  The later
[`FIVE_ROW_PROJECTIVE_NORMAL_FORMS.md`](FIVE_ROW_PROJECTIVE_NORMAL_FORMS.md)
refines each local map into three geometric strata; the exact permanent
cancellation equations across the five modes remain.
