# Exact-fibre resolution attempt, 2026-09-04

Status: completed parent attempt; parent not solved. This is a coordination
and outcome record, not a theorem. Global status: **UNRESOLVED**.
Base: `80b3565b5b8808522d2389fa491543cffdf28e41` (`origin/main`).

## One parent and its exhaustive first split

For every even integer n >= 6 and every collection of complex 3-by-3
edge matrices W on n labelled vertices, prove that its perfect-matching
tensor T_W differs from Delta_3, or produce an exact counterexample.
This is pointwise, with no genericity, degree, nonzero-entry, or reality
restriction. Restricting the alphabet to three colours handles all d >= 3.
The downstream consumer is the original global Krenn--Gu conjecture.

The first split is exhaustive: every edge matrix is diagonal, or at least
one edge matrix has a bichromatic entry. The former branch requires the
arbitrary-order weighted Bogdanov proposition (Parent A in the fibre-exact
brief). The latter requires an exact-fibre argument retaining all mixed
entries; a proof of the former alone is not a global resolution.

Upstream supply: the exact matching-tensor definition and ternary
restriction in README; WB2's witness-to-AP-prime bridge and WB3's
accessibility/common-matching mechanisms for the diagonal branch; the
accepted killer, maximal-root, and full-source identities for the general
branch, with each worker required to identify the owning hypotheses before
use. BR1 is a mandatory sharp control: tensor-image closure contains GHZ,
so a tensor-only closed obstruction cannot solve the parent.

## Assigned independent attacks

1. All-diagonal branch: attempt the complete AP-prime parent analytically,
   combining accessibility, forcing, and three-colour partitions; do not
   stop at another degree/support sibling.
2. General branch: attempt an arbitrary-order exact-fibre implication from
   the killer/cofactor identities that rules out a full witness. Identify
   and test the precise load-bearing missing implication if it fails.
3. Adversarial diagonal branch: seek an exact abstract AP-prime countermodel
   to eliminate the support-only mechanism, with bounded computation and
   direct independent validation. Such a model is not a weighted witness.
4. Coordinator: attempt exact polynomial/cofactor synthesis; integrate and
   adversarially review proposed mathematical deltas.

Success means a proof of the parent, an independently validated exact
counterexample, or a proved mechanism obstruction with a strictly sharper
next lemma. A scoped branch result remains explicitly scoped. No numerical
limit, untraced solver UNSAT, local chart, or documentation pass counts as
resolution. No scientific claim is promoted before independent review.

Only the coordinator packages accepted work. Workers own all computations
they launch, use bounded runners for long jobs, and write only assigned
scratch files under this isolated worktree. Existing worktrees and the
owner's untracked root file are untouched.

## Outcome

No global proof, exact original-conjecture counterexample, or complete
all-diagonal exclusion was found. The accepted mathematical delta is the
[pure-matching scaffold mechanism obstruction](../../claims/arbitrary-order/PURE_MATCHING_SCAFFOLD_STRUCTURAL_GATE_NO_GO_THEOREM.md),
with [independent review](../audits/PURE_MATCHING_SCAFFOLD_STRUCTURAL_GATE_NO_GO_REVIEW_2026-09-04.md).
It shows that pure targets, killers, termwise annihilation, the entire
majority ideal hierarchy, and strong maximum-root blockers jointly leave
unbounded surplus possible. The owning proof specifies the generic scope,
nonwitness coefficient, exact finite replays, and the source-sensitive next
obligation. No branch of the global witness locus was excluded.

The analytic AP-prime attack tried extracting one perfect matching per
colour whose every edge union has nonzero support-family status. Its
one-colour intermediate inference fails even for three disjoint four-cycles
with every edge top-active: the family can encode the incompatible
orientation requirements x0=x1, x1=x2, x0!=x2 by omitting 24 two-matching
subsets while retaining accessibility and unique-matching forcing. This is
not a three-colour AP-prime model and cannot be realized by actual hafnian
weights, whose disconnected-component multiplication would forbid those
omissions. Thus a continuation must use cross-colour constraints or retain
the actual factorization law. This failed intermediate route was not
promoted into a separate frontier theorem.

The adversarial AP-prime search found no model. Among 1,440 sampled fixed
support triples at n=10,12,14, 1,380 had an explicitly forced rainbow
partition and 60 were rejected by a family SAT encoding. These are sampled
search outcomes, not exhaustive finite exclusions or certified UNSAT proof
leaves. Two small constrained n=10 support searches also returned UNSAT;
no all-n inference is made. Scratch scripts, outputs, and bounded-run
receipts remain in the ignored task-owned tmp directory.

The literature check was bounded reconnaissance, not a completeness or
novelty claim. It inspected the primary arXiv abstract for
[Krenn--Gu conjecture for sparse graphs](https://arxiv.org/abs/2407.00303),
the Quantum Optics paragraph in section 4 and reference 38 of
[Advancing Mathematics Research with AI-Driven Formal Proof Search, v2](https://arxiv.org/html/2605.22763v2),
and the statement and scope in the author's
[sharp-colour-bound repository](https://github.com/KitaKen1/monochromatic-quantum-graph-sharp-bound-lean/blob/main/README.md).
No new external theorem was imported into the scaffold proof. The
in-preparation manuscript named in reference 38 was not available for
theorem inspection; its title is not evidence of a ternary resolution.

The frontier records the mechanism no-go. Existing mathematical claims and
the global UNRESOLVED status are unchanged. No remote branch, pull request,
website, or external communication was published during this attempt.
