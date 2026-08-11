# Adversarial review of the rank-one-mode five-cell detector

## Review status and provenance

This record reviews
[`PROJECTIVELY_CONSTANT_LIFT_RANK_ONE_MODE_AND_REGULAR_TWO_DEFECT_FIVE_CELL_DETECTOR_THEOREM.md`](../../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_RANK_ONE_MODE_AND_REGULAR_TWO_DEFECT_FIVE_CELL_DETECTOR_THEOREM.md)
as a conditional characteristic-zero theorem.

Codex reconstructed the local quotient argument, the balanced-companion
tensor line, the one-dependent-mode collision inverse, and the five-mode
defect transport independently of the primary script.  The standard-library
audit separately uses rational elimination, Bareiss determinants, and
polarized rank-one-subspace checks.  This is durable adversarial reasoning,
not an independent human review.

Review verdict: **accept complete two-open detection when the locally
dependent set has size one, or size two with at least one nonzero
proportional `a/b` pair**, after the focused and repository-wide replay gates
pass.  Two one-sided/zero defects and every three-or-more-defect pattern
remain open.  No witness is excluded, and global Krenn--Gu remains
**UNRESOLVED**.

## 1. Reconstructed obligation

The previously merged theorem closes the cell where every
`S_u=span(a_u,b_u)` has dimension two.  At a dependent mode, the quotient
`(K^3)^*/S_u` is larger, and the old common-kernel proof cannot simply be
reused.  The new proof instead needs two exact ingredients:

1. collective invisibility plus four nonzero retained collision tensors must
   make the four local root quotients span at most one line; and
2. a checkable deletion condition must guarantee those four retained tensors
   are nonzero.

The fixed layer then supplies the contradiction: one quotient line above a
local space of dimension at most one has total dimension at most two, but the
weighted ternary diagonal has local flattening rank three.

## 2. Companion-pattern quotient audit

At a dependent mode `u`, write

```text
v_p=pi_u(h_(p,u)),
r_p=P_4(h_p,a,a,b;B-{u}).                             (1)
```

The quotient of each pair tensor is exactly

```text
F_pq=v_p tensor r_q+v_q tensor r_p.                  (2)
```

Assume every `r_p` is nonzero and every collective coefficient vanishes.

- On a good companion frame, all six `F_pq` vanish.  Centering the equations
  at any root shows either every `v_p` is zero or every one is proportional
  to the center.
- At a zero companion `k`, the three tensors incident with `k` vanish.  The
  same centered argument gives a one-dimensional quotient span, including
  the two-zero-companion case.
- On a balanced partition `{p,q}|{s,t}`, the companion equations kill the two
  within-pair tensors and make the four cross tensors fixed nonzero scalar
  multiples of one tensor.  The two zero pairs give

  ```text
  v_q=lambda v_p, r_q=-lambda r_p,
  v_t=mu v_s,       r_t=-mu r_s.                     (3)
  ```

  If `v_p,v_s` were independent, then
  `A=v_p tensor r_s` and `E=v_s tensor r_p` would be independent, while two
  cross tensors would be `A+E` and `mu(-A+E)`.  No nonzero scalar can make
  those proportional in characteristic zero.  Hence the quotient span is
  again at most one.

The review checked the complement indexing between the symmetric matrix
`X` and the pair tensors `B_pq`: complements preserve the two balanced
blocks and permute their four cross edges.  Thus the cross-tensor-line claim
is applied to the correct pair labels.

## 3. Local flattening contradiction

The four root covectors at `u` lie in the inverse image of one quotient line,
and the fifth fixed-layer source row `b_u` lies in `S_u`.  Their local span
therefore has dimension at most

```text
dim S_u+1<=2.                                         (4)
```

The permanent restriction cannot have local flattening rank above that
source span.  The right side is
`sum_c X_c e_c^(tensor B)` with all `X_c` nonzero, so its local flattening
has rank three.  This contradiction uses no unproved root-transversality or
companion genericity.

