# Self-review of the `m=3` separated-singleton pole localization

## Verdict

**PASS as an exact localization theorem; not an independent mathematical
review and not a global-resolution audit.**

The review covered the theorem, SymPy primary replay, standard-library
no-import audit, maintained frontier, arbitrary-order index, and theorem
ledger entry in the candidate tree on branch

```text
codex/kg-s2q-physical-localization-20260812.
```

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Load-bearing mathematical audit

The review checked the following points directly.

1. After `C_empty=1`, the `m=3` target equation has exactly three remaining
   pair coefficients and three singleton columns.  Each singleton column is
   linear in a different nonroot projective factor, with complementary pair
   coefficient line bundle.
2. Function-field rank four of the complete sensor forces function-field
   rank three of these singleton columns.  Hence the rational pair
   coefficient triple is unique.
3. Every rank-drop point has a minimal dependence support of size one, two,
   or three.  For image dimensions `r_u`, pair-sum dimensions `s_uv`, and
   total dimension `s`, the corresponding nonempty strata have codimensions

   ```text
   r_u,              s_uv-1,              s-2.
   ```

   The projectivized-kernel maps used in the proof are injective on the
   stated minimal-support opens because the scalar dependence relation is
   unique there.  The three strata exhaust the rank-drop locus.
4. A prime divisor supports rank drop only when `r_u=1`, `s_uv=2`, or `s=3`.
   Conversely each equality produces a divisor unless an earlier minimal
   support already does, so the named union is exact.
5. Away from rank drop, a three-row minor is a unit at the generic point of
   a divisor.  Cramer's rule in local line-bundle frames makes all three
   coefficients regular there.  On the smooth product of projective spaces,
   regularity at every prime divisor extends a rational line-bundle section
   globally.
6. The global sections of the three complementary pair bundles are exactly
   bilinear edge blocks.  At `m=3` there is no higher even deck component and
   no higher Euler--hafnian recurrence.  Thus a regular physical target
   incidence would reconstruct a six-vertex graph.

No step infers physical realizability from column degrees alone.  The last
step is applied only after the common-shore matching formulas are assumed.

## 2. Sharpness and predecessor compatibility

The review replayed three exact separated-column pole controls.

```text
rank-one image:        common minor factor x_0;
pair-plane image:      common factor x_0 y_1-x_1 y_0;
common three-space:    trilinear determinant det[x,y,r].
```

Each control has a global target section and a genuine rational Cramer pole.
A fourth arrangement with image dimensions `(2,2,2)`, pair sums `(3,4,3)`,
and total span four has maximal-minor gcd one.

All eight S2M controls were reconstructed at the selected-column level.  In
every case the chosen singleton column has image dimension one, so the new
theorem does not falsely regularize them.  S2P remains the separate theorem
that excludes their physical common-shore realizations.

The sharp controls in the new theorem are abstract separated-column systems.
They are not claimed to satisfy the common-shore matching formulas or the GHZ
target.

## 3. Evidence and independence

The primary replay uses SymPy matrices, symbolic maximal minors, exact gcds,
Cramer identities, rational multidegrees, and a coordinate-subspace census.

The independent audit imports neither SymPy, the primary verifier, nor
repository modules.  It uses a separately written sparse integer-polynomial
exterior product, exact `Fraction` row reduction, cleared-denominator Cramer
identities, a singular-point pole check, and an independently written
coordinate-subspace census.

At review time:

```text
primary replay:                    PASS;
independent python -I audit:       PASS;
coordinate signatures:            PASS (15130 in both implementations);
Python compilation:                PASS;
Ruff 0.16.2:                       PASS;
JSON parse:                        PASS;
git diff --check:                  PASS.
```

The finite coordinate census checks the dimension ledger and fixed controls;
the arbitrary-subspace exhaustion is the written minimal-support proof.

## 4. Upstream six-vertex evidence boundary

The physical regular-stratum corollary invokes the repository's accepted
computer-assisted six-vertex theorem.  A direct call to

```text
python claims/finite/n06/verify_six_vertex_final.py
```

did not replay in this fresh worktree because its large `tmp/` CNF and DRAT
artifacts are intentionally not present.  The failure was a fail-closed
`FileNotFoundError`, not a contradictory solver result.

Accordingly this review does **not** claim a fresh replay of that historical
certificate chain.  The divisor-localization theorem is independent of the
certificate; only the final statement that the regular physical stratum is
empty uses the accepted six-vertex result.

## 5. Scope firewall

The review rejects every stronger reading below.

```text
the three exceptional low-span strata are empty:             NOT PROVED;
every m=3 target incidence has a pole:                        NOT PROVED;
the eight S2M controls exhaust the exceptional strata:        FALSE;
the sharp pole controls are physical GHZ incidences:          FALSE;
the localization applies unchanged to m>=4:                  FALSE;
higher Euler--hafnian recurrences are controlled:             NOT PROVED;
the all-balanced rank-drop branch is excluded:                NOT PROVED;
the universal S2 full-sensor branch is closed:                NOT PROVED;
the global Krenn--Gu conjecture is resolved:                  FALSE.
```

The exact advance is that arbitrary `m=3` pair poles are no longer an
unstructured Cramer phenomenon: they are confined to rank-one, pair-plane,
or common-three-space singleton incidence.  Those three strata and every
higher balanced order remain the next obligations.
