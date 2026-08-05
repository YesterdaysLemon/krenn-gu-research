# Order-14 `C6+C8` 119-orbit certificate

> **Scope correction.** This artifact exactly replays its stored CNF and
> DRAT proof, but its late minimum-activity clauses were certified only
> under a three-connected support hypothesis that was not explicit in the
> final CNF. Do not cite the unqualified 119-orbit exclusion as a theorem.
> The repaired, explicitly connectivity-conditioned result is
> `FOURTEEN_VERTEX_C6_C8_121_ORBITS_KAPPA3_CERTIFICATE.md`.

## Scope

This is a finite computer-assisted theorem inside the order-14
`C6+C8` equality architecture. It is not a proof of the full family or
of the Krenn--Gu conjecture.

No support exists whose pinned first singleton perfect matching belongs
to any of these 119 census orbits:

```text
0--6
100--143
171--173, 179, 182, 185, 187--189
200--218, 220--225, 227, 232, 233, 238, 247, 269
300--327
```

The other 209 first-factor orbits remain SAT in this rule checkpoint.

## The 119th orbit

The certified predecessor excludes the same list with orbit 6 omitted.
A direct continuation on orbit 6 finds 38 full-only/one-extra
cycle-factor cores. Every core and its three-connected minimum-activity
certificate is independently replayed.

The minimized activation premises have size one through four. Stabilizer
transport gives four clauses per core, for 152 new clauses of width two
through five. Appending them to the predecessor makes orbit 6 UNSAT.
A separate factor-fork continuation also reached UNSAT, but it is not
needed by the promoted proof.

The resulting 559-variable, 124,663-clause global CNF has SHA-256

```text
5162bd3a83a0f730f2860059d39731ae439fe8dc085be3498339ba1c843ce300
```

## Selector audit and UNSAT proof

An exact solve under all 328 selector assumptions reports the 119-orbit
list above as UNSAT and its 209-orbit complement as SAT.

Appending one positive clause containing exactly the 119 UNSAT selectors
gives a 124,664-clause conditioned CNF with SHA-256

```text
8ca5d7cf43a81fe2d102e00ddf4e3f779fd0c8f55091fe749775bd23aa712b88
```

Kissat generated a 307,363-byte DRAT proof with SHA-256

```text
9e9e20ae8b271ac5caea452f90cef99ffcbdebd0eb5c036966dcb014e5d85bc4
```

Independent forward `drat-trim` verification returned `s VERIFIED`.

## One-command replay

With the pinned repository runtime (`requirements.txt`) installed, run:

```text
python verify_fourteen_vertex_c6_8_119_orbits.py
```

The verifier first replays the complete 118-orbit predecessor. It then
reconstructs the 38 new certificates and 152 clauses, audits all 328
selectors, compares the conditioned DIMACS sequence exactly, and reruns
`drat-trim`. Its final output is
`tmp/fourteen_vertex_c6_8_119_orbits_final_verified.json` and contains
`"verified": true`.

## Boundary

This closes 119 of 328 first-factor orbits in one remaining order-14
factor family. The other 209 `C6+C8` orbits, the other unresolved
factor types, and the global conjecture remain unresolved.
