# Hostile review of the co-two `r=4` pure-star full-extension exclusion

## Verdict

**PASS, at the stated pointwise scope.**

The package proves that the displayed based `(4,1)`, `k=3` frame,
representative `014`, has no exact `P_6 -> Delta_3` extension over a field
of characteristic zero.  The proof uses the complete five-dimensional
pair-product target and closes every projection-kernel incidence exposed by
that frame.

This verdict does **not** close the fixed `(4,2)` representatives `025` or
`024`, the dimension-at-least-six co-two sensor residual, unrestricted
`P_6 -> Delta_3`, arbitrary-order permanent nonrestriction, or the global
Krenn--Gu conjecture.  The global status remains **UNRESOLVED**.

## Reviewed artifacts

Hashes are SHA-256 of LF-normalized text bytes.

```text
theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_COTWO_R4_PURE_STAR_FULL_EXTENSION_EXCLUSION_THEOREM.md
E0B069B11107F006650954D339EF8E6E9465C2B492059450236F5238B2567CBC

primary:
claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_pure_star_full_extension_exclusion.py
36C285C44BFA4D4C61FC084773F1604E398EBAC94E1AA8FD72E6BF5A8E1E6D49

independent audit:
claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_pure_star_full_extension_exclusion.py
4FCFBF910701EB28C1913AB9FC39A6921C689C536EE12F42CADF6A35B0B51163
```

The audit pins the theorem and primary hashes.  Both replays pin the exact
based-frame classification and the reviewed hyperplane-product predecessor.
The hash normalization is deliberate: the same Git text blobs replay on LF
and CRLF checkouts.

## 1. Claim and proof boundary

The exact input is the based frame

```text
U=(x_0-x_1, x_0-x_3, x_0-x_2),

V=(x_0-x_1+x_2+x_3,
   x_0+x_1+x_2-x_3,
   x_0+x_1-x_2+x_3).
```

The package does not infer this frame from a filename or from the unbased
star orbit.  Both replays multiply the nine pair products directly and
obtain mixed-product rank two and total product rank five.  They also check
that the four off-diagonal products lie in the displayed mixed plane.
Consequently the two mixed zero targets and three diagonal targets form the
complete pair-product target.

The conclusion is nonextension of this based frame.  Orbit transport was
proved separately and identifies `014` as the sole remaining pure-star
representative after the displayed mixed-star frame was excluded.  No step
in this package transports the result to a different unproved based orbit.

## 2. Attacks on the complementary cores

### Attack: wrong edge-complement convention

The source products and the five complementary quadratic cores are rebuilt
from the six edge coordinates.  The primary uses symbolic square-free
arithmetic and a set-complement map.  The audit uses separate integer
arithmetic and its own edge lookup.  Both obtain

```text
g_(m_1)=(x_0-x_1)(x_2-x_3),
g_(m_2)=-(x_0-x_3)(x_1-x_2)
```

and the same three diagonal cores.  Thus the two four-factor projection
maps are derived rather than assumed.

### Attack: selected sensors rather than the full target

The total product rank is five, the mixed plane has rank two, and the three
diagonal classes complete it.  A relation discarded from the five displayed
channels would therefore change the target.  No such discard occurs.

## 3. Attacks on the kernel classification

The two ambient kernels are parameterized independently as

```text
p_1(a,b)=(a,a,b,b),             p_2(a,b)=(a,b,b,a).
```

For each family, the nonzero mixed contraction and the three diagonal
contractions have determinant

```text
-64 a^2 b(a-b).
```

The primary derives this with a computer-algebra determinant.  The audit
uses a custom bivariate integer polynomial ring and permutation expansion;
it obtains the coefficient dictionary

```text
{a^3 b:-64, a^2 b^2:64}.
```

This rules out a hidden fourth generic root.  The three projective roots in
each family give

```text
Phi_1: A=x_2+x_3, B=x_0+x_1, N=x_0+x_1+x_2+x_3;
Phi_2: C=x_1+x_2, D=x_0+x_3, N=x_0+x_1+x_2+x_3.
```

### Attack: the quotient-incidence lemma assumes support at most two

It does not.  If all three other local planes miss `H_p`, the quotient
trilinear map forces cross-colour `J`-orthogonality.  Three active colours
are impossible in a two-dimensional nondegenerate `J`-space.  The one- and
two-support cases are then separately impossible.  Therefore a companion
exists for every nonzero support.  Legal double contraction with that
companion gives disjoint support and only then yields the support-at-most-two
conclusion.

This order matters for the common line `N`, whose first contraction has no
missing diagonal.  The proof does not silently borrow a support filter from
the displayed mixed-star frame.

### Attack: the common line might survive

For `N`, the three diagonal contractions have rank three and their common
annihilator is exactly

```text
K(-x_0+x_1+x_2+x_3).
```

At that companion line, two exact contraction relations force all three
local colour coefficients to vanish.  Both implementations check the rank,
annihilator, and relations.  Thus `N` is excluded without a same-mode double
contraction.

The remaining exceptional relations force

