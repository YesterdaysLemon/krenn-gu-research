# Four-root full-rank pure-survivor exclusion hostile review -- 2026-08-20

## Verdict

**Accepted at the frozen hashes below.  No P0, P1, or P2 defect remains.**

The accepted theorem is an exact characteristic-zero exclusion of one narrow
root-order-four witness branch.  Start with an actual maximum-root surplus-two
ternary GHZ hypothetical witness and the residual pair \(Q\) supplied by GLS4.
If the physical block \(H_Q\) is invertible and all six same-\(Q\) physical
pair-response tensors vanish identically, then the complete contracted GHZ
target is inconsistent.  Equivalently, on this full-rank chart at least one of
the six pair responses must be nonzero.  GLS9 derives the seventh, four-port,
response zero from the six inputs, so the result excludes the full-rank part of
the literal all-seven-zero leaf.

This is a pointwise witness-locus exclusion, not a local support atlas and not
a target-attachment theorem.  It does not cover \(\det H_Q=0\), a pattern in
which only some responses vanish, any nonzero-response absorbed or exceptional
fibre, or any root order other than four.  It supplies no named downstream
selector package.  The supply-and-target-attachment strategic node remains
**OPEN**, and the global Krenn--Gu conjecture remains **UNRESOLVED**.

The only pre-acceptance finding was a P2 scope imprecision in the three summary
surfaces.  They initially said that both diagonal fibres used the same one or
two local lines.  On the singleton shore the two residual shores can have
independent local factors, and only the first fibre is needed.  The summaries
were repaired before this freeze: the singleton now dies solely in the
\((i,i)\) fibre, while shared local lines are asserted only in the two-port
normal form.  The theorem and both checkers already made that distinction, so
the repair changed no proof or computation.

## Frozen artifacts

Base HEAD and contemporaneous origin/main before the theorem package:

~~~text
df394d387d246d4331359a9ce0f16d7700f724bb
~~~

Reviewed theorem package:

~~~text
theorem
  61550677438b34a3ce8db837d5cff880356345482f52fc87b43b9c6f2190377a
primary verifier
  03d9f95c1bd85db0ae3b60d4e79df463ee178043a30f7a9cb3feda2a829884e1
independent no-import audit
  ba910528bb07aad159e197e085edfd0b74adb5cdfadeeb16a56d7a93ed8ded32
exact discovery probe
  87cdacecb69ab5861c57c43207d0109efb8724e780bab932adb1fa74173aa27e
discovery-probe handoff
  154929dc4550782d477bc1224a44a049e414d5085e8194f56c262659c99bb7bd
package README
  5459a6c2c48f6f9860525c5d9fdd086ffb5f18af61c98f05bf103c9537374a27
current frontier
  1efc5ab4b15a40937860ae9b450d0048332be0fb5deae654fae2879e4b442dfd
internal proof DAG
  aa2c0d959c74375a47b41cf3d6c27d409beb535228a017f3308e128282ebd827
~~~

Load-bearing merged dependencies and replay implementations:

~~~text
GLS9 theorem
  c441518d2478830001110dc0475c73a1b980e307e12d09223d16c5ca6e8ee4dc
GLS9 primary
  355d037a8f2a0464732b032a5775ed5dcee7b1b4463b4e5e5e265427e667ac2e
GLS9 no-import audit
  f9740aa329f14a11531f463fc040d5e3361e9a86b66a9b95233e5cadf2dfef46
GLS4 theorem
  f887dd58c724160fa7b52df24385f7f89311ac410373c636069e7b420b027466
GLS4 primary
  d73c8ed6882eea8ae3e46aad1fce4781fbc7bf2140353b8e805c347af716d474
GLS4 no-import audit
  4232fd5e0e5648fedaa8d57c31c64bd492dbf6d7c2a9fbd6042028ba6d6e06a0
~~~

Reviewed artifacts:

- [full-rank pure-survivor exclusion theorem](../../claims/arbitrary-order/FOUR_ROOT_FULL_RANK_ALL_RESPONSE_ZERO_PURE_COMPLEMENTARY_PERMANENT_SURVIVOR_EXCLUSION_THEOREM.md)
- [focused primary verifier](../../claims/arbitrary-order/verify_four_root_full_rank_all_response_zero_pure_complementary_permanent_survivor_exclusion.py)
- [independent no-import audit](../../claims/arbitrary-order/audit_four_root_full_rank_all_response_zero_pure_complementary_permanent_survivor_exclusion.py)
- [exact discovery probe](../../tools/explore/r4_pure_pi_survivor_exact_probe.py)
- [discovery-probe handoff](../history/handoffs/R4_PURE_PI_SURVIVOR_EXACT_PROBE_2026-08-20.md)
- [arbitrary-order package README](../../claims/arbitrary-order/README.md)
- [live frontier](../current-frontier.md)
- [maximum-root supply/target internal DAG](../history/handoffs/MAXIMUM_ROOT_SURPLUS_TWO_SUPPLY_TARGET_NODE_DAG_2026-08-20.md)
- [GLS9 localization theorem](../../claims/arbitrary-order/FOUR_ROOT_FULL_RANK_ALL_RESPONSE_ZERO_OPPOSITE_COLOUR_PURE_COMPLEMENTARY_PERMANENT_LOCALIZATION_THEOREM.md)
- [GLS4 same-pair source theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_THEOREM.md)

