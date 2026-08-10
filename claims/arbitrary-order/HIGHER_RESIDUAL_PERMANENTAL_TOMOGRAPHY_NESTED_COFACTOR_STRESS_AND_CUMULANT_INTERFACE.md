# Higher-residual permanental tomography, nested cofactor stress, and the cumulant interface

## Status

**Exact arbitrary-even-order characteristic-zero theorem and sharp
observability boundary.**  Let `Q` be an even residual set of order `q`, and
choose a square transversal of `q` scalar boundary ports.  For each even
`k`, the degree-`k` relative response is the `k`th permanental compound of
the residual--port incidence matrix applied to the `k`-deletion principal
hafnian cofactors.

All these compounds are simultaneously invertible on a nonempty Zariski-open
incidence chart: at the identity incidence, every compound is the identity.
Consequently the complete relative response on that chart reconstructs every
principal cofactor

```text
c_T=haf(A[Q minus T]),                 |T| even.        (1)
```

The reconstructed arrays come from one residual matrix if and only if they
satisfy the nested partner-expansion equations

```text
c_T=sum_(s in Q minus (T union {p}))
        c_(Q minus {p,s}) c_(T union {p,s}),           (2)
```

for every even `T` and every `p notin T`, together with `c_Q=1`.  This is a
necessary-and-sufficient arbitrary-order integrability test.  Its depth-zero
row is precisely the Hadamard stress

```text
(A Hadamard C(A))1=haf(A)1,                            (3)
```

and its deeper rows are the missing nested stresses.  Clearing the compound
determinants turns (2) into explicit polynomial response equations, so any
failure is an exact obstruction.

If compatible principal residual-depth responses are also exposed, the same
reconstructed `A` and incidence matrix predict them all.  Equivalently their
higher residual cumulants vanish; a division-free set-partition formula is
given below.

This theorem does not prove that a top `P_5`, `P_6`, or `P_7` equation
legally exposes the square transversal and all required port degrees.  The
lower mixed-root theorem supplies cofactor **spans**, but usually does not
label individual deletion classes.  Without that label synchronization the
test cannot be applied.  The full-rank torus-zero family with identity
incidence satisfies the complete tower and proves the boundary sharp.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

No residual support, graph family, colour word, matching family, minor, or
parameter space is enumerated.

## 1. Relative response and its permanental compounds

Work over a characteristic-zero field `K`.  Let

```text
Q={1,...,q},                  U={1,...,q},              (4)
```

where `q` is even.  After all previously fixed contractions, write

```text
A_pv       for residual--residual edges,
R_pu       for residual--port incidences.              (5)
```

Divide the residual-present response by the port-only moment family.  Its
relative polynomial is

```text
Phi(x)=[y_Q] exp(
  sum_(p<v) A_pv y_p y_v+sum_(p,u)R_pu y_p x_u).       (6)
```

For every even `k` and every `k`-subset `T of Q`, put

```text
c_T=haf(A[Q minus T]).                                 (7)
```

For `k`-subsets `T of Q` and `S of U`, define the square permanental
compound

```text
P_k(R)_(T,S)=per R[T,S].                               (8)
```

Coefficient extraction gives

```text
phi_S=[x_S]Phi
     =sum_(T subset Q, |T|=k)c_T per R[T,S],

phi^(k)=c^(k) P_k(R).                                  (9)
```

Only even port degrees occur, and every degree above `q` vanishes.  At the
three characteristic depths,

```text
c_empty=haf(A)=h,
c_{p,s}=haf(A[Q minus {p,s}])=C(A)_ps,
c_(Q minus {p,s})=A_ps,
c_Q=1.                                                 (10)
```

Thus degree two is the common cofactor--Gram layer, degree `q-2` carries the
residual edge matrix itself, and degree `q` is the top incidence permanent.

## 2. One common compound-open chart

### Theorem 1 (simultaneous permanental observability)

There is a nonempty Zariski-open set of square incidence matrices `R` on
which

```text
det P_k(R)!=0                       for every even 0<=k<=q. (11)
```

### Proof

At `R=I_q`,

```text
per I_q[T,S]=1 if T=S,
                 0 otherwise.                          (12)
```

Hence every `P_k(I_q)` is an identity matrix.  The product of the finitely
many determinant polynomials in (11) takes value one at `I_q`, so its
nonvanishing locus is a nonempty Zariski-open set.

For `k=q-2`, relabeling the columns by the complementary residual pairs
turns (12) into the complement-index permutation used by the seven-core
fifth-compound observability theorem.  The present statement uses the same
mechanism simultaneously at every even depth.

### Corollary 2 (cofactor tomography)

On the open chart (11), every principal cofactor array is uniquely recovered:

```text
c^(k)=phi^(k) P_k(R)^(-1).                             (13)
```

