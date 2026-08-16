# Hostile review of the triangle-pair same-mode two-low exclusion

## Verdict and exact scope

**PASS, for the displayed `(3,1)` triangle frame, pointwise,
characteristic-zero, full-`Delta_3` scope.**  No mathematical,
case-exhaustiveness, contraction-slot, characteristic, dependency, or
implementation blocker survived hostile review.

For this explicit frame, the new package excludes every local plane that
has rank two under both mixed-factor projection families.  The five-line
kernel boundary leaves only the same-mode pairs

```text
N/N, B/S, C/S
```

after rank-nullity, and the new argument closes all three.  This is not a
full exclusion of the triangle pair: exceptional low modes in different
local slots remain open.  It does not transport automatically to another
based frame or to another equality-five orbit.  Unrestricted
`P_6 -> Delta_3` nonrestriction is unknown, and the global Krenn--Gu
conjecture remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_TRIANGLE_PAIR_SAME_MODE_TWO_LOW_EXCLUSION_THEOREM.md
  verify_arbitrary_permanent_triangle_pair_same_mode_two_low_exclusion.py
  audit_arbitrary_permanent_triangle_pair_same_mode_two_low_exclusion.py
```

Load-bearing predecessors replayed during review:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_TRIANGLE_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
  ARBITRARY_PERMANENT_TRIANGLE_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md
  ARBITRARY_PERMANENT_FIXED_PAIR_EXCEPTIONAL_KERNEL_NECESSITY_THEOREM.md
```

The first supplies the rank floor and five exceptional lines, the second
supplies the exact hyperplane/plane permanent-zero classification, and the
third gives an independently reviewed form of the field-linear
one-surviving-diagonal lemma adapted in the propagation step.

## 1. Exhausting the same-mode line pairs

The reviewed predecessor gives

```text
Phi_1 lines: N=x_1+x_2, B=x_0+x_2, C=x_0-x_1,
Phi_2 lines: N=x_1+x_2, S=x_3,
rank(Phi_k|L_t)>=2.
```

The last inequality says that each local intersection with an ambient
projection kernel has dimension at most one.  If a plane containing `N`
also contained any distinct line from the other family's list, then one of
its two kernel intersections would contain two independent lines.  This
excludes `N/S`, `B/N`, and `C/N`.  The common line `N/N` and the two
noncommon pairs `B/S,C/S` are the only cases left.  No orbit symmetry or
realizability assumption is used.

## 2. The legal single-slot `Theta` exclusion

Suppose one local plane contains `p=B` or `C` and `q=S`.  Define

```text
Theta:R^* -> tensors on the other three local modes,
ell |-> T_(x_4x_5 ell),
Q=ker Theta,
R=span{x_0,x_1,x_2,x_3}.
```

Direct single contraction gives

```text
i_p F_2=x_4x_5(x_0-x_1+x_2),
i_q F_1=x_4x_5(-x_0-x_1+x_2).
```

Both mixed target tensors vanish.  The two independent displayed
covectors therefore span a plane `U subset Q`.

The local coordinate rows on `span{p,q}` are, after choosing the relevant
nonzero entries,

```text
q: (beta_0,0,0), beta_0!=0,
B: (alpha_0,alpha_1,0), alpha_1!=0,
C: (alpha_0,0,alpha_2), alpha_2!=0.
```

The second nonzero coefficient is forced because `p,q` are independent.
In either case the two live coordinate rows are independent.  Contracting
the two associated diagonal targets therefore puts two independent
coordinate cubes in `im Theta`, so `rank Theta>=2` and `dim Q<=2`.
Consequently `Q=U`.

The vector

```text
z_0=beta_0 p-alpha_0 q
```

has zero colour-zero coordinate.  Its `D_0` contraction must lie in `Q`,
but its residual covector, up to the harmless factor two, is

```text
beta_0 x_3-alpha_0 x_0.
```

This is not in `U`, whose covectors have zero `x_3` coefficient.  The
nonzero `beta_0` gives the contradiction.

This argument contracts only one vector into the one local slot.  It never
inserts both `p` and `q` into two tensor slots, and it never replaces a
tensor identity by a scalar multiple of a mixed channel.

## 3. Propagation from `N` to another local mode

Contracting a common kernel vector `N` leaves only

```text
D_1=x_4x_5 h_+, D_2=x_4x_5 h_-,
h_+=x_0+x_1+x_2, h_-=x_0-x_1-x_2.
```

Their common residual kernel is

```text
H=span{x_1-x_2,x_3}.
```

Assume, for contradiction, that all three other local planes are disjoint
from `H`.  They inject as three-planes into

