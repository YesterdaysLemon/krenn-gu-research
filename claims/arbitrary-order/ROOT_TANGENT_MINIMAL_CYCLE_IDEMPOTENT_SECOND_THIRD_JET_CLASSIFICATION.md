# Idempotent second/third-jet classification of minimal tangent cycles

## Status

**Exact characteristic-zero low-jet classification and full-root
obstruction.**  Suppose projectively constant root--blocker first derivatives
are repaired by a minimal cycle of root--root tangent companions.  The two
incident complementary-cofactor quotient lines form a basis at every root,
and the root--root companion support on the restricted slice is exactly this
cycle.  In particular, no off-cycle tangent--tangent block that is invisible
to the first jet becomes effective in a higher selected derivative.

The mixed second jet forces every shared edge class to be a projective fixed
point of coordinatewise squaring.  There are exactly three:

```text
A=[1:0],                 B=[0:1],                 C=[1:1].            (1)
```

The mixed third jet on three consecutive roots then forbids `C`.  Hence the
only minimal-cycle topology surviving these selected second and third jets
is an **even cycle whose edge classes alternate `A,B,A,B,...`**.

This is stronger than the earlier generic-cycle obstruction: it classifies
its exceptional directions instead of assuming the edge parameters avoid
`0,1,infinity`.  The alternating binary cycle has an explicit symmetric
formal edge-block realization of every first jet and of all selected tests
used in the proof, so the conclusion is sharp for this jet subsystem.

The selected low-jet survivor is nevertheless impossible for the complete
restricted GHZ jet.  Varying every root in the `A` direction selects the
`A` perfect matching, while varying every root in the `B` direction selects
the `B` perfect matching.  Both matchings delete exactly the same root set,
so both graph derivatives are scalar multiples of one common complementary
principal hafnian.  The two GHZ derivatives are nonzero independent pure
tensors.  This common-cofactor collision excludes the entire minimal-cycle
topology under the stated hypotheses.

The complementary classes in the sharp low-jet model are still formal.  No
simultaneous principal-hafnian realization, nonminimal companion exclusion,
`P_7` exclusion, or global Krenn--Gu proof is claimed.

## 1. Normalized tangent quotient

Normalize every fully supported root to

```text
x=(1,1,1),                     ell=e_0^*.                         (2)
```

On the tangent plane `S=ker ell`, the logarithmic GHZ derivative modulo the
scalar diagonal is

```text
F(y)=(y_1,y_2) in Q=K^2.                                      (3)
```

Let the cycle edge `e_i={i,i+1}` carry a nonzero shared quotient class

```text
q_i=[u_i:v_i] in P(Q).                                        (4)
```

At root `i`, the two incident classes `q_(i-1),q_i` are independent.  Thus a
unique tangent direction can isolate either incident class.  For (4), take

```text
y(q_i)=(0,u_i,v_i),              F(y(q_i))=(u_i,v_i).           (5)
```

The minimality hypothesis says that on `y(q_i)` every effective companion
other than `e_i` vanishes.  Projective root--blocker derivatives vanish on
`S` as well.

## 2. Second jets force Hadamard idempotents

Vary the two endpoints of `e_i` in the direction (5).  Separate companion
matchings vanish because the other incident covector is zero at each
endpoint.  A tangent--tangent correction on `e_i` can only multiply the same
complementary cofactor class `q_i`.  Therefore the graph mixed second jet,
modulo the scalar diagonal, lies on the line

```text
K q_i.                                                           (6)
```

The GHZ mixed Hessian has quotient class

```text
q_i^[2]=(u_i^2,v_i^2).                                         (7)
```

### Theorem 1 (projective idempotent law)

Second-jet compatibility on `e_i` implies

```text
q_i^[2] wedge q_i=0,
u_i v_i(v_i-u_i)=0.                                             (8)
```

Consequently `q_i` is one of the three classes in (1).

