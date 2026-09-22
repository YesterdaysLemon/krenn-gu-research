# Exhaustive k=2 minimum-density support cover

Date: 2026-09-22

Status: **exact exhaustive finite cover, independently replayed.**  Every one
of the `4^6 * 2^6 = 262,144` literal supports in the supplied `k=2`
minimum-density normal form has a mixed physical word with
`min_c q_c<=1` and exactly one supported scalar perfect-matching term.
Consequently no choice of nonzero complex weights on one of these supports
can satisfy the WP1 low-q zero equations.

This closes the finite child, conditional on the upstream structural
reduction to the normal form below.  It does not establish that reduction,
resolve other density branches, prove WP1 in general, or resolve the global
Krenn--Gu conjecture.

## 1. Exact finite obligation

There are two protected K4 components, called side 0 and side 1, with local
ports `0,1,2,3` and protected color matchings

```text
M_0={01,23}, M_1={02,13}, M_2={03,12}.
```

For every ordered unequal color pair `(a,b)` there is one two-entry gadget.
It allocates one edge of `M_a` on side 0 and one edge of `M_b` on side 1,
then uses one of the two endpoint bijections.  There are no other crossings.

At a fixed `(side,color)` node, its two incident foreign labels independently
choose one of the two protected edges.  In increasing foreign-color order,
the ordered allocation is one of

```text
00, 01, 10, 11.
```

Thus the six `(side,color)` nodes supply `4^6` literal choices.  The six
ordered-color gadgets each supply one bijection bit, giving `2^6` more.
No symmetry quotient is used:

```text
4^6 * 2^6 = 262,144.                                (1)
```

The parameter index is

```text
index = 64 * allocation_code + orientation_code,
```

where `allocation_code` has six base-4 digits in node order

```text
(side0,color0),(side0,color1),(side0,color2),
(side1,color0),(side1,color1),(side1,color2),
```

and the six orientation bits use lexicographic ordered labels

```text
01,02,10,12,20,21.
```

This parameterization allows both coincident allocations (`00,11`) and
complementary allocations (`01,10`).

## 2. Claim checked

For a physical word `w in {0,1,2}^8`, let

```text
q_c(w)=#{e in M_c on either K4:
         both endpoints of e have word color different from c}.
```

For each support in (1), the cover supplies a word `w` such that:

1. `w` is mixed;
2. `min_c q_c(w)<=1`; and
3. the word-specific scalar graph has exactly one perfect matching.

At a fixed word, a physical pair supports at most one scalar entry with its
ordered endpoint colors.  Protected pairs have one color, and each ordered
crossing color `(a,b)` has only its one gadget.  Therefore the graph perfect
matching count is exactly the scalar-term support count, even when different
gadgets reuse one protected edge or physical pair at other endpoint colors.

The unique term is a product of supported nonzero entries and hence is
nonzero for arbitrary nonzero complex weights.  No cancellation or generic
specialization argument is involved.

## 3. Primary exhaustive generator

The primary generator is:

```text
K2Generator/Program.cs
```

For every literal parameter point it:

1. reconstructs all protected and crossing scalar entries as endpoint-color
   masks on the 28 unordered physical pairs;
2. generates all 105 unlabeled perfect matchings of eight vertices;
3. enumerates their compatible scalar entries and counts every word,
   saturating counts at two; and
4. chooses the first base-3 word that is mixed, has `min q<=1`, and has
   count one.

It writes one little-endian `uint16` word code per support.  The binary
certificate format is:

```text
bytes 0..3:   ASCII K2W1
bytes 4..7:   little-endian uint32 row count = 262144
remaining:    262144 little-endian uint16 base-3 word codes
```

The generator inspected `14,315,520` literal supported scalar terms across
the full cover and returned:

```text
K2_MINIMUM_DENSITY_COVER_PASS supports=262144
```

It completed in `0.798` seconds inside the 180-second, 8192 MiB bounded run
`k2-minimum-density-generate-20260922`.

## 4. Independent replay

The independent checker is:

```text
verify_k2.py
```

It does not repeat the generator's scalar-term traversal over the 105
complete-graph matchings.  For each certificate row it independently:

1. decodes the six base-4 allocation digits and six orientation bits;
2. reconstructs only the supplied word's physical adjacency graph;
3. checks mixedness and `min q<=1`; and
4. recursively counts perfect matchings of that graph, choosing an unmatched
   vertex and branching over its available neighbors, with the count capped
   at two.

All rows passed:

```text
verified=65536
verified=131072
verified=196608
verified=262144
INDEPENDENT_K2_COVER_PASS supports=262144
```

The final replay completed in `3.447` seconds inside the 180-second, 8192 MiB
bounded run `k2-minimum-density-verify-final-20260922`.

## 5. Certificate identity and mathematical bridge

The durable binary witness table has 524,296 bytes and SHA-256
10B9BC58DB753FDC4DCB8DC16CC86A7D919C481C3B1ED21AA14B1F10B8B6056A.
It contains 439 distinct witness words: 46,787 supports use a selected
word with min q=0 and 215,357 use min q=1. These frequencies are descriptive;
all 262,144 rows are checked individually.

The singleton-macro equality proof in
[PSMD](../PROTECTED_MINIMUM_CROSSING_DENSITY_EXCLUSION.md) gives exactly
3k two-entry gadgets at m=6k, with one incidence toward each foreign color
at every component/color literal. At k=2, hollowness forces the other
component to be the target, leaving precisely the six ordered-color
gadgets and independent pair allocations parameterized above. Thus every
k=2 equality support satisfying the macros is in the checked cover.
The unique low-q word rules it out for arbitrary nonzero complex weights.
Consequently k=2 WP1 requires m>12.

The manifest pins promoted source files and exact certificate data. The
generator and checker use different representations and enumeration
directions. No claim beyond the stated k=2 finite cover follows.
