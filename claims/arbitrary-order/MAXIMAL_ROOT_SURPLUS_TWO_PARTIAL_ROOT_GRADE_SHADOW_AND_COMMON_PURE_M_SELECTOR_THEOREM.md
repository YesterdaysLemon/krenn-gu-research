# Maximum-root surplus-two partial-root grade shadow and common pure-M selector

## Status

**Exact characteristic-zero arbitrary-root, all-even-target module theorem.**
In the original surplus-two fixed-`Q` chart, let an even target have size
`|S|=2t`.  Its residual-absent desired companion has root--root grade `t-1`,
while its residual-present companion has grade `t`.  Leave any `t-1` root
slots open and evaluate every other root at the maximum-root vectors.  Every
grade at least `t` is killed, and the grade-`t-1` desired column becomes one
explicit one-sided root-matching tensor.

After applying the same partial-root contraction to the **complete** joint
nuisance, survival of this leading tensor has two consequences:

1. the target joint operator space is nonzero; and
2. it contains the pure residual-absent coefficient row `(1,0)`.

Thus any finite family of even targets whose leading tensors survive has one
common pure-`M` operator direction, even when some target spaces have rank two.
Conversely, if a target has no pure-`M` operator row, every one of its
leading partial-root classes is swallowed by the exact lower-or-equal-grade
nuisance shadow.

For pair targets this is GLS16's base-grade theorem.  For the four-root
four-port target it is a new first-root shadow: one root is left open, the
residual-present grade-two column vanishes, and survival of the explicit
grade-one covector forces the four-port line to contain pure `M`.  Hence
survival of all six pair shadows and one four-port first-root shadow produces
the common seven-target pure-`M` package required by GLD16; GLD16 then excludes
that branch only if its separate three-colour activity hypothesis holds.

**Successor update (2026-08-24).**  The implication remains correct, but
[`GLD68`](FOUR_ROOT_COMPLEMENTARY_PAIR_BASE_NUISANCE_SATURATION_AND_SEVEN_SHADOW_SOURCE_EXCLUSION_THEOREM.md)
proves that its all-six pair-base premise is empty: complementary pair base
classes cannot both survive, so at most three of the six are nonzero.  A
seven-row package must therefore come from non-leading operator supply or a
different promoted interface, not from the displayed six pair base shadows.

The theorem is pointwise on every incidence-rank fibre and uses no support
atlas, response division, incidence inverse, or chosen rank minor.  It does
**not** force a leading class to survive, response activity, or a nonzero
physical output; it does not integrate the distinct GLS8 promoted two-probe
module; and it does not close the strategic node.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## Dependencies and provenance

The exact companion grade is owned by

- [`GLS2`](MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md).

The complete two-column target quotient and operator-coefficient space are
owned by

- [`GLD15`](FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md).

The case `t=1` recovers

- [`GLS16`](MAXIMAL_ROOT_SURPLUS_TWO_BASE_GRADE_PAIR_SHADOW_AND_CROSS_TARGET_SELECTOR_ANNIHILATION_THEOREM.md).

The conditional common-line detector is

- [`GLD16`](FIXED_Q_COMMON_PROJECTIVE_JOINT_RESPONSE_SELECTOR_AND_SHIFTED_GLD3_DETECTOR_THEOREM.md).

No external literature claim is used.  The new content is the arbitrary-grade
partial-root filtration, its explicit leading physical tensor, and the
all-even-target common pure-`M` consequence.

## 1. Even target grades in the original fixed-Q chart

Work over a characteristic-zero field `K`.  Let

```text
R={1,...,r},              |R|=r>=2,
B=Q disjoint-union U,     |Q|=2,       |U|=r.         (1)
```

Every local space is ternary.  Fix fully supported maximum-root vectors
`x_i`, `i in R`, satisfying

```text
W_ij(x_i,x_j)=0                     for i!=j,          (2)
```

and fix residual vectors `z_Q`.

Let

```text
empty!=S subset U,       |S|=2t,       1<=t<=floor(r/2),
C=U-S.                                                   (3)
```

The complete GLD15 joint quotient retains the two labels

```text
I=S,                    I=Q union S                    (4)
```

with desired columns

