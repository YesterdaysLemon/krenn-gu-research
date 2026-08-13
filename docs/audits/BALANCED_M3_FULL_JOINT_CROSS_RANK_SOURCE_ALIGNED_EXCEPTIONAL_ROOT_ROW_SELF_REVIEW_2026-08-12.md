# Self-review: source-aligned exceptional-root-row obstruction

## Claim audited

The S2U sparse block-permanent equation has no invertible joint cross map
whose exceptional root block row is supported on one nonroot/source summand.

## Scope and quantifiers

- Exact linear algebra is used after importing the characteristic-zero S2U
  normal form.
- The aligned row is specifically the exceptional root opposite the unique
  surviving root--root edge.  The theorem does not silently symmetrize this
  role to either endpoint root.
- Only support on exactly one source summand is excluded.  A row space
  meeting two or three source summands remains open.
- No statement is made about joint cross rank at most eight, other S2Q
  strata, `m>=4`, or global resolution.

## Adversarial checks

1. **Could a mixed `q` have a larger zero-divisor space through
   cancellation?**  No.  Equality of two nonzero rank-one tensors forces
   both proportionalities, leaving the single line `span((x,-y))`.
2. **Are the two vectors placed in `Z(q_c)` really independent?**  Yes.  The
   lower `6 x 6` block is invertible after expansion along the aligned
   invertible root row, so the three `p_b` are independent.
3. **Do the ignored `X` components of `p_b,q_c` contribute?**  No.  The
   root-1 factor already lies in `X^*`; every term using another `X^*`
   component has repeated source degree and vanishes in the square-free
   `(1,1,1)` projection.
4. **Does the target really kill every `b!=c` row?**  Yes.  Both GHZ and the
   exceptional line `A_1 tensor e_s tensor e_s` have equal root-2/root-3
   colours.
5. **Could the pigeonhole step leave a complementary configuration?**  No.
   Two pure `q` vectors in one summand force all three `p` vectors into that
   summand; their independence fills it and makes those `q` vectors dependent
   on the `p` vectors.

## Evidence independence

The primary script uses symbolic rational matrices and canonical pure/mixed
normal forms.  The audit imports neither the verifier nor SymPy; it performs
a separately written finite-field census of every nonzero vector in a
six-dimensional binary space and independently enumerates the eight purity
patterns.  These computations replay the structural boundary.  The written
rank-one tensor argument, not the finite census, proves the arbitrary-field
lemma.

## Residual risk and honest boundary

The argument depends crucially on exact source alignment.  Replacing
`R_1=X^*` by a graph over `X^*` adds three mixed contributions to (5), so the
zero-divisor lemma cannot be imported without a new graph-gauge calculation.
That two-source/graph chart is the next stated obligation, not an implicit
corollary.

Global status remains **UNRESOLVED**.
