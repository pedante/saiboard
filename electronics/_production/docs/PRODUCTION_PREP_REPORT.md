# Saiboard production preparation report

Updated **2026-10-30**. **NOT RELEASED FOR MANUFACTURE.**

## 1. Summary and current status

**Re-scoped to minimum-change manufacturing preparation; 8x3 prototype first. Stopped at Decision02 for the family-wide LED choice; BOM-05/09 approved, BOM-19 pending.** All four designs remain eventual scope. Original circuit and footprints are accepted as proven. Paper qualification findings are advisory unless JLCPCB flags a problem or a part is unavailable. The specific LED comparison remains required. The old Phase3 qualification gates are superseded by the user's re-scope.

**CHG-009 Verified:** R1–R8 are330Ω in schematic and PCB, Value fields only including schematic instance caches. **CHG-016 applied as an export population policy:**89 hand components across one of each design;19 on8x3. Actual assembly exports remain to be generated and checked. **CHG-004 remains Applied-provisional:** no LED ordering-BOM assignment until the user decides.

[Current MUST/CHEAP/PARK scope](../01_audit/prototype_8x3/CURRENT_SCOPE.md), [first passive decision sheet](../01_audit/prototype_8x3/DECISION_01_PASSIVES.md), [tile/full-board totals](../01_audit/prototype_8x3/BOM_TOTALS.md). LED comparison is now documented; import preparation waits for its decision. Originals/snapshot remain untouched; no firmware edits, frame design, upload or ordering.

11x3 length260.7mm is within the published Standard single-PCB maximum460×500mm, but above the panel table250×250mm; width66mm is below Standard single-board minimum70mm.8x3 also has66mm width. Manufacturer handling acceptance remains a workflow item; no frame is designed. Official source/check date and fallback options are in the current-scope note.


### Decision update — 2026-10-30

[LED one-page decision](../01_audit/prototype_8x3/DECISION_02_LEDS.md): nominal contact/pin fit PASS on all four for original drawing, current RGB C5378720 and RGBW C5378724. This is not tolerance/reflow certification. Recommended all-four CHG-004 rollback plus RGB procurement candidate CHG-023 remains **Proposed**, not applied. Current RGB datasheet differs from historical document (12mA version, reset>200µs); prototype advisory only, no code edits. All-or-nothing selection retained.

[Identity/land audit](../01_audit/prototype_8x3/SHARED_LED_SENSOR_CHECK.md):145 LEDs and145 sensors, each one identity/land pattern across four designs. Hall MPN/LCSC absent uniformly; a common future SKU is still required. [Original/snapshot hashes](../01_audit/prototype_8x3/INTEGRITY_2026-10-30.json):117+117 PASS. No CAD edit this update. Shared LED/Hall check avoids duplicate analyses; existing CHG-011/015 meanings are retained and parked qualification stays parked.

[Size, quantities and cost plan](../01_audit/prototype_8x3/SIZE_ORDER_PLAN.md):11x3 four-layer1.600mm; others two-layer.582mm,nominal.6. Difference1.018mm retained.11x3/8x3 widths66mm fall below Standard70mm minimum. Manufacturer handling and conflicting0.6mm-size documentation remain unresolved. After hand exclusions, **8x8 SMT is front-only**, the other three front/back; this corrects the blanket double-sided-service assumption. Service-only cost estimates are not full quotes.

[Author-instruction search](../01_audit/prototype_8x3/ORDER_INSTRUCTIONS_SEARCH.md):223 files searched includingPDF text, imageOCR and archive strings. No exact author quantities/order settings located; native CAD annotations not fully decoded. User's1/1/2/4 mix remains provisional. README describes PCB/stencil and user reflow, not turnkey assembly. Conditional board totals1313 components/170hand/1143SMT candidates;361LEDs+361sensors.19 procurement groups after330Ω merge, not19 approvedMPNs.

**Open decision/release items:** BOM-19 C17930; LED rollback/selection; author's instruction location; current JLC capacitor/resistor/LED stock and full quote;8x3 decoder supply; accepted thickness/handling; subsequent import/export verification. CHG-012 PARKED accepted. CI4 is UI2 output C106:scope3.3Vunder load; CHG-027 PARKED. Import and production output not started.

## 2. Source inventory

117 original files, 55,776,867 bytes, preserved in `00_original_snapshot/`. [Inventory](../01_audit/SOURCE_INVENTORY.md), [SHA-256 CSV](../01_audit/SOURCE_INVENTORY.csv), [format metadata](../01_audit/SOURCE_FORMATS.json). This extracted tree does not establish an upstream commit.

The baseline contains 27 selected original files: 12 EDA files, 12 datasheet/reference assets, README.md, pcb.jpg and paste.jpg. Exact selection and hashes are in the CHG-004 verification. The original family was approved as the base; candidate material remains evidence rather than an automatically adopted library. No historical fabrication files were copied into output.

`02_work/baseline_before_CHG004/` is byte-identical to that original selection and read-only. Eight working schematic/PCB files contain approved CHG-004 LED identity fields; the8x3 pair additionally contains approved CHG-009 resistor Value changes. The other19 baseline files remain byte-identical. Each change has a separate before-copy and parsed-tree reversal proof. Embedded `LED:SK6812` symbols, library IDs, footprints, nets and all geometry remain unchanged.

