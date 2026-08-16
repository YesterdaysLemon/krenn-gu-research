# Arbitrary permanent `P_6` co-two equality-five full-extension exclusion

## Status

This note proves an exact characteristic-zero exclusion for the
**equality-five co-two branch of `P_6 -> Delta_3`**.  In any exact weighted
restriction, every omitted pair `{a,b}` satisfies

```text
dim B_ab >= 6.                                                (1)
```

Equivalently, no omitted pair with `dim B_ab=5` can extend through the
other four source modes.  Consequently all fifteen complementary co-two
product sensors of a hypothetical `P_6` restriction have rank at most

```text
binomial(6,2)-3 = 12.                                        (2)
```

The proof composes the reviewed active-support synthesis, the complete
based-frame orbit classification, permanent monomial covariance and
source-mode symmetry, and six pointwise endpoint packages.  No endpoint is
used outside its exact based-frame orbit.

This is **not** an unrestricted `P_6 -> Delta_3` nonrestriction theorem.
The simultaneous mixed-target incidence when every `dim B_ab>=6` remains
open.  The endpoint packages are specific to `P_6`; no exclusion for
`P_r`, `r!=6`, is inferred.  Arbitrary-order permanent nonrestriction and
the global Krenn--Gu conjecture remain **UNKNOWN/UNRESOLVED**.

## 1. Exact statement

Let `K` be a field of characteristic zero.  For each source mode
`t in {0,...,5}`, choose an ordered independent triple

```text
z^(t)_0,z^(t)_1,z^(t)_2 in K^6.                            (3)
```

Write `P_6` for the unnormalized permanent tensor.  An exact weighted
restriction to `Delta_3` means that some `lambda_0,lambda_1,lambda_2 in K^*`
satisfy

```text
P_6(z^(0)_(c_0),...,z^(5)_(c_5))
  = lambda_c,   if c_0=...=c_5=c;
  = 0,          otherwise.                                 (4)
```

For an omitted pair `{a,b}`, put

```text
U_a=span{z^(a)_0,z^(a)_1,z^(a)_2},
U_b=span{z^(b)_0,z^(b)_1,z^(b)_2},
B_ab=U_a U_b subset (Z_6)_2.                               (5)
```

Let `A_S` be the complementary product sensor from the co-two sensor
theorem.

### Theorem 1 (`P_6` equality-five full-extension exclusion)

If (3)--(4) hold, then for every omitted pair `{a,b}`,

```text
dim B_ab>=6,                 dim A_S<=12.                  (6)
```

In particular, there is no exact `P_6 -> Delta_3` extension whose chosen
omitted pair has product dimension five.

## 2. Frozen reviewed dependencies

This is a proof-composition theorem.  The load-bearing mathematics remains
in the nine owning packages below.  Every package consists of a theorem,
primary verifier, genuinely separate audit, and hostile review.  The
commits and SHA-256 values below pin the exact reviewed text after
normalizing checkout `CRLF` to Git-style `LF`.

