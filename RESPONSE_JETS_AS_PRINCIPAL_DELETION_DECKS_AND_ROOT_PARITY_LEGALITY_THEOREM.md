# Response jets as principal-deletion decks and the root-parity legality theorem

## Status

**Exact arbitrary-order characteristic-zero identification, universal
same-graph no-go, and sharp root-parity criterion.**  For the common-cofactor
response

```text
Lambda_Q(A)=haf(A) U
  +sum_(e subset Q, |e|=2) haf(A[Q\e]) T_e,             (1)
```

the formal residual-edge jets needed by Euler--Hessian channel unmixing have
a completely physical meaning:

```text
g_e=Lambda_(Q\e),
G_(e,f)=Lambda_(Q\(e union f))  if e,f are disjoint,
G_(e,f)=0                       otherwise.             (2)
```

Thus the missing tensor data are precisely the principal response decks with
two and four residual vertices deleted.  No continuously variable graph edge
and no infinitesimal edge operation is required.  On `det D!=0`, the top
response plus the two-deletion deck unmixes all channels when `haf(A)!=0`;
at a residual hafnian zero, the four-deletion deck removes the exact first-jet
gauge.  On the singular Hessian divisor the two-deletion deck obeys the
polynomial physical obstruction

```text
adj(D) (Lambda_(Q\e))_e=0.                              (3)
```

Identification is not exposure.  The graph tensor with all residual vertices
present does not universally determine any nonzero pair-deletion tensor, even
if **all** of its physical local-vector evaluations and polarizations are
known.  An exact nonzero affine fibre below keeps the full tensor fixed while
the pair-deletion tensor varies.  Local finite differences therefore cannot
manufacture (2).

Mixed root words provide the only existing herald-free way to consume named
residual vertices.  If `r` probe roots are present, a deck deleting an even
set `D`, `|D|=2k`, occurs in the root cofactor ledger exactly with weight

```text
Omega_D=haf [ L    H_D ]
              [H_D^T  0 ],                            (4)
```

where `L` is the hollow root--root matrix and `H_D` is the root-to-`D`
incidence matrix.  Consequently `Omega_D` is identically zero unless

```text
r is even and r>=2k.                                  (5)
```

This closes the root-polarization candidate for every odd-root branch: no
mixed root word, polarization, or linear combination contains any column of
the two- or four-deletion response deck.  In particular, the three-root and
five-root response shores underlying the active `P_5` and `P_7` reductions
cannot expose `g` or `G` by that mechanism.

The four-root `P_6` shore is the first parity-compatible case.  Its
two-deletion weight is one root--root edge times a polarized two-root fan;
its four-deletion weight is a four-row permanent.  A clean `2 x 2` polar fan
has rank at most four and cannot recover the six two-deletion faces on a
four-residual window.  A clean `2 x 3` fan can recover all six: the explicit
certificate in (24) has determinant `-2`.  This is a sharp legal P6 escape,
conditional on nuisance separation and a nonzero compatible root--root
shore.  It is not forced in an arbitrary witness.

The theorem gives a smaller and more physical target for future selectors:
observe a synchronized principal deck, not a formal tensor of edge
derivatives.  It does not expose that deck from the single top GHZ equality,
does not force the clean P6 chart, and does not prove or refute Krenn--Gu.
Global Krenn--Gu remains **UNRESOLVED**.

No graph family, support family, colour word, matching family, parameter
tuple, or finite field is searched or enumerated.  The proof is symbolic at
arbitrary order; the replays use only fixed small identities.

## 1. The full principal response deck

Let `K` be a characteristic-zero field, let `Q` be a named even set of order
`q=2m`, and let `A=(a_pq)` be a hollow symmetric scalar matrix on `Q`.
Coefficients

```text
U in W,                    T_e in W                    (6)
```

take values in an arbitrary `K`-vector space `W` and are independent of the
edge variables of `A`.  For every even subset `S subset Q`, define

```text
Lambda_S
 =haf(A[S]) U
  +sum_(e subset S, |e|=2) haf(A[S\e]) T_e.           (7)
```

The top member is (1).  The other members use the same `U,T_e`; they are the
responses of the same block graph after the residual vertices `Q\S` have
been removed.  In the blocker aggregate of the Euler--Hessian theorem,

```text
U=sum_(u<v) F_uv B_uv,
T_e=P_(r+2)(H_1,...,H_r,a_p,a_q),       e={p,q}.      (8)
```

Thus (7) is tensor-valued and preserves every blocker mode.