```text
g_S^M=G_(Q union C)(z_Q),
g_S^Z=G_C,
N_S^J=N_S^(MZ) subset
  L_S^*=(tensor_(i in R)V_i^*) tensor
        (tensor_(u in C)V_u^*).                       (5)
```

The surplus-two grade rule gives

```text
p_M=t-1,                 p_Z=t.                       (6)
```

That is, every matching in `g_S^M` has exactly `t-1` root--root edges and
every matching in `g_S^Z` has exactly `t`.

## 2. Partial-root contraction and the leading tensor

Choose any root subset

```text
A subset R,               |A|=t-1.                   (7)
```

Leave the roots in `A` open and contract every root in `R-A` with its fixed
maximum-root vector:

```text
epsilon_(A,S):L_S^* ->
 (tensor_(a in A)V_a^*) tensor (tensor_(u in C)V_u^*).
                                                               (8)
```

Define

```text
Lambda_(A,S)=epsilon_(A,S)(g_S^M),
N_(A,S)^lead=epsilon_(A,S)(N_S^J),                    (9)
```

and let

```text
b_(A,S)=[Lambda_(A,S)]
```

in the quotient by `N_(A,S)^lead`.

The leading tensor has a direct physical formula.  For an injection

```text
tau:A -> R-A,                                         (10)
```

put

```text
R_tau=product_(a in A) W_(a,tau(a))(-_a,x_(tau(a))). (11)
```

The remaining root set

```text
R_tau^0=R-(A union tau(A))                            (12)
```

has size `r-2t+2=|Q union C|`.  Let

```text
Per_(tau;Q,C)
```

be the root-to-`Q union C` permanent from `R_tau^0`, with its root slots
evaluated at `x`, its `Q` slots evaluated at `z_Q`, and its `C` slots open.

### Theorem 1 (partial-root grade shadow)

For every `A,S` as above,

```text
Lambda_(A,S)=sum_(tau:A -> R-A injective)
                R_tau tensor Per_(tau;Q,C),           (13)

epsilon_(A,S)(g_S^Z)=0.                              (14)
```

Moreover `N_(A,S)^lead` is exactly the span of the partial-root coefficient
slices of all joint-nuisance labels `I` satisfying

```text
2<=|I|<=2t,           |I| even,       I!=S.           (15)
```

Every label of order at least `2t+2` is killed.  Consequently (8) induces a
well-defined quotient map

```text
bar epsilon_(A,S):
 L_S^*/N_S^J ->
 ((tensor_(a in A)V_a^*) tensor (tensor_(u in C)V_u^*))
   /N_(A,S)^lead                                      (16)
```

which sends

```text
bar g_M |-> b_(A,S),             bar g_Z |->0.        (17)
```

#### Proof

Consider a companion matching with `p` disjoint root--root edges.  A
root--root factor survives (8) only if at least one of its endpoints lies in
`A`; otherwise it is evaluated at `(x_i,x_j)` and vanishes by (2).  Since the
root--root edges are disjoint, `A` can meet at most `|A|=t-1` of them.  Hence
every matching with `p>=t` vanishes.  This proves (14) and kills every label
of order at least `2t+2` by the grade rule.

For `g_S^M`, there are exactly `t-1` root--root edges.  A surviving matching
must have every edge meet `A`.  Because there are as many edges as vertices
of `A`, each edge has exactly one endpoint in `A`; an edge internal to `A`
would leave too few open vertices to meet all the remaining edges.  The other
endpoints therefore define an injection `tau:A->R-A`.  The unused roots are
bijected to `Q union C`.  This is exactly one term of (13), and the
construction is reversible and multiplicity preserving.

Apply the same argument to every coefficient slice in the complete joint
nuisance.  A label `I` has grade `(|I|-2)/2`; precisely the labels in (15)
can survive, while `I=S` was removed from the nuisance definition.  The other
desired label `Q union S` has order `2t+2` and is killed.  This proves the
nuisance description and therefore the induced map (16)--(17).  `square`

For `t=1`, `A=empty`, (13) is the root-to-`Q union C` complementary permanent,
and Theorem 1 is exactly the GLS16 base-grade shadow.

## 3. Common pure-M operator supply

Define the exact operator-coefficient space directly by

```text
C_S={
 (lambda(g_S^M),lambda(g_S^Z)):
 lambda in (N_S^J)^perp
} subset K^2
```

