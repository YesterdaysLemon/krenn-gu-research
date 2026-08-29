# Maximum-root surplus-two zero-anchor eta-zero permanent source and two-two local-rank localization

## Status

**Exact characteristic-zero same-source restriction theorem (`GLS65`).**
Continue from the `GLS64` exactly-two-deficient residual on
`W_(nm)(e_c,e_c)=0`.  Contract the two deficient labels at their common
kernel line and leave the four injective nonaxis ports open.  The complete
source is exactly a separated restriction of the fourth-order permanent
tensor:

```text
(tensor_(i in U) L_i(z_0,z_1)) P_4
 =kappa z_(0,c)z_(1,c) tensor_(i in U)e_(i,c)^*,
kappa!=0.                                                (1)
```

The four local maps have rank at least two.  The exact `P_4` rank-drop
theorem therefore supplies at least two generic rank-two ports.  Every such
port is one of the three or four `c`-oriented ports, and its two fixed
deficient-edge rows both lie on the target `c`-line.  Exact orientation and
triple-product arguments exclude both four and three generic rank-two
ports.  Hence every hypothetical witness in this residual has the single
local rank profile

```text
2,2,3,3,                                                (2)
```

with both rank-two ports contained in `E_c` and silent in their two fixed
rows.

This is a strict source-integrability localization, not an exclusion of
the `eta=0` divisor.  The two-rank-two/two-rank-three residual, the nonzero
raw matching deck `H`, all three-or-more-deficient profiles, attachment,
synchronization, and the global conjecture remain open.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## Parent-theorem checkpoint

The proposition attacked here is the complete `GLS64` eta-zero parent:

> No four-port separated permanent source with the exact `GLS63` orientation
> and injectivity data can produce its nonzero pure `c` target.

The argument below uses the entire same-source four-row permanent rather
than another sibling fibre calculation.  It tests the known pure-`P_4`
rank-drop theorem against every local rank profile, all sixteen orientation
words on the all-rank-two boundary, the mixed and homogeneous three-plane
boundaries, and a sharp exact mixed-orientation family.  The attempt does not
close the parent: it identifies the exact load-bearing successor as the
`2+2` local-rank profile in Section 9.

## Dependencies and notation

- [`GLS63`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_MIXED_KERNEL_PARTIAL_UNCONTRACTION_AND_TWO_DEFICIENT_BINARY_LOCALIZATION_THEOREM.md)
  owns the exactly-two-deficient family, the common kernel `K e_c`, the
  injective nonaxis port set `U`, and `|E_c| in {3,4}`.
- [`GLS64`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TWO_DEFICIENT_MATCHING_INTEGRABILITY_AND_KERNEL_EDGE_ZERO_LOCALIZATION_THEOREM.md)
  proves `W_(nm)(e_c,e_c)=0` and supplies the factorized effective port
  blocks used below.
- [The decomposable `P_4` rank-drop theorem](../p4/classifications/pair-geometry/decomposable-restriction-rank-drop/P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md)
  says that a nonzero pure restriction by four maps of rank at least two has
  at least two maps of rank exactly two.

Put `U={0,1,2,3}`.  For each port write

```text
p_i=X_i(z_0,-),              q_i=Y_i(z_1,-),
a_i=W_(ni)(e_c,-),           b_i=W_(mi)(e_c,-).       (3)
```

The harmless nonzero scalars used to choose the two generic kernel vectors
are absorbed into `a_i,b_i` and `kappa`.  The vectors `a_i,b_i` are fixed;
only `p_i` depends on `z_0` and only `q_i` depends on `z_1`.  Define

```text
L_i(P)=p_i,       L_i(Q)=q_i,
L_i(A)=a_i,       L_i(B)=b_i.                         (4)
```

Here `P,Q,A,B` are the four source-row labels of `P_4`.  All ranks below are
generic ranks over the common fraction field in the two probe variables.

