# Four-root complete Q-layer secant boundary trap and torus-star compression

## Status

**Exact complex parent reduction, complete nuisance map, and certified
root-torus star compression.**  This is the first successor to `GLD69` that
keeps all nine labels meeting `Q` in one object.  It does not exclude that
object from the target.

The complete contracted nuisance space is the image of one explicit
`79`-column map.  A degree-three epsilon contraction cuts the honest concise
three-colour GHZ orbit out of the third Segre secant: over `C`,

```text
GHZ_3 = sigma_3(Segre((P^2)^4)) intersect D_P(epsilon).     (1)
```

Consequently, trapping every third-secant point of the nuisance space on
`epsilon=0` is a basis-independent sufficient contradiction.  Yang Qi's
set-theoretic equations turn that statement into one exact ideal saturation
using flattening minors **and** Strassen equations.  Balanced flattening
minors alone are only a potentially stronger shortcut, not a proved complete
test.

There is also a genuine physical compression.  If every coordinate of the
two residual vectors is nonzero and the common residual form has rank two,
then the residual pair has, up to root permutation, root-diagonal gauge, and
irrelevant residual scalings, the unique ratio pattern

```text
(xi_i/eta_i)_i = (1,1,1,-1).                            (2)
```

On a maximal star, the remaining nonisotropic quotient slope `h!=0` produces
the **same** complete nuisance space for every `h`: one fixed
`44`-dimensional subspace of the `81`-dimensional four-qutrit tensor space.
Thus the entire root-torus maximal-star family has been reduced to one exact
fixed-space question,

```text
N_star intersect GHZ_3 = empty ?                         (3)
```

Equivalently, the restricted third-secant ideal must force `epsilon=0`.
This radical-membership calculation has not been completed.  The
projection-full triangle gives a different `35`-dimensional nuisance space
with a `16`-dimensional quotient beyond the pair layer; it has not been
compressed to (3).  Scalar-zero stars, residual coordinate boundaries,
lower port ranks, smaller survivor families, other root orders, and
non-leading/promoted source supply remain open.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

The internal-pair geometry and its rank-three hypotheses come from the
[`GLD69` common-incidence theorem](FOUR_ROOT_MAXIMAL_BASE_SURVIVOR_COMMON_INCIDENCE_AND_SPARSE_RADICAL_DETECTOR_BOUNDARY_THEOREM.md).
The secant normal forms and equations imported below are recorded in the
repository literature registry.

## 1. The complete 79-column Q-layer map

Let

```text
U={0,1,2,3},                    E_u=C^3,
X=C^4,                          W=tensor_(u in U) E_u^*.
```

Retain the notation of `GLD69`.  The fully supported residual contraction
gives vectors `xi,eta in X`; each port gives a rank-three map

```text
A_u:E_u -> X;
```

and `P_4:X^4->C` is the symmetric four-linear permanent form.  Define the
four-port tensor

```text
Q_A=P_4(A_0-,A_1-,A_2-,A_3-) in W.                    (4)
```

For `r in {xi,eta}` and `u in U`, define the three-port companion

```text
K_u^r=P_4(r,(A_v-)_(v!=u)) in tensor_(v!=u) E_v^*.    (5)
```

Finally, for a port pair `I={u,v}` with complement `{w,x}`, put

```text
B_I=P_4(xi,eta,A_w-,A_x-) in E_w^* tensor E_x^*.      (6)
```

After contracting the two residual target slots, the complete order-two
nuisance space is

```text
N_full = <Q_A>
       + sum_(r in {xi,eta}) sum_(u in U) E_u^* tensor K_u^r
       + sum_(I in binom(U,2)) E_I^* tensor B_I.       (7)
```

The three displayed layers have respectively

```text
1,  2*4*3=24,  6*3^2=54                           (8)
```

