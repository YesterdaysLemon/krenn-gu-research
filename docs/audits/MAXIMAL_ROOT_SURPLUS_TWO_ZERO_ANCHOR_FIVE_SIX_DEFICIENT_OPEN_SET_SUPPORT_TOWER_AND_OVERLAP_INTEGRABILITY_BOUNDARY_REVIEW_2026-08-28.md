# Hostile review: five-/six-deficient open-set tower and overlap-integrability boundary

## Review target and verdict

Target reviewed:

`claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FIVE_SIX_DEFICIENT_OPEN_SET_SUPPORT_TOWER_AND_OVERLAP_INTEGRABILITY_BOUNDARY_THEOREM.md`

Supporting artifacts reviewed:

`claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_five_six_deficient_minimal_open_set_and_overlap_integrability_boundary.py`

`claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_five_six_deficient_minimal_open_set_and_overlap_integrability_boundary.py`

**Verdict: PASS for the exact `GLS69` scope after independent hostile
reviews of the same-source tower and the three-open span, plus two finite
replays.**  The result proves an exact open-set support formula, commuting
same-source face maps, normalized necessary-profile censuses, and one
six-deficient three-open span exclusion.  It does not prove physical
realizability of a surviving profile, close either higher-deficient branch,
or establish source integrability.

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Same-source tower audit

For deficient set `N`, pure-axis set `P`, nonaxis set `U`, and colour `a`, put

```text
M_a={n in N:a in A_n},
D_a=N-M_a,
E_a={u in U:(k_u)_a=0},
L_a=D_a disjoint-union E_a.
```

For arbitrary `T subseteq N union U`, contract `N-T` at independent generic
kernel vectors, contract `U-T` at the actual nonaxis cross products, leave
`T union P` open, and quotient each pure-axis slot by its active line.  The
review checked that:

- a source pair survives structurally exactly when both endpoints lie in
  `T`;
- each surviving deck is an evaluation and quotient of the corresponding
  physical matching deck of the original graph;
- the formal colour-`a` coefficient is nonzero exactly when
  `D_a subseteq T` and `E_a subseteq T`, equivalently `L_a subseteq T`; and
- evaluating an open deficient slot at its generic kernel vector, or an open
  nonaxis slot at its cross product, gives the literal `T-{t}` face.

These evaluations commute because they act on distinct tensor factors.  A
three-open face evaluated at one kernel vector recovers only the opposite
two-open pair equation.  It does not produce a sum of three pair equations;
evaluating all three open slots gives only `0=0`.

The wording “formal colour-term support” is deliberate when a pure-axis
quotient factor remains: the nonzero displayed terms need not be asserted
independent across colours.  No deck is chosen independently and no
pointwise specialization is promoted to a function-field theorem.

## Five-deficient replay

Both implementations reproduce

| branch | raw | after `GLS63` | after `GLS67` | keys |
|---|---:|---:|---:|---:|
| `P=1,U=0` | 59,049 | 18,270 | 2,640 | 12 |
| `P=0,U=1` | 236,196 | 79,095 | 24,435 | 89 |

The minimum complete-open-set counts are `2,190 / 450` for sizes two/three
in the pure-axis branch and `17,475 / 6,960` in the nonaxis branch.  The
nonaxis replay also confirms that 270 profiles have some five-open colour;
150 of them, in two keys, have no size-two minimum.  The representative

```text
S_0,S_0,S_0,S_1,S_1,       E_0={u}
```

has deficient missing sizes `(2,3,5)` and complete open sizes `(3,3,5)`.
Thus a minimal-leaf theorem cannot silently discard the five-open parent.

## Six-deficient span correction

The `GLS63` and `GLS67` predicates first give

```text
531,441 -> 276,750 -> 99,855 profiles,
90 S_6 x S_3 type-profile keys.                      (1)
```

For an open triple `T={i,j,k}`, the actual same-source equation is

```text
g_ij tensor d_k^ij+g_ik tensor d_j^ik+g_jk tensor d_i^jk
 =sum_(a:D_a subseteq T) theta_(T,a)
   e_(i,a)^* tensor e_(j,a)^* tensor e_(k,a)^*.
```

