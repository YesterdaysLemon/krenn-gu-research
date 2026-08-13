# Self-review: `(1,2,2)` third-root-coloop exclusion

Date: 2026-08-13

## Reviewed claim

The new theorem excludes exactly the three S2AZ coordinate-coloop
alternatives

```text
N subset {gamma_k=0},                 k=0,1,2,
```

on the normalized, target-consistent physical `m=3` common-three-space
full-sensor stratum with `dim U=3` and `rank H=5`.

It does not exclude the two complementary first-root coloops, joint rank at
most four, another component or pole stratum, any higher order, or the
global conjecture.  Global status remains `UNRESOLVED`.

## Exact dependency audit

The proof uses the following previously proved interfaces.

1. S2AZ gives the gauge, the nine-coordinate coloop fork, the two-plane
   `R=rho(e_s^perp)`, and
   `H^T(L intersect {gamma_k=0})=R` in a selected third-root orientation.
2. The target-contraction arguments already used in S2BA--S2BC make all
   three row maps injective.  This is needed to preserve the three binary
   two-planes and the nonzero intersection row.
3. S2BF Lemma 1 excludes a binary diagonal table when two row planes lie in
   a three-space and the third plane has any nonzero intersection with it.
   Its 28-case certificate pin is
   `0a92e61cef0b3db7940c68ea6e24bab4befb5dc1bd137ada581d0dbde4b9e0ca`.
4. S2BI Lemma 1 excludes a common-active-row table under the same
   two-planes-plus-intersection geometry.  Its 90-case certificate pin is
   `a56242675744f848fc4f747045ce9b2a18c7b32ae2152ca800bd6c654d29e8d1`.
5. S2BB and S2BJ together exclude all three second-root coordinate coloops,
   not merely a generic subset of them.

The focused gate reruns both the primary and independent audits for items 3
and 4.  The new package does not relabel their stored certificates as new
evidence.

## Row-space transfer audit

For `beta_t=0`, the adjusted root covector

```text
(-lambda^(-1)beta(y)e_s^*,beta,0)
```

lies in `L intersect {gamma_k=0}`.  Hence
`p(beta)-beta(y)A` lies in `R`, and the whole plane
`P_t=pi(e_t^perp)` lies in `S=R direct-sum span(A)`.

For `gamma(w)=gamma_k=0`, the adjusted root covector

```text
(-lambda^(-1)gamma(z)e_s^*,0,gamma)
```

lies in the same coloop hyperplane.  Thus
`q(gamma)-gamma(z)A` lies in `R`.  Since two planes in a
three-dimensional covector space meet nontrivially,
`w^perp intersect e_k^perp` supplies a nonzero row of
`Q_w=theta(w^perp)` in `S`.  Injectivity of `theta` is explicitly required;
without it, the intersection line could collapse.

All first-root rows lie in `S`, so `R_t=rho(e_t^perp)` also lies there.
Injectivity makes `R_t`, `P_t`, and `Q_w` genuine two-planes.  The proof uses
only `Q_w intersect S !=0`; it never upgrades that incidence to
`Q_w subset S`.

## Complete-face audit

On `beta_t=gamma(w)=0`, every component of the exact derivative transpose
vanishes.  The complete target equation therefore restricts to

```text
per(r(alpha),p(beta),q(gamma))
 =sum_i alpha_i beta_i gamma_i T_i.
```

There is no sampling step.

If `w_t!=0`, the exact lifts

```text
gamma^i=e_i^*-(w_i/w_t)e_t^*,          i!=t,
```

give all eight cells of the binary diagonal table, not merely its two
nonzero cells.  Permanent symmetry permits the second/third argument
permutation needed to match S2BF Lemma 1.

If `w_t=0` and both complementary coordinates are nonzero, the basis

```text
n=w_b e_a^*-w_a e_b^*,                  e_t^*
```

gives exactly two nonzero cells sharing `q(n)` and six zero cells.  S2BI
allows the escaping plane's intersection line to be its active row, its
zero row, or a generic combination, so no unproved identification of the
intersection line is needed.

## Root-exchange audit

If `w=nu e_v`, exchanging roots two and three sends the kernel to

```text
span{(lambda e_s,z,y),(0,nu e_v,mu e_t)}.
```

This preserves both projected dimensions.  The standard generator gauge
sets the new `v` coordinate of `z` to zero and leaves all new
Hilbert--Burch blocks unchanged.  The old divisor `gamma_k=0` becomes the
new divisor `beta'_k=0` exactly.  The `k=v` case is S2BB and the two
`k!=v` cases are S2BJ.  No assumption that the gauge-fixed pictures were
already beta/gamma symmetric is made.

## Exhaustiveness

The independence of `z,w` implies `w!=0`.  Therefore exactly one of the
following holds:

1. `w_t!=0`;
2. `w_t=0` and both complementary coordinates are nonzero;
3. `w_t=0` and `w` is one complementary coordinate vector.

The three proof sections exclude these cases respectively.  Thus the
support split is exhaustive over every characteristic-zero field.

## Computational independence

The new primary replay uses SymPy to check the coloop adjustments, both
complete face tables, the exact root-exchange gauge, and both certificate
hashes.  The new independent audit imports no repository module and no
third-party package.  It builds its own five-dimensional canonical row
model, Gaussian elimination, face tables, block arrays, and SHA-256 checks
using only `Fraction` and the standard library.

The inherited S2BF and S2BI certificate replays are run separately in both
their primary and independent implementations.  A hash match alone is not
treated as a replay of a Nullstellensatz identity.

## Verdict

The transfer closes all three third-root coordinate-coloop orientations in
exact characteristic zero.  Seven of nine `(1,2,2)` coloop orientations
are now closed.  The two complementary first-root coloops and every wider
open branch remain explicit; the global conjecture remains `UNRESOLVED`.
