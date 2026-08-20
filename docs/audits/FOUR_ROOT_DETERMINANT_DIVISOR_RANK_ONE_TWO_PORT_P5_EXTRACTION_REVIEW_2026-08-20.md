# Hostile review: four-root rank-one two-port \(P_5\) extraction

Date: 2026-08-20

## Verdict

**PASS, at the theorem's stated pointwise characteristic-zero scope.**

The reviewed package proves the following conditional source-to-downstream
edge.  Start with an actual hypothetical ternary GHZ witness whose
maximum-cardinality torus root has order four and surplus two.  Fix the GLS4
residual pair \(Q=\{q_0,q_1\}\), assume all six same-\(Q\) pair responses
vanish, and enter the rank-one Branch-III two-port normal form supplied by
GLS11 and GLS12.  Then the complete mixed target identities and the one common
physical four-root incidence family force five injective local maps whose
pullback of \(P_5\) is

\[
\mu_i e_i^{\otimes5}+\mu_j e_j^{\otimes5}+\mu_k e_k^{\otimes5},
\qquad
\mu_i\mu_j\mu_k\ne0.
\]

An invertible diagonal change on one target mode therefore gives an ordinary
\(P_5\to\Delta_3\) restriction.  The physical six-vertex response that is
separate in the general determinant-divisor reduction is also zero term by
term on this two-port branch.

This is a downstream permanent-extraction edge, not an exclusion of the
branch.  It supplies no physical residual vertex, GLD selector, alignment,
synchronization, activity, nuisance-survival, or target-pure-anchor package.
The unrestricted \(P_5\to\Delta_3\) problem, rank-one Branches I and II,
weaker response-zero patterns, nonzero-response absorption and exceptional
fibres, the named same-\(Q\) selector package, and the strategic
supply-and-target node remain open.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

No P0, P1, or P2 defect remains in the frozen package reviewed below.

## Frozen review surface

The worktree HEAD before publication was

~~~text
e9a6c42636f3bfa18dda4d1228d5971fac98d239
~~~

The reviewed uncommitted publication bytes were frozen by SHA-256:

| artifact | SHA-256 |
| --- | --- |
| [theorem](../../claims/arbitrary-order/FOUR_ROOT_DETERMINANT_DIVISOR_RANK_ONE_TWO_PORT_P5_EXTRACTION_THEOREM.md) | c14479a51c69d5e2d3b0c85aef5b98c926383db7513a390e2daa5e9dcaa0333c |
| [focused primary verifier](../../claims/arbitrary-order/verify_four_root_determinant_divisor_rank_one_two_port_p5_extraction.py) | 5d81c0d6f2b0ebb310fa276fdb169b4278b5cd75c9cfd0368a9005dc6d444704 |
| [independent no-import audit](../../claims/arbitrary-order/audit_four_root_determinant_divisor_rank_one_two_port_p5_extraction.py) | 5203ac23bf9f3b583f88d7a8ad2dddb9f9ad8fd93fd249dbb04783bcf2772ef4 |
| [arbitrary-order navigation](../../claims/arbitrary-order/README.md) | f093488155fcd5119e596d7562559c1be69b073fc089c285bd8578b5953f0af0 |
| [live frontier](../current-frontier.md) | 32ca546911abd18fde3cacb8edc06163a7f7efd29fad88ddc985b0dac59da2f1 |
| [supply/target node DAG](../history/handoffs/MAXIMUM_ROOT_SURPLUS_TWO_SUPPLY_TARGET_NODE_DAG_2026-08-20.md) | f80629a72ab582f8294f023a50961599a7736395146c7523eababf5e34f87976 |

The theorem's dependencies GLS4, GLS11, GLS12, and the order-five permanent
frontier were read only to check the inherited interface and downstream stop.
The present review does not re-prove those owning packages.

## Independent hostile derivation

The following derivation was completed before opening the no-import audit.
Agreement with that audit was therefore not used as a substitute for
independent reasoning.

### 1. Coordinate pairing is exhaustive

On the inherited two-port branch, after relabelling the ports if necessary,

~~~text
A_s=e_(q0,i)^* tensor alpha_s
A_t=e_(q0,i)^* tensor alpha_t
C_s=tau e_(q1,j)^* tensor alpha_s
C_t=-tau e_(q1,j)^* tensor alpha_t
H=gamma e_(q0,k)^* tensor e_(q1,k)^*
~~~

where \(i,j,k\) are distinct, every other \(A,C\) block is zero, every
internal \(B\)-edge is zero, and at least one of
\(\alpha_s,\alpha_t\) is coordinate.  Put
\(\alpha_s=a e_{s,d}^*\) after exchanging \(s,t\) if required.

