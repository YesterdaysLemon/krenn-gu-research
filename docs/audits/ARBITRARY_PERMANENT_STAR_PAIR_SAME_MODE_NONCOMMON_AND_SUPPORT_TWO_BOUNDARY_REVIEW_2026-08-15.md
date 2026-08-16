# Hostile review of the star-pair same-mode noncommon and support-two boundary

## Verdict and exact scope

**PASS, for the displayed `(4,1)` star frame, pointwise,
characteristic-zero, full-`Delta_3` scope.**  The exceptional-pair case
split, common-kernel rigidity, legal single-slot quotient, common-line
propagation, support-one/support-two distinction, full cubic tensor-rank
obstruction, and exact singleton sharpness fixture all survived independent
hostile review.

For this displayed based frame, a local mode can be low for both mixed-factor
projection families only on their common ambient line

```text
N=K(x_1+x_2).
```

The occurrence must be singleton-supported at local colour `0` or `1`, and
it forces a different local mode to contain

```text
Q=K(x_2+x_3)
```

singleton-supported at colour `2`.  The resulting singleton `N/Q` boundary
is **OPEN**.  The theorem does not exclude distinct-mode exceptional
incidences, transport the argument to every based representative of the
unbased `(4,1)` orbit, treat the `(3,1)` orbit, prove unrestricted
`P_6 -> Delta_3` nonrestriction, or resolve the prize problem.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

Reviewed frozen package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_STAR_PAIR_SAME_MODE_NONCOMMON_AND_SUPPORT_TWO_BOUNDARY_THEOREM.md
  verify_arbitrary_permanent_star_pair_same_mode_noncommon_and_support_two_boundary.py
  audit_arbitrary_permanent_star_pair_same_mode_noncommon_and_support_two_boundary.py
```

Load-bearing committed predecessors replayed in this review:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_STAR_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
  ARBITRARY_PERMANENT_STAR_TRIANGLE_EXCEPTIONAL_COMPANION_PROPAGATION_THEOREM.md
```

The first supplies the local rank floor, the two three-line exceptional
sets, and the support bound.  The second supplies an independently reviewed
version of the all-support quotient propagation lemma, including the exact
full-contraction formula and the countermodel to the invalid scalar-only
second-contraction shortcut.

## 1. Exhausting the same-mode exceptional pairs

The kernel-support predecessor gives

```text
Phi_1: N=x_1+x_2, B_0=x_0+x_2, C_0=x_0-x_1,
Phi_2: N=x_1+x_2, B_1=x_0+x_3, C_1=x_0+x_1+x_2+x_3,
rank(Phi_k|L_t)>=2.
```

Every restricted kernel therefore has dimension at most one.  If a local
plane containing `N` also contained a noncommon line from either family,
the other family's ambient kernel intersection would contain two
independent lines.  This excludes exactly

```text
(N,B_1), (N,C_1), (B_0,N), (C_0,N).
```

The only unclassified pairs are the four noncommon/noncommon pairs and
`(N,N)`.  Thus the line-pair split is exhaustive; no orbit symmetry or
realizability assumption is hidden in it.

## 2. Legal `Theta` quotient for all four noncommon pairs

For independent displayed generators

```text
p in {B_0,C_0}, q in {B_1,C_1}
```

in the same local mode, define the single-slot contraction map on the other
three modes

```text
Theta:R^* -> three-mode tensors,
Theta(ell)=T_(x_4x_5 ell),
Q=ker Theta.
```

The two zero mixed targets put the independent residuals

```text
g_1=(1,1,-1,1), g_2=(-1,1,-1,1)
```

in `Q`.  If `I` is the set of nonzero local coordinate rows on
`span{p,q}`, injectivity gives `|I|>=2`.  Each colour in `I` contributes a
nonzero independent coordinate cube to `im Theta`, so

```text
rank Theta>=|I|, dim Q<=4-|I|.
```

Since `span{g_1,g_2} subset Q`, necessarily `|I|=2` and
`Q=span{g_1,g_2}`.  This is the complete dimension gate.

The quotient map with that kernel is

```text
pi(w)=(w_1+w_2,-w_1+w_3).
```

Independent contraction reproduced the diagonal table

```text
line       pi B_(d_0)       pi B_(d_1)       pi B_(d_2)

B_0             0               (-2,2)            (0,2)
C_0           (2,-2)              0                (0,2)
B_1           (2,-2)              0                (0,2)
C_1             0               (-2,2)            (0,2).
```