and put

```text
k_S=dim C_S=dim span{bar g_M,bar g_Z}.                (18)
```

The equality is the transpose-rank argument of GLD15 and does not depend on
the number of roots or the size of `S`: the evaluation map from the dual of
`L_S^*/N_S^J` to `K^2` is the transpose of
`(u,v) |-> u bar g_M+v bar g_Z`.  Thus the exact rank-zero, rank-one, and
rank-two operator classification applies to every target in (3), not merely
to the four-root instances emphasized in GLD15's opening notation.

### Theorem 2 (leading survival forces the pure-M row)

If

```text
b_(A,S)!=0                                             (19)
```

for at least one `A in binom(R,t-1)`, then

```text
k_S>=1,                 (1,0) in C_S.                (20)
```

More precisely:

```text
k_S=1  => C_S=K(1,0),
k_S=2  => C_S=K^2.                                    (21)
```

Equivalently, if `(1,0) notin C_S`, then

```text
b_(A,S)=0             for every A in binom(R,t-1).   (22)
```

#### Proof

If `k_S=0`, then `g_S^M in N_S^J`, and (16) forces every `b_(A,S)` to vanish.
Thus (19) gives `k_S>=1`.

If `k_S=1`, choose its homogeneous orientation

```text
bar g_M=delta_S bar g_S,
bar g_Z=eta_S bar g_S,                                (23)
```

so that `C_S=K(delta_S,eta_S)`.  The quotient-kernel identity is

```text
delta_S g_S^Z-eta_S g_S^M in N_S^J.                 (24)
```

Apply (16).  It gives

```text
eta_S b_(A,S)=0.                                     (25)
```

Under (19), `eta_S=0`.  Since the projective vector is nonzero,
`delta_S!=0`, proving the first line of (21).  At rank two, GLD15 gives
`C_S=K^2`, which contains `(1,0)`.  This proves (20)--(21), and (22) is the
contrapositive.  No coefficient has been normalized in (24)--(25).  `square`

### Corollary 2.1 (finite-family common pure-M selector)

Let `F` be any finite family of nonempty even targets in `U`.  If every
`S in F` has at least one leading class satisfying (19), then

```text
(1,0) in intersection_(S in F) C_S.                  (26)
```

Thus one coefficient direction gives legal constant pure-`M` operator rows
for the whole family.  The target functionals themselves may depend on `S`;
the graph, `Q`, residual contraction, and coefficient direction do not.

On a complete hypothetical witness, every selected response is the physical
residual-absent tensor

```text
M_S=H_S,                                              (27)
```

and is target-diagonal.  It is nonzero exactly when the separately declared
physical tensor `H_S` is nonzero.

#### Proof

Theorem 2 puts `(1,0)` in every `C_S`, proving (26).  Apply each exact
operator identity to the complete GHZ target.  Its output is target-pure, so
the selected tensor `M_S` is diagonal.  Operator legality alone does not force
that tensor to be nonzero.  `square`

This common-line conclusion includes rank-two target spaces; separate paired
attachment is stronger than needed for the shared pure-`M` direction.

## 4. Exact four-root pair/four-port consequence

Take `r=4` and `U={1,2,3,4}`.  The six pair targets have `t=1`, so their
leading classes are the GLS16 base classes

```text
b_(empty,S)=[Pi_S(z_Q)].                              (28)
```

For the four-port target `S=U`, take `t=2` and leave one root `a` open.  Here
`C=empty`, and (13) becomes the explicit covector

```text
Lambda_(a,U)=sum_(j in R-{a})
 W_aj(-_a,x_j) p_(R-{a,j},Q)(z_Q) in V_a^*.          (29)
```

Its nuisance shadow contains the one-root contractions of every order-two
label and every order-four label other than `U`; every order-six label is
killed.  Put

```text
b_(a,U)=[Lambda_(a,U)] in V_a^*/N_(a,U)^lead.        (30)
```

### Corollary 2.2 (conditional seven-target synchronization)

Assume

```text
b_(empty,S)!=0                 for all S in binom(U,2),
b_(a,U)!=0                     for at least one a in R.       (31)
```

Then all seven complete GLD15 operator spaces contain the common pure-`M`
direction `(1,0)`.  On a hypothetical witness the legally selected package is

