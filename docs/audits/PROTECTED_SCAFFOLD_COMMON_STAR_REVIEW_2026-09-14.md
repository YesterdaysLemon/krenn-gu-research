# Independent review: protected-scaffold common-star component obstruction

## Review conclusion

This record covers the initial owner snapshot pinned below. The later
at-most-two-port extension has its own
[independent review](PROTECTED_SCAFFOLD_COMMON_STAR_TWO_PORT_REVIEW_2026-09-14.md).
The historical hash and narrower scope in this record are preserved.

The source identity and the edge-local obstruction in
[`PROTECTED_SCAFFOLD_COMMON_STAR_COMPONENT_TARGET_OBSTRUCTION.md`](../../claims/arbitrary-order/PROTECTED_SCAFFOLD_COMMON_STAR_COMPONENT_TARGET_OBSTRUCTION.md)
are correct under their stated hypotheses over `C`.

The proof establishes two conditional statements for the literal common-star
construction with one ordered unequal-color gadget on each edge of a simple
component graph.  First, the component-constant targets force every gadget
edge to have a common-neighbor triangle.  Second, they force a specified
ordered endpoint port to repeat near every oriented gadget edge.  Hence both
a triangle-free component graph and a graph with at most one gadget in every
ordered port are excluded.  These are route no-go results for those
constructions.  They do not classify arbitrary hollow protected-scaffold
fillings, prove Q4, or resolve the global Krenn--Gu conjecture.  No Lean
formalization was reviewed.

The accepted owner and durable independent checker were reviewed at these
SHA-256 values over LF-normalized Git text bytes:

```text
owner:
af7ca8b9262505fb8ffe0385489a8349e270f9cd9b04ee708805392f4f75ec7c

independent checker:
630af3f7b48fa226453a1c8ec8e6f1813749c345afb69229e06b93868b720d38
```

I reconstructed the physical array and coefficient expansion independently.
The first finite checker proposed during review was rejected because it
repeated the reduced double-hafnian formula, never expanded the actual
physical scalar graph, and reported an unconditional pass.  It was not an
independent audit and supplies no evidence for this conclusion.  I did not
use it.  The durable independent checker reviewed here starts from all `4k`
physical vertices and recursively expands their scalar perfect matchings.  It
does not import the owner's current primary verifier or any project scientific
implementation.

## Independent derivation of the source

Fix a component-constant word `x`.  In a component of color `c`, the two
leaves other than the color-`c` leaf have one forced internal unit edge.  The
remaining center and color-`c` leaf are either matched to each other by their
protected internal edge or are both matched across component boundaries.

Let `S` be the components taking the latter option.  The centers in `S` have
an arbitrary perfect matching in the compatible center-weight graph `A_x[S]`.
Independently, the selected leaves in the same `S` have an arbitrary perfect
matching in `B_x[S]`.  This gives the actual physical coefficient

```
F(x) = sum_(S subset V, |S| even) haf(A_x[S]) haf(B_x[S]).
```

This retains both matching sums.  They cannot be replaced globally by a
single matching polynomial.  If the compatible graph is a forest, however,
each induced subgraph has at most one perfect matching: two distinct perfect
matchings would have an alternating cycle in their symmetric difference.
Thus the two matchings coincide whenever both exist, and only in this forest
case

```
F(x) = sum_(M matching) product_(e in M) q_e,
q_e = a_e b_e.
```

For an edge `uv` labeled `(d,e)`, let `c` be the third color.  In the word
with only `u` changed from `c` to `d`, the compatible graph is a star at `u`
and does not contain `uv`; the one-label hypothesis is used here.  Hence
`F_u=1+s_u`.  Similarly `F_v=1+s_v`.

For the word changing both endpoints to `(d,e)`, every exterior component
still has color `c`.  Hollow labels prohibit compatible edges between two
exterior components.  If `u` and `v` have no common neighbor, their two
exterior stars have disjoint leaf sets, so the compatible graph is a double
star plus its central edge `uv`.  It is a forest, and its matching polynomial
is exactly

```
F_uv = (1+s_u)(1+s_v) + q_uv.
```

Therefore `q_uv=F_uv-F_u F_v`.  All three words are mixed for `k>=2`, so the
component-constant target equations set all three coefficients to zero.  But
`q_uv` is nonzero because both gadget factors are assumed nonzero over `C`.
This proves that each gadget edge must lie in a triangle.  The separate empty
graph argument in the owner is also correct: every nonconstant component word
then has its protected internal matching as a unique unit contribution.

The Q4 interface is stated accurately.  The first two rows have four physical
minorities relative to the constant color `c`; the third has eight, but is
included among Q4's component-constant rows.  At `k=2`, the third word is also
four minorities from either endpoint color.

## Ordered-port extension

For distinct colors `a,b`, let the ordered port `(u,a,b)` contain incident
gadgets labeled `a` at `u` and `b` at their other endpoint.  The singleton
word with `u` colored `a` and all other components colored `b` has compatible
graph exactly this star, hence source

```
1 + sum_(f in port(u,a,b)) q_f.
```

The zero target forces every port to be nonempty.  If a port is unique, its
one product is therefore `-1`.

