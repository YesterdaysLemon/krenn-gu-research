# Four-root full-rank all-response-zero localization hostile review -- 2026-08-20

## Verdict

**Accepted at the frozen hashes below. No P0, P1, or P2 defect remains.**

The accepted package is an exact characteristic-zero **conditional
localization** of one narrow root-order-four response-zero subbranch.  For the
GLS4-supplied residual pair `Q`, it assumes `det H_Q!=0` and literal vanishing
of all six same-`Q` pair-response tensors.  It proves that every direct edge
among the four complementary ports vanishes, classifies the remaining common
one- or two-port support, derives the four-port response zero, excludes equal
residual colours, and localizes the survivor to the opposite-colour
pure-third-colour `Pi_Q` locus.

It does **not** exclude that surviving locus, cover `det H_Q=0`, cover the
broader GLS7 `R` branch in which only one of the seven responses is zero, or
treat any nonzero-response absorption or exceptional-rank fibre.  It supplies
no legal target row or named downstream detector package.  The
supply-and-target-attachment strategic node remains **OPEN**, and the global
Krenn--Gu conjecture remains **UNRESOLVED**.

The only pre-acceptance findings were tooling-level Ruff defects in the primary
verifier: import-block spacing, a call in an argument default, and two
immediately evaluated loop-variable captures.  They were repaired without
changing the checked identities.  The frozen primary below passes both the
exact replay and pinned Ruff check/format.

## Frozen artifacts

Base HEAD before the candidate package:

```text
a5ec085a0ce29f4acdd33562de626b76b34ef2f6
```

```text
theorem            c441518d2478830001110dc0475c73a1b980e307e12d09223d16c5ca6e8ee4dc
primary verifier   355d037a8f2a0464732b032a5775ed5dcee7b1b4463b4e5e5e265427e667ac2e
no-import audit    f9740aa329f14a11531f463fc040d5e3361e9a86b66a9b95233e5cadf2dfef46
package README     928466f3ceed5e3bff7fda7fd924f9c472e104f107a4a1bf1f52293c09bc2c20
current frontier   bd85c0771e236f860aced1f45c3ffbf22219445f867014abf5fe43a1c417b771
internal DAG       3b626dbdadd31655570c39109dd5ca020a5a74cb0e672f73beccaf3bd59f9b69
```

Reviewed artifacts:

- [full-rank all-response-zero localization theorem](../../claims/arbitrary-order/FOUR_ROOT_FULL_RANK_ALL_RESPONSE_ZERO_OPPOSITE_COLOUR_PURE_COMPLEMENTARY_PERMANENT_LOCALIZATION_THEOREM.md)
- [arbitrary-order package README](../../claims/arbitrary-order/README.md)
- [live frontier](../current-frontier.md)
- [maximum-root supply/target internal DAG](../history/handoffs/MAXIMUM_ROOT_SURPLUS_TWO_SUPPLY_TARGET_NODE_DAG_2026-08-20.md)

## Source, field, and response quantifiers

The physical application starts with an actual hypothetical complex witness
whose maximum-cardinality fully supported torus root has order four and
surplus two.  Thus `Omega=R disjoint-union B`, `|R|=4`, and `|B|=6`.  The
algebraic implication is valid over a characteristic-zero field once the
displayed maximum-root configuration, complete contracted GHZ identity, and
GLS4 pair with `Pi_Q!=0` are supplied.  It does not silently promote the
source theorem establishing that pair from complex witnesses to arbitrary
fields.

For `Q={q_0,q_1}` and `U=B-Q`, the theorem assumes the full physical block
`H=H_Q` is invertible and that all six uncontracted four-slot hafnian tensors

```text
Z_uv=H boxtimes B_uv+A_u boxtimes C_v+A_v boxtimes C_u
```

vanish identically.  These are tensor identities, not vanishing at one
residual contraction or in one response coordinate.  The four-port response
is a conclusion, not a seventh input.  Every conclusion is pointwise on the
declared full-rank chart.

