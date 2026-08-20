# Fixed-Q dense colour-dependent private-permutation exclusion

## Status

**Exact characteristic-zero exclusion of the full private-permutation
root-companion chart.**  Continue in the dense `K_4/K_4`, `h!=0` residue of
`GLD21`.  Assume that, for each of the three GHZ colours separately, the four
root-to-port blocks form a private colour-diagonal perfect matching with
nonzero entries.  The private root--port bijection may depend arbitrarily on
the colour.

No hypothetical witness lies on this chart.  After an exact dense-shore and
diagonal-coordinate normalization, the dead-colour matching is the identity
and the two active matchings are an ordered pair in `S_4 x S_4`.  The complete
ten-vertex coefficient equation is affine-linear in `24` root--residual
entries, `54` root--root entries, and `3` freely allowed pure target scalars.
The `576` permutation pairs reduce to `28` simultaneous-conjugacy and
active-colour-swap orbits.  Every orbit has an exact rational contradiction
certificate using between `5` and `20` coefficient equations.

This strictly extends the common-matching chart excluded by `GLD22`.  It does
**not** exclude nonprivate root-to-port arrays, either proper-secondary-clique
cell, or the other `F=empty` and pure-absorption cells.  It supplies no
weighted-permanent implication.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Dependencies:

- [`GLD21`](FIXED_Q_RESPONSE_MAP_ZERO_DEAD_COLOUR_H_GATE_AND_DENSE_COMPANION_ABSORPTION_THEOREM.md)
- [`GLD22`](FIXED_Q_DENSE_PRIVATE_CROSS_MATCHING_ROOT_COMPANION_EXCLUSION_THEOREM.md)

## 1. Private permutations

Work over a characteristic-zero field `K` with roots and ports

```text
R={r_0,r_1,r_2,r_3},    U={u_0,u_1,u_2,u_3},
```

residual pair `Q={q_0,q_1}`, and colours `{c,d,a}`, where `a` is the dead
colour from `GLD21`.  Retain the dense conclusions

```text
h=H_Q(z_Q)!=0,
B_ij=0,
K_ij(c,c)K_ij(d,d)!=0,
K_ij(s,t)=0 for s!=t,
v_i^a=(x_i^a,y_i^a)=0                         (1)
```

for all distinct ports `i,j`.  Here

```text
v_i^s=(x_i^s,y_i^s),
K_ij(s,t)=x_i^s y_j^t+y_i^s x_j^t.            (2)
```

### Definition 1 (colour-dependent private chart)

For each colour `s`, choose a permutation `pi_s in S_4` and nonzero scalars
`tau_i^s`.  The root-to-port array is **private colour-diagonal by colour**
when

```text
W_(r_j,u_i)(-,e_s)=0                         if j!=pi_s(i),
W_(r_(pi_s(i)),u_i)(-,e_s)
  =tau_i^s e_(pi_s(i),s)^*.                  (3)
```

Thus every colour slice is a monomial `4 x 4` cross array, but the three
monomial supports need not agree.  No restriction is imposed on any
root--root or root--residual block.

`GLD22` is precisely the subchart `pi_c=pi_d=pi_a`.

## 2. The dense chart has one canonical gauge

### Lemma 2 (shore lines)

There are nonzero vectors `C,D in K^2` and nonzero scalars
`lambda_i,mu_i` such that

```text
v_i^c=lambda_i C,
v_i^d=mu_i D,
<C,D>=0,
<C,C><D,D>!=0,                               (4)
```

where `<(x,y),(x',y')>=xy'+yx'`.

### Proof

Fix `i`.  By (1), the three nonzero vectors `v_j^d`, `j!=i`, lie in the
one-dimensional orthogonal complement of `v_i^c`.  Comparing two choices of
`i` through one common nonzero `v_j^d` shows that all `v_i^c` span one line.
The same argument with `c,d` exchanged gives the second line.  The diagonal
pairings in (1) make both lines nonisotropic, proving (4).  `square`

### Lemma 3 (canonical normalization)

If a witness satisfying Definition 1 exists over `K`, then after extending
scalars to an algebraic closure and making invertible diagonal changes in the
residual contraction and in the colour coordinates at the eight external
vertices, there is a witness with

```text
h=1,
v_i^c=(1,1),    v_i^d=(1,-1),    v_i^a=(0,0),
tau_i^s=1,
pi_a=id.                                           (5)
```

