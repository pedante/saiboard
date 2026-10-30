# Phase 2 discrepancy audit

Checked **2026-10-29**. Analysis complete; **not released for fabrication or assembly**. No Phase 2 design fixes applied.

## Approved baseline and preservation

The original four-project family is now in `02_work/baseline/`. `02_work/baseline_before_CHG004/` preserves the 27 selected original files, byte for byte, with read-only permissions. The original electronics tree and the 117-file snapshot remain unchanged.

**CHG-004 is Applied-provisional**, approved 2026-10-29. It changes LED identity fields only: schematic/PCB Value, schematic Datasheet, added Manufacturer/MPN/LCSC/AssemblyStatus properties, and schematic instance-cache Value. It retains original embedded symbols, library IDs, footprint names, pad geometry, nets, tracks, zones, placements, outline, holes, layers and stackup. No candidate library or symbol retargeting was imported.

[Exact diff](../CHG-004/ORIGINAL_TO_BASELINE.diff), [field changes](../CHG-004/FIELD_CHANGES.json), and [verification with file hashes](../CHG-004/VERIFICATION.json) prove the permitted scope. Reversing the allowed fields restores the complete parsed original trees; the other 19 baseline files are byte-identical. Native schematic net names and pin memberships also equal the originals after the change.

| Design | Original LEDs | Updated | Coverage |
| --- | ---: | ---: | --- |
| 11x3 | 33 | 33 | D1–D33 |
| 8x3 | 24 | 24 | D1–D24 |
| 3x8 | 24 | 24 | D1–D24 |
| 8x8 | 64 | 64 | D1–D64 |
| Total | **145** | **145** | **None uncovered** |

These are counts across one of each design, not a bill of quantities for a complete Go board. No original purchasing or revision record was supplied. That is not a blocker to this audit. Historical Gerber electrical revision remains **UNVERIFIED**. In Phase 6 use the historical files only to compare outline, drill count/positions and copper geometry with new exports; never reuse them as production output.

## Method and limits

KiCad Flatpak **10.0.7** ran four ERC checks, four DRC/parity checks, four schematic netlist exports, then four additional DRC screens. All inputs were isolated audit copies. There was no save, upgrade, refill, production export or EasyEDA import. KiCad generated `.kicad_prl` preferences only inside audit copies. An initial hash guard correctly noticed these new files; inspection confirmed no design input changed. [Commands, settings and hash guards](NATIVE_RUNS.json).

The additional screen changes only audit-copy `.kicad_pro` settings: legend height 1.0 mm, legend stroke/clearance 0.15 mm, mask bridge 0.13 mm and mask-to-copper clearance 0.09 mm. Original, stricter copper/hole constraints remain in place. These are analysis settings, not changes to the baseline. Both runs examine **stored** zone fills. They cannot certify a future refill or import. A completed check is not a clean-design declaration.

[Measurements](MEASUREMENTS.json) include source coordinates, direct field discrepancies, hole spacing, copper extents, legend details and native counts. [Footprint variants](FOOTPRINT_VARIANTS.json) retain per-value/per-pad variants, including differently sized pads under the same library name. [Footprint gallery](FOOTPRINT_GALLERY.svg) supports visual pin-marker review; it shows source-local coordinates and is not a placement/rotation file. Curved board outlines and nonorthogonal pads are rejected by the measurement helper; these sources use rectangular outlines and orthogonal pads. Pad-gap measurements use conservative bounding boxes for rounded rectangles. Copper edge distance includes stored-fill bounds, not a new fill.

## Current manufacturer constraints

All URLs below checked **2026-10-29**. Values apply to the stated process, not every JLCPCB option. No order options were selected.

