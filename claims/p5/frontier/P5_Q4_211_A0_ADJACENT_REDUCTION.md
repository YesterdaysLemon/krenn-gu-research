# Adjacent reduction on the `a=0` boundary of normalized `q4_211`

## Status

This note gives an exact reduction of adjacent incidence on

```text
a=0,   b c != 0.                                    (1)
```

The doubled-colour contraction becomes a third embedded `P_4`, with
normal

```text
h_0=e_1-e_2.
```

The adjacent two-cross branch remains excluded.  In the one-cross
branch, write `A` for the original `h_1,h_2` common mode, `Y` for the
mandatory opposite-pencil mode, and `C,D` for the other two modes.
Then necessarily

```text
h_0 in R_C intersect R_D,                           (2)
```

and, in the `q` orientation,

```text
u_1 in R_C union R_D.                               (3)
```

In the colour-swapped `p` orientation, (3) is
`u_2 in R_C union R_D`.

This is a strict boundary reduction, not an exclusion of (2)--(3), all
adjacent incidence, normalized `q4_211`, `P_5 -> Delta_3`, or the
global Krenn--Gu conjecture.

## The third embedded `P_4`

At `a=0`,

```text
u_0=e_1+e_2
```

and

```text
u_0 contract P_5
 =P_4(e_0,e_1+e_2,e_3,e_4).                        (4)
```

Its supporting hyperplane has normal

```text
h_0=e_1-e_2.                                       (5)
```

The decomposable-`P_4` rank-drop theorem therefore puts `h_0` in at
least two of the four remaining row spaces.

The adjacent two-cross analysis uses only `bc!=0`, so its marked
`P_4 -> Delta_2` obstruction applies unchanged.  It remains to treat
the one-cross branch.

## The third normal avoids the two pencil modes

Stay in the `q` orientation.  The common mode `A` contains
`h_1,h_2`.  If it also contained `h_0`, then the three independent rows

```text
h_0,h_1,h_2
```

would all annihilate `s=e_1+e_2`.  Since the ambient row space has
dimension three,

```text
L_A(s)=0.
```

This is the common-kernel gate, which is excluded by the
common-kernel obstruction; that gate lemma requires only `bc!=0` and
therefore applies on (1).

The opposite-pencil mode `Y` contains

```text
span(h_1,n),
n=(0,0,0,c,b).
```

If `h_0` also lay in `R_Y`, the same three-dimensional argument with
the independent rows `h_0,h_1,n` would give

```text
L_Y(s)=0,
```

the other excluded common-kernel gate.

Thus `h_0` occurs at neither `A` nor `Y`.  It must occur at least twice,
and only `C,D` remain.  This proves (2).

## One of the two modes carries the rigid direction

The one-cross normal-pencil theorem applies on `bc!=0`.  Away from the
already excluded common-kernel gate, it has only two relevant
outcomes in the `q` orientation:

1. a mode contains the double-normal plane `span(h_2,n)`; or
2. the three normal-pencil lines at the remaining modes are

   ```text
   C h_2, C n, C u_1.
   ```

The double-normal mode cannot be `A` or `Y`, because either placement
would contain `h_1,h_2,n`, a boundary already excluded by the
two-cross theorem.  It is therefore one of `C,D`.  The identity

```text
c u_1=b h_2+n                                      (6)
```

puts `u_1` in that row space.

In the rigid three-line outcome, `C` and `Y` already carry the
selected `h_2` and `n` lines.  The third line `u_1` is carried by the
remaining member of `{C,D}`.  Thus (3) holds in either outcome.

The `p` orientation follows by interchanging singleton colours and
using

```text
b u_2=c h_1+n.
```

## Consequence

The `a=0` adjacent frontier is no longer a free third-normal edge.
Both non-pencil modes contain the third normal `h_0`, and one also
contains a fixed direction row.  Equivalently, the remaining problem
is a marked simultaneous compression of the third embedded `P_4`,
not an ambient support search.

## Verification

Run:

```text
python verify_p5_q4_211_a0_adjacent.py
python audit_p5_q4_211_a0_adjacent.py
```

The primary verifier checks (4)--(6), the row independence, and the
kernel implications.  The independent audit checks the same
incidence forcing over `F_5,F_7`.  It enumerates no ambient maps or
Grassmannians.  The finite-field calculations audit the formulas; the
proof above is over `C`.
