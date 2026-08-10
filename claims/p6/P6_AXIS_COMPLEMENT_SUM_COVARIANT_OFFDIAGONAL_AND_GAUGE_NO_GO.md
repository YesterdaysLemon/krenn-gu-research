# P6 axis complement-sum covariant and off-diagonal/gauge no-go

## Status

**Exact characteristic-zero tensor obstruction for the canonical physical
six-face section.**  The scalar section from the preceding theorem realizes
the three pulled-back Segre face columns by diagonal `3 x 3` edge blocks, but
has a nonzero mixed-colour coefficient.  This note proves that adding
arbitrary off-diagonal entries to those same edge blocks cannot make all six
faces GHZ diagonal while retaining the prescribed diagonal entries.

The proof uses only the first mixed layer.  For two target colours `c,d`,
the coefficient of a word with one `d`-coloured vertex and five `c`-coloured
vertices is linear in the directed off-diagonal edge entries.  Across the
six synchronized faces these are the **axis equations**.  Their exact kernel
is five-dimensional, but every kernel vector is supported entirely inside
the four-vertex core: it is a directed core circulation with zero row and
column sums.  In particular, every off-diagonal entry incident to the
four-window is forced to zero.

The next `4+2` word is then fatal.  On a face `C union {p,q}`, colour the core
by `c` and both window vertices by `d`.  All cross-colour alternatives have
just been killed, while the matching `p--q` times a pure core matching has
coefficient

```text
3 b_pq^(d) !=0.                                       (1)
```

Thus none of the six faces is GHZ diagonal under an off-diagonal completion.
The obstruction is controlled by a two-coordinate complement-sum covariant
of the pure face column.  For a colour `c`, put

```text
kappa_c=(
 (y_45^c+y_67^c)-(y_46^c+y_57^c),
 (y_45^c+y_67^c)-(y_47^c+y_56^c)).                   (2)
```

Whenever `kappa_c` and `kappa_d` are nonzero, the axis collapse holds for
the canonical section.  All three exact Segre columns have nonzero
`kappa`.  Hence every colour pair is excluded.

A local gauge which maps one concise order-six three-colour GHZ tensor to
another does not evade the result.  Every such gauge consists only of a
common colour permutation and invertible vertexwise diagonal scalings.  Such
monomial gauges preserve the zero/nonzero status of mixed coefficients and
cannot turn the coefficient (1) into zero.

This is a genuine tensor no-go, but only for the canonical scalar section
and its target-stabilizer gauge orbit.  The six pure face values have other
scalar graph realizations because the face morphism has large fibres.  It is
**UNKNOWN** whether a different point of those fibres, or a gauge not in the
target stabilizer but preserving only the prescribed pure face columns,
makes the axis kernel large enough to admit a full mixed-colour cancellation.
It is also unknown whether the independently prescribed `H_4` target
incidence forces the canonical-type axis covariant.  No unrestricted `P_6`
obstruction, Krenn--Gu counterexample, or global proof is claimed.  Global
Krenn--Gu remains **UNRESOLVED**.

No colour words, graphs, supports, gauges, parameter tuples, or finite fields
are enumerated or searched.  The proof uses the symbolic `5+1` coefficient
family and one structurally forced `4+2` coefficient.  The fixed replays
only audit the resulting linear operator and identities.

## 1. The canonical three-colour scalar section

Let

```text
C={0,1,2,3},                 W={4,5,6,7}.              (3)
```

For each colour `c`, keep the pure diagonal scalar graph in the general
section form

```text
a_ij^(c)=1                                      i,j in C,
a_ip^(c)=tau_c                                  i in C,p in W,
b_pq^(c)=(y_pq^(c)-12 tau_c^2)/3                p,q in W,      (4)
```

where `tau_c!=0`.  Then

```text
haf A^(c)[C]=3,
haf A^(c)[C union {p,q}]=y_pq^(c).                    (5)
```

Let a general bilinear edge block retain these diagonal entries but have
arbitrary off-diagonal entries.  For distinct colours `c,d`, define the
directed variable

```text
x_vu=B_vu[d,c].                                       (6)
```

Thus `x_vu` is the edge value when vertex `v` receives the minority colour
`d` and vertex `u` receives the majority colour `c`.  Symmetry of the graph
block says that the reverse colour assignment is `x_uv`; the two directions
are independent entries of the same `2 x 2` colour subblock.

