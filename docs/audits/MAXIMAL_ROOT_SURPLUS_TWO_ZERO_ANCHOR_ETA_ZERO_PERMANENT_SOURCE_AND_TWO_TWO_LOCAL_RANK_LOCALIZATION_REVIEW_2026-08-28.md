# Hostile review: eta-zero permanent source and two-two local-rank localization

## Review target and verdict

Target reviewed:

`claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_ETA_ZERO_PERMANENT_SOURCE_AND_TWO_TWO_LOCAL_RANK_LOCALIZATION_THEOREM.md`

Supporting artifacts reviewed:

`claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py`

`claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py`

**Verdict: PASS for the exact `GLS65` scope after explicit base-change,
zero-vector, and quotient-kernel repairs.**  The theorem correctly identifies
the `GLS64` eta-zero same-source tensor as a separated `P_4` restriction and
confines its generic local ranks to exactly `2,2,3,3`.  It does not exclude
that residual.

The review initially rejected the compressed draft as written because it
invoked a complex `P_4` theorem over a fraction field without a bridge,
skipped a zero-vector subcase in the mixed-triple proof, and used fixedness
of two anchor rows without displaying the common-kernel argument.  The
reviewed theorem now supplies a complex specialization argument, treats the
missing zero-vector strata directly, and writes the quotient matrix equation
`M H^T=0`.  It also corrects a sharpness-control overstatement: arbitrary
majority `Q` rows do not raise the corresponding local source spans above
two.

This is an exact source-integrability localization inside the
exactly-two-deficient branch.  The `2233` residual, three-plus-deficient
profiles, attachment, response, synchronization, and the global conjecture
remain open.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Exact permanent source

On `eta=W_nm(e_c,e_c)=0`, the effective complementary-port block is

```text
D_ij=a_i tensor b_j+b_i tensor a_j.
```

For each choice of the two ports receiving `P,Q`, the companion block has
two orders and the complementary fixed-row block has two orders.  The six
pair choices therefore give `6*2*2=24` labelled terms.  They are exactly the
twenty-four permutations of `P,Q,A,B`, with no repeated or missing source
assignment.  Thus the complete two-kernel hierarchy member is one tensor

```text
(tensor_i L_i) P_4
 =kappa z_(0,c)z_(1,c) tensor_i e_(i,c)^*,   kappa!=0.
```

This uses all six blocks from one physical source.  It does not replace
them by independently selectable pair tensors.

## Fixed generic rank-two ports

Each open port has independent generic probe rows, hence local rank at least
two, and each physical local space is a qutrit, hence rank at most three.
The hypothetical graph has complex coefficients, so its local minors are
complex polynomials, and the accepted rank-drop theorem is stated over
`C`.  The reviewed proof uses it as follows: if three generic ranks were
three, one nonzero three-minor at each such port, nonzero two-minors at the
others, and
`z_(0,c)z_(1,c)` would have one common nonempty complex principal open.  A
point in that open would be a nonzero pure complex `P_4` restriction with
three rank-three maps, contradicting the theorem.  Therefore at least two
of the four fixed polynomial maps have generic rank two.  This is not a
fibre-dependent choice of ports.

At a rank-two port, the nonzero target factor belongs to the local image, so
`p_i,q_i,c_i` lie in one plane and `(p_i cross q_i)_c=0`.  The accepted
orientation theorem puts the port in `E_c`.  Modulo its `c`-line, each fixed
row `a_i,b_i` would have to be proportional to a generic two-direction
opposite-shore row.  Wedge comparison with its two coefficient vectors
forces both fixed rows to vanish in the quotient.  Zero fixed rows are
included.  These are the silent rank-two ports used in the rest of the
proof.

## Exclusion of profile `2222`

The review checked all sixteen binary orientation words, grouped only by
port permutation and the global `P/Q` exchange.

- For four equal orientations, every one-off coefficient is a complementary
  three-row cofactor.  Expanding the all-target permanent along the repeated
  off-source column makes it zero.
- For a `1+3` word, three opposite two-off equations kill the three
  within-majority `N_ij`.  The remaining one-off system has determinant
  `2x_1x_2x_3`, nonzero because these are the active pure-shore
  coefficients.
- For a `2+2` word, four opposite equations kill the cross `N_ij`, and two
  active one-off coefficients kill the remaining within-pair values.

