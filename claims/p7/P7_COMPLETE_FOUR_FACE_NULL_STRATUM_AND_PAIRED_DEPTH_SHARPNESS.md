# The complete P7 four-face null stratum and paired-depth sharpness

## Status

**Exact characteristic-zero conditional obstruction and rational common-block
sharpness control.**  The eighteen colour-tagged fixed-complement windows on the six
double blockers cover all fifteen physical four-subsets.  Consequently, if
the two distinguished top selectors are legal on every tagged window, then
every common-null direct and two-residual four-point response is zero.

This is much stronger than the four-window tetrahedral statement.  The
six-vertex vanishing-four-hafnian lemma then implies that the direct
common-null blocker graph has matching number at most two.  Its six-point
direct moment is zero, and dual Wick forces its two-residual six-point
response to be zero as well.  Thus **no** `m_4` or `m_6` denominator survives
anywhere on the six common-null blocker lines.  The residual pair correction
is tangent to the complete four-hafnian-zero locus.

There is also a sharp rational common-block model.  All three pure GHZ
coefficients equal one, but every root-triple null space at every double
blocker is exactly its canonical coordinate axis.  Hence none of the
fixed-complement windows has a noncanonical clean word: every legal clean
direction in this model is the already known GHZ-null direction.  The same
common edge-block assembly can be given both complete blocker-side singleton rows while
all direct blocker edges vanish.  Those rows and every nonempty response are
then fixed while the residual-empty scalar varies freely.

The model is one common symmetric bilinear block ledger and realizes the three
pure diagonal coefficients.  It is **not** a target-compatible physical P7
construction or a full `P_7 -> Delta_3` restriction: its mixed blocker words
are not asserted to equal GHZ.  Thus it
proves that pure nonvanishing, canonical incidence, and even granted paired
singleton rows do not force the desired nonzero moment.  It does not rule out
a new cross-depth identity using the complete mixed P7 system.  Legal top
selectors in the unrestricted problem, such a cross-depth identity, the P7
restriction problem, and the Krenn--Gu conjecture remain
**UNKNOWN/UNRESOLVED**.

No graph family, support family, colour word, selector family, or parameter
set is enumerated below.

## 1. Eighteen tagged windows are all fifteen four-sets

Let the six double blockers be the disjoint union

```text
X=U_0 disjoint union U_1 disjoint union U_2,     |U_c|=2.       (1)
```

For pure colour `c`, fixed-complement Laplace supplies every tagged window

```text
W=U_c union S,                 S subset X minus U_c, |S|=2.     (2)
```

There are six such windows for each colour.  Some physical four-sets receive
two tags, so eighteen is not the number of distinct windows.

### Lemma 1 (complete four-set cover)

Every four-subset of `X` has the form (2) for at least one `c`.  Hence the
eighteen colour-tagged windows have exactly

```text
binom(6,4)=15                                             (3)
```

distinct physical supports.

Proof.  Four selected elements distributed among three two-element boxes
must fill at least one box `U_c`.  This proves coverage without listing the
four-sets.  Equivalently, each of the three tagged families has size six,
each pair of families meets in the single set `U_c union U_d`, and the triple
intersection is empty, so inclusion--exclusion gives
`3*6-3=15`.

Use once and for all the canonical common-null direction at each double
blocker.  A multiply tagged support therefore carries the same physical
scalar response in each tag; it is not a new coordinate.

### Theorem 2 (conditional complete four-face collapse)

Assume that on every colour-tagged fixed-complement window the two
distinguished residual-absent/residual-present companions admit independent
legal selectors with the common nonzero shore normalization.  Then

```text
m_W=haf(B[W])=0,             z_W=haf(G[Q union W])=0    (4)
```

for every four-subset `W subset X`.

Proof.  Every tagged common-null word is GHZ-null.  Independent selectors
therefore force both top coefficients to zero on that tag.  Lemma 1 covers
every physical four-subset, and the globally fixed null lines identify
multiple tags of the same support.

The selector hypothesis is substantive.  Fixed-complement Laplace forces the
graph-side windows, but the unrestricted P7 theory does not yet force the two
legal top observations on all eighteen tags.

## 2. Matching number at most two

Write the scalar direct edge on the common-null lines as `b_ij=b_ji`.  For
four distinct vertices,

```text
m_ijkl=b_ij b_kl+b_ik b_jl+b_il b_jk.                  (5)
```

We recall the exact six-vertex lemma, including its characteristic-zero
proof because it is the mechanism that turns (4) into a support theorem.

### Lemma 3 (vanishing four-hafnians forbid a support perfect matching)

Over a characteristic-zero field, if (5) vanishes for all four-subsets of
six vertices, the nonzero-edge support of `(b_ij)` has matching number at
most two.

Proof.  Suppose three disjoint weights are nonzero.  Relabel and apply
nonzero vertex scalings so that

```text
b_01=b_23=b_45=1.                                      (6)
```

Put

```text
p=b_02, q=b_03, r=b_12, s=b_13,
u=b_04, v=b_05, w=b_14, x=b_15,
a=b_24, b=b_25, c=b_34, d=b_35.                        (7)
```

