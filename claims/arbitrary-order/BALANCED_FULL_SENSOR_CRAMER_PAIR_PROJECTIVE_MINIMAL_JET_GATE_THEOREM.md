# Balanced full-sensor Cramer pair projective-minimal jet gate

## Status

**Exact projective compression of the proved full-sensor pair-pole gate.**
Fix one affine chart in every nonroot projective factor.  For a Cramer pair
component, the full cone-coordinate differential-flatness family is
equivalent to the strictly smaller family consisting of

1. one first stress in each nonpivot coordinate at every nonendpoint; and
2. one symmetric Hessian stress in each pair of nonpivot coordinates at both
   endpoints.

The omitted radial stresses follow from the degree-zero and differentiated
degree-one Euler identities.  If every local space has dimension `d`, the
number of pair identities falls from

```text
d(m-2)+d(d+1)
```

to

```text
(d-1)(m-2)+d(d-1)=(d-1)(m+d-2).                    (1)
```

For the ternary Krenn--Gu problem this is

```text
3m+6  --->  2m+2                                   (2)
```

identities per pair.  Through the replacement-minor theorem, the retained
identities may equivalently be written as `2m+2` selected-column replacement
determinants or full-sensor column-span conditions.

This theorem does **not** prove that any balanced target incidence fails a
retained identity.  Its coordinatewise sharp controls are ambient
multihomogeneous rational sections, not balanced complete-deck sensors with
the GHZ target.  The all-balanced rank-drop branch is unchanged, and the
global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Cramer pair stresses and a projective chart

Use the hypotheses and notation of the
[`pair-pole differential-flatness theorem`](BALANCED_FULL_SENSOR_CRAMER_PAIR_POLE_DIFFERENTIAL_FLATNESS_THEOREM.md)
and the
[`pair-jet replacement-minor theorem`](BALANCED_FULL_SENSOR_CRAMER_PAIR_JET_REPLACEMENT_MINOR_THEOREM.md).
Thus, on one nonzero maximal-minor chart,

```text
f_e=v_e/beta,              e={p,q},                 (3)
```

is multihomogeneous of degree one in the endpoint groups `z_p,z_q` and
degree zero in every group `z_w` with `w notin e`.  Work in the integral
polynomial coordinate ring of the affine cones and its fraction field.

For every group `u`, choose one coordinate as projective pivot and write

```text
z_u=(z_(u,0),z_(u,1),...,z_(u,d_u-1)).              (4)
```

The chart is `z_(u,0)!=0`.  The pivot is a chart choice, not a Cramer-row or
sensor-column choice.

Recall the cleared stresses

```text
S_(w,a)=beta^2 partial_(w,a) f_e,                    (5)

H^(r)_(a,b)=beta^3 partial_(r,a)partial_(r,b) f_e,   (6)
```

where `w notin e`, `r in {p,q}`, and `H^(r)` is symmetric.  Equations
(5)--(6) abbreviate the polynomial quotient-rule formulas displayed in the
differential-flatness theorem; they remain meaningful even if `f_e` has a
pole.

Define the **reduced projective family** by

```text
S_(w,a)=0       for w notin e and 1<=a<d_w;

H^(r)_(a,b)=0  for r in {p,q} and
               1<=a<=b<d_r.                        (7)
```

These are ordinary affine-cone partials in the nonpivot directions.  On the
chart `z_(u,0)=1`, they are exactly the first derivatives, respectively the
symmetric Hessian, in the affine projective coordinates.

## 2. Exact Euler syzygies among the cleared jets

### Lemma 1 (radial stress syzygies)

For every nonendpoint group `w`,

```text
sum_(a=0)^(d_w-1) z_(w,a) S_(w,a)=0.                (8)
```

For either endpoint `r` and every `0<=b<d_r`,

```text
sum_(a=0)^(d_r-1) z_(r,a) H^(r)_(a,b)=0.            (9)
```

These are polynomial identities.  They require neither characteristic zero
nor division by an integer.

### Proof

If a rational function `f` is homogeneous of degree `delta` in one group,
Euler's identity and its derivative are