The two active permutations remain arbitrary.

### Proof

Write `C=(C_0,C_1)`.  Nonisotropy gives `C_0 C_1!=0`, and orthogonality gives
`D` proportional to `(C_0,-C_1)`.  Rescaling the two residual contraction
coordinates sends these lines to `(1,1)` and `(1,-1)`.  Their common remaining
scale can be chosen so that the nonzero residual edge value becomes `h=1`;
passing to the algebraic closure permits the required square root.

Now rescale the active colour coordinate at each port to remove `lambda_i`
or `mu_i`.  For each colour, `pi_s` is a bijection, so the corresponding four
root-colour coordinates can then independently remove the four `tau_i^s`.
Do the same for the dead colour and relabel the roots relative to the ports to
make `pi_a=id`.

All changes are invertible.  They preserve the monomial zero pattern and
send a diagonal GHZ target to another diagonal GHZ target, with possibly
changed pure coefficients.  Existence over `K` would therefore imply
existence on (5).  `square`

Allowing an algebraic extension only strengthens the exclusion: an exact
rational inconsistency on (5) persists over every characteristic-zero field.

## 3. Complete normalized coefficient system

Put

```text
p_(epsilon,r,t)=W_(r,q_epsilon)(e_(r,t),z_(q_epsilon)),
w_(rs,tv)=W_(r_r,r_s)(e_(r,t),e_(s,v)).             (6)
```

There are `2*4*3=24` entries `p`, `6*3*3=54` entries `w`, and three target
scalars `alpha_c,alpha_d,alpha_a`.  We deliberately allow the `alpha` values
to be arbitrary, including zero; inconsistency in this enlarged target class
is stronger than the required GHZ inconsistency.

For a port word `omega`, define

```text
f_omega(i)=pi_(omega_i)(i).                          (7)
```

For each of the `3^4` port words and `3^4` root words, expand the complete
ten-vertex perfect-matching coefficient.  Since `B_ij=0`, every nonzero
matching has exactly one of three types.

1. `q_0--q_1` and four root--port edges.  This contributes `1` exactly when
   `f_omega` is bijective and the induced root colours equal the root word.
2. One residual--root edge, one residual--port edge, and three root--port
   edges.  Omitting port `i`, the other three values of `f_omega` must be
   distinct.  The missing root contributes

   ```text
   y^(omega_i) p_(0,r,t)+x^(omega_i) p_(1,r,t),      (8)
   ```

   where `x=(1,1,0)` and `y=(1,-1,0)`.
3. Two residual--port edges, two root--port edges, and one root--root edge.
   Omitting ports `i,j`, the other two `f_omega` values must be distinct.  The
   missing root pair contributes

   ```text
   K(omega_i,omega_j) w_(rs,tv),                     (9)
   K(c,c)=2, K(d,d)=-2, K(s,t)=0 otherwise.
   ```

Subtract `alpha_s` only on the root/port word that is monochromatic in `s`.
This produces an affine rational system with `81` unknowns.  The list above
is exhaustive by vertex count: every other matching either contains a direct
port--port edge or more than one unrestricted root block and hence vanishes
in the dense chart.

## 4. Exhaustive private-permutation certificate

After `pi_a=id`, simultaneous relabelling of the identified root/port indices
acts by conjugation on `(pi_c,pi_d)`.  Swapping the two active colours exchanges
the pair; on (8)--(9) this is accompanied by the invertible variable change
`p_0 -> -p_0` and `w -> -w`, which exchanges `K(c,c)=2` and `K(d,d)=-2`.
The `576` ordered pairs split into the following `28` orbits.  Permutations
are displayed by their image tuples; `core` is the number of coefficient
equations in the exact contradiction certificate.