raw columns.  Dependencies are retained; `79` is a presentation size, not a
dimension claim.  The last summand is exactly the pair layer `P_U` of
`GLD69`.  The first two summands are exactly the nine formerly open labels:
the label `Q` and the eight residual--port labels.

If a complete contracted maximal-profile coefficient identity exists, its
weighted target

```text
Delta_omega=sum_(c=0)^2 omega_c e_(c,0)^* tensor ... tensor e_(c,3)^*,
omega_0 omega_1 omega_2 !=0,                           (9)
```

belongs to `N_full`.  Equation (7), rather than the pair-layer quotient by
itself, is therefore the exact parent object.

## 2. The epsilon open orbit

Choose volume forms on the four ternary factors.  For `T in W`, define

```text
epsilon(T)=
 sum_(sigma_0,...,sigma_3 in S_3)
   product_(u in U) sgn(sigma_u)
   product_(c=0)^2
     T_(sigma_0(c),sigma_1(c),sigma_2(c),sigma_3(c)).  (10)
```

This is a homogeneous cubic relative invariant.  Independent local changes
of basis `g_u` give

```text
epsilon((tensor_u g_u)T)=product_u det(g_u) epsilon(T). (11)
```

Write `GHZ_3` for the projective `GL(E_0) x ... x GL(E_3)` orbit of
`[d_0+d_1+d_2]`, and write `D_P(epsilon)` for the projective principal open
on which the homogeneous invariant is nonzero.  A hat on a projective variety
will denote its affine cone in `W`.

### Lemma 2.1 (value on an honest rank-three decomposition)

For

```text
T=sum_(c=0)^2 lambda_c
    a_(0c) tensor a_(1c) tensor a_(2c) tensor a_(3c), (12)
```

one has

```text
epsilon(T)=6 lambda_0 lambda_1 lambda_2
  product_(u in U) det[a_(u0) a_(u1) a_(u2)].         (13)
```

#### Proof

Expand the three copies of `T` in (10).  A determinant in any mode vanishes
unless the three selected colours are distinct.  The common colour selection
is therefore one of the six permutations of `{0,1,2}`.  Each contributes the
same product in (13).  `square`

In particular,

```text
epsilon(Delta_omega)=6 omega_0 omega_1 omega_2 !=0.   (14)
```

### Theorem 2.2 (epsilon cuts out the GHZ open inside the third secant)

Let

```text
X_Seg=Segre(P(E_0^*) x ... x P(E_3^*)).
```

Over `C`, equation (1) holds set-theoretically.

#### Proof

Lemma 2.1 proves the assertion on an honest sum of three Segre points.  It is
nonzero exactly when all three weights are nonzero and the three local
vectors form a basis in every mode, which is exactly the concise GHZ orbit.

Buczynski--Landsberg, Theorem 1.2 and normal forms (1.2)--(1.5), classify
every point of `sigma_3(X_Seg)-sigma_2(X_Seg)` into four types.  Type (i) is
the honest sum just treated.  In type (ii), one selected monomial must supply
the third local vector in all four modes, while the two remaining tangent
monomials can supply the second local vector in at most two modes.  Hence at
least one determinant in (10) repeats its first local vector.  In types (iii)
and (iv), a monomial carrying the third local vector does so in only one
mode.  Three selected monomials cannot supply that vector in all four modes.
Thus `epsilon=0` on each boundary normal form.  It also vanishes on the dense
honest sums of at most two points and hence on their closure `sigma_2`.
This proves (1).  `square`

The normal-form classification is imported only over the complex numbers,
which is sufficient for the complex-weight Krenn--Gu problem.  No
characteristic-free version is inferred.

## 3. Exact secant-boundary trap

Let `b:C^79->W` be the linear map whose columns are (7).  Theorem 2.2 gives
the exact equivalence

```text
P(N_full) intersect sigma_3(X_Seg) subset V_P(epsilon)
  <=> N_full contains no concise GHZ tensor.           (15)
```

