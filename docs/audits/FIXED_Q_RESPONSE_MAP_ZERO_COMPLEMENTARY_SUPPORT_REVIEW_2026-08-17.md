# Fixed-Q response-map-zero complementary support hostile review -- 2026-08-17

## Verdict

**Accepted at the frozen theorem and script hashes below.**  No P0 or P1
defect remains.  The package proves an exact characteristic-zero
response-map-zero support classification, a fixed five-row detector per
complementary partition, and a physical opposite-annihilation refinement.
It does not prove that a hypothetical witness has zero realized response
maps, construct a legal selector, exclude the resulting sparse-support
locus, integrate a response control into a witness, or imply a permanent
restriction.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Response-map-zero bridge

For arbitrary residual scalar `h`, the physical response layers are

```text
M_e=B_e,                 Z_e=hB_e+K_e,
M_U=C(B),                Z_U=hC(B)+X(B,K).
```

Literal vanishing of the full mixed-response map `R_e` makes both pair
columns pure and therefore separates `B_e` and `K_e` as diagonal blocks.
Likewise `R_U=0` separates the pure tensors `C(B)` and `X(B,K)`.  This is
strictly stronger than purity of one selected operator line.  The theorem
uses the term response-map-zero for this hypothesis and reserves
response-invisible line for the rank-one module situation defined in
`GLD18`.

For a complementary partition `e|f` and ordered colours `c!=d`, pair
diagonality makes the other two matchings vanish on the word `cc|dd`.  The
two actual response coefficients are exactly

```text
b_e^c b_f^d,
h b_e^c b_f^d+b_e^c k_f^d+k_e^c b_f^d.
```

No cancellation term or matching is omitted.

## Exhaustive support classification and detector

The twelve ordered rows have three disjoint and exhaustive alternatives:
both direct blocks are nonzero and all four raw supports lie in one common
colour; exactly one direct block is nonzero and constrains the opposite
channel support according to whether its support has size one or at least
two; or both direct blocks vanish and only the diagonal physical rank bound
remains.  Each converse was checked directly.

For arbitrary projective pair rows, including pure coordinate axes, the
classification forces

```text
prod_(c=0)^2 D_e(c,c)D_f(c,c)=0
```

on every complementary partition.  These are three separate equations, so
the locus is the intersection of the three support divisors, not the weaker
union defined by their product.

A fixed cycle of the three colours reduces detection to five scalar rows per
partition: three `M_U` rows and two `Z_U` rows.  The missing-colour proof
exhausts the omitted third `Z_U` case using the physical rank bound on the
opposite edge.  Fifteen fixed scalar coefficients therefore cover the three
partitions.  No minimality below five rows is claimed.

## Physical opposite annihilation

On the full response-map-zero locus, one three-full selected edge first
forces the opposite direct block to vanish and confines its channel block to
the missing colour.  The other two active colours give a basis of the
two-dimensional physical shore at one endpoint.  Diagonality of the cross
edges makes the opposite colour vector orthogonal to that basis under the
nondegenerate physical bilinear form, so it vanishes at both opposite
endpoints.  Hence the opposite channel block also vanishes.  Three-full
selected edges consequently form an intersecting family in `K_4`, of size at
most three and star or triangle type at equality.

The proof uses the common physical shore factorization and is not inferred
from edgewise rank alone.  Its arbitrary-field argument remains a
load-bearing written proof.

## Controls and independent checks

Exact controls separately preserve pure four-port normalization and
three-colour activity on the support divisor, attain the opposite-annihilation
conclusion, and show that pair-map zero, residual-present four-port purity,
the physical rank bound, and literal map zero are load-bearing.  They are
physical response windows or formal module controls, not hypothetical
witnesses or counterexamples.

The primary replay uses SymPy tensor enumeration and checks all
`8^2*7^2=3136` diagonal support configurations, of which `201` satisfy the
twelve-row equations.  The independent audit imports neither SymPy nor the
primary; it uses standard-library `Fraction`, recursive matching generation,
support masks, sparse tensors, and raw endpoint vectors.  Both focused
scripts pass, as do Ruff check and format-check.  The scripts replay the
bounded formulas, finite support ledger, five-row detector, divisor, attaining
fixture, and sharp controls.  The full response-map implication, general
support proof, shore-level opposite-annihilation argument, and conditional
witness interpretation remain load-bearing.

Frozen at base HEAD `f4a878e1234f92bcf773f6450f75492801dd5bc2`:

```text
theorem  099c88f378db54b2f998e082d02ea8c76c4fbce34ca53e035d464e0a6d0b1552
primary  03b839d92cb4ee2329178f9c80af4c1d0794c798491850bb3627ecd8008badef
audit    5293339335eaed1fb0f1f8725a9c4f72334ccc3b5f5bd1adb7363591b4c16302
```

## Exact remainder

Still **UNKNOWN**: forcing `R_S=0` on any or every hypothetical witness;
forcing nonzero legal operator rows on that stratum; excluding the
intersecting sparse-support locus; synchronizing or integrating the surviving
responses across windows; and every weighted-permanent consequence.
