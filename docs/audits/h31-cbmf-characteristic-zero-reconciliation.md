# H31 chart-boundary marked-fibre characteristic-zero reconciliation

Date: 2026-08-10 UTC  
Frozen base: `2a0bc5899e9edfcfd2add0f52f46827c47a54344`  
Disposition: owner-authorized bounded audit, outcome A  
Global Krenn--Gu status: **UNRESOLVED**

Frozen source paths and blobs:

```text
P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md  73ade81380b483a81f52ebda4f14443f815ebb32
verify_p5_h31_component_chart_boundary_marked_fibre.py      0366d5a7233ba3f4fcc1427b66b7a72d17c44330
audit_p5_h31_component_chart_boundary_marked_fibre.py       799b2c1098910bd10596f359ae88f384fbd3a229
derive_p5_h31_chart_boundary_marked_fibre_elimination.py    b2ed4c8096d22da626141922a5df926fac853d43
```

## Scope and conclusion

This audit reconciles only the theorem, primary verifier, independent
modular audit, and elimination generator for the H31 component-chart
boundary marked fibre.  The four source blobs were frozen before the
audit.  No unrelated claim or global status was reconsidered.

The evidence supports precise outcome A:

- equation (9) has **13 irreducible projection-closure components**, in
  counts `4,2,3,4` for `q=0,1,2,3`;
- the proof uses **16 factor-certificate records**: 13 generic
  rational-basis records, one for each component, plus 3
  exceptional-basis records;
- after two explicit overlap assignments, those records form 16
  disjoint locally closed proof pieces on the saturated incidence;
- two residual loci of the projection closure are not certificate
  pieces because exact row identities force `d_1=0` there; and
- all four exact characteristic-zero saturated
  selected-minor ideals are the unit ideal.

Thus neither fourteen nor sixteen is the number of irreducible
projection components.  Sixteen is the correct certificate-record
count.  The correction uses these distinct terms rather than replacing
one numeral blindly.

## Objects kept distinct

An **irreducible projection component** below means an irreducible
closed component of one elimination ideal in theorem equation (9).  A
**locally closed proof piece** is the part assigned to one record after
component intersections, closure-only loci, and exceptional parameter
values are separated.  A **generic rational-basis record** is a
residual-factor identity in the verifier's ordinary rational kernel
basis.  An **exceptional-basis record** is a second, denominator-free
kernel calculation on the same projection component at a pole of that
ordinary basis.  A **verifier certificate record** is one such exact
factor identity, not a new projection component.

## Projection components

Writing ideals in `Q[A,R,t0,t1,t2,t3]`, the 13 components are:

| label | `q` | projection-component ideal |
| --- | ---: | --- |
| C00 | 0 | `<R,t1,t2,t3>` |
| C01 | 0 | `<A-1,t1,t2,t3>` |
| C02 | 0 | `<t0,t2,t3,R*t1+A-1>` |
| C03 | 0 | `<R,t0,t2,t3>` |
| C10 | 1 | `<A+1,R*t0+1,t1,t2,t3>` |
| C11 | 1 | `<A-1,t0,t1,t2,t3>` |
| C20 | 2 | `<t0,t1,t2,t3>` |
| C21 | 2 | `<R,t1,t2,t3>` |
| C22 | 2 | `<A-1,t1,t2,t3>` |
| C30 | 3 | `<R*t0+1,t3-A-1,t1,t2>` |
| C31 | 3 | `<t0,t3,t1,t2>` |
| C32 | 3 | `<R,t3,t1,t2>` |
| C33 | 3 | `<A+1,t3,t1,t2>` |

The primary verifier mechanically intersects the component ideals for
each `q` and reduces both directions against equation (9).  Each listed
ideal is visibly a coordinate or graph prime after eliminating its
displayed linear/graph variables.  This gives the irreducible counts
`4+2+3+4=13` without treating a record flag as evidence.

## Component-to-record coverage table

Throughout the table, theorem normalization already requires `A!=0`.
"Generic" and "exceptional" describe the kernel basis used, not the
mathematical status of the theorem.

| `q` | component | verifier record | assigned locally closed conditions | basis | selected minor; residual factor |
| ---: | --- | --- | --- | --- | --- |
| 0 | C03 | `R0_t1_axis` | `R=t0=t2=t3=0`, `t1!=0`, `A!=1` | generic | `(2;0237)`; `d_0` |
| 0 | C00 | `R0_t0_axis` | `R=t1=t2=t3=0`; intersections are assigned here | generic | `(2;0367)`; `-d_1` |
| 0 | C02 | `R_nonzero_A_nonone` | `t0=t2=t3=0`, `R!=0`, `A!=1`, `t1=(1-A)/R` | generic | `(2;0237)`; `d_0` |
| 0 | C01 | `A1_axis_generic` | `A=1`, `t1=t2=t3=0`, `R!=0`, `R*t0!=-1` | generic | `(2;0267)`; `-2R*d_0` |
| 0 | C01 | `A1_axis_exception` | same component, `R*t0=-1` | exceptional | `(0;0457)`; `R*d_1` |
| 1 | C11 | `A1` | `A=1`, `t0=t1=t2=t3=0`, `R!=0` | generic | `(0;0357)`; `-(1/R)*d_1` |
| 1 | C10 | `Aminus1` | `A=-1`, `R*t0=-1`, `t1=t2=t3=0` | generic | `(0;0457)`; `R*d_1` |
| 2 | C20 | `t0_zero` | `t0=t1=t2=t3=0`, `R!=0`; the `A=1` overlap is assigned here | generic | `(2;0237)`; `d_0` |
| 2 | C21 | `R0_axis` | `R=t1=t2=t3=0`; the `t0=0` intersection is assigned here when `R=0` | generic | `(2;0367)`; `d_1` |
| 2 | C22 | `A1_axis_generic` | `A=1`, `t1=t2=t3=0`, `R!=0`, `t0!=0`, `R*t0!=1` | generic | `(2;0267)`; `-2R*d_0` |
| 2 | C22 | `A1_axis_exception` | same component, `R*t0=1` | exceptional | `(2;0267)`; `-2R*d_0` |
| 3 | C31 | `t0_zero` | `t0=t1=t2=t3=0`, `R!=0`; the `A=-1` overlap is assigned here | generic | `(2;0237)`; `-d_0` |
| 3 | C32 | `R0_axis` | `R=t1=t2=t3=0`; component intersections are assigned here when `R=0` | generic | `(2;0367)`; `d_1` |
| 3 | C33 | `Aminus1_axis_generic` | `A=-1`, `t1=t2=t3=0`, `R!=0`, `t0!=0`, `R*t0!=-1` | generic | `(0;0457)`; `-R^2*t0*d_1` |
| 3 | C33 | `Aminus1_axis_exception` | same component, `R*t0=-1` | exceptional | `(0;0457)`; `R*d_1` |
| 3 | C30 | `nonzero_t3` | `R*t0=-1`, `t3=A+1`, `t1=t2=0`, `A!=-1` | generic | `(0;0457)`; `R*d_1` |

