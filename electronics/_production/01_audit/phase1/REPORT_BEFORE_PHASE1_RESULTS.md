# Saiboard production preparation report

Updated: **2026-10-29**. Target: JLCPCB fabrication and SMT assembly. Status: **NOT RELEASED FOR MANUFACTURE**.

## 1. Summary and current status

**Phase 0 was approved on 2026-10-29. Phase 1 prerequisites are in progress; component-level audit is not yet performed.** Production scope and the sourcing/assignment fallbacks below await confirmation. No baseline, component replacement or design change is approved.

The complete electronics tree, excluding the newly created `_production/`, was inventoried and copied: **117 files, 55,776,867 bytes, 18 subdirectories**. Source and snapshot SHA-256, sizes and modification times match. Snapshot file/directory write bits were removed after copying. Originals were not edited. No production design was selected, merged, imported, saved, rerouted, refilled or exported.

Two source families exist, each containing the four designs `11x3`, `3x8`, `8x3`, and `8x8`: the original `kicad_files/` and the explicitly unreleased `updated_components_SKC6812RGBW-WS/`. Treat the latter's statements and prior validation as **UNVERIFIED**, not approval evidence.

Historical Gerbers and drill files **are present**, contrary to the initial missing-files premise. Their consistency with the source designs and suitability for ordering are unverified. A complete assembly BOM and CPL were not found; the partial folder contains LED-only candidate documentation.

Open workflow blockers:

- **F-001:** no file-import MCP tool is exposed. User-assisted GUI import was explicitly approved on 2026-10-29; MCP fidelity verification remains mandatory. No object-by-object reconstruction is allowed.
- **F-002 update:** installed Flatpak CLI **10.0.7** runs successfully. Native `/usr/bin/kicad-cli` and MCP IPC remain unavailable. Direct Flatpak invocation is available for checks exclusively on `01_audit/` or `02_work/` copies; no upgrade/save-over command is allowed.
- **F-004:** exact EasyEDA editor build and import compatibility with these source-format revisions remain UNVERIFIED.

No software installation, system configuration change, JLCPCB upload, order, payment or communication to a third party occurred.

## 2. Source inventory and source-of-truth candidates

All source paths below are relative to `electronics/`. The full file-level inventory provides **path, type, bytes, UTC modification date and SHA-256**:

- [SOURCE_INVENTORY.md](../01_audit/SOURCE_INVENTORY.md) — human-readable inventory of all 117 files.
- [SOURCE_INVENTORY.csv](../01_audit/SOURCE_INVENTORY.csv) — machine-readable inventory, including nanosecond modification times.
- [SOURCE_SHA256SUMS.txt](../01_audit/SOURCE_SHA256SUMS.txt) — source-relative content hashes.
- [ARCHIVE_INVENTORY.json](../01_audit/ARCHIVE_INVENTORY.json) — ZIP members, sizes, timestamps and hashes; all five ZIP CRC checks passed.
- [SOURCE_FORMATS.json](../01_audit/SOURCE_FORMATS.json) — source-header and exporter-version evidence.
- [SNAPSHOT_VERIFICATION.json](../01_audit/SNAPSHOT_VERIFICATION.json) — preservation checks and tool-path discovery.

| Source group | Files | Bytes | Role / current disposition |
| --- | ---: | ---: | --- |
| `kicad_files/` | 69 | 9,743,617 | Original-source candidate, including historical fabrication files. Preserved, not selected as production baseline. |
| `updated_components_SKC6812RGBW-WS/` | 23 | 7,926,905 | Unverified update candidate, including local LED library, four symbol tables, two CSVs, prior validation, README and two PDFs. |
| `datasheets/` | 12 | 5,854,709 | Original reference documents/images; applicability to actual fitted parts has not been checked. |
| `3d_prints/` | 10 | 28,642,135 | Included to preserve the entire electronics folder; not modified or used to redesign hardware. |
| Root `README.md`, `paste.jpg`, `pcb.jpg` | 3 | 3,609,501 | Construction context and photos. |

