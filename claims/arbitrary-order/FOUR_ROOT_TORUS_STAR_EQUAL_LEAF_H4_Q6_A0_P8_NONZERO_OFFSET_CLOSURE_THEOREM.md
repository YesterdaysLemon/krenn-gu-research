# Four-root torus-star equal-leaf H4 Q6 a=0 P8 nonzero-offset closure (GLD104)

## Status

**Proved exact scoped characteristic-zero selected-minor composition
(`GLD104`).**

The exact primary and a separate no-primary-import composition audit pass.
Juniper and Mycelium then accepted immutable pre-promotion commit `75da0298`
from fresh detached checkouts, giving the required `2/2` external
consolidation.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Exact theorem statement

Work pointwise over the complex numbers on the normalized GLD88/F88
equal-leaf H4 offset chart `U88`.  Set `a=0` and retain

```text
Q6(p,q)=0,
H2(p)*Delta(p,q) != 0.
```

Here `B,C` are the GLD88 offsets, `H2=2p^2-2p+1`, and `Delta` is the full
GLD88 chart denominator product.  Let

```text
T0,T1,T2,T3,D0,Y0,Y1,X3
```

be the denominator-cleared numerators of the eight displayed actual ordered
seven-minors of the complete GLD71 syndrome.  On `D(Delta)`, each numerator
vanishes exactly when its corresponding rational minor vanishes.

The proved selected-minor proposition is

```text
Q6=T0=T1=T2=T3=D0=Y0=Y1=X3=0
and H2*Delta != 0
    => B=C=0.                                      (P8)
```

Consequently, because `rank M(G)<=6` makes every actual seven-minor vanish,
the one-way rank corollary is

```text
V(a,Q6) intersect D(H2*Delta) intersect {rank M(G)<=6}
    is contained in {B=C=0}.                       (RC)
```

No converse from the eight selected minors to complete syndrome rank is used
or claimed.

The field is stated as `C` to match the committed GLD101 pointwise theorem.
Although the identities are computed over `Q`, this theorem does not use that
observation to silently strengthen the field quantifier.

## 2. The eight actual minors

With zero-based row and column indices, the four `T` minors and `D0` are

```text
T0: rows (0,1,2,17,25,31,28), columns (0,1,3,4,6,7,8),
T1: rows (0,1,2,17,25,31,32), columns (0,1,3,4,6,7,2),
T2: rows (0,1,2,17,25,31,32), columns (0,1,3,4,6,7,5),
T3: rows (0,1,2,17,25,31,33), columns (0,1,3,4,6,7,8),
D0: rows (1,17,28,0,25,31,32), columns (0,1,2,3,4,5,6).
```

The remaining three use common rows

```text
(0,1,17,28,31,32,33)
```

and columns

```text
Y0: (0,1,2,3,4,5,6),
Y1: (0,1,3,4,5,6,7),
X3: (0,1,2,3,4,6,7).
```

The six GLD101 selectors are

```text
T0,T1,T2,T3,Y1,X3.
```

They form a strict subset of P8.  The extra `D0,Y0` equations are
load-bearing on the `R110` fibre.  Therefore this package proves no
six-selector proposition `P6`.

## 3. Selected equations imply the GLD101 norm gate

After setting `a=0`, substituting the normalized GLD88 offsets, and reducing
coefficientwise modulo `Q6`, each of the six actual selected equations is
supported on the ordered offset monomials

```text
m = (C, B, B*C, B^2, B^2*C, B^3)^T.
```

Write the six equations as `K(p,q)m=0`.  The primary freshly
reconstructs all six actual seven-minors from the pinned GLD71/GLD88 data,
rejects every constant or off-list offset monomial, rebuilds `K`, and obtains
the exact selector determinant signature

```text
c8b675268458576454cf3eeab5fe38c4ef468a2113c94febfd471c0cfc6d6431.
```

If `(B,C)!=(0,0)`, the first two coordinates `(C,B)` make `m` nonzero.
Thus six-equation vanishing makes `K` singular and forces `det K=0`.  This is
the selected-minor-to-norm direction needed by P8; it does not use a complete
rank hypothesis.

The exact GLD101 norm computation then gives the necessary support

```text
(p-1)*p*(p^2+1)*P*H2*R4*R8*R110 = 0,             (1)
```

where

```text
P  = p^2-p+1,
R4 = 5p^4-16p^3+30p^2-16p+5,
R8 = 64p^8-256p^7+580p^6-844p^5
     +946p^4-784p^3+388p^2-94p+13,
```

and `R110` is the hash-pinned degree-110 primitive factor in the tracked
GLD101 and R110 certificates.  Equation (1) is necessary only.  No root of
the norm is treated as a sufficient rank or physical point.