For a matching `M={e_1,...,e_k}` of a vertex set `D subset Q`, write

```text
partial_M=partial_(a_e1)...partial_(a_ek).            (9)
```

### Theorem 1 (edge jets collapse to vertex-deletion decks)

For every matching `M` with vertex set `D`,

```text
partial_M Lambda_Q=Lambda_(Q\D).                     (10)
```

In particular (2) holds.  More generally, the derivative in (10) is
independent of the chosen perfect matching of `D`.

### Proof

Every monomial of `haf(A[S])` is a perfect matching of `S`.  Differentiating
by the pairwise disjoint edges in `M` retains exactly the matchings containing
`M`; deleting those fixed edges is a weight-preserving bijection with the
perfect matchings of `S\D`.  Therefore

```text
partial_M haf(A[S])=haf(A[S\D])                     (11)
```

when `D subset S`, and the derivative is zero otherwise.  Apply (11) first
to the direct term in (1).  A cofactor term indexed by `e` survives exactly
when `e` is disjoint from `D`, and then becomes

```text
haf(A[Q\(D union e)]) T_e.                           (12)
```

The sum of (12) over `e subset Q\D`, together with the direct term, is
exactly (7) for `S=Q\D`.  This proves (10).

For two edge derivatives, intersecting edges can occur in no matching
monomial, so that entry is zero.  Disjoint edges give the four-deletion deck,
proving (2).

### Corollary 2 (four-set integrability for tensor responses)

For distinct `i,j,k,l`,

```text
G_(ij,kl)=G_(ik,jl)=G_(il,jk)=Lambda_(Q\{i,j,k,l}).  (13)
```

The formal symmetric `E x E` second response jet therefore contains only
`binom(q,4)` potentially distinct nonzero tensors.  A legal construction
does not need to imitate `N(N+1)/2` independent coefficient derivatives: it
needs the named four-deletion principal deck.

## 2. Euler--Hessian unmixing stated only with physical decks

Let

```text
h=haf(A),       c_e=haf(A[Q\e]),
D_ef=haf(A[Q\(e union f)]) for disjoint e,f,
D_ef=0 otherwise.                                      (14)
```

Let `J` be the analogous six-deletion tensor.  By Theorem 1, the response
value and decks are exactly

```text
L=Lambda_Q,
g=(Lambda_(Q\e))_e=c U+D T,
G=(Lambda_(Q\(e union f)))_(e,f)=D U+J dot T,        (15)
```

with the convention that the intersecting entries of `G` are zero.

### Theorem 3 (principal-deck unmixing)

Assume `det D!=0`.

1. If `h!=0`, the top response and the two-deletion deck uniquely recover
   `U,T`:

   ```text
   U=(m-1)/h (c^T D^(-1)g-L),
   T=D^(-1)g-a U/(m-1).                              (16)
   ```

2. At every `h`, the two- and four-deletion decks uniquely recover `U,T`:

   ```text
   Ttilde=D^(-1)g,
   S=G-J dot Ttilde,
   U=(m-1)/N tr(D^(-1)S),
   T=Ttilde-a U/(m-1).                               (17)
   ```

3. On `det D=0`, every physical two-deletion deck satisfies (3).

### Proof

Equations (15) are the response equations of the Euler--Hessian theorem,
now identified by Theorem 1 with actual principal graph responses.  Euler's
identities `Da=(m-1)c` and `J dot a=(m-2)D` give (16)--(17) exactly as in the
Euler--Hessian proof.  Multiplying the first equation of (15) by `adj(D)` at
`det D=0` gives (3).

This theorem changes the legality target, not the algebraic formulas.  An
independently exposed principal deletion tensor is a legitimate graph
tensor.  Merely knowing that it exists is not the same as obtaining its
target value from the original top equality.

## 3. A nonlinear no-go from the complete present-vertex tensor

The failure of local finite differences is stronger than a degree count.
It persists even if the complete multilinear graph tensor with every vertex
present is supplied.

Choose distinct vertices

```text
p,q,u,v,s_1,t_1,...,s_d,t_d.                         (18)
```

Install only the edge blocks

```text
p--u,             q--v,             s_i--t_i,
```

and one variable edge block `X` on `u--v`.  Set every other edge block,
including `p--q`, to zero.  All displayed fixed blocks are nonzero.

### Theorem 4 (complete-tensor pair-vacuum fibre)

The full graph tensor on all vertices in (18) is the fixed nonzero product