This hypothesis is much narrower than GLS7 alternative `R`.  GLS7 enters `R`
when **at least one** of the six pair responses and four-port response is
identically zero.  The reviewed theorem treats only the literal all-seven-zero
subbranch, using the six pair zeros as input and deriving the seventh.

## Labelled tensor and direct-block audit

The complete contracted six-slot identity is correctly typed with labelled
slots:

```text
sum_(P in binom(B,2)) sh_(P,B-P)(H_P tensor Pi_P)
 =sum_(c=0)^2 mu_c product_(v in B)e_(v,c)^*.
```

The canonical shuffle has coefficient one.  It introduces no factorial,
sign, averaging, or unlabelled symmetrization.  The complementary permanent
`Pi_P` occupies exactly the four labelled slots in `B-P`.

For each pair `u,v` in `U`, evaluation in the two port slots turns `Z_uv=0`
into

```text
bH+a_u c_v^T+a_v c_u^T=0.
```

If `b!=0`, the first term has rank three and the remaining sum has rank at
most two.  Hence `b=0` for every port evaluation and `B_uv=0` as a whole
tensor.  This step uses only `det H!=0`; it does not divide by a response
coordinate, residual contraction, nuisance minor, or selector factor.

## Support, sign, maximum-root, and tau audit

After the direct blocks vanish, the exact relation is

```text
A_u boxtimes C_v+A_v boxtimes C_u=0.
```

Maximum-root maximality first excludes either whole block family being empty:
otherwise `{q_0} union U` or `{q_1} union U`, with fully supported all-ones
vectors, would be a five-vertex torus root.  Equality of the nonzero simple
tensors then makes the two whole-block supports agree.

On two active ports, the `(q_0,u)|(q_1,v)` realignment has one nonzero
rank-one outer product opposite a permuted Kronecker product.  Its rank is
`rank(A_v) rank(C_u)`, and the opposite realignment treats `A_u,C_v`.
Therefore all four active blocks have rank one.  Factor-line uniqueness gives

```text
A_u=s_u a tensor alpha_u,
C_u=t_u c tensor alpha_u,
s_u t_v+s_v t_u=0.
```

For three active ports the ratios `s_u/t_u` would be pairwise negatives, and
the three pair equations force twice a nonzero ratio to vanish.  Characteristic
zero excludes this, so the common support has size one or two.

The normalization in the two-port case is sound.  Absorbing each `s_u` into
its local factor leaves the two `C` coefficients as one common nonzero ratio
with opposite signs.  That common ratio is absorbed into `c`; after writing
the coordinate residual lines as `a=lambda_0 e_i^*` and
`c=lambda_1 e_j^*`, absorbing `lambda_0` into both local factors leaves the
single nonzero scalar `tau=lambda_1/lambda_0`, with opposite signs on the two
ports.  No port-dependent scalar has been silently discarded.

The maximum-root coordinate forcing is also exact.  A noncoordinate covector
over an infinite field has a fully supported torus kernel point.  A nonzero
bilinear form is zero-free on the two endpoint tori exactly when it is one
coordinate monomial.  Consequently both singleton blocks are coordinate
monomials.  In the two-port case both residual factor lines are coordinate,
and at least one of the two local factor lines is coordinate.  The theorem and
the three documentation surfaces preserve this asymmetric local conclusion;
they do not claim that both two-port local factors are coordinate.

Every perfect matching on `Q union U` contains a direct `U-U` edge.  Since all
such blocks are zero, the physical four-port response vanishes without being
assumed or divided by.

## Complete-target projection and divisor ledger

Killing residual coordinate `i` in the `q_0` slot and `j` in the `q_1` slot
splits all fifteen terms in the contracted deck exhaustively:

- the `P=Q` term survives as `H' tensor Pi_Q`;
- the six pairs inside `U` vanish because `B_uv=0`;
- the four `q_0-u` terms are killed by the `q_0` projection; and
- the four `q_1-u` terms are killed by the `q_1` projection.

Thus the projected equation is the projection of the **complete** GHZ tensor,
not an isolated desired coordinate.  If `H'` were zero, `H` would be supported
in one row union one column and would have rank at most two.  Hence the left
side has `Q|U` flattening rank one.

