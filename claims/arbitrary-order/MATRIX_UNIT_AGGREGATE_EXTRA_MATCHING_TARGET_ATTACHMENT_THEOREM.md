# Matrix-unit aggregate extra-matching target attachment theorem

## Status

This is an exact arbitrary-order characteristic-zero refinement of the live
`U7J -> U7` obligation in the complete nonzero `r=1` matrix-unit branch.
It traces one **offdiagonal** extra matching in an aggregate active-cycle
fibre through the complete target equations.

There is an exhaustive attachment theorem.  Let `X` be such an extra matching
at an active word `chi`, and let `E` be its nonempty offdiagonal core.

1. If a residual pure shore of `X` cancels, then a conformally minimal zero
   inside that shore is a connected matching-covered core.  It is either a
   primitive pure cycle, a sparse conformal fan, or has a nonzero aggregate
   port.  Every matching term of that exact pure relation extends by the
   fixed edges of `X` into the **same mixed target fibre**.  Matching-exponent
   differences are preserved exactly.  This supplies the previously missing
   matrix-unit attachment between the pure structure and mixed response.
2. If every residual shore is nonzero, `E` is cofactor-active.  Its imported
   bridge normalization either enters the deeper-blocker branch or produces
   a nonzero diagonal matching at another mixed word `psi`.
3. At `psi`, a zero pure shore again gives the attached pure relation above.
   If all three shores are nonzero, the complete target equation forces
   nonzero mixed response at `psi`; thus `psi` is active.

Choose a shortest active transport cycle.  An active `psi` produced by an
extra matching is either outside that cycle or is exactly the selected
successor.  The latter **parallel-successor** case cannot be removed.  There
is an exact complete, locally concise ten-vertex family over `Q(t)` with:

```text
all three pure target coefficients:              1;
complete active-cycle fibre sizes:               3,2,2;
one offdiagonal extra matching:                   YES;
its residual shore hafnians:                      all nonzero;
its forced bridge output:                         the selected successor term;
new target-fibre lattice direction at successor:  zero;
H:                                                -1/(1+t).
```

The family is the smallest even-order pure-anchor completion of its exact
eight-vertex parallel template.  Its selected cycle plus the three pure
anchors has zero holonomy elimination.  The **complete** target system does
exclude the support: the mixed word `0011111122` has one matching term of
weight one, hence gives a Laurent unit.

Thus the new result proves a genuine pure-to-mixed attachment whenever the
extra matching meets a cancelling shore, and it forces the remaining
offdiagonal case into deeper data, another active target equation, or an
exact parallel bridge.  It does **not** prove that every attachment gives a
unit, useful non-direct overlap, or killed quotient sheets.  Purely diagonal
aggregate excess also remains outside the theorem.  The `r=1` branch and the
global Krenn--Gu conjecture remain **UNKNOWN/UNRESOLVED**.

## 1. Active fibre and one extra matching

Work over `C` at a hypothetical complete nonzero `r=1` matrix-unit witness.
Let `chi` be one word on an imported active transport cycle.  Put

```text
V_c={v:chi(v)=c},                  c=0,1,2.          (1)
```

Every `|V_c|` is even.  Let `X` be a compatible perfect matching in the
complete fibre of `chi`, distinct from the selected incoming and outgoing
terms.  Split it uniquely as

```text
X=E union P_0 union P_1 union P_2,                  (2)
```

where `E` is the set of offdiagonal edges and `P_c` is a pure-`c` perfect
matching on

```text
S_c=V_c-partial_c E.                                (3)
```

The theorem concerns the case `E` nonempty.  Each `P_c` is a nonzero physical
matching term, but its full shore hafnian

```text
h_c(S_c)=haf(Z^c[S_c])                              (4)
```

may vanish by cancellation.

## 2. Conformally minimal pure residuals

The ordinary least-residual theorem chooses a least zero without remembering
whether it can be completed inside the shore from which it came.  The extra
matching supplies exactly the missing completion condition.

Let `Z=(z_uv)` be a hollow symmetric scalar matrix on a finite even set `S`.
Assume

```text
h(S)=haf(Z[S])=0                                    (5)
```

although the support on `S` has a perfect matching.  Call an even set
`R subset S` **conformally admissible** when

```text
h(R)=0;
the support on R has a perfect matching;
the support on S-R has a perfect matching.          (6)
```

The set `S` itself is admissible, with the empty matching on its complement.
Choose an admissible `R` of least cardinality.  For `uv subset R`, put

```text
C_uv=z_uv h(R-{u,v}).                               (7)
```

### Theorem 1 (conformally minimal allowed core)

The graph