For `(B_0,C_1)` and `(C_0,B_1)`, the two live quotient columns agree and
force the two local coefficient vectors to agree, contradicting independence
of the ambient generators.  For `(B_0,B_1)` and `(C_0,C_1)`, each of the
three possible zero coordinate rows exposes a nonzero entry in its matching
diagonal quotient column.  All four noncommon pairs are therefore excluded.

Only one vector from the shared local plane is inserted at a time.  The
proof never puts `p` and `q` into two tensor slots, so no same-slot double
contraction occurs.

## 3. Common-line propagation for support one or two

Contracting with `N` leaves only

```text
h_0=(1,-1,-1,1), h_1=(-1,-1,-1,1),
H=ann(h_0,h_1)={(0,u,v,u+v)}.
```

The existence of a companion in a distinct local mode was rederived rather
than inferred from the computer output.  If all three remaining local
planes missed `H`, they would embed as three-planes in

```text
W=(R/H) direct-sum A, dim W=4,
```

and the correct vector-valued contracted tensor would be

```text
C(y,z,w)=r(y)J(a(z),a(w))+r(z)J(a(y),a(w))
                         +r(w)J(a(y),a(z)).
```

Fixing differently coloured vectors in two modes gives a map `W -> R/H`
that kills the third embedded three-plane and hence has rank at most one.
On the two-dimensional `R/H` summand it is scalar multiplication by the
associated `J`-pairing.  A nonzero pairing would give rank two, so all
cross-colour pairings vanish.

For singleton support, a surviving diagonal contains a nonzero same-colour
pairing after permuting the remaining modes.  In the third mode, each
off-colour vector has zero `R/H` part and lies in the same one-dimensional
orthogonal line in `A`; those two vectors are dependent, contradicting the
local triple's independence.

For support two, both supported colours are active.  The two-dimensional
cross-orthogonality lemma forces every `A`-column at the third colour to
vanish in all three remaining modes.  The original pure target at that
third colour would then have only the removed mode available to supply
`x_4,x_5`.  Since the two factors must come from distinct multilinear slots,
that coefficient vanishes, contradicting its nonzero target scalar.

Thus a distinct mode contains nonzero `q=(0,u,v,u+v) in H`.  The exact
single-contraction identity

```text
2B_(m_1)q-B_(d_0)q+B_(d_1)q=0
```

kills its colour-`0` and colour-`1` coordinates.  Its remaining colour-`2`
coordinate is nonzero, and

```text
uB_(d_2)q=(u+v)(B_(m_1)q+B_(m_2)q)
```

then gives `u=0`.  Hence `q` is a nonzero multiple of `Q=x_2+x_3`, at
colour `2`.  No division by `u`, `u+v`, or another unproved parameter is
used, and the argument applies equally to singleton and support-two `N`.

## 4. Full cubic-rank exclusion of support-two `N/N`

Assume `N` has support `{0,1}` in mode `a`, and let the propagated `Q` at
colour `2` lie in mode `b`.  On the two remaining modes `c,d`, define the
full symmetric trilinear polarization

```text
P_x=pol(x_0x_4x_5).
```

The `d_2` contraction by `Q` and the `d_0,d_1` contractions by `N`, using
`2x_0=h_0-h_1`, give the complete identities

```text
P_x|_(L_a,L_c,L_d)=mu_2 E_222,
P_x|_(L_b,L_c,L_d)=mu_0 E_000+mu_1 E_111,
mu_0mu_1mu_2!=0.
```

Therefore the slice images of `y_(a,2),y_(b,0),y_(b,1)` are independent
nonzero multiples of `E_22,E_00,E_11`.  Those three ambient vectors span a
three-space `Y`, and the restriction to `Y x L_c x L_d` is a weighted
`Delta_3`.

Because weighted `Delta_3` is concise, the coordinate evaluations

```text
Y -> span{x_0,x_4,x_5},
L_c -> span{x_0,x_4,x_5},
L_d -> span{x_0,x_4,x_5}
```

are isomorphisms.  The same restriction would consequently be
`GL_3^3`-equivalent to `pol(XUV)`.  But the first-mode slice space of that
tensor is

```text
span{sym(UV),sym(XV),sym(XU)}.
```

A general slice is

```text
[[0,c,b],[c,0,a],[b,a,0]],
```

whose three principal two-minors are `-c^2,-b^2,-a^2`.  Over a
characteristic-zero field, rank at most one forces `a=b=c=0`.  Since the
tensor is concise, a three-term tensor-rank decomposition would isolate
three nonzero rank-one matrices in this slice space, impossible.  Thus
`rank(pol(XUV))>3`, while weighted `Delta_3` has rank three.

