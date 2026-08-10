# Matching saturation is necessary on every axis-deficient root jet

## Status

**Exact arbitrary-order characteristic-zero reduction.**  Consider a
hypothetical three-colour GHZ graph witness on a root/kernel slice whose
three target diagonal coefficients are nonzero.  Suppose the root--blocker
rows vary projectively to first order.  At root `i`, restrict to

```text
S_i=ker(a_i),             a_i(1,1,1) != 0,         (1)
```

so every differentiated root--blocker edge vanishes.

For every nonempty root subset `I`, form the restricted companion graph
appropriate to the `I`-mixed derivative:

1. an edge from `i in I` to a fixed vertex outside `I` is admissible when
   its one-tangent contraction is nonzero on `S_i`;
2. an edge `{i,j}` inside `I` is admissible when its tangent--tangent
   restriction on `S_i tensor S_j` is nonzero.

Then exactly one of the following necessary alternatives holds:

```text
the admissible companion graph has a matching saturating I;
I contains roots of all three coordinate-axis types
  a_i=e_0^*, a_j=e_1^*, a_k=e_2^*.                (2)
```

Equivalently, every root subset missing at least one coordinate-axis type
must be saturable by effective companion edges.

This incorporates root--root tangent propagation rather than assuming it
away.  It is a necessary matching condition, not a sufficient construction:
an admissible saturating matching may fail to extend to a perfect matching,
its complementary cofactor may vanish, and different terms may fail the
full mixed-colour identities.  The arbitrary-order local-to-global reduction
and the global Krenn--Gu conjecture remain **UNRESOLVED**.  No finite field
is used.

## Differentiated matching terms

Fix a nonempty subset `I` of roots and differentiate the matching tensor once
at each root in `I`, along vectors `y_i in S_i`.  A term is indexed by one
perfect matching of the whole graph.  Each root in `I` is incident to exactly
one edge of that matching.

If its partner lies outside `I`, the differentiated edge evaluates through
the one-tangent contraction

```text
B_(i,v)(y_i,z_v).                                  (3)
```

If two roots `i,j in I` pair together, their edge evaluates through

```text
B_ij(y_i,y_j).                                     (4)
```

Root--blocker instances of (3) vanish on `S_i` by (1).  Every nonzero term
therefore selects admissible edges of types 1--2 above.  Because those edges
come from a perfect matching, they are vertex-disjoint and saturate every
root of `I`.

Consequently, if no admissible matching saturates `I`, every differentiated
matching term vanishes separately.  The complete graph `I`-mixed derivative
is zero.  This conclusion uses neither cancellation nor any assumption on
the complementary hafnians.

## When the GHZ derivative is zero

After logarithmic normalization, the GHZ `I`-mixed derivative has its three
diagonal coefficient forms proportional to

```text
product_(i in I) y_i[0],
product_(i in I) y_i[1],
product_(i in I) y_i[2].                           (5)
```

The three omitted proportionality constants are nonzero by the slice
hypothesis.  For coordinate `c`, the corresponding multilinear form is the
tensor product of the functionals `e_c^*|S_i`.  It vanishes identically if
and only if one factor vanishes.  Since both `S_i` and `ker(e_c^*)` are
hyperplanes,

```text
e_c^*|S_i=0  iff  S_i=ker(e_c^*)
              iff  a_i is projectively e_c^*.     (6)
```

Thus all three forms in (5) vanish exactly when `I` contains at least one
root of each coordinate-axis type.  If `I` misses an axis type, the GHZ
mixed derivative is nonzero.  Equality with the zero graph derivative is
then impossible, proving (2).

## Immediate corollaries

Let `R_c` be the roots whose tangent covector is coordinate axis `c`, and
let `R_*` be the non-axis roots.

1. `R_*` must admit a saturating companion matching whenever it is nonempty.
2. For each coordinate `c`, the full set `R\R_c` must admit a saturating
   companion matching whenever nonempty.
3. Every one- or two-root subset must be saturable, because fewer than three
   roots cannot contain all three axis types.
4. If there are no effective root--root edges and only `t` fixed nonroot
   companion endpoints, applying (2) to every `(t+1)`-subset recovers
   `t>=ceiling(2r/3)` and the axis multiplicity bounds in
   [`ROOT_FINITE_NONROOT_COMPANION_ENDPOINT_COUNT_OBSTRUCTION.md`](ROOT_FINITE_NONROOT_COMPANION_ENDPOINT_COUNT_OBSTRUCTION.md).

The new unresolved object is therefore explicit: classify effective
root/root and root/nonroot companion graphs that saturate every
axis-deficient subset while their actual complementary hafnian classes also
satisfy the quotient-frame, mixed-colour, and higher-cofactor identities.

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_root_restricted_jet_companion_matching_saturation_necessity.py
python claims/arbitrary-order/audit_root_restricted_jet_companion_matching_saturation_necessity.py
uv run --with sympy --with ruff python -m ruff check claims/arbitrary-order/verify_root_restricted_jet_companion_matching_saturation_necessity.py claims/arbitrary-order/audit_root_restricted_jet_companion_matching_saturation_necessity.py
python -m py_compile claims/arbitrary-order/verify_root_restricted_jet_companion_matching_saturation_necessity.py claims/arbitrary-order/audit_root_restricted_jet_companion_matching_saturation_necessity.py
```

The primary reconstructs the zero-product criterion with exact symbolic
kernel bases and audits the incident-edge saturation ledger for perfect
matchings through ten vertices.  The no-import audit uses independent
integer kernels and perfect-matching recursion through twelve vertices.
These bounded enumerations audit the indexing; the arbitrary-order theorem
is the termwise matching argument above.
