# Residual-null incidence is sharp on the canonical P7 profile

## Status

**Exact structural sharpness theorem and fixed rational countermodel.**  Work
over a characteristic-zero field.  Combine only the following data:

1. the canonical five-root blocker profile

   ```text
   012, 01,01, 02,02, 12,12;
   ```

2. the three nonzero pure `P_5` root permanents; and
3. the residual-null conclusion from
   [`P7_RESIDUAL_NULL_POLAR_SELECTOR_H0_THEOREM.md`](P7_RESIDUAL_NULL_POLAR_SELECTOR_H0_THEOREM.md):
   at least three residual polar planes contain a target coordinate covector.

At this level the lower bound three is sharp.  The three incidences need not
use different target colours, need not meet three different double-blocker
types, and need not be aligned with the canonical root-row plane.  More
strongly, any prescribed set of residual-null boundary blockers and any
prescribed coordinate label at each of them can be realized while preserving
the canonical blocker types, local rank three, and all three pure
coefficients.

This is not a factorized `P_7 -> Delta_3` construction.  The mixed-word
identity is neither checked nor claimed.  The theorem proves that no stronger
incidence conclusion follows from the stated canonical and pure data alone.
In particular, the example does **not** satisfy the stronger per-colour
kernel Hall quotas obeyed by an actual permanent restriction.  The later
[`ARBITRARY_PERMANENT_FOUR_MODE_ROW_PAIR_INCIDENCE_THEOREM.md`](ARBITRARY_PERMANENT_FOUR_MODE_ROW_PAIR_INCIDENCE_THEOREM.md)
uses those quotas and the full polar rank to improve the factorized lower
bound from three blockers to four.

## 1. Root and residual planes are different objects

Let `V_w=K^3` at every blocker.  Write

```text
T_w=span{H_(i,w):0<=i<5} subset V_w^*                (1)
```

for the root-row span, and

```text
A_w=span{a_w,b_w} subset V_w^*,
K_w=ker a_w intersection ker b_w                     (2)
```

for the residual polar plane and its common null space.  The canonical
profile specifies the seven `T_w`:

```text
T_t=span{e_0^*,e_1^*,e_2^*},
T_(01)=span{e_0^*,e_1^*},
T_(02)=span{e_0^*,e_2^*},
T_(12)=span{e_1^*,e_2^*}.                             (3)
```

It does not identify `A_w` with `T_w`.  If `A_w` has rank two, write

```text
A_w=k_w^perp                                         (4)
```

for a nonzero normal `k_w in V_w`, unique projectively.  Then

```text
e_c^* in A_w iff k_w[c]=0.                            (5)
```

Thus `K_w` is non-torus exactly when one coordinate of `k_w` is zero.  A
normal with exactly one zero gives exactly one coordinate incidence; a normal
with all coordinates nonzero gives a torus-capable null line.

## 2. Arbitrary incidence prescription

Let `B` be the seven blockers, choose any subset `N subset B`, and choose any
map

```text
gamma:N->{0,1,2}.                                    (6)
```

### Theorem 1 (arbitrary residual-null incidence realization)

Assume the root rows have the canonical spans (3) and their three pure
`P_5` permanents are nonzero.  There are ordered residual rows `(a_w,b_w)`
such that:

1. if `w in N`, then `A_w` contains exactly `e_(gamma(w))^*` among the three
   coordinate covectors;
2. if `w notin N`, then `A_w` contains no coordinate covector;
3. every double blocker remains locally concise:

   ```text
   T_w+A_w=V_w^*;
   ```

4. for each colour `c`, if `{u_c,v_c}` is the double-blocker pair missing
   `c`, then

   ```text
   D_(u_c v_c)^(cc)
    =a_(u_c)[c] b_(v_c)[c]+b_(u_c)[c] a_(v_c)[c]
    !=0.                                               (7)
   ```

Consequently the full pure colour coefficient

```text
P_c D_(u_c v_c)^(cc)                                 (8)
```

is nonzero for all three colours.

Proof.  For `w in N`, choose a normal `k_w` whose `gamma(w)` coordinate is
zero and whose other two coordinates are nonzero.  For `w notin N`, choose
all three coordinates of `k_w` nonzero.  Equations (4)--(5) give assertions
1--2.

Every chosen normal has at least two nonzero coordinates.  It is therefore
not proportional to the missing coordinate normal of any canonical double
plane in (3).  Two distinct planes in a three-space span the full space, so
assertion 3 follows.

For every coordinate `c`, evaluation at `e_c` is a nonzero functional on
`A_w`: it would vanish on all of `A_w` only if `k_w` were proportional to
`e_c`, which never occurs.  After choosing an ordered basis `(a_w,b_w)` of
`A_w`, its coordinate evaluation is the nonzero column