Since (9) is a concise GHZ tensor, either side of (15) is a sufficient
contradiction to the complete contracted identity.

This is deliberately one-way at graph level.  A failure of (15) supplies a
GHZ-orbit tensor in the nuisance space, not necessarily the particular
weighted diagonal of a graph and not a graph witness.

Yang Qi, Theorem 1.4, gives homogeneous equations whose projective zero set is
the third secant and whose affine zero set is its cone
`widehat(sigma_3(X_Seg))`.  In the present four-factor, three-dimensional
setting they consist of the `4 x 4` generalized-flattening minors together
with the degree-four Strassen equations for the partitions

```text
{i} | {j} | (U-{i,j}).                               (16)
```

Pull these equations back along `b` and write

```text
I_N=b^* I_sec subset C[z_1,...,z_79],
e_N=epsilon(b(z)).                                    (17)
```

Hilbert's Nullstellensatz and Theorem 2.2 give

```text
P(N_full) intersect GHZ_3 = empty
  <=> (I_N : e_N^infinity)=<1>
  <=> e_N belongs to radical(I_N).                    (18)
```

Here `V(I_N)=b^(-1)(widehat(sigma_3(X_Seg)))` set-theoretically in the affine
parameter space.  Points in `ker b` have `e_N=0` and disappear on the
principal open, so the affine saturation and projective intersection in (18)
match exactly.

Thus (18) is a finite exact proof obligation.  A certificate may exhibit an
integer `m` and an identity `e_N^m in I_N`; a sound exact checker can replay
that identity without trusting the elimination program that found it.

Every tensor in `sigma_3` has rank at most three in each balanced
`2|2` flattening.  Therefore the stronger implication

```text
T in N_full and epsilon(T)!=0
  => some balanced flattening of T has rank at least 4 (19)
```

would close (15) using minors alone.  The converse use is forbidden: the
balanced minors do not, in general, replace all of Qi's Strassen equations.
Neither (18) nor (19) is proved here.

## 4. Full-support residual rank-two classification

Assume for this section that

```text
xi_i eta_i !=0 for every root coordinate i,
rank J=2,                    J=P_4(xi,eta,-,-).        (20)
```

### Theorem 4.1 (unique root-torus ratio pattern)

Under (20), equation (2) holds after a root-coordinate permutation and a
nonzero common rescaling of the four ratios.

#### Proof

A root-diagonal change multiplies every four-linear permanent evaluation in
(4)--(7) by one common determinant.  It therefore preserves `N_full`
projectively.  Apply `diag(eta_i^(-1))` and put

```text
eta=(1,1,1,1),                 r_i=xi_i/eta_i.
```

For distinct `i,j`, with complementary coordinates `{k,l}`,

```text
J_ij=r_k+r_l,                  J_ii=0.                (21)
```

The disjoint-support factorization proved in `GLD69` writes a rank-two
zero-diagonal symmetric form as

```text
J=kappa(ell tensor m+m tensor ell),
supp(ell) intersect supp(m)=empty.                    (22)
```

The two supports cover all four coordinates.  Otherwise a zero row in `J`
would make every pair among the other three ratios sum to zero, which in
characteristic zero forces those nonzero ratios to vanish.

The support partition cannot have size `2+2`.  If its parts are
`{0,1}` and `{2,3}`, the within-part zeros in (21) give, after relabelling,

```text
(r_0,r_1,r_2,r_3)=(a,-a,b,-b),       ab!=0.
```

But the cross block of (21) then has determinant `-4ab`, whereas (22) makes
that cross block an outer product of rank one.  This is a contradiction.

The partition is therefore `1+3`.  If `3` is the singleton, every pair in
the other part has zero `J` entry.  Equation (21) then says

```text
r_0=r_1=r_2=-r_3.
```

Scale `xi` and permute the singleton to obtain (2).  `square`