| Process feature | Official limit used |
| --- | --- |
| Copper, 1 oz | Track/space: two-layer 0.10/0.10 mm; multilayer 0.09/0.09 mm |
| Drills/vias | Drill 0.15–6.3 mm; via hole/diameter 0.15/0.25 mm; NPTH ≥0.50 mm |
| Annular rings | PTH absolute minimum: two-layer 0.18 mm, multilayer 0.15 mm; via diameter ≥hole+0.10 mm |
| Hole separation | Via holes 0.20 mm; pad holes 0.45 mm |
| Other copper clearances | SMD different-net pads 0.15 mm; inner via-hole/copper 0.20 mm, PTH-hole/copper 0.30 mm |
| Routed edge | Copper ≥0.20 mm |
| Mask, 1 oz | Bridge 0.10 mm colored, 0.13 mm black/white; opening-to-neighboring-trace 0.09 mm |
| Legend | Stroke 0.15 mm; height 1.0 mm; pad clearance 0.15 mm |
| FR4 | 1–32 layers; listed nominal thickness includes 0.4/0.6/0.8/1.0/1.2/1.6/2.0 mm |

Source: [JLCPCB PCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities). The manufacturer also lists two-layer PTH recommended ring 0.25 mm, multilayer 0.20 mm; do not confuse these with the via criterion. The source's 0.50 mm NPTH limit covers the 3 mm mounting holes.

