# Tricolour incidence quotients and the projective-support theorem

## Status

**Exact arbitrary-graph theorem with a sharp abstract boundary.**  Three
prescribed degree-five faces couple the three colour pairs separately.  The
one-edge incidence quotient therefore forces all three diagonal pair tensors
onto one line at every pair of core modes.  A projective-support argument then
shows that at most three of the seven quotient modes can retain rank at least
two.  Equivalently, at least four terminal-incidence spans meet the
three-colour diagonal space in dimension at least two.

This is a stronger necessary condition than the binary quotient dichotomy.
An exact quotient model attains three rank-two modes, so the bound is sharp at
this layer.  The model is not asserted to lift to the full ledger.

No graph family, mixed word, alignment, or support is enumerated.

## 1. Three exact two-colour faces

Let `rho^2=21`, and let `Phi_S` be the terminal-Wick-deconvolved tensor on a
five-terminal face `S`.  Direct exact inversion of the formal `2+2+1` ledger
with the common terminal block gives

```text
Phi_1234a = (1+43rho/21)D_0 - 6D_1,
Phi_1235b = rho D_0 + 2(1+rho)/7 D_2,
Phi_1345b = rho D_1 + 2(1+rho)/7 D_2.                 (1)
```

All three faces are prescribed.  Every displayed coefficient is nonzero in
`Q(rho)`:

```text
N(1+43rho/21)=-1828/21,
N(rho)=-21,
N(2(1+rho)/7)=-80/49.                                 (2)
```

## 2. One-edge quotient on an arbitrary physical graph

At core mode `i`, put

```text
U_i=span{R_i,p : p in P} subset V_i^*,
Q_i=V_i^*/U_i,
x_i^c=pi_i(epsilon_i^c),             c=0,1,2.          (3)
```

For a five-face `S`, the deconvolved physical response is

```text
T_S=sum_(i<j) A_ij tensor Per(R_(Z\{i,j}),S).          (4)
```

Projecting modes `i,j` to `Q_i tensor Q_j` kills every summand except the one
using core edge `A_ij`.  Its flattening across `{i,j}|Z\{i,j}` has rank at
most one.

The three right-hand diagonal tensors

```text
tensor_(k notin {i,j}) epsilon_k^c,       c=0,1,2,     (5)
```

are linearly independent.  Applying the rank-one statement to the three
faces in (1), and using (2), gives pairwise dependence of

```text
t_ij^c=x_i^c tensor x_j^c,                c=0,1,2.     (6)
```

Thus every physical realization must satisfy

```text
dim span{t_ij^0,t_ij^1,t_ij^2} <= 1
for every i<j.                                           (7)
```

The full terminal span in (3) is used only to make the same quotient valid
for all three faces.  Face-specific smaller quotients may be stronger.

## 3. The projective-support translation

For each mode define its colour support and its independent colour pairs:

```text
S_i={c : x_i^c!=0},
I_i={{c,d} subset S_i : x_i^c,x_i^d are independent}. (8)
```

### Lemma 1 (projective-support criterion)

Condition (7) holds if and only if, for every two distinct modes `i,j`,

```text
I_i intersect binom(S_j,2) is empty.                   (9)
```

Proof.  If `{c,d}` belongs to the intersection in (9), then both tensors
`t_ij^c,t_ij^d` are nonzero, but their first factors are independent.  Two
nonzero decomposable tensors can be proportional only when their factors in
each mode are proportional, so (7) fails.

Conversely, if (7) fails, some nonzero `t_ij^c,t_ij^d` are independent.
Both colours lie in `S_i intersect S_j`.  If the local factors were
proportional at both modes, their tensor products would be proportional.
Hence `{c,d}` belongs to `I_i` or to `I_j`, contradicting (9) in one of the
two orders.

This criterion retains support and projective direction, but no coordinates.

## 4. At most three high-rank modes

### Theorem 2 (tricolour quotient rank bound)

For any number of modes satisfying (7), at most three maps

