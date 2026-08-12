# Review of the normalized pair-control common-shore pullback reduction

## Verdict

**PASS at the frozen three-file core, with no P0--P3 finding.**

Reviewed commit and exact parent/base:

```text
c3c41ae7592e6869bc4b1cad5c8032aeeb1ec61e
9a679a7af6726bbba32df0258ea2fb4e4655d675
```

Reviewed raw Git-object SHA-256 values:

```text
reduction: b471309a81395a7b3ca8fd8bf89a8aed4558e1e59ec3bcd0d7ba0776a7009a31
primary:   c840bebd5c44b25ce3b87f9a2cb784e3062058e696e63d41b4b5ac2b945b7592
audit:     1d35858f92530e7c632420e568f5f62455146896461282ceefdbdc2f0856e3cb
```

The reduction Git blob is

```text
c9147173f38fcb885cd69dbb55df82f1d7557aed.
```

The review was read-only.  The worktree remained clean and the reviewed core
bytes were not edited.  The final integrated candidate must retain these
bytes, add only the review and maintained navigation, and pass the complete
candidate-tree floor.

The result is an exact necessary reduction for eight particular `m=3`
ambient controls.  It proves neither residual emptiness nor common-shore
nonrealizability.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. Eight-control projection audit

For a control with pivot colour `a in {1,2}`, let `q` be the other nonzero
colour and project each root space onto the span of its `a`- and `q`-basis
vectors.  Direct reconstruction of the two outside, three `x`-endpoint, and
three `y`-endpoint controls confirms all of the following.

1. The pivot singleton contribution at `(a,a,a)` survives as one pure tensor.
2. Every correction is supported at `(0,0,1)`, `(0,1,0)`, or `(1,0,0)` and
   dies under the projection.
3. This includes the correction terms of the mixed `x_(1,2)` and `y_(1,2)`
   controls; there is no exceptional eighth-control branch.
4. The pivot empty coefficient was overwritten to zero, the colour-zero GHZ
   coefficient dies, and exactly the `q`-diagonal GHZ coefficient survives.

Thus all eight controls have the same projected coefficient pattern.  The
proof does not identify the original ternary controls with that projection;
it uses the projection only as a necessary test for a putative realization.

## 2. Common-shore functoriality audit

The S2N singleton formula is a sum of three tensor products using one fixed
triple of root--root blocks.  Applying the root projections to every factor
therefore gives the same formula on the binary quotient spaces.

Likewise, each term in the empty companion is a tensor product of three cross
blocks, summed over the six root-to-nonroot bijections.  Root projection
commutes termwise with that six-term permanent.  Consequently, the three
vanished quiet-colour singleton slices give three vectors in the kernel of
the displayed binary shared-factor map, while the surviving empty coefficient
is their polarized permanent.

The resulting conditions are correctly stated only as necessary:

```text
transverse pure tensor in the binary image;
quiet pure tensor as a permanent of three binary kernel vectors.
```

No converse is asserted.  Even a binary solution would still need a lift
through every ternary singleton and empty coefficient.

## 3. Sharp boundary audit

The reduction explicitly rejects the shortcut that three zero singleton
slices force their empty coefficient to vanish.  In one-dimensional root
spaces with all three root--root blocks equal to one, the kernel is the plane

```text
u_1+u_2+u_3=0.
```

For the displayed integer matrix

```text
[  0   3   3 ]
[  1   3   2 ]
[ -1  -6  -5 ],
```

every column lies in that plane and the ordinary permanent is exactly `-48`.
The example supports only the stated logical boundary.  It is not a binary
solution of the full residual because no transverse-image condition is
imposed.

## 4. Evidence and independence

The primary replay uses SymPy polynomial coefficients to reconstruct all
eight S2M matrices, applies the root projections, and checks every surviving
singleton and empty coefficient.  It separately checks the six-term sharp
permanent.

The independent audit imports neither SymPy nor repository code.  It uses an
independently written integer sparse-support representation, reconstructs all
eight controls, and enumerates the six permanent permutations directly.

At the reviewed commit:

```text
primary replay:              PASS (8/8);
independent python -I audit: PASS (8/8);
Python compilation:          PASS;
Ruff 0.16.2:                 PASS;
exact diff and clean status: PASS.
```

The scripts replay the displayed finite coefficient reductions.  The written
tensor-product argument supplies the general functoriality bridge.

## 5. Scope firewall

The review rejects every stronger reading below:

```text
the binary residual is empty:                              NOT PROVED;
one of the eight controls has a common-shore realization:  NOT PROVED;
one of the eight controls is nonrealizable:                 NOT PROVED;
a binary survivor necessarily lifts to ternary data:        NOT PROVED;
all realized target incidences fail a retained pair jet:    NOT PROVED;
shared physical variables imply lattice coupling:           NOT CLAIMED;
a physical graph, witness, or counterexample is built:      NOT CLAIMED;
the all-balanced rank-drop branch is excluded:              NOT PROVED;
the Krenn--Gu conjecture is resolved:                       FALSE.
```

The exact advance is one common necessary residual for all eight ambient
controls, plus a sharp reason that the singleton-zero layer alone cannot
decide it.  The physical-variable and support-difference-lattice notions stay
separate throughout.

## 6. Final assessment

No mathematical, scope, independence, or portability defect was found in the
frozen core.  Promotion is appropriate after exact navigation integration,
complete candidate-tree validation, final exact-head repinning, and
published-head plus merged-main verification.  Global Krenn--Gu remains
**UNRESOLVED**.
