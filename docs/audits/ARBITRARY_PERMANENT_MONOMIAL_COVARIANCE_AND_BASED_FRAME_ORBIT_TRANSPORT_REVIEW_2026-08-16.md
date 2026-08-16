# Hostile review of permanent monomial covariance and based-frame transport

## Verdict and exact scope

**PASS, for the stated permanent-monomial covariance, based-frame
extendibility transport, and equality-five residual-orbit composition.**

The reviewed theorem proves that exact weighted `Delta_3` extendibility is
constant under the equivalences used by the based-frame census:

```text
one common coordinate monomial map in every source mode;
one common target-colour permutation;
independent nonzero colour scaling in the displayed two modes;
exchange of those two symmetric source modes.
```

Together with the frozen support synthesis, based-frame classification, and
displayed triangle/star/fixed full-extension exclusions, the exact remaining
equality-five extension-exclusion representatives are

```text
(4,1) pure star: 014;
(4,2) e=1:       025;
(4,2) e=2:       024.
```

The review found no covariance, inverse-transport, target-support,
mode-exchange, classification-composition, implementation-independence,
field, or scope blocker.

The residual representatives are not claimed to extend.  The theorem does
not address the dimension-at-least-six co-two sensor residual, does not close
unrestricted `P_6 -> Delta_3`, and does not resolve the Krenn--Gu conjecture.
The global status remains **UNRESOLVED**.

Reviewed LF-normalized frozen text bytes:

```text
theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_MONOMIAL_COVARIANCE_AND_BASED_FRAME_ORBIT_TRANSPORT_LEMMA.md
B1762F22813E5B749FF0C81DA6C6CE5E9B8E95601662D87CB21835AAF63C3DA0

primary verifier:
claims/arbitrary-order/verify_arbitrary_permanent_monomial_covariance_and_based_frame_orbit_transport.py
E37A2E98447F6058496A3487D0A01F498B331E730CC3B01C72FC6750CEC5838E

independent no-import audit:
claims/arbitrary-order/audit_arbitrary_permanent_monomial_covariance_and_based_frame_orbit_transport.py
1EC63510DB2E03A58D7502AAE7160310B4F324BFAD0547BB1E86A05A2602A740
```

### 2026-08-16 portability addendum

A fresh Windows checkout exposed that raw working-tree SHA-256 checks
rejected CRLF checkout bytes for the same Git text blobs that passed in the
original LF worktree and Linux CI.  The primary and audit now normalize CRLF
to LF before checking their theorem, predecessor, review, and primary hashes.
Mismatch assertions also report the exact drifting path and digests.

No tensor identity, orbit action, residual representative, expected LF blob
hash, field scope, or theorem boundary changed.  The based-frame predecessor
review received the same portability-only correction and its new normalized
hash is pinned by both transport scripts.  Fresh Windows replay now passes
the primary and structurally separate no-import audit.

## 1. The exact tensor predicate is the right one

The theorem writes the permanent tensor as

```text
P_r(z^(0),...,z^(r-1))
  =sum_(tau in S_r) product_t z^(t)_(tau(t)).
```

For six local independent triples it then uses the full `3^6` coefficient
table, not only the two-mode product space or the five complementary
quartics.  An exact weighted diagonal target means precisely three nonzero
constant-colour entries and zero on every mixed colour word.

This matches the three displayed full-extension packages.  Those packages
allow a nonzero target weight `lambda_c` for each colour.  The transport
proof preserves that convention and does not silently replace it with one
common target scalar.

The unnormalized polarization convention is harmless.  Any alternative
uniform polarization normalization multiplies both sides of every
covariance identity by the same nonzero scalar in characteristic zero.

## 2. Coordinate monomial covariance

The monomial action is fixed unambiguously by

```text
(g z)_(pi(i))=d_i z_i,
chi(g)=product_i d_i.
```

For a target coordinate assignment `tau`, the source assignment is
`rho=pi^(-1) tau`.  It is again a permutation.  Consequently the scale
factor in every permanent summand is

```text
product_t d_(rho(t))=product_i d_i=chi(g).
```

This proves the relative-invariant identity term by term.  In particular:

- there is no determinant sign under coordinate permutation;
- `chi(g)` is nonzero because every `d_i` is nonzero;
- the same `g` must be applied in every source mode; and
- the proof does not extend to an arbitrary general-linear map.

The theorem states exactly these restrictions.

The primary verifier constructs 36 independent source-entry symbols and six
independent scale symbols.  For a nontrivial coordinate permutation it
expands both 720-term permanent polynomials and obtains zero residual.

