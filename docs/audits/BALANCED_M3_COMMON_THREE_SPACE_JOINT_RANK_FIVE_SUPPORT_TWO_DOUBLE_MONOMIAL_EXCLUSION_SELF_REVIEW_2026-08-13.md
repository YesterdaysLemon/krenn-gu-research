# Hostile self-review: joint-rank-five support-two double-monomial exclusion

## Scope under review

This review covers
[`BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_DOUBLE_MONOMIAL_EXCLUSION_THEOREM.md`](../../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_DOUBLE_MONOMIAL_EXCLUSION_THEOREM.md),
its SymPy verifier, and its independent standard-library audit.

The package excludes exactly the transverse joint-rank-five profile with a
rank-two third row of kernel support two, both involved rows of rank two, and
both root blocks coordinate monomials.  It does not exclude the singly
monomial/nonmonomial case, where the nonmonomial block is unrestricted at
this stage, another involved-row profile, support one, a
Hilbert--Burch boundary, joint rank at most four, or any global branch.
Global Krenn--Gu remains **UNRESOLVED**.

## Adversarial claim inventory

1. The two involved rank-two rows have coordinate kernels and aligned
   diagonal block rows even though the third row is no longer injective.
2. Support two plus two coordinate-monomial blocks forces the colours and the
   projected three-plane into one canonical normal form.
3. Complete target consistency, not a selected quotient, gives three mixed
   zero maps and one nonzero rank-one square on the third-row two-plane.
4. Full singleton rank is equivalent to nonvanishing of one alternating
   separated tensor.
5. The mixed-product lemma exhausts every source-support case of the squared
   row and permits neither a hidden rank-five exception nor a
   characteristic-zero division error.

## Hostile checks

### 1. Was a rank-six containment `A_3 subset K` reused silently?

No.  S2AG gives the rank-five split

```text
K=P direct-sum eta^perp,
U=D_(B,C)(P),
```

with `dim P=3`.  The proof uses only this split.  It never replaces
`eta^perp` by all of `A_3` and never assumes the third row is injective.

### 2. Does the target-kernel argument still force coordinate kernels?

Yes.  A covector in `ker pi` kills the corresponding empty-permanent row and
all second components of `P`.  Contracted `U` then has one fixed third-root
factor `(v tensor id)(B)`.  Independent pure target monomials show that a
nonzero kernel covector cannot use two colours; the factor is nonzero and
has the matching coordinate colour.  A two-dimensional kernel would contain
a vector of support at least two, so a rank-two row has exactly one
coordinate kernel line.  The symmetric proof applies to `rho`.

### 3. Could a coordinate monomial use a different third-root colour?

No.  For `B`, its nonzero endpoint row is the row selected by `ker pi`, and
the target-kernel conclusion says its third factor is the same coordinate.
Its contraction by `eta` is nonzero and lies on the first support colour.
These facts force both monomial endpoints to that colour.  The second block
is symmetric and uses the other support colour.

### 4. Is the normal form for `P` losing an extension parameter?

No.  The zero rows put `P` inside
`e_1^perp direct-sum e_0^perp`.  Contracted target consistency supplies
preimages of `e_0 tensor e_0` and `e_1 tensor e_1`.  The only ambiguity in
either ambient preimage is the line `(e_1,-e_0)`, which violates those zero
coordinates, so the two pure lifts lie in `P`.  After subtracting them, a
third vector is `(alpha e_2,beta e_2)`.  Both projection ranks are two, so
`alpha beta!=0`, giving `(e_2,tau e_2)` with `tau!=0`.

### 5. Are the mixed zero identities only quotient identities?

No.  The exact singleton span is supported on root rows

```text
000, 111, 200, 121.
```

The root-row pairs `(0,1)`, `(0,2)`, and `(2,1)` meet neither that support
nor the GHZ diagonal, so their empty-permanent coefficients vanish in every
third-root row.  Pair `(2,2)` also misses the singleton span and carries only
`T_2` in third-root colour two.  This is the full `27`-row target equation.

### 6. Why is the alternating tensor the singleton determinant?

In the basis of `P`, the `P`-projection of the source-`X` cross column has
coordinates obtained by restricting `v_0,v_1,v_2` to `X`; similarly for
`Y,Z`.  Expanding their `3 x 3` determinant gives exactly the signed six-term
tensor in the theorem.  Since `D_(B,C)|_P` is injective, these projected
columns are generically independent exactly when the physical singleton
columns are.  Full sensor rank four in particular requires this determinant
to be nonzero.

### 7. Is decomposability used correctly in the three-source case?

Yes.  The square image is the Segre tangent space at
`x tensor y tensor z`.  Projecting a decomposable image successively modulo
the three base factor lines shows that it shares at least two of them.  This
is a pointwise tensor statement, not a generic tangent assertion.  It permits
the displayed normalization to `x tensor y tensor t`, including the case
`t` proportional to `z`.

### 8. Does the two-source conjugate case omit a larger zero-divisor space?

No.  If `x tensor b+a tensor y` is nonzero, the first zero equation kills
the entire `Z` component and the second leaves only `x-y`.  If it is zero,
`q_0` is exactly the conjugate line.  A nonzero remaining tangent tensor gives
the displayed two-plane, which contains `q_0`; spanning it would violate
`V intersect Q=0`.  When that tensor also vanishes, the common zero-divisor
space is `span(x-y) direct-sum Z`, and the last mixed equation supplies both
relations needed to kill the alternating tensor.

### 9. Does the three-source one-zero case divide by a possible zero?

No.  After setting one scaling coefficient to zero, the other two are
opposite and nonzero.  The proof then splits `z,t` independent versus
proportional.  In the proportional case it separately treats the exceptional
coefficient equality.  Characteristic zero is used only to conclude from
`2 lambda=0` that `lambda=0`; no parameter declared possibly zero is divided
out.

### 10. Could the finite-field reconnaissance be carrying the proof?

No.  The earlier searches returned either `unknown`, timeout, or bounded
no-hit outcomes and are not recorded as evidence.  The theorem is the
arbitrary-vector case split in Lemma 1.  The scripts replay exact symbolic or
rational identities only.  The sharpness fixture is over `Q` and shows why
joint rank five plus the target table is insufficient without singleton
independence.

### 11. Are the primary verifier and audit genuinely independent?

The primary uses SymPy matrices, symbolic vectors, and Kronecker products.
The audit imports no repository code or symbolic package; it implements a
separate tuple-based `Fraction` tensor algebra and row reduction, changes the
source colours and numerical representatives, and independently reconstructs
the canonical plane and sharp fixture.  Both are identity replays; neither is
presented as a formal proof of the arbitrary-vector lemma.

## Verdict

The package supports the exact scoped exclusion.  The load-bearing
conjunction is:

```text
joint row rank five
+ third-row rank two with support-two kernel
+ involved-row profile (2,2)
+ two coordinate-monomial blocks
+ all target rows
+ full singleton independence.
```

Dropping the last condition admits the exact rank-drop fixture.  At the time
of this review the singly-monomial/nonmonomial `(2,2)` profile remained open
without a proved tangent-family restriction on the nonmonomial block.  The
successor complete-profile theorem now excludes that case and shows that the
apparent Type-II family collapses to a monomial block; its separate proof,
verifier, audit, and review do not retroactively strengthen the S2AH
argument.  Every other stated residual remains open.  Global status must
remain **UNRESOLVED**.
