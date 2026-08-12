# Hostile review: all-bridge beta-three route-port pairing

## Verdict

**PASS as an exact characteristic-zero refinement of the rank-three
extremal-sparse least-core branch.  No P0--P3 finding remains.**

The reviewed theorem is frozen at commit
`fcfb9af0d42b9f70d745a08aa09a705c1c23b5b1`.  Its exact evidence pins are:

| Artifact | SHA-256 | Git blob |
|---|---|---|
| theorem | `399aa81ee9ebee3f51d30e4d467c6ae492d8820a4d3acd1341debcd833ef7f52` | `b6b156515626ee2089b16e11c0030337645b2b96` |
| primary verifier | `eab670097df9986c238973d3c1f830a0c22184a13c90da15921712b0e143b27e` | `bedaa3e1fa66c8d48c6dd3f06c6931027cb8b005` |
| independent audit | `441aec91bc846b168e8ce947fffb5f0a1aa1b252dfc2483604bb3c12c6d95128` | `83b29d863650d60e34cf1881406ee8d2bf286272` |

The theorem does not exclude either rank-three sparse kernel.  It composes
the route parity already owned by `A4` with the nonzero weighted port
partition owned by `U7I`.  In `Q/Q`, every odd route pairs the same singleton
port at its two quartic endpoints, so the two endpoint contributions are the
same nonzero full perfect-matching monomial.  In `Q/C^2`, the four odd routes
pair four singleton ports, while the unique even route has disjoint
complementary doubleton endpoint ports.  Their edge-inclusive cofactor sums
are nonzero exact negatives.

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Claim reconstruction

The load-bearing chain is:

1. `A4` supplies a globally least connected bipartite matching-covered core
   with `beta=3`, an extremal sparse quartic site, exactly four perfect
   matchings, and exactly the `Q/Q` or `Q/C^2` suppressed route kernel.
2. `U7I` identifies every incident port with the perfect matchings using its
   core edge and gives the nonzero weighted identity

   ```text
   C_f=z_f haf(Z^e[S-endpoints(f)])
      =sum_(M in P(p,f)) lambda(M) != 0.
   ```

   The endpoint-edge factor `z_f` is part of the contribution.
3. On a route with edge indicators `t_1,...,t_l`, every internal degree-two
   vertex gives `t_i+t_(i+1)=1`.  Thus an odd route has endpoint states `00`
   or `11`, while an even route has endpoint states `01` or `10`.
4. Therefore the two endpoint port sets coincide on every odd route and are
   disjoint complements on every even route.  This recurrence, rather than a
   bounded graph census, carries the arbitrary route-length quantifier.
5. At the sparse quartic site, four nonempty ports partition four perfect
   matchings, so they are four distinct singletons.  In `Q/Q`, all four odd
   routes carry those singletons to the opposite quartic site.
6. In `Q/C^2`, the four odd routes carry the same four singletons to the two
   cubic sites.  At each cubic site the remaining port is the endpoint of the
   unique even route, hence the two even-route ports are complementary
   doubletons.
7. The two even-route contributions sum over all four perfect matchings and
   therefore sum to `h(S)=0`.  Each is nonzero by `U7I`, so they are exact
   negatives.

## Novelty and ownership

The route-state recurrence is already implicit in the `A4` route-parity
classification.  The new theorem is the exact `A4 + U7I` interface: it turns
route parity into equality or complementarity of named matching-port sets and
then into edge-inclusive weighted cofactor identities.  It does not claim
that route alternation itself is new, and it does not move ownership of the
five-kernel rank-three census, the `Q/Q` versus `Q/C^2` exhaustiveness, or the
least-core port theorem.

## Adversarial checks

