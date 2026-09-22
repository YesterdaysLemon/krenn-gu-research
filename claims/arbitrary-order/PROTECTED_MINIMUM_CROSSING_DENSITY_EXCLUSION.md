# Protected full sources exceed the minimum crossing density

Date: 2026-09-22.

Status: proved all-order theorem over C, with completed independent review
of the assembled argument. The global Krenn--Gu conjecture remains
**UNRESOLVED**. No Lean formalization or arbitrary-witness scaffold reduction
is supplied.

## 1. Parent, scope, and result

Take k>=2 protected unit K4 components, with

```text
M_0={01,23}, M_1={02,13}, M_2={03,12}.
```

Allow arbitrary complex hollow intercomponent scalar entries: a supported
crossing joins different components and has different endpoint colors. The
protected intracomponent entries are fixed; there are no other internal
entries. A supported scalar entry means a nonzero colored entry, counted
once without physical orientation. Distinct color labels on the same
physical edge count separately. Let m be the number of supported crossings.
The physical source coefficient T_W(w) is the sum of matching monomials
compatible with the complete physical color word w.

A macro word is constant on each K4. The macro targets are one on each of
the three globally constant words and zero on all mixed macro words. The
full-source targets impose the same GHZ rule on every physical word.
For a background color c, q_c(w) counts protected M_c pairs whose two
endpoints both have colors different from c. Write WP2 for all macro targets
and all mixed physical zero targets with min_c q_c<=2. WP1 uses the cutoff
one instead; it is a strictly smaller asserted antecedent here.

**Theorem (PSMD).** The macro equations imply m>=6k. If m=6k and WP2 holds,
the support is a complete protected-edge pairing as defined in
[PSCG](PROTECTED_PAIR_GADGET_CUBIC_MATCHING_EXCLUSION.md), and the two crossing
weights of each gadget multiply to -1. Consequently every full protected
source must have **m>6k**.

The last implication uses PSCG's all-order cubic matching exclusion. That
theorem gives a mixed unique-matching word without a paired-depth bound.
Therefore the present theorem does not assert that WP2, or WP1, is excluded
at m=6k. It proves a normal form from WP2 and excludes the full source there.

The starting parent asked whether WP1 already forces m>6k. The successful
full-source route instead uses a mixed word of minimum paired depth exactly
two to remove an overlapping allocation, then uses the unrestricted mixed
word supplied by PSCG. The WP1 parent remains open in general. This is a new
full-source implication, not a change to the meaning of WP1.

## 2. Singleton macros force the lower bound and equality form

Fix a component A, a color a there, and a different background color c
everywhere else. The protected term of this singleton macro word is one.
Its zero target therefore needs a nonprotected matching. Hollowness forbids
crossings between exterior color-c components. Every nonprotected matching
crosses the four-vertex cut of A a positive even number of times, hence uses
at least two supported entries of type (A,a | exterior,c).

Let d(A,a|c) count those entries. There are 6k such incidences, each at least
two. A crossing with endpoint literals (A,a),(B,c) is counted exactly twice:
in d(A,a|c) and d(B,c|a). Thus

```text
2m = sum_(A,a,c:a!=c) d(A,a|c) >= 12k.               (1)
```

At equality every incidence has exactly two entries. Any nonprotected
singleton matching must use both. Their endpoints in A must be distinct,
and their complement must be an M_a edge, so they themselves form the other
M_a edge. Both exterior endpoints must lie in one component B: otherwise
two exterior components have odd unmatched vertex counts. They are distinct
and form one M_c(B) edge by the same complement argument. Thus the two
entries give a bijection between protected edges in different components
and colors. The singleton word has exactly the protected term and this
two-crossing term, so their weights x,y obey

```text
1+xy=0.                                             (2)
```

The reverse incidence at (B,c) is exhausted by the same two entries.
Consequently all crossings partition into exactly 3k such pair gadgets.
At each literal (A,a), the gadget toward each of the other two colors uses
one of its two M_a edges. Call the literal **split** if the two resource
edges are complementary, and **transit** if they coincide. No resource
allocation is assumed in advance.

## 3. Macro rigidity eliminates literal triangles

Let F have the 3k literals (A,a) as vertices and one edge for each pair
gadget. Every literal has one neighbor of each other color; no edge joins
two literals of one physical component. Hence F is a simple 2-regular
graph, with each color-pair edge set a bijection of the components.

For a<b, write sigma_ab(A)=B for the edge (A,a)--(B,b). Each sigma_ab is a
permutation. If a macro word selects an independent transversal of F, no
crossing is compatible and its coefficient is one. Therefore the macro
targets force the only independent transversals to be the three constants.
This necessity does not use any proposed converse or weighted factorization.

Each sigma_ab must be a single k-cycle. Otherwise color a on a nonempty
proper union of its cycles and color b on the remaining components. This
is a mixed independent transversal, a contradiction.

Suppose F contains a triangle (A,0)--(B,1)--(C,2)--(A,0). Put
p=sigma_01, q=sigma_02, r=sigma_12. Then B=p(A) and C=q(A)=r(B); A,B,C are
distinct. Follow the p-cycle A,B,...,C,...,A and assign component colors

```text
0 on B,...,p^-1(C);
2 at C;
1 on p(C),...,A.                                    (3)
```

Both arcs are nonempty. The p-cycle has no selected 0->1 edge. The only
2-colored component is C; its unique q-preimage is A, colored 1, and its
unique r-preimage is B, colored 0. Thus no 02 or 12 edge is selected either.
Word (3) is a mixed independent transversal. This contradiction proves that
**F has no triangles**, at every k.

## 4. The two-exception macro localizes every overlap

