# An aligned 2+2+1 core identification passes every prescribed degree-five mixed face

## Status

**Exact six-parameter completion for one fixed alignment and one fixed mixed
word.**  Relabel the colour-2 core roles against the colour-0 roles by

```text
z_*       -> f_1,
(z_1,z_2) -> (ell,h_3),
(z_3,z_4) -> (h_5,h_a),
(z_5,z_6) -> (f_2,h_4).                               (1)
```

Evaluate colour 2 on the physical positions occupied by `z_*,z_1,z_2` and
colour 0 on the other four positions.  Keep every same-colour core edge and
every frozen core--terminal incidence fixed by the exact scalar
certificates, while allowing all twelve cross-colour core edges to vary.

The twenty prescribed mixed-zero degree-five Wick faces form an affine
`20 x 12` system over `Q(rho)`, `rho^2=21`.  Its coefficient and augmented
ranks are both six.  Hence it is consistent and has an explicit
six-parameter solution family.

The seven degree-one mixed-zero conditions are also consistent: one exact
point of the degree-five family satisfies all of them.  This note originally
stopped before degree three.  The later three-face theorem proves that the
entire six-parameter family fails there.  This remains a positive boundary
for degrees five and one, not a tensor realization.

## 1. Fixed physical order and mixed incidence

Order the physical core positions by the colour-0 roles

```text
(f_1,f_2,ell,h_3,h_4,h_5,h_a)=(0,1,2,3,4,5,6).       (2)
```

Under (1), the mixed colour word is therefore

```text
(2,0,2,2,0,0,0).                                      (3)
```

Put

```text
alpha=5+2rho/21,
beta =1+16rho/21,
C    =230+104rho/7,
delta=6+rho/21.                                       (4)
```

With terminal columns ordered `(1,2,3,4,5,a,b)`, the frozen incidence matrix
for (3) is

```text
R=
[ 0 0 0 0 1/7 0 0     ]
[ 0 1 0 0 0   0 0     ]
[ 1 0 1 0 0   0 0     ]
[ 0 1 0 1 0   0 0     ]
[ 0 0 0 1 0   0 -alpha]
[ 0 0 0 0 1   0 C     ]
[ 0 0 0 0 0   1 beta  ].                              (5)
```

The fixed same-colour core edges are

```text
A_23=1,
A_45=-6-rho/21,
A_46=rho/21,
A_56=1+22rho/21,                                      (6)
```

and the other same-colour edges vanish.  Denote the twelve free cross edges
by

```text
x_ij=A_ij,       i in {0,2,3}, j in {1,4,5,6}.        (7)
```

The orientation in (7) only names the variables; the core matrix is
symmetric.

## 2. The twenty-face compound system

For a surviving five-terminal set `S`, the no-terminal-edge response is the
one-core-edge Laplace formula

```text
Phi_S=sum_(0<=i<j<=6) A_ij per R[Z\{i,j},S].           (8)
```

The formal ledger prescribes the mixed coefficient to be zero on every
five-set except

```text
P\Q={1,2,3,4,5},                                      (9)
```

which corresponds to the free deletion `Q={a,b}`.  Thus (8) gives exactly
twenty affine equations in the twelve variables (7).

Nine face equations vanish identically:

```text
1234a, 1234b, 1235a, 1235b, 123ab,
1345a, 1345b, 134ab, 135ab.                           (10)
```

Five pairs of faces give duplicate equations:

```text
1245a=2345a,       1245b=2345b,
124ab=234ab,       125ab=235ab,
145ab=345ab.                                           (11)
```

After (10)--(11), the complete system is the following six equations:

```text
x_01+x_04+x_35/7-delta/7=0,                            (12)

beta(x_01+x_04)+(beta/7)x_35-alpha x_06
  +(C/7)x_36+(1+rho)/7=0,                              (13)

C(x_01+x_04)-alpha x_05=0,                             (14)

-alpha x_01+(C/7)x_34-(alpha/7)x_35=0,                (15)

-alpha x_01+(C/7)x_31=0,                              (16)

(C/7)(x_21+x_24+1)-(alpha/7)x_25=0.                   (17)
```

Direct exact row reduction gives

