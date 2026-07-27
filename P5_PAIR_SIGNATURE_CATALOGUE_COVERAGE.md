# `P_5` pair-signature catalogue coverage over `C`

## Status

This is an exact finite-assisted local theorem over `C`.

Let

```text
r_0,...,r_4 in C^3
```

span `C^3`, and suppose that for every distinct pair `p,q`,

```text
span(r_p,r_q) contains at least one of e_0,e_1,e_2.     (1)
```

Record:

1. the exact zero/nonzero support of each row; and
2. for each of the ten row pairs, exactly which coordinate points
   `e_c` its span contains.

Every such complex support/pair-incidence signature occurs in the
6,495-pattern catalogue obtained by enumerating five-row configurations
over `F_5`.

The finite field is only a device for listing the signatures.  The
coverage conclusion is over `C`; it does **not** assume that an arbitrary
complex coefficient configuration can be reduced modulo five.

This theorem makes that catalogue safe for support and pair-incidence
case splits in the hypothetical restriction

```text
P_5 -> Delta_3.
```

It does not certify higher-subset incidences or solve the coefficient
equations by itself.

## Abstract necessary conditions

The verifier introduces Boolean variables for:

```text
x_(p,c) = row p has a nonzero c-coordinate,
y_(pq,c) = e_c belongs to span(r_p,r_q).
```

Every complex configuration satisfying (1) obeys the following clauses.

1. Each pair has at least one and at most two coordinate incidences.
2. A coordinate row `r_p proportional to e_c` forces `y_(pq,c)` for
   every `q`.
3. If neither row is `e_c`, membership of `e_c` forces the two
   projections onto the other coordinate plane to have compatible
   supports.  A determinant with exactly one supported monomial is
   forbidden.
4. Two rows supported in one coordinate plane and jointly using both
   axes span that plane whenever their span contains a coordinate point.
5. Projective plane closure holds: if

   ```text
   e_c in span(r_a,r_b) intersect span(r_a,r_d)
   ```

   and `r_a` is not `e_c`, then `span(r_b,r_d)` also contains `e_c`
   unless `r_b,r_d` are the same coordinate point.
6. The support matrix has structural rank three, a necessary condition
   for the five rows to span `C^3`.

These conditions deliberately over-approximate complex realizability.

## Exhaustion and the 303 apparent exceptions

The `F_5` enumeration produces:

```text
2,556 unordered spanning row multisets
6,495 labelled support/pair-incidence signatures.
```

The verifier blocks those 6,495 signatures and searches the abstract
necessary-condition CNF.  It finds exactly 303 further Boolean patterns.
For every one of them, all ten pair incidences are the same singleton:

```text
y_(pq,c) = true for one fixed c and every p != q.       (2)
```

They form eight orbits under `S_5 x S_3`, with labelled orbit sizes

```text
3, 15, 15, 30, 30, 60, 60, 90.
```

Every pattern in (2) is impossible for spanning rows.  If three rows
`r_a,r_b,r_d` were independent, then

```text
span(r_a,r_b) intersect span(r_a,r_d) = span(r_a).
```

Both planes contain `e_c`, so `r_a` would be proportional to `e_c`.
Repeating the same argument with `r_b` would make `r_a,r_b` proportional,
contradicting independence.  Thus no three rows are independent and the
five-row matrix has rank at most two.

After adding the 303 exclusion clauses, the final CNF has:

```text
150 variables
9,099 clauses
```

CaDiCaL returns `UNSAT`.  Its 3,349,683-byte DRAT proof is independently
accepted by forward `drat-trim`:

```text
s VERIFIED
```

## Independent audit

`audit_p5_pair_signature_catalogue_coverage.py` independently:

1. rebuilds the `F_5` catalogue and its 6,495 labelled pair signatures;
2. checks that the 303 records are distinct and outside the catalogue;
3. uses a separate Smith-normal-form row-lattice implementation to
   verify that every recorded local determinant system forces all ten
   `3 x 3` row minors to vanish;
4. reconstructs the eight `S_5 x S_3` orbits and their sizes;
5. checks the CNF and DRAT hashes and the successful forward replay.

The audit returns:

```text
"verified": true
"catalogue_pair_patterns": 6495
"outside_exclusions": 303
"outside_orbits": 8
"all_outside_patterns_share_one_axis": true
"reason_counts": {"forced_rank_two_map": 303}
```

## Verification

Run:

```text
python verify_p5_pair_signature_catalogue_coverage.py \
  --records tmp/p5_pair_signature_catalogue_coverage_verified.json \
  --cnf tmp/p5_pair_signature_catalogue_coverage.cnf

python audit_p5_pair_signature_catalogue_coverage.py
```

The independently replayed artifact hashes are:

```text
records
3ca857f513f2a2d02193b48953d339d3472b82e576bd91885b1510a545d4c6d4

CNF
fdd8f2184d9efa50db1634a0c774009c17c60b236e113b4c80dac794cb31a093

DRAT
fcdf1cdce1df1b68579c7404272635a30ecc13f02fc8615c1dd04ff9b4c7afe2
```

## Boundary

The result certifies only support and **pair** incidence.  A finite-field
representative may have special higher-subset ranks, so those data must
not be imported into a complex proof without an additional coverage
argument.

The current safe continuation uses the 6,495 patterns with only the
pair quotas from the complex kernel Hall theorem, then checks the
remaining permanent coefficient equations over `C`.