## 1. Exact permanent extraction

### Lemma 1 (the eta-zero source is `P_4`)

Equation (1) holds with the local maps (4).

### Proof

On `eta=W_(nm)(e_c,e_c)=0`, the `GLS64` effective block on a port pair is

```text
D_(ij)=a_i tensor b_j+b_i tensor a_j.                 (5)
```

The two-kernel member of the complete same-source hierarchy is

```text
sum_({i,j} subset U) g_(ij) tensor D_(U-{i,j}),       (6)
```

in labelled-factor order, where

```text
g_(ij)=p_i tensor q_j+q_i tensor p_j.                 (7)
```

Choose the two slots receiving `P,Q` and their order in (7), then order
`A,B` on the complementary slots in (5).  The six choices of the pair and
the two choices in each block give `6*2*2=24` terms, once each.  They are
exactly the twenty-four permutations defining
`(tensor_i L_i)P_4`.

The deficient kernel contractions kill target colours other than `c`.
The surviving target coefficient is the nonzero `GLS63` target weight,
the two nonzero kernel coordinates, and `z_(0,c)z_(1,c)`.  Absorbing the
fixed factors into `kappa!=0` gives (1). `square`

This count is the same-source bridge.  Treating the six blocks (5) as
unrelated tensors discards it.

## 2. A fixed generic rank-two pair

Each port in `U` is injective and nonaxis.  Hence its polynomial cross
product `p_i cross q_i` is nonzero, so `p_i,q_i` are independent over the
fraction field and

```text
rank L_i>=2.                                           (8)
```

Every local physical space is the three-dimensional qutrit space, so also
`rank L_i<=3`.

The actual hypothetical graph has complex coefficients, so all local minors
are polynomials over `C`.  The cited decomposable `P_4` rank-drop theorem is
also stated over `C`; apply it by specialization rather than silently
changing its base field.  If at least three of the generic ranks were three,
choose one nonzero rank-three minor at each of those ports and one nonzero
rank-two minor at every remaining port.  Their common nonvanishing locus,
together with
`z_(0,c)z_(1,c)!=0`, is a nonempty Zariski open in the complex probe space.
At any point of that open, (1) is a nonzero pure complex restriction of
`P_4` with at least three rank-three maps and every map of rank at least
two, contradicting the complex theorem.  Hence at least two generic ranks
are exactly two.  The generic ranks are intrinsic ranks of the four fixed
polynomial maps, so this supplies one fixed generic pair; no fibrewise
choice of a different pair is made.

### Lemma 2 (rank-two ports are oriented and fixed-row silent)

If `rank L_i=2`, then

```text
i in E_c,              a_i,b_i in K e_(i,c)^*.        (9)
```

### Proof

The nonzero pure factor `e_(i,c)^*` in (1) belongs to `im L_i`.  Thus
`p_i,q_i,e_(i,c)^*` lie in the same two-plane, so

```text
(p_i cross q_i)_c=0.                                  (10)
```

By the exact injective nonaxis orientation theorem in `GLS61`, (10) is
precisely membership in `E_c`.  Suppose, after exchanging the probes if
needed, that this is the `X` orientation:

```text
row X_i subseteq K e_(i,c)^*,
pi_c(row Y_i)=K^2.                                    (11)
```

Modulo the `c`-line, rank two says that each fixed vector `a_i,b_i` is
proportional over the fraction field to the generic vector
`pi_c(q_i(z_1))`.  A fixed nonzero vector cannot be proportional to a
generic vector whose coefficient span is two-dimensional: wedging with the
two independent coefficient vectors of `pi_c(q_i)` forces it to vanish.
Hence `pi_c(a_i)=pi_c(b_i)=0`.  The `Y` orientation is symmetric. `square`

Call a port satisfying (9) **silent**.  At a silent `X`-oriented port the
three source rows `P,A,B` lie on `c` and only the `Q` row has an off-`c`
component.  At a silent `Y`-oriented port the roles of `P,Q` are exchanged.

