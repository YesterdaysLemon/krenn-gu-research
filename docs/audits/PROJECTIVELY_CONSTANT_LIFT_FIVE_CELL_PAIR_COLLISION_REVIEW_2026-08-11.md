# Adversarial review of the five-cell pair-collision detector

## Review status and provenance

This record reviews
[`PROJECTIVELY_CONSTANT_LIFT_FIVE_CELL_PAIR_COLLISION_AND_ALL_COMPANION_DETECTOR_THEOREM.md`](../../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_FIVE_CELL_PAIR_COLLISION_AND_ALL_COMPANION_DETECTOR_THEOREM.md)
as a conditional characteristic-zero theorem.

Codex reconstructed the common-kernel contraction, the scalar proportionality
argument, and the rank-two companion zero-edge lemma independently of the
primary script.  The standard-library audit separately uses a recursive
permanent, rational elimination, and a larger finite companion census.  This
is durable adversarial reasoning, not an independent human review.

Review verdict: **accept arbitrary-companion detection on the stated locally
transverse root-pair stratum** after the focused and repository-wide replay
gates pass.  At most one persistent root may fail double transversality.  The
result is not full five-cell closure, fixed-root injectivity, or witness
exclusion.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Reconstructed obligation

For four persistent roots `P={1,2,3,4}`, define

```text
B_pq=P_5(h_p,h_q,a,a,b),
C_i=sum_(v!=i) ell_v tensor B_(P-{i,v}).               (1)
```

The prior theorem made the coefficient map injective away from a zero
companion and a balanced `2+2` split.  The present obligation is different:
show that **every** rank-two companion kernel has a zero pair-tensor slot,
then prove that the physical pair tensors are all nonzero on a specified
root-transverse stratum.

## 2. Common-kernel contraction audit

Assume `a_u,b_u` are independent and choose

```text
0!=k_u in ker a_u intersection ker b_u.               (2)
```

For arbitrary row families `h,g`, set

```text
alpha_u=h_u(k_u),            beta_u=g_u(k_u).         (3)
```

Contracting `P_5(h,g,a,a,b)` at `k_u` kills assignments of either `a` row
and of `b`.  The only survivors assign `h` or `g` to mode `u`, giving

```text
P_4(alpha_u g+beta_u h,a,a,b;B-{u}).                  (4)
```

The review checked the labelled-row multiplicity.  Both four-mode tensors
contain the factor two from the repeated `a` rows, so no extra scalar is
needed in (4).  The primary checks all `5 x 81` slices with a labelled
permanent; the audit uses deletion recursion and unrelated integer data.

On the four retained modes, the prior collision theorem is injective.  If
the five-mode pair tensor vanishes, (4) therefore gives

```text
alpha_u g_v+beta_u h_v=0               for v!=u.      (5)
```

## 3. Double transversality and the third support mode

Suppose `alpha_p,alpha_q` are nonzero at distinct modes and `h_r!=0` at a
third mode.  From (5),

```text
g_r=lambda_p h_r=lambda_q h_r,
lambda_p=-beta_p/alpha_p,
lambda_q=-beta_q/alpha_q.                             (6)
```

The nonzero covector `h_r` forces a common scalar `lambda`.  The remaining
`p` and `q` equations give `g=lambda h` at every mode.  But evaluation at
`k_p` gives both

```text
beta_p=lambda alpha_p,
beta_p=-lambda alpha_p.                               (7)
```

Thus `2 lambda alpha_p=0`; characteristic zero gives `g=0`.

The third support mode is obtained from the imported cross-mode full-span
theorem only before any local normalization: a three-dimensional span needs
at least three nonzero covectors.  Nonzeroness survives independent local
basis changes.  The proof does **not** infer that normalized row coordinates
still have cross-mode span three.

## 4. Rejected universal pair-injectivity strengthening

The review explicitly checked the normalized ambient kernel

```text
a_u=e_0^*,                 b_u=e_1^*,
h=(b,b,b,a-b,a-b),
g=(0,0,0,-a,a).                                      (8)
```

