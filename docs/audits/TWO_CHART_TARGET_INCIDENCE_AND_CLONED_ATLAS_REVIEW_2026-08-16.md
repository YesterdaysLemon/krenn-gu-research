# Two-chart target-incidence and cloned-atlas review

Date: 2026-08-16

Global status: **UNRESOLVED**

Reviewed claim:
[`Two-chart target incidence and cloned camouflage atlas boundary`](../../claims/arbitrary-order/TWO_CHART_TARGET_INCIDENCE_AND_CLONED_CAMOUFLAGE_ATLAS_BOUNDARY_THEOREM.md)

## 1. Review question

The package was reviewed against the following exact question.

> Do two constant uncontracted chart equations give a noncircular
> supply-or-detect trichotomy, and do additional overlapping GLD3 pair/four
> packages force either a three-active detector or a coefficient-pure overlap
> defect?

The review separated four claims that must not be conflated:

1. affine target incidence in the arbitrary-deck space;
2. conversion of a left syzygy into an actual mixed target coefficient;
3. matching-integrable physical `q=2` response data; and
4. constant target attachment from a hypothetical full GHZ witness equation.

Only the first three are addressed, and the physical counterboundary in item
3 observes only the selected `D`-pair/`T`-four package.  Item 4 remains open.

## 2. Exact positive result

For constant chart maps

```text
T=g_c+A_c p+B_c n_c,      c=0,1,
```

the stacked target equation is `M(p,n_0,n_1)=tau`.  Quotienting nuisance
images gives

```text
bar A : P -> coker B_0 direct_sum coker B_1.
```

The proof establishes the exhaustive trichotomy:

- target nonincidence;
- incidence plus injectivity, which uniquely supplies `p`; or
- incidence plus nonzero kernel, which leaves an affine common-sector fibre.

The load-bearing rank statement is a **conjunction**:

```text
rank[M|tau]=rank M
and
rank M-rank diag(B_0,B_1)=dim P.
```

The second equality alone proves only injectivity.  The hostile reviewer found
the exact counterexample `F=P=K`, no nuisances, `A_0=A_1=id`, `g_0=0`,
`g_1=1`, `J=0`; the equality holds while target incidence fails.  The theorem,
primary verifier, and independent audit were all repaired to retain the
conjunction.

## 3. Target coupling and sparsity

For `ell=(ell_0,ell_1) in ker M^*`, the exact identity is

```text
ell(tau)=(ell_0+ell_1)(J-T).
```

This is a target-defect aggregate before pure normalization.  After the
**complete** pure word basis is synchronized, its remaining support is mixed.
If the aggregate is one mixed evaluation plus synchronized pure evaluations,
one actual coefficient is displayed.  For a fixed mixed set `S`, the exact
feasibility problem is the constant linear system

```text
M^*ell=0,
(ell_0+ell_1)_w=0 for w outside the pure basis union S,
ell(tau)=1.
```

The normalization replaces the non-linear-looking condition
`ell(tau)!=0`; every nonzero separator can be rescaled.

The dense affine family has a one-dimensional left kernel whose aggregate is
`sum_i x_i^*`.  Its support is arbitrarily large, while the common tensor can
avoid any preselected mixed coordinate.  It therefore refutes a uniform sparse
certificate from bare affine cokernel data or ordinary Noetherianity.  The
family is not promoted to a physical graph response.

## 4. Physical cloned-package audit

The physical control uses one common residual pair, `h=1`, two type-`A` ports,
one core type-`B` port, and arbitrarily many cloned type-`B` ports.  Every
selected window is `{0,1,2,j}`.  Direct calculation and independent perfect-
matching enumeration give

```text
T_j=3 e_0^tensor4+(4/3)e_1^tensor4+e_2^tensor4.
```

Every selected pair tensor is diagonal, all 78 mixed four-port coefficients
vanish, and all three pure coefficients are nonzero.  At every chart port the
active-colour set is exactly `{0,1}`: the only colour-`2` edges are the
complementary pair `01,2j`, so the complementary different-colour product
required by GLD3 is absent.

Each sign realization separately has one common physical graph, common
residual rows, identity overlap transitions, and trivial holonomy.  The global
change `K -> -K`, `B=D-K -> D+K` produces a **second physical graph** with the
same selected `D`/`T` packages.  It is not a second channel inside one fixed
graph and not a common `O(J)` gauge change.

