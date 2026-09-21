# Independent review: common-star full-source exclusion

## Verdict and exact scope

I accept the direct proof in
[`PROTECTED_SCAFFOLD_COMMON_STAR_FULL_SOURCE_EXCLUSION.md`](../../claims/arbitrary-order/PROTECTED_SCAFFOLD_COMMON_STAR_FULL_SOURCE_EXCLUSION.md).
For every finite number `k>=2` of protected K4 components, a simple
one-label common-star array cannot realize every physical ternary GHZ target
coefficient.  The proof derives an exact tensor decomposition on the words
whose center colors and uniform leaf colors vary independently, then uses a
scalar contradiction at odd order and a two-by-two rank contradiction at
even order.

The scope correction is load-bearing.  At odd `k>=3`, the diagonal argument
uses only component-constant target equations and therefore excludes the
odd-order common-star CSQ4 branch.  At even `k>=2`, the rank argument uses
many AB words outside the component-constant and U4 equation sets.  It proves
CSFULL for this construction, not even-order CSQ4 or FB.  It is not a normal
form for arbitrary protected hollow fillings or arbitrary witnesses and does
not prove the Krenn--Gu conjecture.  The global conjecture remains
**UNRESOLVED**.

The four durable artifacts were inspected at these SHA-256 values over
LF-normalized UTF-8 text bytes:

```text
owner:
0509d7013650ce2d384b496c4c6a7cafff3a278694436d2095ef249f8f7a0c18

primary companion:
d1670c5871b069d73746937028627e5f73a2dd355689dbdd4ca8aa4918f07d36

independent audit:
295abae2176a521f25ff4cbee3d91a5fa0363582c96b5052178edf981b6fccc3

test module:
9338d862c59d7fa4ca0e1d1d38b047f65cc8293613bd60fdd4823f3112400acf
```

I read the complete owner, the literal PSCS definition it cites, the primary
companion, and all eight scientific tests.  I independently derived the
physical classification and contraction proof before reading the primary,
then wrote and ran the separate audit below.  I did not re-review every
earlier PSCS result or certify concurrent frontier and ledger edits.

## Literal physical classification

Give center `u` color `x_u` and all three of its leaves color `y_u`.  A
crossing edge incident to local leaf `d` has endpoint color `d`, so among
the uniformly colored leaves only leaf `y_u` can cross.  The other two
leaves have exactly one compatible edge: their protected unit edge in
`M_(y_u)`.  This rules out a local BB type, crossing degree four, and a
second internal matching contribution.

After the forced leaf-leaf edge, the two remaining vertices are the center
and leaf `y_u`.  They may use their protected unit edge only if `x_u=y_u`;
otherwise each must cross.  A crossed center uses an A edge and a crossed
leaf uses a B edge.  Thus both crossing matchings have the same active
component set `S`, while their component-edge matchings may differ.  This
gives the literal physical identity

```text
F(x,y)=sum_(S subset V, |S| even)
         haf(A_x[S]) haf(B_y[S]) product_(u outside S) delta_(x_u,y_u).
```

This classification accounts for unequal center/leaf matching
interference.  It does not replace the two actual hafnians by a matching
polynomial in gadget products.  It also remains valid when a hafnian or a
contracted factor vanishes; no division or genericity is used.

For fixed `S`, the center hafnian depends only on `x_S`, the leaf hafnian
only on `y_S`, and the complementary Kronecker deltas give an identity
operator.  Hence, with tensor factors kept in component order,

```text
F=sum_(S even) (a_S b_S^T) tensor I_(V outside S).
```

All pairings are complex bilinear.  There is no conjugation, positivity, or
real-sign assumption.

## Odd-order diagonal obstruction

On the diagonal `x=y`, all inspected words are component-constant.  Weight
the color at every component by `h=(1,1,-2)`.  For an even active set `S`,
each component outside `S` contributes

```text
sum_c h[c]=0.
```

When `k` is odd, every even `S` is proper, so the complete contracted source
is zero.  The component-constant GHZ target gives

```text
sum_c h[c]^k=2+(-2)^k,
```

which is nonzero for every odd `k>=3`.  This is a diagonal trace argument,
not an invocation of target values at off-diagonal AB words.  It is therefore
valid under the component-target subsystem already contained in CSQ4.

## Even-order rank obstruction

For arbitrary local row and column covectors `r_u,s_u`, a term with active
set `S` contracts as

