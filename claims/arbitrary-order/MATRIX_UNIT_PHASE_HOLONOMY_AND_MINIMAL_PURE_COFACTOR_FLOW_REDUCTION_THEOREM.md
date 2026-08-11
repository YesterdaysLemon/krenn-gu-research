# Matrix-unit phase holonomy and minimal pure-cofactor flow reduction

## Status

This is an exact arbitrary-order characteristic-zero refinement of the two
phase-sensitive exits in the `r=1` matrix-unit active-word branch.

First, every finite active transport cycle carries a nonzero Laurent
monomial

```text
H=product_i lambda(B_i)/lambda(E_i),                 (1)
```

where `E_i` is the selected offdiagonal cross core and `B_i` is its forced
diagonal bridge matching.  The exponent vector of (1) is a nonzero integral
circulation for the endpoint-label incidence map.  Consequently `H` is
invariant under every local diagonal coordinate gauge, including the
moment-balancing gauge.

Every active cycle has an exact alternative:

1. some word fibre contains a compatible matching beyond its incoming
   diagonal and outgoing offdiagonal terms; or
2. every cycle fibre is exactly binomial, and the mixed target equations
   force

   ```text
   H=(-1)^m,                                         (2)
   ```

   where `m` is the cycle length.

Equation (2) is not automatically contradictory.  An exact sparse
eight-vertex table below realizes a three-step binary bridge cycle with
exactly two terms in every selected fibre and `H=-1`.  The table is not
complete, has no colour-two target, and is **not** a Krenn--Gu witness.  It
proves that an odd active cycle is not a sign contradiction even at the
binomial boundary.

Second, every pure-shore hafnian cancellation containing a nonzero matching
term has a least supported cancelling residual `R`.  Its edge-cofactor flow

```text
C_ij=z_ij haf(Z[R-{i,j}])                            (3)
```

is nonzero at a matching edge through every vertex and has zero sum at every
vertex.  Hence its active graph has minimum degree at least two.  Exactly
one of the following occurs:

1. a vertex has at least three active cofactor terms, giving a genuine
   phase-branching equation; or
2. the active graph is a spanning disjoint union of even cycles, and the
   nonzero `C_ij` alternate exactly as `alpha,-alpha` around each cycle.

The minimal residual, active graph, branching/cycle split, and alternating
relations are invariant under diagonal gauge.  Thus the preceding
moment-balanced magnitude normal form can be imposed without changing these
remaining phase obstructions.

This theorem narrows active holonomy and pure-shore cancellation; it does
not exclude either one.  The deeper branch, the `r=1` branch, and the global
Krenn--Gu conjecture remain **UNKNOWN/UNRESOLVED**.

## 1. Imported active transport data

Let `Omega` have even cardinality and let every physical pair in the `r=1`
branch carry one nonzero matrix unit

```text
W_uv=lambda_uv e_(ell_u(uv))^* tensor e_(ell_v(uv))^*,
lambda_uv!=0.                                        (4)
```

Assume

```text
T_W=Delta_(n,3).                                     (5)
```

The imported
[`active-word bridge-transport theorem`](MATRIX_UNIT_ACTIVE_WORD_FIBRE_CROSS_MATCHING_RESPONSE_AND_BRIDGE_TRANSPORT_TRICHOTOMY.md)
starts at an active mixed word `chi_i`, selects a cofactor-active
offdiagonal matching `E_i`, and chooses nonzero residual pure matchings
`P_i`.  Put

```text
F_i=E_i union P_i.                                   (6)
```

This is a nonzero physical perfect matching inducing `chi_i`.  If the
selected bridge steps avoid the deeper alternative, their union `B_i` is a
diagonal matching on the endpoints of `E_i`, and

```text
G_i=B_i union P_i                                   (7)
```

is a nonzero diagonal perfect matching inducing the transported word
`chi_(i+1)`.

If the pure-shore exit is also absent, `chi_(i+1)` is active.  Finite
iteration then gives a cycle

```text
chi_0 -> chi_1 -> ... -> chi_(m-1) -> chi_0,
m>=2.                                                (8)
```

Indices below are taken modulo `m`.

## 2. The endpoint-character circulation

Let `Z^E` be the integral edge-exponent lattice.  Define the endpoint-label
character map