The independent audit takes a different route.  It imports no symbolic
algebra and enumerates all 720 target assignments.  Applying its separately
implemented inverse permutation recovers all 720 source assignments exactly
once, with the full six-coordinate scale mask in every term.  This is a
complete combinatorial check of the general reindexing, not a finite-field
or random sample.

## 3. Complementary quartics transport as full tensors

For a square-free quadratic

```text
q=sum_(i<j) q_ij x_i x_j,
star(q)=sum_(i<j) q_ij product_(k notin {i,j}) x_k,
```

the complete polarization of `star(uv)` on the remaining four modes is
exactly the six-linear permanent with `u,v` in the first two slots.  The
quadratic coefficient `u_i v_j+u_j v_i` accounts for the two first-slot
assignments; the complementary quartic polarization accounts for the
remaining `4!` assignments.

Therefore the quartic identity in the theorem follows from the full tensor
identity without guessing a substitution rule for `star`.  This avoids a
real failure mode: under a nonuniform diagonal scaling, `star(gq)` is not in
general obtained by applying the same naive polynomial substitution to
`star(q)`.  The theorem uses the correct evaluated-polarization identity.

The primary independently checks that identity with 15 algebraically
independent quadratic coefficients, all 360 pair/complement assignments,
generic remaining-mode vectors, and independent symbolic scales.

The no-import audit enumerates all 15 source pairs and all 24 assignments of
each four-coordinate complement.  It recovers the correct source complement
and full six-coordinate scale mask in all 360 cases.

## 4. Colour bookkeeping and source-mode exchange

For the ordered-mode transport, direct substitution gives

```text
C'_(c_0,...,c_(r-1))
 =a_(c_0)b_(c_1)chi(g)
  C_(sigma(c_0),...,sigma(c_(r-1))).
```

A common colour permutation preserves constant words and mixed words.  The
three diagonal weights become

```text
lambda'_c=a_c b_c chi(g) lambda_(sigma(c)),
```

which stay nonzero.  Independent permutations on the first two colour
triples would not have this property; the theorem does not allow them.

For omitted-mode exchange, symmetry of the permanent swaps the first two
entries of the source colour word.  A word is constant before that swap if
and only if it is constant after it.  Thus the same diagonal formula and
mixed-word vanishing remain valid.

All operations are invertible.  The use of `g^(-1)`, `sigma^(-1)`, reciprocal
colour scales, and the involutive mode swap proves an equivalence of
extendibility, rather than only a one-way construction.  Nonextendibility
therefore transports by contraposition with no quantifier change.

The primary exhausts all `3^6=729` colour words for both direct and exchanged
formulas and finds exactly three nonzero diagonal words in each case.

The audit does more than repeat the support truth table.  It constructs six
separate rank-three rational local triples, evaluates their full 729-entry
coefficient tensor using a subset-dynamic-programming permanent, and then
re-evaluates two transformed tensors.  Every direct and every exchanged
entry agrees with the predicted covariance formula under a nontrivial
coordinate permutation and nonuniform signed rational scalings.  Its
monomial character is the nonzero rational `143/12`.

The rational fixture is regression evidence, not the proof of generality.
Generality is owned by the written reindexing proof and the two complete
discrete assignment audits above.

## 5. Composition with the equality-five census

The primary and audit both pin the exact theorem and hostile-review bytes for
five frozen inputs:

1. equality-five active-support orbit synthesis;
2. co-two `r=4` based-frame orbit classification;
3. displayed `(3,1)` triangle-pair full-extension exclusion;
4. displayed `(4,1)` star-pair full-extension exclusion; and
5. displayed `(4,2)` fixed-pair full-extension exclusion.

The support synthesis is used only conditionally: an omitted pair with
product dimension five in an actual weighted diagonal restriction has
active support four and one of the three admissible unbased types.  No claim
is made that an arbitrary pair outside that hypothesis has this form.

The based census and frozen exclusions compose as follows:

```text
type    based invariants       displayed exclusion    exchange action    residual

(3,1)  unique 012             012 excluded            unique             none
(4,1)  k=3,2,1,0              k=2 excluded            k -> 3-k           k=3/0
(4,2)  e=0,1,2                e=0 excluded            e -> e             e=1,e=2
```

For `(4,1)`, exchange transports the displayed `k=2` exclusion to `k=1`.
It also identifies the two still-open pure types `k=3` and `k=0`, so one
representative `014` suffices.  The theorem does **not** use that
identification to exclude the pure type.

For `(4,2)`, exchange preserves `e`.  It therefore cannot collapse either
`e=1` or `e=2` into the excluded displayed `e=0` orbit.  Representatives
`025` and `024` remain separate.

The exact residual list is consequently

```text
014,025,024.
```

