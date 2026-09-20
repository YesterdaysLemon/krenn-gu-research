# Independent review: common-star two-sided binary cycle control

## Verdict and exact scope

I accept
[`PROTECTED_SCAFFOLD_TWO_SIDED_BINARY_CYCLE_NO_GO.md`](../../claims/arbitrary-order/PROTECTED_SCAFFOLD_TWO_SIDED_BINARY_CYCLE_NO_GO.md)
as an exact mechanism no-go inside the one-label common-star family.  The
displayed nine-component array simultaneously satisfies both localized
three-cycle faces and every singleton and same-color double-component target
for one binary color pair.  It has a specified nonzero three-component cut.

This proves that those two faces plus that binary low-order subsystem are not
already contradictory.  The array has no color-2 gadgets and supplies no
distinct-color S2 equations.  It is not an FB or CSQ4 model, an arbitrary-
witness normal form, or a counterexample to Krenn--Gu.  The global conjecture
remains **UNRESOLVED**.

The four durable artifacts were inspected at these SHA-256 values over
LF-normalized UTF-8 text bytes:

```text
owner:
68e804c6568d54488f5fd9cd0e57658e6bef578d71200811f444eee9704e7710

primary replay:
aa0df74a978af7cb820a522d921792ba332c7626d07bc80203897b91dfe95346

independent physical audit:
cdf6beeb73bebf5628075568515a40e4255f7839e944190607ec12a79b93d39a

test module:
360353962448292ae68e654fa680e18a96c5048ae40b98012d52066f39d70b61
```

The earlier PSCL owner remained byte-for-byte unchanged from its accepted
review identity.  I rechecked the PSCL source and matching-row deletion used
by this owner, but this review does not reopen the whole PSCL proof or certify
concurrent frontier and ledger metadata.

## Parameter tower and nonzero factors

The parameter construction is nonvacuous.  The polynomial
`H(s)=3s^2+3s+1` has complex roots, and each of

```text
s, 1+s, 2+3s, 3s+1, 2s+1
```

is coprime to `H`.  Thus `P_s(r)` has degree four and nonzero constant
coefficient for either chosen root `s`.  Its norm is exactly

```text
N(r)=r^8+36r^6+134r^4+36r^2+1.
```

Direct polynomial gcd calculations show that `N` is coprime to
`r(r+1)(r^2-1)(r^2+1)`.  Every root `r` paired with the chosen `s` is
therefore nonzero, is not `-1`, and has `r^2+1!=0`.  The leading and constant
coefficients of the displayed quadratic `E_(s,r)(t)` are then nonzero.  It
has complex roots and neither is zero.

These same facts cover every actual factor and denominator.  The products
`q=-1-s`, `w=s/2`, `delta=-(2+3s)/2`, and `-1/2` are nonzero, as are the four
entries `t`, `rt` of the nontrivial center block.  Hence `B=Q/A` is defined
and nonzero exactly where `A` is nonzero.  No irreducibility, distinct-root,
or numerical-embedding premise is used.

## Actual array and physical provenance

The directed support has 27 arcs, no loop, and no opposite pair.  Every arc
has the one displayed endpoint label `(0,1)`, so there is at most one gadget
on each component pair.  Installing the center factors `A`, leaf factors
`B`, and protected unit K4 matchings therefore gives a literal 36-vertex
common-star array.

The independent audit reconstructs this physical graph for each asserted
component word.  Its perfect-matching recursion keeps the center and leaf
edges separate and uses their actual algebraic weights.  A second evaluator
computes the component source as

```text
sum per(A[J,K]) per(B[J,K]).
```

For all 90 asserted cuts and the exhibited failed cut, the literal physical
matching sum and this permanent expansion agree identically before imposing
`H`, `P`, or `E`.  The 90 physical graphs have between 3 and 51 supported
perfect matchings; the failed word has 49.  This establishes the physical
source bridge without replacing exterior terms or permanents by independent
data.

The independent algebra then reduces each actual source successively through
`E(t)`, `P_s(r)`, and `H(s)`, using univariate remainders over the appropriate
fraction fields.  It imports no primary verifier and does not use the
primary's Groebner basis.  It still uses SymPy arithmetic, so it is an
independent derivation and physical reconstruction rather than a fully
separate computer-algebra implementation.

## Both localized faces and their full words

The product matrix has row and column sum `-1`.  The three relevant forms are

