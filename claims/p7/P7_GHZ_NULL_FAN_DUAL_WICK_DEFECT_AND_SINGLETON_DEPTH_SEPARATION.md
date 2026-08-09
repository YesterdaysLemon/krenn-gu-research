# GHZ-null fan words, the dual-Wick defect, and singleton-depth separation

## Status

**Exact characteristic-zero target consequence and sharp physical response
boundary.**  The canonical six double blockers have three coordinate-axis
common-null pairs.  Every four-window in the fixed-complement pure Laplace
cover contains blockers from at least two such pairs.  After its pure shore
is fixed, the resulting seven-blocker word is nonmonochromatic.  The GHZ
target therefore vanishes on every one of these graph-side windows.

If a window also has two independent residual-absent/residual-present
companion selectors, its direct and two-residual top responses are both
forced to be zero.  In particular, the tetrahedral fan does not provide a
nonzero direct four-point chart from which to divide and recover the missing
residual scalar.  Its four-point dual-Wick equation instead becomes the
observable, vacuum-free bilinear equation

```text
sum_(e subset W, |e|=2) z_e m_(W minus e)=0.          (1)
```

The same target-nullity holds on the six-double-blocker word, so any legally
synchronized six-point top responses there are also zero.  Thus the
canonical common-null chart does not force a nonzero `m_4` or `m_6`; it lies
on the simultaneous moment-null boundary identified by the vacuum-free
projectivization theorem.

This boundary is sharp at the physical response level.  One honest
seven-port coloured block graph simultaneously satisfies every GHZ-null fan
top equation and every equation (1), while its residual-empty scalar varies
freely.  Its paired one-residual blocker rows vary with that scalar.  Root
singleton companion forms live on different physical edges and do not by
themselves expose these blocker rows.

The result is not a full P7 realization: the response counterfamily does not
satisfy all uncontracted root and mixed-word equations.  Legal marked-star
selection, paired blocker-singleton depths, and a contradiction from (1)
remain **UNKNOWN**.  The P7 restriction problem and the Krenn--Gu conjecture
remain **UNRESOLVED**.

## 1. The canonical common-null directions

Write the canonical blocker profile as

```text
B={t} disjoint union U_0 disjoint union U_1 disjoint union U_2,
t=012,                         |U_c|=2.               (2)
```

Here a blocker in `U_c` is missing pure colour `c`.  Its total root-row span
is the complementary coordinate plane and its simultaneous-kernel line is

```text
K_u=K e_c,                     u in U_c.              (3)
```

For pure colour `c`, the five-column root--blocker base is

```text
B_c=B minus U_c={t} disjoint union A_c,               (4)
```

where `A_c` consists of the four double blockers in the other two pairs.
The fixed-complement Laplace theorem says that, for every two-subset
`S subset A_c`, there is a graph-side clean window

```text
W=U_c union S,
D=B minus W={t} union (A_c minus S),                  (5)
```

with a nonzero pure shore factor.  Evaluate every blocker in `D` at `e_c`
and every blocker `u in W` at its common-null vector `e_mu(u)`, where
`u in U_mu(u)`.

### Theorem 1 (GHZ-nullity of the complete clean-window cover)

Every window (5) evaluates the seven-blocker GHZ diagonal tensor to zero.
This holds for all six windows in each pure colour, hence for all eighteen
colour-tagged graph-side windows.

Proof.  The target blocker tensor is a linear combination of

```text
D_d=e_d^(tensor 7),                    d=0,1,2.       (6)
```

The shore `D` contains the triple blocker `t` evaluated at `e_c`.  Therefore
every term `D_d` with `d!=c` vanishes at `t`.  The set `S` is nonempty and
disjoint from `U_c`, so any `u in S` has `mu(u)!=c` and is evaluated at
`e_mu(u)`.  The remaining term `D_c` vanishes at that blocker.  All three
target terms are zero.

This is a mixed-word equation of the actual GHZ target, not a response
dimension count.  It uses the common total-kernel directions (3); a larger
shore-null space not restricted to those lines would be a different chart.

## 2. The tetrahedral fan is target-null

Relabel

```text
U_1={1,2},             U_2={3,4},
U_0={5,6}.                                             (7)
```

The graph-side fan is

```text
1234, 1256, 1356, 1456.                              (8)
```

The first window is supplied, for example, by pure colour `1`; the other
three are supplied by pure colour `0`.  Their common-null words respectively
contain the axis patterns

```text
1122,       1100,       1200,       1200             (9)
```

up to the order of the four blocker positions.  Each is nonmonochromatic,
so Theorem 1 kills its target coefficient.

Let `I` be the complementary root pair and let

```text
T_I=g_empty tensor C_I+g_Q tensor C_(I union Q)       (10)
```

be its two distinguished companion classes.  The clean shore contracts
these cofactors to

```text
f z_W,                       f m_W,                   (11)

f!=0,
```

with the same shore factor `f`.

### Corollary 2 (independent top selectors force the moment-null chart)