```text
A:{0},        B subset {1,2},
C:{1},        D subset {0,2}.
```

Since a vector space over the infinite field `K` cannot be a finite union
of two proper lines, every restricted projection has rank at least two.

## 4. Attack on rank-drop existence

The proof does not assume a low mode.  Suppose one projection family had
rank three on all four local planes.  The reviewed hyperplane-product lemma
applies because:

1. the four displayed factors form coordinates on a four-space;
2. every local image is a hyperplane;
3. the complete polarized mixed tensor vanishes.

The common missing factor cannot be `x_4` or `x_5`, since every diagonal
sensor contains both.  Either remaining hyperplane meets the other ambient
projection kernel only in `N`.  Since `N` is excluded, the other family is
also full rank and has a common missing factor.

The four resulting common cells have exact diagonal sensor ranks

```text
(2,2,2,1).
```

Both replays solve the two defining hyperplanes and restrict all three
diagonal cores.  The audit uses rational row reduction rather than the
primary's symbolic substitution.  Every rank is below the three independent
diagonal targets.  The argument is symmetric, so both families contain a
rank-two mode.

## 5. Attacks on companion exhaustiveness

The annihilator spaces are exactly

```text
H_A=span{C,E},       H_B=K F,
H_C=span{A,E},       H_D=K G,
```

where `E=x_1+x_3`, `F=x_1-x_0`, and `G=x_3-x_0`.

For `q=uC+vE`, deleting `d_1` and `d_2` from the contraction matrix gives
nonzero `3 x 3` minors that are constant multiples of `uv^2` and `u^2v`.
For `q=uA+vE`, the analogous `d_0,d_2` minors have the same monomials.
If a companion colour is live, its diagonal column must be a coloop, so
`uv=0`.  Endpoint relations then force the exact colours.  The audit checks
every nonzero deletion minor, not only a selected determinant.

The complete necessary table is

```text
A -> C/1 or E/2,
C -> A/0 or E/2,
B -> F/0,
D -> G/1.
```

Every companion lies in a distinct local mode.  The table is a necessary
classification, not a realizability claim.

## 6. Attacks on the terminal cycle exclusions

Only a `Phi_1` low is needed.  Its exhaustive cycles are

```text
(A,C),                     (A,E),                     (B,F).
```

Both implementations verify the common nonzero contraction covector on
the low and companion shores.  This produces full three-slot copies of
`pol(ell*x_4*x_5)`, not a scalar surrogate for a second contraction.

### Support-two attack

Only `B` can use two colours.  If it does, the common cubic's slice map
contains three independent diagonal matrices and becomes a concise weighted
`Delta_3`.  But the first-mode slice space of `pol(XUV)` is

```text
span{sym(UV),sym(XV),sym(XU)},
```

whose three principal rank-one conditions are `-c^2,-b^2,-a^2`.  It
contains no nonzero rank-one matrix in characteristic zero.  The independent
audit exhausts all `124` and `342` nonzero coefficient triples over
`F_5` and `F_7` as audit-only stress tests; the written square argument is
the characteristic-zero proof.

### Singleton attack

The two live slices make the common cubic slice rank two or three.  In rank
three the unused-colour vectors on the low/companion shores vanish after
evaluation by `(ell,x_4,x_5)`.  In rank two, the exact contraction matrix

```text
[0 V U; V 0 X; U X 0]
```

has no two-dimensional annihilator for a nonzero vector, so the unused
vectors on the other shores vanish after evaluation.

The terminal channel combinations are checked coefficient by coefficient:

```text
g_(d_0)+g_(d_1)+g_(d_2)=-2x_0(x_1+x_2+x_3),

-g_(m_1)+2g_(m_2)-2g_(d_0)-g_(d_1)-g_(d_2)
  =4x_0(x_2+x_3).
```

Each is divisible by the applicable `ell` and has nonzero coefficient at
every possible unused diagonal.  The ambient polarization is therefore zero
on the relevant two `ker(ell)` shores, while the exact diagonal target is a
nonzero multiple of `lambda_t`.  This closes both slice ranks.

## 7. Independence assessment

The audit is genuinely implementation-independent at the practical level:

- it imports neither the primary verifier nor SymPy;
- it rebuilds the nine products and Hodge complement with integer tuples;
- it uses rational row reduction instead of symbolic matrix methods;
- it expands determinants in a custom polynomial dictionary;
- it checks every deletion minor rather than a gcd reported by the primary;
- it separately enumerates the finite-field slice obstruction.

The two programs necessarily share the mathematical frame and the expected
claim.  They are not formal proofs and the finite-field checks are not used
to infer characteristic zero.  Their role is to replay and adversarially
cross-check the exact algebra supporting the written proof.

## 8. Scope ledger

```text
pure-star based representative 014:                    EXCLUDED;
all four noncommon low lines:                           CLASSIFIED;
all load-bearing Phi_1 cycles:                          EXCLUDED;

fixed e=1 representative 025:                          OPEN;
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
hostile mathematical review:                           PASS;
```
