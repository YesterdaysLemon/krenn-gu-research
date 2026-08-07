# Full-kernel flat collisions are zero cubes or presymplectic rank-drop seams

## Status

This is an exact characteristic-zero classification of every affine-ratio
collision in the full-kernel-support flat rank-two-relation triangle.

Combined with the distinct-ratio finite and projective theorems,

- [`P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md`](../../../../boundaries/rank-two-triangle/resonant/flat-generic-binary-cubic/P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md),
- [`P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md`](../flat-projective-partner/P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md),

it proves:

> No flat all-rank-three-relation triangle has a kernel row of full source
> support.

For ratio multiplicities `2+1+1` and `3+1`, the active cubic is zero.  For
`2+2`, the synchronizer jumps from a projective line to a projective plane.
Its induced alternating form has a one-dimensional radical, so compatible
flat triples are projective lines through that radical.  The only finite
pure points form four signed seams, and every one makes the two noncentral
planes have pair-image rank two.  The projective endpoints are empty.

The smaller-support strata have since been classified and contain one
support-two annihilator-line survivor:
[`P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md`](../../../triangle-211/rank-two-relation-triangle-corrected/P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md).
This is not a classification of every pure `P_4` component and not a proof or
counterexample for the global Krenn--Gu conjecture.

## The collision list under legal Borel gauge

Let the full-support kernel row be scaled to

```text
y=(1,1,1,1).
```

A common affine change of the four ratios is legal.  Excluding four equal
ratios, which would make the local map rank one, every collision pattern is
one of

```text
2+1+1:        x=(0,0,1,ell),       ell(ell-1)!=0,
2+2:          x=(0,0,1,1),
3+1:          x=(0,0,0,1).                         (1)
```

Source permutations cover all labelings.  This list uses only the affine
group preserving the marked kernel line, not full row `PGL_2`.

## The `2+1+1` and `3+1` zero-cube mechanism

For the `2+1+1` center `A=(y;x)`, the full synchronizer is

```text
span(A,B),

B=(z;0),             z=(0,0,-1,ell).                (2)
```

The projective point `B` has local rank one and is inadmissible.  Every
valid partner is therefore finite, `A+tB`, and has the same active row `x`.
Since `x` has support two in the squarefree algebra,

```text
x^3=0.                                                 (3)
```

The escaping binary-cubic coefficient `X` is consequently zero, contrary
to purity.

For `3+1`, the same calculation gives

```text
B=((0,0,0,1);0),
```

and now `x` has support one, so (3) is even more immediate.  Thus both
collision types are empty before any determinant calculation.

## The `2+2` synchronizer as a presymplectic plane

Put

```text
A=((1,1,1,1);(0,0,1,1)),

B_0=((0,0,-1,1);(0,0,0,0)),
B_1=((-1,1,0,0);(-1,1,0,0)).                       (4)
```

The synchronizer is the three-dimensional vector space

```text
S=span(A,B_0,B_1).                                    (5)
```

For row-pairs `P=(y_P;x_P)`, define the alternating product

```text
omega(P,Q)=y_P x_Q-x_P y_Q in R_2.                   (6)
```

Direct multiplication gives

```text
omega(A,B_0)=omega(A,B_1)=0,
omega(B_0,B_1)=(0,1,-1,-1,1,0)=:w.                  (7)
```

Thus `A` is the radical of this presymplectic plane.  For

```text
P=cA+aB_0+bB_1,       Q=c'A+a'B_0+b'B_1,
```

one has

```text
omega(P,Q)=(ab'-ba')w.                                (8)
```

Consequently two partners synchronized with `A` synchronize with each
other exactly when their directions `[a:b]` agree.  Every flat triple is
therefore contained in a projective line through `[A]`:

```text
A,                 A+tD,                 A+uD,
D=rB_0+sB_1.                                        (9)
```

This is the useful foreign shape: the compatibility problem is not a large
permanent ideal but the isotropic-line geometry of a degenerate alternating
form.

## The finite `2+2` line

Write `D=(d_y;d_x)`, so

```text
d_y=(-s,s,-r,r),          d_x=(-s,s,0,0).            (10)
```

For the three planes in (9), let `C=[Y K J X]`.  Its compression minors are

```text
-16s(t+u)(rt+1)(ru+1),
-16s(t+u)(rt-1)(ru-1),
 16r(t+u)(st+1)(su+1),
 16r(t+u)(st-1)(su-1),                              (11)
```

and

