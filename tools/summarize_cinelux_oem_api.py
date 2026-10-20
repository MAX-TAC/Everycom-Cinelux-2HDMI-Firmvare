#!/usr/bin/env python3
"""Generate a concise auditable interface map from static signature metadata."""
import json,re
from pathlib import Path
root=Path("analysis/OEM_API_8052_Latest")
root.mkdir(parents=True,exist_ok=True)
raw=json.loads(Path("/tmp/oem-api/8052-ota.json").read_text())
groups=[
("Settings I2C and hardware","TvSettingsPlus","ProjectorManager|I2CDevice|FocusSettingsSecondaryController|ProjectionModeSecondaryController|AdvanceSettingsSecondaryController|SourceSubMenuController|i2c"),
("Factory engineering interface","Factory","ProjectorManager|I2CDevice|FanActivity|i2c"),
("Focus motor, camera and ToF","RuiAutoFocus","RuiCameraApi|Motor|Tof|Focus"),
("Keystone geometry","KeystoneCorrection","KeystoneUtil|Trapezoid|Keystone|Mirror|i2c"),
("HDMI inputs","KuSourceRJ","BootSoure|SourceSubMenu|hd2Focus|TofAutofocus|Source|HDMI"),
("Binder control interface","trdmiddle","IProjectorCtrl|ITofCtrl|ITrdSystemService|TrdSystemManager|TofCtrl|Motor"),
("Event service","trdservice","TrdService|TrdSystemManager|RJFocusDialog|IKeyEventCtrl"),
("OEM settings","KuSettings","Bluetooth|Sound|Projector|Source|Display|I2C")
]
lines=[
"# OEM settings and hardware interfaces — RUIOS 8052 latest OTA",
"",
"Read-only static study of SHA256-verified OTA 8052 Oct 2026 (one HDMI).",
"App signatures extracted via JADX. JNI dynamic symbols collected with readelf.",
"No proprietary decompiled Java source is committed.",
"No code has been executed on a real projector. Interfaces remain unverified at runtime.",
"",
"## APK inventory",
"",
"| App | Package | Classes | JNI libraries | Selected privileged permissions |",
"|---|---|---:|---|---|"]
for name,row in raw["apps"].items():
    if row.get("missing"):
        lines.append("| "+name+" | Missing | — | — | — |")
        continue
    perms=[s for s in row["permissions"] if re.search("BLUETOOTH|WRITE_SECURE|MANAGE|CONTROL|INTERACT|REBOOT|HDMI",s,re.I)]
    lines.append("| "+name+" | "+str(row.get("package"))+" | "+str(row.get("decompiled_class_count",0))+" | "+
                 (", ".join(row.get("jni_loads",[])) or "—")+" | "+(", ".join(perms[:6]) or "—")+" |")
for title,name,pattern in groups:
    item=raw["apps"].get(name,{})
    reg=re.compile(pattern,re.I)
    matches=[x for x in item.get("declarations",[]) if reg.search(x["class"]+" "+x["signature"])]
    lines+=["","## "+title+" — "+name,""]
    for m in matches[:100]:
        lines.append("- "+m["class"]+" :: "+m["signature"]+(" [native]" if m.get("jni") else ""))
    if not matches:lines.append("- No matching declaration surfaced; inspect the structured JSON.")
    calls=[x for x in item.get("call_sites",[]) if reg.search(x["class"])]
    if calls:
        lines+=["","Call-site identifiers (without proprietary Java body):",""]
        lines += ["- "+x["class"]+" line "+str(x["line"])+": "+", ".join(x["calls"]) for x in calls[:30]]
    if item.get("related_actions"):
        lines+=["","Referenced intent actions (strings only):",""]
        lines += ["- "+x for x in item["related_actions"][:15]]
lines+=["","## Relevant JNI/native exports",""]
for filename,row in sorted(raw["native"].items()):
    lines+=["","### "+filename,""]
    if "error" in row:
        lines.append("- Error: "+row["error"])
    else:
        lines += ["- SHA256: "+row["sha256"],
                  "- Dependencies: "+(", ".join(row.get("deps",[])) or "none listed"),
                  "- Relevant dynamic symbol names: "+str(len(row["candidate_export_symbols"]))]
        lines += ["- "+name for name in row["candidate_export_symbols"][:80]]
lines+=["","## Bluetooth output routing evidence",""]
for filename,row in sorted(raw["bluetooth_audio"].items()):
    lines+=["","### "+filename,"",
            "- A2DP mentions: "+str(row["a2dp_mentions"]),
            "- LE audio mentions: "+str(row["le_audio_mentions"]),
            "- The existence of a Bluetooth audio policy does not confirm simultaneous output to 2 A2DP devices."]
    lines += ["- "+l for l in row["hits"][:25]]
lines+=["","## Safe integration path","",
"1. Prefer OEM settings activities and existing Binder service over direct hardware I2C access.",
"2. Identify actual package export flags and Binder service registration on a real device before implementing a companion.",
"3. Use separate hardware profiles for one-HDMI 8052 and two-HDMI/ToF 8054.",
"4. Bound motor steps, preserve emergency stop, and verify ToF presence and privileges before tests.",
"5. Treat HDMI selection, image options, and keystone separately; keep stock services until tested.",
"6. For two Bluetooth headphones, inspect A2DP source multiplicity, Android audio routing, BT stack and HAL. App-level audio duplication alone does not guarantee support.",
"7. Keep the stock, device-matched initial setup application. Do not import 8053 Provision or A2DP sink functionality.",
"",
"## Limits","",
"- Decompiled signatures and JNI exports are not a public supported SDK.",
"- Exact Binder permissions, I2C bus and register semantics are not yet determined.",
"- No OEM JNI method was executed; there was no flashing or calibration write.",
""]
(root/"README.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
for value in raw["apps"].values():
    if len(value.get("declarations",[]))>500:value["declarations"]=value["declarations"][:500]
    if len(value.get("call_sites",[]))>200:value["call_sites"]=value["call_sites"][:200]
(root/"8052-ota.json").write_text(json.dumps(raw,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("REPORT",len(lines),"lines; libs",len(raw["native"]),"APKs",len(raw["apps"]),flush=True)
print("\n".join(lines[:45]),flush=True)