```text
sum_a z_a partial_a f=delta f,

sum_a z_a partial_a partial_b f
  =(delta-1) partial_b f.                           (10)
```

For a nonendpoint group, `delta=0`.  Multiply the first identity by
`beta^2` to obtain (8).  For an endpoint, `delta=1`.  Multiply the second
identity by `beta^3` to obtain (9).  Since (5)--(6) are polynomial, both
syzygies hold in the original coordinate ring.

Equivalently, if `beta` and `v_e` have group degrees `B` and `B+delta`, then
the first identity can be checked without fractions:

```text
sum_a z_a(beta partial_a v_e-v_e partial_a beta)
 =delta beta v_e.                                   (11)
```

The cases used in (8)--(9) have coefficients `0` and `1`, so no positive-
characteristic division is concealed here.

## 3. The reduced family is the full pair-pole gate

### Theorem 2 (projective-minimal pair differential flatness)

Over characteristic zero, the following are equivalent for the Cramer pair
component (3).

1. `f_e` is one constant physical bilinear block:

   ```text
   f_e(z_p,z_q)=z_p^T W_pq z_q.                     (12)
   ```

2. `f_e` has no prime-divisor pole as a rational section of `O(1_e)`.
3. The full cone-coordinate stress family of the pair-pole differential-
   flatness theorem vanishes.
4. The reduced projective family (7) vanishes for one choice of pivot in
   every group.
5. The reduced projective family vanishes for every choice of nonzero
   projective chart.

### Proof

The predecessor theorem proves the equivalence of conditions 1--3 in
characteristic zero.  Condition 3 plainly implies condition 4.

Assume condition 4.  For an outside group `w`, every term of (8) except the
pivot term is zero, hence

```text
z_(w,0) S_(w,0)=0.                                  (13)
```

The cone coordinate ring is a domain and `z_(w,0)` is nonzero, so
`S_(w,0)=0`.  Thus every outside first stress vanishes.

Now fix an endpoint `r`.  For each nonpivot index `b>0`, equation (9) and the
reduced Hessian identities give

```text
z_(r,0) H^(r)_(0,b)=0,                              (14)
```

so every mixed radial/nonradial entry vanishes.  Taking `b=0` in (9), using
Hessian symmetry and (14), then gives

```text
z_(r,0) H^(r)_(0,0)=0.                              (15)
```

Hence the entire endpoint Hessian vanishes.  Repeating at the other endpoint
proves condition 3.

Finally, conditions 1--3 are intrinsic and imply the reduced equations in
every chart.  Therefore condition 4 implies condition 5, while condition 5
trivially implies condition 4.

The implication 4 to 3 is the new algebraic compression and is valid in any
characteristic.  Characteristic zero remains load-bearing only through the
imported implication from full differential flatness to a constant physical
block: coordinate derivations can have a larger constant field in positive
characteristic.

## 4. Exact counts and target-column form

For a pair `e={p,q}` with possibly unequal local dimensions, the reduced
family contains

```text
sum_(w notin e)(d_w-1)
 + binomial(d_p,2)+binomial(d_q,2)                  (16)
```

identities.  Here `binomial(d_r,2)` counts the symmetric Hessian on the
`d_r-1` nonpivot coordinates.  Uniform dimension `d` gives (1), and `d=3`
gives exactly `2m+2`.

Under the full-rank and target-consistency hypotheses of the pair-jet
replacement-minor theorem, every retained equation in (7) has either of the
equivalent target-facing forms

```text
Q_D lies in span_F Gamma_hat(e)
iff det(A[e <- q_D])=0,                              (17)

Q_DE lies in span_F Gamma_hat(e)
iff det(A[e <- q_DE])=0.                            (18)
```

Before imposing target consistency, the selected-row replacement minors
already obey the exact polynomial syzygies

```text
sum_a z_(w,a) det(A[e <- q_(w,a)])=0,               (19)

sum_a z_(r,a) det(A[e <- q_((r,a),(r,b))])=0
  for every endpoint r and every b.                 (20)
```

