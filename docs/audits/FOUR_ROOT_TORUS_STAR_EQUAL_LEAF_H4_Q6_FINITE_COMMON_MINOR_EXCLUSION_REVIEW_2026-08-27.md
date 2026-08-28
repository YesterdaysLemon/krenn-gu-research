# GLD95 hostile review: H4 Q6 finite common-minor exclusion

## Disposition

**Accepted as an exact, narrowly scoped closure of the finite residual.**
The package proves that the two GLD92 six-minors cannot vanish together on
`D(Delta)` inside the written GLD88 rational family `F88`, including every
resultant-content component that lies on the old GLD88 pivot boundary
`P6=0`.  It does not prove that arbitrary points of `H4 intersect V(Q6)`
lie in `F88`, and it does not change the global status: Krenn--Gu remains
**UNRESOLVED**.

The reviewed conclusion is

```text
V(Q6,F28,F31) intersect D(Delta) = empty,

B intersect V(I_7(A)) intersect F88 intersect V(Q6)
  intersect D(Omega Delta) = empty.
```

Here `Delta=(p-q)(p+q-1)P L1 L2 e`, and `F88` means the displayed rational
formula family, not the whole H4 divisor.

## Exact evidence inspected

The primary verifier
`claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_finite_common_minor_exclusion.py`
reconstructs the committed GLD71 `37 x 9` syndrome and GLD88 family and
checks:

1. all `111` common block-kernel identities, giving rank at most six on
   `F88`;
2. the exact GLD92 six-minors with columns `(0,1,3,4,6,7)` and rows
   `(0,1,2,17,25,28)` and `(0,1,2,17,25,31)`;
3. the common denominator `P^2 e^2`, the factor shapes
   `N28=(p-q)^3F28` and `N31=d0(p-q)^3F31`, and the exact resultant hashes;
4. the resultant-content factorization and squarefree p-eliminant;
5. the exact generic unit-minor cover on `H0,H1,H3,H4,H5,H6`;
6. the direct `H2` fibre computation, where `H2=LC_q(Q6)` and the generic
   division denominator `H2^47` is invalid;
7. all five retained content fibres at `p=0,1,-1,1/2`, including their
   Groebner bases, quotient-algebra unit minors, old `P6=0` identities, and
   `Delta`/leaf-determinant unit checks; and
8. the zero-dimensional coefficient-ideal certificate ruling out vertical
   a-lines.

The independent audit
`claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_finite_common_minor_exclusion.py`
imports none of the primary, GLD71 builder, or GLD88 family builder.  It
directly evaluates copied sparse supports for rows
`{0,1,2,3,4,17,19,25,28,31,32}`, uses its own explicit formula copy, and
repeats the determinant, resultant, H2, generic-unit, and content-unit
checks.  Its support digest is pinned as
`24cdba204347947370076c621b167f5aac617b9731d30cd22e25504630cf87d3`.
For the content witnesses it takes a separate numerator/denominator gcd
route in `Q[q]`, directly checks old `P6=0`, and verifies every `Delta` factor
is a unit.

Both scripts are intended to be replayed with the bounded research runner;
ignored run logs are diagnostic only, while the tracked scripts and hashes
are the durable evidence surface.

## Adversarial checks

### Quantifier and family boundary

The GLD90 pivots contain `Q6`, so GLD90 does not force the GLD88 Schur family
at a general Q6 point.  GLD95 therefore states `F88` in the hypothesis and
never says that it closes the whole H4 Q6 boundary.  Any wording that drops
the `F88` qualifier is an overclaim and is rejected.

### Exhaustive residual decomposition

The exact `a`-resultant has total degree `99`, degrees `(56,53)` in `(p,q)`,
and the pinned `srepr` hash
`fd85a520800c5bda4d93bc66d3ddf4be0fc16fdb1e65281be1a76cc23a3f9c8d`.
After q-division by `Q6`, the denominator is exactly `H2^47`, and the
primitive content is

```text
(1/2)(p-1)(p+1)(2p-1)p^4 P^9.
```

