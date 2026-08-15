# Hostile review of the active-support-at-least-six equality exclusion

## Verdict and scope

**PASS, for the stated pair-level, full-active-support, `n>=6`,
characteristic-zero scope.**  No mathematical, quantifier,
case-exhaustiveness, support-boundary, field, converse, or implementation
blocker survived hostile review.

For three-planes `U,V subset (Z_n)_1` whose union uses all `n` coordinates,
the package proves

```text
n>=6 and dim(UV)=5
  => U=V=Kx_i direct-sum W,  dim W=2,  dim(W^2)=3.
```

The converse holds, with full active support exactly when `W` uses every
coordinate other than `i`.  The multiplication-dual rank-one locus then has
all factors in one fixed two-plane, so no classified pair is
Delta-admissible at the pair level.

This does not prove that every omitted pair in a putative full restriction
has product dimension five, does not treat the separately owned
active-support-five case, and does not replace the active-support-four orbit
classification.  Unrestricted `P_6 -> Delta_3` remains unknown, and the
global Krenn--Gu conjecture remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_ACTIVE_SUPPORT_AT_LEAST_SIX_EQUALITY_EXCLUSION_THEOREM.md
  verify_arbitrary_permanent_active_support_at_least_six_equality_exclusion.py
  audit_arbitrary_permanent_active_support_at_least_six_equality_exclusion.py
