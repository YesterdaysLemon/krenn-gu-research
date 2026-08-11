# Adversarial review of the complete transverse five-cell detector

## Review status and provenance

This record reviews
[`PROJECTIVELY_CONSTANT_LIFT_COMPLETE_TRANSVERSE_FIVE_CELL_TWO_OPEN_DETECTOR_THEOREM.md`](../../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_TRANSVERSE_FIVE_CELL_TWO_OPEN_DETECTOR_THEOREM.md)
as a conditional characteristic-zero theorem.

Codex reconstructed the companion-imposed zero-pair patterns, weak-root
trapping, and final local-concision case split independently of the primary
script.  The standard-library audit separately uses rational elimination and
a recursive permanent.  This is durable adversarial reasoning, not an
independent human review.

Review verdict: **accept complete two-open detection throughout the locally
transverse aligned projective `q=0,r=5` cell** after the focused and
repository-wide replay gates pass.  "Complete" does not extend beyond this
conditional cell.  Local `a/b` independence is not derived, no witness is
excluded, and the global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Reconstructed obligation

There are four persistent roots and six pair tensors

```text
B_pq=P_5(h_p,h_q,a,a,b).                              (1)
```

Their collective two-open coefficients are

```text
C_i=sum_(v!=i) ell_v tensor B_(P-{i,v}).              (2)
```

Prior work covered good companions under deletion activity and all companions
when at most one root had quotient support below two.  The remaining
obligation was the intersection of exceptional companion frames with
multiple quotient-sparse root rows.  The reviewed proof must close that
intersection without falsely claiming that every full-support pair tensor is
nonzero.

## 2. Common-kernel and weak trapping audit

At each outside mode set

```text
S_u=span(a_u,b_u),
0!=k_u in ker a_u intersection ker b_u.               (3)
```

For a zero pair `B_pq`, contraction at `k_u` gives exactly

```text
P_4(alpha_u h_q+beta_u h_p,a,a,b;B-{u})=0,           (4)
alpha_u=h_(p,u)(k_u),
beta_u=h_(q,u)(k_u).
```

Both repeated-`a` multiplicities are already inside the two four-mode
summands.  The primary and audit independently check all `5 x 81` slices.

Four-mode collision injectivity converts (4) into

```text
alpha_u h_(q,v)+beta_u h_(p,v)=0       for v!=u.      (5)
```

If `p` has at least two nonzero `alpha` values, the prior pair-collision
lemma and the third nonzero mode from root-row full span make every `B_pq`
nonzero.  If instead `p` is weak and `u` is outside its unique possible
escape, then `alpha_u=0`.  Full span gives a nonzero `h_(p,v)` with `v!=u`,
so (5) forces `beta_u=0`.  Thus every zero-pair partner is trapped in `S_u`
at all nonescape modes of a weak endpoint.

The review checked that full span is used only for the invariant count of
nonzero local covectors.  It does not survive arbitrary independent local
basis changes as a common-coordinate span statement, and no such inference
is made.

## 3. Rejected pairwise shortcut

In normalized local bases, the exact row families

```text
h=(a,a,-2a,0,0),
g=(a,a,a,-a,0)                                        (6)
```

have supports three and four but satisfy

```text
P_5(h,g,a,a,b)=0.                                    (7)
```

Both scripts replay all 243 coefficients as zero.  This is not a graph
witness and does not include the fixed five-row diagonal identity.  It does
show that root-row support counts alone cannot replace the companion-pattern
and concision argument.  The theorem preserves this negative result rather
than silently strengthening pair nonvanishing.

## 4. Companion zero-pattern reconstruction

The four equations `C_i=0` are the tensor system `XL=0`, where `X` is
symmetric zero-diagonal and `rank L=2`.

- On a good frame, the already proved companion map is injective, so all six
  `B_pq` vanish.
- If `ell_k=0`, choose independent companions `ell_a,ell_b` among the other
  roots.  The equation at the remaining root `c` splits as

  ```text
  ell_a tensor B_kb+ell_b tensor B_ka=0,             (8)
  ```

  forcing the first two incident pairs zero.  A second equation forces the
  third.  The same derivation covers two zero companions.
- On a balanced partition `{p,q}|{s,t}`, the component of `C_p` on the first
  companion line is `ell_q tensor B_st`; the corresponding component of
  `C_s` is `ell_t tensor B_pq`.  Hence the two within-pair tensors vanish.

The primary checks these exact zero masks on 1,220 rank-two frames.  The
audit reconstructs forced-zero coordinates by rational column-deletion rank
on 2,310 independently chosen frames.  The written companion-line argument,
not either census, proves completeness over an arbitrary characteristic-zero
field.

## 5. Exhaustive local-concision case split

Assume all `C_i` vanish.

1. **Good frame.**  All pair tensors vanish.  A strong root would contradict
   one of its incident zero pairs, so all four roots are weak.  Four singleton
   escape sets cannot cover five modes.  At an uncovered mode all four root
   rows and `b` lie in `S_u`.
2. **Zero companion.**  All three pairs incident with the zero-companion root
   vanish.  If that root is strong, pair injectivity is contradicted.  If it
   is weak, choose any nonescape mode; weak trapping puts all three partners
   into `S_u` there.
3. **Balanced frame.**  Each of the two forced zero pairs would be nonzero if
   either endpoint were strong.  Thus all four roots are weak, and the same
   five-mode pigeonhole supplies a common `S_u` mode.

In every case all five fixed-layer source rows lie in a local space of
dimension at most two.  Every permanent tensor lies locally in their span,
while the weighted ternary diagonal has flattening rank three because all
three weights are nonzero.  This is the required contradiction.

## 6. Independence and evidence boundary

The primary uses SymPy companion nullspaces, exact labelled permanents,
explicit weak-chart nullspaces, the scope-wall tensor, and the escape-set
pigeonhole.  The audit uses standard-library rational ranks, recursive
permanents, rowspace membership instead of nullspaces, independently chosen
weak charts, and a separate dimension ledger.  It imports neither repository
code nor computer algebra.

Neither bounded census proves the arbitrary-field case split.  The written
common-kernel contraction, companion-line decomposition, finite pigeonhole,
and local flattening proof carry that implication.

## 7. Exact acceptance boundary

Accepted:

- weak-root trapping at every nonescape mode;
- exact good/zero/balanced companion zero-pair patterns;
- the negative support-3/support-4 pairwise kernel;
- exhaustive companion/root-transversality case coverage; and
- nonzero two-open detection in the complete locally transverse aligned
  projective `q=0,r=5` cell.

Still open:

- the local `a/b` dependence boundary in aligned `q=0,r=5`;
- fixed-root injectivity and existence or exclusion of a witness;
- `q=0,r>=6`, every `q>=1` cell, and the unfactorized branch;
- universal extraction/gluing; and
- the global Krenn--Gu conjecture.

## Replay record

Before publication, run:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_complete_transverse_five_cell_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_complete_transverse_five_cell_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_complete_transverse_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_complete_transverse_five_cell_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_complete_transverse_five_cell_detector.py claims/arbitrary-order/audit_projectively_constant_lift_complete_transverse_five_cell_detector.py
```
