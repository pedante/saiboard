# Phase 3 sourcing and qualification review

Checked **2026-10-29**. Scope:11x3,8x3,3x8,8x8, one of each for counts. **Analysis package complete; component qualification and manufacturing release are NOT complete. Stop at the Phase3 gate.** No design fixes, sourcing assignments, refills, new fabrication exports or DNP flags were applied. CHG-004 stays **Applied-provisional** and cannot support downstream production until revised or qualified.

## Results and review documents

The [full sourcing worksheet](BOM_SOURCING.md) accounts for every one of **582 electronic instances in20 procurement groups**. It includes exact designators, original values/footprints, candidate MPNs/LCSC IDs, status, class, dated stock/price observations, links and unresolved fit. These are procurement groups, not20 qualified unique MPNs. Fourteen core candidate LCSC IDs include **8 verified Extended,3 Basic,3 classification-unverified**; two socket search leads are additional and unqualified. No Preferred classification was verified. Every group retains at least one unresolved qualification or availability item; final unique-MPN/Extended counts are not fixed. Fee evidence is in that worksheet.

[Equivalence and power analysis](EQUIVALENCE_AND_POWER.md) contains mandatory parameter comparisons, actual LED and decoder package drawings, each design's full-channel budget, R1–R8 connectivity/calculations and regulator-tab alternatives. [Individual change proposals](CHANGE_PROPOSALS.md) cover every BLOCKER/MAJOR. Their “evidence first” entries are not ready-to-apply repairs. This package does not claim available, compatible replacements where evidence is missing.

The LED pinout agrees, but retained lands differ from the candidate recommendation; assembly tolerance/joint acceptance is unresolved. The candidate is32-bit GRBW, versus24-bit GRB in the supplied original document. Its datasheet omits maximum channel current. Typical full-channel budgeting gives1.346A/0.979A/0.979A/2.611A for11x3/8x3/3x8/8x8, respectively. A documented19×19 population gives14.725A before other loads, exceeding the README's5V10A supply. Neither that typical estimate nor a generic trace calculator meets the user's guaranteed worst-case suitability condition. No brightness cap or firmware change is assumed.

For8x3 R1–R8, tracing identifies PNP Hall-bank base resistors. The equivalent11x3 resistors explicitly say330. **330Ω is recommended for the user's choice; it is not assigned.** The user's response is still a placeholder. Historical silk does not independently establish the value. Driver loading remains a separate concern even with330Ω.

TI SN74HCT138NSR is a promising same-footprint decoder candidate based on the actual NS0016A drawing; JLC/LCSC sourcing is not verified. Available-listing narrow alternatives require a footprint/copper proposal. For the regulator, retain same-part C6186 priority, but obtain explicit SOT-223 tab evidence before any pad/net correction. No unchecked tab assumption was applied.

## Thickness, mechanical dependencies and assembly limits

The user's instruction establishes nominal **0.6mm intent** for the three0.582mm projects. Source stackups are unchanged. Native dimensions and reference drill counts are:

| Design | Source layers | Source / nominal thickness | Outline mm | Historical drill hits |
| --- | ---: | --- | --- | ---: |
| 11x3 | 4 | 1.6 /1.6mm | 66×260.7 | 302 |
| 8x3 | 2 | 0.582 /0.6mm | 66×189.6 | 151 |
| 3x8 | 2 | 0.582 /0.6mm | 176×71.1 | 172 |
| 8x8 | 2 | 0.582 /0.6mm | 176×189.6 | 358 |

