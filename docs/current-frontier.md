# Current frontier of the Krenn–Gu conjecture programme

## Status, scope, and authority

The global Krenn–Gu conjecture is **UNRESOLVED**. No complete
characteristic-zero proof and no exact counterexample to the original global
statement is known in this repository.

This is the canonical maintained research map. Its initial consolidation was
reconstructed through PR #82 at merged commit
`367eef49e5917a0f71594dce4c18a608850cdd6a`; subsequent owning advances are
incorporated here as committed. Owning theorem documents are authoritative for
proofs, assumptions, and evidence. This page records how those claims fit
together; it does not replace them or strengthen their scope.
The [theorem ledger](../catalog/theorem-ledger.json) is a partial claim/evidence
index, not the proof graph, and its empty `dependencies` arrays mean “not
recorded.”

Except where an owner says otherwise, the live symbolic trunk below is over
`C` or characteristic zero. Generic/function-field theorems do not include
excluded divisors, projective boundaries, or arbitrary points without a proved
specialization argument.

For even `n >= 6` and `d >= 3`, the conjecture asks whether block matrices
`W_ij in C^(d x d)` can satisfy

```text
T_W(a_1,...,a_n)
  = sum_(perfect matchings M) product_({i,j} in M) W_ij[a_i,a_j]
  = sum_(c=0)^(d-1) product_v 1_(a_v=c).
```

The programme concentrates on the ternary restriction. Every local P5, P6,
or P7 result remains only a local proof leaf until a theorem extracts and
glues that leaf from every hypothetical global witness.

## Live proof topology

Arrows are typed. A `boundary` arrow names a surviving obligation; it is not a
proof of the target. A `specialization` arrow applies only under the owner's
hypotheses.

```mermaid
flowchart TD
  G0["Hypothetical complex witness<br/>global conjecture UNRESOLVED"]

  S1["Balanced complete-deck sensor<br/>PROVED reduction"]
  S2E["Cramer--Euler pair-pole gate<br/>PROVED exact refinement"]
  S2J["Finite pair differential-flatness gate<br/>PROVED exact refinement"]
  S2K["Target-column replacement-minor gate<br/>PROVED exact refinement"]
  S2L["Projective-minimal pair-jet gate<br/>PROVED exact refinement"]
  S2M["Normalized full-row pair controls<br/>PROVED compatibility boundary"]
  S2N["m=3 common-shore image<br/>PROVED iff / ambient separator"]
  S2O["Eight controls -> one binary residual<br/>PROVED reduction"]
  S2P["Binary transverse residual<br/>PROVED empty; eight controls EXCLUDED"]
  S2Q["m=3 separated singleton poles<br/>LOCALIZED to three low-span strata"]
  S2R["m=3 singleton-span annihilators<br/>ROOT TORUS EXCLUDED by P3 rank"]
  S2S["m=3 boundary annihilators<br/>COMMON BINARY P3 QUOTIENT classified"]
  S2T["m=3 common-three-space components<br/>MULTI-BOUNDARY / beta-zero / rank-collapse"]
  S2U["m=3 full joint cross rank<br/>ONE DIAGONAL MONOMIAL ROOT EDGE"]
  S2V["m=3 sparse block permanent<br/>SOURCE-ALIGNED EXCEPTIONAL ROW EXCLUDED"]
  S2W["m=3 sparse block permanent<br/>ALL TWO-SOURCE EXCEPTIONAL ROWS EXCLUDED"]
  S2X["m=3 common-three-space<br/>FULL JOINT CROSS RANK EXCLUDED"]
  S2Y["m=3 common-three-space<br/>JOINT CROSS RANK EIGHT EXCLUDED"]
  S2Z["m=3 common-three-space rank seven<br/>SINGLE ROOT BLOCK EXCLUDED"]
  S2AA["m=3 common-three-space<br/>ALL JOINT RANK SEVEN EXCLUDED"]
  S2AB["m=3 common-three-space<br/>ALL SINGLE ROOT BLOCKS EXCLUDED"]
  S2AC["m=3 common-three-space rank six<br/>SHARED-FACTOR DERIVATIVE EXCLUDED"]
  S2AD["m=3 transverse rank six<br/>BETA-ZERO / RANK-TWO BOUNDARY"]
  S2AE["m=3 transverse rank six<br/>ALIGNED RANK-TWO EXCLUDED"]
  S2AF["m=3 common-three-space<br/>ALL JOINT RANK SIX EXCLUDED"]
  S2AK["m=3 rank-five support-two<br/>ALL INVOLVED ROW PROFILES EXCLUDED"]
  S2AL["m=3 rank-five support-one<br/>HIGHER INVOLVED ROW RANKS EXCLUDED"]
  S2AM["m=3 rank-five transverse two-root<br/>ALL SUPPORT PROFILES EXCLUDED"]
  S2AN["m=3 rank-five Hilbert--Burch (1,1,1)<br/>REPEATED-COORDINATE LOCALIZED"]
  S2AO["m=3 rank-five Hilbert--Burch (1,1,1)<br/>REPEATED PATTERN (s,s,t) ONLY"]
  S2AP["m=3 rank-five Hilbert--Burch (1,1,1)<br/>REPEATED-COORDINATE CHART EXCLUDED"]
  S2AQ["m=3 rank-five Hilbert--Burch (1,1,1)<br/>ALL-COORDINATE-DISTINCT CHART EXCLUDED"]
  S2AR["m=3 rank-five Hilbert--Burch (1,1,1)<br/>COMPLETE PROFILE EXCLUDED"]
  S2AS["m=3 rank-five Hilbert--Burch (1,1,2)<br/>CENTRAL CHART: ORDINARY COLOOPS ONLY"]
  S2AT["m=3 rank-five Hilbert--Burch (1,1,2)<br/>THIRD-COLOUR COLOOPS EXCLUDED"]
  S2AU["m=3 rank-five Hilbert--Burch (1,1,2)<br/>DISTINCT CENTRAL CHART EXCLUDED"]
  S2AV["m=3 rank-five Hilbert--Burch (1,1,2)<br/>SINGLE REPEATED OUTER DIVISORS EXCLUDED"]
  S2AW["m=3 rank-five Hilbert--Burch (1,1,2)<br/>DISTINCT CENTRAL CHART COMPLETELY EXCLUDED"]
  S2AX["m=3 rank-five Hilbert--Burch (1,1,2)<br/>BOTH CENTRAL CHARTS EXCLUDED"]
  S2AY["m=3 rank-five Hilbert--Burch (1,1,2)<br/>COMPLETE PROFILE EXCLUDED"]
  S2AZ["m=3 rank-five Hilbert--Burch (1,2,2)<br/>NINE COORDINATE COLOOPS"]
  S2BA["m=3 rank-five Hilbert--Burch (1,2,2)<br/>beta_t COLOOP: w COORDINATE"]
  S2BB["m=3 rank-five Hilbert--Burch (1,2,2)<br/>beta_t COLOOP EXCLUDED"]
  S2BC["m=3 rank-five Hilbert--Burch (1,2,2)<br/>alpha_s COLOOP EXCLUDED"]
  S2BD["m=3 rank-five Hilbert--Burch (1,2,2)<br/>residual beta_j COLOOPS: w_t=0"]
  S2BE["m=3 rank-five Hilbert--Burch (1,2,2)<br/>residual beta_j COLOOPS: w COORDINATE"]
  S2BF["m=3 rank-five Hilbert--Burch (1,2,2)<br/>residual beta_j ENDPOINT SUPPORT TABLE"]
  S2BG["m=3 rank-five Hilbert--Burch (1,2,2)<br/>residual beta_j ENDPOINTS: s!=t"]
  S2BH["m=3 rank-five Hilbert--Burch (1,2,2)<br/>residual beta_j ENDPOINTS: y COORDINATE"]
  S2BI["m=3 rank-five Hilbert--Burch (1,2,2)<br/>residual beta_j TERMINAL ENDPOINT"]
  S2BJ["m=3 rank-five Hilbert--Burch (1,2,2)<br/>both residual beta_j COLOOPS EXCLUDED"]
  S2BK["m=3 rank-five Hilbert--Burch (1,2,2)<br/>all gamma_k COLOOPS EXCLUDED"]
  S2BL["m=3 rank-five Hilbert--Burch (1,2,2)<br/>COMPLETE PROFILE EXCLUDED"]
  S2BM["m=3 joint rank 3/4 transverse two-root<br/>FOUR-CELL ATLAS / EXACT POLE CONTROLS"]
  S2BN["m=3 joint rank 4 transverse two-root q=2<br/>COMPLETE CELL EXCLUDED"]
  S2BO["m=3 joint rank 3 transverse two-root q=2<br/>LOCAL CONTROLS / GRAPH CELL EXCLUDED"]
  S2BP["m=3 joint rank 3/4 transverse two-root q=1<br/>PAIR POLES / GRAPH CELLS EXCLUDED"]
  S2BQ["m=3 joint rank 3/4 three-root<br/>DERIVATIVE 9/8/7 + TORUS ATLAS"]
  S2BR["m=3 rank 4 / derivative rank 8<br/>TARGET ROW ATLAS / DISTINCT (2,2) EXCLUDED"]
  S2BS["m=3 rank 4 / derivative rank 8<br/>SAME-COLOUR Q2 SPLIT LIFT EXCLUDED"]
  S2BT["m=3 rank 4 / derivative rank 8<br/>SAME-COLOUR Q2 EXHAUSTIVE LIFT ATLAS"]
  S2BU["m=3 rank 4 / derivative rank 8<br/>SAME-COLOUR Q2 ALIGNED CHART EXCLUDED"]
  S2BV["m=3 rank 4 / derivative rank 8<br/>SAME-COLOUR Q2 NONALIGNED PAIR POLES"]
  S2BW["m=3 rank 4 / derivative rank 8<br/>SAME-COLOUR (2,2,2) COMPLETE"]
  S2BX["m=3 rank 4 / derivative rank 8<br/>SAME-COLOUR (2,2,3) EXCLUDED"]
  S2BY["m=3 rank 4 / derivative rank 8<br/>MIXED (2,3,3)/(3,2,3) EXCLUDED"]
  S2BZ["m=3 rank 4 / derivative rank 8<br/>MIXED Q2 SUPPORT TWO EXCLUDED"]
  S2CA["m=3 rank 4 / derivative rank 8<br/>MIXED Q2 SUPPORT ONE EXCLUDED"]
  S2CB["m=3 rank 4 / derivative rank 8<br/>FULLY INJECTIVE (3,3,2) EXCLUDED"]
  S2CC["m=3 rank 4 / derivative rank 8<br/>MONOMIAL ENDPOINT LOCALIZATION"]
  S2CD["m=3 rank 4 / derivative rank 8<br/>DIAGONAL SUPPORT TWO EXCLUDED"]
  S2CE["m=3 rank 4 / derivative rank 8<br/>OFF-DIAGONAL ENDPOINT EXCLUDED"]
  S2CF["m=3 rank 4 / derivative rank 8<br/>DIAGONAL ENDPOINT FULL-TARGET REDUCTION"]
  S2CG["m=3 rank 4 / derivative rank 8<br/>CANONICAL BINOMIAL RESIDUAL EXCLUDED"]
  S2CH["m=3 rank 4 / derivative rank 8<br/>DIAGONAL ZERO-VISIBLE WALL EXCLUDED"]
  S2CI["m=3 rank 4 / derivative rank 8<br/>SAME-COORDINATE ONE-VISIBLE CELLS EXCLUDED"]
  S2CJ["m=3 rank 4 / derivative rank 8<br/>COMPLETE ONE-VISIBLE WALL EXCLUDED"]
  S2CK["m=3 rank 4 / derivative rank 8<br/>DIAGONAL TWO-VISIBLE CELL EXCLUDED"]
  S2CL["m=3 rank 4 / derivative rank 8<br/>NONMONOMIAL ZERO-PAIR LOCALIZATION"]
  S2CM["m=3 rank 4 / derivative rank 8<br/>NONMONOMIAL ZERO-PAIR-FREE CELL EXCLUDED"]
  S2CN["m=3 rank 4 / derivative rank 8<br/>NONCOORDINATE NONMONOMIAL STRUCTURAL CELL EXCLUDED"]
  S2CO["m=3 rank 4 / derivative rank 8<br/>COORDINATE NONMONOMIAL STRUCTURAL CELL EXCLUDED"]
  S2["Force a refined full-sensor gate failure<br/>OPEN"]
  S3["All balanced partitions rank-drop<br/>OPEN on witness locus"]
  S3D["Diagonal-complete all-rank-drop family<br/>PROVED sharpness, NOT a witness"]
  S3Q["Common-quadratic local-GL orbit<br/>PROVED rank-drop, EXCLUDED from witness locus"]
  S3P["Common-quadric mixed/pure residues<br/>PROVED; common-conformal shore EXCLUDED"]
  S3B["Root-quadric basepoint bridge<br/>m=3,4 EXCLUDED; m>=5 -> PR"]
  S3C["Every induced K5 of an n=8 witness<br/>CODIMENSION >=3 boundary envelope"]
  S3CA["Fixed adjacent five-set pair<br/>CODIMENSION >=5 boundary overlap"]
  S3CB["Same adjacent pair inside B_all<br/>CODIMENSION >=6; NONEMPTY residual"]
  S3CC["Four-K5 pencil rank-cardinality boundary<br/>CODIM-9 ROUTE WITHDRAWN; CODIM-8 STRATUM"]
  S3CCD["Four-K5 support-Segre rank census<br/>FINITE GENERIC q>=20; CODIM-8 EQUALITY"]
  S3H["Adjacent-cut monomial control<br/>H1 BLIND; pair-local H2 DETECTS"]

  M1["Maximum torus-root split<br/>PROVED reduction"]
  M2["r >= 2 fixed-surplus layer<br/>PROVED reduction"]
  PR["Weighted permanent restriction family<br/>OPEN at arbitrary order"]
  PRC["Every co-two permanent product sensor corank >=2<br/>PROVED necessary boundary"]
  PR5["P6 co-two equality-five branch<br/>PROVED EXCLUDED"]
  PR6["P6 co-two product dimension >=6<br/>PAIR MODULI; OPEN factored sensor residual"]
  PRT["P6 simultaneous co-two tree radicals<br/>PROVED criterion / factor boundary"]
  O1["Fixed-layer truncation and nonobservability<br/>PROVED boundary"]
  O2["Two-open detector and q=0 star gauge<br/>PROVED boundary"]
  O2P["Projective single-open consecutive lift<br/>PROVED conditional reduction"]
  O2M["Minimum q=0, r=3 row replacement<br/>TWO-OPEN DETECTED conditionally"]
  O2T["q=0, r=4 locally transverse cell<br/>AT LEAST ONE DETECTOR conditionally"]
  O2F["Complete aligned q=0, r=4 cell<br/>AT LEAST ONE DETECTOR conditionally"]
  O2V["q=0, r=5 good-companion activity stratum<br/>AT LEAST ONE DETECTOR conditionally"]
  O2A["q=0, r=5 all-companion root-transverse stratum<br/>AT LEAST ONE DETECTOR conditionally"]
  O2C["Complete locally transverse q=0, r=5 cell<br/>AT LEAST ONE DETECTOR conditionally"]
  O2D["q=0, r=5 one arbitrary or regular-two defects<br/>AT LEAST ONE DETECTOR conditionally"]
  O2E["q=0, r=5 at most two defects except AA/BB<br/>AT LEAST ONE DETECTOR conditionally"]
  O2G["q=0, r=5 at most two defects, all types<br/>AT LEAST ONE DETECTOR conditionally"]
  O2H["q=0, r=5 at most three defects;<br/>A/Z fixed-layer modes impossible<br/>AT LEAST ONE DETECTOR conditionally"]
  O2I["Complete aligned q=0, r=5 cell<br/>AT LEAST ONE DETECTOR conditionally"]
  O3["q=0 r>=6, q>=1,<br/>or unfactorized detector OPEN"]

  U1["r = 1 complete matrix units<br/>PROVED normal form"]
  U1B["Support-minimal GHZ-torus endpoint balance<br/>PROVED"]
  U1C["Actual squared amplitudes moment-balanced<br/>PROVED gauge over C"]
  U2["At-most-four-port response<br/>k = 1, 2, 3 remain OPEN"]
  U3["Globally rigid colour system<br/>CONDITIONAL"]
  U4["Three-block primitive and dual bridges<br/>PROVED"]
  U5["Primitive-alone closure<br/>REFUTED ROUTE"]
  U6["Cross parity, bridges, rigid-head Wick<br/>PROVED reduction"]
  U7A["Nonzero parity fibre has exact word-shore rematching<br/>PROVED"]
  U7B["Cofactor-active cross core<br/>DEEPER / TRANSPORT / PURE CANCEL proved"]
  U7C["Gauge-invariant phase holonomy / pure cofactor flow<br/>PROVED reduction"]
  U7D["Complete pure-target moment-compatible odd holonomy<br/>PROVED sharpness, NOT a witness"]
  U7["Exclude pure-shore cancellation or active holonomy<br/>OPEN"]
  U8["Proper flag propagation<br/>OPEN"]
  D1["Deeper blocker branch<br/>OPEN"]

  A1["Simultaneous balanced all-bridge<br/>CONDITIONAL branch"]
  A2["D-degree <= 4 excluded; D-degree 5 has localized cancellation<br/>full-support degree >= 8"]
  A3["All saturated degrees have localized cancellation<br/>least core bipartite / port-count refined"]
  A4["Extremal sparse least core<br/>opposite extremal theta or aggregate sites"]
  A5["Beta-three sparse route ports<br/>paired singletons / complementary doubletons"]
  A6["Beta-three fixed-completion block<br/>rank three / fibre size never five"]
  A7["Beta-three binomial sign filter<br/>global scalar units / one aligned Q/C2 partition"]
  A8["Beta-three sparse-port primitive lattice<br/>even rank-three fibre / comparison graph"]
  A3R["Least-core complementary response<br/>edgewise zeros / minimum-crossing portals"]

  P5["Local P5 component programme<br/>PARTIAL / boundary-limited"]
  P7["Committed local P7 incidence<br/>criterion proved, outcome OPEN"]
  GLS2["Maximal-root surplus-two deck sensor<br/>PROVED conditional supply / rank-drop boundary"]
  GLS3["Surplus-two raw pair companion / physical fibre<br/>PROVED positive edge and sharp rank-drop"]
  GLS4["Same-pair quotient survival / raw companion<br/>PROVED source edge; target attachment OPEN"]
  GLS5["Pointwise selector-failure module<br/>PROVED exact criterion / abstract rank-only no-go"]
  GLS6["Common residual h,p / alignment gate<br/>PROVED exact source corollary and incidence"]
  GLS7["Four-root all-seven attachment trichotomy<br/>PROVED six-leaf cover; R/A package leaves OPEN"]
  GLS8["Promoted two-probe one-target reduction<br/>PROVED all-r criterion; physical failure OPEN"]
  GLS9["Four-root full-rank all-response-zero localization<br/>PROVED conditional; pure-Pi localized"]
  GLS10["Four-root full-rank literal-zero exclusion<br/>PROVED conditional; determinant and broader leaves OPEN"]
  GLS11["Four-root determinant-divisor six-response reduction<br/>PROVED exact core/trichotomy; survivor OPEN"]
  GLS12["Four-root divisor rank-two/singleton exclusion<br/>PROVED exact; continuations below"]
  GLS13["Four-root rank-one two-port P5 extraction<br/>PROVED exact downstream edge"]
  GLS14["Four-root rank-one contained/one-sided reduction<br/>PROVED exact routing; interfaces OPEN"]
  GLS15["Physical pair-companion transport<br/>PROVED arbitrary-r synchronization obstruction"]
  GLS16["Base-grade pair shadow / cross-target annihilation<br/>PROVED arbitrary-r circuit localization"]
  GLS17["Partial-root all-even-target shadow<br/>PROVED common pure-M selector gate"]
  GLS18["Leading-shadow target coupling / Fitting failure<br/>PROVED all-r exact bad-locus profile"]
  GLS19["Residual-present top shadow / pure-Z selector<br/>PROVED all-r second-axis failure profile"]
  GLS20["Promoted source-aligned base shadow<br/>PROVED 9-row failure profile"]
  GLS21["Promoted base-shadow all-port collapse<br/>PROVED factor-through route NO-GO"]
  GLS22["Promoted all-target transverse quotient<br/>PROVED exact 72/8-row equivalence"]
  GLS23["Promoted transverse nuisance decomposition<br/>PROVED slice formula / top-anchor split"]
  GLS24["Promoted one-probe anchor marginal<br/>PROVED 9-row route / double-transverse boundary"]
  GLS25["Promoted double-transverse anchor core<br/>PROVED 27/4-row routes"]
  GLS26["Promoted zero-anchor diagonal reconstruction<br/>PROVED essential-pair / shore-cover split"]
  GLS27["Zero-anchor residual-family shore cover<br/>PROVED generic escape / C12-C22 forms"]
  GLS28["Zero-anchor target envelope<br/>PROVED product selectors / bounded redundant cover"]
  GLS29["Rank-two-shore normal channel<br/>PROVED mixed identity / r=3 full-activity exclusion"]
  GLS30["Normal-product divisor kernel profile<br/>PROVED six-response/full-normal boundary / divisor OPEN"]
  GLS31["Evaluation-pencil mixed equations / simultaneous absorption<br/>PROVED static coupling NO-GO / divisor OPEN"]
  GLS32["First-polarized singleton kernels / full-pencil absorption<br/>PROVED projected-plane NO-GO / residual-family lift now GLS33"]
  GLS33["Residual-Laurent polarization / root-deck kernel anchor<br/>PROVED coefficientwise lift / anchor survival OPEN"]
  GLS34["Tangent-root Fitting / constant-anchor Segre silence<br/>PROVED six ambient-generic blind directions / legal attachment OPEN"]
  GLS35["Raw residual-absent anchor quotient / separation no-go<br/>PROVED exact escape-swallow split / no downstream entry"]
  GLS36["Zero-anchor incidence image / labelwise lift<br/>PROVED common-row NO-GO / mixed lift OPEN"]
  GLS37["Minimal raw swallow / shore-rank exclusion<br/>PROVED rank-3 two-shore fibre EMPTY / other fibres OPEN"]
  GLS38["Nonzero root companion / minimal raw swallow<br/>PROVED nonzero-q rank-3 full-swallow fibres EMPTY"]
  GLS39["Complete pairwise-diagonal family / minimal raw swallow<br/>PROVED all rank-3 full-swallow fibres EMPTY"]
  GLS40["Full-swallow aggregate deck / excess syzygies / cylinders<br/>PROVED rank-stratified reduction / rank-5 and rank-6 sharp boundaries"]
  GLS41["Full-swallow pure core / excess response<br/>PROVED 18/27-row useful-core reduction"]
  GLS42["Full-residual excess hafnian first variation<br/>PROVED trace-zero gauge family / active physical boundary"]
  GLS43["Rank-four full-swallow off-diagonal root deck<br/>PROVED q-outside-Delta fibre EMPTY"]
  GLS44["Rank-four full-swallow diagonal root deck<br/>PROVED nonzero-q fibre EMPTY / q=0 remains"]
  GLS45["Rank-four silent residual-shore profile<br/>PROVED only residual-free / sparse one-label cores remain"]
  GLS46["Rank-four silent complete-pair structure<br/>PROVED effective dimension <=12 / triangle-plus-feeder fork"]
  GLS47["Rank-four silent complete-pair exclusion<br/>PROVED both cores EMPTY / full-swallow rank floor 5"]
  GLS48["Zero-anchor two-effective-label pure target<br/>PROVED adaptive-cut rank 1 vs 3 / at least 3 labels"]
  GLS49["Zero-anchor residual-pair-plus-one-port target<br/>PROVED q-cylinder exclusion / D(p) at least 4 labels"]
  GLS50["Zero-anchor rank-five three-label kernel/deck profiles<br/>PROVED five-profile reduction / existence and exclusion OPEN"]
  GLS51["Zero-anchor exactly-three-label shared polarization<br/>PROVED only rank-7 separated normal form can survive"]
  GLS52["Zero-anchor uncontracted three-label target<br/>PROVED rank-7 normal form EMPTY / at least 4 labels"]
  GLS53["Zero-anchor four-promoted-label reconstruction<br/>PROVED no-residual four-label support EMPTY via n=6"]
  GLS54["Zero-anchor four-slot partial uncontraction<br/>PROVED actual-witness activity at least 5 via n=6"]
  GLS55["Zero-anchor torus-kernel contraction<br/>PROVED at least 5 full-map rigid labels via n=6"]
  GLS56["Probe-kernel pure-star flag / rigid companion<br/>PROVED structural split / natural GLD3 activity NO-GO"]
  GLS57["All-rank-one rigid colour pairing<br/>PROVED 2+2+2 pure companions / response polynomial<br/>old-probe GLD3 activity NO-GO"]
  GLS58["All-rigid kernel contraction / cross product<br/>PROVED rank-profile reduction / binary n=6 boundary"]
  GLS59["Unique-nonrigid old-probe exchange / overlap<br/>PROVED mono-binary descent / natural GLD3 target gate NO-GO"]
  GLS60["Rank-one pure-probe orientation / splice boundary<br/>PROVED two-colour shore purity<br/>direct / vertex-gauge graph splices NO-GO"]
  GLQ2["Two-residual response-atlas descent<br/>PROVED conditional / sharp boundary"]
  GLD1["Same-graph defects and target selector<br/>PROVED boundary / conditional detector"]
  GLD2["Four-root adjacent-grade target selectors<br/>PROVED decomposition / single-shore no-go"]
  GLD3["Pair/four-port diagonal interference<br/>PROVED nine-word detector / sharp camouflage"]
  GLD4["Two-chart target incidence / cloned atlas<br/>PROVED trichotomy / breadth boundary"]
  GLD5["Four-root constant module quotient<br/>PROVED criterion / maximum-root sharpness"]
  GLD6["Six-port physical Wick selectors<br/>PROVED two-active supply / depth-six detector"]
  GLD7["Fixed-Q target quotient<br/>PROVED rank-one trichotomy / conditional attachment"]
  GLD8["Global square-free Wick map<br/>PROVED support-union classification / common rows"]
  GLD9["Common contraction synchronization<br/>PROVED maximal-rank open intersection"]
  GLD10["Seven-port tensor Wick cover<br/>PROVED five-helper 189-coordinate supply"]
  GLD11["Simultaneous swallowed-pure control<br/>PROVED physical sharpness / mixed exclusion"]
  GLD12["Full tensor h=0 Z fibre<br/>PROVED z4 closure / two-vertex-cover boundary"]
  GLD13["Contraction escape / generic absorption<br/>PROVED function-field dichotomy"]
  GLD14["Paired M2/M4 response closure<br/>PROVED affine incidence / all-depth shape"]
  GLD15["Joint M/Z target quotient<br/>PROVED paired rank / block-cover boundary"]
  GLD16["Common projective joint selector<br/>PROVED arbitrary-h shifted GLD3 detector"]
  GLD17["Unequal-slope cancellation<br/>PROVED eighteen-word detector"]
  GLD18["Response-visible / edge-dependent slopes<br/>PROVED determinant and divisor detector"]
  GLD64["Decomposable variable slopes<br/>PROVED 43-word all-finite-slope exclusion"]
  GLD65["First-root product selector<br/>PARTIALLY WITHDRAWN root/full-coefficient mismatch"]
  GLD66["Product-selector response anchor<br/>PARTIALLY WITHDRAWN dependent conclusions"]
  GLD67["Root companion / full coefficient separation<br/>PROVED correction / exact three-colour control"]
  GLD68["Complementary pair base shadows<br/>PROVED nuisance saturation / all-six source impossible"]
  GLD69["Maximal survivor common incidence<br/>PROVED pair-layer exclusion / sparse-radical detector"]
  GLD70["Complete Q-layer secant trap<br/>PROVED exact reduction / torus-star 44-space"]
  GLD71["Torus-star punctured syndrome<br/>PROVED one-word atlas / determinant-safe route REFUTED"]
  GLD72["Torus-star Gaussian GHZ survivor<br/>PROVED exact fixed-space counterexample / integrability OPEN"]
  GLD73["Gaussian survivor contracted edge fibre<br/>PROVED p0 control / pinned first-jet nonextension"]
  GLD74["Gaussian survivor full coefficient fibre<br/>PROVED all raw lifts fail q0 first response"]
  GLD75["Torus-star survivor local germ<br/>PROVED smooth 5D germ / symmetry compression refuted"]
  GLD76["Survivor universal response module<br/>PROVED exact reduction / projective escape boundary"]
  GLD77["Survivor sign projective boundary<br/>PROVED three reduced points in sign plane"]
  GLD78["Survivor sign-boundary charts<br/>PROVED invariant principal-open nonextension"]
  GLD79["Gaussian full projective boundary<br/>PROVED exactly three reduced sign points"]
  GLD80["Survivor principal neighborhood<br/>PROVED existential first-response nonextension"]
  GLD81["Torus-star source-response bridge<br/>PROVED principal-open source branch exclusion"]
  GLD82["Fraction-free quadratic survivor open<br/>PROVED explicit principal-open nonextension"]
  GLD83["Bordered Pluecker/Fitting survivor open<br/>PROVED gamma-free intrinsic reduction"]
  GLD84["Equal-leaf centre-rank cover<br/>PROVED finite determinantal parameter reduction"]
  GLD85["Rank-eight full intrinsic Fitting point<br/>PROVED nonzero/proper open on one chart"]
  GLD86["Equal-leaf low-rank boundary<br/>PROVED four-divisor syndrome containment"]
  GLD87["Equal-leaf H1/H2/H3 safety<br/>PROVED singular-center exclusion"]
  GLD88["Equal-leaf H4 principal open<br/>PROVED forced-family center exclusion"]
  GLD89["Equal-leaf H4 P/d0 boundary<br/>PROVED determinant-safe exclusion"]
  GLD90["Equal-leaf H4 Q6-open low rank<br/>PROVED full principal-open exclusion"]
  GLD93["Equal-leaf H4 L1/L2 boundaries<br/>PROVED rank-seven exclusion"]
  GLD91["Rank-eight two-leaf Fitting slice<br/>PROVED exact slice exclusion"]
  GLD92["Equal-leaf H4 Q6 dense boundary<br/>PROVED two-minor cover inside GLD88 family"]
  GLD19["Response-map-zero support<br/>PROVED five-row detector / opposite annihilation"]
  GLD20["Global map-zero physical support<br/>PROVED channel atlas / pure-absorption reduction"]
  GLD21["Map-zero dead-colour h-gate<br/>PROVED h=0 subcell exclusion / h!=0 residue"]
  GLD22["Dense private cross matching<br/>PROVED same-graph subcell exclusion"]
  GLD23["Dense private permutations<br/>PROVED all 576 monomial charts excluded"]
  GLD24["Dense balanced single switch<br/>PROVED first nonprivate chart exclusion"]
  GLD25["Dense two-amplitude switch<br/>PROVED full 2-parameter chart exclusion"]
  GLD26["Dense directed spur<br/>PROVED generic 3-parameter exclusion"]
  GLD27["Directed-spur uv=-1 divisor<br/>PROVED pointwise exclusion"]
  GLD28["Directed-spur uv=1 divisor<br/>PROVED pointwise exclusion"]
  GLD29["Directed-spur uv-u-v-1 divisor<br/>PROVED pointwise exclusion"]
  GLD30["Directed-spur uv+vw+w+1 divisor<br/>PROVED chart completion"]
  GLD31["Dense bidirected spur<br/>PROVED generic 4-parameter exclusion"]
  GLD32["Bidirected-spur uv=-1 divisor<br/>PROVED generic refinement"]
  GLD33["Bidirected-spur uv=-1, u=1<br/>PROVED surface exclusion"]
  GLD34["Bidirected-spur uv=-1, z=1<br/>PROVED surface exclusion"]
  GLD35["Bidirected-spur uv=-1, z=-1<br/>PROVED surface exclusion"]
  GLD36["Bidirected-spur uv=-1 divisor<br/>PROVED pointwise exclusion"]
  GLD37["Bidirected-spur uv+wz-1 divisor<br/>PROVED pointwise exclusion"]
  GLD38["Bidirected-spur uv+wz+1 divisor<br/>PROVED pointwise exclusion"]
  GLD39["Dense bidirected-spur nonzero chart<br/>PROVED chart completion"]
  GLD40["Dense bidirected-spur affine chart<br/>PROVED all-support completion"]
  GLD41["Single-active-slice affine cell<br/>PROVED full 12-parameter completion"]
  GLD42["Two-active reciprocal spike<br/>PROVED affine-chart exclusion"]
  GLD43["Full two-active affine cell<br/>PROVED reciprocal-support reduction"]
  GLD44["Two reciprocal pairs<br/>PROVED five-orbit generic exclusion"]
  GLD45["Two-pair same-tail orbit<br/>PROVED pointwise exclusion"]
  GLD46["Two-pair disjoint orbit<br/>PROVED pointwise exclusion"]
  GLD47["Two-pair reverse orbit<br/>PROVED pointwise exclusion"]
  GLD48["Two-pair same-head orbit<br/>PROVED pointwise exclusion"]
  GLD49["Two-pair chain orbit<br/>PROVED pointwise exclusion / all 66 masks"]
  GLD50["Three reciprocal pairs<br/>PROVED 13-orbit generic exclusion"]
  GLD51["Three-pair directed path<br/>PROVED pointwise exclusion / 24 masks"]
  GLD52["Three-pair out-star<br/>PROVED pointwise exclusion / 4 masks"]
  GLD53["Three-pair fork path<br/>PROVED pointwise exclusion / 24 masks"]
  GLD54["Three-pair reverse-disjoint<br/>PROVED pointwise exclusion / 12 masks"]
  GLD55["Three-pair in-star<br/>PROVED colour-exchange exclusion / 4 masks"]
  GLD56["Three-pair reverse fork<br/>PROVED colour-exchange exclusion / 24 masks"]
  GLD57["Three-pair in-fork<br/>PROVED pointwise exclusion / 12 masks"]
  GLD58["Three-pair out-fork<br/>PROVED colour-exchange exclusion / 12 masks"]
  GLD59["Three-pair O6<br/>PROVED pointwise exclusion / 24 masks"]
  GLD60["Three-pair O3<br/>PROVED pointwise exclusion / 24 masks"]
  GLD61["Three-pair O2 and O7<br/>PROVED pointwise exclusion / 48 masks"]
  GLD62["Three-pair O9<br/>PROVED pointwise exclusion / all 220 masks closed"]
  BO1["Uniform bounded-window certification<br/>REFUTED on ambient decks / responses"]
  GL["Universal extraction, synchronization,<br/>and local-to-global gluing OPEN"]
  C2["Automatic characteristic-two lift<br/>REFUTED as a general route"]

  G0 -->|universal reduction| S1
  S1 -->|exact gate refinement| S2E
  S2E -->|finite-jet refinement| S2J
  S2J -->|target-column refinement| S2K
  S2K -->|projective compression| S2L
  S2L -. full-row compatibility .-> S2M
  S2M -->|exact image interface| S2N
  S2M -->|eight-control input| S2O
  S2N -->|common-shore pullback| S2O
  S2O -->|transverse residual obstruction| S2P
  S2P -. eight controls not exhaustive .-> S2
  S2E -->|m=3 normalized pair layer| S2Q
  S2N -->|separated physical singleton columns| S2Q
  S2Q -. three exceptional strata remain .-> S2
  S2N -->|physical empty-column P3 contraction| S2R
  S2R -->|coordinate-boundary refinement| S2S
  S2Q -->|common-three-space component| S2T
  S2S -->|dimension / closure refinement| S2T
  S2T -->|full joint cross-rank refinement| S2U
  S2U -->|source-aligned exceptional row| S2V
  S2V -->|two-source splitting refinement| S2W
  S2W -->|full-support derivative dichotomy| S2X
  S2X -->|hyperplane rank-loss / zero-grid bound| S2Y
  S2Y -->|sharp zero-grid equality classification| S2Z
  S2Z -->|sharp two-root derivative / pointwise slice rank| S2AA
  S2AA -->|lower-rank pure/mixed and tangent boundaries| S2AB
  S2AB -->|rank-six shared-factor / crossed-pair obstruction| S2AC
  S2AC -->|beta-zero atlas / relation-plane contraction| S2AD
  S2AD -->|graph permanent / symmetric square obstruction| S2AE
  S2AE -->|coordinate relation / square-pencil obstruction| S2AF
  S2AF -->|rank-five derivative census / beta-zero torus atlas| S2AG
  S2AG -->|"support-two (2,2) double-monomial mixed-product obstruction"| S2AH
  S2AH -->|Type-II collapse / fully transverse correction-line| S2AI
  S2AI -->|mixed graph / zero-row target-line obstruction| S2AJ
  S2AJ -->|invertible graph / binary diagonal-plane common-zero| S2AK
  S2AK -->|support-one graph / two-plane square pencil| S2AL
  S2AL -->|two zero rows / diagonal-plane common-zero| S2AM
  S2AG -->|Hilbert--Burch repeated-coordinate binary frame| S2AN
  S2AN -->|complementary support-two same-row obstruction| S2AO
  S2AO -->|torus coloop / quadratic-annihilator obstruction| S2AP
  S2AP -->|coordinate-triangle torus coloop / two-plane fork| S2AQ
  S2AQ -->|eight-hyperplane torus fork / mixed-factor sharing| S2AR
  S2AR -->|nine-hyperplane torus fork / split-centre factor atlas| S2AS
  S2AS -->|primal coloop plane / square-support split| S2AT
  S2AT -->|central-coloop tangent / fibre obstruction| S2AU
  S2AU -->|one-face fork / alternating zero-rectangle atlas| S2AV
  S2AV -->|seven-factor fork / square-radical and correction obstruction| S2AW
  S2AW -->|ordinary-coloop coefficient fork / endpoint atlases| S2AX
  S2AX -->|nine-coordinate coloop fork / binary-face endpoint atlases| S2AY
  S2AY -->|rank-seven recovery / nine-coordinate coloop atlas| S2AZ
  S2AZ -->|complete 3x2x2 face / binary-diagonal obstructions| S2BA
  S2BA -->|coordinate-endpoint single-cell radical obstruction| S2BB
  S2BB -->|projective determinant-face pencil / same-pair obstruction| S2BC
  S2BC -->|one-row-escape binary frame / 28 exact endpoint certificates| S2BD
  S2BD -->|one-row-escape same-third-row frame / 21 exact families| S2BE
  S2BE -->|projective pencil / generic middle-line obstruction| S2BF
  S2BF -->|generic-line same-third-row obstruction / 21 exact families| S2BG
  S2BG -->|one-sided pencil degeneration / generalized same-third-row obstruction| S2BH
  S2BH -->|common-active-middle-row obstruction / 90 exact families| S2BI
  S2BI -->|coloop-specific same-pair incidence / 15 exact families| S2BJ
  S2BJ -->|intersecting-face transfer / exact root exchange| S2BK
  S2BK -->|complementary-coloop plane / 5 exact families| S2BL
  S2AG -->|lower-rank projection / uninvolved-row support| S2BM
  S2BM -->|noncontained-plane common-zero / profile transfer| S2BN
  S2BN -->|contained conjugate chart / two-diagonal forcing| S2BO
  S2BM -->|one-cell tangent atlas / missing-coordinate Cramer residues| S2BP
  S2BP -->|remaining lower-rank three-root derivative census| S2BQ
  S2BQ -->|rank-four shared-syzygy target contraction| S2BR
  S2BR -->|eight quotient coefficients / transverse-product obstruction| S2BS
  S2BR -->|two pure-target contractions / projection split| S2BT
  S2BT -->|four root coefficients / Segre-tangent kernel| S2BU
  S2BT -->|deformed source atlas / Cramer residues| S2BV
  S2BR -->|support-two contractions / projection rank| S2BW
  S2BV -->|support-one graph cell| S2BW
  S2BR -->|injective third row / exact binary table| S2BX
  S2BW -->|remaining same-colour row profile| S2BX
  S2BX -->|one deficient involved row / binary restriction| S2BY
  S2BY -->|rank-two third row / one correction line| S2BZ
  S2BZ -->|support-one resonance / dual-row collapse| S2CA
  S2CA -->|fully injective q=2 / direct root-box fork| S2CB
  S2CB -->|fully injective q=3 / monomial binary face| S2CC
  S2CC -->|diagonal two-supported endpoint / 29 exact charts| S2CD
  S2CC -->|off-diagonal coordinate endpoint / sparse-edge atlas| S2CE
  S2CD -->|coordinate w / restore the unsliced target| S2CF
  S2CE -->|only surviving monomial branch is diagonal| S2CF
  S2BR -->|common coordinate shared factors / complementary diagonal binomial| S2CG
  S2CF -->|corrected-cube visibility split| S2CH
  S2CG -->|full-sensor radical-line bound| S2CH
  S2CH -->|same-coordinate one-visible support cells| S2CI
  S2CG -->|zero-pair plane geometry| S2CI
  S2CI -->|exhaust all remaining one-visible support masks| S2CJ
  S2CF -->|complete faces and unsliced root matrix| S2CJ
  S2CJ -->|fourteen-mask two-visible support atlas| S2CK
  S2CG -->|zero-pair classification / radical geometry| S2CK
  S2BQ -->|actual nonmonomial residual / coordinate shared factor| S2CL
  S2BR -->|fully-injective graph / complete three slices| S2CL
  S2CG -->|alternating-space zero-pair geometry| S2CL
  S2CK -->|two-transverse mixed-map obstruction| S2CL
  S2CL -->|exhaust the zero-pair-free successor| S2CM
  S2CK -->|two-transverse mixed-map obstruction| S2CM
  S2CM -->|both shared factors noncoordinate| S2CN
  S2CG -->|zero-pair classification / radical geometry| S2CN
  S2CI -->|two-cross incidence dichotomy| S2CN
  S2CK -->|two-transverse mixed-map obstruction| S2CN
  S2CN -->|coordinate shared-factor structural residual| S2CO
  S2CG -->|zero-pair classification / radical geometry| S2CO
  S2CI -->|two-cross incidence dichotomy| S2CO
  S2CK -->|zero-corner and mixed-map obstructions| S2CO
  S2CO -->|lower-rank cells / components / poles / higher orders| S2
  S2CF -->|corrected cube and exact visibility census| S2CK
  S2T -. three physical component types remain .-> S2
  S2AM -. transverse branch closed; other rank-five branches / rank <=4 .-> S2
  S2BL -. rank <=4 / other components / poles / higher m .-> S2
  S2BS -. exact coordinate specialization .-> S2BT
  S2CF -. other nonmonomial residuals / components and poles .-> S2
  S2CG -. other nonmonomial (3,3,3) / other components and poles .-> S2
  S2CH -. nonmonomial residuals / wider branches .-> S2
  S2CI -. nonmonomial residuals / wider branches .-> S2
  S2CK -. nonmonomial residuals / wider branches .-> S2
  S1 -->|boundary| S3
  S3 -. pure/local data insufficient .-> S3D
  S3 -->|common-quadratic stratum| S3Q
  S1 -->|common-quadric shore specialization| S3P
  S3Q -. strict special case .-> S3P
  S3P -->|fully supported conic point| S3B
  G0 -->|n=8 anchored five-root slices| S3C
  S3C -->|exact fixed adjacent-pair overlap| S3CA
  S3CA -->|proper B_all cut on equality sources| S3CB
  S3CB -->|span-rank counterboundary corrects pencil route| S3CC
  S3CC -->|corrected finite support-Segre census| S3CCD
  S3CC -. corrected span-rank analysis and seventy-pencil compatibility open .-> S3
  S3CCD -. rank-degenerate components, B_all, and seventy-pencil glue open .-> S3
  S3 -. rankdrop + pure + H1 insufficient .-> S3H

  G0 -->|universal reduction| M1
  M1 -->|case r >= 2| M2
  M1 -->|case r = 1| U1
  M2 -->|surplus-two uncontracted sensor| GLS2
  GLS2 -->|blocker-corank and physical-secant refinement| GLS3
  GLS3 -->|complete contracted mixed target| GLS4
  GLS4 -->|pointwise/function-field failure topology| GLS5
  GLS4 -->|common nonzero h,p contraction| GLS6
  GLD2 -->|exact ambient and legal-subspace alignment gate| GLS6
  GLS4 -->|four-root pair-block split| GLS7
  GLS5 -->|pure-profile and common-incidence criterion| GLS7
  GLD13 -->|four-root R/E/A target split| GLS7
  GLS4 -->|promote all but two roots; top-depth target family| GLS8
  GLS5 -->|radical-Fitting pointwise failure criterion| GLS8
  GLS6 -->|retain common nonzero h,p gate| GLS8
  GLS7 -->|one-row refinement of the all-seven split| GLS8
  GLS7 -->|literal all-seven response zero on det H_Q nonzero| GLS9
  GLS9 -->|two complete residual-colour fibres| GLS10
  GLS10 -->|det H_Q zero; six pair responses zero| GLS11
  GLS11 -->|six active-pair quotients / P4 column splice| GLS12
  GLS12 -->|two-port common-tail Latin splice| GLS13
  GLS13 -->|weighted P5 restriction; downstream open| P5
  GLS12 -->|double-contained / one-sided complete-target routing| GLS14
  GLD15 -->|joint rank-one quotient/kernel orientation| GLS15
  GLS2 -->|maximum-root grade shadow| GLS16
  GLS15 -->|physical pair columns / absorbed direction| GLS16
  GLS2 -->|partial-root grade filtration| GLS17
  GLD15 -->|complete all-even-target joint quotient| GLS17
  GLS16 -->|pair-target t=1 specialization| GLS17
  GLS17 -->|partial-root leading quotient| GLS18
  GLD15 -->|complete target equation| GLS18
  GLS5 -->|all-rank geometric Fitting method| GLS18
  GLS2 -->|t-open-root top-grade filtration| GLS19
  GLD15 -->|individual-Z quotient / complete target| GLS19
  GLS5 -->|all-rank geometric Fitting method| GLS19
  S1 -->|premise| O1
  M2 -->|premise| O1
  O1 -->|residual refinement| O2
  O2 -->|aligned projective branch| O2P
  O2P -->|permanent reduction| PR
  O2P -->|minimum Hall cell| O2M
  O2P -->|transverse next cell| O2T
  O2P -->|complete four-cell closure| O2F
  O2P -->|five-cell collective transport| O2V
  O2P -->|five-cell pair collision| O2A
  O2P -->|complete transverse five-cell| O2C
  O2P -->|rank-one-mode transport| O2D
  O2T -. strict special case .-> O2F
  O2V -. strict overlapping stratum .-> O2C
  O2A -. strict overlapping stratum .-> O2C
  O2C -. strict special stratum .-> O2D
  O2D -. strict special strata .-> O2E
  O2E -. strict special strata .-> O2G
  O2G -. strict special strata .-> O2H
  O2H -->|remaining-strata closure| O2I
  O2F -->|larger-cell boundary| O3
  O2I -->|larger/unfactorized boundary| O3
  O2 -->|boundary| O3
  M2 -->|zero-surplus specialization| PR
  S3B -->|existing zero-surplus extraction| PR
  PR -->|necessary corank-two boundary| PRC
  PRC -->|product dimension five| PR5
  PRC -->|product dimension at least six| PR6
  PR6 -->|common-factor simultaneous refinement| PRT

  U1 -->|reduction| U2
  U1 -->|support-minimal refinement| U1B
  U1B -->|moment-gauge refinement| U1C
  U2 -->|specialization| U3
  U3 -->|premise| U4
  U4 -. primitive alone insufficient .-> U5
  U1 -->|premise| U6
  U2 -->|premise| U6
  U6 -->|exact erasure| M2
  U6 -->|active-fibre refinement| U7A
  U7A -->|exact response| U7B
  U7B -->|phase refinement| U7C
  U7C -->|boundary| U7
  U7C -. stronger sharpness .-> U7D
  U7D -->|remaining mixed equations| U7
  U7B -->|deeper exit| D1
  U1C -. moment-gauge compatibility .-> U7C
  U1C -. compatible sharpness .-> U7D
  U2 -->|boundary| U8
  U2 -->|boundary| D1
  U6 -->|boundary| D1
  U2 -->|simultaneous full flags| A1
  A1 -->|residual refinement| A2
  A2 -->|all-degree localization and core refinement| A3
  U7I -->|port/theta specialization| A3
  A3 -->|extremal sparse shore refinement| A4
  U7I -->|nonzero port partition| A4
  A2 -. full-support density .-> A4
  A4 -->|rank-three route specialization| A5
  U7I -->|weighted port composition| A5
  A3 -. rank-three simplex .-> A6
  A5 -->|route-port block| A6
  U7A -. complete mixed zero fibre .-> A6
  U7K -. conditional fixed completion .-> A6
  A6 -->|completion coverage / rank-three ideal| U7
  A6 -->|integral binomial-lattice containment| A7
  U7F -->|fixed sign quotient| A7
  A7 -->|balanced Q/Q / aligned Q/C2 residual| U7
  A5 -. sparse quartic port coordinates .-> A8
  A6 -->|rank-three complete-fibre lattice| A8
  A7 -->|contained balanced survivors| A8
  U7E -. complete-fibre difference lattice .-> A8
  U7F -. quotient sign criterion .-> A8
  A8 -->|rank at least four / unforced comparisons| U7
  A3 -->|least-core response refinement| A3R
  U7I -->|conformal attachment interface| A3R
  A3R -->|remaining support / target coupling| U7

  PR -->|local specialization only| P5
  PR -->|local specialization only| P7
  P5 -->|open gluing obligation| GL
  P7 -->|open gluing obligation| GL
  GLS2 -->|Q-observable paired charts| GLQ2
  GLS2 -->|rank drop / higher surplus / target attachment open| GL
  GLS4 -. r=4 same-pair raw p_A; legal augmented l unforced .-> GLD2
  GLS4 -->|individual same-Q supply only; legal target selector open| GL
  GLS5 -->|physical mixed identity still required| GL
  GLS6 -->|legal M / response / synchronization / anchor open| GL
  GLS7 -->|E on O or C gives legal seven-target interface| GLD3
  GLS7 -->|all-seven R, A and exceptional fibres remain| GL
  GLS8 -->|simultaneous all-target Fitting failure; downstream shape for r>=5| GL
  GLS8 -->|maximum-root factor-through quotient on source Laplace pairs| GLS20
  GLS20 -->|retained D=Q all-port label gives p I_9| GLS21
  GLS21 -->|quotient exact uncontracted all-port root line| GLS22
  GLS22 -->|label-by-label projected nuisance slices| GLS23
  GLS23 -->|one-probe anchor marginal / exact exterior quotient| GLS24
  GLS23 -->|zero anchor / complete top-target reconstruction| GLS26
  GLS24 -->|zero-marginal nonzero anchor / core projector| GLS25
  GLS25 -->|reduced failure / activity / downstream package open| GL
  GLS26 -->|residual-family generic/exceptional refinement| GLS27
  GLS27 -->|foreign-supplier target envelope| GLS28
  GLS28 -->|one-dimensional redundant-cover normal channel| GLS29
  GLS29 -->|one-/two-active divisor kernel isolation| GLS30
  GLS30 -->|coupled maximum-root / full-nuisance boundary| GLS31
  GLS31 -->|singleton-kernel contraction / complete-pencil audit| GLS32
  GLS32 -->|residual-family lift / actual-root constant deck| GLS33
  GLS33 -->|coefficientwise blind-space / constant-anchor case cover| GLS34
  GLS34 -->|raw anchor module / output-to-coefficient audit| GLS35
  GLS35 -->|swallowed pure probes / incidence-map audit| GLS36
  GLS36 -->|minimal nuisance-rank / residual-shore audit| GLS37
  GLS37 -->|nonzero-root-companion shore-drop audit| GLS38
  GLS38 -->|q=0 whole-domain pair-family audit| GLS39
  GLS39 -->|rank>=4 aggregate-deck / target-cylinder audit| GLS40
  GLS40 -->|pure-core / excess-response audit| GLS41
  GLS41 -->|selected excess first-variation audit| GLS42
  GLS42 -->|additional GHZ coupling / pure-core attachment open| GL
  GLS40 -->|rank-four zero-excess complete-labelled audit| GLS43
  GLS43 -->|nonzero diagonal rank-four incidence audit| GLS44
  GLS44 -->|q=0 residual-shore profile audit| GLS45
  GLS45 -->|complete-pair structural-degree / cut audit| GLS46
  GLS46 -->|triangle synchronization / excess locking| GLS47
  GLS47 -->|rank>=5 full swallow / wider attachment open| GL
  GLS40 -->|two-effective-label adaptive target cut| GLS48
  GLS48 -->|four-or-more-label / higher-rank target coupling open| GL
  GLS48 -->|"D(p) equality / q-cylinder audit"| GLS49
  GLS49 -->|p=0 three-label kernel/deck audit| GLS50
  GLS50 -->|shared-polarization profile classification| GLS51
  GLS51 -->|uncontracted inactive-port deck coupling| GLS52
  GLS52 -->|four-promoted-label six-vertex reconstruction| GLS53
  GLS53 -->|active-residual partial uncontraction / inactive-port padding| GLS54
  GLS8 -->|outside torus-kernel contraction / four open slots| GLS55
  GLS55 -->|uniform pointwise activity corollary| GLS54
  GLS55 -->|exactly-five-rigid trilinear decks / six-plus-rigid and attachment open| GL
  GLS8 -->|nonrigid kernel matching contraction / pure-star flag| GLS56
  GLS55 -->|r=3 rigid/nonrigid structural bifurcation| GLS56
  GLS56 -->|r=3 all-six rigid, all joint ranks one| GLS57
  GLS56 -->|r=3 all-six rigid, higher-rank profile| GLS58
  GLS56 -->|r=3 unique nonrigid / old-probe exchange| GLS59
  GLS56 -->|alternate receiver / arbitrary-r attachment open| GL
  GLS57 -->|pure-shore orientation / natural splice audit| GLS60
  GLS60 -->|non-gauge reconstruction / promoted attachment open| GL
  GLS58 -->|binary descents / injective cancellation / attachment open| GL
  GLS59 -->|coupled overlaps / promoted attachment open| GL
  GLS29 -->|r>=4 disjoint cover / other shores open| GL
  GLS14 -->|pure P4/P5 compression; Phi selector or Psi face defect open| GL
  GLS15 -->|physical transport defect| GLS16
  GLS16 -->|pair base-swallowed circuits| GLS17
  GLS17 -->|complete-target leading identity| GLS18
  GLS18 -->|simultaneous Fitting failure / activity / transport / promoted interface open| GL
  GLS19 -->|top absorptions / activity / two-axis coexistence / promoted interface open| GL
  GLS3 -->|higher mixed witness-locus equations required| GL
  GLQ2 -->|permanent attachment remains open| GL
  GLD1 -->|four-root target-coupling refinement| GLD2
  GLD1 -->|general / other-root selector and nuisance open| GL
  GLD2 -->|constant multi-selector supply remains open| GL
  GLD1 -->|two-depth target-coupling refinement| GLD3
  GLD3 -->|two-chart target-incidence refinement| GLD4
  GLS2 -->|full fixed-Q module| GLD5
  GLD5 -->|good quotient gives exact D/T attachment| GLD3
  GLD5 -->|full witness target quotient| GLD7
  GLD7 -->|seven rank-one classes attach D/T| GLD3
  GLD7 -->|31 rank-one classes attach z2/z4/z6| GLD6
  GLD7 -->|maximal-rank common contraction| GLD9
  GLD9 -->|common seven selectors| GLD3
  GLD9 -->|common 31 selectors| GLD6
  GLD3 -->|h=0 pair/four response identity| GLD6
  GLD4 -->|all-subwindow and deeper-response refinement| GLD6
  GLD6 -->|global square-free common-row refinement| GLD8
  GLD8 -->|five-helper tensor word cover| GLD10
  GLD7 -->|simultaneous swallowed-pure sharpness| GLD11
  GLD6 -->|full tensor four-port closure| GLD12
  GLD8 -->|all-depth scalar classification| GLD12
  GLD7 -->|function-field pure-absorption split| GLD13
  GLD9 -->|generic-rank escape refinement| GLD13
  GLD13 -->|common seven attachment on escape branch| GLD3
  GLD12 -->|paired M2/M4 target-shape refinement| GLD14
  GLD7 -->|joint two-column quotient refinement| GLD15
  GLD12 -->|fixed-Z block-cover refinement| GLD15
  GLD14 -->|one-colour kernel and M-shape refinement| GLD15
  GLD15 -->|common projective operator line| GLD16
  GLS15 -->|if transport defects vanish and the four-port line agrees| GLD16
  GLS16 -->|conditional pair-line implication; all-six r=4 source impossible by GLD68| GLD16
  GLS17 -->|conditional seven-shadow implication; all-six r=4 pair premise impossible by GLD68| GLD16
  GLS19 -->|seven useful top shadows give common pure-Z line| GLD16
  GLD3 -->|arbitrary-h denominator-free shifted detector| GLD16
  GLD15 -->|unequal pair/four operator slopes| GLD17
  GLD16 -->|different-slope cancellation refinement| GLD17
  GLD15 -->|mixed-response visibility / full-nuisance slopes| GLD18
  GLD16 -->|common-line and decomposable-channel boundary| GLD18
  GLD17 -->|edge-dependent cancellation refinement| GLD18
  GLD18 -->|globally decomposable arbitrary-slope refinement| GLD64
  GLS17 -->|first-root product selector constrains root companions| GLD67
  GLD15 -->|complete joint module keeps companion/full types distinct| GLD67
  GLD65 -. cross-Gram bridge refuted .-> GLD67
  GLD66 -. dependent conclusions withdrawn .-> GLD67
  GLS16 -->|complementary labels saturate opposite base nuisances at r=4| GLD68
  GLD68 -. all-six GLS17 base-shadow source impossible .-> GLD16
  GLD68 -->|one labelled star/triangle parent module and physical common-J lift| GLD69
  GLD69 -->|complete 79-column map / epsilon secant trap / torus-star compression| GLD70
  GLD70 -->|exact pair erasure / 37-check syndrome / one-word atlas| GLD71
  GLD71 -->|exact Gaussian survivor / determinant-safe route refuted| GLD72
  GLD72 -->|pinned edge-fibre realization / complete first-response obstruction| GLD73
  GLD73 -->|35D affine quotient / complete projective rank-one exclusion| GLD74
  GLD74 -->|exact stabilizer / bidirectional local ideal certificate| GLD75
  GLD75 -->|68x4 full quotient / S3 blocks / exact boundary witnesses| GLD76
  GLD76 -->|exact sign compression / exhaustive three-point sign cover| GLD77
  GLD77 -->|all-three moving jets / invariant 8-to-9 determinant opens| GLD78
  GLD78 -->|S3 isotypic determinant cover / all charts exhaustive| GLD79
  GLD79 -->|s-saturated projective closure / DVR trait exclusion| GLD80
  GLD80 -->|physical raw-edge partition / complete 17-coordinate response factorization| GLD81
  GLD80 -->|Reynolds P8 compression / fraction-free 45-quadric determinant| GLD82
  GLD81 -->|physical source consequence on explicit open| GLD82
  GLD82 -->|bordered Pluecker decharting / full quadratic Fitting map| GLD83
  GLD81 -->|physical source consequence on gamma-free open| GLD83
  GLD83 -->|centre-linear survivor equations / exhaustive rank 8, 7, at-most-6 cover| GLD84
  GLD84 -->|exact six-leaf/two-residual rank-eight specialization and full Fitting minor| GLD85
  GLD84 -->|exact syndrome minor / rank-at-most-6 four-divisor containment| GLD86
  GLD86 -->|exact H1 kernel / leaf-column equivariance for H2,H3| GLD87
  GLD87 -->|two linear Schur residuals / complete common-row kernel| GLD88
  GLD88 -->|P=0 and d0 overlap seven-minor closure| GLD89
  GLD89 -->|alternate/auxiliary pivots, residual curve, and T-boundary closure| GLD90
  GLD90 -->|direct L1/L2 rank-seven divisors and exceptional fibres| GLD93
  GLD85 -->|exact Q(i) two-leaf residual elimination and fibre boundary cover| GLD91
  GLD90 -->|exact two-minor Q6 boundary cover inside GLD88 family| GLD92
  GLD18 -->|response-map-zero support refinement| GLD19
  GLD19 -->|common-shore global support refinement| GLD20
  GLD20 -->|complete-clique dead-colour refinement| GLD21
  GLD21 -->|common private cross-matching integrability| GLD22
  GLD22 -->|all colour-dependent private permutations| GLD23
  GLD23 -->|balanced two-matching switch| GLD24
  GLD24 -->|two-independent-amplitude completion| GLD25
  GLD25 -->|one directed support edge / generic cut| GLD26
  GLD26 -->|uv=-1 divisor closure| GLD27
  GLD26 -->|uv=1 divisor closure| GLD28
  GLD26 -->|uv-u-v-1 divisor closure| GLD29
  GLD26 -->|uv+vw+w+1 divisor closure| GLD30
  GLD30 -->|add reverse support edge / generic cut| GLD31
  GLD31 -->|uv=-1 generic divisor refinement| GLD32
  GLD32 -->|u=1 residual surface closure| GLD33
  GLD32 -->|z=1 residual surface closure| GLD34
  GLD32 -->|z=-1 residual surface closure| GLD35
  GLD32 -->|wz=2 residual closure / divisor completion| GLD36
  GLD31 -->|uv+wz-1 divisor closure| GLD37
  GLD31 -->|uv+wz+1 divisor closure| GLD38
  GLD31 -->|uniform two-row chart completion| GLD39
  GLD39 -->|support-drop completion / affine closure| GLD40
  GLD23 -->|all-zero private boundary| GLD40
  GLD40 -->|complete 12-parameter active slice| GLD41
  GLD23 -->|all-zero private boundary| GLD41
  GLD41 -->|first reciprocal two-active chart| GLD42
  GLD42 -->|full two-slice reciprocal-support atlas| GLD43
  GLD43 -->|five two-pair orbit certificates| GLD44
  GLD44 -->|same-tail exceptional-divisor closure| GLD45
  GLD44 -->|disjoint exceptional-divisor closure| GLD46
  GLD44 -->|reverse exceptional-divisor closure| GLD47
  GLD44 -->|same-head exceptional-divisor closure| GLD48
  GLD44 -->|chain exceptional-divisor closure| GLD49
  GLD49 -->|next support-size stratum| GLD50
  GLD50 -->|O10 exceptional-surface closure| GLD51
  GLD50 -->|O1 exceptional-surface closure| GLD52
  GLD50 -->|O4 exceptional-surface closure| GLD53
  GLD50 -->|O8 exceptional-surface closure| GLD54
  GLD52 -->|active-colour exchange / arrow reversal| GLD55
  GLD53 -->|active-colour exchange / arrow reversal| GLD56
  GLD50 -->|O11 exceptional-surface closure| GLD57
  GLD57 -->|active-colour exchange / arrow reversal| GLD58
  GLD50 -->|O6 exceptional-surface closure| GLD59
  GLD50 -->|O3 exceptional-divisor closure| GLD60
  GLD50 -->|O2 divisor closure / O7 arrow reversal| GLD61
  GLD50 -->|final O9 exceptional-divisor closure| GLD62
  GLD3 -->|constant synchronized window and three-activity supply open| GL
  GLD4 -->|target attachment / sparse syzygy / deeper depth open| GL
  GLD7 -->|pure survival / response nonvanishing / activity open| GL
  GLD8 -->|row attachment / word cover / depth-six and permanent open| GL
  GLD9 -->|individual maximal-rank survival / activity open| GL
  GLD10 -->|35-row attachment / helper forcing / permanent open| GL
  GLD11 -->|full mixed target exclusion still required| GL
  GLD12 -->|witness integration / paired M,Z / permanent open| GL
  GLD13 -->|generic absorption exclusion / activity / permanent open| GL
  GLD14 -->|legal M-row attachment / witness integration / permanent open| GL
  GLD15 -->|rank-two forcing / cover attachment / activity / permanent open| GL
  GLD16 -->|common-line and three-activity forcing open| GL
  GLD17 -->|slope/support forcing and other slopes open| GL
  GLD18 -->|operator incidence / sparse support / noncancellation open| GL
  GLD64 -->|decomposability / three-fullness / M-active supply open| GL
  GLD67 -->|genuine full-target equation / second legal axis / coefficient-pure bridge open| GL
  GLD69 -->|scalar-zero / nonsparse centre / low port ranks open| GL
  GLD70 -->|residual-boundary atlas / triangle compression open| GL
  GLD84 -->|rank-seven and lower-rank pullbacks / other charts, components, and source branches open| GL
  GLD85 -->|two-leaf slice closed; full rank-eight residual and remaining chart/component coverage open| GLD91
  GLD86 -->|three collision divisors / exact determinant-safe successor| GLD87
  GLD87 -->|H4 named principal-open successor| GLD88
  GLD88 -->|H4 P=0 and d0 boundary successor| GLD89
  GLD89 -->|H4 Q6-open low-rank successor| GLD90
  GLD90 -->|H4 Q6 and L1/L2/e boundaries / pulled-back Fitting / other branches open| GLD93
  GLD93 -->|H4 Q6/e boundaries / pulled-back Fitting / other branches open| GL
  GLD90 -->|H4 Q6 outside GLD88 / finite residual / L1/L2/e boundaries / pulled-back Fitting / other branches open| GL
  GLD91 -->|full six-leaf rank-eight residual and remaining chart/component coverage open| GL
  GLD92 -->|finite common-minor residual / full H4 Q6 outside GLD88 / L1/L2/e / Fitting / other branches open| GL
  GLD19 -->|map-zero forcing / sparse support / permanent open| GL
  GLD20 -->|F-empty / pure-absorption / legal-row exclusion open| GL
  GLD21 -->|proper-secondary / other h!=0 cells open| GL
  GLD62 -->|four-plus supports / uniform argument open| GL
  GLD36 -->|larger supports / integration open| GL
  BO1 -->|bounded witness-locus certificate still open| GL
  G0 -. route boundary .-> C2
```

## Node key

| ID | Live node and exact status | Owning theorem or programme document |
|---|---|---|
| `G0` | Original global conjecture: **UNRESOLVED** | [Problem statement](../README.md#the-conjecture) |
| `S1` | Balanced complete even deck and full-sensor/rank-drop dichotomy: **proved reduction** | [Balanced half-sensor theorem](../claims/arbitrary-order/BALANCED_HALF_SENSOR_COMPLETE_DECK_AND_WICK_GLOBALIZATION_THEOREM.md) |
| `S2E` | On a full sensor, target residuals plus empty normalization, prime-divisor regularity of only the pair components, and one symmetric Euler--hafnian recurrence per higher even subset are **necessary and sufficient** for same-graph globalization | [Cramer--Euler pair-pole gate](../claims/arbitrary-order/BALANCED_FULL_SENSOR_CRAMER_EULER_PAIR_POLE_GATE_THEOREM.md) |
| `S2J` | For each Cramer pair component, prime-divisor regularity is equivalent to finitely many nonendpoint first stresses and endpoint Hessian stresses; in ternary dimension there are `3m+6` polynomial identities per pair, and the physical block is reconstructed uniquely: **proved exact refinement** | [Pair-pole differential flatness](../claims/arbitrary-order/BALANCED_FULL_SENSOR_CRAMER_PAIR_POLE_DIFFERENTIAL_FLATNESS_THEOREM.md) |
| `S2K` | Every cleared pair first or second jet is one selected-column replacement determinant.  After target consistency, its vanishing is equivalent to a differentiated target residual lying in the span of all sensor columns except that pair column: **proved exact refinement** | [Pair-jet replacement minors](../claims/arbitrary-order/BALANCED_FULL_SENSOR_CRAMER_PAIR_JET_REPLACEMENT_MINOR_THEOREM.md) |
| `S2L` | On one projective chart, the full pair-jet gate is equivalent to only the nonpivot outside first stresses and nonpivot endpoint Hessians.  Euler syzygies recover every radial coordinate and hold directly among replacement minors; the uniform count is `(d-1)(m+d-2)`, hence `2m+2` per ternary pair: **proved exact refinement** | [Projective-minimal pair jets](../claims/arbitrary-order/BALANCED_FULL_SENSOR_CRAMER_PAIR_PROJECTIVE_MINIMAL_JET_GATE_THEOREM.md) |
| `S2M` | At `m=3`, complete `27`-row GHZ target consistency, empty normalization, rank four, deck-complement column degrees, and seven vanished retained pair coordinates are compatible with the eighth being nonzero.  Exact controls exist for all eight coordinates, but they are not proved common-shore companion matching-sum sensor realizations: **proved compatibility boundary** | [Normalized full-row controls](../claims/arbitrary-order/BALANCED_FULL_SENSOR_CRAMER_PAIR_EMPTY_NORMALIZATION_CONTROL_COMPATIBILITY_THEOREM.md) |
| `S2N` | At `m=3`, one fixed common shore is characterized exactly by nine singleton slices sharing `A_1 tensor B_23+B_13 tensor A_2+B_12 tensor A_3` and an empty sensor column equal to the six-term permanent of the same cross blocks.  A normalized target-consistent rank-four Latin-plane system lies outside this image, but imposes no retained pair jet: **proved iff and ambient separator** | [Common-shore compatibility theorem](../claims/arbitrary-order/BALANCED_FULL_SENSOR_COMMON_SHORE_SINGLETON_SLICE_AND_EMPTY_PERMANENT_COMPATIBILITY_THEOREM.md) |
| `S2O` | Project every S2M control onto its two nonzero root colours.  All eight become one binary pattern: one transverse pure singleton, zero quiet-colour singleton slices, and one quiet-colour pure empty coefficient.  Thus realization of any control requires one explicit binary image/kernel/permanent system; zero singleton slices alone do not force zero empty coefficient: **proved common residual reduction** | [Normalized control pullback](../claims/arbitrary-order/BALANCED_FULL_SENSOR_COMMON_SHORE_NORMALIZED_PAIR_CONTROL_PULLBACK_REDUCTION.md) |
| `S2P` | For three binary root spaces, a nonzero pure tensor in the common-shore singleton image and a nonzero pure tensor obtained as the polarized permanent of three singleton syzygies must share a factor line.  The S2O tensors are transverse in all three factors, so its residual is empty and none of the eight S2M controls is a common-shore realization: **proved exact obstruction** | [Binary syzygy--permanent obstruction](../claims/arbitrary-order/BALANCED_FULL_SENSOR_COMMON_SHORE_BINARY_SYZYGY_PERMANENT_RESIDUAL_OBSTRUCTION_THEOREM.md) |
| `S2Q` | At `m=3`, every divisorial pole of the normalized unique rational pair lift forces one singleton image of dimension one, one pair-image sum of dimension two, or total singleton-image span dimension three.  Outside this union every pair is a global bilinear block, so the certified six-vertex theorem makes the regular physical target-incidence stratum empty.  The three exceptional strata and all higher orders remain open: **proved localization, not S2 closure** | [`m=3` separated-singleton pole localization](../claims/arbitrary-order/BALANCED_M3_FULL_SENSOR_SEPARATED_SINGLETON_POLE_LOCALIZATION_THEOREM.md) |
| `S2R` | For any normalized physical `m=3` target incidence, the total singleton span has no fully supported decomposable root annihilator.  Such a contraction would identify a local image of the rank-four tensor `P_3` with a concise rank-three diagonal.  In the common-three-space S2Q stratum, a product-annihilator family of dimension at least three exists but is forced entirely onto the coordinate boundary: **proved obstruction, boundary classification open** | [Singleton-span torus-annihilator obstruction](../claims/arbitrary-order/BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md) |
| `S2S` | A product annihilator supplies one vector `beta`, formed from the three root--root contractions, in the kernel of all three contracted cross maps.  For `beta!=0`, the physical empty contraction factors through one common binary quotient of `P_3`; that quotient is zero, rank-three W, or rank-two GHZ as `beta` has support one, two, or three.  A two-colour target boundary forces full-support `beta`, three rank-two maps, two fully supported rank-one surviving-colour cross matrices, and a zero missing-colour matrix, while `beta=0` and rank-one-map degenerations remain: **proved orbit/rank refinement, not an exclusion** | [Boundary-annihilator common-quotient theorem](../claims/arbitrary-order/BALANCED_M3_BOUNDARY_ANNIHILATOR_COMMON_QUOTIENT_P3_ORBIT_THEOREM.md) |
| `S2T` | On the common-three-space S2Q stratum, each irreducible product-annihilator component has dimension at least three and is either contained in at least two target-coordinate divisors, has `beta=0` identically, or generically loses one colour whose three cross-column spans have total rank at most three (at most two when the boundary equation is independent).  The branches are not excluded: **proved exhaustive component trichotomy** | [Common-three-space component trichotomy](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_ANNIHILATOR_COMPONENT_TRICHOTOMY_THEOREM.md) |
| `S2U` | On the common-three-space stratum, invertibility of the joint `9 x 9` cross-colour map identifies the singleton span with the shared-derivative image.  Dimension three then forces one root block; torus blocking makes it a coordinate monomial, and the six-vertex theorem excludes every off-diagonal monomial by explicit global `2 x 2`-permanent pair blocks.  Only one diagonal monomial edge and a GHZ-modulo-root-line block-permanent equation survive.  Its invertible monomial joint-cross subcase is excluded here; S2X subsequently excludes all nonmonomial cases as well: **proved localization feeding a now-closed full-rank branch** | [Full-joint-rank monomial-root-edge localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_MONOMIAL_ROOT_EDGE_LOCALIZATION_THEOREM.md) |
| `S2V` | In the S2U sparse block-permanent branch, the exceptional root block row cannot be supported on one source summand.  The off-diagonal target zeros would give each of three complementary marked vectors two independent mixed-product zero divisors; the exact pure-or-line classification and pigeonhole contradict invertibility.  This entry alone leaves rows meeting two or three sources, which S2W--S2X subsequently exclude: **proved nonmonomial subcase exclusion** | [Source-aligned exceptional-root-row obstruction](../claims/arbitrary-order/BALANCED_M3_FULL_JOINT_CROSS_RANK_SOURCE_ALIGNED_EXCEPTIONAL_ROOT_ROW_OBSTRUCTION.md) |
| `S2W` | The S2U exceptional root row cannot be contained in the sum of two source summands.  Apart from the two pure planes handled by S2V, all two-source three-plane normal forms split the two mixed products; the resulting `(6+3)` pure-or-line zero-divisor classification contradicts complementarity: **proved two-source exclusion** | [Two-source exceptional-root-row obstruction](../claims/arbitrary-order/BALANCED_M3_FULL_JOINT_CROSS_RANK_TWO_SOURCE_EXCEPTIONAL_ROOT_ROW_OBSTRUCTION.md) |
| `S2X` | Every full-support exceptional root row is also impossible.  The off-diagonal sparse-target grid feeds a shared derivative that is either injective, forcing an impossible pure-source pigeonhole, or has the unique synchronized rank-one-pair kernel, which traps all nine joint-cross rows in a five-space.  Thus the entire joint-cross-rank-nine part of the common-three-space stratum is empty: **proved full-rank exclusion** | [Complete full-joint-cross-rank exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_EXCLUSION_THEOREM.md) |
| `S2Y` | Joint cross rank eight is also impossible.  A hyperplane image still forces the one-diagonal-monomial sparse equation.  Its regular derivative chart has a sharp four-dimensional off-diagonal zero-grid span and hence total rank at most seven; its unique exceptional chart makes both nonexceptional GHZ colours use one root covector instead of two independent covectors: **proved corank-one exclusion** | [Joint-cross-rank-eight exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_CROSS_RANK_EIGHT_EXCLUSION_THEOREM.md) |
| `S2Z` | At joint rank seven, the entire single-root-block branch is also impossible.  Equality in the S2Y zero-grid bound leaves complementary pure or conjugate-mixed marked two-planes.  Its exhaustive `P/P`, `P/M`, and `M/M` normal forms respectively force a common GHZ covector, shared target factor lines, proportional diagonal products, or a derivative pair with zero common kernel: **proved sharp-equality subcase exclusion** | [Single-root-block joint-rank-seven exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_SINGLE_ROOT_BLOCK_JOINT_CROSS_RANK_SEVEN_EXCLUSION_THEOREM.md) |
| `S2AA` | The remaining two-root-block rank-seven case is impossible.  Codimension two forces exactly two rank-one root blocks with one shared coordinate endpoint factor and puts the full four-dimensional derivative kernel in the joint image.  The two unaffected GHZ slices make both involved root rows globally rank three and generically invertible pointwise, where the slice is an invertible transform of a nonzero zero-diagonal matrix of rank at least two, not the required rank-one coordinate matrix: **proved complete rank-seven exclusion** | [Two-root-block joint-rank-seven exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_TWO_ROOT_BLOCK_JOINT_CROSS_RANK_SEVEN_EXCLUSION_THEOREM.md) |
| `S2AB` | The single-root-block branch is impossible at every joint rank.  The regular off-diagonal grid reduces to two crossed pure-or-conjugate-mixed pairs; lower-dimensional pure boundaries and the previously missing shared-line `M/M` boundary are excluded by common-covector, common-factor, injective-pair, and Segre-tangent arguments.  The exceptional derivative chart already has only one rank-one covector line: **proved complete physical-component exclusion** | [Complete single-root-block exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_SINGLE_ROOT_BLOCK_COMPLETE_EXCLUSION_THEOREM.md) |
| `S2AC` | At joint rank six, the shared-factor derivative-rank-five branch is impossible.  Its two unaffected GHZ slices leave four involved-row profiles: `(2,2)` misses the exceptional pure coefficient, `(3,3)` violates the zero-diagonal matrix rank floor, and the mixed profiles promote two slice zeros to crossed quadratic zero products whose pure/mixed atlas cannot carry two independent GHZ diagonal maps.  Thus the only rank-six survivor has exactly two root blocks with disjoint derivative summands: **proved subcase exclusion; transverse rank six open** | [Joint-rank-six shared-factor exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_CROSS_RANK_SIX_SHARED_FACTOR_EXCLUSION_THEOREM.md) |
| `S2AD` | In the transverse rank-six survivor, the derivative kernel is exactly the third root space and the remaining image is a three-plane.  The automatic beta-zero annihilator locus avoids the root torus only when one root block is a coordinate monomial or belongs to a sharp boundary-pencil tangent pair.  Unless the relation three-plane is already coordinate-boundary, S2R--S2S force both block contractions onto one coordinate and target consistency forces an involved row rank exactly two with the aligned coordinate kernel and diagonal block contraction: **proved localization; two coordinate boundaries open** | [Transverse-rank-six beta-zero localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_TRANSVERSE_RANK_SIX_BETA_ZERO_LOCALIZATION_THEOREM.md) |
| `S2AE` | In the non-coordinate relation branch, an aligned rank-two row makes `K_12` the graph of a rank-two map and makes the second permanent row a fixed image of the first.  The beta-zero atlas, coefficientwise target equation, and permanent symmetry force one root block to be diagonal and the other onto the graph-kernel line.  A repeated-row Segre-tangent mode-rank obstruction removes its last diagonal part; the residual would require a two-plane with zero cross product and two square maps onto distinct GHZ lines, which the exhaustive zero/one/two/three pair-tensor kernel atlas forbids: **proved aligned-boundary exclusion; coordinate relation plane open** | [Aligned-rank-two exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_TRANSVERSE_RANK_SIX_ALIGNED_RANK_TWO_EXCLUSION_THEOREM.md) |
| `S2AF` | In the coordinate-relation survivor, duality forces an involved row of rank two.  Profile `(3,2)` is a graph: equal kernel/missing colours give the prior two-square contradiction, while unequal colours reduce after an exact local projection to a binary five-product table whose full-, two-, and one-source cases all fail.  Profile `(2,2)` forces one diagonal monomial root block; the remaining square map has only a one-dimensional mixed zero-divisor space, and every nonzero rank-one mixed image shares a factor with its GHZ line.  Two independent rows contradict this.  Thus every common-three-space point has joint cross rank at most five: **proved complete joint-rank-six exclusion** | [Complete joint-rank-six exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_COMPLETE_JOINT_RANK_SIX_EXCLUSION_THEOREM.md) |
| `S2AG` | At joint rank five, the shared-factor derivative is rank-free impossible.  A two-root transverse point survives only when the uninvolved row has rank two and a kernel supported on at most two target colours; an injective third row falls to the existing three-plane obstructions.  A three-root point has a rank-seven Hilbert--Burch derivative kernel contained in the joint image.  Its `(2,2,2)` projection profile has a fully supported beta-zero product annihilator and is impossible, while `(1,2,2)`, `(1,1,2)`, and `(1,1,1)` satisfy an exact coordinate-boundary atlas: **proved rank-five localization; boundary profiles open** | [Joint-rank-five derivative and torus localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md) |
| `S2AH` | In the transverse joint-rank-five support-two boundary, if both involved rows have rank two and both root blocks are coordinate monomials, target consistency forces one canonical row table.  Its third-row two-plane annihilates all three mixed products while one square maps rank one to `T_2`.  A complete two-/three-source zero-divisor atlas shows that either the alternating separated singleton determinant vanishes or the involved and third row spaces intersect.  Full singleton rank and joint rank five exclude both outcomes: **proved exact profile exclusion; successor S2AI closes the complete support-two `(2,2)` profile, while other rank-five profiles remain open** | [Support-two double-monomial exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_DOUBLE_MONOMIAL_EXCLUSION_THEOREM.md) |
| `S2AI` | In the same support-two `(2,2)` profile, the apparent Type-II beta-zero form `B=e_i tensor z` automatically becomes the coordinate monomial `e_i tensor e_i` under the involved rank-two target-kernel row.  The resulting monomial block forces two exact relation-plane charts.  One makes a singleton coefficient tensor simultaneously vanish and absorb `T_2`.  In the other, every entry of the unrestricted block survives only as a `T_1` correction against a rank-one `T_2` square.  Full factor transversality and the two-/three-source common-zero atlas kill the corrections and then the alternating singleton determinant: **proved complete support-two `(2,2)` exclusion** | [Support-two `(2,2)` complete exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_TWO_BY_TWO_COMPLETE_EXCLUSION_THEOREM.md) |
| `S2AJ` | In the support-two mixed involved-row profile, the rank-three shore makes the relation plane a graph and the rank-two shore has a coordinate kernel.  The contracted colour-one target forces that graph to miss colour two.  Its zero physical row then pins all singleton coefficient tensors to the single line `T_2`.  But the supported third-root rows `q_0,q_1` are proportional, while the corresponding fixed-pair slices differ by the independent target line `T_1`: **proved complete support-two `(3,2)/(2,3)` exclusion** | [Support-two mixed-row-rank exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_MIXED_ROW_RANK_EXCLUSION_THEOREM.md) |
| `S2AK` | In the remaining support-two `(3,3)` graph profile, the two contracted diagonal targets preserve the supported coordinate plane and the full kernel contraction confines every singleton correction to `D_01=span(T_0,T_1)`.  Coefficientwise permanent symmetry fixes the third graph column on colour two.  The complete target table then gives a rank-one `T_2` square and three mixed maps into the fully transverse binary diagonal plane.  The exact two-/three-source common-zero atlas forces the alternating singleton determinant to vanish: **proved complete support-two `(3,3)` exclusion; all support-two involved-row profiles closed** | [Support-two `(3,3)` exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_THREE_BY_THREE_EXCLUSION_THEOREM.md) |
| `S2AL` | In the support-one boundary, the `(3,3)` graph contraction is injective and every singleton correction lies on `T_2`; a mixed graph's complete zero row forces the same correction line and makes its rank-two shore miss colour two.  Permanent symmetry reduces the invertible and equal-kernel charts to two repeated squares on a two-plane.  Tangent-line separation and an exact two-source/three-source atlas forbid two fully transverse square images.  The unequal-kernel mixed chart is the inherited binary five-product obstruction: **proved support-one `(3,3)/(3,2)/(2,3)` exclusion; successor handles `(2,2)`** | [Support-one higher-row-rank exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md) |
| `S2AM` | In the final support-one `(2,2)` profile, the two involved zero rows determine every singleton correction, force distinct missing colours, and put the relation three-plane in one exact normal form.  The support colour is one missing colour.  The untouched third-colour square has rank one, while all three mixed maps land in the plane spanned by the other two fully transverse targets.  The binary-diagonal-plane common-zero atlas kills the alternating singleton determinant: **proved complete support-one `(2,2)` exclusion; all transverse two-root joint-rank-five profiles closed** | [Support-one `(2,2)` complete exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_TWO_BY_TWO_COMPLETE_EXCLUSION_THEOREM.md) |
| `S2AN` | In the Hilbert--Burch `(1,1,1)` profile, if two rank-one triangle factors use the same target coordinate `e_s`, a nonzero same-colour coordinate of the third factor would expose an untouched binary target cube on three two-planes inside one three-space.  Equal planes violate the exact two-plane square lemma; pairwise-distinct planes violate the independent-normal or pencil-normal cubic polarization kernel.  Therefore the third factor lies in the complementary coordinate plane and the all-same-coordinate triangle is impossible: **proved repeated-coordinate localization; successor chain closes this chart** | [Hilbert--Burch repeated-coordinate localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_REPEATED_COORDINATE_LOCALIZATION_THEOREM.md) |
| `S2AO` | On the complementary plane left by S2AN, a genuinely two-supported third factor gives one contracted row with nonzero values `T_u,T_v` on the two diagonal root pairs and the same-colour row with a zero binary table.  The latter row cannot vanish because then both the all-cross term and every singleton correction would miss the required `(s,s,s)` target.  The resulting three two-planes in one three-space violate either the distinct-normal cubic kernels, the two-square lemma, or an equal-plane singularity.  Thus every repeated-coordinate chart has factor-line pattern `(s,s,t)` with `s!=t`: **proved exact support localization; successor S2AP excludes the discrete residual** | [Repeated-coordinate support localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_REPEATED_COORDINATE_SUPPORT_LOCALIZATION_THEOREM.md) |
| `S2AP` | For the discrete pattern `(s,s,t)`, the seven-dimensional annihilator of the Hilbert--Burch derivative kernel maps onto the common three-space with four-dimensional kernel.  The S2R root-torus obstruction forces that relation space into one coordinate hyperplane, hence forces one of seven rows to be a coloop.  All coloop orientations fail by the S2AL two-square lemma, a direct missing-target coefficient, or an exact binary-cubic quadratic-annihilator factor-sharing lemma: **proved complete repeated-coordinate `(1,1,1)` exclusion; other Hilbert--Burch charts open** | [Repeated-coordinate exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_REPEATED_COORDINATE_EXCLUSION_THEOREM.md) |
| `S2AQ` | For `x=lambda e_0`, `y=mu e_1`, `z=nu e_2`, the seven-dimensional Hilbert--Burch annihilator again maps onto a three-space with four-dimensional relation kernel.  S2R torus self-recovery forces a coloop.  The complete untouched binary cube is zero while its three exterior faces carry `T_0,T_1,T_2`: a combined-row coloop contradicts the totally cubic-zero two-plane factor atlas, and every ordinary-row coloop contradicts the quadratic-annihilator fork lemma: **proved all-coordinate-distinct `(1,1,1)` exclusion; successor S2AR closes the residual chart** | [All-coordinate-distinct exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ALL_COORDINATE_DISTINCT_EXCLUSION_THEOREM.md) |
| `S2AR` | For `x=lambda e_0`, `y=mu e_1`, and noncoordinate `z`, the Hilbert--Burch relation kernel avoids an eight-hyperplane torus open set.  Each resulting hyperplane alternative makes two of the exact row planes `R,P,Q` equal.  Equal `R,P` violates a square-zero mixed-factor lemma; the two ordinary-coloop orientations for equal `P,Q` violate transverse target-line independence or the S2AL pointwise tangent-factor lemma, and equal `R,Q` is symmetric: **proved two-coordinate/noncoordinate exclusion; complete `(1,1,1)` profile closed** | [Two-coordinate/noncoordinate exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_TWO_COORDINATE_NONCOORDINATE_EXCLUSION_THEOREM.md) |
| `S2AS` | In the `(1,1,2)` central coordinate-pair chart `x=lambda e_s`, `y=mu e_t`, exact transpose recovery has scalar `gamma(z)gamma(w)`.  S2R forces the four-dimensional relation kernel into one of nine hyperplanes.  The three combined-row and two recovery-factor alternatives make the first and second row planes equal; the same-colour case violates the S2AL two-square lemma, while the distinct-colour case violates an exact pure/two-source/three-source split-centre factor atlas.  Away from `w parallel e_s` and `z parallel e_t`, only four ordinary first-/second-root coloops remain: **proved central-chart localization; profile open** | [`(1,1,2)` central-coordinate torus localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_CENTRAL_COORDINATE_TORUS_LOCALIZATION_THEOREM.md) |
| `S2AT` | In the distinct-colour central chart, a third-colour first-root coloop puts `r_t`, the complete second-row plane, and every combined third row in one two-plane `S`.  The third-row image still has dimension three.  Its zero `r_t x S x Q` table upgrades a nonzero exterior `T_t` face to a square.  Three-source support has square kernel dimension two; two-source support would kill that square; and pure support either puts three independent target factor lines in `S` or makes the transverse `T_s,T_u` share a factor with `T_t`.  First/second-root symmetry excludes the mate: **proved exclusion of `alpha_u,beta_u`; central-colour coloop orbit and other `(1,1,2)` boundaries open** | [`(1,1,2)` third-colour coloop exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_THIRD_COLOUR_COLOOP_EXCLUSION_THEOREM.md) |
| `S2AU` | In the remaining central-colour coloop orbit, `r_t` lies outside a two-plane `S` but its complete `S x Q` row is zero and `dim Q=3`.  The exterior `T_t` face becomes a square.  Pure support forces a zero or factor-sharing core; two-source support confines `Q` to a two-dimensional fibre.  For full support, the square belongs to the Segre tangent at its repeated row: the two-supported square and every full-supported pair-sum degeneration leave either only a one-dimensional common annihilator or a core target sharing a factor with `T_t`.  Root symmetry closes the mate: **proved distinct-colour central-coordinate chart exclusion away from the two repeated outer lines; profile open** | [`(1,1,2)` central-colour coloop exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_CENTRAL_COLOUR_COLOOP_EXCLUSION_THEOREM.md) |
| `S2AV` | On one repeated outer divisor, say `w parallel e_s` but `z not parallel e_t`, transpose recovery becomes `nu gamma(z)gamma_s`.  The combined-row alternatives fail by a new one-face equal-plane lemma using only the surviving `T_t` face and untouched `T_u` core.  Four ordinary coloops remain.  The first-root orientations fall to one-sided square/core refinements of S2AT--S2AU; the second-root orientations fall to exact common-radical and complete-zero-rectangle atlases constrained by the nonzero full-sensor alternating tensor.  Every surviving decomposable exterior value shares a core factor, contradicting target transversality.  Root symmetry excludes the mate divisor: **proved exclusion of exactly-one-repeated outer divisors; only their simultaneous intersection remains in the distinct-colour central chart** | [`(1,1,2)` repeated-outer-factor divisor exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_REPEATED_OUTER_FACTOR_DIVISOR_EXCLUSION_THEOREM.md) |
| `S2AW` | At the simultaneous repeated intersection, transpose recovery has the seven distinct factors `alpha_t,alpha_u,beta_s,beta_u,gamma_s,gamma_t,gamma_u`.  A combined-row alternative makes the first and second row planes equal, but a three-dimensional radical shore cannot carry the resulting nonzero rank-one square.  A third-colour coloop puts `q_u=h_u` in incompatible sum/difference rulings.  A central-colour coloop has one exact two-source zero-rectangle normal form; the full coefficientwise correction identity then forces `T_s` or `T_t` to share two factor lines with `T_u`: **proved simultaneous-intersection exclusion; complete distinct-colour central coordinate-pair chart closed** | [`(1,1,2)` double-repeated intersection exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_DOUBLE_REPEATED_OUTER_INTERSECTION_EXCLUSION_THEOREM.md) |
| `S2AX` | In the same-colour central chart, S2AS leaves four symmetric ordinary coloops and the third-row image has dimension three.  In one orientation, write the surviving first-row vector as `c p_a+d p_b` in the second-row plane.  For `cd!=0`, the untouched table gives a rank-one square and rank-one mixed map onto fully transverse targets, contrary to the S2AL tangent lemma.  At `d=0`, a square-zero row cannot carry two transverse rank-one mixed targets; at `c=0`, a rank-one square cannot have two independent radical rows while the full-sensor alternating tensor is nonzero: **proved complete same-colour central-chart exclusion; both central coordinate-pair charts closed** | [`(1,1,2)` same-colour central-chart exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_SAME_COLOUR_CENTRAL_CHART_EXCLUSION_THEOREM.md) |
| `S2AY` | In an outer chart `x=lambda e_s`, `w=nu e_t`, recovery has scalar `nu gamma(z)gamma_t`; S2R forces a coordinate coloop among the nine root coordinates.  The exact face `alpha_s=beta(y)=0` carries the complementary fully transverse targets `T_a,T_b`.  Equal-plane cases and generic first-/second-root coloops reduce to the S2AL/S2AX square--mixed forks.  When `y_s=0`, a square-zero radical bridge and a radical-plane two-target lemma exclude the two support-degenerate endpoints.  Root exchange closes `(y,z)`.  Since the S2AG Boolean atlas is the union of the central and two outer coordinate-pair charts: **proved complete `(1,1,2)` profile exclusion** | [`(1,1,2)` outer-coordinate-chart exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_OUTER_COORDINATE_CHART_EXCLUSION_THEOREM.md) |
| `S2AZ` | In the `(1,2,2)` profile, root symmetry selects `x=lambda e_s`, `c=mu e_t`; an exact kernel-generator gauge sets `y_t=0` without changing the Hilbert--Burch blocks.  Transpose recovery is `lambda mu alpha_sbeta_t`, so S2R forces one of nine ordinary coordinate coloops.  The first-row map on `e_s^perp` is injective by a complete target-contraction argument.  Hence the `alpha_s`, all three `beta_j`, and all three `gamma_k` complements have the same two-plane image `R`; only `alpha_a,alpha_b` require separate first-root-coloop normal forms: **proved complete `(1,2,2)` coordinate-coloop localization; all nine orientations open** | [`(1,2,2)` coordinate-coloop localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_COORDINATE_COLOOP_LOCALIZATION_THEOREM.md) |
| `S2BA` | Under the distinguished `beta_t` coloop, exact target contraction makes the second- and third-root row maps injective.  The complete face `beta_t=gamma(w)=0` lies in one at-most-three-space.  If `w_t!=0`, it is the forbidden S2AN binary diagonal cube; if both complementary coordinates of `w` are nonzero, it is the forbidden S2AO same-third-row table.  Thus `w` is coordinate.  Two auxiliary derivative-zero faces force `y` coordinate when `s=t` and make `span(z,w)` contain a coordinate different from `e_s`: **proved `beta_t`-coloop support localization; two coordinate endpoints open** | [`(1,2,2)` `beta_t`-coloop support localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_BETA_T_COLOOP_SUPPORT_LOCALIZATION_THEOREM.md) |
| `S2BB` | At either coordinate endpoint `w=e_a`, the complete face has one surviving cell on the exact three-space `S=R direct-sum span(A)`: `per(S,p_a,span(q_b,q_t))=0`, `per(S,p_b,q_t)=0`, but `per(-,p_b,q_b)` is nonzero.  Splitting `p_a` by source support, full support collapses `S` to a line, two-source support either collapses the partner plane or kills every permanent on `S`, and pure support makes both partner maps vanish together: **proved complete exclusion of the distinguished `beta_t` coloop orientation** | [`(1,2,2)` `beta_t`-coloop coordinate-endpoint exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_BETA_T_COLOOP_COORDINATE_ENDPOINT_EXCLUSION_THEOREM.md) |
| `S2BC` | Under the distinguished `alpha_s` coloop, a projective pencil of determinant-zero product faces puts `R,p(P_delta),q(Q_delta)` in one at-most-three-space.  Their two coordinate-projection gates cannot both be nonzero by the S2AN binary cube.  Exact polynomial factorization leaves `s!=t,y_s=0` or `z_s=w_s=0`; either one-sided degeneration is the S2AO same-third-row table.  Their intersection gives two fully transverse targets sharing one second/third-row pair.  Independent normals, pencil normals, and every equal-plane incidence contradict the cubic kernels, a singular change matrix, or S2AL tangent-line separation: **proved complete exclusion of the distinguished `alpha_s` coloop orientation** | [`(1,2,2)` `alpha_s`-coloop exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_ALPHA_S_COLOOP_EXCLUSION_THEOREM.md) |
| `S2BD` | Under either residual second-root coloop `beta_j`, `j!=t`, the complete face `beta_t=gamma(w)=0` puts the first- and third-row binary planes and the complementary second row in the exact three-space `S=R direct-sum span(A)`; only the selected row `p_j` may escape.  If `w_t!=0`, the face is a binary diagonal table.  Tangent-line and mixed-factor arguments force the intersection of the two in-space planes to be a coordinate endpoint in both.  Four endpoint pairs and seven nonzero support masks give 28 exhaustive normal forms, each excluded by a pinned rational Nullstellensatz identity: **proved `w_t=0` support localization for both residual `beta_j` coloops; neither coloop excluded** | [`(1,2,2)` residual second-root-coloop support localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_SUPPORT_LOCALIZATION_THEOREM.md) |
| `S2BE` | Continue either residual `beta_j` coloop from S2BD.  If both complementary coordinates of `w` are nonzero, the complete face is a same-third-row binary diagonal table whose first and third planes and complementary middle row lie in `S`; only the selected middle row may escape.  The zero third row is forced to equal the intersection of the two in-space planes.  Fourteen endpoint-support, five generic fixed-support, and two genuine one-parameter row-space families exhaust the residual; pinned rational Nullstellensatz identities exclude all 21, with the parameter identities holding polynomially for every parameter value: **proved coordinate-line localization for both residual `beta_j` coloops; four ordered endpoints open** | [`(1,2,2)` residual second-root-coloop coordinate-line localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_COORDINATE_LINE_LOCALIZATION_THEOREM.md) |
| `S2BF` | Under either residual `beta_j` coloop, the seven canonical annihilator rows force the selected row `p_j` genuinely outside `S`.  On every determinant-face pencil member, the first- and third-row planes and a nonzero line of the middle plane lie in one at-most-three-space.  A strengthened binary-diagonal obstruction handles an arbitrary, non-coordinate middle intersection: four ordered plane endpoints and seven support masks give 28 exact normal forms, all excluded by pinned rational Nullstellensatz identities.  Projective factorization and an auxiliary face then give `s=t => z_t=0`, `s=l => y parallel e_m and z_m z_t=0`, and `s=m => y_m z_m=0` at an endpoint `w=e_l`: **proved residual-coloop projective-pencil and endpoint-support localization; four ordered endpoints still open** | [`(1,2,2)` residual second-root-coloop projective-pencil localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_PROJECTIVE_PENCIL_LOCALIZATION_THEOREM.md) |
| `S2BG` | At a residual coordinate endpoint with `s=t`, S2BF gives `z_t=w_t=0`, so `z,w` form a basis of the complementary coordinate plane.  A generic determinant-pencil member has one active third row with both complementary coordinates and the zero row `q_t`; its middle plane has an arbitrary nonzero intersection with the common three-space.  A strengthened same-third-row obstruction has 14 endpoint-support, five generic fixed-support, and two polynomial parameter families, all excluded by pinned rational identities: **proved exclusion of every residual endpoint with `s=t`; surviving endpoints have `s in {j,k}`** | [`(1,2,2)` residual second-root-coloop `s=t` endpoint exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_S_EQUAL_T_ENDPOINT_EXCLUSION_THEOREM.md) |
| `S2BH` | At a surviving endpoint let `u` be the coordinate complementary to `s,t`.  If `w=e_s`, the S2BF projective fork directly gives `y_s=0`.  If `w=e_u`, assuming `y_s!=0` forces `z_s=w_s=0`; a generic pencil member is then the generalized same-third-row table excluded by S2BG.  Since `y_t=0` and `y,e_t` are independent: **proved `y` is proportional to `e_u` at every residual endpoint; endpoints remain open** | [`(1,2,2)` residual second-root-coloop complementary-`y` localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_COMPLEMENTARY_Y_COORDINATE_LOCALIZATION_THEOREM.md) |
| `S2BI` | With `y` on the complementary coordinate, every determinant-pencil member outside `z_s=w_s=0` gives two fully transverse targets sharing the active middle row while the middle plane has only a nonzero common-space intersection.  Ten first/third-plane incidences, three middle-line positions, and three exact affine patches give 90 normal forms; pinned rational identities exclude all of them.  Thus **every residual endpoint is localized to `w=e_u`, `z_s=0`, `z_t!=0`; that terminal chart remains open** | [`(1,2,2)` residual second-root-coloop common-middle-row localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_COMMON_MIDDLE_ROW_LOCALIZATION_THEOREM.md) |
| `S2BJ` | The S2BI terminal chart gives two fully transverse targets sharing the active middle/third pair.  If the selected residual colour is `s`, those active rows cancel modulo `R`; if it is the complementary colour `u`, the inactive middle row lies in `R`.  An equal-plane symmetry contradiction and a complete `9+6=15` polynomial row-space cover, with pinned rational identities, exclude both alternatives: **proved exclusion of both residual second-root `beta_j` coloops** | [`(1,2,2)` residual second-root-coloop exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_EXCLUSION_THEOREM.md) |
| `S2BK` | Under any selected `gamma_k` coloop, the complete face `beta_t=gamma(w)=0` puts its first and second binary row planes in `S=R direct-sum span(A)` and gives the third plane a nonzero intersection with `S`.  For `w_t!=0`, the S2BF arbitrary-intersection binary-diagonal obstruction applies.  For `w_t=0` with complementary support two, the S2BI common-active-row obstruction applies.  If `w` is coordinate, exchanging roots two and three sends `gamma_k=0` to one of the second-root coloops closed by S2BB and S2BJ: **proved exclusion of all three third-root `gamma_k` coloops** | [`(1,2,2)` third-root-coloop exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_THIRD_ROOT_COLOOP_EXCLUSION_THEOREM.md) |
| `S2BL` | Under either complementary `alpha_a` coloop, the determinant-zero `alpha_s=0` pencil has both partner planes in an at-most-three-space and its first plane meets that space in `r_b`.  S2BF forces `s!=t,y_s=0` and `z_s=w_s=0` simultaneously; S2BE excludes either one-sided degeneration.  At their intersection the selected coloop plane contains `r_b,p_s,q_s,p_*+q_*`.  Equal partner planes fail by S2AL, the all-in-space boundary is S2BC, and the remaining equal/distinct inactive-line incidences have exactly `2+3=5` polynomial normal forms, all excluded by pinned rational identities: **proved exclusion of both complementary first-root coloops; complete `(1,2,2)` profile closed** | [`(1,2,2)` complementary first-root-coloop exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_COMPLEMENTARY_FIRST_ROOT_COLOOP_EXCLUSION_THEOREM.md) |
| `S2BM` | At joint rank three or four with two transverse root blocks, the uninvolved row has rank one or two and the row-space incidences are exactly `Q subset V` for rank three, disjoint `V,Q` for `(4,1)`, or line intersection for `(4,2)`.  Every kernel vector has support at most two.  Rank one forces a coordinate kernel plane, complementary diagonal root blocks, and a one-cell permanent grid.  Exact physical controls populate both `(3,1)` and `(4,1)` with full sensor rank and all target rows, but their unique pair lifts have explicit coordinate poles: **proved localization and sharp controls, not an exclusion** | [Lower-joint-rank transverse localization and pole controls](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_LOWER_JOINT_RANK_TRANSVERSE_TWO_ROOT_LOCALIZATION_AND_POLE_CONTROLS_THEOREM.md) |
| `S2BN` | At joint rank four and uninvolved-row rank two, `V` and `Q` meet in exactly one line, so `Q` is not contained in `V`.  A strengthened exact common-zero lemma shows that any rank-one square plus fully transverse diagonal-plane mixed corrections has zero alternating singleton tensor whenever `Q` is not contained in `V`: the sole old intersection-sensitive conjugate chart forces its second `Q` generator into `V`.  Incidence-free transfers close the higher-row profiles, and the strengthened lemma closes the remaining `(2,2)` and support-two `(3,3)` profiles: **proved complete exclusion of the joint-rank-four `q=2` transverse cell** | [Joint-rank-four uninvolved-rank-two complete exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_TRANSVERSE_TWO_ROOT_UNINVOLVED_RANK_TWO_COMPLETE_EXCLUSION_THEOREM.md) |
| `S2BO` | At joint rank three and uninvolved-row rank two, `Q subset V`.  The exact common-zero atlas leaves only the two-source conjugate chart.  Since every empty value is then on one pure target, the other two target diagonals force complementary coordinate-monomial root blocks and both involved row ranks two.  The source chart normalizes to `a=-2y+t`, `b=2x-t`, `v=x+y`, `w=x-y`, `q=(x+y+t)/2`; one missing third row or two proportional rows give the two kernel supports.  Exact local controls populate both, but the exhaustive unique pair lift has unavoidable poles on `xyt=0`, so the Cramer--Euler gate excludes every regular graph extension: **proved complete exceptional atlas and graph-cell exclusion** | [Joint-rank-three q=2 exceptional normal form and pole controls](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_THREE_TRANSVERSE_TWO_ROOT_UNINVOLVED_RANK_TWO_EXCEPTIONAL_NORMAL_FORM_AND_POLE_CONTROLS_THEOREM.md) |
| `S2BP` | In both remaining uninvolved-row-rank-one cells, S2BM's one-cell square has an exhaustive two-/three-source Segre-tangent atlas.  Its common-zero kernels make the singleton determinant carry one, two, or all three missing-colour coordinate factors.  A global pair Cramer numerator omits the corresponding source coordinate; the two-factor residues contradict the two coprime residual targets or the nonzero third singleton row.  In the sole one-factor chart, a vanishing numerator would kill the alternating singleton determinant.  Hence every point has a prime-divisor pair pole and the Cramer--Euler gate excludes every regular graph extension: **proved complete pair-pole exclusion of the joint-rank-three/four `q=1` cells** | [Lower-joint-rank q=1 complete pair-pole exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_LOWER_JOINT_RANK_TRANSVERSE_TWO_ROOT_UNINVOLVED_RANK_ONE_COMPLETE_PAIR_POLE_EXCLUSION_THEOREM.md) |
| `S2BQ` | With all three root blocks nonzero at joint rank three or four, the shared derivative has rank `9`, `8`, or `7`.  Rank four cannot have rank nine.  Rank eight is exactly one two-supported shared-factor syzygy plus a residual block outside its tangent plane; root-torus blocking gives an iff coordinate/monomial quotient atlas.  Rank seven is Hilbert--Burch: `(2,2,2)` is impossible at every rank, and the other projection profiles obey the rank-independent S2AG coordinate atlas.  The exact preimage table records full/line/zero kernel incidence without importing rank-five containment: **proved complete lower-rank three-root derivative and torus localization, surviving target cells open** | [Lower-joint-rank three-root derivative and torus census](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_LOWER_JOINT_RANK_THREE_ROOT_DERIVATIVE_AND_TORUS_CENSUS_THEOREM.md) |
| `S2BR` | In the joint-rank-four derivative-rank-eight chart, the shared syzygy lies in `K`.  Complete empty-target contraction forces every root-row rank to be at least two.  A deficient first/second row has one coordinate kernel and the matching nonzero diagonal row/column of `C`; a deficient third row has one-/two-colour support represented by `x,y` and is nonzero on `w`.  If both involved rows have rank two, distinct missing colours make one pure-target correction preimage have a third component that the two contractions force simultaneously nonzero and zero: **proved target-row atlas and complete exclusion of the distinct-missing-colour `(2,2)` subcell** | [Rank-four/rank-eight target-kernel atlas](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_TARGET_KERNEL_ATLAS_AND_DISTINCT_MISSING_COLOUR_EXCLUSION_THEOREM.md) |
| `S2BS` | In the same-missing-colour `(2,2,2)` survivor, the exact coordinate split lift with `x=w=e_s`, `y=e_t`, `C=e_d e_d+e_s e_s`, and the displayed four-space `K` has an eight-dimensional root-permanent quotient disjoint from `U`.  The three target diagonals reduce to two quotient vectors, forcing six polarized source products to vanish and two to equal fully transverse `T_d,T_t`.  A rank-free eight-product lemma excludes this by exhausting the one-/two-/three-source support of the repeated vector: **proved complete exclusion of the coordinate split-lift cell; S2BT later makes the lift atlas exhaustive** | [Same-colour coordinate split-lift exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_RANK_TWO_COORDINATE_SPLIT_LIFT_EXCLUSION_THEOREM.md) |
| `S2BT` | In every same-missing-colour `(2,2,2)` point with coordinate third-row kernel `e_s^*`, the `T_d` correction first fixes its third component and then puts its first two components on the shared syzygy, forcing `(0,0,e_d) in K`; the `T_s` correction similarly forces `(0,e_s,0) in K`.  Projection rank gives two exhaustive nonaligned/aligned four-space charts.  Their polarized root permanents span explicit eight-dimensional boxes, disjoint from `U` on the nonmonomial residual-block branch: **proved exhaustive support-one split-lift atlas; nonsplit missing-colour lifts impossible** | [Same-colour support-one split-lift atlas](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_SUPPORT_ONE_SPLIT_LIFT_ATLAS_THEOREM.md) |
| `S2BU` | In S2BT's aligned chart, the root box meets `U` trivially for every `C_bar` and every `w` nonzero on the missing third-row colour.  The `ttt` target makes `g_3` fully supported; `stt=tst=0` put `g_0,g_2` in the two-dimensional kernel of `h -> P(h,g_3,g_3)`.  The `ttd` coefficient lies in the Segre tangent at `T_t` and cannot equal a nonzero multiple of transverse `T_d`, so `g_1` joins the same kernel.  Four dual rows then span at most three dimensions: **proved complete aligned-chart exclusion, including monomial `C` and noncoordinate `w`** | [Aligned support-one split-lift exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_SUPPORT_ONE_ALIGNED_SPLIT_LIFT_EXCLUSION_THEOREM.md) |
| `S2BV` | In S2BT's nonaligned chart, the eight root coefficients have a complete two-/three-source atlas.  Four-row independence forces every local solution into one same-source two-plane family with `C_bar=0`, `w=e_s`, and coordinate fourth lift.  These are exact generic-rank-four empty-target controls.  Their singleton determinant is `-2 mu x_t y_t r`; the unique pair lift has `x_t,y_t` denominators, and cancelling both residues would equate the distinct `x_s y_s` and `x_d y_d` monomials.  Hence every control has a pair pole: **proved complete nonaligned graph-extension exclusion; coordinate-third-kernel same-colour `(2,2,2)` cell closed** | [Nonaligned source atlas and pair-pole exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_SUPPORT_ONE_NONALIGNED_SOURCE_ATLAS_AND_PAIR_POLE_EXCLUSION_THEOREM.md) |
| `S2BW` | If the third-row kernel in the same-colour `(2,2,2)` cell has both complementary colours in its support, first-`d` contraction fixes the `T_d` preimage vertically and gives zero third components for the `T_s,T_t` preimages.  Contracting by the support-two kernel then forces `(0,e_s,0)` and `(e_t,0,0)` modulo the shared syzygy.  These four independent vectors fill `K` but have third projection rank one, contradicting rank two.  With S2BU--S2BV handling support one: **proved complete same-colour `(2,2,2)` rank-two-third-row profile exclusion** | [Support-two third-row exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_SUPPORT_TWO_COMPLETE_EXCLUSION_THEOREM.md) |
| `S2BX` | In the same-colour `(2,2,3)` cell, the missing involved row reduces the complete correction to one pure source line.  A nonzero residual would map rank-four `P_3` invertibly to a rank-three concise diagonal, so the empty permanent is exactly binary and `q_d` is a common zero.  Every plane obtained by shifting `q_s,q_t` along `q_d` carries the same binary frame; the exact intersecting-plane obstruction makes all of them transverse to both involved planes.  Four-space dimension then forces `q_d` into both involved planes, a contradiction: **proved complete same-colour `(2,2,3)` exclusion; all same-colour `(2,2,q)` profiles closed** | [Third-row-rank-three complete exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_RANK_THREE_COMPLETE_EXCLUSION_THEOREM.md) |
| `S2BY` | The S2BX correction and shift proof needs only one deficient involved row when the third row is injective.  Restricting the other injective involved row to the two complementary colours still gives a binary plane; the exact same shifted-frame contradiction excludes `(2,3,3)` and, by root exchange, `(3,2,3)`: **proved complete one-deficient-involved-row, third-row-rank-three exclusion** | [One-deficient-row injective-third-row exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_ONE_DEFICIENT_INVOLVED_ROW_THIRD_ROW_RANK_THREE_COMPLETE_EXCLUSION_THEOREM.md) |
| `S2BZ` | With one deficient involved row and a support-two third kernel, first-missing-row contraction puts every non-`T_d` correction in the derivative image of `ker(pr_3|K)`, which is one-dimensional modulo the shared syzygy.  Third-kernel contraction would make that same nonzero root tensor proportional to both complementary diagonal tensors: **proved complete one-deficient-involved-row support-two exclusion; mixed `(2,3,2)/(3,2,2)` support-two cells closed** | [One-deficient-row support-two exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_ONE_DEFICIENT_INVOLVED_ROW_THIRD_ROW_SUPPORT_TWO_COMPLETE_EXCLUSION_THEOREM.md) |
| `S2CA` | With one deficient involved row and a coordinate third kernel, the pure target corrections force a vertical lift and the unique projection-compatible split orientation.  The direct twelve-entry root box makes four third-`t` coefficients produce a cubic resonance frame.  Two missing-colour coefficients then put two polarized products both in the Segre tangent at `T_t` and on the fully transverse `T_d` line; their exact common kernel makes two independent dual rows proportional: **proved complete mixed support-one exclusion; every rank-four/rank-eight profile with a deficient involved row is closed** | [One-deficient-row support-one exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_ONE_DEFICIENT_INVOLVED_ROW_THIRD_ROW_SUPPORT_ONE_COMPLETE_EXCLUSION_THEOREM.md) |
| `S2CB` | In the fully injective `(3,3,2)` profile, a vertical third lift lowers an involved projection.  Without one, the eighteen-dimensional root box is disjoint from `U`; the rank-four `P_3` obstruction forces a supported target cube into `U`.  Support one gives an equal-plane binary frame.  Support two reduces by outer permanent symmetry and mixed-factor sharing to either the same binary frame or two fully transverse rank-one squares with zero mixed map: **proved complete `(3,3,2)` exclusion; only `(3,3,3)` remains in the rank-four/rank-eight row census** | [Fully-injective third-row-rank-two exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_INVOLVED_ROWS_THIRD_ROW_RANK_TWO_COMPLETE_EXCLUSION_THEOREM.md) |
| `S2CC` | In the last fully injective `(3,3,3)` profile, the joint preimage is a graph over the third root space.  Contracting the complete target identity on `w^perp` gives an exact two-root slice.  If `C=lambda e_d tensor e_e` and `w_d!=0`, the complementary colours form an exact binary diagonal frame while `p_d` is a nonzero common zero.  A four-space shift transfers the S2BF intersecting-plane obstruction and excludes it; root exchange similarly excludes `w_e!=0`: **proved monomial endpoint localization `w_d=w_e=0`; S2CD--S2CK subsequently close every monomial endpoint** | [Fully-injective monomial-residual endpoint localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_MONOMIAL_RESIDUAL_ENDPOINT_LOCALIZATION_THEOREM.md) |
| `S2CD` | At the diagonal S2CC endpoint `C=lambda e_d tensor e_d`, a `w` with both complementary coordinates nonzero gives an exact same-third-row binary table with the physical common rows `p_d,r_d`.  S2BG separation, common-row shifts, tangent/mixed-factor incidence, and a complete four-quotient/Borel census reduce the row space to 29 polynomial charts.  Exact rational Nullstellensatz identities, replayed by independent implementations, exclude all 29: **proved two-supported endpoint exclusion; diagonal `w` is forced onto a complementary coordinate line** | [Diagonal-monomial two-supported endpoint exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_TWO_SUPPORTED_ENDPOINT_EXCLUSION_THEOREM.md) |
| `S2CE` | At the off-diagonal S2CC endpoint `C=lambda e_d tensor e_e`, `d!=e`, the complete target slice is a two-corner binary table with one free parallel edge, two physical common rows, and their cross-zero.  A proved projective incidence/flag cover and 308 exact separation charts force both involved planes transverse to the third plane; common-row shifts then put the physical middle row in that plane.  Three quotient orbits and three common-row-line orbits give nine terminal charts.  Canonical rational Nullstellensatz identities for 287 literal systems, independently replayed, exclude all 317 logical charts: **proved complete off-diagonal monomial coordinate-endpoint exclusion** | [Off-diagonal-monomial coordinate-endpoint exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_OFF_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_EXCLUSION_THEOREM.md) |
| `S2CF` | At either remaining diagonal coordinate endpoint, the full coefficient identity splits into two recovered exceptional source slices and one unsliced equation.  The exceptional entries determine two source tensors while all sixteen other face entries remain explicit.  Gauge-free tangent tensors reduce the unsliced equation to a nonzero root factor in the affine tangent coset `C+(A_1 tensor y+x tensor A_2)` times one source tensor, equivalently all ordinary root/source flattening minors.  Contracting by `x^perp,y^perp` gives a corrected `2 x 2 x 3` cube, an exact target-visibility census, and a two-radical exclusion of its fully supported exceptional-intersection orbit.  An omission control proves that the cube is only a consequence of the complete faces, while a quotient-only realization proves the remaining full-target coupling is essential: **proved exact diagonal-endpoint full-target reduction; S2CH, S2CJ, and S2CK subsequently close both endpoints** | [Diagonal coordinate-endpoint full-target reduction](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_FULL_TARGET_REDUCTION_THEOREM.md) |
| `S2CG` | In the exact nonmonomial orbit where the three shared factors lie on one coordinate line and the actual residual block is a two-term complementary diagonal binomial, target-stabilizer normalization gives `x=y=w=e_2` and `C=kappa_0 E_00+kappa_1 E_11`.  Kernel incidence identifies the injective third-row space with the three-dimensional full-sensor row space and gives a nonzero alternating separated tensor.  The complete target supplies two mixed zero pairs and a rank-two weighted diagonal difference.  A support classification makes every independent zero pair a two-source conjugate pair; its radical bound and an exhaustive `R/P/G` nine-flag cover exclude every dependent and two-plane profile, with the generic flag falling to S2AL tangent-line separation.  The coefficient ratio and every projective boundary are retained: **proved exact canonical-binomial orbit exclusion; no general nonmonomial atlas or degeneration bridge** | [Canonical-binomial residual exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_CANONICAL_BINOMIAL_RESIDUAL_EXCLUSION_THEOREM.md) |
| `S2CH` | At either diagonal monomial coordinate endpoint, simultaneous failure of both nonexceptional target-visibility conditions forces the shared factors onto the crossed coordinate pairs `(e_0,e_1)` or `(e_1,e_0)`.  A coordinate row in one perpendicular plane then annihilates the entire other perpendicular plane in every third-row direction of the corrected cube.  Kernel incidence and third-row injectivity identify that cube with the full-sensor alternating three-space `Q`, while S2CG's support theorem bounds the radical of every nonzero row in `Q` by one dimension.  The resulting two-dimensional radical shore is impossible: **proved complete zero-visible-wall exclusion; S2CJ and S2CK subsequently close the one-visible and two-visible successors** | [Diagonal zero-visible-wall exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_ZERO_VISIBLE_WALL_EXCLUSION_THEOREM.md) |
| `S2CI` | On the two same-coordinate one-visible support cells, `x=y=e_1` or `x=y=e_0`, the corrected cube gives two cross-zero pairs and one visible target inside the full-sensor alternating three-space.  S2CG's zero-pair classification leaves only a split three-source space or coincident split two-source involved planes.  For `e_1`, the complete recovered `P_111=T_1` face contradicts both alternatives.  For `e_0`, exact source recovery and the unsliced `(0,0,0)` coefficient descend modulo the `T_1` factor lines to a false proportionality between the independent images of `T_0,T_2`: **proved exact same-coordinate one-visible-subcell exclusion; S2CJ and S2CK subsequently close the remaining visibility cells** | [Same-coordinate one-visible-wall exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_SAME_COORDINATE_ONE_VISIBLE_WALL_EXCLUSION_THEOREM.md) |
| `S2CJ` | The one-visible wall has exactly twenty ordered support masks.  S2CI closes two; four more create a forbidden two-dimensional radical shore.  Explicit perpendicular-plane bases give two cross-zero pairs on the remaining fourteen.  All seven `T_0` masks contradict the retained `P_111=T_1` face, six `T_1` masks contradict the unsliced target after exact source recovery, and the final `{0,2}` by `{0,2}` mask makes the whole unsliced root matrix force `H_2=0`; graph gauge and row injectivity then collapse both perpendicular planes to one split two-source plane, killing the visible target: **proved complete one-visible-wall exclusion; S2CK subsequently closes the two-visible successor** | [Complete one-visible-wall exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_COMPLETE_ONE_VISIBLE_WALL_EXCLUSION_THEOREM.md) |
| `S2CK` | The two-visible diagonal cell has exactly fourteen ordered support masks.  On four central masks, one correction-free mixed map contains both fully transverse target tensors; a support split and exact Segre-tangent/secant argument prove that a polarized split-cubic mixed map cannot do so.  Each of the ten boundary masks has one structural zero pair and two correction-free rank-one corners on the transverse target lines.  S2CG classifies the zero pair as independent conjugate rows or one pure dependent line, and a zero-corner rectangle obstruction forbids the two transverse corners in either case: **proved complete two-visible-cell exclusion; both diagonal monomial endpoints and the full monomial-residual branch of this cell are closed** | [Diagonal two-visible-cell exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_TWO_VISIBLE_CELL_EXCLUSION_THEOREM.md) |
| `S2CL` | For every actual nonmonomial residual in the remaining fully-injective rank-four/rank-eight cell, S2BQ makes the shared third factor coordinate and the complete target becomes two rank-one slices on the actual block `C` plus one slice on a nonzero representative of its affine tangent coset.  The perpendicular-plane contraction lies in the full-sensor alternating three-space.  Every zero-correction mixed zero is one of at most four explicit disjoint-support projective pairs; a positive-dimensional shore violates S2CG's radical bound.  A nonzero-correction zero would force a diagonal tangent-quotient pivot, then one perfect target-colour pairing on coincident split planes; quotienting one retained full slice either gives a nonzero target equal to zero or makes the actual `C` monomial: **proved complete-target zero-pair localization; correcting zeros excluded; S2CM subsequently closes the zero-pair-free successor** | [Nonmonomial complete-target zero-pair localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_NONMONOMIAL_RESIDUAL_COMPLETE_TARGET_ZERO_PAIR_LOCALIZATION_THEOREM.md) |
| `S2CM` | S2BQ's actual-nonmonomial tangent-quotient alternatives are exhausted under the assumption that the structural-zero locus is empty.  With both shared factors noncoordinate, the tangent-quotient monomial forces a correction-free two-target mixed map.  With one coordinate shared factor, the residual restriction is a nonzero `2 x 2` matrix; absence of structural zeros makes both cross entries nonzero, and its rank-one and rank-two forms each produce the same transverse secant.  S2CK forbids every case: **proved zero-pair-free-cell exclusion; every surviving point has between one and four structural mixed zero pairs** | [Nonmonomial zero-pair-free-cell exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_NONMONOMIAL_RESIDUAL_ZERO_PAIR_FREE_CELL_EXCLUSION_THEOREM.md) |
| `S2CN` | In the structural-zero successor with both shared factors noncoordinate, S2BQ's quotient monomial and S2CK force one coordinate zero shore and an exact one-sided target table.  An independent partner gives an aligned split plane or split three-space.  A dependent partner is pure; its one-factor source slab makes both shared factors have the same complementary two-support and creates a second structural corner.  S2CI's two-cross dichotomy then gives the same aligned alternatives.  In every case a target-factor quotient of a retained complete face makes the actual residual block diagonal monomial: **proved exclusion of every both-noncoordinate structural cell; any survivor has coordinate `x` or coordinate `y`** | [Nonmonomial noncoordinate-shared-factors exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_NONMONOMIAL_RESIDUAL_NONCOORDINATE_SHARED_FACTORS_EXCLUSION_THEOREM.md) |
| `S2CO` | In the remaining structural-zero successor, root exchange normalizes one shared factor to `x=e_s`.  If `y_s!=0`, the residual restriction is an exact `2 x 2` matrix whose one-cross and double-cross zero patterns are exhausted by zero-pair source geometry, shifted zero-corner obstructions, and retained complete faces.  If `y_s=0` with noncoordinate `y`, the structural map's independent/dependent split forces transverse target-factor contradictions.  If `y=e_r` is coordinate, rank one, rank two with nonzero corner, and the zero-corner rank-two pencil are all excluded; the delicate dependent pencil uses only a retained diagonal coefficient after a source projection.  Root exchange covers coordinate `y`: **proved complete coordinate-shared-factor structural-zero exclusion; the fully-injective rank-four/derivative-rank-eight actual-nonmonomial residual branch is closed** | [Coordinate-shared-factor structural-zero exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_NONMONOMIAL_RESIDUAL_COORDINATE_SHARED_FACTOR_STRUCTURAL_ZERO_EXCLUSION_THEOREM.md) |
| `S2` | Prove every realized full-sensor target incidence fails normalization, one of the retained projective pair target-column-span identities, or an Euler--hafnian recurrence.  S2P excludes the eight ambient coordinatewise controls; S2Q localizes every `m=3` pair pole to three low-span singleton strata; S2R--S2S force and classify coordinate-boundary product annihilators; S2T reduces every common-three-space component to multi-boundary, `beta=0`, or collapsed cross-column type; S2U--S2AA exclude joint cross ranks nine, eight, and seven, S2AB excludes every single-root-block case, S2AC--S2AF exclude every joint-rank-six mechanism, S2AG localizes joint rank five, S2AH--S2AK exclude every support-two involved-row profile, S2AL excludes the support-one higher-row profiles, S2AM excludes support-one `(2,2)`, S2AN--S2AR close the complete Hilbert--Burch `(1,1,1)` profile, S2AS--S2AY close the complete Hilbert--Burch `(1,1,2)` profile, S2AZ reduces `(1,2,2)` to nine coordinate coloops, S2BA--S2BB exclude the distinguished `beta_t` coloop, S2BC excludes the distinguished `alpha_s` coloop, S2BD--S2BJ exclude both residual `beta_j` coloops, S2BK excludes all three `gamma_k` coloops, and S2BL excludes both complementary `alpha_a,alpha_b` coloops.  Thus the complete transverse two-root joint-rank-five branch, the complete `(1,1,1)` and `(1,1,2)` profiles, and the complete `(1,2,2)` profile are closed.  Joint rank at most four, the other physical component types, rank-one and pair-plane pole strata, and all higher orders remain open: **open** | [S2P exact boundary](../claims/arbitrary-order/BALANCED_FULL_SENSOR_COMMON_SHORE_BINARY_SYZYGY_PERMANENT_RESIDUAL_OBSTRUCTION_THEOREM.md#7-proof-topology-consequence), [`m=3` pole localization](../claims/arbitrary-order/BALANCED_M3_FULL_SENSOR_SEPARATED_SINGLETON_POLE_LOCALIZATION_THEOREM.md#6-proof-topology-consequence), [torus-annihilator boundary](../claims/arbitrary-order/BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md#6-proof-topology-consequence), [common binary quotient](../claims/arbitrary-order/BALANCED_M3_BOUNDARY_ANNIHILATOR_COMMON_QUOTIENT_P3_ORBIT_THEOREM.md#4-remaining-boundary-and-proof-topology), [component trichotomy](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_ANNIHILATOR_COMPONENT_TRICHOTOMY_THEOREM.md#5-proof-topology-consequence), [rank-eight exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_CROSS_RANK_EIGHT_EXCLUSION_THEOREM.md#5-proof-topology-consequence), [single-root rank-seven exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_SINGLE_ROOT_BLOCK_JOINT_CROSS_RANK_SEVEN_EXCLUSION_THEOREM.md#5-rank-seven-consequence), [two-root rank-seven exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_TWO_ROOT_BLOCK_JOINT_CROSS_RANK_SEVEN_EXCLUSION_THEOREM.md#4-proof-topology-consequence), [complete single-root exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_SINGLE_ROOT_BLOCK_COMPLETE_EXCLUSION_THEOREM.md#5-proof-topology-consequence), [rank-six shared-factor exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_CROSS_RANK_SIX_SHARED_FACTOR_EXCLUSION_THEOREM.md#5-proof-topology-consequence), [transverse-rank-six localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_TRANSVERSE_RANK_SIX_BETA_ZERO_LOCALIZATION_THEOREM.md#5-proof-topology-consequence), [aligned-rank-two exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_TRANSVERSE_RANK_SIX_ALIGNED_RANK_TWO_EXCLUSION_THEOREM.md#8-proof-topology-consequence), [complete joint-rank-six exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_COMPLETE_JOINT_RANK_SIX_EXCLUSION_THEOREM.md#5-proof-topology-consequence), [joint-rank-five localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md#5-proof-topology-consequence), [support-two double-monomial exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_DOUBLE_MONOMIAL_EXCLUSION_THEOREM.md#7-proof-topology-consequence), [support-two `(2,2)` complete exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_TWO_BY_TWO_COMPLETE_EXCLUSION_THEOREM.md#6-proof-topology-consequence), [support-two mixed-row-rank exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_MIXED_ROW_RANK_EXCLUSION_THEOREM.md#4-proof-topology-consequence), [support-two `(3,3)` exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_THREE_BY_THREE_EXCLUSION_THEOREM.md#7-proof-topology-consequence), [support-one higher-row-rank exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md#5-proof-topology-consequence), [support-one `(2,2)` complete exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_TWO_BY_TWO_COMPLETE_EXCLUSION_THEOREM.md#5-proof-topology-consequence), [Hilbert--Burch repeated-coordinate localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_REPEATED_COORDINATE_LOCALIZATION_THEOREM.md#4-proof-topology-consequence), [repeated-coordinate support localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_REPEATED_COORDINATE_SUPPORT_LOCALIZATION_THEOREM.md#4-proof-topology-consequence), [repeated-coordinate exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_REPEATED_COORDINATE_EXCLUSION_THEOREM.md#5-repeated-coordinate-exclusion), [all-coordinate-distinct exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ALL_COORDINATE_DISTINCT_EXCLUSION_THEOREM.md#5-proof-topology-consequence), [two-coordinate/noncoordinate exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_TWO_COORDINATE_NONCOORDINATE_EXCLUSION_THEOREM.md#5-proof-topology-consequence), [`(1,1,2)` central-coordinate localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_CENTRAL_COORDINATE_TORUS_LOCALIZATION_THEOREM.md#5-residual-ordinary-coloops), [`(1,1,2)` third-colour coloop exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_THIRD_COLOUR_COLOOP_EXCLUSION_THEOREM.md#5-symmetry-and-proof-topology-consequence), [`(1,1,2)` central-colour coloop exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_CENTRAL_COLOUR_COLOOP_EXCLUSION_THEOREM.md#5-symmetry-and-proof-topology-consequence), [`(1,1,2)` repeated-outer-factor divisor exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_REPEATED_OUTER_FACTOR_DIVISOR_EXCLUSION_THEOREM.md#6-symmetry-and-proof-topology-consequence), [`(1,1,2)` double-repeated intersection exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_DOUBLE_REPEATED_OUTER_INTERSECTION_EXCLUSION_THEOREM.md#6-proof-topology-consequence), [`(1,1,2)` same-colour central-chart exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_SAME_COLOUR_CENTRAL_CHART_EXCLUSION_THEOREM.md#4-proof-topology-consequence), [`(1,1,2)` outer-coordinate-chart exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_OUTER_COORDINATE_CHART_EXCLUSION_THEOREM.md#6-symmetry-and-proof-topology-consequence), [`(1,2,2)` coordinate-coloop localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_COORDINATE_COLOOP_LOCALIZATION_THEOREM.md#4-proof-topology-consequence), [`(1,2,2)` `beta_t`-coloop support localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_BETA_T_COLOOP_SUPPORT_LOCALIZATION_THEOREM.md#6-proof-topology-consequence), [`(1,2,2)` `beta_t`-coloop endpoint exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_BETA_T_COLOOP_COORDINATE_ENDPOINT_EXCLUSION_THEOREM.md#3-endpoint-exclusion-and-proof-topology-consequence), [`(1,2,2)` `alpha_s`-coloop exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_ALPHA_S_COLOOP_EXCLUSION_THEOREM.md#4-proof-topology-consequence), [`(1,2,2)` residual second-root-coloop localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_SUPPORT_LOCALIZATION_THEOREM.md#3-proof-topology-consequence), [`(1,2,2)` residual second-root coordinate-line localization](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_COORDINATE_LINE_LOCALIZATION_THEOREM.md#3-coordinate-line-consequence), [`(1,2,2)` residual second-root-coloop exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_EXCLUSION_THEOREM.md#6-proof-topology-consequence), [`(1,2,2)` third-root-coloop exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_THIRD_ROOT_COLOOP_EXCLUSION_THEOREM.md#4-proof-topology-consequence), [`(1,2,2)` complementary first-root-coloop exclusion](../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_COMPLEMENTARY_FIRST_ROOT_COLOOP_EXCLUSION_THEOREM.md#4-proof-topology-consequence) |
| `S3` | Exclusion of all-balanced rank drop inside the hypothetical-witness locus: **open**; properness is proved only in ambient block-graph space | [Balanced half-sensor theorem](../claims/arbitrary-order/BALANCED_HALF_SENSOR_COMPLETE_DECK_AND_WICK_GLOBALIZATION_THEOREM.md#3-the-proper-closed-all-balanced-boundary) |
| `S3D` | For every `n=2m>=8`, one diagonal-complete graph with invertible blocks, complete support, local concision, and normalized pure coefficients lies in **every** balanced rank-drop locus; its mixed coefficients are nonzero, so it is **not a witness** | [Diagonal-complete sharpness theorem](../claims/arbitrary-order/BALANCED_ALL_RANK_DROP_DIAGONAL_COMPLETE_SHARPNESS_THEOREM.md) |
| `S3Q` | The full vertex-gauge common-quadratic orbit lies in `B_all` for `n>=8` but is **disjoint from the witness equations** for `n>=6`: nondegenerate members have two-flattening rank six versus GHZ rank three, while degenerate members fail local rank | [Common-quadratic orbit exclusion](../claims/arbitrary-order/BALANCED_COMMON_QUADRATIC_ORBIT_RANK_DROP_AND_FLATTENING_EXCLUSION_THEOREM.md) |
| `S3P` | On any balanced shore whose root-root diagonal quadratics share one nondegenerate `Q`, every nonconstant mixed-word cross permanent is **divisible by `Q`**, while each constant word has the exact pure-root residue; every physical common-conformal shore is **excluded**, even with arbitrary internal nonroot blocks, by the nonzero-permanent mixed branch or zero-permanent pure branch | [Common-quadric mixed/pure residue theorem](../claims/arbitrary-order/BALANCED_COMMON_QUADRIC_MIXED_PERMANENT_DIVISIBILITY_AND_CONFORMAL_SHORE_EXCLUSION_THEOREM.md) |
| `S3B` | A fully target-supported common projective zero of all diagonal root quadrics on one balanced shore exposes the existing zero-surplus restriction `P_m -> Delta_3`.  A common nondegenerate `Q` always supplies such a conic point, so the entire common-`Q` shore is **excluded for `m=3,4`** and **reduced to PR for `m>=5`**, without cross-column separability.  An exact normalized `n=8` fixture shows `B_all` does not force a basepoint in a prescribed root gauge; the fixture is latently common-quadratic and not a witness. | [Root-quadric basepoint bridge and gauge sharpness](../claims/arbitrary-order/BALANCED_ROOT_QUADRIC_BASEPOINT_PERMANENT_RESTRICTION_AND_GAUGE_SHARPNESS_THEOREM.md) |
| `S3C` | For every five-set of an eight-vertex weighted concise ternary witness, the three target-colour root products belong to the ten internal-edge ideal.  Five-root nonemptiness and a `120`-product incidence cover put every induced `K_5` tuple whose ten blocks are all nonzero in a fixed closed projective **codimension-at-least-three** envelope, with the same affine bound after whole-zero-block branches are added.  The result uses `729` anchored-slice equations, including `726` mixed zeros; it does not use balanced minors or prove independence across the `56` five-sets. | [Five-root three-colour boundary-incidence theorem](../claims/arbitrary-order/EIGHT_VERTEX_FIVE_ROOT_THREE_COLOUR_BOUNDARY_INCIDENCE_CODIMENSION_THREE_THEOREM.md) |
| `S3CA` | For any fixed labelled adjacent pair of five-sets at eight vertices, exact synchronization stratification gives a closed necessary envelope of **codimension at least five** in the selected fourteen projective blocks, the selected affine blocks, and the full twenty-eight-block affine pullback.  Exactly `60` labelled fully synchronized common-`K_4` selector strata attain the source-dimension bound.  Exact projected codimension, distinct intrinsic components, independence among the `420` adjacent pairs, and witness exclusion are not claimed. | [Adjacent five-set boundary-overlap theorem](../claims/arbitrary-order/EIGHT_VERTEX_ADJACENT_FIVE_SET_BOUNDARY_OVERLAP_CODIMENSION_FIVE_THEOREM.md) |
| `S3CB` | On the same fixed adjacent-pair envelope, the all-balanced rank-drop equations cut every dimension-`247` equality source properly in the full affine block space.  Every hypothetical witness in this branch therefore lies in a fixed closed subset of `A^252` of dimension at most `246`, hence **ambient codimension at least six**.  A common-quadratic rank-seven control proves the residual is nonempty; no transverse intersection, exact codimension, multi-pair additivity, or witness exclusion follows. | [Balanced adjacent-overlap codimension-six theorem](../claims/arbitrary-order/EIGHT_VERTEX_ADJACENT_FIVE_SET_BOUNDARY_OVERLAP_BALANCED_RANK_DROP_CODIMENSION_SIX_THEOREM.md) |
| `S3CC` | The proposed four-chart Bell-partition codimension lift is **withdrawn**: its shared-edge cardinality `q_ij` is not tensor-span rank for four decomposable evaluations.  An exact feasible selector/partition stratum has common span ranks `(2,3,3,4,4,4)` versus six cardinalities `4`, and a locally projected affine incidence image of codimension eight.  This is a route boundary, not a Krenn--Gu counterexample; the corrected generic support-rank census is recorded at S3CCD, while rank-degenerate components, the `B_all` intersection, independence among the `70` pencils, witness exclusion, and global resolution remain open. | [Four-five-set pencil tensor-span-rank boundary correction](../claims/arbitrary-order/EIGHT_VERTEX_FOUR_FIVE_SET_PENCIL_TENSOR_SPAN_RANK_BOUNDARY_CORRECTION.md), [correction review](audits/EIGHT_VERTEX_FOUR_FIVE_SET_PENCIL_TENSOR_SPAN_RANK_BOUNDARY_CORRECTION_REVIEW_2026-08-27.md) |
| `S3CCD` | The corrected support-Segre census exhausts the 120 nonconstant selector maps modulo implemented safe symmetries, all 15 exact common-vertex partition types, and all feasible canonical systems.  Using actual generic shared-edge tensor-span ranks gives `q=Delta+sum rho>=20`, with exactly two q=20 equality orbits; generic exact-partition incidence sources therefore have affine codimension at least eight.  Rank-degenerate components and their `c_rank`, the `B_all` cut, compatibility among the `70` pencils, full target equations, witness exclusion, and global resolution remain open; no codimension-nine/ten claim follows. | [Support-Segre generic-rank census](../claims/arbitrary-order/EIGHT_VERTEX_FOUR_FIVE_SET_PENCIL_SUPPORT_SEGRE_GENERIC_RANK_CENSUS_THEOREM.md), [hostile review](audits/EIGHT_VERTEX_FOUR_FIVE_SET_PENCIL_SUPPORT_SEGRE_GENERIC_RANK_CENSUS_REVIEW_2026-08-27.md) |
| `S3H` | In the invertible monomial common-form orbit, every nonzero pure coefficient makes all Hamming-one mixed coefficients vanish, while for every vertex pair and base colour one or two of the four pair-local Hamming-two cells are nonzero.  An exact all-rank-drop adjacent-cut control has empty prescribed-gauge base loci and all `48` Hamming-one zeros, so rank drop plus pure and Hamming-one data do not force compatible fixed-gauge roots.  This is route sharpness, not a witness or a general `B_all` classification. | [Adjacent-cut monomial Hamming-shell sharpness](../claims/arbitrary-order/EIGHT_VERTEX_ADJACENT_CUT_MONOMIAL_HAMMING_ONE_BLINDNESS_AND_HAMMING_TWO_DETECTOR_SHARPNESS_THEOREM.md) |
| `M1` | Maximum torus-root saturation and `r=1` / `r>=2` split: **proved universal reduction** | [Maximal torus-root theorem](../claims/arbitrary-order/MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md) |
| `M2` | One complete fixed-surplus physical hafnian layer; coordinate two-residual absorption: **proved reduction, not exclusion** | [Maximal torus-root theorem](../claims/arbitrary-order/MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md#2-the-saturated-principal-hafnian-layer) |
| `PR` | Weighted `P_t -> Delta_3` restriction family: **extracted at zero surplus and on the conditional consecutive-lift branch; arbitrary-order exclusion open**. The live `t=6` / P6 restriction remains inside this node; the three-excess notes address only the first strict-support layer, not arbitrary support. | [Maximal-root extraction](../claims/arbitrary-order/MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md#2-the-saturated-principal-hafnian-layer), [consecutive single-open lift](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_SINGLE_OPEN_CONSECUTIVE_PERMANENT_LIFT_AND_COMPANION_FRAME_THEOREM.md), [P6 package index](../claims/p6/README.md), [three-excess port boundary](../claims/arbitrary-order/ARBITRARY_PERMANENT_THREE_EXCESS_PORT_PERMUTATION_THEOREM.md), and [conformal Birkhoff boundary](../claims/arbitrary-order/ARBITRARY_PERMANENT_THREE_EXCESS_CONFORMAL_BIRKHOFF_REDUCTION.md) |
| `PRC` | Every weighted `P_r -> Delta_3` restriction has `dim B_ab>=5` and `dim A_S+dim B_ab<=binomial(r,2)+3` for each omitted pair.  Hence every complementary co-two product sensor has corank at least two; for P6 all fifteen sensors have rank at most `13`.  This is a **proved necessary boundary, not a nonrestriction theorem**. | [Co-two sensor corank-two strengthening](../claims/arbitrary-order/ARBITRARY_PERMANENT_COTWO_PRODUCT_SENSOR_CORANK_TWO_STRENGTHENING_THEOREM.md) |
| `PR5` | For an exact characteristic-zero `P_6 -> Delta_3` restriction, product dimension five at any omitted pair forces active support four and one of six based-frame exchange classes.  Exact covariance transports the six pointwise endpoint exclusions across every class, so the `P_6` equality-five branch is **proved excluded**.  This is a `P_6` theorem; no equality-five exclusion for another order is claimed. | [Full equality-five exclusion](../claims/arbitrary-order/ARBITRARY_PERMANENT_P6_COTWO_EQUALITY_FIVE_FULL_EXTENSION_EXCLUSION_THEOREM.md), [hostile consolidation review](audits/ARBITRARY_PERMANENT_P6_COTWO_EQUALITY_FIVE_FULL_EXTENSION_EXCLUSION_REVIEW_2026-08-16.md), [support synthesis](../claims/arbitrary-order/ARBITRARY_PERMANENT_COTWO_EQUALITY_FIVE_ACTIVE_SUPPORT_ORBIT_SYNTHESIS_THEOREM.md), [based-frame classification](../claims/arbitrary-order/ARBITRARY_PERMANENT_COTWO_R4_BASED_FRAME_ORBIT_CLASSIFICATION_THEOREM.md), and [orbit transport](../claims/arbitrary-order/ARBITRARY_PERMANENT_MONOMIAL_COVARIANCE_AND_BASED_FRAME_ORBIT_TRANSPORT_LEMMA.md) |
| `PR6` | The equality-five exclusion forces every omitted pair of a hypothetical exact `P_6` restriction to satisfy `dim B_ab>=6`, hence all fifteen complementary four-mode sensors have rank at most `12`.  At the minimal value six, full-support pair-level `Delta_3` frames already form a nonempty nine-dimensional Grassmann open; coordinate monomial orbits have dimension at most five, and the maximal twelve-dimensional linear complementary envelope attains pairing rank three.  Thus the finite equality-five endpoint method does not continue, while factorization by four actual local planes and simultaneous compatibility across all fifteen pairs remain **open**.  No `P_6` closure follows. | [Dimension-six pair-moduli boundary](../claims/arbitrary-order/ARBITRARY_PERMANENT_P6_COTWO_DIMENSION_SIX_PAIR_MODULI_AND_LINEAR_ENVELOPE_BOUNDARY.md), [hostile review](audits/ARBITRARY_PERMANENT_P6_COTWO_DIMENSION_SIX_PAIR_MODULI_AND_LINEAR_ENVELOPE_REVIEW_2026-08-16.md), [full equality-five exclusion](../claims/arbitrary-order/ARBITRARY_PERMANENT_P6_COTWO_EQUALITY_FIVE_FULL_EXTENSION_EXCLUSION_THEOREM.md), [strengthened co-two sensor bound](../claims/arbitrary-order/ARBITRARY_PERMANENT_COTWO_PRODUCT_SENSOR_CORANK_TWO_STRENGTHENING_THEOREM.md#4-the-strengthened-sensor-bound) |
| `PRT` | Once one common six-mode `P_6` pullback with six labelled three-planes is already supplied, mixed-radical constraints on the five edges of any spanning tree are necessary and sufficient for every mixed word to vanish; the other ten pair radicals follow.  Triple and quartet zeon-product identities are necessary for simultaneous pair-factor compatibility, but an exact common equality-six model has all fifteen sensor ranks six, every product identity, and nonzero pure coefficients while its `001122` coefficient is `41456`.  This is a **proved target compression and sharp compatibility boundary**, not factor identification, extraction, or nonrestriction. | [Spanning-tree radical and simultaneous factor boundary](../claims/arbitrary-order/ARBITRARY_PERMANENT_P6_COTWO_SPANNING_TREE_RADICAL_AND_SIMULTANEOUS_FACTOR_COMPATIBILITY_BOUNDARY.md), [hostile review](audits/UNIVERSAL_EXTRACTION_GLUING_RESPONSE_ATLAS_SUPPORTING_LANES_REVIEW_2026-08-16.md) |
| `O1` | Contracted truncation, same-fibre rank nonobservability, and single-open absorption: **proved structural boundary** | [Balanced fixed-surplus theorem](../claims/arbitrary-order/BALANCED_FIXED_SURPLUS_TRUNCATION_FIBRE_NONOBSERVABILITY_AND_TRANSVERSE_ABSORPTION_THEOREM.md) |
| `O2` | Complete two-open equation and conditional `q=0` tensor-preserving star gauge: **proved boundary** | [Two-open gauge theorem](../claims/arbitrary-order/BALANCED_TWO_OPEN_ROOT_GAUGE_DETECTOR_AND_STAR_INVISIBILITY_BOUNDARY.md) |
| `O2P` | On the aligned common-two-row, projectively constant branch, the complete single-open identity is a consecutive `P_(m+1)` restriction and its old-root companions form an exact rank-two diagonal quotient frame: **proved conditional reduction** | [Consecutive single-open lift](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_SINGLE_OPEN_CONSECUTIVE_PERMANENT_LIFT_AND_COMPANION_FRAME_THEOREM.md) |
| `O2M` | In the minimum aligned projective cell `q=0,r=3`, the lifted row quotas force `P_3(a,a,b)!=0`, so every nonzero absorption direction at either non-aligned root is **detected by the complete two-open tensor**; this is not a witness exclusion | [Lifted minimum-cell detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_ROW_QUOTAS_AND_MINIMAL_CELL_TWO_OPEN_DETECTOR_THEOREM.md) |
| `O2T` | In the aligned projective `q=0,r=4` cell, local independence of `a_u,b_u` at all four outside modes makes `h -> P_4(h,a,a,b)` injective; a companion-basis deletion then gives **at least one nonzero two-open detector**. This remains a verified strict special case of `O2F`. | [Transverse four-cell detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_TRANSVERSE_FOUR_CELL_TWO_OPEN_DETECTOR_THEOREM.md) |
| `O2F` | In the full aligned projective `q=0,r=4` cell, collision quotients plus Hall incidence reduce invisibility to a common outside `a/b` zero; recolouring and local concision exclude it. Hence **at least one nonzero two-open detector** always exists, and all three do when the companions are pairwise independent. This is not a witness exclusion. | [Complete four-cell detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_FOUR_CELL_TWO_OPEN_DETECTOR_THEOREM.md) |
| `O2V` | In aligned projective `q=0,r=5`, the four companion equations form an exact symmetric `XL=0` system. Away from a zero companion or balanced `2+2` projective split, modewise three-activity forces **at least one nonzero two-open detector**. Local `a/b` transversality implies activity. This is conditional detection, not full-cell closure or witness exclusion. | [Five-cell collective detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_FIVE_CELL_COLLECTIVE_COMPANION_AND_ACTIVITY_DETECTOR_THEOREM.md) |
| `O2A` | In locally transverse aligned projective `q=0,r=5`, common-kernel contraction makes a doubly transverse root's five-mode pair-collision map injective. If at most one root is not doubly transverse, all six pair tensors are nonzero, and the rank-two companion zero-edge lemma gives **at least one detector for every companion frame**. This is not witness exclusion. | [Five-cell all-companion pair detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_FIVE_CELL_PAIR_COLLISION_AND_ALL_COMPANION_DETECTOR_THEOREM.md) |
| `O2C` | In every locally transverse aligned projective `q=0,r=5` cell, weak-root common-kernel trapping plus the exhaustive good/zero/balanced companion split forces a local-concision contradiction if all four collective tensors vanish. Hence **at least one nonzero two-open detector** exists for every companion frame and every root quotient-support pattern. This is not full-cell closure or witness exclusion. | [Complete transverse five-cell detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_TRANSVERSE_FIVE_CELL_TWO_OPEN_DETECTOR_THEOREM.md) |
| `O2D` | In aligned projective `q=0,r=5`, a dependent mode with four active deletions forces every invisible companion pattern into one quotient line. A sharp retained four-mode inverse therefore gives **at least one detector** with one arbitrary local defect, or with two defects when at least one has nonzero proportional `a_u,b_u`. This covers every companion/root-support pattern in those strata, but does not exclude a witness. | [Rank-one-mode detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_RANK_ONE_MODE_AND_REGULAR_TWO_DEFECT_FIVE_CELL_DETECTOR_THEOREM.md) |
| `O2E` | In aligned projective `q=0,r=5`, three active deletions force a quotient-line trap for every companion frame. Exact `A/B/Z` retained collision kernels then give **at least one detector** for the zero-containing `AZ`, `BZ`, `ZZ` cells and the mixed `AB` cell. Together with `O2C` and `O2D`, this detects every at-most-two-defect cell except same-type `AA` and `BB`; it does not exclude a witness. | [Three-activity two-defect detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_THREE_ACTIVITY_AND_MIXED_DEGENERATE_TWO_DEFECT_FIVE_CELL_DETECTOR_THEOREM.md) |
| `O2G` | In aligned projective `q=0,r=5`, exact row-pair and triple Hall incidence turns the same-type `AA` and `BB` double-kernel survivors into pure-coefficient assignment contradictions. Together with `O2C`, `O2D`, and `O2E`, this gives **at least one detector in every cell with at most two local defects**. It does not exclude a witness. | [Same-type row-incidence detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_ROW_INCIDENCE_SAME_TYPE_TWO_DEFECT_FIVE_CELL_DETECTOR_THEOREM.md) |
| `O2H` | In aligned projective `q=0,r=5`, row-pair incidence plus the two-singleton `P_5` obstruction excludes every local defect with `b=0`. Exact arbitrary-ratio collision intersections and inactive-set crowding then give **at least one detector in every cell with at most three local defects**, including all `RRR`, `RRB`, `RBB`, and `BBB` three-defect cells. This does not exclude a witness. | [Complete three-defect detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_THREE_DEFECT_FIVE_CELL_DETECTOR_THEOREM.md) |
| `O2I` | In the complete aligned common-two-row, projectively constant `q=0,r=5` cell, the lifted `p_a>=2` quota excludes four/five `B` defects. Exact four-/five-defect collision kernels, the all-regular cofactor graph, and a basis-free `3|2` Hall bridge then give **at least one detector in every remaining cell**. The primitive-cube-root `RRRRT` divisor is retained and still has only a one-dimensional common kernel. This does not exclude a witness. | [Complete aligned five-cell detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_ALIGNED_FIVE_CELL_TWO_OPEN_DETECTOR_THEOREM.md) |
| `O3` | Conditional aligned `q=0,r=5` detection does not prove witness exclusion or fixed-root injectivity. Every aligned `q=0,r>=6` cell, every `q>=1` cell, and every unfactorized outside graph remains **open** at detector depth. | [Complete aligned five-cell boundary](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_ALIGNED_FIVE_CELL_TWO_OPEN_DETECTOR_THEOREM.md#6-complete-aligned-five-cell-boundary) and [two-open exact boundary](../claims/arbitrary-order/BALANCED_TWO_OPEN_ROOT_GAUGE_DETECTOR_AND_STAR_INVISIBILITY_BOUNDARY.md#6-exact-boundary) |
| `U1` | Complete nonzero one-matrix-unit blocks and forbidden-word cancellation: **proved normal form; exclusion open** | [Maximal-root one branch](../claims/arbitrary-order/MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md#3-the-maximum-one-monomial-branch) |
| `U1B` | Every globally support-minimal matrix-unit realization is stable against support-erasing diagonal GHZ one-parameter directions. Equivalently, every physical edge occurs with positive integral multiplicity in an endpoint-label multicover whose three positive colour loads are constant across vertices. The multicover weights are not physical amplitudes. | [GHZ diagonal-torus endpoint balance](../claims/arbitrary-order/MATRIX_UNIT_GHZ_DIAGONAL_TORUS_POLYSTABILITY_ENDPOINT_BALANCE_AND_ACTIVE_TRANSPORT_SHARPNESS_THEOREM.md) |
| `U1C` | Over `C`, every support-minimal matrix-unit realization has a unique positive diagonal GHZ gauge modulo the edgewise stabilizer in which the actual squared physical amplitudes have three positive vertex-independent colour loads. This magnitude normal form does not synchronize phases. | [GHZ moment-balanced gauge](../claims/arbitrary-order/MATRIX_UNIT_GHZ_MOMENT_BALANCED_GAUGE_AND_UNIT_PHASE_ACTIVE_TRANSPORT_SHARPNESS_THEOREM.md) |
| `U2` | Globally minimum forbidden word has at most four deviations; exact finite-port response and partial bridges: **proved reduction**. The `k=1`, `k=2`, and `k=3` cells all remain unexcluded; only `k=4` forces rigidity in the base colour. | [Four-switch theorem](../claims/arbitrary-order/MATRIX_UNIT_FOUR_SWITCH_MINIMAL_PORT_AND_PARTIAL_BRIDGE_REDUCTION_THEOREM.md) |
| `U3` | Globally rigid colour factors into a pure hafnian and binary tensor: **proved conditionally; rigidity not forced** | [Rigid-colour boundary](../claims/arbitrary-order/RIGID_COLOUR_COFACTOR_ANNIHILATION_AND_BACKBONE_CANCELLATION_BOUNDARY.md) |
| `U4` | Bi-null cuts, three-block primitive, and dual quadratic bridges: **proved; arbitrary-order exclusion open** | [Rigid primitive theorem](../claims/arbitrary-order/RIGID_COLOUR_THREE_BLOCK_BINARY_PRIMITIVE_AND_QUADRATIC_BRIDGE_THEOREM.md) |
| `U5` | “The primitive alone contradicts the tensor”: **refuted route** for every even order at least eight | [Primitive sharpness theorem](../claims/arbitrary-order/RIGID_COLOUR_THREE_BLOCK_PRIMITIVE_SHARPNESS_AND_DUAL_BRIDGE_COMPLETION_OBSTRUCTION.md) |
| `U6` | Cross-parity erasure, bridge/deeper entry, rigid-head Wick tower, and pseudoforest normal form: **proved reduction** | [Cross-parity theorem](../claims/arbitrary-order/MATRIX_UNIT_CROSS_PARITY_ERASURE_RIGID_HEAD_WICK_AND_BRIDGE_CORE_REDUCTION_THEOREM.md) |
| `U7A` | For every mixed word with nonzero aggregate offdiagonal coefficient, the diagonal contribution factors as the product of three nonzero pure-shore hafnians. Hence every active parity-zero fibre already has an exact word-preserving diagonal rematching; a Tutte failure can occur only in an internally zero fibre. | [Active parity-fibre synchronization theorem](../claims/arbitrary-order/MATRIX_UNIT_PARITY_FIBRE_DIAGONAL_FACTORIZATION_AND_ACTIVE_WORD_SHORE_SYNCHRONIZATION_THEOREM.md) |
| `U7B` | Expanding an active coordinate by its exact off-shore matching produces a cofactor-active physical cross core. Its cross-type counts have one parity, and the imported square/hexagon alternative gives exactly: deeper-blocker entry, transport to another active word with the same multiplicities, or a pure-shore hafnian that cancels despite a nonzero matching term. No-exit transport has a finite active-word cycle. | [Active-word cross-response and bridge-transport trichotomy](../claims/arbitrary-order/MATRIX_UNIT_ACTIVE_WORD_FIBRE_CROSS_MATCHING_RESPONSE_AND_BRIDGE_TRANSPORT_TRICHOTOMY.md) |
| `U7C` | Every active cycle carries a nonzero endpoint-character circulation and a diagonal-gauge-invariant Laurent holonomy. Its fibres are aggregate, or exact binomials force `H=(-1)^m`. Every pure cancellation has a least supported residual whose Euler cofactor flow branches or is a spanning union of alternating even cycles. A sparse exact odd binomial cycle shows this is a phase normal form, not a sign contradiction. | [Phase holonomy and minimal pure-cofactor flow](../claims/arbitrary-order/MATRIX_UNIT_PHASE_HOLONOMY_AND_MINIMAL_PURE_COFACTOR_FLOW_REDUCTION_THEOREM.md) |
| `U7D` | A complete exact eight-vertex `r=1` table simultaneously has all three pure target coefficients, strict positive endpoint balance, a moment-balanced representative over `C`, three proper nonempty nonrigidity sets, and an odd three-fibre binomial cycle with `H=-1`. Its exposed `(7,1,0)` mixed coefficient is transport-isolated, and its only additional zero mixed fibre leaves the selected elimination ideal `(H+1)`. The **complete** `(4,4,0)` block instead has `57` empty, `10` singleton, and exactly `3` binomial fibres, so its Laurent-saturated ideal is `(1)` and the fixed label support is excluded in the cycle's own multidegree. This is a fixed-template theorem, not an arbitrary-cycle exclusion. | [Complete pure-target moment-compatible odd-holonomy sharpness](../claims/arbitrary-order/MATRIX_UNIT_COMPLETE_PURE_TARGET_MOMENT_COMPATIBLE_ODD_HOLONOMY_SHARPNESS_THEOREM.md), [exposed-fibre transport isolation](../claims/arbitrary-order/MATRIX_UNIT_EXPOSED_MIXED_FIBRE_TRANSPORT_ISOLATION_AND_NEIGHBOUR_SHARPNESS_THEOREM.md), and [complete same-multidegree saturation exclusion](../claims/arbitrary-order/MATRIX_UNIT_U7D_COMPLETE_SAME_MULTIDEGREE_TARGET_BLOCK_SATURATION_EXCLUSION_THEOREM.md) |
| `U7E` | For any complete same-multidegree target block, removing one invertible reference matching per nonempty fibre descends the exact ideal to the group algebra of the within-fibre difference lattice, preserving unit status and holonomy elimination even for nonsaturated lattices. A singleton is a unit. An all-binomial block is a unit exactly when its signed relation lattice has an odd kernel dependency; otherwise it is proper and gives exactly `H=(-1)^m`, with no stronger holonomy polynomial. Aggregate fibres remain explicit unresolved Laurent polynomials. | [Complete same-multidegree fibre-lattice reduction and binomial parity dichotomy](../claims/arbitrary-order/MATRIX_UNIT_COMPLETE_SAME_MULTIDEGREE_FIBRE_LATTICE_REDUCTION_AND_BINOMIAL_PARITY_DICHOTOMY_THEOREM.md) |
| `U7F` | For a parity-consistent binomial core containing every fibre of an active binomial cycle, untwisting gives the exact residual group algebra `C[L/L_B]`. Smith torsion splits it into finite character sheets. Quotient free rank zero is completely decided by scalar character evaluations; free rank one is completely decided by univariate Laurent gcds. Killing every sheet gives `(1)`; any surviving sheet leaves exactly `H=(-1)^m`. Aggregate cycle fibres and free rank at least two remain open. | [Binomial-core torsion-sheet and rank-one aggregate quotient](../claims/arbitrary-order/MATRIX_UNIT_BINOMIAL_CORE_TORSION_SHEET_AND_RANK_ONE_AGGREGATE_QUOTIENT_THEOREM.md) |
| `U7G` | Any selected target equations, across arbitrary word multidegrees and including pure anchors, descend faithfully to one global support-difference group algebra. Mixed residuals lie in the endpoint-character kernel; direct-sum difference lattices do not couple even when physical variables overlap. For a fully binomial active cycle, arbitrary extra target equations give only `(1)` or `(H-(-1)^m)`, and the rank-zero/rank-one torsion-sheet criteria apply globally. Cross-multiplicity algebra is exact; cross-multiplicity unit forcing remains open. | [Cross-multiplicity global target lattice and holonomy dichotomy](../claims/arbitrary-order/MATRIX_UNIT_CROSS_MULTIPLICITY_GLOBAL_TARGET_LATTICE_AND_HOLONOMY_DICHOTOMY_THEOREM.md) |
| `U7H` | At a least supported pure hafnian cancellation, the active first-cofactor graph is exactly the allowed-edge graph and is connected and matching-covered. Every active edge lies on a fixed-matching alternating cycle. The degree-two branch is one even cycle with exactly two terms, a primitive signed relation, and monomial first cofactors. The branching branch has at least three matchings, cyclomatic rank at least two, and either two branch sites or one degree-at-least-four site. Neither branch is yet excluded. | [Minimal pure-cofactor matching-covered core and single-cycle theorem](../claims/arbitrary-order/MATRIX_UNIT_MINIMAL_PURE_COFACTOR_MATCHING_COVERED_CORE_AND_SINGLE_CYCLE_THEOREM.md) |
| `U7I` | At every branch vertex of the least pure residual, the residual matchings partition into nonzero cofactor ports. Either every port is a singleton, giving a conformal alternating `d`-fan and one exact `d`-nomial Laurent relation, or some port is an unavoidable nonzero aggregate. Two exits carry exactly an all-odd three-matching theta or an odd/even/even two-matching theta with one exterior-completed port. Exact rational least residuals realize every sparse arity, both cubic theta profiles, and the aggregate alternative, so these pure structures alone are not contradictions. | [Minimal pure-cofactor port aggregate and conformal-fan reduction](../claims/arbitrary-order/MATRIX_UNIT_MINIMAL_PURE_COFACTOR_PORT_AGGREGATE_AND_CONFORMAL_FAN_REDUCTION_THEOREM.md) |
| `U7J` | For an active cycle with aggregate fibres, the outgoing-normalized extra sums `A_i` are gauge invariant and the exact holonomy is `H=(-1)^m product_i(1+A_i)`. Aggregate extra terms may cancel separately, leaving the binomial sign. A complete locally concise eight-vertex matrix-unit family has complete cycle-fibre sizes `5,2,2` and `H=-2/(1+2t)`, so the selected cycle subsystem has zero elimination ideal in `H`. The family fails every pure target and is not a witness; complete-target coupling of the defects remains open. | [Aggregate active-cycle defect factorisation and split-fibre sharpness](../claims/arbitrary-order/MATRIX_UNIT_AGGREGATE_ACTIVE_CYCLE_DEFECT_FACTORISATION_AND_SPLIT_FIBRE_SHARPNESS_THEOREM.md) |
| `U7K` | Every offdiagonal extra matching in an aggregate active-cycle fibre now attaches exactly: a cancelling source or bridge shore contains a conformally minimal primitive cycle, sparse fan, or aggregate port whose terms embed with identical exponent differences into one mixed target fibre; otherwise bridge normalization enters the deeper branch or the complete target equation makes another word active. On a shortest cycle that word is outside the cycle or is the selected successor. The parallel-successor case is sharp even with all pure coefficients one, and can contribute zero new successor-fibre direction; a separate singleton excludes the fixed sharpness support. Universal unit forcing remains open. | [Aggregate extra-matching target attachment](../claims/arbitrary-order/MATRIX_UNIT_AGGREGATE_EXTRA_MATCHING_TARGET_ATTACHMENT_THEOREM.md) |
| `U7L` | If every aggregate extra on an active cycle is diagonal, each diagonal fibre is exactly the Cartesian product of its pure-shore matching sets and its difference lattice is their disjoint-support direct sum. Aggregate size forces a primitive one-shore alternating-cycle direction, but not a vanishing binomial. A complete locally concise twelve-vertex `Q(t)` family has the unique shortest active `3/2/2` cycle, one diagonal extra, all pure coefficients one, shared physical variables, and a saturated direct rank-four fibre lattice with no integer dependency; `H=-1/(1+t)` remains free in the selected-plus-pure subsystem. An outside singleton excludes the fixed support. | [Diagonal aggregate shore product and primitive exchange](../claims/arbitrary-order/MATRIX_UNIT_DIAGONAL_AGGREGATE_SHORE_PRODUCT_AND_PRIMITIVE_EXCHANGE_SHARPNESS_THEOREM.md) |
| `U7` | Force the global target-lattice ideal to be a unit or close a topological exit: turn an attached pure relation into an odd dependency or unit, make a primitive diagonal shore direction meet another target lattice non-directly, use an outside or parallel target equation to kill every quotient sheet, control a rank-at-least-two ideal, or close the deeper branch. This remains **open**: `U7K` covers offdiagonal extras, `U7L` gives the exact diagonal shore-product normal form, `A7` kills every imbalanced binomial-contained A6 block while excluding the two misaligned balanced `Q/C^2` restrictions only on the localized nonzero-port locus, and `A8` makes the sparse-port lattice primitive, excludes odd exact-rank-three contained fibres, and classifies any already-landed comparison carriers. None forces the A6 completion, exact rank three, lattice containment, or a comparison carrier; kills aligned `Q/C^2` or balanced `Q/Q` universally; closes a general rank-at-least-two ideal; or excludes the deeper branch. | [Offdiagonal attachment boundary](../claims/arbitrary-order/MATRIX_UNIT_AGGREGATE_EXTRA_MATCHING_TARGET_ATTACHMENT_THEOREM.md#8-consequence-for-the-live-u7-edge), [diagonal aggregate boundary](../claims/arbitrary-order/MATRIX_UNIT_DIAGONAL_AGGREGATE_SHORE_PRODUCT_AND_PRIMITIVE_EXCHANGE_SHARPNESS_THEOREM.md#7-consequence-for-the-live-u7-edge), [beta-three sign filter](../claims/arbitrary-order/MATRIX_UNIT_ALL_BRIDGE_BETA_THREE_FIXED_COMPLETION_BINOMIAL_SUBLATTICE_PORT_SIGN_DICHOTOMY_THEOREM.md), [sparse-port primitive lattice and comparison graph](../claims/arbitrary-order/MATRIX_UNIT_ALL_BRIDGE_BETA_THREE_SPARSE_PORT_PRIMITIVE_LATTICE_AND_BINOMIAL_COMPARISON_GRAPH_THEOREM.md), and [global cross-multiplicity boundary](../claims/arbitrary-order/MATRIX_UNIT_CROSS_MULTIPLICITY_GLOBAL_TARGET_LATTICE_AND_HOLONOMY_DICHOTOMY_THEOREM.md#7-consequence-for-the-live-u7-edge) |
| `U8` | Proper nonempty colour-nonrigidity sets propagate to all vertices: **open** | [Four-switch partial-bridge theorem](../claims/arbitrary-order/MATRIX_UNIT_FOUR_SWITCH_MINIMAL_PORT_AND_PARTIAL_BRIDGE_REDUCTION_THEOREM.md#5-partial-bridge-systems) |
| `D1` | Deeper double-star/multi-star blocker branch: **open**. Its blocker alternatives are pointwise after shrinking to a dense constructible stratum; no uniform blocker pair is proved on the whole component. | [Double-star lemma](../claims/arbitrary-order/DOUBLE_STAR_ANNIHILATION_LEMMA.md) and [multi-star factorization](../claims/arbitrary-order/MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md) |
| `A1` | Simultaneous balanced all-bridge system: **proved conditional branch**, not universal extraction | [Three-colour balanced bridge intersection](../claims/arbitrary-order/THREE_COLOUR_BALANCED_BRIDGE_INTERSECTION_THEOREM.md) |
| `A2` | Every all-bridge witness satisfies `deg_G(v)>=deg_D(v)+3`; hence `Delta(G)>=8` and `n>=10`, so maximum full-support degree at most seven is **excluded**. Saturated `Delta(D)<=4` is also **excluded**. The degree-five owner localizes one of three supported pure cancellations and makes the globally least core bipartite subcubic with exact cycle/theta/higher-rank and typed-site refinements. Its later successor `A3` removes the upper-degree restriction only from localization and bipartite-core conclusions; the degree-five subcubic/site structure remains owned here. | [Cubic exclusion](../claims/arbitrary-order/ALL_BRIDGE_ACTIVE_DECK_EXCLUSIVITY_AND_CUBIC_DIAGONAL_EXCLUSION.md), [degree-four exclusion](../claims/arbitrary-order/ALL_BRIDGE_ACTIVE_DECK_MAXIMUM_DEGREE_FOUR_EXCLUSION.md), [universal zero layer](../claims/arbitrary-order/UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md), and [degree-five/full-support reduction](../claims/arbitrary-order/ALL_BRIDGE_ACTIVE_DECK_MAXIMUM_DEGREE_FIVE_BRANCHING_OR_CANCELLATION_CORE_REDUCTION_THEOREM.md) |
| `A3` | At **every** saturated degree, every simultaneous all-bridge system has a supported pure cancellation localized to an inactive-selected-edge complement, one side of a selected-matching-component/complement cut, or one side of a Hamiltonian-chord-arc/complement cut: **proved exhaustive reduction; all three open as exclusions**. The minimal Hall shore gives two common-cofactor-zero repairs. Independently, every globally least pure core is bipartite; rank one is an even cycle and rank two a closed all-odd theta, while the generic one-open theta is excluded in this specialization. Its perfect-matching polytope has dimension `beta`, so `N>=beta+1`; every branch site with `d<=beta` has a nonzero aggregate port, and a sparse site requires `d=N=beta+1`. Aggregate and extremal sparse strata remain open. | [All-degree localization and bipartite core](../claims/arbitrary-order/ALL_BRIDGE_ACTIVE_DECK_ALL_DEGREE_LOCALIZED_PURE_CANCELLATION_AND_BIPARTITE_CORE_REDUCTION_THEOREM.md) |
| `A4` | If a globally least all-bridge pure core has an extremal sparse site `d=N=beta+1`, that site exhausts its shore excess.  The opposite shore either has one second extremal site and the core is exactly `beta+1` internally disjoint odd routes, or has `2,...,beta-1` lower-degree branch sites, each with a nonzero aggregate port: **proved exhaustive reduction; both open as exclusions**.  At the sparse site `deg_D>=beta+3` and `deg_G>=beta+6`.  At `beta=3` the sparse split is exactly `Q/Q` versus `Q/C^2`; the full five-kernel census has `N in {4,5}`.  Exact least residuals realize both sparse forms, and weighted `K_(3,3)-e` refutes `N=beta+1 => sparse theta`.  These scalar controls are not simultaneous all-bridge witnesses. | [Extremal-sparse opposite-shore dichotomy](../claims/arbitrary-order/ALL_BRIDGE_BIPARTITE_LEAST_CORE_EXTREMAL_SPARSE_OPPOSITE_SHORE_DICHOTOMY_THEOREM.md) |
| `A5` | In the `beta=3` extremal-sparse `Q/Q` or `Q/C^2` core, route parity composes with the nonzero cofactor-port partition.  Odd-route endpoint ports coincide.  In `Q/Q` they are paired singletons with the same nonzero full matching contribution.  In `Q/C^2` the four odd routes pair four singletons, while the unique even route has complementary doubleton ports whose edge-inclusive cofactor sums are nonzero exact negatives: **proved refinement, not an exclusion**.  Bare deletion hafnians, mixed-fibre attachment, independence, and impossibility of either kernel are not proved. | [Beta-three route-port pairing](../claims/arbitrary-order/ALL_BRIDGE_BIPARTITE_LEAST_CORE_BETA_THREE_ROUTE_PORT_PAIRING_THEOREM.md) |
| `A6` | Conditional on one fixed nonzero `U7K`-compatible completion extending all four `beta=3` `Q/Q` or `Q/C^2` core matchings into the same complete mixed zero-target fibre, the injected four-term block has exponent-difference rank three and zero total.  The complete fibre therefore has four terms or at least six, never five; its difference lattice has rank at least three.  In `Q/C^2`, the two complementary doubleton port sums remain nonzero exact negatives.  The normalized formal block is the proper nonunit `1+X+Y+Z`, while its physical evaluation vanishes and its four full exponents have no nontrivial integer affine dependency: **proved conditional composition, not an exclusion**.  Existence of such a completion and control of the remaining rank-at-least-three ideal are open. | [Beta-three fixed-completion mixed-fibre block](../claims/arbitrary-order/MATRIX_UNIT_ALL_BRIDGE_BETA_THREE_ROUTE_PORT_FIXED_COMPLETION_MIXED_FIBRE_RANK_THREE_BLOCK_THEOREM.md) |
| `A7` | Conditional on the A6 fixed-completion branch and integral containment of its free rank-three difference lattice in one parity-consistent same-multidegree binomial-core lattice, the one fixed core character reduces `1+X+Y+Z` to a scalar.  Five of eight possible restrictions are imbalanced and give the global combined-branch unit ideal; the other three are exactly the two-plus/two-minus partitions.  In `Q/C^2`, nonzero complementary doubleton ports leave one aligned balanced partition and exclude the other two only after port localization.  In `Q/Q`, all three balanced restrictions remain: **proved conditional sign filter, not a universal exclusion**.  Neither the fixed completion nor the integral containment is forced. | [Beta-three binomial-sublattice port-sign dichotomy](../claims/arbitrary-order/MATRIX_UNIT_ALL_BRIDGE_BETA_THREE_FIXED_COMPLETION_BINOMIAL_SUBLATTICE_PORT_SIGN_DICHOTOMY_THEOREM.md) |
| `A8` | At the A5 sparse quartic, the three nonreference port coordinates split the free rank-three `A6` difference lattice as a primitive direct summand of the physical edge lattice.  Hence an A6 complete fibre of exact difference rank three has exactly that lattice.  Under the `A7` integral containment, every surviving exact-rank-three complete fibre has even size; odd sizes are excluded, and a six-term fibre has an opposite-sign two-term complement in the binomial-core ideal.  Every physical comparison difference already known to land in the A6 lattice is exactly one sparse port-pair direction.  The resulting graph survives precisely when all edges cross the chosen balanced cut: a within-doubleton comparison closes aligned `Q/C^2`; across the three possible `Q/Q` core restrictions, the inclusion-minimal uniform three-edge closures are a triangle or `K_(1,3)`, while `P_4` is sharp: **proved conditional lattice and comparison refinement, not carrier existence or a universal exclusion**. | [Sparse-port primitive lattice and comparison graph](../claims/arbitrary-order/MATRIX_UNIT_ALL_BRIDGE_BETA_THREE_SPARSE_PORT_PRIMITIVE_LATTICE_AND_BINOMIAL_COMPARISON_GRAPH_THEOREM.md) |
| `A3R` | For every allowed edge `f` of a globally least all-bridge pure core and either other colour `d`, the completed complementary shore satisfies `h_d((V-S) union f)=0`.  If supported, it obeys `2|S|<=n+2` and contains a conformally minimal pure relation attached termwise in one mixed target fibre; if `2|S|>n+2`, every response shore is support-unmatchable.  Opposite-colour active neighbour sets across each core edge are nonempty and disjoint, but need not leave `S`; for a co-two exterior with `|S|>=6`, the exterior-neighbour vertices form only an independent set.  In the original colour, either the complement matches or a minimum-crossing portal has every nonempty induced image unmatchable: **proved response/portal reduction, not an exclusion**. | [Least-core complementary-shore response and portal dichotomy](../claims/arbitrary-order/MATRIX_UNIT_LEAST_CORE_COMPLEMENTARY_SHORE_RESPONSE_AND_PORTAL_DICHOTOMY_THEOREM.md) |
| `P5` | Local `P5 -> Delta_3` component programme: **partial, generic and boundary-limited** | [P5 package index](../claims/p5/README.md) and [obligation ledger](../claims/p5/frontier/P5_DELTA3_OBLIGATION_LEDGER.md) |
| `P7` | One committed legal sensor/incidence pullback: criterion **proved**, algebra outcome **open** | [Committed P7 criterion](../claims/p7/COMMITTED_LEGAL_SENSOR_ORDERED_SECANT_FACTOR_CHOW_NORM_AND_BOUNDARY_TRAP_CRITERION.md) |
| `GLS2` | In a maximal-root surplus-two cell, the full uncontracted root tensor contains every nonempty even principal hafnian of the same outside graph.  Injectivity of its `2^(r+1)-1`-column companion sensor reconstructs the complete deck from the GHZ target; kernel projection gives the exact weaker necessary-and-sufficient criterion for linear identification of one fixed residual pair, and sufficient criteria for physical paired-deck or all-pair-block supply.  Failure of the criterion is only linear-sensor nonidentifiability, not a second physical deck.  An explicit maximum-root triple-blocker chart has full rank, so rank drop is a proper ambient determinantal boundary, but observability is not forced on the witness locus.  At surplus at least four, the residual edge and pair moments are absent from every linear root-word selector.  This is **proved conditional Universal Supply and a sharp higher-surplus depth boundary**, not permanent extraction or witness exclusion. | [Surplus-two complete-deck sensor](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md), [hostile review](audits/UNIVERSAL_SUPPLY_AND_TARGET_COUPLED_DETECTION_REVIEW_2026-08-16.md) |
| `GLS3` | In every blocker-saturated maximum-root surplus-two hypothetical complex-witness cell, the corank-six incidence bound forces some nonzero raw pair companion `p_(A,Q)=per H_(A,Q)`.  This does not force the augmented four-root detector weight `l^T Jp`.  Pair-coordinate supply is exactly independence of the order-two companion columns modulo every higher-order column.  A maximum-root, quota-saturated, locally concise `r=3` family with normalized pure coefficients and zero Hamming-one shell nevertheless has a three-torus physical same-state pair fibre and fails every fixed-`Q` criterion; one displayed higher mixed coefficient excludes the whole family.  This is a **proved positive raw-companion edge and physical rank-drop sharpness theorem**, not universal paired-window supply or a witness. | [Nonzero pair companion and physical rank-drop sharpness](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_NONZERO_PAIR_COMPANION_AND_PHYSICAL_RANK_DROP_SHARPNESS_THEOREM.md), [hostile review](audits/SURPLUS_TWO_RANK_DROP_AND_FOUR_ROOT_SELECTOR_REVIEW_2026-08-16.md) |
| `GLS4` | In every actual maximum-cardinality-root surplus-two hypothetical complex witness, the complete contracted mixed outside target forces one **same** residual pair `Q` with nonzero physical edge block, nonzero complementary permanent tensor, an order-two companion class surviving individually modulo every order-four-and-higher column over the outside function field, and some fully-supported raw `p_(A,Q)!=0`.  The proof excludes the only all-failure rank-one triangle using the corank-six quota, the three pure target tensors, and one common permanental cofactor map.  Separately, the scalar complementary-permanent map is dominant in characteristic not two, so those scalar readings obey no universal Pluecker-type polynomial identity.  This is a **proved exact source-to-individual-supply edge**.  It is not collective pair-observability, full fixed-`Q` coordinate-family observability, a GLD5/GLD7 selector, response nonvanishing, augmented-weight/alignment/anchor supply, permanent extraction, or witness exclusion. | [Same-pair quotient survival and permanent dominance](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_REVIEW_2026-08-20.md) |
| `GLS5` | On a declared Laurent contraction chart, universal geometric-point absorption of a desired column is equivalent to equality of every geometric radical determinantal/Fitting profile; absence of a fibre with both nonzero response and desired survival is the exact response-ideal containment `Rho I_j([A|g]) subset sqrt_geom I_j(A)`.  On the complete GLD7 witness equation this is equivalently the pure-column profile `[A|D]`, and a single shared-variable incidence ideal encodes common attachment for a finite target family.  GLS2 function-field failure instead has an exact projected-kernel/rank-stratum formula.  A coordinate-free quotient class measures the gap between unrestricted recovery and a legal `lambda tensor id` selector.  Exact rational modules show that injective observability, maximal nuisance rank, three pure targets, and nonzero response do **not** imply legal attachment abstractly.  This is a **proved exact failure-topology reduction and abstract no-go**, not a physical countermodel or exclusion of any witness branch. | [Pointwise selector failure and decomposable-retraction boundary](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_POINTWISE_SELECTOR_FAILURE_AND_DECOMPOSABLE_RETRACTION_BOUNDARY_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_FAILURE_MODULE_ALIGNMENT_AND_FOUR_ROOT_SOURCE_TRICHOTOMY_REVIEW_2026-08-20.md) |
| `GLS6` | The `GLS4`-supplied pair has one fully supported residual contraction with `h=H_Q(z_Q)!=0` and raw `p_(A,Q)(z_Q)!=0` simultaneously.  At four roots, ambient augmented alignment has the exact pointwise failure locus `p^T Jp=0` and `Jp in im U^*`; after restricting to a proposed legal-weight subspace `M`, failure is exactly `Jp in M^perp+(p^perp intersect im U^*)`.  Every rank, including rank-drop repair directions, is covered without division.  This is a **proved source corollary and alignment criterion**.  It does not force `M`, response nonvanishing, synchronization, nuisance survival, or a target-pure anchor. | [Common residual contraction and augmented-alignment gate](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_COMMON_RESIDUAL_CONTRACTION_AND_AUGMENTED_ALIGNMENT_GATE_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_FAILURE_MODULE_ALIGNMENT_AND_FOUR_ROOT_SOURCE_TRICHOTOMY_REVIEW_2026-08-20.md) |
| `GLS7` | For an actual maximum-root surplus-two complex witness with root order four, the `GLS4` pair lies in the exhaustive source cover `{O,C} x {R,E,A}`: its order-two block is either observable modulo every other order-two and all higher columns or belongs to a named inclusion-minimal quotient circuit; independently, the seven GLD5 targets have a response-identically-zero branch, one common legal seven-target escape, or a named function-field desired-plus-three-pure absorption branch with denominator-cleared identities and explicit exceptional fibres.  The entire E branch, on both O and C, reaches the required individual pair-supply plus legal same-`Q` GLD5/7 interface; O additionally gives stronger pair-block observability.  An exact physical graph has a rank-15 order-two sensor and seven nonzero responses but no target selector; one complete mixed coefficient excludes it from the witness locus.  This is a **proved six-leaf four-root all-seven source cover and sharp off-target boundary**.  Its four R/A leaves remain open for that stronger GLD3 package; GLS8 gives the exact isolated-one-row refinement.  Root order three, every root order at least five, GLD3 activity, and all downstream nodes are not closed by GLS7. | [Four-root supply-to-attachment trichotomy](../claims/arbitrary-order/FOUR_ROOT_MAXIMAL_ROOT_SUPPLY_TO_ATTACHMENT_TRICHOTOMY_AND_OBSERVABLE_NONSELECTOR_BOUNDARY_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_FAILURE_MODULE_ALIGNMENT_AND_FOUR_ROOT_SOURCE_TRICHOTOMY_REVIEW_2026-08-20.md) |
| `GLS8` | Re-root any `GLS4` source point at its two probe roots and promote every other old root to an open port.  For every root order `r>=3`, the resulting two-probe module has only deck orders `2r-2` and `2r`; Laplace expansion of `Pi_Q` forces one top-minus-two desired coefficient to survive the unique top column.  Complete nuisance slicing gives an exact normalized constant-selector criterion, and the complete GHZ quotient makes a legal nonzero response equivalent to pure quotient rank one.  Geometric radical--Fitting containments give an exact pointwise criterion for simultaneous failure of every promoted target, including response-zero and every exceptional rank drop.  The same criterion refines the standard four-root isolated-one-row topology: GLS7's R/E/A split remains the stronger all-seven GLD3 cover, while one R or A target does not prevent another row from being useful.  This is a **proved arbitrary-root promoted-module reduction and exact isolated-one-row failure criterion**, not proof that any useful row occurs on every witness and not entry to a named committed downstream detector.  Common-package, synchronization, alignment, activity, and any additional anchor gates remain open. | [Promoted two-probe target module](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_REVIEW_2026-08-20.md) |
| `GLS9` | On an actual root-order-four maximum-root surplus-two witness, fix the GLS4 pair `Q`.  If `det H_Q!=0` and all six same-`Q` pair-response tensors vanish identically, rank three forces every direct `U-U` block to vanish.  Maximum-root maximality makes the two `Q-U` block families share a nonempty support of size one or two and forces coordinate residual factors, with an opposite-sign normal form on two ports; the four-port response is then zero automatically.  A projection of the complete contracted six-slot GHZ identity excludes equal residual colours and localizes the only remaining chart to opposite residual colours and pure third-colour `Pi_Q`.  This is a **proved exact full-rank literal-response-zero localization**; GLS10 excludes its localized survivor. | [Full-rank all-response-zero localization](../claims/arbitrary-order/FOUR_ROOT_FULL_RANK_ALL_RESPONSE_ZERO_OPPOSITE_COLOUR_PURE_COMPLEMENTARY_PERMANENT_LOCALIZATION_THEOREM.md), [hostile review](audits/FOUR_ROOT_FULL_RANK_ALL_RESPONSE_ZERO_LOCALIZATION_REVIEW_2026-08-20.md) |
| `GLS10` | In the GLS9 opposite-colour pure-`Pi_Q` chart, the complete `(i,i)` fibre makes the singleton shore impossible because one insertion line cannot carry the two required pure colours `{i,k}`.  In the two-port normal form the same two alpha-lines occur on both residual shores: the `(i,i)` fibre forces them to cover `{i,k}`, while `(j,j)` forces them to cover `{j,k}`.  Two fixed labelled lines cannot satisfy both covers.  The theorem therefore excludes the entire `det H_Q!=0` literal all-seven response-zero branch in characteristic zero.  This is a witness-locus exclusion, not target attachment.  The determinant divisor, every weaker response-zero pattern, all nonzero-response absorbed or exceptional fibres, and the named downstream package remain open. | [Pure complementary-permanent survivor exclusion](../claims/arbitrary-order/FOUR_ROOT_FULL_RANK_ALL_RESPONSE_ZERO_PURE_COMPLEMENTARY_PERMANENT_SURVIVOR_EXCLUSION_THEOREM.md), [hostile review](audits/FOUR_ROOT_FULL_RANK_ALL_RESPONSE_ZERO_PURE_SURVIVOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLS11` | On the determinant divisor with all six pair responses zero, rank zero is absent; rank two reduces to an exactly-two-active-port conformal core, and rank one has an exhaustive contained/one-sided/two-sided trichotomy.  The seventh response is a separate quartic.  This is a **proved exact reduction**, not attachment or exclusion of every survivor. | [Determinant-divisor rank reduction](../claims/arbitrary-order/FOUR_ROOT_DETERMINANT_DIVISOR_ALL_PAIR_RESPONSE_ZERO_RANK_TWO_CORE_AND_RANK_ONE_TRICHOTOMY_REDUCTION_THEOREM.md), [hostile review](audits/FOUR_ROOT_DETERMINANT_DIVISOR_ALL_PAIR_RESPONSE_ZERO_RANK_REDUCTION_REVIEW_2026-08-20.md) |
| `GLS12` | Six complete-target quotients exclude the rank-two conformal core, and a common-incidence column splice excludes the rank-one singleton triangle through exact fourth-order permanent subrank two.  This is a **proved exact exclusion of those two leaves**; the other rank-one branches pass to GLS13 and GLS14. | [Rank-two and singleton-triangle exclusion](../claims/arbitrary-order/FOUR_ROOT_DETERMINANT_DIVISOR_RANK_TWO_CORE_AND_RANK_ONE_SINGLETON_TRIANGLE_EXCLUSION_THEOREM.md), [hostile review](audits/FOUR_ROOT_DETERMINANT_DIVISOR_ALL_PAIR_RESPONSE_ZERO_RANK_REDUCTION_REVIEW_2026-08-20.md) |
| `GLS13` | The two-port two-sided rank-one branch gives an exact weighted `P_5 -> Delta_3` restriction by a twelve-identity common-tail splice; its seventh response is termwise zero.  This is a **proved downstream permanent edge**, not an exclusion or selector theorem. | [Rank-one two-port P5 extraction](../claims/arbitrary-order/FOUR_ROOT_DETERMINANT_DIVISOR_RANK_ONE_TWO_PORT_P5_EXTRACTION_THEOREM.md), [hostile review](audits/FOUR_ROOT_DETERMINANT_DIVISOR_RANK_ONE_TWO_PORT_P5_EXTRACTION_REVIEW_2026-08-20.md) |
| `GLS14` | The remaining contained and one-sided rank-one branches are exhaustively routed to pure decomposable `P_4/P_5` compression interfaces or a balanced Branch-I core.  On that core `Phi!=0` makes the seventh response visible without a legal selector, while `Phi=0` aligns the partitions and leaves one explicit augmented-`P_6` face defect `Psi`.  This is a **reviewed proved exact reduction with primary, independent audit, and hostile review PASS**, not a downstream exclusion or node closure. | [Contained and one-sided permanent reduction](../claims/arbitrary-order/FOUR_ROOT_DETERMINANT_DIVISOR_RANK_ONE_CONTAINED_AND_ONE_SIDED_PERMANENT_REDUCTION_THEOREM.md), [hostile review](audits/FOUR_ROOT_DETERMINANT_DIVISOR_RANK_ONE_CONTAINED_AND_ONE_SIDED_PERMANENT_REDUCTION_REVIEW_2026-08-20.md) |
| `GLS15` | For every root order `r>=2` and every fixed-`Q` pair target in the original `r`-root, `r`-port chart, both physical GLD15 desired columns are images of one linear partial-matching transform: `g_S^M=Psi_C(K^Q)` and `g_S^Z=Psi_C(R)`.  A rank-one selector line `K(delta_S,eta_S)` is exactly absorption of `Psi_C(delta_S R-eta_S K^Q)`.  Applying another target's absorbed direction gives the denominator-free class `(delta_T eta_S-eta_T delta_S)bar g_S`; on a complete witness its product with any selected active diagonal value equals the same determinant times the active pure GHZ class.  This is a **proved arbitrary-root physical companion-exchange and synchronization-obstruction theorem**, not the distinct GLS8 promoted interface, transport-defect vanishing, nonzero operator supply, four-port synchronization, activity, or node closure. | [Physical pair-companion transport](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PHYSICAL_PAIR_COMPANION_TRANSFORM_AND_PROJECTIVE_SYNCHRONIZATION_OBSTRUCTION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_PHYSICAL_PAIR_COMPANION_TRANSFORM_AND_PROJECTIVE_SYNCHRONIZATION_REVIEW_2026-08-20.md) |
| `GLS16` | Maximum-root evaluation sends the original fixed-`Q` pair columns to `g_S^M -> Pi_S(z_Q)` and `g_S^Z -> 0`, while the complete joint nuisance maps exactly to the coefficient slices of every other order-two label.  Thus a surviving base pair class excludes joint rank zero and orients rank one to the common pure-`M` line; every oblique/pure-`Z` line and every rank-zero target forces an explicit swallowed base pair circuit.  Separately, any legal selector for target `T` annihilates both labelled physical columns of every `S!=T` by the exact map from `S-T` to `T-S`.  This is a **proved arbitrary-root base-shadow and cross-target annihilation theorem**, not source-level base survival, foreign nuisance membership, the distinct GLS8 promoted interface, four-port synchronization, activity, or node closure. | [Base-grade pair shadow and cross-target annihilation](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_BASE_GRADE_PAIR_SHADOW_AND_CROSS_TARGET_SELECTOR_ANNIHILATION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_BASE_GRADE_PAIR_SHADOW_AND_CROSS_TARGET_SELECTOR_ANNIHILATION_REVIEW_2026-08-20.md) |
| `GLS17` | For every original fixed-`Q` even target `|S|=2t`, leave `t-1` roots open and evaluate the rest at the maximum root.  Every grade at least `t` vanishes, while the residual-absent grade-`t-1` column becomes an explicit injection/permanent leading tensor and the complete nuisance retains every lower-or-equal-grade label other than `S`.  Survival of one leading class forces the target operator space to contain pure `M`; simultaneous survival gives one common pure-`M` direction even across rank-two spaces.  At `r=4`, six pair shadows plus one explicit four-port first-root covector synchronize all seven rows and enter GLD16 conditionally on its separate activity gate.  This is a **proved arbitrary-root all-even-target grade-shadow and conditional common-selector theorem**, not survival forcing, activity, foreign transport, the distinct GLS8 promoted interface, or node closure. | [Partial-root grade shadow and common pure-M selector](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PARTIAL_ROOT_GRADE_SHADOW_AND_COMMON_PURE_M_SELECTOR_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_PARTIAL_ROOT_GRADE_SHADOW_AND_COMMON_PURE_M_SELECTOR_REVIEW_2026-08-20.md) |
| `GLS18` | Applying each GLS17 partial-root quotient to the complete GLD15 witness equation gives `sum_c alpha_c[d_c] tensor w_c=b tensor M_S`.  Thus the pure leading quotient has rank at most one and is useful exactly when both the leading desired class and physical `M_S` response are nonzero.  Universal failure on every residual contraction and nuisance-rank fibre is exactly a family of geometric radical--Fitting containments, with finite target families encoded at one shared residual point.  At `r=4`, absence of pure `M` makes every four-port first-root nuisance shadow the full three-dimensional root covector space, while a pair shadow is forced to contain only its diagonal three-space inside a nine-space.  This is a **proved arbitrary-root target-coupled failure-profile theorem**, not survival forcing, failure-locus exclusion, activity, foreign transport, GLS8 integration, or node closure. | [Leading-shadow target coupling and Fitting failure](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_LEADING_SHADOW_TARGET_COUPLING_AND_FITTING_FAILURE_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_LEADING_SHADOW_TARGET_COUPLING_AND_FITTING_FAILURE_REVIEW_2026-08-20.md) |
| `GLS19` | For every original fixed-`Q` even target `|S|=2t`, leave `t` roots open and put the residual-absent `M` column into its exact individual-`Z` nuisance.  Every grade above `t` dies, while the grade-`t` residual-present column becomes an explicit injection/permanent top tensor.  Top survival supplies a legal pure-`Z` row; across a finite useful family the direction `(0,1)` is common.  The complete target makes the pure top quotient rank at most one and useful exactly when both the top class and physical `Z_S` response are nonzero, with universal failure encoded by all-rank radical--Fitting containments at one shared residual point.  At `r=4`, seven useful top shadows enter GLD16 with `a=h`, but activity remains separate.  This is a **proved arbitrary-root second-axis target-coupled failure-profile theorem**, not top survival, failure-locus exclusion, activity, foreign transport, GLS8 integration, or node closure. | [Residual-present top shadow and common pure-Z selector](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_TOP_GRADE_RESIDUAL_PRESENT_SHADOW_COMMON_PURE_Z_SELECTOR_AND_TARGET_FAILURE_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_TOP_GRADE_RESIDUAL_PRESENT_SHADOW_COMMON_PURE_Z_SELECTOR_AND_TARGET_FAILURE_REVIEW_2026-08-20.md) |
| `GLS20` | On every GLS8 source Laplace pair `C subset U`, maximum-root contraction of the two probe slots sends the complete `81`-row target module to the exact `9`-row base quotient `V_C^*/epsilon_A(N_C)`.  Base survival is equivalent to a legal normalized selector factoring through that contraction.  The source Laplace identity forces some raw base coefficient nonzero and makes universal base absorption an explicit nonzero `Pi_Q` circuit.  On the complete target the three diagonal base columns have rank at most one and are useful exactly when the base class and physical promoted response are both nonzero; all exceptional fibres are captured by nine-row radical--Fitting containments.  `GLS21` subsequently proves that the retained all-port nuisance makes this base quotient zero on the required `p!=0` gate.  This is a **proved arbitrary-root source-aligned failure reduction with a subsequently closed no-go survival route**, not full `GLS8` absorption, a downstream package, activity, or node closure. | [Promoted source-aligned base shadow](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_SOURCE_ALIGNED_BASE_SHADOW_AND_TARGET_FAILURE_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_SOURCE_ALIGNED_BASE_SHADOW_AND_TARGET_FAILURE_REVIEW_2026-08-20.md) |
| `GLS21` | For every GLS20 source target, the distinct active `D=Q` label is the residual-absent all-port input `H_Uhat`.  Maximum-root contraction turns its coefficient into exactly `p_(A,Q)`, and complete coefficient slicing contributes `pV_C^*` to the nine-row base nuisance.  Thus on the GLS4 gate `p!=0` the base nuisance has rank nine, every base class is absorbed, no selector factors through `epsilon_A`, and all GLS20 Fitting failure containments are automatic.  This is a **proved arbitrary-root factor-through route no-go**, not absorption in the full `81`-row GLS8 quotient, exclusion of upstairs selectors/responses, a witness contradiction, or node closure. | [All-port nuisance collapse](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_BASE_SHADOW_ALL_PORT_NUISANCE_COLLAPSE_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_BASE_SHADOW_ALL_PORT_NUISANCE_COLLAPSE_REVIEW_2026-08-20.md) |
| `GLS22` | On `p!=0`, the denominator-free operator `P_Q=pI-G_Q^A(z_Q) tensor epsilon_A` kills exactly the retained all-port root line and has image `ker epsilon_A`, with `P_Q^2=pP_Q`.  For every promoted target it induces an exact selector-equivalent quotient: `81 -> 72` rows for top-minus-two targets and `9 -> 8` for the top target.  The transverse desired tensor is `t_C=pg_C-q tensor epsilon_A(g_C)`; full legal survival, target-coupled pure rank one, and all-rank failure are equivalent in the transverse module.  Source Laplace terms obey the exact aggregate fork `T_Q=pF_Q-q tensor Pi_Q`.  This is a **proved arbitrary-root all-target transverse reduction and projective-synchronization failure split**, not transverse survival, response supply, common activity, a downstream detector, or node closure. | [All-target transverse quotient](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_REVIEW_2026-08-20.md) |
| `GLS23` | Every active unwanted complement pair `D` contributes exactly `Slice_(D_0-C)(a_D) tensor V_(C-D_0)^*` to a target's complete transverse nuisance, with all intersections typed and the projected top term included exactly for pair targets.  Disjoint projected root slices spanning `ker epsilon_A` fill a pair target's entire `72` rows.  The common root tensor `omega=W_(a_0,a_1)` is nuisance for every pair target and desired for the top target: `omega=0` kills the top row, while `omega!=0` gives exact `63`-row pair quotients and an explicit eight-row top survival test.  At `r=3` this is an exhaustive top-anchor split for all seven promoted shapes.  This is a **proved arbitrary-root physical nuisance decomposition and anchor dichotomy**, not slice-span exclusion, selector/response survival, common activity, a downstream detector, or node closure. | [Transverse nuisance decomposition](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_REVIEW_2026-08-20.md) |
| `GLS24` | Contracting the `GLS23` transverse root factor at either actual probe-root vector gives an exact `8 -> 2` map.  When the corresponding top-anchor marginal is nonzero, wedging by it gives a denominator-free one-dimensional root quotient and an exact physical `9`-row nuisance for every pair target (`72 -> 63 -> 9`).  Its survival is equivalent to a legal selector **factoring through this marginal route**, with complete-target rank and all-rank Fitting profiles preserved.  The anchor splits exhaustively into zero, nonzero-marginal, and nonzero double-transverse branches.  At `r=3`, six useful rows through one common marginal plus a useful top row and `GLD3` activity give the existing nine-word contradiction.  This is a **proved arbitrary-root marginal reduction and conditional `r=3` detector edge**, not equivalence with full selector survival, forced activity, an `r>=4` detector, or node closure. | [One-probe anchor marginal](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ONE_PROBE_ANCHOR_MARGINAL_NINE_ROW_REDUCTION_AND_DOUBLE_TRANSVERSE_BOUNDARY_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ONE_PROBE_ANCHOR_MARGINAL_NINE_ROW_REDUCTION_AND_DOUBLE_TRANSVERSE_BOUNDARY_REVIEW_2026-08-20.md) |
| `GLS25` | On the nonzero double-transverse anchor branch, the retained all-port tensor `q` canonically defines `Xi_Q(v)=pv-s_0 tensor rho_0(v)-rho_1(v) tensor s_1`.  Its image/kernel have dimensions `4/4`, it restricts to `p id` on the double core, and `Xi_Q^2=pXi_Q`.  Wedging the core image by `omega` gives an exact physical `27`-row pair route; the top target has a separate four-row core test with desired `p^2 omega`.  Complete-target rank, all-rank Fitting, and source synchronization descend.  At `r=3`, all six useful core rows plus useful top and activity enter `GLD3`.  This is a **proved arbitrary-root double-core reduction and conditional `r=3` detector edge**, not forced reduced/full survival, zero-anchor exclusion, an `r>=4` detector, or node closure. | [Double-transverse anchor core](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_DOUBLE_TRANSVERSE_ANCHOR_CORE_PROJECTOR_AND_TWENTY_SEVEN_ROW_REDUCTION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_DOUBLE_TRANSVERSE_ANCHOR_CORE_PROJECTOR_AND_TWENTY_SEVEN_ROW_REDUCTION_REVIEW_2026-08-20.md) |
| `GLS26` | On the zero-anchor branch, the complete top-target GHZ quotient forces the projected diagonal root space, of dimension two or three, into the remaining physical pair-label nuisance.  Labels meeting `Q` once lie in the projected residual-shore tangent `P_Q(X_0 tensor V_1^*+V_0^* tensor X_1)`, of dimension at most seven.  Modulo that tangent, either some promoted pair label has an essential nonzero transverse slice, or every colour coordinate line lies in one of the two residual shore spans.  This is a **proved arbitrary-root zero-anchor reconstruction and exact coordinate-shore-cover localization**, not survival of the essential pair in its own complete nuisance, response supply, exclusion of the shore cover, a downstream detector, or node closure. | [Zero-anchor diagonal reconstruction](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ZERO_ANCHOR_DIAGONAL_RECONSTRUCTION_AND_RESIDUAL_SHORE_COVER_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ZERO_ANCHOR_DIAGONAL_RECONSTRUCTION_AND_RESIDUAL_SHORE_COVER_REVIEW_2026-08-20.md) |
| `GLS27` | Retaining the residual pair as a Laurent family, failure of the GLS26 coordinate-shore cover over the function field persists on a nonempty principal open and supplies an essential promoted pair at an actual contraction.  Otherwise one fixed cover persists generically and has exactly the `C12`, `C21`, or `C22` shore normal form.  The GLD11 maximum-root control realizes `C21` identically with nonzero `h,p,Pi_Q`, pure normalization, zero Hamming-one shell, and all responses nonzero, but fails a displayed mixed coefficient.  This is a **proved arbitrary-root residual-family escape/normal-form reduction and sharp mixed-equation boundary**, not target survival, cover exclusion, response/synchronization/activity supply, or node closure. | [Residual-family shore normal forms](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RESIDUAL_FAMILY_GENERIC_ESCAPE_AND_COORDINATE_SHORE_NORMAL_FORM_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RESIDUAL_FAMILY_GENERIC_ESCAPE_AND_COORDINATE_SHORE_NORMAL_FORM_REVIEW_2026-08-20.md) |
| `GLS28` | On the GLS26 zero-anchor branch, every promoted pair target's complete transverse nuisance lies in the root envelope generated by `P_Q(T_Q)` and all other promoted pair root supports.  A desired supplier outside this envelope gives a legal full GLS8 selector; a projected pure-diagonal direction outside it gives the named nonzero-response row.  Universal useful-row failure forces the diagonal defect to remain spanned after deletion of any supplier label, with certificates using at most four labels; full absorption gives supplier relations on at most five labels.  The Laurent E family splits into a principal-open useful row or a fixed generic redundant cover.  This is a **proved arbitrary-root target-envelope and attachment reduction**, not exclusion of the redundant cover or `C12/C21/C22`, synchronization/activity supply, an arbitrary-root downstream detector, or node closure. | [Zero-anchor target envelope](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TARGET_ENVELOPE_PRODUCT_SELECTOR_AND_BOUNDED_REDUNDANT_COVER_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TARGET_ENVELOPE_PRODUCT_SELECTOR_AND_BOUNDED_REDUNDANT_COVER_REVIEW_2026-08-22.md) |
| `GLS29` | On the GLS28 branch with `(d_0,d_1)=(2,2)`, the two shore normals identify the one-dimensional quotient `E/P_Q(T_Q)` and turn every promoted supplier into `k_uv=x_u tensor y_v+y_u tensor x_v`.  The complete GLS23 nuisance has an exact normal-cylinder image, while the complete physical equation becomes `sum_D k_D tensor R_(Uhat-D)=sum_c alpha_c gamma_c e_c^tensor Uhat`.  Active colours force same-channel coefficient/response activity and occurrence at two ports.  On `gamma_0 gamma_1 gamma_2!=0`, intersecting support and exactly two disjoint suppliers are excluded at arbitrary root order; at `r=3`, a complementary-kernel identity exhausts every local-rank and response fibre and forces `gamma_0 gamma_1 gamma_2=0`.  An exact rational same-graph control has all six target nuisances full and all six responses nonzero but fails mixed GHZ coefficients.  This is a **proved arbitrary-root normal-channel reduction and pointwise four-port full-activity exclusion**, not closure of the normal-product divisors, the `r>=4` disjoint branch, other shore ranks, synchronization, or the strategic node. | [Rank-two-shore normal channel](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_TWO_SHORE_NORMAL_CHANNEL_AND_INTERSECTING_SUPPLIER_EXCLUSION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_TWO_SHORE_NORMAL_CHANNEL_AND_INTERSECTING_SUPPLIER_EXCLUSION_REVIEW_2026-08-22.md) |
| `GLS30` | Contracting every complement port by its exact local two-channel kernel isolates one supplier at arbitrary root order, with no division and with every zero-star/response-zero fibre retained.  At `r=3` this gives exact one-active and two-active projected-kernel profiles.  Neither scalar profile is contradictory: exact rational one- and two-active same-graph response decks satisfy the complete normal identity with all six responses nonzero and every normal nuisance image full.  A separate one-active graph also has a maximum torus root, incidence defect four within the bound six, pure coefficients `(1,1,1)`, and the exact normal tensor, but fails two Hamming-one coefficients.  This is a **proved divisor kernel profile and exact six-response/full-normal-image insufficiency boundary**, not a combined maximum-root/full-normal countermodel, a point of the complete zero-anchor witness locus, full top reconstruction, full-nuisance absorption, simultaneous useful-row failure, divisor exclusion, or node closure. | [Normal-product divisor profile](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_NORMAL_PRODUCT_DIVISOR_KERNEL_PROFILE_AND_SAME_GRAPH_SHARPNESS_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_NORMAL_PRODUCT_DIVISOR_KERNEL_PROFILE_AND_SAME_GRAPH_SHARPNESS_REVIEW_2026-08-22.md) |
| `GLS31` | On the rank-two zero-anchor branch, evaluation of the two retained `A` slots along their residual-shore normals polarizes the complete top equation into two first-polarized equations and the old product-normal equation.  The first two retain every one-`Q` labelled deck term; the induced retained-root quotient is exactly the old `gamma` channel, not a second invariant.  An exact rational `r=3` graph simultaneously has a maximum root, incidence defect six, pure coefficients `(1,1,1)`, six nonzero responses, full normal images, the scalar normal identity, the GLS26 diagonal inclusion, and absorption of all six nonzero desired pair tensors in their complete GLS23 nuisances, yet fails exactly `313` mixed GHZ words.  This is a **proved physical polarization and simultaneous-static-gate insufficiency theorem**, not a witness, divisor exclusion, legal selector, arbitrary-root source cover, or node closure. | [Simultaneous absorption and evaluation-pencil sharpness](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIMULTANEOUS_ABSORPTION_EVALUATION_PENCIL_AND_MIXED_EQUATION_SHARPNESS_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIMULTANEOUS_ABSORPTION_EVALUATION_PENCIL_AND_MIXED_EQUATION_SHARPNESS_REVIEW_2026-08-22.md) |
| `GLS32` | Contracting all but one promoted port in either complete `GLS31` first-polarized equation by the exact two-row local kernels gives arbitrary-root, denominator-free singleton identities, including every zero-star and zero-deck fibre.  A rational `r=3` graph has a maximum root, defect three, one-active `L=H` shore profile, pure coefficients `(1,1,1)`, six nonzero responses, full normal images, all three complete projected evaluation-pencil equations with every one-`Q` label retained, the `GLS26` diagonal inclusion, and absorption of all six nonzero desired tensors in complete `GLS23` nuisances, yet fails exactly `316` mixed words.  This is a **proved singleton-kernel profile and whole projected-plane insufficiency theorem**, not a witness, one-/two-active divisor exclusion, legal selector, residual-`Q`-resolved theorem, arbitrary-root source cover, or node closure. | [First-polarized singleton kernels and full-pencil sharpness](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FIRST_POLARIZED_SINGLETON_KERNEL_AND_SIMULTANEOUS_ABSORPTION_SHARPNESS_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FIRST_POLARIZED_SINGLETON_KERNEL_AND_SIMULTANEOUS_ABSORPTION_SHARPNESS_REVIEW_2026-08-22.md) |
| `GLS33` | Keeping the residual pair formal and using the signed shore minors as denominator-free normals turns the two first-polarized equations and the normal equation into exact arbitrary-root polynomial identities of bidegrees `(2,2)`, `(2,2)`, and `(3,3)`.  The missing unprojected constant coefficient contains `pH_Uhat`; all-port and singleton `ker a_u intersect ker b_u` contractions isolate it modulo the exact local two-row nuisance.  The `GLS32` graph has `76/76/0` resolved nonconstant failures and `200` constant failures, with opposite residual monomials explaining the chosen-point cancellation and a direct constant-kernel defect `2!=1`.  This is a **proved residual-family lift and root-deck anchor quotient**, not divisor exclusion, forced anchor/selector survival, other-shore or arbitrary-root source coverage, or node closure. | [Residual-Laurent polarization and root-deck kernel anchor](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RESIDUAL_LAURENT_POLARIZATION_AND_ROOT_DECK_KERNEL_ANCHOR_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RESIDUAL_LAURENT_POLARIZATION_AND_ROOT_DECK_KERNEL_ANCHOR_REVIEW_2026-08-22.md) |
| `GLS34` | The four `GLS33` coefficientwise profiles have an exact block-kernel formula.  On a nonempty **ambient shore-data** Fitting open they reconstruct rank `75` of the `81` probe coefficients, with exactly six missing directions generated by the two physical tangent-root syzygies; the same rank formula retains every exceptional fibre, but no witness-locus intersection with that open is asserted.  Independently, the constant diagonal either restricts nontrivially to `tensor_u(ker a_u intersect ker b_u)`, forcing one root-deck value and all singleton anchor classes to survive simultaneously and excluding `p=0`, or it lies in the exact local-cylinder sum.  The latter has a complete killed-colour/Segre-line classification through zero to three colours.  A same-graph two-active control has silent diagonal and singleton target contractions while retaining the normal identity and six responses, but its physical constant deck has defect `4` and the uncontracted profiles fail.  This is a **proved tangent-root Fitting boundary and pointwise constant-anchor survival/silence case cover**, not a coefficient-side legal selector, complete nuisance survivor, divisor exclusion, arbitrary-root source cover, or node closure. | [Tangent-root Fitting and anchor Segre silence](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TANGENT_ROOT_FITTING_AND_CONSTANT_ANCHOR_SEGRE_SILENCE_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TANGENT_ROOT_FITTING_AND_CONSTANT_ANCHOR_SEGRE_SILENCE_REVIEW_2026-08-22.md) |
| `GLS35` | Re-labeling the raw `D=Q` coefficient `q` as desired defines the exact unprojected nuisance `B_Q^anc=K omega+sum_(D!=Q) Slice_(D intersect Uhat)(g_D)`.  Escape `q notin B_Q^anc` is equivalent to one constant functional isolating the residual-absent deck `H_Uhat`; on the complete target and the GLS34 non-silent gate it makes that deck nonzero and pure diagonal.  Swallowing `q in B_Q^anc` instead forces all three raw pure probe tensors into `B_Q^anc`.  An exact rational local graph satisfies the all-port kernel equation and all four surviving singleton output identities while one raw one-`Q` slice equals `q`, proving that output survival does not force coefficient separation.  The jump is erased by `P_Q`, because `q` is nuisance for every original GLS22/23 target.  At `r=3`, `H_Uhat=C(B)` is not GLD3's residual-present `T`.  This is a **proved raw anchor quotient, interface correction, and local physical no-go**, not a witness, original promoted-target selector, downstream entry, divisor exclusion, arbitrary-root source cover, or node closure. | [Raw root-deck quotient and separation no-go](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RAW_ROOT_DECK_QUOTIENT_AND_OUTPUT_COEFFICIENT_SEPARATION_NO_GO_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RAW_ROOT_DECK_QUOTIENT_AND_OUTPUT_COEFFICIENT_SEPARATION_NOGO_REVIEW_2026-08-22.md) |
| `GLS36` | On `omega=0`, the complete raw anchor nuisance is exactly the image of the incidence-only map with components `xi_0^s tensor Y_u x+X_u x tensor xi_1^s` and `X_u x tensor Y_v y+X_v y tensor Y_u x`; complementary-deck edges disappear from this coefficient map.  On full swallow, every fixed common annihilator row kills all labels, `q`, and the three pure target rows, so it supplies no normalized separator; rank/Fitting membership alone does not manufacture one, although parameter-locus equations may still contribute.  At every fixed residual contraction, the mixed promoted-port equations are exactly the labelwise kernel lift `rho_Q(z)+H_Uhat(z)v in ker sigma_Q` for every primal mixed test and any `sigma_Q(v)=q`; one contraction is not equivalent to the uncontracted target.  Retyping the GLD11 maximum-root graph gives an exact rank-eight `B_Q^anc` containing `q,r_0,r_1,r_2`, equal to the full two-probe flattening image, while retaining triple blockers, pure/Hamming shell data, concision, and all seven nonzero responses.  The graph is diagonal-silent and has `116` mixed failures.  This is a **proved incidence-image reduction, fixed-common-row no-go, fixed-residual labelwise-lift interface, and maximum-root sharpness theorem**, not witness-locus exclusion, non-silent swallowing, an original target selector, arbitrary-root source cover, downstream attachment, or node closure. | [Incidence image and labelwise-lift sharpness](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_REVIEW_2026-08-22.md) |
| `GLS37` | On the zero-anchor full-swallow fibre (`q,r_0,r_1,r_2 in B_Q^anc`), the smallest possible nuisance rank is three.  If both residual shore spans have rank two, the swallowed root deck has diagonal rank two and pins both shores to one two-colour coordinate plane.  Every one-residual and pair incidence generator is then supported in that plane, whose intersection with the three-colour diagonal has rank two, contradicting `B_Q^anc=im sigma_Q=Delta`.  Hence at every promoted root order `r>=3` and on every divisor/rank fibre, full swallow forces `rank B_Q^anc>=4` or a residual shore rank at most one.  The exact GLS35 local graph separately has `q` swallowed, all three pure probes escaping, zero non-`Q` complementary decks, nonzero `pH_Uhat`, and satisfies the GLS36 mixed-port lift for every certificate, while a pure-port slice fails.  This is a **proved pointwise minimal-rank/two-shore fibre exclusion, corrected companion-interface statement, and mixed-only faithfulness no-go**, not an exclusion of shore-rank drops or rank at least four, a full source cover, a legal downstream attachment, or node closure. | [Minimal raw-swallow incidence classification](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_MINIMAL_RAW_SWALLOW_INCIDENCE_CLASSIFICATION_AND_MIXED_ONLY_FAITHFULNESS_NO_GO_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_MINIMAL_RAW_SWALLOW_INCIDENCE_CLASSIFICATION_AND_MIXED_ONLY_FAITHFULNESS_NOGO_REVIEW_2026-08-22.md) |
| `GLS38` | If full swallow had nuisance rank three, then `B_Q^anc=Delta`.  On a nonzero root-companion coefficient `q`, any residual shore of rank at most one is actually rank one; the diagonal rank-one tensor fixes one colour `c`.  Off-diagonal rows of every one-residual incidence column force every port incidence on that probe shore onto the same `c`-axis, so all one-residual and pair columns lie in `K r_c`, contradicting `im sigma_Q=Delta`.  Together with GLS37's two-rank-two-shore exclusion, every promoted `r>=3` rank-three full-swallow fibre with `q!=0` is empty.  Since GLS35 non-silence has `p=epsilon_A(q)!=0`, its full-swallow branch satisfies `rank B_Q^anc>=4` pointwise on every divisor/rank fibre.  This is a **proved arbitrary-root nonzero-root-companion minimal-rank exclusion**, not an exclusion of ranks four through nine or rank-three `q=0` fibres (which may include `p=0` and diagonal silence), raw escape, a legal downstream package, source coverage, or node closure. | [Nonzero-root-companion minimal raw-swallow exclusion](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_NONZERO_ROOT_DECK_MINIMAL_RAW_SWALLOW_EXCLUSION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_NONZERO_ROOT_DECK_MINIMAL_RAW_SWALLOW_EXCLUSION_REVIEW_2026-08-22.md) |
| `GLS39` | For a finite family of whole-domain maps `X_t,Y_t:V_t->K^3`, if every distinct-label polarization `X_s tensor Y_t+X_t tensor Y_s` lands in the three-colour diagonal, then their combined image has rank at most two in characteristic not two.  Add the two fixed residual labels as one-dimensional domains: the residual pair is `q`, the residual-port pairs are the one-`Q` components of `sigma_Q`, and the port pairs are its remaining components.  Rank-three full swallow would give `B_Q^anc=im sigma_Q=Delta`, while the complete auxiliary pair image is `im sigma_Q+Kq=B_Q^anc`, contradicting the bound.  Thus every zero-anchor full-swallow point has `rank B_Q^anc>=4`, including conditional `q=0`, `p=0`, and diagonal-silent fibres.  This is a **proved arbitrary-root unconditional minimal full-swallow rank floor**.  It does not force a silent source point into full swallow, exclude ranks four through nine, turn raw escape into an original target, supply a legal downstream package, close source coverage, or close the node. | [Complete pairwise-diagonal rank bound and minimal raw-swallow exclusion](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_COMPLETE_PAIRWISE_DIAGONAL_FAMILY_RANK_BOUND_AND_MINIMAL_RAW_SWALLOW_EXCLUSION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_COMPLETE_PAIRWISE_DIAGONAL_FAMILY_RANK_BOUND_AND_MINIMAL_RAW_SWALLOW_EXCLUSION_REVIEW_2026-08-23.md) |
| `GLS40` | On every fixed-residual zero-anchor full-swallow fibre, the aggregate incidence/deck map is `J_Q=sum_c alpha_c r_c tensor ell_c-q tensor H_Uhat`, so its image lies in `S=Delta+Kq` and every port test has an exact lift through `ker sigma_Q`.  The canonical excess module `sigma_Q^*(Ann S)` has dimension `k-3` for `q in Delta` and `k-4` otherwise; its rows are nonzero on labelled incidence but cancel after deck aggregation and kill `q,r_0,r_1,r_2`.  On `D(p)`, every promoted pair desired tensor, complete nuisance, and pure column lies in the exact `9(k-1)`-row cylinder `P_Q(B_Q^anc) tensor V_C^*`.  A rational rank-six labelled interface satisfies all `81` fixed-residual target words with freely assigned decks but is not proved physical; a rational rank-five full-swallow incidence family satisfies every mixed lift but fails the pure target by flattening rank `1<3`.  This is a **proved aggregate/excess/cylinder reduction and sharp fixed-interface no-go**, not exclusion of ranks four through nine, physical principal-permanent compatibility, target survival/response, synchronization/activity, source coverage, or node closure. | [Aggregate deck, excess syzygies, and transverse cylinders](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FULL_SWALLOW_AGGREGATE_DECK_EXCESS_SYZYGY_AND_TRANSVERSE_CYLINDER_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FULL_SWALLOW_AGGREGATE_DECK_EXCESS_SYZYGY_AND_TRANSVERSE_CYLINDER_REVIEW_2026-08-23.md) |
| `GLS41` | On every zero-anchor full-swallow `D(p)` fibre, `P_Q` canonically identifies `B_Q^anc/(Delta+Kq)` with `C_Q/P_Q(Delta)`.  For each promoted pair target, the `GLS40` cylinder has the exact filtration `0 -> R_C/(N_C^tr intersect R_C) -> L_C^cyl/N_C^tr -> ((C_Q/P_Q(Delta)) tensor V_C^*)/pi(N_C^tr) -> 0`, where the projected pure core `R_C=P_Q(Delta) tensor V_C^*` has `27` rows for `q notin Delta` and `18` for `q in Delta`.  The complete target identity projects to `[pi(t_C)] tensor response=0`: a surviving excess desired class forces zero response, and every useful nonzero-response row is represented in the pure core.  Pointwise useful rank rise is therefore exactly the three pure columns modulo `N_C^tr intersect R_C`, with the intersection retained by an exact fibre-product kernel on every rank/divisor fibre.  This is a **proved arbitrary-root pure-core/excess-response and all-rank intersection reduction**, not forced pure-core survival, response, synchronization/activity, nuisance survival, a named receiver, `p=0` coverage, raw-escape attachment, or node closure. | [Pure-core/excess-response dichotomy](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FULL_SWALLOW_PURE_CORE_EXCESS_RESPONSE_DICHOTOMY_AND_ALL_RANK_INTERSECTION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FULL_SWALLOW_PURE_CORE_EXCESS_RESPONSE_DICHOTOMY_AND_ALL_RANK_INTERSECTION_REVIEW_2026-08-23.md) |
| `GLS42` | On the zero-anchor branch, applying any constant row in `Ann(Delta)` to the complete open-`A` GHZ equation gives the full-residual one-edge hafnian first variation `F_Bhat^lambda=0`, before residual evaluation and on every fibre.  It is the coefficient `[t]H_Bhat(W+tTheta^lambda)` and obeys an exact pointed-matching recurrence.  Every tensorwise vertex gauge `Theta_st=(a_s+a_t)W_st` satisfies `F_I=(sum_s a_s)H_I`, so the trace-zero gauge family lies in the kernel; no full-kernel classification is claimed.  An exact eight-vertex physical graph with six complementary labels has rank-six full swallow, nonzero `H_Q` and `Pi_Q`, `p(z_Q)=2`, root-root orthogonality, and four detected nonzero decks (two promoted-pair responses and two one-`Q` nuisance decks), while one nonzero excess row is a trace-zero gauge.  A separate displayed root row fails the GHZ equation, so the graph is not a witness.  This is a **proved arbitrary-root identity and selected-excess route boundary**, not pure-core survival, complete `GLS8` eligibility, response synchronization/activity, a receiver, `p=0` coverage, raw-escape attachment, or node closure. | [Full-residual excess hafnian first variation](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FULL_RESIDUAL_EXCESS_HAFNIAN_FIRST_VARIATION_AND_ACTIVE_VERTEX_GAUGE_BOUNDARY_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FULL_RESIDUAL_EXCESS_HAFNIAN_FIRST_VARIATION_AND_ACTIVE_VERTEX_GAUGE_BOUNDARY_REVIEW_2026-08-23.md) |
| `GLQ2` | For fixed named residual contractions, paired block-polarized `q=2` response charts with three mutually cross-observed rank-two port groups have one unique `O(J)` overlap transition.  A connected finite chart graph glues one residual frame exactly when its cycle holonomies are trivial.  Two groups retain a full `GL_2`/contragredient ambiguity, and an exact three-chart physical-response counteratlas has nontrivial rational holonomy.  This is **proved conditional descent and sharp route boundary**: `GLS2` now supplies the paired data on its observable surplus-two branch, while identifying rank, the rank-drop and higher-surplus branches, and weighted-diagonal permanent attachment remain open. | [Two-residual response-atlas theorem](../claims/arbitrary-order/TWO_RESIDUAL_RESPONSE_ATLAS_IDENTIFYING_OVERLAP_AND_HOLONOMY_BOUNDARY_THEOREM.md), [surplus-two supply](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md), [hostile review](audits/UNIVERSAL_EXTRACTION_GLUING_RESPONSE_ATLAS_SUPPORTING_LANES_REVIEW_2026-08-16.md) |
| `GLD1` | Every insertion defect of a literal same-graph `q=2` response vanishes by matching edge-pointing, and one graph's global residual frame makes every identifying-atlas holonomy trivial.  A rational physical control has diagonal uncorrected top block but a nonzero mixed corrected entry cancelled by `hB`.  The exact target attachment is `Omega T=Omega Lambda_Q-hY+hN`; a mixed corrected component becomes an explicit GHZ coefficient only for `h=0` or a nonzero coefficient-pure selector with proved nuisance control.  Odd-root selectors and maximal-root base selectors with `r>2` vanish.  This is a **proved detector boundary and conditional target bridge**, not a forced selector. | [Same-graph defect and target-selector boundary](../claims/arbitrary-order/SAME_GRAPH_RESPONSE_DEFECT_VANISHING_AND_TARGET_COUPLED_SELECTOR_BOUNDARY_THEOREM.md), [hostile review](audits/UNIVERSAL_SUPPLY_AND_TARGET_COUPLED_DETECTION_REVIEW_2026-08-16.md) |
| `GLD2` | At four roots, the zero-root-edge and one-root-edge grades have an exact common-shore decomposition.  For `h!=0`, one zero-grade equation removes the direct nuisance exactly when `l-kappa p` lies in the kernel of the six direct response tensors; nonzero augmented `Omega=l^T Jp` does not imply this alignment and is itself unforced by `GLS4`.  Function-field inversion is not target purity.  One sufficient detector package uses a legal constant `l` with `l^T Jp!=0`, constant synchronized response/direct selectors, and a separate target-pure residual-absent anchor or exact nuisance identity.  This package is not proved minimal.  One coefficientwise-clean shore has trivial corrected response, and a maximum-root triple-blocker control has augmented `Omega!=0`, nonzero corrected response, and both adjacent matching grades zero by nested cancellation.  This is a **proved conditional detector interface and sharp single-shore no-go**, not a witness or forced detector. | [Four-root constant-selector boundary](../claims/arbitrary-order/FOUR_ROOT_PAIRED_GRADE_CONSTANT_TARGET_SELECTOR_AND_SINGLE_SHORE_CLEANNESS_BOUNDARY_THEOREM.md), [hostile review](audits/SURPLUS_TWO_RANK_DROP_AND_FOUR_ROOT_SELECTOR_REVIEW_2026-08-16.md) |
| `GLD3` | For one physical same-`Q` four-port response, the six residual-present pair tensors and the residual-present four-port tensor obey `hT=C(D)-C(K)`, while every one-port flattening of the corrected compound `C(K)` has rank at most two.  If nuisance-free constant synchronized target selectors supply the exact diagonal `D` and `T` tensors and three colours have nonzero complementary pair-depth products at one port, a displayed `3 x 3` minor forces at least one of nine actual mixed target coefficients to be nonzero (and excludes the active chart outright at `h=0`).  An exact rational same-graph response has diagonal pair data, three nonzero pure four-port coefficients, zero complete mixed four-port target, rank-two residual frames, and two inequivalent mixed corrected channels while only two colours are active.  This is a **proved conditional nine-word detector and sharp two-active camouflage boundary**, not universal target attachment, paired-window supply, or permanent extraction. | [Pair/four-port diagonal interference](../claims/arbitrary-order/TWO_RESIDUAL_PAIR_FOUR_PORT_DIAGONAL_INTERFERENCE_AND_CAMOUFLAGE_BOUNDARY_THEOREM.md), [hostile review](audits/PAIR_FOUR_PORT_DIAGONAL_INTERFERENCE_REVIEW_2026-08-16.md) |
| `GLD4` | Two constant uncontracted chart equations have an exact target-incidence trichotomy: nonincidence, unique common-sector supply, or affine ambiguity.  A left syzygy always converts nonincidence into a target-defect aggregate; after every pure word is synchronized, it becomes a mixed aggregate and displays one coefficient exactly under a coefficient-pure-modulo-pure-anchors condition.  Bare affine cokernel data have arbitrarily dense defects.  At the physical response-package level, an arbitrary sunflower of overlapping same-`Q` `K_4` windows has literal identity overlaps, diagonal pair data, the same three nonzero pure four-port coefficients, zero mixed four-port coefficients, and only two active colours.  Two physical sign realizations preserve all selected `D`/`T` packages but differ on the corrected channel; complete paired `M,Z` charts would distinguish them.  This is a **proved affine supply/detect theorem and sharp multi-window observed-package boundary**, not constant target attachment, a full response-atlas ambiguity, a witness, or permanent extraction. | [Two-chart target incidence and cloned atlas](../claims/arbitrary-order/TWO_CHART_TARGET_INCIDENCE_AND_CLONED_CAMOUFLAGE_ATLAS_BOUNDARY_THEOREM.md), [hostile review](audits/TWO_CHART_TARGET_INCIDENCE_AND_CLONED_ATLAS_REVIEW_2026-08-16.md) |
| `GLD5` | For one full fixed-`Q`, four-root/four-port companion module retaining all `2079` nonempty even deck coordinates, a desired pair or four-port projection has a constant module selector exactly when its companion coefficient `g_S` survives modulo every nuisance coefficient slice `N_S`.  This is the exact noncircular criterion `P_S in im A_S`; failure is module nonmembership, not an unrestricted sensor kernel or physical graph ambiguity.  A maximum-root triple-blocker chart has all seven selectors for `t!=0`, while another point on the same graph-side incidence stratum has `g_U!=0` and `N_U=L_U^*`, so even `T` attachment fails.  This is a **proved constant-selector quotient theorem and sharp maximum-root incidence boundary**, not proof that the good quotient meets every witness. | [Four-root constant target-module quotient](../claims/arbitrary-order/FOUR_ROOT_CONSTANT_TARGET_MODULE_SELECTOR_QUOTIENT_AND_MAXIMUM_ROOT_SHARPNESS_THEOREM.md), [hostile review](audits/CONSTANT_TARGET_MODULE_AND_SIX_PORT_WICK_REVIEW_2026-08-17.md) |
| `GLD6` | On one physical same-`Q` `h=0` response, every scalar six-port coefficient word has a `15 x 15` Wick map from direct pairs to the fifteen four-port rows.  Its physical rank-two determinant is explicit; `5+1` singular words still have ten-row cross-pair selectors, and overlapping two-shore unions of at least seven ports are coordinatewise injective.  On the fully two-active nonvanishing diagonal line locus, polarization over all fifteen `K_4` subwindows reconstructs every coefficient of every direct pair block, including inactive coefficients.  Target-diagonal four-port rows then force `B^0=cK^0`, `B^1=-cK^1`; one nonzero pure four-port row forces an explicit nonzero mixed `2+4` depth-six row.  This is a **proved conditional all-subwindow supply and deeper-response detector**, with legal attachment of every used `z_2,z_4,z_6` row, the tensor-valued witness singular locus, and permanent extraction still open. | [Six-port physical Wick selector](../claims/arbitrary-order/SIX_PORT_PHYSICAL_WICK_SELECTOR_TWO_ACTIVE_ALL_SUBWINDOW_AND_DEEPER_RESPONSE_THEOREM.md), [hostile review](audits/CONSTANT_TARGET_MODULE_AND_SIX_PORT_WICK_REVIEW_2026-08-17.md) |
| `GLD7` | Quotienting the full fixed-`Q` hypothetical-witness equation by all `GLD5` nuisance slices leaves one decomposable tensor.  Hence the active pure GHZ classes have quotient rank at most one.  Rank at least two is an exact target-incidence obstruction; rank one forces both the desired quotient class and a nonzero physical response, so the legal constant selector exists; rank zero is the swallowed-pure branch, and under a nonzero response it is exactly selector failure.  The identical module argument applies conditionally to the fifteen pair, fifteen four-port, and one six-port rows of a six-root/six-port chart.  This is a **proved witness-target rank-one trichotomy and conditional attachment theorem**, not proof that all seven or all thirty-one pure ranks equal one, and not a coefficient-pure syzygy. | [Fixed-Q target quotient rank-one trichotomy](../claims/arbitrary-order/FIXED_Q_FULL_MODULE_TARGET_QUOTIENT_RANK_ONE_PURE_SURVIVAL_AND_SIX_PORT_ATTACHMENT_TRICHOTOMY_THEOREM.md), [hostile review](audits/FIXED_Q_TARGET_QUOTIENT_AND_GLOBAL_SQUARE_FREE_WICK_REVIEW_2026-08-17.md) |
| `GLD8` | For one scalar physical rank-two channel on `n>=7` ports, the aggregate pair-to-four-row Wick map is multiplication by two linear forms in the square-free algebra.  It is injective exactly when both factor supports have size at least five and their union has size at least seven, or the union has size six and the `GLD6` discriminant is nonzero.  A five-port union has exact kernel dimension five.  Full scalar edge support forces injectivity.  With one full factor and one five-support factor, every pair has a selector on at most twenty-one rows of one seven-set even though all five principal six-window determinants through the two zero ports vanish.  This is a **proved exhaustive scalar support-union classification and bounded common-row selector**, downstream of legal row attachment and not a tensor-word cover or permanent restriction. | [Global square-free Wick classification](../claims/arbitrary-order/GLOBAL_SQUARE_FREE_PHYSICAL_WICK_SUPPORT_UNION_CLASSIFICATION_AND_COMMON_ROW_SELECTOR_THEOREM.md), [hostile review](audits/FIXED_Q_TARGET_QUOTIENT_AND_GLOBAL_SQUARE_FREE_WICK_REVIEW_2026-08-17.md) |
| `GLD9` | For one fixed graph and residual pair `Q`, let the fully supported residual contraction vary on one irreducible torus.  If every member of a finite selector family survives at a point where its complete nuisance matrix has maximal rank, exact nuisance and augmented minors define nonempty principal opens whose finite intersection supplies one common contraction with all selector identities.  On a hypothetical witness, adding one nonzero response coordinate at each such point similarly synchronizes all seven or all thirty-one rank-one attachments.  Two exact one-parameter modules have disjoint survival loci confined to different rank-drop points, so the maximal-rank hypothesis is sharp.  This is a **proved common-contraction synchronization theorem**, not proof that any individual maximal-rank survival point exists on every witness. | [Maximal-nuisance-rank common contraction](../claims/arbitrary-order/FIXED_Q_MAXIMAL_NUISANCE_RANK_COMMON_CONTRACTION_SYNCHRONIZATION_THEOREM.md), [hostile review](audits/COMMON_CONTRACTION_TENSOR_WICK_AND_ALL_DEPTH_RESPONSE_REVIEW_2026-08-17.md) |
| `GLD10` | On one fixed physical same-`Q`, `h=0` seven-port response, five bi-supported helper coefficient vectors select any requested direct-pair tensor coefficient from at most twenty-one, six, or one attached four-port coefficient rows according to whether zero, one, or two endpoint vectors vanish.  One helper coefficient at every port therefore reconstructs all `21*9=189` direct-pair coefficients from the thirty-five `K_4` tensors.  Pair diagonality, one rank-two diagonal pair response, and no isolated response port are an exact observable sufficient entry condition.  Six-port `3+3` and seven-port five-support controls show that four helpers and target diagonality alone do not suffice.  This is a **proved full tensor word cover on the five-helper stratum**, with legal attachment of all thirty-five same-`Q` `z_4` tensors still an input. | [Seven-port five-helper tensor Wick selector](../claims/arbitrary-order/SEVEN_PORT_FIVE_NONISOTROPIC_HELPER_TENSOR_WICK_SELECTOR_THEOREM.md), [hostile review](audits/COMMON_CONTRACTION_TENSOR_WICK_AND_ALL_DEPTH_RESPONSE_REVIEW_2026-08-17.md) |
| `GLD11` | One exact four-root maximum-root graph has triple blockers at all six outside modes, pure coefficients one, zero Hamming-one shell, local concision, and all seven physical responses nonzero, yet every one of the twenty-one active pure target classes lies in its complete nuisance space, so all seven quotient ranks are zero.  A displayed mixed ten-mode coefficient equals one, hence the control is not a GHZ witness.  This is a **proved simultaneous swallowed-pure physical graph-side sharpness theorem**: the full mixed target equations are load-bearing, and the control is neither a witness-locus point nor a counterexample. | [Simultaneous swallowed-pure physical control](../claims/arbitrary-order/FOUR_ROOT_SIMULTANEOUS_SWALLOWED_PURE_NONZERO_RESPONSE_PHYSICAL_CONTROL_THEOREM.md), [hostile review](audits/COMMON_CONTRACTION_TENSOR_WICK_AND_ALL_DEPTH_RESPONSE_REVIEW_2026-08-17.md) |
| `GLD12` | For fixed `K` in the complete labelled square-free tensor algebra at `h=0`, the entire residual-present `Z` fibre through `B` is exactly `B+ker(mu_K:A_2->A_4)`.  Hence equality of the full tensor four-port layer is equivalent to equality at every deeper `Z` layer and every principal subwindow.  A one-edge tensor direction lies in the kernel exactly when its endpoints cover the whole-block support graph; a genuine multi-edge cancellation shows the full kernel is larger.  Exact nonisolated `K_(5,2)` and star controls remain invisible at every `Z` depth.  This is a **proved full-tensor four-port closure and all-depth `Z`-fibre boundary**, not paired `(M,Z)` agreement, same-graph ambiguity, witness integration, or permanent extraction. | [Full tensor h-zero Z fibre](../claims/arbitrary-order/TWO_VERTEX_COVER_ALL_DEPTH_H_ZERO_RESPONSE_FIBRE_THEOREM.md), [hostile review](audits/COMMON_CONTRACTION_TENSOR_WICK_AND_ALL_DEPTH_RESPONSE_REVIEW_2026-08-17.md) |
| `GLD13` | For one full uncontracted hypothetical witness, one graph, and one residual pair `Q`, extend the seven complete nuisance modules to the function field of the six-dimensional fully supported contraction torus.  If every generic augmented rank rises, exact nuisance/augmented minors and one nonzero response coordinate per target have a common principal open, yielding one contraction with all seven quotient ranks one and hence the exact `D_uv,T` package.  Otherwise some desired column is generically nuisance-absorbed, and the witness quotient identity forces all three pure columns into the same function-field nuisance image; clearing one denominator supplies four polynomial identities.  Exceptional rank-drop escape may still occur.  This is a **proved common-escape or generic pure-absorption dichotomy**, not exclusion of the bad branch, proof that either geometric behaviour is pointwise exclusive, activity, or permanent extraction. | [Contraction escape / function-field pure absorption](../claims/arbitrary-order/FIXED_Q_CONTRACTION_ESCAPE_OR_FUNCTION_FIELD_PURE_ABSORPTION_DICHOTOMY_THEOREM.md), [hostile review](audits/CONTRACTION_ESCAPE_AND_PAIRED_RESPONSE_CLOSURE_REVIEW_2026-08-17.md) |
| `GLD14` | On a fixed full residual-present `Z` fibre `B_0+L`, any fixed legally attached linear package of residual-absent pair rows cuts the fibre by the exact empty/affine/unique trichotomy with ambiguity `L intersect ker P`; `dim L` scalar `M_2` rows are sufficient and optimal.  After pair diagonality, all mixed coefficients of `M=exp(B)` vanish at every depth exactly when differently coloured active edge families are cross-intersecting, already certified by the `270` two-colour `M_4` rows (`360` rows including pair diagonality).  A one-pure-colour support decomposition is exhaustive; for the complete-bipartite `K_(3,3)` channel the full ternary kernel has dimensions `16` total, `12` mixed, and `4` pure with an explicit unimodular coordinate package.  This is a **proved paired-response incidence and all-depth mixed-shape boundary**, downstream of legal same-graph same-`Q` `M` attachment and not witness integration or permanent extraction. | [Paired M2/M4 response closure](../claims/arbitrary-order/PAIRED_M2_AFFINE_INCIDENCE_ONE_COLOUR_KERNEL_AND_ALL_DEPTH_MIXED_SHAPE_THEOREM.md), [hostile review](audits/CONTRACTION_ESCAPE_AND_PAIRED_RESPONSE_CLOSURE_REVIEW_2026-08-17.md) |
| `GLD15` | In one complete fixed-`Q` companion module, retain both desired labels `I=S` and `I=Q union S` and quotient by coefficient slices of every other label.  The surviving two-column rank is exactly the dimension of the constant-open-port operator combinations `aM_S+bZ_S`: rank two gives separate normalized selectors, rank one one projective combination, and rank zero none.  On a hypothetical witness, pure quotient rank two is equivalent to joint selector rank two and response independence.  Rank one is ambiguous, including an `M`-active combination useful only on an independently fixed `Z` fibre.  Exact pair-block covers have `kappa=4` for full ternary complete-bipartite `K_(3,3)` and `kappa=6` for full ternary `K_(5,2)`; one four-port and two pair rank-two targets give a localized coefficient-pure `M_4` detector under complementary-edge activity.  `GLD11` has exact graph-side ranks six times one and once zero despite nonzero paired responses.  This is a **proved joint-module paired-attachment and fixed-fibre block-cover boundary**, not proof that any needed rank is two on the witness locus, physical integration of a formal fibre, activity, or permanent extraction. | [Joint M/Z quotient and paired attachment](../claims/arbitrary-order/FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md), [hostile review](audits/FIXED_Q_JOINT_MZ_QUOTIENT_AND_PAIRED_ATTACHMENT_REVIEW_2026-08-17.md) |
| `GLD16` | Intersect the seven exact `GLD15` operator-coefficient spaces inside one fixed `M/Z` coefficient plane.  The intersection is nonzero exactly when no target space is zero and all rank-one spaces have the same projective slope.  For arbitrary physical residual scalar `h`, any common `(delta,eta)` supplies one same-graph, same-`Q`, same-contraction shifted package with effective scalar `a=delta+h eta`, `D_e=aB_e+eta K_e`, and the denominator-free identity `aT'=C(D)-C(eta K)`.  The `GLD3` rank-two corrected-channel determinant excludes this branch under three-colour pair-depth activity: `a=0` is a rank contradiction and `a!=0` exposes one of nine mixed selected coefficients.  Exact unequal-slope three-active and common-line two-active controls prove synchronization and activity are both load-bearing.  This is a **proved arbitrary-`h` common-projective selector criterion and conditional shifted detector**, not common-line forcing, witness integration, or permanent extraction. | [Common projective joint-response selector](../claims/arbitrary-order/FIXED_Q_COMMON_PROJECTIVE_JOINT_RESPONSE_SELECTOR_AND_SHIFTED_GLD3_DETECTOR_THEOREM.md), [hostile review](audits/FIXED_Q_COMMON_PROJECTIVE_JOINT_RESPONSE_SELECTOR_ARBITRARY_H_REVIEW_2026-08-20.md) |
| `GLD17` | Normalize all six pair operator rows to `[1:p]` and the four-port row to `[1:t]` on one fixed `h=0` response.  When `p(p-2t)=0` and `p!=t`, the quadratic `C(K)` correction vanishes.  If all selected pair blocks are diagonal and one complementary pair has all six diagonal entries nonzero, twelve oriented `2+1+1` rows diagonalize its two physical channel blocks and six ordered `2+2` rows force one block to rank three.  Hence one of eighteen displayed mixed four-port coefficients is nonzero.  Exact cancellation-branch and noncancellation controls separately prove the local nonvanishing and slope relation are load-bearing.  This is a **proved unequal-slope eighteen-word detector and conditional module exclusion**, not slope/support forcing, an exhaustive classification of other slopes, witness integration, or permanent extraction. | [Unequal-slope quadratic cancellation](../claims/arbitrary-order/FIXED_Q_UNEQUAL_SLOPE_QUADRATIC_CANCELLATION_THREE_FULL_PAIR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_UNEQUAL_SLOPE_QUADRATIC_CANCELLATION_REVIEW_2026-08-17.md) |
| `GLD18` | For each complete `GLD15` target quotient, every legally attachable operator coefficient lies in the kernel of the realized mixed-response map on a hypothetical witness.  Thus a rank-one operator line is either recovered from exact mixed-response minors or is response-invisible and remains module-only.  With six independent `M`-active pair slopes `p_e` and one four-port slope `t`, the response has an exact complementary-matching expansion with corrections `gamma_(ef)=p_ep_f-t(p_e+p_f)`.  If all three corrections vanish, global pair diagonality and one three-full complementary pair whose two slopes differ from `t` force one of eighteen displayed mixed rows.  The cancellation locus splits exactly into nonzero-`t` support divisors and a `t=0` pure-`M` boundary.  For globally vertex-factorable rank-one physical channels, one three-full complementary pair excludes every common slope, with branch-specific `GLD16`, `GLD17`, or twenty-five-word detectors.  This is a **proved response-visible slope interface, edge-dependent cancellation detector, and decomposable-channel exclusion**, not operator-space or support forcing, a projective pure-`Z` extension, witness integration, or permanent extraction. | [Response-visible and edge-dependent slopes](../claims/arbitrary-order/FIXED_Q_RESPONSE_VISIBLE_OPERATOR_SLOPE_AND_EDGE_DEPENDENT_CANCELLATION_DIVISOR_THEOREM.md), [hostile review](audits/FIXED_Q_RESPONSE_VISIBLE_OPERATOR_SLOPE_AND_EDGE_DEPENDENT_CANCELLATION_REVIEW_2026-08-17.md) |
| `GLD64` | On the `GLD18` all-`M`-active `h=0` response, suppose the physical channel factors globally as `K_uv=a_u tensor a_v`, all six independently sloped selected pair blocks are diagonal, and one complementary pair is three-full.  Thirty-six `2+1+1` rows and six named `2+2` rows first force full ternary support.  The resulting edge relations reduce the fixed `3+1` row to `-2G` times a nonzero port monomial, killing the aggregate quadratic correction in characteristic zero; a final named `2+2` row is then nonzero.  Hence all six finite pair slopes, with no synchronization or cancellation hypothesis, are excluded in this physical class after seven legal `GLD15` rows attach.  This is a **proved forty-three-word globally decomposable variable-slope exclusion**, not legal-row, decomposability, three-fullness, pure-`Z`, general rank-two, arbitrary-root source, or permanent forcing. | [Decomposable variable-slope exclusion](../claims/arbitrary-order/FIXED_Q_GLOBALLY_DECOMPOSABLE_CHANNEL_VARIABLE_SLOPE_THREE_FULL_PAIR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_GLOBALLY_DECOMPOSABLE_CHANNEL_VARIABLE_SLOPE_THREE_FULL_PAIR_EXCLUSION_REVIEW_2026-08-23.md) |
| `GLD65` | **Partially withdrawn on 2026-08-24.**  The standalone matching stratification, diagonal-support lemma, and abstract conditional dimension lemma remain correct.  The claimed cross-Gram identity transferred a legal-selector equation for the root companion `G_(Q union {u,v})` to the distinct full matching coefficient `F_(Q union {u,v})`; the latter actually contains the direct term `B_uv G_Q`.  The three-colour product-selector exclusion and its downstream corollaries are therefore withdrawn. | [Partially withdrawn GLD65 record](../claims/arbitrary-order/FIXED_Q_FOUR_ROOT_PRODUCT_SELECTOR_THREE_COLOUR_CAMOUFLAGE_EXCLUSION_THEOREM.md), [superseded historical review](audits/FIXED_Q_FOUR_ROOT_PRODUCT_SELECTOR_THREE_COLOUR_CAMOUFLAGE_EXCLUSION_REVIEW_2026-08-23.md), [interface correction](../claims/arbitrary-order/FIXED_Q_PRODUCT_SELECTOR_ROOT_COMPANION_FULL_COEFFICIENT_SEPARATION_AND_THREE_COLOUR_COUNTEREXAMPLE.md) |
| `GLD66` | **Withdrawn in its load-bearing product-selector conclusions on 2026-08-24.**  Its response-anchor subspace observation survives as a conditional linear-algebra statement, but the common cross-pairing identity inherited from `GLD65` is false.  Consequently the at-most-one-colour conclusion, two-colour exclusion, and synchronized-plane corollaries are not live frontier reductions. | [Partially withdrawn GLD66 record](../claims/arbitrary-order/FIXED_Q_FOUR_ROOT_PRODUCT_SELECTOR_TWO_COLOUR_EXCLUSION_AND_FIRST_ROOT_PLANE_SYNCHRONIZATION_THEOREM.md), [superseded historical review](audits/FIXED_Q_FOUR_ROOT_PRODUCT_SELECTOR_TWO_COLOUR_EXCLUSION_AND_FIRST_ROOT_PLANE_SYNCHRONIZATION_REVIEW_2026-08-23.md), [interface correction review](audits/FIXED_Q_PRODUCT_SELECTOR_ROOT_COMPANION_FULL_COEFFICIENT_INTERFACE_CORRECTION_REVIEW_2026-08-24.md) |
| `GLD67` | A normalized legal pure-`M` product selector annihilates every evaluated root companion except `G_Q=m`, but it does **not** annihilate the corresponding full matching coefficient: exactly `F_(Q union {u,v})=mB_uv`.  An explicit ternary maximum-root graph has a `GLS17`-factored complete legal row, all six direct port blocks diagonal, and `M_U=0000+1111+2222`; all `431` evaluated companion entries satisfy the selector while `G_(Q union {u_0,u_1})=0` and `F_(Q union {u_0,u_1})=1`.  This is a **proved coefficient-type correction, exact graph-side counterexample to GLD65, and source-route obstruction for GLD66**, not a GHZ witness or a counterexample to Krenn--Gu. | [Root-companion/full-coefficient separation](../claims/arbitrary-order/FIXED_Q_PRODUCT_SELECTOR_ROOT_COMPANION_FULL_COEFFICIENT_SEPARATION_AND_THREE_COLOUR_COUNTEREXAMPLE.md), [hostile correction review](audits/FIXED_Q_PRODUCT_SELECTOR_ROOT_COMPANION_FULL_COEFFICIENT_INTERFACE_CORRECTION_REVIEW_2026-08-24.md) |
| `GLD68` | At root order four, let `S` and `T=U-S` be complementary port pairs.  The complete target-`S` base nuisance contains the order-two label `I=T`, whose maximum-root term is `H_T tensor Pi_T` in the exact receiver/target factorization.  If `Pi_T!=0`, its coefficient slices span the whole target-`S` base receiver and force `b_S=0`; if `Pi_T=0`, then `b_T=0`.  Hence complementary pair base shadows are mutually exclusive, at most three of six survive, and every maximal survivor set is a star or triangle.  The all-six pair-base source premise formerly feeding the `GLS17 -> GLD16` route is therefore empty.  This is a **proved complete-module source exclusion**, not a statement about non-leading legal rows, full operator-space intersections, promoted sources, other root orders, response activity, or global resolution. | [Complementary-pair base-nuisance saturation](../claims/arbitrary-order/FOUR_ROOT_COMPLEMENTARY_PAIR_BASE_NUISANCE_SATURATION_AND_SEVEN_SHADOW_SOURCE_EXCLUSION_THEOREM.md), [hostile review](audits/FOUR_ROOT_COMPLEMENTARY_PAIR_BASE_NUISANCE_SATURATION_REVIEW_2026-08-24.md) |
| `GLD69` | For each of the eight maximal `GLD68` survivor families, the three targetwise relations have one exact labelled direct-sum module.  Every star and triangle nevertheless has a three-colour formal model satisfying the complete foreign port-pair nuisances and aggregate `Delta_4`, so coefficient data alone give no contradiction.  Physically, all six companions are pullbacks of `J=P_4(xi,eta,-,-)`.  With four rank-three ports a maximal profile forces `rank J=2`; a star contains the common radical plane at all ports, while a triangle has three equal maximal-isotropic sibling hyperplanes but a centre which need contain only one radical line.  The internal six-label port-pair image has exact dimension `21` for a star and `19` for a triangle, and weighted concise GHZ belongs to neither; the complete equation still has nine labels meeting `Q`.  Every rank-two zero-diagonal form has a support-at-most-two radical vector.  If such a vector lies in all four port images, its common pullback annihilates all fifteen contracted order-two labels; a nonzero weighted-GHZ evaluation is therefore a contradiction.  This condition is automatic up to the final scalar on stars and conditional on the centre incidence for triangles.  Exact controls make the scalar-zero star and nonsparse-centre triangle gaps real.  This is a **proved common-incidence bridge, universal pair-layer obstruction, nonzero-scalar star detector, and exact no-go/boundary classification**, not a universal complete maximal-profile exclusion or a statement about lower port ranks, fewer survivors, other root orders, non-leading/promoted sources, or global resolution. | [Common-incidence and sparse-radical detector boundary](../claims/arbitrary-order/FOUR_ROOT_MAXIMAL_BASE_SURVIVOR_COMMON_INCIDENCE_AND_SPARSE_RADICAL_DETECTOR_BOUNDARY_THEOREM.md), [hostile review](audits/FOUR_ROOT_MAXIMAL_BASE_SURVIVOR_COMMON_INCIDENCE_REVIEW_2026-08-24.md) |
| `GLD70` | The complete contracted four-port nuisance has one exact `1+24+54=79` raw-column map.  A cubic epsilon contraction cuts the concise GHZ orbit out of the complex third Segre secant, so a witness forces an epsilon-nonzero third-secant point in that nuisance space; the flattening-plus-Strassen equations make its absence one exact saturation obligation.  On the fully supported residual-coordinate locus, `rank J=2` forces the ratio pattern `(1,1,1,-1)` up to the declared gauges, and every nonisotropic maximal-star quotient slope gives the same fixed `44`-dimensional nuisance space, with a `23`-dimensional quotient beyond the rank-`21` pair layer.  The projection-full triangle has dimension `35` and corrected quotient dimension `16`.  The `Q` generator has `epsilon=-288` but balanced ranks `(5,5,5)`, so epsilon alone is insufficient.  This is a **proved complete-map/secant reduction and torus-star infinite-family compression**, not the restricted saturation, a complete maximal-profile exclusion, a triangle compression, residual-boundary or lower-rank coverage, source integration, or global resolution. | [Complete Q-layer secant boundary trap and torus-star compression](../claims/arbitrary-order/FOUR_ROOT_COMPLETE_Q_LAYER_SECANT_BOUNDARY_TRAP_AND_TORUS_STAR_COMPRESSION_THEOREM.md), [hostile review](audits/FOUR_ROOT_COMPLETE_Q_LAYER_SECANT_BOUNDARY_TRAP_AND_TORUS_STAR_COMPRESSION_REVIEW_2026-08-24.md) |
| `GLD71` | In the fixed `GLD70` torus-star space, the rank-`21` pair layer is exactly the coordinate erasure with at least two leaf indices equal to `2`.  Puncturing leaves a rank-`23` code in dimension `60` with a `37`-dimensional syndrome.  Every non-erased decomposable leaf word has syndrome rank exactly `3` in characteristic zero; six root-slice checks and three binary balanced determinants give an Eisenstein `A_2` norm gate.  A nonhidden exact second-secant point has a rank-`5` two-word syndrome block and singular centre, refuting MDS-style pairwise independence.  `GLD72` subsequently refutes the proposed determinant-safe three-word target while leaving every proved `GLD71` assertion intact.  This is a **proved punctured-code parent theorem, one-word atlas, and exact boundary control**, not source integration, residual-boundary or triangle coverage, or global resolution. | [Punctured syndrome and Eisenstein-norm gate](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_PUNCTURED_SYNDROME_AND_EISENSTEIN_NORM_GATE_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_PUNCTURED_SYNDROME_AND_EISENSTEIN_NORM_GATE_REVIEW_2026-08-24.md) |
| `GLD72` | The exact Gaussian-rational frames `G=[[1,1,1],[0,0,1+i],[0,1,1]]` and `A=[[-2-2i,-1+2i,3],[0,-3+3i,0],[0,-1+2i,1]]` define a three-word tensor in the original fixed rank-`44` nuisance space.  The full syndrome has rank `7` and kills `vec(A)`; `det G=-1-i`, `det A=12`, all four local and all three balanced ranks are `3`, and `epsilon=144-144i`.  Thus the fixed-star GHZ exclusion, balanced-minor shortcut, and determinant-safe saturation are **exactly refuted**.  The tensor has `61` nonzero displayed coordinates and no legal graph/source lift is supplied.  This is a **proved fixed-space counterexample and route correction**, not a graph witness, source-integrability theorem, counterexample to Krenn--Gu, or global resolution. | [Gaussian GHZ survivor and route refutation](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_GAUSSIAN_GHZ_SURVIVOR_AND_DETERMINANT_SAFE_ROUTE_REFUTATION_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_GAUSSIAN_GHZ_SURVIVOR_AND_DETERMINANT_SAFE_ROUTE_REFUTATION_REVIEW_2026-08-24.md) |
| `GLD73` | Pull the `GLD72` survivor back to the literal `Delta_4` and transform one pinned `79`-coefficient preimage covariantly.  Its `52` nonzero transformed entries define one exact ten-vertex contracted edge array; all `945` perfect matchings give `Delta_4`.  For each of the six contracted vertices, the complete `17`-parameter first-response map has full/mixed ranks `(17,16)`, so its intersection with the diagonal target space is only `C Delta_4`; every edge-matrix completion over this same effective data fails the first-transverse GHZ identity.  This is **proved single-fibre grade-zero edge control and pointwise first-jet nonextension**, not exclusion of the other points in the affine `35`-dimensional coefficient fibre, maximum-root certification, a graph witness, or global resolution. | [Contracted edge control and first-transverse nonextension](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_GAUSSIAN_SURVIVOR_CONTRACTED_EDGE_CONTROL_AND_FIRST_TRANSVERSE_NONEXTENSION_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_GAUSSIAN_SURVIVOR_CONTRACTED_EDGE_CONTROL_AND_FIRST_TRANSVERSE_NONEXTENSION_REVIEW_2026-08-24.md) |
| `GLD74` | Parametrize the complete affine `35`-space of raw preimages of the literal `Delta_4`.  At `q_0`, the `Q` and twelve eta-residual cofactors have full/mixed rank `13`; quotienting them leaves a `65 x 3` affine matrix `Z` controlling the four root directions.  A three-dimensional diagonal response would force `rank Z<=1`.  Two sparse exact `Q(i)` Nullstellensatz identities and one inconsistent affine coordinate system exclude the exhaustive three-chart projective cover, including every response-rank drop.  Hence every raw preimage of the exact `GLD72` tensor fails first response in the fixed ten-vertex effective model.  This is a **proved full-raw-fibre fixed-model nonextension**, not exclusion of the whole survivor locus or every source presentation, maximum-root/no-fifth-root certification, a graph witness, or global resolution. | [Full coefficient-fibre first-response nonextension](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_GAUSSIAN_SURVIVOR_FULL_COEFFICIENT_FIBRE_FIRST_RESPONSE_NONEXTENSION_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_GAUSSIAN_SURVIVOR_FULL_COEFFICIENT_FIBRE_FIRST_RESPONSE_NONEXTENSION_REVIEW_2026-08-24.md) |
| `GLD75` | At the exact `GLD72` point, the identity component of the local-basis stabilizer of the complete fixed rank-`44` nuisance space is only the four factor-scalar torus, whose tensor orbit has dimension `1`.  The survivor tangent and the actual survivor germ both have dimension `5`.  On an explicit frame gauge, a bidirectional `Q(i)` ideal certificate proves that the full germ is smooth and equals its equal-leaf subgerm; after tensor scaling, four genuine survivor parameters remain.  Thus symmetry transport cannot globalize `GLD74`, and the minimal local parent response incidence must retain those four parameters plus the full raw fibre.  This is an **exact local survivor-germ theorem and route correction**, not a neighborhood or whole-locus first-response exclusion, a global component cover, source integration, or global resolution. | [Survivor-locus symmetry and local-germ reduction](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_SURVIVOR_LOCUS_SYMMETRY_AND_LOCAL_GERM_REDUCTION_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_SURVIVOR_LOCUS_SYMMETRY_AND_LOCAL_GERM_REDUCTION_REVIEW_2026-08-26.md) |
| `GLD76` | On the scale-fixed four-parameter `GLD75` germ, quotienting the complete legal `q_0` response by its thirteen fixed full-tensor columns gives an exact `68 x 4` root module.  The original `17 x 3` lift incidence is equivalent to `Hbar(F,t)X=Rbar(F)` with `X` only `4 x 3`, retaining all `35` raw directions and every rank drop.  Actual leaf-`S_3` response covariance decomposes the raw kernel as `8` trivial, `3` sign, and `24` standard dimensions, while the `GLD74` quotient is `20+3+42`.  Two sparse sign-type raw directions give exact rank-one points at infinity with ratios `(1,-1,1)` and `(1,1,-1)`, so the naive projective-properness lift of `GLD74` fails.  This is an **exact universal-module reduction and projective-boundary route correction**, not an affine lift, a survivor-open exclusion, an exhaustive boundary cover, source integration, or global resolution. | [Universal module and projective escape reduction](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_SURVIVOR_RESPONSE_UNIVERSAL_MODULE_AND_PROJECTIVE_ESCAPE_REDUCTION_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_SURVIVOR_RESPONSE_UNIVERSAL_MODULE_AND_PROJECTIVE_ESCAPE_REVIEW_2026-08-26.md) |
| `GLD77` | At the exact `GLD72` fibre, the three-dimensional sign-isotypic raw-kernel block compresses the homogeneous `GLD74` response to `W=[[u,iu+(1+i)v,-u],[v,(1-i)u-iv,-v],[w,-w,w]]`.  Its two-minor ideal is `((u+v)(u-iv),uw,vw)`, so its projective rank-one scheme is the reduced union of exactly three points with response ratios `(1,-1,1)`, `(1,1,-1)`, and `(1,-1,-1)`.  All three induced raw directions transform by the leaf sign character.  This is an **exact exhaustive sign-plane projective-boundary classification**, not a classification outside that plane, an affine response lift, a survivor-open exclusion, strict-transform closure, source integration, or global resolution. | [Sign-boundary trichotomy](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_SURVIVOR_RESPONSE_SIGN_BOUNDARY_TRICHOTOMY_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_SURVIVOR_RESPONSE_SIGN_BOUNDARY_TRICHOTOMY_REVIEW_2026-08-26.md) |
| `GLD78` | On the fixed-star, scale-fixed equal-leaf `GLD75` germ, transport the complete nuisance and legal response interface by the moving frame to literal `Delta_4`; only there does the signed matching partition make the moving `65 x 3` rank-one condition necessary.  Reynolds averaging reduces any raw solution in a `GLD77` first proportional-column chart to the moving eight-dimensional invariant kernel block.  The Gaussian quotient and invariant-basis minors are `8(1+i)/27` and `1008i`.  At all three sign points, exact selected augmented minors give rank jumps `8 -> 9` and define nonzero regular `delta_j(F,a,b)` continuations.  Hence no affine branch, including any higher-order formal arc with homogenizing coordinate not identically zero, enters through those three opens.  This is an **exact local all-order sign-boundary-chart nonextension**, not a fixed-coordinate three-column reduction, a full survivor-open exclusion, a cover outside the sign plane, a survivor-only exceptional polynomial, source integration, or global resolution. | [Invariant principal-open nonextension](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_SURVIVOR_RESPONSE_SIGN_BOUNDARY_INVARIANT_PRINCIPAL_OPEN_NONEXTENSION_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_SURVIVOR_RESPONSE_SIGN_BOUNDARY_INVARIANT_PRINCIPAL_OPEN_NONEXTENSION_REVIEW_2026-08-26.md) |
| `GLD79` | At the exact `GLD72` fibre, actual leaf-`S_3` covariance splits the `35` raw directions as `8` trivial, `3` sign, and `24` standard dimensions, and the proportionality equations preserve the direct sum.  Exact `K_0` minors prove rank `35`, so the first-column chart covers the whole projective boundary.  A two-stage trivial minor certificate and a Schur-compressed standard determinant certificate make those blocks empty for every slope pair; mixed isotypes cannot cancel.  The full projective rank-one boundary is therefore exactly the three reduced `GLD77` sign points.  This is an **exact fixed-Gaussian exhaustive boundary classification**, not a moving-survivor open theorem, an explicit survivor-only exceptional polynomial, source integration, or global resolution. | [Full projective-boundary classification](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_GAUSSIAN_SURVIVOR_FULL_PROJECTIVE_RESPONSE_BOUNDARY_CLASSIFICATION_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_GAUSSIAN_SURVIVOR_FULL_PROJECTIVE_RESPONSE_BOUNDARY_CLASSIFICATION_REVIEW_2026-08-26.md) |
| `GLD80` | Over an affine finite-type scale-fixed `GLD75` survivor neighborhood, conjugate each frame to literal `Delta_4` while transporting the complete interface, choose regular moving nuisance/kernel/quotient frames, and homogenize the resulting `35`-raw-parameter necessary rank-one incidence intrinsically in `B x P^35`.  Its `s`-saturated strict closure is proper over `B`.  `GLD74` empties the Gaussian affine fibre, `GLD79` leaves exactly three reduced boundary points, and the repaired moving `GLD78` determinants exclude every DVR trait entering through them using ratios of the full homogenized columns.  The strict closure therefore misses the Gaussian fibre; its closed proper image yields an element `delta` with `delta(F_0)!=0` whose principal open excludes every raw preimage's legal first response.  This is an **exact existential local survivor-open theorem**.  The polynomial `delta` is not computed in GLD80; `GLD82` subsequently supplies an explicit fraction-free principal subopen.  Other survivor components/gauges remain open.  `GLD81` proves the forward source bridge on the named maximum-root torus-star branch. | [Existential principal-open nonextension](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_SURVIVOR_EXISTENTIAL_PRINCIPAL_OPEN_FIRST_RESPONSE_NONEXTENSION_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_SURVIVOR_EXISTENTIAL_PRINCIPAL_OPEN_FIRST_RESPONSE_NONEXTENSION_REVIEW_2026-08-26.md) |
| `GLD81` | In an actual root-order-four, surplus-two ten-mode source, maximum-root zeroes force every surviving contracted matching to contain exactly one of the `1+24+54=79` physical outside-edge coefficients.  Varying `q_0` and partitioning the same matchings by its neighbor gives the complete `13+4=17`-coordinate legal response factorization (not a rank-`17` physical map).  A full GHZ identity therefore supplies an actual lift `L` with `b alpha=T(F)` and `D_q0(alpha)L=R(F)`; complete interface covariance transports it to the GLD80 incidence.  Hence the fully supported, rank-three, nonisotropic maximal-star source branch is empty whenever one induced scale-fixed survivor frame lies in `D(delta)`.  This is an **exact source-interface bridge and conditional source-branch exclusion**, not source integrability of arbitrary nuisance tensors, divisor or off-component coverage, a triangle/lower-rank/other-root theorem, or global resolution.  `GLD82` subsequently supplies an explicit fraction-free choice of principal subopen. | [Source-to-response incidence bridge](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_SOURCE_TO_SURVIVOR_RESPONSE_INCIDENCE_BRIDGE_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_SOURCE_TO_SURVIVOR_RESPONSE_INCIDENCE_BRIDGE_REVIEW_2026-08-26.md) |
| `GLD82` | On the scale-fixed equal-leaf survivor chart, the fixed rank-`44` nuisance pivot gives a polynomial raw section and the invariant raw kernel has a fixed rank-eight basis.  An exact universal-port audit proves individual-root leaf-`S_3` covariance, so Reynolds averaging maps every full affine rank-one response solution to an invariant one.  Adjugate tensor transport and a named thirteen-row quotient pivot give denominator-free polynomial response columns in `P^8`.  Forty-five named intrinsic minors form a `45 x 45` quadratic coefficient matrix; its moving arithmetic circuit specializes entry-for-entry to the independently audited Gaussian matrix, whose determinant is nonzero.  Thus `Delta_82=Omega gamma_num det(M_ff)` defines an **explicit exact principal survivor-open exclusion** containing `GLD72`, and `GLD81` transfers it to the named physical maximal-star source branch.  The determinant, quotient, and frame divisors, other components/gauges and source branches, rank/support boundaries, triangles, other root profiles, and global resolution remain open. | [Fraction-free quadratic principal-open nonextension](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_SURVIVOR_INVARIANT_QUADRATIC_MACAULAY_PRINCIPAL_OPEN_NONEXTENSION_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_SURVIVOR_INVARIANT_QUADRATIC_MACAULAY_PRINCIPAL_OPEN_NONEXTENSION_REVIEW_2026-08-26.md) |
| `GLD83` | On the globally defined scale-fixed equal-leaf subincidence `B` in the displayed frame gauge, without inverting `gamma_num`, replace the selected thirteen-row quotient by the bordered determinants `det[C_F|w_c|w_d]_S`.  The same forty-five descriptors give a polynomial `45 x 45` matrix `M_Pl` with `M_ff=gamma_num M_Pl`, so `Delta_82=gamma_num^46 Delta_83` for `Delta_83=Omega det(M_Pl)`.  Nonvanishing of `det(M_Pl)` itself forces `rank C_F=13`, making Reynolds quotient compression legal without selecting or dividing by `gamma_num`.  Taking every coordinate of `wedge^13(C_F) wedge w_c wedge w_d` gives the intrinsic coefficient map `A_Pl`; `I_Pl=Fitt_0(coker A_Pl)` defines an exact finite **full quadratic Fitting-open exclusion** `D(Omega I_Pl)` containing `D(Delta_83)`.  `GLD81` transfers the selected open only to named physical sources whose induced normalized frame lies in this equal-leaf gauge.  This removes the old quotient pivot and single selected determinant as intrinsic residuals.  `V(I_Pl)`, frame/gauge and other survivor components, remaining source branches, rank/support boundaries, triangles, other roots, and global resolution remain open. | [Bordered-Pluecker Fitting-open nonextension](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_SURVIVOR_BORDERED_PLUCKER_FITTING_OPEN_NONEXTENSION_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_SURVIVOR_BORDERED_PLUCKER_FITTING_OPEN_NONEXTENSION_REVIEW_2026-08-26.md) |
| `GLD84` | After imposing `x_8=0`, the ten exact equal-leaf survivor generators have the global center-linear form `g=A(z)c+q(z)` with eight center and six leaf variables.  The `10 x 8` matrix `A` gives an exhaustive locally closed decomposition into `45` rank-eight Schur charts, `960` exact rank-seven charts, and the named closed rank-at-most-six branch `V(I_7(A))`.  Rank-eight charts reduce the survivor base to six variables and two residual equations; rank-seven charts reduce it to six leaf variables, three compatibility equations, and one free center-kernel coordinate after imposing all `8 x 8` minors.  At `GLD72`, `rank A=7` and a named seven-minor is `12`, but a named eight-minor has derivative `48i` along the smooth survivor tangent `tau_14`; hence rank eight occurs on the same local component.  Pulling `V(I_Pl) intersect D(Omega)` through these Schur models is an **exact finite determinantal parameter reduction**, not a computation or exclusion of the pulled-back Fitting ideals.  Rank at most six, other gauges/components and source branches, rank/support boundaries, triangles, other roots, and global resolution remain open. | [Centre-rank determinantal chart reduction](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_CENTER_RANK_DETERMINANTAL_CHART_REDUCTION_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_CENTER_RANK_DETERMINANTAL_CHART_REDUCTION_REVIEW_2026-08-27.md) |
| `GLD85` | On the named rank-eight Schur chart `R_8=(0,1,2,3,4,5,6,7)`, the exact point `z=(1,0,0,0,-2/3,0)` with the pinned eight center shifts satisfies both Schur residual equations, has `mu_R=-140/9-20i/9 != 0`, `D(Omega)`, and `rank(C_F)=13`.  The full intrinsic quotient map has shape `45 x 6240`; one pinned `45 x 45` maximal minor reduces to nonzero residues `9639769+249939722i` modulo `1000000007` and `1610829+5232695i` modulo `10000019`, with all `6240` exact denominator slots checked as units at both primes.  Therefore the pullback of `I_Pl` is nonzero and `V(I_Pl)` is a proper closed subset of this chart.  The old selected `M_Pl` is exactly zero at the same point, so this is a full-intrinsic proper-open result, not a selected-minor result.  This does not make the residual empty or excluded; other rank-eight charts, rank-seven/lower branches, components, gauges, source branches, and global resolution remain open. | [Rank-eight full intrinsic Fitting nonzero point](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_RANK_EIGHT_FULL_INTRINSIC_FITTING_NONZERO_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_RANK_EIGHT_FULL_INTRINSIC_FITTING_NONZERO_REVIEW_2026-08-27.md) |
| `GLD86` | On the complete scale-fixed equal-leaf base, the exact `GLD75` bidirectional certificate gives `B=0 iff M(G)C=0` for the fixed `37 x 9` `GLD71` syndrome map.  With `C_8=1`, the selected minor on rows `(0,1,17,19,31,32,33)` and columns `(2,3,4,5,6,7,8)` factors as `432(p-q)^2(p-s)^2(q-s)^2(pq+ps+qs-p-q-s)^2`, where `s=1+i+r`.  Off the four named divisors, column replacement forces `rank M(G)[:,0:8]>=7`; differentiating the certificate on `B` gives `rank A>=7`.  Therefore `B intersect V(I_7(A))` is contained in the union of those four divisors, and the same containment holds after intersecting `D(Omega)`.  GLD86 itself computes no divisor-specific Fitting exclusion; GLD87 now excludes H1/H2/H3 on the determinant-safe retained open, leaving H4 and all other divisor, component/gauge, source, and global obligations open. | [Rank-at-most-six syndrome boundary containment](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_RANK_AT_MOST_SIX_SYNDROME_BOUNDARY_CONTAINMENT_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_RANK_AT_MOST_SIX_SYNDROME_BOUNDARY_CONTAINMENT_REVIEW_2026-08-27.md) |
| `GLD87` | On the same complete scale-fixed equal-leaf chart, every rank-at-most-six incidence on `H_1=p-q`, `H_2=p-s`, or `H_3=q-s` has singular actual center `C`.  For `H_1`, the exact 11-row GLD71 transform has 37 nonzero base 4-minors; after dividing by `p-s`, their Groebner basis leaves only `p=1-s`, `s^2-s+1=0` away from `det(G)=0`.  An exact exceptional 7-minor forces `c=s/(s+1)`, an exact 6-minor proves rank six, and all three block kernels are one common line, so `det(C)=0`.  Exact leaf-column covariance transfers this to H2/H3.  Thus the GLD86 four-divisor residual sharpens on `D(Omega)` (where `det(C)det(G)!=0`) to `H_4` only.  GLD88 now excludes one nonempty named principal open in H4, and GLD89 removes its full P and d0 boundary; the remaining H4 boundaries, the GLD83 pulled-back Fitting ideal, other charts/components/source branches, and global resolution remain open. | [Three-collision-divisor determinant safety](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_THREE_COLLISION_DIVISOR_DETERMINANT_SAFETY_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_THREE_COLLISION_DIVISOR_DETERMINANT_SAFETY_REVIEW_2026-08-27.md) |
| `GLD88` | On `H_4` with `p+q-1!=0`, select the exact syndrome six-pivot on rows `(0,1,2,17,19,32)` and columns `(0,1,3,4,6,7)`.  Two bordered Schur residuals are linear in the free leaf shifts `b,c`; their coefficient determinant is the explicit product `-6(p-q)(p+q-1)(p^2-p+1)(p^2+2pq-2p-q)(2pq-p+q^2-2q)(2pq^2-2pq-p-q^2-2q+2)`.  On its nonvanishing open they force a rational three-parameter family.  All 111 block-kernel identities and a nonzero 176-term six-minor show rank exactly six with complete common-row kernel, hence every compatible center is singular and this low-rank principal open misses `D(Omega)`.  GLD89 now closes the full P=0 and d0=0 boundary; the L1/L2/e six-pivot boundaries, lower ranks there, the pulled-back Fitting ideal, and global resolution remain open. | [H4 rank-six principal-open exclusion](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_GENERIC_RANK_SIX_COMMON_ROW_KERNEL_EXCLUSION_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_GENERIC_RANK_SIX_COMMON_ROW_KERNEL_EXCLUSION_REVIEW_2026-08-27.md) |
| `GLD89` | On the exact characteristic-zero H4 equal-leaf chart, the full `P=p^2-p+1` divisor is disjoint from `B intersect V(I_7(A)) intersect D(Omega)`.  Two reduced six-minors, bordered residuals, the alternate-pivot branch, and exact `q=0,1,-1` seven-minor cases either give rank above six or a complete common-row kernel and singular center.  The `d0=p+q-1=0` overlap is handled in a separate chart: four exact syndrome rows force proportional center rows unless the point is on the already excluded GLD87 H2/H3 collision locus.  This is a P/d0 divisor exclusion only; GLD90 supplies the complementary Q6-open theorem, while the remaining H4 boundaries, Fitting pullback, and global problem stay open. | [P divisor and d0-overlap determinant safety](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_P_DIVISOR_AND_D0_OVERLAP_DETERMINANT_SAFETY_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_P_DIVISOR_AND_D0_OVERLAP_DETERMINANT_SAFETY_REVIEW_2026-08-27.md) |
| `GLD90` | Put `Delta=(p-q)(p+q-1)P L1 L2 e`.  On the complete H4 equal-leaf chart, `B intersect V(I_7(A)) intersect D(Omega Delta Q6)` is empty.  The old and alternate raw pivots factor as `-6(p-q)^2 X_j Q6`.  If both `X_j` vanish away from `T=0`, two auxiliary pivots and exact bordered resultants force one residual curve; modulo that curve the leaf family is exactly GLD88's complete common-row-kernel family.  If both auxiliary pivots vanish, four exact parameter corners remain and coprime seven-minors exclude them.  On `T=0`, `q=(p-2)/(2p-1)`, `Q6=8P^4/(2p-1)^4`, and the two pivot brackets differ by `4P`, so one pivot is always available on `D(Delta)`.  Thus every positive-dimensional retained rank-six fibre has singular center.  GLD93 subsequently closes `L1/L2=0`; `Q6=0`, `e=0`, the GLD83 Fitting pullback, other branches, and global resolution remain open. | [H4 Q6-open low-rank exclusion](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_OPEN_LOW_RANK_EXCLUSION_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_OPEN_LOW_RANK_EXCLUSION_REVIEW_2026-08-27.md) |
| `GLD93` | On `H4 intersect D(Omega (p-q)d0P)`, direct L1 and L2 parameterizations make `Q6` nonzero automatically.  The two raw six-pivots and their bordered seven-minors either give an immediate rank-seven certificate or force a solved double-pivot slice with an auxiliary rank-seven minor.  The exceptional L1 points `(2,0),(-1,1)` and L2 points `(0,2),(1,-1)` are closed by direct seven-minor witnesses, including coprime witness pairs when the remaining bracket vanishes.  The L2 calculation does not assume naive p/q carrier symmetry.  Thus the complete named `L1=0` and `L2=0` boundaries are excluded from the rank-at-most-six branch on this open.  `Q6=0`, the remaining `e=0` boundary, the GLD83 Fitting pullback, other branches, and global resolution remain open. | [H4 L1/L2 rank-seven exclusion](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_L1_L2_RANK_SEVEN_EXCLUSION_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_L1_L2_RANK_SEVEN_EXCLUSION_REVIEW_2026-08-27.md) |
| `GLD92` | On the exact GLD88 three-parameter H4 family, the two fixed-column six-minors with rows `(0,1,2,17,25,28)` and `(0,1,2,17,25,31)` have numerators `(p-q)^3F28` and `(p+q-1)(p-q)^3F31` over `P^2e^2`.  `Q6` is irreducible; neither numerator is a Q6 multiple, and `Res_a(F28,F31)` is coprime to Q6.  An exact coefficient-ideal certificate removes vertical a-lines on `D(Delta)`, so `V(Q6,F28,F31)` is a finite retained residual and the union `D(F28) union D(F31)` is excluded by rank-six common-row-kernel singularity.  This is not full Q6 closure: the finite residual, arbitrary H4 Q6 points outside GLD88, `L1/L2/e`, Fitting, other branches, and global resolution remain open. | [H4 Q6 boundary dense minor exclusion](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_BOUNDARY_DENSE_MINOR_EXCLUSION_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_BOUNDARY_DENSE_MINOR_EXCLUSION_REVIEW_2026-08-27.md) |
| `GLD91` | On the same named `R_8` chart, restrict to the exact two-leaf slice `x9=1, x10=x11=x12=0, x13=t, x14=u, x8=0`.  Correcting an earlier omitted-Gaussian-offset exploratory frame calculation, exact `Q(i)` Groebner/resultant data give a degree-10 elimination and degree-11 resultant: six linear fibres plus a squarefree degree-five `Q5` component.  The five `Q5` points and two linear fibres have `mu_R=0`; three further linear fibres have nonzero `mu_R` but zero centre-frame determinant; the sole Schur/frame-open fibre is `(t,u)=(-2/3,0)`, the GLD85 point.  Its audited full intrinsic rank-45 minor therefore gives `V(I_Pl) ∩ D(mu_R Omega)` empty on this two-leaf slice.  This is a finite-slice characteristic-zero exclusion, not unitness of the full six-leaf pullback, a cover of other charts/ranks/components, or global resolution. | [Rank-eight two-leaf slice Fitting exclusion](../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_RANK_EIGHT_TWO_LEAF_SLICE_FITTING_EXCLUSION_THEOREM.md), [hostile review](audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_RANK_EIGHT_TWO_LEAF_SLICE_FITTING_EXCLUSION_REVIEW_2026-08-27.md) |
| `GLD19` | On the literal all-seven response-map-zero stratum, the six pair maps make every raw `B_e,K_e` block diagonal and the four-port map makes both `C(B)` and `X(B,K)` pure, for arbitrary residual scalar `h`.  Twelve ordered `2+2` rows on each complement have an exhaustive support classification.  Five fixed scalar rows per complement detect any two three-full selected pair blocks, so every projective pair package lies on the intersection of all three complementary support divisors.  The common physical shore factorization strengthens this: one three-full selected edge forces the opposite raw pair response `B_f=K_f=0`, hence three-full edges form an intersecting `K_4` family.  This is a **proved response-map-zero support classification, five-row detector, and opposite-annihilation boundary**, not proof that `R_S=0`, a selector construction, exclusion of the sparse-support branch, witness integration, or permanent extraction. | [Response-map-zero support classification](../claims/arbitrary-order/FIXED_Q_FULLY_RESPONSE_INVISIBLE_TWELVE_ROW_COMPLEMENTARY_SUPPORT_DIVISOR_THEOREM.md), [hostile review](audits/FIXED_Q_RESPONSE_MAP_ZERO_COMPLEMENTARY_SUPPORT_REVIEW_2026-08-17.md) |
| `GLD20` | On the `GLD19` map-zero locus, the six diagonal corrected blocks come from four common two-dimensional shores.  Globally at most two corrected colours occur.  A one-colour support graph is any nonempty labelled four-vertex graph except `P_4`; a two-colour support is exactly two clique graphs.  There are `517` corrected-channel support types and `467715` compatible labelled raw support patterns.  The edges whose raw `B/K` support union is all three colours form one of the five intersecting `K_4` families; each forces its opposite raw pair response to zero and, on a full witness, forces that opposite `GLD15` pure target quotient rank to zero.  Maximal stars and triangles therefore reduce to three simultaneous complementary pure-absorption targets.  This is a **proved global physical-channel atlas and full-witness pure-absorption reduction**, not exclusion of the `254995`-pattern `F=empty` cell, the star/triangle cells, legal operator supply, witness integration, or permanent extraction. | [Global map-zero physical support](../claims/arbitrary-order/FIXED_Q_RESPONSE_MAP_ZERO_GLOBAL_PHYSICAL_CHANNEL_SUPPORT_AND_COMPLEMENTARY_PURE_ABSORPTION_THEOREM.md), [hostile review](audits/FIXED_Q_RESPONSE_MAP_ZERO_GLOBAL_PHYSICAL_CHANNEL_SUPPORT_REVIEW_2026-08-18.md) |
| `GLD21` | In the exactly-two-corrected-colour part of the `GLD20` map-zero atlas, assume one corrected support clique is `K_4`.  The missing colour has zero shores at the fixed contraction and every direct block is confined to the complete colour.  This is an exhaustive `F=empty` subcell of `63` corrected types and `1347` labelled raw masks.  The complete mixed GHZ coefficient at the all-missing port word leaves only `H_Q=h`, so every hypothetical witness has `h!=0` and a prescribed pure nonzero `G_U(a^4)` root slice; the full `h=0` divisor is excluded.  In the dense `K_4/K_4` cell, all direct blocks vanish and twelve paired `2+1+1` packages force desired companion columns into explicit nine-column nuisance images.  This is a **proved characteristic-zero subcell exclusion and companion normal form**, not exclusion at `h!=0`, a universally nonzero augmented minor, a legal `GLD15` row, same-graph root-companion integration, or permanent extraction. | [Dead-colour h-gate and dense companion absorption](../claims/arbitrary-order/FIXED_Q_RESPONSE_MAP_ZERO_DEAD_COLOUR_H_GATE_AND_DENSE_COMPANION_ABSORPTION_THEOREM.md), [hostile review](audits/FIXED_Q_RESPONSE_MAP_ZERO_DEAD_COLOUR_H_GATE_AND_DENSE_COMPANION_ABSORPTION_REVIEW_2026-08-18.md) |
| `GLD22` | Inside the `GLD21` dense `K_4/K_4`, `h!=0` residue, suppose all three root-to-port colour slices use one common private bijection and every private edge is colour diagonal with nonzero entries.  Hamming-one words then fix each active one-`Q` companion to `-h` times its private factor.  The opposite repeated-colour `2+1+1` package forces every active diagonal root--root entry to vanish, after which the matching mixed word is `h-3h=-2h` times a nonzero private product.  Thus this positive-dimensional common-private chart is empty on the witness locus: **proved same-graph root-companion integrability subcell exclusion**.  By itself it does not exclude colour-dependent private permutations, nonprivate cross arrays, proper-secondary cells, or any weighted-permanent branch; `GLD23` closes the first of those boundaries. | [Dense private-cross-matching exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_PRIVATE_CROSS_MATCHING_ROOT_COMPANION_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_PRIVATE_CROSS_MATCHING_ROOT_COMPANION_EXCLUSION_REVIEW_2026-08-19.md) |
| `GLD23` | In the same dense `K_4/K_4`, `h!=0` residue, allow an arbitrary private colour-diagonal root-to-port bijection in each of the three colours.  Dense-shore orthogonality and invertible diagonal coordinate changes normalize the dead permutation to the identity, the active shores to `(1,1)` and `(1,-1)`, and all nonzero scalars to one.  The two active permutations give `576` ordered pairs and exactly `28` simultaneous-conjugacy/active-swap orbits.  The complete ten-vertex coefficient system leaves all `24` root--residual entries, `54` root--root entries, and `3` pure target scalars free, yet every orbit has an exact `5`--`20`-row rational contradiction certificate.  Thus the **entire private-permutation chart is proved empty**, not the nonprivate dense cell, proper-secondary cells, or any weighted-permanent branch. | [Dense colour-dependent private-permutation exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_COLOUR_DEPENDENT_PRIVATE_PERMUTATION_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_COLOUR_DEPENDENT_PRIVATE_PERMUTATION_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD24` | In the canonical `GLD23` dense shore gauge, keep two root-to-port colour slices equal to `I_4` and take the third to be `I_4+E_(0,1)+tE_(1,0)` with `t!=0`.  This is genuinely nonprivate and supports two root--port matchings.  An exact polynomial left combination of eighteen complete coefficient rows cancels all `81` root-side and pure-target variables and leaves `-4t(t+1)`; a separate ten-row rational certificate gives `0=1` at `t=-1`.  Thus the **balanced single-switch chart is proved empty**, not a general two-amplitude switch, a larger nonprivate array, proper-secondary cells, or any weighted-permanent branch. | [Dense balanced single-switch exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_BALANCED_SINGLE_SWITCH_CROSS_ARRAY_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_BALANCED_SINGLE_SWITCH_CROSS_ARRAY_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD25` | In the same canonical dense shore gauge, keep two root-to-port colour slices equal to `I_4` and take the third to be `I_4+uE_(0,1)+vE_(1,0)` with independent `u,v!=0`.  An eighteen-row polynomial relation leaves `2uv(u+1)(uv+1)(uv-u-v-1)`.  Separate exact relations on its three exceptional divisors, a seven-row point certificate, and a thirteen-row quadratic-quotient certificate close the entire vanishing locus.  Thus the **full two-amplitude single-switch chart is proved empty**, strictly extending `GLD24`; larger-support nonprivate arrays, root-colour-changing blocks, proper-secondary cells, and every weighted-permanent branch remain open. | [Dense two-amplitude single-switch exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_AMPLITUDE_SINGLE_SWITCH_CROSS_ARRAY_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_AMPLITUDE_SINGLE_SWITCH_CROSS_ARRAY_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD26` | Add one directed support edge and take the active slice to be `I_4+uE_(0,1)+vE_(1,0)+wE_(0,2)` with `u,v,w!=0`.  A sixteen-row polynomial relation cancels all `81` free coefficients and leaves `uvw(uv-1)(uv+1)^2(uv-u-v-1)(uv+vw+w+1)^2`.  Thus the **complement of four explicit divisors is proved empty**, a generic/open-subset larger-support exclusion.  The four divisors, reverse spur, further support entries, root-colour-changing blocks, proper-secondary cells, and every weighted-permanent branch remain open. | [Dense directed-spur generic exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_DIRECTED_SPUR_GENERIC_CROSS_ARRAY_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_DIRECTED_SPUR_GENERIC_CROSS_ARRAY_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD27` | On the `GLD26` exceptional divisor `uv=-1`, a twelve-row relation leaves `2uw(u-1)(u^2+2u-1)`.  The `u=1,v=-1` line is closed by a `2w(w+1)(w+2)` detector plus exact cores at `w=-1,-2`; the quadratic family is closed in `K[u,w]/(u^2+2u-1)` by a certificate leaving `4w`.  Thus the **entire `uv=-1` divisor is proved empty**.  The other three `GLD26` divisors and all broader boundaries remain open. | [Directed-spur uv=-1 divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_DIRECTED_SPUR_UV_MINUS_ONE_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_DIRECTED_SPUR_UV_MINUS_ONE_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD28` | On the `GLD26` exceptional divisor `uv=1`, a sixteen-row relation leaves `-4u(u+w)(w+2)(u+w+1)(uw+2u+w)`.  Four exact curve relations reduce its vanishing locus to four rational points and one shared `u^2+1=0` family; exact point cores and a twelve-row quotient certificate close all residual cases.  Thus the **entire `uv=1` divisor is proved empty**.  The other two `GLD26` divisors and all broader boundaries remain open. | [Directed-spur uv=1 divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_DIRECTED_SPUR_UV_ONE_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_DIRECTED_SPUR_UV_ONE_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD29` | On the `GLD26` exceptional divisor `uv-u-v-1=0`, an eighteen-row relation leaves `2u(u+1)^2(u+w)(w+2)(u+w+1)q_1q_2`.  Exact curve detectors reduce its five components to the `GLD28` `uv=1` locus and one `q_1` cylinder.  A fourteen-row quotient relation leaves `2w(w+2)(3uw+u+7w+3)`; exact cores close its `w=-2` and `w=-u` fibres.  Thus the **entire `uv-u-v-1=0` divisor is proved empty**.  `GLD30` subsequently closes the one divisor then remaining. | [Directed-spur uv-u-v-1 divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_DIRECTED_SPUR_UV_MINUS_U_MINUS_V_MINUS_ONE_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_DIRECTED_SPUR_UV_MINUS_U_MINUS_V_MINUS_ONE_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD30` | On the final `GLD26` exceptional divisor `uv+vw+w+1=0`, the `v=-1` fibre lies in `GLD27`; on `v!= -1`, a sixteen-row relation leaves `-uv(u-1)(u+v)(uv+1)(uv-2v-1)`.  Three curve detectors place every residual in `GLD27`, `GLD28`, `GLD29`, or an excluded chart boundary.  Thus the **entire final divisor and the complete nonzero directed-spur chart are proved empty**.  With the `GLD25` `w=0` theorem, the coordinate family is empty for all `w`.  Reverse spurs, larger supports, and all broader boundaries remain open. | [Directed-spur uv+vw+w+1 divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_DIRECTED_SPUR_UV_PLUS_VW_PLUS_W_PLUS_ONE_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_DIRECTED_SPUR_UV_PLUS_VW_PLUS_W_PLUS_ONE_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD31` | Add the reverse edge `zE_(2,0)` to the completed `GLD30` family, with `u,v,w,z!=0`.  A sixteen-row polynomial relation cancels all `81` free coefficients and leaves `2uv wz(uv+1)(uv+wz-1)(uv+wz+1)(uv+vw+w+1)p`.  Thus the **complement of five explicit hypersurfaces is proved empty**, a generic/open-subset four-parameter exclusion.  The five divisors, further support entries, root-colour-changing blocks, proper-secondary cells, and every weighted-permanent branch remain open; the `z=0` boundary is `GLD30`. | [Dense bidirected-spur generic exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_BIDIRECTED_SPUR_GENERIC_CROSS_ARRAY_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_BIDIRECTED_SPUR_GENERIC_CROSS_ARRAY_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD32` | On the `GLD31` divisor `uv=-1`, the legal parametrization `v=-1/u` and a fourteen-row polynomial-cleared relation leave `-2uwz^2(u-1)(z-1)(z+1)(wz-2)`.  Thus the **complement of four explicit residual surfaces is proved empty inside this divisor**.  The four surfaces and the entire divisor remain open pointwise; the `z=0` boundary lies in `GLD27`. | [Bidirected-spur uv=-1 generic exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_GENERIC_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_GENERIC_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD33` | On the `GLD32` residual `u=1` surface, hence `v=-1`, two exact detectors reduce all nonzero `(w,z)` to `wz=2` or `(w,z)=(1,-1)`.  A polynomial-cleared curve certificate leaves `24` and a point certificate leaves `6`.  Thus the **entire `u=1` surface is proved empty**.  Three other `GLD32` residual surfaces remain open. | [Bidirected-spur u=1 surface exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_U_ONE_SURFACE_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_U_ONE_SURFACE_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD34` | On the `GLD32` residual `z=1` surface, hence `v=-1/u`, the two complete rows `(1202;0212)` and `(2212;2212)` give the exact relation `0=w`.  A disjoint two-row relation gives `0=-u^(-1)`.  Since `u,w!=0`, the **entire `z=1` surface is proved empty**.  Exactly `z=-1` and `wz=2` remain inside this divisor. | [Bidirected-spur z=1 surface exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_Z_ONE_SURFACE_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_Z_ONE_SURFACE_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD35` | On the `GLD32` residual `z=-1` surface, hence `v=-1/u`, the two complete rows `(0100;0010)` and `(2212;2212)` give `0=-w/u`.  A disjoint two-row relation gives `0=-u^(-1)`.  Since `u,w!=0`, the **entire `z=-1` surface is proved empty**.  Only `wz=2` remains inside this divisor. | [Bidirected-spur z=-1 surface exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_Z_MINUS_ONE_SURFACE_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_Z_MINUS_ONE_SURFACE_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD36` | On the final `GLD32` residual `wz=2` surface, hence `w=2/z` and `v=-1/u`, the two complete rows `(0100;1000)` and `(1222;1222)` give `0=-u^(-1)`.  Thus the **entire `wz=2` surface is proved empty**.  Together with GLD32--GLD35, this pointwise completes the nonzero `uv=-1` divisor; the other four GLD31 divisors remain open. | [Bidirected-spur wz=2 surface exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_WZ_TWO_SURFACE_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_WZ_TWO_SURFACE_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD37` | On the `GLD31` divisor `uv+wz-1=0`, the legal parametrization `v=(1-wz)/u` and two complete rows give `0=v`.  A disjoint two-row relation gives `0=wv`.  Since `u,v,w,z!=0`, the **entire divisor is proved empty**.  Exactly three GLD31 divisors remain open. | [Bidirected-spur uv+wz-1 divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_PLUS_WZ_MINUS_ONE_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_PLUS_WZ_MINUS_ONE_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD38` | On the `GLD31` divisor `uv+wz+1=0`, the legal parametrization `v=-(1+wz)/u` and two complete rows give `0=v`.  A disjoint two-row relation gives `0=wv`.  Since `u,v,w,z!=0`, the **entire divisor is proved empty**.  Exactly two GLD31 divisors remain open. | [Bidirected-spur uv+wz+1 divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_PLUS_WZ_PLUS_ONE_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_PLUS_WZ_PLUS_ONE_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD39` | Re-expand over `Z[u,v,w,z]` the complete rows `(1202;0212)` and `(2212;2212)`, first used after specialization in GLD34.  They are exactly `-wP_0+wP_1=0` and `-P_0+P_1=-1`, so their difference gives `0=w` without any divisor equation or denominator.  Since `w!=0` on the original GLD31 chart, the **entire nonzero bidirected-spur chart is proved empty**.  This closes all five exceptional divisors and subsumes GLD31--GLD38 on this chart; broader arrays, support-drop boundaries, and every permanent bridge remain open. | [Dense bidirected-spur nonzero-chart completion](../claims/arbitrary-order/FIXED_Q_DENSE_BIDIRECTED_SPUR_NONZERO_CHART_COMPLETION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_BIDIRECTED_SPUR_NONZERO_CHART_COMPLETION_REVIEW_2026-08-20.md) |
| `GLD40` | Allow arbitrary `u,v,w,z`, including every support drop, in the four-edge bidirected-spur coordinate family.  Global two-row relations give `0=u` and `0=w`; on `u=w=0`, two more give `0=v` and `0=z`.  The all-zero endpoint is the proved GLD23 identity private-permutation chart.  Thus all `16` support masks are covered and the **entire affine four-parameter family is proved empty**, subsuming GLD24--GLD39 on their coordinate subcharts.  Broader cross arrays, further support entries, root-colour-changing blocks, proper-secondary cells, and every permanent bridge remain open. | [Dense bidirected-spur affine-chart completion](../claims/arbitrary-order/FIXED_Q_DENSE_BIDIRECTED_SPUR_AFFINE_CHART_COMPLETION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_BIDIRECTED_SPUR_AFFINE_CHART_COMPLETION_REVIEW_2026-08-20.md) |
| `GLD41` | Keep two colour slices equal to `I_4` and allow the third to be an arbitrary unit-diagonal `4`-by-`4` matrix, with all twelve off-diagonal amplitudes present simultaneously.  For each ordered entry `a_(ij)`, a permuted pair of complete rows is exactly `-a_(ij)P_0+a_(ij)P_1=0` and `-P_0+P_1=-1`, hence leaves `a_(ij)` without division or specialization.  Any nonzero entry is therefore impossible; GLD23 excludes the all-zero origin.  Thus all `4096` support masks are covered and the **complete 12-parameter single-active-slice affine cell is proved empty**, subsuming GLD24--GLD40.  Multiple simultaneously nonprivate slices, root-colour-changing blocks, proper-secondary cells, and every permanent bridge remain open. | [Single-active-slice affine cross-array completion](../claims/arbitrary-order/FIXED_Q_DENSE_SINGLE_ACTIVE_SLICE_AFFINE_CROSS_ARRAY_COMPLETION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_SINGLE_ACTIVE_SLICE_AFFINE_CROSS_ARRAY_COMPLETION_REVIEW_2026-08-20.md) |
| `GLD42` | Take `A^0=I_4+uE_(0,2)`, `A^1=I_4+vE_(2,0)`, and `A^2=I_4`, with arbitrary amplitudes.  Three complete rows force the reciprocal divisor `uv-u-v=0`.  On its nonzero part, a thirteen-row function-field certificate leaves `1` away from `u=-1`; an eleven-row integer certificate leaves `2` at the forced point `(-1,1/2)`.  GLD41 covers the support-drop faces.  Thus the **entire reciprocal two-active-slice affine chart is proved empty**, the first chart in this line with two slices simultaneously nonprivate.  Additional two-slice support, general cross arrays, proper-secondary cells, and every permanent bridge remain open. | [Two-active reciprocal-spike affine exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_RECIPROCAL_SPIKE_AFFINE_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_RECIPROCAL_SPIKE_AFFINE_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD43` | Allow all twenty-four off-diagonal amplitudes across two active unit-diagonal colour slices, with the third slice equal to `I_4`.  For every ordered pair, three complete equations over the full simultaneous ring force `x_(ij)y_(ji)-x_(ij)-y_(ji)=0`.  Hence the two supports are exact transposes and each nonzero reciprocal pair lies on one rational curve.  GLD41 and GLD42 exclude support size zero and one.  Thus the **full two-active-slice cell is reduced to 4083 transpose-matched support patterns with at least two reciprocal pairs**.  This is a necessary-locus reduction, not exclusion or existence of those residual patterns; proper-secondary cells and every permanent bridge remain open. | [Two-active reciprocal-support divisor reduction](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_RECIPROCAL_SUPPORT_DIVISOR_REDUCTION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_RECIPROCAL_SUPPORT_DIVISOR_REDUCTION_REVIEW_2026-08-20.md) |
| `GLD44` | The `66` support masks with exactly two reciprocal pairs split into five position-relabelling orbits: reverse, same tail, same head, directed chain, and disjoint, with counts `6,12,12,24,12`.  After the GLD43 reciprocal parametrization, exact `12`--`17`-row function-field certificates leave `1` on the complement of five explicit orbitwise divisor unions.  Thus the **generic part of every two-pair orbit is proved empty**.  The exceptional divisors remain open pointwise, as do three-or-more-pair supports, proper-secondary cells, and every permanent bridge. | [Two-reciprocal-pair generic exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_TWO_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_TWO_RECIPROCAL_PAIR_GENERIC_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD45` | On the GLD44 same-tail exceptional divisor `u=-1`, the GLD43 reciprocal amplitude is `1/2`.  A twelve-row exact function-field certificate cancels all `81` variables and leaves `1`; its denominator lcm is `2w(w-1)`, whose roots are already forbidden by active reciprocal support.  Thus the **entire same-tail two-pair orbit is proved pointwise empty**, covering all `12` labelled masks.  Reverse, same-head, chain, and disjoint exceptional divisors remain open, as do larger supports and every permanent bridge. | [Same-tail exceptional-divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_SAME_TAIL_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_SAME_TAIL_EXCEPTIONAL_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD46` | On the GLD44 disjoint component `u=-1`, an eleven-row exact function-field certificate leaves `1` with denominator lcm `2w(w-1)`, whose roots are forbidden by active reciprocal support.  The position permutation `(0 1)(2 3)` exchanges the two disjoint directed pairs and covers the component `w=-1`.  Thus the **entire disjoint two-pair orbit is proved pointwise empty**, covering all `12` labelled masks.  Reverse, same-head, and chain exceptional divisors remain open, as do larger supports and every permanent bridge. | [Disjoint exceptional-divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_DISJOINT_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_DISJOINT_EXCEPTIONAL_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD47` | The GLD44 reverse exceptional union has components `u=-1`, `w=-1`, and `uw=-1`.  A seventeen-row exact curve certificate closes `u=-1`; position swap `(0 2)` closes `w=-1`; and a fifteen-row exact curve certificate closes `uw=-1`.  Both multiplier denominator loci are disjoint from the legal active reciprocal domain.  Thus the **entire reverse two-pair orbit is proved pointwise empty**, covering all `6` labelled masks.  Same-head and chain exceptional divisors remain open, as do larger supports and every permanent bridge. | [Reverse exceptional-divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_REVERSE_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_REVERSE_EXCEPTIONAL_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD48` | Applying the GLD44 same-head certificate in both pair orders reduces its full exceptional union to `u+w+1=0` and `(-1,-1)`.  An eleven-row exact curve certificate has denominator lcm `2u^2(u+1)^2`, disjoint from the legal active domain, and a fourteen-row integer certificate closes the point.  Thus the **entire same-head two-pair orbit is proved pointwise empty**, covering all `12` labelled masks.  Only chain exceptional divisors remain among minimal two-pair supports; larger supports and every permanent bridge remain open. | [Same-head exceptional-divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_SAME_HEAD_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_SAME_HEAD_EXCEPTIONAL_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD49` | The GLD44 directed-chain exceptional union has components `u=-1` and `uw+w+1=0`.  Fifteen- and seventeen-row exact curve certificates leave `1`, with denominator loci disjoint from legal active reciprocal support.  Thus the **entire directed-chain two-pair orbit is proved pointwise empty**, covering all `24` labelled masks.  With GLD45--GLD48, all `66` minimal two-pair masks are empty.  Three-or-more-pair supports, proper-secondary cells, and every permanent bridge remain open. | [Chain exceptional-divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_CHAIN_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_CHAIN_EXCEPTIONAL_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD50` | The `220=C(12,3)` support masks with exactly three reciprocal pairs split into `13` position-relabelling orbits.  Exact `14`--`18`-row function-field certificates exclude the generic complement of a fully displayed orbitwise exceptional hypersurface atlas.  Thus the **generic part of every three-pair orbit is proved empty**.  The displayed divisors, four-or-more-pair supports, proper-secondary cells, and every permanent bridge remain open. | [Three-reciprocal-pair generic exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_GENERIC_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD51` | The sole GLD50 `O10` exceptional surface is `uv+v+1=0`.  Writing `v=-1/(u+1)`, a fourteen-row exact certificate over `Q(u,w)` leaves `1` with denominator lcm `uw(u-1)`, disjoint from the legal active domain.  Thus the **entire three-pair directed-path orbit is proved pointwise empty**, covering all `24` labelled masks.  Twelve three-pair orbitwise divisor unions, larger supports, and every permanent bridge remain open. | [Directed-path exceptional-divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_DIRECTED_PATH_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_DIRECTED_PATH_EXCEPTIONAL_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD52` | The GLD50 `O1` exceptional union has surfaces `w=-1` and `v+w+1=0`.  Fifteen- and fourteen-row exact certificates leave `1`, with denominator loci disjoint from the corresponding legal active domains.  Thus the **entire three-pair out-star orbit is proved pointwise empty**, covering all `4` labelled masks.  Eleven three-pair orbitwise divisor unions, larger supports, and every permanent bridge remain open. | [Out-star exceptional-divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_OUT_STAR_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_OUT_STAR_EXCEPTIONAL_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD53` | The GLD50 `O4` exceptional union has two surfaces.  Exact fourteen-row certificates close each away from their common curve, and a thirteen-row certificate closes that intersection with denominator `w(w+2)`, disjoint from its legal domain.  Thus the **entire three-pair fork-path orbit is proved pointwise empty**, covering all `24` labelled masks.  Ten three-pair orbitwise divisor unions, larger supports, and every permanent bridge remain open. | [Fork-path exceptional-divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_FORK_PATH_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_FORK_PATH_EXCEPTIONAL_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD54` | The GLD50 `O8` exceptional union has factors `u+1`, `w+1`, `2w-1`, and `uv+1`.  Four exact surface certificates reduce the legal residue to `(u,w)=(-1,-1)` and `(-1,1/2)`; nine- and thirteen-row exact curve certificates close those overlaps with denominator roots only at `v=0,1`.  Thus the **entire three-pair reverse-disjoint orbit is proved pointwise empty**, covering all `12` labelled masks.  Nine three-pair orbitwise divisor unions, larger supports, and every permanent bridge remain open. | [Reverse-disjoint exceptional-divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_REVERSE_DISJOINT_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_REVERSE_DISJOINT_EXCEPTIONAL_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD55` | Active-colour exchange reverses every reciprocal arrow through the involution `t->t/(t-1)`.  The fixed helper `x` is invariant and `y` changes sign; an invertible signed colour permutation of all `81` nuisance variables makes all `6561` complete equations covariant.  Thus the GLD50 `O13` in-star orbit transfers to the pointwise-empty GLD52 out-star orbit, proving **all `4` in-star masks empty**.  Eight three-pair orbitwise divisor unions, larger supports, and every permanent bridge remain open. | [In-star colour-exchange exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_IN_STAR_COLOUR_EXCHANGE_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_IN_STAR_COLOUR_EXCHANGE_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD56` | Active-colour exchange reverses the GLD53 fork-path support, and the explicit position permutation `(0,1,2,3)->(2,1,3,0)` carries it to the GLD50 `O12` representative.  The signed covariance holds coefficientwise on all `6561` complete equations, so GLD53's pointwise exclusion transfers exactly.  Thus the **entire three-pair reverse-fork orbit is proved pointwise empty**, covering all `24` labelled masks.  Seven three-pair orbitwise divisor unions, larger supports, and every permanent bridge remain open. | [Reverse-fork colour-exchange exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_REVERSE_FORK_COLOUR_EXCHANGE_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_REVERSE_FORK_COLOUR_EXCHANGE_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD57` | The GLD50 `O11` exceptional union has four surfaces.  Exact surface certificates reduce their legal residue to three intersections; sixteen-, seventeen-, and seventeen-row exact curve cores have denominator roots only at active-forbidden values.  Thus the **entire three-pair in-fork orbit is proved pointwise empty**, covering all `12` labelled masks.  Six three-pair orbitwise divisor unions, larger supports, and every permanent bridge remain open. | [In-fork exceptional-divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_IN_FORK_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_IN_FORK_EXCEPTIONAL_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD58` | Active-colour exchange reverses the GLD57 in-fork support, and the explicit position permutation `(0,1,2,3)->(1,0,3,2)` carries it to the GLD50 `O5` representative.  The signed covariance holds coefficientwise on all `6561` complete equations, so GLD57's pointwise exclusion transfers exactly.  Thus the **entire three-pair out-fork orbit is proved pointwise empty**, covering all `12` labelled masks.  Five three-pair orbitwise divisor unions, larger supports, and every permanent bridge remain open. | [Out-fork colour-exchange exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_OUT_FORK_COLOUR_EXCHANGE_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_OUT_FORK_COLOUR_EXCHANGE_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD59` | The GLD50 `O6` exceptional union has four surfaces.  Exact surface certificates reduce their legal residue to `u=v=-1` and `u=-1,vw+v+w=0`; two fifteen-row curve cores have denominator lcms `2w^2` and `2w^3(2w+1)`, with only inactive roots.  Thus the **entire O6 orbit is proved pointwise empty**, covering all `24` labelled masks.  Four three-pair orbitwise divisor unions, larger supports, and every permanent bridge remain open. | [O6 exceptional-divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_O6_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_O6_EXCEPTIONAL_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD60` | The GLD50 `O3` exceptional union has four surfaces.  Exact surface cores leave five intersections; five curve cores leave only `(-1,-1,-1)` and `(-1/2,-1/2,-1)`, and exact nine- and twelve-row rational cores close both.  Thus the **entire O3 orbit is proved pointwise empty**, covering all `24` labelled masks.  Only the `O2`, `O7`, and `O9` three-pair unions remain; larger supports and every permanent bridge remain open. | [O3 exceptional-divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_O3_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_O3_EXCEPTIONAL_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD61` | The six-factor GLD50 `O2` exceptional union is covered by seventeen exact sparse contradictions.  Five localized denominator ideals contain `1`; the sixth leaves only `(-1/2,-1/2,2)`, closed by a nine-row core.  Active-colour exchange reverses O2 exactly to O7.  Thus the **entire O2 and O7 orbits are proved pointwise empty**, covering `48` labelled masks.  Only O9's `8` masks remain among three-pair supports; larger supports and every permanent bridge remain open. | [O2/O7 exceptional-divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_O2_O7_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_O2_O7_EXCEPTIONAL_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `GLD62` | The six-factor GLD50 `O9` exceptional union is covered by fourteen exact sparse contradictions.  Five localized denominator ideals contain `1`; the long surface reduces to the coprime pair `v^3-v-3` and `v-2`.  Thus the **entire O9 orbit is proved pointwise empty**, covering its `8` masks and completing all `220` exactly-three-pair masks.  Four-or-more supports and every permanent bridge remain open. | [O9 exceptional-divisor exclusion](../claims/arbitrary-order/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_O9_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md), [hostile review](audits/FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_O9_EXCEPTIONAL_DIVISOR_EXCLUSION_REVIEW_2026-08-20.md) |
| `BO1` | For every fixed port-support bound, there is a permutation-invariant, restriction-natural deck whose every bounded window is the zero-edge physical deck with trivial overlaps, but whose first Euler--Wick failure occurs above the bound.  The same defect is invisible to a finite `q=2` identifying atlas with common frames and trivial holonomy.  Thus ambient bounded-window characterization is **refuted**; bounded certification after imposing the full witness/target locus or a proved structural-degree theorem remains open. | [Uniform bounded-window noncharacterization](../claims/arbitrary-order/UNIFORM_BOUNDED_WINDOW_WICK_AND_RESPONSE_ATLAS_NONCHARACTERIZATION_THEOREM.md), [hostile review](audits/UNIVERSAL_EXTRACTION_GLUING_RESPONSE_ATLAS_SUPPORTING_LANES_REVIEW_2026-08-16.md) |
| `GL` | Universal extraction, cross-chart/depth synchronization, and local-to-global gluing for the local restriction lanes: **open**. The balanced full-sensor lane instead has the exact same-graph gate `S2E`. | [Top two-port observability boundary](../claims/arbitrary-order/GRAPH_EXTRACTION_TOP_TWO_PORT_SYNCHRONIZATION_OBSERVABILITY_BOUNDARY.md) |
| `C2` | Automatic reduction of arbitrary characteristic-zero solutions to the pinned `F_2` argument: **refuted as a general lemma** | [Characteristic-two route boundary](../claims/arbitrary-order/CHARACTERISTIC_TWO_CONTRACTION_LIFT_OBSTRUCTION.md) |

| `GLS43` | On the zero-anchor full-swallow fibre, rank four and `q notin Delta` would give `B_Q^anc=Delta+Kq`.  If either residual shore has rank one, quotienting by that shore confines every promoted left or right incidence factor to a two-space, which cannot generate all three diagonal tensors.  With both residual shores rank two, full generation makes both residual normals fully supported; diagonal covariance normalizes both shore planes to `1^perp`.  Row/column sums then align both residual and every port shore, while an exhaustive three-coordinate compatibility lemma confines all port images to one common line.  The complete labelled incidence image consequently has rank at most three, a contradiction.  This is an **exact characteristic-zero arbitrary-root pointwise exclusion of the off-diagonal zero-excess rank-four fibre**, not an exclusion of rank-four `q in Delta`, ranks at least five, raw escape, or any selector/response/synchronization/activity/nuisance/anchor/source-cover gate. | [Rank-four off-diagonal full-swallow exclusion](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_FULL_SWALLOW_OFF_DIAGONAL_ROOT_DECK_COMPLETE_EXCLUSION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_FULL_SWALLOW_OFF_DIAGONAL_ROOT_DECK_COMPLETE_EXCLUSION_REVIEW_2026-08-23.md) |
| `GLS44` | On the surviving rank-four zero-anchor full-swallow stratum, a nonzero diagonal `q` has rank one or two.  Rank two makes both residual shores the same two-colour support plane; projecting the two residual-label columns to the missing-colour cross blocks gives rank two unless every port misses that colour, contradicting the missing diagonal target.  Rank one makes one residual shore the root-colour line; quotienting by it and selecting the root-colour column gives a two-dimensional image against the sole excess line, again a contradiction.  With `GLS43`, every rank-four full-swallow point therefore has `q=0` and `p=0`, so **rank four on `D(p)` is empty pointwise for arbitrary port domains and every fibre**.  The silent `q=0` rank-four fibre, ranks at least five, raw escape, and every attachment/source-cover gate remain open. | [Rank-four nonzero-diagonal full-swallow exclusion](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_FULL_SWALLOW_NONZERO_DIAGONAL_ROOT_DECK_COMPLETE_EXCLUSION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_FULL_SWALLOW_NONZERO_DIAGONAL_ROOT_DECK_COMPLETE_EXCLUSION_REVIEW_2026-08-23.md) |
| `GLS45` | On the rank-four `q=p=0` full-swallow fibre, `q=A_0JC_0^T=0` gives a six-profile residual-shore atlas.  A rank-two shore with zero mate contributes a six-space; a rank-one shore with zero mate contributes a fixed-factor three-space whose sum with `Delta` has dimension at least five.  In dense rank `(1,1)`, the two residual labels polarize the fixed-left and fixed-right aggregate port spaces separately inside `B`; their unique excess quotient lines force both aggregate shores into one two-colour plane, contradicting full generation.  Thus **only the residual-free `(0,0)` and sparse same-label `(1,1)` complete-pair cores remain**, pointwise for arbitrary port domains and every fibre.  Neither survivor is excluded or attached, and ranks at least five, raw escape, and all response/source gates remain open. | [Silent rank-four residual-shore profile reduction](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_SILENT_FULL_SWALLOW_RESIDUAL_SHORE_PROFILE_REDUCTION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_SILENT_FULL_SWALLOW_RESIDUAL_SHORE_PROFILE_REDUCTION_REVIEW_2026-08-23.md) |
| `GLS46` | The two `GLS45` survivors have one complete-label form with image `B=Delta direct-sum Kf`.  Rank-one annihilators and the labelled zero-product lemma confine each of the six global coordinate families to at most two labels, giving **at most twelve active labels and total effective domain dimension at most twelve**.  Independently, an arbitrary-dimensional determinant-cubic theorem gives diagonal rank at most two across every label cut.  Hence all three diagonal directions lie on one triangle of independent edge lines, every other edge is diagonal-silent, and the fourth direction must be a two-dimensional triangle edge or an external pure-`f` feeder.  This is a structural reduction, not an exclusion or finite atlas; both forks, ranks at least five, raw escape, and every response/attachment/source gate remain open. | [Rank-four complete-pair structural localization](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_COMPLETE_PAIR_FAMILY_STRUCTURAL_DEGREE_CUT_AND_TRIANGLE_LOCALIZATION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_COMPLETE_PAIR_FAMILY_STRUCTURAL_DEGREE_CUT_AND_TRIANGLE_LOCALIZATION_REVIEW_2026-08-23.md) |
| `GLS47` | On the GLS46 triangle, the product of the three nonzero edge-diagonal bilinear forms selects one common active vector at each vertex over the original characteristic-zero field.  Their left and right factor matrices are invertible; left--right normalization makes the triangle `Sym_0`.  The transformed physical diagonal supplies three rank-one matrices with independent left and right factors.  Their common quotient skew must vanish, and their common diagonal has full support.  Every external label vector then vanishes, while every extra vector in triangle block `i` is a scalar multiple of `(e_i,e_i)`.  Hence the complete image has rank at most three, contradicting rank four.  Thus **both silent rank-four cores and every zero-anchor rank-four full-swallow fibre are pointwise empty**, and full swallow has nuisance rank at least five.  Ranks five through nine, silent source-to-swallow coverage, raw escape, nonzero anchor, and every response/attachment/source gate remain open. | [Silent rank-four complete-pair exclusion](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_SILENT_FULL_SWALLOW_COMPLETE_PAIR_FAMILY_EXCLUSION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_SILENT_FULL_SWALLOW_COMPLETE_PAIR_FAMILY_EXCLUSION_REVIEW_2026-08-23.md) |
| `GLS48` | Adjoin the two residual labels to the promoted ports as in GLS39 and call a label effective when one of its whole-domain root-incidence maps is nonzero.  With at most two effective labels, at most one raw physical pair label survives.  Across the adaptive cut placing the two probe roots and every effective promoted label on one shore, that complete coefficient/deck term has rank at most one.  At least two promoted ports remain opposite for every `r>=3`, and the three nonzero pure-colour target words give rank three.  Thus **every zero-anchor fully supported fixed-residual target point has at least three effective auxiliary labels**, including every divisor, cancellation, zero-deck, and incidence-rank fibre.  This excludes the full two-label rank-five cell but not rank five with at least three effective labels, ranks six through nine, silent source-to-swallow coverage, raw escape, nonzero anchor, or any legal attachment gate. | [Two-effective-label adaptive-cut pure-target exclusion](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TWO_EFFECTIVE_LABEL_ADAPTIVE_CUT_PURE_TARGET_EXCLUSION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TWO_EFFECTIVE_LABEL_ADAPTIVE_CUT_PURE_TARGET_EXCLUSION_REVIEW_2026-08-23.md) |
| `GLS49` | The whole residual-pair-plus-one-port support `Q disjoint-union {u}` is target-inconsistent: if `q=0`, its source has only two left generators against three GHZ columns; if `q!=0`, the complete `(A union {u})|(Uhat-{u})` source lies in two residual--port tensors plus the `q tensor V_u^*` cylinder.  The target quotient forces `q` pure.  Its rank-one residual factorization makes one residual shore a coordinate line; projecting the other two target-column representations then forces the opposite at-most-two-dimensional shore to contain all three coordinate axes.  On `D(p)`, both residual labels are effective, so **exactly three effective labels are impossible and GLS48 raises the `D(p)` floor to four**, with arbitrary physical decks and every exceptional fibre retained.  The other `p=0` three-label types, four-or-more labels, full-swallow/source coverage, raw escape, and every legal attachment gate remain open.  Here `p` is a root-deck coefficient evaluation, not a physical response. | [Residual-pair-plus-one-port q-cylinder exclusion](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RESIDUAL_PAIR_PLUS_ONE_PORT_THREE_EFFECTIVE_LABEL_Q_CYLINDER_EXCLUSION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RESIDUAL_PAIR_PLUS_ONE_PORT_THREE_EFFECTIVE_LABEL_Q_CYLINDER_EXCLUSION_REVIEW_2026-08-23.md) |
| `GLS50` | In the two `p=0` exactly-three-label rank-five supports left by GLS49, contracting only inactive promoted ports gives a complete physical target consequence.  With one residual and two ports, the evaluated port-pair deck scalar is nonzero, every port joint kernel has dimension at most one, and two simultaneous kernel lines would put all incidence images in `Delta`; the only profiles are `(1,2,3)` and `(1,3,3)`.  With three ports, triple quotient forces the three opposite-pair deck covectors to be the coordinate-line permutation, every joint kernel has dimension at most one, and all three kernels cannot be lines; the only profiles are `(2,2,3)`, `(2,3,3)`, and `(3,3,3)`.  This is an **exhaustive pointwise rank-five exactly-three-label kernel/deck reduction**, not existence or exclusion of the five profiles, a physical response/selector, downstream synchronization, source coverage, four-or-more-label classification, higher-rank closure, or node closure. | [Rank-five three-label kernel/deck profiles](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FIVE_THREE_EFFECTIVE_LABEL_KERNEL_PROFILE_AND_MANDATORY_DECK_REDUCTION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FIVE_THREE_EFFECTIVE_LABEL_KERNEL_PROFILE_AND_MANDATORY_DECK_REDUCTION_REVIEW_2026-08-23.md) |
| `GLS51` | For exactly three effective labels, GLS49 excludes the two-residual support.  With three promoted ports, the complete target quotient makes the three opposite decks the coordinate-line permutation; restricting each port to its deck hyperplane makes every pair polarization diagonal while the three pair images contain the three independent diagonal lines, contradicting GLS39.  With one residual and two ports, a denominator-free shifted determinant synchronizes both deck covectors to one coordinate line.  The shifted unmatched zero graph makes the deck-coordinate vectors vanish, forces both residual shores pure on that line, and leaves only the separated crossed-square orientation on the other two colours.  Both port joint maps are injective and the complete incidence image is exactly `Delta` plus the four coordinate-star matrix units, of rank seven.  Thus **exactly three effective labels can occur only at rank seven in this normal form**; ranks five, six, eight, and nine have at least four labels.  An exact rational shared-interface control shows rank seven is sharp without proving principal-deck physical realization.  That realization, four-or-more labels, source coverage, raw escape, every legal attachment gate, and node closure remain open; evaluated decks are not responses or selectors. | [Three-label shared-polarization rank-seven normal form](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_THREE_EFFECTIVE_LABEL_SHARED_POLARIZATION_RANK_SEVEN_NORMAL_FORM_AND_OTHER_RANK_EXCLUSION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_THREE_EFFECTIVE_LABEL_SHARED_POLARIZATION_RANK_SEVEN_NORMAL_FORM_AND_OTHER_RANK_EXCLUSION_REVIEW_2026-08-23.md) |
| `GLS52` | In the sole one-residual/two-port support left conditionally by GLS51, retain every inactive promoted port instead of evaluating it at `1`.  The GLS51 common-coordinate lock puts both residual--port images in one coordinate star.  Projecting the full target to either off-coordinate diagonal therefore isolates the same residual-evaluated physical deck complementary to the port pair.  The contracted target fixes the corresponding two nonzero port-pair coefficients.  The full target then forces that one deck tensor to equal `gamma` times the pure inactive-port word in each of two distinct colours, impossible because `|Uhat-{u,v}|=2r-4>=2` and `gamma!=0`.  Together with GLS49 and the three-port part of GLS51, **every exactly-three-effective-label zero-anchor full-swallow target fibre is empty and every such point has at least four effective labels**.  The result retains every exceptional fibre and uses no response, selector, or chosen minor.  Four-or-more labels, source coverage, raw escape, nonzero anchor, every legal attachment gate, and node closure remain open. | [Three-label uncontracted complementary-deck exclusion](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_THREE_EFFECTIVE_LABEL_UNCONTRACTED_COMPLEMENTARY_DECK_TWO_COLOUR_SEPARATION_EXCLUSION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_THREE_EFFECTIVE_LABEL_UNCONTRACTED_COMPLEMENTARY_DECK_TWO_COLOUR_SEPARATION_EXCLUSION_REVIEW_2026-08-23.md) |
| `GLS53` | Suppose the GLS52 floor is attained by four promoted auxiliary labels and no residual label.  Contract the fixed residuals and only the inactive promoted ports.  The six surviving raw pair labels are exactly the fifteen-matching hafnian expansion of a reconstructed legal graph on the two probes and four active ports: the root edge is zero, root--port edges are the physical `X/Y` incidence blocks, and each port--port edge is the corresponding residual- and inactive-evaluated physical complementary deck.  Its target is weighted ternary GHZ with three nonzero weights; one invertible local diagonal scaling normalizes them.  The accepted complete six-vertex theorem therefore makes **the no-residual exactly-four-label support empty at every `r>=3` and on every exceptional fibre**.  Four-label supports with one or two residual labels, five-or-more-label supports, source coverage, raw escape, nonzero anchors, every legal attachment gate, and node closure remain open. | [Four-promoted-label six-vertex reconstruction exclusion](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FOUR_PROMOTED_LABEL_SIX_VERTEX_RECONSTRUCTION_EXCLUSION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FOUR_PROMOTED_LABEL_SIX_VERTEX_RECONSTRUCTION_EXCLUSION_REVIEW_2026-08-23.md) |
| `GLS54` | Start with an actual complete witness, then fix a fully supported residual point and define auxiliary activity.  If `|Act|<=4`, pad `Act` to a four-set using only inactive promoted ports.  Retain that set as four open physical vertices, contract inactive residuals at their defining vectors and other inactive promoted ports at all ones, and apply the complete `GLS8` identity.  Every raw pair outside the four-set has an inactive contracted endpoint and vanishes; each surviving complement is a bilinear edge on the other two open vertices.  The result is a reconstructed legal weighted six-vertex GHZ graph, excluded after local normalization by the accepted finite theorem.  Thus **every actual characteristic-zero zero-anchor witness has `|Act|>=5` at every fully supported residual point**, without full swallow, rank, response, selector, or deck-nonzero assumptions.  One fixed residual equation alone cannot license this uncontraction; inactive residuals remain contracted.  Five-plus labels, source/attachment gates, nonzero anchors, node closure, and global resolution remain open. | [Four-slot partial-uncontraction five-label floor](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FOUR_SLOT_PARTIAL_UNCONTRACTION_SIX_VERTEX_RECONSTRUCTION_AND_FIVE_LABEL_FLOOR_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FOUR_SLOT_PARTIAL_UNCONTRACTION_SIX_VERTEX_RECONSTRUCTION_AND_FIVE_LABEL_FLOOR_REVIEW_2026-08-23.md) |
| `GLS55` | Before fixing any residual point, call an auxiliary label rigid when the kernel of its full joint two-probe incidence map contains no fully supported local vector.  If at most four labels were rigid, retain a four-set containing all of them and contract every outside label at its own fully supported simultaneous-kernel vector.  Every outside raw pair vanishes, the zero anchor kills the top term, and the six surviving terms reconstruct a legal weighted six-vertex GHZ graph.  Hence **every actual characteristic-zero zero-anchor witness has at least five full-map rigid labels**.  Over an infinite field, rigidity is exactly containment of some coordinate covector in the joint incidence row space, so those five labels are active at every fully supported residual point.  On `|Rig|=5`, contracting every non-rigid label gives the exact seven-party identity with ten trilinear decks; `|Rig|>=6` remains separate.  This strictly strengthens GLS54 without full swallow, rank, response, selector, or deck assumptions.  The coordinate rows may differ by label and supply no complete nuisance annihilation, response, synchronization, receiver, nonzero-anchor closure, node closure, or global resolution. | [Torus-kernel contraction and five-rigid-label floor](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TORUS_KERNEL_CONTRACTION_AND_FIVE_RIGID_LABEL_FLOOR_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TORUS_KERNEL_CONTRACTION_AND_FIVE_RIGID_LABEL_FLOOR_REVIEW_2026-08-23.md) |
| `GLS56` | For any nonrigid auxiliary label in the complete `GLS8` chart, contract one fully supported vector in its full joint probe kernel.  If one target colour had no nonzero coordinate-pure edge from that label, choose on every other auxiliary label an edge-kernel vector retaining that colour.  Every complete matching term then dies through the probe-silent label while the pure target word survives.  Thus **every kernel-torus point has three distinct colour-pure neighbours**.  Finite irreducibility gives one fixed nonzero pure restricted shore per colour, one simultaneous activating torus point, and a descending linear-section flag covering every exceptional divisor.  Rigid same-coordinate readouts obey an exact pure-axis/projective-anti-synchronization trichotomy.  On zero-anchor `r=3`, either all six labels are rigid or the unique nonrigid label has a three-colour star into rigid neighbours.  Under the natural `GLD3` re-anchor, `h=0`; if the star triangle is target-diagonal, all three pair responses vanish, so pair-depth activity is impossible.  This is a structural split and receiver no-go, not a promoted response, legal selector, target attachment, source cover, named detector entry, node closure, or global resolution. | [Probe-kernel pure-star flag and GLD3 activity no-go](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_NONRIGID_PROBE_KERNEL_THREE_COLOUR_PURE_STAR_ESCAPE_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_PROBE_KERNEL_PURE_STAR_AND_RIGID_COMPANION_BOUNDARY_REVIEW_2026-08-23.md) |
| `GLS57` | On the zero-anchor `r=3` all-six-rigid subbranch where every joint probe-incidence map has rank one, torus rigidity gives one coordinate readout per label.  The complete pure target forces an exact **`2+2+2` colour-pair partition**.  For every colour, the unique same-colour pair companion is the full pure diagonal target tensor times a nonzero scalar, and its complementary physical four-deck has a nonzero pure coefficient.  An exact mixed-word master identity makes the deck's complementary `2 x 2 x 2 x 2` off-readout face pure: fifteen mixed cells vanish and the sole constant-colour cell survives.  At least one colour pair lies in `Uhat`, so one named promoted pair response polynomial is nonzero; exactly two occur when `Q` itself is one colour pair.  A common residual torus point retains one such response and the two original `GLS4` polynomial gates.  With the old probes as a `GLD3` residual pair, the zero anchor removes every direct pair term and each remaining response has only the cell `(kappa(s),kappa(t))`; hence every port has diagonal activity in at most one colour and the direct `GLD3` route is impossible.  This is a same-graph source/deck and generic response-supply theorem plus a receiver no-go, not fibrewise response nonvanishing, complete-nuisance survival, a normalized selector, other-receiver synchronization/activity, higher-rank all-rigid closure, arbitrary-root coverage, node closure, or global resolution. | [All-rank-one rigid colour pairing and promoted-response supply](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_ALL_RANK_ONE_RIGID_COLOUR_PAIRING_AND_PROMOTED_RESPONSE_SUPPLY_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ALL_RANK_ONE_RIGID_COLOUR_PAIRING_AND_PROMOTED_RESPONSE_SUPPLY_REVIEW_2026-08-23.md) |
| `GLS58` | On the zero-anchor `r=3` all-six-rigid branch, every nonzero boundary-kernel coordinate forces a fixed coordinate-pure neighbour shore.  One deficient contraction gives an exact seven-slot identity with ten physical trilinear decks.  Two deficient contractions reconstruct one honest six-vertex graph with `D_uv=hW_uv+a_u tensor b_v+b_u tensor a_v`; rigidity makes its target zero, mono, or binary, and an exact all-rigid `h=0` binary control shows the three-colour finite theorem cannot exclude it.  With no deficient label, all six joint maps are injective and obey the denominator-free cross-product identity `sum_c z_(0,c)z_(1,c) product_t(k_t)_c=0`, split exactly into a coordinate-axis-shore cover or genuine polynomial cancellation.  Transverse all-rank-two maps force their kernel zero sets to cover all three colours.  This is an exhaustive rank-profile reduction, not a response, selector, receiver, higher-rank exclusion, arbitrary-root theorem, node closure, or global resolution. | [All-rigid kernel contraction and cross-product reduction](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_ALL_RIGID_KERNEL_CONTRACTION_AND_CROSS_PRODUCT_REDUCTION_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ALL_RIGID_KERNEL_CONTRACTION_AND_CROSS_PRODUCT_REDUCTION_REVIEW_2026-08-23.md) |
| `GLS59` | At zero anchor, a nonzero auxiliary joint-kernel vector forces, for either old probe and every colour supported by both vectors, a distinct nonzero coordinate-pure neighbour block.  Finite irreducibility gives fixed whole-domain pure probe blocks and complete three-step exceptional-section flags.  On the `r=3` unique-nonrigid branch, the two three-label old-probe stars overlap among five rigid labels.  Same-colour overlap gives a rank-one coordinate-plane kernel and an exact binary six-vertex descent; cross-colour overlap gives a rank-two coordinate-axis kernel and an exact monocolour descent.  At every fully supported old-probe vector, the natural `GLD3` pure-star triangle cannot be simultaneously target-diagonal.  This is an arbitrary-root conditional exchange theorem and an exhaustive unique-nonrigid `r=3` structural reduction, not a response, selector, nuisance survivor, alternate receiver, branch exclusion, arbitrary-root source cover, node closure, or global resolution. | [Probe exchange, overlap, and unique-nonrigid descent](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_PROBE_EXCHANGE_OVERLAP_AND_UNIQUE_NONRIGID_DESCENT_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_PROBE_EXCHANGE_OVERLAP_AND_UNIQUE_NONRIGID_DESCENT_REVIEW_2026-08-23.md) |
| `GLS60` | On the `GLS57` all-rank-one branch, each same-colour pair equation has rank one, so at least one full old-probe shore lies on the corresponding coordinate line; the opposite shore has an exact quotient anti-synchronization, every label has a nonzero pure old-probe edge, and one probe is shore-pure on at least two colour pairs.  Every fully supported probe contraction is the one-edge hafnian first variation with three nonzero diagonal weights.  The direct companion graph is zero or decomposable on the mixed `2+2+2` word, while a vertex-gauge identification with the internal graph would either kill the first variation or create an excluded ternary six-vertex witness.  The earlier claim that a weighted permanent `P_6` restriction is accepted by the six-vertex theorem is corrected: it enters the separate open permanent subtree.  This is a pointwise raw-structure theorem and two-splice no-go, not a non-gauge reconstruction, permanent restriction, nuisance survivor, selector, response synchronization/activity theorem, named receiver, higher-rank/arbitrary-root cover, node closure, or global resolution. | [Pure-probe orientation and hafnian splicing boundary](../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_ONE_PURE_PROBE_ORIENTATION_AND_HAFNIAN_SPLICING_BOUNDARY_THEOREM.md), [hostile review](audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_ONE_PURE_PROBE_ORIENTATION_AND_HAFNIAN_SPLICING_BOUNDARY_REVIEW_2026-08-23.md) |

## Typed-edge table

| Source | Relationship | Target | Exact meaning |
|---|---|---|---|
| `G0` | reduction | `S1` | Every hypothetical ternary witness has a balanced-sensor dichotomy. |
| `S1` | exact refinement | `S2E` | The unique rational full-sensor lift has an exact Cramer target, normalization, pair-pole, and Euler--hafnian gate. |
| `S2E` | exact finite-jet refinement | `S2J` | Prime-divisor regularity of each Cramer pair is equivalent to explicit nonendpoint first stresses and endpoint Hessian stresses; no factorization of the Cramer minor is needed. |
| `S2J` | exact target-column refinement | `S2K` | Every cleared pair jet is an adjugate image and one selected-column replacement determinant; under target consistency, its vanishing is the corresponding full-sensor column-span condition. |
| `S2K` | exact projective compression | `S2L` | Degree-zero and differentiated degree-one Euler syzygies recover the omitted radial first/Hessian coordinates, so only the affine-projective replacement minors remain. |
| `S2L` | ambient full-row compatibility boundary | `S2M` | Eight exact `m=3` controls restore all target rows and empty normalization without making any retained coordinate redundant; the construction stops before the common-shore matching-sum sensor image. |
| `S2M` | exact common-shore image interface | `S2N` | At `m=3` the singleton shared-factor equations and empty six-term permanent are necessary and sufficient for the four shore-sensor columns.  A separate Latin-plane system proves the ambient full-row format is strictly larger, but does not decide any of the eight S2M controls. |
| `S2M` + `S2N` | exact binary pullback | `S2O` | Root-colour projection sends every one of the eight controls to the same necessary binary image/kernel/permanent system.  The reduction neither asserts that this residual is empty nor lifts a binary solution to a ternary common shore. |
| `S2O` | exact transverse residual obstruction | `S2P` | The common binary singleton map has four exhaustive kernel-plane rank types plus the zero-block degenerations.  A pure image tensor and a pure kernel permanent always share a factor line, contradicting the three transverse S2O factor pairs. |
| `S2P` | realized-incidence boundary obligation | `S2` | All eight ambient coordinatewise controls are excluded from the common-shore image, but they do not exhaust realized ways to fail a retained pair identity.  A universal argument must now control arbitrary common-shore target incidences, and higher orders also retain the Euler--hafnian recurrences. |
| `S2E` + `S2N` | exact `m=3` pole localization | `S2Q` | Empty normalization leaves three separately linear singleton columns.  Minimal one-, two-, and three-column dependence supports classify every possible rank-drop divisor; outside the three low-span cases the rational pair deck extends globally.  The accepted six-vertex theorem then excludes that regular physical stratum. |
| `S2Q` | exceptional-incidence boundary obligation | `S2` | The rank-one singleton, pair-plane, and common-three-space strata are not excluded, and the three-column divisor classification does not apply to the larger complete deck at `m>=4`. |
| `S2N` | exact physical contraction obstruction | `S2R` | Modulo the total singleton span, target consistency identifies the physical empty companion with GHZ.  A fully supported product annihilator would turn the former into a local image of `P_3` and the latter into a concise diagonal; flattening and tensor rank contradict this. |
| `S2R` | exact coordinate-boundary refinement | `S2S` | Singleton annihilation places the root--root contraction vector `beta` in all three cross-map kernels.  For nonzero `beta`, the empty companion factors through one common binary quotient, whose `P_3` orbit is determined by the coordinate support of `beta`. |
| `S2Q` + `S2S` | exact common-three-space component refinement | `S2T` | Projective dimension gives every annihilator component dimension at least three.  Closed missing-colour equations then bound the total cross-column rank, unless the whole component is multi-boundary or `beta` vanishes identically. |
| `S2T` | exact full-joint-cross-rank refinement | `S2U` | If the joint cross map is invertible, the singleton span equals the shared-derivative image.  The common-three-space condition leaves one coordinate-monomial root block, and explicit global pair blocks plus the six-vertex theorem force its two endpoint colours to agree. |
| `S2U` | exact source-aligned-row refinement | `S2V` | If the exceptional root row equals one source summand, all six off-diagonal marked products vanish.  The pure-or-line zero-divisor lemma and complementarity make this impossible. |
| `S2V` | exact two-source-row refinement | `S2W` | Every nonaligned three-plane in two source summands splits the two mixed products.  Concatenation gives one `(6+3)` zero-divisor problem and excludes the remaining two-source charts. |
| `S2W` | exact full-support-row refinement | `S2X` | The shared derivative is injective except for one synchronized rank-one-pair geometry.  Pure-source pigeonhole excludes the regular case and a five-space trap excludes the exception. |
| `S2X` | exact corank-one refinement | `S2Y` | Restriction to a hyperplane loses at most one derivative rank, so the sparse equation persists.  The regular zero-grid span and exceptional covector line both contradict rank eight. |
| `S2Y` | exact rank-seven single-root refinement | `S2Z` | On the one-root-block branch, rank seven is equality in the four-dimensional zero-grid bound.  The pure/conjugate-mixed marked-plane classification contradicts the two surviving GHZ diagonal rows in every normal form. |
| `S2Z` | exact rank-seven two-root refinement | `S2AA` | Codimension two makes the two-root derivative sharp.  Its coordinate common factor leaves two exact target slices whose pointwise zero-diagonal permanent matrices cannot have rank one after both involved root rows are forced full rank. |
| `S2AA` | exact lower-rank single-root refinement | `S2AB` | The pure/mixed zero-grid classification extends below the sharp rank-seven equality.  Its lower-dimensional and shared-tangent boundaries also contradict the two diagonal GHZ rows, excluding one root block at every rank. |
| `S2AB` | exact rank-six shared-factor refinement | `S2AC` | Codimension three permits derivative rank five or six.  In the shared-factor rank-five case, the two unaffected target slices force a row-rank trichotomy; the mixed profile reduces to the rank-free crossed-pair obstruction, while the equal profiles fail directly. |
| `S2AC` | exact transverse-rank-six refinement | `S2AD` | The derivative kernel splits off the third root space.  Its beta-zero locus yields a complete two-block torus-avoidance atlas, while relation-plane annihilators and the binary quotient force every non-coordinate relation plane into an aligned rank-two row boundary. |
| `S2AD` | exact aligned-rank-two refinement | `S2AE` | The rank-two row makes the joint image a graph.  The full target coefficient identity and permanent symmetry reduce it to a repeated-row tangent obstruction followed by an exhaustive symmetric-square mixed-product kernel atlas. |
| `S2AE` | exact coordinate-relation refinement | `S2AF` | A coordinate relation forces one involved row rank two.  The `(3,2)` graph charts fall to the binary five-product obstruction, while the `(2,2)` chart falls to the square-pencil factor-sharing and zero-divisor bound. |
| `S2AF` | exact joint-rank-five refinement | `S2AG` | Codimension four permits derivative rank at most seven.  The shared-factor and injective-third-row mechanisms inherit rank-free contradictions; the three-root equality is Hilbert--Burch and its beta-zero components force the explicit projection/coordinate atlas. |
| `S2AG` | exact support-two profile refinement | `S2AH` | Two involved rank-two rows and two coordinate-monomial blocks force a canonical target table.  The third-row two-plane is a common mixed-product annihilator with one rank-one square, while full singleton rank is the nonzero alternating separated tensor. |
| `S2AH` | exact `(2,2)` completion | `S2AI` | The beta-zero Type-II coordinate factor collapses to a monomial under the target-kernel row.  The two remaining kernel-colour planes fall to incompatible coefficients or a fully transverse correction-line upgrade of the common-zero atlas. |
| `S2AI` | exact support-two mixed-row refinement | `S2AJ` | A rank-two graph shore misses one target colour.  Its zero row pins every singleton correction to that pure target line, while the support-two relation makes two third-root rows proportional; the intervening diagonal target line cannot be absorbed. |
| `S2AJ` | exact support-two `(3,3)` refinement | `S2AK` | The invertible graph contraction puts every singleton correction in the binary diagonal plane.  Permanent symmetry fixes the third graph column, and the full target table gives a transverse binary-plane common-zero system whose alternating singleton determinant vanishes. |
| `S2AK` | exact support-one higher-row refinement | `S2AL` | The support-one coordinate kernel kills one third-root row.  Injective or zero-row graph control leaves one pure correction line; permanent symmetry then produces a two-plane square pencil or the binary five-product table. |
| `S2AL` | exact support-one `(2,2)` refinement | `S2AM` | The two involved zero rows determine the complete correction table and one relation-plane normal form; its untouched square and three binary-plane mixed maps satisfy the inherited common-zero obstruction. |
| `S2AG` + `S2AL` | exact Hilbert--Burch repeated-coordinate refinement | `S2AN` | In profile `(1,1,1)`, two equal coordinate factors leave a complete untouched `2 x 2 x 3` grid.  Away from the complementary-coordinate boundary it contracts to a forbidden binary diagonal permanent frame on three two-planes in one three-space. |
| `S2AN` + `S2AL` | exact complementary-support refinement | `S2AO` | A two-supported complementary factor gives two transverse diagonal targets at one contracted row and zero at a nonzero same-colour row.  The three-plane incidence split excludes every equal or distinct arrangement, leaving only `(s,s,t)` with `s!=t`. |
| `S2AO` + `S2R` + `S2AL` | exact repeated-coordinate completion | `S2AP` | For `(s,s,t)`, torus avoidance forces a coloop among seven annihilator rows.  Equal-plane square symmetry, untouched target coefficients, and a binary-cubic quadratic-annihilator lemma exclude all seven orientations. |
| `S2AP` + `S2R` | exact all-coordinate-distinct completion | `S2AQ` | For the coordinate triangle, torus avoidance again forces a coloop.  Its zero binary cube and three transverse exterior target faces contradict either the totally cubic-zero two-plane atlas or the quadratic-annihilator fork lemma. |
| `S2AQ` + `S2R` + `S2AL` | exact `(1,1,1)` completion | `S2AR` | For two distinct coordinate factors and a noncoordinate third factor, torus avoidance gives eight hyperplane alternatives.  Each forces equal row planes, where square-zero mixed-factor sharing or the pointwise tangent-factor lemma excludes every orientation. |
| `S2AR` + `S2R` + `S2AL` | exact `(1,1,2)` central-chart refinement | `S2AS` | The recovery scalar `gamma(z)gamma(w)` gives nine hyperplanes.  Five force equal first/second row planes and fail by the two-square lemma or a complete split-centre source-support atlas, leaving four ordinary coloops away from two repeated outer lines. |
| `S2AS` | exact distinct-colour third-colour-coloop refinement | `S2AT` | A third-colour coloop makes six rows span a two-plane while the third-row image remains three-dimensional.  An exterior face becomes a square, and the complete source-support split contradicts either square rank, three independent target factor lines, or transverse factor sharing. |
| `S2AT` | exact distinct-colour central-colour-coloop refinement | `S2AU` | The remaining coloop again gives a two-plane, three-dimensional third-row image, and nonzero target square.  Fibre dimensions and the full Segre-tangent pair-sum atlas contradict every source-support case, closing the distinct-colour central chart away from two repeated outer lines. |
| `S2AU` | exact single-repeated-divisor refinement | `S2AV` | On one repeated outer divisor the `T_s` exterior face vanishes, but transpose recovery still gives a finite hyperplane fork.  A one-face equal-plane lemma and two full-sensor alternating coloop atlases use the surviving `T_t` face and `T_u` core to exclude every nonintersection point; root symmetry closes the mate divisor. |
| `S2AV` | exact double-repeated-intersection refinement | `S2AW` | At the simultaneous intersection, seven distinct recovery/coordinate factors give three equal-plane and four coloop cases.  A three-dimensional square-radical bound, a common-radical sum/difference intersection, and a coefficientwise zero-rectangle correction obstruction exclude all seven. |
| `S2AW` | exact same-colour central-chart refinement | `S2AX` | The four same-colour ordinary coloops are one symmetry orbit.  The in-plane row coefficient fork gives a square/mixed tangent contradiction or one of two exact endpoint atlases: a square-zero row with two transverse targets, or a rank-one square with two alternating radical rows. |
| `S2AX` + `S2AG` + `S2R` | exact outer-chart and `(1,1,2)` completion | `S2AY` | In either outer coordinate-pair chart, recovery forces one of nine coordinate coloops.  A universal binary exterior face, the S2AL/S2AX coefficient forks, and two support-degenerate endpoint lemmas exclude all orientations.  Root symmetry closes the mate, and the three-pair Boolean atlas then closes the complete `(1,1,2)` profile. |
| `S2AY` + `S2AG` + `S2R` | exact `(1,2,2)` coordinate-coloop localization | `S2AZ` | Root symmetry and a kernel-generator gauge give `x=lambda e_s`, `c=mu e_t`, and `y_t=0`.  Recovery by `lambda mu alpha_s beta_t` forces nine coordinate coloops.  Exact target contraction makes the common first-row image `R` two-dimensional, so seven coloop complements equal `R` and only the two complementary first-root coloops require separate normal forms. |
| `S2AZ` + `S2AL` + `S2AN` + `S2AO` | exact distinguished-second-root-coloop refinement | `S2BA` | Exact target contraction makes `pi` and `theta` injective.  On `beta_t=gamma(w)=0`, the derivative vanishes and the complete target equation gives a `3 x 2 x 2` diagonal face inside `R+span(A)`.  The binary-diagonal and same-third-row obstructions force `w` onto one of the two complementary coordinate lines; two auxiliary faces give the remaining coordinate incidences. |
| `S2BA` | exact coordinate-endpoint completion | `S2BB` | At a coordinate endpoint the face shore is exactly three-dimensional and the target table has one surviving cell.  The zero second row has full, two-source, or pure support; the three cases respectively collapse the shore, remove one tensor source, or force the two third-row partner maps to have the same zero behavior. |
| `S2BB` + `S2AZ` + `S2AN` + `S2AO` + `S2AL` | exact distinguished-first-root-coloop exclusion | `S2BC` | The determinant-zero projective pencil gives three row planes in one at-most-three-space.  Its coordinate gates force one of two linear degeneracies; one-sided cases are same-third-row tables, while their intersection is excluded by the new same-pair plane-incidence lemma. |
| `S2BC` + `S2AZ` + `S2AL` + `S2AN` | exact residual-second-root-coloop refinement | `S2BD` | For either `beta_j` coloop with `j!=t`, the derivative-zero face gives a binary diagonal table whose first and third planes and complementary middle row lie in one exact three-space.  The one-row escape is impossible: plane intersection reduces to four endpoint incidences, seven nonzero support masks exhaust each endpoint, and all 28 leaves have exact rational Nullstellensatz contradictions.  Hence `w_t=0`, without excluding either coloop. |
| `S2BD` + `S2BC` + `S2AL` + `S2AO` | exact residual-second-root coordinate-line refinement | `S2BE` | With `w_t=0`, complementary support two gives a same-third-row table with one possible middle-row escape.  Plane incidence forces the zero third row to be the intersection line.  The remaining torus orbit has 14 endpoint-support, five generic fixed-support, and two polynomial one-parameter families; exact rational identities exclude all 21.  Hence `w` is coordinate, without excluding the four ordered endpoints. |
| `S2BE` + `S2BC` + `S2BD` | exact residual-second-root endpoint-support refinement | `S2BF` | The residual coloop forces `p_j` genuinely outside `S`.  Every determinant-face pencil member nevertheless puts the first and third planes and a nonzero middle-plane line in one at-most-three-space.  A strengthened 28-case binary-frame obstruction forces one projective gate to vanish identically; the auxiliary gamma-kernel face then gives the exact six-case endpoint support table, without excluding an endpoint. |
| `S2BF` + `S2BE` + `S2BC` | exact residual-second-root `s=t` endpoint exclusion | `S2BG` | When `s=t`, the endpoint support table makes `z,w` a basis of `e_t^perp`.  A generic projective direction produces a same-third-row table whose middle plane has an arbitrary nonzero intersection with the common space.  The generic intersection has 21 exact row-space families; rational unit-ideal identities exclude all of them. |
| `S2BG` + `S2BF` | exact residual-second-root complementary-`y` refinement | `S2BH` | With `s!=t`, an endpoint equal to `s` directly forces the other complementary coordinate for `y`.  At the other endpoint, the contrary `y_s!=0` assumption makes `z,w` span `e_s^perp`; a generic determinant face is the S2BG generalized same-third-row table.  Hence `y` is always the coordinate complementary to `s,t`. |
| `S2BH` + `S2BF` + `S2BC` | exact residual-second-root terminal-endpoint refinement | `S2BI` | With `y=e_u`, every projective direction outside `z_s=w_s=0` exposes a common-active-middle-row table.  The escaping plane can meet the common space in either indexed row or a generic line; the first/third planes may agree or meet in any ordered line.  A complete 90-case polynomial cover and rational unit identities leave only `w=e_u,z_s=0,z_t!=0`. |
| `S2BI` + `S2BF` + `S2BC` | exact residual-second-root-coloop completion | `S2BJ` | On the terminal same-pair face, the selected residual divisor distinguishes two exact incidences: active-row cancellation modulo `R`, or an inactive middle row in `R`.  Equal first/third planes contradict permanent symmetry; otherwise the intersection line has three supports and the two incidence branches have three or two affine patches.  Exact rational identities exclude all `9+6=15` families. |
| `S2BJ` + `S2BF` + `S2BI` + `S2AZ` | exact third-root-coloop completion | `S2BK` | A selected `gamma_k` coloop puts the first and second binary row planes of `beta_t=gamma(w)=0` in one exact three-space and gives the third plane a nonzero intersection.  The `w_t!=0` table is S2BF's arbitrary-intersection binary diagonal, complementary support two is S2BI's common-active-row table, and coordinate `w` becomes a beta coloop under exact root exchange.  Thus all three `gamma_k` orientations are impossible. |
| `S2BK` + `S2BF` + `S2BE` + `S2BC` + `S2AL` | exact complementary-first-root-coloop completion | `S2BL` | A selected `alpha_a` divisor supplies a two-plane meeting the exact `alpha_s=0` pencil face in `r_b` and containing both partner kernels and the opposite active-row sum.  Arbitrary-intersection binary diagonal and same-third-row obstructions force the common degeneration.  Equal partner planes and the all-in-space boundary fail analytically; five exhaustive polynomial row-space families have exact rational unit identities. |
| `S2AG` + `S2AD` + `S2AF` | lower-joint-rank transverse projection and sharpness refinement | `S2BM` | For joint rank three or four, projection to the involved roots is a three-plane and the uninvolved row has rank one or two.  Kernel contraction gives support at most two.  Rank one forces complementary diagonal root blocks and a one-cell permanent frame; explicit physical row systems realize it at both ranks and expose the exact coordinate-pole pair lifts. |
| `S2BM` + `S2AI` + `S2AJ` + `S2AK` + `S2AL` + `S2AM` | joint-rank-four transverse `q=2` completion | `S2BN` | The rank-four incidence has a two-plane `Q` meeting the involved-row three-plane `V` in one line.  The common-zero atlas strengthens from `V intersect Q=0` to `Q not subset V`: its sole intersection-sensitive conjugate chart forces the second `Q` generator into `V`.  This closes the residual `(2,2)` and `(3,3)` profiles, while the old target-line and square-pencil proofs transfer incidence-free. |
| `S2BN` + `S2BM` + `S2AI` + `S2AK` + `S2AM` | joint-rank-three transverse `q=2` exceptional completion | `S2BO` | On `Q subset V`, every nonzero singleton determinant lies in the conjugate two-source chart.  The two unrepresented pure targets force complementary monomial root blocks and collapse both involved rows to rank two.  The remaining source chart has one exact normal form and two kernel-support variants; both have exact local singleton/empty controls and the same unavoidable three-pole rational pair lift.  Exhaustiveness plus the Cramer--Euler pair-regularity gate excludes every graph extension. |
| `S2BM` + `S2E` | joint-rank-three/four transverse `q=1` pair-residue completion | `S2BP` | S2BM's one-cell frame has an exhaustive Segre-tangent/common-zero source atlas.  Its singleton determinant contains missing-colour coordinate divisors.  The corresponding Cramer numerator omits that coordinate; the residual two-/one-factor charts contradict coprime GHZ monomials, the nonzero third singleton row, or the alternating determinant itself.  Hence every rational lift has a pair pole and the exact pair-regularity gate excludes both graph-extension cells. |
| `S2AG` + `S2X` + `S2R` + `S2BP` | lower-rank three-root derivative and torus localization | `S2BQ` | Three nonzero derivative summands have zero, one, or two syzygies.  The one-syzygy chart is shared-factor rank eight and its torus-zero equations give a coordinate/monomial quotient atlas.  The two-syzygy chart is Hilbert--Burch; its full projection profile is rank-independently impossible and its other profiles retain the S2AG coordinate atlas.  Rank--nullity records the distinct rank-three/rank-four kernel incidences. |
| `S2BQ` + common-shore empty identity | rank-four/rank-eight target-row coupling | `S2BR` | Containment of the shared syzygy in `K` kills the tangent terms under deficient involved rows.  Coefficientwise diagonal targets force coordinate kernels and matching diagonal residual-block contractions.  Two distinct involved missing colours then impose incompatible contractions on the same pure-target correction preimage. |
| `S2BQ` + `S2BR` + `S2AL` | canonical-binomial nonmonomial completion | `S2CG` | When all three shared-factor lines agree with one coordinate and the actual residual block is a nonzero complementary diagonal binomial, kernel incidence identifies the injective third-row space with the full-sensor alternating three-space.  The complete target gives two mixed zero pairs and a rank-two diagonal difference.  The zero-pair support classification, radical-line bound, and exhaustive nine projective flags force a tangent-line contradiction in every row-plane profile. |
| `S2CF` + `S2CG` | diagonal zero-visible-wall completion | `S2CH` | The two failed visibility conditions have only the crossed coordinate solutions `(x,y)=(e_0,e_1),(e_1,e_0)`.  In either case one perpendicular coordinate row has the other injective perpendicular plane as a two-dimensional radical shore in the corrected cube.  The general full-sensor `Alt(Q)` interface and S2CG radical-line bound exclude it. |
| `S2CF` + `S2CG` + `S2CH` | diagonal same-coordinate one-visible completion | `S2CI` | On `x=y=e_0` and `x=y=e_1`, two corrected-cube cross-zero pairs have an exhaustive split-three-space/common-split-plane dichotomy.  The complementary cell contradicts a complete recovered target face; the aligned cell contradicts the unsliced target after exact source recovery and quotient by the visible target's factor lines. |
| `S2CF` + `S2CG` + `S2CH` + `S2CI` | complete diagonal one-visible completion | `S2CJ` | The exact visibility census has twenty ordered one-visible masks.  Four radical masks violate the S2CG radical bound; fourteen explicit cross-pair charts reduce to split-Q/common-plane geometry.  Recovered faces close all `T_0` cells, source recovery and the unsliced target close six `T_1` cells, and full root-matrix coefficient separation plus graph gauge closes the final `{0,2}` by `{0,2}` cell. |
| `S2CF` + `S2CG` + `S2CJ` | complete diagonal two-visible completion | `S2CK` | The exact two-visible support atlas has fourteen masks.  Four central masks put both transverse targets in one correction-free mixed map, contradicting the split-cubic mixed-map obstruction.  Each of the ten boundary masks has one structural zero pair and two transverse rank-one corners, contradicting the S2CG zero-pair classification and the zero-corner rectangle obstruction. |
| `S2BQ` + `S2BR` + `S2CG` + `S2CK` | arbitrary-nonmonomial zero-pair localization | `S2CL` | Coordinate `w` gives an exact complete three-slice rank-one normal form and a corrected perpendicular-plane cube in the alternating physical three-space.  Structural zeros have an exhaustive at-most-four-point coordinate-shore atlas.  A correcting zero triggers the `P_3` rank fork, a one-colour perfect pairing, coincident split row planes, and a retained-slice quotient that forces the actual residual block monomial. |
| `S2BQ` + `S2CL` + `S2CK` | arbitrary-nonmonomial zero-pair-free completion | `S2CM` | Exhausting the coordinate/noncoordinate shared-factor split turns absence of a structural zero into a correction-free mixed map containing two transverse targets.  In the coordinate branch this holds in both ranks of the exact `2 x 2` residual restriction.  The S2CK mixed-map obstruction excludes all such maps. |
| `S2BQ` + `S2CG` + `S2CI` + `S2CK` + `S2CL` + `S2CM` | noncoordinate actual-nonmonomial structural completion | `S2CN` | A coordinate structural shore gives a one-sided target table.  Independent zero-pair geometry produces an aligned split plane or split source space.  In the dependent case a one-factor slab manufactures a second structural corner and invokes the same two-cross dichotomy.  A retained-face quotient makes the actual residual block monomial in every branch. |
| `S2BQ` + `S2CG` + `S2CI` + `S2CK` + `S2CL` + `S2CM` + `S2CN` | coordinate actual-nonmonomial structural completion | `S2CO` | Root exchange reduces to `x=e_s`.  The `y_s!=0` wall is a complete `2 x 2` cross-zero atlas; the `y_s=0` noncoordinate wall is a map-source zero-pair split; and coordinate `y=e_r` is an exact matrix-rank/pure-pencil census.  Source-factor quotients of retained faces, with only a diagonal coefficient used on the delicate boundary, exclude every case. |
| `S2BR` + polarized-permanent support census | same-colour coordinate split-lift exclusion | `S2BS` | The split-lift four-space has exactly eight independent root-permanent coefficients modulo `U`; target consistency makes their source coefficients a six-zero/two-transverse table.  The new rank-free eight-product obstruction proves that table empty. |
| `S2BR` + complete pure-target coefficient identity | support-one split-lift completion | `S2BT` | On the coordinate third-row-kernel cell, first- and third-root contractions of `T_d` force the missing-colour correction preimage to be vertical modulo the contained syzygy; the `T_s` coefficient supplies a second split vector.  The projection ranks then leave exactly the nonaligned and aligned four-space charts, whose root-product spans are computed exactly. |
| `S2BT` + square-polarization tangent kernel | aligned support-one completion | `S2BU` | The aligned root rows make `ttt` a pure cube-polarization target and force three other dual rows into its two-dimensional tangent kernel via `stt`, `tst`, and `ttd`.  The resulting rank-at-most-three transpose contradicts the four-dimensional joint image. |
| `S2BT` + `S2E` | nonaligned support-one completion | `S2BV` | The deformed eight-product table has one exhaustive independent-row normal form: a same-source two-plane control with monomial `C` and coordinate `w`.  Its three singleton columns give a unique pair lift; the `x_t,y_t` residues cannot both cancel because their equality would identify different pure target monomials.  The Cramer--Euler pair-regularity gate excludes every graph extension. |
| `S2BR` + `S2BV` | same-colour rank-two-third-row completion | `S2BW` | A support-two third-kernel covector makes the two complementary pure-target corrections force two split tangent vectors; together with the vertical missing-colour correction and shared syzygy they fill `K` but leave third projection rank one.  S2BU--S2BV already close support one, so the complete same-colour `(2,2,2)` profile is empty. |
| `S2BR` + `S2BF` + `S2BW` | same-colour involved-row completion | `S2BX` | Injectivity of the third row makes the complete correction one-dimensional; the `P_3` rank obstruction removes its last coefficient and leaves an exact binary frame with common zero `q_d`.  Arbitrary shifts along that zero preserve the frame.  The intersecting-plane obstruction and four-space dimension force `q_d` into two transverse involved planes, closing `(2,2,3)` and hence every same-colour `(2,2,q)` profile. |
| `S2BX` + root exchange | mixed injective-third-row completion | `S2BY` | The one-line correction and shifted binary-frame contradiction use only one deficient involved row.  The other injective row restricts to a binary plane on the complementary colours, excluding `(2,3,3)`; symmetry excludes `(3,2,3)`. |
| `S2BY` + third-kernel contraction | mixed support-two completion | `S2BZ` | With third-row rank two, all non-missing correction preimages lie in a two-plane whose derivative image is one line.  A two-colour third-kernel contraction forces that line onto two independent diagonal root tensors, excluding both mixed orientations. |
| `S2BZ` + cubic resonance tangent separation | mixed support-one completion | `S2CA` | The support-one target corrections force a vertical lift and one projection-compatible split.  Injectivity of the other involved row turns the third-`t` face into a resonant scaling frame.  The missing-colour face then makes the third dual row proportional to the resonant cube row, contradicting injectivity of the four-dimensional physical transpose. |
| `S2CA` + direct-root-box rank fork | fully injective third-row-rank-two completion | `S2CB` | A vertical third direction contradicts the involved projection ranks.  On the nonvertical branch the exact `P_3` rank obstruction kills one supported root representative.  Support one becomes an equal-plane binary frame; support two reduces by outer symmetry to the binary or two-square obstruction. |
| `S2AM` | remaining common-three-space obligation | `S2` | The transverse two-root joint-rank-five branch is closed.  Hilbert--Burch boundaries, joint rank at most four, other S2T component types, other S2Q strata, and every higher order remain open. |
| `S2BE` | remaining common-three-space obligation | `S2` | The complete `(1,1,1)` and `(1,1,2)` Hilbert--Burch profiles and the distinguished `(1,2,2)` `beta_t` and `alpha_s` coloops are closed.  Both residual second-root coloops are localized to four ordered coordinate endpoints but remain open; the three third-root and two complementary first-root coloops, joint rank at most four, other S2T component types, other S2Q strata, and every higher order also remain open. |
| `S2BF` | remaining common-three-space obligation | `S2` | The four residual second-root coloop/endpoint cases now satisfy the exact support table in S2BF but remain open.  The three third-root and two complementary first-root coloops, joint rank at most four, other S2T component types, other S2Q strata, and every higher order also remain open. |
| `S2BG` | remaining common-three-space obligation | `S2` | Residual second-root endpoints with `s=t` are excluded.  The four ordered endpoints with `s in {j,k}` and the S2BF support constraints remain open, as do the three third-root and two complementary first-root coloops, joint rank at most four, other S2T component types, other S2Q strata, and every higher order. |
| `S2BH` | remaining common-three-space obligation | `S2` | Every residual second-root endpoint now has complementary coordinate `x,y` rows, but both possible coordinate locations of `w` remain open with the residual S2BF `z` constraints.  The other five `(1,2,2)` coloop orientations, lower-rank and component branches, pole strata, and higher orders also remain open. |
| `S2BI` | remaining common-three-space obligation | `S2` | Both residual second-root coloops are confined to the terminal chart `y=w=e_u`, `z_s=0`, `z_t!=0`, but that chart is not excluded.  The other five `(1,2,2)` coloop orientations, lower-rank and component branches, pole strata, and higher orders also remain open. |
| `S2BJ` | remaining common-three-space obligation | `S2` | Four of the nine `(1,2,2)` coordinate-coloop orientations are now closed: `beta_t`, `alpha_s`, and both residual `beta_j`.  The three third-root and two complementary first-root coloops, lower-rank and component branches, pole strata, and higher orders remain open. |
| `S2BK` | remaining common-three-space obligation | `S2` | Seven of the nine `(1,2,2)` coordinate-coloop orientations are closed.  Only the two complementary first-root `alpha_a,alpha_b` coloops remain in this profile; lower-rank and component branches, pole strata, and higher orders remain open. |
| `S2BL` | remaining common-three-space obligation | `S2` | All nine `(1,2,2)` coordinate coloops are closed, so the complete joint-rank-five Hilbert--Burch profile is impossible.  Joint rank at most four, other S2T component types, other S2Q pole strata, and every higher order remain open. |
| `S2BM` | remaining common-three-space obligation | `S2` | The lower-rank transverse two-root branch is reduced to four exact cells with sharp local controls.  S2BN, S2BO, and S2BP subsequently close all four at the exclusion or graph-extension level.  Three-root lower-rank cells, other components and pole strata, and higher orders remain open. |
| `S2BN` | remaining common-three-space obligation | `S2` | The complete joint-rank-four transverse `q=2` cell is closed.  S2BO and S2BP subsequently close the rank-three `q=2` graph cell and both remaining `q=1` graph cells.  Lower-rank three-root derivatives, other components and pole strata, and all higher orders remain open. |
| `S2BO` | remaining common-three-space obligation | `S2` | The joint-rank-three `q=2` local equations have sharp controls, but their exhaustive pair lifts fail divisorial regularity, so the complete graph-extension cell is closed.  S2BP subsequently closes both populated `q=1` cells.  Lower-rank three-root derivatives, other components and pole strata, and all higher orders remain open. |
| `S2BP` | remaining common-three-space obligation | `S2` | Every joint-rank-three/four transverse two-root `q=1` point has a prime-divisor pair pole.  Together with S2BN and S2BO, the complete lower-rank transverse two-root graph-extension branch is empty.  S2BQ subsequently localizes the lower-rank three-root derivatives; other components and pole strata and all higher orders remain open. |
| `S2BQ` | remaining common-three-space obligation | `S2` | The lower-rank three-root branch has an exact derivative-rank `9/8/7` census.  Rank four excludes rank nine; rank-eight points lie on the shared-factor coordinate/monomial torus atlas; rank-seven `(2,2,2)` is impossible and the other Hilbert--Burch profiles lie on explicit coordinate atlases.  S2BR--S2CO now close every joint-rank-four/derivative-rank-eight row profile, including all monomial and actual-nonmonomial fully-injective residuals.  Joint-rank-three/rank-eight cells, derivative-rank-seven target and pair cells, components, poles, and higher orders remain open. |
| `S2BR` | remaining common-three-space obligation | `S2` | Every rank-four/rank-eight root row has rank two or three, and the distinct-missing-colour involved `(2,2)` subcell is empty.  S2BT--S2CA close every profile with a deficient involved row, S2CB closes fully injective involved rows with third-row rank two, S2CC--S2CK close all monomial `(3,3,3)` residuals, and S2CL--S2CO close every actual-nonmonomial residual.  Thus the complete joint-rank-four/derivative-rank-eight cell is closed.  Joint-rank-three/rank-eight cells, derivative-rank-seven cells, pair coupling elsewhere, other components and pole strata, and higher orders remain open. |
| `S2BS` | remaining common-three-space obligation | `S2` | The displayed same-missing-colour `(2,2,2)` coordinate split-lift cell is empty for every cross map onto its four-space.  S2BT--S2BW close every rank-two-third-row lift and S2BX closes third-row rank three.  Other involved-row profiles, joint rank three, derivative rank seven, pair coupling elsewhere, and higher orders remain open. |
| `S2BT` | remaining common-three-space obligation | `S2` | The coordinate-third-kernel same-colour `(2,2,2)` four-space is exhaustively split into nonaligned and aligned charts, with no nonsplit missing-colour lift.  S2BU closes the aligned chart, S2BV closes every nonaligned graph extension, S2BW closes support-two kernels, and S2BX closes the rank-three continuation.  Other row profiles, lower-rank cells, other components and poles, and higher orders remain open. |
| `S2BU` | remaining common-three-space obligation | `S2` | The aligned support-one chart is empty uniformly, including monomial `C` and noncoordinate `w`.  S2BV closes the nonaligned chart, S2BW closes support two, and S2BX closes third-row rank three.  Other row profiles, lower-rank cells, other components and poles, and higher orders remain open. |
| `S2BV` | remaining common-three-space obligation | `S2` | Every coordinate-third-kernel same-colour `(2,2,2)` point is excluded at the empty-target or pair-regularity gate.  S2BW closes two-coordinate third-kernel support and S2BX closes the injective-third-row continuation.  Mixed or injective involved rows, joint-rank-three/rank-eight and derivative-rank-seven target cells, other components and pole strata, and higher orders remain open. |
| `S2BW` | remaining common-three-space obligation | `S2` | The complete same-colour involved-row `(2,2)` profile with third-row rank two is closed for both possible kernel supports; S2BX subsequently closes third-row rank three.  Mixed `(2,3)/(3,2)` and injective `(3,3)` involved rows, joint-rank-three/rank-eight and derivative-rank-seven target cells, pair coupling on those cells, other components and poles, and higher orders remain open. |
| `S2BX` | remaining common-three-space obligation | `S2` | The complete same-colour involved-row `(2,2,q)` rank-four/rank-eight profile is closed for `q=2,3`; S2BY subsequently closes mixed profiles with `q=3`.  Mixed third-row-rank-two and injective `(3,3,q)` involved rows, joint-rank-three/rank-eight and derivative-rank-seven target cells, pair coupling on those cells, other components and poles, and higher orders remain open. |
| `S2BY` | remaining common-three-space obligation | `S2` | Every rank-four/rank-eight profile with third-row rank three and at least one deficient involved row is closed; S2BZ and S2CA subsequently close both third-row-rank-two kernel supports in the mixed profiles.  Fully injective involved rows, joint-rank-three/rank-eight and derivative-rank-seven target cells, pair coupling, other components and poles, and higher orders remain open. |
| `S2BZ` | remaining common-three-space obligation | `S2` | Every mixed rank-four/rank-eight profile is closed except the third-row-rank-two support-one cells; S2CA subsequently closes those cells.  Fully injective involved-row profiles, joint-rank-three/rank-eight and derivative-rank-seven target cells, pair coupling, other components and poles, and higher orders remain open. |
| `S2CA` | remaining common-three-space obligation | `S2` | Every rank-four/rank-eight profile having at least one deficient involved row is closed.  S2CB subsequently closes the fully injective `(3,3,2)` profile, S2CC--S2CK close all monomial `(3,3,3)` residuals, and S2CL--S2CO close every actual-nonmonomial residual.  Thus the complete joint-rank-four/derivative-rank-eight cell is closed.  Joint-rank-three/rank-eight and derivative-rank-seven target cells, pair coupling, other components and pole strata, and higher orders remain open. |
| `S2CB` | remaining common-three-space obligation | `S2` | The complete rank-four/rank-eight third-row-rank-two row census is closed.  S2CC--S2CK close all monomial residuals in the remaining fully-injective `(3,3,3)` profile, and S2CL--S2CO close every actual-nonmonomial residual.  Thus the complete joint-rank-four/derivative-rank-eight cell is closed.  Joint-rank-three/rank-eight and derivative-rank-seven target cells, pair coupling, other components and pole strata, and higher orders remain open. |
| `S2CC` | remaining common-three-space obligation | `S2` | Every fully injective `(3,3,3)` monomial residual away from `w_d=w_e=0` is impossible.  S2CE excludes the off-diagonal survivor; S2CD and S2CF reduce each diagonal survivor to an exact visibility split; S2CH, S2CJ, and S2CK exclude its zero-, one-, and two-visible cells.  S2CL--S2CO separately close the complete actual-nonmonomial successor.  Thus the fully-injective joint-rank-four/derivative-rank-eight profile is closed.  Lower-rank cells, components and pole strata, and higher orders remain open. |
| `S2CD` | remaining common-three-space obligation | `S2` | At a diagonal monomial endpoint, `w` must lie on one complementary coordinate line.  S2CF reduces each discrete survivor to sixteen recovered faces and an ordinary tangent-coset rank-one flattening; S2CH, S2CJ, and S2CK exclude the complete zero-, one-, and two-visible cells.  S2CE closes the off-diagonal endpoint, while S2CL--S2CO close every actual-nonmonomial residual.  The fully-injective joint-rank-four/derivative-rank-eight profile is closed.  Lower-rank target cells, pair coupling, components and pole strata, and higher orders remain open. |
| `S2CE` | remaining common-three-space obligation | `S2` | Every off-diagonal monomial endpoint is impossible.  S2CK closes the last two-visible cells at the discrete diagonal endpoints left by S2CD and reduced by S2CF, completing the monomial residual branch together with S2CH and S2CJ.  S2CL--S2CO close every actual-nonmonomial residual.  The fully-injective joint-rank-four/derivative-rank-eight profile is closed.  Lower-rank target cells, pair-coupling obligations, components and pole strata, and higher orders remain open. |
| `S2CF` | remaining common-three-space obligation | `S2` | The full target on each diagonal coordinate endpoint is exactly sixteen recovered face equations plus a nonzero root factor in an affine tangent coset and its rank-one source flattening.  Its corrected cube is a useful consequence but not a converse.  S2CH, S2CJ, and S2CK exclude every zero-, one-, and two-visible cell, while S2CL--S2CO close the actual-nonmonomial successor.  The fully-injective joint-rank-four/derivative-rank-eight profile is closed.  Lower-rank cells, pair coupling, components, poles, and higher orders remain open. |
| `S2CG` | remaining common-three-space obligation | `S2` | The common-coordinate/complementary-diagonal binomial nonmonomial orbit is empty for every nonzero coefficient ratio.  Its general zero-pair/radical geometry supports S2CH--S2CO; S2CL excludes correcting zero pairs, S2CM excludes the zero-pair-free successor, S2CN excludes both-noncoordinate structural points, and S2CO excludes every coordinate-shared-factor structural cell.  Together with the monomial chain, the fully-injective joint-rank-four/derivative-rank-eight profile is closed.  Lower-rank cells, pair coupling, components, poles, and higher orders remain open. |
| `S2CH` | remaining common-three-space obligation | `S2` | Neither diagonal coordinate endpoint can lie on the zero-visible wall; S2CJ and S2CK subsequently exclude the one-visible and two-visible cells, while S2CL--S2CO close the actual-nonmonomial successor.  The fully-injective joint-rank-four/derivative-rank-eight profile is closed.  Lower-rank cells, pair coupling, components, poles, and higher orders remain open. |
| `S2CI` | remaining common-three-space obligation | `S2` | The same-coordinate one-visible cells `x=y=e_0,e_1` are empty; S2CJ exhausts every other one-visible support mask and S2CK closes the two-visible successor.  Its two-cross incidence dichotomy also feeds S2CN--S2CO, completing the actual-nonmonomial branch.  The fully-injective joint-rank-four/derivative-rank-eight profile is closed.  Lower-rank cells, pair coupling, components, poles, and higher orders remain open. |
| `S2CJ` | remaining common-three-space obligation | `S2` | Every one-visible support mask at the diagonal monomial coordinate endpoints is impossible, and S2CK closes the remaining two-visible cell.  S2CL--S2CO close every actual-nonmonomial residual.  The fully-injective joint-rank-four/derivative-rank-eight profile is closed.  Lower-rank cells, pair coupling, components, poles, higher orders, and all-rank drop remain open. |
| `S2CK` | remaining common-three-space obligation | `S2` | Every two-visible support mask at the diagonal monomial coordinate endpoints is impossible.  Together with S2CH, S2CJ, and S2CE, this closes the complete monomial-residual branch.  Its mixed-map and zero-corner lemmas feed S2CL--S2CO, which close every actual-nonmonomial successor.  The fully-injective joint-rank-four/derivative-rank-eight profile is closed.  Lower-rank cells, pair coupling, components, poles, higher orders, and all-rank drop remain open. |
| `S2CL` | remaining common-three-space obligation | `S2` | In the fully-injective rank-four/rank-eight actual-nonmonomial branch, the complete target has an exact three-slice rank-one normal form.  Correcting zeros are impossible; S2CM excludes the zero-pair-free cell, S2CN excludes both-noncoordinate structural points, and S2CO excludes every coordinate-shared-factor structural point.  Thus the complete actual-nonmonomial residual branch is closed.  Joint-rank-three/rank-eight and derivative-rank-seven cells, pair coupling elsewhere, other components and poles, higher orders, and all-rank drop remain open. |
| `S2CM` | remaining common-three-space obligation | `S2` | The zero-pair-free fully-injective rank-four/rank-eight actual-nonmonomial cell is empty.  S2CN and S2CO subsequently exclude every structural successor, so the complete actual-nonmonomial residual branch is closed.  Joint-rank-three/rank-eight and derivative-rank-seven cells, pair coupling elsewhere, other components and poles, higher orders, and all-rank drop remain open. |
| `S2CN` | remaining common-three-space obligation | `S2` | Every fully-injective rank-four/rank-eight actual-nonmonomial structural point with both shared factors noncoordinate is impossible.  S2CO excludes the coordinate-shared-factor successor, completing the actual-nonmonomial residual branch.  Joint-rank-three/rank-eight and derivative-rank-seven cells, pair coupling elsewhere, other components and poles, higher orders, and all-rank drop remain open. |
| `S2CO` | remaining common-three-space obligation | `S2` | Every fully-injective rank-four/rank-eight actual-nonmonomial structural point with coordinate `x` or coordinate `y` is impossible.  With S2CL--S2CN, this closes the complete actual-nonmonomial residual branch; with S2CC--S2CK, it closes the fully-injective `(3,3,3)` profile and hence the complete joint-rank-four/derivative-rank-eight cell.  Joint-rank-three/rank-eight and derivative-rank-seven cells, pair coupling elsewhere, other components and poles, higher orders, and all-rank drop remain open. |
| `S2T` | boundary-annihilator obligation | `S2` | Multi-coordinate, `beta=0`, and collapsed cross-column components remain to be coupled to full sensor rank and all uncontracted target equations.  Rank-one and pair-plane pole strata and every higher order also remain open. |
| `S1` | boundary obligation | `S3` | The all-balanced rank-drop branch is not excluded on the witness locus. |
| `S3` | refutation of argument | `S3D` | Local concision, complete support, invertible blocks, and the pure target coefficients do not force any balanced sensor to have full rank; mixed-word zeros are essential. |
| `S3` | exact stratum exclusion | `S3Q` | Simultaneously vertex-gauge-equivalent common symmetric edge forms are all-rank-drop from `n=8` onward, but flattening rank excludes their entire local-GL orbit from the ternary witness locus; no synchronization theorem for arbitrary `B_all` is inferred. |
| `S1` | conditional stratum obstruction | `S3P` | A common root diagonal quadric makes the all-cross permanent the complete residue modulo `Q`; nonconstant words give zero and constant words give pure-root products.  The two scalar-permanent cases exclude a physical common-conformal shore, but no universal common-quadric or conformal extraction is inferred. |
| `S3Q` | strict special case | `S3P` | The fully synchronized common-quadratic orbit has column-separable cross scalars all equal to one; the newer shore theorem allows arbitrary internal nonroot blocks and varying root/cross scalars and also closes zero permanent by a pure word. |
| `S3P` | exact proof-DAG bridge | `S3B` | A point on the common nondegenerate conic avoids the finite target-coordinate line arrangement, producing a fully supported balanced root half.  The already proved zero-surplus extraction gives `P_m -> Delta_3`; `P_3` rank and `P_4` subrank exclude `m=3,4`, while `m>=5` remains at PR. |
| `S3B` | exact fixed-gauge sharpness | `S3` | All-cut rank drop, invertible blocks, local concision, and normalized pure coefficients do not force a projective basepoint for the same-vector root quadrics in a prescribed gauge.  The control is latently common-quadratic, so existential multiroot synchronization remains open. |
| `G0` | eight-vertex mixed-slice specialization | `S3C` | On each five-set, every matching in a complement-colour slice contains an internal five-set edge, while the target slice is one colour product.  Existing five-root nonemptiness plus projective incidence yields the codimension-at-least-three necessary envelope. |
| `S3C` | exact adjacent-pair overlap refinement | `S3CA` | For one fixed adjacent pair, exact common-root synchronization accounts for the shared `K_4` evaluations and improves the necessary coefficient envelope from codimension at least three per five-set to codimension at least five for the pair. |
| `S3CA` | exact all-balanced affine dimension refinement | `S3CB` | The all-balanced maximal-minor locus cuts every dimension-`247` equality source properly, giving ambient codimension at least six in the full affine block space; a rank-seven common-quadratic fixture shows the cut is nonempty. |
| `S3CB` | four-chart pencil rank correction | `S3CC` | The proposed `15^4` Bell-partition lift used partition-pair cardinality in place of tensor-span rank.  An exact feasible stratum exposes a codimension-eight local incidence image, so the codimension-nine/ten promotion is withdrawn. |
| `S3CC` | corrected finite support-Segre rank census | `S3CCD` | The actual generic support-Segre ranks are enumerated over every canonical selector/partition stratum.  The exact finite result is `q>=20`, with exactly two equality orbits and generic affine codimension at least eight; rank-degenerate pieces are not included. |
| `S3CCD` | unresolved rank-degeneracy and four-pencil gluing obligation | `S3` | Prove the missing `Delta+sum(r_ij)+c_rank>=20` bound on rank-degenerate components, decide the `B_all` cut, and attach compatible conditions across the `70` pencils.  Full target equations and witness exclusion remain separate. |
| `S3CC` | unresolved corrected pencil compatibility obligation | `S3` | The four-chart rank boundary is not a witness or global counterexample.  Actual span-rank stratification, its `B_all` intersection, the `70`-pencil compatibility problem, remaining mixed equations, and witness exclusion remain open. |
| `S3` | refutation of prescribed-gauge extraction | `S3H` | Two adjacent all-rank-drop shores, nonzero pure coefficients, and the complete Hamming-one shell do not force compatible same-vector basepoints.  Four pair-local Hamming-two equations detect the monomial synchronized control class only. |
| `G0` | reduction | `M1` | Maximum-cardinality torus roots give a pointwise exhaustive split. |
| `M1` | case coverage | `M2`, `U1` | The two cases are `r>=2` and `r=1`; neither is excluded by the split. |
| `S1` + `M2` | mathematical premises | `O1` | Rebalancing the fixed layer exposes a truncated contracted sensor. |
| `O1` | residual refinement | `O2` | A second open root gives the exact next detector equation. |
| `O2` | specialization | `O2P` | If the outside two-row factorization is aligned with root `j` and its open shore is projectively constant, the whole single-open equation lifts the fixed `P_m` layer to `P_(m+1)`. |
| `O2P` | reduction | `PR` | The synchronized projective branch is reduced to the same arbitrary weighted-permanent restriction family; no permanent nonrestriction theorem is inferred. |
| `O2P` | conditional cell closure | `O2M` | The repeated-row Hall quotas and adjacent pure/mixed equations close row-replacement vanishing only in the minimum `q=0,r=3` cell; they do not exclude a witness there. |
| `O2P` | conditional cell closure | `O2T` | In `q=0,r=4`, local `a/b` transversality plus a surviving companion basis forces at least one nonzero row-replacement detector; transversality is not derived and no witness is excluded. |
| `O2P` | conditional cell closure | `O2F` | Collision quotients, Hall incidence, recolouring, and local concision close every local-dependence boundary in aligned projective `q=0,r=4`; no witness is excluded. |
| `O2P` | conditional stratum detector | `O2V` | In `q=0,r=5`, the collective companion matrix and deletion activity force at least one nonzero detector away from the two classified companion exceptions; neither activity nor good companions is universal. |
| `O2P` | conditional stratum detector | `O2A` | In locally transverse `q=0,r=5`, pair-collision injectivity and the companion zero-edge lemma cover every companion frame when at most one root has quotient support at most one. |
| `O2P` | conditional cell closure | `O2C` | In locally transverse `q=0,r=5`, weak-root trapping and the exhaustive companion split close every root quotient-support pattern; no witness is excluded. |
| `O2P` | conditional stratum closure | `O2D` | In `q=0,r=5`, rank-one quotient trapping and a retained four-mode inverse close one arbitrary local defect, or two defects with a regular member; no witness is excluded. |
| `O2T` | strict special case | `O2F` | The earlier local-transversality proof remains valid but its extra hypothesis is no longer needed for four-cell detection. |
| `O2V` | strict overlapping stratum | `O2C` | Good companion frames with deletion activity are a strict subcase of the complete locally transverse five-cell detector. |
| `O2A` | strict overlapping stratum | `O2C` | Frames with at most one quotient-sparse root are a strict subcase of the complete locally transverse five-cell detector. |
| `O2C` | strict special stratum | `O2D` | The defect-free five-cell is the locally transverse subcase of the enlarged one-defect/regular-two-defect detector region. |
| `O2D` | strict special strata | `O2E` | The previously detected transverse, one-defect, and regular-two-defect strata sit inside the enlarged at-most-two-defect region; exact three-activity and `A/B/Z` collision kernels add `AB`, `AZ`, `BZ`, and `ZZ`, but not `AA` or `BB`. |
| `O2E` | strict special strata | `O2G` | The mixed and zero-containing two-defect cells sit inside the complete at-most-two-defect detector region; exact pair/triple incidence and pure-support matching add the same-type `AA` and `BB` cells. |
| `O2G` | strict special strata | `O2H` | The complete at-most-two-defect region sits inside the enlarged at-most-three-defect region; fixed-layer incidence excludes `A/Z`, while exact `R/B` common kernels add `RRR`, `RRB`, `RBB`, and `BBB`. |
| `O2H` | remaining-strata closure | `O2I` | The lifted `p_a>=2` row quota removes four/five `B` words; exact four-/five-defect kernels, reciprocal forcing, and the `3|2` Hall bridge add all remaining `R/B` words.  The conclusion is complete conditional detection, not witness exclusion. |
| `O2F` | boundary obligation | `O3` | Four-cell closure does not automatically transport to larger aligned cells, positive surplus, or the unfactorized branch. |
| `O2I` | boundary obligation | `O3` | Complete aligned `q=0,r=5` detection neither excludes a witness nor transports automatically to larger aligned cells, positive surplus, or the unfactorized branch. |
| `O2` | boundary obligation | `O3` | The tight star refutes an automatic detector; higher/unfactorized data are needed. |
| `M2` | specialization | `PR` | Zero surplus yields a tight weighted permanent restriction at arbitrary `r>=5`; it is not reduced to P7. |
| `PR` | necessary condition | `PRC` | Every co-two pair product space has dimension at least five, and every complementary sensor has corank at least two.  For P6 all fifteen four-mode sensors have rank at most thirteen, but simultaneous corank two plus local rank and pure nonvanishing is insufficient. |
| `PRC` | exact `P_6` equality-five branch | `PR5` | Product dimension five forces active support four; the complete based-frame orbit cover and six reviewed endpoints exclude every full-extension class.  The branch is closed for `P_6`, not for arbitrary order. |
| `PRC` | remaining `P_6` boundary branch | `PR6` | Every hypothetical `P_6` restriction is now forced to product dimension at least six at all fifteen omitted pairs, with sensor rank at most twelve.  Equality six already has positive-dimensional pair-level moduli, so the remaining obligation is the factored four-mode and simultaneous mixed-target incidence rather than a finite endpoint list. |
| `PR6` | exact common-factor target compression / boundary | `PRT` | After six labelled local planes are synchronized, five spanning-tree mixed radicals are equivalent to all mixed target equations.  Product-space overlap identities are necessary but insufficient: a common equality-six/all-rank-drop model passes them and still has a nonzero mixed coefficient.  Identifying the common factors and excluding the five radical conditions remain open. |
| `U1` | reduction | `U2` | Matrix-unit cancellation reduces to an at-most-four-port response. |
| `U1` | exact support-minimal refinement | `U1B` | The strict incidence alternative turns every absent positive endpoint balance into an integral GHZ-preserving degeneration that erases a physical edge; global support minimality therefore forces the balance. |
| `U1B` | exact complex-analytic refinement | `U1C` | Strict all-edge balance makes the squared-amplitude exponential functional coercive and strictly convex on the positive GHZ torus modulo its edgewise stabilizer; its unique critical orbit has actual vertex-independent colour loads. |
| `U2` | specialization | `U3` | Only the globally rigid-colour cell enters the deletion-deck factorization. |
| `U3` | mathematical premise | `U4` | Rigid factorization yields the primitive and dual bridges. |
| `U4` | refutation of argument | `U5` | The primitive alone cannot close arbitrary order. |
| `U1` + `U2` | mathematical premises | `U6` | Parity and bridge structure refine the one-root branch. |
| `U6` | reduction | `M2` | Exact erasure may produce a different realization with at least two roots. |
| `U6` | exact refinement | `U7A` | Target equality factors every diagonal word fibre over its pure shores and synchronizes every nonzero aggregate offdiagonal coordinate; internally zero fibres may still contain unsynchronized terms. |
| `U7A` | exact refinement | `U7B` | The complete cross-matching response selects a cofactor-active physical term and bridge-normalizes its parity core, giving the deeper/transport/pure-cancellation trichotomy and finite no-exit holonomy. |
| `U7B` | exact phase refinement | `U7C` | A finite active cycle produces a nonzero endpoint-character circulation; complete binomial fibres impose one Laurent holonomy equation, while aggregate fibres remain explicit. A least supported pure cancellation has a spanning conserved cofactor flow and therefore branches or forms alternating even cycles. |
| `U7C` | exact aggregate-cycle refinement | `U7J` | Complete aggregate cycle equations factor holonomy through gauge-invariant extra-term defects. A split aggregate can retain the binomial sign, while an exact complete physical family shows the cycle subsystem can have zero holonomy elimination. |
| `U7C` | exact pure-cofactor refinement | `U7H` | Minimality identifies the active flow with the connected allowed-edge core. Degree two is one primitive binomial cycle; branching is a connected matching-covered multi-cycle exchange core with quantified excess. |
| `U7H` | exact branch-port refinement | `U7I` | Perfect matchings partition into nonzero cofactor ports. Singleton ports form a conformal alternating fan and an exact sparse Laurent sum; otherwise an aggregate port is forced. Every pair of branch exits carries one of two exact conformal theta profiles. |
| `U7I` | boundary obligation | `U7` | Arbitrary-arity sparse fans, both cubic theta profiles, and aggregate ports all occur in least characteristic-zero pure residuals. Exclusion therefore needs mixed coupling, aggregate control, or genuine deeper-blocker incidence absent from pure topology alone. |
| `U7J` + `U7I` | exact attachment refinement | `U7K` | An offdiagonal aggregate extra either embeds a conformally minimal primitive cycle/fan/aggregate port termwise in mixed response, enters deeper data, or activates its bridge target. Shortest-cycle minimality reduces the last case to an outside word or a parallel successor. |
| `U7J` + `U7A` | exact diagonal-excess refinement | `U7L` | Diagonal fibres factor as Cartesian shore products with disjoint-support shore lattices. Aggregate size forces one primitive shore exchange, while diagonal extras create no bridge arc and the full shore hafnians remain nonzero. |
| `U7K` | boundary obligation | `U7` | Parallel bridge reuse can have zero successor-fibre difference even with all pure coefficients one. Conversion of attached relations into units, forced non-direct overlap, and killed quotient sheets remain open. |
| `U7L` | boundary obligation | `U7` | A unique shortest diagonal-aggregate cycle with all pure anchors can have a saturated direct fibre-lattice sum, no integer dependency, and freely varying holonomy. Closure needs another target equation, a forced proper-subshore cancellation, a unit, or a separately proved deeper exit. |
| `U7K` | exact exit | `D1` | Any selected bridge square or hexagon for the aggregate extra may enter the existing deeper-blocker component. |
| `U7C` | boundary obligation | `U7` | The Laurent holonomy can take the required odd sign and aggregate fibres retain additional summands. The pure-cofactor side is now refined through `U7I`, but further mixed or deeper equations are still needed. |
| `U1C` + `U7C` | refutation of stronger argument | `U7D` | Complete physical support, all pure target coordinates, strict endpoint balance, the actual moment gauge, and three proper nonrigidity sets coexist with an exact odd binomial cycle. The same table has an exposed nonzero mixed coefficient, so only the shortcut is refuted. |
| `U7C` + complete target block | exact lattice reduction | `U7E` | Every normalized fibre lies in the within-fibre difference group algebra. Faithful Laurent extension preserves units and holonomy elimination; singleton and all-binomial blocks are decided exactly by unit/parity alternatives. |
| `U7D` | fixed-template specialization | `U7E` | The complete `(4,4,0)` block lands in the universal singleton branch because it contains ten singleton monomials. Its three-binomial subsystem is parity-consistent and gives only `(H+1)`, while the singleton enlarges the complete block to `(1)`. |
| `U7E` + parity-consistent active binomial cycle | exact aggregate quotient | `U7F` | Untwisting the selected core gives `C[L/L_B]`; finite Fourier sheets and Laurent gcds completely decide residual ideals in quotient free ranks zero and one. |
| `U7E` | boundary obligation | `U7` | The universal reduction does not force a singleton, odd relation, or fully binomial active cycle from response data. Aggregate cycle fibres remain outside the selected binomial-core quotient. |
| `U7F` | boundary obligation | `U7` | The quotient theorem does not force free rank at most one or kill every low-rank sheet; free rank at least two remains multivariate. A continuation must close one of those exact residuals, couple another multidegree, or enter the pure/deeper topology. |
| `U7B` | boundary obligation | `D1` | Any selected square or hexagon may enter the existing deeper-blocker alternative. |
| `U1C` + `U7C` | compatible normal forms | `U7`, `D1` | Moment gauge leaves the active-cycle Laurent monomial invariant and multiplies every cofactor-flow edge on one pure residual by a common nonzero scalar. Magnitude balance and the phase normal forms therefore hold simultaneously, but neither closes the deeper or phase exits. |
| `U2` | boundary obligation | `U8` | Full flags have consequences, but proper nonempty flag sets remain. |
| `U2`, `U6` | boundary obligation | `D1` | Both reductions retain the deeper-blocker alternative. |
| `U2` | specialization | `A1` | Simultaneous full flags for all colours enter all-bridge, absent deeper blockers. |
| `A1` | support-density and degree-five cut refinement | `A2` | Three off-diagonal killers lift `Delta(D)>=5` to full-support `Delta(G)>=8`. At degree five, active-deck and mixed-cut identities localize a supported pure cancellation to an inactive-edge complement, selected-pair component/complement, or Hamiltonian chord-arc/complement cut. Independently, the universal least pure core becomes bipartite subcubic with the cycle/theta/higher-rank split. |
| `A2`, `U7I` | all-degree quantifier and port/core specialization | `A3` | The unconditional lower bound `Delta(D)>=5` makes every selected active-matching triple leave residual saturated support, so the component/Hamiltonian-chord localization needs no upper-degree bound. Saturated bit flips make every least core bipartite; shore excess and the perfect-matching polytope refine U7I's port partition and two theta profiles to the rank-two closed theta and aggregate-port boundary. |
| `U7H`, `U7I`, `A2`, `A3` | extremal sparse opposite-shore refinement | `A4` | Matching-coveredness makes the nontrivial least core 2-connected; A3's shore excess and equality `d=N=beta+1` exhaust one shore; U7I's nonzero port partition forces aggregate ports at every lower-degree opposite site; A2 supplies only the pointwise `deg_G>=deg_D+3` landing.  Neither sparse-shore alternative is excluded. |
| `A4`, `U7I` | exact rank-three route-port refinement | `A5` | A4 supplies the `Q/Q` or `Q/C^2` route kernel, its parities, and `N=4`; U7I supplies the nonzero edge-inclusive port sums.  Their composition pairs odd-route singleton ports and makes the unique `Q/C^2` even-route ports complementary nonzero doubletons with exact-negative sums.  No mixed-target attachment, independence, or kernel exclusion follows. |
| `A3`, `A5`, `U7A`, `U7K` | conditional fixed-completion mixed-fibre composition | `A6` | A3 makes the four core matching exponents an affine rank-three simplex; A5 supplies the exact route-port blocks; U7K supplies exponent-preserving termwise injection under the explicitly assumed common completion; and U7A supplies the complete mixed zero-target coefficient.  The result is a rank-three four-term zero block and a no-five fibre census, not completion existence or an exclusion. |
| `A6` | boundary obligation | `U7` | Force a compatible fixed completion, or control the resulting complete-fibre ideal of difference rank at least three.  The complement may be empty, `1+X+Y+Z` is a proper nonunit, and the three exponent differences have no nonzero integer dependency, so neither a unit nor an odd dependency follows from the block alone. |
| `A6`, `U7F` | conditional binomial-sublattice sign refinement | `A7` | Integral containment of the A6 difference lattice makes the block a single fixed sign-character scalar before the U7F torsion-sheet split.  Imbalanced restrictions are global units.  Balanced `Q/C^2` is further filtered by its nonzero exact-negative doubletons; `Q/Q` has no doubleton filter. |
| `A5`, `A6`, `A7`, `U7E`, `U7F` | sparse-port primitive-lattice and comparison-graph refinement | `A8` | The sparse-port identity minor makes the A6 lattice primitive, so exact complete-fibre rank three collapses to equality.  Under A7 containment a survivor has even fibre size.  Any physical comparison already landing in that lattice becomes one port-pair edge, and the exact balanced-cut graph criterion identifies the Q/C^2 and uniform Q/Q closures.  Rank equality, containment, and the comparison carriers remain assumptions. |
| `A8` | boundary obligation | `U7` | Force the fixed completion, exact rank three, integral containment, and a useful comparison carrier; otherwise control the rank-at-least-four or uncontained fibre ideal.  The aligned `Q/C^2` survivor and all three possible balanced `Q/Q` restrictions remain live when their required comparison graphs are absent. |
| `A3`, `U7I` | exact complementary-shore response and portal refinement | `A3R` | Every allowed least-core edge exposes a nonzero deletion cofactor, so the mixed-cut identity forces two opposite-colour response zeros.  A supported response obeys the global size bound and attaches a conformally minimal cycle/fan/aggregate relation; otherwise it is an exact support obstruction.  Same-colour conformal failure gives a minimum-crossing portal obstruction family. |
| `A3R` | boundary obligation | `U7` | The response family does not force any response shore to be supported, any opposite-colour active neighbour to be exterior, or any two-portal pair to be allowed.  Its cancelling mixed-fibre subrelations and finite portal obstructions still require non-direct target-lattice coupling, a unit, or a genuine deeper exit. |
| `PR` | specialization | `P5`, `P7` | These are two separately developed local lanes. The still-open `r=6` / P6 restriction remains in `PR`, and arbitrary `r>=8` is not reduced to any of these ranks. |
| `P5`, `P7` | open gluing obligation | `GL` | Even complete local exclusions require a theorem connecting every global witness to them. |
| `M2` | uncontracted surplus-two refinement | `GLS2` | Opening all root slots grades the same outside principal deck by root--root matching number.  At surplus two the target sees every nonempty even label; full companion rank, pair-label observability, or fixed-`Q` observability legally reconstructs the corresponding same-graph data.  At surplus at least four the low `q=2` anchors are absent from all linear root words. |
| `GLS2` | conditional paired-window supply | `GLQ2` | A `Q`-observable surplus-two sensor reconstructs the full block-polarized residual-absent/present response from one graph.  GLQ2 applies only if the chosen overlaps additionally contain three cross-observed rank-two port groups. |
| `GLS2` | maximal-root incidence and physical-secant refinement | `GLS3` | The blocker corank bound forces some raw two-residual pair companion to be nonzero, but pair supply is the quotient-column condition.  A rational sensor kernel need not integrate physically; the exact matching-secant equations decide that issue. |
| `GLS3` | complete contracted mixed-target refinement | `GLS4` | Root evaluation kills every order-four-and-higher companion, while the complete outside target and the corank-six quota exclude the only all-failure rank-one triangle.  Thus one same physical pair has individual quotient survival and nonzero raw incidence.  This does not make any multi-column sensor injective or attach a target selector. |
| `GLS4` | exact failure-topology refinement | `GLS5` | Pointwise selector absorption is compressed by geometric radical Fitting profiles, while GLS2 supply failure remains a distinct outside-function-field projected-kernel condition.  Unrestricted recovery differs from a legal decomposable selector by an exact quotient class; a maximal-rank rational model proves that abstract ranks cannot close the bridge. |
| `GLS4` | common-contraction refinement | `GLS6` | Nonzero `H_Q` and nonzero raw `p_(A,Q)` are nonzero polynomials on the same residual torus, so one fully supported point retains both.  At four roots the ambient and legal-subspace augmented-alignment failures have exact annihilator/rank descriptions, but the physical legal-weight space and response package are not supplied. |
| `GLS4`, `GLS5`, `GLD13` | four-root source integration | `GLS7` | Every root-order-four source point lies in `{O,C} x {R,E,A}`.  The whole E branch retains GLS4 individual survival modulo higher columns and adds seven legal nonzero same-`Q` GLD5/7 attachments; O additionally separates `Q` from the other order-two columns.  Response-zero, generic absorption, and exceptional-fibre leaves remain unexcluded. |
| `GLS7` | conditional legal seven-row attachment | `GLD3` | Both `O x E` and `C x E` supply the same-graph pair block and the six pair plus four-port response selectors on one residual contraction.  GLD3 activity and downstream target contradiction remain separate. |
| `GLS4`, `GLS5`, `GLS6`, `GLS7` | arbitrary-root promoted one-row reduction | `GLS8` | Re-rooting at the GLS4 probe pair gives, for every `r>=3`, a top-minus-two/top fixed-`Q` target module.  A desired coefficient survives the unique higher grade, while exact radical--Fitting profiles decide whether any legal nonzero row exists at any residual contraction.  For the standard four-root module this replaces the coarse per-target R/A wording by simultaneous failure of every target for every eligible `Q`; GLS7 E remains the stronger seven-row GLD3 edge. |
| `GLS4`, `GLS8` | source-aligned promoted base quotient | `GLS20` | Contracting the two GLS8 probe-root coefficient slots at their maximum roots maps the complete nuisance to a nine-dimensional base nuisance.  A surviving base class gives a legal factor-through selector, while the GLS4 Laplace identity makes simultaneous base absorption an explicit nonzero source circuit.  Complete-target usefulness is exactly base survival plus nonzero physical response on every rank fibre. |
| `GLS8`, `GLS20` | all-port nuisance route audit | `GLS21` | The retained same-grade `D=Q` label acts as `G_Q^A(z_Q) tensor id_(W_Uhat)`.  Maximum-root contraction gives `p_(A,Q)id`; its target-factor coefficient slices are `pI_9`.  Hence the entire source-aligned base quotient vanishes on `D(p)`, closing that factor-through route as a no-go while leaving the full upstairs quotient open. |
| `GLS8`, `GLS21` | exact all-port-line quotient | `GLS22` | The operator `P_Q=pI-q tensor epsilon_A` has kernel `Kq` and image `ker epsilon_A` on `D(p)`.  Since `q tensor V_C^*` is contained in the complete nuisance, it reduces every full GLS8 legal-selector quotient equivalently to `72` or `8` transverse rows, with the complete target and all rank drops preserved. |
| `GLS8`, `GLS22` | physical transverse nuisance expansion | `GLS23` | Each labelled companion term is a fixed projected coefficient tensor times an identity on its missing promoted ports.  Splitting its complement pair across the target gives the exact coefficient-slice space.  The top term supplies one common pair-target anchor line and the desired top tensor, yielding the zero/nonzero anchor dichotomy. |
| `GLS23`, `GLD3` | common-anchor one-probe marginal reduction | `GLS24` | A nonzero partial contraction of the common top anchor turns one probe-root contraction into a canonical exterior quotient.  Its exact image has nine pair-complement rows.  At `r=3`, simultaneous marginal usefulness, top usefulness, and the pre-existing activity gate supply the exact legally attached pair/four-port window of `GLD3`. |
| `GLS22`, `GLS24`, `GLD3` | double-transverse core continuation | `GLS25` | The all-port tensor supplies normalized complement lines to the two root annihilators.  The resulting scaled projector has the exact four-dimensional double core as image; wedging by the nonzero core anchor gives three root rows.  At `r=3`, simultaneous `27/4`-row usefulness plus activity supplies the same exact `GLD3` window. |
| `GLS22`, `GLS23` | zero-anchor complete-target reconstruction | `GLS26` | With `omega=0`, the top-target desired side vanishes.  Independence of the three pure promoted-port words therefore puts every projected pure diagonal root tensor into the exact remaining top nuisance.  Splitting its labels by intersection with `Q` separates one-residual tangent slices from genuine promoted pair-label slices. |
| `GLS26` | residual-shore projective faithfulness test | `GLS26` | The one-residual slices lie in `P_Q(T_Q)`, where `T_Q=X_0 tensor V_1^*+V_0^* tensor X_1` and `dim P_Q(T_Q)<=7`.  The diagonal defect outside this tangent is nonzero exactly off the coordinate-shore cover `e_(a_0,c)^* in X_0 or e_(a_1,c)^* in X_1` for every colour; any nonzero defect forces an essential raw promoted pair slice. |
| `GLS26`, `GLS4` | residual-family generic escape or fixed cover | `GLS27` | Function-field rank and augmented-minor tests produce a principal open on which a missing colour remains absent from both shores, or a fixed colour-to-shore cover persists.  The latter has only `C12`, `C21`, and `C22` generic normal forms; all individual rank-drop fibres remain part of the family but cannot obstruct choosing the declared open contraction. |
| `GLS22`, `GLS23`, `GLS26`, `GLS27` | zero-anchor foreign-supplier target envelope | `GLS28` | The exact GLS23 label slices put one-residual nuisance in `P_Q(T_Q)` and every other promoted pair contribution in that supplier's root support.  With the top anchor zero, root separation gives a full legal selector, and separation of a projected pure diagonal gives the named nonzero response through GLS22 target coupling.  Failure leaves a deletion-stable diagonal cover in a quotient of dimension at most four. |
| `GLS22`, `GLS23`, `GLS26`, `GLS28` | rank-two-shore normal-channel continuation | `GLS29` | When both shore ranks are two, the product shore normal is the exact dual of `E/P_Q(T_Q)`.  It gives a two-channel factorization of every supplier, an exact cylinder image of every target nuisance, and a complete mixed-response identity.  Coordinate-annihilator contractions exclude intersecting full-activity support at arbitrary root order and every full-activity local-rank fibre at `r=3`. |
| `GLS29` | normal-product divisor kernel continuation | `GLS30` | Complement-kernel contraction isolates one supplier without division at arbitrary root order.  For four ports it gives exact one- and two-active kernel profiles, including silent zero-star fibres.  Same-graph controls show that the scalar normal identity plus response nonvanishing and normal-image fullness do not exclude the divisor; a separate maximum-root/pure-normalized control shows those graph-side gates do not upgrade the scalar identity to a witness.  GLS31 audits their combined static coupling. |
| `GLS2` | original fixed-Q physical pair-companion exchange | `GLS15` | For every pair target in the original `r`-root, `r`-port fixed-`Q` chart, the residual-absent and residual-present desired columns are the same partial-matching transform applied respectively to the effective residual root-pair array `K^Q` and the actual root-edge array `R`.  This is pointwise on every incidence-rank fibre and uses no support atlas.  It is not the distinct two-root, `2r-2`-port promoted module of GLS8. |
| `GLD15` | rank-one physical quotient-kernel refinement | `GLS15` | A projective operator line `K(delta,eta)` is equivalent to nuisance absorption of `Psi_C(delta R-eta K^Q)`.  Cross-applying another target's absorbed direction gives exactly the projective determinant times the local quotient generator and, on a witness, the corresponding denominator-free pure-target identity. |
| `GLS2`, `GLS15` | maximum-root base-grade quotient shadow | `GLS16` | Root evaluation sends the pair `M` column to the fixed-`Q` complementary permanent and kills the pair `Z` column.  The complete joint nuisance maps to every other order-two coefficient slice.  Hence base survival excludes `k=0` and forces a rank-one line to be pure `M`; any oblique/pure-`Z` line or `k=0` target supplies an explicit swallowed base circuit. |
| `GLD15`, `GLS15` | foreign-label coefficient comparison | `GLS16` | Restricting a legal target-`T` operator identity to the labels `S` and `Q union S` proves that both physical `S` columns have zero cross-contraction from `S-T` to `T-S`.  This does not imply membership in `N_S^J`, which is tested by the differently typed `S`-selector dual. |
| `GLS16` | conditional pure-M pair synchronization interface | `GLD16` | If every required pair base class survives and every pair joint space has rank one, all pair rows share the pure-`M` line without choosing a denominator.  GLD16 entry still requires the four-port line to agree and the selected package to satisfy the declared three-colour activity. |
| `GLS2`, `GLD15` | all-even-target partial-root grade filtration | `GLS17` | For `|S|=2t`, leaving `t-1` roots open kills the residual-present grade `t` column and every higher grade.  The residual-absent grade `t-1` column becomes the explicit injection/permanent leading tensor, while the complete nuisance shadow retains every other label through order `2t`.  Leading survival forces the exact pure-`M` coefficient row. |
| `GLS16` | pair specialization and finite-family refinement | `GLS17` | The `t=1` leading class is GLS16's base complementary-permanent class.  Across arbitrary even target sizes, any mixture of rank-one and rank-two spaces with leading survival has the common pure-`M` direction `(1,0)`; absence of that row forces every relevant leading shadow to be swallowed. |
| `GLS17`, `GLD15` | complete-target leading quotient coupling | `GLS18` | The partial-root quotient kills the residual-present desired class and sends the residual-absent class to `b_(A,S)`.  Applied to the complete target equation, this makes the three pure leading quotient classes a rank-at-most-one family, useful exactly when `b_(A,S)` and `M_S` are both nonzero; absence of pure `M` forces every desired and pure leading shadow to be swallowed. |
| `GLS5` | all-rank geometric failure topology | `GLS18` | Adjoining the three pure leading columns raises nuisance rank exactly on the response-gated useful locus.  Universal failure, including every exceptional nuisance-rank drop, is the exact radical--Fitting containment profile; finite target families use one shared residual point and a finite choice of partial-root shadows. |
| `GLS2`, `GLD15` | residual-present top-grade filtration | `GLS19` | Leaving `t` roots open for `|S|=2t` kills every grade above `t` and turns `g_S^Z` into the injection/permanent top tensor.  The generally surviving `g_S^M` is included in the exact individual-`Z` nuisance.  Top survival therefore gives the legal pure-`Z` row rather than an unjustified separate joint-rank-one attachment. |
| `GLD15`, `GLS5` | complete-target top coupling and failure topology | `GLS19` | The pure top quotient has rank at most one and rises exactly when its top desired class and `Z_S` response are both nonzero.  Universal and simultaneous failure retain every nuisance-rank drop through geometric radical--Fitting profiles at one shared residual point. |
| `GLS17` | four-root seven-target common-line gate | `GLD16` | Survival of all six pair base shadows and one of the four explicit four-port first-root covectors gives legal pure-`M` rows for all seven targets.  GLD16 then has effective scalar `a=1` for every residual `h`, but its three-colour pair-depth activity remains an independent input. |
| `GLS17`, `GLD15` | factored four-port selector with exact coefficient typing | `GLD67` | A surviving four-port first-root class can give a product-evaluation pure-`M` row.  That row annihilates the complete evaluated root-companion nuisance, so `G_(Q union {u,v})=0`; matching stratification nevertheless gives `F_(Q union {u,v})=B_uvG_Q`.  The legal module does not identify these two coefficient types. |
| `GLD65`, `GLD66` | invalid companion-to-full-coefficient bridge | `GLD67` | The cross-Gram identity and all dependent colour and plane exclusions are withdrawn.  An exact maximum-root graph satisfies the full evaluated selector row and has a diagonal pure three-colour four-port response, so the formerly claimed conditional exclusion is false. |
| `GLD67` | corrected product-selector boundary | `GL` | Any successor must use an actual full-target equation, a second independently legal response axis, or another coefficient-pure bridge.  Adding more labels from the same complete companion module cannot repair the failed transfer, because the exact control already satisfies every evaluated companion label. |
| `GLS16` | complementary order-two label in the four-root base nuisance | `GLD68` | For `T=U-S`, the label `I=T` contributes `H_T tensor Pi_T` to the target-`S` base map.  Nonzero `Pi_T` makes its target coefficient slices span the whole receiver, so `b_S=0`; zero `Pi_T` gives `b_T=0`.  Thus at most one base shadow in each complementary pair survives. |
| `GLD68` | maximal star/triangle common-incidence parent attempt | `GLD69` | The three surviving targetwise relations are retained in one labelled module, then lifted to the actual common residual permanent form `J=P_4(xi,eta,-,-)`.  The coefficient-only implication has exact countermodels; the physical rank-three locus compresses to rank-two star/triangle incidence and a sparse-radical detector. |
| `GLD69` | complete Q-layer parent reduction | `GLD70` | Retain all nine `Q`-meeting labels in the exact `79`-column nuisance map, replace targetwise quotient searches by the epsilon-open third-secant intersection, and compress the fully supported maximal-star family to one fixed `44`-space. |
| `GLD69` | exceptional-incidence and source obligation | `GL` | Outside the residual torus, classify or exclude simultaneous vanishing of the sparse-radical target values.  On a maximal rank-three triangle cover the centre--radical line and scalar-zero fibres.  Separately route lower port ranks, fewer surviving base classes, other root orders, and non-leading/promoted legal-row supply. |
| `GLD70` | punctured fixed-star parent reduction | `GLD71` | Remove the exact pair erasure, replace the `79` nuisance parameters by the complete `37`-check syndrome, close the one-word locus, and expose the coupled root-slice and Eisenstein-norm gates without assuming pairwise independence. |
| `GLD70` | remaining non-star atlas | `GL` | Build compatible residual-coordinate-boundary and triangle-centre atlases, then cover lower port ranks and smaller survivor profiles.  The fixed-star puncture does not extend to these strata automatically. |
| `GLD71` | exact determinant-safe route refutation | `GLD72` | The full `37 x 9` syndrome has an exact Gaussian-rational rank-`7` point with all three leaf-frame determinants and the centre determinant nonzero.  Direct original-space membership independently confirms the survivor, so the proposed saturation is false rather than merely incomplete. |
| `GLD72` | pinned contracted-edge and first-response test | `GLD73` | Pull the Gaussian survivor to the literal diagonal, realize one pinned raw preimage as complete ten-vertex contracted edge data, and test every unused incident row direction.  The grade-zero contraction succeeds, but the diagonal part of every contracted-vertex first-response image is only the base target line. |
| `GLD73` | full coefficient-fibre first-response parent theorem | `GLD74` | Quotient the complete `q_0` response by its thirteen fixed mixed columns.  The four root cofactors reduce to one `65 x 3` affine rank-one obstruction, so a complete projective cover replaces six separate determinantal saturations. |
| `GLD74` | survivor-locus symmetry and local geometry | `GLD75` | The complete local-basis stabilizer identity component is only factor scaling, while the `GLD72` survivor germ is smooth of dimension five.  A bidirectional exact ideal certificate integrates all five tangent directions and identifies the local equal-leaf gauge; four transverse parameters survive after scaling. |
| `GLD75` | universal response-module and boundary parent reduction | `GLD76` | Quotient the complete response by its thirteen fixed full-tensor columns, retain all four root columns, decompose the actual response under leaf `S_3`, and compactify the `GLD74` necessary rank-one system.  The exact module has a `4 x 3` lift, while two sign-type directions survive at infinity. |
| `GLD76` | exact sign-isotypic boundary compression | `GLD77` | Restrict the homogeneous mixed response to the full three-dimensional raw sign block.  Its determinantal ideal has exactly three reduced projective points, adding the third ratio `(1,-1,-1)` and replacing two isolated witnesses by an exhaustive finite sign-plane cover. |
| `GLD77` | all-three sign-boundary chart nonextension | `GLD78` | Retain the four scale-fixed survivor directions and two slope variables in corrected first jets, then Reynolds-average actual raw coefficients.  Three exact augmented `9 x 9` determinants give rank jumps `8 -> 9` on named principal opens and exclude affine arcs of every order through the pure-sign boundary points. |
| `GLD78` | full Gaussian projective-boundary classification | `GLD79` | Exact central idempotents and Schur compression split the boundary by isotype.  Injective `K_0` minors cover every projective chart; finite trivial and standard determinant certificates leave exactly the three reduced sign points. |
| `GLD79` | existential survivor principal-open nonextension | `GLD80` | The intrinsic rank-one incidence in `B x P^35`, saturated by `s`, is proper over the survivor base.  Algebraic DVR selection plus the three `GLD78` determinant units shows its strict closure misses the Gaussian fibre, yielding a principal open containing `F_0` on which every raw preimage fails first response. |
| `GLD80` | physical source-to-response incidence bridge | `GLD81` | In the actual root-order-four surplus-two torus-star source, partition the same ten-mode perfect matchings first by their unique outside raw edge and then by the neighbor of `q_0`.  This produces the physical `79`-coefficient vector and the complete `17`-coordinate legal response factorization, while GHZ target multilinearity supplies the `17 x 3` lift. |
| `GLD80` | explicit invariant quadratic principal open | `GLD82` | Reynolds-average the affine necessary rank-one incidence to a fixed rank-eight invariant raw kernel, transport by adjugates, quotient fraction-free on a named thirteen-row chart, and select forty-five intrinsic response quadrics whose moving coefficient determinant is nonzero at `F_0`. |
| `GLD81` | physical source consequence on explicit open | `GLD82` | Apply the source-to-incidence bridge to `D(Delta_82)`; every named maximal-star source there would enter the invariant quadratic incidence and is excluded. |
| `GLD82` | bordered-Pluecker quotient decharting and full quadratic Fitting reduction | `GLD83` | Replace quotient minors by `15 x 15` bordered determinants.  Their selected coefficient determinant removes `gamma_num`, while all exterior coordinates define the intrinsic Fitting-open union. |
| `GLD83` | equal-leaf centre-rank determinantal cover | `GLD84` | Use the exact global affine-linearity in the eight center shifts to split the intrinsic Fitting residual into finite rank-eight and rank-seven Schur charts plus the rank-at-most-six determinantal branch. |
| `GLD84` | named rank-eight chart full intrinsic Fitting specialization | `GLD85` | Pin one six-leaf/two-residual rank-eight point and certify a nonzero maximal minor of the full intrinsic coefficient map with denominator-checked exact modular reductions; retain the old selected-minor wall as a control. |
| `GLD85` | pulled-back rank-eight residual and remaining component/source cover | `GL` | Decide whether the rank-eight pullback of `I_Pl` is unit, has additional components, or leaves a residual; then analyze the other rank-eight charts, the saturated Gaussian rank-seven chart, `V(I_7(A))`, other survivor components/gauges, lower ranks, triangles, residual-coordinate and isotropic boundaries, smaller survivor families, off-chart source branches, other roots, and non-star atlases. |
| `GLD84` | equal-leaf rank-at-most-six syndrome boundary | `GLD86` | Use the fixed `37 x 9` syndrome map, the exact `C_8=1` scale-fixed relation, and one factorized `7 x 7` minor to confine `V(I_7(A))` to four named divisors. |
| `GLD86` | three-collision-divisor determinant safety | `GLD87` | On `H_1`, use the exact 11-row block transform, all base 4-minors, the difference-minor gcd, and the exceptional kernel shape; transfer the singular-center conclusion to `H_2,H_3` by exact leaf-column equivariance. |
| `GLD87` | H4 rank-six principal-open exclusion | `GLD88` | On a named six-pivot open, solve two exact linear Schur residuals for the forced leaf family and prove its complete center kernel has proportional rows. |
| `GLD88` | H4 P/d0 boundary exclusion | `GLD89` | Analyze the full `P=0` divisor and the separate `d0=0` overlap chart inside `H_4 intersect D(Omega)`, retaining the GLD87 H1/H2/H3 dependency only at the named overlaps. |
| `GLD89` | H4 Q6-open low-rank exclusion | `GLD90` | Factor the old and alternate raw pivots, classify their double-pivot locus by auxiliary charts and exact resultants, close the finite factor corners, and handle `T=0` without division. |
| `GLD90` | H4 Q6/L1/L2/e boundaries, Fitting, and remaining component/source cover | `GLD93` | Close the named L1/L2 coefficient divisors by direct rank-seven minors, double-pivot auxiliary witnesses, and exceptional-fibre certificates before pursuing Q6/e, the Fitting pullback, and remaining component/source coverage. |
| `GLD93` | H4 Q6/e boundaries, Fitting, and remaining component/source cover | `GL` | Analyze the retained `Q6=0` and `e=0` coefficient boundaries, compute the GLD83 pullback with full raw response incidence on `C_F` rank drops, and then cover remaining gauges, components, sources, profiles, roots and orders. |
| `GLD90` | H4 Q6 boundary on the GLD88 family | `GLD92` | Reconstruct two alternative six-minors on the GLD88 family, prove their Q6-open union is dense, and retain the finite common-minor locus explicitly; do not infer full H4 Q6 closure. |
| `GLD92` | H4 Q6 outside the GLD88 family, finite common residual, L1/L2/e boundaries, Fitting, and remaining component/source cover | `GL` | Analyze the retained finite `V(Q6,F28,F31)` locus and arbitrary H4 Q6 points outside the GLD88 family, then compute the GLD83 pullback with full raw response incidence on `C_F` rank drops and cover remaining gauges, components, sources, profiles, roots and orders. |
| `GLD85` | named rank-eight chart full intrinsic Fitting specialization | `GLD91` | The pinned point proves only that the full intrinsic pullback is nonzero/proper.  The exact two-leaf residual slice now supplies the next finite fibre-classification edge. |
| `GLD91` | completed two-leaf rank-eight Fitting-slice exclusion | `GL` | The corrected characteristic-zero slice has exactly one Schur/frame-open residual fibre, the GLD85 point, so the full intrinsic residual is empty on this two-leaf slice.  Full six-leaf rank-eight unitness/residual coverage, other charts, rank-seven/lower branches, components, source branches, and global resolution remain open. |
| `GLS19` | four-root seven-target common-line gate | `GLD16` | Useful top shadows for all six pair targets and the four-port target give legal nonzero pure-`Z` rows with one common direction.  GLD16 has effective scalar `a=h`; its proved `h=0` and `h!=0` branches both contradict a witness only under the unchanged three-colour activity gate. |
| `GLS15` | conditional pair-line synchronization interface | `GLD16` | If the physical cross-target transport defects vanish, every nonzero rank-one pair space has one common line.  Entry to GLD16 still additionally requires the four-port line to agree and the selected package to have the declared three-colour activity. |
| `GLS7` | full-rank literal all-response-zero localization | `GLS9` | On `D(det H_Q)`, vanishing of all six pair responses forces all direct port blocks to zero and a common one- or two-port shore.  The residual factors are coordinate; the singleton shore is fully monomial, while in the two-port shore at least one local factor is coordinate.  The four-port response then vanishes automatically and the complete contracted target forces opposite residual colours with pure third-colour `Pi_Q`.  The equal-colour branch is excluded, but the opposite-colour pure locus survives. |
| `GLS9` | two-complete-fibre exclusion | `GLS10` | In the localized opposite-colour chart, the `(i,i)` fibre excludes the singleton shore.  In the two-port normal form the same two alpha-lines occur on both residual shores: `(i,i)` forces them to cover `{i,k}`, while `(j,j)` forces them to cover `{j,k}`.  The labelled active-slot quotient uses no selector, response coordinate, or nuisance-minor division. |
| `GLS10` | determinant-divisor six-response reduction | `GLS11` | On the same GLS4 pair, assume all six full pair-response tensors vanish.  Rank zero is absent.  At rank two, complete mixed coefficients and maximality exclude every quotient escape and leave a conformal core with exactly two active combined ports, injective residual projections, fixed coordinate blockers, and a labelled quotient four-port target.  At rank one, an exhaustive double-contained/one-sided/two-sided trichotomy gives support-at-most-two normal forms for the escaping branches and exact target refinements.  Six pair zeros do not imply the seventh response zero; its quartic is separate. |
| `GLS11` | rank-two and singleton-triangle exclusion | `GLS12` | Six labelled active-pair quotients of the complete target exclude every rank-two active-dimension profile.  In the full `(2,2)` profile, conformal orthogonality gives opposite symplectic graph planes and a rank-two `B_st`, contradicting the final coordinate rank-one quotient.  On rank one, the singleton triangle's three pure companions share three tail incidence maps; column splicing would give a weighted `Delta_3` restriction of `P_4`, contradicting its exact subrank two. |
| `GLS12` | rank-one two-port common-tail extraction | `GLS13` | The complete mixed target forces the two local factor lines onto the two residual colours.  Eight mixed-target and four pure-companion coefficient identities share one two-tail permanent map.  A Latin bottom-row splice gives an exact weighted `P_5 -> Delta_3` restriction, and the physical seventh response is already termwise zero.  This is a proved downstream extraction edge, not an exclusion or selector theorem. |
| `GLS13` | structured permanent interface | `P5` | The displayed weighted `P_5` restriction enters the still-open local permanent programme.  No committed theorem excludes unrestricted `P_5 -> Delta_3`, so this branch stops at the downstream node. |
| `GLS12` | contained/one-sided rank-one continuation | `GLS14` | Branch I is exhaustively routed either to a nonzero decomposable `P_5` pullback or to the same-coordinate balanced core.  The balanced core splits into `Phi!=0`, where the seventh response is nonzero but no selector follows, and `Phi=0`, where the partitions align and an augmented `P_6` carries one explicit face defect `Psi` in the active-line module.  Branch II and its transpose supply a pure decomposable `P_4` singleton companion or one exact decomposable `P_5` deletion. |
| `GLS14` | remaining divisor and downstream interfaces | `GL` | The pure `P_4/P_5` pullbacks are nonconcise compression interfaces, not exclusions or the weighted `P_5 -> Delta_3` node of GLS13.  The `Phi!=0` branch still needs a legal response-visible selector; the `Phi=0` branch still needs `Psi=0` or a downstream theorem accepting the face defect.  Weaker response-zero patterns, nonzero-response absorption, exceptional fibres, and the legal attachment package remain outside this six-response divisor theorem. |
| `GLS15` | remaining projective transport and package obligation | `GL` | Prove that every foreign absorbed root-pair direction transports into every other complete joint nuisance quotient, or use its exact nonzero determinant/pure-target identity to contradict a complete mixed coefficient.  Separately cover joint rank zero, response-zero/missing-activity fibres, and at `r=4` the four-port line.  Raw or generic injectivity of `Psi_C` is insufficient, and pair rows alone are not a named downstream package at `r=3` or `r>=5`. |
| `GLS16` | remaining base-circuit and package obligation | `GL` | At root order four, `GLD68` proves that every complementary pair has at least one swallowed base shadow, so at most three pair base classes survive and every maximal survivor family is a star or triangle.  Exclude the resulting three-or-more swallowed-base circuits with complete mixed GHZ coefficients, or obtain legal rows from a non-leading source.  The foreign cross-annihilation maps are exact additional equations but are not transport membership.  Other root orders, four-port synchronization, activity, exceptional fibres, and the distinct GLS8 promoted interface remain. |
| `GLS17` | remaining leading-absorption and activity obligation | `GL` | Force leading survival for a sufficient even-target family, or contradict the simultaneous partial-root absorptions by complete mixed GHZ coefficients.  At `r=4`, `GLD68` proves that the all-six pair-base premise of the old seven-shadow route is impossible: at most three pair base shadows survive.  A surviving four-port first-root class still supplies a legal pure-`M` companion row, but `GLD67` proves that this alone gives no cross-Gram control of the direct port blocks.  Non-leading selectors, the swallowed star/triangle complements, other root orders, and `GLS8` remain separate. |
| `GLS18` | remaining target-coupled failure-locus obligation | `GL` | Exclude the simultaneous geometric radical--Fitting containments for a sufficient target family on the complete witness locus, or exhibit a shared residual point with useful leading shadows and all downstream activity gates.  At `r=4`, three pure first-root columns still imply the target-pure `M_U` response, but the withdrawn `GLD65`/`GLD66` bridge supplies no coupling between that response and the direct blocks.  Pair failure forces only the diagonal three-space, not the whole nine-space.  Full-target coupling, foreign transport, response activity, arbitrary-root source coverage, and `GLS8` remain separate. |
| `GLS19` | remaining second-axis and coexistence obligation | `GL` | Force useful residual-present top shadows for a sufficient target family at one shared residual point, or contradict their all-rank failure profile together with GLS18's pure-`M` leading failures.  At `r=4`, the pair and four-port top pure columns span only three-dimensional diagonal subspaces of dimensions 27 and nine; their absorption is not ambient fullness.  Oblique/unequal lines, activity, foreign transport, arbitrary-root source coverage, and GLS8 remain separate. |
| `GLS20` | factor-through base-survival audit | `GLS21` | The nine-row failure profile is not an open locus to exclude: `GLS21` proves it is forced by the complete all-port nuisance on `p!=0`. |
| `GLS21` | exact upstairs continuation | `GLS22` | Quotient the retained all-port root line rather than deleting it.  The transverse projector loses no legal selector on `D(p)` and removes the collapsed factor-through direction exactly. |
| `GLS22` | exact nuisance-structure continuation | `GLS23` | Expand the projected complete nuisance into physical label-slice spaces and isolate the common top-anchor line without dropping any active label. |
| `GLS23` | exact anchor-marginal continuation | `GLS24` | Contract the transverse root factor at the actual probe vectors and quotient a nonzero anchor marginal by its denominator-free exterior map, while retaining the zero and double-transverse anchor fibres explicitly. |
| `GLS24` | double-transverse continuation | `GLS25` | On `omega!=0` with both actual-root marginals zero, use `q,p` to project denominator-free onto the four-dimensional core and quotient the common anchor line without deleting any physical nuisance label. |
| `GLS25` | remaining promoted reduced/full failure obligation | `GL` | Use complete mixed GHZ coefficients to exclude the zero anchor and simultaneous `9`-row or `27/4`-row plus full-quotient Fitting failures, or force one reduced useful family with top survival and response activity.  Reduced absorption is not full `63/72`-row absorption.  At `r=3`, low activity and any failed pair/top row remain; at `r>=4`, no named complete downstream package accepts the high-depth responses. |
| `GLS28` | remaining zero-anchor attachment obligation | `GL` | On the generic-escape branch, exclude the deletion-stable diagonally redundant supplier cover by complete mixed equations, including every exceptional GLS22 Fitting/rank-drop fibre, or force one diagonal-coloop useful row.  Separately attach or exclude the exact `C12/C21/C22` forms.  A supplier coloop alone may have zero response, envelope containment is not actual nuisance absorption, and no promoted arbitrary-root downstream theorem accepts one isolated row.  Synchronization, activity, simultaneous package coverage, and detector entry remain open. |
| `GLS29` | remaining higher-root rank-two-shore obligation | `GL` | At `r>=4`, exclude or attach the at-least-three-edge disjoint-supplier branch using the complete mixed equation.  Normal-image fullness is not full nuisance absorption and the normal supplier tensor is not the complementary GLS8 response.  Other shore ranks and `C12/C21/C22` remain separate. |
| `GLS30` | combined static-gate audit | `GLS31` | Maximum-root incidence, pure normalization, simultaneous complete pair absorption, full normal images, six responses, the scalar normal identity, and the GLS26 diagonal inclusion coexist on one exact graph.  Hence those static gates cannot close the divisor without original mixed equations. |
| `GLS31` | singleton-kernel and whole-pencil audit | `GLS32` | Contracting the complete first-polarized equations isolates exact one-port identities without deleting one-`Q` labels or dividing by a response.  One maximum-root graph then realizes all three nonconstant coefficient equations, the full projected evaluation pencil, and every listed `GLS31` static gate while all desired classes remain absorbed. |
| `GLS32` | residual-family and actual-root lift | `GLS33` | Formal residual variables separate the fixed-point one-`Q` cancellations coefficientwise.  The unprojected constant term supplies a distinct root-deck equation whose exact local kernels isolate `pH_Uhat` modulo `span{a_u,b_u}`. |
| `GLS33` | coefficientwise blind-space and constant-anchor case cover | `GLS34` | Split the four polynomial profiles into their exact shore/tangent multiplication blocks.  Independently restrict the constant diagonal to the product of the local two-row kernels and classify its zero tensor through three colours. |
| `GLS34` | raw anchor module / output-to-coefficient audit | `GLS35` | Define the complete unprojected non-`Q` slice span before invoking a coefficient-side selector, and type-check its output against GLS22/23 and GLD3.  The resulting jump selects only the residual-absent `D=Q` deck; it is not an original promoted-target selector. |
| `GLS35` | incidence-map and labelwise-faithfulness audit | `GLS36` | Present the complete zero-anchor raw nuisance as one physical incidence map, determine exactly what the full-swallow branch does to common coefficient rows, and retain the complementary deck labels in a type-correct mixed-equation interface. |
| `GLS36` | minimal nuisance-rank / residual-shore audit | `GLS37` | Use the exact incidence image to classify the smallest full-swallow rank before seeking a deck-coupled contradiction; correct the grade-zero companion provenance and retain every shore-rank fibre. |
| `GLS37` | nonzero-root-companion shore-drop audit | `GLS38` | Use `q!=0` (inherited in particular from the GLS35 non-silent gate `p!=0`) to determine whether the rank-three full-swallow shore-drop alternative can occur. |
| `GLS38` | complete whole-domain pair-family audit | `GLS39` | Adjoin the fixed residual labels as one-dimensional domains and use every distinct-label polarization at once, rather than continuing the shore-rank case split, to decide the remaining conditional `q=0` rank-three full-swallow fibre. |
| `GLS39` | aggregate-deck / target-cylinder audit | `GLS40` | Use the complete fixed-residual equation to identify dual incidence rows detecting the quotient `B/(Delta+Kq)`, and type every `p!=0` promoted pair target inside the resulting rank-stratified transverse cylinder. |
| `GLS40` | pure-core / excess-response audit | `GLS41` | Quotient the rank-stratified cylinder by its projected diagonal core and use the complete target equation to decide whether any excess class can carry a useful nonzero physical response. |
| `GLS41` | selected excess first-variation audit | `GLS42` | Lift a fixed-point excess row back to the complete open-`A` tensor identity, identify its denominator-free principal-hafnian first variation, and determine whether that equation plus nonzero detected decks alone can force the remaining pure-core escape. |
| `GLS42` | remaining pure-core physical attachment obligation | `GL` | At one common contraction retaining `H_Q(z_Q)p(z_Q)!=0`, force `im D_C^tr` outside `N_C^tr intersect (P_Q(Delta) tensor V_C^*)` for one eligible pair, or contradict all such containments with additional complete same-graph pure/mixed and principal-deck equations.  The selected excess first variation and its four detected nonzero decks do not by themselves contradict a physical graph, and pure-core containment in that control is undecided.  Any rank rise must still be synchronized with responses, selected activity, every additional/common nuisance gate, and a named receiver.  The zero-anchor top target is dead; silent `p=0` source coverage and raw escape attachment remain separate. |
| `GLS8` | remaining physical and downstream-package obligation | `GL` | Derive a complete-mixed companion/integrability identity forcing at least one failure containment to break for some eligible `(Q,A)`, or contradict the simultaneous all-target profiles on the same graph.  Then prove the rows so obtained satisfy the complete common-package, synchronization, alignment, activity, and anchor hypotheses of a named committed downstream detector; GLS8 alone does not do so.  The C leaf is an obligation only for an entry expressly requiring stronger pair observability.  Rank, pure-target, or bounded-support data alone are insufficient. |
| `GLS2` | remaining supply and attachment obligation | `GL` | Companion-sensor rank drop on the target locus, every higher-surplus nonlinear/cross-window supply, the three-group overlap condition, and weighted-diagonal attachment remain open.  Ambient full rank does not discard the witness rank-drop branch. |
| `GLS3` | sharp mixed-equation rank-drop boundary | `GL` | Maximum-root data, exact blocker quotas, local concision, pure normalization, the Hamming-one target shell, and nonzero raw `p_A` do not force pair observability.  The exact physical fibre is excluded by one higher mixed coefficient, so a positive theorem must use the full mixed witness equations or a proved physical quotient. |
| `GLS4` | remaining same-pair attachment obligation | `GL` | The source now supplies one individual order-two class and raw companion on the same `Q`.  It still must force a legal nonzero same-`Q` response/target selector package, including every downstream alignment and anchor gate, or exclude all selector-failure fibres with complete mixed coefficients.  Scalar complementary permanents have no universal polynomial relation that can do this alone. |
| `GLQ2` | exact conditional descent / boundary | `GL` | Three rank-two cross-observed groups identify one `O(J)` transition and cycle holonomy exactly decides finite-atlas frame descent.  The observable `GLS2` branch now supplies its paired windows, but a glued corrected frame is not yet a weighted diagonal permanent restriction. |
| `GLD1`, `GLS4` | four-root adjacent-grade refinement | `GLD2` | The same-pair theorem supplies individual quotient survival and some `p_A!=0` on one active `Q`, but not a legal complementary root-edge selector.  Conditional on augmented `l^T Jp!=0`, the polarized selector decomposes into residual-absent, direct, corrected, and one-residual cross sectors.  Augmented nonvanishing supplies neither same-index alignment nor target purity. |
| `GLD2` | exact sufficient-selector detector boundary | `GL` | For `h!=0`, cross-depth direct cancellation requires `l-kappa p in ker mathcal U`.  One sufficient detector package additionally needs a legal constant `l` with `l^T Jp!=0`, constant synchronized selectors for the response and zero-grade companion, and the residual-absent anchor or an exact target-diagonal nuisance identity.  This package is not proved minimal.  A single coefficientwise-clean shore is trivial, and nested cancellation survives maximum-root triple-blocker controls. |
| `GLD1` | pair/four-port target-coupling refinement | `GLD3` | The polynomial interference identity eliminates the direct deck across pair and four-port depths.  Same-graph common residual rows give the corrected compound a one-mode rank-two bound, but exact target attachment is a separate input. |
| `GLD3` | bounded three-active detector / two-active boundary | `GL` | Once one nuisance-free constant same-`Q` target window is supplied, three complementary active colours give a nine-word mixed coefficient certificate.  Full pair-plus-four mixed zeros do not close the zero/one/two-active branch or identify the corrected channel, as shown by the exact camouflage response. |
| `GLD3` | two-chart affine and overlap refinement | `GLD4` | Stacking constant uncontracted chart equations gives an exact quotient-incidence trichotomy.  Disagreement is target-coupled, but a displayed coefficient additionally requires a coefficient-pure left syzygy.  Repeating the two-active observed package on arbitrarily many common-core windows leaves literal overlap agreement and no GLD3 activity. |
| `GLD4` | remaining target-attachment and physical-integrability obligation | `GL` | Produce the constant chart maps from the full witness equation, prove coefficient-pure or uniformly sparse left syzygies, add a deeper target-attached response layer, or exclude the cloned two-active package on the witness locus.  Abstract affine kernels and observed `D`/`T` agreement do not supply complete paired `M,Z` charts or a permanent restriction. |
| `GLS2` | fixed-`Q` full-module attachment refinement | `GLD5` | The full companion equation gives a finite constant-module question with every nuisance retained.  Exact attachment is the nonvanishing quotient class `[g_S] in L_S^*/N_S`; maximum-root and triple-blocker incidence alone meet both its good and bad branches. |
| `GLD5` | conditional exact same-`Q` attachment | `GLD3` | If all seven quotient classes survive on one hypothetical-witness chart, their constant selectors supply the exact six `D_uv` tensors and `T` required by GLD3.  The theorem does not force those classes or GLD3's three-colour activity. |
| `GLD3`, `GLD4` | all-subwindow and deeper-response refinement | `GLD6` | At `h=0`, all fifteen four-port restrictions on six ports form a coefficientwise Wick system.  The two-active line locus has bounded selectors even on its singular words, and its remaining diagonal direct layer leaks into a displayed mixed depth-six coefficient once one pure four-port response is nonzero. |
| `GLD5` | full witness-target quotient refinement | `GLD7` | Modulo every nuisance slice, the witness equation is `[g_S] tensor P_S(H)` and the active pure target has rank at most one.  Pure rank one forces attachment; pure rank at least two excludes target incidence; rank zero is the swallowed-pure residue. |
| `GLD7` | conditional seven-row attachment | `GLD3` | Rank one for each of the six pair quotients and the four-port quotient supplies the exact same-graph `D_uv` and `T` package.  Rank one does not force coefficient purity or GLD3 activity. |
| `GLD7` | conditional thirty-one-row attachment | `GLD6` | In the six-root/six-port full module, rank one for all fifteen pair, fifteen four-port, and one six-port pure quotients legally attaches the response rows used by GLD6.  The theorem does not force those ranks or physical response nonvanishing. |
| `GLD6` | global common-row refinement | `GLD8` | Square-free factorization classifies the complete scalar pair-to-four-row map by the two residual support sets.  A seven-port common-row selector can exist even when every principal six-window through the named pair is singular. |
| `GLD7` | remaining quotient-locus obligation | `GL` | Force active pure rank one and the required response nonvanishing for every relevant row, or exclude the swallowed-pure branch.  A rank-one pure quotient supplies attachment but not a coefficient-pure mixed syzygy. |
| `GLD8` | remaining attachment and tensor-cover obligation | `GL` | Attach the required same-`Q` `z_2,z_4,z_6` rows, prove a coefficient-word support cover of every needed tensor entry, force the nonzero pure/activity hypotheses for the depth-six detector, and separately supply any weighted-diagonal permanent bridge. |
| `GLD7` | maximal-rank common-contraction refinement | `GLD9` | For a finite selector family on one graph and one `Q`, maximal nuisance-rank survival defines nonempty principal opens whose intersection supplies one fully supported common contraction.  On a witness, response nonvanishing must be included separately to synchronize quotient rank one. |
| `GLD9` | conditional common seven-row attachment | `GLD3` | Seven individually witnessed maximal-rank rank-one points synchronize to one contraction and then supply the exact six `D_uv` tensors and `T`.  The theorem does not force those individual points or three-colour activity. |
| `GLD9` | conditional common thirty-one-row attachment | `GLD6` | Thirty-one individually witnessed maximal-rank rank-one points synchronize the six-port `z_2,z_4,z_6` selector package.  This does not extend attachment automatically to seven ports. |
| `GLD8` | five-helper tensor-word refinement | `GLD10` | On seven ports, five bi-supported helper coefficient vectors reduce every requested direct-pair tensor coefficient to an injective `21`-, `6`-, or `1`-row scalar block.  Varying the coefficient word reconstructs all 189 entries from the same thirty-five attached `z_4` tensors. |
| `GLD7` | simultaneous swallowed-pure sharpness | `GLD11` | Maximum-root incidence, triple blockers, local concision, pure normalization, the Hamming-one shell, and all seven nonzero responses coexist with quotient rank zero for every target.  A mixed target coefficient excludes the control, so full witness equations remain essential. |
| `GLD6`, `GLD8` | full tensor four-port closure | `GLD12` | At fixed `K` and `h=0`, equality of the complete tensor `z_4` layer is equivalent to equality of the entire residual-present `Z` tower.  The fibre is `B+ker mu_K`; GLD8 therefore becomes an exhaustive all-depth scalar criterion, while scalar-word kernels need not survive tensor polarization. |
| `GLD9` | remaining individual-survival obligation | `GL` | Prove that every needed selector survives on its maximal nuisance-rank stratum with nonzero response, or exclude the determinantal exceptional locus.  Common-contraction synchronization alone supplies no individual selector. |
| `GLD10` | remaining seven-port attachment/helper obligation | `GL` | Legally attach all thirty-five same-`Q` four-port tensors and force the five-helper condition or another exhaustive coefficientwise cover on the witness locus.  Tensor supply alone gives no depth-six detector or permanent restriction. |
| `GLD11` | remaining swallowed-pure witness-locus obligation | `GL` | Use the full mixed GHZ equations to exclude simultaneous quotient rank zero, or derive a bounded coefficient-pure detector.  The physical graph-side control is explicitly not a witness. |
| `GLD12` | remaining target and paired-response obligation | `GL` | Full tensor `z_4` kernels cannot be repaired by deeper same-`Q` residual-present `Z` rows.  A positive theorem must attach paired `M,Z` information, exploit target-shape rather than equality, or use the full mixed witness equations; no permanent bridge follows. |
| `GLD7`, `GLD9` | function-field contraction dichotomy | `GLD13` | For a full uncontracted witness with all seven response polynomials nonzero, generic desired survival for every target has one common contraction; failure localizes to a named target whose desired and three pure columns are all absorbed over the contraction function field.  Generic absorption permits exceptional rank-drop escape. |
| `GLD13` | conditional common seven-row attachment | `GLD3` | The generic-survival branch supplies one common fully supported contraction with all seven rank-one quotient classes and hence the exact six `D_uv` tensors and `T`.  It does not force GLD3 activity. |
| `GLD12` | paired M2/M4 target-shape refinement | `GLD14` | Fixed legally attached `M_2` rows cut the complete `Z` fibre affinely and optimally.  Pair diagonality plus the finite two-colour `M_4` equations is equivalent to all-depth mixed `M` purity; legal attachment of those rows remains an input. |
| `GLD7` | joint two-column target-quotient refinement | `GLD15` | Retaining the residual-absent `I=S` and residual-present `I=Q union S` labels simultaneously makes the exact constant operator-supply space the row space of their two quotient classes.  Pure quotient rank two forces separate legal `M_S,Z_S` attachment and response independence; ranks zero and one retain the classified ambiguities. |
| `GLD12`, `GLD14` | fixed-Z pair-block cover refinement | `GLD15` | An `M`-active joint row cuts a fixed compatible full-`Z` fibre exactly like the corresponding direct pair block.  Pair-block projection covers eliminate `ker mu_K`; the full ternary complete-bipartite `K_(3,3)` and `K_(5,2)` controls have exact cover numbers four and six.  This does not separately attach `M` or transfer diagonality without the required `Z` information. |
| `GLD15` | conditional localized paired-response detector | `GL` | Joint rank two on the selected pair/four-port targets attaches the corresponding same-graph same-`Q` `M,Z` tensors.  One four-port and two cross-pair targets isolate a mixed `M_4` coefficient when a complementary-colour product is externally nonzero; forcing those ranks and activity remains open. |
| `GLD3`, `GLD15` | common projective shifted detector | `GLD16` | A nonzero intersection of the seven joint operator-coefficient spaces supplies one common linear combination of every pair and four-port `M/Z` target.  For arbitrary `h`, the effective scalar `a=delta+h eta` gives the denominator-free identity `aT'=C(D)-C(eta K)`; three-colour activity excludes both the `a=0` divisor and the `a!=0` mixed-coefficient branch. |
| `GLD15`, `GLD16` | unequal-slope quadratic-cancellation detector | `GLD17` | Pair slope `[1:p]` and four-port slope `[1:t]` give `T=C(D)+(t-p)X(D,K)+p(p-2t)C(K)`.  On the two noncommon cancellation branches, one three-full complementary pair forces a mixed coefficient among eighteen fixed rows by the physical block-rank bound. |
| `GLD15` | response-visible operator-slope interface | `GLD18` | On the full fixed-`Q` witness equation, every complete-nuisance operator space lies in the kernel of its mixed-response map.  Visible rank-one slopes are determined by response minors; invisible rank-one slopes remain module-only.  This is an exact one-way inclusion, not response-shape manufacture of a selector. |
| `GLD16`, `GLD17` | edge-dependent cancellation and decomposable-channel refinement | `GLD18` | Independent pair slopes give one exact quadratic correction for each complementary matching.  Vanishing of all three corrections plus one three-full pair gives the eighteen-word rank contradiction.  On a globally vertex-factorable rank-one channel, the common-slope noncancellation residue is also excluded by a branch-specific finite detector. |
| `GLD18` | response-map-zero support refinement | `GLD19` | Literal vanishing of each full realized mixed-response map separates the raw pair blocks `B,K` and the four-port layers `C(B),X(B,K)`.  The resulting ordered `2+2` equations classify every complementary support pattern and yield a five-row detector without choosing or synchronizing hidden slopes. |
| `GLD18` | globally decomposable arbitrary-slope refinement | `GLD64` | Global port factorization makes the three complementary `K_eK_f` terms one word monomial.  Under one three-full complementary pair, forty-three fixed mixed rows exclude every finite six-pair/four-port slope package without synchronization or cancellation assumptions. |
| `GLD19` | common-shore global support refinement | `GLD20` | Simultaneous physical shore factorization reduces the six diagonal corrected blocks to zero, one non-`P_4` colour graph, or two clique colour graphs.  Full-capable edges inherit opposite raw annihilation, and the full quotient witness equation converts each opposite zero response into one `GLD15` pure-rank-zero target. |
| `GLD20` | complete-clique dead-colour coefficient refinement | `GLD21` | In the two-colour channel cell with one complete corrected clique, common shores kill the third colour and the complementary support alternatives confine every direct block to the complete colour.  The full all-missing GHZ coefficient then excludes `h=0`; Hamming-one and dense `2+1+1` coefficients give the surviving companion normal form. |
| `GLD21` | common-private same-graph integrability exclusion | `GLD22` | On one common private colour-diagonal root-to-port matching, an opposite-colour double flip isolates and kills the active diagonal of the shared root--root edge.  Three Hamming-one singleton values then turn the matching mixed coefficient into the nonzero scalar `-2hP`.  The argument uses one physical edge array across both packages; arbitrary formal companion columns do not satisfy that interface. |
| `GLD22` | colour-dependent private-permutation exhaustion | `GLD23` | Dense-shore orthogonality gives one canonical scalar gauge.  The remaining two active private permutations form `28` exact symmetry orbits, each excluded by a characteristic-zero left-null coefficient certificate; an independent audit checks all `576` ordered pairs. |
| `GLD23` | first nonprivate balanced-switch exclusion | `GLD24` | On one switched active colour slice `I+E_(0,1)+tE_(1,0)`, an eighteen-row polynomial relation gives the nonzero detector `-4t(t+1)` away from `t=-1`, and a separate ten-row certificate closes that exceptional fibre. |
| `GLD24` | two-independent-amplitude switch completion | `GLD25` | Replacing the fixed first switch amplitude by independent `u,v!=0` gives a bivariate generic detector.  Three exact divisor relations and point/quadratic residual certificates close its complete exceptional locus, so the two-dimensional chart is empty. |
| `GLD25` | generic directed-spur support extension | `GLD26` | Adding `wE_(0,2)` produces a three-parameter larger-support chart.  A sixteen-row polynomial relation excludes the complement of the four divisors `uv=1`, `uv=-1`, `uv-u-v-1=0`, and `uv+vw+w+1=0`; no specialization across those divisors is claimed. |
| `GLD26` | pointwise `uv=-1` divisor closure | `GLD27` | A polynomial-cleared divisor detector reduces `uv=-1` to the `u=1` line and the quadratic `u^2+2u-1=0`; exact line, point, and quotient-ring certificates close every residual point for `w!=0`. |
| `GLD26` | pointwise `uv=1` divisor closure | `GLD28` | A divisor detector reduces `uv=1` to four explicit curves; their exact detectors leave four rational points and one shared `u^2+1=0` family, all closed by point and quotient-ring certificates. |
| `GLD26` | pointwise `uv-u-v-1=0` divisor closure | `GLD29` | An eighteen-row detector reduces the divisor to five curves.  Their exact relations feed the proved `GLD28` locus or one quadratic cylinder, whose two residual fibres have exact quotient contradictions. |
| `GLD26` | pointwise `uv+vw+w+1=0` divisor closure | `GLD30` | After its `v=-1` fibre feeds `GLD27`, a sixteen-row detector reduces the remaining divisor to three curves and the same proved `uv=-1` locus.  Three exact curve relations feed `GLD27`, `GLD28`, or `GLD29`, completing the exceptional-locus cover and hence the nonzero directed-spur chart. |
| `GLD30` | generic bidirected-spur support extension | `GLD31` | Adding `zE_(2,0)` produces a four-parameter chart.  A sixteen-row polynomial relation excludes the complement of five explicit hypersurfaces; its `z=0` boundary is the completed `GLD30` family, but no specialization across the five new divisors is claimed. |
| `GLD31` | generic `uv=-1` divisor refinement | `GLD32` | Substituting `v=-1/u` into fourteen complete rows excludes the complement of `u=1`, `z=1`, `z=-1`, and `wz=2` inside the first exceptional divisor.  No pointwise closure of those four surfaces is claimed. |
| `GLD32` | pointwise `u=1` residual closure | `GLD33` | Two surface detectors leave one rational curve and one point; exact constant contradictions close both, eliminating the full residual surface. |
| `GLD32` | pointwise `z=1` residual closure | `GLD34` | One two-row complete-system relation leaves the nonzero chart parameter `w`; a disjoint two-row relation leaves `-u^(-1)`, eliminating the full residual surface. |
| `GLD32` | pointwise `z=-1` residual closure | `GLD35` | Two disjoint two-row complete-system relations leave `-w/u` and `-u^(-1)`, eliminating the full residual surface. |
| `GLD32` | pointwise `wz=2` residual closure | `GLD36` | One two-row complete-system relation leaves `-u^(-1)`.  This closes the last surface and, with GLD33--GLD35, exhausts the exact GLD32 case cover. |
| `GLD31` | pointwise `uv+wz-1=0` divisor closure | `GLD37` | Two disjoint two-row complete-system relations leave `v` and `wv`, eliminating the full divisor under the original nonzero chart hypotheses. |
| `GLD31` | pointwise `uv+wz+1=0` divisor closure | `GLD38` | Two disjoint two-row complete-system relations leave `v` and `wv`, eliminating the full divisor under the original nonzero chart hypotheses. |
| `GLD31` | pointwise nonzero-chart completion | `GLD39` | Two complete rows over the full polynomial ring leave `w`, eliminating the whole GLD31 chart under its original `w!=0` hypothesis and subsuming the generic and divisor-specific refinements there. |
| `GLD39` | all-support affine-chart completion | `GLD40` | Relabelled and boundary-specialized two-row relations successively leave `u`, `w`, `v`, and `z`; GLD23 closes the all-zero identity endpoint, exhaustively covering all `16` support masks. |
| `GLD23` | all-zero private boundary | `GLD40` | The origin of the affine parameter space has all three cross slices equal to `I_4`, hence is an exact instance of the proved private-permutation exclusion. |
| `GLD40` | complete single-active-slice affine extension | `GLD41` | The two-row entry detector is valid over the polynomial ring in all twelve off-diagonal amplitudes, so each of the twelve ordered entries is excluded without specializing any other entry. |
| `GLD23` | all-zero private boundary | `GLD41` | The unique support mask with no active off-diagonal entry has all three cross slices equal to `I_4`, hence is the proved private-permutation origin. |
| `GLD41` | reciprocal two-active-slice affine exclusion | `GLD42` | The support-drop faces lie in the completed single-active-slice cell.  On the genuinely two-active interior, an exact divisor relation, function-field certificate, and rational exceptional-point core exhaust the reciprocal-spike chart. |
| `GLD42` | full two-active-slice reciprocal-support reduction | `GLD43` | Twelve exact three-row divisor relations force transpose-matched support in the simultaneous 24-amplitude ring.  GLD41 and GLD42 remove the matched masks of size zero and one, leaving at least two reciprocal pairs. |
| `GLD43` | five-orbit two-pair generic exclusion | `GLD44` | Exhaustive directed-support classification gives `66` masks in five orbits.  One exact function-field core per orbit excludes the complement of its displayed denominator divisor. |
| `GLD44` | same-tail exceptional-divisor closure | `GLD45` | On `u=-1`, a new twelve-row certificate has no denominator root inside the active reciprocal domain, so the generic same-tail exclusion becomes pointwise complete. |
| `GLD44` | disjoint exceptional-divisor closure | `GLD46` | An eleven-row certificate closes `u=-1`; an explicit support-pair exchange closes `w=-1`, exhausting the generic theorem's disjoint exceptional union. |
| `GLD44` | reverse exceptional-divisor closure | `GLD47` | Two exact curve certificates close `u=-1` and `uw=-1`; pair exchange closes `w=-1`, exhausting the reverse exceptional union. |
| `GLD44` | same-head exceptional-divisor closure | `GLD48` | Pair-ordered generic certificates reduce the exceptional intersection to one curve and one point; exact sparse contradictions close both. |
| `GLD44` | chain exceptional-divisor closure | `GLD49` | Exact curve certificates close both factors of the generic exceptional divisor, completing all five two-pair orbits. |
| `GLD49` | three-pair generic exclusion | `GLD50` | An exact `13`-orbit census and one sparse function-field contradiction per orbit exclude the generic part of all `220` masks. |
| `GLD50` | directed-path exceptional-surface closure | `GLD51` | One fourteen-row certificate has no denominator root in the active domain, making the full `24`-mask `O10` orbit pointwise empty. |
| `GLD50` | out-star exceptional-surface closure | `GLD52` | Two exact surface certificates have no legal denominator root, making the full `4`-mask `O1` orbit pointwise empty. |
| `GLD50` | fork-path exceptional-surface closure | `GLD53` | Two surface certificates reduce to their common curve; a third exact certificate closes it, making all `24` `O4` masks empty. |
| `GLD50` | reverse-disjoint exceptional-surface closure | `GLD54` | Four surface certificates leave two legal overlap curves; exact certificates close both, making all `12` `O8` masks empty. |
| `GLD52` | exact active-colour-exchange transfer | `GLD55` | Swapping active colours reverses the three arrows and an invertible signed nuisance-coordinate change preserves every complete equation, carrying `O13` to the excluded `O1` orbit. |
| `GLD53` | exact active-colour-exchange transfer | `GLD56` | Swapping active colours reverses the fork path and a position permutation carries it to `O12`; the signed nuisance covariance transfers the full pointwise exclusion. |
| `GLD50` | in-fork exceptional-surface closure | `GLD57` | Four surface certificates leave three legal intersections; exact curve certificates close all three, making all `12` `O11` masks empty. |
| `GLD57` | exact active-colour-exchange transfer | `GLD58` | Swapping active colours reverses the in-fork and a position permutation carries it to `O5`; the signed nuisance covariance transfers the full pointwise exclusion. |
| `GLD50` | O6 exceptional-surface closure | `GLD59` | Four surface certificates leave two legal curves; exact fifteen-row certificates close both, making all `24` `O6` masks empty. |
| `GLD50` | O3 exceptional-divisor closure | `GLD60` | Four surface certificates leave five intersections; five curve certificates leave two points, and exact rational cores close both, making all `24` `O3` masks empty. |
| `GLD50` | O2 exceptional-divisor closure and O7 colour exchange | `GLD61` | Seventeen exact O2 cores have a complete saturated denominator cover with one terminal point; active-colour exchange reverses O2 to O7, making all `48` masks empty. |
| `GLD50` | final O9 exceptional-divisor closure | `GLD62` | Fourteen exact cores give a complete saturated and Euclidean denominator cover, making all `8` O9 masks and all `220` exactly-three-pair masks empty. |
| `GLD13` | remaining generic-absorption obligation | `GL` | Exclude the function-field absorbed branch by the full mixed equations or turn one of its denominator-cleared nuisance identities into a bounded coefficient-pure target contradiction.  Exceptional rank-drop behaviour, response-zero blocks, activity, and permanent attachment remain separate. |
| `GLD14` | remaining paired-attachment/witness obligation | `GL` | Legally attach a sufficient same-graph same-`Q` package of the selected `M_2,M_4` rows and intersect its radical cross-intersection locus with the full witness equations.  Pure one-colour kernel families show that mixed response shape alone does not remove every `Z` fibre. |
| `GLD15` | remaining joint-rank and integration obligation | `GL` | Force joint quotient rank two on a pair-block cover and the needed four-port rows, or exclude the rank-one/zero branches with the full mixed witness equations.  `GLD11` shows that maximum-root incidence, blockers, concision, pure/Hamming shell data, and nonzero paired responses do not suffice; no permanent bridge follows. |
| `GLD16` | remaining common-line and activity obligation | `GL` | The common-line detector works for arbitrary residual scalar `h`; no `h` divisor remains inside this conditional branch.  `GLD68` proves that the `GLS17` all-six pair-base route cannot supply its seven rows.  Force one nonzero projective coefficient vector into all seven full operator spaces by a non-leading or promoted source and force three-colour pair-depth activity, or exclude the zero and different-slope branches with the full mixed equations.  Target-dependent slopes and two-active common-line packages are exact sharp boundaries; no permanent bridge follows. |
| `GLD17` | remaining unequal-slope and support obligation | `GL` | Force one of the two quadratic-cancellation slope relations together with a three-full complementary pair, or classify/exclude the remaining slope and sparse-support locus by the full mixed equations.  The theorem neither supplies legal rows nor proves the local six-value condition; no permanent bridge follows. |
| `GLD18` | remaining operator-incidence and response-locus obligation | `GL` | Force nonzero complete-nuisance operator spaces, resolve response-invisible and pure-`Z` axes, force a three-full complement, or exclude the nondecomposable noncancellation and sparse-support strata with the full witness equations.  GLD64 removes slope synchronization and cancellation only on the globally decomposable finite-slope branch; the response-visible minors do not themselves supply legal rows or a permanent bridge. |
| `GLD64` | remaining decomposable-branch source obligation | `GL` | Force seven `M`-active legal rows, global port factorization, and one three-full complementary pair on a named physical response, or use the theorem only after an upstream source reduction supplies those gates.  Pure-`Z` axes, general rank-two channels, arbitrary-root source coverage, anchors, nuisance survival, and permanent consequences remain separate. |
| `GLD67` | corrected product-selector parent obligation | `GL` | Couple a legal root-companion selector to the direct port response through a genuine full GHZ target coefficient, a second independently legal response axis, or another proved coefficient-pure map.  The exact three-colour control rules out any theorem that uses only the complete evaluated companion row.  `GLD68` separately removes the proposed all-six pair-base source branch, but single product rows and non-leading all-seven packages remain possible.  Swallowed circuits, other root orders, promoted-source integration, activity, anchors, and permanent consequences remain separate. |
| `GLD68` | completed maximal-profile parent handoff | `GLD69` | The at-most-three survivor atlas now has one common labelled module, exact coefficient-only countermodels, and a physical common-`J` lift.  The old instruction to prove a third targetwise sibling theorem is superseded by the explicit GLD69 exceptional-incidence obligations. |
| `GLD69` | completed full-Q-layer handoff | `GLD70` | The nine formerly open labels now have one exact `79`-column map and one basis-independent secant-boundary criterion.  The fully supported rank-two maximal-star family is one fixed `44`-space rather than an unbounded slope family. |
| `GLD69` | remaining exceptional-incidence obligation | `GL` | Prove sparse-radical target activity or classify the simultaneous scalar-zero divisor outside the residual torus.  For triangles, handle the centre hyperplane's radical intersection and scalar-zero fibre.  Port-rank-deficient profiles, fewer survivors, source supply, and other roots remain separate. |
| `GLD70` | completed punctured-syndrome handoff | `GLD71` | The fixed star now has an exact `60/23/37` punctured-code presentation, a complete characteristic-zero one-word atlas, root-slice gates, and an Eisenstein-norm boundary.  An exact two-word defect rules out MDS-style strengthening. |
| `GLD70` | remaining non-star secant atlas | `GL` | Extend the secant language to residual-coordinate boundaries and the general triangle, then cover lower port ranks and smaller survivor profiles.  A failed elimination, timeout, modular sample, or nonunit algebraic survivor changes no graph status. |
| `GLD71` | completed exact counterexample handoff | `GLD72` | The full coupled syndrome, not the rejected ten-row compression, has a genuine invertible-centre Gaussian point.  Exact original-space membership, local and balanced ranks, and nonzero epsilon refute the strong fixed-space exclusion while preserving every proved puncture and one-word result. |
| `GLD72` | completed pinned edge-fibre handoff | `GLD73` | One transformed raw preimage now has an exact ten-vertex grade-zero realization and a complete first-row audit.  Its first-response image meets the diagonal target space only on the base line, excluding every edge-matrix completion of that effective data from the global GHZ locus. |
| `GLD73` | completed full-fibre first-response handoff | `GLD74` | The entire affine `35`-dimensional raw fibre is now covered at `q_0`; exact projective certificates exclude the necessary rank-one quotient on every chart, so no further raw preimage of this tensor remains to test. |
| `GLD74` | completed symmetry and local-germ handoff | `GLD75` | The interface orbit is only the tensor-scaling line, while the actual survivor germ is smooth of dimension five and locally equal-leaf in the certified frame gauge.  Four transverse parameters remain, so orbit transport cannot prove the parent theorem. |
| `GLD75` | completed universal-module/boundary handoff | `GLD76` | The exact local response incidence now has a fixed `68 x 4` quotient and only twelve lift variables, with all raw and rank-drop fibres retained.  Leaf symmetry gives exact blocks but two sign directions remain on the projective boundary, preventing the naive properness lift of `GLD74`. |
| `GLD76` | completed sign-boundary compression handoff | `GLD77` | The full three-dimensional sign plane has exactly three reduced projective rank-one points, not merely the two witnesses first exposed by GLD76.  Their ratios are `(1,-1,1)`, `(1,1,-1)`, and `(1,-1,-1)`. |
| `GLD77` | completed sign-boundary nonextension handoff | `GLD78` | Corrected first jets retain all `35` raw, four survivor, and two slope directions.  More strongly, Reynolds reduction to the eight invariant raw directions and three nonzero augmented determinants exclude affine arcs of every order on one named principal open around each pure-sign boundary point. |
| `GLD78` | completed full Gaussian boundary handoff | `GLD79` | Central-idempotent decomposition, Schur compression, and exact determinant covers exclude every trivial, standard, mixed, and non-first-chart direction, leaving exactly the three reduced sign points. |
| `GLD79` | completed existential survivor-open handoff | `GLD80` | Saturate the intrinsic projective incidence by `s`; properness, algebraic DVR selection, and the three `GLD78` determinant units prove its closed image misses `F_0`, hence a principal survivor-open exclusion exists. |
| `GLD80` | completed physical source-interface handoff | `GLD81` | The actual ten-mode source matching identity supplies the physical raw vector, and its `q_0` first variation factors through the complete `17`-coordinate response domain.  Thus every legal GHZ source on the named torus-star branch enters the GLD80 incidence rather than merely the abstract nuisance space. |
| `GLD80` | completed explicit-determinant handoff | `GLD82` | A fixed nuisance solve, exact Reynolds compression, adjugate transport, and fraction-free quotient produce the polynomial circuit `Delta_82`; its normalized Gaussian specialization matches the audited coefficient matrix entry for entry. |
| `GLD81` | completed explicit-open source handoff | `GLD82` | The physical maximal-star source bridge now lands in the explicit `D(Delta_82)` survivor-open exclusion rather than only an existential neighborhood. |
| `GLD82` | completed bordered-Pluecker decharting handoff | `GLD83` | The quotient-chart quadrics are `gamma_num` times exact bordered Pluecker quadrics.  Their coefficient determinant yields a larger principal open and the complete exterior-coordinate family yields an intrinsic Fitting-open reduction. |
| `GLD83` | completed centre-rank cover handoff | `GLD84` | The equal-leaf survivor equations are globally affine-linear in eight center variables.  Their exact determinantal strata give `45` rank-eight charts, `960` rank-seven charts, and a named rank-at-most-six residual. |
| `GLD84` | completed named rank-eight specialization handoff | `GLD85` | One exact six-leaf/two-residual point on the named rank-eight chart has a denominator-checked nonzero maximal minor of the full intrinsic Fitting map.  The old selected `M_Pl` vanishes there, so the handoff is genuinely full-intrinsic. |
| `GLD85` | completed two-leaf residual-slice handoff | `GLD91` | The exact lifted two-variable residual classification corrects the earlier omitted-Gaussian-offset exploratory frame calculation and identifies all boundary fibres plus the unique Schur/frame-open fibre. |
| `GLD91` | remaining rank-eight and global Fitting obligation | `GL` | Extend beyond the two-leaf slice: decide full six-leaf rank-eight unitness or residual components, then compute the other rank-eight charts and the Gaussian rank-seven and lower-rank branches.  Other survivor components/gauges, triangles, residual-coordinate and isotropic boundaries, smaller survivor families, non-star profiles, other root orders, and global resolution remain open. |
| `GLD84` | completed rank-at-most-six boundary handoff | `GLD86` | The exact syndrome minor and `C_8=1` column replacement force every rank-at-most-six point onto the four named divisors, while leaving the divisor-specific analysis to GLD86. |
| `GLD86` | completed three-collision-divisor boundary handoff | `GLD87` | The exact syndrome minor and `C_8=1` column replacement force every rank-at-most-six point onto the four named divisors; GLD87 supplies the exact H1 kernel analysis and H2/H3 leaf-column transport. |
| `GLD87` | completed H4 principal-open handoff | `GLD88` | The collision divisors are gone on `D(Omega)`; GLD88 classifies a nonempty H4 six-pivot open by two exact Schur residuals and excludes it by center singularity. |
| `GLD88` | completed H4 P/d0 boundary handoff | `GLD89` | GLD89 excludes the entire `P=0` divisor and the `d0=0` overlap on `D(Omega)` by exact six-/seven-minor factors, a complete common kernel, and the separate overlap row subsystem. |
| `GLD89` | completed H4 Q6-open handoff | `GLD90` | GLD90 combines the prior principal-open theorem with alternate and auxiliary six-pivot charts, exact residual-curve matching, finite corner seven-minors, and a separate `T=0` two-pivot obstruction. |
| `GLD90` | completed L1/L2 boundary handoff | `GLD93` | GLD93 directly closes both coefficient divisors using the two H4 rational parameterizations, all selected six-/seven-minor identities, solved double-pivot auxiliary minors, and all pivot/T exceptional fibres; it does not use naive p/q carrier symmetry. |
| `GLD93` | remaining H4-boundary/Fitting/component/source-cover obligation | `GL` | Analyze `Q6=0` and the remaining `e=0` coefficient boundary, compute the GLD83 Fitting pullback with full raw response incidence on `C_F` rank drops, and then cover other components/gauges, lower ranks, source branches, profiles, roots, orders and global resolution. |
| `GLD92` | remaining H4 Q6 and global Fitting/component/source-cover obligation | `GL` | Analyze `V(Q6,F28,F31)` and arbitrary H4 Q6 points outside GLD88, close `L1/L2/e` coefficient boundaries, compute the GLD83 Fitting pullback, and then cover other components/gauges, lower ranks, source branches, profiles, roots, orders and global resolution. |
| `GLD19` | remaining response-map-zero witness-locus obligation | `GL` | Force or exclude the literal all-seven `R_S=0` stratum, force a nonzero legal pair package there, or use the full mixed witness equations to exclude its intersecting/sparse-support locus.  A pure selected line is weaker than map zero, and the support classification supplies neither selector attachment nor a permanent bridge. |
| `GLD20` | remaining global map-zero support obligation | `GL` | Exclude the `F=empty` cell or the one-to-three complementary pure-target-absorption cells with genuinely uncontracted mixed coefficients, or force a nonzero legal complete-nuisance operator row.  The finite support atlas is exhaustive for response windows but is neither a witness enumeration nor a permanent bridge. |
| `GLD21` | remaining complete-clique map-zero obligation | `GL` | On the proved `h!=0` residue, integrate the forced pure `G_U(a^4)` slice and dense nuisance absorptions into one same-graph principal-permanent root-companion family and derive a contradiction, or produce a further coefficient detector.  `GLD23` excludes every private colour-diagonal permutation chart; GLD41 closes the single-active-slice cell; GLD42 closes one reciprocal pair; GLD43 forces transpose-matched support with at least two pairs; GLD45--GLD49 pointwise close all `66` two-pair masks; and GLD50--GLD62 pointwise close all `220` three-pair masks.  Four-or-more-pair supports and the proper-secondary-clique cells remain.  The formal solution `G_U=J_Q/h` still shows that fixed-`Q` linear algebra alone cannot close them.  Other `F=empty` and pure-absorption cells remain separate. |
| `GLD22` | completed private-permutation successor | `GLD23` | The common-matching `-2hP` detector is now subsumed in scope by an exact exhaustion of every colour-dependent private permutation.  The elementary proof remains a separately replayable explanation of the identity orbit. |
| `GLD23` | completed first nonprivate successor | `GLD24` | The private-permutation boundary has an exact genuinely nonprivate continuation on the balanced one-switch chart.  `GLD25` subsequently closes its two-independent-amplitude boundary. |
| `GLD24` | completed two-amplitude successor | `GLD25` | The balanced slice is now subsumed by an exact exclusion with both off-diagonal switch amplitudes independent and nonzero.  The separately replayable `GLD24` certificate remains a simpler one-parameter explanation. |
| `GLD25` | completed generic directed-spur successor | `GLD26` | One additional directed support edge now has an exact three-parameter detector away from four explicit divisors.  This is a generic successor, not a pointwise completion analogous to `GLD25`. |
| `GLD26` | completed first divisor successor | `GLD27` | The `uv=-1` component of the generic detector's exceptional locus is now pointwise empty; the generic theorem's other three divisor boundaries remain unchanged. |
| `GLD26` | completed second divisor successor | `GLD28` | The `uv=1` component of the generic detector's exceptional locus is now pointwise empty; exactly two divisor boundaries remain on this chart. |
| `GLD26` | completed third divisor successor | `GLD29` | The `uv-u-v-1=0` component of the generic detector's exceptional locus is now pointwise empty; exactly one divisor boundary remains on this chart. |
| `GLD26` | completed final divisor successor | `GLD30` | The `uv+vw+w+1=0` component is pointwise empty.  Together with `GLD27`--`GLD29`, this exhausts the four-factor exceptional locus of `GLD26`; with the `GLD25` `w=0` boundary, the full directed-spur coordinate family is empty for every `w`. |
| `GLD30` | completed generic reverse-spur successor | `GLD31` | One reverse support edge now has an exact four-parameter detector away from five explicit hypersurfaces.  This is a generic successor, not a pointwise completion analogous to `GLD30`. |
| `GLD31` | completed first divisor refinement | `GLD32` | The `uv=-1` hypersurface now has an exact generic detector leaving four residual surfaces; the other four `GLD31` divisors remain unchanged. |
| `GLD32` | completed first residual successor | `GLD33` | The `u=1` component is pointwise empty; `z=1`, `z=-1`, and `wz=2` remain on the `uv=-1` divisor away from their overlap with it. |
| `GLD32` | completed second residual successor | `GLD34` | The `z=1` component is pointwise empty; exactly `z=-1` and `wz=2` remain on the `uv=-1` divisor away from their overlap with the completed surfaces. |
| `GLD32` | completed third residual successor | `GLD35` | The `z=-1` component is pointwise empty; only `wz=2` remains on the `uv=-1` divisor away from its overlap with the completed surfaces. |
| `GLD32` | completed final residual successor | `GLD36` | The `wz=2` component is pointwise empty.  Together with GLD33--GLD35, this exhausts the four-surface cover and proves the nonzero `uv=-1` divisor empty. |
| `GLD31` | completed second divisor exclusion | `GLD37` | The `uv+wz-1=0` divisor is pointwise empty by two-row contradictions.  Exactly three GLD31 divisors remain. |
| `GLD31` | completed third divisor exclusion | `GLD38` | The `uv+wz+1=0` divisor is pointwise empty by two-row contradictions.  Exactly two GLD31 divisors remain. |
| `GLD31` | completed uniform nonzero-chart exclusion | `GLD39` | The unspecialized two-row relation leaves `w`, closing the full chart and both formerly remaining divisors.  GLD31--GLD38 remain valid but are subsumed on this chart. |
| `GLD39` | completed all-support successor | `GLD40` | Three additional exact two-row detectors and the GLD23 origin close every support-drop face, proving the whole affine coordinate family empty. |
| `GLD40` | completed full-slice successor | `GLD41` | The four-edge family is subsumed by twelve simultaneous entry detectors, one for every off-diagonal coordinate of a full active colour slice. |
| `GLD41` | completed first two-active successor | `GLD42` | A reciprocal off-diagonal pair across two colour slices is excluded pointwise, including its exact curve and exceptional point. |
| `GLD42` | completed full-support reduction successor | `GLD43` | The complete 24-amplitude two-slice ring now has twelve reciprocal divisor constraints and an exact residual support census. |
| `GLD43` | completed generic two-pair successor | `GLD44` | All five two-pair support orbits now have exact sparse function-field contradictions away from explicit denominator divisors. |
| `GLD44` | completed first pointwise orbit successor | `GLD45` | The same-tail exceptional divisor has no residual point, so one of the five minimal two-pair orbit types is fully empty. |
| `GLD44` | completed second pointwise orbit successor | `GLD46` | The disjoint `u=-1` curve and its edge-exchanged `w=-1` branch are empty, closing a second minimal two-pair orbit. |
| `GLD44` | completed third pointwise orbit successor | `GLD47` | The reverse `u=-1`, `w=-1`, and `uw=-1` components are empty, closing a third minimal two-pair orbit. |
| `GLD44` | completed fourth pointwise orbit successor | `GLD48` | The same-head pair-order intersection leaves one curve and one point, and exact contradictions close both, leaving only the chain orbit open among minimal two-pair supports. |
| `GLD44` | completed fifth pointwise orbit successor | `GLD49` | Both directed-chain exceptional curves are empty, completing every minimal two-pair orbit and all `66` labelled masks. |
| `GLD49` | completed first larger-support successor | `GLD50` | All `220` three-pair masks have exact generic contradictions, leaving a finite explicit divisor atlas rather than an unconstrained three-parameter open set. |
| `GLD50` | completed first three-pair divisor successor | `GLD51` | The single directed-path exceptional surface is empty, closing one full three-pair orbit and `24` labelled masks pointwise. |
| `GLD50` | completed second three-pair divisor successor | `GLD52` | Both out-star exceptional surfaces are empty, closing a second full three-pair orbit and `4` labelled masks pointwise. |
| `GLD50` | completed third three-pair divisor successor | `GLD53` | Both fork-path surfaces and their intersection are empty, closing a third full three-pair orbit and `24` labelled masks pointwise. |
| `GLD50` | completed fourth three-pair divisor successor | `GLD54` | All four reverse-disjoint surfaces and their legal overlaps are empty, closing a fourth full three-pair orbit and `12` labelled masks pointwise. |
| `GLD52` | completed fifth three-pair orbit successor | `GLD55` | Exact active-colour exchange and signed nuisance covariance transfer the `4`-mask in-star orbit to the pointwise-empty out-star orbit. |
| `GLD53` | completed sixth three-pair orbit successor | `GLD56` | Exact active-colour exchange and position relabelling transfer the `24`-mask reverse-fork orbit to the pointwise-empty fork-path orbit. |
| `GLD50` | completed seventh three-pair divisor successor | `GLD57` | Four in-fork surfaces and all three legal intersections are empty, closing the full `12`-mask O11 orbit pointwise. |
| `GLD57` | completed eighth three-pair orbit successor | `GLD58` | Exact active-colour exchange and position relabelling transfer the `12`-mask out-fork orbit to the pointwise-empty in-fork orbit. |
| `GLD50` | completed ninth three-pair divisor successor | `GLD59` | Four O6 surfaces and both legal intersections are empty, closing the full `24`-mask orbit pointwise. |
| `GLD50` | completed tenth three-pair divisor successor | `GLD60` | Four O3 surfaces, their five legal intersections, and the final two points are empty, closing the full `24`-mask orbit pointwise. |
| `GLD50` | completed eleventh and twelfth three-pair orbit successor | `GLD61` | Exact saturated denominator coverage closes O2, and active-colour exchange transfers it to O7, closing `48` labelled masks pointwise. |
| `GLD50` | completed final three-pair orbit successor | `GLD62` | Exact saturated and Euclidean denominator coverage closes O9, completing all `13` orbits and `220` labelled three-pair masks pointwise. |
| `GLD62` | remaining dense nonprivate integrability obligation | `GL` | Attack four-or-more-pair supports or find a uniform support-size argument.  Proper-secondary cells and every weighted-permanent bridge remain separate. |
| `BO1` | refutation of ambient bounded-window route | `GL` | Symmetry, restriction functoriality, all bounded physical windows, identifying overlaps, and trivial holonomy do not characterize an unrestricted full deck or response.  A positive bounded-obstruction theorem must use the actual target locus, prove global generative equality, expose the first higher defect as a target coefficient, or establish a uniform structural-degree bound. |
| `G0` | refutation of argument | `C2` | Good reduction to the prime field is not automatic, and the source theorem's local correspondence remains pending. |

| `GLS40` | rank-four zero-excess complete-labelled incidence audit | `GLS43` | On `q notin Delta` and `rank B_Q^anc=4`, use the whole-domain residual--port and distinct-label port--port incidence family to decide whether `B_Q^anc=Delta+Kq` can occur on any shore-rank or divisor fibre. |
| `GLS43` | surviving nonzero-diagonal rank-four incidence audit | `GLS44` | The off-diagonal zero-excess fibre is empty.  Use the complete GLS36 incidence family to decide every nonzero diagonal rank-one/rank-two shore profile without entering a localized selector receiver. |
| `GLS44` | silent residual-shore profile audit | `GLS45` | Every rank-four full-swallow point has `q=p=0`.  Use the complete GLS36 residual--port family to classify every shore-rank and label-support fibre before attacking the remaining pair-family. |
| `GLS45` | complete-pair structural-degree and cut successor | `GLS46` | Unify the residual-free and sparse same-label cores, prove a uniform arbitrary-root effective-dimension bound, and localize all three diagonal directions without silently selecting a port value. |
| `GLS46` | completed triangle/feeder successor | `GLS47` | Synchronize one vector at every triangle vertex, normalize the three triangle edges, and use the transformed physical diagonal to eliminate both the internal two-dimensional edge and external pure-excess feeder mechanisms. |
| `GLS47` | rank-five-through-nine and wider physical attachment obligation | `GL` | Rank four is empty.  Decide or attach full-swallow nuisance ranks five through nine, where the excess has dimension at least two, while retaining response/activity, synchronization, complete nuisance survival, anchors, a named receiver, and source coverage.  Raw escape and nonzero anchor remain separate. |
| `GLS40` | complete two-effective-label target-coupling audit | `GLS48` | Use the one-to-one auxiliary-pair/raw-label factorization and an adaptive coefficient/deck cut to decide every residual--residual, residual--port, and port--port two-label cell without treating a high-rank incidence tensor as one `E_A^*` coefficient. |
| `GLS48` | rank-five three-label target-coupled successor | `GL` | The target forces at least three effective auxiliary labels.  Classify or attach rank-five full swallow on that surviving support, then integrate ranks six through nine, raw escape, nonzero anchor, and every named receiver/source gate. |
| `GLS48` | `D(p)` equality audit | `GLS49` | On `D(p)`, both residual labels are active.  Quotient the unique three-label source by its full `q`-cylinder, then retain both residual-shore rank-one orientations and every physical deck-zero fibre. |
| `GLS49` | other three-label `p=0` kernel/deck successor | `GLS50` | Contract only inactive promoted ports, then use the complete target to decide every joint-kernel and evaluated-deck fibre in the one-residual/two-port and three-port supports. |
| `GLS50` | shared-polarization five-profile classification | `GLS51` | Use the shared `X/Y` polarization to decide the five rank-five profiles without assuming a kernel minor nonzero or treating the evaluated deck lines as responses. |
| `GLS51` | uncontracted inactive-port deck successor | `GLS52` | Retain the common physical port-pair deck before the all-ones inactive-port contraction and compare its two off-coordinate diagonal target rows. |
| `GLS52` | four-promoted-label reconstruction | `GLS53` | When exactly four promoted labels and no residual label are effective, contract only inactive ports and identify the complete source with one reconstructed legal six-vertex graph. |
| `GLS53` | complete-witness partial-uncontraction successor | `GLS54` | Start before fixed-residual contraction, retain every active residual vertex, and pad a short activity set only with inactive promoted ports. |
| `GLS8` | full-map torus-kernel contraction | `GLS55` | Return to every original residual and promoted joint incidence map.  If at most four kernels miss no fully supported vector, retain a four-set containing all rigid labels and contract every outside non-rigid label at its own torus-kernel vector. |
| `GLS55` | uniform pointwise activity corollary | `GLS54` | Every full-map rigid promoted label is whole-domain active, and every fully supported residual vector avoids a rigid residual kernel.  Thus the five fixed rigid labels lie in every pointwise GLS54 activity set; GLS54 is comparison-only and not a proof dependency of GLS55. |
| `GLS55` | exactly-five-rigid / six-plus-rigid successor | `GL` | On `|Rig|=5`, contract every non-rigid label to obtain the exact seven-party identity with ten trilinear physical decks.  Six-or-more rigid labels remain a separate open branch.  In both branches, coordinate readout alone is not nuisance survival, synchronization, response activity, or a named receiver. |
| `GLS8` | nonrigid probe-kernel matching contraction | `GLS56` | At one fully supported joint-kernel vector, use the complete promoted identity and a colourwise covector alternative.  If no pure neighbour exists, kill every matching through the silent label while retaining one nonzero pure target coefficient.  Irreducibility then promotes the pointwise escape to fixed restricted shores and a complete exceptional-section flag. |
| `GLS55` | root-order-three rigid/nonrigid bifurcation | `GLS56` | With six auxiliary labels and at least five rigid, either all six are rigid or the unique nonrigid label receives the simultaneous three-colour pure-star conclusion.  This is exhaustive only as a source-structure split, not as an attachment cover. |
| `GLS56` | rigid coupling / alternate-receiver successor | `GL` | On the all-six-rigid branch, `GLS57` handles the all-rank-one cell and `GLS58` gives an exhaustive but nonexclusive higher-rank profile reduction.  `GLS59` now handles the unique-nonrigid source structure: old-probe exchange forces overlapping pure probe stars and closes the natural `GLD3` re-anchor because its star triangle cannot be target-diagonal.  A different legally transported receiver or complete-equation exclusion is still required, with every response, selector, synchronization, nuisance-survival, activity, and anchor gate.  For `r>=4`, neighbour rigidity and arbitrary-root receiver coverage remain separate. |
| `GLS56` | all-six-rigid rank-one refinement | `GLS57` | At `r=3`, assume all six rigid joint maps have rank one.  Coordinate-row rigidity and the complete pure/mixed target equations force the exact `2+2+2` partition, pure pair companions, pure off-readout deck faces, and at least one nonzero promoted pair response polynomial. |
| `GLS57` | pure-shore orientation / natural-splice audit | `GLS60` | Factor each pure same-colour companion through its two probe shores, retain the zero-edge boundaries, and distinguish the contracted hafnian first variation from both a six-vertex matching graph and the permanent `P_6` tensor. |
| `GLS60` | remaining rank-one rigid receiver successor | `GL` | The direct companion graph and vertex-gauge splice are impossible.  Use additional complete mixed/deck equations to construct a demonstrably non-gauge honest six-vertex graph, or transport the raw pure-probe data into one promoted target quotient with pointwise response, selector, synchronization, nuisance-survival, activity, and anchor gates.  A separately proved permanent `P_6` extraction enters the open permanent subtree, not the six-vertex theorem.  Higher joint ranks, the unique-nonrigid branch, response divisors, and arbitrary-root coverage remain separate. |
| `GLS56` | all-six-rigid higher-rank refinement | `GLS58` | Split by the number of joint maps of rank below three.  One deficient label gives fixed boundary pure shores and ten trilinear decks; two give a legal six-vertex descent with at most two target colours; none gives the injective cross-product polynomial identity. |
| `GLS58` | remaining rigid mixed-equation successor | `GL` | Couple the zero/mono/binary descents across kernel choices or contradict the all-injective coordinate-cover/cancellation fork using additional complete mixed equations.  The accepted three-colour six-vertex theorem and the cross-product identity alone are sharp no-gos.  Every response, selector, nuisance-survival, synchronization, activity, anchor, arbitrary-root, and nonzero-anchor gate remains separate. |
| `GLS56` | unique-nonrigid old-probe exchange and overlap | `GLS59` | At zero anchor, kill every complete matching by the chosen old probe rather than by the nonrigid auxiliary label.  Uniformize the resulting pointwise pure shores on each old-probe space, overlap the two three-label stars among five rigid labels, and contract the resulting second deficient label together with the fully supported nonrigid kernel. |
| `GLS59` | remaining unique-nonrigid mixed-equation/attachment successor | `GL` | Couple the mono/binary descents across all overlap labels and coordinate-plane kernel choices, or transport a forced pure probe block into one named promoted target quotient with nonzero response and complete nuisance survival.  One overlap and the accepted three-colour six-vertex theorem are insufficient.  Alternate receiver, synchronization, activity, anchors, arbitrary-root source coverage, all-rigid branches, and nonzero anchor remain separate. |

## Smallest positive next obligations

These are positive theorems or exact decisions that would advance a surviving
branch. They are not an instruction to begin all of them at once.

1. **Maximum-root same-pair target attachment.**  `GLS4` closes the
   all-pairs individual-supply failure: in every surplus-two maximum-root
   complex witness, one same residual pair has a nonzero physical pair block,
   a nonzero complementary permanent, an order-two companion class surviving
   modulo all higher columns, and a fully-supported nonzero `p_(A,Q)`.  It
   does not make the full sensor pair-observable or make the complete
   fixed-`Q` coordinate family observable.  More importantly, it does not
   supply a legal GLD response/target selector on that pair.  The scalar
   complementary-permanent map is dominant, so no universal polynomial
   identity among those scalar readings can provide the missing attachment.
   The smallest remaining source edge is therefore to attach a complete legal
   package to at least one supplied pair, or exclude every such attachment
   failure with complete mixed equations.  If the chosen downstream theorem
   needs collective or full fixed-`Q` observability, that stronger rank must
   also be proved.

   `GLS5` now closes the quantifier-compatible failure encoding.  Pointwise
   absorption on every fully-supported contraction is equality of all
   geometric radical Fitting profiles; response-gated failure is an exact
   response-ideal containment; and, on the complete GLD7 witness equation,
   the three pure columns give an equivalent profile.  One shared-residual
   incidence ideal encodes common attachment without a 730-rank-stratum
   atlas.  GLS2 failure remains a separate function-field projected-kernel
   locus with a finite coefficientwise rank-stratum formula.  An exact
   maximal-nuisance-rank module has injective sensing, three pure targets, and
   nonzero response but no legal decomposable selector, so the physical
   bridge cannot follow from ranks or unrestricted recovery alone.

   The exact `r=3` physical fibre still shows that maximum-root data, quotas,
   local concision, pure normalization, and the Hamming-one shell do not force
   collective or fixed-`Q` observability; actual higher mixed equations remain
   indispensable.  `GLS6` synchronizes `h!=0` and raw `p!=0` on one
   fully-supported contraction.  At four roots it classifies ambient
   augmented-alignment failure exactly by `p^T Jp=0` and
   `Jp in im mathcal U^*`, and gives the exact annihilator condition after
   intersecting with a proposed legal-weight space `M`.  This covers every
   rank without division, but neither forces `M` nor supplies the response,
   synchronized nuisance, or target-pure anchor required by the GLD2 route.

   `GLS7` provides the first actual-witness source cover at root order four:
   `{observable O, quotient circuit C} x {response zero R, common seven-row
   escape E, function-field pure absorption A}`.  Both `O x E` and `C x E`
   reach the required individual-supply plus legal same-`Q` GLD5/7 interface;
   O adds stronger separation from the other order-two columns.  The four R/A
   leaves remain open for this stronger all-seven package, as do absorption
   denominators and exceptional rank-drop fibres.  A full-rank
   order-two physical control with seven nonzero responses still has all
   seven selectors swallowed; one complete mixed coefficient excludes it.
   `GLS8` supplies the exact isolated-one-row correction.  A single R or A target is not
   a bad one-row leaf if another target is useful.  Exact four-root failure is
   simultaneous response-gated radical containment for every target and every
   GLS4-eligible `Q`, including every exceptional fibre.

   More generally, `GLS8` re-roots at the GLS4 probe pair and promotes all
   other roots.  At every root order `r>=3` this gives only top-minus-two and
   top deck grades, forces one desired coefficient to survive the unique top
   column, and reduces legal nonzero attachment to the same pointwise Fitting
   profile.  This is a uniform promoted-module reduction to a legal isolated
   one-row criterion, not
   proof that a useful row exists.  At `r=3` the promoted shapes are the six
   pairs and four-port target, but one row is not the full GLD3 package; for
   `r>=4` the promoted top layers do not by themselves match a committed
   downstream detector.  The smallest physical obligation for this reduction is a
   same-graph complete-mixed identity contradicting the simultaneous failure
   profiles.  The strategic node still separately requires a proved common
   package satisfying every synchronization, alignment, activity, nuisance,
   and anchor gate of a named downstream theorem.

   `GLS20` contracts the complete promoted top-minus-two module along the
   same maximum-root probe vectors used by the source.  For each source
   Laplace pair `C subset U`, the resulting target quotient has only nine
   coefficient rows.  Base survival is exactly a legal selector factoring
   through that contraction, while the source identity
   `Pi_Q=sum_C b_C tensor Per_(K_0,U-C)` forces some raw `b_C` nonzero and
   records universal base absorption as a nonzero nuisance circuit.  On the
   complete target, usefulness is exactly base survival plus nonzero promoted
   response, with every rank-drop fibre encoded by the nine-row Fitting
   profile.  `GLS21` then identifies the retained `D=Q` all-port nuisance:
   after the same contraction it is exactly `p_(A,Q)I_9`.  Therefore on the
   required `p!=0` source gate every base nuisance is full and the GLS20
   Fitting failure profile is automatic.  This closes the factor-through base
   route as a no-go, not the full `81`-row promoted quotient.  Any continuation
   must retain the probe-root directions upstairs or use a different legal
   joint identity; it may not delete the all-port label.

   `GLS22` now performs the exact legal continuation.  On `D(p)`, the operator
   `P_Q=pI-q tensor epsilon_A` has kernel precisely the retained all-port root
   line and image `ker epsilon_A`.  It therefore identifies every full GLS8
   quotient with a transverse quotient of `72` rows for top-minus-two targets
   and `8` for the top target.  Full legal survival and response-gated pure
   rank are equivalent after projection, including every exceptional rank
   fibre.  The source aggregate satisfies `T_Q=pF_Q-q tensor Pi_Q`, splitting
   raw transverse nonvanishing from projective synchronization.  Neither
   branch is yet excluded or assembled into a downstream package.

   `GLS23` expands those projected nuisances exactly.  A complement pair `D`
   contributes the slices of its projected companion on `D_0-C`, tensored with
   the full missing left factors `C-D_0`; the sum over all unwanted labels is
   the complete nuisance.  Disjoint root slices spanning `ker epsilon_A` fill
   a pair target outright.  The projected top term supplies the common anchor
   `omega=W_(a_0,a_1)`: if zero, the top desired row vanishes; if nonzero, all
   pair targets reduce exactly to `63` rows while the top target survives only
   if `omega` escapes its explicit eight-row root-slice span.  This is an exact
   physical failure topology, not an exclusion of either anchor branch.

   `GLS24` filters the nonzero-anchor branch at the actual probe-root vectors.
   Each one-probe contraction maps the eight transverse root rows onto a
   two-space.  A nonzero anchor marginal then defines a denominator-free
   exterior quotient with one root row, hence an exact nine-row pair module.
   The zero, nonzero-marginal, and nonzero double-transverse anchor branches
   are exhaustive.  At `r=3`, all six useful rows through one common marginal,
   a useful top row, and three-colour activity enter `GLD3`; any failed row,
   top absorption, or low-activity branch remains.  Failure of the marginal
   route does not imply failure of the full `63/72`-row selector problem.

   `GLS25` handles the complementary nonzero double-transverse anchor branch.
   The all-port tensor `q` and `p!=0` define a scaled idempotent onto the exact
   four-dimensional double core.  Wedging by `omega` gives three root rows,
   hence exact `27`-row pair modules; the top desired anchor instead uses the
   unwedged four-row core map.  At `r=3`, simultaneous usefulness of all six
   pair modules and the top module plus activity enters `GLD3`.  Reduced
   failure still does not imply full failure, and neither usefulness nor
   activity is forced.

   `GLS26` returns to the zero-anchor fibre.  The complete top-target GHZ
   quotient now forces the projected diagonal root space, of dimension two
   or three, into the exact remaining nuisance.  Every label meeting `Q`
   once is confined to the projected residual-shore tangent
   `P_Q(X_0 tensor V_1^*+V_0^* tensor X_1)`, whose dimension is at most
   seven.  Modulo this tangent, the diagonal reconstruction either forces an
   essential nonzero promoted pair slice or the two residual shore spans
   cover all three coordinate lines.  This is an exact generic/exceptional
   localization, not survival in the essential pair's own target quotient;
   the coordinate-shore cover and every response/activity gate remain open.

   `GLS27` retains the residual contraction as a Laurent family.  If the
   coordinate-shore cover fails at the function-field point, exact rank and
   augmented minors preserve that failure on a nonempty principal open, so an
   actual contraction enters GLS26's essential-pair branch.  Otherwise one
   fixed cover persists generically and has only the `C12`, `C21`, or `C22`
   shore normal form.  The GLD11 graph realizes `C21` with all source gates,
   pure normalization, Hamming-one vanishing, and response nonvanishing; its
   displayed mixed coefficient excludes it.  Thus complete mixed equations,
   rather than genericity alone, must eliminate or attach the three forms.

   `GLS28` now compares each essential promoted pair with its own complete
   pair-target nuisance.  On the zero-anchor branch that nuisance is contained
   in the explicit envelope generated by the residual-shore tangent and every
   other pair supplier.  A supplier outside the envelope gives a legal full
   selector; a projected pure diagonal outside it gives the stronger named
   nonzero-response row.  If every useful row fails, the diagonal defect is
   deletion-stably covered in a quotient of dimension at most four.  Actual
   full absorption yields relations on at most five supplier labels, but
   useful-row failure alone does not: a surviving zero-response direction is
   an exact sharp obstruction.  The redundant cover, exceptional fibres,
   `C12/C21/C22`, synchronization/activity, and arbitrary-root downstream
   entry remain open.

   `GLS29` resolves the one-dimensional quotient's physical normal channel.
   On `(d_0,d_1)=(2,2)`, the two shore normals identify
   `E/P_Q(T_Q)` and factor every promoted supplier as
   `x_u tensor y_v+y_u tensor x_v`.  Applying that normal to the exact GLS23
   nuisance gives target cylinders, while applying it to the complete physical
   equation gives one denominator-free arbitrary-root mixed-response identity.
   Every active normal colour occurs in two local channel spans and has a
   supplier with both nonzero pure coefficient and response.  Full three-colour
   activity excludes intersecting supplier support at arbitrary root order.
   At `r=3`, complementary kernel contractions exhaust all local ranks and
   force `gamma_0 gamma_1 gamma_2=0`; thus the full-activity locus is empty,
   including every response-zero fibre.  The surviving normal-product divisor,
   the `r>=4` disjoint-supplier branch, other shore ranks, and all simultaneous
   selector/synchronization gates remain open.  A rational graph-side control
   with six full nuisances and six nonzero responses fails an original mixed
   coefficient, confirming that the complete physical equations remain
   load-bearing.

   `GLS30` resolves exactly how far the surviving four-port normal-product
   divisor can be pushed inside that scalar channel.  Complement-kernel
   contraction isolates one supplier at arbitrary root order without dividing
   by a response or coordinate.  The resulting one-active and two-active
   projected-kernel profiles retain all silent zero-star fibres.  Exact
   one-graph response decks realize both profiles with six nonzero responses
   and full normal nuisance images; a separate one-active graph additionally
   has a maximum torus root, pure normalization, and the exact normal tensor,
   but fails Hamming-one coefficients.  Therefore the complete normal identity
   plus six responses and full normal images is insufficient, and maximum-root
   plus pure normalization separately does not upgrade that scalar identity to
   a witness.

   `GLS31` resolves the proposed combined static coupling.  One exact rational
   graph has a maximum root, incidence defect six, pure normalization, six
   nonzero responses, simultaneous complete pair absorption, full normal
   images, the scalar normal identity, and the projected-diagonal inclusion,
   while failing `313` original mixed words.  Thus those gates can coexist and
   cannot by themselves force a selector or contradiction.  Polarizing the
   two retained `A` slots along the shore normals gives two exact first-degree
   equations, but each necessarily keeps all one-`Q` labelled nuisance terms;
   the induced one-dimensional quotient is just the old product-normal
   channel.  Coupling those complete equations to every divisor/rank fibre is
   the next tested route.

   `GLS32` proves that this entire projected route is still insufficient on
   the one-active fibre.  Its arbitrary-root singleton-kernel contractions
   retain every labelled one-`Q` term and every silent zero-star fibre.  Yet
   one exact rational graph satisfies the complete first-polarized equations,
   the normal equation, hence the whole projected evaluation pencil, together
   with maximum-root incidence, pure normalization, six responses, full
   normal images, complete pair absorption, and the projected-diagonal
   inclusion.  It fails `316` original mixed words.  The smallest surviving
   equation family must therefore resolve residual-`Q` colours or actual-root
   directions outside the shore-normal evaluation plane; the two-active and
   arbitrary-root branches remain open.

   `GLS33` supplies both missing equation layers without localization.  Signed
   shore minors make the complete first-polarized and normal equations exact
   polynomials over the residual family, retaining every divisor and rank-drop
   fibre.  The unprojected constant coefficient has a separate physical
   `pH_Uhat` term; contracting the other suppliers by their exact local
   `ker a_u intersect ker b_u` spaces isolates its target-diagonal class.  The
   `GLS32` graph is detected coefficientwise: its fixed-point first-polarized
   cancellations split into `76+76` opposite residual monomials, and its
   constant kernel identity reads `2=1`.  Anchor survival, response coupling,
   two-active and other-shore fibres, and arbitrary-root source coverage remain
   open.

   `GLS34` computes the exact algebra left by those layers.  Coefficientwise,
   the four residual profiles have a `75/81` observation rank on a nonempty
   ambient shore-data Fitting open; no intersection with the witness locus is
   asserted.  The six blind coefficients are precisely the two shore
   tangent-root incidence syzygies, while one block-rank formula retains every
   exceptional fibre.  Pointwise, the constant diagonal either forces one
   nonzero root-deck value and simultaneous singleton anchor-class survival at
   every port, or lies in a completely classified local-cylinder locus.  With
   three colours, every surviving silent term is projectively aligned at all
   but at most one port.  These are output-side classes, not legal complete-
   nuisance selectors.  The remaining coupling must kill the simultaneous
   tangent/Segre locus or prove the coefficient-side selector rank jump.

   `GLS35` corrects the type of that proposed jump.  The complete raw
   non-`Q` span `B_Q^anc` belongs to a newly re-labelled residual-absent anchor
   problem, and `q notin B_Q^anc` isolates `H_Uhat`; `P_Q` erases this extension
   class because `q` is nuisance for every original promoted target.  On the
   complete target, non-silent output therefore splits exactly into anchor
   escape or simultaneous swallowing of all three raw pure probe tensors.  A
   rational local graph satisfies the all-port kernel equation and all four
   surviving singleton identities while one one-`Q` slice is literally `q`,
   so output survival alone cannot force escape.  At `r=3` the selected
   `H_Uhat=C(B)` is not GLD3's residual-present `T`; no named detector entry has
   been supplied.

   `GLS36` isolates the exact algebra that a successful swallowed-branch
   contradiction must see.  At zero anchor, `B_Q^anc` is the image of a map
   made only from root-to-residual and root-to-port incidence blocks.  Every
   fixed common coefficient annihilator is therefore silent after `q` and the
   three pure rows are swallowed.  At each fixed residual contraction, the
   mixed promoted-port equations survive only as a labelwise lift into the
   kernel of that incidence map, with each component weighted by its own
   complementary physical deck; one contraction is not the full uncontracted
   target family.  This distinction is
   sharp: the GLD11 maximum-root graph has rank-eight full swallow and its
   entire two-probe flattening image equals `B_Q^anc`, while all seven
   responses remain nonzero.  It lies on the diagonal-silent side and is
   excluded by `116` mixed coefficients.  The next theorem must therefore be
   deck-coupled and label-dependent; another fixed common quotient row or
   generic incidence-rank claim cannot close the branch.  Tangent and Fitting
   equations may still constrain which witness-locus fibres occur.

   `GLS37` removes the smallest two-shore full-swallow fibre pointwise.  Full
   swallow at nuisance rank three makes the nuisance exactly the three-colour
   diagonal.  If both residual shores had rank two, the diagonal rank-two root
   deck would pin both shores and every incidence generator to one two-colour
   plane, whose diagonal part has rank only two.  Thus the surviving
   alternatives are precisely a shore-rank drop at nuisance rank three or
   nuisance rank at least four.  This argument is arbitrary-root and uses no
   divisor.  A separate exact graph shows that q-swallow, local output
   non-silence, zero labelled decks, and every mixed-port lift can coexist
   while one pure-port coefficient fails.  Hence that mixed-only premise is
   insufficient; any exclusion needs at least one additional full-witness
   gate absent from the control.  The original-target selector,
   response/activity, synchronization, nuisance survival, and source cover
   remain open.

   `GLS38` closes the shore-rank-drop half of that minimum-rank alternative
   whenever the root-companion coefficient `q` is nonzero, hence in particular
   on the live non-silent branch where `p!=0` implies `q!=0`.  The swallowed `q` is
   nonzero.  A rank-one residual shore makes it a rank-one diagonal tensor on
   one colour; the missing off-diagonal rows then force every port incidence
   on that probe shore onto the same coordinate axis.  All raw incidence
   columns collapse to one diagonal line, contradicting three-colour full
   swallow.  Together with `GLS37`, no nonzero-`q` rank-three full-swallow
   fibre remains; the exact zero-anchor non-silent full-swallow remainder
   starts at nuisance rank four.  At this stage ranks four through nine and
   rank-three `q=0` remained open; `GLS39` below closes the latter only under
   the declared full-swallow premise.  The silent/escape branches, every
   original target gate, and source coverage remain open.

   `GLS39` removes the conditional rank-three `q=0` full-swallow remainder
   without assuming a shore rank.  Treat the two residual labels as
   one-dimensional members of the same whole-domain incidence family.  Their
   mutual polarization is `q`; residual-port and port-port polarizations are
   exactly the components of `sigma_Q`.  A characteristic-not-two
   pairwise-diagonal-family lemma bounds the combined image by two, whereas
   rank-three full swallow would make it `Delta`.  Hence the zero-anchor
   **full-swallow** remainder universally starts at nuisance rank four.  This
   does not force silent `p=0` source points into full swallow.  Ranks four
   through nine, raw escape, every original target gate, and source coverage
   remain open.

   `GLS40` makes the rank-four-through-nine aggregate boundary exact.  The
   complete fixed-residual deck aggregate lands in `Delta+Kq`; the pulled-back
   rows canonically dual to `B/(Delta+Kq)` form the `k-3` or `k-4` labelwise
   incidence syzygies that cancel after deck insertion and annihilate every
   available raw anchor/pure normalization.  On `D(p)`, every promoted pair target is
   confined to a `27,36,45,54,63,72`-row cylinder.  Exact rank-five and
   rank-six controls show that polarization plus the mixed lift, and even a
   freely assigned fixed-residual full aggregate equation, are insufficient:
   the former fails the pure deck flattening and the latter is not proved to
   arise from one physical matching graph.  Simultaneous principal-permanent
   compatibility, target survival and response, synchronized activity,
   source coverage, and node closure remain open.

   `GLS41` removes the apparent high-rank growth from the useful-response
   question without claiming survival.  The quotient of the `GLS40` cylinder
   by `P_Q(Delta) tensor V_C^*` is canonically the root excess quotient tensored
   with the pair slots.  The complete target identity makes every surviving
   desired class there response-zero.  Hence every useful nonzero-response
   row is represented in the `27`-row (`q notin Delta`) or `18`-row
   (`q in Delta`) pure core, and its exact obstruction is the complete
   nuisance intersection with that core on the same fibre.  The intersection
   can jump even when the excess projection is constant, so generic
   complements and chosen minors remain invalid.  Pure-core survival,
   response, synchronization/activity, a named receiver, `p=0` source
   coverage, raw escape, and node closure remain open.

   `GLS42` lifts a fixed-point excess row back to the uncontracted physical
   matching identity.  On the zero-anchor branch every constant row in
   `Ann(Delta)` gives the exact one-edge hafnian first variation, and
   trace-zero vertex gauges form an explicit family inside its kernel.  An
   eight-vertex physical control retains rank-six full swallow, nonzero
   `H_Q,Pi_Q`, `p(z_Q)=2`, root-root orthogonality, and four detected nonzero
   decks while one selected excess row is such a gauge.  Two of those decks
   are promoted-pair responses and two are one-`Q` nuisance decks.  A different
   root row fails the GHZ equation, so the control is not a witness and does
   not decide pure-core containment.  Closing the branch requires additional
   GHZ-row/target coupling or nonlinear principal-deck compatibility, plus all
   response, synchronization/activity, receiver, exceptional-fibre, and
   source-coverage gates.

   `GLS43` removes the unique off-diagonal zero-excess rank-four line.  If
   `q notin Delta`, full swallow and rank four would make the complete
   incidence image exactly `Delta+Kq`.  Low residual shores cannot generate
   all three diagonal rows after quotienting by the residual line.  When both
   shores have rank two, diagonal covariance, row/column alignment, and the
   exact three-coordinate compatibility lemma confine every port image to one
   line and the total labelled incidence image to rank at most three.  Thus
   the rank-four remainder is only `q in Delta`; it carries one excess row.

   `GLS44` then removes every nonzero diagonal point.  Rank-two `q` pins both
   residual shores to one two-colour plane, and the missing-colour cross-block
   projection contradicts the one-dimensional excess.  Rank-one `q` pins one
   shore to a root-colour axis; the left quotient and right root-column test
   produce two independent vectors against that same excess line.  Thus every
   rank-four full-swallow point has `q=p=0`, and `D(p)` begins at rank five.
   The silent rank-four fibre lies outside the GLS40/41 transverse receiver.
   Ranks at least five and every response, attachment, raw-escape, silent,
   and source-cover obligation remain open.

   `GLS45` classifies that silent fibre before any new target localization.
   Zero root deck permits six residual-shore rank profiles.  Four one-shore-
   zero profiles exceed rank four by fixed-factor dimension, and dense
   rank `(1,1)` polarizes two fixed-factor aggregate spaces whose common
   excess line collapses both port shores to one two-colour plane.  The only
   surviving rank-four incidence cores are residual-free `(0,0)` and sparse
   `(1,1)` with one common active residual label.  Neither is yet excluded,
   and neither enters an existing response/attachment receiver.

   `GLS46` unifies those cores without a support atlas.  Each global left or
   right coordinate family meets at most two labels, so joint-kernel
   quotienting leaves total effective domain dimension at most twelve,
   uniformly in the promoted root order.  A separate two-block determinant-
   cubic theorem bounds every label cut to two diagonal directions.  Thus
   three-colour diagonal supply is forced onto one triangle of independent
   edge lines; all other edges are diagonal-silent, and only a two-dimensional
   triangle edge or an external pure-excess feeder can supply the fourth
   direction.  The exact symmetric triangle shows why global diagonal rank
   two is false, but spans only three dimensions.  Both fourth-direction
   forks and every wider attachment/source obligation remain open.

   `GLS47` closes both forks.  The product of the three nonzero triangle-edge
   diagonal coefficient forms supplies a synchronized vector at each label.
   Their factor matrices are invertible, so a left--right change of basis
   makes the triangle the symmetric zero-diagonal three-space.  The
   transformed physical diagonal is a rank-one basis; its common quotient
   skew would trap all left factors in one plane, and therefore vanishes.
   Its common diagonal has all three entries nonzero.  In that normal form
   every external vector is zero and every triangle block is one-dimensional,
   so no fourth image direction survives.  Both GLS45 cores are empty and
   zero-anchor full swallow now has nuisance rank at least five.  This does
   not force silent full swallow or address any wider attachment/source gate.

   `GLS48` closes the entire two-effective-label target cell without a support
   atlas.  GLS39 identifies auxiliary pairs with the raw physical labels.
   When at most two labels are effective, only one coefficient/deck summand
   can remain.  Moving its zero, one, or two open port variables to the probe
   shore makes that summand rank one across the complementary-port cut,
   whereas the exact GHZ target has rank three and at least two ports on the
   other shore.  The tempting `E_A^*|Uhat` cut is invalid for residual--port
   and port--port labels because their incidence tensors can have higher
   rank; the adaptive cut is load-bearing.  Rank-five full swallow with at
   least three effective labels, higher ranks, and every attachment/source
   gate remain open.

   `GLS49` excludes the entire residual-pair-plus-one-port support.  If `q=0`,
   only two source-left generators remain.  If `q!=0`, the full cut source is
   those two tensors plus a three-dimensional `q`-cylinder.  Modulo that
   cylinder the three target columns force pure `q`; its residual rank-one
   factorization and the other two target columns then force an at-most-two-
   dimensional residual shore to contain all three coordinate axes.  On
   `D(p)`, both residual labels are active, so every target point has at least
   four effective labels.  Here `p=epsilon_A(q)` is a root-deck coefficient
   evaluation, not a physical response.  The proof supplies activity only,
   not a legal response/selector package, and leaves the other `p=0` three-
   label types, the four-label cell, and all source/attachment obligations.

   `GLS50` now exhausts those other exactly-three-label `p=0` support types
   at rank five.  Contracting only inactive promoted ports preserves the
   three nonzero target colours and turns every surviving principal deck into
   its exact scalar or covector slice.  With one residual and two ports, the
   port-pair deck scalar cannot vanish, each port joint kernel is at most a
   line, and the two-line profile would collapse the entire incidence image
   into `Delta`; only `(1,2,3)` and `(1,3,3)` remain.  With three ports, the
   target triple quotient forces the three opposite-pair deck lines to be a
   permutation of the coordinate lines, each joint kernel is at most a line,
   and at least one port is injective; only `(2,2,3)`, `(2,3,3)`, and
   `(3,3,3)` remain.  These five profiles are not proved realizable or empty,
   and the coordinate deck permutation is not a downstream response or
   selector package.  Shared `X/Y` polarization and principal-deck coupling
   are the smallest remaining load-bearing structure in this cell.

   `GLS51` applies that shared polarization before fixing nuisance rank.  In
   the three-promoted-port support, restricting each joint map to the kernel
   of its mandatory coordinate deck leaves three pair images inside `Delta`
   that contain `Kr_2`, `Kr_1`, and `Kr_0`; this contradicts the complete
   GLS39 rank-two bound and removes every kernel profile.  In the one-
   residual support, a denominator-free shifted determinant puts both deck
   covectors on one coordinate line.  The unmatched zero graph then kills
   both shifted deck-coordinate vectors, makes the residual shores pure, and
   leaves only the separated crossed-square orientation.  The two port maps
   are injective and the complete incidence image is exactly `Delta` plus
   four star matrix units, hence rank seven.  Therefore exactly three labels
   can survive only in this rank-seven normal form.  Its principal-deck
   realization is not proved; four-or-more labels and all source/attachment
   obligations remain open.  The evaluated coordinate decks are still not
   responses or selectors.

   `GLS52` closes that conditional rank-seven branch by returning to the full
   inactive-port tensor.  In the one-residual/two-port normal form, both
   residual--port images lie in the common-coordinate star.  Each of the two
   other diagonal rows therefore sees only the port-pair polarization times
   one shared physical complementary deck.  The contracted target makes both
   polarization coefficients nonzero; the uncontracted target forces the
   shared deck to be the pure inactive-port word in each off-coordinate
   colour.  Those words are independent because at least two inactive ports
   remain.  Thus the one-residual support is empty, and GLS49/GLS51 make the
   entire exactly-three-label locus empty.  Zero-anchor full swallow now
   requires at least four effective labels.  The load-bearing remainder is
   four-or-more-label target coupling, not a rank-seven principal-deck or
   kernel-profile search.

   `GLS53` decides the no-residual equality case without a new support atlas.
   If the four effective labels are promoted ports, fixed-residual and
   inactive-port contraction leaves exactly six promoted pair terms.  Those
   terms are the complete hafnian of a reconstructed legal six-vertex graph on the two
   probes and four ports, with the evaluated complementary decks serving as
   the port--port edge blocks.  The target has three nonzero pure weights,
   normalized by one local diagonal scaling, and the accepted six-vertex
   theorem excludes it.  This includes the empty inactive set at `r=3` and
   every rank/divisor/deck fibre.  The one-residual/three-port and two-
   residual/two-port four-label supports, all five-plus supports, and every
   source/attachment obligation remain open.

   `GLS54` closes both residual-containing four-label types and, by padding
   smaller activity sets with inactive promoted ports, proves the stronger
   floor five.  The quantifier order is essential: start with an actual
   complete witness, fix the residual point, retain active residual vertices
   directly from the full identity, and keep inactive residuals contracted at
   the vectors that kill their shores.  Every outside raw pair then vanishes,
   while each surviving complementary deck is a bilinear edge on the other
   two of four retained vertices.  The same six-vertex theorem applies.
   Full swallow is not used.  This is not a theorem about an arbitrary single
   fixed-residual equation, and it supplies no attachment gate.  Five-plus
   physical-deck coupling is the remaining zero-anchor activity branch.

   `GLS55` strengthens this to a residual-point-independent full-map floor.
   A label is rigid when its joint two-probe kernel misses the local torus.  If
   there were at most four such labels, leave a four-set containing them and
   contract every outside label at its own torus-kernel vector.  The same
   weighted six-vertex contradiction applies.  Thus at least five labels
   contain a coordinate covector in their joint probe-incidence row spaces
   and are active at every fully supported residual point.  The coordinate
   may vary with the label, and the resulting row is not a response, legal
   complete-nuisance selector, synchronized projective line, or target anchor.
   On the equality branch `|Rig|=5`, contracting every non-rigid label leaves
   ten trilinear physical decks on seven open vertices; they are not graph
   edges.  The six-or-more-rigid branch has no five-label contraction.
   Equality-branch deck coupling, the six-plus branch, and named receiver
   entry all remain open.

   `GLS56` decides what a nonrigid label itself forces.  At every fully
   supported point of its joint probe kernel, the complete promoted identity
   supplies three distinct coordinate-pure neighbours, one for each target
   colour.  On the whole kernel, finite irreducibility gives one fixed
   nonzero pure restricted shore per colour and one torus point activating
   all three; a descending linear-section flag retains every exceptional
   divisor.  Rigid readouts have an exact same-coordinate cancellation
   trichotomy: common pure probe axis or projective anti-synchronization.  At
   zero-anchor `r=3`, the source structure is therefore all six rigid or one
   unique nonrigid label with a star into rigid neighbours.  This is not an
   attachment cover.  The natural `GLD3` re-anchor has `h=0`, and a
   target-diagonal star triangle is forced identically zero, so its
   three-colour activity gate fails.  The all-rigid branch needs complete
   mixed/deck coupling; the star branch needs either a complete-equation
   exclusion of this low-activity cell or a differently transported legal
   receiver.  For higher root order, the star neighbours are not forced
   rigid.

   `GLS57` decides the all-rank-one part of that all-six-rigid branch at
   zero-anchor `r=3`.  Rank-one rigidity assigns one coordinate readout to
   each of the six labels.  The complete pure target forces exactly two labels
   of each colour, and the unique same-colour pair term gives the full pure
   probe/pair companion times a nonzero complementary physical-deck
   coefficient.  The complete mixed equations give a master identity on
   every auxiliary word; each same-colour complementary deck is pure on its
   off-readout `2 x 2 x 2 x 2` face.  At least one same-colour pair avoids
   `Q`, so one named promoted pair response polynomial is nonzero and can be
   retained on a common torus open with the two `GLS4` gates.  The formerly
   suggested old-probe `GLD3` window is pointwise impossible: every pair
   response has only the cell `(kappa(s),kappa(t))`, so each port has diagonal
   activity in at most its one readout colour, never all three.  Pointwise
   response divisors, complete-nuisance survival, legal selector normalization,
   synchronization and activity for a different receiver, higher-rank rigid
   maps, the unique-nonrigid receiver, and arbitrary-root coverage remain
   open.

   `GLS60` factors the three pure same-colour companion equations one level
   further.  For each pair, at least one whole old-probe shore lies on the
   corresponding coordinate line and the other shore is projectively anti-
   synchronized; zero individual edges are retained, but every label still
   has a nonzero pure probe edge.  One probe is shore-pure on at least two
   colour pairs.  At every fully supported probe contraction, the six-label
   tensor is the one-edge hafnian first variation with three nonzero target
   weights.  Its direct companion graph is decomposable on the mixed
   `2+2+2` word, and a vertex-gauge identification with the internal graph
   either makes the variation zero or produces an excluded honest six-vertex
   witness.  Thus both natural graph splices are closed.  The tranche also
   corrects a receiver-type error: a weighted permanent `P_6` restriction is
   not accepted by the six-vertex theorem and instead enters the separate
   open `PR/PR6/PRT` subtree.  A non-gauge graph reconstruction or a fully
   gated promoted attachment remains open, as do higher joint ranks and
   arbitrary-root coverage.

   `GLS58` gives the exact rank-profile continuation for the higher-rank
   all-six-rigid branch.  An arbitrary nonzero vector in a deficient joint
   kernel forces distinct pure neighbour shores for its supported colours;
   one such contraction leaves ten physical trilinear decks on seven open
   slots.  Two deficient contractions reconstruct an honest six-vertex graph
   with port blocks `hW_uv+a_u tensor b_v+b_u tensor a_v`, including `h=0`,
   but rigidity leaves at most two nonzero target colours.  An exact all-six-
   rigid binary control shows this endpoint is real and is not excluded by
   the accepted three-colour theorem.  With no deficient labels, a global
   cross-product polynomial identity splits the injective cell into a
   coordinate-axis-shore cover or a genuine cancellation branch; a physical
   off-target control has all six maps injective, all three pure coefficients,
   and the termwise identity while `61` mixed words survive.  Thus the
   remaining step is additional complete mixed/deck coupling, not another
   application of the finite theorem or a rank-minor division.

   `GLS59` gives the corresponding exact continuation on the `r=3`
   unique-nonrigid branch.  At zero anchor, contract every slot except one old
   probe after choosing edge-kernel vectors against the other old probe.  The
   complete matching tensor forces a nonzero coordinate-pure neighbour for
   every jointly supported colour.  Irreducibility promotes these pointwise
   shores to fixed whole-domain pure blocks, with descending linear-section
   flags retaining every exceptional root-vector fibre.  The two old probes
   therefore carry three-label pure stars among the five rigid labels; their
   overlap has joint rank one on a common colour or rank two on two distinct
   colours.  Contracting that boundary kernel together with the fully
   supported nonrigid kernel reconstructs an honest binary or monocolour
   six-vertex target.  The accepted finite theorem does not exclude either.
   The natural old-probe `GLD3` triangle is now closed as a receiver route:
   on every root-torus point it cannot be simultaneously target-diagonal.
   Coupling all overlaps with further complete mixed equations, or attaching
   a forced pure probe block to a complete-nuisance surviving promoted target,
   remains open.

   `GLS15` now identifies a support-free physical synchronization invariant in
   the original `r`-root, `r`-port fixed-`Q` chart.  For every pair target
   there, the two joint desired columns are `Psi_C(K^Q)` and `Psi_C(R)`.  A
   rank-one line absorbs exactly
   `Psi_C(delta R-eta K^Q)`, and cross-applying another target's absorbed
   direction leaves the projective determinant times the local quotient
   generator.  On the complete target this class is tied denominator-free to
   each active pure class.  What remains is not to rediscover slopes in a
   support atlas: it is to prove the cross-target transport class is nuisance,
   or contradict its nonzero pure-target identity, on every generic and
   exceptional fibre.  Joint rank zero, missing activity, the four-port line,
   and the absence of an arbitrary-order downstream package remain separate.
   This does not integrate the distinct GLS8 two-probe promoted target, whose
   target size is `2r-4` rather than two.

   On the narrower literal all-seven response-zero branch at root order four,
   `GLS9` localizes the full-rank chart.  Rank-three `H_Q` kills every
   direct port block; maximum-root maximality leaves one or two shores with
   coordinate residual factors (and at least one coordinate local factor in
   the two-port case); and the complete contracted target excludes the
   equal-colour case.  `GLS10` excludes the remaining opposite-colour
   pure-`Pi_Q` chart: the singleton dies in the `(i,i)` fibre, while the
   two-port branch uses the same two alpha-lines in the incompatible `(i,i)`
   and `(j,j)` colour covers.  It makes the entire literal-zero chart on
   `D(det H_Q)` empty.  The determinant divisor
   is reduced by `GLS11`: rank zero is absent; rank two is a
   two-active-port conformal core with fixed coordinate blockers; and rank one
   has an exhaustive double-contained/one-sided/two-sided trichotomy.  The
   six pair-response equations have a denominator-free 15-matching identity,
   but they do not imply the seventh four-port response zero.  `GLS12`
   excludes the whole rank-two core by six support-space quotients and
   excludes the rank-one singleton triangle by a common-incidence `P_4`
   column splice.  The reviewed
   [GLS13 two-port extraction](../claims/arbitrary-order/FOUR_ROOT_DETERMINANT_DIVISOR_RANK_ONE_TWO_PORT_P5_EXTRACTION_THEOREM.md)
   treats the two-port two-sided
   branch: the complete target forces a coordinate pairing, twelve
   common-tail identities admit a Latin bottom-row splice to a weighted
   `P_5 -> Delta_3` restriction, and the seventh response is termwise
   zero.  That is a downstream permanent interface, not an exclusion.  The
   [GLS14 contained/one-sided reduction](../claims/arbitrary-order/FOUR_ROOT_DETERMINANT_DIVISOR_RANK_ONE_CONTAINED_AND_ONE_SIDED_PERMANENT_REDUCTION_THEOREM.md)
   exhaustively routes the sibling rank-one branches.  Branch I reaches a
   nonzero decomposable `P_5` pullback or a same-coordinate balanced core;
   `Phi!=0` makes the seventh response visible without producing a selector,
   while `Phi=0` leaves the explicit augmented-`P_6` face defect `Psi`.
   Branch II and its transpose reach pure decomposable `P_4/P_5` compression
   interfaces.  None of those downstream interfaces is an exclusion, and the
   selector/face-defect obligations remain open.  This does not close
   the broader `R` branch,
   because `GLS7` enters `R` when even one of the seven responses is zero.
   The pair/four-port interference theorem now gives a second, smaller target
   bridge after one exact same-`Q` window is attached: three nonzero
   complementary colour products at one port force one of nine displayed
   mixed coefficients to be nonzero.  Its camouflage control proves that the
   full pair-plus-four mixed target equations alone do not close the
   zero/one/two-active residue.  GLD4 now shows that simply repeating the same
   observed package on arbitrarily many common-core windows also does not
   help: all overlaps can agree literally while every chart stays two-active.
   GLD5 makes the first attachment step finite, and GLD7 now imposes the full
   witness target on its quotient.  For each pair or four-port label, the
   active pure target classes have quotient rank at most one.  Rank at least
   two excludes target incidence, while rank one forces the desired class and
   legal attachment.  With a nonzero physical response, rank zero is exactly
   the bad quotient branch where every active pure class is swallowed by
   nuisance.  Thus the isolated-one-row obligation is to force rank one and
   response nonvanishing for at least one eligible row, or exclude simultaneous
   failure of them all.  This alone does not close Universal Supply and Target
   Attachment: supplying all seven synchronized rows is the stronger GLD3
   entry.  The same exact trichotomy reduces the six-port
   attachment package to thirty-one finite rank-one conditions, but does not
   force them.  On the attached branch, one must still force three activity
   products or produce a genuinely coefficient-pure cross-window syzygy;
   quotient rank one alone is not coefficient purity.

   GLD6 closes a separate, sharply typed part of the two-active residue.  If
   all fifteen `K4` responses on six ports are legally attached on the fully
   two-active nonvanishing `h=0` line locus, coefficientwise Wick selectors
   reconstruct every direct pair block.  Target-diagonal four-port rows and
   one nonzero pure row then force a displayed mixed depth-six coefficient,
   provided that six-port row is also attached.  The remaining obligation is
   therefore attachment of the full `z_2,z_4,z_6` package, proof that the
   witness lies in the named nonvanishing line branch (and has a nonzero pure
   row), or an exact treatment of the remaining tensor support branches.
   GLD8 now completely classifies the scalar common-row map: both residual
   factors need support at least five, a union of at least seven is always
   injective, a six-union is decided by the published discriminant, and a
   five-union has kernel dimension five.  In particular, twenty-one rows on
   seven ports can identify a pair even when every relevant principal
   six-window is singular.  The open step is no longer scalar
   all-minors-singular linear algebra; it is legal row attachment plus a
   coefficient-word support cover of the full tensor on the witness locus.
   Rational deck recovery and selected `D`/`T` package agreement do not
   satisfy these obligations.

   GLD9 removes one coordination ambiguity from the attachment edge.  If each
   required selector survives with nonzero response at a maximal
   nuisance-rank point, all seven or all thirty-one identities can be placed
   at one fully supported contraction.  The exact disjoint rank-drop control
   shows why arbitrary individual survival points cannot simply be
   intersected.  The remaining obligation is therefore individual
   maximal-rank survival, not common-contraction topology.  GLD11 makes that
   obligation genuinely witness-theoretic: maximum-root incidence, triple
   blockers, local concision, pure normalization, the Hamming-one shell, and
   all seven nonzero responses coexist with simultaneous swallowed-pure rank
   zero in one physical graph.  Its displayed mixed coefficient excludes it
   from the target, so only the full mixed equation or another exact target
   detector can close the residue.

   GLD10 supplies the first complete seven-port tensor word cover on an exact
   structural branch.  Five bi-supported helpers recover every one of the
   `189` direct-pair coefficients from the same thirty-five `K4` tensors, and
   one rank-two diagonal pair plus no isolated response port is an observable
   sufficient entry condition.  Legal constant same-`Q` attachment of those
   thirty-five tensors and witness forcing of the helper branch remain open.
   GLD12 closes the deeper-response question for genuine full-tensor kernels:
   at fixed `K` and `h=0`, the full residual-present `Z` tower has exactly the
   affine fibre `B+ker(mu_K:A_2->A_4)`.  Thus a complete tensor `z_4` kernel
   cannot be repaired by any deeper same-`Q` `Z` row.  This does not contradict
   GLD6's depth-six mixed target-shape detector, and scalar-word kernels may
   disappear under tensor polarization.  The surviving routes are legal row
   attachment plus tensor cover, paired `M,Z` information, or direct use of
   the full mixed GHZ equations.

   GLD13 now makes the contraction part of the swallowed-pure residue
   exhaustive at generic rank.  If every desired column survives over the
   contraction function field, one common principal open supplies all seven
   rank-one quotient classes.  Otherwise one named target absorbs the desired
   and all three pure columns over that function field, with four
   denominator-cleared polynomial nuisance identities.  This does not exclude
   the absorbed branch, and exceptional rank-drop escape may coexist with it.
   The next witness-theoretic step is to contradict that exact absorbed branch
   using the full mixed equations or a bounded coefficient-pure detector.

   GLD14 closes the response-shape part once paired rows are legally attached.
   Fixed `M_2` rows cut the full `Z` fibre by an optimal affine incidence
   theorem, while pair diagonality and the two-colour `M_4` rows already decide
   mixed `M` purity at every depth.  The complete-bipartite one-colour control
   leaves a four-dimensional pure residue after all mixed rows, so a universal
   mixed-only detector is impossible on the ambient paired-response locus.
   Legal same-graph attachment, witness integration, activity, and the
   weighted-permanent bridge remain open.

   GLD15 now makes that legal paired-row interface exact at the module level.
   The two desired deck labels have a joint quotient rank zero, one, or two,
   and this rank is exactly the dimension of the constant operator combinations
   `aM_S+bZ_S`.  Pure target quotient rank two forces separate `M_S,Z_S`
   attachment and independent responses; rank one can still be an `M`-active
   combination that cuts an already fixed `Z` fibre.  Exact pair-block covers
   reduce full-tensor complete-bipartite `K_(3,3)` and `K_(5,2)` fibres to four
   and six pair supports.  A local mixed `M_4` row needs only one four-port and
   two nuisance-killing pair targets once complementary-colour activity is
   known.  The unresolved step is to force those joint ranks and activity on
   the actual witness locus, or exclude the rank-one/zero branches with the
   full mixed equations; no permanent bridge is supplied.

   GLD16 weakens the sufficient module input from seven rank-two quotients to
   one common projective operator line across the six pair targets and the
   four-port target.  For arbitrary residual scalar `h`, the selected package
   obeys the denominator-free shifted identity
   `aT'=C(D)-C(eta K)`, where `a=delta+h eta`.  Three-colour activity excludes
   both the effective-scalar divisor `a=0` and the `a!=0` nine-word branch.
   The exact residual is now to force that common line and activity, or use
   the full mixed equations to exclude a zero coefficient space or incompatible
   rank-one slopes.  Unequal-slope three-active and common-line two-active
   controls show that neither obligation can be silently dropped.

   GLD17 closes two special different-slope branches.  When the common pair
   slope `p` and four-port slope `t` satisfy `p=0` or `p=2t`, with `p!=t`, one
   complementary pair carrying all six pure selected values forces one of
   eighteen fixed mixed four-port rows.  The unresolved task is to force that
   slope/support pattern or classify the remaining unequal-slope and sparse
   branches.  Exact controls show three-colour activity alone does not supply
   the six local values and arbitrary unequal slopes remain possible.

   GLD18 makes that remaining slope locus exact.  Complete-nuisance operator
   lines lie in the kernels of `114` mixed-response rows on a witness;
   visible rank-one lines are determined by exact `2 x 2` minors, while
   invisible lines remain a separate module obstruction.  Six independent
   pair slopes produce three complementary quadratic corrections.  If all
   three vanish, one three-full complement forces an eighteen-word mixed
   detector; otherwise the noncancellation residue is explicit.  On the
   cancellation locus, a nonzero four-port `Z` coefficient forces all three
   support products to vanish on any surviving witness, whereas the pure-`M`
   four-port axis forces one pure-`M` pair on every complement.  The next step
   is to force one of these legal incidence patterns or exclude its zero,
   pure-`Z`, invisible, noncancellation, and sparse-support branches using the
   full mixed witness equations.

   GLD64 closes the strongest globally decomposable part of GLD18's
   noncancellation residue.  Once `K_uv=a_u tensor a_v` and one complementary
   selected pair is three-full, all six finite pair slopes may be unrelated:
   thirty-six `2+1+1` rows force the common edge relations, six named `2+2`
   rows remove every support drop, and one `3+1` row kills the aggregate
   correction.  A final `2+2` coefficient is nonzero.  This removes both
   synchronization and cancellation equations inside that physical class,
   but it does not force legal `M`-active rows, decomposability,
   three-fullness, or any arbitrary-root source interface.

   GLD67 corrects the product-selector interface formerly used by GLD65 and
   GLD66.  The complete legal row annihilates root companions `G_D`, which by
   definition contain no direct edges among the outside vertices.  The full
   matching coefficient on `R union Q union {u,v}` is a different object and
   retains the exact term `B_uv G_Q`; it is therefore `B_uv G_Q`, not zero,
   when the other companions vanish.  The old cross-Gram identity silently
   crossed this type boundary.

   An exact ternary maximum-root graph makes the failure concrete.  Product
   evaluation at one open root gives the complete legal pure-`M` companion
   row: across `431` evaluated companion entries, `G_Q=1` and every nuisance
   entry vanishes.  All six port blocks are diagonal, and the four-port
   response is the sum of all three pure colour words.  Thus the GLD65
   three-colour exclusion and the dependent GLD66
   two-colour and synchronized-plane conclusions are withdrawn.  Their
   standalone matching/support and response-anchor linear algebra remains
   available only at its explicitly conditional scope.  The corrected parent
   obligation is to supply a genuine full-target equation, a second legal
   response axis, or another coefficient-pure bridge; more labels from the
   same complete companion row cannot suffice.

   GLD68 then removes the immediate all-six base-shadow source branch rather
   than trying to repair that transfer.  For complementary port pairs
   `S,T`, the order-two label `I=T` is part of the complete target-`S` base
   nuisance.  Its evaluated term is `H_T tensor Pi_T`; if `Pi_T` is nonzero,
   its coefficient slices fill the entire receiver and swallow `b_S`, while
   `Pi_T=0` already kills `b_T`.  Thus at most three of the six pair base
   shadows survive, with maximal star/triangle patterns.  The old
   `GLS17 -> GLD16` all-six source premise is empty; the live universal work
   moves to the complementary swallowed circuits or to non-leading pair-row
   supply.

   GLD69 makes that promised parent attempt without splitting into another
   star theorem and triangle theorem.  The three targetwise relations embed
   in one labelled direct-sum module, but all eight maximal profiles have
   exact three-colour formal models whose desired classes survive the complete
   foreign port-pair nuisances and whose aggregate is `Delta_4`.  The missing
   information is genuinely physical: all six companions are pullbacks of
   one zero-diagonal residual permanent form `J=P_4(xi,eta,-,-)`.  On the
   four-rank-three locus, a maximal profile forces `rank J=2`.  Stars put its
   radical plane in every port image; triangles put the three sibling images
   on one maximal-isotropic hyperplane but allow the centre to meet the
   radical in only a full-support line.  The internal port-pair image is an
   exact rank-`21` Segre-tangent space for stars and a rank-`19` fixed-factor
   space for triangles; weighted concise GHZ is outside both.  The complete
   base equation still contains eight residual--port labels and `Q`.  A
   support-at-most-two radical vector common to all ports pulls back to one
   decomposable functional annihilating all fifteen contracted order-two
   labels.  A nonzero weighted-GHZ value is therefore a bounded contradiction.
   Stars automatically have the common sparse line but may have zero detector
   value; triangles need not have the line at the centre.  Exact controls
   realize both boundaries.  The live parent obligation is now to remove or
   synchronize the nine `Q`-meeting labels, or close the
   scalar-zero/nonsparse-centre incidence locus, plus lower port ranks and
   non-leading supply--not a third targetwise sibling.

   GLD70 keeps all nine missing labels instead of quotienting them away.  The
   full contracted nuisance is one `79`-column map, and the cubic epsilon
   relative invariant identifies the honest concise GHZ orbit as the
   epsilon-nonzero open inside the complex third Segre secant.  The desired
   contradiction is therefore one exact restricted secant saturation using
   both flattening and Strassen equations.  On the fully supported residual
   locus, rank two forces the unique ratio pattern `(1,1,1,-1)`; every
   nonisotropic maximal-star quotient slope gives the same fixed rank-`44`
   nuisance space.  Its quotient beyond the pair layer has dimension `23`.
   The projection-full triangle instead has rank `35` and quotient dimension
   `16`, with `Q` contributing the corrected extra direction.  Epsilon alone
   cannot close the problem: the `Q` generator has nonzero epsilon but all
   three balanced flattening ranks equal five.  `GLD70` left a
   radical-membership certificate for the fixed star space as its next target;
   `GLD71` reformulated it and `GLD72` subsequently refuted it.  Compatible
   residual-coordinate-boundary and triangle atlases remain unsupplied.

   GLD71 makes the fixed-star obligation substantially smaller and more
   structured.  The rank-`21` pair layer is exactly the coordinate erasure in
   which at least two leaf indices are `2`.  Puncturing leaves a rank-`23`
   nuisance code in dimension `60`, hence `37` exact parity checks.  Every
   non-erased decomposable leaf word has syndrome rank three in characteristic
   zero: a symmetry-reduced `36`-chart SymPy atlas and a separate `108`-chart
   Singular replay both close the projective cover.  Root slices have parity
   dimensions `4,4,6`, and the three binary balanced determinants factor into
   pairwise products of differences of the Eisenstein norms
   `alpha^2-alpha beta+beta^2`, forcing at least three of four norms to agree
   on any third-secant survivor.  Pairwise syndrome independence is false:
   an exact nonhidden second-secant point has a rank-`5` two-word block, but
   its centre is singular and epsilon is zero.  At publication, the proposed
   universal target was determinant safety of the full `37 x 9` three-word
   syndrome kernel.  Six slice rows or a tested ten-row compression are not
   equivalent to the full syndrome; the latter produced and then rejected an
   apparent invertible-centre point.  `GLD72` later finds a different point
   that survives the actual full syndrome and direct original-space replay.

   GLD72 gives exact Gaussian-rational leaf and centre frames with determinants
   `-1-i` and `12`.  Their three-word tensor lies in the original rank-`44`
   fixed space, the full syndrome has rank `7`, all local and balanced ranks
   equal three, and `epsilon=144-144i`.  Thus the fixed-star GHZ exclusion,
   balanced-minor shortcut, and determinant-safe saturation are refuted.  The
   tensor has `61` nonzero coordinates in the fixed basis and is not supplied
   with legal shared graph/source data.  The live universal target is now a
   nonlinear source-integrability theorem for the GHZ-survivor locus, starting
   with this exact hostile control.  The global conjecture remains unresolved.

   GLD73 begins that nonlinear comparison without overstating the result.  An
   equivariant open-port basis change sends the Gaussian survivor to the
   literal `Delta_4`, and one pinned raw preimage gives exact effective data on
   a ten-vertex edge array.  All `945` perfect matchings reproduce the
   contracted target.  Nevertheless, at each of the six contracted vertices
   the complete `17`-parameter first-response map has ranks `(17,16)` before
   and after projection to the `78` mixed coordinates.  Its diagonal
   intersection is therefore only `C Delta_4`, whereas a ten-mode GHZ identity
   would require the full three-dimensional diagonal derivative.  This
   excludes every unused-row completion over that pinned effective array, but
   not by itself the other points of the affine `35`-dimensional raw fibre.
   `GLD74` is the serious parent-theorem successor rather than another pinned
   calculation.

   GLD74 parametrizes that entire raw fibre and closes it at one contracted
   vertex.  At `q_0`, the `Q` cofactor and twelve eta-residual cofactors have
   full and mixed rank `13`.  Modding out their mixed image leaves four affine
   root-cofactor columns in dimension `65`, with
   `Z_0+Z_1+Z_2-Z_3=0`.  Any three-dimensional diagonal response would force
   `[Z_0 Z_1 Z_2]` to have rank at most one.  Two exact sparse
   Nullstellensatz identities and one inconsistent affine coordinate system
   exclude the exhaustive projective cover, including all response-rank
   drops.  Thus every raw preimage of the exact GLD72 tensor fails the
   complete `q_0` first response in this fixed effective model.

   GLD75 performs the required first parent-level survivor-locus test.  The
   identity component of the local-basis stabilizer of the complete fixed
   rank-`44` space is only the four factor-scalar torus, and its orbit tangent
   at GLD72 is one-dimensional.  The survivor tangent is instead
   five-dimensional.  An exact bidirectional ideal certificate goes beyond
   tangent comparison: on a frame gauge containing GLD72, it proves that the
   full survivor germ is smooth of dimension five and equals its equal-leaf
   subgerm.  Thus four genuine survivor parameters remain after tensor
   scaling, so symmetry transport cannot globalize GLD74.  The live local
   parent target is the denominator-free response incidence over those four
   parameters, with the full `35`-dimensional raw kernel and every rank-drop
   fibre retained.  Exceptional divisors, other survivor components, source
   presentations, maximum-root certification, fifth-root exclusion, non-star
   coverage, and global resolution remain separate.

   GLD76 constructs that denominator-free parent incidence.  Quotienting the
   thirteen fixed full-tensor response directions gives a `68 x 4` root
   module, and the original `17 x 3` lifting problem is exactly equivalent to
   one `4 x 3` lift with `204` equations.  All rank drops remain.  Actual
   leaf-permutation covariance splits the raw kernel into `8` trivial, `3`
   sign, and `24` standard dimensions.  Compactifying the GLD74 necessary
   mixed rank-one condition then exposes two sparse sign-type directions at
   infinity, with root-column ratios `(1,-1,1)` and `(1,1,-1)`.  They are not
   affine lifts, but they invalidate the simplest properness argument for a
   survivor-open exclusion.  The live local obligation is now the strict
   transform along these named boundary branches plus an exact cover of any
   remaining projective boundary; only after that can a parametric
   certificate or exceptional polynomial be claimed.

   GLD77 makes the sign part of that boundary cover exhaustive.  The complete
   three-dimensional sign block compresses to a `3 x 3` linear matrix whose
   two-minor ideal is `((u+v)(u-iv),uw,vw)`.  Its projective scheme is reduced
   and consists of exactly three points: the two GLD76 witnesses and one new
   direction with ratios `(1,-1,-1)`.  Thus the sign-plane strict transform
   has a finite three-chart obligation.  Boundary directions with trivial or
   standard raw components remain unclassified, and no projective direction
   is a finite raw lift.

   GLD78 closes all three pure-sign affine entrances without mistaking a jet
   calculation for an all-order theorem.  Its repaired formulation first
   transports the complete moving interface to literal-Delta coordinates;
   a fixed untransformed `65 x 3` quotient would not be legally necessary.
   Its corrected dual-number systems retain all `35` raw corrections, four
   scale-fixed survivor directions, and both slope derivatives, giving exact
   ranks `34`, `36`, and `37` before and after affine augmentation at every
   sign point.  The load-bearing argument is stronger: average the actual
   moving `79`-coordinate raw vector under the interface-preserving leaf
   `S_3`, reduce to the eight invariant kernel
   directions, and use one explicit augmented `9 x 9` determinant per slope
   chart.  The quotient pivot is `8(1+i)/27`, the invariant-basis pivot is
   `1008i`, and all three obstruction determinants are nonzero at GLD72.
   Their regular continuations `delta_j(F,a,b)` therefore exclude affine
   branches and formal arcs of every order on named principal opens in the
   survivor-frame times slope-chart space.  The smallest remaining local
   parent computation is now an exact isotypic/determinantal cover of the
   boundary outside the pure sign plane.  A survivor-only exceptional
   polynomial, other components, and source-interface globalization remain
   open.

   GLD79 supplies that exhaustive Gaussian boundary cover.  The actual leaf
   `S_3` action decomposes the raw kernel as `8+3+24`, and equivariance makes
   the two proportionality equations a direct sum on those isotypes.
   Nonzero block minors make `K_0` injective, so every projective point lies
   in the first-column slope chart.  A finite two-stage certificate makes the
   trivial block empty; Schur compression to a twelve-dimensional
   multiplicity space and another exact determinant cover make the standard
   block empty.  Mixed components cannot cancel across output isotypes.
   Hence the complete fixed-Gaussian boundary is precisely the three reduced
   sign points of GLD77.  This closes the missing fibre classification and
   reopens the proper-image route to a genuine survivor-open exclusion, but
   that geometric bridge and any explicit survivor-only exceptional
   polynomial remain separate successor obligations.

   GLD80 completes the geometric bridge.  Over an actual affine finite-type
   scale-fixed survivor neighborhood, it transports the complete interface
   to moving literal-Delta coordinates, where a matching partition restores
   the necessary three-column rank-one system without contradicting the full
   fixed-coordinate `GLD76` `68 x 4` incidence.  It removes nonproper slope
   variables and uses the intrinsic rank-one minors in `B x P^35`.  The strict
   finite-raw closure is the `s`-saturation and is proper over `B`.  If it met
   the Gaussian fibre, `GLD74` would put the point at infinity and `GLD79`
   would make it one of the three sign points.  An algebraic DVR-selection
   lemma supplies a trait with affine generic point; a nonzero full
   `mathcal Z_0` coordinate recovers regular slopes, and the corresponding
   repaired moving `GLD78` determinant is a unit and forces `s=0`, a
   contradiction.  The proper
   image is therefore closed and misses `F_0`, so some principal open
   containing `F_0` excludes every raw preimage's first response.  This is
   existential: the base polynomial is not expanded.

   GLD81 supplies the forward source/interface bridge on the named physical
   branch.  For an actual root-order-four, surplus-two maximum-root source,
   every nonzero contracted ten-mode matching has exactly one outside raw
   edge, giving the physical `79`-coefficient vector.  Partitioning the same
   matching set by the neighbor of `q_0` gives the complete `13+4=17`-
   coordinate legal response factorization.  Multilinearity of a full GHZ
   target then supplies an actual `17 x 3` lift, and the complete GLD80 intertwiners carry
   it to the moving literal-Delta incidence.  Therefore the fully supported,
   rank-three, nonisotropic maximal-star source branch is excluded whenever
   its induced survivor frame lies in `D(delta)`.

   GLD82 makes a survivor-open exclusion explicit and fraction-free.  The
   fixed rank-`44` nuisance solve and fixed rank-eight invariant kernel remove
   two apparent moving divisors.  A universal polynomial-port audit proves
   individual-root leaf covariance, so averaging is exact for the affine base
   image of the necessary rank-one incidence.  Adjugate tensor transport and
   a named thirteen-row quotient pivot then produce polynomial homogeneous
   response columns on `P^8`.  Forty-five named intrinsic minors form a
   `45 x 45` quadratic coefficient matrix whose moving circuit specializes
   entry-for-entry to the exact Gaussian matrix with nonzero determinant.
   Thus `Delta_82=Omega gamma_num det(M_ff)` defines a principal open
   containing `F_0`; every raw first response there is excluded, and GLD81
   transfers the same open to the named physical source branch.

   GLD83 removes the selected quotient pivot from that conclusion.  Before
   quotienting, append each pair of transported response columns to the full
   thirteen-column constant block and take its `15 x 15` bordered Pluecker
   coordinates on the globally defined equal-leaf subincidence, without
   inverting the old pivot.  The selected coefficient matrix satisfies
   `M_ff=gamma_num M_Pl`, hence
   `Delta_82=gamma_num^46 Delta_83` with
   `Delta_83=Omega det(M_Pl)`.  Nonvanishing of the bordered determinant
   itself forces the constant block to rank thirteen, so no `gamma_num`
   branch is divided away.  All exterior coordinates together give the
   intrinsic coefficient map `A_Pl`; its maximal-minor Fitting open is an
   exact finite excluded union.  The smallest fixed-chart obligation is now
   the genuine rank-drop locus `V(I_Pl)`, not the old quotient pivot or one
   selected Macaulay determinant.  Covering that locus, other survivor
   components/gauges, and the triangle, rank-drop, residual-boundary,
   isotropic, smaller-survivor, and other-root branches remains open.

   GLD84 gives that intrinsic residual an exact finite parameter cover.  On
   the complete scale-fixed equal-leaf base the ten survivor equations are
   globally affine-linear in eight center shifts, `g=A(z)c+q(z)`, with six
   leaf variables.  The `10 x 8` coefficient matrix yields `45` rank-eight
   Schur charts with two residual equations, `960` exact rank-seven charts
   with three leaf-compatibility equations and one free center-kernel
   coordinate, and the named closed rank-at-most-six branch `V(I_7(A))`.
   `GLD72` is rank seven with a pivot minor `12`, but a named eight-minor has
   derivative `48i` along the smooth survivor tangent `tau_14`; rank-eight
   points therefore occur on the same local component.  This prevents the
   Gaussian rank-seven chart from masquerading as a component theorem and
   reduces the next response computation to six-variable chart rings.  The
   pulled-back Fitting ideals themselves are not yet computed or excluded.

   GLD85 now supplies the first exact rank-eight point-level specialization.
   On the named rows `R_8=(0,1,2,3,4,5,6,7)`, the point
   `z=(1,0,0,0,-2/3,0)` with its pinned eight center shifts satisfies both
   Schur residuals, has nonzero `mu_R`, and lies in `D(Omega)`.  The full
   intrinsic quotient map has shape `45 x 6240`; one pinned maximal minor has
   nonzero residues modulo `1000000007` and `10000019`, with every exact
   Gaussian-rational denominator slot checked as a unit at both primes.
   Therefore the pullback of `I_Pl` is nonzero and its vanishing locus is a
   proper closed subset of this rank-eight chart.  The old selected `M_Pl`
   is exactly zero at the same point, so this is a full-intrinsic
   proper-open result rather than a selected-minor computation.  The point
   does not empty or exclude the intrinsic residual; all other charts,
   ranks, components, source branches, and global resolution remain open.

   GLD86 closes the next high-value rank boundary without overclaiming a
   Fitting result.  On the same scale-fixed equal-leaf base, the exact GLD75
   bidirectional certificate gives `B=0 iff M(G)C=0` for the fixed `37 x 9`
   GLD71 syndrome map.  Since `C_8=1`, the selected rows
   `(0,1,17,19,31,32,33)` and columns `(2,3,4,5,6,7,8)` have determinant
   `432(p-q)^2(p-s)^2(q-s)^2(pq+ps+qs-p-q-s)^2`, with `s=1+i+r`.  Off the
   four named divisors, column replacement forces the first eight syndrome
   columns to have rank at least seven; differentiating the certificate on
   `B` transfers that rank to `A`.  Thus the rank-at-most-six branch is
   contained in the union of those four divisors, and the same containment
   holds after `D(Omega)`.  GLD87 now closes the three linear collision
   divisors on the determinant-safe retained open: on `H_1=p-q`, the exact
   eleven-row block calculation leaves only `p=1-s`, `s^2-s+1=0`, where the
   complete center kernel has proportional rows and hence `det(C)=0`.
   Exact leaf-column equivariance transfers this to `H_2=p-s` and `H_3=q-s`.
   Since `D(Omega)` includes the `det(C)det(G)` gate in the normalized
   GLD83 frame, the retained low-rank branch is now confined to `H_4`.
   GLD88 now removes a nonempty exact principal open inside `H_4`.  On the
   named six-pivot chart, two bordered syndrome residuals are linear in the
   remaining leaf shifts; their explicit coefficient determinant forces the
   displayed rational three-parameter family.  All three root blocks then
   have one common kernel line, the full syndrome rank is six, and every
   compatible center has proportional rows.  Hence that principal open is
   disjoint from `D(Omega)`.  The parameter, coefficient and pivot
   boundaries, the pulled-back Fitting ideal, and all other
   chart/component/source obligations remain open.

   GLD89 now removes the full `P=p^2-p+1` divisor inside `H_4 intersect
   D(Omega)`, including both the named six-pivot open and its exact
   six-pivot boundary.  The two reduced six-minors, the bordered residuals,
   and the exceptional `q=0,1,-1` seven-minor table force a complete common
   kernel line in every remaining P branch, hence a singular center.  The
   `d0=p+q-1=0` overlap is checked in a separate chart: `H_4+d0=0` gives
   `q=1-p` and `P=0`, and four exact syndrome rows either force two
   proportional center rows or land in GLD87 H2/H3.  Thus P and d0 are
   excluded on the determinant-safe open.

   GLD90 now closes the entire complementary H4 low-rank stratum on
   `D((p-q)d0 P L1 L2 e Q6)`.  The old and alternate six-pivots share the
   explicit factor `Q6`.  On their double-pivot locus, two auxiliary charts
   force one exact residual curve; modulo that curve the leaf family is the
   GLD88 common-row-kernel family.  Four simultaneous auxiliary-pivot
   corners are excluded by coprime seven-minors.  The formerly exceptional
   `T=2pq-p-q+2=0` divisor is handled without dividing by `T`: its two pivot
   brackets differ by `4P`, so one pivot is nonzero on the declared open.
   The remaining H4 boundaries are `Q6=0` and `L1/L2/e=0`; the pulled-back
   Fitting ideal and all other chart/component/source obligations remain
   open.

   GLD93 now closes both named coefficient divisors `L1=0` and `L2=0` on
   the upstream-open H4 equal-leaf chart.  Direct specialization gives
   `q=p(2-p)/(2p-1), s=p` on L1 and
   `p=q(2-q)/(2q-1), s=q` on L2; in each chart the upstream open makes
   `Q6` automatically nonzero.  The two raw six-pivots and their bordered
   seven-minors either give an immediate rank-seven witness or force an
   exact double-pivot slice with one auxiliary rank-seven witness.  The
   exceptional `e=T=0` L1 fibres and `T=0` L2 fibres are checked separately
   by coprime seven-minor pairs.  The L2 computation is direct and does not
   assume that a naive p/q leaf-column permutation preserves the fixed
   carrier.  The remaining H4 low-rank boundaries are `Q6=0` and `e=0`
   away from the handled intersections; the pulled-back Fitting ideal and
   all other chart/component/source obligations remain open.
   GLD92 now gives an exact dense continuation on the Q6 boundary, but only
   inside the GLD88 three-parameter family.  Two fixed-column six-minors have
   numerators `(p-q)^3F28` and `(p+q-1)(p-q)^3F31` over `P^2e^2`.
   Irreducibility of `Q6`, nonzero Q6-division remainders, and an exact
   resultant coprimality check show that their union of principal opens is
   dense.  A coefficient-ideal Groebner certificate rules out vertical
   common-minor fibres on `D(Delta)`, so
   `V(Q6,F28,F31)` is a finite retained residual.  GLD92 does not force
   arbitrary H4 Q6 points into GLD88, does not enumerate that finite locus,
   and leaves `L1/L2/e`, Fitting, and the other chart/component/source
   obligations open.

   GLD91 makes the next finite slice exact without promoting it to a
   full-chart statement.  On the same `R_8` chart, impose
   `x9=1, x10=x11=x12=0, x13=t, x14=u`.  After correcting an earlier
   exploratory frame calculation that omitted the Gaussian offsets in the
   centre base, exact `Q(i)` elimination gives a degree-eleven resultant:
   six linear fibres and a squarefree degree-five `Q5` component.  The five
   `Q5` points and two linear fibres have `mu_R=0`; three further linear
   fibres have nonzero `mu_R` but zero centre-frame determinant.  The only
   residual fibre in `D(mu_R*Omega)` is `(t,u)=(-2/3,0)`, the GLD85 point.
   Its denominator-checked full-intrinsic rank-45 certificate therefore
   excludes `V(I_Pl)` on this two-leaf slice.  Full six-leaf rank-eight
   unitness/residual coverage, the other charts and ranks, other components
   and source branches, and global resolution remain open.

   GLD19 resolves the strongest response-map-zero residue at the support
   level.  If every realized mixed-response map vanishes, then all raw pair
   blocks are diagonal and the two four-port layers give an exact twelve-row
   complementary support classification.  Five scalar rows per complement
   already prohibit two three-full selected blocks, independently of hidden
   slopes or projective axes; a three-full edge even annihilates its opposite
   raw response.  The remaining task is not another slope calculation: it is
   to force or exclude the map-zero stratum and then eliminate its
   intersecting sparse-support locus using the full witness equations.  This
   does not supply a legal operator row or a permanent bridge.

   GLD20 now makes the common-shore global topology of that residue exact.
   The corrected channel uses at most two colours: one colour gives every
   nonempty four-vertex graph except `P_4`, while two colours give two clique
   supports.  Combining this atlas with the three complementary GLD19 ledgers
   leaves `467715` labelled raw support patterns.  A full-capable edge
   annihilates its opposite raw response, and the complete witness quotient then forces that
   opposite pair target to pure quotient rank zero.  Maximal stars and
   triangles therefore reduce to three simultaneous pure-absorption targets.
   The largest `F=empty` cell, those absorption targets, legal operator supply,
   and every permanent consequence remain open.

   GLD21 attacks an exact `1347`-mask part of that `F=empty` cell with the
   complete mixed equation.  When one of the two corrected clique colours is
   supported on all six edges, the third colour is dead on every contracted
   shore and no direct block can use it.  The all-dead-colour coefficient then
   leaves only `hG_U`: it excludes the entire `h=0` divisor and forces one
   nonzero pure root-to-four-port permanent slice at `h!=0`.  In the dense
   two-clique cell, twelve paired mixed coefficient packages additionally
   force desired companion columns into nine-column nuisance images.  The
   surviving task is genuinely same-graph root-companion integrability;
   arbitrary companion arrays solve the linear equation by `G_U=J_Q/h`.
   GLD22 makes the first exact cut on that integrability problem.  On the
   common private colour-diagonal cross chart, the opposite repeated-colour
   package kills the active root--root diagonal while Hamming-one equations
   make three singleton terms equal to `-h` times the same private word.  The
   resulting `-2h` mixed detector excludes the whole chart.  GLD23 now closes
   its full colour-dependent private-permutation boundary: dense-shore gauge
   normalization reduces to `576` active permutation pairs, and exact
   characteristic-zero certificates exclude all `28` symmetry orbits even
   with every root-side coefficient free.  GLD24 makes the first nonprivate
   cut: the balanced two-matching switch `I+E_(0,1)+tE_(1,0)` is excluded by
   an eighteen-row `-4t(t+1)` detector and a separate exact `t=-1` core.
   GLD25 closes the full two-independent-amplitude switch
   `I+uE_(0,1)+vE_(1,0)`: a bivariate generic detector, three divisor cores,
   and point/quadratic residual certificates exhaust every `u,v!=0`.
   GLD26 adds a directed `wE_(0,2)` support edge and excludes the complement
   of four explicit divisors by one exact sixteen-row detector.  GLD27 closes
   `uv=-1` pointwise through a divisor detector, a line with two point cores,
   and a quadratic-quotient certificate.  GLD28 closes `uv=1` through four
   curve detectors, four point cores, and one shared quadratic certificate.
   GLD29 closes `uv-u-v-1=0` through five curve reductions and a quadratic-
   cylinder certificate.  GLD30 closes `uv+vw+w+1=0`, the final divisor,
   through a sixteen-row detector and three curve certificates feeding the
   prior divisor theorems.  Thus the full directed-spur coordinate family is
   empty.  GLD31 adds the reverse support edge and excludes a generic open
   subset of the resulting four-parameter chart, leaving five explicit
   divisors.  GLD32 refines `uv=-1` to four residual surfaces; GLD33--GLD36
   close all four pointwise and therefore complete that divisor.  GLD37 and
   GLD38 pointwise close `uv+wz-1=0` and `uv+wz+1=0`.  GLD39 then removes
   every divisor restriction from a two-row certificate first seen in GLD34
   and proves the entire nonzero GLD31 chart empty.  GLD40 adds three exact
   detectors plus the GLD23 origin to close every support-drop face and the
   full affine four-parameter coordinate family.  GLD41 then places all
   twelve off-diagonal amplitudes in one active colour slice simultaneously;
   twelve uniform two-row detectors plus the GLD23 origin exhaust all `4096`
   support masks.  GLD42 crosses into two simultaneously nonprivate slices on
   the reciprocal-spike chart: one exact divisor, a thirteen-row generic
   certificate, and an eleven-row exceptional-point core close the full
   affine plane.  GLD43 then restores all twenty-four two-slice amplitudes and
   proves twelve reciprocal divisor equations, forcing transpose-matched
   support and at least two active pairs.  GLD44 exhausts the `66` minimal
   two-pair masks into five orbits and excludes the generic part of each by a
   sparse function-field certificate.  GLD45 closes the same-tail exceptional
   divisor without a residual point, proving that full `12`-mask orbit empty.
   GLD46 closes the disjoint orbit by one eleven-row curve certificate and an
   exact support-pair exchange.  GLD47 closes all three reverse exceptional
   components with two curve certificates and pair exchange.  GLD48 closes
   the same-head residue by intersecting the pair-ordered generic divisors and
   excluding the resulting curve and point.  GLD49 closes both directed-chain
   exceptional curves, completing all `66` minimal two-pair masks.  GLD50
   then exhausts the `220` three-pair masks into `13` orbits and excludes each
   generic complement.  GLD51 pointwise closes the `24`-mask directed-path
   orbit, GLD52 closes the `4`-mask out-star orbit, GLD53 closes the
   `24`-mask fork-path orbit, and GLD54 closes the `12`-mask reverse-disjoint
   orbit.  GLD55 then transfers the `4`-mask in-star orbit to GLD52 by exact
   active-colour exchange, and GLD56 transfers the `24`-mask reverse-fork
   orbit to GLD53.  GLD57 then closes the `12`-mask in-fork orbit by an exact
   seven-stratum divisor cover, and GLD58 transfers the `12`-mask out-fork
   orbit to GLD57.  GLD59 closes the `24`-mask O6 orbit through four surfaces
   and two residual curves.  GLD60 closes the `24`-mask O3 orbit through four
   surfaces, five residual curves, and two points.  GLD61 closes the `24`-mask
   O2 orbit by complementary exact denominator covers and transfers it by
   active-colour exchange to the `24`-mask O7 orbit.  GLD62 closes the final
   `8`-mask O9 orbit, completing all `220` exactly-three-pair masks.  The
   smallest continuation is a four-pair support orbit or a uniform
   support-size argument; four-or-more-pair supports and a
   coordinate-free nonprivate argument remain broader alternatives.
   Other `F=empty` and pure-absorption cells and every permanent consequence
   remain open.

   At surplus at least four, the residual edge and pair moments remain absent
   from every linear root word, so a continuation must use nonlinear target
   coupling, a cross-window theorem, or the independent balanced complete-deck
   sensor.  Same-graph dual-Wick and holonomy defects still vanish identically.

2. **Balanced full-sensor gate failure.** Starting from the exact Cramer
   target residuals, prove that every target-consistent full sensor violates
   empty normalization, one retained affine-projective target-column-span
   condition, or one higher Euler--hafnian recurrence.  Euler syzygies reduce
   the ternary pair layer to `2m+2` selected-column replacement determinants.
   At `m=3`, exact full-row controls show that all target rows, empty
   normalization, rank, column degrees, and seven retained conditions still
   do not make the eighth condition redundant at the degree-compatible Cramer
   level.  The common-shore image is now written exactly by the singleton
   shared-factor equations and empty six-term permanent, and a Latin-plane
   separator proves that the ambient format is strictly larger.  Every one of
   the eight controls pulls back to the same exact binary
   image/kernel/permanent residual, and the transverse-factor obstruction now
   proves that residual empty.  Thus all eight known ambient coordinatewise
   controls lie outside the physical common-shore image.  They are not an
   exhaustive parametrization of realized pair-gate failure, so the remaining
   bridge is to force a retained determinant nonzero on every arbitrary
   realized balanced target incidence, or derive a smaller exhaustive
   physical alternative.  The lower-rank transverse analysis supplies a
   second, genuinely physical sharp boundary: at joint ranks three and four,
   exact one-cell common-shore controls satisfy full sensor rank and every
   local target equation.  S2BP's exhaustive tangent/common-zero atlas now
   proves that every such rational pair lift has a divisor pole; S2BN and
   S2BO close the two uninvolved-row-rank-two cells.  Thus the complete
   lower-rank transverse two-root graph-extension branch is empty.  S2BQ now
   classifies the lower-rank three-root derivatives into injective rank nine,
   shared-factor rank eight, and Hilbert--Burch rank seven, with exact torus
   and kernel-incidence atlases.  S2BR starts the full empty-target coupling:
   it gives the complete root-row kernel atlas on the rank-four/rank-eight
   cell and excludes the involved `(2,2)` subcell with distinct missing
   colours.  S2BS additionally excludes the exact same-colour third-row-
   rank-two coordinate split lift through a rank-free eight-product
   obstruction.  S2BT then uses the two missing-row contractions of the pure
   target coefficients to force both split vectors and derive the exhaustive
   nonaligned/aligned support-one four-space atlas.  S2BU closes the whole
   aligned chart through a four-row Segre-tangent rank contradiction.  S2BV
   classifies every nonaligned local control and proves that its unique pair
   lift has an unavoidable coordinate-divisor pole.  Thus the complete
   coordinate-third-kernel same-colour `(2,2,2)` graph cell is closed.  S2BW
   uses the two complementary pure-target corrections to rule out support-two
   third kernels by projection rank.  Hence the complete same-colour
   `(2,2,2)` rank-two-third-row profile is closed.  S2BX then uses the
   injective third projection to reduce the full singleton correction to one
   line; the `P_3` rank obstruction leaves an exact binary frame with a common
   zero.  Shifting that frame along the zero and applying the exact
   intersecting-plane obstruction forces the zero into two transverse row
   planes.  Hence every same-colour `(2,2,q)` profile is closed.  S2BY notes
   that the argument needs only one deficient involved row when the third row
   is injective; restriction of the other row to the complementary colours
   closes `(2,3,3)` and `(3,2,3)`.  S2BZ then observes that a support-two
   third kernel confines every non-missing correction to one root-tensor
   line, while its two target coefficients demand two distinct diagonal
   lines.  S2CA closes the last mixed support-one cells: projection rank
   forces one split-lift orientation, four third-face coefficients create a
   cubic resonance frame, and two missing-colour coefficients collapse two
   independent dual rows onto one line.  Hence every profile with a deficient
   involved row is closed.  S2CB then handles fully injective involved rows
   with third-row rank two: vertical lifts violate projection rank, while the
   nonvertical direct root box and the `P_3` rank fork reduce to equal-plane
   binary or two-square obstructions.  S2CC starts the remaining `(3,3,3)`
   profile: for a monomial residual `C=e_d tensor e_e`, an exact binary face
   with a common zero excludes every point off `w_d=w_e=0`.  S2CD then uses
   both physical common rows and 29 exact row-space charts to exclude
   complementary support two at a diagonal endpoint.  S2CE uses the complete
   sparse-edge face, an exhaustive projective flag atlas, and independently
   replayed exact certificates to exclude the off-diagonal coordinate
   endpoint.  S2CF then restores the unsliced target equation at each surviving
   diagonal endpoint: two source tensors are recovered at their exceptional
   entries, all sixteen other face equations are retained, and the last slice
   is one nonzero tangent-coset rank-one condition.  Their perpendicular
   contraction gives a corrected `2 x 2 x 3` cube in the third-row space but
   does not replace the complete faces.  A two-radical lemma removes its fully
   supported exceptional-intersection orbit, while exact omission and quotient
   controls prove that the full coupling is essential.  S2CG separately uses
   the full-sensor alternating tensor, a mixed-zero-pair support lemma, and an
   exhaustive nine-flag cover to exclude the exact nonmonomial orbit with all
   three shared factors on one coordinate line and a complementary diagonal
   binomial residual.  Its general radical-line theorem then combines with
   S2CF in S2CH: simultaneous failure of both diagonal-endpoint visibility
   conditions creates a forbidden two-dimensional radical shore, so the
   entire zero-visible wall is empty.  S2CI then combines the same zero-pair
   geometry with the complete recovered faces and unsliced source coupling
   to exclude the two same-coordinate one-visible cells `x=y=e_0,e_1`.
   S2CJ exhausts the resulting twenty-mask one-visible support atlas: four
   masks give forbidden radical shores, thirteen fall to the cross-pair
   incidence dichotomy coupled to the recovered faces or source quotient,
   and the final `{0,2}` by `{0,2}` mask falls only after the whole unsliced
   root matrix forces a graph-gauge collapse.  S2CK closes the remaining
   two-visible system by an exact fourteen-mask cover.  Four central masks
   would put both transverse target tensors in one polarized split-cubic
   mixed map, contrary to a source-support/Segre-tangent obstruction.  Each
   of the other ten masks has one structural zero pair and two transverse
   correction-free corners, contrary to the S2CG zero-pair classification
   and the zero-corner rectangle obstruction.  Thus both diagonal monomial
   endpoints are empty; with S2CE, the monomial-residual branch of the
   fully-injective joint-rank-four/derivative-rank-eight cell is closed.
   S2CL then keeps the actual nonmonomial residual block in the complete
   three-slice equations.  It excludes every correcting mixed zero and proves
   that any remaining mixed zero is one of at most four explicit structural
   projective pairs.  S2CM exhausts the S2BQ root-torus split under the
   zero-pair-free assumption: both the noncoordinate tangent-quotient branch
   and the two ranks of the coordinate `2 x 2` residual restriction create a
   forbidden two-target mixed map.  S2CN then attacks the structural successor
   with both shared factors noncoordinate.  Its coordinate zero shore gives a
   one-sided target table; independent zero-pair geometry splits the source
   space, while the dependent branch manufactures a second structural corner.
   S2CI reduces both to the same aligned source quotient, and a retained face
   would make the actual residual block monomial.  S2CO exhausts the remaining
   coordinate-shared-factor cells.  The `y_s!=0` branch is an exact `2 x 2`
   cross-zero atlas; the `y_s=0` noncoordinate branch falls to its structural
   map's zero-pair geometry; and coordinate `y` has a complete matrix-rank and
   pure-pencil split.  The final pencil boundary uses only one retained
   diagonal coefficient, avoiding any claim that a whole slice vanishes.
   Hence the complete fully-injective joint-rank-four/derivative-rank-eight
   residual profile is closed.  The other derivative ranks and pair gates
   remain.
   This obligation does not address the
   all-balanced rank-drop
   branch.

3. **All-balanced mixed-word exclusion.** Intersect the balanced maximal-minor
   ideals with the full mixed GHZ zero equations and prove emptiness, or derive
   a smaller exact branch.  Complete support, invertible blocks, local
   concision, and the normalized pure coefficients are insufficient by the
   diagonal-complete family; its explicit mixed even-colour coefficients are
   the missing equations.  The whole vertex-gauge common-quadratic orbit is
   now excluded by a `6` versus `3` flattening mismatch, so the surviving
   branch is genuinely nonsynchronized.  More generally, a common root
   quadric forces every nonconstant mixed cross permanent to be divisible by
   that quadric and fixes the constant-word pure residue.  These complementary
   equations exclude the entire physical common-conformal shore, regardless
   of its scalar permanent.  A fully supported point on the common conic also
   exposes the existing zero-surplus restriction `P_m -> Delta_3`, without
   any cross-column separability: this excludes the full common-quadric shore
   at `m=3,4` and routes `m>=5` to the permanent frontier.  A normalized
   eight-vertex control shows that all-cut rank drop cannot force a root-ideal
   basepoint in a prescribed same-vector gauge, even with invertible blocks,
   local concision, and pure normalization.  The full anchored mixed slices
   now give a gauge-invariant alternative: on every five-set, every induced
   `K_5` tuple whose ten blocks are all nonzero lies in a closed projective
   codimension-at-least-three three-colour boundary envelope; the affine
   envelope also includes whole-zero-block branches.  For one fixed adjacent
   pair, exact synchronization improves this to codimension at least five;
   imposing the all-balanced minors cuts the equality sources properly and
   gives ambient affine codimension at least six.  A proposed four-chart
   refinement over one common `K_4` is withdrawn after an exact
   tensor-span-rank boundary: four distinct partition-block pairs can have
   only a two- or three-dimensional tensor span.  The explicit feasible
   stratum has a locally projected affine incidence image of codimension
   eight, so the prior codimension-nine/ten lift is not valid.  Corrected
   span-rank stratification and the `B_all` intersection remain open.  Rank drop, pure
   coefficients, and all
   Hamming-one equations still do not force adjacent fixed-gauge basepoints;
   pair-local Hamming-two equations detect only the monomial synchronized
   control class.  The residual S3 problem is to prove compatibility or
   further dimension gain among the `70` four-chart pencil pullbacks and then
   couple those loci to the remaining mixed equations and
   transverse/nontransverse boundary strata, without assuming codimensions
   add.

4. **Zero-surplus permanent restrictions.** Every hypothetical restriction
   lies in the simultaneous co-two product-sensor corank-two locus.  The
   `P_6` equality-five branch is now excluded by the complete based-frame
   orbit synthesis and adversarial consolidation audit.  Every hypothetical
   `P_6` restriction is therefore forced into the product-dimension
   at-least-six branch, where all fifteen corresponding sensor ranks are at
   most twelve.  At equality six, pair-level admissible frames already fill a
   nine-dimensional open with at least four parameters beyond monomial
   covariance, and the twelve-dimensional linear annihilator envelope is
   rank-three compatible.  The live obligation is the factorized four-mode
   incidence and its compatibility across all fifteen pairs; none of these
   pair-level or dimension statements is `P_6` closure.  The exact `P_6` block model
   shows that sensor rank drop, local rank, and nonzero pure coefficients alone
   are insufficient. The committed P7 sensor and exactly-three-excess support
   normal forms are not exhaustive arbitrary-r theorems.

5. **Active word holonomy and pure-shore cancellation.** Every active
   coordinate has a cofactor-active cross core. Absent the deeper branch,
   bridge normalization either transports activity to a new mixed word with
   the same multiplicities or exposes a pure-shore hafnian that cancels
   despite containing a nonzero matching term; no-exit iteration yields a
   finite nontrivial active-word cycle. In addition, global support
   minimality first forces a positive integral endpoint-label multicover and,
   over `C`, then a positive GHZ gauge with vertex-independent loads of the
   actual squared amplitudes. Intersect that magnitude normal form with the
   full response and deeper-bridge topology to exclude one exit, or use
   additional coefficient identities to make transport impossible. The
   exact unit-phase eight-vertex nonwitness is already moment-balanced,
   retains the local algebra of one ternary bridge-pattern transport, and
   keeps all three nonrigidity sets proper. At the next exact depth, an
   active cycle has a nonzero gauge-invariant Laurent circulation: either a
   fibre has an extra compatible term or binomial fibres force
   `lambda^z=(-1)^m`. A complete eight-vertex table now attains `-1` while
   also having all pure target coordinates, strict endpoint balance, an
   actual moment-balanced representative, and three proper nonrigidity sets.
   Its exposed mixed coefficient is a one-monomial obstruction in
   multiplicity `(7,1,0)`, outside the `(4,4,0)` transport stratum, so it
   rejects that fixed label support without constraining `H`.  The table's
   only additional zero mixed fibre shares cycle variables, but an exact
   `Q(t)` deformation satisfies it and the three cycle equations with
   `H=-1`; the selected elimination ideal in `H` remains `(H+1)`.  Imposing
   the **complete** `(4,4,0)` block on that fixed table gives a different
   outcome: ten singleton fibres make the Laurent ideal `(1)`, so the support
   is excluded before any stronger polynomial in `H` arises.  The arbitrary-
   cycle step is still open because equal multidegree is only a grading, not
   a proved transport closure.  The complete-block fibre-lattice theorem now
   makes every singleton a unit and classifies every all-binomial block by
   exact signed-kernel parity.  For a fully binomial active cycle, the
   binomial-core quotient theorem further decides all residual aggregate
   systems of quotient free rank zero or one by finite torsion characters and
   Laurent gcds.  The global target-lattice theorem then removes the same-
   multidegree restriction: arbitrary mixed blocks share one exact endpoint-
   character-kernel algebra, pure targets add anchor directions, and a proper
   fully binomial-cycle quotient still imposes only the known sign.  What
   remains is to force the combined ideal to be a unit by killing a favourable
   low-rank quotient, controlling free rank at least two or an aggregate cycle
   fibre, proving effective cross-multiplicity unit forcing, or coupling to
   the deeper topology.
   An aggregate active cycle now has the exact defect formula
   `H=(-1)^m product_i(1+A_i)`.  The defects are gauge invariant, but the
   cycle equations alone do not couple them: a complete locally concise
   `5/2/2`-fibre family has `H=-2/(1+2t)` and zero elimination ideal in `H`.
   At `t=1/2`, its aggregate extras cancel separately and the ordinary odd
   sign survives.  The family fails every pure target, so the still-open step
   is to use the remaining target equations to constrain the defect product
   or force the global ideal to be a unit.  For every offdiagonal extra term,
   the new attachment theorem now makes this concrete: a cancelling source
   or bridge shore has a conformally minimal primitive cycle, sparse fan, or
   aggregate port whose matching differences embed termwise in the mixed
   fibre; otherwise the bridge enters deeper data or activates another
   complete target equation.  On a shortest cycle, the active word is outside
   the cycle or is its selected successor.  A pure-anchor-compatible exact
   `3/2/2` family realizes the parallel case with zero new successor-fibre
   difference and variable `H=-1/(1+t)`; its complete target system is killed
   by a separate singleton.  What remains is to force such a unit or useful
   non-direct overlap in general or control distinct parallel successor pairs.
   The complementary diagonal-only case now factors exactly as a Cartesian
   product of pure-shore matching polynomials, with a direct sum of shore
   difference lattices and at least one primitive alternating-cycle
   direction.  A complete pure-anchor-compatible twelve-vertex `3/2/2` family
   makes the selected cycle unique and shortest while its four fibre
   directions remain saturated and independent despite shared physical
   edges; `H=-1/(1+t)` is still free.  Its outside singleton excludes that
   support, but an arbitrary complete-target unit, useful non-direct overlap,
   proper-subshore cancellation, or deeper exit is not yet forced.
   A least pure cancelling residual now has a connected matching-covered
   allowed core.  Its degree-two branch is one primitive binomial cycle with
   monomial cofactors.  At every branching vertex, the multi-cycle core
   further splits into a sparse conformal `d`-fan with an exact `d`-nomial
   relation or a nonzero aggregate cofactor port; its two-exit carriers have
   only the closed all-odd and one-open-port theta profiles.  Exact families
   realize every one of these pure possibilities.  The next pure-side step
   must therefore control an aggregate port or couple a sparse fan character
   to mixed response or genuine deeper-blocker data.

6. **Remaining larger/unfactorized detector.** The complete aligned
   projectively constant `q=0,r=5` cell is now conditionally detected; the
   lifted physical-row quota removes the apparent four-/five-`B` zero before
   the remaining `R/B` words are closed.  Treat `q=0,r>=6` or `q>=1`, or prove
   a legal selector separating the replacement tensors. Outside that branch,
   produce an exact nonzero selector or otherwise exclude the unfactorized
   high-surplus cell.  The existing cell detectors do not exclude a witness.

7. **All-bridge localized cancellations and bipartite least cores.** Every
   saturated degree now has an active-deck-localized supported pure
   cancellation.  Exclude the inactive-edge-complement form using its two
   inactive common-cofactor-zero repairs, or prove simultaneous control of
   both factors of the selected-matching-component/complement and Hamiltonian-
   chord-arc/complement cuts.  Separately, couple a primitive even-cycle or
   closed all-odd-theta relation to mixed response or control a forced nonzero
   aggregate cofactor port.  In the extremal sparse stratum `d=N=beta+1`,
   `A4` reduces the opposite shore to a second extremal odd multi-theta site
   or several lower-degree aggregate sites.  At `beta=3`, `A5` further pairs
   the four odd-route singleton ports and identifies the `Q/C^2` even-route
   aggregates as complementary nonzero doubletons with exact-negative
   edge-inclusive sums.  `A6` now shows that any one compatible fixed
   completion carries those four terms into a rank-three zero block in a
   complete mixed fibre, forces the full fibre size to be four or at least
   six, and preserves the exact-negative doubletons.  `A7` then filters the
   sign restriction whenever that rank-three difference lattice is integrally
   contained in a parity-consistent binomial core: every imbalanced sign
   restriction is a global unit, while balanced `Q/C^2` has only one
   nonzero-port-aligned partition and balanced `Q/Q` retains all three.
   `A8` proves that the sparse-port coordinates make the `A6` lattice
   primitive.  Thus exact complete-fibre rank three collapses to that lattice,
   and, under `A7` containment, every surviving fibre is even; odd sizes
   `7,9,...` are excluded in this conditional branch.  An additional physical
   comparison already landing there is exactly a sparse port-pair edge.  A
   within-doubleton edge closes aligned `Q/C^2`; a predetermined uniform
   `Q/Q` closure needs a triangle or `K_(1,3)`, while `P_4` is sharp.  The next
   step is to force the completion, rank equality, containment, and those
   comparison carriers, or control the rank-at-least-four or uncontained
   ideal.  The complementary fibre may be empty, so neither `A8` nor equality
   `N=beta+1` is a universal exclusion.  The three balanced `Q/Q` cuts are
   alternatives across possible binomial cores, not simultaneous sheets.
   In parallel, `A3R` turns every allowed least-core edge into two exact
   opposite-colour response zeros.  A supported response lands on the
   `2|S|<=n+2` side and attaches a conformally minimal relation to one mixed
   fibre; on the large-shore side all such responses are support-unmatchable.
   Same-colour conformal failure now gives a finite minimum-crossing portal
   family whose every induced nonempty image is unmatchable.  The next honest
   step is to force a supported/aligned response, exploit those portal
   obstructions, or prove new target-lattice coupling.  Active-neighbour
   separation alone does not do this: the active colour's own bit is free,
   and, only for a co-two exterior with `|S|>=6`, the conclusion is an
   independent exterior-neighbour set.
   The globally least core need not retain localized cut labels.  Degree five
   adds subcubic typed sites, but localization and the bipartite rank-one/
   rank-two structure are all-degree.  The deeper-blocker branch remains
   separate.

8. **Component 22 remaining finite-`D23` residual.** The whole generic
   `H=f2=f8=0` cell over `Q(A,R,D)` is now empty: one maximal minor forces
   `h0`, and two further minors have incompatible linear `h3` factors.  This
   includes both `2h3+s=0` and its isolated complement, but it does not close
   special parameter fibres.  Close the remaining `f2=0` residual outside
   `f8=0`, together with its special/projective/source boundaries.  The
   generic finite-`D01` pair orbit is already excluded by its separately
   owned theorem, but its special/projective component fibres remain open. See
   the [generic complete intersection](../claims/p5/h22/unequal-complement-common-kernel-component-d23-f2-f8-generic-complete/P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_F2_F8_GENERIC_COMPLETE_OBSTRUCTION.md),
   the [finite-`D01` owner](../claims/p5/h22/unequal-complement-common-kernel-component-d01-pair-orbit/P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D01_PAIR_ORBIT_OBSTRUCTION.md),
   and the [two-minor partial owner](../claims/p5/h22/unequal-complement-common-kernel-component-d23-h1-nonzero-two-minor-factor-cover-partial/P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H1_NONZERO_TWO_MINOR_FACTOR_COVER_PARTIAL_OBSTRUCTION.md).

9. **P4-B3 semantic/composition audit.** Audit the nonzero-pure-factor, symmetry,
   inclusion, and lower-pair quantifiers in the
   [P4 all-pair-rank reduction](../claims/p4/classifications/P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md).
   The owner asserts a 25-component exhaustiveness theorem; the independent
   acceptance of those load-bearing quantifiers remains open. Script replay is
   not a substitute for that review.

10. **Committed P7 calculation.** Materialize the residual equations, pull back
   the factor equations, justify properness/finiteness where used, and decide
   `A_good`; proceed to `A_gen^star` only if the criterion requires it. A result
   on this fixed sensor would still need `GL`.

Component 25 is not a closed shortcut: its finite-`D23` three-branch cover is
not an exclusion, and finite-`D01`, special fibres, and projective boundaries
remain open.

Within the `r=1` route, the minimum-word cells `k=1`, `k=2`, and `k=3`
remain distinct positive obligations. The port theorem packages their exact
responses; it does not collapse them into the globally rigid `k=4` cell.

## Refuted or insufficient proof routes

| Route | Exact finding | Owner |
|---|---|---|
| Automatic characteristic-zero to `F_2` reduction | Refuted as a general lemma; good reduction and prime-field residue are not forced | [Characteristic-two boundary](../claims/arbitrary-order/CHARACTERISTIC_TWO_CONTRACTION_LIFT_OBSTRUCTION.md) |
| Fixed surplus determines balanced-sensor rank | False: one fixed-layer fibre can contain deficient and full uncontracted shores | [Fixed-surplus nonobservability](../claims/arbitrary-order/BALANCED_FIXED_SURPLUS_TRUNCATION_FIBRE_NONOBSERVABILITY_AND_TRANSVERSE_ABSORPTION_THEOREM.md) |
| The first two-open equation always detects the affine gauge | False on a conditional tight `q=0` outside-star cell | [Two-open star invisibility](../claims/arbitrary-order/BALANCED_TWO_OPEN_ROOT_GAUGE_DETECTOR_AND_STAR_INVISIBILITY_BOUNDARY.md) |
| Primitive or pure scalar hafnian pencils close the rigid branch | False at arbitrary order; mixed deletion and completion coupling remain essential | [Primitive sharpness](../claims/arbitrary-order/RIGID_COLOUR_THREE_BLOCK_PRIMITIVE_SHARPNESS_AND_DUAL_BRIDGE_COMPLETION_OBSTRUCTION.md) |
| Bogdanov-backbone cancellation alone contradicts equality | False: all selected backbone mixed words can cancel while other words fail | [Rigid-colour cancellation boundary](../claims/arbitrary-order/RIGID_COLOUR_COFACTOR_ANNIHILATION_AND_BACKBONE_CANCELLATION_BOUNDARY.md) |
| Bridge normalization, parity/Wick, or fully active pure cofactors synchronize each individual term | False; exact six-vertex countermechanisms retain unsynchronized compatible terms inside aggregate-zero fibres. Nonzero aggregate fibres are nevertheless word-shore synchronized by the later factorization theorem. | [Word-synchronization boundary](../claims/arbitrary-order/MATRIX_UNIT_BRIDGE_WORD_SYNCHRONIZATION_AND_WICK_SHARPNESS_BOUNDARY.md) and [active parity-fibre refinement](../claims/arbitrary-order/MATRIX_UNIT_PARITY_FIBRE_DIAGONAL_FACTORIZATION_AND_ACTIVE_WORD_SHORE_SYNCHRONIZATION_THEOREM.md) |
| Positive endpoint-label balance turns complex matching cancellation into convexity or excludes active transport | False: the balance weights are incidence-dual multiplicities, not physical amplitudes. A complete balanced eight-vertex nonwitness has pure coefficients `(1,1,1)` and two exact active fibres joined by the forced ternary bridge label pattern, while a different mixed coefficient remains nonzero. It reproduces local transport algebra but makes no geometric deeper-component claim. | [GHZ diagonal-torus endpoint-balance sharpness](../claims/arbitrary-order/MATRIX_UNIT_GHZ_DIAGONAL_TORUS_POLYSTABILITY_ENDPOINT_BALANCE_AND_ACTIVE_TRANSPORT_SHARPNESS_THEOREM.md#3-a-balanced-active-transport-table) |
| Moment-balanced actual squared amplitudes make matching cancellation positive or force every nonrigidity set global | False from those hypotheses alone: an exact Eisenstein unit-phase table has actual load `(3,2,2)` at every vertex, pure coefficients `(1,1,1)`, two active cancellations `1+(-1)=0`, and three proper nonrigidity sets, while an exposed mixed coefficient proves it is not a witness. Full-target propagation remains open. | [GHZ moment-balanced unit-phase sharpness](../claims/arbitrary-order/MATRIX_UNIT_GHZ_MOMENT_BALANCED_GAUGE_AND_UNIT_PHASE_ACTIVE_TRANSPORT_SHARPNESS_THEOREM.md#4-exact-unit-phase-active-transport-table) |
| Binomiality plus completion, pure normalization, moment balance, proper nonrigidity, and one locally coupled neighbouring mixed equation exclude an odd active-word cycle | False: a complete eight-vertex matrix-unit table has all three pure coefficients one, strict balance, a moment-balanced representative, three proper nonempty nonrigidity sets, and three complete fibres `(1,-1)` with `H=-1=(-1)^3`. Its exposed word is transport-isolated, while an exact `Q(t)` deformation also satisfies the table's only additional zero mixed fibre and leaves that selected holonomy elimination ideal `(H+1)`. The **complete** same-multidegree block does reject the fixed table, but by a singleton Laurent unit rather than a stronger holonomy relation; no arbitrary-cycle inference follows. | [Complete moment-compatible odd-holonomy sharpness](../claims/arbitrary-order/MATRIX_UNIT_COMPLETE_PURE_TARGET_MOMENT_COMPATIBLE_ODD_HOLONOMY_SHARPNESS_THEOREM.md), [exposed-fibre transport isolation](../claims/arbitrary-order/MATRIX_UNIT_EXPOSED_MIXED_FIBRE_TRANSPORT_ISOLATION_AND_NEIGHBOUR_SHARPNESS_THEOREM.md), and [same-multidegree saturation exclusion](../claims/arbitrary-order/MATRIX_UNIT_U7D_COMPLETE_SAME_MULTIDEGREE_TARGET_BLOCK_SATURATION_EXCLUSION_THEOREM.md) |
| Shortest-cycle minimality forces every aggregate extra matching to expose a new outside word or a nonzero successor-fibre lattice direction | False: an exact ten-vertex pure-anchor-compatible `3/2/2` family has an offdiagonal extra whose nonzero bridge output is exactly the already selected successor matching, so its successor difference vector is zero. A different singleton target word excludes the fixed support; the family is not a witness. | [Aggregate extra-matching target attachment](../claims/arbitrary-order/MATRIX_UNIT_AGGREGATE_EXTRA_MATCHING_TARGET_ATTACHMENT_THEOREM.md#6-pure-anchor-compatible-parallel-sharpness) |
| A primitive diagonal exchange or shared physical variables force an odd dependency or cross-fibre lattice coupling | False: a complete twelve-vertex `Q(t)` family has the unique shortest active `3/2/2` cycle, one primitive diagonal six-cycle extra, all pure coefficients one, and three shared physical variables, yet a determinant-one minor makes its three fibre lattices a direct saturated rank-four sum with no integer dependency. Its selected holonomy is `-1/(1+t)`; an outside singleton, not the diagonal exchange, excludes the fixed support. | [Diagonal aggregate shore-product sharpness](../claims/arbitrary-order/MATRIX_UNIT_DIAGONAL_AGGREGATE_SHORE_PRODUCT_AND_PRIMITIVE_EXCHANGE_SHARPNESS_THEOREM.md#4-complete-twelve-vertex-sharpness-family) |
| One fixed P7 survivor or incidence result globalizes automatically | False as an inference: one still needs physical edge descent, all Wick equations, and universal extraction | [Balanced sensor Wick gate](../claims/arbitrary-order/BALANCED_HALF_SENSOR_COMPLETE_DECK_AND_WICK_GLOBALIZATION_THEOREM.md) |
| Determinant-cleared Wick identities automatically remove Cramer poles | False: a normalized four-label rational hafnian deck can satisfy the cleared Euler recurrence while one pair has valuation `-1` | [Cramer--Euler pair-pole boundary](../claims/arbitrary-order/BALANCED_FULL_SENSOR_CRAMER_EULER_PAIR_POLE_GATE_THEOREM.md#5-sharp-boundary-cleared-wick-does-not-remove-poles) |
| Either endpoint Hessian flatness alone or nonendpoint transverse flatness alone removes every ambient multihomogeneous pair pole | False in both directions at the rational-section level: an outside degree-zero ratio passes both endpoint Hessians but has a transverse pole, while an endpoint degree-one ratio has no outside dependence but fails an endpoint Hessian. Neither control is realized as a balanced target incidence, so no independent sharpness claim inside the Cramer image follows. | [Pair-pole differential-flatness ambient sharpness](../claims/arbitrary-order/BALANCED_FULL_SENSOR_CRAMER_PAIR_POLE_DIFFERENTIAL_FLATNESS_THEOREM.md#5-ambient-sharpness-both-jet-layers-are-needed-from-degrees-alone) |
| The tautological selected Cramer equation `Af=j` forces a pair replacement minor either to vanish or to be nonzero | False for abstract Cramer systems: diagonal `2 x 2` systems realize both the transverse-pole and endpoint-pole outcomes exactly.  They are not balanced complete-deck sensors with the GHZ target, so no sharpness inside the actual target-incidence image follows. | [Pair-jet replacement-minor boundary](../claims/arbitrary-order/BALANCED_FULL_SENSOR_CRAMER_PAIR_JET_REPLACEMENT_MINOR_THEOREM.md#5-sharp-boundary-cramer-consistency-alone-selects-no-outcome) |
| Complete `27`-row GHZ target consistency, empty normalization, rank, deck-complement column degrees, and seven retained pair conditions make the eighth condition redundant | False at the degree-compatible full-row level: eight exact `m=3` controls separately make each retained coordinate the sole nonzero one.  They are not proved common-shore matching-sum sensor realizations and do not establish sharpness inside actual balanced target incidences. | [Normalized full-row compatibility boundary](../claims/arbitrary-order/BALANCED_FULL_SENSOR_CRAMER_PAIR_EMPTY_NORMALIZATION_CONTROL_COMPATIBILITY_THEOREM.md#5-exact-proof-topology-consequence) |
| Degree-compatible full-row target consistency, empty normalization, and rank imply common-shore matching-sum realizability | False at `m=3`: an exact normalized target-consistent rank-four Latin-plane system has nine independent singleton slices, but their coordinate subspace contains no complete tensor-axis line and cannot equal any common-shore shared-factor subspace.  The separator imposes no retained pair jet and decides no S2M control. | [Common-shore Latin-plane separator](../claims/arbitrary-order/BALANCED_FULL_SENSOR_COMMON_SHORE_SINGLETON_SLICE_AND_EMPTY_PERMANENT_COMPATIBILITY_THEOREM.md#2-a-normalized-full-row-system-outside-the-image) |
| Three vanished singleton slices force the corresponding empty-companion coefficient to vanish | False even in one-dimensional root spaces: three vectors in the plane `u_1+u_2+u_3=0` can have nonzero `3 x 3` permanent.  This does not contradict S2P: its obstruction uses the simultaneous transverse pure tensor in the shared-factor image. | [Normalized control pullback boundary](../claims/arbitrary-order/BALANCED_FULL_SENSOR_COMMON_SHORE_NORMALIZED_PAIR_CONTROL_PULLBACK_REDUCTION.md#3-the-exact-residual-obligation), [binary residual obstruction](../claims/arbitrary-order/BALANCED_FULL_SENSOR_COMMON_SHORE_BINARY_SYZYGY_PERMANENT_RESIDUAL_OBSTRUCTION_THEOREM.md#6-sharpness-of-the-shared-factor-conclusion) |
| Function-field independence of the three separated `m=3` singleton columns prevents every divisorial Cramer pole | False for abstract separated columns: a rank-one singleton image, a pair contained in one plane, or three images contained in one three-space each gives an exact rank-drop divisor and a global target with a genuine rational pole.  The theorem proves these are the only divisor mechanisms; the controls are not physical GHZ incidences. | [`m=3` separated-singleton pole localization](../claims/arbitrary-order/BALANCED_M3_FULL_SENSOR_SEPARATED_SINGLETON_POLE_LOCALIZATION_THEOREM.md#5-sharp-separated-column-controls) |
| A three-dimensional singleton span automatically has a fully supported product annihilator | False: the target diagonal root plane blocks the whole root torus, since annihilating each diagonal basis tensor forces at least one local coordinate to vanish for every colour.  That particular plane cannot support full sensor rank under target consistency, but other coordinate-boundary blocking spaces remain open. | [Singleton-span torus-annihilator boundary](../claims/arbitrary-order/BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md#5-sharp-boundary) |
| Local concision, complete support, invertible blocks, and normalized pure coefficients force some balanced sensor to be full | False for every `n>=8`: the diagonal-complete family has all these properties and rank at most `binomial(m,2)+1` on every cut; it fails explicit mixed-word zero equations | [Diagonal-complete all-rank-drop boundary](../claims/arbitrary-order/BALANCED_ALL_RANK_DROP_DIAGONAL_COMPLETE_SHARPNESS_THEOREM.md) |
| Independent local basis changes can rescue the common-quadratic all-rank-drop mechanism as a witness | False: the synchronized orbit has two-vertex flattening rank six when nondegenerate, invariant under every local isomorphism, while ternary GHZ has rank three; degenerate forms already fail local rank | [Common-quadratic orbit exclusion](../claims/arbitrary-order/BALANCED_COMMON_QUADRATIC_ORBIT_RANK_DROP_AND_FLATTENING_EXCLUSION_THEOREM.md) |
| Arbitrary internal nonroot blocks can repair a common-conformal balanced shore | False: modulo the common root quadric every non-all-cross sector vanishes; nonzero scalar permanent leaves a forbidden mixed product, while zero permanent contradicts the nonzero pure-root product from a constant word | [Common-quadric mixed/pure residue theorem](../claims/arbitrary-order/BALANCED_COMMON_QUADRIC_MIXED_PERMANENT_DIVISIBILITY_AND_CONFORMAL_SHORE_EXCLUSION_THEOREM.md) |
| All-balanced rank drop plus invertible blocks, local concision, and normalized pure coefficients force a common zero of the same-vector root quadrics in a prescribed gauge | False at `n=8`: a normalized rational common-quadratic-orbit graph has every balanced sensor of rank at most seven, while six root quadrics in the target gauge span all of `Sym^2(C^3)^*` and have empty projective base locus.  Independent vertex gauges recover one common conic, so the fixture does not refute latent synchronization. | [Root-quadric basepoint gauge sharpness](../claims/arbitrary-order/BALANCED_ROOT_QUADRIC_BASEPOINT_PERMANENT_RESTRICTION_AND_GAUGE_SHARPNESS_THEOREM.md#4-all-cut-rank-drop-does-not-force-a-fixed-gauge-basepoint) |
| Two adjacent all-rank-drop shores, nonzero pure coefficients, and all Hamming-one mixed equations force compatible same-vector root-ideal basepoints | False at `n=8`: an exact invertible monomial common-form graph has every balanced sensor of rank at most seven, pure coefficients `(1,1,1)`, all `48` Hamming-one coefficients zero, and both adjacent six-quadric ideals equal the irrelevant square with empty projective base locus.  A pair-local Hamming-two coefficient is `-1`; latent gauges recover synchronization, so no existential multiroot claim is refuted. | [Adjacent-cut monomial Hamming-shell sharpness](../claims/arbitrary-order/EIGHT_VERTEX_ADJACENT_CUT_MONOMIAL_HAMMING_ONE_BLINDNESS_AND_HAMMING_TWO_DETECTOR_SHARPNESS_THEOREM.md) |
| Simultaneous co-two permanent sensor corank two, local rank, and nonzero pure coefficients exclude P6 | False as an argument: an exact two-block coordinate model has all fifteen four-mode sensors of dimension at most nine and all pure coefficients nonzero, but has mixed support and flattening rank one rather than the target rank three | [Co-two permanent product-sensor boundary](../claims/arbitrary-order/ARBITRARY_PERMANENT_COTWO_PRODUCT_SENSOR_RANK_DROP_THEOREM.md#5-sharpness-of-what-rank-drop-alone-can-say) |
| Only equal regular ratios survive the four-regular five-cell common kernel | False: a `2+2` reciprocal primitive-cube-root divisor also gives a one-dimensional kernel; the corrected dimension bound still closes detection | [Complete aligned five-cell detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_ALIGNED_FIVE_CELL_TWO_OPEN_DETECTOR_THEOREM.md#lemma-2-four-defect-full-common-kernels) |

These are refutations of arguments, not counterexamples to the Krenn–Gu
conjecture.

## Evidence, disagreements, and maintenance

- The P4 owner asserts a 25-component exhaustiveness theorem. The programme
  retains P4-B3 as a human semantic/composition audit of its load-bearing
  quantifiers. This is an audit-acceptance gap, not an automatic mathematical
  contradiction and not permission to call the cover either unproved or fully
  audited without qualification.
- Several P5 results are generic/function-field or divisor-specific. Package
  colocation, a component count, or a finite certificate does not close their
  special and projective boundaries.
- The external characteristic-two Lean project is source-inspected candidate
  evidence here; local build replay and statement correspondence remain
  pending. The local algebraic route obstruction is independent of accepting
  that external formalization.
- `primary_verifier` and `independent_audit` are evidence roles, not
  mathematical premises. Bounded checks do not prove arbitrary-order prose.
- Any PR that changes a node, edge, open leaf, route refutation, or local/global
  scope on this page must update it. A PR that changes mathematical claims but
  leaves this live frontier unchanged must explicitly state why no frontier
  update is needed. The owning claim document must change when the theorem
  itself changes.
- CI renders this Mermaid block with the pinned Mermaid CLI. Keep edge labels
  containing punctuation quoted so GitHub and the CI renderer parse them alike.

The detailed reconstruction, reviewer disagreements, relocation inventory,
and PR #72–#82 evidence are in the
[programme proof-topology audit](audits/PROGRAMME_PROOF_TOPOLOGY_AUDIT_2026-08-10.md).
The superseded chronology remains available in the
[2026-08-05 frontier snapshot](history/current-frontier-stabilization-snapshot-2026-08-05.md)
and [2026-08-10 handoff](history/handoffs/SYMBOLIC_PROGRAM_HANDOFF_2026-08-10.md).