## 2. The complete axis equations

Fix a face

```text
S_pq=C union {p,q}.                                   (7)
```

Give one vertex `v in S_pq` colour `d` and every other vertex colour `c`.
In every perfect matching, `v` has a unique partner `u`; the remaining four
vertices are monochromatic.  Vanishing of that mixed target coefficient is
therefore exactly

```text
sum_(u in S_pq minus {v})
 x_vu haf A^(c)[S_pq minus {v,u}]=0.                  (8)
```

These are thirty-six linear equations for the ordered pair `(d,c)`.  The
thirty-six equations with singleton colour `c` and majority colour `d` are
the same construction for `X^T` with the scalar graph `A^(d)`.  Together
they form a `72 x 56` operator on the directed entries of the complete
eight-vertex graph.

Equation (8), rather than a word list, is the entire `5+1` coefficient
family.

## 3. Complement-sum collapse

For a fixed majority colour `c`, put

```text
r_i=sum_(j in C minus {i}) x_ij,              i in C. (9)
```

### Lemma 1 (majority-axis port collapse)

If `kappa_c!=0`, equations (8) imply

```text
r_i=0,                  x_ip=0
       for every i in C,p in W.                       (10)
```

### Proof

Take the singleton vertex to be a core vertex `i`.  Pairing it to another
core vertex leaves two core and two window vertices.  By the synchronized
four-deck formula, their pure `c`-hafnian is

```text
b_pq^(c)+2 tau_c^2.                                   (11)
```

Pairing `i` to `p` or `q` leaves three core vertices and one window vertex,
whose hafnian is `3 tau_c`.  Thus (8) is

```text
(b_pq^(c)+2 tau_c^2) r_i
 +3 tau_c(x_ip+x_iq)=0              for every p<q in W. (12)
```

For four scalars `xi_p=x_ip`, their six pair sums obey

```text
(xi_4+xi_5)+(xi_6+xi_7)
=(xi_4+xi_6)+(xi_5+xi_7)
=(xi_4+xi_7)+(xi_5+xi_6).                             (13)
```

Apply (13) to (12).  After multiplication by `3 tau_c`, the common
`2 tau_c^2` terms cancel and give

```text
r_i((b_45+b_67)-(b_46+b_57))=0,
r_i((b_45+b_67)-(b_47+b_56))=0.                       (13a)
```

Replacing `b` by `y` multiplies each displayed complement difference by
three.  Thus `kappa_c!=0` forces `r_i=0`.  Equation (12) and `tau_c!=0` now
give `x_ip+x_iq=0` for all pairs.  Over characteristic zero, all four
`x_ip` are zero, proving (10).

Apply Lemma 1 to the reversed singleton assignment: its matrix is `X^T`, its
majority graph is `A^(d)`, and its covariant is `kappa_d`.

### Theorem 2 (exact axis kernel)

If `kappa_c!=0` and `kappa_d!=0`, all seventy-two axis equations hold if and
only if

```text
x_vu=0                 whenever v or u lies in W,
sum_(j in C minus {i})x_ij=0,
sum_(j in C minus {i})x_ji=0           for every i in C.             (14)
```

The kernel is the five-dimensional space of hollow directed `4 x 4` core
matrices with zero row and column sums.

### Proof

Lemma 1 for majority `c` kills `x_ip` and the core row sums.  Applied to
`X^T` with majority `d`, it kills `x_pi` and the core column sums.

It remains to use (8) with a window singleton `p`.  Pairing `p` to `q`
leaves the pure core hafnian `3`; pairing it to a core vertex leaves a
three-core/one-window hafnian `3 tau_c`.  Hence

```text
3 x_pq+3 tau_c sum_(i in C)x_pi=0.                    (15)
```

The already proved `x_pi=0` gives `x_pq=0`.  Reversing `p,q` handles the
other direction.  This proves necessity.

Conversely, (14) makes every window-singleton equation zero and reduces each
core-singleton equation to its zero row or column sum.  Hence it is also
sufficient.

A hollow directed `4 x 4` matrix has twelve coordinates.  Its four row and
four column sums impose seven independent conditions, because the total row
sum equals the total column sum.  The kernel dimension is therefore
`12-7=5`.

