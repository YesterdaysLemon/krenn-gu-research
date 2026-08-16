# Arbitrary permanent star-pair full-extension exclusion theorem

## Status

This note proves an exact characteristic-zero endpoint for the **displayed
based** Delta-admissible equality-five `(4,1)` star frame.  That displayed
frame has no exact extension from `P_6` to the three-colour diagonal tensor
`Delta_3`.

The reviewed predecessors force a rank-two mode in each mixed-factor
projection family, classify every possible kernel line and its local support,
exclude a mode that is low for both families, and propagate every remaining
exceptional line to a singleton companion in a distinct mode.  The new step
here excludes each of the four noncommon low/companion cycles individually.

For every cycle, exact channel combinations give the same nonzero residual
covector `ell` from the low and companion shores.  If the low has support two,
three diagonal slices would make `pol(ell*x_4*x_5)` equivalent to a weighted
`Delta_3`, although `pol(XUV)` has tensor rank greater than three.  If the low
has singleton support, a rank-two/rank-three slice dichotomy pushes the unused
colour onto `ker(ell)` on one pair of shores.  An exact star-core relation on
that hyperplane then equates its live diagonal target to zero targets.

No second contraction is replaced by a scalar complementary pairing, and no
two vectors from one local plane are inserted into distinct tensor slots.
This endpoint is **not** transported to every based-frame stabilizer orbit in
the unbased `(4,1)` orbit.  That classification remains missing.  The
unrestricted `P_6 -> Delta_3` problem and the global Krenn--Gu conjecture
therefore remain **UNRESOLVED**.

## 1. Displayed frame and exact endpoint

Let `K` be a field of characteristic zero and work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

At the first two modes fix

```text
u_0=-x_0+x_2,      u_1=x_0-x_3,       u_2=x_1-x_2,
v_0=x_0+x_1-x_2+x_3,
v_1=x_0+x_1,       v_2=-x_1+x_2.                         (1)
```

The five complementary quartics are `x_4x_5g_z`, where

```text
g_(m_1)=x_3(x_0+x_1-x_2),
g_(m_2)=(x_0-x_3)(x_1-x_2),

g_(d_0)=x_0x_1+x_0x_3-x_1x_2+2x_1x_3-x_2x_3,
g_(d_1)=-x_2(x_0+x_1-x_3),
g_(d_2)=2x_0x_3.                                        (2)
```

Put

```text
Phi_1=(x_3,x_4,x_5,x_0+x_1-x_2),
Phi_2=(x_0-x_3,x_4,x_5,x_1-x_2).                        (3)
```

Let four ordered independent local triples span `L_a,L_b,L_c,L_d`.
An exact extension would satisfy the complete polarized targets

```text
T_(m_1)=T_(m_2)=0,
T_(d_i)=lambda_i e_i^* tensor e_i^* tensor e_i^*
                         tensor e_i^*,
lambda_i!=0,                                      i=0,1,2. (4)
```

### Theorem 1 (displayed based star full-extension exclusion)

There are no four ordered independent local triples satisfying (4) over a
field of characteristic zero.  Equivalently, the displayed based frame (1)
has no exact `P_6 -> Delta_3` extension.

## 2. Frozen reviewed interfaces

The proof composes the following reviewed commits.  SHA-256 digests are
uppercase; the independent audit also checks the corresponding Git blobs.

### 2.1 Two-sided projection drop

```text
commit: ca21e1d32c2e00a228d5be8050e57badd95f73d4

theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md
76AEBB661CA3E89DF3E4228954B0D7CB3D736414A4AB22C2EBC9A2C84A774D62

primary:
claims/arbitrary-order/verify_arbitrary_permanent_star_pair_two_sided_projection_drop.py
223B61126635FE59987B75684CFA6FCA1173737913CEAD0F46D98AA3A8C3DF1B

audit:
claims/arbitrary-order/audit_arbitrary_permanent_star_pair_two_sided_projection_drop.py
CD4D833DB7CB132FCFED02A0BD2353799E184DAC3DFAC9EC5F714F998F614311

review:
docs/audits/ARBITRARY_PERMANENT_STAR_PAIR_TWO_SIDED_PROJECTION_DROP_REVIEW_2026-08-15.md
F0C61339191FDD02C6F72F721C175636DC4A302554C71FF51C8809747D30203F
verdict: PASS.                                             (5)
```

