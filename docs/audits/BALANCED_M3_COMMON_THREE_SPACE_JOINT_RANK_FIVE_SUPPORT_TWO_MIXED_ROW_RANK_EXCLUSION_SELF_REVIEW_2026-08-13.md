# Hostile self-review: rank-five support-two mixed-row-rank exclusion

## Verdict

**PASS at the stated local scope.**  The package excludes the complete
transverse joint-rank-five support-two `(3,2)` and `(2,3)` involved-row
profiles.  It does not exclude `(3,3)`, support one, a Hilbert--Burch
boundary, joint rank at most four, another physical component, or any higher
order.  Global Krenn--Gu remains **UNRESOLVED**.

Reviewed artifacts:

- the owning theorem;
- its SymPy verifier;
- its independent standard-library `Fraction` audit;
- the S2AG support-two localization;
- the S2AH target-kernel argument; and
- the S2AI complete `(2,2)` exclusion and its coefficient conventions.

## Adversarial claim inventory

1. A `(3,2)` relation plane is the graph of a rank-two map `L`.
2. The rank-two involved-row kernel is a single target coordinate, so
   `image L` is a coordinate two-plane.
3. The support-two contracted colour-one target forces `L e_1` to have
   nonzero colour-zero and colour-one coordinates.  Hence the missed colour
   is exactly two.
4. The zero physical row `p_2=0` makes all `b=2` all-cross coefficients
   vanish and pins the three singleton coefficient tensors to
   `S_0=S_1=0`, `S_2=-kappa^(-1)T_2`.
5. Thus every remaining singleton correction lies on `T_2`, without any
   condition beyond the inherited support contractions on the remaining
   entries of `B`, `C`, or `L`.
6. The support-two relation makes `q_0,q_1` nonzero scalar multiples.
7. At the fixed row pair `(1,1)`, the colour-zero slice lies on `T_2` while
   the colour-one slice has a nonzero `T_1` component.  Linearity contradicts
   independence of `T_1,T_2`.
8. Exchanging the involved roots covers `(2,3)`.
9. An exact local correction-table control explains why the same comparison
   does not decide `(3,3)`.

## Hostile questions

### Does row rank really determine the graph projections?

Yes.  The transposed row map restricted to `A_i^*` has kernel equal to the
annihilator of `pr_i P`; hence its rank is `dim pr_i P`.  Rank three of
`rho` makes `P -> A_1` an isomorphism because both spaces have dimension
three.  Rank two of `pi` then makes the graph map `L:A_1->A_2` have rank
two.  No generic point or basis specialization is used.

### Is the coordinate kernel imported from a theorem that assumed `(2,2)`?

No.  The package repeats the one-shore argument.  If `delta` spans
`ker pi`, contraction in root two kills the all-cross permanent and sends
the singleton image into

```text
A_1 tensor span((delta tensor id)(B)).
```

Every colour supported by `delta` has an independent nonzero diagonal target
coefficient.  The same fixed second-factor line cannot equal two distinct
coordinate lines, and a zero contraction cannot absorb even one.  Therefore
`delta` has coordinate support one.  This argument does not use the rank of
`rho`.

### Could cancellation in the support contraction make one coefficient in equation (10) zero?

No.  Write `b_eta=beta e_0` and `c_eta=chi e_1`, where S2AG gives
`beta chi!=0`.  A preimage of the nonzero colour-one diagonal target must be
`t e_1` with `t!=0`; otherwise its projection modulo `e_1` leaves a nonzero
first factor.  The equality becomes

```text
beta e_0+chi L e_1=nu e_1
```

with `nu!=0`.  Hence the `e_0` and `e_1` coefficients of `L e_1` are both
nonzero.  A coordinate image plane containing that vector can miss only
colour two.

### Was the entire graph map accidentally normalized?

No.  Only its forced column `L e_1` is displayed.  In the target-table replay,
the verifier keeps four independent symbols in the other two columns,
subject only to the already proved zero third row.  That replay even keeps
the root block `C` at nine independent symbols and the first two rows of `B`
at six independent symbols, because the final zero-row inference does not
need their inherited support contractions.