The squarefree p-eliminant has degree `36` and hash
`86eca671802beaf8cb2cb1f3755494b24ece747f3bc3efb8129cf2263f8c6743`; its
factors are exactly `p-1,p,H0,P,H1,H2,H3,H4,H5,H6`.  This decomposition is
what makes the branch cover exhaustive; no modular scan is promoted to a
proof.

### H2 denominator correction

`H2=2p^2-2p+1` is the q-leading coefficient of `Q6`.  A generic quotient
field calculation would introduce `H2^47` in the denominator and cannot be
specialized to `H2=0`.  GLD95 performs the specialization first: `Q6` has
q-degree three, the specialized resultant has q-degree `50`, and the exact
gcd is `d0=p+q-1`.  Hence the entire true H2 common locus is outside
`D(Delta)`.  The apparent quadratic q branch from generic division is
explicitly marked a division artifact.

### Generic units and content units

Every generic branch of `H0,H1,H3,H4,H5,H6` has an exact unit six-minor with
the fixed columns `S`; the theorem document records all ten row/hash pairs.
The p-content fibres have exact lexicographic Groebner bases.  Removing only
the boundary components `q=0` at `p=0` and `q=1` at `p=1`, the remaining five
components are covered by the displayed quotient-algebra units.  These
checks handle all complex roots of each q modulus, not numerical samples.

### Old P6 boundary and denominator safety

On each of the five retained content components, the old GLD88 pivot

```text
P6 = det M[(0,1,2,17,19,32),S]
```

is exactly zero.  The new row sets use additional sparse supports and give a
unit determinant anyway.  Independent `Q[q]` gcds show both unit numerator
and denominator are coprime to each modulus.  The same direct specialization
checks all six factors of `Delta` and the leaf determinant, so no content
component is silently discarded by a denominator or by the old pivot chart.
The `P=0` content factor is outside `D(Delta)` and remains governed by GLD89.

### Rank and center argument

The 111 block-kernel identities give three independent kernel vectors and
therefore syndrome rank at most six.  A unit six-minor gives rank exactly
six and makes those three vectors the complete kernel.  Every compatible
center then has proportional rows, contradicting `det(C) != 0` in
`D(Omega)`.  In the common-minor case, the exhaustive residual cover gives a
unit six-minor on every surviving decomposition branch, so the common case
does not remain.

### Vertical resultant blind spot

The coefficient ideal generated by `Q6` and every a-coefficient of `F28`
and `F31` is zero-dimensional, has q eliminant
`q^6(q^2-q+1)^4`, and contains `((p-q)P)^6`.  Thus a resultant-zero fibre
where both polynomials vanish identically in a is outside `D(Delta)`.  This
closes the usual vertical-line gap before the unit branch cover is applied.

### Independence

The audit is materially different at the determinant layer: it uses direct
sparse-support loops, an independently written formula copy, a separate
quotient-field gcd implementation, and a `Q[q]` numerator/denominator gcd
route.  It shares the fixed sparse supports and written F88 formulas as
mathematical input, and it does not independently reprove the GLD75/GLD86
incidence bridge or GLD88's common-kernel lemma.  Calling it an independent
proof of the complete theorem would be inaccurate; it is an independent
exact arithmetic audit of the finite-residual closure.

## Accepted residuals and non-claims

| item | review verdict |
| --- | --- |
| `F88 intersect V(Q6) intersect D(F28)` | excluded by exact unit minors and the rank/kernel bridge |
| `F88 intersect V(Q6) intersect D(F31)` | excluded by exact unit minors and the rank/kernel bridge |
| `V(Q6,F28,F31) intersect D(Delta)` | empty by exhaustive exact decomposition and unit cover |
| old `P6=0` content fibres | explicitly included and covered; all five have `P6=0` |
| `H2=0` fibre | direct gcd is `d0`; excluded by `D(Delta)` |
| arbitrary `H4 intersect V(Q6)` outside `F88` | not covered |
| `P=0` | outside `D(Delta)`; upstream GLD89 scope |
| GLD83 Fitting pullback | not computed |
| other charts/components/gauges/source branches | open |
| global Krenn--Gu conjecture | **UNRESOLVED** |
