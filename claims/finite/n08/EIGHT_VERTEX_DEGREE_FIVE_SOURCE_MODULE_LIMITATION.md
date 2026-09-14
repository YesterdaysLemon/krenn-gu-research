# Exact degree-five source-module limitation on the original 134 support

## Statement and scope

On the support in
[`recursive_physical_support_n8_four_cut_survivor_134.json`](../../../tests/fixtures/recursive_physical_support_n8_four_cut_survivor_134.json),
let `R=Q[g_s : s is one of the 134 live entries]`, with all other entries zero.
Let `P_a=T_W(a)-delta_a` for all `3^8=6561` words, and let
`rho=g88*g91-g82*g97`. The exact vector space

```text
L = span_Q{P_a, g_s*P_a : every word a and every live entry s}
    + {q*rho : q in R, deg(q)<=3}
```

contains **no nonzero monomial**. This is an exact finite bounded-space
limitation, not consistency of the full target ideal. Indeed the
[degree-six two-edge certificate](EIGHT_VERTEX_TWO_EDGE_SURPLUS_SHORE_EXCLUSION.md)
excludes this very support. It uses quadratic multipliers outside L.
Global Krenn–Gu remains **UNRESOLVED**.

All degrees count physical entries; the induced cofactors are expanded.
The pure equations contain their actual `-1` constants, with respectively
5,8,10 matching monomials. No proper-cofactor value/support or generic
coefficient field is introduced. Because the matrices are rational, extending
the scalar row-combination field to C cannot turn a missing rational coordinate
vector into a present one.

## Exact reduction and completeness

Polynomial reduction by the single monic binomial with leading term `g88*g91`
replaces it by `g82*g97`. A monomial order choosing that leading term makes the
single polynomial a Groebner basis. This normal form is degree-preserving and
sends every monomial to one monomial. Its kernel through degree five consists
exactly of the permitted rho multiples; no localization is used.

The primary computation enumerates all 105 perfect matchings for all words,
all 6,561 original rows, and all 879,174 distinct live-entry multiples.
Endpoint-colour multigrading divides the homogeneous leading terms. Actual
row-column connected components retain the three shared pure constants and
all 402 pure linear tails, so neither target normalization nor cross-grade
coupling through the low terms is discarded. Exact rational RREF contains a
coordinate vector if and only if it has a singleton row.

The original-row rank is 6,561. The degree-one-multiplier row rank is 877,851;
the latter occupies 463,376 connected components. Both singleton counts are zero.
The original and multiplied layers have disjoint physical degrees (0/4 versus
1/5), so they cannot cancel between layers.

## Independent audit

The [primary probe](../../../tools/explore/probe_physical_degree5_module_134.py)
freezes the complete counts and expansion/coverage hashes in the
[result fixture](../../../tests/fixtures/eight_vertex_degree5_module_134.json).
The [independent audit](audit_eight_vertex_degree5_module_134.py) imports no
primary scientific implementation, reverses the rho orientation, and uses
column-matroid coloop checks rather than RREF of source rows. It reconstructs
the full matching expansions and every pure tail, and agrees on both ranks
and the absence of a monomial.

The small components have a structural explanation: a matching plus one edge
has only two physical vertices of degree two. Its extra-edge decompositions
must use the same physical pair. A matching avoiding that pair determines a
private source-row column; otherwise only a coloured doubled-edge swap is
possible. Rho can add interactions only for extra edges 14 and 15. The audit
explicitly checks the resulting column incidences and actual pure couplings;
the explanation is not substituted for the complete check.

```text
python tools/explore/probe_physical_degree5_module_134.py tests/fixtures/recursive_physical_support_n8_four_cut_survivor_134.json --expected tests/fixtures/eight_vertex_degree5_module_134.json
python claims/finite/n08/audit_eight_vertex_degree5_module_134.py
```

Both calculations were bounded to 900 seconds and 8 GiB, completing in about
27 and 10 seconds respectively. This limits precisely the declared space,
including rho through degree five; arbitrary higher-degree or Laurent target
multipliers are outside it. No separate-human referee or Lean proof is claimed.