- If \(d=i\), quotient the \(q_0\)- and \(s\)-slots by their
  colour-\(i\) lines.  The two \(A\)-terms and \(C_s\) vanish.  Only \(C_t\)
  remains against the nonzero pure-\(j\) target, so factor-line uniqueness
  forces \(\alpha_t\in K^*e_{t,j}^*\).
- If \(d=j\), the symmetric quotient in the \(q_1\)- and \(s\)-slots leaves
  only \(A_t\) and the pure-\(i\) target.  Hence
  \(\alpha_t\in K^*e_{t,i}^*\).  Exchanging \(s,t\) and replacing
  \(\tau\) by \(-\tau\) gives the same normal form as the first case.
- If \(d=k\), quotient the \(s\)-slot by its colour-\(k\) line.  The two
  surviving source terms share the same \(t\)-factor \(\alpha_t\), so their
  \(t\mid B-\{t\}\) flattening has rank at most one.  The surviving
  pure-\(i\) and pure-\(j\) target summands have independent \(t\)-lines and
  independent complementary tags, hence rank two.  This is impossible.

Thus, without an undeclared divisor,

~~~text
alpha_s=a e_(s,i)^*,       alpha_t=b e_(t,j)^*,
a b tau gamma mu_i mu_j mu_k != 0.
~~~

### 2. The common-tail table has the exact \(8+4\) source split

Define

~~~text
S_c=L_s[:,c],     T_c=L_t[:,c],
X=L_(q1)[:,i],    Y=L_(q0)[:,j],
Kcal(u,v)=P_4(u,v,L_m,L_n).
~~~

The shore orientation is load-bearing: the pure-\(i\) \(A_s\)-term leaves
the \(q_1,t\) columns \(X,T_i\), while the pure-\(j\) \(C_t\)-term leaves
the \(q_0,s\) columns \(Y,S_j\).

The two pure coefficients of the complete mixed identity and the pure
companion identity give

~~~text
a Kcal(X,T_i)=mu_i I_i
-tau b Kcal(Y,S_j)=mu_j I_j
gamma Kcal(S_k,T_k)=mu_k I_k.
~~~

Six complete mixed-target words in slot order \((q_0,q_1,s,t)\),

~~~text
[j,j,i,i], [i,i,i,k], [j,j,i,k],
[i,i,j,j], [j,j,k,j], [i,i,k,j],
~~~

have exactly one surviving physical term.  Their nonzero multipliers are,
respectively,

~~~text
tau a, a, tau a, b, -tau b, b.
~~~

They force

~~~text
Kcal(T_i,Y)=0, Kcal(T_k,X)=0, Kcal(T_k,Y)=0,
Kcal(S_j,X)=0, Kcal(S_k,Y)=0, Kcal(S_k,X)=0.
~~~

The \((s,t)\)-slices \([j,i],[j,k],[k,i]\) of the pure-\(k\) companion
identity force

~~~text
Kcal(S_j,T_i)=0, Kcal(S_j,T_k)=0, Kcal(S_k,T_i)=0.
~~~

This is exactly eight relations from the complete mixed target and four from
the pure companion: three diagonal identities and nine zero identities.  The
same labelled \(L_m,L_n\) occur in every relation.  Independent abstract
companion tensors would not yield this common bilinear map.

### 3. The Latin \(P_5\) splice has the claimed signs and complete coverage

In \(K^5=K^4\oplus K e_*\), extend \(L_m,L_n\) by a zero bottom row and
use the three synthetic column tables

~~~text
             colour i       colour j          colour k
D_0          a e_*          iota(S_j)         iota(S_k)
D_1          iota(T_i)      -tau b e_*        iota(T_k)
D_2          iota(X)        iota(Y)           gamma e_*.
~~~

For a colour triple on \(D_0,D_1,D_2\):

- no bottom-only column gives five columns in a four-dimensional top
  subspace, hence zero;
- at least two bottom-only columns require two proportional bottom columns
  to occupy one row, hence zero;
- exactly one bottom-only column leaves its scalar times one four-by-four
  permanent with the common tails.

The exactly-one-bottom triples are exhausted by the following twelve routes:

~~~text
iii -> a Kcal(T_i,X)       jjj -> -tau b Kcal(S_j,Y)
kkk -> gamma Kcal(S_k,T_k)

iij -> Kcal(T_i,Y)         iki -> Kcal(T_k,X)
ikj -> Kcal(T_k,Y)         jji -> Kcal(S_j,X)
kjj -> Kcal(S_k,Y)         kji -> Kcal(S_k,X)
jik -> Kcal(S_j,T_i)       jkk -> Kcal(S_j,T_k)
kik -> Kcal(S_k,T_i).
~~~

