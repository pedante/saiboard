# Tile and board BOM totals

Updated2026-10-30. User provisionally confirmed the tile mix. Full local-search results: [search report](ORDER_INSTRUCTIONS_SEARCH.md). Order quantities,unique groups,Extended fees and cost limits: [plan](SIZE_ORDER_PLAN.md).

Original count check2026-10-29.  Electronics README explicitly states 19×19 pixels. The inspected root/electronics/board README files do NOT explicitly give tile quantities. The photos inspected do not establish the assembled tile layout. Thus 1×11x3 +1×8x3 +2×3x8 +4×8x8 is arithmetically consistent (361 pixels), but repo-document confirmation remains UNVERIFIED. Board totals below are conditional on that proposed population; no other population is assumed.

| BOM-ID / source |11x3|8x3|3x8|8x8|Board (conditional)|
|---|---:|---:|---:|---:|---:|
|BOM-01 SKC6812RGBW-WS|33|24|24|64|361|
|BOM-02 AH49E|33|24|24|64|361|
|BOM-03 Power_top_side_a/Power_top/Hall_top/PQ_side_b/LedOut_side_b/LedOut_side_a/PQ_side_a/LedIn_side_a/LedIn_side_b|3|0|4|2|19|
|BOM-04 2N3906|11|8|0|0|19|
|BOM-05 C104|37|27|25|64|370|
|BOM-06 esp32s3left/esp32s3right|2|0|0|0|2|
|BOM-07 PQ_side_a/Touch_bottom_side_b/PQ_side_b/Touch_side_b/IC_bottom_side_a/IC_bottom_side_b/Touch_side_a/Touch_bottom_side_a/Hall_bottom_side_a/Hall_bottom_side_b/Conn_side_b/IC/Touch/Hall_top/LedIn/LedIn_top|16|14|5|5|60|
|BOM-08 PQ_bottom_side_b/PQ_bottom_side_a/Power_bottom_side_a/Power_bottom_side_b/Power_side_a/Power_side_b/Conn_side_a/Led/Hall/LedIn_side_a/LedIn_side_b|6|5|0|0|11|
|BOM-09 C106|2|2|0|0|4|
|BOM-10 Power_top_side_b/IC_top_2/IC_top_1/Touch_top/Touch_side_b/IC_side_b/Touch_side_a/Hall_side_b/Hall_side_a/IC_side_a/Hall_bottom/PQ_side_a/PQ_side_b/LedOut_bottom|4|0|6|15|76|
|BOM-11 Power_Terminal/Power_RaspberryPi|2|0|0|0|2|
|BOM-12 330|11|0|0|0|11|
|BOM-13 SN74LV1T34|1|0|0|0|1|
|BOM-14 AMS1117-3.3|1|1|0|0|2|
|BOM-15 74HCT154D|1|0|0|0|1|
|BOM-16 220|1|0|0|0|1|
|BOM-17 1000 µF|1|0|0|0|1|
|BOM-18 74HCT138|0|1|0|0|1|
|BOM-19 330 ohm (CHG-009)|0|8|0|0|8|
|BOM-20 74hc4052D|0|0|1|0|2|
|All electronic instances|165|114|89|214|1313|
|Hand-populated|33|19|15|22|170|
|JLC candidates incl undecided LEDs|132|95|74|192|1143|

Mechanical holes, external modules and assembly spares excluded. Counts are components, not unique SKUs. The approved 87+2 hand count is one of each design; full-board multiplication changes it.

Needs from you: location of the author’s exact ordering instructions; provisional confirmation is already recorded.
