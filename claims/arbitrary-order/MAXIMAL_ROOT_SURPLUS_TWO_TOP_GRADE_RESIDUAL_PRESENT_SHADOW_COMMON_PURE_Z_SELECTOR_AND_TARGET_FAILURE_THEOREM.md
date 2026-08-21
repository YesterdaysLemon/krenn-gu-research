# Maximum-root surplus-two top-grade residual-present shadow, common pure-Z selector, and target failure

## Status

**Exact characteristic-zero arbitrary-root, all-even-target module theorem.**
In the original surplus-two fixed-`Q` chart, let an even target have size
`|S|=2t`.  Leave exactly `t` roots open and evaluate all other roots at the
maximum root.  Every companion grade greater than `t` vanishes.  The
residual-present desired column has grade `t` and becomes an explicit
injection/permanent top tensor.

For the individual `Z` target quotient, the residual-absent desired column is
nuisance.  Adjoining its shadow to the complete joint nuisance therefore
gives an exact smaller quotient.  Survival of the top residual-present class
in this quotient supplies a legal normalized pure-`Z` coefficient row
`(0,1)`.  A finite family of surviving targets has the same coefficient
direction even when some complete joint spaces have rank two.

Applying the same top shadow to the complete GHZ witness equation gives

```text
sum_c alpha_c [d_(A,S,c)^Z] tensor w_(S,c)
  =c_(A,S) tensor Z_S.                                (1)
```

Thus the pure top quotient has rank at most one and is useful exactly when
both the desired top class and physical residual-present response are
nonzero.  Universal failure on all residual contractions and all nuisance-
rank fibres is exactly a geometric radical--Fitting containment profile.

At root order four, pair targets leave one root open and the four-port target
leaves two.  The four-port top tensor is the sum of the two cross-matchings
between the open and closed root pairs.  If all six pair targets and the
four-port target have useful top shadows at one residual point, their legal
rows share the pure-`Z` direction.  In GLD16 its effective scalar is `a=h`,
and the already-proved arbitrary-`h` detector excludes the branch only under
its separate three-colour activity gate, including both `h=0` and `h!=0`.

The theorem does **not** force any top class or response to survive, exclude
the simultaneous top-absorption branch, prove selected-response activity,
establish GLS15 foreign transport, or integrate the distinct GLS8 promoted
module.  It does not close the strategic node.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## Dependencies and provenance

The original fixed-`Q` companion grades and maximum-root vanishing come from

- [`GLS2`](MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md).

The exact joint quotient, its individual-`Z` nuisance

```text
N_S^Z=N_S^(MZ)+K g_S^M,
```

and the complete target equation come from

- [`GLD15`](FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md).

The all-rank geometric failure method comes from

- [`GLS5`](MAXIMAL_ROOT_SURPLUS_TWO_POINTWISE_SELECTOR_FAILURE_AND_DECOMPOSABLE_RETRACTION_BOUNDARY_THEOREM.md).

The conditional four-root common-line consequence uses

- [`GLD16`](FIXED_Q_COMMON_PROJECTIVE_JOINT_RESPONSE_SELECTOR_AND_SHIFTED_GLD3_DETECTOR_THEOREM.md).

No external literature claim is used.  The new content is the `t`-open-root
top shadow, its explicit residual-present tensor, the common pure-`Z` route,
and its response-gated target/Fitting profile.

## 1. Top-grade shadow

Work over a characteristic-zero field `K`.  Let

```text
R={1,...,r},              |R|=r>=2,
B=Q disjoint-union U,     |Q|=2,       |U|=r,         (2)
```

with fully supported maximum-root vectors `x_i` satisfying

```text
W_ij(x_i,x_j)=0                     for i!=j.          (3)
```

Fix fully supported residual vectors `z_Q`.  For

```text
empty!=S subset U,       |S|=2t,       C=U-S,         (4)
```

