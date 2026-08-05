# Residual-depth loop-hafnian cumulants and the two-port discriminant

## Status

**Exact arbitrary-order characteristic-zero theorem and complete response
criterion.**  The residual-hafnian common-cofactor theorem is correct, but
its quadratic Gram layer is only one coefficient of a stronger object.
Retain the responses for every principal subset of the residual vertices and
divide each of them by the common port-only matching family.  The resulting
residual-depth generating series is the exponential of one quadratic-plus-
linear form.  Equivalently:

```text
its logarithm has residual degree at most two;
its singleton coefficients are port-linear;
its pair coefficients beyond singleton products are scalars.       (1)
```

Thus the complete normalized residual tower is a loop-hafnian family over
the vertex-exclusive port algebra.  This is a necessary-and-sufficient
representability theorem when all residual depths are supplied.

For two residual vertices it gives the division-free discriminant

```text
M Z_01-Y_0 Y_1=h M^2.                                  (2)
```

Here `M` is the residual-absent response, `Y_i` has only residual vertex
`q_i` present, `Z_01` has both present, and `h` is the residual edge.  The
usual corrected two-port formula is the degree-two coefficient of (2), not
an independent factorization assumption.  Every higher port coefficient of
(2) is a synchronized cross-depth obstruction.

This theorem does not manufacture the missing principal deletion responses
from a top `P_7` equation.  It proves exactly what must hold if those depths
are legally exposed.  The current top-only, projective, and `B=0` controls
remain valid.  No `P_5`, `P_6`, `P_7`, or global Krenn--Gu nonrestriction is
claimed; the global conjecture remains **UNRESOLVED**.

No graph, support, colour-word, matching-family, or parameter enumeration is
used.

## 1. The two vertex-exclusive algebras

Let `U` be a finite scalar port set and `Q` a finite residual set.  Work over
a characteristic-zero field `K` in

```text
A=K[x_u,y_p:u in U,p in Q]/(x_u^2,y_p^2).             (3)
```

Write

```text
B_uv  for a port--port edge,
R_pu  for a residual--port incidence,
A_pq  for a residual--residual edge.                  (4)
```

Put

```text
Q_B=sum_(u<v) B_uv x_u x_v,
Q_R=sum_(p,u) R_pu y_p x_u,
Q_A=sum_(p<q) A_pq y_p y_q.                           (5)
```

The full matching response is

```text
E(x,y)=exp(Q_B+Q_R+Q_A).                              (6)
```

For each `T subset Q`, define the response with exactly the residual
vertices in `T` present by

```text
Z_T(x)=[y_T]E(x,y).                                   (7)
```

Thus `Z_T` contains the matching responses on `T union S` for every port
subset `S`.  In particular,

```text
M=Z_empty=exp(Q_B),                                   (8)
```

and `M` is a unit because its constant coefficient is one.  Define

```text
Phi_T=M^(-1) Z_T,
Phi(y)=sum_(T subset Q) Phi_T y_T.                    (9)
```

All inverses, exponentials, and logarithms are finite polynomials in the
nilpotent square-zero ideals.

## 2. Residual-depth logarithmic flatness

### Theorem 1 (normalized residual-depth exponential)

```text
Phi(y)=exp(Q_A+Q_R),
log Phi=Q_A+Q_R.                                     (10)
```

Proof.  The three quadrics in (5) commute, so

```text
E=exp(Q_B) exp(Q_A+Q_R)=M exp(Q_A+Q_R).
```

Take every residual coefficient and multiply by `M^(-1)`.  This gives the
first identity in (10).  The second follows because finite `exp` and `log`
are inverse in the nilpotent ideal.

Consequently the normalized residual cumulants satisfy

```text
[y_p] log Phi=L_p=sum_u R_pu x_u,
[y_p y_q] log Phi=A_pq,
[y_T] log Phi=0                         for |T|>=3.   (11)
```

The singleton cumulant is port-linear, the residual pair cumulant is a
port-independent scalar, and every higher residual cumulant vanishes.

This is stronger than checking a separate two-port Gram factorization at
each depth.  All depths use one incidence matrix `R`, one residual matrix
`A`, and one port moment family `M`.

### Corollary 2 (first residual-curvature equation)

For distinct residual vertices `p,q,r`,

```text
Phi_pqr
 -Phi_pq Phi_r-Phi_pr Phi_q-Phi_qr Phi_p
 +2 Phi_p Phi_q Phi_r=0.                              (12)
```

This is the vanishing third residual cumulant.  It couples four different
principal residual depths and is invisible in a fixed top response.

## 3. Loop-hafnian reconstruction

For `p in Q`, put

```text
L_p=Phi_{p}.                                         (13)
```

For distinct `p,q`, put

```text
C_pq=Phi_{pq}-Phi_p Phi_q.                           (14)
```