Let u=(A,a) be transit, with neighbors v=(B,b), w=(C,c), where a,b,c are
the three different colors. Suppose B!=C. Color B by b, C by c, and all
other components by a. The two gadgets v--u and u--w are enabled. The only
other possible enabled gadget is v--w: the background-a incidence at each
exception is already exhausted by its gadget to u, and crossings between
background components are hollow. But v--w would make an F triangle, already
excluded by Section 3.

The source is therefore a two-gadget open ladder, with the two gadgets
reusing the same protected M_a(A) pair. Its matchings use neither gadget
or both lanes of exactly one gadget. A one-lane term cannot close at an
outer resource, and using both gadgets would reuse a physical vertex.
The exact coefficient is 1+(-1)+(-1)=-1, contradicting the mixed macro
target. Hence B=C.

Every transit literal is therefore **hidden**: its two neighbors are
(B,b),(B,c) in one other physical component. They need not be split for
the next argument.

## 5. A hidden overlap fails a one-pair or two-pair physical word

Let the reused M_a(A) pair be {s,p}. The two foreign resource pairs are
R_b(B)={u,q} and R_c(B)={u,l}; their common port is u. Write v for the fourth
port of B. The two unshared ports q,l form an M_a(B) edge, and {u,v} is its
complement. There are two relative orientations of the gadget bijections.

If the crossing lanes from q of color b and l of color c land at distinct
A ports, give q color b, l color c, and every other vertex color a. The two
displayed lanes, the complementary M_a edges in A and B, and the protected
matchings outside form the sole matching. Other lanes have a wrong endpoint
color; the unused exits at the foreign literals expect b or c outside B,
where only a occurs. This mixed word has q_a=1 and a nonzero coefficient.
Thus WP1, and hence WP2, forbids that orientation.

In the remaining orientation those two unshared lanes hit the same A port.
Consequently the shared foreign port u hits the other A port in both
gadgets. Rename s,p so that the actual lanes and their nonzero weights are

```text
g: s--u with x,    p--q with -1/x,     labels (a,b);
h: s--u with z,    p--l with -1/z,     labels (a,c).  (4)
```

The repeated physical endpoints s,u carry different scalar color labels.
Now give every vertex outside B color a, give u color b, and the other
three B vertices color c. There is exactly one matching:

```text
s--u from g; p--l from h;
the complementary M_a edge in A;
the complementary M_c edge {q,v} in B;
the protected color-a matchings in every exterior component.            (5)
```

Its coefficient is -x/z, nonzero. The other g lane has the wrong B color,
and the other h lane does too. The literal (A,a) has no further gadget.
The other gadget at (B,b) expects exterior color c and the other at (B,c)
expects exterior color b; both are absent everywhere outside B. No further
selected non-a literal exists, and all exterior a-to-a crossings vanish by
hollowness. Thus (5) is unique in the **full array**, whatever the unused
exterior gadgets and their weights are.

After normalizing (a,b,c)=(0,1,2), this word is
0000|1222|0000|... and its exact paired-depth vector is

```text
(q_0,q_1,q_2)=(2,2k-1,2k-2).                         (6)
```

It is mixed with minimum paired depth exactly two. WP2 forbids it; WP1 does
not include its equation. These two orientation cases exclude every transit
literal from an equality-case WP2 array.

## 6. Complete pairing and the full-source contradiction

All literals are now split. Thus every one of the 6k protected colored
edges is used exactly once in the 3k pair gadgets. Each gadget joins
different colors and physical components by a bijection, with nonzero
lane product -1. This is precisely the complete protected-edge pairing
of PSCG, with no bipartition or uniform port-table assumption.

The full source supplies WP2. By PSCG it also cannot occur on a complete
pairing: the associated simple triangle-free properly 3-edge-colored cubic
graph has an additional perfect matching, giving a mixed physical word with
one nonzero matching monomial. Hence a full source cannot have m=6k.
Together with (1), it must have m>6k.

PSCG imports the connected matching-covered three-perfect-matchings
classification from Kothari--Lee--Lucchesi--da Silva,
[*Cubic graphs, S-minors and conformal minors*, Theorem 2.4](https://arxiv.org/html/2606.04173v1#S2.SS1).
Its exact hypotheses and provenance are recorded in PSCG and in the
literature registry. This document introduces no new external premise.

## 7. Evidence and boundaries

The all-order proof is Sections 2--6; finite scripts replay local identities
and explicit witnesses rather than replacing any unbounded quantifier.

- `verify_protected_minimum_crossing_normal_form.py` exhausts the 496
  two-entry singleton supports on three K4s, including shared-endpoint and
  split-exterior failures, and identifies exactly the 16 pair bijections.
- `verify_protected_literal_triangle_witness.py` replays the explicit arc
  witness through k=6 on 72,246 normalized permutation pairs and 11,618
  triangles. The written arc argument supplies the all-order scope.
- `audit_protected_hidden_crossing_words.py` reconstructs complete literal
  arrays and checks the unique one-pair/two-pair words with literal matching
  recursion, including nontrivial exterior gadgets.
- The imported PSCG theorem has its own proof, independent audit and three
  portable exact replays.

No all-order result is inferred from an empty finite search. The local
single-monomial contradictions are valid for every nonzero permitted weight;
the displayed product normalization comes from actual singleton equations.

The [independent audit](../../docs/audits/PROTECTED_MINIMUM_CROSSING_DENSITY_REVIEW_2026-09-22.md)
checks the complete chain and records the separate computational evidence.
For a compact model-review handoff, use the
[review brief](../../docs/strategy/minimum-crossing-density-review-2026-09-22.md).

The theorem closes the minimum-density branch of the full protected-source
parent. It does not reduce a denser protected array to equality, exclude
WP1 at arbitrary order, or reduce an arbitrary Krenn--Gu witness to the
protected scaffold. The live global status remains UNRESOLVED.