There were two overlaps in the earlier record predicates.  At `q=2`,
`A=1,R!=0,t=0` lay in both `t0_zero` and `A1_axis_generic`; the latter
now explicitly requires `t0!=0`.  At `q=3`, `R=0,t=0` lay in both
`t0_zero` and `R0_axis`; the former now explicitly requires `R!=0`.
The factor identities themselves do not change.  These refinements
make the 16-piece locally closed cover disjoint.

## Closure-only loci

Two loci in the Zariski projection closure, within the standing `A!=0`
parameter domain, are not saturated binary incidence points:

1. For `q=0`, `A=1,R=0,t0=t2=t3=0,t1!=0`, exact symbolic
   recomputation gives
   `t1*d_1 + row_0(M_0) - t1*row_4(M_0) - row_10(M_0)=0`.
   Hence `M_0 z=0` implies `d_1(z)=0`.
2. For `q=1`, `A=1,R=0,t0=t1=t2=t3=0`, the `d_1` coefficient row
   vanishes identically.

Neither locus meets `A*d_0*d_1!=0`.  This is the exact bridge from the
closed projection ideals to every certificate record; checking sixteen
factor identities alone would not have supplied it.

## Exact selected-unit-ideal replay

The function `selected_program()` had no caller before this audit.
The ordinary verifier ran the four projection eliminations and the
factor ledger, while a report key ambiguously described those runs as
"unit or ledger" runs.  The verifier now calls all four programs by
default (and exposes a clearly labelled bounded local-check opt-out):

```text
python verify_p5_h31_component_chart_boundary_marked_fibre.py \
  --selected-unit-ideals --selected-timeout 900
```

A clean serialized replay of the single committed generator used Python
3.13.14, SymPy 1.14.0, and WSL
Singular 4.3.2.  Each exact characteristic-zero saturated obstruction
ideal returned the one-element basis `basis[1]=1`:

| `q` | products | program bytes | program SHA-256 | stdout SHA-256 | wall time |
| ---: | ---: | ---: | --- | --- | ---: |
| 0 | 32 | 497904 | `0be03968acd44b69c706a11ebd579ec3bfaa4b120d4a3bcbdc2447eb2669d0b0` | `ab65be10b7be9fffe5fcda4702106bee2eaeb92ba5ac497390bdf189c8da8ac3` | 390.966 s |
| 1 | 16 | 73826 | `bdc29924e58fa9df2470bd67bee4b2b882b1453d73f03bc6d4bc1aa8606278a2` | `31a4d4c78e1711e7ba7658970bf1a60cd7d921b1e98d2c65756310fd01ea5e2f` | 50.822 s |
| 2 | 24 | 358105 | `b312ad32fe43d04a9b064b15b6bd7fee7cd1b6b040f0a92f982d0a6cfa135cd8` | `0c83968825218a7548820003141ebadadd5c439bb03a107babff9b25548aa663` | 248.929 s |
| 3 | 24 | 224117 | `1976c82821aa762b9c7cc2899ecf7cff9eecc6b3515295242d73c38b8ba08548` | `6ac6f9037d8ffc9fcda78251e145e39aa422f66e1691b6b2a34d1ad89b26e53d` | 122.913 s |

The exact stdout payload for each run was its `Q=q_SELECTED` marker,
`BASIS_SIZE`, `1`, and `basis[1]=1`.  The first bounded `q=0` attempt
timed out during local symbolic program construction before Singular
ran; it changed no tracked file and is not counted as evidence.

## Independence and evidence boundary

A fresh scientific reviewer on 2026-08-10 UTC returned outcome-A
**ACCEPT** for exactly this bounded H31 package.  The reviewer independently
decomposed equation (9),
reconstructed the permanent and mixed matrices from scratch in SymPy,
checked all 16 residual identities and pure-column witnesses, found the
two overlaps and two closure-only loci, and then independently audited the
raw outputs and hashes replayed from `selected_program()`.  The reviewer did
not accept the primary report flags or
the F5/F7 audit as evidence of characteristic-zero exhaustiveness.

The existing F5/F7 script remains useful independent modular QA.  Its
report now states explicitly that it does not prove characteristic-zero
exhaustiveness.  The exact cover above concerns only this bounded H31
component-chart divisor.  It does not close other H31 components, an
arbitrary-order bridge, the prize graph, or the global conjecture.