Accepted interface:

```text
min_t rank(Phi_1|L_t)<=2,             min_t rank(Phi_2|L_t)<=2. (6)
```

### 2.2 Kernel-support boundary

```text
commit: 985f1a4cd49508da067ba1b4d788b2e576368448

theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
2B44641806EEE9B14D2F9DCC692C2E8E1CB9917832A9C2FD9E658243ACFE51F5

primary:
claims/arbitrary-order/verify_arbitrary_permanent_star_pair_kernel_support_boundary.py
73406FF9C62A2113341BBC97E36E2E4F4151CF399E72EEBFD831A05944744124

audit:
claims/arbitrary-order/audit_arbitrary_permanent_star_pair_kernel_support_boundary.py
0D4F649C78577158E39577FB5CBDDA1A0057534E75A803F1EB73F25726DA5721

review:
docs/audits/ARBITRARY_PERMANENT_STAR_PAIR_KERNEL_SUPPORT_BOUNDARY_REVIEW_2026-08-15.md
EC573CB950EFBCB9DFE300DBCEBDCE9992E6DF839EF77A45C038E605EA925A45
verdict: PASS.                                             (7)
```

Accepted interface: every restricted projection rank is at least two.  A
rank-two kernel line and its nonempty local support are among

```text
Phi_1: N=x_1+x_2 in {0,1},
       B_0=x_0+x_2 in {1,2},
       C_0=x_0-x_1 in {0,2};

Phi_2: N=x_1+x_2 in {0,1},
       B_1=x_0+x_3 in {0,2},
       C_1=x_0+x_1+x_2+x_3 in {1,2}.                    (8)
```

### 2.3 Noncommon and support-two same-mode boundary

```text
commit: 85e49d1100b6b77b610b07744ac377eb291691e7

theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_PAIR_SAME_MODE_NONCOMMON_AND_SUPPORT_TWO_BOUNDARY_THEOREM.md
27AA460A9846A3568F3160DF3F6A03C798E87696D1A6E22900F13F8A76EF5AD9

primary:
claims/arbitrary-order/verify_arbitrary_permanent_star_pair_same_mode_noncommon_and_support_two_boundary.py
0D24DC727902A18824B5D5470542F5BDF7E87FDAB4C5D5FEBE5C439CCE4FFAEA

audit:
claims/arbitrary-order/audit_arbitrary_permanent_star_pair_same_mode_noncommon_and_support_two_boundary.py
E849C2F5A3D0A14414156F70DC7A58CF62B332585A4271268EB54B705719F543

review:
docs/audits/ARBITRARY_PERMANENT_STAR_PAIR_SAME_MODE_NONCOMMON_AND_SUPPORT_TWO_BOUNDARY_REVIEW_2026-08-15.md
FB85A20E79B35020FECD790A6A9B5B2922F12B2D699C50052967AF434C164E82
verdict: PASS.                                            (9a)
```

Accepted interface: all common/noncommon and noncommon/noncommon same-mode
pairs are excluded, as is support-two `N/N`; only singleton `N/N` remained.

### 2.4 Singleton completion of same-mode exclusion

```text
commit: 4541cce432f621b9954251a0454f820cef500aac

theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_PAIR_SINGLETON_NN_EXCLUSION_THEOREM.md
EA29D52F17100A7D99F5A56254309B69BC21744E5C2BAFE78A981F19097B4693

primary:
claims/arbitrary-order/verify_arbitrary_permanent_star_pair_singleton_nn_exclusion.py
CED670F3D48B567CBC62B4759718E056E21A5E21CB1F42DDA85426F502A4B0FE

audit:
claims/arbitrary-order/audit_arbitrary_permanent_star_pair_singleton_nn_exclusion.py
8ADCB1EAF9B4E3C5B140463AEC89615DBE323A385DC3893030F57C10ECAFA031

review:
docs/audits/ARBITRARY_PERMANENT_STAR_PAIR_SINGLETON_NN_EXCLUSION_REVIEW_2026-08-15.md
271D2C87D4F76FDF3541816183A40E83A3E7B5B8F9379FDEB6FC584188122535
verdict: PASS.                                            (9b)
```

