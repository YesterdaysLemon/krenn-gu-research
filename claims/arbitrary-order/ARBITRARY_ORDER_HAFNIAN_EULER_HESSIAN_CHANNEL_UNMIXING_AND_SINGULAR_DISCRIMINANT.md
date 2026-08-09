# Hafnian Euler--Hessian channel unmixing and the singular discriminant

## Status

**Exact arbitrary-order characteristic-zero theorem, conditional blocker-
surplus extraction, and exact observability wall.**  Let `h=haf(A)` on an
even residual vertex set, let `c` be its principal two-deletion vector, and
let `D` and `J` be its edge Hessian and third edge derivative.  A common-
cofactor response with coefficients in any vector space `W` has the form

```text
L(A)=h(A) U+sum_e c_e(A) T_e.                         (1)
```

The direct channel `U` and every cofactor channel `T_e` can be unmixed from
the residual-edge response jets by one Euler--Hessian connection.  On
`det D!=0`:

- if `h!=0`, the value and first response jet recover `U,T` uniquely;
- at every `h`, the first and second response jets recover `U,T` uniquely;
- at `h=0`, the value and first jet have one exact `W`-dimensional gauge,
  so the second jet is minimal **inside the linear response model (1)**;
- on `det D=0`, every actual first jet obeys the polynomial adjugate
  obstruction `adj(D)g=0`.

For the arbitrary-residual root/blocker aggregate, `U` is the direct
blocker-edge aggregate and

```text
T_{pq}=P_(r+2)(H_1,...,H_r,a_p,a_q).                 (2)
```

Thus legally observing the required response jets separates the multichannel
sum into honest two-row permanent extensions at arbitrary residual order.
If the observed jets lie in the diagonal target space and one recovered
`T_{pq}` has all three diagonal coefficients nonzero, it gives a genuine
`P_(r+2) -> Delta_3` extraction.  The strict support theorem then forces
support at least `3r+9` and full target-dual span in every row family.

The word "legally" is essential.  The current shallow `P_7` sensor supplies
the scalar decks `(h,c,D)` and reconstructs `A` on its Hessian open, but it
does not supply the tensor-valued residual-edge derivatives `g` and `G` in
(7) below.  Differentiating a graph coefficient while holding all incidence
rows fixed is not a local-vector operation.  The theorem is therefore a new
exact local-to-global test and a precise missing-data statement, not an
unconditional `P_5`, `P_6`, or `P_7` obstruction.  Global Krenn--Gu remains
**UNRESOLVED**.

No graph, support, blocker, colour-word, matching-family, parameter, or
finite-field search is used.

## 1. Hafnian polar notation

Let `K` be a characteristic-zero field.  Let `Q` be a named set of order

```text
q=2m>=4,
E=binom(Q,2),
N=|E|=binom(q,2).                                    (3)
```

Write `a=(a_e)_(e in E)` for the edge vector of a hollow symmetric matrix
`A`.  Put

```text
h(a)=haf(A),
c_e=partial_e h,
D_ef=partial_e partial_f h,
J_efk=partial_e partial_f partial_k h.                (4)
```

The tensor `J` is symmetric in its three edge indices.  It is zero unless
`e,f,k` are pairwise vertex-disjoint, and otherwise it is the principal
six-vertex-deletion hafnian.  At `q=4`, `J=0`.

The degree of `h,c,D` is respectively `m,m-1,m-2`.  Euler's identity gives

```text
D a=(m-1)c,
sum_k J_efk a_k=(m-2)D_ef.                           (5)
```

The first identity is the shallow Hessian inversion equation.  The second
is its derivative-degree companion.

Let `W` be any finite-dimensional `K`-vector space.  Fix coefficients

```text
U in W,                   T=(T_e)_(e in E) in W^E,   (6)
```

independent of `a`, and define the `W`-valued response (1).  Its first and
second residual-edge jets are

```text
g_f=partial_f L,
G_fg=partial_f partial_g L.                          (7)
```

Matrix-vector operations below act only on edge indices.  Thus `D T` is an
element of `W^E`, while

```text
(J dot T)_ef=sum_k J_efk T_k                         (8)
```

is a `W`-valued symmetric edge matrix.  A scalar row such as `c^T` contracts
the edge index and leaves an element of `W`.

Direct differentiation gives the fundamental response equations

```text
g=c U+D T,
G=D U+J dot T.                                       (9)
```

## 2. Determinant-cleared channel identities

Put

```text
delta=det D,
That=adj(D) g,
Shat=delta G-J dot That.                             (10)
```

Here `That in W^E` and `Shat in W^(E x E)`.