All four fit the applicable fabrication dimension envelopes in [JLCPCB PCB dimensions](https://jlcpcb.com/help/article/pcb-dimensions). For thin FR4 the published maximum is 599×497 mm; 11x3 also fits the listed four-layer envelope. This does not establish an acceptable assembly panel.

[JLCPCB assembly capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities) lists Economic as single-sided, 0.8–1.6 mm; Standard permits double-sided assembly and lists no thickness limit, but requires rails/fiducials and at least 70×70 mm single boards. Standard single-board maximum is 460×500 mm; its listed panel maximum is 250×250 mm. The 11x3 length exceeds that panel figure. Manufacturer confirmation is needed for any frame/service arrangement; none was designed or uploaded.

The [ordering guide](https://jlcpcb.com/help/article/instructions-for-ordering) describes mask openings taking priority over legend. The [legend article](https://jlcpcb.com/blog/pcb-silkscreen) distinguishes 0.8 mm absolute text height from a 1.0 mm recommendation, whereas the capabilities table says 1.0 mm minimum. We used the stricter table for screening and report the discrepancy; 0.8 mm text alone is not claimed to force order rejection.

## Board and geometry results

| Design | Outline mm | Cu layers | Source thickness mm | Front/back nonmechanical footprints | Drills incl. vias | Min copper-to-outline mm | Min hole-edge gap mm |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: |
| 11x3 | 66×260.7 | 4 | 1.6 | 99 / 66 | 302 | 0.5085 | 0.8143 |
| 8x3 | 66×189.6 | 2 | 0.582 | 72 / 42 | 151 | 0.8000 | 1.5181 |
| 3x8 | 176×71.1 | 2 | 0.582 | 72 / 17 | 172 | 1.9800 | 0.8310 |
| 8x8 | 176×189.6 | 2 | 0.582 | 192 / 22 | 358 | 2.2000 | 0.8167 |

Each outline is one closed `gr_rect` on Edge.Cuts. All have front/back mask, paste, legend and Fab layers declared; 11x3 has both inner copper layers. Fab graphics are present for electrical footprints except custom J32/J33 on 11x3, which have Fab text but no body drawing. Mechanical holes have Fab text only. Export presence still requires Phase 6 verification.

Minimum track width is **0.5 mm** on every design. Ordinary vias are **0.8/0.4 mm**, giving **0.2 mm** annular copper. 11x3 also has two 5/2.5 mm and two 4/2 mm vias. Mounting holes are 3 mm NPTH; there are no component PTH pads or slots. These measured features exceed the applicable stated minima. A 0.25 mm *PTH pad* recommendation is not a reason to enlarge the 0.2 mm via rings.

The source DRC uses copper clearance 0.2 mm, copper edge 0.25 mm, hole clearance 0.35 mm and hole-to-hole 0.5 mm. It reported no violations of those checks. This supports fabrication clearance screening; it is not an exact minimum of every trace pair or an analysis of same-net narrow gaps. Minimum different-net SMD pad bounding-box gaps are 0.3500/0.5315/0.6700/1.0484 mm respectively. The smallest SMD pad dimensions are 0.55/0.60/0.60/0.80 mm respectively.

Global pad mask expansion is 0.05 mm per edge. Native screening reports no solder-mask bridge, mask/copper or silk-over-copper violations. Source-only pad-gap bounds, less two expansions, remain above the screened bridge threshold. Via plotting is configured `viasonmask false`; this is not proof of a JLCPCB via-filling process. No such process is selected. Exported mask openings still need verification after EasyEDA import.

The two-layer stackups sum to 0.582 mm (0.492 dielectric + 2×0.035 copper + 2×0.010 mask), while 11x3 totals 1.600 mm. Do not silently convert 0.582 to an order for nominal 0.6, increase it to 0.8, or change dielectric thickness. The intended finished thickness and JLCPCB stackup acceptance are unresolved.

## Native checks and warning classification

| Design | ERC errors/warnings | Baseline DRC errors/warnings | Unconnected | Parity warnings | Additional legend warnings |
| --- | --- | --- | ---: | ---: | ---: |
| 11x3 | 0 / 273 | 2 / 164 | 0 | 184 | 22 |
| 8x3 | 0 / 230 | 0 / 114 | 0 | 134 | 0 |
| 3x8 | 0 / 166 | 0 / 89 | 0 | 101 | 0 |
| 8x8 | 0 / 399 | 0 / 214 | 0 | 272 | 0 |

Native warning counts match Phase 1. All new baseline netlists have the exact original native net names and memberships. Earlier source-to-native PCB alias comparisons remain applicable because all PCB net fields are unchanged. There are no missing schematic nonpower/on-board components or unassigned schematic footprints. PCB-only objects are mounting holes. Zero reported unconnected items does **not** cover pads with no net assignment (see F-018).

Severity here means production-preparation impact: BLOCKER prevents release, MAJOR needs resolution or explicit evidence-based disposition, MINOR is limited manufacturing/readability impact, INFO is provenance or a checked observation. Native severity is preserved in the raw reports.

| Finding | Classification and evidence | Proposed resolution, not applied |
| --- | --- | --- |
| F-007 | **BLOCKER.** Two equal-priority intersections on 11x3: GND/In1.Cu zones `47f45fd7-05d8-4264-b78d-4a4cce2ee78b` and `ebc1b9d1-5ab5-498d-8c7c-d1dbd7d2f21e`; P/In2.Cu zones `2f5d64fb-0afd-415d-874d-0afc87e27243` and `adf31dc2-64bf-4999-b7a4-ff94006b3351`, all priority 0. Same-net overlap is not itself a JLCPCB trace-spacing breach, but unresolved zone semantics prevent a verified refill/export baseline. | Propose a separate, narrow zone-priority correction for approval, then refill an isolated copy and compare copper/connectivity before accepting it. No priority, polygon or copper changed. |
| F-008 | **BLOCKER for assembly BOM.** Correction to Phase 1 wording: actual 8x3 schematic and native netlist say `R330` for R1–R8; actual PCB Value says `R`. Native parity text says “Value (R1) ... symbol value (R)” etc.; it is retained as tool output, not treated as the literal file fields. Intended resistance is UNVERIFIED; no assumption of 330 Ω or 0.33 Ω. | Obtain intended resistance and ratings; propose field synchronization only after confirmation. Exact purchasing specification is needed by [JLCPCB BOM requirements](https://jlcpcb.com/help/article/bill-of-materials-for-pcb-assembly), checked 2026-10-29. |
| F-009 | **MINOR**, downgraded from initial MAJOR after scope review: M6 repeated three times on 11x3; m1 seven times on 8x8, all NPTH mounting holes. No assembled-reference duplicates or case-fold collisions were found. This does not stop copper fabrication. | Explicitly exclude mechanical holes from assembly BOM/CPL later; rename only if separately approved/needed for import. If mechanical rows leak into BOM/CPL, promote to assembly BLOCKER. |
| F-010 | **MAJOR.** Embedded/custom libraries differ from installed KiCad 10 libraries; some named libraries cannot resolve. These are portability/reproducibility risks, not automatically JLCPCB spacing failures. Actual geometry and pin memberships are preserved. | Package/verify the existing embedded definitions for import; never refresh to current library geometry merely to silence warnings. |
| F-011 | **INFO for proven net aliases**, MAJOR where a field or library discrepancy remains unresolved. Native schematic/PCB naming differences have identical pad membership; metadata warnings cannot be waived as a group. | Keep proven connectivity, verify naming/fields during import, address F-008 separately. |
| F-015 | **BLOCKER for a defined assembly route.** All boards have components on both sides. Standard assembly framing is unresolved; 11x3 and 8x3 are 66 mm wide, and 11x3 is 260.7 mm long. | Evaluate Standard assembly with manufacturer-approved temporary tooling/frame, or user-selected partial/hand assembly in Phase 3. Do not alter outline, holes, placement or panelize without explicit approval. |
| F-016 | **MAJOR.** All 145 AH49E sensor footprints use 0.9×0.8 mm rectangular pads, opposite rows 2.0 mm apart, same-row pitch 1.9 mm. Official current AH49E suggested layout lists X=0.7, Y=1.0, Z=3.6, G=1.6, E1=0.95, E2=1.9 mm. Existing overall pad extent across opposite rows is 2.9 mm. Thus the historical footprint is not the current recommended land pattern. | In Phase 3 verify the exact SOT-23-3 SKU and solderable lead overlap/tolerances. Accept historical pads only with adequate evidence; otherwise propose an explicitly approved footprint change. Pin mapping matches; land-pattern acceptance remains UNVERIFIED. |
| F-017 | **BLOCKER for sourcing/assembly.** 8x3/UI1 says generic 74HCT138 but has a 5.3×10.2 mm SO16 body footprint. Supplied TI family includes different packages; the NS drawing is not proof that an HCT138 ordering code exists in that package. Nexperia 74HCT138D uses 3.9 mm body SO16. | Find an exact function/pin-compatible SKU fitting the retained pads first. If unavailable, request explicit approval for a footprint change. Do not substitute HC138 or a 238 variant based on the shared family document. |
| F-018 | **MAJOR.** UI2 on 11x3 and 8x3 has an unassigned pad 4 (tab); symbols expose pins 1–3 only. Pad 4 is at (102.37,96.01) and (70.83,101.00) mm. No-net pad is omitted from electrical membership checks. This is not proof of a circuit open: physical tab connectivity/thermal behavior depends on the selected regulator. | Verify selected AMS1117 package/tab assignment and thermal land requirements. If needed, propose pad-number/net mapping correction without routing changes. Do not automatically connect it to any net. |
| F-019 | **MAJOR.** Custom 11x3 J32/J33 footprint name says Wago_2601-602, whereas source document describes 2061-602/998-404. Four pads are numbered 1,1,2,2. Fab body/polarity drawing is absent; generic connector values do not specify an exact purchasing part. | Verify exact connector and drawing/orientation in Phase 3; treat the name as an unresolved identifier, not a silently corrected typo. |
| F-020 | **MINOR; MAJOR if a required orientation mark becomes unreadable.** 2,036 footprint silk segments are 0.12 mm (660/387/301/688 by design). On 11x3, 20 connector reference fields are 0.8 mm high; J15/J19 strokes are 0.125 mm. No native silk-over-pad violation reported. | Propose only necessary legend-field/width corrections after an overlap check; obtain approval before editing. Alternatively obtain explicit manufacturing/readability disposition. No clipping or thickening applied. |
| F-021 | **MAJOR.** Exact MPNs/ratings are missing for generic passives, CP1, pin headers/sockets and several active devices. The source-only package comparison below cannot establish full assembly equivalence. No full BOM/CPL exists. | Complete authoritative sourcing and pad/pin review in Phase 3. Generic package names are not evidence of fit or ratings. |
| F-022 | **INFO.** Rectangular closed outlines and expected source layers exist. Geometry minima screened above are within the applicable fabrication limits; no release claimed. | Recheck actual Gerber/drill output in Phase 6, including historical regression comparison. |
| F-023 | **MAJOR.** Three projects specify 0.582 mm, not a listed nominal JLCPCB thickness; intended finished thickness and stackup are UNVERIFIED. | Confirm intent and manufacturer acceptance. Any nominal-thickness or stackup change requires separate approval. |
| F-024 | **INFO.** ERC endpoint-off-grid warnings total 182/166/121/302. ERC reports no errors, and native pin membership agrees with PCB. | Keep coordinates. Review for import fidelity; do not move symbols or wires merely to align a grid. |
| F-025 | **MAJOR.** Other retained active-device land patterns differ from supplied recommended layouts; examples include 11x3 Q1–Q11 and UI3. Differences alone do not establish unsolderability. | Verify exact packages and joint overlap in Phase 3; no library refresh or pad edit without approval. |

## Package and polarity evidence

Local datasheets below are copied originals with SHA-256 in the source inventory. Date of inspection: **2026-10-29**. Source URLs identify the associated documents; inaccessible current downloads are distinguished from locally inspected pages. None of these checks approves a substitute.

| Part/family | Retained geometry / pin evidence | Datasheet/package comparison and status |
| --- | --- | --- |
| LED, all 145 | Four 1.5×1.0 mm pads, local centers (±2.45,±1.60); 1=VSS, 2=DIN, 3=VDD, 4=DOUT. Silk L and Fab chamfer mark pad 1. | CHG-004 names **SKC6812RGBW-WS/C5378724** provisionally. [Candidate datasheet](https://datasheet.lcsc.com/datasheet/pdf/f73fcb028ddf7140b2dbd34804e8ce40.pdf?productCode=C5378724) full actual-drawing/electrical comparison is explicitly gated to Phase 3. No fit claim. |
| AH49E, all 145 | SOT-23-3, 1=VCC, 2=OUT, 3=GND; Fab chamfer at pin 1. | [Diodes AH49E](https://www.diodes.com/assets/Datasheets/AH49E.pdf), Rev.2-2 April 2025, pp.1/8/9: pin table agrees, suggested pad dimensions differ (F-016). Original BCD Rev.1.3 p.9 drawing was visually inspected. Current PDF text verified through web; image retrieval/download failed (403), so current drawing-image confirmation remains UNVERIFIED. |
| 2N3906-labelled Q, 19 total | 11x3 pads 0.9×0.8, row separation 2.0; 8x3 pads 1.475×0.6, separation 1.875 mm; pair pitch 1.9. Source pins B/E/C=1/2/3. | Supplied ON Semiconductor MMBT3906 PDF, PDF p.10/printed p.9: recommended lead-direction pad 1.40 mm, widths 1.00/0.95, row separation 2.20 mm. Both retained patterns differ. The document distinguishes TO-92 2N3906 from SOT-23 MMBT3906; exact MPN remains UNVERIFIED. [Manufacturer family document](https://www.onsemi.com/pdf/datasheet/pzt3906-d.pdf). |
| 11x3/UI3 SN74LV1T34 | SOT-23-5: 1.325×0.6 pads, opposite-row centers 2.275 mm, pitch 0.95. Pins 1 NC, 2 A, 3 GND, 4 Y, 5 VCC. Fab chamfer present. | Supplied TI PDF p.22 DBV0005A shows 1.1×0.6 pads, 2.6 mm row separation, 0.95 pitch. Pin functions agree; lands differ, F-025. [TI datasheet URL](https://www.ti.com/lit/ds/symlink/sn74lv1t34.pdf); current fetch timed out, local drawing inspected. |
| 8x3/UI1 74HCT138 | 1.975×0.6 pads, row separation 6.925 mm, pitch 1.27; Fab pin-1 chamfer. | Supplied TI NS0016A p.21 recommends 1.85×0.6 pads, rows 7.0 mm apart. Current [TI family datasheet](https://www.ti.com/lit/ds/symlink/cd74hct138.pdf) and [Nexperia product/package mapping](https://www.nexperia.com/products/analog-logic-ics/logic/decoders-and-demultiplexers-digital-multiplexers/decoders-demultiplexers/serie/74hc138-74hct138) do not establish a matching exact SKU. F-017. |
| 3x8/UI1 74HC4052D | 1.75×0.6 pads, rows 5.15 mm apart, pitch 1.27; 3.9×9.9 body, Fab pin-1 chamfer. | [Nexperia datasheet](https://assets.nexperia.com/documents/data-sheet/74HC_HCT4052.pdf), SOT109-1, 1.27 pitch and 3.9 mm nominal body agree. Number/function mapping agrees (16 supply, 8 GND, 7 negative supply; mux/control pins checked). No separate manufacturer land-pattern acceptance claimed; exact suffix/reel review Phase 3. |
| 11x3/UI1 74HCT154D | 2.0×0.55 pads, rows 9.3 mm apart, pitch 1.27; 7.5×15.4 body; Fab pin-1 chamfer. | Source references a Nexperia document but supplied PDF is TI CD74HCT154 family. The [TI family page](https://www.ti.com/product/CD74HC154) establishes a 24-pin SOIC package family only, not approval of the source's exact MPN. Package/manufacturer ambiguity remains F-021. |
| UI2 AMS1117-3.3, two | 2.0×1.5 lead pads at 2.3 pitch; 2.0×3.8 tab pad; opposing centers 6.3 mm. Fab chamfer exists. | Original AMS PDF p.7 SOT-223 drawing visually inspected: lead pitch 2.29 nominal, tab width 2.95–3.15, total lead span 6.71–7.29 mm. Leads 1 GND, 2 OUT, 3 IN agree; tab net absent (F-018). [AMS document via LCSC](https://datasheet.lcsc.com/lcsc/1811142212_Advanced-Monolithic-Systems-AMS1117-3-3_C6186.pdf). Exact sourced variant and thermal adequacy remain unverified. |
| 11x3/J32,J33 | Two potentials, each with 4.5×2.4 and 6.5×2.1 pads; potential pitch 6 mm, opposing pad centers 11.5 mm. | Supplied WAGO_2061-602.pdf lists those pad sizes/pitch for 2061-602/998-404. Full coordinate datum and orientation acceptance UNVERIFIED; identifier discrepancy F-019. Source URL recorded in schematic is malformed (trailing `~`): https://cdn-reichelt.de/documents/datenblatt/C160/WAGO_2061-6_DB.pdf~ . No online compatibility claim based on that URL. |
| Headers/sockets, 2/3/44 contacts | Source geometry, numbers and Fab chamfers retained; gallery includes reversed header/socket arrangements. | Generic names and original photographs do not establish an exact MPN, mating orientation or current rating. All corresponding placements require Phase 3 selection and Phase 6 directional review. |
| R/C 1206; CP1 | Source land dimensions retained; CP1 has a plus mark and pad1 on P, pad2 on GND. | No exact passive manufacturer drawings, ratings or CP1 case variant supplied. UNVERIFIED until sourced; do not infer voltage, dielectric, power or capacitor height from the footprint name. |

The gallery shows source orientation cues, not proven surviving manufactured legend. Some cues exist only on Fab; the WAGO body/polarity drawing is missing. Full per-designator physical pin-1 and bottom-side CPL rotation verification remains Phase 6. No mounting or sensor orientation was changed.

## Phase 3 hard gate for CHG-004

Status stays **Applied-provisional**. Phase 3 must verify the actual candidate package drawing against every retained pad geometry and pinout, suitable supply/logic/timing/electrical ratings, pixel format and firmware impact. Original supplied LED documentation describes 24-bit RGB; candidate family documentation describes 32-bit RGBW. The original fitted SKU is unknown, so no claim is made about the deployed firmware's behavior. Firmware is not read or edited by this work.

Calculate worst-case full-channel LED current per design (33/24/24/64) and for the user's actual board multiplicities. Include driver/quiescent current and a genuine specified maximum or clearly marked bound; typical channel current is not a guaranteed worst case. Compare the current paths with the actual supply, trace/plane geometry/copper, vias and exact connector ratings. Supply model, assembled multiplicities and allowable temperature rise are not inferred. If equivalence fails, revise/reject CHG-004 and stop downstream reliance on it. No production files or import should proceed on an unverified LED.

## Gate and outstanding decisions

1. Accept this analysis with **APPROVED PHASE 2** to begin Phase 3; that does not approve any repair or waive a finding.
2. Confirm the intended resistance of **8x3 R1–R8** (source label `R330`), or explicitly leave it unresolved for further evidence.
3. Confirm whether **0.582 mm source thickness** was intended to represent nominal 0.6 mm, or must remain an exact requirement. No thickness/stackup edit or order selection follows automatically.

All proposed fixes above remain parked and unapproved. Manufacturer consultation, panel/frame design, source corrections, parts assignments and production exports have not occurred. LED package/electrical/current checks remain the explicit Phase 3 condition.

Needs from you: APPROVED PHASE 2, intended R1–R8 resistance, and thin-board thickness intent.
