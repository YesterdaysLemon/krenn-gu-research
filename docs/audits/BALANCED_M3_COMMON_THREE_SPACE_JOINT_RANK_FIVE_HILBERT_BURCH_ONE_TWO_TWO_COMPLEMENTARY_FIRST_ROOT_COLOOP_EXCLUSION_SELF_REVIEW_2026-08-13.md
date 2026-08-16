# Self-review: `(1,2,2)` complementary first-root-coloop exclusion

Date: 2026-08-13

## Reviewed claim

The theorem excludes exactly the two remaining S2AZ coordinate-coloop
alternatives

```text
N subset {alpha_a=0},                  a!=s,
```

on the normalized, target-consistent physical `m=3` common-three-space
full-sensor stratum with `dim U=3` and `rank H=5`.

Together with S2BB, S2BC, S2BJ, and S2BK, this closes the complete
joint-rank-five Hilbert--Burch `(1,2,2)` profile.  It does not address joint
rank at most four, another physical component, a pole stratum, higher order,
or the global conjecture.  Global status remains `UNRESOLVED`.

## Critical face/divisor distinction

The derivative-zero pencil uses

```text
alpha_s=0,
```

not the selected divisor `alpha_a=0`.  This distinction was explicitly
caught during adversarial drafting and corrected before the package was
staged.

The selected divisor instead gives the two-plane

```text
C=H^T(L intersect {alpha_a=0}).
```

The derivative-zero face has first row plane

```text
R=rho(e_s^perp)=span(r_a,r_b),
```

where `b` is the third colour.  The pure root covector `e_b^*` lies in both
`L` and `alpha_a=0`, so `r_b in C`.  This is the nonzero intersection row
needed by the inherited arbitrary-intersection lemmas.  No claim that
`r_a in C` or `R subset C` is made.

## Pencil and gate audit

For every projective direction `delta=[h:kappa]`, the planes

```text
P_delta: kappa beta(y)-h mu beta_t=0,
Q_delta: kappa gamma(z)-h gamma(w)=0
```

make the determinant in the first component of the derivative transpose
zero.  The other two components vanish because the face has `alpha_s=0`.
Thus the target identity is complete on
`e_s^perp x P_delta x Q_delta`.

The evaluation-kernel rows of both partner planes are pure root covectors
in `L intersect {alpha_a=0}`.  Representatives with opposite evaluation
pairs have sum in that same space.  Hence both partner planes lie in

```text
S_delta=C+span(p_delta),               dim S_delta<=3.
```

The face plane `R` meets `S_delta` in at least `r_b`.  Injectivity of all
three row maps preserves every plane and intersection row.

Projection to the two target colours different from `s` has the exact
gates

```text
L_P=kappa y_s-h mu delta_(s,t),
L_Q=kappa z_s-h w_s.
```

When both are nonzero, the complete table is a binary diagonal frame with
two planes in `S_delta` and the third intersecting it.  S2BF Lemma 1 applies
after a permanent-argument permutation.  Its 28-family certificate is
pinned at
`0a92e61cef0b3db7940c68ea6e24bab4befb5dc1bd137ada581d0dbde4b9e0ca`.

Vanishing of the gate product at every projective point is promoted to a
polynomial identity only because the characteristic-zero field is infinite.
Integral-domain factorization gives exactly

```text
A: s!=t and y_s=0,
B: z_s=w_s=0.
```

No pointwise choice of a different factor is treated as a global fork.

## One-sided degeneration audit

Under `A` alone, the active second-root row has both complementary target
coordinates while the third-root plane has coordinate lifts.  The two
targets share that active second row.  Under `B` alone, the symmetric table
shares the active third row.

In both cases the two partner planes lie in `S_delta`, and `r_b` is one
indexed row of the possibly escaping first plane.  After permuting permanent
arguments, the table is exactly S2BE Lemma 1, including its all-in-space
boundary.  Its 21-family certificate is pinned at
`e822cb443173acbab3604d6e3e28afaf7fd99a3e306731e21c7c7bc5023ac5fc`.
Therefore neither one-sided degeneration survives.

## Common degeneration and boundary audit

Under both `A` and `B`, generic pencil rows give

```text
r_b,p_s,q_s,p_*+q_* in C.
```

The only nonzero binary cells are the fully transverse targets at
`(r_a,p_*,q_*)` and `(r_b,p_*,q_*)`.

If `p_* in C`, then `q_* in C` and both partner planes equal `C`.
Permanent symmetry aligns the inactive partner rows.  The two active values
then lie in the image of the single square map
`per(-,p_*,p_*)|R`, contradicting S2AL tangent-line separation.

If `p_* notin C`, put `S=C+span(p_*)`.  If `r_a in S`, all three row planes
lie in a three-space and S2BC's same-pair lemma applies.  Otherwise
`R intersect S=span(r_b)`, so the four-dimensional normal form is exact.

## Exhaustive five-case cover

In the proper-intersection branch, normalize

```text
C=<e0,e1>,            p_*=e2,            r_a=e3,
q_*=-e2+c0e0+c1e1.
```

Injectivity makes the inactive rows `p_s,q_s` nonzero lines of `C`.

- If the lines agree, normalize both to `e0`; the stabilizer has exactly two
  orbits for `r_b`: `e0` and `e1`.
- If they differ, normalize them to `e0,e1`; the diagonal stabilizer has
  exactly three nonzero support types for `r_b`: `e0`, `e1`, `e0+e1`.

Thus `2+3=5` cases exhaust the orbit.  The parameters `c0,c1` remain free in
the full polynomial ring.  No division, nonzero-parameter assumption,
sample, saturation, or missing coincidence boundary occurs.

An earlier exploratory atlas kept two inactive lines independently
parametrized relative to a fixed `r_b`; its broad Gröbner batch timed out.
That timeout is not used as evidence.  The final five-case orbit quotient is
proved by the line-incidence split above, and every leaf has a durable unit
identity.

## Certificate and independence audit

The new certificate contains five rational Nullstellensatz identities and
5,928 sparse multiplier terms.  Its SHA-256 is

```text
10ce1216ed2360159eb4709140eabe4db1c51ad509f340ac137300a636583088.
```

The primary replay reconstructs all 64 cubic generators per case with
SymPy.  The independent audit imports no repository module or third-party
package, reverses all 26 variables, rebuilds each polarized permanent with
standard-library `Fraction` sparse arithmetic, and verifies that every
multiplier sum is exactly one.  Both programs separately reconstruct the
one-sided target tables and recompute the inherited certificate pins.

The optional Singular 4.x generator was rerun byte-for-byte before the
repository gate.  Regeneration is not required for proof replay.

## Verdict

Both complementary first-root coordinate coloops are impossible in exact
characteristic zero.  The complete joint-rank-five Hilbert--Burch `(1,2,2)`
profile is closed.  Every wider obligation listed above remains open, and
the global conjecture remains `UNRESOLVED`.
