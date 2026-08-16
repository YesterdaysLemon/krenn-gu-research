# Hostile review of the co-two `r=4` fixed-`e=1` full-extension exclusion

## Verdict

**PASS, at the stated pointwise scope.**

The package proves that the displayed based `(4,2)`, `e=1` frame,
representative `025`, has no exact `P_6 -> Delta_3` extension over a field
of characteristic zero.  It uses the complete five-dimensional
pair-product target, proves rather than assumes a rank drop in both mixed
projection families, and closes every exceptional companion incidence
needed by one family.

This verdict does **not** close fixed `e=2` representative `024`, the
dimension-at-least-six co-two sensor residual, unrestricted
`P_6 -> Delta_3`, arbitrary-order permanent nonrestriction, or the global
Krenn--Gu conjecture.  The global status remains **UNRESOLVED**.

## Reviewed artifacts

Hashes are SHA-256 of LF-normalized text bytes.

```text
theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_COTWO_R4_FIXED_E1_FULL_EXTENSION_EXCLUSION_THEOREM.md
A7EE294986E79C7F1BC38E0B2CE0DC1A5EE09D230F2FD06796846D677A361ACF

primary:
claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_fixed_e1_full_extension_exclusion.py
24A84558C6D842BC5D034DFCC6494C60A03C75CF8E5F47E2E63A6C3CCFEED2F8

independent audit:
claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_fixed_e1_full_extension_exclusion.py
EF9CC36CBE0AD27DFEAFC1E24EE0A717CDE17E9E2FF6684FFC1981567585B4CC
```

The audit pins the theorem and primary hashes.  Both replays pin the exact
based-frame classification and the reviewed hyperplane-product and sharp
hyperplane-plane product interfaces.  Hash normalization makes the same Git
text blobs replay on LF and CRLF checkouts.

## 1. Claim and proof boundary

The exact input is

```text
U=(x_1-x_2, x_0-x_1, x_0-x_3),
V=(x_1+x_3, x_0-x_1, x_0+x_2).
```

Both replays multiply all nine pair products directly.  They obtain mixed
rank two and total product rank five, and check that the four remaining
off-diagonal products are signed copies of the two displayed mixed basis
vectors.  The two mixed zeros and three diagonal targets are therefore the
complete pair-product target, not a selected subsystem.

The conclusion is only nonextension of this based frame.  The based-frame
classification and orbit transport identify it as the fixed `e=1`
representative.  Nothing here transports the result to fixed `e=2` `024`.

## 2. Attacks on complementary cores and projection maps

### Attack: wrong edge-complement convention

The primary rebuilds the edge complement symbolically from set complements.
The audit uses a separate integer edge lookup.  Both derive

```text
g_(m_1)=x_3(x_0-x_1+x_2),
g_(m_2)=x_2(-x_0+x_1+x_3)
```

and all three diagonal cores.  Hence

```text
Phi_1=(x_3,h_1,x_4,x_5),
Phi_2=(x_2,h_2,x_4,x_5)
```

are consequences of the frame rather than guessed factor maps.

### Attack: a discarded product relation changes the target

Total product rank five equals mixed rank two plus the three independent
diagonal classes.  The proof keeps all five channels throughout.  No
certificate based on a smaller sensor family is promoted to this theorem.

## 3. Attacks on the kernel classification

The two ambient kernels are parameterized as

```text
p_1(a,b)=(a-b,a,b,0),             p_2(a,b)=(a+b,a,0,b).
```

The primary computes the contraction determinants

```text
-8ab^2(a-b),                      8ab^2(a+b).
```

The audit independently expands them in a custom bivariate polynomial ring
and obtains

```text
{-8a^2b^2+8ab^3},                 {8a^2b^2+8ab^3}.
```

Thus no generic projective root is hidden.  The exact exceptional lines are

```text
Phi_1: A=-x_0+x_2, B=x_1+x_2, N=x_0+x_1;
Phi_2: C= x_0+x_3, D=x_1-x_3, N=x_0+x_1.
```

Their contraction ranks are `3,3,3,3,2`, respectively, and both
implementations verify every displayed relation and annihilator.

