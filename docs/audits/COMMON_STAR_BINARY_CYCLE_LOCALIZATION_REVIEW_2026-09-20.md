# Independent review: common-star binary cycle localization

## Verdict and exact scope

I accept the direct argument in
[`PROTECTED_SCAFFOLD_FULL_BINARY_CYCLE_LOCALIZATION.md`](../../claims/arbitrary-order/PROTECTED_SCAFFOLD_FULL_BINARY_CYCLE_LOCALIZATION.md).
For a fixed color pair in the one-label common-star family, the full binary
cut identity localizes every proper induced directed cycle to one connected
binary resource, with both color states of every cycle component in that
resource.  After deleting the cycle rows, all proper exterior contractions
have the displayed cycle-product values and the full-cycle contraction is
zero.

I also accept the disjoint-shore classification: under the full binary target,
resources with no physical index on both shores occur if and only if the
directed support is one Hamilton cycle and every gadget product is `-1`.
The previously proved PSCS no-singleton-port result excludes this topology
under S1 and both S2 families.  Thus the FB antecedent forces, for each color
pair, a proper shortest cycle whose two shores lie in one resource.

This is a new necessary reduction inside the common-star parent.  It does not
exclude the remaining internal-cycle defect and does not prove FB, CSQ4, a
normal form for arbitrary protected arrays, or the Krenn--Gu conjecture.  The
global conjecture remains **UNRESOLVED**.

The accepted artifacts were inspected at these SHA-256 values over
LF-normalized UTF-8 text bytes:

```text
owner:
b2e2b147d4afbb39701d655a91f2f71b3694283e3cd0f57ec6c6cf3a6eb44ce3

primary companion:
e323d1c9c569f54f3d24ad83b5b41d2b2c7518e2d5d28d3a10b1d5555fd7b0f9

independent audit:
8c820d05b21ec0e72f96eee4bb1f7e8aaaf87e33a0b49868ab540fa0413e3819

test module:
327be974d36f5d95bf9dcfc52a4b42c5863a9d7595d17d713aa426077ebd7b01
```

My proof inspection covered the complete owner, the source definitions and
no-singleton bridge in PSCS, and the parent-attempt statement and outcome.  I
read and ran the primary companion, independently wrote and ran
[`audit_common_star_binary_cycle_localization.py`](../../claims/arbitrary-order/audit_common_star_binary_cycle_localization.py),
and read and ran the six-test module.  I did not re-review every earlier PSCS
result or the unrelated exploratory searches recorded by the parent attempt.

## Cut factorization and resource membership

For a binary word with `a` on `S` and `b` on its complement, every compatible
common-star gadget goes from a selected left state to a selected right state.
The center and leaf matchings therefore use common row and column subsets and
give the exact source

```text
Z(S,S^c)=sum per(A[I,J]) per(B[I,J]).
```

Since `A` and `B` have the same support, their selected bipartite graph splits
over the connected components of the state graph.  Each physical component
selects one state, so no matching crosses between resources.  This proves the
product factorization used in the owner without treating a resource factor as
free cofactor data.

The physical-index/state distinction is handled correctly in the localization
proof.  If `T` is a subset of the cycle right shore `Y_R`, recoloring `T` adds
right states only to `R`.  A different resource can lose some left states when
the same physical components are recolored, but it gains no selected right
state and its exact factor remains one.  Consequently the full mixed target
really gives `Z(L_R\T,T)=0`; it does not assume that the physical indices in
`T` also have their left states in `R`.

## Deletion, subset induction, and localization

The row-deletion identity is exact.  When an added row has one supported
selected column, both permanents either omit the row or use that same entry.
The latter case extracts the actual product `q_xy` and leaves the two smaller
permanents.  Iteration is valid because the matching rows have distinct unique
columns.  A row with a second selected-column entry would invalidate the
identity; the primary companion explicitly rejects that mutation.

For a proper induced cycle, the only cycle rows that can meet a selected
column set `T` are the predecessors of its columns.  After already recolored
rows are removed, the surviving set is precisely the incoming cycle boundary

```text
P_T={pred(y): y in T and pred(y) notin T}.
```

This boundary is nonempty for every nonempty proper subset of a directed
cycle.  Substituting the smaller-column induction values in the deletion
formula makes every term share the same complete product of cycle `q` values.
The signs sum to `(1-1)^|P_T|`, leaving

```text
Z(U_R,T)=(-1)^|T| product_(y in T) q_(pred(y),y).
```

For the word changing all cycle components, the global source is the product
of `Z(U_R,Y_R)` over resources.  Empty `Y_R` contributes one, and every
nonempty proper `Y_R` contributes the nonzero value above.  Its required zero
therefore forces one resource to contain the full right shore.  The cycle
edges then put the full left shore in the same resource.  Applying the mixed
target once more at the complete cycle set gives `Z(U,C)=0`.

Boolean subset inversion of these `Z` values gives the owner's exact fixed-
column formula

```text
E_K = product_(y in K)(-1-q_y)                         (K proper in C),
E_C = product_(y in C)(-1-q_y)
      - (-1)^|C| product_(y in C)q_y.
```

