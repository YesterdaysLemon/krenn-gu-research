# Three-mode residual annihilation and the full-quotient rank-sum bound

## Status

**Exact characteristic-zero arbitrary-graph obstruction.**  A degree-five
response on seven core modes contains exactly one core--core edge.  After
quotienting any three core modes by their terminal-incidence spans, every
physical summand vanishes: the edge can protect at most two of the three
quotiented modes, while the remaining mode contributes an incidence
covector.

Applying this observation to the three prescribed faces

```text
F_01=1234a,       F_02=1235b,       F_12=1345b
```

produces an invertible three-by-three system on every triple of core modes.
Consequently, in the common full-terminal quotient, each of the three pure
colour directions can survive at **at most two** of the seven modes.  The
sum of the seven quotient ranks on the prescribed colour spaces is at most
six, and at least one core mode has its entire three-colour space contained
in the full terminal-incidence span.

This also proves that the earlier rational rank-sum-ten incidence lift in
`P7_221_FACE_SPECIFIC_QUOTIENT_MAYER_VIETORIS_AND_SHARP_LIFT.md` cannot
extend to the actual five-terminal equations, regardless of how its core
edges are chosen.  The lift remains sharp only for the pairwise quotient-line
constraints that it was constructed to test.

No graph family, support, word, alignment, face system, or parameter space is
enumerated.

## 1. Five-row residual permanents

Work over a characteristic-zero field containing `rho`, where `rho^2=21`.
Let the seven core modes be `V_i`, let

```text
P={1,2,3,4,5,a,b},
A_ij in V_i^* tensor V_j^*,
R_i,p in V_i^*.
```

For a five-terminal face `F`, put

```text
U_i(F)=span{R_i,p:p in F},       q_i^F:V_i^* -> V_i^*/U_i(F).
```

After terminal Wick deconvolution, the degree-five response is

```text
T_F=sum_(i<j) A_ij tensor Per(R_(Z minus {i,j}),F).    (1)
```

The permanent in the `{i,j}` summand is the five-row tensor-valued
permanent on the other core modes.

### Lemma 1 (three-mode residual annihilation)

For every three-element core set `I`,

```text
(tensor_(i in I) q_i^F tensor id_(Z minus I)) T_F=0.   (2)
```

Proof.  Fix one summand of (1), with core edge `e={i,j}`.  Since `|e|=2`
and `|I|=3`, choose `k in I minus e`.  In every monomial of the residual
permanent, mode `k` contributes one of the covectors `R_k,p`, `p in F`.
That covector lies in `U_k(F)` and is killed by `q_k^F`.  Thus every monomial
of every edge summand vanishes.

Equivalently, first isolating an edge by the two-port quotient gives

```text
bar(A)_ij tensor P_ij^F.                              (3)
```

For every third mode `k notin {i,j}`, the actual residual factor obeys

```text
(q_k^F tensor id)P_ij^F=0.                            (4)
```

Equation (4) is the residual-permanent compatibility absent from the
projective edge-line comparison.

## 2. Descent to one common quotient

Use the full incidence spans

```text
U_i=U_i(P),             Q_i=V_i^*/U_i,
q_i:V_i^* -> Q_i.                                      (5)
```

Because `F` is contained in `P`, each `q_i` factors through `q_i^F`.
Therefore (2) remains valid with the same common maps `q_i` for all three
faces.

Let `epsilon_i^c`, `c=0,1,2`, be the prescribed pure colour covectors and
write

```text
D_c=tensor_(i in Z) epsilon_i^c,
x_i^c=q_i(epsilon_i^c).                               (6)
```

Exact terminal Wick inversion gives

```text
T_F01 = alpha D_0-6D_1,
T_F02 = rho D_0+beta D_2,
T_F12 = rho D_1+beta D_2,                             (7)

alpha=1+43rho/21,            beta=2(1+rho)/7.
```

All three equations are prescribed physical responses.

## 3. The invertible triple system

Fix any three core modes `I`.  Apply their common quotient maps to (7).
By Lemma 1, the three left sides vanish.  Put

```text
Y_c^I=(tensor_(i in I)x_i^c)
      tensor (tensor_(k notin I)epsilon_k^c).          (8)
```

Then

```text
[ alpha  -6    0 ] [Y_0^I]   [0]
[ rho     0  beta] [Y_1^I] = [0].                    (9)
[  0     rho beta] [Y_2^I]   [0]
```

The determinant is

```text
rho beta(6-alpha)=(124-76rho)/7,                      (10)
```

whose quadratic norm is

```text
N((124-76rho)/7)=-105920/49 !=0.                      (11)
```

Thus (9) is invertible over every characteristic-zero extension of
`Q(rho)`, and

```text
Y_0^I=Y_1^I=Y_2^I=0                                  (12)
```

for every triple `I`.

The unquotiented factors in (8) are nonzero.  A tensor product over a field
is nonzero exactly when all its factors are nonzero.  Hence (12) is
equivalent to

```text
product_(i in I) x_i^c=0
for every colour c and every three-element I.          (13)
```

### Theorem 2 (two-mode support per colour)

Define

```text
S_c={i:x_i^c!=0}.                                     (14)
```

Every physical realization of the three faces in (7) satisfies

```text
|S_c|<=2,                         c=0,1,2.             (15)
```

Indeed, three elements of `S_c` would form a triple contradicting (13).
This conclusion is field-independent after adjoining `rho`; it does not use
a missing cube root or an order property.

### Corollary 3 (rank-sum six and a full-span mode)

