# Cross-root coordinate-monomial chart holonomy and the nine-chart no-go

## Status

**Exact characteristic-zero cross-chart compatibility theorem and sharp
common-edge countermodels.**  The coordinate choice in a two-residual
coordinate-monomial slice is not automatically a global colour label.  It is
a label for the restriction of one fixed residual edge to the two current
simultaneous-kernel spaces.

On overlapping charts there is an exact compatibility law.  Two coordinate
labels can differ only when their coordinate covectors become proportional
on the kernel overlap.  The proportionality scalars define transition gains,
and their product around every chart cycle is one.

This holonomy does not force constant labels.  One fixed rank-one residual
edge on `K^3 x K^3` has nine overlapping torus-plane charts, one for every
ordered coordinate pair `(c,d)`, on which its restriction is exactly

```text
e_c^* tensor e_d^*                                  (1)
```

with scalar one.  All three planes on either shore contain the same torus
line, so even a common torus anchor and common normalization do not identify
the labels.

There is a second sharp boundary for one-dimensional kernel charts.  The
coordinate label is pure gauge on a torus line: every nonzero bilinear value
can be written using any coordinate pair after changing its scalar.  Nine
independent line-pair charts can prescribe arbitrary values for one `3 x 3`
residual edge.  The complete first cross-chart equations appear only as
linear circuits among the rank-one evaluation tensors `x_alpha y_alpha^T`.

Thus changing legal root vectors or blocker charts does not by itself exclude
the coordinate-monomial branch.  A successful proof must use a
target-normalized evaluation circuit, a coordinate-separating overlap, or
the cofactor-valued mixed jets.  The plane and line controls below are not
full GHZ restrictions and are not Krenn--Gu counterexamples.  The global
conjecture remains **UNRESOLVED**.

No support, graph-family, matching-family, colour-word, or tuple enumeration
is used.

## 1. Coordinate-monomial charts

Let `V_0,V_1` be three-dimensional spaces with fixed target coordinate
covectors

```text
epsilon_0,epsilon_1,epsilon_2 in V_0^*,
eta_0,eta_1,eta_2 in V_1^*.                          (2)
```

Let `B:V_0 x V_1 -> K` be the single physical edge between the two residual
vertices.  A root/kernel chart `alpha` supplies simultaneous-kernel spaces

```text
U_alpha subset V_0,          W_alpha subset V_1.     (3)
```

It is a nonzero coordinate-monomial chart of label `(c_alpha,d_alpha)` if

```text
B restricted to U_alpha x W_alpha
 =lambda_alpha epsilon_(c_alpha)|U_alpha
                    tensor eta_(d_alpha)|W_alpha,
lambda_alpha!=0.                                      (4)
```

Every object in (4) is a restriction of fixed global data.  What may change
with the root choice is the pair `(U_alpha,W_alpha)` and therefore which
global coordinate covectors become proportional there.

## 2. The overlap theorem

Take two charts `alpha,beta` and put

```text
X=U_alpha intersect U_beta,
Y=W_alpha intersect W_beta.                          (5)
```

Assume the common restriction of `B` to `X x Y` is nonzero.

### Theorem 1 (coordinate-separation and transition law)

There are nonzero scalars `s_(alpha,beta),t_(alpha,beta)` such that

```text
epsilon_(c_beta)|X
   =s_(alpha,beta) epsilon_(c_alpha)|X,

eta_(d_beta)|Y
   =t_(alpha,beta) eta_(d_alpha)|Y,                  (6)
```

and

```text
lambda_alpha
 =lambda_beta s_(alpha,beta)t_(alpha,beta).          (7)
```

Consequently:

1. if the two left coordinate covectors are independent on `X`, the two
   charts are incompatible;
2. if the two right coordinate covectors are independent on `Y`, they are
   incompatible; and
3. around every cycle of charts with nonzero consecutive overlaps,

   ```text
   product s_(alpha,beta)t_(alpha,beta)=1.            (8)
   ```

Proof.  Restrict (4) for both charts to `X x Y`.  Two nonzero decomposable
tensors are equal only if their left factors are proportional and their
right factors are inversely proportional after the total scalar is included.
This gives (6)--(7).  Multiplying (7) around a cycle cancels all chart
scalars and proves (8).

If `x in X` and `y in Y` are torus vectors, the same transition can be read
without choosing bases:

```text
lambda_alpha epsilon_(c_alpha)(x)eta_(d_alpha)(y)
 =lambda_beta epsilon_(c_beta)(x)eta_(d_beta)(y).     (9)
```

Equation (8) is a multiplicative coordinate holonomy.  It is a necessary
common-edge invariant, not a claim that pairwise overlap agreement is
sufficient to realize the full graph or its cofactor tensors.

## 3. A common residual edge with all nine labels

Now take `V_0=V_1=K^3` with the standard coordinate covectors and put

```text
B(z,w)=z_0 w_0.                                      (10)
```

On the left define