```text
A_R={uv:C_uv!=0}                                    (8)
```

is exactly the union of all support perfect matchings on `R`.  It is
connected, matching-covered, and has minimum degree at least two.

Consequently exactly one of the following holds.

1. `A_R` is one even cycle.  It has exactly two perfect matchings and gives
   one primitive signed Laurent binomial.
2. `A_R` branches.  At every branch vertex its perfect matchings partition
   into nonzero cofactor ports.  If every port is a singleton, the matchings
   form the imported sparse conformal fan and one exact `d`-nomial relation.
   Otherwise at least one port is a nonzero aggregate.

### Proof

Let `uv` be allowed, and choose a support perfect matching of `R` containing
it.  Deleting `uv` leaves a support perfect matching on `R-{u,v}`.  If

```text
h(R-{u,v})=0,                                       (9)
```

then `R-{u,v}` would also be conformally admissible: a fixed support matching
on `S-R`, together with the edge `uv`, is a support perfect matching on

```text
S-(R-{u,v}).                                        (10)
```

This contradicts minimality.  Hence every allowed edge has nonzero first
cofactor and belongs to `A_R`.

Conversely, if `C_uv!=0`, then `uv` is a support edge and the nonzero hafnian
on `R-{u,v}` contains a support perfect matching.  Adjoining `uv` proves that
the edge is allowed.  This proves the allowed-core identity.

Let `R_1,...,R_s` be the connected components of `A_R`.  Every support
perfect matching stays inside them, and each component supports the
restriction of a fixed perfect matching.  Therefore

```text
h(R)=product_q h(R_q).                              (11)
```

Some factor vanishes.  If `s>1`, that `R_q` is a smaller conformally
admissible zero: the other components and `S-R` supply a support perfect
matching of its complement in `S`.  This is impossible, so `s=1`.

At a vertex `v`, hafnian Laplace expansion gives

```text
sum_(uv in A_R) C_uv=h(R)=0.                        (12)
```

Every vertex lies in an allowed perfect matching and therefore has at least
one nonzero incident cofactor.  It cannot have exactly one, by (12).  Hence
the minimum degree is at least two.

The allowed-core, connectedness, and minimum-degree statements are exactly
the hypotheses used by the imported matching-covered single-cycle and
cofactor-port theorems.  Their alternating-cycle, sparse-fan, and aggregate-
port proofs now apply to `A_R`.  No stronger minimality was used in those
steps.  QED.

The theorem works over every field in which the imported port theorem works,
in particular over `C`.  Characteristic two is excluded in the signed
cycle/fan interpretation.

## 3. Exact extension into one mixed target fibre

Fix one support perfect matching `C` on `S-R`.  Let `K` be any fixed nonzero
matching on vertices disjoint from `S`, chosen so that every union below is a
full physical matching inducing one word.

### Corollary 2 (termwise mixed-fibre attachment)

For every support perfect matching `M` of `R`, put

```text
M_hat=K union C union M.                             (13)
```

Then all `M_hat` lie in the same complete target fibre, the map
`M -> M_hat` is injective, and

```text
sum_M lambda(M_hat)
 =lambda(K)lambda(C)h(R)=0.                         (14)
```

For any two residual matchings `M,N`, one also has the exact exponent identity

```text
1_(M_hat)-1_(N_hat)=1_M-1_N.                        (15)
```

Thus a primitive pure-cycle character, every sparse-fan character, and every
aggregate-port partition occurs term for term inside that mixed fibre.  This
is lattice interaction through identical matching differences, not an
observation that the two constructions share physical variables.

### Proof

The three matchings in (13) use disjoint vertex sets.  Their union is
therefore a full perfect matching, and the fixed parts give every union the
same endpoint-label word.  Matching weights multiply, proving (14).
Cancellation of the common incidence vectors `1_K+1_C` proves (15).  QED.

Equation (14) is an exact additional zero subrelation on this cancellation
branch.  It is not silently promoted to a universal generator of the target
ideal away from that branch.

## 4. Offdiagonal aggregate-extra attachment

Return to (1)--(4).

### Theorem 3 (extra-matching target attachment)

For every compatible extra matching `X` with `E` nonempty, at least one of
the following holds.

```text
source pure attachment:
    some h_c(S_c)=0, and Theorem 1 plus Corollary 2 embeds a primitive
    pure cycle, sparse fan, or aggregate port into the fibre of chi;

deeper attachment:
    some bridge square or hexagon selected for E enters the imported
    deeper-blocker component;

target pure attachment:
    bridge normalization produces a word psi whose diagonal matching is
    nonzero but whose diagonal aggregate D_psi vanishes; a conformally
    minimal pure residual embeds into the diagonal subfibre at psi;

active target attachment:
    D_psi!=0, and the complete mixed target equation forces
    Q_psi=-D_psi!=0.                                 (16)
```