### Attack: the incidence lemma assumes small support

It does not.  The quotient argument first handles arbitrary nonempty
support: if all other local planes miss `H_p`, the `D`-valued trilinear map
forces cross-colour orthogonality in the two-dimensional `x_4,x_5` factor.
The three-, two-, and one-colour possibilities are then eliminated using
the full diagonal target and local independence.  A distinct-mode companion
is obtained before disjoint support, and only then does a legal double
contraction imply support size at most two.  No vector is inserted twice in
two tensor slots.

The exceptional relations give the exact support bounds

```text
A,C subset {0,1};        B,D subset {1,2};        N subset {0,2}.
```

Over characteristic zero, an intersection plane cannot be a finite union of
three lines.  Every restricted projection therefore has rank at least two.

## 4. Attack on two-sided rank-drop existence

The endpoint does not assume a low mode.  Suppose all four `Phi_1` images
were hyperplanes.  The pinned hyperplane-product lemma gives one common
missing factor.  Missing `x_4` or `x_5` kills every sensor; missing `x_3`
kills `d_1`; hence all local planes lie in `ker(h_1)`.

Inside that hyperplane, the secondary kernel is exactly `K N`.  With zero
or one secondary low, the full-rank or hyperplane-plane equality argument
gives a common second factor.  The ordinary `x_2` cell has diagonal rank
two.  Both replays solve it exactly.

### Attack: the rank-three common cell was waved away

It was not.  On `ker(h_1) cap ker(h_2)`, use

```text
(x_0,x_1,x_2,x_3)=(s-t,s,t,-t).
```

The diagonal rows are

```text
(-1,3,-2),             (0,0,2),             (-1,-1,0)
```

in coefficients of `(s^2,st,t^2)`, and

```text
4g_(d_0)+3g_(d_1)+4g_(d_2)=-2(2s-t)^2.
```

All target weights are nonzero.  A putative common cell would identify the
pullback of `pol(X^2UV)` with a concise weighted `Delta_3`.  Its first-mode
cubic slice space is

```text
span{pol(XUV),X^2V,X^2U}.
```

Every member is divisible by `X`.  A nonzero symmetric rank-one member
would be `ell^3`; divisibility makes `ell` proportional to `X`, but `X^3`
is absent.  A concise rank-three four-tensor would put three decomposable
cubics in this slice space, so its rank is strictly greater than three.
The audit separately checks all nonzero linear forms over `F_5,F_7`; that
enumeration is stress evidence only, not the characteristic-zero proof.

### Attack: three or four common-kernel lows survive

At `N`, the double contractions are exactly

```text
(m_1,m_2,d_0,d_1,d_2)=(0,0,-2J,0,-2J).
```

Single contraction kills colour `1`.  For any two low modes, equality of
the `d_0,d_2` source forms against distinct diagonal target cells forces
same-colour coefficient products at colours `0,2` to vanish.  The lows are
therefore pairwise disjoint singletons in a two-element set, so there are at
most two.

Exactly two remain.  The pinned sharp `(3,3,2,2)` classification has a
common-coordinate branch, already excluded, and one cancellation branch.
Contracting the two low slots, supported at different colours, kills the
complete target and forces `J(H_+,H_-)=0`.  Two mutually orthogonal
hyperplanes for this rank-two form contain its two-dimensional radical;
their intersection plane is that radical.  Both low modes then lack
`x_4,x_5`, while the high modes have zero `J`-pairing, so every sensor
vanishes.  This contradicts the diagonal target.

The argument with the two projection families exchanged has the same `N`,
dangerous cell, and contraction identities.  The remaining ordinary cell
is the symmetric `x_3` cell of diagonal rank two.  Hence both projection
families contain a rank-two mode.

## 5. Attacks on companion exhaustiveness

For the four noncommon lines, both replays obtain

```text
H_A=K A',        H_B=K B',        H_C=K C',        H_D=K D'.
```

The exact relations at `A',B',C',D'` force the companion colours
`2,0,2,0`.  There is no unexamined direction in these one-dimensional
annihilators.

For `N`, every companion is