The first three are the diagonal relations and the last nine vanish.  The
triple split is therefore

~~~text
diagonal 3, zero-relation 9, structural 15; total 27.
~~~

Retaining the full two-tail tensors accounts for all \(3^5=243\) target
coefficients.  The bottom signs \(a,-\tau b,\gamma\) reproduce the three
weighted pure coefficients without division.

The resulting tensor has one-mode flattening rank three at all five modes.
Pullback flattening rank is bounded by local-map rank, so all five
three-dimensional-domain maps have rank three and are injective.  This
discharges the repository's actual \(P_5\)-restriction interface, rather than
merely displaying a possibly nonconcise pullback.

### 4. The seventh response is termwise zero

There are fifteen perfect matchings on \(Q\cup U\).

- A matching using \(H\) leaves the four vertices of \(U\) to two internal
  \(B\)-edges, all of which are zero.
- A matching not using \(H\) must attach \(q_0,q_1\) to the only active ports
  \(s,t\).  It then leaves \(m,n\) on the zero edge \(B_{mn}\).

Thus no cancellation or response-coordinate division is involved.  This is
not the opposite-sign cancellation in the four-vertex pair response.

### 5. The \(P_6\) comparison is only a sharpness check

The two-extra-row augmentation has precisely five nonzero bottom two-column
permanents:

~~~text
(q0,q1): tau,  (q0,s): a,  (q0,t): b,
(q1,s): tau a, (q1,t): -tau b.
~~~

The \(s,t\) bottom permanent cancels.  Laplace expansion therefore gives

\[
P_6(\widetilde L_v)
=
\mu_i e_i^{\otimes6}
+\mu_j e_j^{\otimes6}
+\frac{\tau\mu_k}{\gamma}
e_{q_0,i}\otimes e_{q_1,j}\otimes e_k^{\otimes U}.
\]

This tensor is not locally equivalent to a concise weighted \(\Delta_3\):
its \(q_0\)- and \(q_1\)-mode flattenings have rank two, whereas every
one-mode flattening of \(\Delta_3\) has rank three.  The comparison explains
the five-mode Latin splice but is not load-bearing for the extraction.

## Field, divisor, and scope audit

The arbitrary-point proof is exact over a characteristic-zero field; the
actual witness application is over \(\mathbb C\).  No generic point,
finite-field result, numerical sample, or support-mask inference enters the
proof.

The only scalars used as nonzero are

~~~text
a, b, tau, gamma, mu_i, mu_j, mu_k.
~~~

They are inherited active or target scalars.  Zero common-tail relations use
only cancellation by these declared nonzero factors.  The \(P_5\) splice
keeps their multiplied signs, target normalization uses the declared
\(\mu_c\ne0\), and the optional \(P_6\) display uses the declared
\(\gamma\ne0\).  No response coordinate, observable minor, nuisance
determinant, selector coefficient, alignment form, GLD activity gate, or
target-pure-anchor factor is inverted.

The proof genuinely uses complete mixed coefficients beyond the pure and
Hamming-one shells.  It does not claim, without a separate countermodel, that
those shells are logically insufficient on this exact inherited locus.

## Verification and independence audit

The focused primary verifier uses SymPy symbolic expressions.  It checks:

- all three coordinate-factor quotient cases and the two exact quotient
  nullspaces;
- the three diagonal and nine zero common-tail routes;
- all 243 \(P_5\) coefficients by all 120 permanent permutations;
- all fifteen physical matchings at all 729 six-mode colour words; and
- the signed \(P_6\) Laplace decomposition over all 729 words and all 720
  permutations.

The no-import audit was opened only after this hostile derivation and after
the audit agent reported completion.  It imports no repository module and
uses the Python standard library only.  Its representation differs
materially: exact Fraction scalars, sparse row-assignment polynomials,
recursive perfect matchings, and direct permutation grouping.  It checks the
same displayed finite interface but expressly leaves arbitrary-point
quotient implications to the written theorem.  This is genuinely independent
finite replay, not merely a renamed import of the primary verifier.

Subagent agreement was not treated as proof.  The written arbitrary-point
argument, the symbolic primary replay, the sparse no-import replay, and this
hostile derivation play distinct evidentiary roles.

## Defects found and repaired before freeze

The hostile pass found the following defects in earlier candidate bytes.  All
were repaired and rechecked before the hashes above were frozen.

1. **P2, \(P_6\) invariant justification.**  An earlier draft inferred
   non-equivalence to \(\Delta_3\) from a mismatched displayed word alone.
   The final proof uses the invariant one-mode flattening ranks \(2\ne3\).
