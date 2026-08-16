# Hostile review of the co-two `r=4` fixed-`e=2` full-extension exclusion

## Verdict

**PASS, at the stated pointwise scope.**

The package proves that the displayed based `(4,2)`, `e=2` frame,
representative `024`, has no exact `P_6 -> Delta_3` extension over a field
of characteristic zero.  It handles the common projection-kernel line before
ordinary incidence, proves rank drop in both mixed projection families, and
closes every companion incidence needed by one family.

This is the last equality-five representative endpoint, but this review does
not substitute for the planned full equality-five synthesis audit.  The
dimension-at-least-six co-two sensor residual, unrestricted
`P_6 -> Delta_3`, and the global Krenn--Gu conjecture remain open.  Global
status remains **UNRESOLVED**.

## Reviewed artifacts

Hashes are SHA-256 of LF-normalized text bytes.

```text
theorem:
claims/arbitrary-order/ARBITRARY_PERMANENT_COTWO_R4_FIXED_E2_FULL_EXTENSION_EXCLUSION_THEOREM.md
CF79C02D6C45359F1F26AEFAD4E4C0AB9715A57ADA26B1E57D18A772022B764E

primary:
claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_fixed_e2_full_extension_exclusion.py
A4F68FB8AE8D5D977C99875C2E2298C2417E29A408B81F1345C9BDE990477A91

independent audit:
claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_fixed_e2_full_extension_exclusion.py
7D0C24E338524ED04EF387A0C31977A821C73DBD70E31F3BA2D390A8A6809589
```

The audit pins the theorem and primary.  Both replays pin the reviewed
based-frame classification and hyperplane-product interface.  LF
normalization makes the pins portable across LF and CRLF checkouts.

## 1. Claim boundary and complete target

The exact input is

```text
U=(x_0+x_1-x_2-x_3, x_1-x_3, x_0-x_3),
V=(x_0+x_1+x_2+x_3, x_1+x_2, x_0+x_2).
```

Both replays multiply all nine pair products.  The mixed products have rank
two, the full products have rank five, and every off-diagonal product is one
of the two displayed mixed basis vectors.  The two mixed zeros and three
diagonal targets are therefore the complete pair-product target.

The conclusion is pointwise nonextension of `024`.  The based-frame and
transport packages, not this theorem alone, establish its orbit role.

## 2. Attack on the complementary cores

The primary uses symbolic square-free multiplication and set complementation.
The audit uses independent integer tuples and an edge lookup.  Both derive

```text
g_(m_1)=-(x_0-x_3)(x_1+x_2),
g_(m_2)=-(x_0+x_2)(x_1-x_3)
```

and the same three diagonal cores.  Hence both projection maps are derived,
not supplied as unchecked input.

## 3. Attacks on generic and exceptional kernel directions

The kernels are parameterized by

```text
p_1(r,s)=(r,s,-s,r),              p_2(r,s)=(r,s,-r,s).
```

The primary obtains determinants

```text
8rs(r-s)(r+s),                   -8rs(r-s)(r+s).
```

The audit expands both with a custom bivariate polynomial dictionary and
gets coefficient maps `{r^3s:8,rs^3:-8}` and its negative.  There is no
unlisted generic root.

### Attack: support three at the common line is assumed away

It is handled first.  The common root

```text
N=(1,1,-1,1)
```

has contraction rank three and no diagonal support relation, so all three
colours are initially possible.  Its annihilator is exactly
`K G`, where `G=(0,0,1,1)`.  The all-support companion lemma supplies a
nonzero `G` in another mode before making any small-support assumption.

At `G`, the exact relations are

```text
-B_(m_1)-B_(m_2)+B_(d_0)=0,
B_(d_1)=B_(d_2)=0.
```

The legal single-contraction support filter forces the companion
coefficients at colours `0,1,2` all to vanish.  This contradicts `G!=0`.
Thus `N` is impossible for every support, including support three.

### Attack: the incidence lemma reuses one tensor slot

It does not.  The quotient argument first forces a companion in one of the
three other local modes.  Disjoint support is then obtained by contracting
the source tensor in those two distinct modes.  Every later use preserves
distinct slots.

The six remaining roots all have contraction rank three and exact support
bounds

```text
A,D subset {0,2};       B,E subset {0,1};       C,F subset {1,2}.
```