```text
package       commit                                     theorem
support       843b4f459790b88499646e7dd79c8280633d622e   9399ccb4286583a1f1e90bd7025e706b3de47c652214bb1e8b7c8f6ba986a6d5
based         dc6eca42605086fbffba4059f87f4702e68c9a54   cff044ea8e89d504f4ecf9c62ca55dfd5361cd54f5cb85083b09aed8b834d677
transport     513100ac7cbf0f97e4710a7e32a4fa35b6cc96e4   b1762f22813e5b749ff0c81da6c6ce5e9b8e95601662d87cb21835aaf63c3da0
triangle      2e6c74d36fda60d6b3428047325c5398053b247c   02c87a0811777b0a833598d9217fbf117613f8b7089a21c0ae6d4ed6964648b9
star-mixed    3a53f19a789baa055c3b951efdacc505b2a69117   c9daabb0c288f6fb54c9fb209fd5d2e341118efe0c181442899757063ea0b66d
fixed-e0      82ab1090076bcd765c89b463214eb7714618722e   8ae57e0032b046303260bcef9dc0ae56635dc9aeaa9af096d609079523d65dde
star-pure     43c85d6dc3cea0e6e47ed0a20701c173598ab31e   e0b069b11107f006650954d339ef8e6e9465c2b492059450236f5238b2567cbc
fixed-e1      9e27d6e4efc73eccc27e306408d618c5fcb831c3   a7ee294986e79c7f1bc38e0b2ce0dc1a5ee09d230f2fd06796846d677a361acf
fixed-e2      cf55f7bbe889dbd2239302543fd0c92b11edbbe6   cf79c02d6c45359f1f26aefad4e4c0ab9715a57ada26b1e57d18a772022b764e

package       primary                                    audit                                      review
support       175543a58c352b05ff2f13ccf1b75ec3b9080b11bd0a879a1649391481cfd779  2f8272cea197fac253fe0b4f6e09091fffd6d0be161a3e0ff5f0bc72dfcc4047  be13f69678f36b6db79277af66a85144e0b334c14535dcdd29573ab10fb53f03
based         8560c80c85abc643a7591161295c22bf052589bcfc0529ca2a067a452cb1baf1  123ee95416724fa80a537fd3fd2eec216f461d9f2e2d88268ccb82aed3758fc8  f1610e9bbcc4065ac24a1e0cd7f81ddaf989bca5d4026ae2a23bd2ff7a5f680f
transport     e37a2e98447f6058496a3487d0a01f498b331e730cc3b01c72fc6750cec5838e  1ec63510db2e03a58d7502aae7160310b4f324bfad0547bb1e86a05a2602a740  3cfdc0b2d7ceb5af59247fd87d6469a8bb5b4c6f03ff2c077b05abda866ef5ec
triangle      fdbbe2711c471ebf0453398f722412371fd4091b0593a5fddd70ae4b6508d31a  9b15c86c1c0b232ea3d622a9868b95cacb135da59534d9da97175a55236f23ce  3d30a06354ea4f929ddd015436b5fd94ac3e05f133743019fb87a1783fadafcd
star-mixed    3ae361503755db59fec772a042ceb319b31ca869958758bca55083a0b2de5ecc  0add6399e692361bae467a0b6ca361b6e6c521c34f230b28e7babc36fd200371  35ece859d0da216d3e60008410feb109eea531dceceff442a53e1f3c8ac2480d
fixed-e0      9979fbc9528c8d059f5a1802a2487a5da3d4b0ce651947c0d7ea6480b5050c35  7cf90a8a3e3498cc707fea3ec5e273b90e10372da04e3c8262b8c1bf74c72f21  be668be16f2a9df74a122ce34d8adf5f177a35d4acc9a1596adf558bccbda5f5
star-pure     36c285c44bfa4d4c61fc084773f1604e398ebac94e1aa8fd72e6bf5a8e1e6d49  4fcfbf910701eb28c1913ab9fc39a6921c689c536ee12f42cadf6a35b0b51163  f324e6741a0ad66a53849a6298a266e745b358c275523620036d5765dd60d6bc
fixed-e1      24a84558c6d842bc5d034dfcc6494c60a03c75cf8e5f47e2e63a6c3ccfeed2f8  ef9cc36cbe0ad27dfeafc1e24ee0a717cde17e9e2ff6684ffc1981567585b4cc  0b3775df217207a36538ffaf02d2e483bbe5c08193574b2d3ecc8873b81f9287
fixed-e2      a4f68fb8ae8d5d977c99875c2e2298c2417e29a408b81f1345c9bde990477a91  7d0c24e338524ed04ef387a0c31977a821c73dbd70e31f3ba2d390a8a6809589  55cd1aa465a250af3107139931a21685802d66291a400b28bb92cfa9e9803374
```

The `support`, `triangle`, `star-mixed`, and `fixed-e0` primary/audit
hashes above include the mechanical newline-portability repair in this PR:
only checkout `CRLF` is normalized to `LF` before comparing frozen text.
The expected Git-style hashes, theorem statements, proof logic, and review
bytes are unchanged.  Section 7 audits this repair separately.

The executable manifest in the primary and audit gives every full path.
The imported statements, with their scopes unchanged, are:

1. equality `dim B_ab=5` in an actual restriction forces active support
   four and unbased type `(3,1)`, `(4,1)`, or `(4,2)`;
2. the exact based-frame classification has ordered orbit counts `1,4,3`,
   or `1,2,3` after the two omitted modes may be exchanged;
3. extendibility and nonextendibility are invariant under the common
   coordinate monomial map, common colour permutation, independent nonzero
   colour scalings in the displayed pair, and exchange of that pair; and
4. the six endpoint packages exclude the displayed triangle, mixed star,
   fixed `e=0`, pure star, fixed `e=1`, and fixed `e=2` frames.

## 3. From an arbitrary omitted pair to a based `r=4` frame

Assume (4) and choose any omitted pair `{a,b}` with

```text
dim B_ab=5.                                                (7)
```

Permuting the six source slots moves `a,b` to slots `0,1`.  This operation
preserves (4): `P_6` is symmetric in its six arguments, and a colour word is
constant before the slot permutation exactly when it is constant after it.

The equality-five support theorem now supplies three facts:

```text
|supp(U_a+U_b)|=4;
the actual colour bases form a pair-level Delta_3-admissible frame;
the underlying unbased type is (3,1), (4,1), or (4,2).     (8)
```