Accepted interface, including its reviewed predecessors:

```text
There is no t with
rank(Phi_1|L_t)=rank(Phi_2|L_t)=2.                       (10)
```

### 2.5 Exceptional companion propagation

```text
commit: 76240ca4becc1b58b9803ac1ec6a4db159c07d3c

theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_STAR_TRIANGLE_EXCEPTIONAL_COMPANION_PROPAGATION_THEOREM.md
9C70842573B3DD02BE5AC9CC65B08047AF0C6877892EA816A5D89B2024ED36A3

primary:
claims/arbitrary-order/verify_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py
97177FE5D7A44821428AAED34707FAD30490D50D80163609A28FB3AE7BE663F0

audit:
claims/arbitrary-order/audit_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py
9DB62582D752C85F2E7AE8343EC806B95786C5693466ECFB3666C5F838A35289

review:
docs/audits/ARBITRARY_PERMANENT_STAR_TRIANGLE_EXCEPTIONAL_COMPANION_PROPAGATION_REVIEW_2026-08-15.md
7BDFE90C91664B8A8AF5C3B6BFC8997F274D8EB4BCBF863757CD63E81DC30300
verdict: PASS.                                            (11)
```

The accepted noncommon star rows are

```text
B_0 -> q=x_2-x_0 singleton colour 0;
C_0 -> q=x_0+x_1 singleton colour 1;
B_1 -> q=x_3-x_0 singleton colour 1;
C_1 -> q=-x_0+x_1+x_2+x_3 singleton colour 0,          (12)
```

where the companion occurs in a distinct local mode.

## 3. Reduction to four individual cycles

Assume (4).  By (6), some mode is low for `Phi_1` and some mode is low for
`Phi_2`; the floor in Section 2.2 makes every such rank exactly two.

The common line `N` lies in both ambient projection kernels.  If any local
plane contained it, both restricted ranks would be at most two and hence
exactly two, contradicting (10).  Thus no `N` occurrence is possible.
Every low line is therefore one of

```text
B_0,C_0,B_1,C_1.                                      (13)
```

It suffices to exclude a single occurrence of each line in (13), regardless
of all other low modes.  Choose such a low generator `p in L_a`.  Its
companion theorem supplies the displayed `q in L_b`, `b!=a`.  Name the other
two modes `c,d`.

## 4. Exact common-cubic table

Use channel order

```text
(m_1,m_2,d_0,d_1,d_2).                                (14)
```

For a coefficient vector `r`, write

```text
B_r p=sum_z r_z B_zp.
```

Direct contraction of (2) gives the complete table

```text
low p    allowed support   companion q / colour e
          r_p                 r_q                 common ell

B_0      {1,2}             x_2-x_0 / 0
          (0,-1,0,1,-1)      (0,0,1,0,0)         -2(x_1+x_3)

C_0      {0,2}             x_0+x_1 / 1
          (0,1,-1,0,-1)      (0,0,0,1,0)         -2x_2

B_1      {0,2}             x_3-x_0 / 1
          (-3,0,1,0,1)       (0,0,0,1,0)          2x_2

C_1      {1,2}             -x_0+x_1+x_2+x_3 / 0
          (-1,0,0,1,1)       (-2,0,1,0,0)          2(x_3-x_1). (15)
```

In every row,

```text
B_(r_p)p=B_(r_q)q=ell.                                (16)
```

The `r_q` coefficient of `d_e` is one, and its other nonzero coordinates
are mixed channels.  The two `r_p` diagonal coefficients on the allowed
support are both nonzero.  If

```text
p=sum_i alpha_i y_(a,i),          q=beta_e y_(b,e),    beta_e!=0, (17)
```

then the exact single contractions of (4) and (16) give

```text
pol(ell*x_4*x_5)|_(L_a,L_c,L_d)
 =nu_e e_e^* tensor e_e^* tensor e_e^*,              nu_e!=0,

pol(ell*x_4*x_5)|_(L_b,L_c,L_d)
 =sum_(i in supp(alpha)) nu_i e_i^* tensor e_i^*
                                      tensor e_i^*,    nu_i!=0. (18)
```