### Theorem 1 (polynomial Euler--Hessian identities)

Every response (1) satisfies

```text
That=delta (T+a U/(m-1)),                             (11)

(m-1)(c^T That-delta L)=delta h U,                   (12)

(m-1)Shat=delta D U.                                 (13)
```

Consequently the coefficient-free discriminant

```text
h Shat=D (c^T That-delta L)                          (14)
```

holds identically.  All equations are polynomial in the observed hafnian
jet and response jet; no inverse occurs.

### Proof

Multiply the first equation of (9) by `adj(D)`.  Since

```text
adj(D)D=delta I,
adj(D)c=delta a/(m-1)                                (15)
```

by (5), equation (11) follows.  Contract it with `c^T`.  Euler for `h`
gives `c^T a=m h`, so

```text
c^T That
 =delta c^T T+delta m h U/(m-1)
 =delta L+delta h U/(m-1),                           (16)
```

which is (12).

Substitute (11) and the second identity of (5) into (10):

```text
Shat
 =delta(D U+J dot T)
  -delta J dot (T+a U/(m-1))
 =delta D U/(m-1).                                   (17)
```

This proves (13).  Multiplying (13) by `h`, multiplying (12) by `D`, and
comparing proves (14).

### Corollary 2 (singular-Hessian first-jet obstruction)

At every point with `delta=0`,

```text
adj(D) g=0.                                          (18)
```

If `D` has corank one and `k` spans its kernel, symmetry gives
`adj(D)=gamma k k^T` for some `gamma!=0`; hence (18) is exactly

```text
k^T g=0 in W.                                        (19)
```

Equivalently, every scalar coordinate of the response gradient lies in
`im D`.  This is an actual equation on the singular Hessian divisor, not a
rank assertion inferred from a generic inverse.  It can be vacuous on
corank at least two because then `adj(D)=0`.

There are full-edge-torus corank-one points, so (18) is not merely a
coordinate-support condition.  For example, split six vertices as
`L disjoint_union R`, `|L|=|R|=3`, give the edges within `L` weight one,
the edges within `R` weight two, and every cross edge weight `t`.  The exact
Hessian determinant is

```text
det D=-46656 t^5(t-1)(t+1).                          (20)
```

At `t=1`, all fifteen edge weights are nonzero, `haf(A)=24`, and `D` has
rank fourteen.  Thus any legally exposed response first jet at that point
must satisfy one nontrivial `W`-valued kernel equation (19).

## 3. The Euler--Hessian connection on the open chart

Assume from now on that `delta!=0`.  Define

```text
Ttilde=D^(-1)g,
S=G-J dot Ttilde.                                    (21)
```

Equation (11) and division of (13) by `delta` give

```text
Ttilde=T+a U/(m-1),
S=D U/(m-1).                                         (22)
```

The operator

```text
L |-> G-J dot D^(-1)g                               (23)
```

will be called the **Euler--Hessian connection** here.  The name is local
to this proof package: (23) is a defined differential combination, not a
claim of standard terminology.  It cancels every cofactor channel `T_e` and
retains only the direct channel multiplied by `D/(m-1)`.

### Theorem 3 (arbitrary-order second-jet unmixing)

On `det D!=0`, the first and second response jets determine all coefficients
in (1) uniquely:

```text
U=(m-1)/N tr(D^(-1)S),
T=Ttilde-a U/(m-1).                                  (24)
```

For candidate data `(g,G)`, existence of coefficients `(U,T)` is equivalent
to

```text
D^(-1)S=(tr(D^(-1)S)/N) I_N.                        (25)
```

Once (25) holds, (24) is the unique solution.  A supplied value `L` belongs
to the same response if and only if the additional zero-order check

```text
L=hU+c^T T                                            (26)
```

holds.

### Proof

Equation (22) makes `D^(-1)S=I_N U/(m-1)`.  Its trace gives the first formula
in (24), and the first equation of (22) gives the second.  This proves
necessity and uniqueness.  Conversely, (25) and (24) reverse the calculation
and give both equations (9); (26) supplies the value equation.

Condition (25) is a compact obstruction: every off-diagonal entry of
`D^(-1)S` must vanish and all diagonal entries must agree as elements of
`W`.  Clearing `delta` turns it into polynomial adjugate equations.

## 4. Value plus first jet, and the exact `h=0` gauge

### Theorem 4 (first-jet dichotomy)

On `det D!=0`:

1. If `h!=0`, the value and first response jet recover the coefficients
   uniquely by

   ```text
   U=(m-1)/h (c^T D^(-1)g-L),
   T=D^(-1)g-a U/(m-1).                              (27)
   ```

   Every candidate pair `(L,g)` has exactly one representation of the form
   (1) at that point.  Thus value plus first jet provides unmixing but no
   representability obstruction on the `h!=0` chart.