When `i=j`, two nonzero GHZ colours remain.  Their `Q`-side and `U`-side pure
tensors are independently linearly independent, giving flattening rank two
and a contradiction.  When `i!=j`, exactly the third colour `k` remains, and
uniqueness of nonzero simple-tensor factor lines gives

```text
H'=lambda e_(q0,k)^* tensor e_(q1,k)^*,
lambda Pi_Q=mu_k product_(u in U)e_(u,k)^*.
```

The second identity is denominator-free.  The scalar `lambda!=0` is derived,
not saturated in advance.

The saturation ledger is complete for this implication.  The only
physical-block divisor inverted is `det H_Q`.  Source nonvanishing of the
tensor `Pi_Q` is correctly a cover by its coordinate opens, not one invented
canonical scalar.  Active rank-one support charts invert only their selected
nonzero entries.  No `h=H_Q(z_Q)`, raw `p_(A,Q)(z_Q)`, response coordinate,
nuisance or augmented minor, legal selector coefficient, alignment factor, or
target-module denominator is inverted.  The entire divisor `V(det H_Q)` stays
open.

## Sharpness fixture and its exact limitation

The rational ten-vertex fixture has a maximum root of order four, total
outside incidence corank five, `H_Q=I_3`, pure third-colour `Pi_Q`, raw
`p_(A,Q)=1`, and one fully supported contraction with `h=3`.  A disjoint
coordinate-monomial clique cover proves the maximum-root upper bound without
assuming that `H_Q=I_3` itself is a monomial block.  All six pair responses
and the derived four-port response vanish, and the projected target equation
lies on the surviving opposite-colour pure-`Pi_Q` locus.

The fixture does **not** verify the GLS4 conclusion that the order-two
companion for `Q` survives individually modulo every order-four-and-higher
column.  Its raw incidence and common-contraction values cannot be promoted to
that quotient-survival statement.

The fixture is also off the complete GHZ target.  At the displayed mixed
outside word `(0,0,2,2,2,2)`, the `P=Q` contribution equals one and every
other pair-deck contribution is zero.  Thus it is not a hypothetical witness,
not an exact counterexample, and not evidence that the surviving pure locus
meets the witness locus.  It is only a sharp graph-side boundary showing that
maximum-root incidence, the corank quota, raw `p`, nonzero `h`, response zeros,
and the isolated projected equation do not supply the missing complete-mixed
identity.

## Independent evidence and bounded verification

The primary verifier is a focused exact SymPy replay.  It checks the symbolic
rank-three slice obstruction and realignment identity, 81 singleton normal
forms, nine two-port sign forms, determinant and characteristic-two controls,
all nine same/opposite-colour target projections, and every displayed fixture
coefficient.

The no-import audit is independent at the implementation level.  It uses only
the Python standard library and imports neither the primary verifier, project
code, nor SymPy.  Its representations differ materially:

- `Fraction` Gaussian elimination for rank mechanisms;
- Boolean support masks and signed-incidence matrices for support and sign;
- explicit rational torus-zero searches for coordinate forcing;
- labelled perfect-matching reconstruction of four- and six-slot responses;
- a separately implemented root-to-port permanent; and
- independent deck and ten-vertex matching recurrences for the fixture.

The audit reports PASS for `20736` rank-three slices, 15 support-mask pairs,
124 covectors, 834 bilinear blocks, all nine target projections, all 1024
vertex subsets in the maximum-root enumeration, 486 pair-response
coefficients, 729 six-port coefficients, and 945 ten-vertex matchings.

These are bounded exact replays, not the proof of the arbitrary-point
implication.  The written rank, simple-tensor, maximum-root, and complete-target
arguments remain load-bearing.  Neither checker proves anything on
`det H_Q=0`, excludes the opposite-colour pure locus, covers broader
response-zero patterns or nonzero-response absorption, or supplies a
downstream detector.  No Lean or other formal proof is claimed.

## Exact command results

The following commands were rerun on the frozen theorem, primary, and audit
bytes.