In particular the residual edge matrix and the quadratic cofactor matrix are
reconstructed independently from degrees `q-2` and `2`.  Their compatibility
is therefore testable rather than hidden behind an arbitrary Gram
factorization.

The first two even orders make the distinction concrete.  At `q=4`, degree
two is also degree `q-2`: after complementary-pair relabeling it reconstructs
`A`, and the scalar `h=haf(A)` is then predicted rather than independently
free.  At `q=6`, degree four reconstructs `A` while degree two independently
reconstructs the four-vertex deletion cofactors `C(A)`; equations (14)--(17)
are precisely the tests that the latter really are the principal hafnians of
the former, with Hadamard stress as their depth-zero contraction.

## 3. Nested principal-hafnian integrability

For an even deletion set `T` and `p notin T`, expand the hafnian of
`A[Q minus T]` along vertex `p`:

```text
c_T=sum_(s in Q minus (T union {p})) A_ps c_(T union {p,s}). (14)
```

Using the observable edge identity in (10), this is exactly (2).

### Theorem 3 (complete nested-cofactor criterion)

Assume (11).  A relative response polynomial `Phi` is representable in the
form (6), for the fixed incidence matrix `R`, if and only if:

1. its odd port layers and all layers above `q` vanish;
2. the recovered top cofactor satisfies `c_Q=1`; and
3. the recovered even arrays obey (2) for every `T` with `Q minus T`
   nonempty and every `p notin T`.

### Proof

Necessity is (9), `c_Q=haf(empty)=1`, and the partner expansion (14).

Conversely, define a hollow symmetric matrix by

```text
A_ps=c_(Q minus {p,s}).                                (15)
```

Descend on `|Q minus T|`.  The empty hafnian gives the base `c_Q=1`, and
when two vertices remain, (15) gives their hafnian.  If all deeper cofactors
are already the corresponding principal hafnians, equation (2) is exactly
the expansion of `haf(A[Q minus T])` along `p`; hence `c_T` is that hafnian.
Induction proves (7) at every depth.  Substitution into (9) then reconstructs
the given `Phi` coefficient by coefficient, proving sufficiency.

Thus the open-chart test is complete, not merely necessary.  It classifies
the previously unresolved `q>=4` relative polynomials whenever one legally
known square incidence chart has all even compounds invertible.

## 4. Division-free obstruction equations

Put

```text
delta_k=det P_k(R),
w^(k)=phi^(k) adj(P_k(R)),                              (16)
```

so `w_T^(k)=delta_k c_T`.  Equation (2), with `|T|=k`, becomes the polynomial
identity

```text
delta_(q-2) delta_(k+2) w_T^(k)
 -delta_k sum_(s notin T union {p})
    w_(Q minus {p,s})^(q-2) w_(T union {p,s})^(k+2)=0. (17)
```

All quantities in (17) are polynomial in the incidence and response
coefficients.  No inverse remains.  Failure of one named equation (17) on a
compound-open chart is an exact characteristic-zero obstruction to a common
residual graph.

For `T=empty`, identify

```text
A_ps=c_(Q minus {p,s}),             C_ps=c_{p,s}.       (18)
```

Then (2) reads

```text
sum_(s!=p) A_ps C_ps=h,                                (19)
```

which for every row is the Hadamard stress (3).  For nonempty `T`, (17)
gives its principal-deletion descendants.  A candidate can therefore pass
the global stress and still fail a deeper one.

## 5. Higher residual cumulants on the same reconstructed graph

Suppose the principal residual-depth responses of the same scalar chart are
also exposed.  Write

```text
M=Z_empty,
Psi_T=M^(-1)Z_T.                                       (20)
```

The complete response theorem gives

```text
sum_T Psi_T y_T
 =exp(sum_(p<s)A_ps y_p y_s+sum_p L_p y_p),            (21)
```

where `L_p=sum_u R_pu x_u`.  Hence every residual cumulant of order at least
three vanishes.  For `n=|T|>=3`, the division-free cumulant is

```text
K_T=sum_(pi a set partition of T)
 (-1)^(|pi|-1)(|pi|-1)!
 M^(n-|pi|) product_(B in pi) Z_B=0.                   (22)
```

At three residual vertices this is

```text
M^2 Z_pqr
 -M(Z_pq Z_r+Z_pr Z_q+Z_qr Z_p)
 +2 Z_p Z_q Z_r=0.                                    (23)
```

Tomography and cumulant flatness test different presentations of one graph.
Equations (13)--(17) recover and integrate the principal hafnian cofactors
from the full-residual response across port degrees.  Equations (21)--(23)
then require every separately observed residual-deletion response to use the
same reconstructed `A,R`.  Passing only the common-Gram quadratic layer is
strictly weaker.

## 6. Interface with legally observable root jets

The lower mixed-root theorem writes a root derivative as

```text
T_I^graph=sum_D G_D tensor C_(I union D)               (24)
```

