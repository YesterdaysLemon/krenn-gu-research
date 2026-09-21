# Review handoff: complete common-star full-source exclusion

**Global Krenn--Gu remains UNRESOLVED.** The new result excludes the entire
common-star protected-K4 construction over C at every k>=2. It is an
all-order branch closure, not a finite search or a degree refinement.

## Compact argument to review

At each protected K4, vertex 0 is the center and vertex c+1 the color-c
leaf. Internal edges are the three unit monochromatic perfect matchings.
A simple component edge has one unequal color label (a,b) and exactly two
nonzero crossing factors: center-center A and selected-leaf B. All other
crossing entries vanish.

Give the center of component u color x_u and all three leaves color y_u.
Only its color-y_u leaf can cross; the other two leaves are forced onto
their unit protected edge. Thus the literal physical source is

    F(x,y) = sum_(S even) haf A_x[S] haf B_y[S]
                         product_(u outside S) delta(x_u,y_u).

Both hafnians use the same actual physical array. A full witness requires
F(x,y)=sum_c product_u delta(x_u,c)delta(y_u,c).

Contract at each component with r_u[x_u]s_u[y_u], choosing r_u dot s_u=0.
Every proper S disappears. For odd k>=3 nothing survives, while the choice
r=(1,1,1), s=(1,1,-2) gives target 2-2^k!=0. This parity case also works
using component-constant words alone and one zero-sum covector per site.

For even k, only S=V survives, so the source factors as A(r)B(s). Choose
two r systems differing only at site 1, with (1,-1,0) or (1,0,-1), and
two s systems differing only at site 2 by the same choices. Set s_1 and
r_2 to (1,1,1). At every remaining site use r=(1,1,1), s=(1,1,-2).
All four cross pairs are locally orthogonal. Their source matrix has
rank at most one, but their target matrix is

    [[2,1],[1,1+2^(k-2)]],

whose determinant is 1+2^(k-1)!=0. The k=1 K4 is the sharp valid exception.

## Exact claim boundary

The even-k argument requires independently colored centers and leaf
triples. Those words are not all supplied by CSQ4 (component-constant
targets plus physical U4) or FB (the written binary subsystem). Neither
even-k CSQ4 nor FB is claimed proved. The full common-star branch is
excluded directly, bypassing those intermediate routes.

Arbitrary protected hollow blocks can add center-leaf crossings or use
a leaf in a different color. They need not satisfy the factorization.
No arbitrary-witness-to-common-star or arbitrary-witness-to-scaffold
normal form is assumed. The dedicated review is by a separate agent in
the same session; there is no claim of human refereeing or Lean proof.

Please focus adversarial review on the completeness of the physical
matching classification, all four cross-orthogonality conditions, the
outer-product argument over C without conjugation, and the scope boundary.

## Inspectable evidence

- [Full proof and source definitions](../../claims/arbitrary-order/PROTECTED_SCAFFOLD_COMMON_STAR_FULL_SOURCE_EXCLUSION.md).
- [Independent proof review](../audits/COMMON_STAR_FULL_SOURCE_EXCLUSION_REVIEW_2026-09-20.md).
- [Primary exact companion](../../claims/arbitrary-order/verify_common_star_full_source_exclusion.py).
- [Independent no-import audit](../../claims/arbitrary-order/audit_common_star_full_source_exclusion.py).
- [Scientific mutation tests](../../tests/test_common_star_full_source_exclusion.py).
- [Parent attempt and continuation](exterior-coupling-parent-resumption-2026-09-20.md).

From repository root:

```text
python claims/arbitrary-order/verify_common_star_full_source_exclusion.py
python claims/arbitrary-order/audit_common_star_full_source_exclusion.py
python -m unittest -v tests.test_common_star_full_source_exclusion
```

The universal quantifier comes from the written proof. Finite exact
replays corroborate its identities and reject altered hypotheses.