```text
A:Z^E -> Z^(Omega x {0,1,2}),
(Aq)_(v,c)=sum_(e incident to v, ell_v(e)=c) q_e.    (9)
```

For a matching `M` inducing a word `chi`, its indicator vector satisfies

```text
A 1_M = 1_chi,                                      (10)
```

where `1_chi` has a one in coordinate `(v,chi(v))` and zero in the other two
coordinates at `v`.

Define

```text
z=sum_i (1_(G_i)-1_(F_i))
 =sum_i (1_(B_i)-1_(E_i)).                           (11)
```

The residual matchings cancel in the second equality.  Equations (8)--(10)
give

```text
Az=sum_i (1_(chi_(i+1))-1_(chi_i))=0.               (12)
```

Every edge of `B_i` is diagonal and every edge of `E_i` is offdiagonal.
Those are disjoint fixed classes of physical edges, so the positive and
negative supports in (11) cannot cancel each other.  Since every `E_i` is
nonempty,

```text
z!=0.                                                (13)
```

Thus an active cycle produces a genuine nonconstant torus-invariant Laurent
monomial, not the empty identity.

### Theorem 1 (gauge-invariant matching holonomy)

Put

```text
H=lambda^z
 =product_i lambda(G_i)/lambda(F_i)
 =product_i lambda(B_i)/lambda(E_i).                 (14)
```

Then `H in C^*` is unchanged by every diagonal coordinate scaling

```text
lambda'_uv
 =s_(u,ell_u(uv))s_(v,ell_v(uv))lambda_uv,
s_(v,c) in C^*.                                     (15)
```

### Proof

Under (15), the matching weight at word `chi` is multiplied by

```text
gamma_s(chi)=product_v s_(v,chi(v)).                 (16)
```

Hence one transition ratio is multiplied by

```text
gamma_s(chi_(i+1))/gamma_s(chi_i).
```

These factors telescope around (8).  Equivalently, direct substitution in
the Laurent monomial gives the multiplier

```text
product_(v,c) s_(v,c)^((Az)_(v,c))=1                (17)
```

by (12).

## 3. Aggregate or exact binomial holonomy

At the word `chi_i`, the incoming matching `G_(i-1)` is diagonal and the
outgoing matching `F_i` is offdiagonal.  Both are nonzero and compatible.

### Theorem 2 (cycle-fibre split)

Exactly one of the following holds:

```text
aggregate: some chi_i has at least one compatible matching
           other than G_(i-1) and F_i;

binomial:  every chi_i has exactly the two compatible matchings
           G_(i-1), F_i, and H=(-1)^m.               (18)
```

### Proof

If any additional matching occurs, the first case holds.  Otherwise the
complete mixed coefficient at `chi_i` is

```text
0=lambda(G_(i-1))+lambda(F_i),                       (19)
```

so

```text
lambda(F_i)=-lambda(G_(i-1)).                        (20)
```

Multiplying (20) over the cycle and cyclically reindexing the `G` factors
gives

```text
product_i lambda(F_i)=(-1)^m product_i lambda(G_i).
```

Taking the ratio proves (2).

The aggregate alternative is not a failure of the theorem.  It records the
precise point at which a summed response cannot be replaced by one binomial
transition ratio.

## 4. Exact sparse odd-cycle sharpness

Use vertices `0,...,7` and the three words

```text
chi_0=(0,0,0,0,1,1,1,1),
chi_1=(0,0,1,1,0,0,1,1),
chi_2=(0,1,0,1,0,1,0,1).                            (21)
```

The cross, residual, and bridge matchings are

```text
i   E_i       P_i       B_i
0   24|35     01|67     23|45
1   12|56     04|37     15|26
2   14|36     02|57     46|13.                       (22)
```

Every one of the 18 displayed edges is distinct.  Give each edge of `E_i`
its endpoint labels from `chi_i`, each edge of `P_i` its equal labels from
`chi_i`, and each edge of `B_i` its equal labels from `chi_(i+1)`.  This
defines one consistent sparse matrix-unit table.  Give weight `-1` to

```text
24, 12, 14                                             (23)
```

and weight `1` to every other displayed edge.  All omitted pairs are zero.

### Theorem 3 (a physical three-step binomial cycle)

