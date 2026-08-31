# GLD101 normalized a=0 R4 B-open resultant leaf

Date: 2026-08-31

Status: scoped exact selected-necessary-minor proof leaf; independently
replayable from a clean clone; global Krenn--Gu status **UNRESOLVED**.

## Exact obligation

Work on the normalized equal-leaf H4 chart with

- `a=0`;
- `R4=5*p^4-16*p^3+30*p^2-16*p+5=0`;
- `Q6(p,q)=0`; and
- `B*H2*Delta != 0`.

Here `Delta` contains the GLD88 chart gates.  The polynomial R4 is
irreducible over `QQ`, and

`resultant_p(R4, 2*p^2-2*p+1)=145`,

so `H2` is a unit on the R4 field.

If the GLD71 syndrome matrix has rank at most six, the selected actual
seven-minors `T3,Y1,X3` must vanish.  This is a necessary implication only;
the package does not claim a converse.

Because `B!=0`, write `C=B*t`.  Direct determinant reconstruction shows that
each selected minor has a common B factor.  After cancelling it, every
rational denominator factors through `Delta`; clearing those denominators is
therefore valid on the stated open locus.  Reduction modulo R4 yields three
polynomials that are quadratic in B and linear in t.

## Compact resultant proof

Write each reduced equation as

`H_i(B,t)=A_i(B)*t+C_i(B)`.

A common zero of `T3,Y1,X3` must make both pairwise t-resultants vanish:

```text
R_TX(B) = A_T3(B)*C_X3(B) - A_X3(B)*C_T3(B)
R_YX(B) = A_Y1(B)*C_X3(B) - A_X3(B)*C_Y1(B).
```

Both are quartics in B over the finite algebra

`A=QQ[p,q]/(R4,Q6)`.

Their 8-by-8 Sylvester determinant in B is an element `rho` of A.  In the
basis

`p^i*q^j`, for `0<=i,j<4`,

multiplication by `rho` is a 16-by-16 rational matrix.  Its exact determinant
is nonzero.  The certificate pins the entire `rho` coordinate vector and
multiplication matrix; its determinant has a 3,429-digit numerator, a
252-digit denominator, and SHA-256

`f0b194b39ae1a5638defb64e3eb664400b69d423d7ac85db0c62ce3cd549db48`.

Thus multiplication by `rho` is invertible, so `rho` is a unit in A.  The two
quartics cannot share a B-root on any R4,Q6 fibre.  Hence the three selected
minor equations have no common point on the stated R4 B-open locus.

This argument does not assume that Q6 is irreducible over the R4 field.  A
nonzero multiplication determinant proves invertibility in the full
16-dimensional quotient algebra and therefore handles every component and
every R4 root simultaneously.  All arithmetic is exact over `QQ`, so the
identity base-changes to characteristic zero.

## Reproducible evidence and independence

The tracked package consists of:

- `claims/arbitrary-order/certificates/GLD101_A0_R4_B_OPEN_RESULTANT_CERTIFICATE.json`,
  LF SHA-256
  `1961eed09059a7434002c610f89eb4e0ebc195398fbd026b0a4a7ddf778cc36e`;
- `claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_r4_b_open_resultant.py`;
- `claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_r4_b_open_resultant.py`;
  and
- `tests/test_gld101_r4_b_open_resultant_portable_leaf.py`.

The primary checker imports only hash-pinned GLD71/GLD88 parents, rebuilds
the actual sparse B,C determinants, performs the B-open substitution and
denominator audit, and computes the Sylvester and multiplication determinants
by subset dynamic programming and domain-matrix elimination.

The audit imports no repository module or primary checker.  It parses the
literal GLD71 relation table with `ast.literal_eval`, transcribes the
hash-pinned GLD88 a=0 chart locally, substitutes `C=B*t` at the leaf level,
and independently reconstructs the three determinants.  It recomputes the
B-resultant by recursive Laplace expansion and recomputes the multiplication
determinant in a reversed basis with Bareiss elimination.  Every load-bearing
record is compared with the hash-pinned certificate.

Run from repository root:

```text
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_r4_b_open_resultant.py
python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_r4_b_open_resultant.py
python -m unittest -v tests.test_gld101_r4_b_open_resultant_portable_leaf
```

No Singular installation, ignored run directory, terminal transcript,
Commons checkout, or machine-specific path is required.

## Historical lineage

The earlier accepted R4 computation used a direct Singular unit lift.  Its
source SHA-256 was
`fad9adaa23e2f94093b7b6db7875981ed0c7961791d2d01a4ab7a908fcab6cc1`.
An independent direct-minor audit reproduced the same Q6/T3/Y1/X3 equation
hashes and multiplied back 564 printed terms exactly.

That historical certificate remains valid scoped lineage, but its output was
about 50 MB because the normalized multipliers contained 11,077-digit
coefficients.  This package derives a new compact exact resultant proof from
the tracked parents.  The historical process, transcript, and giant
multipliers are not load-bearing inputs.

## Scope boundary and frontier effect

This package does not prove:

- a converse from `T3,Y1,X3` to syndrome rank;
- the `B=0` or generic C-open loci;
- another residual factor, arbitrary `a`, endpoints, or physical incidence;
- P6, P8, or the full E31 wall; or
- the global Krenn--Gu conjecture.

No `docs/current-frontier.md` change is made because the exact scoped R4
B-open selected-minor conclusion and its role in the recorded P8 parent
attempt predate this package.  The quantifiers, locus, implication edge, and
residual proof topology are unchanged.  This commit replaces a host-local
large-transcript dependency with a clean-clone compact certificate and a
second independent audit route.  Any later parent-branch closure or theorem
composition must update the live frontier in its separately reviewed change.
