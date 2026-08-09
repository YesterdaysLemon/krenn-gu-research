# Pure-chart fifth-compound fibre dichotomy and a singular escape

## Status

**Exact characteristic-zero conditional theorem and explicit fibre escape.**
Let the three scalar pure charts vary over their complete deconvolved
degree-one, degree-three, and degree-five ledger fibres.  For each mixed core
word, fifth-compound observability gives a finite dichotomy:

1. if the mixed fifth compound is invertible, every compatible core-edge
   vector lies on one inverse-column line and the prescribed same-colour
   entries obey adjugate proportionality circuits;
2. if the compound is singular, either the exceptional face is killed by a
   left-kernel functional or the solution set is an affine line plus the
   compound kernel.

The invertible branch is not uniform over the pure-chart fibre.  The verified
colour-2 scalar chart has two identical incidence rows.  A legal relabelling
can place those rows at two colour-2 positions of the mixed word
`2220000`, forcing at least five independent kernel directions in its fifth
compound.  For this singular alignment there is an exact assignment of the
cross-colour core edges for which all 21 mixed degree-five faces vanish.

Thus the pure scalar ledgers do not force the earlier fixed-alignment
`2220000` violation throughout their entire fibre.  This is only a
degree-five statement: degrees one and three, other mixed words, and one
physical tensor lift remain unresolved.

No mixed-word enumeration or solution of the full scalar chart fibre is used.

## 1. Fibre setup

For each colour `c`, let

```text
(A^(c),R^(c))                                          (1)
```

be a seven-core scalar graph realizing the complete prescribed
no-terminal-edge pure ledger through degrees one, three, and five.  Relabel
the seven internal core vertices independently in each pure chart before
identifying them in a putative tensor graph.

Fix a mixed core word `sigma in {0,1,2}^7`.  Its frozen incidence matrix is
obtained rowwise:

```text
(R_sigma)_(i,*)=(R^(sigma_i))_(i,*).                  (2)
```

The mixed core-edge vector `a_sigma` has 21 entries.  Entries whose endpoints
have the same colour are already prescribed by the appropriate `A^(c)`;
cross-colour entries remain completion variables.

Let

```text
C_sigma=C_5^per(R_sigma),                             (3)
```

with rows indexed by five-terminal faces and columns by deleted core pairs.
The one-edge Laplace formula is

```text
Phi_sigma^(5)=C_sigma a_sigma.                        (4)
```

All twenty prescribed mixed degree-five ledger faces vanish.  Only

```text
S_*=P minus Q,                    Q={a,b},             (5)
```

is unprescribed.  Hence every completion must solve

```text
C_sigma a_sigma=tau e_(S_*)                          (6)
```

for some scalar `tau`.

## 2. The exact finite dichotomy

### Theorem 1 (fifth-compound fibre dichotomy)

Let `C` be any `21 x 21` fifth compound and let `e_*` denote the exceptional
face vector.

#### Nonsingular branch

If `det C!=0`, put

```text
v=C^(-1)e_*.                                          (7)
```

Every solution of (6) is

```text
a=tau v.                                             (8)
```

For fixed same-colour coordinates `a_e=alpha_e`, define

```text
w=adj(C)e_*.
```

The necessary and sufficient compatibility conditions on those fixed
coordinates are

```text
alpha_e w_f-alpha_f w_e=0                 for e,f fixed,
w_e=0  =>  alpha_e=0.                                  (9)
```

#### Singular branch

Assume `det C=0`.  Exactly one of the following alternatives holds.

1. **Exceptional face outside the image.**  Some `y in ker C^T` has
   `y_(S_*)!=0`.  Pairing (6) with `y` forces

   ```text
   tau=0,                     a in ker C.              (10)
   ```

2. **Exceptional face inside the image.**  Every `y in ker C^T` has
   `y_(S_*)=0`, equivalently `e_* in im C`.  Choose any `v` with `Cv=e_*`.
   Then every solution is

   ```text
   a=tau v+k,                 k in ker C.              (11)
   ```

