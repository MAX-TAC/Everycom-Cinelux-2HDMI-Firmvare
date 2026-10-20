#!/usr/bin/env python3
"""Read-only, public, non-secret hardware markers in two RUIOS OTA packages."""
import argparse
import collections
import hashlib
import json
import re
import struct
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--code", choices=("8052", "8053"), required=True)
parser.add_argument("--vendor-root", type=Path, required=True)
parser.add_argument("--images", type=Path, required=True)
parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args()
args.out.mkdir(parents=True, exist_ok=True)
props_path = args.vendor_root / "build.prop"
assert props_path.is_file(), f"Missing vendor build.prop: {props_path}"
raw_properties = props_path.read_text(encoding="utf-8", errors="replace")
all_props = {}
for line in raw_properties.splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        name, value = line.split("=", 1)
        all_props[name.strip()] = value.strip()

public_names = [
    "ro.rjpj.machine.id", "ro.rjpj.yunota.version",
    "ro.rjpj.yunota.baseurl", "ro.rjpj.yunota.url", "ro.rjpj.yunota.zip",
    "ro.rjpj.hdmi.ports", "ro.rjpj.hdmi.port.count",
    "ro.rjpj.support.toffunction", "ro.rjpj.autokeystone.poweron",
    "ro.rjpj.autokeystone.move", "ro.rjpj.autofocus.poweron",
    "ro.rjpj.gitrev", "ro.rjpj.buildtime",
    "ro.product.board", "ro.soc.model", "ro.build.ab_update",
    "ro.product.first_api_level",
]
visible = {k: all_props.get(k) for k in public_names}
dtbo_path = args.images / "dtbo.img"
blob = dtbo_path.read_bytes()
magic, total, header_len, entry_len, count, offset, page_size, version = struct.unpack(">8I", blob[:32])
assert magic == 0xD7B7AB1E and 0 < count < 1000 and entry_len >= 32
dtbo_records = []
for index in range(count):
    entry = blob[offset + index * entry_len: offset + index * entry_len + 32]
    dt_size, dt_offset, board_id, rev, c0, c1, c2, c3 = struct.unpack(">8I", entry)
    assert 0 < dt_size < len(blob) and dt_offset + dt_size <= len(blob)
    dtb = blob[dt_offset:dt_offset + dt_size]
    assert dtb[:4] == bytes.fromhex("d00dfeed")
    dtbo_records.append({"index": index, "size": dt_size, "id": board_id, "rev": rev, "sha256": hashlib.sha256(dtb).hexdigest()})

def from_ext4(image_name, file_name):
    image = args.images / (image_name + ".img")
    if not image.is_file():
        return None
    run = subprocess.run(["debugfs", "-R", "cat /" + file_name, str(image)],
                         capture_output=True, timeout=40)
    if run.returncode or not run.stdout:
        return {"error": run.stderr.decode("utf-8", errors="replace")[-250:]}
    data = run.stdout
    text = data.decode("utf-8", errors="replace")
    relevant = []
    for line in text.splitlines():
        # Filter long records; expose hardware labels only, no serials/calibration contents.
        if len(line) <= 180 and re.search(r"(?i)(hdmi|tof|panel|board|dtbo|cec|input|gpio)", line):
            if not re.search(r"(?i)(serial|mac|password|secret|token|private|key|uuid|imei)", line):
                relevant.append(line.strip())
        if len(relevant) >= 35:
            break
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "preview_lines": relevant}

result = {
    "code": args.code,
    "source": "verified stock OTA; vendor/DTBO/tvconfig/bootdata extracted without flashing",
    "vendor_prop_public": visible,
    "vendor_prop_sha256": hashlib.sha256(raw_properties.encode()).hexdigest(),
    "dtbo": {"entry_count": count, "table_bytes": total,
             "entries": dtbo_records},
    "tvconfig_board_ini": from_ext4("tvconfig", "bsp/board/BD_MT5873_H1V1_B6_S/board.ini"),
    "tvconfig_dtbo_mapping": from_ext4("tvconfig", "config/dtbo_mapping.ini"),
    "bootdata_dtbo_mapping": from_ext4("bootdata", "config/dtbo_mapping.ini"),
}
output = args.out / (args.code + ".json")
output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
print("CODE", args.code, flush=True)
print("PROPS", json.dumps(visible, ensure_ascii=False, indent=2), flush=True)
print("DTBO", count, "entries; hashes", len(set(x["sha256"] for x in dtbo_records)), flush=True)
for n in ("tvconfig_board_ini", "tvconfig_dtbo_mapping", "bootdata_dtbo_mapping"):
    v=result[n]
    print(n, (v or {}).get("sha256", (v or {}).get("error")), flush=True)