This five-dimensional survivor is a circulation/gauge shadow, but it is
confined to the core and cannot affect a window-minority coefficient.

## 4. The forced `4+2` obstruction

### Theorem 3 (off-diagonal completion no-go)

Assume `kappa_c,kappa_d` are nonzero and all window diagonal weights
`b_pq^(d)` are nonzero.  No choice of off-diagonal edge-block entries can
make all six tensors on `C union {p,q}` GHZ diagonal while retaining the
pure scalar section (4).

### Proof

After imposing the necessary `5+1` equations, Theorem 2 kills every
off-diagonal entry between a window vertex and any other vertex.  In the
face `S_pq`, colour every core vertex by `c` and both window vertices by `d`.

If `p` and `q` are not paired together, each must pair with a core vertex,
and the matching product contains a killed off-diagonal entry.  The only
surviving matching family pairs `p` to `q`; the core contributes its three
pure matchings.  The mixed coefficient is therefore

```text
b_pq^(d) haf A^(c)[C]=3 b_pq^(d),                     (16)
```

which is nonzero.  This contradicts GHZ diagonality.

The proof uses no equation of colour type `3+3` or `2+2+2`: the first two
mixed layers already close this canonical section.

## 5. Application to the exact Segre columns

For the three face columns

```text
y^(0)=(14,-24,20,15,-29,9),
y^(1)=(10,-33,36,30,-58,18),
y^(2)=(2,38,-45,-30,73,-23),                         (17)
```

in pair order `45,46,47,56,57,67`, their three complementary sums and
covariants are

```text
colour 0: (23,-53,35),       kappa_0=(76,-12),
colour 1: (28,-91,66),       kappa_1=(119,-38),
colour 2: (-21,111,-75),     kappa_2=(-132,54).       (18)
```

Every covariant is nonzero.  At `tau_c=1`, all eighteen `b_pq^(c)` are
nonzero by the preceding section table.  Theorem 3 therefore applies to
each of the three colour pairs.  For example, on face `C union {4,5}` with
core colour zero and window colour two, the forced coefficient is

```text
3 b_45^(2)=3(-10/3)=-10.                              (18a)
```

This is a new `4+2` obstruction; it does not rely on protecting the earlier
`2+2+2` coefficient `-10/3` against the surviving core circulations.

The exact axis matrices for all three colour pairs have

```text
shape 72 x 56,       rank 51,       nullity 5,         (19)
```

and their nullspaces have precisely the core-circulation support (14).  The
replays check (19) independently, but Theorem 2 is the arbitrary-parameter
proof.

## 6. GHZ-to-GHZ gauges are monomial

For nonzero coefficient triples `lambda,mu`, let

```text
Delta(lambda)=sum_(c=0)^2 lambda_c e_c^(tensor 6).    (20)
```

### Theorem 4 (GHZ-to-GHZ gauge boundary)

Suppose invertible local maps `G_1,...,G_6` satisfy

```text
(G_1 tensor ... tensor G_6) Delta(lambda)=Delta(mu).  (21)
```

Then there is one permutation `pi of {0,1,2}` and nonzero scalars
`gamma_(i,c)` such that

```text
G_i e_c=gamma_(i,c)e_(pi(c)),
lambda_c product_(i=1)^6 gamma_(i,c)=mu_(pi(c)).      (22)
```

Thus every gauge between concise GHZ tensors is a common colour permutation
followed by vertexwise diagonal scaling.

### Proof

Flatten (21) between the first mode and the other five.  Since `G_1` is
invertible, the three decomposable tensors

```text
tensor_(i=2)^6 G_i e_c
```

form a basis of the diagonal subspace
`span{e_0^(tensor 5),e_1^(tensor 5),e_2^(tensor 5)}`.  A nonzero decomposable
tensor in this subspace is a scalar multiple of one coordinate power: if
two diagonal coefficients were nonzero, its first-versus-rest flattening
would have rank at least two.  Therefore every `G_i e_c`, `i>=2`, is
proportional to one common coordinate vector.  Invertibility makes the three
coordinates a permutation.  The first mode follows from (21), and equality
of the pure coefficients gives the weighted product condition in (22).

Monomial transformations multiply every tensor coefficient by a nonzero
scalar and permute its colour label.  They preserve zero versus nonzero.
Hence the mixed obstruction (16) survives every GHZ-to-GHZ gauge.

