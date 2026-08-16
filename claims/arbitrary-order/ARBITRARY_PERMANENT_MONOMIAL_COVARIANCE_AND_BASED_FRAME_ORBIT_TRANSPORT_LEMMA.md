# Arbitrary permanent monomial covariance and based-frame orbit transport

## Status

This note proves the exact covariance lemma needed to transport a
`P_r -> Delta_3` extension, or its nonexistence, through the equivalences
used by the based-frame orbit classification.

The allowed operations are:

1. one common coordinate permutation and nonzero coordinate scaling in
   every source mode;
2. one common permutation of the three target colours;
3. independent nonzero rescaling of the three colour vectors in either of
   the two displayed source modes; and
4. exchange of those two source modes.

The permanent tensor is symmetric in its source modes and is a relative
invariant for the coordinate monomial group.  Therefore exact extendibility
is constant on every based-frame orbit, including the larger orbit relation
that permits exchange of the two omitted modes.

Combining this lemma with the reviewed equality-five support synthesis,
based-frame classification, and the three displayed-frame full-extension
exclusions gives the following exact characteristic-zero residual list:

```text
pure star (4,1), representative 014;
fixed (4,2), e=1, representative 025;
fixed (4,2), e=2, representative 024.
```

These are **open extension-exclusion obligations**, not extensions and not
counterexamples.  No result for the dimension-at-least-six co-two sensor
residual is proved here.  Unrestricted `P_6 -> Delta_3`, arbitrary-order
permanent nonrestriction, and the global Krenn--Gu conjecture remain
**UNKNOWN/UNRESOLVED**.

## 1. Exact extension predicate

Let `K` be a field, let `r>=2`, and write a vector of `K^r` as

```text
z=(z_0,...,z_(r-1)).
```

Use the unnormalized permanent tensor

```text
P_r(z^(0),...,z^(r-1))
  = sum_(tau in S_r) product_(t=0)^(r-1) z^(t)_(tau(t)).     (1)
```

It is the complete polarization of `x_0...x_(r-1)` up to the harmless
conventional polarization scalar.

For every source mode `t`, let

```text
z^(t)_0, z^(t)_1, z^(t)_2 in K^r                         (2)
```

be linearly independent.  The resulting coefficient tensor is

```text
C_(c_0,...,c_(r-1))
  =P_r(z^(0)_(c_0),...,z^(r-1)_(c_(r-1))).                (3)
```

The local triples give an exact weighted `Delta_3` restriction when there
are `lambda_0,lambda_1,lambda_2 in K^*` such that

```text
C_(c_0,...,c_(r-1))
  =lambda_c,  if c_0=...=c_(r-1)=c;
  =0,         otherwise.                                  (4)
```

An ordered based pair `(u,v)` is **extendible** when it can be used for the
first two triples in (2) and completed by triples in the other `r-2` modes
satisfying (4).

## 2. The coordinate monomial character

Choose `pi in S_r` and `d_0,...,d_(r-1) in K^*`.  Define the coordinate
monomial map `g` by

```text
(g z)_(pi(i))=d_i z_i,                    0<=i<r,          (5)
```

and put

```text
chi(g)=product_(i=0)^(r-1) d_i in K^*.                    (6)
```

### Lemma 1 (permanent monomial covariance)

For arbitrary `z^(0),...,z^(r-1) in K^r`,

```text
P_r(g z^(0),...,g z^(r-1))
  =chi(g) P_r(z^(0),...,z^(r-1)).                          (7)
```

### Proof

In a summand on the left, write `tau(t)=pi(rho(t))`.  As `tau` runs through
`S_r`, so does `rho=pi^(-1) tau`.  Equation (5) gives

```text
product_t (g z^(t))_(tau(t))
  =product_t d_(rho(t)) z^(t)_(rho(t))
  =chi(g) product_t z^(t)_(rho(t)),                        (8)
```

because `rho` uses every coordinate exactly once.  Summing (8) proves (7).
There is no determinant sign: coordinate permutation preserves the
permanent tensor.  `square`

### Complementary-form version

For `r=6`, let `q` be a square-free quadratic and define

```text
star(q)=sum_(i<j) q_ij product_(k notin {i,j}) x_k.         (9)
```

If `q=uv`, complete polarization gives

```text
pol(star(uv))(y_2,y_3,y_4,y_5)
  =P_6(u,v,y_2,y_3,y_4,y_5).                              (10)
```

Consequently Lemma 1 is exactly the quartic covariance identity

```text
pol(star((g u)(g v)))(g y_2,g y_3,g y_4,g y_5)
  =chi(g) pol(star(uv))(y_2,y_3,y_4,y_5).                  (11)
```

Thus the complementary quartics used by the fixed, star, and triangle
packages need not be compared term by term after a frame move.  Their full
polarizations transport together by the one nonzero scalar `chi(g)`.

## 3. Based-frame orbit transport

Let

```text
u=(u_0,u_1,u_2),                 v=(v_0,v_1,v_2)           (12)
```

be ordered independent triples in `K^r`.  Choose `sigma in S_3` and
nonzero scalars `a_c,b_c`.

There are two relevant forms of based-frame equivalence.  The ordered-mode
form is

```text
u'_c=a_c g u_(sigma(c)),          v'_c=b_c g v_(sigma(c)),  (13)
```

and the omitted-mode-exchange form is

```text
u'_c=a_c g v_(sigma(c)),          v'_c=b_c g u_(sigma(c)).  (14)
```

### Theorem 2 (based-frame orbit transport)