Indeed, the replacement-minor theorem identifies the determinants in
(19)--(20) with the stress coordinates in (8)--(9).  Target consistency is
not needed for these selected-system syzygies; it is needed only to interpret
the same determinants as full-row span conditions.

Use (17) only for the `d_w-1` nonpivot directions at each outside group, and
(18) only for the symmetric pairs of nonpivot directions at the endpoints.
The omitted target-column tests follow because their replacement determinants
are the omitted stresses in (8)--(9).  No target residual is silently
dropped: the span interpretation still requires the separately imposed
identity `Gamma v=beta J` and function-field column rank `k`.

Consequently the exact same-graph globalization gate can be written as

```text
target residuals;
empty normalization;
reduced projective pair jets for every pair;
Euler--hafnian recurrences for higher even subsets. (21)
```

This gate is necessary and sufficient because Theorem 2 makes its reduced
pair layer equivalent to the already proved prime-divisor layer.  The mixed
endpoint derivatives used to reconstruct all entries of `W_pq` are outputs,
not additional vanishing conditions, and their number is not included in
(16).

## 5. Chart covariance and what “minimal” means

The displayed subset depends on the chosen projective pivots, but its
vanishing does not.  On any chart, Theorem 2 identifies it with the intrinsic
full-stress family.  On chart overlaps this also agrees with the common
Cramer rescaling laws

```text
S'=g^2 S,                 H'=g^3 H.                 (22)
```

Thus one fixed projective chart is sufficient for a symbolic proof.  No
union of charts and no point sampling is needed, because the equations are
identities in the function field or polynomial coordinate ring.

“Projective-minimal” here has a precise limited meaning: for a fixed pivot,
the retained coordinate list has the dimension of the affine projective
first jet outside the pair and the symmetric affine projective Hessian at
the endpoints.  Section 6 shows that no single retained coordinate follows
from the prescribed multidegrees and the other retained coordinates alone.
This is not a lower bound for arbitrary nonlinear encodings and not a
sharpness theorem inside the balanced target-incidence image.

## 6. Ambient coordinatewise sharpness

Take ternary endpoint groups `x,y`, with pivots `x_0,y_0`, and use pivot
`r_0` in one outside group `r`.

### One independently failing outside coordinate

For either nonpivot index `a in {1,2}`, set

```text
beta=r_0,
v=r_a x_0 y_0,
f=(r_a/r_0)x_0y_0.                                  (23)
```

This has multidegrees `(1,1,0)`.  Both endpoint Hessians vanish and the other
retained outside derivative vanishes, while

```text
S_(r,a)=r_0 x_0 y_0 !=0.                            (24)
```

### One independently failing endpoint Hessian coordinate

For `1<=a<=b<=2`, put

```text
beta=x_0,

v=x_a^2 y_0              if a=b,
v=x_a x_b y_0            if a<b.                    (25)
```

Again `f=v/beta` has the required endpoint bidegree.  Every outside stress,
the `y`-endpoint Hessian, and every retained `x`-Hessian entry other than
`(a,b)` vanish.  The exceptional cleared entry is

```text
H^(x)_(a,a)=2x_0^2 y_0,
H^(x)_(a,b)= x_0^2 y_0       for a<b.               (26)
```

Swapping `x,y` gives the same controls at the other endpoint.  Each example
is an exact abstract `2 x 2` Cramer system by taking

```text
A=diag(beta,1),             j=(v,0)^T.               (27)
```

There is also a stronger selected-system realization that respects all four
even-deck column multidegrees at `m=3` and uses only zero or pure GHZ entries
in the selected target rows.  Let the groups be `x,y,r`, let `e={x,y}`, and
write the four deck labels as `e,{x,r},{y,r},empty`.  For the outside control
with exceptional `a in {1,2}`, take columns in that order and

```text
A_out = [ r_0  y_0   0       0         ]
        [ 0    y_1   0       0         ]
        [ 0    0     x_0     0         ]
        [ 0    0     0       x_0y_0r_0 ],

j_out=(x_a y_a r_a,0,0,0)^T.                        (28)
```

The Cramer solution has pair coordinate

```text
f_e=(r_a/r_0)x_a y_a,                               (29)
```