```text
q_i:E_i=<epsilon_i^0,epsilon_i^1,epsilon_i^2> -> Q_i  (10)
```

have rank at least two.

Proof.  If `rank q_i>=2`, then `I_i` is nonempty; choose one colour pair
`e_i in I_i`.  For distinct high-rank modes `i,j`, the chosen pairs cannot
coincide: if `e_i=e_j`, then `e_i subset S_j`, contradicting (9).  The map
`i -> e_i` injects the high-rank modes into the three two-subsets of
`{0,1,2}`.

For seven cores, at least four modes therefore have `rank q_i<=1`.  Since
`E_i` has dimension three and

```text
ker q_i=E_i intersect U_i,                              (11)
```

the incidence consequence is

```text
dim(E_i intersect U_i)>=2
at at least four of the seven core modes.               (12)
```

### Corollary 3 (one rank-three mode)

If one mode `g` has rank three, then every other mode supports at most one
of the three quotient colour images.

Indeed, `I_g` consists of all three colour pairs, so (9) forces
`|S_j|<=1` for `j!=g`.  Thus every other incidence span contains at least two
of the three pure colour axes.

## 5. Sharp quotient models

The constant three in Theorem 2 is exact.  Take three modes

```text
mode 01: (x^0,x^1,x^2)=(e_0,e_1,0),
mode 12: (x^0,x^1,x^2)=(0,e_0,e_1),
mode 02: (x^0,x^1,x^2)=(e_0,0,e_1).                    (13)
```

Each has rank two.  Their pairwise colour-support intersections are the
singletons `1,0,2`, respectively.  Give each remaining mode support on only
one colour.  Then every pair in (7) has at most one nonzero tensor, so (7)
holds.

The rank-three corollary is also sharp at the quotient level: take one mode
with the three standard basis vectors and make each other mode support a
single colour.

These models prove that (12) cannot be strengthened using only the three
full-incidence quotient ranks.

## 6. New symbolic frontier

The three-colour diagonal has now been reduced to a projective support
hypergraph.  There are two natural next moves.

1. Replace `U_i` by the smaller five-terminal spans belonging to the three
   faces in (1), then glue the overlapping quotient kernels.
2. Combine the at-least-four codimension-two intersections (12) with the pure
   permanent and degree-one/degree-three equations.

Either route must distinguish actual incidence covectors from abstract
quotient data.  The sharp model (13) rules out a stronger rank count with no
additional equations.

## Scope wall

Proved:

- the exact three-face identities (1);
- the universal tricolour pair condition (7) for arbitrary physical `A,R`;
- the projective-support criterion (9);
- at most three high-rank quotient modes, hence the four-mode incidence
  intersection law (12);
- sharp abstract quotient models.

Not proved:

- that either sharp quotient model lifts to the formal ledger;
- a contradiction on the four forced codimension-two incidence modes;
- compatibility across the smaller face-specific quotients;
- the `P_7 -> Delta_3` restriction or the global Krenn--Gu conjecture.

```text
three prescribed colour-pair faces: EXACT;
all 21 tricolour quotient ranks:    AT MOST ONE;
high-rank quotient modes:           AT MOST THREE, SHARP;
full physical common core:          UNRESOLVED.         (14)
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_221_tricolour_incidence_quotient_projective_support.py
python claims/p7/audit_p7_221_tricolour_incidence_quotient_projective_support.py
python -m py_compile claims/p7/verify_p7_221_tricolour_incidence_quotient_projective_support.py claims/p7/audit_p7_221_tricolour_incidence_quotient_projective_support.py
uv run --with ruff ruff check claims/p7/verify_p7_221_tricolour_incidence_quotient_projective_support.py claims/p7/audit_p7_221_tricolour_incidence_quotient_projective_support.py
```

The primary replay reconstructs (1) from the formal ledger and checks the
projective-support models.  The independent replay uses hand-written
`Q(sqrt(21))` arithmetic and a separate tensor-rank routine.  No replay
searches graphs, words, alignments, supports, or parameters.
