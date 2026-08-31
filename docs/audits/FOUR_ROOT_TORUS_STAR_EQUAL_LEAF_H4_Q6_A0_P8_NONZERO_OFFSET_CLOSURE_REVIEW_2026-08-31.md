# GLD104 a=0 P8 nonzero-offset composition hostile review

## Verdict

**Verdict: PASS for the exact scoped GLD104 P8 composition.**

The reviewed package gives an exact composition for the selected-minor
proposition

```text
a=0, Q6=T0=T1=T2=T3=D0=Y0=Y1=X3=0,
H2*Delta != 0  =>  B=C=0.                         (P8)
```

It also gives the one-way corollary with `rank M(G)<=6`, because complete
syndrome rank at most six makes all eight actual seven-minors vanish.  The
immutable candidate received exact fresh-detached acceptances from Juniper
and Mycelium before this promotion.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. Exact scope audited

The ambient field is `C`, matching the committed GLD101 pointwise statement.
The chart is the normalized GLD88/F88 equal-leaf H4 offset chart `U88`; the
parameters satisfy `a=0`, `Q6(p,q)=0`, and `H2(p)Delta(p,q)!=0`.  The offsets
are `B,C`.

P8 uses the actual ordered GLD71 seven-minors `T0,T1,T2,T3,D0,Y0,Y1,X3`.
The six GLD101 selectors `T0,T1,T2,T3,Y1,X3` are a strict subset.  This is
not a P6 theorem: `D0,Y0` are load-bearing on the R110 support.

The rank statement is only a corollary in the safe direction

```text
rank M(G)<=6 => all actual seven-minors vanish => P8 => B=C=0.
```

No converse from selected-minor vanishing to complete-syndrome rank is used.

## 2. Selected equations really reach the norm gate

The most dangerous composition gap was that GLD101's public headline is
rank-scoped, whereas P8 is a selected-minor proposition.  Merely citing the
headline would not justify feeding P8 into its norm factorization.

The primary closes that gap directly.  It reconstructs the six
actual minors from the hash-pinned GLD71 and GLD88 sources, reduces their
coefficients modulo `Q6`, rejects constant terms and every offset monomial
outside

```text
C, B, B*C, B^2, B^2*C, B^3,
```

and forms the six-by-six coefficient matrix `K(p,q)`.  If the six equations
vanish then `K m=0` for

```text
m=(C,B,B*C,B^2,B^2*C,B^3)^T.
```

On a nonzero offset, the first two coordinates make `m` nonzero.  Thus `K`
is singular.  The reconstructed determinant has the exact GLD101 signature

```text
c8b675268458576454cf3eeab5fe38c4ef468a2113c94febfd471c0cfc6d6431.
```

This supplies the selected-equation-to-norm direction without assuming rank.
The separate composition audit imports no repository verifier and checks the
same bridge structurally from the pinned GLD101 source, including the selector
names, monomial columns, support rejection, coefficient-matrix construction,
and determinant signature.

## 3. Offset cover is exhaustive and reversible

Every nonzero offset lies in exactly one of the logical alternatives

```text
D(B)  or  (V(B) intersect D(C)).
```

On the second chart, the six selected equations are `C` times their recorded
coefficients.  Since `C!=0`, the portable arbitrary-`p` C-open unit certificate
closes the chart.

On `D(B)`, the substitution `C=B*t` and cancellation of the common factor
`B` are reversible.  No statement is inferred on `B=0` from that chart; it is
handled separately above.

## 4. Eight-factor routing

GLD101 supplies only the necessary support

```text
(p-1)*p*(p^2+1)*P*H2*R4*R8*R110=0.
```

The composition routes every factor and does not treat any factor root as a
sufficient rank point.

| factor | reviewed disposition |
| --- | --- |
| `p` | GLD102's selected B-open basis contains `a-1`; at `a=0` it is unit |
| `p-1` | GLD102's `T3` remainder is coprime to the first-five residual quadratic |
| `p^2+1` | exact `p=i` portable unit leaf plus rational-coefficient conjugation for `p=-i` |
| `P` | outside the chart because `P` divides `Delta` |
| `H2` | outside the explicitly declared `D(H2)` open |
| `R4` | exact `T3,Y1,X3` multiplication-determinant/resultant unit leaf |
| `R8` | exact five-row cofactor-kernel contradiction |
| `R110` | exact q-substitution unit certificate using all eight P8 minors |

The `p=0,1` uses are selected-minor subcases extracted from GLD102, not an
invalid invocation of GLD102's rank-only headline.  The R110 route is the
reason P8 cannot be weakened to P6 in this package.

## 5. Denominators and boundaries

On `D(Delta)`, each denominator-cleared numerator vanishes exactly when its
rational minor does.  The factor `P` is removed only because it is explicitly
a divisor of `Delta`; `H2` is removed only by the written open condition.
Neither boundary is claimed closed.

The package does not cancel across `Delta=0`, `H2=0`, `B=0`, or `C=0`.
The two offset charts and all eight norm supports are written explicitly,
making an omitted branch detectable by the focused tests.

## 6. Evidence boundary

The composition certificate hash-pins 29 child owner, certificate, primary,
audit, and review files.  The primary reconstructs the selected-minor bridge
and validates the child-certificate seam.  The independent composition audit
does not import the primary or a child verifier: it reads the pinned JSON,
rebuilds factor signatures and the offset-cover truth table, extracts the
two GLD102 constants through a restricted AST, and separately checks the
GLD101 coefficient-matrix source contract.

External consolidation used immutable commit
`75da0298a535888e7a84257b7bfd6a556a3267b2` and tree
`86fae29848c52c7ccd3236c84e156aedb3f02b78`.  Commons request
`kgc_01M1BXKGZ8F86B6XWK1J6Q3DMF` received Juniper receipt
`kgc_01M1BXV18D8NZQ22BDEXDXJWTP` and Mycelium receipt
`kgc_01M1BYMJPC3VD2N7ENK20RXE3B`, reaching `2/2`.  Mycelium also executed
the exact primary and ten focused tests from a Git-free clean export.

The prospective promotion commit must itself receive independent exact-diff
review before GLD104 is treated as live.  A failed source pin, selector
mismatch, unhandled factor, selected/rank direction error, or widened
field/scope is a stop condition.

## 7. Required nonclaims

The theorem does not prove:

- P6;
- exclusion or inadmissibility of the endpoint `B=C=0`;
- physical incidence emptiness or removal of the downstream `Omega` open;
- arbitrary `a`, full E31, another pivot patch, or a boundary fibre;
- the GLD83 Fitting pullback, source integrability, target attachment, graph
  lifting, or global gluing;
- another root number, order, component, or a global exhaustive cover; or
- the global Krenn--Gu conjecture.

Subject to those fences and the accepted external consolidation, the exact
scoped GLD104 theorem passes hostile review.
