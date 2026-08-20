# Fixed-Q dense private-cross-matching root-companion exclusion

## Status

**Exact characteristic-zero exclusion of a same-graph integrability
subcell.**  Continue in the dense `K_4/K_4`, `h!=0` residue of `GLD21`.
Assume the four root-to-port blocks have one common private matching in the
three GHZ colours: after relabelling roots and ports, the contraction of
`r_i--u_j` against port colour `s` is zero for `i!=j`, while the private
edge `r_i--u_i` sends colour `s` to a nonzero multiple of the same root
colour.

No hypothetical witness lies on this chart.  The proof uses two already
legal families of coefficients from the complete same-graph equation.

1. A dense `2+1+1` word with both repeated-port roots flipped to the other
   active colour has only one possible matching term.  It forces the
   corresponding active diagonal coefficient of the root--root edge to
   vanish.
2. A Hamming-one word makes each active one-`Q` companion equal to `-h`
   times its private matching word.  On the matching `2+1+1` root word there
   are three active singleton positions, so the coefficient is

   ```text
   h-3h=-2h,
   ```

   after the root--root diagonal from step 1 is removed.  This is nonzero in
   characteristic zero because `GLD21` already proves `h!=0`.

Thus the standard common private full-rank companion chart cannot integrate
the forced pure `G_U(a^4)` slice together with the dense nuisance
absorptions.  This is a genuine same-graph principal-permanent obstruction,
not a formal companion-array rank test.

The theorem does **not** exclude nonprivate cross-edge arrays, charts whose
private matching depends on colour, either proper-secondary-clique cell, or
the other `F=empty` and pure-absorption cells.  It supplies no weighted
permanent restriction.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Dependencies:

- [`GLD21`](FIXED_Q_RESPONSE_MAP_ZERO_DEAD_COLOUR_H_GATE_AND_DENSE_COMPANION_ABSORPTION_THEOREM.md)
- [`GLD20`](FIXED_Q_RESPONSE_MAP_ZERO_GLOBAL_PHYSICAL_CHANNEL_SUPPORT_AND_COMPLEMENTARY_PURE_ABSORPTION_THEOREM.md)

## 1. Dense fixed-contraction notation

Work over a characteristic-zero field `K`.  Retain one graph, four roots

```text
R={r_0,r_1,r_2,r_3},
```

one residual pair `Q={q_0,q_1}`, four ports

```text
U={u_0,u_1,u_2,u_3},
```

the fully supported residual contraction, and the ternary GHZ basis.  Write
the two corrected-active colours as `c,d` and the dead colour as `a`.

Use the contracted quantities from `GLD21`:

```text
h=H_Q(z_Q)!=0,
x_i^s=W_(q_0,u_i)(z_(q_0),e_s),
y_i^s=W_(q_1,u_i)(z_(q_1),e_s),
K_ij(s,s)=x_i^s y_j^s+y_i^s x_j^s.                  (1)
```

In the dense `K_4/K_4` cell,

```text
K_ij(c,c)K_ij(d,d)!=0               for i!=j,
x_i^a=y_i^a=0,
B_ij=0.                                                (2)
```

Here `B_ij` is the residual-absent direct port block.  Equations (2) are
exactly the dense conclusions of `GLD21`; they are not new assumptions about
an arbitrary response window.

For the root-to-residual covectors put

```text
p_i^0=W_(r_i,q_0)(-,z_(q_0)),
p_i^1=W_(r_i,q_1)(-,z_(q_1)),
L_i^s=y_i^s p_i^0+x_i^s p_i^1 in L_(r_i)^*.          (3)
```

Thus `L_i^s` is the sum of the two matchings in which one residual endpoint
meets `r_i` and the other meets `u_i` in colour `s`.

## 2. The common private colour-diagonal chart

### Definition 1 (private cross matching)

The root-to-port array is **common private colour-diagonal** if, after one
common relabelling of `R` and `U`, there are scalars

```text
tau_i^s!=0             (i in {0,1,2,3}, s in {a,c,d}) (4)
```

such that

```text
W_(r_i,u_j)(-,e_s)=0                    for i!=j,
W_(r_i,u_i)(-,e_s)=tau_i^s e_(i,s)^*.   (5)
```

The same root--port bijection is used for all three colours.  The twelve
scalars are arbitrary and nonzero.  No assumption is made on the six
root--root blocks or the eight root--residual blocks.

For a port word `omega=(omega_0,...,omega_3)`, put

```text
P(omega)=product_i tau_i^(omega_i).                   (6)
```