```text
r_w^c=(a_w[c],b_w[c])^T in K^2.                       (9)
```

Changing the ordered basis by `GL_2` moves `r_w^c` through every nonzero
column of `K^2`.  The three missing-colour blocker pairs are disjoint.
Choose their bases independently so that

```text
(r_(u_c)^c)^T [[0,1],[1,0]] r_(v_c)^c !=0.            (10)
```

This is (7).  The residual basis choices do not change the root rows or their
permanents, proving (8) and the theorem.

### Corollary 2 (the three-boundary law is sharp)

Take `|N|=3`.  Theorem 1 realizes exactly three non-torus residual null
spaces.  The labels `gamma(w)` may all be equal, and the three blockers may
be the triple blocker together with both copies of one double type.  Hence
the canonical/pure data force none of:

- one residual-null incidence of each target colour;
- one incidence in each missing-colour pair;
- a balanced multiplicity pattern; or
- equality or functorial alignment between `A_w` and `T_w`.

## 3. A clustered exact rational countermodel

Label the blockers

```text
t,u01,v01,u02,v02,u12,v12.                            (11)
```

For root `i`, put `n=i+1` and take the fixed root-row covectors

```text
H_(i,t)   =(1,n,n^2),
H_(i,u01) =(1,n,0),       H_(i,v01)=(n,1,0),
H_(i,u02) =(1,0,n),       H_(i,v02)=(n,0,1),
H_(i,u12) =(0,1,n),       H_(i,v12)=(0,n,1).           (12)
```

Their blocker spans are exactly (3).  For each root, its seven rows span
`K^3`.  The colour-`c` pure matrix uses the triple blocker and the four
double blockers containing `c`.  Its permanent is respectively

```text
P_0=1020,             P_1=2700,             P_2=9116. (13)
```

Put

```text
g=(1,1,1),                h=(1,2,3).                  (14)
```

Choose residual rows

```text
(a_t,b_t)       =(e_0^*,g),
(a_u01,b_u01)   =(e_0^*,g),
(a_v01,b_v01)   =(g,e_0^*),
(a_w,b_w)       =(g,h)  for w in {u02,v02,u12,v12}.   (15)
```

The first three polar planes have normal `(0,-1,1)`, so they contain exactly
`e_0^*`; their null line is non-torus.  The last four planes have normal
`(1,-2,1)`, whose null line is a torus line and whose polar plane contains no
coordinate covector.  Thus the incidence set is exactly

```text
N={t,u01,v01},             gamma identically 0.       (16)
```

The three pure residual factors are

```text
D_(u01 v01)^(22)=1,
D_(u02 v02)^(11)=4,
D_(u12 v12)^(00)=2.                                  (17)
```

Equations (13) and (17) make all three pure `P_7` coefficients nonzero.  The
example also satisfies local rank three at every blocker.

## Scope wall

Proved here:

- arbitrary placement and colouring of residual-null coordinate incidences
  alongside the canonical root-row profile;
- compatibility with local blocker concision;
- compatibility with all three nonzero pure `P_5` permanents and the three
  nonzero residual pure-pair factors;
- an exact clustered example attaining the lower bound three with all three
  incidence labels equal.

Not proved or claimed:

- the mixed-word equations in the full factorized identity;
- the two-incidences-per-colour kernel Hall quotas of that identity;
- a `P_7 -> Delta_3` restriction;
- simultaneous principal-hafnian realization of additional deletion data;
- any conclusion for the `h!=0` branch;
- the Krenn--Gu conjecture.

The strict logical conclusion is therefore:

```text
canonical profile + three pure permanents + residual-null theorem
    => at least three coordinate incidences, sharply;
    !=> any stronger placement or colour multiplicity law.           (18)

full factorized P7 identity
    => stronger per-colour quotas and at least four incidence modes.  (19)
```

## Replay

```powershell
uv run --with sympy python verify_p7_residual_null_incidence_canonical_profile_sharpness.py
python audit_p7_residual_null_incidence_canonical_profile_sharpness.py
uv run --with sympy --with ruff python -m ruff check verify_p7_residual_null_incidence_canonical_profile_sharpness.py audit_p7_residual_null_incidence_canonical_profile_sharpness.py
python -m py_compile verify_p7_residual_null_incidence_canonical_profile_sharpness.py audit_p7_residual_null_incidence_canonical_profile_sharpness.py
```

The verifier checks the fixed rational construction, its exact blocker
planes, root concision, the three permanents, the polar-plane incidence
labels, the torus/non-torus null lines, local rank, and the three values in
(17).  It performs no support or parameter search.
The independent no-import audit reconstructs the row ranks, three fixed
five-by-five permanents, polar normals, and residual pair values using exact
integer arithmetic and separate routines.