Proof.  The nonsingular statement is inversion and the adjugate identity.
For singular `C`, the annihilator of `im C` is `ker C^T`.  Thus `e_*` is in
the image exactly when every left-kernel vector has zero exceptional
coordinate.  Equations (10)--(11) are then elementary linear algebra.

This dichotomy is fibre-uniform.  What is not fibre-uniform is which branch a
mixed incidence matrix occupies.

## 3. Pure-fibre symmetries

Two exact operations preserve every pure scalar response.

### Core relabelling

Simultaneously permuting the rows of `R^(c)` and the rows and columns of
`A^(c)` merely relabels internal vertices, so every hafnian response is
unchanged.

### Product-one vertex gauge

Choose nonzero scalars `t_0,...,t_6` with

```text
product_i t_i=1.                                      (12)
```

Replace

```text
R_(i,p) -> t_i R_(i,p),
A_(i,j) -> t_i t_j A_(i,j).                           (13)
```

Every matching covers every core vertex exactly once, so every response
monomial is multiplied by `product_i t_i=1`.  Thus (13) is a six-dimensional
torus inside each pure-chart fibre.

These symmetries matter when pure charts are glued: independent core
relabelings can change the mixed row assembly (2), even though no pure ledger
coordinate changes.

## 4. Proportional rows force a large singular branch

### Lemma 2 (proportional-row kernel)

Suppose rows `i,j` of a `7 x 7` incidence matrix satisfy

```text
R_(j,*)=lambda R_(i,*),                 lambda!=0.     (14)
```

For every `k` different from `i,j`, the fifth-compound columns obey

```text
C_5(R)_(*,{i,k})=lambda C_5(R)_(*,{j,k}).             (15)
```

The five relations (15), one for each such `k`, are linearly independent.
Consequently

```text
nullity C_5(R)>=5,                    rank C_5(R)<=16. (16)
```

Proof.  Deleting `{i,k}` leaves row `j`, whereas deleting `{j,k}` leaves row
`i`; all other surviving rows agree.  Permanents are multilinear and
symmetric in their rows, giving (15).  The five relations have disjoint pairs
of column coordinates, so they are independent.

The product-one gauge preserves proportionality, replacing equal rows by
arbitrary nonzero scalar multiples.  Hence any such example extends to a
positive-dimensional singular family inside the pure fibre.

## 5. An exact singular pure-fibre alignment

Use terminal order `(1,2,3,4,5,a,b)` and put `rho^2=21`.  The verified
colour-2 common-terminal chart contains the identical incidence rows

```text
r_1=r_5=(1,0,1,0,0,0,0).                             (17)
```

Relabel its cores so that `r_1,r_5`, and the private row

```text
r_*=(0,0,0,0,1/7,0,0)
```

occupy the three colour-2 positions of `sigma=2220000`.  Put the colour-0
rows `h_3,h_4,h_5,h_a` at the remaining four positions.  The resulting
mixed incidence is

```text
R_sing=
[ 1 0 1 0 0   0 0                    ]
[ 1 0 1 0 0   0 0                    ]
[ 0 0 0 0 1/7 0 0                    ]
[ 0 0 1 0 0   0 -rho                 ]
[ 0 0 0 1 0   0 -5-2rho/21           ]
[ 0 0 0 0 1   0 230+104rho/7         ]
[ 0 0 0 0 0   1 1+16rho/21           ].              (18)
```

This is obtained solely by relabelling two already verified pure scalar
charts.  It therefore remains in their complete pure-ledger fibres.  Lemma 2
immediately gives `det C_5(R_sing)=0`; exact row reduction in the replay finds
rank six.

The prescribed same-colour core edges are zero inside the first three
positions and, among the last four positions,

