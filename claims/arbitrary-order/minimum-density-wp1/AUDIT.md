# Independent audit of the minimum-density `k=3` WP1 exclusion

Date: 2026-09-22

## Verdict and exact scope

**PASS.**  The all-`k=3` topology reduction, physical color/port
correspondence, componentwise Klein-four gauge quotient, analytic local gates,
and finite residual exclusion in
[K3 cover](K3_COVER.md) are sound.

Consequently, conditional on the already proved minimum-density equality
normal form, every protected `k=3` array with exactly `6k=18` supported
crossing scalar entries fails WP1.  The finite leaf is exhaustive for this
`k=3` equality case.  It does not treat `k>3`, prove general WP1, exclude
higher crossing density, or change the global Krenn--Gu status.

The finite conclusion is support-only.  Each residual configuration has a
mixed word of paired depth at most one with exactly one supported physical
perfect matching.  Its coefficient is therefore one nonzero monomial for
arbitrary nonzero gadget weights; the `+1,-1` weights in the primary replay
are not a specialization assumption in the exclusion.

## 1. Independent topology audit

At equality, the gadgets between each unordered pair of state colors give a
perfect matching of the three physical components.  Hollowness makes each
associated permutation `sigma_ab` a derangement.  Macro rigidity forces it
to be a single cycle: a proper invariant cycle union, colored `a` with its
complement colored `b`, is a mixed component-constant word selecting no
gadget and hence has forbidden protected coefficient one.

For `k=3`, every derangement is one of the two 3-cycles.  Relabel the physical
components so that `sigma_01` is the positive shift on `Z/3`.  The remaining
literal graphs are the four sign systems

```text
(+,+,+), (+,+,-), (+,-,+), (+,-,-).
```

Direct reconstruction gives a single 9-cycle in the first, second and fourth
systems, and three disjoint literal triangles in `(+,-,+)`.  In the triangle
case the component word `(0,2,1)` is an additional independent transversal,
so that case already violates a macro zero equation.

The three 9-cycle systems are physical scaffold isomorphs, not merely graph
isomorphs.  Besides a simultaneous component reflection, their color maps
are respectively

```text
identity, swap(1,2), cycle(0,1,2),
```

and the corresponding local port permutations are

```text
(0,1,2,3), (0,1,3,2), (0,2,3,1).
```

Applying these port permutations to

```text
M0={01,23}, M1={02,13}, M2={03,12}
```

induces exactly the displayed color maps.  Thus they preserve physical
matching multiplicities and merely permute the three `q_c`.  The topology
replay independently exhausts all four normalized sign systems and passes.

## 2. Gauge quotient and analytic pruning gates

The kernel of the action of `S4` on the three protected matchings is the
translation Klein four group.  Its action on the three pair indices is

```text
000, 011, 101, 110.
```

For each component there is a unique translation setting the first color-0
and first color-1 incidence to pair index zero.  The second color-1 incidence
is then one because that literal is split.  The second color-0 incidence and
the two color-2 incidences are free, leaving `2^3=8` representatives per
component.  Every one of the nine gadgets still has both endpoint
bijections.  Hence the quotient has exactly

```text
8^3 * 2^9 = 262144
```

configurations.  The action is free on the fixed incidences, so no orbit or
stabilizer correction is missing.

The analytic gates used before finite enumeration are necessary WP1
conditions:

1. In the fixed `C9`, a color-1 literal has neighbors in two distinct
   physical components, and those neighbors are not adjacent.  Reusing one
   protected pair would enable the nontriangle two-edge macro ladder with
   coefficient `f_3=-1`; hence every color-1 literal is split.
2. The neighbors of every color-0 or color-2 literal are in one common
   physical component.  If such a hidden transit literal is misaligned, its
   two unshared target ports have distinct root preimages and the accepted
   empty-q1 row has exactly one matching.  WP1 therefore forces alignment.
3. For two adjacent aligned hidden transit literals, the actual three-gadget
   lane maps have only the two intersection behaviors displayed in
   [two-hidden proof](TWO_HIDDEN_BLOCK.md).  In one case its explicit
   physical word has `q_1=1`; in the other it has `q_1=0`.  Endpoint colors
   disable both unused middle lanes and both end exits, so each word has one
   nonzero actual matching monomial.  Thus hidden transit literals form an
   independent set in this triangle-free literal graph.

