# Arbitrary permanent fixed-pair singleton-exceptional companion propagation theorem

## Status

This note proves an exact characteristic-zero propagation rule inside the
exceptional-line residual of
`ARBITRARY_PERMANENT_FIXED_PAIR_EXCEPTIONAL_KERNEL_NECESSITY_THEOREM.md`.
If a rank-two local projection has a kernel generator supported on a single
local colour, then one of the other three local planes must meet an explicit
residual-kernel line or plane.  The exact target equations then force the
colour of that companion incidence.

For four of the five distinct exceptional ambient lines, propagation returns
to the original line after one more step.  For the common exceptional line
`K(x_2+x_3)`, the generic companion also returns to that line, while one
special companion returns only to an explicit two-plane.  Thus the result is
a finite incidence reduction, not an exclusion.  It does not prove that an
exceptional low is singleton-supported and does not rule out the resulting
two-cycles.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Fixed pair and exceptional lines

Let `K` be a field of characteristic zero and work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

Use the fixed equality-five pair and exact target equations

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (1)
```

from the predecessor.  Split the complement space as

```text
K^6=R direct-sum A,
R=span{x_0,x_1,x_2,x_3},             A=span{x_4,x_5},  (2)
```

and put

```text
J((s_4,s_5),(t_4,t_5))=s_4t_5+s_5t_4.                 (3)
```

The five complementary quartics are

```text
star(m_1)= x_4x_5 x_1 (x_3-x_2-x_0),
star(m_2)= x_4x_5 x_0 (x_3-x_2-x_1),
star(d_0)= x_4x_5 (x_1+x_2)(x_3-x_0),
star(d_1)= x_4x_5 (x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5 x_0x_1.                             (4)
```

Write

```text
h_0=-x_0+x_1+x_2+x_3,
h_1= x_0-x_1+x_2+x_3,
h_2= x_0-x_1-x_2+x_3,
h_2'=-x_0+x_1-x_2+x_3.                                (5)
```

The exceptional kernel directions are

```text
Phi_1: N=x_2+x_3,  A_0=x_0+x_3,  C_0=x_0-x_2,
Phi_2: N=x_2+x_3,  A_1=x_1+x_3,  C_1=x_1-x_2.          (6)
```

The predecessor proves that every low kernel line is one of (6), and that
its generator misses the following local colour:

```text
N misses 2;       A_0 misses 0;       C_0 misses 1;
                  A_1 misses 1;       C_1 misses 0.     (7)
```

This note adds information only when the generator is supported on one of
the two remaining colours.

## 2. Quotient one-diagonal propagation

Let `D` be a vector space of dimension `d>=2`, let `A` be two-dimensional
with nondegenerate symmetric form `J`, and set `W=D direct-sum A`.  For
`y=(r(y),a(y))` define

```text
C(y,z,w)=r(y)J(a(z),a(w))+r(z)J(a(y),a(w))
                         +r(w)J(a(y),a(z)).              (8)
```

### Lemma 1 (one diagonal cannot survive on three embedded triples)

Let three linearly independent ordered triples in `W` be indexed by modes
`s,u,v` and colours `0,1,2`.  It is impossible that, for one colour `e`,

```text
C(y_(s,i),y_(u,j),y_(v,l))=0 unless i=j=l=e,
C(y_(s,e),y_(u,e),y_(v,e))!=0.                         (9)
```

### Proof

For `(i,j)!=(e,e)`, the map

```text
w |-> C(y_(s,i),y_(u,j),w) : W -> D                   (10)
```

kills the three-space spanned by the third triple.  Its rank is at most
`dim W-3=d-1`.  On the `D`-summand it is scalar multiplication by
`J(a(y_(s,i)),a(y_(u,j)))`.  A nonzero scalar would give rank `d`, so all
cross-colour pairings between distinct modes vanish.

The nonzero vector in (9) contains a nonzero same-colour pairing.  After
permuting modes, assume the pairing between the `s` and `u` vectors is
nonzero.  For either `l!=e`, the other two pairings in (8) vanish, and the
zero value in (9) forces `r(y_(v,l))=0`.  Both corresponding `A`-vectors
lie in the one-dimensional orthogonal complement of the nonzero
`a(y_(s,e))`.  Hence the two off-`e` vectors of the third triple are
dependent, a contradiction.

### Corollary 2 (residual-kernel propagation)

Let `Q subset R^*` be a `d`-dimensional residual-covector space with
`d>=2`, and put

```text
H=ann_R(Q).                                               (11)
```

Suppose contraction in one local mode leaves, on the other three modes,
exactly one nonzero diagonal cell after evaluation by every covector in
`Q`.  Then some other local plane meets `H` nontrivially.

Indeed, if all three planes were disjoint from `H`, their images in

```text
(R/H) direct-sum A
```

would be three-dimensional and Lemma 1 would apply.  Moreover, if the
surviving colour is `e`, every vector in the propagated intersection has
zero `e`-coefficient: double contraction annihilates the residual covector
of the nonzero `d_e` channel, while the right side of (1) is a nonzero
multiple of that coefficient.

## 3. The six exceptional contraction cases

Contract (4) once with the six exceptional directions, counting the common
line `N` once in each projection family.  Omitting the common factor
`x_4x_5`, the nonzero residual covectors and their common kernels are

```text
low direction       nonzero residual covectors       H=common kernel

Phi_1: N            h_0,h_1                          span{x_0+x_1,x_2-x_3}
Phi_1: A_0          h_2,h_1,x_1                      K(x_0-x_3)
Phi_1: C_0          h_2,h_0,x_1                      K(x_0+x_2)

Phi_2: N            h_0,h_1                          span{x_0+x_1,x_2-x_3}
Phi_2: A_1          h_2',h_0,x_0                     K(x_1-x_3)
Phi_2: C_1          h_2',h_1,x_0                     K(x_1+x_2).       (12)
```

The residual-covector ranks are respectively `2,3,3,2,3,3`.  If the low
generator is singleton-supported at colour `e`, all contractions except
the `d_e` target are zero.  Corollary 2 therefore proves that another local
plane meets the displayed `H`, in a vector whose local `e`-coefficient is
zero.

This is already a finite propagation rule.  The full target equations make
the companion colours sharper.

## 4. Four forced singleton companions

Put

```text
U_0=x_0-x_3,       V_1=x_0+x_2,
U_1=x_1-x_3,       V_0=x_1+x_2.                         (13)
```

Direct contraction of (4) gives the tensor identities

```text
i_(U_0)star(m_1)=i_(U_0)star(d_2),
i_(U_0)star(m_2)=i_(U_0)star(d_1),

i_(V_1)star(m_1)=i_(V_1)star(d_2),
i_(V_1)star(m_2)=i_(V_1)star(d_0),

i_(U_1)star(m_2)=i_(U_1)star(d_2),
i_(U_1)star(m_1)=i_(U_1)star(d_0),

i_(V_0)star(m_2)=i_(V_0)star(d_2),
i_(V_0)star(m_1)=i_(V_0)star(d_1).                     (14)
```

The mixed tensors vanish, while every diagonal target in (1) is nonzero.
Thus a local plane containing one of (13) contains it on the forced colour
line

```text
U_0: colour 0,       V_1: colour 1,
U_1: colour 1,       V_0: colour 0.                    (15)
```

Combining (12) and (15) gives four exact companion arrows:

```text
A_0 singleton at colour 1 or 2  -->  U_0 singleton at colour 0,
C_0 singleton at colour 0 or 2  -->  V_1 singleton at colour 1,
A_1 singleton at colour 0 or 2  -->  U_1 singleton at colour 1,
C_1 singleton at colour 1 or 2  -->  V_0 singleton at colour 0.   (16)
```

Every arrow goes to a different local mode.

## 5. The common-line companion plane

Every vector in the two-plane paired with `N` has the form

```text
q=s(x_0+x_1)+t(x_2-x_3)=(s,s,t,-t).                    (17)
```

Its contractions satisfy

```text
i_q star(d_0)=i_q star(d_1)
 =-(s+t)x_4x_5(x_0+x_1+x_2-x_3),

i_q star(d_2)=-2s x_4x_5(x_0+x_1).                     (18)
```

Equality of the first two target contractions in (18) forces the local
colour-0 and colour-1 coefficients of `q` to vanish separately.  Therefore
every nonzero propagated `q` is singleton-supported at colour `2`.
The `d_2` target is nonzero, so (18) also forces

```text
s!=0.                                                    (19)
```

Consequently the two common-line arrows are

```text
Phi_1: N singleton at colour 0 or 1 --> q singleton at colour 2,
Phi_2: N singleton at colour 0 or 1 --> q singleton at colour 2,  (20)
```

where `q` is as in (17)--(19) and lies in a different local mode.

## 6. Exact return cycles

The companion incidences themselves have one surviving diagonal, so the
same argument can be applied again.  Their residual kernels are

```text
U_0 colour 0  --> K A_0,
V_1 colour 1  --> K C_0,
U_1 colour 1  --> K A_1,
V_0 colour 0  --> K C_1.                               (21)
```

Thus each arrow in (16) closes an allowed two-cycle.  On the return arrow,
the propagated vector misses the companion colour, exactly as required by
(7).  The return mode may be the original mode, so (21) is not a
contradiction and does not force a third incidence.

For `q` in (17), put

```text
L=-x_0-x_1-x_2+x_3.
```

The residual covectors are

```text
m_1: sL-2t x_1,             m_2: sL-2t x_0,
d_0=d_1: (s+t)L,            d_2: -2s(x_0+x_1).          (22)
```

If `t!=0`, they span a three-space with common kernel `K N`, so the second
arrow returns to the original common exceptional line.  If `t=0`, they
span a two-space with common kernel

```text
span{N,x_0-x_1}.                                         (23)
```

This is the only wider return boundary.  It contains `N`, so the original
mode can again satisfy the propagated incidence.  The propagation graph
therefore closes but does not exclude any of its cycles.

## 7. Exact scope and replay

```text
all six exceptional family-line contraction cases:       INCLUDED;
singleton-supported exceptional low:                      ASSUMED;
explicit companion line/plane in another mode:            PROVED;
forced companion singleton colour:                        PROVED;
exact two-cycle / wider boundary classification:           PROVED;
existence or exclusion of those cycles:                    OPEN;
support-two exceptional lows:                              OPEN HERE;
unrestricted P_6 -> Delta_3:                              UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.   (24)
```

Replay the exact identities with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_singleton_exceptional_companion_propagation.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_singleton_exceptional_companion_propagation.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_singleton_exceptional_companion_propagation.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_singleton_exceptional_companion_propagation.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_singleton_exceptional_companion_propagation.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_singleton_exceptional_companion_propagation.py
```

The primary verifier reconstructs every contraction, residual rank, common
kernel, forced-colour identity, and return cycle over exact symbolic
arithmetic.  The independent audit imports neither the primary verifier nor
SymPy: it rebuilds contractions from square-free quadratic coefficient
dictionaries and checks all ranks and kernels by rational row reduction.
The scripts replay displayed algebra; the written characteristic-zero
argument proves the propagation theorem.
