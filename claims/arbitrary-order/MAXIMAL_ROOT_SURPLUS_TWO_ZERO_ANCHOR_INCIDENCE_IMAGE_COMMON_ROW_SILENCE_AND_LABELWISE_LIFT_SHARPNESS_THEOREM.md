# Maximum-root surplus-two zero-anchor incidence image, common-row silence, and labelwise-lift sharpness

## Status and scope

**Exact characteristic-zero arbitrary-root reduction and four-root physical
sharpness theorem.**  On the zero-anchor branch, the complete raw nuisance
`B_Q^anc` of `GLS35` is exactly the image of one explicit map built only from
the root-to-residual and root-to-port incidence blocks.  Residual--port,
port--port, and all other complementary-deck edges do not enter that
coefficient map.

Consequently, on the swallowed-pure branch, every constant coefficient row
annihilating the nuisance also annihilates `q` and all three pure probe
tensors.  Applying any such common row to the complete promoted identity
gives `0=0`.  Thus a fixed common annihilator row cannot separate the branch,
and a Fitting rank profile alone does not manufacture such a row.  This does
not make tangent or Fitting equations on the parameter locus globally silent.

The mixed promoted-port equations at every fixed residual contraction instead
become an exact **labelwise lift condition** in the kernel of the incidence
map.  This identifies the
smallest type-correct continuation: one must control the complementary deck
attached to each labelled incidence slice, including zero-response and
cancelling labels, rather than only its aggregate coefficient image.

The boundary is sharp on a strong physical graph.  Retyping the exact
four-root maximum-root control of `GLD11` gives

```text
rank B_Q^anc=8,
q,r_0,r_1,r_2 in B_Q^anc,
im Flat_A(G)=B_Q^anc.
```

The same graph has triple blockers, pure coefficients one, zero Hamming-one
shell, local concision, and all seven physical responses nonzero.  It is on
the `GLS34` diagonal-silent side and fails `116` mixed GHZ coefficients, so
it is not a witness and not a counterexample.  The theorem does not exclude
the swallowed branch on the witness locus, force raw-anchor escape, supply a
legal original target selector, or close any arbitrary-root source cover.

This is `GLS36`.  The maximum-root surplus-two supply-and-target-attachment
node and the global Krenn--Gu conjecture remain **UNRESOLVED**.

## Dependencies and provenance

The owning interfaces are:

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  for the grade-zero two-root/two-label companion definition;
- [`GLS21`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_BASE_SHADOW_ALL_PORT_NUISANCE_COLLAPSE_THEOREM.md)
  for the raw promoted matching decomposition;
- [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md)
  for complete labelled coefficient slicing;
- [`GLS33`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RESIDUAL_LAURENT_POLARIZATION_AND_ROOT_DECK_KERNEL_ANCHOR_THEOREM.md)
  for the unprojected constant root-deck equation;
- [`GLS34`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TANGENT_ROOT_FITTING_AND_CONSTANT_ANCHOR_SEGRE_SILENCE_THEOREM.md)
  for the constant-anchor survival/silence split;
- [`GLS35`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RAW_ROOT_DECK_QUOTIENT_AND_OUTPUT_COEFFICIENT_SEPARATION_NO_GO_THEOREM.md)
  for `B_Q^anc` and the escape/swallow dichotomy; and
- [`GLD11`](FOUR_ROOT_SIMULTANEOUS_SWALLOWED_PURE_NONZERO_RESPONSE_PHYSICAL_CONTROL_THEOREM.md)
  for the exact maximum-root graph and its previously proved source-side
  properties.

No external literature claim is used.  The new content is the incidence-map
presentation, the common-row no-go, the exact mixed labelwise-lift
reformulation, and the retyping of the `GLD11` graph in the `GLS35` module,
including its full-state flattening image.

## 1. The zero-anchor incidence map

Let `K` have characteristic zero.  Retain the promoted notation

```text
A={a_0,a_1},                 Q={q_0,q_1},
Bhat=Q disjoint-union Uhat,
E_A^*=V_(a_0)^* tensor V_(a_1)^*,
omega=W_(a_0,a_1)=0.                                  (1)
```

Fix the residual vectors `z_(q_s)`.  For `u in Uhat`, define the incidence
maps

```text
X_u:V_u -> V_(a_0)^*,       X_u(v)=W_(a_0,u)(-,v),
Y_u:V_u -> V_(a_1)^*,       Y_u(v)=W_(a_1,u)(-,v),

xi_i^s=W_(a_i,q_s)(-,z_(q_s)).                        (2)
```

