# A quantitative lower bound on nonroot tangent companion endpoints

## Status

**Exact arbitrary-order characteristic-zero theorem.**  Let a hypothetical
three-colour GHZ graph witness have `r>=2` fully supported roots.  Suppose
the root--blocker rows vary projectively to first order, and restrict at each
root `i` to the scalar tangent kernel

```text
S_i=ker(a_i),             a_i(1,1,1) != 0.         (1)
```

Assume no root--root edge is effective on the restricted jets.  If the only
remaining effective tangent companions are `t` fixed nonroot endpoints,
then

```text
t >= ceiling(2r/3).                                (2)
```

More precisely, when `t<r`, each of the three coordinate covectors occurs
among the projective `a_i` with multiplicity at least `r-t`, and the number
of non-coordinate covectors is at most

```text
3t-2r.                                             (3)
```

For `t=2`, this says `r<=3`; at `r=3` the covectors must be exactly the three
coordinate axes.  Thus the earlier two-residual-only obstruction for
`r>=4` is the first sharp instance of (2).

The theorem is a topology/counting obstruction.  It does not apply after an
effective root--root restricted tangent channel appears, and it does not
exclude systems meeting (2).  It supplies no proof that the required
nonroot endpoints or axis multiplicities are globally realizable.  The
arbitrary-order local-to-global reduction and the global Krenn--Gu
conjecture remain **UNRESOLVED**.  No finite field is used.

## Why a high mixed derivative vanishes on the graph side

For `y_i in S_i`, every differentiated root--blocker edge vanishes by
projective constancy.  By hypothesis, every restricted one- or two-tangent
root--root edge vanishes as well.  Therefore a varied root can survive in a
matching only by pairing to one of the `t` effective nonroot companion
endpoints.

Take any set `I` of `t+1` roots.  A perfect matching would have to inject
those `t+1` roots into `t` endpoints, which is impossible.  Hence the full
graph mixed derivative on

```text
tensor_(i in I) S_i
```

is identically zero.  Equality with GHZ forces the coordinatewise-product
map

```text
mu_I: tensor_(i in I) S_i -> K^3,
mu_I((y_i))=(product_i y_i[0],
             product_i y_i[1],
             product_i y_i[2])                    (4)
```

to vanish identically too.  Here the unquotiented map is appropriate because
the graph derivative itself is zero.

## Exact zero-product classification

For a fixed coordinate `c`, the `c`th component of (4) is the tensor product
of the restricted coordinate functionals

```text
(e_c^*|S_i)_(i in I).                              (5)
```

A tensor product of linear functionals over a field is zero exactly when at
least one factor is zero.  Now

```text
e_c^*|S_i=0
iff S_i is contained in ker(e_c^*)
iff S_i=ker(e_c^*)
iff a_i is projectively e_c^*.                     (6)
```

The middle equivalence uses that both spaces are hyperplanes.  Consequently
`mu_I=0` if and only if `I` contains at least one root of each of the three
coordinate-axis types.

Since every `(t+1)`-subset has zero graph derivative, every such subset must
contain all three axis types.

## Counting the axes

Let `n_c` be the number of roots with `a_i` projectively equal to `e_c^*`.
If `r-n_c>=t+1`, one could choose `t+1` roots avoiding axis type `c`, contrary
to the preceding classification.  Thus

```text
n_c >= r-t                 for c=0,1,2.            (7)
```

The axis types are disjoint, so

```text
r >= n_0+n_1+n_2 >= 3(r-t).                       (8)
```

Equation (8) is `3t>=2r`, proving (2).  If `m` roots have non-coordinate
covectors, then

```text
m=r-(n_0+n_1+n_2) <= 3t-2r,                       (9)
```

which proves (3).  When `t>=r`, inequality (2) is automatic and there is no
`(t+1)`-root derivative to use; the sharper multiplicity assertion is only
claimed for `t<r`.

## Consequence for the current local-to-global frontier

In the two-residual surplus-two cell, a repair that keeps root--blocker
variation projectively constant and suppresses all root--root tangent
channels cannot use the two residual vertices alone once `r>=4`.  More
generally, a no-root--root repair needs a number of effective nonroot
endpoints growing linearly with the number of roots.  A bounded companion
set cannot support arbitrary root order.

This narrows the genuine escapes to nonprojective blocker variation,
root--root tangent propagation, or an unbounded supply of nonroot companion
endpoints with the axis-population constraint (7).

## Replay

Replay the two-endpoint instance first:

```powershell
uv run --with sympy python verify_root_two_residual_only_companion_third_jet_obstruction.py
python audit_root_two_residual_only_companion_third_jet_obstruction.py
```

Then run:

```powershell
uv run --with sympy python verify_root_finite_nonroot_companion_endpoint_count_obstruction.py
python audit_root_finite_nonroot_companion_endpoint_count_obstruction.py
uv run --with sympy --with ruff python -m ruff check verify_root_finite_nonroot_companion_endpoint_count_obstruction.py audit_root_finite_nonroot_companion_endpoint_count_obstruction.py
python -m py_compile verify_root_finite_nonroot_companion_endpoint_count_obstruction.py audit_root_finite_nonroot_companion_endpoint_count_obstruction.py
```

The primary checks (6) with exact symbolic kernel bases and audits the
integer counting ledger through 30 roots.  The no-import audit independently
checks the tensor-product zero criterion on rational projective covectors
and the extremal axis counts through 60 roots.  These bounded checks audit
the all-order proof above; they are not theorem evidence by themselves.