This is the decisive support-two contradiction.  It retains all three
polarization summands and all three tensor modes.  It does **not** replace a
second contraction by a scalar multiple of an aggregate pairing matrix.
The predecessor's exact countermodel to that scalar-only replacement was
replayed and still gives full contraction `1` versus scalar-only value `0`.
The new package therefore fully retracts that failed shortcut rather than
quietly reusing it.

## 5. Singleton sharpness and the accepted open boundary

The rational four-mode fixture was evaluated from the displayed columns
using independent square-free coefficient extraction.  Every local triple
has rank three, and both projection profiles are exactly

```text
(2,2,2,3).
```

It has `y_(a,0)=N` and `y_(b,2)=Q`.  All cubic slices forced by those two
singleton incidences hold:

```text
P_r|_(L_a,L_c,L_d)=0,
P_(x_0)|_(L_a,L_c,L_d)=E_222,
P_(h_1)|_(L_b,L_c,L_d)=0,
P_(x_0)|_(L_b,L_c,L_d)=E_000,
```

up to the harmless nonzero target normalizations.  These are precisely the
full three-mode consequences of singleton `N` at colour `0` and singleton
`Q` at colour `2`.

The fixture is not a full extension.  Direct exact evaluation gives

```text
T_(d_1)(1,1,1,1)=0, required nonzero,
T_(m_1)(1,0,0,0)=3, required zero.
```

It is therefore neither an extension nor a counterexample to the
conjecture.  It proves only that the propagated singleton slices and local
rank floors do not by themselves close the residual.  Uncontracted target
entries or a genuinely stronger invariant are still required.

Accepted boundary:

```text
same-mode common/noncommon pairs:                       EXCLUDED;
same-mode four noncommon/noncommon pairs:               EXCLUDED;
same-mode N/N with support two:                         EXCLUDED;
same-mode N/N with singleton support:                   OPEN;
singleton N forces distinct-mode singleton Q:           PROVED;
distinct-mode exceptional incidences:                   OPEN;
all based frames in the unbased (4,1) orbit:             NOT TREATED;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

## 6. Field, implementation independence, and replay

The written proof uses finite-dimensional rank, exact nonzero target
scalars, nondegeneracy of the two-dimensional form `J`, and characteristic
zero.  It uses no positivity, topology, numerical approximation, algebraic
closure, or finite-field-to-characteristic-zero inference.  Every
double-contraction statement used in propagation involves distinct local
modes; the noncommon quotient uses only one contraction in the shared mode.

The primary verifier reconstructs the pair, ambient kernels, contraction
table, quotient cases, propagation identities, cubic slice obstruction,
and rational fixture with exact SymPy arithmetic.  The independent audit
imports neither SymPy nor the primary verifier.  It rebuilds the quadratic
cores from square-free edge dictionaries, uses standalone `Fraction` row
reduction, and independently evaluates the cubic slices and uncontracted
target failures.  The `F_3,F_5` enumerations audit the finite
cross-orthogonality case table only; the written field-linear argument is
the characteristic-zero proof.

Focused final replay passed at base commit
`76240ca4becc1b58b9803ac1ec6a4db159c07d3c`:

```text
new primary exact verifier:                       PASS;
new independent no-import audit:                 PASS;
star kernel-boundary primary/audit:               PASS/PASS;
star--triangle companion primary/audit:           PASS/PASS;
py_compile on both new Python files:              PASS;
Ruff on both new Python files:                    PASS;
git diff --check before adding this review:       PASS.
```

## Final reviewed hashes

```text
new theorem:
27AA460A9846A3568F3160DF3F6A03C798E87696D1A6E22900F13F8A76EF5AD9

new primary verifier:
0D24DC727902A18824B5D5470542F5BDF7E87FDAB4C5D5FEBE5C439CCE4FFAEA

new independent audit:
E849C2F5A3D0A14414156F70DC7A58CF62B332585A4271268EB54B705719F543

star kernel-boundary theorem:
2B44641806EEE9B14D2F9DCC692C2E8E1CB9917832A9C2FD9E658243ACFE51F5

star kernel-boundary primary verifier:
73406FF9C62A2113341BBC97E36E2E4F4151CF399E72EEBFD831A05944744124

star kernel-boundary independent audit:
0D4F649C78577158E39577FB5CBDDA1A0057534E75A803F1EB73F25726DA5721

star--triangle companion theorem:
9C70842573B3DD02BE5AC9CC65B08047AF0C6877892EA816A5D89B2024ED36A3

star--triangle companion primary verifier:
97177FE5D7A44821428AAED34707FAD30490D50D80163609A28FB3AE7BE663F0

star--triangle companion independent audit:
9DB62582D752C85F2E7AE8343EC806B95786C5693466ECFB3666C5F838A35289
```
