# Size, stackup and provisional order plan

Checked **2026-10-30**. Analysis only; no quote submission, upload, order, frame or stackup change. Original PCB files independently confirm the user's layer counts. Measurements: [parsed inputs](COST_AND_NET_INPUTS.json), [full stackups](STACKUPS_TEXT.json).

## Per-design comparison

| Design | Length × width mm | Copper layers | Source thickness / stackup sum mm | Order thickness intent | Fabrication-only size range for this thickness/layers | Standard assembly single-board range | Result |
|---|---|---:|---:|---:|---|---|---|
|11x3|260.7 ×66.0|4|1.600 /1.600|1.6|3×3 to663×593|70×70 to460×500|Fab size passes; assembly width66<70. Length260.7 passes single-board maximum, exceeds published250 mm panel maximum.|
|8x3|189.6 ×66.0|2|0.582 /0.582|nominal0.6|3×3 to599×497 at nominal0.6*|70×70 to460×500|Fab capability-table size passes*; assembly width66<70.|
|3x8|176.0 ×71.1|2|0.582 /0.582|nominal0.6|3×3 to599×497 at nominal0.6*|70×70 to460×500|Size passes tables*; handling rails still required.|
|8x8|189.6 ×176.0|2|0.582 /0.582|nominal0.6|3×3 to599×497 at nominal0.6*|70×70 to460×500|Size passes tables*; handling rails still required.|

