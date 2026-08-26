# Four-root torus-star survivor response: universal module and projective escape reduction

## Status

**Exact fixed-star local incidence reduction and route correction (`GLD76`).**
Work over `Q(i)` and then extend scalars to `C`.  Retain the complete canonical
`GLD70` torus-star interface, its fully-supported/nonisotropic hypotheses, the
rank-`44` nuisance map `b: C^79 -> C^81`, the `GLD75` equal-leaf survivor germ,
and the complete legal first-row response at `q_0`.

This result does three things.

1. It gives an exact denominator-free response-module incidence over the four
   scale-fixed survivor parameters and all `35` raw-kernel parameters.
2. It decomposes the raw map and the `GLD74` mixed response quotient under the
   actual leaf-permutation symmetry, including a covariance check of the legal
   response semantics.
3. It exhibits two exact projective raw-fibre escape directions at the
   `GLD72` fibre.  Therefore the simplest properness argument for transporting
   the affine `GLD74` exclusion to a survivor-open neighbourhood is invalid.

It does **not** prove an affine response lift, exclude a survivor
neighbourhood, classify the entire projective boundary, cover other survivor
components or interfaces, integrate a source graph, or resolve Krenn--Gu.
The global conjecture remains **UNRESOLVED**.

**Successor notice.**  `GLD77` restricts the homogeneous boundary to the
entire three-dimensional leaf-sign raw block and proves that it consists of
exactly three reduced projective points.  It recovers the two witnesses below
and adds the ratio `(1,-1,-1)`.  Boundary directions with trivial or standard
components and every strict-transform branch remain open.

## 1. The scale-fixed survivor base

Use the `GLD75` equal-leaf frame gauge

```text
F=(A,G,G,G)
```

with `15` shifted frame coordinates `x_0,...,x_14`.  The exact bidirectional
`GLD75` certificate replaces the original `37` nuisance-membership equations
by ten generators with the same ideal.  Their Jacobian at the Gaussian point
has rank `10` and free coordinates

```text
x_6, x_8, x_12, x_13, x_14.                            (1)
```

The coordinate `x_8` is the tensor-scaling direction.  Add `x_8=0`.  The
resulting eleven-equation chart has Jacobian rank `11` and four local
parameters

```text
x_6, x_12, x_13, x_14.                                 (2)
```

All frame determinants, support coordinates, and nonisotropic slopes remain
on their declared `GLD70`/`GLD75` open set.  No equation below divides by a
response minor.

## 2. Exact universal response module

Fix one left-to-right pivot solve for `b`.  On the survivor ideal it gives

```text
alpha(F,t)=alpha_0(F)+K t,        K: C^35 -> ker b.     (3)
```

Here `alpha_0(F)` is polynomial in the frame entries because the selected
pivot inverse is a constant matrix over `Q`; equation (3) is interpreted in
the coordinate ring of the certified survivor chart.  The verifier checks
the selected rows directly and identifies the remaining residual with the
certified nuisance-membership ideal.

Write the complete legal response as

```text
D_q0(alpha)=[C | H_0(alpha) H_1(alpha) H_2(alpha) H_3(alpha)].   (4)
```

The fixed block `C` consists of the `Q` cofactor and the twelve eta-residual
cofactors.  It has rank `13` in the full `81`-coordinate tensor space.  A
fixed pivot-row quotient

```text
q: C^81 -> C^81 / im C = C^68                         (5)
```

therefore gives a `68 x 4` root-response matrix

```text
Hbar(F,t)=q[H_0(alpha(F,t)) ... H_3(alpha(F,t))]        (6)
```

and a `68 x 3` target matrix `Rbar(F)=qR(F)`.

### Theorem 2.1 (denominator-free module equivalence)

On the declared survivor chart, including every response-rank-drop fibre,

```text
im R(F) subset im D_q0(alpha(F,t))
```

if and only if there is a `4 x 3` matrix `X` such that

```text
Hbar(F,t) X = Rbar(F).                                 (7)
```

#### Proof

Quotienting (4) by `im C` kills exactly the first thirteen response columns
and sends the other four columns to (6).  A target column lies in the image of
(4) exactly when its quotient lies in the image of (6); apply this to the
three target columns.  Equation (7) encodes all three containments
simultaneously.  It introduces twelve lift variables and `68*3=204`
equations, compared with the original `51` lift variables, and makes no rank
assumption.  `square`

The signed root combination

```text
H_0+H_1+H_2-H_3                                         (8)
```

vanishes only after restriction to the `78` mixed words and quotient by the
mixed constant block, as in `GLD74`.  It does not vanish in the full quotient
(5).  Thus replacing (6) by three columns would silently discard diagonal
response information; all four columns in (7) are load-bearing.

The equivalent Fitting formulation is the finite rank cover

```text
rank Hbar = rank[Hbar | Rbar] = r,       0 <= r <= 4.    (9)
```

The verifier records the exact minor counts.  At `r=3`, for example, the
augmented rank bound alone has `28,503,475` four-minors.  This explains why
the twelve-variable lift (7), not a literal expansion of all Fitting minors,
is the practical denominator-free parent system.

At the Gaussian specialization the verifier replays the exact `GLD74`
`65 x 3` mixed quotient fingerprint

```text
17c10d8e04a4e29b073914919beb0a99ff77735be12cc16f095e07ef7549452e. (10)
```

## 3. Leaf-S3 block structure

Permuting the three identical leaf ports acts on raw labels, tensor words,
the nuisance image, and the complete legal `q_0` response.  The verifier
checks, for every permutation `sigma`,

```text
b P_raw(sigma) = P_tensor(sigma) b,                    (11)
H_j P_raw(sigma) = P_mix(sigma) H_j       (j=0,...,3), (12)
P_mix(sigma) im C_mix = im C_mix.                      (13)
```