```text
B_pu B_qv product_i B_(s_i,t_i),                     (19)
```

independent of `X`.  After deleting `p,q`, the graph tensor is

```text
X product_i B_(s_i,t_i),                             (20)
```

and varies freely with `X`.

Consequently no graph-independent function, whether linear, polynomial,
rational on a common domain, or otherwise, of the complete present-vertex
graph tensor
can recover the pair-deletion tensor for every block graph.  In particular,
arbitrary physical local-vector evaluations, polarizations, and finite
differences at the present vertices do not universally expose `g_e`.

### Proof

In the full graph, `p` has the unique possible partner `u` and `q` has the
unique possible partner `v`.  Every `s_i` has the unique partner `t_i`.
Hence (19) is the unique nonzero matching product, and the edge `u--v`
cannot be used.  After deleting `p,q`, every `s_i--t_i` is still forced and
`u--v` is the remaining forced edge, proving (20).

The full multilinear tensors are literally identical for every value of
`X`, so all of their evaluations and polarizations agree.  The deletion
tensors do not.  Any purported universal postprocessing would assign one
value to the common input but would have to return all values of (20), a
contradiction.

The control is nonzero and works with genuine bilinear edge blocks.  It is
not a GHZ realization, so it does not rule out a target-specific nonlinear
identity imposed by all mixed GHZ equations.

## 4. Mixed-root legality and the augmented-hafnian weight

Let `R` be a set of `r` probe roots and let `N` be the nonroot set.  After
choosing any fixed or polarized root vectors, write

```text
L_ij=B_ij(x_i,x_j),                  i,j in R,
H_(i,u)=B_(i,u)(x_i,z_u),            i in R,u in N.   (21)
```

Fix an even deletion set `D subset N`, `|D|=2k`.  In the mixed-root cofactor
expansion, the coefficient on the principal cofactor `C_D` is the sum over
all root partial matchings whose remaining roots map bijectively to `D`.

### Theorem 5 (root-deletion weight and parity)

That coefficient is exactly (4).  Equivalently,

```text
Omega_D
 =sum_(P partial matching of R, |P|=(r-2k)/2)
    product_({i,j} in P) L_ij
    per H_(R\vertices(P),D).                         (22)
```

It is zero when `(r-2k)/2` is not a nonnegative integer.  Hence an
even-deletion deck can occur only under (5).

### Proof

Expand the hafnian in (4).  The lower-right block is zero, so no two
vertices of `D` may match each other.  Every vertex of `D` must therefore
match a distinct root, using a root--`D` entry of `H_D`.  The remaining
`r-2k` roots must pair among themselves through `L`.  Choosing those root
pairs gives `P`; the bijections from the remaining roots to `D` give the
permanent in (22).  This partitions the nonzero matchings and proves both
formulas.

If `r` is odd, every mixed-root cofactor depth is `r-2j`, hence odd.  The
decks in (2) have depths two and four.  Their columns are therefore absent,
not merely linearly dependent.

### Corollary 6 (odd-root selector no-go)

On every three-root or five-root shore, all root-vector polarizations and
all their linear combinations have zero coefficient on every component of
`g` and `G`.  Thus the existing root-polarization mechanism cannot expose
the Euler--Hessian response jets in the active odd-root `P_5` and `P_7`
branches.

Nonlinear target equations can relate an observed odd-depth cofactor to an
unobserved even-depth deck; Theorem 5 does not prohibit such an additional
identity.  It proves that the deck is not a root-word selector output.

## 5. The parity-compatible four-root/P6 boundary

For `r=4`, Theorem 5 gives

```text
|D|=2:
Omega_D=sum_({i,j} subset R) L_ij
  per H_(R\{i,j},D),

|D|=4:
Omega_D=per H_(R,D).                                  (23)
```

Thus a first response deck is carried by one root--root shore and a
two-root permanental fan.  A second response deck is carried by the
four-root permanental incidence compound.  These are genuine physical
mixed-root coefficients.

### Corollary 7 (the active two-residual P6 selector)

For `Q={p,q}`, the response is simply

```text
Lambda_Q=a_pq U+T_pq,              Lambda_empty=U.   (24)
```

If a legal four-root coefficient selector isolates the deletion column
`D={p,q}` with `Omega_D!=0`, it exposes a nonzero scalar multiple of `U`.
After dividing by that known shore scalar,

```text
U=Lambda_empty,              T_pq=Lambda_Q-a_pq U.   (25)
```

