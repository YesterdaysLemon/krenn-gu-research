# GLD102 p=0,1 nonzero-offset exclusion hostile review

## Verdict

**Verdict: PASS for the exact scoped GLD102 implication.**  The tracked
primary and no-import audit independently establish that, on the normalized
GLD88 H4/Q6 offset chart in characteristic zero, for `p=0` or `p=1`,
arbitrary `a`, and `D(Delta)`, a complete-syndrome rank bound of six forces
`B=C=0`.

The accepted status is **Proved exact scoped characteristic-zero theorem
(GLD102)**.  It is not an endpoint exclusion or physical empty-set theorem.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Exact claim audited

The proposition under review is

~~~text
p in {0,1}, Q6=0, Delta!=0, rank M(G)<=6  =>  B=C=0,
~~~

where `M(G)` is the complete `37 x 9` GLD71 syndrome and `B,C` are the affine
offsets from the written GLD88/F88 family.  The parameter `a` remains
symbolic.  The nonzero-offset cover is set-theoretically exhaustive:

~~~text
(B,C)!=(0,0) = D(B) union (V(B) intersect D(C)).
~~~

No other chart or fibre is imported into that equality.

## 1. Rank-to-selector direction

The six generators are the named actual ordered seven-minors `T0,T1,T2,T3,
Y1,X3`.  Therefore `rank M(G)<=6` makes them vanish.  The proof uses no
converse.

This distinction is load-bearing at `p=0`: the six selectors really do have
two common points on `D(B*Delta)`, but a separate direct seven-minor of the
complete syndrome is nonzero at each.  Treating the selected ideal as the
full rank ideal would have produced a false survivor conclusion.  Both
tracked routes explicitly recompute the full-matrix witness.

## 2. B-open audit

On `D(B)`, the substitution `C=B t` and division by `B` are reversible.
Every remaining determinant denominator factors through `Delta`, and the
ideal includes `z B Delta-1`.

At `p=0`, both implementations obtain

~~~text
z^2+z/8+1/128, a-1, q-16z-2, B+8z, t+240z/17+7/17.
~~~

`T3` has zero remainder.  The quadratic is squarefree and gives exactly two
conjugate points.  At both, all six selectors vanish, while the direct minor
on rows `(0,1,2,17,25,28,32)` and columns `(0,1,2,3,4,5,6)` equals

~~~text
(-29952 +/- 28416 i)/289 != 0.
~~~

Thus both points have syndrome rank at least seven and cannot satisfy the
hypothesis.

At `p=1`, the first-five basis is

~~~text
z^2+1/64, a+8z-1, q+8z, B+1/2, t-40z/13+12/13.
~~~

The sixth-selector remainder `-2048z/13-384/13` is coprime to `64z^2+1`.
Hence the six-selector B-open locus is empty.  The large exploratory unit
lift is not needed by the tracked theorem.

## 3. B=0, C-open audit

At `B=0`, each selected minor is `C` times its recorded coefficient.  On
`D(C)` it is legitimate to divide by `C`.  Both exact routes independently
obtain unit ideals

~~~text
<Q6, six C-coefficients, z Delta-1> = <1>
~~~

for `p=0` and `p=1`.  This proves emptiness only on `V(B) intersect
D(C*Delta)`; it does not extend over `C=0`.

## 4. Gates and denominator clearing

At both parameter values `H2=2p^2-2p+1=1`, so no degree-drop fibre is hidden.
The specialized gates are

~~~text
p=0: Delta=-q^3(q-2)(q-1)(q^2+2q-2),
p=1: Delta=-q(q-1)^3(q+1)(q^2-4q+1).
~~~

Every cleared denominator factor appears in these products.  Both chart
ideals retain an inverse for `Delta`; there is no cancellation across its
zero locus.

## 5. Independent evidence boundary

The primary imports the pinned committed GLD71 and GLD88 constructors and
uses a sparse `B,C` determinant representation before specialization.  The
audit imports no project verifier, copies the exact support rows, locally
transcribes the chart, specializes each chart first, and then takes direct
exact matrix determinants.  They agree on:

* all 24 primitive equation hashes;
* both five-selector triangular bases;
* the `p=0` zero and `p=1` nonzero `T3` remainders;
* both C-open unit results; and
* both conjugate direct rank-seven witnesses.

The audit's copied inputs are separately compared to the committed GLD71
supports and GLD88 formulas by the evidence-status test.  Neither tracked
route consumes Singular output, a Commons message, or an ignored
`.research-runs` file.

## 6. Composition and retained frontier

GLD102 may be composed with GLD101 only as follows: on the `a=0` norm cover,
the retained `p=0` and `p=1` supports contain no nonzero-offset rank point.
GLD102 does not close `p^2+1`, `R4`, `R8`, or `R110`, and it does not exclude
the `B=C=0` endpoint.

The frontier delta is therefore a scoped child closure of two GLD101 factor
supports, not closure of the complete norm cover, E31 wall, physical
incidence problem, or global proof DAG.

## 7. Nonclaims required for acceptance

The owner and ledger must retain all of the following:

* the result is restricted to `p=0,1`, arbitrary `a`, the normalized chart,
  `Q6=0`, and `D(Delta)`;
* only the nonzero-offset locus is excluded;
* the selected minors are necessary, not sufficient, rank equations;
* no physical incidence or `D(Omega)` corollary is asserted;
* `Delta=0`, arbitrary `p`, the remaining GLD101 factors, full E31,
  outside-chart, Fitting, source-integrability, and gluing obligations remain
  open; and
* the global Krenn--Gu conjecture remains **UNRESOLVED**.

With those fences, the exact GLD102 theorem is accepted.