If `g_empty,g_Q` are linearly independent, then on every selected canonical
window

```text
z_W=m_W=0.                                            (12)
```

Proof.  By Theorem 1, contracting the GHZ side of the exact root-pair jet is
zero.  The graph side is `f(g_empty z_W+g_Q m_W)`.  Since `f` is nonzero and
the two companion forms are independent, both coefficients vanish.

In the strict two-endpoint all-axis model, the existing companion theorem
proves this independence for every root pair.  Hence all four fan top faces
in (8) are zero in that model.  Outside it, a rank-one companion observation
may constrain only one linear combination of `z_W,m_W`; Theorem 1 alone does
not separate them.

There is also an exact target-compatible **formal** boundary.  The
jet-orthogonal `2+2+1` splice in
`P7_221_JET_ORTHOGONAL_SPLICE_AND_FORMAL_FIXED_WINDOW_NO_GO.md` simultaneously
satisfies all 31 nonempty mixed lower-root GHZ equations, retains every
fixed-complement window, and has independent distinguished companions at
every root pair.  Applying Corollary 2 gives

```text
m_W=z_W=0                                             (12a)
```

on every selected fan shore in that formal principal-cofactor ledger.
Consequently the complete nonempty mixed lower-root target equations do not
force a nonzero fan `m_4`; they admit the moment-null alternative exactly.
The splice remains formal at the complementary-cofactor layer, so (12a) is
not a common physical blocker/residual graph realization.

## 3. The canonical six-point word is null as well

Let

```text
W_6=U_0 union U_1 union U_2.                          (13)
```

On common-null directions its blocker word contains two copies of each axis.
Every diagonal tensor `D_d` therefore contains four zero factors.

### Proposition 3 (conditional six-point moment nullity)

Any legal synchronized selector whose target contraction fixes the triple
blocker in a pure direction and exposes the residual-absent or
residual-present top response on `W_6` has target value zero.  If the two
depths are independently selected, then

```text
m_(W_6)=z_(W_6)=0.                                    (14)
```

This proposition is conditional on the selector: unlike the four-window
cover, no fixed-complement theorem presently forces the required six-point
companion shore.  It nevertheless rules out using this canonical common-null
word as a nonzero `m_6` denominator.

## 4. The surviving vacuum-free equation

For an honest two-residual response on a four-set `W`, put

```text
D_W=sum_(e subset W, |e|=2) z_e m_(W minus e)-z_W.    (15)
```

Dual-Wick gives `D_W=h m_W`.  On the target-null chart (12), this becomes

```text
sum_(e subset W, |e|=2) z_e m_(W minus e)=0,          (16)
```

which is exactly (1).  No empty face, residual scalar, division, or additive
weight hypothesis occurs.

Thus legal tetrahedral pair tomography plus compatible residual-present pair
selection would turn each fan window into a genuine bilinear target test.
The four-window theorem reconstructs the direct pairs from marked-star data;
it does not yet expose those sensors or the six `z_e` values in the same
normalization.  Nor is any current P7 theorem known to make the left side of
(16) nonzero.

For two target-null windows, the projective cross-window minor is automatic:
both defects vanish separately.  The new information is therefore (16), not
another ratio equation.

### Proposition 4 (the nonempty mixed-root ledger does not determine the defect)

In the projective lower-root branch, every differentiated root--blocker edge
vanishes.  The 31 nonempty root-jet equations therefore use complementary
deletion labels

```text
C_(I union A),                 empty!=I subset R,     (17)
```

where `A` consists only of companion endpoints such as `Q` (and any other
allowed nonblocker/frozen-root companions).  No label in (17) deletes a
blocker.

By contrast, a pair face on blockers has labels

```text
z_e: C_(R union (B minus e)),
m_e: C_(R union Q union (B minus e)).                 (18)
```

These delete five blockers and are distinct from every label in (17).
Consequently, at the formal cofactor level, adjoining all pair-face variables
is a polynomial-ring extension of the nonempty mixed-root ledger.  The ideal
generated by those 31 target equations has zero elimination ideal in the new
pair-face coordinates.

Proof.  The deletion-class expansion of a lower root jet groups matchings by
the nonblocker companion set `A`; differentiated root--blocker edges are zero,
so `A` contains no blocker.  Equation (18) is the exact principal-deletion
label for leaving only the named blocker pair after all roots have been
removed, with or without `Q`.  The two label families are disjoint.  Formal
cofactor symbols with distinct labels are independent until a common
principal-hafnian realizability equation is imposed.  The jet-orthogonal
splice supplies a point of the 31-equation ledger, so that target ideal is
proper.  Extending a proper ideal by independent pair variables has zero
intersection with the polynomial ring on those pair variables, proving the
elimination claim.

Hence the complete nonempty mixed-root target subsystem cannot make the
left side of (16) nonzero or zero: it does not contain its pair coordinates.
Marked-star tomography and residual-present pair selection are genuinely new
observations.  The physical family below supplies one common response choice
of those formal coordinates satisfying (16).