For each `i`, `F_i=E_i union P_i` is offdiagonal and induces `chi_i`, while
`G_i=B_i union P_i` is diagonal and induces `chi_(i+1)`.  The complete
supported fibres are

```text
chi_0: F_0=-1, G_2= 1;
chi_1: F_1=-1, G_0= 1;
chi_2: F_2=-1, G_1= 1.                              (24)
```

Thus all three selected mixed coefficients vanish exactly and

```text
H=product_i lambda(B_i)/lambda(E_i)=-1=(-1)^3.       (25)
```

### Proof

Direct matching enumeration gives exactly the two displayed terms in every
fibre.  The bridge labels in (22) are precisely the binary-square labels
obtained by swapping the two endpoint colours along each pair of cross
edges.  The three negative cross products give (25).

This table omits ten physical pairs and uses no colour-two labels.  It is
not in the complete `r=1` branch, does not realize any ternary GHZ target,
and is not a witness or counterexample.  It proves only that fixed physical
labels, exact bridge squares, binomial mixed equations, and an odd cycle can
coexist when the nontrivial invariant (25) has the required value.

## 5. Minimal supported pure cancellation

Let `Z` be a hollow symmetric scalar matrix on an even set `S`, over a field
of characteristic not two.  Write

```text
h(R)=haf(Z[R])                                       (26)
```

for even `R subset S`, with `h(empty)=1`.

Suppose

```text
h(S)=0
```

but the support of `Z[S]` has a perfect matching.  This is exactly the
pure-shore cancellation exit supplied by active transport: the zero
hafnian contains a nonzero matching monomial.

Choose a least-cardinality even subset `R subset S` such that

```text
h(R)=0
and the support on R has a perfect matching P.       (27)
```

Necessarily `|R|>=4`.  For every `ij in P`, the residual `R-{i,j}` has the
supported matching `P-{ij}`.  Minimality and the convention at the empty
set give

```text
h(R-{i,j})!=0.                                      (28)
```

Thus the cancellation is regular in at least one cofactor direction at
every vertex.  This avoids the false inference that an arbitrary displayed
matching term must survive aggregation in the full first-cofactor deck;
minimality is what makes (28) rigorous.

## 6. Euler cofactor flow and the cycle/branching split

For every pair `ij subset R`, put

```text
C_ij=z_ij h(R-{i,j}),                               (29)
```

and let `A_R` be the simple graph of pairs with `C_ij!=0`.

### Theorem 4 (minimal cofactor-flow normal form)

The graph `A_R` spans `R`, contains `P`, and has minimum degree at least two.
Moreover exactly one of the following holds:

```text
phase branching: some vertex has degree at least three in A_R;

alternating cycles: A_R is a spanning disjoint union of even cycles,
                    and its C-values alternate alpha,-alpha
                    around every component.         (30)
```

### Proof

Equation (28) and the nonzero weights on `P` show that every edge of `P`
belongs to `A_R`; hence the active graph spans.

Expanding the zero hafnian at any vertex `i` gives the exact Euler row
equation

```text
sum_(j in R-{i}) C_ij=h(R)=0.                        (31)
```

No row can have exactly one nonzero term, so every degree is at least two.
If some degree is at least three, the first case of (30) holds.

Otherwise every degree is two, and a finite 2-regular graph is a disjoint
union of cycles.  On one cycle, write consecutive edge values as `w_k`.
Equation (31) says

```text
w_k=-w_(k-1).                                       (32)
```

The values alternate.  An odd cycle would give `w_0=-w_0`, forcing
`2w_0=0`, contrary to characteristic not two and activity.  Every component
is therefore even.

### Sharpness

On vertices `0,1,2,3`, the `K_(2,2)` support

```text
z_01=2, z_02=3, z_13=-2, z_23=3                    (33)
```

has hafnian `6-6=0`.  Its active flow is the four-cycle with values

```text
C_01=6, C_13=-6, C_23=6, C_02=-6.                  (34)
```

The complete support

```text
z_01=z_23=z_02=z_13=z_03=1, z_12=-2                (35)
```

has hafnian `1+1-2=0` and active graph `K_4`, with degree three at every
vertex.  Both alternatives in (30) therefore occur exactly at the smallest
possible residual size.  These scalar shores are local cancellation models,
not graph witnesses.