| Design | PCB / schematic format | Original LEDs | Updated | Uncovered |
| --- | --- | ---: | ---: | --- |
| 11x3 | 20211014 / 20211123 | 33, D1–D33 | 33 | None |
| 8x3 | 20211014 / 20211123 | 24, D1–D24 | 24 | None |
| 3x8 | 20211014 / 20211123 | 24, D1–D24 | 24 | None |
| 8x8 | 20211014 / 20211123 | 64, D1–D64 | 64 | None |
| Total | | **145** | **145** | **None** |

Project JSON schema is 1 except 8x3 schema 3. KiCad 6-era source formats; exact earliest complete-project opener remains **UNVERIFIED**. Installed Flatpak KiCad **10.0.7** successfully reads them. No installation, uninstall, upgrade or source save-over was needed. Counts represent one of each design, not complete-board multiplicities.

## 3. Findings log

**Historical severity ledger below:** original qualification severities are retained for provenance, but do not override the re-scope. Current action classes are in CURRENT_SCOPE.md. F-008 is resolved by CHG-009. Sensor, drive, power, capacitor, library and original-footprint concerns are PARK advisories; sourcing/manufacturer flags remain actionable.

Checked 2026-10-29. Full evidence and proposed resolutions: [Phase 3 audit](../01_audit/phase3/PHASE3_AUDIT.md), [Phase 2 audit](../01_audit/phase2/PHASE2_AUDIT.md), [Phase 1 audit](../01_audit/phase1/PHASE1_AUDIT.md). Severity means production impact, not native tool severity.

| ID | Severity | Finding / disposition |
| --- | --- | --- |
| F-001 | INFO | No MCP file importer; approved user GUI import then MCP verification. |
| F-002 | INFO | Host CLI/MCP path unavailable; Flatpak 10.0.7 copy-only checks work. |
| F-003 | INFO | Historical fabrication files exist; reference only. |
| F-004 | MAJOR | EasyEDA build/import fidelity unverified; Phase 5. |
| F-005 | BLOCKER for release | Full assembly BOM/CPL absent; resolve Phases 3/6. |
| F-006 | BLOCKER for downstream LED reliance | Provisional SKC6812RGBW-WS/C5378724 must pass actual package/pin/electrical verification. |
| F-007 | BLOCKER | Two same-net, equal-priority inner-layer zone intersections on 11x3. No fix/refill applied. |
| F-008 | BLOCKER for assembly | **Resolved by CHG-009:** historical schematic `R330` / PCB `R`; user confirmed330 ohm, now Value330 in both. No resistance ambiguity remains. |
| F-009 | MINOR, conditional | Repeated mechanical-only references; all20 holes already exclude BOM and position output. Preserve flags; if either export includes these duplicates, reclassify MAJOR and reject output. No renaming authorized. |
| F-010 | MAJOR | Library mismatch/missing-library warnings threaten reproducibility. Preserve embedded geometry; no refresh. |
| F-011 | INFO / MAJOR by cause | Proven net aliases INFO; unresolved field/library metadata MAJOR or F-008 BLOCKER. Electrical pin membership agrees. |
| F-012 | MAJOR | Supplied original LED document is 24-bit RGB; candidate family is 32-bit RGBW. Fitted original SKU unknown; firmware impact pending, code untouched. |
| F-013 | INFO | Historical outline/layers/holes agree with both families; exact electrical revision UNVERIFIED. Missing records do not block analysis. |
| F-014 | INFO | Exact minimum opener unverified; use tested 10.0.7. |
| F-015 | BLOCKER for assembly route | All designs have front/back components; service, rails/fiducials and narrow-board framing unresolved. |
| F-016 | MAJOR | 145 AH49E footprints differ from current suggested lands; pin table agrees, exact-package joint acceptance unverified. |
| F-017 | BLOCKER for sourcing | TI SN74HCT138NSR drawing fits retained wide lands nominally, but JLC/LCSC supply is UNVERIFIED. Narrow DR alternatives require footprint/copper approval. |
| F-018 | MAJOR | UI2 pad4/tab unassigned on 11x3 and 8x3; three-pin symbol cannot check it. Verify selected package before any net/pad correction. |
| F-019 | MAJOR | WAGO footprint name 2601-602 versus source document 2061-602; custom connector body/polarity Fab drawing absent. |
| F-020 | MINOR, potentially MAJOR for orientation | Thin legend graphics and some small 11x3 text. No native silk-over-pad violation reported. |
| F-021 | MAJOR | Exact passive, connector and several active MPNs/ratings absent; generic package names cannot establish fit. |
| F-022 | INFO | Closed outlines, source layers and measured fabrication features screened; actual exports still need verification. |
| F-023 | BLOCKER for acceptance | User confirmed nominal0.6mm intent. JLC official size limits conflict (100×100 vs599×497mm); all three thin boards exceed100mm. Exact-size/flatness/tolerance acceptance and mechanical Z dependencies remain unverified. No stackup conversion. |
| F-024 | INFO | Off-grid ERC endpoints, with zero ERC errors and matching pin groups; no coordinate edits. |
| F-025 | MAJOR | Transistor/logic recommended land patterns differ from retained geometry; exact-package overlap acceptance pending. |
| F-026 | BLOCKER for full-channel RGBW release |361 LEDs at datasheet-typical full channels budget14.725A, exceeding README5V10A before other loads. Guaranteed maximum and actual distribution unverified. |
| F-027 | MAJOR |330Ω PNP base-current illustration exceeds HCT1384mA guaranteed output condition; switched sensor supply margin unverified. |
| F-028 | MAJOR |3x8 HC4052 on5V P has nominal3.3V controls; guaranteed logic margin unverified. |
| F-029 | MAJOR | AMS1117 output10µF MLCC capacitance/ESR/load/thermal suitability not established by its general22µF tantalum stability guarantee. |