### Lemma 2 (private companion support)

On (5), the root companion `G_U` has exactly one nonzero root word above
each port word:

```text
G_U(-_R;omega)=P(omega)
  e_(0,omega_0)^* tensor ... tensor e_(3,omega_3)^*.  (7)
```

If the outside partner set is `{q} union (U-{u_i})`, its companion has the
same three private root--port factors and the remaining root factor is the
appropriate root--residual covector.  Consequently a one-`Q` companion can
change the root colour relative to the port word at at most one position.

### Proof

In `G_U`, every root must meet a distinct port.  The zero off-private blocks
in (5) leave only the identity bijection, proving (7).  After replacing one
port by one residual endpoint, the three retained ports again force their
three private roots; the remaining root meets the residual endpoint.  Hence
only that root position can differ from the port word.  `square`

The condition is a positive-dimensional physical chart.  It is the
colour-diagonal version of the standard private-port full-rank companion
construction; it is much stronger than the private missing-colour slice used
as a sharpness control in `GLD21`.

## 3. Hamming-one equations fix the active singleton companions

### Lemma 3 (active single-site value)

Every hypothetical witness on (5) satisfies, for every port `i` and active
colour `s in {c,d}`,

```text
L_i^s=-h tau_i^s e_(i,s)^*.                           (8)
```

### Proof

Evaluate the complete fixed-`Q` equation on the port word which has colour
`s` at `u_i` and dead colour `a` at the other three ports.  `GLD21`'s exact
Hamming-one ledger leaves only `H_Q=h` and the two one-`Q` pair labels at
`u_i`.  The target coefficient is zero.

By Lemma 2, the common factor at the other three roots is

```text
product_(j!=i) tau_j^a e_(j,a)^*.
```

It is nonzero by (4).  Cancelling it from the root-tensor identity leaves

```text
h tau_i^s e_(i,s)^*+L_i^s=0,
```

which is (8).  This is a vector equality, not merely its `s` coordinate.
`square`

## 4. Opposite repeated colour kills the root--root diagonal

Fix an edge `e={i,j}` and write its complementary ports as `{k,l}`.  Choose
an active colour `s`, and let `r` be the other active colour.

### Lemma 4 (double-flip diagonal exclusion)

Every hypothetical witness on (5) satisfies

```text
W_(r_i,r_j)(e_(i,s),e_(j,s))=0                       (9)
```

for all six root pairs and both active colours.

### Proof

Use one of the two `GLD21` dense packages with port colours

```text
(u_i,u_j,u_k,u_l)=(r,r,s,a),                          (10)
```

and inspect the root word

```text
(r_i,r_j,r_k,r_l)=(s,s,s,a).                          (11)
```

The target coefficient is mixed and therefore zero.  Relative to (10), the
root word (11) differs at both repeated positions `i,j`.  Lemma 2 shows that
neither `G_U` nor any one-`Q` nuisance companion can reach it: those columns
allow zero or one changed root position only.

The unique surviving dense label is `I=Q union {u_i,u_j}`.  Its outside
coefficient is the nonzero `K_ij(r,r)`.  Its companion pairs `r_i,r_j`
internally and sends `r_k,r_l` through their private edges, so the coefficient
equation is

```text
K_ij(r,r) tau_k^s tau_l^a
  W_(r_i,r_j)(e_(i,s),e_(j,s))=0.                    (12)
```

All three scalar factors preceding the root--root entry are nonzero by
(2) and (4), proving (9).  Swapping the two complementary ports gives the
same conclusion.  `square`

This is the first place where the same-graph grade-one companion is used.
An arbitrary formal assignment of companion columns has no root--root entry
whose value is shared between the two repeated-colour packages.

## 5. The mixed private word is impossible

### Theorem 5 (dense private-cross-matching exclusion)

The `h!=0` dense `K_4/K_4` residue contains no hypothetical witness whose
root-to-port array satisfies Definition 1.

### Proof

Keep `e={i,j}`, complement `{k,l}`, and active colours `s,r`.  Evaluate the
complete same-graph equation on the matching port and root word

```text
(u_i,u_j,u_k,u_l)=(s,s,r,a),
(r_i,r_j,r_k,r_l)=(s,s,r,a).                          (13)
```

This is a mixed GHZ coefficient, so its target is zero.  Put

```text
P=tau_i^s tau_j^s tau_k^r tau_l^a!=0.                (14)
```

The dense ledger and Lemma 2 give all contributions:

- `H_Q G_U` contributes `hP`;
- the one-`Q` pair at each of `i,j,k` contributes `-hP` by Lemma 3;
- the one-`Q` pair at the dead port `l` vanishes by `x_l^a=y_l^a=0`;
- the residual-present pair label on `e` contributes
  `K_ij(s,s) tau_k^r tau_l^a W_(r_i,r_j)(s,s)`, which
  vanishes by Lemma 4;
- every other label vanishes by the dense `GLD21` ledger.

Therefore the supposedly zero target coefficient equals

```text
hP-hP-hP-hP=-2hP.                                    (15)
```

Characteristic zero, `h!=0`, and (14) make (15) nonzero, a contradiction.
`square`

Only one edge and one orientation are needed after Lemma 4.  Running the
argument over all edges and both repeated active colours gives twelve
equivalent predetermined mixed detectors.

## 6. Sharpness and exact boundary

1. **Private missing-colour data alone are insufficient.**  `GLD21` already
   constructs the forced pure `G_U(a^4)` slice using one private matching in
   the dead colour.  The present proof also needs the same private matching
   in both active colours to factor the Hamming-one and `2+1+1` companions.
2. **Hamming-one equations alone are insufficient.**  Take private diagonal
   root--port blocks, `h!=0`, dense shores
   `v_i^c=(1,1)`, `v_i^d=(1,-1)`, `v_i^a=0`, no direct or root--root blocks,
   and choose the root--residual covectors so that (8) holds.  The pure dead
   slice and all eight dense Hamming-one equations hold.  The matching
   `2+1+1` coefficient is exactly `-2hP` and excludes the control.
3. **The opposite package is load-bearing.**  Without Lemma 4, the active
   diagonal root--root entry in the final package could cancel (15).  The
   package with the other repeated colour is what forces that same graph
   entry to zero.
4. **A common matching is load-bearing.**  If the private root--port
   permutation depends on colour, a one-`Q` companion need not be localized
   to one root position relative to the mixed word.  This theorem makes no
   claim about that residual.
5. **Formal companion arrays remain insufficient.**  The abstract solution
   `G_U=J_Q/h`, `G_D=0` for `D!=U` has no shared private root--port and
   root--root edge data.  It is outside the hypothesis, exactly as required
   by the `GLD21` integrability boundary.

## 7. Exact frontier and scope ledger

```text
GLD21 dense h!=0 companion normal form:                 INPUT;
common private matching in all three colours:          ASSUMED;
active Hamming-one effective covectors:                 FIXED;
all twelve active root--root diagonal entries:          ZERO;
matching dense 2+1+1 coefficient:                      -2hP;
common private colour-diagonal integrability subcell:    EMPTY;
colour-dependent private permutations:                UNKNOWN;
nonprivate root-to-port arrays:                        UNKNOWN;
proper-secondary-clique h!=0 cells:                    UNKNOWN;
other F=empty / pure-absorption cells:                 UNKNOWN;
weighted permanent implication:                       UNKNOWN;
global Krenn--Gu conjecture:                        UNRESOLVED.
```

Scope:

- **field:** characteristic zero;
- **breadth:** one fixed graph, residual pair, fully supported contraction,
  four roots, and one four-port window;
- **response hypothesis:** the dense `K_4/K_4` literal all-seven
  response-map-zero cell of `GLD21`;
- **root-to-port subcell:** one common private bijection, diagonal in all
  three GHZ colours, with twelve nonzero scalars;
- **same-graph input:** the same root--root coefficient occurs in the two
  opposite repeated-colour packages;
- **excluded object:** the complete private colour-diagonal subcell, not the
  whole dense cell;
- **permanent implication:** none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_private_cross_matching_root_companion_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_dense_private_cross_matching_root_companion_exclusion.py
```

The primary exact replay uses SymPy and a direct ten-vertex
perfect-matching expansion.  It checks the common-private companion support,
all eight Hamming-one tensors, every edge/active-colour double-flip
coefficient, and all twenty-four oriented matching `2+1+1` coefficients with
arbitrary symbolic private scalars on a canonical package and exact rational
specializations on the full orbit.

The independent audit imports neither SymPy nor the primary.  It uses
standard-library `Fraction`, a separately written recursive matching sum,
different nonzero private scalars, and all six edges, two active colours, and
two orientations.  The programs audit the coefficient ledger and sign.  The
arbitrary-field cancellation of a nonzero decomposable common factor and the
use of the already-proved `GLD21` dense label exhaustion remain the
load-bearing written proof.
