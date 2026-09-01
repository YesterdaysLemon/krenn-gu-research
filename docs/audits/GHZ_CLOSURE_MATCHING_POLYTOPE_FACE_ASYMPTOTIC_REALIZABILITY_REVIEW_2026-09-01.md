# Adversarial review: GHZ closure and matching-polytope face theorem

Date: 2026-09-01

Reviewed package:

- `claims/arbitrary-order/GHZ_CLOSURE_MATCHING_POLYTOPE_FACE_ASYMPTOTIC_REALIZABILITY_THEOREM.md`
- `claims/arbitrary-order/verify_ghz_closure_matching_polytope_face_asymptotic_realizability.py`
- `claims/arbitrary-order/audit_ghz_closure_matching_polytope_face_asymptotic_realizability.py`

## Independence disclosure

This review was written by the same agent (Claude) that wrote the theorem
and both scripts, in the same session.  It is an adversarial self-review,
not an independent audit in the sense of `AGENTS.md` section 5.  The
independent-audit *script* differs from the primary in enumeration
algorithm, family construction code, and evidence mode (numerical control
in addition to the exact check), but a second reviewer has not yet examined
the package.  That absence is recorded here rather than papered over.

## Verdict

**PASS as a scoped exact closure theorem and route no-go.**  The package
proves that `Delta_n` lies in the closure of the matching-tensor image for
every even `n >= 4` and that, consequently, no tensor-level closed condition
can exclude a witness.  It is not a witness, not an approximation of one in
any bounded gauge, and not an exclusion.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## 1. Attacks on the statement

*Is the target the original one?*  Yes: `Delta_n(a) = [a constant]` with all
three coefficients exactly one, blocks `W_ij in C^(3 x 3)`, and the sum over
all perfect matchings of `K_n` with non-edges carrying zero blocks.  No
herald, ancilla, or normalization change is involved.

*Is "closure" being confused with "image"?*  The document states repeatedly
that the theorem concerns the closure only and that the conjecture is the
statement about the image.  Corollary D's unconditional part is restricted
to `n = 6`, where it cites the six-vertex computer-assisted exclusion; the
`n >= 8` part is explicitly conditional on the conjecture.

*Does the family really have exactly `T(c^n) = 1`?*  A perfect matching
inducing `c^n` consists of colour-`c` edges, so it is contained in the
colour class `M_c`; two perfect matchings with one containing the other are
equal.  Hence the only contribution is `eps^(nu(M_c)) = eps^0`.  The
symbolic check confirms this for `n <= 10`, and the numeric control finds
the constant coefficients equal to one to machine precision.

## 2. Attacks on the proof of Theorem B

*Truncation bookkeeping.*  The perfect matchings of the truncated graph use
one or three attachment edges; zero and two are impossible by parity of the
triangle.  The one-attachment matchings biject with the perfect matchings of
`G` (remove `t_a t_b` and `u_c t_c`, add `v u_c`), and this bijection
preserves colour classes.  The three-attachment matchings are in bijection
with perfect matchings of `G - N[v]`.  The verifier's counts
`3, 4, 5, 7, 10, 15, 23` for `n = 4, ..., 16` are consistent with this
recursion (for example, `5 = 4 + 1` at `n = 8` because the prism minus a
closed neighbourhood is a single edge).

*Potential recursion.*  `nu'(M') = nu(M)` for lifted matchings is an exact
cancellation of `+A` and `-A`.  For three-attachment matchings the bound on
`A` is derived correctly; the code computes the minimum inner potential over
all perfect matchings of `G - N[v]` exactly and takes the ceiling.  The
verifier found `A = 1` suffices at every step through `n = 16`.

*Face equivalence.*  The claim "`(3)` for some integer `nu` iff
`{M_0,M_1,M_2}` is the vertex set of a face" uses that perfect-matching
polytopes have exactly the perfect matchings as vertices and are rational.
Both are standard.  The theorem does not otherwise depend on this
equivalence; the construction supplies `nu` directly.

## 3. Attacks on Corollary C

The corollary is pure continuity.  One might object that repository
"sensor" and "rank-drop" arguments are conditions on `T`; the document is
careful that those arguments are valid exactly insofar as they are
consequences of exact identities in `W` derived from `T_W = Delta`.  The
corollary refutes only arguments that use closed conditions on `T_W` alone.

## 4. Attacks on the evidence

- The primary and the audit share no code.  The primary uses recursive
  perfect-matching enumeration and a sympy expansion over all perfect
  matchings of `K_n`; the audit uses a bitmask dynamic programme and a
  numpy einsum evaluation of the full `3^n` tensor.
- The audit's numerical bound `eps^(nu_min) <= max mixed <= extras * eps^(nu_min)`
  is loose but correct; the observed values equal `eps^(nu_min)` up to
  rounding at `n = 6, 8, 10`.
- Both scripts write a JSON summary to the untracked `tmp/` directory; no
  generated artifact is tracked.
- Runtime is under one second each; the fast-verifier set in
  `check_hygiene.py` was deliberately not extended, since the theorem does
  not gate any existing claim.

## 5. Novelty and provenance

The abstracts and problem page of Krenn--Gu--Soltesz, Chandran--Gajjala,
Chandran--Gajjala--Illickan, and the maintained problem page were inspected
at abstract level on 2026-09-01; none mentions closures, limits, or weights
tending to zero or infinity.  This is a bounded novelty assessment, not a
literature search of record, and no source is imported as a premise.  The
document records this boundary.

## 6. Frontier consequence

The frontier gains one node `BR1` with a dashed boundary edge from `G0` and
a boundary edge to the gluing node `GL`, one node-key row, two typed-edge
rows, and one refuted-route row.  No existing node, edge, status, or scope
changes.  The global status remains **UNRESOLVED**.
