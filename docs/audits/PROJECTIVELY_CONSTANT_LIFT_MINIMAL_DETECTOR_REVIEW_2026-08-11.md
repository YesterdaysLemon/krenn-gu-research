# Adversarial review of the lifted minimal-cell two-open detector

## Review status and provenance

This record reviews
[`PROJECTIVELY_CONSTANT_LIFT_ROW_QUOTAS_AND_MINIMAL_CELL_TWO_OPEN_DETECTOR_THEOREM.md`](../../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_ROW_QUOTAS_AND_MINIMAL_CELL_TWO_OPEN_DETECTOR_THEOREM.md)
as a conditional characteristic-zero theorem.

Codex performed a fresh line-by-line reconstruction after formulating the
candidate cross-depth lemma.  The standard-library audit was independently
implemented as a six-vertex graph-matching ledger and imports neither the
SymPy verifier nor repository code.  This is durable adversarial reasoning,
not an independent human review.  It records the failed strengthenings and
the exact acceptance boundary.

Review verdict: **accept the repeated-row quotas and the `q=0,r=3` detector at
their stated conditional scope** after the focused and repository-wide replay
gates pass.  Do not change the global Krenn--Gu status, which remains
**UNRESOLVED**.

## 1. Reconstructed obligation and assumptions

The upstream theorem proves, under aligned common-two-row and projective-shore
hypotheses, the complete restriction

```text
1/(q+1)! P_M(hat H,hat a^(q+1),hat b^(q+1))
 =weighted Delta_3,
M=r+2q+1.                                             (1)
```

The new claim does not re-extract or universalize those hypotheses.  It asks
two narrower questions inside their intersection:

1. what do the arbitrary-permanent Hall quotas say separately about the two
   repeated physical row families; and
2. in the first Hall-admissible cell `q=0,r=3`, can the two-open replacement
   tensor vanish?

The second question is load-bearing because the earlier exact star gauge
made automatic row-replacement transport false without the complete diagonal
identity.

## 2. Hall-transfer audit

For `q>=1`, select all `q+1` identical copies of `hat a` in the all-subset
Hall theorem.  Their local span is one line, so the theorem requires that line
to contain each target coordinate axis at `q+1` distinct modes.  The same
argument applies to `hat b`.  At `q=0`, the singleton tricolour theorem gives
the identical one-mode-per-colour statement.

Distinct coordinate axes cannot lie in one covector line.  Thus each family
uses at least `3(q+1)` distinct modes.  Because `hat b_j=0`, all of its modes
belong to `B`; because only one new mode `j` exists, at least one fewer of the
`hat a` modes belongs to `B`.  The exact consequences are

```text
p_b>=3q+3,
p_a>=3q+2.                                            (2)
```

No row-cell multiplicity is being mistaken for physical support here:
`p_a,p_b` count distinct outside modes with nonzero covectors.  The argument
uses repeated source rows only to invoke the quota.  At `r=q+3`, the `b`
quota fills all `|B|=3(q+1)` modes and therefore forces the stated coordinate
partition.

For `q=0`, (2) excludes the one-mode `a` star from an actual lifted diagonal
restriction.  The review preserves the earlier theorem's scope: its star is
still a correct tensor-preserving gauge and a sharp boundary for truncated
data; it simply does not satisfy the additional complete-GHZ premise (1).

## 3. Zero-collision classification

At `q=0,r=3`, the `b` row occupies exactly three outside modes.  Hall equality
therefore permits labels with

```text
b_(u_c)=beta_c e_c^*,       beta_c!=0.                (3)
```

For either choice of the second open root, the replacement tensor is the same

```text
A=P_3(a,a,b).                                         (4)
```

The factor-two expansion of (4) has three rank-one summands.  The review
checked two possible gaps in the written classification.

First, if one `a_u` vanishes, the remaining summand with the corresponding
nonzero `b_u` forces another `a` to vanish.  This leaves at most one nonzero
outside `a` mode, contradicting `p_a>=2`.

Second, with every `a_u` nonzero, flattening at mode `u` separates `a_u` from
`b_u`.  If they were independent, a functional killing the first and not the
second would leave a nonzero product of the other two `a` covectors.  Hence
`a_u` and `b_u` are proportional at all three modes.  There is no hidden
positivity assumption; the argument is linear algebra over any
characteristic-zero field.