Every coefficient of `P_5(h,g,a,a,b)` is zero although `g!=0`.  Both scripts
replay this exact identity independently.  It is not a lifted root pair:
`g` has only two nonzero mode entries and violates root-row full span.  It
does show that local `a/b` transversality and full support of `h` alone do
not justify deleting the double-transverse hypothesis from the operator
lemma.

## 5. Rank-two companion zero-edge lemma

Package the pair tensors into a symmetric zero-diagonal matrix

```text
X_iv=B_(P-{i,v}),                 XL=0,               (9)
```

where `L` has the four companion rows and rank two.  Assume for contradiction
that all six tensor entries of `X` are nonzero.  Over an infinite
characteristic-zero field, a functional can be chosen nonzero on all six
entries.  Entrywise evaluation gives a scalar symmetric matrix `Y` with
zero diagonal, `YL=0`, and all six off-diagonal entries nonzero.

The two columns of `L` lie in `ker Y`, so `rank Y<=2`.  Symmetric rank one
with zero diagonal is impossible unless `Y=0`; hence `rank Y=2`.  A nonzero
off-diagonal principal block is hyperbolic, so

```text
Y=u v^T+v u^T.                                       (10)
```

The zero diagonal gives `u_i v_i=0`.  Nonzero entries can therefore occur
only across the two disjoint supports of `u` and `v`.  Their support graph is
bipartite and cannot be the complete graph on four indices.  This contradicts
six nonzero off-diagonal entries.

The argument is strictly weaker than classifying every kernel vector, but it
is exactly sufficient: collective invisibility forces at least one physical
pair tensor to vanish for every rank-two companion frame, including the two
previous coefficient exceptions.

## 6. Detector transport

A doubly transverse root `p` has two nonzero `alpha` values, while root-row
full span supplies the third nonzero mode.  The pair-collision lemma makes

```text
g |-> P_5(h_p,g,a,a,b)                               (11)
```

injective.  Hence `B_pq!=0` for every other root `q`.

If at most one of the four roots is not doubly transverse, every unordered
pair has a doubly transverse endpoint.  All six `B_pq` are nonzero, so the
zero-edge lemma forbids all four `C_i` from vanishing.  The projective
two-open variation is a tensor product of the selected nonzero `C_i` with
the absorption covector, so every nonzero absorption direction at that root
is detected.

## 7. Independence and evidence boundary

The primary uses SymPy for the exact four-mode rank, 120 normalized
five-mode injectivity charts, and 1,220 companion frames; it checks the
common-kernel identity with a labelled permanent and runs two end-to-end
exceptional-frame models.  The audit uses standard-library rational
elimination on 150 separately assembled charts and 2,310 companion frames,
plus a recursive permanent for both the contraction identity and the sharp
kernel.

The finite chart and frame censuses do not prove the arbitrary-field result.
The written contraction/proportionality proof and the symmetric hyperbolic
support proof carry that implication.

## 8. Exact acceptance boundary

Accepted:

- the common-kernel contraction identity;
- five-mode pair-collision injectivity from two transverse and one additional
  nonzero mode;
- the exact weak-root ambient kernel preserving the scope wall;
- the rank-two companion zero-edge lemma;
- all-pair nonvanishing when at most one root is weak; and
- arbitrary-companion two-open detection on that stratum.

Still open:

- exceptional companion frames with at least two quotient-support-at-most-one
  root rows;
- local `a/b` dependence and deletion-activity failure;
- complete `q=0,r=5`, all `q=0,r>=6`, every `q>=1`, and the unfactorized
  branch;
- fixed-root injectivity, witness exclusion, and universal gluing; and
- the global Krenn--Gu conjecture.

## Replay record

Before publication, run:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_projectively_constant_lift_five_cell_pair_collision_detector.py
python claims/arbitrary-order/audit_projectively_constant_lift_five_cell_pair_collision_detector.py
python -m py_compile claims/arbitrary-order/verify_projectively_constant_lift_five_cell_pair_collision_detector.py claims/arbitrary-order/audit_projectively_constant_lift_five_cell_pair_collision_detector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_projectively_constant_lift_five_cell_pair_collision_detector.py claims/arbitrary-order/audit_projectively_constant_lift_five_cell_pair_collision_detector.py
```