## 3. Source-row form at a silent port

Work in the squarefree Frobenius algebra

```text
R=K[P,Q,A,B]/(P^2,Q^2,A^2,B^2).                      (12)
```

At a silent port choose output rows `(c,o)`.  Its two-dimensional dual
source plane has the form

```text
U_i=span{u_i,e_(rho_i)},
rho_i=Q for the X orientation,
rho_i=P for the Y orientation.                        (13)
```

The nonzero active opposite-shore coefficient has been absorbed into `o`.
The row `u_i` records the four `c`-coordinates of `p_i,q_i,a_i,b_i`.
Purity of (1) says that the coefficient using all four `u_i` is nonzero and
every coefficient in which at least one `u_i` is replaced by its off row
vanishes.

For later use put

```text
N_(ij)=u_i[A]u_j[B]+u_i[B]u_j[A].                    (14)
```

## 4. Four rank-two ports are impossible

### Lemma 3 (complete binary orientation no-go)

The local rank profile cannot be `2,2,2,2`.

### Proof

There are three orientation types up to exchanging `P,Q` and permuting
ports.

**All equal.**  If all off rows are `e_Q`, the coefficient with only port
`i` off is the permanent of the other three `u` rows on columns `P,A,B`.
All four such cofactors vanish.  Expanding the all-`c` permanent along its
`Q` column therefore makes it zero.  The all-`e_P` case is symmetric.

**One plus three.**  Normalize

```text
rho_0=P,              rho_1=rho_2=rho_3=Q.            (15)
```

The three opposite-orientation two-off equations give

```text
N_12=N_13=N_23=0.                                    (16)
```

Write `x_i=u_i[P]` for `i=1,2,3`.  These are nonzero because they are the
active pure-`P` shore coefficients at the three `X`-oriented ports.  The
one-off equations at ports `1,2,3`, after (16), have coefficient matrix

```text
[0   x_3 x_2]
[x_3 0   x_1]       on (N_01,N_02,N_03),             (17)
[x_2 x_1 0  ]
```

whose determinant is `2x_1x_2x_3!=0`.  Hence the remaining three `N` values
also vanish.

**Two plus two.**  Normalize

```text
rho_0=rho_1=P,       rho_2=rho_3=Q.                   (18)
```

The four opposite two-off equations kill
`N_02,N_03,N_12,N_13`.  The one-off equation at port `0` reduces to
`u_1[Q]N_23=0`, while the one at port `2` reduces to
`u_3[P]N_01=0`.  Both displayed active coefficients are nonzero, so all six
`N` values vanish.

In the last two cases, expand the all-`c` permanent by the ordered slots
receiving `P,Q`.  Every summand has the complementary factor `N_ij`, hence
the permanent is zero.  All orientation words are covered, including zero
entries in the `u_i`; only the required active pure-shore coefficients were
divided out.  This contradicts (1). `square`

## 5. Mixed triples of silent ports

Suppose exactly three ports are silent and call the remaining rank-three
port `0`.  Put

```text
C=U_1 U_2 U_3 subseteq R_3.                           (19)
```

The `0|123` flattening is the perfect multiplication pairing between the
three-dimensional source rowspace at port `0` and `C`.  Its restricted rank
is one, so

```text
1>=3+dim C-4,             hence dim C<=2.             (20)
```

Let `C_off` be spanned by products in which at least one of
`u_1,u_2,u_3` is replaced by its off row.  If
`g=u_1u_2u_3`, purity gives

```text
g notin C_off                                            (21)
```

because the `c`-row at port `0` kills `C_off` but pairs nontrivially with
`g`.

### Lemma 4 (mixed silent triples have too large a product)

If `rho_1,rho_2,rho_3` are not all equal, (20)--(21) are impossible.

### Proof

