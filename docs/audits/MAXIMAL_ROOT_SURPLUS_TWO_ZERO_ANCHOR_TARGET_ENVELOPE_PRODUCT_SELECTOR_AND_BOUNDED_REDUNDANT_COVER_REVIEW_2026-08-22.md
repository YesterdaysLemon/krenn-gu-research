# Hostile review: zero-anchor target envelope and bounded redundant cover

## Decision

**Accept as scoped theorem `GLS28` after revision.**  The exact `GLS23`
label decomposition and `GLS26` residual-shore tangent imply the claimed
foreign-supplier envelope for every promoted pair target on the zero-anchor
branch.  Root separation gives a legal full `GLS8` selector, while separation
of a projected pure diagonal gives the stronger named nonzero-response row
through the complete `GLS22` target coupling.

The first draft incorrectly blurred useful-row failure with full desired-
tensor absorption.  The accepted theorem keeps them separate.  Useful-row
failure yields only a deletion-stable cover of the reconstructed diagonal
space.  Relations for every supplier direction require the additional full-
absorption hypothesis.  The global conjecture remains **UNRESOLVED**.

## 1. Type and label audit

For a promoted pair target `D`, the ambient transverse coefficient space is

```text
E_A^tr tensor V_D^*.
```

The theorem defines

```text
Tbar=P_Q(T_Q),
W_D=Slice_D(t_D),
A_D=Tbar+sum_(E!=D) W_E.
```

Every summand of `A_D` is a root-coefficient subspace of `E_A^tr`; tensoring
with `V_D^*` therefore has the correct receiving-target type.  The proof does
not confuse a source label's port factors with the receiving target factors.

The `GLS23` nuisance terms check as follows.

- The top term is `K(p omega) tensor V_D^*` and vanishes because `omega=0`.
- The label `Q` is killed by `P_Q(q)=0`.
- A one-`Q` label has all root coefficients in `P_Q(T_Q)` by `GLS26`, whether
  its promoted port is retained in `D` or sliced outside it.
- A foreign promoted pair contributes a partial slice and target padding of
  its tensor `t_E`.  Every resulting root coefficient lies in the full left
  support `Slice_E(t_E)=W_E`.
- The desired label `E=D` is correctly omitted from nuisance.

Thus

```text
N_D^tr subset A_D tensor V_D^*
```

is exact.  It is an upper bound, not an equality.

## 2. Selector and response audit

If `W_D` is not contained in `A_D`, one contraction of `t_D` lies outside the
envelope.  A root functional separating that contraction from `A_D`, tensored
with the same port contraction, annihilates the complete nuisance and detects
`t_D`.  `GLS22` then lifts the transverse functional to a legal constant full
`GLS8` selector.  This conclusion does not imply a nonzero response.

For the stronger criterion, if `Delta_Q` is not contained in `A_D`, at least
one displayed generator `delta_c=P_Q(r_c)` lies outside.  Tensor the separating
root functional with the coordinate functional extracting the pure target
word `v_(D,c)`.  The transverse pure class is nonzero.  Theorem 3 of `GLS22`
then gives all three linked conclusions:

```text
[t_D]!=0,
P_(S_D)(H;z_Q)!=0,
a legal full selector with that named response.
```

No response coordinate or nuisance minor is inverted.  The selector is
normalized only after a pointwise nonzero value has been proved.

## 3. Failure-cover and relation-bound audit

Let

```text
H=E_A^tr/P_Q(T_Q),
L=(Delta_Q+P_Q(T_Q))/P_Q(T_Q).
```

The residual shore ranks give

```text
(d_0,d_1)=(1,1),(1,2),(2,1),(2,2),
dim H=4,2,2,1.
```

If every useful row fails, the contrapositive of the diagonal-coloop theorem
puts `L` in the span of all suppliers after deleting any fixed label.  Combine
all vectors from one supplier and prune to a linearly independent spanning
subfamily.  At most `dim H<=4` distinct labels remain.

This does **not** make every supplier redundant.  The retained exact quotient
control

```text
H=K^2,       L=K e_1,
W_1=W_2=K e_1,       W_3=K e_2
```