## 4. One-dependent-mode collision audit

On four retained modes, suppose three `a_i,b_i` pairs are independent and
the fourth satisfies

```text
a_0=e_0^*,       b_0=lambda e_0^*,       lambda!=0.  (5)
```

The labelled expansion of `P_4(h,a,a,b)` first kills every component of `h`
outside the displayed local `a/b` directions.  Two-`b` coordinates on the
three transverse modes kill the three `b` coefficients.  If `x_0,x_1,x_2,x_3`
are the remaining `a` coefficients and `S=x_1+x_2+x_3`, the one-`b` and
pure-`a` coordinates give

```text
x_0+S-x_i=0,          lambda S=0.                    (6)
```

Hence `S=0`, every `x_i=x_0`, and `3x_0=0`; the collision map is injective.
The primary symbolic minor is `-24576 lambda^4`.  The audit chooses its rows
independently and reproduces the normalized determinant at three distinct
nonzero rational values.

The nonzero hypothesis in (5) is sharp for this operator.  The review
directly substituted the three preserved kernels:

```text
b_0=0:       h=(-2a_0,a_1,a_2,a_3);
a_0=0:       h=(0,-a_1,a_2,0);
a_0=b_0=0:   any h supported away from mode 0.        (7)
```

They are ambient collision kernels, not diagonal restrictions or graph
witnesses.  They prohibit extending the new collision lemma across the
one-sided/zero boundary without another argument.

## 5. Five-mode defect transport

Let `D={u:dim span(a_u,b_u)<=1}`.

- If `|D|=1`, delete its unique member.  The retained four modes are all
  transverse, so the existing four-mode collision inverse makes every
  `r_p` nonzero.
- If `|D|=2` and one member is regular, delete the other member.  The retained
  set has three transverse modes and one regular dependent mode, so the new
  collision lemma again makes every `r_p` nonzero.

The imported root full-span theorem is used only to show that
`h_p|_(B-{u})` is nonzero: each root has at least three nonzero modes.  No
cross-mode span statement is inferred after independent local basis changes.

An exact five-letter type census confirms the boundary.  Among all `5^5`
words over transverse, regular-dependent, `a`-only, `b`-only, and zero types,
there are 20 one-defect words and 70 two-defect words with a regular member.
The 90 two-defect words with both defects one-sided/zero, and 2,944 words with
at least three defects, remain outside the theorem.

## 6. Independence and evidence boundary

The primary uses SymPy for a symbolic collision minor, companion nullspaces,
and quotient-kernel charts.  It checks 1,220 rank-two companion frames and 40
representative retained-tensor systems.

The audit imports no repository code and no computer algebra.  It uses a
larger 2,310-frame companion census, fraction-free determinants, rational
row reduction, 48 independently assembled quotient systems, and polarized
minor coefficients to certify that every vector in each sampled kernel has
rank at most one.

Neither finite census proves the arbitrary-field case split.  The written
companion-line argument, tensor selectors, collision coordinates, and local
flattening proof carry that implication.

## 7. Exact acceptance boundary

Accepted:

- all-companion trapping at a dependent mode with four active deletions;
- injectivity of the four-mode collision operator with three transverse
  pairs and one nonzero proportional pair;
- exact one-sided/zero collision kernels;
- complete two-open detection with one arbitrary local defect; and
- complete two-open detection with two defects and at least one regular
  defect.

Still open:

- two local defects that are both one-sided or zero;
- every cell with at least three local defects;
- fixed-root injectivity and existence or exclusion of a witness;
- `q=0,r>=6`, every `q>=1` cell, and the unfactorized branch;
- universal extraction/gluing; and
- the global Krenn--Gu conjecture.

## Replay record

Before publication, run:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_rank_one_mode_five_cell_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_rank_one_mode_five_cell_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_rank_one_mode_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_rank_one_mode_five_cell_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_rank_one_mode_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_rank_one_mode_five_cell_detector.py
```