The equations on `0123`, `0145`, and the four sets containing `01` give

```text
1+ps+qr=0,                 1+ux+vw=0,                  (8)
a=-pw-ur, b=-px-vr, c=-qw-us, d=-qx-vs.                (9)
```

Substitute (9) into the four equations containing `23`.  Since two is
invertible,

```text
u=pqw,       v=pqx,       w=rsu,       x=rsv.          (10)
```

Equation `1+ux+vw=0` makes at least one of `ux,vw` nonzero; (10) then makes
all eight variables before `a,b,c,d` nonzero.  Set `P=ps`, `Q=qr`.  Equations
(8)--(10) give

```text
P+Q=-1,                 PQ=1,                 2vw=-1.  (11)
```

The equation on `0245`, after (9)--(11) and division by nonzero `p`, is

```text
1+(Q^2+P)vw=0.                                       (12)
```

From (11), `Q^2=P`; comparing (12) with `2vw=-1` forces
`P=1`, hence `Q=1`, contradicting `P+Q=-1` in characteristic zero.

### Theorem 4 (complete null-stratum obstruction)

Under the selector hypothesis of Theorem 2:

```text
matching_number(supp B|X)<=2,
m_X=0,
z_X=0.                                                 (13)
```

Proof.  Lemma 3 gives the support bound.  A nonzero term of the six-point
hafnian `m_X` would be a support matching of size three, so `m_X=0`.
For `|X|=6`, dual Wick is

```text
sum_(e subset X, |e|=2) z_e m_(X minus e)-z_X=2h m_X. (14)
```

Every `m_(X minus e)` is a four-point moment and is zero by Theorem 2;
therefore (14) gives `z_X=0`.

This eliminates the entire canonical `m_4/m_6` recovery route, not merely
the four tetrahedral supports previously singled out.

## 3. The residual correction is tangent to the null stratum

For an honest two-residual response, write

```text
k_ij=z_ij-h b_ij=a_i b'_j+a_j b'_i,                   (15)
```

where `a_i,b'_i` are the two blocker-side singleton incidence rows.  On a
four-set `W`, the dual-Wick equation with `m_W=z_W=0` is

```text
sum_(e subset W, |e|=2) z_e m_(W minus e)=0.           (16)
```

Substituting `z_e=h b_e+k_e`, the coefficient of `h` is twice (5), because
each perfect matching is selected once through each of its two edges.  It
vanishes on the null stratum.  Hence

```text
sum_(e subset W, |e|=2) k_e m_(W minus e)=0            (17)
```

for all fifteen four-sets.

### Proposition 5 (tangent correction)

Equation (17) is exactly

```text
d(haf_W)_B(K)=0.                                       (18)
```

Thus the residual pair correction `K=(k_ij)` lies in the Zariski tangent
space at `B` to the simultaneous four-hafnian-zero locus.

This is a first-order cross-depth constraint, but it still contains no
nonzero denominator.  At singular points such as `B=0`, the tangent equations
are vacuous.

## 4. A saturated-null common-block countermodel

We now show that a noncanonical clean word is not forced by the pure/common-
block hypotheses.  Work over `Q`.  At each blocker use coordinates
`e_0,e_1,e_2`.  The double blockers are

```text
u_01,v_01;        u_02,v_02;        u_12,v_12,         (19)
```

and `t` is the triple blocker.  For roots `i=0,...,4`, put

```text
r_(i,u_ab)=e_a^*+(i+1)e_b^*,
r_(i,v_ab)=2e_a^*+(2i+3)e_b^*,                         (20)

r_(i,t)=tau_0 e_0^*+tau_1 e_1^*+tau_2 e_2^*,
(tau_0,tau_1,tau_2)=(1/480,1/4800,1/38124).            (21)
```

For distinct roots `i,j`, the two-by-two row determinants at `u_ab` and
`v_ab` are respectively

```text
j-i,                         4(j-i).                   (22)
```

They are nonzero.  Therefore every root triple spans the full supported
coordinate plane at every double blocker.  If `w` is missing colour `c`,

```text
intersection_(j in J) ker r_(j,w)=Q e_c               (23)
```

for every root triple `J`.  There is no additional, noncanonical clean
direction.

The three pure five-by-five matrices, with their indicated columns, are

```text
H_0: (t,u_01,v_01,u_02,v_02), row i
     [1/480,   1,      2,      1,      2],

H_1: (t,u_01,v_01,u_12,v_12), row i
     [1/4800,  i+1,    2i+3,   1,      2],

H_2: (t,u_02,v_02,u_12,v_12), row i
     [1/38124, i+1,    2i+3,   i+1,    2i+3].          (24)
```

Their unscaled permanents are `480,4800,38124`, so

```text
per H_0=per H_1=per H_2=1.                             (25)
```

All three pure charts are therefore nonzero.  Nevertheless, in any
fixed-complement window of pure colour `c`, the shore contains `t` evaluated
at `e_c`, while the open set contains two blockers supported on a pair that
contains `c`.  Those two blockers are missing a colour different from `c`;
by (23) their only clean directions have zero `c` coordinate.  The diagonal
GHZ contraction is zero.  Thus every possible root-triple clean direction in
this model is GHZ-null.

