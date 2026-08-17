# Same-graph response-defect vanishing and target-coupled selector boundary

## Status

**Exact characteristic-zero correction to the proposed extraction-or-detection
dichotomy.**  A legally supplied response chart from one physical graph cannot
fail its own dual-Wick equations.  For every even port set `S`, the displayed
insertion defect below vanishes as a matching identity, independently of the
GHZ target.  Likewise, literal restrictions of one graph carry one global
residual frame, so every identifying response-atlas holonomy is trivial.

Consequently a nonzero response or holonomy defect can occur only in
independently reconstructed, target-imputed, or incompatible candidate data.
It is not automatically an actual mixed GHZ coefficient.  The detection arm
of a Universal Supply theorem must contain a separate target-coupled selector.

The exact surviving identity is simple.  If a two-residual top response is

```text
Lambda_Q=h U+T                                           (1)
```

and a legal target coefficient selector supplies

```text
Y=Omega U+N,              Omega!=0,                      (2)
```

including every nuisance term in `N`, then

```text
Omega T=Omega Lambda_Q-hY+hN.                            (3)
```

Thus a mixed component of the corrected channel becomes a genuine target
detector only when `h=0`, or when a coefficient-pure selector has nonzero
`Omega` and its nuisance is proved zero or independently subtractable.

Both qualifications are sharp.  A rational physical `q=2` response has a
fully diagonal uncorrected top block while its corrected channel has a
nonzero mixed entry, cancelled exactly by the residual-absent direct block.
Moreover the root-deletion selector weight is zero for every odd root count;
at the maximal-root base word it is also zero for every `r>2`.  The first
possible nontrivial polarized even-root case is the existing four-root/P6
selector.

This theorem refutes an overly strong proof route.  It does not exhibit a
graph witness, force a clean selector, or resolve Universal Supply.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Physical `q=2` responses have no insertion defect

Let `U` be a finite port set and work in the vertex-exclusive square-zero
algebra.  A physical two-residual response has

```text
M=sum_(S even) m_S x_S,
Z=sum_(S even) z_S x_S,
h=z_empty,
Z=M(h+Q_K),
Q_K=sum_(u<v) K_uv x_u x_v.                            (4)
```

Here `M_empty=1` and

```text
z_uv=h m_uv+K_uv.                                      (5)
```

For an even set `S`, `|S|=2m`, define

```text
E_S
 =z_S-sum_(e subset S, |e|=2) z_e m_(S-e)
    +(m-1)h m_S.                                       (6)
```

### Theorem 1 (same-graph insertion defects vanish)

For every physical `q=2` response and every even `S`,

```text
E_S=0.                                                 (7)
```

In particular the first four-port tangent-Wick defect, every higher insertion
defect, and every nonquadratic relative cumulant vanish without using a target
equation.

### Proof

Equation (4) gives

```text
z_S=h m_S+sum_(e subset S, |e|=2) K_e m_(S-e).         (8)
```

Substitute (5) into the sum in (6).  Every perfect matching contributing to
`m_S` is counted once for each of its `m` edges, so

```text
sum_(e subset S, |e|=2) m_e m_(S-e)=m m_S.            (9)
```

The `K` terms in the substituted sum equal `z_S-hm_S` by (8), while the
direct terms equal `hm m_S`.  Hence the sum is
`z_S+(m-1)hm_S`, which is exactly (7).

The identity is tensor-valued after block polarization.  It is a perfect-
matching edge-pointing identity, not a generic scalar specialization.

## 2. Literal same-graph atlases have trivial holonomy

Fix one named residual pair and contractions in a physical graph.  Its global
residual incidence frame is

```text
F_u=(a_u,b_u)^T,
K_uv=F_u^T J F_v,
J=[[0,1],[1,0]].                                       (10)
```

### Theorem 2 (physical transition torsor is trivial)

Let a finite atlas consist of literal restrictions of this graph.  Assume
every nonempty overlap is three-block identifying in the sense of the `GLQ2`
theorem.  For any chosen local factorizations, every overlap transition is an
`O(J)` coboundary and every cycle holonomy is the identity.

### Proof

Compare the chosen local factorization on a chart with the restriction of the
global frame (10).  On each identifying overlap, uniqueness in the
three-block overlap theorem gives one chart gauge `k_alpha in O(J)`.  The
transition from chart `alpha` to chart `beta` is

```text
g_(beta,alpha)=k_beta^(-1) k_alpha.                    (11)
```