The theorem is a root-torus statement.  It does not cover a zero coordinate
of `xi` or `eta`; the scalar-zero control below lies precisely outside its
scope.

## 5. One fixed nuisance space for every torus star

Use the canonical residual pair

```text
xi=(1,1,1,-1),                  eta=(1,1,1,1).
```

Then

```text
R=rad J=< (1,-1,0,0), (1,0,-1,0) >.                 (23)
```

On the maximal-star profile, `GLD69` says that the centre and leaf images are
`R` plus orthogonal nonisotropic quotient lines.  After scaling
representatives, choose port bases

```text
A_0(h)=[r_0,r_1,(1,0,0,h)],
A_i(h)=[r_0,r_1,(1,0,0,-h)],       i=1,2,3,          (24)
```

where `h!=0`.  Independent changes of the four port bases act on `W` by
local `GL_3` and preserve the orbit condition (15).

### Theorem 5.1 (exact torus-star family compression)

Let `N_star(h)` be (7) for (24).  For every `h!=0`,

```text
N_star(h)=N_star(1),                 dim N_star(1)=44. (25)
```

The pair layer has dimension `21`, the residual-plus-`Q` layer has dimension
`24`, and

```text
dim(N_star/P_U)=23.                                  (26)
```

#### Proof and certificate semantics

Every entry of each of the `79` raw columns is affine in `h`: every occurrence
of `h` lies in the fourth root coordinate, and a nonzero permanent monomial
uses that root row at most once.  Exact row
reduction at `h=1` produces a `44`-column basis and a `37`-dimensional left
annihilator.  Direct coefficient comparison shows that this annihilator kills
both the constant and linear coefficient of every raw column.  Hence
`N_star(h) subset N_star(1)` for every `h`.

On the pinned `44` columns and `44` tensor coordinates recorded by the
primary verifier, the determinant is

```text
510015580149921683079168 h^33.                        (27)
```

It is nonzero for `h!=0`, so the inclusion has equal dimension and is an
equality.  The checker proves (27) without a symbolic-algebra dependency:
each matrix entry is affine, so the determinant has degree at most `44`; it
checks the displayed polynomial at `45` exact integer values.  The
independent audit reconstructs the permanent by subset dynamic programming,
reverses the raw-label traversal, and checks the fixed space at six signed
slopes.  The written affine-degree argument and primary exact certificate,
not the audit samples by themselves, prove (25).  The layer ranks give (26).
`square`

Theorem 5.1 is the promised reduction from an infinite physical family to
one fixed orbit-intersection calculation.  It is not the calculation's
answer.

## 6. Exact controls and sharp boundary

Let `D=<d_0,d_1,d_2>` be the three-dimensional coordinate-diagonal space,
where `d_c=e_c^* tensor4`.  The primary and independent constructions give:

| physical control | `rank(R_xi+R_eta+Q)` | `rank P_U` | `rank N_full` | `rank(N_full+D)` |
|---|---:|---:|---:|---:|
| scalar-zero star | 16 | 21 | 21 | 24 |
| root-torus star | 24 | 21 | 44 | 46 |
| projection-full triangle | 22 | 19 | 35 | 38 |

Thus the residual-plus-`Q` quotient is not a small factorwise radical
quotient.  It contributes `23` dimensions beyond `P_U` on the torus star and
`16` on the displayed triangle.  In particular, the triangle value is `16`,
not `15`; the `Q` column supplies the additional direction.

The cubic epsilon invariant is also not, by itself, a separator.  On the
root-torus star, the single `Q` generator satisfies

```text
epsilon(Q_A)=-288,
rank_(01|23)(Q_A)=rank_(02|13)(Q_A)=rank_(03|12)(Q_A)=5. (28)
```

So `N_star` contains epsilon-nonzero tensors.  This does not refute (15): the
same tensor violates the flattening equations and is outside `sigma_3`.
Equation (28) is why the next proof must combine epsilon with secant equations
rather than search for another scalar invariant in isolation.

