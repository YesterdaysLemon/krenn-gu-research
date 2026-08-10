# Degree-three hafnians exclude the disjoint extremal rank-six support

## Status

**Exact characteristic-zero arbitrary-graph obstruction.**  The earlier
three-mode residual theorem gives, in the common full-terminal quotient,

```text
|S_c|<=2,                         c=0,1,2,
sum_i rank(q_i restricted to E_i)<=6.                (1)
```

This note closes one complete extremal stratum.  If equality holds in (1),
the three colour supports are distinct two-element core sets.  They cannot
be pairwise disjoint.

Indeed, suppose they were three disjoint pairs on six core modes.  Every
four-set of those modes contains a complete colour-support pair.  The
corresponding nonzero degree-five residual permanent has a nonzero
three-row Laplace cofactor.  The prescribed degree-three equation on that
cofactor face then forces the projected four-mode core hafnian to vanish.
Thus all fifteen four-point hafnians on the six active modes vanish.

A new characteristic-zero lemma shows that a symmetric edge system with all
four-point hafnians zero has matching number at most two: it cannot contain
three disjoint nonzero edges.  But the three colour-support edges are forced
nonzero by the degree-five equations.  This contradiction excludes the
disjoint extremal stratum.

Overlapping support pairs remain possible at this layer.  An exact triangle
quotient diagram attains rank sum six and makes every four- and six-mode
quotient shadow vanish.  It is not asserted to lift to the full unprojected
ledger.  The global `P_7` restriction and Krenn--Gu conjecture remain
**UNRESOLVED**.

No graph family, support assignment, word, alignment, face family, or
parameter space is enumerated.

## 1. Extremal support normal form

Use the notation of
`P7_221_THREE_MODE_RESIDUAL_ANNIHILATION_AND_FULL_QUOTIENT_RANK_SUM_BOUND.md`:

```text
U_i=span{R_i,p:p in P},        q_i:V_i^* -> Q_i,
E_i=span{epsilon_i^0,epsilon_i^1,epsilon_i^2},
x_i^c=q_i(epsilon_i^c),
S_c={i:x_i^c!=0}.                                      (2)
```

Assume the extremal equality

```text
sum_i rank(q_i restricted to E_i)=6.                  (3)
```

The proof of (1) factors through

```text
sum_i rank(q_i|E_i)
 <=sum_i |{c:i in S_c}|
 =sum_c |S_c|
 <=6.                                                  (4)
```

Equality in (3) therefore forces equality everywhere in (4).  Hence

```text
|S_c|=2                                                (5)
```

for every colour, and at every mode the nonzero displayed colour images are
linearly independent.

The three support pairs are distinct.  If `S_c=S_d={i,j}`, then the
degree-five full-quotient pair condition says

```text
x_i^c tensor x_j^c,       x_i^d tensor x_j^d          (6)
```

are proportional.  Both tensors are nonzero, so their factors are
proportional at both modes.  This contradicts the equality condition in
(4), which makes the two local images independent.

Write the three distinct support edges as

```text
e_c=S_c,                         c=0,1,2.              (7)
```

## 2. Each support edge carries a nonzero projected core edge

For each colour `c`, choose one of the three prescribed degree-five faces

```text
F_01=1234a,       F_02=1235b,       F_12=1345b        (8)
```

on which its coefficient is nonzero.  Their exact responses are

```text
T_F01=alpha D_0-6D_1,
T_F02=rho D_0+beta D_2,
T_F12=rho D_1+beta D_2,                               (9)

alpha=1+43rho/21,                 beta=2(1+rho)/7.
```

Project the two modes of `e_c`.  A different colour `d` survives both maps
only if `e_c` is contained in `S_d`; by (5) this would say `e_c=e_d`, which
was excluded above.  Thus the projected formal response has exactly one
nonzero colour term.

The physical one-edge decomposition consequently becomes

```text
bar(A)_e_c tensor P_e_c^F
 =lambda_c (tensor_(i in e_c)x_i^c)
             tensor (tensor_(k notin e_c)epsilon_k^c) !=0.              (10)
```

In particular,

```text
bar(A)_e_c !=0,                   P_e_c^F !=0,         (11)
```

and `bar(A)_e_c` is proportional to the displayed two-mode pure tensor.
These are three nonzero projected core edges, one for each colour.

## 3. Four quotients factor every degree-three response

For a three-terminal face `G`, the no-terminal-edge physical response has
two core edges and a three-row permanent:

```text
T_G^(3)=sum_({e,f} disjoint)
          A_e tensor A_f tensor Per(R_(Z minus (e union f)),G).         (12)
```

Let `I` be four core modes.  Project all four through their full incidence
quotients.  To survive, the two core edges in a summand must cover every
mode of `I`; hence they form one of the three perfect matchings of `I`.
All three summands have the same residual permanent on `Z minus I`.  Thus