Move the four active coordinates to `x_0,...,x_3`.  Every coordinate
permutation or nonzero scaling used by the `r=4` classification extends to
`K^6` by acting as the identity on the two inactive coordinates.  It is
therefore one common coordinate monomial map in the sense of the transport
theorem.  The based classification applies to the actual ordered colour
bases, not merely to the two underlying three-planes.

## 4. Exhaustive orbit-to-endpoint table

The complete ordered-orbit list and its quotient by omitted-mode exchange
give exactly the following six extension classes.

```text
unbased type   ordered invariant(s)   exchange class     reviewed endpoint

(3,1)          unique                 unique             triangle 012

(4,1)          k=2, k=1               mixed             displayed star 013
(4,1)          k=3, k=0               pure              pure star 014

(4,2)          e=0                    e=0                displayed fixed 013
(4,2)          e=1                    e=1                fixed e=1 025
(4,2)          e=2                    e=2                fixed e=2 024.       (9)
```

For `(4,1)`, exchange sends `k` to `3-k`; hence it pairs `k=2` with
`k=1` and `k=3` with `k=0`.  For `(4,2)`, exchange preserves `e`, so all
three values need separate endpoints.  The repeated numerical labels are
not global identifiers: `(4,1),k=1,025` is transported to the mixed star
`013`, whereas `(4,2),e=1,025` is the distinct fixed-`e=1` endpoint.

Every equivalence used to reach the rightmost column is one of the exact
operations in the covariance/transport theorem.  In particular, nonzero
target weights remain nonzero.  Therefore each pointwise endpoint exclusion
transported through (9) excludes its entire exchange class.

## 5. Proof of Theorem 1

Suppose (7).  Section 3 puts the actual based pair in one of the six rows of
(9).  The owning endpoint theorem in that row excludes an exact completion
through the other four source modes.  Transport is reversible, so it also
excludes the original pair.  This contradicts (4).  Hence `dim B_ab!=5`.

The co-two sensor theorem already gives `dim B_ab>=5`.  Since dimensions are
integers,

```text
dim B_ab>=6.                                               (10)
```

The pair was arbitrary, so (10) holds for all `binomial(6,2)=15` omitted
pairs.  The same co-two theorem gives

```text
dim A_S+dim B_ab <= binomial(6,2)+3 = 18.                 (11)
```

Combining (10)--(11) yields `dim A_S<=12`, proving (6).

## 6. Exact boundary

```text
field:                                                     CHARACTERISTIC ZERO;
source tensor:                                             P_6;
target:                                                    WEIGHTED Delta_3;
equality-five active support and unbased types:             EXHAUSTIVE/PINNED;
based-frame ordered orbit counts:                          1,4,3;
classes after omitted-mode exchange:                       1,2,3;
full extension classes in the orbit-to-endpoint table:     SIX;
all six endpoint classes:                                  EXCLUDED;

dim B_ab=5 for any omitted pair of an exact P_6 restriction: EXCLUDED;
dim B_ab>=6 for all fifteen omitted pairs:                  PROVED NECESSARY;
dim A_S<=12 for all fifteen complementary sensors:          PROVED NECESSARY;

simultaneous feasibility inside the dim B_ab>=6 residual:   OPEN;
unrestricted P_6 -> Delta_3:                               UNKNOWN;
P_r equality-five exclusion for r!=6:                      NOT CLAIMED;
arbitrary-order permanent nonrestriction:                  UNKNOWN;
global Krenn--Gu conjecture:                               UNRESOLVED.       (12)
```

## 7. Replay and portability audit

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_p6_cotwo_equality_five_full_extension_exclusion.py
python -I claims/arbitrary-order/audit_arbitrary_permanent_p6_cotwo_equality_five_full_extension_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_p6_cotwo_equality_five_full_extension_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_p6_cotwo_equality_five_full_extension_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_p6_cotwo_equality_five_full_extension_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_p6_cotwo_equality_five_full_extension_exclusion.py
```

The focused validation also replays all eighteen upstream primary/audit
scripts.  For the eight legacy scripts repaired here, the hostile review
checks the diff mechanically: primary hash helpers replace only raw bytes by
`bytes.replace(b"\r\n",b"\n")`, and Git-object audits apply that same
normalization only to the working-tree copy before comparing it with the
frozen blob.  Expected digests and all mathematical checks are unchanged.

The primary verifier imports the exact based-classification and transport
replays, re-derives all characteristic-zero catalogs and both group actions,
checks all eight ordered representatives, and exhausts the six endpoint
classes.  The independent audit imports neither the primary, the upstream
verifiers, nor SymPy.  It uses a standalone finite-group implementation and
rational row reducer on frozen raw catalogs and integral frames, checks the
same six-class cover, and independently replays the `P_6` sensor arithmetic.
Both scripts pin every reviewed dependency byte.  They guard proof
composition and transcription; the written implications and the nine
reviewed packages prove the theorem.
