# Hostile review of fixed-pair same-mode `N/N`, `q_-` exclusion

## Verdict and exact scope

**PASS, for the stated fixed-pair, pointwise, characteristic-zero,
same-mode common-kernel branch with a `q_-` companion.**  No support split,
propagation, quotient-dimension, tensor-slot, rank, coordinate-fork, scalar,
field, quantifier, dependency, implementation, or scope blocker survived
hostile review.

The package treats a remaining local plane whose restricted `Phi_1` and
`Phi_2` kernels are both the common line

```text
N=K(x_2+x_3).
```

The local support of `N` is necessarily singleton or `{0,1}`.  In both
cases the exact target produces a singleton colour-2 companion in

```text
H_N=span{x_0+x_1,x_2-x_3}.
```

The companion has only two projective branches.  This package excludes

```text
q_-=x_0+x_1-x_2+x_3
```

through every placement and support case.  It does not exclude

```text
q_+=x_0+x_1,
```

does not exclude every same-mode `N/N` incidence, and does not prove
unrestricted `P_6 -> Delta_3` nonrestriction.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_SAME_MODE_NN_Q_MINUS_EXCLUSION_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_same_mode_nn_q_minus_exclusion.py
  audit_arbitrary_permanent_fixed_pair_same_mode_nn_q_minus_exclusion.py
```

Load-bearing frozen predecessors:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
  ARBITRARY_PERMANENT_FIXED_PAIR_SINGLETON_EXCEPTIONAL_COMPANION_PROPAGATION_THEOREM.md
  ARBITRARY_PERMANENT_FIXED_PAIR_SAME_MODE_COMMON_NONCOMMON_EXCLUSION_THEOREM.md
```

The support-two double-contraction incidence package supplies adjacent
background, but the new proof restates and rederives each double-contraction
identity it actually uses.

## 1. Exhaustive support and placement split

The kernel-support predecessor proves that a local `N` occurrence misses
colour `2` and has support at most two.  Since `N` is nonzero, its support is
therefore exactly one of

```text
{0}, {1}, {0,1}.
```

This makes singleton versus support two exhaustive.  For singleton `N`,
the companion-propagation predecessor puts a colour-2 vector in `H_N` in
one of the other three modes.  Section 2 independently extends that
conclusion to support-two `N`.

If support-two `N` occurs, the identical `N,N` double contractions rule out
an `N` in any second mode.  If singleton `N` occurs, every additional `N`
must be singleton at the opposite colour: equal singleton colours and a
support-two second occurrence are both impossible.  Two additional
opposite-colour occurrences would have equal colours to each other and are
therefore also impossible.  Hence there is at most one second `N` mode.

After the visible `x_0 <-> x_1`, `d_0 <-> d_1`, `m_1 <-> m_2` symmetry,
the only surviving two-`N` labelling is

```text
y_(a,0)=N,                 y_(c,1)=N.
```

The vector `q_-`, forced into a mode different from the original mode `a`,
then either lies in the second-`N` mode `c` or in one of the other two modes.
These are precisely Sections 5.2 and 5.1.  No third-`N` or companion-placement
case is omitted.

## 2. Support-two propagation to `H_N`

Contracting the five complementary quartics once with `N` gives

```text
m_1=m_2=d_2=0,             d_0=h_0,             d_1=h_1,
```

where `h_0,h_1` are independent and

```text
ann_R(h_0,h_1)=H_N=span{M,x_2-x_3},
M=x_0+x_1.
```

For support-two `N`, rescaling the two active local columns preserves the
diagonal target form and permits

```text
N=y_(t,0)+y_(t,1).
```

Modulo `H_N`, the contraction tensor on the other three modes is a
two-dimensional `R/H_N`-valued cubic with exactly two nonzero diagonal
cells, `000` and `111`.  If all three remaining local planes missed `H_N`,
their quotient images would still have dimension three in the
four-dimensional space

```text
(R/H_N) direct-sum A.
```

For two distinct colours, fixing two modes gives a linear map to `R/H_N`
which kills the third three-plane, so its rank is at most one.  A nonzero
`J`-pairing would restrict to a scalar identity of rank two on `R/H_N`.
Thus all cross-colour `A` pairings vanish.  The exact two-active-colour
lemma then kills every colour-2 `A` column in those three modes.  Only the
removed mode could supply an `A` factor to the pure `2222` coefficient,
which cannot supply the two distinct factors `x_4,x_5`.  This contradicts
`lambda_2!=0`.