```text
U_0=ker(e_1^*-e_2^*),
U_1=ker(e_0^*-e_1^*),
U_2=ker(e_0^*-e_2^*),                                (11)
```

and define `W_0,W_1,W_2` by the same equations on the right.  Every plane is
two-dimensional, is not contained in a coordinate hyperplane, and contains

```text
v=(1,1,1).                                           (12)
```

On these planes,

```text
e_0^*|U_c=e_c^*|U_c,
e_0^*|W_d=e_d^*|W_d.                                 (13)
```

The first equality is tautological for `c=0` and is the defining equation of
the plane for `c=1,2`; similarly on the right.

### Theorem 2 (nine overlapping plane charts)

For every `(c,d) in {0,1,2}^2`, the one common edge (10) obeys

```text
B|_(U_c x W_d)=e_c^*|U_c tensor e_d^*|W_d.           (14)
```

All nine chart scalars are one, all charts use the same torus residual
vectors `(v,v)`, and every chart value is

```text
h_cd=B(v,v)=1.                                       (15)
```

The three planes on either shore have common intersection `K v`.  On this
line all three coordinate forms agree, so every transition gain in (6) can
be taken to be one and every holonomy (8) is trivial.  Nevertheless the
displayed labels run through all nine ordered coordinate pairs.

This proves that common edge blocks, two-dimensional kernel charts, nonzero
torus overlaps, and synchronized scalar normalization do not force a common
coordinate label.

## 4. One common root-incidence system generates the plane charts

The planes (11) are not merely abstract restrictions.  They arise as
simultaneous kernels while the root vectors vary in one fixed edge-block
system.

Take three left gate roots `r_0,r_1,r_2`, three right gate roots
`s_0,s_1,s_2`, and put

```text
omega=e_0^*-e_1^*,
x_off=(1,1,1),              omega(x_off)=0,
x_on =(2,1,1),              omega(x_on)=1.            (16)
```

Let

```text
g_0=e_1^*-e_2^*,
g_1=e_0^*-e_1^*,
g_2=e_0^*-e_2^*.                                    (17)
```

Use the fixed symmetric edge blocks

```text
B_(r_c,q_0)=omega tensor g_c,
B_(s_d,q_1)=omega tensor g_d,                         (18)
```

and set the crossed root--residual blocks and all root--root blocks to zero.
In chart `(c,d)`, evaluate `r_c,s_d` at `x_on` and the other four gate roots
at `x_off`.  Then the only nonzero root incidence at `q_0` is `g_c`, and the
only nonzero root incidence at `q_1` is `g_d`.  Hence

```text
K_(q_0)=ker g_c=U_c,
K_(q_1)=ker g_d=W_d.                                 (19)
```

All gate-root vectors are fully supported, all root pairs are zero-coupled,
and `span(g_c)` contains no coordinate covector.  Thus both residual vertices
are legal nonblockers in every chart.

The root--blocker chart can be held fixed while the gates switch.  Let
`a=e_2^*`; then

```text
a(x_off)=a(x_on)=1.                                  (20)
```

For arbitrary desired blocker covectors `H_u[root,-]`, install

```text
B_(root,u)=a tensor H_u[root,-].                     (21)
```

Their evaluated root--blocker rows are identical in every one of the nine
gate charts.  Hence the changing coordinate labels cannot be blamed on a
change of the blocker matrix.

The construction addresses exactly the cross-root residual-kernel question.
It uses six gate roots, one for each of the three left and three right chart
labels, so it is not itself a five-root `q=2` `P_7` realization.
No claim is made that the resulting union satisfies the GHZ mixed equations.

## 5. Why line charts carry no coordinate label

Let `U=Kx` and `W=Ky` be torus lines, so every coordinate of `x,y` is
nonzero.  If `B(x,y)=h!=0`, then for every coordinate pair `(c,d)`,

```text
B|_(U x W)
 =[h/(x_c y_d)] e_c^*|U tensor e_d^*|W.              (22)
```

Thus all nine coordinate labels describe the same nonzero restriction.  On
a one-dimensional kernel chart, the label is a choice of trivialization,
not an invariant of the physical residual edge.

This applies directly to the torus-line slice-universality construction:
its label `0,0` may be rewritten as any `(c,d)` without changing one edge or
one matching coefficient.

## 6. The complete line-chart compatibility theorem

For line charts indexed by `alpha`, choose nonzero representatives

```text
U_alpha=K x_alpha,       W_alpha=K y_alpha,
h_alpha=B(x_alpha,y_alpha).                           (23)
```

Put

```text
T_alpha=x_alpha y_alpha^T in V_0 tensor V_1.          (24)
```

### Theorem 3 (evaluation-circuit criterion)

A value vector `(h_alpha)` comes from one common bilinear edge `B` if and
only if

```text
sum_alpha rho_alpha h_alpha=0                         (25)
```

for every linear circuit

```text
sum_alpha rho_alpha T_alpha=0.                        (26)
```

These linear circuit equations generate the complete ideal of the common-
edge value image.  In particular, if the `T_alpha` are independent, the chart
values are arbitrary.