Two limitations are explicit and load-bearing.

1. A complete GLQ2 chart retains the residual-absent deck `M`, whose pair
   layer is `B`; it distinguishes the two sign realizations.  The result is an
   observed-package ambiguity, not a full paired-response-atlas ambiguity.
2. Only the sunflower windows `{0,1,2,j}` are controlled.  Four-sets containing
   multiple clones and higher responses on the union have additional equations
   and are not claimed diagonal.

Thus arbitrarily many common-core observed windows do not force activity or an
overlap defect, but all-subwindow, deeper-depth, and full-witness routes remain
open.

## 5. Evidence independence

The primary verifier
[`verify_two_chart_target_incidence_and_cloned_camouflage_atlas_boundary.py`](../../claims/arbitrary-order/verify_two_chart_target_incidence_and_cloned_camouflage_atlas_boundary.py)
uses SymPy exact ranks and the corrected-compound response formula.  It checks:

- the rank conjunction counterexample;
- dense affine controls for mixed support sizes `2,...,8`;
- cloned atlases with `1,...,7` clone ports;
- every selected pair coefficient and every four-port word;
- exact two-activity, overlap agreement, and sign preservation.

The no-import audit
[`audit_two_chart_target_incidence_and_cloned_camouflage_atlas_boundary.py`](../../claims/arbitrary-order/audit_two_chart_target_incidence_and_cloned_camouflage_atlas_boundary.py)
uses only the Python standard library.  It has a separate fraction-based row
reduction and directly enumerates all fifteen perfect matchings of each
six-vertex residual-plus-window graph for four simultaneous clones and both
sign realizations.  It does not import the primary verifier or SymPy.

The scripts replay the bounded displayed controls.  The arbitrary-field and
arbitrary-clone statements are proved in writing.

## 6. Hostile-review repairs

The fresh hostile review required and rechecked the following repairs:

1. unique supply now requires both incidence and injectivity;
2. the synchronized pure set is the complete pure basis;
3. the sparse-separator test is a genuine normalized linear system;
4. unsupported language about the first six-port leak was removed;
5. `response atlas` was narrowed to `observed-package atlas` wherever the sign
   ambiguity is discussed;
6. the selected-star versus all-subwindow boundary is explicit; and
7. general target-defect aggregates are called mixed only after complete pure
   synchronization.

Final hostile mathematical verdict on the repaired snapshot: **ACCEPT**.
Hashes and the repository-wide replay are recorded only after the final
snapshot is frozen below.

## 7. Frontier effect

This package adds `GLD4`:

- a proved two-chart affine supply/detect trichotomy;
- an exact coefficient-pure mixed-detector criterion;
- a sharp no-uniform-sparsity affine boundary; and
- a sharp arbitrary-breadth cloned observed-package boundary.

It does not add a proved edge from maximal-root data, `GLS2`, or `GLQ2` to
constant target attachment.  It does not extract a permanent restriction.

## 8. Frozen hashes and final validation

The accepted mathematical snapshot is pinned by:

```text
D1D9F2E661766BCA38040B4FF61E6BCC46669D7F3898357E85CE0A6337A97EC7  TWO_CHART_TARGET_INCIDENCE_AND_CLONED_CAMOUFLAGE_ATLAS_BOUNDARY_THEOREM.md
28D83B17B566F61725C016DB3F50A10A280D0B3C3DD69A7DC24763667EE26DB5  verify_two_chart_target_incidence_and_cloned_camouflage_atlas_boundary.py
5EAA7F64A3AA3C7E1ADCFE77FCE7D02F2229BF6E8196254DA659AAA14DD228E5  audit_two_chart_target_incidence_and_cloned_camouflage_atlas_boundary.py
```

Final repository-wide validation: **PASS**.

- primary verifier: PASS;
- independent no-import audit: PASS;
- owning GLD3 primary and independent audit: PASS;
- Ruff check and format check: PASS;
- `py_compile`: PASS;
- `python check_hygiene.py`: PASS (`2112` Python files and `1251`
  Markdown files checked);
- `tests.test_migration_tools`: `191/191` PASS;
- `tests.test_fourteen_vertex_cycle_cover_lattice`: `14/14` PASS;
- link rewrite: zero changes;
- cached-diff and unstaged-diff checks: clean.

The global Krenn--Gu conjecture remains **UNRESOLVED**.
