# The degree-five rectangle obstructs every alignment of the fixed colour-0/colour-2 charts

## Status

**Exact arbitrary-alignment obstruction for the two fixed scalar charts.**
Keep the colour-0 and colour-2 scalar certificates from
`P7_221_COMMON_TERMINAL_BLOCK_SCALAR_HAFNIAN_REALIZABILITY.md`, but identify
their seven core vertices by an arbitrary bijection.  Keep every same-colour
core edge and every core--terminal row fixed, and allow every cross-colour
core edge to be an arbitrary scalar.

For every such bijection there is a mixed `0/2` core word for which the same
four prescribed degree-five faces

```text
125ab, 145ab, 235ab, 345ab                              (1)
```

have an off-diagonal-independent alternating response

```text
Phi_125ab-Phi_145ab-Phi_235ab+Phi_345ab != 0.           (2)
```

The word is constructed symbolically from the alignment; no permutation,
word, face, support, or parameter family is enumerated.  Thus **no alignment
of these fixed colour-0/colour-2 charts admits a cross-core completion to the
formal tensor ledger**.  The result does not address different scalar
realizations of the pure ledgers.

## 1. The rectangle transform

Put `rho^2=21` and order the terminal columns as

```text
(1,2,3,4,5,a,b).
```

The alternating functional in (2) is exactly the permanent after the column
transform

```text
A = column(1)-column(3),
B = column(2)-column(4),
F = (A,B,5,a,b).                                        (3)
```

Indeed, multilinearity in the first two columns gives

```text
per(A,B,5,a,b)
 =per(1,2,5,a,b)-per(1,4,5,a,b)
  -per(3,2,5,a,b)+per(3,4,5,a,b).                       (4)
```

Write

```text
tau  = -5-2 rho/21,
C    = 230+104 rho/7,
beta = 1+16 rho/21.                                     (5)
```

In the transformed columns (3), the seven colour-0 rows are

```text
f1  = ( 1, 0,0,0,0),       f2 = (0, 1,0,0,0),
ell = (-1, 0,1,1,0),       h3 = (-1,0,0,0,-rho),
h4  = ( 0,-1,0,0,tau),     h5 = (0,0,1,0,C),
ha  = ( 0, 0,0,1,beta).                                 (6)
```

The colour-2 rows become

```text
z_* = (1/7)e_5,
z_3 = e_a,
z_4 = e_b,
z_1=z_2=z_5=z_6=0.                                     (7)
```

The two pairs of zero rows are also fixed nonzero colour-2 edges:

```text
z_1 z_2 has weight 1,       z_5 z_6 has weight rho.     (8)
```

This simultaneous zero-row/fixed-edge structure is the selector mechanism.

## 2. The alignment-adapted mixed words

Use the colour-0 labels in (6) as the physical core set `Z`.  Let `pi` be an
arbitrary bijection from the colour-2 core labels to `Z`, and put

```text
P={pi(z_1),pi(z_2)},        Q={pi(z_5),pi(z_6)},
r_5=pi(z_*),                r_a=pi(z_3),
r_b=pi(z_4),                R={r_5,r_a,r_b}.             (9)
```

Thus `P,Q,R` partition `Z`.  Choose one of the two zero-row pairs as a
colour-2 fixed edge `E`, let `O` be the other pair, and choose any

```text
T subset {5,a,b}.                                        (10)
```

The mixed word `sigma_(E,T)` assigns colour 2 precisely at

```text
E union {r_t:t in T}                                    (11)
```

and assigns colour 0 everywhere else.  It is mixed for every `T`, because
`E` has two vertices while the other zero-row pair `O` remains colour 0.

Let `L_0` be the `7 x 5` matrix (6), and define the anchored minor

```text
m_(O,T)=per L_0[O union {r_t:t notin T}, F minus T].     (12)
```

Both its row and column sets have size `5-|T|`.  The degree-five one-edge
Laplace formula shows that (2), evaluated at `sigma_(E,T)`, is

```text
w_E 7^(-1_(5 in T)) m_(O,T),                            (13)
```

where `w_E` is `1` or `rho` according to (8).

To see why (13) contains no hidden terms, note the following.

- Deleting the endpoints of a cross-colour edge removes at most one of the
  two zero rows in `E`; the other zero row kills its permanent.
- Deleting a colour-0 edge removes no row in `E`, so both zero rows remain.
- If `r_a,r_b` are both colour 2, their fixed edge removes those two rows but
  leaves both zero rows in `E`.
- The other zero-row edge `O` is colour 0 in the word (11).
- Only the fixed edge `E` removes both zero rows.  Its remaining colour-2
  basis rows factor out and leave exactly (12).

Therefore every cross-colour core entry cancels, and (13) isolates one fixed
monochromatic edge.

## 3. The anchored-minor lemma

Partition the colour-0 rows by their `B` coordinate:

```text
Y={f2,h4},
H={f1,ell,h3,h5,ha}.                                    (14)
```

Rows in `H` have zero `B` coordinate; `f2` and `h4` have `B` coordinates
`1` and `-1`.

### Lemma 1

For every partition (9), at least one of

```text
{m_(P,T):T subset {5,a,b}},
{m_(Q,T):T subset {5,a,b}}                              (15)
```

contains a nonzero element.

### Proof

First consider the full minor `m_(O,emptyset)` on the five-row set
`K=O union R`.

