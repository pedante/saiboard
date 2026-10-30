# Decision 02 — one LED across all four tiles

Checked **2026-10-30**. **Recommend rollback of CHG-004 across all four, identity fields only, and the RGB C5378720 candidate, subject to approval and JLC placement preview.** This keeps the original RGB format. Historical purchased manufacturer/revision is unknown: repo document LED COLOR, current candidate OPSCO. It is not claimed to be the exact historical SKU. No rollback or LED ordering-BOM assignment applied.

| Item | Original documented SK6812 | Available RGB candidate | Provisional RGBW candidate |
|---|---|---|---|
|Identity|LED COLOR SK6812,Rev01|OPSCO SK6812; linked sheet SK6812-012 B/1,2025-08-11; **C5378720**|OPSCO **SKC6812RGBW-WS/C5378724**, family B/1,2025-07-31|
|JLC status|Exact historical SKU **UNVERIFIED**|Found,**Extended**,Standard-only; indexed stock90,799/orderable88,810|Found,**Extended**; indexed stock74,695/orderable72,252|
|Pixel format|24-bit GRB:3 bytes|24-bit GRB:3 bytes|32-bit GRBW:4 bytes|
|Supply|5 V nominal|3.7–5.5 V|3.5–5.5 V|
|11x3,D1–33|PASS*|PASS*|PASS*|
|8x3,D1–24|PASS*|PASS*|PASS*|
|3x8,D1–24|PASS*|PASS*|PASS*|
|8x8,D1–64|PASS*|PASS*|PASS*|

**PASS* criterion:** nominal package contacts overlap the correct retained lands, without nominal pin-location conflict. This is a dimensional screen, not tolerance/reflow qualification or JLC acceptance. All145 LED footprints identical: lands1.5×1.0 mm, centres x=±2.45,y=±1.60; pins1=GND,2=DIN,3=VDD,4=DOUT. Right lower land x1.70–3.20,y1.10–2.10. Contact bounds: original x1.70–2.70,y1.10–2.10; current RGB x1.70–2.70,y1.10–2.00; RGBW x1.70–2.50,y1.15–2.05. Others mirror these. OPSCO recommended lands1.8×1.2 are **not identical** to retained lands. Zero nominal heel margin/drawing tolerances remain a JLC match/preview check; no footprint edit proposed. A manufacturer FAIL on any tile rejects the option for all four.

**Protocol advisory:** RGB stays3 bytes, but specifies reset>200 µs and T1H0.65–1.00 µs versus original reset80 µs and T1H0.60±0.15 µs. Its sheet advises70% grayscale when lighting all three colours. RGBW needs4 bytes. Verify on prototype; **no firmware edits**. Full power qualification remains PARKED.

**Rule applied:** a purchasable RGB SK6812 candidate exists and passes this nominal fit screen, favouring rollback. Exact historical-SKU availability remains unverified; do not infer RGB is unavailable and automatically retain RGBW. CHG-004 remains Applied-provisional until decision; no mixed pixels. Either choice adds one Extended type per tile order ($1.53 Standard feeder contribution).

Sources checked2026-10-30: [RGB JLC](https://jlcpcb.com/partdetail/C5378720), [LCSC-linked RGB sheet](https://item.szlcsc.com/6242291.html), [saved pp4–5](C5378720.pdf), [original pp2–3](../../00_original_snapshot/datasheets/SK6812.pdf), [RGBW JLC](https://jlcpcb.com/partdetail/SKC6812RGBW-WS/C5378724), [RGBW pp5–7](../../00_original_snapshot/updated_components_SKC6812RGBW-WS/datasheets/OPSCO_SKC6812RGBW_RevB1_2025-07-31.pdf). Stock from indexed JLC pages (crawl:last month); **live stock UNVERIFIED**, not reserved.

Needs from you: approve/reject **CHG-004 rollback on all four + RGB C5378720 candidate (CHG-023)**. Import preparation waits for this decision.