## 4. Exhaustive offset and factor cover

Every nonzero offset lies in the disjoint logical alternatives

```text
D(B)  or  (V(B) intersect D(C)).                  (2)
```

### 4.1 The C-open chart

On `B=0,C!=0`, each of the six actual selected minors is exactly `C` times
its recorded coefficient.  The portable arbitrary-`p` generic C-open
certificate proves that those six coefficient equations together with `Q6`
and the `H2*Delta` open generate the unit ideal.  Hence the second chart in
(2) is empty for a P8 point.

### 4.2 The B-open chart

On `B!=0`, put `C=B*t` and cancel the common nonzero factor `B`.  The eight
supports in (1) have the following exhaustive dispositions.

| support | exact disposition |
| --- | --- |
| `p=0` | the GLD102 B-open selected basis contains `a-1`; the present `a=0` specialization is empty |
| `p=1` | the GLD102 sixth-selector remainder is coprime to the first-five residual quadratic |
| `p^2+1=0` | the portable `T3,Y1,X3` unit leaf closes `p=i`; rational-coefficient conjugation closes `p=-i` |
| `P=0` | excluded because `P` is an explicit factor of `Delta` |
| `H2=0` | excluded by the declared `D(H2)` open, not claimed closed |
| `R4=0` | the portable exact `T3,Y1,X3` resultant/multiplication-determinant leaf is unit |
| `R8=0` | the portable five-row cofactor-kernel obstruction is contradictory |
| `R110=0` | the portable q-substitution certificate gives a unit ideal using all eight P8 actual minors |

No support in the GLD101 factorization is omitted.  The `P` and `H2`
supports are removed only by the written open conditions.  In particular,
this composition does not claim a theorem on either boundary.

Combining Sections 4.1 and 4.2 contradicts every nonzero-offset P8 point,
which proves (P8).  The rank corollary then follows only in the direction

```text
rank M(G)<=6 => every actual seven-minor vanishes => P8 => B=C=0.
```

## 5. Certificate and audit boundary

The tracked composition certificate pins 29 load-bearing child files by
LF-normalized SHA256, including the GLD101 and GLD102 theorem/checker/audit
surfaces and every portable leaf certificate/primary/audit package.  It also
pins the exact eight-factor signatures, the offset cover, the P8 selector
surface, and the factor dispositions.

The primary verifier performs the fresh actual-minor/determinant replay in
Section 3 and checks the complete composition seam.  Its bounded pre-freeze
run succeeded in 81.702 script seconds.  The independent composition audit
imports no repository verifier, checks the 29 source pins and child JSON
directly, reconstructs every factor signature, validates the offset-cover
truth table, extracts the GLD102 constants through a restricted AST, and
independently audits the GLD101 source-level coefficient-matrix construction.

The ordinary audit command is

```text
python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_p8_nonzero_offset_closure.py
```

It is intentionally not advertised with `python -I`: on the reference
Windows host, isolated mode cannot see the installed user-site SymPy.  The
audit's zero-repository-import boundary is enforced by its AST and focused
tests rather than by a command that does not run in the recorded environment.

The immutable candidate commit and tree were

```text
75da0298a535888e7a84257b7bfd6a556a3267b2
86fae29848c52c7ccd3236c84e156aedb3f02b78.
```

Commons request `kgc_01M1BXKGZ8F86B6XWK1J6Q3DMF` received exact scoped
acceptances from Juniper (`kgc_01M1BXV18D8NZQ22BDEXDXJWTP`) and Mycelium
(`kgc_01M1BYMJPC3VD2N7ENK20RXE3B`).  Mycelium additionally replayed the
primary and all ten focused tests from a Git-free clean export.  These are
external consolidation receipts for this scoped theorem, not evidence for a
wider or global conclusion.

## 6. Nonclaims and remaining obligations

This theorem does not prove or assert:

- `P6`, because the R110 certificate uses `D0` and `Y0` with nonzero
  multipliers;
- emptiness or inadmissibility of the endpoint `B=C=0`;
- a physical incidence theorem or removal of the downstream `Omega` open;
- arbitrary `a`, the full `E31=0` wall, or the other affine pivot patches;
- `Delta=0`, `H2=0`, another chart, gauge, component, or source branch;
- another root number, graph order, or a global case cover;
- the GLD83 pulled-back Fitting ideal, source integrability, target
  attachment, graph lifting, or global gluing; or
- resolution of the global Krenn--Gu conjecture.

Those are separate proof obligations.  The exact scope here is the normalized
`a=0`, `Q6=0`, `D(H2*Delta)` nonzero-offset closure and no more.
