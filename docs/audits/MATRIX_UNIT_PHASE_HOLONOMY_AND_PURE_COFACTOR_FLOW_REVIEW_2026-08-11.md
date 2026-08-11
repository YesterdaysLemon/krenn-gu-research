# Hostile review of matrix-unit phase holonomy and pure-cofactor flow

## Verdict and provenance

**PASS, as an exact phase-sensitive reduction with explicit sharp
boundaries.**  The active-cycle result constructs a genuine nonzero integral
endpoint-character circulation and its diagonal-gauge-invariant Laurent
monomial.  The full mixed equations determine that monomial only when every
cycle fibre is exactly binomial.  The pure-cancellation result correctly
uses a least supported residual before asserting nonzero first cofactors,
then applies exact hafnian row expansions to obtain the branching/even-cycle
split.

The sparse eight-vertex cycle and the two four-vertex scalar shores are
accepted only as sharpness.  None is a Krenn--Gu witness or counterexample.
The deeper branch, all phase normal forms, the `r=1` branch, and the global
conjecture remain **UNKNOWN/UNRESOLVED**.

## 1. The holonomy exponent is a genuine torus circulation

For one transport step, the selected offdiagonal matching `F_i` induces the
old word and the bridge-normalized diagonal matching `G_i` induces the new
word.  The endpoint-label character of their exponent difference is exactly

```text
1_(chi_(i+1))-1_(chi_i).
```

Summing around a word cycle telescopes to zero at every vertex-colour
coordinate.  Therefore the product of bridge/cross matching ratios is
invariant under arbitrary local diagonal scaling, not only under the
positive GHZ subgroup used for moment balance.

The exponent vector is not silently allowed to be zero.  Residual pure
matchings cancel stepwise.  Every remaining positive edge is diagonal and
every remaining negative edge is offdiagonal.  A fixed matrix-unit edge
cannot belong to both classes, so the two supports do not cancel.  Every
selected cross core is nonempty, proving that the circulation is nonzero.

This gives a nonconstant invariant Laurent monomial.  It does **not** give a
universal value for that monomial.

## 2. The binomial equation uses the complete fibre

At each cycle word there is an incoming diagonal matching and an outgoing
offdiagonal matching.  The identity

```text
lambda(F_i)=-lambda(G_(i-1))
```

is valid only if those are the complete compatible matching fibre.  The
theorem states this as an exact alternative:

- if another matching occurs anywhere, the cycle remains in the aggregate
  branch;
- if no other matching occurs, multiplication gives
  `H=(-1)^m`.

No summed response is divided or multiplied as if it were a binomial.  This
repairs the exact logical hazard identified in the preceding active-word
review.

## 3. Odd binomial holonomy is not a sign contradiction

The sparse eight-vertex table uses three binary bridge-square transitions.
The primary and independent checkers agree on:

```text
selected words:                         3;
physical nonzero pairs:                 18;
complete matching terms per word:       2;
diagonal/offdiagonal values per word:    (1,-1);
endpoint-character circulation support: 12;
Laurent holonomy:                        -1=(-1)^3.
```

All cross, bridge, and residual edges in the construction are distinct, so
the prescribed endpoint labels define one consistent physical sparse table.
The table directly refutes the tempting claim that an odd word cycle gives
`1=-1`.  The missing step in that claim is the unjustified assumption that
the nontrivial invariant holonomy equals one.

The construction omits ten pairs and every colour-two label.  It does not
have complete `r=1` support, does not realize `Delta_(8,3)`, and says nothing
about the geometric deeper component.  It is accepted only at the scalar
holonomy boundary stated in the theorem.

## 4. A displayed matching term does not automatically activate a cofactor

For an arbitrary zero hafnian, a nonzero matching monomial can cancel inside
each first deletion cofactor.  The theorem does not assume otherwise.