F-008 corrects the previous report's literal-field claim; raw Phase 1 tool evidence is retained. F-009 was downgraded after confirming mechanical-only scope. Native library warnings are not automatically fabrication violations, and passing spacing checks does not establish part compatibility.

## 4. Change log

**Current status overrides, recorded2026-10-30:**

| ID | Approval / before → after | Evidence / impact / current status |
|---|---|---|
| CHG-009 | Explicit user approval:8x3 R1–R8 SCH R330 / PCB R →330Ω Value only, including instance Value cache | [Verification/diffs](../01_audit/CHG-009/VERIFICATION.json); approved/applied2026-10-29; **Verified**. No net, geometry, firmware or other field change. Backup02_work/baseline_before_CHG009. |
| CHG-016 | Explicit user approval:87 generic connectors +2 WAGO terminals → hand-population export policy | [Exact references/policy](../02_work/ASSEMBLY_POPULATION.json); approved/applied2026-10-29; **Applied, policy coverage Verified**. CAD unchanged; actual BOM/CPL exclusion verification remains pending export. |
| CHG-012 | Conditional quick proof → skipped; exact SOT-223 tab proof not established on one unambiguous page | [Decision01](../01_audit/prototype_8x3/DECISION_01_PASSIVES.md); **Parked, not applied**, prototype advisory only. |
| CHG-007/008 | Optional non-blocking work, where applicable | **Not applicable to8x3**; no zones.11x3 deferred until its work begins; skip if unrelated copper changes. |
| CHG-014 | Generic passives only; Basic first; approvals by BOM-ID | BOM-05/C24497 and BOM-09/C13585 approved2026-10-30 for8x3; identities recorded in02_work/APPROVED_BOM_IDENTITIES.json, CAD/ordering BOM assignment pending. BOM-19 C17930 proposed; live stock unverified. Value fields unchanged. |
| CHG-004/023 | Decision02 recommends all-four RGB rollback and C5378720 candidate; awaiting decision | Applied-provisional; no LED assigned to ordering BOM; hold/rollback decision pending. |
| CHG-006 | Continued authorized analysis/documentation → re-scope record and decision sheet | Current scope and totals linked above; no design impact. |

CHG-010/011/013/015/017/019/022/024/025/026/027 are **PARK**, non-blocking prototype advisories; no further analysis. Unavailable parts and JLC flags may reopen the specific manufacturing issue. CHG-020/021 remain future import/export work. CHG-018 retains nominal0.6mm intent for manufacturer workflow verification.

The tables below preserve the earlier proposal details; their old statuses and qualification gates are superseded by this current-status table and CURRENT_SCOPE.md.