```text
(R/H) direct-sum span{x_4,x_5},
```

whose two summands both have dimension two.

If the removed `N` has singleton local support, the two residual covectors
give a standard contraction tensor with exactly one nonzero diagonal.  An
off-diagonal slice kills an injected three-plane, so its rank is at most
one; a nonzero `J` pairing would make its restriction to the two-dimensional
`R/H` summand a rank-two scalar identity.  Thus the cross-colour `J`
pairings vanish.  A nonzero diagonal then forces the two other-colour
vectors in a suitable mode into one `J`-orthogonal line, contradicting
their independence.

If `N` has support `{1,2}`, both diagonal colours are active.  The same
two-dimensional cross-orthogonality argument forces every colour-zero
`x_4,x_5` column in the other three modes to vanish.  In the original
all-colour-zero `D_0` coefficient, at most the removed local mode could
supply an `x_4,x_5` factor.  Since the two distinct factors must be
assigned to distinct multilinear slots, that coefficient is zero,
contrary to `lambda_0!=0`.  The fact that `N` itself is pure `R` is
consistent but is not needed for this last slot count.

Therefore another local plane contains a nonzero vector

```text
q=s(x_1-x_2)+t x_3.
```

Independent contraction gives, after suppressing `x_4x_5`,

```text
F_1=t ell_1-2s x_3,  F_2=-2s x_0,  D_0=2t x_0,
D_1=s ell_1,          D_2=-s ell_1.
```

If `s!=0`, the last two contractions are opposite copies of one tensor but
their exact targets occupy different diagonal colours.  Both corresponding
local coefficients vanish.  The remaining coefficient is colour zero and
nonzero.  The mixed `F_2` equation then kills the `x_0` residual; if
`t!=0`, this contradicts the live `D_0` equation, while if `t=0`, the
identically zero `D_0` residual contradicts it directly.  Hence `s=0`.

The propagated vector is therefore `S=x_3`.  Its zero `D_1,D_2`
contractions force exact singleton support at colour zero.  The propagated
mode is distinct from the original `N` mode.

## 4. The two-low permanent-zero profiles

Assume the original `N` and propagated `S` are the only `Phi_2`-low modes.
The zero `F_2` tensor has two plane images and two hyperplane images in

```text
(z_0,z_1,z_2,z_3)=(x_0,x_4,x_5,ell_2).
```

The exact HHPP predecessor has two exhaustive branches.

In the common-coordinate branch, omission of `z_1` or `z_2` kills all
diagonal tensors, and omission of `z_0` kills `D_0`.  If `z_3` is omitted,
then `ell_1=ell_2-x_0=-x_0` on every local plane and hence

```text
F_1=-D_0/2,
```

contradicting their zero and nonzero targets.

In the exceptional branch, the low images are a coordinate plane `P` and
the highs are

```text
H_+=P direct-sum K(z_i+t z_j),
H_-=P direct-sum K(z_i-t z_j), t!=0.
```

Contracting the singleton `S` in its one legal slot requires on
`P x H_+ x H_-`

```text
pol(z_1z_2(z_3-z_0))=0,
pol(z_1z_2z_0)!=0.
```

The complete six-plane check is

```text
P=<z_0,z_1> or <z_0,z_2>: first and second tensors nonzero;
P=<z_0,z_3>:              both tensors zero;
P=<z_1,z_2>:              first contains t-1 and -t-1;
P=<z_1,z_3> or <z_2,z_3>: first contains t and -t,
                                 second tensor zero.
```

For the `z_1,z_2` chart, simultaneous vanishing would require
`t=1=-t`, impossible in characteristic zero.  For the final two charts,
`t!=0` prevents vanishing.  Thus no exceptional profile satisfies both
target requirements.

The primary and audit scripts correctly expose all displayed affine
polynomials.  Their generic polynomial-nonzero loop alone would not rule
out a common special value of `t`; the explicit pair `t-1,-t-1` and the
nonzero-`t` checks above are the load-bearing specialization audit.

## 5. The forced three-low cycle

There must be a third `Phi_2`-low mode.  It cannot contain another `S`:
the legal double contraction of `S` vectors from two distinct modes kills
all five quartics, while their singleton colour-zero coordinates leave a
nonzero `D_0` target.

The new low line is another `N`.  Double contraction of the two `N`
vectors, again in distinct slots, gives

```text
D_1=2x_4x_5, D_2=-2x_4x_5,
F_1=F_2=D_0=0.
```

The `D_1,D_2` targets have different coordinate support.  Their common
remaining pairing tensor must therefore vanish, and the two nonempty
`N` supports are disjoint subsets of `{1,2}`.  They are complementary
singletons.  Pairwise disjointness rules out a third `N`, while the
previous double contraction rules out another `S`.  Up to names, the only
profile is

