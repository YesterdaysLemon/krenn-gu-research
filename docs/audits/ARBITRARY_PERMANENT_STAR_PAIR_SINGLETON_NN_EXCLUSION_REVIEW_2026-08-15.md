# Hostile review of the star-pair singleton `N/N` exclusion

## Verdict and exact scope

**PASS, for the displayed `(4,1)` star frame, pointwise,
characteristic-zero, full-`Delta_3` scope.**  The forced `E`-projection
slices, rank-two/rank-three exhaustion, hyperbolic-annihilator lemma, exact
four-slot factorizations, both singleton colours, and star-core
contradiction all survived independent hostile review.

Together with its predecessor, the theorem excludes every local plane that
is rank two for both displayed star mixed-factor projections.  This is not
a full exclusion of the star pair: low modes for the two projection
families may occur in distinct local slots.  The theorem does not classify
those distinct-mode incidences, transport to every based representative of
the unbased `(4,1)` orbit, treat the `(3,1)` orbit, prove unrestricted
`P_6 -> Delta_3` nonrestriction, or resolve the prize problem.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

Reviewed frozen package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_STAR_PAIR_SINGLETON_NN_EXCLUSION_THEOREM.md
  verify_arbitrary_permanent_star_pair_singleton_nn_exclusion.py
  audit_arbitrary_permanent_star_pair_singleton_nn_exclusion.py
```

Load-bearing committed predecessors replayed in this review:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_STAR_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
  ARBITRARY_PERMANENT_STAR_PAIR_SAME_MODE_NONCOMMON_AND_SUPPORT_TWO_BOUNDARY_THEOREM.md
```

The predecessors reduce the same-mode boundary to a common line

```text
N=K(x_1+x_2)
```

singleton-supported at a colour `s in {0,1}`, and force a distinct mode to
contain

```text
Q=K(x_2+x_3)
```

singleton-supported at colour `2`.  All common/noncommon,
noncommon/noncommon, and support-two `N/N` cases were already excluded.

## 1. Reconstructing the two forced `E` slices

Let

```text
E=span{X,U,V}=span{x_0,x_4,x_5},
P=pol(XUV),
S(e)_(kl)=P(e,bar(y_(c,k)),bar(y_(d,l))).
```

Here `bar(y)` is the evaluation projection to the three displayed
coordinates, not the ambient vector itself.  Independent contraction of
the five star cores reproduced

```text
B_(m_1)N=B_(m_2)N=B_(d_2)N=0,
B_(d_0)N=h_0=(1,-1,-1,1),
B_(d_1)N=h_1=(-1,-1,-1,1),
B_(d_2)Q=2x_0,
2x_0=h_0-h_1.
```

Contracting `Q` in its distinct mode and using its colour-`2` singleton
support gives

```text
S(bar(y_(a,i)))=rho_2 delta_(i,2) E_22, rho_2!=0.
```

Contracting `N` in its own mode gives

```text
S(bar(y_(b,j)))=rho_s delta_(j,s) E_ss, rho_s!=0.
```

For `s=0`, the `h_0` target is live and the `h_1` target is zero.  For
`s=1`, the `h_0` target is zero and the `h_1` target is live; the minus sign
in `2x_0=h_0-h_1` changes only the nonzero scalar.  Thus both singleton
colours are covered without an unstated symmetry.

Since `E_ss,E_22` are independent and `dim E=3`, exactly two cases remain:

```text
rank S=2 or rank S=3.
```

If `t` is the other colour in `{0,1}`, the same forced equations give

```text
S(bar(y_(a,t)))=S(bar(y_(b,t)))=0.
```

No target scalar is normalized, and no zero coefficient is divided out.

## 2. Exact star-core and annihilator lemmas

Direct reconstruction from the square-free star cores gives

```text
g_(d_0)-g_(d_1)-2g_(m_1)=x_0(x_1+x_2-x_3).
```

Therefore, for two vectors whose `x_0` coordinates vanish,

```text
g_(d_0)(p,q)-g_(d_1)(p,q)=2g_(m_1)(p,q).
```