Thus this is covariance of the actual interface response, not merely an
abstract symmetry of the GHZ orbit.

Using character order `(identity, transposition, three-cycle)`, the exact
decompositions are:

| Space | Character | Multiplicities `(trivial, sign, standard)` | Isotypic dimensions |
|---|---:|---:|---:|
| raw `C^79` | `(79,25,7)` | `(28,3,24)` | `(28,3,48)` |
| nuisance image | `(44,20,8)` | `(20,0,12)` | `(20,0,24)` |
| raw kernel | `(35,5,-1)` | `(8,3,12)` | `(8,3,24)` |
| mixed `C^78` | `(78,24,6)` | `(27,3,24)` | `(27,3,48)` |
| mixed constant block | `(13,7,4)` | `(7,0,3)` | `(7,0,6)` |
| `GLD74` quotient | `(65,17,2)` | `(20,3,21)` | `(20,3,42)` |

In particular, the invariant raw fibre has dimension `8`, but the full fibre
also has a three-dimensional sign block and a 24-dimensional standard block.
Symmetry therefore gives honest block compression but does not authorize
discarding non-invariant raw coefficients.

## 4. Exact projective escape at GLD72

In the `GLD74` literal-diagonal coordinates, write its mixed quotient as

```text
Z(t)=Z_const + sum_(j=0)^34 t_j K_j.                   (14)
```

The affine theorem proves `rank Z(t)>=2` for every finite `t`.  Homogenizing
the raw fibre introduces

```text
Z^h(s,t)=s Z_const + sum_(j=0)^34 t_j K_j.             (15)
```

The boundary `s=0` is not empty.  Let `e_j` denote the `t_j` coordinate
vector.  The following two nonzero vectors are exact:

```text
v_- = -e_13+e_15+e_22-e_24-e_31+e_33,                 (16)

v_+ = -i e_9-e_10+i e_11+e_14+i e_18+e_19-i e_20
      -e_23-i e_27-e_28+i e_29+e_32.                  (17)
```

They satisfy

```text
(K_0 v_-, K_1 v_-, K_2 v_-) = (z,-z,z),     z != 0,   (18)
(K_0 v_+, K_1 v_+, K_2 v_+) = (w, w,-w),    w != 0.   (19)
```

Equivalently, on the first proportional-column chart the full `130 x 35`
matrices at `(a,b)=(-1,1)` and `(1,-1)` both have exact rank `34` and the
displayed vectors span their one-dimensional kernels.  The associated raw
directions `K v_-` and `K v_+` both transform by the **sign representation**
of leaf `S_3`.

### Corollary 4.1 (properness route correction)

The direct projectivization (15) cannot turn the affine `GLD74` exclusion
into a survivor-open exclusion merely by observing that the fibre over
`GLD72` is empty: its boundary fibre already contains (16)--(19).

These points are at infinity.  They do not contradict `GLD74`, do not solve
(7) at a finite raw coefficient vector, and are not graph witnesses or
counterexamples.  Nor has this result proved that (16)--(17) exhaust the
projective boundary.

## 5. Bounded comprehensive-basis outcome

A bounded determinant pilot formed the two proportional-column matrices at
infinity.  The second chart has one constant nonzero maximal minor, and the
third chart has full column rank `35`.  On the first chart, exact selected
maximal minors had degrees `32` and `33`; direct evaluation exposed the two
rank-`34` points above.  A further selected minor had degree `29` with `309`
terms.  The attempted selected-minor standard-basis refinement did not finish
inside its bounded window and was terminated.  This timeout proves no
exhaustiveness statement.

The planned comprehensive `grobcov` run on the four-parameter survivor family
was not promoted after the exact boundary stop condition fired.  Feeding the
unresolved strict transform to a larger cover computation would conflate the
known escape branch with affine solutions.

## 6. Named residual parent obligations

The smallest next fixed-star calculation is now a blow-up/strict-transform
problem, not another pointwise raw solve:

1. blow up the homogenized incidence along the two sign directions
   (16)--(17) and test compatibility with the four survivor parameters (2);
2. determine the rest of the projective rank-one boundary, or give a finite
   exact cover containing it;
3. exclude or lift every strict-transform branch before claiming a principal
   survivor-open polynomial `delta`;
4. only then run a comprehensive Groebner cover on the remaining smallest
   block and record every leading coefficient as a named divisor.

An exact finite strict-transform lift would be a route correction requiring
independent validation.  An exclusion of these branches would reopen the
principal-open `GLD74` certificate-lifting route.  Other survivor components,
interfaces, source integration, maximum-root/fifth-root questions, and global
Krenn--Gu remain separate obligations.

## 7. Verification and hostile controls

Run:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_survivor_response_universal_module_reduction.py
python claims/arbitrary-order/verify_four_root_torus_star_survivor_response_s3_representation_reduction.py
python claims/arbitrary-order/verify_four_root_torus_star_survivor_response_projective_escape_boundary.py
python -I claims/arbitrary-order/audit_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension.py
```

The replay preserves the hostile controls:

- `GLD72` remains an exact concise GHZ survivor in the nuisance space;
- the `GLD70` epsilon generator is not used as a GHZ-membership test;
- the `GLD74` `65 x 3` quotient and three-chart affine exclusion are replayed;
- frame nonuniqueness is handled through the certified `GLD75` gauge and
  explicit scale fixing, not by assuming a unique GHZ decomposition;
- no response minor, support coordinate, slope, or determinant is divided by
  silently;
- the `S_3` audit checks the complete graph/source response maps;
- the two boundary witnesses are explicitly labelled projective, not affine;
- no fixed-star or local-germ statement is promoted to a global theorem.