```

No theorem or verifier edit was required.

## 1. Symmetric-annihilator dimension

Let `E=K^n`, put `r=dim(U intersect V)`, `H=U+V`, and let
`C=ann_E(H)`.  Thus

```text
dim H=6-r,                 dim C=k=n-6+r.
```

For

```text
T={Q in Sym^2(E^*):Q(U,V)=0},
```

the zero-diagonal part is exactly the annihilator of `UV` in the
square-free quadratic space.  The factor `2` in the off-diagonal pairing is
invertible in characteristic zero.  Hence `dim(UV)=5` gives

```text
dim(T intersect D_0)=binomial(n,2)-5.                       (1)
```

Choose

```text
H=R direct-sum Y direct-sum Z,
R=U intersect V,
U=R direct-sum Y,
V=R direct-sum Z.
```

A symmetric form on `H` that kills `U x V` has only its `Y x Y` and
`Z x Z` blocks free.  Thus, if `T_0` is the kernel of restriction to
`H x H`, then

```text
T/T_0 = Sym^2(ann_H(V)) direct-sum Sym^2(ann_H(U)),
dim(T/T_0)=(3-r)(4-r).
```

The residual dimensions for `r=0,1,2,3` are therefore exactly
`12,6,2,0`.  Combining this with (1) and rank-nullity gives the forced
diagonal rank

```text
d=rank(diag|T)=n-4+r(r-1)/2.                               (2)
```

This calculation is valid pointwise and uses neither genericity nor an
unstated transversality assumption.

## 2. The invisible block and the strict support bound

Let

```text
J=supp(C),        s=|J|,        I={0,...,n-1}\J.
```

The forms in `T_0` are spanned by symmetrized tensors `c tensor ell` with
`c in C`.  Their coordinate diagonals are
`(2c(x_j)ell(x_j))_j`, so their diagonal image is exactly `K^J`.  It follows
that

```text
s<=d.                                                       (3)
```

Since `C subset K^J`, one also has `s>=k`.  The only delicate boundary is
equality.  If `k>0` and `s=k`, then dimension forces `C=K^J`; consequently
`H=C^perp` omits every nonempty coordinate in `J`, as do both `U` and `V`.
This contradicts full active support.  Therefore

```text
k>0 and full active support  =>  s>=k+1.                   (4)
```

For `i in I`, the coordinate axis `x_i` belongs to `H`.  If `a_i` and
`b_i` are its evaluations on `ann_H(V)` and `ann_H(U)`, respectively, then
projection away from the already free `J`-coordinates gives the exact
identity

```text
q:=d-s=dim span{a_i^2 direct-sum b_i^2:i in I}.            (5)
```

The elementary inequality

```text
dim span{z_i} <= dim span{z_i^2}                            (6)
```

holds because the squares of any linearly independent subfamily remain
linearly independent in its symmetric-square basis.  Applying (6) to the
first summands of (5), the evaluation map `H -> ann_H(V)^*`, whose kernel is
`V`, yields for `X=span{x_i:i in I}`

```text
dim(X intersect V)>=n-s-q.                                 (7)
```

This confirms that the proof uses the equality `q=d-s`, not merely an
upper bound, and that no support direction has been lost in the quotient.

## 3. Exhaustion of `r=0,1,2,3`

The four possible intersection dimensions give the following complete
table.

```text
r   k=n-6+r   d                     consequence
0   n-6       n-4                   dim(X intersect V)>=4>3
1   n-5       n-4, s=k+1=d, q=0     dim X=4 but X subset U intersect V
2   n-4       n-3, s=k+1=d, q=0     dim X=3 but X subset U intersect V
3   n-3       n-1, residual=0        s=d=n-1
```

For `r=0`, substituting `q=d-s` into (7) gives four independently of
`s`; this case is impossible even without active support.  For `r=1,2`,
(3)--(4) squeeze `s` to `d`.  Then (5) has zero span, so every outside axis
has both evaluations zero and hence lies in `U intersect V`, contradicting
the displayed dimensions.  These arguments also cover the boundary
`n=6`; there is no hidden assumption that `k` is large.

Thus only `r=3` survives, and `U=V`.  Here the residual block is zero, so
(5) forces `q=0`, hence `s=d=n-1`.  There is exactly one outside coordinate
axis `x_i`, and it lies in `U`.

## 4. Survivor classification and converse

Writing

```text
W=U intersect ker(x_i-coordinate)
```

gives `U=Kx_i direct-sum W` with `dim W=2` and `W` supported away from
`i`.  Square-free edge support separates the product into

```text
U^2=x_iW direct-sum W^2.
```

Multiplication by `x_i` is injective on forms supported away from `i`, so
`dim(x_iW)=2`.  The equality hypothesis therefore forces
`dim(W^2)=3`.  Conversely, any such split has product dimension
`2+3=5`; it uses all `n` coordinates precisely when `W` uses all `n-1`
coordinates away from `i`.  This proves both directions of the stated
classification rather than only a necessary normal form.

As an additional hostile check, an independent exact enumeration of all
`33,880` planes in `Gr(3,6)(F_3)` found `3,840` full-support planes with
square dimension five.  Every one contained exactly one coordinate axis;
none contained zero or multiple coordinate axes.  This finite-field census
is corroborative only; the written argument above proves the claimed
characteristic-zero result.

## 5. Delta nonadmissibility

For the common plane, the multiplication-dual space

```text
L=mu^*((U^2)^*) subset Sym^2(U^*)
```

has dimension five.  Every square-free edge functional vanishes on
`(x_i,x_i)`, so `L` is contained in the five-dimensional hyperplane of
symmetric forms with that entry zero.  Equality of dimensions makes this
containment an equality.

A nonzero rank-one tensor lying in a symmetric tensor space has
proportional factors, say `c lambda tensor lambda`.  Its value at
`(x_i,x_i)` is zero only if `lambda(x_i)=0`.  Hence every left and right
factor in the complete rank-one locus of `L` belongs to the same
two-dimensional annihilator of `x_i`.  No three such factors can form the
two bases required by the invariant multiplication-dual criterion, so none
of the survivors is Delta-admissible.

## 6. Computational replay and independence

The primary verifier uses exact SymPy arithmetic to check the annihilator
and diagonal-rank formulas through `n=24`, canonical models for all four
intersection dimensions, the square-span inequality, rational active
survivors through `n=10`, and the rank-one hyperplane obstruction.

The independent audit imports neither the primary verifier nor SymPy.  It
reconstructs the symmetric restriction equations with a custom finite-field
row reducer, checks the block dimensions over `F_5`, exhausts all
`4,991` projective square families of sizes at most three, checks the
arbitrary-`n` boundary arithmetic through `n=40`, rebuilds survivor examples,
and exhausts the rank-one hyperplane locus.  It found `24` nonzero rank-one
matrices and zero whose factor failed to annihilate the coordinate axis.
This is meaningfully independent implementation evidence; the finite-field
checks audit conventions and case structure, while Sections 1--5 of the
theorem are the arbitrary-`n` proof.

Focused final replay passed:

```text
primary exact verifier:       PASS;
independent no-import audit:  PASS;
py_compile:                   PASS;
Ruff:                         PASS.
```

## 7. Accepted boundary

```text
active-support n>=6 equality-five pairs:                 CLASSIFIED;
only surviving normal form:                              U=V=Kx_i+W;
survivor condition:                                      dim(W^2)=3;
pair-level Delta-admissible active-support n>=6 pair:    NONE;
active-support-five package:                             SEPARATELY OWNED;
active-support-four classification:                      NOT CHANGED;
arbitrary omitted-pair product dimension five:           NOT PROVED;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.
```

## Final reviewed hashes

```text
theorem:
D55AA47CDA33CC749522164AC477935798B9E6BEE1DEF41EDAADA80BE9E645F7

primary verifier:
A505515EF0274F03EA636E8C339054A55D659705F00A951DE5A5C5B49E4687E8

independent audit:
3C911034221D721E079856AE0D20223E09A8363717EFA22E9498FF7F4994F147
```