Proof.  Equality of (6) and (7) requires the two vectors to be dependent.
Their determinant is `u_i v_i^2-v_i u_i^2`, which factors as (8).  A nonzero
projective point satisfying (8) is exactly `A`, `B`, or `C`.

This argument allows the most general tangent--tangent correction on the
same edge.  It uses only the fact that the correction retains the edge's
already fixed complementary-cofactor line.

## 3. A three-root matching pinch eliminates C

Take consecutive edges

```text
e_i={i,i+1},                  e_(i+1)={i+1,i+2}                  (9)
```

with distinct classes `q,r`; distinctness is forced because the two classes
at the middle root form a basis.  Vary roots `i,i+1` in direction `y(q)` and
root `i+2` in direction `y(r)`.

Only the path

```text
i -- i+1 -- i+2                                                (10)
```

remains effective.  It has no matching saturating its three vertices.  Thus
every graph matching term in this restricted third derivative vanishes.
The GHZ derivative is

```text
y(q)^[2] Hadamard y(r)
  =(0,u^2 a,v^2 b),             r=[a:b].                         (11)
```

It must therefore be zero.

### Theorem 2 (alternating-binary cycle law)

Among distinct projective idempotents, equation (11) vanishes only for the
ordered adjacent pairs

```text
(A,B),                         (B,A).                             (12)
```

Hence `C` occurs on no edge.  Every pair of adjacent edge classes alternates
between `A` and `B`, and the cycle length is even.

Proof.  The four pairs involving `C` give respectively

```text
A^[2] Hadamard C=A,            B^[2] Hadamard C=B,
C^[2] Hadamard A=A,            C^[2] Hadamard B=B,                (13)
```

all nonzero.  In contrast `A Hadamard B=B Hadamard A=0`.  This proves
(12).  Alternation around a closed cycle is possible only at even length.

The graph-side vanishing is termwise and uses no complementary-hafnian
calculation: an odd effective path cannot cover its three varied roots.

## 4. Sharp formal alternating model

Let

```text
s=e_1^*-e_0^*,                 t=e_2^*-e_0^*.                    (14)
```

Then `s(x)=t(x)=0`, and on `S` they are the two coordinates in (3).  On an
`A` edge use the symmetric bilinear block

```text
M_A=s tensor ell+ell tensor s+s tensor s,                         (15)
```

and on a `B` edge use

```text
M_B=t tensor ell+ell tensor t+t tensor t.                         (16)
```

For `p in {s,t}` and `M_p` equal to (15) or (16),

```text
M_p(-,x)=p,                 M_p(x,-)=p,
M_p(y_p,y_p)=1,                                                 (17)
```

where `y_s=(0,1,0)` and `y_t=(0,0,1)`.  Give the complementary cofactor of
an `A` edge quotient class `A`, and similarly for `B`.  Around any even
alternating cycle:

1. the two incident first-jet classes are `A,B`, hence reproduce `F`;
2. the selected second jet is `A^[2]=A` or `B^[2]=B`, reproduced by the last
   term of (15) or (16); and
3. every selected consecutive third jet has target product `A Hadamard B=0`,
   matching the unsaturable path.

This is a formal jet realization, not a graph witness.  In particular, it
does not construct blocker-edge data whose complementary principal hafnians
are the prescribed alternating classes, and it does not test nonselected
higher jets.

## 5. The full-root cofactor collision excludes the survivor

Let the alternating cycle have length `2k`, let `R` be its complete root
set, and assume at least one unvaried three-mode port remains.  The `A` edges
and the `B` edges are the two perfect matchings

```text
P_A={{0,1},{2,3},...,{2k-2,2k-1}},
P_B={{1,2},{3,4},...,{2k-1,0}}.                    (18)
```