## 7. Gauge covariance and the moment-balanced representative

Scale one pure-colour matrix by nonzero vertex factors:

```text
z'_ij=t_i t_j z_ij.                                 (36)
```

For every even `R`, matching homogeneity gives

```text
h'(R)=(product_(i in R)t_i) h(R),
C'_ij=(product_(i in R)t_i) C_ij.                   (37)
```

Thus supported cancellation, least residuals, the active graph, its degree
split, and all alternating relations are unchanged.  Every active `C_ij` in
one residual is merely multiplied by the same nonzero scalar.

Over `C`, the preceding
[`moment-balanced gauge theorem`](MATRIX_UNIT_GHZ_MOMENT_BALANCED_GAUGE_AND_UNIT_PHASE_ACTIVE_TRANSPORT_SHARPNESS_THEOREM.md)
uses positive factors of the form (36).  Theorem 1 and equation (37) show
that it changes neither the active-cycle holonomy nor the minimal pure-
cofactor obstruction.  Magnitude balance and the phase reduction can
therefore be imposed simultaneously.

## 8. Combined proof-topology consequence

Start with a support-minimal offdiagonal matrix-unit hypothetical witness
over `C`, put it in moment-balanced gauge, and make any fixed sequence of
cofactor-active transport choices.  The imported theorem and the results
above give the following exact finite alternative:

```text
deeper:             a selected bridge enters the deeper component;

pure branching:     a least cancelling pure residual has an active
                    cofactor-flow vertex of degree at least three;

pure phase cycle:   a least cancelling pure residual has a spanning
                    union of alternating even cofactor cycles;

aggregate holonomy: an active word cycle has an additional compatible
                    term in at least one fibre;

binomial holonomy:  an active word cycle has a nonzero endpoint-character
                    circulation z and lambda^z=(-1)^m.               (38)
```

These are phase-sensitive normal forms, not exclusions.  In particular:

```text
active-cycle Laurent circulation and gauge invariance: PROVED;
aggregate/binomial active-cycle split:                 PROVED;
binomial holonomy equation H=(-1)^m:                   PROVED;
odd binomial cycle is automatically contradictory:    FALSE;
least supported pure cancelling residual exists:      PROVED;
cofactor branching/even-cycle split:                   PROVED;
compatibility with the actual moment gauge:            PROVED over C;
aggregate holonomy excluded:                           UNKNOWN;
binomial Laurent holonomy excluded:                    UNKNOWN;
pure cofactor branching/cycles excluded:               UNKNOWN;
deeper-blocker branch excluded:                        UNKNOWN;
r=1 matrix-unit branch excluded:                       UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.
```

The next phase-sensitive step must use additional mixed coefficient
identities to constrain the nontrivial invariant `lambda^z`, or propagate
the Euler cofactor rows beyond one minimal pure residual.  Neither the word
cycle nor the alternating cofactor signs alone contradict the target.

## Replay

```powershell
python claims/arbitrary-order/verify_matrix_unit_phase_holonomy_and_minimal_pure_cofactor_flow.py
python claims/arbitrary-order/audit_matrix_unit_phase_holonomy_and_minimal_pure_cofactor_flow.py
python -m py_compile claims/arbitrary-order/verify_matrix_unit_phase_holonomy_and_minimal_pure_cofactor_flow.py claims/arbitrary-order/audit_matrix_unit_phase_holonomy_and_minimal_pure_cofactor_flow.py
python -m ruff check claims/arbitrary-order/verify_matrix_unit_phase_holonomy_and_minimal_pure_cofactor_flow.py claims/arbitrary-order/audit_matrix_unit_phase_holonomy_and_minimal_pure_cofactor_flow.py
```

The primary verifier enumerates every supported matching of the sparse
eight-vertex table, checks the three complete binomial fibres, constructs
the endpoint-character circulation, replays a nontrivial exact GHZ gauge,
and computes both minimal cofactor-flow alternatives.  The independent
no-import audit uses decimal endpoint codes, a least-set-bit compatible-
matching recursion, a separately encoded circulation census, and an
independent bitmask hafnian.  These finite checks audit conventions and
sharpness.  The arbitrary-order results are the character telescoping,
binomial multiplication, least-residual argument, and Euler row proof above.