If `K` contains exactly one row of `Y`, expansion down the unique nonzero
entry of column `B` reduces to one of the following four-column permanents,
up to sign.  The table is indexed by the omitted row of `H`:

```text
omitted f1:  -231-307 rho/21,
omitted ell: -rho,
omitted h3:   231+328 rho/21,
omitted h5:  -rho,
omitted ha:  -rho.                                     (16)
```

All five values are nonzero in `Q(rho)`.

If `K` contains both rows of `Y`, write `K=Y union J` with
`J subset H`, `|J|=3`.  Direct expansion of the sparse rows (6) gives

```text
m_(O,emptyset)=0  iff  {f1,h3} subset J;                (17)
```

in the other seven cases its value is `tau` or `-tau`.  Here `tau != 0`
because the quadratic norm of `5+2 rho/21` is `521/21`.

Now let `y=|R intersect Y|`.

- If `y=1`, the remaining row of `Y` lies in exactly one of `P,Q`; the other
  pair gives a five-row set with exactly one `Y` row, so (16) applies.
- If `y=2`, write `R=Y union {q}` with `q in H`.  The pairs `P,Q` partition
  `H minus {q}`.  If both full minors vanished, (17) would force both
  `P union {q}` and `Q union {q}` to contain `f1,h3`, impossible because
  `P,Q` are disjoint.
- Suppose `y=0`.  If `f2,h4` lie in different pairs, both full minors have
  exactly one `Y` row.  If they lie together, say `P=Y`, then
  `Q union R=H`.  The full minor for `O=P` is nonzero by (17) unless

  ```text
  R={f1,h3,q},       q in {ell,h5,ha}.                  (18)
  ```

  In the exceptional case, expand an anchored minor first through the only
  nonzero entry of row `f2`, namely `B`, and then through the `b` entry
  `tau` of `h4`.  If the row `r_b` has nonzero `A` coordinate, then

  ```text
  m_(Y,{5,a})=tau A(r_b) != 0.                          (19)
  ```

  The only remaining possibilities are `r_b=h5` or `r_b=ha`.  If
  `r_b=h5`, the row `r_5` is `f1` or `h3` and

  ```text
  m_(Y,{a})=tau A(r_5) != 0.                            (20)
  ```

  If `r_b=ha`, the row `r_a` is `f1` or `h3` and

  ```text
  m_(Y,{5})=tau A(r_a) != 0.                            (21)
  ```

These cases exhaust `y=0,1,2` and prove the lemma.  Notice that the proof
uses only the two row types in (14), the sparse table (6), and the partition
`P+Q+R`; it never lists the possible bijections `pi`.

## 4. The obstruction theorem

### Theorem 2 (arbitrary-alignment fixed-chart obstruction)

For every bijection between the cores of the fixed colour-0 and colour-2
scalar certificates, no assignment of the cross-colour core--core entries
realizes the formal `2+2+1` tensor cofactor ledger.

### Proof

Lemma 1 supplies `O,T` with `m_(O,T) != 0`; choose as `E` the other zero-row
pair and use the mixed word (11).  Equation (13) then makes the circuit (2)
nonzero, independently of every cross-colour core entry.

On the formal tensor ledger, the coefficient at every mixed core word is
zero on every prescribed cofactor face.  For each five-set in (1), its
Wick-deconvolved coefficient is a linear combination of full cofactor
coefficients on surviving terminal sets of sizes `5,3,1`.  Their complements
have sizes `2,4,6`, so all of them are prescribed faces and all have zero
coefficient at the mixed word (11).  Consequently each of the four `Phi`
values in (2) would have to be zero.  This contradicts (13).

## Scope wall

Proved:

- one fixed four-face rectangle suffices for every core alignment of the
  current colour-0 and colour-2 scalar charts;
- the mixed word is constructed from the alignment by (9)--(11);
- arbitrary cross-colour core edges cannot repair the charts.

Not proved:

- an obstruction for a different scalar realization of either pure ledger;
- an arbitrary-alignment statement involving the colour-1 chart is needed
  (the colour-0/colour-2 subproblem already obstructs the three-chart lift);
- a universal tensor-valued `P_7` obstruction;
- the `P_7 -> Delta_3` restriction or the Krenn--Gu conjecture.

The exact boundary is

```text
fixed c0/c2 charts, indexwise alignment:       EXCLUDED (earlier circuit);
fixed c0/c2 charts, every core alignment:      EXCLUDED (this theorem);
other pure scalar lifts:                       UNKNOWN;
global Krenn--Gu:                              UNRESOLVED.              (22)
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_221_arbitrary_alignment_degree5_rectangle_obstruction.py
python claims/p7/audit_p7_221_arbitrary_alignment_degree5_rectangle_obstruction.py
python -m py_compile claims/p7/verify_p7_221_arbitrary_alignment_degree5_rectangle_obstruction.py claims/p7/audit_p7_221_arbitrary_alignment_degree5_rectangle_obstruction.py
uv run --with ruff ruff check claims/p7/verify_p7_221_arbitrary_alignment_degree5_rectangle_obstruction.py claims/p7/audit_p7_221_arbitrary_alignment_degree5_rectangle_obstruction.py
```

The primary verifier reconstructs the transformed row tables, checks (16)--
(17), and checks the exceptional anchored identities (19)--(21) exactly in
`Q(rho)`.  The independent audit uses rational-pair arithmetic and a dynamic
permanent; it imports neither SymPy nor the primary verifier.  Neither replay
enumerates alignments, mixed words, or face rectangles.