Products around cycles telescope.  Thus nontrivial holonomy is possible for
an abstract family of individually physical charts, but not for restrictions
of one graph.

Theorems 1--2 show that the phrase “response integrability fails” cannot be
the detection branch after physical same-graph supply.  A failure belongs to
a candidate reconstruction and requires a separate proof that the failed
candidate coefficient is target-derived.

## 3. Diagonal top data do not diagonalize the corrected channel

Work over `Q` with two ternary ports `u,v`.  Let

```text
h=1,
B_uv=I_3+E_01,
a_u=e_0^*,             b_v=-e_1^*,
b_u=0,                 a_v=0.                         (12)
```

Then

```text
K_uv=a_u tensor b_v+b_u tensor a_v=-E_01,
W_uv=hB_uv+K_uv=I_3.                                  (13)
```

### Theorem 3 (exact top-target cancellation control)

The data (12) are a physical two-residual response.  Its uncorrected top
block is fully diagonal, its corrected channel has the nonzero mixed entry

```text
K_uv[0,1]=-1,                                         (14)
```

and every physical dual-Wick equation holds.

### Proof

Install two residual vertices with mutual contracted value one and the four
displayed incidence covectors.  The three matchings on the residual pair and
ports give (13).  The residual-absent graph has edge block `B_uv`; the exact
physical response is therefore `Z=M(h+Q_K)`, so Theorem 1 applies.  The
matrix calculation in (13) proves the diagonal and mixed assertions.

This is a response proof-route countermodel, not a GHZ graph witness.  Its
arbitrary-order version is equally direct: on any coordinate-monomial
two-residual slice with `h=1`, choose a factorized mixed channel `K` and
replace the direct blocks by

```text
B_uv=W_uv^top-K_uv.                                    (15)
```

The top aggregate remains fixed.  Hence top target diagonality never permits
the direct `hB` term to be discarded silently.

## 4. The target-coupled selector identity

Let `U` and `T` be tensors on a common blocker shore and suppose the physical
two-residual top tensor is (1), where `T` is the honest corrected two-row
permanent aggregate.  Suppose a separately legal root word, deletion
coefficient, or companion construction gives (2).  The term `N` is defined to
contain **all** other cofactor columns and normalizations in that selector.

### Theorem 4 (selector-coupled target attachment)

Identity (3) holds.  For a mixed blocker word `chi`,

```text
Omega T_chi
 =Omega (Lambda_Q)_chi-hY_chi+hN_chi.                 (16)
```

If `Lambda_Q` and `Y` are actual target-derived tensors of a hypothetical
witness, their mixed components vanish, so

```text
Omega T_chi=hN_chi.                                   (17)
```

Consequently:

1. if `h=0`, then `T_chi=(Lambda_Q)_chi` is itself an actual mixed target
   coefficient;
2. if `h!=0`, `N=0`, and `Y_chi` is coefficient-pure, then

   ```text
   Y_chi=-(Omega/h) T_chi;                             (18)
   ```

   hence `T_chi!=0` displays an explicit nonzero mixed GHZ coefficient;
3. without nuisance separation, (17) permits exact cancellation and gives no
   contradiction.

### Proof

Multiply (1) by `Omega`, multiply (2) by `h`, and subtract:

```text
Omega Lambda_Q-hY+hN
 =Omega(hU+T)-h(Omega U+N)+hN
 =Omega T.                                            (19)
```

Taking the `chi` coefficient gives (16).  The target conclusions are the
specializations just stated.  No component of `N` is omitted.

The theorem identifies the exact additional hypothesis needed to turn a
corrected-channel defect into a target detector.  Merely sharing physical
variables, atlas transitions, or a top diagonal equation does not supply
(2).

## 5. Root legality and the first possible selector

Let `R` be a root set of order `r` and let `Q={q_0,q_1}` be the deletion pair.
After a chosen root word or polarization, write `L` for the hollow
root--root matrix and `H_Q` for the root-to-`Q` incidence matrix.  The exact
selector weight on the residual-absent deck is

```text
Omega_Q
 =haf [ L      H_Q ]
        [ H_Q^T  0  ].                                (20)
```

### Theorem 5 (parity and maximal-root base-word wall)

The polynomial `Omega_Q` is identically zero unless `r` is even and `r>=2`.
At the maximal-root base word, where every entry of `L` is zero,

```text
Omega_Q=0                  for every r>2.              (21)
```

For `r=4`, the first polarized even-root possibility is

```text
Omega_Q
 =sum_({i,j} subset R) L_ij
    per H_(R-{i,j},Q).                                 (22)
```