```powershell
python claims/arbitrary-order/verify_four_root_full_rank_all_response_zero_opposite_colour_pure_complementary_permanent_localization.py
```

Result: exit `0`, `four-root full-rank response-zero exact replay: PASS`.
The replay reported 9 response slices, 16 Kronecker-rank controls, 81
singleton and 9 two-port normal forms, all 9 target projections, the exact
maximum-root fixture, `Pi_Q=e_2^4`, raw `p=1`, `h=3`, and mixed coefficient
one.

```powershell
python -I claims/arbitrary-order/audit_four_root_full_rank_all_response_zero_opposite_colour_pure_complementary_permanent_localization.py
```

Result: exit `0`,
`four-root full-rank all-response-zero no-import audit: PASS`, with the exact
counts recorded in the preceding section.

Compilation was redirected outside the repository so the read-only review did
not create a local `__pycache__`:

```powershell
$cache=Join-Path ([IO.Path]::GetTempPath()) 'kg-r4-hostile-review-pycache-355d'
python -X pycache_prefix=$cache -m py_compile claims/arbitrary-order/verify_four_root_full_rank_all_response_zero_opposite_colour_pure_complementary_permanent_localization.py claims/arbitrary-order/audit_four_root_full_rank_all_response_zero_opposite_colour_pure_complementary_permanent_localization.py
```

Result: exit `0`.

```powershell
uvx --from ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_four_root_full_rank_all_response_zero_opposite_colour_pure_complementary_permanent_localization.py claims/arbitrary-order/audit_four_root_full_rank_all_response_zero_opposite_colour_pure_complementary_permanent_localization.py
uvx --from ruff==0.16.2 ruff format --check --no-cache claims/arbitrary-order/verify_four_root_full_rank_all_response_zero_opposite_colour_pure_complementary_permanent_localization.py claims/arbitrary-order/audit_four_root_full_rank_all_response_zero_opposite_colour_pure_complementary_permanent_localization.py
```

Results: exit `0`, `All checks passed!`; exit `0`,
`2 files already formatted`.

```powershell
git diff --check
```

Result: exit `0`.  Separate `git diff --no-index --check -- NUL <path>` checks
for each of the three untracked package files returned the expected difference
exit `1` and zero whitespace diagnostics.  Git emitted only the worktree's
ordinary LF-to-CRLF warnings.

The repository hygiene link checker was invoked read-only on the theorem,
package README, current frontier, and internal DAG.  Result: exit `0`, four
Markdown files checked, all local links resolve.  Full index-complete hygiene
was not run because that command requires staging the candidate tree, which
the read-only hostile-review phase did not authorize.

## Frozen proof-DAG ledger

```text
rank-three det(H_Q)!=0 kills every direct U-U block:      PROVED;
common one- or two-port Q-U support:                      PROVED;
coordinate residual factors and exact two-port sign:     PROVED;
four-port response zero from six pair-response zeros:    PROVED;
equal residual colour:                                   EXCLUDED;
opposite-colour pure-third-colour Pi_Q localization:     PROVED;

det H_Q=0 response-zero divisor:                         OPEN;
opposite-colour pure-Pi_Q witness locus empty:           OPEN;
broader GLS7 R branch, including one-zero patterns:      OPEN;
nonzero-response absorption and exceptional fibres:      OPEN;
legal useful row on every four-root witness:             OPEN;
named downstream common-package/synchronization/alignment/
  activity/nuisance/anchor gates:                        OPEN;
supply-and-target-attachment strategic node:             OPEN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

The smallest remaining obligation inside this literal response-zero leaf is a
same-graph complete-mixed companion or integrability identity excluding the
surviving pure locus, or an exact physical point on that locus satisfying
every coefficient of the complete GHZ tensor.  Separately, the determinant
divisor, every weaker response-zero pattern, and every nonzero-response
absorbed or exceptional fibre require coverage.  Even closing those branches
would still require an explicit edge satisfying every hypothesis of one named
downstream detector before the strategic node could close.

There is no claimed permanent restriction, extraction or gluing completion,
global proof, or exact counterexample in this package.