and forces the span of the complementary cofactor tensors to contain the
required one-, two-, or three-dimensional GHZ frame.  This is enough to
force rank and certain target values, but it normally does not select which
deletion label supplies which frame vector.

The tomography theorem can test a root jet only under the following legal
identification:

1. a fixed scalar contraction identifies the jet complement with the same
   residual matrix `A` and incidence chart `R` used in (6);
2. an individual deletion label `T` is exposed, rather than only an
   unspecified span of several `C_(I union D)`; and
3. enough port degrees are present to invert the corresponding `P_k(R)`.

When these conditions hold, the individually observed jet cofactor must
equal the recovered `c_T`, and adjacent labels must satisfy (17).  A mismatch
is an exact lower-jet obstruction.

Without conditions 1--3, the root-frame theorem does not imply a stress or
cumulant violation.  An arbitrary invertible change among the cofactor-frame
generators preserves its span while changing the labeled values needed in
(2).  This is the exact observability gap, not an invitation to identify
unrelated deletion depths.

## 7. Sharp controls and surviving blocker surplus

The criterion has two sharp controls.

1. At `R=I_q`, every compound is the identity.  For every hollow symmetric
   `A`, equations (7) and (9) give a represented response, and Theorem 3
   accepts it.  Therefore no additional isolated fixed-incidence equation
   exists after all nested stresses hold.
2. Take the complete-support torus-zero family

   ```text
   A_12=-(q-2),             A_ij=1 otherwise,
   ```

   for even `q>=4`, together with `R=I_q`.  It has `haf(A)=0` and full-rank
   `C(A)`, yet it satisfies every nested stress and every higher cumulant
   because it is one honest graph.  Thus Hadamard stress plus all deletion
   compatibility does not force a rank drop or contradict the multichannel
   branch by itself.

For arbitrary blocker surplus, the theorem applies after any legal
contraction that leaves a common scalar residual graph and a square
transversal port chart.  It does not synchronize unfactored surplus port
forms automatically.  At `q>=4`, multiple common-Gram channels remain legal;
the new obstruction is their common higher-compound integrability, not a
one-channel reduction.

## 8. Scope wall

Proved:

- simultaneous generic invertibility of all even permanental compounds on a
  square residual--port chart;
- unique reconstruction of every nested principal hafnian cofactor there;
- necessary and sufficient nested partner-expansion integrability;
- division-free polynomial obstruction equations (17);
- Hadamard stress as the depth-zero member of the hierarchy;
- the division-free arbitrary-order higher-cumulant equations (22);
- the exact labeled interface required to combine lower root jets with the
  reconstructed cofactor tower;
- full-rank torus-zero sharpness for the entire intrinsic hierarchy.

Not proved:

- that every hypothetical Krenn--Gu witness exposes a qualifying square
  transversal chart;
- invertibility of the required compounds on coordinate-boundary charts;
- individual deletion-label selection from a cofactor span alone;
- a GHZ-derived labeled value violating (17) or (22);
- synchronization of arbitrary unfactored higher-surplus port forms;
- unrestricted `P_5`, `P_6`, or `P_7` nonrestriction;
- the global Krenn--Gu conjecture.

```text
q>=4 compound-open relative response classification: COMPLETE;
nested cofactor/Hadamard integrability:                EXACT;
higher residual cumulant obstruction:                  EXACT IF DEPTHS EXPOSED;
root-jet span -> labeled deletion values:               NOT AUTOMATIC;
torus-zero full-rank multichannel family:               PASSES ALL INTRINSIC TESTS;
forced compound-open chart in every witness:            UNKNOWN;
global Krenn--Gu:                                       UNRESOLVED.         (25)
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_higher_residual_permanental_tomography_nested_cofactor_stress_and_cumulant_interface.py
python claims/arbitrary-order/audit_higher_residual_permanental_tomography_nested_cofactor_stress_and_cumulant_interface.py
python -m py_compile claims/arbitrary-order/verify_higher_residual_permanental_tomography_nested_cofactor_stress_and_cumulant_interface.py claims/arbitrary-order/audit_higher_residual_permanental_tomography_nested_cofactor_stress_and_cumulant_interface.py
uv run --with ruff ruff check claims/arbitrary-order/verify_higher_residual_permanental_tomography_nested_cofactor_stress_and_cumulant_interface.py claims/arbitrary-order/audit_higher_residual_permanental_tomography_nested_cofactor_stress_and_cumulant_interface.py
```

The primary replay checks every even identity compound at `q=6`, reconstructs
an exact generic cofactor tower, verifies the complete nested recurrence and
Hadamard stress, checks the division-free third cumulant, and audits the
torus-zero full-rank control.  The independent no-project-import audit uses a
separate integer hafnian recurrence and rational rank elimination.  These are
fixed small audits; the complement-index, partner-expansion, induction, and
set-partition proofs establish arbitrary order without enumerating graph
supports, colour words, or parameter families.