With `N` absent, a kernel intersection cannot contain a plane because a
plane over the infinite field cannot be a union of three lines.  Restricted
projection rank is therefore at least two.

## 4. Attack on rank-drop existence

Suppose every `Phi_1` image had rank three.  The reviewed
hyperplane-product lemma forces one common missing factor.  The missing
factor cannot be `x_4` or `x_5`, so it is `a=x_0-x_3` or `b=x_1+x_2`.

Inside either hyperplane, the kernel of `Phi_2` is exactly `K N`.  Since `N`
is impossible, all four `Phi_2` images are also hyperplanes, and their mixed
zero tensor forces common missing factor `c=x_0+x_2` or `d=x_1-x_3`.

Both implementations solve all four cells independently and obtain diagonal
sensor ranks

```text
(a,c):2,       (a,d):2,       (b,c):2,       (b,d):2.
```

Each is below the three independent diagonal targets.  Exchanging the two
families proves a rank-two mode in both.

## 5. Attack on companion exhaustiveness

The annihilators are exactly

```text
H_A=K A', H_B=K B', H_C=K C',
H_D=K D', H_E=K E', H_F=K C'.
```

No positive-dimensional pencil remains.  Exact relations at the five
companion lines force colours

```text
A -> A'/1, B -> B'/2, C -> C'/0,
D -> D'/1, E -> E'/2, F -> C'/0.
```

Both programs verify the relations and every annihilator by rank and direct
pairing.  The table is necessary incidence, not a realizability assertion.

They also agree on all six common contraction covectors.  In particular the
three load-bearing `Phi_1` rows are

```text
A,A': ell=-2x_0;
B,B': ell=-2x_1;
C,C': ell= 2(x_2-x_3).
```

These yield full three-slot polarizations of `ell*x_4*x_5`; no scalarized
same-mode contraction is substituted.

## 6. Attacks on terminal exclusion

### Support-two attack

Every low line permits at most two colours, while its companion has the
third.  If both low colours occur, the common cubic has three independent
diagonal slices and becomes a concise weighted `Delta_3`.  But the slice
space of `pol(XUV)` is

```text
span{sym(UV),sym(XV),sym(XU)}.
```

The principal rank-one conditions of a general slice are
`-c^2,-b^2,-a^2`; there is no nonzero rank-one matrix in characteristic
zero.  The audit enumerates all nonzero coefficient triples over `F_5,F_7`
only as a stress check.

### Singleton attack

The two live diagonal slices make the common-cubic slice map rank two or
three.  At rank three, the unused-colour evaluations vanish on the low and
companion shores.  At rank two, the matrix

```text
[0 V U; V 0 X; U X 0]
```

has rank at least two for every nonzero `(X,U,V)`, so the unused evaluations
vanish on the two untouched shores.

The exact terminal gates are

```text
-g_(m_1)-g_(m_2)+g_(d_0)+g_(d_2)=-x_0(x_1-x_2+x_3),
-g_(m_1)-g_(m_2)+g_(d_0)+g_(d_1)=-x_1(x_0-x_2+x_3),
-g_(d_1)+g_(d_2)=(x_0-x_1)(x_2-x_3).
```

Each is divisible by its row's `ell` and has nonzero coefficient at every
possible unused diagonal.  Polarization vanishes on the two forced
`ker(ell)` shores, while the target is a nonzero multiple of the unused
`lambda`.  Both slice ranks are contradicted.

## 7. Independence assessment

The audit is genuinely implementation-independent at the practical level:

- it imports neither the primary nor SymPy;
- it rebuilds the nine products and complements with integer tuples;
- it uses rational row reduction rather than symbolic matrices;
- it expands determinants in a custom polynomial ring;
- it solves all common cells from their defining forms;
- it checks every relation, annihilator, residual, and core combination;
- it separately enumerates the slice obstruction over two odd finite fields.

The finite-field enumeration does not prove the characteristic-zero result.
The written argument is the proof; both programs replay its load-bearing
exact algebra.

## 8. Scope ledger

```text
fixed e=2 based representative 024:                    EXCLUDED;
common support-three line N:                           EXCLUDED;
ordinary lines A,B,C,D,E,F:                            CLASSIFIED;
load-bearing Phi_1 incidences:                         EXCLUDED;

all equality-five representatives individually:        EXCLUDED;
equality-five synthesis audit:                         PENDING;
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