retain the GLD15 desired columns

```text
g_S^M=G_(Q union C)(z_Q),       grade t-1,
g_S^Z=G_C,                      grade t,              (5)
```

in

```text
L_S^*=(tensor_(i in R)V_i^*) tensor
      (tensor_(u in C)V_u^*).                         (6)
```

Let `N_S^J=N_S^(MZ)` be the complete joint nuisance and

```text
N_S^Z=N_S^J+K g_S^M                                  (7)
```

the exact individual-`Z` nuisance.

Choose

```text
A subset R,                 |A|=t,                    (8)
```

leave the roots of `A` open, and contract every root in `R-A` with its
maximum-root vector.  Denote the resulting map by

```text
epsilon_(A,S)^Z:L_S^* ->
 E_(A,S)^Z=(tensor_(a in A)V_a^*) tensor
           (tensor_(u in C)V_u^*).                    (9)
```

Put

```text
Theta_(A,S)=epsilon_(A,S)^Z(g_S^Z),
N_(A,S)^Ztop=epsilon_(A,S)^Z(N_S^Z),
c_(A,S)=[Theta_(A,S)] in
  overline E_(A,S)^Z=E_(A,S)^Z/N_(A,S)^Ztop.         (10)
```

For an injection

```text
tau:A -> R-A,                                         (11)
```

define

```text
R_tau=product_(a in A) W_(a,tau(a))(-_a,x_(tau(a))). (12)
```

The unused root set

```text
R_tau^0=R-(A union tau(A))                            (13)
```

has size `r-2t=|C|`.  Let `Per_(tau;C)` be the permanent assigning these
unused roots to `C`, with root slots evaluated at `x` and the `C` slots open.

### Theorem 1 (residual-present top-grade shadow)

For every `A,S` as above,

```text
Theta_(A,S)=sum_(tau:A -> R-A injective)
              R_tau tensor Per_(tau;C).               (14)
```

Every companion of grade greater than `t` vanishes under (9).  Moreover
`N_(A,S)^Ztop` is exactly the span of

1. `epsilon_(A,S)^Z(g_S^M)`; and
2. the partial-root coefficient slices of every joint-nuisance label `I`
   satisfying

   ```text
   2<=|I|<=2t+2,       |I| even,
   I notin {S,Q union S}.                             (15)
   ```

Every nuisance label of order at least `2t+4` is killed.  Hence (9) induces

```text
bar epsilon_(A,S)^Z:
 L_S^*/N_S^Z -> overline E_(A,S)^Z                   (16)
```

with

```text
bar g_M |->0,                 bar g_Z |->c_(A,S).    (17)
```

#### Proof

A companion matching of grade `p` has `p` disjoint root--root edges.  A root
edge survives (9) only if at least one endpoint lies in `A`; a closed--closed
edge evaluates to zero by (3).  The `t` open roots meet at most `t` disjoint
edges, so every grade `p>t` vanishes.

The residual-present column has exactly `t` root edges.  In a surviving
matching every edge meets `A`.  Since there are as many edges as open roots,
each edge has exactly one endpoint in `A`: an edge internal to `A` would use
two open roots and leave too few open roots to meet the remaining disjoint
edges.  The closed endpoints therefore give an injection (11), and the unused
closed roots are bijected to `C`.  This construction is reversible and
multiplicity preserving, proving (14).

Apply the same grade cutoff to the complete joint nuisance.  The grade rule
`p=(|I|-2)/2` retains exactly (15); the two desired labels were removed from
the joint nuisance.  Adjoining `g_S^M` is exactly the individual-`Z` nuisance
(7).  This proves the nuisance description and the induced map (16)--(17).
`square`

## 2. Common pure-Z operator supply

Recall the complete operator-coefficient space

```text
C_S={
 (lambda(g_S^M),lambda(g_S^Z)):
 lambda in (N_S^J)^perp
} subset K^2.                                         (18)
```

