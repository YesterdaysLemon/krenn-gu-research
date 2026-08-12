# Hostile review: diagonal aggregate shore product and primitive exchange

Date: 2026-08-11

Reviewed artifact:

[`Matrix-unit diagonal aggregate shore-product and primitive-exchange
sharpness theorem`](../../claims/arbitrary-order/MATRIX_UNIT_DIAGONAL_AGGREGATE_SHORE_PRODUCT_AND_PRIMITIVE_EXCHANGE_SHARPNESS_THEOREM.md)

Review disposition: **PASS at the stated diagonal-only structural-reduction
and fixed-family sharpness scope**.

The Krenn--Gu conjecture remains **UNRESOLVED**.

This is a durable hostile self-review of the written proof and evidence
package.  The two scripts are implementation-independent at their stated
mechanism scope; they are not claimed to be independent authors.

## 1. Exact obligation under review

`U7J` gives the aggregate-cycle identity

```text
H=(-1)^m product_i(1+A_i),
```

and `U7K` treats every extra matching with a nonempty offdiagonal core.
`U7K` explicitly leaves an extra with empty offdiagonal core outside its
bridge decision tree.

The reviewed checkpoint claims:

1. all diagonal matchings at one word form the Cartesian product of the three
   pure-shore matching sets;
2. their difference lattice is the exact direct sum of the three shore
   lattices;
3. any aggregate diagonal fibre contains a second term differing from the
   selected incoming matching on one primitive alternating even cycle;
4. a cycle with diagonal-only excess has an exact shore-product target
   equation and holonomy formula;
5. shortest-cycle minimality, bridge/deeper transport, and full-shore
   pure-cofactor cancellation do not add a conclusion to the diagonal extra;
   and
6. a complete twelve-vertex family makes that boundary sharp while
   satisfying all three pure target equations.

The theorem does not claim universal unit forcing, useful non-direct overlap,
proper-subshore cancellation, a deeper-blocker exclusion, an `r=1`
exclusion, or a global resolution.

## 2. Adversarial proof checks

### 2.1 Is “diagonal” being confused with a diagonal physical pair?

No.  Diagonal refers to the two endpoint labels of the matrix unit carried
by a physical edge.  If a compatible edge has labels `c,c`, compatibility
places both physical endpoints in `V_c={v:chi(v)=c}`.  Conversely every
pure-`c` edge inside `V_c` is compatible with `chi`.

Thus a diagonal full matching splits uniquely by colour shore.  No statement
about the numerical vertex indices or an adjacency-matrix diagonal is used.

### 2.2 Is the Cartesian product exact, including the empty shore?

Yes.  The three shores partition the vertex set and have even size.  A
diagonal full matching restricts to one perfect matching on each shore, and
the union of any such triple is a full compatible matching.  The empty shore
contributes its unique empty matching of weight one.

There is neither omission nor multiplicity: restriction and disjoint union
are inverse maps.

### 2.3 Why are all shore hafnians nonzero?

At an active word the imported synchronization theorem gives a nonzero
offdiagonal aggregate `Q_chi`.  The complete mixed target coefficient is
zero, so

```text
D_chi=-Q_chi!=0.
```

The diagonal factorization is `D_chi=product_c h_c(V_c)` over a field.
Therefore every factor is nonzero.  This is a pointwise statement at the
hypothetical witness, not a claim that the shore polynomials are units.

### 2.4 Does normalization divide by an aggregate sum?

No.  Each shore polynomial is normalized only by the monomial of the
selected incoming shore matching.  The full target equation is divided only
by the selected incoming full matching monomial.  Those monomials are
nonzero in the complete nonzero torus.

The inverse shore factors in the displayed holonomy formula are inverses of
their nonzero scalar values at the witness.  The proof explicitly does not
invert them as group-algebra elements.

### 2.5 Is the shore-lattice sum genuinely direct?

Yes.  A difference from shore `c` is supported on edge coordinates with
both endpoints in `V_c`.  The coordinate sets for different shores are
pairwise disjoint.  If a sum of three shore vectors is zero, restriction to
each coordinate set makes every summand zero.

This proves only the internal diagonal decomposition.  It does not assume or
conclude directness against target lattices from other words.

### 2.6 Does an aggregate fibre really force a primitive cycle?

Yes, as a support difference.  If a second diagonal matching exists, one
shore matching `M` differs from the selected shore matching `P`.  Their
symmetric difference is a disjoint union of alternating even cycles.
Flipping only one component and retaining `P` elsewhere gives another
support perfect matching.  Extending by the fixed other shores gives a term
in the same diagonal fibre.

The resulting incidence vector has alternating coefficients `+1,-1` on one
cycle, so its coordinate gcd is one.  It is primitive in the ambient integer
edge lattice.

### 2.7 Is that primitive vector silently promoted to a binomial relation?