### Does the zero-row comparison really use the same coefficient tensors?

Yes.  The graph vectors

```text
u_i=e_i tensor B+C tensor L e_i
```

form a basis of `U`.  Their coefficient tensors `S_i` in the full target
equation are global, not selected separately by root row.  At `b=2`, the
`C tensor L e_i` term vanishes because every `L e_i` lies in
`span(e_0,e_1)`, and the forced row of `B` is `kappa e_2`.  The three rows
`(0,2,2)`, `(1,2,2)`, `(2,2,2)` therefore give exactly
`S_0=0`, `S_1=0`, `S_2=-kappa^(-1)T_2`.

### Could another singleton basis vector contribute a hidden `T_1` correction at `(1,1,c)`?

No.  Its coefficient tensor is already zero.  The only surviving term is a
scalar entry of `u_2` multiplying `S_2`, so its image is contained in
`span(T_2)` regardless of `C` and `L e_2`.  This is the load-bearing gain
from the rank-two shore.

### Are `q_0` and `q_1` genuinely proportional rather than merely dependent modulo something?

They are genuinely equal up to a nonzero scalar in `W^*`:
`theta(eta)=eta_0q_0+eta_1q_1=0`, and both coefficients are nonzero because
the support of `eta` is exactly `{0,1}`.  If either row vanished, the other
would vanish too and `ker theta` would have dimension at least two,
contradicting `rank theta=2`.

### Does the final comparison have the correct target signs?

Yes.  The convention is `G_N-J=sum_i S_i u_i`, so the all-cross row equals
the target row plus the singleton correction.  At `(1,1,0)` there is no
target and the row lies on `T_2`; at `(1,1,1)` the target is `+T_1` and the
correction still lies on `T_2`.  Reversing the global sign convention would
change only the correction scalars, not the surviving nonzero `T_1`
component.  Both computational routes reconstruct the physical root index
as `9a+3b+c`.

### Is root exchange legitimate for `(2,3)`?

Yes.  Exchanging roots one and two swaps `rho,pi`, swaps `B_23,C_13`, and
preserves every diagonal target tensor.  The support-two conclusion is
symmetric; the two supported coordinate lines may then be renamed zero and
one in their exchanged order.

### Why does this not close `(3,3)`?

For `(3,3)`, the graph map is invertible and there is no zero root row.  The
three coefficient tensors in `G_N-J=sum_i S_i u_i` are not forced onto one
target line.  In particular a `T_1` correction can absorb the difference
between the proportional third-root slices.  Equation (24) is an exact
local table showing that the final two-slice inference fails; it is
explicitly not claimed to be a physical witness.

### Is the independent audit genuinely independent?

Yes.  The primary verifier uses SymPy symbolic matrices and a physical
`A_1,A_2,A_3` placement function.  The audit imports no repository code and
no third-party package.  It uses flat tuples of standard-library `Fraction`
values, constructs each root coefficient directly at `9a+3b+c`, and checks
the graph contraction, zero row, target-line independence, and stop control
through separate functions.

### Did review expose an implementation mistake?

Yes, and it was corrected before packaging.  The first primary replay
declared the provisional off-diagonal row symbols `B_(2,0),B_(2,1)` as
nonzero and then asked SymPy to solve the target equations forcing them to
zero.  The solver correctly rejected the inconsistent assumptions.  Those
two symbols are now unrestricted; only `kappa=B_(2,2)` is declared nonzero.
The fresh symbolic replay and the independently indexed `Fraction` audit
both pass.

## Stop boundary

The proved conjunction is

```text
normalized target-consistent physical m=3 common-three-space point
+ transverse two-root derivative of rank six
+ total joint row rank five
+ third-row rank two with support-two kernel
+ involved row ranks (3,2) or (2,3).
```

No beta-zero, monomial, tangent, separability, or full-singleton-determinant
assumption is added.  Removing the rank-two involved shore removes the zero
row that pins every correction to `T_2`.  The `(3,3)` profile, support one,
the Hilbert--Burch atlases, and the lower-rank/global branches are not decided
here.  Global status must remain **UNRESOLVED**.
