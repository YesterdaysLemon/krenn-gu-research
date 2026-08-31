# Adversarial review of GLD103: all-zero coefficient branch exclusion

## Verdict

**PASS -- GLD103 exact scoped theorem.**

The tracked primary, independent audit, full certificate, and exact
comparison-only reconciliation all replayed successfully from a detached
clean checkout of commit `02ca1921c00deecbec1fd9c2b3dd378f381ce67e`.
The durable replay-provenance record pins every repaired 64-hex source and
comparison digest, the tracked certificate, and all three clean-run manifests and logs. The
comparison helper is neither a runtime dependency nor primary acceptance
evidence. This PASS certifies only the exact branch stated below. The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Proposition under review

The theorem is over an algebraically closed field of characteristic
zero, on the normalized GLD88/F88 equal-leaf H4 chart with symbolic
arbitrary a. It assumes

    Q6(p,q) = 0,
    rank M(G) <= 6,
    B*H2*Delta != 0,

and the coefficient branch

    G_T0 = G_T1 = G_T2 = G_Y1 = G_X3 = 0.

Its conclusion is that this intersection is empty. M(G) is the GLD71
37-by-9 syndrome matrix. The five selected actual minors are T0, T1, T2,
Y1, and X3, with the row/column sets stated in the GLD103 theorem document.
The E31 wall/equation is neither imposed nor inverted.

The review is of this exact branch only. It is not a review of the pivot
branches, an endpoint theorem, or a physical/global Krenn--Gu resolution.

## 2. Adversarial checklist

| check | PASS condition | current status |
| --- | --- | --- |
| Exact chart reconstruction | Clean-clone primary rebuilds the normalized GLD88/F88 chart, Q6, H2, Delta, and all five actual minors from pinned parents. | PASS |
| Field and quantifiers | The proof is exact over QQ, extends to every algebraically closed characteristic-zero field, keeps symbolic arbitrary a, and introduces no specialization or hidden inversion. | PASS |
| Open-set audit | Every denominator is shown nonzero on D(B*H2*Delta); no conclusion is drawn on Delta=0 or H2=0. | PASS |
| Clearing gate | The package records ClearingGate=P^23*H2^45 and proves the open-set equality because P|Delta, H2 is already inverted, and integer contents are characteristic-zero units. | PASS |
| Rank bridge | The primary proves only the one-way implication rank M<=6 => vanishing of the selected actual minors. No selected-minor or coefficient-minor converse is used. | PASS |
| Affine-C identity | For every selected minor, exact parameter-only clearing gives A_i=F_i+C*G_i with F_i=B*f_i; this is checked entrywise, not inferred from a sample. No B-coefficient is rescaled independently. A later single whole-P_i rational-content division is allowed only when its uniform unit and exact reconstruction are recorded. | PASS |
| Ratio equations | On D(B), the primary records H_i=f_i+t*G_i for t=C/B and uses the ratio only in that B-open. | PASS |
| Gamma identity | The package verifies K_ij=F_i*G_j-F_j*G_i=B*Gamma_ij and uses it only in the forward direction. | PASS |
| Exhaustive coefficient split | The five open pivot patches and their all-zero complement are explicitly exhaustive; the all-zero equations are not confused with C=0. | PASS |
| Coefficient/Fitting reduction | On the all-zero leaf, P0=F_T0/B, P1=G_T0, ..., P5=G_X3 are quadratic in B, and the nonzero vector (1,B,B^2) forces all 20 maximal row minors; the cover uses the necessary subset D012,D013,D014,D015,D023,D123. | PASS |
| Exact factor cover | The six selected coefficient determinants have exact squarefree support p, p-1, P, H2, p^2+1, R4, R8, C4, F4, p^2-2*p+2, and F40. Raw cover degree/multiplicities and every clearing scalar are reported separately and reconciled between the native and source-normalized representations. | PASS |
| p and p-1 fibres | The required GLD102 nonzero-offset fibre certificates are present, correctly scoped, and do not import a selected-minor converse. | PASS |
| Boundary factors | P is removed only because P|Delta; H2 is removed only because D(H2) is declared. | PASS |
| Determinant-fibre leaves | C4, R8, p^2+1, and R4 each have an exact determinant-fibre Macaulay identity with its localizer and a checker that validates the identity. | PASS |
| Direct all-zero-branch leaves | F4 and p^2-2*p+2 each have an exact localized Macaulay contradiction in `<Q6,P0,...,P5,z*B*Delta-1>`; this is not the GLD83 physical Fitting ideal and neither leaf is replaced by a rank converse. | PASS |
| Degree-40 leaf | F40 has an exact quotient-gcd relation and a nonzero multiplication norm. The full primary replay explicitly sets `GLD103_FACTOR_MATRIX_INVERSE=1` and `GLD103_FACTOR_NO_FINAL_INVERSE=1`, and its certificate records effective value `1` with each environment-variable name as the source. The modular timeout remains neutral. | PASS |
| Independent audit | The audit differs in derivation, representation, and checker, and states that arithmetic/factor-cover independence is not independent reconstruction of the graph model or rank bridge. | PASS |
| Clean-clone replay | The primary, independent audit, and comparison-only helper ran from the same detached clean candidate commit and reproduced the exact source identities, factor support, fibre certificates, quotient-gcd relation, and hashes recorded in the replay provenance. | PASS |
| Scope fences | No claim is made for pivot branches, B=0, E31, Delta=0, H2=0, other charts/components/sources/roots/orders, physical incidence, or global resolution. | PASS |