## 5. A sharp physical response boundary

Use the seven blocker ports and two residual vertices `q_0,q_1`.  For a
parameter `lambda`, install only

```text
B_12=1,
A_(q_0,q_1)=lambda,
R_(q_0,1)=-lambda,
R_(q_1,2)=1,                                          (19)
```

and set every other edge to zero.  In the square-zero port algebra, with
`t=x_1x_2`,

```text
M=1+t,
Phi=lambda-lambda t,
Z=M Phi=lambda.                                       (20)
```

Therefore, simultaneously for every four-window and for `W_6`,

```text
m_W=z_W=0,
z_e=0 for every pair e,
sum_(e subset W) z_e m_(W minus e)=0.                 (21)
```

The complete direct pair layer is fixed (`m_12=1`, all other pairs zero),
while `h=z_empty=lambda` is arbitrary.

### Theorem 5 (physical sharpness of the GHZ-null response equations)

All scalar consequences (12), (14), and (16) admit a one-parameter family of
honest seven-port two-residual responses with fixed nonempty data and varying
residual-empty scalar.

The construction embeds in the canonical coloured port spaces.  On blockers
`1,2 in U_1`, put the displayed rank-one blocks on the covectors dual to
their common-null axes `e_1`, and extend every other colour entry by zero.
Then (20)--(21) hold as full block-response identities, so all mixed-colour
rank and cumulant identities are satisfied automatically.

This is target-compatible only with the contracted GHZ-null equations proved
above.  It supplies no root--blocker system and is not a full P7/GHZ
realization.

## 6. Why root singleton jets are not the required paired depths

In the strict root-companion notation, the singleton GHZ equations constrain

```text
p_i=B_(r_i,q_0)(-,z_0),
q_i=B_(r_i,q_1)(-,z_1),                               (22)
```

which are forms on the tangent space of a **root** `r_i`.  The paired
one-residual response data needed to recover `h` are instead

```text
a_u=B_(q_0,u)(z_0,-),
b_u=B_(q_1,u)(z_1,-),                                 (23)
```

which are forms on a **blocker port** `u`.  Equations (22) and (23) belong to
different unordered physical edge blocks.  Symmetry transposes an edge; it
does not identify a root--residual block with a residual--blocker block.

### Proposition 6 (singleton-depth separation)

The fact that every pair `(p_i,q_i)` is a basis does not expose, determine,
or synchronize any pair `(a_u,b_u)`.  Exact paired-companion recovery of `h`
still requires a legal shore/selector for the blocker-side coefficients in
(23).

This is a statement about what the root singleton equations contain, not a
claim that the full higher mixed-word system leaves (23) arbitrary.  A
common principal-hafnian realization can couple the two edge families through
later matching equations.  No current theorem extracts that coupling as the
paired one-residual response required by the vacuum-free boundary.

The physical family (19) displays the distinction: its blocker singleton row
`a_1=-lambda` varies with `lambda`, even though no root singleton datum has
been changed or supplied.

## Scope wall

```text
all canonical fixed-complement fan words:             GHZ-NULL;
four tetrahedral fan words:                           GHZ-NULL;
independent top selectors => m4=z4=0:                 PROVED;
canonical six-double word:                            GHZ-NULL;
independent six-point selectors => m6=z6=0:           CONDITIONAL;
vacuum-free null-window equation (16):                PROVED;
physical free-h response satisfying every such test: PROVED;
all 31 nonempty mixed root jets with null fan tops:    FORMALLY REALIZED;
pair-face defect fixed by those 31 equations:          FALSE FORMALLY;
root singleton forms = blocker singleton rows:        FALSE;
legal marked-star and z-pair synchronization:         UNKNOWN;
legal paired blocker-singleton depths:                UNKNOWN;
nonzero evaluation of the null-window defect in P7:   UNKNOWN;
full target-compatible physical boundary:             UNKNOWN;
P7 nonrestriction and global Krenn--Gu:               UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_p7_ghz_null_fan_dual_wick_defect_and_singleton_depth_separation.py
python audit_p7_ghz_null_fan_dual_wick_defect_and_singleton_depth_separation.py
python -m py_compile verify_p7_ghz_null_fan_dual_wick_defect_and_singleton_depth_separation.py audit_p7_ghz_null_fan_dual_wick_defect_and_singleton_depth_separation.py
uv run --with ruff ruff check verify_p7_ghz_null_fan_dual_wick_defect_and_singleton_depth_separation.py audit_p7_ghz_null_fan_dual_wick_defect_and_singleton_depth_separation.py
```

The primary replay checks the fan mixed-word vanishings, the selector
implication, the vacuum-free defect, the six-double word, and the full
square-zero counterresponse symbolically.  The independent no-import audit
uses direct coordinate evaluations, a separate matching recurrence, and
rational square-zero multiplication.  Neither script searches or enumerates
graphs, supports, colour words, windows, selectors, or parameters.
