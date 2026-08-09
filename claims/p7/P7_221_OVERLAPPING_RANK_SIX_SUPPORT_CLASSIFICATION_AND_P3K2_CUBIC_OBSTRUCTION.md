# Overlapping rank-six supports: exact classification and the `P3+K2` cubic obstruction

## Status

**Exact characteristic-zero arbitrary-graph obstruction, with sharp quotient
controls.**  In the extremal full-terminal quotient of the formal `2+2+1`
ledger, the three colour supports are distinct two-element sets and the rank
sum is six.  Regard those supports as the three edges of a simple graph.

There are structurally only five possibilities:

```text
3K2,          P3 disjoint-union K2,          P4,
K1,3,         K3.                                             (1)
```

The earlier six-vertex four-hafnian theorem excludes `3K2`.  This note
excludes `P3 disjoint-union K2`.  Thus every surviving equality case has
support graph

```text
P4,                    K1,3,                    or K3.          (2)
```

The exclusion uses the full, unprojected five-row residual permanent.  Its
nonvanishing legally selects a nonzero three-row Laplace cofactor on every
four-set containing the associated support edge.  The prescribed
degree-three equation then forces the projected four-hafnian tensor to
vanish.  On `P3 disjoint-union K2`, the five resulting tensor equations have
an explicit characteristic-zero unit-ideal certificate.

This is sharp for the information extracted here.  Exact projected core
systems for `K3`, `K1,3`, and `P4` satisfy every forced four-mode
degree-three shadow and every six-mode degree-one shadow.  These controls are
not asserted to lift to the full unprojected response ledger.  The `P_7`
restriction and the Krenn--Gu conjecture remain **UNRESOLVED**.

No graph family, support assignment, terminal word, alignment, face family,
or parameter space is enumerated.

## 1. Extremal setup

Use the common full-terminal quotient notation

```text
U_i=span{R_i,p:p in P},                 q_i:V_i^* -> Q_i,
E_i=span{epsilon_i^0,epsilon_i^1,epsilon_i^2},
x_i^c=q_i(epsilon_i^c),
S_c={i:x_i^c!=0}.                                      (3)
```

The rank-sum-six equality theorem gives

```text
|S_c|=2,                                               (4)

sum_i rank(q_i restricted to E_i)=6,                  (5)
```

and the nonzero displayed colour images at every mode are linearly
independent.  The three sets `S_0,S_1,S_2` are distinct.  For every colour
`c`, one prescribed degree-five face `F_c` gives

```text
bar(A)_S_c tensor P_S_c^F_c
 =lambda_c (tensor_(i in S_c)x_i^c)
              tensor (tensor_(k notin S_c)epsilon_k^c) !=0.    (6)
```

Here `bar(A)_ij=(q_i tensor q_j)A_ij`, and `P_e^F` is the actual five-row
residual permanent after deleting the endpoints of `e`.  In particular,

```text
bar(A)_S_c !=0,                    P_S_c^F_c !=0.       (7)
```

The exact coefficients behind (6) are those of the three faces

```text
F_01=1234a,             F_02=1235b,             F_12=1345b,

T_F01=alpha D_0-6D_1,
T_F02=rho D_0+beta D_2,
T_F12=rho D_1+beta D_2,                               (8)

rho^2=21,       alpha=1+43rho/21,       beta=2(1+rho)/7.
```

Every colour has a nonzero coefficient on at least one of these faces over
characteristic zero.

## 2. Full residual descent at degrees three and one

For a four-set `I`, let

```text
H_I(bar A)=sum_(mu a perfect matching of I)
                 tensor_(e in mu)bar(A)_e.             (9)
```

For a six-set `I`, define `H_I^(6)(bar A)` analogously using its three-edge
perfect matchings.

### Theorem 1 (universal cubic cofactor descent)

If a four-set `I` contains a colour-support edge `e=S_c`, then

```text
H_I(bar A)=0.                                         (10)
```

### Proof

Put `J=I minus e`, so `|J|=2`.  Expand the nonzero five-row permanent in
(7) along the two residual rows `J`:

```text
P_e^F=sum_(H subset F, |H|=2)
          Per(R_J,H) tensor P_I^(F minus H).           (11)
```

Since the left side is nonzero, some summand is nonzero.  Hence for some
three-face `G=F minus H`,

```text
P_I^G !=0.                                            (12)
```

Project the exact degree-three equation through `q_i` on every `i in I`.
Every prescribed diagonal tensor is killed because every colour support has
size two.  The physical two-core-edge expansion factors as

```text
H_I(bar A) tensor P_I^G=0.                            (13)
```