### Theorem 2 (top survival forces the pure-Z row)

If

```text
c_(A,S)!=0,                                           (19)
```

then

```text
(0,1) in C_S.                                         (20)
```

Equivalently, there is a legal constant functional annihilating the complete
joint nuisance and `g_S^M` while taking `g_S^Z` to one.  More precisely,

```text
k_S=1  => C_S=K(0,1),
k_S=2  => C_S=K^2.                                    (21)
```

Conversely, if `(0,1) notin C_S`, then

```text
c_(A,S)=0                  for every A in binom(R,t). (22)
```

#### Proof

Condition (19) says `Theta_(A,S)` does not lie in the image of the individual-
`Z` nuisance.  A quotient functional nonzero on its class, composed with
(9), annihilates `N_S^Z=N_S^J+K g_S^M` and is nonzero on `g_S^Z`.  Normalize
its second coefficient to one; this gives (20).

At joint rank one, the coefficient line containing `(0,1)` is exactly the
pure-`Z` line.  At rank two the coefficient space is `K^2`.  Finally, absence
of `(0,1)` is equivalent by finite-dimensional duality to
`g_S^Z in N_S^J+K g_S^M`; every induced quotient (16) then kills its class,
proving (22).  No projective coordinate is divided out.  `square`

### Corollary 2.1 (finite-family common pure-Z direction)

Let `F` be a finite family of nonempty even targets.  If every `S in F` has
some `A_S in binom(R,|S|/2)` satisfying (19), then

```text
(0,1) in intersection_(S in F) C_S.                  (23)
```

The legal functional may depend on `S`, but the graph, `Q`, residual point,
and coefficient direction do not.

## 3. Complete-target coupling and all-rank failure

For a colour `c in {0,1,2}`, put

```text
kappa_(A,c)=product_(i in R-A)e_(i,c)^*(x_i) !=0,
d_(A,S,c)^Z=kappa_(A,c)
 (tensor_(a in A)e_(a,c)^*) tensor
 (tensor_(u in C)e_(u,c)^*) in E_(A,S)^Z.             (24)
```

The fully supported residual weights are

```text
alpha_c=product_(q in Q)e_(q,c)^*(z_q) !=0,
w_(S,c)=tensor_(u in S)e_(u,c)^*.                     (25)
```

### Theorem 3 (top-shadow witness coupling)

On every complete hypothetical-witness point,

```text
sum_(c=0)^2 alpha_c[d_(A,S,c)^Z] tensor w_(S,c)
  =c_(A,S) tensor Z_S.                                (26)
```

Consequently the pure top quotient rank

```text
q_(A,S)^Z=dim span{[d_(A,S,c)^Z]:c=0,1,2}            (27)
```

satisfies `q_(A,S)^Z<=1`, and the following are equivalent:

1. `q_(A,S)^Z=1`;
2. at least one pure top class is nonzero;
3. `c_(A,S)!=0` and `Z_S!=0`.

If these conditions hold, the pure-`Z` row of Theorem 2 is legal and has the
named nonzero physical output `Z_S`.  If `c_(A,S)=0` or `Z_S=0`, all three
pure top classes lie in `N_(A,S)^Ztop`.  Whenever `c_(A,S)!=0`, equation (26)
also forces every mixed target-word coordinate of `Z_S` to vanish.

#### Proof

Apply (16) to the complete GLD15 witness equation

```text
sum_c alpha_c[d_(S,c)] tensor w_(S,c)
  =bar g_M tensor M_S+bar g_Z tensor Z_S.             (28)
```

The pure root/complement column maps to (24), while (17) kills `bar g_M` and
sends `bar g_Z` to `c_(A,S)`.  This gives (26).  The right side is
decomposable.  The `w_(S,c)` are independent and every `alpha_c` is nonzero,
so its left flattening has rank (27), is nonzero exactly when one pure class
survives, and equals a nonzero tensor exactly when both right factors are
nonzero.  The equivalences and absorption conclusion follow.  Finally compare
(26) in a mixed target word: the left side has no such coordinate, so its
right coefficient is `c_(A,S)` times that coordinate of `Z_S`.  `square`

