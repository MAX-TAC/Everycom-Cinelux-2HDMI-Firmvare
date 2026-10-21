#!/usr/bin/env python3
"""Targeted read-only comparison of tvconfig ConfigDefaultValue.ini in Oct 8052 vs Sep 8054.
Reuses original verified factory archive metadata artifact; avoids publishing proprietary raw config.
"""
from pathlib import Path
import collections,difflib,json,re,subprocess
base=Path("/tmp/stock-8054/8054.json")
if not base.is_file():
    raise FileNotFoundError("Expected verified stock board metadata artifact "+str(base))
old=json.loads(base.read_text())["files"]["ConfigDefaultValue.ini"]["text"].splitlines()
img=Path("/tmp/images/tvconfig.img")
p=subprocess.run(["debugfs","-R","cat /platform/data/misc/ConfigDefaultValue.ini",str(img)],
                 capture_output=True,timeout=50)
if p.returncode or not p.stdout:
    raise RuntimeError("Extract failed: "+p.stderr.decode(errors="replace")[-250:])
new=p.stdout.decode("utf-8","replace").splitlines()
def redact(line):
    if line.strip()=="# [redacted]":return "[sensitive key redacted]"
    if re.search(r"(?i)(ssid|password|passwd|private.?key|serial[_ -]?number|token|mac[_ -]?address|hdcp|widevine|certificate|device.?key|license)",line):
        return "[sensitive key redacted]"
    return line[:270]
matcher=difflib.SequenceMatcher(None,[redact(x) for x in old],[redact(x) for x in new],autojunk=False)
opcodes=[(tag,a0,a1,b0,b1) for tag,a0,a1,b0,b1 in matcher.get_opcodes() if tag!="equal"]
changes=[]
for tag,a0,a1,b0,b1 in opcodes:
    changes.append({"operation":tag,"stock_line_range":[a0+1,a1],
                    "ota_line_range":[b0+1,b1],
                    "stock_preview":[redact(s) for s in old[a0:a1][:25]],
                    "ota_preview":[redact(s) for s in new[b0:b1][:25]],
                    "stock_line_count":a1-a0,"ota_line_count":b1-b0})
out=Path("analysis/Latest_8052_OTA_vs_8054_Stock")
out.mkdir(parents=True,exist_ok=True)
data={"file":"tvconfig/platform/data/misc/ConfigDefaultValue.ini",
      "stock_lines":len(old),"ota_lines":len(new),
      "changed_blocks":len(opcodes),
      "added_lines":sum(b1-b0 for _,_,_,b0,b1 in opcodes),
      "removed_lines":sum(a1-a0 for _,a0,a1,_,_ in opcodes),
      "changes":changes}
(out/"default_config_diff.json").write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n")
md=["# Image and source defaults: ConfigDefaultValue.ini, Oct 8052 vs Sep 8054",
"",
"Factory 8054 metadata was extracted from the SHA-verified stock PKG in GitHub Actions run 39452884650.",
"October 8052 file was extracted read-only from the verified OTA payload.",
"",
"Stock lines: "+str(len(old))+"; OTA lines: "+str(len(new))+
"; changed blocks: "+str(len(opcodes))+
"; removed/added lines: "+str(data["removed_lines"])+"/"+str(data["added_lines"])+".",
"",
"Note: differences in config text can be changed defaults, comments or firmware version updates; not proof of physical board differences.",
"",
"## Changed ranges and sanitized excerpts",""]
for i,chg in enumerate(changes[:45],1):
    md+=["### Change "+str(i)+" ("+chg["operation"]+")",
         "Stock lines "+str(chg["stock_line_range"])+", OTA lines "+str(chg["ota_line_range"]),"",
         "8054 stock:"]
    md+=["- "+s.replace("|","/") for s in chg["stock_preview"]]
    md+=["","8052 OTA:"]
    md+=["- "+s.replace("|","/") for s in chg["ota_preview"]]
    md+=[""]
md+=["## Interpretation","",
"- The repeated changed rows are within InputSourceID[0] through InputSourceID[11]; each relevant row is 70,75,50 in stock 8054 and 80,75,50 in OTA 8052.",
"- Exact meaning of that InputSourceID table row is unverified; do not interpret 80/70 as a HDMI port count or brightness unit.",
"- Do not swap the entire file across profiles based only on a small diff.",
"- Determine which of the changed keys influences input source, picture defaults, brightness and panel calibration before changing values.",
"- Read-only static evidence: no GPIO, I2C, flash or display setting was modified.",
""]
(out/"default_config_diff.md").write_text("\n".join(md)+"\n")
print("DIFF ConfigDefaultValue.ini blocks",len(opcodes),"lines",len(old),len(new),flush=True)
for row in changes[:8]:print("CHANGE",row["operation"],row["stock_preview"][:5],row["ota_preview"][:5],flush=True)