In the displayed canonical bases, adjoining the three diagonal words gives
ranks

```text
scalar-zero star:             21 -> 24,
root-torus star:              44 -> 46,
projection-full triangle:     35 -> 38.               (29)
```

For the torus star, `d_2` already lies in the nuisance space while `d_0` and
`d_1` add two directions.  These are exact coordinate controls, not a
basis-independent GHZ-orbit decision.

## 7. Best next proof-producing targets

The smallest high-leverage successor is no longer another star or triangle
incidence lemma.  It is one of the following two certificates for the fixed
space `N_star=N_star(1)`:

1. prove (19), equivalently show that the ideal of all balanced `4 x 4`
   minors on `N_star` forces `epsilon=0`; or
2. if that stronger claim fails, use the complete restricted Qi ideal and
   certify `epsilon^m in I_N` as in (18).

The first route is cheaper and should be tested first, but a failed search or
a finite-field sample is not a proof.  An exact tensor in `N_star` with all
balanced ranks at most three and `epsilon!=0` would refute route 1 and must be
tested against the Strassen equations before it is called a third-secant
survivor.

In parallel, the root-coordinate boundary of Theorem 4.1 and the general
triangle centre require their own finite canonical atlases.  They should feed
the same secant-boundary language, rather than restarting targetwise sibling
calculations.  Lower port rank, fewer than three surviving base classes,
non-leading/promoted rows, response activity, arbitrary-root coverage, and
permanent consequences remain separate obligations.

## Verification

Run

```text
python claims/arbitrary-order/verify_four_root_complete_q_layer_secant_boundary_trap_and_torus_star_compression.py
python -I claims/arbitrary-order/audit_four_root_complete_q_layer_secant_boundary_trap_and_torus_star_compression.py
python -m py_compile claims/arbitrary-order/verify_four_root_complete_q_layer_secant_boundary_trap_and_torus_star_compression.py claims/arbitrary-order/audit_four_root_complete_q_layer_secant_boundary_trap_and_torus_star_compression.py
uv run --with ruff ruff check claims/arbitrary-order/verify_four_root_complete_q_layer_secant_boundary_trap_and_torus_star_compression.py claims/arbitrary-order/audit_four_root_complete_q_layer_secant_boundary_trap_and_torus_star_compression.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_four_root_complete_q_layer_secant_boundary_trap_and_torus_star_compression.py claims/arbitrary-order/audit_four_root_complete_q_layer_secant_boundary_trap_and_torus_star_compression.py
```

The primary verifier constructs all `79` columns, checks the three exact rank
controls, verifies the epsilon formula on an honest decomposition, checks
representative tensors of the four secant normal-form types, certifies the
`44`-space identity (25)--(27), and replays (28).  Exhaustiveness of the
boundary types comes from the imported classification and the written
argument, not from those representative computations.  The no-import
audit uses a different permanent algorithm and label traversal, evaluates the
full `6^4` epsilon contraction, independently obtains the corrected ranks,
checks six torus-star slopes, and exhausts the rank-two nonzero-ratio
classification over `F_7`.  That finite-field census audits the formulas; the
written characteristic-zero proof establishes Theorem 4.1.

## External provenance

- Jaroslaw Buczynski and J. M. Landsberg,
  [*On the third secant variety*](https://arxiv.org/abs/1111.7005),
  Theorem 1.2 and normal forms (1.2)--(1.5), supply the four complex secant
  normal-form types used in Theorem 2.2.
- Yang Qi,
  [*Equations for the third secant variety of the Segre product of n projective spaces*](https://arxiv.org/abs/1311.2566),
  Theorem 1.4, supplies the set-theoretic flattening-plus-Strassen equations
  used in (16)--(18).

The repository usages, assumptions, inspection locators, and limitations are
recorded in `catalog/literature/sources.json`.