No.  This is the central hostile boundary.  Both matching monomials occur in
the complete aggregate equation, but their two-term difference or sum is
not known to vanish.  The shore hafnian is nonzero.  The theorem calls the
object a primitive exchange or direction, not a primitive zero relation.

An odd signed dependency concerns the integer kernel of actual binomial
generators.  A primitive support direction alone supplies no such kernel
element.

### 2.8 Is the diagonal-only cycle normal form missing offdiagonal terms?

No, because the hypothesis says every term other than the selected incoming
`G_(i-1)` and outgoing `F_i` is diagonal.  Therefore the complete
offdiagonal coefficient is the singleton `lambda(F_i)` and the complete
diagonal coefficient is the Cartesian shore product.  Their sum is the whole
fibre coefficient.

If a second offdiagonal matching existed, this theorem would not apply; that
term belongs to the `U7K` decision tree.

### 2.9 Is the holonomy indexing correct?

Yes.  At `chi_i`,

```text
lambda(G_(i-1))/lambda(F_i)
  =-product_c S_(i,c)^(-1).
```

Multiplication over `i` cyclically reindexes the incoming `G_(i-1)` factors
to the imported numerator `product_i lambda(G_i)`.  This gives exactly
`H=(-1)^m product_(i,c)S_(i,c)^(-1)`.

### 2.10 Can shortest-cycle minimality act on the primitive exchange?

No.  The `U7K` shortest-cycle argument starts from a new active **arc**
obtained by bridge-normalizing a nonempty offdiagonal core.  A diagonal extra
has empty offdiagonal core, stays at the same word, and has no bridge square
or hexagon.  It creates no arc.

Shortestness can constrain the already selected outgoing bridge, but it
cannot turn the diagonal exchange into an outside word or parallel successor
without an additional construction.

### 2.11 Does the full shore enter the pure-cofactor machinery?

No.  Its hafnian is nonzero by Section 2.3.  The least-residual theorems start
from a supported zero hafnian.

A proper even subset of the shore could cancel in another support.  The
general theorem neither excludes nor forces that event.  In the sharpness
family, both checkers verify that every supported even subshore of the two
nonempty active shores has nonzero exact hafnian.

### 2.12 Does absence of an offdiagonal core prove absence of deeper blockers?

Only for the extra's bridge route.  The imported bridge/deeper alternative
selects squares or a hexagon from a nonempty cross core.  There is none for a
diagonal extra.  The theorem does not claim the global geometric
deeper-blocker component is empty; that independent branch remains open.

## 3. Adversarial checks on the sharpness family

### 3.1 Is the twelve-vertex table complete and locally concise?

Yes.  Equations (18)--(21) assign one nonzero matrix unit to each of the
`66=binomial(12,2)` physical pairs.  Both checkers reconstruct that exact
edge set and verify that the endpoint labels at every vertex are precisely
`{0,1,2}`.

The only excluded parameter divisors are `t=0` and `1+t=0`, which keep the
extra edge `28` and selected edge `24` nonzero.  The unrelated edge `1,11`
has fixed weight two.

### 3.2 Are the displayed `3/2/2` fibres complete?

Yes.  The primary checker enumerates all `11!!=10395` perfect matchings as
edge tuples.  The no-import audit enumerates the same physical matching set
as 66-bit masks, pairing the highest remaining vertex.  Both group by the
full twelve-entry word and recover exactly:

```text
chi_0: one outgoing offdiagonal term and two diagonal terms;
chi_1: one incoming diagonal term and one outgoing offdiagonal term;
chi_2: one outgoing offdiagonal term and one incoming diagonal term.
```

Their weights are `(-(1+t),t,1)`, `(1,-1)`, and `(-1,1)`.

### 3.3 Is the extra really diagonal and the only extra?

Yes.  At `chi_0` the matching

```text
01|28|39|46|57|10,11
```

uses only equal-label edges and is diagonal.  The other nonselected term is
the designated incoming matching.  The two other cycle fibres are
binomial.  Hence every extra cycle matching is diagonal, with exactly one
such extra in the family.

### 3.4 Is the cycle actually shortest, not merely displayed?

Yes at the stated `Q(t)` point.  Both exact ledgers compute the total and
offdiagonal polynomial of every nonempty word.  Exactly the three displayed
words have total coefficient zero and nonzero offdiagonal coefficient.

Each has one offdiagonal matching, and its square bridge is the displayed
successor.  The active transport graph is therefore exactly one directed
three-cycle.  It has no two-cycle or outside active vertex.  The fixed weight
two on `1,11` is necessary to break a fourth accidental active fibre that
would occur at weight one; this choice is disclosed and checked.

### 3.5 Are all three pure target equations satisfied?

Yes.  Each constant word has one compatible matching and that matching has
weight one.  The new vertices are completed differently in the three
colours, so this is not a disjoint gadget that multiplies both the incoming
and outgoing cycle terms.

