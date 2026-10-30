# Shared LED and Hall identities/lands

Read-only,2026-10-30. [Every instance and full normalized pad check](IDENTITY_GEOMETRY_FULL_CHECK.json); [summary](SHARED_PARTS_SUMMARY.json). Footprint placement/rotation removed for comparison; local pad position, angle, shape, size, layer set and pin metadata retained. Net names/UUIDs excluded because they vary by circuit position.

| Part |11x3|8x3|3x8|8x8|Total / identity variants / land variants |
|---|---:|---:|---:|---:|---|
|LED|33|24|24|64|145 /1 /1|
|Hall sensor|33|24|24|64|145 /1 /1|

**No cross-module deviations found** in schematic/PCB Value, Footprint, Manufacturer, MPN or LCSC properties, or normalized lands. LED fields everywhere:Value/MPN SKC6812RGBW-WS,Manufacturer OPSCO Optoelectronics,LCSC C5378724,footprint `LED_SMD:LED_SK6812_PLCC4_5.0x5.0mm_P3.2mm`. These are provisional CHG-004 fields, not an approved procurement assignment.

Hall fields everywhere:Value AH49E,footprint `Package_TO_SOT_SMD:SOT-23`; Manufacturer/MPN/LCSC **absent on every instance**. Uniform blanks establish consistency, **not a verified common purchasable part**. Future selection must assign one approved sensor SKU to all modules. No sensor identity was assigned this turn.

One retained Hall land analysis:pad1(-1,-.95),pad2(-1,.95),pad3(1,0),all.9×.8 mm rectangles onF.Cu/F.Paste/F.Mask. One LED land analysis is in [Decision02](DECISION_02_LEDS.md), applied to all145 instances. No per-tile duplication of physical qualification work. The existing ledger uses CHG-011 for Hall sensors and CHG-015 for transistor/buffer lands. This shared LED/Hall comparison implements the requested consolidation without silently renumbering those entries. Both parked qualifications stay PARK; the transistor/buffer advisory is unchanged.

The original family has145 SK6812 LEDs; CHG-004 covers all145 (D1–33,D1–24,D1–24,D1–64). No original LED instance is omitted. Conditional complete-board totals are361 LEDs and361 Hall sensors. One SKU per family is mandatory; failure of a selected LED on any tile excludes it for all four. No mixed RGB/RGBW fallback.

Needs from you: LED decision; sensor procurement selection remains common to the complete family.