To assemble one common symmetric bilinear block ledger, take a root covector
`alpha_i` with `alpha_i(x_i)=1` at the fixed root vector and set

```text
B_(r_i,w)=alpha_i tensor r_(i,w),                       (26)
```

using the transpose on the reversed edge.  Equations (20)--(25) are then the
actual coordinate slices of one common block system, not three unrelated
scalar matrices.

### Theorem 6 (noncanonical-word no-go at the pure/common-block level)

Canonical incidence, one common rational root--blocker system, and all three
nonzero pure coefficients do not force any noncanonical GHZ-nonzero
fixed-complement clean word.  The model (20)--(26) has none.

This theorem does not include the complete mixed root and blocker-word GHZ
equations.  A theorem using those extra equations could still exclude this
model.

## 5. Full paired singleton rows still need a nonzero direct edge

Extend the same common-block control by residual vertices `q_0,q_1`.  Write

```text
U_c={u_c,v_c}
```

for the double pair missing colour `c`; explicitly
`U_0={u_12,v_12}`, `U_1={u_02,v_02}`, and
`U_2={u_01,v_01}`.  Install the residual--blocker covectors

```text
a_(u_c)=e_c^*,       b_(u_c)=0,
a_(v_c)=0,           b_(v_c)=e_c^*,                    (27)
```

set every blocker--blocker edge to zero, and put
`B_(q_0,q_1)=h`.  Set all other new blocks to zero.

On pure colour `c`, the two residual vertices are forced onto `u_c,v_c`,
where their two-by-two permanent is one, while the five roots match the other
five blockers with permanent (25).  Hence the complete fourteen-vertex pure
hafnian is exactly one for every colour, independently of `h`.

On the blocker response algebra, let

```text
A=x_(u_0)+x_(u_1)+x_(u_2),
C=x_(v_0)+x_(v_1)+x_(v_2).                             (28)
```

Because the direct blocker graph is zero,

```text
M=1,                         Z=h+A C.                  (29)
```

Both complete singleton rows (27), every nonempty coefficient of `M`, and
every nonempty coefficient of `Z` are fixed while `h` is arbitrary.  In
particular all `m_4,m_6,z_4,z_6` vanish.

### Theorem 7 (paired-depth sharpness)

Even granting both full blocker-side singleton rows does not recover the
empty scalar unless they co-occur with a known nonzero direct blocker edge.
The family (27)--(29) is an exact common-edge scalar-hafnian response control with
fixed singleton depths, fixed nonempty responses, three fixed nonzero pure
coefficients, and free `h`.

It remains not target-compatible on the mixed P7 words, so this is not a
physical construction of the conjectured restriction or its counterexample.

Conversely, if for some pair `u,v` the same physical chart exposes
`a_u,b_u,a_v,b_v`, `z_uv`, and a nonzero direct edge `b_uv`, then

```text
h=(z_uv-a_u b_v-a_v b_u)/b_uv.                         (30)
```

Thus (29) is sharp: the missing requirement is not another singleton row,
but legal cross-depth co-occurrence with a nonzero direct pair.

## Scope wall

```text
18 tagged common-null windows cover all 15 four-sets:      PROVED;
independent selectors on all tags => all m4=z4=0:           PROVED;
all m4=0 => common-null support matching number <=2:        PROVED;
complete canonical m6=z6=0:                                PROVED;
residual pair correction tangent to the null stratum:       PROVED;
pure/common-block forcing of a noncanonical clean word:      FALSE;
full paired singleton rows alone recover h:                  FALSE;
paired rows + known z2 + nonzero compatible m2 recover h:    PROVED;
legal independent top selectors on every P7 tag:             UNKNOWN;
mixed-word exclusion of the saturated-null model:            UNKNOWN;
legal cross-depth nonzero direct-pair co-occurrence:          UNKNOWN;
full target-compatible physical boundary:                    UNKNOWN;
P7 nonrestriction and global Krenn--Gu:                      UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_complete_four_face_null_stratum_and_paired_depth_sharpness.py
python claims/p7/audit_p7_complete_four_face_null_stratum_and_paired_depth_sharpness.py
python -m py_compile verify_p7_complete_four_face_null_stratum_and_paired_depth_sharpness.py audit_p7_complete_four_face_null_stratum_and_paired_depth_sharpness.py
uv run --with ruff ruff check verify_p7_complete_four_face_null_stratum_and_paired_depth_sharpness.py audit_p7_complete_four_face_null_stratum_and_paired_depth_sharpness.py
```

The primary replay checks the inclusion--exclusion cover, the normalized
four-hafnian ideal, the tangent identity, the rational pure matrices, the
saturated root-triple kernels, and the free-`h` paired-row response.  The
independent no-import audit uses rational permanent recurrence, the hand
characteristic-zero contradiction, and a separate square-zero coefficient
ledger.  Neither replay searches graph families, supports, colour words,
selectors, or parameters.
