> **Phase 2 erratum, 2026-10-29:** F-008 wording is corrected: the 8x3 R1–R8 schematic and native netlist contain `R330`; PCB Value fields contain `R`. The native DRC message reports different text and must not be mistaken for literal source fields. F-009 mechanical reference duplication is now MINOR; see [Phase 2 audit](../phase2/PHASE2_AUDIT.md). Raw Phase 1 evidence remains unchanged.

# Phase 1 audit and baseline proposal

Date checked: **2026-10-29**. **Analysis complete; no baseline assembled and no design change applied.** All four designs are in production scope. GUI import, manual sourcing/assignment and conditional GUI-export fallbacks were explicitly approved by the user. Historical fabrication files are reference only.

## Source formats and native environment

| Design (both original and update) | PCB format | Schematic format | Project JSON meta.version | Minimum opener / verification |
| --- | --- | --- | --- | --- |
| 11x3 | 20211014 | 20211123 | 1 | KiCad 6-era formats; exact earliest compatible release UNVERIFIED; successfully read by 10.0.7 |
| 8x3 | 20211014 | 20211123 | 3 | KiCad 6-era drawings with a separately versioned project schema; exact earliest complete-project compatibility UNVERIFIED; successfully read by 10.0.7 |
| 3x8 | 20211014 | 20211123 | 1 | KiCad 6-era formats; exact earliest compatible release UNVERIFIED; successfully read by 10.0.7 |
| 8x8 | 20211014 | 20211123 | 1 | KiCad 6-era formats; exact earliest compatible release UNVERIFIED; successfully read by 10.0.7 |