```text
q(u,v)=(-u,u,v,v).
```

The relation `B_(d_0)-B_(d_2)=0` forces colour `1`, so `d_1` must be a
coloop.  The primary takes the gcd of all nonzero deleted `3 x 3` minors:

```text
4u(u-v)(u+v).
```

The independent audit expands every deletion minor in its own polynomial
ring: exactly four are nonzero, each equal up to sign to this polynomial.
It also exhibits full-family minors `-8uv^2` and
`-4u(u^2-v^2)`.  Thus the full rank is three exactly for `u!=0`; at `u=0`
the deleted and full ranks are both two.  The only coloop directions are

```text
Q_+=(-1,1,1,1),                  Q_-=(-1,1,-1,-1),
```

both at colour `1`.  The six rows `A,A'`; `B,B'`; `C,C'`; `D,D'`;
`N,Q_+`; `N,Q_-` exhaust the finite incidence table.

## 6. Attacks on the terminal incidence exclusions

Only a `Phi_1` low is needed, so the load-bearing rows are

```text
(A,A'),                         (B,B'),                         (N,Q_+/-).
```

Both implementations verify a common nonzero contraction covector on each
low and companion shore.  The resulting identities are full three-slot
copies of `pol(ell*x_4*x_5)`, not scalar second-contraction surrogates.  Every
diagonal coefficient used on a live support is nonzero.

### Support-two attack

A two-colour low plus its singleton companion produces three independent
diagonal slices, hence a concise weighted `Delta_3` for `pol(XUV)`.  But its
first-mode slice space

```text
span{sym(UV),sym(XV),sym(XU)}
```

contains no nonzero rank-one matrix: the three principal minors of a general
slice are `-c^2,-b^2,-a^2`.  The no-import audit exhausts the same obstruction
over two odd finite fields only as a stress test.

### Singleton attack

The two live slices make the common-cubic slice rank two or three.  Rank
three kills the unused-colour evaluations on the low and companion shores.
At rank two, the exact contraction matrix

```text
[0 V U; V 0 X; U X 0]
```

has rank at least two for every nonzero `(X,U,V)`, so the corresponding
common annihilator has dimension at most one and the unused-colour
evaluations vanish on the two untouched shores.

The three terminal factor gates are checked coefficient by coefficient:

```text
g_(m_1)+g_(m_2)+g_(d_0)+g_(d_1)=-x_1(x_0-x_2+x_3),
g_(m_1)+g_(m_2)+g_(d_1)+g_(d_2)=-x_0(x_1+x_2-x_3),
-g_(d_0)+g_(d_2)=(x_0+x_1)(x_3-x_2).
```

Each is divisible by the applicable common `ell` and has nonzero coefficient
at every possible unused diagonal.  Polarization is zero on the relevant two
`ker(ell)` shores, whereas the target is a nonzero multiple of the unused
`lambda_t`.  This closes both slice-rank cases.

## 7. Independence assessment

The audit is genuinely implementation-independent at the practical level:

- it imports neither the primary verifier nor SymPy;
- it rebuilds all nine products and edge complements with integer tuples;
- it uses rational row reduction instead of symbolic matrices;
- it expands determinants in a custom bivariate polynomial dictionary;
- it checks every nonzero common-line deletion minor rather than trusting a
  reported gcd;
- it separately enumerates both slice obstructions over `F_5,F_7`.

The programs necessarily share the mathematical frame and expected claim.
They are not formal proofs, and finite-field stress tests are not used to
infer characteristic zero.  The written proof carries the theorem.

## 8. Scope ledger

```text
fixed e=1 based representative 025:                    EXCLUDED;
exceptional low lines A,B,C,D,N:                       CLASSIFIED;
all load-bearing Phi_1 incidences:                     EXCLUDED;

fixed e=2 representative 024:                          OPEN;
dimension-at-least-six co-two sensor residual:           OPEN;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

## Replay verdict

```text
primary exact replay:                                  PASS;
independent no-import audit:                           PASS;
Python compilation:                                    PASS;
Ruff:                                                  PASS;
hostile mathematical review:                           PASS.
```
