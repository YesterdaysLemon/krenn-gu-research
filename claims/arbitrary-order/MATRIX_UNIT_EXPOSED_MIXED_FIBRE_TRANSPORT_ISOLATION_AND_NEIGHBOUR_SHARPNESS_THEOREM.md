# Matrix-unit exposed mixed-fibre transport isolation and neighbour sharpness

## Status

This is an exact negative result over the Laurent field `Q(t)` for the
complete eight-vertex label support in the preceding
[`U7D` sharpness theorem](MATRIX_UNIT_COMPLETE_PURE_TARGET_MOMENT_COMPATIBLE_ODD_HOLONOMY_SHARPNESS_THEOREM.md).
It answers the first load-bearing question about using that theorem's
exposed mixed word to constrain the active-cycle holonomy.

The exposed word

```text
eta=00000100
```

does **not** belong to the active transport stratum carrying the holonomy.
Its colour multiplicities are `(7,1,0)`, whereas all three cycle words have
multiplicities `(4,4,0)`, and established bridge transport preserves the
three multiplicities.  Its complete word fibre is the single matching

```text
04|17|26|35.
```

Thus its complete target equation is the monomial equation

```text
lambda_04 lambda_17 lambda_26 lambda_35=0.           (1)
```

On the complete nonzero `r=1` torus, (1) rejects the label support outright.
It does not give a Laurent relation on the active-cycle holonomy `H`.

There is nevertheless one additional exact zero mixed fibre in the complete
`U7D` census.  For

```text
nu=02001121
```

its two complete terms are offdiagonal and cancel.  A one-parameter Laurent
deformation preserves all three pure targets, the three active-cycle
equations, strict support balance, and this fourth mixed equation while
retaining

```text
H=-1
```

and `c_eta=t!=0`.  Hence the smallest nontrivial satisfiable extension of the
three cycle equations visible in this exact table still imposes no holonomy
relation beyond `H+1=0`.

This closes only the proposed continuation from the `U7D` exposed word and
one neighbouring zero fibre.  It does not exclude aggregate fibres, active
holonomy on a hypothetical witness, pure cofactor branching or cycles, the
deeper branch, the `r=1` matrix-unit branch, or the global Krenn--Gu
conjecture.  The global conjecture remains **UNRESOLVED**.

## 1. Fixed label support and active-cycle variables

Keep the endpoint labels of the complete `U7D` table on all `28` physical
pairs, but initially write every nonzero physical amplitude as an
independent Laurent variable `lambda_ij`.

The three active words are

```text
chi_0=00001111,
chi_1=00110011,
chi_2=01010101.                                     (2)
```

Use the imported cross cores, bridges, and pure residuals

```text
E_0=24|35,  B_0=23|45,  P_0=01|67,
E_1=12|56,  B_1=15|26,  P_1=04|37,
E_2=14|36,  B_2=46|13,  P_2=02|57.                 (3)
```

Put

```text
r_i=lambda(B_i)/lambda(E_i),
H=r_0 r_1 r_2.                                      (4)
```

The complete cycle equations are

```text
0=lambda_01 lambda_24 lambda_35 lambda_67
 +lambda_02 lambda_13 lambda_46 lambda_57,          (5a)

0=lambda_01 lambda_23 lambda_45 lambda_67
 +lambda_04 lambda_12 lambda_37 lambda_56,          (5b)

0=lambda_02 lambda_14 lambda_36 lambda_57
 +lambda_04 lambda_15 lambda_26 lambda_37.          (5c)
```

Every displayed monomial is nonzero in the complete matrix-unit branch.
Multiplying the three binomial ratios and cancelling the residual matchings
gives exactly

```text
H=-1.                                               (6)
```

This is the already proved `U7C` equation for a three-step binomial cycle.

## 2. Complete exposed-word equation

Direct compatibility with the fixed endpoint labels gives

```text
F(eta)={04|17|26|35}.                               (7)
```

The term has the exact cross/pure decomposition

```text
cross core:           35,
pure-shore residual:  04|17|26.                    (8)
```

The residual product is nonzero.  There are no other categories hidden in
the fibre:

```text
active-cycle terms:          none;
diagonal rematching terms:   none;
aggregate extra terms:       none;
deeper-blocker terms:        not coefficient monomials;
pure residual terms:         the single product 04|17|26.            (9)
```