The sign of the missing full-set term is correct.  This formula exposes the
top permanental defect rather than replacing it by a product of first moments.

## Shortest cycles and the PSCS bridge

Every full binary cut has an outgoing supported arc: otherwise its source is
the empty term one.  Hence the directed support is strongly connected.  A
shortest directed cycle is induced, because any additional arc between two of
its vertices closes with a directed subpath to make a shorter cycle.  Under
the disjoint-shore hypothesis the localization theorem forbids that cycle
from being proper, so it is Hamiltonian.  Any extra arc would again create a
shorter cycle, and singleton cuts then set the unique cycle products to `-1`.

Conversely, a directed Hamilton cycle with products `-1` has a disjoint-edge
compatible graph for every binary cut.  Every proper nonempty cut contains an
outgoing cycle edge, whose resource factor is `1+q=0`; both constant words
have source one.  This proves the stated equivalence, including sufficiency.

PSCS proves from S1 and the same-color and distinct-color S2 equations that
every ordered port has size at least two.  In the directed binary support this
is minimum outdegree and indegree at least two.  The exact Hamilton-cycle case
has singleton ports and is therefore unavailable to FB.  A shortest cycle is
then proper and the localization theorem applies.  This use of PSCS is a
downstream implication from the same physical array, not a new equivalence or
an assumption that all resources are complete bicliques.

## Exact controls and the all-length family

For the five-component control I reconstructed the field
`Q[s]/(3s^2+3s+1)`, with cycle product `q=-1-s` and six outside-to-cycle
products `w=s/2`.  The independent audit builds all 20 protected physical
vertices and recursively sums literal weighted perfect matchings.  A separate
component-minor evaluator agrees on all 32 binary words.  With the two outside
components fixed to zero, the eight cycle words have amplitudes
`delta_(000)`.  The resource sizes are `8,1,1`; the eight-state resource
contains both cycle shores and both outside left states.  The checker also
verifies all six proper nonempty deletion recurrences and every fixed-column
coefficient.  Changing either outside component alone gives amplitude one, so
the construction is not a full binary witness.

The written generalization to every `r>=3` is also correct.  Choose a
nontrivial `r`-th root of unity `rho`, set `s=1/(rho-1)` and `q=-1-s`, and
choose the `r-1` outside row weights as the roots, with multiplicity, of

```text
P(z)=sum_(m=0)^(r-1) (-1)^m s^m z^(r-1-m)/(m!)^2.
```

This monic polynomial has elementary symmetric functions
`e_m=s^m/(m!)^2`.  Its constant coefficient is nonzero, so every row weight
is nonzero.  For a fixed `m`-column set, each selected all-one center matrix
has permanent `m!`, and the row-constant leaf matrix has permanent `m!` times
the selected row-weight product.  Summing rows gives

```text
E_K=(m!)^2 e_m=s^m       for m<r,
E_C=0                    because only r-1 exterior rows exist.
```

Thus every proper exterior source is `(1+s)^|T|=(-q)^|T|`, while the full one
is

```text
(1+s)^r-s^r=(rho^r-1)s^r=0.
```

The same exact row deletion proves the complete `2^r` face.  An outside
singleton still has no incoming gadget and has amplitude one.  The support is
a legal simple one-label graph on `2r-1` components and `8r-4` physical
vertices.  For `r=3`, the polynomial has the repeated roots `s/2,s/2`, so it
recovers the independently reconstructed 20-vertex control.

The all-length statement is established by this written algebraic proof.  The
primary program checks the squared-factorial identity for a finite generic
instance and the root-of-unity identity for orders 3 through 9; it does not
enumerate or prove all orders computationally.

## Reproducible evidence and boundaries

The primary companion uses SymPy to check generic matching-row deletion, its
failure after adding a second supported column, the five-component control,
56 directed-cycle words at orders 3, 4 and 5, and the finite all-length
identity samples.  The independent audit imports only the Python standard
library.  It uses a different exact field implementation and a literal
physical matching recursion rather than importing the primary or any project
scientific helper.

The following commands passed in the inspected tree:

```text
python -X utf8 claims/arbitrary-order/verify_common_star_binary_cycle_localization.py
python -X utf8 claims/arbitrary-order/audit_common_star_binary_cycle_localization.py
python -m unittest -v tests.test_common_star_binary_cycle_localization
python -m ruff check claims/arbitrary-order/verify_common_star_binary_cycle_localization.py claims/arbitrary-order/audit_common_star_binary_cycle_localization.py tests/test_common_star_binary_cycle_localization.py
python -m py_compile claims/arbitrary-order/verify_common_star_binary_cycle_localization.py claims/arbitrary-order/audit_common_star_binary_cycle_localization.py tests/test_common_star_binary_cycle_localization.py
```

The unit-test run executed six tests.  The exact programs corroborate the
displayed finite controls and identities; the arbitrary-order localization
and all-length construction rest on the written proofs above.  No external
theorem is imported into either proof.  No Lean formalization or kernel check
is supplied, and this is separate-agent review in the same research session,
not separate-human refereeing.