At mode `i`, the first two source terms lie in `row J_i`; the third adds at
most the one row `d_i^jk`.  Hence the local source image is contained in
`row J_i+F d_i^jk`.  For type `R_c`, quotienting by
`row J_i=F e_(i,c)^*` has dimension at most one.  The target quotient has
dimension

```text
#{a:D_a subseteq T and a!=c},
```

because its complementary diagonal coordinate tensors are independent and
their coefficients are nonzero.  Therefore this number is at most one.
The proof is over the common characteristic-zero function field and neither
inverts a deck nor assumes that the one-slot decks are independent.

The original pair-only draft omitted this necessary condition.  Hostile
review found the omission, and both implementations now apply it to every
triple.  It removes exactly

| type-profile orbit, up to colour | profiles |
|---|---:|
| `S_0^2 R_0^4` | 45 |
| `S_0^2 R_0^3 T_0` | 180 |
| `S_0^2 R_0^2 T_0^2` | 270 |
| `S_0^2 R_0 T_0^3` | 180 |

and gives the corrected final stage

```text
99,855 -> 99,180 profiles,       90 -> 86 keys.      (2)
```

Only the `(2,2,4)` missing-size row changes, from `5,040 / 8` to
`4,365 / 4` profiles/keys.  The final minimum-size split is
`64,710 / 34,380 / 90` profiles in sizes two/three/four and
`48 / 37 / 1` keys.

Every three-open target has at most two colours.  In the post-span residual,
3,360 profiles have one binary triangle and 45 have four.  The latter form
the sole binary pair-class key `S_c^2 T_c^4`; the four triangles are the
same binary pair face with each outside label opened in turn.

## Boundary and failed routes retained

The review checked the exact outside-row identity.  With `|D_a|>=2`, a
triangle colour outside `row J_i` necessarily has `D_a=T-{i}` and therefore
already belongs to the opposite pair target.  Consequently the proposed
“no-target pair plus outside-row colour” route is vacuous; exact enumeration
finds no forced profile of that form.  The next useful obligation couples
nonzero pure or binary pair faces to their triangle and higher-open parents.

The displayed binary `P_3` control was also corrected during development.
Over `Q(omega)`, with `omega^2+omega+1=0`, the rows

```text
p=a+c,       q=a+omega c,       h=(a+omega^2 c)/6
```

give exactly `a tensor a tensor a+c tensor c tensor c`.  An earlier rational
formula did not.  The accepted formula is only a fixed-fibre row/deck
control: its `h` rows are not shown to be simultaneous evaluations of one
global physical deck, so it is neither a graph witness nor a counterexample.

The load-bearing successor is common-deck restriction separation.  On the
sharp `S_c^2 T_c^4` branch, one nonzero binary pair equation propagates to
four triangles; quotienting an outside `T_c` slot recovers the expected pair
face but leaves a row-space deck component uncontrolled.  Those components
must be coupled through the common four-, five-, and six-open physical
parents.  The 3,360 single-binary-triangle profiles and the five-deficient
large-face profiles remain separate residual families.

## Replay evidence

The following targeted commands pass in the isolated working tree:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_five_six_deficient_minimal_open_set_and_overlap_integrability_boundary.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_five_six_deficient_minimal_open_set_and_overlap_integrability_boundary.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_five_six_deficient_minimal_open_set_and_overlap_integrability_boundary.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_five_six_deficient_minimal_open_set_and_overlap_integrability_boundary.py
python -m ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_five_six_deficient_minimal_open_set_and_overlap_integrability_boundary.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_five_six_deficient_minimal_open_set_and_overlap_integrability_boundary.py
python -m ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_five_six_deficient_minimal_open_set_and_overlap_integrability_boundary.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_five_six_deficient_minimal_open_set_and_overlap_integrability_boundary.py
```

The primary uses explicit set-valued deficient types and exact
`Q(omega)` arithmetic.  The independent audit imports no project code, uses
integer masks, and replays the displayed binary identity in `F_7` only as an
audit of the characteristic-zero formula.  Both agree on all stage, key,
missing-size, minimum-leaf, five-open, removed-orbit, triangle-target, and
binary-multiplicity totals.

Final review status: **PASS for `GLS69`; 99,180 six-deficient profiles in 86
type-profile keys and both five-deficient branches remain open; shared-deck
integrability and the global Krenn--Gu conjecture remain UNRESOLVED.**