Let the residual contraction vary on its Laurent torus `T_Q=Spec Lambda` and
work geometrically after extending to the algebraic closure.  In fixed bases,
let

```text
B_(A,S)^Z(z)
```

have columns spanning `N_(A,S)^Ztop(z)`, and put

```text
D_(A,S)^Z=[d_(A,S,0)^Z|d_(A,S,1)^Z|d_(A,S,2)^Z].     (29)
```

Define

```text
U_(A,S)^Z={z in T_Q:
 rank[B_(A,S)^Z(z)|D_(A,S)^Z]>rank B_(A,S)^Z(z)}.    (30)
```

### Theorem 4 (all-rank top-shadow Fitting criterion)

On the complete witness locus, `U_(A,S)^Z` is exactly the set where

```text
c_(A,S)(z)!=0,                 Z_S(z)!=0.             (31)
```

For every `1<=j<=dim E_(A,S)^Z`, the useful locus is empty exactly when

```text
I_j([B_(A,S)^Z|D_(A,S)^Z])
 subset sqrt_geom(I_j(B_(A,S)^Z))       for every j.  (32)
```

On a declared principal open `D(rho)`, its intersection with the useful locus
is empty exactly when

```text
rho I_j([B_(A,S)^Z|D_(A,S)^Z])
 subset sqrt_geom(I_j(B_(A,S)^Z))       for every j.  (33)
```

These statements include every nuisance-rank drop and exceptional residual
fibre.  For an activity ideal `(p_1,...,p_m)`, apply (33) separately to every
`rho=p_i`; replacing the union of principal opens by their product is not
valid.

#### Proof

Theorem 3 identifies rank rise with (31).  At a point of nuisance rank `j-1`,
adjoining the pure columns raises rank exactly when every `j`-minor of the
nuisance vanishes and some `j`-minor of the augmented matrix does not.  Union
over `j` and apply the Laurent Nullstellensatz.  Intersecting with `D(rho)`
multiplies each augmented minor by `rho`, giving (33) without choosing or
inverting a minor.  `square`

For a finite target family, simultaneous usefulness at one shared residual
point is the finite union, over choices `A_S in binom(R,|S|/2)`, of the
incidence loci

```text
intersection_(S in F) U_(A_S,S)^Z.                   (34)
```

This is an exact finite formulation, not a claim that a locus in (34) is
empty or nonempty.

## 4. Four-root pure-Z route

Take `r=4` and `U={1,2,3,4}`.

For a pair target `S`, `t=1`, choose `A={a}`, and let `C=U-S`.  Formula (14)
is

```text
Theta_(a,S)=sum_(j in R-{a})
 W_aj(-_a,x_j) Per_(R-{a,j};C),                       (35)
```

where the remaining two roots are bijected to the two ports of `C`.  Its
ambient space has dimension `3^3=27`.  The three pure tensors (24) are
independent but do not span that space.

For the four-port target `S=U`, `t=2`.  If `A={a,b}` and `R-A={c,d}`, then

```text
Theta_(ab,U)=
 W_ac(-_a,x_c) tensor W_bd(-_b,x_d)
 +W_ad(-_a,x_d) tensor W_bc(-_b,x_c)                  (36)
```

in the nine-dimensional space `V_a^* tensor V_b^*`.  The three pure tensors

```text
kappa_(A,e)e_(a,e)^* tensor e_(b,e)^*,       e=0,1,2 (37)
```

span only its three-dimensional diagonal subspace.

### Corollary 4.1 (conditional seven-target pure-Z synchronization)