Both implementations reconstruct that list.  The audit additionally derives
the `014 <-> 235` pure-star exchange pairing from `k -> 3-k` and orders the
two fixed representatives by `e=1,2` rather than accepting a tautological
literal tuple.

## 6. Hostile failure-mode audit

The following possible overclaims were tested against the theorem and its
implementations.

### Applying the coordinate map only to the displayed pair

That would not yield the covariance factor in general.  The completion in
the proof applies the same `g` to every remaining local triple.  **No
blocker.**

### Replacing monomial covariance by arbitrary `GL_r` covariance

The square-free permanent tensor is not a relative invariant of arbitrary
`GL_r`.  The theorem consistently says coordinate permutation plus nonzero
coordinate scaling.  **No blocker.**

### Using independent colour permutations in the two based modes

That can move a diagonal word to a mixed word.  Only one common `sigma` is
allowed and propagated to every completion mode.  **No blocker.**

### Losing nonzero diagonal targets under rescaling

All monomial and colour scales are explicitly nonzero, so `chi(g)` and every
new `lambda'_c` are nonzero.  **No blocker.**

### Treating source-mode exchange as pair-level only

Equation (18) uses symmetry of the full permanent tensor, not merely symmetry
of the pair product space.  It transports the other four modes explicitly.
**No blocker.**

### Collapsing inequivalent based-frame orbits

The transport theorem applies only when the census supplies an actual
monomial/colour/mode-exchange equivalence.  It does not identify the pure and
mixed star types or the three fixed `e` types.  **No blocker.**

### Calling a residual representative feasible

The status, consequence, and exact-boundary sections all say that the three
representatives are open obligations, not extensions.  **No blocker.**

### Strengthening the field scope

The covariance lemma itself is valid over any field for nonzero scalings.
The orbit census and exclusion inputs are characteristic-zero theorems, and
the residual corollary retains characteristic zero.  **No blocker.**

### Promoting equality-five closure to `P_6` closure

The theorem explicitly leaves the dimension-at-least-six co-two sensor
residual unaddressed and unrestricted `P_6 -> Delta_3` unknown.  **No
blocker.**

## 7. Implementation independence and replay

Fresh replay of the frozen bytes gave

```text
primary exact verifier:                                  PASS;
independent no-import audit:                             PASS;
py_compile on both scripts:                              PASS;
Ruff on both scripts:                                    PASS.
```

Primary output:

```text
permanent terms:                                         720;
generic complementary assignments:                      360;
colour words checked, direct and exchanged:              729 each;
residual representatives:                                014,025,024.
```

Independent-audit output:

```text
permanent term bijection:                                720/720;
quadratic/complement term bijection:                     360/360;
rational fixture entries checked, direct:                729;
rational fixture entries checked, exchanged:             729;
imports primary:                                         NO;
imports SymPy:                                           NO;
residual representatives:                                014,025,024.
```

Source inspection confirms that the audit imports neither the primary nor
SymPy.  Its general covariance check is based on permutation inversion and
coordinate masks, while its numerical route uses `Fraction` arithmetic and
a subset dynamic program.  These differ from the primary's SymPy polynomial
expansion and symbolic coefficient route.

The audit pins the theorem and primary hashes.  Both scripts pin all ten
theorem/review dependency hashes used by the residual composition.  A changed
input is rejected rather than silently inherited.

## 8. Accepted boundary

```text
field of covariance lemma:                                ARBITRARY;
field of equality-five residual corollary:                CHARACTERISTIC ZERO;

common coordinate monomial covariance:                    PROVED;
common target-colour relabeling:                           PROVED;
nonzero first-two-mode colour rescaling:                   PROVED;
exchange of first two source modes:                        PROVED;
two-way extension/nonextension transport:                  PROVED;

all based (3,1) equality-five frames:                      EXCLUDED;
mixed (4,1) equality-five frames:                          EXCLUDED;
fixed (4,2) e=0 equality-five frames:                      EXCLUDED;

pure (4,1) residual representative:                        014;
fixed (4,2) e=1 residual representative:                   025;
fixed (4,2) e=2 residual representative:                   024;

nonextension of 014:                                      OPEN;
nonextension of 025:                                      OPEN;
nonextension of 024:                                      OPEN;
dimension-at-least-six co-two sensor residual:             OPEN/NOT ADDRESSED;
unrestricted P_6 -> Delta_3:                              UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

## Final reviewed hashes

```text
theorem:
B1762F22813E5B749FF0C81DA6C6CE5E9B8E95601662D87CB21835AAF63C3DA0

primary verifier:
E37A2E98447F6058496A3487D0A01F498B331E730CC3B01C72FC6750CEC5838E

independent no-import audit:
1EC63510DB2E03A58D7502AAE7160310B4F324BFAD0547BB1E86A05A2602A740
```
