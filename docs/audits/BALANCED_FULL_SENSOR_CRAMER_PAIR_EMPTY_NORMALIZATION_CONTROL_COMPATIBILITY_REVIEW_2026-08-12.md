# Review of the balanced full-row Cramer target-consistency and normalization compatibility boundary

## Verdict

**PASS at the frozen three-file core, with no P0--P3 finding.**

Reviewed commit:

```text
8ec176b56dccc1fedf190644abfa84393e2b6d5d
```

Reviewed normalized Git-blob SHA-256 values:

```text
theorem:  a50efa8fd128462b24a9e8b8ddc802eb5cde192d434a69cbc5d376f6fa235997
primary:  59d5596f43b4e4472910469e2c2ef1e8cd8127588ac9109987e0a0dcc288f18f
audit:    344f8a90dcfe3b41c642c6037e659e611ea4aebd44f4b788edf52805380c99c5
```

These are raw normalized Git-object byte hashes.  Repository publication must
also pin the theorem through the canonical ledger hash and exact commit
object.

The result is a proved compatibility boundary at `m=3`.  It is not an actual
balanced-sensor realization and does not exclude or construct a Krenn--Gu
witness.  The global conjecture remains **UNRESOLVED**.

## 1. Exact claim reviewed

For the complete ternary root-word row set

```text
{0,1,2}^3
```

and the four even-deck columns ordered as

```text
(xy,xr,yr,empty),
```

the theorem constructs eight separate exact `27 x 4` polynomial matrices.
In every construction:

1. the four columns have the exact deck-complement multidegrees;
2. the rational candidate components have their own correct deck-label
   multidegrees;
3. the full equation `Gamma f=J` holds in every one of the `27` rows for the
   exact contracted GHZ target;
4. `f_empty=1` and, on the displayed Cramer minor,
   `v_empty=beta`;
5. the selected minor has nonzero determinant, hence the full matrix has
   function-field column rank four; and
6. exactly one of the eight retained S2L coordinates for `f_xy` is nonzero.

The controls cover the two nonpivot outside first derivatives and all three
nonpivot symmetric Hessian coordinates at each endpoint.  Therefore full-row
target consistency and empty normalization do not, even together with rank
and the multidegrees, make any one retained coordinate follow from the other
seven at this ambient full-row level.

The old S2L selected-row matrices are not claimed to admit literal row
extensions.  Their unique solutions have the wrong empty component.  The
new theorem changes the matrices and uses auxiliary pair coordinates to
build normalized replacements with the same eight sharpness patterns.

## 2. Manual algebra audit

### 2.1 Target and column conventions

The reviewer checked that the only nonzero target rows are

```text
J_(c,c,c)=x_c y_c r_c,       c=0,1,2,
```

and that every remaining root word has target zero.  The standard column
order is used consistently.  Every nonzero entry in the `xy`, `xr`, `yr`,
and `empty` columns has multidegree respectively

```text
(0,0,1), (0,1,0), (1,0,0), (1,1,1).
```

Every nonzero rational component has degree respectively

```text
(1,1,0), (1,0,1), (0,1,1), (0,0,0).
```

These checks include denominator contributions.

### 2.2 Outside controls

For each `a in {1,2}`, the candidate is

```text
f_xy=(r_a/r_0)x_a y_a,
f_xr=f_yr=0,
f_empty=1.
```

The four displayed selected rows give

```text
beta=r_0 r_a x_0 x_a y_0 y_a,
```

and the complete matrix equation holds row by row.  The only nonzero
retained coordinate is

```text
partial_(r,a) f_xy=x_a y_a/r_0.
```

The two signs and both selected minors were replayed exactly.

### 2.3 Endpoint controls

For `1<=a<=b<=2`, the `x` construction uses

```text
f_xy=(x_a x_b/x_0)y_a,
f_yr=(x_a/x_0)y_a r_a,
f_xr=0,
f_empty=1,
```

and has

```text
beta= r_0 r_a x_0^2 y_0^2.
```