In the last case `psi` is another active synchronized word with the same
three colour multiplicities as `chi`.

### Proof

If some value in (4) vanishes, the actual matching `P_c` proves that the
shore support is matchable.  Apply Theorem 1 with `S=S_c`.  In Corollary 2,
take `K` to be `E`, the fixed matchings `P_d` for `d!=c`, and the fixed
completion inside `S_c-R`.  Every extended term induces `chi`, proving the
first case.

Suppose now that every value in (4) is nonzero.  Then `E` is cofactor-active
in the exact sense of the imported active-word response theorem.  Its three
cross-type counts have one parity, so its edges partition into bridge squares
and at most one bridge hexagon.  A selected block may enter the deeper
component, giving the second case.

Absent that outcome, the imported bridge theorem produces a nonzero diagonal
matching `B(E)` on the endpoints of `E`.  The union

```text
Y=B(E) union P_0 union P_1 union P_2                (17)
```

is a nonzero diagonal matching at a word `psi!=chi` with the same colour
multiplicities.  If `D_psi=0`, at least one pure shore hafnian at `psi`
vanishes despite containing the matching term supplied by `Y`.  Apply
Theorem 1 and Corollary 2 inside that shore, fixing all other edges of `Y`.
This is the target pure-attachment case.

Finally suppose `D_psi!=0`.  The word is mixed because bridge normalization
preserves the multiplicity vector of the mixed word `chi`.  Its complete
target coefficient is zero, so

```text
D_psi+Q_psi=0.                                      (18)
```

This gives the last line of (16).  The cases are exhaustive.  QED.

This theorem uses the complete equation at the bridge word.  It does not
multiply aggregate cycle equations or divide by an aggregate sum.

## 5. Shortest-cycle consequence and parallel boundary

Form the finite directed transport graph whose vertices are active words of
one fixed multiplicity and whose no-deeper, noncancelling bridge steps are
arcs.  Choose a directed cycle

```text
chi_0 -> chi_1 -> ... -> chi_(m-1) -> chi_0          (19)
```

of minimum length.  At `chi_i`, write the selected outgoing and successor
matchings as

```text
F_i=E_i union P_i,
G_i=B(E_i) union P_i.                               (20)
```

### Corollary 4 (outside or parallel)

Suppose an extra matching `X` at `chi_i` reaches the active-target case of
Theorem 3, with bridge output `Y` at `psi`.  Then exactly one of the following
holds.

1. `psi` is outside the selected cycle; the extra matching has exposed a
   complete target equation outside the cycle.
2. `psi=chi_(i+1)`; the extra matching is a parallel successor route.

### Proof

The bridge changes the word on a nonempty endpoint set, so `psi!=chi_i`.  If
`psi=chi_j` lies on (19), join the extra arc `chi_i -> chi_j` to the selected
directed path from `chi_j` back to `chi_i`.  Unless `j=i+1` cyclically, this
is a directed cycle shorter than (19), contradicting minimality.  QED.

In the parallel case put

```text
u=1_X-1_(F_i) in L_(chi_i),
v=1_Y-1_(G_i) in L_(chi_(i+1)).                     (21)
```

Both are exact within-fibre differences in the universal endpoint-character
kernel.  Useful non-direct cross-fibre overlap is an additional condition on
the lattices generated by `u`, `v`, and the remaining target terms.  It is
not forced by parallel transport.  In particular, `Y` may equal `G_i`, in
which case

```text
u!=0,                 v=0.                          (22)
```

The next section realizes (22) while retaining all three pure target
coefficients.

## 6. Pure-anchor-compatible parallel sharpness

Use vertices `0,...,9`, parameter `t`, and

```text
t!=0,                    1+t!=0,
x=-(1+t).                                             (23)
```

The three cycle words are

```text
chi_0=0000111122,
chi_1=0011001122,
chi_2=0101010122.                                   (24)
```

For a physical pair `uv`, the notation `uv:ab:w` means endpoint labels
`(a,b)` in increasing vertex order and scalar weight `w`.  The complete old
eight-vertex part is

```text
01:00:1   02:00:1   03:00:1   04:00:1
05:22:1   06:11:1   07:22:1
12:01:-1  13:00:1   14:10:-1  15:11:1  16:22:1  17:00:1
23:11:1   24:01:x   25:01:t   26:00:1  27:20:1
34:01:1   35:01:1   36:10:1   37:11:1
45:00:1   46:11:1   47:22:1
56:01:1   57:11:1   67:11:1.                         (25)
```