Consequently a different local plane meets `H_N`.  Choosing nonzero
`q` in that intersection and contracting in the two distinct modes is
legal.  The left sides of both `d_0` and `d_1` vanish because
`h_0(q)=h_1(q)=0`.  The support-two coefficients of `N` and the nonzero
`lambda_0,lambda_1` force the colour-0 and colour-1 coefficients of `q` to
vanish.  Hence `q` is singleton-supported at colour `2`.

This reproduces for support-two `N` exactly the companion conclusion used
from the predecessor in the singleton case.

## 3. Exact companion fork

Write

```text
q=sM+u(x_2-x_3),                 s!=0.
```

The nonzero condition on `s` is forced by the live `d_2` target, not by a
projective normalization.  Direct contraction independently gives

```text
m_1=sL-2u x_1,              m_2=sL-2u x_0,
d_0=d_1=(s+u)L,             d_2=-2sM,
L=-x_0-x_1-x_2+x_3.
```

The first four contractions have zero target and the last has nonzero
target.  If both `u` and `s+u` were nonzero, the zero residual covectors
would span `L,x_0,x_1` and hence contain the live residual `M`.  Therefore

```text
u=0              or              u=-s.
```

After projectivizing only now, these are exactly

```text
q_+=M,                    q_-=M-x_2+x_3.
```

For `q_-`, the residual table is

```text
m_1=h_2',       m_2=h_2,       d_0=d_1=0,       d_2=-2M.
```

The three nonzero covectors are independent and have common kernel `KN`.
They span `N^perp`; no fourth covector or unproved fullness assumption is
used.

## 4. The zero/live quotient pair gate

Put

```text
D=R/KN,                     dim D=3,
W=D direct-sum A,           dim W=5.
```

The line in `D` simultaneously annihilated by `h_2,h_2'` and seen
nontrivially by `M` is represented by `class(M)`: indeed

```text
h_2(M)=h_2'(M)=0,                 M(M)=2!=0.
```

Suppose three-dimensional shores `U,V subset W` satisfy

```text
B_u|_(U,V)=0,
B_v|_(U,V)=e tensor rho tensor sigma !=0.
```

The rank proof is exact:

1. If `a(U)=0`, then `U=D`.  The live equation has image either zero or all
   of the three-space `D`, contradicting its nonzero one-dimensional output.
   The same excludes `a(V)=0`.
2. If `a(U)=A`, choose a nonzero pure-`D` vector in the kernel of
   `a|V`.  The zero equation forces `a(u)=0`; nondegeneracy of `J`,
   surjectivity of `a(U)`, and the already nonzero `a(V)` then force
   `r(u)=0`, contradicting `u!=0`.  The other rank-two shore is symmetric.

Thus both `A`-projection ranks are one.  Factor them as

```text
a(z)=alpha(z)p,                 a(w)=beta(w)q.
```

The kernels of `alpha` and `beta` are two-dimensional pure-`D` planes.
Restricting the live equation to either kernel shows

```text
J(a(v),q)=J(a(v),p)=0;
```

otherwise a two-dimensional output would lie in the one-dimensional line
`Ke`.  The live equation reduces to

```text
B_v=r(v)J(p,q) alpha tensor beta.
```

Uniqueness of the three factor lines in a nonzero decomposable tensor forces
`alpha proportional rho` and `beta proportional sigma`.  This establishes
both the ranks and colour alignment; neither conclusion follows from the
zero equation alone.

After contracting `q_-` in its colour-2 mode, choose an off-colour local
basis vector in the original `N` mode whose class modulo `KN` is nonzero,
and choose its colour-2 vector for `v`.  Such an off-colour class exists:
for singleton `N` it follows from local independence, while for
`N=y_0+y_1` neither `y_0` nor `y_1` can lie in `KN` without making them
dependent.  If neither remaining shore contains a second `N`, its quotient
image is still three-dimensional.  The exact target gives the zero/live
pair with `rho=sigma=e_2^*`, hence

```text
a(y_(U,0))=a(y_(U,1))=a(y_(V,0))=a(y_(V,1))=0.
```

This records precisely where the no-second-`N` and three-dimensional-shore
hypotheses enter.  The proof does not apply this gate after a quotient shore
has collapsed.

## 5. No-second-`N` exclusions

### Singleton original `N`

If the original `N` is singleton-supported at colour `c in {0,1}`, its
pure-colour-`c` vector is in `R`, and both last-shore colour-`c` vectors are
in `R` by the pair gate.  Only the companion mode can have an `A` part.
Complete polarization of any quartic with factor `x_4x_5` requires two
distinct input slots to supply those factors.  The live `d_c` coefficient
therefore vanishes, a contradiction.