An independent reconstruction finds 216 of the 512 pair allocations after
the adjacent-hidden gate.  Across their `2^9` endpoint maps, exactly 32,768
configurations satisfy every hidden alignment equation, agreeing with the
claimed residual.

## 3. Independent computational route

The primary-route producer
`generate_k3_receipt.py` imports the owning enumerator pinned by SHA-256

```text
5aff9e47d5d775f7fb446cc2cb610d6c62cd40dff041a4b1715607885d792b7c
```

and writes a reproducible JSONL receipt.  For every aligned isolated
configuration it records the two gauge-fixed bit fields, a SHA-256 digest of
the canonical 36-entry scalar support, and one primary-derived mixed
word/matching witness.  It produced exactly 32,768 rows.

`audit_k3_words.py` is a separate implementation and imports
neither the producer nor the owning enumerator.  It:

* hard-codes only the published `C9` literal edges and protected K4 matchings;
* reconstructs the gauge allocation and endpoint bijections directly from
  the two bit fields;
* independently exhausts all 262,144 gauge configurations and obtains the
  exact 32,768 isolated/aligned configuration set;
* rebuilds all 36 scalar entries and compares the canonical support digest;
* recomputes the physical paired-depth vector from the supplied 12-color
  word;
* checks that the supplied six edges form a compatible physical perfect
  matching; and
* counts every compatible matching for that fixed word by a vertex-mask,
  word-first adjacency recursion.

Every receipt word is mixed, has `min_c q_c<=1`, and has matching count
exactly one.  The checker also proves that the receipt configuration set is
equal to, rather than merely contained in, its independently reconstructed
residual.  This differs from the primary route in decoding, enumeration
direction and matching representation; it is not a renamed invocation of the
same helper functions.



## Promotion and exact evidence boundary

The original separate-agent audit report was frozen at SHA-256
BDBE8C274F015DBDFBF74809959222D0D8782E7F25DAE8D36566F7D6507D5D21.
Its original receipt SHA-256 was
3f11e93124ed3cb1435ed99231208085b7f54a4cf61165f91696b187ce0bdf19.
Promotion changes sibling file paths, portable optional output/input
handling, and compression. The k3 checker additionally rejects a supplied
word unless it has exactly twelve integer colors in {0,1,2}; this closes
malformed-input ambiguity without changing acceptance of any pinned row.
The two-hidden replay received formatting-only cleanup, and the k2 producer
now creates its output directory for clean-checkout regeneration.
The primary source hash uses canonical UTF-8/LF
bytes, which equal the original audited source bytes. Every witness row and
the metadata line are byte-identical to the original audited receipt.
The promoted raw receipt SHA-256 is
3f11e93124ed3cb1435ed99231208085b7f54a4cf61165f91696b187ce0bdf19.

The k2 C# generator and Python graph-recursion checker likewise differ in
representation and enumeration direction. Its full 262,144-row table was
independently regenerated byte-for-byte and every row independently checked.
The handwritten bridge from macro equality to the finite parameterization
is in K2_COVER.md, rather than being inferred from generator output.

This is same-session separate-agent computational and analytic review,
not human refereeing or Lean formalization. All finite conclusions preserve
their exact order, density, scaffold and low-q scope.

## Final promotion review

A final separate-agent promotion review compared this assembled package with
the three owning scratch reports and their audited certificate data.  It
confirmed the PSMD equality-to-gadget bridge, the complete `k=2` parameter
cover, the `k=3` topology/gauge/local-gate reduction, and the exact residual
certificate correspondence.  The promoted k2 table is byte-identical to its
audited original, and decompressing the promoted k3 certificate gives the
byte-identical audited JSONL receipt.

The review passes after the documented clean-checkout k2 output-directory
repair and strict k3 physical-word validation.  The manifest covers only the
15 intended source, proof, and certificate files; generated bytecode and
build outputs are excluded.  This promotion adds no higher-order,
higher-density, arbitrary-witness, formalization, or global-resolution claim.
