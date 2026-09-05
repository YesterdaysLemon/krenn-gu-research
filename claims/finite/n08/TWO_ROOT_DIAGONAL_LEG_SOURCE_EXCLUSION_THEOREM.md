# Eight-vertex exclusion with six diagonal root legs

**Proved exact finite exclusion over C, independently reviewed on
2026-09-04.** The global Krenn--Gu conjecture remains **UNRESOLVED**.
This theorem excludes the entire root configuration stated below; it does
not assert that every witness supplies that configuration. No computational
certificate or Lean formalization is claimed.

## Exact statement

Let W be a ternary block graph on eight vertices, with roots r,s and
outsiders A_0,A_1,A_2,B_0,B_1,B_2. Suppose

```text
Q=W_rs is invertible,
W_rAi=L_i is invertible,   W_sAi=alpha_i E_ii,
W_rBj=beta_j E_jj,         W_sBj=M_j is invertible,
alpha_i!=0, beta_j!=0.
```

Assume each of the three physical AA blocks and three physical BB blocks
is a **nonzero matrix unit**, with arbitrary endpoint colours and arbitrary
nonzero complex coefficients. The nine AB blocks are arbitrary.

Then the full perfect-matching tensor of W cannot be Delta_(8,3).

The matrix-unit assumption is on the full physical blocks. Their inactive
restrictions may be zero; no such restriction is divided out. No maximum
torus-root assumption is needed once this configuration is given.

## Upstream source and exhaustive proof cover

Suppose for contradiction that the full tensor equals Delta_(8,3).
The [common-plane source reduction](TWO_ROOT_DIAGONAL_LEG_COMMON_PLANE_REDUCTION_THEOREM.md)
applies to this same physical graph. It supplies at least one shore whose
three inactive root-image planes coincide. Exchange the roots and shores
if necessary, and write

```text
U=L_i(ker e_i), with nonzero normal n,
H(A_inactive,B_full)=0,
P_0 C_AB+T C_BB=0.
```

Here all C blocks are actual four-vertex principal hafnians of the same
outside six-vertex graph, and every B variable remains fully open.
The opposite shore's planes are unrestricted throughout.

The [uniform zero-gauge lemma](diagonal-root-leg-source-exclusion/uniform-zero-gauge.md)
shows that C_BB cannot vanish identically on this slice. Its proof derives
global C_AB=0 from that temporary hypothesis, then specializes all three
inactive P columns to one generic vector v. One fixed fully supported
covector m annihilating v is used in all three first-normal equations.
This supplies all three nonzero target colours even when n has coordinate
zeros. The actual AB-normal derivative term is retained.

On the other hand, the number of nonzero coordinates of n is exactly
three, two, or one. These cases exhaust every nonzero normal:

1. If all three coordinates are nonzero, the hollow symmetric matrix C_BB
   has kernel vector `(beta_j n_j z_Bj[j])_j` with all entries nonzero over
   the full-B fraction field. Its three equations force every off-diagonal
   entry to vanish in characteristic zero. Thus C_BB=0.
2. If n has two nonzero coordinates, the
   [two-coordinate normal proof](diagonal-root-leg-source-exclusion/two-coordinate-normal.md)
   retains the entire hollow cofactor star and proves its coefficient
   lambda zero. It covers zero and nonzero weighted cofactor combinations
   and every remaining row-rank pattern. The final case uses the missing
   colour's complete mixed-normal equation, including its unknown AB-normal
   rows. Hence C_BB=0.
3. If n has one nonzero coordinate, the
   [coordinate-normal proof](diagonal-root-leg-source-exclusion/coordinate-normal.md)
   retains the free BB cofactor G. A generic two-column kernel lemma and
   the full corrected source column force G=0, including all zero-row and
   rank-one boundaries. Hence C_BB=0.

Every case contradicts the same uniform lemma. This proves the claimed
exclusion. Colour permutations cover the choices of missing coordinates;
they simultaneously relabel all physical slots and preserve Delta_(8,3).

## Noncircular dependencies and evidence

The upstream N8R2S theorem is already proved and is unchanged. The uniform
zero-gauge proof uses its full one-shore matrix equation, not either
coordinate-normal exclusion. The coordinate-normal proof's generic
kernel-column lemma is also used in the two-coordinate case; that algebraic
lemma includes a zero scalar parameter. Its larger corrected-source
forcing argument is used only when its scalar parameter is nonzero.
The zero-parameter branches are handled separately. Thus the proof cover
is exhaustive and noncircular.

The [independent integration review](../../../docs/audits/TWO_ROOT_DIAGONAL_LEG_SOURCE_EXCLUSION_REVIEW_2026-09-04.md)
pins the parent and all three proof leaves. The
[primary arithmetic replay](verify_common_plane_parent.py) checks the exact
weighted cofactor-column identity and the repaired missing-colour normal
extraction. Its physical fixture deliberately retains nonzero AB-normal
rows and uses the actual matching tensor on the right side. It is not a
GHZ witness, and finite replays are corroboration rather than the analytic
proof or a global certificate.

```text
python claims/finite/n08/verify_common_plane_parent.py
```

## Application: adjacent degree-four invertible vertices are excluded

In an eight-vertex hypothetical GHZ witness with maximum torus-root
cardinality two, let H3 contain exactly the invertible physical edges.
Then H3 cannot have two adjacent vertices of degree four.

The [N8R2S parent application](TWO_ROOT_DIAGONAL_LEG_COMMON_PLANE_REDUCTION_THEOREM.md)
already proves that such vertices supply the root configuration above.
It remains to supply the six nonzero physical AA/BB matrix units.

More generally, two invertible edges of a physical triangle force the
third edge to be a nonzero matrix unit under maximum root cardinality two.
Name the first two forms Q(x,y) and L(x,z), and the third B(y,z). On the
dense product-torus part of Q=0, absence of a third root forces a coordinate
component of `(x^T L) cross (y^T B)` to vanish. The product of the three
components vanishes modulo the irreducible Q, so one component is a
constant multiple of Q. Its coefficient matrix has rank at most two;
invertibility of Q forces that multiple to be zero.

The two-coordinate projection of x^T L is surjective. Its identically
zero determinant with the corresponding projection of y^T B therefore
forces that B projection to be zero. Thus B=b(y) z[c] for some c.
If B=0, choose a torus x whose L row is noncoordinate and whose Q row
has a torus kernel. Choose torus y in that kernel and torus z in the
L-row kernel, obtaining a forbidden root triple. These x exist outside
finitely many proper linear subspaces because Q,L are invertible.

If b is nonzero and noncoordinate, choose a generic torus y in ker b
such that Qy is noncoordinate. The x hyperplane `x^T Qy=0` has a dense
torus part. Its image under invertible L^T is two-dimensional, so choose
a torus x there with x^T L noncoordinate, then a torus z killing that row.
Again all three edges vanish. Hence b is a nonzero coordinate functional,
and B is a nonzero matrix unit.

Apply this fact to the two invertible r spokes at every A pair, and to
the two invertible s spokes at every B pair. The six required matrix units
are supplied on the same graph. The parent exclusion now gives the
contradiction, proving the adjacent-degree-four consequence.

Other invertible-edge components, graphs with no invertible edges, other
maximum root orders, arbitrary n, and the global conjecture remain open.
This result does not assert that every witness has adjacent degree-four
invertible vertices, and it does not exclude arbitrary eight-vertex graphs.