## Source and quantifier audit

The physical application has

~~~text
Omega=R disjoint-union B,  |R|=4,  |B|=6,
Q={q0,q1},                 U=B-Q,  |U|=4.
~~~

The root is a maximum-cardinality fully supported torus root, the complete
contracted six-slot graph tensor is the ternary GHZ target, and all three
contracted pure weights are nonzero.  GLS4 supplies the same physical pair
\(Q\) with \(\Pi_Q\ne0\).  The new theorem adds exactly

~~~text
det H_Q != 0,
H_(Q union {u,v}) = 0 for every pair {u,v} in U.
~~~

The six equations are identities of the full four-slot physical response
tensors, not values at one residual contraction, one response coordinate, or
one chosen selector.  GLS9 is pointwise on this chart.  It proves that all
direct \(U\)-to-\(U\) blocks vanish, that the two \(Q\)-to-\(U\) block families
have one common nonempty support \(T\) of size one or two, and that the
residual colours \(i,j\) are distinct.  If \(k\) is the third colour, GLS9 also
gives one derived \(\lambda\ne0\) with

~~~text
(rho_i tensor rho_j)H_Q
  =lambda e_(q0,k) tensor e_(q1,k),
lambda Pi_Q=mu_k e_k^U.
~~~

The singleton and two-port normal forms are the complete GLS9 support cover.
No genericity, sampled support mask, or unproved finite atlas is inserted by
the successor theorem.

## Independent derivation of the exclusion

### Residual-block pivots

Order the residual colours as \((i,j,k)\).  The projected GLS9 identity forces

~~~text
H_Q =
[[H_ii, H_ij, H_ik],
 [0,    H_jj, 0   ],
 [0,    H_kj, lambda]].
~~~

Direct determinant expansion gives

~~~text
det H_Q=H_ii H_jj lambda.
~~~

Thus \(H_{ii}\) and \(H_{jj}\) are nonzero consequences of the declared
full-rank chart and the derived \(\lambda\ne0\).  They are not extra saturated
entries.

### The complete \((i,i)\) fibre

The fifteen labelled pair-deck terms split without multiplicity:

- one \(P=Q\) term gives \(H_{ii}\Pi_Q\);
- all six \(P\subset U\) terms vanish because their physical blocks vanish;
- all four \(P=\{q_1,u\}\) terms vanish because their residual factor has
  colour \(j\ne i\); and
- among the four \(P=\{q_0,u\}\) labels, exactly the active ports contribute.

After multiplying, not dividing, by \(\lambda\) and using
\(\lambda\Pi_Q=\mu_k e_k^U\), the complete 81-coordinate fibre is

~~~text
sum_(u in T) sh_u(hat(alpha)_u tensor lambda D_u^i)
  =lambda mu_i e_i^U-mu_k H_ii e_k^U.
~~~

Both displayed pure coefficients are nonzero.  If \(T\) is a singleton,
quotient its active labelled slot by its nonzero local line.  The insertion
dies, while the two pure tensors on the other three labelled slots are
independent.  Both coordinate vectors in the active slot would have to lie in
one line, which is impossible.

If \(T=\{s,t\}\), quotient the \(s\)- and \(t\)-slots by their respective
local lines.  Both insertion summands die.  Since the two pure tensors on the
remaining two labelled slots are independent, the \(i\)-coordinate line must
occur at one active site and the \(k\)-coordinate line at the other.  A single
local line cannot contain two independent coordinate vectors, so this is the
exact labelled cover

~~~text
{col(alpha_s),col(alpha_t)}={i,k}.
~~~

This argument is coordinate-free apart from naming the two target coordinate
lines.  It covers every nonzero local covector line, not a finite list of
projective representatives.

### The complete \((j,j)\) fibre

Only the two-port branch remains.  Here GLS9's opposite-sign normal form uses
the same fixed local covectors on both residual shores:

~~~text
A_s=e_i tensor alpha_s,       A_t=e_i tensor alpha_t,
C_s=tau e_j tensor alpha_s,   C_t=-tau e_j tensor alpha_t.
~~~

