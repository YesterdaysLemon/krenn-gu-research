# Arbitrary permanent fixed-pair two-low zero-branch exclusion theorem

## Status

This note proves an exact characteristic-zero exclusion inside the fixed
equality-five pair.  Assume the committed same-mode exclusions and the
distinct-two-low reduction.  Thus there are exactly two distinct low modes,
one for each mixed-factor projection family; the other two modes are high
for both families.  This note excludes the branch in which the
`x_4,x_5` pairing matrix between those two high modes is zero.

The key point is that a noncommon `Phi_1` exceptional vector contracts the
opposite mixed quartic to the covector

```text
h_2=x_0+(x_3-x_2-x_1),
```

while a noncommon `Phi_2` exceptional vector contracts the other mixed
quartic to

```text
h_1=x_1+(x_3-x_2-x_0).
```

On a high mode, `h_k` is independent of the unique covector carrying its
rank-one `A`-projection.  The two mixed-zero equations then put both low
`A`-images in the common orthogonal complement of the two high image lines.
The high lines are already orthogonal.  A two-dimensional dichotomy now
makes every `A`-pairing zero, contradicting the nonzero diagonal target.

This theorem does not exclude the surviving nonzero-`E_22` branch, does not
normalize an arbitrary equality-five pair to the fixed pair, and does not
prove unrestricted permanent nonrestriction.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## 1. Fixed pair and reduction input

Let `K` be a field of characteristic zero and work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

Put

```text
l_1=x_3-x_2-x_0,              l_2=x_3-x_2-x_1.        (1)
```

At the fixed equality-five pair, the two mixed complementary quartics are

```text
star(m_1)=x_4x_5 x_1 l_1,
star(m_2)=x_4x_5 x_0 l_2,                              (2)
```

and the three diagonal quartics are

```text
star(d_0)= x_4x_5 (x_1+x_2)(x_3-x_0),
star(d_1)= x_4x_5 (x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5 x_0x_1.                             (3)
```

Let the ordered independent triples in the four remaining modes span local
three-spaces `L_t`.  Assume the exact target equations

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (4)
```

Split the ambient space as

```text
K^6=R direct-sum A,
R=span{x_0,x_1,x_2,x_3},       A=span{x_4,x_5},
J((r_4,r_5),(s_4,s_5))=r_4s_5+r_5s_4.                 (5)
```

Write `A_t:L_t -> A` for the `A`-projection.  The two projection families
are

```text
Phi_1=(x_1,x_4,x_5,l_1),
Phi_2=(x_0,x_4,x_5,l_2).                               (6)
```

The distinct-two-low predecessor reduces the zero branch, after relabelling
the four tensor slots, to the following data:

```text
a: low only for Phi_1, with line A_0 or C_0;
b: low only for Phi_2, with line A_1 or C_1;
s,t: high for both Phi_1 and Phi_2;
A_s^T J A_t=0.                                        (7)
```

Here

```text
A_0=(1,0,0,1,0,0),       C_0=(1,0,-1,0,0,0),
A_1=(0,1,0,1,0,0),       C_1=(0,1,-1,0,0,0).          (8)
```

The vectors in (8) are normalized generators.  Multiplying one by a nonzero
scalar only multiplies the corresponding contraction and changes none of
the conclusions below.  Their local colour supports may have size one or
two; the proof never assumes either alternative.

## 2. Rank-one high shores

Every high mode has nonzero `A`-projection.  Indeed, if `A_s=0`, either map
in (6) has at most its two displayed `R`-coordinates on `L_s`, so its rank
is at most two, contrary to highness.

The zero matrix in (7) and nondegeneracy of `J` imply

```text
rank A_s=rank A_t=1.                                  (9)
```

For if one map had rank two, its image would be all of `A`; orthogonality
would force the other map to vanish.  Choose nonzero image vectors `u,v`
and nonzero local covectors `rho_s,rho_t` so that

```text
A_s=u rho_s,                 A_t=v rho_t.              (10)
```

Equation (7) becomes

```text
J(u,v)=0.                                               (11)
```

## 3. The exact opposite-mixed contractions

Define

```text
h_1=x_1+l_1=2x_1-x_0-x_2+x_3,
h_2=x_0+l_2=2x_0-x_1-x_2+x_3.                         (12)
```

For both `p in {A_0,C_0}` one has

```text
x_0(p)=l_2(p)=1,
```

and for both `q in {A_1,C_1}` one has

```text
x_1(q)=l_1(q)=1.                                      (13)
```

Consequently the polarization of `x_0l_2` contracted by `p` is exactly
`h_2`, and that of `x_1l_1` contracted by `q` is exactly `h_1`.

The independence needed below is forced by highness, not assumed.  On the
rank-one high mode `s`, the row span of `Phi_2|L_s` is

```text
span{x_0|L_s,l_2|L_s,rho_s}.                           (14)
```

Its rank is three, so those three covectors are independent.  Hence

```text
rho_s and h_2|L_s are independent.                    (15)
```

The same holds on `t`.  Using `Phi_1` instead gives

```text
rho_s and h_1|L_s are independent,
rho_t and h_1|L_t are independent.                    (16)
```

In particular, all covectors appearing in (15)--(16) are nonzero.

Let `p` be the normalized `Phi_1`-low generator in slot `a`.  Contract
`T_(m_2)=0` legally once in that slot.  Complete polarization of (2), with
the common normalization fixed by (13), gives on the remaining slots
`b,s,t`

```text
 J(A_b(-),u) tensor rho_s tensor h_2|L_t