[Official schematic-format documentation](https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/) establishes that this S-expression family starts with KiCad 6.0. It does not certify these exact files against every 6.x release. No unsupported exact-minimum claim is made. Historical Gerbers identify Pcbnew 6.0.7-1, which is exporter evidence, not an opening test of the current projects. The verified usable opener here is **10.0.7**. There is no need to install/downgrade to an older version. Native CLI DRC/ERC was introduced in KiCad 8 ([official release notes](https://www.kicad.org/blog/2024/02/Version-8.0.0-Released/)). Sources checked 2026-10-29.

Command: `/usr/bin/flatpak run --command=kicad-cli org.kicad.KiCad`. The KiCad MCP remains pointed at an absent host executable; the Flatpak CLI is the native-check path. Eight project copies were placed under `01_audit/phase1/copies/`, preserving the candidate's relative library layout. ERC, DRC with schematic parity, and netlist export ran on each copy. No save, upgrade or zone-refill option was used. DRC uses stored copper fills and inherited rules, not current JLCPCB rules. Detailed commands, outputs, return codes, and input hashes are in [NATIVE_RUNS.json](NATIVE_RUNS.json). Exit code 5 means violations were found; it is not a tool connection failure.

## Component-level and file-level comparison

[COMPONENT_DIFF.csv](COMPONENT_DIFF.csv) and [COMPONENT_DIFF.json](COMPONENT_DIFF.json) give per-reference changes and unchanged records, including values, footprints, MPN/LCSC fields, and pad nets/geometry. Per-design component inventories include schematic identities/properties and PCB positions/pads. Native pin/net evidence is in [CONNECTIVITY_AND_CHECKS.json](CONNECTIVITY_AND_CHECKS.json). [FILE_COMPARISON.json](FILE_COMPARISON.json) lists file hashes/status; eight unified text diffs preserve all source edits.

| Design | Changed references | Count | Classification |
| --- | --- | ---: | --- |
| 11x3 | D1–D33 | 33 | (a) intentional component identity update |
| 8x3 | D1–D24 | 24 | (a) intentional component identity update |
| 3x8 | D1–D24 | 24 | (a) intentional component identity update |
| 8x8 | D1–D64 | 64 | (a) intentional component identity update |

**145 LED instances** across four unique designs; this is not a full-board procurement quantity. All other component identities are unchanged. For each LED:

- Schematic Value changes `SK6812` -> `SKC6812RGBW-WS`; library ID changes `LED:SK6812` -> `Saiboard_LED:SKC6812RGBW-WS`; Datasheet URL changes to the supplied LCSC PDF URL.
- Manufacturer=`OPSCO Optoelectronics`, MPN=`SKC6812RGBW-WS`, LCSC=`C5378724`, and AssemblyStatus=`HOLD - compatibility differences; see README.md` are added to schematic and PCB.
- PCB value text changes to the new MPN. The existing `LED_SMD:LED_SK6812_PLCC4_5.0x5.0mm_P3.2mm` footprint remains. Schematic instance-cache values and the embedded LED library label change consistently.
- Pin numbers/types/coordinates remain 1=VSS/power_in, 2=DIN/input, 3=VDD/power_in, 4=DOUT/output. All PCB pads, positions, layers, copper objects, outline and stackup fields remain identical.

The complete parsed PCB and schematic trees match after removing only the listed LED identity changes and the changed embedded LED definition. This comparison includes every footprint occurrence, including duplicate references; it does not rely only on a reference-keyed dictionary. Non-LED embedded libraries match. The LED pin signatures match. Original/update native netlists have identical names and node memberships for each design. The embedded symbol's altered descriptive artwork/identity is intentional; it does not establish an electrically equivalent part.

All four `.kicad_pro` files are byte-identical between sets. The candidate adds a local symbol library, four relative symbol tables, two LED-only CSVs, a prior validation record and datasheet/report evidence. These are category (a) supporting additions, not production approval. Its README is a separate candidate report, not a replacement for the original electronics construction README. The four LED BOM rows match all 145 candidate PCB LED references, MPN/LCSC fields and footprint names; all 580 pad-audit rows match their candidate PCB pad function, net and geometry. The local LED symbol matches the embedded candidate symbol in all four schematics, and its copied original LED PDF matches the original PDF hash. See [CANDIDATE_SUPPORT_CHECKS.json](CANDIDATE_SUPPORT_CHECKS.json). These checks establish internal record consistency, not datasheet equivalence. Prior validation claims beyond these checks remain unverified.

## Exact LED identity and unresolved compatibility

The spelling **SKC6812RGBW-WS is real**, not silently corrected to SK6812. The official [LCSC C5378724 listing](https://www.lcsc.com/product-detail/C5378724.html), checked 2026-10-29, identifies OPSCO Optoelectronics, MPN SKC6812RGBW-WS, SMD5050-4P. This verifies identity only; JLCPCB stock/class/assembly eligibility is not inferred.

The update replaces design records labelled **SK6812**; the exact originally fitted manufacturer SKU/white bin is **UNVERIFIED**. The original embedded symbol and footprint name do not establish that SKU. The supplied original datasheet describes 24-bit data on page 1 and the 24-bit structure on page 6. The candidate's supplied family datasheet identifies revision B/1, 2025-07-31, on page 1 and a 32-bit GRBW/Y/A structure on page 10. Local supplied PDF hashes are in the source inventory; extracted text is saved as `original_LED_datasheet.txt` and `candidate_LED_datasheet.txt`. The remote PDF could not be retrieved through the web tool in this phase; its currency and exact family-suffix applicability remain unverified. No timing, current, land-pattern or drop-in equivalence claim is made in Phase 1.

**Firmware impact is flagged:** the documented RGB vs RGBW payload distinction needs confirmation before any substitution approval. The firmware was not inspected or changed. Prior candidate firmware/timing and power claims remain parked until their evidence is reviewed under the allowed scope. A match in pin numbering is not sufficient to approve the candidate LED.

## Internal consistency and native checks

Counts below are identical for original and update. ERC counts are warnings; DRC errors/warnings exclude the separate parity column. Raw reports are under `native/{original,updated}/{design}/`.

| Design | PCB footprints | On-board schematic non-power parts | ERC warnings | DRC errors | DRC warnings | Unconnected | Parity warnings |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 11x3 | 171 | 165 | 273 | 2 | 164 | 0 | 184 |
| 8x3 | 117 | 114 | 230 | 0 | 114 | 0 | 134 |
| 3x8 | 92 | 89 | 166 | 0 | 89 | 0 | 101 |
| 8x8 | 222 | 214 | 399 | 0 | 214 | 0 | 272 |

- No on-board schematic non-power component lacks a PCB reference or an assigned footprint. PCB-only parts are mounting holes: 6 on `11x3`, 3 each on `8x3`/`3x8`, 8 on `8x8`. These are mechanical exceptions, not missing electrical parts.
- `11x3` repeats mounting-hole reference M6 three times (M1/M2/M5 occur once each). `8x8` repeats m1 seven times and has one m2. Duplicates predate the update: category (b), inherited inconsistency. No renumbering performed.
- `8x3` has eight parity warnings: the PCB resistor value fields literally contain `R1`…`R8`, while schematic values are the generic `R`. The numerical resistor values are unexplained/category (c). They cannot become procurement values by inference.
- `11x3` has two inherited `zones_intersect` errors: equal-priority GND zones on In1.Cu and P zones on In2.Cu intersect. These are errors, not passed checks. No zone priority/geometry was changed or refilled.
- All ERC findings are warnings: off-grid endpoints, footprint-link issues, library-symbol mismatch or missing-library-symbol entries. DRC warnings are library-footprint mismatches/link issues. Current KiCad 10 libraries differ from embedded legacy content and some custom library links are unresolved. Embedded source content was preserved; no library refresh or relink was applied. Count/type details and descriptions remain in the raw JSON.
- Parity reports legacy generated-net aliases, datasheet/field mismatches, mechanical extras/duplicates and the resistor issue. Pin-membership comparison shows zero connectivity mismatch pins and zero missing schematic/PCB net nodes in every design. Fully identical pin groups have 58/34/26/67 name aliases (`11x3`/`8x3`/`3x8`/`8x8`). Thus the reported name differences are not evidence of rewiring; native parity is still not clean and its metadata warnings remain open.
- Candidate LED Datasheet properties exist in the schematic but not as PCB Datasheet properties, an inherited/general category (b) metadata-sync issue. Added MPN/LCSC/Manufacturer/HOLD fields agree across candidate schematic and PCB. The LED-only candidate CSV is not a complete assembly BOM.
- Project rules suppress some native checks; `ignored_checks` and included severities are recorded in every native report. These results are not a full manufacturer DFM signoff. No new suppressions were added.

## Historical Gerber/drill attribution — reference only

[HISTORICAL_FAB_COMPARISON.json](HISTORICAL_FAB_COMPARISON.json) records generator/date, ProjectId, outline, hole coordinates/diameters, counts, layers, and ZIP-vs-loose member hashes. Dimensions below use the outline path centreline, not the plotted stroke's outer extent.

| Design | Outline mm (Gerber = both sources) | Copper layers (all match) | PTH records | NPTH records | Source holes incl. vias | Generation date |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 11x3 | 66.0 × 260.7 | 4 | 296 | 6 | 302 | 2023-12-02T14:15:27+01:00 |
| 8x3 | 66.0 × 189.6 | 2 | 148 | 3 | 151 | 2022-12-02T15:43:41+01:00 |
| 3x8 | 176.0 × 71.1 | 2 | 169 | 3 | 172 | 2022-12-02T15:50:45+01:00 |
| 8x8 | 176.0 × 189.6 | 2 | 350 | 8 | 358 | 2022-12-02T15:51:39+01:00 |

All holes can be paired one-to-one by plating type, diameter and coordinates within 0.001 mm; maximum coordinate distance is below 0.0007 mm, consistent with the historical Excellon decimal quantization. Exact rounding into 0.001 mm bins differs for one hole each on `11x3` and `8x3`; raw differences are retained rather than hidden. Job-file dimensions are 0.1 mm larger per axis than outline centreline sizes, matching the 0.1 mm outline stroke extent; no board outline changed.

All compared historical ZIP fabrication members match their loose counterparts byte-for-byte. Their generator is `(6.0.7-1)-1`, but ProjectId revision is **`rev?`**. Geometry matches both current source families because the LED update did not change fabrication geometry. **Exact design/electrical revision attribution is UNVERIFIED**; these tests cannot distinguish the original from a metadata-only LED revision or prove all copper equals a particular commit. No historical file will be reused as production output.

## One proposed baseline — CHG-004 (Proposed, not applied)

Use the **original four-project source family** as the audit baseline. It preserves the existing design without treating a compatibility-unapproved LED substitution as accepted hardware. Phase 3 will first check availability of the original exact part if it can be identified, then follow the requested substitution priority. Selecting this baseline does not claim the original BOM is orderable or its ERC/DRC is clean.

| Files to keep in future `02_work/baseline/` | Exact source version | Why |
| --- | --- | --- |
| `kicad_files/11x3/11x3.kicad_pro`, `.kicad_sch`, `.kicad_pcb` | Original snapshot versions, 3 files | Original controller/power design; do not accept LED update implicitly. |
| `kicad_files/8x3/8x3.kicad_pro`, `.kicad_sch`, `.kicad_pcb` | Original snapshot versions, 3 files | Same criterion; preserve ambiguous resistor values for explicit resolution. |
| `kicad_files/3x8/3x8.kicad_pro`, `.kicad_sch`, `.kicad_pcb` | Original snapshot versions, 3 files | Original multiplexed sensor design. |
| `kicad_files/8x8/8x8.kicad_pro`, `.kicad_sch`, `.kicad_pcb` | Original snapshot versions, 3 files | Original matrix design; retain/report mechanical duplicate references. |
| `datasheets/` (12 files), original `README.md`, `pcb.jpg`, `paste.jpg` | Original snapshot versions | Preserve local construction and reference context without changing evidence. |
| Existing partial-update sources, LED library/tables, candidate CSVs/PDFs/report | Keep under preserved snapshot/audit evidence only | Useful candidate evidence; not included as baseline source or full BOM. |
| Historical Gerbers/drills/ZIPs, `.kicad_prl`, `.lck`, archived duplicate `8x8`, 3D-print manufacturing assets | Preserve in snapshot; exclude from the new baseline | Historical/transient/non-EDA evidence; do not mix into a new production release. No originals deleted. |

This is a file-selection proposal for **27 files**, with exact hashes in [PROPOSED_BASELINE_MANIFEST.json](PROPOSED_BASELINE_MANIFEST.json), derived from the Phase 0 manifest. Nothing has been copied to `02_work/baseline/`. CHG-004 requires explicit approval before materialization. Any LED adoption, resistor correction, zone fix, renumbering or library change needs a separate future CHG with its own approval.

## Verification and gate

Native checks ran on eight audit copies only. All input `.kicad_pcb`, `.kicad_sch`, `.kicad_pro`, `.kicad_sym` and symbol tables retained their pre-run hashes. All 117 originals and snapshot files match the Phase 0 hashes after the checks. `03_output/` remains empty. No design upgrade, save-over, baseline merge, component replacement or manufacture output occurred.

Open evidence: original fitted LED manufacturer/SKU; exact historical source revision; exact earliest KiCad release capable of the complete projects. None is guessed. Please provide original purchasing/revision records if available; otherwise retain these as UNVERIFIED and continue using the verified 10.0.7 environment.

Needs from you: `APPROVED PHASE 1` and approval of **CHG-004** (original-family baseline). Baseline approval is separate from approving any design fix or substitution.
