# Jet-orthogonal splicing preserves every mixed lower jet and every fixed-window lower-frame gap

## Status

**Exact rational common-block theorem and formal-cofactor no-go.**  The
fixed-complement theorem forces every graph-side `P_7` window, but its common
rational model has zero marked-shore product at every root pair with
cofactor-image rank `rho>=2`.  This note tests whether the mixed lower-root
tensor equations repair that gap.

They do not, at the formal principal-cofactor level.  The same rational
root--blocker system admits a **jet-orthogonal splice** with the exact common
two-endpoint `2+2+1` tangent model.  In the splice:

1. all three pure `5 x 5` root permanents remain `-1`;
2. every one of the eighteen colour-tagged fixed-complement windows remains
   graph-side clean;
3. every marked-shore product at the two `rho=2` root pairs remains zero;
4. one honest common family of tangent root--root and root--endpoint blocks
   satisfies all 31 nonempty mixed lower-root GHZ equations; and
5. the distinguished empty/residual companion forms are nevertheless
   independent at **every** root pair, including every `rho=1` shore.

Thus neither the mixed lower-root value equations nor common companion blocks
force a fixed retained pair to meet a `rho>=2` shore.  They also show why
such co-occurrence is not necessary for root-side selector independence:
`rho` measures the GHZ/cofactor image, not the span of the distinguished
companion forms.

The complementary tensors in the lower-jet model are one globally
nonconflicting **formal** principal-cofactor ledger.  They are scalar-hafnian
realizable chart by chart and with one common terminal block by existing
theorems, but no tensor-valued common graph is known to realize the ledger
while cancelling all mixed blocker words.  Consequently this result does not
construct a `P_7 -> Delta_3` restriction and does not settle Krenn--Gu.

No support, graph, alignment, matching-family, or colour-word enumeration is
used.

## 1. The jet-orthogonal splice

For each root `i`, let `V_i` be its local three-space.  Fix a covector and a
frozen vector

```text
alpha_i in V_i^*,        v_i in V_i,
alpha_i(v_i)=1,          S_i=ker alpha_i.              (1)
```

The projection onto the tangent plane along the frozen line is

```text
pi_i(x)=x-alpha_i(x)v_i.                               (2)
```

Let `V_b` be a blocker space and let `r_(i,b) in V_b^*` be arbitrary.  Define
the root--blocker block

```text
E_(i,b)(x,y)=alpha_i(x) r_(i,b)(y).                    (3)
```

Independently choose tangent companion data:

```text
L_ij in S_i^* tensor S_j^*,
p_i,q_i in S_i^*.                                     (4)
```

Extend them to the full root spaces by precomposing every root argument with
`pi_i`.  For example,

```text
Ltilde_ij(x,y)=L_ij(pi_i x,pi_j y),
ptilde_i(x)=p_i(pi_i x),
qtilde_i(x)=q_i(pi_i x).                               (5)
```

### Lemma 1 (jet-orthogonal splice lemma)

The blocks (3) and (5) have the exact complementary behaviour

```text
E_(i,b)(v_i,-)=r_(i,b),       E_(i,b)(S_i,-)=0,

Ltilde_ij(v_i,-)=Ltilde_ij(-,v_j)=0,
ptilde_i(v_i)=qtilde_i(v_i)=0,                         (6)
```

while their restrictions to the tangent planes are precisely the data in
(4).  Hence arbitrary frozen pure root--blocker rows can be combined with an
arbitrary tangent-only common companion system without changing either the
pure root--blocker matrices or any lower tangent companion form.

Proof.  Equations (1)--(2) give

```text
pi_i(v_i)=0,        pi_i|_(S_i)=id,        alpha_i|_(S_i)=0. (7)
```

Substitution into (3) and (5) proves (6).  The construction is edgewise, so
all blocks belong to one bilinear graph system.

This is an exact first-jet splitting, not a limiting or generic argument.

## 2. The frozen pure sector

Use the axis pattern

```text
alpha_0=alpha_1=e_0^*,
alpha_2=alpha_3=e_1^*,
alpha_4=e_2^*,                 v_i=(1,1,1).            (8)
```

Take the three pure root--blocker matrices