The absence of a diagonal rematching also follows before enumeration: the
`0`- and `1`-shores have odd sizes `7` and `1`.  The single cross edge has
cross-count triple

```text
(x_01,x_02,x_12)=(1,0,0),                           (10)
```

which does not have the common parity required by the `U7B` active-core
lemma.  Thus the bridge square/hexagon partition and its
deeper/transport/pure-cancellation trichotomy do not apply at `eta`.

Equation (7) proves (1).  In the Laurent ring where all physical amplitudes
are inverted, the left side of (1) is a unit.  Adding the exposed target
equation therefore gives the unit ideal.  Before localization it forces at
least one physical amplitude to vanish and exits complete `r=1` support.
Neither interpretation produces a new equation in `H`.

## 3. Transport multidegree isolation

Every established bridge transport changes endpoint colours on the selected
cross core but preserves the total number of endpoints of each colour.  The
three relevant multiplicity vectors are

```text
active cycle: (4,4,0),
eta:          (7,1,0).                              (11)
```

Consequently no sequence of the established `U7B` transport/rematching
operations can connect `eta` to `chi_0,chi_1,chi_2`.  Starting from `eta`,
the operation closure is the singleton coefficient equation (1), because
`eta` is outside the domain of the active transport theorem.

This is a grading obstruction, not a claim that equations in different word
characters can never share edge variables.  A new cross-multiplicity theorem
could couple them.  No such theorem is supplied by `U7A`--`U7D`.

## 4. The smallest satisfiable neighbouring mixed subsystem

The complete fixed-label census has `105` perfect matchings in `101` word
fibres.  Exactly four mixed coefficients vanish in the Laurent family below:
the three cycle words and

```text
nu=02001121,       multiplicities (3,3,2).          (12)
```

Its complete fibre is

```text
F(nu)={02|16|35|47, 03|16|24|57}.                  (13)
```

Both terms are offdiagonal.  Thus `D_nu=0`, and its complete equation is

```text
0=lambda_02 lambda_16 lambda_35 lambda_47
 +lambda_03 lambda_16 lambda_24 lambda_57.          (14)
```

Since `lambda_16!=0`, saturation reduces (14) to

```text
0=lambda_02 lambda_35 lambda_47
 +lambda_03 lambda_24 lambda_57.                    (15)
```

This equation genuinely shares `24` and `35` with the first active cross
core and shares `02` and `57` with the third residual matching.  It is
therefore an exact local coupling, not a disjoint dummy equation.

Nevertheless `Q_nu=0` after the two terms cancel and `D_nu=0` by odd-shore
parity.  It is an internally zero fibre, not a new active word.  Therefore
the selected subsystem

```text
{(5a),(5b),(5c),(14)}                               (16)
```

is closed under the established transport data of this table: the three
active equations transport cyclically among themselves, while `nu` is not
in the active transport domain.  It is the smallest nontrivial satisfiable
extension of the active cycle among the table's complete zero fibres.

## 5. Exact Laurent countermechanism

Let `t` be invertible.  Keep all `U7D` endpoint labels and put

```text
lambda_35=t,       lambda_24=-t^(-1),
lambda_47=t^(-2), lambda_06=t^2,
lambda_12=-1,     lambda_14=-1,                     (17)
```

with every other physical amplitude equal to `1`.  At `t=1` this is the
original `U7D` table.

All `28` amplitudes are nonzero in `Q(t)`.  The three pure matching products
are

```text
lambda_03 lambda_17 lambda_26 lambda_45=1,
lambda_06 lambda_15 lambda_23 lambda_47=t^2 t^(-2)=1,
lambda_07 lambda_16 lambda_25 lambda_34=1.           (18)
```

In (5a)--(5c), every offdiagonal term is `-1` and every diagonal term is
`1`.  Moreover (14) becomes

```text
t^(-1)-t^(-1)=0.                                   (19)
```

The three local transport ratios in (4) are all `-1`, so

```text
H=(-1)^3=-1.                                        (20)
```

But the exposed coefficient is

```text
c_eta=t!=0.                                         (21)
```

The strict positive endpoint-balance certificate depends only on the label
support and remains the same certificate with common loads `(7,7,7)`.  Over
`C`, every nonzero specialization of (17) therefore has the exact
moment-balanced representative supplied by the imported coercive-convexity
theorem.  Word-character covariance preserves (5), (14), (18), (20), and
the nonvanishing in (21).