[Fabrication capabilities](https://jlcpcb.com/capabilities/pcb-capabilities), checked2026-10-30:0.6 mm offered, tolerance±0.1 mm;1.6 mm±10% (1.44–1.76). Exact0.582 is below the0.6 threshold for published minimum dimensions and would need manual review; use approved nominal0.6 intent without editing CAD. ***Conflict:** [quote-form help](https://cart.jlcpcb.com/quote/?fromDemo=yes), checked same date, restricts0.6 mm to100×100 and excludes4-layer; all three thin tiles exceed100 mm. Exact-size0.6 acceptance remains **UNVERIFIED**, pending user's instant-quote check. This conflict does not apply to1.6 mm11x3.

[Standard assembly capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), checked2026-10-30:1–32 layers, no separate thickness limit, rails/fiducials required, panels70×70 to250×250. Thus0.6 is not prohibited by the assembly thickness table, but fabrication acceptance is unresolved. Exact thin-board warpage limits/fixture acceptance at these dimensions were not established. No thickness increase is assumed.

**Stackups, top→bottom (mm):**11x3 mask.010 /Cu.035 /core.492 /In1Cu.017 /prepreg.492 /In2Cu.017 /core.492 /Cu.035 /mask.010 =1.600. Each other tile:mask.010 /Cu.035 /core.492 /Cu.035 /mask.010 =.582. **11x3 is1.018 mm thicker in the source;1.0 mm thicker than nominal0.6 ordering intent.** Copper finish field is `None` in all source stackups; it does not establish an author's ordering finish. Exact vendor dielectric construction is not yet agreed; nothing changed.

## JLC-provided undersize handling options

| Official option | Finished outline impact | Application here |
|---|---|---|
| **Panel by JLCPCB**, duplicate same design in rows/columns, default5 mm edge | Adds removable material; intended finished tile outline retained, subject to depanel tolerance | Potential8x3 solution; vendor must confirm thin-board route. No panel designed here. |
| Assembly's suggested panel; **“Pls help me make the panel”** | V-cut/mouse-bite/bridge connections are removed; nominal outline retained, with scoring tolerance or tab remnants to review | Ask vendor for handling of66 mm width;11x3 exceeds published panel limit, so not an automatically valid workaround. |
| Fabrication-only, user assembly | Original outline retained; no JLC SMT preview/assembly service | Fallback if JLC rejects Standard handling, requiring user's scope decision. |

Sources: [Panel by JLCPCB](https://jlcpcb.com/help/article/how-do-i-order-a-panel), [assembly panel assistance](https://jlcpcb.com/help/article/panelizing-your-pcb-for-assembly), checked2026-10-30. Panel order quantity counts **panels**, not finished tiles. These services do not authorize permanent outline enlargement; any proposed finished-outline change needs separate approval. Mixed-layer/thickness tiles are separate jobs, not a proposed combined panel.

## Quantities — conditional on provisional tile mix

The author-specific tile/order instructions were **not located**; [search record](ORDER_INSTRUCTIONS_SEARCH.md). User provisionally confirmed1×11x3,1×8x3,2×3x8,4×8x8. Do not call these author instructions.

[Quote form](https://cart.jlcpcb.com/quote/?fromDemo=yes) currently offers fabrication5,10,15… and rejects custom3/8; Standard assembly table minimum2. The following is a **single-tile ordering calculation**, not a validated checkout configuration. Manufacturer panelization changes quantities and must be recalculated.

| Design | Tiles needed:1 board | Fabricate / assemble target:1 board | Tiles needed:2 boards | Fabricate / assemble target:2 boards |
|---|---:|---|---:|---|
|11x3|1|5 /2|2|5 /2|
|8x3|1|5 /2|2|5 /2|
|3x8|2|5 /2|4|5 /4|
|8x8|4|5 /4|8|10 /8|

These meet the published MOQ floors. Availability of the exact partial-assembly quantities4/8 in the final service configuration remains UNVERIFIED; if checkout requires another increment, round assembly up to the next permitted value. **Prototype first:**8x3 only; target5 fabricated/2 assembled, subject to accepted handling. No other designs ordered now. Bare-only alternative minimum5/design.

## BOM totals and cost impact

| Design | All components | Hand | SMT candidates incl undecided LEDs | SMT sides after hand exclusions | Unique SMT procurement groups | Known Extended groups, excluding/including chosen LED* |
|---|---:|---:|---:|---|---:|---|
|11x3|165|33|132|Front+back|11|6 /7|
|8x3|114|19|95|Front+back|8|3 /4|
|3x8|89|15|74|Front+back|4|2 /3|
|8x8|214|22|192|Front only|3|1 /2|
|One complete board, conditional mix|1313|170|1143|As above|13 shared SMT groups|7 /8 unique across family|
|Two complete boards, conditional mix|2626|340|2286|As above|13 shared SMT groups|7 /8 unique across family|

Counts exclude mechanical holes and external ESP32/Raspberry Pi modules; include361 LEDs+361 sensors per complete board. [Full20-row source BOM](BOM_TOTALS.md). After combining equivalent330 Ω groups BOM-12/19,19 procurement groups total (13 SMT+6 hand), **not19 approved exact MPNs**. Source groups remain traceable. *Extended counts assume C17930 proposed for both330 Ω groups and the existing dated candidates retained; BOM-19 approval only covers8x3, so11x3 reuse needs its own BOM-ID approval. LED undecided; decoder class/supply unresolved. Final purchased unique/Extended count remains UNVERIFIED.

Known Extended candidates:AH49ENTR-G1/C314698,MMBT3906LT1G/C53444,SN74LV1T34DBVR/C100024,220 Ω/C17957,1000 µF/C51953415,74HC4052D/C11350,proposed330 Ω/C17930; chosen LED adds one. [Dated candidate sources](../phase3/BOM_SOURCING.md). **No verified in-library drop-in for8x3 SN74HCT138NSR**;11x3 CD74HCT154M96 availability/class unresolved. All unmatched/Extended candidates still require decisions. “Extended candidate” does not establish that no alternate Basic part exists.

With those conditional selections and separate tile orders, Extended feeder contributions are11x3 $10.71,8x3 $6.12,3x8 $4.59,8x8 $3.06 = **$24.48 across four jobs**. Counting8 family-unique types once would undercount. Standard charges Basic feeders too; Extended-vs-Basic premium is$0. Same type count applies for1 or2 boards if one job per design.

### Partial prototype cost estimate — two assembled tiles per separate job

| Design | SMD pads per tile | Setup+stencil+minimum handling+all candidate feeders+placement | With published small-batch fixture, packing base, placement confirmation and single-board surcharge allowances |
|---|---:|---:|---:|
|11x3|401|$100.58|about **$119 + PCB + parts + shipping/tax**|
|8x3|286|$95.63|about **$114 + PCB + parts + shipping/tax**|
|3x8|234|$89.34|about **$108 + PCB + parts + shipping/tax**|
|8x8|576|$55.13|about **$73 + PCB + parts + shipping/tax**|

**These are service-only estimates, not total order quotes.** Candidate types11/8/4/3 and all SMT pads included; unresolved parts may change them. [Fee schedule](https://jlcpcb.com/help/article/pcb-assembly-price), updatedOct22, checkedOct30:double/single setup51.12/25.56;stencil16.42/8.21;handling≥14.93;feeders1.53/type;placement.0016/joint. Allowances:fixture16.42,packing≥.50,confirmation.45,single-board surcharge.48×2. Excludes panel-specific charges, optional storage, increased handling, losses/spares and any inspection costs. No fabrication or complete component price has been verified; therefore a reliable **all-in estimate remains UNVERIFIED**. Quote needs final LED/decoder, finish, accepted thickness and handling. No invented$2 fabrication assumption.

Needs from you: retain the provisional quantity plan until the author's instruction location is supplied; vendor quote acceptance and full prices remain needed before release.