The remaining seventeen pairs are

```text
08:11:1   18:20:1   28:22:1   38:00:1
48:20:1   58:20:1   68:20:1   78:20:1

09:00:1   19:11:1   29:21:1   39:22:1
49:21:1   59:21:1   69:21:1   79:21:1

89:22:1.                                               (26)
```

Every physical pair carries one nonzero matrix unit.  At each vertex, the
incident endpoint labels are exactly `{0,1,2}`.

### Theorem 5 (exact `3/2/2` parallel family)

The complete fibres of (24) are exactly

```text
chi_0:
  01|24|35|67|89     weight x       selected F_0,
  01|25|34|67|89     weight t       extra X,
  02|13|46|57|89     weight 1       incoming G_2;

chi_1:
  01|23|45|67|89     weight 1       incoming G_0,
  04|12|37|56|89     weight -1      selected F_1;

chi_2:
  02|14|36|57|89     weight -1      selected F_2,
  04|15|26|37|89     weight 1       incoming G_1.     (27)
```

All three fibre sums vanish.  The pure fibres are the singletons

```text
0^10: 09|17|26|38|45     weight 1,
1^10: 08|19|23|46|57     weight 1,
2^10: 05|16|28|39|47     weight 1.                  (28)
```

The extra term has cross core

```text
E={25,34}                                             (29)
```

and residual shore matching `01|67|89`.  Its three residual hafnians are all
one.  The no-deeper bridge square is

```text
25|34  ->  23|45,                                   (30)
```

because `23` has labels `11` and `45` has labels `00`.  Its bridge output is

```text
01|23|45|67|89=G_0.                                 (31)
```

Thus (22) holds exactly.

The selected holonomy and aggregate defect are

```text
H=1/x=-1/(1+t),
A_0=t/x=-t/(1+t),              A_1=A_2=0,           (32)
```

and

```text
H=(-1)^3(1+A_0).                                    (33)
```

### Proof

There are `9!!=945` perfect matchings on ten labelled vertices.  Exact
matching-first enumeration gives precisely (27)--(28).  The first cycle sum
is `x+t+1=0`, and the other two sums are `1-1=0`.  Every pure singleton has
weight one.

The label check in (29)--(31) proves the parallel bridge statement.  All
selected incoming products are one; the outgoing products are `x,-1,-1`.
This gives (32), and direct substitution gives (33).  QED.

### Smallest completion of the fixed parallel template

Delete vertices `8,9` and the common edge `89` from (27).  The physical pairs
not used by any of the resulting `3/2/2` fibre terms are exactly

```text
03,05,06,07,16,17,27,47.                            (34)
```

Every edge labelled `22` must lie in this unused graph because the three
cycle words use only labels zero and one on the old vertices.  But vertex `2`
has only unused neighbour `7`, and vertex `4` also has only unused neighbour
`7`.  Hence (34) has no perfect matching and the pure-`2` target cannot be
retained on the same eight vertices.  An extension must preserve even order,
so at least two vertices are necessary.  Equations (26)--(28) show that two
are sufficient.  This proves minimality only as a completion of the exact
parallel template, not among all possible matrix-unit supports.

## 7. Exact holonomy boundary and the complete-target unit

Before substituting (23), use independent Laurent variables `x,t,H` and the
two equations

```text
1+x+t=0,
Hx-1=0.                                             (35)
```

The quotient maps to `Q(t)` by

```text
x |-> -(1+t),
H |-> -1/(1+t).                                     (36)
```

The image of `H` is nonconstant, so the induced map from `Q[H,H^(-1)]` is
injective.  Therefore the selected cycle equations, even together with the
three pure singleton equations (28), have zero elimination ideal in `H`.
Indeed, the displayed one-parameter assignment satisfies all six equations
identically while `H` remains a nonconstant rational function.

This does not survive the complete target block.  The mixed word

```text
omega=0011111122                                    (37)
```

has the unique matching

```text
01|23|46|57|89                                      (38)
```

of weight one.  Its target-zero residual is one Laurent monomial, a unit in
the physical Laurent ring.  Hence the complete target ideal of this fixed
support is `(1)`.  The family is not a witness and is not an apparent
counterexample.

The exact lesson is narrower.  Pure anchors do not by themselves constrain
the aggregate defect, and a parallel bridge can contribute no new successor-
fibre lattice direction.  In this support an equation farther outside the
cycle supplies the unit, but no arbitrary-order theorem yet forces that
outcome.

## 8. Consequence for the live `U7` edge

The offdiagonal aggregate-extra branch now has the exact decision tree