```text
D_e=M_e=B_e,                   T'=M_U.               (32)
```

It is target-diagonal.  In GLD16's notation

```text
(delta,eta)=(1,0),             a=delta+h eta=1,       (33)
```

so no residual-scalar divisor occurs.  If this selected pair package also
satisfies GLD16's declared three-colour pair-depth activity, the GLD16
nine-word detector contradicts the complete mixed target.

#### Proof

Apply Corollary 2.1 to the six pair targets and `U`.  Equations (32)--(33) are
the pure-`M` specialization of the GLD16 package and its effective scalar.
The final implication is exactly the conditional GLD16 detector theorem; no
activity statement is supplied here.  `square`

Thus on the root-order-four nonzero-response synchronization problem, every
surviving witness must fail at least one condition in (31), fail the separate
activity gate, or leave the complete rank/response hypotheses through a
branch already recorded elsewhere.  This is a pointwise reduction, not an
exhaustive source-level exclusion.

## 5. Pointwise failure ledger and boundary

For a target `|S|=2t`, define its **leading-survival locus** by the existence
of at least one `A` with `b_(A,S)!=0`.  The exact implications are

```text
leading survival:
  k_S=1 with pure-M line, or k_S=2;
  a legal pure-M operator row exists;

no pure-M operator row:
  every one of the binom(r,t-1) leading classes is swallowed;

all targets in a finite family have leading survival:
  one common pure-M coefficient direction exists;

all seven r=4 shadows in (31) survive plus GLD16 activity:
  complete mixed-target contradiction.                           (34)
```

The converses not displayed in (34) are not claimed.  In particular, all
leading classes may be swallowed while a pure-`M` selector exists through a
different full-module functional.

```text
partial-root grade cutoff at t-1 open roots:               PROVED;
explicit leading tensor (13):                              PROVED;
complete nuisance shadow through order 2t:                 PROVED;
leading survival forces pure-M operator supply:            PROVED;
finite-family leading survival gives common pure-M line:   PROVED;
r=4 four-port first-root shadow (29):                       PROVED;
r=4 seven-shadow plus activity implication via GLD16:      PROVED CONDITIONAL;
r=4 all-six pair-base source premise (by GLD68):            IMPOSSIBLE;
needed leading survival on every actual witness:           UNKNOWN;
three-colour selected-response activity:                    UNKNOWN;
foreign GLS15 transport on swallowed-leading branches:      UNKNOWN;
GLS8 promoted target integration:                           OPEN;
complete maximum-root supply/attachment node:               OPEN;
global Krenn--Gu conjecture:                                 UNRESOLVED.      (35)
```

The smallest next obligation is to exploit the complementary swallowed-base
circuits forced by GLD68, obtain pair rows from a non-leading source, or use
the complete mixed GHZ equations to contradict the simultaneous lower-grade
absorption identities (22), including
every exceptional incidence fibre.  For `r=4`, failure of the four-port gate
is the four exact first-root absorptions `b_(a,U)=0`; it is not a generic
determinant or an untracked response divisor.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_partial_root_grade_shadow_and_common_pure_m_selector.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_partial_root_grade_shadow_and_common_pure_m_selector.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_partial_root_grade_shadow_and_common_pure_m_selector.py claims/arbitrary-order/audit_maximal_root_surplus_two_partial_root_grade_shadow_and_common_pure_m_selector.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_partial_root_grade_shadow_and_common_pure_m_selector.py claims/arbitrary-order/audit_maximal_root_surplus_two_partial_root_grade_shadow_and_common_pure_m_selector.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_partial_root_grade_shadow_and_common_pure_m_selector.py claims/arbitrary-order/audit_maximal_root_surplus_two_partial_root_grade_shadow_and_common_pure_m_selector.py
```

The focused primary verifier enumerates every root matching by grade through
order seven, applies every relevant partial-root mask, and compares the
surviving desired matchings with the injection/permanent formula (13).  It
also checks the nuisance grade cutoff, projective rank implications, and the
four-root covector count.  The independent no-import audit uses a recursive
matching generator through order eight, bitmask transversals instead of the
primary injection construction, and a separate primitive-projective/common-
intersection census.  These bounded programs audit the conventions and exact
finite identities; the arbitrary-root disjoint-edge and labelled-quotient
arguments above are the proofs.