| ID | Phase / category | Affected files/designators; Before → After | Reason / evidence + date | Electrical / mechanical / firmware impact; risk | Status / approval |
| --- | --- | --- | --- | --- | --- |
| CHG-001 | 0 / preservation | New snapshot/manifests/report | Explicit START request; inventory/hash verification, 2026-10-29 | No design impact; local provenance only | Proposed → Approved → Applied → Verified; Phase 0 accepted |
| CHG-002 | 1 prerequisites / documentation | Tools matrix, CLI and user decisions recorded | User prerequisite instruction; [tool matrix](../01_audit/EASYEDA_TOOLS.md), 2026-10-29 | No design impact; production operations untested | Proposed → Approved → Applied → Verified |
| CHG-003 | 1 / audit | Isolated audit copies/reports created | Phase 1 authorization; [native runs](../01_audit/phase1/NATIVE_RUNS.json), 2026-10-29 | No design modifications; stored fills/current libraries. F-008 wording corrected under CHG-005 | Proposed → Approved → Applied → Verified (execution, not clean design) |
| CHG-004 | 1 follow-up / baseline and provisional LED identity | Original 27-file baseline + pristine copy; all 145 D references: SK6812 → SKC6812RGBW-WS; schematic Datasheet, added Manufacturer/MPN/LCSC/AssemblyStatus, instance-cache Value | Explicit conditional approval, 2026-10-29; F-006/F-012; [official identity](https://www.lcsc.com/product-detail/C5378724.html), checked 2026-10-29; [field evidence](../01_audit/CHG-004/FIELD_CHANGES.json) | No net/geometry edits. Proposed physical part may change format/current/fit; firmware impact unresolved. HIGH until validated | Proposed → Approved-provisional (2026-10-29) → **Applied-provisional**; execution/diff verified, equivalence NOT Verified |
| CHG-005 | 2 / analysis/documentation | Audit-copy screening settings, checks/measurements/drawing review and report correction | Explicit Phase 2 instruction after clean diff; F-007–F-025; [audit evidence](../01_audit/phase2/PHASE2_AUDIT.md), 2026-10-29 | No baseline changes; only audit project settings changed. Current drawing retrieval limits disclosed | Proposed → Approved (user instruction, 2026-10-29) → Applied → Verified (analysis execution) |
| CHG-006 | 3 / analysis/documentation | New sourcing, equivalence, power/mechanical evidence, individual proposals and living report | Explicit Phase3 instruction after Phase2 acceptance; F-006–F-029; [Phase3 evidence](../01_audit/phase3/PHASE3_AUDIT.md),2026-10-29 | No design impact; qualification gaps remain. [Final integrity check](../01_audit/phase3/FINAL_VERIFICATION.json) | Proposed → Approved (user instruction,2026-10-29) → Applied → Verified (analysis execution only) |

No additional CAD edit was made in this update. BOM-05/09 identities are approved as recorded above. Audit verification does not waive violations. Historical proposal statuses below are superseded by the current-status table. CHG-020 records an already-approved fallback whose Phase5 gate has not yet been reached.

**CHG-004 hard gate:** status remains Applied-provisional until Phase 3 verifies the actual LED package drawing, pad geometry, pinout, supply/logic/timing and electrical suitability. Report pixel format and firmware impact without editing code. Calculate worst-case full-channel LED current per design and actual board multiplicities, against supply, trace/plane/via paths and exact connector ratings. Typical current is not a guaranteed maximum. If unsuitable, revise/reject CHG-004 and stop downstream reliance. The pristine copy supports a documented clean rollback.


### Proposed changes, each awaiting an individual decision

Common log fields: Phase3 proposal; evidence checked2026-10-29; status **Proposed**; approval date **—**; no application date. The exact before/after options, affected designators/files, F-ID reasons, source links, impacts and risk are recorded per row. Evidence-first entries cannot be applied merely by accepting the investigation. The full [decision document](../01_audit/phase3/CHANGE_PROPOSALS.md) includes mandatory zone copper-difference verification.

| Change / category | Affected files or parts; Before → proposed After | Reason / evidence | Options and recommendation | Impact / risk / readiness |
| --- | --- | --- | --- | --- |
| CHG-007 / zone setting | 11x3 PCB, In1.Cu GND zone `ebc1b9d1-5ab5-498d-8c7c-d1dbd7d2f21e`: priority 0 → 1, then refill | F-007; [zone boundaries](../01_audit/phase3/ZONE_BOUNDARIES.json), [Phase 2 DRC](../01_audit/phase3/../phase2/PHASE2_AUDIT.md) | A: priority change plus refill, recommended first. B: delete/merge overlapping zones, a separate geometry edit requiring a revised proposal. Refill alone does not remove the equal-priority overlap condition | Electrical: fill connectivity must be rechecked. Mechanical/firmware: none intended. MEDIUM. Concrete setting proposal; use verification below |
| CHG-008 / zone setting | 11x3 PCB, In2.Cu P zone `adf31dc2-64bf-4999-b7a4-ff94006b3351`: priority 0 → 1, then refill | F-007; [zone boundaries](../01_audit/phase3/ZONE_BOUNDARIES.json) | Same options as CHG-007; approve separately | Electrical: power-plane fill may change. Mechanical/firmware: none intended. MEDIUM. Concrete setting proposal |
| CHG-009 / resistance identity | 8x3 R1–R8 schematic `R330`, PCB `R` → explicit `330` ohms in both, if chosen; preserve footprint/nets | F-008; [all eight connections and calculations](../01_audit/phase3/EQUIVALENCE_AND_POWER.md) | A: 330 Ω, recommended from the equivalent 11x3 circuit. B: retain unresolved. 0.33 Ω is not supported by the base-drive calculation. Exact procurement under CHG-014 | Electrical: determines actual base resistance; F-027 remains. Mechanical/firmware: none. HIGH until value chosen; field-only edit becomes concrete with choice |
| CHG-010 / decoder identity | 8x3 UI1 generic 74HCT138 → exact qualified HCT138 package/MPN | F-017; [TI NS0016A drawing and options](../01_audit/phase3/EQUIVALENCE_AND_POWER.md), [TI PDF](https://www.ti.com/lit/ds/symlink/sn74hct138.pdf) | Prefer TI SN74HCT138NSR: recommended lands fit within existing copper, but JLC/LCSC supply is UNVERIFIED. If unavailable, SN74HCT138DR/C352958 requires a separately dimensioned footprint/copper proposal. Neither HC138 nor HCT238 is an automatic substitute | Electrical: preserve pinout/TTL thresholds/polarity. Mechanical: NSR nominal fit; DR changes lands. Firmware: none intended. HIGH. Evidence first; no package edit ready |
| CHG-011 / sensor package acceptance | All 145 U sensors, existing AH49E SOT-23 → verified AH49ENTR-G1/C314698 identity and accepted lands | F-016/F-021; [sensor parameters and land discrepancy](../01_audit/phase3/EQUIVALENCE_AND_POWER.md), [Diodes drawing](https://www.diodes.com/assets/Datasheets/AH49E.pdf) | Prefer retaining same sensor family and geometry if tolerance/joint evidence supports it. Otherwise submit exact pad changes for approval; do not silently refresh SOT-23 | Electrical: sensor rail/sensitivity and magnetic orientation matter. Mechanical: 2.9 vs 3.6 mm land span unresolved. Firmware/calibration: flag only. HIGH. Evidence first |
| CHG-012 / regulator tab model | 11x3/UI2, 8x3/UI2 copper tab pad4/no net → output model, after exact SOT-223 proof | F-018; [three tab options and exact C6186 datasheet](../01_audit/phase3/EQUIVALENCE_AND_POWER.md) | Recommend A: existing tab numbered2 and P3.3, no geometry changes. B: explicit symbol tab4 tied to output. C: documented exception only with package/thermal acceptance. Never assign arbitrary GND | Electrical: connectivity modelling changes, may reveal routing requirement. Mechanical: none for A. Firmware: none. HIGH. Manufacturer tab proof required before any implementation |
| CHG-013 / terminal identity | Two WAGO connectors, footprint name 2601-602 vs supplied 2061 document → verified 2061-602/998-404/C2765058 identity, if matched | F-019; [body, lands and current evidence](../01_audit/phase3/EQUIVALENCE_AND_POWER.md), [WAGO drawing](https://pimassetsprdst.blob.core.windows.net/assets/apc_Original/11/51/130811151.pdf) | Prefer exact identity documentation and local footprint alias after complete drawing comparison. Alternative: leave unresolved/hand-populate under CHG-016. Do not rename as a substitute for proving fit | Electrical: exact current/wire rating required. Mechanical: drawing/polarity acceptance. Firmware: none. HIGH. Evidence first |
| CHG-014 / procurement identities | BOM-05/09/12/15/16/17/20: C104, C106, known330Ω, HCT154,220Ω,1000µF,HC4052 → candidates in sourcing table; optional BOM-19 only after CHG-009 | F-021; [full sourcing/ratings](../01_audit/phase3/BOM_SOURCING.md), [side-by-side comparisons](../01_audit/phase3/EQUIVALENCE_AND_POWER.md) | Same functional parts first; Basic C24497/C13585 where suitable. Candidates are decisions individually by BOM-ID, not one blanket substitution. C106 on regulator output depends on CHG-027; HC4052 on CHG-026. C17930 class, HCT154 stock, terminal drawings and original ratings remain open | Electrical: unspecified ratings become defined; no value change authorized by nominal interpretation alone. Mechanical: no assumed generic-package fit. Firmware: none intended. HIGH. Evidence first; no blanket application |
| CHG-015 / transistor and buffer package acceptance | 19 Q SOT-23 instances and 11x3/UI3 → MMBT3906LT1G/C53444 and SN74LV1T34DBVR/C100024 with accepted retained lands | F-025/F-021; [two Q variants and buffer lands](../01_audit/phase3/EQUIVALENCE_AND_POWER.md) | Prefer same supplied part families without geometry changes if tolerances support them. Any pad correction must be a separate dimensioned amendment covering each variant | Electrical: original pin functions preserved; drive checks remain. Mechanical: overlap/assembly margin unverified. Firmware: none. HIGH. Evidence first |
| CHG-016 / assembly population | BOM-03/06/07/08/10, 87 generic connectors → excluded from JLC BOM/CPL and retained in hand-population list; optional 2 WAGO terminals separately | F-021/F-019; [coverage and assembly choices](../01_audit/phase3/BOM_SOURCING.md) | Recommend hand-population provisionally because exact mating/lands and automated assembly acceptance are unknown. Alternative: qualify each exact library part and retain SMT placement. Approve generic87 and WAGO2 separately | Electrical/function: all still required, no permanent removal. Mechanical/current fit still needs exact parts. Firmware: none. MEDIUM; population decision ready, part procurement remains blocked |
| CHG-017 / library portability | Four projects' missing/mismatched external library dependencies → project-local copies of the embedded symbols/footprints plus explicit tables | F-010/F-011; [Phase 2 evidence](../01_audit/phase3/../phase2/PHASE2_AUDIT.md) | Recommend preserving embedded definitions verbatim and referencing them locally; no refresh from installed libraries. Alternative: leave warnings documented until GUI import, with continued reproducibility risk | Electrical/mechanical/firmware: none intended; only library identifiers/tables and necessary cache references. MEDIUM. Before application provide exact file/identifier mapping and prove parsed pin/pad/net/geometry equality |
| CHG-018 / nominal thickness and acceptance | 8x3,3x8,8x8 source0.582 mm → documented nominal0.6 mm per user, with exact-size JLC acceptance | F-023; [conflicting official limits and mechanical evidence](../01_audit/phase3/PHASE3_AUDIT.md) | Retain nominal0.6 intent; obtain acceptance for listed dimensions/tolerance/warpage. Do not silently choose0.8 or edit stackup. If rejected, return a separate thickness/mechanical proposal | Electrical/mechanical: thickness can affect assembly and sensor height; firmware none. HIGH. Documentation intent already authorized, CAD change NOT approved; supplier acceptance unresolved |
| CHG-019 / assembly service/frame | Four two-sided designs, unresolved service/rails → confirmed Standard assembly arrangement preserving finished outline/holes | F-015; [official assembly limits](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), [dimensions](../01_audit/phase3/PHASE3_AUDIT.md) | Recommend Standard double-sided subject to confirmation. 66 mm widths need handling arrangement; 11x3 length260.7 exceeds stated250 mm panel limit. Request exact external rail/fiducial/fixture proposal for approval; no automatic panel creation | Electrical: none intended. Mechanical: external frame may be needed. Firmware:none. HIGH. Evidence first; no accepted frame geometry yet |
| CHG-020 / import verification | Approved baseline files → user GUI EasyEDA Pro import, then MCP fidelity audit | F-004; [approved fallback matrix](../01_audit/phase3/../EASYEDA_TOOLS.md) | Existing fallback approval retained. Execute only at Phase5 after gates clear; stop on losses, no object-by-object reconstruction | Electrical/mechanical/firmware: no intended change; import may lose data. HIGH until verified; no new approval needed for the already-authorized fallback itself, but Phase5 gate still applies |
| CHG-021 / production outputs | Missing released BOM/CPL/Gerber/drill → verified Phase6 outputs, with hand-list and mechanical exclusions | F-005/F-009; [20 source exclusion flags](../01_audit/phase3/MECHANICAL_REFERENCE_EXCLUSIONS.json) | Generate only after individual part approval/import verification. Match assembled references 1:1; exclude mechanical holes in both files. If duplicates leak into either output, F-009 becomes MAJOR and output is rejected | No design impact intended. HIGH release risk until checked. Future phase work, not early export authorization |
| CHG-022 / directional legend | Only any identified unreadable orientation cue → separately specified manufacturing-readable cue | F-020; [Phase 2 legend screening](../01_audit/phase3/../phase2/PHASE2_AUDIT.md) | First prove orientation from approved package/assembly drawing; if thin silk is the only cue, reclassify MAJOR and submit exact text/line edits. Otherwise retain MINOR. No wholesale silk cleanup | Mechanical/silk change only if specifically approved. Firmware:none. MEDIUM. Evidence first; no exact edit proposed yet |
| CHG-023 / CHG-004 disposition | All145 provisional RGBW identity fields → hold, or clean rollback of only CHG-004 fields | F-006/F-012/F-026; [LED drawing/current comparison](../01_audit/phase3/EQUIVALENCE_AND_POWER.md), [original diff](../01_audit/phase3/../CHG-004/ORIGINAL_TO_BASELINE.diff) | Recommend **do not accept as a verified drop-in**. A: keep provisional and blocked pending proof. B: approve exact rollback to pre-CHG004 identities, then separately qualify an RGB candidate. C: explicitly request a new RGBW layout/power/firmware scope; no such redesign performed. Rollback does not qualify the old generic LED | HIGH electrical/fit/firmware risk. A is current status. B is a concrete reversible identity-only action, not yet approved. C exceeds current scope |
| CHG-024 / LED power qualification | Unverified all-channel-full power claim → verified maximum-current and distribution budget | F-026/F-006; [per-design totals, traces/connectors and supply](../01_audit/phase3/EQUIVALENCE_AND_POWER.md) | Obtain actual LED maximum, supply, module population/wiring, connector ratings and allowable rise; validate actual paths. Recommend blocking RGBW full-array release: typical load already exceeds README supply. A larger supply, trace changes or brightness cap would need a separate explicit scope decision | Electrical/system change not authorized. Firmware limits not assumed. HIGH. Validation only; no design fix ready |
| CHG-025 / Hall-bank drive qualification | 11x3/8x3 decoder→R→PNP bank: unverified margin → documented driver/base-current and sensor-rail acceptance | F-027; [resistor/driver calculations](../01_audit/phase3/EQUIVALENCE_AND_POWER.md) | Verify actual scan load, decoder loaded VOL, transistor saturation and minimum AH49E VCC. Recommend retaining circuit unchanged pending proof. If it fails, return options for explicit design-scope approval; no resistor optimization now | Electrical margin risk; mechanical none; firmware timing may influence load but is not edited/assumed. HIGH. Evidence first |
| CHG-026 / mux logic qualification | 3x8/UI1 HC4052 on5V, nominal3.3V controls → guaranteed threshold/VOH margin | F-028; [HC4052 comparison](../01_audit/phase3/EQUIVALENCE_AND_POWER.md), [Nexperia data](https://assets.nexperia.com/documents/data-sheet/74HC_HCT4052.pdf) | Obtain actual driver rail/VOH and operating tolerances. Recommend hold selection until margin proven; an HCT swap is a different proposal, not automatic | Electrical logic/analog limits matter; firmware untouched. HIGH. Evidence first |
| CHG-027 / regulator stability/thermal qualification | 11x3/8x3 UI2 and output C106: unspecified capacitor/load → demonstrated capacitance/ESR/load/thermal suitability | F-029/F-021; [AMS evidence and candidate limits](../01_audit/phase3/EQUIVALENCE_AND_POWER.md) | Recommend qualifying the same regulator and existing nominal value first. Datasheet's22µF tantalum general guarantee does not establish this10µF MLCC case. Any changed capacitance, package or added component requires a separate amendment | Electrical stability/heat risk; no actual oscillation asserted. Mechanical/firmware none unless later proposed. HIGH. Evidence first |


## 5. BOM substitution table

These are candidates, not approved substitutions. Exact quantities, original values, footprints and **every designator** are in the [full worksheet](../01_audit/phase3/BOM_SOURCING.md); mandatory datasheet comparisons are in [equivalence analysis](../01_audit/phase3/EQUIVALENCE_AND_POWER.md). All official observations checked2026-10-29; indexed stock is not live assembly allocation. CHG-004 is the sole applied provisional identity update.

| Group / original | Candidate → LCSC | Reason / risk |
| --- | --- | --- |
| BOM-01: SK6812 (145 LEDs) | OPSCO SKC6812RGBW-WS → C5378724 | HIGH; CHG-004 remains provisional; [official evidence](https://jlcpcb.com/partdetail/SKC6812RGBW-WS/C5378724) |
| BOM-02: AH49E | Diodes AH49ENTR-G1 → C314698 | HIGH; exact same family, SOT-23 land acceptance open; [official evidence](https://jlcpcb.com/partdetail/DiodesIncorporated-AH49ENTRG1/C314698) |
| BOM-03: PinSocket_1x03_P2.54mm_Horizontal_SMD | No approved match; search lead Samtec SSM-103-SM-SH-LC-TR → C6302166 | HIGH; propose assembly-DNP / later hand-solder; [official evidence](https://jlcpcb.com/partdetail/Samtec-SSM_103_SM_SH_LCTR/C6302166) |
| BOM-04: 2N3906 | onsemi MMBT3906LT1G → C53444 | HIGH until package/joint review; matches supplied device family; [official evidence](https://jlcpcb.com/partdetail/onsemi-MMBT3906LT1G/C53444) |
| BOM-05: C104 | Samsung CL31B104KBCNNNC → C24497 | MEDIUM; proposed interpretation C104 = 100 nF; original ratings absent; [official evidence](https://jlcpcb.com/partdetail/CL31B104KBCNNNC/C24497) |
| BOM-06: PinSocket_2x22_P2.54mm_Vertical_SMD | No verified exact 2x22 vertical SMT socket → UNVERIFIED | HIGH; 44 pads per socket with adjacent pins paired electrically; hand fit required; [official evidence](https://www.lcsc.com/) |
| BOM-07: PinHeader_1x02_P2.54mm_Horizontal_SMD | No verified exact 1x02 horizontal SMT male header → UNVERIFIED | HIGH; propose assembly-DNP / later hand-solder; [official evidence](https://www.lcsc.com/) |
| BOM-08: PinHeader_1x03_P2.54mm_Horizontal_SMD | No verified exact 1x03 horizontal SMT male header → UNVERIFIED | HIGH; propose assembly-DNP / later hand-solder; [official evidence](https://www.lcsc.com/) |
| BOM-09: C106 | Samsung CL31A106KBHNNNE → C13585 | HIGH on regulator outputs: effective capacitance/stability not established; [official evidence](https://jlcpcb.com/partdetail/14236-CL31A106KBHNNNE/C13585) |
| BOM-10: PinSocket_1x02_P2.54mm_Horizontal_SMD | No approved match; search lead Samtec SSM-102-T-SH-TR → C6685390 | HIGH; propose assembly-DNP / later hand-solder; [official evidence](https://jlcpcb.com/partdetail/Samtec-SSM_102_T_SHTR/C6685390) |
| BOM-11: Power_Terminal/Power_RaspberryPi | WAGO 2061-602/998-404 → C2765058 | HIGH; footprint name says 2601; propose hand-solder if no accepted supply; [official evidence](https://jlcpcb.com/partdetail/WAGO-2061_602_998404/C2765058) |
| BOM-12: 330 | UNI-ROYAL 1206W4F3300T5E → C17930 | MEDIUM for component, HIGH for driver-load validation; [official evidence](https://www.lcsc.com/product-detail/C17930.html?is_substitute=1&original_product_code=C965000&original_unit_price=0.0072) |
| BOM-13: SN74LV1T34 | TI SN74LV1T34DBVR → C100024 | HIGH pending package overlap; same functional part; [official evidence](https://jlcpcb.com/partdetail/SN74LV1T34DBVR/C100024) |
| BOM-14: AMS1117-3.3 | Advanced Monolithic Systems AMS1117-3.3 → C6186 | HIGH; tab evidence/stability/thermal checks open; [official evidence](https://jlcpcb.com/partdetail/AMS1117-3.3/C6186) |
| BOM-15: 74HCT154D | TI CD74HCT154M96 (alternative to generic 74HCT154D) → C2653299 | HIGH; sourcing and base-current load open; do not replace with HC; [official evidence](https://jlcpcb.com/partdetail/TexasInstruments-CD74HCT154M96/C2653299) |
| BOM-16: 220 | UNI-ROYAL 1206W4F2200T5E → C17957 | MEDIUM; original tolerance/power absent; [official evidence](https://jlcpcb.com/partdetail/18645-1206W4F2200T5E/C17957) |
| BOM-17: 1000 µF | jieerrui RVT16V1000M10X10 → C51953415 | HIGH; ripple/ESR/terminal/polarity acceptance open; [official evidence](https://jlcpcb.com/partdetail/jieerrui-RVT16V1000M10X10/C51953415) |
| BOM-18: 74HCT138 | Preferred geometry candidate TI SN74HCT138NSR; narrow alternative SN74HCT138DR → UNVERIFIED for NSR; C352958 for DR | HIGH; no available verified drop-in released; [official evidence](https://www.lcsc.com/product-detail/C352958.html) |
| BOM-19:330 | Value330Ω approved/applied; procurement C17930 proposed | Extended verified2026-10-30; stock/price confirmation and BOM-ID approval pending; [official evidence](https://www.lcsc.com/product-detail/C17930.html?is_substitute=1&original_product_code=C965000&original_unit_price=0.0072) |
| BOM-20: 74hc4052D | Nexperia 74HC4052D,653 → C11350 | HIGH pending 3.3V-control/5V-supply logic margin; no HCT substitution applied; [official evidence](https://jlcpcb.com/partdetail/74HC4052D%2C653/C11350) |

Current totals:582 electronic instances across one of each tile;89 hand components are covered by applied CHG-016 export policy, leaving493 SMT candidates. Conditional complete board:1313/170/1143 respectively.20 source groups become19 procurement groups if330Ω groups share one SKU (13 SMT+6 hand). Final exact MPN count remains unverified. Candidate family Extended count7 excludingLED/8 includingoneLED, conditional on330Ω selection and unresolveddecoder class; fees recur per separate design job. [Current totals/fees](../01_audit/prototype_8x3/SIZE_ORDER_PLAN.md). Historical candidate ratings above are retained as provenance; parked qualifications are not release gates. BOM-05/09 are approved for8x3 only; CAD/ordering assignments pending.

## 6. Parked items

- CHG-010: decoder procurement may be unavailable; verify exact library SKU/placement and test bank selection on prototype; no further original-package qualification.
- CHG-011: sensor assembly/response risk; inspect solder joints and test all sensor positions.
- CHG-012: tab model uncertainty; prototype-check regulator output/tab continuity and operation.
- CHG-013: terminal naming risk; hand-fit the selected terminal and check polarity/connection retention.
- CHG-015: transistor/buffer joint risk; inspect joints and test switching/LED data.
- CHG-017: external library portability risk; check imported parts against retained geometry.
- CHG-019: handling/rail acceptance risk; inspect JLC workflow feedback and prototype flatness; no frame designed.
- CHG-022: orientation marking risk; check directional parts in placement preview and on arrival.
- CHG-024: high-brightness load risk; measure prototype current/voltage drop/temperature under intended operation.
- CHG-025: Hall switching margin risk; measure switched sensor supply and verify scanning on prototype.
- CHG-026: mux control margin risk; verify all mux channels on prototype.
- CHG-027: regulator stability/heat risk; observe startup, load steps and temperature on prototype.
- Historical electrical revision/minimum KiCad opener: provenance limits; compare required geometry at export, use tested10.0.7.


No further paper qualification analysis is authorized for these advisories. Historical Gerbers remain reference-only; no ordering/upload/frame/firmware changes.

## 7. Open questions / decision stop

1. Approve/reject **CHG-004 all-four rollback + CHG-023 RGB C5378720 candidate** on [Decision02](../01_audit/prototype_8x3/DECISION_02_LEDS.md). Nominal drawing fit passes all four; current RGB timing differs from historical document. No LED assignment yet.
2. Approve/reject **BOM-19 C17930** for8x3, conditional on live assembly stock/price confirmation. MCP verifies Extended; resistance330Ω is already approved and applied. BOM-05/09 approvals are recorded and are not requested again.
3. Provide the repository path/URL with the author's exact tile quantities/order settings. User's provisional1/1/2/4 confirmation is recorded; [223-file search](../01_audit/prototype_8x3/ORDER_INSTRUCTIONS_SEARCH.md) did not locate the passage.

Stop at the LED decision sheet before import preparation. Remaining UNVERIFIED release inputs:live stock counts for approved capacitors and candidates, exact decoder supply, thin-board/handling acceptance, author settings/finish, complete quote, import/DFM/placement and production exports. These are listed without reopening parked design qualification.

## 8. Verification results

**Current8x3 result:** CHG-009 parsed-tree reversal verifies only Value fields changed; all other baseline files and117 originals/snapshot hashes unchanged. Native KiCad10.0.7 on audit copies: ERC0 errors/230 warnings; DRC0 errors/114 warnings;0 unconnected; parity134→126 (eight resistor mismatches removed). No refill/save/upgrade. Exact report files are under01_audit/CHG-009/. CHG-016 policy covers89 distinct design/reference pairs,19 on8x3. Future output verification remains outstanding.

The following Phase0–3 results are historical snapshots before CHG-009; their baseline hash assertions must not be rerun as if the baseline were unchanged after an approved edit.

Phase 0 preserved source hashes and checked archives. Phase 1 compared both families, with eight ERC, eight DRC/parity and eight native netlist runs. Approved follow-up built baseline/backup and proved only the permitted fields changed. All 145 original LEDs are covered.

Phase 2 completed four baseline ERC, four baseline DRC/parity, four native netlists and four additional screening DRC runs, direct metadata/geometry measurements and selected datasheet drawing review. No save, upgrade or zone refill. KiCad generated local preferences only inside audit copies; design inputs stayed unchanged. [Native commands/guards](../01_audit/phase2/NATIVE_RUNS.json), [measurements](../01_audit/phase2/MEASUREMENTS.json), [final verification](../01_audit/phase2/FINAL_VERIFICATION.json).

| Design | ERC errors/warnings | Baseline DRC errors/warnings | Unconnected | Parity warnings | Additional JLC screen warnings |
| --- | --- | --- | ---: | ---: | ---: |
| 11x3 | 0/273 | 2/164 | 0 | 184 | 22 legend |
| 8x3 | 0/230 | 0/114 | 0 | 134 | 0 |
| 3x8 | 0/166 | 0/89 | 0 | 101 | 0 |
| 8x8 | 0/399 | 0/214 | 0 | 272 | 0 |

Native net names and pin memberships remain identical to the originals. Source checks report no additional copper/drill/outline-clearance problem in the geometry examined. This does not certify future fills, current capacity, exact-part solderability or manufacturer DFM.

Phase3 verified582 unique design/reference instances across20 groups, all20 mechanical BOM/CPL exclusion flags,145/145 LED identity coverage, native resistor/power connections, current arithmetic and read-only mechanical evidence. Actual current LED/decoder package pages were visually inspected where available. Baseline/snapshot/original/backup/mechanical hashes remain unchanged; see [Phase3 final verification](../01_audit/phase3/FINAL_VERIFICATION.json). No new native ERC/DRC runs were needed because no design input changed. These are analysis/integrity checks, not electrical qualification or manufacturer acceptance.

Phase 6 checklist **NOT RUN**: new layers/outline/drill units; BOM↔CPL 1:1 references; verified LCSC assignment for every assembled part; bottom-side coordinates/rotation; every directional part/pin-1 review; import/pad/copper fidelity and refill; historical outline/drill/copper regression; current output formats; final ZIP/release. `03_output/` is empty.

## 9. Known risks and assumptions

Original circuit/footprints accepted by user; their old qualification warnings are non-blocking prototype advisories. JLC part availability, actual assembly preview/DFM and import/export correctness still need checks. No Basic330Ω1206 match was verified; exact Extended total remains open. LED decision is pending and no LED has been assigned to an ordering BOM. Full-board quantities are provisionally confirmed by the user; exact author instructions were not located in the223-file search, with native CAD/OCR limitations disclosed. Original system qualification was intentionally not extended.

Needs from you: LED rollback/candidate decision, BOM-19 decision, and author ordering-instruction location.
