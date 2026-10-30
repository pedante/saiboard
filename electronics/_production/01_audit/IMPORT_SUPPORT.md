# Import support and tool readiness

Checked: **2026-10-29**. No import or conversion was attempted.

## Exposed MCP surface

The session exposes **101 EasyEDA Pro tools**, listed individually in [EASYEDA_TOOLS.md](EASYEDA_TOOLS.md). No EasyEDA Standard tool is exposed. The EasyEDA MCP server and extension report 1.6.0; the bridge reports 1.0.0 and a connected state. The active server profile is `pro`. These are connector versions, not the editor version. The actual EasyEDA editor build is **UNVERIFIED**, because the health and bridge responses omit it.

No currently exposed MCP tool accepts a KiCad archive, schematic, PCB, EasyEDA Standard JSON or EasyEDA Pro archive for project import. Consequently **no external-design file-import format is verified through this MCP surface**. `schematic_sync_to_pcb` transfers an already-open schematic's changes and requires a human dialog; it is not a project-file importer.

The bridge advertises `project.open`, `api.call` and `pcb.rebuildCopper`, but no corresponding callable tools are exposed here. The runtime inventory reports 84 API classes. It lists existing project/document open methods and route-result import methods, not a general KiCad project import method. Enumerating an API does not authorize or enable calling it. No server profile, settings or installation was changed.

Gerber/drill, BOM and CPL export tools are exposed, but export success and format compliance are untested. Native EasyEDA DRC requires a focused PCB and returns aggregate severity counts; detailed violations remain in the UI. Native ERC requires a focused schematic; some multi-page operations explicitly fail closed. Inferred ERC is not a replacement for native checks or verified pin types. Direct PCB pad-geometry reads and copper-refill execution are not established by the exposed tools.

## Vendor-documented application formats (distinct from MCP support)

| Route | Documented formats | Limit / local status | Official source, checked 2026-10-29 |
| --- | --- | --- | --- |
| EasyEDA Pro native project/library import | Project ZIP / `.epro`; libraries `.elibz`, `.esym`, `.efoo`, `.epanl` | UI operation; not exposed by the present MCP tools. Not attempted. | [Import EasyEDA Pro](https://prodocs.easyeda.com/en/import-export/import-easyeda-pro/) |
| EasyEDA Pro direct KiCad import | KiCad-packaged project ZIP and library files; guide explicitly names KiCad 5.1 and 5.9 | Use KiCad's package function to include libraries. Guide warns that PCB import rebuilds copper, so fidelity must be checked. The supplied numeric file-format versions are not expressly covered by those version claims. | [Import KiCad](https://prodocs.easyeda.com/en/import-export/import-kicad/index.html) |
| Separate EasyEDA Pro Format Converter | KiCad ZIP, `.lib`, `.mod`, `.kicad_mod`, `.kicad_wks`, `.kicad_sym`, `.sch`, `.kicad_sch`, `.kicad_pcb`; project extension entry is printed as `.pro.kicad_pro` in the source | That project-extension spelling is ambiguous; not silently corrected. Converter availability and support for these exact local revisions are UNVERIFIED. Installation would require separate permission. | [Format Converter](https://prodocs.easyeda.com/en/import-export/easyeda-pro-format-converter/) |
| Same separate converter: other advertised families | Altium, Allegro/OrCAD, PADS, EAGLE, EasyEDA Standard | Vendor lists family-specific extensions; this is not evidence of an MCP importer. Not needed or tested for this project. | [Format Converter](https://prodocs.easyeda.com/en/import-export/easyeda-pro-format-converter/) |

The converter documentation also warns about conversion differences and repeated conversions. A documented extension alone does not establish lossless import. Phase 5 must compare components, connectivity, outline, layers, pad geometry and rebuilt copper before accepting a converted copy. No alternate design, autorouting or reconstruction is authorized.

## Native source checks

No `kicad-cli`, `kicad`, `eeschema` or `pcbnew` executable was found on the local PATH. The available KiCad MCP server reports version 4.4.0, missing `/usr/bin/kicad-cli`, unavailable IPC, and disabled native file-backed DRC/ERC/export. Its configured project is a different workspace; it was neither read as design evidence nor changed. See [KICAD_READINESS.json](KICAD_READINESS.json).

This blocks completing the native source ERC/DRC requirement with the current environment. Static parsing can support Phase 1 comparison after approval, but cannot be reported as a native ERC/DRC pass. No installation or configuration change has been made.

## Evidence

- [EASYEDA_TOOL_CATALOG_RAW.json](EASYEDA_TOOL_CATALOG_RAW.json): exact session tool descriptions and schemas.
- [EASYEDA_HEALTH.json](EASYEDA_HEALTH.json), [EASYEDA_CAPABILITIES.json](EASYEDA_CAPABILITIES.json), [EASYEDA_BRIDGE_STATUS.json](EASYEDA_BRIDGE_STATUS.json): read-only MCP replies.
- [EASYEDA_API_INVENTORY.json](EASYEDA_API_INVENTORY.json): live runtime API inventory, without invocation.
- [SOURCE_FORMATS.json](SOURCE_FORMATS.json): numeric versions and historical exporter metadata read from the snapshot.

No JLCPCB stock, fees, capabilities or fabrication format requirements were evaluated in Phase 0. Those checks remain assigned to their requested phases.