Now orient a gadget `uv` with label `(d,e)` and let `c` be the third color.
If the three ports `(u,d,e)`, `(u,d,c)`, and `(v,e,c)` are unique, their
gadgets are respectively `uv`, `uU`, and `vV`, all with product `-1`.
Simplicity and the one-label-per-pair condition give `U!=v` and `V!=u`.
In the component word `(d,e,c,...)`, these are exactly the compatible edges:
all exterior-exterior edges would require the forbidden equal label `(c,c)`,
and port uniqueness excludes additional incident edges at `u` or `v`.

If `U!=V`, the compatible graph is the path `U-u-v-V`.  Direct matching
enumeration gives

```
1 - 3 + 1 = -1.
```

If `U=V`, it is a triangle.  In the exact double-hafnian formula only the
empty subset and the three two-vertex subsets contribute, giving

```
1 - 3 = -2.
```

There is no omitted center/leaf cross-matching: the active triangle has an
odd vertex set, and adjoining any isolated exterior component makes both
hafnians zero.  Both values contradict the mixed target zero.  Thus at least
one of those three ports must repeat for every oriented gadget edge.  If every
ordered port has multiplicity at most one, missing ports already fail their
singleton equations; otherwise all ports are unique and the preceding
contradiction applies.  For `k=2`, this fails at the missing-port stage because
the single possible component neighbor cannot realize all six ordered ports.

## Independent exact controls

The portable program
[`audit_protected_scaffold_common_star_control.py`](../../claims/arbitrary-order/audit_protected_scaffold_common_star_control.py)
uses two independent evaluation routes:

1. direct recursion on the scalar graph of all `4k` physical vertices, with
   protected internal matrix-unit edges and literal center/leaf crossing
   entries; and
2. separate component-level enumeration of the double-hafnian subset formula
   and the ordinary matching polynomial.

It uses exact integer arithmetic and prints its result to standard output by
default.  Run it from any working directory with its absolute path, or from
the repository root with:

```
python -X utf8 claims/arbitrary-order/audit_protected_scaffold_common_star_control.py
```

An optional `--output PATH` writes LF-terminated JSON without relying on a
repository-relative output directory.

The controls were:

- **Forest:** on a weighted four-component path, all 81 component words were
  checked.  The physical recursion, double-hafnian formula, and ordinary
  matching polynomial agreed for every word.  On the fully active word their
  common value was `1043`.
- **Rejected global shortcut:** on the unit-weight four-cycle and its fully
  active alternating word, the physical recursion and double-hafnian formula
  both gave `9`, while the ordinary matching polynomial gave `7`.  The extra
  two terms are the cases where the center and leaf perfect matchings choose
  opposite perfect matchings of the cycle.  Across all 81 component words,
  physical and double-hafnian values always agreed; the ordinary matching
  polynomial failed on exactly this fully active word.
- **Triangle hypothesis:** take a triangle `u,v,w` with labels `(0,1)` on
  `uv`, `(0,2)` on `uw`, and `(1,2)` on `vw`, and products
  `(q_uv,q_uw,q_vw)=(1,-1,-1)`.  The two singleton sources and the
  both-changed source are all exactly zero.  The disjoint-star expression
  would instead leave `q_uv=1`; it incorrectly counts the product of the two
  spokes that collide at `w`.  This control validates the precise use of the
  no-common-neighbor hypothesis.  It is a local identity control and is not
  claimed to satisfy every component-constant target.
- **One-label hypothesis:** for `k=2`, place all six unequal ordered labels on
  the sole component pair, each with center weight `1` and leaf weight `-1`.
  Direct physical recursion gives `1` on `00,11,22` and `0` on all six mixed
  component words.  Thus all nine component-constant targets hold exactly.
  This is an actual countercontrol to any extension that permits multiple
  differently labeled gadgets on the same component pair.
- **Unique-port extension:** two literal local physical arrays set all three
  relevant gadget products to `-1`.  With distinct spoke endpoints, the three
  required singleton sources are zero and the double-changed source is `-1`.
  With a shared spoke endpoint, the same singleton sources are zero and the
  double-changed source is `-2`.  The checker separately confirms both values
  with the component double-hafnian formula and verifies that the displayed
  endpoint ports do not repeat.  These are local equation controls, not full
  target models with all other ordered ports supplied.

The durable checker compiled cleanly and passed `ruff check`.  These finite
tests validate the physical decoding and expose the two load-bearing graph
hypotheses; the analytic derivation above supplies the arbitrary-order proof.

## Scope boundary

The result allows repeated endpoint labels on distinct component edges and
arbitrary nonzero complex factor weights.  It does not cover multiple labels
on one component pair, zero gadget factors, crossing entries outside the two
common-star positions, or arbitrary hollow crossing blocks.  Triangle-
freeness can be weakened exactly to the local condition that the selected
edge's endpoints have no common neighbor when applying the first identity.
With triangles present, the second obstruction still applies unless one of
the specified ordered ports repeats.  The remaining common-star boundary
therefore has interacting triangles and repeated ports; the two conditions
are necessary and are not claimed sufficient.

The global conjecture remains **UNRESOLVED**.