has deletion-stable diagonal coverage, but `W_3` is not in `W_1+W_2`.  It is
the correct abstract model of a surviving zero-response supplier.

Under the strictly stronger hypothesis `t_D in N_D^tr` for every `D`, the
target envelope forces every `W_D` into the other suppliers modulo the
tangent.  The same pruning argument gives a relation using the chosen label
and at most `dim H` other labels, hence at most five labels.  The accepted
statement records this extra hypothesis explicitly.

When both shore ranks are two, `dim H=1`.  On the essential branch `L=H`, so
deletion-stable useful failure needs at least two nonzero supplier labels.
Full absorption then gives two-label relations.  This is a scoped quotient
fact, not projective synchronization of a downstream physical operator
package.

## 4. Laurent-family and exceptional-fibre audit

Over the exact `GLS27` Laurent fraction field, either some fixed receiving
target has

```text
Delta_(Q,F) notsubset A_(D,F),
```

or all target containments hold.  For the first branch, let
`r_D=dim_F A_(D,F)` in a fixed finite generator matrix.  A nonzero augmented
`(r_D+1)`-minor witnesses escape.  Clearing it together with the source and
shore-rank factors produces a nonempty principal open where the same target
is useful.

In the second branch, choose a basis of `L_F` and rational supplier
certificates after each label deletion.  Combining equal labels and pruning
gives at most `dim H` labels per certificate.  Clearing the finitely many
coefficients, generator expressions, and basis minors makes those fixed
certificates specialize on one nonempty principal open.

This is a source-choice statement.  It does not extend the certificates over
every rank-drop or assignment-change divisor.  Exceptional fibres remain
pointwise in the exact `GLS22` Fitting criterion and GLS28 Theorems 1--5.

On the function-field `C12/C21/C22` branch, `L_F=0`; at a pointwise shore-cover
specialization, `L=0`.  The diagonal-coloop response criterion cannot fire
there.  A supplier-coloop legal selector, if present, has zero named response
by the complete target identity.  Mixed equations remain load-bearing.

## 5. Verification and independence

The primary verifier uses SymPy tensor coordinates.  It checks:

- all four residual-shore quotient dimensions;
- retained and sliced one-`Q` labels;
- overlapping and disjoint foreign promoted-pair labels;
- product separation and a nontrivial quotient target-coupling fixture;
- deletion covers, full-absorption relations, and the sharp zero-response
  countermodel; and
- an augmented Laurent rank minor.

The no-import audit uses standard-library `Fraction`, sparse coefficient
dictionaries, its own Gaussian elimination, a combinatorial
inclusion--exclusion derivation of tangent dimensions, a non-coordinate
alternating separator, rationally transformed circuit and countermodel data,
and a different Laurent specialization family.  It imports neither the
primary verifier nor repository mathematics code.

The finite checks audit the displayed linear-algebra mechanisms.  The
arbitrary-root label cover and principal-open specialization are the written
proof.  After revision, the focused verifier, independent audit,
`py_compile`, `ruff check`, and `ruff format --check` all pass.

Dependency replay of the GLS8, GLS22, GLS23, GLS26, and GLS27 primary and
independent audits also passes.

## 6. Exact accepted scope

```text
complete zero-anchor target-envelope inclusion:             ACCEPTED;
supplier coloop -> legal full GLS8 selector:                 ACCEPTED;
diagonal coloop -> named nonzero-response row:               ACCEPTED;
useful failure -> deletion-stable diagonal cover:            ACCEPTED;
full absorption -> at-most-five-label supplier relation:     ACCEPTED;
generic U/R source-choice refinement:                        ACCEPTED;

redundant cover excluded by mixed equations:                 OPEN;
C12/C21/C22 attached or excluded:                            OPEN;
all exceptional fibres closed:                               OPEN;
synchronization, activity, simultaneous downstream package:  OPEN;
arbitrary-r promoted detector entry:                         OPEN;
maximum-root supply/attachment strategic node:                OPEN;
global Krenn-Gu conjecture:                                  UNRESOLVED.
```
