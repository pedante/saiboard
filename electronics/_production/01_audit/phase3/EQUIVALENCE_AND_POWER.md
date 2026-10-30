# Phase 3 equivalence and power assessment

Checked 2026-10-29. Analysis only. No replacement below is released for assembly. Original manufacturer/orderable suffixes and ratings that are missing stay **UNVERIFIED**. Sources supplied with the project are preserved in `02_work/baseline/datasheets/`; extracted text is in `../phase2/datasheet_text/`. Measured retained lands are in `../phase2/FOOTPRINT_VARIANTS.json`. The [full sourcing worksheet](BOM_SOURCING.md) links official part identities, classifications and dated stock observations.

## CHG-004: result and package comparison

**Result: equivalence has NOT passed. Status stays Applied-provisional; downstream reliance is blocked.** Pin mapping agrees and nominal contacts overlap the retained pads, but the manufacturer's recommended lands are different. Tolerance/joint acceptance, maximum current and system electrical suitability remain unresolved. The 32-bit format also differs from the supplied original 24-bit document. Recommend holding CHG-004 and revising/rejecting it through the explicit decision in CHG-023; do not silently roll it back.

Original evidence: `SK6812.pdf`, LED COLOR, SPC/SK6812 Rev.01, supplied with the originals. Exact historically purchased SKU is unknown. Candidate evidence: supplied `OPSCO_SKC6812RGBW_RevB1_2025-07-31.pdf`, 18 pages, in the unverified update folder. Its identity link was checked through the [current LCSC datasheet viewer](https://www.lcsc.com/datasheet/C5378724.pdf), which points to [this OPSCO PDF](https://datasheet.lcsc.com/datasheet/pdf/f73fcb028ddf7140b2dbd34804e8ce40.pdf?productCode=C5378724). Direct re-download returned HTTP403; current-file byte identity is UNVERIFIED. Relevant supplied pages 5, 7, 8, 9 and 10 were rendered in `images/` and inspected. Current listing: [C5378724](https://jlcpcb.com/partdetail/SKC6812RGBW-WS/C5378724).

| Property | Original document / retained design | OPSCO candidate | Assessment |
| --- | --- | --- | --- |
| Identity | `SK6812`; actual purchased manufacturer/suffix unknown | `SKC6812RGBW-WS`, C5378724, warm-white family; several bin suffixes in PDF | Short catalog name does not resolve the exact WS bin/suffix |
| Format | 24-bit GRB, MSB first | 32-bit GRBW, MSB first | Firmware serialization and chain alignment must change if firmware uses original format; flag only, code not inspected/edited |
| Supply | Original text is internally awkward: electrical conditions mention 4.5–5.5 V, VDD typical 5.2 V; board P is intended 5 V by README | PDF 3.7–5.5 V; product listing says 3.5–5.5 V | Use stricter PDF minimum pending supplier resolution; actual voltage-drop margin unverified |
| Logic | Original VIH/VIL 3.4/1.6 V are typical thresholds, not guaranteed limits | VIH min 0.65 VDD; VIL max 0.35 VDD | At 5 V: 3.25/1.75 V. Direct 3.3 V logic has little guaranteed margin; existing UI3 level translator is on the 5 V rail |
| Data timing | T0H 0.30 ±0.15 us; T1H 0.60 ±0.15 us; T0L 0.90 ±0.15 us; T1L 0.60 ±0.15 us; reset 80 us | T0H 0.25–0.40 us; T1H 0.65–1.0 us; T0L ≥0.8 us; T1L ≥0.2 us; period ≥1.2 us; reset >200 us, low intervals <20 us outside reset | Timing ranges are not identical. Existing firmware compatibility is UNVERIFIED |
| Full-channel current | Original document gives DOUT drive currents, which are **not LED-channel current ratings**; LED maximum unavailable | R/G/B 8 mA typical each, W 16.5 mA typical; IC quiescent 0.29 mA typical; maximum cells blank | Guaranteed worst case cannot be calculated from this datasheet |
| Pin 1 / 2 / 3 / 4 | VSS / DIN / VDD / DOUT | GND / DIN / VDD / DOUT | Matches all 145 retained pad/net mappings |
| Package | Retained footprint name PLCC4 5×5, 3.2 mm vertical pad-center pitch | Actual drawing: body 4.8×4.85 mm, lead span 5.0 mm, height 1.6 mm; unspecified tolerances ±0.1 mm | Actual drawing, not the generic “5050” name, used below |
| Copper lands | Each 1.50×1.00 mm; centers x=±2.45, y=±1.60 mm | Recommended 1.80×1.20 mm; centers x=±2.55, y=±1.60 mm | Pad area 1.50 vs 2.16 mm²: retained land is 30.6% smaller; geometry is not identical |
| Nominal bottom contact | Right retained copper x=1.70…3.20, y=1.10…2.10 mm | Nominal contact x=1.70…2.50, y=1.15…2.05 mm, mirrored at other corners | Nominal overlap is complete, but inner heel margin is zero; no tolerance/placement allowance established |
| Assembly conditions | Original part/reflow moisture class unknown | PDF MSL5a versus JLC listing MSL3; JLC marks assembly difficulty High | Exact lot moisture/reflow handling needs resolution; do not treat listing as overriding datasheet |

The candidate recommended right land spans x=1.65…3.45 and y=1.0…2.2 mm. Relative to it, retained copper lacks 0.05 mm at the inner edge, 0.25 mm at the outer edge and 0.10 mm per vertical edge. This comparison does **not** prove solder failure; it does prevent claiming a verified drop-in under the user's condition. Any enlargement is a copper geometry change needing approval and new DRC/clearance checks, including all 145 instances. No geometry was changed.

Same-name priority was also checked: [OPSCO SK6812 C5378720](https://www.lcsc.com/product-detail/C5378720.html) exists. It is a lead for an RGB-preserving revision, not evidence that it is the historically fitted LED COLOR device or a qualified substitute. Live JLC stock, exact current/package/protocol equivalence and bin remain UNVERIFIED. No further part was assigned.

## LED totals and power gate

All original LEDs are covered: 11x3 D1–D33 (33), 8x3 D1–D24 (24), 3x8 D1–D24 (24), 8x8 D1–D64 (64): **145**, none omitted. One-of-each quantities are not full-board multiplicities. Electronics README states a 19×19 array, and `board/cnc_files/top.dxf` contains 361 circles; exact PCB interconnection/multiplicity remains unconfirmed.

Illustrative datasheet-typical full RGBW input current per LED is `(3×8 + 16.5 + 0.29) mA = 40.79 mA`. The quiescent value is added as a budgeting approximation; it is not a manufacturer-specified total maximum.

| Design / population | LEDs | Typical full RGBW budget | At nominal 5 V | Guaranteed worst case |
| --- | ---: | ---: | ---: | --- |
| 11x3 | 33 | 1.34607 A | 6.73035 W | UNVERIFIED |
| 8x3 | 24 | 0.97896 A | 4.89480 W | UNVERIFIED |
| 3x8 | 24 | 0.97896 A | 4.89480 W | UNVERIFIED |
| 8x8 | 64 | 2.61056 A | 13.05280 W | UNVERIFIED |
| One of each | 145 | 5.91455 A | 29.57275 W | UNVERIFIED |
| README full 19×19 array | 361 | **14.72519 A** | **73.62595 W** | UNVERIFIED |

Repository `electronics/README.md` calls for **5 V, 10 A, 50 W**. This is a documented intended rating, not verification of the user's actual supply or its transient behavior. The 361-pixel full-RGBW typical estimate alone exceeds that rating by 4.725 A / 23.626 W, before Hall sensors, ESP32, Raspberry Pi or losses. Consequently suitability at the requested all-channel-full condition cannot be signed off. No brightness cap, power-supply upgrade, reroute or firmware limitation is assumed or implemented. A 145-pixel one-of-each bench population is a different load and does not validate the full board.

**Traces:** source outer copper is 0.035 mm, inner 11x3 copper 0.017 mm. [Power track measurements](POWER_TRACK_WIDTHS.json) show all two-layer P/GND track segments at 0.5 mm; 11x3 additionally has 1.2/3/4 mm trunks and inner P/GND zones. EasyEDA's read-only engineering tool estimates 0.5 mm, 1 oz outer copper at **1.447 A for +10°C**, or **1.963 A for +20°C**; 1.2/3/4 mm at +10°C gives 2.730/5.304/6.534 A. See [tool results and caveats](TRACE_CURRENT_ESTIMATES.json). These are IPC-2221 estimates, not certified ratings; no allowable rise has been chosen. Comparing whole-module current to every branch would be incorrect. If one 0.5 mm branch carried the entire 8x8 load, 2.611 A exceeds both illustrative estimates. Actual splits through parallel tracks, zones, vias and inter-board headers need a verified power-distribution map and thermal/voltage-drop check. Stored fills and global minimum width cannot establish path capacity. **No pass is claimed for any design.**

**Connectors:** all generic header/socket exact MPNs/current derating remain unknown. A 3 A or 5.2 A listing for an unqualified search lead cannot be assigned to retained connectors. The [WAGO 2061-602/998-404 drawing](https://pimassetsprdst.blob.core.windows.net/assets/apc_Original/11/51/130811151.pdf), version 2026-01-08, identifies 6 mm pitch, two solder feet per potential, 11.7×15.8×5.6 mm body. [LCSC-hosted WAGO datasheet](https://atta.szlcsc.com/upload/public/pdf/source/20210406/C2765058_42F16AD0A4D4755D149E55C8B45DF4E1.pdf) gives 17.5 A IEC / 10 A UL ratings with specified conductor sizes. Do not treat 17.5 A as an unconditional assembled-board rating. A single 10 A-rated input path would not support the 361-pixel typical full-white budget. Actual part/wire/temperature/routing/load division are UNVERIFIED.

## 8x3 R1–R8 investigation

User response remains a placeholder; neither “unknown” nor a value has been confirmed. Analysis below is evidence for a choice, not a value assignment.

All eight are **PNP Hall-bank base resistors**. Rn.1 connects UI1 Y(n−1), Rn.2 connects Qn.1 base; Qn.2 emitter is P3.3 from UI2.2, and Qn.3 collector is PQn. Each PQn powers three local AH49E VCC pins and reaches inter-board connectors. Decoder UI1 output pins for R1…R8 are 15,14,13,12,11,10,9,7. The [native nets](NATIVE_POWER_AND_RESISTOR_NETS.json) preserve every connector/sensor reference. In 11x3, R1…R11 serve the same function and literally read `330`. 3x8/8x8 have no equivalent transistor/base-resistor bank.

Historical 8x3 bottom silk contains R1…R8 reference strokes and component attributes, not an encoded component-value field; no Fab/assembly drawing was found in historical Gerbers. Source resistor Value is `R` on B.Fab, not a resistance printed on the exported silk. Numerical “330” substrings in Gerber coordinates are not resistor markings. Electronics/board README has no resistor specification. Thus history provides **no independent value confirmation**; its electrical revision remains UNVERIFIED.

`Ibase = (3.3 − VBE − VOL)/R`. Supplied MMBT3906 data gives VBE(sat) 0.65–0.85 V at Ic=10 mA/Ib=1 mA and max 0.95 V at Ic=50 mA/Ib=5 mA. [TI HCT138 datasheet](https://www.ti.com/lit/ds/symlink/sn74hct138.pdf) gives VOL max 0.33 V at IOL=4 mA over the SN74 temperature range. Using 0.95 V and 0.33 V solely as an illustration gives:

| Candidate | Illustrative Ibase | Illustrative resistor dissipation | Assessment |
| --- | ---: | ---: | --- |
| 330 Ω | 2.02/330 = 6.12 mA | 2.02²/330 = 12.36 mW | Supported by equivalent 11x3 value; driver loading still needs validation |
| 0.33 Ω | Idealized 6.12 A | Idealized 12.36 W | Not a plausible intended logic-driver base resistor; real driver would limit/sag and the assumed VOL would fail |

The 6.12 mA estimate is already outside the decoder's 4 mA guaranteed output test condition; it is **not a guaranteed operating point**. A nominal VBE=0.7/VOL=0.2 scenario gives 7.27 mA and 17.45 mW for 330 Ω. These assumed voltages are illustrative, not new verified part limits. Local three-sensor load is 13.5 mA using the sensor's 4.5 mA maximum at its specified 5 V test condition; a 19-sensor column would be 85.5 mA under that same conditional calculation. Actual 3.3 V load/scan distribution and saturation margin are not established. Do not infer saturation from hFE measured at VCE=1 V.

**Recommendation: ask the user to choose 330 Ω**, based on topology and the 11x3 source. Keep PCB `R` unset and schematic `R330` unresolved until then. Driver current and minimum switched sensor voltage remain a separate MAJOR check even after the choice. No 1 kΩ redesign, altered transistor, or firmware scan change is proposed as an automatic fix.

## Other mandatory component comparisons

| Group | Original evidence | Candidate / side-by-side differences | Fit, electrical and firmware result |
| --- | --- | --- | --- |
| C104, 153 pcs | Source literal C104, 1206; capacitance interpretation, tolerance, voltage and dielectric not explicitly stated | C24497: 100 nF, ±10%, 50 V, X7R, 1206 | Proposed specification, not proof of original equivalence. Exact terminal/dimension drawing not retrieved (HTTP403); no new footprint. No firmware effect |
| C106, 4 pcs | Literal C106, 1206; ratings/dielectric absent | C13585: 10 uF, ±10%, 50 V, X5R, 1206 | DC-bias effective capacitance and regulator output-capacitor stability UNVERIFIED; do not assume any 1206 MLCC is equivalent |
| R330/330/220 | Values as above; 1206; original tolerance, voltage and wattage absent | C17930 330 Ω and C17957 220 Ω: ±1%, 250 mW, 200 V, thick film, 1206 | Nominal size/value candidates; exact terminal geometry and original ratings unverified. Original 330/220 retained, ambiguous 8x3 needs choice |
| CP1 | 1000 uF, 10×10.5 mm footprint; voltage/tolerance/ESR/ripple absent | C51953415: 1000 uF ±20%, 16 V, D10×10.5 mm, 347 mA at 120 Hz, 2000 h/105°C | Terminal drawing, polarity marking, ripple/ESR suitability unavailable; not yet a qualified fit |
| AH49E, 145 pcs | Supplied BCD AH49E Rev1.3; linear analog sensor, 3–6.5 V; 1 VCC/2 OUT/3 GND | Diodes AH49ENTR-G1 C314698, SOT-23; [manufacturer datasheet](https://www.diodes.com/assets/Datasheets/AH49E.pdf): same pin functions and sensor family | At 5 V: sensitivity 1.1/1.6/2.1 mV/G min/typ/max, quiescent output 2.25/2.5/2.75 V, supply current 3.5 typ/4.5 max mA. Analog bipolar response, no digital operate/release thresholds. SOT-23 magnetic polarity differs from TO-92 drawing; preserve SOT orientation. Current 3.6 mm land span vs retained 2.9 mm and opposing pad centers 2.6 vs 2.0 mm requires joint review. 3.3 V sensitivity/rail margin and actual field orientation verification pending; no calibration/software changes |
| Q1… | Symbol 2N3906, SOT-23; supplied MMBT3906 document, not a TO-92 purchasing record | onsemi MMBT3906LT1G C53444, [datasheet](https://www.onsemi.com/download/data-sheet/pdf/mmbt3906lt1-d.pdf): PNP, 40 V VCEO, 200 mA Ic, 5 V VEBO, 225 mW on specified FR-5 test board; pin1 B/2 E/3 C | Function/pin order agrees; retained 11x3 pads 0.9×0.8 / 2.0 mm row spacing, 8x3 pads 1.475×0.6 / 1.875 mm. Supplied suggested pattern about 2.2 mm rows; different land variants need separate fit checks. Do not infer usable current from absolute maximum |
| UI3 | SN74LV1T34, 5 V VCC, 3.3 V-named input; pin1 NC/2 A/3 GND/4 Y/5 VCC | TI SN74LV1T34DBVR C100024; [datasheet](https://www.ti.com/lit/ds/symlink/sn74lv1t34.pdf), 1.6–5.5 V operation, TTL-compatible input at 5 V, ±8 mA output-drive class | Same functional part; 1.325×0.6 mm retained pads / 2.275 mm row spacing vs TI example 1.1×0.6 / 2.6 mm. Fit and exact loaded VOH to LED VIH margin remain unverified. No topology change |
| 11x3 UI1 | 74HCT154D label, supplied TI HCT154 family data, 5 V P rail; 24-pin wide SOP | TI CD74HCT154M96 C2653299; [datasheet](https://www.ti.com/lit/ds/symlink/cd74hct154.pdf), 4.5–5.5 V HCT, VIH≥2/VIL≤0.8 V, ±4 mA drive, SOIC24 DW | Pin map 1–11=Y0…Y10,12 GND,13–17=Y11…Y15,18/19 enables,20–23=A3…A0,24 VCC agrees. Retained 1.27 pitch wide body nominal 7.5×15.4; availability/joint proof and PNP drive remain open. HC variant is not an automatic substitute |
| 3x8 UI1 | 74hc4052D, SO16 3.9×9.9, pin16 on P and 6/7/8 GND | Nexperia 74HC4052D,653 C11350; [datasheet](https://assets.nexperia.com/documents/data-sheet/74HC_HCT4052.pdf), 2–10 V family supply, analog 2×4 mux, Ron typ80 Ω at 4.5 V; same package/function | Complete source pin map matches supplied datasheet. HC control VIH 3.15 V at VCC4.5 and 4.2 V at VCC6; guaranteed 5 V operation from nominal 3.3 V S0/S1 is not established. Exact external driver VOH/interconnect needs checking; no unapproved HCT swap |
| Generic connectors | Pitch/count from source only; no original manufacturer/current/contact plating/reflow/mating data | C6302166/C6685390 are library search leads; JLC tags wave solder despite SMT names. C46061767 (female3), C2997407 (XH male3), C668622 (XH male2, catalog2.5 pitch) also surfaced | None is established as a drop-in. XH mating bodies and 2.5 vs2.54 pitch cannot be ignored. Do not transfer their ratings to originals. Propose DNP-for-assembly and hand-fit/solder subject to exact part selection |

Passive official datasheet entry points: [C24497](https://www.lcsc.com/datasheet/C24497.pdf), [C13585](https://www.lcsc.com/datasheet/C13585.pdf), [C17930](https://www.lcsc.com/datasheet/C17930.pdf), [C17957](https://jlcpcb.com/partdetail/18645-1206W4F2200T5E/C17957), [C51953415](https://jlcpcb.com/partdetail/jieerrui-RVT16V1000M10X10/C51953415). Entry links do not imply the actual terminal drawing was obtained. Missing drawings stay UNVERIFIED.

## Decoder package resolution options (8x3/UI1)

| Option | Datasheet / package evidence | Availability | Recommendation |
| --- | --- | --- | --- |
| A: TI SN74HCT138NSR, retain footprint | Downloaded current TI PDF, NS0016A drawing pp25–26 visually checked: body 5.2–5.4×10.0–10.4 mm; 1.27 pitch; recommended pads 1.85×0.6, rows7.0 mm. Retained 1.975×0.6, rows6.925: retained x=2.475…4.45 covers recommended2.575…4.425 on each side; y/pitch agree | No verified JLC/LCSC listing/number/stock found; sourcing/consigned-service acceptance UNVERIFIED | **First geometry-compatible candidate. Prefer qualifying supply before approving layout work.** TI front-page NS body length says6.2 mm, inconsistent with actual NS0016A drawing; use actual drawing and flag discrepancy |
| B: TI SN74HCT138DR C352958 | Same 1–16 logic pinout, 4.5–5.5 V, ±4 mA; D package3.9×9.9 mm, different lead span from existing wide footprint | LCSC listing found, indexed6,783; JLC availability/class unverified | Footprint/copper change required; only if A cannot be sourced and individually approved |
| C: Nexperia 74HCT138D,653 C5965 or Wuxi AIP74HCT138SA.TB C2974588 | [Nexperia](https://www.nexperia.com/products/analog-logic-ics/logic/decoders-and-demultiplexers-digital-multiplexers/decoders-demultiplexers/serie/74hc138-74hct138) SO16 body3.9; [Wuxi manufacturer sheet](https://datasheet.lcsc.com/datasheet/pdf/ba1c629741cd877c49282d49b583f681.pdf?productCode=C2943288) explicitly lists HCT138SA body10.0×3.9, pitch1.27 | LCSC low indexed stock19 /55 (another Wuxi category100); JLC allocation unverified | Neither resolves wide-package fit; not selected ahead of A |

HCT138 pin map is 1=A0,2=A1,3=A2,4/5 active-low enables,6 active-high enable,7=Y7,8=GND,9…15=Y6…Y0,16=VCC. Source mapping agrees. An HCT238 changes output polarity; an HC138 changes logic thresholds. Neither is an approved equivalent.

## Regulator tab resolution options (11x3/UI2, 8x3/UI2)

Same part priority: retain **AMS1117-3.3 C6186**, Basic listing. Source pin1 GND,2 P3.3,3 P; copper pad4 is netless. [Exact C6186 datasheet](https://datasheet.lcsc.com/datasheet/pdf/e6935943fc6b1bbf350a1a0f3e90dc4a.pdf?productCode=C6186), checked via current LCSC entry, specifies the three pins, 1 A headline current, dropout up to1.3 V under its stated conditions, 15 V absolute input limit, SOT223 and thermal dependence. Its explicit tab-output annotation is beside TO-252; SOT223 tab identity is not unambiguously labelled there. A LCSC FAQ says SOT223 tab=pin2, but that explanatory text is not a substitute for the requested manufacturer package proof. **Exact SOT223 tab confirmation remains UNVERIFIED.**

Option A (recommended after that proof): renumber the existing copper tab **pad4→pad2**, matching the same physical output pin, and assign P3.3. Keep pad size/position, tracks and zones unchanged. This is a footprint pin/net-model change, not a requested new thermal pour. Check duplicate-pad semantics and all source/netlist/DRC results; any required new copper becomes a separate proposal.

Option B: add an explicit tab pin4 to a local three-plus-tab symbol, electrically tied to output, and retain PCB pad4 numbered4 with P3.3. Same available C6186; larger library/schematic change and possible native connectivity consequences. No automatic wiring or pad renumbering is approved.

Option C: leave current isolated copper land and record a justified model exception only after supplier/package proof and assembly/thermal acceptance. This does not make the tab physically isolated: the package may connect it internally. It must never be treated as arbitrary no-net metal. Do not assign it GND.

Output-capacitor stability is a separate MAJOR issue: source output C106 is an unspecified 1206 part, proposed10uF MLCC. AMS documentation guarantees its stated general stability using22uF solid tantalum and says smaller capacitance can work under conditions; it does not establish the selected10uF X5R/DC-bias/ESR combination here. No assertion of actual oscillation is made. Confirm suitability through manufacturer evidence and load/transient validation before assigning the candidate; any capacitor/topology change needs its own approval. At nominal5→3.3 V, regulator dissipation is approximately1.7×Iload plus quiescent losses; source thermal copper and real maximum load are not sufficiently characterized to accept the headline1 A.

Needs from you: R1–R8 choice, LED disposition and individual CHG decisions; electrical suitability remains blocked where marked UNVERIFIED.