```text
(tensor_(i in I)q_i tensor id)T_G^(3)
 =H_I(bar A) tensor P_I^G,                            (13)

H_I(bar A)=sum_(mu a perfect matching of I)
              tensor_(e in mu) bar(A)_e,              (14)

P_I^G=Per(R_(Z minus I),G).                           (15)
```

Equation (13) is the degree-three common-core analogue of the one-edge
degree-five factorization.  It retains the shared projected core edges;
it is not merely a rank count.

The formal tensor on every prescribed three-face is a linear combination of
the three pure diagonals `D_c`.  Since every `S_c` has size two, projecting
any four modes kills every `D_c`.  Therefore every physical realization
must satisfy

```text
H_I(bar A) tensor P_I^G=0                             (16)
```

for all four-sets `I` and all three-faces `G`.

## 4. Degree-five Laplace descent makes the four-hafnian nonzero test legal

Assume now that the three support edges in (7) are pairwise disjoint, and
let

```text
W=e_0 disjoint_union e_1 disjoint_union e_2.          (17)
```

Fix any four-set `I` contained in `W`.  Selecting four vertices from three
two-element boxes forces `I` to contain one complete support edge, say
`e_c`.  Put `J=I minus e_c`.

Choose the face `F` used in (10).  Expand its nonzero five-row residual
permanent along the two residual modes in `J`:

```text
P_e_c^F
 =sum_(H subset F, |H|=2)
    Per(R_(J,H)) tensor P_I^(F minus H).               (18)
```

If every three-row factor on the right were zero, then `P_e_c^F` would be
zero, contrary to (11).  Hence some three-face

```text
G=F minus H                                           (19)
```

has `P_I^G!=0`.  All three-terminal faces are prescribed.  Equation (16)
then gives

```text
H_I(bar A)=0.                                         (20)
```

Since `I` was arbitrary,

```text
H_I(bar A)=0             for every four-subset I of W. (21)
```

This deduction uses the actual five-row permanent from degree five to
select a nonzero three-row cofactor.  It does not assume a generic minor.

## 5. A vanishing-four-hafnian matching lemma

### Lemma 1

Let `K` be a characteristic-zero field and let `(a_ij)` be symmetric edge
weights on six labelled vertices.  If

```text
a_ij a_kl+a_ik a_jl+a_il a_jk=0                      (22)
```

for every four distinct vertices `i,j,k,l`, then the nonzero-edge support
has matching number at most two.

### Proof

Suppose instead that three disjoint weights are nonzero.  Relabel and apply
independent nonzero vertex scalings to arrange

```text
a_01=a_23=a_45=1.                                     (23)
```

Put

```text
p=a_02, q=a_03, r=a_12, s=a_13,
u=a_04, v=a_05, w=a_14, z=a_15,
m=a_24, n=a_25, o=a_34, t=a_35.                       (24)
```

The equations on `0123`, `0145`, and the four sets containing `01` give

```text
1+ps+qr=0,                    1+uz+vw=0,              (25)

m=-pw-ur,      n=-pz-vr,
o=-qw-us,      t=-qz-vs.                              (26)
```

Substituting (26) into the four equations containing `23` gives, because
the characteristic is not two,

```text
u=pqw,          v=pqz,
w=rsu,          z=rsv.                                (27)
```

Equation `1+uz+vw=0` makes at least one of `uz,vw` nonzero.  Relations (27)
then make all eight variables in (24) before `m,n,o,t` nonzero.  With

```text
X=ps,                  Y=qr,                           (28)
```

the first equation in (25) and (27) imply

```text
X+Y=-1,                XY=1.                          (29)
```

Moreover `uz=XY vw=vw`, so the second equation in (25) gives

```text
2vw=-1.                                               (30)
```

Finally use the equation on `0245`:

```text
p+un+vm=0.                                            (31)
```

Substituting (26)--(29) reduces (31), after division by nonzero `p`, to

```text
1+(Y^2+X)vw=0.                                        (32)
```

From (29), `Y^2=X`.  Equations (30)--(32) therefore force `X=1`.
Then `XY=1` gives `Y=1`, contradicting `X+Y=-1` in characteristic zero.
This proves the lemma.

The lemma is a bosonic analogue of a support theorem for Pluecker-type
quadrics: cancellation among the three perfect matchings of every four-set
cannot coexist with a six-vertex perfect matching in the edge support.

## 6. Exclusion of the disjoint extremal branch

For every active mode `i in W`, equality in (4) and disjointness leave one
surviving prescribed colour direction.  Choose a linear functional

```text
ell_i:Q_i -> K,             ell_i(x_i^c)=1             (33)
```

for that colour.  Scalarize each projected core edge by

