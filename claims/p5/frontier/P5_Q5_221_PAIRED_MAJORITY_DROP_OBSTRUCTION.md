# Paired-majority drop obstruction in normalized `q5_221`

## Status

This is an exact conditional obstruction over `C` inside normalized
`q5_221`.

Let `D_0,D_1,D_2` be the exact rank-drop sets from
[`P5_Q5_221_HYPERPLANE_INCIDENCE_REDUCTION.md`](P5_Q5_221_HYPERPLANE_INCIDENCE_REDUCTION.md),
where colours zero and one have source multiplicity two and colour two
has source multiplicity one.  Then it is impossible that

```text
D_0=D_1={A,B}.                                        (1)
```

Thus the two multiplicity-two colours cannot have the same exact
two-mode drop set.  In particular, the exact triple-parallel,
double-plus-adjacent, and double-plus-disjoint marked types in which
the singleton colour is the lone edge are impossible.

This does not exclude the complementary pattern (2), the other marked
incidence types, all of normalized `q5_221`, `P_5 -> Delta_3`, or the
arbitrary-order prize conjecture.

## Setup

Use

```text
x_+=e_0+e_1,  x_-=e_0-e_1,
y_+=e_2+e_3,  y_-=e_2-e_3,  z=e_4,
```

and identify the distinguished-mode contraction covectors and
hyperplane normals as

```text
u_0=x_+, u_1=y_+, u_2=z,
h_0=x_-, h_1=y_-, h_2=z.
```

Every remaining local map

```text
L_i:C^5 -> C^3
```

has rank three.  Indeed, its target image must contain the three
independent factors `e_0,e_1,e_2` occurring in the nonzero pure target
terms.

Assume (1).  First suppose, for a contradiction, that `A in D_2`.  Its row
space contains the three independent normals, hence

```text
U_A=span(h_0,h_1,h_2)=:K.                             (3)
```

## First cross-contraction

Because `B in D_1`, there is a target covector `alpha_(B,1)` with

```text
L_B^* alpha_(B,1)=h_1.
```

Contract the colour-zero pure `P_4` identity in mode `B` by this
covector.  The remaining source tensor is, up to a nonzero sign,

```text
Q_01=Sym(x_+,y_-,z)
```

on

```text
J_01=span(x_+,y_-,z),
J_01^perp=span(h_0,u_1).
```

Its image through modes `A,C,D` is either zero or a nonzero pure cube
in target colour zero.

The restriction of (3) to `J_01` is the coordinate plane

```text
span((y_-)^*,z^*),
```

which has rank two and kills the first factor `x_+`.

Modes `C,D` do not belong to `D_0`, so `h_0` is absent from their row
spaces.  Equivalently, each restriction `L_i|H_0` has rank three.
Since `J_01` is a three-space inside the four-space `H_0`, restricting
once more can lower rank by at most one:

```text
rank(L_C|J_01)>=2,   rank(L_D|J_01)>=2.               (4)
```

If the image of `Q_01` were a nonzero pure cube, the decomposable-`P_3`
classification would apply to the three rank-at-least-two maps in
(4).  It forbids the support-one plane normal present in mode `A`.
Therefore the image is zero.

The zero-`P_3` theorem now says that all three restricted row spaces are
the same coordinate plane.  Since the plane in mode `A` kills `x_+`,

```text
L_C(x_+)=L_D(x_+)=0.                                  (5)
```

## Second cross-contraction

Repeat the argument with the colour-one identity, contracting mode `B`
by the covector pulling back to `h_0`.  The residual tensor is

```text
Q_10=Sym(x_-,y_+,z)
```

on `J_10`.  The restriction of `K` in mode `A` is now the coordinate
plane that kills `y_+`.  Because `C,D` do not belong to `D_1`, their
restrictions to `J_10` again have rank at least two.  The nonzero pure
case is excluded by the same support-one normal, and the zero theorem
gives