Thus the two-residual P6 cell needs no Hessian inverse: one synchronized
pure response deck exactly separates the direct aggregate from the honest
two-row permanent channel.  If the selected target coefficients put both
tensors in the diagonal target and `T_pq` has three nonzero colours, this is
an honest `P_6 -> Delta_3` restriction and forces strict support at least
`21`.

One transparent sufficient graph-side chart has one nonzero root--root shore
on a chosen root pair, a nonzero `2 x 2` permanent from the other two roots
to `p,q`, and every competing deletion column either zero or independently
subtracted.  The existing zero-root--root P6 four-hafnian chart cannot use
this selector: setting all root--root blocks to zero kills every depth-two
weight in the first line of (23).  Whether a nonzero diagonal target forces
a compatible depth-two selector is **UNKNOWN**.

Consider a clean four-residual window and one selected nonzero root--root
shore.  Let the two residual-active root polarization spaces have dimensions
`a,b`, with incidence matrices `A in K^(a x 4)` and `B in K^(b x 4)`.  The
six pair-deletion tensors are observed through the `ab x 6` matrix

```text
K(A,B)_(uv)=a_u tensor b_v+a_v tensor b_u.            (26)
```

This is the mixed permanental fan.  It recovers all six faces exactly when
`rank K(A,B)=6`, and necessarily `ab>=6`.

### Theorem 8 (sharp `2 x 3` first-deck tomography)

A `2 x 2` polar sector has rank at most four and cannot recover the deck.
The bound `ab>=6` is sharp in three-dimensional local spaces.  Take

```text
A=[1 0 1 1]              B=[1 0 0 0]
  [0 1 0 1],               [0 1 0 0]
                            [0 0 1 0].                (27)
```

In pair order `12,13,14,23,24,34`, the determinant of the `6 x 6` matrix
`K(A,B)` is

```text
det K(A,B)=-2.                                        (28)
```

Hence this clean polarized sector recovers every two-deletion tensor.  If
the compatible four-root permanent in (23) is nonzero, it also exposes the
unique four-deletion tensor on this window.  Theorem 3 then performs complete
channel unmixing.  Indeed, at `q=4` the edge Hessian is the complement
permutation

```text
12 <-> 34,          13 <-> 24,          14 <-> 23,
D^2=I_6,            det D=-1.                              (29)
```

It is invertible at every residual graph, not merely generically.  Since the
four-deletion response is `Lambda_empty=U`, the recovery simplifies to

```text
U=Lambda_empty,             T=D(g-cU).                    (30)
```

When `h!=0`, the top and the first deck already suffice by (16).

### Proof

The rank upper bound is the row count `ab`.  Substituting (27) into (26) and
expanding the fixed determinant gives (28), so full rank is attained.
Nonvanishing of the four-root coefficient in (23) leaves a nonzero scalar
multiple of the unique response with all four residual vertices deleted.

The word **clean** includes all legality obligations: the chosen root--root
grade must be isolated, root--blocker and mixed residual--blocker nuisance
columns must vanish or be independently subtracted, all observations must
share the same shore normalization, and the target equality must supply the
corresponding coefficient tensors.  The theorem proves the exact observation
matrix once those physical conditions hold.  It does not assert that an
arbitrary `P_6` witness contains such a chart.

## 6. Translation to neighboring structures

Three familiar mathematical languages clarify what has happened.

1. In square-free apolarity, a matching monomial in edge derivatives
   contracts its covered vertices.  Theorem 1 is exactly that apolar action
   on the matching polynomial, lifted to a tensor-valued response.  Its
   matching-independence is why the apparent second edge jet collapses to a
   much smaller four-vertex deck.
2. The mixed-root filtration has a genuine `Z/2` grading.  Root--root edges
   remove roots in pairs, so the parity of every deletion depth equals the
   parity of the root count.  Corollary 6 is therefore a superselection rule,
   not an observation-capacity estimate.
3. Formula (4) is a boundary-signature or connection-matrix entry: adjoining
   zero-coupled deletion vertices to the root graph turns the legal selector
   weight into one augmented hafnian.  The matrix of these `Omega_D` over
   chosen polarizations is the exact observability matrix.  P6 succeeds on a
   chart precisely when that matrix has the required column rank.

The affine fibre of Theorem 4 is the complementary algebraic-statistical
statement: the parameter-to-top-tensor map is nonidentifiable in a direction
on which the deletion observable is nonconstant.  No postprocessing of the
top tensor can remove that fibre without extra target equations or a new
physical measurement.

