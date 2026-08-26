# Review: survivor response sign-boundary trichotomy

Date: 2026-08-26

## Verdict

Accept `GLD77` as an **exact exhaustive classification of the projective
rank-one boundary inside the three-dimensional leaf-sign raw-kernel block at
the fixed GLD72 fibre**.  Do not describe it as a classification of the full
projective boundary, a finite raw response lift, a survivor-open exclusion, a
strict-transform theorem, a source/interface globalization result, or a
resolution of Krenn--Gu.  The global conjecture remains **UNRESOLVED**.

## Evidence checked

The primary verifier reconstructs the `GLD74` `65 x 3` affine quotient and
extracts its three `65 x 35` homogeneous coefficient matrices.  It constructs
the raw leaf-sign central projector from all six actual raw permutation
matrices, proves that its intersection with the raw kernel has dimension
three, and checks the sign character on every resulting 79-coordinate raw
direction.

On a sparse exact basis `(u,v,w)`, the homogeneous response spans a
three-dimensional output block and has coordinate matrix

```text
[ u   i*u+(1+i)*v       -u ]
[ v   (1-i)*u-i*v       -v ]
[ w       -w             w ].
```

The verifier computes all two-minors over `Q(i)`.  Their Groebner basis is

```text
((u+v)(u-i*v), u*w, v*w).
```

The elementary split `w!=0` or `w=0` is exhaustive in projective space and
gives exactly the three reduced points `[0:0:1]`, `[i:1:0]`, and
`[1:-1:0]`.  For every point, the full `130 x 35` proportionality matrix has
rank `34`, the sparse vector spans its kernel, the leading first response has
rank one with nonzero first column, and the induced raw vector transforms by
the sign character.

The augmented standard-library audit is genuinely independent of the primary
implementation: it imports no project module, rebuilds the literal-Delta
permanent map and complete raw fibre, uses the reverse fibre-variable order,
constructs the three sparse sign basis vectors directly, checks the compressed
matrix by custom Gaussian arithmetic, and replays all three proportionality
systems.  It simultaneously replays the original `GLD74` Nullstellensatz
certificates and quotient fingerprint.

## Integrity repair inherited from the hostile GLD76 audit

A post-merge hostile audit of `GLD76` found two evidence-scope gaps, neither a
mathematical contradiction.  This successor branch repairs both before using
GLD76:

1. the universal-module verifier now constructs explicit tensor and raw
   intertwiners and checks the Gaussian specialization against the actual
   literal-Delta permanent map, all four full response maps, the fixed block,
   the target tensor, and the diagonal target response;
2. the representation verifier now checks leaf covariance on the complete
   `81 x 79` response maps and invariance of the full `81 x 13` fixed block,
   rather than only their mixed restrictions.

These repairs strengthen the verifier evidence without changing GLD76's
mathematical scope or the live proof topology.

## Load-bearing limits

1. Exhaustiveness is proved only after restricting to the raw sign block.
   The eight-dimensional trivial and 24-dimensional standard blocks, and
   mixtures among isotypic blocks, remain in the full projective boundary
   obligation.
2. The three points lie at infinity in the homogenized necessary mixed
   rank-one system.  They are not finite values of the 35 raw parameters and
   do not solve the full `68 x 4` universal affine incidence.
3. Leaf permutations act by a scalar sign on every one of the three lines;
   they do not identify the three projective points.
4. Root permutations that preserve the abstract fixed interface need not
   stabilize the GLD72 tensor line or the chosen literal-Delta fibre.  No
   fixed-fibre orbit identification is claimed.
5. A first-order strict-transform obstruction would still leave higher-order
   homogenizing arcs unless the missing geometric step were proved.
6. `GLD74` remains the exact finite-fibre exclusion at GLD72; `GLD77` neither
   weakens nor globalizes it.

## Recommended successor

Compute the moving strict transform at all three reduced sign points against
the four scale-fixed GLD75 survivor directions, with the raw pivot solve and
13-column quotient differentiated rather than frozen.  In parallel, seek an
exact isotypic or determinantal cover of boundary directions having trivial
or standard components.  Only a cover of every projective branch can support
a principal survivor-open exclusion.