Instead it chooses a least-cardinality even residual `R` whose hafnian is
zero but whose support has a perfect matching `P`.  Deleting an edge of `P`
leaves a smaller residual supported by `P` minus that edge.  Its hafnian
cannot vanish by minimality.  Hence every edge of `P` has nonzero aggregated
cofactor at `R`, and the active cofactor graph really spans all vertices.

The empty-hafnian convention and nonzero physical matching weights also
show that `|R|>=4`; there is no hidden two-vertex exception.

## 5. Euler flow gives exactly the claimed graph split

At each vertex, partner expansion of the zero hafnian is

```text
sum_j z_ij haf(Z[R-{i,j}])=0.
```

These summands are the edge flows `C_ij`.  Since the active graph spans, a
degree-one row would contain one nonzero term and could not sum to zero.
Thus every degree is at least two.

If a degree is at least three, the theorem records phase branching and stops.
If no degree exceeds two, the graph is 2-regular and hence a union of
cycles.  Each row on a cycle has two terms, forcing consecutive values to be
negatives.  An odd cycle would force a nonzero value to equal its negative,
which is impossible outside characteristic two.  The even alternating-cycle
conclusion is exact.

The active cofactor graph is not confused with the original pure support
graph.  A physical pure edge may have zero complementary hafnian and be
absent from the flow graph.

## 6. Both pure-flow alternatives are sharp

The `K_(2,2)` example has two matching terms `6` and `-6`; its four active
cofactor values alternate around one cycle.  The complete `K_4` example has
three matching terms `1,1,-2`; all six cofactor edges are active and every
row is a three-term zero-sum polygon.

Both examples are minimal supported cancellations on four vertices.  Thus
neither phase branching nor alternating even cycles can be removed using
only one zero pure hafnian and support nonvanishing.

## 7. Gauge covariance is exact and does not add positivity

Under `z_ij -> t_i t_j z_ij`, the hafnian on `R` scales by the product of all
`t_i`, and every `C_ij` scales by that same product.  Zero/nonzero status,
the active graph, and the alternating relations are unchanged.

Together with the Laurent invariance of active holonomy, this justifies
putting a hypothetical complex witness into the preceding moment-balanced
gauge before applying the phase reduction.  It does not make the cofactor
values positive or align their phases.

## 8. Computational independence

The primary checker uses recursive supported perfect matchings, exact
rational diagonal scaling, an explicit endpoint-character counter, generic
recursive hafnians, and automated least-residual selection.

The no-import audit encodes endpoint labels as decimal pairs, computes word
fibres by a least-set-bit recursion, rebuilds the Laurent numerator and
denominator independently, and checks separate integer cycle/branching
examples with a bitmask hafnian.  It shares no primary matching or hafnian
implementation.

The programs audit the bounded tables and conventions.  The arbitrary-order
proof is the written character, minimality, and Euler argument.

## 9. Accepted proof-topology update

```text
support-minimal complex matrix-unit candidate
  -> actual squared-magnitude moment gauge              PROVED
  -> active bridge transport choices                    PROVED reduction
  -> deeper exit                                        OPEN
     or least pure cancellation residual
          -> cofactor branching / alternating cycles    PROVED split, OPEN
     or finite active cycle
          -> aggregate fibre / binomial Laurent H        PROVED split, OPEN

binomial cycle equation H=(-1)^m:                       PROVED;
odd binomial cycle contradiction without fixing H:      FALSE;
pure cofactor branching/even cycles excluded:            UNKNOWN;
aggregate or binomial holonomy excluded:                 UNKNOWN;
r=1 matrix-unit branch:                                  UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.
```

## Strongest fresh-referee objection

The new Laurent monomial can look like a conserved sign, but it is a free
nonzero torus invariant until additional target equations constrain it.  The
three-step sparse table realizes the odd value `-1` exactly.  Likewise, an
alternating even cofactor cycle is a conservation law, not a contradiction.
The theorem is accepted because it converts the two vague cancellation exits
into exact gauge-invariant algebraic normal forms while explicitly retaining
their unresolved phase freedom.