```text
L_C(y_+)=L_D(y_+)=0.                                  (6)
```

## Contradiction

The vectors `x_+,y_+` are independent.  Equations (5)-(6) put both in
the two-dimensional kernels of the rank-three maps `L_C,L_D`.
Therefore

```text
ker L_C=ker L_D=span(x_+,y_+),
U_C=U_D=span(h_0,h_1,h_2)=K.
```

In particular, `C,D` belong to both `D_0` and `D_1`, contradicting
(1).  Hence `A notin D_2`; the same argument applies to `B`.  The
rank-drop lower bound `|D_2|>=2` then leaves only

```text
D_0=D_1={A,B},   D_2={C,D}.                           (7)
```

## The complementary singleton pair is impossible

It remains to exclude (7).  Cross-contract the colour-zero and
colour-one identities at mode `A`.  Through modes `B,C,D` they produce
the zero-or-pure residuals `Q_01` and `Q_10`.

There are two possible rank-one exceptions at mode `B`:

```text
rank(L_B|J_01)=1  iff  u_1 in U_B,
rank(L_B|J_10)=1  iff  u_0 in U_B.                    (8)
```

The equivalences follow from

```text
J_01^perp=span(h_0,u_1),
J_10^perp=span(u_0,h_1)
```

and `h_0,h_1 in U_B`.  The two exceptions cannot occur together,
because `h_0,u_0,h_1,u_1` are four independent covectors while
`dim U_B=3`.

Suppose first that `u_1 in U_B`.  Then

```text
U_B=span(h_0,h_1,u_1),
```

and its restriction to `J_10=span(x_-,y_+,z)` is the rank-two
coordinate plane that kills `z`.  Modes `C,D` are outside `D_1`, so
their `J_10` restrictions have rank at least two.  A nonzero pure
`Q_10` is forbidden by the support-one normal in mode `B`; if `Q_10`
is zero, the zero-`P_3` theorem forces modes `C,D` to kill `z` as well.
That contradicts `h_2 in U_C,U_D`, because `h_2(z)=1`.  Thus
`u_1 notin U_B`.  The symmetric argument gives

```text
u_0 notin U_B.                                        (9)
```

Consequently both residual maps at `B` have rank two.  The restrictions
at `C,D` have rank at least two because those modes are outside
`D_0,D_1`.

If `Q_01` had nonzero pure image, the `P_3` classification would apply.
The mode-`B` restricted plane contains the coordinate covector dual to
`y_-`, so its projective normal has zero `y_-` coordinate.  A
support-one normal is forbidden, hence its support would be exactly

```text
{x_+,z}.                                               (10)
```

But mode `C` contains `h_2`, whose restriction is the coordinate
covector dual to `z`.  Its plane normal therefore has zero `z`
coordinate.  The nonzero `P_3` classification requires all three plane
normals to have the same coordinate support, contradicting (10).
Thus `Q_01` is zero.

The same argument for `Q_10` says that the mode-`B` normal would have
support `{y_+,z}`, whereas the mode-`C` normal again has zero `z`
coordinate.  Hence `Q_10` is zero too.

Finally, the two independent covectors in mode `A` have zero diagonal
target entries.  Their two cross entries cannot both vanish, so at
least one of `Q_01,Q_10` must have nonzero pure image.  This contradicts
the preceding paragraph and excludes (7).  Therefore (1) is
impossible.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q5_221_paired_majority_drop.py
python claims/p5/frontier/audit_p5_q5_221_paired_majority_drop.py
```

The primary verifier checks both residual source spaces, their
annihilators, the two support-one coordinate-plane restrictions of
`K`, the exceptional rank-one boundaries, the incompatible normal
supports in the complementary branch, and the final common kernel.
The independent audit enumerates all rank-three row spaces over `F_3`
and `F_5` and checks the rank gates and annihilator conclusions without
importing the primary code.
The finite-field census audits the linear-algebra boundary; the written
argument above is over `C`.