Thus (17) is an exact one-parameter countermechanism to the claim that one
additional locally coupled mixed equation forces a stronger holonomy
condition.  It is not a Krenn--Gu witness.

## 6. Exact elimination statement

Work in the Laurent ring on all physical amplitudes and adjoin `H` with its
defining equation (4).  Let `I` contain the three pure normalizations (18),
the three cycle equations (5), the neighbouring equation (14), and the
definition of `H`.

Equation (6) gives

```text
H+1 in I.                                           (22)
```

The Laurent family (17) defines a homomorphism from the quotient by `I` to
`Q[t,t^(-1)]`, so `I` is proper.  Therefore

```text
I intersect Q[H]=(H+1).                             (23)
```

Indeed an ideal of the principal ideal domain `Q[H]` containing the linear
ideal `(H+1)` is either `(H+1)` or the unit ideal; the family excludes the
latter.  Hence the neighbouring equation contributes no polynomial or
Laurent restriction on `H` beyond the original cycle equation.

If (1) is added, the Laurent ideal becomes the unit ideal.  That is support
exclusion, not holonomy elimination.

## 7. Exceptional cases and exact proof boundary

The case split is explicit:

```text
t=0 or a physical denominator vanishes:
    outside the complete nonzero r=1 Laurent torus;

eta target equation imposed on the fixed support:
    impossible because its complete fibre is one nonzero monomial;

nu equation:
    exact two-term offdiagonal aggregate cancellation, D_nu=Q_nu=0;

aggregate active-cycle fibre:
    not addressed; U7C aggregate exit remains open;

deeper-blocker exit:
    not reached from eta or nu by the hypotheses of U7B and remains open;

pure cofactor branching / alternating even cycles:
    no least even-shore pure cancellation is produced here; both remain open.
```

The exact proof-topology consequence is:

```text
exposed U7D word couples to H through existing transport:     FALSE;
exposed target equation on the fixed complete support:        IMPOSSIBLE;
one additional locally coupled zero mixed fibre exists:       PROVED;
cycle + that neighbouring equation has H=-1 solutions:        PROVED;
extra elimination relation beyond H+1:                        NONE;
all complete mixed equations satisfied by the family:         FALSE;
displayed Laurent family is a Krenn--Gu witness:               FALSE;
aggregate holonomy excluded:                                  UNKNOWN;
pure cofactor branching/cycles excluded:                       UNKNOWN;
deeper-blocker branch excluded:                                UNKNOWN;
r=1 matrix-unit branch excluded:                               UNKNOWN;
global Krenn--Gu conjecture:                                   UNRESOLVED.
```

The next holonomy attack must use mixed equations in the same transport
multidegree, prove a new cross-multiplicity coupling, or invoke one of the
remaining deeper/pure exits.  The exposed `U7D` word and one neighbouring
internally zero fibre are now an exact closed negative route.

## Replay

```powershell
python claims/arbitrary-order/verify_matrix_unit_exposed_mixed_fibre_transport_isolation_and_neighbour_sharpness.py
python claims/arbitrary-order/audit_matrix_unit_exposed_mixed_fibre_transport_isolation_and_neighbour_sharpness.py
python -m py_compile claims/arbitrary-order/verify_matrix_unit_exposed_mixed_fibre_transport_isolation_and_neighbour_sharpness.py claims/arbitrary-order/audit_matrix_unit_exposed_mixed_fibre_transport_isolation_and_neighbour_sharpness.py
python -m ruff check claims/arbitrary-order/verify_matrix_unit_exposed_mixed_fibre_transport_isolation_and_neighbour_sharpness.py claims/arbitrary-order/audit_matrix_unit_exposed_mixed_fibre_transport_isolation_and_neighbour_sharpness.py
```

The primary verifier imports the committed `U7D` matching and label
conventions, then performs an exact sparse-Laurent `Q(t)` census, checks the
complete exposed and neighbouring fibres, the transport multidegrees, the
pure normalizations, the four selected mixed zeros, strict support balance,
and holonomy.  The independent no-import audit separately encodes decimal
endpoint labels, Laurent exponents, and balance weights; traverses matchings
by least-set-bit deletion; packs words in base three; and reconstructs the
holonomy from independent numerator and denominator ledgers.  The scripts
audit the bounded table and family.  The transport-grading and elimination
claims are the written arguments above.
