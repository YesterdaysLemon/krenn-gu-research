# Idempotent second/third-jet classification of minimal tangent cycles

## Status

**Exact arbitrary-order characteristic-zero classification and sharp formal
boundary.**  Suppose projectively constant root--blocker first derivatives
are repaired by a minimal cycle of root--root tangent companions.  The two
incident complementary-cofactor quotient lines form a basis at every root,
and no additional companion class survives on the tangent directions that
isolate one cycle edge.

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

The complementary classes are still formal.  No simultaneous principal-
hafnian realization, full mixed tensor identity, `P_7` exclusion, or global
Krenn--Gu proof is claimed.

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

## 5. Consequence for the coordinate-boundary program

The projectively constant companion route is no longer a continuous family
at minimal degree.  Exact second/third jets reduce it to one discrete
topology:

```text
minimal tangent cycle
  -> Hadamard-idempotent edge classes
  -> even alternating binary cycle.                                (18)
```

A genuine next obstruction must therefore do at least one of the following:

1. exclude simultaneous principal-hafnian realization of the alternating
   `A/B` cofactor classes;
2. use a nonselected fourth or higher root jet;
3. prove that a third effective companion class is unavoidable; or
4. leave the projectively constant root--blocker boundary.

No support or colour-word enumeration is involved.

## Scope wall

```text
generic minimal-cycle edge classes:          EXCLUDED at second jet;
exceptional second-jet classes:              A, B, C only;
C on a minimal cycle:                        EXCLUDED at third jet;
surviving minimal-cycle topology:            EVEN ALTERNATING A/B;
selected first/second/third jet subsystem:    FORMALLY REALIZED;
principal-hafnian cofactor realization:      UNKNOWN;
full coordinate-monomial P7 branch:          UNKNOWN;
global Krenn--Gu conjecture:                 UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_root_tangent_minimal_cycle_idempotent_second_third_jet_classification.py
python audit_root_tangent_minimal_cycle_idempotent_second_third_jet_classification.py
python -m py_compile verify_root_tangent_minimal_cycle_idempotent_second_third_jet_classification.py audit_root_tangent_minimal_cycle_idempotent_second_third_jet_classification.py
uv run --with ruff ruff check verify_root_tangent_minimal_cycle_idempotent_second_third_jet_classification.py audit_root_tangent_minimal_cycle_idempotent_second_third_jet_classification.py
```

The primary verifier checks the generic idempotent factor, all three fixed
classes, the third-jet products, and the symmetric block identities.  The
independent no-import audit repeats them with exact integer vectors and
matrices.  Both are fixed symbolic replays, not graph or support searches.