Equation (12) and tensor cancellation over a field give (10).  Notice that
the proof does not assume a generic residual minor: it selects a nonzero
cofactor from the actual unprojected permanent in (7).

### Theorem 2 (universal singleton cofactor descent)

If a six-set `I` contains a colour-support edge `e=S_c`, then

```text
H_I^(6)(bar A)=0.                                     (14)
```

### Proof

Write `I=Z minus {k}` and put `J=I minus e`, so `|J|=4`.  Four-row Laplace
expansion of the same nonzero five-row residual gives

```text
P_e^F=sum_(H subset F, |H|=4)
          Per(R_J,H) tensor R_(k,F minus H).           (15)
```

Some summand is nonzero, so `R_k,p!=0` for some singleton terminal
`p in F`.  After quotienting the exact degree-one response at the six modes
of `I`, all terms with a terminal incidence at a mode of `I` vanish.  The
only surviving physical term is

```text
H_I^(6)(bar A) tensor R_k,p.                           (16)
```

The formal diagonal side is zero because no colour support contains six
modes.  Therefore (16) is zero, and `R_k,p!=0` gives (14).

Theorem 2 is an exact use of the unprojected singleton equations.  It need
not produce a type-only contradiction: in every overlapping type in (1),
the displayed colour images occupy at most five modes, so a further
projection to their displayed spans makes every six-mode tensor tautologically
zero.  Extra quotient directions, if present, remain constrained by (14).

## 3. Structural classification of the three support edges

Let `Gamma` be the simple graph with edge set `{S_0,S_1,S_2}`.  It has three
distinct edges and degree sum six.

- If `Delta(Gamma)=3`, all three edges meet one vertex, so `Gamma=K1,3`.
- If `Delta(Gamma)=2` and a component is a cycle, all three edges form `K3`.
- If `Delta(Gamma)=2` and the largest path has three edges, `Gamma=P4`.
- If `Delta(Gamma)=2` and the largest path has two edges, the remaining edge
  is disjoint, so `Gamma=P3 disjoint-union K2`.
- If `Delta(Gamma)=1`, `Gamma=3K2`.

This proves (1) without listing labelled supports.  The `3K2` case is already
excluded by the characteristic-zero six-vertex matching lemma.  It remains
to analyze the four overlap types.

## 4. The `P3 disjoint-union K2` equations form the unit ideal

Suppose, after relabelling colours and modes,

```text
S_0={0,1},                 S_1={1,2},
S_2={3,4}.                                             (17)
```

At mode `1`, the two displayed colour images are independent.  Map its
quotient to a two-dimensional space with basis `(e_0,e_1)` carrying those
images.  At modes `0,2,3,4`, choose scalar quotient functionals that are
nonzero on their unique displayed colour images.  Kill all unused quotient
directions.  Equation (6) lets us normalize the three dedicated projected
edges to

```text
a_01=e_0,                    a_12=e_1,
a_34=1.                                                (18)
```

Write the remaining scalar edges and the two vector edges as

```text
a_02=p,       a_03=x,       a_04=y,
a_23=u,       a_24=v,
a_13=r e_0+s e_1,           a_14=t e_0+w e_1.          (19)
```

Every four-subset of `{0,1,2,3,4}` contains a support edge, so Theorem 1
applies.  The needed components of the five equations `H_I=0` are

```text
A=u+pr=0,                 B=x+ps=0,
C=v+pt=0,                 D=y+pw=0,                    (20)

E=1+xt+yr=0,
F=p+xv+yu=0.                                          (21)
```

The first pair comes from `I=0123`, the second from `I=0124`, `E` is the
`e_0` component on `0134`, and `F` is the scalar equation on `0234`.
The omitted components are unnecessary.

The following is an explicit ideal certificate:

```text
pE+F-xC-yA=2p,                                        (22)

E-tB-rD + ((st+rw)/2)(pE+F-xC-yA)=1.                 (23)
```

Thus equations (20)--(21) generate the unit ideal whenever `2` is
invertible.  In particular they have no solution in characteristic zero.

### Theorem 3 (`P3 disjoint-union K2` obstruction)

No physical realization of the formal `2+2+1` ledger can have rank sum six
and support graph `P3 disjoint-union K2`.

This theorem uses only six named tensor components after the general
Laplace descent.  It is not a labelled-support computation or a parameter
search.

## 5. Exact controls for the three surviving quotient types

The remaining three types cannot be excluded by (10) and (14) alone.  The
following reduced quotient-core systems are exact controls.  All omitted
projected edges are zero, and every inactive displayed quotient space is
zero.  At each active mode, take the displayed colour images indexed by its
incident support edges as a basis.  The local ranks are therefore the graph
degrees and sum to six.  Because the support edges are distinct, every pair
of modes supports at most one nonzero diagonal pair tensor, so the original
full-terminal pair-rank condition is also satisfied.