The `y` construction is the exchanged formula

```text
f_xy=x_a(y_a y_b/y_0),
f_xr=x_a(y_a/y_0)r_a,
f_yr=0,
f_empty=1,
```

with

```text
beta=-r_0 r_a x_0^2 y_0^2.
```

The positive `x` and negative `y` determinant signs were checked directly.
The diagonal Hessian cases have the required coefficient `2`; the mixed
cases have coefficient `1`.  The quotient-cleared Hessian residual retains
both middle terms when the two derivations agree.

### 2.4 All retained replacement minors

The primary verifier and independent audit do not merely inspect the eight
advertised nonzero derivatives.  For each of the eight controls they rebuild
all eight retained selected-column replacement determinants.  Thus each
implementation evaluates exactly

```text
8 controls x 8 retained coordinates = 64
```

replacement minors, proves seven are zero, and proves the designated one is
the correct nonzero `beta^2` first stress or `beta^3` Hessian stress.

## 3. Independence and execution evidence

The primary verifier uses SymPy matrices, adjugates, determinants,
differentiation, rational simplification, and polynomial multidegrees.  It
constructs all `27` rows rather than checking only the displayed selected
minor.

The independent audit imports neither SymPy nor repository code.  It defines
a separate sparse Laurent-polynomial ring over `Q`, direct exponent
differentiation, Leibniz determinants, and explicit matrix-vector products.
It reconstructs the eight systems from its own data and independently checks
all `27` target rows and all `64` replacement determinants.

At the reviewed commit both exact replays passed, Ruff `0.16.2` passed, the
files compiled, and the worktree remained clean during the read-only hostile
review.  The local repository floor also passed with:

```text
1825 Python files compiled;
973 Markdown files with all local links resolving;
137/137 existing ledger hashes valid;
191 migration-tool tests;
14 cycle-cover lattice tests.
```

These counts describe the frozen unique-file core before this review and
before its eventual navigation/ledger integration.  Publication must rerun
the candidate-tree floor at the final exact head.

## 4. Scope firewall

The phrase **degree-compatible full-row Cramer system** is load-bearing.  The
constructed matrices have the correct bundle degrees, row index set, GHZ
target, full target equation, normalization, and rank.  They are not shown
to be companion columns

```text
G_(N-I)
```

obtained simultaneously from one common collection of root--root and
root--nonroot physical shore blocks by the balanced matching-sum formula.
That nonlinear common-shore image may impose further relations not visible
from degrees and the full linear equation.

Accordingly the review rejects all of the following stronger readings:

```text
one control is an actual balanced target incidence;             NOT PROVED;
one control is a physical graph or tensor equality;              NOT PROVED;
the displayed matrices are unrealizable by a common shore;       NOT PROVED;
the auxiliary pair components pass their pair-pole gates;        NOT PROVED;
all pairs pass simultaneously;                                   NOT PROVED;
the construction extends from m=3 to arbitrary m;                NOT PROVED;
normalization plus target consistency settle S2;                  FALSE;
the controls are Krenn--Gu counterexamples;                       FALSE / NOT CLAIMED.
```

At `m=3` there is no higher even-subset Euler--hafnian recurrence, but this
does not remove the common-shore realization or physical pair-regularity
obligations.  The nearest live bridge is therefore exactly the pullback from
these full-row controls to the common-shore companion matching-sum image, or
an exact theorem proving that pullback impossible.

## 5. Final assessment

The theorem correctly closes the narrow feasibility question that motivated
S2M: empty normalization and every unselected/full target row can coexist
with the failure of any chosen retained pair coordinate at the ambient
degree-compatible full-row level.  It also makes the remaining missing layer
more precise.

No mathematical or evidence defect was found at the pinned core.  Promotion
is appropriate after rebasing onto the latest verified main, integrating the
maintained frontier and ledger without collision, rerunning the complete
candidate-tree floor, and completing exact-head and merged-main publication
verification.  Global Krenn--Gu remains **UNRESOLVED**.