Theorem 1 says `L_p` is linear in the port variables and `C_pq=A_pq` is a
scalar.

### Theorem 3 (residual loop-hafnian formula)

For every `T subset Q`,

```text
Phi_T
 =sum_(D a partial matching of T)
    product_({p,q} in D) C_pq
    product_(r in T minus vertices(D)) L_r.           (15)
```

In other words, `Phi_T` is the loop hafnian of the hollow symmetric matrix
`C[T]` with loop weights `(L_p)_(p in T)`, computed in the square-zero port
algebra.

Proof.  Extract `y_T` from `exp(Q_A+Q_R)`.  Every residual vertex is used
either once in an internal residual edge, or once in a residual--port term.
The internal edges form a partial matching `D`; every unmatched residual
vertex supplies its loop weight `L_r`.  Conversely each term in (15) gives
one such selection.  Square-zero multiplication kills assignments that use
one physical port twice and sums the surviving port bijections with
permanent signs, exactly as required.

### Theorem 4 (complete residual-tower criterion)

A family `(M,(Z_T)_(T subset Q))` is the complete scalar response tower of a
loopless port/residual graph if and only if:

1. `M` has constant term one and `log M` is a port quadratic;
2. in `Phi_T=M^(-1)Z_T`, every `L_p=Phi_p` is port-linear;
3. every `C_pq=Phi_pq-Phi_p Phi_q` is a scalar; and
4. all `Phi_T` obey (15), equivalently all residual cumulants of order at
   least three vanish.

When these conditions hold, the graph is reconstructed by

```text
B_uv=[x_u x_v]log M,
R_pu=[x_u]L_p,
A_pq=C_pq.                                           (16)
```

Necessity is Theorems 1 and 3.  Conversely, conditions 1--4 give
`M=exp(Q_B)` and `Phi=exp(Q_A+Q_R)`; hence
`sum_T Z_T y_T=M Phi=E`, which is the complete matching response of (16).

Thus (11)--(15) are not merely necessary equations.  They are the strongest
possible isolated all-depth response test: after they hold, there is no
additional scalar principal-hafnian representability condition.

## 4. The common-cofactor theorem is the quadratic shadow

Fix an even residual set `Q` and inspect the coefficient of a port pair
`{u,v}` in `Phi_Q`.  In (15), exactly two residual vertices `p,q` use the
ports while the others match internally.  Therefore

```text
[x_u x_v]Phi_Q
 =sum_(p<q in Q) haf(A[Q minus {p,q}])
    (R_pu R_qv+R_pv R_qu)
 =R_u^T C(A)R_v.                                    (17)
```

Multiplying by `M` restores the direct port contribution
`haf(A)B_uv`.  Hence

```text
H_uv=haf(A)B_uv+R_u^T C(A)R_v,                       (18)
```

which is exactly the arbitrary-order residual-hafnian common-cofactor
decomposition.  The matching proof and the residual-depth logarithmic proof
agree, so the existing decomposition is confirmed rather than weakened.

The known full-rank `haf(A)=0` family shows that the quadratic rank bound in
(18) is sharp.  The new information starts only when several `Z_T` are
retained and equations (12) or (15) can be tested.

## 5. The two-residual discriminant

Take `Q={q_0,q_1}` and write

```text
Y_0=Z_{q_0},        Y_1=Z_{q_1},
Z=Z_{q_0,q_1},      h=A_(q_0,q_1).                   (19)
```

Theorem 1 gives

```text
Y_0=M L_0,
Y_1=M L_1,
Z=M(h+L_0 L_1).                                     (20)
```

### Theorem 5 (two-port response discriminant)

```text
M Z-Y_0 Y_1=h M^2.                                  (21)
```

This identity is division-free and uses four legal principal residual
depths of one common graph.

Let

```text
M=sum_S m_S x_S,
Y_i=sum_S y_(i,S) x_S,
Z=sum_S z_S x_S,                                    (22)
```

and, for even `S`, define

```text
D_S=sum_(T subset S) m_T z_(S minus T)
    -sum_(T subset S) y_(0,T)y_(1,S minus T).         (23)
```

If `|S|=2d`, then

```text
D_S=2^d h m_S.                                       (24)
```

Indeed `M^2=exp(2Q_B)`.  Every matching of `S` has `d` edges and each edge
may be selected from either copy of `M`, giving the factor `2^d`.

At `|S|=2`, equation (24) is the usual two-port cofactor formula

```text
z_uv=h m_uv+y_(0,u)y_(1,v)+y_(0,v)y_(1,u).           (25)
```

At every higher even depth it supplies a new synchronized insertion
identity involving the odd one-residual responses.

Whenever `m_S!=0`, the empty residual edge is recovered without using the
empty coefficient:

```text
h=D_S/(2^d m_S).                                     (26)
```

For two even sets `S,T`, eliminate `h` division-free:

```text
2^(|T|/2) m_T D_S-2^(|S|/2) m_S D_T=0.              (27)
```

These minors are exact observable cross-depth obstructions.  If every
nonempty `m_S` vanishes, (24) cannot recover `h`; the honest `B=0` free-`h`
family proves this escape is sharp.

## 6. Consequences for the active branches

1. **General residual order.**  The common-cofactor decomposition is valid.
   The strongest complete refinement is the loop-hafnian tower (15), or
   equivalently residual-logarithmic flatness (11).  A quadratic rank test
   alone cannot see this information.
2. **Two-residual `P_7` cell.**  If `M,Y_0,Y_1,Z` are legally exposed on one
   blocker chart, (21)--(27) synchronize the direct layer and both residual
   rows exactly.  Any nonzero port moment recovers `h`.
3. **Current observability boundary.**  A top `P_7` equation exposes `Z`,
   not the three companion families.  Root singleton jets concern different
   physical edges from the blocker one-residual responses `Y_i`.  Theorem 5
   does not identify them.
4. **Canonical null fan.**  Conditional top selectors force the canonical
   `m_4,m_6` to vanish.  The direct pair layer or a noncanonical moment can
   still feed (26); the `B=0` common-block control shows no such moment is
   forced by pure/common-block data alone.
5. **Three or more residual vertices.**  Equation (12) is the first new
   residual-depth obstruction.  It becomes usable only after four compatible
   principal residual subsets are exposed from the same witness.
6. **`P_5/P_6/P_7` and blocker surplus.**  No unconditional branch closes
   merely from (15).  The exact next selector problem is now narrower: expose
   enough residual deletion depths to test one nonzero coefficient of (12)
   or (21), rather than seek another top-only rank drop.

## Literature interface

The square-zero exponential is the algebraic Wick/Isserlis mechanism behind
hafnians and Gaussian boson sampling; see Hamilton et al.,
[*Gaussian Boson Sampling*](https://arxiv.org/abs/1612.01199).  Gaussian
moment varieties motivate treating the complete response as one algebraic
image rather than unrelated moments; see Amendola, Faugere, and Sturmfels,
[*Moment Varieties of Gaussian Mixtures*](https://arxiv.org/abs/1510.04654).
Loop hafnians encode Gaussian moments with singleton contributions; a recent
moment/cumulant treatment is Cardin and Quesada,
[*Photon-number moments and cumulants of Gaussian states*](https://doi.org/10.22331/q-2024-11-13-1521).
Here the loop weights live in a vertex-exclusive port algebra, which is why
their products produce permanental incidence compounds rather than ordinary
scalar Gaussian moments.

Theorem 1 is also a bosonic connection-flatness statement: `M` removes the
port-only background, and the logarithm of the normalized residual tower has
zero curvature in every residual order above two.  This terminology is an
organizing translation; equations (10)--(15), not the analogy, are the
proved content.

## Scope wall

```text
arbitrary-order common-cofactor decomposition:       CONFIRMED;
normalized all-residual-depth exponential:           PROVED;
residual logarithm quadratic/linear form:             PROVED;
loop-hafnian reconstruction at every residual depth: PROVED;
complete isolated scalar tower criterion:             PROVED;
two-residual discriminant MZ-Y0Y1=hM^2:              PROVED;
h recovery from any nonzero synchronized moment:      PROVED;
top-only two-port synchronization at h!=0:             FALSE;
legal P7 exposure of M,Y0,Y1 with Z:                  UNKNOWN;
nonzero canonical m4 or m6 in the P7 null fan:         FALSE CONDITIONALLY;
nonzero direct/noncanonical moment forced by mixed P7: UNKNOWN;
unrestricted P5, P6, or P7 nonrestriction:            UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_residual_depth_loop_hafnian_cumulant_and_two_port_discriminant.py
python audit_residual_depth_loop_hafnian_cumulant_and_two_port_discriminant.py
python -m py_compile verify_residual_depth_loop_hafnian_cumulant_and_two_port_discriminant.py audit_residual_depth_loop_hafnian_cumulant_and_two_port_discriminant.py
uv run --with ruff ruff check verify_residual_depth_loop_hafnian_cumulant_and_two_port_discriminant.py audit_residual_depth_loop_hafnian_cumulant_and_two_port_discriminant.py
```

The primary verifier constructs the generic four-residual/four-port
square-zero exponential, divides every residual depth by the common port
moment, checks the logarithm and loop-hafnian reconstruction, and verifies
the symbolic two-residual discriminant and `2^d` coefficient law.  The
independent no-import audit starts from a separate matching recurrence with
integer weights, performs finite square-zero inversion, reconstructs every
residual subset by a separately written loop-hafnian recurrence, and checks
the discriminant.  These are fixed small replays of the algebra; the written
exponential and matching proofs establish arbitrary order.