Put

```text
L_Q=
  direct-sum_(s=0,1; u in Uhat) V_u
  direct-sum_(unordered {u,v} subset Uhat) (V_u tensor V_v).  (3)
```

Define `sigma_Q:L_Q->E_A^*` componentwise by

```text
sigma_(s,u)(x)
 =xi_0^s tensor Y_u(x)+X_u(x) tensor xi_1^s,          (4)

sigma_(u,v)(x tensor y)
 =X_u(x) tensor Y_v(y)+X_v(y) tensor Y_u(x).         (5)
```

The second formula extends linearly from pure tensors.

### Theorem 1 (exact incidence-image presentation)

On `omega=0`, pointwise at every residual, shore-rank, incidence-rank,
nuisance-rank, divisor, and `p` fibre,

```text
B_Q^anc=im sigma_Q.                                   (6)
```

In particular, `B_Q^anc` depends only on the incidence data (2).  Under the
owning `GLS8` root-companion grading, edges whose endpoints both lie in
`Bhat` do not occur in the grade-zero pair companions at all.  The separate
top summand `K omega` vanishes on the present zero-anchor branch.

#### Proof

For `D={q_s,u}`, the grade-zero root companion is the sum of the two
root-to-`D` bijections.  After evaluating `q_s` it gives

```text
g_D(z_Q)
 =xi_0^s tensor Y_u+X_u tensor xi_1^s.               (7)
```

Taking every coefficient slice in the open `u` slot gives exactly the image
of (4).

For `D={u,v}`, the same two-bijection definition gives

```text
g_D
 =X_u tensor Y_v+X_v tensor Y_u.                     (8)
```

Complete slicing in `u,v` gives the image of (5).  These are every label
`D!=Q` in the definition of `B_Q^anc`; the separate top summand `K omega` is
zero by (1).  Summing their images proves (6) without division or a rank-open
restriction. `square`

### Corollary 1.1 (all-rank finite criterion)

For any fixed matrix of `sigma_Q`, the full swallowed-pure condition is

```text
q,r_0,r_1,r_2 in B_Q^anc
iff
rank sigma_Q=rank[sigma_Q|q|r_0|r_1|r_2],           (9)
```

where `r_c=e_(a_0,c)^* tensor e_(a_1,c)^*`.  Thus no chosen incidence minor
or generic rank is implicit in the criterion.

## 2. Why a common coefficient row becomes silent

Write

```text
B=B_Q^anc,                B^perp={lambda:lambda(B)=0}. (10)
```

### Theorem 2 (fixed common-row silence on the swallowed branch)

Assume

```text
q,r_0,r_1,r_2 in B.                                  (11)
```

Then every `lambda in B^perp` obeys

```text
lambda sigma_Q=0,
lambda(q)=lambda(r_0)=lambda(r_1)=lambda(r_2)=0.      (12)
```

Consequently, applying one common constant coefficient row `lambda` to the
raw promoted identity annihilates every labelled source coefficient and the
complete ternary GHZ target.  It yields the identity `0=0` on every port
word.  No common-row quotient of this coefficient map can be normalized on
`q`.  Equivalently, incidence-rank/Fitting data do not by themselves supply a
separating row.  They may still constrain which parameter fibres can occur.

#### Proof

The first equality in (12) is (6) and the definition of the annihilator.
The other four equalities are exactly (11).  Every non-`Q` source label has
coefficient in `im sigma_Q`; the `D=Q` label has coefficient `q`; and the
three target coefficients are the `r_c`.  Applying `lambda` therefore kills
both sides coefficientwise. `square`

This is a no-go for a **common coefficient row**, not for label-dependent
operators.  It does not say that the complete mixed equations are silent
before the labels and their complementary physical decks are coupled.

## 3. Exact mixed labelwise-lift reformulation

Let the primal port test space be

```text
Z_Uhat=tensor_(u in Uhat) V_u,
H=H_Uhat.                                              (13)
```

This `Z_Uhat` is distinct from the dual deck space denoted `W_Uhat` in
`GLS35`.  For each non-`Q` label `D`, put `D_0=D intersect Uhat`.  Evaluate
every residual vertex remaining in the complementary physical deck and set

```text
h_D=H_(Bhat-D)(z_(Q-D))
    in tensor_(u in Uhat-D_0) V_u^*.

rho_D(tensor_u z_u)
 =h_D(tensor_(u notin D_0) z_u)
  tensor_(u in D_0) z_u
 in tensor_(u in D_0) V_u.                            (14)
```

