# Matrix-unit parity-fibre factorization and active word-shore synchronization

## Status

This is an exact characteristic-zero refinement of the `r=1` matrix-unit
branch.  Split every parity-zero coefficient into completely diagonal and
offdiagonal matching sectors.  For a word `chi`, the diagonal sector factors
exactly over its three colour shores:

```text
D_chi = product_(c=0)^2 haf(Z^c[V_c]),
V_c={v:chi(v)=c}.                                    (1)
```

If `chi` is mixed and the full graph tensor is `Delta_(n,3)`, then

```text
Q_chi = -D_chi,                                      (2)
```

where `Q_chi` is the sum of all compatible matchings using at least one
offdiagonal unit.  Consequently every fibre with `Q_chi!=0` already has a
nonzero pure hafnian, hence a perfect matching, on **every** word shore.
This supplies an exact word-preserving global rematching for every active
offdiagonal fibre; no bridge-by-bridge word preservation is needed.

Conversely, a word-shore Tutte failure forces `D_chi=Q_chi=0`.  Thus the
six-vertex relay mechanism with no word-conformal matching can occur only in
an internally cancelling zero fibre.  It cannot carry a nonzero coordinate
of the offdiagonal parity tensor in a hypothetical witness.

In a support-minimal matrix-unit witness with at least one offdiagonal unit,
the upstream erasure theorem gives `Q_off!=0`.  Hence at least one mixed
parity-zero word has all three shore hafnians nonzero and satisfies the exact
nonzero scalar cancellation (2).  The remaining obligation is to exclude or
structurally use that aggregate cancellation.  The theorem does not prove
that every matching-induced word has shore matchings, match individual
offdiagonal terms weight-preservingly, or exclude the `r=1` branch.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Matrix-unit and parity-fibre notation

Let `Omega` have even cardinality `n>=6`.  In the maximum-one branch every
physical pair `uv` carries one nonzero matrix unit

```text
W_uv=lambda_uv e_(ell_u(uv))^* tensor e_(ell_v(uv))^*,
lambda_uv!=0.                                        (3)
```

Call `uv` **diagonal** if its endpoint labels agree, and offdiagonal
otherwise.  For each colour `c`, let `Z^c` be the scalar adjacency matrix of
the pure `(c,c)` units, with zero on every other pair.

Fix a coordinate word `chi`.  Put

```text
V_c=chi^(-1)(c).                                     (4)
```

Let `D_chi` be the weighted sum of all completely diagonal perfect matchings
inducing `chi`, and let `Q_chi` be the weighted sum of all other perfect
matchings inducing `chi`.  Thus

```text
[T_W]_chi=D_chi+Q_chi.                               (5)
```

Odd and empty hafnians have their standard values zero and one.

## 2. Exact diagonal-shore factorization

### Theorem 1

For every word `chi`, equation (1) holds.

### Proof

A diagonal edge has the same colour at both endpoints.  Therefore a
completely diagonal matching inducing `chi` never crosses between distinct
sets `V_c`; it restricts to one pure-`c` perfect matching on each `V_c`.

Conversely, the union of one pure-`c` matching on each `V_c` is a completely
diagonal perfect matching inducing `chi`.  This is a weight-preserving
bijection

```text
{diagonal matchings inducing chi}
  <-> product_c {pure-c matchings on V_c}.            (6)
```

Summing products over the Cartesian product in (6) factors into the product
of the three principal hafnians, proving (1).  No genericity or absence of
cancellation inside an individual shore is assumed.

### Corollary 2 (parity support)

If any `|V_c|` is odd, then `D_chi=0`.  In particular the diagonal sector is
supported only on colour-count parity `000`.

This is a support statement.  Even shore sizes do not by themselves make a
shore hafnian nonzero.

## 3. Active fibres synchronize globally

Assume now

```text
T_W=Delta_(n,3).                                     (7)
```

### Theorem 3 (active-fibre synchronization)

For every mixed word `chi`, equation (2) holds.  Moreover the following are
equivalent:

```text
Q_chi != 0;
D_chi != 0;
haf(Z^c[V_c]) != 0 for every c.                      (8)
```

Whenever these conditions hold, every induced pure support graph
`G_c[V_c]` has a perfect matching and satisfies Tutte's one-factor
inequalities.

### Proof

The target coefficient of a mixed word is zero, so (5) immediately gives
(2).  Over `C`, the product (1) is nonzero if and only if each of its three
factors is nonzero.  This proves (8).

A nonzero hafnian contains at least one nonzero matching monomial.  Hence
each `G_c[V_c]` has a perfect matching.  The union of any three such
matchings is a completely diagonal matching inducing the exact original
word `chi`.  Tutte's inequalities are equivalent to the existence of those
shore matchings.

The conclusion is stronger than support existence: each weighted shore
hafnian is nonzero.  The converse support implication is deliberately not
claimed, because different pure matchings inside a shore may cancel.

### Corollary 4 (location of every Tutte failure)

If some `G_c[V_c]` has no perfect matching, then

```text
D_chi=Q_chi=0.                                      (9)
```

Thus every compatible offdiagonal matching in that word fibre, if any,
cancels internally with other offdiagonal matchings.  A missing shore
matching cannot occur in a nonzero coordinate of `Q_off`.

The reverse implication is false in general: `Q_chi=0` may result from
weighted cancellation even when every shore has matchings.

## 4. Support-minimal consequence

Let

```text
Q_off=sum_(chi of parity 000) Q_chi e_chi             (10)
```