| `pi_c` | `pi_d` | orbit | core |
|---|---:|---:|---:|
| `0123` | `0123` | 1 | 20 |
| `0123` | `0132` | 12 | 11 |
| `0123` | `0231` | 16 | 5 |
| `0123` | `1032` | 6 | 9 |
| `0123` | `1230` | 12 | 8 |
| `0132` | `0132` | 6 | 20 |
| `0132` | `0213` | 24 | 6 |
| `0132` | `0231` | 48 | 10 |
| `0132` | `1023` | 6 | 9 |
| `0132` | `1032` | 12 | 10 |
| `0132` | `1203` | 48 | 9 |
| `0132` | `1230` | 48 | 7 |
| `0132` | `2301` | 24 | 8 |
| `0132` | `2310` | 24 | 5 |
| `0231` | `0231` | 8 | 16 |
| `0231` | `0312` | 8 | 5 |
| `0231` | `1032` | 48 | 7 |
| `0231` | `1203` | 24 | 7 |
| `0231` | `1230` | 48 | 11 |
| `0231` | `1302` | 48 | 10 |
| `0231` | `1320` | 24 | 12 |
| `1032` | `1032` | 3 | 20 |
| `1032` | `1230` | 24 | 9 |
| `1032` | `2301` | 6 | 5 |
| `1032` | `2310` | 12 | 8 |
| `1230` | `1230` | 6 | 9 |
| `1230` | `1302` | 24 | 9 |
| `1230` | `3012` | 6 | 11 |

The orbit sizes sum to `576`.  For every representative, exact Gaussian
elimination over `Q` returns multipliers `lambda_j` on the displayed
coefficient equations such that

```text
sum_j lambda_j A_j=0,       sum_j lambda_j b_j=1.    (10)
```

Thus the same equations assert `0=1`.  The certificate coefficients are
exact fractions; no modular or numerical inference is used.  Equation (10)
persists after scalar extension to every characteristic-zero field.

### Theorem 4 (private-permutation exclusion)

The dense `K_4/K_4`, `h!=0` residue of `GLD21` contains no hypothetical
witness satisfying Definition 1.

### Proof

Assume such a witness.  Lemma 3 carries it to the normalized chart (5), with
some ordered pair `(pi_c,pi_d) in S_4 x S_4`.  The complete matching expansion
in Section 3 is an affine subsystem of its GHZ coefficient identities, while
allowing all `81` entries to vary independently only enlarges the solution
set.  The pair belongs to one of the `28` exact orbits.  Its certificate (10)
contradicts the normalized coefficient system.  Therefore no normalized
witness, and hence no original witness, exists.  `square`

## 5. Exact frontier and scope ledger

```text
GLD21 dense h!=0 companion normal form:                 INPUT;
one private colour-diagonal bijection per colour:       ASSUMED;
dense shore / scalar gauge normalization:              PROVED;
ordered active permutation pairs:                      576;
symmetry orbit representatives:                        28;
exact rational contradiction cores:                    28;
common-private GLD22 chart:                             INCLUDED;
full colour-dependent private-permutation chart:        EMPTY;
nonprivate root-to-port arrays:                         UNKNOWN;
proper-secondary-clique h!=0 cells:                     UNKNOWN;
other F=empty / pure-absorption cells:                  UNKNOWN;
weighted permanent implication:                        UNKNOWN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

Scope:

- **field:** characteristic zero, with a harmless algebraic scalar extension
  used only for invertible normalization;
- **breadth:** one fixed graph, residual pair, fully supported contraction,
  four roots, and one four-port window;
- **response hypothesis:** the dense `K_4/K_4` literal all-seven
  response-map-zero cell of `GLD21`;
- **root-to-port subcell:** one arbitrary private bijection in each colour,
  colour diagonal with twelve nonzero entries;
- **unrestricted graph data:** all `24` root--residual and `54` root--root
  coefficient entries are free in the certificate system;
- **target:** all three pure diagonal coefficients are freely variable;
- **excluded object:** the complete private-permutation chart, not the whole
  dense cell;
- **permanent implication:** none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_colour_dependent_private_permutation_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_dense_colour_dependent_private_permutation_exclusion.py
```

The primary verifier constructs the system from a separately enumerated list
of all `945` perfect matchings.  It proves the `28`-orbit cover, generates
exact `Fraction` contradiction multipliers, replays `lambda A=0` and
`lambda b=1`, and pins the certificate digest.

The independent audit imports neither the primary nor third-party algebra.
It derives the equations anew from the three matching types, performs no
symmetry reduction, and separately eliminates all `576` ordered pairs over
`Fraction`.  Its exact inconsistent-rank distribution is

```text
rank 75: 2,  rank 76: 56,  rank 78: 63,
rank 79: 305, rank 80: 150.                           (11)
```

The checkers discharge the finite permutation case cover and coefficient
arithmetic.  The shore-line argument, scalar-extension normalization, and
bridge from a physical witness to the normalized affine system remain the
load-bearing written proof.
