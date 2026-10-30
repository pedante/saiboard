> **2026-10-30 current update:** BOM-05/09 approved (identity manifest only); BOM-19 C17930 proposed; Decision02 LED sheet ready, waiting before import. CHG-012 PARKED accepted. All-four identity/geometry check passes; Hall SKU fields uniformly blank. 11x3=4layers/1.6mm, others2layers/.582mm nominal.6.8x8 SMT front-only after hand exclusions. See [size/order plan](SIZE_ORDER_PLAN.md), [LED sheet](DECISION_02_LEDS.md) and [author search](ORDER_INSTRUCTIONS_SEARCH.md). These supersede any older blanket layer/thickness/assembly-side statement below.

# Current scope — supersedes Phase3 qualification gates

2026-10-29. Prototype8x3 first, all four designs eventually. Original circuit and footprints accepted as proven. Reopen only for JLCPCB DFM/placement/part-match flags or unavailable parts. LED drawing comparison remains an explicit user requirement. No uploads, orders, firmware edits or source edits. Stop at each decision sheet.

## MUST

- CHG-009: **Approved → Applied → Verified**.8x3 R1–R8 Value only,330 Ω; instance Value cache synchronized. Pre-change baseline preserved in02_work/baseline_before_CHG009. Parsed-tree reversal proves no other change; native ERC/DRC completed on audit copies. Approval2026-10-29.
- CHG-014: generic passives only; first [BOM-ID decision sheet](DECISION_01_PASSIVES.md) ready. No new component assignments yet. Unavailable/Extended candidate decisions are sourcing requirements, not permission to redesign.
- CHG-016: **Approved → Applied → Verified population policy**,2026-10-29. Exact89 one-of-each hand references recorded in02_work/ASSEMBLY_POPULATION.json; future assembly BOM/CPL both exclude them.95 JLC candidates/19 hand parts on8x3; LEDs held. Actual exported file verification remains later.
- CHG-023/004: next LED one-page comparison and user identity decision. Provisional CAD identity retained; no LED assigned to ordering BOM. CHG-004 remains Applied-provisional. Original/RGBW status and drawing fit must be evaluated under the user's decision rule.
- CHG-020: after decisions, prepare baseline for user GUI import; verify via MCP. Previously approved fallback retained.
- CHG-021: generate and check files and matching assembly population, then prepare minimum prototype order settings and user-operated preview checklist. No ordering.
- CHG-018: retain user nominal0.6mm intent; exact manufacture options are checked in manufacturer workflow. Prior paper-analysis conflict is recorded, not a new qualification programme.
- Tile population evidence and per-tile/board counts: [BOM totals](BOM_TOTALS.md). Full-board counts conditional until documented quantity or user confirmation closes the gap.

## CHEAP

- CHG-007/008: no8x3 zones, so not applicable now. Optional11x3 setting/refill attempt later; skip if unrelated copper changes. No frame work.
- CHG-012: quick proof attempt completed from existing exact-part evidence; not established in one unambiguous SOT-223 page. Skip modification and PARK advisory below.
- Reference exclusions: preserve20 existing mechanical BOM/CPL exclusion flags; check actual exports.

## PARK — one-line prototype advisories, non-blocking

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

## 11x3 current size check

[JLCPCB assembly capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), checked2026-10-29: Standard single-board maximum460×500mm, minimum70×70mm; panel table maximum250×250mm. Its FAQ allows possible oversized-panel review rather than an absolute rejection.

The **260.7mm length is within the single-board maximum**, but exceeds the panel table by10.7mm. The **66mm width is below the Standard single-board minimum**;8x3 shares this width issue. Therefore length alone does not disqualify11x3, and bare-outline acceptance cannot be assumed. Fallback options for the later manufacturer workflow: request an accepted single-board handling/fixture arrangement preserving the outline; request oversized-panel acceptance if required; or fabricate bare11x3 and hand-assemble if automated assembly is declined. All require user decisions/manufacturer acceptance; no frame is designed or manufacturer message sent.

Standard publishes an assembly order range starting at2 pieces. Plan for2 assembled8x3 prototypes provisionally; actual PCB fabrication quantity, exact-size acceptance, available parts and minimum checkout combination must be verified in the later user-operated workflow. No quote or purchase submitted.

Needs from you: decide the first passive sheet before the LED sheet/import preparation.