and every other coordinate zero.  The four columns have respective degrees
`r`, `y`, `x`, and `xyr`, exactly the complements of their deck labels, while
the only nonzero target row is one pure GHZ monomial.

For the `x`-endpoint control indexed by `1<=a<=b<=2`, order the columns as
`e,empty,{x,r},{y,r}` and take

```text
A_x = [ r_a  -x_b y_a r_a   0    0   ]
      [ 0      x_0 y_a r_a   0    0   ]
      [ 0      0              y_0  0   ]
      [ 0      0              0    x_0 ],

j_x=(0,x_a y_a r_a,0,0)^T.                          (30)
```

Its first two Cramer coordinates are

```text
f_e=(x_a x_b/x_0)y_a,       f_empty=x_a/x_0.        (31)
```

The analogous `y`-endpoint control is

```text
A_y = [ r_a  -x_a y_b r_a   0    0   ]
      [ 0      x_a y_0 r_a   0    0   ]
      [ 0      0              y_0  0   ]
      [ 0      0              0    x_0 ],

j_y=(0,x_a y_a r_a,0,0)^T,                          (32)

f_e=x_a(y_a y_b/y_0),       f_empty=y_a/y_0.        (33)
```

Again the columns have the exact deck-complement multidegrees `r,xyr,y,x`,
and the selected target is zero except for one pure GHZ monomial.  These
systems show that column multidegrees, the complete four-column count, and
the selected-row GHZ zero/pure pattern still do not make any retained affine
jet redundant.

The controls prove coordinatewise irredundancy only for the ambient
multihomogeneous rational-section lemma and the displayed selected Cramer
architecture on the fixed chart.  Neither (27) nor (28)--(33) is shown to
arise from the matching-sum formula for the balanced complete-deck sensor;
the unselected target rows and full target consistency are not supplied, and
the systems deliberately do not impose empty normalization.  They are
therefore not balanced target incidences, graph witnesses, or Krenn--Gu
counterexamples.

## 7. Proof-topology consequence and residual frontier

The open full-sensor route now needs only the projective tangent directions:

```text
one target-consistent full sensor;
for every ternary pair e:
  2(m-2) outside replacement minors;
  3+3 endpoint replacement minors;
higher Euler--hafnian recurrences.                  (34)
```

The advance removes exactly `m+4` redundant radial identities per pair.  It
does not force any retained determinant to be nonzero and does not combine
the pair layer with normalization or the higher recurrences.  The next `S2`
obligation remains target-specific: prove that every balanced target-
consistent full sensor violates normalization, one of the `2m+2` retained
pair span conditions, or a higher Euler--hafnian identity.

No such universal violation is proved here.  The all-balanced rank-drop
branch and every unrelated local/global branch retain their previous status.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_full_sensor_cramer_pair_projective_minimal_jet_gate.py
python claims/arbitrary-order/audit_balanced_full_sensor_cramer_pair_projective_minimal_jet_gate.py
python -m py_compile claims/arbitrary-order/verify_balanced_full_sensor_cramer_pair_projective_minimal_jet_gate.py claims/arbitrary-order/audit_balanced_full_sensor_cramer_pair_projective_minimal_jet_gate.py
uv run --with ruff ruff check claims/arbitrary-order/verify_balanced_full_sensor_cramer_pair_projective_minimal_jet_gate.py claims/arbitrary-order/audit_balanced_full_sensor_cramer_pair_projective_minimal_jet_gate.py
```

The primary verifier uses SymPy to check the universal quotient-cleared Euler
syzygies on nontrivial multihomogeneous Cramer data, reconstruct every omitted
ternary stress from the retained family, check the `2m+2` count and chart
rescaling, and enumerate every coordinatewise sharp control, including the
structured four-column Cramer embeddings.  The independent audit imports
neither SymPy nor repository code; it uses a separately written sparse
polynomial ring over `Q`, direct differentiation, and different exact
homogeneous data and rebuilds the structured systems.  Both scripts replay
displayed identities and conventions.
The arbitrary-dimension theorem is the Euler/domain argument above.