### Support-two original `N`

Normalize `N=y_(t,0)+y_(t,1)`.  Since `N` has zero `A` part,

```text
a(y_(t,1))=-a(y_(t,0)).
```

In the pure colour-zero `d_0` coefficient, the only possible `A` suppliers
are the original mode and the companion mode.  Replacing the original
colour-zero vector by its colour-one vector changes the only potentially
nonzero `A` pairing by a sign.  Terms using its `R` part have only one
possible `A` supplier and vanish.  Therefore

```text
T_(d_0)(1,0,0,0)=-T_(d_0)(0,0,0,0).
```

The left side is an off-diagonal target entry and is zero; the right side is
`-lambda_0`, which is nonzero.

The support-two branch cannot hide a collapsed quotient.  For two `N`
vectors in distinct modes, direct double contraction gives

```text
d_0=d_1=2x_4x_5,              m_1=m_2=d_2=0.
```

If the second `N` is singleton, the identical left tensor would have to be
zero in one diagonal channel and nonzero in the other.  If it has support
two, it would have to be nonzero multiples of both `E_00` and `E_11`.
Both are impossible.  Thus support-two original `N` has no second-`N`
case beyond the exclusion above.

## 6. Singleton original `N` with a second `N`

Equal singleton colours produce the same live/zero conflict from the
identical double contractions.  A support-two second `N` does as well.
After the exact colour symmetry, the only survivor is

```text
y_(a,0)=N,                 y_(c,1)=N.
```

### Companion in a third mode

Let `q_-=y_(b,2)` and let `d` be the fourth mode.  Legal double contraction
in the distinct modes `a,c` gives

```text
A_b^T J A_d=0,                rank A_b+rank A_d<=2.
```

Neither rank is zero.  For example, if `A_d=0`, the zero `d_1` cubic after
contracting `N` in mode `a` and the live `d_0` cubic force
`h_1R_d=0`; contracting `N` in mode `c` would then make its live `d_1`
cubic vanish.  The `A_b=0` case is the same direct argument with the shores
interchanged.  Hence both ranks are one.

Write

```text
A_b=p alpha^T,          A_d=q gamma^T,
J(p,q)=0,               alpha_2=0.
```

The last equality uses that the companion vector `y_(b,2)=q_-` is pure
`R`.  Direct polarization reproduces all four displayed tensors

```text
X tensor delta tensor gamma + alpha tensor beta tensor Z
  =lambda_0 e_0 tensor e_0 tensor e_0,
Y tensor delta tensor gamma + alpha tensor beta tensor W=0,
X tensor epsilon tensor gamma + alpha tensor pi tensor Z=0,
Y tensor epsilon tensor gamma + alpha tensor pi tensor W
  =lambda_1 e_1 tensor e_1 tensor e_1.
```

Quotienting the first factor by `K alpha` is legitimate because
`alpha!=0`.  Since `alpha_2=0`, if its line is neither `Ke_0` nor `Ke_1`,
both target images remain nonzero.  The first equation forces
`gamma proportional e_0`, while the fourth forces
`gamma proportional e_1`, an impossibility.

If `alpha=e_1`, the four equations successively force

```text
delta,gamma proportional e_0,       epsilon=0,
pi,W proportional e_1,              Z=0,
Y=0,                                beta=0.
```

If `alpha=e_0`, they force the colour-swapped fork

```text
epsilon,gamma proportional e_1,     delta=0,
beta,Z proportional e_0,            W=0,
X=0,                                pi=0.
```

The nonzero target scalars affect only the nonzero proportionality constants,
not any vanishing or factor-line conclusion.

In both forks `alpha_2=gamma_2=0`, so modes `b,d` have no colour-2
`A` parts.  In the first fork `beta_2=epsilon_2=0`; in the second
`delta_2=pi_2=0`.  Because `A` is two-dimensional, `J` is nondegenerate,
and `J(p,q)=0`, these statements put the two remaining colour-2 columns on
the two mutually orthogonal lines `Kp,Kq`.  This remains valid when `p,q`
are proportional isotropic vectors.  Therefore

```text
J(A_a e_2,A_c e_2)=0.
```

No pair of modes can supply a nonzero `x_4,x_5` pairing in the pure `2222`
coefficient, contradicting the live `d_2` target.

### Companion in the second-`N` mode