The pair `(u,v)` is extendible if and only if `(u',v')` is extendible for
either (13) or (14).  Hence nonextendibility also transports in both
directions.

### Proof for the ordered-mode form

Suppose `(u,v)` has completing triples `z^(t)` for `2<=t<r`.  Define

```text
z'^(t)_c=g z^(t)_(sigma(c)),              2<=t<r.          (15)
```

All local triples stay independent.  Lemma 1 gives, for every colour word,

```text
C'_(c_0,...,c_(r-1))
 =a_(c_0)b_(c_1)chi(g)
  C_(sigma(c_0),...,sigma(c_(r-1))).                      (16)
```

The word on the right is constant exactly when the word on the left is
constant.  Therefore all mixed target entries stay zero, while

```text
lambda'_c=a_c b_c chi(g) lambda_(sigma(c)) !=0.            (17)
```

So (15) completes `(u',v')`.

Conversely, (13) can be inverted using `g^(-1)`, `sigma^(-1)`, and nonzero
colour rescalings.  The same argument transports any completion back.

### Proof for omitted-mode exchange

Use (15) again.  Symmetry of (1) in its first two slots gives

```text
C'_(c_0,...,c_(r-1))
 =a_(c_0)b_(c_1)chi(g)
  C_(sigma(c_1),sigma(c_0),sigma(c_2),...,sigma(c_(r-1))). (18)
```

Swapping the first two entries cannot change whether a word is constant.
Equation (17) therefore remains the diagonal target, and all mixed words
remain zero.  The operation is invertible, proving the converse. `square`

## 4. Exact equality-five consequence

The following frozen, hostile-reviewed inputs are used only for this
corollary; Lemma 1 and Theorem 2 do not depend on them.

```text
843b4f459790b88499646e7dd79c8280633d622e
  equality-five active-support orbit synthesis

dc6eca42605086fbffba4059f87f4702e68c9a54
  co-two r=4 based-frame orbit classification

2e6c74d36fda60d6b3428047325c5398053b247c
  displayed triangle-pair full-extension exclusion

3a53f19a789baa055c3b951efdacc505b2a69117
  displayed star-pair full-extension exclusion

82ab1090076bcd765c89b463214eb7714618722e
  displayed fixed-pair full-extension exclusion.           (19)
```

The support synthesis says that an equality-five omitted pair in an actual
restriction has active support four and one of the three unbased types
`(3,1)`, `(4,1)`, `(4,2)`.  The based-frame classification gives the exact
ordered-orbit representatives

```text
(3,1): 012;

(4,1): 014 (k=3), 013 (k=2), 025 (k=1), 235 (k=0);

(4,2): 013 (e=0), 025 (e=1), 024 (e=2).                    (20)
```

When the two omitted modes may be exchanged, the `(4,1)` invariant changes
by `k -> 3-k`, whereas the `(4,2)` invariant `e` is fixed.  Theorem 2 proves
that this optional quotient is legitimate for full extensions, not only at
the pair level.

The displayed exclusion theorems rule out `(3,1):012`, `(4,1):013`, and
`(4,2):013`.  Transport inside the ordered stabilizer orbits and through
omitted-mode exchange therefore gives

```text
all based (3,1) frames:                                  EXCLUDED;
(4,1) mixed frames k=1,2:                               EXCLUDED;
(4,2) e=0 frames:                                       EXCLUDED;

remaining pure (4,1) orbit k=0,3:                       REPRESENTATIVE 014;
remaining (4,2) orbit e=1:                              REPRESENTATIVE 025;
remaining (4,2) orbit e=2:                              REPRESENTATIVE 024. (21)
```

The word `remaining` in (21) means not excluded by the frozen inputs plus
transport.  It does not mean feasible, extendible, or realized.

## 5. Exact boundary

```text
permanent covariance under a common coordinate monomial map: PROVED;
common colour permutation and first-two-mode colour scaling: PROVED;
transport through exchange of the first two source modes:    PROVED;
extendibility constant on the classified based-frame orbits: PROVED;

equality-five residual representatives after frozen
  displayed-frame exclusions:                               014,025,024;

nonextension of residual 014:                               NOT PROVED HERE;
nonextension of residual 025:                               NOT PROVED HERE;
nonextension of residual 024:                               NOT PROVED HERE;
dimension-at-least-six co-two sensor residual:               NOT ADDRESSED;
unrestricted P_6 -> Delta_3:                                UNKNOWN;
global Krenn--Gu conjecture:                                UNRESOLVED. (22)
```

## Replay

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_monomial_covariance_and_based_frame_orbit_transport.py
python claims/arbitrary-order/audit_arbitrary_permanent_monomial_covariance_and_based_frame_orbit_transport.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_monomial_covariance_and_based_frame_orbit_transport.py claims/arbitrary-order/audit_arbitrary_permanent_monomial_covariance_and_based_frame_orbit_transport.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_monomial_covariance_and_based_frame_orbit_transport.py claims/arbitrary-order/audit_arbitrary_permanent_monomial_covariance_and_based_frame_orbit_transport.py
```

The primary verifier checks (7) and (11) as symbolic polynomial identities,
exhausts all `3^6` colour words in (16) and (18), and replays the residual
orbit bookkeeping in (20)--(21).  The independent audit imports neither the
primary nor SymPy.  It proves the monomial reindexing combinatorially over all
`6!` coordinate assignments, checks the complementary-form indexing over all
quadratic/complement assignments, and evaluates a separate exact rational
six-mode fixture by a dynamic-programming permanent.