+J(A_b(-),v) tensor h_2|L_s tensor rho_t=0.            (17)
```

There is ordinarily a third term

```text
J(u,v) h_2|L_b tensor rho_s tensor rho_t,
```

but it vanishes by (11).  No vector from one local mode is ever inserted
into a different tensor slot.

Because `rho_s,h_2|L_s` are independent, choose a vector of `L_s` on which
the first is nonzero and the second is zero.  Evaluating (17) there, and
using `h_2|L_t!=0`, proves

```text
J(A_b(-),u)=0.                                        (18)
```

Choose instead a vector on which `rho_s` is zero and `h_2|L_s` is nonzero.
Since `rho_t!=0`, this proves

```text
J(A_b(-),v)=0.                                        (19)
```

Now contract `T_(m_1)=0` once in slot `b` by its normalized
`Phi_2`-low generator `q`.  The identical argument using (16) yields

```text
J(A_a(-),u)=J(A_a(-),v)=0.                            (20)
```

Thus both low images lie in

```text
im A_a, im A_b subset u^perp intersect v^perp.         (21)
```

## 4. Two-dimensional closure

There are two cases.

If `u,v` are independent, they span the two-dimensional nondegenerate space
`A`, so (21) gives

```text
A_a=A_b=0.                                             (22)
```

The only possible `A` suppliers are then `s,t`, whose entire pairing matrix
is zero by (7).

If `u,v` are dependent, write `v=cu` with `c!=0`.  Equation (11) gives
`J(u,u)=0`.  In a nondegenerate two-dimensional space, an isotropic line is
its own orthogonal complement:

```text
(Ku)^perp=Ku.                                          (23)
```

Equations (10) and (21) therefore put all four local `A`-images in `Ku`.
Every pairwise `J`-pairing again vanishes.

In either case, every term in the polarization of every quartic in (2)--(3)
vanishes: such a term must choose two distinct slots to supply `x_4,x_5`,
and their contribution is precisely a `J`-pairing.  This contradicts, for
example,

```text
T_(d_0)(e_0,e_0,e_0,e_0)=lambda_0!=0.                 (24)
```

This proves the exclusion.

## 5. Exact scope and replay

```text
fixed equality-five pair:                                  ASSUMED;
exactly two distinct noncommon lows, one per family:        ASSUMED;
other two modes high for both families:                     ASSUMED;
high-high pairing matrix zero:                              EXCLUDED;
nonzero E_22 high-high branch:                              OPEN;
unrestricted P_6 -> Delta_3:                               UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED. (25)
```

Replay the exact identities and finite sanity checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_two_low_zero_branch_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_two_low_zero_branch_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_two_low_zero_branch_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_two_low_zero_branch_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_two_low_zero_branch_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_two_low_zero_branch_exclusion.py
```

The primary verifier uses exact symbolic complete polarization to check all
four exceptional generators, both family orientations, the high-covector
determinant identity, and the mixed-contraction factorization.  It also
exhausts the cancellation and two-dimensional orthogonality lemmas over odd
finite fields as error-detecting checks.  The independent audit imports
neither the primary verifier nor SymPy: it reconstructs the quartics as
square-free monomial dictionaries, polarizes them independently, and uses
separate modular row reduction for its finite checks.  These computations
replay displayed algebra and finite sanity checks; the written
characteristic-zero argument proves the theorem.