## 4. Adjacent recolouring audit

Under the proportionality conclusion, evaluate (1) with all three outside
modes set to colour `c`.  The `b` row has exactly one available outside
column, `u_c`; the `a` row must use the new column `j`; and the two persistent
rows use the remaining columns.  The coefficient is

```text
eta_j(e_c) beta_c K_c=bar X_c!=0.                    (5)
```

Changing only mode `j` from `e_c` to `e_d`, `d!=c`, preserves the unique
row-type assignment and the nonzero factor `beta_c K_c`.  Its coefficient is

```text
eta_j(e_d) beta_c K_c.                                (6)
```

The target word is mixed, so (6) vanishes.  Taking `c=0,d=1` forces
`eta_j(e_1)=0`, while (5) for `c=1` forces it nonzero.  This contradiction
uses the full diagonal target, not merely Hall support or the existence of a
single companion frame.

The primary verifier reconstructs all nine `(c,d)` coefficient identities by
a labelled `4!` permanent.  The no-import audit instead evaluates the original
six-vertex graph through its 15 perfect matchings.  It also reconstructs the
complete two-open graph variation for all 81 integer input words before using
the direct three-case formula for `P_3(a,a,b)`.  Both routes confirm that no
assignment with a persistent row at `j` was missed: such an assignment would
leave the `b` row without any available column.

## 5. Detection versus injectivity

The upstream quotient-frame theorem gives exactly two independent companion
covectors at `j`.  For fixed open root `i`, only the coefficient belonging to
the third root `s` survives, so the variation is

```text
tau kappa_i tensor ell_(j,s) tensor A.                (7)
```

Every factor is nonzero.  Thus (7) detects every nonzero absorption direction.
The map from the two-dimensional effective plane to the single coefficient
line is nevertheless rank one.  The review rejected wording that called the
fixed-`i` map injective.  Stacking the two possible open roots is rank two,
but collective stacking is not needed for the individual nonzero-detector
claim.

## 6. Falsified strengthenings

Hall support by itself does not force (4) nonzero.  The exact row families

```text
a=(e_0^*,e_1^*,e_2^*),
b=(e_0^*,e_1^*,-2e_2^*)                              (8)
```

have full tricolour covers but give `P_3(a,a,b)=0`.  Both verifiers replay
this boundary.  The accepted proof therefore retains the adjacent
pure/mixed GHZ equations as an essential premise.

The result also does not prove:

- fixed-`i` injectivity;
- transport for `q=0,r>=4`;
- transport for `q>=1`;
- common-two-row alignment or projective constancy in every witness;
- an unfactorized detector;
- exclusion of the six-vertex witness cell; or
- the global conjecture.

## 7. Independence and evidence boundary

The primary verifier uses SymPy, a symbolic labelled permanent, and symbolic
coefficient tables.  The audit uses only the Python standard library, sparse
integer coordinate tensors, a first-vertex graph-matching recursion, and a
direct collision expansion.  It imports no project module and no computer
algebra.  The two implementations share the displayed mathematical model but
differ in derivation, representation, and arithmetic.

Neither bounded script proves the implication from a vanishing tensor to
local proportionality or the arbitrary-field recolouring contradiction.
Those are the written characteristic-zero proofs reviewed above.

## 8. Exact acceptance boundary

Accepted:

- the separate physical support quotas `p_a>=3q+2`, `p_b>=3q+3`;
- the coordinate partition for `b` at `r=q+3`;
- incompatibility of the one-mode tight star with the complete lifted GHZ
  identity;
- nonvanishing of `P_3(a,a,b)` at `q=0,r=3`; and
- nonzero two-open detection of each absorption direction in that cell.

Still open:

- every larger aligned projective cell;
- every unfactorized higher-surplus cell;
- arbitrary permanent nonrestriction; and
- global Krenn--Gu.

## Replay record

Before publication, run:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_row_quotas_and_minimal_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_row_quotas_and_minimal_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_row_quotas_and_minimal_detector.py claims/arbitrary-order/audit_projectively_constant_lift_row_quotas_and_minimal_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_row_quotas_and_minimal_detector.py claims/arbitrary-order/audit_projectively_constant_lift_row_quotas_and_minimal_detector.py
```