The all-target coefficient expands through the six `N_ij` values and is
therefore zero in every case.  No fixed-row scalar, raw edge, or deck is
divided out.

## Exclusion of mixed profile `2223`

For three silent planes, the `0|123` flattening is the restriction of the
perfect `R_1 x R_3` squarefree multiplication pairing.  Rank-one purity
gives product dimension at most two.  If `C_off` is the span of products
containing a silent off row and `g` is the all-target product, nonzero purity
requires `g` to be independent of `C_off`; hence `dim C_off<=1`.

For the mixed word `(P,P,Q)`, replacing a target row `u_i` by
`u_i+lambda_i e_(rho_i)` changes `g` only modulo `C_off`, which justifies
the displayed normal form.  The five off products have the reviewed
complementary cofactor rows

```text
m_1=(0,b_2c_3+c_2b_3,a_2c_3,a_2b_3),
m_2=(0,b_1c_3+c_1b_3,a_1c_3,a_1b_3),
m_3=(b_1c_2+c_1b_2,0,0,0),
m_4=(0,0,c_2,b_2),
m_5=(0,0,c_1,b_1).
```

If `v_3=0`, the dimension-one condition first kills the symmetric product
of `v_1,v_2`, after which
`g=d PQ(a_1v_2+a_2v_1)` is zero or already in `C_off`.  This explicitly
covers `v_1=0,v_2!=0` and its transpose.  If `v_3!=0`, the `PQ`, `PAB`, and
`QAB` coordinates put every nonzero `v_i` on one isotropic line.  In
characteristic zero that is a coordinate line, and the all-target product
again belongs to `C_off`.  Thus every zero stratum is retained.

## Homogeneous triple and anchor rigidity

For three equal silent orientations, direct permanent expansion isolates
the three off-row coefficients and leaves

```text
K_P4!=0,                q_0 in Kc_0.
```

Because `q_0` depends on one probe only, its two quotient-coordinate
polynomials vanish identically, so the entire opposite shore is pure.  Put
the three coefficient rows into `H` and the anchor columns into
`M=[p_0 a_0 b_0]`.  The off-row equations are exactly `M H^T=0`.

If `rank H>=2`, every coordinate row of the quotient of `M` lies in the
same at-most-one-dimensional kernel.  A nonzero fixed quotient row among
`a_0,b_0` fixes the resulting physical line; if both vanish, the nonzero
`h^P` column forces the quotient of `p_0` to vanish too.  If `rank H=1`, the
three exact permanent identities give the displayed fixed-line formula for
`p_0`; rank zero contradicts `K_P4!=0`.  Thus the anchor shore has transverse
coefficient span at most one, contradicting its required injective opposite
orientation.

Profiles `2222` and `2223` are therefore empty.  Since every local rank is
two or three and at least two are two, the only remaining profile is
exactly `2233`.

## Sharp control and retained boundary

The exact `YXXX` binary-row control restricts `P_4` to one nonzero pure
coefficient.  Its three majority `Q` rows may be replaced by arbitrary
output vectors while the restriction stays pure, because the complementary
`P,A,B` permanent vanishes.  Their other three source rows remain collinear,
so the local ranks stay at most two.  The control is a sharp warning against
pointwise or independently based reasoning, not a full-injective witness.

The proof stops with two silent rank-two planes and two rank-three
hyperplanes, coupled to the nonzero raw matching deck and all `GLS64` scalar
equations.  Same versus opposite silent orientations, the pair-image
annihilator, and source-hyperplane synchronization are the next exact
obligations.  Three-plus-deficient profiles require a separate mixed-kernel
analysis.

## Replay evidence

The following commands were rerun in the isolated working tree:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_eta_zero_permanent_source_and_two_two_local_rank_localization.py
```

The primary replay reconstructed all twenty-four source assignments, the
sixteen orientation words, five mixed-triple products, three anchor
identities, and the fixed-fibre flat.  The independent replay checked 4,608
orientation trials, 13,182 mixed-plane tuples over `F_3` with zero dangerous
cases, and 5,000 anchor trials over `F_101`.  Compilation and Ruff checks
passed.  These programs audit displayed finite algebra; specialization,
perfect-pairing, and same-source bridges remain the written proof.

Final review status: **PASS for `GLS65`; exact `2233` residual open; global
Krenn--Gu conjecture UNRESOLVED.**