Normalize the word to `(P,P,Q)`.  Replacing
`u_i` by `u_i+lambda_i e_(rho_i)` does not change its plane, and changes
`g=u_1u_2u_3` only by an element of `C_off`.  Thus both (21) and the class
of `g` modulo `C_off` are unchanged.  Use this freedom to write

```text
u_i=a_i Q+b_i A+c_i B,              i=1,2,
u_3=dP+b_3A+c_3B.                                    (22)
```

Let `v_i=(b_i,c_i)`.  In the basis of `R_3`, `C_off` contains

```text
PQ v_1,     PQ v_2,
(b_1c_2+c_1b_2)QAB,
a_2PQv_3+(b_2c_3+c_2b_3)PAB,
a_1PQv_3+(b_1c_3+c_1b_3)PAB.                         (23)
```

Equivalently, identify a three-row product with its four complementary
cofactor coordinates `(P,Q,A,B)`.  The five mixed rows in (23) and the
all-`c` row are

```text
m_1=(0,b_2c_3+c_2b_3,a_2c_3,a_2b_3),
m_2=(0,b_1c_3+c_1b_3,a_1c_3,a_1b_3),
m_3=(b_1c_2+c_1b_2,0,0,0),
m_4=(0,0,c_2,b_2),
m_5=(0,0,c_1,b_1),

m_0=(a_1(b_2c_3+c_2b_3)+b_1a_2c_3+c_1a_2b_3,
     d(b_1c_2+c_1b_2),
     d(a_1c_2+c_1a_2),
     d(a_1b_2+b_1a_2)).                              (23a)
```

Thus `C_off=span{m_1,...,m_5}`, while `g` is represented by `m_0`.

If `g` is independent of `C_off` and `dim C<=2`, then
`dim C_off<=1`.  The first two vectors in (23) show that every nonzero
`v_1,v_2` lies on one common line in the `(A,B)` plane.  They cannot both
vanish, since then `u_1u_2=0` and `g=0`.

First dispose of `v_3=0`.  The `QAB` vector in (23), together with
`dim C_off<=1`, forces
`b_1c_2+c_1b_2=0`; otherwise it is independent of the nonzero
`PQv_1,PQv_2` line.  Direct expansion then gives

```text
g=d PQ(a_1v_2+a_2v_1),                               (23b)
```

which is zero or already belongs to `span{PQv_1,PQv_2} subseteq C_off`.
This includes the edge cases `v_1=0,v_2!=0` and its transpose.

Now take `v_3!=0`.  The `PAB` coordinates in `m_1,m_2` force its symmetric
products with every nonzero `v_1,v_2` to vanish.  Their `PQ` coordinates
also put `v_3` on the same common line whenever the corresponding `a_i` is
nonzero.  If both `a_1,a_2` vanish, the already-forced symmetric product of
`v_1,v_2` makes `u_1u_2=0` and hence `g=0`.  Thus every remaining nonzero
case puts all three relevant `v_i` on one common line and makes all their
pairwise symmetric products zero.

Thus, in every nonzero case, the common line is isotropic for
`(b,c),(b',c') mapsto bc'+cb'`.  In characteristic zero it is one of the
coordinate lines `K A` or `K B`.  All three `u_i` then use only `P,Q` and
that one coordinate.  Their product `g` is zero or a multiple of the
corresponding vector `PQA` or `PQB`, already present in `C_off` by (23).
Equivalently `m_0` lies in `span{m_1,...,m_5}`, contradicting (21).
`square`

## 6. Homogeneous triples and anchor rigidity

It remains to consider three silent ports with the same orientation.
Exchange the probes if necessary and take ports `1,2,3` to be silent
`X`-oriented ports.  Write

```text
p_i=x_i c_i,       a_i=alpha_i c_i,
b_i=beta_i c_i,                                      (24)
```

where `alpha_i,beta_i` are fixed and `x_i=x_i(z_0)`.  Their `q_i` have
nonzero images modulo `c_i`.  For `{i,j,k}={1,2,3}` define