The fifteen labels split symmetrically.  The \(Q\) term gives
\(H_{jj}\Pi_Q\), the six direct terms vanish, every \(q_0\)-shore term is
killed by \(i\ne j\), and only the two active \(q_1\)-shore insertions remain.
Keeping the nonzero scalar and its sign inside the exact companion slices
gives

~~~text
D_s^j= tau Pi_({q1,s})[q0=j],
D_t^j=-tau Pi_({q1,t})[q0=j],

sh_s(alpha_s tensor lambda D_s^j)
 +sh_t(alpha_t tensor lambda D_t^j)
 =lambda mu_j e_j^U-mu_k H_jj e_k^U.
~~~

The same active-slot quotient therefore forces

~~~text
{col(alpha_s),col(alpha_t)}={j,k}.
~~~

The two covers cannot both hold because \(i,j,k\) are distinct.  This
exhausts the GLS9 singleton/two-port cover and proves the claimed contradiction.

The argument can equivalently be written with annihilating covectors: choose,
at each active site, a covector killing its local line.  Applying their tensor
product kills every insertion.  Independence on the untouched labelled slots
separates the two pure target colours and forces the same coordinate-line
incidence.  This dual derivation is materially different from choosing
quotient coordinates and confirms that no selected line entry is being
inverted.

## Saturation, field, and divisor audit

The proof retains the following exact ledger.

1. The only physical-block divisor is \(D(\det H_Q)\).  Its complement remains
   open.
2. The three \(\mu_c\) are source nonzeros.  \(\Pi_Q\ne0\) is inherited from
   GLS4, and the pure identity with \(\lambda\) is a GLS9 conclusion.
3. The pivots \(H_{ii},H_{jj}\) are derived from the determinant monomial; they
   are not independently declared nonzero.
4. Active local factors are nonzero because they index active whole blocks.
   Forming their one-dimensional subspaces or annihilators does not divide by
   a chosen coordinate.
5. The proof multiplies each fibre by \(\lambda\); it never divides by
   \(\lambda\), a companion coordinate, response coordinate, selector,
   nuisance minor, alignment factor, or target-module denominator.
6. The quotient lemma itself works over every field.  Characteristic zero
   enters through GLS9: infinitude is used for maximum-root coordinate forcing,
   and \(2\ne0\) is used to prove \(1\le|T|\le2\).  No exceptional
   characteristic is silently discarded.

The determinant-divisor and three-active-line controls are correctly labelled
as abstract proof-boundary controls, not target points or witnesses.  If one
pivot vanishes, a diagonal fibre can lose one pure summand.  With three active
coordinate lines, the two fibres can use \(\{i,k\}\) and \(\{j,k\}\)
separately.  Neither control weakens the theorem on its declared chart.

## Verification independence and provenance

The focused primary is a SymPy implementation.  It materializes every one of
the 15 labelled deck terms for all 81 port words in each diagonal fibre, both
support normal forms, and all six ordered colour triples.  It checks the
symbolic determinant pivot, general singleton rank minor, exact fibre
rearrangement, bounded rational quotient-line controls, determinant and
three-line sharpness controls, and the displayed GLS9 fixture coefficient.

The no-import audit imports neither the primary, repository modules, nor
SymPy.  It uses standard-library integer and Fraction arithmetic, primitive
rational projective lines, dual annihilator incidence instead of quotient
coordinates, a separate determinant expansion, a separately constructed
labelled pair deck, and an independent perfect-matching recurrence.  Its
representation and derivation therefore differ materially from the primary.

Both programs explicitly say that their finite line censuses and coefficient
replays are not the arbitrary-point proof.  The written labelled quotient or
dual-annihilator argument is load-bearing.

The exploratory 729-coefficient probe works in a larger relaxed module in
which active non-\(Q\) complementary permanents are independent tensors.
Its 216 singleton charts and 648 covering two-port charts expose the same
minor and line-cover obstruction.  This is exact theorem-discovery provenance,
but it is not a physical incidence-integrability proof, an arbitrary-root
argument, a named selector package, or a global counterexample.  Its rational
GLS9 fixture fails exactly six of the 729 target coefficients and is correctly
recorded as an off-target control.

## Exact command results

The following commands were rerun against the frozen publication bytes.

~~~powershell
python claims/arbitrary-order/verify_four_root_full_rank_all_response_zero_pure_complementary_permanent_survivor_exclusion.py
~~~

Result: exit \(0\), focused replay PASS.  It reported 1,944 complete fibre-word
checks, 29,160 labelled pair-term checks, six determinant pivots, six
singleton rank minors, 288 singleton quotient charts, three symbolic quotient
charts, 13,824 ordered rational two-line charts, 972 three-line coefficients,
486 determinant-boundary coefficients, and fixture coefficient
\(002222=1\).

~~~powershell
python -I claims/arbitrary-order/audit_four_root_full_rank_all_response_zero_pure_complementary_permanent_survivor_exclusion.py
~~~