```text
extra offdiagonal matching X
    -> cancelling source shore
         -> conformally minimal primitive cycle / sparse fan / aggregate port
            embedded termwise in the cycle fibre;

    -> all source shores nonzero
         -> deeper blocker,
         -> cancelling target shore with the same exact attachment,
         -> active target word outside a shortest cycle,
         -> or parallel successor route.             (39)
```

This is genuine progress on `U7J -> U7`: the pure-cancellation alternatives
are no longer merely adjacent nodes in the proof forest.  When they are
created by an aggregate extra matching, their exact characters occur inside
the relevant mixed target fibre.

The sharpness family corrects the stronger proposed mechanism.  Shortest-
cycle minimality does not force every extra matching outside the cycle, and
parallel bridge reuse does not force a nonzero second-fibre difference.  To
close the surviving branch, a later theorem must do at least one of the
following without relying on physical-variable overlap alone:

1. turn the attached pure relation into an odd dependency or another unit
   certificate;
2. prove genuine non-direct overlap with additional target fibres and kill
   every quotient sheet;
3. force an outside singleton or another exact unit as in (37)--(38);
4. control parallel successor pairs when `Y!=G_i`;
5. treat aggregate excess consisting only of diagonal matchings; or
6. close the deeper-blocker branch.

No item in this list is claimed here.

## 9. Assumptions and exact boundary

```text
field for the matrix-unit theorem:                    C;
physical branch:                                      complete nonzero r=1 matrix units;
target hypothesis:                                    complete GHZ equations at the hypothetical witness;
cycle input:                                          imported active transport cycle;
extra term:                                           compatible matching with nonempty offdiagonal core;
conformally minimal allowed-core theorem:              PROVED;
primitive cycle / sparse fan / aggregate port:         PROVED by exact imported consequences;
termwise pure-to-mixed extension:                      PROVED;
deeper / pure attachment / active target trichotomy:   PROVED EXHAUSTIVE;
shortest-cycle outside-or-parallel alternative:        PROVED;
ten-vertex complete locally concise family:            PROVED over Q(t), t(1+t)!=0;
all three pure target coefficients in family:          EXACTLY 1;
parallel successor target difference in family:        ZERO;
selected holonomy elimination in family:               ZERO IDEAL;
complete target ideal of family:                       UNIT by singleton omega;
family a Krenn--Gu witness:                            NO;
purely diagonal aggregate excess:                      OUTSIDE THIS THEOREM;
parallel/external active attachment forced to a unit:  UNKNOWN;
useful non-direct overlap forced:                       UNKNOWN;
all quotient sheets killed:                            UNKNOWN;
deeper-blocker branch excluded:                        UNKNOWN;
general r=1 branch excluded:                           UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.
```

The pure residual relation is exact at the hypothetical witness and defines
a valid branch equation.  It is not asserted to be a formal consequence of
the GHZ target generators for every point of the fixed label-support torus.
No aggregate sum, shore hafnian, or defect is divided out.

## 10. Evidence and replay

Run:

```powershell
python claims/arbitrary-order/verify_matrix_unit_aggregate_extra_matching_target_attachment.py
python claims/arbitrary-order/audit_matrix_unit_aggregate_extra_matching_target_attachment.py
python -m py_compile claims/arbitrary-order/verify_matrix_unit_aggregate_extra_matching_target_attachment.py claims/arbitrary-order/audit_matrix_unit_aggregate_extra_matching_target_attachment.py
python -m ruff check claims/arbitrary-order/verify_matrix_unit_aggregate_extra_matching_target_attachment.py claims/arbitrary-order/audit_matrix_unit_aggregate_extra_matching_target_attachment.py
```

The primary verifier uses exact SymPy coefficient arithmetic, a complete
matching-first census of all `945` ten-vertex perfect matchings, exact shore
hafnians, endpoint-character differences, and a small Groebner elimination.
It checks the complete `3/2/2` cycle fibres, all three pure singleton targets,
the parallel bridge, the zero successor difference, the outside singleton
unit, the order-eight completion obstruction, and conformally minimal cycle,
sparse-fan, and aggregate-port fixtures.

The independent audit imports no repository module and no symbolic algebra
package.  It uses 45-bit physical matching masks, custom exact polynomial
coefficient tuples, a separate last-vertex pure-matching recursion, different
conformal residual weights, exact Gaussian ranks for the triangular
holonomy-substitution map, and an independent order-eight obstruction check.
The arbitrary-order result is the written minimality, completion, bridge, and
shortest-cycle proof above; the scripts audit the mechanisms and exact
sharpness family rather than claiming a global case census.