### Triangle `K3`

Take the three support edges `01,12,02`, with a two-dimensional displayed
quotient at each of modes `0,1,2`, and put a nonzero dedicated pure tensor on
each edge.  There is no four-set of active displayed modes.  Hence every
four-mode equation (10) and every six-mode equation (14) vanishes after the
displayed-span projection.

### Star `K1,3`

Let the support edges be `01,02,03`.  At the centre use independent basis
vectors `e_0,e_1,e_2`; each leaf quotient is one-dimensional.  Put

```text
bar(A)_01=e_0,             bar(A)_02=e_1,
bar(A)_03=e_2.                                          (24)
```

The only active four-hafnian is zero because no two nonzero edges in (24)
are disjoint.

### Path `P4`

Let the support edges be `01,12,23`.  Use bases

```text
Q_0=<a>,        Q_1=<u,v>,        Q_2=<s,t>,        Q_3=<d>.
```

Put

```text
bar(A)_01=a tensor u,          bar(A)_12=v tensor s,
bar(A)_23=t tensor d,

bar(A)_02=a tensor t,          bar(A)_13=-u tensor d,
bar(A)_03=0.                                             (25)
```

Then the only active four-hafnian is

```text
H_0123
 =(a tensor u)(t tensor d)
  +(a tensor t)(-u tensor d)
  +0(v tensor s)
 =0.                                                     (26)
```

The middle dedicated edge remains nonzero; the two cross edges cancel the
matching made by the two outer support edges.  Projecting either endpoint
pair `S_c` still isolates its dedicated edge, because neither cross edge
contains both endpoints of a support pair.

These are honest tensors in vertexwise quotient spaces, not global
idempotent coefficients.  They prove sharpness of the quotient equations,
but they do not specify compatible terminal columns or lift (6) for all
prescribed faces.  In particular they are not physical counterexamples to
the `P_7` restriction.

## 6. Exact boundary

Proved:

- the structural five-type classification of three distinct support pairs;
- universal degree-five-to-degree-three cofactor descent for every four-set
  containing a support edge;
- universal degree-five-to-degree-one cofactor descent for every six-set
  containing a support edge;
- an explicit characteristic-zero unit-ideal certificate excluding
  `P3 disjoint-union K2`;
- together with the earlier theorem, exclusion of both `3K2` and
  `P3 disjoint-union K2` at rank sum six;
- exact quotient-core controls for `K3`, `K1,3`, and `P4`.

Not proved:

- a full unprojected physical lift of any of the three controls;
- exclusion of `K3`, `K1,3`, or `P4` using residual permanents beyond the
  forced shadows (10) and (14);
- compatibility of the controls with the complete degree-one,
  degree-three, degree-five, and degree-seven ledger simultaneously;
- exclusion of rank sum below six;
- the `P_7 -> Delta_3` restriction or the global Krenn--Gu conjecture.

```text
rank six + 3K2:                         EXCLUDED (earlier theorem);
rank six + P3 disjoint-union K2:        EXCLUDED (this note);
rank six + P4, K1,3, or K3:             UNKNOWN physically;
P4, K1,3, K3 quotient-core shadows:     EXIST;
rank sum below six:                     UNKNOWN;
P7 and global Krenn--Gu:                UNRESOLVED.       (27)
```

## Replay

```powershell
uv run --with sympy python verify_p7_221_overlapping_rank_six_support_classification_and_p3k2_cubic_obstruction.py
python audit_p7_221_overlapping_rank_six_support_classification_and_p3k2_cubic_obstruction.py
python -m py_compile verify_p7_221_overlapping_rank_six_support_classification_and_p3k2_cubic_obstruction.py audit_p7_221_overlapping_rank_six_support_classification_and_p3k2_cubic_obstruction.py
uv run --with ruff ruff check verify_p7_221_overlapping_rank_six_support_classification_and_p3k2_cubic_obstruction.py audit_p7_221_overlapping_rank_six_support_classification_and_p3k2_cubic_obstruction.py
```

The primary verifier checks both generic five-row Laplace splittings, the
exact ideal certificate, a Groebner unit-ideal cross-check, the structural
degree signatures, and all three quotient controls.  The independent audit
imports no project code and no computer algebra; it repeats the certificate
over a minimal rational sparse-polynomial implementation and checks the
controls directly.  Neither replay searches graphs, supports, words, faces,
alignments, or parameter values.