### 3.6 Is the shore exchange one primitive cycle?

Yes.  On the zero shore the incoming and extra matchings are

```text
02|13|89,
01|28|39.
```

Their symmetric difference is the connected degree-two graph
`0-2-8-9-3-1-0`.  The primary checker reconstructs its adjacency; the audit
reconstructs it by XOR of edge masks.  Its signed incidence vector has
coordinate gcd one.

### 3.7 Is the claimed lattice separation stronger than a rational-rank test?

Yes.  On edge columns `01,02,12,24`, the four mixed-fibre generators have a
four-by-four minor of determinant one.  This proves integer independence and
saturation, not merely rank over `Q`.

Consequently the rank-two aggregate fibre lattice and the two rank-one
binomial fibre lattices sum directly.  There is no integer dependency, so
there cannot be an odd signed dependency among them.

### 3.8 Is physical overlap nevertheless present?

Yes.  The primitive diagonal vector and the selected cycle vectors both use
`01,02,13`.  This is literal physical-variable overlap.  The determinant-one
minor proves that the associated difference lattices still have no
non-direct intersection.  The example directly tests the distinction
required by the repository contract.

### 3.9 Is the zero holonomy elimination exact?

Yes.  With `a,b,c` the selected cycle directions and `q` the diagonal
exchange direction, the exact normalized equations are

```text
1+a+q=0,  1+b=0,  1+c=0.
```

The family sends `q` to `t` and `H=(abc)^(-1)` to `-1/(1+t)`.  Because `t`
is transcendental, no nonzero Laurent polynomial in `H` vanishes.  The pure
anchor equations hold along the same map.

The primary verifier checks the exact Groebner basis and finds no `H`-only
member.  The independent audit checks the triangular independence of the
substituted powers through degree twelve using Fraction row reduction.  The
written distinct-degree proof covers all degrees; the bounded audit is not
presented as that proof.

### 3.10 Is the family a candidate counterexample?

No.  The mixed word `000001000011` has exactly one compatible matching,

```text
04|17|26|35|89|10,11,
```

of weight one.  Its target-zero equation is a Laurent unit.  Thus the
complete target ideal of this fixed support is `(1)`.

This means the family refutes only the proposed **local** forcing mechanisms.
It does not refute the possibility that the complete target block always
forces a unit in the diagonal-only branch.

The artifact also makes no support-minimality or moment-balanced-gauge claim
for this family.  Those stronger upstream witness normal forms are not used
to advertise the sharpness result.

## 4. Evidence independence

The primary verifier uses:

- recursive first-vertex matching tuples;
- exact SymPy polynomial arithmetic in `t`;
- complete word, diagonal, and offdiagonal ledgers;
- direct shore matching enumeration and subshore hafnians;
- SymPy integer rank, determinant, and Groebner calculations; and
- explicit bridge, pure-anchor, and singleton matching sets.

The independent audit imports neither the primary verifier nor SymPy.  It
uses:

- 66-bit physical matching masks;
- a separate literal-table construction;
- custom Fraction coefficient tuples for `Q[t]`;
- packed base-three words;
- a last/lowest-vertex shore hafnian recursion;
- local Fraction Gaussian elimination and a custom determinant; and
- triangular coefficient matrices for the holonomy substitution.

The scripts necessarily share the stated table and target assertions.  Their
matching representations, polynomial engines, shore computations, and
elimination checks are separate.  Their independence is computational-route
independence, not independent mathematical authorship.

The arbitrary-order theorem is the written Cartesian-product,
alternating-cycle-flip, disjoint-support, and holonomy proof.  The finite
scripts audit the mechanism and sharpness family rather than proving an
arbitrary-order census.

## 5. Remaining boundary

The checkpoint leaves open:

- whether the primitive diagonal exchange meets another complete target
  lattice non-directly in every hypothetical witness;
- whether such an intersection kills every quotient sheet;
- whether a proper cancelling subshore is forced at arbitrary order;
- whether the complete target block always supplies a singleton, odd
  dependency, or another exact unit;
- the offdiagonal parallel-successor and outside-word survivors already
  isolated by `U7K`;
- the deeper-blocker branch;
- exclusion of the complete nonzero `r=1` matrix-unit branch; and
- the global Krenn--Gu conjecture.

## 6. Verdict

The theorem is accepted as an exact structural classification of
diagonal-only aggregate excess.  It forces a primitive one-shore exchange
and an exact shore-product normal form, but correctly refuses to turn that
support direction into a vanishing relation.

The twelve-vertex family is a sharp local obstruction to the proposed
shortcuts.  It simultaneously has a unique shortest diagonal-aggregate
cycle, all three pure anchors, physical-variable overlap, direct saturated
fibre lattices, no integer dependency, and freely varying selected
holonomy.  Its outside singleton transparently excludes it from the original
target.

No complete proof or counterexample follows.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.