## 7. Translation and exact residual

The axis operator is the first catalecticant of the mixed-colour coefficient
ideal: it linearizes the tensor completion problem around the three pure
scalar graphs.  Its surviving five-space is the intersection of the row-zero
and column-zero flow spaces on the directed complete core.  The covariant
`kappa` is the two-dimensional quotient of the three perfect-matching sums
on `K_4`; it detects whether the six pair-sum equations can carry a nonzero
core row or column sum.

This gives a compact alternative to eliminating hundreds of mixed words:

```text
5+1 axis equations
  -> complement-sum covariant
  -> port off-diagonals vanish
  -> one 4+2 coefficient is forced nonzero.           (23)
```

The terminology is an organizing translation.  Equations (8), (12), and
(16) are the proved content.

The remaining branch must leave the canonical scalar section or its
target-stabilizer gauge orbit.  A future obstruction can try to prove that
the independently exposed `H_4` target sensor forces `kappa!=0` and trivial
port projection for **every** scalar realization of the six pure face
columns.  Conversely, a construction must find a different scalar fibre on
which the axis kernel has nonzero port support and then solve the `4+2`,
`3+3`, and `2+2+2` equations.

## Scope wall

```text
complete symbolic 5+1 axis family:                    DERIVED;
axis complement-sum covariant kappa:                  DERIVED;
canonical-section axis kernel:                        CORE CIRCULATIONS;
axis rank / nullity:                                  51 / 5;
off-diagonal entries incident to W:                   FORCED ZERO;
forced 4+2 coefficient:                               3 b_pq^(d);
off-diagonal completion of exact Segre section:       IMPOSSIBLE;
GHZ-to-GHZ nonmonomial local gauge:                    IMPOSSIBLE;
canonical section and its target-stabilizer orbit:     EXCLUDED;
non-stabilizer gauge preserving only pure columns:     UNKNOWN;
other scalar graph fibres with the same pure faces:   UNKNOWN;
fixed H4 target incidence forces this axis stratum:   UNKNOWN;
unrestricted P6 obstruction or construction:          UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.      (24)
```

## Replay

```powershell
uv run --with sympy python claims/p6/verify_p6_axis_complement_sum_covariant_offdiagonal_and_gauge_no_go.py
python claims/p6/audit_p6_axis_complement_sum_covariant_offdiagonal_and_gauge_no_go.py
python -m py_compile claims/p6/verify_p6_axis_complement_sum_covariant_offdiagonal_and_gauge_no_go.py claims/p6/audit_p6_axis_complement_sum_covariant_offdiagonal_and_gauge_no_go.py
uv run --with ruff ruff check claims/p6/verify_p6_axis_complement_sum_covariant_offdiagonal_and_gauge_no_go.py claims/p6/audit_p6_axis_complement_sum_covariant_offdiagonal_and_gauge_no_go.py
```

The primary replay constructs the three exact `72 x 56` axis matrices,
checks rank, nullity, and core-circulation support, verifies the complement
covariants and forced `4+2` coefficients, and checks a fixed monomial gauge.
The independent no-import audit rebuilds the operator from a separate
matching recurrence and uses exact rational row reduction.  Neither replay
enumerates colour words or searches any graph, support, gauge, parameter
family, or finite field.

## Dependencies

- [`P6_PHYSICAL_SIX_FACE_HAFNIAN_SECTION_FOUR_DECK_SYNCHRONIZATION_AND_SEGRE_SHARPNESS.md`](P6_PHYSICAL_SIX_FACE_HAFNIAN_SECTION_FOUR_DECK_SYNCHRONIZATION_AND_SEGRE_SHARPNESS.md)
- [`P6_CLEAN_TWO_BY_THREE_SELECTOR_SEGRE_PULLBACK_AND_TORUS_PERMISSION_THEOREM.md`](P6_CLEAN_TWO_BY_THREE_SELECTOR_SEGRE_PULLBACK_AND_TORUS_PERMISSION_THEOREM.md)
- [`P6_FOUR_ROOT_FULL_H4_SENSOR_AND_TARGET_INCIDENCE_BOUNDARY.md`](P6_FOUR_ROOT_FULL_H4_SENSOR_AND_TARGET_INCIDENCE_BOUNDARY.md)