Result: exit \(0\), independent no-import audit PASS.  It reported 49 rational
projective lines, 147 singleton cases, 7,203 ordered two-site cases, exactly
six sharp coordinate covers, no two-line three-colour cover, 15,625 rational
pivot specializations, both 81-coordinate diagonal fibres, all 15 pair labels,
all 729 fixture outside words, and all 945 ten-vertex perfect matchings.

~~~powershell
python tools/explore/r4_pure_pi_survivor_exact_probe.py
~~~

Result: exit \(0\).  The exact relaxed probe reported 216 singleton charts and
648 covering two-port charts excluded, no complete contracted-target point,
no actual witness, and the six exact off-target residual coefficients.

Focused dependency replays:

~~~powershell
python claims/arbitrary-order/verify_four_root_full_rank_all_response_zero_opposite_colour_pure_complementary_permanent_localization.py
python -I claims/arbitrary-order/audit_four_root_full_rank_all_response_zero_opposite_colour_pure_complementary_permanent_localization.py
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_same_pair_survival_and_permanent_dominance.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_same_pair_survival_and_permanent_dominance.py
~~~

Results: all four exited \(0\).  GLS9 primary and audit both reported PASS,
including the source normal forms, all target projections, the 729
six-port coefficients, and the exact maximum-root fixture.  GLS4 primary and
audit both reported PASS for their bounded exact source replays; both preserve
that arbitrary-root coverage comes from the written theorem, not the finite
audit.

Compilation and pinned formatting checks:

~~~powershell
$kgReviewCache=Join-Path ([IO.Path]::GetTempPath()) 'kg-r4-pure-survivor-hostile-review-03d9'
python -X pycache_prefix=$kgReviewCache -m py_compile claims/arbitrary-order/verify_four_root_full_rank_all_response_zero_pure_complementary_permanent_survivor_exclusion.py claims/arbitrary-order/audit_four_root_full_rank_all_response_zero_pure_complementary_permanent_survivor_exclusion.py tools/explore/r4_pure_pi_survivor_exact_probe.py
uvx --from ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_four_root_full_rank_all_response_zero_pure_complementary_permanent_survivor_exclusion.py claims/arbitrary-order/audit_four_root_full_rank_all_response_zero_pure_complementary_permanent_survivor_exclusion.py tools/explore/r4_pure_pi_survivor_exact_probe.py
uvx --from ruff==0.16.2 ruff format --check --no-cache claims/arbitrary-order/verify_four_root_full_rank_all_response_zero_pure_complementary_permanent_survivor_exclusion.py claims/arbitrary-order/audit_four_root_full_rank_all_response_zero_pure_complementary_permanent_survivor_exclusion.py tools/explore/r4_pure_pi_survivor_exact_probe.py
~~~

The actual pinned Ruff invocations included all three package Python files.
Results: compilation exit \(0\); Ruff check exit \(0\), “All checks passed!”;
Ruff format check exit \(0\), “3 files already formatted”.

~~~powershell
git diff --check
~~~

Result: exit \(0\).  Git emitted only the worktree's ordinary LF-to-CRLF
warnings for the three edited documentation files.

## Frozen proof-DAG and open-boundary ledger

~~~text
GLS4 same-pair physical block and individual higher-column survival:
  PROVED upstream;
GLS9 full-rank literal response-zero localization:
  PROVED upstream;
singleton opposite-colour pure-Pi_Q survivor on det H_Q nonzero:
  EXCLUDED here;
two-port opposite-colour pure-Pi_Q survivor on det H_Q nonzero:
  EXCLUDED here;
full-rank literal all-seven response-zero leaf at root order four:
  EXCLUDED here;

det H_Q=0 literal response-zero divisor:
  OPEN;
one-zero and every weaker GLS7 R response pattern:
  OPEN;
nonzero-response absorption and exceptional nuisance fibres:
  OPEN;
root order three and every root order at least five:
  NOT ADDRESSED here;
legal same-Q constant selector and nonzero response:
  OPEN;
full nuisance survival, synchronization, augmented alignment, activity,
target-pure anchor, and every other named downstream hypothesis:
  OPEN;
supply-and-target-attachment strategic node:
  OPEN;
permanent restriction, extraction, and gluing:
  OUTSIDE this package and OPEN;
global Krenn--Gu conjecture:
  UNRESOLVED.
~~~

The smallest remaining obligation on this literal response-zero lane is the
divisor \(\det H_Q=0\).  The broader strategic node still needs a pointwise
complete-mixed exclusion or a full legal named-interface output for every
weaker response-zero, nonzero-response absorbed, and exceptional-rank branch.
No theorem in this package turns its clean local contradiction into that
missing exhaustive source-to-interface edge.

No apparent exact global counterexample, contradiction with a live theorem,
or candidate global resolution was found.