These translations use standard languages, but the combined
**principal-deletion response jet** and augmented-hafnian legality criterion
are definitions local to this proof package; no claim of established
terminology is made.

## 7. Consequences for blocker surplus

For the common-cofactor blocker aggregate (8), a legally exposed deck gives
honest coefficients rather than formal derivatives:

```text
two-deletion deck + top, h!=0
  -> recover U and every T_e;

two- and four-deletion decks, arbitrary h
  -> recover U and every T_e;

full-diagonal recovered T_e
  -> honest P_(r+2) -> Delta_3
  -> strict support at least 3r+9.                    (31)
```

On a singular Hessian fibre, (3) is already an exact target-valued relation
among physical pair-deletion tensors.  It can be tested without inverting
`D`.  This is the strongest unconditional obstruction furnished by the
response connection; its application to a top Krenn restriction still
requires legal deck exposure or an independently proved target relation.

## Scope wall

```text
edge-response jet = principal two-deletion deck:        PROVED;
second response jet = principal four-deletion deck:     PROVED;
higher matching derivative = named deletion deck:       PROVED;
four-set equality and reduced second-jet data count:     PROVED;
Euler--Hessian recovery from physical decks:             EXACT;
singular adj(D) relation on physical two-deletion deck:  EXACT;
top tensor universally determines pair deletion:        FALSE;
local polarizations/finite differences simulate vacuum: FALSE;
root-deletion weight Omega_D as augmented hafnian:       PROVED;
odd-root response shore exposes any even deck:           FALSE;
P5/P7 root-polarization exposure of g,G:                 RULED OUT;
four-root/P6 parity compatibility:                       PROVED;
two-residual P6 deck selector unmixes U,T:                CONDITIONAL EXACT;
zero-root--root P6 H4 chart exposes the pure deck:        FALSE;
clean 2x2 first-deck fan suffices on four vertices:      FALSE;
clean 2x3 first-deck fan can be invertible:              PROVED;
clean compatible P6 chart forced in every witness:       UNKNOWN;
target-specific nonlinear odd/even depth identity:       UNKNOWN;
legal herald or independently exposed deletion deck:     UNKNOWN;
unrestricted P5/P6/P7 obstruction:                      UNKNOWN;
global Krenn--Gu:                                         UNRESOLVED.       (32)
```

## Replay

Run from the repository root:

```powershell
uv run --with sympy python verify_response_jet_principal_deletion_deck_and_root_parity_legality.py
python audit_response_jet_principal_deletion_deck_and_root_parity_legality.py
python -m py_compile verify_response_jet_principal_deletion_deck_and_root_parity_legality.py audit_response_jet_principal_deletion_deck_and_root_parity_legality.py
uv run --with ruff ruff check verify_response_jet_principal_deletion_deck_and_root_parity_legality.py audit_response_jet_principal_deletion_deck_and_root_parity_legality.py
```

The primary verifier checks the symbolic six-residual response against every
two-deletion and four-deletion derivative, the augmented-hafnian formulas at
root order four, the odd-root zero, the determinant `-2`, and the nonzero
pair-vacuum fibre.  The independent no-import audit uses separately written
integer hafnian/permanent recurrences, response-deck evaluation, fraction-free
determinants, and the same displayed certificates.  Neither script imports
the other or searches graphs, supports, words, matchings, fields, or
parameter tuples.

Dependencies:

- [`ARBITRARY_ORDER_HAFNIAN_EULER_HESSIAN_CHANNEL_UNMIXING_AND_SINGULAR_DISCRIMINANT.md`](ARBITRARY_ORDER_HAFNIAN_EULER_HESSIAN_CHANNEL_UNMIXING_AND_SINGULAR_DISCRIMINANT.md)
- [`MIXED_ROOT_DELETION_FILTRATION_AND_HERALD_FREE_PAIR_NO_GO.md`](MIXED_ROOT_DELETION_FILTRATION_AND_HERALD_FREE_PAIR_NO_GO.md)
- [`NONPROJECTIVE_ROOT_PAIR_FAN_SELECTOR_TOMOGRAPHY_THEOREM.md`](NONPROJECTIVE_ROOT_PAIR_FAN_SELECTOR_TOMOGRAPHY_THEOREM.md)
- [`P6_FOUR_ROOT_FULL_H4_SENSOR_AND_TARGET_INCIDENCE_BOUNDARY.md`](P6_FOUR_ROOT_FULL_H4_SENSOR_AND_TARGET_INCIDENCE_BOUNDARY.md)