2. If `h=0`, a candidate `(L,g)` has a representation if and only if

   ```text
   L=c^T D^(-1)g,                                    (28)
   ```

   equivalently `delta L=c^T adj(D)g`.  When (28) holds, its complete
   solution set is one affine `W`-gauge:

   ```text
   (U,T_e) |-> (U-(m-1)X, T_e+a_e X),       X in W. (29)
   ```

### Proof

Contract the first identity of (22) with `c^T` and use
`c^T a=m h`.  This gives

```text
c^T D^(-1)g-L=h U/(m-1).                            (30)
```

When `h!=0`, solve for `U` and then for `T`, proving (27).  Direct
substitution also proves that every `(L,g)` is represented.

When `h=0`, equation (30) becomes the necessary condition (28).  If it
holds, choose any `U` and put `T=D^(-1)g-aU/(m-1)`; the first jet and value
then agree.  If two coefficient systems give the same `(L,g)`, their
difference obeys

```text
D deltaT=-c deltaU,
deltaT=-a deltaU/(m-1).                              (31)
```

Writing `deltaU=-(m-1)X` gives exactly (29).  Conversely, (29) fixes `g`
by `Da=(m-1)c` and fixes `L` by `c^T a=m h=0`.

### Corollary 5 (precise minimality statement)

At `h=0`, value plus first jet cannot identify `U,T` inside the unrestricted
linear coefficient model (1): its fibre has dimension `dim W`, exactly the
gauge (29).  Adding the second jet removes that gauge on `det D!=0`, by
Theorem 3.

This is not an information-theoretic claim about every nonlinear physical
model.  Extra permanent factorization, support, target, or cross-root
structure could distinguish gauge representatives.  The proved minimality
is only for the isolated linear response model (1), as stated.

## 5. Exact transfer to the common-cofactor blocker aggregate

Take `r` fixed root rows and a blocker set `B` of size `r+2`.  For blockers
`u,v`, put

```text
F_uv=P_r(H_w:w in B minus {u,v}).                    (32)
```

Let the even residual graph have edge matrix `A`.  For a residual vertex
`p`, let `a_p(u)` be its common blocker incidence row.  The arbitrary-order
two-port cofactor theorem gives the exact aggregate

```text
Lambda(A)
 =h(A) sum_(u<v) F_uv B_uv
  +sum_(p<q) c_pq(A)
       P_(r+2)(H_1,...,H_r,a_p,a_q).                 (33)
```

This is (1) in the tensor product of the blocker local spaces, with

```text
U=sum_(u<v) F_uv B_uv,
T_pq=P_(r+2)(H_1,...,H_r,a_p,a_q).                   (34)
```

All coefficients in (34) are independent of the residual--residual edge
variables `a`.  Theorems 1--4 therefore apply without a factorization
assumption.

### Corollary 6 (conditional arbitrary-surplus permanent extraction)

Assume a legal common-deletion construction exposes the residual-edge jets
required by Theorem 3, or by Theorem 4 on `h!=0`, and assume those observed
jets lie in the diagonal target subspace

```text
D_3=span{e_0^(tensor(r+2)),
         e_1^(tensor(r+2)),
         e_2^(tensor(r+2))}.                         (35)
```

Then every recovered `U` and `T_pq` lies in `D_3`.  If for some pair `p,q`
the three diagonal coefficients of `T_pq` are all nonzero, (34) is a concise
restriction

```text
P_(r+2) -> Delta_3.                                  (36)
```

Consequently the strict permanent support and first-polar theorems give

```text
support(H_1,...,H_r,a_p,a_q)>=3(r+2)+3=3r+9,         (37)
```

and every one of the `r+2` row families spans the full target dual.

### Proof

The recovery formulas (24) or (27) use only scalar linear combinations of
the observed jets, so the recovered coefficients remain in the linear
space `D_3`.  Full diagonal support makes `T_pq` equivalent to `Delta_3` by
an invertible diagonal change in one source mode.  The established strict
support and first-polar theorems then give (37) and the span assertions.

For five roots this recovers the familiar lower bound `24`, but now from an
arbitrary even residual set once the necessary edge-response jets are
legally present.  The theorem does not assert that some recovered channel
has all three diagonal coefficients nonzero; that is a separate target
incidence question.

## 6. What the shallow Hessian does and does not supply

The synthesis with shallow tomography is exact:

```text
scalar decks (h,c,D), det D!=0
  -> reconstruct A and therefore J;

tensor response jets (g,G)
  -> Euler--Hessian connection (23)
  -> recover U and every honest T_pq;

diagonal full-support recovered T_pq
  -> P_(r+2) -> Delta_3
  -> strict support at least 3r+9.                    (38)
```

The first arrow does **not** imply the second.  In particular:

1. Knowing `(h,c,D)` and only the top value `L` leaves the coefficient map
   `(U,T) |-> hU+c^T T` highly nonidentifiable.
2. The legal `P_7` `H_4/H_6/H_8` sensor observes scalar principal hafnians.
   It does not currently observe `partial_e Lambda` or
   `partial_e partial_f Lambda` while holding `U,T` fixed.
3. A derivative with respect to one scalar graph edge changes the graph
   coefficient.  Varying a physical local vector instead changes an entire
   incident star and generally changes the port rows in (34), violating the
   fixed-coefficient hypothesis of (1).
4. The existing marked-star theorem shows this gap concretely: formal edge
   differentiation has a common shore normalization, but its physical
   implementing weights vanish on the projectively constant root branch.

Thus (18), (25), and (28) become legal obstructions only after a paired-depth
selector, a clean marked-edge circuit, or an equivalent physical operation
has actually exposed the relevant response jets.  Naming formal derivatives
does not expose them.

## 7. Scope wall

```text
arbitrary-order response equations (9):                 EXACT;
determinant-cleared identities (11)--(14):               EXACT;
singular-Hessian adj(D)g obstruction:                    EXACT;
full-torus q=6 corank-one control:                       EXACT;
second-jet coefficient recovery on det D:               UNIQUE;
h!=0 value/first-jet recovery:                           UNIQUE, NO CONSTRAINT;
h=0 value/first-jet discriminant:                        EXACT;
h=0 first-jet coefficient fibre:                         W-GAUGE;
second-jet minimality:                                   ONLY IN MODEL (1);
arbitrary-residual permanent channels after legal jets:  RECOVERED;
full-diagonal recovered channel support >=3r+9:           CONDITIONAL EXACT;
current P7 scalar shallow deck exposes g,G:               FALSE;
legal marked/deletion selector for g,G:                   UNKNOWN;
some recovered T_pq has three nonzero colours:            UNKNOWN;
unrestricted P5/P6/P7 obstruction:                       UNKNOWN;
global Krenn--Gu:                                         UNRESOLVED.       (39)
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_arbitrary_order_hafnian_euler_hessian_channel_unmixing.py
python claims/arbitrary-order/audit_arbitrary_order_hafnian_euler_hessian_channel_unmixing.py
python -m py_compile verify_arbitrary_order_hafnian_euler_hessian_channel_unmixing.py audit_arbitrary_order_hafnian_euler_hessian_channel_unmixing.py
uv run --with ruff ruff check verify_arbitrary_order_hafnian_euler_hessian_channel_unmixing.py audit_arbitrary_order_hafnian_euler_hessian_channel_unmixing.py
```

The primary verifier differentiates one fixed symbolic six-vertex response,
checks both recovery formulas and the determinant-cleared identities, proves
the exact `h=0` gauge on a four-vertex full-torus point, and checks the
one-parameter determinant and corank-one singular discriminant (20).  The
independent no-import audit uses a separate matching-monomial response,
rational elimination, and its own kernel calculation.  These are fixed
exact audits of the displayed formulae, not searches over supports, graphs,
blockers, words, fields, or parameter tuples.

Dependencies and legality boundary:

- [`RESIDUAL_HAFNIAN_COMMON_COFACTOR_GRAM_THEOREM.md`](RESIDUAL_HAFNIAN_COMMON_COFACTOR_GRAM_THEOREM.md)
- [`RESIDUAL_HAFNIAN_HESSIAN_KNESER_ETALE_AND_JET_INTEGRABILITY_THEOREM.md`](RESIDUAL_HAFNIAN_HESSIAN_KNESER_ETALE_AND_JET_INTEGRABILITY_THEOREM.md)
- [`P7_CROSS_DEPTH_HAFNIAN_DERIVATIVE_AND_PROJECTIVE_MARKED_STAR_BOUNDARY.md`](../p7/P7_CROSS_DEPTH_HAFNIAN_DERIVATIVE_AND_PROJECTIVE_MARKED_STAR_BOUNDARY.md)
- [`ARBITRARY_ORDER_TWO_RESIDUAL_STRICT_SUPPORT_STAIRCASE_AND_COORDINATE_FORCING.md`](ARBITRARY_ORDER_TWO_RESIDUAL_STRICT_SUPPORT_STAIRCASE_AND_COORDINATE_FORCING.md)