Proof.  Evaluation is the linear map

```text
Ev:V_0^* tensor V_1^* -> K^A,
B |-> (<B,T_alpha>)_alpha.                            (27)
```

The annihilator of its image is exactly the kernel of the transpose map,
which is the circuit space (26).  A linear subspace has an ideal generated by
its annihilating linear forms, proving the assertion.

Since `dim(V_0 tensor V_1)=9`, no common-edge equation is forced on nine
independent line charts.

## 7. Exact nine-chart interpolation

Take the torus bases whose rows are

```text
x_i=(1,t_i,t_i^2),       t_i=1,2,3,
y_j=(1,s_j,s_j^2),       s_j=4,5,6.                  (28)
```

Let `X,Y` be the corresponding `3 x 3` row matrices.  Both are Vandermonde
and invertible.  For an arbitrary `3 x 3` value matrix `H`, define

```text
B=X^(-1) H Y^(-T).                                   (29)
```

Then

```text
B(x_i,y_j)=H_ij                                      (30)
```

for all nine line-pair charts.

### Corollary 4 (nine-chart universality)

Nine torus line charts have no common-edge compatibility equation at all.
If every `H_ij` is nonzero, assign an arbitrary coordinate label
`(c_ij,d_ij)` to every chart and put

```text
lambda_ij=H_ij/(x_i[c_ij]y_j[d_ij]).                 (31)
```

Equations (22) and (30) realize all labels and all values with one physical
edge `B`.  The first possible line-chart obstruction is therefore a circuit
of ten or more evaluations, or an earlier dependence among the tensors
`T_alpha`.  Crucially, its values must be normalized by target data; labels
alone still impose nothing.

## 8. Relation to the existing sharpness theorems

The conclusions fit the three existing boundaries exactly.

1. `TWO_RESIDUAL_COORDINATE_MONOMIAL_SLICE_UNIVERSALITY_NOGO.md` uses the
   common torus line `K(1,1,1)`.  Formula (22) strengthens its interpretation:
   the named coordinate is not identifiable on that slice.
2. `ROOT_TANGENT_COMPANION_NECESSITY_FOR_COORDINATE_SLICE.md` proves that a
   fully global extension needs either nonprojective root--blocker variation
   or two effective tangent companions at every projectively constant root.
   The gate system (18) does not supply those cofactor-valued tangent frames
   and is not claimed to evade that theorem.
3. `ROOT_ARBITRARY_ORDER_TWO_ENDPOINT_FULL_JET_FRAME_SHARPNESS_NOGO.md`
   realizes the full-root two-class frame and companion matching saturation
   but fails an undifferentiated mixed root word.  Theorems 2--3 do not repair
   that failure; they prove only that changing coordinate labels cannot be
   used to exclude it.

Thus the next valid cross-root test must retain data discarded by the label:

```text
normalized residual values h_alpha,
rank-one evaluation tensors T_alpha,
and cofactor-valued tangent transition maps.          (32)
```

An exact circuit (25) whose right target values violate the relation would
exclude the branch.  Neither the current extraction theorems nor the slice
models force such a circuit.

## Scope wall

```text
two-chart overlap proportionality:                    PROVED;
coordinate-separating overlap forces label agreement: PROVED;
cycle transition holonomy:                            PROVED;
one fixed edge with all nine plane labels:             CONSTRUCTED;
common torus anchor and scalar one on all charts:      CONSTRUCTED;
one common gated root-incidence system:                CONSTRUCTED;
coordinate label on a torus line:                      PURE GAUGE;
complete line-chart compatibility ideal:               LINEAR CIRCUITS;
nine independent line charts:                          VALUE-UNIVERSAL;
changing root charts alone excludes coordinate branch: FALSE;
target-normalized ten-chart circuit:                    UNKNOWN;
cofactor-valued transition holonomy:                    UNKNOWN;
full unspecialized GHZ realization:                     NOT CLAIMED;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

## Replay

Run from the repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_cross_root_coordinate_monomial_chart_holonomy_and_nine_chart_no_go.py
python claims/arbitrary-order/audit_cross_root_coordinate_monomial_chart_holonomy_and_nine_chart_no_go.py
python -m py_compile verify_cross_root_coordinate_monomial_chart_holonomy_and_nine_chart_no_go.py audit_cross_root_coordinate_monomial_chart_holonomy_and_nine_chart_no_go.py
uv run --with ruff ruff check verify_cross_root_coordinate_monomial_chart_holonomy_and_nine_chart_no_go.py audit_cross_root_coordinate_monomial_chart_holonomy_and_nine_chart_no_go.py
```

The primary verifier checks the nine plane restrictions, their common torus
overlaps and transition gains, the gated root-kernel system, the evaluation-
tensor rank, and arbitrary symbolic nine-value interpolation.  The independent
no-project-import audit uses separately written rational rank, inverse, and
matrix-product routines.  Neither replay searches root choices, blockers,
supports, words, graphs, or tuple families.