### Candidate map

| Design / source | Original candidate | Partial-update candidate | Phase 0 disposition |
| --- | --- | --- | --- |
| `11x3` | `kicad_files/11x3/11x3.kicad_{pro,sch,pcb}` | `updated_components_SKC6812RGBW-WS/kicad_files/11x3/11x3.kicad_{pro,sch,pcb}` | Preserve both; component comparison deferred to Phase 1. |
| `3x8` | `kicad_files/3x8/3x8.kicad_{pro,sch,pcb}` | `updated_components_SKC6812RGBW-WS/kicad_files/3x8/3x8.kicad_{pro,sch,pcb}` | Preserve both; comparison deferred. |
| `8x3` | `kicad_files/8x3/8x3.kicad_{pro,sch,pcb}` | `updated_components_SKC6812RGBW-WS/kicad_files/8x3/8x3.kicad_{pro,sch,pcb}` | Preserve both, including original lock/local-settings files; comparison deferred. |
| `8x8` | `kicad_files/8x8/8x8.kicad_{pro,sch,pcb}` | `updated_components_SKC6812RGBW-WS/kicad_files/8x8/8x8.kicad_{pro,sch,pcb}` | Preserve both; comparison deferred. |
| Archived `8x8` | `kicad_files/8x8/8x8.kicad_.zip` | None | Its schematic and PCB member hashes match the loose original files. It contains no project configuration; not an independent candidate revision. |
| Local update library | None at the matching original path | `Saiboard_LED.kicad_sym` plus each project's `sym-lib-table` | Preserve relative paths. Presence does not verify the symbols, parts or footprints. |
| Historical fabrication | Each original design's `gerbers/` directory and `gerber.zip` | None in partial-update set | Preserve for evidence only; not released or copied into `03_output/`. |

Brace notation above identifies three actual files; their exact filenames and individual hashes are in the inventory. **Baseline: UNSELECTED.** Phase 1 must propose one coherent family of four projects and their required libraries before any baseline is built in `02_work/baseline/`.

### EDA format and version evidence

- Eight PCB files: KiCad S-expression, format version **20211014**, generator `pcbnew`.
- Eight schematic files: KiCad S-expression, format version **20211123**, generator `eeschema`.
- Update symbol library: KiCad S-expression, format version **20211014**, generator `kicad_symbol_editor`.
- Eight `.kicad_pro` files: JSON; `meta.version` is **1** for `11x3`, `3x8`, `8x8`, and **3** for `8x3`, in both families. These are project-file schema versions, not editor release numbers.
- Historical Gerber job metadata identifies **KiCad Pcbnew `(6.0.7-1)-1`**, with generation dates 2023-12-02 for `11x3` and 2022-12-02 for the other three designs. This establishes the historical exporter build only. The exact application build that last wrote each source is **UNVERIFIED**, because the source headers do not record it.
- There are **38 loose Gerber layers, 8 drill files, 4 Gerber job files, 4 Gerber ZIPs**, and the separate `8x8` source ZIP. Presence/CRC checks do not establish fabrication correctness or source synchronization.