```text
q+2w=-1,        3w+delta=-1,        2(-1/2)=-1.
```

Thus all singleton rows and columns have the required source zero.  For a
cycle subset `T` of size `m`, direct expansion with the actual factors gives

```text
Z(I,T)=Z(T,O)=1+m*s+binom(m,2)*s^2.
```

For `m<3` this equals `(1+s)^m=(-q)^m`; for `m=3` it is `H(s)=0`.  These are
the two opposite localized systems in the same matrices.  The closing blocks
restore the outside singleton sums without entering either contraction.

Applying the exact PSCL matching-row deletion in each orientation gives the
two complete eight-word faces.  The regression test evaluates their literal
binary component sources: with the exterior fixed to zero, only the all-zero
cycle word has source one; with the exterior fixed to one, only the all-one
cycle word has source one.  The other fourteen face words have source zero.

## Exhaustive low-order table

Before imposing `P` or `E`, the primary replay expands every two-row source
and reduces only by `H`.  For the original array, its 36 cases are exhausted
by the owner's table:

| Pair type | Count | Source modulo `H` |
| --- | ---: | --- |
| `C,C` | 3 | `0` |
| `C,I` | 6 | `E_(s,r)(t)/(24rt)` |
| `C,O` | 6 | `0` |
| `C,D` | 6 | `0` |
| `I,I` | 1 | `P_s(r)/(16r^2)` |
| `I,O` | 4 | `0` |
| `I,D` | 4 | `0` |
| `O,O` | 1 | `0` |
| `O,D` | 4 | `0` |
| `D,D` | 1 | `0` |

The counts sum to 36.  The replay checks every pair individually rather than
assuming the displayed symmetries.  It then checks all 36 pairs in the
transposed array, where `I` and `O` exchange roles.  This gives 72 exact table
identities modulo `H` alone.  Imposing `P=0` and `E=0` kills the only two
surviving types.

The complete asserted cut set is therefore

```text
9 cuts of size 1,
36 cuts of size 2,
36 cuts of size 7,
9 cuts of size 8.
```

Sizes 1 and 8 are the two binary singleton orientations.  Sizes 2 and 7 are
the two same-color double-component orientations, using
`F_(A,B)(V\S)=F_(A^T,B^T)(S)`.  These 90 cuts are exhaustive for the claimed
binary S1 and same-color S2 subsystem.  They do not cover other binary words
or the distinct-color three-color S2 equations.

## Interference controls

The two negative tests protect the actual-factor claim.  Replacing the
nontrivial `I`-by-`O` center block by ones and compensating in `B` preserves
the product matrix `Q`, all singleton equations, and both localized faces.
It breaks the `{3,4}` double cut.  Thus product data alone do not prove the
low-order subsystem.

Likewise, replacing the product of the two actual permanents by an ordinary
matching-polynomial expression in `Q` gives a nonzero `{3,4}` value, while
the correct source vanishes.  The unequal center/leaf matching interference
is load-bearing and has not been silently discarded.

## Exact remaining failure

For `S={0,1,3}`, corresponding to `001011111`, both exact implementations
give

```text
F(S)=(r^2+1)/(12r).
```

The norm gcd proves its numerator and denominator are nonzero for every
admitted parameter choice.  Hence this is a genuine failed proper binary cut,
not a numerical observation.  The control also has no color-2 support, so a
singleton color-2 change in a color-0 background has source one.  Both facts
are explicit scope boundaries.

## Reproducible evidence and limitations

The following checks passed in bounded runs with a 900-second and 8192-MiB
ceiling per research computation:

```text
python -X utf8 claims/arbitrary-order/verify_common_star_two_sided_cycle_control.py
python -X utf8 claims/arbitrary-order/audit_common_star_two_sided_cycle_control.py
python -m unittest -v tests.test_common_star_two_sided_cycle_control
```

The primary reports 16 localized equations, 72 pre-specialization table
identities, and all 90 target cuts.  The independent audit reports no
physical/component mismatch.  Five unit tests pass, including both full
faces, the product-preserving factor mutation, and the interference-deletion
control.  Ruff and Python compilation also pass for both checkers and the
test module.

No external theorem is imported into this construction.  No numerical or
modular computation is used as a proof premise.  No Lean formalization or
kernel check is supplied, and this is separate-agent review in the same
research session rather than separate-human refereeing.