**Official size/tolerance guidance conflicts; F-023 is now BLOCKER for manufacturing acceptance.** [JLC fabrication capabilities](https://jlcpcb.com/capabilities/pcb-capabilities) offers0.6mm and specifies ±0.1mm for thickness below1mm. Its thin-FR4 maximum is599×497mm, also stated by [PCB dimensions, updated2026-09-09](https://jlcpcb.com/help/article/pcb-dimensions). However, the [official quote page's publicly readable help](https://cart.jlcpcb.com/quote/?fromDemo=yes) says0.6mm maximum100×100mm and gives a generic±10% tolerance; it excludes0.6mm for1/4/6layers and excludes leaded HASL for2-layer0.6mm. All three thin designs exceed100mm in at least one dimension. The two-layer option exists, but these exact designs' acceptance is **UNVERIFIED**. No settings were submitted or files uploaded. Do not silently choose0.8mm, a finish, or the more permissive limit. Obtain a definitive exact-size/finish/tolerance response through a user-authorized channel.

[JLC assembly capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), checked the same date, lists Economic thickness0.8–1.6mm and single-side placement. Standard supports both sides and reports no thickness limit, but single boards start at70×70mm, max460×500mm; panels max250×250mm, with rails/fiducials required. Thus Standard supports thin two-sided assembly in principle, not automatic acceptance of these boards. The66mm-wide boards need a confirmed handling arrangement;11x3's260.7mm length also exceeds that panel limit. No frame or finished-outline edit is approved.

[JLC's warpage article](https://jlcpcb.com/blog/prevent-pcb-warping), dated2026-04-09, gives a general0.75% SMT limit and0.5% as a special requirement, but does not guarantee these thin-board dimensions. Exact flatness acceptance, supporting fixture and reflow handling remain UNVERIFIED. The nominal0.018mm difference between0.582 and0.600 is smaller than the capabilities page's±0.1mm thickness tolerance; that observation does not establish mechanical clearance.

Read-only inspection covered22 mechanical/reference files; hashes and observations are in [MECHANICAL_READONLY.json](MECHANICAL_READONLY.json). Local evidence:

- `board/README.md`: top plywood6.5mm, sides10mm, bottom5mm; the stated0.6mm material is **veneer**, not a PCB specification. Resin/finish thickness is unspecified.
- `electronics/README.md`: printed mask, copper foil and double-sided tape on PCB front; no complete assembly Z-stack or mounting datum.
- Four PCB-mask G-code files have printing Z up to2.08mm, starting0.26mm; Raspberry Pi mount up to5.98mm. Printed layer height is not proof of recess depth or sensor spacing.
- DXF header units are millimetres; bottom has1 closed-polyline entity, grid38lines+1circle, side4polylines+1circle+2lines, top361circles+2polylines. They are planar, with no machining depths establishing a PCB-thickness dependency.
- Native Fusion F3D archive members/metadata were read, but binary solid dimensions/constraints were not semantically decoded. **Recess depth, PCB mounting datum and sensor-to-surface distance remain UNVERIFIED.** Absence of a readable parameter is not proof of independence. A read-only CAD section/dimension inspection is still needed; no new software was installed.

If mounting references the PCB rear face, thickness changes can move sensor height; if the front face is the datum, the rear clearance changes instead. Neither datum is established here. No mechanical or electronics source file was edited.

## Findings added or refined

| ID | Severity | Evidence / implication | Proposed disposition |
| --- | --- | --- | --- |
| F-006 | BLOCKER, retained | Candidate land pattern differs; guaranteed max current/electrical suitability unavailable | CHG-023/024; keep provisional and block downstream reliance |
| F-009 | MINOR, conditional | All20 mechanical footprints already have exclude_from_bom and exclude_from_pos_files; [actual flags](MECHANICAL_REFERENCE_EXCLUSIONS.json) | Preserve flags. If either export includes repeated mechanical references, immediately MAJOR and reject output, CHG-021 |
| F-017 | BLOCKER, refined | Wide NSR package geometry candidate found, JLC availability not established | CHG-010, same-footprint sourcing first |
| F-023 | BLOCKER for acceptance, raised from MAJOR | Nominal0.6 intent resolved; official100×100 vs599×497 size and tolerance statements conflict; mechanical Z dependencies not fully decoded | CHG-018, manufacturer confirmation; no stackup edit |
| F-026 | BLOCKER for full-channel RGBW release | Full361-pixel typical current alone exceeds documented10A; guaranteed maxima and distribution limits missing | CHG-024; actual power evidence or separately authorized scope decision |
| F-027 | MAJOR |330Ω illustrative base load exceeds HCT138's4mA guaranteed output condition; sensor switched-rail margin unknown | CHG-025; loaded circuit validation, no optimization |
| F-028 | MAJOR | HC4052 pin16 is5V P; nominal3.3V controls do not establish guaranteed VIH/VOH margin | CHG-026; verify actual driver and tolerances |
| F-029 | MAJOR | Selected10µF MLCC effective capacitance/ESR is not established by AMS's general22µF tantalum stability guarantee | CHG-027; qualify without assuming oscillation or changing capacitance |

Other Phase2 findings retain their accepted classifications. F-020 becomes MAJOR only if the affected legend is necessary for unambiguous orientation and no valid assembly cue exists. Library warnings remain MAJOR for portability, not automatic copper violations. Two native11x3 zone errors remain; [CHG-007/008](CHANGE_PROPOSALS.md) distinguishes settings/refill from geometry edits and specifies before/after copper verification and historical regression.

## UNVERIFIED register

**30 tracked unresolved items**, with scope shown below. This is a count of evidence gaps, not a count of defective components. All20 procurement groups retain at least one such gap. Historical provenance and exact minimum KiCad opener do not independently block the present analysis.

| ID | Still unverified | What closes it / affected decision |
| --- | --- | --- |
| U-001 | Live assembly allocation, quantity/spares and current prices for all selected parts; cached/LCSC counts are not reservations | Current JLC acceptance for actual order quantities; no purchase authorized |
| U-002 | Final MPN set, Extended count; C17930/C2653299/C352958 class; socket leads; Preferred eligibility | Exact approved BOM and current official classifications |
| U-003 | Exact RGBW WS bin/orderable suffix and original fitted LED manufacturer/suffix | Lot/package ordering data; old purchase records optional, alternative qualification still possible |
| U-004 | LED tolerance/placement/joint acceptance on retained pads | Exact drawing/tolerance overlap and assembly acceptance; CHG-023 |
| U-005 | Guaranteed full-channel LED current over supply/temperature, not typical values | Manufacturer maximum data or an explicitly accepted qualification specification; CHG-024 |
| U-006 | Actual supply rating/transient capability, PCB multiplicities and power distribution | User's physical configuration plus verified ratings; CHG-024 |
| U-007 | Trace/plane/via path current, voltage drop and acceptable temperature rise | Actual distribution and thermal verification; generic tool estimates are insufficient |
| U-008 | Header/wire/terminal current derating in actual assembly | Exact connector/contact/conductor/ambient evidence; CHG-013/016/024 |
| U-009 | RGBW timing/format compatibility with existing firmware | Firmware impact review by user/authorized software scope; no code edited or inspected here |
| U-010 | Candidate LED MSL5a vs listingMSL3, supply-minimum discrepancy and lot reflow handling | Exact manufacturer/JLC reconciliation before assembly |
| U-011 | Loaded level-translator output to LED VIH margin | Exact guaranteed VOH/load/supply analysis; CHG-015/024 |
| U-012 |8x3 R1–R8 intended resistance | User choice; recommend330Ω, CHG-009 |
| U-013 | Decoder NSR JLC availability; narrow-alternative exact assembly/class; HCT154 supply | Current exact-SKU supply plus footprint acceptance; CHG-010/014 |
| U-014 | Exact C6186 SOT-223 tab/output association | Unambiguous manufacturer package evidence; CHG-012 |
| U-015 | Regulator effective output capacitance/ESR/load stability and thermal margin | Exact part data and load/transient/thermal evidence; CHG-027 |
| U-016 | AH49E, both Q land variants and buffer joint/tolerance acceptance | Package drawings against actual lands; CHG-011/015 |
| U-017 | Switched Hall supply minimum,3.3V sensitivity/current, magnetic direction and PNP/decoder margin | Exact operating conditions/qualification; CHG-011/025 |
| U-018 | Generic connector exact mating/body/land/reflow specs, especially J30/J31 paired44-pad sockets | Exact drawings and mating parts; CHG-016 |
| U-019 | WAGO2601 label versus2061 actual fit, orientation and supplier stock | Complete exact-SKU drawing match and supply; CHG-013 |
| U-020 | Original passive ratings and candidate terminal dimensions; C104/C106 intended specs | User specification plus exact data; CHG-014 |
| U-021 | CP1 terminal geometry, polarity, ripple/ESR adequacy | Actual manufacturer datasheet/drawing and load requirement; CHG-014 |
| U-022 | HC4052 guaranteed control margin at actual supplies | Driver VOH/rail tolerance and mux VIH; CHG-026 |
| U-023 | Portable library resolution without symbol/pad/net changes | Local-library mapping and equality checks; CHG-017 |
| U-024 | EasyEDA import fidelity/DRC, exact LCSC assignment and export fallback behavior | User-assisted Phase5 import and MCP verification; CHG-020 |
| U-025 | Phase6 outputs: 1:1 BOM/CPL, exclusions, bottom rotations/pin1, new copper/drills/outline/ZIP | Approved export and complete production checklist; CHG-021/022 |
| U-026 | Standard double-sided service, rails/fiducials/fixture and narrow/long-board handling | Exact accepted arrangement; CHG-019 |
| U-027 |0.6mm exact-size acceptance, tolerance, finish and thin-board flatness | Reconcile conflicting official limits; CHG-018 |
| U-028 | Mechanical recess/PCB datum/sensor-to-surface stack dependencies hidden in F3D | Read-only dimensioned CAD section; CHG-018 |
| U-029 | Historical Gerber electrical revision | Remains reference-only; compare geometry at Phase6 without forcing electrical equivalence |
| U-030 | Exact earliest KiCad version opening complete projects | Not needed with tested installed10.0.7; format-era statement retained |

## Execution and preservation

Source parsing and read-only official web/MCP evidence were used. EasyEDA's catalog verification tool required a cache-write confirmation; it was not enabled. The approved manual sourcing fallback was used. Several PDF downloads returned403, leaving exact drawings unverified; successful current TI HCT138 PDF and inspected page images are saved here. Linked viewer entries do not prove a successful PDF download or content hash match.

Phase2 native ERC/DRC results remain applicable to the unchanged baseline; no repeat was needed. No KiCad upgrade/save/refill command, installation, manufacturer message, ordering action or firmware edit occurred. The [final integrity check](FINAL_VERIFICATION.json) verifies original/snapshot/backup/baseline/mechanical hashes, complete sourcing coverage and empty production output. CHG-006 logs analysis artifacts only. Historical files remain reference-only for the later outline/drill-position/copper regression.

Needs from you: review this Phase3 package, choose R1–R8 resistance and CHG-004 disposition, and decide individual CHG proposals. Further evidence is needed for the listed qualification gates; Phase4 has not started.