## 3. Specific failure modes checked

### 3.1 Hidden strengthening of the rank statement

The implication needed is

    rank M(G) <= 6
        => every actual 7-by-7 minor vanishes
        => T0=T1=T2=Y1=X3=0.

The reverse implication is not available and is not permitted in this review.
In particular, the six coefficient/Fitting determinants derived from the
all-zero branch are a necessary support locus only. A determinant factor
cover by itself does not exclude a physical point.

### 3.2 Hidden endpoint or E31 assumption

B is inverted only to form t=C/B and F_T0/B; the B=0 endpoint is outside the
theorem. The all-zero coefficient equations are not an E31=0 equation, and
E31 is neither imposed nor inverted. Any certificate that uses an E31
relation, silently cancels Delta, or applies an endpoint identity fails this
review's scope check.

### 3.3 Clearing and characteristic

The source clearing gate is P^23*H2^45. The review accepts its removal from
the declared open only after checking both facts: P|Delta and H2 is already
a unit. Integer contents are units only in characteristic zero. The theorem
cannot be silently advertised in positive characteristic, on Delta=0, or on
H2=0.

### 3.4 Resultants versus fibres

The eleven-factor expression is a necessary support cover. Resultant
degree drops, infinity components, and denominator factors are not
contradictions. Each retained factor must have its own exact fibre
certificate:

* p and p-1: GLD102;
* p^2+1, R4, R8, C4: determinant-fibre Macaulay;
* F4 and p^2-2*p+2: direct all-zero-branch localized Macaulay;
* F40: quotient-gcd and nonzero norm.

P and H2 are outside the open, not discharged by a fabricated fibre
identity.

### 3.5 False independence

A python-flint or compact arithmetic replay can be independent of a Singular
resultant/factorization implementation while still sharing the pinned parser,
matrix model, or selected coefficient source. That is useful arithmetic audit
evidence but not an independent graph derivation or an independent rank
bridge. The audit must state this boundary rather than calling every
matching arithmetic result a fully independent proof.

### 3.6 Neutral modular timeout

The modular subset-lift/RREF attempt at the degree-40 leaf timed out without a
verdict. The timeout is neutral: it neither supports nor refutes the exact
F40 route. The only acceptable closure there is the exact quotient-gcd
identity together with the nonzero norm and a clean-clone replay.

## 4. Evidence supporting the verdict

The following evidence is present in tracked files and was replayed from a
detached clean checkout:

1. a primary verifier that reconstructs the normalized chart, the five
   actual minors, the affine-C decomposition, the B-divisibility, the
   all-zero coefficient reduction, and the exact eleven-factor cover;
2. an audit that derives/checks the cover and all factor leaves through a
   materially different arithmetic or checking route, with its limitations
   stated;
3. exact GLD102 fibre dependencies for p=0 and p=1;
4. exact determinant-fibre Macaulay certificates for C4, R8, p^2+1, and R4;
5. exact direct all-zero-branch localized Macaulay certificates for F4 and
   p^2-2*p+2;
6. the exact F40 quotient-gcd relation and nonzero norm;
   the bounded full-replay provenance and certificate record explicit
   `GLD103_FACTOR_MATRIX_INVERSE=1` and
   `GLD103_FACTOR_NO_FINAL_INVERSE=1`, rather than relying on defaults;
7. a reconciliation showing that every localizer, factor, source identity,
   and hash is the same object in the primary and audit;
8. this negative-scope report preserving all nonclaims in the theorem.

The replay record is
[`GLD103_ALL_ZERO_COEFFICIENT_BRANCH_REPLAY_PROVENANCE.json`](../../claims/arbitrary-order/certificates/GLD103_ALL_ZERO_COEFFICIENT_BRANCH_REPLAY_PROVENANCE.json).
It pins clean runs `gld103-allhash-clean-primary-20260831-v1`,
`gld103-allhash-clean-audit-20260831-v1`, and
`gld103-allhash-clean-compare-20260831-v1`, including their bounded-run
manifests and logs. All three succeeded at the same repaired candidate
commit. The helper's exact comparison log is byte-identical to the earlier
designated comparison replay, but remains outside primary acceptance.

## 5. Final scope and status

This PASS certifies only the GLD103 all-zero coefficient leaf on
the normalized arbitrary-a chart and the open D(B*H2*Delta). It does not
certify pivot branches, the B=0 endpoint, the E31 wall/equation, Delta=0,
H2=0, other charts/components/sources/roots/orders, physical incidence, or a
global Krenn--Gu resolution. No review outcome here changes the global
status from **UNRESOLVED**.