```text
h_i^P=alpha_j beta_k+beta_j alpha_k,
h_i^A=x_j beta_k+beta_j x_k,
h_i^B=x_j alpha_k+alpha_j x_k,                        (25)
```

and

```text
K_P4=sum_i x_i h_i^P
    =per([x_i,alpha_i,beta_i]_(i=1)^3).               (26)
```

Direct permanent expansion gives

```text
P_4=q_0 K_P4 tensor c_1 tensor c_2 tensor c_3
 +sum_i (h_i^P p_0+h_i^A a_0+h_i^B b_0)
          tensor q_i tensor c_j tensor c_k.           (27)
```

Projecting slot `i` modulo `c_i` isolates its summand, so purity forces

```text
h_i^P p_0+h_i^A a_0+h_i^B b_0=0,       i=1,2,3.      (28)
```

Equation (27) then reduces to its first term.  The target is nonzero, so

```text
K_P4!=0,              q_0 in K c_0.                  (29)
```

Because `q_0` depends only on `z_1`, the fraction-field identity (29) makes
each of its two off-`c_0` coefficient polynomials identically zero.  Thus
the entire rowspace of `Y_0` lies on `Kc_0`, and the fourth port is forced
into the opposite `Y` orientation if its joint map is injective.

### Lemma 5 (separated anchor rigidity)

Equations (25)--(29) force

```text
dim_K pi_c(row X_0)<=1.                               (30)
```

### Proof

Let `H` be the `3 x 3` matrix whose row `i` is
`(h_i^P,h_i^A,h_i^B)`, and put `M=[p_0\ a_0\ b_0]`.  Equation (28) is
exactly `M H^T=0`.  If `rank H>=2`, its kernel has dimension at most one.
After applying any quotient functional modulo `Kc_0`, the corresponding
coefficient row of `[pi_c(p_0)\ pi_c(a_0)\ pi_c(b_0)]` belongs to this same
kernel.  Hence that quotient matrix has rank at most one.  If either fixed
vector `pi_c(a_0),pi_c(b_0)` is nonzero, its span is one fixed physical
line and `pi_c(p_0)` lies on it.  If both are zero, the nonzero `h^P`
column (forced by `K_P4!=0`) makes (28) give `pi_c(p_0)=0`.  Thus in all
cases `p_0` modulo `c_0` is zero or lies on one fixed physical line; in
particular two independent fixed quotient rows cannot be hidden in the
one-dimensional kernel.

If `rank H=1`, (26) makes the `h^P` column nonzero.  There are fraction-field
scalars `rho,sigma` with

```text
h_i^A=rho h_i^P,          h_i^B=sigma h_i^P.          (31)
```

The two row-symmetry identities

```text
K_P4=sum_i alpha_i h_i^A=sum_i beta_i h_i^B          (32)
```

show that

```text
K_P4=rho R_A=sigma R_B,
R_A=sum_i alpha_i h_i^P,       R_B=sum_i beta_i h_i^P. (33)
```

All three displayed quantities are nonzero.  Equations (28) become

```text
p_0=-rho(a_0+(R_A/R_B)b_0),                           (34)
```

again one fixed physical line.  Rank zero would make `h^P=0` and then
`K_P4=0`, contrary to (29).  This proves (30) without dividing by any
individual entry of `H`. `square`

Injective `Y` orientation at port `0` requires
`pi_c(row X_0)=K^2`, contradicting (30).  Lemma 4 handles mixed silent
triples, and Lemma 5 handles homogeneous ones.  Therefore the local rank
profile cannot contain exactly three rank-two maps.

## 7. Exact local-rank localization

### Theorem 6 (`GLS65`)

Every hypothetical witness in the `GLS64` eta-zero residual has exactly two
generic rank-two and two generic rank-three local permanent maps:

```text
#{i:rank L_i=2}=2,          #{i:rank L_i=3}=2.        (35)
```

