# Independent hostile review: generic K4 scaffold obstruction

Reviewer: independent AP analytic subagent, 2026-09-04; integration and scope
review by the coordinator. Reviewed the K4 construction now owned by the
[structural-gate obstruction](../../claims/arbitrary-order/PURE_MATCHING_SCAFFOLD_STRUCTURAL_GATE_NO_GO_THEOREM.md).
This is a scoped mathematical review, not a Lean proof or global resolution
audit. It asserts no original-conjecture witness.

Verdict: **PASS** for the precisely delimited no-go claim. It is a family
satisfying the listed necessary gates, while demonstrably failing full mixed
target equations. It must not be described as satisfying the full-source
identity or every theorem in the maximal-root literature.

## Independently derived checks

1. The three K4 factor matchings are disjoint and cover every intra-component edge. Hollow inter-component blocks contribute no monochromatic entries. Thus each pure coefficient is exactly one and every vertex has its three singleton Ecc killers.

2. A torus root contains at most one vertex per K4. The three same-component neighbours of each root are distinct from all other such neighbours, yielding 3r genuine outside blockers and r per colour. The matching argument for a single colour also applies to non-torus roots whenever that colour coordinate is nonzero at every root. At a chosen scaffold neighbour of a zero pair, the blocker determinant for that scaffold colour is identically zero because the incident row is proportional to ec. Thus at least five fixed divisibilities with scalar zero are valid for every rank>=2 free pair block. The fact that scalar zero is permitted is essential and is explicit in the owning theorem.

3. For |S|=m+q, a perfect matching contains a=q+d>=q internal S edges, with d its number of internal complement edges. Using q internal edges of Mc gives an explicit product of q generators of IS equal, after multiplication by remaining colour coordinates, to the desired pure tensor on S. This matches the exact ideal-power definition in MAJORITY_SUBSET_INTERNAL_EDGE_IDEAL_HIERARCHY.md and proves its dual harmonic consequence. No radical-to-ideal substitution is made.

4. Independent six-root incidence: over the 12-dimensional torus of projective root variables, fifteen equations each use their own block parameters and are nonzero linear functionals. The incidence dimension is D-3, so its projection closure cannot fill D-dimensional parameter space. There are only finitely many six-sets. Sets containing an intra-K4 pair have no torus points at all. Consequently a generic filling has no six roots.

5. Independent five-root dominance: direct expansion of a hollow block in normalized variables is

   f=b01*s+b02*t+u*b10+u*b12*t+v*b20+v*b21*s.

   Its value and four first derivatives at all ones have rank five as linear functions of its six entries. Rational row reduction gives exact preimages of all four derivative-only jets. Assigning outgoing edges of the regular K5 tournament to the two coordinates at each vertex produces an invertible 10x10 root Jacobian. The incidence projection is dominant; its constructible image contains a nonempty open. The explicit two forms in the draft are an even simpler realization of these jets. Intersecting this existence open with the finite no-six opens is legitimate in irreducible affine parameter space.

6. Uniform exterior rank: for any torus x, the three coordinates of x^T B use disjoint pairs of free off-diagonal coefficients; each pair has nonzero coefficients. Hence B->x^T B is onto, without any genericity assumption on x beyond torus support. For an outside vertex there are either zero fixed rows and five independent free rows, or one fixed coordinate row and four independent free rows. Failure of rank three has codimension three in either case: rank<=2 for a 5x3 matrix, or rank<=1 for its 4x2 quotient. These parameters are disjoint from all internal root equations. The bad incidence therefore has dimension at most D-3, stronger than the draft's sufficient D-1 bound. This proves a uniform statement at every five-root tuple, not merely a statement at a selected tuple. Finitely many root sets and outside vertices suffice.

7. Generic nonwitness: at zero hollow filling, the word constant on each K4 with different colours on two components has exactly one matching contribution. Therefore its coefficient polynomial has constant term one. Its nonvanishing open meets all preceding generic opens. Positive algebraically independent real parameters provide an exact existence choice avoiding proper rational algebraic bad loci and preserve a strictly positive mixed coefficient. This is not an explicit rational specialization or computational witness certificate.

8. Depth-floor usage: the owning companion theorem's expansion and |I|=s+2p count apply to arbitrary physical tensors before target substitution. It is valid to say these graphs have surplus n-10 and lack pair columns in that linear expansion. It would be invalid to infer that they satisfy the nonzero GHZ source equation; the draft explicitly declines this inference.

## Exact computational corroboration

The [independent replay](../../claims/arbitrary-order/audit_pure_matching_scaffold_structural_gate_no_go.py)
uses only Python Fraction arithmetic, an independently written RREF, and
direct coefficient expansion. It verifies rank5 of the jet map, constructs
four rational jet preimages, verifies rank10 of the K5 root Jacobian, and
checks an exterior row-map representative. The all-torus row surjectivity
and arbitrary-order dimension statements above are human proofs; the finite
code is not their substitute.

The separate [primary replay](../../claims/arbitrary-order/verify_pure_matching_scaffold_structural_gate_no_go.py)
was written by the adversarial-search subagent using sparse polynomial
expansion, an exact determinant, and exhaustive eight-vertex matching
enumeration. The reviewer did not import it. The coordinator reran both
scripts on the integrated candidate tree.