This identity is polynomial and field-linear; it is not a numerical or
generic-point observation.

For the rank-two case, write

```text
kappa(c,d)=P(-,c,d).
```

For fixed `d=(X,U,V)`, the map `c -> kappa(c,d)` has matrix

```text
M(d)=[[0,V,U],[V,0,X],[U,X,0]].
```

Its three principal two-minors are

```text
-V^2, -U^2, -X^2.
```

If `d` is nonzero, at least one of these minors is nonzero over a
characteristic-zero field.  Hence `rank M(d)>=2`, and either the left or
right annihilator of a nonzero vector has dimension at most one.  This
proof explicitly includes vectors with one or two zero coordinates and
isotropic vectors for the hyperbolic `U,V` pairing.  It does not divide by
`X`, `U`, `V`, or `J(d,d)`.

The independent finite-field stress audit checked the same claim for all
nonzero vectors and every independent vector pair over `F_3` and `F_5`.
Those scans are corroboration only; the displayed minors are the
characteristic-zero proof.

## 3. Rank-three slice case

If `rank S=3`, then `S` is injective.  The two projected colour-`t`
vectors therefore vanish:

```text
bar(y_(a,t))=bar(y_(b,t))=0.
```

Their ambient vectors may remain nonzero, but they have zero
`x_0,x_4,x_5` coordinates.  At the all-colour-`t` entry, the factors
`x_4,x_5` must consequently come from the two other modes `c,d`, one factor
per multilinear slot.  Exact full polarization gives, for every star
channel `z`,

```text
T_z(t,t,t,t)
=g_z(y_(a,t)^R,y_(b,t)^R)
 J(y_(c,t)^A,y_(d,t)^A).
```

The live `d_t` target makes the common `J` factor and the `g_(d_t)` factor
nonzero.  The zero `m_1` and `d_(1-t)` targets make the corresponding core
factors zero.  Both first vectors lie on `x_0=0`, so the star-core identity
then makes `g_(d_t)` zero as well, a contradiction.

The two singleton colours are genuinely separate specializations:

```text
s=0, t=1: g_(m_1)=g_(d_0)=0 forces g_(d_1)=0;
s=1, t=0: g_(m_1)=g_(d_1)=0 forces g_(d_0)=0.
```

## 4. Rank-two slice case

If `rank S=2`, its image is exactly

```text
span{E_ss,E_22}.
```

Put `C_i=bar(y_(c,i))` and `D_j=bar(y_(d,j))`.  Every other matrix entry
vanishes identically, while the two displayed diagonal entries are live:

```text
kappa(C_i,D_j)=0 off (s,s),(2,2),
kappa(C_s,D_s)!=0,
kappa(C_2,D_2)!=0.
```

The cross zeros prove that `D_s,D_2` are independent.  If they were
proportional, the nonzero same-colour pairing at `(s,s)` would contradict
the zero cross cell `(s,2)`; neither vector can be zero because the
corresponding live cell is nonzero.  Symmetrically, `C_s,C_2` are
independent.

The vector `C_t` annihilates both independent vectors `D_s,D_2`.  The
annihilator lemma rules this out unless `C_t=0`.  Applying the symmetric
argument gives `D_t=0`.  Thus

```text
bar(y_(c,t))=bar(y_(d,t))=0.
```

At the all-colour-`t` entry, the two `A` factors now have to come from
`a,b`, and exact full polarization gives

```text
T_z(t,t,t,t)
=J(y_(a,t)^A,y_(b,t)^A)
 g_z(y_(c,t)^R,y_(d,t)^R).
```

The live `d_t` target makes the common `J` factor nonzero.  Cancelling it
against the zero `m_1,d_(1-t)` targets and applying the same core identity
to the `c,d` pair contradicts the live `d_t` factor.  This closes the
rank-two branch, including every zero-coordinate and isotropic subcase.

## 5. Full polarization and the rejected scalar shortcut