Now the same mode `c` contains `N` at colour `1` and `q_-` at colour `2`.
Define one linear map `Theta:R^* ->` cubic tensors on the other three legal
slots.  Contracting `N` in mode `c` gives

```text
Theta(h_0)=0,                 Theta(h_1)!=0.
```

Contracting `q_-` in that same mode in a separate evaluation gives

```text
Theta(h_2)=Theta(h_2')=0.
```

The exact covector identity

```text
h_1=h_0+h_2-h_2'
```

then forces `Theta(h_1)=0`.  Both contractions use one vector in the same
single slot and are compared only through linearity of `Theta`; the proof
never inserts `N` and `q_-` into two tensor slots.

## 7. Tensor-slot, field, and quantifier audit

Every double contraction in the proof uses vectors from distinct local
modes: the propagated `N,q` pair, the two separate `N` modes, or a fixed
vector after the companion mode has already been contracted.  When `N` and
`q_-` share one mode, Section 5.2 uses separate single contractions and the
same linear `Theta`.  No illegal same-mode double contraction appears.

Characteristic zero is sufficient.  It keeps the factors `2` nonzero,
makes `M(M)=2` detect the live quotient direction, and supplies the field
scope of the predecessors.  The proof divides only by explicitly nonzero
support or projective scalars.  It uses no algebraic closure, square roots,
order, positivity, or genericity.

The finite-field computations in the audit stress rank-one alignment and
orthogonal-line geometry only.  They are not used as a characteristic-zero
case cover.  The proof is pointwise under the full exact target with every
`lambda_c!=0`.

The `q_+` residual geometry is different and is never fed into the
`q_-` quotient gate or collapsed-cycle equations.  Both executables and the
written scope retain `q_+` as open.

## 8. Computational replay and independence

Focused replay passed:

```text
new primary exact verifier:                            PASS;
new independent no-import audit:                       PASS;
kernel-support predecessor primary and audit:          PASS;
singleton-companion predecessor primary and audit:     PASS;
same-mode common-line predecessor primary and audit:   PASS;
support-two incidence context primary and audit:       PASS;
py_compile on new and predecessor scripts:             PASS;
Ruff on new and predecessor scripts:                   PASS;
tracked and untracked whitespace checks:                PASS.
```

The primary verifier uses SymPy to reconstruct all residual covectors,
their spans and common kernels, the identical double-`N` row, the
support-two sign identity, and the zero/live pair-gate algebra.  It compares
all `108` entries of the four collapsed-cycle tensors against direct
polarization and checks both coordinate forks and their final colour-2
pairing.

The independent audit imports neither the primary module nor SymPy.  It
rebuilds the quadratics as edge dictionaries, uses exact rational row
reduction and a separate complete-polarization implementation, checks the
support-word identities on independent exact samples, and compares `432`
collapsed-cycle tensor entries across four data sets.  Its `F_3` and `F_5`
rank-one and orthogonal-line runs are explicitly labelled audit-only.

## 9. Accepted boundary

```text
same-mode common kernel line N/N:                       ASSUMED;
singleton/support-two support of original N:            EXHAUSTIVE;
q_- with no second N:                                   EXCLUDED;
q_- with a distinct second singleton N:                 EXCLUDED;
q_- sharing the second-N mode:                          EXCLUDED;
all q_- companion placements:                           EXCLUDED;
q_+ companion branch:                                   OPEN;
all same-mode N/N incidences:                           NOT EXCLUDED;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                          UNRESOLVED.
```

## Final reviewed hashes

```text
new theorem:
3F4141CDE71069FB249025A0122C657F8F803DA922FDC47268181B5BE99D76D4

new primary verifier:
C6A42FB9978B8C10FBDA250DCEE47F6EBF017D3A0045B683FD414C998208BD01

new independent audit:
0DF945F10B1233CDD90F12BDD7A8AA0937B816282AC7D33F6DD0583D545553C0

kernel-support predecessor theorem:
7AEC9CD00DEBAC1D5CFA91D44E5D3634BD6D05FF8CA755BA1C2E83D1F8C3C45B

singleton-companion predecessor theorem:
EF703D8B5EA711945D6384A93F2542F8A84F2D5140FBB2B7D2F1CB944D25EA57

same-mode common/noncommon predecessor theorem:
05F1655F238025804309A8A0071BA0B53FE4BB5A250DE76DD5ABF15438FAF990

support-two incidence context theorem:
8C6B0EB9AA3BDD885A0703AB1EE902456045A7DEA89B66E0C097654F1189631F
```