Let

```text
E_i=span{epsilon_i^0,epsilon_i^1,epsilon_i^2}.
```

The images of the three displayed basis covectors span `q_i(E_i)`, so

```text
sum_i rank(q_i restricted to E_i)
 <=sum_i |{c:i in S_c}|
 =sum_c |S_c|
 <=6.                                                  (16)
```

There are seven modes.  Therefore at least one mode `i` has

```text
q_i(E_i)=0,                    E_i subset U_i(P).      (17)
```

This is a genuine coordinate-boundary consequence of the degree-five
ledger, not a genericity condition.

## 4. Sharpness at the common-quotient layer

The constant six in (16) is attained by a legal incidence-span diagram.
Take `V_i^*=E_i` and use only terminal columns `1,3,5`:

```text
modes 0,1: R_i,1=epsilon_i^1,  R_i,3=epsilon_i^2,
modes 2,3: R_i,1=epsilon_i^0,  R_i,3=epsilon_i^2,
modes 4,5: R_i,1=epsilon_i^0,  R_i,3=epsilon_i^1,
mode 6:    R_6,1=epsilon_6^0,  R_6,3=epsilon_6^1,
           R_6,5=epsilon_6^2,                         (18)
```

with every other incidence entry zero.  Its full-quotient colour supports
are

```text
S_0={0,1},                 S_1={2,3},
S_2={4,5},                 rank q_6=0.                (19)
```

Thus the rank sum is six.  Every three-fold pure quotient tensor vanishes,
and for every pair of modes at most one colour has a nonzero pair tensor.
Consequently this one incidence system satisfies both the common-quotient
triple equations proved here and all earlier common-quotient rank-one pair
conditions.

This is an exact sharp **quotient diagram**, not a full response realization.
For example, taking every core edge to be zero makes all projected physical
faces zero, but does not reproduce the nonzero unprojected tensors in (7).
A stronger obstruction must use information discarded by the full quotient,
or combine the forced full-span mode with another degree.

## 5. The earlier sharp incidence lift does not extend

The rational incidence system in the earlier Mayer--Vietoris note has
full-terminal quotient kernels

```text
mode 0:      <epsilon^2>,
mode 1:      <epsilon^1>,
mode 2:      <epsilon^0>,
modes 3--6: <epsilon^1,epsilon^2>.                    (20)
```

Its colour supports are therefore

```text
S_0={0,1,3,4,5,6},       S_1={0,2},       S_2={1,2}, (21)
```

and the quotient-rank sum is ten.  Both values violate (15)--(16).

One explicit failure already occurs on `F_01` and the triple `{0,1,3}`.
The colour-zero projection is nonzero at all three modes, while the
colour-one projection is killed at modes 1 and 3.  The projected formal
response is therefore the nonzero tensor

```text
alpha x_0^0 tensor x_1^0 tensor x_3^0
      tensor (the four unprojected colour-zero factors),                (22)
```

whereas Lemma 1 forces every physical response to project to zero.

Consequently no choice of the tensors `A_ij`, and no change of incidence
coordinates that preserves the full spans (18), can turn that quotient
construction into the three actual responses (7).  This closes the exact
question left open by its common-edge projective lift.

## 6. Exact boundary

Proved:

- universal three-mode annihilation of every five-row residual permanent;
- simultaneous descent of the three prescribed faces to the full quotient;
- invertibility of the exact three-colour coefficient system;
- at most two surviving full-quotient modes per colour;
- total colour-space quotient rank at most six;
- sharpness of six for a legal common-quotient incidence diagram;
- existence of at least one mode whose full incidence span contains all
  three prescribed colour axes;
- nonextendability of the earlier rational rank-sum-ten incidence lift to
  the actual face equations.

Not proved:

- a contradiction from the forced full-span mode (17);
- that `E_i subset U_i(P)` is incompatible with degrees one, three, or seven;
- a classification or realization of the rank-sum-at-most-six boundary;
- a `P_7 -> Delta_3` restriction;
- the global Krenn--Gu conjecture.

The exact status is

```text
three-mode five-row residual annihilation:      EXACT;
full-quotient support per colour:                AT MOST TWO;
sum of seven colour-space quotient ranks:        AT MOST SIX, SHARP ABSTRACTLY;
earlier rank-sum-ten common-edge lift:            EXCLUDED AS A FULL LIFT;
rank-sum-at-most-six physical realization:        UNKNOWN;
P7 and global Krenn--Gu:                          UNRESOLVED.             (23)
```

## Replay

```powershell
uv run --with sympy python verify_p7_221_three_mode_residual_annihilation_and_full_quotient_rank_sum_bound.py
python audit_p7_221_three_mode_residual_annihilation_and_full_quotient_rank_sum_bound.py
python -m py_compile verify_p7_221_three_mode_residual_annihilation_and_full_quotient_rank_sum_bound.py audit_p7_221_three_mode_residual_annihilation_and_full_quotient_rank_sum_bound.py
uv run --with ruff ruff check verify_p7_221_three_mode_residual_annihilation_and_full_quotient_rank_sum_bound.py audit_p7_221_three_mode_residual_annihilation_and_full_quotient_rank_sum_bound.py
```

The primary replay reconstructs the three exact Wick coefficients, checks
the determinant and its norm, and exhibits the forbidden projection in the
earlier sharp lift.  The no-import audit repeats the arithmetic and support
calculation with hand-written rational-pair algebra.  Neither replay searches
graphs, supports, words, alignments, faces, or parameters.