Vary every root in direction `y_A=(0,1,0)`.  At each root this direction
annihilates the incident `B` companion and isolates the incident `A`
companion.  Projectively constant root--blocker terms vanish on tangent
directions, and the minimality hypothesis kills every additional selected
companion.  Hence `P_A` is the unique effective root matching.  The same
argument with `y_B=(0,0,1)` makes `P_B` the unique effective root matching.

Both perfect matchings delete the same set `R`.  If

```text
C_R=haf G[V\R]                                                   (19)
```

is the remaining principal-hafnian tensor, the two graph derivatives
therefore lie on the common line `K C_R`; their edge-block evaluations only
change the two scalar multipliers.  This remains true for arbitrary
tangent--tangent corrections on the cycle edges.

On the normalized GHZ side, if `m>=1` ports remain, the same two derivatives
are nonzero scalar multiples of

```text
e_1 tensor ... tensor e_1,       e_2 tensor ... tensor e_2,        (20)
```

with `m` factors.  These pure tensors are linearly independent.  Thus they
cannot both lie on `K C_R`; if `C_R=0`, neither nonzero target can be
matched, and if `C_R!=0`, at most one independent target line can be
matched.

### Theorem 3 (full-root common-cofactor obstruction)

No even alternating `A/B` minimal cycle realizes the complete restricted
GHZ jet when at least one unvaried three-mode port remains.  Combined with
Theorems 1 and 2, no minimal tangent-companion cycle satisfying the opening
hypotheses realizes that jet.

The obstruction is structural: it compares two exact derivatives and the
principal deletion set they share.  It performs no graph, support, or
colour-word enumeration.

## 6. Consequence for the coordinate-boundary program

The projectively constant companion route is no longer a continuous family
at minimal degree.  Exact second/third jets reduce it to one discrete
topology:

```text
minimal tangent cycle
  -> Hadamard-idempotent edge classes
  -> even alternating binary cycle
  -> full-root common-cofactor collision.                           (21)
```

A surviving companion construction must therefore do at least one of the
following:

1. add an effective companion outside the minimal cycle on at least one of
   the two uniform tangent selections;
2. introduce a third effective complementary-cofactor line;
3. make the root--blocker layer nonprojective on the tangent plane; or
4. leave the minimal-cycle boundary in another explicitly identifiable way.

No support or colour-word enumeration is involved.

## Scope wall

```text
generic minimal-cycle edge classes:          EXCLUDED at second jet;
exceptional second-jet classes:              A, B, C only;
C on a minimal cycle:                        EXCLUDED at third jet;
selected low-jet survivor:                    EVEN ALTERNATING A/B;
selected first/second/third jet subsystem:    FORMALLY REALIZED;
alternating survivor in the full-root jet:    EXCLUDED;
complete minimal-cycle topology:              EXCLUDED;
nonminimal/additional companion systems:      UNKNOWN;
full coordinate-monomial P7 branch:          UNKNOWN;
global Krenn--Gu conjecture:                 UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_root_tangent_minimal_cycle_idempotent_second_third_jet_classification.py
python claims/arbitrary-order/audit_root_tangent_minimal_cycle_idempotent_second_third_jet_classification.py
python -m py_compile claims/arbitrary-order/verify_root_tangent_minimal_cycle_idempotent_second_third_jet_classification.py claims/arbitrary-order/audit_root_tangent_minimal_cycle_idempotent_second_third_jet_classification.py
uv run --with ruff ruff check claims/arbitrary-order/verify_root_tangent_minimal_cycle_idempotent_second_third_jet_classification.py claims/arbitrary-order/audit_root_tangent_minimal_cycle_idempotent_second_third_jet_classification.py
```

The primary verifier checks the generic idempotent factor, all three fixed
classes, the third-jet products, the symmetric block identities, the two
distinct perfect matchings with their common deletion set, and independence
of the two GHZ target tensors.  The independent no-import audit repeats the
claims with exact integer vectors, matrices, and edge sets.  Both are fixed
symbolic replays, not graph or support searches.