```text
rank(coefficient matrix)=6,
rank(augmented matrix)=6.                              (18)
```

No dual face circuit with nonzero constant exists in this system.

## 3. Exact six-parameter solution

Take

```text
x_24,x_25,x_26,x_34,x_35,x_36                         (19)
```

as free parameters.  Solve (12)--(17) by

```text
x_01 = C x_34/(7alpha)-x_35/7,

x_04 = delta/7-C x_34/(7alpha),

x_05 = C(delta-x_35)/(7alpha),

x_06 = C x_36/(7alpha)
       +(beta delta+1+rho)/(7alpha),

x_21 = -1-x_24+alpha x_25/C,

x_31 = x_34-alpha x_35/C.                              (20)
```

Substitution of (20) into the original twenty responses, before removing the
zero and duplicate rows, makes every response exactly zero.  Therefore:

### Theorem 1 (aligned degree-five affine completion)

For the fixed alignment (1), mixed word (3), fixed same-colour data (5)--(6),
and arbitrary parameters (19), equation (20) supplies all twelve cross-core
entries and satisfies every prescribed mixed-zero degree-five face.

This is an exact characteristic-zero statement over `Q(sqrt(21))`; no
genericity or numerical approximation is used.

## 4. A degree-one extension point

The next smallest Wick boundary has seven degree-one coefficients.  It is
also consistent with the degree-five family.  In (19), set

```text
x_34=0,       x_35=0,       x_36=1,       x_26=0,

x_24=337/506778-(41206/1773723)rho,

x_25=23005/521+(11638/10941)rho,                       (21)
```

and obtain the other six cross edges from (20).  Direct hafnian evaluation
gives

```text
Phi_1=Phi_2=Phi_3=Phi_4=Phi_5=Phi_a=Phi_b=0.           (22)
```

Thus neither the twenty degree-five faces nor the seven degree-one faces
exclude this aligned mixed word.  The later note
`P7_221_ALIGNED_CORE_DEGREE3_THREE_FACE_NULLSTELLENSATZ_OBSTRUCTION.md`
shows that three of the 35 degree-three faces already generate the unit
ideal on this family.

## 5. Sharp scope

This result concerns exactly one prescribed alignment and one prescribed
mixed word.  It does not search alignments, permutations, supports, words,
or graphs.  It also does not prove:

- the degree-three mixed-zero equations;
- cancellation of other mixed core words for the same alignment;
- one tensor graph realizing the entire formal ledger;
- tangent-jet compatibility beyond the frozen cofactor layer;
- a `P_7` restriction or counterexample; or
- the Krenn--Gu conjecture.

The exact boundary is

```text
alignment (1), degree-five mixed faces:  CONSISTENT, DIMENSION SIX;
one degree-one extension point:          REALIZED;
degree-three faces:                      EXCLUDED LATER;
all mixed words / full tensor graph:     EXCLUDED FOR THESE FIXED CHARTS;
global Krenn--Gu:                        UNRESOLVED.     (23)
```

The all-word statement in the status wall uses the separate
`P7_221_ARBITRARY_ALIGNMENT_DEGREE5_RECTANGLE_OBSTRUCTION.md`, which selects
an obstructing word from any alignment.  It still does not exclude different
scalar realizations of the pure ledger.

## Replay

```powershell
uv run --with sympy python verify_p7_221_aligned_core_degree5_affine_completion.py
python audit_p7_221_aligned_core_degree5_affine_completion.py
python -m py_compile verify_p7_221_aligned_core_degree5_affine_completion.py audit_p7_221_aligned_core_degree5_affine_completion.py
uv run --with ruff ruff check verify_p7_221_aligned_core_degree5_affine_completion.py audit_p7_221_aligned_core_degree5_affine_completion.py
```

The primary verifier reconstructs the fixed matrices (5)--(7), evaluates the
twenty responses (8), checks both ranks in (18), substitutes the full family
(20), and checks the seven degree-one hafnians at (21).  The independent
audit imports neither SymPy nor the primary verifier; it repeats the
calculation with exact rational-pair arithmetic in
`Q[rho]/(rho^2-21)`, including its own Gaussian elimination.  Neither replay
performs an alignment, support, word, permutation, or graph search.