The fixed canonical port order is understood, and `rho_D` extends linearly
from pure tensors.  Collect these labelled components into

```text
rho_Q:Z_Uhat -> L_Q.                                  (15)
```

This definition retains labels with zero complementary deck as zero
components; it does not divide by a response.  Define the primal mixed test
space

```text
Z_mix=intersection_(c=0)^2 ker((e_c^*)^(tensor |Uhat|))
      subset Z_Uhat.                                  (16)
```

### Theorem 3 (labelwise lift of the fixed-residual mixed equations)

At the fixed residual vectors, contracting the exact raw promoted
decomposition by `z in Z_Uhat` says that the corresponding `E_A^*`-valued
coefficient of the `Q`-contracted state is the left side below.  Consequently,
the `Q`-contracted ternary target equation at those residual vectors is
equivalent to

```text
q H(z)+sigma_Q(rho_Q(z))
 =sum_(c=0)^2 alpha_c r_c (e_c^*)^(tensor |Uhat|)(z). (17)
```

Here every residual-torus scalar `alpha_c` is retained.  A complete
uncontracted hypothetical witness implies (17) for every residual choice (or
coefficientwise over the formal residual family); one fixed residual equation
does not imply the full target equation.  On `Z_mix`, (17) becomes

```text
q H(z)+sigma_Q(rho_Q(z))=0.                           (18)
```

If `q` is swallowed and `v in L_Q` is any certificate with
`sigma_Q(v)=q`, then all mixed `Uhat` coefficients of this fixed
`Q`-contracted equation are equivalent to

```text
rho_Q(z)+H(z)v in ker sigma_Q
for every z in Z_mix.                                 (19)
```

Condition (19) is independent of the chosen certificate `v` modulo
`ker sigma_Q`.

#### Proof

The left side of (17) is the `GLS21` raw labelled decomposition after complete
contraction of the `Uhat` ports.  Formulas (4)--(5) collect its non-`Q`
coefficients, the `D=Q` term is `qH`, and the GHZ target is the right side.
The target vanishes on (16), proving (18).  Substitute `q=sigma_Q(v)` in
(18) and use linearity to obtain (19).  Conversely, applying `sigma_Q` to
(19) recovers (18).  Two
certificates for `q` differ by `ker sigma_Q`, proving independence. `square`

The load-bearing missing theorem is therefore not another row of (12).  It
must prove that (19) fails on every hypothetical swallowed witness, using a
new physical companion-exchange or mixed-coefficient identity that couples
each incidence component to its own deck.  Such a theorem must cover zero
deck components, proportional or cancelling labelled components, and every
exceptional rank/divisor fibre.

## 4. Maximum-root exact sharpness control

Use the exact graph of `GLD11`, with its notation

```text
R={r_0,r_1,r_2,r_3},
U={u_0,u_1,u_2,u_3},
Q={q_0,q_1}.                                          (20)
```

Retype it in the promoted chart as

```text
A=(r_1,r_2),          K_0={r_0,r_3},
Uhat=K_0 disjoint-union U,
Q=(q_0,q_1).                                          (21)
```

All actual root and residual vectors are `(1,1,1)`.  Use the ordered basis
`e_i tensor e_j` of `E_A^*`.

### Theorem 4 (full raw swallow and flattening-image sharpness)

For the retyping (21),

```text
omega=0,
q=e_2 tensor e_1,
p=1,                                                  (22)

B_Q^anc=span{
 e_00,e_01,e_02,e_10,e_11,e_20,e_21,e_22},           (23)

rank B_Q^anc=rank[B_Q^anc|q|r_0|r_1|r_2]=8.          (24)
```

In (24), `r_c=e_c tensor e_c` denotes the pure probe tensor of `GLS35`, not
the graph root carrying the same subscript in (20).

The only missing coordinate is `e_12`.  Every displayed basis vector in
(23) has a single-slice certificate:

```text
coefficient   label D        open coefficient word
e_00          {u_2,q_1}      (0)
e_01          {q_1,u_1}      (1)
e_02          {q_1,u_3}      (2)
e_10          {u_2,u_3}      (0,1)
e_11          {u_1,u_3}      (1,1)
e_20          {q_0,u_2}      (0)
e_21=q        {u_0,u_1}      (2,1)
e_22          {u_0,u_3}      (2,2).                 (25)
```

