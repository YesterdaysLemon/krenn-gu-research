# Self-review of the residual second-root-coloop complementary-`y` localization

## Review verdict

The localization is supported.  S2BG removes `s=t`.  When the coordinate
endpoint equals `s`, S2BF directly forces `y_s=0`.  When the endpoint is the
other complementary coordinate, assuming `y_s!=0` activates the opposite
S2BF projective factor and produces the generalized same-third-row table
excluded in S2BG.  Hence `y` is always the coordinate complementary to
`s,t`.

This is a localization, not an endpoint exclusion.  The surviving endpoint
charts and all other stated global branches remain open.  Global Krenn--Gu
remains **UNRESOLVED**.

## Case-cover audit

S2BG proves `s in {j,k}` and S2BE proves `w in {e_j,e_k}`.  For fixed `s`,
there are exactly two endpoint positions:

1. `w=e_s`;
2. `w=e_u`, where `{s,u,t}={0,1,2}`.

No third endpoint or `s=t` chart is omitted.

In the first case, the S2BF alternative is `y_s=0` or `z_s=w_s=0`.
The second branch is impossible because `w_s!=0`.  With `y_t=0` and
`dim span(y,e_t)=2`, only the nonzero `e_u` coordinate remains.

## Nontrivial endpoint audit

In the second case `w=e_u`, suppose `y_s!=0`.  S2BF then forces
`z_s=w_s=0`.  Since `z,w` are independent, they form a basis of
`e_s^perp`.

As the determinant-pencil direction varies, the normal `kappa z-hw`
traverses every line of `e_s^perp`.  One can therefore avoid `kappa=0` and
the two coordinate annihilator lines.  This uses only that the
characteristic-zero field is infinite.

At the chosen direction, `L_P=kappa y_s` is nonzero, so the proof uses the
actual coordinate lifts of `P_delta`; it does not replace them by pure root
coordinates.  The `s` components of those lifts make no target contribution
because `alpha_s=0`.  The full table is

```text
per(r_a,p(beta^b),q(gamma_*))
 =delta_(a,b)(gamma_*)_aT_a,
per(r_a,p(beta^b),q_s)=0,
```

for `a,b in {u,t}`.  Both target coefficients are nonzero.

S2BF's common-space construction applies pointwise to this pencil member and
gives a nonzero middle-plane intersection.  S2BC injectivity prevents any
plane collapse.  The hypotheses of S2BG Lemma 1 are therefore met exactly;
no stronger conclusion from the distinguished `alpha_s` coloop is imported.

## Replay independence

The primary replay constructs symbolic normals, actual coordinate lifts, and
all eight target cells with SymPy.  The independent audit imports no
repository module or third-party package and reconstructs the table with a
separately chosen rational direction and `fractions.Fraction` arithmetic.
These scripts replay the displayed identities; the finite-avoidance argument
and the already independently certified S2BG lemma are the proof.

No new certificate is claimed.  Reusing S2BG is a mathematical dependency,
not a second supposedly independent implementation of that lemma.

## Remaining obligations

The exact residual statement is

```text
s in {j,k},
y proportional to the other coordinate in {j,k},
w proportional to e_j or e_k,
with the remaining S2BF z constraints:              OPEN.
```

The endpoint charts, three third-root and two complementary first-root
coloops, lower joint rank, other physical components and pole strata, higher
orders, and global resolution remain open.  Global status stays
**UNRESOLVED**.