```text
A_35=rho,
A_45=-6-1/rho,
A_46=1/rho,
A_56=1+22/rho.                                       (19)
```

Set the cross-colour edges

```text
A_03=(-16905+1092rho)/84463,
A_04=(  5747-4778rho)/84463,
A_05=-2rho,
A_06=( 16618- 339rho)/84463,                         (20)
```

and set every other cross-colour edge to zero.

### Theorem 3 (exact degree-five singular escape)

For (18)--(20),

```text
C_5^per(R_sing) a_sigma=0.                            (21)
```

Thus all 21 mixed degree-five faces vanish, including the exceptional face
with `tau=0`.

The primary verifier checks (21) exactly in `Q(sqrt(21))`.  The independent
audit repeats it with its own rational-pair arithmetic.  This is one fixed
linear solve on the six-dimensional compound image, not a solve of the
70-variable pure-chart fibre.

Applying the same gauge (13) simultaneously to all three relabelled charts
before gluing produces a positive-dimensional family of proportional-row
singular escapes.  The displayed member suffices to show that
fifth-compound invertibility is not forced by the pure ledger.

## 6. The exact pure rectangle does not determine a mixed word

Independent Wick deconvolution of the pure ledger gives

```text
Phi_125ab=(rho-2)D_0+((1+rho)/7)D_2,
Phi_145ab=          ((1+rho)/7)D_2,
Phi_235ab=          ((1+rho)/7)D_2,
Phi_345ab=(rho-2)D_1+((1+rho)/7)D_2.                 (22)
```

Therefore

```text
Phi_125ab-Phi_145ab-Phi_235ab+Phi_345ab
 =(rho-2)(D_0+D_1).                                  (23)
```

The `D_2` coefficient cancels.  These four identities are verified exactly
in the primary replay.

Equation (23) fixes three monochromatic diagonal evaluations of the blocker
tensor.  It does not determine any mixed blocker word: a seven-multilinear
form is not determined by its values on the three pure coordinate points.
The singular model (21) makes the selected mixed `2220000` coefficient zero
without changing any pure value in (22).

## 7. Exact boundary

The current conclusion is a conditional theorem, not a global obstruction.

Proved:

- the fibre-uniform invertible/singular fifth-compound dichotomy;
- adjugate circuits on the invertible branch;
- left-kernel/image alternatives on the singular branch;
- a positive-dimensional singular family inside the verified pure-chart
  fibre;
- one exact singular `2220000` completion with every degree-five face zero;
- the deconvolved pure rectangle (22)--(23).

Not proved:

- simultaneous vanishing of mixed degrees one and three for the escape;
- compatibility of the escape across other mixed words;
- one physical tensor graph realizing the full ledger;
- that no other mixed word is forced to violate somewhere on this fibre;
- a universal `P_7` obstruction or the Krenn--Gu conjecture.

In particular, the pure ledgers alone do **not** make
`Delta_5(R_2220000)!=0` fibre-uniform.  A stronger theorem would have to
control the singular kernels jointly across words and degrees, rather than
discarding them as nongeneric.

## Replay

```powershell
uv run --with sympy python verify_p7_pure_chart_fifth_compound_fibre_dichotomy_and_singular_escape.py
python audit_p7_pure_chart_fifth_compound_fibre_dichotomy_and_singular_escape.py
uv run --with sympy --with ruff python -m ruff check verify_p7_pure_chart_fifth_compound_fibre_dichotomy_and_singular_escape.py audit_p7_pure_chart_fifth_compound_fibre_dichotomy_and_singular_escape.py
python -m py_compile verify_p7_pure_chart_fifth_compound_fibre_dichotomy_and_singular_escape.py audit_p7_pure_chart_fifth_compound_fibre_dichotomy_and_singular_escape.py
```

Both replays are fixed exact calculations.  They perform no mixed-word,
support, graph-family, parameter, or pure-fibre enumeration.