be the parity-zero offdiagonal tensor from the imported cross-parity
decomposition.  Constant words receive no contribution from `Q_off`, since
an offdiagonal edge already gives two different endpoint colours.

### Theorem 5 (existence of an active synchronized word)

Suppose a support-minimal hypothetical witness lies in the `r=1`
matrix-unit branch and contains an offdiagonal unit.  Then there is a mixed
word `chi` of parity `000` such that

```text
0 != Q_chi
   = - product_c haf(Z^c[V_c]).                      (11)
```

In particular all three word shores have nonzero weighted perfect-matching
sums and their union gives a word-preserving diagonal rematching.

### Proof

The imported parity-erasure theorem proves `Q_off!=0`: otherwise deleting
all offdiagonal units would preserve `Delta_(n,3)` and strictly reduce
support.  Choose a nonzero coordinate `Q_chi`.  It cannot be constant by the
preceding observation.  Corollary 2 and equation (2) force parity `000`.
Theorem 3 then gives every assertion in (11).

This proof uses support minimality only to obtain some nonzero offdiagonal
fibre.  The fibre factorization and synchronization themselves hold for
every matrix-unit realization of (7), minimal or not.

## 5. Two exact sharpness tables

### 5.1 An active synchronized cancellation

On vertices `0,...,5`, use the following complete matrix-unit table.  Each
triple is `(label at the smaller endpoint, label at the larger endpoint;
weight)`:

```text
01=(2,1;+1)   02=(1,1;+1)   03=(0,1;+1)
04=(2,2;+1)   05=(0,0;+1)   12=(2,1;+1)
13=(2,2;+1)   14=(0,0;+1)   15=(1,1;+1)
23=(0,0;+1)   24=(0,2;+1)   25=(2,2;+1)
34=(1,1;+1)   35=(0,1;-1)   45=(0,2;+1).            (12)
```

The pure coefficients are all one, with unique matchings

```text
M_0=05|14|23,
M_1=02|15|34,
M_2=04|13|25.                                       (13)
```

For

```text
chi=(2,1,0,0,2,1),                                  (14)
```

the compatible graph is one alternating six-cycle.  Its two perfect
matchings are

```text
04|15|23,       diagonal,    weight +1,
01|24|35,       offdiagonal, weight -1.              (15)
```

Thus `D_chi=1`, `Q_chi=-1`, and the mixed target equation holds exactly at
this fibre.  Each two-vertex word shore is matched by the corresponding
edge in the first matching.

The table is not a witness.  For example the word

```text
(0,0,2,1,0,2)                                       (16)
```

has the unique compatible matching `03|14|25` of weight one.

### 5.2 An unsynchronized zero fibre

In the complete six-vertex gadget from the word-synchronization boundary,
the selected word

```text
(a,a,b,b,b,b)                                       (17)
```

has two offdiagonal compatible matchings of weights `+1` and `-1`, no
diagonal compatible matching, and hence

```text
D_chi=Q_chi=0.                                      (18)
```

That gadget realizes only one pure tensor and is not a witness.  It is the
sharp reason Theorem 3 cannot be strengthened from nonzero aggregate fibres
to every matching-induced word: support may be present inside a coordinate
whose total offdiagonal value is exactly zero.

## 6. Exact proof-topology boundary

The active-fibre result replaces the earlier broad synchronization target
by a narrower scalar obligation:

```text
diagonal contribution factors over exact word shores: PROVED;
nonzero offdiagonal fibre has every shore hafnian !=0: PROVED;
active fibre has an exact word-preserving rematching:  PROVED;
Tutte failure can carry a nonzero Q_off coordinate:    IMPOSSIBLE;
all matching-induced words have shore matchings:       NOT PROVED/NOT NEEDED;
individual bridge normalization preserves the word:    FALSE;
aggregate identity Q_chi=-product shore hafnians:      PROVED;
that nonzero aggregate cancellation is impossible:     UNKNOWN;
support-minimal r=1 matrix-unit branch excluded:        UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

The theorem does not compare an individual offdiagonal matching weight with
an individual diagonal matching weight.  It does not make a zero weighted
hafnian into a support obstruction, force every internally cancelling word
fibre to be empty, or enter the erased `r>=2` or deeper-blocker branches.

## Replay

```powershell
python claims/arbitrary-order/verify_matrix_unit_parity_fibre_diagonal_factorization_and_active_word_shore_synchronization.py
python claims/arbitrary-order/audit_matrix_unit_parity_fibre_diagonal_factorization_and_active_word_shore_synchronization.py
python -m py_compile claims/arbitrary-order/verify_matrix_unit_parity_fibre_diagonal_factorization_and_active_word_shore_synchronization.py claims/arbitrary-order/audit_matrix_unit_parity_fibre_diagonal_factorization_and_active_word_shore_synchronization.py
python -m ruff check claims/arbitrary-order/verify_matrix_unit_parity_fibre_diagonal_factorization_and_active_word_shore_synchronization.py claims/arbitrary-order/audit_matrix_unit_parity_fibre_diagonal_factorization_and_active_word_shore_synchronization.py
```

The primary verifier enumerates complete matrix-unit tables, checks (1) on
every word through eight vertices, and replays both six-vertex sharpness
fibres.  The independent no-import audit uses a separate bitmask hafnian and
matching partition, a different deterministic table family, and explicit
support tests.  These bounded checks audit conventions and examples; the
arbitrary-order proof is the matching bijection and target-coordinate
identity above.