```text
a: N at colour 1,
b: S at colour 0,
c: N at colour 2,
h: high for Phi_2.
```

The vanishing remaining pairing is the full matrix identity

```text
A_b^T J A_h=0.
```

Mode `b` is high for `Phi_1`, since every possible same-mode low line has
already been excluded; mode `h` is high for `Phi_2`.  Consequently both
`A_b,A_h` are nonzero.  Orthogonality in a nondegenerate two-space forces
both to have rank one:

```text
A_b=u rho_b, A_h=v rho_h, J(u,v)=0,
u,v,rho_b,rho_h nonzero.
```

## 6. The full two-by-two tensor gate

Let `X,Y` be the `h_+,h_-` rows on mode `b`, let `U,V` be those rows on
mode `h`, and let

```text
delta_t=J(A_t(-),v), epsilon_t=J(u,A_t(-)).
```

Contracting `N` once in mode `a` and once, separately, in mode `c` gives
four full three-mode tensor identities.  After reordering tensor factors,
they are

```text
delta_c tensor (X tensor rho_h)
 +epsilon_c tensor (rho_b tensor U) = lambda e_1 tensor E_11,
delta_c tensor (Y tensor rho_h)
 +epsilon_c tensor (rho_b tensor V) =0,

delta_a tensor (X tensor rho_h)
 +epsilon_a tensor (rho_b tensor U) =0,
delta_a tensor (Y tensor rho_h)
 +epsilon_a tensor (rho_b tensor V) =mu e_2 tensor E_22,
```

with `lambda,mu!=0`.  The terms in which `h_+` or `h_-` is supplied by the
`a` or `c` mode and `x_4,x_5` are supplied by `b,h` vanish because the
entire matrix `A_b^T J A_h` is zero.  Thus no polarization summand is
discarded silently.

The pure-`R` kernel columns give

```text
delta_c(e_2)=epsilon_c(e_2)=0,
delta_a(e_1)=epsilon_a(e_1)=0.
```

If `delta_c,epsilon_c` were independent, the second tensor identity would
force both of its two-mode factors to vanish, contradicting the nonzero
fourth identity.  Hence they span one line; the first nonzero identity and
the displayed colour zero force that line to be `Ke_1`.  The symmetric
argument puts `delta_a,epsilon_a` on `Ke_2`.

Writing their scalar rows as `(r_1,r_2)` and `(s_1,s_2)`, and setting

```text
A=X tensor rho_h, B=rho_b tensor U,
C=Y tensor rho_h, D=rho_b tensor V,
```

gives the exact two-by-two system

```text
r_1A+r_2B=lambda E_11, r_1C+r_2D=0,
s_1A+s_2B=0,           s_1C+s_2D=mu E_22.
```

The coefficient rows cannot be proportional: a nonzero right side would
then be proportional to a zero one.  The matrix is invertible.  Solving it
makes `A,B` scalar multiples of `E_11` and `C,D` scalar multiples of
`E_22`.

This is the full tensor gate.  At no point is a tensor replaced by a scalar
multiple of a mixed matrix or an aggregate `M`; the shared rank-one factors
`rho_b,rho_h` remain visible throughout.

## 7. Zero patterns and the final diagonal slice

If both `A,C` were nonzero, their shared nonzero factor `rho_h` would have
to be proportional to both `e_1` and `e_2`.  Similarly, `B,D` cannot both
be nonzero because they share `rho_b`.  Combining these restrictions with
invertibility leaves exactly

```text
diagonal:     r_2=s_1=0,
antidiagonal: r_1=s_2=0.
```

In the diagonal case, `rho_b` is supported at colour two and `rho_h` at
colour one; the `a,c` rows force the same shore/color split.  The
antidiagonal case exchanges the shores.  If `u,v` were dependent, their
orthogonality would make `delta_t,epsilon_t` proportional for every mode,
contradicting either surviving pattern.  Thus `u,v` are an orthogonal basis
of `A`; nondegeneracy makes both self-pairings nonzero, so the row
conditions really do localize every `A_t` column.

In both patterns,

```text
A_a e_0=A_b e_0=A_c e_0=A_h e_0=0.
```

The all-colour-zero coefficient has no supplier for `x_4` or `x_5` in any
slot.  Every displayed quartic therefore vanishes there, whereas the exact
`D_0` target equals `lambda_0!=0`.  This final uncontracted diagonal slice,
not the two `N` contractions alone, closes the cycle.

## 8. Contraction-slot and field audit

Every contraction is legal:

- `p,q,z_0` in the noncommon case are used one at a time in their single
  shared local slot;
- the propagated-line argument contracts one vector in one mode;
- the HHPP argument contracts the singleton `S` once;
- `N/N` and `S/S` double contractions use vectors from two distinct local
  modes;
- the two-by-two gate uses two separate single contractions, one in mode
  `a` and one in mode `c`.

No proof step inserts two vectors from one local plane into different
tensor slots.

Characteristic zero is correctly stated.  The proof uses `2!=0`, the
opposite-parameter HHPP family, the incompatibility of `t-1` and `-t-1`,
and exact divisions by nonzero scalars.  It uses no algebraic closure,
positivity, or extraction of roots.

## 9. Near-survivor and failed shortcut

The exact rational fixture in the theorem has the claimed projection-rank
profile, satisfies the vanishing `A_b^T J A_h` gate, and exactly realizes
both single-`N` target slices.  It nevertheless has zero colour-zero
`x_4,x_5` columns in every mode.  Its singleton-`S` slice contains
off-target `F_1` and `D_0` cells at `(0,1,1)`, so it is not an extension or
a counterexample.

This witness correctly records the methodological failure: the two
single-`N` slices and the rank-one shores do not by themselves close the
branch.  The full all-colour-zero `D_0` slice is indispensable.

Accepted boundary:

```text
triangle same-mode N/noncommon pairs:                 EXCLUDED;
triangle same-mode B/S and C/S:                       EXCLUDED;
triangle same-mode N/N:                               EXCLUDED;
every same-mode cross-family low:                     EXCLUDED;
distinct-mode exceptional incidences:                    OPEN;
unrestricted P_6 -> Delta_3:                          UNKNOWN;
global Krenn--Gu conjecture:                        UNRESOLVED.
```

## 10. Computational replay and independence

The primary verifier uses exact SymPy arithmetic to reconstruct the line
contractions, `Theta` rank gate, propagated pencil, `N/N` and `S/S`
double contractions, six HHPP charts, coefficient zero-pattern split, and
complete polarization of the rational near-survivor.

The no-import audit imports neither the primary verifier nor SymPy.  It
rebuilds the quartics as square-free monomial dictionaries, differentiates
and polarizes them directly, uses a separate exact rational reducer,
represents the HHPP charts by affine coefficient tuples, exhausts the
coefficient split over `F_5,F_7`, and independently replays the fixture.
These computations audit identities and finite case splits; the written
characteristic-zero tensor arguments are the proof.

Focused final replay passed:

```text
new primary exact verifier:                    PASS;
new independent no-import audit:              PASS;
triangle kernel-boundary primary/audit:       PASS/PASS;
triangle two-sided predecessor primary/audit: PASS/PASS;
fixed one-diagonal predecessor primary/audit: PASS/PASS;
py_compile on all replayed scripts:           PASS;
Ruff on all replayed scripts:                 PASS;
git diff --check on tracked changes:          PASS.
```

## Final reviewed hashes

```text
new theorem:
196A46E7B85A332956DB6CCF99BD72F1999E3B8205E774F077C552C70961A155

new primary verifier:
9DDA7DB2F2059A596E242D69834078CE852E70DBB90B450E0775F040394870E5

new independent audit:
4F0B502445D5330421D597CCF674B1F0227E5D14E8DADABFF26253954827BE95

triangle kernel-boundary theorem:
60858DFE1C1C9E11C74662B815E1A4173616C3277E28A25520EDAD97148EBA82

triangle kernel-boundary primary verifier:
67F27BEF7A3C8A071344F6B48BEA265DF2173E839586C988239F039DBB72F8DF

triangle kernel-boundary independent audit:
B0C5DFBC8ED8086BCF5EDAA8665BD57131E2291ED73601A269F35996B973FBA8

triangle two-sided theorem:
C5E8F47B499318595481D84DB75425240BA6A01AD512A92BF923F5FAB56BF485

triangle two-sided primary verifier:
770F21C2D34A5B98CE5820D023405D0A95B3FE167539747E3EFB9EDE4A538153

triangle two-sided independent audit:
14AB3E48905246452B9B02D962D0D5902D543398EA74B0009ACAF12C720D136D

fixed one-diagonal theorem:
2FAB590264EDE5999F55540F2234BE2055637386B978D77469F592F58B004B60

fixed one-diagonal primary verifier:
256D1F4DEB3639E912E41C426E2D28E5FCB384C72DCDB00F9592064D33C904E5

fixed one-diagonal independent audit:
90014EC8E37B0F48F26BD4A9528E235F2FC26D5E757948E34B1744B1B743D6F1
```