| Attack | Result |
|---|---|
| Odd-route parity might identify only endpoint states, not global matching sets | **Rejected.** Ranging the pointwise equality `t_l=t_1` over all perfect matchings gives equality of the two port sets. |
| Even-route endpoint ports might overlap or omit matchings | **Rejected.** Every perfect matching has exactly one endpoint edge, so the ports are disjoint and cover `PM(A)`. |
| Four ports at the sparse site might not be singleton | **Rejected.** They are four nonempty parts of a partition of four perfect matchings. |
| The `Q/C^2` even-route ports might have sizes other than two | **Rejected.** At each cubic site the two odd-route singleton ports remove exactly two matchings; the remaining even-route port is the complementary doubleton. |
| Port nonvanishing might follow from topology alone | **Rejected.** It is imported from global leastness through the `U7I` edge-inclusive cofactor identity. |
| Equality of odd-route contributions might imply equality of bare deletion hafnians | **Rejected explicitly.** The cofactor contribution includes its endpoint-edge weight.  The exact control has equal weighted port sums but bare deletion hafnians `-3` and `1`. |
| Exact negatives on the even route might require algebraic independence | **Rejected.** Complementarity partitions the four full matching monomials and their total is the single relation `h(S)=0`; no independence is used or proved. |
| The finite scripts might carry arbitrary route length | **Rejected.** They test exact subdivisions; the written alternating recurrence carries the universal length statement. |
| The scalar controls might be simultaneous all-bridge witnesses | **Rejected explicitly.** They contain only one pure weighted core and omit the other colours, active decks, mixed cuts, and target equations. |
| Port pairing might already give target attachment or exclude a kernel | **Rejected.** No mixed fibre is identified and both least-zero controls realize the asserted patterns. |

## Computational evidence and independence

The primary verifier

```powershell
python -B claims/arbitrary-order/verify_all_bridge_bipartite_least_core_beta_three_route_port_pairing.py
```

builds physical route subdivisions, represents perfect matchings as tuples of
edges, checks the unique alternating restriction route by route, reconstructs
the `Q/Q` and `Q/C^2` ports, and computes exact rational full-matching sums.
It exercises three length-varied fixtures of each topology and separately
replays the displayed `Q/Q` and `Q/C^2` least-zero controls, including all
`141` and `51` proper supported even minors respectively.

The independent audit

```powershell
python -B claims/arbitrary-order/audit_all_bridge_bipartite_least_core_beta_three_route_port_pairing.py
```

imports neither repository code nor the primary verifier.  It uses an
edge-bitmask matching oracle and independently exhausts `189` labelled simple
`Q/Q` subdivisions and `675` labelled simple `Q/C^2` subdivisions over odd
route lengths through seven and even lengths through six.  It separately
recomputes exact hafnians of induced vertex masks, the two least-zero
controls, the edge-inclusive Laplace terms, the complementary even-port sums
`2,-2`, and the unequal bare-deletion countercontrol.

The implementations differ in matching representation, enumeration topology,
and weighted-control route.  Their agreement is independent exact bounded QA
for the displayed mechanisms; neither script is an arbitrary-order proof or
a witness search.  Both scripts PASS, and Ruff `0.16.2` reports no findings.

## Scope firewall

```text
simultaneous balanced all-bridge branch:                    ASSUMED;
globally least bipartite pure core:                         IMPORTED;
beta=3 extremal sparse quartic site:                        ASSUMED;
Q/Q or Q/C^2 kernel and N=4:                               IMPORTED EXHAUSTIVE;
odd-route endpoint port sets coincide:                     PROVED;
even-route endpoint ports are disjoint complements:        PROVED;
Q/Q paired singleton contributions agree and are nonzero:  PROVED;
Q/C^2 odd-route singleton pairing:                         PROVED;
Q/C^2 even-route complementary doubletons:                 PROVED;
Q/C^2 edge-inclusive doubleton sums are exact negatives:   PROVED;
bare deletion hafnians equal or opposite:                  NOT PROVED / NOT CLAIMED;
paired ports algebraically independent:                    NOT PROVED / NOT CLAIMED;
paired ports occupy distinct mixed target fibres:          NOT PROVED / NOT CLAIMED;
target attachment or deeper incidence:                     NOT PROVED;
either Q/Q or Q/C^2 excluded:                              NOT PROVED;
scalar controls are simultaneous all-bridge witnesses:     FALSE / NOT CLAIMED;
universal extraction/gluing:                               NOT PROVED;
global Krenn--Gu conjecture:                                UNRESOLVED.
```

The smallest honest successor must add genuinely mixed-target or
deeper-incidence data to the now-exact port pairing.  Repackaging the same
pure route partitions cannot supply an exclusion.