Moreover, if `Flat_A(G)` is the full ten-mode state flattened with the two
probe modes on the coefficient side, then

```text
rank Flat_A(G)=8,
im Flat_A(G)=B_Q^anc.                                 (26)
```

The residual-absent deck `H_Uhat` is nonzero: it has nine unit coefficient
words and `H_Uhat(1,...,1)=9`.  The already proved `GLD11` properties remain
simultaneous:

- `R` is a maximum-cardinality torus zero set;
- every outside mode is a rank-three blocker;
- the pure full-state coefficients are one and the full Hamming-one shell is
  zero;
- the state is locally concise; and
- all six pair responses and the four-port response are nonzero.

The constant diagonal is nevertheless on the `GLS34` silent side.  In the
port order `(r_0,r_3,u_0,u_1,u_2,u_3)`, its local product kernels are

```text
K_(r_0)^00=K_(r_3)^00=K^3,
K_(u_0)^00=ker e_2^*,
K_(u_1)^00=ker e_1^*,
K_(u_2)^00=ker e_0^*,
K_(u_3)^00=ker e_1^* intersection ker e_2^*.         (27)
```

Thus each diagonal colour is killed at a port.  Finally, the complete state
has `119` supported words from `124` nonzero matchings.  Besides the three
pure words, exactly `116` mixed GHZ coefficients fail: `111` equal one and
five equal two.  Hence the graph is not a hypothetical witness.

#### Proof

The root--root blocks in `GLD11` vanish, proving `omega=0`.  Reading the two
residual columns in rows `r_1,r_2` gives `q=e_21` and `p=1`.  Direct
substitution in (4)--(5) gives the eight single-slice identities (25).
Every remaining slice is supported on those same eight coordinate tensors;
the complete 171-column incidence matrix has rank eight, while adjoining
`e_12` raises the rank to nine.  This proves (23)--(24).

Exact matching enumeration of the full graph gives a probe flattening of
rank eight with precisely the same eight coordinate rows, proving (26).
The six-mode induced deck gives the nine unit words.  Formula (27) follows by
evaluating the two probe-incidence rows at `(1,1,1)`.  The maximum-root,
blocker, pure-shell, concision, and response statements are the exact
`GLD11` theorem; the focused verifier replays their finite graph data.  The
same enumeration gives the final support and mixed-failure counts. `square`

This control realizes the algebraic swallowed membership and every listed
source-side gate, but not the complete-target premise of `GLS35` Theorem 2.
It is also diagonal-silent.  It therefore proves that raw coefficient escape
does not follow from those source gates; it does not prove that a swallowed
hypothetical witness exists.

## 5. Frontier and unresolved remainder

```text
zero-anchor raw nuisance equals incidence-map image:       PROVED;
all-rank swallowed criterion:                              PROVED;
common coefficient rows are silent after full swallow:     PROVED;
fixed-residual mixed equations equal labelwise lift (19):  PROVED;
maximum-root source-gated full-swallow control:             PROVED;
control satisfies complete mixed GHZ equations:             FALSE;
control lies on GLS34 non-silent branch:                     FALSE;
labelwise faithfulness excludes (19) on every witness:      UNKNOWN;
raw escape supplies an original GLS22/23 or GLD3 target:     FALSE;
arbitrary-root source cover and strategic-node closure:     UNKNOWN;
global Krenn--Gu conjecture:                                UNRESOLVED.
```

The smallest remaining obligation on this branch is a support-free physical
identity proving, for every `v in sigma_Q^(-1)(q)`, that some exact mixed test
`z` violates (19), or an equivalent same-graph contradiction from the full
mixed coefficient system.  It must be label-dependent: the `GLS35` local
control has a raw generator equal to `q` whose complementary deck is zero,
and `GLS32` has nonzero response labels which cancel in aggregate.  A theorem
must also retain selected-response activity, nuisance survival,
synchronization, anchor gates, exceptional fibres, and arbitrary-root source
coverage before it can enter a named downstream attachment theorem.

## Verification boundary

Run the focused exact primary verifier:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
```

Run the genuinely independent no-import audit:

```text
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
```

The primary uses exact SymPy matrices, explicit perfect matchings, and a
probe-flattening computation.  The audit uses only the Python standard
library, a vertex-deletion matching recurrence, direct coordinate incidence
columns, and independent rational elimination.  These scripts audit the
finite sharpness leaf.  The arbitrary-root incidence formulas and the
labelwise-lift equivalence are proved symbolically above.