```text
A_S(r) B_S(s) product_(u outside S) (r_u dot s_u).
```

If every local dot product is zero, all proper `S` vanish.  At even order
only the full active set remains, and its contraction separates as
`A_V(r)B_V(s)`.

The two row systems and two column systems in the owner are pairwise locally
orthogonal for all four global combinations.  Their source contractions
therefore form one outer-product matrix and have rank at most one, including
when a factor vanishes.  Direct bilinear contraction of the full GHZ target
gives

```text
[[2, 1],
 [1, 1+2^(k-2)]],
```

whose determinant is `1+2^(k-1)`, nonzero over `C`.  The source and target
cannot agree on every AB word.

These contractions have nonzero coefficients on AB words outside even-order
CSQ4 and FB.  Unknown target entries cannot be discarded merely because the
proper source layers cancel after summation.  The owner states this boundary
explicitly and makes no even-order proper-subsystem claim.

## Sharp control and construction boundary

At `k=1`, the protected K4 by itself realizes the full ternary GHZ tensor:
each globally constant physical word has its unique protected matching of
weight one and every other physical word has source zero.  The odd target
contraction is `2-2=0`, and the even argument has no second component.  Thus
the `k>=2` scope is sharp.

The proof relies on the exact common-star support: a common center edge, the
color-indexed leaf edge, one unequal label on a simple component edge, and
zero other crossings.  An arbitrary protected hollow array may contain
center-leaf crossings or other leaf endpoint colors, which invalidate the
forced leaf pair and the active-set outer product.  No upstream theorem is
used to eliminate those entries.

## Independent exact replay

I wrote
[`audit_common_star_full_source_exclusion.py`](../../claims/arbitrary-order/audit_common_star_full_source_exclusion.py)
before reading the primary replay.  It imports only the Python standard
library and uses `Fraction` arithmetic.  It builds every protected physical
edge and actual A/B gadget edge, selects entries from the physical word, and
computes the `4k`-vertex hafnian by a direct perfect-matching recurrence.  A
separate component evaluator computes the common-active-set hafnian formula.

On exact fixtures of orders two, three, and four, the two evaluators agree on
every AB word: respectively 81, 729, and 6,561 comparisons, for 7,371 total.
The factors include unequal positive and negative rational values and the
order-four fixture has five differently labelled gadgets.  The audit also
enumerates every supported physical matching for every AB word at orders two
and three.  At every component the crossing-edge multiset is either empty or
exactly one A and one B edge; no BB or degree-four case occurs.

The same checker verifies all 81 unrestricted four-vertex physical words in
the `k=1` control.  It checks the odd diagonal contraction at `k=3` and the
even two-by-two source minor at `k=2` and `k=4`, including the displayed
target matrix and determinant.  These are finite corroborations of the
physical classification and arithmetic.  The quantifier over every finite
`k` is established by the written proof, not by these samples.

## Reproducible evidence and limitations

The primary and independent programs use separate implementations.  The
independent audit does not import the primary replay or any project
scientific helper.  This is separate-agent review in the same research
session, not separate-human refereeing.  No external theorem is imported,
and no Lean formalization or kernel check is supplied.

The primary companion checks 810 literal AB words at orders two and three,
all 81 unrestricted physical words at order one, the odd diagonal
contraction at order three, and the even outer-product identity at orders two
and four.  It checks the target determinant closed form for even orders two
through twenty and detects an added off-family center-to-leaf entry.  The
test module extends the closed-form samples through order forty and confirms
that breaking one crossed orthogonality condition allows a proper active
layer to survive.  In that mutation, the primary certificate contracts the
target against the actual supplied probes, and the test checks it against a
separate direct contraction rather than the canonical target matrix.  These
controls protect both physical-support assumptions used by the proof.

The following commands passed in bounded runs with a 900-second and
8192-MiB ceiling on each research computation:

```text
python -X utf8 claims/arbitrary-order/verify_common_star_full_source_exclusion.py
python -X utf8 claims/arbitrary-order/audit_common_star_full_source_exclusion.py
python -m unittest -v tests.test_common_star_full_source_exclusion
```

The final primary took 1.17 seconds, the independent audit 0.68 seconds, and
the final eight-test run 1.99 seconds at the process boundary.  Ruff and Python
compilation also passed for both checkers and the test module.  The exact
programs corroborate the finite expansions, controls, and arithmetic; the
all-order statement rests on the written proof.