The two factorizations above are not instances of the previously refuted
rule that an arbitrary second contraction is a scalar multiple of an
aggregate `A`-pairing matrix.  They are used only after two complete tensor
shores have been proved to have zero `(x_0,x_4,x_5)` projection.  At that
point multilinearity forces `x_4,x_5` onto the opposite two shores and the
quadratic core onto the projected-zero pair; all other polarization
summands vanish for explicit coordinate reasons.

The primary verifier checks both symbolic factorizations in the full
six-variable square-free algebra for all five star cores.  The independent
audit checks `1620` basis entries for each shore ordering.  Neither proof
contracts two vectors from one local mode, and no aggregate matrix or
unproved nonzero scalar is introduced.

## 6. Predecessor sharpness fixture

The predecessor's exact rational singleton fixture was replayed.  In its
`s=0,t=1` orientation, the slice images of the `E` basis `(X,U,V)` are

```text
S(X)=E_00,
S(U)=E_22,
S(V)=E_20.
```

They are independent, so the fixture lies in the rank-three case exactly
as claimed.  Its colour-`1` vectors in modes `a,b` have zero
`x_0,x_4,x_5` projection.  Exact full-quartic evaluation at the all-colour
`1` entry gives

```text
T_(m_1)(1,1,1,1)=0,
T_(d_0)(1,1,1,1)=0,
T_(d_1)(1,1,1,1)=0,
```

so the live `d_1` target fails exactly at the new theorem's obstruction.
The previously displayed off-target value `T_(m_1)(1,0,0,0)=3` also
remains.  The fixture is a sharpness witness for the earlier slice method,
not a full extension and not a counterexample.

## 7. Accepted boundary and replay

```text
same-mode common/noncommon star lows:                   EXCLUDED;
same-mode noncommon/noncommon star lows:                EXCLUDED;
same-mode support-two N/N:                              EXCLUDED;
same-mode singleton N/N:                               EXCLUDED;
every same-mode low for both displayed star families:  EXCLUDED;
distinct-mode exceptional incidences:                  OPEN;
all based frames in the unbased (4,1) orbit:            NOT TREATED;
unrestricted P_6 -> Delta_3:                           UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.
```

The final current-byte replay passed at base commit
`2e6c74d36fda60d6b3428047325c5398053b247c`:

```text
new primary exact verifier:                       PASS;
new independent no-import audit:                 PASS;
star same-mode-boundary primary/audit:            PASS/PASS;
star kernel-support primary/audit:                PASS/PASS;
predecessor rational fixture replay:              PASS;
py_compile on both new Python files:              PASS;
Ruff on both new Python files:                    PASS;
git diff --check before adding this review:       PASS.
```

The primary uses exact SymPy arithmetic.  The audit imports neither SymPy
nor the primary verifier; it rebuilds the cores from edge dictionaries,
uses standalone rational reduction, verifies the annihilator minors
formally, and exhausts both full-quartic factorizations on basis vectors.

## Final reviewed hashes

```text
new theorem:
EA29D52F17100A7D99F5A56254309B69BC21744E5C2BAFE78A981F19097B4693

new primary verifier:
CED670F3D48B567CBC62B4759718E056E21A5E21CB1F42DDA85426F502A4B0FE

new independent audit:
8ADCB1EAF9B4E3C5B140463AEC89615DBE323A385DC3893030F57C10ECAFA031

star same-mode-boundary theorem:
27AA460A9846A3568F3160DF3F6A03C798E87696D1A6E22900F13F8A76EF5AD9

star same-mode-boundary primary verifier:
0D24DC727902A18824B5D5470542F5BDF7E87FDAB4C5D5FEBE5C439CCE4FFAEA

star same-mode-boundary independent audit:
E849C2F5A3D0A14414156F70DC7A58CF62B332585A4271268EB54B705719F543

star kernel-support theorem:
2B44641806EEE9B14D2F9DCC692C2E8E1CB9917832A9C2FD9E658243ACFE51F5

star kernel-support primary verifier:
73406FF9C62A2113341BBC97E36E2E4F4151CF399E72EEBFD831A05944744124

star kernel-support independent audit:
0D4F649C78577158E39577FB5CBDDA1A0057534E75A803F1EB73F25726DA5721
```