```text
H_0, columns (t,u_01,v_01,u_02,v_02):
[-1 1 0 0 0]
[ 0 0 1 0 0]
[-1 0 0 1 0]
[ 0 0 0 0 1]
[ 1 1 0 1 0]

H_1, columns (t,u_12,v_12,u_01,v_01):
[ 0 1 0 0 0]
[-1 0 1 0 0]
[ 0 0 0 1 0]
[-1 0 0 0 1]
[ 1 0 1 0 1]

H_2, columns (t,u_02,v_02,u_12,v_12):
[-1 1 0 0 0]
[-1 0 1 0 0]
[-1 0 0 1 0]
[ 1 0 0 0 1]
[ 1 1 0 1 0].                                       (9)
```

Assemble their colour slices into blocker covectors `r_(i,b)` exactly as in
the fixed-complement lower-frame theorem, and use (3).  Since
`alpha_i(v_i)=1`, frozen evaluation gives (9).  Since every tangent vector
lies in `S_i`, differentiated root--blocker edges vanish identically.

For a local unmarked column pair `S` and root pair `I`, write

```text
Lambda_S(I)=per H[I,S]
             per H[R\I,{t} union ({1,2,3,4}\S)].      (10)
```

Every matrix in (9) has permanent `-1`, and fixed-complement Laplace gives

```text
sum_(|I|=2) Lambda_S(I)=-1                            (11)
```

for each of the six `S`.  The cofactor-image ranks for (8) are

```text
rho(01)=rho(23)=2,       rho(I)=1 otherwise.          (12)
```

Direct subpermanent multiplication gives

```text
Lambda_S(01)=Lambda_S(23)=0                           (13)
```

for every `S` and every `H_c`.  Therefore each fixed window has a nonzero
shore, but no fixed window has a nonzero shore at a `rho>=2` pair.

Lemma 1 guarantees that adjoining tangent companion blocks cannot change any
quantity in (9)--(13).

## 3. The common mixed lower-jet sector

On the tangent planes in (8), use local coordinates

```text
root 0: (e_0,e_1,e_2)|S_0=(0,x_1,y_1),
root 1: (e_0,e_1,e_2)|S_1=(0,x_2,y_2),
root 2: (e_0,e_1,e_2)|S_2=(u_3,0,y_3),
root 3: (e_0,e_1,e_2)|S_3=(u_4,0,y_4),
root 4: (e_0,e_1,e_2)|S_4=(u_5,x_5,0).               (14)
```

Let the two endpoint forms be

```text
(p_0,q_0)=(x_1,y_1),       (p_1,q_1)=(y_2,x_2),
(p_2,q_2)=(u_3,y_3),       (p_3,q_3)=(y_4,u_4),
(p_4,q_4)=(u_5,x_5).                                  (15)
```

Write

```text
R_ij=p_i q_j+q_i p_j.                                 (16)
```

The common tangent root--root blocks are

```text
L_01= y_1 y_2,                  L_23= y_3 y_4,
L_02=-x_1 y_3-y_1 u_3+y_1 y_3, L_03= y_1 y_4,
L_12= y_2 y_3,                 L_13=-y_2 u_4-x_2 y_4+y_2 y_4,
L_04=-y_1 u_5,                 L_14= x_2 x_5,
L_24= u_3 u_5,                 L_34=-y_4 x_5.          (17)
```

Extend (15)--(17) by (5).  The previously proved common `2+2+1` jet theorem
assigns one globally nonconflicting formal cofactor ledger to the two
parity-legal tags at every nonempty root subset.  With the blocks
(15)--(17), its exact graph-side expression equals

```text
sum_(c=0)^2 [product_(i in I)(e_c^*|S_i)] tensor D_c (18)
```

for every nonempty `I subset {0,1,2,3,4}`.  This includes all five
singletons, ten pairs, ten triples, five quartets, and the quintet: 31 mixed
lower-root tensor equations in one common companion system.

By Lemma 1, (18) and the pure data (9)--(13) hold simultaneously in one
common edge-block system.

### Theorem 2 (formal mixed-jet extension with fixed-window separation)

Over `Q`, there is one common bilinear root/root--endpoint/root--blocker
system and one globally nonconflicting formal principal-cofactor ledger that
simultaneously satisfy:

1. the canonical blocker profile and all three nonzero pure root
   permanents;
2. the complete fixed-complement graph-side window cover;
3. all 31 nonempty mixed lower-root GHZ equations; and
4. zero marked-shore product at every `rho>=2` root pair for every fixed
   retained pair `S`.

Proof.  The frozen sector is (8)--(13), the tangent sector is (14)--(18), and
Lemma 1 gives their common physical edge-block splice.  The formal cofactor
labels are unchanged from the common `2+2+1` theorem, hence remain globally
nonconflicting.

Consequently no argument using only the common mixed lower-root tensor
equations and formal deletion-label consistency can force