The [upstream project page](https://github.com/miliar/saiboard), checked 2026-10-29, identifies Saiboard and its GPL-3.0 license. The local extracted tree has not been tied to a verified upstream commit; filenames and filesystem timestamps are not proof of upstream identity. No upstream files replaced local files.

### Tool discovery

All **101 exposed EasyEDA Pro tools** are listed individually with action and limits in [EASYEDA_TOOLS.md](../01_audit/EASYEDA_TOOLS.md); full schemas are retained alongside it. The connected MCP server/extension is 1.6.0, bridge is 1.0.0, profile is `pro`. No Standard MCP tools were found. The actual EasyEDA editor build is UNVERIFIED.

[IMPORT_SUPPORT.md](../01_audit/IMPORT_SUPPORT.md) separates verified MCP capabilities from vendor-documented application import formats and records official source URLs and the check date. MCP file import: **not exposed**. Application routes include native Pro ZIP/`.epro` and libraries, direct KiCad packaging, and a separate converter accepting KiCad source formats; compatibility and fidelity are not tested. Export tools for Gerber/drill, BOM and CPL are advertised but have not been run.

## 3. Findings log

These are discovery findings, not a completed design/manufacturability audit. Severity describes impact on the requested workflow.

| ID | Severity | Finding / evidence | Proposed resolution | Status |
| --- | --- | --- | --- | --- |
| F-001 | BLOCKER | No project-file importer among 101 exposed EasyEDA tools. Bridge capabilities are broader than callable tools. [Tool inventory](../01_audit/EASYEDA_TOOLS.md), checked 2026-10-29. | Provide an import-capable MCP surface or explicitly approve a manual/UI import exception for Phase 5. No conversion or import now. | Open |
| F-002 | BLOCKER | Local KiCad executables absent; KiCad MCP reports CLI/IPC unavailable and native DRC/ERC/export disabled. Connector targets an unrelated project. [Readiness evidence](../01_audit/KICAD_READINESS.json), checked 2026-10-29. | Identify an existing native KiCad environment for Phase 1. If none is available, request specific installation/setup approval separately. Never substitute static checks for native passes. | Open |
| F-003 | INFO | Original `gerbers/` directories contain historical fabrication artifacts. [Inventory](../01_audit/SOURCE_INVENTORY.md), checked 2026-10-29. | Correct the missing-artifact premise; preserve existing files and verify/regenerate against the approved baseline in the proper later phases. | Recorded |
| F-004 | MAJOR | Exact EasyEDA editor build missing from status replies; direct KiCad guide names 5.1/5.9 while these files declare other numeric format revisions. Converter extension support does not establish exact-version compatibility. [Import evidence](../01_audit/IMPORT_SUPPORT.md), checked 2026-10-29. | Establish editor version and supported import route; perform fidelity verification only in approved Phase 5. | UNVERIFIED |
| F-005 | MAJOR | No complete assembly BOM or CPL identified. Partial README expressly identifies `LED_BOM_CANDIDATE.csv` as LED-only. [Snapshot README](../00_original_snapshot/updated_components_SKC6812RGBW-WS/README.md), checked 2026-10-29. | Derive full component sourcing data in Phase 3 and assembly outputs from the approved baseline in Phase 6. | Open |
| F-006 | MAJOR | Update README explicitly says candidate/not released and describes unresolved electrical, footprint and firmware questions. Prior `validation.json` is unverified supplied evidence. | Independently audit in Phase 1; perform equivalence/sourcing checks in Phase 3. Do not accept the folder name, supplier code or prior conclusions as verified. | UNVERIFIED |

## 4. Change log

Statuses follow **Proposed -> Approved -> Applied -> Verified**, or **Rejected**. All subsequent circuit, component, footprint, baseline-selection and import changes require their own approved CHG entry. Existing partial work is inherited evidence, not an applied/approved change in this workflow.

| ID | Phase | Category | Affected designators / files | Before -> After | Reason / finding | Evidence and date | Electrical / mechanical / firmware impact | Risk | Status | Approved |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHG-001 | 0 | Preservation and documentation only | No designators; new `_production/` folders, snapshot, audit records, helper and this report | No production workspace -> inventory, verified read-only snapshot and Phase 0 documentation | Establish requested preservation/change-control process; retain historical artifacts identified by F-003 | User's Phase 0 instructions; [inventory](../01_audit/SOURCE_INVENTORY.csv) and [verification](../01_audit/SNAPSHOT_VERIFICATION.json), 2026-10-29. Local evidence; external URL not applicable. | None: original design bytes unchanged; no design copy edited | Snapshot reflects current local tree, not independently authenticated upstream history | **Verified** | Explicit Phase 0 authorization in user's START request, 2026-10-29 |

CHG-001 lifecycle: proposed by the user's requested structure and discovery scope; approved by the same START instruction; applied and hash-verified 2026-10-29. Snapshot creation is not a baseline approval. The helper is [phase0_snapshot.py](../02_work/phase0_snapshot.py); it refuses to overwrite an existing snapshot and includes preservation assertions. No design changes have been proposed, approved or applied by this session.

## 5. BOM substitution table

**Not started — Phase 3 is not authorized.** No supplier selection or replacement is approved. Counts of unique parts, Extended parts, stock, fees, price and unverified sourcing items are **NOT ASSESSED**, not zero. The supplied LED candidate CSV is retained only as source material.

| Designators / qty | Original part | Proposed replacement | LCSC # | Library status / class / stock / date | Equivalence evidence / URL | Footprint change | Reason / risk | CHG / status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pending component inventory | UNVERIFIED | None proposed | UNVERIFIED | UNVERIFIED | Required in Phase 3 | UNVERIFIED | No part availability or compatibility claim yet | None |

## 6. Parked items — not acted on

- Any firmware format/timing/power statements in the inherited update README: **UNVERIFIED assertions**, retained for later flagging. No firmware/software files were inspected or edited for this task.
- Suggested footprint, electrical or power changes in that README: no adoption, correction or redesign authorized.
- Any topology, routing, placement, outline, mounting-hole or stackup changes: prohibited without explicit scope expansion and change approval.
- Existing `8x3` lock/local-settings files and ZIP housekeeping members: preserved; not cleaned up. A lock file alone does not establish an active editor session.
- Legacy manufacturing ZIPs: quarantined as historical evidence in the snapshot; not treated as ready-to-order deliverables.
- Any new installation, connector reconfiguration or import-route workaround: not performed.

## 7. Open questions / Phase 1 prerequisites

Phase 0 approval and user-assisted Phase 5 import are accepted, dated 2026-10-29. The user's production-design list still contains placeholders.

| Design | Purpose inferred from original PCB component labels (not a completed connectivity audit) | Recommendation |
| --- | --- | --- |
| `11x3` | 33 Hall/LED positions, ESP32-S3 socket interfaces, power/regulator and row-control electronics | Include for a complete Saiboard; confirm production vs audit-only/ignore. |
| `8x3` | 24 Hall/LED positions with 74HCT138 row decoding, transistors and regulator | Include for the complete board family; confirm scope. |
| `3x8` | 24 Hall/LED positions with 74HC4052 analog multiplexing | Include for the complete board family; confirm scope. |
| `8x8` | 64 Hall/LED matrix positions and interconnects | Include for the complete board family; confirm scope. |

These purposes are provisional inferences from the supplied sources. Quantities and physical arrangement have not been established. No production choice is made from filenames alone.

1. Confirm which of the four designs are for production, and whether the remainder are audit-only or ignored. Recommendation: all four if preparing the complete Saiboard family.
2. Accept official JLCPCB/LCSC page verification where MCP sourcing/classification is incomplete, and GUI assignment of approved LCSC numbers followed by MCP readback. See the prerequisite matrix in [EASYEDA_TOOLS.md](../01_audit/EASYEDA_TOOLS.md).
3. Accept user-assisted GUI exports/detailed DRC review only if MCP output/detail is insufficient. No fallback has been executed.

The Flatpak CLI works; installation/uninstallation is unnecessary. Package suffix `-2` identifies the Arch packaging revision, not a requirement to replace KiCad 10.0.7. The interrupted native-package installation attempt produced no confirmed installation; `pacman -Q kicad` still reports no installed native package. No system changes were performed by this task.

## 8. Verification results

### Phase 0 checks actually performed

| Check | Result / evidence |
| --- | --- |
| Recursive inventory, including hidden/lock files and all existing source groups | PASS: 117 regular files; no symlinks or special filesystem objects found. |
| Original/snapshot SHA-256, byte count and modification time equality | PASS for all 117 files; original path list unchanged during snapshot. |
| Snapshot protection | PASS: file and directory write bits removed. This is a filesystem safeguard, not an immutable storage service. |
| Existing ZIP integrity | PASS: all five ZIP CRC checks; member inventory saved. No extracted files written back to originals. |
| Archived `8x8` candidate identity | PASS: its two members match the loose original schematic/PCB hashes. |
| Source-format identification | PASS: KiCad source headers/project metadata and historical Gerber generator metadata recorded. Exact source-writing editor build remains unverified. |
| EasyEDA MCP discovery | PASS: 101 tool schemas recorded; healthy Pro bridge; no imported design examined. |
| Native KiCad readiness | BLOCKED: missing CLI and unavailable IPC; no ERC/DRC run. |
| No unauthorized design work | No baseline directory or production export created. `02_work/` contains only the discovery helper; `03_output/` is empty. |

### Phase 6 checklist — all NOT RUN

| Required verification | Status |
| --- | --- |
| Gerber layer count and closed outline match approved source | NOT RUN |
| Excellon drill units and hole types/sizes | NOT RUN |
| BOM/CPL assembled designators match 1:1 | NOT RUN |
| Every assembled component has a verified LCSC number | NOT RUN |
| Bottom-side coordinates and rotation convention | NOT RUN |
| Rotation/pin-1 review of LEDs, ICs, diodes, connectors and sensors | NOT RUN |
| Source/import component, net, outline, layer and pad geometry fidelity; copper refill review | NOT RUN |
| Native ERC/DRC and approved findings closure | NOT RUN |
| Current JLCPCB column formats, capabilities, stock/class/fee policy | NOT RUN |
| Final ZIP contents and release hash verification | NOT RUN |

## 9. Known risks and assumptions

- The snapshot is the exact local starting point, including previously modified files and unverified prior reports. No upstream revision is assumed.
- The four designs are treated as a design family for discovery. Physical-board quantities and assembly-side requirements are not inferred from filenames.
- The `SKC6812RGBW-WS` spelling is preserved verbatim; no typo correction or exact LED identity is assumed. Identity and replacement history remain Phase 1 work.
- Historical Gerbers, embedded footprints, library tables and prior validation records do not establish production readiness.
- Datasheet identity/revision, pin mapping, geometry, protocol, current consumption and real-device behavior remain unverified in this phase. No numerical substitution claims are adopted from memory or the partial report.
- Future import may change copper fills or represent primitives differently; only a measured fidelity review can accept the imported design. No rerouting is authorized as a workaround.
- UTC inventory timestamps are filesystem metadata; ZIP timestamps have no reliable timezone. Neither establishes design chronology.
- The finished-board design is **not orderable/released on the basis of Phase 0**. Phases 1–7 and all required approvals remain outstanding.

Needs from you: production scope and decisions on the prerequisite fallbacks in section 7.


### Phase 1 prerequisite update — 2026-10-29

[CLI evidence](../01_audit/PHASE1_CLI_PREFLIGHT.json): system Flatpak application `org.kicad.KiCad` reports CLI version 10.0.7 with exit code 0 when run outside the execution sandbox. MCP still targets the missing native binary. ERC/DRC has not run. Source files and snapshot have not been opened by KiCad, upgraded or saved. Historical Gerber/drill revision comparison and component-level diff remain pending the prerequisite decisions.

CHG-002 | Phase 1 prerequisites | Documentation only | `EASYEDA_TOOLS.md`, CLI evidence, production report | Phase 0 status -> approval/GUI-import decisions and Flatpak readiness recorded | User decisions and read-only command evidence, 2026-10-29 | Electrical/mechanical/firmware impact: none | Risk: capabilities remain unexercised on a production import | Proposed -> Approved (user's Phase 1 prerequisite request, 2026-10-29) -> Applied -> Verified (CLI version output) | No design changes.