### Proof

In every nonzero matching of the augmented matrix (20), the two vertices of
`Q` must meet two distinct roots.  The remaining `r-2` roots must pair through
`L`.  This requires even `r>=2`.  If `L=0`, no remaining roots can pair, so
only `r=2` can survive.  At `r=4`, choose the one root--root edge and biject
the other two roots to `Q`; summing gives (22).

Thus odd root counts cannot supply (2) by a root-word selector.  Even counts
at least four require nonprojective root tangents or polarizations that make
`L` nonzero, together with exact nuisance separation.  The four-root/P6
response-jet selector is the first conditional case; it is not forced in
every witness.

## 6. Correct theorem shape for GL

A valid target-coupled extraction-or-detection statement may use the
following implication:

```text
legal paired response supply
 + a target-normalized companion U
 or a coefficient-pure selector (Omega,N)
 -> corrected channel T is target-attached by (3).     (23)
```

Its axes are:

```text
breadth:
  one paired chart for (3); an atlas only after every chart has a target
  anchor;

depth:
  exactly the residual-present tensor Lambda_Q and one residual-absent
  companion U;

common hidden data:
  U and the corrected two-row aggregate T;

transition group:
  O(J) after three-group block-polarized identification;

agreement:
  yields a permanent restriction only after T is weighted diagonal with
  three nonzero weights;

disagreement:
  yields a mixed GHZ detector only through the explicit coefficient identity
  (16), not through physical response failure or holonomy alone.            (24)
```

The remaining universal alternatives are exact: force `h=0`; legally expose
and target-normalize `U`; force a clean even-root selector; or prove every
nuisance component in (17) zero or subtractable.  None is presently known in
all maximal-root branches.

## 7. Exact frontier

```text
same-graph q=2 insertion defect:                    IDENTICALLY ZERO;
same-graph identifying-atlas holonomy:              IDENTICALLY TRIVIAL;
top diagonal implies corrected channel diagonal:    FALSE;
selector-coupled identity (3):                       PROVED;
nuisance-free nonzero selector gives mixed detector: PROVED CONDITIONAL;
odd-root pair selector:                              IMPOSSIBLE;
maximal-root base selector for r>2:                  ZERO;
clean four-root/P6 selector forced:                  UNKNOWN;
universal target-normalized companion:              UNKNOWN;
universal nuisance separation:                      UNKNOWN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

## Focused checks

Run from repository root:

```powershell
python claims/arbitrary-order/verify_same_graph_response_defect_vanishing_and_target_coupled_selector_boundary.py
python -I claims/arbitrary-order/audit_same_graph_response_defect_vanishing_and_target_coupled_selector_boundary.py
```

The primary verifier checks the insertion formula through six ports, the
exact rational matrix control, the selector identity, and the `r=2,3,4,5,6`
augmented-hafnian parity table.  The independent no-import audit uses exact
`Fraction` arithmetic, a bitmask perfect-matching recurrence, and separate
matrix operations to verify the response and cancellation controls; it also
checks (3) at two nontrivial exact substitutions.  It is not a second
symbolic derivation of (3).  These bounded replays audit the displayed
fixtures; the written algebraic identity and the matching, coboundary, and
augmented-hafnian arguments prove the arbitrary-order statements.

Dependencies:

- [`RESIDUAL_RELATIVE_RESPONSE_POLYNOMIAL_DUAL_WICK_THEOREM.md`](RESIDUAL_RELATIVE_RESPONSE_POLYNOMIAL_DUAL_WICK_THEOREM.md)
- [`RESPONSE_JETS_AS_PRINCIPAL_DELETION_DECKS_AND_ROOT_PARITY_LEGALITY_THEOREM.md`](RESPONSE_JETS_AS_PRINCIPAL_DELETION_DECKS_AND_ROOT_PARITY_LEGALITY_THEOREM.md)
- [`TWO_RESIDUAL_RESPONSE_ATLAS_IDENTIFYING_OVERLAP_AND_HOLONOMY_BOUNDARY_THEOREM.md`](TWO_RESIDUAL_RESPONSE_ATLAS_IDENTIFYING_OVERLAP_AND_HOLONOMY_BOUNDARY_THEOREM.md)
- [`GRAPH_EXTRACTION_TOP_TWO_PORT_SYNCHRONIZATION_OBSERVABILITY_BOUNDARY.md`](GRAPH_EXTRACTION_TOP_TWO_PORT_SYNCHRONIZATION_OBSERVABILITY_BOUNDARY.md)