```text
Lambda_S(I)!=0 for some I with rho(I)>=2              (19)
```

for even one fixed `S`.  Any such theorem must use additional
principal-hafnian realizability or mixed blocker-word information.

## 4. Distinguished companion rank is independent of rho

For a root pair `ij`, the two distinguished even companion forms in this
model are

```text
g_empty=L_ij,            g_Q=R_ij                    (20)
```

because the residual--residual scalar is set to zero.  They are independent
for every one of the ten root pairs.  A compact coefficient-minor certificate
is:

| pair | monomial columns | determinant for rows `(L_ij,R_ij)` |
|:--|:--|--:|
| `01` | `y_1y_2, x_1x_2` | `1` |
| `02` | `y_1y_3, x_1y_3` | `1` |
| `03` | `y_1y_4, u_4x_1` | `1` |
| `04` | `x_1x_5, u_5y_1` | `1` |
| `12` | `y_2y_3, u_3x_2` | `1` |
| `13` | `y_2y_4, x_2y_4` | `1` |
| `14` | `x_5y_2, x_2x_5` | `-1` |
| `23` | `y_3y_4, u_3u_4` | `1` |
| `24` | `u_5y_3, u_3u_5` | `-1` |
| `34` | `x_5y_4, u_4u_5` | `-1` |

Every minor is a nonzero constant.  Therefore every fixed-complement shore
in this model can be chosen at a root pair with two independent distinguished
companion forms—even though every such nonzero shore has `rho=1` by
(12)--(13).

### Corollary 3 (root-side selector-ready fan)

The four graph-side fan windows

```text
1234, 1256, 1356, 1456                               (21)
```

can simultaneously coexist with two independent distinguished root
companions at each shore in the formal mixed-jet extension.

This is a root-side selector statement.  It does not prove that the selected
formal cofactors are the principal hafnians of one physical blocker/residual
graph, nor does it expose the four marked-star pair observations required by
tetrahedral tomography.

## 5. Exact remaining shared-block boundary

The logical hierarchy is now

```text
pure fixed-complement Laplace
    => every graph-side window and the tetrahedral fan;

common mixed lower-root jets + formal cofactor ledger
    !=> rho>=2 shore co-occurrence for a fixed window;

same formal model
    => independent distinguished companions at every shore;

common tensor-valued principal-hafnian realization
    + mixed blocker-word cancellation
    + legal marked-star rows
    remain UNKNOWN.                                  (22)
```

The next useful identity must therefore involve data not present in (18):

1. a common principal-hafnian relation linking different formal deletion
   values;
2. an unavoidable mixed blocker-colour word in every scalar lift of the
   ledger;
3. a shore-preserving marked-star selector equation; or
4. a common physical edge-block circuit coupling those marked-star rows to
   the selected top cofactors.

## Scope wall

```text
jet-orthogonal splice lemma:                         PROVED;
all 31 mixed lower-root equations in the splice:    PROVED;
all fixed graph-side windows retained:              PROVED;
rho>=2 shore product in the splice:                  ZERO FOR EVERY WINDOW;
distinguished companion independence in the splice: EVERY ROOT PAIR;
formal-cofactor fixed-S rho>=2 forcing theorem:      IMPOSSIBLE;
one common tensor principal-hafnian ledger:          UNKNOWN;
mixed blocker-word cancellation:                    UNKNOWN;
legal marked-star fan:                              UNKNOWN;
partition-closed P7 response window:                UNKNOWN;
P7 nonrestriction:                                  UNKNOWN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_221_jet_orthogonal_splice_and_formal_fixed_window_no_go.py
python claims/p7/audit_p7_221_jet_orthogonal_splice_and_formal_fixed_window_no_go.py
python -m py_compile claims/p7/verify_p7_221_jet_orthogonal_splice_and_formal_fixed_window_no_go.py claims/p7/audit_p7_221_jet_orthogonal_splice_and_formal_fixed_window_no_go.py
uv run --with ruff ruff check claims/p7/verify_p7_221_jet_orthogonal_splice_and_formal_fixed_window_no_go.py claims/p7/audit_p7_221_jet_orthogonal_splice_and_formal_fixed_window_no_go.py
```

The primary verifier replays the two certified component models, checks their
jet-orthogonal interface, verifies all 31 mixed lower-root equations, and
certifies every companion-rank minor and fixed-window shore statement.  The
independent no-import audit reconstructs the rational frozen matrices,
tangent companion forms, splice projectors, and formal ledger with separate
integer and sparse-polynomial routines.