```text
det C=-64rs(t+u)^2.                                  (12)
```

More strongly, every full `3 x 3` minor is divisible by `t+u`.

There are three direction types.

### `s=0`

The fourth column `X` is identically zero, so purity is impossible.

### `r=0`, `s!=0`

The first minor in (11) forces `u=-t`.  If the compressed span were a
line, two of its `2 x 2` minors would give

```text
(st)^2=1,                  (st)^2=3/2,               (13)
```

a contradiction.

### `rs!=0`

The first two equations in (11) force `t+u=0`.  Indeed, otherwise
`{rt,ru}` would have to be `{+1,-1}`, which already implies `t+u=0`.
All full cofactors now vanish, so purity can survive only if
`span(Y,K,J)` is a line.  Two compressed minors are

```text
4((st)^2-1),
4(r^2s^2t^4+2s^2t^2-3).                              (14)
```

They force

```text
st=+/-1,                    rt=+/-1.                  (15)
```

After rescaling the direction `D`, take `t=1,u=-1` and
`(r,s)=(epsilon,eta)` with `epsilon,eta in {+/-1}`.  At all four signed
points,

```text
C = ((8,4,2,0),
     (8,4,2,0),
     (8,4,2,2),
     (8,4,2,2)),                                      (16)
```

so the compressed/full ranks are exactly `(1,2)`: these are genuine pure
`P_4` restrictions.

But let `M_{+-}` be the `6 x 4` product matrix of the two noncentral planes
`A+D` and `A-D`.  At each of the four sign choices, every `3 x 3` minor of
`M_{+-}` is zero and a `2 x 2` minor is nonzero.  Hence

```text
rank M_{+-}=2.                                         (17)
```

The required triangle has pair-image rank three on every edge.  All four
pure seams therefore leave the triangle stratum.

## Projective endpoints of the `2+2` line

The endpoint `[D]` has local rank two exactly when `rs!=0`; otherwise it is
already inadmissible.

For the one-endpoint triple

```text
A,                     D,                     A+uD,
```

every full cofactor vanishes.  Purity would require the compressed span to
be a line, but two of its minors are

```text
8r^2su,                    4rs(rsu^2-1).              (18)
```

The first forces `u=0` and the second then stays nonzero.  For
`(A,D,D)`, every full cofactor again vanishes while a compressed minor is

```text
4r^2s^2 != 0.                                          (19)
```

Thus neither one nor two projective endpoints are pure.

## Combined full-support theorem

The four ratio-multiplicity types now have exact dispositions:

| affine ratios | disposition |
|---|---|
| `1+1+1+1` | finite and projective partner sheets empty |
| `2+1+1` | active cube `X=0` |
| `2+2` | four finite pure seams, all with a rank-two partner pair; endpoints empty |
| `3+1` | active cube `X=0` |
| `4` | center map has local rank one |

Therefore the flat all-rank-three-relation triangle has no
full-kernel-support point.

## Literature translation

The `2+2` jump is naturally a tiny presymplectic polar space: compatibility
is an isotropic-line condition and the central plane is the radical.  The
general projective language of regular, tangential, and symplectic-copolar
subspaces is developed by Prazmowska--Prazmowski--Zynel,
[Projective symplectic geometry on regular subspaces](https://arxiv.org/abs/1203.2053).

The rank-two seam (17) then lands in the smallest Kronecker/Segre pencil
boundary classified intrinsically in
[`P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md`](../../../pair-geometry/rank-two-pair-kernel-geometry/P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md),
next to De Teran--Dopico--Landsberg,
[Irreducible components of matrix pencils with bounded normal rank](https://arxiv.org/abs/1606.02574).
Equations (2)--(19) are direct squarefree-algebra calculations; neither
paper contains this particular collision-to-rank-drop implication.

## Verification

Run:

```text
python claims/p4/classifications/rank-two-triangle/resonant/flat-full-kernel-collision/verify_p4_resonant_flat_full_kernel_collision.py
python claims/p4/classifications/rank-two-triangle/resonant/flat-full-kernel-collision/audit_p4_resonant_flat_full_kernel_collision.py
```

The primary verifier reconstructs all three synchronizer spaces, checks the
presymplectic form, derives the finite compression and compound identities,
verifies the four pure seams and their pair-rank drops, and closes both
projective endpoint sheets.  The audit uses an independent subset-dynamic
squarefree product and replays the zero cubes, finite seams, and endpoints.
Neither script performs a search.
