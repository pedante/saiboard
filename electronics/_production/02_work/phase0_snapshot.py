"""One-shot Phase 0 inventory and verified snapshot; refuses an existing snapshot."""
from collections import Counter
from datetime import datetime, timezone
import csv
import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile


ROOT = Path(__file__).resolve().parents[2]
PROD = ROOT / "_production"
AUDIT = PROD / "01_audit"
SNAPSHOT = PROD / "00_original_snapshot"
assert ROOT.name == "electronics"
assert not SNAPSHOT.exists(), "Refusing to overwrite the original snapshot"


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def originals():
    return sorted(p for p in ROOT.rglob("*") if "_production" not in p.relative_to(ROOT).parts)


def utc(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat()


entries = originals()
assert all(not p.is_symlink() for p in entries), "Review symlinks before snapshotting"
assert all(p.is_file() or p.is_dir() for p in entries), "Unexpected filesystem object"
files = [p for p in entries if p.is_file()]
types = {
    ".kicad_pcb": "KiCad PCB (S-expression)",
    ".kicad_sch": "KiCad schematic (S-expression)",
    ".kicad_pro": "KiCad project (JSON)",
    ".kicad_prl": "KiCad local settings (JSON)",
    ".kicad_sym": "KiCad symbol library (S-expression)",
    ".gbr": "Gerber fabrication layer",
    ".gbrjob": "Gerber job (JSON)",
    ".drl": "Drill file", ".zip": "ZIP archive", ".pdf": "PDF",
    ".jpg": "JPEG", ".csv": "CSV", ".json": "JSON",
    ".md": "Markdown", ".gcode": "3D printer G-code",
    ".f3d": "Fusion design archive", ".lck": "KiCad lock file",
}
rows = []
for p in files:
    stat = p.stat()
    rows.append({"path": str(p.relative_to(ROOT)), "type": types.get(p.suffix, "KiCad library table" if p.name == "sym-lib-table" else "UNVERIFIED"),
                 "size_bytes": stat.st_size, "modified_utc": utc(stat.st_mtime),
                 "mtime_ns": stat.st_mtime_ns, "sha256": digest(p)})

for name in ["01_audit", "02_work", "03_output", "docs"]:
    (PROD / name).mkdir(exist_ok=True)
SNAPSHOT.mkdir()
for p in entries:
    target = SNAPSHOT / p.relative_to(ROOT)
    if p.is_dir():
        target.mkdir(exist_ok=True)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)

assert entries == originals(), "Source file/directory list changed during snapshot"
for row in rows:
    src, dst = ROOT / row["path"], SNAPSHOT / row["path"]
    assert digest(src) == digest(dst) == row["sha256"], row["path"]
    assert src.stat().st_size == dst.stat().st_size == row["size_bytes"]
    assert src.stat().st_mtime_ns == dst.stat().st_mtime_ns == row["mtime_ns"]
    dst.chmod(dst.stat().st_mode & ~0o222)
for p in sorted(SNAPSHOT.rglob("*"), reverse=True):
    if p.is_dir():
        p.chmod(p.stat().st_mode & ~0o222)
SNAPSHOT.chmod(SNAPSHOT.stat().st_mode & ~0o222)

with (AUDIT / "SOURCE_INVENTORY.csv").open("x", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
(AUDIT / "SOURCE_SHA256SUMS.txt").write_text("".join(f'{r["sha256"]}  {r["path"]}\n' for r in rows))
md = ["# Phase 0 source inventory", "", "Paths are relative to electronics/. `_production/` is excluded. File types identify containers, not manufacturing validity. Timestamps are UTC filesystem metadata, not proof of design chronology.", "", "| Path | Type | Bytes | Modified (UTC) | SHA-256 |", "| --- | --- | ---: | --- | --- |"]
md.extend(f'| `{r["path"]}` | {r["type"]} | {r["size_bytes"]} | {r["modified_utc"]} | `{r["sha256"]}` |' for r in rows)
(AUDIT / "SOURCE_INVENTORY.md").write_text("\n".join(md) + "\n")

formats, archives = [], []
for row in rows:
    p = SNAPSHOT / row["path"]
    if p.suffix in {".kicad_pcb", ".kicad_sch", ".kicad_sym"}:
        with p.open() as stream:
            header = stream.read(512)
        version, generator = re.search(r"\(version ([^)]+)\)", header), re.search(r"\(generator ([^)]+)\)", header)
        assert version and generator, row["path"]
        formats.append({"path": row["path"], "format_version": version.group(1), "generator": generator.group(1), "exact_editor_build": "UNVERIFIED: not recorded in header"})
    elif p.suffix in {".kicad_pro", ".gbrjob"}:
        data = json.loads(p.read_text())
        formats.append({"path": row["path"], "metadata": data.get("meta", data.get("Header"))})
    elif p.suffix == ".zip":
        with zipfile.ZipFile(p) as archive:
            assert archive.testzip() is None, row["path"]
            for member in archive.infolist():
                data = archive.read(member) if not member.is_dir() else b""
                item = {"archive": row["path"], "member": member.filename, "type": "directory" if member.is_dir() else "file", "size_bytes": member.file_size,
                        "zip_modified_local_unspecified_timezone": list(member.date_time), "sha256": hashlib.sha256(data).hexdigest() if not member.is_dir() else None}
                if row["path"] == "kicad_files/8x8/8x8.kicad_.zip" and not member.is_dir():
                    sibling = p.parent / member.filename
                    item["matches_loose_source_sha256"] = sibling.is_file() and digest(sibling) == item["sha256"]
                archives.append(item)
(AUDIT / "SOURCE_FORMATS.json").write_text(json.dumps(formats, indent=2) + "\n")
(AUDIT / "ARCHIVE_INVENTORY.json").write_text(json.dumps(archives, indent=2) + "\n")
verification = {"checked_at_utc": utc(datetime.now(timezone.utc).timestamp()), "source_root": str(ROOT), "snapshot_root": str(SNAPSHOT),
                "file_count": len(rows), "directory_count": sum(p.is_dir() for p in entries), "total_bytes": sum(r["size_bytes"] for r in rows),
                "types": dict(Counter(r["type"] for r in rows)), "source_and_snapshot_hash_size_mtime_match": True,
                "snapshot_write_bits_removed": True, "zip_crc_checks_passed": True, "source_paths_unchanged": True,
                "directories": [str(p.relative_to(ROOT)) for p in entries if p.is_dir()],
                "native_tool_paths": {name: shutil.which(name) for name in ["kicad-cli", "kicad", "eeschema", "pcbnew"]}}
(AUDIT / "SNAPSHOT_VERIFICATION.json").write_text(json.dumps(verification, indent=2) + "\n")
print(json.dumps({key: value for key, value in verification.items() if key not in {"directories", "source_root", "snapshot_root"}}, indent=2))