Both rank-two ports belong to `E_c` and satisfy

```text
a_i,b_i in K e_(i,c)^*.                               (36)
```

### Proof

The rank-drop theorem and (8) give at least two rank-two maps.  Lemma 3
excludes four, while Lemmas 4--5 exclude three.  Hence exactly two remain.
Lemma 2 gives (36). `square`

This covers both `|E_c|=3` and `|E_c|=4`.  In the three-zero case the
nonoriented fourth port cannot be rank two by Lemma 2.

## 8. Sharp fixed-fibre and separated controls

Fibrewise `P_4` purity is not enough.  In source coordinates `(P,Q,A,B)`
take the two row covectors

```text
s_0=(1,0,-2,1),        t_0=(0,1,0,0),
s_i=(1,0, 1,1),        t_i=(0,1,0,0),   i=1,2,3.     (37)
```

Exact expansion gives

```text
P_4 restricted to (span{s_i,t_i})
 =6 t_0 tensor s_1 tensor s_2 tensor s_3.             (38)
```

All other fifteen binary coefficients vanish.  Every displayed `P` and
`Q` shore is nonzero, with the mixed orientation `YXXX`.  This is not a
full-injective separated family: each joint shore span is only two-
dimensional.

The control has a large exact flat.  Keep all `P,A,B` columns in (37), keep
`q_0=t_0`, and replace each of `q_1,q_2,q_3` arbitrarily.  Whenever `Q` is
assigned to one of these three modes, the complementary `P,A,B` permanent
vanishes because the mode-zero coefficients sum as

```text
1-2+1=0.                                               (39)
```

Thus (38) is unchanged.  The three majority `Q` rows can point in arbitrary
output directions, although each majority local source span remains at
most two-dimensional because its fixed `P,A,B` rows are collinear.  Lemma 5
says the port-zero `P` shore cannot acquire a two-dimensional transverse
image while purity is retained.  The control is therefore sharp for the
three-port flat and for the anchor obstruction, but it is not a GHZ
witness.

## 9. Exact remaining obligation

The eta-zero branch is now confined to the following `2+2` local-rank
problem:

> Two ports are silent rank-two `c`-oriented maps of the form (13), two
> ports are rank-three maps, all four arise from the same separated
> `p_i(z_0),q_i(z_1),a_i,b_i` source, equation (1) holds with nonzero target,
> and the same physical graph also satisfies the `GLS64` scalar hierarchy
> with `H!=0`.

The next proof must exhaust the same- and opposite-orientation choices of
the two silent ports and the rank-three hyperplane/pair-image boundary.  A
generic chart rank or a fibre-dependent basis change is insufficient.

## 10. Exact frontier

```text
eta-zero same-source tensor = separated P_4:           PROVED;
fixed generic rank-two pair:                            PROVED;
rank-two port c-orientation and fixed-row silence:      PROVED;
local rank profiles 2222 and 2223:                      EXCLUDED;
local rank profile 2233:                                OPEN / LOCALIZED;
GLS63 eta-zero residual, |E_c|=3 or 4:                 OPEN;
three-or-more-deficient profiles:                       OPEN;
response/selector/synchronization/activity package:    OPEN;
nonzero-anchor and arbitrary-root strategic node:      OPEN;
global Krenn-Gu conjecture:                            UNRESOLVED. (40)
```

## 11. Verification boundary

The primary verifier expands the twenty-four-term source, checks the
sixteen-word all-rank-two orientation census identities, reconstructs the
mixed-triple product formulas and anchor matrix identities, and verifies
the fixed-fibre and exact-flat controls.  The independent standard-library
audit uses a separate permanent implementation and a finite-field census of
the mixed triple-product boundary.  These programs audit finite and
displayed algebraic leaves; the fraction-field rank, perfect-pairing, and
same-source arguments above remain the written proof.

From repository root run:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py
```