Suppose one residual point has, for every six pair targets and `U`, a choice
of top shadow for which (31) holds.  Then all seven targets have legal nonzero
rows with the common coefficient direction

```text
(delta,eta)=(0,1),                a=delta+h eta=h.     (38)
```

If the selected pair package also satisfies GLD16's three-colour pair-depth
activity at one port, the complete mixed target is contradicted.  At `h=0`
this is GLD16's three-active rank contradiction; at `h!=0` it is the shifted
nine-word detector.  No division by `h` occurs.

#### Proof

Theorem 3 and Corollary 2.1 supply the seven legal nonzero pure-`Z` rows.
Substitute (38) in GLD16's denominator-free identity

```text
aT'=C(aB+eta K)-C(eta K).
```

The two `h` branches and their activity-based contradictions are exactly the
proved GLD16 theorem.  `square`

The failure alternative is equally exact: if a target lacks a pure-`Z` row,
then every top class (14) and all three pure tensors (24) are absorbed by the
complete top nuisance including the `M` shadow.  Equations (35)--(37) do not
turn that absorption into fullness of the 27- or 9-dimensional ambient space.

## 5. Exact frontier

```text
t-open-root grade cutoff and top tensor (14):                PROVED;
complete individual-Z top nuisance through order 2t+2:      PROVED;
top survival forces legal pure-Z operator row:               PROVED;
finite-family survival gives common pure-Z direction:        PROVED;
complete-target rank-one coupling (26):                      PROVED;
all-rank geometric radical-Fitting criterion:                PROVED;
r=4 pair and four-port explicit top tensors:                 PROVED;
r=4 seven useful top shadows plus activity excluded:         PROVED CONDITIONAL;
some useful top shadow forced on every witness:              UNKNOWN;
simultaneous M-leading and Z-top failure excluded:           UNKNOWN;
three-colour selected-response activity:                     UNKNOWN;
GLS15 foreign transport on the failure locus:                UNKNOWN;
GLS8 promoted source integration:                            OPEN;
complete maximum-root supply/attachment node:                OPEN;
global Krenn--Gu conjecture:                                 UNRESOLVED.      (39)
```

The smallest next obligation is now two-sided and target-coupled: for a
sufficient target family, force either a useful GLS18 pure-`M` leading shadow
or a useful pure-`Z` top shadow at one shared residual point, or contradict
the simultaneous radical--Fitting failure profiles by complete mixed GHZ
coefficients.  Unequal/oblique projective lines and selected-response activity
remain separate, as does the promoted GLS8 source interface.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_top_grade_residual_present_shadow_common_pure_z_selector_and_target_failure.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_top_grade_residual_present_shadow_common_pure_z_selector_and_target_failure.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_top_grade_residual_present_shadow_common_pure_z_selector_and_target_failure.py claims/arbitrary-order/audit_maximal_root_surplus_two_top_grade_residual_present_shadow_common_pure_z_selector_and_target_failure.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_top_grade_residual_present_shadow_common_pure_z_selector_and_target_failure.py claims/arbitrary-order/audit_maximal_root_surplus_two_top_grade_residual_present_shadow_common_pure_z_selector_and_target_failure.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_top_grade_residual_present_shadow_common_pure_z_selector_and_target_failure.py claims/arbitrary-order/audit_maximal_root_surplus_two_top_grade_residual_present_shadow_common_pure_z_selector_and_target_failure.py
```

The primary verifier enumerates explicit matching tuples, checks the top-grade
injection formula and all higher-grade cutoffs through root order seven,
replays exact quotient/response ranks and Fitting tables, and checks the two
four-root formulas.  The independent no-import audit uses recursive bitmask
matchings through root order eight, finite-field target-word and gated
vanishing-set tables, and a separate sparse four-root representation.  These
programs audit bounded combinatorics and linear algebra; the arbitrary-root
matching bijection, quotient duality, and Laurent Nullstellensatz argument
above are the proofs.