```text
a_ij=(ell_i tensor ell_j)(bar(A)_ij).                 (34)
```

Equation (21) becomes the scalar four-hafnian equation (22).  Equation
(10) makes each of

```text
a_e0,             a_e1,             a_e2              (35)
```

nonzero.  They are three disjoint edges on `W`, contradicting Lemma 1.

### Theorem 2 (disjoint extremal rank-six obstruction)

No physical realization of the formal `2+2+1` ledger can satisfy both

```text
sum_i rank(q_i|E_i)=6
```

and pairwise disjointness of the three two-mode colour supports `S_0,S_1,S_2`.
Therefore every surviving extremal realization must have

```text
S_c intersect S_d != empty
```

for at least one pair of colours.

## 7. Degree one and the exact surviving boundary

The same matching argument gives the degree-one six-port factorization.  If
`I=Z minus {k}` has six modes, then for a singleton terminal face `{p}`,

```text
(tensor_(i in I)q_i tensor id)T_{p}^(1)
 =H_I^(6)(bar A) tensor R_k,p.                        (36)
```

Here `H_I^(6)` is the three-edge hafnian tensor on the six quotient modes.
The formal diagonal side is already killed because every colour support has
size at most two.  Hence

```text
H_I^(6)(bar A) tensor R_k,p=0                         (37)
```

for every `k,p`.  This is exact, but it is not needed for Theorem 2 and does
not yet exclude the overlapping-support branch.

That branch is nonempty at the quotient-shadow level.  Take

```text
S_0={0,1},              S_1={1,2},              S_2={0,2}.             (38)
```

Let the quotient ranks on modes `0,1,2` be two with their displayed colour
images independent, and let every other quotient be zero.  The rank sum is
six.  Every pair supports at most one nonzero diagonal pair tensor.  Every
four- or six-mode quotient includes a zero quotient mode, so (16) and (37)
hold identically.  The three dedicated projected edges can all be nonzero
on the triangle `01,12,02` without contradicting Lemma 1.

This triangle is a legal incidence-span diagram: in `V_i^*=E_i`, take

```text
U_0=<epsilon_0^1>,       U_1=<epsilon_1^2>,
U_2=<epsilon_2^0>,       U_i=E_i for i=3,4,5,6,       (39)
```

and generate these spans with terminal columns `1,3,5`.  It is not asserted
to realize the nonzero unprojected responses or their residual permanents.

## 8. Exact boundary

Proved:

- the equality normal form for rank sum six;
- distinctness of the three two-mode colour supports;
- nonzero projected core edges on all three support pairs;
- exact four-mode degree-three hafnian/permanent factorization;
- legal descent from each nonzero five-row residual to a nonzero three-row
  residual;
- the characteristic-zero vanishing-four-hafnian matching lemma;
- exclusion of pairwise disjoint support pairs at rank sum six;
- the exact degree-one six-port quotient equation;
- an overlapping triangle quotient diagram surviving all these quotient
  shadows.

Not proved:

- exclusion of the triangle, star, path, or other overlapping support-pair
  configurations;
- a full physical lift of the triangle diagram;
- exclusion of rank sum below six;
- compatibility or incompatibility with the unprojected degree-one and
  degree-three equations on the overlapping branch;
- the `P_7 -> Delta_3` restriction or global Krenn--Gu conjecture.

```text
rank sum six + disjoint colour-support pairs:      EXCLUDED;
rank sum six + overlapping support pairs:          UNKNOWN;
overlap triangle at quotient-shadow level:         EXISTS;
rank sum below six:                                 UNKNOWN;
P7 and global Krenn--Gu:                            UNRESOLVED.           (40)
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_221_extremal_rank_six_disjoint_support_degree3_hafnian_obstruction.py
python claims/p7/audit_p7_221_extremal_rank_six_disjoint_support_degree3_hafnian_obstruction.py
python -m py_compile claims/p7/verify_p7_221_extremal_rank_six_disjoint_support_degree3_hafnian_obstruction.py claims/p7/audit_p7_221_extremal_rank_six_disjoint_support_degree3_hafnian_obstruction.py
uv run --with ruff ruff check claims/p7/verify_p7_221_extremal_rank_six_disjoint_support_degree3_hafnian_obstruction.py claims/p7/audit_p7_221_extremal_rank_six_disjoint_support_degree3_hafnian_obstruction.py
```

The primary replay checks the exact coefficient antecedent, the hand
identities in Lemma 1, its normalized characteristic-zero ideal, a symbolic
five-row Laplace identity, and the overlapping triangle boundary.  The
independent audit imports no project code or computer algebra and verifies
the hand identities with a small rational sparse-polynomial implementation.
Neither replay searches graphs, supports, faces, words, alignments, or
parameters.