2. **P2, primary quotient replay.**  The first primary draft displayed the
   quotient coordinates of a generic \(\alpha_t\) but did not assert the
   quotient nullspaces.  The final primary verifies that they are exactly
   \(K e_j\) and \(K e_i\).
3. **P1, proof-DAG sibling edge.**  An intermediate frontier draft routed
   Branches I/II and broader response/absorption leaves out of GLS13, although
   GLS13 owns only Branch III two-port.  The final frontier retains the direct
   GLS12-to-open edge for Branches I/II and keeps broader leaves on their
   actual GLS7/GLS8 source edges.  GLS13 points only to the downstream
   \(P_5\) node.
4. **P2, tranche provenance.**  An intermediate DAG header paired the new
   continuation branch with the stale original determinant-tranche base.
   The final DAG distinguishes the original base from the current
   \(e9a6c426\) two-port-tranche base.
5. **P2, injective restriction interface.**  Equality (21) was initially
   called a restriction without spelling out injectivity.  The final proof
   derives rank three for all five maps from the concise output flattenings.
6. **P2, shell-sufficiency wording.**  An earlier scope sentence claimed
   pure and Hamming-one equations could not imply the result, without a
   locus-specific countermodel.  The final statement makes only the proved
   claim that this derivation uses higher mixed coefficients.
7. **P2, promotion markers.**  Final-freeze scanning found and removed stale
   uses of “candidate package” in the theorem and “candidate two-port
   theorem” in the node DAG.

No defect was waived.

## Exact commands and results

From the isolated worktree

~~~text
C:\w\kg-supply-target-node-rank1-20260820
~~~

the final focused replay was:

~~~text
python claims/arbitrary-order/verify_four_root_determinant_divisor_rank_one_two_port_p5_extraction.py

PASS
coordinate pairing: 3 quotient cases, 2 forced lines, forbidden rank 2
common tails: 3 diagonal + 9 zero = 12, split 8+4
P5: 243 coefficients, 29,160 permutation terms, split (3,9,15)
seventh response: 15 matchings, 10,935 termwise-zero evaluations
P6: 135 bottom coefficients, 729 routes, 524,880 permutation terms
~~~

The independent replay was:

~~~text
python claims/arbitrary-order/audit_four_root_determinant_divisor_rank_one_two_port_p5_extraction.py

PASS coordinate-pairing
PASS common-tail-routing
PASS P5-row-assignments
PASS six-vertex-matchings
PASS P6-sign-sharpness
PASS scope-controls
PASS independent rank-one two-port P5 extraction audit
~~~

Static and patch hygiene were:

~~~text
python -m ruff check \
  claims/arbitrary-order/verify_four_root_determinant_divisor_rank_one_two_port_p5_extraction.py \
  claims/arbitrary-order/audit_four_root_determinant_divisor_rank_one_two_port_p5_extraction.py

All checks passed!

git diff --check

PASS
~~~

A final targeted stale-marker scan found no remaining candidate or pending
status attached to this theorem, GLS13, or the two-port package.  The word
“candidate” remaining as a local variable name inside the no-import audit is
not a lifecycle marker.

All theorem, verifier, audit, navigation, frontier, DAG, and review-link
targets were checked to exist at the frozen worktree paths.  Repository-wide
candidate-tree QA, exact-head hosted CI, commit/push, and merge are publication
steps outside this review record and must be reported separately.

## Final boundary

What is proved:

- every actual point in the exact inherited rank-one Branch-III two-port
  locus yields the displayed injective weighted \(P_5\) restriction;
- all 243 coefficients of the splice follow from the twelve common-tail
  relations;
- the seventh physical response is termwise zero on this branch; and
- no undeclared exceptional divisor is removed.

What is not proved:

- nonexistence of the resulting structured or unrestricted
  \(P_5\to\Delta_3\) restriction;
- exclusion or target attachment for rank-one Branch I or II;
- coverage of weaker response-zero, nonzero-response absorption, or
  exceptional-fibre branches;
- a legal same-\(Q\) GLD response/target selector package;
- closure of the maximum-root surplus-two supply-and-target strategic node;
- permanent nonrestriction, extraction/gluing completion, or resolution of
  the global conjecture.

The smallest remaining obligation on this particular Branch-III leaf is the
downstream structured \(P_5\) permanent problem.  The smallest remaining
source obligations inside the active strategic node are rank-one Branches I
and II together with the broader response-zero and
absorption/exceptional-fibre cover.  The global Krenn--Gu status remains
**UNRESOLVED**.