These are full three-slot tensors, not scalarized second contractions.

## 5. Support-two lows are impossible

Suppose `p` uses both allowed colours.  Let `E` be the three-space with
coordinates

```text
(X,U,V)=(ell,x_4,x_5),                 P=pol(XUV).      (19)
```

Fixing `L_c,L_d`, the first-mode slice map of `P` sends the three ambient
vectors

```text
y_(a,e),       y_(b,i_1),       y_(b,i_2)              (20)
```

to nonzero multiples of the independent matrices

```text
E_ee,          E_(i_1i_1),      E_(i_2i_2),            (21)
```

where `{e,i_1,i_2}={0,1,2}`.  Hence the vectors in (20) are independent.
On their span `Y`, equation (18) makes

```text
P|_(Y,L_c,L_d)
```

a concise weighted `Delta_3`.  Since `P` factors through the three
evaluation maps to `E`, conciseness makes all three maps from `Y,L_c,L_d`
to `E` isomorphisms.  Thus `P=pol(XUV)` would be `GL_3^3`-equivalent to a
rank-three weighted `Delta_3` tensor.

This is impossible.  The first-mode slice space of `P` is

```text
span{sym(UV),sym(XV),sym(XU)}.                         (22)
```

It contains no nonzero rank-one matrix: a rank-one symmetric matrix is a
nonzero scalar multiple of `(aX+bU+cV)^2`, while membership in (22) kills
the three square coefficients and forces `a=b=c=0`.  If the concise tensor
`P` had rank at most three, isolating three independent first-mode factors
would put three nonzero rank-one matrices in (22).  Therefore

```text
rank(P)>3,                                             (23)
```

contradicting (21).  Every low in (13) is consequently singleton-supported.

## 6. The singleton slice dichotomy

Let the singleton low colour be `i`, let `e` be the companion colour in
(15), and let

```text
t={0,1,2}\{e,i}.                                      (24)
```

For `v in K^6`, write

```text
bar(v)=(ell(v),x_4(v),x_5(v)) in E.
```

Define the `c,d` slice map

```text
S:E -> Mat_(3x3)(K),
S(w)_(kl)=P(w,bar(y_(c,k)),bar(y_(d,l))).              (25)
```

Equation (18) gives nonzero multiples of `E_ee,E_ii` in `im S` and gives

```text
S(bar(y_(a,t)))=S(bar(y_(b,t)))=0.                    (26)
```

Thus

```text
rank S in {2,3}.                                      (27)
```

For later use, put

```text
kappa(c,d)=P(-,c,d).
```

If `d=(X,U,V)`, the matrix of `c -> kappa(c,d)` is

```text
[ 0  V  U ]
[ V  0  X ]
[ U  X  0 ],                                          (28)
```

whose principal two-minors are `-V^2,-U^2,-X^2`.  Every nonzero `d`,
including a vector with zero coordinates or an isotropic `A`-part, therefore
has an annihilator of dimension at most one.

If `rank S=3`, equation (26) and injectivity give

```text
bar(y_(a,t))=bar(y_(b,t))=0.                           (29)
```

If `rank S=2`, its image is exactly `span{E_ee,E_ii}`.  All other cell
functionals `kappa(C_k,D_l)` vanish, where

```text
C_k=bar(y_(c,k)),                 D_l=bar(y_(d,l)).
```

The live cells make `D_e,D_i` independent: proportionality would turn the
cross zero `kappa(C_e,D_i)=0` into the live diagonal
`kappa(C_e,D_e)!=0`.  Similarly `C_e,C_i` are independent.  Since `C_t`
annihilates both `D_e,D_i`, and `D_t` annihilates both `C_e,C_i`, equation
(28) forces

```text
C_t=D_t=0.                                             (30)
```

Here (29)--(30) mean zero only after projection to
`(ell,x_4,x_5)`; none of the ambient local vectors is asserted to be zero.

## 7. The unused-colour core gate

For the four rows of (15), the following exact quadratic identities hold:

```text
low       channel relation                         exact factor

B_0   -g_(m_1)+g_(m_2)+g_(d_0)-g_(d_1)+g_(d_2)
                                                    =2x_0(x_1+x_3)

C_0,
B_1   -3g_(m_1)-g_(m_2)+g_(d_0)+g_(d_2)
                                                    =x_2(x_0-x_1+x_3)

C_1   -g_(m_1)-g_(m_2)+g_(d_1)+g_(d_2)
                                                    =-(x_0+x_2)(x_1-x_3). (31)
```

Each right side is divisible by the corresponding `ell` in (15), up to a
nonzero scalar.  Hence its bilinear polarization vanishes on
`ker(ell) x ker(ell)`.  The coefficients of the two possible unused live
diagonals are

```text
B_0:       d_1=-1, d_2= 1;
C_0,B_1:   d_0= 1, d_2= 1;
C_1:       d_1= 1, d_2= 1.                            (32)
```

They are all nonzero in characteristic zero.

In the rank-three case (29), the `a,b` colour-`t` vectors have no `A`-part
and their `R`-parts lie in `ker(ell)`.  Full four-slot polarization factors
at the all-colour-`t` entry as

```text
T_z(t,t,t,t)
 =g_z(y_(a,t)^R,y_(b,t)^R)
  J(y_(c,t)^A,y_(d,t)^A).                              (33)
```

Multiplying (33) by the applicable channel coefficients in (31) gives zero.
But the exact target (4) gives the nonzero scalar in (32) times `lambda_t`.
Contradiction.

In the rank-two case (30), the same argument uses the other shores:

```text
T_z(t,t,t,t)
 =J(y_(a,t)^A,y_(b,t)^A)
  g_z(y_(c,t)^R,y_(d,t)^R).                            (34)
```

Again (31) makes the channel combination zero while (4) makes it a nonzero
multiple of `lambda_t`.  Thus singleton lows are impossible as well.

Sections 5--7 exclude every occurrence in (13), independent of all other
low-count diagrams.

## 8. Proof of Theorem 1 and exact boundary

The two-sided theorem supplies at least one low mode.  Section 3 removes the
common line and leaves (13).  Sections 4--7 exclude every line in (13), a
contradiction.  This proves Theorem 1.

```text
field:                                                   CHARACTERISTIC ZERO;
displayed based Delta-admissible (4,1) frame (1):        ASSUMED;
exact local triples and full targets (4):                ASSUMED;
two-sided rank-drop existence:                           REVIEWED/PINNED;
rank floor and exceptional-kernel classification:        REVIEWED/PINNED;
complete same-mode low exclusion:                        REVIEWED/PINNED;
exceptional companion propagation:                       REVIEWED/PINNED;
four noncommon low/companion cycles:                      EXCLUDED HERE;
exact extension of the displayed based frame (1):        EXCLUDED;

all based-frame stabilizer orbits of unbased (4,1):      NOT CLASSIFIED;
transport from (1) to every based (4,1) frame:           NOT PROVED;
unbased (4,1) orbit universally excluded:                NOT PROVED;
active-support-five/six cases:                            OPEN;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.   (35)
```

Any later PR that promotes this displayed-frame endpoint into the live
frontier must update `docs/current-frontier.md`.  This local package does not
assert the missing based-frame transport.

## 9. Exact replay

Run

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_star_pair_full_extension_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_star_pair_full_extension_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_star_pair_full_extension_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_star_pair_full_extension_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_star_pair_full_extension_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_star_pair_full_extension_exclusion.py
```

The primary verifier pins all reviewed dependencies, reconstructs the four
common-cubic rows and every target coefficient, proves the restricted-core
identities symbolically, checks the `XUV` annihilator and rank obstruction,
and verifies (33)--(34) in the full six-variable square-free algebra.  The
independent audit imports neither the primary verifier nor SymPy.  It checks
the committed Git blobs, rebuilds all tables with integer matrices, exhausts
the full-quartic factorizations on basis vectors, and searches the slice
annihilator incidence over finite fields.  Those finite searches are
corroboration, not the characteristic-zero proof; the exact written argument
and algebraic checks prove the theorem.
