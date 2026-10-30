# Decision 01 — 8x3 generic passives

Updated **2026-10-30**. BOM-05 and BOM-09 APPROVED; BOM-19 selection still requires approval. CHG-014 records identities in [approved manifest](../../02_work/APPROVED_BOM_IDENTITIES.json). CAD assignment remains pending; no Value or footprint edits this turn.

**BOM-09 connections first:** CI2 connects GND (pad1) to P (pad2), the UI2 input rail (UI2 pad3). CI4 connects GND (pad1) to P3.3 (pad2), the UI2 output rail (UI2 pad2). Both retain Value **C106**. CI4 is the regulator output capacitor. **Prototype bench note: scope the 3.3 V rail under load. CHG-027 stays PARKED; no design change.** [Net evidence](COST_AND_NET_INPUTS.json).

| BOM-ID | References / quantity | Approved identity | Verified specifications / class | Stock count |
|---|---|---|---|---|
| BOM-05 | C1–C24, CI1, CI3, CI5 /27 | Samsung CL31B104KBCNNNC / **C24497** |100 nF, ±10%, **1206, 50 V, X7R, Basic** | **UNVERIFIED current JLC stock**; fetched page exposes no count |
| BOM-09 | CI2, CI4 /2 | Samsung CL31A106KBHNNNE / **C13585** |10 µF, ±10%,1206,50 V,X5R,Basic | **UNVERIFIED current JLC stock** |

BOM-05 [JLC part page](https://jlcpcb.com/partdetail/CL31B104KBCNNNC/C24497) checked **2026-10-30**; specs/Basic also confirmed by MCP that date. BOM-09 [JLC page](https://jlcpcb.com/partdetail/14236-CL31A106KBHNNNE/C13585) checked2026-10-29, MCP identity/class rechecked2026-10-30. Older indexed LCSC/EasyEDA counts conflict and are not substituted for JLC assembly inventory. The requested numerical stock verification remains incomplete. Browser fallback failed: browser access host unavailable.

## BOM-19 — three lowest-price matching candidates retrieved

All330 Ω,1206,±1%,250 mW. Ranked at the **same100-piece LCSC price break**, not reel price; not an exhaustive global ranking. Retrieved **2026-10-30**: indexed LCSC observations, **not live JLC assembly stock or quote prices**. MCP verified all three **Extended**. No Basic/Preferred match found.

| Rank | MPN / LCSC | USD each,100+ | Indexed stock | Class | Voltage |
|---|---|---:|---:|---|---:|
|1|UNI-ROYAL1206W4F3300T5E / **C17930**|0.0048|223,400 (index:last week)|Extended|200 V|
|2|RALEC RTT063300FTP / **C104763**|0.0067|4,700 (index:last month; another URL4,200)|Extended|150 V|
|3|YAGEO RC1206FR-07330RL / **C114944**|0.0082|182,000 (index:3 days ago; older URL74,200/$0.0072)|Extended|200 V|

Sources: [C17930](https://www.lcsc.com/product-detail/C17930.html?is_substitute=1&original_product_code=C965000&original_unit_price=0.0072), [C104763](https://www.lcsc.com/product-image/C104763.html?whichImg=0), [C114944](https://www.lcsc.com/product-image/C114944.html). Conflicting index observations disclosed; current stock/price **UNVERIFIED**. No resistor assigned.

**Recommend BOM-19=C17930, conditional on live assembly stock/price confirmation.** Cheapest retrieved candidate; retains previously proposed200 V rating. C104763 is comparison only, with lower voltage. Historical resistor tolerance/power/voltage are unspecified; equality to an unknown SKU cannot be proved. User's explicit330 Ω/1%/¼ W/1206 target is met. Standing rule: where Basic is unavailable, propose cheapest verified in-stock Preferred/Extended equivalent; obtain BOM-ID approval.

**Fee impact:** C17930 adds one Extended type:8x3 known count **2→3**, or **4 with either undecided LED**; decoder unresolved. [Standard fees](https://jlcpcb.com/help/article/pcb-assembly-price), checked2026-10-30: **$1.53 per Basic or Extended type**. Resistor feeder contribution+$1.53/order; **Extended-vs-Basic premium $0** in Standard. Two approved capacitors add0 Extended types. [Family/order totals](SIZE_ORDER_PLAN.md).

CHG-009 remains Verified:R1–R8=330, Value only. CHG-007/008 not applicable to8x3 (no zones). CHG-012 **PARKED**, skip accepted. CHG-016 excludes19 hand components from both future BOM/CPL. Last native checks:DRC0 errors/114 warnings/0 unconnected; ERC0 errors/230 warnings. No new CAD edits warranted another run.

Needs from you: approve/reject **BOM-19 C17930**, conditional on live stock/price; current JLC counts for C24497/C13585 still need capture before release.
